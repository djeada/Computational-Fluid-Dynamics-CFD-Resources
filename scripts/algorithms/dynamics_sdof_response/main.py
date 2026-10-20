"""Single-degree-of-freedom vibration: free decay, frequency response and transmissibility.

A mass-spring-damper with natural frequency 1 Hz is released from a 10 mm
displacement for damping ratios 0 (undamped), 0.1 (underdamped), 1 (critical)
and 2 (overdamped). The closed-form free response is compared with the
Newmark-beta average-acceleration integrator. The steady-state magnification
factor and phase lag of harmonic forcing and the displacement transmissibility
of base excitation are plotted for several damping ratios, with the resonance
peaks at r = sqrt(1 - 2 zeta^2) marked.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MASS = 1.0  # m (kg)
NATURAL_FREQUENCY_HZ = 1.0  # f_n (Hz)
STIFFNESS = MASS * (2.0 * np.pi * NATURAL_FREQUENCY_HZ) ** 2  # k (N/m)
X0 = 0.010  # initial displacement (m)
V0 = 0.0  # initial velocity (m/s)
DURATION = 3.0  # length of the free-decay record (s)
STEPS_PER_PERIOD = 50  # Newmark time step dt = T_n / 50
FREE_ZETAS = (0.0, 0.1, 1.0, 2.0)  # damping ratios of the free-decay panel
FRF_ZETAS = (0.05, 0.1, 0.2, 0.5, 1.0 / np.sqrt(2.0), 1.0)  # damping ratios of FRFs
NEWMARK_BETA = 0.25  # average acceleration (unconditionally stable, no damping)
NEWMARK_GAMMA = 0.5


def damping_coefficient(zeta, m=MASS, k=STIFFNESS):
    """Viscous damping c (N s/m) giving damping ratio zeta."""
    return 2.0 * zeta * np.sqrt(k * m)


def free_response(t, zeta, omega_n, x0=X0, v0=V0):
    """Closed-form free response x(t) of m x'' + c x' + k x = 0 for any zeta >= 0."""
    t = np.asarray(t, dtype=float)
    if zeta < 1.0:
        wd = omega_n * np.sqrt(1.0 - zeta**2)
        return np.exp(-zeta * omega_n * t) * (
            x0 * np.cos(wd * t) + (v0 + zeta * omega_n * x0) / wd * np.sin(wd * t)
        )
    if zeta == 1.0:
        return np.exp(-omega_n * t) * (x0 + (v0 + omega_n * x0) * t)
    root = np.sqrt(zeta**2 - 1.0)
    s1 = (-zeta + root) * omega_n
    s2 = (-zeta - root) * omega_n
    c1 = (v0 - s2 * x0) / (s1 - s2)
    c2 = (s1 * x0 - v0) / (s1 - s2)
    return c1 * np.exp(s1 * t) + c2 * np.exp(s2 * t)


def newmark(m, c, k, force, dt, x0, v0, beta=NEWMARK_BETA, gamma=NEWMARK_GAMMA):
    """Integrate m x'' + c x' + k x = f(t) with the Newmark-beta method.

    `force` holds f at the n + 1 time levels. Returns displacement, velocity and
    acceleration arrays of the same length (incremental form, Chopra 2017).
    """
    n = len(force)
    x, v, a = np.zeros(n), np.zeros(n), np.zeros(n)
    x[0], v[0] = x0, v0
    a[0] = (force[0] - c * v0 - k * x0) / m
    k_hat = k + gamma / (beta * dt) * c + m / (beta * dt**2)
    coef_v = m / (beta * dt) + gamma / beta * c
    coef_a = m / (2.0 * beta) + dt * (gamma / (2.0 * beta) - 1.0) * c
    for i in range(n - 1):
        dp = force[i + 1] - force[i] + coef_v * v[i] + coef_a * a[i]
        dx = dp / k_hat
        dv = (
            gamma / (beta * dt) * dx
            - gamma / beta * v[i]
            + dt * (1.0 - gamma / (2.0 * beta)) * a[i]
        )
        da = dx / (beta * dt**2) - v[i] / (beta * dt) - a[i] / (2.0 * beta)
        x[i + 1], v[i + 1], a[i + 1] = x[i] + dx, v[i] + dv, a[i] + da
    return x, v, a


def magnification(r, zeta):
    """Dynamic magnification X k / F0 of harmonic forcing at frequency ratio r."""
    return 1.0 / np.sqrt((1.0 - r**2) ** 2 + (2.0 * zeta * r) ** 2)


def phase_lag(r, zeta):
    """Phase lag (rad, 0 to pi) of the displacement behind the force."""
    return np.arctan2(2.0 * zeta * r, 1.0 - r**2)


def transmissibility(r, zeta):
    """Displacement (base excitation) or force transmissibility."""
    return np.sqrt(1.0 + (2.0 * zeta * r) ** 2) * magnification(r, zeta)


def peak_frequency_ratio(zeta):
    """Frequency ratio of the magnification peak; nan when there is no peak."""
    return np.sqrt(1.0 - 2.0 * zeta**2) if zeta < 1.0 / np.sqrt(2.0) else np.nan


