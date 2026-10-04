"""Gray-Scott reaction-diffusion: a seeded square grows into dividing spots.

Two chemicals react, U + 2V -> 3V and V -> P, and diffuse on a periodic square
grid. U is fed in at rate F, V is removed at rate F + k. A small square seeded
with V at the centre grows into self-replicating spots ("mitosis") or branching
coral, depending on (F, k), as in Pearson (1993). The equations are advanced
with explicit Euler and the periodic 5-point Laplacian, and the colour map
shows the concentration of V.
"""

import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Model parameters, in the dimensionless units of Pearson (1993)
DIFFUSIVITY_U = 2e-5  # D_u [length^2 / time]
DIFFUSIVITY_V = 1e-5  # D_v [length^2 / time]
PATTERNS = {  # name: (feed rate F, kill rate k) [1 / time]
    "mitosis": (0.0367, 0.0649),  # spots that divide until they fill the domain
    "coral": (0.0545, 0.062),  # branching stripes that grow outwards
}
DEFAULT_PATTERN = "mitosis"

# Grid and time stepping
GRID_SIZE = 256  # cells per side of the periodic square
GRID_SPACING = 2.5 / 256  # h [length]: the default domain is 2.5 x 2.5
TIME_STEP = 1.0  # dt [time]; D_u dt / h^2 = 0.21 < 1/4, see stability_limit
SEED_SIZE = 20  # side of the perturbed central square [cells]
SEED_U, SEED_V = 0.5, 0.25  # concentrations inside the seed square
NOISE_AMPLITUDE = 0.01  # uniform noise in [-0.01, 0.01] added to both fields
SEED = 0  # random seed of the noise
COVER_THRESHOLD = 0.1  # cells with V above this count as covered by the pattern
V_MAX = 0.4  # top of the fixed colour scale (V stays below about 0.45)
STEPS_PER_FRAME = 100  # time steps per animation frame
N_FRAMES = 250  # default frames -> t = 25 000, when the spots fill the domain


def laplacian(field, h=GRID_SPACING):
    """Periodic 5-point Laplacian (f_E + f_W + f_N + f_S - 4 f) / h^2."""
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4.0 * field
    ) / h**2


def laplacian_eigenvalue(mode_x, mode_y, n, h=GRID_SPACING):
    """Eigenvalue of ``laplacian`` for the Fourier mode exp(2 pi i (m x + l y) / n h)."""
    return (
        -4.0
        / h**2
        * (np.sin(np.pi * mode_x / n) ** 2 + np.sin(np.pi * mode_y / n) ** 2)
    )


def reaction(u, v, feed, kill):
    """Reaction terms of the U and V equations: -uv^2 + F(1 - u), uv^2 - (F + k)v."""
    uvv = u * v * v
    return -uvv + feed * (1.0 - u), uvv - (feed + kill) * v


def euler_step(u, v, feed, kill, h=GRID_SPACING, dt=TIME_STEP):
    """One explicit Euler step of both reaction-diffusion equations."""
    reaction_u, reaction_v = reaction(u, v, feed, kill)
    u_next = u + dt * (DIFFUSIVITY_U * laplacian(u, h) + reaction_u)
    v_next = v + dt * (DIFFUSIVITY_V * laplacian(v, h) + reaction_v)
    return u_next, v_next


def homogeneous_states(feed, kill):
    """Spatially uniform steady states (u, v): (1, 0) and, if F >= 4(F + k)^2, two more.

    Setting both reaction terms to zero with v != 0 gives u v = F + k and
    (F + k) v^2 - F v + F (F + k) = 0.
    """
    states = [(1.0, 0.0)]
    rate = feed + kill
    discriminant = feed**2 - 4.0 * feed * rate**2
    if discriminant >= 0:
        for sign in (1.0, -1.0):
            v = (feed + sign * np.sqrt(discriminant)) / (2.0 * rate)
            states.append((rate / v, v))
    return states


