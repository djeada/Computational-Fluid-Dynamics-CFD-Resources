# From Newton to Navier–Stokes

A gas is a collection of molecules obeying Newton's laws, yet engineers describe it by a handful of smooth fields. This note follows the chain of reduced descriptions that connects the two: molecular dynamics, the $N$-particle probability density, the one-particle distribution function of the Boltzmann equation, and finally the continuum equations. It defines the distribution function and shows which of its velocity moments are the density, momentum, energy, stress and heat flux. The evolution equation for the distribution function and the derivation of the Navier–Stokes closure follow in [The Boltzmann Equation](boltzmann_equation.md).

## Problem Statement

Consider $N$ identical molecules of mass $m$ with positions $\mathbf{x}_k(t)$ and velocities $\boldsymbol{\xi}_k(t)$, $k = 1, \ldots, N$, interacting through a pair potential $\phi(r)$:

$$
\frac{d\mathbf{x}_k}{dt} = \boldsymbol{\xi}_k,
\qquad m \frac{d\boldsymbol{\xi}_k}{dt} = -\sum_{l \neq k} \nabla
\phi\left(|\mathbf{x}_k - \mathbf{x}_l|\right) + \mathbf{F}_k^{\mathrm{ext}}
$$

One cubic millimetre of air holds about $2.5 \times 10^{16}$ molecules, so this system of $6N$ ordinary differential equations cannot be solved for any engineering flow. The goal is a reduced description in terms of a few fields, $\rho(\mathbf{x}, t)$, $\mathbf{u}(\mathbf{x}, t)$ and the specific internal energy $e(\mathbf{x}, t)$, that satisfies closed partial differential equations. The questions are which intermediate object carries enough information, how the macroscopic fields are defined from it, and which assumption is made at each step of the reduction.

## The Hierarchy of Descriptions

| Level | Unknown | Phase-space dimension | Equation | Assumption that leads to the next level |
| --- | --- | --- | --- | --- |
| Molecular dynamics | $\mathbf{x}_k$, $\boldsymbol{\xi}_k$ for all $k$ | $6N$ | Newton | statistical description of an ensemble of initial states |
| $N$-particle density | $F_N(\mathbf{x}_1, \boldsymbol{\xi}_1, \ldots, \mathbf{x}_N, \boldsymbol{\xi}_N, t)$ | $6N$ | Liouville (exact) | integrate out all but $s$ particles: BBGKY hierarchy |
| One-particle distribution | $f(\mathbf{x}, \boldsymbol{\xi}, t)$ | 6 | Boltzmann | dilute gas, binary collisions, molecular chaos $f_2 \approx f f$ |
| Continuum | $\rho$, $\mathbf{u}$, $e$ | 3 (physical space only) | Euler, Navier–Stokes | $\mathrm{Kn} \ll 1$: $f$ close to local equilibrium |

The steps are:

1. Instead of one trajectory, follow the probability density $F_N$ of an ensemble of systems. It is conserved along the trajectories of Newton's equations, which gives the Liouville equation, exact and linear in $6N$ dimensions.
2. Integrating the Liouville equation over all but one particle gives an equation for the one-particle density that involves the two-particle density $f_2$. The equation for $f_2$ involves $f_3$, and so on. This chain of equations, named after Bogoliubov, Born, Green, Kirkwood and Yvon, is still exact and still unclosed.
3. In a dilute gas the range of the intermolecular force is much smaller than the mean spacing, so collisions are binary and short. Boltzmann's molecular-chaos assumption states that two molecules about to collide are uncorrelated, $`f_2(\mathbf{x}, \boldsymbol{\xi}, \mathbf{x}, \boldsymbol{\xi}_\star) \approx f(\mathbf{x}, \boldsymbol{\xi}) f(\mathbf{x}, \boldsymbol{\xi}_\star)`$. This closes the hierarchy at the first level and gives the Boltzmann equation, with a nonlinear collision integral.
4. When the mean free path is much shorter than the flow scale, collisions keep $f$ near a local Maxwell–Boltzmann distribution. Its moments obey the Euler equations, and the first correction in Kn adds viscous stress and heat conduction (the Chapman–Enskog expansion).

