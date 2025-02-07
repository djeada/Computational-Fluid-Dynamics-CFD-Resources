# From Boltzmann to Lattice-Boltzmann

The Boltzmann equation forms the basis of relating to motion theory by statistically describing the evolution of the distribution function $f(\xi, x, t)$ of particles in phase space. To numerically solve macroscopic fluid dynamics problems (i.e., the NSE) using a relating to motion approach, one discretizes this continuous equation—leading to the Lattice-Boltzmann method (LBM). This mesoscopic approach simplifies the complicated collision dynamics while preserving necessary physics.

## 1. Discretization of the Distribution Function $f(\xi, x, t)$

In its continuous form, the distribution function $f(\xi, x, t)$ depends on position $x$, particle velocity $\xi$, and time $t$. For numerical computations, we must discretize all these variables.

### 1.1. Steps for Discretization

I. **Space:**  

- **Discretize $x$:**  
 The spatial domain is divided into lattice points separated by a spacing $\Delta x$. Each lattice point represents a control volume over which fluid properties are averaged.

II. **Time:**  

- **Discretize $t$:**  
 Time is partitioned into discrete time steps $\Delta t$. The simulation advances by updating the distribution function at each time step.

III. **Velocity Space:**  

- **Discretize $\xi$:**  
 The continuous velocity space is approximated by a finite set of discrete velocities, resulting in a set of distribution functions $f_i(x, t)$ where the index $i$ labels the discrete velocities.

## 2. Velocity Space Discretization

The key to bridging relating to motion theory and macroscopic fluid dynamics lies in how we treat the velocity space. For solving the NSE, we require only certain moments of the distribution function:

$$\int d^3\xi , f(\xi, x, t) = \rho(x, t), \quad \int d^3\xi , \xi, f(\xi, x, t) = \rho(x, t),\mathbf{u}(x, t)$$

where $\rho(x, t)$ is the fluid density and $\mathbf{u}(x, t)$ is the macroscopic velocity. By replacing these integrals with sums—often helped by a Hermite expansion—we simplify the computation.

### 2.1. Discrete Velocity Sets

Two of the most common discrete velocity sets in LBM are:

- **D2Q9 (2D, 9 velocities):**
For a two-dimensional simulation, the discrete velocities $c_i$ are often given by:

$$(c_i) = \begin{pmatrix}
0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1
\end{pmatrix} \Delta x$$

These nine velocities include a rest particle (zero velocity) and eight moving directions (cardinal and diagonal).

- **D3Q19 (3D, 19 velocities):**
In three dimensions, a common set is the D3Q19 model:

$$(c_i) = \begin{pmatrix}
0 & 1 & -1 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & -1 & 0 & 1 & 1 & -1 & -1 & 0 & 0 & 1 & 1 & -1 & -1 & 1 & 1 & -1 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & -1 & 1 & 1
\end{pmatrix} \Delta t$$

This set comprises 19 discrete velocities that efficiently capture the directional propagation in three dimensions.

## 3. Detailed Steps in Using the Boltzmann Equation to Solve NSE

The Lattice-Boltzmann method proceeds through several key steps to simulate fluid dynamics:

### 3.1. Initialize the Distribution Function

- **Starting Point:**  
At time $t=0$, assign an initial distribution $f_i(x, 0)$ at each lattice point. This function should reflect the initial fluid state (e.g., initial density, velocity).

### 3.2. Collision Step

- **Collision Operator:**  
Apply a collision operator to the distribution functions at each lattice node. A common choice is the BGK (Bhatnagar-Gross-Krook) model:

$$f_i^{\text{post}}(x, t) = f_i(x, t) - \frac{1}{\tau} \Bigl( f_i(x, t) - f_i^{\text{eq}}(x, t) \Bigr)$$

where $\tau$ is the relaxation time and $f_i^{\text{eq}}$ is the equilibrium distribution (often derived from the Maxwell-Boltzmann distribution).

### 3.3. Streaming Step

- **Propagation:**  
After collisions, propagate (or "stream") the post-collision distribution functions along their respective discrete velocity directions:

$$f_i(x + c_i \Delta t, t + \Delta t) = f_i^{\text{post}}(x, t)$$

This streaming step moves information from one lattice point to its neighbors along the direction $c_i$.

### 3.4. Boundary Conditions

- **Handling Boundaries:**  
Apply boundary conditions to account for interactions with walls or interfaces. Common strategies include bounce-back schemes (for no-slip boundaries) and various other methods for open or periodic boundaries.

### 3.5. Macroscopic Variables Calculation

- **Extracting Fluid Properties:**  
Compute the macroscopic density and velocity from the moments of the distribution functions:

- **Density:**
$$\rho(x, t) = \sum_i f_i(x, t)$$

- **Velocity:**
$$\mathbf{u}(x, t) = \frac{1}{\rho(x, t)} \sum_i c_i , f_i(x, t)$$

### 3.6. Iterate

- **Time Advancement:**  
Repeat the collision, streaming, boundary condition, and macroscopic variable calculation steps for each time step until the simulation reaches the desired final time.

## 4. Validation and Applications

### 4.1. Validation

- **Comparison with Experiments or Direct Simulations:**  
Validate the LBM results by comparing them with experimental data or with solutions obtained from direct numerical simulation of the NSE. This step makes sure the reliability and accuracy of the LBM approach.

### 4.2. Applications

- **Wide-Ranging Uses:**  
The Lattice-Boltzmann method has been successfully applied to simulate:

- Fluid flow in porous media.
- Multiphase and multicomponent flows.
- Thermal flows.
- Flows involving complicated boundary dynamics.

## 5. The Maxwell-Boltzmann Distribution

At equilibrium, the distribution function $f^{\text{eq}}(\xi, x, t)$ follows the Maxwell-Boltzmann distribution, which is given by:

$$f^{\text{eq}}(\xi, x, t) = \rho \left( \frac{1}{2\pi RT} \right)^{3/2} \exp\!\left( -\frac{|\xi - \mathbf{u}|^2}{2RT} \right)$$

### Explanation

- **Equilibrium State:**  
This distribution describes the equilibrium state of a gas, with particle velocities following a specific statistical law.

- **Conservation Laws:**  
The Maxwell-Boltzmann distribution makes sure the conservation of mass, momentum, and energy during collisions.

- **Isotropy:**  
The equilibrium distribution is isotropic; it depends only on the magnitude $|\xi - \mathbf{u}|$ rather than on the direction.

- **Primary Variables:**  
The key parameters are:

- $\rho$: Density.
- $\xi$: Molecular velocity.
- $\mathbf{u}$: Macroscopic (average) velocity.
- $T$: Temperature.
- $R$: Specific gas constant.
By utilizing the Maxwell-Boltzmann distribution, the LBM captures the correct equilibrium properties, making sure that the simulated fluid behavior is physically accurate.

## 6. Using the Boltzmann Equation to Solve the Navier-Stokes Equations (NSE)

### 6.1. Key Ideas

- **Goal:**  
Instead of directly solving the NSE for macroscopic variables like velocity $\mathbf{u}(x, t)$ and pressure $p(x, t)$, the LBM simulates the evolution of the distribution function $f(\xi, x, t)$. The macroscopic quantities are then extracted as moments of $f$.

- **Approach:**  
The LBM uses a simplified version of the Boltzmann equation (via discretization in space, time, and velocity) to evolve $f_i(x, t)$ and recovers the NSE in the macroscopic limit (through Chapman-Enskog analysis).

- **Challenge:**  
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

