"""Synthetic instantaneous velocity field and its mean, as in a Reynolds decomposition.

A noisy longitudinal velocity field u(x, y) is generated on a 200 x 60 grid.
Since the data has no time axis, the mean is taken along the streamwise
direction x (a stand-in for a time average) to give u_bar(y).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

X_RANGE = (1750.0, 1900.0)  # mm
Y_RANGE = (0.0, 60.0)  # mm
NX, NY = 200, 60
NOISE_STD = 5.0  # m/s
SEED = 0


def synthetic_velocity_field(X, Y, rng, noise_std=NOISE_STD):
    """u(x, y) = 10 sin(0.02 x) cos(0.1 y) + Gaussian noise (x, y in mm, u in m/s)."""
    return 10 * np.sin(0.02 * X) * np.cos(0.1 * Y) + noise_std * rng.standard_normal(
        X.shape
    )


def streamwise_average(field):
    """Average a (ny, nx) field over x, returning the profile u_bar(y) of length ny."""
    return field.mean(axis=1)


def plot_fields(seed=SEED):
    """Plot the instantaneous field and its x-averaged mean; return the figure."""
    rng = np.random.default_rng(seed)
    x = np.linspace(*X_RANGE, NX)
    y = np.linspace(*Y_RANGE, NY)
    X, Y = np.meshgrid(x, y)  # shape (NY, NX)
    u = synthetic_velocity_field(X, Y, rng)
    u_mean = streamwise_average(u)

    fig = plt.figure(figsize=(10, 10))

    plt.subplot(2, 1, 1)
    plt.imshow(
        u,
        extent=[*X_RANGE, *Y_RANGE],
        origin="lower",  # row 0 of the array is y = 0
        aspect="auto",
        cmap="jet",
    )
    plt.colorbar(label="U (m/s)")
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    plt.title("Instantaneous longitudinal velocity field")

    plt.subplot(2, 1, 2)
    plt.contourf(X, Y, np.tile(u_mean[:, None], (1, NX)), levels=50, cmap="jet")
    plt.colorbar(label="U (m/s)")
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    plt.title(
        "Time-averaged longitudinal velocity field (approximated by the mean along x)"
    )

    plt.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    fig = plot_fields()

    finish_figures(
        {"time_averaged_velocity_field.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
