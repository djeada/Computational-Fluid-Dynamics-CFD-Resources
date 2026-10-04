"""2D wave equation on a square with fixed edges, solved by explicit leapfrog.

A Gaussian pulse at rest in the centre of [-L, L]^2 spreads outward as a
circular ring, reflects with inverted sign from the fixed (u = 0) edges and
interferes with itself. The displacement u is shown as a 3D surface coloured
by height.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Physical parameters (nondimensional)
L = 5.0  # half-width of the square domain [-L, L]^2
C = 1.0  # wave speed c
SCALE_FACTOR = 5.0  # amplitude A of the initial Gaussian pulse

# Numerical parameters
NX = 100  # grid points in x
NY = 100  # grid points in y
CFL_SAFETY = 0.5  # dt = CFL_SAFETY * min(dx, dy) / (c * sqrt(2))
T_END = 40.0  # simulated time of the default run
# dt of the default grid (make_grid computes it for any grid): about 0.0357
TIME_STEP = CFL_SAFETY * 2 * L / (max(NX, NY) - 1) / (C * np.sqrt(2))
STEPS_PER_FRAME = 4  # leapfrog steps per animation frame
N_FRAMES = int(T_END / TIME_STEP) // STEPS_PER_FRAME  # 280 frames reach t = 40
COLORMAP = "viridis"
COLOR_LIMIT = 2.0  # colour scale -2 .. 2; only the start and brief focusing exceed it


def make_grid(length=L, nx=NX, ny=NY, c=C, cfl_safety=CFL_SAFETY):
    """Return X, Y, dx, dy, dt; axis 0 is y and axis 1 is x."""
    if nx < 3 or ny < 3 or length <= 0 or c <= 0 or not 0 < cfl_safety <= 1:
        raise ValueError(
            "require grids >= 3, positive length/speed, and 0 < CFL safety <= 1"
        )
    x = np.linspace(-length, length, nx)
    y = np.linspace(-length, length, ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dt = cfl_safety * min(dx, dy) / (c * np.sqrt(2))
    X, Y = np.meshgrid(x, y)
    return X, Y, dx, dy, dt


def initial_condition(X, Y, dx, dy, dt, c=C, amplitude=SCALE_FACTOR):
    """Gaussian pulse with fixed edges and a second-order zero-velocity start."""
    u0 = amplitude * np.exp(-0.5 * (X**2 + Y**2))
    u0[[0, -1], :] = 0.0
    u0[:, [0, -1]] = 0.0
    _, first_order = leapfrog_step(u0, u0, dx, dy, dt, c)
    u_prev = u0 + 0.5 * (first_order - u0)
    return u_prev, u0


def leapfrog_step(u_prev, u, dx, dy, dt, c=C):
    """Return (u, u_new) after one leapfrog step with u = 0 on the boundary."""
    u_new = np.zeros_like(u)
    u_new[1:-1, 1:-1] = (
        2 * u[1:-1, 1:-1]
        - u_prev[1:-1, 1:-1]
        + (c * dt) ** 2
        * (
            (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dx**2  # axis 1 = x
            + (u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dy**2  # axis 0 = y
        )
    )
    return u, u_new


class WaveSimulation(Simulation):
    """Two leapfrog time levels of the wave field on a fixed grid."""

    def __init__(self, length=L, nx=NX, ny=NY, c=C, cfl_safety=CFL_SAFETY):
        super().__init__()
        self.X, self.Y, self.dx, self.dy, self.dt = make_grid(
            length, nx, ny, c, cfl_safety
        )
        self.c = c
        self.u_prev, self.u = initial_condition(
            self.X, self.Y, self.dx, self.dy, self.dt, c
        )

    def step(self):
        self.u_prev, self.u = leapfrog_step(
            self.u_prev, self.u, self.dx, self.dy, self.dt, self.c
        )


class WaveView(View):
    """Surface of u over the square on fixed height and colour scales.

    The height axis spans the initial amplitude. The colour scale is narrower,
    so the weaker rings after the first spreading still show crests and
    troughs; the initial pulse and brief focusing peaks saturate it. The
    surface is re-plotted for every frame. In a reel the colour bar sits
    below the surface.
    """

    figsize = (8.0, 6.5)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        self.ax = figure.add_subplot(projection="3d")
        self.norm = Normalize(-COLOR_LIMIT, COLOR_LIMIT)
        figure.colorbar(
            ScalarMappable(self.norm, COLORMAP), ax=self.ax, extend="both",
            label="displacement u", shrink=0.6,
            location="bottom" if portrait else "right",
        )  # fmt: skip
        self.ax.set(
            xlim=(simulation.X.min(), simulation.X.max()),
            ylim=(simulation.Y.min(), simulation.Y.max()),
            zlim=(-SCALE_FACTOR, SCALE_FACTOR),
            xlabel="x", ylabel="y", zlabel="u",
        )  # fmt: skip
        # Zoom into the margin the 3D axes leaves around the box. The reel panel
        # is nearly square, so a taller box fills it (and exaggerates heights).
        self.ax.set_box_aspect((4, 4, 4) if portrait else None, zoom=1.1)
        if portrait:  # keep the large axis labels clear of the tick labels
            self.ax.xaxis.labelpad = self.ax.yaxis.labelpad = 18
        self.surface = None

    def draw(self):
        if self.surface is not None:
            self.surface.remove()
        simulation = self.simulation
        self.surface = self.ax.plot_surface(
            simulation.X, simulation.Y, simulation.u, cmap=COLORMAP, norm=self.norm
        )

    def status(self):
        return f"t = {self.simulation.time:.2f}"


ANIMATION = Animation(
    title="2D Wave Equation",
    subtitle="A pulse spreads and reflects off fixed edges",
    filename="wave_2d.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"leapfrog steps of dt = {TIME_STEP:.4f}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, WaveSimulation(), WaveView)
    print(
        f"t = {simulation.time:.2f} after {simulation.steps} steps of "
        f"dt = {simulation.dt:.4f}: u from {simulation.u.min():.3f} "
        f"to {simulation.u.max():.3f}"
    )


if __name__ == "__main__":
    main()
