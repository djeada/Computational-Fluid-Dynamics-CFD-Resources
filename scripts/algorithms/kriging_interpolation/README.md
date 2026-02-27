# Kriging Interpolation

This script demonstrates ordinary kriging interpolation using a cubic spline radial basis function (RBF). Eleven data points sampled from the test function $y(x) = (3x-3)^2 \sin(2x-10)$ are interpolated over a fine prediction grid for four values of the length-scale parameter $\theta$, illustrating how $\theta$ controls the smoothness and locality of the kriging surrogate.

## Overview

- Evaluates the test function at 11 equally spaced training points in a compact interval.
- Constructs a kriging surrogate for each of four $\theta$ values: $0.1$, $3$, $6.5$, and $10.0$.
- Uses SciPy's `Rbf` class with the `'cubic'` kernel to assemble and solve the interpolation system.
- Plots the true function, training data, and kriging prediction on a single figure with one curve per $\theta$.
- Highlights how small $\theta$ yields a smooth, slowly varying surrogate while large $\theta$ produces a more localised fit.

## Mathematical Background

### Kriging Model

The kriging surrogate is a weighted sum of correlation functions centred at the $n$ training locations $x_1, \dots, x_n$:

$$\tilde{y}(x) = \sum_{i=1}^{n} w_i\, R\!\bigl(|x - x_i|;\,\theta\bigr),$$

where $R(\cdot\,;\,\theta)$ is the chosen correlation (basis) function and $\mathbf{w} = (w_1, \dots, w_n)^T$ are the interpolation weights.

### Weight Determination

The weights are found by enforcing exact interpolation at all training points, leading to the linear system

$$R\,\mathbf{w} = \mathbf{y},$$

where $\mathbf{y} = (y(x_1), \dots, y(x_n))^T$ and the correlation matrix $R \in \mathbb{R}^{n \times n}$ has entries

$$R_{ij} = R\!\bigl(|x_i - x_j|;\,\theta\bigr), \quad i,j = 1,\dots,n.$$

### Cubic Spline Basis Function

The cubic spline RBF used here is the piecewise polynomial

$$R(h;\,\theta) = \begin{cases} 1 - \tfrac{3}{2}(\theta h)^2 + \tfrac{3}{4}(\theta h)^3, & \theta|h| \leq 1, \\ \tfrac{1}{4}\bigl(2 - \theta|h|\bigr)^3, & 1 < \theta|h| \leq 2, \\ 0, & \theta|h| > 2. \end{cases}$$

### Effect of $\theta$

The length-scale parameter $\theta$ determines the effective support radius of each basis function. A large $\theta$ concentrates influence near each training point, increasing the risk of ill-conditioning but producing sharper local features; a small $\theta$ gives broad, smooth interpolants.

### Test Function

The ground-truth function used to generate training data is

$$y(x) = (3x - 3)^2 \sin(2x - 10),$$

a non-linear oscillatory function that provides a challenging test for surrogate modelling.

## Implementation

1. **Training data** — evaluate $y(x)$ at 11 equally spaced points $x_i$ in the training domain.
2. **Prediction grid** — create a dense array of prediction locations spanning the same interval.
3. **Surrogate construction** — for each $\theta \in \{0.1, 3, 6.5, 10.0\}$, instantiate `scipy.interpolate.Rbf` with the training points, response values, and `function='cubic'`; the constructor internally assembles $R$ and solves $R\mathbf{w} = \mathbf{y}$.
4. **Prediction** — call the `Rbf` object on the prediction grid to obtain $\tilde{y}(x)$ at all prediction locations.
5. **Plotting** — plot the true function as a reference curve, overlay the training points as markers, and draw one kriging prediction curve per $\theta$; add a legend and axis labels.

## Output

The script displays a single figure containing:

- The **true function** $y(x) = (3x-3)^2 \sin(2x-10)$ as a solid reference curve.
- **Training data** shown as discrete markers at the 11 sample locations.
- **Four kriging prediction curves**, one per $\theta$ value, demonstrating the transition from a globally smooth surrogate ($\theta = 0.1$) to an increasingly localised fit ($\theta = 10.0$).
