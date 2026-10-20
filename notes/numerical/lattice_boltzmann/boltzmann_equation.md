# The Boltzmann Equation

The Boltzmann equation governs the one-particle distribution function $f(\mathbf{x}, \boldsymbol{\xi}, t)$ of a dilute gas. Molecules stream freely along their velocities and occasionally collide, and collisions drive $f$ towards a local Maxwell–Boltzmann equilibrium. This note states the equation and its collision operator, shows why mass, momentum and energy are conserved and why entropy increases (the H-theorem), introduces the BGK relaxation model that lattice Boltzmann methods use, and outlines the Chapman–Enskog expansion that turns the kinetic equation into the Navier–Stokes equations with a viscosity set by the relaxation time. The distribution function and its moments are defined in [From Newton to Navier–Stokes](from_newton_to_nse.md).

## Problem Statement

Find $f(\mathbf{x}, \boldsymbol{\xi}, t)$, the mass density in the six-dimensional phase space of position $\mathbf{x}$ and molecular velocity $\boldsymbol{\xi}$, such that

$$
\frac{\partial f}{\partial t} + \boldsymbol{\xi} \cdot \nabla_{\mathbf{x}} f +
\mathbf{a} \cdot \nabla_{\boldsymbol{\xi}} f = \Omega(f)
$$

for given initial data $f(\mathbf{x}, \boldsymbol{\xi}, 0)$ and conditions at walls and open boundaries. Here $\mathbf{a}$ is the acceleration due to an external force, such as gravity, and $\Omega(f)$ is the collision operator. The second part of the problem is to show that, when the Knudsen number $\mathrm{Kn} = \lambda/L$ is small, the moments $\rho$, $\mathbf{u}$ and $T$ of the solution obey the Navier–Stokes equations, and to find the viscosity and thermal conductivity that follow from the collision model.

The difficulties are the dimension (six phase-space coordinates and time), the nonlinear five-fold collision integral, and the stiffness at small Kn: collisions act on the time scale $\tau \sim \lambda/\bar{v}$, which is many orders of magnitude shorter than the flow time $L/U$.

## Streaming and Collisions

The left-hand side is the rate of change of $f$ along a molecular trajectory in phase space, $d\mathbf{x}/dt = \boldsymbol{\xi}$ and $d\boldsymbol{\xi}/dt = \mathbf{a}$. Without collisions, $f$ is constant along these trajectories: molecules simply stream. For a uniform force-free gas this gives $f(\mathbf{x}, \boldsymbol{\xi}, t) = f(\mathbf{x} - \boldsymbol{\xi} t, \boldsymbol{\xi}, 0)$, an advection at the molecular velocity. The lattice Boltzmann method keeps this structure exactly: its streaming step moves each population by one lattice link per time step.

For a dilute gas of molecules of mass $m$ with binary collisions, Boltzmann's collision operator is

```math
\Omega(f) = \frac{1}{m}\int_{\mathbb{R}^3} \int_{S^2} \lvert\boldsymbol{\xi} - \boldsymbol{\xi}_\star\rvert \, \sigma(\lvert\boldsymbol{\xi} - \boldsymbol{\xi}_\star\rvert, \Theta) \left[f(\boldsymbol{\xi}')\,f(\boldsymbol{\xi}_\star') - f(\boldsymbol{\xi})\,f(\boldsymbol{\xi}_\star)\right] d\Omega \; d^3\xi_\star
```

where $`\boldsymbol{\xi}_\star`$ is the velocity of the collision partner, $`\boldsymbol{\xi}'`$ and $`\boldsymbol{\xi}_\star'`$ are the velocities after a collision with scattering angle $\Theta$, and $\sigma$ is the differential cross-section (for hard spheres of diameter $d$, $\sigma = d^2/4$). The first term counts collisions that produce a molecule with velocity $\boldsymbol{\xi}$ (gain), and the second those that remove one (loss). All functions are evaluated at the same $\mathbf{x}$ and $t$. The post-collision velocities follow from conservation of momentum and kinetic energy in an elastic collision:

$$
\boldsymbol{\xi}' + \boldsymbol{\xi}_\star' = \boldsymbol{\xi} + \boldsymbol{\xi}_\star,
\qquad \lvert\boldsymbol{\xi}'\rvert^2 +
\lvert\boldsymbol{\xi}_\star'\rvert^2 = \lvert\boldsymbol{\xi}\rvert^2 +
\lvert\boldsymbol{\xi}_\star\rvert^2
$$

## Collision Invariants and Conservation Laws

A function $\psi(\boldsymbol{\xi})$ is a collision invariant if $`\psi(\boldsymbol{\xi}') + \psi(\boldsymbol{\xi}_\star') = \psi(\boldsymbol{\xi}) + \psi(\boldsymbol{\xi}_\star)`$ for every collision. By the conservation laws above, $\psi = 1$, $\xi_\alpha$ and $|\boldsymbol{\xi}|^2$ are invariants, and every collision invariant is a linear combination of these five. Exchanging the roles of the colliding molecules and of pre- and post-collision states in the integral shows that

```math
\int \psi(\boldsymbol{\xi}) \, \Omega(f) \, d^3\xi = 0
\qquad \text{for } \psi \in \left\lbrace 1, \boldsymbol{\xi},
\tfrac{1}{2}\lvert\boldsymbol{\xi}\rvert^2 \right\rbrace
```

Collisions redistribute velocities but create no mass, momentum or energy. Multiplying the Boltzmann equation by each invariant and integrating over $\boldsymbol{\xi}$ therefore gives exact balance laws, written with the moments $\rho$, $\mathbf{u}$, $e$, $\mathbf{P}$ and $\mathbf{q}$ of [From Newton to Navier–Stokes](from_newton_to_nse.md#macroscopic-fields-as-moments) and the total specific energy $E = e + \frac{1}{2}|\mathbf{u}|^2$:

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho\mathbf{u}) = 0
$$

$$
\frac{\partial (\rho\mathbf{u})}{\partial t} + \nabla \cdot
(\rho\mathbf{u}\mathbf{u} + \mathbf{P}) = \rho\mathbf{a}
$$

$$
\frac{\partial (\rho E)}{\partial t} + \nabla \cdot
(\rho E \mathbf{u} + \mathbf{P} \cdot \mathbf{u} + \mathbf{q}) = \rho\mathbf{a} \cdot
\mathbf{u}
$$

These are the continuum conservation laws. They hold for any $f$, but they are closed only once $\mathbf{P}$ and $\mathbf{q}$ are known in terms of $\rho$, $\mathbf{u}$ and $T$.

## The H-Theorem and the Maxwell–Boltzmann Equilibrium

Boltzmann's H-function is

```math
H(t) = \int \int f \ln f \; d^3\xi \; d^3x
```

For the collision operator above, the same symmetrisation gives

```math
\int \ln f \; \Omega(f) \, d^3\xi = -\frac{1}{4m}\iiint \lvert\boldsymbol{\xi} - \boldsymbol{\xi}_\star\rvert \sigma \left(f' f_\star' - f f_\star\right) \ln\frac{f' f_\star'}{f f_\star} \, d\Omega \, d^3\xi_\star \, d^3\xi \le 0
```

because $(y - x)\ln(y/x) \ge 0$ for all positive $x$ and $y$. In a closed or periodic domain, $dH/dt \le 0$. This is the **H-theorem**. Since $-H$ is proportional to the entropy, collisions make entropy grow. Equality holds only when $f' f_\star' = f f_\star$ for all collisions, which means that $\ln f$ is a collision invariant, $\ln f = a + \mathbf{b} \cdot \boldsymbol{\xi} + c|\boldsymbol{\xi}|^2$. Fixing the five constants with the local density, velocity and temperature gives the **Maxwell–Boltzmann equilibrium**

$$
f^{\mathrm{eq}}(\boldsymbol{\xi}) = \frac{\rho}{(2\pi RT)^{3/2}}
\exp\left(-\frac{\lvert\boldsymbol{\xi} - \mathbf{u}\rvert^2}{2RT}\right)
$$

