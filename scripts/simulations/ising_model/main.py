import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from numba import njit
import numba


# Optimize the Metropolis step with Numba
@njit
def metropolis_step_numba(lattice, beta):
    n_rows, n_cols = lattice.shape
    for _ in range(n_rows * n_cols):
        # Pick a random site
        i = np.random.randint(0, n_rows)
        j = np.random.randint(0, n_cols)

        spin = lattice[i, j]
        # Sum of the four nearest neighbors (with periodic boundary conditions)
        neighbors = (lattice[(i + 1) % n_rows, j] +
                     lattice[i, (j + 1) % n_cols] +
                     lattice[(i - 1) % n_rows, j] +
                     lattice[i, (j - 1) % n_cols])
        delta_E = 2 * spin * neighbors

        # Metropolis acceptance rule
        if delta_E < 0 or np.random.random() < np.exp(-delta_E * beta):
            lattice[i, j] = -spin
    return lattice


@njit
def calculate_energy_numba(lattice):
    energy = 0
    n_rows, n_cols = lattice.shape
    for i in range(n_rows):
        for j in range(n_cols):
            spin = lattice[i, j]
            neighbors = lattice[(i + 1) % n_rows, j] + lattice[
                i, (j + 1) % n_cols]
            energy -= spin * neighbors
    return energy


@njit
def calculate_magnetization_numba(lattice):
    mag = 0
    n_rows, n_cols = lattice.shape
    for i in range(n_rows):
        for j in range(n_cols):
            mag += lattice[i, j]
    return mag


def initialize_lattice(n_rows: int, n_cols: int) -> np.ndarray:
    # Initialize the lattice with random spins up or down as int8 for memory efficiency
    return np.random.choice([-1, 1], size=(n_rows, n_cols)).astype(np.int8)


def run_simulation_numba(lattice: np.ndarray, beta: float, steps: int,
                         update_interval: int = 1):
    mag = []
    energy = []
    steps_record = []
    for step in range(steps):
        lattice = metropolis_step_numba(lattice, beta)
        if step % update_interval == 0:
            mag_val = calculate_magnetization_numba(lattice)
            energy_val = calculate_energy_numba(lattice)
            mag.append(mag_val)
            energy.append(energy_val)
            steps_record.append(step)
            # Yield as tuples
            yield step, lattice.copy(), mag_val, energy_val
    return


