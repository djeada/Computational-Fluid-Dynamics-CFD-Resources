# Numerical Methods for CFD

These notes cover how the equations of fluid flow are turned into numbers that can be trusted. They start with what a CFD calculation is and the workflow from geometry to result, then develop the three main discretization families (finite differences, finite volumes and finite elements), the solution of the resulting algebraic systems, stability and time integration, and the verification and validation that establish how accurate a result is. Two further families, lattice Boltzmann and high-order spectral and discontinuous Galerkin methods, follow, and the last part turns to data-driven methods that reduce the cost of many repeated simulations: proper orthogonal decomposition, reduced-order models and surrogate models. The physics behind the equations is in [`notes/fluid_mechanics/`](../fluid_mechanics/), hands-on work with solvers and meshers in [`practice/`](../../practice/), and machine-learning approaches in [`notes/machine_learning/`](../machine_learning/).

## Prerequisites

- Calculus of several variables: partial derivatives, Taylor series, the divergence theorem.
- Linear algebra: matrices, eigenvalues, linear systems, the singular value decomposition (for the data-driven part).
- Basic fluid mechanics: conservation of mass and momentum, viscosity, the Reynolds number ([Governing Equations of Fluid Mechanics](../fluid_mechanics/governing_equations/README.md)).
- Some programming in Python, to run and modify the scripts in [`scripts/`](../../scripts/).

## Suggested Reading Order

1. CFD fundamentals: [Why CFD](./cfd/intro.md), [The Strategy of CFD](./cfd/cfd_process.md), [Governing Equations for CFD](./cfd/governing_equations.md) and [Boundary Conditions](./cfd/boundary_conditions.md).
2. Finite differences: [Finite Difference Method](./fdm/intro.md), then [Systematic Finite-Difference Discretization](./fdm/discretization.md).
3. Finite volumes: [The Finite Volume Method](./fvm/intro.md), [discretization](./fvm/discretization.md), [convection schemes](./fvm/convection_schemes.md), [pressure–velocity coupling](./fvm/pressure_velocity_coupling.md) and [Riemann solvers](./fvm/riemann_solvers.md).
4. Finite elements: [Finite Element Method](./fem/intro.md), then [the weak formulation](./fem/weak_formulation_pde.md).
5. Solving the discrete system: [Dealing with Nonlinearity](./cfd/dealing_with_nonlinearity.md), [Direct and Iterative Solvers](./cfd/direct_and_iterative_solvers.md) and [Iterative Convergence](./cfd/iterative_convergence.md).
6. Stability and time integration: [Numerical Stability](./cfd/numerical_stability.md) and [Time Integration](./cfd/time_integration.md).
7. Verification: [Verification and Validation](./cfd/verification_and_validation.md), with [Turbulence Modeling in CFD](./cfd/turbulence_modeling.md) for the main source of modelling error.
8. Advanced discretizations: [lattice Boltzmann methods](./lattice_boltzmann/README.md) and [high-order methods](./high_order/README.md).
9. Data-driven methods: [proper orthogonal decomposition](./pod/README.md), [reduced-order models](./rom/README.md) and [surrogate models](./surrogates/README.md).

## Contents

### CFD Fundamentals: [`cfd/`](./cfd/README.md)

| Note | What it covers |
| --- | --- |
| [Why CFD](./cfd/intro.md) | Why the Navier–Stokes equations need numerical solution, what a discrete solution and its error are, DNS cost scaling, the discretization families and the sources of error |
| [The Strategy of CFD](./cfd/cfd_process.md) | Continuous and discrete domains, the workflow from pre-processing to post-processing, and a 1D problem carried through every step including grid refinement |
| [Governing Equations for CFD](./cfd/governing_equations.md) | Conservation form of the compressible equations, incompressible flow and pressure, the generic transport equation, dimensionless groups and PDE classification |
| [Boundary Conditions](./cfd/boundary_conditions.md) | Dirichlet, Neumann and Robin conditions, characteristic counts, ghost points and ghost cells, incompressible flow boundaries, non-reflecting outflow and initial conditions |
| [Dealing with Nonlinearity](./cfd/dealing_with_nonlinearity.md) | Linearizing the discrete equations: Picard and Newton iteration, under-relaxation and their convergence |
| [Direct and Iterative Solvers](./cfd/direct_and_iterative_solvers.md) | Solving sparse linear systems: factorization, stationary iterations, Krylov methods, preconditioning and multigrid |
| [Iterative Convergence](./cfd/iterative_convergence.md) | Residuals and their normalization, convergence criteria and monitoring quantities of interest |
| [Numerical Stability](./cfd/numerical_stability.md) | Von Neumann analysis, the CFL condition and stability of discretized evolution equations |
| [Time Integration](./cfd/time_integration.md) | Explicit and implicit time-stepping schemes, their accuracy and stability, and dual time stepping |
| [Verification and Validation](./cfd/verification_and_validation.md) | Order-of-accuracy tests, manufactured solutions, Richardson extrapolation and GCI, validation against experiments with ASME V\&V 20 |
| [Turbulence Modeling in CFD](./cfd/turbulence_modeling.md) | RANS, LES and hybrid models as used inside a CFD workflow, wall treatment and model choice |

