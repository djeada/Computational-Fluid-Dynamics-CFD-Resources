"""Chaotic mixing of dye in the time-periodic double gyre.

The double gyre of Shadden, Lekien & Marsden (2005) is a pair of
counter-rotating cells on [0, 2] x [0, 1] whose dividing line sways from side
to side. About 720 000 passive tracers, cyan from the left half and pink from
the right half, are advected with the fourth-order Runge-Kutta method and
drawn as an image of the fraction of right-half fluid in each pixel. The lower
panel shows the backward-time finite-time Lyapunov exponent (FTLE): its ridges
are the attracting Lagrangian coherent structures along which the dye is
stretched and folded into filaments.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from numba import njit, prange

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Flow parameters of Shadden, Lekien & Marsden (2005), all nondimensional
AMPLITUDE = 0.1  # A, stream function amplitude [length^2 / time]
EPSILON = 0.25  # epsilon, amplitude of the sideways sway of the gyres [-]
PERIOD = 10.0  # forcing period 2 pi / omega [time]
OMEGA = 2 * np.pi / PERIOD  # omega, forcing angular frequency [1 / time]
WIDTH, HEIGHT = 2.0, 1.0  # domain [0, 2] x [0, 1] [length]

# Tracers and time stepping
TRACER_GRID = (1200, 600)  # jittered lattice of tracers along x and y (720 000)
SEED = 0  # random jitter of the tracer lattice
TIME_STEP = 0.025  # RK4 step dt [time]: 400 steps per forcing period
STEPS_PER_FRAME = 10  # RK4 steps per animation frame (0.25 time units)
N_FRAMES = 240  # default frames: t = 60, six forcing periods

# Diagnostics and display
IMAGE_SHAPE = (240, 480)  # rows, columns of the dye image (about 6 tracers each)
MIXING_CELLS = (20, 40)  # coarse cells of 0.05 x 0.05 for the mixing measure
MIXED_RANGE = (0.25, 0.75)  # right-half fraction of a well-mixed cell
FTLE_SHAPE = (160, 320)  # rows, columns of the FTLE grid
FTLE_TIME = 15.0  # integration time of the backward FTLE [time], 1.5 periods
FTLE_STEP = 0.1  # RK4 step of the FTLE flow map [time]
FTLE_PHASES = 100  # FTLE fields per forcing period, reused every period
FTLE_MAX = 0.4  # upper end of the FTLE colour scale [1 / time]
DYE_CMAP = LinearSegmentedColormap.from_list(
    "dye", ["#00c8ff", "#7a3cff", "#ff2a6d"]
)  # cyan (left-half fluid), violet (mixed), pink (right-half fluid)


@njit(cache=False)
def velocity(x, y, t):
    """Double-gyre velocity (u, v) = (-dpsi/dy, dpsi/dx) at (x, y) and time t.

    psi = A sin(pi f(x, t)) sin(pi y) with f = a x^2 + b x, a = eps sin(omega t)
    and b = 1 - 2a. Works on scalars and on arrays.
    """
    a = EPSILON * np.sin(OMEGA * t)
    b = 1.0 - 2.0 * a
    f = (a * x + b) * x
    dfdx = 2.0 * a * x + b
    u = -np.pi * AMPLITUDE * np.sin(np.pi * f) * np.cos(np.pi * y)
    v = np.pi * AMPLITUDE * np.cos(np.pi * f) * np.sin(np.pi * y) * dfdx
    return u, v


@njit(cache=False, parallel=True)
def advect(x, y, t, dt, n_steps):
    """Move the points (x, y) in place by n_steps RK4 steps of dt from time t.

    A negative dt integrates backward in time.
    """
    for i in prange(x.size):
        px, py = x[i], y[i]
        for k in range(n_steps):
            time = t + k * dt
            k1u, k1v = velocity(px, py, time)
            k2u, k2v = velocity(
                px + 0.5 * dt * k1u, py + 0.5 * dt * k1v, time + 0.5 * dt
            )
            k3u, k3v = velocity(
                px + 0.5 * dt * k2u, py + 0.5 * dt * k2v, time + 0.5 * dt
            )
            k4u, k4v = velocity(px + dt * k3u, py + dt * k3v, time + dt)
            px += dt / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u)
            py += dt / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
        x[i], y[i] = px, py


@njit(cache=False)
def count_tracers(x, y, from_right, n_rows, n_cols):
    """Tracers from the left (index 0) and right (1) half in each grid cell."""
    counts = np.zeros((2, n_rows, n_cols))
    for i in range(x.size):
        column = min(max(int(x[i] / WIDTH * n_cols), 0), n_cols - 1)
        row = min(max(int(y[i] / HEIGHT * n_rows), 0), n_rows - 1)
        counts[from_right[i], row, column] += 1.0
    return counts


def right_fraction(counts):
    """Fraction of right-half fluid per cell; 0.5 where a cell is empty."""
    total = counts.sum(axis=0)
    return np.where(total > 0, counts[1] / np.maximum(total, 1.0), 0.5)


def well_mixed_fraction(counts, mixed_range=MIXED_RANGE):
    """Fraction of cells whose right-half fluid fraction lies in mixed_range."""
    fraction = right_fraction(counts)
    low, high = mixed_range
    return float(np.mean((fraction >= low) & (fraction <= high)))


def seed_tracers(n_x, n_y, rng):
    """One tracer at a random point of each cell of an n_x by n_y lattice."""
    columns, rows = np.meshgrid(np.arange(n_x), np.arange(n_y))
    x = (columns + rng.random(columns.shape)) * WIDTH / n_x
    y = (rows + rng.random(rows.shape)) * HEIGHT / n_y
    return x.ravel(), y.ravel()


def cell_centres(shape):
    """x and y coordinates of the centres of a (rows, columns) grid."""
    n_rows, n_cols = shape
    x = (np.arange(n_cols) + 0.5) * WIDTH / n_cols
    y = (np.arange(n_rows) + 0.5) * HEIGHT / n_rows
    return np.meshgrid(x, y)


def flow_map(x, y, t0, duration, max_step=FTLE_STEP):
    """Positions at t0 + duration of the points that are at (x, y) at t0.

    The interval is split into equal RK4 steps no longer than max_step; a
    negative duration integrates backward in time.
    """
    n_steps = max(1, int(np.ceil(abs(duration) / max_step - 1e-9)))
    shape = np.shape(x)
    x_end = np.array(x, dtype=float).ravel()
    y_end = np.array(y, dtype=float).ravel()
    advect(x_end, y_end, float(t0), duration / n_steps, n_steps)
    return x_end.reshape(shape), y_end.reshape(shape)


def ftle_from_flow_map(x_end, y_end, spacing, duration):
    """Largest finite-time Lyapunov exponent of a flow map sampled on a grid.

    The deformation gradient is taken with central differences (one-sided at
    the edges); sigma = ln(lambda_max of the Cauchy-Green tensor) / (2 |T|).
    """
    dx, dy = spacing
    j11 = np.gradient(x_end, dx, axis=1)
    j12 = np.gradient(x_end, dy, axis=0)
    j21 = np.gradient(y_end, dx, axis=1)
    j22 = np.gradient(y_end, dy, axis=0)
    c11 = j11**2 + j21**2
    c12 = j11 * j12 + j21 * j22
    c22 = j12**2 + j22**2
    half_trace = 0.5 * (c11 + c22)
    determinant = c11 * c22 - c12**2
    lambda_max = half_trace + np.sqrt(np.maximum(half_trace**2 - determinant, 0.0))
    return np.log(np.maximum(lambda_max, 1.0)) / (2.0 * abs(duration))


def ftle_field(t0, duration=-FTLE_TIME, shape=FTLE_SHAPE, max_step=FTLE_STEP):
    """FTLE at time t0 over [t0, t0 + duration] on the cell centres of shape.

    The default negative duration gives the backward-time FTLE, whose ridges
    are attracting Lagrangian coherent structures.
    """
    x, y = cell_centres(shape)
    x_end, y_end = flow_map(x, y, t0, duration, max_step)
    spacing = (WIDTH / shape[1], HEIGHT / shape[0])
    return ftle_from_flow_map(x_end, y_end, spacing, duration)


class DoubleGyreSimulation(Simulation):
    """Tracer positions advected through the double gyre.

    ``from_right`` labels each tracer by the half it started in. The FTLE
    depends on the time only through the forcing phase, so ``ftle()`` keeps
    one field per phase and every later period reuses it.
    """

    dt = TIME_STEP

    def __init__(
        self,
        tracers=TRACER_GRID,
        image_shape=IMAGE_SHAPE,
        ftle_shape=FTLE_SHAPE,
        seed=SEED,
    ):
        super().__init__()
        self.x, self.y = seed_tracers(*tracers, np.random.default_rng(seed))
        self.from_right = (self.x > 0.5 * WIDTH).astype(np.int64)
        self.image_shape = image_shape
        self.ftle_shape = ftle_shape
        self.ftle_fields = {}  # forcing phase index -> backward FTLE field

    def step(self):
        advect(self.x, self.y, self.time, self.dt, 1)

    def counts(self, shape):
        return count_tracers(self.x, self.y, self.from_right, *shape)

    def dye(self):
        """Fraction of right-half fluid in each pixel of the dye image."""
        return right_fraction(self.counts(self.image_shape))

    def mixed_fraction(self):
        """Fraction of the 0.05 x 0.05 cells that are well mixed."""
        return well_mixed_fraction(self.counts(MIXING_CELLS))

    def ftle_phase(self):
        """Index of the stored forcing phase nearest to the current time."""
        return round(self.time % PERIOD / PERIOD * FTLE_PHASES) % FTLE_PHASES

    def ftle(self):
        """Backward FTLE at the forcing phase nearest to the current time."""
        phase = self.ftle_phase()
        if phase not in self.ftle_fields:
            t0 = phase * PERIOD / FTLE_PHASES
            self.ftle_fields[phase] = ftle_field(t0, shape=self.ftle_shape)
        return self.ftle_fields[phase]


class DoubleGyreView(View):
    """Dye above the backward FTLE, both on the 2:1 domain.

    The two 2:1 maps stacked fill the nearly square reel panel, so the window
    and the reel use the same layout. The dye map goes from cyan (left-half
    fluid) through violet (mixed) to pink (right-half fluid).
    """

    figsize = (8.4, 8.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        top, bottom = figure.subplots(2, 1, sharex=True)
        extent = (0.0, WIDTH, 0.0, HEIGHT)
        self.dye = top.imshow(
            simulation.dye(), cmap=DYE_CMAP, vmin=0.0, vmax=1.0, extent=extent,
            interpolation="bilinear", interpolation_stage="data",
        )  # fmt: skip
        figure.colorbar(
            self.dye, ax=top, ticks=[0.0, 0.5, 1.0], label="right-half fluid"
        )
        top.set(title="Dye from the left and right halves", ylabel="y")
        self.ftle = bottom.imshow(
            simulation.ftle(), cmap="inferno", vmin=0.0, vmax=FTLE_MAX,
            extent=extent, interpolation="bilinear", interpolation_stage="data",
        )  # fmt: skip
        figure.colorbar(
            self.ftle, ax=bottom, ticks=np.linspace(0.0, FTLE_MAX, 5),
            label=r"FTLE $\sigma$",
        )  # fmt: skip
        bottom.set(title="Backward FTLE: attracting LCS", xlabel="x", ylabel="y")
        bottom.set_xticks(np.linspace(0.0, WIDTH, 5))
        for ax in (top, bottom):
            ax.set_yticks([0.0, 0.5, 1.0])

    def draw(self):
        self.dye.set_data(self.simulation.dye())
        self.ftle.set_data(self.simulation.ftle())

    def status(self):
        periods = self.simulation.time / PERIOD
        mixed = 100 * self.simulation.mixed_fraction()
        return f"t = {periods:.2f} periods   well mixed {mixed:.0f} %"


ANIMATION = Animation(
    title="Double Gyre Chaotic Mixing",
    subtitle="Dye folds along Lagrangian coherent structures",
    filename="double_gyre_chaotic_mixing.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"RK4 steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, DoubleGyreSimulation(), DoubleGyreView)
    rows, columns = MIXING_CELLS
    print(
        f"t = {simulation.time:g} ({simulation.time / PERIOD:g} forcing periods), "
        f"{simulation.x.size} tracers: {simulation.mixed_fraction():.1%} of the "
        f"{columns} x {rows} cells well mixed"
    )


if __name__ == "__main__":
    main()
