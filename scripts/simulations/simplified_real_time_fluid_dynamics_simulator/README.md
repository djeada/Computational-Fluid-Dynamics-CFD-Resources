# Simplified Real-Time Fluid Dynamics Simulator

This script is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window. The `FluidSimulation` class advances a velocity field and a passive density field on an Eulerian grid inside a closed box, using implicit diffusion, semi-Lagrangian advection and a pressure projection. A short demonstration is on YouTube: [![Watch on YouTube](https://img.youtube.com/vi/auwaTfkpIXo/maxresdefault.jpg)](https://youtube.com/shorts/auwaTfkpIXo)

## Overview

- **Grid**: velocity components $(V_x, V_y)$ and density on a collocated 200 × 150 grid (`GRID_WIDTH`, `GRID_HEIGHT`).
- **Diffusion**: implicit (backward Euler) for velocity and density. The linear system is solved with 20 Jacobi iterations.
- **Advection**: semi-Lagrangian back-tracing with bilinear interpolation for velocity and density.
- **Projection**: the velocity is made divergence-free by a pressure Poisson solve (20 Jacobi iterations). It is applied after diffusion and again after advection.
- **Walls**: `set_bnd` enforces solid walls on all four sides.
- **Interaction**: a left click in the window adds 1000 units of density and a random velocity kick of up to ±200 in each component at the clicked cell, drawn from a seeded generator. Clicks are ignored while the toolbar's zoom or pan mode is active. With `--auto-inject`, and always without a window (`--no-show` or `--reel`), a swaying plume is injected at the bottom centre before every solver step.
- **Display**: the density is drawn from black through blue to white. Full blue is $\rho = 0.255$ (`DENSITY_BLUE`) and white is $\rho = 0.51$, so only the jet's core and fresh click puffs are lighter than full blue.

## Mathematical Background

### Governing Equations

$$
\frac{\partial \mathbf{u}}{\partial t} = -(\mathbf{u}\cdot\nabla)\mathbf{u} - \nabla p +
\nu\nabla^2\mathbf{u},
\qquad \nabla\cdot\mathbf{u} = 0
$$

```math
\frac{\partial \rho}{\partial t} = -(\mathbf{u}\cdot\nabla)\rho + D\,\nabla^2\rho
```

External sources (mouse clicks or the scripted plume) are added to $\mathbf{u}$ and $\rho$ before a step.

### Implicit Diffusion

```math
(\mathbf{I} - \nu\,\Delta t\,\nabla^2)\,\mathbf{u}^{n+1} = \mathbf{u}^n
```

In `diffuse` this becomes the Jacobi update

```math
x_{i,j} \leftarrow
\frac{x^0_{i,j} + a\,(x_{i-1,j}+x_{i+1,j}+x_{i,j-1}+x_{i,j+1})}{1+4a},
\qquad a = \Delta t\,\nu\, N_x N_y
```

with $N_x, N_y$ the interior grid sizes (Stam's $`a = \Delta t\,\nu N^2`$ for a square grid of spacing $1/N$). The exact backward-Euler step is unconditionally stable. The system is diagonally dominant, so the fixed 20 Jacobi iterations converge towards it without ever amplifying the solution.

### Semi-Lagrangian Advection

```math
q^{n+1}(\mathbf{x}) = q^n\!\left(\mathbf{x} - \Delta t_0\,\mathbf{u}(\mathbf{x})\right),
\qquad \Delta t_0 = \Delta t\, N_x
```

The departure point is clamped to the interior and $q^n$ is interpolated bilinearly. The new value is a weighted average of old values, so the step is stable for any $\Delta t$.

### Pressure Projection

With $h = 1/W$ (where $W$ is the grid width), `project` solves

$$
\nabla^2 q = \nabla\cdot\mathbf{u}^*
$$

by Jacobi iterations of $`q_{i,j} = \tfrac14\left(\text{div}_{i,j} + q_{i-1,j}+q_{i+1,j}+q_{i,j-1}+q_{i,j+1}\right)`$, where $`\text{div}_{i,j} = -\tfrac{h}{2}\left(V_{x,i+1}-V_{x,i-1}+V_{y,j+1}-V_{y,j-1}\right)`$. It then corrects the velocity:

$$
\mathbf{u} = \mathbf{u}^* - \nabla q
$$

Here $`q = \Delta t\,p/\rho`$ absorbs the time step and density.

### Boundary Conditions (`set_bnd`)

- Horizontal velocity changes sign at the left and right walls, and vertical velocity at the top and bottom walls, so there is no flow through the walls.
- All other quantities have zero normal gradient.
- Each corner is the average of its two neighbours.

## Implementation

- `FluidSimulation.vel_step` runs `diffuse` → `project` → `advect` → `project`, swapping the `Vx0`/`Vy0` scratch arrays as in Stam's reference code.
- `FluidSimulation.dens_step` runs `diffuse` → `advect` for the density. `step` calls `inject_plume` when `auto_inject` is set, then `vel_step` and `dens_step`.
- `add_density` and `add_velocity` inject sources at a grid cell. `add_click` adds a click's density and random kick, and `inject_plume` adds the scripted source (`PLUME_DENSITY`, `PLUME_VELOCITY`, `PLUME_SWAY`).
- `FluidView` draws the density with `imshow`. Row 0 of the grid is the top of the box, so the image uses `origin="upper"` and the y axis counts cells downwards. Its `on_click` handler converts a left click to the nearest grid cell and calls `add_click`.
- `ANIMATION` and `main` use the shared runner in `scripts/_animation.py`. `main` turns the plume on for `--auto-inject`, `--no-show` and `--reel`. A frame is `STEPS_PER_FRAME = 2` solver steps, headless runs and reels default to `N_FRAMES = 450` frames ($t = 90$), and the window runs until it is closed.
- Parameters are module constants: `DIFFUSION`, `VISCOSITY`, `TIME_STEP` (0.1), `SOLVER_ITERATIONS`, `GRID_WIDTH` and `GRID_HEIGHT`. The generator is seeded with `SEED`.

## Usage

```bash
python main.py                                    # interactive: left-click to add smoke (space pauses)
python main.py --auto-inject                      # watch the scripted plume in a window
python main.py --no-show --output . --steps 150   # scripted plume, save the frame at t = 30 as a PNG
python main.py --reel reel.mp4                    # 30 s vertical video of the plume for Shorts/Reels
```

`--steps N` sets the number of frames; each frame is 2 solver steps of $\Delta t = 0.1$.

## Output

![Stable Fluids smoke plume after 300 solver steps](simplified_real_time_fluid_dynamics_simulator.png)

The image shows the scripted plume after 150 frames (300 solver steps, $t = 30$), with the density colour bar on the right:

- **Jet**: a bright, swaying jet rises from the source near the bottom of the box. Only its core next to the source is dense enough ($\rho > 0.255$) to be drawn lighter than full blue.
- **Smoke clouds**: the smoke rolls up into two large vortices and spreads into diffuse blue clouds as it fills the upper part of the closed box.

Over the default 450 frames ($t = 90$) the clouds spread until most of the box is a blue haze, while the jet keeps swaying.

Stable Fluids trades accuracy for robustness. Semi-Lagrangian advection and the few Jacobi iterations add strong numerical dissipation and leave a small residual divergence, so the result is visually plausible rather than a quantitative Navier-Stokes solution.

## Related Notes

- [Navier-Stokes equations](../../../notes/fluid_mechanics/governing_equations/navier_stokes.md)
- [Eulerian and Lagrangian descriptions of flow](../../../notes/fluid_mechanics/flow_kinematics/eulerian_lagrangian_flows.md)
- [Direct and iterative solvers](../../../notes/numerical/cfd/direct_and_iterative_solvers.md)
- [Numerical stability](../../../notes/numerical/cfd/numerical_stability.md)