### Finite Difference Method: [`fdm/`](./fdm/README.md)

| Note | What it covers |
| --- | --- |
| [Finite Difference Method](./fdm/intro.md) | Difference quotients from Taylor series, truncation error, consistency and order of accuracy |
| [Systematic Finite-Difference Discretization](./fdm/discretization.md) | Deriving difference formulas of arbitrary order and assembling the discrete system for a model problem |

### Finite Volume Method: [`fvm/`](./fvm/README.md)

| Note | What it covers |
| --- | --- |
| [The Finite Volume Method](./fvm/intro.md) | Integral conservation laws on control volumes, face fluxes and discrete conservation |
| [Finite Volume Discretization on General Meshes](./fvm/discretization.md) | Discretizing diffusion, convection, sources and unsteady terms on structured and unstructured meshes |
| [Convection Schemes for Finite Volume Methods](./fvm/convection_schemes.md) | Upwind, central, hybrid and QUICK schemes, boundedness, TVD schemes and flux limiters |
| [Pressure–Velocity Coupling](./fvm/pressure_velocity_coupling.md) | Staggered and collocated grids, Rhie–Chow interpolation, SIMPLE, SIMPLEC, PISO and projection methods |
| [Riemann Solvers and Godunov Methods](./fvm/riemann_solvers.md) | Godunov's method, the exact Riemann solver, Roe, HLL and HLLC fluxes and MUSCL reconstruction |

### Finite Element Method: [`fem/`](./fem/README.md)

| Note | What it covers |
| --- | --- |
| [Finite Element Method](./fem/intro.md) | Weighted residuals, basis functions, element assembly and error estimates |
| [Weak Formulation of a Reaction–Diffusion Equation](./fem/weak_formulation_pde.md) | Deriving and discretizing the weak form of a reaction–diffusion equation |

### High-Order Methods: [`high_order/`](./high_order/README.md)

| Note | What it covers |
| --- | --- |
| [High-Order Methods: Spectral and Discontinuous Galerkin](./high_order/intro.md) | Spectral accuracy, Fourier and Chebyshev methods, and discontinuous Galerkin discretizations on unstructured meshes |

### Lattice Boltzmann Method: [`lattice_boltzmann/`](./lattice_boltzmann/README.md)

| Note | What it covers |
| --- | --- |
| [Introduction to the Lattice Boltzmann Method](./lattice_boltzmann/intro.md) | The mesoscopic approach to fluid flow and where it fits among CFD methods |
| [From Newton to Navier–Stokes](./lattice_boltzmann/from_newton_to_nse.md) | The hierarchy from molecular dynamics through kinetic theory to continuum equations |
| [The Boltzmann Equation](./lattice_boltzmann/boltzmann_equation.md) | The distribution function, the Boltzmann equation, collision operators and the equilibrium distribution |
| [From Boltzmann to Lattice Boltzmann](./lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md) | Discretizing velocity, space and time, lattices such as D2Q9, and the recovery of the Navier–Stokes equations |
| [The Lattice Boltzmann Algorithm](./lattice_boltzmann/lattice_boltzmann_algorithm.md) | Streaming and collision, BGK relaxation, boundary conditions and the relation between relaxation time and viscosity |
| [The Lattice Boltzmann Method in Practice](./lattice_boltzmann/practical_lbm.md) | Units, stability limits, boundary treatment and practical use |

### Proper Orthogonal Decomposition: [`pod/`](./pod/README.md)

