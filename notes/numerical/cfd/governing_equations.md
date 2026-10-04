# Governing Equations in Fluid Dynamics

In fluid dynamics, the behavior of fluid flows is described by a set of governing equations. These equations are derived from fundamental principles of physics, including conservation of mass, momentum, and energy. The primary governing equations are the Continuity Equation, the Navier-Stokes Equations, and the Energy Equation.

## Continuity Equation

The Continuity Equation represents the conservation of mass in a fluid flow. It states that the rate of change of mass in a control volume is equal to the net mass flux across its boundaries.

### Continuity Equation (General Form)

For a compressible fluid:

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0
$$

Where:

- $ \\rho $ is the fluid density,
- $ \\vec{v} $ is the fluid velocity vector,
- $ t $ is time.

For an incompressible fluid ($ \\rho $ is constant):

$$
\nabla \cdot \vec{v} = 0
$$

### Explanation

- The first term, $ \\frac{\\partial \\rho}{\\partial t} $, represents the local rate of change of density.
- The second term, $ \\nabla \\cdot (\\rho \\vec{v}) $, represents the convective rate of change of density due to fluid motion.

## Navier-Stokes Equations

The Navier-Stokes Equations describe the conservation of momentum in fluid flows. They are derived from Newton's second law and account for the forces acting on a fluid element.

### Navier-Stokes Equations (General Form)

For a compressible fluid:

$$
\rho
\left(\frac{\partial \vec{v}}{\partial t} + \vec{v} \cdot \nabla \vec{v}
\right) = -\nabla p + \mu \nabla^2 \vec{v} + \left(\frac{\mu}{3} + \mu_v \right) \nabla
(\nabla \cdot \vec{v}) + \vec{f}
$$

Where:

- $ \\vec{v} $ is the fluid velocity vector,
- $ p $ is the pressure,
- $ \\mu $ is the dynamic viscosity,
- $ \\mu_v $ is the bulk viscosity,
- $ \\vec{f} $ represents body forces (e.g., gravity).

For an incompressible fluid:

$$
\rho
\left(\frac{\partial \vec{v}}{\partial t} + \vec{v} \cdot \nabla \vec{v}
\right) = -\nabla p + \mu \nabla^2 \vec{v} + \vec{f}
$$

### Explanation

- The left side of the equation represents the rate of change of momentum.
- The right side includes pressure forces, viscous forces, and body forces.

## Energy Equation

The Energy Equation describes the conservation of energy in a fluid flow. It accounts for the internal energy, kinetic energy, and heat transfer within the fluid.

### Energy Equation (General Form)

For a compressible fluid:

$$
\frac{\partial}{\partial t} \left(\rho e \right) + \nabla \cdot
\left(\rho e \vec{v} \right) = -p (\nabla \cdot \vec{v}) + \nabla \cdot (k \nabla T) +
\Phi
$$

Where:

- $ e $ is the internal energy per unit mass (this form, with $-p(\nabla \cdot \vec{v})$ on the right, is the internal-energy equation),
- $ k $ is the thermal conductivity,
- $ T $ is the temperature,
- $ \\Phi $ represents viscous dissipation.

For an incompressible fluid (simplified form):

$$
\rho c_p \left(\frac{\partial T}{\partial t} + \vec{v} \cdot \nabla T \right) = k
\nabla^2 T + \Phi
$$

Where:

- $ c_p $ is the specific heat at constant pressure.

### Explanation

- The left side represents the rate of change of internal energy (local change plus convection).
- The right side includes work done by pressure forces, heat conduction, and viscous dissipation.

## Reynolds Transport Theorem

- defined through Reynolds transport theorem

- RTT relates lagrangian system to eulerian control volume

- The RTT connects a Lagrangian system with an Eulerian control volume.

  - By Lagrangian system, we mean a system of a given specified mass, or a *marked mass*.

- Conservation laws are written in terms of Lagrangian systems, but we solve CFD problems on Eulerian domains. The RTT connects these.

- The RTT is written as

$$
\frac{dB_{\text{sys}}}{dt} = \frac{d}{dt}\int_V \rho\beta dV + \int_A
\rho\beta\vec{v}\cdot\vec{n} dA
$$

