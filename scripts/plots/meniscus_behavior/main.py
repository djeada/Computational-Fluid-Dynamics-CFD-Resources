"""Sketch the meniscus of water and of mercury in a glass tube.

Two side-by-side panels show (a) water, which wets glass and forms a concave
meniscus that rises above the outside level, and (b) mercury, which does not
wet glass and forms a convex meniscus below the outside level. Each meniscus
is drawn as the parabola y = +/- 0.5 x^2 between the tube walls, and the
contact angle implied by that shape is computed and annotated.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

CURVATURE = 0.5  # meniscus shape y = +/- CURVATURE * x**2 [1/length]
X_WALL = 1.0  # inner radius of the tube, walls at x = +/- X_WALL [length]
X_OUTSIDE = 2.0  # half-width of the drawing, liquid outside the tube [length]
OUTSIDE_LEVEL = 0.3  # distance between the meniscus apex and the outside level [length]


def meniscus_height(x, wetting, curvature=CURVATURE):
    """Height of the liquid surface inside the tube (apex at y = 0)."""
    sign = 1.0 if wetting else -1.0
    return sign * curvature * x**2


def contact_angle_deg(wetting, curvature=CURVATURE, x_wall=X_WALL):
    """Contact angle, measured through the liquid, where the parabola meets the wall.

    The wall is vertical, so the angle between the wall and the free surface
    is 90 degrees minus the surface inclination dy/dx at x = x_wall.
    """
    sign = 1.0 if wetting else -1.0
    slope = sign * 2.0 * curvature * x_wall
    return 90.0 - np.degrees(np.arctan(slope))


def draw_panel(ax, wetting, name, line_color, fill_color, alpha, text_color):
    """Draw one tube with its meniscus, the outside liquid level and labels."""
    theta = contact_angle_deg(wetting)
    outside = -OUTSIDE_LEVEL if wetting else OUTSIDE_LEVEL
    y_bottom, y_top = (-0.8, 1.0) if wetting else (-1.0, 0.8)

    # Liquid inside the tube, below the meniscus
    x_in = np.linspace(-X_WALL, X_WALL, 100)
    y_in = meniscus_height(x_in, wetting)
    ax.fill_between(x_in, y_bottom, y_in, color=fill_color, alpha=alpha)
    ax.plot(x_in, y_in, color=fill_color, linewidth=3)

    # Liquid outside the tube: flat free surface
    for side in (-1, 1):
        x_out = np.array([side * X_WALL, side * X_OUTSIDE])
        ax.fill_between(x_out, y_bottom, outside, color=fill_color, alpha=alpha)
        ax.plot(x_out, [outside, outside], line_color, linewidth=2)

    # Glass tube walls
    for side in (-1, 1):
        ax.plot(
            [side * X_WALL, side * X_WALL],
            [y_bottom, y_top],
            color="dimgray",
            linewidth=4,
        )

    # Height difference between the meniscus apex and the outside level
    ax.annotate(
        "",
        xy=(0, 0),
        xytext=(0, outside),
        arrowprops=dict(arrowstyle="<->", color=text_color),
    )
    ax.text(
        0.08, outside / 2, "h > 0" if wetting else "h < 0", va="center", fontsize=10
    )

    label_y = 0.6 if wetting else -0.8
    ax.text(
        0,
        label_y,
        "Water climbs" if wetting else "Mercury dips",
        ha="center",
        fontsize=12,
        color=text_color,
    )
    ax.text(
        -1.5,
        outside + (0.08 if wetting else -0.25),
        f"flat {name}\nsurface outside",
        ha="center",
        fontsize=9,
    )
    wall_contact = meniscus_height(X_WALL, wetting)
    ax.text(
        1.1,
        wall_contact + (0.15 if wetting else 0.0),
        rf"$\theta_c = {theta:.0f}^\circ$"
        + ("\n(< 90°, wetting)" if wetting else "\n(> 90°, non-wetting)"),
        ha="left",
        va="center",
        fontsize=10,
    )

    ax.set_xlim(-X_OUTSIDE, X_OUTSIDE)
    ax.set_ylim(y_bottom, y_top)
    ax.axis("off")


def plot_menisci():
    """Create the two-panel figure and return it."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    draw_panel(axes[0], True, "water", "navy", "skyblue", 0.4, "navy")
    axes[0].set_title("(a) Water in Glass: Upward Meniscus", fontsize=14)
    draw_panel(axes[1], False, "mercury", "grey", "silver", 0.6, "black")
    axes[1].set_title("(b) Mercury in Glass: Downward Meniscus", fontsize=14)
    fig.suptitle("Visualization of Meniscus Behavior", fontsize=16)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for wetting, name in ((True, "water"), (False, "mercury")):
        print(
            f"{name}: contact angle of the sketched meniscus = {contact_angle_deg(wetting):.0f} deg"
        )

    fig = plot_menisci()

    finish_figures(
        {"meniscus_behavior.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
