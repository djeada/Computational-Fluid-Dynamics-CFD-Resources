# Lattice Boltzmann Method

The lattice Boltzmann method simulates incompressible and weakly compressible flow by evolving particle distribution functions on a uniform lattice instead of discretising the Navier–Stokes equations. These notes start from the kinetic theory that justifies it, derive the lattice Boltzmann equation from the Boltzmann equation, describe the algorithm with its boundary conditions and collision models, and end with unit conversion, parameter choice, a complete NumPy implementation and performance. Read them in order; each note assumes the previous ones.

## Table of Contents

### 1. [Introduction to the Lattice Boltzmann Method](./intro.md)

Why a mesoscopic method works for continuum flows, the Knudsen number and the micro, meso and macro levels of description, the weakly compressible equations that LBM solves, and a comparison with finite-volume Navier–Stokes solvers.

### 2. [From Newton to Navier–Stokes](./from_newton_to_nse.md)

The hierarchy from molecular dynamics through the Liouville and Boltzmann equations to continuum equations, the distribution function, and the moments that define density, momentum, energy, stress and heat flux.

### 3. [The Boltzmann Equation](./boltzmann_equation.md)

The collision operator, collision invariants and conservation laws, the H-theorem and the Maxwell–Boltzmann equilibrium, the BGK model, and the Chapman–Enskog expansion leading to $\nu = c_s^2(\tau - \Delta t/2)$ in lattice form.

### 4. [From Boltzmann to Lattice Boltzmann](./from_boltzmann_to_lattice_boltzmann.md)

Hermite expansion and Gauss–Hermite quadrature in velocity space, the D1Q3, D2Q9, D3Q15, D3Q19 and D3Q27 lattices, the second-order equilibrium, and integration along characteristics with the trapezoidal variable change.

### 5. [The Lattice Boltzmann Algorithm](./lattice_boltzmann_algorithm.md)

The collide–stream algorithm, bounce-back, moving-wall, Zou–He and outflow boundaries, Guo forcing, stability limits, and the MRT and TRT collision operators.

### 6. [The Lattice Boltzmann Method in Practice](./practical_lbm.md)

Conversion between physical and lattice units with worked examples, choosing $\tau$ and the Mach number, a lid-driven cavity in NumPy, memory and throughput, and whether LBM is meshless.
