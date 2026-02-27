# Generating Synthetic Data for Boundary Layer Simulation

This script generates synthetic velocity data for a laminar boundary layer over a flat plate using a simplified power-law profile. It adds Gaussian noise to simulate realistic measurement scatter, saves the resulting dataset to a CSV file, and produces plots of the streamwise velocity component against wall-normal distance.

## Overview

- Computes the wall-normal velocity profile using a square-root (power-law) approximation
- Adds Gaussian noise to all velocity components to mimic experimental data
- Saves the generated dataset (Y, U0, U1, U2) to a CSV file
- Produces a plot of U0 vs Y and a combined plot of all velocity components

## Mathematical Background

### Boundary Layer Velocity Profile

The streamwise velocity component across the boundary layer is approximated by:

$$U(y) = U_\infty \sqrt{\frac{y}{\delta}}$$

where:
- $U(y)$ is the velocity at wall-normal distance $y$
- $U_\infty$ is the free-stream velocity
- $\delta$ is the boundary layer thickness

### Noise Model

Gaussian noise $\mathcal{N}(0, \sigma^2)$ is added to each velocity component to simulate measurement uncertainty:

$$U_i^{\text{noisy}} = U_i + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$

## Implementation

1. Define parameters: free-stream velocity $U_\infty$ and boundary layer thickness $\delta$
2. Generate Y-coordinates from $0$ to $2\delta$ to capture the full profile and free-stream region
3. Compute $U_0 = U_\infty\sqrt{y/\delta}$; set lateral components $U_1 = U_2 = 0$
4. Add Gaussian noise to all three velocity components
5. Save the data array $(Y, U_0, U_1, U_2)$ to a CSV file
6. Plot $U_0$ vs $Y$ and all components vs $Y$; save figures to disk

## Output

- **CSV file**: tabular dataset with columns Y, U0, U1, U2 representing the synthetic boundary layer measurement
- **Plot 1**: streamwise velocity $U_0$ versus wall-normal distance $Y$
- **Plot 2**: all three velocity components ($U_0$, $U_1$, $U_2$) versus $Y$ on a single axes
