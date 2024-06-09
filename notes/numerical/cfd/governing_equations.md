# Governing Equations in Fluid Dynamics

In fluid dynamics, the behavior of fluid flows is described by a set of governing equations. These equations are derived from fundamental principles of physics, including conservation of mass, momentum, and energy. The primary governing equations are the Continuity Equation, the Navier-Stokes Equations, and the Energy Equation.

## Continuity Equation

The Continuity Equation represents the conservation of mass in a fluid flow. It states that the rate of change of mass in a control volume is equal to the net mass flux across its boundaries.

### Continuity Equation (General Form)

For a compressible fluid:

$$ \frac{\partial \rho}{\partial t} + 
abla \cdot (\rho \vec{v}) = 0 $$

Where:
- $ \rho $ is the fluid density,
- $ \vec{v} $ is the fluid velocity vector,
- $ t $ is time.

For an incompressible fluid ($ \rho $ is constant):

$$ 
abla \cdot \vec{v} = 0 $$

### Explanation

- The first term, $ \frac{\partial \rho}{\partial t} $, represents the local rate of change of density.
- The second term, $ 
abla \cdot (\rho \vec{v}) $, represents the convective rate of change of density due to fluid motion.

## Navier-Stokes Equations

The Navier-Stokes Equations describe the conservation of momentum in fluid flows. They are derived from Newton's second law and account for the forces acting on a fluid element.

### Navier-Stokes Equations (General Form)

For a compressible fluid:

$$ \rho \left( \frac{\partial \vec{v}}{\partial t} + \vec{v} \cdot 
abla \vec{v} \right) = -
abla p + \mu 
abla^2 \vec{v} + \left( \frac{\mu}{3} + \mu_v \right) 
abla (
abla \cdot \vec{v}) + \vec{f} $$

Where:
- $ \vec{v} $ is the fluid velocity vector,
- $ p $ is the pressure,
- $ \mu $ is the dynamic viscosity,
- $ \mu_v $ is the bulk viscosity,
- $ \vec{f} $ represents body forces (e.g., gravity).

For an incompressible fluid:

$$ \rho \left( \frac{\partial \vec{v}}{\partial t} + \vec{v} \cdot 
abla \vec{v} \right) = -
abla p + \mu 
abla^2 \vec{v} + \vec{f} $$

### Explanation

- The left side of the equation represents the rate of change of momentum.
- The right side includes pressure forces, viscous forces, and body forces.

## Energy Equation

The Energy Equation describes the conservation of energy in a fluid flow. It accounts for the internal energy, kinetic energy, and heat transfer within the fluid.

### Energy Equation (General Form)

For a compressible fluid:

$$ \frac{\partial}{\partial t} \left( \rho e \right) + 
abla \cdot \left( \rho e \vec{v} \right) = - p (
abla \cdot \vec{v}) + 
abla \cdot (k 
abla T) + \Phi $$

Where:
- $ e $ is the total energy per unit mass,
- $ k $ is the thermal conductivity,
- $ T $ is the temperature,
- $ \Phi $ represents viscous dissipation.

For an incompressible fluid (simplified form):

$$ \rho c_p \left( \frac{\partial T}{\partial t} + \vec{v} \cdot 
abla T \right) = k 
abla^2 T + \Phi $$

Where:
- $ c_p $ is the specific heat at constant pressure.

### Explanation

- The left side represents the rate of change of internal energy and kinetic energy.
- The right side includes work done by pressure forces, heat conduction, and viscous dissipation.



## UNDEFINED

* defined trough reynold transport theorem
* RTT relates lagrangian system to eulerian control volume
* The RTT connects a Lagrangian system with an Eulerian control volume. 
    * By Lagrangian system, we mean a system of a given specified mass, or a *marked mass*.
* Conservation laws are written in terms of Lagrangian systems, but we solve CFD problems on Eulerian domains. The RTT connects these.

* The RTT is written as

$$\frac{dB_{\text{sys}}}{dt} = \frac{d}{dt}\int_V \rho\beta dV + \int_A \rho\beta\vec{v}\cdot\vec{n} dA$$

* $B_{sys}$ is some extensive quantity, like mass, momentum, or energy.
* $\beta = B_{sys}/m$ is intensive.
* $\rho\beta$ will be mass, momentum, energy, etc. per unit volume.
* $\rho\beta\vec{v}$ is $B$-flux, like mass flux, momentum flux, energy flux.
* $\vec{n}$ is a unit normal vector pointing *out* of the surface of a control volume. 
* In an area dA, $\rho\beta\vec{v}\cdot\vec{n}dA$ will be rate of B flowing out of a control volume through that area dA. 

### Mass

* $B_{sys} = m$
* $\beta = B_{sys}/m = 1$.
* Lagrangian conservation law: mass is conserved, or the rate of change of a given mass is zero:
$$\frac{dm}{dt} = 0.$$
* Substitute into the RTT and swap the right and left sides of the equality:

$$\frac{d}{dt}\int_V\rho dV + \int_A\rho\vec{v}\cdot\vec{n}dA = 0.$$

### Momentum
* $B_{sys} = m\vec{v}$
* $\beta = B_{sys}/m = \vec{v}$
* Lagrangian conservation law: the rate of change of momentum of a fixed mass (system) is the sum of the external forces on the mass (system).
    * We have surface forces $\vec{F}$, and body forces (denoted with external field $\vec{g}$, nominally gravitational acceleration):
