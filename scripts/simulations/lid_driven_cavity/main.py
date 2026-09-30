"""Lid-driven cavity flow at Re = 100 with an explicit projection method.

The 2D incompressible Navier-Stokes equations are advanced with forward Euler
and second-order central differences on a collocated 129 x 129 grid; a Jacobi
pressure Poisson solve projects the velocity at every step. Contours of u and v
are animated, and ``--compare-ghia`` adds the vertical-centreline u profile
against the Re = 100 benchmark of Ghia, Ghia & Shin (1982).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from numpy import ndarray

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

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
EPSILON: float = 1e-6  # avoids a zero range for the contour levels

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


class CavitySimulation:
    """Projection-solver state independent of animation and benchmark plotting."""

    def __init__(self, n_points=N_POINTS):
        if n_points < 3:
            raise ValueError("at least three points per axis are required")
        self.y = np.linspace(0.0, CAVITY_SIZE, n_points)
        self.X, self.Y = np.meshgrid(self.y, self.y)
        self.element_length = CAVITY_SIZE / (n_points - 1)
        self.u = np.zeros((n_points, n_points))
        self.v = np.zeros_like(self.u)
        self.p = np.zeros_like(self.u)
        apply_boundary_conditions(self.u, self.v, LID_VELOCITY)
        self.steps = 0

    @property
    def time(self):
        return self.steps * TIME_STEP

    def advance(self, steps=1):
        """Advance exactly steps projection iterations without drawing contours."""
        if steps < 0:
            raise ValueError("steps must be nonnegative")
        for _ in range(steps):
            self.u, self.v, self.p = time_step(
                self.u, self.v, self.p, self.element_length
            )
            self.steps += 1


def style_axes(ax) -> None:
    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    for spine in ax.spines.values():
        spine.set_color("white")


def draw_contour(fig, ax, X, Y, field, title):
    ax.set_title(title, color="white")
    contour = ax.contourf(
        X,
        Y,
        field,
        cmap="coolwarm",
        levels=np.linspace(np.min(field), np.max(field) + EPSILON, 20),
    )
    colorbar = fig.colorbar(contour, ax=ax)
    colorbar.ax.yaxis.set_tick_params(color="white")
    colorbar.outline.set_edgecolor("white")
    plt.setp(plt.getp(colorbar.ax.axes, "yticklabels"), color="white")
    return contour, colorbar


def main(argv=None) -> None:
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=N_FRAMES,
        help=f"animation frames, each {STEPS_PER_FRAME} time steps "
        f"of {TIME_STEP:g} s (default: {N_FRAMES})",
    )
    parser.add_argument(
        "--compare-ghia",
        action="store_true",
        help="add the centreline u profile against Ghia et al. (1982), Re = 100",
    )
    args = parser.parse_args(argv)

    reynolds = LID_VELOCITY * CAVITY_SIZE / KINEMATIC_VISCOSITY
    simulation = CavitySimulation()
    X, Y, y = simulation.X, simulation.Y, simulation.y

    n_panels = 3 if args.compare_ghia else 2
    fig, axs = plt.subplots(1, n_panels, figsize=(6 * n_panels, 6), facecolor="black")
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    ax_u, ax_v = axs[0], axs[1]
    for ax in (ax_u, ax_v):
        ax.set_xlim(0, CAVITY_SIZE)
        ax.set_ylim(0, CAVITY_SIZE)
        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
    for ax in axs:
        style_axes(ax)

    artists = {}
    artists["u"] = draw_contour(fig, ax_u, X, Y, simulation.u, "Velocity u [m/s]")
    artists["v"] = draw_contour(fig, ax_v, X, Y, simulation.v, "Velocity v [m/s]")
    iteration_text = fig.suptitle(f"Re = {reynolds:g}, t = 0.00 s", color="white")

    if args.compare_ghia:
        ax_c = axs[2]
        ax_c.plot(GHIA_U, GHIA_Y, "o", color="orange", label="Ghia et al. (1982)")
        (profile_line,) = ax_c.plot(
            simulation.u[:, len(y) // 2],
            y / CAVITY_SIZE,
            color="cyan",
            label="this solver",
        )
        ax_c.set_xlim(-0.4, 1.05)
        ax_c.set_ylim(0, 1)
        ax_c.set_xlabel("u / U at x = L/2")
        ax_c.set_ylabel("y / L")
        ax_c.set_title(f"Vertical centreline (Re = {reynolds:g})", color="white")
        ax_c.grid(color="0.35")
        ax_c.legend(facecolor="black", labelcolor="white", edgecolor="white")

    def redraw(frame: int):
        t = simulation.time
        for key in ("u", "v"):
            contour, colorbar = artists[key]
            colorbar.remove()  # before the contour set it belongs to
            contour.remove()
        artists["u"] = draw_contour(fig, ax_u, X, Y, simulation.u, "Velocity u [m/s]")
        artists["v"] = draw_contour(fig, ax_v, X, Y, simulation.v, "Velocity v [m/s]")
        iteration_text.set_text(
            f"Re = {reynolds:g}, t = {t:.2f} s (frame {frame + 1}/{args.steps})"
        )

        if args.compare_ghia:
            profile, at_ghia = centreline_u(simulation.u, y)
            profile_line.set_xdata(profile)
            error = at_ghia - GHIA_U
            print(
                f"t = {t:6.2f} s: centreline u vs Ghia et al. "
                f"max |error| = {np.abs(error).max():.4f}, "
                f"RMS = {np.sqrt(np.mean(error**2)):.4f}"
            )
        return ()

    def update(frame: int):
        simulation.advance(STEPS_PER_FRAME)
        return redraw(frame)

    if args.no_show:
        simulation.advance(args.steps * STEPS_PER_FRAME)
        redraw(args.steps - 1)
    else:
        animation = FuncAnimation(  # noqa: F841 (keep a reference while showing)
            fig, update, frames=args.steps, init_func=lambda: (), repeat=False
        )
        plt.show()

    if args.output:
        save_figure(
            fig, args.output, "lid_driven_cavity.png", facecolor=fig.get_facecolor()
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
