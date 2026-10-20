"""Draw the D2Q9 and D3Q19 velocity sets, the streaming step and half-way bounce-back.

The top row shows the discrete velocities of the two most common lattices with
their indices and quadrature weights. The bottom row shows the nine populations
of one D2Q9 node before and after streaming, and how half-way bounce-back sends
populations that hit a wall back to the node they came from, with the wall
halfway along the link.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch, Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# D2Q9, counter-clockwise ordering: rest, E, N, W, S, NE, NW, SW, SE.
D2Q9_VELOCITIES = np.array(
    [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
)
D2Q9_WEIGHTS = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
D2Q9_OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])
WEIGHT_LABELS = {4 / 9: "4/9", 1 / 9: "1/9", 1 / 36: "1/36"}

# D3Q19: rest, 6 face neighbours (|c|^2 = 1), 12 edge neighbours (|c|^2 = 2).
D3Q19_WEIGHT_REST, D3Q19_WEIGHT_FACE, D3Q19_WEIGHT_EDGE = 1 / 3, 1 / 18, 1 / 36

ARROW_LENGTH = 0.32  # drawn length of a population arrow, as a fraction of a link
COLORS = plt.cm.tab10.colors


def d3q19_velocities():
    """The 19 velocities of D3Q19 in the order rest, faces, edges."""
    shells = [(0, 0, 0)]
    candidates = [(x, y, z) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1)]
    shells += [c for c in candidates if sum(abs(v) for v in c) == 1]
    shells += [c for c in candidates if sum(abs(v) for v in c) == 2]
    return np.array(shells)


def d3q19_weights(velocities):
    """Weights 1/3, 1/18, 1/36 by squared speed 0, 1, 2."""
    squared = np.sum(velocities**2, axis=1)
    return np.choose(squared, [D3Q19_WEIGHT_REST, D3Q19_WEIGHT_FACE, D3Q19_WEIGHT_EDGE])


def arrow(ax, start, end, color, **kwargs):
    """Draw a 2D arrow from start to end."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=kwargs.pop("arrowstyle", "-|>"),
            mutation_scale=kwargs.pop("mutation_scale", 16),
            color=color,
            linewidth=kwargs.pop("linewidth", 2.0),
            shrinkA=0,
            shrinkB=0,
            **kwargs,
        )
    )


def draw_d2q9(ax):
    """Velocity vectors of D2Q9 with indices and weights."""
    for x in (-1, 0, 1):
        ax.axvline(x, color="0.85", linewidth=1, zorder=0)
        ax.axhline(x, color="0.85", linewidth=1, zorder=0)
    shell_color = {4 / 9: COLORS[3], 1 / 9: COLORS[0], 1 / 36: COLORS[2]}
    for i, (c, w) in enumerate(zip(D2Q9_VELOCITIES, D2Q9_WEIGHTS)):
        color = shell_color[w]
        if i == 0:
            ax.plot(0, 0, "o", color=color, markersize=12, zorder=3)
            ax.text(0.1, -0.22, "0\n4/9", color=color, fontsize=11, ha="left")
            continue
        arrow(ax, (0, 0), tuple(c), color, mutation_scale=20)
        offset = 0.2 * c / np.linalg.norm(c)
        ax.text(
            c[0] + offset[0],
            c[1] + offset[1],
            f"{i}\n{WEIGHT_LABELS[w]}",
            color=color,
            fontsize=11,
            ha="center",
            va="center",
        )
    for w, label in ((4 / 9, "rest"), (1 / 9, "axis, |c| = 1"), (1 / 36, "diagonal")):
        ax.plot([], [], "-", color=shell_color[w], linewidth=3, label=label)
    ax.legend(fontsize=10, loc="lower left", bbox_to_anchor=(1.0, 0.0), frameon=False)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$c_{ix}\ [\Delta x / \Delta t]$", fontsize=11)
    ax.set_ylabel(r"$c_{iy}\ [\Delta x / \Delta t]$", fontsize=11)
    ax.set_title("(a) D2Q9: index i and weight $w_i$", fontsize=12)


def draw_d3q19(ax):
    """3D quiver of the D3Q19 velocities coloured by shell."""
    velocities = d3q19_velocities()
    weights = d3q19_weights(velocities)
    corners = np.array([(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)])
    for a in corners:
        for b in corners:
            if np.sum(np.abs(a - b)) == 2:
                ax.plot(*zip(a, b), color="0.85", linewidth=0.8)
    for w, color, label in (
        (D3Q19_WEIGHT_FACE, COLORS[0], "6 faces, $w = 1/18$"),
        (D3Q19_WEIGHT_EDGE, COLORS[2], "12 edges, $w = 1/36$"),
    ):
        c = velocities[np.isclose(weights, w)]
        zeros = np.zeros(len(c))
        ax.quiver(
            zeros, zeros, zeros, c[:, 0], c[:, 1], c[:, 2],
            color=color, arrow_length_ratio=0.15, linewidth=1.8, label=label,
        )  # fmt: skip
    ax.scatter([0], [0], [0], color=COLORS[3], s=60, label="rest, $w = 1/3$")
    ax.set_xlabel("$c_x$", fontsize=11)
    ax.set_ylabel("$c_y$", fontsize=11)
    ax.set_zlabel("$c_z$", fontsize=11)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])
    ax.view_init(elev=22, azim=-58)
    ax.set_box_aspect((1, 1, 1))
    ax.legend(fontsize=10, loc="upper left", bbox_to_anchor=(0.9, 0.9), frameon=False)
    ax.set_title("(b) D3Q19: no corner velocities", fontsize=12)


