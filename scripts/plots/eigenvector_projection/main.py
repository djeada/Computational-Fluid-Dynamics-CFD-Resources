"""Find the principal directions of correlated two-point velocity fluctuations.

The synthetic fluctuations u'_a and u'_b of the two-point POD example (a
large-scale motion shared by both probes plus a local motion at each probe)
are arranged as a 2 x M matrix, and the eigenvectors of the 2 x 2 sample
covariance matrix are computed. This is the two-point Proper Orthogonal
Decomposition (POD). Two figures are produced: the data cloud with the
eigenvectors drawn as arrows, and the data projected onto each eigenvector.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Same signal model and seed as longitudinal_velocity_fluctuations_and_projections.
SEED = 0
N_SAMPLES = 10_000  # number of samples M
DT = 1.0e-3  # sampling interval [s]
TAU_SHARED = 10.0e-3  # correlation time of the shared large-scale motion [s]
TAU_LOCAL = 2.0e-3  # correlation time of the local small-scale motion [s]
VAR_SHARED = 2.8  # variance of the shared motion [m^2/s^2]
VAR_LOCAL = 2.2  # variance of the local motion at each probe [m^2/s^2]
MODE_COLORS = ("tab:red", "tab:green")


def ar1_process(n, dt, tau, variance, rng):
    """Stationary first-order autoregressive signal with correlation time tau."""
    r = np.exp(-dt / tau)
    kicks = rng.standard_normal(n) * np.sqrt(variance * (1.0 - r**2))
    signal = np.empty(n)
    signal[0] = rng.standard_normal() * np.sqrt(variance)
    for i in range(1, n):
        signal[i] = r * signal[i - 1] + kicks[i]
    return signal


def generate_fluctuations(n=N_SAMPLES, dt=DT, seed=SEED):
    """Return the 2 x n matrix of zero-mean fluctuations [u'_a; u'_b]."""
    rng = np.random.default_rng(seed)
    shared = ar1_process(n, dt, TAU_SHARED, VAR_SHARED, rng)
    local_a = ar1_process(n, dt, TAU_LOCAL, VAR_LOCAL, rng)
    local_b = ar1_process(n, dt, TAU_LOCAL, VAR_LOCAL, rng)
    data = np.vstack((shared + local_a, shared + local_b))
    return data - data.mean(axis=1, keepdims=True)


def principal_directions(data):
    """Return C, its eigenvalues (descending) and unit eigenvectors (columns).

    The sign of each eigenvector is fixed so that its first nonzero component
    is positive.
    """
    cov = data @ data.T / (data.shape[1] - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)  # symmetric matrix
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    eigenvectors *= np.where(eigenvectors[0] < 0, -1.0, 1.0)
    return cov, eigenvalues, eigenvectors


def draw_eigenvectors(ax, eigenvalues, eigenvectors):
    """Draw each eigenvector as an arrow of length 2 sqrt(eigenvalue)."""
    for k, color in enumerate(MODE_COLORS):
        vec = 2.0 * eigenvectors[:, k] * np.sqrt(eigenvalues[k])
        ax.quiver(
            0,
            0,
            vec[0],
            vec[1],
            angles="xy",
            scale_units="xy",
            scale=1,
            color=color,
            edgecolor="black",
            linewidth=0.8,
            width=0.008,
            zorder=4,
            label=(
                rf"$\phi_{k + 1}$ = ({eigenvectors[0, k]:.3f}, "
                rf"{eigenvectors[1, k]:.3f}), $\lambda_{k + 1}$ = "
                rf"{eigenvalues[k]:.2f} m$^2$/s$^2$"
            ),
        )


def format_axes(ax, title):
    ax.set_xlabel(r"$u'_a$ [m/s]")
    ax.set_ylabel(r"$u'_b$ [m/s]")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)


def plot_raw_data_with_eigenvectors(data, eigenvalues, eigenvectors):
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.scatter(data[0], data[1], s=4, alpha=0.25, color="tab:blue", label="samples")
    draw_eigenvectors(ax, eigenvalues, eigenvectors)
    format_axes(
        ax, r"Eigenvectors of $\mathbf{C}$ (arrows of length $2\sqrt{\lambda}$)"
    )
    return fig


def plot_projections_on_eigenvectors(data, eigenvalues, eigenvectors):
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.scatter(data[0], data[1], s=4, alpha=0.15, color="tab:blue", label="samples")
    for k, color in enumerate(MODE_COLORS):
        ev = eigenvectors[:, k]
        coeff = ev @ data  # scalar projections a_kj = phi_k . u'_j
        points = np.outer(ev, coeff)  # projected points a_kj phi_k in the plane
        ax.scatter(
            points[0],
            points[1],
            s=5,
            alpha=0.6,
            color=color,
            zorder=3,
            label=rf"$a_{k + 1}\phi_{k + 1}$ (variance {coeff.var(ddof=1):.2f})",
        )
    draw_eigenvectors(ax, eigenvalues, eigenvectors)
    format_axes(ax, "Samples projected on the two POD modes")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    data = generate_fluctuations()
    cov, eigenvalues, eigenvectors = principal_directions(data)
    print("Covariance matrix C (m^2/s^2):")
    print(np.array2string(cov, precision=3))
    fractions = eigenvalues / eigenvalues.sum()
    for k in range(2):
        angle = np.degrees(np.arctan2(eigenvectors[1, k], eigenvectors[0, k]))
        print(
            f"lambda_{k + 1} = {eigenvalues[k]:.3f} m^2/s^2 ({100 * fractions[k]:.1f} %),"
            f" phi_{k + 1} = {np.array2string(eigenvectors[:, k], precision=3)},"
            f" angle = {angle:.1f} deg"
        )

    figures = {
        "eigenvector_projection_raw.png": plot_raw_data_with_eigenvectors(
            data, eigenvalues, eigenvectors
        ),
        "eigenvector_projection_projections.png": plot_projections_on_eigenvectors(
            data, eigenvalues, eigenvectors
        ),
    }

    finish_figures(
        figures,
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
