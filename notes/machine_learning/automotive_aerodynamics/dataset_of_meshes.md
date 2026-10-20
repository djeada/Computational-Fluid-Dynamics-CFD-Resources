# Building and Validating a Mesh Dataset

A surrogate trained on hundreds of CFD cases inherits any difference in how those cases were meshed. If one design gets a finer wake or a worse prism layer than its neighbours, the change in its drag becomes a label the model tries to learn. This note covers how to make a set of meshes that is good cell by cell and consistent across designs: geometry checks before meshing, cell quality metrics with their usual limits, consistency and outlier checks over the whole dataset, post-run $y^+$ and mesh-independence checks, coverage statistics of the accepted designs, and the storage and HPC costs of the campaign. The sampling of the designs is covered in [Design of Experiments and Dataset Construction](datasets.md), and the meshing rules themselves in [Generating CFD Training Data](generating_cfd_datasets.md).

## Problem Statement

A design of experiments gives $N$ parameter vectors $\mathbf{p}_1, \dots, \mathbf{p}_N \in [0, 1]^d$. Each is turned into a surface geometry $S_i$ and then into a volume mesh $`\mathcal{M}_i = G(S_i;\, R)`$ by a meshing procedure $G$ with a fixed set of rules $R$ (cell sizes, refinement regions, prism layers). For each mesh compute quality metrics $q_m(c)$ for every cell $c$ and accept the mesh when

```math
\max_{c \in \mathcal{M}_i} q_m(c) \le \tau_m \quad \text{for every metric } m,
```

with limits $\tau_m$ that depend on the solver. The dataset is acceptable when, in addition,

- the discretization error $\delta_{\mathrm{disc}}(\mathbf{p})$ of the labels is small and varies smoothly with $\mathbf{p}$, which requires $R$ to adapt to the geometry in the same way for every design;
- the accepted designs $`\{\mathbf{p}_i : \mathcal{M}_i \text{ accepted}\}`$ still cover the design space;
- the meshes, solutions and fields fit the compute and storage budget.

The hard part is that the meshes are generated automatically from morphed geometry, nobody inspects most of them, and a mesh can pass every cell-level check while still differing from its neighbours in a way that changes the forces.

## Geometry Checks Before Meshing

Errors in the surface are cheaper to catch before meshing than after a failed or wrong run.

- Watertightness: in a closed, manifold triangulation every edge is shared by exactly two faces. Count the edges with one or more than two adjacent faces; both counts must be zero.
- Topology: for a closed orientable surface of genus $g$ the Euler characteristic is $V - E + F = 2 - 2g$, with $V$, $E$, $F$ the numbers of vertices, edges and faces. A morph should not change $g$ relative to the baseline; a change means that a gap has closed or a hole has opened.
- Orientation: with outward normals the signed volume $V_S = \tfrac{1}{6}\sum_{\text{faces}} \mathbf{x}_a \cdot (\mathbf{x}_b \times \mathbf{x}_c)$ is positive, where $\mathbf{x}_a, \mathbf{x}_b, \mathbf{x}_c$ are the vertices of each triangle in order.
- Self-intersections and small gaps: a morph can push two surfaces through each other or close a gap below the target surface cell size, which the mesher then resolves differently from case to case.
- Fidelity to CAD: the two-sided Hausdorff distance $`d_H(S_i, S_{\mathrm{CAD}}) = \max\{\sup_{\mathbf{x} \in S_i} d(\mathbf{x}, S_{\mathrm{CAD}}),\ \sup_{\mathbf{y} \in S_{\mathrm{CAD}}} d(\mathbf{y}, S_i)\}`$ should stay below a tolerance tied to the surface cell size.

## Cell Quality Metrics

The table summarises the metrics most finite-volume solvers report, with typical limits. The limits are guidance, not universal rules; take the actual values from the solver's documentation and from experience with the baseline. More detail and tool commands are in [Mesh Quality Assessment](../../../practice/mesh_generation/mesh_quality.md).

