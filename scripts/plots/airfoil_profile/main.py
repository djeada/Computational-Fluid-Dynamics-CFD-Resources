"""Draw an annotated NACA 4-digit airfoil profile (default NACA 4412).

Parses the four-digit code, computes the mean camber line and the standard
NACA thickness distribution, offsets the surfaces perpendicular to the camber
line, and annotates the chord, the maximum camber and thickness and the
leading-edge radius. A second panel compares NACA 0012, 2412, 4412 and 4421.
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


def leading_edge_radius(t, c=1.0):
    """Leading-edge radius of the NACA 4-digit thickness form, 1.1019 t^2 c."""
    return 1.1019 * t**2 * c


def max_thickness_location(t, c=1.0, n=2001):
    """Chordwise station and value of the maximum half-thickness y_t."""
    x = np.linspace(0, c, n)
    yt = thickness_distribution(x, t, c)
    i = np.argmax(yt)
    return x[i], 2 * yt[i]


def _dimension(ax, p0, p1, text, offset=(0, 0), colour="0.2", **kw):
    ax.annotate(
        "",
        xy=p1,
        xytext=p0,
        arrowprops=dict(arrowstyle="<->", color=colour, lw=1.2),
    )
    mid = (0.5 * (p0[0] + p1[0]) + offset[0], 0.5 * (p0[1] + p1[1]) + offset[1])
    ax.text(*mid, text, color=colour, fontsize=10, **kw)


def plot_airfoil(code, c=1.0, n=500):
    m, p, t = parse_naca4(code)
    x, yc, (xu, yu), (xl, yl) = naca4_geometry(code, c, n)
    fig, axes = plt.subplots(
        2, 1, figsize=(11, 7.5), gridspec_kw=dict(height_ratios=[1.6, 1])
    )

    ax = axes[0]
    ax.fill(np.r_[xu, xl[::-1]], np.r_[yu, yl[::-1]], color="0.88")
    ax.plot(xu, yu, color="0.2", lw=1.5, label="Upper and lower surfaces")
    ax.plot(xl, yl, color="0.2", lw=1.5)
    ax.plot([0, c], [0, 0], color="tab:blue", lw=1.5, label="Chord line")
    ax.plot(x, yc, "--", color="tab:red", lw=2, label="Mean camber line")

    # Leading-edge circle, centred on the line through the nose with the
    # camber-line slope at x = 0.
    r = leading_edge_radius(t, c)
    slope0 = 2 * m / p if p > 0 else 0.0
    centre = r * np.array([np.cos(np.arctan(slope0)), np.sin(np.arctan(slope0))])
    ax.add_patch(
        plt.Circle(
            centre, r, fill=False, ec="tab:green", lw=1.2, label="Leading-edge radius"
        )
    )
    ax.text(
        0.0,
        -0.075 * c,
        f"LE radius\n{r / c * 100:.2f} % c",
        color="tab:green",
        fontsize=10,
        ha="left",
    )

    _dimension(
        ax,
        (0, -0.13 * c),
        (c, -0.13 * c),
        f"chord c = {c:g}",
        offset=(0, -0.035 * c),
        ha="center",
    )
    if m > 0:
        ymax = m * c
        _dimension(
            ax,
            (p * c, 0),
            (p * c, ymax),
            f"max camber {m * 100:g} % c\nat x = {p * 10:g}0 % c",
            colour="tab:red",
            offset=(0.012 * c, -0.005 * c),
            ha="left",
            va="center",
        )
    xt, tmax = max_thickness_location(t, c)
    i = np.argmin(abs(x - xt))
    _dimension(ax, (xu[i], yl[i] + 0.0), (xu[i], yu[i]), "", colour="0.3")
    ax.text(
        xt + 0.015 * c,
        yu[i] + 0.035 * c,
        f"max thickness {t * 100:g} % c at x = {xt / c * 100:.0f} % c",
        fontsize=10,
        color="0.3",
    )
    ax.text(-0.03 * c, 0.03 * c, "LE", fontsize=11, ha="right")
    ax.text(1.01 * c, 0.0, "TE", fontsize=11, ha="left", va="center")
    ax.set_xlim(-0.08 * c, 1.08 * c)
    ax.set_ylim(-0.21 * c, 0.2 * c)
    ax.set_aspect("equal")
    ax.set_xlabel("x / c")
    ax.set_ylabel("y / c")
    ax.set_title(f"NACA {code}: geometry of a four-digit section")
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    ax.grid(alpha=0.25)

    ax = axes[1]
    for k, (other, colour) in enumerate(
        (
            ("0012", "tab:blue"),
            ("2412", "tab:orange"),
            ("4412", "tab:green"),
            ("4421", "tab:purple"),
        )
    ):
        xo, yco, (xuo, yuo), (xlo, ylo) = naca4_geometry(other, c, n)
        ax.plot(
            np.r_[xuo, xlo[::-1]],
            np.r_[yuo, ylo[::-1]],
            color=colour,
            lw=1.5,
            label=f"NACA {other}",
        )
        ax.plot(xo, yco, ":", color=colour, lw=1.2)
    ax.set_aspect("equal")
    ax.set_xlim(-0.08 * c, 1.08 * c)
    ax.set_xlabel("x / c")
    ax.set_ylabel("y / c")
    ax.set_title(
        "Effect of camber (0012, 2412, 4412) and thickness (4412, 4421); dotted: camber lines"
    )
    ax.set_ylim(-0.09 * c, 0.17 * c)
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    ax.grid(alpha=0.25)
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
