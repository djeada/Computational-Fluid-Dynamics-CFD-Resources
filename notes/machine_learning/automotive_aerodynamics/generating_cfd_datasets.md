# Generating CFD Training Data

A surrogate for vehicle aerodynamics learns from the outputs of a CFD pipeline, so it learns that pipeline's errors as well as the physics. This note covers how to run hundreds of external-aerodynamics simulations so that the labels are consistent from case to case, converged, and accurate enough for the design differences the model must resolve. It covers solver and turbulence-model choice, meshing rules, grid-convergence and iterative-convergence checks, automation with failure handling, and data extraction. Choosing where in the design space to run the cases is covered in [Design of Experiments and Dataset Construction](datasets.md), and checking the meshes in [Building and Validating a Mesh Dataset](dataset_of_meshes.md).

## Problem Statement

Let $\mathbf{p} \in \mathcal{P} \subset \mathbb{R}^d$ be the design parameters (for example the deformation parameters of [Deformation Parameters](deformation_parameters.md)) and let $\mathbf{y}(\mathbf{p})$ be the true quantities of interest: the drag coefficient $C_d$, lift coefficients, and surface fields such as the pressure coefficient $C_p$. A design of experiments supplies points $\mathbf{p}_1, \dots, \mathbf{p}_N$. The CFD pipeline $\mathcal{M}_h$ (geometry, mesh with characteristic size $h$, solver, turbulence model, averaging) returns labels

```math
\hat{\mathbf{y}}_i = \mathcal{M}_h(\mathbf{p}_i) = \mathbf{y}(\mathbf{p}_i) + \boldsymbol{\delta}_i,
\qquad
\boldsymbol{\delta}_i = \boldsymbol{\delta}_{\mathrm{model}} + \boldsymbol{\delta}_{\mathrm{disc}} + \boldsymbol{\delta}_{\mathrm{iter}} + \boldsymbol{\delta}_{\mathrm{avg}},
```

where the four terms are the modelling error (turbulence model, boundary conditions, geometric simplification), the discretization error, the iterative-convergence error and the statistical error of time averaging. Each run costs $c_i$ core-hours, and the campaign must satisfy $\sum_i c_i \le B$ for a budget $B$. The task is to choose the pipeline settings so that the dataset $`\mathcal{D} = \{(\mathbf{p}_i, \hat{\mathbf{y}}_i)\}_{i=1}^N`$ is as accurate as the budget allows and, above all, consistent.

Split the label error into a part common to all cases and a part that varies, $`\boldsymbol{\delta}_i = \mathbf{b} + \boldsymbol{\epsilon}_i`$. A surrogate $`f_{\boldsymbol\theta}`$ trained on $\mathcal{D}$ has error against the truth

```math
f_{\boldsymbol\theta}(\mathbf{p}) - \mathbf{y}(\mathbf{p}) = \underbrace{f_{\boldsymbol\theta}(\mathbf{p}) - \hat{\mathbf{y}}(\mathbf{p})}_{\text{surrogate error}} + \mathbf{b} + \boldsymbol{\epsilon}(\mathbf{p})
```

The common bias $\mathbf{b}$ shifts every prediction equally and cancels when two designs are compared. The varying part $\boldsymbol{\epsilon}$ does not cancel: it is noise (or, worse, a spurious trend) in the labels, and the test error of any surrogate measured against CFD labels cannot fall below its variance. The pipeline therefore has two targets. The varying error must be small compared with the design differences of interest (often a few drag counts, where one count is $\Delta C_d = 0.001$), and the settings that determine $\mathbf{b}$ must be identical for every case. This is hard because each case costs hundreds to thousands of core-hours, automatic meshing of morphed geometry fails in ways that depend on the geometry, and errors such as the position of a separation line can change abruptly across the design space.

## The Error Budget of a Label

