"""Finite-difference weights from the Taylor (Vandermonde) system, their errors and modified wavenumbers.

For an arbitrary set of stencil offsets the weights of a derivative of any
order follow from matching Taylor series, which is a small Vandermonde system.
Fornberg's recursion gives the same weights more stably. The script checks the
order of each stencil on f(x) = exp(sin x), including the round-off floor at
small h, and compares the modified wavenumbers of explicit central, one-sided
and sixth-order compact (Lele 1992) schemes with the exact derivative.
"""

import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_circulant

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

X0 = 1.0  # evaluation point of the pointwise error study [-]
H_VALUES = np.logspace(0.0, -14.0, 57)  # grid spacings h of the pointwise study [-]
N_COMPACT = 2 ** np.arange(3, 12)  # periodic grid sizes for the compact scheme
MACHINE_EPS = np.finfo(float).eps

# First-derivative stencils (offsets in units of h) shown in the figure.
STENCILS = {
    "forward, 1st order": (0, 1),
    "central, 2nd order": (-1, 0, 1),
    "central, 4th order": (-2, -1, 0, 1, 2),
    "central, 6th order": (-3, -2, -1, 0, 1, 2, 3),
}
ONE_SIDED = {
    "backward, 1st order": (-1, 0),
    "backward, 2nd order": (-2, -1, 0),
    "upwind-biased, 3rd order": (-2, -1, 0, 1),
}

# Sixth-order tridiagonal compact scheme of Lele (1992), eq. (2.1.7):
# alpha f'_{i-1} + f'_i + alpha f'_{i+1}
#     = a (f_{i+1} - f_{i-1}) / (2h) + b (f_{i+2} - f_{i-2}) / (4h)
COMPACT_ALPHA, COMPACT_A, COMPACT_B = 1.0 / 3.0, 14.0 / 9.0, 1.0 / 9.0

PHASE_TOLERANCES = (
    0.01,
    0.001,
)  # relative phase-speed errors for points per wavelength


def fd_weights(offsets, derivative):
    """Weights w with f^(m)(x) ~ h^-m sum_j w_j f(x + s_j h) from the Taylor system.

    Row k of the Vandermonde system is sum_j w_j s_j^k / k! = delta_{km}, for
    k = 0..n-1 with n the number of offsets.
    """
    s = np.asarray(offsets, dtype=float)
    n = s.size
    if derivative >= n:
        raise ValueError("need more offsets than the derivative order")
    k = np.arange(n)
    a = s[None, :] ** k[:, None] / np.array([factorial(int(j)) for j in k])[:, None]
    rhs = np.zeros(n)
    rhs[derivative] = 1.0
    return np.linalg.solve(a, rhs)


