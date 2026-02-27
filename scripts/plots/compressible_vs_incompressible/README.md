# Compressible vs. Incompressible Pipe Flow

This script presents a side-by-side comparison of incompressible and compressible pipe flow on a 40×10 computational grid. The incompressible case uses a parabolic velocity profile that remains identical at every streamwise cross-section, while the compressible case features an accelerating parabolic profile that grows in magnitude along the pipe to reflect the density changes caused by compressibility effects. Both panels use colour maps for velocity magnitude and quiver arrows for flow direction, making the fundamental difference between the two flow regimes immediately apparent.

## Overview

- Generates a 40×10 grid representing a rectangular pipe cross-section
- Implements a fully developed parabolic profile for the incompressible case
- Implements a streamwise-accelerating parabolic profile for the compressible case
- Renders colour maps of velocity magnitude with consistent colour scales
- Overlays quiver arrows to visualise the local flow direction in both panels

## Mathematical Background

### Incompressible Velocity Profile

For incompressible flow the velocity profile is fully developed and identical at every streamwise location $x$:

$$u_{\text{incomp}}(y) = U_{\max}\left[1 - \left(\frac{y - y_{\text{mid}}}{y_{\text{mid}}}\right)^2\right]$$

The continuity equation $\nabla \cdot \mathbf{u} = 0$ enforces a constant cross-sectional profile with no streamwise variation.

### Compressible Velocity Profile

Compressibility causes the fluid density to decrease as velocity increases. The modelled profile accelerates with $x$:

$$u_{\text{comp}}(x, y) = \left(U_{\text{inlet}} + U_{\text{slope}} \cdot x\right)\left[1 - \left(\frac{y - y_{\text{mid}}}{y_{\text{mid}}}\right)^2\right]$$

### Continuity for Compressible Flow

The compressible continuity equation requires:

$$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho\, \mathbf{u}) = 0$$

As velocity increases along the pipe, density decreases to satisfy mass conservation, a key departure from the incompressible assumption.

## Implementation

1. Define the 40×10 grid with uniform node spacing.
2. Compute the incompressible profile $u_{\text{incomp}}(y)$ across all streamwise positions.
3. Compute the compressible profile $u_{\text{comp}}(x, y)$ with a linear streamwise velocity increase.
4. Create a side-by-side figure with two subplots.
5. Render colour maps of velocity magnitude using `pcolormesh` or equivalent.
6. Overlay quiver arrows sampled at a coarser grid to avoid clutter.
7. Add colour bars, axis labels, and titles identifying each flow regime.

## Output

The script produces a two-panel figure. The left panel shows the incompressible flow with a uniform colour band reflecting the constant parabolic profile, while the right panel shows the compressible flow with a colour gradient that intensifies from inlet to outlet. Quiver arrows confirm the direction and relative speed of the flow in each case.

![compressible_vs_incompressible](https://github.com/user-attachments/assets/73f166dd-d6da-45aa-91b2-16f0cdd52d8e)
