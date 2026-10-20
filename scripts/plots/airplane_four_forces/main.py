"""Free-body diagram of a light aircraft in a steady climb, with its force polygon.

Computes lift, drag, weight and thrust of a 1100 kg aircraft climbing at
40 m/s on a 6 degree flight path from the equilibrium conditions
L = W cos(gamma) and T = D + W sin(gamma) with the parabolic polar
C_D = C_D0 + k C_L^2, and draws them on a side view of the aircraft and as a
closed force polygon. Thrust is assumed to act along the flight path.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

RHO = 1.225  # kg/m^3
G = 9.81  # m/s^2
MASS = 1100.0  # kg
WING_AREA = 16.2  # m^2
SPAN = 11.0  # m
OSWALD = 0.80
CD0 = 0.027
SPEED = 40.0  # m/s, climb speed
CLIMB_ANGLE = 6.0  # deg, flight-path angle gamma


def climb_forces(speed=SPEED, gamma_deg=CLIMB_ANGLE):
    """Return a dict with L, D, W, T (N), C_L, C_D and the rate of climb."""
    gamma = np.radians(gamma_deg)
    w = MASS * G
    q = 0.5 * RHO * speed**2
    k = 1 / (np.pi * OSWALD * SPAN**2 / WING_AREA)
    lift = w * np.cos(gamma)
    cl = lift / (q * WING_AREA)
    cd = CD0 + k * cl**2
    drag = q * WING_AREA * cd
    thrust = drag + w * np.sin(gamma)
    return dict(
        L=lift,
        D=drag,
        W=w,
        T=thrust,
        CL=cl,
        CD=cd,
        rate_of_climb=speed * np.sin(gamma),
        excess_power=(thrust - drag) * speed,
        gamma=gamma,
    )


def _rotate(points, angle):
    c, s = np.cos(angle), np.sin(angle)
    return points @ np.array([[c, s], [-s, c]])


def draw_aircraft(ax, pitch):
    """Side-view silhouette pitched nose-up by `pitch` radians about the CG."""
    fuselage = Ellipse(
        (0.0, 0.0), 7.5, 1.1, angle=np.degrees(pitch), fc="0.8", ec="0.3"
    )
    ax.add_patch(fuselage)
    tail = np.array([[-3.4, 0.2], [-3.9, 1.6], [-3.3, 1.6], [-2.6, 0.3]])
    stab = np.array([[-3.9, 0.05], [-3.1, 0.05], [-3.1, -0.1], [-3.9, -0.1]])
    wing = np.array([[0.7, 0.05], [-0.8, 0.05], [-0.8, -0.15], [0.7, -0.1]])
    for shape in (tail, stab, wing):
        ax.add_patch(Polygon(_rotate(shape, pitch), closed=True, fc="0.6", ec="0.3"))


def _arrow(ax, start, vec, colour, label, offset=(0.15, 0.15), at=1.0, **text_kw):
    ax.annotate(
        "",
        xy=start + vec,
        xytext=start,
        arrowprops=dict(arrowstyle="-|>", lw=2.5, color=colour, mutation_scale=18),
    )
    point = start + at * vec
    ax.text(
        point[0] + offset[0],
        point[1] + offset[1],
        label,
        color=colour,
        fontsize=11,
        **text_kw,
    )


def plot_forces(f):
    gamma = f["gamma"]
    scale = 6.0 / f["W"]  # drawing units per newton
    along = np.array([np.cos(gamma), np.sin(gamma)])
    normal = np.array([-np.sin(gamma), np.cos(gamma)])
    vec = dict(
        L=f["L"] * scale * normal,
        D=-f["D"] * scale * along,
        W=np.array([0.0, -f["W"] * scale]),
        T=f["T"] * scale * along,
    )
    colours = dict(L="tab:blue", D="tab:red", W="0.2", T="tab:green")

    fig, axes = plt.subplots(
        1, 2, figsize=(12.5, 5.6), gridspec_kw=dict(width_ratios=[1.4, 1])
    )
    ax = axes[0]
    draw_aircraft(ax, gamma)
    origin = np.zeros(2)
    nose, tail = 3.75 * along, -3.75 * along
    _arrow(
        ax,
        origin,
        vec["L"],
        colours["L"],
        f"Lift L\n{f['L']:,.0f} N",
        offset=(0.25, -0.6),
    )
    _arrow(
        ax,
        origin,
        vec["W"],
        colours["W"],
        f"Weight W\n{f['W']:,.0f} N",
        offset=(0.25, 0.2),
    )
    _arrow(
        ax,
        nose,
        vec["T"],
        colours["T"],
        f"Thrust T\n{f['T']:,.0f} N",
        offset=(-0.4, 0.35),
    )
    _arrow(
        ax,
        tail,
        vec["D"],
        colours["D"],
        f"Drag D\n{f['D']:,.0f} N",
        offset=(-0.9, -1.05),
    )
    ax.plot(0, 0, "o", color="k", ms=5)
    ax.text(0.15, -0.55, "CG", fontsize=10)
    base = np.array([-5.0, -3.2])
    ax.plot(*np.c_[base, base + 10.2 * along], ":", color="0.4")
    ax.annotate(
        "",
        xy=base + 10.5 * along,
        xytext=base + 9.0 * along,
        arrowprops=dict(arrowstyle="-|>", color="0.4"),
    )
    ax.text(1.0, -3.2, f"flight path, V = {SPEED:g} m/s", color="0.3", fontsize=10)
    ax.plot(*np.c_[base, base + [3.5, 0]], color="0.5", lw=0.8)
    arc = np.linspace(0, gamma, 20)
    ax.plot(base[0] + 3.0 * np.cos(arc), base[1] + 3.0 * np.sin(arc), color="0.3")
    ax.text(
        base[0] + 3.4, base[1] - 0.05, rf"$\gamma = {CLIMB_ANGLE:g}^\circ$", fontsize=11
    )
    ax.set_xlim(-6, 6)
    ax.set_ylim(-7, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a) Forces on the aircraft, drawn to scale")

    ax = axes[1]
    start = np.zeros(2)
    label_offsets = dict(W=(0.12, 0.0), L=(-0.45, 0.0), D=(-0.1, 0.12), T=(-0.1, 0.12))
    for key in ("W", "L", "D", "T"):
        _arrow(
            ax, start, vec[key], colours[key], key, offset=label_offsets[key], at=0.5
        )
        start = start + vec[key]
    closure = np.linalg.norm(start) / scale
    ax.plot(0, 0, "o", color="k")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-6.6, 0.6)
    ax.set_xlabel("Horizontal (drawing units)")
    ax.set_ylabel("Vertical (drawing units)")
    ax.set_title(f"(b) Force polygon W + L + D + T, closure error {closure:.1e} N")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig, closure


def main(argv=None):
    args = create_parser(__doc__).parse_args(argv)
    f = climb_forces()
    print(
        f"V = {SPEED:g} m/s, gamma = {CLIMB_ANGLE:g} deg: C_L = {f['CL']:.3f}, "
        f"C_D = {f['CD']:.4f}, L/D = {f['CL'] / f['CD']:.2f}"
    )
    print(
        f"  W = {f['W']:.0f} N, L = {f['L']:.0f} N, D = {f['D']:.0f} N, "
        f"T = {f['T']:.0f} N, rate of climb = {f['rate_of_climb']:.2f} m/s, "
        f"excess power = {f['excess_power'] / 1e3:.1f} kW"
    )
    fig, closure = plot_forces(f)
    print(f"  force polygon closure error = {closure:.2e} N")
    finish_figures(
        {"airplane_four_forces.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
