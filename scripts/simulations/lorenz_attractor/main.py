"""Lorenz attractor: trajectories that start 1e-5 apart fan out over the butterfly.

The Lorenz (1963) equations are a three-mode truncation of Rayleigh-Benard
convection. A short line of initial states, 1e-5 long, is placed on the
attractor and every state is advanced with the classical fourth-order
Runge-Kutta scheme. The states travel together as one comet until their
separation, which grows about like exp(0.9 t), reaches the size of the
attractor; then the line is stretched and folded over both wings. A 3D view,
whose camera swings slowly back and forth, shows the recent trail of every
state, and a second panel the spread of the cloud on a log scale next to the
Lyapunov growth exp(0.906 t).
"""

import sys
from collections import deque
from pathlib import Path

import numpy as np
from matplotlib import colormaps
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Model parameters (Lorenz 1963); x, y, z and t are dimensionless
SIGMA = 10.0  # Prandtl number nu / kappa
RHO = 28.0  # Rayleigh number over its critical value, Ra / Ra_c
BETA = 8.0 / 3.0  # geometric factor 4 / (1 + a^2) of rolls with a^2 = 1/2
LYAPUNOV_EXPONENT = 0.906  # largest Lyapunov exponent for these values [1 / time]

# Ensemble and time stepping
TIME_STEP = 0.01  # RK4 step [time]
N_TRAJECTORIES = 60  # states on the initial line
INITIAL_LENGTH = 1e-5  # length of the line of initial states
START = (1.0, 1.0, 1.0)  # integrated for TRANSIENT to land on the attractor
TRANSIENT = 30.0  # [time]
SEED = 0  # random direction of the initial line
TRAIL_STEPS = 120  # time steps kept in every trail (1.2 time units)
GHOST_TIME = 60.0  # length of the dim reference orbit drawn behind [time]
STEPS_PER_FRAME = 5  # RK4 steps per animation frame
N_FRAMES = 500  # default frames -> t = 25

# Camera and colours
ELEVATION = 12.0  # camera elevation [degrees]
AZIMUTH = -45.0  # camera azimuth facing both wings [degrees]
SWING = 35.0  # amplitude of the camera's swing about AZIMUTH [degrees]
SWING_PERIOD = 12.5  # period of the swing [time]
ZOOM, ZOOM_PORTRAIT = 1.3, 1.6  # magnification of the 3D box in window and reel
TRAIL_CMAP = "turbo"  # colour by position along the initial line
SPREAD_LIMITS = (1e-6, 1e2)  # fixed range of the spread axis


def lorenz_rhs(state, sigma=SIGMA, rho=RHO, beta=BETA):
    """Right-hand side f(x, y, z) for states stored along the last axis."""
    x, y, z = state[..., 0], state[..., 1], state[..., 2]
    return np.stack((sigma * (y - x), x * (rho - z) - y, x * y - beta * z), axis=-1)


def rk4_step(state, dt=TIME_STEP, rhs=lorenz_rhs):
    """One classical fourth-order Runge-Kutta step of dX/dt = rhs(X)."""
    k1 = rhs(state)
    k2 = rhs(state + 0.5 * dt * k1)
    k3 = rhs(state + 0.5 * dt * k2)
    k4 = rhs(state + dt * k3)
    return state + dt / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(state, duration, dt=TIME_STEP):
    """Advance ``state`` by ``duration`` with RK4 steps of about ``dt``."""
    n_steps = max(1, round(duration / dt))
    h = duration / n_steps
    state = np.asarray(state, dtype=float)
    for _ in range(n_steps):
        state = rk4_step(state, h)
    return state


def fixed_points(sigma=SIGMA, rho=RHO, beta=BETA):
    """The origin (conduction) and, for rho > 1, the two steady rolls C+ and C-."""
    points = [np.zeros(3)]
    if rho > 1:
        a = np.sqrt(beta * (rho - 1.0))
        points += [np.array([a, a, rho - 1.0]), np.array([-a, -a, rho - 1.0])]
    return points


