# Machine Learning for CFD

These notes cover machine-learning methods that replace, accelerate or analyse parts of a CFD workflow: surrogates that map design parameters or geometries to forces and fields, physics-informed and operator-learning networks, learned turbulence closures, data-driven models of flow dynamics, reconstruction of measured and coarse fields, ML on CAD and meshes, and an automotive-aerodynamics case study that follows one project from dataset generation to model training. The emphasis is on the mathematics of each method and on what makes its predictions trustworthy for engineering use, with the general training and validation machinery treated once in `fundamentals/`.

## Prerequisites

The notes assume the CFD basics in [`notes/numerical/cfd/`](../numerical/cfd/intro.md) and linear algebra at the level of the singular value decomposition. Three numerical topics are used throughout:

- [Proper orthogonal decomposition](../numerical/pod/pod_intro.md) (`notes/numerical/pod/`), the linear baseline for dimensionality reduction and field surrogates;
- [Surrogate modelling](../numerical/surrogates/intro.md) (`notes/numerical/surrogates/`): kriging, radial basis functions and sampling plans, the first choice for small datasets;
- [Reduced-order models](../numerical/rom/rom.md) (`notes/numerical/rom/`), the projection-based alternative to learned dynamics.

## Suggested Reading Order

1. [Introduction](intro.md) for the problem statement and the map of methods.
2. [Neural Networks](fundamentals/neural_networks.md) and [Training and Validation](fundamentals/training_and_validation.md).
3. [Neural-Network Surrogates for Aerodynamics](neural_networks/intro.md), then [PINNs](neural_networks/pinns.md), [Neural Operators](neural_networks/neural_operators.md) and [Graph Neural Networks](neural_networks/graph_neural_networks.md), depending on the data you have.
4. The `flow/` notes in any order. [Flow Feature Extraction](flow/feature_extraction.md) and [Flow Dynamics](flow/flow_dynamics.md) connect most directly to POD and ROM.
5. The `geometry/` notes, then the `automotive_aerodynamics/` case study in the order listed below.

## Contents

| Note | Description |
| --- | --- |
| [Introduction to Machine Learning for CFD](intro.md) | Where ML enters the CFD pipeline, the learning paradigms and their objectives, the task-to-method map, physics integration and limitations |
| [Neural Networks](fundamentals/neural_networks.md) | MLPs, activation functions, universal approximation, backpropagation, optimisers, initialisation, scaling and spectral bias |
| [Training and Validation](fundamentals/training_and_validation.md) | Leak-free splits, scaling, bias-variance, regularisation, metrics, cross-validation, hyperparameter search, UQ and OOD detection |
| [Neural-Network Surrogates for Aerodynamics](neural_networks/intro.md) | Mapping parameters, grids, latent codes, point clouds or meshes to coefficients and fields, and when a surrogate pays off |
| [Graph Neural Networks for CFD](neural_networks/graph_neural_networks.md) | Encode-process-decode message passing on unstructured meshes, receptive fields, invariances and rollout stability |
| [Physics-Informed Neural Networks](neural_networks/pinns.md) | Training on the PDE residual, forward and inverse problems, boundary-condition enforcement and failure modes |
| [Neural Operators](neural_networks/neural_operators.md) | Learning solution operators with DeepONet and the Fourier neural operator, and discretization invariance |
| [Flow Feature Extraction](flow/feature_extraction.md) | POD, autoencoders, manifold learning, randomized and sparse methods, sensor placement and clustering of flow data |
| [Modeling Flow Dynamics](flow/flow_dynamics.md) | DMD, Koopman analysis, SINDy, recurrent networks, neural ODEs and the stability of learned dynamics |
| [Machine-Learned Turbulence Closures](flow/ml_turbulence_closures.md) | Field inversion, tensor-basis networks, learned subgrid and wall models, a priori versus a posteriori testing |
| [Machine Learning in Particle Image Velocimetry](flow/particle_image_velocimetry.md) | Cross-correlation PIV, outlier detection and uncertainty, and the CNN and PTV methods built on it |
| [Super-Resolution and Flow Cleansing](flow/superresolution_and_flow_cleansing.md) | Recovering fine, clean fields from coarse, noisy or gappy data as a regularised inverse problem |
| [Optimization with CFD and Machine Learning](flow/optimization.md) | Adjoint and gradient-free optimisation, Bayesian optimisation, multi-fidelity and multi-objective design |
| [Machine Learning on CAD Geometry](geometry/ml_on_cad.md) | Shape representations, parametric and PCA shape spaces, autoencoders, implicit fields and B-rep learning |
| [Machine Learning for Mesh Generation and Adaptation](geometry/ml_with_meshes.md) | Error estimation, goal-oriented and metric-based adaptation, and learned sizing fields |
| [Automotive Aerodynamics Case Study: Overview](automotive_aerodynamics/ml_process.md) | The workflow of the case study, force coefficients, model choice, metrics and public datasets |
| [Deformation Parameters and Shape Morphing](automotive_aerodynamics/deformation_parameters.md) | Morphing methods, the design parameters and global sensitivity analysis |
| [Design of Experiments and Dataset Construction](automotive_aerodynamics/datasets.md) | Sampling plans, discrepancy, dataset size, legacy data, decimation and leak-free splits |
| [Generating CFD Training Data](automotive_aerodynamics/generating_cfd_datasets.md) | Solver, turbulence-model and mesh choices, grid convergence and averaging error in the labels |
| [Building and Validating a Mesh Dataset](automotive_aerodynamics/dataset_of_meshes.md) | Quality metrics, consistency checks, y+ coverage and mesh independence across a dataset |
| [Output Data: CFD Results as Machine-Learning Targets](automotive_aerodynamics/output_data.md) | Scalar, surface and volume outputs, averaging uncertainty and turning results into training targets |
| [Training and Evaluating Surrogates Across Vehicle Designs](automotive_aerodynamics/model_training.md) | Cross-design experiments, field losses, integrated force errors and how to read the results |

Each subfolder has its own index: [fundamentals](fundamentals/README.md), [neural_networks](neural_networks/README.md), [flow](flow/README.md), [geometry](geometry/README.md) and [automotive_aerodynamics](automotive_aerodynamics/README.md).

## Notation

| Symbol | Meaning |
| --- | --- |
| $\mathbf{x}$, $\mathbf{p}$ | Model input; design or operating parameters |
| $\mathbf{y}$, $\hat{\mathbf{y}}$ | Target output and its prediction |
| $`\mathcal{D} = \{(\mathbf{x}_i, \mathbf{y}_i)\}_{i=1}^N`$ | Dataset of $N$ samples |
| $f_{\boldsymbol\theta}$, $\boldsymbol\theta$ | Model (network) and its parameters |
| $\mathcal{L}$, $\ell$ | Total loss and per-sample loss |
| $\lambda$ | Regularisation or penalty weight |
| $\eta$ | Learning rate |
| $W^{(l)}$, $\mathbf{b}^{(l)}$, $\sigma$ | Weights and biases of layer $l$; activation function |
| $\mathbf{u}$, $p$, $\nu$ | Velocity, pressure, kinematic viscosity |
| $C_d$, $C_L$, $C_p$ | Drag, lift and pressure coefficients |
| $\Phi$ | Matrix of POD modes |
