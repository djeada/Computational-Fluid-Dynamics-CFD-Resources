# Introduction to the Lattice Boltzmann Method

The lattice Boltzmann method (LBM) computes a flow without discretising the Navier–Stokes equations. It evolves a small set of particle distribution functions on a uniform lattice, and the density and velocity are moments of these distributions. Because the update is a local relaxation followed by a shift to neighbouring nodes, the method has no pressure Poisson equation, handles geometry as a mask of solid nodes, and parallelises almost perfectly. In exchange it only solves the weakly compressible Navier–Stokes equations at low Mach number, and its time step is tied to the lattice spacing.

This note explains why a kinetic (mesoscopic) description can replace the continuum equations, which scales make that valid, what equations LBM actually solves, and where it is stronger or weaker than a finite-volume Navier–Stokes solver. The general CFD workflow (geometry, mesh, discretisation, solution, verification and validation) is covered in [Introduction to CFD](../cfd/intro.md); the reading order of the lattice Boltzmann notes is in the [README](README.md).

## Problem Statement

The target is the incompressible Navier–Stokes system for velocity $\mathbf{u}(\mathbf{x}, t)$ and pressure $p(\mathbf{x}, t)$ in a domain $\Omega$:

$$
\nabla \cdot \mathbf{u} = 0,
\qquad \frac{\partial \mathbf{u}}{\partial t} +
(\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nu \nabla^2
\mathbf{u} + \mathbf{g}
$$

with density $\rho$, kinematic viscosity $\nu$, body acceleration $\mathbf{g}$, initial velocity $\mathbf{u}_0$ and no-slip, inflow, outflow or periodic conditions on $\partial\Omega$. A finite-volume solver discretises these equations directly and must couple pressure and velocity through a Poisson-type equation (see [Pressure–Velocity Coupling](../fvm/pressure_velocity_coupling.md)).

LBM instead advances $Q$ populations $f_i(\mathbf{x}, t)$, one per discrete velocity $\mathbf{c}_i$, and defines $\rho = \sum_i f_i$ and $\rho\mathbf{u} = \sum_i \mathbf{c}_i f_i$. The questions this note answers are:

- Under what conditions does a kinetic description reproduce the continuum equations? This is a statement about the Knudsen number.
- Which macroscopic equations does the lattice scheme reproduce, and with what errors?
- For which problems is that trade a good one?

A lattice Boltzmann solution counts as solved when its moments approximate the incompressible solution within a stated tolerance, which requires the discretisation error ($`O(\Delta x^2)`$) and the compressibility error ($`O(\mathrm{Ma}^2)`$) to be small together. The difficulty is that $\Delta x$, $\Delta t$, $\nu$ and the Mach number are coupled through a single relaxation parameter, so they cannot be chosen independently.

## Scales of Description

A gas at rest is still a swarm of molecules moving at the thermal speed, about 400 m/s for air or argon at room temperature. Each molecule travels a **mean free path** $\lambda$ between collisions. For hard spheres of diameter $d$ at pressure $p$ and temperature $T$,

```math
\lambda = \frac{k_B T}{\sqrt{2}\,\pi d^2 p}
```

which gives $\lambda \approx 66$ nm for nitrogen ($d = 0.37$ nm) at 293 K and 1 atm. The mean time between collisions is $\lambda$ divided by the mean thermal speed, about $2 \times 10^{-10}$ s. The ratio of $\lambda$ to a flow length scale $L$ is the **Knudsen number**

$$
\mathrm{Kn} = \frac{\lambda}{L}
$$

and it decides which description is valid:

| Regime | Knudsen number | Description |
| --- | --- | --- |
| Continuum | $\mathrm{Kn} < 0.01$ | Navier–Stokes with no-slip walls |
| Slip flow | $0.01 < \mathrm{Kn} < 0.1$ | Navier–Stokes with velocity slip and temperature jump at walls |
| Transitional | $0.1 < \mathrm{Kn} < 10$ | Boltzmann equation (DSMC, discrete-velocity methods) |
| Free molecular | $\mathrm{Kn} > 10$ | Collisionless Boltzmann equation |

The boundaries are conventional, not sharp. In the **continuum limit** $\mathrm{Kn} \to 0$ collisions keep the gas close to a local equilibrium. Then the Boltzmann equation reduces to the Euler equations at zeroth order in Kn and to the Navier–Stokes equations at first order; the [Boltzmann Equation](boltzmann_equation.md) note outlines the expansion. For a gas, the Knudsen, Mach and Reynolds numbers are linked, $\mathrm{Kn} \sim \mathrm{Ma}/\mathrm{Re}$, so a low-Mach flow at moderate or high Reynolds number is deep in the continuum regime.

The three levels of description are:

|  | Microscopic | Mesoscopic (kinetic) | Macroscopic (continuum) |
| --- | --- | --- | --- |
| State | positions and velocities of every molecule | distribution function $f(\mathbf{x}, \boldsymbol{\xi}, t)$ | fields $\rho$, $\mathbf{u}$, $p$, $T$ |
| Governing law | Newton's equations with an interaction potential | Boltzmann equation | Navier–Stokes equations |
| Typical methods | molecular dynamics (MD) | direct simulation Monte Carlo (DSMC), discrete-velocity methods | finite volume, finite element, finite difference, spectral |
| Valid for | any Kn, but domains of nanometres and nanoseconds | dilute gases at any Kn | $\mathrm{Kn} \lesssim 0.01$ (0.1 with slip conditions) |

The path from the first column to the last is the subject of [From Newton to Navier–Stokes](from_newton_to_nse.md).

LBM borrows the mesoscopic variables but is used almost entirely for continuum flows. Its velocity set and equilibrium are designed to reproduce the Navier–Stokes equations in the limit $\mathrm{Kn} \to 0$, and nothing more. The same scheme therefore simulates water, for which the Boltzmann equation is not a physical model, as well as air. A standard LBM is not a rarefied-gas solver: at $\mathrm{Kn} \gtrsim 0.1$ it needs larger velocity sets and modified boundary conditions.

## What the Lattice Boltzmann Method Solves

The lattice Boltzmann equation with the BGK collision operator, derived in [From Boltzmann to Lattice Boltzmann](from_boltzmann_to_lattice_boltzmann.md), is

$$
f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = f_i(\mathbf{x}, t) -
\frac{\Delta t}{\tau}\left[f_i(\mathbf{x}, t) - f_i^{\mathrm{eq}}(\rho,
\mathbf{u})\right]
$$

where $\tau$ is the relaxation time and $f_i^{\mathrm{eq}}$ a polynomial in $\mathbf{u}$. A Chapman–Enskog analysis shows that its moments satisfy, up to the errors listed below,

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{u}) = 0,
\qquad \frac{\partial (\rho \mathbf{u})}{\partial t} + \nabla \cdot
(\rho \mathbf{u}\mathbf{u}) = -\nabla p + \nabla \cdot
\left[\rho\nu\left(\nabla\mathbf{u} + (\nabla\mathbf{u})^T\right)\right] + \mathbf{F}
$$

