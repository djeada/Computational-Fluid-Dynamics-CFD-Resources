# Finite Volume Method in CFD

The finite volume method (FVM) is one of the four common techniques for solving partial differential equations (PDEs) in computational fluid dynamics (CFD). The other techniques are finite difference methods (FDM), spectral methods, and finite element methods (FEM). This document provides an overview of FVM, highlighting its unique aspects and applications compared to other methods.

## Overview of Numerical Methods

### Finite Difference Methods (FDM)

In FDM, the domain is discretized into a grid or mesh of points, and differential operators in the PDEs are approximated by difference operators using values at these grid points. This method is effective for simple geometries and boundary conditions.

### Finite Volume Methods (FVM)

FVM also discretizes the domain but focuses on approximating integrals rather than derivatives. This method ensures the conservation of key physical quantities like mass, momentum, and energy by integrating the PDEs over control volumes. FVM is particularly advantageous in fluid dynamics for maintaining the integral conservation laws.

### Spectral Methods

Spectral methods differ from FDM and FVM as they do not discretize the domain into a grid. Instead, they express the solution as a sum of basis functions (e.g., Fourier series) and determine the coefficients of these basis functions to approximate the solution. Spectral methods are known for their high accuracy in smooth problems.

### Finite Element Methods (FEM)

FEM combines the local approximation approach of FDM and FVM with the solution space approximation of spectral methods. The domain is divided into elements, and the solution is approximated using polynomial basis functions within each element. FEM is versatile and effective for complex geometries and boundary conditions.

## Detailed Description of FVM

### Key Concepts in FVM

1. **Control Volume**: The domain is divided into small control volumes (cells) where the conservation laws are applied.
2. **Integral Form of PDEs**: The PDEs are integrated over each control volume, converting the differential equations into algebraic equations.
3. **Fluxes**: The method focuses on calculating the fluxes across the boundaries of each control volume, ensuring the conservation of physical quantities.

### Steps in FVM

1. **Define the Domain and Control Volumes**: 
    - Divide the domain into control volumes (e.g., hexahedral, tetrahedral cells in 3D).
    - Each control volume is associated with a node or cell center.

2. **Discretize the PDEs**:
    - Integrate the PDEs over each control volume.
    - Apply the divergence theorem to convert volume integrals into surface integrals involving fluxes.

3. **Calculate Fluxes**:
    - Determine the fluxes across the boundaries of each control volume.
    - Approximate the fluxes using interpolation schemes (e.g., central differencing, upwind schemes).

4. **Formulate the System of Equations**:
    - Write an equation for each control volume involving the fluxes and conserved quantities.
    - Assemble these equations into a global system of algebraic equations.

5. **Apply Boundary Conditions**:
    - Implement boundary conditions by modifying the flux calculations at the domain boundaries.

6. **Solve the System**:
    - Use numerical methods (e.g., Gauss-Seidel, Conjugate Gradient) to solve the system of linear equations for the unknown quantities.

### Example: Solving a 1D Convection-Diffusion Equation

Consider the 1D convection-diffusion equation $ \frac{\partial u}{\partial t} + v \frac{\partial u}{\partial x} = D \frac{\partial^2 u}{\partial x^2} $:

1. **Define Control Volumes**: 
    - Divide the domain into control volumes $ V_i $ centered at points $ x_i $.

2. **Integrate the PDE**:
    - Integrate over each control volume $ V_i $:
      $$
      \int_{V_i} \frac{\partial u}{\partial t} \, dV + \int_{V_i} v \frac{\partial u}{\partial x} \, dV = \int_{V_i} D \frac{\partial^2 u}{\partial x^2} \, dV
      $$

3. **Apply Divergence Theorem**:
    - Convert volume integrals to surface integrals:
      $$
      \frac{d}{dt} \int_{V_i} u \, dV + \int_{A_i} v u \cdot dA = \int_{A_i} D 
abla u \cdot dA
      $$

4. **Approximate Fluxes**:
    - Approximate the fluxes at the control volume faces using interpolation schemes.

5. **Formulate and Solve**:
    - Write the discretized equations for each control volume.
    - Solve the resulting system of equations for $ u $ at each control volume center.

## Further Reading

1. **Books**
    - "Computational Methods for Fluid Dynamics" by Joel H. Ferziger and Milovan Perić.
    - "Introduction to Computational Fluid Dynamics: The Finite Volume Method" by Versteeg and Malalasekera.

2. **Research Papers**
    - "A Finite Volume Method for the Prediction of Three-Dimensional Fluid Flow in Complex Ducts" by S.V. Patankar and D.B. Spalding.
    - "Numerical Heat Transfer and Fluid Flow" by S.V. Patankar.

3. **Online Resources**
    - Coursera and edX courses on Computational Fluid Dynamics and Finite Volume Method.
    - YouTube tutorials on Finite Volume Methods in CFD.
