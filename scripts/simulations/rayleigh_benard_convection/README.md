# Rayleigh-Bénard Convection Simulation

This project simulates the Rayleigh-Bénard convection using a simplified thermal convection model and visualizes it using Pygame.

## Steps

1. Initialize the grid with a temperature gradient.
2. Update the temperature and velocity fields.
3. Visualize the temperature distribution.

## Simulation Parameters

- **Grid Size**: 128x128 cells
- **Window Size**: 400x400 pixels
- **Frame Rate**: 60 frames per second
- **Cell Size**: Computed as `WINDOW_SIZE // GRID_SIZE`
- **Temperature Range**: [0.0, 1.0]

## Explanation of the Script

1. **Initialization**:
    - Import necessary libraries (Pygame, NumPy, multiprocessing).
    - Set up simulation parameters.
    - Initialize Pygame for visualization.

2. **Temperature to Color Conversion**:
    - Define a function to map temperature values to colors for visualization.

3. **Grid Initialization**:
    - Initialize the grid with a linear temperature gradient from 1.0 (bottom) to 0.0 (top).

4. **Cell Update Function**:
    - Define a function to update the temperature of a cell based on its neighbors and velocity field.
    - Use multiprocessing for efficient computation.

5. **Grid Update**:
    - Define a function to update the entire grid using multiprocessing to parallelize cell updates.

6. **Velocity Update**:
    - Define a function to update the velocity fields based on the temperature gradient.

7. **Grid Drawing**:
    - Define a function to draw the grid on the Pygame window using the color mapping.

8. **Main Loop**:
    - Initialize the grid and velocity fields.
    - Run the main loop to continuously update and draw the grid.
    - Handle Pygame events for quitting the simulation.

## Running the Script

1. Ensure you have Pygame and NumPy installed.
2. Run the script to start the simulation.
3. The simulation window will display the evolving temperature field with colors indicating different temperatures.
