# From Newton to Navier-Stokes

## Lattice-Boltzmann Approach
The Lattice-Boltzmann method (LBM) is designed to solve the Navier-Stokes equations (NSE) rather than the Boltzmann equation directly. It represents a mesoscopic approach, providing a bridge between microscopic molecular dynamics (MD) and macroscopic computational fluid dynamics (CFD).

### Key Questions:
- Can a mesoscopic approach be effectively used to solve the Navier-Stokes equations?
- What are the advantages of using the Lattice-Boltzmann method?

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
- **Objective:** Eliminate unnecessary microscopic details while retaining essential macroscopic behaviors.

### Key Points:
- **Averaging Molecules in Small Volumes:**
  - The scale of averaging ($\ell_{\text{av}}$) is much larger than the mean free path ($\ell_{\text{mfp}}$) but much smaller than the macroscopic scale ($\ell$).
- **Distribution Function $f(\xi, x, t)$:**
  - Defines the density of molecules with velocity $\xi$ at location $x$ and time $t$.
  - $\xi = \frac{dx}{dt}$, where $\xi$ represents the velocity of molecules.

- **Density of Molecules:**
  - Considering molecules with velocity $\xi + d\xi$.
  - At location $x + dx$.
  - At time $t$.

- **Enables Continuum Description on Kinetic Level:**
  - Provides a bridge between microscopic (molecular) and macroscopic (fluid) descriptions of behavior.

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

### Advantages of the Lattice-Boltzmann Method:

1. The method is inherently parallel, making it well-suited for high-performance computing.
2. LBM can handle complex boundary conditions more easily compared to traditional CFD methods.
3. The algorithm is relatively simple, reducing the complexity of implementation.
4. LBM directly solves the fluid flow problems using the mesoscopic kinetic model, which can be more intuitive and physically insightful.

## Probability Distribution Function

### Important Properties of \( f(\xi, x, t) \):

1. **Normalization:**
   - Total mass within a volume \( \ell^3_{\text{av}} \):
   $$
   \int d^3\xi \int d^3x \, f(\xi, x, t) = M(t)
   $$

2. **Fluid Density:**
   - Density at a point \( x \) and time \( t \):
   $$
   \int d^3\xi \, f(\xi, x, t) = \rho(x, t)
   $$

3. **Momentum Density:**
   - Momentum at a point \( x \) and time \( t \):
   $$
   \int d^3\xi \, \xi f(\xi, x, t) = \rho u(x, t)
   $$

4. **Pressure:**
   - Derived from the distribution function and represents the stress tensor:
   $$
   \text{[complicated form not detailed here]}
   $$

### Comprehensive Information:
- \( f(\xi, x, t) \) contains all local fluid properties.
- Macroscopic properties are obtained as moments of \( f(\xi, x, t) \).

![Probability Distribution Function](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/9821d7ff-d499-45a9-8fdd-3e4d73e6efb9)

## Introduction to the Boltzmann Equation

### Key Concepts

- **Distribution Function \( f(\xi, x, t) \):**
  - Represents the state of a particle system in terms of position \( x \), velocity \( \xi \), and time \( t \).
  - Describes how the number of particles changes over time and space.

- **Evolution of \( f(\xi, x, t) \):**
  - To understand how the distribution function evolves, we examine its rate of change over time. The Boltzmann equation governs this evolution, incorporating both the advection of particles and their collisions.

### Boltzmann Equation:

The Boltzmann equation provides a statistical description of a dilute gas. It is a fundamental equation in the kinetic theory of gases, describing the time evolution of the distribution function \( f(\xi, x, t) \). The general form of the Boltzmann equation is:

$$
\frac{\partial f}{\partial t} + \xi \cdot \nabla_x f + F \cdot \nabla_\xi f = \left( \frac{\partial f}{\partial t} \right)_{\text{collision}}
$$

Where:
- \( \frac{\partial f}{\partial t} \) is the time derivative of \( f \).
- \( \xi \cdot \nabla_x f \) represents the advection term, accounting for the movement of particles.
- \( F \cdot \nabla_\xi f \) is the force term, describing the influence of external forces.
- \( \left( \frac{\partial f}{\partial t} \right)_{\text{collision}} \) is the collision term, which models the interactions between particles.

