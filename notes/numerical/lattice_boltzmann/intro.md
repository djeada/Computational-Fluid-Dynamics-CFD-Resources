# Navier-Stokes Equations (NSE)

## Challenges of Solving NSE Analytically

1. **Non-Linearity:**
   - The Navier-Stokes equations are non-linear in the velocity field $u$.
   - Mathematical representation:
     
$$
     \rho \left( \frac{\partial u}{\partial t} + (u \cdot 
abla)u \right) = -
abla p + \eta 
abla^2 u + f
     $$

   - Non-linearity arises from the convective term $(u \cdot 
abla)u$.

2. **Partial Differential Equations (PDEs):**
   - NSE are PDEs, which are inherently more complex to solve than ordinary differential equations (ODEs).
   - Solutions require consideration of spatial and temporal variations.

3. **Boundary Conditions:**
   - Accurate solutions necessitate proper application of boundary conditions, which can be complex and varied depending on the problem domain.

# Computational Fluid Dynamics (CFD)

## Numerical Methods in CFD

1. **Finite Difference Method:**
   - Approximates derivatives using difference equations.
   - Simple implementation but may require fine meshing for accuracy.

2. **Finite Volume Method:**
   - Conserves quantities like mass, momentum, and energy by integrating over control volumes.
   - Widely used in industry due to its balance of accuracy and computational efficiency.

3. **Spectral Methods:**
   - Use global functions (e.g., Fourier series) to approximate solutions.
   - Highly accurate for problems with smooth solutions but can be computationally intensive.

4. **Finite Element Method (FEM):**
   - Divides the domain into smaller sub-domains (elements) and uses variational methods to solve.
   - Particularly useful for complex geometries and boundary conditions.

# Common Issues with CFD

1. **Mesh Generation:**
   - Creating a computational grid (mesh) that accurately represents the geometry of the problem domain.
   - Quality of mesh significantly affects solution accuracy and convergence.

2. **Boundary Conditions:**
   - Properly defining and implementing boundary conditions is critical for accurate simulations.
   - Common types include Dirichlet, Neumann, and mixed boundary conditions.

3. **Poisson Pressure Equation:**
   - The pressure field is obtained by solving the Poisson equation:
     
$$
     
abla^2 p = f(u)
     $$

   - Ensuring numerical stability and accuracy in solving this equation is a common challenge.


## Alternative Perspectives in Fluid Mechanics

### Representative Elementary Volume (REV) vs. Fluid Particle
- **REV:**
  - Conceptual volume over which fluid properties are averaged.
  - Facilitates macroscopic analysis of fluid behavior.
- **Fluid Particle:**
  - Infinitesimal volume element used to study flow properties at specific points.
  - Represents microscopic analysis in fluid mechanics.

### Transition from Microscopic to Macroscopic Analysis
- REV helps in transitioning from detailed molecular-level analysis to a broader, averaged-out perspective suitable for practical engineering problems.

## Collisions and Mean Free Path

### Thermal Motion of Molecules
- **Example: Argon at Room Temperature**
  - Thermal velocity ($v_{\text{th}}$): Approximately 400 m/s.
  - Thermal velocity squared ($\left\langle v_{\text{th}}^2 \right\rangle$): Given by $\frac{3kT}{m}$.

### Number Density
- Number of molecules per unit volume:
  - $n/V = \frac{p}{RT} \approx 40 \, \text{mol/m}^3$.
- **Atomic Radius:** $\ell_a \approx 0.1 \, \text{nm}$.
- **Mean Free Path:** Average distance between molecular collisions, $\ell_{\text{mfp}} \approx 3 \, \text{nm}$.

### Time Scales
- **Collision Time ($t_c$)**: 
  - Time between molecular collisions.
  - $t_c = \ell_a / v_{\text{th}} \approx 0.3 \, \text{ps}$.
- **Mean Free Path Time ($t_{\text{mfp}}$)**:
  - Time to travel the mean free path distance.
  - $t_{\text{mfp}} = \ell_{\text{mfp}} / v_{\text{th}} \approx 10 \, \text{ps}$.

## Macroscopic Fluids: Continuum Assumption

### Key Points
- **Scale Separation**: 
  - Macroscopic scales ($\ell$) are much larger than mean free path ($\ell_{\text{mfp}}$).
