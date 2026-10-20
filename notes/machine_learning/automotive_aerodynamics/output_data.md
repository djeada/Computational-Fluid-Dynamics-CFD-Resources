# Output Data: CFD Results as Machine-Learning Targets

Every CFD run of the case study produces force histories, surface fields and volume fields, often several gigabytes per design. Before any of it can be used for training it has to be defined precisely, averaged to statistical convergence, mapped onto a representation shared by all designs and normalised; and once a model exists, its predictions have to be compared with CFD in ways that reveal where it fails. This note collects the definitions of the outputs, the file formats they are stored in, the statistics of time-averaging, the steps that turn raw outputs into ML targets, and the standard comparisons of prediction against CFD.

## Problem Statement

For design $i$ the solver delivers raw data $\mathcal{R}_i$ on its own mesh: time series of forces and moments, instantaneous or averaged fields on the body surface $\Gamma_i$ and in the fluid volume $\Omega_i$. The goal is a target vector

```math
\mathbf{y}_i = \mathcal{T}(\mathcal{R}_i) = \left(\overline{C_d}, \overline{C_l}, \dots,
\; \overline{C_p}(\boldsymbol\xi_1), \dots, \overline{C_p}(\boldsymbol\xi_M),
\dots\right)
```

where $\mathcal{T}$ includes time-averaging over a converged window, evaluation of surface fields at $M$ points $\boldsymbol\xi_m$ of a reference surface shared by all designs, and normalisation. The targets must satisfy two conditions. They must be comparable across designs (same definitions, reference values, axes and averaging procedure), and their statistical uncertainty must be small compared with the differences between designs that the model is expected to resolve. For drag that means a confidence interval on $\overline{C_d}$ well below one drag count.

The difficulties are that every design has a different mesh, that unsteady wakes produce force signals with long correlation times so that averages converge slowly, that field data is large, and that inconsistencies such as a different reference area or moment centre in a subset of runs are silent: they produce plausible-looking numbers that corrupt the training set.

## Output Types

| Category | Examples | Size per design | Typical ML use |
| --- | --- | --- | --- |
| Integral scalars | $C_d$, $C_l$, $C_s$, front and rear lift, pitch, roll and yaw moments | A few numbers | Regression targets, optimisation objectives |
| Time histories | $C_d(t)$, $C_l(t)$, probe signals | $10^3$ to $10^5$ samples per signal | Convergence checks, unsteady statistics, spectra |
| Surface fields | $\overline{C_p}$, $C_{p,\mathrm{rms}}$, $C_f$ vector, $y^+$ | $10^5$ to $10^7$ faces | Graph or point-cloud network targets, POD |
| Volume fields | $\overline{\mathbf{u}}$, $\overline{p}$, total pressure, turbulent kinetic energy | $10^7$ to $10^8$ cells | Field surrogates, wake analysis |
| Planes and lines | Wake slices, centreline $C_p$ | $10^4$ to $10^6$ points | Compact field targets, comparison with experiment |

A volume field with $10^8$ cells and five variables in single precision is already 2 GB per design, so datasets of thousands of designs usually keep volume data only on subsampled points, planes or a coarse background grid.

## Definitions

### Forces and Moments

The aerodynamic force is the surface integral of pressure and wall shear stress,

```math
\mathbf{F} = \oint_{\Gamma} \left[-(p - p_\infty)\,\mathbf{n} + \boldsymbol\tau_w\right]
dS = \mathbf{F}_p + \mathbf{F}_f
```

with $\mathbf{n}$ the outward unit normal of the body (pointing into the fluid). The pressure part $`\mathbf{F}_p`$ and the friction part $`\mathbf{F}_f`$ are worth storing separately: for passenger cars the pressure part dominates drag. With $`q_\infty = \tfrac{1}{2}\rho U_\infty^2`$, frontal area $A$ and wheelbase $L_{wb}$,

$$
C_d = \frac{F_x}{q_\infty A},
\qquad C_s = \frac{F_y}{q_\infty A},
\qquad C_l = \frac{F_z}{q_\infty A},
\qquad C_{m} = \frac{M_y}{q_\infty A L_{wb}}
$$

where $M_y$ is the pitching moment about a stated reference point, commonly the ground point midway between the axles. Front and rear axle lift are then often reported as $C_{l,f} = C_l/2 + C_m$ and $C_{l,r} = C_l/2 - C_m$; the sign conventions for the axes and for $C_m$ differ between organisations and must be recorded with the data.