def fornberg_weights(z, x, max_derivative):
    """Fornberg's (1988) recursion: weights for derivatives 0..m at z on nodes x.

    Returns an array c of shape (len(x), m + 1); column m holds the weights of
    the m-th derivative for physical (not scaled) node positions.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    c = np.zeros((n, max_derivative + 1))
    c1 = 1.0
    c4 = x[0] - z
    c[0, 0] = 1.0
    for i in range(1, n):
        mn = min(i, max_derivative)
        c2 = 1.0
        c5 = c4
        c4 = x[i] - z
        for j in range(i):
            c3 = x[i] - x[j]
            c2 *= c3
            if j == i - 1:
                for k in range(mn, 0, -1):
                    c[i, k] = c1 * (k * c[i - 1, k - 1] - c5 * c[i - 1, k]) / c2
                c[i, 0] = -c1 * c5 * c[i - 1, 0] / c2
            for k in range(mn, 0, -1):
                c[j, k] = (c4 * c[j, k] - k * c[j, k - 1]) / c3
            c[j, 0] = c4 * c[j, 0] / c3
        c1 = c2
    return c


def truncation_error(offsets, weights, derivative, max_terms=12):
    """Order p and leading coefficient C of the error C h^p f^(m+p).

    The moments sum_j w_j s_j^q / q! vanish for q < n except q = m; the first
    non-zero moment beyond m gives the leading error term.
    """
    s = np.asarray(offsets, dtype=float)
    for q in range(derivative + 1, derivative + 1 + max_terms):
        moment = np.sum(weights * s**q) / factorial(q)
        if abs(moment) > 1e-10:
            return q - derivative, moment
    raise ValueError("no non-zero error term found")


def as_fraction(value, max_denominator=10000):
    """Rational form of a weight for printing."""
    return Fraction(value).limit_denominator(max_denominator)


def apply_stencil(f, x0, h, offsets, derivative=1):
    """Pointwise finite-difference derivative of a callable f at x0."""
    w = fd_weights(offsets, derivative)
    values = np.array([f(x0 + s * h) for s in offsets])
    return np.dot(w, values) / h**derivative


def periodic_derivative(u, h, offsets):
    """First derivative of periodic samples u with an explicit stencil."""
    w = fd_weights(offsets, 1)
    return sum(wj * np.roll(u, -s) for wj, s in zip(w, offsets)) / h


def compact_derivative(u, h, alpha=COMPACT_ALPHA, a=COMPACT_A, b=COMPACT_B):
    """Sixth-order compact first derivative on a periodic grid.

    Builds the right-hand side from the explicit part and solves the cyclic
    tridiagonal system with a circulant solver.
    """
    n = u.size
    rhs = a * (np.roll(u, -1) - np.roll(u, 1)) / (2 * h) + b * (
        np.roll(u, -2) - np.roll(u, 2)
    ) / (4 * h)
    column = np.zeros(n)
    column[0] = 1.0
    column[1] = alpha
    column[-1] = alpha
    return solve_circulant(column, rhs)


def modified_wavenumber(offsets, theta):
    """k_eff h of an explicit first-derivative stencil for theta = k h.

    Applying the stencil to exp(i k x) gives i k_eff exp(i k x), so
    k_eff h = -i sum_j w_j exp(i s_j theta).
    """
    w = fd_weights(offsets, 1)
    phase = np.exp(1j * np.outer(theta, offsets))
    return -1j * phase @ w


def compact_modified_wavenumber(theta, alpha=COMPACT_ALPHA, a=COMPACT_A, b=COMPACT_B):
    """k_eff h of the tridiagonal compact scheme (real: the scheme is central)."""
    return (a * np.sin(theta) + 0.5 * b * np.sin(2 * theta)) / (
        1.0 + 2.0 * alpha * np.cos(theta)
    )


def points_per_wavelength(keff_function, tolerance, n_theta=200001):
    """Smallest points per wavelength 2 pi / theta with |Re k_eff / k - 1| < tolerance."""
    theta = np.linspace(1e-6, np.pi, n_theta)
    error = np.abs(np.real(keff_function(theta)) / theta - 1.0)
    bad = np.nonzero(error > tolerance)[0]
    theta_max = theta[bad[0] - 1] if bad.size else np.pi
    return 2 * np.pi / theta_max


def test_function(x):
    return np.exp(np.sin(x))


def test_derivative(x):
    return np.cos(x) * np.exp(np.sin(x))


def pointwise_errors(h_values=H_VALUES, x0=X0):
    """Absolute error of each stencil at x0 for every h."""
    exact = test_derivative(x0)
    return {
        name: np.array(
            [
                abs(apply_stencil(test_function, x0, h, offsets) - exact)
                for h in h_values
            ]
        )
        for name, offsets in STENCILS.items()
    }


def compact_errors(n_values=N_COMPACT):
    """Maximum error of the compact scheme on periodic grids of n points."""
    h = 2 * np.pi / n_values
    errors = []
    for n in n_values:
        x = 2 * np.pi * np.arange(n) / n
        du = compact_derivative(test_function(x), 2 * np.pi / n)
        errors.append(np.max(np.abs(du - test_derivative(x))))
    return h, np.array(errors)


def observed_orders(h, err):
    """Local slopes log(e_k / e_k+1) / log(h_k / h_k+1)."""
    return np.log(err[:-1] / err[1:]) / np.log(h[:-1] / h[1:])


def make_figure(errors, compact):
    colors = plt.cm.tab10.colors
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))

    ax = axes[0]
    for (name, err), color in zip(errors.items(), colors):
        ax.loglog(H_VALUES, err, "o-", color=color, markersize=3.5, label=name)
    h_c, e_c = compact
    ax.loglog(
        h_c,
        e_c,
        "s--",
        color=colors[4],
        markersize=5,
        label="compact, 6th order (periodic grid)",
    )
    ax.loglog(
        H_VALUES,
        MACHINE_EPS * test_function(X0) / H_VALUES,
        ":",
        color="0.4",
        label=r"round-off model $\epsilon_{\mathrm{mach}}|f|/h$",
    )
    for text, xy, color in (
        ("slope 1", (1.5e-6, 2e-4), colors[0]),
        ("slope 2", (1.5e-5, 2e-6), colors[1]),
        ("slope 4", (2.5e-5, 1.2e-10), colors[2]),
        ("slope 6", (0.12, 1e-10), colors[3]),
    ):
        ax.text(*xy, text, fontsize=10, color=color, fontweight="bold")
    ax.set_ylim(1e-17, 10)
    ax.set_xlabel("Grid spacing $h$ [-]", fontsize=11)
    ax.set_ylabel(r"Error in $f'(1)$, $f = e^{\sin x}$ [-]", fontsize=11)
    ax.set_title("(a) Truncation error falls, round-off rises", fontsize=12)
    ax.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=8.5, loc="lower left")

    theta = np.linspace(0.0, np.pi, 400)
    ax = axes[1]
    ax.plot(theta, theta, "k-", linewidth=2, label="exact")
    for (name, offsets), color in zip(STENCILS.items(), colors):
        if name.startswith("forward"):
            continue
        ax.plot(
            theta, modified_wavenumber(offsets, theta).real, color=color, label=name
        )
    ax.plot(
        theta,
        compact_modified_wavenumber(theta),
        "--",
        color=colors[4],
        label="compact, 6th order",
    )
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, np.pi)
    ax.set_xlabel(r"Wavenumber $k\Delta x$ [-]", fontsize=11)
    ax.set_ylabel(r"Re $k_{\mathrm{eff}}\Delta x$ [-]", fontsize=11)
    ax.set_title("(b) Dispersion of central schemes", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="upper left")

    ax = axes[2]
    for (name, offsets), color in zip(
        ONE_SIDED.items(), (colors[5], colors[6], colors[9])
    ):
        keff = modified_wavenumber(offsets, theta)
        ax.plot(theta, keff.real, color=color, label=f"{name}, Re")
        ax.plot(theta, keff.imag, "--", color=color, label=f"{name}, Im")
    ax.plot(theta, theta, "k-", linewidth=2, label="exact (Im = 0)")
    ax.axhline(0.0, color="0.5", linewidth=0.8)
    ax.set_xlim(0, np.pi)
    ax.set_xlabel(r"Wavenumber $k\Delta x$ [-]", fontsize=11)
    ax.set_ylabel(r"$k_{\mathrm{eff}}\Delta x$ [-]", fontsize=11)
    ax.set_title("(c) One-sided schemes: Im < 0 damps for $c > 0$", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=8.5, loc="lower left")
    fig.tight_layout()
    return fig


def report():
    print("First-derivative weights (offsets in units of h):")
    for name, offsets in {**STENCILS, **ONE_SIDED}.items():
        w = fd_weights(offsets, 1)
        p, c = truncation_error(offsets, w, 1)
        weights = ", ".join(str(as_fraction(v)) for v in w)
        print(
            f"  {name:26s} offsets {offsets}: [{weights}], "
            f"error {as_fraction(c)} h^{p} f^({p + 1})"
        )
    for offsets in ((-1, 0, 1), (-2, -1, 0, 1, 2), (0, 1, 2, 3)):
        w = fd_weights(offsets, 2)
        p, c = truncation_error(offsets, w, 2)
        weights = ", ".join(str(as_fraction(v)) for v in w)
        print(
            f"  2nd derivative, offsets {offsets}: [{weights}], "
            f"error {as_fraction(c)} h^{p} f^({p + 2})"
        )

    errors = pointwise_errors()
    print("Smallest pointwise error and the h where it occurs:")
    for name, err in errors.items():
        k = np.argmin(err)
        print(f"  {name:22s} min error {err[k]:.2e} at h = {H_VALUES[k]:.1e}")
    h_c, e_c = compact_errors()
    print("Compact scheme, max error on periodic grids:")
    for n, e in zip(N_COMPACT, e_c):
        print(f"  N = {n:5d}: {e:.3e}")
    print("  observed orders:", " ".join(f"{p:.2f}" for p in observed_orders(h_c, e_c)))

    print("Points per wavelength for a relative phase-speed error below tolerance:")
    schemes = {
        name: (lambda t, o=offsets: modified_wavenumber(o, t))
        for name, offsets in STENCILS.items()
        if not name.startswith("forward")
    }
    schemes["compact, 6th order"] = compact_modified_wavenumber
    for name, fn in schemes.items():
        ppw = [points_per_wavelength(fn, tol) for tol in PHASE_TOLERANCES]
        print(f"  {name:22s} 1%: {ppw[0]:5.1f}   0.1%: {ppw[1]:5.1f}")
    return errors, (h_c, e_c)


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    errors, compact = report()
    fig = make_figure(errors, compact)
    finish_figures(
        {"finite_difference_stencils.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
