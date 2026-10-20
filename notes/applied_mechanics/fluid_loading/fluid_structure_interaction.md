# Fluid–Structure Interaction: Coupling Methods

When the deformation or motion of a structure changes the flow enough to change its load, the fluid and structural problems must be solved together. This note is about how that is done numerically: when one-way transfer of loads is enough, how monolithic and partitioned schemes couple a flow solver to a structural solver, why loosely coupled schemes fail for light structures in dense fluids (the added-mass instability) and how sub-iterations with relaxation cure it, how data are transferred between non-matching interface meshes, and how the fluid mesh follows the moving structure in the arbitrary Lagrangian–Eulerian (ALE) formulation without violating the geometric conservation law. The field equations and interface conditions are derived in the [FSI theory note](../../fluid_mechanics/specialized_topics/fluid_structure_interaction.md); this note assumes them and concentrates on algorithms.

## Problem Statement

A fluid occupies a domain $\Omega_f(t)$ and a structure a domain $\Omega_s(t)$, sharing a moving interface $\Gamma(t)$ with unit normal $\mathbf{n}$ pointing out of the structure. The fluid obeys the incompressible Navier–Stokes equations written on a moving mesh with velocity $\mathbf{w}$ (the ALE form),

$$
\rho_f\left(\left. \frac{\partial\mathbf{u}}{\partial t}\right|_{\chi} +
\left[(\mathbf{u} -
\mathbf{w})\cdot\nabla\right]\mathbf{u}\right) = \nabla\cdot\boldsymbol{\sigma}_f,
\qquad \nabla\cdot\mathbf{u} = 0
$$

where $|_\chi$ denotes the time derivative at a fixed mesh point and $\boldsymbol{\sigma}_f = -p\mathbf{I} + \mu(\nabla\mathbf{u} + \nabla\mathbf{u}^T)$. The structure obeys elastodynamics for the displacement $\mathbf{d}$, $\rho_s\ddot{\mathbf{d}} = \nabla\cdot\boldsymbol{\sigma}_s$. On the interface, the velocities match (kinematic condition) and the tractions balance (dynamic condition):

$$
\mathbf{u} = \dot{\mathbf{d}},
\qquad \boldsymbol{\sigma}_f\mathbf{n} = \boldsymbol{\sigma}_s\mathbf{n}
\qquad \text{on } \Gamma(t)
$$

and the fluid mesh must follow the interface. Given a fluid solver, a structural solver and the interface meshes of each, the task is to advance the coupled system in time so that both interface conditions hold to a chosen tolerance at every time step, the scheme is stable, and mass, momentum and energy are not created or lost at the interface. After spatial discretisation the structure is $`\mathbf{M}_s\ddot{\mathbf{d}} + \mathbf{C}_s\dot{\mathbf{d}} + \mathbf{K}_s\mathbf{d} = \mathbf{f}_\Gamma`$, where $`\mathbf{f}_\Gamma`$ is the fluid load mapped onto the structural nodes, typically from a [finite-element model](../../numerical/fem/intro.md).

## One-Way and Two-Way Coupling

In one-way coupling the information passes in one direction only:

1. Fluid to structure: a CFD solution on the undeformed geometry gives pressures and shear stresses that are mapped onto a structural model as loads, steady or as a time history. This is the standard route for wind and wave loads on stiff structures and for thermal and pressure loads on machine parts.
2. Structure to fluid: a prescribed motion (a pitching aerofoil, a forced oscillating cylinder, a known deflection) is imposed on the fluid mesh to measure the resulting forces, for example the flutter derivatives or added-mass and damping coefficients that later feed a structural model.

Two-way coupling is needed when the structural response changes the load. The decision can be made with a few estimates before any simulation:

| Indicator | One-way is usually adequate | Two-way is needed |
| --- | --- | --- |
| Deflection relative to the flow length scale, $\delta/D$ | Small (well below 1%) | Changes the shape seen by the flow |
| Structural velocity relative to the flow, $\dot{x}/U$ | Small | Comparable, so the relative velocity changes |
| Reduced velocity $U_r = U/(f_nD)$ | Far from lock-in and from aeroelastic onset speeds | Near VIV lock-in, galloping, flutter or divergence speeds |
| Added-mass ratio $m_a/m_s$ | Small (light fluid, heavy structure) | Of order 1 or larger (water, blood, thin shells) |
| Frequency content | Load frequencies far from structural frequencies | Load and natural frequencies close |

