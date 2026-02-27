# Wall Shear in Pipe Cross-Section

This script visualizes fully developed laminar (Poiseuille) flow in a circular pipe by drawing the pipe cross-section and overlaying a parabolic velocity profile. Velocity arrows are drawn at multiple radial positions, scaling in length with the local velocity $u(r) = u_{max}(1 - (r/R)^2)$. Labels identify the no-slip condition at the wall, the high-shear region near the wall, and the velocity gradient across the cross-section.

![wall_shear_pipe_cross_section](https://github.com/user-attachments/assets/47c89e71-e6ab-4530-b00b-9b0db72fca68)

## Overview

- Circular pipe cross-section with parabolic axial velocity profile
- Velocity arrows at multiple radii scaled to local flow speed
- Annotations for no-slip condition, shear stress, and velocity gradient
- Highlights the wall region where viscous effects dominate

## Mathematical Background

### Hagen–Poiseuille Velocity Profile

For fully developed, incompressible laminar flow driven by a pressure gradient $\Delta p / L$, the axial velocity at radius $r$ is:

$$u(r) = \frac{\Delta p}{4\mu L}(R^2 - r^2)$$

where $\mu$ is the dynamic viscosity, $R$ is the pipe radius, and $L$ is the pipe length.

### Maximum Velocity

The velocity is maximum at the pipe centerline ($r = 0$):

$$u_{max} = \frac{\Delta p\, R^2}{4\mu L}$$

allowing the profile to be written as $u(r) = u_{max}\!\left(1 - (r/R)^2\right)$.

### Wall Shear Stress

The shear stress is greatest at the wall, where the velocity gradient is steepest:

$$\tau_w = -\mu\frac{\partial u}{\partial r}\bigg|_{r=R} = \frac{\Delta p\, R}{2L}$$

### No-Slip Condition

The fluid velocity vanishes at the solid wall:

$$u(R) = 0$$

## Implementation

1. Define radial positions $r \in [0, R]$ and compute $u(r)$ for the parabolic profile.
2. Draw the pipe circle and shade the fluid region.
3. Place velocity arrows at evenly spaced radii, with arrow length proportional to $u(r)$.
4. Annotate the no-slip boundary, high-shear zone near the wall, and centerline maximum.
5. Display the figure with axis labels and a legend.

## Output

The script displays and saves `wall_shear_pipe_cross_section.png`: a circular pipe cross-section with the parabolic Poiseuille velocity profile, annotated velocity arrows, and labels identifying key flow features including the no-slip wall and maximum centerline velocity.

