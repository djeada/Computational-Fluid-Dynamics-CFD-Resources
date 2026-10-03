# Fluid Mechanics - Theoretical Foundations

This section covers the theoretical foundations of fluid mechanics, providing the mathematical and physical framework for understanding fluid behavior. Unlike applied mechanics which focuses on practical engineering applications, this section emphasizes the fundamental equations, theoretical analysis, and mathematical methods that underpin all fluid flow phenomena.

## Overview

Fluid mechanics is the branch of physics that studies the motion and behavior of fluids (liquids and gases) and the forces acting on them. This theoretical treatment covers:

- **Fundamental governing equations** and their derivations
- **Physical principles** governing fluid behavior
- **Classical analytical results** for statics, inviscid, viscous, internal, compressible, and turbulent flow

**Note**: For practical engineering applications of fluid forces on structures, see [Applied Mechanics - Fluid Loading](../applied_mechanics/fluid_loading/) section.

## Table of Contents

### 1. Fundamentals

- [Introduction](intro.md): Basic concepts, continuum hypothesis, and fundamental principles
- [Dimensional Analysis](dimensions.md): Buckingham Pi theorem, dimensionless numbers, and similarity

### 2. [Governing Equations](./governing_equations/)

- [Continuity Equation](./governing_equations/continuity.md)
- [Navier-Stokes Equations](./governing_equations/navier_stokes.md)
- [Energy Equation](./governing_equations/energy.md)
- [Equation of State](./governing_equations/equation_of_state.md)

### 3. [Fluid Properties](./fluid_properties/)

- [Viscosity and Newtonian Fluids](./fluid_properties/viscosity.md)
- [Pressure, Density and Compressibility](./fluid_properties/pressure_and_compressibility.md)
- [Surface Tension and Capillary Effects](./fluid_properties/surface_tension.md)

### 4. [Flow Kinematics](./flow_kinematics/)

- [Flow Kinematics](./flow_kinematics/flow_kinematics.md)
- [Eulerian and Lagrangian Descriptions](./flow_kinematics/eulerian_lagrangian_flows.md)

### 5. [Fluid Statics](./fluid_statics/)

- [Hydrostatics](./fluid_statics/hydrostatics.md)

### 6. [Inviscid Flow](./inviscid_flow/)

- [Bernoulli's Equation](./inviscid_flow/bernoulli.md)
- [Potential Flow Theory](./inviscid_flow/potential_flow.md)

### 7. [Viscous Flow](./viscous_flow/)

- [Boundary Layer Theory](./viscous_flow/boundary_layers.md)
- [Drag](./viscous_flow/drag.md)

### 8. [Internal Flow](./internal_flow/)

- [Pipe Flow](./internal_flow/pipes.md)

### 9. [Compressible Flow](./compressible_flow/)

- [Thermodynamics of Compressible Flow](./compressible_flow/thermodynamics.md)
- [Speed of Sound and Mach Number](./compressible_flow/speed_of_sound.md)
- [Isentropic Flow](./compressible_flow/isentropic_flow.md)
- [Shock Waves](./compressible_flow/shock_waves.md)
- [Rayleigh and Fanno Flow](./compressible_flow/rayleigh_fanno.md)

### 10. [Turbulence](./turbulence/)

- [Reynolds Decomposition](./turbulence/reynolds_decomposition.md)
- [Turbulence Statistics](./turbulence/statistics.md)
- [Energy Cascade Theory](./turbulence/energy_cascade.md)
- [RANS Equations](./turbulence/rans_equations.md)
- [Turbulence Modeling](./turbulence/modeling.md)

### 11. [Specialized Topics](./specialized_topics/)

- [Fluid-Structure Interaction](./specialized_topics/fluid_structure_interaction.md)

Topics that are planned but not written yet (stability theory, heat and mass transfer, multiphase flow, exact viscous solutions, mathematical methods, and more) are listed in the [roadmap](../../ROADMAP.md).

## Learning Pathways

### Beginner Level

1. Start with the **Introduction** and **Fluid Properties**
2. Study **Hydrostatics** and basic **Flow Kinematics**
3. Learn **Dimensional Analysis** fundamentals
4. Explore **Bernoulli's Equation** and simple **Potential Flow** solutions

### Intermediate Level

1. Work through the **Governing Equations** and their derivations
2. Study **Boundary Layer Theory**, **Drag**, and **Pipe Flow**
3. Learn **Compressible Flow** fundamentals: speed of sound, isentropic flow, shocks
4. Learn the basics of **Turbulence**: Reynolds decomposition and statistics

### Advanced Level

1. Study the **Energy Cascade** and **RANS Equations**
2. Compare **Turbulence Models** and their assumptions
3. Explore **Fanno and Rayleigh Flow** and oblique shocks
4. Study **Fluid-Structure Interaction**

## Mathematical Prerequisites

- **Vector Calculus**: Gradients, divergence, curl, and integral theorems
- **Partial Differential Equations**: Classification and solution methods
- **Complex Analysis**: Functions, contour integration, and conformal mapping
- **Linear Algebra**: Matrix operations and eigenvalue problems
- **Statistics**: Probability theory for turbulence analysis

## Theoretical Foundations

### Conservation Laws

All fluid mechanics stems from fundamental conservation principles:

- **Mass Conservation**: Leads to continuity equation
- **Momentum Conservation**: Results in Navier-Stokes equations
- **Energy Conservation**: Produces energy equation

### Constitutive Relations

Connect stress to deformation rate:

- **Newtonian fluids**: Linear stress-strain rate relationship
- **Non-Newtonian fluids**: Nonlinear constitutive equations
- **Compressible fluids**: Equation of state relationships

### Boundary Conditions

Mathematical constraints that make problems well-posed:

- **No-slip condition**: Velocity matches wall velocity
- **No-penetration**: Normal velocity component zero at walls
- **Pressure conditions**: Specified pressure at boundaries
- **Periodic conditions**: For flows with spatial periodicity

## Analytical vs. Numerical Methods

### Analytical Solutions

Exact mathematical solutions for simplified cases:

- **Poiseuille flow**: Pipe and channel flows
- **Couette flow**: Flow between parallel plates
- **Stagnation point flow**: Flow near stagnation points
- **Blasius boundary layer**: Flat plate boundary layer

### Asymptotic Methods

Approximate solutions using small parameters:

- **Boundary layer theory**: High Reynolds number flows
- **Lubrication theory**: Thin film flows
- **Perturbation methods**: Weakly nonlinear problems

## Connection to CFD

This theoretical foundation directly supports computational fluid dynamics:

- **Governing equations** form the basis for numerical schemes (see [Numerical Methods](../numerical/))
- **Dimensional analysis** guides mesh resolution and scaling
- **Stability theory** informs numerical stability requirements
- **Turbulence models** require theoretical understanding

## Further Reading

### Classic Textbooks

- **Batchelor, G.K.**: "An Introduction to Fluid Dynamics"
- **Panton, R.L.**: "Incompressible Flow"
- **White, F.M.**: "Fluid Mechanics"
- **Kundu, P.K. & Cohen, I.M.**: "Fluid Mechanics"

### Advanced References

- **Pope, S.B.**: "Turbulent Flows"
- **Drazin, P.G. & Reid, W.H.**: "Hydrodynamic Stability"
- **Acheson, D.J.**: "Elementary Fluid Dynamics"
- **Tritton, D.J.**: "Physical Fluid Dynamics"
