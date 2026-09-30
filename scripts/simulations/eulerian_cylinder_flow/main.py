"""Real-time Eulerian simulation of inviscid flow past a cylinder with Pygame.

A 2D staggered (MAC) grid holds the velocity and a passive dye ("smoke")
field. Each frame applies gravity (off by default), makes the velocity
divergence-free with Gauss-Seidel over-relaxation, extrapolates boundary
velocities, and advects velocity and dye with the semi-Lagrangian method. A
uniform inflow enters from the left; a dye streak released at mid-height shows
the wake. The scheme follows Matthias Mueller's "Ten Minute Physics" Eulerian
fluid demo. There is no explicit viscosity; only numerical diffusion from the
interpolation damps the flow.

Keys: P pauses or resumes, M advances one frame while paused.
"""

import os
import sys
from pathlib import Path

import numpy as np
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int  # noqa: E402

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # pixels
SIM_HEIGHT = 1.1  # visible height of the window, m
GRAVITY = 0.0  # m/s^2 (turned off)
DELTA_TIME = 1.0 / 60.0  # s per frame
NUM_ITERATIONS = 20  # Gauss-Seidel iterations per frame
OVER_RELAXATION = 1.9  # SOR factor for the projection
OBSTACLE_X, OBSTACLE_Y = 0.4, 0.5  # cylinder centre, m
OBSTACLE_RADIUS = 0.15  # m
DENSITY = 1000.0  # kg/m^3 (only scales the pressure field)
INLET_VELOCITY = 2.0  # m/s
RESOLUTION = 100  # cells across the domain height
DEFAULT_HEADLESS_STEPS = 300  # frames used with --no-show when --steps is omitted

BACKGROUND = (240, 248, 255)  # Alice blue
OBSTACLE_COLOR = (47, 79, 79)  # dark slate grey
PALETTE = np.array(
    [
        (173, 216, 230),  # light blue      dye fraction 0.00-0.25
        (100, 149, 237),  # cornflower blue 0.25-0.50
        (70, 130, 180),  # steel blue       0.50-0.75
        (144, 238, 144),  # light green     0.75-1.00 (clear fluid)
    ],
    dtype=np.uint8,
)


@njit(cache=False)
def integrate(v, s, nx, ny, dt, gravity):
    """Add gravity to v on faces between two fluid cells."""
    n = ny
    for i in range(1, nx):
        for j in range(1, ny - 1):
            if s[i * n + j] != 0.0 and s[i * n + j - 1] != 0.0:
                v[i * n + j] += gravity * dt


@njit(cache=False)
def solve_incompressibility(u, v, p, s, nx, ny, num_iters, cp, omega):
    """Remove the velocity divergence of every fluid cell by Gauss-Seidel SOR.

    s is 1 for fluid and 0 for solid cells; solid faces are not changed. The
    accumulated correction times cp = rho*h/dt is the pressure.
    """
    n = ny
    for _ in range(num_iters):
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                if s[i * n + j] == 0.0:
                    continue
                sx0 = s[(i - 1) * n + j]
                sx1 = s[(i + 1) * n + j]
                sy0 = s[i * n + j - 1]
                sy1 = s[i * n + j + 1]
                s_sum = sx0 + sx1 + sy0 + sy1
                if s_sum == 0.0:
                    continue
                div = (
                    u[(i + 1) * n + j] - u[i * n + j] + v[i * n + j + 1] - v[i * n + j]
                )
                corr = -div / s_sum * omega
                p[i * n + j] += cp * corr
                u[i * n + j] -= sx0 * corr
                u[(i + 1) * n + j] += sx1 * corr
                v[i * n + j] -= sy0 * corr
                v[i * n + j + 1] += sy1 * corr


@njit(cache=False)
def extrapolate(u, v, nx, ny):
    """Copy tangential velocities into the boundary rows and columns."""
    n = ny
    for i in range(nx):
        u[i * n + 0] = u[i * n + 1]
        u[i * n + ny - 1] = u[i * n + ny - 2]
    for j in range(ny):
        v[0 * n + j] = v[1 * n + j]
        v[(nx - 1) * n + j] = v[(nx - 2) * n + j]


