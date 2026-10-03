## Machine Learning on Meshes

Generating high-quality computational meshes for CFD simulations has traditionally required deep domain expertise and iterative manual refinement, making it one of the most time-consuming steps in the simulation pipeline. Goal-oriented adaptive refinement methods like the dual weighted residual approach produce excellent meshes but require solving expensive adjoint problems for every new geometry. ML offers a way to learn the mapping from geometric features to optimal mesh density distributions, enabling rapid mesh generation for new cases without repeated adjoint solves.

Integrating machine learning (ML) into computational fluid dynamics (CFD) opens new avenues for optimizing mesh generation—cutting down on both time and the specialized expertise traditionally required to achieve high simulation accuracy.

Historically, crafting an optimal computational mesh has depended on expert intuition, iterative trial-and-error, and significant computational resources. Engineers manually adjust and refine meshes based on experience and iterative validation, often using complex goal-oriented adaptive refinement techniques that are computationally expensive and challenging to implement in routine industrial workflows.

By contrast, an ML-driven approach leverages a curated database of high-quality meshes to train models that can predict optimal mesh densities directly from geometric features. Once trained, these models can provide accurate starting points for new simulations, thereby reducing manual intervention and accelerating the setup process. This not only makes high-fidelity simulations more accessible in environments where domain expertise is limited but also ensures consistency and reproducibility. Statistical learning from large datasets minimizes human error and subjective decision-making, leading to robust and reliable mesh configurations.

Below is a schematic comparing the traditional manual process with the ML-driven approach:

```
Traditional Process (Manual Mesh Generation)
  ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
  │  Expert Knowledge  │─────►│   Trial & Error    │─────►│    Refine Mesh     │
  └────────────────────┘      └────────────────────┘      └────────────────────┘
                                                    │
                                                    ▼
                                            ┌────────────────────┐
                                            │     Validate       │
                                            └────────────────────┘
                                                    │
                                                    ▼
                                            ┌────────────────────┐
                                            │      Repeat        │
                                            └────────────────────┘

---------------------------------------------------------

ML-Driven Approach (Mesh Generation with Machine Learning)
  ┌─────────────────────────────┐      ┌─────────────────────────────┐
  │ Precomputed Optimal Meshes  │─────►│     Train ML Model          │
  └─────────────────────────────┘      └─────────────────────────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────────────────┐
                                          │    Predict Mesh Density     │
                                          └─────────────────────────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────────────────┐
                                          │   Direct Use in CFD         │
                                          └─────────────────────────────┘
```

In this framework, ML serves as a surrogate for the traditionally expensive, iterative mesh refinement process. By automatically generating high-quality mesh predictions based on learned geometric patterns, ML streamlines CFD workflows—enabling rapid, reproducible, and accurate simulations across a range of industrial applications.

## State of the Art

CFD simulations are inherently computationally expensive, with costs rising steeply as mesh resolution increases. Adaptive mesh refinement techniques can optimize computational resources by concentrating effort only where needed, yet they typically require expert tuning and the solution of additional, often complicated, adjoint equations.

Recent advances in ML have shown promise in various aspects of CFD, such as surrogate modeling for flow predictions and reduced-order modeling for turbulence closures. However, applying ML directly to predict the optimal mesh configuration remains a nascent area of research. The idea is to use ML not to replace the underlying physics-based solvers but to intelligently guide them by providing high-quality initial meshes that reduce the overall computational burden.

This integration of ML into the CFD pipeline represents a model shift: rather than iteratively refining meshes using computationally expensive error estimators, engineers can use a pre-trained model to obtain an excellent approximation of the mesh density distribution. Such models, when trained on a rich dataset of optimal meshes, are well-equipped to generalize to new geometries and flow conditions.

### Adaptive Grid Refinement

Classical adaptive refinement techniques rely on goal-oriented error estimators to determine where the mesh requires further resolution. One prominent method is the dual weighted residual (DWR) approach. In DWR, both the primal (original) and the adjoint (sensitivity) problems are solved. The error in a specific quantity of interest (like drag or lift) is then estimated, and the mesh is refined in regions that contribute most to that error.

While DWR provides a systematic way to achieve an optimal mesh, it is computationally intensive because it necessitates solving the adjoint problem—a challenge in complicated industrial applications. By coupling DWR-derived data with ML, it becomes possible to capture the necessary mapping from flow features to mesh density without having to solve the adjoint problem for every new case.

