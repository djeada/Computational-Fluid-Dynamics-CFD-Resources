# Flow Visualization Around a Cylinder: Steady and Unsteady Pathlines with Vortex Shedding

This project simulates fluid flow around a cylindrical obstacle using potential flow superposition and discrete shed vortices, then compares steady streamlines with unsteady particle pathlines integrated by the Runge-Kutta 4th-order method.

## Overview

- **Potential flow** around a cylinder: uniform stream superposed with circulation $\Gamma = 4\pi RU_\infty$.
- **Vortex shedding model**: discrete vortices added via Biot–Savart law to simulate an unsteady wake.
- **Strouhal number** $St = fD/U_\infty \approx 0.2$ characterizes shedding frequency at $Re \approx 100$–1000.
- **RK4 integration** computes accurate particle trajectories in the time-varying velocity field.
- **Matplotlib animation**: overlays pathline trails and instantaneous streamlines for direct comparison.

## Mathematical Background

### Potential Flow Around a Cylinder

The stream function for flow past a cylinder of radius $R$ with circulation $\Gamma$ in a uniform stream $U_\infty$:

$$\psi = U_\infty\!\left(r - \frac{R^2}{r}\right)\sin\theta + \frac{\Gamma}{2\pi}\ln\frac{r}{R}$$

Velocity components at any point $(X,Y)$, with $\theta = \arctan(Y/X)$:

$$U_r = U_\infty\!\left(1 - \frac{R^2}{X^2+Y^2}\right), \quad U_\theta = -U_\infty\frac{R^2}{X^2+Y^2} + \frac{\Gamma}{2\pi(X^2+Y^2)}$$

$$U_x = U_r\cos\theta - U_\theta\sin\theta, \quad U_y = U_r\sin\theta + U_\theta\cos\theta$$

### Vortex Shedding via Biot–Savart Law

Each shed vortex at $(x_v,y_v)$ with strength $\gamma$ contributes:

$$U_x = \frac{\gamma}{2\pi}\left(-\frac{Y-y_v}{(X-x_v)^2+(Y-y_v)^2}\right), \quad U_y = \frac{\gamma}{2\pi}\left(\frac{X-x_v}{(X-x_v)^2+(Y-y_v)^2}\right)$$

The shedding frequency satisfies $St = fD/U_\infty \approx 0.2$ for $Re \approx 100$–1000.

### RK4 Particle Integration

Particle positions are advanced with the classical Runge-Kutta 4th-order scheme:

$$k_1 = \mathbf{u}(\mathbf{x}_n),\quad k_2 = \mathbf{u}(\mathbf{x}_n+\tfrac{\Delta t}{2}k_1),\quad k_3 = \mathbf{u}(\mathbf{x}_n+\tfrac{\Delta t}{2}k_2),\quad k_4 = \mathbf{u}(\mathbf{x}_n+\Delta t\,k_3)$$

$$\mathbf{x}_{n+1} = \mathbf{x}_n + \frac{\Delta t}{6}(k_1+2k_2+2k_3+k_4)$$

## Implementation

1. Set parameters: cylinder radius $R$, free-stream velocity $U_\infty$, circulation $\Gamma = 4\pi RU_\infty$, time step $\Delta t$, steps `nt`, and particle count `num_particles`.
2. Seed fluid particles at initial positions upstream of the cylinder.
3. At each time step, compute the base potential-flow velocity field from the cylinder superposition formula.
4. Add vortex contributions from all currently shed vortices using the Biot–Savart formula.
5. Advance each particle position using RK4; remove particles that enter the cylinder interior.
6. Periodically shed a new vortex pair from the cylinder surface at the Strouhal frequency.
7. Animate pathline trails and instantaneous streamlines in Matplotlib.

## Output

The Matplotlib animation shows:

- **Steady case**: pathlines coincide with streamlines, tracing smooth arcs around the cylinder.
- **Unsteady case**: shed vortices distort the wake into a von Kármán vortex street; pathlines diverge from instantaneous streamlines, illustrating the key difference between the two concepts.

## Running the Script

Modify parameters at the top of the script to explore different flow regimes:

```python
R            = 1.0          # cylinder radius
U            = 1.0          # free-stream velocity
Gamma        = 4*pi*R*U     # circulation
dt           = 0.05         # time step
nt           = 200          # number of time steps
num_particles = 50          # number of tracer particles
```
