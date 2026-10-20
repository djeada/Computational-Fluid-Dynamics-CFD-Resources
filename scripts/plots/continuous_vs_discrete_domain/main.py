"""From a continuous domain to a discrete one, and the error that discretization introduces.

The model problem du/dx + u = 0 on [0, 1] with u(0) = 1 has the exact solution
u = exp(-x). Replacing the derivative by a backward difference on N equally
spaced grid points gives u_i = u_{i-1} / (1 + dx). The figure contrasts the
continuous and the discrete description of the same field, compares the
discrete solutions on 4, 8 and 16 points with the exact solution, and shows
the error at x = 1 decreasing in proportion to dx, the formal first order of
the scheme.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

INLET_VALUE = 1.0  # u(0), dimensionless
N_COMPARE = (4, 8, 16)  # grid points in the solution panel
N_STUDY = (4, 8, 16, 32, 64, 128, 256)  # grid points in the convergence study


def exact_solution(x):
    """u(x) = u(0) exp(-x)."""
    return INLET_VALUE * np.exp(-x)


def solve_backward_difference(n_points):
    """Solve (u_i - u_{i-1}) / dx + u_i = 0 with u_1 = u(0) on n_points nodes.

    Returns the node coordinates and the discrete solution. The system is
    lower bidiagonal, so forward substitution gives u_i = u_{i-1} / (1 + dx).
    """
    if n_points < 2:
        raise ValueError("need at least two grid points")
    x = np.linspace(0.0, 1.0, n_points)
    dx = x[1] - x[0]
    u = INLET_VALUE * (1.0 + dx) ** -np.arange(n_points)
    return x, u


def assemble_system(n_points):
    """Matrix and right-hand side of the discrete system (Dirichlet row first)."""
    dx = 1.0 / (n_points - 1)
    a = np.diag(np.full(n_points, 1.0 + dx)) + np.diag(np.full(n_points - 1, -1.0), -1)
    a[0, 0] = 1.0
    b = np.zeros(n_points)
    b[0] = INLET_VALUE
    return a, b


def outlet_errors(n_points_seq=N_STUDY):
    """Grid spacing and |u_N - exp(-1)| for every grid of the sequence."""
    dx = 1.0 / (np.asarray(n_points_seq) - 1.0)
    err = np.array(
        [
            abs(solve_backward_difference(n)[1][-1] - exact_solution(1.0))
            for n in n_points_seq
        ]
    )
    return dx, err


def observed_orders(dx, err):
    """Observed order between consecutive grids with non-constant ratio."""
    return np.log(err[:-1] / err[1:]) / np.log(dx[:-1] / dx[1:])


def make_figure():
    fig = plt.figure(figsize=(13, 8.5))
    grid = fig.add_gridspec(2, 2, height_ratios=(0.75, 1.0))
    colors = plt.get_cmap("tab10").colors

    ax = fig.add_subplot(grid[0, :])
    xf = np.linspace(0.0, 1.0, 400)
    ax.plot(xf, exact_solution(xf) + 1.3, color="k", linewidth=2)
    ax.fill_between(xf, 1.3, exact_solution(xf) + 1.3, color="0.85")
    ax.plot([0, 1], [1.3, 1.3], color="k", linewidth=1)
    ax.text(
        1.13, 1.95, "continuous: $u(x)$ defined at every $x$ in [0, 1]", va="center"
    )
    x, u = solve_backward_difference(N_COMPARE[0])
    ax.plot([0, 1], [0.0, 0.0], color="k", linewidth=1)
    ax.vlines(x, 0.0, u, color=colors[0], linewidth=2)
    ax.plot(x, u, "o", color=colors[0], markersize=9)
    for i, (xi, ui) in enumerate(zip(x, u), start=1):
        ax.text(xi + 0.012, ui + 0.06, f"$u_{i} = {ui:.4f}$", fontsize=10)
        ax.text(xi, -0.18, f"$x_{i}$", ha="center", fontsize=10)
    ax.text(
        1.13,
        0.5,
        "discrete: $u_i$ stored only at the grid points\n"
        rf"$x_i = (i - 1)\Delta x$, $\Delta x = 1/{N_COMPARE[0] - 1}$",
        va="center",
    )
    ax.set_xlim(-0.03, 1.68)
    ax.set_ylim(-0.3, 2.45)
    ax.axis("off")
    ax.set_title("(a) The same field on a continuous and on a discrete domain")

    ax = fig.add_subplot(grid[1, 0])
    ax.plot(xf, exact_solution(xf), "k-", linewidth=2, label=r"exact $e^{-x}$")
    for k, n in enumerate(N_COMPARE):
        x, u = solve_backward_difference(n)
        ax.plot(x, u, "o-", color=colors[k + 1], label=f"N = {n} points", markersize=6)
    ax.set_xlabel("x [-]")
    ax.set_ylabel("u [-]")
    ax.set_title(r"(b) Backward-difference solutions of $du/dx + u = 0$")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(loc="upper right")

    ax = fig.add_subplot(grid[1, 1])
    dx, err = outlet_errors()
    p = observed_orders(dx, err)
    ax.loglog(
        dx, err, "o-", color=colors[0], label=f"error at x = 1, finest p = {p[-1]:.2f}"
    )
    ax.loglog(dx, 0.2 * dx, "k--", label="slope 1")
    ax.set_xlabel(r"Grid spacing $\Delta x$ [-]")
    ax.set_ylabel(r"$|u_N - e^{-1}|$ [-]")
    ax.set_title("(c) Grid convergence of the outlet value")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    a, b = assemble_system(N_COMPARE[0])
    print("System for N = 4 (rows: Dirichlet, then backward differences):")
    print(np.array2string(a, precision=4))
    print("solution:", np.linalg.solve(a, b))
    dx, err = outlet_errors()
    p = observed_orders(dx, err)
    for k, n in enumerate(N_STUDY):
        line = f"  N = {n:3d}, dx = {dx[k]:.5f}: error at x = 1 = {err[k]:.5f}"
        line += f" ({100 * err[k] / exact_solution(1.0):.2f}%)"
        if k > 0:
            line += f", p = {p[k - 1]:.3f}"
        print(line)

    fig = make_figure()
    finish_figures(
        {"continuous_vs_discrete_domain.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
