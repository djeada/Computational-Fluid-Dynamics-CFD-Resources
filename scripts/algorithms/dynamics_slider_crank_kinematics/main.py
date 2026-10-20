"""Slider-crank kinematics by relative velocity and acceleration, with the instantaneous centre.

A crank OA (0.1 m) turns at a constant 10 rad/s counterclockwise and drives a
connecting rod AB (0.3 m) whose end B slides on the line through O. At every
crank angle the rigid-body relations v_B = v_A + w_AB x r_B/A and
a_B = a_A + alpha_AB x r_B/A - w_AB^2 r_B/A are solved for the rod's angular
velocity and acceleration and the slider's velocity and acceleration. The
results are checked against finite differences of the exact slider position
and against the instantaneous centre of zero velocity of the rod; the usual
two-term approximation of the piston acceleration is drawn for comparison.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

CRANK = 0.1  # r = OA (m)
ROD = 0.3  # l = AB (m)
CRANK_RATE = 10.0  # omega_OA, counterclockwise, constant (rad/s)
DRAW_ANGLE_DEG = 60.0  # crank angle of the mechanism drawing (deg)


def slider_position(theta, r=CRANK, l=ROD):
    """Exact slider coordinate x_B (m) for crank angle theta (rad)."""
    return r * np.cos(theta) + np.sqrt(l**2 - (r * np.sin(theta)) ** 2)


def kinematics(theta, w=CRANK_RATE, r=CRANK, l=ROD):
    """Solve the relative-motion equations at crank angle(s) theta.

    Returns a dict with the positions of A and B, the rod vector r_B/A and
    w_AB, alpha_AB (rad/s, rad/s^2, counterclockwise positive), v_B and a_B
    (m/s, m/s^2, positive along +x).
    """
    theta = np.asarray(theta, dtype=float)
    a_pos = np.array([r * np.cos(theta), r * np.sin(theta)])
    x_b = slider_position(theta, r, l)
    bx, by = x_b - a_pos[0], -a_pos[1]  # r_B/A components
    v_a = w * np.array([-a_pos[1], a_pos[0]])  # omega k x r_A
    acc_a = -(w**2) * a_pos  # constant crank speed: only the normal term
    # j-component of v_B = v_A + w_AB k x r_B/A must vanish.
    w_ab = -v_a[1] / bx
    v_b = v_a[0] - w_ab * by
    # j-component of a_B = a_A + alpha_AB k x r_B/A - w_AB^2 r_B/A must vanish.
    alpha_ab = (w_ab**2 * by - acc_a[1]) / bx
    a_b = acc_a[0] - alpha_ab * by - w_ab**2 * bx
    return {
        "A": a_pos,
        "B": np.array([x_b, np.zeros_like(x_b)]),
        "r_BA": np.array([bx, by]),
        "v_A": v_a,
        "w_AB": w_ab,
        "alpha_AB": alpha_ab,
        "v_B": v_b,
        "a_B": a_b,
    }


def instantaneous_centre(theta, r=CRANK, l=ROD):
    """IC of the rod: line OA extended meets the vertical through B."""
    x_b = slider_position(theta, r, l)
    return np.array([x_b, x_b * np.tan(theta)])


def approximate_piston_acceleration(theta, w=CRANK_RATE, r=CRANK, l=ROD):
    """Two-term series a_B = -r w^2 (cos theta + (r/l) cos 2 theta)."""
    return -r * w**2 * (np.cos(theta) + r / l * np.cos(2.0 * theta))


def finite_difference_check(n=721, w=CRANK_RATE):
    """Central differences of x_B(theta(t)) for v_B and a_B on a periodic grid."""
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    dtheta = theta[1] - theta[0]
    x = slider_position(theta)
    v = w * (np.roll(x, -1) - np.roll(x, 1)) / (2.0 * dtheta)
    a = w**2 * (np.roll(x, -1) - 2.0 * x + np.roll(x, 1)) / dtheta**2
    return theta, v, a


def draw_mechanism(ax, theta):
    """Draw the linkage, the velocity vectors and the rod's IC."""
    colors = plt.get_cmap("tab10").colors
    k = kinematics(theta)
    a, b = k["A"], k["B"]
    ic = instantaneous_centre(theta)
    ax.plot([-0.12, 0.45], [0.0, 0.0], color="0.7", linewidth=6, zorder=0)
    ax.plot([0.0, a[0]], [0.0, a[1]], color=colors[0], linewidth=4, label="crank OA")
    ax.plot([a[0], b[0]], [a[1], b[1]], color=colors[1], linewidth=4, label="rod AB")
    ax.add_patch(plt.Rectangle((b[0] - 0.03, -0.02), 0.06, 0.04, color="0.3"))
    ax.plot([0.0, ic[0]], [0.0, ic[1]], color="0.5", linestyle="--", linewidth=1)
    ax.plot([b[0], ic[0]], [b[1], ic[1]], color="0.5", linestyle="--", linewidth=1)
    ax.plot(*ic, "o", color=colors[3], ms=8, label="IC of rod AB")
    scale = 0.1  # drawing scale (m per m/s)
    for point, vel, name in ((a, k["v_A"], "$v_A$"), (b, [k["v_B"], 0.0], "$v_B$")):
        ax.annotate(
            "",
            xy=(point[0] + scale * vel[0], point[1] + scale * vel[1]),
            xytext=point,
            arrowprops={"arrowstyle": "-|>", "color": colors[2], "lw": 2},
        )
        ax.text(
            point[0] + scale * vel[0] - 0.02,
            point[1] + scale * vel[1] + 0.015,
            name,
            fontsize=11,
            color=colors[2],
        )
    for point, name in ((np.zeros(2), "O"), (a, "A"), (b, "B")):
        ax.plot(*point, "ko", ms=5)
        ax.text(point[0] + 0.01, point[1] - 0.035, name, fontsize=11)
    ax.set(
        xlim=(-0.15, 0.45),
        ylim=(-0.08, 0.62),
        aspect="equal",
        xlabel="$x$ (m)",
        ylabel="$y$ (m)",
        title=rf"(a) $\theta$ = {np.degrees(theta):.0f}°: "
        rf"$\omega_{{AB}}$ = {k['w_AB']:.2f} rad/s, $v_B$ = {k['v_B']:.3f} m/s",
    )
    ax.legend(fontsize=9, loc="upper left")


