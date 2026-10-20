"""Show the bias-variance trade-off with polynomial fits of increasing degree.

Twenty noisy samples of a smooth response y(x) at fixed, equally spaced
locations are fitted by least-squares Legendre polynomials of degree 0 to 15.
Panel 1 shows an underfit, a well-chosen and an overfit model; panel 2 the
training, validation and leave-one-out cross-validation error against degree;
panel 3 a Monte Carlo estimate of squared bias, variance and noise over many
independent noise realisations of the training set.
"""

import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import legendre

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 1
N_TRAIN = 20  # training samples per data set
N_VALIDATION = 500  # independent validation samples
NOISE_STD = 0.2  # standard deviation of the observation noise
MAX_DEGREE = 15  # highest polynomial degree tried
SHOWN_DEGREES = (1, 7, 15)  # degrees drawn in panel 1
N_FOLDS = N_TRAIN  # folds in k-fold cross-validation (N_TRAIN = leave-one-out)
N_DATASETS = 400  # training sets in the Monte Carlo bias-variance estimate
N_TEST = 200  # test locations for the bias-variance estimate


def true_function(x):
    """Smooth response on x in [0, 1]: one dominant wave plus a weaker one."""
    return np.sin(2.0 * np.pi * x) + 0.3 * np.cos(5.0 * np.pi * x)


def training_locations(n=None):
    """Fixed, equally spaced design points (cell centres of n bins on [0, 1])."""
    n = N_TRAIN if n is None else n
    return (np.arange(n) + 0.5) / n


def sample_data(x, rng, noise_std=NOISE_STD):
    """Noisy observations y = f(x) + eps, eps ~ N(0, noise_std^2)."""
    return true_function(x) + noise_std * rng.standard_normal(x.size)


