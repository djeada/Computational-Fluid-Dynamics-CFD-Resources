"""Multiquadric radial basis function (RBF) interpolation of 11 data points.

Fits SciPy's ``Rbf`` interpolant with the multiquadric basis through a fixed
set of 11 points on [0, 1] and plots the interpolant on a fine grid.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Rbf

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Data points digitised from a reference plot
X_DATA = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
Y_DATA = np.array([0.0, 0.5, -0.5, -1.0, -0.5, 0.0, 1.0, 2.0, 4.0, 10.0, 20.0])
N_PREDICT = 100  # prediction points in [0, 1]


def fit_rbf(x, y, function="multiquadric"):
    """Build the SciPy RBF interpolant (default shape parameter epsilon)."""
    return Rbf(x, y, function=function)


def plot_interpolation(x, y, x_new, y_new):
    fig, ax = plt.subplots()
    ax.plot(x, y, "ks", label="Original points")
    ax.plot(x_new, y_new, "b-", label="RBF interpolation")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_title(r"RBF Interpolation $\tilde{y}(x)$")
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    rbf = fit_rbf(X_DATA, Y_DATA)
    print(f"Multiquadric shape parameter epsilon = {rbf.epsilon:.4f}")
    x_new = np.linspace(0.0, 1.0, N_PREDICT)
    fig = plot_interpolation(X_DATA, Y_DATA, x_new, rbf(x_new))

    finish_figures(
        {"radial_basis_functions.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
