# Flow Separation in a Boundary Layer

This script illustrates the phenomenon of boundary layer separation by plotting two distinct flow regions side by side. An attached boundary layer grows along a surface from $x = -1$ to $x = 0$, following the characteristic $\sqrt{x}$ thickness growth of laminar (Blasius) flow. Beyond the separation point at $x = 0$, the script draws a recirculation zone extending to $x = 1.5$ where the boundary layer has detached from the surface and reversed-flow streamlines indicate a separated, recirculating region. Free-stream arrows at the top of the domain and a label at the separation point complete the annotation.

## Overview

- Plots the attached boundary layer with $\delta \sim \sqrt{x}$ growth from $x = -1$ to $x = 0$
- Draws the separated recirculation zone with an inverted $\sqrt{}$ shape from $x = 0$ to $x = 1.5$
- Shows free-stream arrows above the boundary layer indicating undisturbed outer flow
- Marks the separation point at $x = 0$ with a label and vertical indicator
- Demonstrates the qualitative transition from attached to separated flow

## Mathematical Background

### Laminar Boundary Layer Growth

For laminar flow over a flat plate the boundary layer thickness grows as (Blasius solution):

$$\delta(x) \sim \sqrt{x}$$

More precisely, $\delta(x) \approx 5x / \sqrt{Re_x}$ where $Re_x = U_\infty x / \nu$.

### Separation Criterion

Flow separation occurs when an adverse pressure gradient $\partial p / \partial x > 0$ decelerates the near-wall fluid to zero velocity. Prandtl's separation criterion is:

$$\left.\frac{\partial u}{\partial y}\right|_{y=0} = 0$$

### Post-Separation Recirculation

Downstream of the separation point the wall shear stress reverses sign and a recirculation zone forms where:

$$u(x, y) < 0 \quad \text{near the wall}$$

### Adverse Pressure Gradient

The separation is driven by an adverse pressure gradient which decelerates the boundary layer faster than turbulent mixing can re-energise it:

$$\frac{\partial p}{\partial x} > 0 \implies \text{risk of separation}$$

## Implementation

1. Define the attached region $x \in [-1, 0]$ and compute $\delta(x) = C\sqrt{x + 1}$ for a scaling constant $C$.
2. Fill the boundary layer region between the wall and $\delta(x)$ with a shaded area.
3. Define the separated region $x \in [0, 1.5]$ and draw a recirculation envelope growing downward from the wall.
4. Add horizontal free-stream arrows above the boundary layer edge.
5. Mark the separation point at $x = 0$ with a vertical dashed line and text label.
6. Label the attached layer, recirculation zone, and free-stream regions.

## Output

The script produces a schematic diagram with the wall along the bottom edge. The left portion shows the attached boundary layer growing smoothly from the leading edge to the separation point. The right portion shows the recirculation bubble below the separated shear layer. Free-stream arrows at the top remain straight and undisturbed throughout the domain.

![flow_separation_boundary_layer](https://github.com/user-attachments/assets/aac53dde-9acf-4f5f-857d-00ef54ecbf6b)
