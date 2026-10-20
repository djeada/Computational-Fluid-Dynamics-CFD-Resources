"""Transform a 2D plane-stress state and draw Mohr's circle with its elements.

Given sigma_x, sigma_y and tau_xy, the script computes the stresses on a plane
rotated by an angle theta, the principal stresses and their directions, and
the maximum in-plane shear stress. The figure shows Mohr's circle with the
points X, Y, X' and the principal and maximum-shear points annotated, next to
the stress element in its original orientation, rotated by theta, aligned
with the principal directions, and aligned with the maximum-shear planes.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Polygon

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SIGMA_X = 80.0  # normal stress on the x face (MPa, tension positive)
SIGMA_Y = -40.0  # normal stress on the y face (MPa)
TAU_XY = 50.0  # shear stress on the x face in +y direction (MPa)
THETA = 30.0  # rotation of the x' axis from x, counterclockwise (degrees)

COLORS = {"x": "tab:blue", "y": "tab:orange", "p": "tab:green", "s": "tab:red"}


def transform(sigma_x, sigma_y, tau_xy, theta):
    """Return (sigma_x', sigma_y', tau_x'y') on axes rotated by theta (rad)."""
    mean = 0.5 * (sigma_x + sigma_y)
    half_diff = 0.5 * (sigma_x - sigma_y)
    c, s = np.cos(2.0 * theta), np.sin(2.0 * theta)
    sx = mean + half_diff * c + tau_xy * s
    sy = mean - half_diff * c - tau_xy * s
    txy = -half_diff * s + tau_xy * c
    return sx, sy, txy


def circle(sigma_x, sigma_y, tau_xy):
    """Return the centre and radius of Mohr's circle."""
    centre = 0.5 * (sigma_x + sigma_y)
    radius = np.hypot(0.5 * (sigma_x - sigma_y), tau_xy)
    return centre, radius


def principal(sigma_x, sigma_y, tau_xy):
    """Return (sigma_1, sigma_2, theta_p) with theta_p the angle from x to sigma_1.

    sigma_1 >= sigma_2 are the in-plane principal stresses; theta_p lies in
    (-90, 90] degrees and is returned in radians.
    """
    centre, radius = circle(sigma_x, sigma_y, tau_xy)
    theta_p = 0.5 * np.arctan2(2.0 * tau_xy, sigma_x - sigma_y)
    return centre + radius, centre - radius, theta_p


def max_shear(sigma_x, sigma_y, tau_xy, sigma_z=0.0):
    """Return (in-plane maximum shear, its angle, absolute maximum shear).

    The angle theta_s = theta_p - 45 deg gives tau_x'y' = +tau_max on the x'
    face. The absolute maximum shear includes the out-of-plane principal
    stress sigma_z (zero for plane stress).
    """
    s1, s2, theta_p = principal(sigma_x, sigma_y, tau_xy)
    in_plane = 0.5 * (s1 - s2)
    all_three = (s1, s2, sigma_z)
    absolute = 0.5 * (max(all_three) - min(all_three))
    return in_plane, theta_p - np.pi / 4.0, absolute


