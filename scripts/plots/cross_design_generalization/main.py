"""Synthetic illustration of in-distribution and cross-design surrogate errors.

Two "design families" X and Y occupy different, partly overlapping boxes of a
normalised 2D parameter space. A known ground-truth function plays the role of
the CFD drag coefficient, with small Gaussian label noise standing in for the
dataset error. Three ridge-regression surrogates on Gaussian radial basis
function features are trained on X only (Model 1), Y only (Model 2) and X + Y
(Model 3), with the ridge penalty and RBF width chosen by 5-fold cross
validation on each training set. Each model is evaluated on held-out designs of
both families. Nothing here is real vehicle data.
"""

import sys
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 1
NOISE_STD = 0.002  # std of the label noise on C_d (2 drag counts)
FAMILIES = {
    # name: ((p1_min, p1_max), (p2_min, p2_max)), n_train, n_test
    "X": (((0.0, 0.6), (0.0, 0.65)), 60, 15),
    "Y": (((0.4, 1.0), (0.35, 1.0)), 30, 10),
}
RBF_GRID = 7  # RBF centres on a RBF_GRID x RBF_GRID lattice over the unit square
LAMBDAS = (1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1)  # ridge penalties searched
WIDTHS = (0.15, 0.25, 0.4)  # RBF widths searched (normalised units)
N_FOLDS = 5
DRAG_COUNT = 1e-3  # one drag count is Delta C_d = 0.001
MODELS = {
    "Model 1 (train X)": ("X",),
    "Model 2 (train Y)": ("Y",),
    "Model 3 (train X+Y)": ("X", "Y"),
}
MODEL_COLORS = ("tab:blue", "tab:orange", "tab:green")


def true_cd(p):
    """Ground-truth drag coefficient on the normalised parameters p = (p1, p2)."""
    p1, p2 = p[:, 0], p[:, 1]
    return (
        0.29
        + 0.04 * (p1 - 0.3) ** 2
        + 0.05 * p1 * p2
        + 0.012 * np.sin(3.0 * np.pi * p2)
        - 0.02 * np.exp(-((p1 - 0.85) ** 2 + (p2 - 0.8) ** 2) / 0.02)
    )


def sample_family(box, n, rng):
    """Latin hypercube sample of n points in an axis-aligned box."""
    (a1, b1), (a2, b2) = box
    u = np.empty((n, 2))
    for k in range(2):
        u[:, k] = (rng.permutation(n) + rng.random(n)) / n
    return np.column_stack((a1 + (b1 - a1) * u[:, 0], a2 + (b2 - a2) * u[:, 1]))


def make_datasets(seed=SEED, noise=NOISE_STD):
    """Train and test inputs and noisy labels for each family."""
    rng = np.random.default_rng(seed)
    data = {}
    for name, (box, n_train, n_test) in FAMILIES.items():
        p_tr = sample_family(box, n_train, rng)
        p_te = sample_family(box, n_test, rng)
        data[name] = {
            "train": (p_tr, true_cd(p_tr) + noise * rng.normal(size=n_train)),
            "test": (p_te, true_cd(p_te) + noise * rng.normal(size=n_test)),
        }
    return data


def rbf_features(p, width, n_grid=RBF_GRID):
    """Gaussian RBFs on a lattice of centres plus the two linear terms."""
    c = np.linspace(0.0, 1.0, n_grid)
    centres = np.array(list(product(c, c)))
    d2 = ((p[:, None, :] - centres[None, :, :]) ** 2).sum(axis=-1)
    return np.hstack((p, np.exp(-d2 / (2.0 * width**2))))


class RidgeRBF:
    """Ridge regression on RBF features with an unpenalised intercept."""

    def __init__(self, lam, width):
        self.lam, self.width = lam, width

    def fit(self, p, y):
        phi = rbf_features(p, self.width)
        self.phi_mean, self.y_mean = phi.mean(axis=0), y.mean()
        a = phi - self.phi_mean
        lhs = a.T @ a + self.lam * len(y) * np.eye(a.shape[1])
        self.w = np.linalg.solve(lhs, a.T @ (y - self.y_mean))
        return self

    def predict(self, p):
        return self.y_mean + (rbf_features(p, self.width) - self.phi_mean) @ self.w


def rmse(y, y_hat):
    return float(np.sqrt(np.mean((y - y_hat) ** 2)))


def cross_validate(p, y, n_folds=N_FOLDS, seed=SEED):
    """Grid search over (lambda, width) by k-fold CV; return the best model fitted on all data."""
    folds = np.array_split(np.random.default_rng(seed).permutation(len(y)), n_folds)
    best = None
    for lam, width in product(LAMBDAS, WIDTHS):
        errs = []
        for k in range(n_folds):
            val = folds[k]
            tr = np.concatenate([folds[j] for j in range(n_folds) if j != k])
            model = RidgeRBF(lam, width).fit(p[tr], y[tr])
            errs.append(np.mean((model.predict(p[val]) - y[val]) ** 2))
        score = np.sqrt(np.mean(errs))
        if best is None or score < best[0]:
            best = (score, lam, width)
    return RidgeRBF(best[1], best[2]).fit(p, y), best


