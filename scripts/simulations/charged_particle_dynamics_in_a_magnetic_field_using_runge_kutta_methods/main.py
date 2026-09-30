"""Animate the helical path of a charged particle in a uniform magnetic field.

The Lorentz-force equations of motion dr/dt = v, dv/dt = (q/m) v x B are
integrated with the classical fourth-order Runge-Kutta method (RK4). The
trajectory is revealed progressively in a 3D animation.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

Q = 1.0  # particle charge, C
M = 1.0  # particle mass, kg
B = np.array([0.0, 0.0, 1.0])  # magnetic field, T
R0 = np.array([0.0, 1.0, 0.0])  # initial position, m
V0 = np.array([1.0, 0.0, 1.0])  # initial velocity, m/s
DT = 0.01  # RK4 time step, s
NUM_FRAMES = 200  # animation frames in the default run
STEPS_PER_FRAME = 25  # RK4 steps per frame; 200 * 25 * 0.01 s = 50 s


def lorentz_force(t, y):
    """Return d/dt of the state y = (x, y, z, vx, vy, vz)."""
    v = y[3:]
    a = (Q / M) * np.cross(v, B)
    return np.hstack((v, a))


def rk4_step(func, t, y, dt):
    """Advance y by one classical fourth-order Runge-Kutta step."""
    k1 = func(t, y)
    k2 = func(t + dt / 2, y + dt / 2 * k1)
    k3 = func(t + dt / 2, y + dt / 2 * k2)
    k4 = func(t + dt, y + dt * k3)
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(num_steps, dt=DT):
    """Integrate from t = 0 for num_steps RK4 steps; return t, r, v arrays."""
    t_vals = np.arange(num_steps + 1) * dt
    r_vals = np.zeros((num_steps + 1, 3))
    v_vals = np.zeros((num_steps + 1, 3))
    y = np.hstack((R0, V0))
    r_vals[0], v_vals[0] = R0, V0
    for i in range(1, num_steps + 1):
        y = rk4_step(lorentz_force, t_vals[i - 1], y, dt)
        r_vals[i] = y[:3]
        v_vals[i] = y[3:]
    return t_vals, r_vals, v_vals


def report(t_vals, r_vals, v_vals):
    """Print the speed drift and the numerical vs analytical Larmor radius."""
    speed = np.linalg.norm(v_vals, axis=1)
    v_perp0 = np.linalg.norm(np.cross(V0, B / np.linalg.norm(B)))
    omega_c = abs(Q) * np.linalg.norm(B) / M
    r_larmor = v_perp0 / omega_c
    radius = np.linalg.norm(r_vals[:, :2], axis=1)  # guiding centre at origin
    print(
        f"t_final = {t_vals[-1]:.2f} s, cyclotron period = {2 * np.pi / omega_c:.3f} s"
    )
    print(
        f"Larmor radius: analytical {r_larmor:.6f} m, numerical {radius.mean():.6f} m"
    )
    print(f"max relative speed drift: {np.max(np.abs(speed / speed[0] - 1)):.2e}")


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=NUM_FRAMES,
        help=f"animation frames, each {STEPS_PER_FRAME} RK4 steps of dt = {DT} s "
        f"(default {NUM_FRAMES}, i.e. t = 50 s)",
    )
    args = parser.parse_args(argv)

    n_frames = args.steps
    t_vals, r_vals, v_vals = integrate(n_frames * STEPS_PER_FRAME)
    report(t_vals, r_vals, v_vals)

    fig = plt.figure(facecolor="black")
    ax = fig.add_subplot(111, projection="3d", facecolor="black")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, max(60.0, 1.05 * r_vals[:, 2].max()))
    ax.set_xlabel("X (meters)", color="white")
    ax.set_ylabel("Y (meters)", color="white")
    ax.set_zlabel("Z (meters)", color="white")
    ax.tick_params(colors="white")
    ax.set_title(
        "Helical Motion of a Charged Particle in a Magnetic Field", color="white"
    )

    (line,) = ax.plot([], [], [], "b-")
    (point,) = ax.plot([], [], [], "bo")  # the moving particle

    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
        return line, point

    def update(frame):
        idx = frame * STEPS_PER_FRAME
        line.set_data(r_vals[: idx + 1, 0], r_vals[: idx + 1, 1])
        line.set_3d_properties(r_vals[: idx + 1, 2])
        point.set_data([r_vals[idx, 0]], [r_vals[idx, 1]])
        point.set_3d_properties([r_vals[idx, 2]])
        return line, point

    if args.no_show:
        update(n_frames)
    else:
        ani = FuncAnimation(
            fig,
            update,
            frames=range(1, n_frames + 1),
            init_func=init,
            blit=True,
            interval=50,
            repeat=False,
        )
        plt.show()
        del ani

    if args.output:
        update(n_frames)
        save_figure(
            fig,
            args.output,
            "charged_particle_helix.png",
            facecolor=fig.get_facecolor(),
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
