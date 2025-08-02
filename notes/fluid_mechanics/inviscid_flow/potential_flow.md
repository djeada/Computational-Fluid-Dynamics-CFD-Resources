# Potential Flow Theory

## Fundamental Concepts

### Definition of Potential Flow

Potential flow is **irrotational flow** where the vorticity is zero everywhere:
$$\vec{\omega} = \nabla \times \vec{V} = 0$$

This allows us to define a **scalar velocity potential** $\phi$ such that:
$$\vec{V} = \nabla \phi$$

### Conditions for Irrotational Flow

For a flow to be irrotational initially:
1. **Inviscid fluid** (no viscous torques)
2. **Conservative body forces** (e.g., gravity)
3. **Initially irrotational** conditions
4. **Kelvin's circulation theorem** ensures it remains irrotational

### Mathematical Framework

#### Laplace Equation

For incompressible potential flow, substituting $\vec{V} = \nabla \phi$ into continuity:
$$\nabla \cdot \vec{V} = \nabla \cdot (\nabla \phi) = \nabla^2 \phi = 0$$

This is **Laplace's equation** - a linear, elliptic PDE.

#### Linearity and Superposition

Since Laplace's equation is linear:
- If $\phi_1$ and $\phi_2$ are solutions, then $c_1\phi_1 + c_2\phi_2$ is also a solution
- This enables building complex flows from elementary solutions

## Stream Function

### Definition

For 2D incompressible flow, we can define a **stream function** $\psi$ such that:
$$u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}$$

This automatically satisfies continuity.

### Relationship to Velocity Potential

For irrotational flow:
$$\frac{\partial \phi}{\partial x} = \frac{\partial \psi}{\partial y}, \quad \frac{\partial \phi}{\partial y} = -\frac{\partial \psi}{\partial x}$$

These are the **Cauchy-Riemann equations**, indicating that $\phi$ and $\psi$ are harmonic conjugates.

### Properties of Streamlines

- **Streamlines**: Lines of constant $\psi$
- **Equipotential lines**: Lines of constant $\phi$
- Streamlines and equipotential lines are **orthogonal**
- Flow velocity is tangent to streamlines

## Elementary Solutions

### 1. Uniform Flow

**Velocity potential**:
$$\phi = U_\infty x \cos \alpha + U_\infty y \sin \alpha$$

**Stream function**:
$$\psi = U_\infty y \cos \alpha - U_\infty x \sin \alpha$$

**Velocity components**:
$$u = U_\infty \cos \alpha, \quad v = U_\infty \sin \alpha$$

For flow parallel to x-axis ($\alpha = 0$):
$$\phi = U_\infty x, \quad \psi = U_\infty y$$

### 2. Source/Sink

**Velocity potential**:
$$\phi = \frac{m}{2\pi} \ln r$$

**Stream function**:
$$\psi = \frac{m}{2\pi} \theta$$

**Velocity components**:
$$u_r = \frac{m}{2\pi r}, \quad u_\theta = 0$$

where:
- $m > 0$: **source** (outward flow)
- $m < 0$: **sink** (inward flow)
- $m$ has units of $[L^2/T]$ (volume flow rate per unit depth)

### 3. Doublet

A doublet is the limit of a source-sink pair as their separation approaches zero while their strength approaches infinity.

**Velocity potential**:
$$\phi = -\frac{\mu}{2\pi} \frac{\cos \theta}{r}$$

**Stream function**:
$$\psi = -\frac{\mu}{2\pi} \frac{\sin \theta}{r}$$

**Velocity components**:
$$u_r = \frac{\mu}{2\pi r^2} \cos \theta, \quad u_\theta = \frac{\mu}{2\pi r^2} \sin \theta$$

where $\mu$ is the **doublet strength**.

### 4. Point Vortex

**Velocity potential**:
$$\phi = -\frac{\Gamma}{2\pi} \theta$$