- $B_{sys}$ is some extensive quantity, like mass, momentum, or energy.
- $\beta = B_{sys}/m$ is intensive.
- $\rho\beta$ will be mass, momentum, energy, etc. per unit volume.
- $\rho\beta\vec{v}$ is $B$-flux, like mass flux, momentum flux, energy flux.
- $\vec{n}$ is a unit normal vector pointing *out* of the surface of a control volume.
- In an area dA, $\rho\beta\vec{v}\cdot\vec{n}dA$ will be rate of B flowing out of a control volume through that area dA.

### Mass

- $B_{sys} = m$

- $\beta = B_{sys}/m = 1$.

- Lagrangian conservation law: mass is conserved, or the rate of change of a given mass is zero:

  ```math
  \frac{dm}{dt} = 0
  ```

- Substitute into the RTT and swap the right and left sides of the equality:

$$
\frac{d}{dt}\int_V\rho dV + \int_A\rho\vec{v}\cdot\vec{n}dA = 0
$$

### Momentum

- $B_{sys} = m\vec{v}$

- $\beta = B_{sys}/m = \vec{v}$

- Lagrangian conservation law: the rate of change of momentum of a fixed mass (system) is the sum of the external forces on the mass (system).

  - We have surface forces $\vec{F}$, and body forces (denoted with external field $\vec{g}$, nominally gravitational acceleration):

    ```math
    \frac{dm\vec{v}}{dt} = \int_A \vec{F}dA + \int_V\vec{g}\rho dV
    ```

  - Consider viscous and pressure forces, so that $\vec{F} = -\boldsymbol{\tau}\cdot\vec{n} - P\boldsymbol{\delta}\cdot{\vec{n}}$, where $\boldsymbol{\tau}$ is the viscous stress tensor, and $\boldsymbol{\delta}$ is the unit tensor.

    - (The negative sign is because $\vec{n}$ points *out* of the suface, and we want the force on or into the surface.)

  - This gives

    ```math
    \frac{dm\vec{v}}{dt} = -\int_A\boldsymbol{\tau}\cdot\vec{n}dA -
    \int_AP\boldsymbol{\delta}\cdot\vec{n}dA + \int_V\vec{g}\rho dV
    ```

- Substitute into the RTT and swap the right and left sides of the equality:

$$
\frac{d}{dt}\int_V\rho\vec{v}dV +
\int_A\rho\vec{v}\vec{v}\cdot\vec{n}dA = -\int_A\boldsymbol{\tau}\cdot\vec{n}dA -
\int_AP\boldsymbol{\delta}\cdot\vec{n}dA + \int_V\vec{g}\rho dV
$$

- Here, $\vec{v}\vec{v}$ is a tensor, and can be written as $\vec{v}\otimes\vec{v}$, or $v_iv_j$ in index notation.

### Energy

- $B_{sys} = E$ (where $E = mu + \frac{1}{2}m\vec{v}\cdot\vec{v}$ is internal + kinetic energy).

- $\beta = E/m = e$.

- Lagrangian conservation law: the rate of change of energy of a given mass is the sum of the heat transfered to the mass and the work performed on the mass:

  ```math
  \frac{dE}{dt} = -\int_A\vec{q}\cdot\vec{n}dA + \int_A\vec{F}\cdot\vec{v}dA +
  \int_V\rho\vec{g}\cdot\vec{v}dV
  ```

  - Here, $\vec{q}$ is the heat flux vector. As before, $\vec{F} = -\boldsymbol{\tau}\cdot\vec{n} - P\boldsymbol{\delta}\cdot{\vec{n}}$.
  - The symmetry of $\boldsymbol{\tau}$ and $\boldsymbol{\delta}$ let us write $\boldsymbol{\tau}\cdot\vec{n}\cdot\vec{v} = \boldsymbol{\tau}\cdot\vec{v}\cdot\vec{n}$ and $P\boldsymbol{\delta}\cdot\vec{n}\cdot\vec{v} = P\boldsymbol{\delta}\cdot\vec{v}\cdot\vec{n}$.

- Substitute into the RTT and swap the right and left sides of the equality:

$$
\frac{d}{dt}\int_V\rho edV + \int_A\rho
e\vec{v}\cdot\vec{n}dA = -\int_A\vec{q}\cdot\vec{n}dA -
\int_A(\boldsymbol{\tau}\cdot\vec{v})\cdot\vec{n}dA -
\int_A(P\boldsymbol{\delta}\cdot\vec{v})\cdot\vec{n}dA + \int_V\rho\vec{g}\cdot\vec{v}dV
$$