with specific gas constant $R = k_B/m$. Its moments are $\rho$, $\rho\mathbf{u}$, $`\mathbf{P} = \rho RT\,\mathbf{I}`$ and $\mathbf{q} = 0$. Inserted into the balance laws, these give the Euler equations of an ideal monatomic gas with $p = \rho RT$: a gas in exact local equilibrium has neither viscosity nor heat conduction.

## The BGK Collision Model

Bhatnagar, Gross and Krook (1954) replaced the collision integral by a relaxation towards the local equilibrium:

$$
\Omega_{\mathrm{BGK}}(f) = -\frac{1}{\tau}\left(f - f^{\mathrm{eq}}\right)
$$

where $\tau$ is a relaxation time of the order of the mean collision time and $f^{\mathrm{eq}}$ is the Maxwellian built from the $\rho$, $\mathbf{u}$ and $T$ of $f$ itself. Because $f$ and $f^{\mathrm{eq}}$ share these moments, the BGK operator has the same collision invariants as the full operator, and it also satisfies an H-theorem. It keeps the two properties that matter for hydrodynamics, conservation and relaxation to the right equilibrium, while removing the integral.

The price is a single time scale for all non-equilibrium moments. Stress and heat flux relax at the same rate, so the BGK gas has a Prandtl number of 1, while real monatomic gases have $\mathrm{Pr} \approx 2/3$ and air about 0.71. For isothermal lattice Boltzmann simulations this does not matter. Thermal lattice models fix it with a second distribution or with multiple relaxation times.

## Chapman–Enskog Expansion

The Chapman–Enskog expansion seeks solutions of the BGK equation that depend on time only through the slowly varying fields $\rho$, $\mathbf{u}$ and $T$. Measuring $t$ in units of $L/\bar{v}$ and $\mathbf{x}$ in units of $L$, the collision term is multiplied by $1/\mathrm{Kn}$, so with $\varepsilon = \mathrm{Kn}$:

$$
\varepsilon\left(\frac{\partial f}{\partial t} + \boldsymbol{\xi} \cdot \nabla f +
\mathbf{a} \cdot \nabla_{\boldsymbol{\xi}} f\right) = -\left(f - f^{\mathrm{eq}}\right)
$$

The outline is:

1. Expand $f = f^{(0)} + \varepsilon f^{(1)} + \varepsilon^2 f^{(2)} + \ldots$, and require that the corrections $f^{(k)}$, $k \ge 1$, carry no mass, momentum or energy, so that $\rho$, $\mathbf{u}$ and $T$ are defined by $f^{(0)}$ alone.

2. At order $\varepsilon^0$, $f^{(0)} = f^{\mathrm{eq}}$. Its moments give the Euler equations, which define the time derivatives of $\rho$, $\mathbf{u}$ and $T$ at this order.

3. At order $\varepsilon^1$, back in dimensional form, $`f^{(1)} = -\tau\left(\partial_t + \boldsymbol{\xi} \cdot \nabla + \mathbf{a} \cdot \nabla_{\boldsymbol{\xi}}\right) f^{\mathrm{eq}}`$, with the time derivatives replaced by their Euler values. After some algebra this becomes

   ```math
   f^{(1)} = -\tau f^{\mathrm{eq}} \left[\frac{1}{RT}\left(v_\alpha v_\beta - \frac{1}{3}\lvert\mathbf{v}\rvert^2\delta_{\alpha\beta}\right)\frac{\partial u_\alpha}{\partial x_\beta} + \left(\frac{\lvert\mathbf{v}\rvert^2}{2RT} - \frac{5}{2}\right) \mathbf{v} \cdot \nabla \ln T\right]
   ```

   where $\mathbf{v} = \boldsymbol{\xi} - \mathbf{u}$ is the peculiar velocity and repeated indices are summed.

4. The moments of $f^{(1)}$ give Newton's law of viscosity and Fourier's law,

   ```math
   \mathbf{P} = p\mathbf{I} - \mu\left(\nabla\mathbf{u} + (\nabla\mathbf{u})^T - \tfrac{2}{3}(\nabla \cdot \mathbf{u})\mathbf{I}\right), \qquad \mathbf{q} = -k\nabla T
   ```

   with $\mu = p\tau$ and $`k = \frac{5}{2}R\,p\tau`$. Substituted into the balance laws, they give the compressible Navier–Stokes–Fourier equations, with errors of order $\mathrm{Kn}^2$ (the Burnett terms).