**Stream function**:
$$\psi = \frac{\Gamma}{2\pi} \ln r$$

**Velocity components**:
$$u_r = 0, \quad u_\theta = \frac{\Gamma}{2\pi r}$$

where $\Gamma$ is the **circulation** (positive for counterclockwise rotation).

**Note**: The vortex itself is a singular point where irrotationality breaks down, but the flow is irrotational everywhere else.

## Complex Analysis in 2D Flows

### Complex Potential

For 2D flows, define the **complex potential**:
$$F(z) = \phi + i\psi$$

where $z = x + iy$ is the complex coordinate.

### Complex Velocity

The complex velocity is:
$$w = \frac{dF}{dz} = u - iv$$

This follows from the Cauchy-Riemann equations.

### Elementary Solutions in Complex Form

**Uniform flow**:
$$F(z) = U_\infty z$$

**Source/sink**:
$$F(z) = \frac{m}{2\pi} \ln z$$

**Doublet**:
$$F(z) = -\frac{\mu}{2\pi z}$$

**Vortex**:
$$F(z) = -i\frac{\Gamma}{2\pi} \ln z$$

## Flow Past Simple Bodies

### Flow Past a Circular Cylinder

Combining uniform flow and doublet:
$$F(z) = U_\infty z + \frac{U_\infty a^2}{z}$$

This represents flow past a cylinder of radius $a$.

**Velocity on surface** ($r = a$):
$$u_\theta = -2U_\infty \sin \theta$$

**Stagnation points**: $\theta = 0, \pi$ where $u_\theta = 0$

**Pressure distribution** (from Bernoulli):
$$C_p = \frac{p - p_\infty}{\frac{1}{2}\rho U_\infty^2} = 1 - 4\sin^2 \theta$$

### Flow Past Cylinder with Circulation

Adding circulation to the cylinder flow:
$$F(z) = U_\infty z + \frac{U_\infty a^2}{z} - i\frac{\Gamma}{2\pi} \ln z$$

**Effects of circulation**:
- Moves stagnation points
- Creates asymmetric pressure distribution
- Generates lift (Kutta-Joukowsky theorem)

**Stagnation points** located at:
$$\sin \theta_s = -\frac{\Gamma}{4\pi U_\infty a}$$

For $|\Gamma| > 4\pi U_\infty a$, stagnation points move off the cylinder.

## Conformal Mapping

### Joukowsky Transformation

The Joukowsky transformation:
$$z = \zeta + \frac{c^2}{4\zeta}$$

maps a circle in the $\zeta$-plane to an airfoil-like shape in the $z$-plane.

**Process**:
1. Solve for flow past circle in $\zeta$-plane
2. Apply circulation for lift
3. Transform to $z$-plane using Joukowsky mapping
4. Obtain flow past airfoil

### Kutta Condition

For physically realistic airfoil flows:
- Flow must leave the **trailing edge smoothly**
- No infinite velocities at trailing edge
- Determines the circulation automatically

## Forces and Moments

### Kutta-Joukowsky Theorem

For a cylinder with circulation in crossflow:
$$\vec{L} = \rho \vec{V}_\infty \times \vec{\Gamma}$$

In 2D:
$$L = \rho U_\infty \Gamma$$

**Physical interpretation**: Circulation around a body in crossflow generates lift.

### Blasius Theorem

The complex force per unit depth is:
$$F_x - iF_y = \frac{i\rho}{2} \oint w^2 dz$$

where the integral is around the body surface.

### D'Alembert's Paradox

For a body without circulation in potential flow:
- **Drag = 0** (impossible in reality)
- **Lift = 0** (unless circulation is present)

This paradox shows the limitation of inviscid theory for predicting drag.

## Method of Images

### Flow Past Plane Boundary

To satisfy no-penetration condition at a plane boundary:
1. Place image sources/sinks across boundary
2. Image strength equals original but opposite sign
3. Boundary becomes a streamline

