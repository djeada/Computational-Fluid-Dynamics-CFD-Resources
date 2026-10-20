# POD-Galerkin Projection

POD-Galerkin projection turns the incompressible Navier–Stokes equations into a small system of ordinary differential equations for the amplitudes of a few POD modes. Because the convective term is quadratic in the velocity, the reduced system is quadratic in the amplitudes, and all its coefficients can be computed once from the modes. This note derives that system, explains how the pressure term and inhomogeneous boundary conditions are handled, how the procedure is carried out with a finite volume solver, why truncated models drift and how closure and stabilization fix this, and how the cylinder wake model of Noack et al. (2003) captures vortex shedding with three modes. The POD itself is covered in [`notes/numerical/pod/`](../pod/pod_intro.md); the general setting of projection-based reduced-order models (ROMs) is in [Reduced-Order Modeling](rom.md).

## Problem Statement

The full-order model (FOM) is the incompressible Navier–Stokes system in a domain $\Omega$ with boundary $\partial\Omega = \Gamma_{\mathrm{in}} \cup \Gamma_{\mathrm{w}} \cup \Gamma_{\mathrm{out}}$ (inflow, walls, outflow):

```math
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \nu\nabla^2\mathbf{u},
\qquad \nabla \cdot \mathbf{u} = 0,
\qquad \mathbf{u} = \mathbf{u}_{\mathrm{in}} \text{ on } \Gamma_{\mathrm{in}},
\quad \mathbf{u} = \mathbf{0} \text{ on } \Gamma_{\mathrm{w}},
\quad (\nu\nabla\mathbf{u} - p\mathbf{I})\mathbf{n} = \mathbf{0} \text{ on } \Gamma_{\mathrm{out}}
```

with velocity $\mathbf{u}(\mathbf{x}, t)$, kinematic pressure $p$ and viscosity $\nu$. A FOM run supplies snapshots $\mathbf{u}(\mathbf{x}, t_k)$, $k = 1, \dots, N_s$, and possibly $p(\mathbf{x}, t_k)$. The task is to find a reduced model

$$
\mathbf{u}(\mathbf{x}, t) \approx \mathbf{U}(\mathbf{x}) + \sum_{i=1}^{r}
a_i(t)\boldsymbol{\phi}_i(\mathbf{x})
$$

with a base field $\mathbf{U}$, $r$ POD modes $\boldsymbol{\phi}_i$ and ODEs for $\mathbf{a}(t) = (a_1, \dots, a_r)$ that reproduce the FOM over the training window and, ideally, beyond it or at nearby parameters, with a cost per time step independent of the number of cells. What makes it hard: the pressure enters the momentum equation but has no evolution equation of its own; inhomogeneous and time-dependent boundary conditions must be carried by $\mathbf{U}$; the truncated modes take with them most of the dissipation, so the reduced model can become unstable; and in a finite volume code the continuous derivation must be replaced by a consistent discrete one.

## Expansion and Lifting Function

The POD modes are computed from the snapshots minus the base field, $\mathbf{u}(\mathbf{x}, t_k) - \mathbf{U}(\mathbf{x})$, in the $L^2(\Omega)$ inner product $`(\mathbf{f}, \mathbf{g}) = \int_\Omega \mathbf{f} \cdot \mathbf{g} \, d\mathbf{x}`$, so they are orthonormal, $`(\boldsymbol{\phi}_i, \boldsymbol{\phi}_j) = \delta_{ij}`$ ([Snapshot POD](../pod/snapshot_pod.md)). The base field is chosen so that the modes satisfy homogeneous boundary conditions:

- If the inflow is steady, $\mathbf{U}$ can be the snapshot mean or a steady solution. Every snapshot satisfies the same Dirichlet data, so the fluctuations, and hence the modes, vanish on $\Gamma_{\mathrm{in}} \cup \Gamma_{\mathrm{w}}$.
- If the inflow changes in time or with a parameter, $`\mathbf{u}_{\mathrm{in}}(\mathbf{x}, t) = c(t)\mathbf{g}(\mathbf{x})`$, a lifting function $`\boldsymbol{\chi}`$ with $`\boldsymbol{\chi} = \mathbf{g}`$ on $`\Gamma_{\mathrm{in}}`$ and $\nabla \cdot \boldsymbol{\chi} = 0$ (for example a FOM solution with unit inflow) is used, $\mathbf{U}(\mathbf{x}, t) = c(t)\boldsymbol{\chi}(\mathbf{x})$, and the snapshots $\mathbf{u}(t_k) - c(t_k)\boldsymbol{\chi}$ are compressed. The coefficient $c(t)$ is then a known input of the reduced model.

