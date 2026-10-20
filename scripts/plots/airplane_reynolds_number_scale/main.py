"""Chord Reynolds numbers of flyers from fruit flies to airliners.

Computes Re = V c / nu for a range of flight speeds V and a typical mean wing
chord c of each flyer (sea-level air, except the airliner at cruise), draws
the ranges on a logarithmic axis with the band in which laminar separation
and transition dominate airfoil behaviour shaded, and plots the flat-plate
skin-friction coefficient of laminar, turbulent and transitional boundary
layers over the same Reynolds-number range.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

RHO_SL = 1.225  # kg/m^3, sea-level density (ISA)
MU_SL = 1.789e-5  # Pa s, sea-level dynamic viscosity (ISA)
RHO_CRUISE = 0.364  # kg/m^3 at 11 km (ISA)
MU_CRUISE = 1.422e-5  # Pa s at 11 km (ISA, 216.65 K)
NU_SL = MU_SL / RHO_SL  # m^2/s
NU_CRUISE = MU_CRUISE / RHO_CRUISE  # m^2/s

# (name, mean chord in m, lowest and highest speed in m/s, kinematic viscosity).
# Insect speeds are wing speeds in flapping flight, not body speeds.
FLYERS = (
    ("Fruit fly", 0.0008, 1.5, 3.0, NU_SL),
    ("Honeybee", 0.003, 5.0, 7.0, NU_SL),
    ("Dragonfly", 0.008, 3.0, 8.0, NU_SL),
    ("Hummingbird", 0.012, 5.0, 10.0, NU_SL),
    ("Sparrow", 0.05, 8.0, 12.0, NU_SL),
    ("Pigeon", 0.10, 10.0, 20.0, NU_SL),
    ("Model glider", 0.20, 8.0, 15.0, NU_SL),
    ("Albatross", 0.20, 10.0, 25.0, NU_SL),
    ("Small UAV", 0.30, 15.0, 30.0, NU_SL),
    ("Sailplane", 0.65, 25.0, 60.0, NU_SL),
    ("Hang glider", 1.5, 8.0, 25.0, NU_SL),
    ("Light aircraft", 1.5, 26.0, 60.0, NU_SL),
    ("Airliner, take-off", 5.0, 75.0, 85.0, NU_SL),
    ("Airliner, cruise 11 km", 5.0, 220.0, 250.0, NU_CRUISE),
)
LOW_RE_BAND = (5e4, 1e6)  # separation bubbles and transition dominate
RE_CRIT_PLATE = 5e5  # flat-plate transition Reynolds number


def reynolds(speed, chord, nu=NU_SL):
    """Chord Reynolds number V c / nu."""
    return np.asarray(speed) * chord / nu


def flyer_ranges(flyers=FLYERS):
    """List of (name, Re_low, Re_high)."""
    return [
        (n, reynolds(v1, c, nu), reynolds(v2, c, nu)) for n, c, v1, v2, nu in flyers
    ]


def cf_laminar(re):
    """Blasius mean skin friction of a laminar flat plate."""
    return 1.328 / np.sqrt(re)


def cf_turbulent(re):
    """Prandtl one-seventh-power mean skin friction, turbulent from the edge."""
    return 0.074 / re**0.2


def cf_transitional(re, re_crit=RE_CRIT_PLATE):
    """Laminar up to re_crit, then turbulent (Prandtl-Schlichting correction)."""
    re = np.asarray(re, dtype=float)
    a = re_crit * (0.074 / re_crit**0.2 - 1.328 / np.sqrt(re_crit))
    return np.where(re < re_crit, cf_laminar(re), cf_turbulent(re) - a / re)


def plot_scale():
    ranges = flyer_ranges()
    fig, axes = plt.subplots(
        1, 2, figsize=(13, 5.6), gridspec_kw=dict(width_ratios=[1.25, 1])
    )
    ax = axes[0]
    colours = plt.cm.viridis(np.linspace(0, 0.9, len(ranges)))
    for i, ((name, lo, hi), colour) in enumerate(zip(ranges, colours, strict=True)):
        ax.plot([lo, hi], [i, i], lw=7, color=colour, solid_capstyle="round")
        ax.text(hi * 1.4, i, name, va="center", fontsize=10)
    ax.axvspan(*LOW_RE_BAND, color="tab:orange", alpha=0.15)
    ax.text(
        np.sqrt(LOW_RE_BAND[0] * LOW_RE_BAND[1]),
        len(ranges) - 0.3,
        "laminar separation\nand transition",
        ha="center",
        va="top",
        fontsize=9,
        color="tab:orange",
    )
    ax.set_xscale("log")
    ax.set_xlim(30, 1e9)
    ax.set_ylim(-0.8, len(ranges) - 0.2)
    ax.set_yticks([])
    ax.set_xlabel(r"Chord Reynolds number $Re_c = Vc/\nu$")
    ax.set_title("(a) Reynolds numbers of flyers")
    ax.grid(axis="x", which="major", alpha=0.3)

    ax = axes[1]
    re = np.logspace(4, 8.5, 400)
    ax.plot(re, cf_laminar(re), color="tab:blue", label=r"Laminar, $1.328/\sqrt{Re}$")
    ax.plot(re, cf_turbulent(re), color="tab:red", label=r"Turbulent, $0.074/Re^{1/5}$")
    ax.plot(
        re,
        cf_transitional(re),
        "--",
        color="0.2",
        label=r"Transition at $Re = 5 \times 10^5$",
    )
    ax.axvspan(*LOW_RE_BAND, color="tab:orange", alpha=0.15)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 2e-2)
    ax.set_xlabel(r"Plate Reynolds number $Re_L$")
    ax.set_ylabel("Mean skin-friction coefficient $C_f$")
    ax.set_title("(b) Flat-plate skin friction")
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(which="both", alpha=0.3)
    fig.tight_layout()
    return fig, ranges


def main(argv=None):
    args = create_parser(__doc__).parse_args(argv)
    fig, ranges = plot_scale()
    print(f"nu at sea level = {NU_SL:.3e} m^2/s, at 11 km = {NU_CRUISE:.3e} m^2/s")
    for name, lo, hi in ranges:
        print(f"  {name:24s} Re = {lo:9.3g} to {hi:9.3g}")
    finish_figures(
        {"airplane_reynolds_number_scale.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
