# Navier-Stokes Equations

The Navier-Stokes equations describe the **conservation of momentum** in fluid flow and are among the most important equations in fluid mechanics. They represent Newton's second law applied to fluid motion, accounting for pressure forces, viscous forces, and body forces.

## Physical Principle

The Navier-Stokes equations are based on the principle that the rate of change of momentum of a fluid particle equals the sum of all forces acting on it:

**Rate of momentum change = Pressure forces + Viscous forces + Body forces**

## General Form

The general form of the Navier-Stokes equations for a Newtonian fluid is:

$$\boxed{\rho \frac{D\vec{v}}{Dt} = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \vec{f}}$$

where:
- $\rho$ = fluid density
- $\vec{v}$ = velocity vector
- $\frac{D}{Dt}$ = material derivative
- $p$ = pressure
- $\boldsymbol{\tau}$ = viscous stress tensor
- $\vec{f}$ = body force per unit mass (e.g., gravity)

## Material Derivative

The material derivative represents the total rate of change following a fluid particle:

$$\frac{D\vec{v}}{Dt} = \frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v}$$

This includes:
- **Local acceleration**: $\frac{\partial \vec{v}}{\partial t}$ (time-dependent changes)
- **Convective acceleration**: $(\vec{v} \cdot \nabla)\vec{v}$ (spatial changes due to particle motion)

## Viscous Stress Tensor

For a **Newtonian fluid**, the viscous stress tensor is:

$$\boldsymbol{\tau} = \mu \left[\nabla \vec{v} + (\nabla \vec{v})^T\right] + \lambda (\nabla \cdot \vec{v})\boldsymbol{I}$$

where:
- $\mu$ = dynamic viscosity
- $\lambda$ = bulk viscosity (often $\lambda = -\frac{2}{3}\mu$)
- $\boldsymbol{I}$ = identity tensor

For incompressible flow ($\nabla \cdot \vec{v} = 0$), this simplifies to:

$$\boldsymbol{\tau} = \mu \left[\nabla \vec{v} + (\nabla \vec{v})^T\right]$$

## Incompressible Form

For **incompressible flow** with constant density and viscosity:

$$\boxed{\rho \left(\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v}\right) = -\nabla p + \mu \nabla^2 \vec{v} + \rho \vec{f}}$$

This can be written in terms of kinematic viscosity $\nu = \mu/\rho$:

$$\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \vec{v} + \vec{f}$$

## Component Forms

### Cartesian Coordinates

In Cartesian coordinates $(x, y, z)$ with velocity components $(u, v, w)$:

**x-momentum:**
$$\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} + w\frac{\partial u}{\partial z} = -\frac{1}{\rho}\frac{\partial p}{\partial x} + \nu\nabla^2 u + f_x$$

**y-momentum:**
$$\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} + w\frac{\partial v}{\partial z} = -\frac{1}{\rho}\frac{\partial p}{\partial y} + \nu\nabla^2 v + f_y$$

**z-momentum:**
$$\frac{\partial w}{\partial t} + u\frac{\partial w}{\partial x} + v\frac{\partial w}{\partial y} + w\frac{\partial w}{\partial z} = -\frac{1}{\rho}\frac{\partial p}{\partial z} + \nu\nabla^2 w + f_z$$

where $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2}$ is the Laplacian operator.

### Cylindrical Coordinates

In cylindrical coordinates $(r, \theta, z)$:

**r-momentum:**
$$\frac{\partial v_r}{\partial t} + v_r\frac{\partial v_r}{\partial r} + \frac{v_\theta}{r}\frac{\partial v_r}{\partial \theta} + v_z\frac{\partial v_r}{\partial z} - \frac{v_\theta^2}{r} = -\frac{1}{\rho}\frac{\partial p}{\partial r} + \nu\left(\nabla^2 v_r - \frac{v_r}{r^2} - \frac{2}{r^2}\frac{\partial v_\theta}{\partial \theta}\right) + f_r$$

