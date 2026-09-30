"""Proper Orthogonal Decomposition (POD) of synthetic flow data via the SVD.

Builds a synthetic spatio-temporal field made of three separable structures,
subtracts the temporal mean, computes the thin SVD of the snapshot matrix and
plots the three leading spatial modes next to their temporal coefficients.
"""

import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import (  # noqa: E402
    PODResult,
    compute_pod,
    create_snapshot_matrix,
    generate_synthetic_data,
)
from _plotting import plot_pod_mode_pairs  # noqa: E402

N_SAMPLES = 100  # number of time snapshots
N_X = 50  # number of spatial points in x
N_Y = 30  # number of spatial points in y
NUM_MODES = 3  # modes to plot


def plot_modes_and_time_coeffs(
    pod: PODResult, x: np.ndarray, y: np.ndarray, t: np.ndarray, num_modes: int = 3
):
    """Plot the spatial modes (left) and their temporal coefficients (right)."""
    if not 1 <= num_modes <= len(pod.singular_values):
        raise ValueError("requested modes exceed the retained rank")
    modes = pod.modes[:, :num_modes].reshape(len(x), len(y), num_modes)
    return plot_pod_mode_pairs(x, y, t, modes, pod.coefficients[:num_modes])


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    data, x, y, t = generate_synthetic_data(N_SAMPLES, N_X, N_Y)
    pod = compute_pod(create_snapshot_matrix(data))

    for i, fraction in enumerate(pod.energy_fractions[:NUM_MODES], start=1):
        print(f"Mode {i}: {fraction:.2%} of the fluctuation energy")

    fig = plot_modes_and_time_coeffs(pod, x, y, t, num_modes=NUM_MODES)

    finish_figures({"pod_modes.png": fig}, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
