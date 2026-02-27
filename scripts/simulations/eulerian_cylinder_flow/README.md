# Eulerian Cylinder Flow

The `FluidSimulator` class simulates 2D incompressible flow past a cylinder using an Eulerian grid-based approach. Fluid properties (velocity, pressure) are tracked at fixed grid points; a pressure Poisson solve enforces incompressibility; and Pygame renders the flow field in real time. A short demonstration is available on YouTube: [![Watch on YouTube](https://img.youtube.com/vi/GYtn9u0awsE/maxresdefault.jpg)](https://youtube.com/shorts/GYtn9u0awsE?si=qlHDFdepFfnIFg8W)

## Overview

- Eulerian fixed-grid representation of velocity and pressure fields
- Pressure Poisson solve to enforce divergence-free (incompressible) velocity
- Semi-Lagrangian advection via backtracing for stable transport
- Cylinder obstacle enforced by zeroing velocities inside the solid region
- Real-time interactive rendering with Pygame

## Mathematical Background

### Governing Equations

The simulation approximates the incompressible Navier-Stokes equations:

$$\nabla \cdot \mathbf{u} = 0$$

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u}$$

where $\mathbf{u}$ is the velocity field, $p$ is pressure, and $\nu$ is kinematic viscosity.

### Pressure Poisson Equation

After computing an intermediate velocity $\mathbf{u}^*$ (ignoring pressure), incompressibility is restored by solving:

$$\nabla^2 p = \frac{\nabla \cdot \mathbf{u}^*}{\Delta t}$$

The pressure gradient is then used to project $\mathbf{u}^*$ onto a divergence-free field.

### Semi-Lagrangian Advection

Each grid point is traced backward along the velocity field for one time step:

$$\mathbf{u}^{\text{new}}(\mathbf{x}) = \mathbf{u}(\mathbf{x} - \mathbf{u}(\mathbf{x})\,\Delta t)$$

## Implementation

1. Initialise a 2D staggered grid with user-defined resolution and viscosity
2. Apply inflow boundary conditions and mark cylinder cells as solid obstacles
3. Compute intermediate velocity $\mathbf{u}^*$ via semi-Lagrangian advection and viscous diffusion
4. Solve the pressure Poisson equation iteratively (Gauss-Seidel) to obtain $p$
5. Correct velocities with $\mathbf{u} = \mathbf{u}^* - \Delta t\,\nabla p$ to enforce $\nabla\cdot\mathbf{u}=0$
6. Zero velocity inside cylinder cells and render the field with Pygame each frame

## Output

- **Real-time Pygame window**: colour-mapped velocity magnitude or pressure field with the cylinder obstacle visible; updates every simulation time step
