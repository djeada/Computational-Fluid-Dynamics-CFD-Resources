"""2D flow past a cylinder with the D2Q9 BGK lattice Boltzmann method.

A uniform inflow (Zou/He velocity inlet) passes a circular obstacle with
bounce-back walls; the domain is periodic in y and has a zero-gradient outlet.
Two stacked colour maps show the velocity magnitude and the vorticity, in which
the von Karman vortex street appears once shedding sets in.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib import colormaps

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Simulation parameters (lattice units: dx = dt = 1)
REYNOLDS_NUMBER = 350.0  # Re = U * r / nu, based on the cylinder radius
LATTICE_DIMENSIONS = (1040, 360)  # (nx, ny) lattice nodes
NUM_POPULATIONS = 9  # D2Q9
CYLINDER_COORDS = (LATTICE_DIMENSIONS[0] // 4, LATTICE_DIMENSIONS[1] // 2)
CYLINDER_RADIUS = LATTICE_DIMENSIONS[1] // 12
VELOCITY_LATTICE_UNITS = 0.06  # inflow speed U (Mach number U / c_s = 0.10)
STEPS_PER_FRAME = 10  # LBM time steps between animation frames
N_FRAMES = 3000  # default frames: 30 000 time steps, shedding starts near 20 000
VORTICITY_SCALE = 3.0  # vorticity colour range: -3 to 3 in units of U / r
# Diverging map with a dark centre (Matplotlib >= 3.10); coolwarm on older versions
VORTICITY_CMAP = "berlin" if "berlin" in colormaps else "coolwarm"

# Relaxation parameter omega = 1 / tau with nu = c_s^2 (tau - 1/2), c_s^2 = 1/3
VISCOSITY_LATTICE_UNITS = VELOCITY_LATTICE_UNITS * CYLINDER_RADIUS / REYNOLDS_NUMBER
RELAXATION_PARAMETER = 1.0 / (3.0 * VISCOSITY_LATTICE_UNITS + 0.5)

# Lattice constants
LATTICE_VELOCITIES = np.array([(x, y) for x in [0, -1, 1] for y in [0, -1, 1]])
LATTICE_WEIGHTS = np.ones(NUM_POPULATIONS) / 36.0
LATTICE_WEIGHTS[np.linalg.norm(LATTICE_VELOCITIES, axis=1) < 1.1] = 1.0 / 9.0
LATTICE_WEIGHTS[0] = 4.0 / 9.0
NOSLIP = np.array(
    [
        LATTICE_VELOCITIES.tolist().index((-LATTICE_VELOCITIES[i]).tolist())
        for i in range(NUM_POPULATIONS)
    ]
)
INDICES_RIGHT_WALL = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] < 0]
INDICES_VERTICAL_MIDDLE = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] == 0]
INDICES_LEFT_WALL = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] > 0]


def compute_density(fin):
    """Zeroth moment: rho = sum_i f_i."""
    return np.sum(fin, axis=0)


def compute_velocity(fin, rho):
    """First moment: u = sum_i c_i f_i / rho."""
    return np.einsum("qd,qxy->dxy", LATTICE_VELOCITIES, fin) / rho


def equilibrium(rho, u):
    """Second-order D2Q9 equilibrium distribution."""
    cu = 3.0 * np.einsum("qd,dxy->qxy", LATTICE_VELOCITIES, u)
    usqr = 1.5 * (u[0] ** 2 + u[1] ** 2)
    return rho * LATTICE_WEIGHTS[:, None, None] * (1.0 + cu + 0.5 * cu**2 - usqr)


def make_obstacle(
    dimensions=LATTICE_DIMENSIONS, coords=CYLINDER_COORDS, radius=CYLINDER_RADIUS
):
    """Boolean mask of the lattice nodes inside the cylinder."""
    return np.fromfunction(
        lambda x, y: (x - coords[0]) ** 2 + (y - coords[1]) ** 2 < radius**2,
        dimensions,
    )


def make_inflow_velocity(dimensions=LATTICE_DIMENSIONS, speed=VELOCITY_LATTICE_UNITS):
    """Uniform inflow with a tiny sinusoidal perturbation that triggers shedding."""
    return np.fromfunction(
        lambda d, x, y: (
            (1 - d)
            * speed
            * (1.0 + 1e-4 * np.sin(y / (dimensions[1] - 1.0) * 2 * np.pi))
        ),
        (2, *dimensions),
    )


def lbm_step(fin, obstacle, inflow_velocity, relaxation=RELAXATION_PARAMETER):
    """Advance the populations by one time step in place; return the velocity."""
    # Right wall: zero-gradient outflow for the populations entering the domain.
    fin[INDICES_RIGHT_WALL, -1, :] = fin[INDICES_RIGHT_WALL, -2, :]

    rho = compute_density(fin)
    u = compute_velocity(fin, rho)

    # Left wall: prescribed velocity, density from the known populations.
    u[:, 0, :] = inflow_velocity[:, 0, :]
    rho[0, :] = (
        compute_density(fin[INDICES_VERTICAL_MIDDLE, 0, :])
        + 2.0 * compute_density(fin[INDICES_RIGHT_WALL, 0, :])
    ) / (1.0 - u[0, 0, :])

    feq = equilibrium(rho, u)
    # Left wall: Zou/He bounce-back of the non-equilibrium part for unknown populations.
    opposite = NOSLIP[INDICES_LEFT_WALL]
    fin[INDICES_LEFT_WALL, 0, :] = (
        feq[INDICES_LEFT_WALL, 0, :] + fin[opposite, 0, :] - feq[opposite, 0, :]
    )

    # BGK collision.
    fout = fin - relaxation * (fin - feq)

    # Full-way bounce-back inside the obstacle (no-slip wall).
    fout[:, obstacle] = fin[NOSLIP][:, obstacle]

    # Streaming (periodic in y).
    for i in range(NUM_POPULATIONS):
        fin[i] = np.roll(fout[i], shift=tuple(LATTICE_VELOCITIES[i]), axis=(0, 1))
    return u


class LatticeBoltzmannSimulation(Simulation):
    """Population state and BGK time integration, with configurable grid size.

    One step is one collision and streaming iteration (dt = 1 in lattice units).
    """

    def __init__(self, dimensions=LATTICE_DIMENSIONS):
        super().__init__()
        nx, ny = dimensions
        if nx < 12 or ny < 12:
            raise ValueError("at least 12 nodes per axis are required")
        self.radius = ny // 12
        self.viscosity = VELOCITY_LATTICE_UNITS * self.radius / REYNOLDS_NUMBER
        self.relaxation = 1.0 / (3.0 * self.viscosity + 0.5)
        self.obstacle = make_obstacle(dimensions, (nx // 4, ny // 2), self.radius)
        self.inflow_velocity = make_inflow_velocity(dimensions)
        self.populations = equilibrium(1.0, self.inflow_velocity)

    def step(self):
        lbm_step(self.populations, self.obstacle, self.inflow_velocity, self.relaxation)

    @property
    def velocity(self):
        """Velocity (2, nx, ny) of the current, streamed populations."""
        return compute_velocity(self.populations, compute_density(self.populations))

    @property
    def speed(self):
        """Velocity magnitude (nx, ny); NaN inside the cylinder."""
        speed = np.linalg.norm(self.velocity, axis=0)
        speed[self.obstacle] = np.nan
        return speed

    @property
    def vorticity(self):
        """Vorticity dv/dx - du/dy (nx, ny) by central differences; NaN inside."""
        u, v = self.velocity
        vorticity = np.gradient(v, axis=0) - np.gradient(u, axis=1)
        vorticity[self.obstacle] = np.nan
        return vorticity


class LatticeBoltzmannView(View):
    """Speed above vorticity, both normalised with the inflow speed U and radius r.

    The flow runs left to right in the window and the reel alike: two stacked
    2.9:1 maps, with their colour bars below them in a reel, fill the nearly
    square reel panel, while a single map, rotated or not, would leave two
    thirds of it empty. The vorticity map shows the vortex street as
    alternating red (counter-clockwise) and blue (clockwise) eddies. Grey marks
    the cylinder.
    """

    figsize = (10.0, 7.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        axes = figure.subplots(2, 1, sharex=True)
        panels = (
            ("speed", "viridis", (0.0, 2.0), r"Speed $|\mathbf{u}|\,/\,U$"),
            ("vorticity", VORTICITY_CMAP, (-VORTICITY_SCALE, VORTICITY_SCALE),
             r"Vorticity $\omega\, r\,/\,U$"),
        )  # fmt: skip
        self.images = {}
        for ax, (name, cmap, limits, title) in zip(axes, panels):
            self.images[name] = ax.imshow(
                self.field(name), cmap=colormaps[cmap].with_extremes(bad="0.55"),
                vmin=limits[0], vmax=limits[1], origin="lower",
                interpolation="bilinear",
            )  # fmt: skip
            figure.colorbar(
                self.images[name], ax=ax, ticks=np.linspace(*limits, 5),
                location="bottom" if portrait else "right",
            )  # fmt: skip
            ax.set(title=title, ylabel="y [nodes]")
        axes[-1].set_xlabel("x [nodes]")

    def field(self, name):
        """Normalised field in image orientation: rows are y, columns x."""
        simulation = self.simulation
        if name == "speed":
            field = simulation.speed / VELOCITY_LATTICE_UNITS
        else:
            field = simulation.vorticity * simulation.radius / VELOCITY_LATTICE_UNITS
        return field.T

    def draw(self):
        for name, image in self.images.items():
            image.set_data(self.field(name))

    def status(self):
        steps = self.simulation.steps
        diameter = 2 * self.simulation.radius
        return f"step {steps}   t U/D = {steps * VELOCITY_LATTICE_UNITS / diameter:.1f}"


ANIMATION = Animation(
    title="Lattice Boltzmann Cylinder Flow",
    subtitle=f"D2Q9 BGK at Re = {2 * REYNOLDS_NUMBER:g} (diameter): vortex street",
    filename="lattice_boltzmann_cylinder_flow.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="lattice Boltzmann time steps",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, LatticeBoltzmannSimulation(), LatticeBoltzmannView)
    print(
        f"Re = {REYNOLDS_NUMBER:g} (radius), omega = {RELAXATION_PARAMETER:.4f}, "
        f"tau = {1 / RELAXATION_PARAMETER:.4f}: {simulation.steps} time steps, "
        f"max |u| / U = {np.nanmax(simulation.speed) / VELOCITY_LATTICE_UNITS:.2f}"
    )


if __name__ == "__main__":
    main()
