"""Hierarchical kriging of the Forrester function from low- and high-fidelity data.

The high-fidelity function is f_h(x) = (6x - 2)^2 sin(12x - 4) on [0, 1] and the
low-fidelity function is f_l(x) = A f_h(x) + B (x - 0.5) - C with A = 0.5,
B = 10, C = -5 (Forrester, Sobester and Keane, 2007). An ordinary kriging model
of 11 low-fidelity samples becomes the trend of a kriging model of the few
high-fidelity samples, scaled by a factor beta_0 (Han and Goertz, 2012). The
figure compares this hierarchical kriging (HK) model with ordinary kriging of the
high-fidelity samples alone: predictions with +/- 2 sigma bands for the classic
four-sample case, and the test RMSE against the number of high-fidelity samples
averaged over random Latin hypercube designs.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

A, B, C = 0.5, 10.0, -5.0  # low-fidelity constants of Forrester et al. (2007)
N_LF = 11  # low-fidelity samples, equally spaced on [0, 1]
X_HF_CLASSIC = np.array([0.0, 0.4, 0.6, 1.0])  # high-fidelity design of the paper
N_HF_RANGE = range(3, 13)  # high-fidelity sample counts in the RMSE study
N_SEEDS = 20  # random high-fidelity designs per sample count
N_TEST = 501  # test points for the RMSE
LOG10_THETA_BOUNDS = (-2.0, 3.0)  # search range of log10(theta)
NUGGET = 1e-10  # added to the diagonal of R for round-off only
SEED = 0


def f_high(x):
    """High-fidelity Forrester function (6x - 2)^2 sin(12x - 4)."""
    return (6.0 * x - 2.0) ** 2 * np.sin(12.0 * x - 4.0)


def f_low(x):
    """Low-fidelity function A f_h(x) + B (x - 0.5) - C."""
    return A * f_high(x) + B * (x - 0.5) - C


def gaussian_correlation(xa, xb, theta):
    """R_ij = exp(-theta (xa_i - xb_j)^2) for 1D sample arrays."""
    return np.exp(-theta * (xa[:, None] - xb[None, :]) ** 2)


class Kriging:
    """Kriging with a one-column trend: ordinary (trend 1) or hierarchical.

    The model is y(x) = beta t(x) + Z(x), where Z is a zero-mean Gaussian process
    with variance sigma^2 and Gaussian correlation. With t(x) = 1 this is ordinary
    kriging; with t(x) a low-fidelity predictor it is hierarchical kriging and
    beta is the scaling factor beta_0. The correlation parameter theta is chosen
    by maximizing the concentrated log-likelihood unless it is given.
    """

    def __init__(self, x, y, trend=None, theta=None, nugget=NUGGET):
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.trend = trend if trend is not None else np.ones_like
        self.nugget = nugget
        self.t = self.trend(self.x)
        self.theta = self.fit_theta() if theta is None else float(theta)
        self._factorize(self.theta)

    def _factorize(self, theta):
        """Compute beta, sigma^2 and the solves needed by the predictor."""
        n = len(self.x)
        corr = gaussian_correlation(self.x, self.x, theta) + self.nugget * np.eye(n)
        chol = np.linalg.cholesky(corr)
        solve = lambda b: np.linalg.solve(chol.T, np.linalg.solve(chol, b))  # noqa: E731
        self.r_inv_t = solve(self.t)
        self.t_r_t = self.t @ self.r_inv_t
        self.beta = (self.r_inv_t @ self.y) / self.t_r_t
        self.residual_weights = solve(self.y - self.beta * self.t)
        self.sigma2 = (self.y - self.beta * self.t) @ self.residual_weights / n
        self.log_det = 2.0 * np.sum(np.log(np.diag(chol)))
        self.chol = chol

    def concentrated_log_likelihood(self, theta):
        """ln L(theta) = -(n/2) ln sigma^2(theta) - (1/2) ln det R(theta)."""
        try:
            self._factorize(theta)
        except np.linalg.LinAlgError:
            return -np.inf
        n = len(self.x)
        return -0.5 * n * np.log(max(self.sigma2, 1e-300)) - 0.5 * self.log_det

    def fit_theta(self):
        """Grid search in log10(theta), then a bounded 1D refinement."""
        grid = np.linspace(*LOG10_THETA_BOUNDS, 41)
        values = [self.concentrated_log_likelihood(10.0**g) for g in grid]
        k = int(np.argmax(values))
        lo = grid[max(k - 1, 0)]
        hi = grid[min(k + 1, len(grid) - 1)]
        result = minimize_scalar(
            lambda g: -self.concentrated_log_likelihood(10.0**g),
            bounds=(lo, hi),
            method="bounded",
        )
        best = result.x if -result.fun >= values[k] else grid[k]
        return 10.0**best

    def predict(self, x_new, return_mse=False):
        """Kriging predictor beta t(x) + r(x)^T R^-1 (y - beta t) and its MSE."""
        x_new = np.asarray(x_new, dtype=float)
        r = gaussian_correlation(x_new, self.x, self.theta)
        t_new = self.trend(x_new)
        y_hat = self.beta * t_new + r @ self.residual_weights
        if not return_mse:
            return y_hat
        r_inv_r = np.linalg.solve(self.chol.T, np.linalg.solve(self.chol, r.T))
        u = self.r_inv_t @ r.T - t_new
        mse = self.sigma2 * (1.0 - np.sum(r.T * r_inv_r, axis=0) + u**2 / self.t_r_t)
        return y_hat, np.maximum(mse, 0.0)


def fit_models(x_lf, x_hf):
    """Return (HF-only ordinary kriging, LF kriging, hierarchical kriging)."""
    hf_only = Kriging(x_hf, f_high(x_hf))
    lf_model = Kriging(x_lf, f_low(x_lf))
    hk = Kriging(x_hf, f_high(x_hf), trend=lf_model.predict)
    return hf_only, lf_model, hk


def rmse(model, x_test):
    return np.sqrt(np.mean((model.predict(x_test) - f_high(x_test)) ** 2))


def latin_hypercube_1d(n, rng):
    """One random point in each of n equal intervals of [0, 1]."""
    return np.sort((rng.permutation(n) + rng.uniform(size=n)) / n)


def rmse_study(x_lf, x_test, seed=SEED):
    """Mean and quartiles of the test RMSE of both models over random designs."""
    rng = np.random.default_rng(seed)
    lf_model = Kriging(x_lf, f_low(x_lf))
    results = {"kriging": [], "hk": []}
    for n_hf in N_HF_RANGE:
        errs = {"kriging": [], "hk": []}
        for _ in range(N_SEEDS):
            x_hf = latin_hypercube_1d(n_hf, rng)
            errs["kriging"].append(rmse(Kriging(x_hf, f_high(x_hf)), x_test))
            hk = Kriging(x_hf, f_high(x_hf), trend=lf_model.predict)
            errs["hk"].append(rmse(hk, x_test))
        for key, values in errs.items():
            results[key].append(np.percentile(values, [25, 50, 75]))
    return {key: np.array(value) for key, value in results.items()}


def plot_prediction(ax, model, x_plot, x_hf, title, x_lf=None):
    y_hat, mse = model.predict(x_plot, return_mse=True)
    band = 2.0 * np.sqrt(mse)
    ax.fill_between(
        x_plot,
        y_hat - band,
        y_hat + band,
        color="tab:blue",
        alpha=0.2,
        label=r"$\pm 2\hat{s}$",
    )
    ax.plot(x_plot, f_high(x_plot), "k-", lw=1.5, label=r"$f_h$ (truth)")
    ax.plot(x_plot, f_low(x_plot), color="tab:orange", ls=":", lw=1.5, label=r"$f_l$")
    ax.plot(x_plot, y_hat, color="tab:blue", ls="--", lw=2, label="prediction")
    if x_lf is not None:
        ax.plot(
            x_lf,
            f_low(x_lf),
            "o",
            color="tab:orange",
            mfc="white",
            ms=7,
            label="LF samples",
        )
    ax.plot(x_hf, f_high(x_hf), "s", color="k", ms=8, label="HF samples")
    ax.set_ylim(-12, 22)
    ax.set_xlabel("$x$ [-]")
    ax.set_ylabel("$y$ [-]")
    ax.set_title(title)
    ax.legend(loc="upper left", fontsize=10)


def make_figure(x_lf, x_hf, x_test, study):
    hf_only, _, hk = fit_models(x_lf, x_hf)
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.8))
    plot_prediction(
        axs[0],
        hf_only,
        x_test,
        x_hf,
        f"Kriging, 4 HF samples: RMSE {rmse(hf_only, x_test):.2f}",
    )
    plot_prediction(
        axs[1],
        hk,
        x_test,
        x_hf,
        f"HK, 11 LF + 4 HF samples: RMSE {rmse(hk, x_test):.2f}",
        x_lf=x_lf,
    )
    n_hf = np.array(list(N_HF_RANGE))
    for key, colour, label in (
        ("kriging", "tab:red", "kriging, HF only"),
        ("hk", "tab:blue", "hierarchical kriging"),
    ):
        q = study[key]
        axs[2].fill_between(n_hf, q[:, 0], q[:, 2], color=colour, alpha=0.2)
        axs[2].semilogy(
            n_hf, q[:, 1], "o-", color=colour, label=f"{label}: median, quartiles"
        )
    axs[2].set_xlabel("number of HF samples [-]")
    axs[2].set_ylabel("test RMSE [-]")
    axs[2].set_title(f"Test RMSE, {N_SEEDS} random HF designs")
    axs[2].grid(True, which="both", alpha=0.3)
    axs[2].set_ylim(0.02, 60.0)
    axs[2].legend(loc="upper right", fontsize=10)
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    x_lf = np.linspace(0.0, 1.0, N_LF)
    x_test = np.linspace(0.0, 1.0, N_TEST)

    hf_only, lf_model, hk = fit_models(x_lf, X_HF_CLASSIC)
    lf_rmse = np.sqrt(np.mean((lf_model.predict(x_test) - f_low(x_test)) ** 2))
    print(f"LF kriging:   theta = {lf_model.theta:8.2f}, RMSE vs f_l = {lf_rmse:.3f}")
    print(
        f"HF kriging:   theta = {hf_only.theta:8.2f}, "
        f"RMSE = {rmse(hf_only, x_test):.3f}"
    )
    print(
        f"HK:           theta = {hk.theta:8.2f}, beta_0 = {hk.beta:.3f}, "
        f"RMSE = {rmse(hk, x_test):.3f}"
    )

    study = rmse_study(x_lf, x_test)
    print("n_HF  median RMSE kriging  median RMSE HK")
    for n, q_k, q_h in zip(N_HF_RANGE, study["kriging"], study["hk"]):
        print(f"{n:4d}  {q_k[1]:19.3f}  {q_h[1]:14.4f}")

    fig = make_figure(x_lf, X_HF_CLASSIC, x_test, study)
    finish_figures(
        {"hierarchical_kriging_multifidelity.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
