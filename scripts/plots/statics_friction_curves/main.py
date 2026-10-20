"""Coulomb friction regimes, the capstan equation and square-thread screw efficiency.

Panel (a) follows the friction force on a block pushed along a floor as the
push grows: friction matches the push up to mu_s N, then drops to mu_k N once
the block slides. Panel (b) plots the capstan ratio T2/T1 = exp(mu beta)
against wrap angle for several friction coefficients on a logarithmic axis.
Panel (c) plots the efficiency tan(lambda) / tan(lambda + phi) of a
square-threaded screw against lead angle, marks the maximum at
lambda = 45 deg - phi/2 and the self-locking limit lambda = phi.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

BLOCK_WEIGHT = 100.0  # N, normal force on a level floor
MU_STATIC = 0.5  # static coefficient for panel (a)
MU_KINETIC = 0.4  # kinetic coefficient for panel (a)
CAPSTAN_MU = (0.1, 0.2, 0.3, 0.5)  # belt-drum coefficients for panel (b)
MAX_TURNS = 3.0  # wrap angle range of panel (b), in full turns
SCREW_MU = (0.05, 0.1, 0.15, 0.25)  # thread coefficients for panel (c)


def friction_force(push, weight=BLOCK_WEIGHT, mu_s=MU_STATIC, mu_k=MU_KINETIC):
    """Friction force (N) on a block on a level floor for a horizontal push (N).

    The block stays at rest while the push is below mu_s W and the friction
    equals the push; once the push exceeds it the block slides and friction is
    mu_k W.
    """
    push = np.asarray(push, dtype=float)
    return np.where(push <= mu_s * weight, push, mu_k * weight)


def capstan_ratio(mu, wrap):
    """Tension ratio T2/T1 = exp(mu beta) at impending slip, wrap angle beta in rad."""
    return np.exp(mu * np.asarray(wrap))


def screw_efficiency(lead_angle, mu):
    """Efficiency of a square-threaded screw raising a load, lead angle in rad."""
    phi = np.arctan(mu)
    return np.tan(lead_angle) / np.tan(lead_angle + phi)


def make_figure():
    """Three panels: friction regimes, capstan curves, screw efficiency."""
    colors = plt.get_cmap("tab10").colors
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))

    ax = axes[0]
    push = np.linspace(0.0, 80.0, 801)
    f_max = MU_STATIC * BLOCK_WEIGHT
    rest = push <= f_max
    ax.plot(
        push[rest],
        friction_force(push[rest]),
        color=colors[0],
        linewidth=2.5,
        label=r"at rest: $f = P \leq \mu_s N$",
    )
    ax.plot(
        push[~rest],
        friction_force(push[~rest]),
        color=colors[1],
        linewidth=2.5,
        label=r"sliding: $f = \mu_k N$",
    )
    ax.plot(
        [f_max, f_max],
        [MU_KINETIC * BLOCK_WEIGHT, f_max],
        color="0.5",
        linestyle=":",
        linewidth=1.2,
    )
    ax.plot(f_max, f_max, "o", color="black", markersize=7, zorder=5)
    ax.annotate(
        "impending motion\n$f = \\mu_s N$ = 50 N",
        xy=(f_max, f_max),
        xytext=(f_max - 33, f_max + 4),
        arrowprops={"arrowstyle": "->"},
        fontsize=9,
    )
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 62)
    ax.set_xlabel("horizontal push $P$ (N)")
    ax.set_ylabel("friction force $f$ (N)")
    ax.set_title(
        f"(a) Block on a floor, $N$ = {BLOCK_WEIGHT:.0f} N, "
        f"$\\mu_s$ = {MU_STATIC}, $\\mu_k$ = {MU_KINETIC}"
    )
    ax.legend(loc="lower right", fontsize=9)

    ax = axes[1]
    turns = np.linspace(0.0, MAX_TURNS, 301)
    for mu, color in zip(CAPSTAN_MU, colors, strict=False):
        ax.semilogy(
            turns,
            capstan_ratio(mu, 2 * np.pi * turns),
            color=color,
            linewidth=2,
            label=f"$\\mu$ = {mu}",
        )
    example = capstan_ratio(0.3, 2.5 * 2 * np.pi)
    ax.plot(2.5, example, "o", color="black", markersize=6, zorder=5)
    ax.annotate(
        f"2.5 turns, $\\mu$ = 0.3:\n$T_2/T_1$ = {example:.0f}",
        xy=(2.5, example),
        xytext=(1.0, 600),
        arrowprops={"arrowstyle": "->"},
        fontsize=9,
    )
    ax.set_xlim(0, MAX_TURNS)
    ax.set_ylim(1, 2e4)
    ax.set_xlabel(r"wrap angle $\beta$ (turns, $2\pi$ rad each)")
    ax.set_ylabel("tension ratio $T_2/T_1$")
    ax.set_title(r"(b) Capstan equation $T_2/T_1 = e^{\mu\beta}$")
    ax.legend(loc="upper left", fontsize=9)

    ax = axes[2]
    lead = np.radians(np.linspace(0.05, 80.0, 1600))
    for mu, color in zip(SCREW_MU, colors, strict=False):
        phi = np.arctan(mu)
        valid = lead + phi < np.pi / 2
        eff = screw_efficiency(lead[valid], mu)
        locking = lead[valid] <= phi
        ax.plot(
            np.degrees(lead[valid]),
            eff,
            color=color,
            linewidth=2,
            label=f"$\\mu$ = {mu}",
        )
        ax.plot(
            np.degrees(lead[valid][locking]),
            eff[locking],
            color=color,
            linewidth=6,
            alpha=0.35,
            solid_capstyle="butt",
        )
        best = np.pi / 4 - phi / 2
        ax.plot(
            np.degrees(best),
            screw_efficiency(best, mu),
            "^",
            color=color,
            markersize=7,
            markeredgecolor="black",
            zorder=5,
        )
    ax.axhline(0.5, color="0.5", linestyle=":", linewidth=1)
    ax.text(
        38,
        0.36,
        "self-locking range $\\lambda \\leq \\phi$ (shaded)\nalways has $\\eta < 0.5$",
        fontsize=9,
        ha="center",
    )
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r"lead angle $\lambda$ (deg)")
    ax.set_ylabel(r"efficiency $\eta$ raising the load")
    ax.set_title(r"(c) Square-thread screw, $\triangle$ = maximum")
    ax.legend(loc="lower center", fontsize=9)

    for ax in axes:
        ax.grid(True, linewidth=0.5, alpha=0.5, which="major")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    print(
        f"block: slips at P = {MU_STATIC * BLOCK_WEIGHT:.0f} N, "
        f"then friction = {MU_KINETIC * BLOCK_WEIGHT:.0f} N"
    )
    for mu in CAPSTAN_MU:
        print(f"capstan mu = {mu}: T2/T1 = {capstan_ratio(mu, 2 * np.pi):.2f} per turn")
    for mu in SCREW_MU:
        phi = np.arctan(mu)
        best = np.pi / 4 - phi / 2
        print(
            f"screw mu = {mu}: phi = {np.degrees(phi):.2f} deg, "
            f"eta at lambda = phi: {screw_efficiency(phi, mu):.3f}, "
            f"max eta {screw_efficiency(best, mu):.3f} at {np.degrees(best):.1f} deg"
        )

    finish_figures(
        {"statics_friction_curves.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
