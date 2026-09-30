"""Plot four correlation functions used in kriging for several values of theta.

Evaluates the linear, exponential, Gaussian and cubic spline correlation
functions R(h; theta) on lags h in [-2, 2] and overlays the curves for
theta = 0.5, 1 and 2 in a 2 x 2 figure.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

H_MAX = 2.0  # lag range is [-H_MAX, H_MAX]
N_LAGS = 400  # number of lag samples
THETAS = [0.5, 1.0, 2.0]  # correlation parameters to compare


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


def plot_correlation_functions(h, thetas):
    """Plot R(h; theta) for every correlation function, one panel each."""
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (name, func) in zip(axs.ravel(), CORRELATION_FUNCTIONS.items()):
        for theta in thetas:
            ax.plot(h, func(h, theta), label=rf"$\theta={theta}$")
        ax.set_title(name)
        ax.set_xlabel("$h$")
        ax.set_ylabel(r"$R(h;\theta)$")
        ax.legend()
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    h = np.linspace(-H_MAX, H_MAX, N_LAGS)
    fig = plot_correlation_functions(h, THETAS)

    finish_figures(
        {"correlation_functions.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
