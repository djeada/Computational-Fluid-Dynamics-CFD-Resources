# Ship Hull in Water — Free-Surface Flow Visualisation

This script draws a stylised 2D cross-section of a ship hull together with a free-surface wave pattern, annotating the Froude number formula and key hydrodynamic features. It serves as a visual reference for understanding wave-making resistance and the relationship between hull speed and free-surface waves in naval hydrodynamics.

## Overview

- Renders a schematic hull cross-section below a sinusoidal free surface
- Annotates the Froude number formula directly on the figure
- Highlights the Kelvin wake half-angle of approximately 19.47°
- Indicates the hull-speed Froude number of Fr ≈ 0.35 where wave resistance is minimised

## Mathematical Background

### Free-Surface Wave Profile

$$\eta(x) = A\sin\!\left(\frac{2\pi x}{\lambda}\right)$$

### Froude Number

$$Fr = \frac{U}{\sqrt{gL}}$$

where $U$ is the ship speed, $g$ is gravitational acceleration, and $L$ is the waterline length.

### Hull Speed

$$Fr \approx 0.35 \quad \Longrightarrow \quad \text{minimum wave resistance}$$

### Kelvin Wake Angle

$$\theta_K = \arcsin\!\left(\frac{1}{3}\right) \approx 19.47°$$

The Kelvin wake angle is universal: independent of ship speed for deep water.

## Implementation

1. Define hull geometry as a closed polygon representing the cross-sectional profile.
2. Generate a sinusoidal free-surface elevation $\eta(x)$ across the domain.
3. Draw and fill the hull below the waterline using a shaded patch.
4. Overlay the wave profile at the free surface.
5. Annotate the figure with the Froude number formula and the Kelvin wake angle.

## Output

The script displays a 2D schematic figure showing the hull cross-section submerged beneath a sinusoidal wave pattern. Annotations label the Froude number expression and the 19.47° Kelvin wake half-angle, providing an intuitive reference for free-surface CFD post-processing.

![ship_hull_in_water](https://github.com/user-attachments/assets/f1265bd2-3b3c-4860-87a2-7a90a9fdc064)
