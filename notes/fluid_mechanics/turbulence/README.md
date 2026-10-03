# Turbulence Theory

Turbulence is one of the most challenging and important phenomena in fluid mechanics. It is characterized by chaotic, irregular flow patterns with rapid mixing, enhanced transport properties, and complex three-dimensional vortical structures. Understanding turbulence is crucial for many engineering applications and remains an active area of research.

## Overview

Turbulent flow is characterized by:

- **Irregularity**: Chaotic, unpredictable behavior
- **Nonlinearity**: Small changes can have large effects
- **Three-dimensionality**: Complex 3D vortical structures
- **Mixing**: Rapid transport of momentum, heat, and mass
- **Dissipation**: Kinetic energy cascade to heat
- **Wide range of scales**: From large eddies to molecular dissipation

## Table of Contents

### 1. [Reynolds Decomposition](./reynolds_decomposition.md)

Mean and fluctuating parts, averaging operators and their rules, the Reynolds stress tensor, turbulence intensity and TKE, and Favre averaging.

### 2. [Turbulence Statistics](./statistics.md)

PDFs and moments, two-point and two-time correlations, integral scales, Taylor's frozen-turbulence hypothesis, and energy spectra.

### 3. [Energy Cascade Theory](./energy_cascade.md)

Richardson's cascade, Kolmogorov's 1941 hypotheses and microscales, the $-5/3$ spectrum, and what the range of scales means for DNS cost.

### 4. [RANS Equations](./rans_equations.md)

Derivation of the Reynolds-averaged equations, the closure problem, Reynolds-stress and TKE transport, the Boussinesq hypothesis, and the law of the wall.

### 5. [Turbulence Modeling](./modeling.md)

The DNS/LES/DES/RANS hierarchy, the mixing-length, Spalart–Allmaras, $k$–$\varepsilon$, $k$–$\omega$ and SST models with their constants, LES and the Smagorinsky model, and how to choose a model.

For how turbulence models are used inside a CFD workflow, see [Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md).

## Characteristics of Turbulence

### Physical Properties

1. **Irregularity and Randomness**

   - Velocity and pressure fluctuate randomly in time and space
   - Statistical approach required for analysis

2. **Nonlinearity**

   - Small disturbances can grow exponentially
   - Sensitive dependence on initial conditions

3. **Three-Dimensionality**

   - Turbulent flows are inherently three-dimensional
   - Vortex stretching in 3D is key mechanism

4. **Enhanced Mixing**

   - Rapid transport of momentum, heat, and mass
   - Mixing rates much higher than molecular diffusion

5. **Energy Dissipation**

   - Turbulent kinetic energy cascades to small scales
   - Eventually dissipated as heat due to viscosity

6. **Wide Range of Scales**

   - Large energy-containing eddies down to Kolmogorov microscales
   - Scale separation increases with Reynolds number

### Mathematical Properties

1. **Vorticity Dynamics**

   - Vortex stretching and tilting
   - Vorticity equation: $\frac{D\omega}{Dt} = (\omega \cdot \nabla)\vec{v} + \nu \nabla^2 \omega$

2. **Nonlinear Convection**

   - $(\vec{v} \cdot \nabla)\vec{v}$ term in Navier-Stokes equations
   - Responsible for energy transfer between scales

3. **Pressure-Strain Correlation**

   - Pressure fluctuations redistribute Reynolds stresses
   - No net energy production but affects anisotropy

## Reynolds Number and Transition

### Critical Reynolds Numbers

Turbulence onset depends on geometry and flow conditions:

- **Pipe flow**: $Re_c \approx 2300$
- **Flat plate boundary layer**: $Re_c \approx 5 \times 10^5$
- **Mixing layer**: $Re_c \approx 30-50$
- **Taylor-Couette flow**: $Re_c \approx 1700$

### Transition Process

1. **Linear instability**: Small disturbances grow exponentially
2. **Nonlinear saturation**: Finite amplitude waves develop
3. **Secondary instability**: Three-dimensional breakdown
4. **Fully developed turbulence**: Chaotic behavior

## Scales of Turbulence

Turbulence spans a range from energy-containing eddies of the size of the flow, through an inertial subrange, down to the dissipative Kolmogorov microscales $\eta = (\nu^3/\varepsilon)^{1/4}$. The ratio of largest to smallest scales grows as $Re^{3/4}$. Kolmogorov's hypotheses, the $-5/3$ spectrum, and a worked example of the scales in a pipe flow are covered in [Energy Cascade Theory](./energy_cascade.md).

## Turbulent Transport

### Enhanced Mixing

Turbulence greatly enhances transport of:

- **Momentum**: Turbulent viscosity $\nu_t \gg \nu$
- **Heat**: Turbulent thermal diffusivity $\alpha_t \gg \alpha$
- **Mass**: Turbulent mass diffusivity $D_t \gg D$

The eddy-viscosity concept and the models that compute $\nu_t$ (mixing length, one- and two-equation models) are covered in [RANS Equations](./rans_equations.md) and [Turbulence Modeling](./modeling.md).

