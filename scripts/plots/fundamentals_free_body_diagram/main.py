"""Turn a loaded, supported beam into its free-body diagram and solve for the reactions.

An 8 m beam has a pin at A and a roller at B. It carries an inclined 20 kN
point load and a 5 kN/m uniform load over its last 3 m. The top panel is the
space diagram with the supports drawn as symbols; the bottom panel is the
free-body diagram, where the supports are replaced by the unknown reactions
A_x, A_y and B_y, the distributed load by its resultant at the centroid, and
the reactions are solved from the three equilibrium equations of a planar
rigid body. The script prints the reactions and checks the moment sum about B.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LENGTH = 8.0  # beam length (m); pin at x = 0, roller at x = LENGTH
POINT_LOADS = ((3.0, 20.0, -60.0),)  # (x m, magnitude kN, angle deg from +x)
DISTRIBUTED_LOADS = ((5.0, 8.0, 5.0, 5.0),)  # (x0 m, x1 m, w0 kN/m, w1 kN/m), downward
ARROW_SCALE = 0.08  # drawing length per kN (m/kN)


def point_load_components(loads=POINT_LOADS):
    """Return (x, F_x, F_y) in m and kN for each point load."""
    return [
        (x, p * np.cos(np.radians(a)), p * np.sin(np.radians(a))) for x, p, a in loads
    ]


def distributed_resultant(x0, x1, w0, w1):
    """Resultant (kN, downward) and centroid (m) of a linearly varying load."""
    resultant = 0.5 * (w0 + w1) * (x1 - x0)
    if resultant == 0.0:
        return 0.0, 0.5 * (x0 + x1)
    centroid = x0 + (x1 - x0) * (w0 + 2.0 * w1) / (3.0 * (w0 + w1))
    return resultant, centroid


def beam_reactions(
    length=LENGTH, point_loads=POINT_LOADS, distributed=DISTRIBUTED_LOADS
):
    """Solve a pin-roller beam: return A_x, A_y, B_y in kN (positive right and up).

    Equilibrium: sum F_x = 0, sum F_y = 0 and sum M_A = 0 (counterclockwise
    positive), with every applied load acting on the beam axis y = 0.
    """
    fx = fy = moment_a = 0.0
    for x, px, py in point_load_components(point_loads):
        fx += px
        fy += py
        moment_a += x * py
    for x0, x1, w0, w1 in distributed:
        r, xc = distributed_resultant(x0, x1, w0, w1)
        fy -= r
        moment_a -= xc * r
    b_y = -moment_a / length
    a_y = -fy - b_y
    a_x = -fx
    return a_x, a_y, b_y


def equilibrium_residual(reactions, length=LENGTH):
    """Return (sum F_x, sum F_y, sum M_B) with the reactions included; all should vanish."""
    a_x, a_y, b_y = reactions
    fx, fy = a_x, a_y + b_y
    moment_b = -a_y * length  # A_y at distance L to the left of B
    for x, px, py in point_load_components():
        fx += px
        fy += py
        moment_b += (x - length) * py
    for x0, x1, w0, w1 in DISTRIBUTED_LOADS:
        r, xc = distributed_resultant(x0, x1, w0, w1)
        fy -= r
        moment_b -= (xc - length) * r
    return fx, fy, moment_b


def force_arrow(
    ax, tip, vector, color, label, offset=(6, 4), dashed=False, from_point=False
):
    """Draw a force of `vector` kN whose head (or tail, if from_point) is at `tip`."""
    tip = np.asarray(tip, dtype=float)
    start = tip - ARROW_SCALE * np.asarray(vector, dtype=float)
    if from_point:
        start, tip = tip, 2.0 * tip - start
    ax.add_patch(
        FancyArrowPatch(
            start,
            tip,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=2.2,
            color=color,
            linestyle="--" if dashed else "-",
            shrinkA=0,
            shrinkB=0,
        )
    )
    ax.annotate(
        label,
        start,
        xytext=offset,
        textcoords="offset points",
        color=color,
        fontsize=11,
    )


def draw_beam(ax, alpha=1.0):
    ax.add_patch(
        Rectangle(
            (0.0, 0.0),
            LENGTH,
            0.25,
            facecolor="0.80",
            edgecolor="0.25",
            alpha=alpha,
            zorder=2,
        )
    )


def draw_supports(ax):
    ax.add_patch(
        Polygon(
            [[0, 0], [-0.3, -0.55], [0.3, -0.55]],
            facecolor="white",
            edgecolor="0.2",
            linewidth=1.5,
        )
    )
    ax.add_patch(Circle((LENGTH, -0.25), 0.25, facecolor="white", edgecolor="0.2"))
    for x0, y in ((0.0, -0.55), (LENGTH, -0.5)):
        ax.plot([x0 - 0.6, x0 + 0.6], [y, y], color="0.35", linewidth=2)
        for t in np.linspace(x0 - 0.5, x0 + 0.5, 6):
            ax.plot([t, t - 0.15], [y, y - 0.2], color="0.35", linewidth=1)


def draw_loads(ax):
    for x, px, py in point_load_components():
        force_arrow(
            ax,
            (x, 0.25),
            (px, py),
            "tab:blue",
            rf"P = {np.hypot(px, py):.0f} kN at {np.degrees(np.arctan2(-py, px)):.0f}$^\circ$",
        )
    for x0, x1, w0, w1 in DISTRIBUTED_LOADS:
        xs = np.linspace(x0, x1, 7)
        ws = np.interp(xs, (x0, x1), (w0, w1))
        top = 0.25 + ARROW_SCALE * 4 * ws
        ax.plot(xs, top, color="tab:green", linewidth=1.5)
        for xi, ti in zip(xs, top):
            ax.add_patch(
                FancyArrowPatch(
                    (xi, ti),
                    (xi, 0.25),
                    arrowstyle="-|>",
                    mutation_scale=10,
                    color="tab:green",
                    shrinkA=0,
                    shrinkB=0,
                )
            )
        ax.annotate(
            f"w = {w0:.0f} kN/m",
            (x0, top[0]),
            xytext=(0, 6),
            textcoords="offset points",
            color="tab:green",
            fontsize=11,
        )


def make_figure(reactions):
    a_x, a_y, b_y = reactions
    fig, (space, fbd) = plt.subplots(2, 1, figsize=(11, 8.0))

    draw_beam(space)
    draw_supports(space)
    draw_loads(space)
    space.annotate("A (pin)", (0, -0.6), xytext=(-20, -26), textcoords="offset points")
    space.annotate(
        "B (roller)", (LENGTH, -0.6), xytext=(-24, -26), textcoords="offset points"
    )
    space.set_title("(a) Space diagram: beam, supports and applied loads")

    draw_beam(fbd, alpha=0.6)
    for x, px, py in point_load_components():
        force_arrow(
            fbd, (x, 0.25), (px, py), "tab:blue", f"P = {np.hypot(px, py):.0f} kN"
        )
    for x0, x1, w0, w1 in DISTRIBUTED_LOADS:
        r, xc = distributed_resultant(x0, x1, w0, w1)
        force_arrow(
            fbd,
            (xc, 0.25),
            (0.0, -r),
            "tab:green",
            f"wL = {r:.0f} kN at x = {xc:.1f} m",
            offset=(-60, 6),
            dashed=True,
        )
    red = "tab:red"
    force_arrow(
        fbd,
        (0.0, 0.125),
        (a_x, 0.0),
        red,
        rf"$A_x$ = {abs(a_x):.2f} kN",
        offset=(-30, 8),
        from_point=a_x < 0,
    )
    force_arrow(fbd, (0.0, 0.0), (0.0, a_y), red, rf"$A_y$ = {a_y:.2f} kN", (6, 0))
    force_arrow(fbd, (LENGTH, 0.0), (0.0, b_y), red, rf"$B_y$ = {b_y:.2f} kN", (6, 0))
    fbd.set_title("(b) Free-body diagram with the reactions solved from equilibrium")

    for ax in (space, fbd):
        ax.set(
            xlim=(-1.6, LENGTH + 1.4),
            ylim=(-1.8, 2.3),
            aspect="equal",
            xlabel="x (m)",
        )
        ax.set_yticks([])
        for side in ("left", "right", "top"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    reactions = beam_reactions()
    a_x, a_y, b_y = reactions
    print(f"A_x = {a_x:.3f} kN, A_y = {a_y:.3f} kN, B_y = {b_y:.3f} kN")
    fx, fy, mb = equilibrium_residual(reactions)
    print(
        f"check: sum F_x = {fx:.1e} kN, sum F_y = {fy:.1e} kN, sum M_B = {mb:.1e} kN m"
    )
    finish_figures(
        {"fundamentals_free_body_diagram.png": make_figure(reactions)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
