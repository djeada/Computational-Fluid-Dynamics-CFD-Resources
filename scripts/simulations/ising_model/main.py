"""Simulate the 2D Ising model with the Metropolis algorithm and animate it.

A square lattice of +/-1 spins with periodic boundaries (J = 1, k_B = 1) starts
from a random configuration and is evolved at inverse temperature beta by
Metropolis Monte Carlo sweeps, accelerated with Numba. The animation shows the
spin lattice together with the total magnetization and energy versus sweeps.
"""

import sys
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from numba import njit

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int, save_figure  # noqa: E402

N_ROWS, N_COLS = 300, 300  # lattice size
BETA = 0.6  # inverse temperature 1/(k_B T); critical value ln(1 + sqrt 2)/2 ~ 0.4407
WARMUP_STEPS = 1  # sweeps run before the animation starts
TOTAL_STEPS = 3000  # Monte Carlo sweeps in the animation
UPDATE_INTERVAL = 5  # record/draw every this many sweeps
INTERVAL_MS = 100  # delay between animation frames
SEED = 0  # random seed (NumPy and Numba generators)
SAVE_ANIMATION = False  # write the animation to SAVE_PATH instead of showing it
SAVE_PATH = "ising_simulation.gif"


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


def run_simulation_numba(lattice, beta, steps, update_interval=1):
    """Yield (sweeps done, lattice copy, M, E) every update_interval sweeps.

    The final sweep is always yielded so the last frame shows the end state.
    """
    for step in range(steps):
        lattice = metropolis_step_numba(lattice, beta)
        if (step + 1) % update_interval == 0 or step == steps - 1:
            mag_val = calculate_magnetization_numba(lattice)
            energy_val = calculate_energy_numba(lattice)
            yield step + 1, lattice.copy(), mag_val, energy_val


def setup_figure(lattice, steps):
    """Create the lattice, magnetization and energy panels."""
    plt.style.use("dark_background")
    cmap = ListedColormap(["#1F77B4", "#FF7F0E"])  # -1 (blue), +1 (orange)

    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[4, 1], hspace=0.3)

    ax_lattice = fig.add_subplot(gs[0, :])
    img = ax_lattice.imshow(
        lattice, cmap=cmap, interpolation="nearest", aspect="equal", vmin=-1, vmax=1
    )
    ax_lattice.axis("off")
    legend_elements = [
        Patch(facecolor="#FF7F0E", edgecolor="#FF7F0E", label="Spin Up"),
        Patch(facecolor="#1F77B4", edgecolor="#1F77B4", label="Spin Down"),
    ]
    legend = ax_lattice.legend(
        handles=legend_elements,
        loc="upper right",
        facecolor="black",
        edgecolor="white",
        prop={"size": 12},
    )
    for text in legend.get_texts():
        text.set_color("white")

    def kilo_formatter(x, pos):
        return f"{x / 1000:.0f}k"

    ax_mag = fig.add_subplot(gs[1, 0])
    (mag_line,) = ax_mag.plot([], [], color="white", linewidth=2)
    ax_mag.set_xlim(0, steps)
    ax_mag.set_ylim(-lattice.size, lattice.size)  # M ranges over [-N, N]
    ax_mag.set_title("Magnetization", color="white")
    ax_mag.set_xlabel("Monte Carlo sweeps", color="white")
    ax_mag.set_ylabel("Magnetization", color="white")
    ax_mag.yaxis.set_major_formatter(FuncFormatter(kilo_formatter))

    ax_energy = fig.add_subplot(gs[1, 1])
    (energy_line,) = ax_energy.plot([], [], color="white", linewidth=2)
    ax_energy.set_xlim(0, steps)
    ax_energy.set_ylim(-2 * lattice.size, 2 * lattice.size)  # E ranges over [-2N, 2N]
    ax_energy.set_title("Energy", color="white")
    ax_energy.set_xlabel("Monte Carlo sweeps", color="white")
    ax_energy.set_ylabel("Energy", color="white")
    ax_energy.yaxis.set_major_formatter(FuncFormatter(kilo_formatter))

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    return fig, ax_lattice, img, mag_line, energy_line


def animate_simulation(
    lattice,
    beta,
    steps,
    interval_ms=50,
    update_interval=10,
    save_path=None,
    show=True,
):
    """Run the simulation, animating it if show is True; return the figure."""
    fig, ax_lattice, img, mag_line, energy_line = setup_figure(lattice, steps)
    simulation = run_simulation_numba(lattice, beta, steps, update_interval)

    steps_record_plot = []
    mag_data_plot = []
    energy_data_plot = []

    def init_animation():
        img.set_data(lattice)
        mag_line.set_data([], [])
        energy_line.set_data([], [])
        return img, mag_line, energy_line

    def update_animation(frame):
        step, current_lattice, mag, energy = frame
        img.set_data(current_lattice)
        mag_data_plot.append(mag)
        energy_data_plot.append(energy)
        steps_record_plot.append(step)
        mag_line.set_data(steps_record_plot, mag_data_plot)
        energy_line.set_data(steps_record_plot, energy_data_plot)
        ax_lattice.set_title(f"Sweep: {step}", color="white", fontsize=16)
        return img, mag_line, energy_line

    if not show and not save_path:
        for frame in simulation:
            update_animation(frame)
        return fig

    ani = animation.FuncAnimation(
        fig,
        update_animation,
        frames=simulation,
        init_func=init_animation,
        blit=False,
        interval=interval_ms,
        repeat=False,
        cache_frame_data=False,
    )
    if save_path:
        writer = "pillow" if save_path.endswith(".gif") else "ffmpeg"
        ani.save(save_path, writer=writer, fps=1000 // interval_ms)
    else:
        plt.show()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=TOTAL_STEPS,
        help=f"number of Monte Carlo sweeps (default {TOTAL_STEPS})",
    )
    args = parser.parse_args(argv)

    rng = np.random.default_rng(SEED)
    seed_numba(SEED)
    initial_lattice = initialize_lattice(N_ROWS, N_COLS, rng)

    # Short equilibration phase before the animation starts
    for _ in range(WARMUP_STEPS):
        initial_lattice = metropolis_step_numba(initial_lattice, BETA)

    fig = animate_simulation(
        lattice=initial_lattice,
        beta=BETA,
        steps=args.steps,
        interval_ms=INTERVAL_MS,
        update_interval=UPDATE_INTERVAL,
        save_path=SAVE_PATH if SAVE_ANIMATION and not args.no_show else None,
        show=not args.no_show,
    )

    if args.output:
        save_figure(fig, args.output, "ising_model.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