### Turbulent Prandtl and Schmidt Numbers

- **Turbulent Prandtl number**: $Pr_t = \nu_t/\alpha_t \approx 0.9$
- **Turbulent Schmidt number**: $Sc_t = \nu_t/D_t \approx 0.9$

These are much closer to unity than their molecular counterparts.

## Energy Budget and Wall-Bounded Turbulence

The turbulent kinetic energy equation (production, dissipation and transport), the near-wall structure (viscous sublayer, buffer layer, log law), and wall units such as $y^+$ are derived in [RANS Equations](./rans_equations.md). Additional production mechanisms appear in some flows, notably buoyancy in stratified flows and Coriolis effects under system rotation.

### Turbulent Boundary Layers

Key parameters:

- **Displacement thickness**: $\delta^\ast = \int_0^\delta (1 - u/U) dy$
- **Momentum thickness**: $\theta = \int_0^\delta \frac{u}{U}(1 - u/U) dy$
- **Shape factor**: $H = \delta^\ast/\theta \approx 1.4$ (turbulent)

See also [Boundary Layers](../viscous_flow/boundary_layers.md).

## Free Shear Flows

### Turbulent Jets

- **Self-similar profiles**: Velocity and turbulence profiles collapse
- **Entrainment**: Surrounding fluid drawn into jet
- **Spreading rate**: Linear growth of jet width

### Mixing Layers

- **Kelvin-Helmholtz instability**: Primary instability mechanism
- **Large coherent structures**: Dominate mixing process
- **Transition to small-scale turbulence**: Breakdown of large vortices

### Wakes

- **Momentum deficit**: Reduced velocity behind obstacle
- **Vortex shedding**: Periodic vortex formation (low Re)
- **Recovery**: Gradual momentum recovery downstream

## Homogeneous and Isotropic Turbulence

Homogeneous turbulence has statistics that are invariant under translation. Isotropic turbulence is also invariant under rotation and reflection. Grid-generated turbulence in a wind tunnel is the standard laboratory approximation. Definitions, correlation functions and spectra are in [Turbulence Statistics](./statistics.md), and Kolmogorov's theory of the small scales is in [Energy Cascade Theory](./energy_cascade.md).

## Advanced Topics

DNS, LES and hybrid RANS–LES methods, and their cost scalings, are compared in [Turbulence Modeling](./modeling.md).

### Coherent Structures

- **Definition**: Organized patterns in turbulent flows
- **Examples**: Streaks in boundary layers, horseshoe vortices
- **Importance**: Dominate transport and mixing

### Compressible Turbulence

- **Additional complexity**: Density fluctuations
- **Pressure dilatation**: $p'\nabla \cdot \vec{v}'$ term
- **Shock-turbulence interaction**: Highly nonlinear

## Applications

### Engineering Applications

- **Aerospace**: Aircraft design, engine performance
- **Automotive**: Vehicle aerodynamics, engine flows
- **Energy**: Wind turbines, heat exchangers
- **Environmental**: Atmospheric and ocean flows
- **Industrial**: Mixing, combustion, heat transfer

### Research Areas

- **Climate modeling**: Atmospheric and oceanic turbulence
- **Astrophysics**: Stellar formation, galactic dynamics
- **Geophysics**: Atmospheric boundary layer, ocean currents
- **Plasma physics**: Magnetic confinement fusion

## Experimental Techniques

### Measurement Methods

- **Hot-wire anemometry**: High-frequency velocity measurements
- **Particle Image Velocimetry (PIV)**: Instantaneous flow fields
- **Laser Doppler Velocimetry (LDV)**: Point velocity measurements
- **Pressure transducers**: Pressure fluctuation measurements

### Wind Tunnel Studies

- **Boundary layer facilities**: Study wall-bounded turbulence
- **Grid turbulence**: Generate (nearly) isotropic turbulence
- **Mixing layers**: Study free shear flows

## Historical Development

- **1883**: Reynolds experiments on pipe flow transition
- **1895**: Reynolds decomposition and averaged equations
- **1904**: Prandtl's boundary layer theory
- **1922**: Richardson's description of the energy cascade
- **1925**: Prandtl's mixing length theory
- **1941**: Kolmogorov's similarity theory
- **1945**: von Kármán and Howarth equations
- **1970s**: Development of k-ε model
- **1980s**: Large Eddy Simulation
- **1990s**: Direct Numerical Simulation

## Current Research Frontiers

### Computational Methods

- **Machine learning**: Data-driven turbulence modeling
- **High-order methods**: Spectral and discontinuous Galerkin
- **Massively parallel computing**: Exascale simulations

### Physical Understanding

- **Extreme events**: Rare but important large deviations
- **Non-equilibrium turbulence**: Rapidly changing conditions
- **Multiphase turbulence**: Bubbles, drops, particles
- **Magnetohydrodynamic turbulence**: Plasma applications

Turbulence remains one of the most challenging problems in classical physics and continues to drive advances in both fundamental understanding and practical applications.