### Surface Fields

The pressure and skin-friction coefficients are

$$
C_p = \frac{p - p_\infty}{q_\infty},
\qquad \mathbf{C}_f = \frac{\boldsymbol\tau_w}{q_\infty}
$$

$C_p = 1$ at a stagnation point and is negative where the flow accelerates around the body. The mean and the root-mean-square fluctuation $C_{p,\mathrm{rms}}$ of the surface pressure distinguish steady regions from separated, unsteady ones. With these coefficients the force coefficients can be recovered from the surface data,

```math
C_d = \frac{1}{A}\oint_\Gamma \left(-C_p\, n_x + C_{f,x}\right) dS
```

which is a consistency check on stored data and on predicted fields.

### Volume Fields

Besides the mean velocity and pressure, the total-pressure coefficient

$$
C_{p_0} = \frac{p + \tfrac{1}{2}\rho|\mathbf{u}|^2 - p_{0,\infty}}{q_\infty},
\qquad p_{0,\infty} = p_\infty + q_\infty
$$

is zero in loss-free flow and negative where viscous dissipation, separation or mixing has removed mechanical energy, so iso-surfaces of $C_{p_0}$ outline the wake and the vortices that cause drag. Vortex cores are commonly visualised with the $Q$ criterion,

```math
Q = \frac{1}{2}\left(\|\boldsymbol\Omega\|^2 - \|\mathbf{S}\|^2\right),
```

where $\mathbf{S}$ and $\boldsymbol\Omega$ are the symmetric and antisymmetric parts of the velocity-gradient tensor and $Q > 0$ marks regions where rotation dominates strain (Hunt et al., 1988).

## File Formats

| Format | Structure | Typical content | Remarks |
| --- | --- | --- | --- |
| VTK legacy and XML (`.vtk`, `.vtu`, `.vtp`, `.vtm`) | Points, cells and attached point or cell arrays; `.vtu` for unstructured volume grids, `.vtp` for surfaces, `.vtm` for multi-block collections | Surface and volume fields for visualisation and ML | Read by ParaView and VTK-based Python tools; XML variants support binary and compressed arrays |
| CGNS (`.cgns`) | Standardised hierarchy of bases, zones, grid coordinates, flow solutions and boundary conditions, usually stored in HDF5 | Complete CFD solutions including boundary-condition metadata | Designed for exchanging CFD data between solvers and tools |
| HDF5 (`.h5`) | General hierarchical container of named, chunked, compressed arrays with attributes | ML-ready arrays: point coordinates, fields, scalars, metadata | Efficient partial reads; the layout is defined by the dataset author |
| CSV or JSON | Plain text tables | Scalars, time histories, run metadata | Easy to inspect; unsuitable for large fields |

A good ML dataset stores the scalars and metadata (parameters, reference values, solver settings, convergence statistics) in one table, and the fields in binary per-design files with a fixed array layout. Visualisation and inspection are covered in [ParaView](../../../practice/paraview/intro.md).

## Time-Averaging and Its Convergence

Scale-resolving simulations, and many nominally steady RANS runs of bluff bodies, produce force coefficients that fluctuate in time. The target is the mean over an averaging window of length $T$ that starts after the initial transient has decayed,

```math
\overline{C_d} = \frac{1}{T}\int_{t_0}^{t_0 + T} C_d(t)\, dt \approx
\frac{1}{N}\sum_{n=1}^{N} C_d(t_n)
```

with $N$ samples spaced $\Delta t$ apart. Successive samples are correlated, so the standard error of the mean is larger than $\sigma/\sqrt{N}$. With the sample variance $\sigma^2$ and the autocorrelation coefficients $\rho_k$ of the signal,

$$
\sigma_{\overline{C_d}}^2 \approx
\frac{\sigma^2}{N}\left(1 + 2\sum_{k=1}^{N-1}\left(1 - \frac{k}{N}\right)\rho_k\right)
\approx \frac{\sigma^2}{N_{\mathrm{eff}}},
\qquad N_{\mathrm{eff}} \approx \frac{T}{2T_{\mathrm{int}}}
$$

