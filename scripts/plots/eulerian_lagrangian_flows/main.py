"""Contrast Eulerian and Lagrangian descriptions of the time-dependent Double Gyre.

The left panel is an Eulerian snapshot: the velocity field at t = 0 sampled on a
fixed grid. The right panel is Lagrangian: the paths of 20 particles, released at
random (seeded) positions and advected with a fourth-order Runge-Kutta scheme.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures, positive_int  # noqa: E402

DT = 0.01  # time step (non-dimensional time units)
NUM_STEPS = 500  # default number of RK4 steps
NUM_PARTICLES = 20
SEED = 42


def double_gyre_velocity(x, y, t, A=0.25, epsilon=0.25, omega=2 * np.pi):
    """
    Compute the velocity field (u,v) of the time-dependent Double Gyre at time t.

    Parameters
    ----------
    x, y : array_like
        Positions where velocity is evaluated.
    t : float
        Current time.
    A : float
        Amplitude of the velocity field.
    epsilon : float
        Strength of the horizontal oscillation.
    omega : float
        Oscillation frequency.

    Returns
    -------
    u, v : ndarray
        The velocity components at each input point.
    """
    # f(x, t)
    f = epsilon * np.sin(omega * t) * x**2 + (1 - 2 * epsilon * np.sin(omega * t)) * x

    # df/dx
    dfdx = 2 * epsilon * np.sin(omega * t) * x + (1 - 2 * epsilon * np.sin(omega * t))

    # Velocity field, from the stream function psi = A sin(pi f) sin(pi y)
    u = -np.pi * A * np.sin(np.pi * f) * np.cos(np.pi * y)
    v = np.pi * A * np.cos(np.pi * f) * np.sin(np.pi * y) * dfdx

    return u, v


def rk4_step(x, y, t, dt, velocity_func):
    """
    Perform one time-step of 4th-order Runge-Kutta integration for 2D particle positions.

    Parameters
    ----------
    x, y : ndarray
        Current particle positions (arrays of the same shape).
    t : float
        Current time.
    dt : float
        Time step.
    velocity_func : callable
        Function that returns (u, v) given (x, y, t).

    Returns
    -------
    x_next, y_next : ndarray
        Particle positions at time t + dt
    """
    # k1
    u1, v1 = velocity_func(x, y, t)
    k1x = dt * u1
    k1y = dt * v1

    # k2
    u2, v2 = velocity_func(x + 0.5 * k1x, y + 0.5 * k1y, t + 0.5 * dt)
    k2x = dt * u2
    k2y = dt * v2

    # k3
    u3, v3 = velocity_func(x + 0.5 * k2x, y + 0.5 * k2y, t + 0.5 * dt)
    k3x = dt * u3
    k3y = dt * v3

    # k4
    u4, v4 = velocity_func(x + k3x, y + k3y, t + dt)
    k4x = dt * u4
    k4y = dt * v4

    x_next = x + (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0
    y_next = y + (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0

    return x_next, y_next


def compute_eulerian_field(nx=20, ny=10, t=0.0):
    """
    Compute the Eulerian velocity field on a 2D grid at time t.
    """
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)
    U, V = double_gyre_velocity(X, Y, t)
    return X, Y, U, V


def compute_lagrangian_trajectories(
    num_particles=NUM_PARTICLES, num_steps=NUM_STEPS, dt=DT, seed=SEED
):
    """
    Compute Lagrangian trajectories using 4th-order Runge-Kutta in the Double Gyre.

    Returns an array of shape (num_particles, num_steps + 1, 2).
    """
    # Random (seeded) initial positions in the domain [0,2]x[0,1]
    rng = np.random.default_rng(seed=seed)
    x0 = 2.0 * rng.random(num_particles)
    y0 = 1.0 * rng.random(num_particles)

    trajectories = np.zeros((num_particles, num_steps + 1, 2))
    trajectories[:, 0, 0] = x0
    trajectories[:, 0, 1] = y0

    # Time integration
    t = 0.0
    for n in range(num_steps):
        x_current = trajectories[:, n, 0]
        y_current = trajectories[:, n, 1]

        x_next, y_next = rk4_step(
            x_current, y_current, t, dt, velocity_func=double_gyre_velocity
        )

        trajectories[:, n + 1, 0] = x_next
        trajectories[:, n + 1, 1] = y_next
        t += dt

    return trajectories


def make_figure(num_steps=NUM_STEPS, dt=DT):
    """Build the side-by-side Eulerian / Lagrangian figure."""
    # --- Eulerian field at t=0 ---
    X, Y, U, V = compute_eulerian_field(nx=20, ny=15, t=0.0)

    # --- Lagrangian trajectories ---
    trajectories = compute_lagrangian_trajectories(num_steps=num_steps, dt=dt)

    fig, (ax_euler, ax_lagrange) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot Eulerian velocity field (snapshot at t=0)
    ax_euler.quiver(X, Y, U, V, alpha=0.7)
    ax_euler.set_title("Eulerian View at t=0\n(Double Gyre Snapshot)")
    ax_euler.set_xlabel("X")
    ax_euler.set_ylabel("Y")
    ax_euler.set_aspect("equal")
    ax_euler.grid(True)

    # Plot Lagrangian trajectories
    for i in range(trajectories.shape[0]):
        ax_lagrange.plot(trajectories[i, :, 0], trajectories[i, :, 1])
        # Mark initial position
        ax_lagrange.plot(
            trajectories[i, 0, 0], trajectories[i, 0, 1], "ko", markersize=3
        )
    ax_lagrange.set_title(
        f"Lagrangian View\n(Double Gyre Trajectories, 0 ≤ t ≤ {num_steps * dt:g})"
    )
    ax_lagrange.set_xlabel("X")
    ax_lagrange.set_ylabel("Y")
    ax_lagrange.set_xlim(0, 2)
    ax_lagrange.set_ylim(0, 1)
    ax_lagrange.set_aspect("equal")
    ax_lagrange.grid(True)

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=NUM_STEPS,
        metavar="N",
        help=f"number of RK4 time steps (default {NUM_STEPS})",
    )
    args = parser.parse_args(argv)

    fig = make_figure(num_steps=args.steps)

    finish_figures(
        {"eulerian_lagrangian_flows.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
