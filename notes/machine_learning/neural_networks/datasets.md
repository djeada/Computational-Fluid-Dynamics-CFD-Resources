## Datasets Description

The quality and diversity of training datasets directly determine how well a neural network can generalize to new aerodynamic configurations. Assembling such datasets requires systematic variation of geometric and flow parameters through a Design of Experiments framework, combined with consistent CFD methodology. The core challenge is to cover the design space broadly enough to train robust models while keeping dataset generation computationally affordable and ensuring that legacy and new data can be harmonized.

When deploying neural networks in aerodynamic applications, assembling high-quality datasets is important for both model training and validation. In these applications, datasets must capture a wide range of geometrical variations and flow conditions so that the trained model can generalize to new or modified configurations reliably. The overarching objective of these datasets is often to predict aerodynamic properties—such as the drag coefficient $C_d$, lift coefficient $C_l$, or even full flow fields—based on changes in vehicle or aerodynamic body geometry. Making sure that the dataset spans a sufficiently broad design space is important for strong performance and improved predictive accuracy.

A well-curated dataset not only helps in building more accurate models but also aids in uncovering underlying physical relationships between geometry and aerodynamic performance. The quality, diversity, and consistency of the data are key factors that influence the success of subsequent machine learning applications in CFD.

### Design of Experiments (DoE)

A typical dataset for aerodynamic neural networks arises from a systematic variation of key geometry features and flow parameters. This process—known as the Design of Experiments (DoE)—is structured to make sure that the dataset adequately covers the design space of interest. The goal is to create controlled variations that help the network learn the relationships between geometric modifications and aerodynamic responses.

DoE strategies in aerodynamic studies often include:

I. Geometry-Driven Changes

- Front Bumper Modifications: Altering the curvature, angle, or profile to study its effect on flow separation and pressure distribution.
- Side Mirror Relocations or Shape Changes: Changing the position or contour of side mirrors to analyze their impact on drag and potential interference effects with adjacent flow structures.
- Tire Profile Alterations: Modifying tire shapes to assess how underbody flows and ground effects influence overall vehicle aerodynamics.
- Rear Spoiler Installations: Adding or modifying spoilers to study their role in generating downforce or reducing lift.
- Roof Racks and External Accessories: Evaluating how additional components disturb the airflow, impacting both drag and lift characteristics.

II. Flow-Driven Changes

- Variation in Reynolds Number: Adjusting the Reynolds number to simulate different flow regimes, from laminar to turbulent, thereby capturing the effects of scale and velocity variations.
- Variation in Inlet Velocity Profiles: Testing different inlet conditions to mimic real-world scenarios such as gusts or variable wind conditions.
- Different Turbulence Intensities or Swirl Ratios: Altering turbulence parameters to examine their impact on flow separation, mixing, and wake formation.
  By combining these geometric and flow-driven perturbations, the resultant dataset spans a wide spectrum of aerodynamic configurations. This diversity is necessary for training strong models that are capable of predicting flow behavior across a range of design modifications and operating conditions.

### Typical CFD Foundations

Each dataset entry generally originates from high-fidelity simulations based on methods such as Reynolds-Averaged Navier–Stokes (RANS) or, for more complicated phenomena, Large Eddy Simulation (LES). In practice, these CFD simulations are performed on either in-house or cloud-based high-performance computing (HPC) clusters.

Key elements of CFD foundations include:

- Governing Equations: The simulations solve for quantities such as the velocity field $\mathbf{u}(\mathbf{x})$, pressure $p(\mathbf{x})$, and possibly additional variables like turbulent kinetic energy $k$ or dissipation $\epsilon$.
- Mesh Discretization: The flow domain around the geometry is discretized using a computational mesh, which can vary in resolution depending on the simulation objectives and available resources.
- Boundary Conditions: Standard atmospheric or wind-tunnel conditions are typically applied, making sure that the simulations reflect realistic operational environments.
- Data Partitioning: After generating a target number of simulation cases (e.g., several hundred or thousand), the data is usually split into training, testing, and sometimes validation sets. A common split might allocate 90% of the samples for training and 10% for testing, making sure that the model’s performance is evaluated on unseen cases.
  This rigorous CFD foundation makes sure that the resulting dataset is both reliable and rich in physical detail, providing a solid basis for subsequent machine learning model development.

### Legacy vs. Newly Generated Data

