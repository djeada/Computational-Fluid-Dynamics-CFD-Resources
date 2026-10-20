"""Support reactions of a planar rigid body and the rank test for proper constraint.

Every support contributes reaction components: a roller one force along its
normal, a pin two forces, a fixed support two forces and a couple. Each
component is a column [d_x, d_y, x d_y - y d_x] (or [0, 0, 1] for a couple) of
a 3 x r matrix; the body is properly constrained when this matrix has rank 3,
statically determinate when in addition r = 3, and indeterminate to degree
r - 3 when r > 3. The script solves the reactions of a simply supported beam
with a point load and a partial uniform load, and classifies six support
layouts, including two improper ones (parallel and concurrent reactions).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

BEAM_LENGTH = 6.0  # m
POINT_LOAD = 10.0e3  # N, downward at x = 2 m
POINT_LOAD_X = 2.0  # m
UDL = 5.0e3  # N/m, downward on 3 m <= x <= 6 m
UDL_START, UDL_END = 3.0, 6.0  # m


def reaction_components(supports):
    """Expand supports into reaction components (kind, point, direction).

    ``supports`` is a list of (type, (x, y), normal) with type "pin",
    "roller" or "fixed"; ``normal`` is the direction of a roller's reaction.
    """
    components = []
    for kind, point, normal in supports:
        if kind in ("pin", "fixed"):
            components += [("force", point, (1.0, 0.0)), ("force", point, (0.0, 1.0))]
        if kind == "fixed":
            components.append(("couple", point, None))
        if kind == "roller":
            components.append(
                ("force", point, tuple(np.asarray(normal) / np.linalg.norm(normal)))
            )
    return components


def reaction_matrix(supports):
    """3 x r matrix: force components and moment about the origin of unit reactions."""
    columns = []
    for kind, (x, y), d in reaction_components(supports):
        if kind == "couple":
            columns.append([0.0, 0.0, 1.0])
        else:
            columns.append([d[0], d[1], x * d[1] - y * d[0]])
    return np.array(columns).T


def classify_supports(supports):
    """Return (r, rank, label) with label 'determinate', 'indeterminate (n)' or 'improper'."""
    matrix = reaction_matrix(supports)
    r = matrix.shape[1]
    rank = np.linalg.matrix_rank(matrix)
    if rank < 3:
        label = "improper (partial constraint)" if r < 3 else "improper"
    elif r == 3:
        label = "determinate"
    else:
        label = f"indeterminate, degree {r - 3}"
    return r, rank, label


def load_resultant(forces, couples=()):
    """Sum of applied point forces ((x, y), (F_x, F_y)) and couples as [F_x, F_y, M_O]."""
    total = np.zeros(3)
    for (x, y), (fx, fy) in forces:
        total += [fx, fy, x * fy - y * fx]
    total[2] += sum(couples)
    return total


def solve_reactions(supports, forces, couples=()):
    """Reaction components for a determinate body: A R + resultant = 0."""
    r, rank, label = classify_supports(supports)
    if label != "determinate":
        raise ValueError(f"reactions are not determined by statics: {label}")
    return np.linalg.solve(reaction_matrix(supports), -load_resultant(forces, couples))


def example_beam():
    """Pin at A (x = 0), roller at B (x = 6 m), point load and partial uniform load."""
    supports = [("pin", (0.0, 0.0), None), ("roller", (BEAM_LENGTH, 0.0), (0.0, 1.0))]
    resultant = UDL * (UDL_END - UDL_START)
    forces = [
        ((POINT_LOAD_X, 0.0), (0.0, -POINT_LOAD)),
        ((0.5 * (UDL_START + UDL_END), 0.0), (0.0, -resultant)),
    ]
    return supports, forces


LAYOUTS = [
    ("Pin + roller", [("pin", (0, 0), None), ("roller", (6, 0), (0, 1))]),
    ("Fixed end (cantilever)", [("fixed", (0, 0), None)]),
    (
        "Pin + two rollers",
        [("pin", (0, 0), None), ("roller", (3, 0), (0, 1)), ("roller", (6, 0), (0, 1))],
    ),
    (
        "Three parallel rollers",
        [
            ("roller", (0, 0), (0, 1)),
            ("roller", (3, 0), (0, 1)),
            ("roller", (6, 0), (0, 1)),
        ],
    ),
    (
        "Pin + roller whose reaction\npasses through the pin",
        [("pin", (0, 0), None), ("roller", (6, 0), (-1, 0))],
    ),
    ("Pin only", [("pin", (0, 0), None)]),
]


def draw_support(ax, kind, point, normal, size=0.35):
    """Draw a pin (triangle), roller (triangle on circles, oriented) or fixed wall (hatch)."""
    x, y = point
    if kind == "fixed":
        ax.fill(
            [x - 0.25, x, x, x - 0.25],
            [-0.8, -0.8, 0.8, 0.8],
            color="0.6",
            hatch="///",
            edgecolor="0.3",
        )
        return
    n = np.array([0.0, 1.0]) if normal is None else np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    t = np.array([-n[1], n[0]])
    p = np.array(point, float)
    base = p - 1.4 * size * n
    tri = np.array([p, base + size * t, base - size * t])
    ax.fill(*tri.T, color="0.55", zorder=2)
    if kind == "roller":
        for s in (-0.5, 0.5):
            c = base + s * size * t - 0.18 * n
            ax.add_patch(plt.Circle(c, 0.15, color="0.55", zorder=2))


def draw_reactions(ax, supports, color="tab:green"):
    """Draw unit reaction components as arrows (couples as curved arrows)."""
    normals = {tuple(point): normal for _, point, normal in supports}
    for kind, (x, y), d in reaction_components(supports):
        if kind == "couple":
            ax.annotate(
                "",
                xy=(x + 0.55, y + 0.5),
                xytext=(x + 0.55, y - 0.5),
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": color,
                    "lw": 1.8,
                    "connectionstyle": "arc3,rad=0.9",
                },
            )
            continue
        d = np.asarray(d)
        n = normals[(x, y)]
        n = (
            np.array([0.0, 1.0])
            if n is None
            else np.asarray(n, float) / np.linalg.norm(n)
        )
        gap = 0.75 if abs(d @ n) > 0.9 else 0.05  # clear the support symbol
        head = np.array([x, y]) - gap * d
        ax.annotate(
            "",
            xy=head,
            xytext=head - 0.9 * d,
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.8},
        )


def make_figure():
    """Worked beam with computed reactions, then six support layouts with their class."""
    fig = plt.figure(figsize=(12.5, 8.2))
    grid = fig.add_gridspec(3, 3, height_ratios=[1.5, 1, 1], hspace=0.45, wspace=0.12)

    ax = fig.add_subplot(grid[0, :])
    supports, forces = example_beam()
    a_x, a_y, b_y = solve_reactions(supports, forces)
    ax.plot([0, BEAM_LENGTH], [0, 0], color="0.2", linewidth=8, solid_capstyle="butt")
    for kind, point, normal in supports:
        draw_support(ax, kind, point, normal)
    ax.annotate(
        "",
        xy=(POINT_LOAD_X, 0.12),
        xytext=(POINT_LOAD_X, 1.3),
        arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2.5},
    )
    ax.text(POINT_LOAD_X + 0.1, 1.1, "10 kN", color="tab:red", fontsize=11)
    xs = np.linspace(UDL_START, UDL_END, 7)
    ax.fill_between([UDL_START, UDL_END], 0.12, 0.75, color="tab:red", alpha=0.15)
    for x in xs:
        ax.annotate(
            "",
            xy=(x, 0.12),
            xytext=(x, 0.75),
            arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 1.2},
        )
    ax.text(
        3.0, 0.95, "5 kN/m, resultant 15 kN at x = 4.5 m", color="tab:red", fontsize=11
    )
    for x, value, name in ((0.0, a_y, "A_y"), (BEAM_LENGTH, b_y, "B_y")):
        ax.annotate(
            "",
            xy=(x, -0.62),
            xytext=(x, -1.6),
            arrowprops={"arrowstyle": "-|>", "color": "tab:green", "lw": 2.5},
        )
        ax.text(
            x + 0.12,
            -1.45,
            f"${name}$ = {value / 1e3:.2f} kN",
            color="tab:green",
            fontsize=11,
        )
    ax.text(-0.9, 0.3, f"$A_x$ = {abs(a_x) / 1e3:.0f}", color="tab:green", fontsize=11)
    ax.set_xlim(-1.2, BEAM_LENGTH + 1.6)
    ax.set_ylim(-1.8, 1.5)
    ax.set_aspect("equal")
    ax.set_yticks([])
    ax.set_xlabel("x (m)")
    ax.set_title(
        "(a) Simply supported beam, reactions from the 3 x 3 equilibrium system"
    )

    for k, (title, layout) in enumerate(LAYOUTS):
        ax = fig.add_subplot(grid[1 + k // 3, k % 3])
        r, rank, label = classify_supports(layout)
        ax.plot([0, 6], [0, 0], color="0.2", linewidth=6, solid_capstyle="butt")
        for kind, point, normal in layout:
            draw_support(ax, kind, point, normal)
        draw_reactions(ax, layout)
        good = rank == 3
        ax.text(
            3,
            -2.35,
            f"r = {r}, rank = {rank}: {label}",
            ha="center",
            fontsize=10,
            color="black" if good else "tab:red",
            fontweight="normal" if good else "bold",
        )
        ax.set_title(f"({chr(ord('b') + k)}) {title}", fontsize=11)
        ax.set_xlim(-1.4, 7.6)
        ax.set_ylim(-2.6, 0.9)
        ax.set_aspect("equal")
        ax.axis("off")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    supports, forces = example_beam()
    reactions = solve_reactions(supports, forces)
    a_x, a_y, b_y = np.where(np.abs(reactions) < 1e-6, 0.0, reactions)  # drop -0.00
    print(
        f"beam reactions: A_x = {a_x / 1e3:.2f} kN, A_y = {a_y / 1e3:.2f} kN, "
        f"B_y = {b_y / 1e3:.2f} kN"
    )
    for title, layout in LAYOUTS:
        r, rank, label = classify_supports(layout)
        print(f"{title.replace(chr(10), ' '):<50} r = {r}, rank = {rank}: {label}")

    finish_figures(
        {"statics_support_reactions.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
