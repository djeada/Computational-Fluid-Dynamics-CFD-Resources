"""Involute gear geometry: construction, a meshing pair and minimum tooth numbers.

An involute is traced by the end of a taut string unwound from the base circle.
Panel (a) draws that construction. Panel (b) draws a standard 20 deg
full-depth spur pinion and gear in mesh, with their pitch, base and addendum
circles, the line of action tangent to both base circles and the path of
contact cut from it by the two addendum circles; the contact ratio is the
length of that path divided by the base pitch. Panel (c) plots the smallest
pinion that meshes with a given gear without involute interference, for
pressure angles of 14.5, 20 and 25 deg.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MODULE = 4.0e-3  # m (m), metric module
PINION_TEETH = 20
GEAR_TEETH = 40
PRESSURE_ANGLE = np.radians(20.0)  # phi
ADDENDUM = 1.0  # addendum / module (full depth)
DEDENDUM = 1.25  # dedendum / module
PRESSURE_ANGLES_DEG = (14.5, 20.0, 25.0)


def involute(alpha):
    """inv(alpha) = tan(alpha) - alpha."""
    return np.tan(alpha) - alpha


def involute_curve(rb, t):
    """Points of the involute of a circle of radius rb at roll angle t (rad)."""
    return rb * (np.cos(t) + t * np.sin(t)), rb * (np.sin(t) - t * np.cos(t))


def gear_geometry(n, m=MODULE, phi=PRESSURE_ANGLE):
    """Pitch, base, addendum and root radii of a standard spur gear."""
    r = m * n / 2
    return {
        "r": r,
        "rb": r * np.cos(phi),
        "ra": r + ADDENDUM * m,
        "rf": r - DEDENDUM * m,
    }


def half_tooth_angle(radius, n, phi=PRESSURE_ANGLE):
    """Half the angular tooth thickness at a radius on the involute flank.

    psi(rho) = pi/(2N) + inv(phi) - inv(alpha), cos(alpha) = r_b / rho; the
    tooth is half the circular pitch thick on the pitch circle.
    """
    rb = gear_geometry(n, phi=phi)["rb"]
    alpha = np.arccos(np.clip(rb / radius, -1.0, 1.0))
    return np.pi / (2 * n) + involute(phi) - involute(alpha)


def gear_outline(
    n, centre=(0.0, 0.0), rotation=0.0, m=MODULE, phi=PRESSURE_ANGLE, pts=30
):
    """Closed outline of a spur gear: involute flanks, tip arcs, radial lines and root arcs.

    Tooth k is centred at angle rotation + 2 pi k / N. Below the base circle
    the flank is continued as a radial line to the root circle (the fillet
    trochoid is not modelled).
    """
    g = gear_geometry(n, m, phi)
    rho = np.linspace(max(g["rb"], g["rf"]), g["ra"], pts)
    psi = half_tooth_angle(rho, n, phi)
    psi_base = half_tooth_angle(max(g["rb"], g["rf"]), n, phi)
    xs, ys = [], []
    for k in range(n):
        gam = rotation + 2 * np.pi * k / n
        right = (
            np.concatenate(([g["rf"]], rho)),
            np.concatenate(([gam - psi_base], gam - psi)),
        )
        tip = np.full(8, g["ra"]), np.linspace(gam - psi[-1], gam + psi[-1], 8)
        left = (
            np.concatenate((rho[::-1], [g["rf"]])),
            np.concatenate((gam + psi[::-1], [gam + psi_base])),
        )
        nxt = gam + 2 * np.pi / n
        root = np.full(8, g["rf"]), np.linspace(gam + psi_base, nxt - psi_base, 8)
        for rr, aa in (right, tip, left, root):
            xs.append(centre[0] + rr * np.cos(aa))
            ys.append(centre[1] + rr * np.sin(aa))
    return np.concatenate(xs), np.concatenate(ys)


def contact_ratio(n1, n2, m=MODULE, phi=PRESSURE_ANGLE):
    """Length of the path of contact and the transverse contact ratio.

    Z = sqrt(ra1^2 - rb1^2) + sqrt(ra2^2 - rb2^2) - C sin(phi), m_c = Z / (pi m cos(phi)).
    """
    g1, g2 = gear_geometry(n1, m, phi), gear_geometry(n2, m, phi)
    c = g1["r"] + g2["r"]
    z = (
        np.sqrt(g1["ra"] ** 2 - g1["rb"] ** 2)
        + np.sqrt(g2["ra"] ** 2 - g2["rb"] ** 2)
        - c * np.sin(phi)
    )
    return z, z / (np.pi * m * np.cos(phi))


def min_pinion_teeth(ratio, phi, k=ADDENDUM):
    """Smallest pinion without interference against a gear of ratio N_G/N_P (real number).

    N_P = 2k / ((1 + 2 m_G) sin^2 phi) (m_G + sqrt(m_G^2 + (1 + 2 m_G) sin^2 phi));
    ratio = inf gives the rack value 2k / sin^2 phi.
    """
    s2 = np.sin(phi) ** 2
    ratio = np.asarray(ratio, dtype=float)
    with np.errstate(invalid="ignore"):
        finite = (
            2
            * k
            / ((1 + 2 * ratio) * s2)
            * (ratio + np.sqrt(ratio**2 + (1 + 2 * ratio) * s2))
        )
    return np.where(np.isinf(ratio), 2 * k / s2, finite)


def make_figure():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.8), constrained_layout=True)

    ax = axes[0]
    rb = 1.0
    circ = np.linspace(0, 2 * np.pi, 400)
    ax.plot(rb * np.cos(circ), rb * np.sin(circ), color="0.4", label="base circle")
    t = np.linspace(0, np.radians(110), 200)
    x, y = involute_curve(rb, t)
    ax.plot(x, y, color="tab:blue", lw=2.5, label="involute")
    for tk, col in zip(
        np.radians([30, 60, 90, 110]),
        ("tab:orange", "tab:green", "tab:red", "tab:purple"),
        strict=True,
    ):
        tx, ty = rb * np.cos(tk), rb * np.sin(tk)
        px, py = involute_curve(rb, tk)
        ax.plot([tx, px], [ty, py], color=col, lw=1.5)
        ax.plot(tx, ty, "o", color=col, ms=5)
        ax.plot(px, py, "s", color=col, ms=5)
        ax.annotate(
            f"roll {np.degrees(tk):.0f}°", (px, py), textcoords="offset points",
            xytext=(6, -2), fontsize=8.5, color=col,
        )  # fmt: skip
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 2.6)
    ax.set_ylim(-1.3, 2.2)
    ax.set_xlabel("x / base radius")
    ax.set_ylabel("y / base radius")
    ax.set_title("(a) Involute: end of a string unwound from the base circle")
    ax.legend(fontsize=9, loc="lower right")

    ax = axes[1]
    g1, g2 = gear_geometry(PINION_TEETH), gear_geometry(GEAR_TEETH)
    c = g1["r"] + g2["r"]
    to_mm = 1e3
    x1, y1 = gear_outline(PINION_TEETH)
    x2, y2 = gear_outline(
        GEAR_TEETH, centre=(c, 0.0), rotation=np.pi + np.pi / GEAR_TEETH
    )
    ax.fill(x1 * to_mm, y1 * to_mm, color="tab:blue", alpha=0.25)
    ax.plot(
        x1 * to_mm,
        y1 * to_mm,
        color="tab:blue",
        lw=1.2,
        label=f"pinion, N = {PINION_TEETH}",
    )
    ax.fill(x2 * to_mm, y2 * to_mm, color="tab:orange", alpha=0.25)
    ax.plot(
        x2 * to_mm,
        y2 * to_mm,
        color="tab:orange",
        lw=1.2,
        label=f"gear, N = {GEAR_TEETH}",
    )
    for g, cx, col in ((g1, 0.0, "tab:blue"), (g2, c, "tab:orange")):
        ax.plot(
            (cx + g["r"] * np.cos(circ)) * to_mm,
            g["r"] * np.sin(circ) * to_mm,
            color=col,
            ls="--",
            lw=0.9,
        )
        ax.plot(
            (cx + g["rb"] * np.cos(circ)) * to_mm,
            g["rb"] * np.sin(circ) * to_mm,
            color=col,
            ls=":",
            lw=0.9,
        )
    phi = PRESSURE_ANGLE
    t1 = np.array([g1["rb"] * np.cos(phi), g1["rb"] * np.sin(phi)])
    t2 = np.array([c - g2["rb"] * np.cos(phi), -g2["rb"] * np.sin(phi)])
    ax.plot(
        [t1[0] * to_mm, t2[0] * to_mm],
        [t1[1] * to_mm, t2[1] * to_mm],
        color="black",
        lw=1,
        label="line of action",
    )
    direction = (t2 - t1) / np.linalg.norm(t2 - t1)
    start = t2 - direction * np.sqrt(g2["ra"] ** 2 - g2["rb"] ** 2)  # gear tip enters
    end = t1 + direction * np.sqrt(g1["ra"] ** 2 - g1["rb"] ** 2)  # pinion tip leaves
    ax.plot(
        [start[0] * to_mm, end[0] * to_mm],
        [start[1] * to_mm, end[1] * to_mm],
        color="tab:red",
        lw=3.5,
        label="path of contact",
    )
    ax.plot(g1["r"] * to_mm, 0, "k+", ms=12, mew=2)
    ax.annotate(
        "pitch point",
        (g1["r"] * to_mm, 0),
        textcoords="offset points",
        xytext=(-62, -4),
        fontsize=9,
    )
    _, ratio = contact_ratio(PINION_TEETH, GEAR_TEETH)
    ax.set_aspect("equal")
    ax.set_xlim(26, 56)
    ax.set_ylim(-15, 15)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_title(
        rf"(b) Mesh, m = {MODULE * 1e3:g} mm, $\phi$ = 20°, contact ratio {ratio:.2f}"
    )
    ax.legend(fontsize=8, loc="lower left")

    ax = axes[2]
    ratios = np.linspace(1.0, 10.0, 200)
    colors = ("tab:blue", "tab:orange", "tab:green")
    for deg, col in zip(PRESSURE_ANGLES_DEG, colors, strict=True):
        n_min = np.ceil(min_pinion_teeth(ratios, np.radians(deg)))
        rack = np.ceil(min_pinion_teeth(np.inf, np.radians(deg)))
        ax.step(
            ratios,
            n_min,
            where="post",
            color=col,
            label=f"{deg:g}°, rack limit {rack:.0f}",
        )
        ax.axhline(rack, color=col, ls=":", lw=1)
    ax.set_xlabel(r"gear ratio $N_G / N_P$")
    ax.set_ylabel("minimum pinion teeth")
    ax.set_title("(c) Smallest pinion free of interference")
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 35)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc="center right", title="pressure angle")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    g1, g2 = gear_geometry(PINION_TEETH), gear_geometry(GEAR_TEETH)
    z, ratio = contact_ratio(PINION_TEETH, GEAR_TEETH)
    print(
        f"pinion r = {g1['r'] * 1e3:.2f} mm, rb = {g1['rb'] * 1e3:.2f} mm; "
        f"gear r = {g2['r'] * 1e3:.2f} mm, rb = {g2['rb'] * 1e3:.2f} mm"
    )
    print(
        f"path of contact {z * 1e3:.2f} mm, base pitch {np.pi * MODULE * np.cos(PRESSURE_ANGLE) * 1e3:.2f} mm, contact ratio {ratio:.3f}"
    )
    for deg in PRESSURE_ANGLES_DEG:
        phi = np.radians(deg)
        print(
            f"phi = {deg:4.1f} deg: min pinion teeth 1:1 {min_pinion_teeth(1.0, phi):.2f}, "
            f"rack {min_pinion_teeth(np.inf, phi):.2f}"
        )

    finish_figures(
        {"gears_involute_profile.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
