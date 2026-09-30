"""Steady versus unsteady pathlines around a cylinder with circulation.

The steady flow is the potential flow past a circular cylinder (uniform stream,
doublet and point vortex). The unsteady flow adds a kinematic vortex-street
model: point vortices of alternating sign are released behind the cylinder at
the Strouhal frequency and convected downstream, with image vortices keeping
the cylinder impermeable. Particle pathlines are integrated with RK4 and drawn
over the streamlines: they coincide in the steady case and differ in the
unsteady one.
"""

import sys
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

# Flow parameters (dimensionless)
R = 1.0  # cylinder radius
U = 1.0  # free-stream velocity
GAMMA = 4 * np.pi * R * U  # cylinder circulation (counter-clockwise positive)
STROUHAL = 0.2  # St = f D / U
SHEDDING_PERIOD = 2 * R / (STROUHAL * U)  # one full cycle (two vortices)
VORTEX_STRENGTH = GAMMA / 2  # magnitude of each shed vortex
SHED_POSITION = (1.5 * R, 0.6 * R)  # release point (x, |y|) behind the cylinder
CONVECTION_SPEED = 0.8 * U  # downstream speed of the shed vortices
VORTEX_CORE = 0.3 * R  # core radius regularising the shed vortices
GROWTH_TIME = SHEDDING_PERIOD / 2  # shed vortices ramp up to full strength

# Numerical parameters
TIME_STEP = 0.05
N_STEPS = 300  # default number of time steps (one animation frame each)
NUM_PARTICLES = 20
SEED_X = -4.0  # particles start on a vertical line upstream of the cylinder
SEED_Y_RANGE = (-3.0, 3.0)
X_RANGE, Y_RANGE = (-5.0, 10.0), (-5.0, 5.0)
GRID_POINTS = (300, 200)  # (nx, ny) for the streamline plots


def base_velocity(x, y):
    """Potential flow past a cylinder with circulation; NaN inside the cylinder.

    Complex velocity u - i v = U (1 - R^2 / z^2) - i GAMMA / (2 pi z).
    """
    z = np.asarray(x) + 1j * np.asarray(y)
    with np.errstate(divide="ignore", invalid="ignore"):
        w = U * (1 - R**2 / z**2) - 1j * GAMMA / (2 * np.pi * z)
    inside = np.abs(z) < R
    return np.where(inside, np.nan, w.real), np.where(inside, np.nan, -w.imag)


def shed_vortices(t):
    """Positions and strengths of the vortices released up to time t."""
    half_period = SHEDDING_PERIOD / 2
    vortices = []
    for k in range(int(np.floor(t / half_period)) + 1):
        age = t - k * half_period
        x_v = SHED_POSITION[0] + CONVECTION_SPEED * age
        if x_v > X_RANGE[1] + 5:
            continue  # far downstream: negligible influence
        upper = k % 2 == 0
        y_v = SHED_POSITION[1] if upper else -SHED_POSITION[1]
        sign = (
            -1.0 if upper else 1.0
        )  # upper row clockwise, lower row counter-clockwise
        strength = sign * VORTEX_STRENGTH * min(1.0, age / GROWTH_TIME)
        vortices.append((complex(x_v, y_v), strength))
    return vortices


def vortex_velocity(x, y, vortices):
    """Velocity induced by shed vortices plus their images in the cylinder.

    For a vortex of strength g at z_v the circle theorem adds -g at R^2 / conj(z_v)
    and +g at the centre. Only the shed vortex itself has a regularised core.
    """
    z = np.asarray(x) + 1j * np.asarray(y)
    w = np.zeros_like(z)
    for z_v, g in vortices:
        for z_k, g_k, core in (
            (z_v, g, VORTEX_CORE),
            (R**2 / np.conj(z_v), -g, 0.0),
            (0.0, g, 0.0),
        ):
            dz = z - z_k
            with np.errstate(divide="ignore", invalid="ignore"):
                w += -1j * g_k / (2 * np.pi) * np.conj(dz) / (np.abs(dz) ** 2 + core**2)
    return w.real, -w.imag


def steady_velocity(x, y, t=0.0):
    return base_velocity(x, y)


def unsteady_velocity(x, y, t):
    u0, v0 = base_velocity(x, y)
    u1, v1 = vortex_velocity(x, y, shed_vortices(t))
    return u0 + u1, v0 + v1


