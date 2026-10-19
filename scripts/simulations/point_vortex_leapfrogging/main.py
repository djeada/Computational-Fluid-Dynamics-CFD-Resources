"""Leapfrogging of two coaxial vortex pairs, the 2D analogue of two smoke rings.

Four point vortices form two identical vortex pairs, one behind the other,
that travel up the screen. The rear pair contracts, speeds up and slips
through the front pair, which widens and slows down; then the roles swap, again
and again. The vortices are integrated with the fourth-order Runge-Kutta
method, and 240 000 passive smoke tracers seeded around them are carried by
the same velocity field. The view follows the pairs: smoke is drawn as glowing
colour (cyan and orange, one colour per pair) with fading trails of the
vortex paths.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
from numba import njit, prange
from scipy.ndimage import gaussian_filter

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Vortices (nondimensional units)
CIRCULATION = 2 * np.pi  # Gamma of each vortex [length^2 / time]: Gamma / 2 pi = 1
HALF_WIDTH = 1.0  # b, half-width of both pairs at the start [length]
ALPHA = 0.4  # inner / outer half-width when the pairs pass side by side [-]
LOVE_LIMIT = 3 - 2 * np.sqrt(2)  # ~0.172: below it the pairs never pass (Love 1894)
STABILITY_LIMIT = (3 - np.sqrt(5)) / 2  # ~0.382: leapfrogging is stable above it
CORE_RADIUS = 0.15  # delta, Krasny smoothing length of every vortex [length]
PERTURBATION = 1e-3  # sideways shift of one vortex, breaks the mirror symmetry [length]

# Smoke tracers and time stepping
SMOKE_PER_VORTEX = 60_000  # tracers in the Gaussian smoke blob around each vortex
SMOKE_RADIUS = 0.25  # standard deviation of each smoke blob [length]
SEED = 0  # random positions of the smoke tracers
TIME_STEP = 0.0025  # RK4 step dt [time]
STEPS_PER_FRAME = 20  # RK4 steps per animation frame (0.05 time units)
N_FRAMES = 300  # default frames: t = 15, ten leapfrogs at ALPHA = 0.4

# Display, in a frame that moves with the centroid of the four vortices
VIEW_X = (-2.4, 2.4)  # x range of the view [length]
VIEW_Y = (-3.4, 1.4)  # y range relative to the centroid [length]
IMAGE_SIZE = 480  # pixels per side of the smoke image
SMOKE_BLUR = 0.8  # Gaussian blur of the smoke image [pixels]
SMOKE_GAIN = 2.0  # smoke brightness 1 - exp(-gain * (density / initial peak)^gamma)
SMOKE_GAMMA = 0.6  # gamma < 1 brightens thin filaments more than the dense cores
GLOW_RADIUS = 0.06  # size of the glow drawn at each vortex [length]
TRAIL_TIME = 1.5  # length of the fading vortex trails [time]
TRAIL_POINTS = 120  # points per trail
PAIR_COLOURS = ("#33ccff", "#ff8c42")  # rear pair at the start, front pair


def pair_separation(alpha, half_width=HALF_WIDTH):
    """Gap L between two identical pairs that pass each other with ratio alpha.

    Two pairs of half-width b, one a distance L behind the other, pass side by
    side with half-widths alpha A and A. Conservation of impulse gives
    A (1 + alpha) = 2b and conservation of energy gives
    L^2 / (4 b^2 + L^2) = (1 - alpha)^2 / (4 alpha), exact for point vortices.
    """
    if not LOVE_LIMIT < alpha < 1:
        raise ValueError(f"alpha must lie between {LOVE_LIMIT:.4f} and 1")
    return 2 * half_width * (1 - alpha) / np.sqrt(6 * alpha - alpha**2 - 1)


def initial_vortices(alpha=ALPHA, half_width=HALF_WIDTH, perturbation=PERTURBATION):
    """Positions and circulations of two identical pairs moving in +y.

    Vortices 0 and 1 form the rear pair, 2 and 3 the front pair; left vortices
    turn counter-clockwise (+Gamma), right ones clockwise (-Gamma). The pairs
    start a distance pair_separation(alpha) apart, centred on y = 0.
    """
    gap = pair_separation(alpha, half_width)
    x = np.array([-1.0, 1.0, -1.0, 1.0]) * half_width
    y = np.array([-0.5, -0.5, 0.5, 0.5]) * gap
    x[0] += perturbation
    circulation = np.array([1.0, -1.0, 1.0, -1.0]) * CIRCULATION
    return x, y, circulation


@njit(cache=False)
def induced_velocity(px, py, x, y, circulation, core):
    """Velocity at (px, py) induced by Krasny-smoothed vortices at (x, y)."""
    u = 0.0
    v = 0.0
    core2 = core * core
    for j in range(x.size):
        dx = px - x[j]
        dy = py - y[j]
        r2 = dx * dx + dy * dy + core2
        if r2 > 0.0:
            u -= circulation[j] * dy / r2
            v += circulation[j] * dx / r2
    return u / (2 * np.pi), v / (2 * np.pi)


@njit(cache=False)
def vortex_velocities(x, y, circulation, core):
    """Velocity of every vortex induced by all the others.

    A vortex induces no velocity at its own centre, so the sum may include it.
    """
    u = np.empty(x.size)
    v = np.empty(x.size)
    for k in range(x.size):
        u[k], v[k] = induced_velocity(x[k], y[k], x, y, circulation, core)
    return u, v


@njit(cache=False, parallel=True)
def rk4_step(x, y, px, py, circulation, core, dt):
    """Advance vortices (x, y) and tracers (px, py) in place by one RK4 step.

    The tracers use the vortex positions of each Runge-Kutta stage, so the
    vortices and tracers together form one system integrated with RK4.
    """
    k1u, k1v = vortex_velocities(x, y, circulation, core)
    x2, y2 = x + 0.5 * dt * k1u, y + 0.5 * dt * k1v
    k2u, k2v = vortex_velocities(x2, y2, circulation, core)
    x3, y3 = x + 0.5 * dt * k2u, y + 0.5 * dt * k2v
    k3u, k3v = vortex_velocities(x3, y3, circulation, core)
    x4, y4 = x + dt * k3u, y + dt * k3v
    k4u, k4v = vortex_velocities(x4, y4, circulation, core)
    for i in prange(px.size):
        qx, qy = px[i], py[i]
        a1, b1 = induced_velocity(qx, qy, x, y, circulation, core)
        a2, b2 = induced_velocity(
            qx + 0.5 * dt * a1, qy + 0.5 * dt * b1, x2, y2, circulation, core
        )
        a3, b3 = induced_velocity(
            qx + 0.5 * dt * a2, qy + 0.5 * dt * b2, x3, y3, circulation, core
        )
        a4, b4 = induced_velocity(qx + dt * a3, qy + dt * b3, x4, y4, circulation, core)
        px[i] = qx + dt / 6.0 * (a1 + 2.0 * a2 + 2.0 * a3 + a4)
        py[i] = qy + dt / 6.0 * (b1 + 2.0 * b2 + 2.0 * b3 + b4)
    x += dt / 6.0 * (k1u + 2.0 * k2u + 2.0 * k3u + k4u)
    y += dt / 6.0 * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)


@njit(cache=False)
def count_smoke(px, py, pair, x_range, y_range, n_pixels):
    """Tracers of each pair in each pixel of the square view."""
    counts = np.zeros((2, n_pixels, n_pixels))
    x_scale = n_pixels / (x_range[1] - x_range[0])
    y_scale = n_pixels / (y_range[1] - y_range[0])
    for i in range(px.size):
        column = int(np.floor((px[i] - x_range[0]) * x_scale))
        row = int(np.floor((py[i] - y_range[0]) * y_scale))
        if 0 <= column < n_pixels and 0 <= row < n_pixels:
            counts[pair[i], row, column] += 1.0
    return counts


def hamiltonian(x, y, circulation, core=CORE_RADIUS):
    """Interaction energy H = -1/(4 pi) sum_{j<k} G_j G_k ln(r_jk^2 + delta^2)."""
    j, k = np.triu_indices(len(x), 1)
    r2 = (x[j] - x[k]) ** 2 + (y[j] - y[k]) ** 2 + core**2
    return -np.sum(circulation[j] * circulation[k] * np.log(r2)) / (4 * np.pi)


def linear_impulse(x, y, circulation):
    """Linear impulse (sum G y, -sum G x)."""
    return np.array([np.sum(circulation * y), -np.sum(circulation * x)])


def angular_impulse(x, y, circulation):
    """Angular impulse sum G (x^2 + y^2)."""
    return np.sum(circulation * (x**2 + y**2))


def half_widths(x):
    """Half-widths of the rear-start pair (0, 1) and front-start pair (2, 3)."""
    return np.array([x[1] - x[0], x[3] - x[2]]) / 2


class LeapfrogSimulation(Simulation):
    """Four vortices and their smoke, with the vortex paths recorded.

    ``history`` holds the vortex positions after every step (shape
    steps + 1 by 2 by 4), and ``leapfrogs`` counts how often one pair has
    passed through the other.
    """

    dt = TIME_STEP

    def __init__(
        self,
        alpha=ALPHA,
        smoke_per_vortex=SMOKE_PER_VORTEX,
        core=CORE_RADIUS,
        dt=TIME_STEP,
        seed=SEED,
    ):
        super().__init__()
        self.alpha = alpha
        self.core = core
        self.dt = dt
        self.x, self.y, self.circulation = initial_vortices(alpha)
        rng = np.random.default_rng(seed)
        blobs = rng.normal(0.0, SMOKE_RADIUS, size=(2, 4, smoke_per_vortex))
        self.px = (self.x[:, None] + blobs[0]).ravel()
        self.py = (self.y[:, None] + blobs[1]).ravel()
        self.pair = np.repeat([0, 0, 1, 1], smoke_per_vortex)
        self.peak_density = smoke_per_vortex / (2 * np.pi * SMOKE_RADIUS**2)
        self.history = [np.array([self.x, self.y])]
        self.leapfrogs = 0
        self.order = self.pair_order()

    def pair_order(self):
        """+1 while the front-start pair leads, -1 while the other one does."""
        return np.sign(self.y[2:].mean() - self.y[:2].mean())

    def step(self):
        rk4_step(self.x, self.y, self.px, self.py, self.circulation, self.core, self.dt)
        self.history.append(np.array([self.x, self.y]))
        order = self.pair_order()
        if order != self.order and order != 0:
            self.leapfrogs += 1
            self.order = order

    def centroid(self):
        """Mean position of the four vortices, which the view follows."""
        return self.x.mean(), self.y.mean()

    def invariants(self):
        """H, linear impulse (x, y) and angular impulse of the vortices."""
        args = (self.x, self.y, self.circulation)
        return (
            hamiltonian(*args, core=self.core),
            *linear_impulse(*args),
            angular_impulse(*args),
        )


class LeapfrogView(View):
    """Glowing smoke and vortex trails in a square frame that follows the pairs.

    The smoke image is the tracer density of each pair, tone mapped to cyan
    and orange and blurred by a fraction of a pixel; the vortices glow white
    and leave fading trails of their paths. The vertical axis is measured
    from the centroid of the four vortices, so the picture stays centred while
    the pairs travel upward.
    """

    figsize = (7.2, 7.4)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        self.colours = np.array([to_rgb(colour) for colour in PAIR_COLOURS])
        self.image = ax.imshow(
            self.smoke_image(), extent=(*VIEW_X, *VIEW_Y), interpolation="bilinear"
        )
        self.trails = LineCollection([], linewidths=2.5 if portrait else 1.4)
        ax.add_collection(self.trails)
        ax.set(xlim=VIEW_X, ylim=VIEW_Y, xlabel="$x$", ylabel=r"$y - \bar{y}$")
        ax.set_title("Smoke of the two pairs")

    def smoke_image(self):
        simulation = self.simulation
        x_centre, y_centre = simulation.centroid()
        y_range = (y_centre + VIEW_Y[0], y_centre + VIEW_Y[1])
        counts = count_smoke(
            simulation.px, simulation.py, simulation.pair,
            np.array(VIEW_X), np.array(y_range), IMAGE_SIZE,
        )  # fmt: skip
        pixel_area = (VIEW_X[1] - VIEW_X[0]) * (y_range[1] - y_range[0]) / IMAGE_SIZE**2
        density = gaussian_filter(counts, (0, SMOKE_BLUR, SMOKE_BLUR))
        density = (density / (simulation.peak_density * pixel_area)) ** SMOKE_GAMMA
        light = np.tensordot(density, self.colours, axes=(0, 0))
        image = 1 - np.exp(-SMOKE_GAIN * light)
        # White-hot glow at each vortex.
        rows = np.linspace(*y_range, IMAGE_SIZE)[:, None]
        columns = np.linspace(*VIEW_X, IMAGE_SIZE)[None, :]
        for vortex_x, vortex_y in zip(simulation.x, simulation.y):
            r2 = (columns - vortex_x) ** 2 + (rows - vortex_y) ** 2
            image += np.exp(-r2 / (2 * GLOW_RADIUS**2))[..., None]
        return np.clip(image, 0.0, 1.0)

    def trail_segments(self):
        """Faded segments of the recent vortex paths, relative to the centroid."""
        simulation = self.simulation
        steps = max(2, round(TRAIL_TIME / simulation.dt))
        recent = np.array(simulation.history[-steps:])
        recent = recent[np.linspace(0, len(recent) - 1, TRAIL_POINTS).astype(int)]
        recent[:, 1] -= simulation.centroid()[1]
        points = recent.transpose(2, 0, 1)  # vortex, time, (x, y)
        segments = np.stack([points[:, :-1], points[:, 1:]], axis=2)
        fade = np.linspace(0.0, 0.9, segments.shape[1])
        colours = np.zeros(segments.shape[:2] + (4,))
        colours[..., :3] = self.colours[[0, 0, 1, 1]][:, None]
        colours[..., 3] = fade
        return segments.reshape(-1, 2, 2), colours.reshape(-1, 4)

    def draw(self):
        self.image.set_data(self.smoke_image())
        segments, colours = self.trail_segments()
        self.trails.set_segments(segments)
        self.trails.set_color(colours)

    def status(self):
        return f"t = {self.simulation.time:.2f}   leapfrogs {self.simulation.leapfrogs}"


ANIMATION = Animation(
    title="Leapfrogging Vortex Pairs",
    subtitle="Two vortex pairs take turns passing through",
    filename="point_vortex_leapfrogging.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"RK4 steps of dt = {TIME_STEP:g}",
)


def ratio(text):
    value = float(text)
    if not LOVE_LIMIT < value < 1:
        raise ValueError(text)
    return value


def main(argv=None):
    parser = ANIMATION.parser(__doc__)
    parser.add_argument(
        "--alpha",
        type=ratio,
        default=ALPHA,
        metavar="A",
        help="inner / outer pair half-width as the pairs pass, between "
        f"{LOVE_LIMIT:.3f} and 1 (default: %(default)g); leapfrogging is stable "
        f"above {STABILITY_LIMIT:.3f}, try 0.3 to watch it break up",
    )
    args = parser.parse_args(argv)
    simulation = LeapfrogSimulation(alpha=args.alpha)
    start = simulation.invariants()
    ANIMATION.run(args, simulation, LeapfrogView)
    end = simulation.invariants()
    drift = abs(end[0] - start[0]) / abs(start[0])
    print(
        f"alpha = {args.alpha:g}, t = {simulation.time:g}: "
        f"{simulation.leapfrogs} leapfrogs, relative energy drift {drift:.1e}, "
        f"impulse change {abs(end[2] - start[2]):.1e}"
    )


if __name__ == "__main__":
    main()
