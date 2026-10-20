# Governing Equations for CFD

This note collects the equations a CFD solver discretizes, written in the forms the numerical methods need: the integral and differential conservation form for compressible flow, the incompressible form with its special treatment of pressure, a generic transport equation, the dimensionless groups that measure which terms dominate, and the mathematical classification that decides which boundary conditions are needed and how a solution can be marched. The physical derivations are in [Continuity Equation](../../fluid_mechanics/governing_equations/continuity.md), [Navier-Stokes Equations](../../fluid_mechanics/governing_equations/navier_stokes.md), [Energy Equation in Fluid Mechanics](../../fluid_mechanics/governing_equations/energy.md) and [Equation of State](../../fluid_mechanics/governing_equations/equation_of_state.md), and are not repeated here.

## Problem Statement

A single-phase Newtonian fluid is described by its density $\rho$, velocity $\mathbf{u} = (u, v, w)$, pressure $p$ and temperature $T$ (or specific total energy $E$) as functions of position $\mathbf{x}$ and time $t$. The equations express conservation of mass, momentum and energy, closed by constitutive laws for the viscous stress and the heat flux and by an equation of state. A numerical method needs to know three things about them:

1. In which form to discretize them. The conservation (divergence) form lets the discrete scheme conserve mass, momentum and energy exactly and capture shocks at the right speed.
2. Which terms dominate, measured by the Reynolds, Mach and Péclet numbers. This decides the discretization of convection, the treatment of pressure and the resolution required.
3. The mathematical type of the equations (elliptic, parabolic or hyperbolic). This decides how many boundary conditions are needed and where, and whether the solution can be marched in time or space or must be found everywhere at once.

## Integral Form and the Reynolds Transport Theorem

Conservation laws are stated for a material system, a fixed set of fluid particles, but CFD works on fixed control volumes. The Reynolds transport theorem connects the two: for an extensive property $B$ with intensive value $\beta = dB/dm$ and a control volume $V$ fixed in space with outward unit normal $\mathbf{n}$ on its surface $A$,

```math
\frac{dB_{\mathrm{sys}}}{dt} = \frac{d}{dt}\int_V \rho\beta \, dV + \oint_A \rho\beta \,
\mathbf{u}\cdot\mathbf{n} \, dA
```

The rate of change of $B$ for the system equals its rate of change inside the control volume plus its net outflow through the surface. Setting $\beta = 1$, $\mathbf{u}$ and $E$ and inserting the physical laws (mass is conserved; momentum changes by the surface and body forces; energy changes by heat transfer and work) gives every conservation law in the generic integral form

```math
\frac{d}{dt}\int_V \mathbf{U} \, dV + \oint_A
\left(\mathbf{F}_c - \mathbf{F}_v\right)\cdot\mathbf{n} \, dA = \int_V \mathbf{S} \, dV
```

where $\mathbf{U}$ is the vector of conserved variables per unit volume, $\mathbf{F}_c$ the convective (inviscid) flux, $\mathbf{F}_v$ the viscous and conductive flux and $\mathbf{S}$ the volume sources. The finite-volume method applies this equation to each cell of the mesh, so the flux leaving one cell through a face is exactly the flux entering its neighbour. Applying the divergence theorem to a fixed volume and using that $V$ is arbitrary gives the differential conservation form

$$
\frac{\partial\mathbf{U}}{\partial t} +
\nabla\cdot\left(\mathbf{F}_c - \mathbf{F}_v\right) = \mathbf{S}
$$

The integral form is the more general one: it remains valid across shocks and contact discontinuities, where derivatives do not exist.

## Compressible Navier–Stokes Equations in Conservation Form

The conserved variables, fluxes and sources are