def make_figure():
    """Draw the mechanism and the slider and rod histories over one revolution."""
    colors = plt.get_cmap("tab10").colors
    fig, (ax_mech, ax_slider, ax_rod) = plt.subplots(
        1, 3, figsize=(13.5, 5.0), gridspec_kw={"width_ratios": [1.0, 1.1, 1.1]}
    )
    draw_mechanism(ax_mech, np.radians(DRAW_ANGLE_DEG))

    theta = np.linspace(0.0, 2.0 * np.pi, 721)
    k = kinematics(theta)
    deg = np.degrees(theta)
    th_fd, v_fd, a_fd = finite_difference_check(n=36)
    ax_slider.plot(deg, k["v_B"], color=colors[0], label=r"$v_B$ (m/s)")
    ax_slider.plot(deg, k["a_B"] / 10.0, color=colors[1], label=r"$a_B / 10$ (m/s$^2$)")
    ax_slider.plot(
        deg,
        approximate_piston_acceleration(theta) / 10.0,
        color=colors[1],
        linestyle="--",
        linewidth=1.0,
        label=r"two-term $a_B/10$",
    )
    ax_slider.plot(np.degrees(th_fd), v_fd, "o", color=colors[0], ms=3.5)
    ax_slider.plot(np.degrees(th_fd), a_fd / 10.0, "s", color=colors[1], ms=3.5)
    ax_slider.plot([], [], "ko", ms=3.5, label="finite differences of $x_B$")
    ax_slider.set(
        xlabel=r"crank angle $\theta$ (deg)",
        ylabel="slider velocity and acceleration",
        title="(b) Slider B",
        xlim=(0.0, 360.0),
        xticks=np.arange(0, 361, 60),
        ylim=(-1.6, 2.0),
    )
    ax_slider.legend(fontsize=9, loc="upper center", ncol=2)
    ax_rod.plot(deg, k["w_AB"], color=colors[2], label=r"$\omega_{AB}$ (rad/s)")
    ax_rod.plot(
        deg,
        k["alpha_AB"] / 10.0,
        color=colors[4],
        label=r"$\alpha_{AB}/10$ (rad/s$^2$)",
    )
    ax_rod.set(
        xlabel=r"crank angle $\theta$ (deg)",
        ylabel="rod angular velocity and acceleration",
        title="(c) Connecting rod AB",
        xlim=(0.0, 360.0),
        xticks=np.arange(0, 361, 60),
        ylim=(-4.5, 5.5),
    )
    ax_rod.legend(fontsize=9, loc="upper center", ncol=2)
    for ax in (ax_mech, ax_slider, ax_rod):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for deg in (0.0, 60.0, 90.0, 180.0):
        theta = np.radians(deg)
        k = kinematics(theta)
        print(
            f"theta = {deg:5.1f} deg: v_B = {k['v_B']:+.4f} m/s, a_B = {k['a_B']:+.3f} m/s^2, "
            f"w_AB = {k['w_AB']:+.4f} rad/s, alpha_AB = {k['alpha_AB']:+.3f} rad/s^2"
        )
    theta, v_fd, a_fd = finite_difference_check()
    k = kinematics(theta)
    print(
        f"max |v_B - FD| = {np.max(np.abs(k['v_B'] - v_fd)):.2e} m/s, "
        f"max |a_B - FD| = {np.max(np.abs(k['a_B'] - a_fd)):.2e} m/s^2"
    )
    finish_figures(
        {"dynamics_slider_crank_kinematics.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
