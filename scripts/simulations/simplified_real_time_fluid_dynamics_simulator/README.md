# Simplified Real-Time Fluid Dynamics Simulator

The `FluidSimulation` class implements the Stable Fluids algorithm (Stam 1999) on an Eulerian grid to approximate 2D Navier-Stokes dynamics in real time. Each time step consists of three stages: diffusion, semi-Lagrangian advection, and a pressure projection step that enforces incompressibility. A short demonstration is available on YouTube: [![Watch on YouTube](https://img.youtube.com/vi/auwaTfkpIXo/maxresdefault.jpg)](https://youtube.com/shorts/auwaTfkpIXo)

## Overview

- Eulerian grid: velocity components $(V_x, V_y)$ and scalar density tracked at fixed grid points
- Implicit diffusion solve for unconditional stability at any time step
- Semi-Lagrangian advection for stable transport of velocity and density fields
- Pressure Poisson projection to maintain a divergence-free velocity field
- Boundary conditions applied at every step to model container walls

## Mathematical Background

### Diffusion

Viscous diffusion of velocity is modelled by:

$$\frac{\partial \mathbf{u}}{\partial t} = \nu \nabla^2 \mathbf{u}$$

An implicit (backwards-Euler) solve is used so the method is unconditionally stable regardless of $\Delta t$:

$$(\mathbf{I} - \nu\,\Delta t\,\nabla^2)\,\mathbf{u}^{n+1} = \mathbf{u}^n$$

### Advection

Properties are transported using semi-Lagrangian backtracing:

$$\mathbf{u}^*(\mathbf{x}) = \mathbf{u}\!\left(\mathbf{x} - \mathbf{u}(\mathbf{x})\,\Delta t\right)$$

Bilinear interpolation recovers values at non-grid positions.

### Pressure Poisson Projection

To enforce incompressibility $\nabla\cdot\mathbf{u}=0$, pressure $p$ is found by solving:

$$\nabla^2 p = \frac{\nabla \cdot \mathbf{u}^*}{\Delta t}$$

and the velocity is corrected as $\mathbf{u} = \mathbf{u}^* - \Delta t\,\nabla p$.

## Implementation

1. Initialise grid arrays for $V_x$, $V_y$, and density; set viscosity and diffusion coefficients
2. Add external forces or user interactions to velocity/density fields
3. Diffuse velocity and density using an iterative implicit solver (Gauss-Seidel)
4. Advect velocity and density via semi-Lagrangian backtracing with bilinear interpolation
5. Solve the pressure Poisson equation; subtract gradient to project onto divergence-free space
6. Enforce boundary conditions with `set_bnd`; render density field via Pygame each frame

## Output

- **Real-time Pygame window**: colour-mapped scalar density field showing swirling flow patterns; responds interactively to mouse-driven force injections