```math
\mathbf{U} = \begin{bmatrix} \rho \\ \rho\mathbf{u} \\ \rho E \end{bmatrix},
\qquad
\mathbf{F}_c = \begin{bmatrix} \rho\mathbf{u} \\ \rho\mathbf{u}\otimes\mathbf{u} + p\mathbf{I} \\ (\rho E + p)\,\mathbf{u} \end{bmatrix},
\qquad
\mathbf{F}_v = \begin{bmatrix} \mathbf{0} \\ \boldsymbol{\tau} \\ \boldsymbol{\tau}\cdot\mathbf{u} - \mathbf{q} \end{bmatrix},
\qquad
\mathbf{S} = \begin{bmatrix} 0 \\ \rho\mathbf{f} \\ \rho\mathbf{f}\cdot\mathbf{u} + \dot{q}_s \end{bmatrix}
```

with $E = e + \tfrac{1}{2}|\mathbf{u}|^2$ the specific total energy, $e$ the specific internal energy, $\mathbf{f}$ the body force per unit mass and $\dot{q}_s$ a volumetric heat source. For a Newtonian fluid with Stokes' hypothesis (zero bulk viscosity) and Fourier conduction,

$$
\boldsymbol{\tau} = \mu\left(\nabla\mathbf{u} + \nabla\mathbf{u}^T\right) -
\frac{2}{3}\mu\left(\nabla\cdot\mathbf{u}\right)\mathbf{I},
\qquad \mathbf{q} = -k\nabla T
$$

where $\mu$ is the dynamic viscosity and $k$ the thermal conductivity. For a calorically perfect gas the system is closed by

```math
p = \rho R T = (\gamma - 1)\,\rho\left(E - \frac{1}{2}|\mathbf{u}|^2\right),
\qquad e = c_v T
```

with gas constant $R$ and ratio of specific heats $\gamma = c_p/c_v$.

In two dimensions, written component by component as $\partial\mathbf{U}/\partial t + \partial(\mathbf{F} - \mathbf{F}_v)/\partial x + \partial(\mathbf{G} - \mathbf{G}_v)/\partial y = \mathbf{S}$, the vectors are

```math
\mathbf{U} = \begin{bmatrix} \rho \\ \rho u \\ \rho v \\ \rho E \end{bmatrix},
\quad
\mathbf{F} = \begin{bmatrix} \rho u \\ \rho u^2 + p \\ \rho u v \\ (\rho E + p)u \end{bmatrix},
\quad
\mathbf{G} = \begin{bmatrix} \rho v \\ \rho u v \\ \rho v^2 + p \\ (\rho E + p)v \end{bmatrix},
\quad
\mathbf{F}_v = \begin{bmatrix} 0 \\ \tau_{xx} \\ \tau_{xy} \\ u\tau_{xx} + v\tau_{xy} - q_x \end{bmatrix},
\quad
\mathbf{G}_v = \begin{bmatrix} 0 \\ \tau_{xy} \\ \tau_{yy} \\ u\tau_{xy} + v\tau_{yy} - q_y \end{bmatrix}
```

with $\tau_{xx} = \tfrac{2}{3}\mu(2\partial_x u - \partial_y v)$, $\tau_{yy} = \tfrac{2}{3}\mu(2\partial_y v - \partial_x u)$ and $\tau_{xy} = \mu(\partial_y u + \partial_x v)$. There are four equations for the four conserved variables; $p$ and $T$ are computed from them through the equation of state.

Without the viscous and conductive fluxes the system reduces to the Euler equations. In one dimension their flux Jacobian $\partial\mathbf{F}/\partial\mathbf{U}$ has the real eigenvalues $u - c$, $u$ and $u + c$, where $c = \sqrt{\gamma p/\rho}$ is the speed of sound. These are the speeds at which acoustic waves and entropy waves carry information. They determine the stable time step of explicit schemes, the upwind direction in [Riemann Solvers and Godunov Methods](../fvm/riemann_solvers.md) and the number of boundary conditions at inflow and outflow ([Boundary Conditions](./boundary_conditions.md)).

### Why the Conservation Form Matters

