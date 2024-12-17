# Lattice-Boltzmann Algorithm

The **Lattice-Boltzmann method (LBM)** is a computational approach for simulating fluid flows at a mesoscopic scale. It provides a bridge between microscopic kinetic theories and macroscopic continuum models like the Navier-Stokes equations. Over the past decades, LBM has become increasingly popular in computational fluid dynamics (CFD) due to its simplicity, efficiency, and natural handling of complex boundary conditions.

## Key Principles of LBM

I. **Kinetic Origin**:  

LBM originates from the Boltzmann equation of kinetic theory, which describes the evolution of a particle distribution function $f(\xi, x, t)$. Instead of solving the continuous Boltzmann equation directly, LBM discretizes space, time, and velocity space into a finite set of discrete velocities and moves “particles” along a lattice.

II. **Mesoscopic Approach**:  

LBM operates at an intermediate scale: it does not simulate individual molecules (like molecular dynamics) nor solve continuum PDEs (like the Navier-Stokes equations) directly. Instead, it uses distribution functions and collision models that, through proper averaging (Chapman-Enskog analysis), recover macroscopic fluid behavior.

III. **Discrete Velocities and Lattice Grids**:  

The method discretizes the domain into a lattice (grid) and assigns a finite set of discrete velocities $\{c_i\}$. At each lattice point, we track distribution functions $f_i(x,t)$ corresponding to each discrete velocity $c_i$.

## Lattice-Boltzmann Equation

The fundamental equation in LBM is the discrete Boltzmann equation with a simple relaxation collision model (BGK model):

$$f_i(x + c_i \Delta t, t + \Delta t) = f_i(x, t) - \frac{\Delta t}{\tau} [ f_i(x,t) - f_i^{\text{eq}}(x,t) ].$$

**Key Definitions**:

- $f_i(x,t)$: Distribution function for the discrete velocity $c_i$.
- $\Delta t$: Time step.
- $\tau$: Relaxation time controlling viscosity.
- $f_i^{\text{eq}}(x,t)$: Equilibrium distribution approximating the Maxwell-Boltzmann distribution.

## Discretization of $f(\xi, x, t)$

**Discretization Steps**:

I. **Spatial Discretization**:  

Divide the domain $\Omega$ into a lattice of points separated by $\Delta x$.

II. **Temporal Discretization**:  

Evolve the solution in discrete time steps $\Delta t$.

III. **Velocity Space Discretization**:  

Replace the continuous velocity space with a finite, discrete set of velocities $\{c_i\}_{i=1}^Q$. Typical sets are chosen to ensure isotropy and correct recovery of Navier-Stokes equations.

**Common Discrete Velocity Sets**:

- **D2Q9 (2D)**: 9 discrete velocities arranged isotropically in a 2D plane.
- **D3Q19 or D3Q27 (3D)**: Common sets used in three-dimensional simulations.

Each discrete velocity set is chosen so that moments of $f_i$ reproduce the required macroscopic flow equations.

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
$$

## Moments and Macroscopic Variables

From the distribution functions, macroscopic quantities are obtained via moments:

$$\rho(x,t) = \sum_i f_i(x,t), \quad \rho u(x,t) = \sum_i f_i(x,t) c_i.$$

Here:

- $\rho$ is density.
- $u$ is velocity vector.

Higher moments recover stresses, pressure, and other hydrodynamic variables.

## The Lattice-Boltzmann Algorithm

The LBM algorithm consists of two main steps each time iteration:

I. **Collision Step**:

- Locally relax the distribution functions $f_i$ towards an equilibrium $f_i^{\text{eq}}$.
- The post-collision distributions $f_i^*(x,t)$ are computed as:

 $$f_i^*(x,t) = f_i(x,t) - \frac{\Delta t}{\tau} [f_i(x,t)-f_i^{\text{eq}}(x,t)].$$

II. **Streaming Step**:

Move the post-collision distributions along their respective discrete velocities to adjacent lattice sites:

$$f_i(x+c_i\Delta t, t+\Delta t) = f_i^*(x,t).$$

