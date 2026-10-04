"""Interactive 2D smoke simulation with Jos Stam's Stable Fluids method.

Velocity and a passive density field live on a collocated grid inside a closed
box. Each step diffuses (Jacobi iterations of the implicit system), projects,
semi-Lagrangian-advects and projects the velocity again, then diffuses and
advects the density, which is shown as smoke. Left-click in the window to
inject density and a random velocity kick; without a window (``--no-show`` or
``--reel``), or with ``--auto-inject``, a seeded rising, swaying plume is
injected automatically.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

SEED = 0
GRID_WIDTH, GRID_HEIGHT = 200, 150  # grid cells, walls included
DIFFUSION = 0.0001  # density diffusion coefficient
VISCOSITY = 0.0001  # kinematic viscosity
TIME_STEP = 0.1
SOLVER_ITERATIONS = 20  # Jacobi iterations for diffusion and pressure
CLICK_DENSITY = 1000  # density added by a mouse click
CLICK_VELOCITY = 200  # maximum random velocity component added by a click
PLUME_DENSITY = 0.25  # density added per source cell per step (scripted plume)
PLUME_VELOCITY = 0.15  # upward velocity added per source cell per step
PLUME_SWAY = 0.08  # amplitude of the sideways velocity added per step
DENSITY_BLUE = 0.255  # density drawn as full blue; twice this is drawn white
STEPS_PER_FRAME = 2  # solver steps between drawn frames
N_FRAMES = 450  # frames of a headless run or reel (900 steps, t = 90)


class FluidSimulation(Simulation):
    """Stable Fluids state; ``step`` adds the plume (if enabled) and advances."""

    def __init__(
        self,
        width=GRID_WIDTH,
        height=GRID_HEIGHT,
        diffusion=DIFFUSION,
        viscosity=VISCOSITY,
        dt=TIME_STEP,
        auto_inject=False,
        seed=SEED,
    ):
        super().__init__()
        self.size = (height, width)
        self.dt = dt
        self.diff = diffusion
        self.visc = viscosity
        self.auto_inject = auto_inject
        self.rng = np.random.default_rng(seed)  # plume noise and click kicks

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

    def add_click(self, x, y):
        """A left click: a puff of density with a random velocity kick."""
        self.add_density(x, y, CLICK_DENSITY)
        self.add_velocity(
            x,
            y,
            self.rng.uniform(-CLICK_VELOCITY, CLICK_VELOCITY),
            self.rng.uniform(-CLICK_VELOCITY, CLICK_VELOCITY),
        )

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
        if self.auto_inject:
            inject_plume(self, self.steps, self.rng)
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


class FluidView(View):
    """Smoke density from black through blue to white; left-click adds smoke.

    Row 0 of the grid is the top of the box, so the image is drawn with
    ``origin="upper"`` and the y axis counts cells downwards.
    """

    figsize = (8.0, 6.6)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        self.ax = figure.subplots()
        smoke = LinearSegmentedColormap.from_list("smoke", ["black", "blue", "white"])
        self.image = self.ax.imshow(
            simulation.density, origin="upper", cmap=smoke, vmin=0.0,
            vmax=2 * DENSITY_BLUE, interpolation="bilinear",
        )  # fmt: skip
        figure.colorbar(
            self.image, ax=self.ax, label="smoke density",
            location="bottom" if portrait else "right",
        )  # fmt: skip
        self.ax.set(xlabel="x [cells]", ylabel="y [cells]")
        figure.canvas.mpl_connect("button_press_event", self.on_click)

    def on_click(self, event):
        """Left-click inside the box: smoke and a random kick at that cell."""
        toolbar = self.figure.canvas.toolbar
        if event.button != 1 or event.inaxes is not self.ax:
            return
        if toolbar is not None and toolbar.mode:  # zooming or panning
            return
        height, width = self.simulation.size
        x, y = int(round(event.xdata)), int(round(event.ydata))
        if 0 <= x < width and 0 <= y < height:
            self.simulation.add_click(x, y)

    def draw(self):
        self.image.set_data(self.simulation.density)

    def status(self):
        return f"t = {self.simulation.time:.1f}"


ANIMATION = Animation(
    title="Stable Fluids Smoke",
    subtitle="A swaying plume in a closed box, Stam's method",
    filename="simplified_real_time_fluid_dynamics_simulator.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"solver steps of dt = {TIME_STEP:g}",
    endless=True,
)


def main(argv=None):
    parser = ANIMATION.parser(__doc__)
    parser.add_argument(
        "--auto-inject",
        action="store_true",
        help="inject the scripted plume in the window too "
        "(always on with --no-show or --reel)",
    )
    args = parser.parse_args(argv)
    auto_inject = args.auto_inject or args.no_show or args.reel is not None
    simulation = ANIMATION.run(
        args, FluidSimulation(auto_inject=auto_inject), FluidView
    )
    density = simulation.density[1:-1, 1:-1]
    print(
        f"t = {simulation.time:g} after {simulation.steps} solver steps: smoke "
        f"density max {density.max():.3f}, mean {density.mean():.4f}"
    )


if __name__ == "__main__":
    main()
