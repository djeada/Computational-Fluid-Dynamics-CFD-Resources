"""Side-view sketch of a ship hull and its free-surface wave, with the Froude number.

The wave is a sinusoid whose wavelength is tied to the ship speed through the
deep-water dispersion relation (phase speed = ship speed), so the sketch also
reports the speed and Froude number that the drawn wave corresponds to.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # m/s^2
HULL_LENGTH = 10.0  # waterline length L, m
WAVE_LENGTH = 4.0  # free-surface wavelength lambda, m
WAVE_AMPLITUDE = 0.1  # m


def ship_speed_from_wavelength(wavelength, g=G):
    """Speed (m/s) of a ship whose transverse waves have ``wavelength`` (m).

    Deep-water gravity waves travel at c = sqrt(g lambda / 2 pi); steady ship
    waves move with the ship, so U = c.
    """
    return np.sqrt(g * wavelength / (2 * np.pi))


def froude_number(speed, length, g=G):
    """Length-based Froude number Fr = U / sqrt(g L)."""
    return speed / np.sqrt(g * length)


def draw_ship_hull_and_waves(
    hull_length=HULL_LENGTH, wavelength=WAVE_LENGTH, amplitude=WAVE_AMPLITUDE
):
    """Draw the hull profile, the free-surface wave and annotations; return the figure."""
    speed = ship_speed_from_wavelength(wavelength)
    fr = froude_number(speed, hull_length)

    fig = plt.figure(figsize=(7, 5))

    # Free-surface wave, extended beyond the hull for clarity
    x_wave = np.linspace(-2, hull_length + 2, 300)
    y_wave = amplitude * np.sin(2.0 * np.pi * x_wave / wavelength)
    plt.plot(x_wave, y_wave, label="Free Surface Wave")

    # Stylised hull profile (side view) from x = 0 (bow) to x = L (stern).
    # Purely illustrative; it does not represent a specific vessel.
    x_hull = hull_length * np.array([0.0, 0.15, 0.4, 0.6, 0.85, 1.0])
    y_hull = np.array([0.0, -0.5, -0.7, -0.7, -0.5, 0.0])
    plt.fill(x_hull, y_hull, alpha=0.5, label="Ship Hull")

    # Arrow for the oncoming flow in the ship's frame of reference (to the right)
    plt.arrow(1, 0.5, 2.0, 0.0, width=0.02, head_width=0.1, length_includes_head=True)
    plt.text(1, 0.65, "Velocity U", fontsize=10)

    # Still water level
    plt.axhline(0, linestyle="--", label="Still Water Level")

    plt.text(
        hull_length / 2,
        0.7,
        r"$Fr = \frac{U}{\sqrt{g \, L}}$",
        fontsize=12,
        ha="center",
    )
    plt.text(
        hull_length / 2,
        -1.6,
        (
            f"$L$ = {hull_length:.0f} m, $\\lambda$ = {wavelength:.0f} m  →  "
            f"$U = \\sqrt{{g\\lambda / 2\\pi}}$ = {speed:.2f} m/s, $Fr$ = {fr:.2f}"
        ),
        fontsize=10,
        ha="center",
    )

    plt.title("Ship Hull and Wave Pattern – Froude Number Concept")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")
    plt.grid(True)
    plt.legend(loc="upper right")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = draw_ship_hull_and_waves()

    finish_figures(
        {"ship_hull_in_water.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
