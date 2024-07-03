# Lid-Driven Cavity Flow Simulation

This project simulates fluid flow over a flat plate using the 2D incompressible Navier-Stokes equations, known as the lid-driven cavity problem.

## Demonstration

Watch the Lid-Driven Cavity Flow Simulation in action:

[![Lid-Driven Cavity Flow Simulation](https://i9.ytimg.com/vi/mOMWcGnXtFQ/mqdefault.jpg?sqp=CJyclrQG-oaymwEoCMACELQB8quKqQMcGADwAQH4AbYIgAK2CYoCDAgAEAEYMyA_KH8wDw==&rs=AOn4CLCqf8J8ybMPnO9IPgo_ARAmoiQ68g)](https://youtube.com/shorts/mOMWcGnXtFQ)

## Overview

- **Lid-Driven Cavity Problem**: Simulates fluid flow in a confined space with a moving top boundary.
- **2D Incompressible Navier-Stokes Equations**: Computes velocity and pressure fields within the cavity.
- **Complex Flow Patterns**: Creates interesting flow patterns for studying fluid behavior.

## Approach Taken

### Discretization

- **Grid**: The 2D domain is discretized into a grid of `N_POINTS x N_POINTS` (128x128 points).
- **Cell Size**: Each grid cell has a specified size (`element_length`) based on the `DOMAIN_SIZE`.

### Initialization

- **Velocity and Pressure Fields**: Initializes the velocity fields (`u` and `v`) and pressure field (`p`).
- **Perturbation**: Adds a small perturbation to the velocity field `u` to initiate the flow.

### Time Integration

- **Time-Stepping**: Evolves the velocity and pressure fields over `N_ITERATIONS` time steps.
- **Stability**: Uses a small `TIME_STEP` to ensure numerical stability.

### Central Differences

- **Spatial Derivatives**: Functions `central_difference_x` and `central_difference_y` compute the spatial derivatives of the velocity fields using central difference schemes.
- **Laplacian**: The `laplace` function computes the Laplacian of a field, essential for diffusion terms in the Navier-Stokes equations.

### Boundary Conditions

- **Velocity on Boundaries**: The `apply_boundary_conditions` function sets the velocity on the boundaries, enforcing the lid velocity on the top and zero velocities on the other boundaries.

### Pressure Poisson Equation

- **Pressure Solver**: The `solve_pressure_poisson` function iteratively solves the Poisson equation for pressure, ensuring the velocity field remains divergence-free (incompressible).

### Velocity Update

- **Tentative Velocities**: Computes tentative velocities using the Navier-Stokes equations without the pressure gradient.
- **Pressure Correction**: Uses pressure gradients to correct the velocities, enforcing incompressibility.

### Visualization

- **Animated Contour Plots**: Uses Matplotlib to create animated contour plots of the velocity fields (`u` and `v`) at each time step.
- **Dynamic Updates**: The `FuncAnimation` class dynamically updates these plots to show the flow evolution.

## Output

The output is an animation showing the evolution of the velocity fields `u` (horizontal component) and `v` (vertical component) over time, providing insights into flow development within the cavity:

- **Velocity Field Contours**: Displays the distribution and magnitude of the velocity components `u` and `v`. Initially, the flow starts with small perturbations, becoming more pronounced over time.
- **Boundary Effects**: The lid-driven boundary condition creates a shear layer at the top, influencing the entire flow within the cavity and forming recirculating vortices near the stationary boundaries.
- **Iterative Convergence**: The animation illustrates the iterative process over `N_ITERATIONS`, showing how the solution gradually approaches a steady-state or dynamically stable condition.
