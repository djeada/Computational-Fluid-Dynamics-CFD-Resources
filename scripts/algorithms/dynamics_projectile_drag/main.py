"""Projectile with quadratic air drag: trajectories, optimum angle and energy budget.

Newton's second law m a = m g + D with the drag force D = -1/2 rho C_d A |v| v
is integrated with scipy's RK45 for a baseball-sized ball (0.145 kg, 73 mm,
C_d = 0.35) launched at 40 m/s, about its terminal speed. The trajectories are
compared with the drag-free parabola, the range is computed as a function of
launch angle to find the optimum below 45 degrees, and the work done by drag
is integrated alongside the motion to check the work-energy balance
T + V + W_drag = T0 + V0 along the path.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # g (m/s^2)
AIR_DENSITY = 1.2  # rho (kg/m^3)
MASS = 0.145  # m (kg)
DIAMETER = 0.073  # d (m)
DRAG_COEFFICIENT = 0.35  # C_d, roughly constant for a ball in the subcritical regime
LAUNCH_SPEED = 40.0  # v0 (m/s)
ANGLES_DEG = (30.0, 45.0, 60.0)  # launch angles of the trajectory panel
ENERGY_ANGLE_DEG = 45.0  # launch angle of the energy-budget panel
RTOL, ATOL = 1e-9, 1e-11  # RK45 tolerances


def drag_constant(rho=AIR_DENSITY, cd=DRAG_COEFFICIENT, d=DIAMETER, m=MASS):
    """k = rho C_d A / (2 m) (1/m), so the drag deceleration is k |v| v."""
    return rho * cd * np.pi * d**2 / 4.0 / (2.0 * m)


def terminal_speed(k=None, g=GRAVITY):
    """Speed at which drag balances weight, sqrt(g / k) (m/s)."""
    k = drag_constant() if k is None else k
    return np.sqrt(g / k)


def rhs(_t, state, k, g=GRAVITY):
    """State (x, y, vx, vy, w) where w is the work done against drag per unit mass."""
    _, _, vx, vy, _ = state
    speed = np.hypot(vx, vy)
    return [vx, vy, -k * speed * vx, -g - k * speed * vy, k * speed**3]


def fly(angle_deg, k=None, v0=LAUNCH_SPEED, max_points=400):
    """Integrate from launch at the origin to impact on y = 0.

    Returns the times, the states (5, n) ending exactly at impact, and the
    impact time.
    """
    k = drag_constant() if k is None else k
    theta = np.radians(angle_deg)
    state0 = [0.0, 0.0, v0 * np.cos(theta), v0 * np.sin(theta), 0.0]

    def ground(_t, s, _k):
        return s[1]

    ground.terminal = True
    ground.direction = -1
    t_max = 2.0 * v0 / GRAVITY + 1.0  # longer than the drag-free flight time
    sol = solve_ivp(
        rhs,
        (0.0, t_max),
        state0,
        args=(k,),
        events=ground,
        rtol=RTOL,
        atol=ATOL,
        dense_output=True,
    )
    t_end = sol.t_events[0][0]
    t = np.linspace(0.0, t_end, max_points)
    return t, sol.sol(t), t_end


def flight_range(angle_deg, k=None):
    """Horizontal distance to the impact point (m)."""
    _, states, _ = fly(angle_deg, k, max_points=2)
    return states[0, -1]


def vacuum_range(angle_deg, v0=LAUNCH_SPEED, g=GRAVITY):
    """Closed-form range on level ground without drag (m)."""
    return v0**2 * np.sin(2.0 * np.radians(angle_deg)) / g


def optimum_angle(k=None):
    """Launch angle (deg) that maximizes the range with drag."""
    result = minimize_scalar(
        lambda a: -flight_range(a, k),
        bounds=(20.0, 50.0),
        method="bounded",
        options={"xatol": 1e-4},
    )
    return result.x, -result.fun


def fall_speed(t, k=None, g=GRAVITY):
    """Closed-form speed of a body dropped from rest with quadratic drag."""
    vt = terminal_speed(k, g)
    return vt * np.tanh(g * np.asarray(t) / vt)


def energy_budget(states, m=MASS, g=GRAVITY):
    """Kinetic, potential and drag-work histories (J) from the states."""
    kinetic = 0.5 * m * (states[2] ** 2 + states[3] ** 2)
    potential = m * g * states[1]
    return kinetic, potential, m * states[4]


def make_figure():
    """Draw trajectories, range against angle and the energy budget."""
    colors = plt.get_cmap("tab10").colors
    fig, (ax_path, ax_range, ax_energy) = plt.subplots(1, 3, figsize=(13.5, 4.8))

    for i, angle in enumerate(ANGLES_DEG):
        _, s, _ = fly(angle)
        _, s0, _ = fly(angle, k=0.0)
        ax_path.plot(s[0], s[1], color=colors[i], label=f"{angle:g}°, drag")
        ax_path.plot(s0[0], s0[1], color=colors[i], linestyle="--", linewidth=1.0)
    ax_path.plot([], [], "k--", linewidth=1.0, label="no drag")
    ax_path.set(
        xlabel="$x$ (m)",
        ylabel="$y$ (m)",
        title=f"(a) Trajectories, $v_0$ = {LAUNCH_SPEED:g} m/s",
        xlim=(0.0, 170.0),
        ylim=(0.0, 65.0),
    )
    ax_path.legend(fontsize=9, loc="upper right")

    angles = np.linspace(5.0, 85.0, 33)
    ranges = [flight_range(a) for a in angles]
    best_angle, best_range = optimum_angle()
    ax_range.plot(angles, ranges, color=colors[3], label="with drag")
    ax_range.plot(
        angles, vacuum_range(angles), color="0.4", linestyle="--", label="no drag"
    )
    ax_range.plot(best_angle, best_range, "o", color=colors[3])
    ax_range.annotate(
        f"optimum {best_angle:.1f}°, {best_range:.1f} m",
        xy=(best_angle, best_range),
        xytext=(27.0, 40.0),
        fontsize=10,
        arrowprops={"arrowstyle": "->"},
    )
    ax_range.set(
        xlabel="launch angle (deg)",
        ylabel="range (m)",
        title="(b) Range on level ground",
        xlim=(0.0, 90.0),
        ylim=(0.0, 175.0),
    )
    ax_range.legend(fontsize=9, loc="upper right")

    t, s, _ = fly(ENERGY_ANGLE_DEG)
    kinetic, potential, work = energy_budget(s)
    ax_energy.plot(t, kinetic, color=colors[0], label="kinetic $T$")
    ax_energy.plot(t, potential, color=colors[1], label="potential $V$")
    ax_energy.plot(t, work, color=colors[2], label=r"drag work $W_{\mathrm{drag}}$")
    ax_energy.plot(
        t,
        kinetic + potential + work,
        color="k",
        linestyle="--",
        label=r"$T + V + W_{\mathrm{drag}}$",
    )
    ax_energy.set(
        xlabel="time $t$ (s)",
        ylabel="energy (J)",
        title=f"(c) Energy budget, {ENERGY_ANGLE_DEG:g}° launch",
        xlim=(0.0, t[-1]),
        ylim=(-5.0, 165.0),
    )
    ax_energy.legend(fontsize=9, loc="upper center", ncol=2)
    for ax in (ax_path, ax_range, ax_energy):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    k = drag_constant()
    print(f"k = {k:.5f} 1/m, terminal speed = {terminal_speed():.2f} m/s")
    for angle in ANGLES_DEG:
        _, s, t_end = fly(angle)
        print(
            f"{angle:g} deg: range {s[0, -1]:.1f} m (no drag {vacuum_range(angle):.1f} m), "
            f"apex {s[1].max():.1f} m, flight {t_end:.2f} s, "
            f"impact speed {np.hypot(s[2, -1], s[3, -1]):.1f} m/s"
        )
    best_angle, best_range = optimum_angle()
    print(f"optimum angle with drag: {best_angle:.2f} deg, range {best_range:.2f} m")
    _, s, _ = fly(ENERGY_ANGLE_DEG)
    kinetic, potential, work = energy_budget(s)
    total = kinetic + potential + work
    print(
        f"energy: T0 = {kinetic[0]:.2f} J, drag work = {work[-1]:.2f} J, "
        f"max |T + V + W - T0| = {np.max(np.abs(total - total[0])):.2e} J"
    )

    finish_figures(
        {"dynamics_projectile_drag.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
