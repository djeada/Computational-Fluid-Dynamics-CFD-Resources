# NACA 4-Digit Airfoil Profile

This script generates a precise geometric plot of a NACA 4-digit airfoil profile. Given the four-digit designation encoding maximum camber, camber position, and thickness ratio, it computes the camber line via a piecewise parabolic formula and applies the standard NACA thickness distribution to construct the upper and lower surface coordinates. The resulting plot annotates the leading edge, trailing edge, chord line, and camber line to provide a complete visual reference of the airfoil geometry.

## Overview

- Computes the piecewise parabolic camber line from NACA 4-digit parameters
- Applies the NACA thickness distribution formula to determine half-thickness at each chord location
- Constructs upper and lower surface coordinates perpendicular to the camber line
- Annotates key geometric features: leading edge, trailing edge, chord line, and camber line
- Produces a publication-quality plot with equal aspect ratio and labeled axes

## Mathematical Background

### Camber Line

The camber line is defined piecewise using maximum camber $m$ and its chord-fraction position $p$:

$$y_c(x) = \begin{cases} \dfrac{m}{p^2}\!\left(2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right) & x < pc \\[6pt] \dfrac{m}{(1-p)^2}\!\left((1-2p) + 2p\dfrac{x}{c} - \left(\dfrac{x}{c}\right)^2\right) & x \geq pc \end{cases}$$

### NACA Thickness Distribution

The half-thickness $t(x)$ at chord position $x$ is:

$$t(x) = \frac{t_{\max}}{0.2}\!\left(0.2969\sqrt{\frac{x}{c}} - 0.1260\frac{x}{c} - 0.3516\left(\frac{x}{c}\right)^2 + 0.2843\left(\frac{x}{c}\right)^3 - 0.1015\left(\frac{x}{c}\right)^4\right)$$

### Upper and Lower Surfaces

Surface coordinates are offset from the camber line perpendicular to its local slope $\theta = \arctan(dy_c/dx)$:

$$y_u = y_c + t\cos\theta, \qquad y_l = y_c - t\cos\theta$$

$$x_u = x - t\sin\theta, \qquad x_l = x + t\sin\theta$$

## Implementation

1. Parse the NACA 4-digit code to extract $m$, $p$, and $t_{\max}/c$.
2. Discretise the chord $x \in [0, c]$ into a uniform array of points.
3. Evaluate the piecewise camber line $y_c(x)$ and its gradient $dy_c/dx$ at each point.
4. Compute the local camber angle $\theta = \arctan(dy_c/dx)$.
5. Apply the NACA thickness formula to obtain $t(x)$.
6. Calculate upper surface $(x_u, y_u)$ and lower surface $(x_l, y_l)$ using the perpendicular offsets.
7. Plot both surfaces, the camber line, and the chord line; annotate leading and trailing edges.

## Output

The script produces a single figure showing the complete airfoil cross-section with the upper and lower surfaces drawn as solid curves, the camber line as a dashed curve, and the chord line as a reference. Leading and trailing edge positions are marked, and the plot uses an equal aspect ratio so the true airfoil shape is preserved.

![airfoil_profile](https://github.com/user-attachments/assets/1bfe71cf-eeec-45c9-ba34-a9a142074655)