def train_models(data):
    """Fit Models 1-3 and return them with their RMSE on each test family."""
    models, table = {}, {}
    for name, fams in MODELS.items():
        p = np.vstack([data[f]["train"][0] for f in fams])
        y = np.concatenate([data[f]["train"][1] for f in fams])
        model, cv = cross_validate(p, y)
        models[name] = (model, cv)
        table[name] = {
            f: rmse(data[f]["test"][1], model.predict(data[f]["test"][0]))
            for f in FAMILIES
        }
    return models, table


def make_figure(data, models, table):
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 11))

    ax = axes[0, 0]
    g = np.linspace(0, 1, 151)
    G1, G2 = np.meshgrid(g, g)
    Z = true_cd(np.column_stack((G1.ravel(), G2.ravel()))).reshape(G1.shape)
    cf = ax.contourf(G1, G2, Z, levels=20, cmap="cividis")
    fig.colorbar(cf, ax=ax, label="Ground-truth $C_d$")
    styles = {"X": ("o", "white"), "Y": ("^", "tab:red")}
    for f, (marker, color) in styles.items():
        (a1, b1), (a2, b2) = FAMILIES[f][0]
        ax.add_patch(
            plt.Rectangle(
                (a1, a2),
                b1 - a1,
                b2 - a2,
                fill=False,
                edgecolor=color,
                linewidth=2,
                linestyle="--",
            )
        )
        p_tr, p_te = data[f]["train"][0], data[f]["test"][0]
        ax.scatter(
            p_tr[:, 0],
            p_tr[:, 1],
            marker=marker,
            s=36,
            color=color,
            edgecolor="k",
            linewidth=0.5,
            label=f"family {f}, train ({len(p_tr)})",
        )
        ax.scatter(
            p_te[:, 0],
            p_te[:, 1],
            marker=marker,
            s=70,
            facecolor="none",
            edgecolor=color,
            linewidth=1.8,
            label=f"family {f}, test ({len(p_te)})",
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("$p_1$ (normalised)", fontsize=11)
    ax.set_ylabel("$p_2$ (normalised)", fontsize=11)
    ax.set_title("(a) Two design families in parameter space", fontsize=12)
    ax.legend(fontsize=8.5, loc="upper left", framealpha=0.9)

    markers = ("o", "s", "D")
    for ax, f, label in ((axes[0, 1], "X", "(b)"), (axes[1, 0], "Y", "(c)")):
        p_te, y_te = data[f]["test"]
        lo, hi = y_te.min() - 0.01, y_te.max() + 0.01
        for (name, (model, _)), color, m in zip(models.items(), MODEL_COLORS, markers):
            y_hat = model.predict(p_te)
            lo, hi = min(lo, y_hat.min() - 0.005), max(hi, y_hat.max() + 0.005)
            ax.scatter(
                y_te,
                y_hat,
                marker=m,
                s=45,
                color=color,
                edgecolor="k",
                linewidth=0.4,
                label=f"{name}: RMSE {table[name][f] / DRAG_COUNT:.1f} counts",
            )
        ax.plot([lo, hi], [lo, hi], color="0.4", linewidth=1)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_aspect("equal")
        ax.set_xlabel("Reference $C_d$ (test set)", fontsize=11)
        ax.set_ylabel("Predicted $C_d$", fontsize=11)
        ax.set_title(f"{label} Parity plot on family {f} test designs", fontsize=12)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        ax.legend(fontsize=9, loc="lower right")

    ax = axes[1, 1]
    x = np.arange(len(FAMILIES))
    width = 0.26
    for k, (name, color) in enumerate(zip(MODELS, MODEL_COLORS)):
        vals = [table[name][f] / DRAG_COUNT for f in FAMILIES]
        bars = ax.bar(x + (k - 1) * width, vals, width * 0.92, color=color, label=name)
        ax.bar_label(bars, fmt="%.1f", fontsize=9, padding=2)
    ax.axhline(
        NOISE_STD / DRAG_COUNT,
        color="k",
        linestyle=":",
        linewidth=1.2,
        label="label noise (std)",
    )
    ax.set_yscale("log")
    ax.set_xticks(x, [f"test on family {f}" for f in FAMILIES], fontsize=11)
    ax.set_ylabel("Test RMSE (drag counts, log scale)", fontsize=11)
    ax.set_title("(d) In-distribution vs cross-design error", fontsize=12)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, axis="y", which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.set_ylim(0.5, ax.get_ylim()[1] * 3)

    fig.suptitle(
        "Synthetic illustration (analytic ground truth, not CFD data)", fontsize=13
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    data = make_datasets()
    models, table = train_models(data)
    print("Test RMSE in drag counts (1 count = 0.001):")
    for name, (_, (cv, lam, width)) in models.items():
        row = "  ".join(
            f"test {f}: {table[name][f] / DRAG_COUNT:6.2f}" for f in FAMILIES
        )
        print(
            f"  {name:20s} {row}   (CV RMSE {cv / DRAG_COUNT:.2f}, lambda {lam:g}, width {width:g})"
        )

    fig = make_figure(data, models, table)
    finish_figures(
        {"cross_design_generalization.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
