# Surrogate Models

Surrogate models replace an expensive CFD evaluation by a cheap function fitted to a limited number of runs, so that optimization, uncertainty quantification and sensitivity analysis become affordable. These notes cover the approximation problem and its validation, how to choose the sample points before and during a study, the two most used interpolating surrogates (radial basis functions and kriging), and how to combine simulations of different fidelity. Each note has worked examples and exercises, and most figures come from scripts in this repository that implement the methods in numpy.

## Table of Contents

### 1. [Surrogate Models in CFD](./intro.md)

The approximation problem, families of surrogates, the workflow from sampling to validation, leave-one-out shortcuts for RBF and kriging, uses in optimization and uncertainty quantification, and the curse of dimensionality.

### 2. [One-Stage Sampling Plans](./one_stage_sampling.md)

Factorial and Plackett–Burman designs, Latin hypercubes and maximin optimization, distance and discrepancy criteria, Halton and Sobol sequences with scrambling, orthogonal arrays, and a worked nine-point example.

### 3. [Radial Basis Function Interpolation](./radial_basis_functions.md)

Interpolation conditions, kernels and conditional positive definiteness, the polynomial tail, the shape-parameter trade-off with Rippa's LOOCV formula, and smoothing of noisy data.

### 4. [Kriging](./kriging.md)

The Gaussian-process model, the best linear unbiased predictor and its MSE, correlation functions, the nugget, maximum-likelihood estimation with the concentrated likelihood, and a one-dimensional worked example.

### 5. [Hierarchical Kriging and Variable-Fidelity Modelling](./hierarchical_kriging.md)

Correction functions, co-kriging and hierarchical kriging with the low-fidelity model as a scaled trend, the predictor and MSE, the Forrester test case, and when a second fidelity pays off.

### 6. [Adaptive Sampling](./adaptive_sampling.md)

Sequential designs with exploration, exploitation and balanced infill criteria, a numerical comparison against one-shot designs, stopping rules, and batch infill for parallel CFD runs.
