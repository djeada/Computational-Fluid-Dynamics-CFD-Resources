"""Code verification of a 2D Poisson solver with the method of manufactured solutions.

A second-order five-point finite-difference solver for -lap(phi) = f on the
unit square, with Dirichlet conditions on three sides and a Neumann condition
on x = 1, is verified against a chosen smooth solution phi_m. The source term
and boundary data are derived from phi_m analytically, the discrete error is
measured on a sequence of grids, and the observed order of accuracy is
compared with the formal order 2. A second solver, identical except that the
Neumann boundary uses a first-order one-sided difference, shows how the test
exposes a boundary-treatment bug: its observed order drops to 1.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Manufactured solution phi_m = exp(A x) sin(pi y + B) + C cos(K pi x)
# (dimensionless; the unit square has side length 1).
A = 0.5  # growth rate of the exponential part in x
B = 0.4  # phase shift in y, so phi_m is non-zero on y = 0 and y = 1
C = 0.25  # amplitude of the cosine part
K = 1.25  # wavenumber factor of the cosine part

N_SEQUENCE = (8, 16, 32, 64, 128, 256)  # intervals per side, refinement ratio 2
N_FIELD = 32  # grid used for the error-field panels


def manufactured(x, y):
    """Manufactured solution phi_m(x, y)."""
    return np.exp(A * x) * np.sin(np.pi * y + B) + C * np.cos(K * np.pi * x)


def manufactured_dx(x, y):
    """Derivative d(phi_m)/dx, the Neumann data on x = 1."""
    return A * np.exp(A * x) * np.sin(np.pi * y + B) - C * K * np.pi * np.sin(
        K * np.pi * x
    )


def manufactured_source(x, y):
    """Source term f = -lap(phi_m), derived by hand from phi_m."""
    return -(A**2 - np.pi**2) * np.exp(A * x) * np.sin(np.pi * y + B) + C * (
        K * np.pi
    ) ** 2 * np.cos(K * np.pi * x)


def solve_poisson(n, neumann_order=2):
    """Solve -lap(phi) = f on n x n intervals with the manufactured data.

    Dirichlet values phi_m are imposed on x = 0, y = 0 and y = 1. On x = 1 the
    Neumann condition d(phi)/dx = g is imposed either with a ghost node and the
    five-point equation at the boundary node (``neumann_order=2``) or with the
    one-sided difference (phi_N - phi_{N-1}) / h = g (``neumann_order=1``, the
    deliberate bug). Returns the node coordinates and the full nodal solution
    with shape (n + 1, n + 1) indexed [i, j] for (x_i, y_j).
    """
    if neumann_order not in (1, 2):
        raise ValueError("neumann_order must be 1 or 2")
    h = 1.0 / n
    x = np.linspace(0.0, 1.0, n + 1)
    y = np.linspace(0.0, 1.0, n + 1)
    phi = np.zeros((n + 1, n + 1))
    phi[0, :] = manufactured(0.0, y)
    phi[:, 0] = manufactured(x, 0.0)
    phi[:, -1] = manufactured(x, 1.0)

    # Unknowns: i = 1..n (x = 1 included), j = 1..n-1.
    ni, nj = n, n - 1

    def index(i, j):
        return (i - 1) * nj + (j - 1)

    rows, cols, vals = [], [], []
    rhs = np.zeros(ni * nj)

    def add(row, i, j, coef):
        """Add coef * phi_{i,j}: unknowns go to the matrix, known values to rhs."""
        if 1 <= i <= n and 1 <= j <= n - 1:
            rows.append(row)
            cols.append(index(i, j))
            vals.append(coef)
        else:
            rhs[row] -= coef * phi[i, j]

    for i in range(1, n + 1):
        for j in range(1, n):
            row = index(i, j)
            if i < n:
                # Interior five-point equation, multiplied by h^2.
                add(row, i, j, 4.0)
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    add(row, i + di, j + dj, -1.0)
                rhs[row] += h**2 * manufactured_source(x[i], y[j])
            elif neumann_order == 2:
                # Ghost node phi_{n+1,j} = phi_{n-1,j} + 2 h g_j substituted
                # into the five-point equation at the boundary node.
                add(row, i, j, 4.0)
                add(row, i - 1, j, -2.0)
                add(row, i, j - 1, -1.0)
                add(row, i, j + 1, -1.0)
                rhs[row] += h**2 * manufactured_source(x[i], y[j])
                rhs[row] += 2.0 * h * manufactured_dx(x[i], y[j])
            else:
                # First-order one-sided difference, multiplied by h.
                add(row, i, j, 1.0)
                add(row, i - 1, j, -1.0)
                rhs[row] += h * manufactured_dx(x[i], y[j])

    matrix = sp.csr_matrix((vals, (rows, cols)), shape=(ni * nj, ni * nj))
    phi[1:, 1:-1] = spsolve(matrix, rhs).reshape(ni, nj)
    return x, y, phi


def error_norms(n, neumann_order=2):
    """Discrete L2 (root-mean-square over all nodes) and max-norm errors."""
    x, y, phi = solve_poisson(n, neumann_order)
    xx, yy = np.meshgrid(x, y, indexing="ij")
    err = phi - manufactured(xx, yy)
    return np.sqrt(np.mean(err**2)), np.max(np.abs(err))


def observed_orders(errors, ratio=2.0):
    """Observed order log(e_k / e_{k+1}) / log(r) between consecutive grids."""
    errors = np.asarray(errors)
    return np.log(errors[:-1] / errors[1:]) / np.log(ratio)


def convergence_study(n_sequence=N_SEQUENCE):
    """Error norms of both solvers on every grid of the sequence."""
    n = np.array(n_sequence)
    results = {}
    for order in (2, 1):
        norms = np.array([error_norms(k, order) for k in n])
        results[order] = {"l2": norms[:, 0], "linf": norms[:, 1]}
    return n, results


def make_figure(n_seq, results):
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 10.5))
    xf = np.linspace(0.0, 1.0, 201)
    xx, yy = np.meshgrid(xf, xf, indexing="ij")

    ax = axes[0, 0]
    cs = ax.contourf(xx, yy, manufactured(xx, yy), levels=21, cmap="viridis")
    fig.colorbar(cs, ax=ax, label=r"$\phi_m$ [-]")
    ax.set_title(
        "(a) Manufactured solution\n"
        r"$\phi_m = e^{x/2}\sin(\pi y + 0.4) + \frac{1}{4}\cos(1.25\pi x)$",
        fontsize=11,
    )
    ax.annotate(
        r"Neumann $\partial\phi/\partial x = g$",
        xy=(1.0, 0.5),
        xytext=(0.52, 0.5),
        fontsize=10,
        color="white",
        arrowprops={"arrowstyle": "->", "color": "white"},
        va="center",
    )
    ax.text(0.03, 0.5, "Dirichlet", rotation=90, color="white", va="center")

    for ax, order, label in (
        (axes[0, 1], 2, "ghost-node Neumann (correct)"),
        (axes[1, 0], 1, "one-sided Neumann (bug)"),
    ):
        x, y, phi = solve_poisson(N_FIELD, order)
        gx, gy = np.meshgrid(x, y, indexing="ij")
        err = phi - manufactured(gx, gy)
        vmax = np.max(np.abs(err))
        pc = ax.pcolormesh(
            gx, gy, err, cmap="RdBu_r", vmin=-vmax, vmax=vmax, shading="gouraud"
        )
        fig.colorbar(pc, ax=ax, label=r"$\phi_h - \phi_m$ [-]", format="%.1e")
        panel = "(b)" if order == 2 else "(c)"
        ax.set_title(
            f"{panel} Error field, {label}, N = {N_FIELD}\nmax |error| = {vmax:.2e}",
            fontsize=11,
        )

    for ax in axes.flat[:3]:
        ax.set_xlabel("x [-]")
        ax.set_ylabel("y [-]")
        ax.set_aspect("equal")

    ax = axes[1, 1]
    h = 1.0 / n_seq
    styles = {
        (2, "l2"): ("tab:blue", "o-", r"correct, $L_2$"),
        (2, "linf"): ("tab:blue", "s--", r"correct, $L_\infty$"),
        (1, "l2"): ("tab:orange", "o-", r"bug, $L_2$"),
        (1, "linf"): ("tab:orange", "s--", r"bug, $L_\infty$"),
    }
    for (order, norm), (color, fmt, label) in styles.items():
        e = results[order][norm]
        p = observed_orders(e)[-1]
        ax.loglog(h, e, fmt, color=color, label=f"{label}: p = {p:.2f}")
    ref = results[2]["l2"][-1]
    ax.loglog(h, ref * (h / h[-1]) ** 2 / 3, "k:", label="slope 2")
    ref = results[1]["linf"][-1]
    ax.loglog(h, 2.5 * ref * (h / h[-1]), "k-.", label="slope 1")
    ax.set_xlabel("Grid spacing h [-]")
    ax.set_ylabel(r"Error $\phi_h - \phi_m$ [-]")
    ax.set_title(
        "(d) Error against h, observed order p on the two finest grids", fontsize=11
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    n_seq, results = convergence_study()
    for order, name in ((2, "ghost-node Neumann"), (1, "one-sided Neumann (bug)")):
        print(f"{name}:")
        p_l2 = observed_orders(results[order]["l2"])
        p_linf = observed_orders(results[order]["linf"])
        for k, n in enumerate(n_seq):
            line = (
                f"  N = {n:4d}: L2 = {results[order]['l2'][k]:.3e}, "
                f"Linf = {results[order]['linf'][k]:.3e}"
            )
            if k > 0:
                line += f", p(L2) = {p_l2[k - 1]:.3f}, p(Linf) = {p_linf[k - 1]:.3f}"
            print(line)

    fig = make_figure(n_seq, results)
    finish_figures(
        {"method_of_manufactured_solutions.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