```
ASCII Diagram: Adaptive Refinement with DWR

    Initial Mesh
      |
      v
  Primal Solve -> Adjoint Solve -> Compute DWR-based Error
      |                                   |
      v                                   v
  Identify Regions Requiring Refinement -> Refine Mesh Iteratively
```

The idea is to use the DWR process offline to generate high-quality meshes and then train an ML model on these examples. Once trained, the ML model can rapidly predict where mesh refinement is needed, effectively bypassing the repeated cost of the adjoint solve during the simulation workflow.

### Machine Learning in CFD

ML has been increasingly applied to various steps in the CFD process. Some methods use ML to entirely replace parts of the solver for specific flow regimes, while others enhance existing numerical techniques, such as turbulence modeling or pressure-velocity coupling. The success of these applications heavily relies on high-quality training data and rigorous validation protocols.

In the context of mesh generation, ML models excel at interpolating within the bounds of their training data. They can rapidly produce approximations that, while not perfect, are often sufficiently accurate to serve as the starting point for further, more precise refinements. However, caution is required when applying these models to novel geometries or flow conditions that deviate significantly from the training set, as ML models may struggle with extrapolation.

The strength of ML in CFD lies in its ability to learn complicated patterns from data. In mesh generation, these patterns relate geometric features and flow characteristics to the optimal distribution of mesh cells. This data-driven insight can lead to more efficient simulations, reducing both the time and cost associated with high-fidelity CFD analyses.

## Data Generation Pipeline

A strong training dataset is necessary for developing an ML model capable of predicting mesh densities accurately. The authors devised a comprehensive pipeline that begins with random geometry generation, followed by CFD simulations (primal solves), adjoint solves, and iterative mesh refinement. The output is a set of optimal meshes that serve as ground truth for training the ML model.

```
ASCII Diagram: Data Generation Pipeline

       Random Geometries
             |
      Primal CFD Solves  ->  Adjoint Solves  ->  Mesh Refinement
             |                                  ^
             v                                  |
          Optimal Meshes (Ground Truth) <---------
```

This pipeline is designed to cover a wide variety of geometrical configurations and flow scenarios, making sure that the ML model is exposed to diverse situations. By systematically generating and refining these meshes, the pipeline creates a rich dataset that captures the nuances of optimal mesh distribution for different types of geometries.

#### Random Geometry Generation

The pipeline begins with the creation of random 2D geometries, such as polygons and splined shapes, which are then placed within a wind-tunnel-like domain. By blending and transforming simple geometric primitives, the process produces a diverse range of configurations. This diversity is important for training a strong ML model, as it makes sure that the model does not overfit to a narrow class of shapes but rather learns to generalize to a broad spectrum of geometries.

#### Primal and Adjoint Solves

For each randomly generated geometry, a high-fidelity CFD simulation (the primal solve) is performed until convergence. Once the flow field is obtained, an adjoint solve is conducted to assess the sensitivity of the mesh with respect to key performance metrics (e.g., drag or lift). The adjoint solution reveals how errors in different regions of the mesh propagate to the quantity of interest. This information is then used to pinpoint areas where mesh refinement will have the most significant impact on simulation accuracy.

#### Mesh Refinement

Using the error indicators derived from the adjoint solve, the mesh is iteratively refined. Cells that contribute substantially to the error in the target quantity are subdivided, while regions with minimal impact are left coarser. After several iterations, the mesh reaches an optimal state for that particular geometry. These refined meshes, now containing a spatially varying density that reflects the underlying physics, are used as ground truth data for ML training.

## Neural Network Training Pipeline

Predicting mesh densities directly from complicated and irregular CFD meshes is challenging. To address this, the problem is reformulated as predicting a spatial distribution of mesh cell sizes on a regular grid—essentially converting the mesh data into an image. In this representation, each pixel value corresponds to the local mesh size, allowing the use of convolutional neural networks (CNNs), which are well-suited for image processing tasks.

```
ASCII Diagram: From Mesh to Image for ML

   Irregular CFD Mesh          Regular Grid (Image)
        +----+           ->   2D array representing local
        |    |                mesh size as grayscale values
   +----+----+----+
   |    |    |    |
   +----+----+----+
   
After blurring and downsampling:
  A smooth image where pixel intensity
  indicates desired local mesh size.
```

This transformation enables the application of state-of-the-art computer vision techniques to CFD mesh generation. By converting the irregular mesh into a regular grid (an image), the model can use powerful CNN architectures to learn spatial patterns and relationships that dictate optimal mesh density.

#### Neural Network Architecture