Weak two-way coupling captures most aeroelastic and VIV problems of stiff structures in air; strong coupling is required for light structures in water, parachutes, sails, heart valves and blood vessels.

## Monolithic and Partitioned Schemes

A monolithic scheme assembles the discretised fluid, structure and mesh-motion equations into one nonlinear system per time step and solves it with Newton's method, including the coupling blocks of the Jacobian:

```math
\begin{bmatrix} \mathbf{J}_{ff} & \mathbf{J}_{f\Gamma} & \mathbf{0} \\ \mathbf{J}_{\Gamma f} & \mathbf{J}_{\Gamma\Gamma} & \mathbf{J}_{\Gamma s} \\ \mathbf{0} & \mathbf{J}_{s\Gamma} & \mathbf{J}_{ss} \end{bmatrix}
\begin{bmatrix} \Delta\mathbf{x}_f \\ \Delta\mathbf{x}_\Gamma \\ \Delta\mathbf{x}_s \end{bmatrix} = -\begin{bmatrix} \mathbf{r}_f \\ \mathbf{r}_\Gamma \\ \mathbf{r}_s \end{bmatrix}
```

It satisfies the interface conditions exactly at convergence and is robust for strong coupling, but it needs a solver written for the coupled problem and preconditioners for a large, ill-conditioned block system. A partitioned scheme keeps a separate fluid solver and structural solver and exchanges interface data between them, which lets mature, specialised codes be reused and is how most industrial FSI is done.

|  | Monolithic | Partitioned |
| --- | --- | --- |
| Software | One code for the coupled system | Existing fluid and structural codes plus a coupling layer |
| Interface conditions | Exact at convergence | Satisfied to the coupling tolerance, or lagged |
| Strong coupling ($m_a \gtrsim m_s$) | Robust | Needs sub-iterations with relaxation or quasi-Newton acceleration |
| Cost per step | One large Newton solve | Several solver calls per step when strongly coupled |
| Non-matching meshes and time steps | Must be built into the formulation | Handled by the mapping and time-window logic |

### The Dirichlet–Neumann Partitioned Algorithm

The usual partitioned scheme gives the fluid the interface motion (a Dirichlet condition) and the structure the interface traction (a Neumann condition). One time step from $t^n$ to $t^{n+1}$:

1. Predict the interface displacement $\mathbf{d}_\Gamma^{n+1,(0)}$, for example from the previous step or by extrapolation.
2. Move the fluid mesh to match it and compute the mesh velocity.
3. Solve the fluid equations with the interface velocity as a boundary condition.
4. Integrate the interface traction and map it onto the structural interface ([Pressure Forces on Structures](./pressure_forces.md)).
5. Solve the structure for $\tilde{\mathbf{d}}_\Gamma^{n+1,(k+1)}$ with that load.
6. Compute the interface residual $`\mathbf{r}^{(k)} = \tilde{\mathbf{d}}_\Gamma^{(k+1)} - \mathbf{d}_\Gamma^{(k)}`$. Stop if it is below the tolerance; otherwise update the interface displacement with relaxation and return to step 2.

An explicit (loosely coupled, staggered) scheme performs steps 1–5 once per time step. An implicit (strongly coupled) scheme repeats steps 2–6 until the residual is small, which makes it equivalent at convergence to the monolithic scheme with the same time integrators. The roles can also be swapped (Neumann–Dirichlet), or both sides given Robin conditions, which mix motion and traction and improve the convergence for strong added-mass effects (Badia, Nobile and Vergara 2008).

## The Added-Mass Instability

### Scalar Model

Take one structural mode with mass $m_s$ and stiffness $k$ in an incompressible, inviscid fluid. The fluid pressure on the interface is proportional to the interface acceleration, $f = -m_a\ddot{x}$, with an added mass $m_a$ that depends on the fluid density and the geometry only ([Hydroelastic Applications](./hydroelastic_applications.md)). The structure is advanced with the Newmark average-acceleration rule. A loosely coupled scheme computes the fluid load from the previous acceleration:

