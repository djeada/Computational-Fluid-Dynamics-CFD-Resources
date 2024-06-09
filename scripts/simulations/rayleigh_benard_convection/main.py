import pygame
import numpy as np
from multiprocessing import Pool, cpu_count

# Simulation parameters
GRID_SIZE = 128
WINDOW_SIZE = 400
FPS = 60
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
MAX_TEMP = 1.0
MIN_TEMP = 0.0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Rayleigh Bénard Convection')
clock = pygame.time.Clock()

# Function to convert a value to a color
def value_to_color(value):
    # Clamp value to be between 0 and 1
    value = max(0, min(1, value))
    # Map the value to a color from blue to red through cyan and yellow
    if value < 0.25:
        r = 0
        g = int(255 * (value / 0.25))
        b = 255
    elif value < 0.5:
        r = 0
        g = 255
        b = int(255 * (1 - (value - 0.25) / 0.25))
    elif value < 0.75:
        r = int(255 * ((value - 0.5) / 0.25))
        g = 255
        b = 0
    else:
        r = 255
        g = int(255 * (1 - (value - 0.75) / 0.25))
        b = 0

    # Clamp values to be between 0 and 255
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)

# Initialize the grid with a temperature gradient
def initialize_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    for i in range(GRID_SIZE):
        grid[i, :] = 1 - (i / GRID_SIZE)
    return grid

# Update function to be used by multiprocessing
def update_cell(args):
    grid, vel_x, vel_y, i, j = args
    if 1 <= i < GRID_SIZE - 1 and 1 <= j < GRID_SIZE - 1:
        # Simplified thermal convection model
        temp_change = (
            grid[i-1, j] + grid[i+1, j] + grid[i, j-1] + grid[i, j+1]
            - 4 * grid[i, j]
        ) * 0.1  # Simplified thermal diffusion
        # Add velocity influence
        temp_change += -vel_x[i, j] * (grid[i, j] - grid[i, j-1]) - vel_y[i, j] * (grid[i, j] - grid[i-1, j])
        new_temp = grid[i, j] + temp_change + (np.random.rand() - 0.5) * 0.01
        # Clamp temperature values to prevent overflow
        new_temp = max(MIN_TEMP, min(MAX_TEMP, new_temp))
        return new_temp
    return grid[i, j]

# Update the grid using multiprocessing
def update_grid(grid, vel_x, vel_y):
    args = [(grid, vel_x, vel_y, i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    with Pool(cpu_count()) as pool:
        results = pool.map(update_cell, args)
    new_grid = np.array(results).reshape(GRID_SIZE, GRID_SIZE)
    return new_grid

# Update velocity fields based on temperature gradient
def update_velocity(grid, vel_x, vel_y):
    new_vel_x = vel_x.copy()
    new_vel_y = vel_y.copy()
    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):
            new_vel_x[i, j] = vel_x[i, j] + (grid[i, j] - grid[i, j-1]) * 0.01
            new_vel_y[i, j] = vel_y[i, j] + (grid[i, j] - grid[i-1, j]) * 0.01
    return new_vel_x, new_vel_y

# Draw the grid on the screen
def draw_grid(screen, grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color_value = grid[i, j]
            color = value_to_color(color_value)
            pygame.draw.rect(screen, color, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main loop
def main():
    grid = initialize_grid()
    vel_x = np.zeros((GRID_SIZE, GRID_SIZE))
    vel_y = np.zeros((GRID_SIZE, GRID_SIZE))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        vel_x, vel_y = update_velocity(grid, vel_x, vel_y)
        grid = update_grid(grid, vel_x, vel_y)
        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
