"""Compress a grayscale image with a truncated singular value decomposition.

Loads a grayscale image (by default the "camera" sample bundled with
scikit-image), reconstructs it from its 5, 25 and 100 largest singular values,
and plots the singular value spectrum and the cumulative energy ratio.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage import color, data, io
from skimage.util import img_as_float

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

RANKS = [5, 25, 100]  # truncation ranks shown next to the original
ENERGY_LEVELS = [0.90, 0.95, 0.99]  # energy fractions marked on the energy plot


def load_grayscale_image(path=None):
    """Return a 2-D float image in [0, 1]; use the bundled sample if path is None."""
    image = data.camera() if path is None else io.imread(path)
    if image.ndim == 3:
        if image.shape[-1] == 4:
            image = color.rgba2rgb(image)
        image = color.rgb2gray(image)
    return img_as_float(image)


def reconstruct_image(U, S, Vt, rank):
    """Rank-r approximation A_r = U_r diag(S_r) V_r^T."""
    return (U[:, :rank] * S[:rank]) @ Vt[:rank, :]


def compression_ratio(m, n, rank):
    """Values stored by the full image divided by those of the rank-r factors."""
    return m * n / (rank * (m + n + 1))


def energy_ratios(S):
    """Cumulative energy ratio E(r) for r = 1, ..., p."""
    return np.cumsum(S**2) / np.sum(S**2)


def rank_for_energy(ratios, level):
    """Smallest rank r with E(r) >= level."""
    return int(np.searchsorted(ratios, level) + 1)


def plot_reconstructions(image, U, S, Vt, ranks):
    m, n = image.shape
    fig, axes = plt.subplots(1, len(ranks) + 1, figsize=(12, 4))
    axes[0].imshow(image, cmap="gray", vmin=0, vmax=1)
    axes[0].set_title("Original image")
    axes[0].axis("off")
    for ax, rank in zip(axes[1:], ranks):
        approx = np.clip(reconstruct_image(U, S, Vt, rank), 0.0, 1.0)
        ax.imshow(approx, cmap="gray", vmin=0, vmax=1)
        ratio = compression_ratio(m, n, rank)
        ax.set_title(f"Rank {rank} approximation\ncompression ratio {ratio:.1f}")
        ax.axis("off")
    fig.tight_layout()
    return fig


def plot_singular_values(S):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(np.arange(1, S.size + 1), S, "b-o", markersize=3)
    ax.set_yscale("log")
    ax.set_xlabel("Index $i$")
    ax.set_ylabel(r"Singular value $\sigma_i$")
    ax.set_title("Singular values of the image")
    ax.grid(True)
    return fig


def plot_energy_ratios(ratios, levels):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(np.arange(1, ratios.size + 1), ratios, "b-o", markersize=3)
    for level, style in zip(levels, [":", "-.", "--"]):
        r = rank_for_energy(ratios, level)
        ax.axhline(
            y=level, color="r", linestyle=style, label=f"{level:.0%} energy at r = {r}"
        )
    ax.set_xlabel("Truncated SVD size $r$")
    ax.set_ylabel(r"Energy ratio $\mathcal{E}(r)$")
    ax.set_title("Energy ratios in dependence on the size of the truncated SVD")
    ax.legend(loc="lower right")
    ax.grid(True)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--image",
        metavar="PATH",
        help="image file to compress (default: scikit-image 'camera' sample)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    image = load_grayscale_image(args.image)
    U, S, Vt = np.linalg.svd(image, full_matrices=False)
    ratios = energy_ratios(S)

    print(f"Image size: {image.shape[0]} x {image.shape[1]}")
    for level in ENERGY_LEVELS:
        print(f"Rank needed for {level:.0%} energy: {rank_for_energy(ratios, level)}")

    figures = {
        "reconstructed_images": plot_reconstructions(image, U, S, Vt, RANKS),
        "singular_values": plot_singular_values(S),
        "energy_ratios": plot_energy_ratios(ratios, ENERGY_LEVELS),
    }

    finish_figures(
        {f"{name}.png": fig for (name, fig) in figures.items()},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
