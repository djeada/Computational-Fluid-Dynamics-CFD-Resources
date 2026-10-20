"""Pierson-Moskowitz and JONSWAP wave spectra and a random-phase sea surface.

Evaluates the two-parameter Pierson-Moskowitz spectrum in terms of the
significant wave height H_s and peak period T_p, and the JONSWAP spectrum for
several peak-enhancement factors gamma, each normalised so that its zeroth
moment equals H_s^2 / 16. It prints the spectral moments, the mean
zero-crossing period and the normalising factor, and synthesises a seeded
random-phase time series of the surface elevation from the JONSWAP spectrum.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

HS = 4.0  # significant wave height (m)
TP = 9.0  # peak period (s)
GAMMAS = (1.0, 3.3, 7.0)  # JONSWAP peak-enhancement factors (gamma = 1 is PM)
SIGMA_LOW, SIGMA_HIGH = 0.07, 0.09  # JONSWAP peak widths below/above omega_p
OMEGA_MAX = 40.0  # upper integration limit (rad/s); keeps the m_2 tail below 0.1%
N_OMEGA = 40000  # frequency points for the moments
N_COMPONENTS = 400  # harmonic components in the synthesised record
DURATION = 1200.0  # length of the synthesised record (s)
SEED = 4


def pierson_moskowitz(omega, hs=HS, tp=TP):
    """S(omega) = (5/16) H_s^2 w_p^4 w^-5 exp(-1.25 (w_p/w)^4) in m^2 s/rad."""
    omega = np.asarray(omega, dtype=float)
    wp = 2.0 * np.pi / tp
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        s = 5.0 / 16.0 * hs**2 * wp**4 * omega**-5 * np.exp(-1.25 * (wp / omega) ** 4)
    return np.where(omega > 0, s, 0.0)


def peak_enhancement(omega, gamma, tp=TP):
    """JONSWAP factor gamma^exp(-(w - w_p)^2 / (2 sigma^2 w_p^2))."""
    wp = 2.0 * np.pi / tp
    sigma = np.where(omega <= wp, SIGMA_LOW, SIGMA_HIGH)
    return gamma ** np.exp(-((omega - wp) ** 2) / (2.0 * sigma**2 * wp**2))


def spectral_moment(omega, s, n):
    """m_n = integral of omega^n S(omega) d omega (trapezoidal rule)."""
    return np.trapezoid(omega**n * s, omega)


def jonswap(omega, gamma, hs=HS, tp=TP):
    """JONSWAP spectrum normalised so that m_0 = H_s^2 / 16.

    Returns (S(omega), A_gamma), where A_gamma is the factor applied to the
    PM spectrum times the peak enhancement to restore the target m_0.
    """
    grid = np.linspace(1e-3, OMEGA_MAX, N_OMEGA)
    raw = pierson_moskowitz(grid, hs, tp) * peak_enhancement(grid, gamma, tp)
    a_gamma = hs**2 / 16.0 / spectral_moment(grid, raw, 0)
    s = a_gamma * pierson_moskowitz(omega, hs, tp) * peak_enhancement(omega, gamma, tp)
    return s, a_gamma


def random_sea(gamma, duration=DURATION, n_comp=N_COMPONENTS, seed=SEED, dt=0.25):
    """Surface elevation eta(t) = sum a_i cos(w_i t + phi_i), a_i = sqrt(2 S dw).

    Uses equally spaced frequencies with seeded uniform random phases.
    """
    rng = np.random.default_rng(seed)
    omega = np.linspace(0.2, 3.0, n_comp)
    d_omega = omega[1] - omega[0]
    s, _ = jonswap(omega, gamma)
    amp = np.sqrt(2.0 * s * d_omega)
    phase = rng.uniform(0.0, 2.0 * np.pi, n_comp)
    t = np.arange(0.0, duration, dt)
    eta = (amp[:, None] * np.cos(omega[:, None] * t[None, :] + phase[:, None])).sum(0)
    return t, eta


def make_figure(omega, spectra, t, eta, hs_sample):
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), width_ratios=(1, 1.3))
    ax = axes[0]
    colors = ("tab:blue", "tab:orange", "tab:green")
    for (gamma, s), c in zip(spectra.items(), colors):
        label = "Pierson-Moskowitz ($\\gamma$ = 1)" if gamma == 1 else None
        label = label or f"JONSWAP $\\gamma$ = {gamma:g}"
        ax.plot(omega, s, color=c, lw=2, label=label)
    ax.axvline(2 * np.pi / TP, color="0.4", ls="--", lw=1)
    ax.text(2 * np.pi / TP + 0.03, 0.2, "$\\omega_p = 2\\pi/T_p$", fontsize=10)
    ax.set_xlim(0, 2.0)
    ax.set_xlabel("Angular frequency $\\omega$ (rad/s)", fontsize=11)
    ax.set_ylabel("$S(\\omega)$ (m$^2$ s/rad)", fontsize=11)
    ax.set_title(
        f"(a) Spectra with equal $H_s$ = {HS:g} m, $T_p$ = {TP:g} s", fontsize=12
    )
    ax.legend(fontsize=10)
    ax.grid(True, ls="--", lw=0.5, alpha=0.6)

    ax = axes[1]
    window = t <= 300.0
    ax.plot(t[window], eta[window], color="tab:blue", lw=1)
    ax.axhline(HS / 2, color="tab:red", ls="--", lw=1, label="$\\pm H_s/2$")
    ax.axhline(-HS / 2, color="tab:red", ls="--", lw=1)
    ax.set_xlim(0, 300)
    ax.set_ylim(-3.6, 3.6)
    ax.set_xlabel("Time $t$ (s)", fontsize=11)
    ax.set_ylabel("Surface elevation $\\eta$ (m)", fontsize=11)
    ax.set_title(
        f"(b) JONSWAP $\\gamma$ = 3.3 sea, first 300 s (record $4\\sigma_\\eta$ = "
        f"{hs_sample:.2f} m)",
        fontsize=12,
    )
    ax.legend(fontsize=10, loc="upper right", ncol=1)
    ax.grid(True, ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    omega = np.linspace(1e-3, OMEGA_MAX, N_OMEGA)
    spectra = {}
    for gamma in GAMMAS:
        s, a_gamma = jonswap(omega, gamma)
        spectra[gamma] = s
        m0, m1, m2 = (spectral_moment(omega, s, n) for n in (0, 1, 2))
        print(
            f"gamma = {gamma:3.1f}: A_gamma = {a_gamma:.4f} "
            f"(1 - 0.287 ln gamma = {1 - 0.287 * np.log(gamma):.4f}), "
            f"4 sqrt(m0) = {4 * np.sqrt(m0):.3f} m, T_m01 = {2 * np.pi * m0 / m1:.2f} s, "
            f"T_z = {2 * np.pi * np.sqrt(m0 / m2):.2f} s, peak S = {s.max():.3f} m^2 s"
        )
    t, eta = random_sea(3.3)
    hs_sample = 4.0 * eta.std()
    print(f"synthesised {DURATION:.0f} s record: 4 std(eta) = {hs_sample:.3f} m")

    fig = make_figure(omega, spectra, t, eta, hs_sample)
    finish_figures(
        {"fluid_loading_wave_spectra.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
