# Radial Basis Functions

This script fits a multiquadric radial basis function (RBF) interpolant through 11 scattered data points sampled from a non-linear test function. RBF interpolation is a mesh-free technique widely used in CFD for scattered-data interpolation, mesh deformation, and data-driven surrogate modelling; this example shows the complete workflow from data generation to prediction and visualisation.

## Overview

- Samples 11 training points from a smooth non-linear test function.
- Constructs a multiquadric RBF interpolant using SciPy's `Rbf` class.
- Evaluates the interpolant on a fine prediction grid and compares it to the true function.
- Plots the training data, the RBF prediction, and the ground truth on a single figure.
- Illustrates how the shape parameter $\varepsilon$ governs the width of each basis function and thus the global smoothness of the interpolant.

## Mathematical Background

### RBF Interpolant

Given $n$ training locations $x_1, \dots, x_n \in \mathbb{R}$ with associated response values $y_1, \dots, y_n$, the RBF interpolant is

$$\tilde{y}(x) = \sum_{i=1}^{n} w_i\, \phi\!\bigl(\|x - x_i\|\bigr),$$

where $\phi : [0,\infty) \to \mathbb{R}$ is the chosen radial basis function and $\mathbf{w} = (w_1, \dots, w_n)^T$ are the interpolation weights.

### Multiquadric Basis Function

The multiquadric basis function is

$$\phi(r) = \sqrt{1 + (\varepsilon\, r)^2},$$

where $r = \|x - x_i\|$ is the distance from the evaluation point to the $i$-th centre and $\varepsilon > 0$ is the shape parameter. Larger $\varepsilon$ produces a narrower, more peaked basis; smaller $\varepsilon$ yields a broader, flatter basis. The multiquadric is globally supported and conditionally positive definite.

### Weight Determination

Imposing exact interpolation at all $n$ training points gives the symmetric linear system

$$\Phi\,\mathbf{w} = \mathbf{y},$$

where $\mathbf{y} = (y_1, \dots, y_n)^T$ and the collocation matrix $\Phi \in \mathbb{R}^{n \times n}$ has entries

$$\Phi_{ij} = \phi\!\bigl(\|x_i - x_j\|\bigr) = \sqrt{1 + \varepsilon^2(x_i - x_j)^2}, \quad i,j = 1,\dots,n.$$

Because the multiquadric is conditionally positive definite of order 1, the system is non-singular for distinct centres.

### Interpolation Error

For sufficiently smooth target functions the RBF interpolant satisfies error estimates of the form

$$\|\tilde{y} - y\|_\infty \leq C\, h^k,$$

where $h$ is the fill distance (maximum gap between adjacent training points) and the exponent $k$ depends on the smoothness of $\phi$ and the target function.

## Implementation

1. **Training data** — evaluate the test function at 11 equally spaced locations $x_i$ and store the responses $y_i$.
2. **Interpolant construction** — instantiate `scipy.interpolate.Rbf(x_train, y_train, function='multiquadric')`; the constructor assembles $\Phi$ and solves $\Phi\mathbf{w} = \mathbf{y}$ internally.
3. **Prediction grid** — create a dense array of evaluation points spanning the training domain.
4. **Evaluation** — call the `Rbf` object on the prediction grid to obtain $\tilde{y}$ at each point.
5. **Plotting** — plot the true function as a reference curve, overlay the training points as markers, and draw the RBF prediction curve; add axis labels, a legend, and a title.

## Output

The script displays a single figure containing:

- The **true function** shown as a smooth reference curve over the full prediction domain.
- **Training data** displayed as discrete markers at the 11 sample locations.
- The **RBF interpolant** $\tilde{y}(x)$ plotted as a continuous curve, passing exactly through all training points and smoothly interpolating between them.