def free_decay_study():
    """Return time, analytic and Newmark responses for every zeta in FREE_ZETAS."""
    omega_n = np.sqrt(STIFFNESS / MASS)
    dt = 2.0 * np.pi / omega_n / STEPS_PER_PERIOD
    t = np.arange(0.0, DURATION + 0.5 * dt, dt)
    results = {}
    for zeta in FREE_ZETAS:
        c = damping_coefficient(zeta)
        x_num, _, _ = newmark(MASS, c, STIFFNESS, np.zeros_like(t), dt, X0, V0)
        results[zeta] = (free_response(t, zeta, omega_n), x_num)
    return t, results


def make_figure(t, results):
    """Draw free decay, magnification, phase and transmissibility panels."""
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.0))
    (ax_free, ax_mag), (ax_phase, ax_tr) = axes
    colors = plt.get_cmap("tab10").colors
    labels = {0.0: "undamped", 0.1: "underdamped", 1.0: "critical", 2.0: "overdamped"}
    every = 3
    for i, (zeta, (x_exact, x_num)) in enumerate(results.items()):
        ax_free.plot(
            t,
            1e3 * x_exact,
            color=colors[i],
            linewidth=1.8,
            label=rf"$\zeta$ = {zeta:g} ({labels[zeta]})",
        )
        ax_free.plot(
            t[::every],
            1e3 * x_num[::every],
            linestyle="none",
            marker="o",
            markersize=3.5,
            color=colors[i],
        )
    ax_free.plot([], [], "ko", markersize=3.5, label="Newmark, $\\Delta t = T_n/50$")
    ax_free.axhline(0.0, color="0.4", linewidth=0.8)
    ax_free.set(
        xlabel="time $t$ (s)",
        ylabel="displacement $x$ (mm)",
        title="(a) Free response from $x_0$ = 10 mm, $f_n$ = 1 Hz",
        xlim=(0.0, DURATION),
        ylim=(-11.0, 17.0),
    )
    ax_free.legend(fontsize=9, loc="upper center", ncol=2)

    r = np.linspace(0.0, 3.0, 1201)
    for i, zeta in enumerate(FRF_ZETAS):
        label = rf"$\zeta$ = {zeta:.3g}"
        ax_mag.plot(r, magnification(r, zeta), color=colors[i], label=label)
        ax_phase.plot(r, np.degrees(phase_lag(r, zeta)), color=colors[i], label=label)
        ax_tr.plot(r, transmissibility(r, zeta), color=colors[i], label=label)
        rp = peak_frequency_ratio(zeta)
        if np.isfinite(rp):
            ax_mag.plot(rp, magnification(rp, zeta), "o", color=colors[i], ms=5)
    ax_mag.plot([], [], "ko", ms=5, label=r"peak at $r = \sqrt{1 - 2\zeta^2}$")
    ax_mag.set(
        yscale="log",
        ylim=(0.08, 20.0),
        xlim=(0.0, 3.0),
        xlabel=r"frequency ratio $r = \omega/\omega_n$",
        ylabel=r"magnification $X k / F_0$",
        title="(b) Magnification factor of harmonic forcing",
    )
    ax_mag.legend(fontsize=9, loc="upper right")
    ax_phase.set(
        xlim=(0.0, 3.0),
        ylim=(0.0, 180.0),
        yticks=np.arange(0, 181, 45),
        xlabel=r"frequency ratio $r = \omega/\omega_n$",
        ylabel=r"phase lag $\phi$ (deg)",
        title="(c) Phase lag of displacement behind force",
    )
    ax_phase.legend(fontsize=9, loc="lower right")
    ax_tr.axvline(np.sqrt(2.0), color="0.3", linestyle="--", linewidth=1.0)
    ax_tr.axhline(1.0, color="0.3", linewidth=0.8)
    ax_tr.text(1.47, 0.1, r"$r = \sqrt{2}$: isolation begins", fontsize=10)
    ax_tr.set(
        yscale="log",
        ylim=(0.08, 20.0),
        xlim=(0.0, 3.0),
        xlabel=r"frequency ratio $r = \omega/\omega_n$",
        ylabel=r"transmissibility $X/Y$ or $F_T/F_0$",
        title="(d) Transmissibility of base excitation",
    )
    ax_tr.legend(fontsize=9, loc="upper right")
    for ax in axes.flat:
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t, results = free_decay_study()
    print(f"k = {STIFFNESS:.2f} N/m, omega_n = {np.sqrt(STIFFNESS / MASS):.4f} rad/s")
    for zeta, (x_exact, x_num) in results.items():
        error = np.max(np.abs(x_num - x_exact)) / X0
        print(f"zeta = {zeta:3g}: max |Newmark - exact| / x0 = {error:.2e}")
    for zeta in FRF_ZETAS:
        rp = peak_frequency_ratio(zeta)
        if np.isfinite(rp):
            print(
                f"zeta = {zeta:.3f}: peak at r = {rp:.4f}, "
                f"M_max = {magnification(rp, zeta):.3f}, 1/(2 zeta) = {0.5 / zeta:.3f}"
            )
        else:
            print(f"zeta = {zeta:.3f}: no resonance peak, M decreases from 1")

    finish_figures(
        {"dynamics_sdof_response.png": make_figure(t, results)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