### Differential form

- The above equations are in integral form, which is convenient for a Finite Volume solution. (It is also convenient for derivation.)
- We can find the differential form as follows.
  - If the control volume is fixed in time, we can move $d/dt$ inside the volume integral.

  - Replace integrals over the surface area with volume integrals by applying the Gauss Divergence Theorem:

    ```math
    \int_A\vec{v}\cdot\vec{n}\, dA = \int_V \nabla\cdot\vec{v}\, dV
    ```

    where $\vec{v}$ is some vector (not necessarily velocity).

    - Hence, in the equation for mass we have $\int_A\rho\vec{v}\cdot\vec{n}dA = \int_V \nabla\cdot(\rho\vec{v})dV$.

  - Combine all the volume integrals into $\int_V(\text{all terms})dV = 0$. Since the volume integrated over is arbitrary, this equation can only be true if the integrand $(\text{all terms})$ itself is 0. This gives the final result. (Also, $ \\nabla\\cdot(P\\boldsymbol{\\delta}) = \\nabla P$.)

$$
\text{Mass Equation:} \quad \frac{\partial \rho}{\partial t} + \nabla \cdot
(\rho \mathbf{v}) = 0
$$

$$
\text{Momentum Equation:} \quad \frac{\partial (\rho \mathbf{v})}{\partial t} + \nabla
\cdot (\rho \mathbf{v} \mathbf{v}) = -\nabla \cdot \boldsymbol{\tau}
\text{ (viscous forces)} - \nabla P \text{ (pressure forces)} + \rho \mathbf{g}
\text{ (gravitational forces)}
$$

$$
\text{Energy Equation:} \quad \frac{\partial (\rho e)}{\partial t} + \nabla \cdot
(\rho e \mathbf{v}) = -\nabla \cdot \mathbf{q} \text{ (heat flux)} - \nabla \cdot
(\boldsymbol{\tau} \cdot \mathbf{v}) \text{ (viscous heating)} - \nabla \cdot
(P \mathbf{v}) \text{ (PV work)} + \rho \mathbf{g} \cdot \mathbf{v} \text{ (field work)}
$$

- The terms on the left hand side (LHS) of the equation are the accumulation and in/out transport through the control volume.
- The terms on the right hand side (RHS) are as noted. In the energy equation, field work will convert potential energy to kinetic energy (which is part of $e$).

## Purpose in CFD

This note presents the three governing equations of fluid dynamics—continuity, Navier–Stokes (momentum), and energy—in both integral and differential forms. The integral forms are derived via the Reynolds Transport Theorem (RTT) and are the starting point for Finite Volume discretization. The differential forms underpin Finite Difference and Finite Element methods. Every CFD solver is ultimately an approximate solution to these equations.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Fluid density $\rho$, velocity $\vec{v}$, pressure $p$, viscosity $\mu$, thermal conductivity $k$, specific heat $c_p$, body forces $\vec{f}$, heat sources $S$ |
| **Outputs** | Velocity field $\vec{v}(x,t)$, pressure field $p(x,t)$, temperature field $T(x,t)$, stress tensor $\boldsymbol{\tau}$, heat flux $\vec{q}$ |

## Related Scripts

- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and renders a dye tracer in real time with Pygame.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and draws the temperature field in real time with Pygame.

## Exercises

**Exercise 1.** Check whether each 2D velocity field satisfies the incompressible continuity equation $\nabla \cdot \vec{v} = 0$: (a) $\vec{v} = (x^2, -2xy)$; (b) $\vec{v} = (x^2, xy)$.

<details>
<summary>Answer</summary>

(a) $\partial u/\partial x + \partial v/\partial y = 2x - 2x = 0$, so the field is incompressible.

(b) $2x + x = 3x \neq 0$, so the field is not incompressible. It could only describe a flow in which the density changes, as allowed by $\partial\rho/\partial t + \nabla\cdot(\rho\vec{v}) = 0$.

</details>

**Exercise 2.** A steady flow enters a nozzle with $\rho_1 = 1.2$ kg/m³, $A_1 = 0.05$ m² and $V_1 = 10$ m/s, and leaves through $A_2 = 0.02$ m² with $\rho_2 = 1.5$ kg/m³. Use the integral mass equation from the RTT to find $V_2$.

<details>
<summary>Answer</summary>

