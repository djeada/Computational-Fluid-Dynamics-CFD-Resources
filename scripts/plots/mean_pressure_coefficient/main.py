"""Compare mock experimental and CFD mean pressure coefficients along a centreline.

The data are synthetic. A smooth base curve C_P(x) is given a flat separation
plateau between x_sep and x_reat for the "experiment"; the "CFD SRS" curve has
a weaker plateau and small seeded noise. The plot mimics a validation figure in
which the simulation under-predicts the separation plateau.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_POINTS = 50
X_MIN, X_MAX = -1.0, 4.0  # streamwise extent (m)
X_SEP, X_REAT = 2.7, 3.5  # plateau start and end (m)
BLEND_WIDTH = 0.08  # smoothing length of the plateau edges (m)
CFD_PLATEAU_STRENGTH = 0.4  # fraction of the experimental plateau seen in CFD
CFD_NOISE = 0.01  # standard deviation of the CFD scatter


def base_cp(x):
    """Smooth mock pressure distribution without separation."""
    return -0.2 * np.sin(x) - 0.1 * np.cos(2 * x)


def plateau_weight(x):
    """Smooth indicator equal to ~1 on [X_SEP, X_REAT] and ~0 elsewhere."""
    rise = 1.0 / (1.0 + np.exp(-(x - X_SEP) / BLEND_WIDTH))
    fall = 1.0 / (1.0 + np.exp(-(X_REAT - x) / BLEND_WIDTH))
    return rise * fall


def mock_cp(x, plateau_strength, noise, rng):
    """Base curve blended towards the constant C_P(X_SEP) inside the plateau."""
    w = plateau_strength * plateau_weight(x)
    cp = (1.0 - w) * base_cp(x) + w * base_cp(X_SEP)
    return cp + noise * rng.normal(size=x.size)


def make_figure(seed=SEED):
    rng = np.random.default_rng(seed)
    x = np.linspace(X_MIN, X_MAX, N_POINTS)
    exp = mock_cp(x, 1.0, 0.0, rng)
    cfd = mock_cp(x, CFD_PLATEAU_STRENGTH, CFD_NOISE, rng)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, exp, "o-", label="Exp", color="black")
    ax.plot(x, cfd, "o-", label="CFD SRS", color="cyan")
    ax.axvspan(X_SEP, X_REAT, color="gray", alpha=0.1)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("$C_P$ [-]")
    ax.set_title("Mean pressure coefficient\nUpper-body centreline (y = 0 m)")
    ax.legend()

    x_note = 0.5 * (X_SEP + X_REAT)
    ax.annotate(
        "Separation plateau less\npronounced in simulation",
        xy=(x_note, base_cp(X_SEP)),
        xytext=(1.2, 0.15),
        arrowprops=dict(facecolor="blue", shrink=0.05),
        fontsize=10,
        color="blue",
    )
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = make_figure()

    finish_figures(
        {"mean_pressure_coefficient.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
