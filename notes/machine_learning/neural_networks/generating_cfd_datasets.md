## Methodology for Generating Robust CFD Datasets

ML models for aerodynamics are only as reliable as the data they are trained on. Generating a robust CFD dataset requires careful decisions about solver configuration, turbulence modeling, mesh resolution, and boundary conditions to ensure that the resulting flow fields accurately represent physical reality. The challenge is to produce a large, consistent, and high-fidelity collection of simulation results that spans the relevant design and operating space while remaining computationally tractable.

Establishing a high-fidelity computational fluid dynamics (CFD) dataset is a multi-step process that requires thoughtful decisions about software, turbulence models, mesh strategies, and numerical settings. The goal is to simulate vehicle aerodynamics (or similarly complex flows) at a level of accuracy that renders the resulting data suitable for both engineering decisions and advanced machine-learning (ML) applications. Below is a detailed overview of common approaches, key considerations, and best practices to generate robust CFD datasets in the automotive (or similar) context.

### 1. CFD Solver Selection and Setup

I. **Software Tools**\
Popular commercial codes (e.g., Star-CCM+, ANSYS Fluent) and open-source alternatives (e.g., OpenFOAM) are widely used in the automotive industry. Their suitability depends on:

- Support for steady (RANS), unsteady (URANS), or scale-resolving approaches (LES, DES).
- Ability to scale on high-performance computing (HPC) clusters, sometimes up to hundreds or thousands of cores.
- Availability of integrated meshing tools (e.g., polyhedral, trimmer) and boundary-layer refinement utilities.
- In-house familiarity with the software, existing workflows, and licensing constraints.

II. **Governing Equations**

Most automotive simulations solve the 3D, steady or unsteady Reynolds-Averaged Navier–Stokes (RANS) equations, possibly supplemented by turbulence transport equations. For instance, the k–$\omega$ SST model adds the following two PDEs:

$$
\frac{\partial ( \rho k )}{\partial t} + \nabla \cdot (\rho k \mathbf{u}) = P_k -
\beta^* \rho k \omega + \nabla \cdot \bigl((\mu + \sigma_k \mu_t)\nabla k \bigr)
$$

$$
\frac{\partial ( \rho \omega )}{\partial t} + \nabla \cdot
(\rho \omega \mathbf{u}) = \frac{\gamma}{\nu_t} P_k - \beta \rho \omega^2 + \nabla \cdot
\bigl((\mu + \sigma_\omega \mu_t)\nabla \omega \bigr) + 2(1 - F_1)
\frac{\rho \sigma_{\omega 2}}{\omega} \nabla k \cdot \nabla \omega
$$

where $P_k$ is the turbulence production term, $\mu_t$ is the turbulent eddy viscosity, $\omega$ is the specific dissipation rate, and $F_1$ is the blending function that switches the model coefficients from $k$–$\omega$ values near the wall to $k$–$\epsilon$-derived values in the free stream (the last term is the cross-diffusion term that this blending introduces). Choosing the turbulence model (e.g., Spalart–Allmaras, k–$\epsilon$ variants, etc.) depends on whether the objective is capturing mean forces or more complex flow structures.

III. **Boundary Conditions and Domain Setup**

- **Inlet**: Specified velocity or mass flow rate, sometimes with turbulence intensity and length scale.
- **Outlet**: Pressure-outlet or outflow condition to allow fluid to exit the domain without reflection.
- **Wall**: No-slip condition on the vehicle surface, often with near-wall modeling to resolve boundary layers accurately.
- **Symmetry**: Many automotive problems leverage a symmetry plane to halve the computational domain (especially if the vehicle geometry is symmetric).
  IV. **Temporal Discretization**
- **Steady-State Simulations**: Commonly used for design optimization focusing on time-averaged drag, lift, and overall flow patterns.
- **Unsteady/Transient Simulations**: Required for cases involving transient wake dynamics, bluff-body flows, or vortex shedding around spoilers or side mirrors. Time step selection depends on the characteristic flow frequencies (e.g., shedding Strouhal numbers).

