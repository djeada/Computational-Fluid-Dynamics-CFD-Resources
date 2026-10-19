"""Sound of a source that accelerates through the sound barrier: the Mach cone.

A small oscillating source (a Gaussian forcing term with a sinusoidal time
signal) moves upward through a still 2D acoustic medium, accelerating from
rest to twice the speed of sound. The pressure obeys the 2D wave equation,
solved with second-order central differences in space and time (leapfrog);
an absorbing sponge layer surrounds the domain. The waves bunch up ahead of
the source while it is subsonic (Doppler effect), pile up at Mach 1, and
form a Mach cone of half-angle arcsin(1/M) once the source is supersonic.
"""

import math
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Units: lengths in wavelengths of the tone at rest, times in its periods,
# so the speed of sound is 1 wavelength per period.
SOUND_SPEED = 1.0  # c [wavelengths / period]
FREQUENCY = 1.0  # source frequency [1 / period]
WIDTH = 15.0  # visible domain [wavelengths] ...
HEIGHT = 18.0  # ... the sponge layer lies outside it
SPONGE_WIDTH = 3.5  # absorbing layer on every side [wavelengths]
SPONGE_DAMPING = 8.0  # damping rate at the outer edge of the sponge [1 / period]
SOURCE_RADIUS = 0.15  # standard deviation of the Gaussian source [wavelengths]
SOURCE_AMPLITUDE = 100.0  # forcing amplitude [pressure / period^2]
RAMP_TIME = 1.0  # the amplitude rises smoothly over about this time [periods]
SOURCE_START = 3.5  # height of the source at t = 0 [wavelengths]
MACH_MAX = 2.0  # final Mach number of the source
ACCELERATION_TIME = 7.2  # Mach number rises linearly from 0 to MACH_MAX [periods]
END_TIME = 10.4  # time of the last frame [periods]

# Numerical parameters
CELLS_PER_WAVELENGTH = 25  # grid spacing dx = dy = 0.04 wavelengths
COURANT = 0.3125  # c dt / dx; leapfrog in 2D is stable up to 1/sqrt(2)
STEPS_PER_FRAME = 4  # time steps per animation frame
TIME_STEP = COURANT / (CELLS_PER_WAVELENGTH * SOUND_SPEED)  # dt = 1/80 period
N_FRAMES = round(END_TIME / (TIME_STEP * STEPS_PER_FRAME))  # 208 frames reach t = 10.4

# Display
PRESSURE_LIMIT = 1.0  # colour scale -1 .. 1; the pile-up and the cone saturate it
CONE_LENGTH = 9.0  # length of the drawn Mach lines [wavelengths]
SOUND_BARRIER_BAND = 0.06  # |M - 1| below which the label reads "sound barrier"
# Diverging map with a black centre: blue rarefaction, orange compression.
PRESSURE_CMAP = LinearSegmentedColormap.from_list(
    "sound",
    ["#dff6ff", "#3ab7ff", "#0b3c8c", "#000000", "#9c2a00", "#ff8c1a", "#fff2b0"],
)


def mach_number(t, mach_max=MACH_MAX, acceleration_time=ACCELERATION_TIME):
    """Mach number of the source: linear rise to mach_max, then constant."""
    if acceleration_time <= 0.0:
        return mach_max
    return mach_max * min(t / acceleration_time, 1.0)


def travelled(t, mach_max=MACH_MAX, acceleration_time=ACCELERATION_TIME):
    """Distance covered by the source after time t (the integral of M c)."""
    speed = mach_max * SOUND_SPEED
    if acceleration_time <= 0.0:
        return speed * t
    ramp = min(t, acceleration_time)
    return speed * (0.5 * ramp**2 / acceleration_time + max(t - acceleration_time, 0.0))


def sponge_profile(n, cells, damping):
    """Damping rate along one axis: zero inside, rising quadratically to
    ``damping`` over the ``cells`` outermost nodes on each side."""
    sigma = np.zeros(n)
    if cells > 0:
        depth = np.arange(cells, 0, -1) / cells  # 1 at the edge, 1/cells inside
        sigma[:cells] = damping * depth**2
        sigma[n - cells :] = damping * depth[::-1] ** 2
    return sigma


def laplacian(p, h):
    """Five-point Laplacian on the interior nodes; zero on the boundary."""
    result = np.zeros_like(p)
    result[1:-1, 1:-1] = (
        p[1:-1, 2:] + p[1:-1, :-2] + p[2:, 1:-1] + p[:-2, 1:-1] - 4.0 * p[1:-1, 1:-1]
    ) / (h * h)
    return result


