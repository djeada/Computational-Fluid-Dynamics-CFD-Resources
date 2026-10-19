"""Dam break: a collapsing water column simulated with weakly compressible SPH.

A column of water a wide and 2a high stands at rest against the left wall of a
closed tank 4a wide and 3a high. At t = 0 the dam holding it is removed: the
column collapses, a surge runs along the floor, shoots up the far wall to the
lid and falls back as a plunging breaker, and a wave returns to the left wall.
The water is a set of particles that carry mass, density and velocity
(smoothed particle hydrodynamics in the style of Monaghan, 1994): a cubic-spline
kernel, the Tait equation of state with an artificial speed of sound,
artificial viscosity, dummy wall particles whose pressure is extrapolated from
the fluid (Adami et al., 2012), and kick-drift-kick leapfrog time steps limited
by the sound speed and the accelerations. A Numba cell list finds the
neighbours. The particles are drawn as dots coloured by their speed.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib import colormaps
from matplotlib.collections import EllipseCollection
from matplotlib.colors import ListedColormap
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (SI units)
GRAVITY = 9.81  # g [m/s^2], acting in -y
COLUMN_WIDTH = 0.5  # a [m]
COLUMN_HEIGHT = 1.0  # initial water height 2a [m]
TANK_WIDTH = 2.0  # 4a [m]
TANK_HEIGHT = 1.5  # 3a: a lid closes the tank at this height [m]
REST_DENSITY = 1000.0  # rho_0 [kg/m^3]
FREE_FALL_SPEED = np.sqrt(2 * GRAVITY * COLUMN_HEIGHT)  # sqrt(2 g 2a) = 4.4 m/s

# SPH parameters
PARTICLES_ACROSS = 40  # fluid particles across the column: dp = a / 40 = 12.5 mm
SMOOTHING_RATIO = 1.3  # smoothing length h / dp; the kernel reaches 2h
SOUND_SPEED = 10 * FREE_FALL_SPEED  # artificial c_0 = 44 m/s [m/s]
TAIT_EXPONENT = 7.0  # gamma of the Tait equation of state
VISCOSITY_ALPHA = 0.05  # alpha of Monaghan's artificial viscosity
WALL_LAYERS = 3  # rows of dummy particles behind each wall: 3 dp > 2h
CFL_NUMBER = 0.25  # dt <= CFL h / (c_0 + max |v|)
FORCE_NUMBER = 0.25  # dt <= FORCE sqrt(h / max |a|)
STEPS_PER_FRAME = 48  # leapfrog steps per animation frame (about 4 ms)
N_FRAMES = 560  # default frames: 26 880 steps reach t = 2.2 s

# Display
SPEED_CMAP = ListedColormap(colormaps["turbo"](np.linspace(0.08, 1.0, 256)))
WALL_COLOR = "0.4"
DOT_SIZE = 1.1  # diameter of a drawn particle / dp


@njit(cache=False)
def kernel(r, h):
    """Cubic-spline kernel W(r, h) in 2D, normalised to 1; zero beyond 2h."""
    q = r / h
    sigma = 10.0 / (7.0 * np.pi * h * h)
    if q < 1.0:
        return sigma * (1.0 - 1.5 * q * q + 0.75 * q * q * q)
    if q < 2.0:
        return sigma * 0.25 * (2.0 - q) ** 3
    return 0.0


@njit(cache=False)
def kernel_derivative(r, h):
    """dW/dr of the cubic spline (negative inside the support)."""
    q = r / h
    sigma = 10.0 / (7.0 * np.pi * h * h)
    if q < 1.0:
        return sigma / h * (-3.0 * q + 2.25 * q * q)
    if q < 2.0:
        return -sigma / h * 0.75 * (2.0 - q) ** 2
    return 0.0


@njit(cache=False)
def tait_pressure(rho, rho0, c0, gamma):
    """p = B ((rho / rho0)^gamma - 1) with B = rho0 c0^2 / gamma."""
    return rho0 * c0 * c0 / gamma * ((rho / rho0) ** gamma - 1.0)


@njit(cache=False)
def tait_density(p, rho0, c0, gamma):
    """Inverse of tait_pressure."""
    return rho0 * (1.0 + p * gamma / (rho0 * c0 * c0)) ** (1.0 / gamma)


@njit(cache=False)
def build_cells(x, y, grid):
    """Counting sort of the particles into square cells of side 2h.

    ``grid`` is (x0, y0, cell size, nx, ny). Particles outside the grid are
    clamped into its edge cells, which keeps every pair closer than one cell
    in the same or neighbouring cells. Cell c holds the particles
    order[start[c]:start[c + 1]]; ``cell`` gives each particle's cell.
    """
    x0, y0, size, nx, ny = grid
    n = x.size
    cell = np.empty(n, np.int64)
    start = np.zeros(int(nx * ny) + 1, np.int64)
    for i in range(n):
        cx = min(max(int((x[i] - x0) / size), 0), int(nx) - 1)
        cy = min(max(int((y[i] - y0) / size), 0), int(ny) - 1)
        cell[i] = cy * int(nx) + cx
        start[cell[i] + 1] += 1
    for c in range(1, start.size):
        start[c] += start[c - 1]
    fill = start[:-1].copy()
    order = np.empty(n, np.int64)
    for i in range(n):
        order[fill[cell[i]]] = i
        fill[cell[i]] += 1
    return cell, order, start


@njit(cache=False)
def compute_rates(x, y, vx, vy, rho, n_fluid, mass, h, grid, gravity, viscosity):
    """Accelerations and density rates of the fluid particles.

    Particles 0 .. n_fluid - 1 are fluid, the rest are fixed wall particles.
    Wall pressures are extrapolated from the fluid first (Adami et al., 2012).
    Walls push but never pull: negative pressures are set to zero in every
    fluid-wall pair, so that spray cannot stick to them.
    Returns (ax, ay, drho) for the fluid and the pressure of every particle.
    """
    n = x.size
    nx = int(grid[3])
    c0, rho0, gamma = SOUND_SPEED, REST_DENSITY, TAIT_EXPONENT
    support = 2.0 * h
    cell, order, start = build_cells(x, y, grid)
    pressure = np.empty(n)
    density = rho.copy()
    for i in range(n_fluid):
        pressure[i] = tait_pressure(rho[i], rho0, c0, gamma)

    # Wall particles: Shepard-weighted fluid pressure plus the hydrostatic
    # difference rho_f g . (r_w - r_f), and the density that goes with it.
    for w in range(n_fluid, n):
        weighted, weights = 0.0, 0.0
        cx, cy = cell[w] % nx, cell[w] // nx
        for ny in range(max(cy - 1, 0), min(cy + 2, int(grid[4]))):
            for mx in range(max(cx - 1, 0), min(cx + 2, nx)):
                c = ny * nx + mx
                for k in range(start[c], start[c + 1]):
                    f = order[k]
                    if f >= n_fluid:
                        continue
                    dx, dy = x[w] - x[f], y[w] - y[f]
                    r = np.sqrt(dx * dx + dy * dy)
                    if r < support:
                        weight = kernel(r, h)
                        hydrostatic = rho[f] * (gravity[0] * dx + gravity[1] * dy)
                        weighted += (pressure[f] + hydrostatic) * weight
                        weights += weight
        pressure[w] = max(weighted / weights, 0.0) if weights > 0.0 else 0.0
        density[w] = tait_density(pressure[w], rho0, c0, gamma)

    ax = np.zeros(n_fluid)
    ay = np.zeros(n_fluid)
    drho = np.zeros(n_fluid)
    for i in range(n_fluid):
        cx, cy = cell[i] % nx, cell[i] // nx
        p_i = pressure[i] / (rho[i] * rho[i])
        p_i_wall = max(p_i, 0.0)
        for ny in range(max(cy - 1, 0), min(cy + 2, int(grid[4]))):
            for mx in range(max(cx - 1, 0), min(cx + 2, nx)):
                c = ny * nx + mx
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i:
                        continue
                    dx, dy = x[i] - x[j], y[i] - y[j]
                    r2 = dx * dx + dy * dy
                    if r2 >= support * support or r2 == 0.0:
                        continue
                    r = np.sqrt(r2)
                    gradient = kernel_derivative(r, h) / r  # grad_i W = this * (dx, dy)
                    dvx, dvy = vx[i] - vx[j], vy[i] - vy[j]
                    approach = dvx * dx + dvy * dy
                    own = p_i if j < n_fluid else p_i_wall
                    term = own + pressure[j] / (density[j] * density[j])
                    if approach < 0.0:  # artificial viscosity only on approach
                        mu = h * approach / (r2 + 0.01 * h * h)
                        term -= viscosity * c0 * mu / (0.5 * (rho[i] + density[j]))
                    ax[i] -= mass * term * gradient * dx
                    ay[i] -= mass * term * gradient * dy
                    drho[i] += mass * gradient * approach
        ax[i] += gravity[0]
        ay[i] += gravity[1]
    return ax, ay, drho, pressure


def lattice(x_start, y_start, columns, rows, spacing):
    """Points of a square lattice, row by row from (x_start, y_start)."""
    x, y = np.meshgrid(
        x_start + spacing * np.arange(columns), y_start + spacing * np.arange(rows)
    )
    return x.ravel(), y.ravel()


def hydrostatic_density(depth):
    """Density whose Tait pressure is rho_0 g depth."""
    b = REST_DENSITY * SOUND_SPEED**2 / TAIT_EXPONENT
    return REST_DENSITY * (1 + REST_DENSITY * GRAVITY * depth / b) ** (
        1 / TAIT_EXPONENT
    )


class SPHDamBreakSimulation(Simulation):
    """Fluid and wall particles; one step is one leapfrog time step.

    Arrays ``x``, ``y``, ``vx``, ``vy``, ``rho`` and ``pressure`` hold the
    ``n_fluid`` fluid particles first, then the wall particles, which never
    move. The column starts at rest with hydrostatic density. With
    ``tank_width=column_width`` the water has nowhere to go and stays at rest.
    """

    def __init__(
        self,
        particles_across=PARTICLES_ACROSS,
        column_width=COLUMN_WIDTH,
        column_height=COLUMN_HEIGHT,
        tank_width=TANK_WIDTH,
        tank_height=TANK_HEIGHT,
    ):
        super().__init__()
        if particles_across < 2 or tank_width < column_width:
            raise ValueError("need two particles across and a tank around the column")
        dp = column_width / particles_across
        self.spacing = dp
        self.h = SMOOTHING_RATIO * dp
        self.mass = REST_DENSITY * dp * dp
        self.column_width = column_width
        self.tank_width, self.tank_height = tank_width, tank_height
        fluid = lattice(dp / 2, dp / 2, particles_across, round(column_height / dp), dp)
        self.n_fluid = fluid[0].size

        # Dummy wall particles: WALL_LAYERS rows under the floor and above
        # the lid (both with the corners) and beside the two side walls.
        layers = WALL_LAYERS
        across = round(tank_width / dp) + 2 * layers
        up = round(tank_height / dp)
        start = -(layers - 0.5) * dp
        floor = lattice(start, start, across, layers, dp)
        lid = lattice(start, up * dp + dp / 2, across, layers, dp)
        left = lattice(start, dp / 2, layers, up, dp)
        right = lattice(tank_width + dp / 2, dp / 2, layers, up, dp)
        parts = (fluid, floor, lid, left, right)
        self.x = np.concatenate([part[0] for part in parts])
        self.y = np.concatenate([part[1] for part in parts])
        self.vx = np.zeros_like(self.x)
        self.vy = np.zeros_like(self.x)
        self.rho = np.full_like(self.x, REST_DENSITY)
        self.rho[: self.n_fluid] = hydrostatic_density(
            column_height - self.y[: self.n_fluid]
        )

        # Cells of side 2h over the closed tank and its walls.
        size = 2 * self.h
        x0, y0 = -layers * dp - size, -layers * dp - size
        nx = int(np.ceil((tank_width + 2 * layers * dp + 2 * size) / size))
        ny = int(np.ceil((tank_height + 2 * layers * dp + 2 * size) / size))
        self.grid = np.array([x0, y0, size, nx, ny], dtype=float)
        self.gravity = np.array([0.0, -GRAVITY])
        self.t = 0.0
        self.dt = 0.0
        self.update_rates()

    @property
    def time(self):
        return self.t

    def update_rates(self, vx=None, vy=None, rho=None):
        """Evaluate accelerations and density rates, by default at the state."""
        rates = compute_rates(
            self.x, self.y,
            self.vx if vx is None else vx, self.vy if vy is None else vy,
            self.rho if rho is None else rho,
            self.n_fluid, self.mass, self.h, self.grid, self.gravity, VISCOSITY_ALPHA,
        )  # fmt: skip
        self.ax, self.ay, self.drho, self.pressure = rates

    def stable_time_step(self):
        """Smaller of the sound-speed (CFL) and acceleration limits."""
        f = self.n_fluid
        speed = np.sqrt(self.vx[:f] ** 2 + self.vy[:f] ** 2).max()
        accel = np.sqrt(self.ax**2 + self.ay**2).max()
        return min(
            CFL_NUMBER * self.h / (SOUND_SPEED + speed),
            FORCE_NUMBER * np.sqrt(self.h / accel),
        )

    def step(self):
        """Kick-drift-kick leapfrog; the rates at the new positions use the
        velocity and density predicted with the old rates."""
        f = self.n_fluid
        dt = self.dt = self.stable_time_step()
        self.vx[:f] += 0.5 * dt * self.ax
        self.vy[:f] += 0.5 * dt * self.ay
        self.rho[:f] += 0.5 * dt * self.drho
        self.x[:f] += dt * self.vx[:f]
        self.y[:f] += dt * self.vy[:f]
        vx, vy, rho = self.vx.copy(), self.vy.copy(), self.rho.copy()
        vx[:f] += 0.5 * dt * self.ax
        vy[:f] += 0.5 * dt * self.ay
        rho[:f] += 0.5 * dt * self.drho
        self.update_rates(vx, vy, rho)
        self.vx[:f] += 0.5 * dt * self.ax
        self.vy[:f] += 0.5 * dt * self.ay
        self.rho[:f] += 0.5 * dt * self.drho
        self.t += dt

    @property
    def speed(self):
        f = self.n_fluid
        return np.sqrt(self.vx[:f] ** 2 + self.vy[:f] ** 2)

    def surge_front(self):
        """Leading edge of the fluid touching the floor (y < 2 dp) [m]."""
        f = self.n_fluid
        on_floor = self.y[:f] < 2 * self.spacing
        if not on_floor.any():
            return 0.0
        edge = self.x[:f][on_floor].max() + 0.5 * self.spacing
        return min(edge, self.tank_width)


class DamBreakView(View):
    """Particles as dots coloured by speed; the grey dots are wall particles.

    The dots are circles slightly wider than the particle spacing in data
    units, so the water looks the same at any figure size. The 4:3 tank has
    its colour bar to the right in the window and below it in a reel.
    """

    figsize = (8.6, 6.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        ax = figure.subplots()
        f, dp = simulation.n_fluid, simulation.spacing
        size = DOT_SIZE * dp
        walls = np.column_stack([simulation.x[f:], simulation.y[f:]])
        ax.add_collection(
            EllipseCollection(
                size, size, 0.0, units="xy", offsets=walls,
                offset_transform=ax.transData, color=WALL_COLOR, linewidths=0,
            )
        )  # fmt: skip
        self.particles = EllipseCollection(
            size, size, 0.0, units="xy", offsets=self.offsets(),
            offset_transform=ax.transData, cmap=SPEED_CMAP, linewidths=0,
        )  # fmt: skip
        self.particles.set_array(simulation.speed)
        self.particles.set_clim(0.0, FREE_FALL_SPEED)
        ax.add_collection(self.particles)
        edge = (WALL_LAYERS + 0.5) * dp
        ax.set(xlim=(-edge, simulation.tank_width + edge))
        ax.set(ylim=(-edge, simulation.tank_height + edge))
        ax.set_aspect("equal")
        ax.set(xlabel="x [m]", ylabel="y [m]")
        figure.colorbar(
            self.particles, ax=ax, location="bottom" if portrait else "right",
            shrink=0.8 if portrait else 1, label="speed |v| [m/s]",
        )  # fmt: skip

    def offsets(self):
        f = self.simulation.n_fluid
        return np.column_stack([self.simulation.x[:f], self.simulation.y[:f]])

    def draw(self):
        self.particles.set_offsets(self.offsets())
        self.particles.set_array(self.simulation.speed)

    def status(self):
        simulation = self.simulation
        front = simulation.surge_front() / simulation.column_width
        return f"t = {simulation.time:.2f} s   front x/a = {front:.2f}"


ANIMATION = Animation(
    title="SPH Dam Break",
    subtitle="A water column collapses, particle by particle",
    filename="sph_dam_break.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="leapfrog time steps",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, SPHDamBreakSimulation(), DamBreakView)
    f = simulation.n_fluid
    density = simulation.rho[:f] / REST_DENSITY
    print(
        f"t = {simulation.time:.3f} s after {simulation.steps} steps: "
        f"{f} fluid particles, max speed {simulation.speed.max():.2f} m/s, "
        f"density {density.min():.3f} to {density.max():.3f} rho_0"
    )


if __name__ == "__main__":
    main()