The snapshots are divergence-free, so their linear combinations, the modes, are divergence-free too, $\nabla \cdot \boldsymbol{\phi}_i = 0$, and the expansion satisfies continuity for any $\mathbf{a}(t)$.

## Galerkin Projection

Substituting the expansion into the momentum equation and taking the inner product with $\boldsymbol{\phi}_i$ gives, by orthonormality,

$$
\frac{da_i}{dt} = \left(\boldsymbol{\phi}_i,\ - (\mathbf{u} \cdot \nabla)\mathbf{u} +
\nu\nabla^2\mathbf{u}\right) - (\boldsymbol{\phi}_i, \nabla p),
\qquad i = 1, \dots, r
$$

With $\mathbf{u} = \mathbf{U} + \sum_j a_j\boldsymbol{\phi}_j$ and a steady base field, the convective term splits into a constant, a linear and a quadratic part in $\mathbf{a}$, and the viscous term into a constant and a linear part. If the pressure term vanishes (next section), the result is the quadratic system

$$
\frac{d\mathbf{a}}{dt} = \mathbf{b} + L\mathbf{a} + Q(\mathbf{a}, \mathbf{a}),
\qquad Q(\mathbf{a}, \mathbf{a})_i = \sum_{j,k=1}^{r} Q_{ijk}a_ja_k
$$

with coefficients that depend only on the modes and the base field:

```math
b_i = \left(\boldsymbol{\phi}_i,\ \nu\nabla^2\mathbf{U} - (\mathbf{U} \cdot \nabla)\mathbf{U}\right),
\qquad
L_{ij} = \left(\boldsymbol{\phi}_i,\ \nu\nabla^2\boldsymbol{\phi}_j - (\mathbf{U} \cdot \nabla)\boldsymbol{\phi}_j - (\boldsymbol{\phi}_j \cdot \nabla)\mathbf{U}\right),
\qquad
Q_{ijk} = -\left(\boldsymbol{\phi}_i,\ (\boldsymbol{\phi}_j \cdot \nabla)\boldsymbol{\phi}_k\right)
```

The viscous terms are usually integrated by parts, $`(\boldsymbol{\phi}_i, \nabla^2\boldsymbol{\phi}_j) = -(\nabla\boldsymbol{\phi}_i, \nabla\boldsymbol{\phi}_j) + \oint \boldsymbol{\phi}_i \cdot (\nabla\boldsymbol{\phi}_j\,\mathbf{n})\,dS`$, which shows that the modal viscous operator is negative definite when the boundary terms vanish. The initial condition is the projection $a_i(0) = (\boldsymbol{\phi}_i, \mathbf{u}(\cdot, 0) - \mathbf{U})$.

The quadratic term conserves energy when the modes are divergence-free and vanish (or have $\boldsymbol{\phi} \cdot \mathbf{n} = 0$) on the boundary: integration by parts gives $`(\boldsymbol{\phi}_i, (\boldsymbol{\phi}_j \cdot \nabla)\boldsymbol{\phi}_k) = -(\boldsymbol{\phi}_k, (\boldsymbol{\phi}_j \cdot \nabla)\boldsymbol{\phi}_i)`$, so $`Q_{ijk} = -Q_{kji}`$ and

$$
\sum_{i,j,k} a_iQ_{ijk}a_ja_k = 0 \quad \text{for every } \mathbf{a}
$$

The reduced kinetic energy $E = \frac{1}{2}\lVert \mathbf{a} \rVert^2$ then changes only through $\mathbf{b}$ and $L$, as the fluctuation energy of the full flow changes only through production by the base flow and viscous dissipation. In practice open boundaries and discretization break this property slightly, which is one route to instability.

The online cost of the quadratic term is $O(r^3)$ per evaluation, independent of the mesh. The tensor has $r^3$ entries, so the approach is practical up to $r$ of order 100.

## Pressure Term

By the divergence theorem,

```math
(\boldsymbol{\phi}_i, \nabla p) = \oint_{\partial\Omega} p\,\boldsymbol{\phi}_i \cdot
\mathbf{n} \, dS - \int_\Omega p\,\nabla \cdot \boldsymbol{\phi}_i \, d\mathbf{x}
```

