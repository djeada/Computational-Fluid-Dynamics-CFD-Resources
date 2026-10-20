"""PIV by FFT cross-correlation with sub-pixel peak fitting and outlier detection.

Renders a synthetic pair of particle images whose particles move with a known
Lamb-Oseen vortex, decorrelates a few interrogation windows to create spurious
vectors, estimates the displacement field with two-pass FFT cross-correlation
and a three-point Gaussian peak fit, then flags and replaces outliers with the
normalized median test.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.special import erf

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 3
IMAGE_SIZE = 320  # image width and height [px]
PARTICLE_DENSITY = 0.03  # particles per pixel [ppp]
PARTICLE_DIAMETER = 2.8  # e^-2 particle image diameter [px]
NOISE_STD = 0.03  # camera noise, relative to the peak particle intensity
WINDOW = 32  # interrogation window size [px]
STEP = 16  # window spacing (50 % overlap) [px]
CORE_RADIUS = 48.0  # Lamb-Oseen core radius [px]
MAX_DISPLACEMENT = 5.0  # peak swirl displacement between frames [px]
N_DEFORMATION_PASSES = 3  # window-deformation passes after the first pass
PREDICTOR_SMOOTHING = 0.6  # Gaussian filter width on the predictor [grid spacings]
N_DECORRELATED = 5  # windows whose second-frame content is replaced
MEDIAN_EPS = 0.1  # normalized median test noise level [px]
MEDIAN_THRESHOLD = 2.0  # normalized median test threshold [-]

# max over x of (1 - exp(-x^2)) / x, reached at x = 1.1209
_LAMB_OSEEN_PEAK = 0.63817


def render_particles(x, y, intensity, size, diameter):
    """Render pixel-integrated Gaussian particle images.

    Pixel (i, j) covers [j - 1/2, j + 1/2] x [i - 1/2, i + 1/2], so a particle
    at x = j, y = i is centred on that pixel. The image is G_y^T diag(I) G_x.
    """
    sigma = diameter / 4.0
    edges = np.arange(size + 1) - 0.5
    scale = np.sqrt(2.0) * sigma
    gx = 0.5 * np.diff(erf((edges[None, :] - x[:, None]) / scale), axis=1)
    gy = 0.5 * np.diff(erf((edges[None, :] - y[:, None]) / scale), axis=1)
    # Peak pixel value of a centred particle is about intensity * (2 pi sigma^2)^-1
    norm = 2.0 * np.pi * sigma**2
    return (gy * (intensity * norm)[:, None]).T @ gx


def lamb_oseen_displacement(x, y, center, core_radius, max_displacement):
    """Displacement (dx, dy) [px] of a Lamb-Oseen vortex, anticlockwise."""
    rx, ry = x - center[0], y - center[1]
    r = np.hypot(rx, ry)
    r_safe = np.where(r > 0, r, 1.0)
    amplitude = max_displacement / _LAMB_OSEEN_PEAK
    u_theta = (
        amplitude * (core_radius / r_safe) * (1 - np.exp(-((r / core_radius) ** 2)))
    )
    u_theta = np.where(r > 0, u_theta, 0.0)
    return -u_theta * ry / r_safe, u_theta * rx / r_safe


def make_image_pair(displacement, rng, size=IMAGE_SIZE, density=PARTICLE_DENSITY):
    """Seed particles and render both frames.

    A particle seeded at x_m is drawn at x_m - d(x_m)/2 in frame 1 and at
    x_m + d(x_m)/2 in frame 2, so d(x) is the displacement of the particle whose
    path midpoint is x (a central-difference estimate of u * dt).
    """
    margin = 12.0  # seed outside the image so particles can enter the frames [px]
    n = int(density * (size + 2 * margin) ** 2)
    xm = rng.uniform(-margin, size + margin, n)
    ym = rng.uniform(-margin, size + margin, n)
    intensity = rng.uniform(0.6, 1.0, n)
    dx, dy = displacement(xm, ym)
    frame1 = render_particles(
        xm - dx / 2, ym - dy / 2, intensity, size, PARTICLE_DIAMETER
    )
    frame2 = render_particles(
        xm + dx / 2, ym + dy / 2, intensity, size, PARTICLE_DIAMETER
    )
    frame1 += NOISE_STD * rng.standard_normal(frame1.shape)
    frame2 += NOISE_STD * rng.standard_normal(frame2.shape)
    return frame1, frame2


def decorrelate_windows(frame2, starts, rng, window=WINDOW):
    """Replace frame-2 content of whole windows by unrelated particles."""
    frame2 = frame2.copy()
    for x0, y0 in starts:
        n = int(PARTICLE_DENSITY * window**2)
        x = rng.uniform(-0.5, window - 0.5, n)
        y = rng.uniform(-0.5, window - 0.5, n)
        patch = render_particles(
            x, y, rng.uniform(0.6, 1.0, n), window, PARTICLE_DIAMETER
        )
        patch += NOISE_STD * rng.standard_normal(patch.shape)
        frame2[y0 : y0 + window, x0 : x0 + window] = patch
    return frame2


def cross_correlation(window1, window2):
    """Normalized circular cross-correlation, zero displacement at the centre.

    R(s) = sum_x a(x) b(x + s) with a, b the mean-subtracted windows, computed
    as IFFT(conj(FFT a) * FFT b) and divided by sqrt(sum a^2 sum b^2).
    """
    a = window1 - window1.mean()
    b = window2 - window2.mean()
    corr = np.fft.irfft2(np.conj(np.fft.rfft2(a)) * np.fft.rfft2(b), s=a.shape)
    denom = np.sqrt(np.sum(a**2) * np.sum(b**2))
    return np.fft.fftshift(corr) / (denom if denom > 0 else 1.0)


def gaussian_subpixel(minus, centre, plus):
    """Three-point Gaussian peak offset; falls back to a parabola if any <= 0."""
    if min(minus, centre, plus) <= 0:
        denom = minus - 2 * centre + plus
        return 0.0 if denom == 0 else 0.5 * (minus - plus) / denom
    lm, lc, lp = np.log(minus), np.log(centre), np.log(plus)
    denom = lm - 2 * lc + lp
    return 0.0 if denom == 0 else 0.5 * (lm - lp) / denom


def correlation_peak(corr):
    """Sub-pixel displacement (dx, dy) of the highest correlation peak."""
    n_rows, n_cols = corr.shape
    i, j = np.unravel_index(np.argmax(corr), corr.shape)
    i = int(np.clip(i, 1, n_rows - 2))
    j = int(np.clip(j, 1, n_cols - 2))
    di = gaussian_subpixel(corr[i - 1, j], corr[i, j], corr[i + 1, j])
    dj = gaussian_subpixel(corr[i, j - 1], corr[i, j], corr[i, j + 1])
    return j + dj - n_cols // 2, i + di - n_rows // 2


def window_starts(size=IMAGE_SIZE, window=WINDOW, step=STEP):
    """First pixel index of each interrogation window along one axis."""
    return np.arange(0, size - window + 1, step)


def window_centres(size=IMAGE_SIZE, window=WINDOW, step=STEP):
    """Window centre coordinates [px] along one axis (pixel centres are integers)."""
    return window_starts(size, window, step) + (window - 1) / 2


def correlate_grid(frame1, frame2, window=WINDOW, step=STEP):
    """Displacement of the correlation peak in every window of a grid."""
    starts = window_starts(frame1.shape[0], window, step)
    dx = np.zeros((starts.size, starts.size))
    dy = np.zeros_like(dx)
    for r, y0 in enumerate(starts):
        for c, x0 in enumerate(starts):
            w1 = frame1[y0 : y0 + window, x0 : x0 + window]
            w2 = frame2[y0 : y0 + window, x0 : x0 + window]
            dx[r, c], dy[r, c] = correlation_peak(cross_correlation(w1, w2))
    return dx, dy


def dense_predictor(component, size=IMAGE_SIZE, window=WINDOW, step=STEP):
    """Interpolate a vector-grid component to every pixel (cubic spline)."""
    centres = window_centres(size, window, step)
    index = (np.arange(size) - centres[0]) / step
    rows, cols = np.meshgrid(index, index, indexing="ij")
    return map_coordinates(component, [rows, cols], order=3, mode="nearest")


def warp_pair(frame1, frame2, predictor, window=WINDOW, step=STEP):
    """Warp both frames symmetrically by the interpolated predictor.

    Frame 1 is sampled at x - d(x)/2 and frame 2 at x + d(x)/2 (cubic spline
    interpolation), so particles that follow the predicted field line up.
    """
    size = frame1.shape[0]
    pdx = dense_predictor(predictor[0], size, window, step)
    pdy = dense_predictor(predictor[1], size, window, step)
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    warp1 = map_coordinates(frame1, [yy - pdy / 2, xx - pdx / 2], order=3, cval=0.0)
    warp2 = map_coordinates(frame2, [yy + pdy / 2, xx + pdx / 2], order=3, cval=0.0)
    return warp1, warp2


def deformation_pass(frame1, frame2, predictor, window=WINDOW, step=STEP):
    """Correlate the warped pair and add the residual to the predictor."""
    warped = warp_pair(frame1, frame2, predictor, window, step)
    rx, ry = correlate_grid(*warped, window, step)
    return (predictor[0] + rx, predictor[1] + ry), warped


def _neighbours(field):
    """Stack of the 8 neighbours of every node (NaN outside the grid)."""
    padded = np.pad(field, 1, constant_values=np.nan)
    n_rows, n_cols = field.shape
    shifts = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    return np.stack(
        [padded[1 + a : 1 + a + n_rows, 1 + b : 1 + b + n_cols] for a, b in shifts]
    )


def normalized_median_test(dx, dy, eps=MEDIAN_EPS, threshold=MEDIAN_THRESHOLD):
    """Westerweel & Scarano (2005) normalized median test.

    For each component, r0 = |U0 - Um| / (rm + eps), where Um is the median of
    the 8 neighbours and rm the median of their residuals |Ui - Um|. A vector
    is flagged when r0 > threshold for either component.
    """
    flagged = np.zeros(dx.shape, dtype=bool)
    for comp in (dx, dy):
        neigh = _neighbours(comp)
        median = np.nanmedian(neigh, axis=0)
        residual = np.nanmedian(np.abs(neigh - median), axis=0)
        r0 = np.abs(comp - median) / (residual + eps)
        flagged |= r0 > threshold
    return flagged


def replace_outliers(dx, dy, flagged, max_iter=10):
    """Replace flagged vectors by the median of their valid neighbours."""
    dx, dy, bad = dx.copy(), dy.copy(), flagged.copy()
    for _ in range(max_iter):
        if not bad.any():
            break
        for comp in (dx, dy):
            masked = np.where(bad, np.nan, comp)
            comp[bad] = np.nanmedian(_neighbours(masked), axis=0)[bad]
        bad = bad & np.isnan(dx)
        dx[bad] = dy[bad] = np.nan
    return dx, dy


def run_piv(frame1, frame2, n_deform=N_DEFORMATION_PASSES):
    """Plain pass, then deformation passes; validate and replace after each.

    The validated field is smoothed with a narrow Gaussian before it is used
    as the predictor: without it, vector-to-vector noise at the grid Nyquist
    frequency is not corrected by the window average and the iteration stalls.
    Returns the raw field of every pass, the flags of the last pass and the
    final validated field.
    """
    raw = correlate_grid(frame1, frame2)
    passes = [raw]
    warped, predictor = (frame1, frame2), (np.zeros_like(raw[0]), np.zeros_like(raw[1]))
    for _ in range(n_deform):
        validated = replace_outliers(*raw, normalized_median_test(*raw))
        predictor = tuple(
            gaussian_filter(comp, PREDICTOR_SMOOTHING, mode="nearest")
            for comp in validated
        )
        raw, warped = deformation_pass(frame1, frame2, predictor)
        passes.append(raw)
    flagged = normalized_median_test(*raw)
    final = replace_outliers(*raw, flagged)
    return {
        "passes": passes,
        "raw": raw,
        "flagged": flagged,
        "final": final,
        "warped": warped,
        "predictor_at": lambda r, c: (predictor[0][r, c], predictor[1][r, c]),
    }


def vortex_centre(size=IMAGE_SIZE):
    """Vortex centre at the middle of the image [px]."""
    return ((size - 1) / 2, (size - 1) / 2)


def make_case(seed=SEED):
    """Image pair, true displacement at window centres, decorrelated windows."""
    rng = np.random.default_rng(seed)

    def displacement(x, y):
        return lamb_oseen_displacement(
            x, y, vortex_centre(), CORE_RADIUS, MAX_DISPLACEMENT
        )

    frame1, frame2 = make_image_pair(displacement, rng)
    starts = window_starts()
    # Interior windows two or more grid points apart, so no two are neighbours.
    candidates = [
        (r, c)
        for r in range(2, starts.size - 2, 3)
        for c in range(3, starts.size - 2, 6)
    ]
    chosen = rng.choice(len(candidates), N_DECORRELATED, replace=False)
    bad_nodes = [candidates[k] for k in sorted(chosen)]
    frame2 = decorrelate_windows(
        frame2, [(starts[c], starts[r]) for r, c in bad_nodes], rng
    )
    gx, gy = np.meshgrid(window_centres(), window_centres())
    true = displacement(gx, gy)
    return frame1, frame2, true, bad_nodes, (gx, gy)


def make_figure(frame1, frame2, true, result, grid, bad_nodes):
    gx, gy = grid
    fig, axs = plt.subplots(2, 3, figsize=(14, 9.5), layout="constrained")
    starts = window_starts()
    # Window used for panels (a)-(c): inside the vortex core, where gradients are large.
    r0, c0 = 8, 11
    y0, x0 = starts[r0], starts[c0]
    t_dx, t_dy = true[0][r0, c0], true[1][r0, c0]

    ax = axs[0, 0]
    pad = 16
    sl = (slice(y0 - pad, y0 + WINDOW + pad), slice(x0 - pad, x0 + WINDOW + pad))
    a = np.clip(frame1[sl] / 0.9, 0, 1)
    b = np.clip(frame2[sl] / 0.9, 0, 1)
    ext = (
        x0 - pad - 0.5,
        x0 + WINDOW + pad - 0.5,
        y0 - pad - 0.5,
        y0 + WINDOW + pad - 0.5,
    )
    ax.imshow(np.dstack([a, b, a]), origin="lower", extent=ext, interpolation="nearest")
    ax.add_patch(
        Rectangle(
            (x0 - 0.5, y0 - 0.5),
            WINDOW,
            WINDOW,
            fill=False,
            ec="white",
            lw=1.5,
            ls="--",
        )
    )
    ax.set_title("(a) Frame 1 (magenta) and frame 2 (green)")
    ax.set_xlabel("x [px]")
    ax.set_ylabel("y [px]")

    half = WINDOW // 2
    extent = (-half - 0.5, half - 0.5, -half - 0.5, half - 0.5)
    maps = [
        ("(b) Pass 1 correlation", frame1, frame2, (0.0, 0.0)),
        (
            "(c) Last pass, deformed windows",
            *result["warped"],
            result["predictor_at"](r0, c0),
        ),
    ]
    for ax, (title, im1, im2, offset) in zip(axs[0, 1:], maps):
        corr = cross_correlation(
            im1[y0 : y0 + WINDOW, x0 : x0 + WINDOW],
            im2[y0 : y0 + WINDOW, x0 : x0 + WINDOW],
        )
        im = ax.imshow(
            corr, origin="lower", cmap="viridis", extent=extent, vmin=-0.2, vmax=1
        )
        sx, sy = correlation_peak(corr)
        ax.plot(sx, sy, "+", color="white", ms=16, mew=2, label="sub-pixel peak")
        ax.plot(
            t_dx - offset[0],
            t_dy - offset[1],
            "x",
            color="tab:red",
            ms=10,
            mew=2,
            label="true (minus predictor)",
        )
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_title(f"{title}\npeak R = {corr.max():.2f}")
        ax.set_xlabel("$s_x$ [px]")
        ax.set_ylabel("$s_y$ [px]")
        ax.legend(loc="lower left", fontsize=10)
    fig.colorbar(im, ax=axs[0, 1:], label="normalized correlation $R$", shrink=0.9)

    ax = axs[1, 0]
    raw_dx, raw_dy = result["raw"]
    flagged = result["flagged"]
    kw = dict(angles="xy", scale_units="xy", scale=1 / 3.0, width=0.004)
    ax.quiver(gx, gy, *true, color="0.65", label="true", **kw)
    ok = ~flagged
    ax.quiver(
        gx[ok],
        gy[ok],
        raw_dx[ok],
        raw_dy[ok],
        color="tab:blue",
        label="PIV, last pass",
        **kw,
    )
    ax.quiver(
        gx[flagged],
        gy[flagged],
        raw_dx[flagged],
        raw_dy[flagged],
        color="tab:red",
        label="flagged by median test",
        **kw,
    )
    for r, c in bad_nodes:
        ax.plot(gx[r, c], gy[r, c], "s", mfc="none", mec="tab:orange", ms=13, mew=1.5)
    ax.plot(
        [], [], "s", mfc="none", mec="tab:orange", ms=10, label="decorrelated window"
    )
    ax.set_xlim(0, IMAGE_SIZE)
    ax.set_ylim(0, IMAGE_SIZE)
    ax.set_aspect("equal")
    ax.set_title("(d) Displacement (arrows x3)")
    ax.set_xlabel("x [px]")
    ax.set_ylabel("y [px]")
    ax.legend(
        loc="upper left",
        fontsize=9,
        framealpha=0.9,
        bbox_to_anchor=(0.0, -0.13),
        ncol=2,
    )

    ax = axs[1, 1]
    passes = np.arange(1, len(result["passes"]) + 1)
    med = [median_error(p, true) for p in result["passes"]]
    ok_rms = [rms_error(p, true, ~normalized_median_test(*p)) for p in result["passes"]]
    ax.semilogy(passes, med, "o-", color="tab:blue", label="median error, all vectors")
    ax.semilogy(
        passes, ok_rms, "s--", color="tab:green", label="RMS error, unflagged vectors"
    )
    ax.set_xticks(passes)
    ax.set_xlabel("pass (1 = plain correlation, then window deformation)")
    ax.set_ylabel("error [px]")
    ax.set_title("(e) Convergence of multi-pass interrogation")
    ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3)

    ax = axs[1, 2]
    err_raw = vector_error(result["raw"], true).ravel()
    err_fin = vector_error(result["final"], true).ravel()
    bins = np.logspace(-3, 1.5, 37)
    ax.hist(err_raw, bins=bins, color="tab:red", alpha=0.5, label="last pass, raw")
    ax.hist(
        err_fin,
        bins=bins,
        histtype="step",
        color="tab:blue",
        lw=2,
        label="after median test\nand replacement",
    )
    ax.set_xscale("log")
    ax.set_xlabel(r"vector error $|\mathbf{s} - \mathbf{s}_{true}|$ [px]")
    ax.set_ylabel("number of vectors")
    ax.set_title("(f) Error distribution")
    ax.legend(loc="upper left", fontsize=10)
    return fig


def vector_error(field, true):
    """Magnitude of the vector error at every node [px]."""
    return np.hypot(field[0] - true[0], field[1] - true[1])


def median_error(field, true):
    """Median vector error [px]; insensitive to the spurious vectors."""
    return float(np.median(vector_error(field, true)))


def rms_error(field, true, mask=None):
    """Root-mean-square vector error [px], optionally over a boolean mask."""
    sq = vector_error(field, true) ** 2
    return float(np.sqrt(np.mean(sq if mask is None else sq[mask])))


def summarize(true, result):
    """Print the error of each pass and the outlier count."""
    flagged = result["flagged"]
    print(f"vectors: {flagged.size}, flagged in last pass: {flagged.sum()}")
    for k, field in enumerate(result["passes"], start=1):
        print(
            f"pass {k}: median error {median_error(field, true):.3f} px, "
            f"RMS error {rms_error(field, true):.3f} px"
        )
    unflagged = rms_error(result["raw"], true, ~flagged)
    print(f"last pass RMS error over unflagged vectors: {unflagged:.3f} px")
    print(
        f"final RMS error after replacement: {rms_error(result['final'], true):.3f} px"
    )


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    frame1, frame2, true, bad_nodes, grid = make_case()
    result = run_piv(frame1, frame2)
    summarize(true, result)
    fig = make_figure(frame1, frame2, true, result, grid, bad_nodes)
    finish_figures(
        {"piv_cross_correlation.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