| Metric | Definition | Ideal | Typical limit | What goes wrong |
| --- | --- | --- | --- | --- |
| Aspect ratio | Longest over shortest edge or cell dimension | 1 | about 20 to 100 in the core; much higher in prism layers aligned with the wall | Slow convergence and gradient errors when the stretching is not aligned with the flow |
| Equiangle skewness | Deviation of the cell angles from those of the ideal element | 0 | 0.85 maximum, average well below 0.3 | Interpolation errors, divergence |
| Non-orthogonality | Angle between the face normal and the line joining the two cell centres | $0^\circ$ | $65^\circ$ to $70^\circ$ maximum | Diffusion-flux error, needs non-orthogonal correctors |
| Face skewness | Distance from the face centre to where the centre-to-centre line crosses the face, relative to the centre distance | 0 | about 4 in OpenFOAM's checkMesh | Face-interpolation error |
| Volume ratio | Ratio of the volumes of neighbouring cells | 1 | about 5 to 10, except graded prism layers | Truncation error at size jumps |
| Jacobian determinant | $\det(\partial\mathbf{x}/\partial\boldsymbol\xi)$ of the element map, or its scaled form | 1 (scaled) | must be positive; scaled values below about 0.2 are often flagged | Inverted or degenerate elements |

### Equiangle Skewness

For an element whose ideal interior angle is $\theta_{\mathrm{ideal}}$ ($60^\circ$ for triangles and tetrahedral faces, $90^\circ$ for quadrilaterals and hexahedra),

```math
S_{\mathrm{eq}} = \max\left(\frac{\theta_{\max} - \theta_{\mathrm{ideal}}}{180^\circ - \theta_{\mathrm{ideal}}},\ \frac{\theta_{\mathrm{ideal}} - \theta_{\min}}{\theta_{\mathrm{ideal}}}\right)
```

where $\theta_{\max}$ and $\theta_{\min}$ are the largest and smallest angles of the cell. It ranges from 0 for an ideal element to 1 for a degenerate one.

### Non-Orthogonality

For a face $f$ shared by cells with centres $\mathbf{x}_P$ and $\mathbf{x}_N$, with $\mathbf{d} = \mathbf{x}_N - \mathbf{x}_P$ and face normal $\mathbf{n}_f$,

```math
\theta_f = \arccos\left(\frac{\mathbf{d} \cdot \mathbf{n}_f}{\|\mathbf{d}\|\,\|\mathbf{n}_f\|}\right)
```

The two-point gradient $`(\phi_N - \phi_P)/\|\mathbf{d}\|`$ only approximates the normal gradient at the face when $\theta_f = 0$. The remaining part is treated explicitly as a correction, which becomes large and destabilising as $\theta_f$ approaches $90^\circ$.

### Jacobian

Each element is the image of a reference element under a map $\mathbf{x}(\boldsymbol\xi)$. The Jacobian $J = \partial \mathbf{x}/\partial \boldsymbol\xi$ must have $\det J > 0$ everywhere in the element; $\det J \le 0$ at any corner means the element is degenerate or inverted. The scaled Jacobian at a corner of a hexahedron is the determinant of the three unit edge vectors leaving that corner, which lies in $[-1, 1]$. For a quadrilateral corner with angle $\theta$ it equals $\sin\theta$, so a $30^\circ$ corner gives 0.5.

## Consistency Across the Dataset

Each mesh can pass the cell-level limits while the dataset as a whole is still inconsistent. Consistency is a property of the meshing rules and is checked statistically.

