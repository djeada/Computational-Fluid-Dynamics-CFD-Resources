"""Compare model numerical solutions u_N(x) with the exact solution exp(-x).

Plots u_N(x) = exp(-x (1 + x / N)) for N = 4, 8 and 16 against u(x) = exp(-x)
on [0, 1] and prints the maximum error for each N, which halves as N doubles.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_VALUES = [4, 8, 16]  # grid resolution parameters
N_FINE = 100  # points used to draw the curves
X_DISCRETE = np.array([0, 0.25, 0.5, 0.75, 1])  # marker locations
LINE_STYLES = {4: "r-", 8: "b--", 16: "m:"}
MARKER_COLORS = {4: "red", 8: "blue", 16: "magenta"}


def exact_solution(x):
    """Exact solution u(x) = exp(-x)."""
    return np.exp(-x)


def numerical_solution(N, x):
    """Model numerical solution u_N(x) = exp(-x (1 + x / N))."""
    return np.exp(-x * (1 + x / N))


def max_errors(n_values, x):
    """Maximum of |u(x) - u_N(x)| over x for each N."""
    return {
        N: np.max(np.abs(exact_solution(x) - numerical_solution(N, x)))
        for N in n_values
    }


def plot_comparison(x_fine, n_values):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_fine, exact_solution(x_fine), label="Exact solution", color="black")

    for N in n_values:
        ax.plot(x_fine, numerical_solution(N, x_fine), LINE_STYLES[N], label=f"N={N}")
        ax.scatter(
            X_DISCRETE, numerical_solution(N, X_DISCRETE), color=MARKER_COLORS[N]
        )

    ax.set_xlabel("x")
    ax.set_ylabel("u")
    ax.legend()
    ax.set_title("Comparison of Numerical and Exact Solutions")
    ax.grid(True)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    x_fine = np.linspace(0, 1, N_FINE)
    errors = max_errors(N_VALUES, x_fine)
    previous = None
    for N, error in errors.items():
        ratio = (
            ""
            if previous is None
            else f"  (ratio to previous N: {previous / error:.2f})"
        )
        print(f"N = {N:2d}: max |u - u_N| = {error:.5f}{ratio}")
        previous = error

    fig = plot_comparison(x_fine, N_VALUES)

    finish_figures(
        {"comparing_grid_convergence.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
