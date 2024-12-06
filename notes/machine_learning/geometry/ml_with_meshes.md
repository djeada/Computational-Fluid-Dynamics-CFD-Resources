# Machine Learning on Meshes

Applying **machine learning (ML)** to computational fluid dynamics (CFD) offers new opportunities to optimize meshes, reducing both the time and expertise needed to achieve suitable accuracy. The article by Huang, Krügener, Brown, Menhorn, Bungartz, and Hartmann (2021) explores using ML to predict mesh densities for improved simulation outcomes, bridging the gap between human experience-driven mesh generation and data-driven automation.

Traditionally, generating an **optimal computational mesh** demands expert knowledge and extensive iterative refinement. Although tools exist to achieve goal-oriented adaptive refinement, the complexity and computational cost often limit their industrial adoption. Integrating ML-based approaches promises to streamline this process, making CFD workflows more accessible and faster to set up, especially for users with limited simulation experience.

```
ASCII Diagram: From Manual to ML-Driven Mesh Generation

  Traditional Process:
    Expert Knowledge -> Trial & Error -> Refine Mesh -> Validate -> Repeat
                  (Time-consuming, skill-intensive)

  ML-Driven Approach:
    Precomputed Optimal Meshes -> Train ML Model -> Predict Mesh Density -> Direct Use in CFD
                  (Faster start, less trial & error)
```

## 1 Introduction

**Computer Aided Engineering (CAE)**, and specifically **CFD**, is integral to simulating and predicting fluid flows. However, accuracy and convergence often hinge on mesh quality, which can be challenging and resource-intensive to achieve. Goal-oriented adaptivity methods (like dual weighted residual approaches) can produce optimal meshes, but their computational expense and complexity limit their prevalence in industry.

**Machine Learning in CFD** has focused on accelerating flow solutions, but identifying optimal meshes remains a largely unresolved problem. The authors propose leveraging ML to predict mesh density distributions based on previously computed optimal meshes, making mesh refinement more accessible. The approach uses commercial CFD solvers (Simcenter STAR-CCM+) to generate training data, enabling the ML model to learn from industrial-grade solutions. The ML predictions serve as a starting point that can be refined further if necessary.

```
ASCII Diagram: ML-Driven Mesh Prediction Workflow

        Precomputed Optimal Meshes
                |
                v
     Train Convolutional Neural Network (CNN)
                |
                v
    Given New Geometry -> Predict Mesh Density -> Use in CFD Tools
```

## 2 State of the Art

CFD simulations are computationally expensive, scaling poorly with mesh size. Adaptive mesh refinement techniques exist, but they demand high-level expertise and computational resources. Machine learning methods have shown promise in speeding up certain parts of CFD, including surrogate modeling of flow fields and reduced-order modeling for turbulence closures. However, applying ML directly to determine the **optimal mesh configuration** is still in its infancy.

## 2.1 Adaptive Grid Refinement

Classical adaptive refinement relies on **goal-oriented error estimators** like the **dual weighted residual (DWR)** method to identify mesh regions needing refinement, improving accuracy economically. Although powerful, such methods are rarely used widely in industry due to their complexity and need for adjoint solutions. Coupling DWR-derived mesh data with ML could sidestep these limitations, letting the ML model predict good initial refinements without solving adjoint problems each time.

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

## 2.2 Machine Learning in CFD

ML can approximate or accelerate various steps in CFD. Some methods attempt to replace solvers entirely for certain flow regimes, while others augment parts of the pipeline, like turbulence modeling or pressure-velocity coupling steps. Training ML models requires high-quality data and careful validation. While ML models excel at interpolation within known data distributions, caution is needed for extrapolation and application to novel geometries and flow conditions.

## 3 Data Generation Pipeline

To train an ML model to predict mesh densities, a comprehensive training dataset is essential. The authors developed a pipeline using random geometry generation, primal CFD solves, adjoint solves, and iterative mesh refinement to produce optimal meshes. These optimal solutions then provide ground truth data for the ML model.

```
ASCII Diagram: Data Generation Pipeline

       Random Geometries
             |
      Primal CFD Solves  ->  Adjoint Solves  ->  Mesh Refinement
             |                                  ^
             v                                  |
          Optimal Meshes (Ground Truth) <---------
```

### 3.1 Random Geometry Generation

The pipeline generates random 2D geometries (e.g., polygons, splined shapes) placed into a wind-tunnel-like domain. By blending and transforming primitives, the authors ensure a wide range of configurations, helping the ML model generalize to diverse shapes.

### 3.2 Primal and 3.3 Adjoint Solves

For each geometry, a CFD simulation (primal solve) is run until convergence. Then an adjoint solve identifies how different local mesh errors affect quantities of interest (e.g., drag). Using these adjoint solutions, the pipeline refines the mesh in critical areas, iterating until reaching a near-optimal distribution of mesh density.

### 3.4 Mesh Refinement

Refinement is guided by adjoint-based error indicators. Cells that significantly influence the goal quantity are refined. After several iterations, the final mesh is considered optimal for that geometry. These optimal meshes serve as training examples.

## 4 Neural Network Training Pipeline

Predicting mesh densities directly from geometry is challenging, given that CFD meshes are irregular and vary in topology. The authors transform this problem into predicting a **spatial distribution of mesh cell sizes on a regular grid** (i.e., an image). By exporting mesh density as images, they can apply **convolutional neural networks (CNNs)**, common tools in computer vision.

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

### 4.1 Neural Network Architecture

A **UNet-based CNN** is chosen, as UNet architectures excel in image-to-image transformations. Skip-connections help retain detail from early layers, and the “staircase” modification involves additional convolutional steps at each depth, improving the network’s ability to reconstruct fine details.

### 4.2 Data Pre-Processing

Original mesh data is exported as high-resolution images. Gaussian blurring and downsampling yield manageable 128x128 images. This smoothing step reduces noise and aids training. Regions inside the geometry (solid areas) and prism layers are masked, ensuring the network learns only from the fluid domain.

### 4.3 Training

The model is trained on thousands of mesh-image pairs. The loss function is masked to exclude geometry interiors. Various hyperparameters (e.g., Adam optimizer parameters, skip-connection configurations) are tested extensively. Networks that effectively capture large-scale features and details generally perform better, achieving high prediction accuracy.

## 6 Conclusions and Outlook

The authors demonstrate a workflow where **machine learning** predicts near-optimal mesh densities for random geometries, providing a strong starting point for CFD simulations. This approach can significantly reduce setup times, enabling less experienced users to obtain reasonable mesh distributions quickly. In the worst case, if the ML-based mesh is suboptimal, standard refinement steps or solver diagnostics (like lack of convergence) can guide improvements.

As computing capabilities and data availability grow, extending this method to 3D geometries, different flow regimes, or larger domains is possible. Embedding these ML models into industrial CFD workflows can accelerate design studies and encourage broader adoption of adaptive techniques that previously required expert knowledge and heavy computations.

```
ASCII Diagram: Future Outlook

   Current Method: 2D Geometries, Basic Flows
           |
           v
    Extend to 3D, Complex Flows, Turbulent Regimes
           |
           v
  Integrate with Automated CFD Pipelines, 
  Faster Design Iterations, Broader Industrial Use
```

This ML-based mesh generation approach complements physics-based methods, providing a risk-averse and efficient path toward improved CFD workflows. By reducing reliance on human expertise and tedious iterative refinement, it helps democratize high-quality simulations, ultimately making CFD more accessible, time-efficient, and cost-effective for industrial applications.
