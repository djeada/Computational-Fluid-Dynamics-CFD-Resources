## Lattice-Boltzmann Algorithm

The Lattice-Boltzmann method (LBM) is a powerful computational approach used to simulate fluid dynamics. It operates on a mesoscopic scale, bridging the gap between molecular dynamics and continuum fluid dynamics described by the Navier-Stokes equations.

### Lattice-Boltzmann Equation:

The Lattice-Boltzmann equation for the distribution function \( f_i(x, t) \) is given by:

$$
f_i(x + c_i \Delta t, t + \Delta t) = \left(1 - \frac{\Delta t}{\tau}\right) f_i(x, t) + \frac{\Delta t}{\tau} f_i^{\text{eq}}(x, t)
$$

where:
- \( f_i(x, t) \) is the distribution function at position \( x \) and time \( t \) for the discrete velocity \( c_i \).
- \( \Delta t \) is the time step.
- \( \tau \) is the relaxation time.
- \( f_i^{\text{eq}}(x, t) \) is the equilibrium distribution function.

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
  - For solving the Navier-Stokes equations, only certain moments of \( f(\xi, x, t) \) are needed:
  $$
  \int d^3 \xi \, f(\xi, x, t) = \rho(x, t), \quad \int d^3 \xi \, \xi f(\xi, x, t) = \rho \mathbf{u}(x, t)
  $$
  - These integrals are replaced by sums using Hermite expansion, simplifying computations.

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

### Lattice-Boltzmann Algorithm Steps

1. **Initialization:**
   - Initialize the distribution function \( f_i(x, 0) \) according to the initial conditions of the problem.

2. **Collision Step:**
   - Apply the collision operator to update the distribution function:
   $$
   f_i^*(x, t) = f_i(x, t) - \frac{\Delta t}{\tau} \left( f_i(x, t) - f_i^{\text{eq}}(x, t) \right)
   $$

3. **Streaming Step:**
   - Propagate the distribution function along the discrete velocity directions to neighboring lattice points:
   $$
   f_i(x + c_i \Delta t, t + \Delta t) = f_i^*(x, t)
   $$

4. **Boundary Conditions:**
   - Implement appropriate boundary conditions to handle the interaction of fluid with solid boundaries or interfaces.

5. **Macroscopic Variables Calculation:**
   - Compute macroscopic variables such as density \( \rho \) and velocity \( \mathbf{u} \) from the moments of the distribution function:
   $$
   \rho(x, t) = \sum_i f_i(x, t), \quad \rho \mathbf{u}(x, t) = \sum_i f_i(x, t) c_i
   $$

6. **Iteration:**
   - Repeat the collision and streaming steps for each time step until the simulation reaches the desired end time.

### Validation and Applications

- **Validation:**
  - Validate the Lattice-Boltzmann method by comparing simulation results with experimental data or analytical solutions of the Navier-Stokes equations.

- **Applications:**
  - The Lattice-Boltzmann method is versatile and can be applied to simulate fluid flow in porous media, multiphase flows, thermal flows, and complex boundary dynamics.

### Gauss-Hermite Quadrature Rule

#### Explanation

- **Gauss-Hermite Quadrature:**

$$
\int_{-\infty}^{+\infty} \omega(x) P^{(N)}(x) \, dx = \sum_{i=1}^{n} w_i P^{(N)}(x_i)
$$

  - **Weight Function \( \omega(x) \):** Proportional to \( e^{-x^2} \).
  - **Polynomials \( P^{(N)}(x) \):** Polynomials of order \( N \leq 2n - 1 \).
  - **Roots \( x_i \):** The roots of the Hermite polynomial \( H^{(n)}(x) \).
  - **Weights \( w_i \):** Functions of the Hermite polynomial \( H^{(n-1)}(x) \).

#### Key Points

- Used to approximate integrals with a weight function \( \omega(x) \) that matches the distribution of molecular velocities.
- Beneficial in the context of velocity space discretization for kinetic theory.
- Simplifies the representation of continuous velocity distributions by using discrete points and weights.

## Advantages of the Lattice-Boltzmann Method (LBM)

### Key Points

- **Collision Process:**
  - The collision process is local and algebraic, making it computationally efficient.
- **Propagation Process:**
  - The propagation process is linear and exact, simplifying the implementation.

### Additional Advantages

- **Parallelization:**
  - The algorithm's structure is highly parallelizable, making it suitable for high-performance computing.
- **Flexibility in Boundary Conditions:**
  - LBM can handle complex boundaries and interfaces more easily compared to traditional CFD methods.
- **Handling Complex Flows:**
  - It is effective in simulating multiphase and multicomponent flows.

## Viscosity and Speed of Sound

### Viscosity (from Chapman-Enskog Analysis)

$$
\nu = c_s^2 \left( \tau - \frac{\Delta t}{2} \right)
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
- Ensures the conservation of mass, momentum, and energy.
- The equilibrium distribution function \( f_i^{\text{eq}} \) is isotropic and depends on the density \( \rho \), velocity \( u \), and temperature \( T \).

## Why Lattice-Boltzmann Method (LBM) Works

### Key Ingredients

- **Lattice Symmetry/Isotropy:**
  - Ensures accurate macroscopic fluid behavior through the symmetry and isotropy of the lattice structure.
- **Exact Conservation Laws:**
  
$$
\sum_i \Omega_i = 0, \quad \sum_i c_i \Omega_i = 0
$$

  - Conservation of mass and momentum is maintained through the collision operator \( \Omega \).

