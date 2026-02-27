# Mean Pressure Coefficient Along Vehicle Centreline

This script plots the mean pressure coefficient $C_P$ along the upper-body centreline of a vehicle versus streamwise position $x$, comparing experimentally measured data with CFD Scale-Resolving Simulation (SRS) results. A key annotation highlights the separation plateau region where the simulation underpredicts the extent of flow separation relative to experiment.

## Overview

- Plots $C_P(x)$ for both experimental (`Exp`) and CFD SRS data over $x \in [-1, 4]$ m
- Uses distinct markers and colours (black for experiment, cyan for CFD SRS)
- Annotates the separation plateau with an arrow and descriptive text
- Demonstrates typical agreement and discrepancy between high-fidelity CFD and wind-tunnel data

## Mathematical Background

### Pressure Coefficient Definition

The pressure coefficient non-dimensionalises the local surface pressure against the dynamic pressure of the free stream:

$$C_P = \frac{p - p_\infty}{\dfrac{1}{2}\,\rho\,U_\infty^2}$$

where $p$ is the local static pressure, $p_\infty$ the far-field static pressure, $\rho$ the fluid density, and $U_\infty$ the free-stream velocity.

### Flow Separation and the Separation Plateau

An adverse pressure gradient drives flow towards separation. In terms of $C_P$:

$$\frac{\partial C_P}{\partial x} > 0 \implies \frac{\partial p}{\partial x} > 0$$

This deceleration thickens the boundary layer and, beyond a critical point, causes separation. Once separated, $C_P$ remains nearly constant — forming the characteristic **separation plateau**:

$$C_P \approx C_{P,\text{sep}} = \text{const}, \quad x \in [x_{\text{sep}},\, x_{\text{reat}}]$$

### CFD Scale-Resolving Simulation

SRS methods (e.g., LES, DES) resolve large turbulent eddies directly rather than modelling them entirely as in RANS:

$$\frac{\partial \bar{u}_i}{\partial t} + \bar{u}_j \frac{\partial \bar{u}_i}{\partial x_j} = -\frac{1}{\rho}\frac{\partial \bar{p}}{\partial x_i} + \nu \frac{\partial^2 \bar{u}_i}{\partial x_j^2} - \frac{\partial \tau_{ij}^{\text{sgs}}}{\partial x_j}$$

where $\tau_{ij}^{\text{sgs}}$ is the subgrid-scale stress tensor. SRS captures separation dynamics better than RANS but may still underpredict the plateau length.

## Implementation

1. Generate a streamwise coordinate array `x = np.linspace(-1, 4, 50)` (metres)
2. Compute mock experimental $C_P$ as `exp = -0.2 sin(x) - 0.1 cos(2x)`
3. Compute mock CFD $C_P$ by adding small Gaussian noise to `exp`
4. Create a single-axes figure (`figsize=(10, 6)`)
5. Plot experimental data as `"o-"` in black, CFD SRS as `"o-"` in cyan
6. Label axes `x [m]` and `$C_P$ [-]`; set title referencing the upper-body centreline at `y = 0 m`
7. Annotate the separation plateau with `ax.annotate(...)` using a blue arrow
8. Display the figure with `plt.tight_layout()` and `plt.show()`

## Output

The script displays a line plot of $C_P$ versus streamwise position $x$. The black curve (experiment) shows a pronounced flat separation plateau, while the cyan curve (CFD SRS) follows a similar trend but with a less distinct plateau. A blue arrow annotation identifies this discrepancy. A legend distinguishes the two data sources.

![mean_pressure_coefficient_plot](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/04e46497-3f78-40ab-a9ee-4acc15e61cf2)
