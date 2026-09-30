"""Kriging-type interpolation with a cubic spline correlation function.

Samples y(x) = (3x - 3)^2 sin(2x - 10) at 11 points in [0, 1], solves the
interpolation system R w = y for four values of the correlation parameter
theta, and compares each interpolant with the true function.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_SAMPLES = 11  # training points in [0, 1]
N_PREDICT = 100  # prediction points in [0, 1]
THETA_VALUES = [0.1, 3.0, 6.5, 10.0]  # correlation parameters, one panel each


def test_function(x):
    """Ground truth y(x) = (3x - 3)^2 sin(2x - 10)."""
    return (3 * x - 3) ** 2 * np.sin(2 * x - 10)


def cubic_spline(h, theta):
    """Cubic spline correlation in the scaled lag xi = theta |h|."""
    xi = theta * np.abs(h)
    return np.where(
        xi <= 1,
        1 - 1.5 * xi**2 + 0.75 * xi**3,
        np.where(xi <= 2, 0.25 * (2 - xi) ** 3, 0.0),
    )


def fit_weights(x_data, y_data, theta):
    """Solve R w = y with R_ij = R(x_i - x_j; theta)."""
    corr = cubic_spline(x_data[:, None] - x_data[None, :], theta)
    return np.linalg.solve(corr, y_data)


def predict(x_new, x_data, weights, theta):
    """Evaluate y~(x) = sum_i w_i R(x - x_i; theta)."""
    return cubic_spline(x_new[:, None] - x_data[None, :], theta) @ weights


def plot_interpolants(x_data, y_data, x_fine, thetas):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    for ax, theta in zip(axs.ravel(), thetas):
        weights = fit_weights(x_data, y_data, theta)
        y_fine = predict(x_fine, x_data, weights, theta)

        ax.plot(x_fine, test_function(x_fine), "k--", label="$y(x)$")
        ax.plot(x_fine, y_fine, "b-", label=r"$\tilde{y}(x)$")
        ax.plot(x_data, y_data, "ks", label="samples")
        ax.set_title(rf"$\theta={theta}$")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.legend()
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    x_data = np.linspace(0.0, 1.0, N_SAMPLES)
    y_data = test_function(x_data)
    x_fine = np.linspace(0.0, 1.0, N_PREDICT)
    fig = plot_interpolants(x_data, y_data, x_fine, THETA_VALUES)

    finish_figures(
        {"kriging_interpolation.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
