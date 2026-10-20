"""Variable-mass dynamics of a vertically launched rocket: Tsiolkovsky, gravity and drag losses.

The momentum balance of a body that ejects mass at speed v_e relative to
itself, m dv/dt = mdot v_e - m g - D, is integrated with scipy's RK45 for a
1000 kg single-stage rocket burning 700 kg of propellant at 10 kg/s
(v_e = 2500 m/s, thrust 25 kN). The ideal velocity v_e ln(m0/m) of the rocket
equation, the closed-form solution with constant gravity and the numerical
solution with quadratic drag in an exponential atmosphere are compared, and
the burnout speed is split into the ideal increment, the gravity loss and the
drag loss.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # g, taken constant (m/s^2)
INITIAL_MASS = 1000.0  # m0 (kg)
PROPELLANT_MASS = 700.0  # (kg)
MASS_FLOW = 10.0  # mdot (kg/s)
EXHAUST_SPEED = 2500.0  # v_e relative to the rocket (m/s)
DRAG_COEFFICIENT = 0.4  # C_d based on the frontal area
DIAMETER = 0.5  # (m)
SEA_LEVEL_DENSITY = 1.225  # rho_0 (kg/m^3)
SCALE_HEIGHT = 8500.0  # H of the exponential atmosphere rho = rho_0 exp(-h/H) (m)
BURN_TIME = PROPELLANT_MASS / MASS_FLOW  # t_b (s)


def mass(t):
    """Rocket mass (kg) during the burn."""
    return INITIAL_MASS - MASS_FLOW * np.asarray(t)


def ideal_speed(t):
    """Rocket equation without gravity or drag, v = v_e ln(m0/m)."""
    return EXHAUST_SPEED * np.log(INITIAL_MASS / mass(t))


def gravity_only(t, g=GRAVITY):
    """Closed-form speed and altitude with constant gravity and no drag."""
    t = np.asarray(t, dtype=float)
    m = mass(t)
    v = EXHAUST_SPEED * np.log(INITIAL_MASS / m) - g * t
    h = (
        EXHAUST_SPEED / MASS_FLOW * (INITIAL_MASS - m - m * np.log(INITIAL_MASS / m))
        - 0.5 * g * t**2
    )
    return v, h


def rhs(t, state, g, drag):
    """State (h, v, gravity loss, drag loss); mass is known in closed form."""
    h, v, _, _ = state
    m = mass(t)
    area = np.pi * DIAMETER**2 / 4.0
    rho = SEA_LEVEL_DENSITY * np.exp(-max(h, 0.0) / SCALE_HEIGHT)
    d = 0.5 * rho * DRAG_COEFFICIENT * area * v * abs(v) if drag else 0.0
    thrust = MASS_FLOW * EXHAUST_SPEED
    return [v, (thrust - d) / m - g, g, d / m]


def burn(g=GRAVITY, drag=True, n=141):
    """Integrate from lift-off to burnout; return times and the state history."""
    t = np.linspace(0.0, BURN_TIME, n)
    sol = solve_ivp(
        rhs,
        (0.0, BURN_TIME),
        [0.0, 0.0, 0.0, 0.0],
        args=(g, drag),
        t_eval=t,
        rtol=1e-10,
        atol=1e-8,
    )
    return sol.t, sol.y


def make_figure():
    """Draw speed and altitude histories and the burnout speed budget."""
    colors = plt.get_cmap("tab10").colors
    fig, (ax_v, ax_h, ax_bar) = plt.subplots(
        1, 3, figsize=(13.5, 4.8), gridspec_kw={"width_ratios": [1.1, 1.1, 0.9]}
    )
    t = np.linspace(0.0, BURN_TIME, 400)
    v_g, h_g = gravity_only(t)
    t_n, s_g = burn(drag=False, n=15)
    t_d, s_d = burn(drag=True)

    ax_v.plot(t, ideal_speed(t), color=colors[0], label=r"ideal: $v_e \ln(m_0/m)$")
    ax_v.plot(t, v_g, color=colors[1], label="gravity, closed form")
    ax_v.plot(t_n, s_g[1], "o", color=colors[1], ms=4, label="gravity, RK45")
    ax_v.plot(t_d, s_d[1], color=colors[3], label="gravity and drag, RK45")
    ax_v.set(
        xlabel="time $t$ (s)",
        ylabel="speed $v$ (m/s)",
        title=f"(a) Speed during the {BURN_TIME:.0f} s burn",
        xlim=(0.0, BURN_TIME),
    )
    ax_v.legend(fontsize=9, loc="upper left")

    ax_h.plot(t, h_g / 1e3, color=colors[1], label="gravity, closed form")
    ax_h.plot(t_n, s_g[0] / 1e3, "o", color=colors[1], ms=4, label="gravity, RK45")
    ax_h.plot(t_d, s_d[0] / 1e3, color=colors[3], label="gravity and drag, RK45")
    ax_h.set(
        xlabel="time $t$ (s)",
        ylabel="altitude $h$ (km)",
        title="(b) Altitude",
        xlim=(0.0, BURN_TIME),
    )
    ax_h.legend(fontsize=9, loc="upper left")

    ideal = ideal_speed(BURN_TIME)
    g_loss, d_loss, final = s_d[2, -1], s_d[3, -1], s_d[1, -1]
    names = ["ideal", "gravity\nloss", "drag\nloss", "burnout"]
    values = [ideal, -g_loss, -d_loss, final]
    bottoms = [0.0, ideal - g_loss, ideal - g_loss - d_loss, 0.0]
    heights = [ideal, g_loss, d_loss, final]
    bar_colors = [colors[0], colors[1], colors[3], "0.35"]
    ax_bar.bar(names, heights, bottom=bottoms, color=bar_colors, width=0.6)
    for i, (value, bottom, height) in enumerate(zip(values, bottoms, heights)):
        ax_bar.text(
            i, bottom + height + 40.0, f"{value:+.0f}", ha="center", fontsize=10
        )
    ax_bar.set(
        ylabel="speed (m/s)",
        title="(c) Burnout speed budget",
        ylim=(0.0, 1.15 * ideal),
    )
    for ax in (ax_v, ax_h, ax_bar):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    thrust = MASS_FLOW * EXHAUST_SPEED
    print(
        f"thrust = {thrust / 1e3:.1f} kN, lift-off T/W = "
        f"{thrust / (INITIAL_MASS * GRAVITY):.2f}, burn time = {BURN_TIME:.0f} s"
    )
    v_g, h_g = gravity_only(BURN_TIME)
    t, s_g = burn(drag=False)
    print(f"ideal burnout speed = {ideal_speed(BURN_TIME):.1f} m/s")
    print(
        f"gravity only: closed form v = {v_g:.2f} m/s, h = {h_g:.1f} m; "
        f"RK45 v = {s_g[1, -1]:.2f} m/s, h = {s_g[0, -1]:.1f} m"
    )
    t, s_d = burn(drag=True)
    print(
        f"gravity and drag: v = {s_d[1, -1]:.1f} m/s, h = {s_d[0, -1]:.0f} m, "
        f"gravity loss = {s_d[2, -1]:.1f} m/s, drag loss = {s_d[3, -1]:.1f} m/s"
    )
    finish_figures(
        {"dynamics_variable_mass_rocket.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