| Error source | Controlled by | How it is estimated | Constant across the dataset? |
| --- | --- | --- | --- |
| Modelling, $\boldsymbol\delta_{\mathrm{model}}$ | Turbulence model, wall treatment, boundary conditions (moving ground, rotating wheels), geometric detail | Validation against wind-tunnel data or scale-resolving simulations on a few cases | Partly; it changes where the flow topology changes, for example when a rear-slant separation appears |
| Discretization, $\boldsymbol\delta_{\mathrm{disc}}$ | Mesh resolution and quality, discretization schemes | Grid-convergence study (GCI) on a subset | Only if the meshing rules adapt to the geometry in the same way for every case |
| Iterative, $\boldsymbol\delta_{\mathrm{iter}}$ | Number of iterations, residual and force-monitor criteria | Residual history, drift of averaged forces | No; it must be checked case by case |
| Averaging, $\boldsymbol\delta_{\mathrm{avg}}$ | Length of the averaging window for unsteady or oscillating solutions | Standard error of the time mean | No; it depends on the wake unsteadiness of each design |

When the numerical contributions are independent, they are combined as a root sum of squares, $U_{\mathrm{num}} = \sqrt{U_{\mathrm{disc}}^2 + U_{\mathrm{iter}}^2 + U_{\mathrm{avg}}^2}$. Modelling error is not reduced by refinement or longer runs and can only be bounded by validation. A practical rule is that $U_{\mathrm{num}}$ should be several times smaller than the smallest design difference the surrogate is expected to resolve.

## Solver Choice

The solver must be judged on the campaign, not on one showcase case. Commercial codes (Simcenter STAR-CCM+, Ansys Fluent) and open-source codes (OpenFOAM) are all used for road vehicles; the criteria that matter for dataset generation are these.

- The solver has to support the turbulence approach the labels need: steady RANS, unsteady RANS, or hybrid RANS-LES.
- Meshing and solving must run in batch from scripts with no manual steps, because a step that needs a person does not scale to hundreds of cases.
- Robustness on morphed geometry is worth more than peak accuracy on a clean baseline, since every diverged case costs time and leaves a hole in the design space.
- The cost per case is set by core count, parallel efficiency and licensing; with per-core licences the licence often costs more than the hardware.
- Solver version, schemes and settings must be frozen for the whole campaign. A version change halfway through introduces a step change in $\mathbf{b}$ between the two halves of the dataset.

## Turbulence Modelling

### RANS With $k$-$`\omega`$ SST

Steady incompressible RANS solves for the mean velocity $\bar{\mathbf{u}}$ and pressure $\bar{p}$ with the Boussinesq closure $`-\overline{u_i' u_j'} = 2\nu_t \bar{S}_{ij} - \tfrac{2}{3}k\,\delta_{ij}`$, where $\bar{S}_{ij}$ is the mean strain-rate tensor, $k$ the turbulent kinetic energy and $\nu_t$ the eddy viscosity (see [RANS Equations](../../fluid_mechanics/turbulence/rans_equations.md) and [Turbulence Modeling](../../numerical/cfd/turbulence_modeling.md)). The $k$-$`\omega`$ SST model of Menter computes $\nu_t$ from two transport equations, written here in the 2003 form:

```math
\frac{\partial (\rho k)}{\partial t} + \nabla \cdot (\rho \bar{\mathbf{u}} k) = \tilde{P}_k - \beta^* \rho k \omega + \nabla \cdot \left[(\mu + \sigma_k \mu_t)\nabla k\right]
```

```math
\frac{\partial (\rho \omega)}{\partial t} + \nabla \cdot (\rho \bar{\mathbf{u}} \omega) = \gamma \rho S^2 - \beta \rho \omega^2 + \nabla \cdot \left[(\mu + \sigma_\omega \mu_t)\nabla \omega\right] + 2(1 - F_1)\frac{\rho \sigma_{\omega 2}}{\omega}\nabla k \cdot \nabla \omega
```

```math
\nu_t = \frac{a_1 k}{\max(a_1 \omega,\ S F_2)},
\qquad
\tilde{P}_k = \min\left(\mu_t S^2,\ 10\,\beta^* \rho k \omega\right)
```