def draw_element(ax, theta, sx, sy, txy, scale, title):
    """Draw a square element rotated by theta with its face stresses."""
    e1 = np.array([np.cos(theta), np.sin(theta)])
    e2 = np.array([-np.sin(theta), np.cos(theta)])
    half = 1.0
    corners = [
        half * (a * e1 + b * e2) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))
    ]
    ax.add_patch(Polygon(corners, closed=True, facecolor="0.92", edgecolor="0.2"))
    ax.plot([-1.6, 1.6], [0, 0], color="0.6", lw=0.6, ls=":")
    ax.plot([0, 0], [-1.6, 1.6], color="0.6", lw=0.6, ls=":")

    arrow = {"arrowstyle": "-|>", "lw": 1.6, "mutation_scale": 12}
    for normal, tangent, sigma, color in (
        (e1, e2, sx, COLORS["x"]),
        (e2, e1, sy, COLORS["y"]),
    ):
        length = 0.25 + 0.75 * abs(sigma) / scale
        for side in (1.0, -1.0):
            n = side * normal
            base = (half + 0.05) * n
            tip = base + length * n
            start, end = (base, tip) if sigma >= 0 else (tip, base)
            if abs(sigma) > 1e-9 * scale:
                ax.annotate(
                    "", xy=end, xytext=start, arrowprops={**arrow, "color": color}
                )
            if side > 0:
                label = tip + 0.22 * n
                ax.text(
                    *label,
                    f"{sigma:.1f}",
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=color,
                )
    # Shear: +tau acts in +e2 on the +e1 face and in +e1 on the +e2 face.
    if abs(txy) > 1e-9 * scale:
        shear_len = 0.4 + 0.5 * abs(txy) / scale
        sign = np.sign(txy)
        for normal, tangent in ((e1, e2), (e2, e1)):
            for side in (1.0, -1.0):
                mid = side * (half + 0.12) * normal
                d = side * sign * tangent * shear_len
                ax.annotate(
                    "",
                    xy=mid + d,
                    xytext=mid - d,
                    arrowprops={**arrow, "color": "0.25"},
                )
        ax.text(
            *((half + 0.35) * (e1 + e2)),
            rf"$\tau$ = {txy:.1f}",
            fontsize=10,
            ha="center",
            va="center",
            color="0.25",
        )
    ax.set(xlim=(-2.3, 2.3), ylim=(-2.3, 2.3), aspect="equal", title=title)
    ax.set_axis_off()