def stability_limit(feed, kill, h=GRID_SPACING):
    """Largest stable explicit Euler step for the equations linearised about (1, 0).

    A Fourier mode of a species with diffusivity D and decay rate r is
    multiplied by 1 + dt (D lambda - r) per step, with lambda down to -8 / h^2
    for the checkerboard mode, so |1 + dt (D lambda - r)| <= 1 needs
    dt <= 2 / (8 D / h^2 + r). U decays at rate F, V at rate F + k.
    """
    limit_u = 2.0 / (8.0 * DIFFUSIVITY_U / h**2 + feed)
    limit_v = 2.0 / (8.0 * DIFFUSIVITY_V / h**2 + feed + kill)
    return min(limit_u, limit_v)


def seed_fields(n, rng, seed_size=SEED_SIZE):
    """U = 1, V = 0 except a central square at (1/2, 1/4), plus small noise."""
    u = np.ones((n, n))
    v = np.zeros((n, n))
    size = min(seed_size, n // 2)
    square = slice(n // 2 - size // 2, n // 2 - size // 2 + size)
    u[square, square] = SEED_U
    v[square, square] = SEED_V
    u += NOISE_AMPLITUDE * rng.uniform(-1.0, 1.0, (n, n))
    v += NOISE_AMPLITUDE * rng.uniform(-1.0, 1.0, (n, n))
    return np.clip(u, 0.0, 1.0), np.clip(v, 0.0, 1.0)


class GrayScottSimulation(Simulation):
    """Concentrations U and V on an n x n periodic grid of spacing GRID_SPACING."""

    dt = TIME_STEP

    def __init__(self, n=GRID_SIZE, pattern=DEFAULT_PATTERN, seed=SEED):
        super().__init__()
        if n < 4:
            raise ValueError("at least four cells per side are required")
        self.pattern = pattern
        self.feed, self.kill = PATTERNS[pattern]
        self.length = n * GRID_SPACING
        self.u, self.v = seed_fields(n, np.random.default_rng(seed))

    def step(self):
        self.u, self.v = euler_step(self.u, self.v, self.feed, self.kill)

    @property
    def covered_fraction(self):
        """Fraction of the cells where V exceeds COVER_THRESHOLD."""
        return float(np.mean(self.v > COVER_THRESHOLD))


class GrayScottView(View):
    """V on a fixed scale with the inferno colour map: black where U is untouched."""

    figsize = (7.0, 6.2)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        length = simulation.length
        self.image = ax.imshow(
            simulation.v, cmap="inferno", vmin=0.0, vmax=V_MAX,
            extent=(0.0, length, 0.0, length), interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(self.image, ax=ax, label="concentration of V")
        ax.set(
            title=f"{simulation.pattern.capitalize()}: "
            f"F = {simulation.feed:g}, k = {simulation.kill:g}",
            xlabel="x",
            ylabel="y",
        )

    def draw(self):
        self.image.set_data(self.simulation.v)

    def status(self):
        simulation = self.simulation
        return (
            f"t = {simulation.time:,.0f}   "
            f"V > {COVER_THRESHOLD:g} on {simulation.covered_fraction:.0%}"
        )


ANIMATION = Animation(
    title="Reaction-Diffusion Patterns",
    subtitle="Gray-Scott model: two chemicals self-organise",
    filename="gray_scott_reaction_diffusion.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    parser = ANIMATION.parser(__doc__)
    parser.add_argument(
        "--pattern",
        choices=PATTERNS,
        default=DEFAULT_PATTERN,
        help="(F, k) preset: dividing spots or branching coral (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    simulation = ANIMATION.run(
        args, GrayScottSimulation(pattern=args.pattern), GrayScottView
    )
    print(
        f"{simulation.pattern}: t = {simulation.time:g} after {simulation.steps} "
        f"steps, V > {COVER_THRESHOLD:g} on {simulation.covered_fraction:.1%} "
        f"of the domain, max V = {simulation.v.max():.3f}"
    )


if __name__ == "__main__":
    main()