Here $\omega$ is the specific dissipation rate, $\mu$ and $\mu_t = \rho\nu_t$ the molecular and eddy viscosities, $`S = \sqrt{2\bar{S}_{ij}\bar{S}_{ij}}`$ the strain-rate magnitude, and $F_1$, $F_2$ blending functions of the wall distance that equal 1 near walls and tend to 0 in the free stream. Each coefficient $`\phi \in \{\gamma, \beta, \sigma_k, \sigma_\omega\}`$ is blended as $\phi = F_1 \phi_1 + (1 - F_1)\phi_2$ with $\gamma_1 = 5/9$, $\beta_1 = 0.075$, $\sigma_{k1} = 0.85$, $\sigma_{\omega 1} = 0.5$ (the $k$-$`\omega`$ set) and $`\gamma_2 = 0.44`$, $`\beta_2 = 0.0828`$, $`\sigma_{k2} = 1`$, $`\sigma_{\omega 2} = 0.856`$ (the transformed $k$-$`\varepsilon`$ set); $`\beta^* = 0.09`$ and $`a_1 = 0.31`$. The last term of the $`\omega`$ equation is the cross-diffusion term that the transformation from $`k`$-$`\varepsilon`$ introduces. The limiter in $\nu_t$ bounds the shear stress in adverse pressure gradients, which is the reason SST predicts separation better than standard two-equation models.

### Hybrid RANS-LES for Separated Wakes

RANS models are calibrated on attached boundary layers and simple shear flows. For bluff vehicle wakes they can misplace separation on a rear slant or a fastback and the base pressure that follows from it; the 25° Ahmed body is the standard example where RANS fails to reproduce the partly separated slant flow. Detached-eddy simulation (DES) replaces the RANS length scale $l_{\mathrm{RANS}} = k^{1/2}/(\beta^*\omega)$ in the destruction term of the $k$ equation by

```math
l_{\mathrm{DES}} = \min\left(l_{\mathrm{RANS}},\ C_{\mathrm{DES}}\,\Delta\right),
\qquad \Delta = \max(\Delta x, \Delta y, \Delta z),
```

so that the model acts as RANS in the attached boundary layer and as a subgrid model where the grid is fine enough to resolve eddies. Delayed DES (DDES) adds a shielding function that keeps thick attached boundary layers in RANS mode when the wall-parallel spacing is small.

The choice has direct consequences for the labels.

- Hybrid simulations are unsteady, so every label is a time average and carries an averaging error $\boldsymbol\delta_{\mathrm{avg}}$ that has to be controlled (see below).
- In LES regions the filter width is the grid, so mesh refinement changes the model as well as the discretization. Classical grid convergence does not apply there, and a GCI computed from hybrid results mixes the two effects.
- Hybrid RANS-LES costs roughly one to two orders of magnitude more than steady RANS for the same vehicle, which reduces $N$ for a fixed budget.
- Mixing RANS and hybrid labels in one dataset puts a model-dependent offset between the two subsets. If both are needed, keep a fidelity flag as an input or use a multi-fidelity surrogate (see [Hierarchical Kriging](../../numerical/surrogates/hierarchical_kriging.md)).

Steady RANS is a reasonable choice when the surrogate is used to rank designs whose flow topology is similar. Hybrid methods are needed when the design changes move separation lines, which is common for rear-end parameters.

## Meshing Strategy

### Near-Wall Resolution

The dimensionless wall distance of the first cell centre is $y^+ = u_\tau \Delta y / \nu$, with friction velocity $u_\tau = \sqrt{\tau_w/\rho}$ and wall shear stress $\tau_w$. Before the run $\tau_w$ is unknown, so it is estimated from a turbulent flat-plate correlation at a distance $x$ from the front of the vehicle:

```math
\mathrm{Re}_x = \frac{U_\infty x}{\nu},
\qquad
C_f \approx 0.0576\,\mathrm{Re}_x^{-1/5},
\qquad
\tau_w = \tfrac{1}{2}\rho U_\infty^2 C_f,
\qquad
\Delta y = \frac{y^+ \nu}{u_\tau}
```

The correlation is a power-law fit valid for roughly $5 \times 10^5 < \mathrm{Re}_x < 10^7$, and in a cell-centred finite-volume code the first cell height is about $2\Delta y$. A wall-resolved SST mesh targets $y^+ \approx 1$; wall functions need the first cell in the log layer, $30 \lesssim y^+ \lesssim 300$. A $y^+$ in the buffer layer ($5 < y^+ < 30$) should be avoided because neither treatment is accurate there. Details and tool-specific settings are in [Boundary Layer Meshing](../../../practice/mesh_generation/boundary_layers.md).

### Prism Layers

Prism layers grow geometrically from the first height $h_1$ with ratio $G$. After $n$ layers the total thickness is

```math
H = h_1 \frac{G^n - 1}{G - 1}
```

and the layer stack should cover the boundary-layer thickness, estimated for a turbulent flat plate as $`\delta \approx 0.37\,x\,\mathrm{Re}_x^{-1/5}`$. Growth ratios of 1.1 to 1.2 are typical. The height of the last layer should be close to the size of the adjacent core cells, otherwise the volume jump at the interface creates a local discretization error.

### Refinement Regions

Volumetric refinement boxes resolve the regions that set the forces: the wake (typically extending at least one vehicle length downstream), the underbody and diffuser, wheels and wheel arches, mirrors and the A-pillar. Octree-based mesh generators refine in levels that halve the cell size each time. For a dataset the rule is that refinement regions are defined relative to the geometry (the bounding box, or named surface patches that move with the morph), never at fixed coordinates, so that a design whose rear end moves keeps the same resolution of its wake. The domain size, blockage ratio and the boundary conditions (moving ground, rotating wheels) must also be identical for every case.

## Grid-Convergence Study

For a solution in the asymptotic range, a scalar output behaves as $\phi_h = \phi_{\mathrm{exact}} + C h^p + \mathcal{O}(h^{p+1})$, where $h$ is a representative cell size and $p$ the order of the scheme. Three meshes are enough to estimate $p$, the limit $\phi_{\mathrm{exact}}$ and an error band. For a 3D mesh of $N_k$ cells in a volume $V$, the representative size is $h_k = (V/N_k)^{1/3}$. Label the fine, medium and coarse meshes 1, 2, 3, so that $h_1 < h_2 < h_3$, with refinement ratios $r_{21} = h_2/h_1$ and $r_{32} = h_3/h_2$. Celik et al. (2008) recommend ratios of at least 1.3. With $\varepsilon_{21} = \phi_2 - \phi_1$, $\varepsilon_{32} = \phi_3 - \phi_2$ and $s = \mathrm{sign}(\varepsilon_{32}/\varepsilon_{21})$, the observed order solves

```math
p = \frac{1}{\ln r_{21}}\left|\ln\left|\frac{\varepsilon_{32}}{\varepsilon_{21}}\right| + q(p)\right|,
\qquad
q(p) = \ln\left(\frac{r_{21}^p - s}{r_{32}^p - s}\right),
```

by fixed-point iteration. For a constant ratio $r$, $q = 0$ and $p = \ln(\varepsilon_{32}/\varepsilon_{21})/\ln r$. A negative $s$ indicates oscillatory convergence, and the procedure is then unreliable. Richardson extrapolation and the grid convergence index (GCI) of Roache (1994) follow:

```math
\phi_{\mathrm{ext}} = \frac{r_{21}^p\,\phi_1 - \phi_2}{r_{21}^p - 1},
\qquad
\mathrm{GCI}_{\mathrm{fine}} = \frac{F_s}{r_{21}^p - 1}\left|\frac{\phi_1 - \phi_2}{\phi_1}\right|,
```

