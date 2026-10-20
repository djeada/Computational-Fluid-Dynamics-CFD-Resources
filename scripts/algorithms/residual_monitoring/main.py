"""Residuals, iterative error and a monitored wall flux during a Gauss-Seidel solve.

Solves the 2D Poisson problem -(phi_xx + phi_yy) = f on the unit square with
the exact solution phi = sin(pi x) sin(pi y) + sin(pi x) sinh(pi y) / sinh(pi),
using red-black Gauss-Seidel from phi = 0. After every sweep it records the
normalised residual, the change between iterates, the true iterative error
against the direct solution of the same discrete system, and the flux
through the bottom wall. It also shows two ways a residual history stalls (single
precision and an incompatible pure-Neumann problem) and the solution profile
after a few, a few hundred and many sweeps against the exact solution.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags, identity, kron
from scipy.sparse.linalg import spsolve

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures, positive_int  # noqa: E402

N = 31  # interior points per direction, h = 1 / 32
MAX_SWEEPS = 2500
FLUX_BAND = 1e-3  # monitor counts as converged when within 0.1 % of its final value
PROFILE_SWEEPS = (10, 100, 1000)
NEUMANN_N = 32  # cells per direction of the pure-Neumann problem
NEUMANN_SWEEPS = 1500
NEUMANN_MEAN_SOURCE = 0.05  # mean of f that violates the compatibility condition


def exact_solution(x, y):
    """phi = sin(pi x) sin(pi y) + sin(pi x) sinh(pi y) / sinh(pi)."""
    return np.sin(np.pi * x) * (np.sin(np.pi * y) + np.sinh(np.pi * y) / np.sinh(np.pi))


def exact_wall_flux():
    """Q = integral over x of d phi / dy at the bottom wall y = 0: 2 + 2 / sinh(pi)."""
    return 2.0 + 2.0 / np.sinh(np.pi)


def setup(n=N, dtype=np.float64):
    """Grid, source term and a field holding the Dirichlet boundary values."""
    h = 1.0 / (n + 1)
    x = np.linspace(0.0, 1.0, n + 2)
    xx, yy = np.meshgrid(x, x, indexing="ij")  # first index x, second index y
    f = (2.0 * np.pi**2 * np.sin(np.pi * xx) * np.sin(np.pi * yy)).astype(dtype)
    phi = np.zeros((n + 2, n + 2), dtype=dtype)
    phi[:, -1] = np.sin(np.pi * x)  # top wall y = 1; the other walls are zero
    return x, h, f, phi


def residual(phi, f, h):
    """r = f + Laplacian(phi) on the interior (zero on the boundary)."""
    r = np.zeros_like(phi)
    r[1:-1, 1:-1] = (
        f[1:-1, 1:-1]
        - (
            4.0 * phi[1:-1, 1:-1]
            - phi[:-2, 1:-1]
            - phi[2:, 1:-1]
            - phi[1:-1, :-2]
            - phi[1:-1, 2:]
        )
        / h**2
    )
    return r


def gauss_seidel_sweep(phi, f, h):
    """One red-black Gauss-Seidel sweep in place on the interior points."""
    n = phi.shape[0] - 2
    for a, b in ((1, 1), (2, 2), (1, 2), (2, 1)):  # red points, then black points
        rows, cols = slice(a, n + 1, 2), slice(b, n + 1, 2)
        phi[rows, cols] = 0.25 * (
            h**2 * f[rows, cols]
            + phi[a - 1 : n : 2, cols]
            + phi[a + 1 : n + 2 : 2, cols]
            + phi[rows, b - 1 : n : 2]
            + phi[rows, b + 1 : n + 2 : 2]
        )


def wall_flux(phi, h):
    """Second-order one-sided d phi / dy at y = 0, integrated over x (trapezoid rule)."""
    dphi = (-3.0 * phi[:, 0] + 4.0 * phi[:, 1] - phi[:, 2]) / (2.0 * h)
    return h * (np.sum(dphi) - 0.5 * (dphi[0] + dphi[-1]))


def direct_solution(n=N):
    """Solve the same five-point system with a sparse direct solver."""
    _, h, f, phi = setup(n)
    t = diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n))
    a = (kron(t, identity(n)) + kron(identity(n), t)) / h**2
    rhs = f[1:-1, 1:-1].copy()
    rhs[:, -1] += phi[1:-1, -1] / h**2  # known top-wall values
    out = phi.copy()
    out[1:-1, 1:-1] = spsolve(a.tocsc(), rhs.ravel()).reshape(n, n)
    return out


def monitored_solve(n=N, sweeps=MAX_SWEEPS, dtype=np.float64, keep=PROFILE_SWEEPS):
    """Gauss-Seidel with full monitoring; returns a dict of histories and snapshots."""
    _, h, f, phi = setup(n, dtype)
    phi_h = direct_solution(n)
    r0 = np.linalg.norm(residual(phi, f, h))
    norm_f = np.linalg.norm(f[1:-1, 1:-1].astype(np.float64))
    hist = {k: [] for k in ("res_initial", "res_f", "change", "error", "flux")}
    snapshots = {}
    for k in range(1, sweeps + 1):
        old = phi.copy()
        gauss_seidel_sweep(phi, f, h)
        r = np.linalg.norm(residual(phi, f, h).astype(np.float64))
        hist["res_initial"].append(r / r0)
        hist["res_f"].append(r / norm_f)
        hist["change"].append(np.linalg.norm(phi - old) / np.linalg.norm(phi))
        hist["error"].append(np.linalg.norm(phi - phi_h) / np.linalg.norm(phi_h))
        hist["flux"].append(wall_flux(phi.astype(np.float64), h))
        if k in keep:
            snapshots[k] = phi.copy()
    out = {key: np.array(val) for key, val in hist.items()}
    out["snapshots"] = snapshots
    out["phi_h"] = phi_h
    return out


def first_sweep_below(values, threshold):
    """1-based sweep after which ``values`` stays below ``threshold``."""
    above = np.nonzero(values >= threshold)[0]
    return 1 if len(above) == 0 else above[-1] + 2


def neumann_solve(n=NEUMANN_N, sweeps=NEUMANN_SWEEPS, mean_source=NEUMANN_MEAN_SOURCE):
    """Gauss-Seidel on -Laplacian(phi) = f with zero normal gradient on all walls.

    The cell-centred source f = cos(pi x) cos(pi y) + mean_source has a nonzero
    mean, so the compatibility condition (integral of f = 0) fails and no
    solution exists. Returns the relative residual and the mean of phi per sweep.
    """
    h = 1.0 / n
    xc = (np.arange(n) + 0.5) * h
    xx, yy = np.meshgrid(xc, xc, indexing="ij")
    f = np.cos(np.pi * xx) * np.cos(np.pi * yy) + mean_source
    phi = np.zeros((n, n))
    i, j = np.indices((n, n))
    colours = ((i + j) % 2 == 0, (i + j) % 2 == 1)
    res, mean = [], []
    for _ in range(sweeps):
        for mask in colours:  # red-black Gauss-Seidel
            padded = np.pad(
                phi, 1, mode="edge"
            )  # ghost cell = neighbour: zero gradient
            nb = (
                padded[:-2, 1:-1]
                + padded[2:, 1:-1]
                + padded[1:-1, :-2]
                + padded[1:-1, 2:]
            )
            phi[mask] = 0.25 * (nb + h**2 * f)[mask]
        padded = np.pad(phi, 1, mode="edge")
        lap = (
            padded[:-2, 1:-1]
            + padded[2:, 1:-1]
            + padded[1:-1, :-2]
            + padded[1:-1, 2:]
            - 4.0 * phi
        ) / h**2
        res.append(np.linalg.norm(f + lap) / np.linalg.norm(f))
        mean.append(phi.mean())
    return np.array(res), np.array(mean)


def make_figure(mon, mon32, neu_res, neu_mean, neu_res_ok, x, discretisation_error):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    sweeps = np.arange(1, len(mon["res_f"]) + 1)

    ax = axes[0, 0]
    ax.semilogy(
        sweeps,
        mon["res_initial"],
        color="tab:blue",
        linewidth=2,
        label=r"residual $\|r^k\| / \|r^0\|$",
    )
    ax.semilogy(
        sweeps,
        mon["res_f"],
        color="tab:blue",
        linestyle="--",
        linewidth=1.5,
        label=r"residual $\|r^k\| / \|f\|$",
    )
    ax.semilogy(
        sweeps,
        mon["change"],
        color="tab:orange",
        linewidth=2,
        label=r"change $\|\phi^k - \phi^{k-1}\| / \|\phi^k\|$",
    )
    ax.semilogy(
        sweeps,
        mon["error"],
        color="tab:red",
        linewidth=2,
        label=r"iterative error $\|\phi^k - \phi_h\| / \|\phi_h\|$",
    )
    ax.axhline(
        discretisation_error,
        color="k",
        linestyle=":",
        linewidth=1.5,
        label=r"discretisation error $\|\phi_h - \phi\| / \|\phi\|$",
    )
    ax.set_xlabel("Gauss-Seidel sweep $k$ [-]", fontsize=11)
    ax.set_ylabel("Relative norm [-]", fontsize=11)
    ax.set_title(f"(a) Residual, change and error, {N} x {N} grid", fontsize=12)
    ax.set_ylim(1e-15, 10)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9.5, loc="lower left")

    ax = axes[0, 1]
    q_h = wall_flux(mon["phi_h"], 1.0 / (N + 1))
    dev = np.abs(mon["flux"] - q_h) / abs(q_h)
    ax.semilogy(
        sweeps,
        dev,
        color="tab:green",
        linewidth=2,
        label=r"wall flux $|Q^k - Q_h| / |Q_h|$",
    )
    ax.semilogy(
        sweeps,
        mon["res_initial"],
        color="tab:blue",
        linewidth=1.5,
        alpha=0.7,
        label=r"residual $\|r^k\| / \|r^0\|$",
    )
    ax.axhline(FLUX_BAND, color="tab:green", linestyle=":", linewidth=1.2)
    k_flux = first_sweep_below(dev, FLUX_BAND)
    ax.axvline(k_flux, color="tab:green", linestyle=":", linewidth=1.2)
    ax.text(
        k_flux + 40,
        1e-12,
        f"flux within 0.1 %\nafter {k_flux} sweeps",
        fontsize=10,
        color="tab:green",
    )
    for drop, marker in ((1e-3, "o"), (1e-5, "s")):
        k = first_sweep_below(mon["res_initial"], drop)
        ax.plot(
            k,
            drop,
            marker,
            color="tab:blue",
            markersize=8,
            label=f"residual down {-np.log10(drop):.0f} orders: sweep {k}",
        )
    ax.set_xlabel("Gauss-Seidel sweep $k$ [-]", fontsize=11)
    ax.set_ylabel("Relative deviation [-]", fontsize=11)
    ax.set_title("(b) Monitored integral quantity: bottom-wall flux", fontsize=12)
    ax.set_ylim(1e-14, 10)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper right")

    ax = axes[1, 0]
    ax.semilogy(
        sweeps, mon["res_f"], color="tab:blue", linewidth=2, label="double precision"
    )
    ax.semilogy(
        sweeps,
        mon32["res_f"],
        color="tab:purple",
        linewidth=2,
        label="single precision: round-off floor",
    )
    k_neu = np.arange(1, len(neu_res) + 1)
    drift = neu_mean[-1] - neu_mean[-2]
    ax.semilogy(
        k_neu,
        neu_res,
        color="tab:red",
        linewidth=2,
        label=f"pure Neumann, mean(f) = {NEUMANN_MEAN_SOURCE}: no solution,\n"
        rf"mean $\phi$ drifts by {drift:.1e} per sweep",
    )
    ax.semilogy(
        k_neu,
        neu_res_ok,
        color="tab:red",
        linestyle="--",
        linewidth=1.5,
        label="pure Neumann, mean(f) = 0",
    )
    ax.set_xlabel("Gauss-Seidel sweep $k$ [-]", fontsize=11)
    ax.set_ylabel(r"Residual $\|r^k\| / \|f\|$ [-]", fontsize=11)
    ax.set_title("(c) Stalled residuals", fontsize=12)
    ax.set_ylim(1e-15, 10)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9.5, loc="lower left")

    ax = axes[1, 1]
    j = (N + 1) // 2  # y = 0.5
    xf = np.linspace(0, 1, 401)
    ax.plot(xf, exact_solution(xf, 0.5), "k-", linewidth=1.5, label="exact")
    ax.plot(
        x,
        mon["phi_h"][:, j],
        "ko",
        markersize=4,
        fillstyle="none",
        label="converged discrete",
    )
    for k, color in zip(PROFILE_SWEEPS, plt.get_cmap("viridis")([0.15, 0.5, 0.8])):
        ax.plot(
            x,
            mon["snapshots"][k][:, j],
            "-",
            color=color,
            linewidth=2,
            label=f"after {k} sweeps",
        )
    ax.set_xlabel("$x$ [-]", fontsize=11)
    ax.set_ylabel(r"$\phi(x, 0.5)$ [-]", fontsize=11)
    ax.set_title("(d) Profile along y = 0.5", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower center")

    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=MAX_SWEEPS,
        metavar="N",
        help=f"number of Gauss-Seidel sweeps (default {MAX_SWEEPS}, at least {max(PROFILE_SWEEPS)} for the profiles)",
    )
    args = parser.parse_args(argv)
    sweeps = max(args.steps, max(PROFILE_SWEEPS))

    x, h, _, _ = setup()
    mon = monitored_solve(sweeps=sweeps)
    mon32 = monitored_solve(sweeps=sweeps, dtype=np.float32)
    neu_res, neu_mean = neumann_solve()
    neu_res_ok, _ = neumann_solve(mean_source=0.0)

    xx, yy = np.meshgrid(x, x, indexing="ij")
    phi_exact = exact_solution(xx, yy)
    disc = np.linalg.norm(mon["phi_h"] - phi_exact) / np.linalg.norm(phi_exact)
    q_exact, q_h = exact_wall_flux(), wall_flux(mon["phi_h"], h)
    print(
        f"grid {N} x {N}: discretisation error {disc:.3e}, Q exact {q_exact:.6f}, Q discrete {q_h:.6f}"
    )
    err = mon["error"]
    lo, hi = len(err) // 5, len(err) // 2
    rho = (err[hi] / err[lo]) ** (1.0 / (hi - lo))
    print(
        f"asymptotic error ratio per sweep {rho:.5f} (cos^2(pi h) = {np.cos(np.pi * h) ** 2:.5f})"
    )
    for drop in (1e-3, 1e-4, 1e-5, 1e-6):
        k = first_sweep_below(mon["res_initial"], drop)
        if k > len(mon["res_initial"]):
            print(f"  residual not below {drop:.0e} of initial within {sweeps} sweeps")
            continue
        print(
            f"  residual below {drop:.0e} of initial after {k:4d} sweeps: "
            f"iterative error {mon['error'][k - 1]:.2e}, flux deviation "
            f"{abs(mon['flux'][k - 1] - q_h) / abs(q_h):.2e}"
        )
    k_err = first_sweep_below(mon["error"], disc)
    print(f"iterative error below discretisation error after {k_err} sweeps")
    print(f"single-precision residual floor {np.min(mon32['res_f']):.2e}")
    print(
        f"Neumann problem: residual floor {neu_res[-1]:.3e}, mean phi drift per sweep {neu_mean[-1] - neu_mean[-2]:.3e}"
    )
    print(f"compatible Neumann problem: final residual {neu_res_ok[-1]:.2e}")

    fig = make_figure(mon, mon32, neu_res, neu_mean, neu_res_ok, x, disc)
    finish_figures(
        {"residual_monitoring.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