def make_figure(sigma_x, sigma_y, tau_xy, theta):
    """Draw Mohr's circle and four stress elements."""
    centre, radius = circle(sigma_x, sigma_y, tau_xy)
    s1, s2, theta_p = principal(sigma_x, sigma_y, tau_xy)
    tau_max, theta_s, _ = max_shear(sigma_x, sigma_y, tau_xy)
    sxr, syr, txyr = transform(sigma_x, sigma_y, tau_xy, theta)

    fig = plt.figure(figsize=(13.5, 7.2))
    grid = fig.add_gridspec(2, 4, width_ratios=[1.25, 1.25, 1, 1])
    ax = fig.add_subplot(grid[:, :2])

    phi = np.linspace(0.0, 2.0 * np.pi, 400)
    ax.plot(centre + radius * np.cos(phi), radius * np.sin(phi), color="0.3", lw=1.5)
    ax.axhline(0.0, color="0.5", lw=0.8)
    ax.axvline(0.0, color="0.5", lw=0.8)

    def point(s, t, color, label, offset):
        ax.plot(s, t, "o", color=color, ms=7, zorder=5)
        ax.annotate(
            label,
            (s, t),
            xytext=offset,
            textcoords="offset points",
            fontsize=10,
            color=color,
        )

    ax.plot([sigma_x, sigma_y], [tau_xy, -tau_xy], color="0.3", lw=1.0, ls="--")
    ax.plot([sxr, syr], [txyr, -txyr], color="tab:purple", lw=1.0, ls="--")
    point(sigma_x, tau_xy, COLORS["x"], rf"X ({sigma_x:.0f}, {tau_xy:.0f})", (8, 4))
    point(sigma_y, -tau_xy, COLORS["y"], rf"Y ({sigma_y:.0f}, {-tau_xy:.0f})", (8, -14))
    point(
        sxr,
        txyr,
        "tab:purple",
        rf"X$'$ at $\theta$ = {np.degrees(theta):.0f}$^\circ$",
        (8, 4),
    )
    point(s1, 0.0, COLORS["p"], rf"$\sigma_1$ = {s1:.1f}", (6, -16))
    point(s2, 0.0, COLORS["p"], rf"$\sigma_2$ = {s2:.1f}", (-78, -16))
    point(centre, radius, COLORS["s"], rf"$\tau_{{max}}$ = {tau_max:.1f}", (8, 6))
    point(centre, -radius, COLORS["s"], r"$-\tau_{max}$", (8, -14))
    point(centre, 0.0, "0.3", rf"C = {centre:.1f}", (4, 6))

    # 2 theta_p is measured from CX to the sigma_1 point; with tau plotted
    # downward the screen sense matches the counterclockwise element rotation.
    start = np.degrees(np.arctan2(tau_xy, sigma_x - centre))
    ax.add_patch(
        Arc(
            (centre, 0.0),
            0.5 * radius,
            0.5 * radius,
            theta1=min(start, 0.0),
            theta2=max(start, 0.0),
            color=COLORS["p"],
            lw=1.4,
        )
    )
    ax.text(
        centre + 0.3 * radius * np.cos(np.radians(0.5 * start)),
        0.3 * radius * np.sin(np.radians(0.5 * start)),
        rf"$2\theta_p$ = {2 * np.degrees(theta_p):.1f}$^\circ$",
        fontsize=10,
        color=COLORS["p"],
    )

    pad = 0.25 * radius
    ax.set(
        xlim=(centre - radius - pad, centre + radius + pad),
        ylim=(-radius - pad, radius + pad),
        aspect="equal",
        xlabel=r"normal stress $\sigma$ (MPa)",
        ylabel=r"shear stress $\tau$ (MPa), positive downward",
        title="Mohr's circle for plane stress",
    )
    ax.invert_yaxis()
    ax.grid(True, lw=0.4, alpha=0.5)

    scale = max(abs(sigma_x), abs(sigma_y), abs(tau_xy), abs(s1), abs(s2), 1e-12)
    draw_element(
        fig.add_subplot(grid[0, 2]),
        0.0,
        sigma_x,
        sigma_y,
        tau_xy,
        scale,
        "Given element",
    )
    draw_element(
        fig.add_subplot(grid[0, 3]),
        theta,
        sxr,
        syr,
        txyr,
        scale,
        rf"Rotated by $\theta$ = {np.degrees(theta):.0f}$^\circ$",
    )
    draw_element(
        fig.add_subplot(grid[1, 2]),
        theta_p,
        s1,
        s2,
        0.0,
        scale,
        rf"Principal, $\theta_p$ = {np.degrees(theta_p):.1f}$^\circ$",
    )
    draw_element(
        fig.add_subplot(grid[1, 3]),
        theta_s,
        centre,
        centre,
        tau_max,
        scale,
        rf"Max shear, $\theta_s$ = {np.degrees(theta_s):.1f}$^\circ$",
    )
    fig.text(
        0.55,
        0.02,
        "Stresses in MPa; normal arrows point outward for tension; dotted lines are the x and y axes.",
        fontsize=10,
        color="0.3",
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument("--sx", type=float, default=SIGMA_X, help="sigma_x in MPa")
    parser.add_argument("--sy", type=float, default=SIGMA_Y, help="sigma_y in MPa")
    parser.add_argument("--txy", type=float, default=TAU_XY, help="tau_xy in MPa")
    parser.add_argument(
        "--theta", type=float, default=THETA, help="rotation of the x' axis in degrees"
    )
    args = parser.parse_args(argv)
    theta = np.radians(args.theta)

    centre, radius = circle(args.sx, args.sy, args.txy)
    s1, s2, theta_p = principal(args.sx, args.sy, args.txy)
    tau_max, theta_s, tau_abs = max_shear(args.sx, args.sy, args.txy)
    sxr, syr, txyr = transform(args.sx, args.sy, args.txy, theta)
    print(f"centre C = {centre:.2f} MPa, radius R = {radius:.2f} MPa")
    print(
        f"sigma_1 = {s1:.2f} MPa, sigma_2 = {s2:.2f} MPa, "
        f"theta_p = {np.degrees(theta_p):.2f} deg"
    )
    print(
        f"tau_max in-plane = {tau_max:.2f} MPa at theta_s = "
        f"{np.degrees(theta_s):.2f} deg, absolute (sigma_3 = 0) = {tau_abs:.2f} MPa"
    )
    print(
        f"theta = {args.theta:.1f} deg: sigma_x' = {sxr:.2f}, sigma_y' = {syr:.2f}, "
        f"tau_x'y' = {txyr:.2f} MPa"
    )

    finish_figures(
        {"materials_mohr_circle.png": make_figure(args.sx, args.sy, args.txy, theta)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