### Applications

**Ground effect**: Aircraft near ground
**Free surface flows**: Ship waves
**Channel flows**: Flow between parallel walls

## Green's Functions and Integral Equations

### Fundamental Solution

The Green's function for 2D Laplace equation:
$$G(x,y;x',y') = \frac{1}{2\pi} \ln r$$

where $r = \sqrt{(x-x')^2 + (y-y')^2}$.

### Panel Methods

Discretize body surface into panels with:
- **Source distributions**: $\sigma(s)$
- **Vortex distributions**: $\gamma(s)$
- **Doublet distributions**: $\mu(s)$

Solve integral equation:
$$\phi(x,y) = \int \sigma(s') G(x,y;s') ds' + \int \gamma(s') \frac{\partial G}{\partial n'} ds'$$

## Limitations of Potential Flow

### Physical Limitations

1. **No viscosity**: Cannot predict boundary layers
2. **No separation**: Cannot model flow separation
3. **No drag**: D'Alembert's paradox
4. **No heat transfer**: No thermal effects
5. **No compressibility**: Limited to low Mach numbers

### Boundary Conditions

- Can only satisfy **no-penetration**: $\vec{V} \cdot \hat{n} = 0$
- Cannot satisfy **no-slip**: $\vec{V} = 0$ at walls
- Flow can slip along boundaries

## Applications in Engineering

### Aerodynamics

**Initial design phases**:
- Airfoil shape optimization
- Lift curve slope estimation
- Pressure distribution prediction

**Panel methods**:
- Computational implementation of potential theory
- Fast calculation for preliminary design
- Coupling with boundary layer methods

### Hydrodynamics

**Ship design**:
- Wave resistance calculations
- Hull form optimization
- Seakeeping analysis

**Marine propulsors**:
- Propeller design
- Lifting line theory
- Cavitation prediction

### Turbomachinery

**Blade design**:
- Cascade flow analysis
- Loss coefficient estimation
- Performance prediction

### Environmental Flows

**Groundwater flow**:
- Well hydraulics
- Aquifer modeling
- Contamination transport

**Atmospheric flows**:
- Building aerodynamics
- Wind energy assessment
- Pollutant dispersion

## Computational Methods

### Analytical Solutions

- Complex function theory
- Conformal mapping
- Series solutions
- Integral transforms

### Numerical Methods

**Panel methods**:
- Boundary element discretization
- Linear system solution
- Post-processing for forces

**Finite difference/element**:
- Domain discretization
- Iterative solvers
- Grid generation challenges

### Modern Software

- **XFOIL**: Airfoil analysis with coupled boundary layer
- **VSAERO**: Panel method for aircraft
- **WAMIT**: Marine hydrodynamics
- **ANSYS Fluent**: General CFD with potential flow options

## Historical Development

- **1752**: d'Alembert derived d'Alembert's paradox
- **1904**: Kutta developed the Kutta condition
- **1906**: Joukowsky derived the lift theorem
- **1910**: Kármán and Trefftz extended airfoil theory
- **1920s**: Prandtl developed lifting line theory

## Learning Strategy

### Prerequisites
- Vector calculus and partial differential equations
- Complex analysis for 2D problems
- Basic understanding of fluid mechanics

### Key Concepts
1. Irrotational flow and velocity potential
2. Elementary solutions and superposition
3. Complex potential and conformal mapping
4. Boundary conditions and image methods
5. Kutta-Joukowsky theorem and circulation
6. Limitations and connection to viscous flow

### Problem-Solving Approach
1. Identify the geometry and boundary conditions
2. Select appropriate elementary solutions
3. Apply superposition principle
4. Satisfy boundary conditions
5. Calculate velocities and pressures
6. Determine forces using appropriate theorems

Potential flow theory provides powerful analytical tools for understanding inviscid fluid motion and serves as the foundation for many engineering applications in aerodynamics, hydrodynamics, and beyond.
