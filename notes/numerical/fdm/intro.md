# Finite Difference Method in CFD

Finite difference methods (FDM) are one of the four common techniques for solving partial differential equations (PDEs) in computational fluid dynamics (CFD). The other techniques are finite volume methods (FVM), spectral methods, and finite element methods (FEM). This document will describe the fundamentals of FDM, comparing it with these other methods to highlight its unique aspects and applications.

## Overview of Numerical Methods

### Finite Difference Methods (FDM)

In FDM, the domain is discretized into a grid or mesh of points. The differential operators in the PDEs are approximated by difference operators using values at these grid points. For example, the derivative of a function at a point can be approximated using the difference of function values at neighboring points. This straightforward approach is effective for simple geometries and boundary conditions.

### Finite Volume Methods (FVM)

FVM also discretizes the domain but focuses on approximating integrals rather than derivatives. By integrating the PDEs over control volumes, FVM ensures conservation of key physical quantities like mass, momentum, and energy. This method is particularly advantageous in fluid dynamics for maintaining the integral conservation laws.

### Spectral Methods

Spectral methods differ from FDM and FVM as they do not discretize the domain into a grid. Instead, they express the solution as a sum of basis functions (e.g., Fourier series). The coefficients of these basis functions are determined to best approximate the solution. Spectral methods are known for their high accuracy in smooth problems.

### Finite Element Methods (FEM)

FEM combines the local approximation approach of FDM and FVM with the solution space approximation of spectral methods. The domain is divided into elements, and the solution is approximated using polynomial basis functions within each element. FEM is versatile and effective for complex geometries and boundary conditions.

## Detailed Description of FDM

### Key Concepts in FDM

1. **Grid Generation**: Divide the domain into a structured grid of points.
2. **Discretization**: Approximate the differential operators in the PDEs using finite differences.
3. **Boundary Conditions**: Implement boundary conditions by modifying the finite difference equations at the domain boundaries.
4. **Solution of the System**: Solve the resulting system of algebraic equations for the unknown function values at the grid points.

### Steps in FDM

1. **Define the Domain and Grid**: 
    - For a 1D domain, create a grid with points $ x_0, x_1, \ldots, x_N $.
    - For higher dimensions, create a mesh with points $ (x_i, y_j) $ in 2D, or $ (x_i, y_j, z_k) $ in 3D.

2. **Discretize the PDE**:
    - For a 1D PDE like $ \frac{d^2 u}{dx^2} = f(x) $, approximate the second derivative using central differences: 
   
      $$
      \frac{d^2 u}{dx^2} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{\Delta x^2}
      $$
   
    - Similarly, discretize other differential operators.

3. **Formulate the System of Equations**:
    - For each grid point, write an equation involving the function values at that point and its neighbors.
    - Assemble these equations into a system of linear equations.

4. **Apply Boundary Conditions**:
    - Modify the equations at the boundaries to incorporate Dirichlet, Neumann, or mixed boundary conditions as required.

5. **Solve the System**:
    - Use numerical methods (e.g., Gauss-Seidel, Conjugate Gradient) to solve the system of linear equations for the unknown function values at the grid points.

### Example: Solving a 1D Heat Equation

Consider the 1D heat equation $ \frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2} $:

1. **Discretize in Space and Time**:
   
    - Use a grid with points $ x_i = i \Delta x $ and time steps $ t^n = n \Delta t $.
    - Approximate the spatial derivative using central differences and the time derivative using a forward difference.

2. **Formulate the Discretized Equation**:
   
$$
\frac{u_i^{n+1} - u_i^n}{\Delta t} = \alpha \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}
$$

3. **Rearrange and Solve**:

    - Iterate this equation over all grid points and time steps to find the solution.
   
$$
u_i^{n+1} = u_i^n + \alpha \frac{\Delta t}{\Delta x^2} (u_{i+1}^n - 2u_i^n + u_{i-1}^n)
$$
   

## Further Reading

1. **Books**
    - "Numerical Methods for Engineers" by Steven C. Chapra and Raymond P. Canale.
    - "Computational Fluid Dynamics: The Basics with Applications" by John D. Anderson Jr.

2. **Research Papers**
    - "Finite Difference Methods for Ordinary and Partial Differential Equations" by Randall J. LeVeque.
    - "Numerical Solution of Partial Differential Equations: Finite Difference Methods" by G. D. Smith.

3. **Online Resources**
    - MIT OpenCourseWare: Numerical Methods for Partial Differential Equations.
    - YouTube tutorials on Finite Difference Methods in CFD.

