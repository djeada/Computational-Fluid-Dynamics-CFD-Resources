"""Principal component analysis of a family of NACA 4-digit airfoils.

Draws random NACA 4-digit airfoils (maximum camber m, camber position p,
thickness t), samples every airfoil at the same cosine-spaced chord stations,
stacks the upper and lower surface ordinates into one shape vector per airfoil
and runs PCA on the training shapes. The figure shows the explained variance,
the mean shape, the shapes obtained by moving +/-2 standard deviations along
the first three principal components, and the reconstruction error of unseen
airfoils as a function of the number of retained modes.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

SEED = 3
N_STATIONS = 81  # chordwise stations per surface (cosine spacing)
N_TRAIN = 200  # airfoils used to build the shape space
N_TEST = 100  # unseen airfoils used to measure reconstruction error
M_RANGE = (0.0, 0.06)  # maximum camber, fraction of chord
P_RANGE = (0.2, 0.6)  # chordwise position of maximum camber, fraction of chord
T_RANGE = (0.06, 0.18)  # maximum thickness, fraction of chord
N_SHOW_MODES = 3  # principal components drawn as +/-2 sigma shape variations
MAX_MODES = 10  # largest mode count on the reconstruction-error plot


def cosine_stations(n=N_STATIONS):
    """Chord stations x/c in [0, 1] clustered at the leading and trailing edges."""
    return 0.5 * (1.0 - np.cos(np.linspace(0.0, np.pi, n)))


def naca_thickness(x, t):
    """Half-thickness of a NACA 4-digit section (open trailing edge)."""
    return (
        5.0
        * t
        * (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
    )


def naca_camber(x, m, p):
    """Mean camber line of a NACA 4-digit section."""
    if m == 0.0:
        return np.zeros_like(x)
    front = m / p**2 * (2.0 * p * x - x**2)
    back = m / (1.0 - p) ** 2 * ((1.0 - 2.0 * p) + 2.0 * p * x - x**2)
    return np.where(x < p, front, back)


def airfoil_vector(x, m, p, t):
    """Shape vector [y_upper(x), y_lower(x)] with thickness added vertically."""
    yc = naca_camber(x, m, p)
    yt = naca_thickness(x, t)
    return np.concatenate([yc + yt, yc - yt])


def sample_parameters(n, rng):
    """Uniform random (m, p, t) triples in the ranges set by the constants."""
    lows = np.array([M_RANGE[0], P_RANGE[0], T_RANGE[0]])
    highs = np.array([M_RANGE[1], P_RANGE[1], T_RANGE[1]])
    return lows + (highs - lows) * rng.random((n, 3))


def build_shape_matrix(x, params):
    """Columns are shape vectors, one per airfoil (points in rows)."""
    return np.column_stack([airfoil_vector(x, *row) for row in params])


def reconstruct(pod, shapes, n_modes):
    """Project shapes onto the leading modes and map back to coordinates."""
    basis = pod.modes[:, :n_modes]
    return pod.mean + basis @ (basis.T @ (shapes - pod.mean))


def rms_error(reference, approximation):
    """Root-mean-square ordinate error of each column, in chord units."""
    return np.sqrt(np.mean((reference - approximation) ** 2, axis=0))


def reconstruction_errors(pod, shapes, max_modes=MAX_MODES):
    """Mean and worst RMS error of the shapes for 0..max_modes modes."""
    counts = np.arange(0, max_modes + 1)
    errors = np.array([rms_error(shapes, reconstruct(pod, shapes, k)) for k in counts])
    return counts, errors.mean(axis=1), errors.max(axis=1)


def plot_shape(ax, x, vector, **kwargs):
    """Draw a closed airfoil outline from a stacked shape vector."""
    n = x.size
    xs = np.concatenate([x[::-1], x[1:]])
    ys = np.concatenate([vector[:n][::-1], vector[n + 1 :]])
    return ax.plot(xs, ys, **kwargs)


def make_figure(x, pod, counts, mean_err, max_err):
    fig = plt.figure(figsize=(13, 7.5))
    grid = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.25, 1.25])
    ax_var = fig.add_subplot(grid[0, 0])
    ax_err = fig.add_subplot(grid[1, 0])
    shape_axes = [fig.add_subplot(grid[i, j]) for i in range(2) for j in (1, 2)]

    n_bars = 8
    fractions = pod.energy_fractions[:n_bars]
    ax_var.bar(np.arange(1, n_bars + 1), fractions, color="tab:blue", label="per mode")
    ax_var.plot(
        np.arange(1, n_bars + 1),
        np.cumsum(fractions),
        "o-",
        color="tab:orange",
        label="cumulative",
    )
    ax_var.set_yscale("log")
    ax_var.set_ylim(1e-6, 3.0)
    ax_var.set_xlabel("principal component $k$")
    ax_var.set_ylabel("explained variance fraction")
    ax_var.set_title("Explained variance")
    ax_var.legend(loc="center right")

    ax_err.semilogy(counts, mean_err, "o-", color="tab:blue", label="mean (test set)")
    ax_err.semilogy(counts, max_err, "s--", color="tab:red", label="worst test airfoil")
    ax_err.set_xlabel("number of retained modes $K$")
    ax_err.set_ylabel("RMS ordinate error $/c$")
    ax_err.set_title(f"Reconstruction of {N_TEST} unseen airfoils")
    ax_err.grid(True, which="both", alpha=0.3)
    ax_err.legend(loc="upper right")

    mean = pod.mean[:, 0]
    plot_shape(shape_axes[0], x, mean, color="k", lw=2)
    shape_axes[0].set_title(f"Mean of {pod.n_snapshots} training airfoils")

    sigmas = np.sqrt(pod.eigenvalues)
    for k, ax in enumerate(shape_axes[1 : 1 + N_SHOW_MODES]):
        plot_shape(ax, x, mean, color="0.6", lw=1.5, label="mean")
        for sign, color in ((-2, "tab:blue"), (2, "tab:red")):
            shape = mean + sign * sigmas[k] * pod.modes[:, k]
            plot_shape(
                ax, x, shape, color=color, lw=1.8, label=rf"${sign:+d}\sigma_{k + 1}$"
            )
        ax.set_title(f"PC{k + 1}: {100 * pod.energy_fractions[k]:.1f}% of variance")
        ax.legend(loc="upper right", fontsize=9, ncol=3)

    for ax in shape_axes:
        ax.set_aspect(2.0)
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.15, 0.22)
        ax.set_xlabel("$x/c$")
        ax.set_ylabel("$y/c$ (vertical scale x2)")
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


def parse_args(argv=None):
    return create_parser(__doc__).parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    rng = np.random.default_rng(SEED)
    x = cosine_stations()
    train = build_shape_matrix(x, sample_parameters(N_TRAIN, rng))
    test = build_shape_matrix(x, sample_parameters(N_TEST, rng))

    pod = compute_pod(train)
    counts, mean_err, max_err = reconstruction_errors(pod, test)
    cumulative = np.cumsum(pod.energy_fractions)
    for k in range(1, 6):
        print(
            f"K={k}: cumulative variance {cumulative[k - 1]:.6f}, "
            f"test RMS error mean {mean_err[k]:.2e}, worst {max_err[k]:.2e}"
        )

    fig = make_figure(x, pod, counts, mean_err, max_err)
    finish_figures(
        {"airfoil_shape_pca.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
