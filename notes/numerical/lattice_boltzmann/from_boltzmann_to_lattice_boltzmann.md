# From Boltzmann to Lattice-Boltzmann

The Boltzmann equation forms the basis of kinetic theory by statistically describing the evolution of the distribution function $f(\xi, x, t)$ of particles in phase space. To numerically solve macroscopic fluid dynamics problems (i.e., the NSE) using a kinetic approach, one discretizes this continuous equation—leading to the Lattice-Boltzmann method (LBM). This mesoscopic approach simplifies the complicated collision dynamics while preserving necessary physics.

## 1. Discretization of the Distribution Function $f(\xi, x, t)$

In its continuous form, the distribution function $f(\xi, x, t)$ depends on position $x$, particle velocity $\xi$, and time $t$. For numerical computations, we must discretize all these variables.

### 1.1. Steps for Discretization

I. **Space:**

- **Discretize $x$:**\
  The spatial domain is divided into lattice points separated by a spacing $\Delta x$. Each lattice point represents a control volume over which fluid properties are averaged.

II. **Time:**

- **Discretize $t$:**\
  Time is partitioned into discrete time steps $\Delta t$. The simulation advances by updating the distribution function at each time step.

III. **Velocity Space:**

- **Discretize $\xi$:**\
  The continuous velocity space is approximated by a finite set of discrete velocities, resulting in a set of distribution functions $f_i(x, t)$ where the index $i$ labels the discrete velocities.

## 2. Velocity Space Discretization

The key to bridging kinetic theory and macroscopic fluid dynamics lies in how we treat the velocity space. For solving the NSE, we require only certain moments of the distribution function:

```math
\int d^3\xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3\xi \, \xi \,
f(\xi, x, t) = \rho(x, t)\,\mathbf{u}(x, t)
```

where $\rho(x, t)$ is the fluid density and $\mathbf{u}(x, t)$ is the macroscopic velocity. By replacing these integrals with sums—often helped by a Hermite expansion—we simplify the computation.

### 2.1. Discrete Velocity Sets

Two of the most common discrete velocity sets in LBM are:

- **D2Q9 (2D, 9 velocities):**
  For a two-dimensional simulation, the discrete velocities $c_i$ are often given by:

$$
(c_i) = \begin{pmatrix}
0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1
\end{pmatrix} \frac{\Delta x}{\Delta t}
$$

These nine velocities include a rest particle (zero velocity) and eight moving directions (cardinal and diagonal).

- **D3Q19 (3D, 19 velocities):**
  In three dimensions, a common set is the D3Q19 model:

$$
(c_i) = \begin{pmatrix}
0 & 1 & -1 & 0 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 0 & 0 & 1 & -1 & 1 & -1 & 0 & 0 \\
0 & 0 & 0 & 1 & -1 & 0 & 0 & 1 & -1 & 0 & 0 & 1 & -1 & -1 & 1 & 0 & 0 & 1 & -1 \\
0 & 0 & 0 & 0 & 0 & 1 & -1 & 0 & 0 & 1 & -1 & 1 & -1 & 0 & 0 & -1 & 1 & -1 & 1
\end{pmatrix} \frac{\Delta x}{\Delta t}
$$

This set comprises 19 discrete velocities that efficiently capture the directional propagation in three dimensions.

## 3. Detailed Steps in Using the Boltzmann Equation to Solve NSE

The Lattice-Boltzmann method proceeds through several key steps to simulate fluid dynamics:

### 3.1. Initialize the Distribution Function

- **Starting Point:**\
  At time $t=0$, assign an initial distribution $f_i(x, 0)$ at each lattice point. This function should reflect the initial fluid state (e.g., initial density, velocity).

### 3.2. Collision Step

- **Collision Operator:**\
  Apply a collision operator to the distribution functions at each lattice node. A common choice is the BGK (Bhatnagar-Gross-Krook) model:

$$
f_i^{\text{post}}(x, t) = f_i(x, t) - \frac{1}{\tau}
\Bigl(f_i(x, t) - f_i^{\text{eq}}(x, t) \Bigr)
$$

where $\tau$ is the relaxation time and $f_i^{\text{eq}}$ is the equilibrium distribution (often derived from the Maxwell-Boltzmann distribution).

### 3.3. Streaming Step