## Significance of the Boltzmann Equation

- **Connection to Navier-Stokes Equations (NSE):**
  - Through Chapman-Enskog analysis, the Boltzmann equation can recover the NSE, which govern macroscopic fluid dynamics.

- **Mesoscopic Perspective:**
  - The Boltzmann equation captures more physics than the NSE by considering particle-level interactions while discarding irrelevant microscopic details.

## Collision Operator

The collision term \( \left( \frac{\partial f}{\partial t} \right)_{\text{collision}} \) is often the most complex part of the Boltzmann equation. It describes how collisions redistribute the velocities of particles, driving the system towards equilibrium. The collision integral typically involves a double integral over the velocities of colliding particles and the scattering angle.

### Role and Complexity

- **Describes Particle Collisions:**
  
$$
\left( \frac{\partial f}{\partial t} \right)_{\text{collision}} = \iint g(\mathbf{v}, \Omega) \left[ f(\mathbf{x}, \mathbf{p}_A', t) f(\mathbf{x}, \mathbf{p}_B', t) - f(\mathbf{x}, \mathbf{p}_A, t) f(\mathbf{x}, \mathbf{p}_B, t) \right] d\Omega \, d^3\mathbf{p}_B
$$

  - Accounts for changes in \( f \) due to collisions between particles, where \( g(\mathbf{v}, \Omega) \) is the collision kernel, \( \mathbf{p}_A \) and \( \mathbf{p}_B \) are the momenta of particles before collision, and \( \mathbf{p}_A' \) and \( \mathbf{p}_B' \) are the momenta after collision.

### Simplification with BGK Model

- **Bhatnagar-Gross-Krook (BGK) Model:**
  
$$
\left( \frac{\partial f}{\partial t} \right)_{\text{collision}} = -\frac{1}{\tau} \left( f - f^{\text{eq}} \right)
$$

  - Assumes \( f \) relaxes to an equilibrium state \( f^{\text{eq}} \) over a characteristic time \( \tau \).

## Velocities in Kinetic Theory

### Types of Velocities

- **Molecular (Absolute) Velocity \( \mathbf{\xi} \):**
  - The actual velocity of individual molecules.

- **Average Velocity \( \mathbf{u} \):**
  
$$
\mathbf{u} = \frac{1}{\rho} \int d^3\xi \, \mathbf{\xi} f(\mathbf{\xi}, \mathbf{x}, t)
$$

  - The macroscopic flow velocity, which is also used in the Navier-Stokes equations.

- **Relative Velocity \( \mathbf{v} \):**
  
$$
\mathbf{v} = \mathbf{\xi} - \mathbf{u}
$$

  - The velocity of molecules relative to the average flow velocity.

By understanding these velocities, we can describe the kinetic behavior of the fluid at different scales and link microscopic interactions to macroscopic phenomena.

## Comprehensive Information

- The distribution function \( f(\xi, x, t) \) contains all local fluid properties.
- Macroscopic properties are obtained as moments of \( f(\xi, x, t) \).

## Introduction to Using the Boltzmann Equation to Solve Navier-Stokes Equations (NSE)

### Key Ideas

- **Goal:** Utilize the Boltzmann Equation (BE) to solve the Navier-Stokes Equations (NSE).
- **Approach:** Simulate the evolution of the distribution function \( f(\xi, x, t) \) instead of directly solving for macroscopic variables like velocity \( \mathbf{u}(x, t) \) and pressure \( p(x, t) \).
- **Challenge:** Although the BE appears more complex than NSE, it provides a more detailed and accurate physical description of fluid dynamics.

## Tasks for Implementing the Boltzmann Equation

1. **Discretize the distribution function \( f(\xi, x, t) \):**
   - Convert continuous variables into discrete counterparts for computational efficiency.
2. **Understand the Lattice-Boltzmann Equation (LBE):**
   - Learn about the LBE and how it is derived from the BE.
3. **Link LBE and NSE:**
   - Demonstrate the practical connection between the LBE and the NSE.
4. **Validate the method:**
   - Show that the LBE effectively works in simulations, producing results consistent with physical observations.

## From Boltzmann to Lattice-Boltzmann

### Discretization of \( f(\xi, x, t) \)