with safety factor $F_s = 1.25$ for three-grid studies. The GCI is a relative band intended to contain the exact value with about 95% confidence.

![Grid convergence index on a model problem and on drag coefficients](../../../scripts/algorithms/grid_convergence_index/grid_convergence_index.png)

The figure applies the procedure to a 1D advection-diffusion problem with a known wall gradient (panels a to c) and to illustrative drag values on 3.0, 7.5 and 20 million cells (panel d). On the model problem, meshes of 16, 32 and 64 cells give $p = 1.56$ although the scheme is second order, because the boundary layer is only just resolved; the observed order of consecutive triples approaches 2 only above about 200 cells (panel c). Even so, the GCI of 0.84% contains the true error of 0.53%, and the extrapolated value is in error by 0.14%. For the drag example ($r_{21} = 1.39$, $r_{32} = 1.36$) the script gives $p = 1.66$, $C_{d,\mathrm{ext}} = 0.3159$ and a GCI of 1.79%, or about $\pm 6$ counts.

For a dataset the study is run on a subset rather than on every case:

1. Pick the baseline and a few designs at the extremes of the design space, including the ones with the most separation.
2. Generate three meshes for each with the production meshing rules scaled by a global factor, so that every refinement region and the prism layers are scaled together while $y^+$ is held fixed.
3. Compute $p$, $\phi_{\mathrm{ext}}$ and the GCI for $C_d$ and for the other labels. An observed order far from the formal order, or oscillatory convergence, means the meshes are not in the asymptotic range.
4. Choose the production level so that the GCI is below the target, and record the GCI as the discretization uncertainty of the labels.
5. Check that the GCI of design differences $\Delta C_d$ between two designs is also acceptable. Discretization error often cancels partly between similar designs, but it is not guaranteed to, especially when the flow topology differs.

## Iterative Convergence and Averaging

A steady RANS solution is converged when further iterations do not change the labels. Residuals measure the imbalance of the discrete equations (see [Iterative Convergence](../../numerical/cfd/iterative_convergence.md)); a drop of three to four orders of magnitude is a common target. Residuals alone are not sufficient. Vehicle wakes often keep a steady RANS solver in a limit cycle in which the residuals plateau and the forces oscillate, and a slow drift can pass a per-iteration test indefinitely. The robust criteria use force monitors averaged over a window of $W$ iterations:

```math
\bar{C}_d^{(n)} = \frac{1}{W}\sum_{m=n-W+1}^{n} C_d^{(m)},
\qquad
\left|\bar{C}_d^{(n)} - \bar{C}_d^{(n-W)}\right| < \tau_{\mathrm{drift}},
\qquad
\mathrm{std}_W\left(C_d\right) < \tau_{\mathrm{osc}},
```

where $\tau_{\mathrm{drift}}$ and $\tau_{\mathrm{osc}}$ are tolerances (for example a fraction of a drag count) and the label is the windowed mean. The same rule, with the same $W$ and tolerances, must be applied to every case.

For unsteady simulations (URANS or hybrid RANS-LES), first discard the initial transient, typically several convective times $L/U_\infty$, where $L$ is the vehicle length. Then average over a window $T$. For a stationary signal with standard deviation $\sigma$ and integral time scale $T_{\mathrm{int}}$, the standard error of the time mean is approximately

```math
\sigma_{\bar{C}_d} \approx \sigma\sqrt{\frac{2 T_{\mathrm{int}}}{T}}, \qquad T \gg T_{\mathrm{int}},
```

so halving the averaging error costs four times the averaging time. Designs with larger wake unsteadiness need longer windows to reach the same $\sigma_{\bar{C}_d}$; using one fixed window for all cases gives labels whose noise varies across the design space.

## Automation and Failure Handling

A campaign of hundreds of cases needs a pipeline that runs without manual steps and records what it did:

1. Morph or regenerate the geometry for $\mathbf{p}_i$ and check that the surface is closed and free of self-intersections.
2. Mesh with the fixed rules and apply a quality gate (see [Building and Validating a Mesh Dataset](dataset_of_meshes.md)).
3. Run the solver with frozen settings and apply the convergence criteria automatically.
4. Extract the labels with one post-processing script.
5. Archive the inputs, the logs, the mesh statistics, the convergence history, the software versions and the wall time with every case.

Some cases fail at meshing or diverge. The tempting response, dropping them, biases the dataset. Let $r_i = 1$ if case $i$ succeeds. Failures are missing completely at random only if $P(r_i = 1)$ is the same for all designs, and in practice it never is: thin gaps, extreme angles and large separated regions are exactly what breaks meshers and solvers. When failure depends only on $\mathbf{p}$ (for example, the mesher fails on very low ground clearance), the successful cases are still valid samples, but they leave a hole in coverage at the edge of the design space, and the surrogate extrapolates there without warning. When failure depends on the flow itself (a solver that diverges whenever massive separation occurs), the data are missing not at random. A whole flow regime is then removed from the labels, and the surrogate learns a smoother world than the real one.

The handling has to be explicit and uniform.

- Log every failure with its cause and keep the failed designs in the dataset index.
- Retry with a fixed fallback sequence (more conservative relaxation, a first-order start, a modified mesh setting), apply it identically to every failed case, and flag the cases that needed it.
- Report the failure rate in each region of the design space. If failures cluster, either shrink the design space and document the new bounds, or train a feasibility classifier alongside the surrogate.
- Never replace a failed case silently with a nearby successful one.

## Consistent Data Extraction

Labels from different cases are comparable only if they are computed in the same way.

- Use the same reference area $A_{\mathrm{ref}}$, reference length, moment reference point and coordinate system for all cases, with $C_d = F_x / (\tfrac{1}{2}\rho U_\infty^2 A_{\mathrm{ref}})$ and $C_p = (p - p_\infty)/(\tfrac{1}{2}\rho U_\infty^2)$. If $A_{\mathrm{ref}}$ is the frontal area of each design, store it, because it changes with the geometry.
- Use one averaging window rule and one set of monitored surfaces (whether wheels and the underbody are included in the force, for example).
- Integrate the exported surface $p$ and wall shear stress to recompute the forces and compare them with the solver's force monitor. A mismatch reveals extraction errors such as missing patches or wrong normals.
- Store fields with their mesh, units and metadata in a self-describing format (HDF5, VTK), with the same field names in every file. Decimation of the fields for training is discussed in [Design of Experiments and Dataset Construction](datasets.md), and the output quantities in [Output Data](output_data.md).
- Validate a few cases against wind-tunnel data where it exists, comparing both forces and surface pressures. A systematic difference, such as a weaker separation plateau in the simulated $C_p$, belongs to $\mathbf{b}$ and must be documented with the dataset.

## Key Takeaways

- A label is the truth plus an error; the part of the error that varies between cases limits every surrogate trained on the data, while the common part cancels in design comparisons only if the pipeline is identical for all cases.
- Use SST RANS when the design changes keep the flow topology similar, and hybrid RANS-LES when they move separation; never mix the two without a fidelity flag.
- Size the first cell from a flat-plate estimate, define refinement regions relative to the geometry, and scale all mesh parameters together in a grid study.
- Estimate discretization uncertainty with the three-grid GCI on a subset that includes the extremes, and check the observed order before trusting it.
- Judge convergence from windowed force averages and their spread, and size averaging windows from the standard error of the mean.
- Failed runs are not missing at random; log them, retry them uniformly and report where in the design space they occur.

## Related Scripts

- [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/): estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008).
- [Variation of Residual with Iteration](../../../scripts/plots/variation_of_residual/): solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale.
- [Grid Convergence Comparison](../../../scripts/plots/comparing_grid_convergence/): illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$.
- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.

## Exercises

