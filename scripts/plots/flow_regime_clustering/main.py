"""Cluster a regime-switching synthetic wake with POD and k-means.

A sequence of 2D vorticity-like snapshots switches between three wake
regimes: an antisymmetric shedding street, a symmetric (varicose) street and a
nearly steady wake with long shear layers, each with its own mean flow and
travelling-wave fluctuation. The snapshots are projected onto their leading
POD modes, k-means (Lloyd iteration with k-means++ seeding) groups the POD
coefficients into three clusters, and the figure shows the clusters in the
(a1, a2) plane, the cluster sequence over time, and each centroid as a field.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

SEED = 1
NX, NY = 96, 48  # grid points in x (streamwise) and y (cross-stream)
LX, Y_HALF = 12.0, 3.0  # domain [0, LX] x [-Y_HALF, Y_HALF] in body diameters D
DT = 0.1  # snapshot spacing (D / U)
N_POD = 10  # POD coefficients used for clustering
N_CLUSTERS = 3
N_RESTARTS = 10  # k-means restarts; the lowest objective is kept
BLEND_STEPS = 8  # snapshots over which one regime morphs into the next
NOISE_STD = 0.05  # additive noise (field units)
# Regime sequence as (regime index, number of snapshots).
SCHEDULE = [(0, 120), (1, 90), (2, 100), (0, 80), (2, 70), (1, 110), (0, 90)]
REGIME_NAMES = ("antisymmetric street", "symmetric street", "steady wake")

# Per regime: shear-layer offset (D), shear-layer strength, wave amplitude,
# wavenumber (1/D), phase speed (U), antisymmetric (True) or symmetric pattern.
REGIMES = [
    dict(offset=0.9, strength=1.0, wave=0.6, k=1.3, c=0.8, antisym=True),
    dict(offset=0.5, strength=0.6, wave=0.6, k=2.2, c=0.9, antisym=False),
    dict(offset=1.4, strength=1.4, wave=0.12, k=1.0, c=0.7, antisym=True),
]


def grid():
    x = np.linspace(0.0, LX, NX)
    y = np.linspace(-Y_HALF, Y_HALF, NY)
    return np.meshgrid(x, y, indexing="ij")


def regime_field(X, Y, t, offset, strength, wave, k, c, antisym):
    """Shear layers at y = +/- offset plus a travelling wave growing downstream."""
    width = 0.35  # shear-layer thickness (D)
    upper = np.exp(-(((Y - offset) / width) ** 2))
    lower = np.exp(-(((Y + offset) / width) ** 2))
    growth = 1.0 - np.exp(-X / 2.0)
    mean = strength * (lower - upper) * np.exp(-X / 15.0)
    carrier = np.cos(k * (X - c * t))
    sign = 1.0 if antisym else -1.0
    fluctuation = wave * growth * carrier * (upper + sign * lower)
    return mean + fluctuation


def make_snapshots(seed=SEED):
    """Return the snapshot matrix (space x time), true regime labels and times.

    Labels are -1 during the BLEND_STEPS snapshots of each transition.
    """
    X, Y = grid()
    rng = np.random.default_rng(seed)
    labels = np.concatenate([np.full(n, r) for r, n in SCHEDULE])
    t = DT * np.arange(labels.size)
    snapshots = np.empty((X.size, labels.size))
    true_labels = labels.copy()
    start = 0
    for i, (regime, n) in enumerate(SCHEDULE):
        previous = SCHEDULE[i - 1][0] if i > 0 else regime
        for j in range(n):
            step = start + j
            field = regime_field(X, Y, t[step], **REGIMES[regime])
            if i > 0 and j < BLEND_STEPS:
                weight = (j + 1) / (BLEND_STEPS + 1)
                old = regime_field(X, Y, t[step], **REGIMES[previous])
                field = weight * field + (1.0 - weight) * old
                true_labels[step] = -1
            snapshots[:, step] = field.ravel()
        start += n
    snapshots += NOISE_STD * rng.standard_normal(snapshots.shape)
    return snapshots, true_labels, t


def kmeans_plus_plus(points, k, rng):
    """k-means++ seeding: spread the initial centroids out."""
    centroids = [points[rng.integers(len(points))]]
    for _ in range(1, k):
        d2 = np.min(
            ((points[:, None, :] - np.array(centroids)[None]) ** 2).sum(-1), axis=1
        )
        centroids.append(points[rng.choice(len(points), p=d2 / d2.sum())])
    return np.array(centroids)


def kmeans(points, k, rng, max_iter=100):
    """Lloyd's algorithm. Returns labels, centroids and the objective history.

    The objective J = sum_i ||a_i - c_{label_i}||^2 cannot increase from one
    iteration to the next: the assignment step and the update step each
    minimise J over one set of variables with the other held fixed.
    """
    centroids = kmeans_plus_plus(points, k, rng)
    history = []
    labels = None
    for _ in range(max_iter):
        distances = ((points[:, None, :] - centroids[None]) ** 2).sum(-1)
        new_labels = distances.argmin(axis=1)
        history.append(distances[np.arange(len(points)), new_labels].sum())
        if labels is not None and np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for j in range(k):
            members = points[labels == j]
            if len(members):
                centroids[j] = members.mean(axis=0)
    return labels, centroids, np.array(history)


def best_kmeans(points, k, seed=SEED, restarts=N_RESTARTS):
    """Run k-means from several seeds and keep the lowest final objective."""
    rng = np.random.default_rng(seed)
    runs = [kmeans(points, k, rng) for _ in range(restarts)]
    return min(runs, key=lambda run: run[2][-1])


def relabel_by_majority(labels, true_labels, k):
    """Map each cluster to the true regime most of its members belong to."""
    mapping = np.zeros(k, dtype=int)
    for j in range(k):
        members = true_labels[(labels == j) & (true_labels >= 0)]
        mapping[j] = np.bincount(members, minlength=k).argmax()
    return mapping[labels], mapping


def transition_matrix(labels, k):
    """Row-stochastic matrix of one-step cluster transitions (CROM, Kaiser 2014)."""
    counts = np.zeros((k, k))
    np.add.at(counts, (labels[:-1], labels[1:]), 1.0)
    return counts / counts.sum(axis=1, keepdims=True)


def make_figure(coeffs, labels, centroid_fields, example_fields, t, true_labels):
    colours = plt.get_cmap("tab10").colors
    X, Y = grid()
    fig = plt.figure(figsize=(13, 9.5), layout="constrained")
    gs = fig.add_gridspec(3, 3, height_ratios=[1.5, 1, 1])

    ax = fig.add_subplot(gs[0, 0])
    for j in range(N_CLUSTERS):
        member = labels == j
        ax.scatter(
            coeffs[member, 0],
            coeffs[member, 1],
            s=10,
            color=colours[j],
            label=f"cluster {j + 1}: {REGIME_NAMES[j]}",
        )
    centroids = np.array([coeffs[labels == j, :2].mean(0) for j in range(N_CLUSTERS)])
    ax.scatter(*centroids.T, marker="X", s=160, c="k", edgecolors="w", label="centroid")
    ax.set_xlabel("POD coefficient $a_1$")
    ax.set_ylabel("POD coefficient $a_2$")
    ax.set_title("(a) Snapshots in the $(a_1, a_2)$ plane")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(gs[0, 1:])
    for j in range(N_CLUSTERS):
        member = labels == j
        ax.scatter(t[member], np.full(member.sum(), j), s=6, color=colours[j])
    blend = true_labels < 0
    ax.scatter(t[blend], labels[blend], s=14, c="k", marker="|")
    ax.scatter([], [], s=40, c="k", marker="|", label="blended (transition) snapshot")
    ax.set_yticks(range(N_CLUSTERS), REGIME_NAMES)
    ax.set_ylim(-0.6, N_CLUSTERS - 0.4)
    ax.set_xlabel("$t$ ($D/U$)")
    ax.set_title("(b) Cluster sequence over time")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, axis="x", alpha=0.3)

    limit = np.abs(example_fields).max()
    rows = [(example_fields, "snapshot"), (centroid_fields, "centroid")]
    for row, (fields, kind) in enumerate(rows, start=1):
        row_axes = []
        for j in range(N_CLUSTERS):
            ax = fig.add_subplot(gs[row, j])
            mesh = ax.pcolormesh(
                X,
                Y,
                fields[j].reshape(X.shape),
                cmap="RdBu_r",
                vmin=-limit,
                vmax=limit,
                shading="auto",
            )
            ax.set_aspect("equal")
            row_axes.append(ax)
            ax.set_title(f"({'cdefgh'[3 * (row - 1) + j]}) {kind}, cluster {j + 1}")
            ax.set_xlabel("$x/D$")
            if j == 0:
                ax.set_ylabel("$y/D$")
        fig.colorbar(mesh, ax=row_axes, shrink=0.9, label=r"vorticity $\omega$")

    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    snapshots, true_labels, t = make_snapshots()
    pod = compute_pod(snapshots)
    coeffs = pod.coefficients[:N_POD].T
    raw_labels, _, history = best_kmeans(coeffs, N_CLUSTERS)
    labels, mapping = relabel_by_majority(raw_labels, true_labels, N_CLUSTERS)

    centroid_fields = []
    example_fields = []
    for j in range(N_CLUSTERS):
        centroid = coeffs[labels == j].mean(axis=0)
        centroid_fields.append(pod.mean[:, 0] + pod.modes[:, :N_POD] @ centroid)
        first = np.nonzero((labels == j) & (true_labels == j))[0][20]
        example_fields.append(snapshots[:, first])

    clean = true_labels >= 0
    accuracy = np.mean(labels[clean] == true_labels[clean])
    energy = pod.energy_fractions[:N_POD].sum()
    print(f"energy captured by {N_POD} POD modes: {100 * energy:.1f}%")
    print(f"k-means iterations: {history.size}, final objective J = {history[-1]:.1f}")
    print(f"agreement with true regime (transitions excluded): {100 * accuracy:.1f}%")
    print("cluster transition matrix P_jk (rows: from, columns: to):")
    print(np.array2string(transition_matrix(labels, N_CLUSTERS), precision=3))

    fig = make_figure(
        coeffs,
        labels,
        np.array(centroid_fields),
        np.array(example_fields),
        t,
        true_labels,
    )
    finish_figures(
        {"flow_regime_clustering.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