def divergence(sigma=SIGMA, beta=BETA):
    """Divergence of the Lorenz vector field: the same constant at every point."""
    return -(sigma + 1.0 + beta)


def spread(points):
    """RMS distance of the points from their centroid."""
    centred = points - points.mean(axis=0)
    return float(np.sqrt(np.mean(np.sum(centred**2, axis=-1))))


def initial_line(n, length, rng, start=START, transient=TRANSIENT):
    """n states evenly spaced on a segment of ``length`` centred on the attractor."""
    centre = integrate(start, transient)
    direction = rng.normal(size=3)
    direction /= np.linalg.norm(direction)
    offsets = np.linspace(-0.5, 0.5, n) * length
    return centre + offsets[:, None] * direction


class LorenzSimulation(Simulation):
    """An ensemble of Lorenz states with their recent trails and spread history.

    ``trail`` holds the last ``trail_steps + 1`` states of every trajectory;
    ``times`` and ``spreads`` record the spread of the cloud after every step.
    ``ghost`` is one long orbit of the attractor, a fixed backdrop for the view.
    """

    dt = TIME_STEP

    def __init__(
        self,
        n_trajectories=N_TRAJECTORIES,
        initial_length=INITIAL_LENGTH,
        trail_steps=TRAIL_STEPS,
        ghost_time=GHOST_TIME,
        seed=SEED,
    ):
        super().__init__()
        if n_trajectories < 2:
            raise ValueError("at least two trajectories are needed for a spread")
        self.points = initial_line(
            n_trajectories, initial_length, np.random.default_rng(seed)
        )
        self.trail = deque([self.points.copy()], maxlen=trail_steps + 1)
        self.times = [0.0]
        self.spreads = [spread(self.points)]
        ghost = [self.points[n_trajectories // 2]]
        for _ in range(round(ghost_time / TIME_STEP)):
            ghost.append(rk4_step(ghost[-1]))
        self.ghost = np.array(ghost)

    def step(self):
        self.points = rk4_step(self.points)
        self.trail.append(self.points.copy())
        self.times.append((self.steps + 1) * self.dt)
        self.spreads.append(spread(self.points))


class LorenzView(View):
    """3D trails beside (window) or above (reel) the spread history.

    Every trajectory has its own colour, ordered along the initial line, so the
    stretched line reads as a rainbow. Each trail is drawn twice, wide and
    faint under narrow and bright, and fades out with age. ``duration`` sets
    the time axis of the spread panel, which widens if the run goes on longer.
    """

    figsize = (13.0, 6.5)

    def __init__(
        self,
        simulation,
        figure,
        portrait=False,
        duration=N_FRAMES * STEPS_PER_FRAME * TIME_STEP,
    ):
        super().__init__(simulation, figure, portrait)
        if portrait:
            view_cell, spread_cell = figure.add_gridspec(2, 1, height_ratios=(3.2, 1))
        else:
            view_cell, spread_cell = figure.add_gridspec(1, 2, width_ratios=(1.2, 1))
        self.ax = ax = figure.add_subplot(view_cell, projection="3d")
        ax.set_axis_off()
        ax.set(xlim=(-20, 20), ylim=(-25, 25), zlim=(2, 48))
        ax.set_box_aspect((40, 50, 46), zoom=ZOOM_PORTRAIT if portrait else ZOOM)
        ghost = simulation.ghost
        artists = ax.plot(*ghost.T, color="0.45", linewidth=0.4, alpha=0.35)
        for point in fixed_points()[1:]:
            artists += ax.plot(*point[:, None], "+", color="0.8", markersize=8)

        n = len(simulation.points)
        self.colors = colormaps[TRAIL_CMAP](np.linspace(0.05, 0.95, n))
        self.glow = Line3DCollection([], linewidths=6.0 if portrait else 4.0)
        self.core = Line3DCollection([], linewidths=1.6 if portrait else 1.1)
        ax.add_collection(self.glow)
        ax.add_collection(self.core)
        (self.heads,) = ax.plot(
            [], [], [], "o", color="white", markersize=3.5 if portrait else 2.5,
            markeredgewidth=0,
        )  # fmt: skip
        # The attractor may overhang the 3D box into the empty margins beside
        # it; the layout still sizes the box alone.
        for artist in [*artists, self.glow, self.core, self.heads]:
            artist.set_clip_on(False)
            artist.set_in_layout(False)

        ax = self.spread_ax = figure.add_subplot(spread_cell)
        ax.set_yscale("log")
        ax.set(xlim=(0, duration), ylim=SPREAD_LIMITS, xlabel="time t")
        ax.set_ylabel("spread" if portrait else "spread of the cloud")
        ax.grid(color="0.25", linewidth=0.6)
        times = np.linspace(0, duration, 200)
        reference = simulation.spreads[0] * np.exp(LYAPUNOV_EXPONENT * times)
        ax.plot(
            times, reference, "--", color="0.6", linewidth=1.2,
            label=rf"$\propto e^{{{LYAPUNOV_EXPONENT:g}\,t}}$",
        )  # fmt: skip
        (self.spread_line,) = ax.plot([], [], color="#4cc9f0")
        (self.spread_head,) = ax.plot([], [], "o", color="white", markersize=4)
        ax.legend(loc="lower right")
        self.duration = duration

    def trail_segments(self):
        """Segments (n_trajectories * (length - 1), 2, 3) and their RGBA colours."""
        trail = np.asarray(self.simulation.trail)  # (length, n, 3)
        length, n, _ = trail.shape
        if length < 2:
            return np.empty((0, 2, 3)), np.empty((0, 4))
        segments = np.stack((trail[:-1], trail[1:]), axis=2)  # (length - 1, n, 2, 3)
        segments = segments.transpose(1, 0, 2, 3).reshape(-1, 2, 3)
        maxlen = self.simulation.trail.maxlen
        age = np.arange(maxlen - length + 1, maxlen) / (maxlen - 1)  # 1 = newest
        colors = np.repeat(self.colors[:, None, :], length - 1, axis=1)
        colors[..., 3] = age[None, :] ** 1.5
        return segments, colors.reshape(-1, 4)

    def draw(self):
        simulation = self.simulation
        segments, colors = self.trail_segments()
        self.core.set_segments(segments)
        self.core.set_color(colors)
        glow = colors.copy()
        glow[:, 3] *= 0.12
        self.glow.set_segments(segments)
        self.glow.set_color(glow)
        self.heads.set_data_3d(*simulation.points.T)
        swing = np.sin(2 * np.pi * simulation.time / SWING_PERIOD)
        self.ax.view_init(ELEVATION, AZIMUTH + SWING * swing)

        self.spread_line.set_data(simulation.times, simulation.spreads)
        self.spread_head.set_data(simulation.times[-1:], simulation.spreads[-1:])
        self.spread_ax.set_xlim(0, max(self.duration, simulation.time))

    def status(self):
        simulation = self.simulation
        return f"t = {simulation.time:.1f}   spread {simulation.spreads[-1]:.1e}"


ANIMATION = Animation(
    title="Lorenz Attractor",
    subtitle=f"{N_TRAJECTORIES} starts 1e-5 apart: the butterfly effect",
    filename="lorenz_attractor.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"RK4 steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    frames = ANIMATION.frames if args.steps is None else args.steps
    simulation = ANIMATION.run(
        args,
        LorenzSimulation(),
        LorenzView,
        duration=frames * STEPS_PER_FRAME * TIME_STEP,
    )
    print(
        f"t = {simulation.time:.2f} after {simulation.steps} RK4 steps: spread "
        f"{simulation.spreads[0]:.2e} -> {simulation.spreads[-1]:.2e}"
    )


if __name__ == "__main__":
    main()