**Exercise 1.** The inlet of an SST case has $U = 40$ m/s, turbulence intensity $`I = 1\%`$ and turbulence length scale $\ell = 0.01$ m. Using $k = \tfrac{3}{2}(IU)^2$ and $\omega = k^{1/2}/(C_\mu^{1/4}\ell)$ with $C_\mu = 0.09$, compute $k$, $\omega$, the eddy viscosity $\nu_t = k/\omega$ and the ratio $\nu_t/\nu$ for air ($\nu = 1.5 \times 10^{-5}$ m²/s). Why must these values be identical across a dataset?

<details>
<summary>Answer</summary>

$k = 1.5 \times (0.4)^2 = 0.24$ m²/s².

$\omega = \sqrt{0.24}/(0.09^{1/4} \times 0.01) = 0.490/0.005477 \approx 89.4$ s⁻¹.

$\nu_t = 0.24/89.4 \approx 2.68 \times 10^{-3}$ m²/s, so $\nu_t/\nu \approx 179$.

The free-stream turbulence that reaches the vehicle depends on how $k$ and $\omega$ decay across the upstream domain, and it changes the skin friction and the separation predicted by SST. If the inlet values differed between cases, the change would appear in the labels as an effect of the design parameters.

</details>

**Exercise 2.** Air flows at $U = 30$ m/s ($\rho = 1.2$ kg/m³, $\nu = 1.5 \times 10^{-5}$ m²/s) over the roof, $x = 2$ m from the front of the vehicle. Use the flat-plate correlation of the note to find $\tau_w$, $u_\tau$ and the first-cell-centre distance $\Delta y$ for $y^+ = 1$ and for $y^+ = 50$. With a first cell height of $2\Delta y$ for $y^+ = 1$ and growth ratio 1.2, how many prism layers cover the boundary-layer thickness?

<details>
<summary>Answer</summary>

$\mathrm{Re}_x = 30 \times 2/(1.5 \times 10^{-5}) = 4 \times 10^6$, so $C_f = 0.0576 \times (4 \times 10^6)^{-0.2} \approx 2.75 \times 10^{-3}$.

$\tau_w = \tfrac{1}{2} \times 1.2 \times 30^2 \times 2.75 \times 10^{-3} \approx 1.49$ Pa and $u_\tau = \sqrt{1.49/1.2} \approx 1.11$ m/s.

For $y^+ = 1$, $\Delta y = \nu/u_\tau \approx 1.35 \times 10^{-5}$ m (13.5 µm). For $y^+ = 50$, $\Delta y \approx 0.67$ mm.

The boundary-layer thickness is $\delta \approx 0.37 \times 2 \times (4 \times 10^6)^{-0.2} \approx 0.035$ m. With $h_1 = 2.7 \times 10^{-5}$ m and $G = 1.2$, $H = h_1(1.2^n - 1)/0.2$ first exceeds 0.035 m at $n = 31$ ($H \approx 0.038$ m). The last layer is then about 6.4 mm thick. In practice the stack covers only the inner part of the boundary layer with fewer layers, and the core mesh resolves the outer part.

</details>

**Exercise 3.** A grid study with a constant refinement ratio $r = 2$ gives $C_d = 0.3350$ (coarse), $0.3210$ (medium) and $0.3170$ (fine). Compute the observed order $p$, the Richardson-extrapolated $C_d$ and the fine-grid GCI. Is the fine mesh adequate if the surrogate must resolve design differences of 5 counts?

<details>
<summary>Answer</summary>

```math
p = \frac{\ln\left(\frac{0.3350 - 0.3210}{0.3210 - 0.3170}\right)}{\ln 2} = \frac{\ln 3.5}{\ln 2} \approx 1.81
```

Since $r^p - 1 = 2.5$, $C_{d,\mathrm{ext}} = 0.3170 + (0.3170 - 0.3210)/2.5 = 0.3154$.

$`\mathrm{GCI}_{\mathrm{fine}} = 1.25 \times (0.0040/0.3170)/2.5 \approx 0.63\%`$, about $\pm 2$ counts.

