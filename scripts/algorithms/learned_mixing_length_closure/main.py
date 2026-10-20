"""Learn a near-wall mixing-length closure from reference data and test it in a RANS solve.

Spalding's law of the wall plays the role of DNS data for the inner layer of
a turbulent wall flow. The eddy viscosity and mixing length implied by the
data are computed, and two corrections to Prandtl's mixing length l = kappa y
are fitted to the implied damping function on 1 <= y+ <= 100: a van Driest
damping with one learned constant A+, and an unconstrained cubic polynomial in
ln y+. Each closure is then inserted into the 1D RANS momentum equation, which
is integrated to y+ = 1000, and the predicted u+(y+) is compared with the
reference: the a priori fit and the a posteriori solution give different
rankings.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

KAPPA = 0.41  # von Karman constant
B = 5.2  # log-law intercept
TRAIN_RANGE = (1.0, 100.0)  # y+ range of the training data
N_TRAIN = 60  # log-spaced training points
Y_PLUS_MAX = 1000.0  # top of the RANS solution (inner layer, constant stress)
POLY_DEGREE = 3  # degree of the unconstrained regression in ln y+
A_PLUS_CLASSICAL = 26.0  # van Driest's original constant


def spalding_y_plus(u_plus):
    """Spalding's law: y+ as an explicit function of u+."""
    ku = KAPPA * u_plus
    return u_plus + np.exp(-KAPPA * B) * (np.exp(ku) - 1 - ku - ku**2 / 2 - ku**3 / 6)


def reference_u_plus(y_plus, iterations=60):
    """Invert Spalding's law for u+(y+) by Newton iteration."""
    y_plus = np.asarray(y_plus, dtype=float)
    u = np.where(
        y_plus < 5, y_plus, np.log(np.maximum(y_plus, 1e-12)) / KAPPA + B - 1.0
    )
    for _ in range(iterations):
        u = u - (spalding_y_plus(u) - y_plus) / (1.0 + reference_eddy_viscosity_u(u))
    return u


def reference_eddy_viscosity_u(u_plus):
    """nu_t+ = dy+/du+ - 1 implied by Spalding's law at constant total stress."""
    ku = KAPPA * u_plus
    return np.exp(-KAPPA * B) * KAPPA * (np.exp(ku) - 1 - ku - ku**2 / 2)


def implied_closure(y_plus):
    """Eddy viscosity, mixing length and damping D = l+ / (kappa y+) from the data.

    With constant total stress tau+ = (1 + nu_t+) du+/dy+ = 1, the data give
    nu_t+ = 1 / (du+/dy+) - 1, and nu_t+ = l+^2 du+/dy+ gives l+.
    """
    nu_t = reference_eddy_viscosity_u(reference_u_plus(y_plus))
    mixing_length = np.sqrt(nu_t * (1.0 + nu_t))
    return nu_t, mixing_length, mixing_length / (KAPPA * y_plus)


def velocity_gradient(mixing_length):
    """Solve (1 + l^2 g) g = 1 for g = du+/dy+ >= 0 (positive root)."""
    return 2.0 / (1.0 + np.sqrt(1.0 + 4.0 * mixing_length**2))


def solve_rans(damping, y_plus):
    """Integrate the 1D RANS momentum equation with l+ = kappa y+ D(y+).

    d/dy+ [(1 + nu_t+) du+/dy+] = 0 with u+(0) = 0 and unit wall stress is
    integrated once to (1 + nu_t+) du+/dy+ = 1, and solve_ivp integrates
    du+/dy+ = g(y+) from the wall to y_plus[-1].
    """

    def rhs(y, _u):
        return [velocity_gradient(KAPPA * y * damping(max(y, 1e-12)))]

    solution = solve_ivp(
        rhs,
        (0.0, y_plus[-1]),
        [0.0],
        t_eval=y_plus,
        rtol=1e-9,
        atol=1e-11,
        max_step=2.0,
    )
    return solution.y[0]


def van_driest(a_plus):
    """Damping function D = 1 - exp(-y+ / A+)."""
    return lambda y: 1.0 - np.exp(-np.asarray(y) / a_plus)


def fit_van_driest(y_train, damping_train):
    """Least-squares fit of A+ to the data-implied damping (a priori)."""
    result = least_squares(
        lambda q: van_driest(q[0])(y_train) - damping_train, [20.0], bounds=(1, 200)
    )
    return result.x[0]


def fit_polynomial(y_train, damping_train, degree=POLY_DEGREE):
    """Unconstrained regression D = poly(ln y+), clipped at zero."""
    coefficients = np.polyfit(np.log(y_train), damping_train, degree)
    return lambda y: np.clip(np.polyval(coefficients, np.log(y)), 0.0, None)


def build_closures():
    """Return the training data and a dict of named damping functions."""
    y_train = np.geomspace(*TRAIN_RANGE, N_TRAIN)
    _, _, damping_train = implied_closure(y_train)
    a_plus = fit_van_driest(y_train, damping_train)
    closures = {
        r"Prandtl $\ell = \kappa y$ (no damping)": lambda y: np.ones_like(
            np.asarray(y, dtype=float)
        ),
        f"van Driest, learned $A^+ = {a_plus:.1f}$": van_driest(a_plus),
        "cubic in $\\ln y^+$ (unconstrained)": fit_polynomial(y_train, damping_train),
    }
    return y_train, damping_train, a_plus, closures


