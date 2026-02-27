# Turbulent Boundary Layer Velocity Profile

This script plots the velocity profile within a turbulent boundary layer using the empirical one-seventh power law. The profile describes how the streamwise velocity $u$ varies from zero at the wall (no-slip condition) to the free-stream value $U_\infty$ at the edge of the boundary layer $\delta$. The resulting curve is plotted against the wall-normal coordinate $y$, with the boundary layer thickness and wall position clearly indicated.

## Overview

- Implements the 1/7 power law as the turbulent boundary layer velocity profile
- Enforces the no-slip condition $u(0) = 0$ at the wall
- Shows the free-stream condition $u(\delta) = U_\infty$ at the boundary layer edge
- Marks the boundary layer thickness $\delta$ with a horizontal reference line
- Produces a clean, labeled plot of $u/U_\infty$ versus $y/\delta$

## Mathematical Background

### One-Seventh Power Law

The turbulent boundary layer velocity profile is approximated by:

$$\frac{u}{U_\infty} = \left(\frac{y}{\delta}\right)^{1/7}$$

where $y$ is the wall-normal distance, $\delta$ is the boundary layer thickness, and $U_\infty$ is the free-stream velocity.

### Boundary Conditions

No-slip at the wall:

$$u(0) = 0$$

Free-stream velocity at the boundary layer edge:

$$u(\delta) = U_\infty$$

### Wall Shear Stress

The steeper near-wall gradient of the turbulent profile implies a higher wall shear stress compared with the laminar case:

$$\tau_w = \mu \left.\frac{\partial u}{\partial y}\right|_{y=0}$$

## Implementation

1. Define the free-stream velocity $U_\infty$ and boundary layer thickness $\delta$.
2. Generate a uniform array of wall-normal positions $y \in [0, \delta]$.
3. Evaluate $u/U_\infty = (y/\delta)^{1/7}$ at each point.
4. Plot $u/U_\infty$ on the horizontal axis and $y$ on the vertical axis.
5. Add horizontal lines marking the wall ($y = 0$) and boundary layer edge ($y = \delta$).
6. Label axes and annotate the profile with the power-law formula.

## Output

The script produces a figure showing the turbulent velocity profile as a smooth curve from the origin to the free-stream value. A dashed horizontal line marks the boundary layer thickness $\delta$, and the wall is indicated at $y = 0$. Axis labels and a legend identify the profile type and key parameters.

![boundary_layer_velocity_profile](https://github.com/user-attachments/assets/0b3f51b4-7771-4d87-b59a-0bde6705b383)
