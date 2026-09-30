"""Condition number of kriging correlation matrices as a function of theta.

Builds the correlation matrix of four correlation functions (linear,
exponential, Gaussian and cubic spline) on equally spaced points in [0, 1] and
plots its 2-norm condition number over a logarithmic sweep of the correlation
parameter theta.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_POINTS = 10  # number of sample locations in [0, 1]
THETA_MIN = 1e-2  # smallest correlation parameter in the sweep
THETA_MAX = 1e1  # largest correlation parameter in the sweep
N_THETA = 100  # number of theta values (log-spaced)


def linear(h, theta):
    """Linear correlation R(h; theta) = max(0, 1 - theta |h|)."""
    return np.maximum(0.0, 1.0 - theta * np.abs(h))


def exponential(h, theta):
    """Exponential correlation R(h; theta) = exp(-theta |h|)."""
    return np.exp(-theta * np.abs(h))


def gaussian(h, theta):
    """Gaussian correlation R(h; theta) = exp(-theta h^2)."""
    return np.exp(-theta * h**2)


def cubic_spline(h, theta):
    """Cubic spline correlation in the scaled lag xi = theta |h|."""
    xi = theta * np.abs(h)
    return np.where(
        xi <= 1,
        1 - 1.5 * xi**2 + 0.75 * xi**3,
        np.where(xi <= 2, 0.25 * (2 - xi) ** 3, 0.0),
    )


CORRELATION_FUNCTIONS = {
    "linear": linear,
    "exponential": exponential,
    "Gaussian": gaussian,
    "cubic spline": cubic_spline,
}


def lag_matrix(n_points):
    """Return H_ij = x_i - x_j for n_points equally spaced points in [0, 1]."""
    x = np.linspace(0.0, 1.0, n_points)
    return x[:, None] - x[None, :]


def condition_numbers(lags, thetas):
    """Condition number of R(H; theta) for every correlation function and theta."""
    return {
        name: np.array([np.linalg.cond(func(lags, theta)) for theta in thetas])
        for name, func in CORRELATION_FUNCTIONS.items()
    }


def plot_condition_numbers(thetas, cond_numbers):
    """Plot cond(R) against theta on log-log axes, one panel per function."""
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (name, values) in zip(axs.ravel(), cond_numbers.items()):
        ax.plot(thetas, values, "b-")
        ax.set_title(name)
        ax.set_xlabel(r"$\theta$")
        ax.set_ylabel("cond(R)")
        ax.set_xscale("log")
        ax.set_yscale("log")
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    thetas = np.logspace(np.log10(THETA_MIN), np.log10(THETA_MAX), N_THETA)
    cond_numbers = condition_numbers(lag_matrix(N_POINTS), thetas)
    fig = plot_condition_numbers(thetas, cond_numbers)

    finish_figures(
        {"condition_number_of_the_correlation_matrix.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
