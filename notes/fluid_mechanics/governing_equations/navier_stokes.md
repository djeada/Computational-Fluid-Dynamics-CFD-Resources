# Navier-Stokes Equations

The Navier-Stokes equations describe the **conservation of momentum** in fluid flow and are among the most important equations in fluid mechanics. They represent Newton's second law applied to fluid motion, accounting for pressure forces, viscous forces, and body forces.

## Physical Principle

The Navier-Stokes equations are based on the principle that the rate of change of momentum of a fluid particle equals the sum of all forces acting on it:

**Rate of momentum change = Pressure forces + Viscous forces + Body forces**

## General Form

The general form of the Navier-Stokes equations for a Newtonian fluid is:

$$
\boxed{\rho \frac{D\vec{v}}{Dt} = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \vec{f}}
$$

where:

- $\rho$ = fluid density
- $\vec{v}$ = velocity vector
- $\frac{D}{Dt}$ = material derivative
- $p$ = pressure
- $\boldsymbol{\tau}$ = viscous stress tensor
- $\vec{f}$ = body force per unit mass (e.g., gravity)

## Material Derivative

The material derivative represents the total rate of change following a fluid particle:

$$
\frac{D\vec{v}}{Dt} = \frac{\partial \vec{v}}{\partial t} +
(\vec{v} \cdot \nabla)\vec{v}
$$

This includes:

- **Local acceleration**: $\frac{\partial \vec{v}}{\partial t}$ (time-dependent changes)
- **Convective acceleration**: $(\vec{v} \cdot \nabla)\vec{v}$ (spatial changes due to particle motion)

## Viscous Stress Tensor

For a **Newtonian fluid**, the viscous stress tensor is:

$$
\boldsymbol{\tau} = \mu \left[\nabla \vec{v} + (\nabla \vec{v})^T\right] + \lambda
(\nabla \cdot \vec{v})\boldsymbol{I}
$$

where:

- $\mu$ = dynamic viscosity
- $\lambda$ = second viscosity coefficient (Stokes' hypothesis $\lambda = -\frac{2}{3}\mu$ corresponds to zero bulk viscosity $\lambda + \frac{2}{3}\mu$)
- $\boldsymbol{I}$ = identity tensor

For incompressible flow ($\nabla \cdot \vec{v} = 0$), this simplifies to:

$$
\boldsymbol{\tau} = \mu \left[\nabla \vec{v} + (\nabla \vec{v})^T\right]
$$

## Incompressible Form

For **incompressible flow** with constant density and viscosity:

$$
\boxed{\rho \left(\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v}\right) = -\nabla p + \mu \nabla^2 \vec{v} + \rho \vec{f}}
$$

This can be written in terms of kinematic viscosity $\nu = \mu/\rho$:

$$
\frac{\partial \vec{v}}{\partial t} +
(\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \vec{v} + \vec{f}
$$

## Component Forms

### Cartesian Coordinates

In Cartesian coordinates $(x, y, z)$ with velocity components $(u, v, w)$:

**$x$-momentum:**

$$
\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} + v
\frac{\partial u}{\partial y} + w \frac{\partial u}{\partial z} = -\frac{1}{\rho}
\frac{\partial p}{\partial x} + \nu\nabla^2 u + f_x
$$

**$y$-momentum:**

$$
\frac{\partial v}{\partial t} + u \frac{\partial v}{\partial x} + v
\frac{\partial v}{\partial y} + w \frac{\partial v}{\partial z} = -\frac{1}{\rho}
\frac{\partial p}{\partial y} + \nu\nabla^2 v + f_y
$$

**$z$-momentum:**

$$
\frac{\partial w}{\partial t} + u \frac{\partial w}{\partial x} + v
\frac{\partial w}{\partial y} + w \frac{\partial w}{\partial z} = -\frac{1}{\rho}
\frac{\partial p}{\partial z} + \nu\nabla^2 w + f_z
$$

where $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2}$ is the Laplacian operator.

### Cylindrical Coordinates

In cylindrical coordinates $(r, \theta, z)$:

**$r$-momentum:**

$$
\frac{\partial v_r}{\partial t} + v_r \frac{\partial v_r}{\partial r} +
\frac{v_\theta}{r} \frac{\partial v_r}{\partial \theta} + v_z
\frac{\partial v_r}{\partial z} - \frac{v_\theta^2}{r} = -\frac{1}{\rho}
\frac{\partial p}{\partial r} +
\nu\left(\nabla^2 v_r - \frac{v_r}{r^2} - \frac{2}{r^2}
\frac{\partial v_\theta}{\partial \theta}\right) + f_r
$$

**$\theta$-momentum:**

