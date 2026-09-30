"""Solve a random maze with Laplace's equation and follow the potential gradient.

A perfect maze is carved with a seeded depth-first backtracker. Laplace's
equation is solved on the open cells with phi = 0 at the entrance, phi = 1 at
the exit and insulating (zero-flux) walls, using conjugate-gradient iterations
that are animated in Pygame. The route is then traced by stepping to the
neighbour with the largest potential and revealed one cell per frame.
"""

import os
import random
import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int  # noqa: E402

# Constants
MAZE_SIZE: int = 100  # grid cells per side (walls and passages)
CELL_SIZE: int = 8  # pixels per grid cell
SEED: int = 0
CG_ITERATIONS_PER_FRAME: int = 25  # solver iterations drawn per frame
MAX_ITERATIONS: int = 50_000  # cap on conjugate-gradient iterations
TOLERANCE: float = 1e-10  # stop when ||residual|| / ||b|| < TOLERANCE
FPS: int = 30
SCREEN_COLOR: tuple[int, int, int] = (255, 255, 255)
WALL_COLOR: tuple[int, int, int] = (0, 0, 0)
PATH_COLOR: tuple[int, int, int] = (255, 215, 0)
START_COLOR: tuple[int, int, int] = (255, 0, 0)
END_COLOR: tuple[int, int, int] = (0, 255, 0)

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


def draw_maze(
    screen, pygame, maze, phi, path, cell_size, start, end, visible_path_length
):
    """Walls black, open cells from blue (phi = 0) to green (phi = 1), path in gold."""
    potential = np.clip(phi, 0.0, 1.0)
    rgb = np.zeros((*maze.shape, 3), dtype=np.uint8)
    rgb[..., 1] = (255 * potential).astype(np.uint8)
    rgb[..., 2] = (255 * (1 - potential)).astype(np.uint8)
    rgb[maze == 1] = WALL_COLOR
    for point in path[:visible_path_length]:
        rgb[point] = PATH_COLOR
    rgb[start] = START_COLOR
    rgb[end] = END_COLOR
    surface = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))
    screen.blit(
        pygame.transform.scale(
            surface, (maze.shape[1] * cell_size, maze.shape[0] * cell_size)
        ),
        (0, 0),
    )


def main(argv=None) -> None:
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help=f"frames to run; each frame does {CG_ITERATIONS_PER_FRAME} solver "
        "iterations, or reveals one path cell once solved (default: until closed)",
    )
    args = parser.parse_args(argv)

    if args.no_show:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    import pygame

    maze = generate_maze(MAZE_SIZE, random.Random(SEED))
    last = (MAZE_SIZE - 1) // 2 * 2  # largest even index: always a passage cell
    start, end = (0, 0), (last, last)
    solver = LaplaceSolver(maze, start, end)

    pygame.init()
    try:
        screen = pygame.display.set_mode((MAZE_SIZE * CELL_SIZE, MAZE_SIZE * CELL_SIZE))
        pygame.display.set_caption("Interactive Maze Solver")
        clock = pygame.time.Clock()
        path: list[tuple[int, int]] = []
        visible_path_length = 0
        frame = 0

        while args.steps is None or frame < args.steps:
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break

            if not solver.converged and solver.iterations < MAX_ITERATIONS:
                solver.iterate(CG_ITERATIONS_PER_FRAME)
            elif not path:
                print(
                    f"Potential solved after {solver.iterations} conjugate-gradient "
                    "iterations."
                )
                path = follow_gradient(solver.phi, solver.open, start, end)
                print(f"Path from {start} to {end}: {len(path)} cells.")
            else:
                visible_path_length = min(visible_path_length + 1, len(path))

            screen.fill(SCREEN_COLOR)
            draw_maze(
                screen, pygame, maze, solver.phi, path, CELL_SIZE, start, end,
                visible_path_length,
            )  # fmt: skip
            pygame.display.flip()
            if not args.no_show:
                clock.tick(FPS)
            frame += 1

        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            pygame.image.save(
                screen, str(args.output / "laplace_equation_maze_solver.png")
            )
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
