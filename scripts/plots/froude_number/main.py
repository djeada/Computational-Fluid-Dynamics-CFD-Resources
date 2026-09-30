"""Plot the length-based Froude number against speed for several hull lengths.

Fr = U / sqrt(g L) is evaluated for hull lengths of 5, 10, 15, and 20 m over
speeds of 0 to 10 m/s. Dashed reference lines mark the hull speed,
Fr = 1/sqrt(2 pi) (about 0.40), where the bow wave length equals the hull
length, and Fr = 1, a rough threshold for the planing regime.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # gravitational acceleration, m/s^2
HULL_LENGTHS = [5, 10, 15, 20]  # m
V_MAX = 10.0  # m/s
FR_HULL_SPEED = 1.0 / np.sqrt(2.0 * np.pi)  # wave length 2 pi U^2 / g equals L
FR_PLANING = 1.0  # approximate onset of planing (length-based Froude number)


def froude_number(velocity, g, length):
    """
    Compute the Froude number.
    Fr = U / sqrt(g * L)

    Parameters
    ----------
    velocity : float or np.ndarray
        Characteristic flow velocity (m/s).
    g : float
        Gravitational acceleration (m/s^2).
    length : float
        Characteristic length scale (m).

    Returns
    -------
    Fr : float or np.ndarray
        Froude number.
    """
    return velocity / np.sqrt(g * length)


def plot_froude_number_vs_velocity(lengths=HULL_LENGTHS, g=G, v_max=V_MAX):
    """
    Plot the Froude number vs. velocity for a list of characteristic hull lengths.
    """
    velocities = np.linspace(0, v_max, 200)  # m/s

    fig, ax = plt.subplots(figsize=(7, 5))

    for L in lengths:
        fr_values = froude_number(velocities, g, L)
        line = ax.plot(velocities, fr_values, label=f"L = {L} m")[0]
        # Speed at which this hull reaches hull speed
        v_hull = FR_HULL_SPEED * np.sqrt(g * L)
        ax.plot(v_hull, FR_HULL_SPEED, "o", color=line.get_color(), markersize=5)

    ax.axhline(FR_HULL_SPEED, color="gray", linestyle="--", linewidth=1)
    ax.text(
        0.2,
        FR_HULL_SPEED + 0.02,
        rf"Hull speed, $Fr = 1/\sqrt{{2\pi}} \approx {FR_HULL_SPEED:.2f}$",
        fontsize=9,
        color="gray",
    )
    ax.axhline(FR_PLANING, color="gray", linestyle=":", linewidth=1)
    ax.text(
        0.2,
        FR_PLANING + 0.02,
        r"Planing regime, $Fr \gtrsim 1$",
        fontsize=9,
        color="gray",
    )

    ax.set_title("Froude Number vs. Velocity for Various Hull Lengths")
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Froude Number (Fr)")
    ax.set_xlim(0, v_max)
    ax.set_ylim(bottom=0)
    ax.grid(True)
    ax.legend(loc="lower right")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_froude_number_vs_velocity()

    finish_figures(
        {"froude_number.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
