"""Ordinary kriging of the Forrester function with a cubic correlation function.

Samples y(x) = (6x - 2)^2 sin(12x - 4) at nine equally spaced points in [0, 1],
estimates the correlation parameter theta of a compactly supported cubic
correlation function by maximizing the concentrated log-likelihood, and compares
the kriging predictor and its +/- 2 sigma band for theta below, at and above the
maximum-likelihood value. This is the worked example of the kriging note.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_SAMPLES = 9  # training points, equally spaced in [0, 1]
N_PREDICT = 501  # prediction points in [0, 1]
THETA_GRID = np.linspace(0.5, 10.0, 1901)  # theta values for the likelihood scan
THETA_COMPARE = (1.75, 5.0)  # theta values compared with the MLE


def test_function(x):
    """Forrester function y(x) = (6x - 2)^2 sin(12x - 4)."""
    return (6.0 * x - 2.0) ** 2 * np.sin(12.0 * x - 4.0)


def cubic_correlation(h, theta):
    """Cubic correlation with support |h| < 1/theta, in xi = theta |h|.

    R = 1 - 6 xi^2 + 6 xi^3 for xi < 0.5, 2 (1 - xi)^3 for 0.5 <= xi < 1, else 0.
    """
    xi = theta * np.abs(h)
    return np.where(
        xi < 0.5,
        1.0 - 6.0 * xi**2 + 6.0 * xi**3,
        np.where(xi < 1.0, 2.0 * (1.0 - xi) ** 3, 0.0),
    )


def fit(x_data, y_data, theta):
    """Return the ordinary kriging quantities for a given theta.

    beta = 1^T R^-1 y / 1^T R^-1 1, sigma^2 = (y - beta)^T R^-1 (y - beta) / n
    and the concentrated log-likelihood -(n/2) ln sigma^2 - (1/2) ln det R.
    """
    n = len(x_data)
    corr = cubic_correlation(x_data[:, None] - x_data[None, :], theta)
    chol = np.linalg.cholesky(corr)
    ones = np.ones(n)
    r_inv_1 = np.linalg.solve(corr, ones)
    beta = r_inv_1 @ y_data / (r_inv_1 @ ones)
    weights = np.linalg.solve(corr, y_data - beta)
    sigma2 = (y_data - beta) @ weights / n
    log_lik = -0.5 * n * np.log(sigma2) - np.sum(np.log(np.diag(chol)))
    return {
        "theta": theta,
        "corr": corr,
        "beta": beta,
        "sigma2": sigma2,
        "weights": weights,
        "r_inv_1": r_inv_1,
        "log_lik": log_lik,
    }


def maximum_likelihood_theta(x_data, y_data, thetas=THETA_GRID):
    """Scan the concentrated log-likelihood and return (thetas, values, best)."""
    values = np.array([fit(x_data, y_data, t)["log_lik"] for t in thetas])
    return thetas, values, thetas[int(np.argmax(values))]


def predict(x_new, x_data, model):
    """Kriging predictor and MSE at x_new.

    y_hat = beta + r^T R^-1 (y - beta),
    MSE = sigma^2 (1 - r^T R^-1 r + (1 - 1^T R^-1 r)^2 / 1^T R^-1 1).
    """
    r = cubic_correlation(x_new[:, None] - x_data[None, :], model["theta"])
    y_hat = model["beta"] + r @ model["weights"]
    r_inv_r = np.linalg.solve(model["corr"], r.T)
    u = 1.0 - model["r_inv_1"] @ r.T
    mse = model["sigma2"] * (
        1.0 - np.sum(r.T * r_inv_r, axis=0) + u**2 / np.sum(model["r_inv_1"])
    )
    return y_hat, np.maximum(mse, 0.0)


def rmse(x_fine, y_hat):
    return np.sqrt(np.mean((y_hat - test_function(x_fine)) ** 2))


def plot_results(x_data, y_data, x_fine, scan, models):
    thetas, values, best = scan
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    ax = axs[0, 0]
    ax.plot(thetas, values, color="tab:purple", lw=2)
    ax.axvline(best, color="k", ls="--", lw=1, label=rf"MLE $\theta^* = {best:.2f}$")
    for t in THETA_COMPARE:
        ax.axvline(t, color="tab:gray", ls=":", lw=1)
    ax.set_xlabel(r"$\theta$ [-]")
    ax.set_ylabel(r"concentrated $\ln L(\theta)$ [-]")
    ax.set_title("Concentrated log-likelihood")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    for ax, model in zip(axs.ravel()[1:], models):
        y_hat, mse = predict(x_fine, x_data, model)
        band = 2.0 * np.sqrt(mse)
        ax.fill_between(
            x_fine,
            y_hat - band,
            y_hat + band,
            color="tab:blue",
            alpha=0.2,
            label=r"$\hat{y} \pm 2\hat{s}$",
        )
        ax.plot(x_fine, test_function(x_fine), "k-", lw=1.5, label="$y(x)$")
        ax.plot(x_fine, y_hat, color="tab:blue", ls="--", lw=2, label=r"$\hat{y}(x)$")
        ax.plot(x_data, y_data, "ks", ms=7, label="samples")
        ax.set_ylim(-14, 22)
        ax.set_title(
            rf"$\theta = {model['theta']:.2f}$: RMSE {rmse(x_fine, y_hat):.2f}, "
            rf"$\hat\beta = {model['beta']:.2f}$"
        )
        ax.set_xlabel("$x$ [-]")
        ax.set_ylabel("$y$ [-]")
        ax.legend(loc="upper left", fontsize=10)
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

    scan = maximum_likelihood_theta(x_data, y_data)
    thetas = sorted((*THETA_COMPARE, scan[2]))
    models = [fit(x_data, y_data, t) for t in thetas]
    print(" theta    ln L    beta   sigma^2   RMSE   max |error|")
    for model in models:
        y_hat, _ = predict(x_fine, x_data, model)
        err = np.abs(y_hat - test_function(x_fine))
        print(
            f"{model['theta']:6.3f}  {model['log_lik']:6.2f}  {model['beta']:5.2f}"
            f"  {model['sigma2']:7.2f}  {rmse(x_fine, y_hat):5.3f}  {err.max():6.3f}"
        )

    fig = plot_results(x_data, y_data, x_fine, scan, models)
    finish_figures(
        {"kriging_interpolation.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
