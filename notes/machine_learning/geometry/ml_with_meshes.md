# Machine Learning on Meshes

These notes summarize and comment on the article 'Machine Learning-Based Optimal Mesh Generation in Computational Fluid Dynamics,' published on February 25, 2021, by Keefe Huang, Moritz Krügener, Alistair Brown, Friedrich Menhorn, Hans-Joachim Bungartz, and Dirk Hartmann. https://arxiv.org/abs/2102.12923

# 1 Introduction

- **Computer Aided Engineering (CAE) Tools**:
  - Integral in industrial product development.
  - Computational Fluid Dynamics (CFD) is a rapidly growing domain within CAE.
  - Focus: Simulation and prediction of fluid and air flows and their effects.

- **Challenges in CFD**:
  - High computational resource demand.
  - Accuracy depends heavily on mesh quality (e.g., fine mesh in boundary layer separation regions).
  - Optimal mesh generation is complex and situation-specific.
  - Requires extensive experience to generate efficient computational meshes.

- **Strategies for Optimal Mesh Generation**:
  - Various strategies proposed; goal-oriented error estimators are most successful.
  - Goal-oriented error estimators refine mesh in regions contributing to the largest errors.
  - Iterative process finds Pareto optimal meshes (accuracy vs. degrees of freedom).
  - Highly computationally demanding; limited tool availability.

- **Machine Learning in Flow Simulations**:
  - Recent proposals use machine learning to accelerate flow simulations.
  - Approaches:
    - Predict results using neural networks based on previous simulations.
    - Combine traditional and ML approaches to speed up simulations.
  - Limitations:
    - Optimal computational mesh identification remains unresolved.
    - Validation challenges in industrial contexts.

- **Proposed Approach**:
  - Focus: Accelerate optimal grid generation using machine learning.
  - Strategy:
    - Use a commercial solver (Simcenter STAR-CCM+) to determine optimal meshes for various situations.
    - Train a convolutional neural network on these optimal meshes.
    - Predict optimal mesh densities for input into any CFD meshing/simulation tool.

- **Application Focus**:
  - Task: Identify optimal mesh for 2D channel/wind-tunnel-like flows with arbitrary geometries.
  - Potential for generalization to other scenarios.

- **Advantages of ML-Based Mesh Refinement**:
  - High likelihood of industrial adoption.
  - Less sensitive to validation and verification issues compared to previous ML approaches.
  - Non-optimal meshes may affect convergence but not the correctness of predictions.
  - Limited set of industrial tools provide mesh optimization solutions.
  - Computationally inexpensive and provides a good starting point for further refinement.

# 2 State of the Art

- Current CFD methodologies produce highly accurate results but at a significant computational cost.
- Simulation times can span days or even weeks, especially for large and complex geometries.
- Consequently, design optimization studies often become prohibitively costly and slow, limiting their feasibility.

- **Reducing Simulation Time**:
  - Accepting higher errors or coarser resolutions can reduce simulation time.
  - However, this compromise can lead to non-physical behavior in the simulation.

- **Objective**:
  - The goal of adaptive mesh refinement and its machine learning counterpart is to speed up the process without sacrificing accuracy and resolution.

- **Next Steps**:
  - The following sections will review literature on adaptive mesh refinement.
  - Additionally, approaches for integrating machine learning into CFD will be explored.

## 2.1 Adaptive Grid Refinement

- **Importance of Adaptive Mesh Refinement**:
  - Critical since early days of continuum mechanics simulations.
  - Simulation computation time scales at least linearly with mesh size, often quadratically.
  - Local phenomena heavily influence physical quantities of interest.
  - Effective non-homogeneous adaptive grids with appropriate local refinement are key for economic simulations.
  - Optimal mesh choice often relies on simulation expert experience.

- **Classical Error Estimation Methods**:
  - Use global error estimates (e.g., energy norms) based on variational formulations.
  - Global bounds often don't relate directly to specific physical quantities of interest (e.g., drag).
  - Difficulty in determining where and how to refine the mesh.

- **Dual Weighted Residual (DWR) Error Estimators**:
  - Estimate local residuals and their effect on physical quantities of interest.
  - Solve an adjoint problem to identify sensitivities of quantities of interest to local errors.
  - Allow estimation and localization of errors.
  - Functional of interest can be norms or specific values (e.g., integral or point quantities).
  - Enables iterative refinement for optimal meshes.
  - Provides efficient a posteriori error control and economical meshes.

