"""Fourier and Chebyshev spectral differentiation compared with 2nd- and 4th-order finite differences.

On a smooth periodic function the FFT derivative converges exponentially in
the number of points N, while finite differences converge as N^-2 and N^-4.
Chebyshev collocation recovers exponential convergence for a smooth
non-periodic function. For |sin x|, whose derivative jumps, every method
converges at the same slow algebraic rate and the spectral derivative shows
Gibbs oscillations. The script also checks the 3/2 rule for de-aliasing a
quadratic product.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_SPECTRAL = np.arange(4, 66, 2)  # even grid sizes for the Fourier/Chebyshev study
N_FD = 2 ** np.arange(2, 14)  # grid sizes for finite differences, 4..8192
N_GIBBS = 32  # grid size of the Gibbs panel
N_ALIAS = 16  # grid size of the de-aliasing check
CHEB_WAVENUMBER = 4.0  # f(x) = exp(x) sin(4 x) on [-1, 1]


def grid(n):
    """n equispaced points on [0, 2 pi)."""
    return 2 * np.pi * np.arange(n) / n


def wavenumbers(n):
    """Integer wavenumbers in FFT order."""
    return np.fft.fftfreq(n, d=1.0 / n)


def fourier_derivative(u):
    """First derivative of periodic samples on [0, 2 pi) by FFT.

    Multiplies each coefficient by i k. For even n the Nyquist coefficient is
    set to zero, because its derivative is not represented on the grid.
    """
    n = u.size
    k = 1j * wavenumbers(n)
    if n % 2 == 0:
        k[n // 2] = 0.0
    return np.real(np.fft.ifft(k * np.fft.fft(u)))


def fourier_differentiation_matrix(n):
    """Dense periodic first-derivative matrix for even n (Trefethen 2000, ch. 3).

    D_ij = 0.5 (-1)^(i-j) cot((x_i - x_j) / 2) for i != j, D_ii = 0.
    """
    i = np.arange(n)
    diff = i[:, None] - i[None, :]
    with np.errstate(divide="ignore"):
        d = 0.5 * (-1.0) ** diff / np.tan(np.pi * diff / n)
    d[i, i] = 0.0
    return d


def fd_derivative(u, order):
    """Periodic central finite differences of order 2 or 4 on [0, 2 pi)."""
    h = 2 * np.pi / u.size
    up1, um1 = np.roll(u, -1), np.roll(u, 1)
    if order == 2:
        return (up1 - um1) / (2 * h)
    if order == 4:
        up2, um2 = np.roll(u, -2), np.roll(u, 2)
        return (-up2 + 8 * up1 - 8 * um1 + um2) / (12 * h)
    raise ValueError("order must be 2 or 4")


def chebyshev(n):
    """Chebyshev points x_j = cos(pi j / n) and differentiation matrix (n + 1 points).

    Follows cheb.m of Trefethen (2000): off-diagonal entries from the
    Lagrange interpolant, diagonal entries from the negative row sums.
    """
    if n == 0:
        return np.zeros((1, 1)), np.array([1.0])
    x = np.cos(np.pi * np.arange(n + 1) / n)
    c = np.ones(n + 1)
    c[0] = c[-1] = 2.0
    c *= (-1.0) ** np.arange(n + 1)
    dx = x[:, None] - x[None, :]
    d = np.outer(c, 1.0 / c) / (dx + np.eye(n + 1))
    d -= np.diag(d.sum(axis=1))
    return d, x


def smooth(x):
    return np.exp(np.sin(x))


def smooth_derivative(x):
    return np.cos(x) * np.exp(np.sin(x))


def kink(x):
    return np.abs(np.sin(x))


def kink_derivative(x):
    return np.sign(np.sin(x)) * np.cos(x)


def cheb_function(x, k=CHEB_WAVENUMBER):
    return np.exp(x) * np.sin(k * x)


def cheb_function_derivative(x, k=CHEB_WAVENUMBER):
    return np.exp(x) * (np.sin(k * x) + k * np.cos(k * x))


def max_error(method, f, df, n):
    x = grid(n)
    return np.max(np.abs(method(f(x)) - df(x)))


def rms_error(method, f, df, n):
    x = grid(n)
    return np.sqrt(np.mean((method(f(x)) - df(x)) ** 2))


def chebyshev_error(n):
    d, x = chebyshev(n)
    return np.max(np.abs(d @ cheb_function(x) - cheb_function_derivative(x)))


def methods():
    return {
        "Fourier spectral": fourier_derivative,
        "central FD, 2nd order": lambda u: fd_derivative(u, 2),
        "central FD, 4th order": lambda u: fd_derivative(u, 4),
    }


def smooth_study():
    out = {}
    for name, method in methods().items():
        n = N_SPECTRAL if name.startswith("Fourier") else N_FD
        out[name] = (
            n,
            np.array([max_error(method, smooth, smooth_derivative, m) for m in n]),
        )
    out["Chebyshev, non-periodic"] = (
        N_SPECTRAL,
        np.array([chebyshev_error(m) for m in N_SPECTRAL]),
    )
    return out


def kink_study():
    """RMS error of the derivative of |sin x|. Odd n keeps grid points off the kinks."""
    n_values = 2 ** np.arange(3, 14) + 1
    return {
        name: (
            n_values,
            np.array([rms_error(m, kink, kink_derivative, n) for n in n_values]),
        )
        for name, m in methods().items()
    }


def pad_product(u_hat, v_hat):
    """Coefficients of u v truncated to n modes, computed on a 3/2 padded grid.

    u_hat, v_hat are numpy FFT coefficients (length n, even). The Nyquist
    mode is assumed zero. Returns length-n FFT coefficients of the product.
    """
    n = u_hat.size
    m = 3 * n // 2
    half = n // 2

    def pad(a):
        b = np.zeros(m, dtype=complex)
        b[:half] = a[:half]
        b[m - half + 1 :] = a[half + 1 :]
        return b * (m / n)

    w_hat = np.fft.fft(np.fft.ifft(pad(u_hat)) * np.fft.ifft(pad(v_hat)))
    out = np.zeros(n, dtype=complex)
    out[:half] = w_hat[:half]
    out[half + 1 :] = w_hat[m - half + 1 :]
    return out * (n / m)


def aliasing_check(n=N_ALIAS):
    """Product of cos(5x) and cos(6x) on n = 16 points.

    The exact product is (cos x + cos 11x) / 2. Wavenumber 11 exceeds the
    Nyquist limit 8 and aliases to 11 - 16 = -5 on the plain grid; with 3/2
    padding the unresolved mode is discarded and only cos x remains.
    Returns the coefficient magnitudes at k = 1 and k = 5 for both products.
    """
    x = grid(n)
    u, v = np.cos(5 * x), np.cos(6 * x)
    plain = np.fft.fft(u * v) / n
    padded = pad_product(np.fft.fft(u), np.fft.fft(v)) / n
    return {
        "plain": (abs(plain[1]), abs(plain[5])),
        "3/2 padded": (abs(padded[1]), abs(padded[5])),
    }


def slopes(n, err):
    return np.log(err[:-1] / err[1:]) / np.log(n[1:] / n[:-1])


def make_figure(smooth_res, kink_res):
    colors = plt.cm.tab10.colors
    styles = {
        "Fourier spectral": ("o-", colors[0]),
        "central FD, 2nd order": ("s-", colors[1]),
        "central FD, 4th order": ("^-", colors[2]),
        "Chebyshev, non-periodic": ("D--", colors[3]),
    }
    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5))
    floor = 1e-16

    for ax, log_x in ((axes[0, 0], True), (axes[0, 1], False)):
        for name, (n, err) in smooth_res.items():
            style, color = styles[name]
            keep = n <= 64 if not log_x else np.ones_like(n, dtype=bool)
            ax.plot(
                n[keep],
                np.maximum(err[keep], floor),
                style,
                color=color,
                markersize=4,
                label=name,
            )
        ax.set_yscale("log")
        ax.set_ylim(1e-16, 10)
        ax.set_ylabel("Max error of $f'$ [-]", fontsize=11)
        ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.6)
    ax = axes[0, 0]
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Number of grid points $N$ [-]", fontsize=11)
    ax.set_title(r"(a) $f = e^{\sin x}$: algebraic vs spectral (log-log)", fontsize=12)
    ax.text(600, 3e-5, "slope $-2$", color=colors[1], fontsize=10)
    ax.text(300, 1e-10, "slope $-4$", color=colors[2], fontsize=10)
    ax.legend(fontsize=9, loc="upper right")
    ax = axes[0, 1]
    ax.set_xlim(0, 66)
    ax.set_xlabel("Number of grid points $N$ [-]", fontsize=11)
    ax.set_title(
        "(b) Same data, linear $N$: spectral error falls exponentially", fontsize=12
    )
    ax.legend(fontsize=9, loc="center right")

    ax = axes[1, 0]
    for name, (n, err) in kink_res.items():
        style, color = styles[name]
        p = slopes(n, err)[-1]
        ax.loglog(
            n, err, style, color=color, markersize=4, label=f"{name} (slope {-p:.2f})"
        )
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Number of grid points $N$ [-]", fontsize=11)
    ax.set_ylabel("RMS error of $f'$ [-]", fontsize=11)
    ax.set_title(r"(c) $f = |\sin x|$: every method is slow", fontsize=12)
    ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")

    ax = axes[1, 1]
    x_fine = np.linspace(0, 2 * np.pi, 1000)
    ax.plot(x_fine, kink_derivative(x_fine), "k-", linewidth=2, label="exact $f'$")
    x = grid(N_GIBBS)
    ax.plot(
        x,
        fourier_derivative(kink(x)),
        "o-",
        color=colors[0],
        markersize=4,
        label=f"Fourier spectral, N = {N_GIBBS}",
    )
    ax.plot(
        x,
        fd_derivative(kink(x), 2),
        "s--",
        color=colors[1],
        markersize=4,
        label=f"central FD 2nd order, N = {N_GIBBS}",
    )
    ax.set_xlim(0, 2 * np.pi)
    ax.set_xlabel("$x$ [-]", fontsize=11)
    ax.set_ylabel(r"$d|\sin x|/dx$ [-]", fontsize=11)
    ax.set_title("(d) Gibbs oscillations at the jumps of $f'$", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower left")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    smooth_res = smooth_study()
    print("Smooth periodic f = exp(sin x), max error of f':")
    for name, (n, err) in smooth_res.items():
        picks = [k for k, m in enumerate(n) if m in (8, 16, 32, 64, 1024, 8192)]
        text = ", ".join(f"N={n[k]}: {err[k]:.2e}" for k in picks)
        print(f"  {name:24s} {text}")
    for name in ("central FD, 2nd order", "central FD, 4th order"):
        n, err = smooth_res[name]
        print(
            f"  {name} observed orders: " + " ".join(f"{p:.2f}" for p in slopes(n, err))
        )
    d = fourier_differentiation_matrix(16)
    x = grid(16)
    print(
        "  differentiation matrix vs FFT, N = 16: "
        f"{np.max(np.abs(d @ smooth(x) - fourier_derivative(smooth(x)))):.1e}"
    )

    kink_res = kink_study()
    print("f = |sin x|, RMS error of f':")
    for name, (n, err) in kink_res.items():
        print(
            f"  {name:24s} N={n[-1]}: {err[-1]:.2e}, convergence rate {slopes(n, err)[-1]:.2f}"
        )

    for label, (a1, a5) in aliasing_check().items():
        print(
            f"cos5x*cos6x on N={N_ALIAS}, {label}: |c_1| = {a1:.3f}, |c_5| = {a5:.3f}"
        )

    fig = make_figure(smooth_res, kink_res)
    finish_figures(
        {"spectral_vs_finite_difference.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
