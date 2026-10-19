"""Shared lifecycle for the animated simulations: window, headless run and reel.

Every simulation script follows the same three-part pattern:

* a state class derived from ``Simulation``: ``step()`` performs one solver
  iteration, ``advance(n)`` repeats it and counts ``steps``;
* a view class derived from ``View``: it builds its artists on a figure and
  ``draw()`` updates them from the state without advancing it;
* an ``Animation`` describing the title, output name and frame grouping, whose
  ``parser`` and ``run`` methods implement the command line.

A view is a pure function of the state, so the live window, the ``--output``
PNG and the ``--reel`` video all show the same picture for the same state.
Matplotlib is imported lazily so that ``--help`` stays inexpensive.
"""

import shutil
import subprocess
import textwrap
import time
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import count
from pathlib import Path

from _common import create_parser, positive_float, positive_int, save_figure

REEL_SIZE = (1080, 1920)  # pixels, 9:16 portrait for Shorts and Reels
REEL_DPI = 100
REEL_HOLD_SECONDS = 2.0  # the final frame is held this long at the end
# Height of the title band, simulation panel and status band (sums to 1920 px).
# The bands keep text clear of the app overlays at the top and bottom.
REEL_BANDS = (440, 1060, 420)
BACKGROUND = "black"

STYLE = {
    "figure.facecolor": BACKGROUND,
    "axes.facecolor": BACKGROUND,
    "savefig.facecolor": BACKGROUND,
    "axes3d.xaxis.panecolor": BACKGROUND,
    "axes3d.yaxis.panecolor": BACKGROUND,
    "axes3d.zaxis.panecolor": BACKGROUND,
    "axes.grid": False,
    "grid.color": "0.3",  # gridlines, including 3D panes, stay dim on black
    "image.origin": "lower",
}
# Text is read on a phone: everything in a reel is drawn larger.
REEL_STYLE = {
    "font.size": 20,
    "axes.titlesize": 24,
    "axes.labelsize": 22,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "legend.fontsize": 18,
    "lines.linewidth": 3,
}


class Simulation:
    """Solver state advanced one iteration at a time.

    Subclasses call ``super().__init__()``, implement ``step()`` and set ``dt``
    (or override ``time``). Solvers that converge or finish override ``done``;
    ``advance`` then stops early and every runner stops with it.
    """

    dt = 1.0

    def __init__(self):
        self.steps = 0

    @property
    def time(self):
        return self.steps * self.dt

    @property
    def done(self):
        return False

    def step(self):
        raise NotImplementedError

    def advance(self, steps=1):
        """Run up to ``steps`` iterations, stopping once the solver is done."""
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            if self.done:
                break
            self.step()
            self.steps += 1


class View:
    """Artists showing one simulation on a Matplotlib figure.

    ``portrait`` asks for a layout that fills the nearly square reel panel
    (1080 x 1060 pixels), typically by stacking panels vertically. ``draw``
    updates the artists from the state and must never advance the simulation.
    ``status`` is the one-line progress shown with the title; the figure title
    belongs to the runner, panel titles to the view.
    """

    figsize = (8.0, 6.0)  # inches of the window and --output PNG; set per view

    def __init__(self, simulation, figure, portrait=False):
        self.simulation = simulation
        self.figure = figure
        self.portrait = portrait

    def draw(self):
        raise NotImplementedError

    def status(self):
        return f"t = {self.simulation.time:.2f}"


@contextmanager
def style(reel=False):
    """Dark theme shared by every simulation; larger text for reels."""
    import matplotlib.pyplot as plt

    styles = ["dark_background", STYLE] + ([REEL_STYLE] if reel else [])
    with plt.style.context(styles):
        yield


# Padding in inches; compress pulls colour bars against fixed-aspect images.
LAYOUT = {"h_pad": 0.08, "w_pad": 0.08, "compress": True}


