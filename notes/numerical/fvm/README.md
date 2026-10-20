# Finite Volume Method

The finite volume method integrates each conservation law over the cells of a mesh and balances the change of every cell average against the fluxes through its faces, so mass, momentum and energy are conserved exactly on any mesh. These notes start from the integral balance and the 1D convection–diffusion equation, extend the discretization to unstructured 3D meshes, treat the choice of convective face values from upwinding to TVD limiters, and end with the two algorithms that turn the discrete equations into a flow solver: pressure–velocity coupling for incompressible flow and Riemann solvers for compressible flow.

## Table of Contents

### 1. [The Finite Volume Method](./intro.md)

Integral form and cell averages, cell-centred and vertex-centred arrangements, the conservation property, the 1D steady convection–diffusion equation with central and upwind coefficients, the cell Péclet number and the boundedness criterion.

### 2. [Finite Volume Discretization on General Meshes](./discretization.md)

Face area vectors and owner–neighbour storage, Green–Gauss and least-squares gradients, non-orthogonal and skewness corrections, source linearization, unsteady terms, sparse-matrix assembly and boundary faces.

### 3. [Convection Schemes](./convection_schemes.md)

Upwind, central, hybrid, power-law, linear-upwind and QUICK face values, numerical and false diffusion, Godunov's order barrier, TVD limiters and the Sweby diagram, the NVD and the convection boundedness criterion, and deferred correction.

### 4. [Pressure–Velocity Coupling](./pressure_velocity_coupling.md)

Staggered and collocated grids, Rhie–Chow interpolation, and the SIMPLE, SIMPLEC, PISO and projection algorithms for incompressible flow.

### 5. [Riemann Solvers and Godunov Methods](./riemann_solvers.md)

Godunov's method for the Euler equations, the exact Riemann solver, the approximate solvers of Roe, HLL and HLLC, and second-order MUSCL reconstruction.
