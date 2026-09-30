"""Sketch boundary-layer growth, separation, and the recirculation region.

A schematic (not a solution of the boundary-layer equations): the edge of an
attached laminar boundary layer grows as sqrt(x - x0) up to a separation point,
after which a separated shear layer lifts away from the wall and encloses a
recirculation region with reversed flow near the wall. Free-stream arrows that
shorten downstream indicate the decelerating outer flow, i.e. an adverse
pressure gradient.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

X_START = -1.0  # leading edge of the drawn wall
X_SEP = 0.0  # separation point
X_END = 1.5  # end of the drawn separated shear layer
DELTA_COEFF = 0.3  # attached edge: delta = DELTA_COEFF * sqrt(x - X_START)
SHEAR_COEFF = 0.5  # separated shear layer height above delta(X_SEP)


def boundary_layer_edge(x):
    """Attached boundary-layer edge, delta ~ sqrt(distance from leading edge)."""
    return DELTA_COEFF * np.sqrt(x - X_START)


def separated_shear_layer(x):
    """Dividing streamline leaving the wall at the separation point."""
    return SHEAR_COEFF * np.sqrt(x - X_SEP)


def make_figure():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Wall
    wall_x = np.linspace(X_START, 2, 100)
    ax.plot(wall_x, np.zeros_like(wall_x), "k-", linewidth=3, label="Wall")
    ax.fill_between(wall_x, -0.2, 0, color="lightgray", hatch="//", edgecolor="gray")

    # Attached boundary layer
    attached_x = np.linspace(X_START, X_SEP, 100)
    attached_y = boundary_layer_edge(attached_x)
    ax.plot(attached_x, attached_y, "b-", linewidth=2, label="Attached Boundary Layer")
    ax.fill_between(attached_x, 0, attached_y, color="blue", alpha=0.1)

    # Separated shear layer enclosing the recirculation region
    separated_x = np.linspace(X_SEP, X_END, 100)
    separated_y = separated_shear_layer(separated_x)
    ax.plot(
        separated_x,
        separated_y,
        "r-",
        linewidth=2,
        label="Separated Shear Layer",
    )
    ax.fill_between(
        separated_x,
        0,
        separated_y,
        color="red",
        alpha=0.1,
        label="Separated Region (Recirculation)",
    )

    # Reversed-flow arrows near the wall inside the recirculation region
    for x_pos in (0.6, 1.0, 1.4):
        ax.annotate(
            "",
            xy=(x_pos - 0.25, 0.06),
            xytext=(x_pos, 0.06),
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
        )
    ax.annotate(
        "",
        xy=(1.3, 0.35),
        xytext=(0.9, 0.3),
        arrowprops=dict(
            arrowstyle="->", color="red", lw=1.5, connectionstyle="arc3,rad=-0.4"
        ),
    )

    # Free-stream arrows, shortening downstream (decelerating outer flow)
    x_arrows = np.linspace(-0.9, 1.2, 5)
    lengths = np.linspace(0.35, 0.15, 5)
    for x_pos, dx in zip(x_arrows, lengths):
        ax.arrow(
            x_pos, 0.8, dx, 0, head_width=0.05, head_length=0.08, fc="green", ec="green"
        )
    ax.text(
        0.15,
        0.9,
        r"Decelerating free stream: $\partial p/\partial x > 0$",
        fontsize=11,
        color="green",
        ha="center",
    )

    # Separation point
    ax.axvline(X_SEP, color="purple", linestyle="--", linewidth=1)
    ax.plot(X_SEP, 0, "o", color="purple", markersize=8)
    ax.text(X_SEP + 0.05, -0.12, "Flow Separation Point", fontsize=12, color="purple")
    ax.annotate(
        "Reversed flow\nnear the wall",
        xy=(1.25, 0.08),
        xytext=(1.55, 0.25),
        arrowprops=dict(facecolor="black", arrowstyle="->"),
    )

    ax.set_title("Flow Separation in Boundary Layers", fontsize=14)
    ax.set_xlabel("Flow Direction (x)", fontsize=12)
    ax.set_ylabel("Vertical Direction (y)", fontsize=12)
    ax.grid(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-0.2, 1)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = make_figure()

    finish_figures(
        {"flow_separation_boundary_layer.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
