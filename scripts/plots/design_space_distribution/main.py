"""Visualise a scrambled Sobol design of experiments for geometry variants.

A four-dimensional scrambled Sobol sequence of 512 points is drawn in the unit
hypercube, one dimension per normalised geometry parameter, and shown as a
scatter matrix: every 2D projection below the diagonal, the 1D marginal
histograms on the diagonal, and above the diagonal the centred L2 discrepancy
of each 2D projection next to that of a pseudo-random design of the same size.
In a real workflow each sample would be mapped to a deformed mesh and simulated.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0  # seed for the Sobol scrambling and the random comparison design
LOG2_SAMPLES = 9  # 2**9 = 512 samples; Sobol balance needs a power of two
PARAMETERS = ("Ramp angle", "Windscreen angle", "Ground clearance", "Diffuser angle")
N_BINS = 16  # marginal histogram bins (512 / 16 = 32 points per bin if even)


def generate_design(log2_samples=LOG2_SAMPLES, dimension=len(PARAMETERS), seed=SEED):
    """Return an array of shape (2**log2_samples, dimension) in [0, 1)^dimension."""
    sobol = qmc.Sobol(d=dimension, scramble=True, rng=seed)
    return sobol.random_base2(m=log2_samples)


def random_design(n, dimension=len(PARAMETERS), seed=SEED):
    """Pseudo-random design of the same size, for comparison."""
    return np.random.default_rng(seed).random((n, dimension))


def centred_l2_discrepancy(samples):
    """Centred L2 discrepancy (scipy's ``method="CD"`` returns its square)."""
    return float(np.sqrt(qmc.discrepancy(samples, method="CD")))


def min_pairwise_distance(samples):
    """Smallest Euclidean distance between two design points."""
    diff = samples[:, None, :] - samples[None, :, :]
    dist = np.sqrt((diff**2).sum(axis=-1))
    return float(dist[np.triu_indices(len(samples), k=1)].min())


def make_figure(samples, reference, parameters=PARAMETERS):
    """Scatter matrix of the design with marginal histograms and discrepancies."""
    d = samples.shape[1]
    fig, axes = plt.subplots(d, d, figsize=(12, 12))
    bins = np.linspace(0, 1, N_BINS + 1)
    expected = len(samples) / N_BINS
    for i in range(d):
        for j in range(d):
            ax = axes[i, j]
            if i == j:
                ax.hist(
                    samples[:, j],
                    bins=bins,
                    color="tab:blue",
                    edgecolor="white",
                    label="Sobol",
                )
                ax.hist(
                    reference[:, j],
                    bins=bins,
                    histtype="step",
                    color="tab:gray",
                    linewidth=1.5,
                    label="random",
                )
                if i == 0:
                    ax.legend(fontsize=9, loc="upper right")
                ax.axhline(expected, color="k", linestyle=":", linewidth=1)
                ax.set_ylim(0, 2 * expected)
                ax.set_yticks([0, expected])
            elif i > j:
                ax.scatter(samples[:, j], samples[:, i], s=4, color="tab:blue")
                ax.set_ylim(0, 1)
            else:
                pair = [j, i]
                cd_sobol = centred_l2_discrepancy(samples[:, pair])
                cd_rand = centred_l2_discrepancy(reference[:, pair])
                ax.text(
                    0.5,
                    0.5,
                    f"$CD_2$ of projection\nSobol: {cd_sobol:.4f}\nrandom: {cd_rand:.4f}",
                    ha="center",
                    va="center",
                    fontsize=11,
                    transform=ax.transAxes,
                )
                ax.set_xticks([])
                ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_color("0.8")
                continue
            ax.set_xlim(0, 1)
            if i == d - 1:
                ax.set_xlabel(parameters[j], fontsize=11)
            else:
                ax.tick_params(labelbottom=False)
            if j == 0 and i > 0:
                ax.set_ylabel(parameters[i], fontsize=11)
            elif i == j:
                ax.set_ylabel("count", fontsize=9)
            else:
                ax.tick_params(labelleft=False)
    fig.suptitle(
        f"{len(samples)} geometry variants from a {d}D scrambled Sobol sequence "
        "(normalised parameters)\nDiagonal: marginal histograms of the Sobol design and of a "
        "random design of the same size; dotted line = uniform count per bin",
        fontsize=13,
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    samples = generate_design()
    reference = random_design(len(samples))
    for name, design in (("Sobol", samples), ("random", reference)):
        counts = [
            np.histogram(design[:, k], bins=N_BINS, range=(0, 1))[0]
            for k in range(design.shape[1])
        ]
        print(
            f"{name:6s}: CD_2 (4D) = {centred_l2_discrepancy(design):.4f}, "
            f"min distance = {min_pairwise_distance(design):.4f}, "
            f"bin counts range {min(c.min() for c in counts)}-{max(c.max() for c in counts)}"
        )
    fig = make_figure(samples, reference)

    finish_figures(
        {"design_space_distribution.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
