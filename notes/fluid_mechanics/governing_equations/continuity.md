# Continuity Equation

The continuity equation represents the **conservation of mass** in fluid flow. It is one of the fundamental governing equations of fluid mechanics and states that mass cannot be created or destroyed within a fluid system.

## Physical Principle

The continuity equation is based on the principle that the rate of mass accumulation within a control volume equals the net rate of mass flow into that volume. Mathematically, this is expressed as:

**Mass accumulation = Mass inflow - Mass outflow**

## Derivation

### Control Volume Approach

Consider a fixed control volume $V$ bounded by surface $S$. The mass within the volume is:

```math
M = \int_V \rho \, dV
```

The rate of change of mass within the volume is:

```math
\frac{dM}{dt} = \frac{d}{dt}\int_V \rho \, dV = \int_V \frac{\partial \rho}{\partial t}
\, dV
```

The net mass flow rate into the volume through the surface is:

```math
\text{Net inflow} = -\int_S \rho \vec{v} \cdot \vec{n} \, dS
```

where $\vec{n}$ is the outward unit normal vector.

### Conservation Statement

For mass conservation:

```math
\int_V \frac{\partial \rho}{\partial t} \, dV + \int_S \rho \vec{v} \cdot \vec{n} \,
dS = 0
```

Using the divergence theorem:

```math
\int_S \rho \vec{v} \cdot \vec{n} \, dS = \int_V \nabla \cdot (\rho \vec{v}) \, dV
```

Therefore:

$$
\int_V \left[\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v})\right]
dV = 0
$$

Since this must hold for any arbitrary volume $V$, the integrand must be zero:

## General Continuity Equation

$$
\boxed{\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0}
$$

This is the **general form** of the continuity equation, valid for both compressible and incompressible flows.

## Expanded Forms

### Cartesian Coordinates

In three-dimensional Cartesian coordinates:

$$
\frac{\partial \rho}{\partial t} + \frac{\partial (\rho u)}{\partial x} +
\frac{\partial (\rho v)}{\partial y} + \frac{\partial (\rho w)}{\partial z} = 0
$$

where $u$, $v$, and $w$ are the velocity components in the $x$, $y$, and $z$ directions, respectively.

### Cylindrical Coordinates

In cylindrical coordinates $(r, \theta, z)$:

$$
\frac{\partial \rho}{\partial t} + \frac{1}{r} \frac{\partial}{\partial r}(r \rho v_r) +
\frac{1}{r} \frac{\partial (\rho v_\theta)}{\partial \theta} +
\frac{\partial (\rho v_z)}{\partial z} = 0
$$

### Spherical Coordinates

In spherical coordinates $(r, \theta, \phi)$:

$$
\frac{\partial \rho}{\partial t} + \frac{1}{r^2}
\frac{\partial}{\partial r}(r^2 \rho v_r) + \frac{1}{r\sin\theta}
\frac{\partial}{\partial \theta}(\sin\theta \rho v_\theta) + \frac{1}{r\sin\theta}
\frac{\partial (\rho v_\phi)}{\partial \phi} = 0
$$

## Special Cases

### Incompressible Flow

For **incompressible flow**, density is constant ($\rho = \text{constant}$), so:

$$
\frac{\partial \rho}{\partial t} = 0 \quad \text{and} \quad \nabla \rho = 0
$$

The continuity equation simplifies to:

$$
\boxed{\nabla \cdot \vec{v} = 0}
$$

In Cartesian coordinates:

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} +
\frac{\partial w}{\partial z} = 0
$$

This states that the **volumetric flow rate** is conserved in incompressible flow.

### Steady Flow

For **steady flow** ($\frac{\partial}{\partial t} = 0$):

$$
\nabla \cdot (\rho \vec{v}) = 0
$$

### One-Dimensional Flow

For **one-dimensional flow** in a variable area duct:

$$
\frac{\partial \rho}{\partial t} + \frac{\partial (\rho u)}{\partial x} = 0
$$

For steady, one-dimensional flow:

$$
\frac{d(\rho u A)}{dx} = 0
$$

where $A(x)$ is the cross-sectional area. This gives:

$$
\rho u A = \text{constant} = \dot{m}
$$

where $\dot{m}$ is the mass flow rate.

## Physical Interpretation

### Mass Flow Rate

The **mass flow rate** through a surface $S$ is:

```math
\dot{m} = \int_S \rho \vec{v} \cdot \vec{n} \, dS
```

For incompressible flow through a pipe with uniform velocity:

$$
\dot{m} = \rho V A
$$

where $V$ is the average velocity and $A$ is the cross-sectional area.

### Volume Flow Rate

For incompressible flow, the **volume flow rate** (or discharge) is:

```math
Q = \int_S \vec{v} \cdot \vec{n} \, dS = VA
```

### Stream Function

For two-dimensional incompressible flow, the continuity equation is automatically satisfied by introducing a **stream function** $\psi$ such that:

$$
u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}
$$

## Material Derivative Form

Using the material derivative, the continuity equation can be written as:

$$
\frac{D\rho}{Dt} + \rho \nabla \cdot \vec{v} = 0
$$

where $\frac{D}{Dt} = \frac{\partial}{\partial t} + \vec{v} \cdot \nabla$ is the material derivative.

This form shows that the density of a fluid particle changes due to the divergence of the velocity field.

## Applications

### Pipe Flow

For steady flow in a pipe with varying diameter:

$$
\rho_1 V_1 A_1 = \rho_2 V_2 A_2
$$

For incompressible flow:

$$
V_1 A_1 = V_2 A_2
$$

This explains why water speeds up when flowing through a nozzle.

### Channel Flow

For steady, incompressible flow in an open channel:

$$
Q = VA = \text{constant}
$$

### Compressible Flow in Nozzles

For steady, one-dimensional compressible flow:

$$
\rho u A = \text{constant}
$$

Combined with other equations, this leads to important relationships for nozzle design.

## Boundary Conditions

### Solid Boundaries

At solid walls, the **no-penetration condition** requires:

$$
\vec{v} \cdot \vec{n} = 0
$$

This means no flow through solid boundaries.

### Inflow/Outflow Boundaries

- **Inflow**: Specify velocity or mass flow rate
- **Outflow**: Often use zero-gradient condition: $\frac{\partial \vec{v}}{\partial n} = 0$

## Numerical Implementation

In computational fluid dynamics, the continuity equation is typically discretized using:

### Finite Volume Method

```math
\frac{\partial}{\partial t}\int_V \rho \, dV + \sum_{\text{faces}}
(\rho \vec{v} \cdot \vec{n} A)_f = 0
```

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

## Related Scripts

- [Compressible vs. Incompressible Duct Flow](../../../scripts/plots/compressible_vs_incompressible/): draws prescribed incompressible and compressible velocity fields in a 2D duct side by side, so the constant downstream profile of the first can be compared with the accelerating profile of the second.
- [Converging-Diverging Nozzle Flow](../../../scripts/plots/nozzle_flow/): plots quasi-one-dimensional isentropic flow through a converging-diverging (de Laval) nozzle, with streamlines coloured by Mach number.
- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib.
- [Flow Rate Through a Circular Pipe](../../../scripts/plots/flow_rate_pipe/): computes the volumetric flow rate $Q = \pi r^2 v$ of a circular pipe and draws a labelled side view of the pipe with flow arrows.
- [Microscopic vs. Macroscopic View of a Fluid](../../../scripts/plots/microscopic_view/): draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid.

## Exercises

**Exercise 1.** Water ($\rho = 998$ kg/m³) flows at $V_1 = 2$ m/s in a pipe of diameter $D_1 = 0.1$ m that contracts to a nozzle of diameter $D_2 = 0.04$ m. Find $V_2$, the volume flow rate and the mass flow rate.

<details>
<summary>Answer</summary>

- $V_2 = V_1 (D_1/D_2)^2 = 2 \times 6.25 = 12.5$ m/s.
- $Q = \frac{\pi}{4}D_1^2 V_1 = 0.01571$ m³/s.
- $\dot{m} = \rho Q = 15.7$ kg/s.

</details>

**Exercise 2.** Show that the two-dimensional field $u = 3x + y$, $v = 2x - 3y$ satisfies the incompressible continuity equation, and find its stream function $\psi$.

<details>
<summary>Answer</summary>

$\partial u/\partial x + \partial v/\partial y = 3 - 3 = 0$.

From $u = \partial\psi/\partial y = 3x + y$: $\psi = 3xy + y^2/2 + f(x)$.

From $v = -\partial\psi/\partial x = -(3y + f'(x)) = 2x - 3y$: $f'(x) = -2x$, so $f = -x^2$.

The stream function is $\psi = 3xy + \frac{1}{2}y^2 - x^2$, up to a constant.

</details>

**Exercise 3.** A steady, incompressible, two-dimensional flow is purely radial, $`\vec{v} = v_r(r)\,\hat{e}_r`$. Use the cylindrical form of the continuity equation to find $v_r(r)$, and relate the constant to the volume flow rate $Q$ per unit depth leaving a circle of radius $r$.

<details>
<summary>Answer</summary>

With $\rho$ constant and only $v_r(r)$ nonzero, $\frac{1}{r}\frac{d}{dr}(r v_r) = 0$, so $r v_r = C$ and $v_r = C/r$.

The flow rate through a circle is $`Q = \oint v_r \, r\,d\theta = 2\pi C`$, so

```math
v_r = \frac{Q}{2\pi r}
```

This is the potential-flow line source. The velocity is singular at $r = 0$, where the source sits.

</details>

**Exercise 4.** Gas fills a cylinder of length $L(t)$ closed at $x = 0$ and compressed by a piston moving at speed $V_p$, so $dL/dt = -V_p$. Assume the velocity varies linearly, $u = -V_p x/L$, and the density is uniform. (a) Use the one-dimensional continuity equation to show that $\rho L$ stays constant. (b) For $L_0 = 0.2$ m, $\rho_0 = 1.2$ kg/m³ and $V_p = 0.5$ m/s, find $\rho$ and $d\rho/dt$ when $L = 0.1$ m.

<details>
<summary>Answer</summary>

(a) Since $\partial\rho/\partial x = 0$, continuity gives $`d\rho/dt + \rho\,\partial u/\partial x = 0`$. With $\partial u/\partial x = -V_p/L$, this becomes $`d\rho/dt = \rho V_p/L = -\rho\,(dL/dt)/L`$. Therefore $d(\ln\rho + \ln L)/dt = 0$ and $\rho L$ is constant, which is just the statement that the mass per unit piston area is fixed.

(b) $\rho = \rho_0 L_0/L = 1.2 \times 0.2/0.1 = 2.4$ kg/m³, and $d\rho/dt = \rho V_p/L = 2.4 \times 0.5/0.1 = 12$ kg/(m³ s).

</details>

## References

- G. K. Batchelor, *An Introduction to Fluid Dynamics*, Cambridge University Press, 1967.
- P. K. Kundu, I. M. Cohen, D. R. Dowling, *Fluid Mechanics*, 6th ed., Academic Press, 2016.
- R. Aris, *Vectors, Tensors, and the Basic Equations of Fluid Mechanics*, Prentice-Hall, 1962.