with the isothermal equation of state and viscosity

$$
p = c_s^2 \rho,
\qquad \nu = c_s^2\left(\tau - \frac{\Delta t}{2}\right)
$$

where $`c_s = \Delta x/(\sqrt{3}\,\Delta t)`$ is the lattice speed of sound for the standard lattices. These are the isothermal, weakly compressible Navier–Stokes equations. They approach the incompressible equations when the Mach number $\mathrm{Ma} = |\mathbf{u}|/c_s$ is small, because density fluctuations scale as $\delta\rho/\rho \sim \mathrm{Ma}^2$. The pressure is not an independent unknown: it follows from the density, and pressure waves travel at $c_s$, much as in Chorin's artificial-compressibility method.

The main error sources are:

- the discretisation error, $O(\Delta x^2)$ in the bulk for a fixed $\tau$;
- the compressibility error, $O(\mathrm{Ma}^2)$ relative to the incompressible solution;
- a lattice error in the viscous stress of order $\mathrm{Ma}^3$, from the truncated equilibrium on the standard lattices;
- boundary errors, because half-way bounce-back is second order on straight walls with a $\tau$-dependent slip, but first order on curved walls approximated by staircases.

Each of these is quantified in the [algorithm](lattice_boltzmann_algorithm.md) and [practical](practical_lbm.md) notes.

## Strengths and Weaknesses

Compared with a pressure-based finite-volume solver for the incompressible Navier–Stokes equations:

| Aspect | Lattice Boltzmann | Finite-volume Navier–Stokes |
| --- | --- | --- |
| Pressure | from $p = c_s^2\rho$, no Poisson equation | pressure correction or projection with a global linear solve per step |
| Time integration | explicit; one collide and stream per step | explicit or implicit; large implicit steps and steady solvers possible |
| Time step | fixed by the lattice: $\Delta t \propto \Delta x$ at fixed Ma, so slow or steady flows need many steps | chosen by accuracy or CFL; steady problems solved directly |
| Grid | uniform Cartesian lattice; refinement needs special multi-block treatment | unstructured, body-fitted, anisotropic cells near walls |
| Complex geometry | voxelised solid mask; no meshing, but staircase walls unless interpolated boundaries are used | body-fitted mesh; meshing can dominate the project time |
| Parallel efficiency | local collision, nearest-neighbour streaming, one halo layer; excellent on GPUs | good, but the pressure solver needs global communication |
| High-Re wall-bounded flow | uniform cells cannot stretch towards walls; needs wall models or many nodes | stretched prism layers resolve boundary layers efficiently |
| Compressible and thermal flow | standard model is isothermal and low-Ma; extensions needed | mature compressible and energy solvers |
| Multiphase, porous media | natural extensions (Shan–Chen pseudopotential, bounce-back on pore geometry) | interface capturing (VOF, level set), porous resistance models |
| Memory | $Q$ populations per node (9 in 2D, 19 or 27 in 3D) | a few variables per cell, but sparse matrices for implicit solves |

LBM is the stronger choice for unsteady, low-Mach flows in complex or changing geometry, porous media, multiphase and particle-laden flows, and for problems large enough that GPU throughput matters. It is weaker for steady problems, high-speed compressible flow, and thin boundary layers that call for stretched cells.

## Key Takeaways

- The Knudsen number $\mathrm{Kn} = \lambda/L$ measures the separation between molecular and flow scales. Continuum equations hold for $\mathrm{Kn} \lesssim 0.01$.
- LBM evolves discrete distribution functions whose moments are $\rho$ and $\rho\mathbf{u}$. It recovers the isothermal, weakly compressible Navier–Stokes equations with $p = c_s^2\rho$ and $\nu = c_s^2(\tau - \Delta t/2)$.
- Incompressible flow is approximated with an error of order $\mathrm{Ma}^2$, so lattice velocities must stay well below $c_s$.
- The algorithm is explicit and local, needs no pressure equation and handles geometry as a solid mask, so it parallelises very well.
- The price is a uniform lattice, a time step tied to the lattice spacing, many populations per node, and extra work for thermal, compressible or high-Re wall-bounded flows.

## Related Scripts

- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.
- [Lattice Velocity Sets](../../../scripts/plots/lattice_velocity_sets/): draws the D2Q9 and D3Q19 velocity sets with their indices and weights, the streaming step on a small lattice, and half-way bounce-back at a wall.
- [LBM Poiseuille Validation](../../../scripts/algorithms/lbm_poiseuille_validation/): validates a D2Q9 BGK lattice Boltzmann solver against the exact solution for body-force-driven channel flow with half-way bounce-back walls.

## Exercises

**Exercise 1.** The companion cylinder script runs at $\mathrm{Re}_D = UD/\nu = 700$. For water ($\nu = 1.0 \times 10^{-6}$ m²/s) flowing at $U = 0.1$ m/s, what cylinder diameter gives this Reynolds number?

<details>
<summary>Answer</summary>

$`D = \mathrm{Re}_D\,\nu / U = 700 \times 10^{-6} / 0.1 = 7.0 \times 10^{-3}`$ m, i.e. 7 mm. The script states its Reynolds number as 350 based on the radius, which is the same flow.

</details>

**Exercise 2.** For argon (molar mass 39.948 g/mol) at $T = 293.15$ K, compute the mean thermal speed $\bar{v} = \sqrt{8 k_B T/(\pi m)}$. Taking a hard-sphere diameter $d = 0.36$ nm and $p = 101325$ Pa, compute the mean free path $\lambda$ and the mean collision time $\lambda/\bar{v}$.

<details>
<summary>Answer</summary>

The molecular mass is $m = 39.948 \times 1.6605 \times 10^{-27} \approx 6.63 \times 10^{-26}$ kg.

- $\bar{v} = \sqrt{8 \times 1.380649 \times 10^{-23} \times 293.15 / (\pi \times 6.63 \times 10^{-26})} \approx 394$ m/s.
- $`\lambda = k_B T/(\sqrt{2}\,\pi d^2 p) \approx 6.9 \times 10^{-8}`$ m, about 69 nm.
- Collision time $\approx 6.9 \times 10^{-8} / 394 \approx 1.8 \times 10^{-10}$ s.

