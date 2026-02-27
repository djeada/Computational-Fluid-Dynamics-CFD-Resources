# Velocity Layers and Viscosity

This script visualises a fluid divided into three discrete velocity layers — slow, medium, and fast — and annotates the velocity gradient and viscous shear forces acting between adjacent layers. It provides an intuitive illustration of Newton's law of viscosity and momentum transport in laminar shear flow.

## Overview

- Draws three horizontal fluid layers with velocities 0, 5, and 10 (arbitrary units)
- Annotates the velocity gradient $du/dy$ between each pair of adjacent layers
- Indicates the direction and magnitude of viscous shear stress with arrows
- Highlights momentum transport from the fast layer to the slow layer

## Mathematical Background

### Newton's Law of Viscosity

$$\tau = \mu\frac{du}{dy}$$

where $\tau$ is the shear stress (Pa), $\mu$ is the dynamic viscosity (Pa·s), and $du/dy$ is the velocity gradient normal to the flow direction.

### Linear Velocity Profile — Couette Flow

$$u(y) = U_w \cdot \frac{y}{h}$$

where $U_w$ is the velocity of the moving wall and $h$ is the channel height. The shear stress is uniform throughout: $\tau = \mu U_w / h$.

### Momentum Transport

Viscous forces transport momentum from regions of high velocity to regions of low velocity, opposing the relative motion between layers and generating the shear stress $\tau$.

## Implementation

1. Define three horizontal layer bands with assigned velocity values [0, 5, 10].
2. Draw filled rectangles representing each layer, coloured by velocity magnitude.
3. Add horizontal arrows showing the velocity of each layer.
4. Annotate inter-layer boundaries with the velocity gradient formula $\tau = \mu\,du/dy$.
5. Add a legend and axis labels describing the physical setup.

## Output

The script displays a schematic figure of three stacked fluid layers with colour-coded velocities. Arrows illustrate the flow speed in each layer, and annotations at layer interfaces label the viscous shear stress formula and the direction of momentum transport.

![velocity_layers_viscosity](https://github.com/user-attachments/assets/0ac9ac84-a609-41c8-ba58-311b73f7795b)