@njit(cache=False)
def sample_field(x, y, field, off_x, off_y, nx, ny, h):
    """Bilinearly interpolate a staggered field at (x, y).

    off_x, off_y give the offset of the field's sample points from the cell
    corner: u is at (0, h/2), v at (h/2, 0), cell-centred data at (h/2, h/2).
    """
    n = ny
    inv_h = 1.0 / h
    x = min(max(x, h), nx * h)
    y = min(max(y, h), ny * h)

    x0 = min(int((x - off_x) * inv_h), nx - 1)
    tx = ((x - off_x) - x0 * h) * inv_h
    x1 = min(x0 + 1, nx - 1)

    y0 = min(int((y - off_y) * inv_h), ny - 1)
    ty = ((y - off_y) - y0 * h) * inv_h
    y1 = min(y0 + 1, ny - 1)

    sx = 1.0 - tx
    sy = 1.0 - ty
    return (
        sx * sy * field[x0 * n + y0]
        + tx * sy * field[x1 * n + y0]
        + tx * ty * field[x1 * n + y1]
        + sx * ty * field[x0 * n + y1]
    )


@njit(cache=False)
def advect_velocity(u, v, new_u, new_v, s, nx, ny, h, dt):
    """Semi-Lagrangian advection of both velocity components."""
    n = ny
    half_h = 0.5 * h
    new_u[:] = u
    new_v[:] = v
    for i in range(1, nx):
        for j in range(1, ny):
            if s[i * n + j] != 0.0 and s[(i - 1) * n + j] != 0.0 and j < ny - 1:
                x = i * h
                y = j * h + half_h
                uu = u[i * n + j]
                vv = sample_field(x, y, v, half_h, 0.0, nx, ny, h)
                new_u[i * n + j] = sample_field(
                    x - dt * uu, y - dt * vv, u, 0.0, half_h, nx, ny, h
                )
            if s[i * n + j] != 0.0 and s[i * n + j - 1] != 0.0 and i < nx - 1:
                x = i * h + half_h
                y = j * h
                uu = sample_field(x, y, u, 0.0, half_h, nx, ny, h)
                vv = v[i * n + j]
                new_v[i * n + j] = sample_field(
                    x - dt * uu, y - dt * vv, v, half_h, 0.0, nx, ny, h
                )
    u[:] = new_u
    v[:] = new_v


@njit(cache=False)
def advect_dye(m, new_m, u, v, s, nx, ny, h, dt):
    """Semi-Lagrangian advection of the cell-centred dye field."""
    n = ny
    half_h = 0.5 * h
    new_m[:] = m
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            if s[i * n + j] != 0.0:
                uu = 0.5 * (u[i * n + j] + u[(i + 1) * n + j])
                vv = 0.5 * (v[i * n + j] + v[i * n + j + 1])
                x = i * h + half_h - dt * uu
                y = j * h + half_h - dt * vv
                new_m[i * n + j] = sample_field(x, y, m, half_h, half_h, nx, ny, h)
    m[:] = new_m


class FluidSimulator:
    """Staggered-grid fluid state; arrays are flat with index i * grid_height + j."""

    def __init__(self, density, grid_width, grid_height, cell_size):
        self.density = density
        self.grid_width = grid_width + 2  # one ghost/boundary cell on each side
        self.grid_height = grid_height + 2
        self.num_cells = self.grid_width * self.grid_height
        self.cell_size = cell_size
        self.u = np.zeros(self.num_cells, dtype=np.float32)
        self.v = np.zeros(self.num_cells, dtype=np.float32)
        self.new_u = np.zeros(self.num_cells, dtype=np.float32)
        self.new_v = np.zeros(self.num_cells, dtype=np.float32)
        self.pressure = np.zeros(self.num_cells, dtype=np.float32)
        self.solid = np.ones(self.num_cells, dtype=np.float32)  # 1 fluid, 0 solid
        self.density_field = np.ones(self.num_cells, dtype=np.float32)  # dye
        self.new_density_field = np.zeros(self.num_cells, dtype=np.float32)

    def simulate(self, delta_time, gravity, num_iterations, over_relaxation):
        nx, ny, h = self.grid_width, self.grid_height, self.cell_size
        integrate(self.v, self.solid, nx, ny, delta_time, gravity)
        self.pressure.fill(0.0)
        cp = self.density * h / delta_time
        solve_incompressibility(
            self.u,
            self.v,
            self.pressure,
            self.solid,
            nx,
            ny,
            num_iterations,
            cp,
            over_relaxation,
        )
        extrapolate(self.u, self.v, nx, ny)
        advect_velocity(
            self.u, self.v, self.new_u, self.new_v, self.solid, nx, ny, h, delta_time
        )
        advect_dye(
            self.density_field,
            self.new_density_field,
            self.u,
            self.v,
            self.solid,
            nx,
            ny,
            h,
            delta_time,
        )

    def set_obstacle(self, x, y, radius, velocity_x=0.0, velocity_y=0.0):
        """Mark cells inside the circle as solid and set their face velocities."""
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


