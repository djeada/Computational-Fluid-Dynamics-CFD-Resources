"""Centroids of composite areas from a parts table, checked against the polygon formula.

Panel (a) is a T-section made of a flange and a web; the script computes its
centroid and its second moment of area about the centroidal axis with the
parallel-axis theorem. Panel (b) is a plate made of a rectangle and a
semicircular end, with a circular hole and a triangular corner cut-out
treated as negative areas. Each composite result is checked against the
centroid of the exact boundary, a polygon with finely divided arcs, computed
with the shoelace (Green's theorem) formulas.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Wedge

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# T-section (mm): flange on top of a web, origin at the bottom of the web.
FLANGE = (120.0, 20.0)  # width, thickness
WEB = (20.0, 80.0)  # width, height
# Plate (mm): rectangle with a semicircular right end, a hole and a corner notch.
PLATE = (200.0, 120.0)  # width, height of the rectangular part
HOLE_DIAMETER = 40.0  # centred on the semicircle's centre
NOTCH_LEG = 60.0  # legs of the right-triangle cut from the lower-left corner
ARC_POINTS = 4000  # vertices per arc in the polygon check


def composite_centroid(parts):
    """Return (A, x_bar, y_bar) from (area, x_c, y_c) rows; holes have negative area."""
    table = np.asarray([p[:3] for p in parts], dtype=float)
    area = table[:, 0].sum()
    return area, table[:, 0] @ table[:, 1] / area, table[:, 0] @ table[:, 2] / area


def polygon_centroid(vertices):
    """Area and centroid of a simple polygon (counter-clockwise) by the shoelace formulas."""
    x, y = np.asarray(vertices, dtype=float).T
    xn, yn = np.roll(x, -1), np.roll(y, -1)
    cross = x * yn - xn * y
    area = 0.5 * cross.sum()
    return (
        area,
        ((x + xn) * cross).sum() / (6 * area),
        ((y + yn) * cross).sum() / (6 * area),
    )


def t_section_parts(flange=FLANGE, web=WEB):
    """Rows (area, x_c, y_c, I_c, label) of the T-section, x measured from the web axis."""
    (bf, tf), (bw, hw) = flange, web
    return [
        (bw * hw, 0.0, hw / 2, bw * hw**3 / 12, "1 web"),
        (bf * tf, 0.0, hw + tf / 2, bf * tf**3 / 12, "2 flange"),
    ]


def second_moment(parts, y_bar):
    """I about the horizontal centroidal axis: sum of I_c + A d^2 (parallel-axis theorem)."""
    return sum(i_c + a * (y_c - y_bar) ** 2 for a, _, y_c, i_c, _ in parts)


def plate_parts(plate=PLATE, hole=HOLE_DIAMETER, notch=NOTCH_LEG):
    """Rows (area, x_c, y_c, label) of the plate; the hole and the notch are negative."""
    width, height = plate
    r = height / 2
    return [
        (width * height, width / 2, height / 2, "1 rectangle"),
        (np.pi * r**2 / 2, width + 4 * r / (3 * np.pi), height / 2, "2 semicircle"),
        (-np.pi * hole**2 / 4, width, height / 2, "3 hole"),
        (-(notch**2) / 2, notch / 3, notch / 3, "4 notch"),
    ]


def plate_boundary(plate=PLATE, hole=HOLE_DIAMETER, notch=NOTCH_LEG, n=ARC_POINTS):
    """Outer boundary (counter-clockwise) and hole boundary of the plate as polygons."""
    width, height = plate
    r = height / 2
    arc = np.linspace(-np.pi / 2, np.pi / 2, n)
    outer = np.vstack(
        [
            [[notch, 0.0]],
            np.column_stack([width + r * np.cos(arc), r + r * np.sin(arc)]),
            [[0.0, height], [0.0, notch]],
        ]
    )
    circle = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    inner = np.column_stack(
        [width + hole / 2 * np.cos(circle), r + hole / 2 * np.sin(circle)]
    )
    return outer, inner


def plate_centroid_exact():
    """Centroid of the plate from its boundary polygons (outer minus hole)."""
    outer, inner = plate_boundary()
    a1, x1, y1 = polygon_centroid(outer)
    a2, x2, y2 = polygon_centroid(inner)
    area = a1 - a2
    return area, (a1 * x1 - a2 * x2) / area, (a1 * y1 - a2 * y2) / area


def mark_centroid(ax, x, y, text, big=False):
    """Draw a centroid marker with a label."""
    if big:
        ax.plot(
            x,
            y,
            marker="P",
            markersize=14,
            color="black",
            markeredgecolor="white",
            zorder=6,
        )
        ax.text(
            x + 4,
            y + 4,
            text,
            fontsize=10,
            fontweight="bold",
            zorder=6,
            bbox={
                "boxstyle": "round,pad=0.15",
                "fc": "white",
                "ec": "none",
                "alpha": 0.8,
            },
        )
    else:
        ax.plot(x, y, "o", markersize=6, color="black", zorder=6)
        ax.text(x + 3, y - 9, text, fontsize=9, zorder=6)


def make_figure():
    """Draw the T-section and the plate with part and composite centroids."""
    colors = plt.get_cmap("tab10").colors
    fig, (ax_t, ax_p) = plt.subplots(1, 2, figsize=(12.5, 5.2), width_ratios=[1, 1.6])

    parts = t_section_parts()
    area, _, y_bar = composite_centroid(parts)
    inertia = second_moment(parts, y_bar)
    (bf, tf), (bw, hw) = FLANGE, WEB
    ax_t.add_patch(
        Rectangle((-bw / 2, 0), bw, hw, fc=colors[0], alpha=0.45, ec="black")
    )
    ax_t.add_patch(
        Rectangle((-bf / 2, hw), bf, tf, fc=colors[1], alpha=0.45, ec="black")
    )
    for a, x_c, y_c, _, label in parts:
        mark_centroid(ax_t, x_c, y_c, f"{label}\n$y_c$ = {y_c:.0f}")
    ax_t.axhline(y_bar, color="black", linestyle="--", linewidth=1)
    mark_centroid(ax_t, 0.0, y_bar, f"G, $\\bar y$ = {y_bar:.0f} mm", big=True)
    ax_t.text(
        -bf / 2,
        -14,
        f"$A$ = {area:.0f} mm$^2$, $I_x$ = {inertia / 1e6:.3f}"
        r" $\times 10^6$ mm$^4$",
        fontsize=10,
    )
    ax_t.set_xlim(-bf / 2 - 10, bf / 2 + 10)
    ax_t.set_ylim(-22, hw + tf + 10)
    ax_t.set_title("(a) T-section: centroid and centroidal $I_x$")

    plate = plate_parts()
    width, height = PLATE
    r = height / 2
    ax_p.add_patch(
        Rectangle((0, 0), width, height, fc=colors[0], alpha=0.35, ec="black")
    )
    ax_p.add_patch(Wedge((width, r), r, -90, 90, fc=colors[1], alpha=0.35, ec="black"))
    ax_p.add_patch(
        Circle(
            (width, r), HOLE_DIAMETER / 2, fc="white", ec="black", hatch="//", zorder=3
        )
    )
    ax_p.add_patch(
        Polygon(
            [[0, 0], [NOTCH_LEG, 0], [0, NOTCH_LEG]],
            closed=True,
            fc="white",
            ec="black",
            hatch="//",
            zorder=3,
        )
    )
    offsets = {
        "1 rectangle": (0, 0),
        "2 semicircle": (0, 18),
        "3 hole": (0, -14),
        "4 notch": (0, 0),
    }
    for a, x_c, y_c, label in plate:
        dx, dy = offsets[label]
        sign = "+" if a > 0 else "−"
        mark_centroid(ax_p, x_c, y_c, "")
        ax_p.text(
            x_c + 3 + dx,
            y_c - 9 + dy,
            f"{label} ({sign})",
            fontsize=9,
            zorder=6,
            bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none"},
        )
    area_p, x_bar, y_bar_p = composite_centroid(plate)
    mark_centroid(ax_p, x_bar, y_bar_p, f"G ({x_bar:.1f}, {y_bar_p:.1f}) mm", big=True)
    ax_p.set_xlim(-10, width + r + 15)
    ax_p.set_ylim(-10, height + 12)
    ax_p.set_title("(b) Plate with hole and notch (hatched = negative area)")

    for ax in (ax_t, ax_p):
        ax.set_aspect("equal")
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.grid(True, linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    parts = t_section_parts()
    area, _, y_bar = composite_centroid(parts)
    print(
        f"T-section: A = {area:.0f} mm^2, y_bar = {y_bar:.2f} mm, "
        f"I_x = {second_moment(parts, y_bar):.0f} mm^4"
    )

    print(f"{'part':<14}{'A (mm^2)':>12}{'x_c (mm)':>11}{'y_c (mm)':>11}")
    for a, x_c, y_c, label in plate_parts():
        print(f"{label:<14}{a:12.1f}{x_c:11.2f}{y_c:11.2f}")
    area_p, x_bar, y_bar_p = composite_centroid(plate_parts())
    exact = plate_centroid_exact()
    print(
        f"plate, parts table: A = {area_p:.1f} mm^2, centroid ({x_bar:.3f}, {y_bar_p:.3f}) mm"
    )
    print(
        f"plate, boundary polygon: A = {exact[0]:.1f} mm^2, "
        f"centroid ({exact[1]:.3f}, {exact[2]:.3f}) mm"
    )

    finish_figures(
        {"statics_composite_centroid.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
