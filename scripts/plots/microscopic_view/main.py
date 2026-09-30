"""Contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid.

The left panel scatters randomly placed dots that stand for molecules; the
right panel draws a smooth, divergence-free velocity field
u = (sin(y/2), cos(x/2)) as a quiver plot, standing for the continuum
description in which velocity is defined at every point.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

BOX_SIZE = 10.0  # side length of each panel [arbitrary units]
N_MOLECULES = 20  # number of dots in the molecular panel
GRID_POINTS = 20  # quiver arrows per direction in the continuum panel
SEED = 0  # random seed for the molecule positions


def molecule_positions(n=N_MOLECULES, box=BOX_SIZE, seed=SEED):
    """Return uniformly distributed random x and y positions in a square box."""
    rng = np.random.RandomState(seed)
    x = rng.rand(n) * box
    y = rng.rand(n) * box
    return x, y


def continuum_field(n=GRID_POINTS, box=BOX_SIZE):
    """Return a grid and the velocity field u = sin(y/2), v = cos(x/2)."""
    X, Y = np.meshgrid(np.linspace(0, box, n), np.linspace(0, box, n))
    U = np.sin(Y / 2)
    V = np.cos(X / 2)
    return X, Y, U, V


def plot_microscopic_view():
    """Draw both panels and return the figure."""
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].set_title("Microscopic (Molecular) View")
    ax[0].set_xlim(0, BOX_SIZE)
    ax[0].set_ylim(0, BOX_SIZE)
    ax[0].set_aspect("equal")
    ax[0].axis("off")
    x, y = molecule_positions()
    ax[0].scatter(x, y, s=100, color="black")
    ax[0].text(5, -1, "Molecules in constant random motion.", ha="center", fontsize=10)

    ax[1].set_title("Macroscopic (Continuum) View")
    ax[1].set_xlim(0, BOX_SIZE)
    ax[1].set_ylim(0, BOX_SIZE)
    ax[1].set_aspect("equal")
    ax[1].axis("off")
    X, Y, U, V = continuum_field()
    ax[1].quiver(X, Y, U, V, scale=20)
    ax[1].text(
        5,
        -1,
        "Fluid as a continuous medium with properties like density, pressure, velocity.",
        ha="center",
        fontsize=10,
    )

    fig.suptitle("Microscopic vs. Macroscopic View", fontsize=14)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_microscopic_view()

    finish_figures(
        {"microscopic_view.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
