# Lid-Driven Cavity Flow Simulation

This project simulates 2D incompressible fluid flow in a confined square cavity driven by a moving top boundary ("the lid"), producing recirculating vortex structures. Watch it in action: [![YouTube](https://i9.ytimg.com/vi/mOMWcGnXtFQ/mqdefault.jpg)](https://youtube.com/shorts/mOMWcGnXtFQ)

## Overview

- **Lid-Driven Cavity Problem**: fluid enclosed in a square domain driven by a moving top wall at velocity $U_{lid}$.
- **2D Incompressible Navier-Stokes**: coupled velocity and pressure fields solved on a 128×128 grid.
- **Central-difference discretization**: spatial derivatives and Laplacians computed with second-order accuracy.
- **Pressure Poisson solver**: iterative solution enforces the divergence-free constraint.
- **Matplotlib animation**: animated contour plots of $u$ and $v$ updated via `FuncAnimation`.

## Mathematical Background

### Momentum Equations

The 2D incompressible Navier-Stokes equations for velocity components $(u,v)$:

$$\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = -\frac{\partial p}{\partial x} + \nu\nabla^2 u$$

$$\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} = -\frac{\partial p}{\partial y} + \nu\nabla^2 v$$

### Pressure Poisson Equation

To enforce incompressibility ($\nabla\cdot\mathbf{u}=0$), pressure is found from:

$$\nabla^2 p = \frac{\rho}{\Delta t}\,\nabla\cdot\mathbf{u}^*$$

where $\mathbf{u}^*$ is the tentative velocity before pressure correction.

### Spatial Discretization

Central differences on the uniform grid with spacing $\Delta x$:

$$\frac{\partial f}{\partial x}\bigg|_{i,j} \approx \frac{f_{i+1,j}-f_{i-1,j}}{2\Delta x},\quad \nabla^2 f_{i,j} \approx \frac{f_{i+1,j}+f_{i-1,j}-2f_{i,j}}{\Delta x^2}+\frac{f_{i,j+1}+f_{i,j-1}-2f_{i,j}}{\Delta y^2}$$

### Boundary Conditions and CFL Stability

Lid BC: $u = U_{lid}$ at the top wall; $u = v = 0$ on the remaining three walls. The time step satisfies:

$$\frac{U_{lid}\,\Delta t}{\Delta x} \le 1$$

## Implementation

1. Discretize the square domain into a 128×128 grid; set `element_length = DOMAIN_SIZE / (N_POINTS - 1)`.
2. Initialize velocity fields $u$, $v$ to zero; add a small perturbation to $u$ to seed the flow.
3. At each time step, compute tentative velocities $\mathbf{u}^*$ from the advection and diffusion terms via central differences.
4. Apply boundary conditions: $u = U_{lid}$ at the top, $u = v = 0$ on the remaining walls.
5. Iteratively solve the pressure Poisson equation until the residual converges.
6. Correct velocities: $\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t\,\nabla p$.
7. Repeat for `N_ITERATIONS` steps; update the animated contour plots each frame.

## Output

The script produces a Matplotlib animation showing contour maps of the horizontal ($u$) and vertical ($v$) velocity components evolving over time:

- **Velocity contours** reveal the growing shear layer beneath the lid and the formation of a primary recirculating vortex.
- **Boundary effects** show how stationary walls redirect flow and generate secondary corner vortices.
- **Convergence** is visible as the solution approaches a steady-state vortex pattern after sufficient iterations.