```math
\left(m_s + \beta\Delta t^2k\right)a^{n+1} = -m_aa^n -
k\left[x^n + \Delta t\, v^n + \Delta t^2\left(\tfrac12 - \beta\right)a^n\right]
```

For small time steps the stiffness terms are negligible and the acceleration error obeys $`e^{n+1} \approx -(m_a/m_s)\,e^n`$. More precisely, for $\beta = \tfrac14$, $\gamma = \tfrac12$, a solution that changes sign every step ($\lambda = -1$) requires the displacement and velocity to vanish, and then $m_sa = m_aa$. The stability boundary is therefore exactly

$$
\frac{m_a}{m_s} = 1
$$

independent of the time step and the stiffness. This is the added-mass instability analysed by Causin, Gerbeau and Nobile (2005): explicit Dirichlet–Neumann coupling is unconditionally unstable when the added mass exceeds a threshold set by the structural mass, reducing the time step does not help, and in their model of a thin elastic wall the added-mass ratio grows with $\rho_f/\rho_s$ and with the slenderness of the domain. For an incompressible fluid the pressure on the wall responds instantly to its acceleration, so the lag of one step is enough to destabilise the scheme.

### Membrane Model and Stability Map

A tensioned membrane resting on a layer of fluid of depth $H$ with open ends makes the effect concrete. Each sine mode of wave number $k_j = j\pi/L$ has added mass per unit area $m_{a,j} = \rho_f\coth(k_jH)/k_j$, largest for the first mode, so the explicit scheme is stable only if $m_{a,1} < m_s$. The figure shows the partitioned coupling of a finite-difference membrane solver and a potential-flow fluid solver for a 10 mm steel plate ($m_s = 78.5$ kg/m²) on 0.2 m of water, for which $m_{a,1}/m_s = 7.28$.

![Sub-iteration residuals, growth of explicit coupling, stability map and wet-to-dry frequency ratios for a membrane on a fluid layer](../../../scripts/algorithms/fluid_loading_partitioned_fsi/fluid_loading_partitioned_fsi.png)

Panel (b) varies the fluid density: explicit coupling stays bounded at $m_{a,1}/m_s = 0.5$ and 0.95, grows slowly at 1.05 and diverges within 11 steps for water. Panel (c) is the spectral radius of the explicit scheme for one mode; the boundary is the horizontal line $m_a/m_s = 1$ at every time step. Panel (a) shows sub-iterations within one step: unrelaxed fixed-point iteration diverges by a factor 7.25 per iteration, while relaxation converges.

### Sub-Iterations and Relaxation

Within a step, the unrelaxed iteration on the interface load has the iteration matrix $`-(\mathbf{M}_s + \beta\Delta t^2\mathbf{K}_s)^{-1}\mathbf{M}_A`$, whose spectral radius is the largest modal ratio $`m_{a,j}/(m_s + \beta\Delta t^2k_j)`$. Smaller time steps make the iteration converge more slowly, the opposite of the usual experience with implicit schemes. Under-relaxation

```math
\mathbf{d}_\Gamma^{(k+1)} = \mathbf{d}_\Gamma^{(k)} + \omega_k\,\mathbf{r}^{(k)}
```

converges for a small enough constant $\omega$ (here $\omega < 2/(1 + 7.25) = 0.24$), but slowly when the modal ratios are spread over a wide range. Aitken's $\Delta^2$ method, as used for FSI by Küttler and Wall (2008), chooses the factor from the last two residuals,

```math
\omega_k = -\omega_{k-1}\,
\frac{\mathbf{r}^{(k-1)}\cdot\left(\mathbf{r}^{(k)} - \mathbf{r}^{(k-1)}\right)}{\left|\mathbf{r}^{(k)} - \mathbf{r}^{(k-1)}\right|^2}
```

