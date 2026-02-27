# Rayleigh-Bénard Convection Simulation

This project simulates Rayleigh-Bénard convection — buoyancy-driven flow between a hot lower plate and a cold upper plate — using a simplified thermal-velocity coupling on a 128×128 grid rendered in real time with Pygame. Watch it in action: [![YouTube](https://i9.ytimg.com/vi/E_N-ld6Vfwo/mqdefault.jpg)](https://youtube.com/shorts/E_N-ld6Vfwo)

## Overview

- **128×128 grid** with a linear temperature gradient: $T=1$ (bottom, hot) to $T=0$ (top, cold).
- **Buoyancy coupling**: hot fluid rises, cold fluid sinks, forming convection rolls.
- **Multiprocessing**: cell updates parallelized across cores for performance.
- **Pygame visualization**: 400×400 window at 60 fps; temperature mapped to an RGB color palette.

## Mathematical Background

### Rayleigh Number

The onset of convection is governed by the dimensionless Rayleigh number:

$$Ra = \frac{g\,\beta\,\Delta T\,H^3}{\nu\,\kappa}$$

where $g$ is gravitational acceleration, $\beta$ is the thermal expansion coefficient, $\Delta T$ the temperature difference across height $H$, $\nu$ kinematic viscosity, and $\kappa$ thermal diffusivity. Convection cells form when $Ra > Ra_c \approx 1708$.

### Temperature Advection–Diffusion

The temperature field $T$ evolves via advection by the local velocity and thermal diffusion:

$$\frac{\partial T}{\partial t} + \mathbf{u}\cdot\nabla T = \kappa\,\nabla^2 T$$

### Buoyancy and Velocity Update

The vertical velocity is driven by the local temperature gradient; hot cells ($T > 0.5$) experience upward buoyancy:

$$v_{i,j}^{n+1} = v_{i,j}^n + \alpha\,(T_{i,j} - T_{i-1,j})$$

where $\alpha$ is a coupling coefficient controlling convective strength. Buoyancy is proportional to $\beta(T - T_\text{ref})$.

## Implementation

1. Initialize the 128×128 temperature grid with $T_{i,j} = 1 - i/N$ (linear gradient) and velocity fields $u$, $v$ to zero.
2. Each frame, launch a multiprocessing pool to update each cell's temperature from its four neighbors and the local velocity.
3. Update the velocity field from the vertical temperature gradient to model buoyancy.
4. Clamp temperatures to $[0,1]$ and enforce fixed boundary conditions: bottom $T=1$, top $T=0$.
5. Map each cell's temperature to an RGB color (cold → blue, hot → red) and draw to the Pygame surface.
6. Handle Pygame events and tick the clock at 60 fps.

## Output

The Pygame window displays the evolving temperature field as a real-time color map:

- **Convection rolls** emerge as warm plumes rise from the bottom and cool fluid descends from the top.
- **Color gradient** transitions from deep blue (cold, top) to bright red (hot, bottom), with intermediate hues marking the mixing layer.
- The simulation runs continuously until the window is closed.

## Running the Script

```bash
pip install pygame numpy
python rayleigh_benard_convection.py
```

Adjust `GRID_SIZE`, `ALPHA` (buoyancy coupling), and `FPS` at the top of the script to explore different convection regimes.
