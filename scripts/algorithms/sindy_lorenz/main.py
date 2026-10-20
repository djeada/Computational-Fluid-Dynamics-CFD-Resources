"""Sparse identification of nonlinear dynamics (SINDy) on Lorenz-system data.

A Lorenz trajectory is integrated with scipy's solve_ivp, light measurement
noise is added, and time derivatives are estimated by central finite
differences. A library of the 20 monomials of degree up to three in (x, y, z)
is regressed onto the derivatives with sequential thresholded least squares
(STLSQ). The figure compares the identified coefficient matrix with the true
one and integrates the identified model from the same initial condition.
"""

import sys
from itertools import combinations_with_replacement
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0  # Lorenz parameters
X0 = (-8.0, 8.0, 27.0)  # initial condition
DT = 0.002  # sampling interval (time units)
T_TRAIN = 10.0  # length of the training record
T_TEST = 15.0  # length of the comparison run
NOISE_STD = 0.01  # standard deviation of measurement noise on x, y, z
POLY_ORDER = 3  # highest monomial degree in the library
THRESHOLD = 0.1  # STLSQ sparsity threshold lambda
VARIABLES = ("x", "y", "z")


def lorenz(_t, state, sigma=SIGMA, rho=RHO, beta=BETA):
    """Right-hand side of the Lorenz system."""
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def simulate(rhs, x0, t):
    """Integrate dx/dt = rhs(t, x) to the sample times t with tight tolerances."""
    solution = solve_ivp(
        rhs, (t[0], t[-1]), x0, t_eval=t, method="LSODA", rtol=1e-10, atol=1e-10
    )
    return solution.y.T


def library_exponents(n_vars=3, order=POLY_ORDER):
    """Exponent tuples of every monomial up to the given degree, constant first."""
    exponents = []
    for degree in range(order + 1):
        for combo in combinations_with_replacement(range(n_vars), degree):
            powers = [0] * n_vars
            for index in combo:
                powers[index] += 1
            exponents.append(tuple(powers))
    return exponents


def library_names(exponents, variables=VARIABLES):
    """Readable names such as 1, x, xy, z^2 for the library columns."""
    names = []
    for powers in exponents:
        parts = [
            v if p == 1 else f"{v}^{p}" for v, p in zip(variables, powers) if p > 0
        ]
        names.append("".join(parts) or "1")
    return names


def build_library(X, exponents):
    """Theta(X): one column per monomial evaluated on every sample (rows of X)."""
    return np.column_stack(
        [np.prod(X ** np.array(powers), axis=1) for powers in exponents]
    )


def central_difference(X, dt):
    """Fourth-order central differences in the interior, second order at the ends."""
    dX = np.gradient(X, dt, axis=0, edge_order=2)
    dX[2:-2] = (-X[4:] + 8 * X[3:-1] - 8 * X[1:-3] + X[:-4]) / (12 * dt)
    return dX


def stlsq(Theta, dX, threshold=THRESHOLD, max_iter=10):
    """Sequential thresholded least squares (Brunton, Proctor & Kutz 2016).

    Solves Theta Xi ~ dX, then repeatedly zeroes coefficients with magnitude
    below the threshold and refits the remaining ones, column by column.
    """
    Xi = np.linalg.lstsq(Theta, dX, rcond=None)[0]
    for _ in range(max_iter):
        small = np.abs(Xi) < threshold
        Xi[small] = 0.0
        for k in range(dX.shape[1]):
            big = ~small[:, k]
            if big.any():
                Xi[big, k] = np.linalg.lstsq(Theta[:, big], dX[:, k], rcond=None)[0]
        if np.array_equal(small, np.abs(Xi) < threshold):
            break
    return Xi


def true_coefficients(exponents):
    """Coefficient matrix of the Lorenz system in the monomial library."""
    Xi = np.zeros((len(exponents), 3))
    index = {powers: i for i, powers in enumerate(exponents)}
    Xi[index[(1, 0, 0)], 0] = -SIGMA
    Xi[index[(0, 1, 0)], 0] = SIGMA
    Xi[index[(1, 0, 0)], 1] = RHO
    Xi[index[(0, 1, 0)], 1] = -1.0
    Xi[index[(1, 0, 1)], 1] = -1.0
    Xi[index[(1, 1, 0)], 2] = 1.0
    Xi[index[(0, 0, 1)], 2] = -BETA
    return Xi


def identified_rhs(Xi, exponents):
    """Return f(t, state) = Theta(state) Xi for integration with solve_ivp."""

    def rhs(_t, state):
        return (build_library(np.atleast_2d(state), exponents) @ Xi)[0]

    return rhs


