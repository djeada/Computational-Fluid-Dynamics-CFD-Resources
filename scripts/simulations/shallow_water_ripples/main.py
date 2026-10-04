"""Raindrops on a pond: ring waves of the 2D shallow-water equations.

Gaussian drops land at seeded random places and times on a square basin of
still water, and the rain gets heavier as time goes on. Their ring waves
spread, reflect from the walls and interfere. The depth h and the discharges
hu, hv are advanced with a conservative finite-volume scheme: MUSCL
reconstruction with the monotonized-central limiter, the Rusanov flux and the
two-stage strong-stability-preserving Runge-Kutta method, on a flat bottom
with reflective walls. The free surface is drawn as a shaded relief lit from
the upper left, so crests and troughs catch the light like water.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LightSource, LinearSegmentedColormap, Normalize
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (SI units)
GRAVITY = 9.81  # g [m/s^2]
BASIN_SIZE = 2.0  # side L of the square basin [m]
DEPTH = 0.02  # still-water depth H [m]; wave speed sqrt(g H) = 0.44 m/s
DROP_AMPLITUDE = 0.005  # mean peak height of a drop's Gaussian mound [m]
DROP_WIDTH = 0.02  # standard deviation sigma of the mound [m]
DROP_MARGIN = 0.15  # drops land at least this far from the walls [m]
FIRST_DROP_TIME = 0.3  # the first drop breaks the calm at this time [s]
RAIN_RATE_START = 0.6  # drops per second at t = FIRST_DROP_TIME [1/s]
RAIN_RATE_END = 4.0  # drops per second at t = RAIN_DURATION [1/s]
RAIN_DURATION = 16.8  # length of the shower: the whole default run [s]
SEED = 0  # random seed of the drop times, places and sizes

# Numerical parameters
GRID_SIZE = 200  # cells per side: dx = L / 200 = 1 cm
TIME_STEP = 0.004  # dt [s]; Courant number dt (|u| + c) (1/dx + 1/dy) ~ 0.4
STEPS_PER_FRAME = 10  # time steps per animation frame (0.04 s)
N_FRAMES = 420  # default frames: 4200 steps reach t = 16.8 s

# Display
ELEVATION_LIMIT = 0.8e-3  # colour range of the surface elevation: +-0.8 mm [m]
VERTICAL_EXAGGERATION = 12.0  # steepens the relief used for the shading
LIGHT_AZIMUTH, LIGHT_ALTITUDE = 315.0, 40.0  # light from the upper left [degrees]
WATER_CMAP = LinearSegmentedColormap.from_list(
    "pond", ["#000814", "#001d3d", "#023e8a", "#0077b6", "#48cae4", "#caf0f8"]
)


def rain_schedule(rng, duration=RAIN_DURATION, size=BASIN_SIZE):
    """Drops as rows (time [s], x [m], y [m], amplitude [m]), sorted by time.

    The rain rate rises linearly from RAIN_RATE_START at FIRST_DROP_TIME to
    RAIN_RATE_END at ``duration``, so the expected number of drops a time s
    after the first one is N(s) = r0 s + (r1 - r0) s^2 / (2 S). Drop k lands
    when N(s) = k + u_k, with u_k uniform in [0, 1) and u_0 = 0: the times are
    random but never leave the long gaps a Poisson process can. Places are
    uniform at least DROP_MARGIN from the walls; amplitudes vary by +-25 %.
    """
    span = duration - FIRST_DROP_TIME
    if span <= 0:
        raise ValueError("the rain must last longer than FIRST_DROP_TIME")
    r0, r1 = RAIN_RATE_START, RAIN_RATE_END
    count = max(1, int(span * (r0 + r1) / 2))
    target = np.arange(count) + rng.uniform(size=count)
    target[0] = 0.0
    # Positive root of (r1 - r0)/(2 S) s^2 + r0 s - target = 0, written stably.
    s = 2 * target / (r0 + np.sqrt(r0**2 + 2 * (r1 - r0) / span * target))
    margin = min(DROP_MARGIN, size / 4)
    x = rng.uniform(margin, size - margin, count)
    y = rng.uniform(margin, size - margin, count)
    amplitude = DROP_AMPLITUDE * rng.uniform(0.75, 1.25, count)
    return np.column_stack([FIRST_DROP_TIME + s, x, y, amplitude])


def pad_reflective(q, ghost=2):
    """Add ghost cells that mirror the edge cells; normal momentum flips sign.

    ``q`` holds (h, hu, hv) with shape (3, ny, nx). A mirrored state on the
    other side of each wall gives zero mass flux through it: a solid wall.
    """
    padded = np.pad(q, ((0, 0), (ghost, ghost), (ghost, ghost)), mode="symmetric")
    padded[1, :, :ghost] *= -1  # hu at the walls x = 0 and x = L
    padded[1, :, -ghost:] *= -1
    padded[2, :ghost, :] *= -1  # hv at the walls y = 0 and y = L
    padded[2, -ghost:, :] *= -1
    return padded


@njit(cache=False)
def limited_slope(left, centre, right):
    """Monotonized-central slope minmod(2 dl, (dl + dr)/2, 2 dr), 0 at extrema."""
    dl, dr = centre - left, right - centre
    if dl * dr <= 0.0:
        return 0.0
    size = min(2.0 * abs(dl), 2.0 * abs(dr), 0.5 * abs(dl + dr))
    return size if dl > 0.0 else -size


@njit(cache=False)
def face_values(line, k):
    """MUSCL states at the face between cells k + 1 and k + 2 of a padded line.

    Each side extrapolates its cell value with half its limited slope.
    """
    a, b, c, d = line[k], line[k + 1], line[k + 2], line[k + 3]
    return b + 0.5 * limited_slope(a, b, c), c - 0.5 * limited_slope(b, c, d)


@njit(cache=False)
def rusanov_flux(h_l, m_l, t_l, h_r, m_r, t_r, g):
    """Rusanov (local Lax-Friedrichs) flux through a face.

    The states are depth h, normal discharge m and tangential discharge t on
    the left and right. The physical flux is (m, m^2/h + g h^2/2, m t/h);
    F = (F_l + F_r)/2 - a (q_r - q_l)/2, where a is the larger of |u| + sqrt(g h)
    on the two sides: the fastest wave that can cross the face.
    """
    u_l, u_r = m_l / h_l, m_r / h_r
    a = max(abs(u_l) + np.sqrt(g * h_l), abs(u_r) + np.sqrt(g * h_r))
    mass = 0.5 * (m_l + m_r) - 0.5 * a * (h_r - h_l)
    normal = 0.5 * (
        m_l * u_l + 0.5 * g * h_l * h_l + m_r * u_r + 0.5 * g * h_r * h_r
    ) - 0.5 * a * (m_r - m_l)
    tangential = 0.5 * (t_l * u_l + t_r * u_r) - 0.5 * a * (t_r - t_l)
    return mass, normal, tangential


@njit(cache=False)
def flux_divergence(padded, dx, g):
    """-(F_east - F_west)/dx - (G_north - G_south)/dy on the interior cells.

    ``padded`` holds (h, hu, hv) with two ghost cells on every side. Face k
    of a row lies between padded cells k + 1 and k + 2, so faces 0 and n are
    the walls. In y the roles of hu and hv swap: hv is the normal discharge.
    """
    _, rows, columns = padded.shape
    ny, nx = rows - 4, columns - 4
    rate = np.zeros((3, ny, nx))
    for j in range(ny):
        row = j + 2
        for k in range(nx + 1):
            h_l, h_r = face_values(padded[0, row], k)
            m_l, m_r = face_values(padded[1, row], k)
            t_l, t_r = face_values(padded[2, row], k)
            flux = rusanov_flux(h_l, m_l, t_l, h_r, m_r, t_r, g)
            for c in range(3):
                if k > 0:
                    rate[c, j, k - 1] -= flux[c] / dx
                if k < nx:
                    rate[c, j, k] += flux[c] / dx
    for i in range(nx):
        column = i + 2
        for k in range(ny + 1):
            h_l, h_r = face_values(padded[0, :, column], k)
            m_l, m_r = face_values(padded[2, :, column], k)
            t_l, t_r = face_values(padded[1, :, column], k)
            mass, normal, tangential = rusanov_flux(h_l, m_l, t_l, h_r, m_r, t_r, g)
            flux = (mass, tangential, normal)  # back to (h, hu, hv)
            for c in range(3):
                if k > 0:
                    rate[c, k - 1, i] -= flux[c] / dx
                if k < ny:
                    rate[c, k, i] += flux[c] / dx
    return rate


def shallow_water_rhs(q, dx, g=GRAVITY):
    """Finite-volume rate dq/dt of (h, hu, hv) on square cells of side dx."""
    return flux_divergence(pad_reflective(q), dx, g)


def ssp_rk2_step(q, dx, dt):
    """Two-stage strong-stability-preserving Runge-Kutta (Heun) step."""
    stage = q + dt * shallow_water_rhs(q, dx)
    return 0.5 * (q + stage + dt * shallow_water_rhs(stage, dx))


def courant_number(q, dx, dt, g=GRAVITY):
    """dt (max(|u| + c)/dx + max(|v| + c)/dy) for square cells, c = sqrt(g h)."""
    h, hu, hv = q
    c = np.sqrt(g * h)
    return dt / dx * (np.max(np.abs(hu / h) + c) + np.max(np.abs(hv / h) + c))


class ShallowWaterSimulation(Simulation):
    """Depth and discharges on the basin, with the drops still to land.

    ``q`` has shape (3, n, n): h, hu and hv on cells whose rows are y and
    columns x. ``drops`` overrides the seeded rain with rows (time, x, y,
    amplitude); an empty list keeps the water still.
    """

    dt = TIME_STEP

    def __init__(self, n=GRID_SIZE, seed=SEED, drops=None, size=BASIN_SIZE):
        super().__init__()
        if n < 4:
            raise ValueError("at least four cells per side are required")
        self.dx = size / n
        centres = (np.arange(n) + 0.5) * self.dx
        self.x, self.y = np.meshgrid(centres, centres)
        if drops is None:
            drops = rain_schedule(np.random.default_rng(seed), size=size)
        self.drops = np.asarray(drops, dtype=float).reshape(-1, 4)
        self.q = np.zeros((3, n, n))
        self.q[0] = DEPTH
        self.initial_volume = self.volume()
        self.added_volume = 0.0  # water brought in by the drops [m^3]
        self.drops_landed = 0

    @property
    def h(self):
        return self.q[0]

    @property
    def eta(self):
        """Surface elevation above the current mean water level [m]."""
        return self.q[0] - self.q[0].mean()

    def volume(self):
        return self.q[0].sum() * self.dx**2

    def add_drop(self, x0, y0, amplitude):
        """Raise the surface by a Gaussian mound: the water of one drop."""
        r2 = (self.x - x0) ** 2 + (self.y - y0) ** 2
        mound = amplitude * np.exp(-r2 / (2 * DROP_WIDTH**2))
        self.q[0] += mound
        self.added_volume += mound.sum() * self.dx**2

    def step(self):
        while (
            self.drops_landed < len(self.drops)
            and self.drops[self.drops_landed, 0] <= self.time
        ):
            self.add_drop(*self.drops[self.drops_landed, 1:])
            self.drops_landed += 1
        self.q = ssp_rk2_step(self.q, self.dx, self.dt)


class RipplesView(View):
    """The free surface as shaded relief over a blue elevation colour map.

    Troughs are deep blue and crests pale; a light source in the upper left
    brightens slopes that face it, which makes the rings read as water. The
    square basin fills the window and the nearly square reel panel alike.
    """

    figsize = (7.4, 6.4)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        self.light = LightSource(azdeg=LIGHT_AZIMUTH, altdeg=LIGHT_ALTITUDE)
        self.norm = Normalize(-ELEVATION_LIMIT, ELEVATION_LIMIT)
        size = simulation.dx * simulation.h.shape[1]
        self.image = ax.imshow(
            self.shaded(), extent=(0, size, 0, size), origin="lower",
            interpolation="bilinear",
        )  # fmt: skip
        millimetres = Normalize(-1e3 * ELEVATION_LIMIT, 1e3 * ELEVATION_LIMIT)
        # Below the basin in a reel, so the square image can use the full width.
        figure.colorbar(
            ScalarMappable(millimetres, WATER_CMAP), ax=ax,
            location="bottom" if portrait else "right", shrink=0.8 if portrait else 1,
            label="surface elevation η [mm]",
        )  # fmt: skip
        ax.set(xlabel="x [m]", ylabel="y [m]")

    def shaded(self):
        """RGBA image of the surface: colour by height, brightness by slope."""
        dx = self.simulation.dx
        # Rows run upwards (origin="lower"), so dy is negated for LightSource,
        # which assumes rows that run down the image.
        return self.light.shade(
            self.simulation.eta, cmap=WATER_CMAP, norm=self.norm, blend_mode="hsv",
            vert_exag=VERTICAL_EXAGGERATION, dx=dx, dy=-dx,
        )  # fmt: skip

    def draw(self):
        self.image.set_data(self.shaded())

    def status(self):
        simulation = self.simulation
        return f"t = {simulation.time:.1f} s   drops {simulation.drops_landed}"


ANIMATION = Animation(
    title="Raindrops on a Pond",
    subtitle="Shallow-water ring waves, finite volumes",
    filename="shallow_water_ripples.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of {TIME_STEP:g} s",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, ShallowWaterSimulation(), RipplesView)
    error = (
        simulation.volume() - simulation.initial_volume - simulation.added_volume
    ) / simulation.initial_volume
    courant = courant_number(simulation.q, simulation.dx, simulation.dt)
    print(
        f"t = {simulation.time:.2f} s: {simulation.drops_landed} of "
        f"{len(simulation.drops)} drops landed, "
        f"volume error {error:.1e} (relative), Courant number {courant:.2f}"
    )


if __name__ == "__main__":
    main()
