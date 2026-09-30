"""Generate and plot noisy synthetic boundary-layer velocity data.

Builds a square-root velocity profile U0 = U_inf sqrt(y / delta) that reaches
the free-stream value at y = delta, adds Gaussian noise to the streamwise
component, writes the samples to a CSV file and plots the velocity components
against the wall-normal coordinate.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

U_INF = 1.0  # free-stream velocity (m/s)
DELTA = 0.05  # boundary layer thickness (m)
NUM_POINTS = 100  # number of wall-normal samples
NOISE_STD = 0.02  # standard deviation of the noise on U0 (m/s)
SEED = 42  # random seed for reproducible noise
CSV_NAME = "boundary_layer_data.csv"


def velocity_profile(y, u_inf=U_INF, delta=DELTA):
    """Square-root profile inside the layer, U_inf outside it."""
    return u_inf * np.sqrt(np.minimum(y / delta, 1.0))


def generate_data(num_points=NUM_POINTS, noise_std=NOISE_STD, seed=SEED):
    """Return Y and the velocity components U0 (noisy), U1 and U2 (zero)."""
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 2 * DELTA, num_points)
    u0 = velocity_profile(y) + rng.normal(0, noise_std, num_points)
    u1 = np.zeros(num_points)  # no flow in the y direction
    u2 = np.zeros(num_points)  # no flow in the z direction
    return y, u0, u1, u2


def save_csv(path, y, u0, u1, u2):
    """Write columns U0, U1, U2, X, Y, Z (X = Z = 0) to a CSV file."""
    zeros = np.zeros_like(y)
    data = np.column_stack((u0, u1, u2, zeros, y, zeros))
    np.savetxt(path, data, delimiter=",", header="U0,U1,U2,X,Y,Z", comments="")


def plot_u0(y, u0):
    fig, ax = plt.subplots()
    ax.plot(y, u0, "*")
    ax.set_xlabel("Y [m]")
    ax.set_ylabel("U0 [m/s]")
    ax.set_title("U0 versus Y")
    ax.grid()
    return fig


def plot_all_components(y, u0, u1, u2):
    fig, ax = plt.subplots()
    ax.plot(y, u0, "*", label="U0")
    ax.plot(y, u1, "-", label="U1")
    ax.plot(y, u2, ".", label="U2")
    ax.set_xlabel("Y [m]")
    ax.set_ylabel("U [m/s]")
    ax.set_title("U versus Y")
    ax.legend(loc="center left", bbox_to_anchor=(0.6, 0.5), numpoints=2)
    ax.grid()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    y, u0, u1, u2 = generate_data()

    out_dir = Path(args.output) if args.output else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)
    save_csv(out_dir / CSV_NAME, y, u0, u1, u2)
    print(f"Saved {out_dir / CSV_NAME}")

    figures = {
        "U0_vs_Y": plot_u0(y, u0),
        "U_vs_Y": plot_all_components(y, u0, u1, u2),
    }
    finish_figures(
        {f"{name}.png": fig for (name, fig) in figures.items()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