The same equations can be written in non-conservative (primitive-variable) form, for example the momentum equation as $\rho(\partial_t\mathbf{u} + \mathbf{u}\cdot\nabla\mathbf{u}) = -\nabla p + \nabla\cdot\boldsymbol{\tau} + \rho\mathbf{f}$. For smooth solutions the two forms are equivalent. For discrete solutions they are not. A scheme in conservation form telescopes: summing the discrete equations over all cells cancels every interior flux, so the total mass, momentum and energy change only through the boundaries. Lax and Wendroff (1960) showed that if a conservative scheme converges, it converges to a weak solution of the conservation law, which satisfies the correct shock jump (Rankine–Hugoniot) conditions. A non-conservative scheme can converge to a solution with the wrong shock speed and strength. Compressible solvers therefore discretize the conservation form; incompressible solvers usually do as well, because it guarantees discrete mass conservation.

## Incompressible Flow and the Role of Pressure

When the Mach number is small and temperature variations are modest, $\rho$ is constant and the mass equation becomes a constraint on the velocity. With kinematic viscosity $\nu = \mu/\rho$ and constant $\mu$,

$$
\nabla\cdot\mathbf{u} = 0,
\qquad \frac{\partial\mathbf{u}}{\partial t} +
\nabla\cdot(\mathbf{u}\otimes\mathbf{u}) = -\frac{1}{\rho}\nabla p +
\nu\nabla^2\mathbf{u} + \mathbf{f}
$$

The term $\nabla\cdot(\mathbf{u}\otimes\mathbf{u})$ equals $(\mathbf{u}\cdot\nabla)\mathbf{u}$ because $\nabla\cdot\mathbf{u} = 0$, but its divergence form is the one discretized. The energy equation decouples: with constant properties the temperature obeys $\rho c_p(\partial_t T + \mathbf{u}\cdot\nabla T) = k\nabla^2 T + \Phi$, with viscous dissipation $\Phi$, and can be solved after the flow as a passive scalar. Buoyancy-driven flows reintroduce coupling through the Boussinesq term $\mathbf{f} = -\beta(T - T_0)\mathbf{g}$, with thermal expansion coefficient $\beta$.

The pressure no longer has an evolution equation or a thermodynamic meaning. It is the Lagrange multiplier that enforces the constraint $\nabla\cdot\mathbf{u} = 0$. This is clearest for steady Stokes flow, whose solution makes the Lagrangian

```math
\mathcal{L}(\mathbf{u}, p) = \int_\Omega \left(\frac{\mu}{2}\nabla\mathbf{u} : \nabla\mathbf{u} - \rho\,\mathbf{f}\cdot\mathbf{u} - p\,\nabla\cdot\mathbf{u}\right) dV
```

stationary: varying $\mathbf{u}$ gives $-\mu\nabla^2\mathbf{u} + \nabla p = \rho\mathbf{f}$ and varying $p$ gives $\nabla\cdot\mathbf{u} = 0$. The pressure takes whatever value is needed to keep the velocity divergence-free. Taking the divergence of the momentum equation and using the constraint gives the pressure Poisson equation

```math
\nabla^2 p = -\rho\, \frac{\partial u_i}{\partial x_j}
\frac{\partial u_j}{\partial x_i} + \rho\,\nabla\cdot\mathbf{f}
```

an elliptic equation: a change of velocity anywhere is felt by the pressure everywhere at once, which is the limit of infinite sound speed. If velocity is prescribed on the whole boundary, $p$ is determined only up to a constant, and a reference value must be fixed at one point or by a zero-mean condition.

For the numerics this has three consequences. After discretization the system has the saddle-point structure

```math
\begin{bmatrix} \mathbf{A} & \mathbf{G} \\ \mathbf{D} & \mathbf{0} \end{bmatrix}
\begin{bmatrix} \mathbf{u} \\ \mathbf{p} \end{bmatrix} =
\begin{bmatrix} \mathbf{b} \\ \mathbf{0} \end{bmatrix}
```

with a zero diagonal block for pressure, where $\mathbf{A}$ contains the discretized convection and diffusion, $\mathbf{G}$ the pressure gradient and $\mathbf{D}$ the divergence. It cannot be solved by applying a standard iterative method to each equation in turn. Segregated algorithms (projection methods, SIMPLE, PISO) instead derive a pressure or pressure-correction equation from the constraint. And on collocated grids the discrete gradient and divergence must be chosen compatibly, or checkerboard pressure modes appear. These topics are covered in [Pressure–Velocity Coupling](../fvm/pressure_velocity_coupling.md).

