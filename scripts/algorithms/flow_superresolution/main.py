"""Super-resolution and POD denoising of synthetic two-dimensional flow fields.

Super-resolution: random divergence-free velocity fields with a k^-3 energy
spectrum are block-averaged 4x to mimic PIV or coarse-grid data. A cubic-spline
(bicubic) interpolant and a ridge-regression patch model trained on separate
fields both reconstruct a held-out field, compared by relative L2 error and
energy spectrum. Cleansing: noisy snapshots of a convected vortex street are
denoised by truncating their POD, with the error plotted against the rank.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import zoom

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

SEED = 0
N_HIGH = 128  # high-resolution grid points per direction on [0, 2 pi)
FACTOR = 4  # down-sampling factor per direction
SPECTRUM_PEAK = 3.0  # wavenumber of the energy-spectrum peak
SPECTRUM_SLOPE = 3.0  # E(k) ~ k^-SLOPE above the peak
N_TRAIN = 40  # training fields for the patch model
PATCH = 5  # low-resolution patch width used as input (odd)
RIDGE = 1e-3  # ridge penalty, relative to the mean diagonal of X^T X

STREET_NX, STREET_NY = 128, 64  # vortex-street grid [points]
STREET_SNAPSHOTS = 80  # snapshots over one period
VORTEX_RADIUS = 0.35  # Gaussian vortex radius [domain units]
NOISE_LEVEL = 0.5  # noise standard deviation / field RMS


def wavenumbers(n):
    """Integer wavenumbers of an n-point periodic grid on [0, 2 pi)."""
    return np.fft.fftfreq(n, d=1.0 / n)


def random_velocity_field(rng, n=N_HIGH, k0=SPECTRUM_PEAK, slope=SPECTRUM_SLOPE):
    """Divergence-free (u, v) with E(k) ~ k^4 / (1 + (k/k0)^2)^((4 + slope)/2).

    White noise is filtered in Fourier space to give the stream function psi,
    then u = d psi / dy and v = -d psi / dx are evaluated spectrally. The 2D
    shell factor 2 pi k is removed so that the shell-summed spectrum is E(k).
    """
    k = wavenumbers(n)
    kx, ky = np.meshgrid(k, k)  # rows are y, columns are x
    kk = np.hypot(kx, ky)
    kk[0, 0] = 1.0
    energy = (kk / k0) ** 4 / (1 + (kk / k0) ** 2) ** ((4 + slope) / 2)
    amplitude = np.sqrt(energy / (2 * np.pi * kk)) / kk  # |psi_hat|
    amplitude[0, 0] = 0.0
    # Drop the Nyquist modes, whose derivative has no Hermitian partner.
    amplitude[(np.abs(kx) == n // 2) | (np.abs(ky) == n // 2)] = 0.0
    psi_hat = np.fft.fft2(rng.standard_normal((n, n))) * amplitude
    u = np.real(np.fft.ifft2(1j * ky * psi_hat))
    v = np.real(np.fft.ifft2(-1j * kx * psi_hat))
    scale = np.sqrt(np.mean(u**2 + v**2) / 2)
    return u / scale, v / scale


def block_average(field, factor=FACTOR):
    """Measurement operator H: average over factor x factor blocks."""
    n_rows, n_cols = field.shape
    return field.reshape(n_rows // factor, factor, n_cols // factor, factor).mean(
        axis=(1, 3)
    )


def bicubic_upsample(coarse, factor=FACTOR):
    """Periodic cubic-spline interpolation with cell-centred samples."""
    return zoom(coarse, factor, order=3, mode="grid-wrap", grid_mode=True)


def patch_features(coarse, patch=PATCH):
    """Rows of the periodic patch x patch neighbourhood of every coarse cell."""
    half = patch // 2
    shifts = [
        np.roll(coarse, (-a, -b), axis=(0, 1))
        for a in range(-half, half + 1)
        for b in range(-half, half + 1)
    ]
    features = np.stack([s.ravel() for s in shifts], axis=1)
    return np.hstack([features, np.ones((features.shape[0], 1))])


def block_targets(fine, factor=FACTOR):
    """Rows of the factor x factor fine values inside every coarse cell."""
    n_rows, n_cols = fine.shape
    blocks = fine.reshape(n_rows // factor, factor, n_cols // factor, factor)
    return blocks.transpose(0, 2, 1, 3).reshape(-1, factor * factor)


def assemble_blocks(rows, shape, factor=FACTOR):
    """Inverse of block_targets."""
    n_rows, n_cols = shape
    blocks = rows.reshape(n_rows // factor, n_cols // factor, factor, factor)
    return blocks.transpose(0, 2, 1, 3).reshape(shape)


def fit_patch_model(fine_fields, factor=FACTOR, patch=PATCH, ridge=RIDGE):
    """Ridge regression W = (X^T X + lambda I)^-1 X^T Y from patches to blocks."""
    x = np.vstack(
        [patch_features(block_average(f, factor), patch) for f in fine_fields]
    )
    y = np.vstack([block_targets(f, factor) for f in fine_fields])
    gram = x.T @ x
    lam = ridge * np.trace(gram) / gram.shape[0]
    return np.linalg.solve(gram + lam * np.eye(gram.shape[0]), x.T @ y)


def patch_upsample(coarse, weights, factor=FACTOR, patch=PATCH):
    """Apply the learned linear map to every coarse cell."""
    rows = patch_features(coarse, patch) @ weights
    shape = (coarse.shape[0] * factor, coarse.shape[1] * factor)
    return assemble_blocks(rows, shape, factor)


def relative_l2(estimate, truth):
    """||estimate - truth||_2 / ||truth||_2."""
    return float(np.linalg.norm(estimate - truth) / np.linalg.norm(truth))


def energy_spectrum(field):
    """Shell-summed spectrum of 0.5 |u_hat|^2, u_hat normalized by n^2."""
    n = field.shape[0]
    u_hat = np.fft.fft2(field) / n**2
    k = wavenumbers(n)
    shell = np.rint(np.hypot(*np.meshgrid(k, k))).astype(int)
    spectrum = np.bincount(shell.ravel(), weights=0.5 * np.abs(u_hat.ravel()) ** 2)
    return np.arange(1, n // 2), spectrum[1 : n // 2]


def lowpass(field, k_cut):
    """Keep only Fourier modes with |k_x| < k_cut and |k_y| < k_cut."""
    k = wavenumbers(field.shape[0])
    kx, ky = np.meshgrid(k, k)
    mask = (np.abs(kx) < k_cut) & (np.abs(ky) < k_cut)
    return np.real(np.fft.ifft2(np.fft.fft2(field) * mask))


def super_resolution_case(seed=SEED):
    """Train on N_TRAIN fields, test on one held-out field; return all results."""
    rng = np.random.default_rng(seed)
    train = [random_velocity_field(rng)[0] for _ in range(N_TRAIN)]
    truth = random_velocity_field(rng)[0]
    weights = fit_patch_model(train)
    coarse = block_average(truth)
    return {
        "truth": truth,
        "coarse": coarse,
        "bicubic": bicubic_upsample(coarse),
        "ridge": patch_upsample(coarse, weights),
        "lowpass": lowpass(truth, N_HIGH // FACTOR // 2),
    }


def vortex_street(nx=STREET_NX, ny=STREET_NY, n_snap=STREET_SNAPSHOTS):
    """Vorticity of a convected Karman-like street, one period of snapshots.

    Two staggered rows of Gaussian vortices of opposite sign in a periodic box
    of size 4 x 2; the street moves one wavelength (2) over the snapshots.
    Returns an array of shape (ny, nx, n_snap).
    """
    length, height, wavelength = 4.0, 2.0, 2.0
    x = (np.arange(nx) + 0.5) * length / nx
    y = (np.arange(ny) + 0.5) * height / ny
    xx, yy = np.meshgrid(x, y)
    snaps = np.zeros((ny, nx, n_snap))
    for t in range(n_snap):
        shift = wavelength * t / n_snap
        for row_y, sign, offset in ((0.7, 1.0, 0.0), (1.3, -1.0, 0.5 * wavelength)):
            for j in range(int(length / wavelength)):
                xc = (j * wavelength + offset + shift) % length
                dx = (xx - xc + length / 2) % length - length / 2
                r2 = dx**2 + (yy - row_y) ** 2
                # Vortices breathe slightly so the snapshots are not a pure translation.
                strength = 1.0 + 0.2 * np.sin(2 * np.pi * t / n_snap + j)
                snaps[:, :, t] += sign * strength * np.exp(-r2 / VORTEX_RADIUS**2)
    return snaps


def gavish_donoho_threshold(shape, sigma):
    """Optimal hard threshold for singular values with known noise sigma.

    tau = lambda(beta) sqrt(n) sigma, beta = m / n (m <= n),
    lambda(beta) = sqrt(2 (beta + 1) + 8 beta / (beta + 1 + sqrt(beta^2 + 14 beta + 1))).
    """
    m, n = sorted(shape)
    beta = m / n
    lam = np.sqrt(
        2 * (beta + 1) + 8 * beta / (beta + 1 + np.sqrt(beta**2 + 14 * beta + 1))
    )
    return lam * np.sqrt(n) * sigma


def cleansing_case(seed=SEED, noise_level=NOISE_LEVEL):
    """Noisy snapshot matrix, POD truncation errors for every rank."""
    rng = np.random.default_rng(seed + 1)
    clean = vortex_street()
    shape = clean.shape
    clean_mat = clean.reshape(-1, shape[-1])
    sigma = noise_level * np.sqrt(np.mean(clean_mat**2))
    noisy_mat = clean_mat + sigma * rng.standard_normal(clean_mat.shape)
    pod = compute_pod(noisy_mat)
    ranks = np.arange(0, 41)
    errors = np.array([relative_l2(pod.reconstruct(r), clean_mat) for r in ranks])
    tau = gavish_donoho_threshold(noisy_mat.shape, sigma)
    rank_gd = int(np.sum(pod.singular_values > tau))
    return {
        "shape": shape,
        "clean": clean_mat,
        "noisy": noisy_mat,
        "pod": pod,
        "clean_singular_values": compute_pod(clean_mat).singular_values,
        "ranks": ranks,
        "errors": errors,
        "noisy_error": relative_l2(noisy_mat, clean_mat),
        "tau": tau,
        "rank_gd": rank_gd,
    }


def plot_super_resolution(sr):
    fig = plt.figure(figsize=(13, 8.5), layout="constrained")
    top, bottom = fig.subfigures(2, 1, height_ratios=[1, 1.1])
    truth = sr["truth"]
    lim = np.abs(truth).max()
    extent = (0, 2 * np.pi, 0, 2 * np.pi)
    panels = [
        ("Truth, 128 x 128", truth),
        ("Input: 4x block average, 32 x 32", sr["coarse"]),
        (f"Bicubic, error {relative_l2(sr['bicubic'], truth):.3f}", sr["bicubic"]),
        (
            f"Ridge patch model, error {relative_l2(sr['ridge'], truth):.3f}",
            sr["ridge"],
        ),
    ]
    axs = top.subplots(1, 4, sharey=True)
    for ax, (title, field) in zip(axs, panels):
        im = ax.imshow(
            field, origin="lower", cmap="RdBu_r", vmin=-lim, vmax=lim, extent=extent
        )
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x")
    axs[0].set_ylabel("y")
    top.colorbar(im, ax=axs, shrink=0.8, label=r"$u / u_{rms}$")

    axs = bottom.subplots(1, 3, width_ratios=[1, 1, 1.6])
    elim = np.abs(sr["bicubic"] - truth).max()
    for ax, key in zip(axs[:2], ("bicubic", "ridge")):
        im = ax.imshow(
            sr[key] - truth,
            origin="lower",
            cmap="RdBu_r",
            vmin=-elim,
            vmax=elim,
            extent=extent,
        )
        ax.set_title(f"Error, {key}", fontsize=11)
        ax.set_xlabel("x")
    axs[0].set_ylabel("y")
    axs[1].set_yticklabels([])
    bottom.colorbar(
        im, ax=axs[:2], shrink=0.8, label=r"error $/ u_{rms}$", location="left"
    )

    ax = axs[2]
    styles = [
        ("truth", "k", "-", 2.5),
        ("lowpass", "tab:gray", ":", 2.0),
        ("bicubic", "tab:orange", "--", 2.0),
        ("ridge", "tab:blue", "-", 2.0),
    ]
    labels = {"lowpass": "truth with $|k_x|, |k_y| < 16$"}
    for key, color, ls, lw in styles:
        k, e = energy_spectrum(sr[key])
        ax.loglog(k, e, color=color, ls=ls, lw=lw, label=labels.get(key, key))
    kc = N_HIGH // FACTOR // 2
    ax.axvline(kc, color="0.5", lw=1)
    ax.text(kc * 1.05, 1e-9, "input Nyquist\n$k = 16$", fontsize=10, color="0.3")
    ax.set_ylim(1e-11, 1)
    ax.set_xlabel("wavenumber k")
    ax.set_ylabel("E(k) of u")
    ax.set_title("Energy spectra of the held-out field", fontsize=11)
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(True, which="both", alpha=0.3)
    return fig


def plot_cleansing(cl):
    fig = plt.figure(figsize=(13, 8), layout="constrained")
    grid = fig.add_gridspec(2, 3)
    ny, nx, _ = cl["shape"]
    snap = 10
    r_best = int(cl["ranks"][np.argmin(cl["errors"])])
    clean = cl["clean"][:, snap].reshape(ny, nx)
    lim = np.abs(clean).max()
    fields = [
        ("Clean vorticity snapshot", clean),
        (f"Noisy, error {cl['noisy_error']:.2f}", cl["noisy"][:, snap].reshape(ny, nx)),
        (
            f"POD, r = {r_best}, error {cl['errors'][r_best]:.3f}",
            cl["pod"].reconstruct(r_best)[:, snap].reshape(ny, nx),
        ),
    ]
    for col, (title, field) in enumerate(fields):
        ax = fig.add_subplot(grid[0, col])
        im = ax.imshow(
            field,
            origin="lower",
            cmap="RdBu_r",
            vmin=-lim,
            vmax=lim,
            extent=(0, 4, 0, 2),
        )
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.colorbar(im, ax=fig.axes[:3], shrink=0.7, label="vorticity")

    ax = fig.add_subplot(grid[1, :2])
    ax.semilogy(
        cl["ranks"], cl["errors"], "o-", ms=4, color="tab:blue", label="POD truncation"
    )
    ax.axhline(
        cl["noisy_error"], color="tab:red", ls="--", label="noisy data, no filtering"
    )
    ax.axvline(r_best, color="0.4", ls=":", label=f"best rank r = {r_best}")
    ax.axvline(
        cl["rank_gd"],
        color="tab:green",
        ls="-.",
        label=f"Gavish-Donoho rank r = {cl['rank_gd']}",
    )
    ax.set_xlabel("number of POD modes r")
    ax.set_ylabel("relative L2 error vs clean data")
    ax.set_title("Denoising error against truncation rank", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3)

    ax = fig.add_subplot(grid[1, 2])
    n_show = 40
    sv_noisy = cl["pod"].singular_values[:n_show]
    sv_clean = cl["clean_singular_values"][:n_show]
    ax.semilogy(
        np.arange(1, sv_noisy.size + 1),
        sv_noisy,
        "o",
        ms=4,
        color="tab:red",
        label="noisy",
    )
    ax.semilogy(
        np.arange(1, sv_clean.size + 1),
        sv_clean,
        "s",
        ms=4,
        color="k",
        mfc="none",
        label="clean",
    )
    ax.axhline(cl["tau"], color="tab:green", ls="-.", label="threshold")
    ax.set_xlabel("mode index")
    ax.set_ylabel("singular value")
    ax.set_title("Singular values", fontsize=11)
    ax.legend(fontsize=10)
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    sr = super_resolution_case()
    for key in ("bicubic", "ridge", "lowpass"):
        print(f"{key:8s} relative L2 error: {relative_l2(sr[key], sr['truth']):.4f}")
    cl = cleansing_case()
    r_best = int(cl["ranks"][np.argmin(cl["errors"])])
    print(f"noisy snapshots relative L2 error: {cl['noisy_error']:.3f}")
    print(f"best POD rank {r_best}: error {cl['errors'][r_best]:.4f}")
    print(
        f"Gavish-Donoho rank {cl['rank_gd']}: error {cl['errors'][cl['rank_gd']]:.4f}"
    )
    figures = {
        "flow_superresolution.png": plot_super_resolution(sr),
        "flow_cleansing.png": plot_cleansing(cl),
    }
    finish_figures(figures, output=args.output, show=not args.no_show)


if __name__ == "__main__":
    main()
