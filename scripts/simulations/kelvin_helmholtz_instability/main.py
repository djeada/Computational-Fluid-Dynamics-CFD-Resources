import numpy as np
import pygame
import sys

# Simulation parameters
temp_width, temp_height = 400, 400
screen_width, screen_height = 400, 600
cell_width = screen_width // temp_width
cell_height = screen_height // temp_height
dx, dy = 1.0, 1.0
dt = 0.005
diffusion_rate = 0.0001
viscosity = 0.0001

# Flag to draw or hide grid lines
draw_grid = False

# Initialize fields
temperature = np.zeros((temp_height, temp_width))
temperature[:, temp_width - 1] = 0  # Initial cold region on the right
temperature[:, : temp_width // 4] = 100  # Initial hot region on the left

u = np.zeros((temp_height, temp_width))  # x-component of velocity
v = np.zeros((temp_height, temp_width))  # y-component of velocity

# Introduce initial perturbations in the velocity field
perturbation_amplitude = 1.0
frequency = 3

for j in range(temp_width):
    random_factor = np.random.uniform(0, 300)
    peak_length_factor = np.random.uniform(0, 300)
    for i in range(temp_height):
        adjusted_i = int(i * peak_length_factor) % temp_height
        u[i, j] = (
            perturbation_amplitude
            * random_factor
            * np.sin(frequency * np.pi * adjusted_i / temp_height)
            * np.cos(frequency * np.pi * j / temp_width)
        )
        v[i, j] = (
            perturbation_amplitude
            * random_factor
            * np.cos(frequency * np.pi * adjusted_i / temp_height)
            * np.sin(frequency * np.pi * j / temp_width)
        )

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kelvin-Helmholtz Instability Simulation")


# Color mapping
def temperature_to_color(temp, min_temp, max_temp):
    norm_temp = (
        (temp - min_temp) / (max_temp - min_temp)
        if max_temp > min_temp
        else np.zeros_like(temp)
    )
    color = pygame.Color(0)
    color.hsva = (240 * (1 - norm_temp), 100, 100)
    return color


# Velocity and temperature update functions
def advect(field, u, v):
    field_new = np.empty_like(field)

    # Calculate positions from which to sample
    j_indices, i_indices = np.meshgrid(np.arange(temp_width), np.arange(temp_height))

    x = j_indices - u * dt / dx
    y = i_indices - v * dt / dy

    x = (x + temp_width) % temp_width
    y = (y + temp_height) % temp_height

    j0 = np.floor(x).astype(int)
    i0 = np.floor(y).astype(int)
    j1 = (j0 + 1) % temp_width
    i1 = (i0 + 1) % temp_height

    s1 = x - j0
    t1 = y - i0
    s0 = 1 - s1
    t0 = 1 - t1

    field_new[1:-1, 1:-1] = s0[1:-1, 1:-1] * (
        t0[1:-1, 1:-1] * field[i0[1:-1, 1:-1], j0[1:-1, 1:-1]]
        + t1[1:-1, 1:-1] * field[i1[1:-1, 1:-1], j0[1:-1, 1:-1]]
    ) + s1[1:-1, 1:-1] * (
        t0[1:-1, 1:-1] * field[i0[1:-1, 1:-1], j1[1:-1, 1:-1]]
        + t1[1:-1, 1:-1] * field[i1[1:-1, 1:-1], j1[1:-1, 1:-1]]
    )

    # Handle boundary conditions if necessary
    field_new[0, :] = field_new[1, :]
    field_new[-1, :] = field_new[-2, :]
    field_new[:, 0] = field_new[:, 1]
    field_new[:, -1] = field_new[:, -2]

    return field_new


def diffuse(field, rate):
    field_new = field.copy()
    laplacian = (
        field[:-2, 1:-1] + field[2:, 1:-1] - 2 * field[1:-1, 1:-1]
    ) / dx**2 + (field[1:-1, :-2] + field[1:-1, 2:] - 2 * field[1:-1, 1:-1]) / dy**2
    field_new[1:-1, 1:-1] += rate * dt * laplacian

    # Handle boundary conditions if necessary
    field_new[0, :] = field_new[1, :]
    field_new[-1, :] = field_new[-2, :]
    field_new[:, 0] = field_new[:, 1]
    field_new[:, -1] = field_new[:, -2]

    return field_new


def project(u, v):
    p = np.zeros_like(u)
    div = np.zeros_like(u)
    div[1:-1, 1:-1] = -0.5 * (
        (u[1:-1, 2:] - u[1:-1, :-2]) / dx + (v[2:, 1:-1] - v[:-2, 1:-1]) / dy
    )
    for _ in range(20):
        p[1:-1, 1:-1] = (
            div[1:-1, 1:-1] + p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2]
        ) / 4
    u[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) / dx
    v[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) / dy
    return u, v


def update_fields(u, v, temperature):
    u = advect(u, u, v)
    v = advect(v, u, v)
    u, v = project(u, v)
    u = diffuse(u, viscosity)
    v = diffuse(v, viscosity)
    temperature = advect(temperature, u, v)
    temperature = diffuse(temperature, diffusion_rate)
    return u, v, temperature


# Main loop
running = True
iteration = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update velocity and temperature fields
    u, v, temperature = update_fields(u, v, temperature)

    # Render the temperature field
    min_temp = np.min(temperature)
    max_temp = np.max(temperature)
    for i in range(temp_height):
        for j in range(temp_width):
            color = temperature_to_color(temperature[i, j], min_temp, max_temp)
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height),
            )
            if draw_grid:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    pygame.Rect(
                        j * cell_width, i * cell_height, cell_width, cell_height
                    ),
                    1,
                )  # Draw grid lines

    pygame.display.flip()
    pygame.time.wait(10)  # Adjust the delay to slow down the simulation

    iteration += 1

pygame.quit()
sys.exit()