- **Boundary Conditions**: Implement boundary conditions (no-slip, inflow/outflow, moving walls) by prescribing suitable bounce-back or interpolation methods. LBM makes it straightforward to handle complex boundaries.
- **Macroscopic Variables Calculation**: After collision and streaming, compute $\rho$ and $\rho u$ at each lattice point.

Repeat the collision and streaming steps until the desired time is reached.

## Gaussian-Hermite Quadrature and Hermite Expansion

**Why Hermite Polynomials?**

- The equilibrium distributions in LBM are typically truncated expansions of the Maxwell-Boltzmann distribution using Hermite polynomials.
- Gauss-Hermite quadrature approximates continuous velocity integrals by discrete sums, ensuring that the chosen discrete velocities and weights produce correct low-order moments.

**Key Idea**:
- Approximate integrals:

$$\int_{-\infty}^{\infty} f(\xi) e^{-\xi^2} d\xi \approx \sum_i w_i f(x_i),$$
where $x_i, w_i$ come from Hermite polynomial roots and weights.

**Benefit**:
- Ensures correct recovery of isothermal Navier-Stokes equations up to a certain order in Mach number and Knudsen number.

## Physical Interpretations and Parameters

### Viscosity and Speed of Sound

**Viscosity**:

From Chapman-Enskog analysis:

$$\nu = c_s^2 \left( \tau - \frac{\Delta t}{2} \right),$$
where $c_s = \frac{1}{\sqrt{3}}(\frac{\Delta x}{\Delta t})$ is the LBM speed of sound.

**Speed of Sound**:

$c_s$ is a model-dependent quantity and relates the lattice spacing $\Delta x$ and time step $\Delta t$.

### Equilibrium Distribution

The equilibrium distribution function:

$$f_i^{\text{eq}} = w_i \rho \left[1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2c_s^4} - \frac{u \cdot u}{2c_s^2}\right],$$
ensures correct mass, momentum, and pressure representation.

## Why LBM Works

- **Conservation Laws**: The collision operator is designed to conserve mass and momentum. Summation constraints ensure the lowest velocity moments match macroscopic fields.
- **Chapman-Enskog Expansion**: By performing a multi-scale expansion of the LBM and comparing terms order-by-order with the Navier-Stokes equations, one shows that LBM recovers the NSE in the hydrodynamic limit.
- **Isotropy and Lattice Symmetry**: Carefully chosen discrete velocities guarantee isotropic diffusivity and correct second-order accuracy in space and time.

## Advantages of LBM

I. **Simplicity**:

- Local collision step and linear streaming step yield a straightforward and highly parallelizable algorithm.
- No need to solve complex Poisson equations for pressure, simplifying incompressible flow simulations.

II. **Boundary Handling**:

- Complex geometries, moving boundaries, or porous media are more easily handled with bounce-back or immersed boundary methods.

III. **Parallelization and Efficiency**:

- Each lattice node updates independently, making LBM ideal for modern HPC architectures (GPU, clusters).

IV. **Flexible Extensions**:

- Multiphase flows, thermal flows, and reactive flows can be incorporated by modifying collision operators or adding distribution functions for additional fields.

## Limitations and Ongoing Research

**Knudsen and Mach Numbers**:
- LBM works best at low Mach and Knudsen numbers. High-speed or rarefied flows require either more sophisticated collision models or extended velocity sets.
**Turbulence Modeling**:
- High-Reynolds number flows necessitate turbulence models or large-eddy simulation techniques integrated within the LBM framework.
**Compressible and High-Ma Flows**:
- Extended lattice sets or multiple distribution functions are needed to handle compressible regimes accurately.
**Hybrid Methods**:
- Combining LBM with finite volume or finite element approaches, or using dimensional reduction methods (such as Reduced Order Modeling), can improve flexibility and performance.

## LBM and Reduced Order Modeling (ROM)

While LBM itself is a simulation method, it can also benefit from Reduced Order Modeling techniques:
- **ROM Integration**:
- Run LBM for multiple parameter sets (geometry changes, Reynolds number variations).
- Collect snapshots of velocity and pressure fields.
- Use POD or greedy algorithms to build a reduced-order model that approximates LBM solutions for new parameters at a fraction of the cost.

