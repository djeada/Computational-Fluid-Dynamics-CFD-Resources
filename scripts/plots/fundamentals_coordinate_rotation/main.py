"""Transform the components of a force between two rotated coordinate frames.

A 500 N force with components (300, 400) N in the frame xy is expressed in a
frame x'y' rotated counterclockwise by 30 degrees, using the rotation matrix
whose rows are the unit vectors of the new axes written in the old frame. The
left panel shows the vector, both frames and the projections onto them. The
right panel sweeps the rotation angle from 0 to 360 degrees: the components
change as cosines and sines while the magnitude stays at 500 N.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

FORCE = np.array([300.0, 400.0])  # components in the xy frame (N)
ANGLE = 30.0  # rotation of the x'y' frame relative to xy, counterclockwise (deg)
SWEEP = np.linspace(0.0, 360.0, 361)  # rotation angles for the sweep (deg)
AXIS_LENGTH = 560.0  # drawn length of the frame axes (N, same scale as FORCE)


def rotation_matrix(theta_deg):
    """2D transformation matrix: rows are the new unit vectors e_x', e_y' in the old frame.

    Components transform as F' = Q F, and back as F = Q^T F.
    """
    t = np.radians(theta_deg)
    return np.array([[np.cos(t), np.sin(t)], [-np.sin(t), np.cos(t)]])


def rotation_matrix_z(theta_deg):
    """3D transformation matrix for a rotation of the frame by theta about the z axis."""
    q = np.eye(3)
    q[:2, :2] = rotation_matrix(theta_deg)
    return q


def transform(vector, theta_deg):
    """Components of `vector` in a frame rotated by theta_deg."""
    return rotation_matrix(theta_deg) @ np.asarray(vector, dtype=float)


def draw_arrow(ax, start, end, color, width=2.0, style="-|>", ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=16,
            linewidth=width,
            color=color,
            linestyle=ls,
            shrinkA=0,
            shrinkB=0,
        )
    )


def make_figure():
    q = rotation_matrix(ANGLE)
    f_new = q @ FORCE
    fig, (ax, sweep) = plt.subplots(1, 2, figsize=(12.5, 5.6))

    origin = np.zeros(2)
    for direction, name, color in (
        (np.array([1.0, 0.0]), "x", "0.3"),
        (np.array([0.0, 1.0]), "y", "0.3"),
        (q[0], "x'", "tab:orange"),
        (q[1], "y'", "tab:orange"),
    ):
        tip = AXIS_LENGTH * direction
        draw_arrow(ax, origin, tip, color, width=1.2, style="->")
        ax.annotate(name, tip, xytext=(4, 4), textcoords="offset points", color=color)

    draw_arrow(ax, origin, FORCE, "tab:blue", width=2.6)
    ax.annotate(
        "F = (300, 400) N",
        FORCE,
        xytext=(6, 4),
        textcoords="offset points",
        color="tab:blue",
        fontsize=11,
    )
    # Projections onto the old axes.
    ax.plot([FORCE[0], FORCE[0]], [0, FORCE[1]], ":", color="0.4")
    ax.plot([0, FORCE[0]], [FORCE[1], FORCE[1]], ":", color="0.4")
    # Projections onto the new axes.
    for k in (0, 1):
        foot = f_new[k] * q[k]
        ax.plot(
            [FORCE[0], foot[0]],
            [FORCE[1], foot[1]],
            "--",
            color="tab:orange",
            linewidth=1,
        )
        ax.plot(*foot, "o", color="tab:orange", markersize=4)
    ax.annotate(
        f"$F_{{x'}}$ = {f_new[0]:.1f} N",
        f_new[0] * q[0],
        xytext=(8, -14),
        textcoords="offset points",
        color="tab:orange",
        fontsize=11,
    )
    ax.annotate(
        f"$F_{{y'}}$ = {f_new[1]:.1f} N",
        f_new[1] * q[1],
        xytext=(-110, 0),
        textcoords="offset points",
        color="tab:orange",
        fontsize=11,
    )
    ax.set(
        xlim=(-380, 640),
        ylim=(-60, 620),
        aspect="equal",
        xlabel="force component along x (N)",
        ylabel="force component along y (N)",
        title=rf"(a) Components in xy and in x'y' rotated by {ANGLE:.0f}$^\circ$",
    )
    ax.grid(True, linewidth=0.4, alpha=0.4)

    comps = np.array([transform(FORCE, t) for t in SWEEP])
    sweep.plot(SWEEP, comps[:, 0], color="tab:blue", linewidth=2, label="$F_{x'}$")
    sweep.plot(SWEEP, comps[:, 1], color="tab:orange", linewidth=2, label="$F_{y'}$")
    sweep.plot(SWEEP, np.linalg.norm(comps, axis=1), "k--", linewidth=1.5, label="|F|")
    sweep.axvline(ANGLE, color="0.5", linewidth=0.8)
    sweep.set(
        xlim=(0, 360),
        ylim=(-560, 700),
        xticks=np.arange(0, 361, 60),
        xlabel=r"frame rotation $\theta$ (deg)",
        ylabel="component (N)",
        title="(b) Components change with the frame, the magnitude does not",
    )
    sweep.legend(loc="upper center", ncol=3, fontsize=10)
    sweep.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    q = rotation_matrix(ANGLE)
    f_new = q @ FORCE
    print(
        f"Q(30 deg) = [[{q[0, 0]:.4f}, {q[0, 1]:.4f}], [{q[1, 0]:.4f}, {q[1, 1]:.4f}]]"
    )
    print(
        f"F' = ({f_new[0]:.2f}, {f_new[1]:.2f}) N, |F'| = {np.linalg.norm(f_new):.2f} N"
    )
    print(f"Q^T F' = {q.T @ f_new} N (recovers F)")
    finish_figures(
        {"fundamentals_coordinate_rotation.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
