# Eulerian Cylinder Flow

The `FluidSimulator` class is a tool designed to simulate fluid dynamics in a 2D environment using a grid-based approach. This class implements the fundamentals of fluid motion, including advection, incompressibility, and the interaction with obstacles, providing an engaging platform for real-time visualization and educational purposes.

[![Watch the Short on YouTube](https://img.youtube.com/vi/GYtn9u0awsE/maxresdefault.jpg)](https://youtube.com/shorts/GYtn9u0awsE?si=qlHDFdepFfnIFg8W)

## Features

- **Grid-Based Simulation**: Tracks fluid properties on a fixed grid, ensuring efficient computation and easy visualization.
- **Incompressibility**: Ensures that the fluid density remains constant by solving for pressure and adjusting velocities accordingly.
- **Advection**: Simulates the transport of fluid properties through the domain over time.
- **Obstacle Interaction**: Includes the ability to place obstacles within the simulation domain, affecting fluid flow.
- **Real-Time Visualization**: Utilizes Pygame for real-time rendering of the simulation, allowing for interactive exploration.

## Detailed Explanation

### Grid-Based Simulation

The `FluidSimulator` uses a discretized grid to track fluid properties like velocity and density. This method is computationally efficient and aligns well with numerical solvers for fluid dynamics.

### Incompressibility

To maintain incompressibility, the simulator solves a Poisson equation for pressure, which is then used to adjust the velocity field, ensuring mass conservation within the fluid.

### Advection

The `advect` method handles the transport of fluid properties, such as velocity and density, through the simulation domain. This step is crucial for depicting the natural flow and mixing of the fluid.

### Obstacle Interaction

The simulator can incorporate obstacles, which are represented as solid cells within the grid. These obstacles affect the fluid flow, providing a more realistic and interactive simulation experience.

### Real-Time Visualization

Using Pygame, the simulation is rendered in real-time, allowing users to visualize and interact with the fluid dynamics as they happen. This feature makes the simulator an excellent tool for both education and demonstration purposes.