In practice, researchers and engineers often merge legacy data—collected from previous design studies—with newly generated CFD cases to broaden the coverage of both geometry and flow parameter spaces. While legacy data can expedite dataset creation and offer historical insights, it may also introduce inconsistencies due to differences in grid resolutions, turbulence models, or boundary conditions used in earlier studies.

Key challenges in merging legacy with new data include:

- Data Consistency: Making sure that all data points adhere to a consistent set of standards requires careful preprocessing, normalization, and, if necessary, recalibration of legacy cases.
- Quality Control: Verification steps are necessary to confirm that older data meets the current simulation fidelity and can be integrated meaningfully with new cases.
- Coverage Balance: Combining legacy and new data can help achieve a more comprehensive exploration of the design space, but it is necessary to maintain a balance so that the model does not become biased toward the characteristics of one subset.
  Proper data preprocessing—including normalization, grid refinement adjustments, and consistent boundary condition application—is important to harmonize the dataset and enhance the robustness of the training process.

## Dataset Overview

An effective dataset for aerodynamic neural networks is often organized in a tabular format that documents key information about each simulation case. Each row corresponds to a set of simulations performed on a particular baseline model, with columns detailing the geometry changes and operating conditions.

Below is an illustrative example of how such datasets might be structured:

| Dataset ID | Vehicle Model | Variant Description | Geometry Changes | Simulation Conditions |
| --- | --- | --- | --- | --- |
| 1 | Vehicle A | Baseline Model | None | Standard atmospheric conditions |
| 2 | Vehicle A | Modified Front Bumper | Front bumper altered | Standard atmospheric conditions |
| 3 | Vehicle A | Additional Rear Spoiler | Rear spoiler added | Standard atmospheric conditions |
| 4 | Vehicle A | Altered Side Mirrors | Side mirrors changed | Standard atmospheric conditions |
| 5 | Vehicle A | Changes in Underbody Design | Underbody geometry altered | Standard atmospheric conditions |
| 6 | Vehicle A | Different Tire Profiles | Tire profiles changed | Standard atmospheric conditions |
| 7 | Vehicle A | Roof Rack Added | Roof rack added | Standard atmospheric conditions |
| 8 | Vehicle A | Crosswind Study | None | Yaw angle 5°, 10°, 15° |
| 9 | Vehicle A | High-Speed Regime | None | Inlet velocity 40 m/s ($Re \approx 8 \times 10^6$) |
| 10 | Vehicle A | Elevated Turbulence | None | Turbulence intensity 5%, length scale 0.1 m |
| 11 | Vehicle B | Baseline (SUV) | None | Standard atmospheric conditions |
| 12 | Vehicle B | Lowered Ride Height | Ground clearance reduced 30 mm | Standard atmospheric conditions |
| ... | ... | ... | ... | ... |

This table can be extended to include additional columns for specific parameters such as Reynolds number, inlet velocity magnitude, yaw angle, or turbulence intensity if the study focuses on particular flow phenomena. Including multiple vehicle models (Vehicle A, Vehicle B, etc.) and both geometry-driven and flow-driven variations ensures the dataset captures a broad range of aerodynamic behaviors. The “Variant Description” column provides a concise reference to more detailed notes on geometry and flow specifications, making the dataset easier to find your way through and interpret.

## Decimation Workflow

Once high-resolution CFD data has been collected, it is common to reduce (or “decimate”) both the geometry and flow field representations to meet the memory and computational constraints of neural network training. The decimation process is a important preprocessing step that seeks to balance fidelity with efficiency.

The decimation workflow addresses several key objectives:

I. Maintain Important Features

- It is necessary to preserve key aerodynamic features such as leading edges, separation points, and regions of high curvature, as these areas often have a disproportionate impact on aerodynamic performance.

II. Reduce Data Density

- High-resolution meshes that contain millions of cells must be coarsened to a manageable level suitable for GPU-based neural network training. The goal is to reduce the data volume while retaining enough detail to capture the necessary flow physics.

### Geometry Decimation

Mesh Reduction:

- The original surface mesh, which may contain a very high number $N$ of points, is reduced to a fraction of these points, denoted by $\alpha N$ (commonly $\alpha \approx 0.1$ or another fraction).
- Uniform Spacing:\
  The decimation algorithm strives to make sure that the remaining points are uniformly distributed over the geometry. This is important for preserving the overall shape and significant features. Methods such as edge collapse, clustering, or quadric error metrics (QEM) are often used to achieve this.

