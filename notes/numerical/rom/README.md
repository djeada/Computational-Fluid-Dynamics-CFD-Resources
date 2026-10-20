# Reduced-Order Modeling

These notes cover reduced-order models (ROMs) that replace a high-fidelity CFD model with millions of unknowns by a system of tens or hundreds of unknowns, for problems that must be solved many times or in real time. They start with an overview of the projection-based and data-driven families, then set up parametrized variational problems and their truth discretization, develop the certified reduced basis method, apply POD-Galerkin projection to the Navier–Stokes equations, and end with dynamic mode decomposition as a data-driven linear ROM. The POD machinery the notes rely on is in [`notes/numerical/pod/`](../pod/pod_intro.md), and the machine-learning alternatives are in [`notes/machine_learning/`](../../machine_learning/README.md).

## Table of Contents

### 1. [Reduced-Order Modeling](./rom.md)

Problem statement, Galerkin and least-squares Petrov–Galerkin projection, data-driven ROMs, the offline–online split, Kolmogorov $n$-width, hyper-reduction with EIM and DEIM, error estimation, stability and closure, and a comparison of ROM families.

### 2. [Parametrized Variational Problems](./parameterized_variational_problems.md)

Hilbert spaces, parametrized bilinear and linear forms, coercivity, continuity and Lax–Milgram, inf-sup stability, affine parameter dependence, and the thermal block and advection–diffusion examples.

### 3. [Truth Discretization](./discretization_techniques.md)

The high-fidelity Galerkin discretization, its algebraic form and inner-product matrices, Galerkin orthogonality and Céa's lemma, finite element, spectral, DG and finite volume truth spaces, and the assumption that the truth error is negligible.

### 4. [Reduced Basis Approximation](./reduced_basis_approximation.md)

The solution manifold, reduced spaces by POD and weak greedy, offline–online decomposition, residual-based error and output bounds, coercivity lower bounds, stable evaluation of the dual norm, and a certified thermal block example.

### 5. [POD-Galerkin Projection](./pod_galerkin_projection.md)

The quadratic Galerkin system for incompressible Navier–Stokes, lifting functions, pressure treatment with supremizers or a pressure Poisson equation, finite volume implementation, instability and closure, and the cylinder wake mean-field model.

### 6. [Dynamic Mode Decomposition as a Reduced-Order Model](./dmd.md)

DMD as a fitted linear ROM in POD coordinates, its relation to Galerkin projection, Koopman and stability analysis, mode selection, optimized DMD and DMD with control, practical choices of rank, sampling and noise correction, and the comparison with POD and SPOD.
