"""Illustrate Archimedes' principle for a block in a tank of fluid.

Computes the weight of a block and the buoyant force on it, decides whether it
floats or sinks, and draws the block (partly submerged at equilibrium when it
floats) with force arrows scaled to the force magnitudes.
"""

import sys
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

G = 9.81  # gravitational acceleration (m/s^2)
DEFAULT_OBJECT_DENSITY = 500.0  # kg/m^3
DEFAULT_FLUID_DENSITY = 1000.0  # kg/m^3 (water)
DEFAULT_OBJECT_VOLUME = 1.0  # m^3

TANK_WIDTH = 4.0  # drawing units
WATER_DEPTH = 4.0  # drawing units
OBJECT_SIZE = 1.0  # drawing units (side of the square block)
SUNK_POSITION = 1.0  # drawing units: bottom of a sinking block
MAX_ARROW = 1.0  # drawing units: length of the larger force arrow


def buoyancy_state(object_density, fluid_density, object_volume, g=G):
    """Return weight, buoyant force, floats flag and submerged volume fraction.

    The object floats if the buoyant force on the fully submerged object,
    rho_fluid V g, is at least its weight. A floating object sinks until the
    displaced volume gives a buoyant force equal to its weight, so its
    submerged fraction is rho_obj / rho_fluid.
    """
    weight = object_density * object_volume * g
    floats = fluid_density * object_volume * g >= weight
    submerged_fraction = object_density / fluid_density if floats else 1.0
    buoyant_force = fluid_density * submerged_fraction * object_volume * g
    return weight, buoyant_force, floats, submerged_fraction


def plot_archimedes_principle(object_density, fluid_density, object_volume):
    weight, buoyant_force, floats, fraction = buoyancy_state(
        object_density, fluid_density, object_volume
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    # Fluid
    ax.add_patch(
        patches.Rectangle((0, 0), TANK_WIDTH, WATER_DEPTH, color="skyblue", alpha=0.5)
    )

    # Object: at equilibrium depth if it floats, fully submerged otherwise
    if floats:
        bottom = WATER_DEPTH - fraction * OBJECT_SIZE
    else:
        bottom = SUNK_POSITION
    top = bottom + OBJECT_SIZE
    x_mid = TANK_WIDTH / 2
    ax.add_patch(
        patches.Rectangle(
            (x_mid - OBJECT_SIZE / 2, bottom), OBJECT_SIZE, OBJECT_SIZE, color="brown"
        )
    )

    # Force arrows start on the object and point in the force direction
    scale = MAX_ARROW / max(weight, buoyant_force)
    buoyant_length = buoyant_force * scale
    weight_length = weight * scale
    ax.annotate(
        "",
        xy=(x_mid, top + buoyant_length),
        xytext=(x_mid, top),
        arrowprops=dict(arrowstyle="->", lw=2),
        annotation_clip=False,
    )
    ax.text(
        x_mid + 0.1,
        top + buoyant_length / 2,
        f"Buoyant force $F_b$ = {buoyant_force:,.0f} N",
        va="center",
    )
    ax.annotate(
        "",
        xy=(x_mid, bottom - weight_length),
        xytext=(x_mid, bottom),
        arrowprops=dict(arrowstyle="->", lw=2),
        annotation_clip=False,
    )
    ax.text(
        x_mid + 0.1,
        bottom - weight_length / 2,
        f"Weight $W$ = {weight:,.0f} N",
        va="center",
    )

    ax.set_title("Archimedes' Principle Demonstration")
    ax.set_xlim(0, TANK_WIDTH)
    ax.set_ylim(-1, 6)
    ax.axis("off")

    if floats:
        ax.text(
            0.2,
            1.5,
            "The object floats because $\\rho_{obj} \\leq \\rho_{fluid}$:\n"
            f"$F_b = W$ with {fraction:.0%} of its volume submerged.",
            fontsize=12,
            color="green",
        )
    else:
        ax.text(
            0.2,
            4.5,
            "The object sinks because the weight > buoyant force.",
            fontsize=12,
            color="red",
        )
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--object-density",
        type=float,
        default=DEFAULT_OBJECT_DENSITY,
        help="object density in kg/m^3 (default: %(default)s)",
    )
    parser.add_argument(
        "--fluid-density",
        type=float,
        default=DEFAULT_FLUID_DENSITY,
        help="fluid density in kg/m^3 (default: %(default)s)",
    )
    parser.add_argument(
        "--object-volume",
        type=float,
        default=DEFAULT_OBJECT_VOLUME,
        help="object volume in m^3 (default: %(default)s)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    fig = plot_archimedes_principle(
        args.object_density, args.fluid_density, args.object_volume
    )

    finish_figures(
        {"archimedes_principle.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