- **Propagation:**\
  After collisions, propagate (or "stream") the post-collision distribution functions along their respective discrete velocity directions:

$$
f_i(x + c_i \Delta t, t + \Delta t) = f_i^{\text{post}}(x, t)
$$

This streaming step moves information from one lattice point to its neighbors along the direction $c_i$.

### 3.4. Boundary Conditions

- **Handling Boundaries:**\
  Apply boundary conditions to account for interactions with walls or interfaces. Common strategies include bounce-back schemes (for no-slip boundaries) and various other methods for open or periodic boundaries.

### 3.5. Macroscopic Variables Calculation

- **Extracting Fluid Properties:**\
  Compute the macroscopic density and velocity from the moments of the distribution functions:

- **Density:**

$$
\rho(x, t) = \sum_i f_i(x, t)
$$

- **Velocity:**

```math
\mathbf{u}(x, t) = \frac{1}{\rho(x, t)} \sum_i c_i \, f_i(x, t)
```

### 3.6. Iterate

- **Time Advancement:**\
  Repeat the collision, streaming, boundary condition, and macroscopic variable calculation steps for each time step until the simulation reaches the desired final time.

## 4. Validation and Applications

### 4.1. Validation

- **Comparison with Experiments or Direct Simulations:**\
  Validate the LBM results by comparing them with experimental data or with solutions obtained from direct numerical simulation of the NSE. This step makes sure the reliability and accuracy of the LBM approach.

### 4.2. Applications

- **Wide-Ranging Uses:**\
  The Lattice-Boltzmann method has been successfully applied to simulate:

- Fluid flow in porous media.

- Multiphase and multicomponent flows.

- Thermal flows.

- Flows involving complicated boundary dynamics.

## 5. The Maxwell-Boltzmann Distribution

At equilibrium, the distribution function $f^{\text{eq}}(\xi, x, t)$ follows the Maxwell-Boltzmann distribution, which is given by:

```math
f^{\text{eq}}(\xi, x, t) = \rho \left(\frac{1}{2\pi RT} \right)^{3/2}
\exp\!\left(-\frac{|\xi - \mathbf{u}|^2}{2RT} \right)
```

### Explanation

- **Equilibrium State:**\
  This distribution describes the equilibrium state of a gas, with particle velocities following a specific statistical law.

- **Conservation Laws:**\
  The Maxwell-Boltzmann distribution makes sure the conservation of mass, momentum, and energy during collisions.

- **Isotropy:**\
  The equilibrium distribution is isotropic; it depends only on the magnitude $|\xi - \mathbf{u}|$ rather than on the direction.

- **Primary Variables:**\
  The key parameters are:

- $\rho$: Density.

- $\xi$: Molecular velocity.

- $\mathbf{u}$: Macroscopic (average) velocity.

- $T$: Temperature.

- $R$: Specific gas constant.
  By utilizing the Maxwell-Boltzmann distribution, the LBM captures the correct equilibrium properties, making sure that the simulated fluid behavior is physically accurate.

## 6. Using the Boltzmann Equation to Solve the Navier-Stokes Equations (NSE)

### 6.1. Key Ideas

- **Goal:**\
  Instead of directly solving the NSE for macroscopic variables like velocity $\mathbf{u}(x, t)$ and pressure $p(x, t)$, the LBM simulates the evolution of the distribution function $f(\xi, x, t)$. The macroscopic quantities are then extracted as moments of $f$.

- **Approach:**\
  The LBM uses a simplified version of the Boltzmann equation (via discretization in space, time, and velocity) to evolve $f_i(x, t)$ and recovers the NSE in the macroscopic limit (through Chapman-Enskog analysis).

- **Challenge:**\
  While the Boltzmann equation is more complicated than the NSE, its mesoscopic nature provides a more detailed description of fluid dynamics and lends itself to efficient, parallelizable algorithms.

### 6.2. Tasks for Carrying out the Boltzmann Equation

I. **Discretize the Distribution Function $f(\xi, x, t)$:**

- Convert the continuous phase-space variables into discrete sets for computation.

II. **Understand the Lattice-Boltzmann Equation (LBE):**

- Derive the LBE from the Boltzmann equation and carry out it in a numerical scheme.

III. **Link LBE and NSE:**