## The Generic Transport Equation

Mass, momentum components, enthalpy, species and turbulence quantities all obey equations of the same structure. Following Patankar (1980), a scalar $\phi$ per unit mass satisfies

$$
\underbrace{\frac{\partial(\rho\phi)}{\partial t}}_{\text{unsteady}} +
\underbrace{\nabla\cdot(\rho\mathbf{u}\phi)}_{\text{convection}} = \underbrace{\nabla\cdot(\Gamma\nabla\phi)}_{\text{diffusion}} + \underbrace{S_\phi}_{\text{source}}
$$

| Equation | $\phi$ | $\Gamma$ | $S_\phi$ |
| --- | --- | --- | --- |
| Mass | 1 | 0 | 0 |
| $x$-momentum (incompressible, constant $\mu$) | $u$ | $\mu$ | $-\partial p/\partial x + \rho f_x$ |
| Energy (constant $c_p$) | $T$ | $k/c_p$ | $(\Phi + \dot{q}_s)/c_p$ |
| Species mass fraction | $Y_k$ | $\rho D_k$ | reaction rate $\dot\omega_k$ |
| Turbulent kinetic energy | $k$ | $\mu + \mu_t/\sigma_k$ | $P_k - \rho\varepsilon$ |

A solver that discretizes this one equation well (convection, diffusion, unsteady term, sources and boundary conditions) can solve all of them; the pressure is the exception and needs the coupling algorithms above. The discretization of the convection and diffusion terms is developed in [Finite Volume Discretization on General Meshes](../fvm/discretization.md) and [Convection Schemes for Finite Volume Methods](../fvm/convection_schemes.md).

## Non-Dimensionalization

Scaling lengths by $L$, velocities by $U$, time by $L/U$ and pressure by $\rho U^2$, and writing starred quantities for the dimensionless variables, the incompressible momentum equation without body force becomes

$$
\frac{\partial\mathbf{u}^\ast}{\partial t^\ast} +
(\mathbf{u}^\ast\cdot\nabla^\ast)\mathbf{u}^\ast = -\nabla^\ast p^\ast +
\frac{1}{Re}\nabla^{\ast 2}\mathbf{u}^\ast
$$

All flows with the same geometry, boundary conditions and Reynolds number have the same dimensionless solution. The dimensionless groups also say which terms dominate, and that decides much of the numerical method.

| Group | Definition | Ratio | Consequence for the numerics |
| --- | --- | --- | --- |
| Reynolds number | $Re = UL/\nu$ | Convection to viscous diffusion | High $Re$: thin boundary and shear layers that must be resolved or modelled, turbulence, convection-dominated discrete equations that need upwind-biased schemes |
| Mach number | $Ma = U/c$ | Flow speed to sound speed | $Ma < 0.3$: incompressible form is adequate. Compressible solvers at low $Ma$ become stiff (acoustic speed $c$ much larger than $U$ limits the time step) and need low-Mach preconditioning. $Ma > 1$: shocks, shock-capturing schemes |
| Péclet number | $`Pe = UL/\alpha = Re\,Pr`$ | Convection to diffusion of heat or a scalar ($`\alpha = k/(\rho c_p)`$) | High $Pe$: thin thermal layers; the same upwinding issue as high $Re$ |
| Cell Péclet (or cell Reynolds) number | $Pe_\Delta = u\Delta x/\Gamma'$, $\Gamma' = \Gamma/\rho$ | Convection to diffusion across one cell | Central differencing of convection gives bounded, non-oscillatory solutions only for $Pe_\Delta \le 2$ |
| Prandtl number | $Pr = \nu/\alpha$ | Momentum to thermal diffusivity | $Pr \gg 1$ (oils): thermal layer much thinner than the velocity layer, finer near-wall mesh for heat transfer |
| Strouhal number | $St = fL/U$ | Unsteady time scale to convective time scale | Sets the time step needed to resolve vortex shedding |
| Froude number | $Fr = U/\sqrt{gL}$ | Inertia to gravity | Free-surface and stratified flows |

