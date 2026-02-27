# Backward-Facing Step Flow (SIMPLE Algorithm)

This script simulates 2D incompressible viscous flow over a backward-facing step using the SIMPLE (Semi-Implicit Method for Pressure-Linked Equations) algorithm. It is a classic benchmark problem in computational fluid dynamics for validating flow solvers in the presence of separated flow and reattachment.

## Problem Description

A fluid with a parabolic inlet velocity profile enters a channel and encounters a sudden expansion (the backward-facing step). The flow separates at the step corner and reattaches downstream, forming a recirculation zone whose length depends on the Reynolds number:

$$Re = \frac{\rho U_{avg} H}{\mu}$$

where $H$ is the channel height upstream of the step, $U_{avg}$ is the mean inlet velocity, $\rho$ is the fluid density, and $\mu$ is the dynamic viscosity.

## Governing Equations

The 2D steady incompressible Navier-Stokes equations in conservative form:

**Continuity**:
$$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$$

**Momentum** ($x$-component):
$$\rho \left( u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} \right) = -\frac{\partial p}{\partial x} + \mu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

**Momentum** ($y$-component):
$$\rho \left( u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} \right) = -\frac{\partial p}{\partial y} + \mu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right)$$

## Numerical Method

The solver uses a staggered grid (MAC arrangement) and the SIMPLE pressure-velocity coupling algorithm:

1. **Predictor step**: Solve the discretized momentum equations (using hybrid upwind/central differencing) to obtain intermediate velocities $u^*$ and $v^*$.
2. **Pressure correction**: Solve a Poisson equation for the pressure correction $p'$ that enforces continuity.
3. **Corrector step**: Update velocities and pressure using $p'$ to satisfy the divergence-free constraint.
4. **Repeat** until momentum residuals and the global mass imbalance fall below convergence thresholds.

The linear systems are solved iteratively using a Gauss-Seidel SOR (Successive Over-Relaxation) sweep.

## Boundary Conditions

- **Inlet** (left): Parabolic velocity profile $u_{in}(y)$ on the open portion above the step; no-penetration ($v = 0$).
- **Outlet** (right): Zero-gradient for velocity ($\partial u / \partial x = 0$); pressure correction set to zero ($p' = 0$).
- **Walls** (top and bottom): No-slip ($u = v = 0$).
- **Step face**: No-slip enforced via the solid mask.

## Output

The script renders a live interactive plot containing:
- **Velocity magnitude field** with quiver arrows showing the flow direction.
- **Residual history** (u, v, and pressure residuals on a log scale).
- **Global mass imbalance** history (percentage of inlet flux).

## Running the Script

```bash
python main.py                  # Default: 240×80 grid, 3000 iterations
python main.py --demo           # Quick demo: 120×40 grid, 400 iterations
python main.py --nx 160 --ny 60 --max-iters 2000
```
