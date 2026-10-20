"""Learning a mesh-size field for a 1D convection-diffusion boundary layer.

Solves -eps u'' + u' = 0 on [0, 1] with u(0) = 0, u(1) = 1, whose solution
has an outflow boundary layer of width eps = 1/Pe. For training Peclet numbers
the optimal mesh density for the piecewise-linear L2 error is computed from the
exact second derivative, and a ridge regression on two features (log10 Pe and
the wall distance in layer units) learns the log density. For unseen Peclet
numbers the predicted density is turned into a mesh by equidistribution, the
linear finite-element problem is solved, and the L2 error is compared with
uniform meshes and with meshes built from the exact optimal density.
"""

import sys
from itertools import combinations_with_replacement
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_banded

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

TRAIN_PECLET = [10, 20, 50, 100, 200, 500, 1000]  # Pe = U L / D of training cases
TEST_PECLET = [30, 300, 3000]  # unseen cases (3000 lies outside the training range)
POLY_DEGREE = 4  # total degree of the polynomial features
RIDGE = 1e-8  # ridge penalty on the polynomial coefficients
DENSITY_EXPONENT = 0.4  # rho ~ |u''|^(2/5) minimises the L2 interpolation error
NODE_COUNTS = np.array([10, 14, 20, 28, 40, 57, 80, 113, 160, 226, 320])
N_SHOW = 20  # number of elements in the solution panel
N_FINE_UNIFORM = 4001  # uniform part of the fine reference grid
N_FINE_LAYER = 3000  # extra points clustered geometrically in the layer


def exact_solution(x, pe):
    """u(x) = (exp(Pe (x - 1)) - exp(-Pe)) / (1 - exp(-Pe)), overflow-free."""
    return (np.exp(pe * (x - 1.0)) - np.exp(-pe)) / (1.0 - np.exp(-pe))


def exact_second_derivative(x, pe):
    return pe**2 * np.exp(pe * (x - 1.0)) / (1.0 - np.exp(-pe))


def reference_grid(pe):
    """Fine grid on [0, 1] that resolves the layer of width 1/Pe."""
    layer = 1.0 - np.logspace(-5, 1.5, N_FINE_LAYER) / pe
    grid = np.concatenate([np.linspace(0.0, 1.0, N_FINE_UNIFORM), layer])
    return np.unique(np.clip(grid, 0.0, 1.0))


def normalised(x, rho):
    """Scale a density so that its integral over [0, 1] is one."""
    return rho / np.trapezoid(rho, x)


def optimal_density(x, pe):
    """Regularised equidistribution density (1 + |u''|/alpha)^(2/5).

    alpha = (int |u''|^(2/5) dx)^(5/2) is the integral choice: it puts a
    Pe-independent share (about half) of the nodes inside the layer.
    """
    curvature = np.abs(exact_second_derivative(x, pe))
    alpha = np.trapezoid(curvature**DENSITY_EXPONENT, x) ** (1.0 / DENSITY_EXPONENT)
    return normalised(x, (1.0 + curvature / alpha) ** DENSITY_EXPONENT)


def equidistribute(x, rho, n_elements):
    """Nodes x_j with equal density mass int rho dx between neighbours."""
    mass = np.concatenate([[0.0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * np.diff(x))])
    nodes = np.interp(np.linspace(0.0, mass[-1], n_elements + 1), mass, x)
    nodes[0], nodes[-1] = 0.0, 1.0
    return nodes


def solve_fem(nodes, pe):
    """Linear Galerkin FE for -eps u'' + u' = 0 with Dirichlet ends."""
    eps = 1.0 / pe
    h = np.diff(nodes)
    n = nodes.size
    lower = np.zeros(n)  # A[i, i-1]
    diag = np.zeros(n)
    upper = np.zeros(n)  # A[i, i+1]
    # Element matrix: eps/h [[1, -1], [-1, 1]] + 1/2 [[-1, 1], [-1, 1]].
    diag[:-1] += eps / h - 0.5
    diag[1:] += eps / h + 0.5
    upper[:-1] += -eps / h + 0.5
    lower[1:] += -eps / h - 0.5
    rhs = np.zeros(n)
    diag[[0, -1]] = 1.0
    upper[0] = lower[-1] = 0.0
    rhs[-1] = 1.0
    banded = np.zeros((3, n))
    banded[0, 1:] = upper[:-1]
    banded[1] = diag
    banded[2, :-1] = lower[1:]
    return solve_banded((1, 1), banded, rhs)


def l2_error(nodes, u_h, pe):
    x = np.unique(np.concatenate([reference_grid(pe), nodes]))
    diff = np.interp(x, nodes, u_h) - exact_solution(x, pe)
    return np.sqrt(np.trapezoid(diff**2, x))


def features(x, pe):
    """Polynomial features of (log10 Pe, log10(1 + (1 - x) Pe))."""
    s = np.full_like(x, np.log10(pe))
    xi = np.log10(1.0 + (1.0 - x) * pe)
    base = [s / 3.0, xi / 3.0]  # roughly O(1) inputs
    columns = [np.ones_like(x)]
    for degree in range(1, POLY_DEGREE + 1):
        for combo in combinations_with_replacement(range(2), degree):
            columns.append(np.prod([base[i] for i in combo], axis=0))
    return np.column_stack(columns)


