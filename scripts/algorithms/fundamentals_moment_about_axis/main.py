"""Compute the moment of a 3D force about a point and about an axis, and show which parts are invariant.

The force F = (100, -200, 50) N acts at P = (0.3, 0.4, 0.2) m. Its moment
about the origin is M_O = r x F, and its moment about the axis through O with
direction (2, 1, 2) is the projection M_a = u . (r x F), a scalar triple
product. The left panel draws r, F, M_O and the projection of M_O on the axis
in 3D. The right panel moves the reference point along the axis and the point
of application along the line of action: the moment about a point changes,
the moment about the axis does not.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

FORCE = np.array([100.0, -200.0, 50.0])  # N
POINT = np.array([0.3, 0.4, 0.2])  # point of application P (m)
AXIS_POINT = np.array([0.0, 0.0, 0.0])  # a point on the axis (m)
AXIS_DIRECTION = np.array([2.0, 1.0, 2.0])  # direction of the axis (any length)
SHIFTS = np.linspace(-1.0, 1.0, 81)  # shifts along the axis and line of action (m)
FORCE_SCALE = 1.0 / 600.0  # drawing length per unit force (m/N)
MOMENT_SCALE = 1.0 / 250.0  # drawing length per unit moment (m/(N m))


def unit(vector):
    """Return the unit vector along `vector`."""
    vector = np.asarray(vector, dtype=float)
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        raise ValueError("zero vector has no direction")
    return vector / norm


def moment_about_point(about, point, force):
    """Moment (N m) about `about` of `force` (N) applied at `point` (m): r x F."""
    return np.cross(np.asarray(point) - np.asarray(about), force)


def moment_about_axis(axis_point, axis_direction, point, force):
    """Scalar moment about an axis: u . (r x F), r from any axis point to any point on F."""
    u = unit(axis_direction)
    r = np.asarray(point) - np.asarray(axis_point)
    return float(np.linalg.det(np.vstack((u, r, force))))


def split_moment(moment, axis_direction):
    """Split a moment vector into components parallel and perpendicular to an axis."""
    u = unit(axis_direction)
    parallel = np.dot(moment, u) * u
    return parallel, moment - parallel


def invariance_study(shifts=SHIFTS):
    """Moments as the reference point slides along the axis and F slides along its line.

    Returns |M_Q| for Q = A + s u, the axis moment for each Q, and the axis moment
    for each point of application P + s F/|F|.
    """
    u = unit(AXIS_DIRECTION)
    f_hat = unit(FORCE)
    point_moment = np.array(
        [
            np.linalg.norm(moment_about_point(AXIS_POINT + s * u, POINT, FORCE))
            for s in shifts
        ]
    )
    axis_moment_q = np.array(
        [moment_about_axis(AXIS_POINT + s * u, u, POINT, FORCE) for s in shifts]
    )
    axis_moment_p = np.array(
        [moment_about_axis(AXIS_POINT, u, POINT + s * f_hat, FORCE) for s in shifts]
    )
    return point_moment, axis_moment_q, axis_moment_p


def draw_vector(ax, start, vector, color, label, at=1.0):
    ax.quiver(
        *start,
        *vector,
        color=color,
        linewidth=2.2,
        arrow_length_ratio=0.12,
    )
    tip = np.asarray(start) + at * np.asarray(vector)
    ax.text(*tip, f" {label}", color=color, fontsize=12)


def make_figure():
    u = unit(AXIS_DIRECTION)
    m_o = moment_about_point(AXIS_POINT, POINT, FORCE)
    parallel, _ = split_moment(m_o, u)

    fig = plt.figure(figsize=(13, 5.6))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    line = AXIS_POINT[None, :] + np.linspace(-0.3, 0.6, 2)[:, None] * u[None, :]
    ax.plot(*line.T, "k--", linewidth=1.2)
    ax.text(*line[-1], " axis a", fontsize=11)
    draw_vector(ax, AXIS_POINT, POINT - AXIS_POINT, "0.3", "r", at=0.55)
    draw_vector(ax, POINT, FORCE * FORCE_SCALE, "tab:blue", "F")
    draw_vector(ax, AXIS_POINT, m_o * MOMENT_SCALE, "tab:red", r"$M_O$")
    draw_vector(ax, AXIS_POINT, parallel * MOMENT_SCALE, "tab:purple", r"$M_a u$")
    tip = m_o * MOMENT_SCALE
    foot = parallel * MOMENT_SCALE
    ax.plot(*np.vstack((tip, foot)).T, ":", color="tab:purple")
    ax.scatter(*POINT, color="tab:blue", s=20)
    ax.text(*POINT, "  P", fontsize=11)
    ax.text(*AXIS_POINT, "O  ", fontsize=11, ha="right")
    ax.set(
        xlabel="x (m)",
        ylabel="y (m)",
        zlabel="z (m)",
        xlim=(-0.2, 0.45),
        ylim=(-0.1, 0.45),
        zlim=(-0.45, 0.4),
    )
    ax.set_title(
        "(a) Moment about O and its projection on the axis\n"
        "(F and moments drawn to their own scales)"
    )
    ax.view_init(elev=20, azim=-120)
    ax.set_box_aspect((1, 1, 1))

    ax2 = fig.add_subplot(1, 2, 2)
    point_moment, axis_q, axis_p = invariance_study()
    ax2.plot(
        SHIFTS,
        point_moment,
        color="tab:red",
        linewidth=2,
        label=r"$|M_Q|$, Q moved along the axis",
    )
    ax2.plot(
        SHIFTS,
        axis_q,
        color="tab:purple",
        linewidth=2,
        label=r"$M_a$, Q moved along the axis",
    )
    ax2.plot(
        SHIFTS,
        axis_p,
        "--",
        color="tab:green",
        linewidth=2,
        label=r"$M_a$, F slid along its line of action",
    )
    ax2.axhline(0.0, color="0.5", linewidth=0.8)
    ax2.set(
        xlabel="shift s (m)",
        ylabel="moment (N m)",
        title="(b) Moment about a point changes, moment about the axis does not",
    )
    ax2.legend(loc="center right", fontsize=10)
    ax2.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    u = unit(AXIS_DIRECTION)
    m_o = moment_about_point(AXIS_POINT, POINT, FORCE)
    m_a = moment_about_axis(AXIS_POINT, u, POINT, FORCE)
    parallel, perpendicular = split_moment(m_o, u)
    print(
        f"M_O = ({m_o[0]:.1f}, {m_o[1]:.1f}, {m_o[2]:.1f}) N m, |M_O| = {np.linalg.norm(m_o):.1f} N m"
    )
    print(
        f"u = ({u[0]:.4f}, {u[1]:.4f}, {u[2]:.4f}), M_a = u . (r x F) = {m_a:.2f} N m"
    )
    print(
        f"parallel part {np.linalg.norm(parallel):.2f} N m, perpendicular part "
        f"{np.linalg.norm(perpendicular):.2f} N m"
    )
    point_moment, axis_q, axis_p = invariance_study()
    print(
        f"|M_Q| over the shifts: {point_moment.min():.1f} to {point_moment.max():.1f} N m; "
        f"M_a spread {np.ptp(np.concatenate((axis_q, axis_p))):.1e} N m"
    )

    finish_figures(
        {"fundamentals_moment_about_axis.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
