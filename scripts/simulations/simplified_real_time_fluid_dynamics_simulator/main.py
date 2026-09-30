"""Interactive 2D smoke simulation with Jos Stam's Stable Fluids method in Pygame.

Velocity and a passive density field live on a collocated grid inside a closed
box. Each frame diffuses (Jacobi iterations of the implicit system), projects,
semi-Lagrangian-advects and projects the velocity again, then diffuses and
advects the density. Left-click to inject density and a random velocity kick;
with ``--no-show`` (or ``--auto-inject``) a seeded rising, swaying plume is
injected automatically instead.
"""

import os
import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int  # noqa: E402

SEED = 0
SCREEN_SIZE = (800, 600)  # pixels
CELL_SIZE = 4  # pixels per grid cell -> 200 x 150 grid
DIFFUSION = 0.0001  # density diffusion coefficient
VISCOSITY = 0.0001  # kinematic viscosity
TIME_STEP = 0.1
SOLVER_ITERATIONS = 20  # Jacobi iterations for diffusion and pressure
CLICK_DENSITY = 1000  # density added by a mouse click
CLICK_VELOCITY = 200  # maximum random velocity component added by a click
PLUME_DENSITY = 0.25  # density added per source cell per frame (scripted plume)
PLUME_VELOCITY = 0.15  # upward velocity added per source cell per frame
PLUME_SWAY = 0.08  # amplitude of the sideways velocity added per frame
FPS = 60


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
        """Implicit diffusion (I - a lap) x = x0 solved with Jacobi iterations."""
        a = self.dt * diff * (self.size[1] - 2) * (self.size[0] - 2)
        for _ in range(SOLVER_ITERATIONS):
            x[1:-1, 1:-1] = (
                x0[1:-1, 1:-1]
                + a * (x[:-2, 1:-1] + x[2:, 1:-1] + x[1:-1, :-2] + x[1:-1, 2:])
            ) / (1 + 4 * a)
            self.set_bnd(b, x)

    def advect(self, b, d, d0, Vx, Vy):
        """Semi-Lagrangian advection with bilinear interpolation."""
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
        """Make (Vx, Vy) divergence-free; p and div are scratch arrays."""
        h = 1.0 / self.size[1]
        div[1:-1, 1:-1] = (
            -0.5 * h * (Vx[1:-1, 2:] - Vx[1:-1, :-2] + Vy[2:, 1:-1] - Vy[:-2, 1:-1])
        )
        p[1:-1, 1:-1] = 0
        self.set_bnd(0, div)
        self.set_bnd(0, p)

        for _ in range(SOLVER_ITERATIONS):
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
        """Walls: b = 1 reflects Vx at the side walls, b = 2 reflects Vy at top/bottom."""
        sign_x = -1.0 if b == 1 else 1.0
        sign_y = -1.0 if b == 2 else 1.0
        x[1:-1, 0] = sign_x * x[1:-1, 1]
        x[1:-1, -1] = sign_x * x[1:-1, -2]
        x[0, 1:-1] = sign_y * x[1, 1:-1]
        x[-1, 1:-1] = sign_y * x[-2, 1:-1]

        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, -1] = 0.5 * (x[1, -1] + x[0, -2])
        x[-1, 0] = 0.5 * (x[-2, 0] + x[-1, 1])
        x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])

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


def inject_plume(fluid_sim, frame, rng):
    """Scripted source: a swaying jet rising from the bottom centre of the box."""
    height, width = fluid_sim.size
    cx, cy = width // 2, height - 8
    sway = np.sin(frame / 15.0)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            fluid_sim.add_density(cx + dx, cy + dy, PLUME_DENSITY)
            fluid_sim.add_velocity(
                cx + dx,
                cy + dy,
                PLUME_SWAY * sway + 0.02 * rng.standard_normal(),
                -PLUME_VELOCITY + 0.02 * rng.standard_normal(),  # negative y is up
            )


def handle_events(pygame, fluid_sim, cell_size, grid_width, grid_height, rng):
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
                fluid_sim.add_density(grid_x, grid_y, CLICK_DENSITY)
                fluid_sim.add_velocity(
                    grid_x,
                    grid_y,
                    rng.uniform(-CLICK_VELOCITY, CLICK_VELOCITY),
                    rng.uniform(-CLICK_VELOCITY, CLICK_VELOCITY),
                )
    return False


def draw_simulation(pygame, screen, fluid_sim, screen_size):
    screen.fill((0, 0, 0))
    density_scaled = np.clip(fluid_sim.density * 1000, 0, 255).astype(np.uint8)

    # Transpose the density array to match Pygame's (x, y) surface indexing
    density_scaled = np.transpose(density_scaled)

    color_surface = np.zeros((*density_scaled.shape, 3), dtype=np.uint8)
    color_surface[:, :, 2] = density_scaled  # Using blue channel
    density_surface = pygame.surfarray.make_surface(color_surface)
    density_surface = pygame.transform.scale(density_surface, screen_size)
    screen.blit(density_surface, (0, 0))
    pygame.display.flip()


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help="frames (one solver step each) to run (default: until the window is closed)",
    )
    parser.add_argument(
        "--auto-inject",
        action="store_true",
        help="inject a scripted plume every frame (implied by --no-show)",
    )
    args = parser.parse_args(argv)

    if args.no_show:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    import pygame

    rng = np.random.default_rng(SEED)
    grid_width, grid_height = SCREEN_SIZE[0] // CELL_SIZE, SCREEN_SIZE[1] // CELL_SIZE
    fluid_sim = FluidSimulation(
        width=grid_width,
        height=grid_height,
        diffusion=DIFFUSION,
        viscosity=VISCOSITY,
        dt=TIME_STEP,
    )
    auto_inject = args.auto_inject or args.no_show

    pygame.init()
    try:
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Fluid Simulation")
        clock = pygame.time.Clock()
        frame = 0
        while args.steps is None or frame < args.steps:
            if handle_events(
                pygame, fluid_sim, CELL_SIZE, grid_width, grid_height, rng
            ):
                break
            if auto_inject:
                inject_plume(fluid_sim, frame, rng)
            fluid_sim.step()
            draw_simulation(pygame, screen, fluid_sim, SCREEN_SIZE)
            if not args.no_show:
                clock.tick(FPS)
            frame += 1

        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            pygame.image.save(
                screen,
                str(args.output / "simplified_real_time_fluid_dynamics_simulator.png"),
            )
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
