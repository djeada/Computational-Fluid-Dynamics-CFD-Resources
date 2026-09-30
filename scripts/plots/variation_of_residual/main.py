"""Residual history of a Gauss-Seidel solve of the 1D Laplace equation.

Solves u'' = 0 on N points with Dirichlet boundary values, starting from a
random interior guess, and plots the normalised RMS change between successive
iterates on a logarithmic axis until it drops below a convergence criterion.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures, positive_int  # noqa: E402

N = 100  # number of grid points
U_LEFT, U_RIGHT = 0.0, 1.0  # Dirichlet boundary values
MAX_ITERATIONS = 50000
CONVERGENCE_CRITERION = 1e-9
SEED = 0


def compute_residual(u, u_old):
    """Normalised RMS change: RMS(u - u_old) / mean(|u_old|)."""
    return np.sqrt(np.mean((u - u_old) ** 2)) / np.mean(np.abs(u_old))


def gauss_seidel_sweep(u):
    """One in-place lexicographic Gauss-Seidel sweep for u[i-1] - 2 u[i] + u[i+1] = 0."""
    for i in range(1, len(u) - 1):
        u[i] = 0.5 * (u[i - 1] + u[i + 1])


def solve(
    n=N,
    max_iterations=MAX_ITERATIONS,
    tol=CONVERGENCE_CRITERION,
    seed=SEED,
):
    """Iterate until the residual is below ``tol`` or ``max_iterations`` is reached.

    Returns the final solution and the list of residuals.
    """
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    u[0], u[-1] = U_LEFT, U_RIGHT

    residuals = []
    for _ in range(max_iterations):
        u_old = u.copy()
        gauss_seidel_sweep(u)
        residual = compute_residual(u, u_old)
        residuals.append(residual)
        if residual < tol:
            break
    return u, residuals


def plot_residuals(residuals, tol=CONVERGENCE_CRITERION):
    """Plot residual against iteration number on a log scale; return the figure."""
    iterations = np.arange(1, len(residuals) + 1)
    fig = plt.figure(figsize=(10, 6))
    plt.plot(
        iterations,
        residuals,
        marker="o",
        markevery=max(1, len(residuals) // 25),
        color="r",
    )
    plt.axhline(
        tol, color="gray", linestyle="--", label=f"convergence criterion ({tol:g})"
    )
    plt.yscale("log")
    plt.xlabel("Iteration number")
    plt.ylabel("Residual")
    plt.title("Variation of the residual with iterations")
    plt.grid(True)
    plt.legend()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=MAX_ITERATIONS,
        metavar="N",
        help=f"maximum number of iterations (default {MAX_ITERATIONS})",
    )
    args = parser.parse_args(argv)

    u, residuals = solve(max_iterations=args.steps)
    exact = np.linspace(U_LEFT, U_RIGHT, N)
    print(
        f"{len(residuals)} iterations, final residual {residuals[-1]:.3e}, "
        f"max error vs exact solution {np.max(np.abs(u - exact)):.3e}"
    )

    fig = plot_residuals(residuals)

    finish_figures(
        {"variation_of_residual.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