The chosen network architecture is based on the UNet model, which is highly effective for image-to-image translation tasks. UNet uses an encoder–decoder structure with skip connections that allow fine details from the early layers to be preserved and combined with high-level features from deeper layers. The “staircase” modification—adding extra convolutional steps at each depth level—enhances the network’s capacity to reconstruct detailed spatial information, which is important for accurately predicting the local mesh sizes.

This architecture is particularly advantageous because it balances the need for capturing global context (the overall geometry) with the need to reproduce local detail (specific areas requiring refinement). The combination of these capabilities makes UNet a natural choice for converting complicated CFD mesh data into a predictive map of mesh densities.

#### Data Pre-Processing

Before training, the original mesh data is transformed into a format suitable for CNNs. High-resolution images are generated from the mesh data, where pixel intensities encode the local cell size. To manage noise and reduce data dimensionality, the images are subjected to Gaussian blurring and downsampling, resulting in standardized 128×128 images.

An important aspect of the pre-processing step is the use of masking. Regions corresponding to the interior of the geometry (e.g., solid bodies) and specialized regions such as prism layers near boundaries are masked out. This makes sure that the network focuses solely on the fluid domain, where mesh density critically influences simulation accuracy.

#### Training

The training phase involves thousands of mesh-image pairs, allowing the network to learn the complicated relationship between geometric features and optimal mesh density distributions. A masked loss function is used during training to make sure that errors in regions outside the fluid domain do not adversely affect the learning process. Formally, the masked mean squared error is defined as:

$$
\mathcal{L} = \frac{1}{\sum_{i} m_i} \sum_{i} m_i \bigl(\hat{d}_i - d_i\bigr)^2
$$

where $\hat{d}_i$ is the predicted mesh density at pixel $i$, $d_i$ is the ground-truth density from the adjoint-refined mesh, and $m_i \in \{0,1\}$ is the binary mask that is 1 for fluid-domain pixels and 0 for solid interior or prism-layer regions. The denominator $\sum_{i} m_i$ equals the number of fluid-domain pixels, ensuring the loss is averaged only over the physically meaningful region. This formulation ensures the network only receives gradients from physically meaningful regions.

A variety of hyperparameters are carefully tuned—ranging from the choice of optimizer (such as the Adam optimizer) to the configuration of skip connections and learning rates. Extensive experimentation shows that networks capable of capturing both large-scale patterns and minute details tend to perform best. The resulting model demonstrates high prediction accuracy, providing a reliable starting point for CFD simulations and, if necessary, further refinement using traditional methods.

### Further Reading

