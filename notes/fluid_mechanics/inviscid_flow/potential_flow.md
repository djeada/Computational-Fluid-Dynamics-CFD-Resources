# Potential Flow Theory

## Fundamental Concepts

### Definition of Potential Flow

Potential flow is **irrotational flow** where the vorticity is zero everywhere:

$$
\vec{\omega} = \nabla \times \vec{V} = 0
$$

This allows us to define a **scalar velocity potential** $\phi$ such that:

$$
\vec{V} = \nabla \phi
$$

### Conditions for Irrotational Flow

For a flow to be irrotational initially:

1. **Inviscid fluid** (no viscous torques)
2. **Conservative body forces** (e.g., gravity)
3. **Initially irrotational** conditions
4. **Kelvin's circulation theorem** ensures it remains irrotational

### Mathematical Framework

#### Laplace Equation

For incompressible potential flow, substituting $\vec{V} = \nabla \phi$ into continuity:

$$
\nabla \cdot \vec{V} = \nabla \cdot (\nabla \phi) = \nabla^2 \phi = 0
$$

This is **Laplace's equation** - a linear, elliptic PDE.

#### Linearity and Superposition

Since Laplace's equation is linear:

- If $\phi_1$ and $\phi_2$ are solutions, then $c_1\phi_1 + c_2\phi_2$ is also a solution
- This enables building complex flows from elementary solutions

## Stream Function

### Definition

For 2D incompressible flow, we can define a **stream function** $\psi$ such that:

$$
u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}
$$

This automatically satisfies continuity.

### Relationship to Velocity Potential

For irrotational flow:

$$
\frac{\partial \phi}{\partial x} = \frac{\partial \psi}{\partial y}, \quad
\frac{\partial \phi}{\partial y} = -\frac{\partial \psi}{\partial x}
$$

These are the **Cauchy-Riemann equations**, indicating that $\phi$ and $\psi$ are harmonic conjugates.

### Properties of Streamlines

- **Streamlines**: Lines of constant $\psi$
- **Equipotential lines**: Lines of constant $\phi$
- Streamlines and equipotential lines are **orthogonal**
- Flow velocity is tangent to streamlines

## Elementary Solutions

### 1. Uniform Flow

**Velocity potential**:

$$
\phi = U_\infty x \cos \alpha + U_\infty y \sin \alpha
$$

**Stream function**:

$$
\psi = U_\infty y \cos \alpha - U_\infty x \sin \alpha
$$

**Velocity components**:

$$
u = U_\infty \cos \alpha, \quad v = U_\infty \sin \alpha
$$

For flow parallel to x-axis ($\alpha = 0$):

$$
\phi = U_\infty x, \quad \psi = U_\infty y
$$

### 2. Source/Sink

**Velocity potential**:

$$
\phi = \frac{m}{2\pi} \ln r
$$

**Stream function**:

$$
\psi = \frac{m}{2\pi} \theta
$$

**Velocity components**:

$$
u_r = \frac{m}{2\pi r}, \quad u_\theta = 0
$$

where:

- $m > 0$: **source** (outward flow)
- $m < 0$: **sink** (inward flow)
- $m$ has units of $[L^2/T]$ (volume flow rate per unit depth)

### 3. Doublet

A doublet is the limit of a source-sink pair as their separation approaches zero while their strength approaches infinity.

**Velocity potential**:

$$
\phi = -\frac{\mu}{2\pi} \frac{\cos \theta}{r}
$$

**Stream function**:

$$
\psi = \frac{\mu}{2\pi} \frac{\sin \theta}{r}
$$

**Velocity components**:

$$
u_r = \frac{\mu}{2\pi r^2} \cos \theta, \quad u_\theta = \frac{\mu}{2\pi r^2} \sin
\theta
$$

where $\mu$ is the **doublet strength**.

### 4. Point Vortex

**Velocity potential**:

$$
\phi = \frac{\Gamma}{2\pi} \theta
$$

**Stream function**:

$$
\psi = -\frac{\Gamma}{2\pi} \ln r
$$

**Velocity components**:

$$
u_r = 0, \quad u_\theta = \frac{\Gamma}{2\pi r}
$$

where $\Gamma$ is the **circulation** (positive for counterclockwise rotation).

**Note**: The vortex itself is a singular point where irrotationality breaks down, but the flow is irrotational everywhere else.

## Complex Analysis in 2D Flows

### Complex Potential

For 2D flows, define the **complex potential**:

$$
F(z) = \phi + i\psi
$$

where $z = x + iy$ is the complex coordinate.

### Complex Velocity

The complex velocity is:

$$
w = \frac{dF}{dz} = u - iv
$$

This follows from the Cauchy-Riemann equations.

### Elementary Solutions in Complex Form

**Uniform flow**:

$$
F(z) = U_\infty z
$$

**Source/sink**:

$$
F(z) = \frac{m}{2\pi} \ln z
$$

**Doublet**:

$$
F(z) = -\frac{\mu}{2\pi z}
$$

**Vortex**:

$$
F(z) = -i \frac{\Gamma}{2\pi} \ln z
$$

## Flow Past Simple Bodies

### Flow Past a Circular Cylinder

Combining uniform flow and doublet:

$$
F(z) = U_\infty z + \frac{U_\infty a^2}{z}
$$

This represents flow past a cylinder of radius $a$.

**Velocity on surface** ($r = a$):

$$
u_\theta = -2U_\infty \sin \theta
$$

**Stagnation points**: $\theta = 0, \pi$ where $u_\theta = 0$

**Pressure distribution** (from Bernoulli):

$$
C_p = \frac{p - p_\infty}{\frac{1}{2}\rho U_\infty^2} = 1 - 4\sin^2 \theta
$$

### Flow Past Cylinder with Circulation

Adding circulation to the cylinder flow:

$$
F(z) = U_\infty z + \frac{U_\infty a^2}{z} - i \frac{\Gamma}{2\pi} \ln z
$$

**Effects of circulation**:

- Moves stagnation points
- Creates asymmetric pressure distribution
- Generates lift (Kutta-Joukowsky theorem)

**Stagnation points** located at:

$$
\sin \theta_s = \frac{\Gamma}{4\pi U_\infty a}
$$

For $|\Gamma| > 4\pi U_\infty a$, stagnation points move off the cylinder.

## Conformal Mapping

### Joukowsky Transformation

The Joukowsky transformation:

$$
z = \zeta + \frac{c^2}{4\zeta}
$$

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

$$
\vec{L} = \rho \vec{V}_\infty \times \vec{\Gamma}
$$

In 2D (magnitude per unit span):

$$
L = \rho U_\infty \Gamma
$$

**Physical interpretation**: Circulation around a body in crossflow generates lift.

### Blasius Theorem

The complex force per unit depth is:

$$
F_x - iF_y = \frac{i\rho}{2} \oint w^2 dz
$$

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

$$
G(x,y;x',y') = \frac{1}{2\pi} \ln r
$$

where $r = \sqrt{(x-x')^2 + (y-y')^2}$.

### Panel Methods

Discretize body surface into panels with:

- **Source distributions**: $\sigma(s)$
- **Vortex distributions**: $\gamma(s)$
- **Doublet distributions**: $\mu(s)$

Solve integral equation:

$$
\phi(x,y) = \int \sigma(s') G(x,y;s') ds' + \int \mu(s') \frac{\partial G}{\partial n'}
ds'
$$

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
- **1902**: Kutta developed the Kutta condition
- **1906**: Joukowsky derived the lift theorem
- **1918**: Kármán and Trefftz extended airfoil theory
- **1918–1919**: Prandtl developed lifting line theory

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

## Related Scripts

- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](../../../scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/): compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model.

## Exercises

**Exercise 1.** For the point vortex $\phi = \frac{\Gamma}{2\pi}\theta$, $\psi = -\frac{\Gamma}{2\pi}\ln r$: (a) check the polar Cauchy–Riemann relations $u_r = \partial\phi/\partial r = \frac{1}{r}\partial\psi/\partial\theta$ and $u_\theta = \frac{1}{r}\partial\phi/\partial\theta = -\partial\psi/\partial r$; (b) show that the circulation around any circle centred on the vortex is $\Gamma$, even though the vorticity is zero for $r > 0$.

<details>
<summary>Answer</summary>

(a) $u_r = \partial\phi/\partial r = 0$ and $\frac{1}{r}\partial\psi/\partial\theta = 0$. Also $u_\theta = \frac{1}{r}\cdot\frac{\Gamma}{2\pi} = \frac{\Gamma}{2\pi r}$ and $-\partial\psi/\partial r = \frac{\Gamma}{2\pi r}$. Both relations hold.

(b) $`\oint u_\theta\, r\, d\theta = \int_0^{2\pi}\frac{\Gamma}{2\pi r}\, r\, d\theta = \Gamma`$, independent of $r$.

