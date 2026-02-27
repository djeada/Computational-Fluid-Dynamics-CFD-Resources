# Eulerian and Lagrangian Flow Descriptions

This script contrasts the two fundamental descriptions of fluid motion using the time-dependent Double Gyre flow as a canonical example. The Eulerian panel shows the instantaneous velocity field at $t = 0$ as a quiver plot, giving a snapshot of how fluid moves at every fixed point in the domain. The Lagrangian panel tracks 20 particle trajectories integrated forward in time with a fourth-order Runge–Kutta scheme, revealing the complex stirring and transport structures that emerge from this oscillating gyre system.

## Overview

- Uses the analytically defined Double Gyre velocity field with tuneable amplitude, frequency, and perturbation parameters
- Renders the Eulerian velocity field as a quiver plot at $t = 0$
- Integrates 20 particle trajectories using the RK4 time-stepping scheme
- Displays Lagrangian paths to highlight chaotic advection and transport barriers
- Side-by-side panels allow direct comparison of the two kinematic viewpoints

## Mathematical Background

### Double Gyre Velocity Field

The stream-function perturbation factor is:

$$f(x, t) = \varepsilon \sin(\omega t)\, x^2 + \bigl(1 - 2\varepsilon \sin(\omega t)\bigr) x$$

The velocity components are:

$$u = -\pi A \sin(\pi f)\cos(\pi y)$$
$$v = \pi A \cos(\pi f)\sin(\pi y)\,\frac{\partial f}{\partial x}$$

### Eulerian Description

The Eulerian field $\mathbf{u}(\mathbf{x}, t)$ assigns a velocity vector to every fixed spatial location $\mathbf{x}$ at a given instant $t$.

### Lagrangian Description

The Lagrangian trajectory $\mathbf{X}(t; \mathbf{x}_0)$ satisfies the ODE:

$$\frac{d\mathbf{X}}{dt} = \mathbf{u}\!\left(\mathbf{X}(t), t\right), \qquad \mathbf{X}(0) = \mathbf{x}_0$$

### RK4 Integration

Each trajectory step uses the classical fourth-order Runge–Kutta scheme:

$$\mathbf{x}^{n+1} = \mathbf{x}^n + \frac{\Delta t}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

where $k_1, k_2, k_3, k_4$ are the standard RK4 stage velocities evaluated at intermediate positions and times.

## Implementation

1. Define the Double Gyre parameters: amplitude $A$, frequency $\omega$, and perturbation $\varepsilon$.
2. Evaluate $\mathbf{u}(\mathbf{x}, 0)$ on a regular grid and plot as a quiver diagram (Eulerian panel).
3. Select 20 initial particle positions $\mathbf{x}_0$ distributed across the domain.
4. Advance each particle in time using RK4 with a fixed time step $\Delta t$.
5. Store and plot each particle's path as a curve (Lagrangian panel).
6. Label both panels and add colour coding to distinguish individual trajectories.

## Output

The script produces a two-panel figure. The left panel shows the Eulerian quiver plot of the Double Gyre velocity field at $t = 0$, with arrows indicating the two counter-rotating gyres. The right panel shows 20 Lagrangian particle paths that wind around the gyre centres, revealing the chaotic advection structure of the flow.

![eulerian_lagrangian_flows](https://github.com/user-attachments/assets/5c8dbbd4-a00a-4f14-8d0e-058d84de7fe1)
