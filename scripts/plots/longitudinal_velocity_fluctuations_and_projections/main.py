"""Plot two-point velocity fluctuations and their projection onto a unit vector.

One synthetic, correlated data set of longitudinal velocity fluctuations
u'_a(t) and u'_b(t) is used for three figures, following the two-point POD
example: the time traces, the (u'_a, u'_b) scatter cloud, and the cloud
projected onto the unit vector phi = (2, 1)/sqrt(5).
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
T_START, T_END = 0.9, 1.1  # time window of the traces (s)
SIGMA = 2.0  # standard deviation of the Gaussian noise (m/s)
COUPLING = 0.5  # u'_b = COUPLING * u'_a + noise
PHI = np.array([2.0, 1.0]) / np.sqrt(5.0)  # unit vector (0.894, 0.447)


def generate_fluctuations(n=N_SAMPLES, sigma=SIGMA, coupling=COUPLING, seed=SEED):
    """Return time t and an (n, 2) array of zero-mean fluctuations [u'_a, u'_b]."""
    rng = np.random.default_rng(seed)
    t = np.linspace(T_START, T_END, n)
    u_a = rng.normal(0.0, sigma, n)
    u_b = coupling * u_a + rng.normal(0.0, sigma, n)
    data = np.column_stack((u_a, u_b))
    return t, data - data.mean(axis=0)


def project(data, phi):
    """Return scalar projections a_i = u'_i . phi and the projected points a_i phi."""
    coeff = data @ phi
    return coeff, np.outer(coeff, phi)


def plot_time_series(t, data):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(t, data[:, 0], label=r"$u'_a$", color="blue", linewidth=0.8)
    ax.plot(t, data[:, 1], label=r"$u'_b$", color="red", linewidth=0.8)
    ax.set_xlabel(r"$t\ (s)$")
    ax.set_ylabel(r"$u'\ (m/s)$")
    ax.set_title("Longitudinal velocity fluctuations $u'(t)$ at positions (a) and (b).")
    ax.legend()
    return fig


def plot_scatter(data):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(data[:, 0], data[:, 1], s=10, alpha=0.5)
    ax.set_xlabel(r"$u'_a\ (m/s)$")
    ax.set_ylabel(r"$u'_b\ (m/s)$")
    ax.set_title("Raw data plotted on a plane.")
    ax.set_aspect("equal", adjustable="datalim")
    return fig


def plot_projection(data, phi):
    coeff, points = project(data, phi)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(data[:, 0], data[:, 1], s=10, alpha=0.5, label="Data")
    ax.scatter(
        points[:, 0],
        points[:, 1],
        s=10,
        alpha=0.5,
        color="red",
        label=rf"Proj on $\Phi$ (variance {coeff.var(ddof=1):.2f} m$^2$/s$^2$)",
    )
    extent = np.abs(data).max()
    line = np.array([-extent, extent])
    ax.plot(
        line * phi[0],
        line * phi[1],
        color="black",
        label=rf"$\Phi=({phi[0]:.3f}, {phi[1]:.3f})$",
    )
    ax.set_xlabel(r"$u'_a\ (m/s)$")
    ax.set_ylabel(r"$u'_b\ (m/s)$")
    ax.set_title(r"Raw data projected on unit vector $\Phi$.")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t, data = generate_fluctuations()
    cov = np.cov(data, rowvar=False)
    coeff, _ = project(data, PHI)
    print("Covariance matrix C (m^2/s^2):")
    print(np.array2string(cov, precision=3))
    print(f"Correlation coefficient: {cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1]):.3f}")
    print(f"Variance along phi: {coeff.var(ddof=1):.3f} m^2/s^2")

    figures = {
        "velocity_fluctuations_time_series.png": plot_time_series(t, data),
        "velocity_fluctuations_scatter.png": plot_scatter(data),
        "velocity_fluctuations_projection.png": plot_projection(data, PHI),
    }

    finish_figures(
        figures,
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
