"""Eulerian simulation of inviscid flow past a cylinder in a wind tunnel.

A 2D staggered (MAC) grid holds the velocity and a passive dye field. Each
step applies gravity (off by default), makes the velocity divergence-free with
Gauss-Seidel over-relaxation, extrapolates boundary velocities, and advects
velocity and dye with the semi-Lagrangian method. A uniform inflow enters from
the left; a dye streak released at mid-height shows the wake, drawn as a
colour map of the dye concentration with the walls and cylinder in grey. The
scheme follows Matthias Mueller's "Ten Minute Physics" Eulerian fluid demo.
There is no explicit viscosity; only numerical diffusion from the
interpolation damps the flow.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib import colormaps
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

DOMAIN_HEIGHT = 1.0  # m, between the walls (plus one boundary cell at each side)
DOMAIN_WIDTH = 4.0 / 3.0  # m, inlet to outlet
RESOLUTION = 100  # cells across the domain height
GRAVITY = 0.0  # m/s^2 (turned off)
DELTA_TIME = 1.0 / 60.0  # s per time step
NUM_ITERATIONS = 20  # Gauss-Seidel iterations per time step
OVER_RELAXATION = 1.9  # SOR factor for the projection
OBSTACLE_X, OBSTACLE_Y = 0.4, 0.5  # cylinder centre, m
OBSTACLE_RADIUS = 0.15  # m
DENSITY = 1000.0  # kg/m^3 (only scales the pressure field)
INLET_VELOCITY = 2.0  # m/s
DYE_STREAK_HEIGHT = 0.1  # fraction of the grid height released as dye at the inlet
STEPS_PER_FRAME = 2  # time steps per frame: 1/30 s of flow
N_FRAMES = 450  # default frames of a headless run or reel -> t = 15 s


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


class EulerianCylinderSimulation(Simulation):
    """Wind tunnel on a staggered grid; arrays are flat with index i * grid_height + j.

    ``u`` lives on the left face of cell (i, j), ``v`` on its bottom face,
    pressure and dye (``density_field``: 1 = clear fluid, 0 = dye) at its
    centre. ``solid`` is 1 for fluid and 0 for walls and the cylinder. The left
    column is a solid inlet whose faces carry the inflow velocity, the top and
    bottom rows are walls, and the right side is open.
    """

    dt = DELTA_TIME

    def __init__(self, resolution=RESOLUTION, density=DENSITY):
        super().__init__()
        self.density = density
        self.cell_size = DOMAIN_HEIGHT / resolution
        # one ghost/boundary cell on each side
        self.grid_width = int(DOMAIN_WIDTH / self.cell_size) + 2
        self.grid_height = int(DOMAIN_HEIGHT / self.cell_size) + 2
        self.num_cells = self.grid_width * self.grid_height
        self.u = np.zeros(self.num_cells, dtype=np.float32)
        self.v = np.zeros(self.num_cells, dtype=np.float32)
        self.new_u = np.zeros(self.num_cells, dtype=np.float32)
        self.new_v = np.zeros(self.num_cells, dtype=np.float32)
        self.pressure = np.zeros(self.num_cells, dtype=np.float32)
        self.solid = np.ones(self.num_cells, dtype=np.float32)  # 1 fluid, 0 solid
        self.density_field = np.ones(self.num_cells, dtype=np.float32)  # dye
        self.new_density_field = np.zeros(self.num_cells, dtype=np.float32)

        n = self.grid_height
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                inside = i != 0 and j != 0 and j != self.grid_height - 1
                self.solid[i * n + j] = 1.0 if inside else 0.0
                if i == 1:
                    self.u[i * n + j] = INLET_VELOCITY
        # dye streak entering at mid-height through the inlet column (i = 0)
        pipe_height = DYE_STREAK_HEIGHT * self.grid_height
        min_j = int(0.5 * self.grid_height - 0.5 * pipe_height)
        max_j = int(0.5 * self.grid_height + 0.5 * pipe_height)
        self.density_field[min_j:max_j] = 0.0
        self.set_obstacle(OBSTACLE_X, OBSTACLE_Y, OBSTACLE_RADIUS)

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

    def step(self):
        self.simulate(DELTA_TIME, GRAVITY, NUM_ITERATIONS, OVER_RELAXATION)

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

    @property
    def dye(self):
        """Dye concentration 1 - density_field, shape (grid_width, grid_height).

        Solid cells (walls, inlet column and cylinder) are NaN.
        """
        shape = (self.grid_width, self.grid_height)
        dye = 1.0 - self.density_field.reshape(shape).astype(float)
        dye[self.solid.reshape(shape) == 0.0] = np.nan
        return dye


class EulerianCylinderView(View):
    """Dye concentration from black (clear fluid) to yellow; solid cells grey.

    The 4:3 tunnel already fills the nearly square reel panel, so the reel
    keeps the flow left to right and moves the colour bar below the map.
    """

    figsize = (8.0, 5.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        h = simulation.cell_size
        extent = (0.0, simulation.grid_width * h, 0.0, simulation.grid_height * h)
        self.image = ax.imshow(
            simulation.dye.T, extent=extent, origin="lower", vmin=0.0, vmax=1.0,
            cmap=colormaps["inferno"].with_extremes(bad="0.55"),
            interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(
            self.image, ax=ax, label="dye concentration",
            location="bottom" if portrait else "right",
        )  # fmt: skip
        ax.set(xlabel="x [m]", ylabel="y [m]")

    def draw(self):
        self.image.set_data(self.simulation.dye.T)

    def status(self):
        return f"t = {self.simulation.time:.2f} s"


ANIMATION = Animation(
    title="Eulerian Cylinder Flow",
    subtitle="Dye streak behind a cylinder in a wind tunnel",
    filename="eulerian_cylinder_flow.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of 1/{1 / DELTA_TIME:g} s",
    endless=True,
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, EulerianCylinderSimulation(), EulerianCylinderView)
    print(
        f"t = {simulation.time:.2f} s after {simulation.steps} time steps "
        f"on a {simulation.grid_width} x {simulation.grid_height} grid"
    )


if __name__ == "__main__":
    main()
