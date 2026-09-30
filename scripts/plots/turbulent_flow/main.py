"""Reynolds decomposition of a synthetic velocity signal u(t) = u_bar + u'(t).

Plots (a) the signal with its mean, (b) the fluctuation u', and (c) the squared
fluctuation with its mean, and lists u_bar, u_rms, k = <u'^2>/2 and the
turbulence intensity in the fourth panel.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

MEAN_VELOCITY = 5.0  # m/s
OSCILLATION_AMPLITUDE = 1.0  # m/s
NOISE_STD = 0.2  # m/s
DURATION = 100.0  # s
N_SAMPLES = 1000
SEED = 0


def synthetic_signal(seed=SEED):
    """Return time t and u(t) = U + A sin(t) + Gaussian noise."""
    rng = np.random.default_rng(seed)
    time = np.linspace(0, DURATION, N_SAMPLES)
    velocity = (
        MEAN_VELOCITY
        + OSCILLATION_AMPLITUDE * np.sin(time)
        + rng.normal(scale=NOISE_STD, size=time.shape)
    )
    return time, velocity


def reynolds_decomposition(velocity):
    """Split a signal into its time mean and fluctuation."""
    mean = np.mean(velocity)
    return mean, velocity - mean


def turbulence_statistics(mean, fluctuation):
    """Return <u'^2>, u_rms, one-component TKE k = <u'^2>/2 and intensity u_rms/u_bar."""
    variance = np.mean(fluctuation**2)
    u_rms = np.sqrt(variance)
    return variance, u_rms, 0.5 * variance, u_rms / mean


def plot_decomposition(time, velocity):
    """Draw the three signal panels and a statistics panel; return the figure."""
    mean, fluctuation = reynolds_decomposition(velocity)
    squared = fluctuation**2
    variance, u_rms, k, intensity = turbulence_statistics(mean, fluctuation)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    axs[0, 0].plot(time, velocity, color="black")
    axs[0, 0].axhline(mean, color="gray", linestyle="--", label=r"$\bar{u}$")
    axs[0, 0].set_title("(a)")
    axs[0, 0].set_xlabel("time")
    axs[0, 0].set_ylabel("$u$")
    axs[0, 0].legend(loc="upper right")

    axs[0, 1].plot(time, fluctuation, color="black")
    axs[0, 1].set_title("(b)")
    axs[0, 1].set_xlabel("time")
    axs[0, 1].set_ylabel("$u'$")

    axs[1, 0].plot(time, squared, color="black")
    axs[1, 0].axhline(
        variance, color="gray", linestyle="--", label=r"$\overline{u'^2}$"
    )
    axs[1, 0].set_title("(c)")
    axs[1, 0].set_xlabel("time")
    axs[1, 0].set_ylabel("$(u')^2$")
    axs[1, 0].legend(loc="upper right")

    # Fourth panel: summary statistics instead of an empty axes
    axs[1, 1].axis("off")
    axs[1, 1].text(
        0.1,
        0.5,
        (
            f"$\\bar{{u}}$ = {mean:.3f}\n"
            f"$\\overline{{u'^2}}$ = {variance:.3f}\n"
            f"$u_{{rms}} = \\sqrt{{\\overline{{u'^2}}}}$ = {u_rms:.3f}\n"
            f"$k_u = \\frac{{1}}{{2}}\\overline{{u'^2}}$ = {k:.3f}\n"
            f"$Tu = u_{{rms}} / \\bar{{u}}$ = {100 * intensity:.1f} %"
        ),
        fontsize=16,
        va="center",
        linespacing=1.8,
    )

    plt.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    time, velocity = synthetic_signal()
    fig = plot_decomposition(time, velocity)

    finish_figures(
        {"turbulence_plots.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
