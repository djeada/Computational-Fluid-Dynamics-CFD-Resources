# Why CFD

Computational fluid dynamics (CFD) computes approximate solutions of the equations of fluid motion on a computer. This note explains why that is necessary, what a numerical solution actually is, how much it costs to resolve a flow, which families of discretization methods exist, and which errors separate a CFD result from the real flow. It is the entry point to the numerical-methods notes; the workflow that turns a flow problem into numbers is described in [The Strategy of CFD](./cfd_process.md), and the equations themselves in [Governing Equations for CFD](./governing_equations.md).

## Problem Statement

For an incompressible Newtonian fluid of constant density $\rho$ and kinematic viscosity $\nu$, the velocity $\mathbf{u}(\mathbf{x}, t)$ and pressure $p(\mathbf{x}, t)$ in a domain $\Omega$ satisfy

$$
\nabla\cdot\mathbf{u} = 0,
\qquad \frac{\partial\mathbf{u}}{\partial t} +
(\mathbf{u}\cdot\nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{u} +
\mathbf{f}
$$

for $t > 0$, with a body force $\mathbf{f}$, an initial velocity field $\mathbf{u}(\mathbf{x}, 0) = \mathbf{u}_0(\mathbf{x})$ and conditions on the boundary $\partial\Omega$ (prescribed velocity at walls and inlets, a pressure or traction condition at outlets; see [Boundary Conditions](./boundary_conditions.md)). Compressible flows add an energy equation and an equation of state, and the density becomes an unknown.

These equations rest on the continuum hypothesis: the mean free path $\lambda$ of the molecules must be much smaller than the length scale $L$ of the flow, so that the Knudsen number $Kn = \lambda/L$ is small. Below about $Kn = 10^{-3}$ the Navier–Stokes equations with no-slip walls apply; between $10^{-3}$ and $10^{-1}$ they can still be used with slip boundary conditions.

The system has no general closed-form solution. The convective term $(\mathbf{u}\cdot\nabla)\mathbf{u}$ is nonlinear, the pressure is coupled to the velocity through the divergence constraint rather than by an equation of its own, and at high Reynolds numbers the solutions are turbulent, with eddies over a range of scales that widens with $Re$. Even the existence of smooth solutions in three dimensions for all time is an open problem (one of the Clay Millennium Prize problems; Fefferman 2006). Exact solutions are known only for special geometries and simplified flows, such as Couette and Poiseuille flow, Stokes' oscillating plate, stagnation-point flow and the decaying Taylor–Green vortex. These are valuable as test cases, but an aircraft, a pump or an artery requires a numerical method.

A CFD calculation is considered solved when it delivers the quantities of interest (a drag coefficient, a pressure drop, a heat flux, a velocity profile) with an error that is known to be below a stated tolerance. Reaching that point means controlling every source of error listed below.

## What a CFD Solution Is

A numerical method replaces the continuous fields by a finite set of numbers: values at the nodes of a grid, averages over the cells of a mesh, or coefficients of basis functions. With a mesh of characteristic spacing $h$ and a time step $\Delta t$, the derivatives and integrals in the equations are replaced by algebraic approximations, and the result is a large system of algebraic equations for the discrete unknowns $\phi_h$. Its solution is an approximation whose error, for a method of order $p$ in space and $q$ in time, behaves for small $h$ and $\Delta t$ as

$$
\lVert \phi - \phi_h \rVert \approx C_1 h^p + C_2 \Delta t^q
$$

where $\phi$ is the exact solution of the continuous equations and the constants $C_1$, $C_2$ depend on derivatives of $\phi$ but not on $h$ or $\Delta t$. For a second-order scheme, halving $h$ divides the spatial error by four.

This error is controllable only if the discrete problem converges to the continuous one. Convergence needs consistency (the truncation error vanishes as $h, \Delta t \to 0$) and stability (errors are not amplified without bound). For linear problems the Lax equivalence theorem states that a consistent scheme converges if and only if it is stable (Lax and Richtmyer 1956). Stability limits such as the CFL condition $C = u\Delta t/\Delta x \le 1$ for explicit advection schemes are treated in [Numerical Stability](./numerical_stability.md) and [Time Integration](./time_integration.md).

Three practical consequences follow. A CFD result is a member of a sequence of solutions on finer and finer meshes, and a single result says nothing about its own accuracy. The error can be estimated from two or three members of that sequence (Richardson extrapolation and the grid convergence index, in [Verification and Validation](./verification_and_validation.md)). And because the cost grows rapidly as $h$ decreases, every practical calculation is a compromise between accuracy and cost.

## The Cost of Resolving a Flow

A uniform 3D mesh of spacing $h$ in a domain of size $L$ has $(L/h)^3$ cells, so halving $h$ multiplies the cell count by 8. An explicit time integration also halves $\Delta t$ through the CFL condition, so the cost of an unsteady calculation grows by a factor of 16.

For turbulent flow the smallest scale that must be resolved is set by physics. In a direct numerical simulation (DNS), which resolves every eddy, the grid spacing must be of the order of the Kolmogorov scale $\eta$. The ratio of the integral scale $\ell_0$ to $\eta$ grows as

$$
\frac{\ell_0}{\eta} \sim Re^{3/4}
$$

where $Re$ is the Reynolds number of the energy-containing eddies. This is the number of grid points needed per spatial direction. In three dimensions the total number of points is therefore $N \sim (Re^{3/4})^3 = Re^{9/4}$. The time step must resolve the small eddies being swept past the grid, which adds another factor $Re^{3/4}$ in the number of steps, so the total work scales as $Re^3$ (Pope 2000; derivation in [Energy Cascade](../../fluid_mechanics/turbulence/energy_cascade.md)).

| $Re$ | Points per direction $\sim Re^{3/4}$ | Grid points $\sim Re^{9/4}$ | Relative work $\sim Re^3$ |
| --- | --- | --- | --- |
| $10^3$ | 180 | $5.6 \times 10^6$ | $10^9$ |
| $10^4$ | 1000 | $10^9$ | $10^{12}$ |
| $10^5$ | 5600 | $1.8 \times 10^{11}$ | $10^{15}$ |
| $10^6$ | 32000 | $3.2 \times 10^{13}$ | $10^{18}$ |

For wall-bounded flows the near-wall eddies scale with the viscous length, and Choi and Moin (2012) estimate that DNS of a flat-plate boundary layer of length $L_x$ needs $N \sim Re_{L_x}^{37/14}$ points, wall-resolved large-eddy simulation (LES) $Re_{L_x}^{13/7}$ and wall-modelled LES $Re_{L_x}$. A car at highway speed has $Re \approx 10^7$ based on its length, far beyond DNS. Engineering CFD therefore models the effect of turbulence instead of resolving it, with Reynolds-averaged Navier–Stokes (RANS) models or LES, as described in [Turbulence Modeling in CFD](./turbulence_modeling.md). The model is then a source of error that no mesh refinement removes.

## Families of Discretization Methods

The methods differ in what the discrete unknowns represent and in how the equations are approximated.

| Method | Discrete unknowns | How the equations are approximated | Conservation | Geometry | Typical use |
| --- | --- | --- | --- | --- | --- |
| [Finite difference](../fdm/intro.md) (FDM) | Point values $\phi_i$ at grid nodes | Derivatives replaced by difference quotients from Taylor series | Only if written in conservative form | Structured grids, or curvilinear grids by coordinate mapping | Simple geometries, high-order compact schemes, DNS of channel flow |
| [Finite volume](../fvm/intro.md) (FVM) | Cell averages $\bar\phi_i$ | Integral balance over each cell; fluxes reconstructed at faces | Exact in the discrete sense: what leaves one cell enters its neighbour | Any polyhedral mesh | Most commercial and open-source CFD codes (Fluent, STAR-CCM+, OpenFOAM) |
| [Finite element](../fem/intro.md) (FEM) | Coefficients of piecewise polynomial basis functions | Weighted residual (weak) form integrated over elements | Global; local only in special formulations | Unstructured meshes, curved elements | Structural coupling, incompressible flow, error estimation and adaptivity |
| [Spectral and discontinuous Galerkin](../high_order/intro.md) | Coefficients of global (spectral) or element-wise (DG) high-degree polynomials | Galerkin or collocation projection | Local in DG, global in spectral methods | Spectral: simple periodic or box domains; DG: unstructured meshes | DNS of turbulence, aeroacoustics, high-order LES |
| [Lattice Boltzmann](../lattice_boltzmann/intro.md) (LBM) | Particle distribution functions on a regular lattice | Discrete-velocity kinetic equation, streaming and collision | Mass and momentum by construction of the collision operator | Cartesian lattices with immersed boundaries | Porous media, multiphase flow, low-Mach transient aerodynamics on GPUs |

The choice is less exclusive than the table suggests. Finite-volume methods on uniform Cartesian grids reduce to conservative finite differences, and discontinuous Galerkin methods of degree zero are finite-volume methods.

## Sources of Error

The difference between a CFD prediction and the real flow has several distinct sources. They are estimated and reduced in different ways, so they must be kept apart.

| Source | Origin | How it is reduced or estimated |
| --- | --- | --- |
| Modelling error | The equations solved differ from reality: turbulence model, incompressibility, laminar assumption, idealized boundary conditions, simplified geometry | Validation against experiments; comparing models; higher-fidelity models |
| Discretization error | Truncation error of the spatial and temporal approximations on a finite mesh and time step | Mesh and time-step refinement studies; Richardson extrapolation and GCI |
| Iterative error | The algebraic system is solved only until a convergence criterion is met | Residual reduction by several orders of magnitude; monitoring the quantities of interest ([Iterative Convergence](./iterative_convergence.md)) |
| Round-off error | Finite-precision arithmetic, relative precision about $10^{-16}$ in double precision, amplified by ill-conditioned systems | Double precision; avoiding extreme mesh stretching; normally negligible |
| Input (parameter) error | Uncertain geometry, boundary values, fluid properties or operating conditions | Sensitivity studies and uncertainty propagation |

Verification addresses the numerical errors (discretization, iterative, round-off) and the correctness of the code. Validation addresses the modelling error by comparison with measurements, which have their own uncertainty. Both are described in [Verification and Validation](./verification_and_validation.md).

## Applications

| Field | Typical quantities of interest | Typical approach |
| --- | --- | --- |
| Aerospace | Lift, drag, moments, surface heat flux in re-entry | Compressible RANS; LES for high-lift and noise; shock-capturing schemes |
| Automotive | Drag and lift coefficients, cooling flow, cabin noise | Incompressible RANS or hybrid RANS–LES on 10 to 200 million cells |
| Turbomachinery | Efficiency, pressure ratio, blade loading | Rotating-frame or sliding-mesh RANS |
| Civil and environmental | Wind loads, natural ventilation, pollutant dispersion | Atmospheric boundary-layer RANS or LES |
| Chemical and process | Mixing time, residence-time distribution, heat-exchanger performance | Multiphase and reacting-flow models |
| Biomedical | Wall shear stress in arteries, airflow in the respiratory tract | Laminar or transitional incompressible flow with compliant walls |
| Energy | Wind-turbine wakes, combustor emissions | Actuator-line LES, reacting RANS or LES |

## Key Takeaways

- The Navier–Stokes equations have no general closed-form solution; CFD replaces them by an algebraic system on a mesh.
- A CFD solution is an approximation whose discretization error behaves as $C h^p$ and can be estimated only from a sequence of meshes.
- Convergence requires consistency and stability; for linear problems they are equivalent to convergence (Lax).
- DNS needs about $Re^{3/4}$ points per direction, $Re^{9/4}$ points in 3D and $Re^3$ work, so engineering flows rely on turbulence models.
- FDM, FVM, FEM, spectral/DG and LBM differ in what the unknowns represent; FVM dominates general-purpose CFD because it is conservative on any mesh.
- Modelling, discretization, iterative, round-off and input errors are distinct and need distinct remedies.

## Related Scripts

- [Continuous vs Discrete Domain](../../../scripts/plots/continuous_vs_discrete_domain/): illustrates the central step of CFD, replacing a field defined at every point of a continuous domain by values stored at a finite set of grid points, and measures the error this introduces for the model problem $du/dx + u = 0$, $u(0) = 1$.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib.

## Exercises

**Exercise 1.** The mean free path of air at sea level is about 68 nm. Compute the Knudsen number $Kn = \lambda/L$ for a car ($L = 1$ m) and for a microchannel ($L = 10$ µm). Is the no-slip continuum model safe in each case?

<details>
<summary>Answer</summary>

Car: $Kn = 6.8 \times 10^{-8}/1 = 6.8 \times 10^{-8}$. The continuum hypothesis is completely safe.

Microchannel: $Kn = 6.8 \times 10^{-8}/10^{-5} = 6.8 \times 10^{-3}$. This is in the slip-flow range: the Navier–Stokes equations can still be used, but with velocity-slip and temperature-jump wall conditions instead of no-slip.

</details>

**Exercise 2.** A car travels at 30 m/s in air ($\nu = 1.5 \times 10^{-5}$ m²/s, speed of sound 343 m/s) and is 4.5 m long. Compute the Reynolds and Mach numbers and decide whether the incompressible equations of the Problem Statement are appropriate. Estimate the relative density change from $\Delta\rho/\rho \approx Ma^2/2$.

<details>
<summary>Answer</summary>

$Re = 30 \times 4.5/(1.5 \times 10^{-5}) = 9 \times 10^6$, so the flow is turbulent and a turbulence model is required.

$Ma = 30/343 \approx 0.087$, so $`\Delta\rho/\rho \approx 0.087^2/2 \approx 0.4\%`$.

$Ma$ is well below the usual limit of 0.3, so the incompressible equations are appropriate.

</details>

**Exercise 3.** A virtual wind tunnel around the car is 20 m × 8 m × 6 m. How many cells does a uniform mesh with 1 cm cells need, and with 2 cm cells? What does this imply for mesh generation?

<details>
<summary>Answer</summary>

The domain volume is 960 m³.

1 cm cells: $960/10^{-6} = 9.6 \times 10^8$ cells. 2 cm cells: $960/(8 \times 10^{-6}) = 1.2 \times 10^8$ cells.

Halving the cell size multiplies the count by 8 in 3D. Uniform meshes are unaffordable, so practical meshes are fine only near the body, in the wake and in the boundary layer, and coarse far away.

</details>

**Exercise 4.** A DNS of homogeneous turbulence at $Re = 10^4$ (based on the energy-containing eddies) takes one week on a given computer. Using the scalings of this note, how many grid points does it need, and how long would runs at $Re = 2 \times 10^4$ and $Re = 10^5$ take?

<details>
<summary>Answer</summary>

Points: $Re^{9/4} = (10^4)^{9/4} = 10^9$, or $Re^{3/4} = 1000$ points per direction.

Work scales as $Re^3$. Doubling $Re$ multiplies the work by $2^3 = 8$, so 8 weeks (and the grid by $2^{9/4} \approx 4.8$). A tenfold increase multiplies the work by $10^3$: about 1000 weeks, or 19 years. This is why engineering CFD at $Re = 10^6$ to $10^8$ uses turbulence models.

</details>

**Exercise 5.** Classify each activity as verification or validation: (a) a grid-refinement study shows an observed order of 1.98 for a second-order scheme; (b) the predicted drag of a car is compared with wind-tunnel data; (c) a source term is added so that a chosen analytical function becomes the exact solution, and the code's error is measured; (d) the reattachment length behind a backward-facing step is compared with PIV measurements.

<details>
<summary>Answer</summary>

(a) Verification: it checks that the equations are solved correctly at the expected order.

(b) Validation: it checks the model against physical reality.

(c) Verification: this is the method of manufactured solutions, which checks the code against a known mathematical solution.

(d) Validation.

Verification should come first. Agreement with experiment on an unverified code may be the result of cancelling errors.

</details>

## References

- Anderson, J. D., *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
- Ferziger, J. H., Perić, M., & Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- Versteeg, H. K., & Malalasekera, W., *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Education, 2007.
- Pope, S. B., *Turbulent Flows*, Cambridge University Press, 2000.
- Choi, H., & Moin, P., "Grid-point requirements for large eddy simulation: Chapman's estimates revisited," *Physics of Fluids*, 24, 011702, 2012.
- Lax, P. D., & Richtmyer, R. D., "Survey of the stability of linear finite difference equations," *Communications on Pure and Applied Mathematics*, 9(2), 267–293, 1956.
- Fefferman, C. L., "Existence and smoothness of the Navier–Stokes equation," in Carlson, J., Jaffe, A., & Wiles, A. (eds.), *The Millennium Prize Problems*, Clay Mathematics Institute and American Mathematical Society, 57–67, 2006.
- Oberkampf, W. L., & Roy, C. J., *Verification and Validation in Scientific Computing*, Cambridge University Press, 2010.