The volume integral vanishes for divergence-free modes, and the surface integral vanishes where the modes are zero (walls, Dirichlet inflow) and where $\boldsymbol{\phi}_i \cdot \mathbf{n} = 0$. For closed flows, such as a lid-driven cavity, the pressure therefore drops out of the reduced momentum equation altogether. For open flows the outflow integral remains; neglecting it is a modeling error that Noack, Papas and Monkewitz (2005) showed to be significant for shear layers, and it can be modeled from the pressure snapshots.

When the modes are only approximately divergence-free, the pressure must be reduced too, with its own POD basis $\psi_k$ and coefficients $b_k(t)$, $p \approx \sum_k b_k\psi_k$. A Galerkin projection of the momentum and continuity equations then gives a differential-algebraic system,

```math
\frac{d\mathbf{a}}{dt} = \mathbf{b} + L\mathbf{a} + Q(\mathbf{a}, \mathbf{a}) - G\mathbf{b}_p,
\qquad D\mathbf{a} = \mathbf{0},
\qquad G_{ik} = (\boldsymbol{\phi}_i, \nabla\psi_k), \quad D_{ki} = (\psi_k, \nabla \cdot \boldsymbol{\phi}_i)
```

whose velocity and pressure spaces do not in general satisfy a discrete inf-sup condition, so the reduced pressure is unstable. Two remedies are in use (Stabile and Rozza 2018):

- Supremizer enrichment adds to the velocity basis, for each pressure mode $\psi_k$, the supremizer $\mathbf{s}_k$ that solves $(\nabla\mathbf{s}_k, \nabla\mathbf{v}) = (\psi_k, \nabla \cdot \mathbf{v})$ for all test functions $\mathbf{v}$. This restores the inf-sup stability of the reduced pair (Ballarin, Manzoni, Quarteroni and Rozza 2015).
- The pressure Poisson approach takes the divergence of the momentum equation, $\nabla^2 p = -\nabla \cdot ((\mathbf{u} \cdot \nabla)\mathbf{u})$ with Neumann boundary conditions derived from the momentum equation, and projects this equation onto the pressure modes.

## Finite Volume Context

Most CFD codes are finite volume codes, which offer no weak form to project. The derivation above can still be carried out in two ways.

|  | Project, then discretize | Discretize, then project |
| --- | --- | --- |
| Reduced operators | integrals of the continuous terms, evaluated on the mesh with some quadrature | the code's own discrete operators applied to the modes, projected with the discrete inner product |
| Inner product | approximate $L^2$ by cell sums $`\sum_\ell \mathbf{f}_\ell \cdot \mathbf{g}_\ell V_\ell`$ | the same volume-weighted sum, consistent with the FOM |
| Consistency with the FOM | the ROM with all modes does not reproduce the FOM | the ROM with all modes reproduces the FOM trajectory |
| Implementation | independent of the solver | needs access to the solver's operators (intrusive) |

Discretize-then-project writes the FOM as a semi-discrete system $`d\mathbf{u}_h/dt = \mathbf{F}_h(\mathbf{u}_h)`$ on cell-centred values and projects it with $`M_V = \mathrm{diag}(V_\ell)`$: $da_i/dt = \boldsymbol{\phi}_i^TM_V\mathbf{F}_h(\mathbf{U} + \Phi\mathbf{a})$, with modes orthonormal in the volume-weighted product. If $\mathbf{F}_h$ is quadratic, as with central (linear-interpolation) convection, the operators $\mathbf{b}$, $L$ and $Q$ are obtained by applying the discrete convection and diffusion operators to the modes and pairs of modes. Lorenzi et al. (2016) and Stabile and Rozza (2018) describe this construction for OpenFOAM, including the face-flux modes needed by the discrete convective term. Upwind-biased schemes switch with the sign of the face flux and are only piecewise quadratic, and with limiters or turbulence models $\mathbf{F}_h$ is not polynomial at all. In those cases the eddy viscosity is expanded in its own modes with coefficients interpolated from the snapshots, or the nonlinear term is hyper-reduced ([Reduced-Order Modeling](rom.md)).

The volume weighting matters on non-uniform meshes: without it, small cells near walls are over-represented in the POD and the modes are not orthogonal in $L^2$ (Exercise 1).

## Example: Burgers Equation