Both are many orders of magnitude below engineering length and time scales.

</details>

**Exercise 3.** Argon at atmospheric pressure flows through a microchannel of height 50 µm. Using $\lambda$ from Exercise 2, compute the Knudsen number and decide whether the continuum description applies.

<details>
<summary>Answer</summary>

$\mathrm{Kn} = 6.9 \times 10^{-8} / 5 \times 10^{-5} \approx 1.4 \times 10^{-3}$. This is below 0.01, so the Navier–Stokes equations with no-slip walls apply. A standard LBM is also appropriate, because it is built to recover the Navier–Stokes equations in this small-Kn limit.

</details>

**Exercise 4.** Take the divergence of the incompressible momentum equation of the Problem Statement (constant $\rho$, $\mathbf{g} = 0$) to derive the pressure Poisson equation $`\nabla^2 p = -\rho\, \partial_i u_j\, \partial_j u_i`$ (summation over repeated indices). Verify it for solid-body rotation $\mathbf{u} = (-\Omega y, \Omega x)$, whose pressure is $p = p_0 + \rho\Omega^2(x^2 + y^2)/2$.

<details>
<summary>Answer</summary>

Because $\nabla \cdot \mathbf{u} = 0$, the divergences of $\partial\mathbf{u}/\partial t$ and of $\nu\nabla^2\mathbf{u}$ vanish. For the convective term,

```math
\partial_i \left(u_j \partial_j u_i \right) = \partial_i u_j \, \partial_j u_i + u_j \partial_j \left(\partial_i u_i \right) = \partial_i u_j \, \partial_j u_i
```

so $`\nabla^2 p = -\rho\, \partial_i u_j\, \partial_j u_i`$.

For solid-body rotation, $\partial_x u_x = \partial_y u_y = 0$, $\partial_y u_x = -\Omega$ and $\partial_x u_y = \Omega$, so $`\partial_i u_j\, \partial_j u_i = 2\,\partial_y u_x\, \partial_x u_y = -2\Omega^2`$ and $\nabla^2 p = 2\rho\Omega^2$. Directly, $\nabla^2[\rho\Omega^2(x^2 + y^2)/2] = 2\rho\Omega^2$. A pressure-based solver solves a discrete form of this equation every time step; LBM obtains $p$ from $c_s^2\rho$ instead.

</details>

**Exercise 5.** In an LBM simulation the viscosity can be written as $\nu = c_s \lambda_{\mathrm{eff}}$, which defines an effective mean free path $\lambda_{\mathrm{eff}}$. Show that the corresponding Knudsen number is $\mathrm{Kn} = \lambda_{\mathrm{eff}}/L = \mathrm{Ma}/\mathrm{Re}$ with $\mathrm{Ma} = U/c_s$ and $\mathrm{Re} = UL/\nu$. Evaluate it, and $\lambda_{\mathrm{eff}}$ in lattice units, for the cylinder script ($U = 0.06$, $D = 60$, $\nu = 0.00514$, $c_s = 1/\sqrt{3}$).

<details>
<summary>Answer</summary>

$`\mathrm{Kn} = \nu/(c_s L) = (\nu/(UL))(U/c_s) = \mathrm{Ma}/\mathrm{Re}`$.

For the script, $\mathrm{Ma} = 0.06\sqrt{3} = 0.104$ and $`\mathrm{Re}_D = 0.06 \times 60/0.00514 = 700`$, so $`\mathrm{Kn} = 1.5 \times 10^{-4}`$. The effective mean free path is $`\lambda_{\mathrm{eff}} = 0.00514\sqrt{3} \approx 0.0089`$ lattice spacings. The simulated "gas" is far inside the continuum regime even though the lattice itself is coarse: $\tau$ is a numerical parameter that sets $\nu$, not a physical collision time.

</details>

## References

- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
- S. Succi, *The Lattice Boltzmann Equation for Fluid Dynamics and Beyond*, Oxford University Press, 2001.
- S. Succi, *The Lattice Boltzmann Equation: For Complex States of Flowing Matter*, Oxford University Press, 2018.
- S. Chen and G. D. Doolen, "Lattice Boltzmann method for fluid flows", *Annual Review of Fluid Mechanics* 30, 329–364, 1998.
- G. A. Bird, *Molecular Gas Dynamics and the Direct Simulation of Gas Flows*, Oxford University Press, 1994.
- J. H. Ferziger, M. Perić and R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
