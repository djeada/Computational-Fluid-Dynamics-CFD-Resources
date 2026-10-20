"""Adaptive sampling for a kriging surrogate: max-MSE and LOO-CV infill against LHS.

The test function on [0, 1]^2 is a smooth wave plus a narrow Gaussian peak near
(0.8, 0.75), a stand-in for a response with a local feature such as the onset of
separation in one corner of a design space. Each run starts from an 8-point
maximin Latin hypercube and adds one point at a time up to 40 points, choosing
the candidate (on a 31 x 31 grid) that maximizes either the kriging MSE
(exploration only) or the product of a leave-one-out cross-validation error
indicator and the kriging standard deviation. One-shot maximin Latin hypercubes
of the same sizes are the reference. The figure shows the three final 40-point
designs and the normalized RMS error against the number of samples, averaged
over several random initial designs.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular
from scipy.optimize import minimize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_INITIAL = 8  # initial maximin LHS size (4 d)
N_FINAL = 40  # total budget of samples (20 d)
N_SEEDS = 5  # random initial designs averaged in the error curves
N_CANDIDATES_1D = 31  # candidate grid for the infill search is 31 x 31
N_TEST_1D = 50  # test grid for the error is 50 x 50
LHS_TRIES = 20  # random LHS drawn per maximin LHS
LOG10_THETA_BOUNDS = (-2.0, 3.0)  # search range of log10(theta_k)
NUGGET = 1e-8  # diagonal regularization of R for round-off
PEAK_CENTRE = (0.8, 0.75)  # location of the local feature
PEAK_WIDTH2 = 0.01  # squared width of the local feature
SEED = 0


def test_function(x):
    """Smooth wave plus a narrow Gaussian peak; x has shape (n, 2)."""
    x1, x2 = x[:, 0], x[:, 1]
    peak = np.exp(
        -((x1 - PEAK_CENTRE[0]) ** 2 + (x2 - PEAK_CENTRE[1]) ** 2) / PEAK_WIDTH2
    )
    return peak + 0.2 * np.sin(2.0 * np.pi * x1) * np.cos(np.pi * x2)


def latin_hypercube(n, d, rng):
    """Random LHS: one point in each of the n intervals of every coordinate."""
    ranks = np.argsort(rng.uniform(size=(d, n)), axis=1).T
    return (ranks + rng.uniform(size=(n, d))) / n


def min_distance(x):
    diff = np.sqrt(np.sum((x[:, None, :] - x[None, :, :]) ** 2, axis=-1))
    return diff[np.triu_indices(len(x), k=1)].min()


def maximin_lhs(n, d, rng, tries=LHS_TRIES):
    """Best of several random LHS by the maximin (largest minimum distance) rule."""
    designs = [latin_hypercube(n, d, rng) for _ in range(tries)]
    return max(designs, key=min_distance)


def gaussian_correlation(a, b, theta):
    """R_ij = exp(-sum_k theta_k (a_ik - b_jk)^2)."""
    return np.exp(-np.sum(theta * (a[:, None, :] - b[None, :, :]) ** 2, axis=-1))


class OrdinaryKriging:
    """Ordinary kriging with an anisotropic Gaussian correlation.

    The correlation parameters theta_k are fitted by maximizing the concentrated
    log-likelihood -(n/2) ln sigma^2 - (1/2) ln det R unless they are given.
    """

    def __init__(self, x, y, theta=None, theta_start=None):
        self.x, self.y = np.asarray(x), np.asarray(y)
        # squared coordinate differences, shape (n, n, d), reused for every theta
        self.sq_diff = (self.x[:, None, :] - self.x[None, :, :]) ** 2
        if theta is None:
            self.theta = self.fit_theta(theta_start)
        else:
            self.theta = np.asarray(theta)
        self._factorize(self.theta)

    def _factorize(self, theta):
        n = len(self.y)
        corr = np.exp(-self.sq_diff @ theta) + NUGGET * np.eye(n)
        self.chol = cho_factor(corr, lower=True, check_finite=False)
        self.r_inv_1 = self._solve(np.ones(n))
        self.beta = self.r_inv_1 @ self.y / self.r_inv_1.sum()
        self.weights = self._solve(self.y - self.beta)
        self.sigma2 = (self.y - self.beta) @ self.weights / n
        self.log_det = 2.0 * np.sum(np.log(np.diag(self.chol[0])))

    def _solve(self, b):
        return cho_solve(self.chol, b, check_finite=False)

    def negative_log_likelihood(self, log10_theta):
        try:
            self._factorize(10.0**log10_theta)
        except (np.linalg.LinAlgError, ValueError):
            return 1e10
        n = len(self.y)
        return 0.5 * n * np.log(max(self.sigma2, 1e-300)) + 0.5 * self.log_det

    def fit_theta(self, theta_start=None):
        """L-BFGS-B in log10(theta) from several starts; the best one wins."""
        d = self.x.shape[1]
        starts = [np.full(d, s) for s in (-0.5, 0.5, 1.5)]
        if theta_start is not None:
            starts = [np.log10(theta_start), np.full(d, 0.5)]
        best = None
        for start in starts:
            result = minimize(
                self.negative_log_likelihood,
                start,
                bounds=[LOG10_THETA_BOUNDS] * d,
                method="L-BFGS-B",
            )
            if best is None or result.fun < best.fun:
                best = result
        return 10.0**best.x

    def predict(self, x_new, return_mse=False):
        r = gaussian_correlation(x_new, self.x, self.theta)
        y_hat = self.beta + r @ self.weights
        if not return_mse:
            return y_hat
        v = solve_triangular(self.chol[0], r.T, lower=True)
        u = 1.0 - self.r_inv_1 @ r.T
        mse = self.sigma2 * (1.0 - np.sum(v**2, axis=0) + u**2 / self.r_inv_1.sum())
        return y_hat, np.maximum(mse, 0.0)


def loo_error_indicator(model, candidates, y_hat):
    """e(x) = (1/N) sum_i |y_hat_{-i}(x) - y_hat(x)| with theta held fixed."""
    n = len(model.y)
    total = np.zeros(len(candidates))
    for i in range(n):
        keep = np.arange(n) != i
        reduced = OrdinaryKriging(model.x[keep], model.y[keep], theta=model.theta)
        total += np.abs(reduced.predict(candidates) - y_hat)
    return total / n


def infill_score(model, candidates, method):
    """Criterion maximized by the next sample: MSE, or e(x) times sqrt(MSE)."""
    y_hat, mse = model.predict(candidates, return_mse=True)
    if method == "max_mse":
        return mse
    return loo_error_indicator(model, candidates, y_hat) * np.sqrt(mse)


def normalized_rmse(model, test_points, test_values):
    err = model.predict(test_points) - test_values
    return np.sqrt(np.mean(err**2)) / np.std(test_values)


def grid(n_1d):
    g = np.linspace(0.0, 1.0, n_1d)
    gx, gy = np.meshgrid(g, g)
    return np.column_stack([gx.ravel(), gy.ravel()])


def adaptive_run(method, rng, candidates, test_points, test_values):
    """Sequential design from N_INITIAL to N_FINAL samples; returns errors, x."""
    x = maximin_lhs(N_INITIAL, 2, rng)
    y = test_function(x)
    errors = []
    theta = None
    while True:
        model = OrdinaryKriging(x, y, theta_start=theta)
        theta = model.theta
        errors.append(normalized_rmse(model, test_points, test_values))
        if len(y) >= N_FINAL:
            return np.array(errors), x
        x_new = candidates[np.argmax(infill_score(model, candidates, method))]
        x = np.vstack([x, x_new])
        y = np.append(y, test_function(x_new[None, :]))


def one_shot_run(rng, sizes, test_points, test_values):
    """Errors of independent maximin LHS designs of each size; returns errors, x."""
    errors = []
    for n in sizes:
        x = maximin_lhs(n, 2, rng)
        model = OrdinaryKriging(x, test_function(x))
        errors.append(normalized_rmse(model, test_points, test_values))
    return np.array(errors), x


def run_study(seed=SEED, n_seeds=N_SEEDS):
    candidates = grid(N_CANDIDATES_1D)
    test_points = grid(N_TEST_1D)
    test_values = test_function(test_points)
    sizes = np.arange(N_INITIAL, N_FINAL + 1)
    errors = {"max_mse": [], "loo_cv": [], "lhs": []}
    designs = {}
    for k in range(n_seeds):
        for method in ("max_mse", "loo_cv"):
            rng = np.random.default_rng([seed, k])
            err, x = adaptive_run(method, rng, candidates, test_points, test_values)
            errors[method].append(err)
            designs.setdefault(method, x)
        err, x = one_shot_run(
            np.random.default_rng([seed, k, 1]), sizes, test_points, test_values
        )
        errors["lhs"].append(err)
        designs.setdefault("lhs", x)
    return sizes, {m: np.array(e) for m, e in errors.items()}, designs


LABELS = {
    "max_mse": "max MSE",
    "loo_cv": r"max LOO-CV error $\times$ $\hat{s}$",
    "lhs": "one-shot maximin LHS",
}
COLOURS = {"max_mse": "tab:orange", "loo_cv": "tab:blue", "lhs": "tab:gray"}


def make_figure(sizes, errors, designs):
    fig = plt.figure(figsize=(13, 9.5), layout="constrained")
    grid_spec = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.9])
    design_axes = [fig.add_subplot(grid_spec[0, k]) for k in range(3)]
    g = np.linspace(0.0, 1.0, 101)
    gx, gy = np.meshgrid(g, g)
    field = test_function(np.column_stack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
    for ax, method in zip(design_axes, ("max_mse", "loo_cv", "lhs")):
        cs = ax.contourf(gx, gy, field, levels=20, cmap="viridis")
        x = designs[method]
        if method == "lhs":
            ax.plot(*x.T, "wo", mec="k", ms=7)
        else:
            ax.plot(*x[:N_INITIAL].T, "ws", mec="k", ms=8, label="initial LHS")
            ax.plot(
                *x[N_INITIAL:].T, "o", color="tab:red", mec="k", ms=7, label="added"
            )
            ax.legend(loc="lower left", fontsize=10, framealpha=0.9)
        ax.set_aspect("equal")
        ax.set_xlabel("$x_1$ [-]")
        ax.set_ylabel("$x_2$ [-]")
        ax.set_title(f"{LABELS[method]}, N = {len(x)}", fontsize=11)
    fig.colorbar(cs, ax=design_axes, shrink=0.8, label="$y(x)$ [-]")

    ax = fig.add_subplot(grid_spec[1, :])
    for method, err in errors.items():
        ax.semilogy(
            sizes,
            err.mean(axis=0),
            "o-",
            ms=4,
            color=COLOURS[method],
            lw=2,
            label=LABELS[method],
        )
    ax.set_xlabel("number of samples N [-]")
    ax.set_ylabel("mean RMS error / std(y) [-]")
    ax.set_title(f"Surrogate error, mean over {err.shape[0]} initial designs")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=10)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    sizes, errors, designs = run_study()
    print("N    max MSE   LOO-CV x s   maximin LHS   (mean normalized RMSE)")
    for n in (8, 16, 24, 32, 40):
        k = n - N_INITIAL
        print(
            f"{n:2d}   {errors['max_mse'][:, k].mean():7.3f}   "
            f"{errors['loo_cv'][:, k].mean():10.3f}   {errors['lhs'][:, k].mean():11.3f}"
        )
    fig = make_figure(sizes, errors, designs)
    finish_figures(
        {"adaptive_sampling_kriging.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
