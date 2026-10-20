"""Yield and fracture envelopes in the plane-stress principal-stress plane.

Panel (a) draws the Tresca hexagon and the von Mises ellipse for a ductile
steel, panel (b) the maximum-normal-stress rectangle and the Coulomb-Mohr
envelope for a brittle grey cast iron whose compressive strength is several
times its tensile strength. Three load points are plotted in each panel, each
with the radial load line from the origin to the envelope; the safety factor
of a criterion is the ratio of the distance to the envelope to the distance
to the point, so it is printed for every point and criterion.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SIGMA_Y = 250.0e6  # yield strength of the ductile steel (Pa)
S_UT = 214.0e6  # ultimate tensile strength of grey cast iron, ASTM class 30 (Pa)
S_UC = 752.0e6  # ultimate compressive strength of the same iron (Pa)

MPA = 1.0e6
# (label, sigma_1, sigma_2) in Pa; sigma_3 = 0 in plane stress.
DUCTILE_POINTS = [
    ("A: shaft, bending + torsion", 107.7 * MPA, -9.9 * MPA),
    ("B: pressure vessel with axial load", 100.0 * MPA, 64.9 * MPA),
    ("C: pure shear, $\\tau$ = 120 MPa", 120.0 * MPA, -120.0 * MPA),
]
BRITTLE_POINTS = [
    ("D: uniaxial tension 100 MPa", 100.0 * MPA, 0.0),
    ("E: pure shear, $\\tau$ = 120 MPa", 120.0 * MPA, -120.0 * MPA),
    ("F: 50 MPa tension, 400 MPa compression", 50.0 * MPA, -400.0 * MPA),
]


def von_mises(s1, s2):
    """Von Mises equivalent stress in plane stress (Pa)."""
    return np.sqrt(s1**2 - s1 * s2 + s2**2)


def tresca(s1, s2):
    """Twice the absolute maximum shear stress, including sigma_3 = 0 (Pa)."""
    return np.maximum.reduce([np.abs(s1), np.abs(s2), np.abs(s1 - s2)])


def safety_von_mises(s1, s2, sy=SIGMA_Y):
    return sy / von_mises(s1, s2)


def safety_tresca(s1, s2, sy=SIGMA_Y):
    return sy / tresca(s1, s2)


def safety_max_normal(s1, s2, sut=S_UT, suc=S_UC):
    """Maximum-normal-stress (Rankine) safety factor for a brittle material."""
    limits = []
    for s in (s1, s2):
        if s > 0:
            limits.append(sut / s)
        elif s < 0:
            limits.append(suc / -s)
    return min(limits)


def safety_coulomb_mohr(s1, s2, sut=S_UT, suc=S_UC):
    """Brittle Coulomb-Mohr safety factor; s1 and s2 in any order."""
    sa, sb = max(s1, s2), min(s1, s2)
    if sb >= 0:
        return sut / sa
    if sa <= 0:
        return suc / -sb
    return 1.0 / (sa / sut - sb / suc)


def envelope_point(safety, s1, s2):
    """Point where the radial load line through (s1, s2) meets the envelope."""
    n = safety(s1, s2)
    return n * s1, n * s2


def plot_points(ax, points, criteria, colors):
    """Plot load points, their radial lines and a legend entry with safety factors."""
    for (label, s1, s2), color in zip(points, colors, strict=True):
        factors = [(name, safety(s1, s2)) for name, safety in criteria]
        reach = max(n for _, n in factors)
        ax.plot([0, reach * s1 / MPA], [0, reach * s2 / MPA], ":", color=color, lw=1.2)
        for _, safety in criteria:
            e1, e2 = envelope_point(safety, s1, s2)
            ax.plot(e1 / MPA, e2 / MPA, "x", color=color, ms=7, mew=1.8)
        text = ", ".join(f"n$_{{{name}}}$ = {n:.2f}" for name, n in factors)
        ax.plot(s1 / MPA, s2 / MPA, "o", color=color, ms=8, label=f"{label}\n{text}")


def ductile_panel(ax):
    """Tresca hexagon and von Mises ellipse."""
    sy = SIGMA_Y / MPA
    hexagon = np.array(
        [[sy, 0], [sy, sy], [0, sy], [-sy, 0], [-sy, -sy], [0, -sy], [sy, 0]]
    )
    ax.plot(*hexagon.T, color="tab:blue", lw=2.2, label="Tresca (max shear stress)")
    # Parametrise the ellipse s1^2 - s1 s2 + s2^2 = sy^2 along its principal axes.
    t = np.linspace(0, 2 * np.pi, 400)
    a, b = np.sqrt(2) * sy, np.sqrt(2 / 3) * sy
    u, v = a * np.cos(t), b * np.sin(t)
    ax.plot(
        (u - v) / np.sqrt(2),
        (u + v) / np.sqrt(2),
        color="tab:orange",
        lw=2.2,
        label="von Mises (distortion energy)",
    )
    plot_points(
        ax,
        DUCTILE_POINTS,
        [("T", safety_tresca), ("vM", safety_von_mises)],
        ["tab:green", "tab:red", "tab:purple"],
    )
    lim = 1.45 * sy
    ax.set(
        xlim=(-lim, lim),
        ylim=(-lim, lim),
        title=rf"(a) Ductile steel, $\sigma_Y$ = {sy:.0f} MPa",
    )


def brittle_panel(ax):
    """Maximum normal stress rectangle and Coulomb-Mohr envelope."""
    t, c = S_UT / MPA, S_UC / MPA
    rect = np.array([[t, t], [-c, t], [-c, -c], [t, -c], [t, t]])
    ax.plot(*rect.T, color="tab:blue", lw=2.2, label="maximum normal stress")
    mohr = np.array([[t, t], [t, 0], [0, -c], [-c, -c], [-c, 0], [0, t], [t, t]])
    ax.plot(*mohr.T, color="tab:orange", lw=2.2, label="Coulomb-Mohr")
    plot_points(
        ax,
        BRITTLE_POINTS,
        [("MNS", safety_max_normal), ("CM", safety_coulomb_mohr)],
        ["tab:green", "tab:red", "tab:purple"],
    )
    ax.set(
        xlim=(-1.1 * c, 1.5 * t),
        ylim=(-1.1 * c, 1.5 * t),
        title=f"(b) Grey cast iron, $S_{{ut}}$ = {t:.0f} MPa, $S_{{uc}}$ = {c:.0f} MPa",
    )


def make_figure():
    fig, axes = plt.subplots(1, 2, figsize=(13, 8.6))
    ductile_panel(axes[0])
    brittle_panel(axes[1])
    for ax in axes:
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(0, color="0.4", lw=0.8)
        ax.plot([-1e4, 1e4], [-1e4, 1e4], color="0.8", lw=0.8, zorder=0)
        ax.set(
            aspect="equal",
            xlabel=r"$\sigma_1$ (MPa)",
            ylabel=r"$\sigma_2$ (MPa)",
        )
        ax.grid(True, lw=0.5, alpha=0.5)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=9.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for label, s1, s2 in DUCTILE_POINTS:
        label = label.replace("$\\tau$", "tau")
        print(
            f"{label}: von Mises {von_mises(s1, s2) / MPA:.1f} MPa, "
            f"n_vM = {safety_von_mises(s1, s2):.3f}, n_Tresca = {safety_tresca(s1, s2):.3f}"
        )
    for label, s1, s2 in BRITTLE_POINTS:
        label = label.replace("$\\tau$", "tau")
        print(
            f"{label}: n_maxnormal = {safety_max_normal(s1, s2):.3f}, "
            f"n_CoulombMohr = {safety_coulomb_mohr(s1, s2):.3f}"
        )

    finish_figures(
        {"beams_failure_envelopes.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
