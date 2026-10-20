"""How fast linear subspaces approximate three parametrized solution families.

Each family u(x; mu), mu in [0, 1], is sampled at 400 parameter values on 2000
points in x in [0, 1] m: a diffusing pulse whose width changes with mu (smooth
parameter dependence, as in diffusion-dominated problems), a pulse of fixed
width that translates with mu, and a translating step (a shock). The figure
plots example members, the normalized singular values of each snapshot matrix
and the worst-case relative error of projecting the samples onto the best
N-dimensional POD subspace, which is an estimate of the Kolmogorov n-width of
the sampled set. The first family decays exponentially, the second only after
N exceeds the number of pulse widths in the travel distance, and the step
algebraically, like N^(-1/2).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_X = 2000  # grid points in x (m)
N_MU = 400  # parameter samples
N_MAX = 100  # largest subspace dimension shown
SHIFT_START, SHIFT_TRAVEL = 0.2, 0.6  # position x0(mu) = 0.2 + 0.6 mu (m)
PULSE_WIDTH = 0.05  # width of the translating pulse (m)
VARIANCE_MIN, VARIANCE_RANGE = 0.002, 0.05  # variance of the diffusing pulse (m^2)
EXAMPLE_MU = (0.0, 0.25, 0.5, 0.75, 1.0)


def diffusing_pulse(x, mu):
    """Centred Gaussian whose variance grows linearly with mu."""
    variance = VARIANCE_MIN + VARIANCE_RANGE * mu
    return np.exp(-((x - 0.5) ** 2) / (2.0 * variance))


def translating_pulse(x, mu):
    """Gaussian of fixed width centred at x0(mu)."""
    return np.exp(-(((x - SHIFT_START - SHIFT_TRAVEL * mu) / PULSE_WIDTH) ** 2))


def translating_step(x, mu):
    """Unit step at x0(mu)."""
    return (x < SHIFT_START + SHIFT_TRAVEL * mu).astype(float)


FAMILIES = {
    "diffusing pulse": diffusing_pulse,
    "translating pulse": translating_pulse,
    "translating step": translating_step,
}


def snapshot_matrix(family, x, mus):
    """Columns u(x; mu_j)."""
    return np.column_stack([family(x, mu) for mu in mus])


def projection_errors(snapshots, n_max):
    """Worst-case relative error of projecting each column onto the first N modes.

    Uses the uncentred SVD, so the subspace contains no mean field. Every
    column lies in the span of all left singular vectors, so its squared error
    for N modes is the sum of its squared coefficients beyond N; summing the
    tail avoids the cancellation of subtracting the captured from the total.
    """
    modes, singular_values, _ = np.linalg.svd(snapshots, full_matrices=False)
    coefficients = modes.T @ snapshots
    total = np.sum(coefficients**2, axis=0)
    tail = np.cumsum(coefficients[::-1] ** 2, axis=0)[::-1]  # sum over k >= index
    residual = np.sqrt(tail[1 : n_max + 1] / total)
    return singular_values, residual.max(axis=1)


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    x = np.linspace(0.0, 1.0, N_X)
    mus = np.linspace(0.0, 1.0, N_MU)
    results = {
        name: projection_errors(snapshot_matrix(f, x, mus), N_MAX)
        for name, f in FAMILIES.items()
    }
    n = np.arange(1, N_MAX + 1)
    for name, (sigma, worst) in results.items():
        print(
            f"{name:18s}  sigma_10/sigma_1 = {sigma[9] / sigma[0]:.2e}  "
            f"worst error N = 5: {worst[4]:.3f}, N = 20: {worst[19]:.2e}, "
            f"N = 100: {worst[99]:.2e}"
        )

    fig = plt.figure(figsize=(13, 8), constrained_layout=True)
    grid = fig.add_gridspec(2, 6)
    colors = plt.cm.viridis(np.linspace(0.0, 0.9, len(EXAMPLE_MU)))
    for k, (name, family) in enumerate(FAMILIES.items()):
        ax = fig.add_subplot(grid[0, 2 * k : 2 * k + 2])
        for mu, color in zip(EXAMPLE_MU, colors, strict=True):
            ax.plot(x, family(x, mu), color=color, label=rf"$\mu$ = {mu}")
        ax.set(xlabel="x [m]", ylabel="u [-]", title=f"({'abc'[k]}) {name}")
        if k == 0:
            ax.legend(fontsize=9, loc="upper right")

    line_colors = dict(zip(FAMILIES, plt.cm.tab10.colors[:3], strict=True))
    ax = fig.add_subplot(grid[1, :3])
    for name, (sigma, _) in results.items():
        ax.semilogy(n, sigma[:N_MAX] / sigma[0], color=line_colors[name], label=name)
    ax.set(
        ylim=(1e-12, 2),
        xlabel="index k [-]",
        ylabel=r"$\sigma_k / \sigma_1$ [-]",
        title="(d) Singular values of the snapshot matrix",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=10)

    ax = fig.add_subplot(grid[1, 3:])
    for name, (_, worst) in results.items():
        ax.loglog(n, worst, color=line_colors[name], label=name)
    reference = results["translating step"][1][9] * np.sqrt(10.0 / n)
    ax.loglog(n, reference, "k:", label=r"slope $N^{-1/2}$")
    ax.set(
        ylim=(1e-10, 2),
        xlabel="subspace dimension N [-]",
        ylabel=r"$\max_\mu \|u - P_N u\| / \|u\|$ [-]",
        title="(e) Worst-case projection error (n-width estimate)",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=10, loc="lower left")
    finish_figures(
        {"rom_n_width_decay.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
