"""Lid-driven cavity flow at Re = 100 with an explicit projection method.

The 2D incompressible Navier-Stokes equations are advanced with forward Euler
and second-order central differences on a collocated 129 x 129 grid; a Jacobi
pressure Poisson solve projects the velocity at every step. Contours of u and v
are animated, and ``--compare-ghia`` adds the vertical-centreline u profile
against the Re = 100 benchmark of Ghia, Ghia & Shin (1982).
"""

import sys
from pathlib import Path

import numpy as np
from numpy import ndarray

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (SI units)
CAVITY_SIZE: float = 1.0  # side length L [m]
LID_VELOCITY: float = 1.0  # U [m/s]
KINEMATIC_VISCOSITY: float = 0.01  # nu [m^2/s]  -> Re = U L / nu = 100
DENSITY: float = 1.0  # rho [kg/m^3]

# Numerical parameters
N_POINTS: int = 129  # grid points per side (same grid as Ghia et al.)
TIME_STEP: float = 1e-3  # dt [s]; nu*dt/h^2 = 0.16 < 0.25 and U*dt/h = 0.13
STEPS_PER_FRAME: int = 100  # time steps between animation frames
N_FRAMES: int = 150  # default frames -> t = 15 s, close to steady state
N_PRESSURE_POISSON_ITERATIONS: int = 50  # Jacobi sweeps per time step
EPSILON: float = 1e-6  # avoids a zero range for the colour scale
REYNOLDS: float = LID_VELOCITY * CAVITY_SIZE / KINEMATIC_VISCOSITY

# Ghia, Ghia & Shin (1982), J. Comput. Phys. 48, 387-411, Table I, Re = 100:
# u-velocity along the vertical line through the geometric centre of the cavity.
GHIA_Y = np.array(
    [1.0000, 0.9766, 0.9688, 0.9609, 0.9531, 0.8516, 0.7344, 0.6172, 0.5000,
     0.4531, 0.2813, 0.1719, 0.1016, 0.0703, 0.0625, 0.0547, 0.0000]
)  # fmt: skip
GHIA_U = np.array(
    [1.00000, 0.84123, 0.78871, 0.73722, 0.68717, 0.23151, 0.00332, -0.13641,
     -0.20581, -0.21090, -0.15662, -0.10150, -0.06434, -0.04775, -0.04192,
     -0.03717, 0.00000]
)  # fmt: skip


def central_difference_x(f: ndarray, element_length: float) -> ndarray:
    diff = np.zeros_like(f)
    diff[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * element_length)
    return diff


def central_difference_y(f: ndarray, element_length: float) -> ndarray:
    diff = np.zeros_like(f)
    diff[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2 * element_length)
    return diff


def laplace(f: ndarray, element_length: float) -> ndarray:
    lap = np.zeros_like(f)
    lap[1:-1, 1:-1] = (
        f[1:-1, :-2] + f[:-2, 1:-1] + f[1:-1, 2:] + f[2:, 1:-1] - 4 * f[1:-1, 1:-1]
    ) / (element_length**2)
    return lap


def apply_boundary_conditions(
    u: ndarray, v: ndarray, horizontal_velocity_top: float
) -> tuple[ndarray, ndarray]:
    """No-slip walls; the top row (y = L) moves with the lid."""
    u[0, :], u[:, 0], u[:, -1], u[-1, :] = 0.0, 0.0, 0.0, horizontal_velocity_top
    v[0, :], v[:, 0], v[:, -1], v[-1, :] = 0.0, 0.0, 0.0, 0.0
    return u, v


def solve_pressure_poisson(p: ndarray, rhs: ndarray, element_length: float) -> ndarray:
    """Jacobi sweeps for lap(p) = rhs with dp/dn = 0 on all walls.

    The pure-Neumann problem fixes p only up to a constant, so the mean is removed.
    The solution from the previous time step is used as the initial guess.
    """
    for _ in range(N_PRESSURE_POISSON_ITERATIONS):
        p_next = np.copy(p)
        p_next[1:-1, 1:-1] = 0.25 * (
            p[1:-1, :-2]
            + p[:-2, 1:-1]
            + p[1:-1, 2:]
            + p[2:, 1:-1]
            - element_length**2 * rhs[1:-1, 1:-1]
        )
        p_next[:, -1] = p_next[:, -2]
        p_next[:, 0] = p_next[:, 1]
        p_next[0, :] = p_next[1, :]
        p_next[-1, :] = p_next[-2, :]
        p = p_next - p_next.mean()
    return p


def time_step(
    u: ndarray, v: ndarray, p: ndarray, element_length: float
) -> tuple[ndarray, ndarray, ndarray]:
    """One projection step: explicit predictor, pressure solve, correction."""
    h, dt = element_length, TIME_STEP
    u_tent = u + dt * (
        -(u * central_difference_x(u, h) + v * central_difference_y(u, h))
        + KINEMATIC_VISCOSITY * laplace(u, h)
    )
    v_tent = v + dt * (
        -(u * central_difference_x(v, h) + v * central_difference_y(v, h))
        + KINEMATIC_VISCOSITY * laplace(v, h)
    )
    u_tent, v_tent = apply_boundary_conditions(u_tent, v_tent, LID_VELOCITY)

    divergence = central_difference_x(u_tent, h) + central_difference_y(v_tent, h)
    p = solve_pressure_poisson(p, DENSITY * divergence / dt, h)

    u = u_tent - dt / DENSITY * central_difference_x(p, h)
    v = v_tent - dt / DENSITY * central_difference_y(p, h)
    u, v = apply_boundary_conditions(u, v, LID_VELOCITY)
    return u, v, p


