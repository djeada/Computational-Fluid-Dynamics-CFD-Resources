"""Galerkin finite elements for the 1D Poisson equation with linear (P1) and quadratic (P2) elements.

Solves -u'' = f on (0, 1) with u(0) = u(1) = 0 for the manufactured solution
u(x) = exp(x) sin(pi x). Element stiffness matrices and load vectors are built
on a reference element with Gauss quadrature and assembled into a sparse
global system. The script plots the basis functions, a coarse-mesh solution
against the exact one, and the L2 and H1 errors under mesh refinement, which
fall as h^(p+1) and h^p.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

DOMAIN_LENGTH = 1.0  # L [-]
N_GAUSS = 6  # Gauss points per element, exact for polynomials of degree 11
N_COARSE = 4  # elements in the solution panel
N_REFINE = (2, 4, 8, 16, 32, 64, 128)  # element counts of the convergence study

GAUSS_X, GAUSS_W = np.polynomial.legendre.leggauss(N_GAUSS)
GAUSS_XI = 0.5 * (GAUSS_X + 1.0)  # points on the reference element [0, 1]
GAUSS_WI = 0.5 * GAUSS_W  # weights on [0, 1]


def exact_solution(x):
    return np.exp(x) * np.sin(np.pi * x)


def exact_derivative(x):
    return np.exp(x) * (np.sin(np.pi * x) + np.pi * np.cos(np.pi * x))


def source(x):
    """f = -u'' for the manufactured solution."""
    return -np.exp(x) * (
        (1.0 - np.pi**2) * np.sin(np.pi * x) + 2.0 * np.pi * np.cos(np.pi * x)
    )


def shape_functions(xi, degree):
    """Lagrange shape functions and their xi-derivatives on [0, 1].

    Local nodes are xi = 0, 1 for degree 1 and xi = 0, 1/2, 1 for degree 2.
    Returns arrays of shape (degree + 1, len(xi)).
    """
    xi = np.asarray(xi, dtype=float)
    if degree == 1:
        n = np.array([1.0 - xi, xi])
        dn = np.array([-np.ones_like(xi), np.ones_like(xi)])
    elif degree == 2:
        n = np.array(
            [
                2.0 * (xi - 0.5) * (xi - 1.0),
                4.0 * xi * (1.0 - xi),
                2.0 * xi * (xi - 0.5),
            ]
        )
        dn = np.array([4.0 * xi - 3.0, 4.0 - 8.0 * xi, 4.0 * xi - 1.0])
    else:
        raise ValueError("degree must be 1 or 2")
    return n, dn


def element_matrices(xa, xb, degree, f=source):
    """Element stiffness matrix K^e and load vector F^e on [xa, xb]."""
    h = xb - xa
    n, dn = shape_functions(GAUSS_XI, degree)
    dphi = dn / h  # d/dx = (1/h) d/dxi
    x = xa + h * GAUSS_XI
    k_e = (dphi * GAUSS_WI) @ dphi.T * h
    f_e = (n * GAUSS_WI) @ f(x) * h
    return k_e, f_e


def mesh(n_elements, degree, length=DOMAIN_LENGTH):
    """Global node coordinates and element connectivity (local node order)."""
    vertices = np.linspace(0.0, length, n_elements + 1)
    if degree == 1:
        connectivity = np.column_stack(
            [np.arange(n_elements), np.arange(1, n_elements + 1)]
        )
        return vertices, vertices, connectivity
    nodes = np.linspace(0.0, length, 2 * n_elements + 1)
    e = np.arange(n_elements)
    connectivity = np.column_stack([2 * e, 2 * e + 1, 2 * e + 2])
    return vertices, nodes, connectivity


def assemble(n_elements, degree, f=source):
    """Assemble the global stiffness matrix and load vector."""
    vertices, nodes, connectivity = mesh(n_elements, degree)
    k = lil_matrix((nodes.size, nodes.size))
    rhs = np.zeros(nodes.size)
    for e, dofs in enumerate(connectivity):
        k_e, f_e = element_matrices(vertices[e], vertices[e + 1], degree, f)
        k[np.ix_(dofs, dofs)] += k_e
        rhs[dofs] += f_e
    return k.tocsr(), rhs, vertices, nodes, connectivity


def solve(n_elements, degree, f=source, left=0.0, right=0.0):
    """Solve with Dirichlet values u(0) = left, u(L) = right.

    The boundary unknowns are eliminated: their columns move to the
    right-hand side and their rows are dropped.
    """
    k, rhs, vertices, nodes, connectivity = assemble(n_elements, degree, f)
    u = np.zeros(nodes.size)
    u[0], u[-1] = left, right
    interior = np.arange(1, nodes.size - 1)
    rhs_i = rhs[interior] - k[interior][:, [0, nodes.size - 1]] @ u[[0, -1]]
    u[interior] = spsolve(k[interior][:, interior].tocsc(), rhs_i)
    return vertices, nodes, connectivity, u


def evaluate(vertices, connectivity, u, degree, points_per_element=40):
    """Sample u_h finely inside every element for plotting."""
    xi = np.linspace(0.0, 1.0, points_per_element)
    n, _ = shape_functions(xi, degree)
    xs, us = [], []
    for e, dofs in enumerate(connectivity):
        xs.append(vertices[e] + (vertices[e + 1] - vertices[e]) * xi)
        us.append(u[dofs] @ n)
    return np.concatenate(xs), np.concatenate(us)


def errors(vertices, connectivity, u, degree):
    """L2 norm of u - u_h and H1 seminorm of u - u_h by Gauss quadrature."""
    n, dn = shape_functions(GAUSS_XI, degree)
    l2, h1 = 0.0, 0.0
    for e, dofs in enumerate(connectivity):
        h = vertices[e + 1] - vertices[e]
        x = vertices[e] + h * GAUSS_XI
        uh = u[dofs] @ n
        duh = u[dofs] @ dn / h
        l2 += h * np.sum(GAUSS_WI * (uh - exact_solution(x)) ** 2)
        h1 += h * np.sum(GAUSS_WI * (duh - exact_derivative(x)) ** 2)
    return np.sqrt(l2), np.sqrt(h1)


def convergence(degree, n_values=N_REFINE):
    """Mesh sizes and (L2, H1) errors for a refinement sequence."""
    result = np.array(
        [errors(*_drop_nodes(solve(n, degree)), degree) for n in n_values]
    )
    return 1.0 / np.array(n_values), result[:, 0], result[:, 1]


def _drop_nodes(solution):
    vertices, _, connectivity, u = solution
    return vertices, connectivity, u


def observed_orders(h, err):
    return np.log(err[:-1] / err[1:]) / np.log(h[:-1] / h[1:])


def _plot_basis(ax, degree, n_elements, colors):
    vertices, nodes, connectivity = mesh(n_elements, degree)
    for i in range(nodes.size):
        coeff = np.zeros(nodes.size)
        coeff[i] = 1.0
        support = np.nonzero((connectivity == i).any(axis=1))[0]
        x, phi = evaluate(
            vertices[support[0] : support[-1] + 2], connectivity[support], coeff, degree
        )
        style = "-" if degree == 1 or i % 2 == 0 else "--"
        ax.plot(x, phi, style, color=colors[i % len(colors)], linewidth=2)
    ax.plot(vertices, np.zeros_like(vertices), "ks", markersize=7, label="vertices")
    if degree == 2:
        ax.plot(nodes[1::2], np.zeros(n_elements), "ko", markersize=6, fillstyle="none")
    ax.set_ylim(-0.25, 1.15)
    ax.set_xlabel("$x$ [-]", fontsize=11)
    ax.set_ylabel(r"$\phi_i(x)$ [-]", fontsize=11)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)


def make_figure(coarse, studies):
    colors = plt.cm.tab10.colors
    fig, axes = plt.subplots(2, 2, figsize=(13, 9.5))

    _plot_basis(axes[0, 0], 1, N_COARSE, colors)
    axes[0, 0].set_title(f"(a) P1 hat functions, {N_COARSE} elements", fontsize=12)
    _plot_basis(axes[0, 1], 2, 2, colors)
    axes[0, 1].set_title(
        "(b) P2 functions, 2 elements (dashed: midpoint nodes)", fontsize=12
    )

    ax = axes[1, 0]
    x = np.linspace(0.0, DOMAIN_LENGTH, 400)
    ax.plot(x, exact_solution(x), "k-", linewidth=2.5, label=r"exact $e^x\sin\pi x$")
    for (degree, sol), color in zip(coarse.items(), (colors[0], colors[1])):
        vertices, nodes, connectivity, u = sol
        xs, us = evaluate(vertices, connectivity, u, degree)
        ax.plot(xs, us, "-", color=color, linewidth=1.8, label=f"P{degree}, $u_h$")
        marker, size = ("s", 8) if degree == 1 else ("o", 5)
        ax.plot(nodes, u, marker, color=color, markersize=size)
    ax.set_xlabel("$x$ [-]", fontsize=11)
    ax.set_ylabel("$u$ [-]", fontsize=11)
    ax.set_title(f"(c) Solution on {N_COARSE} elements", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="upper left")

    ax = axes[1, 1]
    for (degree, (h, l2, h1)), color in zip(studies.items(), (colors[0], colors[1])):
        p_l2 = observed_orders(h, l2)[-1]
        p_h1 = observed_orders(h, h1)[-1]
        ax.loglog(
            h, l2, "o-", color=color, label=f"P{degree}, $L^2$ (slope {p_l2:.2f})"
        )
        ax.loglog(
            h, h1, "s--", color=color, label=f"P{degree}, $H^1$ semi (slope {p_h1:.2f})"
        )
    ax.set_xlabel("Element size $h$ [-]", fontsize=11)
    ax.set_ylabel(r"Error norm of $u - u_h$ [-]", fontsize=11)
    ax.set_title("(d) Convergence: $h^{p+1}$ in $L^2$, $h^p$ in $H^1$", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=9.5, loc="lower right")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    for degree in (1, 2):
        k_e, _ = element_matrices(0.0, 1.0, degree, f=np.ones_like)
        print(f"P{degree} element stiffness matrix for h = 1:\n{np.round(k_e, 6)}")

    coarse = {degree: solve(N_COARSE, degree) for degree in (1, 2)}
    _, nodes, _, u = coarse[1]
    print(
        f"P1 on {N_COARSE} elements, max nodal error: "
        f"{np.max(np.abs(u - exact_solution(nodes))):.2e}"
    )
    studies = {degree: convergence(degree) for degree in (1, 2)}
    for degree, (h, l2, h1) in studies.items():
        print(f"P{degree}:")
        for n, a, b in zip(N_REFINE, l2, h1):
            print(f"  N = {n:4d}: L2 error {a:.3e}, H1 error {b:.3e}")
        print("  L2 orders:", " ".join(f"{p:.2f}" for p in observed_orders(h, l2)))
        print("  H1 orders:", " ".join(f"{p:.2f}" for p in observed_orders(h, h1)))

    fig = make_figure(coarse, studies)
    finish_figures(
        {"fem_1d_poisson.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
