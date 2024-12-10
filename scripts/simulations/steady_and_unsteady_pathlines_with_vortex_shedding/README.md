# Flow Visualization Around a Cylinder: Steady and Unsteady Pathlines with Vortex Shedding

This project provides a comprehensive simulation of fluid flow around a cylindrical object, demonstrating both steady and unsteady flow conditions. By visualizing pathlines and streamlines, the simulation highlights the phenomenon of vortex shedding, a critical aspect in fluid dynamics with applications in engineering and environmental sciences.

## Features

- **Steady Flow Simulation**: Visualizes the steady-state flow around a cylinder where streamlines and pathlines coincide.
- **Unsteady Flow with Vortex Shedding**: Demonstrates unsteady flow conditions where vortices are periodically shed from the cylinder, causing streamlines and pathlines to diverge.
- **Interactive Visualization**: Uses Matplotlib to animate the flow, allowing for dynamic observation of particle pathlines.
- **Numerical Integration**: Implements the Runge-Kutta 4th order (RK4) method for accurate computation of particle trajectories.
- **Customizable Parameters**: Easily adjust parameters such as cylinder radius, free stream velocity, circulation, and simulation time.

## Physics Behind the Simulation

### Steady Flow

In a steady flow scenario, the fluid moves uniformly around the cylinder without any temporal changes. The flow is characterized by:

- **Streamlines**: Lines that represent the flow direction at every point in the fluid. In steady flow, streamlines are constant over time.
- **Pathlines**: Trajectories that individual fluid particles follow over time. In steady flow, pathlines coincide with streamlines.

### Unsteady Flow and Vortex Shedding

Unsteady flow introduces time-dependent changes in the fluid motion, leading to complex phenomena such as vortex shedding:

- **Vortex Shedding**: Periodic detachment of vortices from the surface of the cylinder, leading to alternating patterns of swirling fluid. This results in oscillating forces on the cylinder, which can cause vibrations and structural fatigue.
- **Differences Between Streamlines and Pathlines**: In unsteady flow, streamlines change over time, and pathlines no longer coincide with streamlines, illustrating the dynamic nature of the flow.

## Mathematical Foundations

### Velocity Field Calculation

The velocity field around the cylinder is computed using the superposition of a uniform flow and a circulation-induced flow:

- **Uniform Flow**: Represents the free stream velocity $U$.
- **Circulation ($\Gamma$)**: Introduces rotational motion around the cylinder, calculated as $\Gamma = 4\pi R U$, where $R$ is the cylinder radius.

The steady velocity components $U_x$ and $U_y$ at any point $(X, Y)$ are given by:

$$U_r = U \left(1 - \frac{R^2}{X^2 + Y^2}\right)$$

$$U_\theta = -U \frac{R^2}{X^2 + Y^2} + \frac{\Gamma}{2\pi (X^2 + Y^2)}$$

$$U_x = U_r \cos(\theta) - U_\theta \sin(\theta)$$

$$U_y = U_r \sin(\theta) + U_\theta \cos(\theta)$$

Where $\theta = \arctan\left(\frac{Y}{X}\right)$.

### Vortex Contribution

Additional vortices are introduced to simulate unsteady flow. The velocity contribution from each vortex is calculated using the Biot-Savart law:

$$U_x = \frac{\gamma}{2\pi} \left(-\frac{Y - y_v}{(X - x_v)^2 + (Y - y_v)^2}\right)$$

$$U_y = \frac{\gamma}{2\pi} \left(\frac{X - x_v}{(X - x_v)^2 + (Y - y_v)^2}\right)$$

Where $(x_v, y_v)$ is the position of the vortex and $\gamma$ is its strength.

### Numerical Integration with RK4

The Runge-Kutta 4th order method is employed to compute the trajectories of fluid particles:

I. **Compute $k_1$**: Velocity at the current position.

II. **Compute $k_2$**: Velocity at the midpoint using $k_1$.

III. **Compute $k_3$**: Velocity at the midpoint using $k_2$.

IV. **Compute $k_4$**: Velocity at the next step using $k_3$.

V. **Update Position**: Combine the slopes to estimate the new position.

### Adjusting Parameters

You can modify various parameters within the script to observe different flow behaviors:

- **Cylinder Radius (`R`)**
- **Free Stream Velocity (`U`)**
- **Circulation (`Gamma`)**
- **Time Step (`dt`)**
- **Number of Time Steps (`nt`)**
- **Number of Particles (`num_particles`)**
