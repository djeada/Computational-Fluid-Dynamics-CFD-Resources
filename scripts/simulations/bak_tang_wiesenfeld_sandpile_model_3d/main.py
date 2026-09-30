"""Animate the Bak-Tang-Wiesenfeld sandpile on a 2D lattice as a 3D surface.

Grains are dropped one at a time on random sites of a square lattice. A site
holding at least 4 grains topples, sending one grain to each of its four
neighbours; grains pushed over the edge are lost. The height field is drawn as
a 3D surface after each grain, and the size of the avalanche it caused (number
of topplings) is shown in the title.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

GRID_SIZE = 20  # lattice is GRID_SIZE x GRID_SIZE
NUM_GRAINS = 1000  # grains added in the default animation
CRITICAL_HEIGHT = 4  # a site topples at this height (= number of neighbours)
SEED = 0  # random seed for the drop positions


def topple(grid, critical_height=CRITICAL_HEIGHT):
    """Relax the lattice in place until every site is below critical_height.

    Each toppling removes 4 grains from a site and adds one to each of its
    four neighbours, so grains are conserved except at the open boundary.
    Returns the avalanche size (total number of topplings).
    """
    n_rows, n_cols = grid.shape
    topplings = 0
    unstable = True
    while unstable:
        unstable = False
        for i in range(n_rows):
            for j in range(n_cols):
                if grid[i, j] >= critical_height:
                    grid[i, j] -= 4
                    if i > 0:
                        grid[i - 1, j] += 1
                    if i < n_rows - 1:
                        grid[i + 1, j] += 1
                    if j > 0:
                        grid[i, j - 1] += 1
                    if j < n_cols - 1:
                        grid[i, j + 1] += 1
                    topplings += 1
                    unstable = True
    return topplings


def add_grain(grid, rng):
    """Drop one grain on a random site, relax the pile, return avalanche size."""
    i, j = rng.integers(0, grid.shape[0]), rng.integers(0, grid.shape[1])
    grid[i, j] += 1
    return topple(grid)


def setup_figure(grid):
    """Create the dark 3D figure with a colour bar; return (fig, ax, draw)."""
    fig = plt.figure(figsize=(12, 8), facecolor="black")
    ax = fig.add_axes([0.3, 0.1, 0.65, 0.8], projection="3d", facecolor="black")
    cbar_ax = fig.add_axes([0.1, 0.1, 0.02, 0.8])

    x, y = np.meshgrid(range(grid.shape[1]), range(grid.shape[0]))
    zmax = CRITICAL_HEIGHT
    norm = Normalize(vmin=0, vmax=zmax - 1)

    ax.set_zlim(0, zmax)
    ax.set_xlabel("X-axis", fontsize=12, color="white")
    ax.set_ylabel("Y-axis", fontsize=12, color="white")
    ax.set_zlabel("Grains (Height)", fontsize=12, color="white")
    ax.xaxis.pane.set_facecolor("black")
    ax.yaxis.pane.set_facecolor("black")
    ax.zaxis.pane.set_facecolor("black")
    ax.grid(True, color="gray", linestyle="--", linewidth=0.5)
    for axis in ("x", "y", "z"):
        ax.tick_params(axis=axis, colors="white")

    def draw(grains, avalanche):
        for coll in ax.collections[:]:
            coll.remove()
        surf = ax.plot_surface(
            x,
            y,
            grid,
            cmap="plasma",
            norm=norm,
            edgecolor="k",
            linewidth=0.5,
            antialiased=True,
        )
        ax.set_title(
            "Bak-Tang-Wiesenfeld Sandpile Model: Evolution Over Time\n"
            f"grains added: {grains}, last avalanche: {avalanche} topplings, "
            f"mean height: {grid.mean():.2f}",
            fontsize=14,
            color="white",
        )
        return surf

    surf = draw(0, 0)
    cbar = fig.colorbar(surf, cax=cbar_ax, orientation="vertical")
    cbar.set_label("Grains (Height)", color="white", fontsize=12)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")
    return fig, ax, draw


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=NUM_GRAINS,
        help=f"number of grains to add, one per frame (default {NUM_GRAINS})",
    )
    args = parser.parse_args(argv)

    rng = np.random.default_rng(SEED)
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    fig, ax, draw = setup_figure(grid)
    state = {"grains": 0, "avalanche": 0, "sizes": []}

    def step():
        state["avalanche"] = add_grain(grid, rng)
        state["sizes"].append(state["avalanche"])
        state["grains"] += 1

    def update(frame):
        step()
        return (draw(state["grains"], state["avalanche"]),)

    if args.no_show:
        for _ in range(args.steps):
            step()
        draw(state["grains"], state["avalanche"])
    else:
        ani = FuncAnimation(
            fig, update, frames=args.steps, interval=20, blit=False, repeat=False
        )
        plt.show()
        del ani

    sizes = np.array(state["sizes"])
    if sizes.size:
        print(
            f"{state['grains']} grains added, mean height {grid.mean():.2f}, "
            f"{np.count_nonzero(sizes)} avalanches, largest {sizes.max()} topplings"
        )
    if args.output:
        save_figure(fig, args.output, "sandpile_3d.png", facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