def rk4_step(velocity, pos, t, dt):
    """Classical RK4 for all particles at once; pos has shape (n, 2)."""

    def f(p, time):
        return np.stack(velocity(p[:, 0], p[:, 1], time), axis=1)

    k1 = f(pos, t)
    k2 = f(pos + 0.5 * dt * k1, t + 0.5 * dt)
    k3 = f(pos + 0.5 * dt * k2, t + 0.5 * dt)
    k4 = f(pos + dt * k3, t + dt)
    return pos + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def compute_pathlines(velocity, particles, dt, nt):
    """Return positions with shape (nt + 1, n, 2); particles hitting the cylinder become NaN."""
    paths = np.empty((nt + 1, *particles.shape))
    paths[0] = particles
    for step in range(nt):
        new = rk4_step(velocity, paths[step], step * dt, dt)
        new[np.hypot(new[:, 0], new[:, 1]) < R] = np.nan
        paths[step + 1] = new
    return paths


def draw_panel(ax, title, X, Y, Ux, Uy, color):
    ax.set_title(title, color="white")
    ax.set_xlim(*X_RANGE)
    ax.set_ylim(*Y_RANGE)
    ax.set_aspect("equal")
    ax.add_patch(Circle((0, 0), R, color="white", zorder=5))
    ax.streamplot(
        X,
        Y,
        Ux,
        Uy,
        color=color,
        linewidth=1.5,
        density=1.5,
        arrowstyle="->",
        arrowsize=1.5,
    )


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=N_STEPS,
        help=f"time steps of {TIME_STEP} (one frame each) (default: {N_STEPS})",
    )
    args = parser.parse_args(argv)
    nt = args.steps

    plt.style.use("dark_background")
    x = np.linspace(*X_RANGE, GRID_POINTS[0])
    y = np.linspace(*Y_RANGE, GRID_POINTS[1])
    X, Y = np.meshgrid(x, y)

    particles = np.column_stack(
        [np.full(NUM_PARTICLES, SEED_X), np.linspace(*SEED_Y_RANGE, NUM_PARTICLES)]
    )
    paths_steady = compute_pathlines(steady_velocity, particles, TIME_STEP, nt)
    paths_unsteady = compute_pathlines(unsteady_velocity, particles, TIME_STEP, nt)

    fig, (ax_steady, ax_unsteady) = plt.subplots(1, 2, figsize=(12, 4.8))
    steady_title = "Steady Flow\nStreamlines and Pathlines coincide"
    unsteady_title = (
        "Unsteady Flow with Vortex Shedding\nStreamlines and Pathlines differ"
    )
    draw_panel(ax_steady, steady_title, X, Y, *steady_velocity(X, Y), "cyan")
    lines_steady = [
        ax_steady.plot([], [], linewidth=1.5, color="lime")[0]
        for _ in range(NUM_PARTICLES)
    ]
    points_steady = ax_steady.plot([], [], "o", markersize=6, color="yellow", zorder=6)[
        0
    ]

    def update(frame):
        k = frame + 1  # number of completed time steps shown
        t = k * TIME_STEP
        for i, line in enumerate(lines_steady):
            line.set_data(paths_steady[: k + 1, i, 0], paths_steady[: k + 1, i, 1])
        points_steady.set_data(paths_steady[k, :, 0], paths_steady[k, :, 1])

        ax_unsteady.clear()
        draw_panel(
            ax_unsteady, f"{unsteady_title} (t = {t:.2f})", X, Y,
            *unsteady_velocity(X, Y, t), "magenta",
        )  # fmt: skip
        for i in range(NUM_PARTICLES):
            ax_unsteady.plot(
                paths_unsteady[: k + 1, i, 0], paths_unsteady[: k + 1, i, 1],
                linewidth=1.5, color="orange",
            )  # fmt: skip
        ax_unsteady.plot(
            paths_unsteady[k, :, 0], paths_unsteady[k, :, 1], "o",
            markersize=6, color="red", zorder=6,
        )  # fmt: skip
        vortices = shed_vortices(t)
        ax_unsteady.plot(
            [z.real for z, _ in vortices], [z.imag for z, _ in vortices], "o",
            markersize=9, markerfacecolor="none", markeredgecolor="white", zorder=6,
        )  # fmt: skip
        return ()

    if args.no_show:
        for frame in range(nt):
            update(frame)
    else:
        ani = animation.FuncAnimation(  # noqa: F841 (keep a reference while showing)
            fig, update, frames=nt, init_func=lambda: (), interval=50, repeat=False
        )
    plt.tight_layout()
    if not args.no_show:
        plt.show()

    if args.output:
        save_figure(fig, args.output, "steady_and_unsteady_pathlines.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