This synergy ensures that LBM-based simulations, already efficient, can become even more accessible for rapid design or control tasks.

### A Practical Guide

The Lattice-Boltzmann method (LBM) simulates fluid flows by tracking particle distribution functions on a lattice grid. To implement the LBM algorithm concretely, you must:

I. **Define the Problem Setup**

II. **Choose a Discrete Velocity Set**

III. **Initialize Data Structures**

IV. **Implement Collision and Streaming Steps**

V. **Enforce Boundary Conditions**

VI. **Compute Macroscopic Variables**

VII. **Run the Time Loop**

VIII. **Post-Process and Validate Results**

Below, we detail each step with a focus on hands-on implementation aspects, assuming a standard scenario like the D2Q9 model for incompressible flow in 2D.

#### 1. Define the Problem Setup

**Inputs**:

- **Domain size**: Physical domain dimensions $L_x \times L_y$.
- **Lattice resolution**: Number of lattice nodes in each direction, e.g., $N_x \times N_y$. This determines the grid spacing $\Delta x = L_x/N_x, \Delta y = L_y/N_y$.
- **Time step $\Delta t$**: Usually chosen such that the lattice speed of sound $c_s = \frac{1}{\sqrt{3}} \frac{\Delta x}{\Delta t}$ matches the required flow regime.
- **Flow parameters**: Density $\rho_0$ (often $\rho_0 = 1$ for simplicity), initial velocity field $u_0$, viscosity $\nu$.
- **LBM relaxation time**: $\tau$ related to viscosity by $\nu = c_s^2(\tau - \frac{\Delta t}{2})$.
- **Boundary conditions**: Type and placement (e.g., no-slip walls, inflow velocity profile, outflow conditions).

**Outputs**:

- Evolving fields of density $\rho(x,t)$ and velocity $\mathbf{u}(x,t)$.
- Possibly pressure fields (derived from $\rho$) and other flow quantities (vorticity, shear stress).
- Final flow fields at each time step or at the end of the simulation.

#### 2. Choose a Discrete Velocity Set

For a 2D simulation, the D2Q9 model is common. The discrete velocities $\{c_i\}$ for D2Q9 are:

$$c_i \in \{(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)\} \times c_l$$

with $c_l = \Delta x/\Delta t$. This gives 9 discrete directions (including rest).

**Weights $w_i$** for D2Q9:

$$w_0 = 4/9, \quad w_{1,2,3,4} = 1/9, \quad w_{5,6,7,8} = 1/36.$$

#### 3. Initialize Data Structures

**Memory Allocation**:

- Create a 2D array for each distribution function $f_i$. For D2Q9, you need 9 arrays, each of size $N_x \times N_y$.
- `double f[i][N_x][N_y];` for $i=0$ to $8$.
- Alternatively, store them in a single 3D array or a vector of length $9 * N_x * N_y$.
- Create arrays for macroscopic fields (density and velocity):
- `double rho[N_x][N_y];`
- `double ux[N_x][N_y];`
- `double uy[N_x][N_y];`

**Initialization**:
  
- Set initial density $\rho_0 = 1.0$ (commonly used).
- Set initial velocity field $(u_{x}, u_{y}) = (0,0)$ or a desired initial flow (e.g., a uniform inflow at the left boundary).
- Compute initial equilibrium distributions $f_i^{\text{eq}}(\rho_0, u_x, u_y)$ at each cell using:
$$f_i^{\text{eq}} = w_i \rho_0 \left[ 1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2c_s^4} - \frac{u \cdot u}{2 c_s^2} \right].$$
- Set $f_i(x,y,0) = f_i^{\text{eq}}$.

#### 4. Implement Collision and Streaming Steps

At each time step:

I. **Collision Step**:

- For each lattice cell (x,y):
- Compute local $\rho, u_x, u_y$.
- Compute equilibrium distributions $f_i^{\text{eq}}$.
- Relax towards equilibrium:

$$f_i^*(x,y) = f_i(x,y) - \frac{\Delta t}{\tau} [f_i(x,y) - f_i^{\text{eq}}(x,y)].$$

II. **Streaming Step**:

- Move the post-collision distributions along $c_i$:
- For each $i$, for each cell (x,y):
- Compute new coordinates: $x' = x + c_{ix}, y' = y + c_{iy}$.
- If $(x',y')$ is within the domain, set:

$$f_i(x',y',t+\Delta t) = f_i^*(x,y,t).$$

- Else handle boundary conditions if stream crosses boundary.

Careful indexing and data layout is crucial for efficiency. Often, you store $f_i^*$ separately or use a swap technique.

#### 5. Enforce Boundary Conditions

Boundary conditions ensure the correct physical behavior. Examples:

- **No-Slip Walls (Bounce-Back)**:
- If a lattice node lies on a wall, invert the direction of incoming velocities to simulate a no-slip condition:

$$f_{\bar{i}}(x,y) = f_i(x,y)$$

where $\bar{i}$ is the opposite velocity direction of $i$.

- **Inflow/Outflow**:
- On inflow boundaries, prescribe a desired velocity or density, then set equilibrium distributions with the given $\rho, u$.
- On outflow boundaries, allow distributions to pass through or apply minimal reflection conditions.
- **Moving Boundaries**:
- Modify bounce-back to account for moving walls by adjusting equilibrium distributions.

#### 6. Compute Macroscopic Variables

After streaming (and before the next collision step):

- For each cell (x,y):
- $\rho(x,y) = \sum_i f_i(x,y)$
- $\rho u_x(x,y) = \sum_i f_i(x,y) c_{ix}$
- $\rho u_y(x,y) = \sum_i f_i(x,y) c_{iy}$

Then:

$$u_x(x,y) = \frac{\sum_i f_i(x,y) c_{ix}}{\rho(x,y)}, \quad u_y(x,y) = \frac{\sum_i f_i(x,y) c_{iy}}{\rho(x,y)}.$$

#### 7. Run the Time Loop

Implement a main time-stepping loop:

```
for (int t = 0; t < T_max; t++) {
// Collision step
collision_step(f, f_eq, rho, ux, uy, tau);

// Streaming step
streaming_step(f);

// Apply boundary conditions
apply_boundary_conditions(f, ...);

// Compute macroscopic variables
compute_macroscopic(f, rho, ux, uy);

// (Optional) Check convergence or compute statistics
}
```

**Inputs to the Loop**:

- Initial distributions and parameters.
- Maximum time steps `T_max` or stopping criteria based on residuals or convergence metrics.

**Outputs**:

- At the end of simulation: final fields $\rho(x), u_x(x), u_y(x)$ for all lattice cells.

#### 8. Post-Process and Validate Results

Post-processing involves:

- Saving results to files (e.g., VTK or HDF5 format) for visualization in Paraview or Tecplot.
- Comparing LBM results with analytical solutions (e.g., Poiseuille flow) or experimental data.
- Checking whether the flow features, such as recirculation zones or vortex shedding frequencies, match known phenomena.

**Validation and Calibration**:

- Adjust $\tau$ to match desired viscosity.
- Increase lattice resolution $N_x, N_y$ to ensure grid convergence.
- Compare velocity profiles along certain lines with reference solutions.

## Additional Refinements and Extensions

**Handling Non-Ideal Gases or Thermal Flows**:

- Introduce additional distribution functions for energy equations.
- Use extended discrete velocity sets.

**LES and Turbulence Modeling**:

- Incorporate subgrid-scale models or filtering strategies to handle turbulence in large domains or high Reynolds number flows.

**Complex Geometries**:

- Use immersed boundary methods or locally refined grids.
- Complex boundary conditions can be implemented using bounce-back rules adapted to curved or moving boundaries.

**Memory and Performance Considerations**:

- Optimize memory layout (SoA vs AoS), cache usage, and vectorization.
- Use MPI or OpenMP for parallelization.