- Use the same mesher, cell types, surface and volume refinement levels, and prism-layer specification (first height, growth ratio, number of layers) for every design.
- Attach refinement regions to the geometry (bounding box, named patches) so that they move with the morph.
- Record per-mesh statistics: cell count, maximum and mean of each quality metric, the number of cells over each limit, the prism-layer coverage (fraction of the wall area where all layers were added), and the minimum cell size.
- Flag outliers. The cell count should vary smoothly with $\mathbf{p}$. A robust test flags mesh $i$ when $`|N_i - \mathrm{median}(N)| > 3 \times 1.4826\,\mathrm{MAD}(N)`$, where $\mathrm{MAD}$ is the median absolute deviation and the factor 1.4826 makes it consistent with the standard deviation for normally distributed data. A sudden jump usually means a refinement rule triggered differently or prism layers collapsed.
- Regress the quality statistics on $\mathbf{p}$. A strong dependence of maximum skewness or of prism-layer coverage on one parameter shows where the rules will break near the edge of the range.

## Checks After the Runs

### $y^+$ Distribution

The near-wall resolution is only known after the solution exists. For each case compute the area-weighted distribution of $y^+$ over the vehicle surface and the fraction of the wall area inside the target band,

```math
\eta_{y^+} = \frac{\sum_{f \in \text{wall}} A_f\, \mathbf{1}\left[y^+_{\mathrm{lo}} \le y^+_f \le y^+_{\mathrm{hi}}\right]}{\sum_{f \in \text{wall}} A_f},
```

where $A_f$ is the area of wall face $f$ and $\mathbf{1}[\cdot]$ is 1 when the condition holds. For a wall-resolved mesh the band might be $y^+ \le 1$ to 2; for wall functions, $30 \le y^+ \le 300$. The value of $\eta_{y^+}$ should be high and similar across all cases. A design with much faster underbody flow, for example at low ground clearance, can push $y^+$ out of the band locally and should be flagged.

### Mesh Independence on a Subset

