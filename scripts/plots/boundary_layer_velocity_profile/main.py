"""Plot the one-seventh power-law velocity profile of a turbulent boundary layer.

Evaluates u / U_inf = (y / delta)^(1/7) for 0 <= y / delta <= 1 and marks the
wall and the boundary layer edge.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_POINTS = 1000  # wall-normal samples (dense, because du/dy is infinite at the wall)
POWER = 1 / 7  # exponent of the power law


def power_law_profile(eta, power=POWER):
    """Velocity ratio u / U_inf as a function of eta = y / delta."""
    return eta**power


def plot_profile(eta, u_ratio):
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(
        u_ratio,
        eta,
        linewidth=2,
        color="blue",
        label=r"1/7 power law: $u/U_\infty = (y/\delta)^{1/7}$",
    )

    # Boundary layer edge, where the power law reaches u = U_inf
    ax.axhline(y=1, linestyle="--", color="red", linewidth=1)
    ax.text(
        0.05, 1.02, r"Boundary Layer Thickness ($\delta$)", fontsize=12, color="red"
    )

    # Wall
    ax.axhline(y=0, color="black", linewidth=3, label="Wall (y=0, u=0)")

    ax.set_title("Turbulent Boundary Layer Velocity Profile", fontsize=14)
    ax.set_xlabel(r"Velocity $u/U_\infty$", fontsize=12)
    ax.set_ylabel(r"Distance from Wall $y/\delta$", fontsize=12)
    ax.legend(loc="center left")
    ax.grid(True)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.1)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    eta = np.linspace(0, 1, N_POINTS)
    fig = plot_profile(eta, power_law_profile(eta))

    finish_figures(
        {"boundary_layer_velocity_profile.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