- **Historical Context and Applications**:
  - DWR method by Becker and Rannacher, based on Babuška and Rheinboldt's work.
  - Refined by others (Eriksson, Estep, Hansbo, Johnson).
  - Applicable to various discretizations (Finite Element Methods, Finite Volume Methods).
  - Available in simulation tools (deal.II, FEniCS, Simcenter STAR-CCM+, Ingrid Cloud).
  - Used in diverse applications: fluid dynamics, structural dynamics, multi-physics problems (e.g., chemically reactive flows, fluid-structure interactions).

- **Limitations in Industrial Practice**:
  - Limited use despite potential for optimal meshes and reliable error estimates.
  - Requires adjoint problem solutions, needing specific simulation tool functionality.
  - Limited industrial tools provide this capability.

- **Proposed Solution**:
  - Learn optimal meshes trained on adjoint solutions.
  - Use these as starting points in other simulation tools, independent of numerical method.

### 2.2 Machine Learning in CFD

- **Integration of Machine Learning in CFD**:
  - Multiple methodologies exist for CFD.
  - Machine learning can be incorporated in various ways.

- **Replacement of CFD Simulation**:
  - Train networks to predict flow results based on geometry and flow parameters.
  - Performance depends on data quality and flow setup.
  - Example: Guo et al. achieved speedups for steady-state laminar flows with moderate error increase.

- **Challenges in Turbulent Flow Simulations**:
  - Direct network replacement of turbulent flow solvers is difficult.
  - Successful approaches often replace specific solver steps (e.g., pressure step).
  - Example: Ling et al. used a network to predict Reynolds stress anisotropy tensor in a modified RANS solver.
  - Kutz suggests deep neural networks could capture complex flow phenomena.

- **Rapidly Growing Field**:
  - Various approaches showing promise.
  - For extensive summaries, refer to recent reviews.

# 3 Data Generation Pipeline

Proper training requires a representative set of training data. This work employed supervised learning, necessitating the generation of input-output pairs with ground truth results. This is accomplished via a data generation pipeline with several key parts:

1. **Random Geometry Generation (Subsection 3.1)**
2. **Iterative Process of Primal Solves (Subsection 3.2)**
3. **Adjoint Solves (Subsection 3.3)**
4. **Mesh Refinement (Subsection 3.4)**

The generated data is then processed for training.

### 3.1 Random Geometry Generation

- **Objective**:
  - Generate a randomized set of geometries representative of the full space of possible CFD simulations within selected constraints.
  - Basis for generating datasets for machine learning.

- **Phases of Geometry Creation**:
  - **Primitives Phase**:
    - Randomly determine the number of primitives.
    - Use five basic primitives: triangle, square, pentagon, hexagon, and dodecagon.
    - Supports use of one or two primitives.

  - **Primitive Type Selection**:
    - Similar methodology as in , but omitting circles and ellipses.
    - Smooth sharp corners using splines.
    - Uniform distribution for geometry selection.

  - **Transform Phase**:
    - Apply several transformations to base primitives.
    - Start with a unit square.
    - Perform two extensions, one rotation, and a displacement.
    - **Extension**:
      - Random variables: axis of extension and extension factor.
      - Axis of extension: angle from horizontal plane (0 to 180°).
      - Extension factor ($\lambda$): normally distributed (mean: 3, standard deviation: 1.5).

  - **Positioning Phase**:
    - Randomly rotate and position the geometry within specified bounds.
    - First primitive: positioned in the middle of allowed bounds.
    - Second primitive (if used): randomly positioned to overlap with the first, using a uniform distribution.

  - **Spline Creation Phase**:
    - Use splines instead of straight lines to reduce sharp edges.
    - Randomly place midpoints between vertices.
    - Number of midpoints (0-5) uniformly distributed.

  - **Merge Phase**:
    - Merge transformed primitives using boolean operations (union or intersection).
    - **Union**: Combines the two primitives.
    - **Intersection**: Uses the region where the two primitives intersect.
    - Prevent arbitrary small intersecting regions by extending intersect regions by a random factor (3-5).

### 3.2 Iterative Process of Primal Solves

- Repeated primal solves are performed as part of the iterative process.
- Details of this process are described in Subsection 3.2.

### 3.3 Adjoint Solves

- Adjoint solves are performed after primal solves.
- Used to refine the mesh at the end of each iteration.
- Details of the adjoint solve process are described in Subsection 3.3.

### 3.4 Mesh Refinement

- Based on results from adjoint solves.
- Iterative refinement process to achieve optimal mesh.
- Details of the mesh refinement process are described in Subsection 3.4.

### Data Processing for Training

- The data generated by the pipeline is processed to be used for training the machine learning models.

### 3.2 CFD Simulation: Primal Solve