at no extra cost, since it uses only interface vectors that are already available. For a scalar linear problem it gives the exact answer after two iterations. The same updates can be applied to the interface load instead of the displacement, which is what the membrane script does. There, in the first step, constant relaxation with $\omega = 0.2$ needs 60 sub-iterations and Aitken 29; over the whole run Aitken averages 25 per step and reproduces the monolithic solution to $4 \times 10^{-9}$. Interface quasi-Newton methods, which build a low-rank approximation of the inverse interface Jacobian from the residual history (IQN-ILS, Degroote, Bathe and Vierendeels 2009), usually converge in fewer iterations still and are the default in modern coupling libraries. The underlying fixed-point and Newton ideas are the same as for the nonlinearity of the flow equations themselves ([Dealing with Nonlinearity](../../numerical/cfd/dealing_with_nonlinearity.md)).

## Interface Data Transfer

The fluid and structural meshes rarely match on the interface: the fluid mesh is usually much finer, and shell or beam structural models do not even lie on the wetted surface. Two kinds of quantity cross the interface, and they need different treatments.

1. Motion goes from the structure to the fluid. Each fluid interface node takes its displacement by interpolation of the structural displacement field, $\mathbf{d}_f = \mathbf{H}\mathbf{d}_s$. This is a consistent mapping: a constant or linear field is reproduced exactly.
2. Load goes from the fluid to the structure. For the transfer to conserve the total force and the energy exchanged at the interface, the virtual work of the loads must be the same on both sides for every admissible interface motion, $\delta\mathbf{d}_s^T\mathbf{f}_s = \delta\mathbf{d}_f^T\mathbf{f}_f = \delta\mathbf{d}_s^T\mathbf{H}^T\mathbf{f}_f$. Hence the conservative mapping $\mathbf{f}_s = \mathbf{H}^T\mathbf{f}_f$ of nodal forces with the transpose of the motion interpolation (Farhat, Lesoinne and LeTallec 1998).

Conservative mapping preserves the resultant force and moment and the interface energy, but when the structural mesh is finer than the fluid mesh it can give a nodal load distribution with spurious peaks. Interpolating pressures (a consistent mapping of the traction field) gives smooth loads but does not preserve the total force exactly. Common interpolation operators $\mathbf{H}$ are nearest-neighbour projection, projection onto the faces of the other mesh, mortar (weighted-residual) methods, and radial basis functions, which need no connectivity and handle gaps between the two surfaces. Whatever is used, the integrated force and moment on both sides should be compared at every coupling step.

## Moving Meshes: ALE and the Geometric Conservation Law

### Mesh Motion

In the ALE formulation the interface nodes of the fluid mesh move with the structure, the nodes far away stay fixed or move as a rigid body, and the interior nodes move smoothly between them. The mesh displacement is usually obtained by solving an auxiliary problem with the interface displacement as boundary data:

| Method | Mesh displacement from | Notes |
| --- | --- | --- |
| Laplacian smoothing | $\nabla\cdot(\gamma\nabla\mathbf{d}_m) = 0$ | Cheap; a diffusivity $\gamma$ that grows near the body keeps boundary-layer cells undistorted |
| Pseudo-solid | Linear elasticity with stiffness raised in small cells | Better at preserving cell shapes under large rotations |
| Spring analogy | Edges as springs, sometimes with torsional springs | Simple, can tangle under large motion |
| Radial basis functions | Interpolation of boundary displacement into the volume | No connectivity needed; dense system for many boundary points |

When the motion is too large for any smoothing (rotating machinery, large flapping, contact), the alternatives are remeshing with solution transfer, overset (chimera) grids, sliding interfaces, or methods in which the structure moves through a fixed fluid mesh: immersed boundary, fictitious domain and cut-cell methods.

### Geometric Conservation Law

On a moving mesh the volume of each cell changes, and the discrete scheme must account for that change consistently with the fluxes through the moving faces. For every control volume $V(t)$ with face velocity $\mathbf{w}$,

```math
\frac{d}{dt}\int_{V(t)}dV = \oint_{\partial V(t)}\mathbf{w}\cdot\mathbf{n}\, dA
```

