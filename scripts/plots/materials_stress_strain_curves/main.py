"""Draw model engineering and true stress-strain curves of a ductile and a brittle material.

The ductile metal follows a Ramberg-Osgood law between true stress and true
strain, eps = sigma/E + 0.002 (sigma/sigma_02)^n, while the deformation is
uniform. Engineering stress and strain follow from constant volume, the
ultimate tensile strength is the maximum of the engineering curve (the
Considere condition), and the drop after necking is drawn as a schematic
curve to fracture. The left panel shows both curves with the toughness area
shaded; the right panel zooms on small strains to show the 0.2 % offset
construction, the modulus of resilience and a brittle material that is linear
to fracture.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Ductile metal model (structural-steel-like values, not a specific grade)
E_DUCTILE = 200e3  # Young's modulus (MPa)
SIGMA_02 = 350.0  # 0.2 % offset yield strength (MPa)
N_RO = 8.0  # Ramberg-Osgood exponent (-)
OFFSET = 0.002  # plastic strain of the offset construction (-)
STRAIN_FRACTURE = 0.30  # engineering strain at fracture (-)
FRACTURE_RATIO = 0.80  # engineering stress at fracture / UTS (-), schematic

# Brittle material model: linear elastic to fracture
E_BRITTLE = 120e3  # Young's modulus (MPa)
SIGMA_FRACTURE_BRITTLE = 300.0  # fracture strength (MPa)


def ramberg_osgood_strain(sigma, modulus=E_DUCTILE, sigma_02=SIGMA_02, n=N_RO):
    """Return total strain for stress sigma (MPa) from the Ramberg-Osgood law."""
    sigma = np.asarray(sigma, dtype=float)
    return sigma / modulus + OFFSET * np.abs(sigma / sigma_02) ** n * np.sign(sigma)


def offset_yield(modulus=E_DUCTILE, sigma_02=SIGMA_02, n=N_RO, offset=OFFSET):
    """Return the stress where the line sigma = E (eps - offset) meets the curve."""

    def gap(sigma):
        return ramberg_osgood_strain(sigma, modulus, sigma_02, n) - (
            sigma / modulus + offset
        )

    return brentq(gap, 1e-6 * sigma_02, 10.0 * sigma_02)


def true_curve(sigma_max=None, points=4000):
    """Return true strain and true stress arrays of the ductile model."""
    if sigma_max is None:
        sigma_max = 3.0 * SIGMA_02
    sigma_true = np.linspace(0.0, sigma_max, points)
    return ramberg_osgood_strain(sigma_true), sigma_true


def engineering_from_true(eps_true, sigma_true):
    """Convert true to engineering values assuming uniform, constant-volume strain."""
    eps_eng = np.expm1(eps_true)
    return eps_eng, sigma_true / (1.0 + eps_eng)


def ultimate_point():
    """Return (engineering strain, UTS, true strain, true stress) at necking."""
    eps_t, sig_t = true_curve()
    eps_e, sig_e = engineering_from_true(eps_t, sig_t)
    i = int(np.argmax(sig_e))
    return eps_e[i], sig_e[i], eps_t[i], sig_t[i]


def engineering_curve(points=600):
    """Return the full engineering curve: model to UTS, schematic drop to fracture."""
    eps_u, uts, _, sigma_u_true = ultimate_point()
    eps_t, sig_t = true_curve(sigma_u_true)
    eps_pre, sig_pre = engineering_from_true(eps_t, sig_t)
    eps_post = np.linspace(eps_u, STRAIN_FRACTURE, points)[1:]
    s = (eps_post - eps_u) / (STRAIN_FRACTURE - eps_u)
    sig_post = uts - (1.0 - FRACTURE_RATIO) * uts * s**2
    return eps_pre, sig_pre, eps_post, sig_post


def toughness(eps, sigma):
    """Return the area under a stress-strain curve (MPa = MJ/m^3)."""
    return float(np.trapezoid(sigma, eps))


def make_figure():
    """Draw the full curves and the small-strain detail."""
    eps_u, uts, eps_u_true, sig_u_true = ultimate_point()
    eps_pre, sig_pre, eps_post, sig_post = engineering_curve()
    eps_eng = np.concatenate([eps_pre, eps_post])
    sig_eng = np.concatenate([sig_pre, sig_post])
    eps_t, sig_t = true_curve(sig_u_true)
    eps_t_ext, sig_t_ext = true_curve(1.6 * sig_u_true)
    keep = (eps_t_ext >= eps_u_true) & (eps_t_ext <= np.log1p(STRAIN_FRACTURE))
    sy = offset_yield()
    eps_bf = SIGMA_FRACTURE_BRITTLE / E_BRITTLE

    fig, (full, zoom) = plt.subplots(1, 2, figsize=(13, 5.6))

    full.fill_between(
        eps_eng,
        sig_eng,
        color="tab:blue",
        alpha=0.15,
        label=f"toughness = {toughness(eps_eng, sig_eng):.0f} MJ/m$^3$",
    )
    full.plot(eps_pre, sig_pre, color="tab:blue", lw=2, label="engineering (model)")
    full.plot(
        eps_post,
        sig_post,
        color="tab:blue",
        lw=2,
        ls="--",
        label="engineering after necking (schematic)",
    )
    full.plot(eps_t, sig_t, color="tab:orange", lw=2, label="true (model)")
    full.plot(
        eps_t_ext[keep],
        sig_t_ext[keep],
        color="tab:orange",
        lw=1.5,
        ls=":",
        label="true, model extrapolated past necking",
    )
    full.plot(eps_u, uts, "o", color="tab:red", ms=7)
    full.annotate(
        f"UTS = {uts:.0f} MPa\nnecking at e = {eps_u:.3f}",
        (eps_u, uts),
        xytext=(eps_u - 0.06, uts + 110),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    full.plot(STRAIN_FRACTURE, sig_post[-1], "x", color="tab:red", ms=9, mew=2)
    full.annotate(
        "fracture",
        (STRAIN_FRACTURE, sig_post[-1]),
        xytext=(STRAIN_FRACTURE - 0.05, sig_post[-1] - 90),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    full.plot(
        [0, eps_bf],
        [0, SIGMA_FRACTURE_BRITTLE],
        color="tab:gray",
        lw=2,
        label="brittle (linear to fracture)",
    )
    full.set(
        xlim=(0, 0.32),
        ylim=(0, 800),
        xlabel=r"strain (-): engineering $e$ (blue), true $\varepsilon$ (orange)",
        ylabel="stress (MPa)",
        title=rf"Ductile metal: Ramberg-Osgood, $n$ = {N_RO:.0f}",
    )
    full.legend(loc="lower right", fontsize=9)

    # Small-strain detail
    eps_z = np.linspace(0.0, 0.012, 400)
    sig_grid = np.linspace(0.0, 1.3 * SIGMA_02, 2000)
    eps_grid = ramberg_osgood_strain(sig_grid)
    resilience = sy**2 / (2.0 * E_DUCTILE)
    zoom.fill_between(
        [0, sy / E_DUCTILE],
        [0, sy],
        color="tab:green",
        alpha=0.25,
        label=rf"resilience $\sigma_y^2/2E$ = {resilience:.2f} MJ/m$^3$",
    )
    zoom.plot(eps_grid, sig_grid, color="tab:blue", lw=2, label="ductile model")
    zoom.plot(
        eps_z,
        E_DUCTILE * (eps_z - OFFSET),
        color="tab:green",
        lw=1.2,
        ls="--",
        label="0.2 % offset line, slope $E$",
    )
    zoom.plot(
        eps_z,
        E_DUCTILE * eps_z,
        color="0.5",
        lw=0.8,
        ls=":",
        label=rf"$\sigma = E\varepsilon$, $E$ = {E_DUCTILE / 1e3:.0f} GPa",
    )
    zoom.plot(sy / E_DUCTILE + OFFSET, sy, "o", color="tab:green", ms=7)
    zoom.annotate(
        rf"$\sigma_{{0.2}}$ = {sy:.0f} MPa",
        (sy / E_DUCTILE + OFFSET, sy),
        xytext=(0.0062, 260),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    zoom.plot(
        [0, eps_bf],
        [0, SIGMA_FRACTURE_BRITTLE],
        color="tab:gray",
        lw=2,
        label=f"brittle, $E$ = {E_BRITTLE / 1e3:.0f} GPa",
    )
    zoom.plot(eps_bf, SIGMA_FRACTURE_BRITTLE, "x", color="tab:red", ms=9, mew=2)
    zoom.annotate(
        rf"fracture at $\varepsilon$ = {eps_bf:.4f}",
        (eps_bf, SIGMA_FRACTURE_BRITTLE),
        xytext=(0.0032, 120),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    zoom.set(
        xlim=(0, 0.012),
        ylim=(0, 450),
        xlabel="strain (-)",
        ylabel="stress (MPa)",
        title="Small strains: offset yield and resilience",
    )
    zoom.legend(loc="lower right", fontsize=9)
    for ax in (full, zoom):
        ax.grid(True, lw=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    eps_u, uts, eps_u_true, sig_u_true = ultimate_point()
    eps_pre, sig_pre, eps_post, sig_post = engineering_curve()
    u_t = toughness(
        np.concatenate([eps_pre, eps_post]), np.concatenate([sig_pre, sig_post])
    )
    sy = offset_yield()
    eps_bf = SIGMA_FRACTURE_BRITTLE / E_BRITTLE
    print(f"0.2 % offset yield = {sy:.1f} MPa (model parameter {SIGMA_02:.0f} MPa)")
    print(
        f"UTS = {uts:.1f} MPa at engineering strain {eps_u:.4f} "
        f"(true strain {eps_u_true:.4f}, true stress {sig_u_true:.1f} MPa)"
    )
    print(
        f"toughness = {u_t:.1f} MJ/m^3, resilience = {sy**2 / (2 * E_DUCTILE):.3f} MJ/m^3"
    )
    print(
        f"brittle: fracture strain {eps_bf:.4f}, toughness "
        f"{0.5 * SIGMA_FRACTURE_BRITTLE * eps_bf:.3f} MJ/m^3"
    )

    finish_figures(
        {"materials_stress_strain_curves.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