Mathematically, one might express the decimation as a minimization problem:

$$
\min_{\text{decimated mesh}} \sum_{\text{original points}}
\|\mathbf{x}_{\text{original}} - \mathbf{x}_{\text{decimated}}\|^2
$$

subject to constraints that preserve the topology and key geometric features.

### Flow Field Interpolation

After geometry decimation, the flow field data must be interpolated onto the new, coarser mesh. This involves several considerations:

- Variable Mapping:\
  Key flow variables such as pressure $p$, velocity components $\mathbf{u} = (u, v, w)$, and other quantities (e.g., turbulent kinetic energy $k$) are mapped from the high-resolution CFD mesh onto the decimated mesh.

- Preservation of Necessary Flow Structures:\
  Higher-order interpolation schemes may be used, particularly near regions with steep gradients, such as boundary layers and separation zones. Special techniques, like adaptive interpolation near important areas, help maintain the fidelity of the flow features.

- Tradeoff Considerations:\
  A finer decimated mesh retains more of the original flow-field resolution but requires greater memory usage. Conversely, a too-coarse mesh might result in the loss of important aerodynamic details, degrading the performance of the neural network.

### Practical Considerations

When designing the decimation workflow, several practical aspects must be considered:

- Symmetry:\
  Many aerodynamic bodies (e.g., vehicles or wings) exhibit symmetry about a central plane. Exploiting this symmetry—by, for instance, using a half-model—can significantly reduce the data volume without sacrificing information.

- Reference Frames:\
  Consistent alignment of geometries is necessary. Standardizing the coordinate system (e.g., $x$-axis along the longitudinal direction, $y$-axis laterally, $z$-axis vertically) simplifies both the decimation process and subsequent neural network training.

- Balancing Samples and Resolution:\
  A key tradeoff exists between the number of distinct geometries (i.e., dataset size) and the resolution per geometry. A rough guideline is given by:

$$
\text{Total memory usage} \approx (\text{number of samples}) \times
(\text{points per sample}) \times (\text{number of variables})
$$

This balance must be carefully managed to make sure that the entire dataset can be effectively processed within the available hardware constraints.

### Setting Up the Problem

1. **Define the geometry family** – Identify the baseline shape (e.g., a specific vehicle body or airfoil class) and list every geometric parameter that can be meaningfully varied (bumper curvature, spoiler angle, mirror position, etc.).
2. **Select flow parameters** – Choose the operating conditions to sweep, such as Reynolds number range, yaw angles, and turbulence intensity levels, based on the target application envelope.
3. **Design the DoE matrix** – Use a space-filling strategy (Latin Hypercube Sampling or Sobol sequences) to distribute sample points across the combined geometry–flow parameter space while keeping the total case count within your computational budget.
4. **Standardize CFD setup** – Fix the solver, turbulence model, mesh topology rules, convergence criteria, and boundary conditions across all cases so that differences in results reflect only geometry and flow changes, not methodology drift.
5. **Harmonize legacy data** – When incorporating older simulations, verify grid independence, re-normalize quantities to common reference values, and flag cases that used different turbulence closures or boundary treatments for potential recalibration.
6. **Run the decimation pipeline** – Reduce each surface mesh to the target point count $\alpha N$ using a consistent algorithm (e.g., QEM-based edge collapse), then interpolate flow variables onto the coarsened mesh while preserving gradients near critical features.
7. **Partition the dataset** – Split the final collection into training, validation, and test sets (e.g., 80/10/10). Stratify the split so that each subset spans the full range of geometric and flow parameters rather than clustering around a narrow region of the design space.

### Key Takeaways

- A well-designed DoE ensures broad, unbiased coverage of the geometry–flow parameter space and prevents the neural network from overfitting to a narrow subset of configurations.
- Consistent CFD methodology (solver settings, mesh standards, boundary conditions) across all cases is essential for producing a coherent dataset free of systematic bias.
- Legacy data can accelerate dataset creation but must be carefully audited and re-normalized to match the quality and conventions of newly generated simulations.
- Geometry decimation and flow-field interpolation should preserve critical aerodynamic features (separation lines, high-curvature edges) while reducing data to a size compatible with GPU memory constraints.
- Exploiting geometric symmetry (e.g., half-models) effectively doubles the usable data density for a given memory budget.
- Stratified partitioning of training, validation, and test sets guarantees that model performance metrics reflect true generalization across the entire design space.