$$\frac{dm\vec{v}}{dt} = \int_A \vec{F}dA + \int_V\vec{g}\rho dV.$$
    * Consider viscous and pressure forces, so that $\vec{F} = -\boldsymbol{\tau}\cdot\vec{n} - P\boldsymbol{\delta}\cdot{\vec{n}}$, where $\boldsymbol{\tau}$ is the viscous stress tensor, and $\boldsymbol{\delta}$ is the unit tensor. 
        * (The negative sign is because $\vec{n}$ points *out* of the suface, and we want the force on or into the surface.) 
    * This gives
$$\frac{dm\vec{v}}{dt} = -\int_A\boldsymbol{\tau}\cdot\vec{n}dA -\int_AP\boldsymbol{\delta}\cdot\vec{n}dA+ \int_V\vec{g}\rho dV.$$
* Substitute into the RTT and swap the right and left sides of the equality:

$$\frac{d}{dt}\int_V\rho\vec{v}dV + \int_A\rho\vec{v}\vec{v}\cdot\vec{n}dA = -\int_A\boldsymbol{\tau}\cdot\vec{n}dA -\int_AP\boldsymbol{\delta}\cdot\vec{n}dA+ \int_V\vec{g}\rho dV.$$
* Here, $\vec{v}\vec{v}$ is a tensor, and can be written as $\vec{v}\otimes\vec{v}$, or $v_iv_j$ in index notation.

### Energy
* $B_{sys} = E$ (where $E = mu + \frac{1}{2}m\vec{v}\cdot\vec{v}$ is internal + kinetic energy).
* $\beta = E/m = e$.
* Lagrangian conservation law: the rate of change of energy of a given mass is the sum of the heat transfered to the mass and the work performed on the mass:
$$\frac{dE}{dt} = -\int_A\vec{q}\cdot\vec{n}dA + \int_A\vec{F}\cdot\vec{v}dA + \int_V\rho\vec{g}\cdot\vec{v}dV.$$
    * Here, $\vec{q}$ is the heat flux vector. As before, $\vec{F} = -\boldsymbol{\tau}\cdot\vec{n} - P\boldsymbol{\delta}\cdot{\vec{n}}$. 
    * The symmetry of $\boldsymbol{\tau}$ and $\boldsymbol{\delta}$ let us write $\boldsymbol{\tau}\cdot\vec{n}\cdot\vec{v} = \boldsymbol{\tau}\cdot\vec{v}\cdot\vec{n}$ and $P\boldsymbol{\delta}\cdot\vec{n}\cdot\vec{v} = P\boldsymbol{\delta}\cdot\vec{v}\cdot\vec{n}$.
* Substitute into the RTT and swap the right and left sides of the equality:

$$\frac{d}{dt}\int_V\rho edV + \int_A\rho e\vec{v}\cdot\vec{n}dA = 
-\int_A\vec{q}\cdot\vec{n}dA - \int_A(\boldsymbol{\tau}\cdot\vec{v})\cdot\vec{n}dA - \int_A(P\boldsymbol{\delta}\cdot\vec{v})\cdot\vec{n}dA+ \int_V\rho\vec{g}\cdot\vec{v}dV.$$

### Differential form

* The above equations are in integral form, which is convenient for a Finite Volume solution. (It is also convenient for derivation.)
* We can find the differential form as follows.
    * If the control volume is fixed in time, we can move $d/dt$ inside the volume integral.
    * Replace integrals over the surface area with volume integrals by applying the Gauss Divergence Theorem:
    $$\int_A\vec{v}\cdot\vec{n}dA = \int_V
abla\cdot\vec{v},$$
    where $\vec{v}$ is some vector (not necessarily velocity).
        * Hence, in the equation for mass we have $\int_A\rho\vec{v}\cdot\vec{n}dA = \int_V
abla\cdot(\rho\vec{v})dV$.
    * Combine all the volume integrals into $\int_V(\text{all terms})dV = 0$. Since the volume integrated over is arbitrary, this equation can only be true if the integrand $(\text{all terms})$ itself is 0. This gives the final result. (Also, $
abla\cdot(P\boldsymbol{\delta}) = 
abla P$.)
    
$$\text{Mass Equation:} \quad \frac{\partial \rho}{\partial t} + 
abla \cdot (\rho \mathbf{v}) = 0$$

$$\text{Momentum Equation:} \quad \frac{\partial (\rho \mathbf{v})}{\partial t} + 
abla \cdot (\rho \mathbf{v} \mathbf{v}) = -
abla \cdot \boldsymbol{\tau} \text{ (viscous forces)} - 
abla P \text{ (pressure forces)} + \rho \mathbf{g} \text{ (gravitational forces)}$$

$$\text{Energy Equation:} \quad \frac{\partial (\rho e)}{\partial t} + 
abla \cdot (\rho e \mathbf{v}) = -
abla \cdot \mathbf{q} \text{ (heat flux)} - 
abla \cdot (\boldsymbol{\tau} \cdot \mathbf{v}) \text{ (viscous heating)} -
abla \cdot (P \mathbf{v}) \text{ (PV work)} + \rho \mathbf{g} \cdot \mathbf{v} \text{ (field work)}$$

* The terms on the left hand side (LHS) of the equation are the accumulation and in/out transport through the control volume.
* The terms on the right hand side (RHS) are as noted. In the energy equation, field work will convert potential energy to kinetic energy (which is part of $e$).