There is a second route to lattice Boltzmann. Lattice-gas automata (Frisch, Hasslacher and Pomeau, 1986) move Boolean particles on a hexagonal lattice with collision rules that conserve mass and momentum, and their large-scale behaviour obeys the Navier–Stokes equations. The lattice Boltzmann equation was first obtained by replacing the Boolean occupation numbers with their ensemble averages, which removes the statistical noise (McNamara and Zanetti, 1988). It was later shown to be a discretisation of the Boltzmann equation with a simplified collision operator (He and Luo, 1997), which is the derivation used in [From Boltzmann to Lattice Boltzmann](from_boltzmann_to_lattice_boltzmann.md).

## The Distribution Function

The **distribution function** $f(\mathbf{x}, \boldsymbol{\xi}, t)$ is defined so that

```math
f(\mathbf{x}, \boldsymbol{\xi}, t)\, d^3x\, d^3\xi
```

is the expected mass of the molecules in the volume element $d^3x$ around $\mathbf{x}$ whose velocities lie in $d^3\xi$ around $\boldsymbol{\xi}$. Its units are kg s³/m⁶. Some texts count molecules instead of mass; the two differ by the factor $m$.

$f$ is a smooth function only if it is understood as an average. The averaging volume of side $\ell_{\mathrm{av}}$ must contain many molecules and be much larger than the mean free path $\lambda$, yet much smaller than the flow scale $L$:

$$
\lambda \ll \ell_{\mathrm{av}} \ll L
$$

For air at atmospheric conditions, a cube of side $\ell_{\mathrm{av}} = 10$ µm holds about $2.5 \times 10^{10}$ molecules, so statistical fluctuations are of relative size $10^{-5}$. It is also about 150 mean free paths wide, so this choice works for flows on scales of a millimetre and above.

![Microscopic and macroscopic views of a fluid](../../../scripts/plots/microscopic_view/microscopic_view.png)

The left panel shows the molecular picture and the right panel the continuum field obtained by averaging. In equilibrium the velocity part of $f$ is the Maxwell–Boltzmann distribution. Integrated over directions, it gives the distribution of molecular speeds shown below for nitrogen: the peak moves to higher speed and broadens as the temperature rises.

![Maxwell–Boltzmann speed distribution of nitrogen at four temperatures](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/probability_distribution_function.png)

## Macroscopic Fields as Moments

The continuum fields are velocity moments of $f$. With the peculiar (thermal) velocity $\mathbf{v} = \boldsymbol{\xi} - \mathbf{u}$,

| Quantity | Moment | Order |
| --- | --- | --- |
| Density | $`\rho = \int f \, d^3\xi`$ | 0 |
| Momentum density | $`\rho \mathbf{u} = \int \boldsymbol{\xi} f \, d^3\xi`$ | 1 |
| Internal energy density | $`\rho e = \frac{1}{2}\int \lvert\mathbf{v}\rvert^2 f \, d^3\xi`$ | 2 (trace) |
| Pressure tensor | $`\mathbf{P} = \int \mathbf{v}\mathbf{v} f \, d^3\xi`$ | 2 |
| Heat flux | $`\mathbf{q} = \frac{1}{2}\int \mathbf{v} \lvert\mathbf{v}\rvert^2 f \, d^3\xi`$ | 3 |

The temperature of a monatomic gas is defined by $e = \frac{3}{2}RT$, with $R = k_B/m$. The thermodynamic pressure is the mean normal stress, $`p = \frac{1}{3}\mathrm{tr}\,\mathbf{P} = \frac{2}{3}\rho e = \rho R T`$, which is the ideal-gas law. The deviatoric part of $\mathbf{P}$ is the viscous stress with the sign reversed, $\boldsymbol{\sigma}' = -(\mathbf{P} - p\mathbf{I})$.

The full second moment splits into a convective part and a thermal part, because $`\int \mathbf{v} f \, d^3\xi = 0`$:

```math
\int \boldsymbol{\xi}\boldsymbol{\xi} f \, d^3\xi = \rho\mathbf{u}\mathbf{u} +
\mathbf{P}
```

