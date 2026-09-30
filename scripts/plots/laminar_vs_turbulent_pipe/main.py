"""Plot laminar and turbulent radial velocity profiles in a circular pipe.

The laminar profile is the Hagen-Poiseuille parabola u = u_max (1 - (r/R)^2)
and the turbulent profile is the empirical 1/7 power law
u = u_max (1 - r/R)^(1/7). Both use the same centreline velocity and are shown
in side-by-side panels with radius on the vertical axis (centreline at the top,
wall at the bottom).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

PIPE_RADIUS = 1.0  # R (length units)
MAX_VELOCITY = 2.0  # centreline velocity u_max (velocity units)


def laminar_profile(r, pipe_radius, max_velocity):
    """Hagen-Poiseuille profile u_max (1 - (r/R)^2)."""
    return max_velocity * (1 - (r / pipe_radius) ** 2)


def turbulent_profile(r, pipe_radius, max_velocity):
    """One-seventh power law u_max (1 - r/R)^(1/7)."""
    return max_velocity * (1 - r / pipe_radius) ** (1 / 7)


def plot_laminar_vs_turbulent(pipe_radius=PIPE_RADIUS, max_velocity=MAX_VELOCITY):
    """Return a two-panel figure of the laminar and turbulent profiles."""
    r = np.linspace(0, pipe_radius, 200)
    laminar_velocity = laminar_profile(r, pipe_radius, max_velocity)
    turbulent_velocity = turbulent_profile(r, pipe_radius, max_velocity)

    fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)

    # Laminar flow plot
    ax[0].plot(laminar_velocity, r, label="Laminar Flow", color="blue")
    ax[0].invert_yaxis()  # shared y-axis: inverts both panels
    ax[0].set_title("Laminar Flow (Parabolic)")
    ax[0].set_xlabel("Velocity")
    ax[0].set_ylabel("Radius (r)")
    ax[0].grid(True)
    ax[0].annotate(
        "v(r) max here",
        xy=(max_velocity, 0),
        xytext=(max_velocity - 0.8, 0.3 * pipe_radius),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10,
    )
    ax[0].annotate(
        "Velocity = 0 at wall",
        xy=(0, pipe_radius),
        xytext=(0.1, 0.6 * pipe_radius),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10,
    )

    # Turbulent flow plot
    r_mix = 0.5 * pipe_radius
    ax[1].plot(turbulent_velocity, r, label="Turbulent Flow", color="red")
    ax[1].set_title("Turbulent Flow (Flatter)")
    ax[1].set_xlabel("Velocity")
    ax[1].set_ylabel("Radius (r)")
    ax[1].grid(True)
    ax[1].annotate(
        "Flat core: strong\nturbulent mixing",
        xy=(turbulent_profile(r_mix, pipe_radius, max_velocity), r_mix),
        xytext=(max_velocity * 0.35, 0.35 * pipe_radius),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10,
    )
    ax[1].annotate(
        "Steep drop to\nvelocity = 0 at wall",
        xy=(0, pipe_radius),
        xytext=(0.5, pipe_radius - 0.2 * pipe_radius),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10,
    )

    fig.suptitle("Laminar vs. Turbulent Flow Velocity Profiles", fontsize=14)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_laminar_vs_turbulent()

    finish_figures(
        {"laminar_vs_turbulent_pipe.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
