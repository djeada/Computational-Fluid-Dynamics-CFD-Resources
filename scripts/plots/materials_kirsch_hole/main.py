"""Plot the Kirsch stress field around a circular hole in a plate under uniaxial tension.

An infinite elastic plate with a hole of radius a carries a remote stress
sigma_inf along x. The closed-form Kirsch (1898) solution gives the polar
stress components everywhere; the hoop stress at the hole edge reaches
3 sigma_inf at theta = 90 deg (stress concentration factor K_t = 3) and
-sigma_inf at theta = 0. The figure shows the hoop-stress field, the decay
of sigma_xx along the ligament x = 0, and the hoop stress around the hole edge.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Circle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

RADIUS = 1.0  # hole radius a (any length unit; results depend on r/a only)
SIGMA_INF = 1.0  # remote tensile stress along x (results are scaled by it)
EXTENT = 4.0  # half-width of the plotted field in hole radii
GRID = 401  # points per direction of the field plot


def kirsch_polar(r, theta, a=RADIUS, sigma=SIGMA_INF):
    """Return (sigma_rr, sigma_tt, tau_rt) at polar coordinates (r, theta), r >= a."""
    q2 = (a / r) ** 2
    q4 = q2**2
    c2, s2 = np.cos(2.0 * theta), np.sin(2.0 * theta)
    s_rr = 0.5 * sigma * (1.0 - q2) + 0.5 * sigma * (1.0 - 4.0 * q2 + 3.0 * q4) * c2
    s_tt = 0.5 * sigma * (1.0 + q2) - 0.5 * sigma * (1.0 + 3.0 * q4) * c2
    t_rt = -0.5 * sigma * (1.0 + 2.0 * q2 - 3.0 * q4) * s2
    return s_rr, s_tt, t_rt


def kirsch_cartesian(x, y, a=RADIUS, sigma=SIGMA_INF):
    """Return (sigma_xx, sigma_yy, tau_xy) at Cartesian points outside the hole."""
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    s_rr, s_tt, t_rt = kirsch_polar(r, theta, a, sigma)
    c, s = np.cos(theta), np.sin(theta)
    s_xx = s_rr * c**2 + s_tt * s**2 - 2.0 * t_rt * s * c
    s_yy = s_rr * s**2 + s_tt * c**2 + 2.0 * t_rt * s * c
    t_xy = (s_rr - s_tt) * s * c + t_rt * (c**2 - s**2)
    return s_xx, s_yy, t_xy


def ligament_stress(r_over_a):
    """Return sigma_xx / sigma_inf on the line x = 0 at distance r/a from the centre."""
    q2 = 1.0 / np.asarray(r_over_a, dtype=float) ** 2
    return 1.0 + 0.5 * q2 + 1.5 * q2**2


def make_figure():
    """Draw the hoop-stress field and the two line plots."""
    fig, (field, line, edge) = plt.subplots(
        1, 3, figsize=(14, 4.9), gridspec_kw={"width_ratios": [1.25, 1, 1]}
    )

    x = np.linspace(-EXTENT, EXTENT, GRID) * RADIUS
    xx, yy = np.meshgrid(x, x)
    r = np.hypot(xx, yy)
    _, s_tt, _ = kirsch_polar(np.maximum(r, RADIUS), np.arctan2(yy, xx))
    s_tt = np.where(r >= RADIUS, s_tt / SIGMA_INF, np.nan)
    norm = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=3.0)
    levels = np.linspace(-1.0, 3.0, 17)
    filled = field.contourf(xx, yy, s_tt, levels=levels, cmap="RdBu_r", norm=norm)
    field.contour(xx, yy, s_tt, levels=[0.0, 1.0, 2.0], colors="k", linewidths=0.6)
    field.add_patch(Circle((0, 0), RADIUS, facecolor="white", edgecolor="k"))
    label_box = {
        "boxstyle": "round,pad=0.15",
        "facecolor": "white",
        "edgecolor": "none",
    }
    field.text(
        0,
        1.15,
        r"$3\sigma_\infty$",
        ha="center",
        va="bottom",
        fontsize=11,
        bbox=label_box,
    )
    field.text(
        1.12,
        0,
        r"$-\sigma_\infty$",
        ha="left",
        va="center",
        fontsize=11,
        bbox=label_box,
    )
    fig.colorbar(
        filled,
        ax=field,
        label=r"$\sigma_{\theta\theta}/\sigma_\infty$",
        ticks=[-1, 0, 1, 2, 3],
    )
    field.set(
        aspect="equal",
        xlabel="$x/a$",
        ylabel="$y/a$",
        title=r"Hoop stress, remote $\sigma_\infty$ along $x$",
    )

    r_line = np.linspace(1.0, 8.0, 400)
    line.plot(
        r_line,
        ligament_stress(r_line),
        color="tab:blue",
        lw=2,
        label=r"$\sigma_{xx}(0, y)/\sigma_\infty$, Kirsch",
    )
    line.axhline(1.0, color="0.4", lw=1, ls="--", label="remote stress")
    for rr in (2.0, 3.0, 5.0):
        value = ligament_stress(rr)
        line.plot(rr, value, "o", color="tab:blue")
        line.annotate(
            f"{value:.3f}",
            (rr, value),
            xytext=(4, 6),
            textcoords="offset points",
            fontsize=10,
        )
    line.set(
        xlim=(1, 8),
        ylim=(0.8, 3.1),
        xlabel="distance from hole centre $y/a$",
        ylabel=r"$\sigma_{xx}/\sigma_\infty$",
        title="Decay along the ligament $x = 0$",
    )
    line.legend(fontsize=10)

    theta = np.linspace(0.0, np.pi, 361)
    _, s_edge, _ = kirsch_polar(RADIUS, theta)
    edge.plot(
        np.degrees(theta),
        s_edge / SIGMA_INF,
        color="tab:red",
        lw=2,
        label=r"$1 - 2\cos 2\theta$",
    )
    edge.axhline(0.0, color="0.4", lw=0.8)
    edge.plot(90, 3, "o", color="tab:red")
    edge.annotate(
        r"$K_t = 3$ at $\theta = 90^\circ$",
        (90, 3),
        xytext=(100, 2.4),
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    edge.set(
        xlim=(0, 180),
        ylim=(-1.3, 3.4),
        xticks=range(0, 181, 30),
        xlabel=r"angle from load axis $\theta$ (deg)",
        ylabel=r"$\sigma_{\theta\theta}/\sigma_\infty$ at $r = a$",
        title="Hoop stress on the hole edge",
    )
    edge.legend(fontsize=10, loc="lower center")
    for ax in (line, edge):
        ax.grid(True, lw=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    _, s_top, _ = kirsch_polar(RADIUS, np.pi / 2.0)
    _, s_side, _ = kirsch_polar(RADIUS, 0.0)
    print(
        f"hoop stress at the hole edge: theta = 90 deg {s_top / SIGMA_INF:.3f}, "
        f"theta = 0 deg {s_side / SIGMA_INF:.3f} (times sigma_inf)"
    )
    for rr in (1.5, 2.0, 3.0, 5.0):
        print(
            f"sigma_xx/sigma_inf on x = 0 at y = {rr:.1f} a: {ligament_stress(rr):.4f}"
        )

    finish_figures(
        {"materials_kirsch_hole.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
