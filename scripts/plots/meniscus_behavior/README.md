
# Meniscus Behavior

This script visualizes the formation of menisci in glass tubes by plotting two side-by-side panels: (a) water in glass, exhibiting an upward concave meniscus due to adhesive forces exceeding cohesive forces, and (b) mercury in glass, exhibiting a downward convex meniscus where cohesion dominates. Each meniscus is approximated as a parabolic curve of the form $\pm 0.5x^2$, illustrating how contact angle determines the curvature direction and the resulting capillary rise or depression.

![meniscus_behavior](https://github.com/user-attachments/assets/9d3eee1d-b9f8-4ed2-b7cb-e95a23bec953)

## Overview

- Two-panel figure comparing concave (water) and convex (mercury) menisci
- Parabolic curve approximation $\pm 0.5x^2$ for each meniscus shape
- Annotations for contact angle, liquid type, and wetting behavior
- Illustrates the link between surface energy and capillary action

## Mathematical Background

### Contact Angle

The contact angle $\theta_c$ is measured between the liquid–solid interface and the liquid surface at the point of contact:

$$\theta_c < 90^\circ \Rightarrow \text{hydrophilic (water on glass)} \Rightarrow \text{liquid climbs} \Rightarrow \text{concave meniscus}$$

$$\theta_c > 90^\circ \Rightarrow \text{hydrophobic (mercury on glass)} \Rightarrow \text{liquid depresses} \Rightarrow \text{convex meniscus}$$

### Young's Equation

Force balance at the three-phase contact line gives the Young equation relating the three interfacial tensions:

$$\sigma_{SG} = \sigma_{SL} + \sigma_{LG}\cos\theta_c$$

### Capillary Rise

The equilibrium height of liquid in a tube of radius $r$ is determined by balancing surface tension and gravitational forces:

$$h = \frac{2\sigma\cos\theta_c}{\rho g r}$$

where $\sigma$ is the liquid–gas surface tension, $\rho$ is fluid density, $g$ is gravitational acceleration, and $r$ is the tube radius. A negative $h$ corresponds to capillary depression.

## Implementation

1. Define a horizontal coordinate array $x \in [-1, 1]$.
2. Compute the concave parabola $y = +0.5x^2$ for the water panel.
3. Compute the convex parabola $y = -0.5x^2$ for the mercury panel.
4. Plot each curve with tube walls, fill the liquid region, and annotate with contact angle and labels.
5. Render both panels side by side using `matplotlib.pyplot.subplots`.

## Output

The script displays a two-panel figure saved as `meniscus_behavior.png`, showing the concave water meniscus on the left and the convex mercury meniscus on the right, each annotated with the relevant contact angle regime and physical interpretation.