def fit_lorenz(noise_std=NOISE_STD, threshold=THRESHOLD, seed=SEED):
    """Generate noisy training data and fit SINDy; return (Xi, exponents)."""
    t = np.arange(0.0, T_TRAIN, DT)
    X = simulate(lorenz, X0, t)
    rng = np.random.default_rng(seed)
    X_noisy = X + noise_std * rng.standard_normal(X.shape)
    dX = central_difference(X_noisy, DT)
    exponents = library_exponents()
    Theta = build_library(X_noisy, exponents)
    return stlsq(Theta, dX, threshold), exponents


def plot_coefficients(ax, Xi, names, title):
    limit = 30.0
    image = ax.imshow(Xi, cmap="RdBu_r", vmin=-limit, vmax=limit, aspect="auto")
    for (i, k), value in np.ndenumerate(Xi):
        if value != 0.0:
            colour = "w" if abs(value) > 0.6 * limit else "k"
            ax.text(
                k, i, f"{value:.3f}", ha="center", va="center", fontsize=9, c=colour
            )
    ax.set_xticks(range(3), [rf"$\dot {v}$" for v in VARIABLES])
    ax.set_yticks(range(len(names)), [f"${n}$" for n in names], fontsize=9)
    ax.set_xticks(np.arange(-0.5, 3), minor=True)
    ax.set_yticks(np.arange(-0.5, len(names)), minor=True)
    ax.grid(which="minor", color="0.85", linewidth=0.8)
    ax.tick_params(which="minor", length=0)
    ax.set_title(title)
    return image


def make_figure(Xi_true, Xi, exponents, t, X_true, X_model):
    names = library_names(exponents)
    fig = plt.figure(figsize=(13, 9.5))
    grid = fig.add_gridspec(
        2, 4, height_ratios=[1.35, 1], width_ratios=[1, 1, 1.2, 1.2]
    )

    ax = fig.add_subplot(grid[0, 0])
    plot_coefficients(ax, Xi_true, names, r"(a) True $\Xi$")
    ax = fig.add_subplot(grid[0, 1])
    image = plot_coefficients(ax, Xi, names, r"(b) Identified $\Xi$ (STLSQ)")
    fig.colorbar(image, ax=ax, fraction=0.08, label="coefficient")

    ax = fig.add_subplot(grid[0, 2:], projection="3d")
    ax.plot(*X_true.T, color="0.4", linewidth=0.6, label="true system")
    ax.plot(*X_model.T, color="tab:orange", linewidth=0.6, label="identified model")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_title("(c) Attractor from the same initial condition")
    ax.legend(fontsize=10, loc="upper left")

    colours = ("0.25", "tab:orange")
    for k, variable in enumerate(("x", "z")):
        ax = fig.add_subplot(grid[1, 2 * k : 2 * k + 2])
        column = VARIABLES.index(variable)
        ax.plot(t, X_true[:, column], color=colours[0], linewidth=1.5, label="true")
        ax.plot(
            t, X_model[:, column], "--", color=colours[1], linewidth=1.5, label="SINDy"
        )
        ax.set_xlabel("$t$")
        ax.set_ylabel(f"${variable}(t)$")
        ax.set_title(f"({'de'[k]}) ${variable}(t)$: true against identified model")
        ax.legend(fontsize=10, loc="upper left", ncol=2)
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def divergence_time(t, X_true, X_model, tolerance=1.0):
    """First time at which the two trajectories differ by more than tolerance."""
    distance = np.linalg.norm(X_true - X_model, axis=1)
    beyond = np.nonzero(distance > tolerance)[0]
    return t[beyond[0]] if beyond.size else np.inf


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    Xi, exponents = fit_lorenz()
    Xi_true = true_coefficients(exponents)
    t = np.arange(0.0, T_TEST, DT)
    X_true = simulate(lorenz, X0, t)
    X_model = simulate(identified_rhs(Xi, exponents), X0, t)

    names = library_names(exponents)
    print("identified model:")
    for k, variable in enumerate(VARIABLES):
        terms = [f"{Xi[i, k]:+.4f} {n}" for i, n in enumerate(names) if Xi[i, k]]
        print(f"  d{variable}/dt = {' '.join(terms)}")
    error = np.abs(Xi - Xi_true)[Xi_true != 0] / np.abs(Xi_true[Xi_true != 0])
    print(f"active terms: {np.count_nonzero(Xi)} (true: {np.count_nonzero(Xi_true)})")
    print(f"largest relative coefficient error: {error.max():.2e}")
    print(
        f"trajectories separate by > 1 at t = {divergence_time(t, X_true, X_model):.2f}"
    )

    fig = make_figure(Xi_true, Xi, exponents, t, X_true, X_model)
    finish_figures({"sindy_lorenz.png": fig}, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
