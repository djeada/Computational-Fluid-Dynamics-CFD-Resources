"""Constraint diagram (T/W against W/S) and Breguet range for a light business jet.

Each performance requirement (takeoff ground run, sustained climb rate,
cruise at altitude, stall speed with landing flaps) gives the thrust-to-weight
ratio needed as a function of wing loading. The curves are referred to
sea-level static thrust and takeoff weight; the feasible region lies above
every thrust curve and to the left of the stall line, and the design point is
the lowest T/W inside it. A second panel plots the Breguet range against the
lift-to-drag ratio for three fuel fractions.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # (m/s^2)
RHO_SL = 1.225  # sea-level density (kg/m^3)

# Aerodynamics of the clean aircraft.
CD0 = 0.022  # zero-lift drag coefficient
ASPECT_RATIO = 8.0
OSWALD = 0.80  # span efficiency e
K_INDUCED = 1.0 / (np.pi * ASPECT_RATIO * OSWALD)  # k in C_D = C_D0 + k C_L^2

# Takeoff: ground run to lift-off on a dry runway at sea level.
GROUND_RUN = 900.0  # S_G (m)
CL_MAX_TO = 1.8  # maximum lift coefficient, takeoff flaps
CL_TO = 0.6  # lift coefficient during the ground run
CD_TO = 0.045  # drag coefficient during the ground run (flaps, gear)
MU_ROLL = 0.04  # rolling friction coefficient
LIFTOFF_FACTOR = 1.2  # V_LOF = 1.2 V_stall,TO

# Climb: sustained climb rate at sea level.
CLIMB_RATE = 12.0  # V_V (m/s), about 2400 ft/min
CLIMB_SPEED = 110.0  # V (m/s)

# Cruise at altitude.
CRUISE_SPEED = 210.0  # (m/s), about Mach 0.71 at 11 km
CRUISE_DENSITY = 0.3639  # density at 11 km in the standard atmosphere (kg/m^3)
CRUISE_WEIGHT_FRACTION = 0.95  # beta = W_cruise / W_TO
LAPSE_EXPONENT = 0.75  # thrust lapse alpha = sigma^m for a turbofan (assumed)

# Stall with landing flaps (approach speed requirement).
STALL_SPEED = 48.0  # V_s (m/s), about 93 kn
CL_MAX_LAND = 2.2  # maximum lift coefficient, landing flaps
LANDING_WEIGHT_FRACTION = 0.85  # W_land / W_TO

# Breguet range example.
BREGUET_SPEED = 230.0  # cruise speed (m/s)
TSFC = 1.6e-5  # thrust-specific fuel consumption c (kg/(N s)), 0.57 lb/(lbf h)
WEIGHT_RATIOS = (1.2, 1.35, 1.5)  # W_i / W_f

WING_LOADING = np.linspace(500.0, 5000.0, 400)  # W/S grid (N/m^2)


def dynamic_pressure(rho, speed):
    return 0.5 * rho * speed**2


def takeoff_constraint(ws):
    """T/W for a ground run S_G, using the average force at V_LOF / sqrt(2)."""
    v_lof = LIFTOFF_FACTOR * np.sqrt(2.0 * ws / (RHO_SL * CL_MAX_TO))
    q = dynamic_pressure(RHO_SL, v_lof / np.sqrt(2.0))
    return (
        v_lof**2 / (2.0 * GRAVITY * GROUND_RUN)
        + q * CD_TO / ws
        + MU_ROLL * (1.0 - q * CL_TO / ws)
    )


def level_flight_tw(ws, q, n=1.0):
    """T/W in steady level flight at load factor n: q C_D0/(W/S) + k n^2 (W/S)/q."""
    return q * CD0 / ws + K_INDUCED * n**2 * ws / q


def climb_constraint(ws):
    """T/W for a sustained climb rate V_V at speed V at sea level."""
    q = dynamic_pressure(RHO_SL, CLIMB_SPEED)
    return CLIMB_RATE / CLIMB_SPEED + level_flight_tw(ws, q)


def cruise_constraint(ws):
    """Sea-level static T/W_TO that gives cruise thrust = drag at altitude."""
    beta = CRUISE_WEIGHT_FRACTION
    alpha = (CRUISE_DENSITY / RHO_SL) ** LAPSE_EXPONENT
    q = dynamic_pressure(CRUISE_DENSITY, CRUISE_SPEED)
    return beta / alpha * level_flight_tw(beta * ws, q)


def stall_wing_loading():
    """Largest takeoff W/S for which the landing stall speed is met."""
    return 0.5 * RHO_SL * STALL_SPEED**2 * CL_MAX_LAND / LANDING_WEIGHT_FRACTION


def design_point(ws=WING_LOADING):
    """Lowest required T/W within the feasible wing loadings."""
    envelope = np.max(
        [takeoff_constraint(ws), climb_constraint(ws), cruise_constraint(ws)], axis=0
    )
    feasible = ws <= stall_wing_loading()
    k = np.argmin(np.where(feasible, envelope, np.inf))
    return ws[k], envelope[k], envelope


def breguet_range(lift_to_drag, weight_ratio, speed=BREGUET_SPEED, tsfc=TSFC):
    """Breguet range R = V/(c g) (L/D) ln(W_i/W_f) in metres (c in kg/(N s))."""
    return speed / (tsfc * GRAVITY) * lift_to_drag * np.log(weight_ratio)


def make_figure():
    ws = WING_LOADING
    ws_stall = stall_wing_loading()
    ws_opt, tw_opt, envelope = design_point(ws)
    colors = plt.get_cmap("tab10").colors

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
    ax = axes[0]
    curves = [
        (takeoff_constraint(ws), f"takeoff, $S_G$ = {GROUND_RUN:.0f} m"),
        (climb_constraint(ws), f"climb, {CLIMB_RATE:.0f} m/s at sea level"),
        (cruise_constraint(ws), f"cruise, {CRUISE_SPEED:.0f} m/s at 11 km"),
    ]
    for (tw, label), color in zip(curves, colors):
        ax.plot(ws, tw, color=color, lw=2, label=label)
    ax.axvline(
        ws_stall,
        color=colors[3],
        lw=2,
        label=f"landing stall, $V_s$ = {STALL_SPEED:.0f} m/s",
    )
    feasible = ws <= ws_stall
    ax.fill_between(
        ws[feasible],
        envelope[feasible],
        0.8,
        color=colors[2],
        alpha=0.15,
        label="feasible region",
    )
    ax.plot(
        ws_opt,
        tw_opt,
        "k*",
        ms=16,
        label=f"design point ({ws_opt:.0f} Pa, {tw_opt:.3f})",
    )
    ax.set_xlim(ws[0], ws[-1])
    ax.set_ylim(0.0, 0.8)
    ax.set_xlabel("wing loading W/S (N/m$^2$)")
    ax.set_ylabel("thrust-to-weight ratio $T_{SL}/W_{TO}$")
    ax.set_title("(a) Constraint diagram")
    ax.legend(fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ld = np.linspace(8.0, 24.0, 100)
    for ratio, color in zip(WEIGHT_RATIOS, colors):
        ax.plot(
            ld,
            breguet_range(ld, ratio) / 1e3,
            color=color,
            lw=2,
            label=f"$W_i/W_f$ = {ratio}",
        )
    ax.set_xlabel("lift-to-drag ratio L/D")
    ax.set_ylabel("range (km)")
    ax.set_title(
        f"(b) Breguet range, V = {BREGUET_SPEED:.0f} m/s, c = {TSFC * 1e6:.0f} mg/(N s)"
    )
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    ws_opt, tw_opt, _ = design_point()
    print(f"k = {K_INDUCED:.4f}, stall-limited W/S = {stall_wing_loading():.0f} N/m^2")
    print(f"Design point: W/S = {ws_opt:.0f} N/m^2, T/W = {tw_opt:.3f}")
    for name, func in (
        ("takeoff", takeoff_constraint),
        ("climb", climb_constraint),
        ("cruise", cruise_constraint),
    ):
        print(f"  {name:8s} T/W at design W/S: {float(func(np.array(ws_opt))):.3f}")
    for ratio in WEIGHT_RATIOS:
        print(
            f"Breguet range at L/D = 18, W_i/W_f = {ratio}: "
            f"{breguet_range(18.0, ratio) / 1e3:.0f} km"
        )

    finish_figures(
        {"aircraft_design_constraint_diagram.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