## Classification of Partial Differential Equations

### Second-Order Equations in Two Variables

The linear second-order equation

$$
a \frac{\partial^2\phi}{\partial x^2} + b \frac{\partial^2\phi}{\partial x\partial y} +
c \frac{\partial^2\phi}{\partial y^2} + d \frac{\partial\phi}{\partial x} + e
\frac{\partial\phi}{\partial y} + f\phi = g
$$

is classified by its discriminant $b^2 - 4ac$, which depends only on the highest derivatives:

| Discriminant | Type | Characteristic curves $dy/dx = \left(b \pm \sqrt{b^2 - 4ac}\right)/(2a)$ | Model equation |
| --- | --- | --- | --- |
| $b^2 - 4ac < 0$ | Elliptic | None (complex) | Laplace and Poisson, $\phi_{xx} + \phi_{yy} = g$ |
| $b^2 - 4ac = 0$ | Parabolic | One family | Heat equation, $\phi_t = \alpha\phi_{xx}$ (with $y = t$) |
| $b^2 - 4ac > 0$ | Hyperbolic | Two real families | Wave equation, $\phi_{tt} = c^2\phi_{xx}$ |

Along characteristics, information propagates and the solution may have discontinuities in its derivatives. If the coefficients depend on position or on the solution, the type can change within the domain. The classical example is the linearized potential equation for steady compressible flow,

$$
(1 - Ma^2) \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0
$$

with discriminant $-4(1 - Ma^2)$: it is elliptic for subsonic flow and hyperbolic for supersonic flow, where the characteristics are the Mach lines at angle $\arcsin(1/Ma)$ to the flow. A transonic solver must handle both types in one domain.

First-order systems $`\partial_t\mathbf{U} + \mathbf{A}\,\partial_x\mathbf{U} = 0`$ are hyperbolic when $\mathbf{A}$ has real eigenvalues and a complete set of eigenvectors; the eigenvalues are the characteristic speeds. The Euler equations are hyperbolic in time.

### What the Type Means for Boundary Conditions and Solution Strategy

| Type | Domain of dependence | Conditions needed | Solution strategy | Examples in CFD |
| --- | --- | --- | --- | --- |
| Elliptic | Every point depends on the whole boundary; a local change is felt everywhere | One condition on every part of a closed boundary (Dirichlet, Neumann or Robin) | Solve for all unknowns simultaneously, usually iteratively; no marching | Steady diffusion, pressure Poisson equation, subsonic potential flow, steady incompressible Navier–Stokes |
| Parabolic | Depends on the past (or upstream) and instantaneously on the whole cross-section | Initial condition plus conditions on the lateral boundaries; none at the final time | March in time (or in the streamwise direction), solving a lower-dimensional problem at each step | Unsteady heat conduction, boundary-layer equations marched downstream, parabolized Navier–Stokes |
| Hyperbolic | Finite region bounded by characteristics; finite propagation speed | Initial data plus conditions only where characteristics enter the domain | March in time with upwind-biased schemes and a CFL time-step limit | Euler equations, acoustics, steady supersonic flow marched in $x$ |

The full Navier–Stokes equations are of mixed type. Unsteady compressible flow is hyperbolic in its inviscid part and parabolic in its viscous part. Steady subsonic flow behaves elliptically, because pressure waves travel upstream. Incompressible flow combines a parabolic momentum equation with the elliptic pressure constraint, so even a time-marching incompressible solver must solve an elliptic problem at every step. Imposing too few boundary conditions leaves the problem without a unique solution; imposing too many over-determines it and produces spurious reflections or a solution that ignores some of the conditions. The details for each boundary type are in [Boundary Conditions](./boundary_conditions.md).

## Key Takeaways

