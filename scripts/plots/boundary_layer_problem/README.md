# Generating Synthetic Data for Boundary Layer Simulation

This project generates velocity data for a boundary layer over a flat plate using a simplified model.

## Steps

1. Define the Y-coordinates (distance from the wall).
2. Calculate the corresponding U-velocity components based on a typical boundary layer profile.
3. Generate plots for U versus Y.

## Simplified Boundary Layer Velocity Profile

The Blasius solution for a laminar boundary layer over a flat plate provides an approximate velocity profile. For simplicity, we use a parabolic profile:

\[ U(y) = U_\infty \left(\frac{y}{\delta}\right)^{0.5} \]

Where:
- \( U(y) \) is the velocity at distance \( y \) from the plate.
- \( U_\infty \) is the free-stream velocity.
- \( \delta \) is the boundary layer thickness.

## Explanation of the Script

1. **Parameters**: 
    - Define the free-stream velocity (\( U_\infty \)).
    - Define the boundary layer thickness (\( \delta \)).

2. **Generate Y-coordinates**: 
    - Generate an array of Y-coordinates from 0 to twice the boundary layer thickness to capture the velocity profile.

3. **Calculate U-velocity components**: 
    - Use a simplified parabolic profile to calculate the U-velocity component.
    - Assume U1 and U2 components are zero.

4. **Add Noise**: 
    - Add some noise to simulate realistic data.

5. **Save Data**: 
    - Save the data to a CSV file.

6. **Plotting**: 
    - Generate and save plots of U0 versus Y and all velocity components versus Y.

## Running the Script

Executing this script will produce a dataset and corresponding plots demonstrating the boundary layer velocity profile. This can be adapted to other scenarios like channel flow or pipe flow by modifying the velocity profile and spatial coordinates accordingly.
