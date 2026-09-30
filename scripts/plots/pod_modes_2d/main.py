"""Two-point POD: contributions of modes 1 and 2 to velocity signals at points a and b.

Following the two-dimensional POD example (velocity measured at two points a
and b), synthetic velocity signals u_a(t) and u_b(t) share an in-phase
10 Hz component and carry an anti-phase 20 Hz harmonic plus seeded noise.
After removing the mean, the m x 2 snapshot matrix is decomposed with the
SVD, and the rank-one contributions U~^k = a_k phi_k^T of modes 1 and 2 are
plotted for each point together with their sum.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

T_START, T_END = 0.9, 1.1  # time window [s]
N_SAMPLES = 1000  # number of snapshots m
FREQUENCY = 10.0  # fundamental frequency [Hz]
AMP_FUNDAMENTAL = 1.0  # amplitude of the in-phase component [m/s]
AMP_HARMONIC = 0.5  # amplitude of the anti-phase harmonic [m/s]
NOISE_STD = 0.1  # standard deviation of measurement noise [m/s]
SEED = 0  # random seed


def generate_signals(n_samples=N_SAMPLES, noise_std=NOISE_STD, seed=SEED):
    """Return time and the snapshot matrix with columns u_a(t), u_b(t)."""
    rng = np.random.default_rng(seed)
    t = np.linspace(T_START, T_END, n_samples)
    fundamental = AMP_FUNDAMENTAL * np.sin(2 * np.pi * FREQUENCY * t)
    harmonic = AMP_HARMONIC * np.sin(4 * np.pi * FREQUENCY * t)
    u_a = fundamental + harmonic + noise_std * rng.standard_normal(n_samples)
    u_b = fundamental - harmonic + noise_std * rng.standard_normal(n_samples)
    return t, np.column_stack((u_a, u_b))


def pod_contributions(snapshots):
    """Return the mode contributions, POD modes and TKE fractions.

    The snapshot matrix U' (mean removed) is factorised as U' = W S Phi^T.
    The rows of Phi^T are the spatial modes phi_k, the columns of A = W S are
    the time coefficients a_k, and U~^k = a_k phi_k^T has the same shape as U'.
    """
    result = compute_pod(snapshots.T)
    contributions = [
        np.outer(result.coefficients[k], result.modes[:, k])
        for k in range(len(result.singular_values))
    ]
    return contributions, result.modes.T, result.energy_fractions


def plot_contributions(t, contributions, energy_fraction):
    """Plot modes 1, 2 and their sum for u'_a (top) and u'_b (bottom)."""
    mode1, mode2 = contributions[0], contributions[1]
    combined = mode1 + mode2
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    for col, (ax, point) in enumerate(zip(axes, ("a", "b"))):
        ax.plot(
            t,
            mode1[:, col],
            "r",
            label=rf"$\tilde{{U}}^1$ ({100 * energy_fraction[0]:.0f}% TKE)",
        )
        ax.plot(
            t,
            mode2[:, col],
            "b",
            label=rf"$\tilde{{U}}^2$ ({100 * energy_fraction[1]:.0f}% TKE)",
        )
        ax.plot(t, combined[:, col], "k--", label=r"$U'=\tilde{U}^1+\tilde{U}^2$")
        ax.set_xlabel("t (s)")
        ax.set_ylabel(f"$u'_{point}$ (m/s)")
        ax.legend(loc="upper right")
    fig.suptitle("Contributions from modes 1 and 2 to $u'_a$ and $u'_b$")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    t, snapshots = generate_signals()
    contributions, modes, energy_fraction = pod_contributions(snapshots)
    for k in range(len(energy_fraction)):
        print(
            f"mode {k + 1}: phi = [{modes[k, 0]:+.3f}, {modes[k, 1]:+.3f}], "
            f"TKE = {100 * energy_fraction[k]:.1f} %"
        )

    fig = plot_contributions(t, contributions, energy_fraction)

    finish_figures({"pod_modes_2d.png": fig}, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
