import pygame
import numpy as np

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SIM_HEIGHT = 1.1
GRAVITY = 0.0  # Gravity turned off
DELTA_TIME = 1.0 / 60.0
NUM_ITERATIONS = 20
OVER_RELAXATION = 1.9
OBSTACLE_RADIUS = 0.15
DENSITY = 1000.0

# Helper functions
def canvas_x(x, scale):
    return x * scale

def canvas_y(y, canvas_height, scale):
    return canvas_height - y * scale

def get_sci_color(value, min_val, max_val):
    value = min(max(value, min_val), max_val - 0.0001)
    delta = max_val - min_val
    normalized_value = (value - min_val) / delta if delta != 0 else 0.5
    segment = 0.25
    colors = [
        (173, 216, 230),  # Light blue
        (100, 149, 237),  # Cornflower blue
        (70, 130, 180),   # Steel blue
        (144, 238, 144)   # Light green
    ]

    color_index = int(normalized_value / segment)
    r, g, b = colors[color_index]

    return r, g, b, 255

class FluidSimulator:
    def __init__(self, density, grid_width, grid_height, cell_size):
        self.density = density
        self.grid_width = grid_width + 2
        self.grid_height = grid_height + 2
        self.num_cells = self.grid_width * self.grid_height
        self.cell_size = cell_size
        self.u = np.zeros(self.num_cells, dtype=np.float32)
        self.v = np.zeros(self.num_cells, dtype=np.float32)
        self.new_u = np.zeros(self.num_cells, dtype=np.float32)
        self.new_v = np.zeros(self.num_cells, dtype=np.float32)
        self.pressure = np.zeros(self.num_cells, dtype=np.float32)
        self.solid = np.ones(self.num_cells, dtype=np.float32)
        self.density_field = np.ones(self.num_cells, dtype=np.float32)
        self.new_density_field = np.zeros(self.num_cells, dtype=np.float32)

    def integrate(self, delta_time, gravity):
        n = self.grid_height
        for i in range(1, self.grid_width):
            for j in range(1, self.grid_height - 1):
                if self.solid[i * n + j] != 0.0 and self.solid[i * n + j - 1] != 0.0:
                    self.v[i * n + j] += gravity * delta_time

    def solve_incompressibility(self, num_iterations, delta_time, density_constant, over_relaxation):
        n = self.grid_height
        for _ in range(num_iterations):
            for i in range(1, self.grid_width - 1):
                for j in range(1, self.grid_height - 1):
                    if self.solid[i * n + j] == 0.0:
                        continue

                    s = (self.solid[(i - 1) * n + j] + self.solid[(i + 1) * n + j] +
                         self.solid[i * n + j - 1] + self.solid[i * n + j + 1])
                    if s == 0.0:
                        continue

                    divergence = (self.u[(i + 1) * n + j] - self.u[i * n + j] +
                                  self.v[i * n + j + 1] - self.v[i * n + j])

                    pressure = -divergence / s
                    pressure *= over_relaxation
                    self.pressure[i * n + j] += density_constant * pressure

                    self.u[i * n + j] -= self.solid[(i - 1) * n + j] * pressure
                    self.u[(i + 1) * n + j] += self.solid[(i + 1) * n + j] * pressure
                    self.v[i * n + j] -= self.solid[i * n + j - 1] * pressure
                    self.v[i * n + j + 1] += self.solid[i * n + j + 1] * pressure

    def extrapolate(self):
        n = self.grid_height
        self.u[:n] = self.u[n:2 * n]
        self.u[-n:] = self.u[-2 * n:-n]
        self.v[:n] = self.v[n:2 * n]
        self.v[-n:] = self.v[-2 * n:-n]

    def sample_field(self, x, y, field_type):
        n = self.grid_height
        h = self.cell_size
        inv_h = 1.0 / h
        half_h = 0.5 * h

        x = min(max(x, h), self.grid_width * h)
        y = min(max(y, h), self.grid_height * h)

        dx, dy = 0.0, 0.0

        if field_type == 'U_FIELD':
            field = self.u
            dy = half_h
        elif field_type == 'V_FIELD':
            field = self.v
            dx = half_h
        elif field_type == 'DENSITY_FIELD':
            field = self.density_field
            dx = dy = half_h

        x0 = min(int((x - dx) * inv_h), self.grid_width - 1)
        tx = ((x - dx) - x0 * h) * inv_h
        x1 = min(x0 + 1, self.grid_width - 1)

        y0 = min(int((y - dy) * inv_h), self.grid_height - 1)
        ty = ((y - dy) - y0 * h) * inv_h
        y1 = min(y0 + 1, self.grid_height - 1)

        sx, sy = 1.0 - tx, 1.0 - ty

        value = (sx * sy * field[x0 * n + y0] +
                 tx * sy * field[x1 * n + y0] +
                 tx * ty * field[x1 * n + y1] +
                 sx * ty * field[x0 * n + y1])

        return value

    def advect(self, delta_time):
        n = self.grid_height
        self.new_u[:] = self.u
        self.new_v[:] = self.v

        for i in range(1, self.grid_width):
            for j in range(1, self.grid_height):
                if self.solid[i * n + j] != 0.0 and self.solid[(i - 1) * n + j] != 0.0 and j < self.grid_height - 1:
                    x = i * self.cell_size
                    y = j * self.cell_size + 0.5 * self.cell_size
                    u = self.u[i * n + j]
                    v = self.sample_field(x, y, 'V_FIELD')
                    x -= delta_time * u
                    y -= delta_time * v
                    self.new_u[i * n + j] = self.sample_field(x, y, 'U_FIELD')

                if self.solid[i * n + j] != 0.0 and self.solid[i * n + j - 1] != 0.0 and i < self.grid_width - 1:
                    x = i * self.cell_size + 0.5 * self.cell_size
                    y = j * self.cell_size
                    u = self.sample_field(x, y, 'U_FIELD')
                    v = self.v[i * n + j]
                    x -= delta_time * u
                    y -= delta_time * v
                    self.new_v[i * n + j] = self.sample_field(x, y, 'V_FIELD')

        self.u[:] = self.new_u
        self.v[:] = self.new_v

    def advect_density(self, delta_time):
        n = self.grid_height
        self.new_density_field[:] = self.density_field

        for i in range(1, self.grid_width - 1):
            for j in range(1, self.grid_height - 1):
                if self.solid[i * n + j] != 0.0:
                    u = 0.5 * (self.u[i * n + j] + self.u[(i + 1) * n + j])
                    v = 0.5 * (self.v[i * n + j] + self.v[i * n + j + 1])
                    x = i * self.cell_size + 0.5 * self.cell_size - delta_time * u
                    y = j * self.cell_size + 0.5 * self.cell_size - delta_time * v
                    self.new_density_field[i * n + j] = self.sample_field(x, y, 'DENSITY_FIELD')

        self.density_field[:] = self.new_density_field

    def simulate(self, delta_time, gravity, num_iterations, density_constant, over_relaxation):
        self.integrate(delta_time, gravity)
        self.pressure.fill(0.0)
        self.solve_incompressibility(num_iterations, delta_time, density_constant, over_relaxation)
        self.extrapolate()
        self

