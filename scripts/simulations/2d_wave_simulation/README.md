# 2D Wave Equation Simulation

This script simulates the 2D scalar wave equation on a square domain using the explicit finite difference method. The wave propagates outward from an initial Gaussian disturbance and is animated in 3D using Matplotlib.

## Overview

- Initializes the wave field with a scaled Gaussian pulse centered at the origin.
- Advances the solution in time using a leapfrog finite difference scheme.
- Enforces Dirichlet (zero) boundary conditions on all four edges.
- Animates the evolving wave amplitude as a 3D surface plot.

## Mathematical Background

The 2D wave equation describes the propagation of a scalar wave field $u(x, y, t)$:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

where $c$ is the wave propagation speed.

### Finite Difference Discretization

The spatial second derivatives are approximated using central differences:

$$\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2}, \quad \frac{\partial^2 u}{\partial y^2} \approx \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2}$$

Combined with the leapfrog time derivative, this yields the explicit update rule:

$$u_{i,j}^{n+1} = 2u_{i,j}^n - u_{i,j}^{n-1} + (c\,\Delta t)^2 \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)$$

### Stability (CFL Condition)

For stability, the time step must satisfy the Courant–Friedrichs–Lewy (CFL) condition:

$$\Delta t \leq \frac{1}{c\sqrt{2}} \min(\Delta x, \Delta y)$$

### Initial Condition

The wave is initialized with a scaled Gaussian pulse centered at the origin:

$$u(x, y, 0) = A \exp\!\left(-\frac{x^2 + y^2}{2}\right)$$

where $A$ is a scale factor controlling the amplitude.

## Implementation

1. **Grid Setup**: Defines a uniform $100 \times 100$ grid over $[-L, L]^2$ and computes the time step to satisfy the CFL condition.
2. **Initial Condition**: Sets $u^0$ and $u^1$ to the Gaussian pulse.
3. **Time Stepping**: Iterates the leapfrog update rule, applying zero Dirichlet boundary conditions at each step.
4. **Animation**: Uses `FuncAnimation` to render the wave amplitude as a 3D surface plot updated each frame.

## Output

The script produces an animated 3D surface plot showing the wave amplitude $u(x, y, t)$ evolving over time. The dark background and viridis colormap highlight the wave crests and troughs as the wave reflects off the domain boundaries.
