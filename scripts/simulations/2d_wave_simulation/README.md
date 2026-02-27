# 2D Wave Equation Simulation

This script simulates the 2D scalar wave equation on a square domain using the explicit finite difference method. The wave propagates outward from an initial Gaussian disturbance and is animated in 3D using Matplotlib.

## Mathematical Background

The 2D wave equation describes the propagation of a scalar wave field $u(x, y, t)$:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

where $c$ is the wave propagation speed.

### Finite Difference Discretization

The spatial second derivatives are approximated using central differences:

$$\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2}, \quad \frac{\partial^2 u}{\partial y^2} \approx \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2}$$

The time derivative uses a leapfrog (second-order) scheme:

$$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_{i,j}^{n+1} - 2u_{i,j}^n + u_{i,j}^{n-1}}{\Delta t^2}$$

Combining these gives the explicit update rule:

$$u_{i,j}^{n+1} = 2u_{i,j}^n - u_{i,j}^{n-1} + (c\,\Delta t)^2 \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)$$

### Stability (CFL Condition)

For stability, the time step must satisfy the Courant–Friedrichs–Lewy (CFL) condition:

$$\Delta t \leq \frac{1}{c\sqrt{2}} \min(\Delta x, \Delta y)$$

### Boundary Conditions

Dirichlet boundary conditions ($u = 0$) are enforced on all four edges of the domain, causing the wave to reflect off the boundaries.

## Initial Condition

The wave is initialized with a scaled Gaussian pulse centered at the origin:

$$u(x, y, 0) = A \exp\!\left(-\frac{x^2 + y^2}{2}\right)$$

where $A$ is a scale factor controlling the amplitude.

## Output

The script produces an animated 3D surface plot showing the wave amplitude $u(x, y, t)$ evolving over time. The dark background and viridis colormap highlight the wave crests and troughs.
