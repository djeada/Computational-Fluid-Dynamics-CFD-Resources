"""Draw an annotated NACA 4-digit airfoil profile (default NACA 4412).

Parses the four-digit code, computes the mean camber line and the standard
NACA thickness distribution, offsets the surfaces perpendicular to the camber
line, and labels the leading edge, trailing edge, chord line and camber line.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

DEFAULT_CODE = "4412"  # 4 % camber at 40 % chord, 12 % thickness
CHORD = 1.0  # chord length (unit length for simplicity)
N_POINTS = 500  # chordwise stations


def parse_naca4(code):
    """Return (m, p, t) as chord fractions from a 4-digit NACA code."""
    if len(code) != 4 or not code.isdigit():
        raise ValueError(f"expected a 4-digit NACA code, got {code!r}")
    return int(code[0]) / 100, int(code[1]) / 10, int(code[2:]) / 100


def camber_line(x, m, p, c=1.0):
    """Piecewise parabolic mean camber line y_c(x) and its slope dy_c/dx."""
    xc = x / c
    if m == 0 or p == 0:
        return np.zeros_like(x), np.zeros_like(x)
    yc = c * np.where(
        xc < p,
        m / p**2 * (2 * p * xc - xc**2),
        m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * xc - xc**2),
    )
    dyc_dx = np.where(xc < p, 2 * m / p**2 * (p - xc), 2 * m / (1 - p) ** 2 * (p - xc))
    return yc, dyc_dx


def thickness_distribution(x, t, c=1.0):
    """NACA 4-digit half-thickness y_t(x) for maximum thickness ratio t."""
    xc = x / c
    return (
        (t / 0.2)
        * c
        * (
            0.2969 * np.sqrt(xc)
            - 0.1260 * xc
            - 0.3516 * xc**2
            + 0.2843 * xc**3
            - 0.1015 * xc**4
        )
    )


def naca4_geometry(code, c=1.0, n=500):
    """Chordwise stations, camber line and upper/lower surface coordinates."""
    m, p, t = parse_naca4(code)
    x = np.linspace(0, c, n)
    yc, dyc_dx = camber_line(x, m, p, c)
    yt = thickness_distribution(x, t, c)
    theta = np.arctan(dyc_dx)
    xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
    xl, yl = x + yt * np.sin(theta), yc - yt * np.cos(theta)
    return x, yc, (xu, yu), (xl, yl)


def plot_airfoil(code, c=1.0, n=500):
    x, yc, (xu, yu), (xl, yl) = naca4_geometry(code, c, n)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xu, yu, color="gray", label="Upper Surface")
    ax.plot(xl, yl, color="gray", label="Lower Surface")
    ax.plot([0, c], [0, 0], "yellow", lw=2, label="Chord Line")
    ax.plot(x, yc, "r--", lw=2, label="Mean Camber Line")

    box = dict(facecolor="lightgray", edgecolor="black")
    ax.text(-0.02 * c, 0.1 * c, "Leading edge", fontsize=12, bbox=box, ha="left")
    ax.text(0.98 * c, 0.1 * c, "Trailing edge", fontsize=12, bbox=box, ha="right")
    ax.text(
        0.5 * c,
        -0.03 * c,
        "Chord line",
        fontsize=12,
        bbox=dict(facecolor="yellow", edgecolor="black"),
        ha="center",
    )
    ax.text(
        0.5 * c,
        0.18 * c,
        "Mean camber line",
        fontsize=12,
        bbox=dict(facecolor="orange", edgecolor="black"),
        ha="center",
    )
    ax.text(0.25 * c, 0.13 * c, "Upper surface", fontsize=10, ha="center")
    ax.text(0.25 * c, -0.1 * c, "Lower surface", fontsize=10, ha="center")

    ax.set_xlim(-0.1 * c, 1.1 * c)
    ax.set_ylim(-0.35 * c, 0.35 * c)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"NACA {code} Airfoil Profile")
    ax.legend()
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--naca",
        default=DEFAULT_CODE,
        metavar="CODE",
        help=f"four-digit NACA designation (default: {DEFAULT_CODE})",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    fig = plot_airfoil(args.naca, CHORD, N_POINTS)

    finish_figures(
        {"airfoil_profile.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