- **Machine Learning‑Based Optimal Mesh Generation in Computational Fluid Dynamics**\
  *Keefe Huang, Moritz Krügener, Alistair Brown, Friedrich Menhorn, Hans‑Joachim Bungartz, Dirk Hartmann (2021)*\
  Introduces a machine learning approach using convolutional neural networks to predict optimal mesh densities for efficient CFD simulations.\
  [arXiv:2102.12923](https://arxiv.org/abs/2102.12923)

- **MeshDQN: A Deep Reinforcement Learning Framework for Improving Meshes in Computational Fluid Dynamics**\
  *Cooper Lorsung, Amir Barati Farimani (2023)*\
  Proposes a reinforcement learning framework that iteratively coarsens meshes while maintaining accuracy in key CFD quantities such as lift and drag.\
  [DOI:10.1063/5.0138039](https://doi.org/10.1063/5.0138039)

- **MeshingNet: A New Mesh Generation Method based on Deep Learning**\
  *Zheyan Zhang, Yongxing Wang, Peter K. Jimack, He Wang (2020)*\
  Describes a novel deep learning–guided strategy that predicts local mesh density to drive automatic finite element mesh generation for various PDEs.\
  [arXiv:2004.07016](https://arxiv.org/abs/2004.07016)

- **SpaceMesh: A Continuous Representation for Learning Manifold Surface Meshes**\
  *Tianchang Shen, Zhaoshuo Li, Marc Law, Matan Atzmon, Sanja Fidler, James Lucas, Jun Gao, Nicholas Sharp (2024)*\
  Presents an innovative neural network framework that directly generates manifold polygonal meshes through a continuous latent connectivity space, useful for mesh repair and other geometry processing tasks.\
  [arXiv:2409.20562](https://arxiv.org/abs/2409.20562)

- **Mesh Generation for Flow Analysis by Using Deep Reinforcement Learning**\
  *Keunoh Lim, Sanga Lee, Kyungjae Lee, Kwanjung Yee (2024)*\
  Demonstrates an approach in which a reinforcement learning agent optimally propagates surface mesh points, ensuring high-quality mesh generation for CFD analysis.\
  [AIAA 2024-0382](https://doi.org/10.2514/6.2024-0382)

- **A Survey of Deep Learning‑Based Mesh Processing**\
  *He Wang & Juyong Zhang (2022)*\
  Provides a comprehensive review of geometric deep learning methods applied to mesh processing, covering both graph‑based and structure‑based techniques.\
  [Springer Link](https://link.springer.com/article/10.1007/s40304-021-00246-7)

- **Autonomous Geometry Processing Using Machine Learning and Forge**\
  *Autodesk University Article (2024)*\
  Explores how machine learning techniques can be applied to extract, segment, and process mesh data from CAD models, with implications for reverse engineering and automated design.\
  [Autodesk University](https://www.autodesk.com/autodesk-university/article/Autonomous-Geometry-Processing-Using-Machine-Learning-and-Forge)

## Setting Up the Problem

1. **Generate training geometries.** Create a diverse set of random 2D geometries (e.g., blended polygons and spline shapes) placed in a wind-tunnel domain.
2. **Run primal and adjoint CFD solves.** For each geometry, run a primal CFD solve to convergence, then perform an adjoint solve targeting a quantity of interest such as drag.
3. **Produce ground-truth meshes.** Use the adjoint-based error indicators to iteratively refine the mesh until it reaches an optimal state—these refined meshes serve as ground truth.
4. **Convert meshes to images.** Transform each optimal mesh into a regular-grid image (e.g., 128×128) where pixel intensity encodes local cell size, applying Gaussian blurring and downsampling to smooth out noise.
5. **Create masks.** Build a corresponding binary mask that excludes solid interior regions and prism layers so the network trains only on the fluid domain.
6. **Choose an architecture.** Use a UNet-based encoder–decoder with skip connections, which balances global context with local detail for image-to-image translation.
7. **Normalize inputs and outputs** (e.g., min–max or log scaling of cell sizes) to stabilize training.
8. **Train with a masked loss function** (e.g., masked MSE) so that errors inside masked regions do not influence gradient updates. Use the Adam optimizer and monitor validation loss for early stopping.
9. **Validate predictions.** Evaluate predicted mesh density images against adjoint-refined references using metrics such as mean absolute error within the fluid domain.
10. **End-to-end verification.** Optionally, feed the predicted density map back into a mesh generator and run a CFD solve to confirm that simulation accuracy is preserved.

## Key Takeaways

- ML can replace the expensive adjoint solve at inference time by learning the mapping from geometry to optimal mesh density, reducing mesh generation from hours to seconds.
- A diverse training dataset of randomly generated geometries and their adjoint-refined meshes is essential for the model to generalize beyond a narrow class of shapes.
- Converting irregular CFD meshes into regular-grid images enables the use of proven CNN architectures like UNet for spatial prediction tasks.
- Masking solid regions and prism layers during both preprocessing and loss computation ensures the network focuses on the fluid domain where mesh quality matters most.
- Predicted mesh densities should be validated end-to-end by running CFD solves on the generated meshes and comparing quantities of interest against adjoint-refined references.
- While ML models interpolate well within training data, caution is needed for geometries or flow conditions that differ significantly from the training distribution.

## Exercises

**Exercise 1.** On a $3 \times 3$ image the predicted densities are $\hat{d} = \begin{bmatrix} 0.2 & 0.4 & 0.5 \\ 0.3 & 0.9 & 0.6 \\ 0.1 & 0.2 & 0.3 \end{bmatrix}$ and the references are $d = \begin{bmatrix} 0.25 & 0.4 & 0.45 \\ 0.3 & 0.1 & 0.7 \\ 0.1 & 0.3 & 0.3 \end{bmatrix}$. The centre pixel lies inside the solid body ($m = 0$); all others have $m = 1$. Compute the masked MSE and the unmasked MSE.

<details>
<summary>Answer</summary>

The squared errors on the fluid pixels are $0.0025, 0, 0.0025, 0, 0.01, 0, 0.01, 0$, which sum to 0.025. The masked MSE is $0.025/8 = 3.125 \times 10^{-3}$.

The centre pixel adds $(0.9 - 0.1)^2 = 0.64$, so the unmasked MSE is $0.665/9 \approx 7.39 \times 10^{-2}$.

The single meaningless solid pixel inflates the loss about 24-fold. Without the mask, training would waste effort fitting values that are never used.

</details>

**Exercise 2.** The wind-tunnel domain is 4 m × 4 m and is rasterized at $1024 \times 1024$, then blurred and downsampled to $128 \times 128$. Compute the pixel size before and after downsampling. Can the network represent a 5 mm refinement zone around a sharp trailing edge?

<details>
<summary>Answer</summary>

Before: $4/1024 \approx 3.9$ mm. After: $4/128 = 3.125$ cm, a downsampling factor of 8.

A 5 mm zone is about one-sixth of an output pixel, so it cannot be resolved as a distinct feature. The network predicts a smooth, averaged size field, and the mesh generator must enforce minimum sizes near sharp features separately (for example, through boundary sizing or prism layers, which the note masks out).

</details>

**Exercise 3.** Cell sizes in the dataset range from $10^{-4}$ m to $10^{-1}$ m. Map the sizes $10^{-3}$ m and $10^{-2}$ m to $[0, 1]$ using (a) linear min–max scaling and (b) min–max scaling of $\log_{10}$ of the size. Which choice suits an MSE loss?

<details>
<summary>Answer</summary>

(a) Linear: $10^{-3} \to (10^{-3} - 10^{-4})/(10^{-1} - 10^{-4}) \approx 0.009$ and $10^{-2} \to 0.099$.

(b) Logarithmic: $10^{-3} \to (-3 + 4)/3 \approx 0.333$ and $10^{-2} \to 0.667$.

With linear scaling, every size below 1 cm is squeezed into the bottom tenth of the range. The MSE hardly notices a factor-of-10 error in the finest cells, which are the ones that matter most. In 2D the cell count scales as $1/h^2$, so relative errors matter, and the log scale handles them correctly.

</details>

**Exercise 4.** In a U-Net, a $3 \times 3$ convolution maps 64 channels to 128. How many parameters does it have? Starting from a $128 \times 128$ input with $2 \times 2$ pooling at each level, what is the spatial size after 4 poolings, and how many poolings are possible before reaching $1 \times 1$?

<details>
<summary>Answer</summary>

$3 \times 3 \times 64 \times 128 + 128 = 73{,}856$ parameters.

After 4 poolings: $128/2^4 = 8$, so $8 \times 8$.

Since $128 = 2^7$, seven poolings reach $1 \times 1$. At the $8 \times 8$ bottleneck each feature summarizes a large part of the domain (the global context), while the skip connections supply local detail. This is the balance the note describes.

</details>

**Exercise 5.** A DWR estimate gives five cells local residuals $\rho_K = (0.8, 0.1, 0.5, 0.05, 0.3)$ and adjoint weights $\omega_K = (0.1, 2.0, 0.4, 1.0, 0.05)$. Compute the indicators $\eta_K = \rho_K \omega_K$ and their sum. Using Dörfler marking with $\theta = 0.6$, find the smallest set of cells (largest indicators first) whose indicators sum to at least $\theta \sum_K \eta_K$. Comment on cell 1.

<details>
<summary>Answer</summary>

$\eta = (0.08, 0.2, 0.2, 0.05, 0.015)$, which sums to 0.545. The target is $0.6 \times 0.545 = 0.327$.

Sorted indicators: cells 2 and 3 (0.2 each) already give $0.4 \ge 0.327$, so cells 2 and 3 are refined.

Cell 1 has the largest residual but a small adjoint weight. Its error hardly affects the quantity of interest (for example, drag), so goal-oriented refinement leaves it alone. This geometry-to-importance mapping is what the ML model is trained to reproduce without solving the adjoint problem.

</details>

## References

- Becker, R., & Rannacher, R., "An optimal control approach to a posteriori error estimation in finite element methods", *Acta Numerica* 10, 2001.
- Dörfler, W., "A Convergent Adaptive Algorithm for Poisson's Equation", *SIAM Journal on Numerical Analysis* 33(3), 1996.
- Ronneberger, O., Fischer, P., & Brox, T., "U-Net: Convolutional Networks for Biomedical Image Segmentation", Medical Image Computing and Computer-Assisted Intervention (MICCAI), 2015.
- Kingma, D. P., & Ba, J., "Adam: A Method for Stochastic Optimization", International Conference on Learning Representations (ICLR), 2015.
- Pfaff, T., Fortunato, M., Sanchez-Gonzalez, A., & Battaglia, P. W., "Learning Mesh-Based Simulation with Graph Networks", International Conference on Learning Representations (ICLR), 2021.
