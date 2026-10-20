# Finite Difference Methods

Finite differences replace derivatives by difference quotients of grid values. These notes derive the standard formulas from Taylor series, assemble boundary-value problems in 1D and 2D, construct stencils of any order systematically, and analyse their dispersion and dissipation with the modified wavenumber.

## Table of Contents

### 1. [Finite Difference Method](./intro.md)

Grid functions, forward, backward and central differences from Taylor series, truncation error and order, round-off, the 1D Poisson problem as a tridiagonal system, the five-point Laplacian, non-uniform grids, and consistency, stability and convergence.

### 2. [Systematic Finite-Difference Discretization](./discretization.md)

The method of undetermined coefficients and Taylor tables, Fornberg's algorithm, a marching problem, compact (Padé) schemes, modified wavenumber analysis, and the points per wavelength each scheme needs.
