# Eulerian Cylinder Flow

This script simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib. It uses the staggered-grid projection and semi-Lagrangian advection scheme of Matthias Müller's "Ten Minute Physics" fluid demo. A uniform inflow enters from the left, and a dye streak released at mid-height is carried around the cylinder into the wake.

## Overview

- Uses a staggered (MAC) grid with velocities on cell faces, and pressure and dye at cell centres. With `RESOLUTION = 100` cells across the 1 m domain height, the grid is 135 × 102 cells including boundary cells.
- Builds a wind tunnel: a left inlet column at `INLET_VELOCITY = 2` m/s, solid top and bottom walls, an open right boundary, and a cylinder of radius `OBSTACLE_RADIUS = 0.15` m centred at (0.4, 0.5) m.
- Removes the velocity divergence every time step with `NUM_ITERATIONS = 20` Gauss–Seidel sweeps with over-relaxation (`OVER_RELAXATION = 1.9`).
- Advects velocity and dye with the semi-Lagrangian (backtracking) method and bilinear interpolation.
- Includes no viscosity term: the flow is inviscid apart from the numerical diffusion of the interpolation. Gravity is supported but set to zero.
- Compiles the grid loops with Numba. The dye concentration is drawn with the `inferno` colour map, from black (clear fluid) to pale yellow (pure dye), and the walls and cylinder are grey.
- Advances $\Delta t = 1/60$ s per time step and draws a frame every 2 steps (1/30 s of flow). The window runs until it is closed; space pauses and the right arrow advances one frame while paused.

## Mathematical Background

The flow is modelled by the incompressible Euler equations with a passive dye marker $m$ (1 for clear fluid, 0 for dye):

$$
\nabla \cdot \mathbf{u} = 0,
\qquad \frac{\partial \mathbf{u}}{\partial t} +
(\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \mathbf{g},
\qquad \frac{\partial m}{\partial t} + \mathbf{u} \cdot \nabla m = 0
$$

Each time step of length $\Delta t = 1/60$ s splits these into three stages.

### 1. Body Forces

$v \leftarrow v + g\,\Delta t$ on faces between two fluid cells ($g = 0$ by default).

### 2. Projection

For every fluid cell with face velocities $u_{i,j}, u_{i+1,j}, v_{i,j}, v_{i,j+1}$ and grid spacing $h$, the discrete divergence is

$$
d = u_{i+1,j} - u_{i,j} + v_{i,j+1} - v_{i,j}
$$

Let $s_k \in \{0, 1\}$ mark each neighbour as solid or fluid, with $s = s_{i-1,j} + s_{i+1,j} + s_{i,j-1} + s_{i,j+1}$. The cell's outflow is removed by moving its fluid-side faces:

$$
u_{i,j} \mathrel{+} = \omega\, s_{i-1,j}\, \frac{d}{s}, \quad u_{i+1,j}
\mathrel{-} = \omega\, s_{i+1,j}\, \frac{d}{s}, \quad v_{i,j} \mathrel{+} = \omega\,
s_{i,j-1}\, \frac{d}{s}, \quad v_{i,j+1} \mathrel{-} = \omega\, s_{i,j+1}\, \frac{d}{s}
$$

Sweeping this over all cells is a Gauss–Seidel iteration, with over-relaxation factor $\omega$, for the pressure Poisson equation $\nabla^2 p = (\rho/\Delta t)\,\nabla \cdot \mathbf{u}^*$ followed by the update $\mathbf{u} = \mathbf{u}^* - (\Delta t/\rho)\nabla p$. The pressure is accumulated as $p \mathrel{+}= (\rho h/\Delta t)\,\omega\,(-d/s)$. After a fixed number of sweeps the divergence is reduced but not exactly zero.

### 3. Semi-Lagrangian Advection

Each velocity sample and dye value is traced back along the velocity field for one time step and interpolated bilinearly at the departure point:

$$
q^{n+1}(\mathbf{x}) = q^n(\mathbf{x} - \Delta t\,\mathbf{u}(\mathbf{x}))
$$

This is stable for any $\Delta t$, but the interpolation smooths the fields. That smoothing acts as numerical viscosity, which lets a wake form behind the cylinder.

## Implementation

- `EulerianCylinderSimulation(resolution)` builds the wind tunnel and stores flat `float32` arrays indexed `i * grid_height + j`: `u`, `v`, `pressure`, `solid` (1 = fluid, 0 = solid) and `density_field` (the dye, 1 = clear fluid, 0 = dye). The constructor marks the walls, sets the inlet velocity, releases the dye streak in the inlet column and calls `set_obstacle` for the cylinder. A smaller `resolution` gives a coarser grid for quick checks.
- `simulate(delta_time, gravity, num_iterations, over_relaxation)` calls the Numba kernels `integrate`, `solve_incompressibility`, `extrapolate` (copies tangential velocities into boundary cells), `advect_velocity` and `advect_dye`. The last two use `sample_field` for bilinear interpolation. `step()` is one `simulate` call with the module constants.
- `dye` returns the dye concentration $1 - m$ as a 2D array with NaN in solid cells. `EulerianCylinderView` shows it with `imshow` and a colour bar, which sits below the map in a reel.
- Parameters are module constants: `DOMAIN_HEIGHT`, `DOMAIN_WIDTH`, `RESOLUTION`, `DELTA_TIME`, `NUM_ITERATIONS`, `OVER_RELAXATION`, the obstacle position and radius, `INLET_VELOCITY`, `STEPS_PER_FRAME` and `N_FRAMES`.

## Usage

```bash
python main.py                                    # animate in a window until it is closed (space pauses)
python main.py --steps 150                        # stop after 150 frames (t = 5 s)
python main.py --no-show --output . --steps 450   # save the final frame (t = 15 s) as a PNG
python main.py --reel reel.mp4                    # 30 s vertical video for Shorts/Reels
```

`--steps N` sets the number of frames; each frame is 2 time steps of 1/60 s. Without `--steps` the window runs until it is closed, while `--no-show` and `--reel` stop after 450 frames ($t = 15$ s). The first steps take a few seconds while Numba compiles the kernels.

## Output

![Dye concentration at t = 15 s](eulerian_cylinder_flow.png)

The figure shows the dye after 450 frames ($t = 15$ s). The grey disc is the cylinder, and the thin grey strips at the left, top and bottom are the solid boundary cells. Clear fluid is black. The dye streak from the inlet (pale yellow) splits around the cylinder into two thin shear layers, which roll up behind it into a wake of alternating vortices. The dye inside the vortices is diluted (orange to purple) by the numerical diffusion of the interpolation. Numerical asymmetries break the symmetry of the wake within about a second, and from then on it sheds vortices periodically: the cross-stream velocity at $x = 0.9$ m on the centreline changes sign with a period of about 0.63 s, a Strouhal number $fD/U \approx 0.24$. A video of the earlier Pygame version is on YouTube:

[![Watch on YouTube](https://img.youtube.com/vi/GYtn9u0awsE/maxresdefault.jpg)](https://youtube.com/shorts/GYtn9u0awsE?si=qlHDFdepFfnIFg8W)

## Related Notes

- [Eulerian and Lagrangian flow descriptions](../../../notes/fluid_mechanics/flow_kinematics/eulerian_lagrangian_flows.md)
- [Navier–Stokes equations (including the Euler equations)](../../../notes/fluid_mechanics/governing_equations/navier_stokes.md)
- [Continuity equation](../../../notes/fluid_mechanics/governing_equations/continuity.md)
- [Drag](../../../notes/fluid_mechanics/viscous_flow/drag.md)
