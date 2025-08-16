import pygame
import numpy as np


class FluidSimulation:
    def __init__(self, width, height, diffusion, viscosity, dt):
        self.size = (height, width)
        self.dt = dt
        self.diff = diffusion
        self.visc = viscosity

        self.s = np.zeros(self.size)
        self.density = np.zeros(self.size)

        self.Vx = np.zeros(self.size)
        self.Vy = np.zeros(self.size)

        self.Vx0 = np.zeros(self.size)
        self.Vy0 = np.zeros(self.size)

    def add_density(self, x, y, amount):
        self.density[y, x] += amount

    def add_velocity(self, x, y, amountX, amountY):
        self.Vx[y, x] += amountX
        self.Vy[y, x] += amountY

    def diffuse(self, b, x, x0, diff):
        a = self.dt * diff * (self.size[1] - 2) * (self.size[0] - 2)
        for _ in range(20):
            x[1:-1, 1:-1] = (
                x0[1:-1, 1:-1]
                + a * (x[:-2, 1:-1] + x[2:, 1:-1] + x[1:-1, :-2] + x[1:-1, 2:])
            ) / (1 + 4 * a)
            self.set_bnd(b, x)

    def advect(self, b, d, d0, Vx, Vy):
        dt0 = self.dt * (self.size[1] - 2)

        rows, cols = np.indices((self.size[0] - 2, self.size[1] - 2)) + 1
        x = cols - dt0 * Vx[1:-1, 1:-1]
        y = rows - dt0 * Vy[1:-1, 1:-1]

        x = np.clip(x, 0.5, self.size[1] - 1.5)
        y = np.clip(y, 0.5, self.size[0] - 1.5)

        i0 = x.astype(int)
        i1 = i0 + 1
        j0 = y.astype(int)
        j1 = j0 + 1

        s1 = x - i0
        s0 = 1 - s1
        t1 = y - j0
        t0 = 1 - t1

        d[1:-1, 1:-1] = s0 * (t0 * d0[j0, i0] + t1 * d0[j1, i0]) + s1 * (
            t0 * d0[j0, i1] + t1 * d0[j1, i1]
        )

        self.set_bnd(b, d)

    def project(self, Vx, Vy, p, div):
        h = 1.0 / self.size[1]
        div[1:-1, 1:-1] = (
            -0.5 * h * (Vx[1:-1, 2:] - Vx[1:-1, :-2] + Vy[2:, 1:-1] - Vy[:-2, 1:-1])
        )
        p[1:-1, 1:-1] = 0
        self.set_bnd(0, div)
        self.set_bnd(0, p)

        for _ in range(20):
            p[1:-1, 1:-1] = (
                div[1:-1, 1:-1]
                + p[:-2, 1:-1]
                + p[2:, 1:-1]
                + p[1:-1, :-2]
                + p[1:-1, 2:]
            ) / 4
            self.set_bnd(0, p)

        Vx[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) / h
        Vy[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) / h
        self.set_bnd(1, Vx)
        self.set_bnd(2, Vy)

    def set_bnd(self, b, x):
        for i in range(1, self.size[0] - 1):
            if b == 1:
                x[i, 0] = -x[i, 1]
                x[i, self.size[1] - 1] = -x[i, self.size[1] - 2]
            else:
                x[i, 0] = x[i, 1]
                x[i, self.size[1] - 1] = x[i, self.size[1] - 2]

        for j in range(1, self.size[1] - 1):
            if b == 2:
                x[0, j] = -x[1, j]
                x[self.size[0] - 1, j] = -x[self.size[0] - 2, j]
            else:
                x[0, j] = x[1, j]
                x[self.size[0] - 1, j] = x[self.size[0] - 2, j]

        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, self.size[1] - 1] = 0.5 * (x[1, self.size[1] - 1] + x[0, self.size[1] - 2])
        x[self.size[0] - 1, 0] = 0.5 * (x[self.size[0] - 2, 0] + x[self.size[0] - 1, 1])
        x[self.size[0] - 1, self.size[1] - 1] = 0.5 * (
            x[self.size[0] - 2, self.size[1] - 1]
            + x[self.size[0] - 1, self.size[1] - 2]
        )

    def dens_step(self):
        self.diffuse(0, self.s, self.density, self.diff)
        self.advect(0, self.density, self.s, self.Vx, self.Vy)

    def vel_step(self):
        self.diffuse(1, self.Vx0, self.Vx, self.visc)
        self.diffuse(2, self.Vy0, self.Vy, self.visc)

        self.project(self.Vx0, self.Vy0, self.Vx, self.Vy)

        self.advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0)
        self.advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0)

        self.project(self.Vx, self.Vy, self.Vx0, self.Vy0)

    def step(self):
        self.vel_step()
        self.dens_step()


def initialize_pygame(screen_size):
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Fluid Simulation")
    return screen


def handle_events(fluid_sim, cell_size, grid_width, grid_height, screen_size):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size
            print(
                f"Mouse Clicked at: ({mouse_x}, {mouse_y}), Grid Coords: ({grid_x}, {grid_y})"
            )
            if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                fluid_sim.add_density(grid_x, grid_y, 1000)
                fluid_sim.add_velocity(
                    grid_x,
                    grid_y,
                    np.random.uniform(-200, 200),
                    np.random.uniform(-200, 200),
                )
    return False


def draw_simulation(screen, fluid_sim, screen_size):
    screen.fill((0, 0, 0))
    density_scaled = np.clip(fluid_sim.density * 1000, 0, 255).astype(np.uint8)

    # Transpose the density array to match Pygame's coordinate system
    density_scaled = np.transpose(density_scaled)

    color_surface = np.zeros((*density_scaled.shape, 3), dtype=np.uint8)
    color_surface[:, :, 2] = density_scaled  # Using blue channel
    density_surface = pygame.surfarray.make_surface(color_surface)
    density_surface = pygame.transform.scale(density_surface, screen_size)
    screen.blit(density_surface, (0, 0))
    pygame.display.flip()


def main():
    screen_size = (800, 600)
    cell_size = 4
    grid_width, grid_height = screen_size[0] // cell_size, screen_size[1] // cell_size
    fluid_sim = FluidSimulation(
        width=grid_width, height=grid_height, diffusion=0.0001, viscosity=0.0001, dt=0.1
    )

    screen = initialize_pygame(screen_size)
    clock = pygame.time.Clock()
    done = False

    while not done:
        done = handle_events(fluid_sim, cell_size, grid_width, grid_height, screen_size)
        fluid_sim.step()
        draw_simulation(screen, fluid_sim, screen_size)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
