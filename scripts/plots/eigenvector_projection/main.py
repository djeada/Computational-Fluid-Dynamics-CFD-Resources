"""Find the principal directions of correlated 2D velocity fluctuations.

Synthetic fluctuations u'_a and u'_b are generated with a linear correlation,
their mean is removed, and the eigenvectors of the 2x2 sample covariance matrix
are computed. This is the two-point Proper Orthogonal Decomposition (POD). Two
figures are produced: the data cloud with the eigenvectors drawn as arrows, and
the data projected onto each eigenvector.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_SAMPLES = 1000
SIGMA = 2.0  # standard deviation of the Gaussian noise (m/s)
COUPLING = 0.7  # u'_b = COUPLING * u'_a + noise


def generate_fluctuations(n=N_SAMPLES, sigma=SIGMA, coupling=COUPLING, seed=SEED):
    """Return an (n, 2) array of zero-mean correlated fluctuations [u'_a, u'_b]."""
    rng = np.random.default_rng(seed)
    u_a = rng.normal(0.0, sigma, n)
    u_b = coupling * u_a + rng.normal(0.0, sigma, n)
    data = np.column_stack((u_a, u_b))
    return data - data.mean(axis=0)


def principal_directions(data):
    """Return eigenvalues (descending) and unit eigenvectors (columns) of cov(data)."""
    cov = np.cov(data, rowvar=False)  # 1/(m-1) normalisation
    eigenvalues, eigenvectors = np.linalg.eigh(cov)  # symmetric matrix
    order = np.argsort(eigenvalues)[::-1]
    return cov, eigenvalues[order], eigenvectors[:, order]


def draw_eigenvectors(ax, eigenvalues, eigenvectors):
    """Draw each eigenvector as an arrow of length sqrt(eigenvalue)."""
    for k, color in enumerate(("black", "gray")):
        vec = eigenvectors[:, k] * np.sqrt(eigenvalues[k])
        ax.quiver(
            0,
            0,
            vec[0],
            vec[1],
            angles="xy",
            scale_units="xy",
            scale=1,
            color=color,
            width=0.006,
            label=rf"EV {k + 1} ($\lambda_{k + 1}$ = {eigenvalues[k]:.2f} m$^2$/s$^2$)",
        )


def format_axes(ax, title):
    ax.set_xlabel(r"$u'_a\ (m/s)$")
    ax.set_ylabel(r"$u'_b\ (m/s)$")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend()
    ax.grid(True)


def plot_raw_data_with_eigenvectors(data, eigenvalues, eigenvectors):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(data[:, 0], data[:, 1], s=10, alpha=0.6, label="Data")
    draw_eigenvectors(ax, eigenvalues, eigenvectors)
    format_axes(
        ax, "Raw Data with Directions of Eigenvectors (EVs) of the Covariance Matrix"
    )
    return fig


def plot_projections_on_eigenvectors(data, eigenvalues, eigenvectors):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(data[:, 0], data[:, 1], s=10, alpha=0.3, label="Data")
    for k, color in enumerate(("red", "blue")):
        ev = eigenvectors[:, k]
        coeff = data @ ev  # scalar projections a_i = u'_i . e_k
        points = np.outer(coeff, ev)  # projected points a_i * e_k in the plane
        ax.scatter(
            points[:, 0],
            points[:, 1],
            s=10,
            alpha=0.6,
            color=color,
            label=f"Proj on EV{k + 1} (variance {coeff.var(ddof=1):.2f})",
        )
    draw_eigenvectors(ax, eigenvalues, eigenvectors)
    format_axes(
        ax, "Projection of Data Points on Eigenvectors of the Covariance Matrix"
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    data = generate_fluctuations()
    cov, eigenvalues, eigenvectors = principal_directions(data)
    print("Covariance matrix C (m^2/s^2):")
    print(np.array2string(cov, precision=3))
    for k in range(2):
        print(
            f"lambda_{k + 1} = {eigenvalues[k]:.3f}, "
            f"e_{k + 1} = {np.array2string(eigenvectors[:, k], precision=3)}"
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