- The finite-volume method discretizes the integral conservation law $`\frac{d}{dt}\int_V\mathbf{U}\,dV + \oint_A(\mathbf{F}_c - \mathbf{F}_v)\cdot\mathbf{n}\,dA = \int_V\mathbf{S}\,dV`$ cell by cell, so interior fluxes cancel and the scheme conserves exactly.
- Conservative schemes converge to weak solutions with the correct shock jump conditions (Lax–Wendroff); non-conservative ones may not.
- In incompressible flow, pressure is the Lagrange multiplier of the divergence constraint, satisfies an elliptic Poisson equation, and leads to a saddle-point system that needs special coupling algorithms.
- One generic transport equation covers momentum, energy, species and turbulence quantities.
- $Re$, $Ma$, $Pe$ and the cell Péclet number decide the convection scheme, the pressure treatment and the required resolution.
- The PDE type (elliptic, parabolic, hyperbolic) decides how many boundary conditions are needed, where, and whether the solution can be marched.

## Related Scripts

- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Supersonic Forward-Facing Step](../../../scripts/simulations/supersonic_forward_facing_step/): solves the 2D compressible Euler equations for a Mach 3 stream that meets a forward-facing step in a wind tunnel, the benchmark of Woodward and Colella (1984), and animates the shock pattern that forms.
- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and animates the temperature field with Matplotlib.

## Exercises

**Exercise 1.** Check whether each 2D velocity field satisfies the incompressible continuity equation $\nabla\cdot\mathbf{u} = 0$: (a) $\mathbf{u} = (x^2, -2xy)$; (b) $\mathbf{u} = (x^2, xy)$.

<details>
<summary>Answer</summary>

(a) $\partial u/\partial x + \partial v/\partial y = 2x - 2x = 0$, so the field is divergence-free.

(b) $2x + x = 3x \neq 0$, so the field is not divergence-free. It could only describe a flow in which the density changes, as allowed by $\partial\rho/\partial t + \nabla\cdot(\rho\mathbf{u}) = 0$.

</details>

**Exercise 2.** A steady flow enters a nozzle with $\rho_1 = 1.2$ kg/m³, $A_1 = 0.05$ m² and $V_1 = 10$ m/s, and leaves through $A_2 = 0.02$ m² with $\rho_2 = 1.5$ kg/m³. Use the integral mass equation to find $V_2$.

<details>
<summary>Answer</summary>

In steady flow the volume integral does not change, so $`\oint_A \rho\mathbf{u}\cdot\mathbf{n}\,dA = 0`$. With $\mathbf{n}$ pointing outward, the inlet contributes $-\rho_1 V_1 A_1$ and the outlet $+\rho_2 V_2 A_2$:

```math
V_2 = \frac{\rho_1 V_1 A_1}{\rho_2 A_2} = \frac{1.2 \times 10 \times 0.05}{1.5 \times 0.02} = 20 \text{ m/s}
```

with a mass flow rate of 0.6 kg/s. A finite-volume scheme enforces exactly this balance for every cell.

</details>

**Exercise 3.** Classify the linearized potential equation $(1 - Ma^2)\phi_{xx} + \phi_{yy} = 0$ for $Ma = 0.5$ and $Ma = 2$. For $Ma = 2$, find the slopes of the characteristics and the angle they make with the $x$ axis, and say which boundary conditions a solver marching in $x$ needs.

<details>
<summary>Answer</summary>

$a = 1 - Ma^2$, $b = 0$, $c = 1$, so $b^2 - 4ac = -4(1 - Ma^2)$.

$Ma = 0.5$: $-4 \times 0.75 = -3 < 0$, elliptic. A disturbance is felt everywhere, and conditions are needed on the whole boundary, including far upstream and downstream.

$Ma = 2$: $-4 \times (-3) = 12 > 0$, hyperbolic. The characteristics satisfy $dy/dx = \pm\sqrt{12}/(2 \times (-3)) = \mp 1/\sqrt{3} \approx \mp 0.577$, at $30^\circ$ to the flow, which is the Mach angle $\arcsin(1/2)$. A disturbance affects only the region between the downstream Mach lines, so the solution can be marched in $x$ from inflow data ($\phi$ and $\phi_x$ on an upstream line) with conditions on the lateral boundaries; no condition is imposed at the outflow.