In steady flow the volume integral does not change, so $`\int_A \rho\vec{v}\cdot\vec{n}\,dA = 0`$. With $\vec{n}$ pointing outward, the inlet contributes $-\rho_1 V_1 A_1$ and the outlet $+\rho_2 V_2 A_2$:

```math
V_2 = \frac{\rho_1 V_1 A_1}{\rho_2 A_2} = \frac{1.2 \times 10 \times 0.05}{1.5 \times 0.02} = 20 \text{ m/s}
```

with a mass flow rate of 0.6 kg/s.

</details>

**Exercise 3.** A water jet ($\rho = 1000$ kg/m³, $A = 10^{-3}$ m², $V = 20$ m/s) hits a flat plate normal to the jet and spreads out radially along the plate. Use the steady integral momentum equation in the jet direction to find the force the plate exerts on the fluid and the force on the plate. Neglect gravity and take the pressure as atmospheric on the free surfaces.

<details>
<summary>Answer</summary>

Take a control volume around the jet and the spreading sheet. At the inlet $\vec{v}\cdot\vec{n} = -V$, so the $x$-momentum flux is $\rho V(-V)A = -\rho V^2 A$. The outflow along the plate has no $x$-velocity.

The steady momentum balance gives $F_{x,\text{on fluid}} = -\rho V^2 A = -1000 \times 400 \times 10^{-3} = -400$ N.

The plate pushes the fluid back with 400 N, so the fluid pushes the plate with 400 N in the jet direction.

</details>

**Exercise 4.** Oil ($\mu = 0.1$ Pa s, $\rho = 870$ kg/m³, $c_p = 1900$ J/(kg K)) is sheared in a 1 mm gap by a wall moving at 5 m/s, with a linear velocity profile. Compute the viscous dissipation $\Phi = \mu (du/dy)^2$ and the adiabatic rate of temperature rise from the incompressible energy equation.

<details>
<summary>Answer</summary>

$du/dy = 5/10^{-3} = 5000$ s$`^{-1}`$, so $\Phi = 0.1 \times 5000^2 = 2.5 \times 10^6$ W/m³.

With no conduction and no convective temperature change, $`\rho c_p\, \partial T/\partial t = \Phi`$:

```math
\frac{\partial T}{\partial t} = \frac{2.5 \times 10^6}{870 \times 1900} \approx 1.5
\text{ K/s}
```

In lubrication and high-shear flows $\Phi$ cannot be neglected.

</details>

**Exercise 5.** For a Newtonian fluid with constant properties, $\boldsymbol{\tau} = \mu(\nabla\vec{v} + \nabla\vec{v}^T) + (\mu_v - \tfrac{2}{3}\mu)(\nabla\cdot\vec{v})\mathbf{I}$, where stress is taken positive in tension (the opposite sign to the $\boldsymbol{\tau}$ in the RTT section). Show that $\nabla\cdot\boldsymbol{\tau}$ gives the viscous terms of the compressible Navier–Stokes equation in this note, and that they reduce to $\mu\nabla^2\vec{v}$ for incompressible flow.

<details>
<summary>Answer</summary>

Using $\nabla\cdot(\nabla\vec{v}) = \nabla^2\vec{v}$ and $\nabla\cdot(\nabla\vec{v}^T) = \nabla(\nabla\cdot\vec{v})$:

```math
\nabla\cdot\boldsymbol{\tau} = \mu\nabla^2\vec{v} + \mu\nabla(\nabla\cdot\vec{v}) +
\left(\mu_v - \tfrac{2}{3}\mu\right)\nabla(\nabla\cdot\vec{v}) = \mu\nabla^2\vec{v} +
\left(\tfrac{\mu}{3} + \mu_v\right)\nabla(\nabla\cdot\vec{v})
```

This matches the compressible form. For incompressible flow $\nabla\cdot\vec{v} = 0$, so only $\mu\nabla^2\vec{v}$ remains.

</details>

## References

- White, F. M., *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- Batchelor, G. K., *An Introduction to Fluid Dynamics*, Cambridge University Press, 1967.
- Bird, R. B., Stewart, W. E., & Lightfoot, E. N., *Transport Phenomena*, 2nd ed., Wiley, 2002.
- Kundu, P. K., Cohen, I. M., & Dowling, D. R., *Fluid Mechanics*, 6th ed., Academic Press, 2016.
- Anderson, J. D., *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
