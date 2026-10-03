# Eulerian and Lagrangian Flow Descriptions

This script contrasts the Eulerian and Lagrangian descriptions of fluid motion using the time-dependent Double Gyre flow. The Eulerian panel is a quiver plot of the velocity field at $t = 0$, sampled at fixed points of a grid. The Lagrangian panel follows 20 particles advected forward in time with a fourth-order Runge–Kutta scheme and draws their paths through the oscillating gyres.

## Overview

- Evaluates the analytical Double Gyre velocity field, whose amplitude `A`, perturbation `epsilon`, and frequency `omega` are function arguments
- Draws the Eulerian velocity field at $t = 0$ as a quiver plot on a 20 × 15 grid
- Releases 20 particles at seeded random positions in $[0, 2] \times [0, 1]$ and integrates their paths with RK4 ($\Delta t = 0.01$, 500 steps by default, so $0 \le t \le 5$)
- Draws each particle path in its own line colour and marks the starting points with black dots
- Places both panels side by side on equal-aspect axes

## Mathematical Background

### Double Gyre Velocity Field

The flow is derived from the stream function $\psi = A \sin(\pi f(x,t)) \sin(\pi y)$ with

$$
f(x, t) = \varepsilon \sin(\omega t)\, x^2 + \bigl(1 - 2\varepsilon \sin(\omega t)\bigr)
x
$$

which gives the velocity components $u = -\partial\psi/\partial y$ and $v = \partial\psi/\partial x$:

$$
u = -\pi A \sin(\pi f)\cos(\pi y)
$$

$$
v = \pi A \cos(\pi f)\sin(\pi y)\, \frac{\partial f}{\partial x}
$$

The script uses $A = 0.25$, $\varepsilon = 0.25$, and $\omega = 2\pi$. At $t = 0$ the field is the steady pair of counter-rotating gyres. For $t > 0$ the dividing line between the gyres oscillates about $x = 1$. The normal velocity is zero on all four domain boundaries, so particles stay inside the domain.

### Eulerian Description

The Eulerian field $\mathbf{u}(\mathbf{x}, t)$ gives the velocity at every fixed location $\mathbf{x}$ at time $t$.

### Lagrangian Description

A particle path $\mathbf{X}(t; \mathbf{x}_0)$ satisfies

$$
\frac{d\mathbf{X}}{dt} = \mathbf{u}\!\left(\mathbf{X}(t), t\right),
\qquad \mathbf{X}(0) = \mathbf{x}_0
$$

### RK4 Integration

$$
\mathbf{k}_1 = \mathbf{u}(\mathbf{x}^n, t^n), \quad
\mathbf{k}_2 = \mathbf{u}\!\left(\mathbf{x}^n + \tfrac{\Delta t}{2}\mathbf{k}_1, t^n +
\tfrac{\Delta t}{2}\right), \quad
\mathbf{k}_3 = \mathbf{u}\!\left(\mathbf{x}^n + \tfrac{\Delta t}{2}\mathbf{k}_2, t^n +
\tfrac{\Delta t}{2}\right), \quad
\mathbf{k}_4 = \mathbf{u}(\mathbf{x}^n + \Delta t\,\mathbf{k}_3, t^n + \Delta t)
$$

$$
\mathbf{x}^{n+1} = \mathbf{x}^n +
\frac{\Delta t}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)
$$

## Implementation

- `double_gyre_velocity(x, y, t, A, epsilon, omega)` returns `(u, v)` at arbitrary points.
- `rk4_step(x, y, t, dt, velocity_func)` advances all particles by one step at once.
- `compute_eulerian_field(nx, ny, t)` samples the field on a grid over $[0, 2] \times [0, 1]$.
- `compute_lagrangian_trajectories(num_particles, num_steps, dt, seed)` returns an array of shape `(num_particles, num_steps + 1, 2)`.
- `make_figure(num_steps, dt)` draws both panels, and `main(argv=None)` handles the flags (`DT = 0.01`, `NUM_STEPS = 500`, `NUM_PARTICLES = 20`, `SEED = 42`).

## Usage

```bash
python main.py                                     # open the figure window (500 steps)
python main.py --steps 1000                        # integrate to t = 10
python main.py --no-show --output out --steps 10   # quick headless run; saves eulerian_lagrangian_flows.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |
| `--steps N` | Number of RK4 time steps (default 500) |

## Output

The left panel shows the two counter-rotating gyres at $t = 0$: clockwise on the left, anticlockwise on the right. The right panel shows the 20 particle paths after 500 steps. Most particles circulate around one gyre centre, while those near the moving dividing line are carried from one gyre into the other.

![Eulerian and Lagrangian views of the Double Gyre](https://github.com/user-attachments/assets/5c8dbbd4-a00a-4f14-8d0e-058d84de7fe1)

## Related Notes

- [Understanding Eulerian and Lagrangian Flows](../../../notes/fluid_mechanics/flow_kinematics/eulerian_lagrangian_flows.md)
- [Flow Kinematics](../../../notes/fluid_mechanics/flow_kinematics/flow_kinematics.md)