The vorticity is $\omega = \frac{1}{r}\frac{d(r u_\theta)}{dr} = 0$ for $r > 0$. By Stokes' theorem, all the circulation must therefore come from a singular concentration of vorticity at $r = 0$.

</details>

**Exercise 2.** For potential flow of air ($\rho = 1.225$ kg/m³) at $U_\infty = 10$ m/s past a circular cylinder, find the pressure at the top of the cylinder relative to $p_\infty$, and the angles where $C_p = 0$.

<details>
<summary>Answer</summary>

$C_p = 1 - 4\sin^2\theta$.

At the top ($\theta = 90^\circ$), $C_p = -3$, so $p - p_\infty = -3 \times \frac{1}{2}(1.225)(10)^2 = -183.8$ Pa.

$C_p = 0$ when $\sin^2\theta = 1/4$, which gives $\theta = 30^\circ, 150^\circ, 210^\circ, 330^\circ$.

The distribution is symmetric front-to-back and top-to-bottom, so the net force is zero (d'Alembert's paradox).

</details>

**Exercise 3.** Superpose a uniform flow $U_\infty = 5$ m/s with a line source of strength $m = 2$ m²/s at the origin (a Rankine half-body). Find the stagnation point and the width of the body far downstream.

<details>
<summary>Answer</summary>

On the negative $x$-axis, $u = U_\infty + \frac{m}{2\pi x}$. This is zero at

```math
x_s = -\frac{m}{2\pi U_\infty} = -\frac{2}{2\pi \times 5} = -0.0637 \text{ m}
```

Far downstream, all the source flow $m$ passes between the two dividing streamlines at speed $U_\infty$. The body width is therefore $m/U_\infty = 0.4$ m, with half-width $m/(2U_\infty) = 0.2$ m.

</details>

**Exercise 4.** A cylinder of radius $a = 0.5$ m spins in an air stream ($\rho = 1.225$ kg/m³, $U_\infty = 10$ m/s) and carries circulation $\Gamma = 20$ m²/s. Find the stagnation-point angles and the magnitude of the force per unit span. With the note's convention ($\Gamma > 0$ counterclockwise, flow in $+x$), which way does the force point?

<details>
<summary>Answer</summary>

On the surface, $u_\theta = -2U_\infty\sin\theta + \frac{\Gamma}{2\pi a}$. Setting this to zero:

```math
\sin\theta_s = \frac{\Gamma}{4\pi U_\infty a} = \frac{20}{4\pi \times 10 \times 0.5} = 0.318
```

so $\theta_s = 18.6^\circ$ and $161.4^\circ$.

The force magnitude is $L = \rho U_\infty\Gamma = 1.225 \times 10 \times 20 = 245$ N/m.

Counterclockwise circulation slows the flow over the top ($\theta = 90^\circ$) and speeds it up underneath. The pressure is therefore higher on top, so the force points in $-y$. The Blasius theorem gives $F_y = -\rho U_\infty\Gamma$. Clockwise circulation would give upward lift.

</details>

**Exercise 5.** Starting from $F(z) = U_\infty\left(z + \frac{a^2}{z}\right)$, compute the complex velocity $w$. Show that the surface speed is $2U_\infty|\sin\theta|$, and use the Blasius theorem to show that the net force is zero.

<details>
<summary>Answer</summary>

$w = dF/dz = U_\infty(1 - a^2/z^2)$. On $z = a e^{i\theta}$,

```math
w = U_\infty(1 - e^{-2i\theta}) = U_\infty
e^{-i\theta}(e^{i\theta} - e^{-i\theta}) = 2iU_\infty\sin\theta\, e^{-i\theta}
```

so $|w| = 2U_\infty|\sin\theta|$.

Next, $w^2 = U_\infty^2(1 - 2a^2/z^2 + a^4/z^4)$ has no $1/z$ term. By the residue theorem $\oint w^2 dz = 0$, so $F_x - iF_y = 0$: there is neither drag nor lift.

</details>

## References

- L. M. Milne-Thomson, *Theoretical Hydrodynamics*, 5th ed., Macmillan, 1968.
- J. Katz, A. Plotkin, *Low-Speed Aerodynamics*, 2nd ed., Cambridge University Press, 2001.
- G. K. Batchelor, *An Introduction to Fluid Dynamics*, Cambridge University Press, 1967.
- D. J. Acheson, *Elementary Fluid Dynamics*, Oxford University Press, 1990.
