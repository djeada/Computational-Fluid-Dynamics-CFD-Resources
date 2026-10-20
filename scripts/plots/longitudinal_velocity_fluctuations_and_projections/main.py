"""Plot two-point velocity fluctuations and their projection onto a unit vector.

One synthetic data set of longitudinal velocity fluctuations u'_a(t) and
u'_b(t) is used for three figures, following the two-point POD example: the
time traces, the (u'_a, u'_b) scatter cloud, and the cloud projected onto the
trial unit vector phi = (2, 1)/sqrt(5). Each signal is the sum of a large-scale
motion shared by both probes and a smaller, faster local motion, so the two
signals are correlated.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_SAMPLES = 10_000  # number of samples M
DT = 1.0e-3  # sampling interval [s]
TAU_SHARED = 10.0e-3  # correlation time of the shared large-scale motion [s]
TAU_LOCAL = 2.0e-3  # correlation time of the local small-scale motion [s]
VAR_SHARED = 2.8  # variance of the shared motion [m^2/s^2]
VAR_LOCAL = 2.2  # variance of the local motion at each probe [m^2/s^2]
PLOT_WINDOW = 0.25  # length of the plotted part of the time traces [s]
PHI = np.array([2.0, 1.0]) / np.sqrt(5.0)  # trial unit vector (0.894, 0.447)


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
    """Return time t and the 2 x n matrix of zero-mean fluctuations [u'_a; u'_b].

    Points are rows and snapshots are columns, as in scripts/_numerics.py.
    """
    rng = np.random.default_rng(seed)
    t = dt * np.arange(n)
    shared = ar1_process(n, dt, TAU_SHARED, VAR_SHARED, rng)
    local_a = ar1_process(n, dt, TAU_LOCAL, VAR_LOCAL, rng)
    local_b = ar1_process(n, dt, TAU_LOCAL, VAR_LOCAL, rng)
    data = np.vstack((shared + local_a, shared + local_b))
    return t, data - data.mean(axis=1, keepdims=True)


def covariance(data):
    """Sample covariance C = U U^T / (M - 1) of a 2 x M fluctuation matrix."""
    return data @ data.T / (data.shape[1] - 1)


def project(data, phi):
    """Return scalar projections a_j = phi . u'_j and the projected points a_j phi."""
    coeff = phi @ data
    return coeff, np.outer(phi, coeff)


def plot_time_series(t, data, window=PLOT_WINDOW):
    keep = t <= t[0] + window
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(t[keep], data[0, keep], color="tab:blue", lw=1.3, label=r"$u'_a$")
    ax.plot(t[keep], data[1, keep], color="tab:orange", lw=1.3, label=r"$u'_b$")
    ax.axhline(0.0, color="0.5", lw=0.8)
    ax.set_xlabel("t [s]")
    ax.set_ylabel("u' [m/s]")
    ax.set_title(
        f"Longitudinal velocity fluctuations at probes a and b (first {window} s)"
    )
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    return fig


def _cloud_axes(ax, data, title):
    ax.scatter(data[0], data[1], s=4, alpha=0.25, color="tab:blue", label="samples")
    ax.set_xlabel(r"$u'_a$ [m/s]")
    ax.set_ylabel(r"$u'_b$ [m/s]")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)


def plot_scatter(data):
    fig, ax = plt.subplots(figsize=(8, 7))
    _cloud_axes(ax, data, "Joint distribution of $u'_a$ and $u'_b$")
    ax.legend(loc="upper left")
    return fig


def plot_projection(data, phi):
    coeff, points = project(data, phi)
    fig, ax = plt.subplots(figsize=(8, 7))
    _cloud_axes(ax, data, r"Samples projected on the trial direction $\phi$")
    ax.scatter(
        points[0],
        points[1],
        s=6,
        alpha=0.6,
        color="tab:red",
        zorder=3,
        label=rf"$a_j\phi$ (variance {coeff.var(ddof=1):.2f} m$^2$/s$^2$)",
    )
    extent = np.abs(data).max()
    line = np.array([-extent, extent])
    ax.plot(
        line * phi[0],
        line * phi[1],
        color="black",
        lw=0.8,
        zorder=2,
        label=rf"$\phi=({phi[0]:.3f}, {phi[1]:.3f})$",
    )
    ax.legend(loc="upper left")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t, data = generate_fluctuations()
    cov = covariance(data)
    coeff, _ = project(data, PHI)
    print("Covariance matrix C (m^2/s^2):")
    print(np.array2string(cov, precision=3))
    print(f"Correlation coefficient: {cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1]):.3f}")
    print(f"Fluctuation energy (tr C)/2: {0.5 * np.trace(cov):.3f} m^2/s^2")
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
