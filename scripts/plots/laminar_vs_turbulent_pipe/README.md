# Laminar vs Turbulent Pipe Flow

This script plots the radial velocity profiles for laminar and turbulent pipe flow side by side, enabling direct visual comparison of their shapes. The laminar profile follows the Hagen–Poiseuille parabola, while the turbulent profile uses the empirical 1/7 power law. Radius is plotted on the vertical axis and velocity on the horizontal axis, with annotations highlighting the key differences between the two regimes.

![laminar_vs_turbulent_flow](https://github.com/user-attachments/assets/1af25fd7-75f3-4687-8ecb-2d24e05a7793)

## Overview

- Side-by-side panels for laminar (parabolic) and turbulent (power-law) velocity profiles
- Radius on the y-axis and velocity on the x-axis for intuitive pipe-cross-section reading
- Annotations marking the centerline maximum, wall no-slip condition, and profile fullness
- Illustrates why turbulent flow transfers momentum more effectively across the pipe

## Mathematical Background

### Laminar Profile (Hagen–Poiseuille)

For $Re < 2300$, the axial velocity follows a parabolic distribution:

$$u(r) = u_{max}\left(1 - \left(\frac{r}{R}\right)^{\!2}\right)$$

The mean velocity is exactly half the centerline velocity: $\bar{u} = u_{max}/2$.

### Turbulent Profile (1/7 Power Law)

For $Re > 4000$, the time-averaged turbulent profile is approximated by the empirical power law:

$$u(r) = u_{max}\left(1 - \frac{r}{R}\right)^{\!1/7}$$

This profile is significantly fuller than the parabola, with $\bar{u} \approx 0.817\,u_{max}$.

### Reynolds Number

The dimensionless Reynolds number determines the flow regime:

$$Re = \frac{\rho\, u_{avg}\, D}{\mu}$$

where $D = 2R$ is the pipe diameter. Transition from laminar to turbulent occurs roughly in the range $2300 < Re < 4000$.

## Implementation

1. Define the radial coordinate $r \in [-R, R]$ (or $[0, R]$ mirrored symmetrically).
2. Compute the laminar profile $u_{lam}(r)$ using the parabolic formula.
3. Compute the turbulent profile $u_{turb}(r)$ using the 1/7 power law.
4. Plot each profile in a separate panel with radius on the y-axis and velocity on the x-axis.
5. Add annotations for $u_{max}$, no-slip at the wall, and a note on profile fullness.

## Output

The script displays and saves `laminar_vs_turbulent_pipe.png`: two velocity profile plots showing the narrow, pointed laminar parabola alongside the broader, flatter turbulent power-law profile, annotated to highlight the contrasting momentum distributions.