def make_figure(y, u_ref, damping_ref, y_train, closures, solutions, table_rows):
    colours = ("tab:red", "tab:blue", "tab:orange")
    fig, axs = plt.subplots(2, 2, figsize=(13, 9.5))

    ax = axs[0, 0]
    ax.semilogx(y, damping_ref, color="k", linewidth=2.5, label="reference (data)")
    ax.semilogx(y_train[::3], implied_closure(y_train[::3])[2], "ko", ms=4)
    for colour, (name, damping) in zip(colours, closures.items()):
        ax.semilogx(y, damping(y), "--", color=colour, linewidth=1.8, label=name)
    ax.axvspan(*TRAIN_RANGE, color="0.9", zorder=0)
    ax.text(10, 1.32, "training range", ha="center", fontsize=10)
    ax.set_ylim(0, 1.45)
    ax.set_xlabel("$y^+$")
    ax.set_ylabel(r"damping $D = \ell^+ / (\kappa y^+)$")
    ax.set_title("(a) A priori: fitted damping functions")
    ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(0.0, 0.9))
    ax.grid(True, which="both", alpha=0.3)

    ax = axs[0, 1]
    ax.semilogx(y, u_ref, color="k", linewidth=2.5, label="reference (Spalding)")
    for colour, (name, u) in zip(colours, solutions.items()):
        ax.semilogx(y, u, "--", color=colour, linewidth=1.8, label=name)
    ax.semilogx(y[y < 12], y[y < 12], ":", color="0.5", label="$u^+ = y^+$")
    log_y = y[y > 20]
    ax.semilogx(log_y, np.log(log_y) / KAPPA + B, "-.", color="0.5", label="log law")
    ax.axvspan(*TRAIN_RANGE, color="0.9", zorder=0)
    ax.set_ylim(0, 30)
    ax.set_xlabel("$y^+$")
    ax.set_ylabel("$u^+$")
    ax.set_title("(b) A posteriori: RANS solution $u^+(y^+)$")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)

    ax = axs[1, 0]
    for colour, (name, u) in zip(colours, solutions.items()):
        ax.loglog(y, np.abs(u - u_ref) + 1e-6, color=colour, linewidth=1.8, label=name)
    ax.axvspan(*TRAIN_RANGE, color="0.9", zorder=0)
    ax.set_ylim(1e-3, 30)
    ax.set_xlabel("$y^+$")
    ax.set_ylabel(r"$|u^+ - u^+_\mathrm{ref}|$")
    ax.set_title("(c) A posteriori velocity error")
    ax.legend(fontsize=9, loc="lower right")
    ax.grid(True, which="both", alpha=0.3)

    ax = axs[1, 1]
    ax.axis("off")
    table = ax.table(
        cellText=[row[1:] for row in table_rows],
        rowLabels=[row[0] for row in table_rows],
        colLabels=[
            "a priori\nmax $|\\Delta D|$,\n$1 \\leq y^+ \\leq 100$",
            "a posteriori\nmax $|\\Delta u^+|$,\n$y^+ \\leq 100$",
            "a posteriori\nmax $|\\Delta u^+|$,\n$y^+ \\leq 1000$",
        ],
        loc="center right",
        cellLoc="center",
        colWidths=[0.22, 0.22, 0.22],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 3.2)
    ax.set_title("(d) A priori and a posteriori errors")

    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    y = np.geomspace(0.1, Y_PLUS_MAX, 300)
    u_ref = reference_u_plus(y)
    _, _, damping_ref = implied_closure(y)
    y_train, damping_train, a_plus, closures = build_closures()
    solutions = {name: solve_rans(damping, y) for name, damping in closures.items()}

    inner = y <= TRAIN_RANGE[1]
    short_names = ("Prandtl", f"van Driest\n$A^+$={a_plus:.1f}", "cubic\nregression")
    table_rows = []
    print(f"learned van Driest constant A+ = {a_plus:.2f}")
    for short, (name, damping) in zip(short_names, closures.items()):
        prior = np.abs(damping(y_train) - damping_train).max()
        error = np.abs(solutions[name] - u_ref)
        table_rows.append(
            [short, f"{prior:.3f}", f"{error[inner].max():.2f}", f"{error.max():.2f}"]
        )
        print(
            f"{short.replace(chr(10), ' '):24s} a priori max|dD| = {prior:.3f}, "
            f"max|du+| (y+ <= 100) = {error[inner].max():.2f}, "
            f"(y+ <= 1000) = {error.max():.2f}"
        )
    classical = solve_rans(van_driest(A_PLUS_CLASSICAL), y)
    print(
        f"classical van Driest A+ = {A_PLUS_CLASSICAL:.0f}: "
        f"max|du+| = {np.abs(classical - u_ref).max():.2f}"
    )

    fig = make_figure(y, u_ref, damping_ref, y_train, closures, solutions, table_rows)
    finish_figures(
        {"learned_mixing_length_closure.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
