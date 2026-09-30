"""Plot the linear increase of hydrostatic pressure with depth, P = P0 + rho g h."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

ATMOSPHERIC_PRESSURE = 101325.0  # Pa


def hydrostatic_pressure(
    depth, fluid_density, g, surface_pressure=ATMOSPHERIC_PRESSURE
):
    """Absolute pressure (Pa) at ``depth`` (m) below a free surface."""
    return surface_pressure + fluid_density * g * depth


def plot_pressure_variation_with_depth(fluid_density=1000, g=9.81, max_depth=20):
    """Plot pressure against depth.

    fluid_density in kg/m^3, g in m/s^2, max_depth in m. Returns the figure.
    """
    depth = np.linspace(0, max_depth, 100)
    pressure = hydrostatic_pressure(depth, fluid_density, g)

    fig = plt.figure(figsize=(8, 6))
    plt.plot(pressure, depth, label="Pressure vs Depth", color="blue")

    # Invert the y-axis so that depth increases downwards
    plt.gca().invert_yaxis()

    plt.title("Pressure Variation with Depth")
    plt.xlabel("Absolute pressure (Pa)")
    plt.ylabel("Depth (m)")
    plt.grid(True)
    plt.legend()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_pressure_variation_with_depth()

    finish_figures(
        {"pressure_variation_with_depth.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