The observed order is close to the formal order 2, which suggests the meshes are near the asymptotic range. The uncertainty of an absolute $C_d$ is 2 counts. Differences between similar designs are usually more accurate than that because part of the error cancels, so the mesh is adequate for 5-count differences, provided the same check on a design with different flow topology gives a similar GCI.

</details>

**Exercise 4.** A hybrid RANS-LES run gives an instantaneous $C_d$ signal with standard deviation 0.004 and integral time scale 0.02 s. The vehicle is 4.6 m long and $U_\infty = 40$ m/s. How long must the averaging window be for a standard error of the mean $C_d$ of 0.5 counts, and how many convective times is that? What happens to the dataset if every case uses a window of 0.64 s instead?

<details>
<summary>Answer</summary>

From $`\sigma_{\bar{C}_d} = \sigma\sqrt{2T_{\mathrm{int}}/T}`$, $T = 2T_{\mathrm{int}}(\sigma/\sigma_{\bar{C}_d})^2 = 2 \times 0.02 \times (0.004/0.0005)^2 = 2.56$ s.

One convective time is $L/U_\infty = 4.6/40 = 0.115$ s, so the window is about 22 convective times, on top of the discarded transient.

With $T = 0.64$ s (a quarter of the time) the standard error doubles to about 1 count for this design. Designs with a more unsteady wake would have even larger errors, so the label noise would vary across the design space and the surrogate would fit part of it as a design effect.

</details>

**Exercise 5.** In a campaign of 400 cases drawn uniformly over the design space, 30 fail. Of these, 24 have a diffuser angle in the top 20% of its range. Compute the failure rate inside and outside that region. What goes wrong if the failed cases are simply dropped, and what would you do instead?

<details>
<summary>Answer</summary>

The top 20% of the range contains about $0.2 \times 400 = 80$ cases, of which 24 fail: a failure rate of 30%. The other 320 cases have 6 failures, or about 1.9%.

Failure clearly depends on the design, so the cases are not missing completely at random. Dropping them leaves the high-diffuser-angle region with 56 instead of 80 samples, so the surrogate is less accurate exactly where the flow is most difficult. If the failures are caused by large diffuser separation, they are missing not at random, and the remaining labels under-represent that separated regime.

Instead, find the cause from the logs (a mesh-quality problem at the diffuser edge, or solver divergence with separation). Apply one fallback strategy to all failed cases and flag them. If the cases still fail, either reduce the upper bound of the diffuser angle and document it, or keep the failures as labelled infeasible points for a feasibility model, and report the failure map with the dataset.

</details>

## References

- Menter, F. R., "Two-equation eddy-viscosity turbulence models for engineering applications", *AIAA Journal*, 32(8), 1598–1605, 1994.
- Menter, F. R., Kuntz, M., & Langtry, R., "Ten years of industrial experience with the SST turbulence model", in *Turbulence, Heat and Mass Transfer 4*, Begell House, 625–632, 2003.
- Spalart, P. R., Deck, S., Shur, M. L., Squires, K. D., Strelets, M. K., & Travin, A., "A new version of detached-eddy simulation, resistant to ambiguous grid densities", *Theoretical and Computational Fluid Dynamics*, 20(3), 181–195, 2006.
- Roache, P. J., "Perspective: A method for uniform reporting of grid refinement studies", *Journal of Fluids Engineering*, 116(3), 405–413, 1994.
- Celik, I. B., Ghia, U., Roache, P. J., Freitas, C. J., Coleman, H., & Raad, P. E., "Procedure for estimation and reporting of uncertainty due to discretization in CFD applications", *Journal of Fluids Engineering*, 130(7), 078001, 2008.
- Wilcox, D. C., *Turbulence Modeling for CFD*, 3rd ed., DCW Industries, 2006.
- Pope, S. B., *Turbulent Flows*, Cambridge University Press, 2000.
- Little, R. J. A., & Rubin, D. B., *Statistical Analysis with Missing Data*, 3rd ed., Wiley, 2019.
