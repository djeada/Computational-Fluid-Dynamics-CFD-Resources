"""Animate the Bak-Tang-Wiesenfeld sandpile on a 2D lattice as a 3D surface.

Grains are dropped one at a time on random sites of a square lattice. A site
holding at least 4 grains topples, sending one grain to each of its four
neighbours; grains pushed over the edge are lost. The height field is drawn as
a 3D surface after each grain, and the size of the avalanche it caused (number
of topplings) is shown in the status line.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

GRID_SIZE = 20  # lattice is GRID_SIZE x GRID_SIZE sites
CRITICAL_HEIGHT = 4  # a site topples at this height [grains] (= number of neighbours)
SEED = 0  # random seed for the drop positions
STEPS_PER_FRAME = 1  # grains added per animation frame
N_FRAMES = 1000  # default frames -> 1000 grains


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


class SandpileSimulation(Simulation):
    """Height field and the avalanche size caused by every grain added."""

    def __init__(self, size=GRID_SIZE, seed=SEED):
        super().__init__()
        self.rng = np.random.default_rng(seed)
        self.grid = np.zeros((size, size), dtype=int)
        self.avalanche_sizes = []  # topplings caused by grain 1, 2, ...

    @property
    def last_avalanche(self):
        return self.avalanche_sizes[-1] if self.avalanche_sizes else 0

    def step(self):
        self.avalanche_sizes.append(add_grain(self.grid, self.rng))


class SandpileView(View):
    """Height field as a 3D surface coloured from 0 to 3 grains.

    The colour bar sits left of the surface in the window and below it in a
    reel, where it also replaces the z label.
    """

    figsize = (10.0, 7.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        self.ax = ax = figure.add_subplot(projection="3d")
        n_rows, n_cols = simulation.grid.shape
        self.x, self.y = np.meshgrid(range(n_cols), range(n_rows))
        self.norm = Normalize(vmin=0, vmax=CRITICAL_HEIGHT - 1)
        self.surface = None
        ax.set_zlim(0, CRITICAL_HEIGHT)
        ax.set_zticks(range(CRITICAL_HEIGHT + 1))
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(MaxNLocator(5, integer=True))
        ax.set(xlabel="x (site)", ylabel="y (site)")
        if portrait:  # keep the larger labels clear of the tick labels
            ax.xaxis.labelpad = ax.yaxis.labelpad = 14
        else:
            ax.set_zlabel("height (grains)")
        figure.colorbar(
            ScalarMappable(self.norm, "plasma"), ax=ax, label="height (grains)",
            location="bottom" if portrait else "left", shrink=0.7,
            pad=0.0 if not portrait else 0.02, ticks=range(CRITICAL_HEIGHT),
        )  # fmt: skip

    def draw(self):
        if self.surface is not None:
            self.surface.remove()
        self.surface = self.ax.plot_surface(
            self.x, self.y, self.simulation.grid, cmap="plasma", norm=self.norm,
            edgecolor="k", linewidth=0.5, antialiased=True,
        )  # fmt: skip

    def status(self):
        simulation = self.simulation
        return f"grain {simulation.steps}   avalanche {simulation.last_avalanche}"


ANIMATION = Animation(
    title="Bak-Tang-Wiesenfeld Sandpile",
    subtitle="Self-organised criticality, grain by grain",
    filename="sandpile_3d.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="grains",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, SandpileSimulation(), SandpileView)
    sizes = simulation.avalanche_sizes
    print(
        f"{simulation.steps} grains added, mean height {simulation.grid.mean():.2f}, "
        f"{np.count_nonzero(sizes)} avalanches, largest {max(sizes, default=0)} "
        "topplings"
    )


if __name__ == "__main__":
    main()
