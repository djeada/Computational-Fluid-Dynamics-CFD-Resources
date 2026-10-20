# Neural Networks for Flow Prediction

Neural-network architectures that predict aerodynamic quantities and flow fields: surrogates on fixed inputs, graph networks on unstructured meshes, networks constrained by the governing equations, and operators that map between function spaces. The basics of networks and training are in [fundamentals](../fundamentals/README.md).

## Table of Contents

### 1. [Neural-Network Surrogates for Aerodynamics](./intro.md)

Neural-network surrogates that map geometry and flow conditions to force coefficients and fields, and how they compare with classical surrogates.

### 2. [Graph Neural Networks](./graph_neural_networks.md)

Representing a CFD mesh as a graph and predicting fields on it by message passing.

### 3. [Physics-Informed Neural Networks](./pinns.md)

Training a network on the residual of the governing equations and boundary conditions, with or without data.

### 4. [Neural Operators](./neural_operators.md)

DeepONet and the Fourier neural operator, which learn the solution operator of a parametric PDE rather than a single solution.