$$
\frac{\partial v_\theta}{\partial t} + v_r \frac{\partial v_\theta}{\partial r} +
\frac{v_\theta}{r} \frac{\partial v_\theta}{\partial \theta} + v_z
\frac{\partial v_\theta}{\partial z} + \frac{v_r v_\theta}{r} = -\frac{1}{\rho r}
\frac{\partial p}{\partial \theta} +
\nu\left(\nabla^2 v_\theta - \frac{v_\theta}{r^2} + \frac{2}{r^2}
\frac{\partial v_r}{\partial \theta}\right) + f_\theta
$$

**$z$-momentum:**

$$
\frac{\partial v_z}{\partial t} + v_r \frac{\partial v_z}{\partial r} +
\frac{v_\theta}{r} \frac{\partial v_z}{\partial \theta} + v_z
\frac{\partial v_z}{\partial z} = -\frac{1}{\rho} \frac{\partial p}{\partial z} +
\nu\nabla^2 v_z + f_z
$$

## Special Cases

### Euler Equations (Inviscid Flow)

For **inviscid flow** ($\mu = 0$):

$$
\frac{\partial \vec{v}}{\partial t} +
(\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \vec{f}
$$

### Stokes Equations (Creeping Flow)

For **very low Reynolds number flow** (inertial terms negligible):

$$
0 = -\nabla p + \mu \nabla^2 \vec{v} + \rho \vec{f}
$$

This is linear in velocity and much easier to solve.

### Steady Flow

For **steady flow** ($\frac{\partial}{\partial t} = 0$):

$$
(\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \vec{v} + \vec{f}
$$

## Dimensionless Form

The equations are often non-dimensionalized using characteristic scales:

- Length scale: $L$
- Velocity scale: $U$
- Time scale: $T = L/U$
- Pressure scale: $\rho U^2$

This introduces the **Reynolds number**:

$$
Re = \frac{\rho U L}{\mu} = \frac{UL}{\nu}
$$

The dimensionless Navier-Stokes equations become:

```math
\frac{\partial \vec{v}^*}{\partial t^*} +
(\vec{v}^* \cdot \nabla^*)\vec{v}^* = -\nabla^* p^* + \frac{1}{Re}\nabla^{*2}
\vec{v}^* + \frac{1}{Fr^2}\vec{g}^*
```

where asterisks denote dimensionless variables and $Fr = U/\sqrt{gL}$ is the Froude number.

## Physical Terms

### Pressure Force

$$
-\nabla p
$$

- Represents force due to pressure gradients
- Always points from high to low pressure
- Normal to isobars (constant pressure lines)

### Viscous Force

$$
\nabla \cdot \boldsymbol{\tau} = \mu \nabla^2 \vec{v} \quad
\text{(incompressible flow, constant } \mu \text{)}
$$

- Represents internal friction effects
- Tends to smooth out velocity gradients
- Proportional to second derivatives of velocity

### Convective Acceleration

$$
(\vec{v} \cdot \nabla)\vec{v}
$$

- Represents acceleration due to spatial velocity changes
- **Nonlinear term** that makes the equations complex
- Responsible for many interesting flow phenomena

### Body Forces

$$
\rho \vec{f}
$$

- External forces acting on fluid volume
- Most common: gravity ($\vec{f} = \vec{g}$)
- Can include electromagnetic forces, centrifugal forces, etc.

## Boundary Conditions

### No-Slip Condition

At solid walls:

$$
\vec{v} = \vec{v}_{wall}
$$

For stationary walls: $\vec{v} = 0$

### Free-Slip Condition

At free surfaces or symmetry planes:

$$
\vec{v} \cdot \vec{n} = 0, \quad \frac{\partial v_t}{\partial n} = 0
$$

where $v_t$ is tangential velocity and $n$ is normal direction.

### Inflow/Outflow Conditions

- **Inflow**: Specify velocity profile or pressure
- **Outflow**: Often use zero-gradient conditions

## Exact Solutions

Several exact solutions exist for simplified geometries:

### Couette Flow

Flow between parallel plates, one moving:

$$
u(y) = \frac{U y}{h}
$$

where $U$ is the plate velocity and $h$ is the gap height.

### Poiseuille Flow

Pressure-driven flow in a circular pipe:

$$
u(r) = \frac{\Delta p}{4\mu L}(R^2 - r^2)
$$

where $\Delta p$ is pressure drop, $L$ is pipe length, and $R$ is pipe radius.

### Stagnation Point Flow

Flow near a stagnation point:

$$
u = ax, \quad v = -ay
$$

where $a$ is a constant related to the strain rate.

## Turbulence and Reynolds Number

### Laminar Flow

- Low $Re$: viscous forces dominate
- Smooth, ordered motion
- Predictable behavior

### Turbulent Flow

- High $Re$: inertial forces dominate
- Chaotic, irregular motion
- Requires statistical treatment (RANS, LES, DNS)

### Critical Reynolds Number

The transition occurs around:

- Pipe flow: $Re_c \approx 2300$
- Flat plate: $Re_c \approx 5 \times 10^5$

## Numerical Solution Methods

The Navier-Stokes equations are typically solved numerically using:

### Finite Difference Method (FDM)

- Approximates derivatives using difference formulas
- Good for structured grids

### Finite Volume Method (FVM)

- Based on conservation principles
- Widely used in commercial CFD codes

### Finite Element Method (FEM)

- Uses variational formulation
- Good for complex geometries

### Spectral Methods

- Uses global basis functions
- High accuracy for smooth solutions

## Computational Challenges

### Nonlinearity

The convective term makes the equations nonlinear, requiring iterative solution methods.

### Pressure-Velocity Coupling

Pressure doesn't appear explicitly in continuity equation for incompressible flow, requiring special algorithms (SIMPLE, PISO, etc.).

### Turbulence

High Reynolds number flows require turbulence modeling or very fine grids (DNS).

### Stiffness

Multiple time scales can make the equations stiff, requiring implicit time integration.

## Historical Development

- **1755**: Euler formulated equations for inviscid flow
- **1822**: Navier added viscous terms
- **1845**: Stokes provided complete mathematical formulation
- **1904**: Prandtl introduced boundary layer concept
- **1950s**: First numerical solutions on computers

## Applications

The Navier-Stokes equations enable analysis of:

- **Aerodynamics**: Aircraft and vehicle design
- **Hydrodynamics**: Ship hulls and propellers
- **Internal flows**: Pipe networks and turbomachinery
- **Environmental flows**: Weather prediction and ocean currents
- **Biomedical flows**: Blood flow and respiratory systems

## Mathematical Properties

### Existence and Uniqueness

The question of existence and uniqueness of solutions to the Navier-Stokes equations remains one of the **Clay Millennium Problems** in mathematics.

### Conservation Properties

The equations conserve:

- Mass (when coupled with continuity)
- Momentum
- Angular momentum
- Energy (in absence of viscosity)

Understanding the Navier-Stokes equations is fundamental to all of fluid mechanics and forms the basis for both theoretical analysis and computational fluid dynamics.

## Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib.
- [Froude Number vs. Flow Velocity](../../../scripts/plots/froude_number/): plots the length-based Froude number $Fr = U/\sqrt{gL}$ against speed for hulls of 5, 10, 15, and 20 m, with reference lines at hull speed and at the approximate start of planing.
- [Kelvin-Helmholtz Instability Simulation](../../../scripts/simulations/kelvin_helmholtz_instability/): simulates the Kelvin-Helmholtz instability, the rolling-up of a shear layer between fluid streams moving in opposite directions, in a periodic 2D incompressible flow animated with Matplotlib.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and animates the temperature field with Matplotlib.
- [Simplified Real-Time Fluid Dynamics Simulator](../../../scripts/simulations/simplified_real_time_fluid_dynamics_simulator/): is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window.
- [Velocity Layers and Viscosity](../../../scripts/plots/velocity_layers_viscosity/): draws a schematic of three stacked fluid layers moving at different speeds to illustrate Newton's law of viscosity, $`\tau = \mu\, du/dy`$.
- [Wall Shear in Pipe Cross-Section](../../../scripts/plots/wall_shear_pipe_cross_section/): sketches fully developed laminar (Hagen-Poiseuille) flow in a circular pipe, with velocity arrows whose lengths follow the parabolic profile $u(r) = u_{max}(1 - (r/R)^2)$.
- [Rayleigh-Taylor Instability](../../../scripts/simulations/rayleigh_taylor_instability/): simulates the Rayleigh-Taylor instability of heavy fluid resting on light fluid in a tall 2D box and animates how a rippled interface grows into rising bubbles and falling mushroom-shaped spikes.
- [SPH Dam Break](../../../scripts/simulations/sph_dam_break/): simulates the collapse of a water column in a closed tank, the classic dam-break problem, with weakly compressible smoothed particle hydrodynamics (SPH), and animates the water particles coloured by their speed.

## Exercises

**Exercise 1.** Compute $Re = UL/\nu$ in water ($\nu = 1.0 \times 10^{-6}$ m²/s) for (a) a bacterium swimming at $U = 30$ μm/s with $L = 1$ μm and (b) a ship at $U = 10$ m/s with $L = 100$ m. Which simplified form of the equations suits each?

<details>
<summary>Answer</summary>

(a) $Re = (30 \times 10^{-6})(10^{-6})/10^{-6} = 3 \times 10^{-5}$. Inertia is negligible, so the Stokes equations $0 = -\nabla p + \mu\nabla^2\vec{v}$ apply.

(b) $Re = 10 \times 100/10^{-6} = 10^9$. The flow outside thin boundary layers is essentially inviscid (Euler equations), the boundary layers themselves are turbulent, and the complete problem needs RANS or LES modeling.

</details>

**Exercise 2.** Verify that the Couette profile $u = Uy/h$, $v = 0$ with uniform pressure is an exact solution of the incompressible Navier–Stokes equations that satisfies the no-slip conditions, and find the wall shear stress.

<details>
<summary>Answer</summary>

- Continuity: $\partial u/\partial x = 0$ and $v = 0$, so it holds.
- $x$-momentum: $\partial u/\partial t = 0$, $`u\,\partial u/\partial x = 0`$, $`v\,\partial u/\partial y = 0`$, $\partial p/\partial x = 0$ and $`\nu\,\partial^2 u/\partial y^2 = 0`$, so every term vanishes.
- $y$-momentum: every term is zero.
- No-slip: $u(0) = 0$ and $u(h) = U$.

The shear stress is uniform: $`\tau = \mu\, du/dy = \mu U/h`$.

</details>

**Exercise 3.** Starting from $u(r) = \frac{\Delta p}{4\mu L}(R^2 - r^2)$, derive the Hagen–Poiseuille flow rate and show that the mean velocity is half the centreline velocity. Evaluate $u_{max}$, $Q$ and $Re = \rho \bar{V} (2R)/\mu$ for water ($\rho = 998$ kg/m³, $\mu = 1.0 \times 10^{-3}$ Pa s) with $R = 1$ mm, $L = 1$ m and $\Delta p = 100$ Pa.

<details>
<summary>Answer</summary>

```math
Q = \int_0^R u\, 2\pi r\,
dr = \frac{\pi \Delta p}{2\mu L}\left(\frac{R^4}{2} -
\frac{R^4}{4}\right) = \frac{\pi R^4 \Delta p}{8\mu L}
```

Since $u_{max} = \Delta p R^2/(4\mu L)$, the mean velocity is $\bar{V} = Q/(\pi R^2) = \Delta p R^2/(8\mu L) = u_{max}/2$.

Numbers:

- $u_{max} = 100 \times 10^{-6}/(4 \times 10^{-3}) = 0.025$ m/s
- $Q = \pi \times 10^{-12} \times 100/(8 \times 10^{-3}) = 3.93 \times 10^{-8}$ m³/s
- $\bar{V} = 0.0125$ m/s
- $Re = 998 \times 0.0125 \times 0.002/10^{-3} = 25$, which is laminar, so the solution is self-consistent.

</details>

**Exercise 4.** For the stagnation-point flow $u = ax$, $v = -ay$ (steady, no body force), show that the flow is incompressible and irrotational, and use the Navier–Stokes equations to find the pressure field.

<details>
<summary>Answer</summary>

$\partial u/\partial x + \partial v/\partial y = a - a = 0$, and $\omega_z = \partial v/\partial x - \partial u/\partial y = 0$. The viscous terms vanish because $\nabla^2 u = \nabla^2 v = 0$.

- $x$-momentum: $`u\,\partial u/\partial x = a^2 x = -\frac{1}{\rho}\partial p/\partial x`$.
- $y$-momentum: $`v\,\partial v/\partial y = a^2 y = -\frac{1}{\rho}\partial p/\partial y`$.

Integrating both,

```math
p = p_0 - \frac{\rho a^2}{2}(x^2 + y^2)
```

which is Bernoulli's equation with $p_0$ the stagnation pressure. This field does not satisfy no-slip on the wall $y = 0$. Hiemenz's solution adds a thin viscous layer there.

</details>

**Exercise 5.** Pressure-driven flow between parallel plates at $y = \pm h$ has $dp/dx = -G$ (constant). Reduce the $x$-momentum equation for fully developed flow, solve for $u(y)$, and find the flow rate per unit width and the ratio of mean to maximum velocity.

<details>
<summary>Answer</summary>

For fully developed flow, $v = 0$ and $u = u(y)$, so the convective terms vanish and $`0 = G + \mu\, d^2u/dy^2`$. With $u(\pm h) = 0$:

```math
u(y) = \frac{G}{2\mu}(h^2 - y^2)
```

The flow rate per unit width is

```math
q = \int_{-h}^{h} u\, dy = \frac{2 G h^3}{3\mu}
```

The maximum is $u_{max} = Gh^2/(2\mu)$ and the mean is $\bar{u} = q/(2h) = Gh^2/(3\mu)$, so $\bar{u}/u_{max} = 2/3$. For a round pipe the ratio is $1/2$.

</details>

## References

- G. K. Batchelor, *An Introduction to Fluid Dynamics*, Cambridge University Press, 1967.
- F. M. White, *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- R. L. Panton, *Incompressible Flow*, 4th ed., Wiley, 2013.
- L. D. Landau, E. M. Lifshitz, *Fluid Mechanics*, 2nd ed., Pergamon Press, 1987.
