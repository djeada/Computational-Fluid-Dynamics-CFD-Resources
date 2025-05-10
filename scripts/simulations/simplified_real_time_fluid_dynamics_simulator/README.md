# Simplified Real Time Fluid Dynamics Simulator

The `FluidSimulation` class is a solver that approximates fluid dynamics in a 2D environment using an Eulerian grid-based approach. This class simulates aspects of the Navier-Stokes equations through diffusion, advection, and projection steps, providing a simplified yet effective solution for real-time simulations and visualizations.

[![Watch the Short on YouTube](https://img.youtube.com/vi/auwaTfkpIXo/maxresdefault.jpg)](https://youtube.com/shorts/auwaTfkpIXo)

## Features

- **Eulerian Approach**: Properties like velocity, pressure, and density are tracked at fixed grid points in space, rather than following individual fluid particles.
- **Navier-Stokes Approximation**: The simulation approximates the Navier-Stokes equations, fundamental for describing the motion of viscous fluids.
- **Diffusion and Viscosity**: Simulates the spreading of fluid properties and incorporates viscosity to influence the momentum transfer within the fluid.
- **Advection**: Transports properties such as density and velocity through the fluid over time.
- **Projection and Pressure**: Ensures incompressibility by solving a Poisson equation for pressure, maintaining realism in the simulation.
- **Discretization and Time Stepping**: Utilizes a discretized grid and discrete time steps for computational simulation.
- **Boundary Conditions**: Manages fluid behavior at the simulation domain's edges for realistic interactions.

## Detailed Explanation

### Eulerian Approach

In an Eulerian fluid simulation, the fluid's properties are tracked at fixed grid points. This method associates properties like velocity components (Vx, Vy) and density with specific grid locations, making it suitable for grid-based simulations.

### Navier-Stokes Equations

The class approximates the Navier-Stokes equations, which describe the motion of viscous fluid substances. These equations account for forces such as pressure, viscosity, and external influences on fluid motion.

### Diffusion and Viscosity

- **Diffusion**: The `diffuse` method simulates the spreading of fluid properties, using an iterative solver (likely a variant of the Jacobi method) to approximate this process over time.
- **Viscosity**: Viscosity, a measure of a fluid's resistance to flow, is included in the simulation. It affects how velocity is diffused across the grid, impacting the overall fluid dynamics.

### Advection

The `advect` method describes how properties like density and velocity are transported through the fluid over time. Advection is crucial for representing the movement of fluid elements in space.

### Projection and Pressure

The `project` method enforces incompressibility, ensuring the velocity field respects the mass conservation principle. This involves solving a Poisson equation for pressure, which is essential to prevent unrealistic compression or expansion of the fluid.

### Discretization and Time Stepping

The simulation operates on a discretized grid (a 2D array) with discrete time steps (`dt`). This approach is common in computational simulations to approximate continuous phenomena using discrete values.

### Boundary Conditions

The `set_bnd` function manages boundary conditions, defining how the fluid behaves at the simulation domain's edges. These conditions are vital for accurately simulating interactions with the container walls.