Mass, momentum and energy conservation then take the familiar continuum form, with $\mathbf{P}$ and $\mathbf{q}$ as fluxes ([The Boltzmann Equation](boltzmann_equation.md#collision-invariants-and-conservation-laws) derives them from the kinetic equation). These balance laws hold for any $f$, but they are not closed: $\mathbf{P}$ and $\mathbf{q}$ are further moments of $f$. Continuum mechanics closes them with constitutive laws (Newtonian stress, Fourier conduction) and measured coefficients. Kinetic theory derives both the form of these laws and the values of $\mu$ and $k$ from the collision model.

Lattice Boltzmann uses exactly this idea. It replaces $f$ with $Q$ discrete populations $f_i$ and keeps only enough velocities that the moments $\rho$, $\rho\mathbf{u}$ and $\mathbf{P}$ come out correctly; the heat flux and higher moments are not represented by the standard isothermal lattices.

## Key Takeaways

- Each level of description averages away information: Newton's equations to the Liouville equation (ensemble), then to the Boltzmann equation (molecular chaos, dilute gas), then to the continuum equations ($\mathrm{Kn} \ll 1$).
- $f(\mathbf{x}, \boldsymbol{\xi}, t)$ is the mass density in phase space, meaningful when averaged over volumes with $\lambda \ll \ell_{\mathrm{av}} \ll L$.
- $\rho$, $\rho\mathbf{u}$, $\rho e$, $\mathbf{P}$ and $\mathbf{q}$ are the moments of order 0 to 3 of $f$. The pressure is $`\mathrm{tr}\,\mathbf{P}/3`$ and the viscous stress is minus the deviatoric part of $\mathbf{P}$.
- The moment equations are exact but unclosed. Kinetic theory closes them near equilibrium, which is the route LBM follows on a lattice.

## Related Scripts

- [Microscopic vs. Macroscopic View of a Fluid](../../../scripts/plots/microscopic_view/): draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid.
- [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve.

## Exercises

**Exercise 1.** Air at $T = 293.15$ K and $p = 101325$ Pa behaves as an ideal gas with number density $n = p/(k_B T)$, where $k_B = 1.380649 \times 10^{-23}$ J/K. Compute $n$, the mean spacing between molecules $n^{-1/3}$, and the number of molecules in a cube of side 10 µm. Is this cube a reasonable averaging volume?

<details>
<summary>Answer</summary>

- $n = 101325 / (1.380649 \times 10^{-23} \times 293.15) \approx 2.50 \times 10^{25}$ m⁻³.
- Mean spacing $n^{-1/3} \approx 3.4 \times 10^{-9}$ m = 3.4 nm.
- A cube of side $10^{-5}$ m has volume $10^{-15}$ m³ and holds about $2.5 \times 10^{10}$ molecules.

Relative statistical fluctuations scale like $N^{-1/2} \approx 6 \times 10^{-6}$, which is negligible. The cube is also much larger than the mean free path (about 66 nm, Exercise 3). For a flow scale of about 1 mm or more it satisfies $\lambda \ll \ell_{\mathrm{av}} \ll L$.

</details>

**Exercise 2.** A one-dimensional "two-beam" gas has $f(\xi) = \rho_1 \delta(\xi - \xi_1) + \rho_2 \delta(\xi - \xi_2)$ with $\rho_1 = 0.6$ kg/m³ at $\xi_1 = 300$ m/s and $\rho_2 = 0.4$ kg/m³ at $\xi_2 = -200$ m/s. Compute $\rho$, $u$ and the momentum flux of the thermal motion $`P_{xx} = \int (\xi - u)^2 f \, d\xi`$.

<details>
<summary>Answer</summary>

- $\rho = 0.6 + 0.4 = 1.0$ kg/m³.
- $\rho u = 0.6 \times 300 + 0.4 \times (-200) = 100$ kg/(m² s), so $u = 100$ m/s.
- The peculiar velocities are $+200$ and $-300$ m/s, so $P_{xx} = 0.6 \times 200^2 + 0.4 \times 300^2 = 24000 + 36000 = 60000$ Pa.

This $f$ is far from a Maxwellian, but its moments still define a density, a velocity and a pressure-like stress.

</details>

**Exercise 3.** For nitrogen take a hard-sphere diameter $d = 0.37$ nm, with $T = 293.15$ K and $p = 101325$ Pa. Compute the mean free path $`\lambda = k_B T / (\sqrt{2}\,\pi d^2 p)`$ and the ratio $\lambda/L$ for $L = 1$ µm and $L = 1$ mm. For which scale is there room for an averaging volume with $\lambda \ll \ell_{\mathrm{av}} \ll L$?

<details>
<summary>Answer</summary>

$`\lambda = 1.380649 \times 10^{-23} \times 293.15 / (\sqrt{2}\,\pi \, (0.37 \times 10^{-9})^2 \times 101325) \approx 6.6 \times 10^{-8}`$ m (66 nm).

- For $L = 1$ µm the ratio is about 0.066. The scales are separated by a factor of only about 15, which leaves no room for an averaging volume, and the flow is in the slip regime.
- For $L = 1$ mm the ratio is about $6.6 \times 10^{-5}$. An averaging volume of about 10 µm is two orders of magnitude above $\lambda$ and two orders below $L$, so the continuum description is well founded.

</details>

**Exercise 4.** Show that $`\int (\boldsymbol{\xi} - \mathbf{u}) f \, d^3\xi = 0`$, and use it to prove $`\int \boldsymbol{\xi}\boldsymbol{\xi} f \, d^3\xi = \rho\mathbf{u}\mathbf{u} + \mathbf{P}`$. Which part becomes the convective flux of the momentum equation, and which becomes pressure and viscous stress?

<details>
<summary>Answer</summary>

$`\int (\boldsymbol{\xi} - \mathbf{u}) f \, d^3\xi = \rho\mathbf{u} - \mathbf{u}\rho = 0`$ by the definitions of density and momentum density.

Expand $\boldsymbol{\xi}\boldsymbol{\xi} = (\mathbf{u} + \mathbf{v})(\mathbf{u} + \mathbf{v}) = \mathbf{u}\mathbf{u} + \mathbf{u}\mathbf{v} + \mathbf{v}\mathbf{u} + \mathbf{v}\mathbf{v}$. Integrated against $f$, the cross terms vanish by the first result, leaving $\rho\mathbf{u}\mathbf{u} + \mathbf{P}$.

In the momentum balance $`\partial_t(\rho\mathbf{u}) + \nabla \cdot \int \boldsymbol{\xi}\boldsymbol{\xi} f \, d^3\xi = \ldots`$, the term $\rho\mathbf{u}\mathbf{u}$ gives the convective flux $\nabla \cdot (\rho\mathbf{u}\mathbf{u})$. The tensor $\mathbf{P}$ is the momentum carried by thermal motion. Its isotropic part is the pressure $`p = \mathrm{tr}\,\mathbf{P}/3`$, and its deviatoric part is minus the viscous stress, which the Chapman–Enskog expansion relates to velocity gradients.

</details>

**Exercise 5.** For the Maxwellian $`f = \rho\,(2\pi RT)^{-3/2} \exp(-\lvert\mathbf{v}\rvert^2/(2RT))`$, show that $\rho e = \frac{3}{2}\rho RT$ and $\mathbf{q} = 0$. Evaluate $e$ and $p$ for argon ($R = 208.1$ J/(kg K)) at $T = 300$ K and $\rho = 1.6$ kg/m³.

<details>
<summary>Answer</summary>

The Maxwellian factorises into three one-dimensional Gaussians in $v_x$, $v_y$, $v_z$, each with variance $RT$. Hence $`\int v_\alpha^2 f \, d^3\xi = \rho RT`$ and $`\rho e = \frac{1}{2}(3\rho RT)`$. The heat-flux integrand $v_\alpha \lvert\mathbf{v}\rvert^2 f$ is odd in $v_\alpha$, so $\mathbf{q} = 0$: a gas in local equilibrium conducts no heat, and heat conduction, like viscosity, comes from the departure from equilibrium.

For argon, $e = 1.5 \times 208.1 \times 300 \approx 9.36 \times 10^4$ J/kg and $p = 1.6 \times 208.1 \times 300 \approx 9.99 \times 10^4$ Pa.

</details>

## References

- S. Chapman and T. G. Cowling, *The Mathematical Theory of Non-Uniform Gases*, 3rd ed., Cambridge University Press, 1970.
- K. Huang, *Statistical Mechanics*, 2nd ed., Wiley, 1987.
- C. Cercignani, *The Boltzmann Equation and Its Applications*, Springer, 1988.
- U. Frisch, B. Hasslacher and Y. Pomeau, "Lattice-gas automata for the Navier-Stokes equation", *Physical Review Letters* 56(14), 1505–1508, 1986.
- G. R. McNamara and G. Zanetti, "Use of the Boltzmann equation to simulate lattice-gas automata", *Physical Review Letters* 61(20), 2332–2335, 1988.
- X. He and L.-S. Luo, "Theory of the lattice Boltzmann method: From the Boltzmann equation to the lattice Boltzmann equation", *Physical Review E* 56(6), 6811–6817, 1997.
- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
