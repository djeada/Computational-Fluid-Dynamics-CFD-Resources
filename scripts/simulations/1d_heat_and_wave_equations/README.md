# 1D Heat and Wave Equation Simulations

This script numerically solves both the 1D heat equation and the 1D wave equation using explicit finite difference schemes. It demonstrates fundamental time-stepping techniques in computational physics and highlights the stability conditions that govern each method.

## Overview

- Solves the 1D heat (diffusion) equation via the explicit forward-Euler finite difference method
- Solves the 1D wave equation via the explicit leapfrog (second-order in time) finite difference method
- Enforces stability criteria for both equations before time-stepping
- Visualises the evolving temperature and displacement fields over time

## Mathematical Background

### Heat Equation

The 1D heat equation governs diffusive transport of temperature $u(x,t)$:

$$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$$

where $\alpha$ is the thermal diffusivity.

### Explicit Finite Difference Discretisation (Heat)

Approximating both derivatives on a uniform grid:

$$\frac{\partial^2 u}{\partial x^2} \approx \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}, \qquad \frac{\partial u}{\partial t} \approx \frac{u_i^{n+1} - u_i^n}{\Delta t}$$

Stability requires the time step to satisfy:

$$\Delta t \leq \frac{\Delta x^2}{2\alpha}$$

### Wave Equation

The 1D wave equation models displacement $u(x,t)$ propagating at speed $c$:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$$

### Leapfrog Discretisation (Wave)

The second-order time derivative is discretised as:

$$\frac{\partial^2 u}{\partial t^2} \approx \frac{u_i^{n+1} - 2u_i^n + u_i^{n-1}}{\Delta t^2}$$

Stability (CFL condition) requires:

$$\frac{c\,\Delta t}{\Delta x} \leq 1$$

## Implementation

1. Define spatial grid, time step, and physical parameters ($\alpha$ for heat; $c$ for wave)
2. Verify stability conditions ($\Delta t \leq \Delta x^2/2\alpha$ and $c\Delta t/\Delta x \leq 1$)
3. Set initial conditions (e.g., Gaussian pulse or step function)
4. Apply boundary conditions (Dirichlet or Neumann) at domain edges
5. Advance each equation through time using the respective explicit update formula
6. Render or save snapshots of the field at selected time steps

## Output

- **Heat simulation**: animated or saved frames showing temperature profile diffusing and flattening over time
- **Wave simulation**: animated or saved frames showing the displacement profile propagating and reflecting from boundaries
