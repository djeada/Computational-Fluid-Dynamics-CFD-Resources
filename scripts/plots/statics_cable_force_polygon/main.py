"""Equilibrium of a particle held by cables: free-body diagram, force polygon and cable sag.

A 100 kg mass hangs from two cables at 30 and 45 degrees above the
horizontal. The tensions follow from the two scalar equilibrium equations,
solved as a linear system; the free-body diagram draws them to scale, and the
force polygon (weight and the two tensions placed head to tail) closes, which
is the graphical statement of sum F = 0. The third panel shows how the tension
of a symmetric cable carrying a transverse load grows as T/W = 1/(2 sin theta)
when the sag angle theta shrinks. The same solver handles 3D cable systems.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

GRAVITY = 9.81  # m/s^2
MASS = 100.0  # kg
ANGLE_RIGHT = np.radians(30.0)  # cable 1, above the horizontal, towards +x (rad)
ANGLE_LEFT = np.radians(45.0)  # cable 2, above the horizontal, towards -x (rad)
TRAFFIC_LIGHT_MASS = 20.0  # kg, for the sag example
TRAFFIC_LIGHT_ANGLE = np.radians(15.0)  # rad


def concurrent_tensions(directions, load):
    """Solve sum_i T_i u_i + load = 0 for the tensions T_i of concurrent cables.

    ``directions`` holds one vector per cable pointing from the particle
    towards the anchor (normalised here); ``load`` is the applied force
    vector. The number of cables must equal the dimension (2 or 3).
    """
    u = np.asarray(directions, dtype=float)
    u = u / np.linalg.norm(u, axis=1, keepdims=True)
    return np.linalg.solve(u.T, -np.asarray(load, dtype=float))


def two_cable_closed_form(weight, theta1, theta2):
    """T1 = W cos(theta2)/sin(theta1 + theta2), T2 = W cos(theta1)/sin(theta1 + theta2)."""
    s = np.sin(theta1 + theta2)
    return weight * np.cos(theta2) / s, weight * np.cos(theta1) / s


def arrow(ax, start, vector, color, label=None, text_offset=(0, 0), lw=2.5):
    """Draw a force arrow from start along vector, with an optional label at its middle."""
    end = np.asarray(start) + vector
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "lw": lw,
            "mutation_scale": 18,
        },
    )
    if label:
        mid = np.asarray(start) + 0.5 * np.asarray(vector) + text_offset
        ax.text(*mid, label, color=color, fontsize=11, ha="center", va="center")


def make_figure(weight, t1, t2):
    """Three panels: free-body diagram, force polygon, tension against sag angle."""
    colors = plt.get_cmap("tab10").colors
    u1 = np.array([np.cos(ANGLE_RIGHT), np.sin(ANGLE_RIGHT)])
    u2 = np.array([-np.cos(ANGLE_LEFT), np.sin(ANGLE_LEFT)])
    w = np.array([0.0, -weight])
    scale = 1.0 / weight  # drawing units per newton

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), width_ratios=[1.15, 0.9, 1.1])
    ax = axes[0]
    origin = np.zeros(2)
    ceiling = 1.15
    for u in (u1, u2):
        ax.plot(*np.array([origin, ceiling / u[1] * u]).T, color="0.6", linewidth=1.2)
    ax.plot([-1.5, 2.1], [ceiling, ceiling], color="0.3", linewidth=3)
    arrow(ax, origin, t1 * scale * u1, colors[0])
    arrow(ax, origin, t2 * scale * u2, colors[1])
    arrow(ax, origin, w * scale, colors[3])
    tip1, tip2 = t1 * scale * u1, t2 * scale * u2
    ax.text(
        *(tip1 + [0.08, -0.12]), f"$T_1$ = {t1:.0f} N", color=colors[0], fontsize=11
    )
    ax.text(
        *(tip2 + [-0.08, -0.12]),
        f"$T_2$ = {t2:.0f} N",
        color=colors[1],
        fontsize=11,
        ha="right",
    )
    ax.text(0.08, -0.75, f"$W$ = {weight:.0f} N", color=colors[3], fontsize=11)
    ax.plot(0, 0, "o", color="black", markersize=9, zorder=5)
    for theta, side in ((ANGLE_RIGHT, 1), (ANGLE_LEFT, -1)):
        arc = np.linspace(0, theta, 30)
        r = 0.3
        ax.plot(side * r * np.cos(arc), r * np.sin(arc), color="black", linewidth=0.8)
        ax.text(
            side * (r + 0.05),
            0.04,
            f"{np.degrees(theta):.0f}$^\\circ$",
            ha="left" if side > 0 else "right",
            fontsize=10,
        )
    ax.axhline(0, color="0.8", linewidth=0.8, linestyle="--")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 2.1)
    ax.set_ylim(-1.15, 1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("(a) Free-body diagram, forces to scale")

    ax = axes[1]
    p0 = np.zeros(2)
    p1 = p0 + w * scale
    p2 = p1 + t1 * scale * u1
    p3 = p2 + t2 * scale * u2
    ax.fill(*np.array([p0, p1, p2]).T, color="0.93")
    arrow(ax, p0, p1 - p0, colors[3], "$W$", (-0.1, 0))
    arrow(ax, p1, p2 - p1, colors[0], "$T_1$", (0.1, -0.07))
    arrow(ax, p2, p3 - p2, colors[1], "$T_2$", (0.12, 0.07))
    gap = np.linalg.norm(p3 - p0)
    ax.text(0.05, -0.55, f"closure error\n{gap * weight:.1e} N", fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-0.35, 0.95)
    ax.set_ylim(-1.15, 0.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(r"(b) Force polygon closes: $\sum \mathbf{F} = 0$")

    ax = axes[2]
    theta = np.radians(np.linspace(1.0, 60.0, 400))
    ax.semilogy(
        np.degrees(theta), 1.0 / (2.0 * np.sin(theta)), color=colors[0], linewidth=2
    )
    ratio = 1.0 / (2.0 * np.sin(TRAFFIC_LIGHT_ANGLE))
    tension = ratio * TRAFFIC_LIGHT_MASS * GRAVITY
    ax.plot(np.degrees(TRAFFIC_LIGHT_ANGLE), ratio, "o", color="black", zorder=5)
    ax.annotate(
        f"20 kg light at 15$^\\circ$:\n$T$ = {tension:.0f} N = {ratio:.2f} $W$",
        xy=(np.degrees(TRAFFIC_LIGHT_ANGLE), ratio),
        xytext=(22, 6),
        arrowprops={"arrowstyle": "->"},
        fontsize=9,
    )
    ax.axhline(0.5, color="0.5", linestyle=":", linewidth=1)
    ax.text(38, 0.43, "vertical cables: $T = W/2$", fontsize=9)
    ax.set_xlim(0, 60)
    ax.set_ylim(0.35, 40)
    ax.set_xlabel(r"sag angle $\theta$ below the horizontal (deg)")
    ax.set_ylabel("cable tension / load $T/W$")
    ax.set_title(r"(c) Symmetric cable: $T/W = 1/(2\sin\theta)$")
    ax.grid(True, which="both", linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    weight = MASS * GRAVITY
    u1 = [np.cos(ANGLE_RIGHT), np.sin(ANGLE_RIGHT)]
    u2 = [-np.cos(ANGLE_LEFT), np.sin(ANGLE_LEFT)]
    t1, t2 = concurrent_tensions([u1, u2], [0.0, -weight])
    c1, c2 = two_cable_closed_form(weight, ANGLE_RIGHT, ANGLE_LEFT)
    print(f"2D: T1 = {t1:.1f} N, T2 = {t2:.1f} N (closed form {c1:.1f}, {c2:.1f} N)")

    anchors = [[3.0, 0.0, 4.0], [-2.0, 2.0, 5.0], [1.0, -3.0, 6.0]]  # m, mass at origin
    tensions = concurrent_tensions(anchors, [0.0, 0.0, -500.0])
    print("3D: T_A = {:.1f} N, T_B = {:.1f} N, T_C = {:.1f} N".format(*tensions))

    finish_figures(
        {"statics_cable_force_polygon.png": make_figure(weight, t1, t2)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
