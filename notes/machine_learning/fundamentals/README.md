# ML Fundamentals

The general machinery behind every model in this section: how a neural network is built and trained, and how any model, neural or not, is validated so that its predictions on new CFD cases can be trusted. Read these before the specialised notes.

## Table of Contents

### 1. [Neural Networks](./neural_networks.md)

The multilayer perceptron, activation functions and their derivatives, universal approximation, regression losses, backpropagation in matrix form, SGD, momentum and Adam, Xavier and He initialisation, input and output scaling, spectral bias, and pointers to CNNs, autoencoders and recurrent networks.

### 2. [Training and Validation](./training_and_validation.md)

Training, validation and test splits and how random splits leak for time series and geometry families, feature scaling, the bias-variance decomposition, regularisation, error metrics, k-fold cross-validation, hyperparameter search, uncertainty quantification, out-of-distribution detection and a reporting checklist for CFD surrogates.

For the introduction to the whole section, see [Introduction to ML for CFD](../intro.md).
