# Mean Velocity Magnitude — Experiment vs CFD Comparison

This script plots the normalised mean velocity magnitude $|U|/U_0$ along the under-body centreline of a bluff body, comparing mock experimental data with CFD Scale-Resolving Simulation (SRS) results. It demonstrates the typical validation workflow used in industrial CFD where computational predictions are benchmarked against wind-tunnel or water-tunnel measurements.

## Overview

- Generates mock experimental data using an exponentially damped sinusoidal profile
- Adds a small random deviation to produce synthetic CFD SRS results
- Plots both datasets against relative streamwise distance $x/L$
- Includes error bars, legend, and axis labels consistent with CFD validation reports

## Mathematical Background

### Velocity Magnitude

$$|\mathbf{U}| = \sqrt{u^2 + v^2 + w^2}$$

### Normalised Velocity

$$\frac{|\mathbf{U}|}{U_0}$$

where $U_0$ is the reference free-stream speed used to non-dimensionalise both experimental and CFD data.

### Mock Experimental Profile

$$u_{exp}(x) = e^{-0.2x}\sin(x) + 0.75$$

### CFD Deviation

The CFD SRS result is generated as $u_{CFD}(x) = u_{exp}(x) + \epsilon$ where $\epsilon$ is a small random perturbation, simulating the slight discrepancy expected between simulation and measurement.

## Implementation

1. Define a streamwise coordinate array representing relative distance along the under-body centreline.
2. Evaluate the mock experimental profile $u_{exp}(x)$.
3. Add a random perturbation to produce the synthetic CFD profile.
4. Plot both profiles on the same axes with distinct markers and line styles.
5. Add labels, legend, and grid consistent with a CFD validation figure.

## Output

The script displays a single plot of $|U|/U_0$ versus relative streamwise position. Two curves are overlaid — one for experimental data and one for the CFD SRS result — illustrating the level of agreement typically achieved by scale-resolving simulations in wake and under-body flow regions.

![mean_velocity_magnitude_plot](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/786494a3-21c4-4141-bafd-0f40da8db897)
