# Machine Learning for Flow Analysis and Modelling

Methods that work on flow data itself: finding structure in it, modelling its time evolution, closing the averaged equations, reconstructing it from measurements or coarse simulations, and using learned models to optimise and control flows.

## Table of Contents

### 1. [Flow Feature Extraction](./feature_extraction.md)

Dimensionality reduction, clustering, classification and sparse methods for identifying coherent structures and flow regimes.

### 2. [Flow Dynamics](./flow_dynamics.md)

Data-driven models of flow evolution: dynamic mode decomposition, Koopman analysis, SINDy, recurrent networks and neural ODEs.

### 3. [ML Turbulence Closures](./ml_turbulence_closures.md)

Learning corrections to RANS eddy-viscosity and Reynolds-stress models and to LES subgrid models, and keeping them stable inside a solver.

### 4. [Particle Image Velocimetry](./particle_image_velocimetry.md)

ML for PIV: velocity estimation from particle images, denoising, outlier detection and uncertainty.

### 5. [Super-Resolution and Flow Cleansing](./superresolution_and_flow_cleansing.md)

Reconstructing high-resolution, noise-free fields from coarse, sparse or noisy data.

### 6. [Optimization](./optimization.md)

Surrogate-based and ML-assisted optimisation of shapes and flow control strategies.
