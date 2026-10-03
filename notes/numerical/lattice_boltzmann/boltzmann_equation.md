# Introduction to the Boltzmann Equation

Fluid dynamics spans multiple scales—from the microscopic interactions of individual molecules to the macroscopic behavior described by the Navier-Stokes equations (NSE). The **Boltzmann equation** plays a central role in kinetic theory by statistically describing the evolution of a particle system. In doing so, it serves as an important bridge between molecular dynamics and continuum fluid mechanics.

## 1. Key Concepts

### 1.1. The Distribution Function $f(\xi, x, t)$

- **Definition:**\
  The distribution function

$$
f(\xi, x, t)
$$

represents the state of a particle system by quantifying the density of particles having velocity $\xi$ at position $x$ and time $t$.

- **Role:**\
  It encapsulates the statistical information about the microscopic state of the system and determines how the number of particles varies over space and time. In essence, $f(\xi, x, t)$ is the cornerstone of kinetic theory, linking microscopic particle dynamics with macroscopic observables.

### 1.2. Evolution of $f(\xi, x, t)$

- **Particle Advection and Collisions:**\
  The evolution of the distribution function is governed by two major processes:

I. **Advection:** Particles move in space following their velocities.

II. **Collisions:** Interactions among particles change their velocities, driving the system toward equilibrium.

- **The Boltzmann Equation:**\
  The time evolution of $f(\xi, x, t)$ is described by the Boltzmann equation:

$$
\frac{\partial f}{\partial t} + \xi \cdot \nabla_x f + F \cdot \nabla_\xi
f = \left(\frac{\partial f}{\partial t} \right)_{\text{collision}}
$$

where:

- $\frac{\partial f}{\partial t}$ is the local time derivative.
- $\xi \cdot \nabla_x f$ accounts for the transport (or advection) of particles.
- $F \cdot \nabla_\xi f$ includes the influence of external forces $F$ acting on the particles.
- $\left( \frac{\partial f}{\partial t} \right)_{\text{collision}}$ represents the collision operator, modeling the effects of particle interactions.

## 2. Significance of the Boltzmann Equation

### 2.1. Connection to the Navier-Stokes Equations

- **Chapman-Enskog Analysis:**\
  Through the Chapman-Enskog expansion, one can derive the macroscopic Navier-Stokes equations from the Boltzmann equation. This derivation demonstrates that, under appropriate limits (e.g., small Knudsen numbers), the microscopic kinetic description recovers the familiar continuum fluid dynamics.

- **Bridging Scales:**\
  While the NSE capture the large-scale behavior of fluids, the Boltzmann equation provides insight into how microscopic interactions and non-equilibrium effects give rise to macroscopic transport phenomena like viscosity and thermal conductivity.

### 2.2. A Mesoscopic Perspective

- **More Detailed Physics:**\
  The Boltzmann equation retains necessary kinetic details—such as particle collisions and non-equilibrium distributions—that are typically absent in purely macroscopic descriptions. This level of detail can be particularly important for flows with high gradients or rarefied gas dynamics.

- **Eliminating Redundant Microscopic Details:**\
  By statistically averaging over many particles, the Boltzmann framework removes unnecessary complexities while still capturing the key dynamics needed to describe fluid behavior.

## 3. The Collision Operator

The collision term in the Boltzmann equation is important because it quantifies how particle collisions redistribute velocities and drive the system toward equilibrium.

### 3.1. Detailed Collision Integral

A typical form of the collision operator is:

$$
\left(\frac{\partial f}{\partial t} \right)_{\text{collision}} = \iint
g(\mathbf{v}, \Omega)
\left[f(\mathbf{x}, \mathbf{p}_A', t) f(\mathbf{x}, \mathbf{p}_B', t) - f(\mathbf{x},
\mathbf{p}_A, t) f(\mathbf{x}, \mathbf{p}_B, t) \right] d\Omega \, d^3\mathbf{p}_B
$$

where:

- $g(\mathbf{v}, \Omega)$ is the collision kernel that encapsulates the probability of collisions as a function of relative velocity and scattering angle.
- $\mathbf{p}_A$ and $\mathbf{p}_B$ are the momenta of particles before collision.
- $\mathbf{p}_A'$ and $\mathbf{p}_B'$ are the momenta after collision.
  This integral generally involves complicated double integrations over velocity space and scattering angles, making it the most challenging part of the Boltzmann equation.