The relation $\mu = p\tau$ makes physical sense. For air at 1 atm, $\mu = 1.8 \times 10^{-5}$ Pa s gives $\tau = \mu/p \approx 1.8 \times 10^{-10}$ s, the mean collision time.

### The Isothermal Case Used by LBM

Standard lattice Boltzmann models use an equilibrium at a fixed reference temperature $T_0$ and do not conserve energy. With $c_s^2 = RT_0$ the equilibrium pressure is $p = c_s^2\rho$, and the first-order non-equilibrium stress becomes

$$
\mathbf{P}^{(1)} = -\tau\left(\partial_t \mathbf{\Pi}^{\mathrm{eq}} + \nabla \cdot
\mathbf{Q}^{\mathrm{eq}}\right) = -\rho c_s^2 \tau
\left(\nabla\mathbf{u} + (\nabla\mathbf{u})^T\right) + O(u^3)
$$

where $`\mathbf{\Pi}^{\mathrm{eq}} = \int \boldsymbol{\xi}\boldsymbol{\xi} f^{\mathrm{eq}} \, d^3\xi`$ and $`\mathbf{Q}^{\mathrm{eq}} = \int \boldsymbol{\xi}\boldsymbol{\xi}\boldsymbol{\xi} f^{\mathrm{eq}} \, d^3\xi`$. The $O(u^3)$ terms cancel for the exact Maxwellian but not on the standard lattices, which is the origin of the $\mathrm{Ma}^3$ error of lattice Boltzmann models. The kinematic shear viscosity is $\nu = c_s^2\tau$. Because the stress has no $-\frac{2}{3}(\nabla \cdot \mathbf{u})\mathbf{I}$ term, the isothermal model also has a bulk viscosity, $\mu_b = \frac{2}{3}\mu$ in three dimensions, which only acts on compressive motion.

### The Lattice Relaxation Time

The lattice Boltzmann equation discretises the BGK equation along its characteristics:

$$
f_i(\mathbf{x} + \mathbf{c}_i\Delta t, t + \Delta t) -
f_i(\mathbf{x}, t) = -\frac{\Delta t}{\tau}\left(f_i - f_i^{\mathrm{eq}}\right)
$$

With $D_i = \partial_t + \mathbf{c}_i \cdot \nabla$ and $f_i^{\mathrm{neq}} = f_i - f_i^{\mathrm{eq}}$, a Taylor expansion of the left-hand side to second order gives

```math
\Delta t\, D_i f_i + \frac{\Delta t^2}{2} D_i^2 f_i = -\frac{\Delta t}{\tau}
f_i^{\mathrm{neq}}
```

At leading order $f_i^{\mathrm{neq}} \approx -\tau D_i f_i^{\mathrm{eq}}$, as in the continuous case. Using it in the second-order term, $\frac{\Delta t^2}{2} D_i^2 f_i \approx -\frac{\Delta t^2}{2\tau} D_i f_i^{\mathrm{neq}}$, so

$$
D_i f_i^{\mathrm{eq}} + \left(1 - \frac{\Delta t}{2\tau}\right) D_i
f_i^{\mathrm{neq}} = -\frac{1}{\tau} f_i^{\mathrm{neq}}
$$

The non-equilibrium part enters the momentum flux multiplied by $1 - \Delta t/(2\tau)$, so the viscous stress is $\rho c_s^2 \tau (1 - \Delta t/(2\tau))(\nabla\mathbf{u} + (\nabla\mathbf{u})^T)$ and

$$
\nu = c_s^2\left(\tau - \frac{\Delta t}{2}\right)
$$