- Through moment analysis and appropriate approximations, demonstrate that the LBE recovers the macroscopic Navier-Stokes equations.

IV. **Validate the Method:**

- Compare LBM simulation results with experimental data or high-fidelity numerical solutions to confirm accuracy and robustness.

## 7. Summary Diagram

Below is a schematic diagram summarizing the process from the Boltzmann equation to the Lattice-Boltzmann method:

```plaintext
    +---------------------------+

    |      Boltzmann Equation   |
    |  (Continuous Distribution)|

    +-------------+-------------+

                  |

                  | Discretize: Space, Time,
                  | and Velocity (via Hermite expansion)
                  v
    +---------------------------+

    |   Lattice-Boltzmann Method|
    | (Discrete Distribution f_i)|

    +-------------+-------------+

                  |

                  | Collision & Streaming Steps
                  v
    +---------------------------+

    | Macroscopic Variables     |
    | (Density, Velocity, etc.) |

    +---------------------------+

                  |

                  v
    +---------------------------+

    |   Navier-Stokes Equations |
    |     (Recovered in limit)  |

    +---------------------------+

```

## Purpose in CFD

This note details how the continuous Boltzmann equation is discretized into the Lattice Boltzmann Equation (LBE). It covers the three discretization steps—space ($\Delta x$), time ($\Delta t$), and velocity (finite set $`\{c_i\}`$)—introduces common velocity sets (D2Q9, D3Q19), and derives the collision, streaming, and macroscopic-variable-extraction steps. The Maxwell–Boltzmann equilibrium distribution and the Chapman–Enskog link to the NSE are also presented.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Lattice spacing $\Delta x$, time step $\Delta t$, discrete velocity set (e.g., D2Q9), relaxation time $\tau$, initial/boundary conditions |
| **Outputs** | Post-collision distributions $f_i^{\text{post}}$, streamed distributions, macroscopic density $\rho = \sum_i f_i$, velocity $\mathbf{u} = \sum_i c_i f_i / \rho$ |

## Related Scripts

- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.
- [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve.

## Exercises

**Exercise 1.** A D2Q9 simulation uses $\Delta x = 1$ mm and $\Delta t = 0.1$ ms. Using the velocity matrix in Section 2.1, how many distinct particle speeds does the set contain, and what are they in m/s?

<details>
<summary>Answer</summary>

The lattice speed is $c = \Delta x/\Delta t = 10^{-3}/10^{-4} = 10$ m/s. The set has three distinct speeds: 0 for the rest particle ($i = 0$), $c = 10$ m/s for the four cardinal directions, and $`\sqrt{2}\,c \approx 14.14`$ m/s for the four diagonal directions.

</details>

**Exercise 2.** At one D2Q9 node, with the populations ordered as the columns of the velocity matrix ($i = 0, \ldots, 8$), the values in lattice units are $f = (0.40, 0.12, 0.10, 0.08, 0.10, 0.03, 0.02, 0.02, 0.03)$. Compute $\rho$ and $\mathbf{u}$.

<details>
<summary>Answer</summary>

The column order is $c_0 = (0,0)$, $c_1 = (1,0)$, $c_2 = (0,1)$, $c_3 = (-1,0)$, $c_4 = (0,-1)$, $c_5 = (1,1)$, $c_6 = (-1,1)$, $c_7 = (1,-1)$, $c_8 = (-1,-1)$.

- $\rho = \sum_i f_i = 0.90$.
- $\rho u_x = f_1 - f_3 + f_5 - f_6 + f_7 - f_8 = 0.12 - 0.08 + 0.03 - 0.02 + 0.02 - 0.03 = 0.04$.
- $\rho u_y = f_2 - f_4 + f_5 + f_6 - f_7 - f_8 = 0.10 - 0.10 + 0.03 + 0.02 - 0.02 - 0.03 = 0$.

So $\mathbf{u} = (0.04/0.90, 0) \approx (0.0444, 0)$ in lattice units.

</details>

**Exercise 3.** Using the collision rule of Section 3.2, compute $f_1^{\text{post}}$ for $f_1 = 0.12$ and $f_1^{\text{eq}} = 0.11$ with $\tau = 1$ and with $\tau = 0.8$. What does $\tau < 1$ do, and what kinematic viscosity (lattice units, $\nu = (\tau - 1/2)/3$) corresponds to each case?

<details>
<summary>Answer</summary>

- $\tau = 1$: $f_1^{\text{post}} = 0.12 - (0.12 - 0.11) = 0.11 = f_1^{\text{eq}}$. The population relaxes fully to equilibrium in one step; $\nu = 1/6 \approx 0.167$.
- $\tau = 0.8$: $f_1^{\text{post}} = 0.12 - 1.25 \times 0.01 = 0.1075$. The population overshoots past equilibrium (over-relaxation, $1 < 1/\tau < 2$); $\nu = 0.3/3 = 0.1$.

Smaller $\tau$ gives lower viscosity. As $\tau \to 1/2$ the viscosity tends to zero and the scheme becomes unstable.

</details>

**Exercise 4.** Show that the Maxwell–Boltzmann distribution of Section 5 satisfies $`\int f^{\text{eq}} \, d^3\xi = \rho`$ and $`\int |\xi - \mathbf{u}|^2 f^{\text{eq}} \, d^3\xi = 3\rho R T`$.

<details>
<summary>Answer</summary>

Substitute $\mathbf{v} = \xi - \mathbf{u}$. The exponential factorises into three one-dimensional Gaussians, each with $\int e^{-v_\alpha^2/(2RT)} dv_\alpha = (2\pi RT)^{1/2}$. Their product $(2\pi RT)^{3/2}$ cancels the prefactor, so the zeroth moment is $\rho$.

For the second moment, $|\mathbf{v}|^2 = v_x^2 + v_y^2 + v_z^2$. Each term contributes $\rho RT$, because the one-dimensional second moment is $RT$ times the normalisation. Hence

```math
\int |\xi - \mathbf{u}|^2 f^{\text{eq}} \, d^3\xi = 3\rho R T
```

and the thermal energy density $`\int \tfrac{1}{2}|\mathbf{v}|^2 f^{\text{eq}} \, d^3\xi = \tfrac{3}{2}\rho R T`$ is that of a monatomic ideal gas.

</details>

**Exercise 5.** Verify that the D3Q19 set in Section 2.1 contains one rest velocity, 6 velocities of length $\Delta x/\Delta t$ and 12 of length $`\sqrt{2}\,\Delta x/\Delta t`$, and that $\sum_i c_i = 0$. With weights $w_0 = 1/3$, $w_i = 1/18$ for the six face neighbours and $w_i = 1/36$ for the twelve edge neighbours, show that $\sum_i w_i c_{i\alpha} c_{i\beta} = c_s^2 \delta_{\alpha\beta}$ with $c_s^2 = 1/3$ in lattice units.

<details>
<summary>Answer</summary>

Reading the columns: $c_0 = 0$; columns 1–6 are $\pm e_x, \pm e_y, \pm e_z$ (squared length 1); columns 7–18 are the twelve vectors with exactly two entries equal to $\pm 1$ (squared length 2). Every vector appears together with its negative, so $\sum_i c_i = 0$.

For $\alpha = \beta = x$: the face vectors $\pm e_x$ contribute $2 \times 1/18 = 1/9$. The edge vectors with a nonzero $x$ entry are $(\pm 1, \pm 1, 0)$ and $(\pm 1, 0, \pm 1)$, eight vectors contributing $8 \times 1/36 = 2/9$. The total is $1/9 + 2/9 = 1/3$. The $y$ and $z$ directions give the same by symmetry.

For $\alpha = x$, $\beta = y$: only $(\pm 1, \pm 1, 0)$ contribute. $(1,1,0)$ and $(-1,-1,0)$ give $+1/36$ each, while $(1,-1,0)$ and $(-1,1,0)$ give $-1/36$ each, so the sum is zero. The weights also sum to $1/3 + 6/18 + 12/36 = 1$.

</details>

## References

- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
- S. Succi, *The Lattice Boltzmann Equation for Fluid Dynamics and Beyond*, Oxford University Press, 2001.
- Y. H. Qian, D. d'Humières and P. Lallemand, "Lattice BGK models for Navier-Stokes equation", *Europhysics Letters* 17(6), 1992.
- X. He and L.-S. Luo, "Theory of the lattice Boltzmann method: From the Boltzmann equation to the lattice Boltzmann equation", *Physical Review E* 56(6), 1997.
