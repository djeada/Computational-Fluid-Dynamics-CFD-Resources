"""Solve a random maze with Laplace's equation and follow the potential gradient.

A perfect maze is carved with a seeded depth-first backtracker. Laplace's
equation is solved on the open cells with phi = 0 at the entrance, phi = 1 at
the exit and insulating (zero-flux) walls, by conjugate-gradient iterations
shown as the potential spreading through the passages. The route is then
traced by stepping to the neighbour with the largest potential and revealed
one cell per solver step.
"""

import random
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgba
from matplotlib.patches import Circle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Constants
MAZE_SIZE: int = 100  # grid cells per side (walls and passages)
SEED: int = 0
MAX_ITERATIONS: int = 50_000  # cap on conjugate-gradient iterations
TOLERANCE: float = 1e-10  # stop when ||residual|| / ||b|| < TOLERANCE
# One solver step is one CG iteration, the path trace, or one revealed path cell.
# The default maze takes 4646 + 1 + 1649 = 6296 steps.
STEPS_PER_FRAME: int = 10
N_FRAMES: int = 630  # frames of a headless run or reel: the full solve and path
PATH_COLOR = "gold"
START_COLOR = "red"
END_COLOR = "lime"
MARKER_RADIUS = 1.4  # entrance and exit markers [cells]

