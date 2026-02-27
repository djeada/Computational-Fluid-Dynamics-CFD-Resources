# Flow Rate Through a Circular Pipe

This script visualises volumetric flow rate through a circular pipe by computing the cross-sectional area from the pipe radius and combining it with the mean flow velocity. Given the pipe radius, mean velocity, and pipe length, it calculates $Q = \pi r^2 v$ and produces a diagram of the pipe with annotated flow direction arrows. The visualisation assumes a uniform (plug) velocity profile, making it suitable for introductory illustrations of the continuity principle.

## Overview

- Accepts pipe radius $r$, mean velocity $v$, and pipe length $L$ as inputs
- Computes the circular cross-sectional area $A = \pi r^2$
- Calculates volumetric flow rate $Q = A \cdot v$
- Draws a rectangular pipe cross-section with inlet and outlet labels
- Overlays evenly spaced flow direction arrows scaled to the velocity magnitude

## Mathematical Background

### Cross-Sectional Area

For a circular pipe of radius $r$, the cross-sectional area is:

$$A = \pi r^2$$

### Volumetric Flow Rate

The volumetric flow rate relates the cross-sectional area to the mean velocity $v$:

$$Q = A \cdot v = \pi r^2 v \quad [\text{m}^3/\text{s}]$$

### Uniform Velocity Assumption

The plug (uniform) velocity profile assumes every fluid element moves at the same speed $v$ across the entire cross-section:

$$u(r') = v \quad \text{for all } r' \in [0, r]$$

This is an idealisation; real pipe flows exhibit parabolic (Hagen–Poiseuille) profiles in the laminar regime.

### Mass Flow Rate

If the fluid density $\rho$ is known, the mass flow rate follows directly:

$$\dot{m} = \rho\, Q = \rho\, \pi r^2 v \quad [\text{kg/s}]$$

## Implementation

1. Accept `pipe_radius`, `velocity`, and `pipe_length` as input parameters.
2. Compute $A = \pi r^2$ and $Q = A \cdot v$.
3. Draw a rectangle representing the pipe with height $2r$ and length $L$.
4. Place uniformly spaced horizontal arrows inside the pipe pointing in the flow direction.
5. Annotate the figure with the computed values of $A$, $Q$, and the input parameters.
6. Label the inlet and outlet faces of the pipe.

## Output

The script produces a schematic diagram of the pipe viewed from the side. Horizontal arrows inside the pipe indicate the flow direction, and a text annotation displays the computed cross-sectional area and volumetric flow rate. The pipe radius and length are labeled on the diagram axes.

![flow_rate](https://github.com/user-attachments/assets/9c141451-1a94-4067-9a25-5f7cb0486c61)