### Exercises

**Exercise 1.** Use the memory guideline from the note to estimate the size of a dataset of 600 samples, each with 200,000 decimated points and 7 variables ($x, y, z, p, u, v, w$) stored as 32-bit floats. What is the size of the training portion under an 80/10/10 split, and what if a half-model with symmetry halves the point count?

<details>
<summary>Answer</summary>

$600 \times 200{,}000 \times 7 \times 4 = 3.36 \times 10^9$ bytes, or about 3.36 GB.

The training portion (80%) is about 2.69 GB.

With a half-model (100,000 points) everything halves: 1.68 GB in total.

</details>

**Exercise 2.** Row 9 of the dataset table lists an inlet velocity of 40 m/s with $Re \approx 8 \times 10^6$. Taking $\nu = 1.5 \times 10^{-5}$ m²/s, what reference length does this imply? What would $Re$ be based on a 4.5 m vehicle length, and why does this matter when datasets are merged?

<details>
<summary>Answer</summary>

$L = Re\,\nu/U = 8 \times 10^6 \times 1.5 \times 10^{-5} / 40 = 3.0$ m.

With $L = 4.5$ m, $Re = 40 \times 4.5 / 1.5 \times 10^{-5} = 1.2 \times 10^7$.

The same physical case can carry Reynolds numbers that differ by 50% depending on the reference length. If one study used wheelbase and another used overall length, the Reynolds-number feature would be inconsistent. Always store the reference length (and area) with every case.

</details>

**Exercise 3.** A legacy study reports $C_d = 0.320$ for a vehicle using a reference area of 2.10 m². The new campaign uses 2.25 m² for the same vehicle. Convert the legacy value to the new convention, and explain the risk of skipping this step.

<details>
<summary>Answer</summary>

The drag force is the same, so $C_d A$ is conserved: $C_{d,\text{new}} = 0.320 \times 2.10/2.25 \approx 0.299$.

Left uncorrected, the legacy cases would carry a spurious offset of about 0.02 in $C_d$. That is larger than many of the geometry effects the network is meant to learn, and it would be learned as a bias tied to whatever features distinguish the legacy cases.

</details>

**Exercise 4.** A surface mesh with $N = 2.5 \times 10^6$ points is decimated with $\alpha = 0.1$. How many points remain, and by what factor does the average point spacing grow if the points stay uniformly distributed over the surface? What does this mean for small features?

<details>
<summary>Answer</summary>

$\alpha N = 250{,}000$ points remain.

On a surface the number of points scales with $1/h^2$, so the spacing grows by $1/\sqrt{\alpha} = 1/\sqrt{0.1} \approx 3.16$.

Features smaller than about three original spacings (thin trailing edges, mirror gaps, grille bars) may disappear. This is why the note recommends preserving leading edges and high-curvature regions, with adaptive rather than uniform decimation near them.

</details>

**Exercise 5.** The crosswind study (row 8) has yaw angles $5^\circ$, $10^\circ$ and $15^\circ$ for the same geometry. A 90/10 random split of all simulations puts the $10^\circ$ case in the test set and the other two in training. Is the resulting test error a fair measure of generalization? Propose a better test design.

<details>
<summary>Answer</summary>

No. The model sees the same geometry at $5^\circ$ and $15^\circ$, so predicting $10^\circ$ is interpolation in a single variable for a known shape. The test error will be optimistic.

A better design uses two held-out sets. An interpolation set holds out complete geometric variants (all yaw angles of a variant together). An extrapolation set holds out a whole vehicle (for example, all Vehicle B cases). Stratify so that both sets span the range of the flow parameters, and report the errors on each separately.

</details>

### References

- McKay, M. D., Beckman, R. J., & Conover, W. J., "A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code", *Technometrics* 21(2), 1979.
- Garland, M., & Heckbert, P. S., "Surface Simplification Using Quadric Error Metrics", Proceedings of SIGGRAPH, 1997.
- Hucho, W.-H. (Ed.), *Aerodynamics of Road Vehicles*, 4th ed., SAE International, 1998.
- Hastie, T., Tibshirani, R., & Friedman, J., *The Elements of Statistical Learning*, 2nd ed., Springer, 2009.