The geometric conservation law (Thomas and Lombard 1979) requires the discrete scheme to satisfy this identity exactly, which is equivalent to preserving a uniform flow on an arbitrarily moving mesh. A scheme that computes the new cell volumes from the node positions but the face fluxes from mesh velocities evaluated in an inconsistent way creates or destroys mass even in a uniform flow. Farhat, Geuzaine and Grandmont (2001) showed that satisfying the discrete geometric conservation law is a necessary condition for an ALE scheme to keep the nonlinear stability of its fixed-mesh counterpart, and the usual practice is to compute the swept volume of each face over the step and derive the mesh fluxes from it. The time integrator itself is discussed in [Time Integration](../../numerical/cfd/time_integration.md).

## A Typical Partitioned Setup

Industrial FSI is usually run with a CFD code, a finite-element code and a coupling layer, which may be built into one of the codes or be a separate coupling library, that handles communication, mapping, time windows and convergence acceleration. Setting up a two-way analysis generically involves:

1. Defining the wetted interface in both models, with consistent units, coordinate systems and normal orientations, and checking that the two surfaces overlap.
2. Choosing the mapping for motion (consistent) and load (conservative or consistent), and checking the transferred resultant force and moment against the integrated fluid force.
3. Choosing the time step common to both solvers (or a coupling window with sub-cycling), the explicit or implicit scheme, the convergence measure and tolerance on the interface residual, and the acceleration method.
4. Starting from a converged steady or periodic flow with the structure held fixed, then releasing it, to avoid a startup shock.
5. Monitoring the number of coupling iterations, the interface residual, the energy transferred across the interface and the mesh quality during the run.

Verification uses benchmarks with reference solutions. The best known is the cylinder with an attached elastic flag in laminar channel flow of Turek and Hron (2006), with cases from steady deflection to self-excited oscillation, which tests the fluid solver, the structural solver and the coupling separately and together ([Verification and Validation](../../numerical/cfd/verification_and_validation.md)).

## Worked Example: Is Explicit Coupling Safe?

Estimate the first-mode added-mass ratio $m_{a,1}/m_s = \rho_f\coth(k_1H)/(k_1\rho_sh_s)$, $k_1 = \pi/L$, for three cases.

1. An aluminium panel ($\rho_s = 2700$ kg/m³, $h_s = 2$ mm) of span 0.5 m in air ($\rho_f = 1.2$ kg/m³) over a deep cavity ($\coth \to 1$): $m_{a,1} = 1.2 \times 0.5/\pi = 0.19$ kg/m² against $m_s = 5.4$ kg/m², a ratio of 0.035. Explicit coupling is stable.
2. A 10 mm steel plate ($m_s = 78.5$ kg/m²) of span 1 m over 0.2 m of water: $m_{a,1} = 572$ kg/m², a ratio of 7.3. Explicit coupling diverges in a few steps.
3. An artery-like wall ($\rho_s = 1100$ kg/m³, $h_s = 0.5$ mm) with a 50 mm wavelength over a 4 mm fluid layer of density 1000 kg/m³: $k_1H = 0.25$, $m_{a,1} = 64.7$ kg/m² and $m_s = 0.55$ kg/m², a ratio of 118. Strong coupling with good acceleration, or a monolithic or Robin-based scheme, is essential.

The first is the situation of most aeroelastic problems; the second and third explain why hydroelastic and haemodynamic FSI were where the added-mass instability was first noticed.

## Key Takeaways

- Decide between one-way and two-way coupling from deflection, structural velocity, reduced velocity, added-mass ratio and frequency proximity.
- Partitioned Dirichlet–Neumann coupling reuses existing solvers; implicit sub-iterations make it equivalent to the monolithic scheme at convergence.
- Explicit coupling is unstable when the added mass exceeds the structural mass, whatever the time step; smaller steps make sub-iterations converge more slowly.
- Aitken relaxation and interface quasi-Newton methods make strong coupling affordable.
- Map motion consistently and loads conservatively, and check resultant force and moment on both sides.
- Moving-mesh schemes must satisfy the discrete geometric conservation law.

## Related Scripts