where $`T_{\mathrm{int}} = \int_0^\infty \rho(\tau)\,d\tau`$ is the integral time scale of the signal (Bendat and Piersol, 2010). A 95% confidence interval is $`\overline{C_d} \pm 1.96\,\sigma_{\overline{C_d}}`$. In practice the sum over $\rho_k$ is noisy and is replaced by the batch-means method: split the signal into $B$ consecutive batches much longer than $T_{\mathrm{int}}$, average each, and estimate $\sigma_{\overline{C_d}}$ from the standard deviation of the batch means divided by $\sqrt{B}$. The start of the window should be chosen by a transient-detection test, not by eye, and the same procedure must be used for every design so that differences between designs are not differences in averaging. Store the confidence interval with each target; it is the noise floor below which no model can be validated.

For steady RANS runs the analogue is iterative convergence. If the residuals stall and the forces oscillate, the forces are averaged over the last iterations and the amplitude of the oscillation is recorded as the uncertainty ([Iterative Convergence](../../numerical/cfd/iterative_convergence.md)).

## From Outputs to ML Targets

### Scalars

Scalar targets are standardised with statistics of the training designs only, $\tilde{y} = (y - \mu_{\mathrm{train}})/\sigma_{\mathrm{train}}$, separately for each output, so that $C_d$ and moments of different magnitude contribute comparably to a multi-output loss. Predictions are transformed back before errors are reported. Outputs that are physically related, such as $C_l$, $C_{l,f}$ and $C_{l,r}$, should be predicted in a consistent subset and the rest derived, so that the predictions cannot contradict each other.

### Surface Fields on a Common Representation

Field targets need a common set of points. Three cases occur.

1. Morphed meshes. When every design is produced by morphing the same baseline mesh, surface vertex $j$ corresponds to the same material point in every design, and the field is directly a vector of fixed length. This is the simplest and most accurate case.
2. Remeshed designs with a reference surface. Each design's field is interpolated to the vertices of a reference surface mesh that has been morphed to the design, by projecting each reference vertex onto the nearest face of the design surface and interpolating within that face.
3. Unrelated geometries. Without correspondence, models that work on each design's own mesh or point cloud (graph and point-cloud networks) take the field at its native points, and the loss is evaluated per design.

Because cell sizes vary by orders of magnitude over a car surface, losses and errors should be area-weighted,

$$
\mathcal{L}_{C_p} = \frac{\sum_{j} A_j \left(\hat{C}_{p,j} - C_{p,j}\right)^2}{\sum_j A_j}
$$

with $A_j$ the area associated with surface point $j$; otherwise the finely meshed wheels and mirrors dominate the loss. When fields are compressed with POD before regression ([POD](../../numerical/pod/pod_intro.md)), the same weighting enters as an area-weighted inner product.

### Volume Fields

Volume targets are usually sampled at fixed points (a Cartesian background grid, a set of wake planes) or at randomly sampled points per design for coordinate-based networks. Points inside the body are masked. Near-wall cells are often excluded because their values depend on the wall treatment and are better represented by the surface fields.

## Comparing Predictions with CFD

### Scalars

The parity plot of predicted against CFD values, with the line $y = x$ and bands of $\pm 1$ or $\pm 5$ drag counts, shows at a glance bias (points shifted off the line), scale errors (slope different from one) and outliers. It is accompanied by MAE and RMSE in drag counts and $R^2$ on held-out designs ([Training and Validation](../fundamentals/training_and_validation.md)). Because design studies often need correct rankings rather than exact values, the fraction of design pairs whose drag difference has the correct sign is a useful additional metric.

![Parity and error plots of two drag surrogates](../../../scripts/plots/drag_coefficient_prediction/drag_coefficient_prediction.png)

The figure shows why the parity plot should always be paired with a plot of the error in drag counts. Both synthetic surrogates lie on the identity line and have $R^2 > 0.997$. Surrogate B has a 4-count offset and a slope of 0.96, which the error plot exposes as a trend of about 30 counts across the range. That is enough to reverse the ranking of designs a few counts apart.

### Fields

For fields, the relative area-weighted $L^2$ error

```math
\varepsilon_{C_p} = \sqrt{\frac{\sum_j A_j\left(\hat{C}_{p,j} - C_{p,j}\right)^2}{\sum_j A_j\, C_{p,j}^2}}
```

