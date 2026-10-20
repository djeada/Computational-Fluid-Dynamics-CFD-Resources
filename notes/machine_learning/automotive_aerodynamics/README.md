# Case Study: ML for Automotive Aerodynamics

A worked project that applies the methods of this section to vehicle aerodynamics: defining a parametric design space, generating and validating a CFD dataset, and training and evaluating models that predict forces and flow fields for new designs. The notes follow the order of the project.

## Table of Contents

### 1. [Overview](./ml_process.md)

The prediction task, the workflow from design space to deployed model, force coefficients, model choice, error metrics and public datasets.

### 2. [Deformation Parameters and Shape Morphing](./deformation_parameters.md)

The morphing methods and the parametric shape changes (bonnet, windscreen, rear end and others) that span the design space, and how to rank them by sensitivity.

### 3. [Design of Experiments and Dataset Construction](./datasets.md)

How to place the samples in the design space, how many are needed, and how to split them without leaking information between training and test sets.

### 4. [Generating CFD Training Data](./generating_cfd_datasets.md)

Solver, turbulence-model and mesh choices, grid-convergence checks and averaging windows that keep the error in the labels below the error the surrogate is asked to reach.

### 5. [Building and Validating a Mesh Dataset](./dataset_of_meshes.md)

Mesh quality metrics, consistency checks across hundreds of meshes, and coverage of the design space.

### 6. [Output Data: CFD Results as Machine-Learning Targets](./output_data.md)

Force coefficients, surface and volume fields, their averaging uncertainty, and how they are turned into training targets.

### 7. [Training and Evaluating Surrogates Across Vehicle Designs](./model_training.md)

Training models on single and merged design families and testing how they generalise to a geometry they have not seen.
