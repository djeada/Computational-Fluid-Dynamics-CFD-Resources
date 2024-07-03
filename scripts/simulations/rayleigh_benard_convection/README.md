# Rayleigh-Bénard Convection Simulation

This project simulates the Rayleigh-Bénard convection using a simplified thermal convection model and visualizes it using Pygame.

## Demonstration

Watch the Rayleigh-Bénard Convection Simulation in action:

[![Rayleigh-Bénard Convection Simulation](https://i9.ytimg.com/vi/E_N-ld6Vfwo/mqdefault.jpg?sqp=CJiVlrQG-oaymwEoCMACELQB8quKqQMcGADwAQH4AbYIgAK-CIoCDAgAEAEYEyAiKH8wDw==&rs=AOn4CLAVlKO8E4MPwP5jiYMMJgc0MW4Aig)](https://youtube.com/shorts/E_N-ld6Vfwo)

## Features

- **Grid Initialization**: The grid is initialized with a linear temperature gradient from 1.0 (bottom) to 0.0 (top).
- **Temperature and Velocity Updates**: Updates the temperature and velocity fields to simulate convection.
- **Visualization**: Uses Pygame to visualize the temperature distribution.

## Simulation Parameters

- **Grid Size**: 128x128 cells
- **Window Size**: 400x400 pixels
- **Frame Rate**: 60 frames per second
- **Cell Size**: Computed as `WINDOW_SIZE // GRID_SIZE`
- **Temperature Range**: [0.0, 1.0]

## Detailed Explanation

### Initialization

- **Libraries**: Imports necessary libraries (Pygame, NumPy, multiprocessing).
- **Simulation Parameters**: Sets up the grid size, window size, frame rate, and other simulation parameters.
- **Pygame Setup**: Initializes Pygame for visualization.

### Temperature to Color Conversion

- **Function**: Defines a function to map temperature values to colors for visual representation.

### Grid Initialization

- **Temperature Gradient**: Initializes the grid with a temperature gradient, with higher temperatures at the bottom and lower temperatures at the top.

### Cell Update Function

- **Temperature Update**: Defines a function to update the temperature of a cell based on its neighbors and velocity field.
- **Multiprocessing**: Utilizes multiprocessing for efficient computation of temperature updates.

### Grid Update

- **Parallel Updates**: Defines a function to update the entire grid using multiprocessing to parallelize cell updates.

### Velocity Update

- **Gradient-Based Update**: Defines a function to update the velocity fields based on the temperature gradient.

### Grid Drawing

- **Visualization**: Defines a function to draw the grid on the Pygame window using the color mapping function.

### Main Loop

- **Initialization**: Initializes the grid and velocity fields.
- **Continuous Update**: Runs the main loop to continuously update and draw the grid.
- **Event Handling**: Handles Pygame events to allow quitting the simulation.

## Running the Script

1. **Dependencies**: Ensure you have Pygame and NumPy installed.
2. **Execution**: Run the script to start the simulation.
3. **Visualization**: The simulation window will display the evolving temperature field, with colors indicating different temperatures.