def fit_polynomial(x, y, degree):
    """Least-squares Legendre coefficients in the variable 2x - 1.

    High degrees on few points are ill-conditioned on purpose (that is the
    overfitting regime), so numpy's RankWarning is silenced.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", np.exceptions.RankWarning)
        return legendre.legfit(2.0 * x - 1.0, y, degree)


def predict(coeffs, x):
    return legendre.legval(2.0 * x - 1.0, coeffs)


def rmse(prediction, target):
    return float(np.sqrt(np.mean((prediction - target) ** 2)))


def kfold_indices(n, k, rng):
    """Shuffle 0..n-1 and split into k nearly equal folds."""
    return np.array_split(rng.permutation(n), k)


def kfold_cv(x, y, degree, k, rng):
    """Pooled k-fold cross-validation RMSE.

    Every sample is predicted once by the model trained on the other k - 1
    folds; the RMSE of those held-out predictions is returned. k = len(x)
    gives leave-one-out cross-validation.
    """
    held_out = np.empty_like(y)
    for fold in kfold_indices(len(x), k, rng):
        train = np.setdiff1d(np.arange(len(x)), fold)
        held_out[fold] = predict(fit_polynomial(x[train], y[train], degree), x[fold])
    return rmse(held_out, y)


def bias_variance(degree, rng, n_datasets=N_DATASETS, x_test=None):
    """Monte Carlo bias^2 and variance of a degree-d fit, averaged over x_test.

    The design points are fixed; only the noise changes between training sets.
    Each of n_datasets training sets gives a prediction f_hat_j(x). With
    f_bar = mean_j f_hat_j, bias^2 = mean_x (f_bar - f)^2 and
    variance = mean_x mean_j (f_hat_j - f_bar)^2.
    """
    if x_test is None:
        x_test = np.linspace(training_locations()[0], training_locations()[-1], N_TEST)
    predictions = np.empty((n_datasets, x_test.size))
    x = training_locations()
    for j in range(n_datasets):
        y = sample_data(x, rng)
        predictions[j] = predict(fit_polynomial(x, y, degree), x_test)
    mean_prediction = predictions.mean(axis=0)
    bias2 = float(np.mean((mean_prediction - true_function(x_test)) ** 2))
    variance = float(np.mean(predictions.var(axis=0)))
    return bias2, variance, predictions


def compute_curves(seed=SEED):
    """All errors needed for panels 2 and 3."""
    rng = np.random.default_rng(seed)
    x = training_locations()
    y = sample_data(x, rng)
    x_val = rng.uniform(x[0], x[-1], N_VALIDATION)
    y_val = sample_data(x_val, rng)
    degrees = np.arange(MAX_DEGREE + 1)
    train_err, val_err, cv_err, bias2, variance = ([] for _ in range(5))
    for degree in degrees:
        coeffs = fit_polynomial(x, y, degree)
        train_err.append(rmse(predict(coeffs, x), y))
        val_err.append(rmse(predict(coeffs, x_val), y_val))
        cv_err.append(kfold_cv(x, y, degree, N_FOLDS, rng))
        b2, var, _ = bias_variance(degree, rng)
        bias2.append(b2)
        variance.append(var)
    return {
        "data": (x, y),
        "degrees": degrees,
        "train": np.array(train_err),
        "val": np.array(val_err),
        "cv": np.array(cv_err),
        "bias2": np.array(bias2),
        "variance": np.array(variance),
    }


def make_figure(curves):
    x, y = curves["data"]
    degrees = curves["degrees"]
    fine = np.linspace(0.0, 1.0, 400)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

    ax = axes[0]
    ax.plot(fine, true_function(fine), "k--", lw=1.5, label="true $f(x)$")
    ax.plot(x, y, "o", color="0.4", ms=5, label=f"{N_TRAIN} training samples")
    for degree, color, name in zip(
        SHOWN_DEGREES,
        ("tab:blue", "tab:green", "tab:red"),
        ("underfit", "good fit", "overfit"),
    ):
        coeffs = fit_polynomial(x, y, degree)
        ax.plot(
            fine,
            predict(coeffs, fine),
            color=color,
            lw=2,
            label=f"d = {degree} ({name})",
        )
    ax.legend(fontsize=9, loc="lower left")
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlabel("design parameter $x$ [-]", fontsize=11)
    ax.set_ylabel("response $y$ [-]", fontsize=11)
    ax.set_title("Polynomial fits of degree d", fontsize=12)

    ax = axes[1]
    best = int(degrees[np.argmin(curves["cv"])])
    cv_label = "leave-one-out CV" if N_FOLDS == N_TRAIN else f"{N_FOLDS}-fold CV"
    ax.semilogy(degrees, curves["train"], "o-", color="tab:blue", label="training")
    ax.semilogy(degrees, curves["val"], "s-", color="tab:red", label="validation")
    ax.semilogy(degrees, curves["cv"], "^--", color="tab:green", label=cv_label)
    ax.axhline(NOISE_STD, color="0.3", ls=":", label=r"noise level $\sigma$")
    ax.axvline(best, color="tab:green", lw=0.8, alpha=0.6)
    ax.set_ylim(0.03, 50.0)
    ax.set_xlabel("polynomial degree d (model complexity)", fontsize=11)
    ax.set_ylabel("RMSE [-]", fontsize=11)
    ax.set_title(f"Error vs complexity (CV picks d = {best})", fontsize=12)
    ax.legend(fontsize=9, loc="upper left")

    ax = axes[2]
    total = curves["bias2"] + curves["variance"] + NOISE_STD**2
    ax.semilogy(degrees, curves["bias2"], "o-", color="tab:blue", label="bias$^2$")
    ax.semilogy(degrees, curves["variance"], "s-", color="tab:orange", label="variance")
    ax.axhline(NOISE_STD**2, color="0.3", ls=":", label=r"noise $\sigma^2$")
    ax.semilogy(degrees, total, "k-", lw=2, label=r"sum = expected test MSE")
    ax.set_xlabel("polynomial degree d (model complexity)", fontsize=11)
    ax.set_ylabel("mean-squared error [-]", fontsize=11)
    ax.set_title(f"Bias-variance split ({N_DATASETS} noise draws)", fontsize=12)
    ax.legend(fontsize=9, loc="lower left")

    for ax in axes:
        ax.grid(True, which="both", lw=0.5, alpha=0.4)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    curves = compute_curves()
    for d in curves["degrees"]:
        print(
            f"d={d:2d}  train={curves['train'][d]:.3f}  val={curves['val'][d]:.3f}  "
            f"cv={curves['cv'][d]:.3f}  bias2={curves['bias2'][d]:.4f}  "
            f"var={curves['variance'][d]:.4f}"
        )

    finish_figures(
        {"bias_variance_tradeoff.png": make_figure(curves)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
