# Finite Element Method in CFD

Four common techniques for solving partial differential equations (PDEs) in computational fluid dynamics (CFD) are finite difference methods (FDM), finite volume methods (FVM), spectral methods, and finite element methods (FEM). FEM is built on more abstract mathematical methods than FDM and FVM. To understand FEM, it's helpful to first introduce these other methods and highlight the key philosophical differences.

## Finite Difference Methods (FDM)

In FDM, we start by creating a mesh to discretize the domain into small discrete pieces. FDM approximates the differential operators as difference operators. The derivative, which is the slope of a function at a point, is approximated by taking the difference of the function at two nearby points. This method is straightforward and works well for simple geometries and boundary conditions.

## Finite Volume Methods (FVM)

FVM also starts with a mesh but approximates the integral rather than the derivative. This method allows for the conservation of important physical quantities such as mass, momentum, and energy by integrating over discrete volumes. FVM is particularly useful in fluid dynamics because it inherently ensures conservation laws are satisfied.

## Spectral Methods

Spectral methods differ from FDM and FVM as they don't break the domain into a mesh. Instead, they assume the solution is a sum of basis functions, such as Fourier series. The goal is to find the coefficients of these basis functions. Spectral methods do not approximate the operators since we can evaluate the derivative and integral of these basis functions exactly.

## Finite Element Methods (FEM)

FEM combines aspects of FVM and spectral methods. FEM approximates the solution space rather than the operators. It discretizes the domain into elements and approximates the solution within each element using simple polynomials. For example, the solution within each element might be approximated by a linear polynomial. We then solve for the coefficients of these polynomials to approximate the solution across the domain.

### Key Steps in FEM

1. **Mesh Generation**: Divide the domain into smaller elements (e.g., triangles, quadrilaterals).
2. **Selection of Basis Functions**: Choose polynomial basis functions (e.g., linear, quadratic) to approximate the solution within each element.
3. **Formulation of the Weak Form**: Convert the PDE into its weak form, which involves integrating the PDE against a test function and applying integration by parts.
4. **Assembly of the System of Equations**: Combine the contributions from each element to form a global system of equations.
5. **Solution of the System**: Solve the global system of equations to find the coefficients of the basis functions.
6. **Post-processing**: Interpret the results, which may involve visualization and further analysis.

## Lattice Boltzmann Method (LBM)

While FEM, FVM, and FDM solve the Navier-Stokes equations describing a continuous vector field, the Lattice Boltzmann Method (LBM) solves the Boltzmann equation for single particles. LBM accounts for the particle nature of fluids and can handle complex boundary conditions and flows with ease. It provides a different perspective by averaging particle velocities to obtain a macroscopic fluid velocity.

## Further Reading

1. **Books**
    - "The Finite Element Method: Linear Static and Dynamic Finite Element Analysis" by Thomas J.R. Hughes.
    - "Computational Fluid Dynamics: Principles and Applications" by Jiyuan Tu, Guan Heng Yeoh, and Chaoqun Liu.

2. **Research Papers**
    - "Finite Element Methods for Fluid Dynamics" by O.C. Zienkiewicz and R.L. Taylor.
    - "A Review of the Lattice Boltzmann Method for Fluid-Flow Simulation" by Succi et al.

3. **Online Resources**
    - Coursera and edX courses on Computational Fluid Dynamics and Finite Element Analysis.
    - GitHub repositories with implementations of FEM in CFD projects.
