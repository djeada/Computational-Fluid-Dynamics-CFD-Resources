"""Column buckling: critical stress against slenderness, buckled modes and a Southwell plot.

Panel (a) draws the column curves for a structural steel: the Euler hyperbola,
the Johnson parabola up to the transition slenderness where it touches the
Euler curve, the yield cut-off, the AISC 360 nominal curve and the secant
formula for two eccentricity ratios. The lower panels show the first buckled
mode for the four classic end conditions, computed with a finite-element
eigenvalue problem (Hermite beam elements with the consistent geometric
stiffness matrix); the effective-length factor K is recovered from the
computed critical load. Panel (b) is a Southwell plot of synthetic test
readings on an imperfect pin-ended strut.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

E_STEEL = 200.0e9  # Young's modulus (Pa)
SIGMA_Y = 250.0e6  # yield strength (Pa)
ECCENTRICITY_RATIOS = (0.1, 0.3)  # e c / r^2 for the secant-formula curves
N_ELEMENTS = 40  # elements per column in the buckling eigenproblem

# Southwell test on a pin-ended solid round steel strut.
STRUT_LENGTH = 2.0  # m
STRUT_DIAMETER = 0.030  # m
STRUT_CROOKEDNESS = STRUT_LENGTH / 1000  # initial mid-height bow (m)
READING_NOISE = 0.02e-3  # standard deviation of the dial-gauge readings (m)
SEED = 3

END_CONDITIONS = {
    # name: (constrained DOFs at x = 0, constrained DOFs at x = L, theoretical K)
    "Pinned-pinned": (("v",), ("v",), 1.0),
    "Fixed-free": (("v", "theta"), (), 2.0),
    "Fixed-pinned": (("v", "theta"), ("v",), 0.699),
    "Fixed-fixed": (("v", "theta"), ("v", "theta"), 0.5),
}


def euler_stress(slenderness, e=E_STEEL):
    """Euler critical stress pi^2 E / (KL/r)^2 (Pa)."""
    return np.pi**2 * e / np.asarray(slenderness, dtype=float) ** 2


def transition_slenderness(e=E_STEEL, sy=SIGMA_Y):
    """Slenderness where the Johnson parabola touches the Euler curve."""
    return np.sqrt(2 * np.pi**2 * e / sy)


def johnson_stress(slenderness, e=E_STEEL, sy=SIGMA_Y):
    """Johnson parabola sy - (sy lambda / (2 pi))^2 / E (Pa)."""
    lam = np.asarray(slenderness, dtype=float)
    return sy - (sy * lam / (2 * np.pi)) ** 2 / e


def aisc_stress(slenderness, e=E_STEEL, sy=SIGMA_Y):
    """AISC 360 nominal flexural-buckling stress F_cr (Pa)."""
    fe = euler_stress(np.maximum(slenderness, 1e-9), e)
    return np.where(sy / fe <= 2.25, 0.658 ** (sy / fe) * sy, 0.877 * fe)


def secant_stress(slenderness, ecc_ratio, e=E_STEEL, sy=SIGMA_Y):
    """Mean stress P/A at which the secant formula reaches first yield (Pa)."""

    def peak_minus_yield(mean, lam):
        arg = 0.5 * lam * np.sqrt(mean / e)
        return mean * (1 + ecc_ratio / np.cos(arg)) - sy

    out = []
    for lam in np.atleast_1d(slenderness):
        upper = min(sy, euler_stress(lam, e)) * (1 - 1e-12)
        out.append(brentq(peak_minus_yield, 1e-6 * sy, upper, args=(lam,)))
    return np.array(out)


def beam_matrices(length, n_elements, ei=1.0):
    """Global elastic and geometric stiffness of a column, DOFs (v, theta) per node."""
    h = length / n_elements
    ke = (ei / h**3) * np.array(
        [
            [12, 6 * h, -12, 6 * h],
            [6 * h, 4 * h**2, -6 * h, 2 * h**2],
            [-12, -6 * h, 12, -6 * h],
            [6 * h, 2 * h**2, -6 * h, 4 * h**2],
        ]
    )
    kg = (1 / (30 * h)) * np.array(
        [
            [36, 3 * h, -36, 3 * h],
            [3 * h, 4 * h**2, -3 * h, -(h**2)],
            [-36, -3 * h, 36, -3 * h],
            [3 * h, -(h**2), -3 * h, 4 * h**2],
        ]
    )
    n_dof = 2 * (n_elements + 1)
    k = np.zeros((n_dof, n_dof))
    g = np.zeros((n_dof, n_dof))
    for el in range(n_elements):
        dofs = slice(2 * el, 2 * el + 4)
        k[dofs, dofs] += ke
        g[dofs, dofs] += kg
    return k, g


def buckling_mode(condition, length=1.0, ei=1.0, n_elements=N_ELEMENTS):
    """Lowest critical load and mode of a column with the named end conditions.

    Solves K phi = P K_G phi. Returns (P_cr, x, v) with v scaled to max |v| = 1.
    """
    base, top, _ = END_CONDITIONS[condition]
    k, g = beam_matrices(length, n_elements, ei)
    offset = {"v": 0, "theta": 1}
    last = 2 * n_elements
    fixed = [offset[d] for d in base] + [last + offset[d] for d in top]
    free = np.setdiff1d(np.arange(k.shape[0]), fixed)
    values, vectors = eigh(k[np.ix_(free, free)], g[np.ix_(free, free)])
    u = np.zeros(k.shape[0])
    u[free] = vectors[:, 0]
    v = u[0::2]
    v /= v[np.argmax(np.abs(v))]
    return values[0], np.linspace(0, length, n_elements + 1), v


def effective_length_factor(condition, n_elements=N_ELEMENTS):
    """K = sqrt(pi^2 EI / (P_cr L^2)) from the finite-element critical load."""
    p_cr, _, _ = buckling_mode(condition, n_elements=n_elements)
    return np.pi / np.sqrt(p_cr)


def southwell_readings(seed=SEED):
    """Synthetic loads (N) and extra mid-height deflections (m) of the test strut."""
    area = np.pi * STRUT_DIAMETER**2 / 4
    inertia = area * STRUT_DIAMETER**2 / 16
    p_cr = np.pi**2 * E_STEEL * inertia / STRUT_LENGTH**2
    rng = np.random.default_rng(seed)
    loads = p_cr * np.linspace(0.15, 0.85, 12)
    ratio = loads / p_cr
    delta = STRUT_CROOKEDNESS * ratio / (1 - ratio)
    return p_cr, loads, delta + READING_NOISE * rng.standard_normal(loads.size)


def southwell_fit(loads, delta):
    """Fit delta/P = delta/P_cr + delta_0/P_cr; return (P_cr, delta_0)."""
    slope, intercept = np.polyfit(delta, delta / loads, 1)
    return 1 / slope, intercept / slope


def plot_column_curves(ax):
    """Panel (a): critical stress against slenderness."""
    lam = np.linspace(1, 250, 600)
    lam_t = transition_slenderness()
    lam_y = np.sqrt(np.pi**2 * E_STEEL / SIGMA_Y)
    mpa = 1e-6
    ax.plot(lam, euler_stress(lam) * mpa, ":", color="0.4", label="Euler hyperbola")
    above = lam >= lam_t
    ax.plot(lam[above], euler_stress(lam[above]) * mpa, color="tab:blue", lw=2.5)
    ax.plot(
        lam[~above],
        johnson_stress(lam[~above]) * mpa,
        color="tab:blue",
        lw=2.5,
        label="Johnson + Euler (used in design)",
    )
    ax.plot(
        lam,
        aisc_stress(lam) * mpa,
        "--",
        color="tab:orange",
        lw=2,
        label="AISC 360 $F_{cr}$",
    )
    for ratio, style in zip(
        ECCENTRICITY_RATIOS, ("-.", (0, (5, 1, 1, 1))), strict=True
    ):
        ax.plot(
            lam,
            secant_stress(lam, ratio) * mpa,
            linestyle=style,
            color="tab:green",
            label=f"secant formula, $ec/r^2$ = {ratio}",
        )
    ax.axhline(SIGMA_Y * mpa, color="tab:red", lw=1.2, label=r"yield $\sigma_Y$")
    ax.axvline(lam_t, color="0.5", lw=0.8)
    ax.annotate(
        rf"$\lambda_t = \sqrt{{2\pi^2E/\sigma_Y}}$ = {lam_t:.1f}",
        (lam_t, SIGMA_Y / 2 * mpa),
        xytext=(8, 40),
        textcoords="offset points",
        fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "0.3"},
    )
    ax.plot(lam_y, SIGMA_Y * mpa, "o", color="0.3")
    ax.annotate(
        f"Euler = yield at {lam_y:.1f}",
        (lam_y, SIGMA_Y * mpa),
        xytext=(10, 18),
        textcoords="offset points",
        fontsize=10,
    )
    ax.set(
        xlim=(0, 250),
        ylim=(0, 1.35 * SIGMA_Y * mpa),
        xlabel="slenderness ratio $KL/r$",
        ylabel=r"critical stress $\sigma_{cr} = P_{cr}/A$ (MPa)",
        title=f"(a) Column curves, E = {E_STEEL / 1e9:.0f} GPa, "
        rf"$\sigma_Y$ = {SIGMA_Y * mpa:.0f} MPa",
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, lw=0.5, alpha=0.5)


def plot_southwell(ax):
    """Panel (b): Southwell plot of the synthetic test readings."""
    p_true, loads, delta = southwell_readings()
    p_fit, d0_fit = southwell_fit(loads, delta)
    ax.plot(delta * 1e3, delta / loads * 1e6, "o", color="tab:blue", label="readings")
    line = np.linspace(0, delta.max() * 1.1, 2)
    ax.plot(
        line * 1e3,
        (line + d0_fit) / p_fit * 1e6,
        color="tab:orange",
        label=rf"fit: $P_{{cr}}$ = {p_fit / 1e3:.2f} kN, $\delta_0$ = {d0_fit * 1e3:.2f} mm",
    )
    ax.set(
        xlabel=r"extra mid-height deflection $\delta$ (mm)",
        ylabel=r"$\delta / P$ (mm/kN)",
        title=f"(b) Southwell plot (exact $P_{{cr}}$ = {p_true / 1e3:.2f} kN)",
    )
    ax.set_xlim(left=0)
    ax.set_ylim(0, 1.4 * (delta / loads).max() * 1e6)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, lw=0.5, alpha=0.5)


def draw_end(ax, y, kinds, top):
    """Draw a pin (triangle) or a fixed end (hatched wall) at height y."""
    sign = 1 if top else -1
    if "theta" in kinds:
        ax.plot([-0.35, 0.35], [y, y], color="k", lw=2.5)
        for xs in np.linspace(-0.3, 0.3, 6):
            ax.plot([xs, xs + 0.08], [y, y + sign * 0.05], color="k", lw=1)
    elif "v" in kinds:
        ax.fill(
            [0, -0.12, 0.12],
            [y, y + sign * 0.09, y + sign * 0.09],
            facecolor="0.8",
            edgecolor="k",
        )
        ax.plot([-0.18, 0.18], [y + sign * 0.09] * 2, color="k")


def plot_mode(ax, condition):
    """One mode-shape panel: undeformed axis, buckled shape, supports, K."""
    base, top, k_theory = END_CONDITIONS[condition]
    _, x, v = buckling_mode(condition)
    k_fe = effective_length_factor(condition)
    ax.plot([0, 0], [0, 1], color="0.6", lw=1, ls="--")
    ax.plot(0.3 * v, x, color="tab:blue", lw=2.5)
    draw_end(ax, 0.0, base, top=False)
    draw_end(ax, 1.0, top, top=True)
    if not top:
        ax.annotate(
            "",
            (0.3 * v[-1], 1.12),
            (0.3 * v[-1], 1.0 + 0.25),
            arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2},
        )
    else:
        ax.annotate(
            "",
            (0, 1.12),
            (0, 1.25),
            arrowprops={"arrowstyle": "-|>", "color": "tab:red", "lw": 2},
        )
    ax.set_title(f"{condition}\nK = {k_fe:.3f} (theory {k_theory})", fontsize=11)
    ax.set(xlim=(-0.55, 0.55), ylim=(-0.15, 1.3), aspect="equal")
    ax.axis("off")


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    lam_t = transition_slenderness()
    print(f"transition slenderness sqrt(2 pi^2 E / sY) = {lam_t:.2f}")
    print(f"Euler = yield at KL/r = {np.sqrt(np.pi**2 * E_STEEL / SIGMA_Y):.2f}")
    for condition, (_, _, k_theory) in END_CONDITIONS.items():
        print(
            f"{condition:14s} K from FE = {effective_length_factor(condition):.4f}"
            f" (theory {k_theory})"
        )
    p_true, loads, delta = southwell_readings()
    p_fit, d0_fit = southwell_fit(loads, delta)
    print(
        f"Southwell: P_cr = {p_fit / 1e3:.3f} kN (exact {p_true / 1e3:.3f} kN), "
        f"delta_0 = {d0_fit * 1e3:.3f} mm (true {STRUT_CROOKEDNESS * 1e3:.3f} mm)"
    )

    fig = plt.figure(figsize=(13, 10.5))
    grid = fig.add_gridspec(2, 4, height_ratios=[1.15, 1], hspace=0.3, wspace=0.45)
    plot_column_curves(fig.add_subplot(grid[0, :3]))
    plot_southwell(fig.add_subplot(grid[0, 3]))
    for i, condition in enumerate(END_CONDITIONS):
        plot_mode(fig.add_subplot(grid[1, i]), condition)
    fig.text(
        0.5,
        0.455,
        "(c) First buckled mode from the finite-element eigenproblem $K\\phi = P K_G \\phi$",
        ha="center",
        fontsize=12,
    )

    finish_figures(
        {"beams_buckling_curves.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