### 3.2. Simplification with the BGK Model

To simplify the collision operator, the **Bhatnagar-Gross-Krook (BGK) model** is often used:

$$
\left(\frac{\partial f}{\partial t} \right)_{\text{collision}} = -\frac{1}{\tau}
\left(f - f^{\text{eq}} \right)
$$

- **Interpretation:**\
  This model assumes that the distribution function $f$ relaxes toward a local equilibrium distribution $f^{\text{eq}}$ over a characteristic relaxation time $\tau$.

- **Advantages:**\
  The BGK model significantly simplifies the collision term while still capturing necessary relaxation dynamics, making it highly amenable to numerical implementation—particularly in the Lattice-Boltzmann method.

## 4. Velocities in Relating to motion Theory

Understanding various velocity definitions is important for linking microscopic particle behavior with macroscopic fluid dynamics.

### 4.1. Molecular (Absolute) Velocity $\boldsymbol{\xi}$

- **Definition:**\
  $\xi$ represents the instantaneous velocity of an individual molecule. It is the primary variable in the kinetic description.

### 4.2. Average (Macroscopic) Velocity $\mathbf{u}$

- **Definition:**\
  The average velocity $\mathbf{u}$ of the fluid is obtained by taking the first moment of the distribution function:

$$
\mathbf{u} = \frac{1}{\rho} \int d^3\xi \, \xi \, f(\xi, x, t)
$$

where the density $\rho$ is defined below.

- **Significance:**\
  This velocity is the same as the one used in the Navier-Stokes equations to describe the flow field.

### 4.3. Relative Velocity $\mathbf{v}$

- **Definition:**\
  The relative velocity is given by:

$$
\mathbf{v} = \xi - \mathbf{u}
$$

which represents the deviation of individual molecular velocities from the average flow velocity.

- **Role:**\
  The relative velocity is important for computing higher-order moments such as pressure and viscous stresses.

## 5. Extracting Macroscopic Quantities: Moments of $f(\xi, x, t)$

The beauty of the Boltzmann framework is that macroscopic fluid properties emerge naturally from the moments of the distribution function.

### 5.1. Normalization and Mass Conservation

- **Total Mass:**\
  The overall mass in a control volume $\ell_{\text{av}}^3$ is given by:

$$
\int d^3\xi \int d^3x \, f(\xi, x, t) = M(t)
$$

### 5.2. Fluid Density

- **Local Density:**\
  The density at a specific location $x$ is the zeroth moment of $f$:

$$
\int d^3\xi \, f(\xi, x, t) = \rho(x, t)
$$

### 5.3. Momentum Density

- **Local Momentum:**\
  The first moment yields the momentum density:

$$
\int d^3\xi \, \xi \, f(\xi, x, t) = \rho(x, t) \, \mathbf{u}(x, t)
$$

### 5.4. Pressure and Stress Tensor

- **Higher Moments:**\
  The second moment (and beyond) of $f$ is related to the pressure and viscous stress tensor:

$$
\int d^3\xi \, \xi \otimes \xi \, f(\xi, x, t) \quad
\text{(leads to the pressure tensor)}
$$

Although the full expression is more complicated, it is important for recovering the constitutive relations used in the NSE.

## 6. From Boltzmann to Navier-Stokes: A Practical Overview

### 6.1. Objective

The ultimate goal is to use the Boltzmann equation to solve for macroscopic variables (e.g., $\mathbf{u}(x, t)$ and $p(x, t)$) as governed by the Navier-Stokes equations. Instead of directly solving the continuum equations, one simulates the evolution of the distribution function $f(\xi, x, t)$.

### 6.2. Advantages and Challenges

- **Advantages:**

- **Enhanced Physical Detail:**\
  The kinetic approach inherently captures non-equilibrium effects and particle-level dynamics.

- **Numerical Efficiency:**\
  Methods such as the Lattice-Boltzmann Equation (LBE) discretize both velocity and space, leading to algorithms that are highly parallelizable and simple to carry out.

- **Natural Emergence of Macroscopic Laws:**\
  Through appropriate moment calculations (and via Chapman-Enskog expansion), the macroscopic Navier-Stokes equations are recovered.

- **Challenges:**

- **High Dimensionality:**\
  The Boltzmann equation is posed in a high-dimensional phase space (position and velocity), requiring careful discretization.