def setup_scene(scene_number=1):
    """Return a FluidSimulator for scene 0 (tank) or 1 (wind tunnel)."""
    resolution = RESOLUTION if scene_number != 0 else RESOLUTION // 2
    domain_height = 1.0  # m
    domain_width = domain_height * WINDOW_WIDTH / WINDOW_HEIGHT  # m
    cell_size = domain_height / resolution
    grid_width = int(domain_width / cell_size)
    grid_height = int(domain_height / cell_size)

    fluid = FluidSimulator(DENSITY, grid_width, grid_height, cell_size)
    n = fluid.grid_height
    if scene_number == 0:  # closed tank, open at the top
        for i in range(fluid.grid_width):
            for j in range(fluid.grid_height):
                inside = i != 0 and i != fluid.grid_width - 1 and j != 0
                fluid.solid[i * n + j] = 1.0 if inside else 0.0
    else:  # wind tunnel: solid left wall with inflow, walls at top and bottom
        for i in range(fluid.grid_width):
            for j in range(fluid.grid_height):
                inside = i != 0 and j != 0 and j != fluid.grid_height - 1
                fluid.solid[i * n + j] = 1.0 if inside else 0.0
                if i == 1:
                    fluid.u[i * n + j] = INLET_VELOCITY
        # dye streak entering at mid-height through the inlet column (i = 0)
        pipe_height = 0.1 * fluid.grid_height
        min_j = int(0.5 * fluid.grid_height - 0.5 * pipe_height)
        max_j = int(0.5 * fluid.grid_height + 0.5 * pipe_height)
        fluid.density_field[min_j:max_j] = 0.0
    return fluid


def draw(screen, fluid, canvas_scale):
    """Draw the dye field (4-colour banded map) and the obstacle."""
    import pygame

    nx, ny = fluid.grid_width, fluid.grid_height
    m = fluid.density_field.reshape(nx, ny)
    solid = fluid.solid.reshape(nx, ny)
    band = (np.clip(m, 0.0, 1.0 - 1e-4) / 0.25).astype(np.int64)
    rgb = PALETTE[band]
    rgb[m == 0.0] = BACKGROUND
    rgb[solid == 0.0] = OBSTACLE_COLOR
    # surfarray is indexed (x, y) with y pointing down; grid j points up
    image = pygame.surfarray.make_surface(np.ascontiguousarray(rgb[:, ::-1, :]))
    size = (
        int(round(nx * fluid.cell_size * canvas_scale)),
        int(round(ny * fluid.cell_size * canvas_scale)),
    )
    screen.fill(BACKGROUND)
    screen.blit(pygame.transform.scale(image, size), (0, WINDOW_HEIGHT - size[1]))


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help="simulate this many frames, then stop (default: run until closed; "
        f"{DEFAULT_HEADLESS_STEPS} with --no-show)",
    )
    args = parser.parse_args(argv)
    max_steps = args.steps
    if args.no_show:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        if max_steps is None:
            max_steps = DEFAULT_HEADLESS_STEPS

    import pygame

    pygame.init()
    try:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Eulerian Cylinder Flow")
        clock = pygame.time.Clock()
        canvas_scale = WINDOW_HEIGHT / SIM_HEIGHT  # pixels per metre

        fluid = setup_scene(1)
        fluid.set_obstacle(OBSTACLE_X, OBSTACLE_Y, OBSTACLE_RADIUS)

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
                        fluid.simulate(
                            DELTA_TIME, GRAVITY, NUM_ITERATIONS, OVER_RELAXATION
                        )
                        frame_number += 1
                        paused = True

            if not paused:
                fluid.simulate(DELTA_TIME, GRAVITY, NUM_ITERATIONS, OVER_RELAXATION)
                frame_number += 1

            draw(screen, fluid, canvas_scale)
            pygame.display.flip()
            if max_steps is not None and frame_number >= max_steps:
                running = False
            if not args.no_show:
                clock.tick(60)

        print(
            f"simulated {frame_number} frames (t = {frame_number * DELTA_TIME:.2f} s)"
        )
        if args.output:
            out_dir = Path(args.output)
            out_dir.mkdir(parents=True, exist_ok=True)
            pygame.image.save(screen, str(out_dir / "eulerian_cylinder_flow.png"))
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
