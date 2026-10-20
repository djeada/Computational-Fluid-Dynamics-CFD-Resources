"""POD energy spectrum, truncation thresholds and rank-r reconstructions of a wake.

A synthetic cylinder-wake transverse velocity field v(x, y, t) is sampled on
a mesh that is stretched toward the wake centreline. Because the cells have
different sizes, POD is computed in the area-weighted inner product (weights
from the trapezoidal rule). The figure shows the eigenvalue spectrum, the
cumulative energy with the 90 % and 99 % thresholds, and one snapshot
reconstructed with r = 1, 2, 5 and 10 modes.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import PODResult, compute_pod  # noqa: E402

# Flow and wake model (lengths in cylinder diameters D, velocities in U_inf).
STROUHAL = 0.2  # shedding Strouhal number f D / U_inf [-]
CONVECTION_SPEED = 0.8  # convection speed of the vortices / U_inf [-]
ENVELOPE_PEAK = 4.0  # x/D at which the fluctuation amplitude peaks [-]
HARMONICS = ((1.0, 1), (0.35, 2), (0.15, 3))  # (amplitude [-], harmonic number)
N_BROADBAND = 30  # number of random small-scale travelling structures
BROADBAND_AMPLITUDE = 0.22  # amplitude of the first one; the j-th has A j^-1/2 [-]
NOISE_STD = 0.01  # measurement noise [-]
SEED = 1

# Sampling: mesh stretched toward y = 0 and snapshots over 8 shedding periods.
X_RANGE = (1.0, 11.0)  # streamwise extent [D]
Y_HALF_WIDTH = 3.0  # the mesh covers -3 <= y/D <= 3
N_X, N_Y = 120, 48
STRETCHING = 2.0  # sinh stretching parameter (0 gives a uniform mesh) [-]
N_SNAPSHOTS = 200
DT = 0.2  # time between snapshots [D / U_inf]

RANKS = (1, 2, 5, 10)
THRESHOLDS = (0.90, 0.99)
SNAPSHOT_INDEX = 37  # snapshot shown in the reconstruction panels
N_SPECTRUM = 40  # modes shown in the spectrum panels


def stretched_mesh(n_x=N_X, n_y=N_Y, beta=STRETCHING):
    """Uniform x, and y = H sinh(beta eta)/sinh(beta) with uniform eta in [-1, 1]."""
    x = np.linspace(*X_RANGE, n_x)
    eta = np.linspace(-1.0, 1.0, n_y)
    y = Y_HALF_WIDTH * (np.sinh(beta * eta) / np.sinh(beta) if beta > 0 else eta)
    return x, y


def trapezoid_weights(coordinates):
    """One-dimensional trapezoidal-rule weights for a sorted, nonuniform grid."""
    widths = np.diff(coordinates)
    weights = np.zeros_like(coordinates)
    weights[:-1] += 0.5 * widths
    weights[1:] += 0.5 * widths
    return weights


def area_weights(x, y):
    """Cell-area weights of the flattened (x, y) grid, x varying slowest."""
    return np.outer(trapezoid_weights(x), trapezoid_weights(y)).ravel()


def wake_components(seed=SEED):
    """Return the travelling structures as (amplitude, wavenumber, omega, phase, shape).

    ``shape(eta)`` gives the cross-stream profile as a function of y / b(x).
    """
    rng = np.random.default_rng(seed)
    omega = 2.0 * np.pi * STROUHAL  # shedding angular frequency [U_inf / D]
    k = omega / CONVECTION_SPEED  # wavenumber of the vortex street [1 / D]
    profiles = (
        lambda eta: np.exp(-(eta**2)),
        lambda eta: 2.0 * eta * np.exp(-(eta**2)),
        lambda eta: (1.0 - 2.0 * eta**2) * np.exp(-(eta**2)),
    )
    components = [(amp, h * k, h * omega, 0.0, profiles[h - 1]) for amp, h in HARMONICS]
    for j in range(N_BROADBAND):
        k_j = k * rng.uniform(1.5, 6.0)
        centre, width = rng.uniform(-1.0, 1.0), rng.uniform(0.3, 0.8)
        components.append(
            (
                BROADBAND_AMPLITUDE / np.sqrt(j + 1),
                k_j,
                CONVECTION_SPEED * k_j,
                rng.uniform(0.0, 2.0 * np.pi),
                lambda eta, c=centre, s=width: np.exp(-(((eta - c) / s) ** 2)),
            )
        )
    return components


def wake_snapshots(x, y, t, seed=SEED, noise_std=NOISE_STD):
    """Return the N x M matrix of v / U_inf, points (x slowest) in rows.

    Every structure is A g(x) f(y / b(x)) cos(k x - omega t + phase), with the
    amplitude envelope g(x) = (x/x_p) exp(1 - x/x_p) and the wake half-width
    b(x) = 0.5 + 0.1 x. A travelling structure is the sum of two standing
    patterns, cos(k x + phase) cos(omega t) + sin(k x + phase) sin(omega t).
    """
    X, Y = np.meshgrid(x, y, indexing="ij")
    envelope = (X / ENVELOPE_PEAK) * np.exp(1.0 - X / ENVELOPE_PEAK)
    eta = Y / (0.5 + 0.1 * X)
    data = np.zeros((X.size, t.size))
    for amp, k, omega, phase, shape in wake_components(seed):
        spatial = (amp * envelope * shape(eta)).ravel()
        data += np.outer(spatial * np.cos(k * X.ravel() + phase), np.cos(omega * t))
        data += np.outer(spatial * np.sin(k * X.ravel() + phase), np.sin(omega * t))
    rng = np.random.default_rng(seed + 1000)
    return data + noise_std * rng.standard_normal(data.shape)


def weighted_pod(snapshots, weights):
    """POD in the inner product <f, g> = f^T W g with diagonal W = diag(weights).

    The SVD of W^{1/2} U gives modes psi with psi^T psi = I; phi = W^{-1/2} psi
    then satisfies phi^T W phi = I. The coefficients a = phi^T W u' and the
    eigenvalues are unchanged by the back-transformation.
    """
    root = np.sqrt(np.asarray(weights, dtype=float))[:, None]
    scaled = compute_pod(root * snapshots)
    return PODResult(
        mean=scaled.mean / root,
        modes=scaled.modes / root,
        singular_values=scaled.singular_values,
        coefficients=scaled.coefficients,
        n_snapshots=scaled.n_snapshots,
    )


def modes_for_energy(energy_fractions, threshold):
    """Smallest r whose leading modes hold at least ``threshold`` of the energy."""
    cumulative = np.cumsum(energy_fractions)
    return int(np.searchsorted(cumulative, threshold - 1e-12) + 1)


def relative_error(pod, snapshots, weights, rank, index):
    """Weighted relative error of the rank-r reconstruction of one snapshot."""
    fluctuation = snapshots[:, index] - pod.mean[:, 0]
    approx = pod.modes[:, :rank] @ pod.coefficients[:rank, index]
    error = fluctuation - approx
    return np.sqrt((weights * error**2).sum() / (weights * fluctuation**2).sum())


def plot_figure(x, y, snapshots, pod, weights, index=SNAPSHOT_INDEX):
    fractions = pod.energy_fractions
    cumulative = np.cumsum(fractions)
    n_show = min(N_SPECTRUM, fractions.size)
    modes = np.arange(1, n_show + 1)

    fig = plt.figure(figsize=(13, 9.5), layout="constrained")
    grid = fig.add_gridspec(3, 3, height_ratios=(1.3, 1.0, 1.0))

    ax = fig.add_subplot(grid[0, :2])
    ax.semilogy(modes, fractions[:n_show], "o-", color="tab:blue", ms=4)
    ax.set_xlabel("mode number i")
    ax.set_ylabel(r"$\lambda_i \,/\, \Sigma_j \lambda_j$ [-]")
    ax.set_title("(a) Eigenvalue spectrum: travelling structures give pairs")
    ax.grid(alpha=0.3, which="both")

    ax = fig.add_subplot(grid[0, 2])
    ax.plot(modes, 100 * cumulative[:n_show], "-", color="tab:blue")
    for threshold, color in zip(THRESHOLDS, ("tab:orange", "tab:red")):
        r = modes_for_energy(fractions, threshold)
        ax.axhline(100 * threshold, color=color, ls="--", lw=1)
        ax.plot(
            r,
            100 * cumulative[r - 1],
            "o",
            color=color,
            label=f"{100 * threshold:.0f} % at r = {r}",
        )
    ax.plot(
        RANKS,
        100 * cumulative[np.array(RANKS) - 1],
        "s",
        color="black",
        ms=5,
        label="r = " + ", ".join(map(str, RANKS)),
    )
    ax.set_xlabel("number of modes r")
    ax.set_ylabel("cumulative energy [%]")
    ax.set_ylim(35, 101)
    ax.set_title("(b) Cumulative energy")
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(alpha=0.3)

    fluctuation = snapshots[:, index] - pod.mean[:, 0]
    limit = np.abs(fluctuation).max()
    shape = (x.size, y.size)
    panels = [("(c) snapshot $v'$", fluctuation)]
    for rank in RANKS:
        approx = pod.modes[:, :rank] @ pod.coefficients[:rank, index]
        err = relative_error(pod, snapshots, weights, rank, index)
        label = "(" + "defg"[len(panels) - 1] + ")"
        panels.append((f"{label} r = {rank}, error {100 * err:.0f} %", approx))
    panels.append(("(h) residual for r = 10", fluctuation - approx))
    for n, (title, values) in enumerate(panels):
        ax = fig.add_subplot(grid[1 + n // 3, n % 3])
        mesh = ax.pcolormesh(
            x,
            y,
            values.reshape(shape).T,
            cmap="RdBu_r",
            vmin=-limit,
            vmax=limit,
            shading="nearest",
        )
        ax.set_title(title)
        ax.set_xlabel("x / D")
        if n % 3 == 0:
            ax.set_ylabel("y / D")
        ax.set_aspect("equal")
    fig.colorbar(mesh, ax=fig.axes[2:], shrink=0.8, label=r"$v' / U_\infty$ [-]")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x, y = stretched_mesh()
    t = DT * np.arange(N_SNAPSHOTS)
    snapshots = wake_snapshots(x, y, t)
    weights = area_weights(x, y)
    pod = weighted_pod(snapshots, weights)
    plain = compute_pod(snapshots)

    print(f"Snapshot matrix: N = {snapshots.shape[0]} points, M = {snapshots.shape[1]}")
    print(
        "Energy fractions of modes 1-6 (weighted):  ",
        np.array2string(100 * pod.energy_fractions[:6], precision=2),
    )
    print(
        "Energy fractions of modes 1-6 (unweighted):",
        np.array2string(100 * plain.energy_fractions[:6], precision=2),
    )
    for threshold in THRESHOLDS:
        print(
            f"{100 * threshold:.0f} % of the energy needs r = "
            f"{modes_for_energy(pod.energy_fractions, threshold)} modes "
            f"(unweighted: {modes_for_energy(plain.energy_fractions, threshold)})"
        )
    cumulative = np.cumsum(pod.energy_fractions)
    for rank in RANKS:
        err = relative_error(pod, snapshots, weights, rank, SNAPSHOT_INDEX)
        print(
            f"r = {rank:2d}: cumulative energy {100 * cumulative[rank - 1]:.1f} %, "
            f"rms error of all snapshots {100 * np.sqrt(1 - cumulative[rank - 1]):.1f} %, "
            f"error of snapshot {SNAPSHOT_INDEX} {100 * err:.1f} %"
        )

    fig = plot_figure(x, y, snapshots, pod, weights)
    finish_figures(
        {"pod_energy_and_truncation.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
