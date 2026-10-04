"""Simulate the 2D Ising model with the Metropolis algorithm and animate it.

A square lattice of +/-1 spins with periodic boundaries (J = 1, k_B = 1) starts
from a random configuration and is evolved at inverse temperature beta by
Metropolis Monte Carlo sweeps, accelerated with Numba. The animation shows the
spin lattice together with the total magnetization and energy versus sweeps.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

N_ROWS, N_COLS = 300, 300  # lattice size [sites]
BETA = 0.6  # inverse temperature 1/(k_B T); critical value ln(1 + sqrt 2)/2 ~ 0.4407
WARMUP_STEPS = 1  # sweeps run before sweep 0 of the animation
STEPS_PER_FRAME = 5  # Monte Carlo sweeps per animation frame
N_FRAMES = 3000 // STEPS_PER_FRAME  # default frames -> 3000 sweeps
SEED = 0  # random seed (NumPy and Numba generators)
SPIN_DOWN_COLOR, SPIN_UP_COLOR = "#1F77B4", "#FF7F0E"  # -1 blue, +1 orange


@njit
def seed_numba(seed):
    """Seed Numba's internal random generator (separate from NumPy's)."""
    np.random.seed(seed)


@njit
def metropolis_step_numba(lattice, beta):
    """Perform one Monte Carlo sweep (N random single-spin-flip attempts)."""
    n_rows, n_cols = lattice.shape
    for _ in range(n_rows * n_cols):
        i = np.random.randint(0, n_rows)
        j = np.random.randint(0, n_cols)

        spin = lattice[i, j]
        # Sum of the four nearest neighbours (periodic boundary conditions)
        neighbors = (
            lattice[(i + 1) % n_rows, j]
            + lattice[i, (j + 1) % n_cols]
            + lattice[(i - 1) % n_rows, j]
            + lattice[i, (j - 1) % n_cols]
        )
        delta_E = 2 * spin * neighbors

        # Metropolis acceptance rule
        if delta_E <= 0 or np.random.random() < np.exp(-delta_E * beta):
            lattice[i, j] = -spin
    return lattice


@njit
def calculate_energy_numba(lattice):
    """Return H = -sum over nearest-neighbour bonds of s_i s_j (each bond once)."""
    energy = 0
    n_rows, n_cols = lattice.shape
    for i in range(n_rows):
        for j in range(n_cols):
            spin = lattice[i, j]
            neighbors = lattice[(i + 1) % n_rows, j] + lattice[i, (j + 1) % n_cols]
            energy -= spin * neighbors
    return energy


@njit
def calculate_magnetization_numba(lattice):
    """Return M = sum of all spins."""
    mag = 0
    n_rows, n_cols = lattice.shape
    for i in range(n_rows):
        for j in range(n_cols):
            mag += lattice[i, j]
    return mag


def initialize_lattice(n_rows: int, n_cols: int, rng) -> np.ndarray:
    """Return a random +/-1 lattice stored as int8."""
    return rng.choice(np.array([-1, 1], dtype=np.int8), size=(n_rows, n_cols))


class IsingSimulation(Simulation):
    """Spin lattice with M and E recorded after every sweep.

    Numba's random generator is global, so constructing a simulation reseeds
    it: runs are reproducible as long as one simulation is advanced at a time.
    ``magnetization[k]`` and ``energy[k]`` belong to sweep ``k`` (0 = start).
    """

    def __init__(
        self, n_rows=N_ROWS, n_cols=N_COLS, beta=BETA, seed=SEED, warmup=WARMUP_STEPS
    ):
        super().__init__()
        self.beta = beta
        rng = np.random.default_rng(seed)
        seed_numba(seed)
        self.lattice = initialize_lattice(n_rows, n_cols, rng)
        for _ in range(warmup):  # short equilibration before sweep 0
            metropolis_step_numba(self.lattice, beta)
        self.magnetization = []
        self.energy = []
        self.record()

    def record(self):
        self.magnetization.append(int(calculate_magnetization_numba(self.lattice)))
        self.energy.append(int(calculate_energy_numba(self.lattice)))

    def step(self):
        metropolis_step_numba(self.lattice, self.beta)
        self.record()


def kilo(value, _position):
    return f"{value / 1000:.0f}k" if value else "0"


class IsingView(View):
    """Spin lattice (orange up, blue down) with M and E histories.

    The window puts the lattice left of the two histories; a reel puts it on
    top with M and E side by side below. ``sweeps`` sets the initial x range
    of the histories, which widens if the run goes on longer.
    """

    figsize = (12.0, 6.0)

    def __init__(
        self, simulation, figure, portrait=False, sweeps=N_FRAMES * STEPS_PER_FRAME
    ):
        super().__init__(simulation, figure, portrait)
        if portrait:
            mosaic = [["lattice", "lattice"], ["M", "E"]]
            axes = figure.subplot_mosaic(mosaic, height_ratios=[2, 1])
        else:
            mosaic = [["lattice", "M"], ["lattice", "E"]]
            axes = figure.subplot_mosaic(mosaic, width_ratios=[1, 1.15])
        self.axes = axes
        ax = axes["lattice"]
        cmap = ListedColormap([SPIN_DOWN_COLOR, SPIN_UP_COLOR])
        self.image = ax.imshow(
            simulation.lattice, cmap=cmap, vmin=-1, vmax=1, origin="upper",
            interpolation="nearest",
        )  # fmt: skip
        ax.axis("off")
        if portrait:
            # The wide top row keeps its box and centres the square lattice,
            # leaving room for the legend; a shrinking box would also shrink
            # the plots below in the compressed layout.
            ax.set_aspect("equal", adjustable="datalim")
        handles = [
            Patch(color=SPIN_UP_COLOR, label="spin up"),
            Patch(color=SPIN_DOWN_COLOR, label="spin down"),
        ]
        ax.legend(handles=handles, loc="upper right", handlelength=1, borderaxespad=0)

        n_spins = simulation.lattice.size
        self.lines = {}
        for name, title, limit in (
            ("M", "Magnetization M", n_spins),  # -N <= M <= N
            ("E", "Energy E", 2 * n_spins),  # -2N <= E <= 2N
        ):
            ax = axes[name]
            (self.lines[name],) = ax.plot([], [], color="white")
            ax.set(xlim=(0, sweeps), ylim=(-limit, limit), title=title)
            ax.set_xlabel("sweeps" if portrait else "Monte Carlo sweeps")
            ax.yaxis.set_major_formatter(FuncFormatter(kilo))
        if not portrait:
            axes["M"].set_xlabel("")
        self.sweeps = sweeps

    def draw(self):
        simulation = self.simulation
        sweeps = np.arange(len(simulation.magnetization))
        self.image.set_data(simulation.lattice)
        self.lines["M"].set_data(sweeps, simulation.magnetization)
        self.lines["E"].set_data(sweeps, simulation.energy)
        for name in ("M", "E"):
            self.axes[name].set_xlim(0, max(self.sweeps, simulation.steps))

    def status(self):
        return f"β = {self.simulation.beta:g}   sweep {self.simulation.steps}"


ANIMATION = Animation(
    title="2D Ising Model",
    subtitle="Domains grow below the critical temperature",
    filename="ising_model.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label="Monte Carlo sweeps",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    frames = ANIMATION.frames if args.steps is None else args.steps
    simulation = ANIMATION.run(
        args, IsingSimulation(), IsingView, sweeps=frames * STEPS_PER_FRAME
    )
    n_spins = simulation.lattice.size
    print(
        f"sweep {simulation.steps} at beta = {simulation.beta:g}: "
        f"M/N = {simulation.magnetization[-1] / n_spins:.4f}, "
        f"E/N = {simulation.energy[-1] / n_spins:.4f}"
    )


if __name__ == "__main__":
    main()
