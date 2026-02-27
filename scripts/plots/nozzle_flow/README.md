# Converging-Diverging Nozzle Flow

This script visualises steady flow through a converging-diverging (de Laval) nozzle by plotting the nozzle geometry and colouring streamlines by local Mach number. The top wall converges linearly from y = 0.8 to y = 0.4 over x ∈ [0, 1] and then diverges from y = 0.4 to y = 0.7 over x ∈ [1, 2]. Velocity at each cross-section is derived from mass conservation, and the Mach number field is overlaid as a colourmap, making the acceleration through the throat immediately apparent.

## Overview

- Defines nozzle geometry with a linear converging and diverging wall profile
- Computes cross-sectional velocity via the continuity equation
- Derives Mach number from local velocity and speed of sound
- Plots nozzle walls and filled streamlines coloured by Mach number
- Includes a colourbar and axis labels for physical interpretation

## Mathematical Background

### Continuity Equation (Incompressible Approximation)

$$A_1 u_1 = A_2 u_2 \implies u(x) = \frac{Q}{A(x)}$$

where $Q$ is the volumetric flow rate and $A(x) = y_{\text{top}}(x)$ is the local cross-sectional height (unit depth assumed).

### Wall Geometry

$$y_{\text{top}}(x) = \begin{cases} 0.8 - 0.4x & 0 \le x \le 1 \\ 0.4 + 0.3(x-1) & 1 < x \le 2 \end{cases}$$

### Mach Number

$$M = \frac{u}{c_s}$$

where $c_s$ is the speed of sound in the working fluid. Flow accelerates in the converging section and decelerates in the diverging section.

## Implementation

1. Define x arrays for the converging (x ∈ [0, 1]) and diverging (x ∈ [1, 2]) sections.
2. Compute the top-wall profile `y_top` piecewise; bottom wall is fixed at y = 0.
3. Set a reference flow rate Q and compute `u(x) = Q / y_top(x)`.
4. Compute Mach number `M = u / c_s` at each x location.
5. Build a 2-D grid and interpolate velocity/Mach fields for streamline plotting.
6. Plot nozzle walls as filled polygons and overlay streamlines coloured by M; add colourbar.

## Output

The script displays the nozzle geometry with streamlines coloured by Mach number. The throat region (x = 1) shows the highest velocities and Mach numbers in warm colours. The converging and diverging sections are clearly delineated, and the colourbar maps colour to Mach number magnitude.