- **Continuum Hypothesis**: 
  - Fluids are treated as continuous fields with properties such as velocity ($u$), pressure ($p$), and density ($\rho$).
- **Coarse-Graining**:
  - Averaging microscopic properties to obtain macroscopic fields.
- **Conservation Equations**:
  - Govern fluid behavior at macroscopic scale.
  - Include continuity equation and Navier-Stokes equations (NSE).

## Scale Comparison: Micro, Meso, Macro

|          | **Micro**                    | **Meso**                         | **Macro**         |
|----------|------------------------------|----------------------------------|-------------------|
| **Scale**| $10^{-9} \, \text{m}$      | $10^{-9} - 10^{-6} \, \text{m}$| $> 10^{-6} \, \text{m}$ |
| **Physics** | Molecular                 | Probabilistic                    | Continuous        |
| **Governing Equations** | Newton's Laws  | Boltzmann Equation               | Navier-Stokes Equations (NSE) |
| **Numerical Methods** | Molecular Dynamics (MD) | Direct Simulation Monte Carlo (DSMC) | Computational Fluid Dynamics (CFD) |


# Numerical Modelling

## Process Flow:

```
                     +-----------+ 
       ------------> | "Reality" |  
       |             +-----------+  
       |                   |      
       |                   v 
       |             +----------------+                       
       |             | Physical model |                       
       |             +----------------+                       
       |                   |                                 
       |                   v                                  
+------------+       +--------------------+    
| validation |       | Mathematical model | <----------------
+------------+       +--------------------+                 |
       ^                   |                                |
       |                   v                                |
       |             +------------------+           +--------------+
       |             | Numerical model  |           | verification |
       |             +------------------+           +--------------+
       |                   |                                ^
       |                   v                                |
       |             +-------------+                        |
       --------------| Simulation  | ------------------------
                     +-------------+ 
```               

### Explanation:

1. **Reality**:
   - The starting point, representing the actual physical system or phenomenon being studied.

2. **Physical Model**:
   - Conceptualization of reality into a simplified version, capturing essential physical aspects.

3. **Mathematical Model**:
   - Formalization of the physical model into mathematical equations and expressions.

4. **Numerical Model**:
   - Discretization of the mathematical model to make it suitable for numerical computation.

5. **Simulation**:
   - Implementation and programming of the numerical model to perform simulations.

6. **Verification**:
   - Ensuring the numerical model accurately solves the mathematical model.

7. **Validation**:
   - Ensuring the mathematical model accurately represents reality.



# From Newton to Navier-Stokes

## Lattice-Boltzmann Approach
- The Lattice-Boltzmann method was designed to solve the Navier-Stokes equations rather than the Boltzmann equation.

### Key Questions:
- Can we use a mesoscopic approach to solve the Navier-Stokes equations (NSE)?
- Would this offer advantages?

### Transition Diagram:


```
+------------+        +-------------+          +---------------+               +-------+
| Newton/MD  +------->+  Boltzmann  +--------->+ Navier-Stokes | <-----------> +  CFD  +
+------------+        +-------------+          +---------------+               +-------+
      |                      |                         ^
      v                      v                         |
+------------+        +----------------+               |
| Lattice    +------->+ Lattice        +---------------+
| Gas        |        | Boltzmann      |
+------------+        +----------------+
```



## Probability Distribution Function

### Simplifying Microscopic Details:
- **Objective:** Eliminate unimportant microscopic details while retaining essential macroscopic behavior.

### Key Points:
- **Averaging Molecules in Small Volumes:**
  - The scale of averaging ($\ell_{\text{av}}$) is much larger than the mean free path ($\ell_{\text{mfp}}$) but much smaller than the macroscopic scale ($\ell$).
- **Distribution Function $f(\xi, x, t)$:**
  - Defines the density of molecules with velocity $\xi$ at location $x$ and time $t$.
  - $\xi = \frac{dx}{dt}$

- **Density of Molecules:**
  - Considering molecules with velocity $\xi + d\xi$
  - At location $x + dx$
  - At time $t$

- **Enables Continuum Description on Kinetic Level:**
  - Provides a bridge between microscopic and macroscopic descriptions of fluid behavior.

### ASCII Representation:


```
-------------------------------
|       .     .       .       |
| .        .         .        |
|      .           .        . |
|   .     .   .          .    |
|        .        . .         |
|   .  .     .         .      |
|      .      .   .    .      |
-------------------------------
```

## Probability Distribution Function 

### Important Properties of $f(\xi, x, t)$:

1. **Normalization:**
   - Total mass within a volume $\ell^3_{\text{av}}$:
   
$$
   \int d^3\xi \int d^3x \, f(\xi, x, t) = M(t)
   $$


2. **Fluid Density:**
   - Density at a point $x$ and time $t$:
   
$$
   \int d^3\xi \, f(\xi, x, t) = \rho(x, t)
   $$


3. **Momentum Density:**
   - Momentum at a point $x$ and time $t$:
   
$$
   \int d^3\xi \, \xi f(\xi, x, t) = \rho u(x, t)
   $$


4. **Pressure:**
   - Derived from the distribution function and represents the stress tensor:
   
$$
   \text{[complicated form not detailed here]}
   $$


- **Comprehensive Information:**
  - $f(\xi, x, t)$ contains all local fluid properties.
  - Macroscopic properties are obtained as moments of $f(\xi, x, t)$.


![probability_distribution_function](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/9821d7ff-d499-45a9-8fdd-3e4d73e6efb9)

## Introduction to Boltzmann Equation

### Key Concepts

- **Distribution Function $f(\xi, x, t)$**:
  - Represents the state of a particle system in terms of position $x$, velocity $\xi$, and time $t$.
  - Describes how the number of particles changes over time and space.

- **Evolution of $f(\xi, x, t)$**:
  - To understand how the distribution function evolves, we examine its rate of change over time.

## Boltzmann Equation

### Formulation

The Boltzmann equation describes the time evolution of the distribution function $f(\xi, x, t)$:


$$
\frac{df(\xi, x, t)}{dt} = \left( \frac{\partial}{\partial t} + \xi \cdot \frac{\partial}{\partial x} + \frac{f}{\rho} \cdot \frac{\partial}{\partial \xi} \right) f(\xi, x, t) = \Omega(f)
$$


### Components of the Equation

- **Total Derivative**:
  
$$
  \frac{df(\xi, x, t)}{dt} = \left( \frac{\partial}{\partial t} + \frac{dx}{dt} \cdot \frac{\partial}{\partial x} + \frac{d\xi}{dt} \cdot \frac{\partial}{\partial \xi} \right) f(\xi, x, t)
  $$

  - Combines the effects of time, space, and velocity changes on $f(\xi, x, t)$.

- **Simplified Form**:
  
$$
  \left( \frac{\partial}{\partial t} + \xi \cdot \frac{\partial}{\partial x} + \frac{f}{\rho} \cdot \frac{\partial}{\partial \xi} \right) f(\xi, x, t)
  $$

  - Shows the relation between the partial derivatives with respect to time, space, and velocity.

- **Collision Term $\Omega(f)$**:
  
$$
  \Omega(f)
  $$

  - Represents the effects of particle collisions.

## Significance of the Boltzmann Equation

- **Connection to Navier-Stokes Equations (NSE)**:
  - Through Chapman-Enskog analysis, the Boltzmann equation can recover the NSE, which govern macroscopic fluid dynamics.

- **Mesoscopic Perspective**:
  - The Boltzmann equation captures more physics than NSE by considering particle-level interactions while discarding irrelevant microscopic details.

## Collision Operator

### Role and Complexity

- **Describes Particle Collisions**:
  
$$
  \left( \frac{\partial f}{\partial t} \right)_{\text{coll}} = \iint g(l, \Omega) \left[ f(r, p_A', t) f(r, p_B', t) - f(r, p_A, t) f(r, p_B, t) \right] d\Omega d^3p_B
  $$

  - Accounts for changes in $f$ due to collisions between particles.

### Simplification with BGK Model

- **Bhatnagar-Gross-Krook (BGK) Model**:
  
$$
  \Omega(f) = -\frac{1}{\tau} (f - f^{\text{eq}})
  $$

  - Assumes $f$ relaxes to an equilibrium state $f^{\text{eq}}$ over a characteristic time $\tau$.

## Velocities in Kinetic Theory

### Types of Velocities

