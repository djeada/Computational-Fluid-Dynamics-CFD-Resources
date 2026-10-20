"""Illustrate regression, classification and clustering on synthetic flow data.

Three panels, each computed in numpy:
1. supervised regression: a Gaussian-process fit to noisy drag coefficients
   versus rear slant angle, with its 95 % predictive band;
2. supervised classification: logistic regression separating laminar from
   turbulent boundary-layer samples in the (log10 Re_x, Tu) plane;
3. unsupervised clustering: k-means on unlabelled wake features
   (mean drag, RMS lift) that come from three flow regimes.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 3

# Regression: drag coefficient versus rear slant angle.
N_REGRESSION = 25  # number of noisy CFD-like samples
SLANT_MIN, SLANT_MAX = 0.0, 40.0  # rear slant angle range, degrees
CD_NOISE_STD = 0.008  # standard deviation of the Cd scatter
GP_LENGTH = 6.0  # Gaussian-process correlation length, degrees
GP_SIGNAL_STD = 0.03  # Gaussian-process prior standard deviation of Cd
Z_95 = 1.96  # two-sided 95 % normal quantile

# Classification: laminar or turbulent boundary layer.
N_CLASSIFICATION = 200  # labelled samples
LOG_RE_MIN, LOG_RE_MAX = 5.0, 6.5  # log10 of the local Reynolds number Re_x
TU_MIN, TU_MAX = 0.0, 3.0  # free-stream turbulence intensity, percent
LOG_RE_CRIT_0 = 6.2  # transition log10 Re_x at Tu = 0 (synthetic rule)
LOG_RE_CRIT_SLOPE = -0.35  # change of transition log10 Re_x per percent Tu
LABEL_SHARPNESS = 8.0  # sharpness of the label probability around the rule
LOGISTIC_ITERATIONS = 25  # Newton (IRLS) iterations

# Clustering: three wake regimes.
REGIME_CENTRES = np.array([[1.05, 0.02], [1.35, 0.30], [1.20, 0.12]])  # (Cd, CL')
REGIME_SPREADS = np.array([[0.04, 0.012], [0.06, 0.04], [0.05, 0.025]])
N_PER_REGIME = 60  # samples per regime
N_CLUSTERS = 3  # k in k-means
KMEANS_ITERATIONS = 50  # maximum Lloyd iterations


def drag_coefficient(slant_deg):
    """Smooth synthetic Cd(phi): a drag rise towards 30 degrees, then a drop."""
    phi = np.asarray(slant_deg, dtype=float)
    return 0.25 + 0.06 * np.exp(-(((phi - 30.0) / 7.0) ** 2)) + 0.0008 * phi


def rbf_kernel(a, b, length=GP_LENGTH, signal_std=GP_SIGNAL_STD):
    """Squared-exponential covariance k(a, b) = s^2 exp(-(a - b)^2 / (2 l^2))."""
    return signal_std**2 * np.exp(-0.5 * ((a[:, None] - b[None, :]) / length) ** 2)


def gp_regression(x, y, x_new, noise_std=CD_NOISE_STD):
    """Gaussian-process posterior mean and 95 % predictive half-width.

    A constant prior mean equal to the sample mean is removed first. The
    predictive variance includes the observation noise.
    """
    y_mean = y.mean()
    gram = rbf_kernel(x, x) + noise_std**2 * np.eye(len(x))
    cross = rbf_kernel(x_new, x)
    chol = np.linalg.cholesky(gram)
    alpha = np.linalg.solve(chol.T, np.linalg.solve(chol, y - y_mean))
    v = np.linalg.solve(chol, cross.T)
    mean = y_mean + cross @ alpha
    var = GP_SIGNAL_STD**2 - np.sum(v**2, axis=0) + noise_std**2
    return mean, Z_95 * np.sqrt(var)


def make_classification_data(rng):
    """Samples in (log10 Re_x, Tu) labelled 1 (turbulent) or 0 (laminar)."""
    log_re = rng.uniform(LOG_RE_MIN, LOG_RE_MAX, N_CLASSIFICATION)
    tu = rng.uniform(TU_MIN, TU_MAX, N_CLASSIFICATION)
    margin = log_re - (LOG_RE_CRIT_0 + LOG_RE_CRIT_SLOPE * tu)
    probability = 1.0 / (1.0 + np.exp(-LABEL_SHARPNESS * margin))
    labels = (rng.random(N_CLASSIFICATION) < probability).astype(float)
    return np.column_stack([log_re, tu]), labels


def fit_logistic_regression(features, labels, iterations=LOGISTIC_ITERATIONS):
    """Logistic regression by Newton's method (iteratively reweighted least squares).

    Minimises the cross-entropy -sum[y log s + (1 - y) log(1 - s)] with
    s = sigmoid(w^T x + b). A tiny ridge term keeps the Hessian invertible.
    Returns (w, b) in the original, unscaled feature units.
    """
    mean, std = features.mean(axis=0), features.std(axis=0)
    x = np.column_stack([(features - mean) / std, np.ones(len(features))])
    theta = np.zeros(x.shape[1])
    for _ in range(iterations):
        s = 1.0 / (1.0 + np.exp(-x @ theta))
        gradient = x.T @ (s - labels) + 1e-6 * theta
        hessian = (x * (s * (1.0 - s))[:, None]).T @ x + 1e-6 * np.eye(x.shape[1])
        theta -= np.linalg.solve(hessian, gradient)
    weights = theta[:-1] / std
    bias = theta[-1] - weights @ mean
    return weights, bias


def make_clustering_data(rng):
    """Unlabelled wake features drawn from three Gaussian regimes."""
    blobs = [
        centre + spread * rng.standard_normal((N_PER_REGIME, 2))
        for centre, spread in zip(REGIME_CENTRES, REGIME_SPREADS)
    ]
    return np.vstack(blobs)


def kmeans(points, k, rng, iterations=KMEANS_ITERATIONS):
    """Lloyd's k-means with k-means++ initialisation on standardised features.

    Returns labels, centroids (in the original units) and the within-cluster
    sum of squares in standardised units.
    """
    mean, std = points.mean(axis=0), points.std(axis=0)
    z = (points - mean) / std
    centroids = [z[rng.integers(len(z))]]
    for _ in range(1, k):
        d2 = np.min([np.sum((z - c) ** 2, axis=1) for c in centroids], axis=0)
        centroids.append(z[rng.choice(len(z), p=d2 / d2.sum())])
    centroids = np.array(centroids)
    labels = np.zeros(len(z), dtype=int)
    for iteration in range(iterations):
        distances = np.sum((z[:, None, :] - centroids[None]) ** 2, axis=2)
        new_labels = distances.argmin(axis=1)
        if iteration > 0 and np.array_equal(new_labels, labels):
            break
        labels = new_labels
        centroids = np.array([z[labels == j].mean(axis=0) for j in range(k)])
    inertia = float(np.sum((z - centroids[labels]) ** 2))
    return labels, centroids * std + mean, inertia


def plot_regression(ax, rng):
    slant = np.sort(rng.uniform(SLANT_MIN, SLANT_MAX, N_REGRESSION))
    cd = drag_coefficient(slant) + CD_NOISE_STD * rng.standard_normal(N_REGRESSION)
    fine = np.linspace(SLANT_MIN, SLANT_MAX, 300)
    mean, half_width = gp_regression(slant, cd, fine)
    ax.fill_between(
        fine,
        mean - half_width,
        mean + half_width,
        color="tab:blue",
        alpha=0.2,
        label="95 % predictive band",
    )
    ax.plot(fine, drag_coefficient(fine), "k--", lw=1.2, label="true trend")
    ax.plot(fine, mean, color="tab:blue", lw=2, label="GP mean")
    ax.plot(slant, cd, "o", color="tab:orange", ms=5, label="CFD samples")
    ax.set_xlabel(r"rear slant angle $\varphi$ [$^\circ$]", fontsize=11)
    ax.set_ylabel("drag coefficient $C_d$ [-]", fontsize=11)
    ax.set_title("Supervised regression: Gaussian process", fontsize=12)
    ax.legend(fontsize=9, loc="upper left")


def plot_classification(ax, rng):
    features, labels = make_classification_data(rng)
    weights, bias = fit_logistic_regression(features, labels)
    grid_re, grid_tu = np.meshgrid(
        np.linspace(LOG_RE_MIN, LOG_RE_MAX, 200), np.linspace(TU_MIN, TU_MAX, 200)
    )
    prob = 1.0 / (1.0 + np.exp(-(weights[0] * grid_re + weights[1] * grid_tu + bias)))
    ax.contourf(
        grid_re, grid_tu, prob, levels=np.linspace(0, 1, 11), cmap="RdBu_r", alpha=0.25
    )
    ax.contour(grid_re, grid_tu, prob, levels=[0.5], colors="k", linewidths=2)
    tu_line = np.array([TU_MIN, TU_MAX])
    ax.plot(
        LOG_RE_CRIT_0 + LOG_RE_CRIT_SLOPE * tu_line,
        tu_line,
        color="0.25",
        ls="--",
        lw=1.5,
        label="rule used to label data",
    )
    for value, marker, color, name in (
        (0.0, "o", "tab:blue", "laminar"),
        (1.0, "^", "tab:red", "turbulent"),
    ):
        mask = labels == value
        ax.scatter(
            features[mask, 0],
            features[mask, 1],
            marker=marker,
            s=22,
            color=color,
            edgecolor="k",
            linewidth=0.4,
            label=name,
        )
    ax.plot([], [], "k-", lw=2, label="learned $p = 0.5$ boundary")
    accuracy = np.mean(((features @ weights + bias) > 0) == (labels == 1))
    ax.set_xlabel(r"$\log_{10} Re_x$", fontsize=11)
    ax.set_ylabel("free-stream turbulence $Tu$ [%]", fontsize=11)
    ax.set_title(
        f"Supervised classification: logistic regression\n(training accuracy {accuracy:.0%})",
        fontsize=12,
    )
    ax.set_xlim(LOG_RE_MIN, LOG_RE_MAX)
    ax.legend(fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    return accuracy


def plot_clustering(ax, rng):
    points = make_clustering_data(rng)
    labels, centroids, _ = kmeans(points, N_CLUSTERS, rng)
    colors = ("tab:blue", "tab:orange", "tab:green")
    markers = ("o", "s", "D")
    for j in range(N_CLUSTERS):
        mask = labels == j
        ax.scatter(
            points[mask, 0],
            points[mask, 1],
            s=18,
            marker=markers[j],
            color=colors[j],
            alpha=0.8,
            label=f"cluster {j + 1}",
        )
    ax.scatter(
        centroids[:, 0],
        centroids[:, 1],
        marker="X",
        s=180,
        color="k",
        edgecolor="w",
        label="centroids",
    )
    ax.set_xlabel(r"mean drag $\overline{C_d}$ [-]", fontsize=11)
    ax.set_ylabel(r"RMS lift $C_L'$ [-]", fontsize=11)
    ax.set_title(f"Unsupervised clustering: k-means, k = {N_CLUSTERS}", fontsize=12)
    ax.legend(fontsize=9, loc="upper left")


def make_figure(seed=SEED):
    rng = np.random.default_rng(seed)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    plot_regression(axes[0], rng)
    plot_classification(axes[1], rng)
    plot_clustering(axes[2], rng)
    for ax in axes:
        ax.grid(True, lw=0.5, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    finish_figures(
        {"ml_learning_paradigms.png": make_figure()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