The [POD-Galerkin Burgers script](../../../scripts/algorithms/pod_galerkin_burgers/) applies discretize-then-project to $u_t + uu_x = \nu u_{xx}$ on $(0, 1)$ with $u = 0$ at both ends and $\nu = 0.005$ m $`^2`$/s, discretized by central differences on 2000 points. A Gaussian pulse steepens into a front and moves to the right. The snapshots of $0 \le t \le 0.5$ s give the POD basis, and the reduced constant, linear and quadratic operators are computed once from it, exactly as above with $\mathbf{U}$ the snapshot mean.

![POD-Galerkin ROM of the viscous Burgers equation: field, profiles, POD spectrum, norm drift, error against r and cost](../../../scripts/algorithms/pod_galerkin_burgers/pod_galerkin_burgers.png)

Inside the training window the ROM error in panel (e) follows the projection error of the snapshots, the best any model in the same space could do: 16% at $r = 2$, 3.8% at $r = 5$, 0.34% at $r = 10$. Applied with the same basis at $\nu = 0.004$, the error stalls at 1.1%, and in the later window the front moves into a region no snapshot covered, so the error stays above 30% for every $r$. Panel (d) shows the stability issue: the ROM norm drifts above the FOM norm, by up to 6% at $r = 2$ inside the window and by 11% to 24% at $t = 1$ s. With all modes the ROM reproduces the FOM trajectory to round-off, which the unit test checks.

## Instability, Closure and Stabilization

The energy equation of the reduced system, $dE/dt = \mathbf{a}^T\mathbf{b} + \mathbf{a}^TL\mathbf{a}$ for an energy-conserving $Q$, contains production by the base flow and viscous dissipation of the resolved modes, but nothing for the energy that the nonlinear term would transfer to the truncated modes and that viscosity would dissipate there. In a flow where the small scales carry a significant part of the dissipation, a truncated Galerkin model therefore accumulates energy: amplitudes grow beyond the FOM values, limit cycles are too large, and some models diverge. The effect grows with the Reynolds number and with the severity of the truncation, and is worst when the model runs outside its training window.

Remedies, roughly in order of complexity:

1. Modal eddy viscosity: replace $\nu$ in $L$ by $\nu + \nu_T$, or add a mode-dependent viscosity $\nu_i$ that grows with the mode index, calibrated so that the ROM energy matches the snapshots. Wang, Akhtar, Borggaard and Iliescu (2012) compare several such closures; Östh et al. (2014) show that at high Reynolds number a nonlinear closure that scales with the resolved fluctuation energy is needed.
2. Calibration of the operators $\mathbf{b}$, $L$, $Q$ by least squares against the projected snapshots, often with energy conservation of $Q$ enforced as a constraint. This is close to operator inference ([Reduced-Order Modeling](rom.md)) and to the constrained regression described in [Modeling Flow Dynamics](../../machine_learning/flow/flow_dynamics.md).
3. Basis enrichment: include modes from transient snapshots, a shift mode for mean-flow changes, or modes that resolve the dissipative scales; Bergmann, Bruneau and Iollo (2009) combine such enrichment with residual-based stabilization.
4. Stabilized projections: Petrov–Galerkin and least-squares Petrov–Galerkin (LSPG) ROMs, which minimize the discrete residual instead of making it orthogonal to the modes.

## The Cylinder Wake

The flow past a circular cylinder at $Re = 100$ is the standard test of POD-Galerkin models. After a transient from the unstable steady solution, it settles on a limit cycle of periodic vortex shedding, and two POD modes, a conjugate pair with nearly equal energy, capture more than 90% of the fluctuation energy on that limit cycle. A two-mode Galerkin model built from limit-cycle snapshots reproduces the shedding frequency, but its amplitude is wrong and it describes the transient poorly: during the transient the mean flow changes from the steady solution to the time-averaged one, and the two oscillating modes cannot represent that change.

Noack, Afanasiev, Morzyński, Tadmor and Thiele (2003) added a shift mode $\boldsymbol{\phi}_\Delta$, the normalized difference between the mean flow and the steady solution, orthonormalized against the two oscillating modes. The resulting three-dimensional Galerkin system has the mean-field form

```math
\frac{da_1}{dt} = \sigma a_1 - \omega a_2 - \beta a_1a_\Delta,
\qquad
\frac{da_2}{dt} = \sigma a_2 + \omega a_1 - \beta a_2a_\Delta,
\qquad
\frac{da_\Delta}{dt} = -\sigma_\Delta a_\Delta + \kappa\,(a_1^2 + a_2^2)
```

