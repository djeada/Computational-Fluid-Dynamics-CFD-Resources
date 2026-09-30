"""Sketch of laminar pipe flow: parabolic velocity arrows, no-slip wall and wall shear.

Velocity arrows are drawn across a pipe section with lengths proportional to
the Hagen-Poiseuille profile u(r) = u_max (1 - (r/R)^2). The axial velocity is
drawn in the plane of the figure for illustration.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

ARROW_SCALE = 0.5  # plot length per unit velocity


def poiseuille_velocity(r, pipe_radius, max_velocity):
    """Axial velocity of fully developed laminar pipe flow at radius r."""
    return max_velocity * (1 - (r / pipe_radius) ** 2)


def plot_wall_shear(pipe_radius=1, max_velocity=2, n_radii=5):
    """Draw the annotated pipe sketch and return the figure."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Pipe section
    ax.add_patch(plt.Circle((0, 0), pipe_radius, color="gray", alpha=0.2))

    # Velocity arrows at +r and -r, length proportional to u(r)
    for r in np.linspace(0, pipe_radius, n_radii):
        length = ARROW_SCALE * poiseuille_velocity(r, pipe_radius, max_velocity)
        for y in {r, -r}:
            if length > 0:
                ax.arrow(
                    0,
                    y,
                    length,
                    0,
                    head_width=0.05,
                    head_length=0.1,
                    length_includes_head=True,
                    fc="blue",
                    ec="blue",
                )
            else:
                ax.plot(0, y, "o", color="blue", markersize=5)

    # Envelope of the arrow tips: the parabolic profile
    y_profile = np.linspace(-pipe_radius, pipe_radius, 100)
    ax.plot(
        ARROW_SCALE * poiseuille_velocity(y_profile, pipe_radius, max_velocity),
        y_profile,
        "b--",
        linewidth=1,
    )

    ax.text(
        ARROW_SCALE * max_velocity + 0.2,
        0,
        "Maximum Velocity\n(r = 0)",
        ha="left",
        va="center",
        fontsize=10,
    )
    ax.text(
        -pipe_radius / 2,
        pipe_radius / 2,
        "Velocity gradient\n$du/dr$",
        ha="center",
        va="center",
        fontsize=10,
    )
    ax.annotate(
        "No-slip Condition\n(u = 0)",
        xy=(0, pipe_radius),
        xytext=(-1.5, pipe_radius + 0.2),
        arrowprops=dict(arrowstyle="->"),
        ha="center",
        fontsize=10,
    )
    # Shear is largest at the wall, where the profile is steepest
    ax.annotate(
        "High Shear Region\n(wall)",
        xy=(0.05, -pipe_radius),
        xytext=(1.2, -1.2),
        arrowprops=dict(arrowstyle="->"),
        ha="center",
        fontsize=10,
    )
    ax.text(
        0,
        -1.6,
        "Wall shear ~ friction force that fluid exerts on the pipe walls",
        ha="center",
        fontsize=11,
    )

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Wall Shear in Pipe Cross-Section", fontsize=14)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_wall_shear()

    finish_figures(
        {"wall_shear_pipe_cross_section.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
