"""Shared simulation runner: frame schedules, CLI, headless runs and reels."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import _animation  # noqa: E402
from _animation import Animation, Simulation, View, frame_schedule  # noqa: E402

from tools import make_reels  # noqa: E402


class Counter(Simulation):
    """Toy solver: one unit per step, optionally finishing after ``limit``."""

    dt = 0.5

    def __init__(self, limit=None):
        super().__init__()
        self.value = 0
        self.limit = limit

    def step(self):
        self.value += 1

    @property
    def done(self):
        return self.limit is not None and self.steps >= self.limit


class CounterView(View):
    figsize = (3.0, 2.0)

    def __init__(self, simulation, figure, portrait=False, color="C0"):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        (self.line,) = ax.plot([0, 1], [0, 0], color=color)
        ax.set_ylim(0, 100)
        self.color = color
        self.draws = 0

    def draw(self):
        self.line.set_ydata([0, self.simulation.value])
        self.draws += 1


ANIMATION = Animation(
    title="Counter", filename="counter.png", frames=4, steps_per_frame=3
)


class FakeWriter:
    """Records frames instead of starting ffmpeg."""

    instances = []

    def __init__(self, path, size, fps):
        self.path, self.size, self.fps, self.frames = path, size, fps, 0
        self.shapes = []
        FakeWriter.instances.append(self)

    def write(self, rgba, repeat=1):
        self.shapes.append(memoryview(rgba).shape)
        self.frames += repeat

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def run(argv, simulation=None, **options):
    simulation = Counter() if simulation is None else simulation
    args = ANIMATION.parser("Toy.").parse_args(argv)
    with redirect_stdout(io.StringIO()):
        ANIMATION.run(args, simulation, CounterView, **options)
    return simulation


class ScheduleTests(unittest.TestCase):
    def test_frames_advance_equal_increments(self):
        cases = ((10, 3), (900, 870), (12345, 869), (5, 5), (2400, 869), (920, 839))
        for total, frames in cases:
            with self.subTest(total=total, frames=frames):
                schedule = frame_schedule(total, frames)
                self.assertEqual(sum(schedule), total)
                self.assertEqual(set(schedule[:-1]) | {schedule[0]}, {schedule[0]})
                self.assertLessEqual(schedule[-1], schedule[0])
                # the nearest whole increment keeps the video close to its length
                self.assertLess(abs(len(schedule) - frames), frames / 2 + 1)
        self.assertEqual(frame_schedule(10, 3), [3, 3, 3, 1])
        self.assertEqual(frame_schedule(2400, 869), [3] * 800)
        self.assertEqual(frame_schedule(920, 839), [1] * 920)
        self.assertEqual(len(frame_schedule(30000, 839)), 834)

    def test_short_runs_give_fewer_frames_instead_of_repeats(self):
        self.assertEqual(frame_schedule(4, 100), [1, 1, 1, 1])
        self.assertEqual(frame_schedule(0, 10), [0])

    def test_invalid_arguments(self):
        for total, frames in ((-1, 3), (3, 0)):
            with (
                self.subTest(total=total, frames=frames),
                self.assertRaises(ValueError),
            ):
                frame_schedule(total, frames)


class SimulationBaseTests(unittest.TestCase):
    def test_advance_counts_steps_and_time(self):
        simulation = Counter()
        simulation.advance(4)
        simulation.advance()
        self.assertEqual((simulation.steps, simulation.value), (5, 5))
        self.assertEqual(simulation.time, 2.5)

    def test_advance_rejects_negative_and_stops_when_done(self):
        with self.assertRaises(ValueError):
            Counter().advance(-1)
        simulation = Counter(limit=3)
        simulation.advance(10)
        self.assertEqual(simulation.steps, 3)
        self.assertTrue(simulation.done)


class RunnerTests(unittest.TestCase):
    def test_parser_shares_flags_and_validates_them(self):
        parser = ANIMATION.parser("Toy example.\nMore text.")
        args = parser.parse_args([])
        self.assertIsNone(args.steps)
        self.assertIsNone(args.reel)
        self.assertEqual((args.reel_seconds, args.reel_fps), (30.0, 30))
        self.assertIn("each 3 time steps", parser.format_help())
        for flags in (["--steps", "0"], ["--reel-seconds", "-2"], ["--reel-fps", "x"]):
            with (
                self.subTest(flags=flags),
                redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                parser.parse_args(flags)

    def test_headless_run_advances_frames_and_saves_png(self):
        with tempfile.TemporaryDirectory() as directory:
            simulation = run(["--no-show", "--steps", "5", "--output", directory])
            self.assertTrue((Path(directory) / "counter.png").is_file())
        self.assertEqual(simulation.steps, 15)
        default = run(["--no-show"])
        self.assertEqual(default.steps, ANIMATION.frames * ANIMATION.steps_per_frame)

    def test_headless_run_stops_when_done(self):
        simulation = run(["--no-show", "--steps", "50"], Counter(limit=7))
        self.assertEqual(simulation.steps, 7)

    def test_window_initialization_does_not_advance(self):
        def animate(figure, update, frames, init_func, **kwargs):
            init_func()
            init_func()  # Matplotlib may initialize again during resize.
            for frame in range(frames):
                update(frame)
            return object()

        with (
            patch("matplotlib.animation.FuncAnimation", side_effect=animate),
            patch("matplotlib.pyplot.show"),
        ):
            simulation = run(["--steps", "2"])
        self.assertEqual(simulation.steps, 2 * ANIMATION.steps_per_frame)

    def test_reel_frames_follow_schedule_and_hold(self):
        FakeWriter.instances.clear()
        with patch.object(_animation, "VideoWriter", FakeWriter):
            simulation = run(
                ["--reel", "x.mp4", "--steps", "10", "--reel-seconds", "2"]
                + ["--reel-fps", "10"],
                color="red",
            )
        (writer,) = FakeWriter.instances
        hold = min(round(_animation.REEL_HOLD_SECONDS * 10), 20 // 3)
        moving = frame_schedule(10 * 3, 20 - hold - 1)  # 30 steps for 13 frames
        self.assertEqual(moving, [2] * 15)
        self.assertEqual(writer.frames, 1 + len(moving) + hold)
        self.assertEqual(simulation.steps, 10 * 3)
        self.assertEqual(len(writer.shapes), 1 + len(moving) + 1)
        self.assertEqual(writer.shapes[0], (1920, 1080, 4))

    def test_reel_stops_early_when_simulation_finishes(self):
        FakeWriter.instances.clear()
        with patch.object(_animation, "VideoWriter", FakeWriter):
            simulation = run(["--reel", "x.mp4", "--steps", "40"], Counter(limit=5))
        self.assertEqual(simulation.steps, 5)
        self.assertLess(FakeWriter.instances[0].frames, 30 * 30)

    def test_reel_and_png_together(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(_animation, "VideoWriter", FakeWriter),
        ):
            run(["--reel", "x.mp4", "--reel-seconds", "1", "--output", directory])
            self.assertTrue((Path(directory) / "counter.png").is_file())


class VideoWriterTests(unittest.TestCase):
    def setUp(self):
        try:
            _animation.find_ffmpeg()
        except RuntimeError:
            self.skipTest("ffmpeg is not available")

    def test_encodes_mp4(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "reel.mp4"
            simulation = run(
                ["--reel", str(path), "--reel-seconds", "1", "--reel-fps", "10"]
            )
            self.assertTrue(make_reels.is_mp4(path))
        self.assertEqual(simulation.steps, 12)

    def test_wrong_frame_size_removes_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.mp4"
            with self.assertRaises(ValueError):
                with _animation.VideoWriter(path, (16, 16), 10) as writer:
                    writer.write(bytes(16 * 16 * 4))
                    writer.write(bytes(10))
            self.assertFalse(path.exists())


class MakeReelsTests(unittest.TestCase):
    def test_selects_simulations_only(self):
        names = [script.parent.name for script in make_reels.simulations([])]
        self.assertEqual(len(names), 25)
        self.assertEqual(
            [s.parent.name for s in make_reels.simulations(["cavity"])],
            ["lid_driven_cavity"],
        )

    def test_arguments_after_double_dash_are_passed_through(self):
        args = make_reels.parse_args(["cavity", "--seconds", "5", "--", "--x", "1"])
        self.assertEqual(
            (args.filters, args.seconds, args.extra), (["cavity"], 5.0, ["--x", "1"])
        )

    def test_failed_render_is_reported(self):
        script = make_reels.simulations(["cavity"])[0]
        args = make_reels.parse_args([])
        with patch.object(make_reels, "run", return_value=(2, "bad flag", False)):
            result = make_reels.render(script, Path("/unused"), args)
        self.assertFalse(result.ok)
        self.assertIn("bad flag", result.output)


if __name__ == "__main__":
    unittest.main()