with a growth rate $\sigma$, a frequency $\omega$ and positive coupling constants. The shift-mode amplitude relaxes quickly to $a_\Delta \approx (\kappa/\sigma_\Delta)A^2$, where $A^2 = a_1^2 + a_2^2$, which turns the quadratic system into the Landau equation $dA/dt = \sigma A - (\beta\kappa/\sigma_\Delta)A^3$ for the oscillation amplitude: exponential growth from the steady solution and saturation on a stable limit cycle (Exercise 5). The trajectories lie on a paraboloid in $(a_1, a_2, a_\Delta)$, which was later recovered from data by sparse regression ([Modeling Flow Dynamics](../../machine_learning/flow/flow_dynamics.md)). The model shows two general lessons: the base flow of a Galerkin model must be able to change with the fluctuation amplitude, and a well-chosen basis of three modes outperforms a poorly chosen one of many.

## Practical Workflow

1. Run the FOM and store snapshots of velocity (and pressure and face fluxes in a finite volume code) at a sampling interval that resolves the dynamics of interest, over the window and parameters the ROM must cover.
2. Choose the base field: snapshot mean, steady solution or lifting function, so that the modes satisfy homogeneous boundary conditions.
3. Compute the POD with the volume-weighted inner product and choose $r$ from the energy spectrum ([POD Introduction](../pod/pod_intro.md)).
4. Assemble $\mathbf{b}$, $L$ and $Q$ with the solver's own operators; decide how the pressure is treated (dropped for closed flows, boundary term, supremizers or pressure Poisson equation).
5. Integrate the ROM with an implicit or IMEX time scheme from the projected initial condition and compare with the FOM: coefficients, energy, and fields at a few times.
6. If the ROM drifts, check energy conservation of $Q$ and consistency of the operators (the full-rank ROM must reproduce the FOM), then add closure or stabilization.
7. Validate outside the training window and at new parameters before using the model.

## Key Takeaways

- Galerkin projection of incompressible Navier–Stokes onto orthonormal, divergence-free POD modes gives $`\dot{\mathbf{a}} = \mathbf{b} + L\mathbf{a} + Q(\mathbf{a}, \mathbf{a})`$ with coefficients computed once from the modes.
- The pressure drops out for closed flows; open flows leave a boundary term, and modes that are not exactly divergence-free need pressure modes with supremizers or a pressure Poisson equation.
- Inhomogeneous boundary conditions go into a base field or lifting function so that the modes satisfy homogeneous ones.
- In a finite volume code, discretize-then-project with a volume-weighted inner product gives a ROM consistent with the FOM.
- Truncated models lack the dissipation of the discarded modes and drift; modal eddy viscosity, calibration, basis enrichment (such as the shift mode of the cylinder wake) and stabilized projections are the remedies.

## Related Scripts

- [POD-Galerkin Reduced-Order Model of the Burgers Equation](../../../scripts/algorithms/pod_galerkin_burgers/): builds a POD-Galerkin reduced-order model (ROM) of the 1D viscous Burgers equation from snapshots of a 2000-point finite-difference solution, precomputes the reduced constant, linear and quadratic operators offline, and compares ROMs of 1 to 30 modes with the full-order model (FOM) inside the training window, in a later time window and at a new viscosity.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.
- [Lorenz Attractor Simulation](../../../scripts/simulations/lorenz_attractor/): integrates the Lorenz equations, a three-mode model of convection in a fluid layer heated from below, for 60 trajectories that start within $10^{-5}$ of one another and animates how they fan out over the butterfly-shaped attractor.

## Exercises

**Exercise 1.** A finite volume mesh has three cells with volumes $V_\ell = (1, 2, 1)$. For the cell-centred fields $\mathbf{u} = (1, 2, 1)$ and $\mathbf{v} = (1, -1, 1)$, compute the volume-weighted inner product $`(\mathbf{u}, \mathbf{v}) = \sum_\ell u_\ell v_\ell V_\ell`$ and the unweighted dot product. Are the fields orthogonal?

<details>
<summary>Answer</summary>

