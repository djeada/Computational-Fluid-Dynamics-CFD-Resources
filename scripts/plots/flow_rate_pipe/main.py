"""Draw a side view of a circular pipe and annotate its volumetric flow rate.

The cross-sectional area A = pi r^2 and flow rate Q = A v are computed for a
uniform (plug) velocity v. The pipe is drawn as a rectangle of height 2r with
flow arrows whose length is proportional to v, inlet and outlet labels, and a
text box listing r, L, v, A, and Q.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

PIPE_RADIUS = 0.1  # m
VELOCITY = 2.0  # mean (plug) velocity, m/s
PIPE_LENGTH = 5.0  # m
ARROW_TIME = 0.2  # s; arrow length = velocity * ARROW_TIME (0.4 m at 2 m/s)


def flow_rate(pipe_radius, velocity):
    """Return (area, Q) for a circular pipe with a uniform velocity profile."""
    area = np.pi * pipe_radius**2  # m^2
    return area, area * velocity  # m^3/s


def plot_flow_rate(pipe_radius=PIPE_RADIUS, velocity=VELOCITY, length=PIPE_LENGTH):
    """Return a figure showing the pipe, flow arrows, and computed A and Q."""
    area, q = flow_rate(pipe_radius, velocity)

    fig, ax = plt.subplots(figsize=(10, 4))

    # Draw the pipe (side view)
    ax.add_patch(
        plt.Rectangle(
            (0, -pipe_radius), length, 2 * pipe_radius, color="gray", alpha=0.3
        )
    )

    # Flow arrows, length proportional to the velocity
    arrow_length = velocity * ARROW_TIME
    x_positions = np.linspace(0.5, length - 0.5 - arrow_length, 8)
    y_positions = np.linspace(-pipe_radius * 0.8, pipe_radius * 0.8, 5)
    for x in x_positions:
        for y in y_positions:
            ax.annotate(
                "",
                xy=(x + arrow_length, y),
                xytext=(x, y),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="blue"),
            )

    # Inlet and outlet labels beside the pipe ends
    ax.text(-0.1, 0, "Inlet", ha="right", va="center", fontsize=11)
    ax.text(length + 0.1, 0, "Outlet", ha="left", va="center", fontsize=11)

    # Computed values below the pipe
    ax.text(
        length / 2,
        -pipe_radius * 1.5,
        f"r = {pipe_radius:g} m, L = {length:g} m, v = {velocity:g} m/s\n"
        f"A = πr² = {area:.4f} m²,  Q = A·v = {q:.4f} m³/s",
        ha="center",
        va="top",
        fontsize=12,
        color="black",
    )

    ax.set_xlim(-1.0, length + 1.0)
    ax.set_ylim(-pipe_radius * 6, pipe_radius * 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Flow Rate Through a Pipe")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_flow_rate()

    finish_figures(
        {"flow_rate_pipe.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