After generating random geometries, the next step is to set up the primal CFD simulation to ensure convergence across a variety of geometries. This section outlines the inputs for the primal solver, the adjoint solver, and the subsequent mesh refinement process. Simcenter STAR-CCM+ , a commercial CFD software by Siemens Digital Industry Software, is used for these simulations.

#### 3.2.1 Computational Domain

- **Domain Size and Positioning**:
  - Generated geometry is placed in a region of size $L \cdot L$.
  - Positioned $75L$ from the inlet, upper, and lower boundaries, and $225L$ from the outlet (Figure 2).
  - Blockage ratio: less than 0.0005% to ensure free slip boundary conditions.
  - Length $L$ set to 5m, domain scaled accordingly.
  - Domain fully within turbulent regime, suitable for fast-moving medium-sized objects (e.g., vehicles, wind-tunnel applications).

- **Boundary Conditions**:
  - **Inlet Boundary**:
    - Flow defined as subsonic and incompressible.
    - Inflow velocity perpendicular to boundary wall: $17.6 \, \text{m/s}$ (approximately $60 \, \text{km/h}$).
  - **Outlet Boundary**:
    - Flow regime defined as subsonic with a static pressure of 1 atm.
  - **Upper and Lower Wall Boundaries**:
    - Considered as far-field, defined as free-slip walls.
  - **Randomly Generated Geometry**:
    - Defined as a no-slip wall with smooth wall roughness.

#### 3.2.2 Initial Mesh Setup

- Initial mesh must have good quality to enhance the robustness of the mesh refinement process.
- Objective: Learn mesh sensitivity relative to specific input geometries.

### 3.4 CFD Simulations with Adaptively Refined Meshes

After obtaining the adjoint error, it was proceed with mesh refinement based on the estimated error per cell $\epsilon(i)$. The process involves:

- **Error Threshold Comparison**:
  - Compare $\epsilon(i)$ to a threshold (e.g., $\epsilon(i) > 0.1 \max(\text{adjoint error estimate})$).
  - If $\epsilon(i)$ exceeds the threshold, refine the affected cell by reducing cell base size in the local region.

- **Mesh Continuity and Growth Ratio**:
  - Ensure neighboring cells are adapted for a continuous mesh.
  - Use a growth ratio of 1.17 to maintain smooth transitions in the domain.

- **Iterative Refinement Process**:
  - Obtain new adjoint solution after each refinement by repeating primal and adjoint solves with the refined mesh.
  - Continue refinement until adjoint solution reaches a steady state or the adjoint solver no longer converges.
  - New primal and adjoint solves required for each refinement step.

- **Outcome**:
  - Example of a mesh after multiple refinements shown in Figure 4.

# 4 Neural Network Training Pipeline

- CFD simulations typically use non-rectilinear mesh structures with varying cell sizes, making prediction challenging.
- Predicting individual edge or node positions via a neural network is infeasible due to the variability in the number and size of cells.
- Instead, the focus is on predicting the average cell size in a region, corresponding to the mesh refinement level.
- This target can be represented in a rectilinear grid, suitable for image processing techniques.
- Cell sizes are exported as images, with the grayscale channel indicating relative cell size.
- These images are blurred and down-sampled to 128x128, representing mesh refinement levels, and fed into a convolutional neural network (CNN) for training.

### 4.1 Neural Network Architecture

- **Chosen Architecture**: Staircase UNet Architecture.
- **Base Model**: UNet with skip-connections, as used in .
  - **Structure**:
    - Convolutional neural network with multiple layers.
    - Each layer involves convolution, activation function, down-sampling, or up-sampling.
    - Additional performance enhancements include batch normalization and dropout (discussed later).

- **Basic UNet Architecture**:
  - Shown in Figure 5 (blue).
  - Number of convolutional channels increases with down-sampling and decreases with up-sampling.
  - Symmetric architecture used as input and output data are of the same size.

- **Skip-Connections**:
  - Used successfully in  to predict flow-based quantities.
  - Shown in Figure 5 (light red lines).
  - Transfer information between specific input and output layers.
  - Address the problem of small gradients in initial layers by reducing the effective distance between output and input layers.
  - Improve training of deeper networks by equalizing gradient magnitudes.

- **Staircase UNet Architecture**:
  - Modifies the UNet with additional layers at each depth.
  - Performs additional convolutions before up- or down-sampling.
  - Visual representation in Figure 5.
  - Aim: Preserve more information during skip-connections.
  - **Outer Skip-Connections**: Information is immediately upsampled (e.g., connecting $C_{21}$ and $U_{22}$).
  - **Inner Skip-Connections**: Additional convolution before upsampling (e.g., connecting $C_{21}$ and $U_{21}$ or $C_{22}$ and $C_{21}$).