def training_set(peclets, n_points=300):
    """Feature rows and log10 density targets sampled on each training case."""
    rows, targets = [], []
    for pe in peclets:
        x = reference_grid(pe)
        rho = optimal_density(x, pe)
        pick = np.linspace(0, x.size - 1, n_points).astype(int)
        rows.append(features(x[pick], pe))
        targets.append(np.log10(rho[pick]))
    return np.vstack(rows), np.concatenate(targets)


def fit_ridge(phi, y, ridge=RIDGE):
    """Ridge regression coefficients (Phi^T Phi + lambda I)^-1 Phi^T y."""
    gram = phi.T @ phi + ridge * np.eye(phi.shape[1])
    return np.linalg.solve(gram, phi.T @ y)


def predicted_density(x, pe, coef):
    return normalised(x, 10.0 ** (features(x, pe) @ coef))


def error_curves(pe, coef, node_counts=NODE_COUNTS):
    """L2 error of uniform, optimally adapted and ML-predicted meshes."""
    x = reference_grid(pe)
    densities = {
        "adapted (exact $u''$)": optimal_density(x, pe),
        "ML-predicted size field": predicted_density(x, pe, coef),
    }
    curves = {"uniform": []}
    curves.update({name: [] for name in densities})
    for n in node_counts:
        nodes = np.linspace(0.0, 1.0, n + 1)
        curves["uniform"].append(l2_error(nodes, solve_fem(nodes, pe), pe))
        for name, rho in densities.items():
            nodes = equidistribute(x, rho, n)
            curves[name].append(l2_error(nodes, solve_fem(nodes, pe), pe))
    return {name: np.array(values) for name, values in curves.items()}


STYLES = {
    "uniform": {"color": "0.4", "marker": "o", "ls": "-"},
    "adapted (exact $u''$)": {"color": "tab:blue", "marker": "s", "ls": "-"},
    "ML-predicted size field": {"color": "tab:orange", "marker": "^", "ls": "--"},
}


def make_figure(coef, curves_by_pe):
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    axs = axs.ravel()
    colors = ["tab:green", "tab:purple", "tab:red"]

    ax = axs[0]
    for pe, color in zip(TEST_PECLET, colors):
        x = reference_grid(pe)
        x = x[x < 1.0]
        dist = 1.0 - x
        h_opt = 1.0 / (N_SHOW * optimal_density(x, pe))
        h_ml = 1.0 / (N_SHOW * predicted_density(x, pe, coef))
        ax.loglog(dist, h_opt, color=color, lw=2, label=f"Pe = {pe} optimal")
        ax.loglog(dist, h_ml, color="k", lw=1.2, ls="--")
    ax.plot([], [], "k--", lw=1.2, label="ML prediction")
    ax.set_xlim(1e-5, 1.0)
    ax.set_xlabel("distance from outflow wall $1 - x$")
    ax.set_ylabel(f"mesh size $h(x)$ for N = {N_SHOW} elements")
    ax.set_title("Size field for unseen Peclet numbers")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=9, loc="lower right")

    ax = axs[1]
    pe = TEST_PECLET[1]
    x_fine = np.linspace(0.85, 1.0, 1500)
    ax.plot(x_fine, exact_solution(x_fine, pe), "k-", lw=2, label="exact")
    x_ref = reference_grid(pe)
    meshes = {
        "uniform": np.linspace(0.0, 1.0, N_SHOW + 1),
        "ML-predicted size field": equidistribute(
            x_ref, predicted_density(x_ref, pe, coef), N_SHOW
        ),
    }
    for name, nodes in meshes.items():
        style = STYLES[name]
        ax.plot(
            nodes,
            solve_fem(nodes, pe),
            color=style["color"],
            marker=style["marker"],
            ls=style["ls"],
            ms=5,
            label=f"{name}, N = {N_SHOW}",
        )
    ax.set_xlim(0.85, 1.005)
    ax.set_ylim(-1.5, 1.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$u$")
    ax.set_title(f"FE solutions near the layer, Pe = {pe}")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)

    for ax, (pe, curves) in zip(axs[2:], curves_by_pe.items()):
        for name, err in curves.items():
            ax.loglog(NODE_COUNTS, err, **STYLES[name], label=name)
        ax.loglog(
            NODE_COUNTS, 2.0 / NODE_COUNTS**2, "k:", lw=1, label=r"$\propto N^{-2}$"
        )
        inside = TRAIN_PECLET[0] <= pe <= TRAIN_PECLET[-1]
        where = "inside" if inside else "outside"
        ax.set_title(f"Error vs elements, Pe = {pe} ({where} training range)")
        ax.set_xlabel("number of elements $N$")
        ax.set_ylabel(r"$\|u_h - u\|_{L^2}$")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=9, loc="lower left")

    fig.tight_layout()
    return fig


def parse_args(argv=None):
    return create_parser(__doc__).parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    phi, y = training_set(TRAIN_PECLET)
    coef = fit_ridge(phi, y)
    rmse = np.sqrt(np.mean((phi @ coef - y) ** 2))
    print(f"training RMSE of log10 density: {rmse:.3e} ({y.size} samples)")

    curves_by_pe = {}
    for pe in TEST_PECLET:
        curves = error_curves(pe, coef)
        for name, err in curves.items():
            print(
                f"Pe = {pe:5d}  {name:26s} L2 error N=20: {err[2]:.2e}, "
                f"N=80: {err[6]:.2e}, N=320: {err[-1]:.2e}"
            )
        if pe != TEST_PECLET[0]:
            curves_by_pe[pe] = curves

    fig = make_figure(coef, curves_by_pe)
    finish_figures(
        {"adaptive_mesh_sizing.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
