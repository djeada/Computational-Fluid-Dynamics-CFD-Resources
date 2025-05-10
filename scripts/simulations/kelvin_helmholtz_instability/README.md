## Incompressible Flow and Temperature Transport

This simulation models a 2D incompressible fluid carrying a temperature field to illustrate the Kelvin–Helmholtz instability.  It combines the Navier–Stokes equations for velocity with an advection–diffusion equation for temperature.

## Incompressible Navier–Stokes Equations

The velocity field $\mathbf{u}(x,y,t) = (u,v)$ satisfies

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} =
-\nabla p + \nu \nabla^2\mathbf{u},
\quad
\nabla\cdot\mathbf{u} = 0$$

* $\nu$ is the kinematic viscosity.
* $p(x,y,t)$ is the pressure, enforcing incompressibility.

### Projection Method

I. **Advection**: backtrace fluid parcels along $\mathbf{u}$ and interpolate to form an intermediate $\mathbf{u}^*$.

II. **Diffusion**: apply viscosity via the Laplacian:

$$\mathbf{u}^{**} = \mathbf{u}^* + \nu \Delta t \nabla^2\mathbf{u}^*$$

III. **Pressure solve**: find $p$ from

$$\nabla^2 p = \frac{1}{\Delta t} \nabla\!\cdot\mathbf{u}^{**}$$

then correct

$$\mathbf{u}^{n+1} = \mathbf{u}^{**} - \Delta t \nabla p$$

## Temperature Advection–Diffusion

The scalar temperature field $T(x,y,t)$ evolves by

$$\frac{\partial T}{\partial t} + (\mathbf{u}\cdot\nabla)T=
D \nabla^2 T$$

where $D$ is the thermal diffusion coefficient.

* **Advection** uses the same backtracing and bilinear interpolation as for velocity.
* **Diffusion** adds $D \Delta t \nabla^2 T$ at each step.

## Discretization and Stability

**Grid**: uniform $N_x\times N_y$ cells, periodic in both directions.

**Time step** $\Delta t$ chosen to satisfy a CFL-like constraint for advection:

$$\max|\mathbf{u}|\frac{\Delta t}{\Delta x} \le 1$$

and to make sure stability of diffusion.

**Finite differences** for spatial derivatives:

$$\nabla^2 f_{i,j}
\approx
\frac{f_{i+1,j} + f_{i-1,j} - 2f_{i,j}}{\Delta x^2}
+
\frac{f_{i,j+1} + f_{i,j-1} - 2f_{i,j}}{\Delta y^2}$$

## Initial and Boundary Conditions

* **Velocity**: zero base flow with small sinusoidal perturbations to seed instability.
* **Temperature**: hot region on the left, cold region on the right.
* **Boundaries**: periodic on all sides.

## Visualization

* **Mapping**: temperature mapped to hue, e.g. blue (cold) to red (hot).
* **Rendering**: each grid cell colored and displayed, optionally with grid lines.
* **Loop**: update velocity $\to$ enforce incompressibility $\to$ transport temperature $\to$ render frame.
