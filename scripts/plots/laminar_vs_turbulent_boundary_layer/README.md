# Laminar vs. Turbulent Boundary Layer Profiles

This script compares the normalised velocity profiles of laminar and turbulent boundary layers on the same axes. The laminar profile follows a quadratic approximation while the turbulent profile uses the empirical one-seventh power law. Plotting both together makes the fundamental difference in profile shape immediately visible: the turbulent boundary layer is fuller and carries higher momentum near the wall, which directly raises wall shear stress.

## Overview

- Computes laminar profile using the quadratic Blasius-like approximation
- Computes turbulent profile using the 1/7 power law
- Plots both normalised velocity profiles against the normalised wall distance $\eta = y/\delta$
- Annotates each curve with descriptive labels (thin/smooth vs. thicker/fuller)
- Highlights the higher near-wall gradient of the turbulent profile

## Mathematical Background

### Laminar Boundary Layer Approximation

$$\frac{u}{U_\infty} = 2\frac{y}{\delta} - \left(\frac{y}{\delta}\right)^2 = 2\eta - \eta^2$$

This quadratic profile satisfies the no-slip condition at the wall and matches the free-stream velocity at $\eta = 1$.

### Turbulent Boundary Layer Power Law

$$\frac{u}{U_\infty} = \left(\frac{y}{\delta}\right)^{1/7} = \eta^{1/7}$$

The 1/7 power law is an empirical fit valid for moderate Reynolds numbers and gives a much fuller profile than the laminar case.

### Wall Shear Stress

$$\tau_w = \mu \left.\frac{\partial u}{\partial y}\right|_{y=0}$$

The steeper near-wall gradient of the turbulent profile yields a larger $\tau_w$ compared with the laminar case.

## Implementation

1. Define `eta = np.linspace(0, 1, 200)` as the normalised wall-distance array.
2. Compute laminar profile: `u_lam = 2*eta - eta**2`.
3. Compute turbulent profile: `u_turb = eta**(1/7)`.
4. Plot both profiles with `eta` on the y-axis and velocity ratio on the x-axis.
5. Add annotations labelling each curve and describing the profile character.
6. Set axis labels, title, legend, and grid; display the figure.

## Output

The script displays a single figure with two normalised velocity profiles plotted against $\eta$. The turbulent curve sits noticeably to the right of the laminar curve, illustrating its fuller shape and higher near-wall momentum. Annotations on the plot identify each profile and note the physical implications for wall shear stress.
