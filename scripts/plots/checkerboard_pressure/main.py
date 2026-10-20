"""Checkerboard pressure: the null space of collocated linear interpolation.

On a collocated grid, face pressures interpolated linearly from cell centres
give the cell pressure gradient (p_{i+1} - p_{i-1}) / (2 dx). It vanishes for
the checkerboard field p_i = (-1)^i, so momentum never sees that pressure, and
the pressure equation obtained from the divergence of the interpolated
gradient (a stencil of width 2 dx) has the checkerboard in its null space. The
compact Laplacian that Rhie-Chow interpolation produces does not. The figure
shows a 2D checkerboard, both operators applied to a 1D one, and the eigenvalue
spectra of both Laplacians on periodic grids.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LENGTH = 1.0  # domain length [m]
N_1D = 16  # cells of the 1D periodic grid
N_2D = 12  # cells per side of the 2D periodic grid
ZERO_TOL = 1e-9  # eigenvalues with |lambda| dx^2 below this count as zero


def periodic_shift(n, k):
    """Matrix S with (S p)_i = p_{i+k} on a periodic 1D grid of n cells."""
    return np.roll(np.eye(n), k, axis=1)


def central_gradient(n, dx):
    """Cell gradient from linearly interpolated face pressures.

    p_{i+1/2} = (p_i + p_{i+1}) / 2 gives (p_{i+1/2} - p_{i-1/2}) / dx
    = (p_{i+1} - p_{i-1}) / (2 dx).
    """
    return (periodic_shift(n, 1) - periodic_shift(n, -1)) / (2.0 * dx)


def wide_laplacian(n, dx):
    """Divergence of the interpolated cell gradient: (p_{i+2} - 2 p_i + p_{i-2}) / (4 dx^2)."""
    G = central_gradient(n, dx)
    return G @ G


def compact_laplacian(n, dx):
    """Face-gradient Laplacian (p_{i+1} - 2 p_i + p_{i-1}) / dx^2 (Rhie-Chow type)."""
    return (periodic_shift(n, 1) - 2.0 * np.eye(n) + periodic_shift(n, -1)) / dx**2


def laplacian_2d(laplacian_1d):
    """Kronecker sum L (x) I + I (x) L on an n x n periodic grid."""
    n = laplacian_1d.shape[0]
    identity = np.eye(n)
    return np.kron(laplacian_1d, identity) + np.kron(identity, laplacian_1d)


def checkerboard(n, dims=1):
    """p = (-1)^i in 1D or (-1)^(i + j) in 2D."""
    index = np.indices((n,) * dims).sum(axis=0)
    return (-1.0) ** index


def symbol_wide(theta, dx):
    """Eigenvalue of the wide Laplacian for the Fourier mode exp(i theta j)."""
    return -(np.sin(theta) ** 2) / dx**2


def symbol_compact(theta, dx):
    """Eigenvalue of the compact Laplacian for the Fourier mode exp(i theta j)."""
    return -4.0 * np.sin(theta / 2.0) ** 2 / dx**2


def count_zero_eigenvalues(matrix, dx):
    eigenvalues = np.linalg.eigvalsh(matrix)
    return int(np.sum(np.abs(eigenvalues) * dx**2 < ZERO_TOL)), eigenvalues


def circulant_eigenvalues(matrix):
    """Eigenvalues of a periodic (circulant) operator: the DFT of its first row.

    Entry m belongs to the Fourier mode exp(2 pi i m j / n), wavenumber
    theta_m = 2 pi m / n.
    """
    return np.real(np.fft.fft(matrix[0]))


def plot_checkerboard(n_1d=N_1D, n_2d=N_2D):
    dx1, dx2 = LENGTH / n_1d, LENGTH / n_2d
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    axes = axes.ravel()

    ax = axes[0]
    image = ax.imshow(
        checkerboard(n_2d, 2), cmap="RdBu_r", vmin=-1.5, vmax=1.5,
        extent=(0, LENGTH, 0, LENGTH), origin="lower",
    )  # fmt: skip
    fig.colorbar(image, ax=ax, label="p [Pa]", fraction=0.046)
    ax.set(
        title=r"2D checkerboard $p_{ij} = (-1)^{i+j}$", xlabel="x [m]", ylabel="y [m]"
    )

    ax = axes[1]
    x = (np.arange(n_1d) + 0.5) * dx1
    p = checkerboard(n_1d)
    gradient = central_gradient(n_1d, dx1) @ p * dx1
    wide = wide_laplacian(n_1d, dx1) @ p * dx1**2
    compact = compact_laplacian(n_1d, dx1) @ p * dx1**2
    ax.plot(x, p, "o:", color="0.35", label=r"$p_i = (-1)^i$")
    ax.plot(
        x,
        compact,
        "o-",
        color="tab:red",
        label=r"compact Laplacian $\times\,\Delta x^2$",
    )
    ax.plot(
        x,
        wide,
        "s-",
        color="tab:blue",
        ms=7,
        label=r"wide Laplacian $\times\,\Delta x^2$",
    )
    ax.plot(
        x,
        gradient,
        "^--",
        color="tab:orange",
        label=r"interpolated gradient $\times\,\Delta x$",
    )
    ax.set(
        title=f"Operators applied to a 1D checkerboard (N = {n_1d})",
        xlabel="x [m]", ylabel="value [Pa]", ylim=(-5, 6.5),
    )  # fmt: skip
    ax.legend(loc="upper center", ncols=2, fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[2]
    theta = np.linspace(0.0, np.pi, 400)
    ax.plot(
        theta, -symbol_compact(theta, dx1) * dx1**2, color="tab:red", label="compact"
    )
    ax.plot(theta, -symbol_wide(theta, dx1) * dx1**2, color="tab:blue", label="wide")
    modes = 2.0 * np.pi * np.arange(n_1d) / n_1d
    half = modes <= np.pi
    for laplacian, color, marker in (
        (compact_laplacian, "tab:red", "o"),
        (wide_laplacian, "tab:blue", "s"),
    ):
        values = circulant_eigenvalues(laplacian(n_1d, dx1))
        ax.plot(
            modes[half], -values[half] * dx1**2, marker, color=color, ms=7, mfc="none"
        )
    ax.annotate(
        "checkerboard mode:\nzero eigenvalue of\nthe wide Laplacian", xy=(np.pi, 0.0),
        xytext=(1.75, 1.6), arrowprops={"arrowstyle": "->"}, fontsize=10,
    )  # fmt: skip
    ax.set(
        title=f"Eigenvalues on a 1D periodic grid (N = {n_1d})",
        xlabel=r"wavenumber $\theta = k\,\Delta x$ [rad]",
        ylabel=r"$-\lambda\,\Delta x^2$ [-]", xlim=(-0.05, np.pi * 1.03), ylim=(-0.1, 4.3),
    )  # fmt: skip
    ax.set_xticks([0, np.pi / 2, np.pi], ["0", r"$\pi/2$", r"$\pi$"])
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)

    ax = axes[3]
    shown = 12
    for laplacian, color, marker, name in (
        (compact_laplacian, "tab:red", "o", "compact"),
        (wide_laplacian, "tab:blue", "s", "wide"),
    ):
        zeros, values = count_zero_eigenvalues(laplacian_2d(laplacian(n_2d, dx2)), dx2)
        smallest = np.sort(-values * dx2**2)[:shown]
        ax.plot(
            np.arange(1, shown + 1), smallest, marker, color=color, ms=8, mfc="none",
            label=f"{name}: {zeros} zero eigenvalue{'s' if zeros > 1 else ''}",
        )  # fmt: skip
    ax.set(
        title=f"Smallest eigenvalues on a 2D periodic grid ({n_2d} x {n_2d})",
        xlabel="eigenvalue index (ascending) [-]", ylabel=r"$-\lambda\,\Delta x^2$ [-]",
    )  # fmt: skip
    ax.set_xticks(range(1, shown + 1))
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    dx1, dx2 = LENGTH / N_1D, LENGTH / N_2D
    p = checkerboard(N_1D)
    print(f"1D checkerboard, N = {N_1D}:")
    print(
        f"  max |central gradient| = {np.abs(central_gradient(N_1D, dx1) @ p).max():.1e}"
    )
    print(
        f"  max |wide Laplacian|   = {np.abs(wide_laplacian(N_1D, dx1) @ p).max():.1e}"
    )
    print(
        f"  compact Laplacian / p  = {(compact_laplacian(N_1D, dx1) @ p / p)[0] * dx1**2:.1f} / dx^2"
    )
    for name, laplacian in (("wide", wide_laplacian), ("compact", compact_laplacian)):
        zeros_1d, _ = count_zero_eigenvalues(laplacian(N_1D, dx1), dx1)
        zeros_2d, _ = count_zero_eigenvalues(laplacian_2d(laplacian(N_2D, dx2)), dx2)
        print(
            f"  {name:7s} Laplacian: {zeros_1d} zero eigenvalue(s) in 1D (N = {N_1D}), "
            f"{zeros_2d} in 2D ({N_2D} x {N_2D})"
        )
    finish_figures(
        {"checkerboard_pressure.png": plot_checkerboard()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