NEIGHBOURS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def generate_maze(size: int, rng: random.Random) -> np.ndarray:
    """Depth-first backtracker on the even-indexed cells; 1 = wall, 0 = open."""
    maze = np.ones((size, size), dtype=int)
    start = (0, 0)
    maze[start] = 0
    stack: list[tuple[int, int]] = [start]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in directions
            if 0 <= x + dx < size and 0 <= y + dy < size and maze[x + dx, y + dy] == 1
        ]
        if neighbors:
            nx, ny = rng.choice(neighbors)
            maze[(x + nx) // 2, (y + ny) // 2] = 0
            maze[nx, ny] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze


def apply_laplacian(phi: np.ndarray, open_mask: np.ndarray) -> np.ndarray:
    """Graph Laplacian on open cells: sum over open neighbours of (phi - phi_nb).

    Walls and the domain edge contribute nothing, i.e. d(phi)/dn = 0 there.
    """
    result = np.zeros_like(phi)
    for di, dj in NEIGHBOURS:
        nb = np.zeros_like(phi)
        nb_open = np.zeros_like(open_mask)
        src = (
            slice(max(di, 0), phi.shape[0] + min(di, 0)),
            slice(max(dj, 0), phi.shape[1] + min(dj, 0)),
        )
        dst = (
            slice(max(-di, 0), phi.shape[0] + min(-di, 0)),
            slice(max(-dj, 0), phi.shape[1] + min(-dj, 0)),
        )
        nb[dst] = phi[src]
        nb_open[dst] = open_mask[src]
        link = open_mask & nb_open
        result[link] += phi[link] - nb[link]
    return result


class LaplaceSolver:
    """Conjugate gradients for the potential on the free open cells.

    Dirichlet values phi(start) = 0 and phi(end) = 1 are held fixed; every
    other open cell satisfies the discrete Laplace equation.
    """

    def __init__(self, maze, start, end):
        self.open = maze == 0
        self.free = self.open.copy()
        self.free[start] = self.free[end] = False
        self.phi = np.zeros(maze.shape)
        self.phi[end] = 1.0
        boundary = np.zeros(maze.shape)
        boundary[end] = 1.0
        # Move the known Dirichlet values to the right-hand side: A x = b.
        self.b = -apply_laplacian(boundary, self.open) * self.free
        self.residual = self.b - self._operator(self.phi * self.free)
        self.direction = self.residual.copy()
        self.rr = np.sum(self.residual**2)
        self.b_norm = np.sqrt(np.sum(self.b**2))
        self.iterations = 0

    def _operator(self, x):
        return apply_laplacian(x, self.open) * self.free

    @property
    def converged(self) -> bool:
        return np.sqrt(self.rr) <= TOLERANCE * self.b_norm

    @property
    def relative_residual(self) -> float:
        return float(np.sqrt(self.rr) / self.b_norm)

    def iterate(self, n: int) -> None:
        for _ in range(n):
            if self.converged or self.iterations >= MAX_ITERATIONS:
                return
            ad = self._operator(self.direction)
            alpha = self.rr / np.sum(self.direction * ad)
            self.phi += alpha * self.direction
            self.residual -= alpha * ad
            rr_new = np.sum(self.residual**2)
            self.direction = self.residual + (rr_new / self.rr) * self.direction
            self.rr = rr_new
            self.iterations += 1


def follow_gradient(
    phi: np.ndarray, open_mask: np.ndarray, start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    """Greedy ascent to the open 4-neighbour with the largest phi, with backtracking."""
    path: list[tuple[int, int]] = [start]
    visited = {start}
    while path and path[-1] != end:
        x, y = path[-1]
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in NEIGHBOURS
            if 0 <= x + dx < phi.shape[0]
            and 0 <= y + dy < phi.shape[1]
            and open_mask[x + dx, y + dy]
            and (x + dx, y + dy) not in visited
        ]
        if neighbors:
            current = max(neighbors, key=lambda n: phi[n])
            visited.add(current)
            path.append(current)
        else:
            path.pop()  # dead end: step back
    return path


class MazeSimulation(Simulation):
    """Two phases: CG iterations for the potential, then the path cell by cell.

    Each step does one unit of work: a conjugate-gradient iteration until the
    solver converges (or reaches MAX_ITERATIONS), then the gradient-ascent
    trace, then one more visible path cell. The run is done once the whole
    path is visible.
    """

    def __init__(self, size=MAZE_SIZE, seed=SEED):
        super().__init__()
        self.maze = generate_maze(size, random.Random(seed))
        last = (size - 1) // 2 * 2  # largest even index: always a passage cell
        self.start, self.end = (0, 0), (last, last)
        self.solver = LaplaceSolver(self.maze, self.start, self.end)
        self.path: list[tuple[int, int]] | None = None
        self.visible = 0  # path cells revealed so far

    @property
    def solved(self):
        solver = self.solver
        return solver.converged or solver.iterations >= MAX_ITERATIONS

    @property
    def done(self):
        return self.path is not None and self.visible >= len(self.path)

    def step(self):
        if not self.solved:
            self.solver.iterate(1)
        elif self.path is None:
            self.path = follow_gradient(
                self.solver.phi, self.solver.open, self.start, self.end
            )
        else:
            self.visible += 1


class MazeView(View):
    """Walls black, passages blue (phi = 0) to green (phi = 1), the path in gold."""

    figsize = (7.2, 6.4)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        cmap = LinearSegmentedColormap.from_list(
            "potential", ["blue", "lime"]
        ).with_extremes(bad="black")  # walls are masked out of the potential
        self.walls = simulation.maze == 1
        self.potential = ax.imshow(
            self.potential_field(), origin="upper", cmap=cmap, vmin=0.0, vmax=1.0,
            interpolation="nearest",
        )  # fmt: skip
        self.overlay = ax.imshow(
            self.path_overlay(), origin="upper", interpolation="nearest"
        )
        figure.colorbar(self.potential, ax=ax, label="potential φ")
        for (row, col), color in (
            (simulation.start, START_COLOR),
            (simulation.end, END_COLOR),
        ):
            ax.add_patch(
                Circle((col, row), MARKER_RADIUS, facecolor=color, edgecolor="white")
            )
        # A black border as wide as the bottom and right wall rows, so the frame
        # surrounds the maze evenly and the entrance marker is not cut off.
        n = self.walls.shape[0]
        ax.set(xlim=(-2.0, n), ylim=(n, -2.0), xticks=[], yticks=[])
        ax.set_xlabel("entrance (red) to exit (green)")

    def potential_field(self):
        return np.ma.masked_array(self.simulation.solver.phi, mask=self.walls)

    def path_overlay(self):
        """RGBA image: the revealed path cells in gold, transparent elsewhere."""
        overlay = np.zeros((*self.walls.shape, 4))
        simulation = self.simulation
        if simulation.path is not None and simulation.visible > 0:
            rows, cols = np.array(simulation.path[: simulation.visible]).T
            overlay[rows, cols] = to_rgba(PATH_COLOR)
        return overlay

    def draw(self):
        self.potential.set_data(self.potential_field())
        self.overlay.set_data(self.path_overlay())

    def status(self):
        simulation = self.simulation
        solver = simulation.solver
        if simulation.path is None:
            return (
                f"CG iteration {solver.iterations}   "
                f"residual {solver.relative_residual:.0e}"
            )
        return f"path {simulation.visible} of {len(simulation.path)} cells"


ANIMATION = Animation(
    title="Laplace Equation Maze Solver",
    subtitle="Solve Laplace's equation, then walk uphill",
    filename="laplace_equation_maze_solver.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="CG iterations or revealed path cells",
)


def main(argv=None) -> None:
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, MazeSimulation(), MazeView)
    solver = simulation.solver
    if simulation.path is None:
        print(
            f"After {solver.iterations} conjugate-gradient iterations the relative "
            f"residual is {solver.relative_residual:.1e}; no path traced yet."
        )
    else:
        print(
            f"Potential solved after {solver.iterations} conjugate-gradient "
            f"iterations. Path from {simulation.start} to {simulation.end}: "
            f"{len(simulation.path)} cells, {simulation.visible} shown."
        )


if __name__ == "__main__":
    main()
