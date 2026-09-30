"""Schematic of the Young-Laplace pressure jump across a spherical droplet.

Draws a droplet cross-section, labels the inside and outside pressures, marks
the radius, and evaluates Delta p = 2 sigma / R for a water droplet of a chosen
radius (and half that radius) to show that smaller droplets carry a larger
pressure jump.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SURFACE_TENSION = 0.0728  # N/m, water at about 20 degC
DROPLET_RADIUS = 1.0e-3  # m
ATMOSPHERIC_PRESSURE = 101325.0  # Pa


def laplace_pressure_jump(sigma, radius):
    """Return p_in - p_out (Pa) for a spherical interface of radius (m)."""
    return 2.0 * sigma / radius


def draw_droplet(
    sigma=SURFACE_TENSION, radius=DROPLET_RADIUS, p_out=ATMOSPHERIC_PRESSURE
):
    """Draw the annotated droplet schematic and return the figure.

    The circle is drawn with unit radius; ``radius`` (m) is only used to
    evaluate the pressure jump shown in the text box.
    """
    delta_p = laplace_pressure_jump(sigma, radius)
    delta_p_half = laplace_pressure_jump(sigma, radius / 2)
    p_in = p_out + delta_p

    fig, ax = plt.subplots(figsize=(8, 8))

    # Droplet interface (schematic, unit radius)
    circle = plt.Circle(
        (0, 0), 1.0, facecolor="skyblue", edgecolor="navy", alpha=0.4, linewidth=2
    )
    ax.add_patch(circle)

    # Radius from the centre to the interface
    angle = np.deg2rad(-45)
    tip = (np.cos(angle), np.sin(angle))
    ax.plot(0, 0, "ko", markersize=4)
    ax.annotate(
        "", xy=tip, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black")
    )
    ax.text(tip[0] / 2 + 0.05, tip[1] / 2 + 0.05, "$R$", fontsize=14)

    # Pressure annotations
    ax.text(
        0,
        0.2,
        r"$p_{in} = p_{out} + \frac{2 \, \sigma}{R}$",
        fontsize=14,
        ha="center",
    )
    ax.text(
        0,
        0.55,
        "Inside droplet: $p_{in}$ (higher)",
        fontsize=12,
        color="navy",
        ha="center",
    )
    ax.text(
        -1.9, 1.3, "Outside droplet\n$p_{out}$ (atmosphere)", fontsize=12, color="navy"
    )

    # Numerical example for water
    ax.text(
        0,
        -1.85,
        (
            f"Water, $\\sigma$ = {sigma:.4f} N/m, $p_{{out}}$ = {p_out:.0f} Pa\n"
            f"$R$ = {radius * 1e3:.2f} mm: $\\Delta p$ = {delta_p:.1f} Pa, "
            f"$p_{{in}}$ = {p_in:.1f} Pa\n"
            f"$R$ = {radius * 0.5e3:.2f} mm: $\\Delta p$ = {delta_p_half:.1f} Pa"
        ),
        fontsize=11,
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray"),
    )

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Pressure Difference Across a Spherical Droplet", fontsize=14)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = draw_droplet()

    finish_figures(
        {"pressure_difference_across_spherical_droplet.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
