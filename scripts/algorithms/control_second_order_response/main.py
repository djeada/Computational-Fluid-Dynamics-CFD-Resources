"""Step responses of the standard second-order system and their time-domain specifications.

Simulates G(s) = wn^2 / (s^2 + 2 zeta wn s + wn^2) for several damping ratios,
measures rise time (10-90 %), peak time, percentage overshoot and 2 % settling
time from the computed responses, compares them with the closed-form formulas
M_p = exp(-pi zeta / sqrt(1 - zeta^2)), t_p = pi / w_d and t_s = 4 / (zeta wn),
and draws the pole locations in the s-plane with lines of constant damping
ratio and circles of constant natural frequency.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

OMEGA_N = 2.0  # natural frequency (rad/s)
ZETAS = (0.1, 0.3, 0.5, 0.7, 1.0, 2.0)  # damping ratios plotted
ANNOTATED_ZETA = 0.3  # response whose specifications are drawn on panel (a)
SETTLING_BAND = 0.02  # settling tolerance (fraction of the final value)
T_END = 20.0  # simulated time (s)
N_TIME = 20001  # time samples (dt = 1 ms)


def second_order_system(zeta, omega_n=OMEGA_N):
    """Return the LTI object of wn^2 / (s^2 + 2 zeta wn s + wn^2)."""
    return signal.lti([omega_n**2], [1.0, 2.0 * zeta * omega_n, omega_n**2])


def step_response(zeta, omega_n=OMEGA_N, t_end=T_END, n=N_TIME):
    """Simulate the unit step response; returns (t, y)."""
    t = np.linspace(0.0, t_end, n)
    t, y = signal.step(second_order_system(zeta, omega_n), T=t)
    return t, y


def _crossing_time(t, y, level):
    """First time at which y reaches level, by linear interpolation."""
    i = int(np.argmax(y >= level))
    if i == 0:
        return t[0]
    return t[i - 1] + (level - y[i - 1]) * (t[i] - t[i - 1]) / (y[i] - y[i - 1])


def step_metrics(t, y, y_final=1.0, band=SETTLING_BAND):
    """Rise time (10-90 %), peak time, overshoot (fraction) and settling time."""
    rise = _crossing_time(t, y, 0.9 * y_final) - _crossing_time(t, y, 0.1 * y_final)
    k_peak = int(np.argmax(y))
    overshoot = max(0.0, (y[k_peak] - y_final) / y_final)
    peak_time = t[k_peak] if overshoot > 0 else np.nan
    outside = np.nonzero(np.abs(y - y_final) > band * abs(y_final))[0]
    settling = t[outside[-1] + 1] if outside.size else t[0]
    return {
        "rise_time": rise,
        "peak_time": peak_time,
        "overshoot": overshoot,
        "settling_time": settling,
    }


def overshoot_formula(zeta):
    """Percentage overshoot as a fraction, exp(-pi zeta / sqrt(1 - zeta^2))."""
    zeta = np.asarray(zeta, dtype=float)
    out = np.zeros_like(zeta)
    under = zeta < 1.0
    out[under] = np.exp(-np.pi * zeta[under] / np.sqrt(1.0 - zeta[under] ** 2))
    return out


def peak_time_formula(zeta, omega_n=OMEGA_N):
    """t_p = pi / (wn sqrt(1 - zeta^2)) for an underdamped system."""
    return np.pi / (omega_n * np.sqrt(1.0 - zeta**2))


def settling_time_estimate(zeta, omega_n=OMEGA_N):
    """Estimate t_s = 4 / |Re p| from the slowest pole (4 / (zeta wn) if zeta < 1)."""
    zeta = np.asarray(zeta, dtype=float)
    over = np.sqrt(np.maximum(zeta**2 - 1.0, 0.0))
    return 4.0 / (omega_n * (zeta - over))


def poles(zeta, omega_n=OMEGA_N):
    """Roots of s^2 + 2 zeta wn s + wn^2."""
    return np.roots([1.0, 2.0 * zeta * omega_n, omega_n**2])


def zeta_from_overshoot(mp):
    """Damping ratio that gives overshoot fraction mp (inverse of the formula)."""
    a = -np.log(mp)
    return a / np.sqrt(np.pi**2 + a**2)


def make_figure(results):
    colors = plt.cm.tab10(np.arange(len(ZETAS)))
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    # (a) step responses with the specifications of one curve annotated
    ax = axes[0, 0]
    for color, zeta in zip(colors, ZETAS):
        t, y = results[zeta]["t"], results[zeta]["y"]
        ax.plot(t, y, color=color, lw=1.8, label=rf"$\zeta = {zeta}$")
    m = results[ANNOTATED_ZETA]["metrics"]
    t, y = results[ANNOTATED_ZETA]["t"], results[ANNOTATED_ZETA]["y"]
    t10 = _crossing_time(t, y, 0.1)
    t90 = _crossing_time(t, y, 0.9)
    ax.axhspan(1 - SETTLING_BAND, 1 + SETTLING_BAND, color="0.85", zorder=0)
    ax.plot([t10, t90], [0.1, 0.9], "ko", ms=5)
    for tk, level in ((t10, 0.1), (t90, 0.9)):
        ax.plot([tk, tk], [0.0, level], "k:", lw=1.0)
    ax.annotate(
        "",
        xy=(t90, 0.04),
        xytext=(t10, 0.04),
        arrowprops={"arrowstyle": "<->", "color": "k"},
    )
    ax.text(
        t90 + 0.15,
        0.06,
        f"$t_r$ = {m['rise_time']:.2f} s (10-90 %)",
        fontsize=10,
    )
    ax.plot(m["peak_time"], 1 + m["overshoot"], "kv", ms=7)
    ax.annotate(
        f"$M_p$ = {100 * m['overshoot']:.1f} % at $t_p$ = {m['peak_time']:.2f} s"
        rf" ($\zeta$ = {ANNOTATED_ZETA})",
        xy=(m["peak_time"], 1 + m["overshoot"]),
        xytext=(6.0, 1.62),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "k"},
    )
    ax.axvline(m["settling_time"], color="k", ls=":", lw=1.2)
    ax.text(
        m["settling_time"] + 0.2,
        0.6,
        rf"$t_s$ = {m['settling_time']:.2f} s ($\zeta$ = {ANNOTATED_ZETA}, 2 % band)",
        fontsize=10,
    )
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1.85)
    ax.set_xlabel("Time $t$ (s)", fontsize=11)
    ax.set_ylabel("Output $y(t)$ for a unit step", fontsize=11)
    ax.set_title(rf"(a) Step responses, $\omega_n$ = {OMEGA_N:g} rad/s", fontsize=12)
    ax.legend(fontsize=10, ncol=2, loc="lower right")
    ax.grid(alpha=0.3)

    # (b) overshoot: formula against simulation
    ax = axes[0, 1]
    zz = np.linspace(0.01, 1.0, 300)
    ax.plot(zz, 100 * overshoot_formula(zz), "k-", lw=1.5, label="Formula")
    for color, zeta in zip(colors, ZETAS):
        ax.plot(
            zeta,
            100 * results[zeta]["metrics"]["overshoot"],
            "o",
            color=color,
            ms=9,
        )
    ax.plot([], [], "o", color="0.4", ms=9, label="Measured from simulation")
    ax.set_xlabel(r"Damping ratio $\zeta$", fontsize=11)
    ax.set_ylabel("Percentage overshoot $M_p$ (%)", fontsize=11)
    ax.set_title(
        r"(b) $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ against simulation", fontsize=12
    )
    ax.set_xlim(0, 2.1)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (c) settling and peak times: estimates against simulation
    ax = axes[1, 0]
    zz = np.linspace(0.05, 2.1, 400)
    ax.plot(
        zz,
        settling_time_estimate(zz),
        "k-",
        lw=1.5,
        label=r"$4/|\mathrm{Re}\,p|$ of the slowest pole",
    )
    zu = zz[zz < 0.99]
    ax.plot(zu, peak_time_formula(zu), "k--", lw=1.5, label=r"$\pi/\omega_d$")
    for color, zeta in zip(colors, ZETAS):
        mm = results[zeta]["metrics"]
        ax.plot(zeta, mm["settling_time"], "s", color=color, ms=8)
        ax.plot(zeta, mm["rise_time"], "^", color=color, ms=8)
        if np.isfinite(mm["peak_time"]):
            ax.plot(zeta, mm["peak_time"], "o", color=color, ms=8, mfc="none")
    ax.plot([], [], "s", color="0.4", label="$t_s$ measured")
    ax.plot([], [], "o", color="0.4", mfc="none", label="$t_p$ measured")
    ax.plot([], [], "^", color="0.4", label="$t_r$ measured")
    ax.set_xlabel(r"Damping ratio $\zeta$", fontsize=11)
    ax.set_ylabel("Time (s)", fontsize=11)
    ax.set_title("(c) Settling, peak and rise times", fontsize=12)
    ax.set_xlim(0, 2.1)
    ax.set_ylim(0, 22)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)

    # (d) s-plane
    ax = axes[1, 1]
    radius = 8.0
    for zeta_line in (0.1, 0.3, 0.5, 0.7, 0.9):
        angle = np.arccos(zeta_line)
        for sign in (1, -1):
            ax.plot(
                [0, -radius * np.cos(angle)],
                [0, sign * radius * np.sin(angle)],
                color="0.6",
                lw=0.8,
            )
        r_label = min(3.25 / np.sin(angle), 7.7 / np.cos(angle))
        ax.text(
            -r_label * np.cos(angle),
            r_label * np.sin(angle),
            rf"$\zeta$={zeta_line}",
            fontsize=9,
            color="0.35",
            ha="center",
            va="center",
            bbox={"fc": "white", "ec": "none", "pad": 0.5},
        )
    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, 200)
    for wn in (1.0, 2.0, 3.0):
        ax.plot(wn * np.cos(theta), wn * np.sin(theta), color="0.6", lw=0.8, ls="--")
        ax.text(0.08, wn, rf"$\omega_n$={wn:g}", fontsize=9, color="0.35", va="center")
    for color, zeta in zip(colors, ZETAS):
        p = poles(zeta)
        ax.plot(
            p.real, p.imag, "x", color=color, ms=10, mew=2.5, label=rf"$\zeta = {zeta}$"
        )
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlim(-8, 1)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Real part $\sigma$ (1/s)", fontsize=11)
    ax.set_ylabel(r"Imaginary part $\omega$ (rad/s)", fontsize=11)
    ax.set_title(
        "(d) Poles, constant-$\\zeta$ rays, constant-$\\omega_n$ arcs", fontsize=12
    )
    ax.legend(fontsize=9, loc="lower left", ncol=2)

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    results = {}
    print(f"Second-order system, wn = {OMEGA_N} rad/s")
    print(
        " zeta   t_r (s)  t_p (s)  t_p formula  M_p (%)  M_p formula  t_s (s)  4/|Re p|"
    )
    for zeta in ZETAS:
        t, y = step_response(zeta)
        m = step_metrics(t, y)
        results[zeta] = {"t": t, "y": y, "metrics": m}
        tp_f = peak_time_formula(zeta) if zeta < 1 else np.nan
        print(
            f" {zeta:4.1f}  {m['rise_time']:7.3f}  {m['peak_time']:7.3f}  {tp_f:11.3f}"
            f"  {100 * m['overshoot']:7.2f}  {100 * overshoot_formula([zeta])[0]:11.2f}"
            f"  {m['settling_time']:7.3f}  {settling_time_estimate(zeta):11.3f}"
        )

    fig = make_figure(results)
    finish_figures(
        {"control_second_order_response.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