Weighted: $1 \cdot 1 \cdot 1 + 2 \cdot (-1) \cdot 2 + 1 \cdot 1 \cdot 1 = -2$. Unweighted: $1 - 2 + 1 = 0$. The fields are orthogonal in the Euclidean sense but not in the discrete $L^2$ sense. On non-uniform meshes the POD must use the volume-weighted product; otherwise small cells are over-represented and the modes are not $L^2$-orthogonal.

</details>

**Exercise 2.** On the mesh of Exercise 1, take $N_s = 2$ snapshots $\mathbf{u}_1 = (1, 1, 0)$ and $\mathbf{u}_2 = (0, 1, 1)$. Compute $`C_{ij} = \frac{1}{N_s}(\mathbf{u}_i, \mathbf{u}_j)`$, its eigenpairs, and the first POD mode $`\boldsymbol{\phi}_1 = \frac{1}{\sqrt{N_s\lambda_1}}\sum_k g_{1k}\mathbf{u}_k`$. Verify that $(\boldsymbol{\phi}_1, \boldsymbol{\phi}_1) = 1$, and find the norm obtained if the factor were $1/\sqrt{\lambda_1}$.

<details>
<summary>Answer</summary>

$(\mathbf{u}_1, \mathbf{u}_1) = 1 + 2 = 3$, $(\mathbf{u}_2, \mathbf{u}_2) = 2 + 1 = 3$ and $(\mathbf{u}_1, \mathbf{u}_2) = 2$. So $`C = \begin{pmatrix} 1.5 & 1 \\ 1 & 1.5 \end{pmatrix}`$, with $\lambda_1 = 2.5$, $\mathbf{g}_1 = (1, 1)/\sqrt{2}$ and $\lambda_2 = 0.5$.

$`\sum_k g_{1k}\mathbf{u}_k = (1, 2, 1)/\sqrt{2}`$, whose weighted squared norm is $(1 + 8 + 1)/2 = 5 = N_s\lambda_1$. Hence $\boldsymbol{\phi}_1 = (1, 2, 1)/\sqrt{10}$ and $(\boldsymbol{\phi}_1, \boldsymbol{\phi}_1) = (1 + 8 + 1)/10 = 1$. With the factor $1/\sqrt{\lambda_1}$ the squared norm would be $5/2.5 = 2 = N_s$, so the mode would not be normalized.

</details>

**Exercise 3.** The quadratic term of the ROM uses the tensor $Q_{ijk}$. How many entries does it have for $r = 10$, $50$ and $200$ modes? Compare the online cost of one reduced right-hand-side evaluation, $O(r^3)$, with one finite volume residual evaluation on $n = 10^6$ cells, $O(n)$.

<details>
<summary>Answer</summary>

The tensor has $r^3$ entries: $10^3 = 1000$, $50^3 = 1.25 \times 10^5$ and $200^3 = 8 \times 10^6$. For $r = 10$ or $50$ the reduced evaluation is much cheaper than an $O(10^6)$ residual. At $r = 200$ it costs as much as several full residuals. Quadratic POD-Galerkin models therefore pay off only for small $r$, which motivates hyper-reduction for larger bases or stronger nonlinearities.

</details>

**Exercise 4.** Apply Galerkin projection to the linear system $d\mathbf{u}/dt = A\mathbf{u}$ with

```math
A = \begin{pmatrix} -2 & 1 & 0 \\ 1 & -2 & 1 \\ 0 & 1 & -2 \end{pmatrix}, \qquad \mathbf{u}(0) = (1, 2, 1)^T
```

using the orthonormal basis $\boldsymbol{\phi}_1 = (1, 1, 1)/\sqrt{3}$ and $\boldsymbol{\phi}_2 = (1, 0, -1)/\sqrt{2}$. Compute $A_r = \Phi^TA\Phi$ and $\mathbf{a}(0) = \Phi^T\mathbf{u}(0)$, solve the reduced system, and compare $\Phi\mathbf{a}(1)$ with the exact solution $e^{A}\mathbf{u}(0)$.

<details>
<summary>Answer</summary>

$A\boldsymbol{\phi}_1 = (-1, 0, -1)/\sqrt{3}$ and $A\boldsymbol{\phi}_2 = (-2, 0, 2)/\sqrt{2}$, so $A_r = \mathrm{diag}(-2/3, -2)$. The initial coefficients are $\mathbf{a}(0) = (4/\sqrt{3}, 0)$. The reduced solution is $a_1(t) = (4/\sqrt{3})e^{-2t/3}$ with $a_2(t) = 0$, giving $\Phi\mathbf{a}(t) = \tfrac{4}{3}e^{-2t/3}(1, 1, 1)$. At $t = 1$ this is $(0.6846, 0.6846, 0.6846)$.

