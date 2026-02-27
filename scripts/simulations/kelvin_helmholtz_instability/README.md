# Kelvin–Helmholtz Instability Simulation

This simulation models a 2D incompressible fluid carrying a temperature field to illustrate the Kelvin–Helmholtz instability — the characteristic rolling vortices that form at the shear interface between fluid layers moving at different velocities.

## Overview

- **2D incompressible Navier–Stokes** solved with a projection (pressure-correction) method.
- **Temperature advection–diffusion** coupled to the velocity field for visual contrast.
- **Periodic boundary conditions** on all sides; instability seeded by sinusoidal velocity perturbations.
- **Real-time color rendering**: temperature mapped to hue (blue = cold, red = hot).

## Mathematical Background

### Incompressible Navier–Stokes Equations

The velocity field $\mathbf{u}=(u,v)$ satisfies:

$$\frac{\partial\mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu\nabla^2\mathbf{u}, \quad \nabla\cdot\mathbf{u}=0$$

### Projection Method

I. **Advection**: backtrace fluid parcels along $\mathbf{u}$ and interpolate to form an intermediate $\mathbf{u}^*$.

II. **Diffusion**: apply viscosity via the Laplacian:

$$\mathbf{u}^{**} = \mathbf{u}^* + \nu\,\Delta t\,\nabla^2\mathbf{u}^*$$

III. **Pressure solve** from the Poisson equation, then correct velocity to enforce $\nabla\cdot\mathbf{u}=0$:

$$\nabla^2 p = \frac{1}{\Delta t}\nabla\cdot\mathbf{u}^{**}, \quad \mathbf{u}^{n+1} = \mathbf{u}^{**} - \Delta t\,\nabla p$$

### Temperature Advection–Diffusion

The scalar temperature $T(x,y,t)$ evolves by:

$$\frac{\partial T}{\partial t} + (\mathbf{u}\cdot\nabla)T = D\,\nabla^2 T$$

where $D$ is the thermal diffusivity. Advection uses the same backtracing as velocity; diffusion adds $D\,\Delta t\,\nabla^2 T$ each step.

### Discretization and Stability

Grid: uniform $N_x\times N_y$ cells, periodic in both directions. Time step satisfies the CFL condition:

$$\max|\mathbf{u}|\frac{\Delta t}{\Delta x} \le 1$$

Second-order central-difference Laplacian:

$$\nabla^2 f_{i,j} \approx \frac{f_{i+1,j}+f_{i-1,j}-2f_{i,j}}{\Delta x^2} + \frac{f_{i,j+1}+f_{i,j-1}-2f_{i,j}}{\Delta y^2}$$

## Implementation

1. Initialize a uniform $N_x\times N_y$ grid with periodic boundaries; set opposing base velocity layers and a sinusoidal perturbation to seed the instability.
2. Assign the temperature field: hot region (one side) $T=1$, cold region (other side) $T=0$.
3. Each time step: backtrace velocity and temperature for advection via bilinear interpolation.
4. Apply viscous diffusion to velocity and thermal diffusion to temperature.
5. Solve the pressure Poisson equation; project velocity onto the divergence-free subspace.
6. Update arrays in-place and re-apply periodic boundary wrapping.
7. Render each cell colored by temperature and display the frame.

## Output

The rendered window shows the evolving temperature field colored from blue (cold) to red (hot):

- Initially a sharp interface between the two fluid layers.
- Sinusoidal perturbations grow into characteristic **Kelvin–Helmholtz rolls** that curl and entrain fluid from both layers.
- The rolls cascade into smaller-scale turbulent mixing as the simulation progresses.
