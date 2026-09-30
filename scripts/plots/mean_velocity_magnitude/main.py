"""Compare a mock experimental profile with a mock CFD scale-resolving simulation.

Plots the normalised mean velocity magnitude |U|/U0 along an under-body
centreline, the kind of line plot used to validate CFD predictions against
wind-tunnel measurements. Both data sets are synthetic: the "experiment" is an
exponentially damped sine and the "CFD SRS" curve adds seeded Gaussian noise.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_POINTS = 50  # number of sample points along the line [-]
X_MAX = 6.0  # length of the sampling line [m]
DECAY_RATE = 0.2  # decay rate of the mock profile [1/m]
OFFSET = 0.75  # mean level of the mock profile [-]
NOISE_STD = 0.05  # standard deviation of the synthetic CFD deviation [-]
SEED = 0  # random seed for the synthetic CFD deviation


def generate_data(n_points=N_POINTS, x_max=X_MAX, noise_std=NOISE_STD, seed=SEED):
    """Return the line coordinate and the mock experimental and CFD profiles."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, x_max, n_points)
    exp = np.exp(-DECAY_RATE * x) * np.sin(x) + OFFSET
    cfd = exp + noise_std * rng.normal(size=x.size)
    return x, exp, cfd


def plot_profiles(x, exp, cfd):
    """Plot both profiles on one set of axes and return the figure."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, exp, "o-", label="Exp", color="black")
    ax.plot(x, cfd, "-", label="CFD SRS", color="cyan")
    ax.set_xlabel("rel. distance [m]")
    ax.set_ylabel("$|U|/U_0$ [-]")
    ax.set_title(
        "Mean velocity magnitude, under-body centreline\n"
        "L1 / Underbody Centerline @ z = -0.2376m"
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x, exp, cfd = generate_data()
    rms = np.sqrt(np.mean((cfd - exp) ** 2))
    print(f"RMS difference between CFD and experiment: {rms:.4f}")

    fig = plot_profiles(x, exp, cfd)

    finish_figures(
        {"mean_velocity_magnitude.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
