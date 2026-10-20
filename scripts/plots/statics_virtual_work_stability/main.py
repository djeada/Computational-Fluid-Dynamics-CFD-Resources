"""Potential energy and stability of a spring-loaded two-bar linkage (snap-through).

Two rigid bars AB and BC of length L are pinned at A, joined by a pin at B, and
end in a roller C on a horizontal guide. A linear spring of stiffness k holds C
and is unstretched at the angle theta0. A downward load P acts at B. The
single generalized coordinate is the bar angle theta, and the total potential
energy is V = 2 k L^2 (cos theta - cos theta0)^2 + P L sin theta. Equilibria
are the stationary points dV/dtheta = 0 (the principle of virtual work) and
are stable where d^2V/dtheta^2 > 0. The load-angle path has a limit point at
cos theta* = cos(theta0)^(1/3), beyond which the linkage snaps through.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

BAR_LENGTH = 0.5  # L (m)
SPRING_STIFFNESS = 4000.0  # k (N/m)
THETA0 = np.radians(30.0)  # angle at which the spring is unstretched (rad)
LOAD_RATIOS = (0.0, 0.05, 0.09, 0.12)  # P / (k L) for the energy curves
THETA_PLOT = np.radians(np.linspace(-55.0, 55.0, 2201))  # rad


def potential_energy(theta, load, k=SPRING_STIFFNESS, length=BAR_LENGTH, theta0=THETA0):
    """Total potential energy V (J): spring energy plus potential of the load P (N)."""
    stretch = 2.0 * length * (np.cos(theta) - np.cos(theta0))
    return 0.5 * k * stretch**2 + load * length * np.sin(theta)


def dv_dtheta(theta, load, k=SPRING_STIFFNESS, length=BAR_LENGTH, theta0=THETA0):
    """First derivative of V; its zeros are the equilibria (J/rad)."""
    c, s = np.cos(theta), np.sin(theta)
    return -4.0 * k * length**2 * (c - np.cos(theta0)) * s + load * length * c


def d2v_dtheta2(theta, load, k=SPRING_STIFFNESS, length=BAR_LENGTH, theta0=THETA0):
    """Second derivative of V; positive at a stable equilibrium (J/rad^2)."""
    c, s = np.cos(theta), np.sin(theta)
    return 4.0 * k * length**2 * (s**2 - c**2 + c * np.cos(theta0)) - load * length * s


def equilibrium_load(theta, k=SPRING_STIFFNESS, length=BAR_LENGTH, theta0=THETA0):
    """Load P (N) that holds the linkage at theta, from the virtual-work equation.

    delta U = (P L cos theta - F_s * 2 L sin theta) delta theta = 0 with the
    spring force F_s = 2 k L (cos theta - cos theta0) gives
    P = 4 k L (cos theta - cos theta0) tan theta.
    """
    return 4.0 * k * length * (np.cos(theta) - np.cos(theta0)) * np.tan(theta)


def limit_point(k=SPRING_STIFFNESS, length=BAR_LENGTH, theta0=THETA0):
    """Angle (rad) and load (N) at which dP/dtheta = 0: cos^3 theta* = cos theta0."""
    theta_star = np.arccos(np.cos(theta0) ** (1.0 / 3.0))
    return theta_star, 4.0 * k * length * np.sin(theta_star) ** 3


def equilibria(load, theta=THETA_PLOT, **params):
    """Roots of dV/dtheta on the grid, refined by bisection; returns (theta, stable)."""
    g = dv_dtheta(theta, load, **params)
    roots = [(t, d2v_dtheta2(t, load, **params) > 0) for t in theta[g == 0.0]]
    for i in np.flatnonzero(np.sign(g[:-1]) * np.sign(g[1:]) < 0):
        lo, hi = theta[i], theta[i + 1]
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if np.sign(dv_dtheta(mid, load, **params)) == np.sign(
                dv_dtheta(lo, load, **params)
            ):
                lo = mid
            else:
                hi = mid
        root = 0.5 * (lo + hi)
        roots.append((root, d2v_dtheta2(root, load, **params) > 0))
    return sorted(roots)


def zigzag(x0, x1, y, n=8, amplitude=0.03):
    """Coordinates of a spring drawn as a zigzag between x0 and x1 at height y."""
    x = np.linspace(x0, x1, 2 * n + 3)
    yy = np.full_like(x, y)
    yy[2:-2:2] += amplitude
    yy[3:-2:2] -= amplitude
    return x, yy


def draw_linkage(ax, theta, color, label, length=BAR_LENGTH):
    """Draw bars AB and BC at angle theta and return the joint coordinates."""
    a = np.array([0.0, 0.0])
    b = length * np.array([np.cos(theta), np.sin(theta)])
    c = np.array([2.0 * length * np.cos(theta), 0.0])
    ax.plot(
        *np.array([a, b, c]).T,
        "-o",
        color=color,
        linewidth=3,
        markersize=6,
        label=label,
    )
    return a, b, c


def make_figure():
    """Schematic, potential-energy curves and the equilibrium path."""
    k, length = SPRING_STIFFNESS, BAR_LENGTH
    kl = k * length
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), width_ratios=[1.0, 1.1, 1.1])

    ax = axes[0]
    wall = 2.0 * length * np.cos(THETA0) + 0.25
    theta_loaded = np.radians(20.0)
    draw_linkage(ax, THETA0, "0.7", r"unloaded, $\theta_0 = 30^\circ$")
    a, b, c = draw_linkage(ax, theta_loaded, "tab:blue", r"loaded, $\theta = 20^\circ$")
    ax.plot(*zigzag(c[0] + 0.02, wall, 0.0), color="black", linewidth=1.2)
    ax.plot([wall, wall], [-0.08, 0.12], color="black", linewidth=3)
    ax.plot([-0.08, wall], [-0.035, -0.035], color="0.4", linewidth=1)
    ax.fill([0, -0.04, 0.04], [0, -0.035, -0.035], color="0.4")
    ax.annotate(
        "",
        xy=b + [0, 0.01],
        xytext=b + [0, 0.17],
        arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2},
    )
    ax.text(b[0] + 0.03, b[1] + 0.13, "$P$", color="tab:red", fontsize=12)
    arc = np.linspace(0, theta_loaded, 30)
    ax.plot(0.15 * np.cos(arc), 0.15 * np.sin(arc), color="tab:blue", linewidth=1)
    ax.text(0.17, 0.02, r"$\theta$", color="tab:blue", fontsize=12)
    for name, point, dx, dy in (
        ("A", a, -0.03, -0.09),
        ("B", b, -0.09, 0.02),
        ("C", c, -0.03, -0.09),
    ):
        ax.text(point[0] + dx, point[1] + dy, name, fontsize=11)
    ax.text(0.5 * (c[0] + wall) - 0.03, 0.05, "$k$", fontsize=12)
    ax.set_aspect("equal")
    ax.set_xlim(-0.12, wall + 0.05)
    ax.set_ylim(-0.15, 0.55)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("(a) Linkage, L = 0.5 m, k = 4 kN/m")
    ax.legend(loc="upper right", fontsize=9)

    ax = axes[1]
    deg = np.degrees(THETA_PLOT)
    colors = plt.get_cmap("tab10").colors
    for ratio, color in zip(LOAD_RATIOS, colors, strict=False):
        load = ratio * kl
        ax.plot(
            deg,
            potential_energy(THETA_PLOT, load),
            color=color,
            linewidth=2,
            label=f"$P/(kL)$ = {ratio:g}",
        )
        for root, stable in equilibria(load):
            ax.plot(
                np.degrees(root),
                potential_energy(root, load),
                "o",
                markersize=8,
                markerfacecolor=color if stable else "white",
                markeredgecolor=color,
                markeredgewidth=2,
                zorder=5,
            )
    ax.set_xlim(-55, 55)
    ax.set_ylim(-85, 60)
    ax.set_xlabel(r"bar angle $\theta$ (deg)")
    ax.set_ylabel("total potential energy $V$ (J)")
    ax.set_title("(b) $V(\\theta)$: filled stable, open unstable")
    ax.legend(loc="lower right", fontsize=9)

    ax = axes[2]
    theta = np.radians(np.linspace(-60.0, 60.0, 2401))
    ratio = equilibrium_load(theta) / kl
    stable = d2v_dtheta2(theta, equilibrium_load(theta)) > 0
    deg = np.degrees(theta)
    ax.plot(
        deg,
        np.where(stable, ratio, np.nan),
        color="tab:blue",
        linewidth=2.5,
        label="stable",
    )
    ax.plot(
        deg,
        np.where(stable, np.nan, ratio),
        color="tab:orange",
        linewidth=2,
        linestyle="--",
        label="unstable",
    )
    theta_star, p_star = limit_point()
    ax.plot(
        np.degrees(theta_star), p_star / kl, "s", color="black", markersize=7, zorder=5
    )
    jump = [r for r, s in equilibria(p_star * 1.0001) if s and r < 0][0]
    ax.annotate(
        "",
        xy=(np.degrees(jump), p_star / kl),
        xytext=(np.degrees(theta_star), p_star / kl),
        arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 1.2, "linestyle": ":"},
    )
    ax.text(
        np.degrees(theta_star) + 3,
        p_star / kl + 0.012,
        f"limit point $\\theta^*$ = {np.degrees(theta_star):.1f}$^\\circ$\n"
        f"$P^*$ = {p_star:.0f} N",
        fontsize=9,
    )
    ax.text(np.degrees(jump) + 2, p_star / kl - 0.03, "snap-through", fontsize=9)
    ax.axhline(0, color="0.6", linewidth=0.8)
    ax.set_ylim(-0.2, 0.3)
    ax.set_xlabel(r"bar angle $\theta$ (deg)")
    ax.set_ylabel("load ratio $P/(kL)$")
    ax.set_title("(c) Equilibrium path from virtual work")
    ax.legend(loc="lower right", fontsize=9)
    for ax in axes[1:]:
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    kl = SPRING_STIFFNESS * BAR_LENGTH
    theta_star, p_star = limit_point()
    print(
        f"limit point: theta* = {np.degrees(theta_star):.2f} deg, P* = {p_star:.1f} N "
        f"(P*/kL = {p_star / kl:.4f})"
    )
    for ratio in LOAD_RATIOS:
        found = ", ".join(
            f"{np.degrees(r):+.2f} deg ({'stable' if s else 'unstable'})"
            for r, s in equilibria(ratio * kl)
        )
        print(f"P/(kL) = {ratio:g}: {found}")

    finish_figures(
        {"statics_virtual_work_stability.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
