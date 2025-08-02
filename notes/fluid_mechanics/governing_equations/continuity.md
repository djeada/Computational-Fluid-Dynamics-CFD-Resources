# Continuity Equation

The continuity equation represents the **conservation of mass** in fluid flow. It is one of the fundamental governing equations of fluid mechanics and states that mass cannot be created or destroyed within a fluid system.

## Physical Principle

The continuity equation is based on the principle that the rate of mass accumulation within a control volume equals the net rate of mass flow into that volume. Mathematically, this is expressed as:

**Mass accumulation = Mass inflow - Mass outflow**

## Derivation

### Control Volume Approach

Consider a fixed control volume $V$ bounded by surface $S$. The mass within the volume is:

$$M = \int_V \rho \, dV$$

The rate of change of mass within the volume is:

$$\frac{dM}{dt} = \frac{d}{dt}\int_V \rho \, dV = \int_V \frac{\partial \rho}{\partial t} \, dV$$

The net mass flow rate into the volume through the surface is:

$$\text{Net inflow} = -\int_S \rho \vec{v} \cdot \vec{n} \, dS$$

where $\vec{n}$ is the outward unit normal vector.

### Conservation Statement

For mass conservation:
$$\int_V \frac{\partial \rho}{\partial t} \, dV + \int_S \rho \vec{v} \cdot \vec{n} \, dS = 0$$

Using the divergence theorem:
$$\int_S \rho \vec{v} \cdot \vec{n} \, dS = \int_V \nabla \cdot (\rho \vec{v}) \, dV$$

Therefore:
$$\int_V \left[\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v})\right] dV = 0$$

Since this must hold for any arbitrary volume $V$, the integrand must be zero:

## General Continuity Equation

$$\boxed{\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0}$$

This is the **general form** of the continuity equation, valid for both compressible and incompressible flows.

## Expanded Forms

### Cartesian Coordinates

In three-dimensional Cartesian coordinates:

$$\frac{\partial \rho}{\partial t} + \frac{\partial (\rho u)}{\partial x} + \frac{\partial (\rho v)}{\partial y} + \frac{\partial (\rho w)}{\partial z} = 0$$

where $u$, $v$, and $w$ are the velocity components in the $x$, $y$, and $z$ directions, respectively.

### Cylindrical Coordinates

In cylindrical coordinates $(r, \theta, z)$:

$$\frac{\partial \rho}{\partial t} + \frac{1}{r}\frac{\partial}{\partial r}(r \rho v_r) + \frac{1}{r}\frac{\partial (\rho v_\theta)}{\partial \theta} + \frac{\partial (\rho v_z)}{\partial z} = 0$$

### Spherical Coordinates

In spherical coordinates $(r, \theta, \phi)$:

$$\frac{\partial \rho}{\partial t} + \frac{1}{r^2}\frac{\partial}{\partial r}(r^2 \rho v_r) + \frac{1}{r\sin\theta}\frac{\partial}{\partial \theta}(\sin\theta \rho v_\theta) + \frac{1}{r\sin\theta}\frac{\partial (\rho v_\phi)}{\partial \phi} = 0$$

## Special Cases

### Incompressible Flow

For **incompressible flow**, density is constant ($\rho = $ constant), so:

$$\frac{\partial \rho}{\partial t} = 0 \quad \text{and} \quad \nabla \rho = 0$$

The continuity equation simplifies to:

$$\boxed{\nabla \cdot \vec{v} = 0}$$

In Cartesian coordinates:
$$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} + \frac{\partial w}{\partial z} = 0$$

This states that the **volumetric flow rate** is conserved in incompressible flow.

### Steady Flow

For **steady flow** ($\frac{\partial}{\partial t} = 0$):

$$\nabla \cdot (\rho \vec{v}) = 0$$

### One-Dimensional Flow

For **one-dimensional flow** in a variable area duct:

$$\frac{\partial \rho}{\partial t} + \frac{\partial (\rho u)}{\partial x} = 0$$

For steady, one-dimensional flow:
$$\frac{d(\rho u A)}{dx} = 0$$

where $A(x)$ is the cross-sectional area. This gives:
$$\rho u A = \text{constant} = \dot{m}$$

where $\dot{m}$ is the mass flow rate.

## Physical Interpretation

### Mass Flow Rate

The **mass flow rate** through a surface $S$ is:
$$\dot{m} = \int_S \rho \vec{v} \cdot \vec{n} \, dS$$

For incompressible flow through a pipe with uniform velocity:
$$\dot{m} = \rho V A$$

where $V$ is the average velocity and $A$ is the cross-sectional area.

### Volume Flow Rate

For incompressible flow, the **volume flow rate** (or discharge) is:
$$Q = \int_S \vec{v} \cdot \vec{n} \, dS = VA$$

### Stream Function

For two-dimensional incompressible flow, the continuity equation is automatically satisfied by introducing a **stream function** $\psi$ such that:

$$u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}$$

## Material Derivative Form

Using the material derivative, the continuity equation can be written as:

$$\frac{D\rho}{Dt} + \rho \nabla \cdot \vec{v} = 0$$

where $\frac{D}{Dt} = \frac{\partial}{\partial t} + \vec{v} \cdot \nabla$ is the material derivative.

This form shows that the density of a fluid particle changes due to the divergence of the velocity field.

## Applications

### Pipe Flow

For steady flow in a pipe with varying diameter:
$$\rho_1 V_1 A_1 = \rho_2 V_2 A_2$$

For incompressible flow:
$$V_1 A_1 = V_2 A_2$$

This explains why water speeds up when flowing through a nozzle.

### Channel Flow

For steady, incompressible flow in an open channel:
$$Q = VA = \text{constant}$$

### Compressible Flow in Nozzles

For steady, one-dimensional compressible flow:
$$\rho u A = \text{constant}$$

Combined with other equations, this leads to important relationships for nozzle design.

## Boundary Conditions

### Solid Boundaries

At solid walls, the **no-penetration condition** requires:
$$\vec{v} \cdot \vec{n} = 0$$

This means no flow through solid boundaries.

### Inflow/Outflow Boundaries

- **Inflow**: Specify velocity or mass flow rate
- **Outflow**: Often use zero-gradient condition: $\frac{\partial \vec{v}}{\partial n} = 0$

## Numerical Implementation

In computational fluid dynamics, the continuity equation is typically discretized using:

### Finite Volume Method
$$\frac{\partial}{\partial t}\int_V \rho \, dV + \sum_{\text{faces}} (\rho \vec{v} \cdot \vec{n} A)_f = 0$$

### Finite Difference Method
Central differences for spatial derivatives and forward/backward differences for time derivatives.

## Common Mistakes

1. **Confusing mass and volume conservation**: For compressible flow, mass is conserved, not volume
2. **Incorrect boundary conditions**: Forgetting no-penetration at walls
3. **Dimensional inconsistency**: Mixing different units for density and velocity
4. **Steady vs. unsteady**: Incorrectly dropping time derivative terms

## Relationship to Other Equations

The continuity equation is **coupled** with:
- **Momentum equations**: Velocity appears in both
- **Energy equation**: Density and velocity affect energy transport
- **Equation of state**: Relates density to pressure and temperature

## Historical Notes

- **1757**: Euler first formulated the continuity equation
- **1822**: Navier included viscous effects in momentum equations
- **1845**: Stokes provided rigorous mathematical foundation

The continuity equation remains fundamental to all fluid flow analysis and is essential for understanding more complex phenomena in fluid mechanics.