#### Steps for Discretization

1. **Space:**
   - Discretize spatial coordinates \( x \) to lattice points \( \Delta x \).

2. **Time:**
   - Discretize time \( t \) to time steps \( \Delta t \).

3. **Velocity Space:**
   - Discretize the continuous velocity distribution into a finite set of discrete velocities \( f_i(x, t) \).

### Velocity Space Discretization

#### Key Concepts

- **Velocity Moments:**
  - For solving the NSE, only certain moments of \( f(\xi, x, t) \) are needed:
  $$
  \int d^3 \xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3 \xi \, \xi f(\xi, x, t) = \rho \mathbf{u}(x, t)
  $$
  - These integrals are replaced by sums using Hermite expansion, which simplifies computations.

#### Discrete Velocity Sets

- **Example Sets:**
  - **D2Q9** (2D, 9 velocities) and **D3Q19** (3D, 19 velocities) are common discrete velocity sets used in Lattice-Boltzmann models.

- **Discrete Velocity Examples:**

  For the D2Q9 model:
  $$
  (c_i) = \begin{pmatrix}
  0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1
  \end{pmatrix} \Delta x
  $$

  For the D3Q19 model:
  $$
  (c_i) = \begin{pmatrix}
  0 & 1 & -1 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 & -1 & 0 & 1 & 1 & -1 & -1 & 0 & 0 & 1 & 1 & -1 & -1 & 1 & 1 & -1 \\
  0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & -1 & 1 & 1
  \end{pmatrix} \Delta t
  ```

### Detailed Steps in Using the Boltzmann Equation to Solve NSE

1. **Initialize the Distribution Function:**
   - Start with an initial distribution function \( f_i(x, t=0) \) that represents the initial state of the fluid.

2. **Collision Step:**
   - Apply the collision operator to update the distribution function. This often involves using a model like the BGK model to relax the distribution towards equilibrium.

3. **Streaming Step:**
   - Propagate the distribution function along the discrete velocity directions to update their values at neighboring lattice points.

4. **Boundary Conditions:**
   - Implement appropriate boundary conditions to handle the interaction of fluid with solid boundaries or interfaces.

5. **Macroscopic Variables Calculation:**
   - Compute macroscopic variables such as density \( \rho \) and velocity \( \mathbf{u} \) from the moments of the distribution function.

6. **Iterate:**
   - Repeat the collision and streaming steps for each time step until the simulation reaches the desired end time.

### Validation and Applications

- **Validation:**
  - Compare the results of the LBE-based simulations with experimental data or solutions obtained from direct numerical simulations of the NSE to ensure accuracy and reliability.

- **Applications:**
  - The Lattice-Boltzmann method can be used in various applications such as fluid flow in porous media, multiphase flows, thermal flows, and complex boundary dynamics.



### Maxwell-Boltzmann Distribution

The Maxwell-Boltzmann distribution describes the equilibrium state of a gas where the molecular velocities follow a specific statistical distribution. The equilibrium distribution function \( f^{\text{eq}}(\xi, x, t) \) is given by:

$$
f^{\text{eq}}(\xi, x, t) = \rho \left( \frac{1}{2\pi RT} \right)^{3/2} e^{-\frac{|\xi - u|^2}{2RT}}
$$

### Explanation:

- **Equilibrium State:** The Maxwell-Boltzmann distribution describes the equilibrium state of a gas, where the velocities of the gas molecules are distributed according to a specific statistical law.
- **Conservation Laws:** This distribution ensures that collisions among particles conserve mass, momentum, and energy, which are fundamental principles in physics.
- **Isotropy:** The equilibrium distribution function \( f^{\text{eq}}(\xi, x, t) \) is isotropic, meaning it depends only on the magnitude of the velocity \( |\xi| \) and not on its direction.
- **Primary Variables:** The parameters involved in this distribution are:
  - \( \rho \): Density of the gas.
  - \( \xi \): Molecular velocity.
  - \( u \): Average macroscopic velocity of the gas.
  - \( T \): Temperature of the gas.
  - \( R \): Specific gas constant.

By understanding and utilizing the Maxwell-Boltzmann distribution, we can describe the statistical behavior of gas molecules at equilibrium, which forms the foundation for more complex kinetic theory analyses.

## Using the Boltzmann Equation to Solve Navier-Stokes Equations (NSE)

### Key Ideas:

- **Goal:** Utilize the Boltzmann Equation (BE) to solve the Navier-Stokes Equations (NSE).
- **Approach:** Instead of directly solving for macroscopic variables like velocity \( \mathbf{u}(x, t) \) and pressure \( p(x, t) \), simulate the evolution of the distribution function \( f(\xi, x, t) \).
- **Challenge:** Although the BE is more complex than the NSE, it provides a more detailed and accurate physical description of fluid dynamics.

## Tasks for Implementing the Boltzmann Equation

1. **Discretize the Distribution Function \( f(\xi, x, t) \):**
   - Convert continuous variables into discrete counterparts for computational efficiency.

2. **Understand the Lattice-Boltzmann Equation (LBE):**
   - Learn about the LBE and how it is derived from the BE.

3. **Link LBE and NSE:**
   - Demonstrate the practical connection between the LBE and the NSE.

4. **Validate the Method:**
   - Show that the LBE effectively works in simulations, producing results consistent with physical observations.

## From Boltzmann to Lattice-Boltzmann

### Discretization of \( f(\xi, x, t) \)

#### Steps for Discretization

1. **Space:**
   - Discretize spatial coordinates \( x \) to lattice points \( \Delta x \).

2. **Time:**
   - Discretize time \( t \) to time steps \( \Delta t \).

3. **Velocity Space:**
   - Discretize the continuous velocity distribution into a finite set of discrete velocities \( f_i(x, t) \).

### Velocity Space Discretization

#### Key Concepts

- **Velocity Moments:**
  - For solving the NSE, only certain moments of \( f(\xi, x, t) \) are needed:
  $$
  \int d^3\xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3\xi \, \xi f(\xi, x, t) = \rho \mathbf{u}(x, t)
  $$
  - These integrals are replaced by sums using Hermite expansion, which simplifies computations.

#### Discrete Velocity Sets

- **Example Sets:**
  - **D2Q9** (2D, 9 velocities) and **D3Q19** (3D, 19 velocities) are common discrete velocity sets used in Lattice-Boltzmann models.

- **Discrete Velocity Examples:**

  For the D2Q9 model:
  $$
  (c_i) = \begin{pmatrix}
  0 & 1 & 0 & -1 & 0 & 1 & -1 & 1 & -1 \\
  0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1
  \end{pmatrix} \Delta x
  $$

  For the D3Q19 model:
  $$
  (c_i) = \begin{pmatrix}
  0 & 1 & -1 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 1 & -1 & 0 & 0 & 0 \\
  0 & 0 & 0 & 1 & -1 & 0 & 1 & 1 & -1 & -1 & 0 & 0 & 1 & 1 & -1 & -1 & 1 & 1 & -1 \\
  0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & -1 & 1 & -1 & 1 & -1 & -1 & 1 & 1
  \end{pmatrix} \Delta t
  ```

### Detailed Steps in Using the Boltzmann Equation to Solve NSE

1. **Initialize the Distribution Function:**
   - Start with an initial distribution function \( f_i(x, t=0) \) that represents the initial state of the fluid.

2. **Collision Step:**
   - Apply the collision operator to update the distribution function. This often involves using a model like the BGK model to relax the distribution towards equilibrium.

3. **Streaming Step:**
   - Propagate the distribution function along the discrete velocity directions to update their values at neighboring lattice points.

4. **Boundary Conditions:**
   - Implement appropriate boundary conditions to handle the interaction of fluid with solid boundaries or interfaces.

5. **Macroscopic Variables Calculation:**
   - Compute macroscopic variables such as density \( \rho \) and velocity \( \mathbf{u} \) from the moments of the distribution function.

6. **Iterate:**
   - Repeat the collision and streaming steps for each time step until the simulation reaches the desired end time.

### Validation and Applications

- **Validation:**
  - Compare the results of the LBE-based simulations with experimental data or solutions obtained from direct numerical simulations of the NSE to ensure accuracy and reliability.

- **Applications:**
  - The Lattice-Boltzmann method can be used in various applications such as fluid flow in porous media, multiphase flows, thermal flows, and complex boundary dynamics.