### 4.2 Data Pre-Processing for Training

- **Data Export**: Cell sizes exported as images from CFD solver.
- **Image Processing**:
  - Grayscale channel represents relative cell size.
  - Images blurred and down-sampled to 128x128.
- **Training Targets**: Down-sampled images represent mesh refinement levels, suitable for CNN input.

### 4.2 Data Preparation

#### 4.2.1 Smoothing

- **Challenges**:
  - Input images often have sharp edges due to significant value differences in adjacent cells.
  - Capturing individual cells with arbitrary shapes and sizes is difficult in machine learning.

- **Solution: Gaussian Blur**:
  - Used to smooth edges and improve training.
  - Common in graphics and computer vision.

- **Gaussian Function**:
  - $G_{\sigma}(x, y) = \frac{1}{2\pi\sigma^2}\exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$
  - Depends on parameters $\sigma$ (standard deviation) and radius $r$.

- **Gaussian Blur Application**:
  - For a pixel at $(x, y)$, Gaussian blur $B_{\sigma, r} (x, y)$ is:
  
$$
  B_{\sigma, r} (x, y) = \frac{1}{k} \sum_{rx=-r}^{r} \sum_{ry=-r}^{r} G_{\sigma}(rx, ry) F(x + rx, y + ry)
  $$

  - Normalization factor $k$:
  
$$
  k = \sum_{rx=-r}^{r} \sum_{ry=-r}^{r} G_{\sigma}(rx, ry)
  $$

  - $F(x, y)$ is the pixel value in the original image.

- **Boundary Conditions**:
  - Neumann boundary conditions applied.
  - Domain beyond the boundary assumed to be the same color as the boundary.

- **Selective Blur for Geometry Pixels**:
  - Geometry pixels excluded to preserve boundary information.
  - Modified convolution kernel excludes data from geometry pixels:
  
$$
  B_{\sigma, r} (x, y) = \frac{1}{k(x, y)} \sum_{rx=-r}^{r} \sum_{ry=-r}^{r} G_{\sigma}(rx, ry) F(x + rx, y + ry) Geo(x + rx, y + ry)
  $$

  - Normalization factor for selective blur:
  
$$
  k(x, y) = \sum_{rx=-r}^{r} \sum_{ry=-r}^{r} G_{\sigma}(rx, ry) Geo(x + rx, y + ry)
  $$

  - $Geo(x, y)$ is an indicator function for geometry (0 inside geometry, 1 otherwise).

- **Parameters Chosen**:
  - $\sigma = 10$
  - $r = 3\sigma = 30$

#### 4.2.2 Downsampling

- Downsampling is performed to reduce the image resolution to an acceptable size for the neural network.
- The transformation of the image is also applied to geometry.
- Several methods can be used for this step, such as Fourier or Wavelet transforms; however, averaging is used in this context.
- Initially, images exported from the CFD solver are at a resolution of 4000x4000 and a single grayscale channel, before being cropped to 3840x3840.
- The images are then downsampled and blurred simultaneously using the kernel from equation (4), with a size of 30 and a stride of 30 without padding.
- This process results in a final image size of 128x128.
- Both the input and output of the network operate at this size.
- Due to the large number of images and their high initial resolution, this post-processing was implemented using CUDA, increasing throughput by 2-3 orders of magnitude.

### 4.3 Training

#### 4.3.1 Hyperparameters

After identifying the best-performing networks (refer to subsection 4.1), a systematic hyperparameter sweep was performed. Preliminary models used parameters listed in Appendix C. Initial results indicated that networks with larger kernels and more convolutional channels performed better, likely due to the ability to capture more complex or larger features. Key parameters identified for further tuning include:

1. Beta parameters for the Adam optimizer
2. Scalar or tensor skip-connection
3. Skip-connection constraints
4. Skip-connection location

**Beta Parameters**

- **Adam Optimizer**:
  - Adds "momentum" to weight updates by including unbiased first and second moment estimates of previous updates.
  - Benefits: Handles sparse data (similar to AdaGrad) and noisy, non-stationary data (similar to RMSProp) due to bias correction in moving averages.

- **Parameters**:
  - $\beta_1$ and $\beta_2$: Control decay rate of moving averages.
  - Performance highly sensitive to changes in $\beta_1$ and $\beta_2$.
  - Lower $\beta_1$ values tend to produce good results with skip connections of depths 1-3.

