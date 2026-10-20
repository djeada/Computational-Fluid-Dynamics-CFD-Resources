# Finite Element Methods

The finite element method approximates the solution of a boundary-value problem by piecewise polynomials on a mesh, starting from the weak form of the equation. These notes cover the Galerkin method, basis functions and assembly, error estimates, the function spaces and well-posedness theory, and the extra requirements of incompressible flow.

## Table of Contents

### 1. [Finite Element Method](./intro.md)

Strong and weak forms of the 1D Poisson equation, the Galerkin method, linear and quadratic basis functions, element matrices and assembly, essential and natural boundary conditions, Céa's lemma and convergence rates, triangles in 2D, and inf–sup stable and stabilized elements for incompressible flow.

### 2. [Weak Formulation of a Reaction–Diffusion Equation](./weak_formulation_pde.md)

The Sobolev spaces $H^1$ and $H^1_0$, Green's identity with Dirichlet and Neumann boundaries, well-posedness by the Lax–Milgram lemma, the semi-discrete system with mass and stiffness matrices, and the θ-scheme in time.
