"""Jacobi, Gauss-Seidel, SOR, conjugate gradients and multigrid on the 2D Poisson equation.

Solves -(u_xx + u_yy) = f on the unit square with u = 0 on the boundary,
discretised by the five-point stencil on an N x N grid of interior points.
Every method starts from u = 0 and stops when the relative residual
||f - A u|| / ||f|| drops below 1e-8. The figure shows the residual histories
on one grid, the number of iterations against N for every method, and how
weighted Jacobi smooths the error, which is the property multigrid is built on.
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

TOLERANCE = 1e-8  # relative residual ||r|| / ||f|| that counts as converged
N_HISTORY = 63  # interior points per direction for the residual-history panel
N_SCALING = (15, 31, 63, 127)  # grids for the iterations-against-N panel
MAX_ITERATIONS = 200_000
MG_PRE_SMOOTH = 2  # red-black Gauss-Seidel sweeps before the coarse-grid correction
MG_POST_SMOOTH = 1  # sweeps after it
SMOOTHING_INTERVALS = 64  # 1D grid for the smoothing demonstration
SMOOTHING_OMEGA = 2.0 / 3.0  # weighted-Jacobi factor that damps high modes best in 1D
SMOOTHING_MODES = (3, 44)  # one smooth and one oscillatory error mode
SMOOTHING_SWEEPS = (1, 3, 10)
SEED = 3

METHODS = ("Jacobi", "Gauss-Seidel", "SOR (optimal)", "CG", "Multigrid V(2,1)")
COLORS = dict(zip(METHODS, plt.get_cmap("tab10").colors))


def grid_spacing(n):
    """Spacing h of an n x n interior grid on the unit square."""
    return 1.0 / (n + 1)


def random_rhs(n, seed=SEED):
    """Seeded source term on the interior points, padded with a zero boundary ring."""
    rng = np.random.default_rng(seed)
    f = np.zeros((n + 2, n + 2))
    f[1:-1, 1:-1] = rng.uniform(-1.0, 1.0, (n, n))
    return f


def norm2(a):
    """Euclidean norm of all entries (plain NumPy reduction, no BLAS threads)."""
    return float(np.sqrt(np.sum(a * a)))


def apply_laplacian(u, h):
    """Five-point -Laplacian of u on the interior; boundary entries stay zero."""
    out = np.zeros_like(u)
    out[1:-1, 1:-1] = (
        4.0 * u[1:-1, 1:-1] - u[:-2, 1:-1] - u[2:, 1:-1] - u[1:-1, :-2] - u[1:-1, 2:]
    ) / h**2
    return out


def residual(u, f, h):
    """r = f - A u (zero on the boundary ring)."""
    r = f - apply_laplacian(u, h)
    r[0, :] = r[-1, :] = r[:, 0] = r[:, -1] = 0.0
    return r


def jacobi(f, h, tol=TOLERANCE, max_iter=MAX_ITERATIONS, omega=1.0):
    """(Weighted) Jacobi: u <- u + omega D^-1 r. Returns u and the residual history."""
    u = np.zeros_like(f)
    norm_f = norm2(f)
    history = [1.0]
    for _ in range(max_iter):
        r = residual(u, f, h)
        history[-1] = norm2(r) / norm_f
        if history[-1] < tol:
            break
        u += omega * (h**2 / 4.0) * r
        history.append(np.nan)
    return u, np.array(history)


RED = ((1, 1), (2, 2))  # (row, column) start offsets of points with i + j even
BLACK = ((1, 2), (2, 1))


def sor_sweep(u, f, h, omega):
    """One red-black SOR sweep in place; omega = 1 is Gauss-Seidel.

    Points of one colour only have neighbours of the other colour, so each
    half-sweep is a vectorised update over strided slices.
    """
    n = u.shape[0] - 2
    for colour in (RED, BLACK):
        for a, b in colour:
            rows, cols = slice(a, n + 1, 2), slice(b, n + 1, 2)
            gs_value = 0.25 * (
                h**2 * f[rows, cols]
                + u[a - 1 : n : 2, cols]
                + u[a + 1 : n + 2 : 2, cols]
                + u[rows, b - 1 : n : 2]
                + u[rows, b + 1 : n + 2 : 2]
            )
            u[rows, cols] += omega * (gs_value - u[rows, cols])


def sor(f, h, omega=1.0, tol=TOLERANCE, max_iter=MAX_ITERATIONS):
    """Red-black SOR from u = 0. Returns u and the residual history."""
    u = np.zeros_like(f)
    norm_f = norm2(f)
    history = [1.0]
    for _ in range(max_iter):
        sor_sweep(u, f, h, omega)
        history.append(norm2(residual(u, f, h)) / norm_f)
        if history[-1] < tol:
            break
    return u, np.array(history)


def optimal_omega(n):
    """Optimal SOR factor for the model Poisson problem: 2 / (1 + sin(pi h))."""
    return 2.0 / (1.0 + np.sin(np.pi * grid_spacing(n)))


def conjugate_gradient(f, h, tol=TOLERANCE, max_iter=MAX_ITERATIONS):
    """Unpreconditioned CG for the SPD five-point matrix. Returns u and history."""
    u = np.zeros_like(f)
    r = residual(u, f, h)
    p = r.copy()
    rr = np.sum(r * r)
    norm_f = norm2(f)
    history = [np.sqrt(rr) / norm_f]
    for _ in range(max_iter):
        ap = apply_laplacian(p, h)
        alpha = rr / np.sum(p * ap)
        u += alpha * p
        r -= alpha * ap
        rr_new = np.sum(r * r)
        history.append(np.sqrt(rr_new) / norm_f)
        if history[-1] < tol:
            break
        p = r + (rr_new / rr) * p
        rr = rr_new
    return u, np.array(history)


def restrict_full_weighting(r):
    """Full-weighting restriction from an n = 2m + 1 grid to the m grid."""
    m = (r.shape[0] - 3) // 2
    coarse = np.zeros((m + 2, m + 2))
    c = r[2:-1:2, 2:-1:2]
    edges = r[1:-2:2, 2:-1:2] + r[3::2, 2:-1:2] + r[2:-1:2, 1:-2:2] + r[2:-1:2, 3::2]
    corners = r[1:-2:2, 1:-2:2] + r[1:-2:2, 3::2] + r[3::2, 1:-2:2] + r[3::2, 3::2]
    coarse[1:-1, 1:-1] = (4.0 * c + 2.0 * edges + corners) / 16.0
    return coarse


def prolong_bilinear(e_coarse):
    """Bilinear interpolation from an m grid to the n = 2m + 1 grid."""
    m = e_coarse.shape[0] - 2
    n = 2 * m + 1
    fine = np.zeros((n + 2, n + 2))
    fine[::2, ::2] = e_coarse  # coincident points (boundary zeros included)
    fine[1::2, ::2] = 0.5 * (fine[:-1:2, ::2] + fine[2::2, ::2])
    fine[:, 1::2] = 0.5 * (fine[:, :-1:2] + fine[:, 2::2])
    return fine


def v_cycle(u, f, h, nu1=MG_PRE_SMOOTH, nu2=MG_POST_SMOOTH):
    """One multigrid V-cycle with red-black Gauss-Seidel smoothing, in place."""
    n = u.shape[0] - 2
    if n == 1:
        u[1, 1] = 0.25 * h**2 * f[1, 1]  # exact solve of the 1 x 1 system
        return u
    for _ in range(nu1):
        sor_sweep(u, f, h, 1.0)
    r_coarse = restrict_full_weighting(residual(u, f, h))
    e_coarse = v_cycle(np.zeros_like(r_coarse), r_coarse, 2.0 * h, nu1, nu2)
    u += prolong_bilinear(e_coarse)
    for _ in range(nu2):
        sor_sweep(u, f, h, 1.0)
    return u


def multigrid(f, h, tol=TOLERANCE, max_iter=100):
    """Repeated V-cycles from u = 0 (n must be 2^k - 1). Returns u and history."""
    n = f.shape[0] - 2
    if n & (n + 1):
        raise ValueError("multigrid needs n = 2^k - 1 interior points")
    u = np.zeros_like(f)
    norm_f = norm2(f)
    history = [1.0]
    for _ in range(max_iter):
        v_cycle(u, f, h)
        history.append(norm2(residual(u, f, h)) / norm_f)
        if history[-1] < tol:
            break
    return u, np.array(history)


def solve(method, n, tol=TOLERANCE):
    """Run one of METHODS on the n x n random-source problem."""
    h = grid_spacing(n)
    f = random_rhs(n)
    if method == "Jacobi":
        return jacobi(f, h, tol)
    if method == "Gauss-Seidel":
        return sor(f, h, 1.0, tol)
    if method == "SOR (optimal)":
        return sor(f, h, optimal_omega(n), tol)
    if method == "CG":
        return conjugate_gradient(f, h, tol)
    if method == "Multigrid V(2,1)":
        return multigrid(f, h, tol)
    raise ValueError(method)


def jacobi_spectral_radius(n):
    """Spectral radius cos(pi h) of the Jacobi iteration matrix."""
    return np.cos(np.pi * grid_spacing(n))


def condition_number(n):
    """kappa = lambda_max / lambda_min = cot^2(pi h / 2) of the 2D five-point matrix."""
    return 1.0 / np.tan(0.5 * np.pi * grid_spacing(n)) ** 2


def weighted_jacobi_1d(e, omega, sweeps):
    """Apply weighted Jacobi to the 1D error equation -e'' = 0 (zero ends)."""
    e = e.copy()
    for _ in range(sweeps):
        e[1:-1] = (1 - omega) * e[1:-1] + 0.5 * omega * (e[:-2] + e[2:])
    return e


def jacobi_damping_factor(k, n_intervals, omega):
    """Eigenvalue 1 - 2 omega sin^2(k pi / 2n) of weighted Jacobi for mode k."""
    return 1.0 - 2.0 * omega * np.sin(0.5 * np.pi * k / n_intervals) ** 2


def make_figure(histories, counts, n_values):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    ax = axes[0, 0]
    for method in METHODS:
        hist = histories[method]
        ax.loglog(np.arange(1, len(hist) + 1), hist, color=COLORS[method], label=method)
    ax.axhline(TOLERANCE, color="gray", linestyle="--", linewidth=1)
    ax.text(12, TOLERANCE * 2, "tolerance $10^{-8}$", fontsize=10, color="gray")
    ax.set_xlim(1, None)
    ax.set_xlabel("Iteration $k$ + 1 (V-cycles for multigrid) [-]", fontsize=11)
    ax.set_ylabel(r"Relative residual $\|r\|_2 / \|f\|_2$ [-]", fontsize=11)
    ax.set_title(
        f"(a) Residual histories, {N_HISTORY} x {N_HISTORY} interior points",
        fontsize=12,
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper right")

    ax = axes[0, 1]
    n = np.array(n_values, dtype=float)
    for method in METHODS:
        ax.loglog(n, counts[method], "o-", color=COLORS[method], label=method)
    guides = (("Jacobi", 2, r"$N^2$"), ("SOR (optimal)", 1, r"$N$"))
    for method, slope, label in guides:
        ref = counts[method][-1] * (n / n[-1]) ** slope * 1.6
        ax.loglog(n, ref, "k:", linewidth=1)
        ax.text(n[1], ref[1] * 1.3, label, fontsize=11)
    ax.set_xlabel("Interior points per direction $N$ [-]", fontsize=11)
    ax.set_ylabel("Iterations to reach $10^{-8}$ [-]", fontsize=11)
    ax.set_title("(b) Cost growth with grid refinement", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.set_xticks(n, [f"{v:.0f}" for v in n])
    ax.minorticks_off()
    ax.legend(fontsize=10, loc="lower right", bbox_to_anchor=(1.0, 0.08))

    n_int = SMOOTHING_INTERVALS
    x = np.linspace(0.0, 1.0, n_int + 1)
    e0 = sum(np.sin(k * np.pi * x) for k in SMOOTHING_MODES)
    ax = axes[1, 0]
    ax.plot(x, e0, color="k", linewidth=1.2, label="initial error")
    for sweeps, color in zip(
        SMOOTHING_SWEEPS, plt.get_cmap("viridis")([0.2, 0.5, 0.8])
    ):
        e = weighted_jacobi_1d(e0, SMOOTHING_OMEGA, sweeps)
        ax.plot(
            x,
            e,
            color=color,
            linewidth=2,
            label=f"after {sweeps} sweep{'s' if sweeps > 1 else ''}",
        )
    ax.set_xlabel("$x$ [-]", fontsize=11)
    ax.set_ylabel("Error $e = u - u_h$ [-]", fontsize=11)
    ax.set_title(
        rf"(c) Weighted Jacobi ($\omega$ = 2/3) on modes k = {SMOOTHING_MODES[0]}"
        rf" and {SMOOTHING_MODES[1]}, n = {n_int}",
        fontsize=12,
    )
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower right", ncol=2)
    ax.set_ylim(-2.4, 2.4)

    ax = axes[1, 1]
    k = np.arange(1, n_int)
    for omega, color in ((1.0, "tab:red"), (2.0 / 3.0, "tab:blue"), (0.5, "tab:green")):
        lam = jacobi_damping_factor(k, n_int, omega)
        label = rf"$\omega$ = {omega:.3g}" if omega != 2.0 / 3.0 else r"$\omega$ = 2/3"
        ax.plot(k, np.abs(lam), color=color, linewidth=2, label=label)
    ax.axvspan(n_int / 2, n_int, color="0.9", zorder=0)
    ax.text(
        n_int / 2 + 1,
        0.9,
        "oscillatory modes $k \\geq n/2$\n(not representable on grid 2h)",
        fontsize=10,
    )
    ax.axhline(1.0 / 3.0, color="tab:blue", linestyle=":", linewidth=1)
    ax.set_xlabel("Mode number $k$ of $\\sin(k\\pi x)$ [-]", fontsize=11)
    ax.set_ylabel(r"Damping per sweep $|\lambda_k|$ [-]", fontsize=11)
    ax.set_title("(d) Weighted-Jacobi damping factor, 1D Poisson", fontsize=12)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower left")

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    start = time.perf_counter()
    histories = {m: solve(m, N_HISTORY)[1] for m in METHODS}
    counts = {m: [] for m in METHODS}
    for n in N_SCALING:
        for m in METHODS:
            counts[m].append(
                len(histories[m]) - 1 if n == N_HISTORY else len(solve(m, n)[1]) - 1
            )
    for n_idx, n in enumerate(N_SCALING):
        print(
            f"N = {n:3d}: rho_J = {jacobi_spectral_radius(n):.6f}, "
            f"omega_opt = {optimal_omega(n):.4f}, kappa = {condition_number(n):.0f}, "
            + ", ".join(f"{m} {counts[m][n_idx]}" for m in METHODS)
        )
    print(f"total time {time.perf_counter() - start:.1f} s")

    fig = make_figure(histories, counts, N_SCALING)
    finish_figures(
        {"iterative_linear_solvers.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