- **Molecular (absolute) Velocity $\xi$**:
  - The actual velocity of individual molecules.

- **Average Velocity $u$**:
  
$$
  u = \int d^3\xi \, \xi f(\xi) / \rho
  $$

  - The macroscopic flow velocity, which is also used in NSE.

- **Relative Velocity $v$**:
  
$$
  v = \xi - u
  $$

  - The velocity of molecules relative to the average flow velocity.



## Introduction to Using Boltzmann Equation to Solve Navier-Stokes Equations (NSE)

### Key Ideas

- **Goal**: Use the Boltzmann Equation (BE) to solve NSE.
- **Approach**: Simulate the evolution of the distribution function $f(\xi, x, t)$ instead of directly solving for macroscopic variables like $u(x, t)$ (velocity) and $p(x, t)$ (pressure).
- **Challenge**: The BE appears more complex than NSE, but it provides a more detailed physical description.

## Tasks for Implementing the Boltzmann Equation

1. **Discretise the distribution function $f(\xi, x, t)$**:
   - Convert continuous variables into discrete counterparts.
2. **Understand the Lattice-Boltzmann Equation (LBE)**:
   - Learn what LBE is and how it is derived from BE.
3. **Link LBE and NSE**:
   - Demonstrate the practical connection between these equations.
4. **Validate the method**:
   - Show that the LBE works effectively in simulations.

## From Boltzmann to Lattice-Boltzmann

### Discretisation of $f(\xi, x, t)$

#### Steps for Discretisation

1. **Space**:
   - $x \rightarrow \Delta x$ (lattice points)
2. **Time**:
   - $t \rightarrow \Delta t$
3. **Velocity Space**:
   - $f(\xi, x, t) \rightarrow f_i(x, t)$
   - Discretise the continuous velocity distribution into a finite set of discrete velocities.

### Velocity Space Discretisation

#### Key Concepts

- **Velocity Moments**:
  - For solving NSE, only certain moments of $f(\xi, x, t)$ are needed:
    
$$
    \int d^3 \xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3 \xi \, \xi f(\xi, x, t) = \rho u(x, t)
    $$

  - Integrals are replaced by sums using Hermite expansion, simplifying computations.

#### Discrete Velocity Sets

- **Example Sets**:
  - **D2Q9** (2D, 9 velocities) and **D3Q19** (3D, 19 velocities) are common discrete velocity sets used in Lattice-Boltzmann models.
  
- **Discrete Velocity Examples**:
  
$$
  (c_i) = \begin{pmatrix}
  0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 1 & 0 & -1 & 0 & 0 & 1 & 1
  \end{pmatrix} \Delta x
  $$

  
$$
  (c_i) = \begin{pmatrix}
  0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 0 & 1 & -1 \\
  0 & 0 & 0 & 0 & 0
  \end{pmatrix} \Delta t
  $$


### Gauss-Hermite Quadrature Rule

#### Explanation

- **Gauss-Hermite Quadrature**:
  
$$
  \int_{-\infty}^{+\infty} \omega(x) P^{(N)}(x) \, dx = \sum_{i=1}^{n} w_i P^{(N)}(x_i)
  $$

  - **Weight Function**: $\omega(x) \propto e^{-x^2}$
  - **Polynomials $P^{(N)}(x)$**: Order $N \leq 2n - 1$
  - **Roots $x_i$**: Roots of the Hermite polynomial $H^{(n)}(x)$
  - **Weights $w_i$**: Functions of $H^{(n-1)}(x)$

## Equilibrium Distribution

### Key Points:

- Collisions must conserve:
  - **Mass (density)**
  - **Momentum (velocity)**
  - **Energy (temperature)**
- Equilibrium distribution depends on $\rho$, $v$, and $T$.
- **Isotropic**: Depends only on the magnitude of the velocity $|v|$.

### Maxwell-Boltzmann Distribution


$$
f^{\text{eq}}(v, x, t) = \rho \left( \frac{1}{2\pi RT} \right)^{3/2} e^{-|v|^2 / (2RT)}
$$



$$
= \rho \left( \frac{1}{2\pi RT} \right)^{3/2} e^{-| \xi - u |^2 / (2RT)}
$$


### Explanation:

- The Maxwell-Boltzmann distribution describes the equilibrium state of a gas, where molecular velocities follow a specific statistical distribution.
- This distribution ensures that collisions among particles conserve mass, momentum, and energy.
- The equilibrium distribution function $f^{\text{eq}}(v, x, t)$ is isotropic, depending only on the magnitude of the velocity $|v|$.
- The parameters $\rho$ (density), $v$ (velocity), and $T$ (temperature) are the primary variables in this distribution.

## Using the Boltzmann Equation to Solve NSE

### Key Ideas:

- **Goal**: Use the Boltzmann Equation (BE) to solve Navier-Stokes Equations (NSE).
- **Approach**: Simulate the evolution of the distribution function $f(\xi, x, t)$ instead of directly solving for macroscopic variables like $u(x, t)$ (velocity) and $p(x, t)$ (pressure).
- **Challenge**: The BE appears more complex than NSE, but it provides a more detailed physical description.

## Tasks for Implementing the Boltzmann Equation

1. **Discretise the distribution function $f(\xi, x, t)$**:
   - Convert continuous variables into discrete counterparts.
2. **Understand the Lattice-Boltzmann Equation (LBE)**:
   - Learn what LBE is and how it is derived from BE.
3. **Link LBE and NSE**:
   - Demonstrate the practical connection between these equations.
4. **Validate the method**:
   - Show that the LBE works effectively in simulations.

## Lattice-Boltzmann Algorithm

### Lattice-Boltzmann Equation:


$$
f_i(x + c_i \Delta t, t + \Delta t) = \left(1 - \frac{\Delta t}{\tau}\right) f_i(x, t) + \frac{\Delta t}{\tau} f_i^{\text{eq}}(x, t)
$$


### Discretisation of $f(\xi, x, t)$

#### Steps for Discretisation

1. **Space**:
   - $x \rightarrow \Delta x$ (lattice points)
2. **Time**:
   - $t \rightarrow \Delta t$
3. **Velocity Space**:
   - $f(\xi, x, t) \rightarrow f_i(x, t)$
   - Discretise the continuous velocity distribution into a finite set of discrete velocities.

### Velocity Space Discretisation

#### Key Concepts

- **Velocity Moments**:
  - For solving NSE, only certain moments of $f(\xi, x, t)$ are needed:
    
$$
    \int d^3 \xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3 \xi \, \xi f(\xi, x, t) = \rho u(x, t)
    $$

  - Integrals are replaced by sums using Hermite expansion, simplifying computations.

#### Discrete Velocity Sets

- **Example Sets**:
  - **D2Q9** (2D, 9 velocities) and **D3Q19** (3D, 19 velocities) are common discrete velocity sets used in Lattice-Boltzmann models.
  
- **Discrete Velocity Examples**:
  
$$
  (c_i) = \begin{pmatrix}
  0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 1 & 0 & -1 & 0 & 0 & 1 & 1
  \end{pmatrix} \Delta x
  $$

  
$$
  (c_i) = \begin{pmatrix}
  0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 0 & 1 & -1 \\
  0 & 0 & 0 & 0 & 0
  \end{pmatrix} \Delta t
  $$


### Gauss-Hermite Quadrature Rule

#### Explanation

- **Gauss-Hermite Quadrature**:
  
$$
  \int_{-\infty}^{+\infty} \omega(x) P^{(N)}(x) \, dx = \sum_{i=1}^{n} w_i P^{(N)}(x_i)
  $$

  - **Weight Function**: $\omega(x) \propto e^{-x^2}$
  - **Polynomials $P^{(N)}(x)$**: Order $N \leq 2n - 1$
  - **Roots $x_i$**: Roots of the Hermite polynomial $H^{(n)}(x)$
  - **Weights $w_i$**: Functions of $H^{(n-1)}(x)$

#### Key Points

- Used to approximate integrals with a weight function $\omega(x)$ that matches the distribution of molecular velocities.
- The method is beneficial in the context of velocity space discretisation for kinetic theory.
- Simplifies the representation of continuous velocity distributions by using discrete points and weights.

## Advantages of the Lattice-Boltzmann Method (LBM)

### Key Points

- **Collision Process**:
  - Local and algebraic, making it computationally efficient.
- **Propagation Process**:
  - Linear and exact, simplifying the implementation.

