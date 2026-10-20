"""Learn the solution operator of a periodic 1D PDE with one spectral convolution.

The operator G: f -> u of -nu u'' + u = f on the periodic unit interval is
diagonal in Fourier space, u_k = f_k / (1 + nu (2 pi k)^2). The script draws
random forcings on a 64-point grid, computes noisy solutions, and fits the
complex weight R_k of every retained Fourier mode |k| <= K by least squares.
This is the linear spectral part of a Fourier neural operator layer. The
learned layer is then applied to an unseen forcing on grids up to 2048 points
without retraining, which shows that its error does not depend on resolution.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

NU = 0.01  # diffusion coefficient, [length^2] on a domain of length 1
N_TRAIN_GRID = 64  # grid points of the training data
N_TRAIN_SAMPLES = 200  # (forcing, solution) pairs in the training set
K_TRAIN_MAX = N_TRAIN_GRID // 2 - 1  # highest mode present in the training forcings
K_TEST_MAX = 48  # highest mode of the unseen test forcing (above training Nyquist)
SPECTRUM_K0 = 8.0  # forcing spectrum |f_k| ~ (1 + (k / k0)^2)^(-1)
NOISE_LEVEL = 1e-3  # std of the noise added to u, relative to std(u)
K_DEFAULT = 16  # retained modes in the main example
K_VALUES = (4, 8, 16, 31)  # truncation levels compared in the error panel
EVAL_GRIDS = (128, 256, 512, 1024, 2048)  # zero-shot evaluation resolutions
SEED = 0


def exact_multiplier(k, nu=NU):
    """Fourier symbol of the solution operator, 1 / (1 + nu (2 pi k)^2)."""
    return 1.0 / (1.0 + nu * (2.0 * np.pi * k) ** 2)


def random_coefficients(rng, n_samples, k_max, k0=SPECTRUM_K0):
    """Complex Fourier coefficients c_k, k = 0..k_max, of real random forcings."""
    k = np.arange(k_max + 1)
    amplitude = 1.0 / (1.0 + (k / k0) ** 2)
    shape = (n_samples, k_max + 1)
    coef = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * amplitude
    coef[:, 0] = coef[:, 0].real
    return coef


def synthesize(coef, n):
    """Sample f(x) = Re(c_0) + 2 sum_{k>=1} Re(c_k exp(2 pi i k x)) on n points.

    The function is defined independently of the grid, so the same forcing can
    be sampled at any resolution n > 2 k_max without aliasing.
    """
    k_max = coef.shape[-1] - 1
    if n <= 2 * k_max:
        raise ValueError(f"grid of {n} points cannot resolve mode {k_max}")
    spectrum = np.zeros(coef.shape[:-1] + (n // 2 + 1,), dtype=complex)
    spectrum[..., : k_max + 1] = coef * n
    spectrum[..., 0] = coef[..., 0].real * n
    return np.fft.irfft(spectrum, n=n, axis=-1)


def solve_exact(coef, nu=NU):
    """Fourier coefficients of the exact solution u for forcing coefficients coef."""
    return coef * exact_multiplier(np.arange(coef.shape[-1]), nu)


def fit_spectral_weights(f, u, n_modes):
    """Least-squares weights R_k minimising sum_i |u_ik - R_k f_ik|^2, k <= K.

    The objective decouples over modes, so each weight has the closed form
    R_k = sum_i conj(f_ik) u_ik / sum_i |f_ik|^2.
    """
    f_hat = np.fft.rfft(f, axis=-1)[:, : n_modes + 1]
    u_hat = np.fft.rfft(u, axis=-1)[:, : n_modes + 1]
    return (np.conj(f_hat) * u_hat).sum(axis=0) / (np.abs(f_hat) ** 2).sum(axis=0)


def spectral_convolution(weights, f):
    """Apply u = IFFT(R_k FFT(f)) for k <= K and zero for higher modes.

    The weights do not depend on the grid size, so the same layer runs at any
    resolution with at least 2K + 1 points.
    """
    n = f.shape[-1]
    n_modes = weights.size - 1
    f_hat = np.fft.rfft(f, axis=-1)
    u_hat = np.zeros_like(f_hat)
    u_hat[..., : n_modes + 1] = f_hat[..., : n_modes + 1] * weights
    return np.fft.irfft(u_hat, n=n, axis=-1)


def relative_l2(prediction, reference):
    return np.linalg.norm(prediction - reference) / np.linalg.norm(reference)


def make_training_set(rng):
    coef = random_coefficients(rng, N_TRAIN_SAMPLES, K_TRAIN_MAX)
    f = synthesize(coef, N_TRAIN_GRID)
    u = synthesize(solve_exact(coef), N_TRAIN_GRID)
    u = u + NOISE_LEVEL * np.std(u) * rng.normal(size=u.shape)
    return f, u


def zero_shot_errors(weights, test_coef):
    """Relative L2 error of the learned layer on each grid in EVAL_GRIDS."""
    errors = []
    for n in EVAL_GRIDS:
        f = synthesize(test_coef, n)
        u = synthesize(solve_exact(test_coef), n)
        errors.append(relative_l2(spectral_convolution(weights, f), u))
    return np.array(errors)


def plot_results(f_train, u_train, test_coef):
    weights = fit_spectral_weights(f_train, u_train, K_DEFAULT)
    k = np.arange(K_DEFAULT + 1)
    k_dense = np.linspace(0, K_TEST_MAX, 400)

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    ax = axs[0, 0]
    ax.semilogy(k_dense, exact_multiplier(k_dense), "k-", label="exact symbol")
    ax.semilogy(k, weights.real, "o", color="tab:blue", label=r"learned Re $R_k$")
    ax.semilogy(
        k, np.abs(weights.imag) + 1e-12, "x", color="tab:orange", label=r"|Im $R_k$|"
    )
    ax.axvline(K_DEFAULT, color="0.5", ls=":", label=f"truncation $K = {K_DEFAULT}$")
    ax.set_title("Fourier multiplier of the solution operator")
    ax.set_xlabel("wavenumber $k$")
    ax.set_ylabel("multiplier")
    ax.set_ylim(1e-6, 2)
    ax.legend(fontsize=10, loc="upper right")

    n_fine = EVAL_GRIDS[-1]
    n_coarse = EVAL_GRIDS[0]
    x_fine = np.arange(n_fine) / n_fine
    x_coarse = np.arange(n_coarse) / n_coarse
    f_fine = synthesize(test_coef, n_fine)[0]
    ax = axs[0, 1]
    ax.plot(x_fine, f_fine, color="tab:green")
    ax.set_title(f"Unseen forcing $f(x)$ (modes up to $k = {K_TEST_MAX}$)")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f$")

    ax = axs[1, 0]
    u_fine = synthesize(solve_exact(test_coef), n_fine)[0]
    pred_fine = spectral_convolution(weights, f_fine)
    pred_coarse = spectral_convolution(weights, synthesize(test_coef, n_coarse)[0])
    ax.plot(x_fine, u_fine, "k-", lw=2.5, label="exact $u$")
    ax.plot(x_fine, pred_fine, color="tab:blue", lw=1.2, label=f"learned, N = {n_fine}")
    ax.plot(
        x_coarse[::2],
        pred_coarse[::2],
        "o",
        ms=4,
        mfc="none",
        color="tab:orange",
        label=f"learned, N = {n_coarse}",
    )
    error = relative_l2(pred_fine, u_fine)
    ax.set_title(
        f"Prediction (trained on N = {N_TRAIN_GRID}), rel. L2 error {error:.1e}"
    )
    ax.set_xlabel("$x$")
    ax.set_ylabel("$u$")
    ax.legend(fontsize=10)

    ax = axs[1, 1]
    for n_modes, color in zip(K_VALUES, plt.get_cmap("tab10").colors):
        errors = zero_shot_errors(
            fit_spectral_weights(f_train, u_train, n_modes), test_coef
        )
        ax.loglog(EVAL_GRIDS, errors, "o-", color=color, label=f"$K = {n_modes}$")
    ax.set_xticks(EVAL_GRIDS, [str(n) for n in EVAL_GRIDS])
    ax.minorticks_off()
    ax.set_title(f"Zero-shot error vs grid size (trained on N = {N_TRAIN_GRID})")
    ax.set_xlabel("evaluation grid points $N$")
    ax.set_ylabel(r"relative $L^2$ error")
    ax.legend(fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    rng = np.random.default_rng(SEED)
    f_train, u_train = make_training_set(rng)
    test_coef = random_coefficients(rng, 1, K_TEST_MAX)

    for n_modes in K_VALUES:
        weights = fit_spectral_weights(f_train, u_train, n_modes)
        exact = exact_multiplier(np.arange(n_modes + 1))
        weight_error = np.max(np.abs(weights - exact) / exact)
        errors = zero_shot_errors(weights, test_coef)
        print(
            f"K = {n_modes:2d}: max relative weight error {weight_error:.1e}, "
            "zero-shot rel. L2 error on N = "
            + ", ".join(f"{n}: {e:.2e}" for n, e in zip(EVAL_GRIDS, errors))
        )

    fig = plot_results(f_train, u_train, test_coef)
    finish_figures(
        {"fourier_neural_operator_1d.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
