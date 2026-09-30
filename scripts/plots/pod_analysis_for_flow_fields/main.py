"""Eigenvalue spectrum and energy content of POD modes of a synthetic flow field.

A 100 x 50 snapshot matrix (100 time instants, 50 spatial points) is built
from three travelling waves of decreasing amplitude plus seeded Gaussian
noise. After removing the temporal mean, POD is performed with the singular
value decomposition, and the first ten eigenvalues are plotted together with
the percentage and cumulative percentage of turbulent kinetic energy (TKE)
captured by each mode.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

N_SAMPLES = 100  # number of snapshots M (rows of the snapshot matrix)
N_POINTS = 50  # number of spatial points N (columns)
# Travelling waves a * sin(k x - w t): (amplitude [m/s], wavenumber [1/m], angular frequency [1/s])
WAVES = [(1.0, 1, 2), (0.5, 2, 5), (0.25, 3, 9)]
MEAN_VELOCITY = 1.0  # uniform mean velocity added to every snapshot [m/s]
NOISE_STD = 0.3  # standard deviation of the random fluctuations [m/s]
SEED = 42  # random seed
N_PLOT = 10  # number of modes to plot


def generate_snapshots(
    n_samples=N_SAMPLES, n_points=N_POINTS, noise_std=NOISE_STD, seed=SEED
):
    """Return the snapshot matrix, shape (n_samples, n_points)."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 2.0 * np.pi, n_points, endpoint=False)
    t = np.linspace(0.0, 2.0 * np.pi, n_samples, endpoint=False)
    T, X = np.meshgrid(t, x, indexing="ij")
    data = np.full((n_samples, n_points), MEAN_VELOCITY)
    for amplitude, k, omega in WAVES:
        data += amplitude * np.sin(k * X - omega * T)
    data += noise_std * rng.standard_normal(data.shape)
    return data


def pod(data):
    """POD by SVD of the mean-subtracted snapshot matrix.

    Returns the eigenvalues lambda_i = sigma_i^2 / (M - 1), the spatial modes
    (rows) and the temporal coefficients (columns).
    """
    result = compute_pod(data.T)
    return result.eigenvalues, result.modes.T, result.coefficients.T


def plot_spectrum(eigenvalues, n_plot=N_PLOT):
    """Bar chart of eigenvalues with %TKE and cumulative %TKE on a twin axis."""
    n_plot = min(n_plot, len(eigenvalues))
    tke_percentage = 100.0 * eigenvalues / eigenvalues.sum()
    cumulative = np.cumsum(tke_percentage)
    modes = np.arange(1, n_plot + 1)

    fig, ax1 = plt.subplots()
    bars = ax1.bar(
        modes, eigenvalues[:n_plot], color="b", alpha=0.5, label=r"$\lambda_i$"
    )
    ax1.set_xlabel("Mode #")
    ax1.set_ylabel(r"$\lambda_i$", color="b")
    ax1.tick_params(axis="y", labelcolor="b")
    ax1.set_xticks(modes)

    ax2 = ax1.twinx()
    (line,) = ax2.plot(modes, tke_percentage[:n_plot], "o-", color="r", label="% TKE")
    (cum,) = ax2.plot(
        modes, cumulative[:n_plot], "s--", color="darkred", label="cumulative % TKE"
    )
    ax2.set_ylabel("% TKE", color="r")
    ax2.tick_params(axis="y", labelcolor="r")
    ax2.set_ylim(0, 105)

    ax1.legend(handles=[bars, line, cum], loc="center right")
    ax1.set_title("Eigenvalues and TKE Percentage from POD")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    data = generate_snapshots()
    eigenvalues, _, _ = pod(data)
    tke = 100.0 * eigenvalues / eigenvalues.sum()
    for i in range(min(N_PLOT, len(eigenvalues))):
        print(
            f"mode {i + 1:2d}: lambda = {eigenvalues[i]:.4f}, TKE = {tke[i]:5.2f} %, "
            f"cumulative = {tke[: i + 1].sum():6.2f} %"
        )

    fig = plot_spectrum(eigenvalues)

    finish_figures(
        {"pod_analysis_for_flow_fields.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