def centreline_u(u: ndarray, y: ndarray) -> tuple[ndarray, ndarray]:
    """u / U along x = L/2, sampled at the Ghia et al. y / L locations."""
    profile = u[:, u.shape[1] // 2] / LID_VELOCITY
    return profile, np.interp(GHIA_Y * CAVITY_SIZE, y, profile)


class CavitySimulation(Simulation):
    """Projection-solver state independent of animation and benchmark plotting."""

    dt = TIME_STEP

    def __init__(self, n_points=N_POINTS):
        super().__init__()
        if n_points < 3:
            raise ValueError("at least three points per axis are required")
        self.y = np.linspace(0.0, CAVITY_SIZE, n_points)
        self.element_length = CAVITY_SIZE / (n_points - 1)
        self.u = np.zeros((n_points, n_points))
        self.v = np.zeros_like(self.u)
        self.p = np.zeros_like(self.u)
        apply_boundary_conditions(self.u, self.v, LID_VELOCITY)

    def step(self):
        self.u, self.v, self.p = time_step(self.u, self.v, self.p, self.element_length)

    def ghia_error(self):
        """Centreline u / U minus the Ghia et al. values at their 17 points."""
        return centreline_u(self.u, self.y)[1] - GHIA_U


class CavityView(View):
    """u and v colour maps, plus the centreline profile with compare_ghia.

    Panels sit side by side in the window. A reel stacks u above v, or puts
    them side by side above the profile. Colour scales are symmetric about
    zero, so white marks fluid at rest.
    """

    def __init__(self, simulation, figure, portrait=False, compare_ghia=False):
        super().__init__(simulation, figure, portrait)
        names = ["u", "v", "profile"] if compare_ghia else ["u", "v"]
        self.figsize = (5.5 * len(names), 5.5)
        if not portrait:
            mosaic = [names]
        elif compare_ghia:
            mosaic = [["u", "v"], ["profile", "profile"]]
        else:
            mosaic = [["u"], ["v"]]
        axes = figure.subplot_mosaic(mosaic)
        extent = (0.0, CAVITY_SIZE, 0.0, CAVITY_SIZE)
        self.images = {}
        for name in ("u", "v"):
            ax = axes[name]
            self.images[name] = ax.imshow(
                getattr(simulation, name), extent=extent, cmap="coolwarm",
                interpolation="bilinear",
            )  # fmt: skip
            # Side-by-side squares in a reel leave no room for vertical bars.
            location = "bottom" if portrait and compare_ghia else "right"
            figure.colorbar(self.images[name], ax=ax, location=location)
            ax.set(title=f"Velocity {name} [m/s]", xlabel="x [m]", ylabel="y [m]")
        if mosaic[0][:2] == ["u", "v"]:  # side by side: one y label is enough
            axes["v"].set_ylabel("")
        self.profile = None
        if compare_ghia:
            ax = axes["profile"]
            ax.plot(GHIA_U, GHIA_Y, "o", color="orange", label="Ghia et al. (1982)")
            (self.profile,) = ax.plot(
                simulation.u[:, len(simulation.y) // 2], simulation.y / CAVITY_SIZE,
                color="cyan", label="this solver",
            )  # fmt: skip
            ax.set(xlim=(-0.4, 1.05), ylim=(0, 1), xlabel="u / U at x = L/2")
            ax.set(ylabel="y / L", title="Vertical centreline")
            ax.grid(color="0.35")
            ax.legend(loc="lower right")

    def draw(self):
        for name, image in self.images.items():
            field = getattr(self.simulation, name)
            image.set_data(field)
            limit = max(np.abs(field).max(), EPSILON)
            image.set_clim(-limit, limit)
        if self.profile is not None:
            self.profile.set_xdata(
                centreline_u(self.simulation.u, self.simulation.y)[0]
            )

    def status(self):
        return f"Re = {REYNOLDS:g}   t = {self.simulation.time:.2f} s"


ANIMATION = Animation(
    title="Lid-Driven Cavity Flow",
    subtitle=f"Navier-Stokes at Re = {REYNOLDS:g}, projection method",
    filename="lid_driven_cavity.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of {TIME_STEP:g} s",
)


def main(argv=None) -> None:
    parser = ANIMATION.parser(__doc__)
    parser.add_argument(
        "--compare-ghia",
        action="store_true",
        help="add the centreline u profile against Ghia et al. (1982), Re = 100",
    )
    args = parser.parse_args(argv)

    simulation = CavitySimulation()
    ANIMATION.run(args, simulation, CavityView, compare_ghia=args.compare_ghia)
    if args.compare_ghia:
        error = simulation.ghia_error()
        print(
            f"t = {simulation.time:6.2f} s: centreline u vs Ghia et al. "
            f"max |error| = {np.abs(error).max():.4f}, "
            f"RMS = {np.sqrt(np.mean(error**2)):.4f}"
        )


if __name__ == "__main__":
    main()
