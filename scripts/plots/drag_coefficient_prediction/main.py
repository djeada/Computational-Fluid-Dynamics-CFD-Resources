"""Judge two synthetic drag-coefficient surrogates against CFD with a parity plot.

Sixty reference drag coefficients stand for held-out CFD results. Surrogate A
adds unbiased Gaussian noise of 3 drag counts; surrogate B has the same noise
but also a scale error (slope 0.96 about the mean) and an offset of +4 counts.
The left panel is the parity plot with a +/-5 count band, the right panel the
error in drag counts against the reference value. MAE, RMSE and R^2 are
reported for each surrogate, so the figure shows why R^2 alone can hide bias.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_SAMPLES = 60
CD_LOW, CD_HIGH = 0.26, 0.34  # reference Cd range of the held-out designs
COUNT = 1e-4  # one drag count
NOISE_COUNTS = 3.0  # standard deviation of the random error of both surrogates
SLOPE_B = 0.96  # scale error of surrogate B about the mean Cd
OFFSET_B_COUNTS = 4.0  # bias of surrogate B
BAND_COUNTS = 5.0  # tolerance band drawn around y = x


def generate_data(n=N_SAMPLES, seed=SEED):
    """Return reference Cd and the predictions of surrogates A and B."""
    rng = np.random.default_rng(seed)
    cd = rng.uniform(CD_LOW, CD_HIGH, n)
    pred_a = cd + NOISE_COUNTS * COUNT * rng.standard_normal(n)
    mean = cd.mean()
    pred_b = (
        mean
        + SLOPE_B * (cd - mean)
        + OFFSET_B_COUNTS * COUNT
        + NOISE_COUNTS * COUNT * rng.standard_normal(n)
    )
    return cd, pred_a, pred_b


def metrics(reference, predicted):
    """Return MAE and RMSE in drag counts, mean error in counts, and R^2."""
    error = (predicted - reference) / COUNT
    ss_res = np.sum((predicted - reference) ** 2)
    ss_tot = np.sum((reference - reference.mean()) ** 2)
    return {
        "mae": np.mean(np.abs(error)),
        "rmse": np.sqrt(np.mean(error**2)),
        "bias": np.mean(error),
        "r2": 1.0 - ss_res / ss_tot,
    }


def make_figure(cd, pred_a, pred_b):
    """Draw the parity plot and the error-versus-reference plot."""
    fig, (parity, residual) = plt.subplots(1, 2, figsize=(12.5, 5.6))
    lo, hi = CD_LOW - 0.005, CD_HIGH + 0.005
    line = np.array([lo, hi])
    band = BAND_COUNTS * COUNT

    parity.fill_between(
        line,
        line - band,
        line + band,
        color="0.85",
        label=rf"$\pm${BAND_COUNTS:.0f} drag counts",
    )
    parity.plot(line, line, color="0.3", linewidth=1, label="$y = x$")
    residual.axhspan(-BAND_COUNTS, BAND_COUNTS, color="0.85")
    residual.axhline(0.0, color="0.3", linewidth=1)

    series = [
        (pred_a, "tab:blue", "o", "A: unbiased"),
        (pred_b, "tab:orange", "s", "B: biased, slope 0.96"),
    ]
    for pred, color, marker, name in series:
        m = metrics(cd, pred)
        label = (
            f"{name}\nMAE {m['mae']:.1f}, RMSE {m['rmse']:.1f} counts, "
            f"$R^2$ = {m['r2']:.4f}"
        )
        parity.scatter(
            cd, pred, s=28, color=color, marker=marker, alpha=0.85, label=label
        )
        residual.scatter(
            cd, (pred - cd) / COUNT, s=28, color=color, marker=marker, alpha=0.85
        )
        trend = np.polyfit(cd, (pred - cd) / COUNT, 1)
        residual.plot(line, np.polyval(trend, line), color=color, linewidth=1.5)

    parity.set(
        xlim=(lo, hi),
        ylim=(lo, hi),
        xlabel="$C_d$ from CFD",
        ylabel="$C_d$ predicted by surrogate",
        title="Parity plot on 60 held-out designs",
        aspect="equal",
    )
    parity.legend(loc="upper left", fontsize=9)
    residual.set(
        xlim=(lo, hi),
        xlabel="$C_d$ from CFD",
        ylabel=r"error $\hat{C}_d - C_d$ (drag counts)",
        title="Error against reference, with linear trend",
    )
    for ax in (parity, residual):
        ax.grid(True, linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    cd, pred_a, pred_b = generate_data()
    for name, pred in (("A", pred_a), ("B", pred_b)):
        m = metrics(cd, pred)
        print(
            f"surrogate {name}: MAE {m['mae']:.2f}, RMSE {m['rmse']:.2f}, "
            f"bias {m['bias']:+.2f} counts, R^2 {m['r2']:.4f}"
        )

    finish_figures(
        {"drag_coefficient_prediction.png": make_figure(cd, pred_a, pred_b)},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