def freeze_layout(figure):
    """Lay out axes and colour bars once instead of on every frame.

    Figures are created with the constrained engine so colour bars reserve
    their space; running it once and then switching it off keeps panels from
    jittering as tick labels change and skips the solver on every redraw.
    Returns the engine so a resized window can run it again.
    """
    engine = figure.get_layout_engine()
    engine.execute(figure)
    figure.set_layout_engine("none")
    return engine


def frame_schedule(total_steps, n_frames):
    """Split ``total_steps`` iterations into frames of equal increments.

    Every frame advances the same whole number of iterations (only the last
    may advance fewer), so motion plays at a steady speed: alternating 2 and 3
    steps per frame would judder. The increment is the one that brings the
    frame count closest to ``n_frames``; a run shorter than the video gives
    fewer frames, never repeated ones.
    """
    if total_steps < 0 or n_frames < 1:
        raise ValueError("need nonnegative steps and at least one frame")
    if total_steps == 0:
        return [0]
    increment = max(1, round(total_steps / n_frames))
    full, rest = divmod(total_steps, increment)
    return [increment] * full + ([rest] if rest else [])


def find_ffmpeg():
    """Return an ffmpeg executable from PATH or the imageio-ffmpeg wheel."""
    import matplotlib

    executable = shutil.which(matplotlib.rcParams["animation.ffmpeg_path"])
    if executable is None:
        try:
            import imageio_ffmpeg
        except ImportError:
            raise RuntimeError(
                "ffmpeg is needed for --reel: install it with your package "
                "manager or run `pip install imageio-ffmpeg`"
            ) from None
        executable = imageio_ffmpeg.get_ffmpeg_exe()
    return executable


class VideoWriter:
    """Pipe RGBA frames to ffmpeg as an H.264 MP4 that phones and apps accept.

    yuv420p and +faststart are what Shorts, Reels and TikTok expect. A failed
    encode removes the partial file.
    """

    def __init__(self, path, size, fps):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        width, height = size
        command = [
            find_ffmpeg(), "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{width}x{height}",
            "-r", str(fps), "-i", "-",
            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(self.path),
        ]  # fmt: skip
        self.frame_bytes = width * height * 4
        self.frames = 0
        self.process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def write(self, rgba, repeat=1):
        data = memoryview(rgba).cast("B")  # bytes of an (height, width, 4) array
        if data.nbytes != self.frame_bytes:
            raise ValueError(f"frame has {data.nbytes} bytes, not {self.frame_bytes}")
        for _ in range(repeat):
            self.process.stdin.write(data)
        self.frames += repeat

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        try:
            self.process.stdin.close()
        except BrokenPipeError:
            pass
        error = self.process.stderr.read().decode(errors="replace").strip()
        code = self.process.wait()
        self.process.stderr.close()
        if exc_type is not None or code != 0:
            self.path.unlink(missing_ok=True)
        if exc_type is None and code != 0:
            raise RuntimeError(f"ffmpeg failed with exit code {code}: {error}")