.advect(delta_time)
        self.advect_density(delta_time)

    def set_obstacle(self, x, y, radius, velocity_x=0.0, velocity_y=0.0):
        n = self.grid_height
        for i in range(1, self.grid_width - 2):
            for j in range(1, self.grid_height - 2):
                self.solid[i * n + j] = 1.0
                dx = (i + 0.5) * self.cell_size - x
                dy = (j + 0.5) * self.cell_size - y
                if dx * dx + dy * dy < radius * radius:
                    self.solid[i * n + j] = 0.0
                    self.density_field[i * n + j] = 1.0
                    self.u[i * n + j] = velocity_x
                    self.u[(i + 1) * n + j] = velocity_x
                    self.v[i * n + j] = velocity_y
                    self.v[i * n + j + 1] = velocity_y

def setup_scene(scene_number=0):
    resolution = 100 if scene_number != 0 else 50
    domain_height = 1.0
    domain_width = domain_height / SIM_HEIGHT * (WINDOW_WIDTH / WINDOW_HEIGHT)
    cell_size = domain_height / resolution
    grid_width = int(domain_width / cell_size)
    grid_height = int(domain_height / cell_size)

    fluid = FluidSimulator(DENSITY, grid_width, grid_height, cell_size)

    n = fluid.grid_height
    if scene_number == 0:  # Tank
        for i in range(fluid.grid_width):
            for j in range(fluid.grid_height):
                fluid.solid[i * n + j] = 1.0 if i != 0 and i != fluid.grid_width - 1 and j != 0 else 0.0
    else:  # Vortex shedding
        inlet_velocity = 2.0
        for i in range(fluid.grid_width):
            for j in range(fluid.grid_height):
                fluid.solid[i * n + j] = 1.0 if i != 0 and j != 0 and j != fluid.grid_height - 1 else 0.0
                if i == 1:
                    fluid.u[i * n + j] = inlet_velocity

        pipe_height = 0.1 * fluid.grid_height
        min_j = int(0.5 * fluid.grid_height - 0.5 * pipe_height)
        max_j = int(0.5 * fluid.grid_height + 0.5 * pipe_height)
        for j in range(min_j, max_j):
            fluid.density_field[j] = 0.0

    return fluid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    canvas_scale = WINDOW_HEIGHT / SIM_HEIGHT
    density_constant = DENSITY * canvas_scale / DELTA_TIME

    fluid = setup_scene(1)
    fluid.set_obstacle(0.4, 0.5, OBSTACLE_RADIUS)

    running = True
    paused = False
    frame_number = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_m:
                    paused = False
                    fluid.simulate(DELTA_TIME, GRAVITY, NUM_ITERATIONS, density_constant, OVER_RELAXATION)
                    paused = True

        if not paused:
            fluid.simulate(DELTA_TIME, GRAVITY, NUM_ITERATIONS, density_constant, OVER_RELAXATION)
            frame_number += 1

        screen.fill((240, 248, 255))  # Alice blue background
        for i in range(fluid.grid_width):
            for j in range(fluid.grid_height):
                color = (240, 248, 255)  # Alice blue
                if fluid.solid[i * fluid.grid_height + j] == 0.0:
                    color = (47, 79, 79)  # Dark slate gray for obstacles
                elif fluid.density_field[i * fluid.grid_height + j] != 0.0:
                    color = get_sci_color(fluid.density_field[i * fluid.grid_height + j], 0.0, 1.0)

                x = int(canvas_x(i * fluid.cell_size, canvas_scale))
                y = int(canvas_y((j + 1) * fluid.cell_size, WINDOW_HEIGHT, canvas_scale))
                pygame.draw.rect(screen, color, (x, y, int(canvas_scale * fluid.cell_size), int(canvas_scale * fluid.cell_size)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

