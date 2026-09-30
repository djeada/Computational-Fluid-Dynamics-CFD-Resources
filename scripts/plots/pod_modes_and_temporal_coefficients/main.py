"""First three POD spatial modes and their temporal coefficients for a synthetic 2-D field.

A space-time field u(x, y, t) on a 50 x 30 x 100 grid is built from three
separable structures with decreasing amplitude plus seeded noise. The field
is reshaped into an (Nx Ny) x Nt snapshot matrix, the temporal mean is
removed, and the SVD gives the spatial modes (contour plots) and temporal
coefficients a_i(t) = sigma_i psi_i(t) (time series).
"""

import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod, create_snapshot_matrix  # noqa: E402
from _plotting import plot_pod_mode_pairs  # noqa: E402

N_X, N_Y, N_T = 50, 30, 100  # grid points in x, y and number of snapshots
X_RANGE = (1700.0, 2000.0)  # streamwise extent [mm]
Y_RANGE = (0.0, 100.0)  # wall-normal extent [mm]
T_END = 4.0  # duration of the record [s]
# Separable structures A * sin(p pi xi) sin(q pi eta) * g(t), xi, eta in [0, 1]
STRUCTURES = [
    (1.0, 1, 1, lambda t: np.sin(np.pi * t)),
    (0.6, 2, 1, lambda t: np.sin(2 * np.pi * t)),
    (0.3, 1, 2, lambda t: np.cos(3 * np.pi * t)),
]
NOISE_STD = 0.02  # standard deviation of the random fluctuations [-]
SEED = 42  # random seed
N_MODES = 3  # number of modes to plot


def generate_field(noise_std=NOISE_STD, seed=SEED):
    """Return x, y, t and the field u with shape (N_X, N_Y, N_T)."""
    rng = np.random.default_rng(seed)
    x = np.linspace(*X_RANGE, N_X)
    y = np.linspace(*Y_RANGE, N_Y)
    t = np.linspace(0.0, T_END, N_T)
    X, Y, T = np.meshgrid(x, y, t, indexing="ij")
    xi = (X - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])
    eta = (Y - Y_RANGE[0]) / (Y_RANGE[1] - Y_RANGE[0])
    field = np.zeros_like(X)
    for amplitude, p, q, g in STRUCTURES:
        field += amplitude * np.sin(p * np.pi * xi) * np.sin(q * np.pi * eta) * g(T)
    field += noise_std * rng.standard_normal(field.shape)
    return x, y, t, field


def pod(field, n_modes=N_MODES):
    """SVD-based POD of the mean-subtracted (Nx Ny) x Nt snapshot matrix.

    Returns the spatial modes reshaped to (N_X, N_Y, n_modes), the temporal
    coefficients a_i(t) = sigma_i psi_i(t) with shape (n_modes, N_T), and the
    fraction of energy in every mode.
    """
    nx, ny, _ = field.shape
    result = compute_pod(create_snapshot_matrix(field))
    if not 1 <= n_modes <= len(result.singular_values):
        raise ValueError("n_modes must be between one and the retained rank")
    modes = result.modes[:, :n_modes].reshape(nx, ny, n_modes)
    return modes, result.coefficients[:n_modes], result.energy_fractions


def plot_modes(x, y, t, modes, time_coeffs, energy_fraction):
    """Contour plots of the modes (left) and their time coefficients (right)."""
    return plot_pod_mode_pairs(x, y, t, modes, time_coeffs, energy_fraction)


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    x, y, t, field = generate_field()
    modes, time_coeffs, energy_fraction = pod(field)
    for i in range(min(N_MODES + 1, len(energy_fraction))):
        print(f"mode {i + 1}: TKE = {100 * energy_fraction[i]:.2f} %")

    fig = plot_modes(x, y, t, modes, time_coeffs, energy_fraction)

    finish_figures(
        {"pod_modes_and_temporal_coefficients.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