summarises a design in one number, but the spatial distribution matters more. Maps of $\hat{C}_p - C_p$ on the surface, and of velocity differences on wake planes, show whether errors are spread uniformly or concentrated at separation lines, wheel wakes and the base, which is where force errors originate. Two further checks are cheap and revealing: integrate the predicted surface fields to obtain $C_d$ and compare with both the CFD value and the directly predicted scalar, and plot centreline profiles of $C_p$ against CFD and, where available, experiment.

## Key Takeaways

- Store force coefficients with their pressure and friction parts, reference values, axis conventions and moment reference point, and keep these identical across the dataset.
- Time-averaged targets carry a statistical uncertainty that depends on the integral time scale; estimate it, for example by batch means, and store it with each target.
- Surface field targets need a common representation: morphed meshes give exact correspondence, otherwise interpolate to a reference surface or use models that work on native meshes.
- Use area-weighted losses and errors for surface fields, and standardise scalars with training-set statistics only.
- Judge predictions with parity plots and errors in drag counts for scalars, and with spatial error maps and integrated forces for fields.

## Related Scripts

- [Drag Coefficient Prediction](../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient surrogates with held-out CFD values in a parity plot and an error plot, and shows that a high $R^2$ can hide errors of ten drag counts.
- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.
- [ML-CFD Surrogate Workflow](../../../scripts/plots/ml_cfd_workflow/): draws a schematic of the workflow for building a machine-learning surrogate of CFD results, from the design of experiments to deployment in an optimisation loop.

## Exercises

**Exercise 1.** The freestream has $U_\infty = 40$ m/s, $\rho = 1.2\ \mathrm{kg/m^3}$ and gauge pressure $p_\infty = 0$. At a point in the wake the gauge pressure is $p = -300$ Pa and the local speed is $|\mathbf{u}| = 45$ m/s. Compute $C_p$ and $C_{p_0}$, and state their values at a loss-free stagnation point.

<details>
<summary>Answer</summary>

$q_\infty = \tfrac{1}{2} \times 1.2 \times 40^2 = 960$ Pa, so $p_{0,\infty} = 960$ Pa and $C_p = -300/960 = -0.3125$.

The local total pressure is $-300 + \tfrac{1}{2} \times 1.2 \times 45^2 = 915$ Pa, so $C_{p_0} = (915 - 960)/960 \approx -0.047$, a small total-pressure loss.

At a loss-free stagnation point $\mathbf{u} = 0$ and $p = p_{0,\infty}$, so $C_p = 1$ and $C_{p_0} = 0$. A positive $C_{p_0}$ cannot occur without energy input (for example a fan), which makes it a useful sanity check on predicted fields.

</details>

**Exercise 2.** A drag signal has 4000 samples with standard deviation $\sigma = 0.008$ and autocorrelation $\rho_k = e^{-k/25}$. Compute the effective number of independent samples, using $1 + 2\sum_{k \ge 1}\rho_k = (1 + e^{-1/25})/(1 - e^{-1/25})$, and the 95% confidence half-width of $\overline{C_d}$ in drag counts. How many samples are needed for a half-width of 0.5 counts?

<details>
<summary>Answer</summary>

The correlation factor is $(1 + e^{-0.04})/(1 - e^{-0.04}) \approx 50.0$, so $N_{\mathrm{eff}} = 4000/50 = 80$. This matches $T/(2T_{\mathrm{int}})$ with $T_{\mathrm{int}} = 25$ samples.

$\sigma_{\overline{C_d}} = 0.008/\sqrt{80} \approx 8.9 \times 10^{-4}$, and the half-width is $1.96 \times 8.9 \times 10^{-4} \approx 1.75 \times 10^{-3}$, or 1.75 counts. Treating all 4000 samples as independent would give 0.25 counts, seven times too optimistic.

For 0.5 counts, $N_{\mathrm{eff}} = (1.96 \times 0.008/0.0005)^2 \approx 984$, so about $984 \times 50 \approx 49{,}200$ samples, 12.3 times the current run. Averaging error shrinks only as $T^{-1/2}$.

</details>

**Exercise 3.** Using $(\nabla\mathbf{u})_{ij} = \partial u_i/\partial x_j$ and Frobenius norms, evaluate $Q$ for (a) the simple shear $\mathbf{u} = (\gamma y, 0, 0)$ and (b) the solid-body rotation $\mathbf{u} = (-\omega_0 y, \omega_0 x, 0)$. What does this say about using $Q$ rather than vorticity magnitude to find vortices?

<details>
<summary>Answer</summary>

(a) The only nonzero gradient is $\partial u/\partial y = \gamma$, so $S_{12} = S_{21} = \gamma/2$ and $\Omega_{12} = -\Omega_{21} = \gamma/2$. Then $`\|\mathbf{S}\|^2 = \|\boldsymbol\Omega\|^2 = \gamma^2/2`$ and $Q = 0$.

(b) $\partial u/\partial y = -\omega_0$ and $\partial v/\partial x = \omega_0$, so $\mathbf{S} = 0$ and $`\|\boldsymbol\Omega\|^2 = 2\omega_0^2`$, giving $Q = \omega_0^2 > 0$.

A boundary layer has large vorticity but $Q \le 0$, so it is not flagged, while a vortex core, where rotation dominates strain, has $Q > 0$. $Q$ iso-surfaces therefore isolate vortices that a vorticity-magnitude plot would mix with every wall shear layer.

</details>

**Exercise 4.** For four test designs the CFD drag coefficients are $(0.300, 0.315, 0.290, 0.330)$ and the predictions $(0.302, 0.312, 0.291, 0.310)$. Compute MAE and RMSE, then repeat without the fourth design. What does the ratio RMSE/MAE reveal?

<details>
<summary>Answer</summary>

The absolute errors are $(0.002, 0.003, 0.001, 0.020)$.

- All four: MAE $= 0.0065$ and RMSE $= \sqrt{(4 + 9 + 1 + 400) \times 10^{-6}/4} \approx 0.0102$.
- First three: MAE $= 0.0020$ and RMSE $\approx 0.0022$.

The ratio RMSE/MAE is about 1.57 with the fourth design and 1.08 without it. A ratio well above one signals that a few large errors dominate; here one design, the one with the highest drag, is off by 20 counts. On a parity plot it would be an obvious outlier, and its surface error map is the first place to look for a flow feature the model has not learned.

</details>

**Exercise 5.** A simplified body has a front face of area 1 $\mathrm{m}^2$ with normal $n_x = -1$ and mean $C_p = 0.8$, and a rear (base) face of area 1 $\mathrm{m}^2$ with $n_x = +1$ and $C_p = -0.2$; the remaining faces are parallel to the flow. With $A = 1\ \mathrm{m}^2$, compute the pressure-drag coefficient. A predicted $C_p$ field has a uniform error of $+0.05$ on every face of the closed body. How much does that error change the integrated pressure drag, and what does that imply for field metrics?

<details>
<summary>Answer</summary>

$`C_{d,p} = -\frac{1}{A}\sum_j C_{p,j}\, n_{x,j} A_j = -[0.8 \times (-1) + (-0.2) \times 1] = 1.0`$. Of this, 0.8 comes from the front and 0.2 from the base suction.

A uniform offset $c$ adds $`-c\oint_\Gamma n_x\,dS`$ to the integral, and $`\oint_\Gamma \mathbf{n}\,dS = 0`$ for any closed surface, so the pressure drag is unchanged. The relative $L^2$ field error is nonetheless nonzero. Conversely, a small error concentrated on the base, where $n_x = 1$, goes straight into drag. Field error norms and integrated forces measure different things, and both must be reported.

</details>

## References

- Hucho, W.-H. (Ed.), *Aerodynamics of Road Vehicles*, 4th ed., SAE International, 1998.
- Katz, J., *Automotive Aerodynamics*, Wiley, 2016.
- Pope, S. B., *Turbulent Flows*, Cambridge University Press, 2000.
- Bendat, J. S., & Piersol, A. G., *Random Data: Analysis and Measurement Procedures*, 4th ed., Wiley, 2010.
- Hunt, J. C. R., Wray, A. A., & Moin, P., "Eddies, streams, and convergence zones in turbulent flows", Center for Turbulence Research Report CTR-S88, 193–208, 1988.
- Schroeder, W., Martin, K., & Lorensen, B., *The Visualization Toolkit: An Object-Oriented Approach to 3D Graphics*, 4th ed., Kitware, 2006.
- Poirier, D., Allmaras, S. R., McCarthy, D. R., Smith, M. F., & Enomoto, F. Y., "The CGNS System", AIAA Paper 98-3007, 29th AIAA Fluid Dynamics Conference, 1998.
