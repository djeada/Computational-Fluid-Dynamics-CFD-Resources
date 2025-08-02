# Governing Equations of Fluid Mechanics

The behavior of fluid flows is described by a set of fundamental governing equations derived from the basic principles of physics. These equations represent the mathematical foundation of fluid mechanics and form the basis for all theoretical analysis and computational fluid dynamics.

## Overview

The governing equations in fluid mechanics are derived from three fundamental conservation principles:

1. **Conservation of Mass** → Continuity Equation
2. **Conservation of Momentum** → Navier-Stokes Equations  
3. **Conservation of Energy** → Energy Equation

These equations, combined with appropriate constitutive relations (such as the equation of state), form a complete mathematical description of fluid behavior.

## Mathematical Framework

### General Conservation Form

All conservation equations can be written in the general form:

$$\frac{\partial (\rho \phi)}{\partial t} + \nabla \cdot (\rho \phi \vec{v}) = \nabla \cdot (\Gamma \nabla \phi) + S_\phi$$

where:
- $\phi$ = conserved quantity per unit mass
- $\rho$ = density
- $\vec{v}$ = velocity vector
- $\Gamma$ = diffusion coefficient
- $S_\phi$ = source term

The terms represent:
- **Accumulation**: $\frac{\partial (\rho \phi)}{\partial t}$
- **Convection**: $\nabla \cdot (\rho \phi \vec{v})$
- **Diffusion**: $\nabla \cdot (\Gamma \nabla \phi)$
- **Source/Sink**: $S_\phi$

## Individual Equations

### 1. [Continuity Equation](./continuity.md)
Conservation of mass for compressible and incompressible flows.

### 2. [Navier-Stokes Equations](./navier_stokes.md)
Conservation of momentum including pressure, viscous, and body forces.

### 3. [Energy Equation](./energy.md)
Conservation of energy including thermal effects and viscous dissipation.

### 4. [Equation of State](./equation_of_state.md)
Thermodynamic relationships between pressure, density, and temperature.

### 5. [Conservation Form](./conservation_form.md)
General mathematical framework for conservation laws.

## Equation Coupling

The governing equations are **strongly coupled**, meaning they must be solved simultaneously:

- **Velocity** appears in continuity, momentum, and energy equations
- **Pressure** appears in momentum equation and equation of state
- **Density** appears in all equations for compressible flow
- **Temperature** affects density through equation of state

## Simplifications and Special Cases

### Incompressible Flow
- $\rho = $ constant
- Continuity becomes: $\nabla \cdot \vec{v} = 0$
- Momentum equation decouples from energy equation

### Inviscid Flow (Euler Equations)
- $\mu = 0$ (no viscosity)
- Simpler momentum equation
- No viscous dissipation in energy equation

### Stokes Flow
- Very low Reynolds number
- Inertial terms negligible
- Linear momentum equation

### Potential Flow
- Inviscid + irrotational flow
- $\vec{v} = \nabla \phi$
- Laplace equation for velocity potential

## Boundary Conditions

The governing equations require appropriate boundary conditions:

### Solid Boundaries
- **No-slip**: $\vec{v} = \vec{v}_{wall}$
- **No-penetration**: $\vec{v} \cdot \vec{n} = 0$
- **Temperature**: Specified $T$ or heat flux

### Inflow/Outflow Boundaries
- **Inlet**: Specified velocity, pressure, or mass flow
- **Outlet**: Specified pressure or zero gradient conditions

### Symmetry Boundaries
- **Normal velocity**: $\vec{v} \cdot \vec{n} = 0$
- **Tangential stress**: $\frac{\partial v_t}{\partial n} = 0$

## Initial Conditions

For unsteady problems, initial conditions must specify:
- Velocity field: $\vec{v}(x,y,z,t=0)$
- Pressure field: $p(x,y,z,t=0)$
- Temperature field: $T(x,y,z,t=0)$ (if energy equation is solved)

## Mathematical Properties

### Classification
The governing equations are:
- **Nonlinear** (due to convective terms)
- **Coupled** (variables appear in multiple equations)
- **Second-order** (highest derivative is second-order)

### Well-Posedness
For a problem to be well-posed, it must have:
1. **Existence**: A solution exists
2. **Uniqueness**: The solution is unique
3. **Stability**: Small changes in data produce small changes in solution

## Analytical Solutions

Exact analytical solutions exist for simplified cases:
- **Couette flow**: Flow between parallel plates
- **Poiseuille flow**: Pipe and channel flow
- **Stagnation point flow**: Flow near stagnation points
- **Blasius solution**: Boundary layer on flat plate

## Numerical Solution Methods

The governing equations are typically solved numerically using:
- **Finite Difference Method (FDM)**
- **Finite Volume Method (FVM)**
- **Finite Element Method (FEM)**
- **Spectral Methods**

## Dimensionless Form

The equations are often non-dimensionalized to:
- Identify important dimensionless parameters
- Reduce number of independent variables
- Enable similarity solutions
- Guide experimental scaling

Key dimensionless numbers include:
- **Reynolds number**: $Re = \frac{\rho V L}{\mu}$
- **Mach number**: $Ma = \frac{V}{a}$
- **Prandtl number**: $Pr = \frac{\mu c_p}{k}$
- **Grashof number**: $Gr = \frac{g \beta \Delta T L^3}{\nu^2}$

## Applications

Understanding the governing equations enables:
- **Flow prediction**: Velocity and pressure fields
- **Force calculation**: Drag and lift on bodies
- **Heat transfer analysis**: Temperature distributions
- **Optimization**: Design improvements
- **Control**: Active flow control strategies

## Historical Development

- **1755**: Euler equations (inviscid flow)
- **1822**: Navier-Stokes equations (viscous flow)
- **1845**: Stokes approximation (creeping flow)
- **1904**: Prandtl boundary layer equations
- **1950s**: Modern computational methods

The governing equations provide the mathematical foundation for all of fluid mechanics and continue to drive advances in both theoretical understanding and practical applications.