@dataclass(frozen=True)
class Animation:
    """Command line and runners shared by every animated simulation.

    One frame is ``steps_per_frame`` solver iterations. ``frames`` is the
    default length of a run; with ``endless`` the window keeps running until
    it is closed, while headless runs and reels still stop after ``frames``.
    """

    title: str
    filename: str  # PNG written to --output DIR
    frames: int
    steps_per_frame: int = 1
    step_label: str = "time steps"  # plural name of a solver iteration, for --help
    subtitle: str = ""  # one line under the title of a reel
    endless: bool = False
    interval_ms: int = 30  # delay between frames in the window

    def parser(self, description):
        """Shared flags: --no-show, --output, --steps and the reel options."""
        parser = create_parser(description)
        parser.epilog = "In the window, space pauses and the right arrow steps a frame."
        per_frame = f"each {self.steps_per_frame} {self.step_label}"
        if (
            self.steps_per_frame == 1
        ):  # "time steps of dt" -> "one time step of dt each"
            head, of, tail = self.step_label.partition(" of ")
            per_frame = f"one {head.removesuffix('s')}{of}{tail} each"
        default = (
            f"run until the window is closed; {self.frames} headless"
            if self.endless
            else str(self.frames)
        )
        parser.add_argument(
            "--steps",
            type=positive_int,
            metavar="N",
            help=f"animation frames, {per_frame} (default: {default})",
        )
        reel = parser.add_argument_group("reel export")
        reel.add_argument(
            "--reel",
            type=Path,
            metavar="FILE",
            help="render a 1080x1920 MP4 for Shorts/Reels instead of a window",
        )
        reel.add_argument(
            "--reel-seconds",
            type=positive_float,
            default=30.0,
            metavar="S",
            help=f"reel length in seconds, ending with a {REEL_HOLD_SECONDS:g} s "
            "hold on the final frame (default: %(default)g)",
        )
        reel.add_argument(
            "--reel-fps",
            type=positive_int,
            default=30,
            metavar="FPS",
            help="reel frame rate (default: %(default)s)",
        )
        return parser

    def run(self, args, simulation, view, **options):
        """Run the simulation as requested by ``args``; return the simulation.

        ``view`` is a View subclass, called as
        ``view(simulation, figure, portrait=..., **options)``.
        """
        frames = self.frames if args.steps is None else args.steps
        if args.reel is not None:
            self.record(simulation, view, options, frames, args)
        elif args.no_show:
            simulation.advance(frames * self.steps_per_frame)
        else:
            limit = None if self.endless and args.steps is None else frames
            self.show(simulation, view, options, limit)
        if args.output is not None:
            self.save_png(simulation, view, options, args.output)
        return simulation

    def headline(self, view):
        return f"{self.title}  ·  {view.status()}"

    def show(self, simulation, view_class, options, frames):
        """Animate in a window. Space pauses, the right arrow steps one frame."""
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        from matplotlib.layout_engine import ConstrainedLayoutEngine

        with style():
            figure = plt.figure()
            figure.set_layout_engine(ConstrainedLayoutEngine(**LAYOUT))
            view = view_class(simulation, figure, portrait=False, **options)
            figure.set_size_inches(view.figsize)
            headline = figure.suptitle("", fontweight="bold")
        if figure.canvas.manager is not None:
            figure.canvas.manager.set_window_title(self.title)

        def redraw():
            with style():
                view.draw()
                headline.set_text(self.headline(view))

        def update(_frame):
            simulation.advance(self.steps_per_frame)
            redraw()
            if simulation.done:
                animation.pause()

        redraw()
        with style():
            engine = freeze_layout(figure)
        animation = FuncAnimation(
            figure,
            update,
            frames=count() if frames is None else frames,
            init_func=redraw,
            interval=self.interval_ms,
            repeat=False,
            cache_frame_data=False,
        )
        paused = [False]

        def on_key(event):
            if event.key == " ":
                paused[0] = not paused[0]
                (animation.pause if paused[0] else animation.resume)()
            elif event.key == "right" and paused[0]:
                update(None)
                figure.canvas.draw_idle()

        figure.canvas.mpl_connect("key_press_event", on_key)
        figure.canvas.mpl_connect("resize_event", lambda event: engine.execute(figure))
        try:
            plt.show()
        finally:
            plt.close(figure)

    def save_png(self, simulation, view_class, options, output):
        """Write the current state with the window layout to output/filename."""
        figure = self.offscreen_figure(View.figsize)
        with style():
            view = view_class(simulation, figure, portrait=False, **options)
            figure.set_size_inches(view.figsize)
            view.draw()
            figure.suptitle(self.headline(view), fontweight="bold")
            freeze_layout(figure)
            save_figure(figure, output, self.filename)

    @staticmethod
    def offscreen_figure(figsize, dpi=100):
        """A figure outside pyplot: nothing to close, never opens a window."""
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
        from matplotlib.layout_engine import ConstrainedLayoutEngine

        figure = Figure(figsize=figsize, dpi=dpi)
        figure.set_layout_engine(ConstrainedLayoutEngine(**LAYOUT))
        FigureCanvasAgg(figure)
        return figure

    def record(self, simulation, view_class, options, frames, args):
        """Render the run as a vertical reel: title, panel, status, progress.

        The view draws on its own panel-sized figure, laid out like the window,
        and each panel image is pasted between the title and status bands.
        """
        import numpy as np
        from matplotlib.patches import Rectangle

        fps = args.reel_fps
        total = round(args.reel_seconds * fps)
        hold = min(round(REEL_HOLD_SECONDS * fps), total // 3)
        moving = max(1, total - hold - 1)  # one more frame shows the start
        schedule = frame_schedule(frames * self.steps_per_frame, moving)
        width, height = REEL_SIZE
        top, panel_height, _ = REEL_BANDS
        writer = VideoWriter(args.reel, REEL_SIZE, fps)  # fails early without ffmpeg

        with style(reel=True):
            panel = self.offscreen_figure((width / REEL_DPI, panel_height / REEL_DPI))
            view = view_class(simulation, panel, portrait=True, **options)
            frame = self.offscreen_figure((width / REEL_DPI, height / REEL_DPI))
            frame.set_layout_engine("none")
            title_y = 1 - 0.62 * top / height
            frame.text(
                0.5, title_y, textwrap.fill(self.title, 24), ha="center",
                va="bottom", fontsize=46, fontweight="bold", linespacing=1.1,
            )  # fmt: skip
            frame.text(
                0.5, title_y - 0.012, textwrap.fill(self.subtitle, 46), ha="center",
                va="top", fontsize=24, color="0.75", linespacing=1.3,
            )  # fmt: skip
            footer_y = 1 - (top + panel_height) / height
            status = frame.text(
                0.5, footer_y - 0.035, "", ha="center", va="center", fontsize=30,
                family="monospace",
            )  # fmt: skip
            bar_y, bar_height = footer_y - 0.075, 0.004
            frame.add_artist(
                Rectangle((0.1, bar_y), 0.8, bar_height, color="0.25",
                          transform=frame.transFigure)
            )  # fmt: skip
            bar = Rectangle(
                (0.1, bar_y), 0, bar_height, color="#4cc9f0",
                transform=frame.transFigure,
            )  # fmt: skip
            frame.add_artist(bar)

            def render(progress):
                view.draw()
                status.set_text(view.status())
                bar.set_width(0.8 * progress)
                panel.canvas.draw()
                frame.canvas.draw()
                image = np.asarray(frame.canvas.buffer_rgba()).copy()
                image[top : top + panel_height] = panel.canvas.buffer_rgba()
                return image

            print(f"Rendering {len(schedule)} frames to {args.reel}", flush=True)
            started = time.monotonic()
            report_every = max(1, len(schedule) // 10)
            with writer:
                view.draw()
                freeze_layout(panel)
                writer.write(render(0.0))
                for index, increment in enumerate(schedule, start=1):
                    if simulation.done:
                        break
                    simulation.advance(increment)
                    progress = 1.0 if simulation.done else index / len(schedule)
                    writer.write(render(progress))
                    if index % report_every == 0 and index < len(schedule):
                        elapsed = time.monotonic() - started
                        remaining = elapsed * (len(schedule) / index - 1)
                        print(
                            f"  {index}/{len(schedule)} frames, "
                            f"{elapsed:.0f} s elapsed, about {remaining:.0f} s left",
                            flush=True,
                        )
                writer.write(render(1.0), repeat=hold)
        print(
            f"Wrote {args.reel}: {writer.frames / fps:.1f} s at {fps} fps, "
            f"{width}x{height}",
            flush=True,
        )
