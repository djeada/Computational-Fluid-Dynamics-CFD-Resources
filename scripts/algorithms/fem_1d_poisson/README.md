# 1D Poisson Equation With Finite Elements

This script solves the 1D Poisson equation $-u'' = f$ on $(0, 1)$ with homogeneous Dirichlet conditions by the Galerkin finite element method with linear (P1) and quadratic (P2) Lagrange elements, and confirms the a priori error estimates: the $L^2$ error falls as $h^{p+1}$ and the $H^1$ error as $h^p$. It uses the manufactured solution $u(x) = e^x\sin(\pi x)$, so every error is measured against the exact answer.

## Overview

- Builds element stiffness matrices and load vectors on the reference element $[0, 1]$ with six-point Gauss quadrature.
- Assembles them into a sparse global matrix through the element connectivity, eliminates the two Dirichlet nodes and solves with `scipy.sparse.linalg.spsolve`.
- Plots the P1 hat functions on four elements and the P2 vertex and midpoint functions on two elements.
- Compares the P1 and P2 solutions on four elements with the exact solution.
- Refines from 2 to 128 elements and plots the $L^2$ norm and $H^1$ seminorm of the error with their observed orders.

## Mathematical Background

The weak form is: find $u \in H^1_0(0, 1)$ with

```math
\int_0^1 u'\,v'\,dx = \int_0^1 f\,v\,dx \quad \text{for all } v \in H^1_0(0, 1),
\qquad f = -u'' = -e^x\left[(1 - \pi^2)\sin\pi x + 2\pi\cos\pi x\right]
```

With $u_h = \sum_j U_j\phi_j$ in the space of continuous piecewise polynomials of degree $p$, the Galerkin equations are $KU = F$ with $`K_{ij} = \int\phi_i'\phi_j'\,dx`$ and $`F_i = \int f\phi_i\,dx`$. On an element of length $h$ mapped from $\xi \in [0, 1]$, the P2 shape functions with nodes at $\xi = 0, 1/2, 1$ are

```math
N_0 = 2(\xi - \tfrac{1}{2})(\xi - 1), \qquad N_{1/2} = 4\xi(1 - \xi), \qquad N_1 = 2\xi(\xi - \tfrac{1}{2})
```

and the element stiffness matrices are

```math
K^e_{P1} = \frac{1}{h}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix},
\qquad
K^e_{P2} = \frac{1}{3h}\begin{pmatrix} 7 & -8 & 1 \\ -8 & 16 & -8 \\ 1 & -8 & 7 \end{pmatrix}
```

For smooth $u$ the errors satisfy $`\|u - u_h\|_{L^2} \le C h^{p+1}|u|_{H^{p+1}}`$ and $`|u - u_h|_{H^1} \le C h^p |u|_{H^{p+1}}`$. In 1D the P1 nodal values are exact when the load integrals are exact, because the Green's function of $-d^2/dx^2$ with a source at a node is itself piecewise linear.

## Implementation

- `shape_functions(xi, degree)` returns the Lagrange shape functions and their derivatives on the reference element.
- `element_matrices(xa, xb, degree, f)` integrates $K^e$ and $F^e$ with the Gauss rule `GAUSS_XI`, `GAUSS_WI`.
- `mesh(n_elements, degree)` returns vertices, node coordinates and connectivity; P2 midpoints get the odd global numbers.
- `assemble` adds the element contributions into a `lil_matrix`; `solve(n_elements, degree, f, left, right)` eliminates the Dirichlet nodes and solves.
- `evaluate` samples $u_h$ inside each element for plotting, and `errors` integrates the $L^2$ and $H^1$ errors element by element.
- `convergence(degree, n_values)` runs the refinement study over `N_REFINE`.

## Usage

```bash
python main.py                          # print the error tables and show the figure
python main.py --no-show --output .     # save fem_1d_poisson.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints the reference stiffness matrices (for $h = 1$ the P2 entries are $7/3$, $-8/3$, $1/3$ and $16/3$) and a maximum P1 nodal error of $8.9 \times 10^{-16}$ on four elements. On 128 elements the P1 errors are $8.53 \times 10^{-5}$ in $L^2$ and $3.45 \times 10^{-2}$ in $H^1$, the P2 errors $1.04 \times 10^{-7}$ and $8.60 \times 10^{-5}$. The observed orders are 2.00 and 1.00 for P1 and 3.00 and 2.00 for P2.

![Finite element basis functions, solution and convergence](fem_1d_poisson.png)

Panels (a) and (b) show the basis: each P1 hat function is 1 at its node and 0 at all others, and the P2 midpoint functions (dashed) live on a single element. Panel (c) shows that the P1 solution on four elements interpolates the exact solution at the nodes while P2 is hard to distinguish from it. Panel (d) shows the four error curves with slopes $p + 1$ and $p$.

## Related Notes

- [Finite Element Method](../../../notes/numerical/fem/intro.md)
- [Weak Formulation of a Reaction-Diffusion Equation](../../../notes/numerical/fem/weak_formulation_pde.md)
