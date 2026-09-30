"""Visualise a scrambled Sobol design of experiments for geometry variants.

A four-dimensional scrambled Sobol sequence is drawn in the unit hypercube, one
dimension per normalised geometry parameter. Two 2D projections of the same
design are plotted side by side to show how evenly the low-discrepancy points
cover each parameter plane. In a real workflow each sample would be mapped to a
deformed mesh and simulated.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from scipy.stats.qmc import Sobol

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0  # seed for the Sobol scrambling
LOG2_SAMPLES = 9  # 2**9 = 512 samples; Sobol balance needs a power of two
PARAMETERS = ("Approach_Angle", "Variable_1", "Decklid_Height", "Variable_2")


def generate_design(log2_samples=LOG2_SAMPLES, dimension=len(PARAMETERS), seed=SEED):
    """Return an array of shape (2**log2_samples, dimension) in [0, 1)^dimension."""
    sobol = Sobol(d=dimension, scramble=True, rng=seed)
    return sobol.random_base2(m=log2_samples)


def make_figure(samples, parameters=PARAMETERS):
    """Scatter (param 0, param 1) and (param 2, param 3) in two panels."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, (i, j) in zip(axes, [(0, 1), (2, 3)]):
        ax.scatter(samples[:, i], samples[:, j], color="blue", s=12)
        ax.set_title("2D design space distribution")
        ax.set_xlabel(f"{parameters[i]} (normalised)")
        ax.set_ylabel(f"{parameters[j]} (normalised)")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
    fig.suptitle(
        f"{len(samples)} geometry variants from a {samples.shape[1]}D scrambled "
        "Sobol sequence (all shown)"
    )
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    samples = generate_design()
    fig = make_figure(samples)

    finish_figures(
        {"design_space_distribution.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