## Viscosity and Speed of Sound

### Viscosity (from Chapman-Enskog Analysis)


$$

u = c_s^2 \left( \tau - \frac{\Delta t}{2} \right)
$$


### Speed of Sound


$$
c_s = \frac{1}{\sqrt{3}} \frac{\Delta x}{\Delta t}
$$


## Equilibrium Distribution Function

### Maxwell-Boltzmann Distribution


$$
f_i^{\text{eq}} = w_i \rho \left( 1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2c_s^4} - \frac{u \cdot u}{2c_s^2} \right)
$$


### Explanation

- The Maxwell-Boltzmann distribution describes the equilibrium state of a gas.
- It ensures the conservation of mass, momentum, and energy.
- The equilibrium distribution function $f_i^{\text{eq}}$ is isotropic and depends on the density $\rho$, velocity $u$, and temperature $T$.

## Why Lattice-Boltzmann Method (LBM) Works

### Key Ingredients

- **Lattice Symmetry/Isotropy**: Ensures accurate macroscopic fluid behavior.
- **Exact Conservation Laws**:
  
$$
  \sum_i \Omega_i = 0, \quad \sum_i c_i \Omega_i = 0
  $$

- **Chapman-Enskog Analysis**: Demonstrates that the Lattice-Boltzmann Equation (LBE) recovers the Navier-Stokes Equations (NSE).

### Explanation

- LBM relies on the symmetry and isotropy of the lattice to accurately capture fluid behavior.
- Conservation laws are maintained through the collision operator $\Omega$.
- Chapman-Enskog analysis provides a theoretical foundation showing how LBE approximates NSE.

## Chapman-Enskog Analysis

### Key Steps

1. **Multiscale Expansion**:
   
$$
   f_i = f_i^{\text{eq}} + \epsilon f_i^{(1)} + \epsilon^2 f_i^{(2)} + \cdots
   $$


2. **Taylor Expansion**:
   
$$
   f_i(x + c_i \Delta t, t + \Delta t) - f_i(x, t) = \sum_n \frac{\Delta t^n}{n!} (\partial_t + c_i \cdot 
abla)^n f_i
   $$


3. **Sort by Orders of $\epsilon$**:
   - Analyze terms of different orders to derive macroscopic equations.

4. **Calculate Moments and Compare**:
   - Compare with target equations like NSE to find the equation of state and expressions for viscosity.

## Advantages and Limitations of LBM

### Advantages

- **Speed**: Fast and computationally efficient due to its explicit, linear nature.
- **Simplicity**: No need for solving Poisson equations.
- **Parallelizability**: Highly parallelizable, suitable for high-performance computing (HPC).
- **Complex Geometries**: Handles complex geometries effectively.

### Limitations

- **Knudsen Number**: Best suited for small Knudsen numbers (minimal rarefied gas effects).
- **Mach Number**: Works well for small Mach numbers (low-speed flows).
- **Transient Solutions**: Often applied to time-dependent problems.

## Main Areas of Development in LBM


$$
\Delta f_i = \Omega_i + S_i
$$


### Streaming Step $\Delta f_i$

- **Advanced Boundary Conditions**: Improving the treatment of boundaries.
- **Rarefied Gases**: Extending LBM to handle rarefied gas flows.
- **Hybrid Methods**: Developing methods like Finite Volume Lattice-Boltzmann Method (FV-LBM).

### Collision Operator $\Omega_i$

- **Transport Equations**: Solving Advection-Diffusion Equations (ADE) and other transport equations.
- **Compressible Flows**: Applying LBM to compressible flow problems.
- **High-Re Flows**: Handling high Reynolds number flows and turbulence.

### Source Term $S_i$

- **Reactions**: Incorporating chemical reactions.
- **Multi-Phase Flows**: Modeling interactions between different fluid phases.
- **Fluid-Structure Interaction**: Simulating interactions between fluids and structures.

### Explanation

- **Streaming Step $\Delta f_i$**: Enhancements in boundary conditions and hybrid methods improve the accuracy and applicability of LBM.
- **Collision Operator $\Omega_i$**: Extensions to handle various transport equations and complex flow scenarios.
- **Source Term $S_i$**: Allows modeling of more complex physical phenomena like reactions and multi-phase flows.

