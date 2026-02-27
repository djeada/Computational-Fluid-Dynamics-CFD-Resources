# Pressure Variation with Depth

This script visualizes how hydrostatic pressure increases with depth in a fluid. It demonstrates the fundamental relationship between fluid depth and pressure, which is foundational to fluid statics and hydraulics.

## Mathematical Background

For a static fluid in a gravitational field, the hydrostatic pressure at depth $h$ below the free surface is given by:

$$P(h) = P_0 + \rho g h$$

where:
- $P_0$ — atmospheric pressure at the free surface (Pa),
- $\rho$ — fluid density (kg/m³),
- $g$ — gravitational acceleration (m/s²),
- $h$ — depth below the free surface (m).

This relationship is derived from the condition of static equilibrium applied to a fluid element:

$$\frac{dP}{dh} = \rho g$$

Integrating from the surface downward yields the linear pressure profile above. For water ($\rho = 1000$ kg/m³) and standard gravity ($g = 9.81$ m/s²), the pressure increases by approximately $9810$ Pa per meter of depth.

## Script Description

The script computes and plots the pressure $P(h)$ as a function of depth $h$ from 0 to 20 m using default parameters:

- **Fluid density**: $\rho = 1000$ kg/m³ (water)
- **Gravitational acceleration**: $g = 9.81$ m/s²
- **Maximum depth**: 20 m

The y-axis is inverted to represent depth increasing downward, consistent with the physical convention.

## Parameters

The `plot_pressure_variation_with_depth` function accepts the following keyword arguments:

| Parameter       | Default | Description                          |
|-----------------|---------|--------------------------------------|
| `fluid_density` | 1000    | Fluid density in kg/m³               |
| `g`             | 9.81    | Gravitational acceleration in m/s²   |
| `max_depth`     | 20      | Maximum depth to plot in meters       |

## Output

The script displays a plot of pressure (Pa) on the x-axis versus depth (m) on the y-axis, with depth increasing downward, illustrating the linear pressure increase with depth.