- [Partitioned Fluid–Structure Coupling and the Added-Mass Instability](../../../scripts/algorithms/fluid_loading_partitioned_fsi/): couples a structure solver and a fluid solver through their interface in the Dirichlet–Neumann way used by partitioned FSI codes, and shows that explicit coupling becomes unstable once the added mass of the fluid exceeds the structural mass, whatever the time step, while implicit coupling with Aitken relaxation converges to the monolithic solution.
- [Surface Force Integration over Boundary Faces](../../../scripts/algorithms/fluid_loading_surface_force_integration/): integrates a surface pressure and wall-shear field over the flat faces of a body into a force and a moment, the same face sum a CFD code uses to report drag, lift and moment coefficients.
- [Vortex-Induced Vibration with a Wake Oscillator](../../../scripts/algorithms/fluid_loading_viv_wake_oscillator/): models vortex-induced vibration of an elastically mounted cylinder with the coupled structure and van der Pol wake oscillators of Facchinetti, de Langre and Biolley (2004).

## Exercises

**Exercise 1.** A structural mode with $m_s = 10$ kg and $k = 4000$ N/m is coupled explicitly, with the previous-step acceleration, to an incompressible fluid with added mass $m_a = 15$ kg, using the Newmark average-acceleration rule with $\Delta t = 10^{-3}$ s. By roughly what factor does an acceleration error grow per step? Would halving the time step help?

<details>
<summary>Answer</summary>

$\beta\Delta t^2k = 0.25 \times 10^{-6} \times 4000 = 0.001$ kg, negligible beside $m_s$, so the error is multiplied by about $-m_a/(m_s + \beta\Delta t^2k) = -1.5$ per step, growing with alternating sign. Halving the time step makes the stiffness term even smaller and leaves the factor at 1.5: the threshold $m_a/m_s = 1$ does not depend on $\Delta t$. The fix is implicit coupling.

</details>

**Exercise 2.** For the same mode, the scheme is made implicit with constant under-relaxation of the interface load. Which values of $\omega$ converge, which value is optimal, and how many iterations would Aitken's method need?

<details>
<summary>Answer</summary>

The unrelaxed iteration multiplies the error by $-\mu$ with $\mu = 15/10.001 = 1.5$. With relaxation the factor is $1 - \omega(1 + \mu)$, so convergence needs $0 < \omega < 2/(1 + \mu) = 0.8$, and $\omega = 1/(1 + \mu) = 0.4$ makes the factor zero. For a scalar linear problem Aitken's update recovers this optimal factor from the first two residuals, so it converges after two iterations whatever the starting factor.

</details>

**Exercise 3.** A structural interface has two nodes at $x = 0$ and $x = 1$ m; the fluid interface has five nodes at $x = 0, 0.25, 0.5, 0.75, 1$ m, each carrying a fluid force of 1 N. Motion is interpolated linearly from structure to fluid. Find the structural nodal forces with the conservative mapping $\mathbf{f}_s = \mathbf{H}^T\mathbf{f}_f$, and with a mapping that samples the fluid force at the coincident nodes. Which conserves the total force, and is the work of the forces the same on both sides?

<details>
<summary>Answer</summary>

The interpolation weights of the structural node at $x = 0$ at the five fluid nodes are $1, 0.75, 0.5, 0.25, 0$, and those of the node at $x = 1$ are $0, 0.25, 0.5, 0.75, 1$. The conservative mapping gives $f_{s,0} = f_{s,1} = 2.5$ N, a total of 5 N, equal to the fluid total. Sampling gives 1 N at each node, a total of 2 N: 60% of the load is lost.

For any structural motion $(d_0, d_1)$ the fluid nodes move by $\mathbf{H}\mathbf{d}_s$, and $\mathbf{f}_f^T\mathbf{H}\mathbf{d}_s = (\mathbf{H}^T\mathbf{f}_f)^T\mathbf{d}_s$, so the conservative mapping transfers the same work. The sampled mapping does not.

</details>

**Exercise 4.** A 1D finite-volume cell has faces at $x_L(t)$ and $x_R(t)$ that move with velocities $w_L$ and $w_R$. A uniform flow carries a scalar $\phi_0$ at speed $u$. Write the explicit ALE update of the cell average and show that it preserves $\phi = \phi_0$ only if the volume change over the step equals $`\Delta t\,(w_R - w_L)`$. What goes wrong if the face velocities are evaluated at the old time level while the cell length is updated from the new node positions of an accelerating mesh?

