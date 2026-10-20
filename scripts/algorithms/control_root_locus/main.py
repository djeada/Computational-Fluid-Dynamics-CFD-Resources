"""Root locus of a third-order position servo, checked against the Routh-Hurwitz criterion.

The loop transfer function is K / (s (s + 2) (s + 5)), a DC motor with an
integrating shaft angle, a mechanical pole and an amplifier pole. The closed-loop
poles are the roots of D(s) + K N(s) = 0, computed with numpy.roots for a sweep
of K. The script computes the asymptote centroid and angles, the breakaway point
from dK/ds = 0, the gain where the locus meets the line of damping ratio 0.5,
and the gain where a branch crosses the imaginary axis. That crossing gain is
compared with the critical gain found from the first column of the Routh array.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Loop transfer function L(s) = K N(s) / D(s)
NUMERATOR = (1.0,)  # N(s) = 1
DENOMINATOR = tuple(np.poly([0.0, -2.0, -5.0]))  # D(s) = s (s + 2) (s + 5)
K_MIN, K_MAX, N_GAINS = 1e-3, 1e3, 4000  # gain sweep (logarithmic)
TARGET_ZETA = 0.5  # damping ratio for the design point marked on the locus
EPS = 1e-9  # replaces a zero pivot in the Routh array


def closed_loop_polynomial(k, num=NUMERATOR, den=DENOMINATOR):
    """Coefficients of D(s) + K N(s), highest power first."""
    den = np.asarray(den, dtype=float)
    num = np.asarray(num, dtype=float)
    padded = np.zeros_like(den)
    padded[len(den) - len(num) :] = num
    return den + k * padded


def closed_loop_poles(k, num=NUMERATOR, den=DENOMINATOR):
    """Roots of the closed-loop characteristic polynomial for gain k."""
    return np.roots(closed_loop_polynomial(k, num, den))


def root_locus(gains, num=NUMERATOR, den=DENOMINATOR):
    """Closed-loop poles for each gain, ordered so each column is one branch."""
    branches = np.empty((len(gains), len(den) - 1), dtype=complex)
    previous = np.roots(den)
    for i, k in enumerate(gains):
        roots = closed_loop_poles(k, num, den)
        ordered = np.empty_like(roots)
        free = list(range(len(roots)))
        for j, p in enumerate(previous):  # nearest-neighbour continuation
            best = min(free, key=lambda m: abs(roots[m] - p))
            ordered[j] = roots[best]
            free.remove(best)
        branches[i] = ordered
        previous = ordered
    return branches


def asymptotes(num=NUMERATOR, den=DENOMINATOR):
    """Centroid sigma_a and angles (degrees) of the n - m asymptotes."""
    poles = np.roots(den)
    zeros = np.roots(num) if len(num) > 1 else np.array([])
    excess = len(poles) - len(zeros)
    centroid = (poles.sum().real - zeros.sum().real) / excess
    angles = np.array([(2 * q + 1) * 180.0 / excess for q in range(excess)])
    return centroid, angles


def breakaway_points(num=NUMERATOR, den=DENOMINATOR):
    """Real points with dK/ds = 0 and K = -D/N > 0, as (s, K) pairs."""
    num = np.poly1d(num)
    den = np.poly1d(den)
    candidates = np.roots((num * den.deriv() - num.deriv() * den).coeffs)
    points = []
    for s in candidates:
        if abs(s.imag) < 1e-9:
            k = -den(s.real) / num(s.real)
            if k > 0:
                points.append((s.real, k))
    return points


def routh_array(coeffs, eps=EPS):
    """Routh array of a polynomial (highest power first) as a 2D numpy array.

    A zero pivot is replaced by eps; a row of zeros is replaced by the
    derivative of the auxiliary polynomial formed from the row above it.
    """
    coeffs = np.asarray(coeffs, dtype=float)
    n = len(coeffs) - 1
    width = n // 2 + 1
    table = np.zeros((n + 1, width))
    table[0, : len(coeffs[0::2])] = coeffs[0::2]
    table[1, : len(coeffs[1::2])] = coeffs[1::2]
    for i in range(2, n + 1):
        if np.allclose(table[i - 1], 0.0):
            order = n - (i - 2)  # power of s of the row above the zero row
            powers = order - 2 * np.arange(width)
            table[i - 1] = np.where(powers > 0, table[i - 2] * powers, 0.0)
        if abs(table[i - 1, 0]) < eps:
            table[i - 1, 0] = eps
        for j in range(width - 1):
            table[i, j] = (
                table[i - 1, 0] * table[i - 2, j + 1]
                - table[i - 2, 0] * table[i - 1, j + 1]
            ) / table[i - 1, 0]
    if np.allclose(table[n], 0.0):
        table[n, 0] = eps
    return table


def sign_changes(column):
    """Number of sign changes in the first column (= right-half-plane roots)."""
    signs = np.sign(column[np.abs(column) > 0])
    return int(np.sum(signs[1:] != signs[:-1]))


def routh_critical_gain(num=NUMERATOR, den=DENOMINATOR, k_hi=1e4, tol=1e-10):
    """Smallest K > 0 at which the Routh first column first changes sign."""

    def unstable(k):
        return sign_changes(routh_array(closed_loop_polynomial(k, num, den))[:, 0]) > 0

    k_lo = 1e-6
    if unstable(k_lo) or not unstable(k_hi):
        raise ValueError("no stability boundary in the bracket")
    while k_hi - k_lo > tol * k_hi:
        k_mid = 0.5 * (k_lo + k_hi)
        if unstable(k_mid):
            k_hi = k_mid
        else:
            k_lo = k_mid
    return 0.5 * (k_lo + k_hi)


def crossing_frequency(k, num=NUMERATOR, den=DENOMINATOR):
    """Frequency of the j-omega roots at the critical gain, from the auxiliary polynomial."""
    table = routh_array(closed_loop_polynomial(k, num, den))
    n = len(den) - 1
    # The s^1 row vanishes at the critical gain; the s^2 row above it gives
    # the auxiliary polynomial a s^2 + b = 0.
    a, b = table[n - 2, 0], table[n - 2, 1]
    return np.sqrt(b / a)


def locus_crossing_gain(num=NUMERATOR, den=DENOMINATOR, k_hi=1e4, tol=1e-10):
    """Gain at which the largest real part of the closed-loop poles reaches zero."""

    def max_real(k):
        return closed_loop_poles(k, num, den).real.max()

    k_lo = 1e-6
    while k_hi - k_lo > tol * k_hi:
        k_mid = 0.5 * (k_lo + k_hi)
        if max_real(k_mid) > 0:
            k_hi = k_mid
        else:
            k_lo = k_mid
    return 0.5 * (k_lo + k_hi)


def damping_line_gain(zeta, num=NUMERATOR, den=DENOMINATOR, k_lo=1e-3, k_hi=1e3):
    """Gain at which the complex branch reaches damping ratio zeta (bisection)."""

    def branch_zeta(k):
        p = closed_loop_poles(k, num, den)
        complex_poles = p[p.imag > 1e-9]
        if complex_poles.size == 0:
            return 1.0
        q = complex_poles[0]
        return -q.real / abs(q)

    for _ in range(200):
        k_mid = np.sqrt(k_lo * k_hi)
        if branch_zeta(k_mid) > zeta:
            k_lo = k_mid
        else:
            k_hi = k_mid
    return np.sqrt(k_lo * k_hi)


def make_figure(gains, branches, data):
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5.8))
    colors = plt.cm.tab10(np.arange(branches.shape[1]))
    for j in range(branches.shape[1]):
        ax.plot(
            branches[:, j].real,
            branches[:, j].imag,
            color=colors[j],
            lw=2,
            label=f"Branch {j + 1}",
        )
    poles = np.roots(DENOMINATOR)
    ax.plot(poles.real, poles.imag, "kx", ms=11, mew=2.5, label="Open-loop poles")

    centroid, angles = data["centroid"], data["angles"]
    for ang in angles:
        r = 9.0
        ax.plot(
            [centroid, centroid + r * np.cos(np.radians(ang))],
            [0, r * np.sin(np.radians(ang))],
            "k--",
            lw=1,
        )
    ax.plot(centroid, 0, "kD", ms=7, label=rf"Centroid $\sigma_a$ = {centroid:.3f}")

    s_b, k_b = data["breakaway"]
    ax.plot(s_b, 0, "o", color="k", mfc="w", ms=9, mew=2)
    ax.annotate(
        f"breakaway s = {s_b:.3f}\nK = {k_b:.3f}",
        xy=(s_b, 0),
        xytext=(-6.6, -2.4),
        fontsize=10,
        arrowprops={"arrowstyle": "->"},
    )
    w_u, k_u = data["omega_u"], data["k_routh"]
    ax.plot([0, 0], [w_u, -w_u], "ks", ms=8, mfc="gold")
    ax.annotate(
        f"Routh: $K_u$ = {k_u:.2f}\n$s = \\pm j${w_u:.3f} rad/s",
        xy=(0, w_u),
        xytext=(0.4, w_u + 1.3),
        fontsize=10,
        arrowprops={"arrowstyle": "->"},
    )
    k_z = data["k_zeta"]
    p_z = closed_loop_poles(k_z)
    pz = p_z[np.abs(p_z.imag) > 1e-9]
    ax.plot(pz.real, pz.imag, "o", color="k", ms=7)
    angle = np.arccos(TARGET_ZETA)
    ax.plot([0, -8 * np.cos(angle)], [0, 8 * np.sin(angle)], ":", color="0.4", lw=1.2)
    ax.annotate(
        rf"$\zeta$ = {TARGET_ZETA}: K = {k_z:.2f}",
        xy=(pz[pz.imag > 0][0].real, pz[pz.imag > 0][0].imag),
        xytext=(-4.6, 2.6),
        fontsize=10,
        arrowprops={"arrowstyle": "->"},
    )
    ax.axhline(0, color="k", lw=0.7)
    ax.axvline(0, color="k", lw=0.7)
    ax.set_xlim(-7, 2.5)
    ax.set_ylim(-6, 6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Real part $\sigma$ (1/s)", fontsize=11)
    ax.set_ylabel(r"Imaginary part $\omega$ (rad/s)", fontsize=11)
    ax.set_title(r"(a) Root locus of $K/[s(s+2)(s+5)]$", fontsize=12)
    ax.legend(fontsize=9, loc="lower left")
    ax.grid(alpha=0.3)

    max_real = branches.real.max(axis=1)
    bx.semilogx(gains, max_real, color="C0", lw=2, label="Largest Re(p) from the sweep")
    bx.axhline(0, color="k", lw=0.8)
    bx.axvline(
        k_u, color="C3", ls="--", lw=1.5, label=f"Routh critical gain $K_u$ = {k_u:.2f}"
    )
    bx.axvline(k_b, color="0.4", ls=":", lw=1.5, label=f"Breakaway gain K = {k_b:.3f}")
    bx.set_xlabel("Gain K", fontsize=11)
    bx.set_ylabel("Largest real part of closed-loop poles (1/s)", fontsize=11)
    bx.set_title("(b) Stability boundary: sweep against Routh", fontsize=12)
    bx.legend(fontsize=10, loc="upper left")
    bx.grid(alpha=0.3, which="both")
    bx.set_xlim(K_MIN, K_MAX)
    fig.tight_layout()
    return fig


def analyse():
    gains = np.concatenate(([0.0], np.geomspace(K_MIN, K_MAX, N_GAINS)))
    branches = root_locus(gains)
    centroid, angles = asymptotes()
    (breakaway,) = breakaway_points()
    k_routh = routh_critical_gain()
    data = {
        "centroid": centroid,
        "angles": angles,
        "breakaway": breakaway,
        "k_routh": k_routh,
        "k_locus": locus_crossing_gain(),
        "omega_u": crossing_frequency(k_routh),
        "k_zeta": damping_line_gain(TARGET_ZETA),
    }
    return gains, branches, data


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    gains, branches, data = analyse()
    print("L(s) = K / (s (s + 2) (s + 5))")
    print(f"Asymptote centroid = {data['centroid']:.4f}, angles = {data['angles']} deg")
    print(
        f"Breakaway point s = {data['breakaway'][0]:.4f} at K = {data['breakaway'][1]:.4f}"
    )
    print(f"Routh critical gain        K_u = {data['k_routh']:.6f}")
    print(f"Locus imaginary-axis gain  K   = {data['k_locus']:.6f}")
    print(f"Crossing frequency  w_u = {data['omega_u']:.6f} rad/s")
    k_z = data["k_zeta"]
    print(
        f"zeta = {TARGET_ZETA} at K = {k_z:.4f}, poles = {np.round(closed_loop_poles(k_z), 4)}"
    )
    print("Routh array at K = 35:")
    print(routh_array(closed_loop_polynomial(35.0)))

    fig = make_figure(gains, branches, data)
    finish_figures(
        {"control_root_locus.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