**Scalar and Tensor Skip-Connections**

- **Implementation**:
  - Scalar skip-connection combines data using a scalar $t \in [0, 1]$:
    
$$
    y = tC_2 + (1 - t)U_2 \quad \text{with} \quad C_2, U_2 \in \mathbb{R}^{n \times n \times c} , \quad t \in [0, 1]
    $$

  - Tensor skip-connection allows a separate scalar for each channel:
    
$$
    y = T \circ C_2 + (1 - T) \circ U_2 \quad \text{with} \quad C_2, U_2 \in \mathbb{R}^{n \times n \times c} , \quad T \in \mathbb{R}^{c}
    $$


- **Results**:
  - Experimented with both types.
  - No clear conclusion on which produced better results.

**Constrained Skip-Connections**

- **Constrained vs. Unconstrained**:
  - Constrained: Values clipped if they exceed 1 or drop below 0.
  - Unconstrained: Values mapped using a sigmoidal function.
  - Unconstrained skip-connections generally performed better.

**Skip Connection Location**

- **Depth Variation**:
  - Higher skip connections (depth 1 or 2) pass larger chunks of information, connecting earlier layers to the last few layers.
  - Lower skip connections pass smaller amounts of data, bypassing fewer convolutional layers.

- **Observations**:
  - Higher depth skip connections typically improve performance.
  - Not all skip connections are used during training—some parameters $t$ are close to 0.
  - Best performing architecture has skip connections at depths 2, 3, 4, and 5.

### 4.3.2 Loss Function

A custom loss function is employed in our neural network training to ensure the network does not learn from data inside the geometries. The loss function is masked using the geometry indicator. For example, the $L2$ loss is computed as follows:


$$ L(x, y, Geo) = \sum_{i \in \text{len}(x)} (x_i - y_i)^2 (1 - Geo_i) $$


where $Geo$ is an indicator function for the geometry and prism layer, $x$ is the prediction, and $y$ is the ground truth. This masking ensures that the loss calculation ignores the regions inside the geometries and prism layers.

- **Geometry Masking**:
  - $Geo$: Indicator function for geometry.
  - $1 - Geo_i$: Ensures loss is not computed inside the geometry.

- **Prism Layers**:
  - As Simcenter STAR-CCM+ does not support iterative refinement of prism layers, these are also masked.
  - Prevents the model from learning the extremely fine mesh density along the prism layers.

# 6 Conclusions and Outlook

- A novel machine learning-based approach for optimal mesh generation in computational fluid dynamics (CFD) applications was presented.
- The commercial CFD simulator Simcenter STAR-CCM+ was utilized, enhanced with an iterative mesh refinement loop to optimize meshes concerning overall error.
- The computational pipeline relied on an appropriate error estimator leveraging adjoint sensitivities.
- Over 60,000 simulations were conducted, generating 6 terabytes of data.
- Approximately 50 years of serial compute time on a CPU were utilized to achieve optimal results.

- **Data and Training**:
  - Tested and fine-tuned various neural network architectures using a subset of the dataset.
  - Relied on three different base architectures, all trained on the same dataset.
  - Automated testing of variants performed on multiple GPUs, equating to roughly 2 months of continuous single GPU training time.
  - Trained and tested multiple hundred variants, finding several highly accurate architectures.
  - Modified U-Net architecture with and without skip connections predicted refined mesh densities for random geometries with 98% accuracy (illustrated in Figure 9).

- **Effort and Automation**:
  - Significant effort in data creation, processing, and training.
  - Achieved through full automation of the entire process from CFD to neural network.
  - Resulting neural network aids inexperienced CFD users in generating reasonable initial mesh refinements for their geometries, reducing the need for tedious hand-tuning.

- **Impact on CFD Workflow**:
  - Use of neural networks provides a risk-averse approach to incorporating machine learning into CFD.
  - Helps avoid potential inaccuracies in simulations due to lack of physical knowledge in neural networks.
  - At worst, produces a bad mesh identifiable by lack of convergence; at best, significantly speeds up initial CFD setup phases for inexperienced engineers, producing usable results quickly.
  - Single prediction computation is quick, taking only seconds on consumer machines.

- **Future Directions**:
  - **Generalization**:
    - Expanding predictions to cover different geometry sizes and flow conditions.
    - Extending from 2D to 3D setups, despite the potential increase in required training data.
  - **Broader Applications**:
    - Leveraging machine learning in the overall CFD workflow to accelerate tasks dependent on personal experience, such as mesh creation.
    - Minimal impact on validation and verification of simulation methods, making it suitable for typical industrial use cases.