| Note | What it covers |
| --- | --- |
| [Proper Orthogonal Decomposition](./pod/pod_intro.md) | The optimal-basis problem, energy content of modes and uses of POD in flow analysis |
| [Two-Point POD: A Worked Example](./pod/derivation_in_2d.md) | The POD eigenvalue problem derived for a simple two-dimensional case |
| [POD for N Points](./pod/derivation_in_n_dim.md) | The general derivation with snapshot matrices and the correlation matrix |
| [The Method of Snapshots](./pod/snapshot_pod.md) | The method of snapshots for fields with many more points than snapshots |
| [POD and the Singular Value Decomposition](./pod/pod_vs_svd.md) | Computing POD through the singular value decomposition and the relation between the two |
| [Gappy POD](./pod/gappy_pod.md) | Reconstructing fields from incomplete data with a POD basis |

### Reduced-Order Models: [`rom/`](./rom/README.md)

| Note | What it covers |
| --- | --- |
| [Reduced-Order Modeling](./rom/rom.md) | Offline–online decomposition, projection-based and data-driven reduced models |
| [Parametrized Variational Problems](./rom/parameterized_variational_problems.md) | The parameterized weak formulation that reduced-basis methods start from |
| [Truth Discretization](./rom/discretization_techniques.md) | The high-fidelity Galerkin approximation that the reduced model approximates in turn |
| [Reduced Basis Approximation](./rom/reduced_basis_approximation.md) | The solution manifold, greedy and POD basis construction and error bounds |
| [POD-Galerkin Projection](./rom/pod_galerkin_projection.md) | Projecting finite-volume Navier–Stokes equations onto POD modes |
| [Dynamic Mode Decomposition as a Reduced-Order Model](./rom/dmd.md) | Extracting modes with single frequencies and growth rates from snapshot sequences |

### Surrogate Models: [`surrogates/`](./surrogates/README.md)

| Note | What it covers |
| --- | --- |
| [Surrogate Models in CFD](./surrogates/intro.md) | Why surrogates are needed, the main model families and how they are built and validated |
| [One-Stage Sampling Plans](./surrogates/one_stage_sampling.md) | Space-filling designs fixed before any evaluation: Latin hypercubes, low-discrepancy sequences |
| [Adaptive Sampling](./surrogates/adaptive_sampling.md) | Adding samples sequentially where the surrogate is uncertain or the optimum is likely |
| [Radial Basis Function Interpolation](./surrogates/radial_basis_functions.md) | RBF interpolation, kernels and the choice of shape parameter |
| [Kriging](./surrogates/kriging.md) | Gaussian-process regression as the best linear unbiased predictor, correlation functions and hyperparameters |
| [Hierarchical Kriging and Variable-Fidelity Modelling](./surrogates/hierarchical_kriging.md) | Variable-fidelity surrogates that combine cheap and expensive simulations |

## Notation

The notes use the following symbols unless a note states otherwise.

| Symbol | Meaning |
| --- | --- |
| $\phi$ | Generic transported variable, or its discrete approximation |
| $\mathbf{u} = (u, v, w)$ | Velocity vector and its Cartesian components |
| $p$ | Pressure |
| $\rho$ | Density |
| $\mu$, $\nu = \mu/\rho$ | Dynamic and kinematic viscosity |
| $\Gamma$ | Diffusion coefficient of $\phi$ |
| $T$, $k$, $c_p$ | Temperature, thermal conductivity, specific heat at constant pressure |
| $c$, $\gamma$ | Speed of sound, ratio of specific heats |
| $\mathbf{U}$, $\mathbf{F}$ | Vector of conserved variables and flux vector of a conservation law |
| $\Delta x$ or $h$ | Grid spacing or representative cell size |
| $\Delta t$ | Time step |
| $C = u\Delta t/\Delta x$ | CFL (Courant) number |
| $i$, $j$, $k$ | Node or cell indices; $P$, $E$, $W$, $N$, $S$ denote a cell and its neighbours in compass notation |
| $i \pm 1/2$ | Faces between cells $i$ and $i \pm 1$ |
| $n$ | Time level, as a superscript: $\phi_i^n \approx \phi(x_i, t^n)$ |
| $N$ | Number of grid points, cells or unknowns |
| $A\boldsymbol{\phi} = \mathbf{b}$ | Discrete linear system; $\mathbf{r} = \mathbf{b} - A\boldsymbol{\phi}$ its residual |
| $p$ (in error estimates), $r$ | Order of accuracy; grid refinement ratio |
| $Re$, $Ma$, $Pe$ | Reynolds, Mach and Péclet numbers |
| $\boldsymbol{\Phi}$, $a_k(t)$ | POD modes and their temporal coefficients |
| $f_i$, $\tau$ | Lattice Boltzmann distribution functions and relaxation time |
