"""Draw the standard 2D supports and connections next to the reactions they exert on a body.

Each cell of the chart shows a support as it is drawn on a space diagram, an
arrow, and the same body as it appears on a free-body diagram with the support
replaced by its unknown reaction forces and moments. The number of unknowns
each support contributes is listed in SUPPORTS, which the caption of every
cell is generated from.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# (key, name, reactions, what the support prevents)
SUPPORTS = (
    ("cable", "Cable", ("T",), "pulls along the cable, away from the body"),
    ("link", "Weightless link", ("F",), "force along the link, either sense"),
    ("roller", "Roller", ("F_y",), "force normal to the rolling surface"),
    ("smooth", "Smooth surface", ("N",), "force normal to the common tangent"),
    ("collar", "Pinned collar on smooth rod", ("F",), "force normal to the rod"),
    ("pin", "Smooth pin or hinge", ("A_x", "A_y"), "two force components"),
    (
        "fixed_collar",
        "Fixed collar on smooth rod",
        ("F", "M"),
        "force normal to the rod and a couple",
    ),
    ("fixed", "Fixed support", ("A_x", "A_y", "M_A"), "two forces and a couple"),
)

BODY_COLOR = "0.80"
GROUND_COLOR = "0.35"
REACTION_COLOR = "tab:red"
OFFSET = 6.0  # x offset of the free-body sketch within a cell (drawing units)


def unknown_count(key):
    """Number of unknown reaction components a support contributes."""
    for k, _, reactions, _ in SUPPORTS:
        if k == key:
            return len(reactions)
    raise KeyError(key)


def ground(ax, x0, x1, y, angle=0.0, below=True):
    """Draw a hatched ground line from x0 to x1 at height y, optionally inclined."""
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    p0 = np.array([x0, y])
    p1 = p0 + (x1 - x0) * np.array([c, s])
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=GROUND_COLOR, linewidth=2)
    normal = np.array([s, -c]) if below else np.array([-s, c])
    for t in np.linspace(0.05, 0.95, 9):
        q = p0 + t * (p1 - p0)
        r = q + 0.28 * normal + 0.18 * np.array([-c, -s])
        ax.plot([q[0], r[0]], [q[1], r[1]], color=GROUND_COLOR, linewidth=1)


def wall(ax, x, y0, y1, left=True):
    """Draw a hatched vertical wall at x from y0 to y1."""
    ax.plot([x, x], [y0, y1], color=GROUND_COLOR, linewidth=2)
    d = -0.28 if left else 0.28
    for y in np.linspace(y0 + 0.1, y1 - 0.1, 8):
        ax.plot([x, x + d], [y, y - 0.2], color=GROUND_COLOR, linewidth=1)


def beam(ax, x, y, width=2.6, height=0.45, alpha=1.0):
    """Draw the end of a body as a rectangle with lower-right corner at (x, y)."""
    ax.add_patch(
        Rectangle(
            (x - width, y),
            width,
            height,
            facecolor=BODY_COLOR,
            edgecolor="0.25",
            linewidth=1.2,
            alpha=alpha,
        )
    )


def arrow(ax, start, end, label=None, offset=(4, 4), color=REACTION_COLOR):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=2,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )
    if label:
        ax.annotate(
            rf"${label}$",
            end,
            xytext=offset,
            textcoords="offset points",
            color=color,
            fontsize=12,
        )


def moment_arrow(ax, center, label, radius=0.45):
    theta = np.linspace(np.radians(-60), np.radians(200), 40)
    pts = np.column_stack(
        (center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta))
    )
    ax.add_patch(
        FancyArrowPatch(
            path=MplPath(pts),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=2,
            color=REACTION_COLOR,
        )
    )
    ax.annotate(
        rf"${label}$",
        (center[0] - radius, center[1] + radius),
        xytext=(-22, 2),
        textcoords="offset points",
        color=REACTION_COLOR,
        fontsize=12,
    )


def pin_symbol(ax, x, y):
    ax.add_patch(
        Polygon(
            [[x, y], [x - 0.35, y - 0.6], [x + 0.35, y - 0.6]],
            closed=True,
            facecolor="white",
            edgecolor="0.2",
            linewidth=1.5,
        )
    )
    ax.add_patch(Circle((x, y), 0.09, facecolor="white", edgecolor="0.2", zorder=3))


def draw_cable(ax):
    x, y = 3.0, 1.2
    beam(ax, x, y)
    top = np.array([x + 1.0, 3.3])
    ax.plot([x - 0.15, top[0]], [y + 0.45, top[1]], color="0.2", linewidth=1.5)
    ground(ax, top[0] - 0.6, top[0] + 0.6, top[1], below=False)
    beam(ax, x + OFFSET, y, alpha=0.6)
    start = np.array([x + OFFSET - 0.15, y + 0.45])
    direction = (top - np.array([x - 0.15, y + 0.45])) / np.hypot(
        *(top - np.array([x - 0.15, y + 0.45]))
    )
    arrow(ax, start, start + 1.6 * direction, "T")


def draw_link(ax):
    x, y = 3.0, 2.0
    beam(ax, x, y)
    a = np.array([x - 0.2, y])
    b = a + np.array([0.9, -1.3])
    ax.plot([a[0], b[0]], [a[1], b[1]], color="0.2", linewidth=4)
    for p in (a, b):
        ax.add_patch(Circle(p, 0.09, facecolor="white", edgecolor="0.2", zorder=3))
    ground(ax, b[0] - 0.6, b[0] + 0.6, b[1])
    beam(ax, x + OFFSET, y, alpha=0.6)
    direction = (a - b) / np.hypot(*(a - b))
    tip = a + np.array([OFFSET, 0.0])
    arrow(ax, tip - 1.5 * direction, tip, "F", offset=(-22, -10))


def draw_roller(ax):
    x, y = 3.0, 1.4
    beam(ax, x, y)
    ax.add_patch(Circle((x - 0.3, y - 0.22), 0.22, facecolor="white", edgecolor="0.2"))
    ground(ax, x - 1.0, x + 0.4, y - 0.44)
    beam(ax, x + OFFSET, y, alpha=0.6)
    tip = np.array([x + OFFSET - 0.3, y])
    arrow(ax, tip - np.array([0.0, 1.3]), tip, "F_y", offset=(6, -26))


def draw_smooth(ax):
    angle = 25.0
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    for dx, alpha in ((0.0, 1.0), (OFFSET, 0.6)):
        base = np.array([0.6 + dx, 0.6])
        if dx == 0.0:
            ground(ax, base[0], base[0] + 3.3, base[1], angle=angle)
        contact = base + 1.8 * np.array([c, s])
        normal = np.array([-s, c])
        ax.add_patch(
            Circle(
                contact + 0.7 * normal,
                0.7,
                facecolor=BODY_COLOR,
                edgecolor="0.25",
                alpha=alpha,
            )
        )
        if dx > 0.0:
            arrow(ax, contact - 1.3 * normal, contact, "N", offset=(8, -20))


def draw_collar(ax, fixed=False):
    x, y = 3.0, 1.6
    rod_x = x + 0.25
    for dx, alpha in ((0.0, 1.0), (OFFSET, 0.6)):
        beam(ax, x + dx, y, alpha=alpha)
        ax.add_patch(
            Rectangle(
                (rod_x - 0.18 + dx, y - 0.25),
                0.36,
                0.95,
                facecolor="0.55" if fixed else "white",
                edgecolor="0.2",
                linewidth=1.5,
                alpha=alpha,
            )
        )
        if not fixed:
            ax.add_patch(
                Circle(
                    (x + dx - 0.1, y + 0.22),
                    0.08,
                    facecolor="white",
                    edgecolor="0.2",
                    zorder=3,
                )
            )
    ax.plot([rod_x, rod_x], [0.3, 3.4], color="0.2", linewidth=2.5, zorder=0)
    ground(ax, rod_x - 0.5, rod_x + 0.5, 0.3)
    tip = np.array([rod_x + OFFSET - 0.18, y + 0.22])
    arrow(ax, tip + np.array([1.4, 0.0]), tip, "F", offset=(16, 6))
    if fixed:
        moment_arrow(ax, (x + OFFSET - 1.3, y + 0.22), "M")


def draw_pin(ax):
    x, y = 2.8, 1.6
    beam(ax, x, y)
    pin_symbol(ax, x, y)
    ground(ax, x - 0.7, x + 0.7, y - 0.6)
    beam(ax, x + OFFSET, y, alpha=0.6)
    p = np.array([x + OFFSET, y])
    arrow(ax, p, p + np.array([1.3, 0.0]), "A_x", offset=(-4, 6))
    arrow(ax, p - np.array([0.0, 1.3]), p, "A_y", offset=(6, -30))


def draw_fixed(ax):
    x, y = 1.0, 1.6
    wall(ax, x, 0.6, 3.0)
    ax.add_patch(Rectangle((x, y), 2.4, 0.45, facecolor=BODY_COLOR, edgecolor="0.25"))
    xr = x + OFFSET
    ax.add_patch(
        Rectangle((xr, y), 2.4, 0.45, facecolor=BODY_COLOR, edgecolor="0.25", alpha=0.6)
    )
    p = np.array([xr, y + 0.22])
    arrow(ax, p - np.array([1.2, 0.0]), p, "A_x", offset=(-44, -22))
    arrow(
        ax, p - np.array([0.0, 1.2]), p - np.array([0.0, 0.22]), "A_y", offset=(6, -30)
    )
    moment_arrow(ax, p + np.array([0.7, 0.0]), "M_A", radius=0.5)


DRAWERS = {
    "cable": draw_cable,
    "link": draw_link,
    "roller": draw_roller,
    "smooth": draw_smooth,
    "collar": draw_collar,
    "pin": draw_pin,
    "fixed_collar": lambda ax: draw_collar(ax, fixed=True),
    "fixed": draw_fixed,
}


def make_figure():
    fig, axes = plt.subplots(4, 2, figsize=(12.5, 13.5))
    for ax, (key, name, reactions, meaning) in zip(axes.flat, SUPPORTS):
        DRAWERS[key](ax)
        arrow(ax, (4.4, 2.0), (5.4, 2.0), color="0.45")
        n = len(reactions)
        ax.set_title(
            f"{name}: {n} unknown{'s' if n > 1 else ''}\n{meaning}", fontsize=12
        )
        ax.set(xlim=(0, 10.5), ylim=(-0.2, 3.8), aspect="equal")
        ax.axis("off")
    fig.suptitle(
        "Supports (left of each arrow) and the reactions they exert on the body (right)",
        fontsize=14,
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    for key, name, reactions, _ in SUPPORTS:
        print(f"{name:30s} {unknown_count(key)} unknown(s): {', '.join(reactions)}")
    finish_figures(
        {"fundamentals_support_reactions.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
