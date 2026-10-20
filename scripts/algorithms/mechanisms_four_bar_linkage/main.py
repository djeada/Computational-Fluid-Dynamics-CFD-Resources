"""Four-bar linkage and slider-crank kinematics by vector loop closure.

The four-bar position problem is solved in closed form with the Freudenstein
equation for the open and crossed assemblies; the velocity and acceleration
problems are the two linear 2 x 2 systems obtained by differentiating the loop
equation. Over a full crank revolution the script draws the linkage at several
positions with its coupler curve, and plots the coupler and rocker angles,
angular velocities, angular accelerations and the transmission angle against
the crank angle. It prints the Grashof classification, the rocker swing, the
quick-return time ratio and the extreme transmission angles. A second figure
compares the exact slider-crank piston velocity and acceleration with the
two-term approximation used in engine balancing.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Four-bar link lengths (m): ground O2-O4, crank O2-A, coupler A-B, rocker O4-B.
GROUND = 0.120
CRANK = 0.040
COUPLER = 0.110
ROCKER = 0.090
COUPLER_POINT = (0.070, np.radians(40.0))  # distance from A (m), angle from AB
CRANK_SPEED = 10.0  # omega_2 (rad/s), constant
N_ANGLES = 721  # crank angles over one revolution
SNAPSHOT_DEG = (0, 90, 180, 270)  # crank angles drawn in panel (a)
MIN_TRANSMISSION_DEG = 40.0  # usual lower limit on the transmission angle

# Slider-crank (in-line): crank radius, connecting-rod length, speed.
SC_CRANK = 0.050  # r (m)
SC_ROD = 0.200  # l (m)
SC_RPM = 3000.0  # crank speed (rev/min)


def grashof_class(ground, crank, coupler, rocker):
    """Classify a four-bar by the Grashof condition and the position of the shortest link.

    Returns one of "crank-rocker", "double-crank", "double-rocker (Grashof)",
    "change-point" or "triple-rocker (non-Grashof)".
    """
    lengths = {"ground": ground, "crank": crank, "coupler": coupler, "rocker": rocker}
    ordered = sorted(lengths.values())
    s, p, q, long_ = ordered
    lhs, rhs = s + long_, p + q
    if np.isclose(lhs, rhs):
        return "change-point"
    if lhs > rhs:
        return "triple-rocker (non-Grashof)"
    shortest = min(lengths, key=lengths.get)
    if shortest == "ground":
        return "double-crank"
    if shortest == "coupler":
        return "double-rocker (Grashof)"
    return "crank-rocker"


def freudenstein_constants(a, b, c, d):
    """K1, K2, K3 of K1 cos(t4) - K2 cos(t2) + K3 = cos(t2 - t4)."""
    return d / a, d / c, (a**2 - b**2 + c**2 + d**2) / (2 * a * c)


def solve_position(theta2, a=CRANK, b=COUPLER, c=ROCKER, d=GROUND, branch=-1):
    """Coupler and rocker angles (rad) for crank angle(s) theta2.

    Solves the Freudenstein equation with the tangent half-angle substitution;
    branch = -1 gives the open assembly, +1 the crossed one. Returns
    (theta3, theta4); NaN where the linkage cannot be assembled.
    """
    theta2 = np.asarray(theta2, dtype=float)
    k1, k2, k3 = freudenstein_constants(a, b, c, d)
    big_a = np.cos(theta2) - k1 - k2 * np.cos(theta2) + k3
    big_b = -2.0 * np.sin(theta2)
    big_c = k1 - (k2 + 1.0) * np.cos(theta2) + k3
    disc = big_b**2 - 4.0 * big_a * big_c
    root = np.sqrt(np.where(disc >= 0, disc, np.nan))
    theta4 = np.angle(np.exp(2j * np.arctan2(-big_b + branch * root, 2.0 * big_a)))
    # Coupler angle from the loop: b e^{i t3} = d + c e^{i t4} - a e^{i t2}.
    vec = d + c * np.exp(1j * theta4) - a * np.exp(1j * theta2)
    theta3 = np.angle(vec)
    return theta3, theta4


def joint_positions(theta2, theta3, theta4, a=CRANK, b=COUPLER, d=GROUND):
    """Complex positions of O2, A, B, O4 and the coupler point P."""
    o2 = np.zeros_like(theta2, dtype=complex)
    pa = a * np.exp(1j * theta2)
    pb = pa + b * np.exp(1j * theta3)
    o4 = np.full_like(o2, d)
    dist, angle = COUPLER_POINT
    pp = pa + dist * np.exp(1j * (theta3 + angle))
    return o2, pa, pb, o4, pp


def solve_velocity(theta2, theta3, theta4, omega2, a=CRANK, b=COUPLER, c=ROCKER):
    """Coupler and rocker angular velocities from the differentiated loop.

    i a w2 e^{i t2} + i b w3 e^{i t3} - i c w4 e^{i t4} = 0, split into real
    and imaginary parts, is linear in (w3, w4).
    """
    omega3 = np.empty_like(theta2)
    omega4 = np.empty_like(theta2)
    for k, (t2, t3, t4) in enumerate(zip(theta2, theta3, theta4, strict=True)):
        matrix = np.array(
            [[-b * np.sin(t3), c * np.sin(t4)], [b * np.cos(t3), -c * np.cos(t4)]]
        )
        rhs = np.array([a * omega2 * np.sin(t2), -a * omega2 * np.cos(t2)])
        omega3[k], omega4[k] = np.linalg.solve(matrix, rhs)
    return omega3, omega4


def solve_acceleration(
    theta2, theta3, theta4, omega2, omega3, omega4, alpha2=0.0,
    a=CRANK, b=COUPLER, c=ROCKER,
):  # fmt: skip
    """Coupler and rocker angular accelerations from the twice-differentiated loop.

    a (i al2 - w2^2) e^{i t2} + b (i al3 - w3^2) e^{i t3}
    - c (i al4 - w4^2) e^{i t4} = 0 is linear in (al3, al4).
    """
    alpha3 = np.empty_like(theta2)
    alpha4 = np.empty_like(theta2)
    for k in range(theta2.size):
        t2, t3, t4 = theta2[k], theta3[k], theta4[k]
        w3, w4 = omega3[k], omega4[k]
        known = (
            a * (1j * alpha2 - omega2**2) * np.exp(1j * t2)
            - b * w3**2 * np.exp(1j * t3)
            + c * w4**2 * np.exp(1j * t4)
        )
        matrix = np.array(
            [[-b * np.sin(t3), c * np.sin(t4)], [b * np.cos(t3), -c * np.cos(t4)]]
        )
        rhs = -np.array([known.real, known.imag])
        alpha3[k], alpha4[k] = np.linalg.solve(matrix, rhs)
    return alpha3, alpha4


def transmission_angle(theta3, theta4):
    """Interior angle mu at joint B between coupler and rocker (rad, 0..pi).

    The direction B -> A is theta3 + pi and B -> O4 is theta4 + pi, so mu is
    the magnitude of the wrapped difference theta3 - theta4.
    """
    return np.abs(np.angle(np.exp(1j * (theta3 - theta4))))


def transmission_angle_closed_form(theta2, a=CRANK, b=COUPLER, c=ROCKER, d=GROUND):
    """Angle mu between coupler and rocker from the law of cosines (rad, 0..pi)."""
    diag2 = a**2 + d**2 - 2 * a * d * np.cos(theta2)  # |A - O4|^2
    return np.arccos((b**2 + c**2 - diag2) / (2 * b * c))


def limit_positions(a=CRANK, b=COUPLER, c=ROCKER, d=GROUND):
    """Crank angles (rad) of the two toggle positions of a crank-rocker.

    Extended: crank and coupler in line, |O2 B| = a + b. Folded: |O2 B| = b - a.
    Returns (theta2_extended, theta2_folded, time_ratio).
    """
    beta1 = np.arccos(((a + b) ** 2 + d**2 - c**2) / (2 * (a + b) * d))
    beta2 = np.arccos(((b - a) ** 2 + d**2 - c**2) / (2 * (b - a) * d))
    forward = np.pi + beta2 - beta1  # crank rotation from extended to folded
    ratio = max(forward, 2 * np.pi - forward) / min(forward, 2 * np.pi - forward)
    return beta1, beta2 + np.pi, ratio


def slider_crank(theta, omega, r=SC_CRANK, l=SC_ROD):  # noqa: E741
    """Exact piston position, velocity and acceleration of an in-line slider-crank.

    x is measured from the crank centre; omega is constant.
    """
    s = np.sqrt(l**2 - (r * np.sin(theta)) ** 2)  # l cos(phi)
    x = r * np.cos(theta) + s
    dx = -r * np.sin(theta) - r**2 * np.sin(theta) * np.cos(theta) / s
    d2x = (
        -r * np.cos(theta)
        - r**2 * np.cos(2 * theta) / s
        - r**4 * np.sin(theta) ** 2 * np.cos(theta) ** 2 / s**3
    )
    return x, omega * dx, omega**2 * d2x


def slider_crank_approx(theta, omega, r=SC_CRANK, l=SC_ROD):  # noqa: E741
    """Two-term (first and second harmonic) approximation of velocity and acceleration."""
    lam = r / l
    v = -r * omega * (np.sin(theta) + 0.5 * lam * np.sin(2 * theta))
    acc = -r * omega**2 * (np.cos(theta) + lam * np.cos(2 * theta))
    return v, acc


def analyse():
    """Kinematics of the four-bar over one crank revolution."""
    theta2 = np.linspace(0.0, 2 * np.pi, N_ANGLES)
    theta3, theta4 = solve_position(theta2)
    omega3, omega4 = solve_velocity(theta2, theta3, theta4, CRANK_SPEED)
    alpha3, alpha4 = solve_acceleration(
        theta2, theta3, theta4, CRANK_SPEED, omega3, omega4
    )
    return {
        "theta2": theta2,
        "theta3": theta3,
        "theta4": theta4,
        "omega3": omega3,
        "omega4": omega4,
        "alpha3": alpha3,
        "alpha4": alpha4,
        "mu": transmission_angle(theta3, theta4),
    }


def draw_linkage(ax, res):
    o2, pa, pb, o4, pp = joint_positions(res["theta2"], res["theta3"], res["theta4"])
    ax.plot(
        pp.real * 1e3, pp.imag * 1e3, color="tab:purple", lw=2, label="coupler curve"
    )
    ax.plot(pb.real * 1e3, pb.imag * 1e3, color="0.6", lw=1, ls="--", label="path of B")
    colors = ("tab:blue", "tab:orange", "tab:green", "tab:red")
    for deg, col in zip(SNAPSHOT_DEG, colors, strict=True):
        t2 = np.radians([deg])
        t3, t4 = solve_position(t2)
        q2, qa, qb, q4, qp = (z[0] * 1e3 for z in joint_positions(t2, t3, t4))
        ax.plot(
            [q2.real, qa.real, qb.real, q4.real], [q2.imag, qa.imag, qb.imag, q4.imag],
            color=col, lw=2.2, marker="o", ms=4, label=rf"$\theta_2$ = {deg}°",
        )  # fmt: skip
        ax.plot(
            [qa.real, qp.real, qb.real], [qa.imag, qp.imag, qb.imag],
            color=col, lw=1, ls=":",
        )  # fmt: skip
        ax.plot(qp.real, qp.imag, "s", color=col, ms=6)
    for x0 in (0.0, GROUND * 1e3):
        ax.plot(x0, 0.0, marker="^", ms=12, color="black")
    ax.plot([0, GROUND * 1e3], [0, 0], color="black", lw=1)
    ax.set_aspect("equal")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_title("(a) Linkage positions and coupler curve")
    ax.legend(loc="lower right", fontsize=8, ncol=2, frameon=False)
    ax.set_ylim(-105, 125)


def make_four_bar_figure(res):
    deg = np.degrees(res["theta2"])
    fig, axes = plt.subplots(2, 3, figsize=(13, 8), constrained_layout=True)
    draw_linkage(axes[0, 0], res)

    ax = axes[0, 1]
    ax.plot(deg, np.degrees(res["theta3"]), label=r"coupler $\theta_3$")
    ax.plot(deg, np.degrees(res["theta4"]), label=r"rocker $\theta_4$")
    ax.set_title("(b) Link angles")
    ax.set_ylabel("angle (deg)")

    ax = axes[0, 2]
    ax.plot(deg, res["omega3"], label=r"$\omega_3$")
    ax.plot(deg, res["omega4"], label=r"$\omega_4$")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_title(rf"(c) Angular velocities, $\omega_2$ = {CRANK_SPEED:g} rad/s")
    ax.set_ylabel("angular velocity (rad/s)")

    ax = axes[1, 0]
    ax.plot(deg, res["alpha3"], label=r"$\alpha_3$")
    ax.plot(deg, res["alpha4"], label=r"$\alpha_4$")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_title(r"(d) Angular accelerations, $\alpha_2 = 0$")
    ax.set_ylabel(r"angular acceleration (rad/s$^2$)")

    ax = axes[1, 1]
    ax.plot(deg, np.degrees(res["mu"]), color="tab:green", label="transmission angle")
    ax.axhline(
        MIN_TRANSMISSION_DEG, color="tab:red", ls="--", label="40° and 140° limits"
    )
    ax.axhline(180 - MIN_TRANSMISSION_DEG, color="tab:red", ls="--")
    ax.axhline(90, color="0.5", lw=0.8)
    ax.set_ylim(0, 180)
    ax.set_yticks(range(0, 181, 30))
    ax.set_title(r"(e) Transmission angle $\mu$")
    ax.set_ylabel("angle (deg)")

    ax = axes[1, 2]
    ax.axis("off")
    _, _, ratio = limit_positions()
    swing = np.degrees(np.nanmax(res["theta4"]) - np.nanmin(res["theta4"]))
    lines = [
        "Link lengths (mm)",
        f"  ground d = {GROUND * 1e3:.0f}, crank a = {CRANK * 1e3:.0f}",
        f"  coupler b = {COUPLER * 1e3:.0f}, rocker c = {ROCKER * 1e3:.0f}",
        f"Grashof: s + l = {(CRANK + GROUND) * 1e3:.0f}"
        f" < p + q = {(COUPLER + ROCKER) * 1e3:.0f}",
        f"Class: {grashof_class(GROUND, CRANK, COUPLER, ROCKER)}",
        f"Rocker swing: {swing:.1f}°",
        f"Time ratio: {ratio:.3f}",
        f"Transmission angle: {np.degrees(res['mu'].min()):.1f}°"
        f" to {np.degrees(res['mu'].max()):.1f}°",
        f"Peak |omega_4|: {np.abs(res['omega4']).max():.2f} rad/s",
    ]
    ax.text(0.02, 0.95, "\n".join(lines), va="top", family="monospace", fontsize=10)
    ax.set_title("(f) Summary")

    for ax in (axes[0, 1], axes[0, 2], axes[1, 0], axes[1, 1]):
        ax.set_xlabel(r"crank angle $\theta_2$ (deg)")
        ax.set_xlim(0, 360)
        ax.set_xticks(range(0, 361, 60))
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9, loc="best")
    return fig


def make_slider_crank_figure():
    omega = SC_RPM * 2 * np.pi / 60
    theta = np.linspace(0.0, 2 * np.pi, 361)
    _, v, acc = slider_crank(theta, omega)
    v_ap, acc_ap = slider_crank_approx(theta, omega)
    deg = np.degrees(theta)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), constrained_layout=True)
    ax = axes[0]
    ax.plot(deg, v, label="exact")
    ax.plot(deg, v_ap, ls="--", label="two-term approximation")
    ax.set_ylabel("piston velocity (m/s)")
    ax.set_title("(a) Piston velocity")
    ax = axes[1]
    ax.plot(deg, acc, label="exact")
    ax.plot(deg, acc_ap, ls="--", label="two-term approximation")
    ax.plot(
        deg, -SC_CRANK * omega**2 * np.cos(theta), ls=":", label="primary term only"
    )
    ax.set_ylabel(r"piston acceleration (m/s$^2$)")
    ax.set_title(f"(b) Piston acceleration, {SC_RPM:.0f} rpm")
    ax = axes[2]
    ax.plot(deg, acc - acc_ap, color="tab:purple")
    ax.set_ylabel(r"acceleration error (m/s$^2$)")
    ax.set_title(
        f"(c) Exact minus two-term, r/l = {SC_CRANK / SC_ROD:g}",
    )
    for ax in axes:
        ax.set_xlabel(r"crank angle $\theta$ from top dead centre (deg)")
        ax.set_xlim(0, 360)
        ax.set_xticks(range(0, 361, 60))
        ax.axhline(0, color="0.5", lw=0.8)
        ax.grid(alpha=0.3)
    for ax in axes[:2]:
        ax.legend(fontsize=9)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    res = analyse()
    t2e, t2f, ratio = limit_positions()
    print(f"Grashof class: {grashof_class(GROUND, CRANK, COUPLER, ROCKER)}")
    print(
        f"rocker angle {np.degrees(np.nanmin(res['theta4'])):.2f} to "
        f"{np.degrees(np.nanmax(res['theta4'])):.2f} deg; toggle at crank "
        f"{np.degrees(t2e):.2f} and {np.degrees(t2f):.2f} deg; time ratio {ratio:.3f}"
    )
    print(
        f"transmission angle {np.degrees(res['mu'].min()):.2f} to "
        f"{np.degrees(res['mu'].max()):.2f} deg; peak |omega4| "
        f"{np.abs(res['omega4']).max():.3f} rad/s; peak |alpha4| "
        f"{np.abs(res['alpha4']).max():.2f} rad/s^2"
    )
    omega = SC_RPM * 2 * np.pi / 60
    _, v60, a60 = slider_crank(np.radians([60.0, 0.0]), omega)
    print(
        f"slider-crank at 60 deg: v = {v60[0]:.2f} m/s, a = {a60[0]:.0f} m/s^2; "
        f"at TDC a = {a60[1]:.0f} m/s^2"
    )

    finish_figures(
        {
            "mechanisms_four_bar_linkage.png": make_four_bar_figure(res),
            "mechanisms_slider_crank.png": make_slider_crank_figure(),
        },
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