<details>
<summary>Answer</summary>

The ALE balance of the cell is

```math
V^{n+1}\phi^{n+1} = V^n\phi^n - \Delta t\left[\phi_0(u - w_R) - \phi_0(u - w_L)\right] = V^n\phi_0 + \Delta t\,\phi_0\,(w_R - w_L)
```

with $\phi^n = \phi_0$. Hence $\phi^{n+1} = \phi_0$ if and only if $`V^{n+1} - V^n = \Delta t\,(w_R - w_L)`$, the discrete geometric conservation law for this cell. If the faces accelerate, the actual change of length from the node positions is $\Delta t$ times the average face velocity over the step, not the old-time velocity, so the two sides differ, and the uniform field changes by a factor $`(V^n + \Delta t\,\Delta w^n)/V^{n+1} \ne 1`$: mass is created or destroyed by the mesh motion alone.

</details>

**Exercise 5.** Using the membrane estimate $m_{a,1}/m_s = \rho_f\coth(k_1H)/(k_1\rho_sh_s)$, find the thickness of a steel plate ($\rho_s = 7850$ kg/m³) of span 1 m over 0.2 m of water above which a loosely coupled scheme would be stable. Is that a practical way out?

<details>
<summary>Answer</summary>

With $k_1 = \pi$ rad/m and $\coth(0.2\pi) = 1.796$, $m_{a,1} = 1000 \times 1.796/\pi = 572$ kg/m². Stability needs $7850h_s > 572$, that is $h_s > 73$ mm. The plate thickness is set by the design, not by the solver, so the remedy has to be numerical: strong coupling with relaxation or quasi-Newton acceleration, a Robin interface condition, or a monolithic solver.

</details>

## References

- Bungartz, H.-J., & Schäfer, M. (eds.), *Fluid-Structure Interaction: Modelling, Simulation, Optimisation*, Lecture Notes in Computational Science and Engineering 53, Springer, 2006.
- Hou, G., Wang, J., & Layton, A., "Numerical methods for fluid-structure interaction: a review," *Communications in Computational Physics*, 12(2), 337–377, 2012.
- Causin, P., Gerbeau, J.-F., & Nobile, F., "Added-mass effect in the design of partitioned algorithms for fluid-structure problems," *Computer Methods in Applied Mechanics and Engineering*, 194(42–44), 4506–4527, 2005.
- Küttler, U., & Wall, W. A., "Fixed-point fluid-structure interaction solvers with dynamic relaxation," *Computational Mechanics*, 43(1), 61–72, 2008.
- Degroote, J., Bathe, K.-J., & Vierendeels, J., "Performance of a new partitioned procedure versus a monolithic procedure in fluid-structure interaction," *Computers & Structures*, 87(11–12), 793–801, 2009.
- Badia, S., Nobile, F., & Vergara, C., "Fluid-structure partitioned procedures based on Robin transmission conditions," *Journal of Computational Physics*, 227(14), 7027–7051, 2008.
- Farhat, C., Lesoinne, M., & LeTallec, P., "Load and motion transfer algorithms for fluid/structure interaction problems with non-matching discrete interfaces," *Computer Methods in Applied Mechanics and Engineering*, 157(1–2), 95–114, 1998.
- Farhat, C., Geuzaine, P., & Grandmont, C., "The discrete geometric conservation law and the nonlinear stability of ALE schemes for the solution of flow problems on moving grids," *Journal of Computational Physics*, 174(2), 669–694, 2001.
- Thomas, P. D., & Lombard, C. K., "Geometric conservation law and its application to flow computations on moving grids," *AIAA Journal*, 17(10), 1030–1037, 1979.
- Turek, S., & Hron, J., "Proposal for numerical benchmarking of fluid-structure interaction between an elastic object and laminar incompressible flow," in Bungartz, H.-J., & Schäfer, M. (eds.), *Fluid-Structure Interaction*, LNCSE 53, Springer, 371–385, 2006.
