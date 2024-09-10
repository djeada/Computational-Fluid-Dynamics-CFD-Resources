import numpy as np
import random
import pygame
from typing import List, Tuple

# Constants
MAZE_SIZE: int = 100
CELL_SIZE: int = 8
DT: float = 0.1
MAX_ITERATIONS: int = 5000
TOLERANCE: float = 1e-6
SCREEN_COLOR: Tuple[int, int, int] = (255, 255, 255)
WALL_COLOR: Tuple[int, int, int] = (0, 0, 0)
PATH_COLOR: Tuple[int, int, int] = (255, 215, 0)
START_COLOR: Tuple[int, int, int] = (255, 0, 0)
END_COLOR: Tuple[int, int, int] = (0, 255, 0)

def generate_maze(size: int) -> np.ndarray:
    print("Generating maze...")
    maze = np.ones((size, size), dtype=int)
    stack: List[Tuple[int, int]] = []
    start: Tuple[int, int] = (0, 0)
    maze[start] = 0
    stack.append(start)
    directions: List[Tuple[int, int]] = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        current = stack[-1]
        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in directions if
                     0 <= x + dx < size and 0 <= y + dy < size and maze[x + dx, y + dy] == 1]
        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            maze[(x + nx) // 2, (y + ny) // 2] = 0
            maze[nx, ny] = 0
            stack.append(next_cell)
        else:
            stack.pop()
    print("Maze generated.")
    return maze


def set_boundary_conditions(maze: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> np.ndarray:
    print(f"Setting boundary conditions. Start: {start}, End: {end}")
    phi = np.full_like(maze, 0, dtype=float)
    phi[maze == 1] = -1  # Walls have -1 potential
    phi[start] = 0  # Start has potential 0
    phi[end] = 1  # End has potential 1
    print("Boundary conditions set.")
    return phi


def solve_laplace_step(phi: np.ndarray, maze: np.ndarray, dt: float = DT) -> Tuple[np.ndarray, float]:
    laplace_update = (
        np.roll(a=phi, shift=1, axis=0) + np.roll(a=phi, shift=-1, axis=0) +
        np.roll(a=phi, shift=1, axis=1) + np.roll(a=phi, shift=-1, axis=1)
    ) / 4
    mask = (maze == 0)
    phi_new = np.where(mask, phi + dt * (laplace_update - phi), phi)
    phi_new = np.clip(phi_new, -1, 1)  # Enforce bounds to prevent overflow or underflow
    max_change = np.abs(phi_new - phi).max()
    phi[:] = phi_new
    return phi, max_change


def follow_gradient(phi: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    print("Following gradient to find path...")
    path: List[Tuple[int, int]] = [start]
    stack: List[Tuple[int, int]] = [start]
    visited: set = set()
    current = start

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while current != end:
        x, y = current
        visited.add(current)

        neighbors = [(x + dx, y + dy) for dx, dy in directions if
                     0 <= x + dx < phi.shape[0] and 0 <= y + dy < phi.shape[1] and (x + dx, y + dy) not in visited]

        neighbors = [(nx, ny) for nx, ny in neighbors if phi[nx, ny] > -1]

        if not neighbors:
            if stack:
                current = stack.pop()
                path.pop()
            else:
                print("No path found, backtracked fully.")
                return path
        else:
            current = max(neighbors, key=lambda n: phi[n])
            path.append(current)
            stack.append(current)

    return path


def draw_maze(screen: pygame.Surface, maze: np.ndarray, phi: np.ndarray, path: List[Tuple[int, int]],
              cell_size: int, start: Tuple[int, int], end: Tuple[int, int], visible_path_length: int) -> None:
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                color = WALL_COLOR
            else:
                potential = (phi[i, j] + 1) / 2  # Normalize phi to [0, 1]
                b = int(255 * (1 - potential))  # Blue for low potential
                g = int(255 * potential)        # Green for high potential
                color = (0, g, b)               # Smooth transition from blue to green
            pygame.draw.rect(screen, color, pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size))

    # Draw only the visible portion of the path
    visible_path = path[:visible_path_length]
    for point in visible_path:
        pygame.draw.rect(screen, PATH_COLOR, pygame.Rect(point[1] * cell_size, point[0] * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, START_COLOR, pygame.Rect(start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, END_COLOR, pygame.Rect(end[1] * cell_size, end[0] * cell_size, cell_size, cell_size))


def main() -> None:
    print("Starting maze solver...")
    maze = generate_maze(size=MAZE_SIZE)
    start, end = (1, 1), (MAZE_SIZE - 2, MAZE_SIZE - 2)
    phi = set_boundary_conditions(maze=maze, start=start, end=end)

    pygame.init()
    screen = pygame.display.set_mode((MAZE_SIZE * CELL_SIZE, MAZE_SIZE * CELL_SIZE))
    pygame.display.set_caption("Interactive Maze Solver")
    clock = pygame.time.Clock()

    running = True
    iterations = 0
    max_change = TOLERANCE + 1
    visible_path_length = 1  # Start by revealing just the first step
    path = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if max_change > TOLERANCE and iterations < MAX_ITERATIONS:
            phi, max_change = solve_laplace_step(phi=phi, maze=maze)
            iterations += 1

        if iterations % 5 == 0:  # Update path after a few iterations
            path = follow_gradient(phi=phi, start=start, end=end)

        # Increase the visible portion of the path gradually
        visible_path_length = min(visible_path_length + 1, len(path))

        screen.fill(SCREEN_COLOR)
        draw_maze(screen=screen, maze=maze, phi=phi, path=path, cell_size=CELL_SIZE, start=start, end=end,
                  visible_path_length=visible_path_length)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print("Maze solver finished.")


if __name__ == "__main__":
    main()
