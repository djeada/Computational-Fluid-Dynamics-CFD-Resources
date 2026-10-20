"""Picard iteration and Newton's method for the steady viscous Burgers equation.

Solves u u' = nu u'' on 0 < x < 1 with u(0) = 1 and u(1) = 0, whose exact
solution u = A tanh(A (1 - x) / (2 nu)) has a thin layer at x = 1. The equation
is discretised conservatively with central differences on N cells, and the
nonlinear algebraic system R(u) = 0 is solved by Picard iteration (lagging the
convecting velocity, with and without under-relaxation), by Newton's method,
by Newton's method with a backtracking line search, and by pseudo-transient
continuation. The figure compares the solutions with the exact one and the
convergence histories, which are linear for Picard and quadratic for Newton.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

VISCOSITY = 0.02  # nu (m^2/s, with u in m/s and x in m); layer thickness ~ 2 nu
N_CELLS = (
    64  # cell Peclet number u h / nu = 0.78 < 2, so central differences do not wiggle
)
U_LEFT, U_RIGHT = 1.0, 0.0  # Dirichlet values (m/s)
TOLERANCE = 1e-10  # converged when ||R||_2 < TOLERANCE
MAX_ITERATIONS = 200
UNDER_RELAXATION = 0.7  # alpha for under-relaxed Picard
HARD_GUESS_AMPLITUDE = -2.0  # u0 = 1 - x + a sin(pi x): reversed flow inside the domain
PSEUDO_TIME_STEP = 0.2  # initial pseudo-time step of pseudo-transient continuation (s)
ARMIJO = 1e-4  # sufficient-decrease constant of the line search
MIN_STEP = 1.0 / 1024  # smallest line-search step before the search is declared failed


def grid(n=N_CELLS):
    """Node coordinates and spacing of a uniform grid with n cells on [0, 1]."""
    return np.linspace(0.0, 1.0, n + 1), 1.0 / n


def exact_solution(x, nu=VISCOSITY):
    """u = A tanh(A (1 - x) / (2 nu)) with A tanh(A / (2 nu)) = 1 so that u(0) = 1."""
    a = brentq(lambda s: s * np.tanh(s / (2.0 * nu)) - 1.0, 0.5, 2.0)
    return a * np.tanh(a * (1.0 - x) / (2.0 * nu))


def linear_guess(x):
    """Straight line between the boundary values."""
    return U_LEFT + (U_RIGHT - U_LEFT) * x


def hard_guess(x, amplitude=HARD_GUESS_AMPLITUDE):
    """Initial guess with reversed flow in the interior: 1 - x + a sin(pi x)."""
    return linear_guess(x) + amplitude * np.sin(np.pi * x)


def residual(u, h, nu=VISCOSITY):
    """R_i = (u_{i+1}^2 - u_{i-1}^2) / (4h) - nu (u_{i+1} - 2u_i + u_{i-1}) / h^2."""
    r = np.zeros_like(u)
    r[1:-1] = (u[2:] ** 2 - u[:-2] ** 2) / (4.0 * h) - nu * (
        u[2:] - 2.0 * u[1:-1] + u[:-2]
    ) / h**2
    return r


def jacobian_bands(u, h, nu=VISCOSITY):
    """Tridiagonal Jacobian dR/du of the interior equations in solve_banded layout."""
    m = len(u) - 2
    ab = np.zeros((3, m))
    ab[0, 1:] = u[2:-1] / (2.0 * h) - nu / h**2  # dR_i / du_{i+1}
    ab[1, :] = 2.0 * nu / h**2  # dR_i / du_i
    ab[2, :-1] = -u[1:-2] / (2.0 * h) - nu / h**2  # dR_i / du_{i-1}
    return ab


def picard_bands(u, h, nu=VISCOSITY):
    """Matrix of the Picard system with the convecting velocity lagged at u."""
    m = len(u) - 2
    ab = np.zeros((3, m))
    ab[0, 1:] = u[2:-1] / (4.0 * h) - nu / h**2
    ab[1, :] = 2.0 * nu / h**2
    ab[2, :-1] = -u[1:-2] / (4.0 * h) - nu / h**2
    return ab


def picard(u0, h, alpha=1.0, nu=VISCOSITY, tol=TOLERANCE, max_iter=MAX_ITERATIONS):
    """Picard iteration A(u^k) u* = b(u^k), u^{k+1} = u^k + alpha (u* - u^k).

    Returns the final iterate, the list of iterates and the residual norms.
    """
    u = u0.copy()
    iterates, history = [u.copy()], [np.linalg.norm(residual(u, h, nu))]
    for _ in range(max_iter):
        rhs = np.zeros(len(u) - 2)
        rhs[0] = (u[0] / (4.0 * h) + nu / h**2) * u[0]  # known boundary value u_0
        rhs[-1] = -(u[-1] / (4.0 * h) - nu / h**2) * u[-1]  # known boundary value u_N
        u_star = solve_banded((1, 1), picard_bands(u, h, nu), rhs)
        u[1:-1] += alpha * (u_star - u[1:-1])
        iterates.append(u.copy())
        history.append(np.linalg.norm(residual(u, h, nu)))
        if history[-1] < tol or not history[-1] < 1e12:
            break
    return u, iterates, np.array(history)


def newton(
    u0,
    h,
    nu=VISCOSITY,
    line_search=False,
    pseudo_dt=None,
    tol=TOLERANCE,
    max_iter=MAX_ITERATIONS,
):
    """Newton's method J(u^k) du = -R(u^k), optionally globalised.

    ``line_search=True`` halves the step until ||R|| decreases sufficiently
    (Armijo) and stops if the step falls below MIN_STEP. ``pseudo_dt`` turns on
    pseudo-transient continuation: (I / dtau + J) du = -R with
    dtau = pseudo_dt ||R_0|| / ||R_k|| (switched evolution relaxation).
    Returns the final iterate, the list of iterates and the residual norms.
    """
    u = u0.copy()
    iterates, history = [u.copy()], [np.linalg.norm(residual(u, h, nu))]
    for _ in range(max_iter):
        r = residual(u, h, nu)
        ab = jacobian_bands(u, h, nu)
        if pseudo_dt is not None:
            ab[1, :] += history[-1] / (pseudo_dt * history[0])
        du = solve_banded((1, 1), ab, -r[1:-1])
        step = 1.0
        if line_search:
            while step >= MIN_STEP:
                trial = u.copy()
                trial[1:-1] += step * du
                if (
                    np.linalg.norm(residual(trial, h, nu))
                    <= (1 - ARMIJO * step) * history[-1]
                ):
                    break
                step *= 0.5
            else:
                break  # no acceptable step: the line search has failed
        u[1:-1] += step * du
        iterates.append(u.copy())
        history.append(np.linalg.norm(residual(u, h, nu)))
        if history[-1] < tol or not history[-1] < 1e12:
            break
    return u, iterates, np.array(history)


def error_sequence(iterates, converged):
    """Max-norm distance of each iterate from the converged discrete solution."""
    return np.array([np.max(np.abs(u - converged)) for u in iterates])


def convergence_order(errors, floor=1e-11):
    """Estimate q in e_{k+1} = C e_k^q from the last three errors above ``floor``."""
    e = errors[errors > floor]
    if len(e) < 3:
        raise ValueError("need at least three errors above the floor")
    return np.log(e[-1] / e[-2]) / np.log(e[-2] / e[-3])


def run():
    x, h = grid()
    u0 = linear_guess(x)
    results = {
        "Picard": picard(u0, h),
        rf"Picard, $\alpha$ = {UNDER_RELAXATION}": picard(
            u0, h, alpha=UNDER_RELAXATION
        ),
        "Newton": newton(u0, h),
    }
    ug = hard_guess(x)
    hard = {
        "Newton, full steps": newton(ug, h),
        "Newton + backtracking": newton(ug, h, line_search=True),
        "Pseudo-transient Newton": newton(ug, h, pseudo_dt=PSEUDO_TIME_STEP),
        rf"Picard, $\alpha$ = {UNDER_RELAXATION}": picard(
            ug, h, alpha=UNDER_RELAXATION
        ),
    }
    return x, h, results, hard


def make_figure(x, results, hard):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    colors = plt.get_cmap("tab10").colors
    u_newton = results["Newton"][0]

    ax = axes[0, 0]
    xf = np.linspace(0, 1, 801)
    x_coarse, _ = grid(N_CELLS // 2)
    u_coarse = newton(linear_guess(x_coarse), 1.0 / (N_CELLS // 2))[0]
    inset = ax.inset_axes([0.08, 0.1, 0.45, 0.55])
    for target in (ax, inset):
        target.plot(xf, exact_solution(xf), "k-", linewidth=1.5, label="exact")
        target.plot(
            x,
            u_newton,
            "o",
            color=colors[0],
            markersize=5,
            label=f"discrete, N = {N_CELLS}",
        )
        target.plot(
            x_coarse,
            u_coarse,
            "s",
            color=colors[1],
            markersize=5,
            fillstyle="none",
            label=f"discrete, N = {N_CELLS // 2}",
        )
    inset.set_xlim(0.85, 1.0)
    inset.set_ylim(-0.05, 1.05)
    inset.set_title("layer at x = 1", fontsize=10)
    inset.tick_params(labelsize=9)
    inset.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.add_patch(plt.Rectangle((0.85, -0.05), 0.15, 1.1, fill=False, edgecolor="0.4"))
    ax.set_xlabel("$x$ [m]", fontsize=11)
    ax.set_ylabel("$u$ [m/s]", fontsize=11)
    ax.set_ylim(-0.1, 1.15)
    ax.set_title(
        rf"(a) Steady Burgers, $\nu$ = {VISCOSITY}: converged solutions",
        fontsize=12,
    )
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="center", bbox_to_anchor=(0.71, 0.45))

    ax = axes[0, 1]
    for (name, (_, _, hist)), color in zip(results.items(), colors):
        ax.semilogy(
            hist, "o-", color=color, markersize=3, label=f"{name} ({len(hist) - 1} it.)"
        )
    ax.axhline(TOLERANCE, color="gray", linestyle="--", linewidth=1)
    ax.set_xlim(-1, 80)
    ax.set_ylim(1e-14, 1e7)
    ax.set_xlabel("Iteration $k$ [-]", fontsize=11)
    ax.set_ylabel(r"Residual norm $\|R(u^k)\|_2$ [-]", fontsize=11)
    ax.set_title("(b) Residual history from the linear guess", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper right")

    ax = axes[1, 0]
    for (name, (_, iterates, _)), color in zip(results.items(), colors):
        e = error_sequence(iterates, u_newton)
        keep = e > 1e-13
        e = e[keep]
        ax.loglog(e[:-1], e[1:], "o-", color=color, markersize=4, label=name)
    ee = np.logspace(-12, 0, 20)
    ax.loglog(ee, ee, "k:", linewidth=1, label="$e_{k+1} = e_k$")
    ax.loglog(ee, ee**2, "k--", linewidth=1, label="$e_{k+1} = e_k^2$ (slope 2)")
    ax.set_xlim(1e-12, 3)
    ax.set_ylim(1e-14, 3)
    ax.set_xlabel(r"Error $e_k = \|u^k - u_h\|_\infty$ [m/s]", fontsize=11)
    ax.set_ylabel(r"Next error $e_{k+1}$ [m/s]", fontsize=11)
    ax.set_title("(c) Linear against quadratic convergence", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower right")

    ax = axes[1, 1]
    styles = {"Newton + backtracking": dict(marker="s", markersize=7, linewidth=2.5)}
    for (name, (_, _, hist)), color in zip(hard.items(), colors[3:]):
        style = styles.get(name, dict(marker="o", markersize=3, linewidth=1.5))
        ax.semilogy(
            hist, color=color, label=name, zorder=3 if name in styles else 2, **style
        )
        if hist[-1] > TOLERANCE and hist[-1] < 1e12:
            ax.annotate(
                "line search fails",
                (len(hist) - 1, hist[-1]),
                xytext=(8, 2e3),
                fontsize=10,
                arrowprops=dict(arrowstyle="->", color=color),
                color=color,
            )
    ax.axhline(TOLERANCE, color="gray", linestyle="--", linewidth=1)
    ax.set_xlim(-1, 70)
    ax.set_ylim(1e-12, 1e13)
    ax.set_xlabel("Iteration $k$ [-]", fontsize=11)
    ax.set_ylabel(r"Residual norm $\|R(u^k)\|_2$ [-]", fontsize=11)
    ax.set_title(
        rf"(d) Hard guess $u^0 = 1 - x {HARD_GUESS_AMPLITUDE:+g}\,\sin(\pi x)$",
        fontsize=12,
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper right")

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x, _, results, hard = run()
    exact = exact_solution(x)
    u_ref = results["Newton"][0]
    print(
        f"nu = {VISCOSITY}, N = {N_CELLS}, max |u_h - u_exact| = {np.max(np.abs(u_ref - exact)):.3e}"
    )
    for label, group in (("linear guess", results), ("hard guess", hard)):
        for name, (u, iterates, hist) in group.items():
            status = "converged" if hist[-1] < TOLERANCE else "failed"
            plain = name.replace("$\\alpha$", "alpha")
            line = f"  {label:12s} {plain:28s} {len(hist) - 1:4d} iterations, final ||R|| = {hist[-1]:.2e} ({status})"
            if status == "converged" and label == "linear guess":
                e = error_sequence(iterates, u_ref)
                if "Newton" not in name:
                    tail = e[(e > 1e-9) & (e < 1e-3)]
                    rate = (tail[-1] / tail[0]) ** (1 / (len(tail) - 1))
                    line += f", mean error ratio per iteration {rate:.3f}"
            print(line)
    e_newton = error_sequence(results["Newton"][1], u_ref)
    print("  Newton errors:", " ".join(f"{v:.1e}" for v in e_newton[:-1]))

    fig = make_figure(x, results, hard)
    finish_figures(
        {"picard_vs_newton.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
