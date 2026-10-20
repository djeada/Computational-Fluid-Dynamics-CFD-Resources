"""Radial basis function (RBF) interpolation with six kernels, written in numpy.

Interpolates eight equally spaced samples of the Forrester function
y(x) = (6x - 2)^2 sin(12x - 4) on [0, 1] with the Gaussian, multiquadric,
inverse multiquadric and Wendland C2 kernels (plain interpolation) and with the
thin-plate spline and cubic kernels (augmented with a linear polynomial tail).
The left panel shows the interpolants, the right panel their pointwise error.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_SAMPLES = 8  # equally spaced samples on [0, 1], spacing 1/7
N_PREDICT = 1001  # evaluation points on [0, 1]
EPSILON = 5.0  # shape parameter of the Gaussian, MQ and IMQ kernels [1/length]
WENDLAND_SUPPORT = 0.4  # support radius of the Wendland kernel [length]


def test_function(x):
    """Forrester function y(x) = (6x - 2)^2 sin(12x - 4)."""
    return (6.0 * x - 2.0) ** 2 * np.sin(12.0 * x - 4.0)


def thin_plate(r):
    """phi(r) = r^2 ln r with phi(0) = 0."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(r > 0.0, r**2 * np.log(np.where(r > 0.0, r, 1.0)), 0.0)


# name -> (phi(r), degree of the polynomial tail, -1 for none)
KERNELS = {
    "Gaussian": (lambda r: np.exp(-((EPSILON * r) ** 2)), -1),
    "multiquadric": (lambda r: np.sqrt(1.0 + (EPSILON * r) ** 2), -1),
    "inverse multiquadric": (lambda r: 1.0 / np.sqrt(1.0 + (EPSILON * r) ** 2), -1),
    "Wendland C2": (
        lambda r: (
            np.maximum(1.0 - r / WENDLAND_SUPPORT, 0.0) ** 4
            * (4.0 * r / WENDLAND_SUPPORT + 1.0)
        ),
        -1,
    ),
    "thin-plate spline + linear": (thin_plate, 1),
    "cubic + linear": (lambda r: r**3, 1),
}


def polynomial_matrix(x, degree):
    """Columns 1, x, ..., x^degree evaluated at the 1D points x."""
    return np.vander(x, degree + 1, increasing=True)


def fit_rbf(x, y, phi, degree=-1):
    """Solve [[A, P], [P^T, 0]] [w; c] = [y; 0] with A_ij = phi(|x_i - x_j|).

    Without a polynomial tail (degree = -1) this is A w = y.
    """
    a = phi(np.abs(x[:, None] - x[None, :]))
    if degree < 0:
        return np.linalg.solve(a, y), np.zeros(0)
    p = polynomial_matrix(x, degree)
    m = p.shape[1]
    system = np.block([[a, p], [p.T, np.zeros((m, m))]])
    sol = np.linalg.solve(system, np.concatenate([y, np.zeros(m)]))
    return sol[: len(x)], sol[len(x) :]


def evaluate_rbf(x_new, x, weights, coeffs, phi, degree=-1):
    """s(x) = sum_i w_i phi(|x - x_i|) + sum_k c_k x^k."""
    s = phi(np.abs(x_new[:, None] - x[None, :])) @ weights
    if degree >= 0:
        s = s + polynomial_matrix(x_new, degree) @ coeffs
    return s


def interpolate_all(x, y, x_new):
    """Return {kernel name: interpolant on x_new} for every kernel."""
    out = {}
    for name, (phi, degree) in KERNELS.items():
        w, c = fit_rbf(x, y, phi, degree)
        out[name] = evaluate_rbf(x_new, x, w, c, phi, degree)
    return out


def plot_interpolants(x, y, x_new, results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    truth = test_function(x_new)
    ax1.plot(x_new, truth, "k-", lw=2.5, label="$y(x)$ (truth)")
    styles = ["-", "--", "-.", ":", "--", "-."]
    for (name, s), ls in zip(results.items(), styles):
        ax1.plot(x_new, s, ls=ls, lw=1.5, label=name)
        ax2.semilogy(x_new, np.abs(s - truth) + 1e-12, ls=ls, lw=1.5, label=name)
    ax1.plot(x, y, "ks", ms=7, label="samples")
    ax1.set_ylim(-12, 22)
    ax1.set_xlabel("$x$ [-]")
    ax1.set_ylabel("$y$ [-]")
    ax1.set_title(f"Interpolants through {len(x)} samples")
    ax1.legend(loc="upper left", fontsize=10)
    ax2.set_ylim(1e-4, 1e2)
    ax2.set_xlabel("$x$ [-]")
    ax2.set_ylabel(r"$|s(x) - y(x)|$ [-]")
    ax2.set_title("Pointwise error (zero at the samples)")
    ax2.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    x = np.linspace(0.0, 1.0, N_SAMPLES)
    y = test_function(x)
    x_new = np.linspace(0.0, 1.0, N_PREDICT)
    results = interpolate_all(x, y, x_new)
    truth = test_function(x_new)
    print("kernel                       RMSE    max |error|")
    for name, s in results.items():
        err = np.abs(s - truth)
        print(f"{name:27s}  {np.sqrt(np.mean(err**2)):6.3f}  {err.max():6.3f}")

    fig = plot_interpolants(x, y, x_new, results)
    finish_figures(
        {"radial_basis_functions.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