**θ-momentum:**
$$\frac{\partial v_\theta}{\partial t} + v_r\frac{\partial v_\theta}{\partial r} + \frac{v_\theta}{r}\frac{\partial v_\theta}{\partial \theta} + v_z\frac{\partial v_\theta}{\partial z} + \frac{v_r v_\theta}{r} = -\frac{1}{\rho r}\frac{\partial p}{\partial \theta} + \nu\left(\nabla^2 v_\theta - \frac{v_\theta}{r^2} + \frac{2}{r^2}\frac{\partial v_r}{\partial \theta}\right) + f_\theta$$

**z-momentum:**
$$\frac{\partial v_z}{\partial t} + v_r\frac{\partial v_z}{\partial r} + \frac{v_\theta}{r}\frac{\partial v_z}{\partial \theta} + v_z\frac{\partial v_z}{\partial z} = -\frac{1}{\rho}\frac{\partial p}{\partial z} + \nu\nabla^2 v_z + f_z$$

## Special Cases

### Euler Equations (Inviscid Flow)

For **inviscid flow** ($\mu = 0$):

$$\frac{\partial \vec{v}}{\partial t} + (\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \vec{f}$$

### Stokes Equations (Creeping Flow)

For **very low Reynolds number flow** (inertial terms negligible):

$$0 = -\nabla p + \mu \nabla^2 \vec{v} + \rho \vec{f}$$

This is linear in velocity and much easier to solve.

### Steady Flow

For **steady flow** ($\frac{\partial}{\partial t} = 0$):

$$(\vec{v} \cdot \nabla)\vec{v} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \vec{v} + \vec{f}$$

## Dimensionless Form

The equations are often non-dimensionalized using characteristic scales:
- Length scale: $L$
- Velocity scale: $U$
- Time scale: $T = L/U$
- Pressure scale: $\rho U^2$

This introduces the **Reynolds number**:

$$Re = \frac{\rho U L}{\mu} = \frac{UL}{\nu}$$

The dimensionless Navier-Stokes equations become:

$$\frac{\partial \vec{v}^*}{\partial t^*} + (\vec{v}^* \cdot \nabla^*)\vec{v}^* = -\nabla^* p^* + \frac{1}{Re}\nabla^{*2} \vec{v}^* + \frac{1}{Fr^2}\vec{g}^*$$

where asterisks denote dimensionless variables and $Fr = U/\sqrt{gL}$ is the Froude number.

## Physical Terms

### Pressure Force

$$-\nabla p$$

- Represents force due to pressure gradients
- Always points from high to low pressure
- Normal to isobars (constant pressure lines)

### Viscous Force

$$\nabla \cdot \boldsymbol{\tau} = \mu \nabla^2 \vec{v}$$ (for incompressible flow)

- Represents internal friction effects
- Tends to smooth out velocity gradients
- Proportional to second derivatives of velocity

### Convective Acceleration

$$(\vec{v} \cdot \nabla)\vec{v}$$

- Represents acceleration due to spatial velocity changes
- **Nonlinear term** that makes the equations complex
- Responsible for many interesting flow phenomena

### Body Forces

$$\rho \vec{f}$$

- External forces acting on fluid volume
- Most common: gravity ($\vec{f} = \vec{g}$)
- Can include electromagnetic forces, centrifugal forces, etc.

## Boundary Conditions

### No-Slip Condition

At solid walls:
$$\vec{v} = \vec{v}_{wall}$$

For stationary walls: $\vec{v} = 0$

### Free-Slip Condition

At free surfaces or symmetry planes:
$$\vec{v} \cdot \vec{n} = 0, \quad \frac{\partial v_t}{\partial n} = 0$$

where $v_t$ is tangential velocity and $n$ is normal direction.

### Inflow/Outflow Conditions

- **Inflow**: Specify velocity profile or pressure
- **Outflow**: Often use zero-gradient conditions

## Exact Solutions

Several exact solutions exist for simplified geometries:

### Couette Flow

Flow between parallel plates, one moving:
$$u(y) = \frac{U y}{h}$$

where $U$ is the plate velocity and $h$ is the gap height.

### Poiseuille Flow

Pressure-driven flow in a circular pipe:
$$u(r) = \frac{\Delta p}{4\mu L}(R^2 - r^2)$$

where $\Delta p$ is pressure drop, $L$ is pipe length, and $R$ is pipe radius.

### Stagnation Point Flow

Flow near a stagnation point:
$$u = ax, \quad v = -ay$$

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