The $-\Delta t/2$ is the numerical diffusion of the explicit streaming step. It is negative and is absorbed exactly into the physical viscosity, which is why the scheme is second-order accurate despite its first-order appearance. It also explains the stability limit $\tau > \Delta t/2$, below which the viscosity would be negative. The same result follows from a trapezoidal integration with a change of variables, derived in [From Boltzmann to Lattice Boltzmann](from_boltzmann_to_lattice_boltzmann.md#integration-along-characteristics), and the [Taylor–Green decay script](../../../scripts/algorithms/lbm_taylor_green_decay/) confirms it numerically.

## Key Takeaways

- The Boltzmann equation balances free streaming of molecules against binary collisions. It is closed by the molecular-chaos assumption and valid for dilute gases at any Kn.
- The collision invariants $1$, $\boldsymbol{\xi}$ and $|\boldsymbol{\xi}|^2/2$ give exact but unclosed conservation laws for mass, momentum and energy.
- The H-theorem shows that collisions increase entropy and that the only equilibrium is the local Maxwell–Boltzmann distribution, whose moments give the Euler equations.
- The BGK model relaxes $f$ towards $f^{\mathrm{eq}}$ with one time scale $\tau$. It conserves the invariants and gives $\mu = p\tau$ and $\mathrm{Pr} = 1$.
- The Chapman–Enskog expansion recovers the Navier–Stokes equations at first order in Kn. In the isothermal lattice form, $\nu = c_s^2(\tau - \Delta t/2)$.

## Related Scripts

- [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve.
- [Microscopic vs. Macroscopic View of a Fluid](../../../scripts/plots/microscopic_view/): draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid.
- [LBM Taylor–Green Decay](../../../scripts/algorithms/lbm_taylor_green_decay/): measures the viscosity of the D2Q9 BGK lattice Boltzmann scheme from the decay of a Taylor–Green vortex and compares it with $\nu = c_s^2(\tau - 1/2)$.

## Exercises

**Exercise 1.** A spatially homogeneous, force-free gas evolves under the BGK model towards a constant equilibrium $f^{\mathrm{eq}}$. Solve for $f(t)$ with $f(0) = f_0$, and find the fraction of the initial departure from equilibrium that remains at $t = 3\tau$.

<details>
<summary>Answer</summary>

With no spatial gradients and $\mathbf{a} = 0$ the equation reduces to $\partial f/\partial t = -(f - f^{\mathrm{eq}})/\tau$. Writing $g = f - f^{\mathrm{eq}}$ gives $dg/dt = -g/\tau$, so

```math
f(t) = f^{\mathrm{eq}} + \left(f_0 - f^{\mathrm{eq}}\right) e^{-t/\tau}
```

At $t = 3\tau$ the remaining fraction is $e^{-3} \approx 0.0498$, about 5%. The relaxation time is the e-folding time of the approach to equilibrium.

</details>

**Exercise 2.** Show that the BGK collision term conserves mass and momentum at every point only if the equilibrium has the same density and momentum as $f$, that is $`\int f^{\mathrm{eq}} \, d^3\xi = \rho`$ and $`\int \boldsymbol{\xi} f^{\mathrm{eq}} \, d^3\xi = \rho\mathbf{u}`$.

<details>
<summary>Answer</summary>

The rate of change of density due to collisions is the zeroth moment of the collision term:

```math
\int \Omega_{\mathrm{BGK}} \, d^3\xi = -\frac{1}{\tau} \left(\rho - \int f^{\mathrm{eq}} \, d^3\xi \right)
```

This vanishes for every $f$ only if $`\int f^{\mathrm{eq}} \, d^3\xi = \rho`$. The first moment gives $`-\frac{1}{\tau}\left(\rho\mathbf{u} - \int \boldsymbol{\xi} f^{\mathrm{eq}} \, d^3\xi\right)`$, which vanishes only if $`\int \boldsymbol{\xi} f^{\mathrm{eq}} \, d^3\xi = \rho\mathbf{u}`$. So $f^{\mathrm{eq}}$ must be built from the local $\rho$ and $\mathbf{u}$ of $f$ itself, and from its local temperature if energy is also to be conserved. The local Maxwellian satisfies all of these constraints.

</details>

**Exercise 3.** In one velocity dimension the Maxwellian is $`f^{\mathrm{eq}}(\xi) = \rho \, (2\pi RT)^{-1/2} \exp\left(-(\xi - u)^2/(2RT)\right)`$. Compute its zeroth, first and second moments, and show that the pressure is $p = \rho RT$. Evaluate $p$ for air with $\rho = 1.2$ kg/m³, $R = 287$ J/(kg K) and $T = 300$ K.

<details>
<summary>Answer</summary>

Substitute $v = \xi - u$ and use $\int e^{-v^2/(2RT)} dv = \sqrt{2\pi RT}$, $`\int v \, e^{-v^2/(2RT)} dv = 0`$ and $\int v^2 e^{-v^2/(2RT)} dv = RT\sqrt{2\pi RT}$:

```math
\int f^{\mathrm{eq}} d\xi = \rho,
\qquad \int \xi f^{\mathrm{eq}} d\xi = \rho u,
\qquad \int \xi^2 f^{\mathrm{eq}} d\xi = \rho u^2 + \rho R T
```

The pressure is the second moment of the peculiar velocity, $`p = \int v^2 f^{\mathrm{eq}} \, dv = \rho R T`$, the ideal-gas law. For the given air, $p = 1.2 \times 287 \times 300 = 103320$ Pa.

</details>

**Exercise 4.** Using the Knudsen-number regimes of the [introduction](intro.md#scales-of-description) and $\lambda \approx 68$ nm for air at atmospheric conditions, classify flow through a channel of width (a) 10 µm and (b) 100 nm, and say whether the Navier–Stokes equations or a Boltzmann-level description is needed.

<details>
<summary>Answer</summary>

(a) $\mathrm{Kn} = 68 \times 10^{-9} / 10 \times 10^{-6} = 6.8 \times 10^{-3}$. This is in the continuum range, close to the slip threshold, so the Navier–Stokes equations with no-slip walls are adequate.

(b) $\mathrm{Kn} = 68 \times 10^{-9} / 100 \times 10^{-9} = 0.68$, transitional flow. The Chapman–Enskog expansion behind the Navier–Stokes equations assumes small Kn, so a kinetic method such as DSMC or a discrete-velocity solver of the Boltzmann equation is needed. A standard lattice Boltzmann model is also built for the small-Kn limit and is not automatically accurate here.

</details>

**Exercise 5.** For the BGK gas, $\mu = p\tau$ and $`k = \frac{5}{2}R\,p\tau`$. Show that the Prandtl number $\mathrm{Pr} = \mu c_p/k$ of a monatomic BGK gas is 1. For argon at 1 atm and 300 K, $\mu = 2.27 \times 10^{-5}$ Pa s; what relaxation time does this imply, and what thermal conductivity would the BGK model predict? The measured value is about 0.0177 W/(m K).

<details>
<summary>Answer</summary>

For a monatomic gas $c_p = \frac{5}{2}R$, so $`\mathrm{Pr} = p\tau \cdot \frac{5}{2}R / (\frac{5}{2}R\,p\tau) = 1`$.

For argon, $\tau = \mu/p = 2.27 \times 10^{-5}/101325 \approx 2.24 \times 10^{-10}$ s. With $R = 208.1$ J/(kg K), the BGK conductivity is $k = \frac{5}{2} \times 208.1 \times 2.27 \times 10^{-5} \approx 0.0118$ W/(m K), about two thirds of the measured value. This is the Prandtl-number defect of the BGK model; the full Boltzmann operator gives $\mathrm{Pr} \approx 2/3$.

</details>

## References

- P. L. Bhatnagar, E. P. Gross and M. Krook, "A model for collision processes in gases. I. Small amplitude processes in charged and neutral one-component systems", *Physical Review* 94(3), 511–525, 1954.
- S. Chapman and T. G. Cowling, *The Mathematical Theory of Non-Uniform Gases*, 3rd ed., Cambridge University Press, 1970.
- C. Cercignani, *The Boltzmann Equation and Its Applications*, Springer, 1988.
- K. Huang, *Statistical Mechanics*, 2nd ed., Wiley, 1987.
- X. He and L.-S. Luo, "Theory of the lattice Boltzmann method: From the Boltzmann equation to the lattice Boltzmann equation", *Physical Review E* 56(6), 6811–6817, 1997.
- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