class MachConeSimulation(Simulation):
    """Pressure at two time levels on a uniform grid around the visible domain.

    One step advances the damped, forced wave equation
    p_tt + sigma p_t = c^2 lap(p) + f by one leapfrog step of ``dt``; the
    outermost nodes stay at p = 0. Rows are y and columns x; the source
    moves up the vertical centre line.
    """

    def __init__(
        self,
        width=WIDTH,
        height=HEIGHT,
        cells_per_wavelength=CELLS_PER_WAVELENGTH,
        sponge_width=SPONGE_WIDTH,
        mach_max=MACH_MAX,
        acceleration_time=ACCELERATION_TIME,
        source_start=SOURCE_START,
        amplitude=SOURCE_AMPLITUDE,
    ):
        super().__init__()
        if cells_per_wavelength < 4 or width <= 0 or height <= 0:
            raise ValueError("need a positive domain and >= 4 cells per wavelength")
        self.h = 1.0 / cells_per_wavelength
        self.dt = COURANT * self.h / SOUND_SPEED
        self.margin = round(sponge_width * cells_per_wavelength)  # sponge cells
        nx = round(width * cells_per_wavelength) + 2 * self.margin + 1
        ny = round(height * cells_per_wavelength) + 2 * self.margin + 1
        # Node coordinates: the visible domain is [0, width] x [0, height].
        self.x = (np.arange(nx) - self.margin) * self.h
        self.y = (np.arange(ny) - self.margin) * self.h
        self.width, self.height = width, height
        sigma_x = sponge_profile(nx, self.margin, SPONGE_DAMPING)
        sigma_y = sponge_profile(ny, self.margin, SPONGE_DAMPING)
        sigma = np.maximum(sigma_x[None, :], sigma_y[:, None])
        self.decay = 1.0 - 0.5 * sigma * self.dt  # leapfrog weights of the damping
        self.gain = 1.0 / (1.0 + 0.5 * sigma * self.dt)
        self.mach_max = mach_max
        self.acceleration_time = acceleration_time
        self.source_start = source_start
        self.amplitude = amplitude
        self.p = np.zeros((ny, nx))  # pressure at time t
        self.p_previous = np.zeros((ny, nx))  # pressure at time t - dt

    @property
    def mach(self):
        return mach_number(self.time, self.mach_max, self.acceleration_time)

    def source_position(self, t=None):
        """(x, y) of the source centre at time t (default: now)."""
        t = self.time if t is None else t
        distance = travelled(t, self.mach_max, self.acceleration_time)
        return 0.5 * self.width, self.source_start + distance

    def source_signal(self, t):
        """Time signal s(t) of the source: a sine of frequency FREQUENCY whose
        amplitude rises as 1 - exp(-(t / RAMP_TIME)^2).

        The smooth start keeps the time integral of s close to zero; a sine
        switched on abruptly would inject a net amount of fluid, which in 2D
        leaves a slowly decaying pressure offset behind the wavefronts.
        """
        envelope = 1.0 - math.exp(-((t / RAMP_TIME) ** 2))
        return self.amplitude * envelope * math.sin(2.0 * math.pi * FREQUENCY * t)

    def add_forcing(self, rate, t):
        """Add the source term s(t) exp(-|x - x_s(t)|^2 / (2 r^2)) to rate.

        Only a patch of five source radii around the source is evaluated;
        the Gaussian is below 4e-6 outside it.
        """
        signal = self.source_signal(t)
        xs, ys = self.source_position(t)
        reach = 5.0 * SOURCE_RADIUS
        cols = slice(*np.searchsorted(self.x, (xs - reach, xs + reach)))
        rows = slice(*np.searchsorted(self.y, (ys - reach, ys + reach)))
        r2 = (self.y[rows, None] - ys) ** 2 + (self.x[None, cols] - xs) ** 2
        rate[rows, cols] += signal * np.exp(-r2 / (2.0 * SOURCE_RADIUS**2))

    def step(self):
        rate = SOUND_SPEED**2 * laplacian(self.p, self.h)
        self.add_forcing(rate, self.time)
        p_next = self.gain * (
            2.0 * self.p - self.decay * self.p_previous + self.dt**2 * rate
        )
        p_next[[0, -1], :] = 0.0
        p_next[:, [0, -1]] = 0.0
        self.p_previous, self.p = self.p, p_next

    def energy(self):
        """Discrete acoustic energy between the two stored time levels.

        E = sum((p - p_prev)/dt)^2 / 2 + c^2 sum(grad p . grad p_prev) / 2,
        times the cell area, with one-sided differences on every grid edge.
        Without forcing and damping the leapfrog scheme conserves it exactly.
        """
        p, q, h = self.p, self.p_previous, self.h
        kinetic = np.sum(((p - q) / self.dt) ** 2)
        gradients = np.sum(np.diff(p, axis=0) * np.diff(q, axis=0)) + np.sum(
            np.diff(p, axis=1) * np.diff(q, axis=1)
        )
        return 0.5 * h * h * (kinetic + SOUND_SPEED**2 * gradients / (h * h))

    @property
    def visible(self):
        """Index slices of the visible domain (without the sponge)."""
        m = self.margin
        return slice(m, self.p.shape[0] - m), slice(m, self.p.shape[1] - m)


