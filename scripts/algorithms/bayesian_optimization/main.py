"""Bayesian optimization with a Gaussian-process surrogate and expected improvement.

Minimizes a one-dimensional drag-like test function (a scaled Forrester
function) and the two-dimensional Branin function. The Gaussian process uses a
squared-exponential kernel whose length scales and amplitude are fitted by
maximizing the log marginal likelihood. Each new sample maximizes the expected
improvement. The figure shows the surrogate and acquisition function after
several iterations and compares the best value found with random search over
several seeds.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 1
NUGGET = 1e-6  # noise variance added to the standardized kernel diagonal
LOG_LENGTH_BOUNDS = (np.log(0.02), np.log(2.0))  # length scale in unit-cube units
LOG_AMPLITUDE_BOUNDS = (np.log(0.1), np.log(10.0))  # sigma_f of standardized data
N_RESTARTS = 3  # likelihood optimizer starts

N_INITIAL_1D, BUDGET_1D = 3, 15  # initial design size, total evaluations
N_INITIAL_2D, BUDGET_2D = 5, 30
N_SEEDS = 10  # repetitions for the convergence comparison
SNAPSHOT_ITERATIONS = (0, 2, 5)  # BO iterations drawn in the top rows
GRID_1D = 1001  # candidate points for maximizing EI in 1D
GRID_2D = 101  # candidate points per direction in 2D


def drag_like_1d(x):
    """C_D-like objective on [0, 1]: 0.30 + 0.005 (6x - 2)^2 sin(12x - 4).

    Global minimum 0.26990 at x = 0.75725, local minimum 0.29507 at x = 0.14259.
    """
    x = np.asarray(x)[..., 0]
    return 0.30 + 0.005 * (6 * x - 2) ** 2 * np.sin(12 * x - 4)


DRAG_1D_MIN = 0.30 + 0.005 * (-6.020740)  # Forrester minimum, f(0.75725)


def branin_2d(x):
    """Branin function mapped to [0, 1]^2; global minimum 0.397887 (three points)."""
    x = np.asarray(x)
    x1 = 15 * x[..., 0] - 5
    x2 = 15 * x[..., 1]
    b, c = 5.1 / (4 * np.pi**2), 5 / np.pi
    return (
        (x2 - b * x1**2 + c * x1 - 6) ** 2
        + 10 * (1 - 1 / (8 * np.pi)) * np.cos(x1)
        + 10
    )


BRANIN_MIN = 0.397887


def se_kernel(a, b, lengths, amplitude):
    """k(a, b) = sigma_f^2 exp(-0.5 sum_j ((a_j - b_j) / l_j)^2)."""
    diff = (a[:, None, :] - b[None, :, :]) / lengths
    return amplitude**2 * np.exp(-0.5 * np.sum(diff**2, axis=-1))


class GaussianProcess:
    """Zero-mean GP on standardized outputs with an ARD squared-exponential kernel."""

    def __init__(self, lengths, amplitude, nugget=NUGGET):
        self.lengths = np.atleast_1d(np.asarray(lengths, dtype=float))
        self.amplitude = float(amplitude)
        self.nugget = nugget

    def fit(self, x, y):
        self.x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        self.y_mean = y.mean()
        self.y_std = y.std() if y.std() > 0 else 1.0
        z = (y - self.y_mean) / self.y_std
        k = se_kernel(self.x, self.x, self.lengths, self.amplitude)
        k[np.diag_indices_from(k)] += self.nugget
        self.chol = np.linalg.cholesky(k)
        self.alpha = np.linalg.solve(self.chol.T, np.linalg.solve(self.chol, z))
        self.z = z
        return self

    def predict(self, x_new):
        """Posterior mean and standard deviation in the original units."""
        k_star = se_kernel(
            np.asarray(x_new, dtype=float), self.x, self.lengths, self.amplitude
        )
        mean = k_star @ self.alpha
        v = np.linalg.solve(self.chol, k_star.T)
        var = np.maximum(self.amplitude**2 - np.sum(v**2, axis=0), 1e-12)
        return self.y_mean + self.y_std * mean, self.y_std * np.sqrt(var)

    def log_marginal_likelihood(self):
        """log p(z | X) = -z^T K^-1 z / 2 - log|K| / 2 - n log(2 pi) / 2."""
        n = self.z.size
        return float(
            -0.5 * self.z @ self.alpha
            - np.sum(np.log(np.diag(self.chol)))
            - 0.5 * n * np.log(2 * np.pi)
        )

    def log_marginal_likelihood_gradient(self):
        """d log p / d theta for theta = (log l_1, ..., log l_d, log sigma_f).

        Uses d log p / d theta_j = tr((alpha alpha^T - K^-1) dK/d theta_j) / 2.
        """
        k_inv = np.linalg.solve(
            self.chol.T, np.linalg.solve(self.chol, np.eye(self.z.size))
        )
        inner = np.outer(self.alpha, self.alpha) - k_inv
        k_f = se_kernel(self.x, self.x, self.lengths, self.amplitude)
        grads = []
        for j, length in enumerate(self.lengths):
            sq = (self.x[:, None, j] - self.x[None, :, j]) ** 2 / length**2
            grads.append(0.5 * np.sum(inner * k_f * sq))
        grads.append(0.5 * np.sum(inner * 2 * k_f))
        return np.array(grads)


def fit_gp(x, y, rng, n_restarts=N_RESTARTS):
    """Fit length scales and amplitude by maximizing the log marginal likelihood."""
    x = np.asarray(x, dtype=float)
    dim = x.shape[1]
    bounds = [LOG_LENGTH_BOUNDS] * dim + [LOG_AMPLITUDE_BOUNDS]

    def negative_lml(theta):
        try:
            gp = GaussianProcess(np.exp(theta[:dim]), np.exp(theta[dim])).fit(x, y)
        except np.linalg.LinAlgError:
            return 1e10, np.zeros_like(theta)
        return -gp.log_marginal_likelihood(), -gp.log_marginal_likelihood_gradient()

    starts = [np.r_[np.full(dim, np.log(0.2)), 0.0]]
    starts += [
        np.array([rng.uniform(lo, hi) for lo, hi in bounds])
        for _ in range(n_restarts - 1)
    ]
    best = min(
        (
            minimize(negative_lml, s, jac=True, method="L-BFGS-B", bounds=bounds)
            for s in starts
        ),
        key=lambda res: res.fun,
    )
    return GaussianProcess(np.exp(best.x[:dim]), np.exp(best.x[dim])).fit(x, y)


def expected_improvement(mean, std, f_best, xi=0.0):
    """EI for minimization: (f_best - mu - xi) Phi(z) + sigma phi(z)."""
    std = np.maximum(std, 1e-12)
    improvement = f_best - mean - xi
    z = improvement / std
    return improvement * norm.cdf(z) + std * norm.pdf(z)


def latin_hypercube(n, dim, rng):
    """One point in each of n equal-probability strata per dimension."""
    strata = np.stack([rng.permutation(n) for _ in range(dim)], axis=1)
    return (strata + rng.uniform(size=(n, dim))) / n


def candidate_grid(dim):
    """Dense grid of candidates on which EI is maximized."""
    if dim == 1:
        return np.linspace(0, 1, GRID_1D)[:, None]
    g = np.linspace(0, 1, GRID_2D)
    return np.stack(np.meshgrid(g, g), axis=-1).reshape(-1, 2)


def bayesian_optimization(objective, dim, n_initial, budget, rng, record=False):
    """Run the EGO loop: fit GP, maximize EI on the candidate grid, evaluate."""
    x = latin_hypercube(n_initial, dim, rng)
    y = objective(x)
    candidates = candidate_grid(dim)
    history = []
    while y.size < budget:
        gp = fit_gp(x, y, rng)
        mean, std = gp.predict(candidates)
        ei = expected_improvement(mean, std, y.min())
        x_next = candidates[np.argmax(ei)]
        if record:
            history.append(
                {
                    "x": x.copy(),
                    "y": y.copy(),
                    "mean": mean,
                    "std": std,
                    "ei": ei,
                    "next": x_next,
                }
            )
        x = np.vstack([x, x_next])
        y = np.append(y, objective(x_next[None, :]))
    return x, y, history


def random_search(objective, dim, budget, rng):
    x = rng.uniform(size=(budget, dim))
    return x, objective(x)


def convergence(objective, dim, n_initial, budget, f_min, n_seeds=N_SEEDS):
    """Best-so-far gap f_best - f_min for BO and random search, one row per seed."""
    gaps_bo, gaps_rs = [], []
    for seed in range(n_seeds):
        rng = np.random.default_rng(1000 + seed)
        _, y_bo, _ = bayesian_optimization(objective, dim, n_initial, budget, rng)
        _, y_rs = random_search(objective, dim, budget, rng)
        gaps_bo.append(np.minimum.accumulate(y_bo) - f_min)
        gaps_rs.append(np.minimum.accumulate(y_rs) - f_min)
    return np.array(gaps_bo), np.array(gaps_rs)


def plot_results(history, conv_1d, conv_2d):
    fig = plt.figure(figsize=(13, 11), layout="constrained")
    top, bottom = fig.subfigures(2, 1, height_ratios=[1.6, 1])
    axs = top.subplots(2, len(SNAPSHOT_ITERATIONS), sharex=True, height_ratios=[2, 1])
    xs = candidate_grid(1)[:, 0]
    truth = drag_like_1d(xs[:, None])
    for col, it in enumerate(SNAPSHOT_ITERATIONS):
        h = history[it]
        ax = axs[0, col]
        ax.plot(xs, truth, "k--", lw=1.5, label="true objective")
        ax.plot(xs, h["mean"], color="tab:blue", lw=2, label="GP mean")
        ax.fill_between(
            xs,
            h["mean"] - 2 * h["std"],
            h["mean"] + 2 * h["std"],
            color="tab:blue",
            alpha=0.2,
            label=r"mean $\pm 2\sigma$",
        )
        ax.plot(h["x"][:, 0], h["y"], "o", color="tab:red", ms=7, label="samples")
        ax.axvline(h["next"][0], color="tab:green", ls=":", lw=2, label="next sample")
        ax.set_ylim(0.255, 0.36)
        ax.set_title(f"Iteration {it}: n = {h['y'].size} evaluations", fontsize=11)
        if col == 0:
            ax.set_ylabel(r"$C_D$-like objective $J(p)$")
            ax.legend(loc="upper left", fontsize=9)
        ax2 = axs[1, col]
        ax2.plot(xs, h["ei"], color="tab:purple", lw=2)
        ax2.fill_between(xs, 0, h["ei"], color="tab:purple", alpha=0.2)
        ax2.axvline(h["next"][0], color="tab:green", ls=":", lw=2)
        ax2.set_xlabel("design parameter p")
        if col == 0:
            ax2.set_ylabel("EI(p)")
        ax2.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))

    axs = bottom.subplots(1, 2)
    for ax, (bo, rs), title in zip(
        axs, (conv_1d, conv_2d), ("1D drag-like function", "2D Branin function")
    ):
        n = np.arange(1, bo.shape[1] + 1)
        for gaps, color, label in (
            (bo, "tab:blue", "Bayesian optimization (EI)"),
            (rs, "tab:orange", "random search"),
        ):
            gaps = np.maximum(gaps, 1e-8)
            q25, q50, q75 = np.percentile(gaps, [25, 50, 75], axis=0)
            ax.semilogy(n, q50, color=color, lw=2, label=f"{label}, median")
            ax.fill_between(n, q25, q75, color=color, alpha=0.2)
        ax.set_xlabel("number of objective evaluations")
        ax.set_ylabel(r"best-so-far gap $J_{best} - J^*$")
        ax.set_title(f"{title}, {bo.shape[0]} seeds (band: quartiles)", fontsize=11)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=10, loc="lower left")
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    rng = np.random.default_rng(SEED)
    x, y, history = bayesian_optimization(
        drag_like_1d, 1, N_INITIAL_1D, BUDGET_1D, rng, record=True
    )
    best = np.argmin(y)
    print(
        f"1D: best J = {y[best]:.5f} at p = {x[best, 0]:.4f} (true 0.26990 at 0.75725)"
    )
    conv_1d = convergence(drag_like_1d, 1, N_INITIAL_1D, BUDGET_1D, DRAG_1D_MIN)
    conv_2d = convergence(branin_2d, 2, N_INITIAL_2D, BUDGET_2D, BRANIN_MIN)
    for name, (bo, rs) in (("1D", conv_1d), ("2D", conv_2d)):
        print(
            f"{name}: median final gap BO {np.median(bo[:, -1]):.2e}, "
            f"random {np.median(rs[:, -1]):.2e}"
        )
    fig = plot_results(history, conv_1d, conv_2d)
    finish_figures(
        {"bayesian_optimization.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
