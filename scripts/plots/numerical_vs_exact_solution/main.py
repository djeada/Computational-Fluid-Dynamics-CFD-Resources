"""Compare a finite-difference solution of du/dx + u = 0 with the exact solution e^{-x}.

The ODE du/dx + u = 0 on 0 <= x <= 1 with u(0) = 1 is discretised with the
first-order backward difference (u_i - u_{i-1}) / dx + u_i = 0, which gives
u_i = u_{i-1} / (1 + dx). With the default 4 grid points (dx = 1/3) this
reproduces the values 1, 3/4, 9/16, 27/64 used in the notes. The top panel
compares the discrete and exact solutions; the bottom panel shows the
pointwise error.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

X_END = 1.0  # right end of the domain [-]
U0 = 1.0  # boundary value u(0) [-]
N_POINTS = 4  # number of grid points, including both ends (dx = 1/3)


def exact_solution(x):
    """Exact solution u(x) = u0 * exp(-x)."""
    return U0 * np.exp(-x)


def solve_backward_difference(n_points=N_POINTS, x_end=X_END, u0=U0):
    """March (u_i - u_{i-1}) / dx + u_i = 0 from x = 0 and return x_i and u_i."""
    x = np.linspace(0.0, x_end, n_points)
    dx = x[1] - x[0]
    u = np.empty(n_points)
    u[0] = u0
    for i in range(1, n_points):
        u[i] = u[i - 1] / (1.0 + dx)
    return x, u


def plot_comparison(x, u_num, error):
    """Plot the exact and discrete solutions and the pointwise error."""
    x_fine = np.linspace(0.0, X_END, 100)
    fig, (ax, ax_err) = plt.subplots(
        2, 1, figsize=(6, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    ax.plot(x_fine, exact_solution(x_fine), label="Exact solution", color="black")
    ax.plot(x, u_num, "ro-", label="Numerical solution", markersize=5)
    ax.set_ylabel("u")
    ax.set_title(f"du/dx + u = 0, backward difference, {len(x)} points")
    ax.legend()
    ax.grid(True)

    ax_err.axhline(0.0, color="black", lw=0.8)
    ax_err.plot(x, error, "rs-", markersize=5)
    ax_err.set_xlabel("x")
    ax_err.set_ylabel(r"$e_i = u(x_i) - u_i$")
    ax_err.grid(True)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--points",
        type=int,
        default=N_POINTS,
        help=f"number of grid points (default {N_POINTS}, dx = 1/3)",
    )
    args = parser.parse_args(argv)
    if args.points < 2:
        parser.error("--points must be at least 2")

    x, u_num = solve_backward_difference(args.points)
    u_exact = exact_solution(x)
    error = u_exact - u_num

    print(f"{'x':>8} {'u_num':>10} {'u_exact':>10} {'error':>10} {'rel. err %':>10}")
    for xi, ui, ue, ei in zip(x, u_num, u_exact, error):
        print(f"{xi:8.4f} {ui:10.6f} {ue:10.6f} {ei:10.6f} {100 * abs(ei) / ue:10.2f}")

    fig = plot_comparison(x, u_num, error)

    finish_figures(
        {"numerical_vs_exact_solution.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
