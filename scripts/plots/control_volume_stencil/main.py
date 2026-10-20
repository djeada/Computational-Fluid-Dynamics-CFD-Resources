"""Control-volume notation for the finite-volume method in 1D and on 2D unstructured cells.

Panel (a) draws a 1D cell-centred grid with the nodes W, P, E, the faces w
and e, the cell width and the node-to-node distances. Panel (b) draws two
polygonal cells that share one face: the owner P, the neighbour N, the face
centre f, the face area vector S_f, the vector d between the centroids and the
over-relaxed split S_f = Delta + k used for the non-orthogonal correction of
the diffusion flux, together with the point f' where d crosses the face, whose
distance from f measures the skewness. The geometry in (b) is computed, not
sketched: the centroids are the polygon centroids and Delta, k follow from
the formulas printed by the script.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# 1D grid: cell width (arbitrary length units) and the cells drawn.
DX = 2.0
CELL_LABELS = ("WW", "W", "P", "E", "EE")

# 2D cells (arbitrary length units, unit depth). The shared face is the
# segment FACE_A -> FACE_B; it belongs to both polygons.
FACE_A = (-0.1, -2.2)
FACE_B = (0.6, 1.0)
OWNER = ((-1.8, -2.1), FACE_A, FACE_B, (-1.1, 1.0), (-2.4, -0.3))
NEIGHBOUR = (FACE_A, (1.9, -1.5), (2.9, 0.6), (2.1, 2.0), FACE_B)

BLUE, ORANGE, GREEN, RED, PURPLE = (
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
)


def polygon_centroid(vertices):
    """Area-weighted centroid of a simple polygon (shoelace formula)."""
    v = np.asarray(vertices, dtype=float)
    x, y = v[:, 0], v[:, 1]
    xn, yn = np.roll(x, -1), np.roll(y, -1)
    cross = x * yn - xn * y
    area = 0.5 * cross.sum()
    cx = ((x + xn) * cross).sum() / (6.0 * area)
    cy = ((y + yn) * cross).sum() / (6.0 * area)
    return np.array([cx, cy]), abs(area)


def face_geometry():
    """Centroids, face vectors and the over-relaxed split for panel (b)."""
    a, b = np.array(FACE_A), np.array(FACE_B)
    x_p, area_p = polygon_centroid(OWNER)
    x_n, area_n = polygon_centroid(NEIGHBOUR)
    x_f = 0.5 * (a + b)
    t = b - a
    s_f = np.array([t[1], -t[0]])  # length |S_f| = face length (unit depth)
    if np.dot(s_f, x_n - x_p) < 0:
        s_f = -s_f  # point from owner to neighbour
    d = x_n - x_p
    delta = d * np.dot(s_f, s_f) / np.dot(d, s_f)  # over-relaxed approach
    k = s_f - delta
    # Point where the line P -> N crosses the face: x_P + lam d on the face.
    lam = np.dot(x_f - x_p, s_f) / np.dot(d, s_f)
    x_fp = x_p + lam * d
    angle = np.degrees(
        np.arccos(np.dot(d, s_f) / (np.linalg.norm(d) * np.linalg.norm(s_f)))
    )
    return {
        "x_p": x_p,
        "x_n": x_n,
        "x_f": x_f,
        "s_f": s_f,
        "d": d,
        "delta": delta,
        "k": k,
        "x_fp": x_fp,
        "weight": lam,
        "angle": angle,
        "areas": (area_p, area_n),
    }


def _arrow(ax, start, end, color, width=2.0, style="-|>", scale=18, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=scale,
            color=color,
            linewidth=width,
            linestyle=ls,
            shrinkA=0,
            shrinkB=0,
        )
    )


def _dimension(ax, x0, x1, y, text, color="k"):
    ax.annotate(
        "",
        xy=(x1, y),
        xytext=(x0, y),
        arrowprops={"arrowstyle": "<->", "color": color, "linewidth": 1.3},
    )
    ax.text(
        0.5 * (x0 + x1),
        y + 0.12,
        text,
        ha="center",
        va="bottom",
        fontsize=12,
        color=color,
    )


def draw_1d(ax):
    n = len(CELL_LABELS)
    x0 = -0.5 * n * DX
    for i, label in enumerate(CELL_LABELS):
        left = x0 + i * DX
        is_p = label == "P"
        ax.add_patch(
            Rectangle(
                (left, -0.6),
                DX,
                1.2,
                facecolor="#cfe2f3" if is_p else "white",
                edgecolor="k",
                linewidth=1.5,
            )
        )
        xc = left + 0.5 * DX
        ax.plot(xc, 0.0, "o", color="k", markersize=8)
        ax.text(
            xc,
            0.18,
            label,
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold" if is_p else "normal",
        )
    # Faces w and e of cell P.
    xw, xe = -0.5 * DX, 0.5 * DX
    for xface, name in ((xw, "w"), (xe, "e")):
        ax.plot([xface, xface], [-0.6, 0.6], color=RED, linewidth=3)
        ax.text(xface, -0.75, name, ha="center", va="top", fontsize=13, color=RED)
    # Fluxes through the faces.
    _arrow(ax, (xw - 0.7, -0.3), (xw + 0.7, -0.3), ORANGE, width=2.0)
    ax.text(xw + 0.75, -0.3, r"$J_w$", va="center", fontsize=12, color=ORANGE)
    _arrow(ax, (xe - 0.7, -0.3), (xe + 0.7, -0.3), ORANGE, width=2.0)
    ax.text(xe + 0.75, -0.3, r"$J_e$", va="center", fontsize=12, color=ORANGE)
    # Distances.
    _dimension(ax, xw, xe, 0.95, r"$\Delta x = \delta x_{we}$")
    _dimension(ax, -DX, 0.0, -1.35, r"$\delta x_{WP}$", color=BLUE)
    _dimension(ax, 0.0, DX, -1.35, r"$\delta x_{PE}$", color=BLUE)
    _dimension(ax, xw, 0.0, 1.6, r"$\delta x_{wP}$", color=GREEN)
    _dimension(ax, 0.0, xe, 1.6, r"$\delta x_{Pe}$", color=GREEN)
    ax.text(
        0.0,
        -2.1,
        r"$J_e - J_w = \bar{S}\,\Delta x$, with $J = \rho u \phi - \Gamma\, d\phi/dx$ on each face",
        ha="center",
        fontsize=12,
    )
    ax.set_xlim(x0 - 0.2, -x0 + 0.2)
    ax.set_ylim(-2.4, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a) 1D cell-centred grid around node P", fontsize=13)


def _label(ax, point, text, offset, color="k", **kwargs):
    ax.text(
        point[0] + offset[0],
        point[1] + offset[1],
        text,
        fontsize=13,
        color=color,
        ha="center",
        va="center",
        **kwargs,
    )


def draw_2d(ax, g):
    ax.add_patch(
        Polygon(OWNER, closed=True, facecolor="#cfe2f3", edgecolor="k", linewidth=1.5)
    )
    ax.add_patch(
        Polygon(
            NEIGHBOUR, closed=True, facecolor="#fde9d9", edgecolor="k", linewidth=1.5
        )
    )
    a, b = np.array(FACE_A), np.array(FACE_B)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=RED, linewidth=3.5)
    _label(ax, b, "face f", (0.45, 0.15), color=RED)
    x_p, x_n, x_f, x_fp = g["x_p"], g["x_n"], g["x_f"], g["x_fp"]
    ax.plot(*x_p, "ko", markersize=8)
    ax.plot(*x_n, "ko", markersize=8)
    _label(ax, x_p, "P (owner)", (-0.1, -0.35))
    _label(ax, x_n, "N (neighbour)", (0.2, 0.35))
    # d from P to N.
    _arrow(ax, x_p, x_n, "k", width=1.6, ls="--")
    _label(ax, x_p + 0.25 * g["d"], r"$\mathbf{d}$", (-0.05, 0.25))
    # Face centre, the point f' where d crosses the face, and m = f - f'.
    ax.plot(*x_f, "s", color=RED, markersize=8, zorder=5)
    _label(ax, x_f, r"$\mathbf{x}_f$", (-0.35, -0.1), color=RED)
    ax.plot(*x_fp, "D", color=PURPLE, markersize=7, zorder=5)
    _label(ax, x_fp, r"$\mathbf{x}_{f'}$", (-0.38, 0.12), color=PURPLE)
    _arrow(ax, x_fp, x_f, PURPLE, width=1.5, scale=12)
    _label(ax, 0.5 * (x_fp + x_f), r"$\mathbf{m}$", (-0.25, -0.05), color=PURPLE)
    # Face area vector and its over-relaxed split, drawn from x_f.
    s, delta = g["s_f"], g["delta"]
    scale = 0.5  # drawing scale for the vectors
    tip, tip_d = x_f + scale * s, x_f + scale * delta
    _arrow(ax, x_f, tip, BLUE, width=2.5)
    _label(ax, tip, r"$\mathbf{S}_f$", (0.25, -0.12), color=BLUE)
    _arrow(ax, x_f, tip_d, GREEN, width=2.5)
    _label(ax, tip_d, r"$\boldsymbol{\Delta}$", (0.2, 0.15), color=GREEN)
    _arrow(ax, tip_d, tip, ORANGE, width=2.5)
    _label(ax, 0.5 * (tip_d + tip), r"$\mathbf{k}$", (0.22, 0.0), color=ORANGE)
    ax.text(
        3.4,
        0.2,
        r"$\mathbf{d} = \mathbf{x}_N - \mathbf{x}_P$"
        "\n"
        r"$\mathbf{S}_f = \boldsymbol{\Delta} + \mathbf{k}$"
        "\n"
        r"$\boldsymbol{\Delta} = \mathbf{d}\,"
        r"\frac{\mathbf{S}_f\cdot\mathbf{S}_f}{\mathbf{d}\cdot\mathbf{S}_f}$"
        "\n"
        r"$\mathbf{m} = \mathbf{x}_f - \mathbf{x}_{f'}$"
        "\n"
        f"angle(d, S_f) = {g['angle']:.0f}" + r"$^\circ$",
        ha="left",
        va="center",
        fontsize=12,
        linespacing=1.8,
    )
    ax.set_xlim(-2.6, 5.6)
    ax.set_ylim(-2.5, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(b) Two unstructured cells sharing face f", fontsize=13)


def make_figure(g):
    fig, axes = plt.subplots(
        2, 1, figsize=(11, 9.5), gridspec_kw={"height_ratios": [0.8, 1.0]}
    )
    draw_1d(axes[0])
    draw_2d(axes[1], g)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    g = face_geometry()
    print(
        f"x_P = {g['x_p'].round(3)}, x_N = {g['x_n'].round(3)}, x_f = {g['x_f'].round(3)}"
    )
    print(f"S_f = {g['s_f'].round(3)}, |S_f| = {np.linalg.norm(g['s_f']):.3f}")
    print(f"d = {g['d'].round(3)}, angle(d, S_f) = {g['angle']:.1f} deg")
    print(
        f"Delta = {g['delta'].round(3)}, k = {g['k'].round(3)}, k . S_f = {np.dot(g['k'], g['s_f']):.2e}"
    )
    print(
        f"f' = {g['x_fp'].round(3)}, |m| = |f - f'| = {np.linalg.norm(g['x_f'] - g['x_fp']):.3f}"
    )
    finish_figures(
        {"control_volume_stencil.png": make_figure(g)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