### 2. Turbulence Modeling Considerations

I. **RANS Models**

- **k–ω SST (Shear Stress Transport)**: Balances near-wall resolution (from the k–$\omega$ formulation) with free-stream stability (from the k–$\epsilon$ adaptation). Widely used in automotive design for body- and underbody-flow predictions.
- **Spalart–Allmaras**: Simplified single-equation model often used for external aerodynamics due to its good compromise between accuracy and computational cost.
  II. **Scale-Resolving Simulations**
- **Large Eddy Simulation (LES)**: Partially resolves the large turbulent eddies in 3D, requiring a very fine mesh in critical regions (e.g., around wheels, in separated wakes). This can drastically increase computational requirements, sometimes by one or two orders of magnitude compared to RANS.
- **Detached Eddy Simulation (DES) / Delayed DES (DDES)**: Combines RANS in near-wall or attached-flow regions with LES-like modeling in separated or wake regions. This is a cost-effective path to capturing unsteady flow features more accurately than pure RANS but with lower HPC overhead than full LES.

Choosing the right turbulence modeling approach depends on the problem’s needs: capturing approximate time-averaged forces may suffice for many design studies, while advanced modeling is necessary for detailed wake analyses or acoustic predictions.

### 3. Meshing Strategy and Grid Details

Meshing remains one of the most critical aspects of generating reliable CFD datasets. In automotive aerodynamics, the geometry typically involves wheels, underbodies, mirrors, spoilers, and complex external surfaces. A carefully planned mesh ensures numerical stability, accurate boundary-layer resolution, and manageable compute times.

I. **Low $y^+$ and High $y^+$ Zones**

- For accurate boundary-layer resolution, especially around the vehicle surface, the first cell height must be chosen to achieve $y^+ \approx 1$. That is,

  $$
  y^+ = \frac{ \rho \, u_\tau \, \Delta y }{ \mu } \approx 1
  $$

  where $u_\tau$ is the friction velocity ($u_\tau = \sqrt{\tau_w/\rho}$), $\Delta y$ is the distance from the wall to the first cell center, and $\tau_w$ is the wall-shear stress. This criterion ensures the boundary-layer profile is adequately captured within the CFD solver’s near-wall model or the fully resolved viscous sublayer in case of LES.

- In regions far away from critical surfaces (e.g., domain far-field), the boundary layer is not of primary concern. A coarser “wall function” approach can be adopted here, reducing cell count and solver time. Typical $y^+$ targets might be 30–200, depending on the chosen wall-function implementation.
  II. **Mesh Topologies**

- **Hexahedral Meshes**: Offer highly structured cells and can yield accurate solutions with fewer elements in regions of simple geometry. However, they are harder to generate around extremely complex surfaces.

- **Polyhedral Meshes**: Provide more flexibility in conforming to intricate vehicle geometries (e.g., wheel arches, engine bays). By having more faces per cell, polyhedral elements can improve convergence and reduce cell count compared to strictly tetrahedral meshes.

- **Trimmer Meshes**: Start from a structured background grid that is “trimmed” around curved surfaces. This approach can yield predominantly orthogonal cells in free-stream regions while still adapting to the vehicle boundary.

III. **Targeted Refinement**

Crucial flow regions—such as the front fascia, side mirrors, underbody diffuser, and wake zone behind the vehicle—may receive extra refinement layers or localized volumetric refinement. For wheels, rotating reference frames or overset meshes might be used to accurately capture wheel rotation effects.

IV. **Mesh Size**\
For a typical full-car automotive simulation:

- 10–50 million cells is common for a production-level simulation.

- 50–200+ million cells may be necessary for capturing detailed unsteady phenomena.

  Balancing mesh resolution against computational resources is critical. Larger meshes may require HPC clusters running for days; smaller meshes might compromise fidelity in critical flow regions.

### 4. Example Meshing Workflow

A simplified workflow can be depicted as follows:

```
             Vehicle CAD Model
             +-------------+
             |             |
             |   Import    |
             +------+------+
                    |
                    v
   Global Meshing Strategy (Hex/Poly/Trimmer)
   +-----------------------------------------+
   |  Generate baseline grid across entire   |
   |  domain (e.g., external wind tunnel)    |
   +-------------------------+---------------+
                                 |
                                 v
   Local Refinement (Critical Surfaces/Flow Regions)
   +-------------------------+---------------+
   |  - Low y+ boundary layer  refinement    |
   |  - Finer cells in wake and wheel zones  |
   |  - Possibly rotating references for     |
   |    wheels                               |
   +-------------------------+
                    |
                    v
           Final Mesh for CFD Analysis
         (Quality Checks & Simulation)
```

I. **Baseline Meshing**: Establish the domain boundaries (wind tunnel or open road environment). Generate an initial grid using a chosen topology (hex, poly, or trimmer).

II. **Local Refinement**: Insert additional boundary-layer cells around the vehicle surface to achieve a target $y^+$. Regionally refine areas prone to separation or vortex shedding (e.g., side mirrors, spoiler edges).

III. **Quality Checks**: Evaluate skewness, aspect ratio, and cell-to-cell transitions. Overly skewed elements or large jumps in cell size can cause solver instability or inaccuracy.

### 5. Numerical Parameters and Solver Convergence

I. **Spatial Discretization**

Select appropriate numerical schemes (e.g., second-order upwind, QUICK, or central differencing for LES). Higher-order schemes can improve accuracy but require more computational effort and are more sensitive to mesh quality.

II. **Temporal Discretization (Unsteady Cases)**

- Time step selection should respect the Courant–Friedrichs–Lewy (CFL) condition,

  $$
  \text{CFL} = \frac{u \, \Delta t}{\Delta x} \lesssim 1
  $$

  where $u$ is the local flow velocity, $\Delta x$ is the cell size, and $\Delta t$ is the time step.

- Ensure enough temporal resolution to capture relevant flow instabilities or periodic phenomena (e.g., vortex shedding, unsteady wake fluctuations).
  III. **Convergence Monitoring**

- **Residual Monitoring**: Track momentum, continuity, and turbulence equation residuals; they should drop by at least three to four orders of magnitude in steady RANS.

- **Force Monitoring**: Drag ($C_d$) and lift ($C_l$) can be monitored in real-time to confirm they settle to stable values.

- **Physical Quantity Checks**: Evaluate boundary-layer profiles, velocity magnitudes in the wake, or pressure distributions on the car surface against known benchmarks or validation data (e.g., wind-tunnel measurements).

### 6. Data Extraction for ML and Post-Processing

Once simulations converge or pass appropriate unsteady run times:

I. **Flow Field Export**

- Store 3D fields of velocity $\mathbf{u}(\mathbf{x})$, pressure $p(\mathbf{x})$, turbulence quantities (e.g., $k$, $\omega$, or Reynolds stresses), and, if needed, temperature or species transport.
- Some workflows also export surface scalar fields (e.g., pressure coefficient $C_p$) and integrated forces.
  II. **Decimation and Formatting**
- For machine learning, large meshes (millions of cells) are typically coarsened to a few hundred thousand nodes or fewer, preserving essential flow features while reducing memory demands.
- Data can be stored in specialized formats (e.g., .vtk, .h5, or graph-based data structures) that facilitate direct import into deep-learning frameworks.

III. **Validation Against Physical Experiments**\
If wind-tunnel or on-road measurement data is available:

- Compare integrated coefficients (drag, lift, pitching moment, etc.) to measured values.
- Compare local pressure or velocity measurements at discrete sensor locations.
- Document discrepancies to inform improvements in meshing, modeling (e.g., better turbulence closure), or solver settings.

### Setting Up the Problem

