# Pressure Variation with Depth

This script visualizes how hydrostatic pressure increases with depth in a fluid. It demonstrates the fundamental relationship between fluid depth and pressure, which is foundational to fluid statics and hydraulics.

## Overview

- Computes the hydrostatic pressure profile from the surface down to a configurable maximum depth.
- Plots pressure as a function of depth with the y-axis inverted to reflect physical convention (depth increasing downward).
- Accepts fluid density, gravitational acceleration, and maximum depth as parameters.

## Mathematical Background

For a static fluid in a gravitational field, the hydrostatic pressure at depth $h$ below the free surface is given by:

$$P(h) = P_0 + \rho g h$$

where:
- $P_0$ — atmospheric pressure at the free surface (Pa),
- $\rho$ — fluid density (kg/m$^3$),
- $g$ — gravitational acceleration (m/s$^2$),
- $h$ — depth below the free surface (m).

### Derivation

This relationship is derived from the condition of static equilibrium applied to a fluid element:

$$\frac{dP}{dh} = \rho g$$

Integrating from the surface downward yields the linear pressure profile above. For water ($\rho = 1000$ kg/m$^3$) and standard gravity ($g = 9.81$ m/s$^2$), the pressure increases by approximately $9810$ Pa per metre of depth.

## Implementation

1. **Depth Array**: Generates 100 evenly spaced depth values from 0 to `max_depth` metres.
2. **Pressure Calculation**: Evaluates $P(h) = P_0 + \rho g h$ at each depth point using the provided parameters.
3. **Plot**: Draws pressure on the x-axis and depth on the y-axis with the y-axis inverted, adds a grid and legend, and displays the figure.

## Parameters

The `plot_pressure_variation_with_depth` function accepts the following keyword arguments:

| Parameter       | Default | Description                          |
|-----------------|---------|--------------------------------------|
| `fluid_density` | 1000    | Fluid density in kg/m$^3$               |
| `g`             | 9.81    | Gravitational acceleration in m/s$^2$   |
| `max_depth`     | 20      | Maximum depth to plot in metres       |

## Output

The script displays a plot of pressure (Pa) on the x-axis versus depth (m) on the y-axis, with depth increasing downward, illustrating the linear pressure increase with depth.
