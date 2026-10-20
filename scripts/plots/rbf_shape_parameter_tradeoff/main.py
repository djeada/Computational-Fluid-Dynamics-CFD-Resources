"""Accuracy against conditioning in RBF interpolation as the shape parameter varies.

Interpolates Franke's 2D test function from 50 scrambled Halton points with the
Gaussian kernel exp(-(eps r)^2) and the multiquadric kernel sqrt(1 + (eps r)^2)
for 80 shape parameters eps between 0.3 and 30. For each eps it records the
true RMS error on a 60 x 60 test grid, the leave-one-out cross-validation
(LOOCV) error from Rippa's closed-form formula e_i = c_i / (A^-1)_ii, and the
2-norm condition number of the interpolation matrix A. The figure shows that
peaked kernels (large eps) give well-conditioned but inaccurate interpolants,
that flat kernels (small eps) drive the condition number past 1/machine epsilon
so round-off destroys the solution, and that the LOOCV curve follows the true
error and has its minimum near the best eps without using the true function.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_CENTRES = 50  # interpolation points in [0, 1]^2
N_GRID = 60  # test grid is N_GRID x N_GRID
EPS_MIN, EPS_MAX, N_EPS = 0.3, 30.0, 80  # shape-parameter sweep (log-spaced)
SEED = 3

KERNELS = {
    "Gaussian": lambda r, eps: np.exp(-((eps * r) ** 2)),
    "multiquadric": lambda r, eps: np.sqrt(1.0 + (eps * r) ** 2),
}


def franke(x, y):
    """Franke's (1979) bivariate test function on [0, 1]^2."""
    return (
        0.75 * np.exp(-((9 * x - 2) ** 2) / 4 - (9 * y - 2) ** 2 / 4)
        + 0.75 * np.exp(-((9 * x + 1) ** 2) / 49 - (9 * y + 1) / 10)
        + 0.5 * np.exp(-((9 * x - 7) ** 2) / 4 - (9 * y - 3) ** 2 / 4)
        - 0.2 * np.exp(-((9 * x - 4) ** 2) - (9 * y - 7) ** 2)
    )


def distance_matrix(a, b):
    """Euclidean distances between the rows of a and the rows of b."""
    return np.sqrt(np.sum((a[:, None, :] - b[None, :, :]) ** 2, axis=-1))


def rippa_loocv(a, y):
    """LOOCV residuals e_i = y_i - s^{(-i)}(x_i) = c_i / (A^-1)_ii (Rippa, 1999)."""
    a_inv = np.linalg.inv(a)
    return (a_inv @ y) / np.diag(a_inv)


def brute_force_loocv(a, y):
    """Same residuals by refitting the interpolant N times without point i."""
    n = len(y)
    errors = np.empty(n)
    for i in range(n):
        keep = np.arange(n) != i
        coeffs = np.linalg.solve(a[np.ix_(keep, keep)], y[keep])
        errors[i] = y[i] - a[i, keep] @ coeffs
    return errors


def sweep(centres, values, test_points, test_values, kernel, epsilons):
    """True RMS error, LOOCV RMS error and cond(A) for each eps."""
    r_cc = distance_matrix(centres, centres)
    r_tc = distance_matrix(test_points, centres)
    true_err, loocv_err, cond = [], [], []
    for eps in epsilons:
        a = kernel(r_cc, eps)
        coeffs = np.linalg.solve(a, values)
        s = kernel(r_tc, eps) @ coeffs
        true_err.append(np.sqrt(np.mean((s - test_values) ** 2)))
        loocv_err.append(np.sqrt(np.mean(rippa_loocv(a, values) ** 2)))
        cond.append(np.linalg.cond(a))
    return np.array(true_err), np.array(loocv_err), np.array(cond)


def make_data(seed=SEED):
    centres = qmc.Halton(d=2, scramble=True, seed=seed).random(N_CENTRES)
    g = np.linspace(0.0, 1.0, N_GRID)
    gx, gy = np.meshgrid(g, g)
    test_points = np.column_stack([gx.ravel(), gy.ravel()])
    return centres, franke(*centres.T), test_points, franke(*test_points.T), gx, gy


def make_figure(centres, gx, gy, epsilons, results):
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.6))
    ax = axs[0]
    cs = ax.contourf(gx, gy, franke(gx, gy), levels=20, cmap="viridis")
    fig.colorbar(cs, ax=ax, label="$f(x, y)$ [-]")
    ax.plot(*centres.T, "wo", mec="k", ms=6)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ [-]")
    ax.set_ylabel("$y$ [-]")
    ax.set_title(f"Franke function and {len(centres)} Halton points")

    colours = {"Gaussian": "tab:blue", "multiquadric": "tab:orange"}
    for name, (true_err, loocv_err, cond) in results.items():
        c = colours[name]
        axs[1].loglog(epsilons, true_err, "-", color=c, lw=2, label=f"{name}: true")
        axs[1].loglog(
            epsilons, loocv_err, "--", color=c, lw=1.5, label=f"{name}: LOOCV"
        )
        k = int(np.argmin(loocv_err))
        axs[1].plot(epsilons[k], loocv_err[k], "v", color=c, ms=9)
        axs[2].loglog(epsilons, cond, "-", color=c, lw=2, label=name)
    axs[1].set_xlabel(r"shape parameter $\varepsilon$ [-]")
    axs[1].set_ylabel("RMS error [-]")
    axs[1].set_title(r"Error vs $\varepsilon$ ($\triangledown$: LOOCV minimum)")
    axs[1].grid(True, which="both", alpha=0.3)
    axs[1].set_ylim(1e-4, 3e2)
    axs[1].legend(fontsize=10, loc="lower left")
    axs[2].axhline(1.0 / np.finfo(float).eps, color="k", ls=":", lw=1)
    axs[2].text(
        EPS_MAX,
        1.2 / np.finfo(float).eps,
        r"$1/\epsilon_{mach}$",
        ha="right",
        va="bottom",
        fontsize=10,
    )
    axs[2].set_xlabel(r"shape parameter $\varepsilon$ [-]")
    axs[2].set_ylabel(r"$\mathrm{cond}_2(A)$ [-]")
    axs[2].set_title("Condition number of the RBF matrix")
    axs[2].grid(True, which="both", alpha=0.3)
    axs[2].legend(fontsize=10)
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    centres, values, test_points, test_values, gx, gy = make_data()
    epsilons = np.logspace(np.log10(EPS_MIN), np.log10(EPS_MAX), N_EPS)
    results = {}
    for name, kernel in KERNELS.items():
        results[name] = sweep(
            centres, values, test_points, test_values, kernel, epsilons
        )
        true_err, loocv_err, cond = results[name]
        k_true, k_cv = int(np.argmin(true_err)), int(np.argmin(loocv_err))
        print(
            f"{name:12s}  best eps (true) = {epsilons[k_true]:6.3f}, "
            f"RMS = {true_err[k_true]:.2e}, cond = {cond[k_true]:.1e}"
        )
        print(
            f"{'':12s}  best eps (LOOCV) = {epsilons[k_cv]:5.3f}, "
            f"true RMS there = {true_err[k_cv]:.2e}"
        )
        print(
            f"{'':12s}  eps = {epsilons[-1]:.0f}: RMS = {true_err[-1]:.2e}, "
            f"cond = {cond[-1]:.1e}; eps = {epsilons[0]:.1f}: "
            f"RMS = {true_err[0]:.2e}, cond = {cond[0]:.1e}"
        )

    fig = make_figure(centres, gx, gy, epsilons, results)
    finish_figures(
        {"rbf_shape_parameter_tradeoff.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