- **Chapman-Enskog Analysis:**
  - Demonstrates that the Lattice-Boltzmann Equation (LBE) recovers the Navier-Stokes Equations (NSE).

### Explanation

- **Lattice Symmetry/Isotropy:**
  - The symmetry and isotropy of the lattice ensure that the macroscopic fluid behavior is accurately captured. This is critical for the correct representation of fluid flow.
- **Conservation Laws:**
  - Conservation of mass, momentum, and energy are embedded within the LBM through the collision operator \( \Omega \), which ensures these properties are maintained throughout the simulation.
- **Chapman-Enskog Analysis:**
  - This analysis provides a theoretical foundation showing how the Lattice-Boltzmann Equation approximates the Navier-Stokes Equations, thus validating the LBM for fluid dynamics simulations.

### Additional Points

- **Flexibility and Adaptability:**
  - LBM is adaptable to a wide range of physical phenomena and can be extended to simulate thermal flows, multiphase flows, and flows in porous media.
- **Efficiency:**
  - The local nature of the collision and streaming steps makes LBM computationally efficient, suitable for large-scale simulations.

## Chapman-Enskog Analysis

Chapman-Enskog analysis is a powerful mathematical technique used to derive macroscopic fluid equations from the Boltzmann equation. This method expands the distribution function in terms of a small parameter \( \epsilon \) and matches terms of the same order to obtain macroscopic equations.

### Key Steps

1. **Multiscale Expansion:**

   The distribution function \( f_i \) is expanded in terms of a small parameter \( \epsilon \):
   $$
   f_i = f_i^{\text{eq}} + \epsilon f_i^{(1)} + \epsilon^2 f_i^{(2)} + \cdots
   $$
   Here, \( f_i^{\text{eq}} \) is the equilibrium distribution function, and \( f_i^{(n)} \) are the nonequilibrium corrections of different orders.

2. **Taylor Expansion:**

   The distribution function is expanded using the Taylor series around \((x, t)\):
   $$
   f_i(x + c_i \Delta t, t + \Delta t) - f_i(x, t) = \sum_n \frac{\Delta t^n}{n!} (\partial_t + c_i \cdot \nabla)^n f_i
   $$
   This expansion helps in understanding how the distribution function evolves over time and space.

3. **Sort by Orders of \( \epsilon \):**

   The terms are sorted by different orders of \( \epsilon \):
   - \( \mathcal{O}(1) \): Represents the equilibrium state.
   - \( \mathcal{O}(\epsilon) \): Represents first-order deviations from equilibrium.
   - \( \mathcal{O}(\epsilon^2) \): Represents second-order deviations, and so on.
   
   Analyzing these terms helps in deriving the macroscopic fluid dynamics equations.

4. **Calculate Moments and Compare:**

   Moments of the distribution function are calculated and compared with the target macroscopic equations (like the Navier-Stokes equations) to find the equation of state and expressions for viscosity, thermal conductivity, and other transport properties.

## Advantages and Limitations of LBM

### Advantages

- **Speed:** LBM is computationally efficient due to its explicit and linear nature.
- **Simplicity:** LBM does not require solving complex Poisson equations, simplifying the implementation.
- **Parallelizability:** The method is highly parallelizable, making it suitable for high-performance computing (HPC) environments.
- **Complex Geometries:** LBM can handle complex geometries and boundaries effectively.

### Limitations

- **Knudsen Number:** LBM is best suited for small Knudsen numbers, indicating minimal rarefied gas effects.
- **Mach Number:** The method works well for small Mach numbers, corresponding to low-speed flows.
- **Transient Solutions:** LBM is often applied to time-dependent problems and may face challenges in steady-state simulations.

## Main Areas of Development in LBM

The Lattice-Boltzmann method is continuously evolving, with ongoing research and development in several key areas.

### Streaming Step \( \Delta f_i \)

- **Advanced Boundary Conditions:** Improving the treatment of boundaries to enhance accuracy and applicability.
- **Rarefied Gases:** Extending LBM to handle rarefied gas flows, which are significant at high Knudsen numbers.
- **Hybrid Methods:** Developing methods like the Finite Volume Lattice-Boltzmann Method (FV-LBM) to combine the strengths of different numerical approaches.

### Collision Operator \( \Omega_i \)

- **Transport Equations:** Solving Advection-Diffusion Equations (ADE) and other transport equations using LBM.
- **Compressible Flows:** Applying LBM to compressible flow problems, which are important in high-speed aerodynamics.
- **High-Re Flows:** Handling high Reynolds number flows and turbulence, which are critical for industrial applications.

### Source Term \( S_i \)

- **Reactions:** Incorporating chemical reactions into the LBM framework to model reactive flows.
- **Multi-Phase Flows:** Modeling interactions between different fluid phases, such as liquid-liquid or gas-liquid flows.
- **Fluid-Structure Interaction:** Simulating interactions between fluids and structures, which is important in engineering applications.

### Explanation

- **Streaming Step \( \Delta f_i \):** Enhancements in boundary conditions and hybrid methods improve the accuracy and applicability of LBM, making it suitable for more complex simulations.
- **Collision Operator \( \Omega_i \):** Extensions to handle various transport equations and complex flow scenarios broaden the range of problems that LBM can address.
- **Source Term \( S_i \):** Including source terms allows the modeling of more complex physical phenomena such as chemical reactions, multi-phase flows, and fluid-structure interactions.