The exact solution is $e^{A}\mathbf{u}(0) = (0.6651, 0.9599, 0.6651)$. The error norm is $0.277$, a relative error of about 21%. The basis is poorly chosen: the slowest eigenvector of $A$ is $(1, \sqrt{2}, 1)/2$ (eigenvalue $-2 + \sqrt{2} \approx -0.586$), and it does not lie in the span of $\Phi$. A POD basis built from snapshots of the trajectory would contain that direction and reduce the error sharply.

</details>

**Exercise 5.** In the mean-field model of the cylinder wake, assume the shift mode is slaved, $a_\Delta = (\kappa/\sigma_\Delta)(a_1^2 + a_2^2)$. Show that the amplitude $A = \sqrt{a_1^2 + a_2^2}$ obeys $dA/dt = \sigma A - lA^3$ with $l = \beta\kappa/\sigma_\Delta$. For $\sigma = 0.05$ and $l = 0.02$ (in units of the shedding time scale), find the limit-cycle amplitude and the rate at which perturbations of the amplitude decay. What would a model without the shift mode predict?

<details>
<summary>Answer</summary>

$`A\,dA/dt = a_1\dot{a}_1 + a_2\dot{a}_2 = \sigma A^2 - \beta a_\Delta A^2`$, because the $\omega$ terms cancel. Dividing by $A$ and inserting $a_\Delta$ gives $dA/dt = \sigma A - (\beta\kappa/\sigma_\Delta)A^3$.

The fixed point is $A^* = \sqrt{\sigma/l} = \sqrt{2.5} \approx 1.58$. Linearizing, $d(\sigma A - lA^3)/dA = \sigma - 3lA^{*2} = -2\sigma = -0.1$, so perturbations of the amplitude decay at rate 0.1, twice the linear growth rate. Without the shift mode ($\beta = 0$) the model is $dA/dt = \sigma A$: exponential growth with no saturation, or, if $\sigma$ is set to zero to match the limit cycle, a neutral oscillation of whatever amplitude the initial condition has.

</details>

## References

- B. R. Noack, K. Afanasiev, M. Morzyński, G. Tadmor and F. Thiele, "A hierarchy of low-dimensional models for the transient and post-transient cylinder wake", *Journal of Fluid Mechanics* 497, 335–363, 2003.
- B. R. Noack, P. Papas and P. A. Monkewitz, "The need for a pressure-term representation in empirical Galerkin models of incompressible shear flows", *Journal of Fluid Mechanics* 523, 339–365, 2005.
- G. Stabile and G. Rozza, "Finite volume POD-Galerkin stabilised reduced order methods for the parametrised incompressible Navier–Stokes equations", *Computers & Fluids* 173, 273–284, 2018.
- S. Lorenzi, A. Cammi, L. Luzzi and G. Rozza, "POD-Galerkin method for finite volume approximation of Navier–Stokes and RANS equations", *Computer Methods in Applied Mechanics and Engineering* 311, 151–179, 2016.
- F. Ballarin, A. Manzoni, A. Quarteroni and G. Rozza, "Supremizer stabilization of POD–Galerkin approximation of parametrized steady incompressible Navier–Stokes equations", *International Journal for Numerical Methods in Engineering* 102(5), 1136–1161, 2015.
- Z. Wang, I. Akhtar, J. Borggaard and T. Iliescu, "Proper orthogonal decomposition closure models for turbulent flows: a numerical comparison", *Computer Methods in Applied Mechanics and Engineering* 237–240, 10–26, 2012.
- J. Östh, B. R. Noack, S. Krajnović, D. Barros and J. Borée, "On the need for a nonlinear subscale turbulence term in POD models as exemplified for a high-Reynolds-number flow over an Ahmed body", *Journal of Fluid Mechanics* 747, 518–544, 2014.
- M. Bergmann, C.-H. Bruneau and A. Iollo, "Enablers for robust POD models", *Journal of Computational Physics* 228(2), 516–538, 2009.
- C. W. Rowley, T. Colonius and R. M. Murray, "Model reduction for compressible flows using POD and Galerkin projection", *Physica D* 189(1–2), 115–129, 2004.
- P. Holmes, J. L. Lumley, G. Berkooz and C. W. Rowley, *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