def animate_simulation(lattice: np.ndarray, beta: float, steps: int,
                       interval_ms: int = 50, update_interval: int = 10,
                       save_path: str = None):
    plt.style.use('dark_background')
    cmap = ListedColormap(
        ['#FF7F0E', '#1F77B4'])  # Spin Up (Orange), Spin Down (Blue)

    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[4, 1], hspace=0.3)

    # Lattice plot
    ax_lattice = fig.add_subplot(gs[0, :])
    img = ax_lattice.imshow(lattice, cmap=cmap, interpolation='nearest',
                            animated=True, aspect='equal', vmin=-1, vmax=1)
    ax_lattice.axis('off')

    # Legend for spins
    legend_elements = [
        Patch(facecolor='#FF7F0E', edgecolor='#FF7F0E', label='Spin Up'),
        Patch(facecolor='#1F77B4', edgecolor='#1F77B4', label='Spin Down')
    ]
    legend = ax_lattice.legend(
        handles=legend_elements,
        loc='upper right',
        facecolor='black',
        edgecolor='white',
        prop={'size': 12}
    )
    for text in legend.get_texts():
        text.set_color('white')

    # Function to format Y-axis ticks as "k" (kilo)
    def kilo_formatter(x, pos):
        return f'{x / 1000:.0f}k'




    # Magnetization plot
    ax_mag = fig.add_subplot(gs[1, 0])
    mag_data_plot = []
    mag_line, = ax_mag.plot([], [], color='white', linewidth=2)
    ax_mag.set_xlim(0, steps)
    ax_mag.set_ylim(-lattice.size, lattice.size)
    ax_mag.set_ylim(-lattice.size, lattice.size)
    ax_mag.set_title('Magnetization', color='white')
    ax_mag.set_xlabel('Steps', color='white')
    ax_mag.set_ylabel('Magnetization',
                      color='white')
    ax_mag.yaxis.set_major_formatter(FuncFormatter(kilo_formatter))
    ax_mag.tick_params(axis='x', colors='white')
    ax_mag.tick_params(axis='y', colors='white')

    # Energy plot
    ax_energy = fig.add_subplot(gs[1, 1])
    energy_data_plot = []
    energy_line, = ax_energy.plot([], [], color='white', linewidth=2)
    ax_energy.set_xlim(0, steps)
    # Set energy limits considering a fully aligned state ~ -2 * lattice.size is reasonable
    ax_energy.set_ylim(-2 * lattice.size, 2 * lattice.size)
    ax_energy.set_ylim(-2 * lattice.size, 2 * lattice.size)
    ax_energy.set_title('Energy', color='white')
    ax_energy.set_xlabel('Steps', color='white')
    ax_energy.set_ylabel('Energy',
                         color='white')
    ax_energy.yaxis.set_major_formatter(FuncFormatter(kilo_formatter))
    ax_energy.tick_params(axis='x', colors='white')
    ax_energy.tick_params(axis='y', colors='white')

    plt.tight_layout()
    fig.subplots_adjust(top=0.92)

    simulation = run_simulation_numba(lattice, beta, steps, update_interval)

    def init_animation():
        img.set_data(lattice)
        mag_line.set_data([], [])
        energy_line.set_data([], [])
        return img, mag_line, energy_line

    # Initialize lists to store data for plotting
    steps_record_plot = []
    mag_data_plot = []
    energy_data_plot = []

    def update_animation(frame):
        step, current_lattice, mag, energy = frame
        img.set_data(current_lattice)
        mag_data_plot.append(mag)
        energy_data_plot.append(energy)
        steps_record_plot.append(step)
        mag_line.set_data(steps_record_plot, mag_data_plot)
        energy_line.set_data(steps_record_plot, energy_data_plot)
        ax_lattice.set_title(f'Step: {step}', color='white', fontsize=16)
        return img, mag_line, energy_line

    ani = animation.FuncAnimation(
        fig, update_animation, frames=simulation,
        init_func=init_animation, blit=False,
        interval=interval_ms, repeat=False
    )

    if save_path:
        if save_path.endswith('.gif'):
            ani.save(save_path, writer='imagemagick', fps=1000 // interval_ms)
        elif save_path.endswith('.mp4'):
            ani.save(save_path, writer='ffmpeg', fps=1000 // interval_ms)
    else:
        plt.show()


if __name__ == "__main__":
    N_ROWS, N_COLS = 300, 300

    # Set beta well above critical beta for strong ordering
    BETA = 0.6

    # Run a warm-up (thermalization) phase first
    # This lets the system approach equilibrium before we start the animation
    WARMUP_STEPS = 1
    TOTAL_STEPS = 3000
    UPDATE_INTERVAL = 5
    INTERVAL_MS = 100
    SAVE_ANIMATION = False
    SAVE_PATH = "ising_simulation.gif"

    # Initialize
    initial_lattice = initialize_lattice(N_ROWS, N_COLS)

    # Equilibration phase (no animation, just evolve the system)
    for _ in range(WARMUP_STEPS):
        initial_lattice = metropolis_step_numba(initial_lattice, BETA)

    # After warm-up, start the animated simulation
    animate_simulation(
        lattice=initial_lattice,
        beta=BETA,
        steps=TOTAL_STEPS,
        interval_ms=INTERVAL_MS,
        update_interval=UPDATE_INTERVAL,
        save_path=SAVE_PATH if SAVE_ANIMATION else None
    )