Mesh independence cannot be shown for every case, but it must be shown for a representative subset: the baseline plus designs at the extremes of the space, especially those with the most separation. Run each on three systematically refined meshes and compute the grid convergence index, as described in [Generating CFD Training Data](generating_cfd_datasets.md#grid-convergence-study). If the GCI differs strongly between designs, the discretization error is not uniform across the dataset and the mesh rules need refinement where it is largest.

### Validation and Visual Inspection

A small subset, typically 5 to 10% of the cases, should be compared with wind-tunnel data or higher-fidelity simulations where these exist. A consistent offset in $C_d$ across the subset is a systematic error that the surrogate will learn; it can be documented, but a large one indicates a problem with the setup (boundary conditions, $y^+$, the turbulence model) that should be fixed before the dataset is used. Visual inspection of a random sample of meshes and solutions catches problems that statistics miss, such as a refinement box missing a mirror or an unexpected recirculation zone.

## Coverage of the Design Space

Failed or rejected meshes remove points from the design, and the removed points are rarely random. After the quality gate, recompute the coverage statistics on the accepted set:

- the marginal histograms of each parameter and the 2D projections;
- a discrepancy measure, such as the centred $L_2$ discrepancy, compared with that of the planned design;
- the minimum pairwise distance, which detects near-duplicates;
- the fill distance $`h_X = \sup_{\mathbf{p} \in [0,1]^d} \min_i \|\mathbf{p} - \mathbf{p}_i\|`$, the radius of the largest empty ball, estimated by evaluating the inner minimum at a large random set of probe points;
- the rejection rate in each region of the design space.

![design space distribution](../../../scripts/plots/design_space_distribution/design_space_distribution.png)

The figure shows the planned 512-point scrambled Sobol design in four normalised parameters as a scatter matrix. The marginal histograms of the Sobol design are perfectly flat (32 points in each of 16 bins), while a random design of the same size ranges from 21 to 43 per bin. Each 2D projection has a centred discrepancy of about 0.0018, against 0.015 to 0.023 for the random design. Repeating the same plot for the accepted subset shows immediately whether rejected meshes have opened a gap, for example in the corner of low ground clearance and steep diffuser angle.

## Storage and HPC Scaling

The campaign cost is the sum over cases of meshing and solver time, and it is dominated by the solver. For a steady RANS case, solver time scales roughly with the number of cells times the number of iterations. Memory is often of order 1 to 2 GB per million cells for an incompressible RANS solver, which sets the minimum number of nodes per case.

The cases are independent, so the campaign is embarrassingly parallel across designs. If one case on $n_c$ cores takes $t(n_c)$ hours, a cluster with $P$ cores completes the campaign of $N$ cases in about

```math
T_{\mathrm{campaign}} \approx \frac{N\, n_c\, t(n_c)}{P}
```

hours. The product $`n_c\, t(n_c)`$ is the cost in core-hours per case, which grows with $n_c$ as the parallel efficiency falls. The campaign therefore finishes soonest when each case runs on the smallest core count that fits in memory and gives an acceptable turnaround, with many cases running side by side.

Storage grows with cells, fields and cases. A full-resolution volume field in double precision takes $8 N_{\mathrm{cells}} n_{\mathrm{fields}}$ bytes per case, plus the mesh. A dataset should keep three tiers: the full solutions archived (or at least the meshes, settings and restart data needed to regenerate them), the surface and selected volume fields at production resolution, and the decimated training representation described in [Design of Experiments and Dataset Construction](datasets.md#data-decimation).

## Key Takeaways

- Check the geometry before meshing: watertight, correct genus, outward normals, no self-intersections, close to CAD.
- Gate every mesh on skewness, non-orthogonality, aspect ratio, volume ratio and a positive Jacobian, using solver-specific limits.
- Consistency across designs matters as much as quality per cell; record mesh statistics and flag outliers with a robust test.
- Check the area-weighted $y^+$ distribution of every solution and the mesh independence of a representative subset.
- Recompute coverage statistics after rejecting meshes, because rejections cluster in difficult regions of the design space.
- Run many cases at modest core counts; parallel efficiency, not turnaround per case, sets the campaign time.

## Related Scripts

- [Design Space Distribution via Sobol Sequences](../../../scripts/plots/design_space_distribution/): draws a four-dimensional scrambled Sobol design of 512 geometry variants and shows all of its 2D projections and 1D marginals in a scatter matrix, with the discrepancy of each projection compared against a random design of the same size.
- [Sampling Strategies Comparison](../../../scripts/plots/sampling_strategies_comparison/): compares random, Latin hypercube and scrambled Sobol designs of the same size in a 2D design space, showing their point layouts, their 1D marginal histograms and how their centred $L_2$ discrepancy falls with the number of samples.
- [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/): estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008).

## Exercises

**Exercise 1.** A triangular surface cell has interior angles $30^\circ$, $60^\circ$ and $90^\circ$. A second triangle has angles $8^\circ$, $52^\circ$ and $120^\circ$. Compute the equiangle skewness of each and decide whether either exceeds the limit of 0.85.

<details>
<summary>Answer</summary>

For triangles $\theta_{\mathrm{ideal}} = 60^\circ$.

First cell: $(90 - 60)/(180 - 60) = 0.25$ and $(60 - 30)/60 = 0.5$, so $S_{\mathrm{eq}} = 0.5$. It is acceptable.

Second cell: $(120 - 60)/120 = 0.5$ and $(60 - 8)/60 = 0.867$, so $S_{\mathrm{eq}} \approx 0.87$, which exceeds 0.85. The small $8^\circ$ angle, not the obtuse angle, sets the value.

</details>

**Exercise 2.** Two cell centres are at $\mathbf{x}_P = (0, 0, 0)$ and $\mathbf{x}_N = (1, 0.4, 0)$ (in mm), and the shared face has normal $\mathbf{n}_f = (1, 0, 0)$. Compute the non-orthogonality angle. What lateral offset of $\mathbf{x}_N$ would give $71^\circ$?

<details>
<summary>Answer</summary>

$\theta_f = \arccos(1/\sqrt{1 + 0.4^2}) = \arctan(0.4) \approx 21.8^\circ$, which is acceptable.

For $71^\circ$ the offset must be $\tan 71^\circ \approx 2.9$ times the normal distance: $\mathbf{x}_N = (1, 2.9, 0)$ gives $\theta_f \approx 71.0^\circ$, above the usual limit of about $70^\circ$. Such faces appear where a refinement level changes next to a surface at an angle to the background grid.

</details>

**Exercise 3.** A prism layer starts with a first cell height $h_1 = 2 \times 10^{-5}$ m and grows with ratio 1.2 over 15 layers. The surface cells are 4 mm wide. Find the total thickness and the aspect ratios of the first and last layers, and say whether they are a problem.

<details>
<summary>Answer</summary>

```math
H = h_1 \frac{1.2^{15} - 1}{0.2} = 2 \times 10^{-5} \times \frac{1.2^{15} - 1}{0.2} \approx 1.44 \times 10^{-3}\ \mathrm{m}
```

The last layer is $h_1 \times 1.2^{14} \approx 2.57 \times 10^{-4}$ m thick.

The aspect ratios are $4 \times 10^{-3}/2 \times 10^{-5} = 200$ for the first layer and $4 \times 10^{-3}/2.57 \times 10^{-4} \approx 15.6$ for the last. A ratio of 200 is normal in a wall-aligned prism layer. The more important check is the jump from the 0.26 mm last layer to the 4 mm core cells, a factor of about 15, which should be reduced with more layers or a transition zone.

</details>

**Exercise 4.** Nine meshes of a dataset have cell counts (in millions) 18.2, 18.5, 17.9, 18.8, 18.4, 24.6, 18.1, 18.6 and 18.3. Apply the median-absolute-deviation test of the note. Which mesh is flagged, and what would you look for?

<details>
<summary>Answer</summary>

The median is 18.4. The absolute deviations are 0.2, 0.1, 0.5, 0.4, 0, 6.2, 0.3, 0.2 and 0.1, whose median is 0.2. The threshold is $3 \times 1.4826 \times 0.2 \approx 0.89$ million.

Only the mesh with 24.6 million cells deviates by more (6.2 million, about 21 robust standard deviations). A jump of a third in cell count from a small change in the design usually means that a refinement region was triggered differently, for example a proximity refinement in a narrowed gap, or that a feature was captured at a finer surface level. Compare its refinement regions and its quality statistics with those of its neighbours in the design space before accepting it.

</details>

**Exercise 5.** A campaign has 300 cases of 40 million cells. On 128 cores a case takes 16 h; on 512 cores it takes 5 h. The cluster has 2048 cores. Estimate the campaign time for both choices, and the raw storage for five double-precision volume fields per case.

<details>
<summary>Answer</summary>

On 128 cores: $300 \times 128 \times 16/2048 = 300$ h, with 16 cases running at once.

On 512 cores: $300 \times 512 \times 5/2048 = 375$ h, with 4 cases running at once.

Each case is faster on 512 cores, but the cost per case rises from 2048 to 2560 core-hours because the parallel efficiency is lower, so the campaign takes 25% longer.

Storage: $40 \times 10^6 \times 5 \times 8 = 1.6$ GB per case, or 480 GB for the campaign, before the mesh and restart files are counted.

</details>

## References

- Thompson, J. F., Soni, B. K., & Weatherill, N. P. (Eds.), *Handbook of Grid Generation*, CRC Press, 1999.
- Knupp, P. M., "Algebraic mesh quality metrics", *SIAM Journal on Scientific Computing*, 23(1), 193–218, 2001.
- Jasak, H., *Error Analysis and Estimation for the Finite Volume Method with Applications to Fluid Flows*, PhD thesis, Imperial College London, 1996.
- Ferziger, J. H., Perić, M., & Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- Roache, P. J., *Verification and Validation in Computational Science and Engineering*, Hermosa Publishers, 1998.
- Hampel, F. R., "The influence curve and its role in robust estimation", *Journal of the American Statistical Association*, 69(346), 383–393, 1974.
- Sobol', I. M., "On the distribution of points in a cube and the approximate evaluation of integrals", *USSR Computational Mathematics and Mathematical Physics*, 7(4), 86–112, 1967.