- **Complicated Collision Operators:**\
  Accurate modeling of the collision term is computationally demanding, which is why simplified models like BGK are often used.

### 6.3. Tasks for Carrying out the Boltzmann Equation

I. **Discretize the Distribution Function:**

Convert the continuous variables $x$ and $\xi$ into discrete counterparts, leading to computationally efficient representations.

II. **Develop the Lattice-Boltzmann Equation (LBE):**

Derive and carry out the LBE as a discretized version of the Boltzmann equation that is tailored for fluid flow simulations.

III. **Link LBE with NSE:**

Demonstrate through theoretical analysis and numerical experiments that the LBE recovers the macroscopic Navier-Stokes equations in the appropriate limits.

IV. **Validation:**

Validate the numerical method by comparing simulation results with analytical solutions or experimental data.

## 7. Diagram: The Flow from Microscopic Kinetics to Macroscopic Fluid Dynamics

Below is a schematic diagram illustrating the hierarchy of models and the role of the Boltzmann equation:

```plaintext
+----------------------+       +--------------------+        +-----------------------+

|    Molecular/MD      | --->  |     Boltzmann      | --->   |     Navier-Stokes     |
| (Newton's Laws at    |       |   Equation (BE)    |        | Equations (NSE) / CFD |
|  microscopic scale)  |       |                    |        |                       |

+----------------------+       +--------------------+        +-----------------------+
     ^                              |
     |                              v
     |                      +------------------+

     |                      |   Lattice-       |

     +----------------------|   Boltzmann      |

                            |   Method (LBM)   |

                            +------------------+

```

*The diagram emphasizes how the Lattice-Boltzmann method sits at the mesoscopic level, bridging microscopic particle dynamics and macroscopic fluid behavior.*

## Purpose in CFD

The Boltzmann equation is the kinetic-theory foundation of the Lattice Boltzmann Method. This note defines the distribution function $f(\xi, x, t)$, derives the Boltzmann transport equation (advection + external forces + collisions), introduces the BGK collision model, and shows how macroscopic quantities (density, momentum, pressure) emerge as moments of $f$. Understanding these concepts is essential before discretizing the equation on a lattice.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Distribution function $f(\xi, x, t)$, external force $F$, collision kernel $g(\mathbf{v}, \Omega)$, relaxation time $\tau$ |
| **Outputs** | Macroscopic density $\rho = \int f\,d^3\xi$, momentum $\rho\mathbf{u} = \int \xi f\,d^3\xi$, pressure tensor (second moment), equilibrium distribution $f^{\text{eq}}$ |

## Related Scripts

- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude with Matplotlib.
- [Maxwell-Boltzmann Speed Distribution of N₂ Molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve.
- [Microscopic vs. Macroscopic View of a Fluid](../../../scripts/plots/microscopic_view/): draws two side-by-side panels that contrast the microscopic (molecular) and macroscopic (continuum) views of a fluid.

## Exercises

**Exercise 1.** A spatially homogeneous gas with no external force evolves under the BGK model toward a constant equilibrium $f^{\text{eq}}$. Solve for $f(t)$ with $f(0) = f_0$, and find the fraction of the initial departure from equilibrium, $f_0 - f^{\text{eq}}$, that remains at $t = 3\tau$.

<details>
<summary>Answer</summary>

With no spatial gradients and $F = 0$ the Boltzmann equation reduces to $\partial f/\partial t = -(f - f^{\text{eq}})/\tau$. Writing $g = f - f^{\text{eq}}$ gives $dg/dt = -g/\tau$, so

```math
f(t) = f^{\text{eq}} + \left(f_0 - f^{\text{eq}}\right) e^{-t/\tau}
```

At $t = 3\tau$ the remaining fraction is $e^{-3} \approx 0.0498$, about 5%. The relaxation time $\tau$ is the e-folding time of the approach to equilibrium.

</details>

**Exercise 2.** Show that the BGK collision term conserves mass and momentum at every point only if the equilibrium has the same density and momentum as $f$, that is $\int f^{\text{eq}} \, d^3\xi = \rho$ and $\int \xi \, f^{\text{eq}} \, d^3\xi = \rho \mathbf{u}$.

<details>
<summary>Answer</summary>

The rate of change of density due to collisions is the zeroth moment of the collision term:

```math
\int \left(\frac{\partial f}{\partial t} \right)_{\text{collision}}
d^3\xi = -\frac{1}{\tau} \left(\rho - \int f^{\text{eq}} \, d^3\xi \right)
```

This vanishes for every $f$ only if $\int f^{\text{eq}} \, d^3\xi = \rho$. The first moment gives $-\frac{1}{\tau}\left(\rho\mathbf{u} - \int \xi f^{\text{eq}} \, d^3\xi\right)$, which vanishes only if $\int \xi f^{\text{eq}} \, d^3\xi = \rho\mathbf{u}$. So $f^{\text{eq}}$ must be built from the local $\rho$ and $\mathbf{u}$ of $f$ itself (and from the local temperature, if energy is also to be conserved). The Maxwell–Boltzmann distribution evaluated with the local $\rho$, $\mathbf{u}$ and $T$ satisfies these constraints.

</details>

**Exercise 3.** In one velocity dimension the Maxwellian is $f^{\text{eq}}(\xi) = \rho \, (2\pi RT)^{-1/2} \exp\left(-(\xi - u)^2/(2RT)\right)$. Compute its zeroth, first and second moments, and use the relative velocity $v = \xi - u$ to show that the pressure is $p = \rho R T$. Evaluate $p$ for air with $\rho = 1.2$ kg/m³, $R = 287$ J/(kg K) and $T = 300$ K.

<details>
<summary>Answer</summary>

Substitute $v = \xi - u$ and use the Gaussian integrals $\int e^{-v^2/(2RT)} dv = \sqrt{2\pi RT}$, $\int v \, e^{-v^2/(2RT)} dv = 0$ and $\int v^2 e^{-v^2/(2RT)} dv = RT\sqrt{2\pi RT}$:

```math
\int f^{\text{eq}} d\xi = \rho,
\qquad \int \xi f^{\text{eq}} d\xi = \rho u,
\qquad \int \xi^2 f^{\text{eq}} d\xi = \rho u^2 + \rho R T
```

The pressure is the second moment of the relative velocity, $p = \int v^2 f^{\text{eq}} \, dv = \rho R T$, which is the ideal gas law. In three dimensions each diagonal component gives the same value, $\int \mathbf{v} \otimes \mathbf{v} \, f^{\text{eq}} \, d^3\xi = \rho R T \, \mathbf{I}$.

For the given air: $p = 1.2 \times 287 \times 300 = 103320$ Pa $\approx 1.03 \times 10^5$ Pa.

</details>

**Exercise 4.** The Knudsen number $\mathrm{Kn} = \ell_{\text{mfp}}/\ell$ indicates whether a continuum description is valid. A common classification is $\mathrm{Kn} < 0.01$ continuum, $0.01 < \mathrm{Kn} < 0.1$ slip flow, $0.1 < \mathrm{Kn} < 10$ transitional and $\mathrm{Kn} > 10$ free molecular. Air at atmospheric conditions has $\ell_{\text{mfp}} \approx 68$ nm. Classify flow through a channel of width (a) 10 µm and (b) 100 nm, and say whether the NSE or a Boltzmann-level description is needed.

<details>
<summary>Answer</summary>

(a) $\mathrm{Kn} = 68 \times 10^{-9} / 10 \times 10^{-6} = 6.8 \times 10^{-3}$. This is in the continuum range (close to the slip threshold), so the NSE with no-slip walls are adequate.

(b) $\mathrm{Kn} = 68 \times 10^{-9} / 100 \times 10^{-9} = 0.68$. This is transitional flow. The Chapman–Enskog expansion behind the NSE assumes small Kn, so a kinetic description (the Boltzmann equation, solved for example by DSMC or a discrete-velocity method) is needed. A standard low-order lattice Boltzmann model is also designed for the small-Kn limit and is not automatically accurate here.

</details>

## References

- P. L. Bhatnagar, E. P. Gross and M. Krook, "A model for collision processes in gases. I. Small amplitude processes in charged and neutral one-component systems", *Physical Review* 94(3), 1954.
- C. Cercignani, *The Boltzmann Equation and Its Applications*, Springer, 1988.
- S. Chapman and T. G. Cowling, *The Mathematical Theory of Non-Uniform Gases*, 3rd ed., Cambridge University Press, 1970.
- T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva and E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.