When preparing a CFD-based dataset pipeline, begin by selecting a solver and turbulence model that match your application. For external aerodynamics a RANS approach (e.g., k–$\omega$ SST) in OpenFOAM or a commercial code is a common starting point. Define boundary conditions—inlet velocity or mass-flow rate, outlet pressure, no-slip walls, and symmetry planes—that faithfully represent the target operating environment.

Plan your mesh resolution around the regions that govern the quantities of interest: refine near walls to achieve $y^+ \approx 1$ where boundary-layer accuracy matters, and use coarser cells in the far field. Performing a brief grid-independence study on a representative case helps establish a mesh density that balances accuracy against cost.

To build a large dataset, automate simulation runs using HPC job schedulers (e.g., SLURM, PBS) combined with scripting (Python or Bash) that parameterizes geometry or operating conditions. After each run, extract the relevant fields—surface pressures, velocity volumes, integrated force coefficients—and convert them to ML-friendly formats such as HDF5, VTK, or NumPy arrays. Where experimental data are available, validate a subset of simulations against wind-tunnel or flight-test measurements to quantify the fidelity of the dataset.

### Key Takeaways

- **Solver and model choice**: match the CFD solver and turbulence model to the physics you need to capture; RANS is cost-effective for time-averaged quantities, while LES or DES may be needed for unsteady phenomena.
- **Mesh quality drives data quality**: invest in boundary-layer refinement and grid-independence checks before scaling up to hundreds of cases.
- **Automate early**: scripted workflows and job schedulers are essential for producing the large, consistent datasets that ML models require.
- **Standardize data formats**: export to well-defined formats (HDF5, VTK) with consistent field naming to simplify downstream ingestion by training pipelines.
- **Validate against experiments**: even partial validation builds confidence in the dataset and helps identify systematic simulation biases.
- **Document everything**: record solver settings, mesh parameters, and convergence criteria so that results are reproducible and any data-quality issues can be traced back to their source.

### Related Scripts

- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.

### Exercises

**Exercise 1.** The inlet of a k–$\omega$ SST case has $U = 40$ m/s, turbulence intensity $I = 1\%$ and turbulence length scale $\ell = 0.01$ m. Using $k = \tfrac{3}{2}(IU)^2$ and $\omega = k^{1/2}/(C_\mu^{1/4}\ell)$ with $C_\mu = 0.09$, compute $k$, $\omega$, the eddy viscosity $\nu_t = k/\omega$, and the ratio $\nu_t/\nu$ for air ($\nu = 1.5 \times 10^{-5}$ m²/s).

<details>
<summary>Answer</summary>

$k = 1.5 \times (0.4)^2 = 0.24$ m²/s².

$\omega = \sqrt{0.24}/(0.09^{1/4} \times 0.01) = 0.490/0.005477 \approx 89.4$ s$^{-1}$.

$\nu_t = 0.24/89.4 \approx 2.68 \times 10^{-3}$ m²/s, so $\nu_t/\nu \approx 179$.

An eddy-viscosity ratio of order 100 at the inlet is high. The value reaching the vehicle depends on how $k$ and $\omega$ decay across the upstream domain, so inlet settings must be kept identical across every case in a dataset.

</details>

**Exercise 2.** Air flows at $U = 30$ m/s ($\rho = 1.2$ kg/m³, $\nu = 1.5 \times 10^{-5}$ m²/s) over the roof, $x = 2$ m from the leading edge. Use the turbulent flat-plate estimate $C_f = 0.0576\,\mathrm{Re}_x^{-1/5}$ to find $\tau_w$, $u_\tau$, and the wall distance $\Delta y$ for $y^+ = 1$ and for $y^+ = 50$.

<details>
<summary>Answer</summary>

$\mathrm{Re}_x = 30 \times 2 / 1.5 \times 10^{-5} = 4 \times 10^6$, so $C_f = 0.0576 \times (4 \times 10^6)^{-0.2} \approx 2.75 \times 10^{-3}$.

$\tau_w = \tfrac{1}{2}\rho U^2 C_f \approx 1.49$ Pa and $u_\tau = \sqrt{\tau_w/\rho} \approx 1.11$ m/s.

