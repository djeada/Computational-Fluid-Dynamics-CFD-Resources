"""Compare random, Latin hypercube and scrambled Sobol designs in two dimensions.

Draws N = 32 points in the unit square with each of the three samplers from
scipy.stats.qmc (plus numpy for the random design), plots them with their 1D
marginal histograms, and plots the centred L2 discrepancy of each sampler
against N on log-log axes, averaged over independent seeds.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
DIMENSION = 2  # number of normalised design parameters
N_SCATTER = 32  # points per design in the scatter panels (a power of two for Sobol)
LOG2_N_RANGE = range(4, 11)  # discrepancy study: N = 16 ... 1024
N_SEEDS = 20  # independent repetitions averaged in the discrepancy study
N_HIST_BINS = (
    8  # bins of the marginal histograms (N_SCATTER / 8 = 4 points per bin if even)
)
METHODS = ("Random", "Latin hypercube", "Scrambled Sobol")
COLORS = {
    "Random": "tab:gray",
    "Latin hypercube": "tab:blue",
    "Scrambled Sobol": "tab:orange",
}


def sample(method, n, dimension=DIMENSION, seed=SEED):
    """Return an (n, dimension) design in [0, 1)^dimension drawn with ``method``."""
    if method == "Random":
        return np.random.default_rng(seed).random((n, dimension))
    if method == "Latin hypercube":
        return qmc.LatinHypercube(d=dimension, rng=seed).random(n)
    if method == "Scrambled Sobol":
        m = int(round(np.log2(n)))
        if 2**m != n:
            raise ValueError("Sobol designs here use a power-of-two sample size")
        return qmc.Sobol(d=dimension, scramble=True, rng=seed).random_base2(m)
    raise ValueError(f"unknown method {method!r}")


def stratum_counts(samples, n_strata):
    """Count points in each of ``n_strata`` equal intervals, per dimension.

    Returns an array of shape (dimension, n_strata). A Latin hypercube with
    n_strata = n has every entry equal to one.
    """
    idx = np.minimum((samples * n_strata).astype(int), n_strata - 1)
    return np.stack(
        [np.bincount(idx[:, k], minlength=n_strata) for k in range(samples.shape[1])]
    )


def min_pairwise_distance(samples):
    """Smallest Euclidean distance between two points (the maximin criterion)."""
    diff = samples[:, None, :] - samples[None, :, :]
    dist = np.sqrt((diff**2).sum(axis=-1))
    return dist[np.triu_indices(len(samples), k=1)].min()


def centred_l2_discrepancy(samples):
    """Centred L2 discrepancy CD_2 (scipy's ``method="CD"`` returns its square)."""
    return np.sqrt(qmc.discrepancy(samples, method="CD"))


def discrepancy_study(log2_n_range=LOG2_N_RANGE, n_seeds=N_SEEDS):
    """Mean centred L2 discrepancy over seeds for each method and N."""
    ns = np.array([2**m for m in log2_n_range])
    result = {}
    for method in METHODS:
        result[method] = np.array(
            [
                np.mean(
                    [
                        centred_l2_discrepancy(sample(method, n, seed=s))
                        for s in range(n_seeds)
                    ]
                )
                for n in ns
            ]
        )
    return ns, result


def fitted_slope(ns, values):
    """Least-squares slope of log(values) against log(N)."""
    return np.polyfit(np.log(ns), np.log(values), 1)[0]


def make_figure(designs, ns, disc):
    """Three scatter panels with marginal histograms, plus the discrepancy panel."""
    fig = plt.figure(figsize=(13, 9.5))
    outer = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.85], hspace=0.35, wspace=0.3)
    n = len(next(iter(designs.values())))
    grid = np.linspace(0, 1, n + 1)
    bins = np.linspace(0, 1, N_HIST_BINS + 1)
    hist_max = 2.5 * n / N_HIST_BINS
    for col, method in enumerate(METHODS):
        pts = designs[method]
        inner = outer[0, col].subgridspec(
            2, 2, width_ratios=[4, 1], height_ratios=[1, 4], wspace=0.05, hspace=0.05
        )
        ax = fig.add_subplot(inner[1, 0])
        ax_top = fig.add_subplot(inner[0, 0], sharex=ax)
        ax_right = fig.add_subplot(inner[1, 1], sharey=ax)
        for edge in grid:
            ax.axvline(edge, color="0.9", linewidth=0.6, zorder=0)
            ax.axhline(edge, color="0.9", linewidth=0.6, zorder=0)
        ax.scatter(pts[:, 0], pts[:, 1], s=28, color=COLORS[method], zorder=2)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel("$p_1$ (normalised)", fontsize=11)
        ax.set_ylabel("$p_2$ (normalised)", fontsize=11)
        ax.text(
            0.02,
            -0.27,
            f"empty columns: {np.sum(stratum_counts(pts, n)[0] == 0)}/{n}   "
            f"min distance: {min_pairwise_distance(pts):.3f}",
            transform=ax.transAxes,
            fontsize=10,
        )
        ax_top.hist(pts[:, 0], bins=bins, color=COLORS[method], edgecolor="white")
        ax_right.hist(
            pts[:, 1],
            bins=bins,
            color=COLORS[method],
            edgecolor="white",
            orientation="horizontal",
        )
        for marg in (ax_top.axhline, ax_right.axvline):
            marg(n / N_HIST_BINS, color="k", linestyle=":", linewidth=1)
        ax_top.set_title(f"{method}, N = {n}", fontsize=12)
        ax_top.set_ylim(0, hist_max)
        ax_right.set_xlim(0, hist_max)
        ax_top.set_yticks([n / N_HIST_BINS])
        ax_right.set_xticks([n / N_HIST_BINS])
        ax_top.set_ylabel("count", fontsize=9)
        ax_right.set_xlabel("count", fontsize=9)
        ax_top.tick_params(labelbottom=False, labelsize=8)
        ax_right.tick_params(labelleft=False, labelsize=8)

    ax_d = fig.add_subplot(outer[1, :])
    markers = {"Random": "o", "Latin hypercube": "s", "Scrambled Sobol": "^"}
    for method in METHODS:
        slope = fitted_slope(ns, disc[method])
        ax_d.loglog(
            ns,
            disc[method],
            marker=markers[method],
            color=COLORS[method],
            linewidth=2,
            label=f"{method} (fitted slope {slope:.2f})",
        )
    ref = disc["Random"][0] * (ns / ns[0]) ** -0.5
    ax_d.loglog(ns, ref, "k:", linewidth=1, label="$N^{-1/2}$ reference")
    ref1 = disc["Scrambled Sobol"][0] * (ns / ns[0]) ** -1.0
    ax_d.loglog(ns, ref1, "k--", linewidth=1, label="$N^{-1}$ reference")
    ax_d.set_xlabel("Number of samples $N$", fontsize=11)
    ax_d.set_ylabel("Centred $L_2$ discrepancy", fontsize=11)
    ax_d.set_title(
        f"Discrepancy in 2D, mean over {N_SEEDS} seeds (lower is more uniform)",
        fontsize=12,
    )
    ax_d.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax_d.legend(fontsize=10, loc="lower left")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    designs = {method: sample(method, N_SCATTER) for method in METHODS}
    ns, disc = discrepancy_study()
    for method in METHODS:
        pts = designs[method]
        print(
            f"{method:16s} N={N_SCATTER}: CD_2 = {centred_l2_discrepancy(pts):.4f}, "
            f"min distance = {min_pairwise_distance(pts):.3f}, "
            f"discrepancy slope = {fitted_slope(ns, disc[method]):.2f}"
        )
    print("N:", " ".join(f"{n:8d}" for n in ns))
    for method in METHODS:
        print(f"{method[:6]:6s}", " ".join(f"{v:8.5f}" for v in disc[method]))

    fig = make_figure(designs, ns, disc)
    finish_figures(
        {"sampling_strategies_comparison.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
