## Datasets Description

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

- Governing Equations: The simulations solve for quantities such as the velocity field $\mathbf{u}(\mathbf{x})$, pressure $p(\mathbf{x})$, and possibly additional variables like turbulence relating to motion energy $k$ or dissipation $\epsilon$.  
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

| Dataset ID | Vehicle Model | Variant Description             | Geometry Changes                              | Simulation Conditions                    |
|------------|---------------|---------------------------------|-----------------------------------------------|------------------------------------------|
| 1          | Vehicle A     | Baseline Model                  | None                                          | Standard atmospheric conditions          |
| 2          | Vehicle A     | Modified Front Bumper           | Front bumper altered                          | Standard atmospheric conditions          |
| 3          | Vehicle A     | Additional Rear Spoiler         | Rear spoiler added                            | Standard atmospheric conditions          |
| 4          | Vehicle A     | Altered Side Mirrors            | Side mirrors changed                          | Standard atmospheric conditions          |
| 5          | Vehicle A     | Changes in Underbody Design     | Underbody geometry altered                    | Standard atmospheric conditions          |
| 6          | Vehicle A     | Different Tire Profiles         | Tire profiles changed                         | Standard atmospheric conditions          |
| 7          | Vehicle A     | Roof Rack Added                 | Roof rack added                               | Standard atmospheric conditions          |
| ...        | ...           | ...                             | ...                                           | ...                                      |

This table can be extended to include additional columns for specific parameters such as Reynolds number, inlet velocity magnitude, yaw angle, or turbulence intensity if the study focuses on particular flow phenomena. The “Variant Description” column provides a concise reference to more detailed notes on geometry and flow specifications, making the dataset easier to find your way through and interpret.

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
- Uniform Spacing:  
The decimation algorithm strives to make sure that the remaining points are uniformly distributed over the geometry. This is important for preserving the overall shape and significant features. Methods such as edge collapse, clustering, or quadric error metrics (QEM) are often used to achieve this.

Mathematically, one might express the decimation as a minimization problem:

$$\min_{\text{decimated mesh}} \sum_{\text{original points}} \|\mathbf{x}_{\text{original}} - \mathbf{x}_{\text{decimated}}\|^2$$

subject to constraints that preserve the topology and key geometric features.

### Flow Field Interpolation

After geometry decimation, the flow field data must be interpolated onto the new, coarser mesh. This involves several considerations:

- Variable Mapping:  
Key flow variables such as pressure $p$, velocity components $\mathbf{u} = (u, v, w)$, and other quantities (e.g., turbulence relating to motion energy $k$) are mapped from the high-resolution CFD mesh onto the decimated mesh.

- Preservation of Necessary Flow Structures:  
Higher-order interpolation schemes may be used, particularly near regions with steep gradients, such as boundary layers and separation zones. Special techniques, like adaptive interpolation near important areas, help maintain the fidelity of the flow features.

- Tradeoff Considerations:  
A finer decimated mesh retains more of the original flow-field resolution but requires greater memory usage. Conversely, a too-coarse mesh might result in the loss of important aerodynamic details, degrading the performance of the neural network.

### Practical Considerations

When designing the decimation workflow, several practical aspects must be considered:

- Symmetry:  
Many aerodynamic bodies (e.g., vehicles or wings) exhibit symmetry about a central plane. Exploiting this symmetry—by, for instance, using a half-model—can significantly reduce the data volume without sacrificing information.

- Reference Frames:  
Consistent alignment of geometries is necessary. Standardizing the coordinate system (e.g., $x$-axis along the longitudinal direction, $y$-axis laterally, $z$-axis vertically) simplifies both the decimation process and subsequent neural network training.

- Balancing Samples and Resolution:  
A key tradeoff exists between the number of distinct geometries (i.e., dataset size) and the resolution per geometry. A rough guideline is given by:

$$\text{Total memory usage} \approx (\text{number of samples}) \times (\text{points per sample}) \times (\text{number of variables})$$

This balance must be carefully managed to make sure that the entire dataset can be effectively processed within the available hardware constraints.