$y^+ = 1$: $\Delta y = \nu/u_\tau \approx 1.35 \times 10^{-5}$ m (13.5 µm).

$y^+ = 50$: $\Delta y \approx 0.67$ mm.

Because the note defines $\Delta y$ as the distance to the first cell centre, the first cell height is about twice these values.

</details>

**Exercise 3.** A side mirror with $D = 0.15$ m sheds vortices at a Strouhal number $St = fD/U = 0.2$ in a $U = 40$ m/s flow. Find the shedding frequency and period. With 50 time steps per period, what is $\Delta t$, and what CFL number does that give in 2 mm cells at 40 m/s? What $\Delta t$ gives CFL = 1, and how many steps per period is that?

<details>
<summary>Answer</summary>

$f = 0.2 \times 40/0.15 \approx 53.3$ Hz and $T = 1/f = 18.75$ ms.

With 50 steps per period, $\Delta t = 3.75 \times 10^{-4}$ s and $\text{CFL} = 40 \times 3.75 \times 10^{-4}/0.002 = 7.5$.

For CFL = 1, $\Delta t = 0.002/40 = 5 \times 10^{-5}$ s, which is 375 steps per period.

The frequency requirement alone would allow a much larger step. In the refined mirror region the CFL limit is the binding constraint for LES and DES accuracy, so it sets the cost.

</details>

**Exercise 4.** A campaign of 300 cases uses 40 million cells each, with 5 stored fields in double precision. Compute the raw storage per case and in total. After decimation to 300,000 nodes with 7 float32 values per node (coordinates plus four fields), what are the storage per case, the total, and the reduction factor?

<details>
<summary>Answer</summary>

Raw: $40 \times 10^6 \times 5 \times 8 = 1.6$ GB per case, or 480 GB in total.

Decimated: $300{,}000 \times 7 \times 4 = 8.4$ MB per case, or about 2.5 GB in total.

The reduction factor is $1.6 \times 10^9 / 8.4 \times 10^6 \approx 190$. The decimated set fits in GPU or host memory, but it no longer contains the boundary-layer detail. Keep the raw data archived so it can be re-extracted differently.

</details>

**Exercise 5.** A grid-independence study with a constant refinement ratio $r = 2$ gives $C_d = 0.3350$ (coarse), $0.3210$ (medium) and $0.3170$ (fine). Compute the observed order of accuracy $p$, the Richardson-extrapolated $C_d$, and the fine-grid GCI with safety factor 1.25.

<details>
<summary>Answer</summary>

$$
p = \frac{\ln\left(\frac{0.3350 - 0.3210}{0.3210 - 0.3170}\right)}{\ln 2} = \frac{\ln 3.5}{\ln 2} \approx 1.81
$$

Since $r^p - 1 = 2.5$, the extrapolated value is $C_{d,\text{ext}} = 0.3170 + (0.3170 - 0.3210)/2.5 = 0.3154$.

The relative fine–medium difference is $|0.3170 - 0.3210|/0.3170 \approx 0.0126$, so $\text{GCI}_{\text{fine}} = 1.25 \times 0.0126/2.5 \approx 0.63\%$.

An observed order close to the formal second order and a GCI below 1% suggest the fine mesh is adequate for the dataset.

</details>

### References

- Menter, F. R., "Two-equation eddy-viscosity turbulence models for engineering applications", *AIAA Journal* 32(8), 1994.
- Spalart, P. R., & Allmaras, S. R., "A one-equation turbulence model for aerodynamic flows", AIAA Paper 92-0439, 1992.
- Wilcox, D. C., *Turbulence Modeling for CFD*, 3rd ed., DCW Industries, 2006.
- Celik, I. B., Ghia, U., Roache, P. J., Freitas, C. J., Coleman, H., & Raad, P. E., "Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications", *Journal of Fluids Engineering* 130(7), 2008.
- Schlichting, H., & Gersten, K., *Boundary-Layer Theory*, 9th ed., Springer, 2017.
