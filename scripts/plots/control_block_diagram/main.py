"""Block diagram of a single-loop feedback control system with disturbance and sensor noise.

Draws the reference r, the error e, the controller C(s), the actuator, the
input disturbance d, the plant G(s), the output y, and the sensor H(s) whose
reading is corrupted by noise n before it is compared with the reference.
Below each block, the matching element of a car cruise-control loop is named.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

BLOCK_W, BLOCK_H = 1.6, 0.9  # block size (axis units)
SUM_R = 0.22  # radius of a summing junction
Y_MAIN, Y_FEEDBACK = 2.2, 0.2  # heights of the forward and feedback paths
FONT = 12
EXAMPLE_COLOR = "0.35"


def block(ax, x, y, text, color):
    """Rounded box centred at (x, y); returns its left and right edge x."""
    patch = FancyBboxPatch(
        (x - BLOCK_W / 2, y - BLOCK_H / 2),
        BLOCK_W,
        BLOCK_H,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        fc=color,
        ec="k",
        lw=1.5,
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=FONT)
    return x - BLOCK_W / 2, x + BLOCK_W / 2


def summing_junction(ax, x, y, signs):
    """Circle with the given signs placed at (dx, dy) offsets."""
    ax.add_patch(Circle((x, y), SUM_R, fc="white", ec="k", lw=1.5))
    for sign, (dx, dy) in signs:
        ax.text(x + dx, y + dy, sign, ha="center", va="center", fontsize=FONT + 1)


def arrow(ax, points, label=None, label_at=0, offset=(0.0, 0.18)):
    """Polyline arrow through points; optional label near segment label_at."""
    for (x0, y0), (x1, y1) in zip(points[:-2], points[1:-1]):
        ax.plot([x0, x1], [y0, y1], color="k", lw=1.5)
    ax.add_patch(
        FancyArrowPatch(
            points[-2],
            points[-1],
            arrowstyle="-|>",
            mutation_scale=16,
            lw=1.5,
            color="k",
        )
    )
    if label:
        (x0, y0), (x1, y1) = points[label_at], points[label_at + 1]
        ax.text(
            (x0 + x1) / 2 + offset[0],
            (y0 + y1) / 2 + offset[1],
            label,
            ha="center",
            va="bottom",
            fontsize=FONT,
        )


def make_figure():
    fig, ax = plt.subplots(figsize=(13, 4.6))
    blue, orange, green, grey = "#cfe2f3", "#fde3c8", "#d5ecd4", "#e6e6e6"

    x_sum1, x_c, x_a, x_sum2, x_g, x_out = 1.0, 3.2, 6.5, 8.5, 10.5, 13.2
    summing_junction(ax, x_sum1, Y_MAIN, [("+", (-0.32, 0.3)), ("−", (-0.32, -0.36))])
    c_l, c_r = block(ax, x_c, Y_MAIN, "Controller\n$C(s)$", blue)
    a_l, a_r = block(ax, x_a, Y_MAIN, "Actuator", orange)
    summing_junction(ax, x_sum2, Y_MAIN, [("+", (-0.3, -0.32)), ("+", (0.32, 0.32))])
    g_l, g_r = block(ax, x_g, Y_MAIN, "Plant\n$G(s)$", green)
    x_h = 8.0
    h_l, h_r = block(ax, x_h, Y_FEEDBACK, "Sensor\n$H(s)$", grey)
    x_sum3 = 3.0
    summing_junction(
        ax, x_sum3, Y_FEEDBACK, [("+", (0.32, 0.3)), ("+", (-0.32, -0.32))]
    )

    arrow(
        ax,
        [(-1.0, Y_MAIN), (x_sum1 - SUM_R, Y_MAIN)],
        "reference $r$",
        offset=(-0.3, 0.18),
    )
    arrow(ax, [(x_sum1 + SUM_R, Y_MAIN), (c_l, Y_MAIN)], "error $e$")
    arrow(ax, [(c_r, Y_MAIN), (a_l, Y_MAIN)], "command $u$")
    arrow(ax, [(a_r, Y_MAIN), (x_sum2 - SUM_R, Y_MAIN)])
    arrow(
        ax,
        [(x_sum2, Y_MAIN + 1.2), (x_sum2, Y_MAIN + SUM_R)],
        "disturbance $d$",
        offset=(0.0, 0.62),
    )
    arrow(ax, [(x_sum2 + SUM_R, Y_MAIN), (g_l, Y_MAIN)])
    arrow(ax, [(g_r, Y_MAIN), (x_out, Y_MAIN)], "output $y$")
    x_tap = 12.0
    ax.plot(x_tap, Y_MAIN, "ko", ms=5)
    arrow(ax, [(x_tap, Y_MAIN), (x_tap, Y_FEEDBACK), (h_r, Y_FEEDBACK)])
    arrow(ax, [(h_l, Y_FEEDBACK), (x_sum3 + SUM_R, Y_FEEDBACK)])
    arrow(ax, [(x_sum3, Y_FEEDBACK - 1.0), (x_sum3, Y_FEEDBACK - SUM_R)])
    ax.text(
        x_sum3, Y_FEEDBACK - 1.05, "noise $n$", ha="center", va="top", fontsize=FONT
    )
    arrow(
        ax,
        [(x_sum3 - SUM_R, Y_FEEDBACK), (x_sum1, Y_FEEDBACK), (x_sum1, Y_MAIN - SUM_R)],
    )
    ax.text(
        x_sum1 - 0.15, 1.0, "measurement $y_m$", ha="right", va="center", fontsize=FONT
    )

    # cruise-control example under each element
    examples = (
        (-0.3, Y_MAIN - 0.35, "center", "set speed"),
        (x_c, Y_MAIN - 0.75, "center", "engine control unit"),
        (x_a, Y_MAIN - 0.75, "center", "throttle and engine"),
        (x_sum2 + 0.15, Y_MAIN + 0.8, "left", "road grade, headwind"),
        (x_g, Y_MAIN - 0.75, "center", "car mass and drag"),
        (x_out - 0.6, Y_MAIN - 0.35, "center", "speed"),
        (x_h, Y_FEEDBACK - 0.75, "center", "wheel-speed sensor"),
    )
    for x, y, ha, text in examples:
        ax.text(
            x,
            y,
            text,
            ha=ha,
            va="center",
            fontsize=FONT - 1,
            color=EXAMPLE_COLOR,
            style="italic",
        )

    ax.set_xlim(-1.2, 13.5)
    ax.set_ylim(-1.5, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        "Single-loop feedback control (italic: the cruise-control example)",
        fontsize=FONT + 1,
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    finish_figures(
        {"control_block_diagram.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
