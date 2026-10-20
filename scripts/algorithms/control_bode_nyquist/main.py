"""Bode and Nyquist analysis of a tank level loop, with and without a transport delay.

A proportional controller drives a pump that fills a tank; the level is measured
by a sensor with a first-order lag, and in the second case the water also takes
a fixed time to travel down the supply pipe. The loop transfer function is

    L(s) = K / (s (tau_p s + 1) (tau_m s + 1)) * exp(-T s),  K = Kc k_q / A.

The script computes the Bode magnitude and phase with their straight-line
asymptotes, the gain and phase margins from the Bode data, the Nyquist plot with
its crossing of the negative real axis, the number of encirclements of -1 along
the full Nyquist contour, the sensitivity functions S and T, and the closed-loop
level response to a step in the set-point.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

TANK_AREA = 1.0  # A, tank cross-section (m^2)
PUMP_GAIN = 0.05  # k_q, pump flow per volt of command (m^3/(s V))
PUMP_TIME_CONSTANT = 2.0  # tau_p, pump and motor lag (s)
SENSOR_TIME_CONSTANT = 0.5  # tau_m, level-sensor lag (s)
CONTROLLER_GAIN = 10.0  # Kc, proportional gain (V/m)
DELAY = 1.0  # T, transport delay in the supply pipe (s)
OMEGA = np.logspace(-2, 2, 4000)  # frequency grid (rad/s)
T_SIM, DT = 60.0, 0.005  # closed-loop simulation length and step (s)


def loop_gain(kc=CONTROLLER_GAIN):
    """K = Kc k_q / A, the gain of the integrating loop (1/s)."""
    return kc * PUMP_GAIN / TANK_AREA


def loop_response(omega, delay=0.0, k=None):
    """L(j omega) of the level loop."""
    k = loop_gain() if k is None else k
    s = 1j * np.asarray(omega, dtype=float)
    return (
        k
        / (s * (PUMP_TIME_CONSTANT * s + 1) * (SENSOR_TIME_CONSTANT * s + 1))
        * np.exp(-delay * s)
    )


def phase_deg(omega, delay=0.0):
    """Continuous (unwrapped) phase of L(j omega) in degrees."""
    omega = np.asarray(omega, dtype=float)
    return -90.0 - np.degrees(
        np.arctan(PUMP_TIME_CONSTANT * omega)
        + np.arctan(SENSOR_TIME_CONSTANT * omega)
        + delay * omega
    )


def magnitude_asymptote_db(omega, k=None):
    """Straight-line Bode magnitude: -20 dB/dec, then -40, then -60."""
    k = loop_gain() if k is None else k
    omega = np.asarray(omega, dtype=float)
    mag = 20 * np.log10(k / omega)
    for tau in (PUMP_TIME_CONSTANT, SENSOR_TIME_CONSTANT):
        mag -= 20 * np.log10(np.maximum(1.0, tau * omega))
    return mag


def phase_asymptote_deg(omega, delay=0.0):
    """Straight-line phase: each lag goes from 0 to -90 deg over 0.1/tau .. 10/tau."""
    omega = np.asarray(omega, dtype=float)
    phase = -90.0 * np.ones_like(omega)
    for tau in (PUMP_TIME_CONSTANT, SENSOR_TIME_CONSTANT):
        x = np.clip(np.log10(omega * tau) + 1.0, 0.0, 2.0)  # 0 .. 2 decades
        phase -= 45.0 * x
    return phase - np.degrees(delay * omega)


def bode_margins(delay=0.0, k=None):
    """Gain and phase margins from the magnitude and phase functions.

    Returns a dict with the gain crossover w_gc, phase margin PM (deg), phase
    crossover w_pc, gain margin GM (ratio and dB) and the delay margin PM / w_gc.
    """
    k = loop_gain() if k is None else k

    def mag_minus_one(w):
        return abs(loop_response(w, delay, k)) - 1.0

    w_gc = brentq(mag_minus_one, 1e-4, 1e3)
    pm = 180.0 + phase_deg(w_gc, delay)
    w_pc = brentq(lambda w: phase_deg(w, delay) + 180.0, 1e-4, 1e3)
    gm = 1.0 / abs(loop_response(w_pc, delay, k))
    return {
        "w_gc": w_gc,
        "pm": pm,
        "w_pc": w_pc,
        "gm": gm,
        "gm_db": 20 * np.log10(gm),
        "delay_margin": np.radians(pm) / w_gc,
    }


def nyquist_real_axis_crossing(delay=0.0, k=None, omega=None):
    """First crossing of the negative real axis of the Nyquist plot.

    Found independently of bode_margins: the sign change of Im L on a dense
    frequency grid is located by linear interpolation. Returns (omega, Re L).
    """
    omega = np.logspace(-3, 2, 200001) if omega is None else omega
    values = loop_response(omega, delay, k)
    im = values.imag
    idx = np.nonzero((im[:-1] < 0) & (im[1:] >= 0) & (values.real[:-1] < 0))[0][0]
    f = -im[idx] / (im[idx + 1] - im[idx])
    w = omega[idx] + f * (omega[idx + 1] - omega[idx])
    re = values.real[idx] + f * (values.real[idx + 1] - values.real[idx])
    return w, re


def nyquist_unit_circle_crossing(delay=0.0, k=None, omega=None):
    """Point where |L| = 1 on the Nyquist plot; returns (omega, L)."""
    omega = np.logspace(-3, 2, 200001) if omega is None else omega
    values = loop_response(omega, delay, k)
    mag = np.abs(values)
    idx = np.nonzero((mag[:-1] >= 1.0) & (mag[1:] < 1.0))[0][0]
    return omega[idx], values[idx]


def clockwise_encirclements(delay=0.0, k=None, eps=1e-4, radius=1e4, n=200001):
    """Clockwise encirclements N of -1 by L(s) along the full Nyquist contour.

    The contour runs up the imaginary axis from j eps to j radius, around the
    large semicircle, up from -j radius to -j eps and around the pole at the
    origin on a small semicircle into the right half-plane.
    """
    k = loop_gain() if k is None else k

    def loop(s):
        return (
            k
            / (s * (PUMP_TIME_CONSTANT * s + 1) * (SENSOR_TIME_CONSTANT * s + 1))
            * np.exp(-delay * s)
        )

    w = np.geomspace(eps, radius, n)
    theta_big = np.linspace(np.pi / 2, -np.pi / 2, 2001)
    theta_small = np.linspace(-np.pi / 2, np.pi / 2, 2001)
    contour = np.concatenate(
        (
            1j * w,
            radius * np.exp(1j * theta_big),
            -1j * w[::-1],
            eps * np.exp(1j * theta_small),
        )
    )
    phase = np.unwrap(np.angle(1.0 + loop(contour)))
    winding = (phase[-1] - phase[0]) / (2 * np.pi)  # counter-clockwise turns
    return int(round(-winding))


def sensitivities(omega, delay=0.0):
    """|S| and |T| on the frequency grid."""
    loop = loop_response(omega, delay)
    s = 1.0 / (1.0 + loop)
    return np.abs(s), np.abs(loop * s)


def simulate_step(delay=0.0, kc=CONTROLLER_GAIN, t_end=T_SIM, dt=DT, setpoint=1.0):
    """Closed-loop level response to a set-point step (RK4 with a delay buffer).

    States: level h (m), pump flow q (m^3/s), measured level y (m). The pump
    command is u = Kc (r - y); the flow reaching the tank is q(t - T).
    """
    n = int(round(t_end / dt))
    lag = int(round(delay / dt))
    q_hist = np.zeros(n + lag + 1)  # q_hist[i + lag] is q at step i
    h = q = y = 0.0
    t = np.arange(n + 1) * dt
    level = np.zeros(n + 1)

    def rhs(state, q_in, u):
        h_, q_, y_ = state
        return np.array(
            [
                q_in / TANK_AREA,
                (PUMP_GAIN * u - q_) / PUMP_TIME_CONSTANT,
                (h_ - y_) / SENSOR_TIME_CONSTANT,
            ]
        )

    state = np.array([h, q, y])
    for i in range(n):
        q_hist[i + lag] = state[1]
        q_in = q_hist[i]  # delayed flow, held over the step
        u = kc * (setpoint - state[2])
        k1 = rhs(state, q_in, u)
        k2 = rhs(state + 0.5 * dt * k1, q_in, u)
        k3 = rhs(state + 0.5 * dt * k2, q_in, u)
        k4 = rhs(state + dt * k3, q_in, u)
        state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        level[i + 1] = state[0]
    return t, level


def make_bode_nyquist_figure(cases):
    fig = plt.figure(figsize=(13, 8.5))
    gs = GridSpec(2, 2, figure=fig, width_ratios=(1.15, 1.0))
    ax_m = fig.add_subplot(gs[0, 0])
    ax_p = fig.add_subplot(gs[1, 0], sharex=ax_m)
    ax_n = fig.add_subplot(gs[:, 1])

    ax_m.semilogx(
        OMEGA, magnitude_asymptote_db(OMEGA), "k:", lw=1.5, label="Asymptotes"
    )
    ax_p.semilogx(
        OMEGA, phase_asymptote_deg(OMEGA), "k:", lw=1.5, label="Asymptotes (no delay)"
    )
    for (label, delay, m), color in zip(cases, ("C0", "C3")):
        mag = 20 * np.log10(np.abs(loop_response(OMEGA, delay)))
        ph = phase_deg(OMEGA, delay)
        ax_m.semilogx(OMEGA, mag, color=color, lw=2, label=label)
        ax_p.semilogx(OMEGA, ph, color=color, lw=2, label=label)
        # gain margin arrow at the phase crossover
        ax_m.annotate(
            "",
            xy=(m["w_pc"], 0),
            xytext=(m["w_pc"], -m["gm_db"]),
            arrowprops={"arrowstyle": "<->", "color": color, "lw": 1.5},
        )
        if delay == 0:
            ax_m.text(
                m["w_pc"] * 1.12,
                -m["gm_db"] / 2,
                f"GM {m['gm_db']:.1f} dB",
                color=color,
                fontsize=10,
                va="center",
            )
        else:
            ax_m.text(
                m["w_pc"] * 0.85,
                -12,
                f"GM {m['gm_db']:.1f} dB",
                color=color,
                fontsize=10,
                va="center",
                ha="right",
            )
        # phase margin arrow at the gain crossover
        ax_p.annotate(
            "",
            xy=(m["w_gc"], -180),
            xytext=(m["w_gc"], -180 + m["pm"]),
            arrowprops={"arrowstyle": "<->", "color": color, "lw": 1.5},
        )
        y_text = -180 + m["pm"] / 2 if delay == 0 else -195
        ax_p.text(
            m["w_gc"] * 0.88,
            y_text,
            f"PM {m['pm']:.1f}°",
            color=color,
            fontsize=10,
            va="center",
            ha="right",
        )
    ax_m.axhline(0, color="k", lw=0.8)
    ax_p.axhline(-180, color="k", lw=0.8)
    ax_m.set_ylim(-70, 40)
    ax_p.set_ylim(-300, -80)
    ax_m.set_ylabel("Magnitude $|L(j\\omega)|$ (dB)", fontsize=11)
    ax_p.set_ylabel("Phase $\\angle L(j\\omega)$ (deg)", fontsize=11)
    ax_p.set_xlabel("Frequency $\\omega$ (rad/s)", fontsize=11)
    ax_m.set_title("(a) Bode magnitude (the delay leaves it unchanged)", fontsize=12)
    ax_p.set_title("(b) Bode phase", fontsize=12)
    ax_m.legend(fontsize=10, loc="lower left")
    ax_p.legend(fontsize=10, loc="lower left")
    for ax in (ax_m, ax_p):
        ax.grid(alpha=0.3, which="both")
    ax_m.set_xlim(OMEGA[0], OMEGA[-1])

    w = np.logspace(-1.5, 2, 6000)
    circle = np.exp(1j * np.linspace(0, 2 * np.pi, 400))
    ax_n.plot(
        circle.real, circle.imag, color="0.6", lw=0.8, ls="--", label="Unit circle"
    )
    for (label, delay, m), color in zip(cases, ("C0", "C3")):
        values = loop_response(w, delay)
        ax_n.plot(values.real, values.imag, color=color, lw=2, label=label)
        ax_n.plot(values.real, -values.imag, color=color, lw=1, ls=":")
        w_c, re_c = nyquist_real_axis_crossing(delay)
        ax_n.plot(re_c, 0, "o", color=color, ms=8)
        _, l_gc = nyquist_unit_circle_crossing(delay)
        ax_n.plot([0, l_gc.real], [0, l_gc.imag], color=color, lw=1)
        ax_n.plot(l_gc.real, l_gc.imag, "s", color=color, ms=7)
        ax_n.annotate(
            f"Re L = {re_c:.3f} = -1/GM",
            xy=(re_c, 0),
            xytext=(-0.45, -0.95 if delay == 0 else -1.15),
            color=color,
            fontsize=10,
            arrowprops={"arrowstyle": "->", "color": color, "lw": 1},
        )
    idx = len(w) // 3
    ax_n.annotate(
        "",
        xy=(values.real[idx + 50], values.imag[idx + 50]),
        xytext=(values.real[idx], values.imag[idx]),
        arrowprops={"arrowstyle": "->", "color": "C3", "lw": 2},
    )
    ax_n.plot(-1, 0, "k+", ms=16, mew=2.5)
    ax_n.text(-1.05, 0.08, "$-1$", fontsize=12, ha="right")
    ax_n.axhline(0, color="k", lw=0.7)
    ax_n.axvline(0, color="k", lw=0.7)
    ax_n.set_xlim(-2.0, 0.6)
    ax_n.set_ylim(-1.6, 1.0)
    ax_n.set_aspect("equal")
    ax_n.set_xlabel("Re $L(j\\omega)$", fontsize=11)
    ax_n.set_ylabel("Im $L(j\\omega)$", fontsize=11)
    ax_n.set_title(
        "(c) Nyquist plot ($\\omega > 0$ solid, $\\omega < 0$ dotted)", fontsize=12
    )
    ax_n.legend(fontsize=10, loc="upper left")
    ax_n.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def make_sensitivity_figure(cases):
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5))
    for (label, delay, m), color in zip(cases, ("C0", "C3")):
        s_mag, t_mag = sensitivities(OMEGA, delay)
        ax.semilogx(
            OMEGA, 20 * np.log10(s_mag), color=color, lw=2, label=f"|S|, {label}"
        )
        ax.semilogx(
            OMEGA,
            20 * np.log10(t_mag),
            color=color,
            lw=1.5,
            ls="--",
            label=f"|T|, {label}",
        )
        i = np.argmax(s_mag)
        ax.plot(OMEGA[i], 20 * np.log10(s_mag[i]), "o", color=color, ms=7)
        ax.text(
            OMEGA[i] * 1.15,
            20 * np.log10(s_mag[i]) + 1.5,
            f"$M_s$ = {s_mag[i]:.2f}",
            color=color,
            fontsize=10,
        )
        t, level = simulate_step(delay)
        bx.plot(t, level, color=color, lw=2, label=label)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylim(-40, 20)
    ax.set_xlim(OMEGA[0], OMEGA[-1])
    ax.set_xlabel("Frequency $\\omega$ (rad/s)", fontsize=11)
    ax.set_ylabel("Magnitude (dB)", fontsize=11)
    ax.set_title("(a) Sensitivity S and complementary sensitivity T", fontsize=12)
    ax.legend(fontsize=9, loc="lower left")
    ax.grid(alpha=0.3, which="both")
    bx.axhline(1.0, color="k", lw=0.8, ls=":")
    bx.set_xlabel("Time $t$ (s)", fontsize=11)
    bx.set_ylabel("Tank level $h$ (m)", fontsize=11)
    bx.set_title("(b) Closed-loop response to a 1 m set-point step", fontsize=12)
    bx.legend(fontsize=10, loc="lower right")
    bx.grid(alpha=0.3)
    bx.set_xlim(0, T_SIM)
    fig.tight_layout()
    return fig


def analyse():
    cases = []
    for label, delay in (("no delay", 0.0), (f"delay T = {DELAY:g} s", DELAY)):
        cases.append((label, delay, bode_margins(delay)))
    return cases


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    cases = analyse()
    print(f"Loop gain K = Kc k_q / A = {loop_gain():.3f} 1/s")
    for label, delay, m in cases:
        w_c, re_c = nyquist_real_axis_crossing(delay)
        s_mag, _ = sensitivities(OMEGA, delay)
        t, level = simulate_step(delay)
        print(f"{label}:")
        print(
            f"  gain crossover {m['w_gc']:.4f} rad/s, PM = {m['pm']:.2f} deg,"
            f" delay margin = {m['delay_margin']:.3f} s"
        )
        print(
            f"  phase crossover {m['w_pc']:.4f} rad/s, GM = {m['gm']:.3f}"
            f" ({m['gm_db']:.2f} dB)"
        )
        print(
            f"  Nyquist crossing at omega = {w_c:.4f}, Re L = {re_c:.4f},"
            f" -1/Re L = {-1 / re_c:.3f}"
        )
        print(
            f"  clockwise encirclements of -1: N = {clockwise_encirclements(delay)},"
            f" with gain x{1.2 * m['gm']:.2f}: N ="
            f" {clockwise_encirclements(delay, k=1.2 * m['gm'] * loop_gain())}"
        )
        print(
            f"  M_s = {s_mag.max():.3f}, step overshoot = {100 * (level.max() - 1):.1f} %"
        )

    figures = {
        "control_bode_nyquist.png": make_bode_nyquist_figure(cases),
        "control_sensitivity.png": make_sensitivity_figure(cases),
    }
    finish_figures(figures, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
