"""Compare two synthetic drag-coefficient predictors against reference values.

Fifty reference drag coefficients are drawn uniformly in [0.15, 0.35] and two
predicted data sets are formed by adding independent uniform errors of up to
+/-0.025. Each predictor is plotted against the reference values together with
its least-squares regression line and the line of perfect prediction, and the
legend reports the slope, intercept, and coefficient of determination.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_SAMPLES = 50
CD_MIN, CD_RANGE = 0.15, 0.2  # reference Cd drawn uniformly in [0.15, 0.35]
ERROR_HALF_WIDTH = 0.025  # predictions = Cd + U(-0.025, 0.025)


def generate_data(n=N_SAMPLES, seed=SEED):
    """Return reference Cd and two noisy predictions of it."""
    rng = np.random.default_rng(seed)
    cd = CD_MIN + CD_RANGE * rng.random(n)
    pred_red = cd + ERROR_HALF_WIDTH * (2.0 * rng.random(n) - 1.0)
    pred_blue = cd + ERROR_HALF_WIDTH * (2.0 * rng.random(n) - 1.0)
    return cd, pred_red, pred_blue


def r_squared(reference, predicted):
    """Coefficient of determination of the predictions about y = x."""
    ss_res = np.sum((predicted - reference) ** 2)
    ss_tot = np.sum((reference - reference.mean()) ** 2)
    return 1.0 - ss_res / ss_tot


def make_figure(cd, pred_red, pred_blue):
    """Scatter both predictors with their regression lines and the identity line."""
    fig, ax = plt.subplots(figsize=(8, 6))
    lo = min(cd.min(), pred_red.min(), pred_blue.min()) - 0.01
    hi = max(cd.max(), pred_red.max(), pred_blue.max()) + 0.01
    x_line = np.array([lo, hi])

    ax.plot(x_line, x_line, color="gray", linewidth=1, label="Perfect prediction y=x")

    series = [
        (pred_red, "red", "+", 100, "--", "Predictor A"),
        (pred_blue, "blue", "o", 60, "-.", "Predictor B"),
    ]
    for pred, color, marker, size, style, name in series:
        fit = linregress(cd, pred)
        r2 = r_squared(cd, pred)
        ax.scatter(cd, pred, color=color, marker=marker, s=size, label=name)
        ax.plot(
            x_line,
            fit.slope * x_line + fit.intercept,
            color=color,
            linestyle=style,
            label=(
                f"{name} fit: y={fit.slope:.2f}x{fit.intercept:+.3f}, $R^2$={r2:.3f}"
            ),
        )

    ax.set_title("Predicted vs. Reference Drag Coefficient", fontsize=14)
    ax.set_xlabel("$C_d$ (reference)", fontsize=12)
    ax.set_ylabel("$C_{d,pred}$", fontsize=12)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = make_figure(*generate_data())

    finish_figures(
        {"drag_coefficient_prediction.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
