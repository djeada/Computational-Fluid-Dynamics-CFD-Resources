"""Reduce a coplanar force system on a plate to a force-couple system and a single resultant.

Three forces and a couple act on a 4 m x 2 m plate. The script sums the forces
into the resultant R, sums their moments about the corner O into M_O, and
finds the line of action of the single force that is equivalent to the whole
system (x R_y - y R_x = M_O). The three panels show the original loads, the
equivalent force-couple system at O, and the single resultant on its line of
action at perpendicular distance d = |M_O| / |R| from O.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.path import Path as MplPath

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

PLATE_WIDTH = 4.0  # m
PLATE_HEIGHT = 2.0  # m
# (magnitude N, direction in degrees counterclockwise from +x, point of application m)
FORCES = (
    (400.0, -90.0, (0.5, 2.0)),
    (300.0, -60.0, (2.5, 2.0)),
    (250.0, 180.0, (4.0, 0.5)),
)
COUPLE = 400.0  # applied couple moment (N m), counterclockwise positive
ORIGIN = np.array([0.0, 0.0])  # reduction point O (m)
ARROW_SCALE = 1.0 / 400.0  # drawing length per unit force (m/N)


def force_vectors(forces=FORCES):
    """Return the force vectors (N) and their points of application (m) as arrays."""
    vectors = np.array(
        [
            magnitude * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))])
            for magnitude, a, _ in forces
        ]
    )
    points = np.array([point for _, _, point in forces], dtype=float)
    return vectors, points


def moment_2d(point, force, about=ORIGIN):
    """Moment (N m, counterclockwise positive) of a force about a point: x F_y - y F_x."""
    rx, ry = np.asarray(point, dtype=float) - about
    return rx * force[1] - ry * force[0]


def resultant(vectors, points, couple=COUPLE, about=ORIGIN):
    """Return the resultant force R and the resultant moment M about `about`."""
    total = vectors.sum(axis=0)
    moment = couple + sum(moment_2d(p, f, about) for p, f in zip(points, vectors))
    return total, moment


def line_of_action(total, moment, about=ORIGIN):
    """Return a point on, and the unit direction of, the line where R alone acts.

    The point is the foot of the perpendicular from `about`, so its distance
    from `about` is the moment arm d = |M| / |R|.
    """
    magnitude = np.hypot(*total)
    if magnitude == 0.0:
        raise ValueError("a zero resultant reduces to a pure couple")
    direction = total / magnitude
    normal = np.array([direction[1], -direction[0]])  # unit vector with n x u = 1
    # A point a = s n satisfies a x R = s |R| (n x u) = s |R|, so s = M / |R|.
    return about + normal * moment / magnitude, direction


def axis_intercept(total, moment, y=0.0, about=ORIGIN):
    """Return x where the line of action crosses the horizontal line at height y."""
    return about[0] + (moment + (y - about[1]) * total[0]) / total[1]


def draw_plate(ax):
    ax.add_patch(
        Rectangle(
            (0.0, 0.0),
            PLATE_WIDTH,
            PLATE_HEIGHT,
            facecolor="0.88",
            edgecolor="0.3",
            linewidth=1.5,
        )
    )
    ax.plot(*ORIGIN, "ko", markersize=6)
    ax.annotate("O", ORIGIN, xytext=(-14, -14), textcoords="offset points")


def draw_force(ax, point, force, color, label=None, tail=False):
    """Draw a force arrow. With tail=True the arrow starts at the point, otherwise it ends there."""
    point = np.asarray(point, dtype=float)
    length = force * ARROW_SCALE
    start, end = (point, point + length) if tail else (point - length, point)
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.2,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )
    if label:
        ax.annotate(
            label,
            start if not tail else end,
            xytext=(6, 4),
            textcoords="offset points",
            color=color,
            fontsize=11,
        )


def draw_couple(ax, center, moment, color, label, radius=0.35):
    """Draw a curved arrow for a couple, counterclockwise when moment > 0."""
    theta = np.linspace(np.radians(200), np.radians(-70), 40)
    if moment > 0:
        theta = theta[::-1]
    pts = np.column_stack(
        (center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta))
    )
    ax.add_patch(
        FancyArrowPatch(
            path=MplPath(pts),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=2.0,
            color=color,
        )
    )
    ax.annotate(
        label,
        (center[0] + radius, center[1] + radius),
        xytext=(4, 2),
        textcoords="offset points",
        color=color,
        fontsize=11,
    )


def make_figure(vectors, points, total, moment):
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.0))
    colors = ("tab:blue", "tab:orange", "tab:green")
    red = "tab:red"

    ax = axes[0]
    draw_plate(ax)
    for i, (p, f, (mag, ang, _)) in enumerate(zip(points, vectors, FORCES)):
        draw_force(ax, p, f, colors[i], rf"$F_{i + 1}$ = {mag:.0f} N")
        ax.plot(*p, "o", color=colors[i], markersize=4)
    draw_couple(ax, (2.8, 0.8), COUPLE, "tab:purple", f"C = {COUPLE:.0f} N m")
    ax.set_title("(a) Applied forces and couple")

    ax = axes[1]
    draw_plate(ax)
    draw_force(ax, ORIGIN, total, red, f"R = {np.hypot(*total):.0f} N")
    sense = "counterclockwise" if moment > 0 else "clockwise"
    draw_couple(
        ax, ORIGIN, moment, red, rf"$M_O$ = {abs(moment):.0f} N m {sense}", radius=0.45
    )
    ax.set_title("(b) Equivalent force-couple system at O")

    ax = axes[2]
    draw_plate(ax)
    foot, direction = line_of_action(total, moment)
    span = np.linspace(-3.0, 3.0, 2)
    line = foot[None, :] + span[:, None] * direction[None, :]
    ax.plot(line[:, 0], line[:, 1], "--", color=red, linewidth=1.2)
    x0 = axis_intercept(total, moment, y=PLATE_HEIGHT)
    draw_force(ax, (x0, PLATE_HEIGHT), total, red, "R", tail=True)
    ax.plot([ORIGIN[0], foot[0]], [ORIGIN[1], foot[1]], ":", color="0.2")
    ax.annotate(
        f"d = {np.hypot(*foot):.3f} m",
        foot,
        xytext=(10, -16),
        textcoords="offset points",
        fontsize=11,
    )
    ax.set_title("(c) Single resultant on its line of action")

    for ax in axes:
        ax.set(
            xlim=(-0.9, 4.9),
            ylim=(-0.9, 3.4),
            aspect="equal",
            xlabel="x (m)",
            ylabel="y (m)",
        )
        ax.grid(True, linewidth=0.4, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    vectors, points = force_vectors()
    total, moment = resultant(vectors, points)
    foot, _ = line_of_action(total, moment)
    print(f"R = ({total[0]:.1f}, {total[1]:.1f}) N, |R| = {np.hypot(*total):.1f} N")
    print(f"direction {np.degrees(np.arctan2(total[1], total[0])):.1f} deg from +x")
    print(f"M_O = {moment:.1f} N m (counterclockwise positive)")
    print(f"moment arm d = |M_O|/|R| = {np.hypot(*foot):.3f} m")
    print(
        f"line of action crosses y = 0 at x = {axis_intercept(total, moment):.3f} m "
        f"and y = {PLATE_HEIGHT:.0f} m at x = "
        f"{axis_intercept(total, moment, y=PLATE_HEIGHT):.3f} m"
    )

    finish_figures(
        {
            "fundamentals_force_resultant.png": make_figure(
                vectors, points, total, moment
            )
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
