# Backward-Facing Step Flow (SIMPLE Algorithm)

This script simulates 2D incompressible viscous flow over a backward-facing step using the SIMPLE (Semi-Implicit Method for Pressure-Linked Equations) algorithm. It is a classic benchmark problem in computational fluid dynamics for validating flow solvers in the presence of separated flow and reattachment.

## Overview

- Models steady 2D incompressible Navier-Stokes flow on a staggered MAC grid.
- Uses the SIMPLE pressure-velocity coupling algorithm with Gauss-Seidel SOR iterations.
- Applies a parabolic inlet velocity profile and enforces no-slip on walls and the step face.
- Monitors momentum residuals and global mass imbalance for convergence.
- Renders a live plot of the velocity magnitude field, residual history, and mass imbalance.

## Mathematical Background

### Governing Equations

The 2D steady incompressible Navier-Stokes equations:

**Continuity**:

$$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$$

**Momentum** ($x$-component):

$$\rho \left( u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} \right) = -\frac{\partial p}{\partial x} + \mu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)$$

**Momentum** ($y$-component):

$$\rho \left( u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} \right) = -\frac{\partial p}{\partial y} + \mu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right)$$

### Reynolds Number

The flow regime is characterised by the Reynolds number:

$$Re = \frac{\rho U_{avg} H}{\mu}$$

where $H$ is the upstream channel height and $U_{avg}$ is the mean inlet velocity.

## Implementation

1. **Geometry Masks**: Boolean arrays mark fluid and solid cells for the pressure, $u$, and $v$ grids on the staggered MAC arrangement.
2. **Predictor Step**: Discretized momentum equations (hybrid upwind/central differencing) are assembled and solved with Gauss-Seidel SOR to obtain intermediate velocities $u^*$ and $v^*$.
3. **Pressure Correction**: A Poisson equation for the pressure correction $p'$ is solved to enforce continuity, with $p' = 0$ enforced at the outlet.
4. **Corrector Step**: Velocities and pressure are updated using $p'$ to satisfy the divergence-free constraint.
5. **Convergence Check**: Iteration stops when momentum residuals drop three orders of magnitude and mass imbalance falls below 0.5%.
6. **Live Visualization**: Every `plot_interval` iterations, the velocity magnitude field, residuals, and mass imbalance are updated on an interactive Matplotlib figure.

## Output

The script renders a live interactive figure containing:
- **Velocity magnitude field** with quiver arrows showing the flow direction.
- **Residual history** ($u$, $v$, and pressure residuals on a log scale).
- **Global mass imbalance** history (percentage of inlet flux).

## Running the Script

```bash
python main.py                  # Default: 240×80 grid, 3000 iterations
python main.py --demo           # Quick demo: 120×40 grid, 400 iterations
python main.py --nx 160 --ny 60 --max-iters 2000
```
