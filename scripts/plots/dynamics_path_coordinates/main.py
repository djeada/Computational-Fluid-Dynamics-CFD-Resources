"""Path, polar and rotating-frame descriptions of the acceleration of a particle.

Three motions are drawn with their acceleration resolved in the coordinate
system that suits them. A projectile (30 m/s at 50 degrees, no drag) shows the
normal-tangential components of gravity and the osculating circle of radius
rho = v^2 / a_n. A bead on a frictionless rod rotating at 3 rad/s
(r = r0 cosh(w t)) shows the radial and transverse unit vectors; its radial
acceleration r'' - r theta'^2 is zero and the whole acceleration is the
transverse Coriolis term 2 r' theta'. A puck sliding in a straight line over a
turntable is seen from the rotating frame, where its curved path is explained
by the Coriolis and centrifugal accelerations.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # g (m/s^2)
LAUNCH_SPEED = 30.0  # v0 (m/s)
LAUNCH_ANGLE = np.radians(50.0)  # theta0 (rad)
ROD_RATE = 3.0  # constant rod angular velocity theta' (rad/s)
BEAD_START = 0.1  # r0 (m)
BEAD_DURATION = 0.75  # length of the bead path (s)
TABLE_RATE = 0.6  # turntable angular velocity Omega (rad/s), counterclockwise
PUCK_START = np.array([-1.0, -0.3])  # inertial start of the puck (m)
PUCK_VELOCITY = np.array([0.8, 0.0])  # constant inertial puck velocity (m/s)
PUCK_DURATION = 2.5  # (s)


def projectile_state(t, v0=LAUNCH_SPEED, angle=LAUNCH_ANGLE, g=GRAVITY):
    """Position, velocity and acceleration (each shape (2, n)) of a drag-free projectile."""
    t = np.atleast_1d(np.asarray(t, dtype=float))
    vx, vy = v0 * np.cos(angle), v0 * np.sin(angle)
    r = np.array([vx * t, vy * t - 0.5 * g * t**2])
    v = np.array([np.full_like(t, vx), vy - g * t])
    a = np.array([np.zeros_like(t), np.full_like(t, -g)])
    return r, v, a


def normal_tangential(v, a):
    """Speed, tangential and normal acceleration, unit vectors and radius of curvature."""
    speed = np.hypot(v[0], v[1])
    e_t = v / speed
    a_t = np.sum(a * e_t, axis=0)
    a_n_vec = a - a_t * e_t
    a_n = np.hypot(a_n_vec[0], a_n_vec[1])
    e_n = a_n_vec / a_n
    return speed, a_t, a_n, e_t, e_n, speed**2 / a_n


def bead_state(t, r0=BEAD_START, w=ROD_RATE):
    """Polar coordinates and their rates of the bead on a frictionless rotating rod."""
    t = np.asarray(t, dtype=float)
    r = r0 * np.cosh(w * t)
    r_dot = r0 * w * np.sinh(w * t)
    r_ddot = r0 * w**2 * np.cosh(w * t)
    theta = w * t
    return r, r_dot, r_ddot, theta, np.full_like(t, w), np.zeros_like(t)


def polar_acceleration(r, r_dot, r_ddot, theta_dot, theta_ddot):
    """Radial and transverse acceleration components a_r, a_theta."""
    return r_ddot - r * theta_dot**2, r * theta_ddot + 2.0 * r_dot * theta_dot


def puck_in_rotating_frame(t, start=PUCK_START, velocity=PUCK_VELOCITY, w=TABLE_RATE):
    """Position (2, n) of a puck moving uniformly in the inertial frame, seen from a
    frame that rotates counterclockwise at w about the origin."""
    t = np.asarray(t, dtype=float)
    inertial = start[:, None] + velocity[:, None] * t
    c, s = np.cos(w * t), np.sin(w * t)
    return np.array(
        [c * inertial[0] + s * inertial[1], -s * inertial[0] + c * inertial[1]]
    )


def rotating_frame_accelerations(r_rel, v_rel, w=TABLE_RATE):
    """Coriolis -2 Omega x v_rel and centrifugal -Omega x (Omega x r_rel) in the plane."""
    coriolis = -2.0 * w * np.array([-v_rel[1], v_rel[0]])
    centrifugal = w**2 * r_rel
    return coriolis, centrifugal


def rotating_frame_check(n=4001):
    """Max difference between the finite-difference relative acceleration and the
    sum of the Coriolis and centrifugal terms (the inertial acceleration is zero)."""
    t = np.linspace(0.0, PUCK_DURATION, n)
    r = puck_in_rotating_frame(t)
    dt = t[1] - t[0]
    v = np.gradient(r, dt, axis=1)
    a = np.gradient(v, dt, axis=1)
    coriolis, centrifugal = rotating_frame_accelerations(r, v)
    interior = slice(5, -5)
    return np.max(np.abs(a[:, interior] - (coriolis + centrifugal)[:, interior]))


def arrow(ax, origin, vector, color, label=None, width=0.006):
    ax.quiver(
        origin[0],
        origin[1],
        vector[0],
        vector[1],
        angles="xy",
        scale_units="xy",
        scale=1.0,
        color=color,
        width=width,
        label=label,
        zorder=3,
    )


def make_figure():
    """Draw the three panels."""
    colors = plt.get_cmap("tab10").colors
    fig, (ax_nt, ax_polar, ax_rot) = plt.subplots(1, 3, figsize=(13.5, 5.2))

    # (a) projectile in normal-tangential components.
    t_flight = 2.0 * LAUNCH_SPEED * np.sin(LAUNCH_ANGLE) / GRAVITY
    t = np.linspace(0.0, t_flight, 400)
    r, _, _ = projectile_state(t)
    ax_nt.plot(r[0], r[1], color="0.3", linewidth=1.5)
    marks = np.array([0.12, 0.35, 0.5, 0.75]) * t_flight
    r_m, v_m, a_m = projectile_state(marks)
    speed, a_t, a_n, e_t, e_n, rho = normal_tangential(v_m, a_m)
    scale_v, scale_a = 0.45, 1.2  # drawing scales (m per m/s, m per m/s^2)
    for k in range(len(marks)):
        first = k == 0
        arrow(
            ax_nt, r_m[:, k], scale_v * v_m[:, k], colors[0], "$v$" if first else None
        )
        arrow(
            ax_nt,
            r_m[:, k],
            scale_a * a_t[k] * e_t[:, k],
            colors[1],
            "$a_t$" if first else None,
        )
        arrow(
            ax_nt,
            r_m[:, k],
            scale_a * a_n[k] * e_n[:, k],
            colors[2],
            "$a_n$" if first else None,
        )
    k = 0
    centre = r_m[:, k] + rho[k] * e_n[:, k]
    phi = np.linspace(0.0, 2.0 * np.pi, 300)
    ax_nt.plot(
        centre[0] + rho[k] * np.cos(phi),
        centre[1] + rho[k] * np.sin(phi),
        color=colors[2],
        linestyle=":",
        linewidth=1.0,
        label=rf"osculating circle, $\rho$ = {rho[k]:.0f} m",
    )
    ax_nt.set(
        xlim=(-5.0, 95.0),
        ylim=(-10.0, 45.0),
        aspect="equal",
        xlabel="$x$ (m)",
        ylabel="$y$ (m)",
        title="(a) Projectile: $a_t = \\dot{v}$, $a_n = v^2/\\rho$",
    )
    ax_nt.legend(fontsize=9, loc="lower center", ncol=2)

    # (b) bead on a rotating rod in polar components.
    t = np.linspace(0.0, BEAD_DURATION, 300)
    r, r_dot, r_ddot, theta, theta_dot, theta_ddot = bead_state(t)
    ax_polar.plot(r * np.cos(theta), r * np.sin(theta), color="0.3", linewidth=1.5)
    ax_polar.plot(0.0, 0.0, "k+", ms=10)
    marks = np.array([0.25, 0.45, 0.6, 0.72])
    r, r_dot, r_ddot, theta, theta_dot, theta_ddot = bead_state(marks)
    a_r, a_theta = polar_acceleration(r, r_dot, r_ddot, theta_dot, theta_ddot)
    for k in range(len(marks)):
        p = r[k] * np.array([np.cos(theta[k]), np.sin(theta[k])])
        e_r = np.array([np.cos(theta[k]), np.sin(theta[k])])
        e_th = np.array([-np.sin(theta[k]), np.cos(theta[k])])
        ax_polar.plot([0.0, p[0]], [0.0, p[1]], color="0.75", linewidth=1.0)
        first = k == 0
        acc = a_r[k] * e_r + a_theta[k] * e_th
        arrow(ax_polar, p, 0.012 * acc, colors[3], r"$a$" if first else None, 0.014)
        arrow(ax_polar, p, 0.07 * e_r, colors[0], r"$e_r$" if first else None)
        arrow(ax_polar, p, 0.07 * e_th, colors[1], r"$e_\theta$" if first else None)
    ax_polar.set(
        xlim=(-0.35, 0.35),
        ylim=(-0.05, 0.62),
        aspect="equal",
        xlabel="$x$ (m)",
        ylabel="$y$ (m)",
        title=r"(b) Bead on rod: $a_r = 0$, $a_\theta = 2\dot{r}\dot{\theta}$",
    )
    ax_polar.legend(fontsize=9, loc="upper left")

    # (c) puck seen from the rotating turntable.
    t = np.linspace(0.0, PUCK_DURATION, 400)
    r_rel = puck_in_rotating_frame(t)
    inertial = PUCK_START[:, None] + PUCK_VELOCITY[:, None] * t
    ax_rot.add_patch(plt.Circle((0, 0), 1.2, color="0.93", zorder=0))
    ax_rot.plot(*inertial, color="0.6", linestyle="--", label="path, inertial frame")
    ax_rot.plot(*r_rel, color="0.2", linewidth=1.5, label="path, rotating frame")
    marks = np.linspace(0.4, 2.2, 4)
    r_m = puck_in_rotating_frame(marks)
    h = 1e-5
    v_m = (puck_in_rotating_frame(marks + h) - puck_in_rotating_frame(marks - h)) / (
        2 * h
    )
    coriolis, centrifugal = rotating_frame_accelerations(r_m, v_m)
    for k in range(len(marks)):
        first = k == 0
        arrow(
            ax_rot,
            r_m[:, k],
            0.4 * coriolis[:, k],
            colors[4],
            r"Coriolis $-2\Omega \times v_{rel}$" if first else None,
        )
        arrow(
            ax_rot,
            r_m[:, k],
            0.4 * centrifugal[:, k],
            colors[5],
            r"centrifugal $\Omega^2 r$" if first else None,
        )
    ax_rot.set(
        xlim=(-1.3, 1.3),
        ylim=(-1.3, 1.3),
        aspect="equal",
        xlabel="$x'$ (m)",
        ylabel="$y'$ (m)",
        title=rf"(c) Turntable frame, $\Omega$ = {TABLE_RATE:g} rad/s",
    )
    ax_rot.annotate(
        "",
        xy=(0.85, 0.85),
        xytext=(1.15, 0.3),
        arrowprops={
            "arrowstyle": "->",
            "connectionstyle": "arc3,rad=0.3",
            "color": "0.4",
        },
    )
    ax_rot.text(0.95, 1.0, r"$\Omega$", fontsize=11, color="0.3")
    ax_rot.legend(fontsize=9, loc="upper left")
    for ax in (ax_nt, ax_polar, ax_rot):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t_flight = 2.0 * LAUNCH_SPEED * np.sin(LAUNCH_ANGLE) / GRAVITY
    _, v, a = projectile_state([0.0, 0.5 * t_flight])
    _, _, a_n, _, _, rho = normal_tangential(v, a)
    print(f"projectile: rho at launch = {rho[0]:.1f} m, at apex = {rho[1]:.1f} m")
    r, r_dot, r_ddot, _, w, alpha = bead_state(np.array([0.5]))
    a_r, a_theta = polar_acceleration(r, r_dot, r_ddot, w, alpha)
    print(
        f"bead at t = 0.5 s: r = {r[0]:.4f} m, a_r = {a_r[0]:.2e}, a_theta = {a_theta[0]:.4f} m/s^2"
    )
    print(
        f"rotating frame: max |a_rel - (Coriolis + centrifugal)| = {rotating_frame_check():.2e} m/s^2"
    )

    finish_figures(
        {"dynamics_path_coordinates.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