def draw_node_grid(ax, extent=2):
    """Lattice nodes on [-extent, extent]^2 with faint links."""
    for x in range(-extent, extent + 1):
        ax.plot([x, x], [-extent, extent], color="0.88", linewidth=1, zorder=0)
        ax.plot([-extent, extent], [x, x], color="0.88", linewidth=1, zorder=0)
    xs, ys = np.meshgrid(np.arange(-extent, extent + 1), np.arange(-extent, extent + 1))
    ax.plot(xs, ys, "o", color="0.55", markersize=5, zorder=1)
    ax.set_xlim(-extent - 0.5, extent + 0.5)
    ax.set_ylim(-extent - 0.5, extent + 0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def draw_streaming(ax, after):
    """Populations of the centre node before streaming, or where they land after."""
    draw_node_grid(ax, extent=1)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    for i, c in enumerate(D2Q9_VELOCITIES[1:], start=1):
        unit = c / np.linalg.norm(c)
        tail = c if after else np.zeros(2)
        if after:
            ax.plot([0, c[0]], [0, c[1]], ":", color=COLORS[i], linewidth=1.2)
        head = tail + ARROW_LENGTH * unit
        arrow(ax, tuple(tail), tuple(head), COLORS[i])
        ax.text(*(tail + 0.53 * unit), str(i), color=COLORS[i], fontsize=10,
                ha="center", va="center")  # fmt: skip
    ax.plot(0, 0, "o", color="k", markersize=8, zorder=3)
    ax.plot(0, 0, "o", color=COLORS[0], markersize=4, zorder=4)
    if after:
        ax.set_title(r"(d) After streaming: $f_i$ at $\mathbf{x} + \mathbf{c}_i$",
                     fontsize=12)  # fmt: skip
    else:
        ax.set_title(
            r"(c) Post-collision $f_i^\star$ at node $\mathbf{x}$", fontsize=12
        )


def draw_bounce_back(ax):
    """Half-way bounce-back: populations reflect at the mid-link wall."""
    ax.add_patch(
        Rectangle(
            (-1.4, -1.4),
            2.8,
            0.9,
            facecolor="0.88",
            edgecolor="none",
            hatch="///",
            zorder=0,
        )  # fmt: skip
    )
    ax.plot([-1.4, 1.4], [-0.5, -0.5], "k-", linewidth=2.5)
    ax.text(-1.35, -0.58, "wall at mid-link", ha="left", va="top", fontsize=10,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})  # fmt: skip
    ax.text(1.35, -1.35, "solid nodes", ha="right", va="bottom", fontsize=10,
            color="0.3", bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})  # fmt: skip
    for x in (-1, 0, 1):
        for y in (0, 1):
            ax.plot(x, y, "o", color="0.55", markersize=5)
        ax.plot(
            x, -1, "o", markerfacecolor="white", markeredgecolor="0.4", markersize=6
        )
    ax.plot(0, 0, "o", color="k", markersize=8, zorder=3)
    for i, label_at in ((4, (-0.33, 0.45)), (8, (0.75, 0.45))):  # S and SE
        c = D2Q9_VELOCITIES[i]
        j = D2Q9_OPPOSITE[i]
        mid = np.array([0.5 * c[0], -0.5])  # where the link crosses the wall
        normal = np.array([-c[1], c[0]]) / np.linalg.norm(c)
        side = 0.06 * normal  # draw the outgoing and returning paths side by side
        arrow(ax, tuple(side), tuple(mid + side), COLORS[i], linewidth=2.4)
        arrow(ax, tuple(mid - side), tuple(0.12 * mid - side), COLORS[j],
              linestyle="--", linewidth=2.4)  # fmt: skip
        ax.text(*label_at, rf"$f_{i}^\star \to f_{j}$", color=COLORS[j],
                fontsize=12, ha="center", va="center")  # fmt: skip
    ax.text(0.08, 0.1, r"$\mathbf{x}_b$", fontsize=12)
    ax.plot([], [], "-", color="k", linewidth=2, label=r"leaves at $t$")
    ax.plot([], [], "--", color="k", linewidth=2, label=r"returns at $t + \Delta t$")
    ax.legend(fontsize=10, loc="upper center", framealpha=1, ncol=2)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("(e) Half-way bounce-back at a wall", fontsize=12)


def make_figure():
    """Velocity sets on top, streaming and bounce-back below."""
    fig = plt.figure(figsize=(13, 9.6))
    grid = GridSpec(2, 6, figure=fig, height_ratios=(1.15, 1.0))
    draw_d2q9(fig.add_subplot(grid[0, 0:3]))
    draw_d3q19(fig.add_subplot(grid[0, 3:6], projection="3d"))
    draw_streaming(fig.add_subplot(grid[1, 0:2]), after=False)
    draw_streaming(fig.add_subplot(grid[1, 2:4]), after=True)
    draw_bounce_back(fig.add_subplot(grid[1, 4:6]))
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for name, velocities, weights in (
        ("D2Q9", D2Q9_VELOCITIES, D2Q9_WEIGHTS),
        ("D3Q19", d3q19_velocities(), d3q19_weights(d3q19_velocities())),
    ):
        second = np.einsum("i,ia,ib->ab", weights, velocities, velocities)
        print(
            f"{name}: sum w = {weights.sum():.6f}, "
            f"sum w c = {np.abs(weights @ velocities).max():.1e}, "
            f"sum w c c = {second[0, 0]:.6f} I (off-diagonal "
            f"{np.abs(second - np.diag(np.diag(second))).max():.1e})"
        )

    finish_figures(
        {"lattice_velocity_sets.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