class MachConeView(View):
    """Pressure map with the source, its Mach lines and a Mach-number gauge.

    The colour scale is fixed and symmetric, so the Doppler pile-up and the
    Mach cone saturate it. The dashed lines are the theoretical cone of
    half-angle arcsin(1/M) for the current Mach number, drawn once M > 1, and
    a label in the corner names the regime. The gauge bar turns from blue to
    pink when the source passes the dashed line at M = 1.
    """

    figsize = (8.6, 8.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        field_ax, gauge_ax = figure.subplots(1, 2, width_ratios=[1.0, 0.07])
        rows, cols = simulation.visible
        extent = (0.0, simulation.width, 0.0, simulation.height)
        self.image = field_ax.imshow(
            simulation.p[rows, cols], extent=extent, cmap=PRESSURE_CMAP,
            vmin=-PRESSURE_LIMIT, vmax=PRESSURE_LIMIT, interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(
            self.image, ax=field_ax, pad=0.02, fraction=0.05, label="pressure",
            ticks=[-PRESSURE_LIMIT, 0, PRESSURE_LIMIT],
        )  # fmt: skip
        field_ax.set(xlabel="x [wavelengths]", ylabel="y [wavelengths]")
        field_ax.set(xlim=extent[:2], ylim=extent[2:])
        line_style = dict(color="white", linestyle="--", linewidth=1.6, alpha=0.85)
        self.cone = [field_ax.plot([], [], **line_style)[0] for _ in range(2)]
        (self.source,) = field_ax.plot([], [], "o", color="white", markersize=4)
        self.regime = field_ax.text(
            0.03, 0.97, "", transform=field_ax.transAxes, ha="left", va="top",
            fontweight="bold",
        )  # fmt: skip

        gauge_ax.set(xlim=(-0.5, 0.5), ylim=(0.0, 1.1 * MACH_MAX), title="M")
        gauge_ax.set_xticks([])
        gauge_ax.set_yticks(np.arange(0.0, MACH_MAX + 0.1, 0.5))
        gauge_ax.axhline(1.0, color="white", linestyle="--", linewidth=1.2)
        self.bar = Rectangle((-0.5, 0.0), 1.0, 0.0, color="#4cc9f0")
        gauge_ax.add_patch(self.bar)

    def draw(self):
        simulation = self.simulation
        rows, cols = simulation.visible
        self.image.set_data(simulation.p[rows, cols])
        xs, ys = simulation.source_position()
        self.source.set_data([xs], [ys])
        mach = simulation.mach
        self.bar.set_height(mach)
        self.bar.set_color("#f72585" if mach > 1.0 else "#4cc9f0")
        for line, side in zip(self.cone, (-1.0, 1.0)):
            if mach > 1.0:
                angle = math.asin(1.0 / mach)
                tip = (xs + side * CONE_LENGTH * math.sin(angle),
                       ys - CONE_LENGTH * math.cos(angle))  # fmt: skip
                line.set_data([xs, tip[0]], [ys, tip[1]])
            else:
                line.set_data([], [])
        if abs(mach - 1.0) < SOUND_BARRIER_BAND:
            self.regime.set_text("sound barrier")
        elif mach < 1.0:
            self.regime.set_text("subsonic")
        else:
            self.regime.set_text(
                f"Mach cone  μ = {math.degrees(math.asin(1 / mach)):.0f}°"
            )

    def status(self):
        return (
            f"t = {self.simulation.time:.1f} periods   M = {self.simulation.mach:.2f}"
        )


ANIMATION = Animation(
    title="Breaking the Sound Barrier",
    subtitle="A sound source accelerates to Mach 2",
    filename="mach_cone_moving_source.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt = {TIME_STEP:g} periods",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, MachConeSimulation(), MachConeView)
    xs, ys = simulation.source_position()
    print(
        f"t = {simulation.time:.2f} periods: source at y = {ys:.2f} wavelengths, "
        f"M = {simulation.mach:.2f}, max |p| = {np.abs(simulation.p).max():.2f}"
    )


if __name__ == "__main__":
    main()
