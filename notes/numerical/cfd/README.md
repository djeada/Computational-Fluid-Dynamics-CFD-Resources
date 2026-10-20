# CFD Fundamentals

These notes cover what is common to every CFD method, whatever the discretization: why numerical solution is needed and what it delivers, the workflow from geometry to result, the governing equations in the form the numerics needs, boundary and initial conditions, the solution of the large nonlinear algebraic systems that discretization produces, stability and time integration, turbulence modelling as part of a CFD calculation, and the verification and validation that establish how far a result can be trusted. The discretization families themselves are in the sibling folders [`fdm/`](../fdm/README.md), [`fvm/`](../fvm/README.md) and [`fem/`](../fem/README.md); the overview of all numerical-methods notes is in [Numerical Methods for CFD](../README.md).

## Table of Contents

### 1. [Why CFD](./intro.md)

Why the Navier–Stokes equations need numerical solution, what a discrete solution and its error are, the $Re^{9/4}$ cost of DNS, a comparison of FDM, FVM, FEM, spectral/DG and lattice Boltzmann methods, and the five sources of error.

### 2. [The Strategy of CFD](./cfd_process.md)

Continuous and discrete domains, pre-processing, discretization, solution and post-processing, and a 1D problem carried through every step, ending with a grid-refinement study.

### 3. [Governing Equations for CFD](./governing_equations.md)

The integral and differential conservation form of the compressible Navier–Stokes equations, incompressible flow with pressure as a Lagrange multiplier, the generic transport equation, $Re$, $Ma$ and $Pe$, and the classification of PDEs into elliptic, parabolic and hyperbolic types.

### 4. [Boundary Conditions](./boundary_conditions.md)

Dirichlet, Neumann and Robin conditions, how many conditions hyperbolic systems need at inflow and outflow, ghost points and ghost cells, physical boundaries for incompressible flow, non-reflecting outflow conditions and initial conditions.

### 5. [Dealing with Nonlinearity](./dealing_with_nonlinearity.md)

Linearizing the discrete equations by Picard and Newton iteration, under-relaxation and their convergence.

### 6. [Direct and Iterative Solvers](./direct_and_iterative_solvers.md)

Direct factorization, stationary iterations, Krylov methods, preconditioning and multigrid for the sparse linear systems of CFD.

### 7. [Iterative Convergence](./iterative_convergence.md)

Residuals and their normalization, convergence criteria, and monitoring the quantities of interest.

### 8. [Numerical Stability](./numerical_stability.md)

Von Neumann stability analysis, the CFL condition and the stability of discretized evolution equations.

### 9. [Time Integration](./time_integration.md)

Explicit and implicit time-stepping schemes, their order and stability regions, and the treatment of stiff problems.

### 10. [Verification and Validation](./verification_and_validation.md)

Order-of-accuracy tests and the method of manufactured solutions, Richardson extrapolation and the grid convergence index, validation against experiments with ASME V\&V 20, and the credibility hierarchy.

### 11. [Turbulence Modeling in CFD](./turbulence_modeling.md)

RANS, LES and hybrid approaches as used inside a CFD workflow, near-wall treatment and how to choose a model.