</details>

**Exercise 4.** Water ($\nu = 10^{-6}$ m²/s, $Pr = 7$) flows at $U = 1$ m/s in a pipe of diameter $D = 0.05$ m. Compute $Re$, the thermal diffusivity $\alpha$ and $Pe$. A first mesh has cells of 1 mm across the pipe. Compute the cell Péclet number for the temperature equation based on $U$ and say what this implies for the convection scheme.

<details>
<summary>Answer</summary>

$Re = 1 \times 0.05/10^{-6} = 5 \times 10^4$, turbulent.

$\alpha = \nu/Pr = 1.43 \times 10^{-7}$ m²/s and $`Pe = Re\,Pr = 3.5 \times 10^5`$.

$Pe_\Delta = U\Delta x/\alpha = 1 \times 10^{-3}/(1.43 \times 10^{-7}) = 7000$, far above 2. Central differencing of the convective term would produce oscillatory, unbounded temperatures; an upwind-biased or bounded high-resolution scheme is needed (see [Convection Schemes for Finite Volume Methods](../fvm/convection_schemes.md)). Reducing $Pe_\Delta$ to 2 would need cells of $0.3\ \mu\mathrm{m}$, which is impossible. In turbulent flow the effective diffusivity $\alpha + \alpha_t$ is larger, but the conclusion is unchanged away from the wall.

</details>

**Exercise 5.** For a Newtonian fluid with constant properties, the viscous stress is $\boldsymbol{\tau} = \mu(\nabla\mathbf{u} + \nabla\mathbf{u}^T) + (\mu_v - \tfrac{2}{3}\mu)(\nabla\cdot\mathbf{u})\mathbf{I}$ with bulk viscosity $\mu_v$. Show that $\nabla\cdot\boldsymbol{\tau} = \mu\nabla^2\mathbf{u} + (\tfrac{\mu}{3} + \mu_v)\nabla(\nabla\cdot\mathbf{u})$, and that it reduces to $\mu\nabla^2\mathbf{u}$ in incompressible flow.

<details>
<summary>Answer</summary>

Using $\nabla\cdot(\nabla\mathbf{u}) = \nabla^2\mathbf{u}$ and $\nabla\cdot(\nabla\mathbf{u}^T) = \nabla(\nabla\cdot\mathbf{u})$ for constant $\mu$:

```math
\nabla\cdot\boldsymbol{\tau} = \mu\nabla^2\mathbf{u} + \mu\nabla(\nabla\cdot\mathbf{u}) +
\left(\mu_v - \tfrac{2}{3}\mu\right)\nabla(\nabla\cdot\mathbf{u}) = \mu\nabla^2\mathbf{u} +
\left(\tfrac{\mu}{3} + \mu_v\right)\nabla(\nabla\cdot\mathbf{u})
```

For incompressible flow $\nabla\cdot\mathbf{u} = 0$, so only $\mu\nabla^2\mathbf{u}$ remains. This is why the incompressible momentum equation can use the Laplacian form, although a solver with variable viscosity (for example an eddy viscosity) must keep the full $\nabla\cdot\boldsymbol{\tau}$.

</details>

## References

- Hirsch, C., *Numerical Computation of Internal and External Flows, Volume 1: Fundamentals of Computational Fluid Dynamics*, 2nd ed., Butterworth-Heinemann, 2007.
- Ferziger, J. H., Perić, M., & Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- Patankar, S. V., *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
- LeVeque, R. J., *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002.
- Lax, P. D., & Wendroff, B., "Systems of conservation laws," *Communications on Pure and Applied Mathematics*, 13(2), 217–237, 1960.
- Gresho, P. M., & Sani, R. L., *Incompressible Flow and the Finite Element Method*, Wiley, 1998.
- White, F. M., *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- Anderson, J. D., *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
