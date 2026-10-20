"""Centrifugal pump curves, the system curve, operating points and NPSH.

A pump is described at its rated speed by a head curve H = H0 - A Q^2 and an
efficiency curve with its best-efficiency point (BEP) at Q_bep. The affinity
laws (Q ~ n, H ~ n^2, P ~ n^3) give the curves at other speeds. The system
curve is a static lift plus Darcy-Weisbach pipe and fitting losses,
H_sys = H_s + K Q^2. The script plots the head curves at four speeds with lines
of constant efficiency and the operating points, compares the shaft power
needed to reduce the flow by throttling a valve with that of reducing the
pump speed, and compares the net positive suction head available with the
NPSH the pump requires for cold and hot water.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # gravitational acceleration (m/s^2)
P_ATM = 101_325.0  # pressure on the sump surface (Pa)

# Pump at its rated speed.
RATED_RPM = 1450.0  # n0 (rev/min)
SHUTOFF_HEAD = 40.0  # H0 (m)
HEAD_COEFF = 16_000.0  # A (s^2/m^5): H = H0 - A Q^2
Q_BEP = 0.025  # flow at best efficiency (m^3/s)
ETA_BEP = 0.78  # best efficiency
SPEEDS_RPM = (1450.0, 1300.0, 1150.0, 1000.0)
NPSHR_0 = 1.5  # NPSH required at zero flow, rated speed (m)
NPSHR_COEFF = 2_400.0  # NPSHr = NPSHR_0 + c Q^2 at rated speed (s^2/m^5)

# System: static lift plus a pipe with fittings.
STATIC_HEAD = 15.0  # H_s (m)
PIPE_LENGTH = 120.0  # (m)
PIPE_DIAMETER = 0.10  # (m)
FRICTION_FACTOR = 0.02  # Darcy f (fully rough turbulent, held constant)
MINOR_LOSS_SUM = 5.0  # sum of fitting loss coefficients
SUCTION_LIFT = 3.0  # pump centreline above the sump surface (m)
SUCTION_LOSS_COEFF = 1_600.0  # suction-line loss h = k Q^2 (s^2/m^5)

# Water: temperature (deg C), density (kg/m^3), vapour pressure (Pa).
WATER = ((20.0, 998.2, 2_339.0), (80.0, 971.8, 47_390.0))


def system_coefficient(
    f=FRICTION_FACTOR, length=PIPE_LENGTH, d=PIPE_DIAMETER, k=MINOR_LOSS_SUM
):
    """K in h_f = K Q^2 from Darcy-Weisbach: (f L/D + sum K) 8 / (g pi^2 D^4)."""
    return (f * length / d + k) * 8.0 / (G * np.pi**2 * d**4)


def pump_head(q, rpm, h0=SHUTOFF_HEAD, a=HEAD_COEFF):
    """Head (m) at flow q (m^3/s) and speed rpm from the affinity laws.

    H_n(Q) = r^2 H_0(Q / r) with r = n / n0, which for H_0 = H0 - A Q^2 is
    r^2 H0 - A Q^2.
    """
    r = rpm / RATED_RPM
    return r**2 * h0 - a * np.asarray(q) ** 2


def pump_efficiency(q, rpm):
    """Efficiency at flow q and speed rpm: eta_0(Q / r), a parabola through the BEP."""
    x = np.asarray(q) / (rpm / RATED_RPM) / Q_BEP
    return np.clip(ETA_BEP * x * (2.0 - x), 0.0, None)


def system_head(q, k_sys, h_s=STATIC_HEAD):
    return h_s + k_sys * np.asarray(q) ** 2


def operating_point(rpm, k_sys, h_s=STATIC_HEAD):
    """Flow and head where the pump curve at rpm meets the system curve."""
    r = rpm / RATED_RPM
    q = np.sqrt(max(r**2 * SHUTOFF_HEAD - h_s, 0.0) / (HEAD_COEFF + k_sys))
    return q, system_head(q, k_sys, h_s)


def shaft_power(q, h, eta, rho=WATER[0][1]):
    """P = rho g Q H / eta (W)."""
    return rho * G * q * h / eta


def efficiency_map(q, h):
    """Efficiency of the pump at (Q, H), at whatever speed puts it there.

    Solves r^2 H0 - A Q^2 = H for r; returns (eta, r).
    """
    r = np.sqrt(np.clip((h + HEAD_COEFF * q**2) / SHUTOFF_HEAD, 1e-12, None))
    return pump_efficiency(q, r * RATED_RPM), r


def flow_reduction(k_sys, fractions):
    """Shaft power to deliver a fraction of the design flow by throttling or by speed.

    Throttling: the pump stays at rated speed and a valve adds head loss.
    Speed control: the speed is lowered until the unthrottled system curve
    passes through the reduced flow. Returns (q, P_throttle, P_speed, rpm).
    """
    q_design, _ = operating_point(RATED_RPM, k_sys)
    q = q_design * np.asarray(fractions)
    h_thr = pump_head(q, RATED_RPM)
    p_thr = shaft_power(q, h_thr, pump_efficiency(q, RATED_RPM))
    h_sys = system_head(q, k_sys)
    r = np.sqrt((h_sys + HEAD_COEFF * q**2) / SHUTOFF_HEAD)
    p_spd = shaft_power(q, h_sys, pump_efficiency(q, r * RATED_RPM))
    return q, p_thr, p_spd, r * RATED_RPM


def npsh_available(q, rho, p_vapour):
    """NPSHa = (p_atm - p_v)/(rho g) - z_lift - k_s Q^2 (m)."""
    return (
        (P_ATM - p_vapour) / (rho * G)
        - SUCTION_LIFT
        - SUCTION_LOSS_COEFF * np.asarray(q) ** 2
    )


def npsh_required(q, rpm=RATED_RPM):
    """NPSHr scaled by the affinity law for head: r^2 NPSHr_0(Q / r)."""
    r = rpm / RATED_RPM
    return r**2 * NPSHR_0 + NPSHR_COEFF * np.asarray(q) ** 2


def make_figure(k_sys):
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.8), constrained_layout=True)
    colors = ("tab:blue", "tab:orange", "tab:green", "tab:red")

    ax = axes[0]
    q_grid = np.linspace(0, 0.055, 300)
    h_grid = np.linspace(0, 45, 300)
    qq, hh = np.meshgrid(q_grid, h_grid)
    eta, r = efficiency_map(qq, hh)
    r_min = min(SPEEDS_RPM) / RATED_RPM
    eta = np.where((r <= 1.0) & (r >= r_min), eta, np.nan)
    cs = ax.contour(
        qq * 1e3, hh, eta, levels=[0.6, 0.7, 0.75], colors="0.45", linewidths=1.0
    )
    ax.clabel(cs, fmt=lambda v: f"{v:.2f}", fontsize=9)
    ax.plot([], [], color="0.45", lw=1.0, label="constant efficiency")
    for rpm, col in zip(SPEEDS_RPM, colors, strict=True):
        q_max = np.sqrt((rpm / RATED_RPM) ** 2 * SHUTOFF_HEAD / HEAD_COEFF)
        q = np.linspace(0, q_max, 200)
        ax.plot(q * 1e3, pump_head(q, rpm), color=col, label=f"{rpm:.0f} rpm")
        q_op, h_op = operating_point(rpm, k_sys)
        ax.plot(q_op * 1e3, h_op, "o", color=col, ms=7, mec="black")
    ax.plot(q_grid * 1e3, system_head(q_grid, k_sys), "k-", lw=2, label="system curve")
    ax.axhline(STATIC_HEAD, color="black", ls=":", lw=1)
    ax.text(41, STATIC_HEAD + 0.6, "static head", fontsize=9)
    ax.set_xlim(0, 55)
    ax.set_ylim(0, 45)
    ax.set_xlabel("flow rate Q (L/s)")
    ax.set_ylabel("head H (m)")
    ax.set_title("(a) Pump curves, system curve, operating points")
    ax.legend(fontsize=9, loc="upper right")

    ax = axes[1]
    fractions = np.linspace(0.5, 1.0, 51)
    q, p_thr, p_spd, _ = flow_reduction(k_sys, fractions)
    ax.plot(q * 1e3, p_thr / 1e3, color="tab:red", label="throttling valve, 1450 rpm")
    ax.plot(q * 1e3, p_spd / 1e3, color="tab:blue", label="speed control")
    ax.set_xlabel("delivered flow Q (L/s)")
    ax.set_ylabel("shaft power (kW)")
    ax.set_title("(b) Shaft power to reduce the flow")
    ax.legend(fontsize=9, loc="upper left")

    ax = axes[2]
    q = np.linspace(0, 0.045, 200)
    for (temp, rho, pv), col in zip(WATER, ("tab:blue", "tab:red"), strict=True):
        ax.plot(
            q * 1e3,
            npsh_available(q, rho, pv),
            color=col,
            label=f"NPSH available, {temp:.0f} °C",
        )
    ax.plot(q * 1e3, npsh_required(q), "k--", label="NPSH required, 1450 rpm")
    q_op, _ = operating_point(RATED_RPM, k_sys)
    ax.axvline(q_op * 1e3, color="0.5", lw=0.8)
    ax.text(q_op * 1e3 - 0.5, 0.4, "design flow", fontsize=9, ha="right")
    ax.set_ylim(0, 11)
    ax.set_xlabel("flow rate Q (L/s)")
    ax.set_ylabel("NPSH (m)")
    ax.set_title(f"(c) Cavitation check, suction lift {SUCTION_LIFT:g} m")
    ax.legend(fontsize=9, loc="upper right")
    for ax in axes:
        ax.grid(alpha=0.3)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    k_sys = system_coefficient()
    print(f"system curve: H = {STATIC_HEAD:g} + {k_sys:.0f} Q^2 (m, Q in m^3/s)")
    for rpm in SPEEDS_RPM:
        q, h = operating_point(rpm, k_sys)
        eta = pump_efficiency(q, rpm)
        print(
            f"{rpm:5.0f} rpm: Q = {q * 1e3:5.2f} L/s, H = {h:5.2f} m, "
            f"eta = {eta:.3f}, shaft power = {shaft_power(q, h, eta) / 1e3:5.2f} kW"
        )
    q, p_thr, p_spd, rpm = flow_reduction(k_sys, [0.7])
    print(
        f"70% flow ({q[0] * 1e3:.2f} L/s): throttling {p_thr[0] / 1e3:.2f} kW, "
        f"speed control {p_spd[0] / 1e3:.2f} kW at {rpm[0]:.0f} rpm"
    )
    q_op, _ = operating_point(RATED_RPM, k_sys)
    for temp, rho, pv in WATER:
        print(
            f"water at {temp:.0f} C: NPSHa = {npsh_available(q_op, rho, pv):.2f} m, "
            f"NPSHr = {npsh_required(q_op):.2f} m at the design flow"
        )

    finish_figures(
        {"hydraulics_pump_system_curve.png": make_figure(k_sys)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
