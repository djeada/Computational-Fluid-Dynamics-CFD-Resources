"""First-order and second-order treatments of Neumann and Robin boundary conditions.

The model problem is a cooling fin, -theta'' + m^2 theta = 0 on (0, 1), with a
prescribed heat flux at the base (Neumann) and convective heat loss at the tip
(Robin). It is solved four ways: vertex-centred finite differences with
first-order one-sided boundary differences or with second-order ghost nodes,
and cell-centred finite volumes with the boundary-face value taken as the
adjacent cell value (first order) or obtained from a ghost cell (second
order). The figure shows the boundary stencils, the coarse-grid solutions
against the exact solution, and the observed order of each variant.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

# Dimensionless fin: x = X / L, theta = (T - T_inf) k / (q_base L).
FIN_PARAMETER = 1.0  # m = sqrt(h_c P / (k A_c)) L [-]
BASE_FLUX = 1.0  # -theta'(0), dimensionless heat flux entering at the base [-]
TIP_BIOT = 2.0  # Bi = h_tip L / k in -theta'(1) = Bi theta(1) [-]

N_SEQUENCE = (4, 8, 16, 32, 64, 128, 256, 512)  # intervals or cells
N_PLOT = 4  # coarse grid of the solution panel

VARIANTS = (
    ("fd", 1, "FD, one-sided boundary differences", "tab:orange", "s--"),
    ("fd", 2, "FD, ghost nodes", "tab:blue", "o-"),
    ("fv", 1, "FV, face value = cell value", "tab:red", "^--"),
    ("fv", 2, "FV, ghost cells", "tab:green", "D-"),
)


def exact_solution(x, m=FIN_PARAMETER, q=BASE_FLUX, bi=TIP_BIOT):
    """theta = A cosh(m x) + B sinh(m x) with -theta'(0) = q, -theta'(1) = Bi theta(1)."""
    b = -q / m
    a = -b * (m * np.cosh(m) + bi * np.sinh(m)) / (m * np.sinh(m) + bi * np.cosh(m))
    return a * np.cosh(m * x) + b * np.sinh(m * x)


def _solve_tridiagonal(lower, diag, upper, rhs):
    """Solve a tridiagonal system given its three diagonals (lower[0], upper[-1] unused)."""
    ab = np.zeros((3, len(diag)))
    ab[0, 1:] = upper[:-1]
    ab[1, :] = diag
    ab[2, :-1] = lower[1:]
    return solve_banded((1, 1), ab, rhs)


def solve_fd(n, order, m=FIN_PARAMETER, q=BASE_FLUX, bi=TIP_BIOT):
    """Vertex-centred finite differences on n intervals; returns nodes and theta.

    ``order=1`` closes the system with (theta_0 - theta_1)/h = q and
    (theta_n - theta_{n-1})/h + Bi theta_n = 0. ``order=2`` applies the
    three-point equation at the boundary nodes with the ghost values
    theta_{-1} = theta_1 + 2 h q and theta_{n+1} = theta_{n-1} - 2 h Bi theta_n.
    """
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    h = 1.0 / n
    size = n + 1
    lower = np.full(size, -1.0)
    diag = np.full(size, 2.0 + (m * h) ** 2)
    upper = np.full(size, -1.0)
    rhs = np.zeros(size)
    if order == 1:
        diag[0], upper[0], rhs[0] = 1.0, -1.0, h * q
        lower[-1], diag[-1] = -1.0, 1.0 + h * bi
    else:
        upper[0], rhs[0] = -2.0, 2.0 * h * q
        lower[-1], diag[-1] = -2.0, 2.0 + 2.0 * h * bi + (m * h) ** 2
    return np.linspace(0.0, 1.0, size), _solve_tridiagonal(lower, diag, upper, rhs)


def solve_fv(n, order, m=FIN_PARAMETER, q=BASE_FLUX, bi=TIP_BIOT):
    """Cell-centred finite volumes on n cells; returns cell centres and theta.

    Cell balance: F_w - F_e - m^2 theta_P h = 0 with flux F = -theta'.
    Interior faces use F = -(theta_E - theta_P)/h and the base face carries the
    prescribed flux q exactly. At the tip face, ``order=1`` takes the face
    value equal to the cell value, F_b = Bi theta_P; ``order=2`` places a ghost
    cell so that the linear profile through theta_P and theta_G satisfies the
    Robin condition at the face, which gives F_b = theta_P / (1/Bi + h/2).
    """
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    h = 1.0 / n
    # Equations multiplied by h: coefficients of theta_W, theta_P, theta_E.
    lower = np.full(n, -1.0)
    diag = np.full(n, 2.0 + (m * h) ** 2)
    upper = np.full(n, -1.0)
    rhs = np.zeros(n)
    diag[0] -= 1.0  # base face flux is q, not a difference
    rhs[0] = h * q
    tip_conductance = bi if order == 1 else 1.0 / (1.0 / bi + 0.5 * h)
    diag[-1] += -1.0 + h * tip_conductance
    x = (np.arange(n) + 0.5) * h
    return x, _solve_tridiagonal(lower, diag, upper, rhs)


def solve(method, n, order):
    """Dispatch to the finite-difference or finite-volume solver."""
    return (solve_fd if method == "fd" else solve_fv)(n, order)


def max_error(method, n, order):
    """Maximum error over the solution points (nodes or cell centres)."""
    x, theta = solve(method, n, order)
    return np.max(np.abs(theta - exact_solution(x)))


def observed_orders(errors, ratio=2.0):
    """Observed order log(e_k / e_{k+1}) / log(r) between consecutive grids."""
    errors = np.asarray(errors)
    return np.log(errors[:-1] / errors[1:]) / np.log(ratio)


def convergence_study(n_sequence=N_SEQUENCE):
    """Max-norm errors of every variant on every grid."""
    return {
        (method, order): np.array([max_error(method, n, order) for n in n_sequence])
        for method, order, *_ in VARIANTS
    }


def _draw_stencils(ax):
    """Sketch of the ghost node (FD) and ghost cell (FV) at the tip x = 1."""
    ax.axvline(3.0, color="k", linewidth=2.5)
    ax.text(3.05, 1.82, "boundary x = 1", fontsize=10, va="top")
    ax.axvspan(3.0, 4.2, color="0.92", zorder=0)
    ax.text(3.6, -0.55, "outside the domain", fontsize=10, ha="center")

    # FD row: nodes at x_{N-2}, x_{N-1}, x_N on the boundary, ghost x_{N+1}.
    y_fd = 1.2
    ax.plot([0.6, 3.0], [y_fd, y_fd], color="k", linewidth=1)
    ax.plot([3.0, 3.8], [y_fd, y_fd], color="k", linewidth=1, linestyle=":")
    for xi, label in ((1.0, "$N-2$"), (2.0, "$N-1$"), (3.0, "$N$")):
        ax.plot(xi, y_fd, "o", color="tab:blue", markersize=11)
        ax.text(xi - 0.04, y_fd + 0.18, label, ha="right", fontsize=10)
    ax.plot(4.0, y_fd, "o", markersize=11, markerfacecolor="white", color="tab:blue")
    ax.text(4.0, y_fd + 0.18, "ghost $N+1$", ha="center", fontsize=10)
    ax.text(3.05, 0.42, "face b", fontsize=10)
    ax.text(
        0.5,
        y_fd - 0.35,
        r"FD: $\theta_{N+1} = \theta_{N-1} - 2h\,\mathrm{Bi}\,\theta_N$, "
        "then the interior equation at node $N$",
        fontsize=10,
    )

    # FV row: cells W, P adjacent to the boundary face, ghost cell G.
    y_fv = 0.15
    for x0, label, ghost in ((1.0, "W", False), (2.0, "P", False), (3.0, "G", True)):
        ax.add_patch(
            Rectangle(
                (x0, y_fv - 0.2),
                1.0,
                0.4,
                fill=False,
                linestyle=":" if ghost else "-",
                edgecolor="tab:green",
                linewidth=1.5,
            )
        )
        ax.plot(
            x0 + 0.5,
            y_fv,
            "s",
            color="tab:green",
            markersize=9,
            markerfacecolor="white" if ghost else "tab:green",
        )
        ax.text(x0 + 0.5, y_fv + 0.25, label, ha="center", fontsize=10)
    ax.text(
        0.5,
        y_fv - 0.45,
        r"FV: $\theta_b = (\theta_P + \theta_G)/2$, "
        r"$-(\theta_G - \theta_P)/h = \mathrm{Bi}\,\theta_b$",
        fontsize=10,
    )
    ax.set_xlim(0.4, 4.3)
    ax.set_ylim(-0.7, 1.9)
    ax.axis("off")
    ax.set_title("(a) Boundary stencils at the convective tip", fontsize=11)


def make_figure(n_seq, errors):
    fig = plt.figure(figsize=(13, 9.5))
    grid = fig.add_gridspec(2, 2, height_ratios=(0.65, 1.0))
    _draw_stencils(fig.add_subplot(grid[0, :]))

    ax = fig.add_subplot(grid[1, 0])
    xf = np.linspace(0.0, 1.0, 200)
    ax.plot(xf, exact_solution(xf), "k-", linewidth=2, label="exact")
    for method, order, label, color, fmt in VARIANTS:
        x, theta = solve(method, N_PLOT, order)
        ax.plot(x, theta, fmt, color=color, label=label, markersize=7)
    ax.set_xlabel("x [-]")
    ax.set_ylabel(r"Fin temperature $\theta$ [-]")
    ax.set_title(f"(b) Solutions on N = {N_PLOT} intervals or cells", fontsize=11)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="upper right")

    ax = fig.add_subplot(grid[1, 1])
    h = 1.0 / np.asarray(n_seq)
    for method, order, label, color, fmt in VARIANTS:
        e = errors[(method, order)]
        p = observed_orders(e)[-1]
        ax.loglog(h, e, fmt, color=color, label=f"{label}: p = {p:.2f}")
    ax.loglog(h, 2.0 * h, "k-.", linewidth=1, label="slope 1")
    ax.loglog(h, 0.01 * h**2, "k:", linewidth=1, label="slope 2")
    ax.set_xlabel("Grid spacing h [-]")
    ax.set_ylabel(r"Max error $|\theta_h - \theta|$ [-]")
    ax.set_title("(c) Error against h, observed order on the finest pair", fontsize=11)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9, loc="lower right")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    n_seq = np.array(N_SEQUENCE)
    errors = convergence_study(n_seq)
    print(f"Exact tip temperature theta(1) = {exact_solution(1.0):.6f}")
    for method, order, label, *_ in VARIANTS:
        e = errors[(method, order)]
        p = observed_orders(e)
        print(f"{label}:")
        print("  max errors:", " ".join(f"{v:.2e}" for v in e))
        print("  observed p:", " ".join(f"{v:.3f}" for v in p))

    fig = make_figure(n_seq, errors)
    finish_figures(
        {"ghost_cell_boundary_conditions.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
