# Radial Basis Functions

This script interpolates eight samples of the Forrester function $y(x) = (6x-2)^2 \sin(12x-4)$ with six radial basis function (RBF) kernels, written directly in numpy, and plots the interpolants and their pointwise errors. RBF interpolation needs no mesh, which is why it is used for scattered-data interpolation, mesh deformation and surrogate modelling in CFD, and the comparison shows how much the choice of kernel matters for the same data.

## Overview

- Samples the test function at eight equally spaced points on $[0, 1]$ (spacing $1/7$).
- Interpolates with four kernels without a polynomial tail (Gaussian, multiquadric and inverse multiquadric with shape parameter $\varepsilon = 5$, Wendland $C^2$ with support radius 0.4) and two kernels with a linear tail (thin-plate spline and cubic).
- Evaluates every interpolant at 1001 points and prints its RMS and maximum error.
- Plots the interpolants with the samples, and the absolute errors on a log scale.

## Mathematical Background

### Interpolant

```math
s(x) = \sum_{j=1}^{N} w_j\,\varphi(|x - x_j|) + \sum_{k=0}^{m} c_k x^k
```

The interpolation conditions $s(x_i) = y_i$ and, when a tail of degree $m$ is present, the side conditions $\sum_j w_j x_j^k = 0$ for $k = 0, \dots, m$ give

```math
\begin{pmatrix} A & P \\ P^T & 0 \end{pmatrix}\begin{pmatrix} \mathbf{w} \\ \mathbf{c} \end{pmatrix} = \begin{pmatrix} \mathbf{y} \\ \mathbf{0} \end{pmatrix},
\qquad A_{ij} = \varphi(|x_i - x_j|),
\qquad P_{ik} = x_i^k
```

Without a tail the system is $A\mathbf{w} = \mathbf{y}$.

### Kernels

| Kernel | $\varphi(r)$ | Type | Tail used |
| --- | --- | --- | --- |
| Gaussian | $e^{-(\varepsilon r)^2}$ | positive definite | none |
| Multiquadric | $\sqrt{1 + (\varepsilon r)^2}$ | $-\varphi$ conditionally positive definite of order 1 | none (nonsingular by Micchelli's theorem) |
| Inverse multiquadric | $1/\sqrt{1 + (\varepsilon r)^2}$ | positive definite | none |
| Wendland $C^2$ | $(1 - r/\rho)_+^4 (4r/\rho + 1)$ | positive definite in up to 3 dimensions, compact support $\rho$ | none |
| Thin-plate spline | $r^2 \ln r$ | conditionally positive definite of order 2 | linear |
| Cubic | $r^3$ | conditionally positive definite of order 2 | linear |

## Implementation

- `test_function(x)` evaluates the Forrester function.
- `KERNELS` maps each name to the pair (function $\varphi(r)$, tail degree), with $-1$ meaning no tail. `thin_plate(r)` handles $\varphi(0) = 0$.
- `fit_rbf(x, y, phi, degree)` assembles and solves the (augmented) system with `numpy.linalg.solve`, and `evaluate_rbf(...)` evaluates $s(x)$.
- `interpolate_all(x, y, x_new)` runs every kernel, and `plot_interpolants(...)` draws the figure.
- `N_SAMPLES`, `N_PREDICT`, `EPSILON` and `WENDLAND_SUPPORT` set the experiment.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Six RBF interpolants of the Forrester function and their pointwise errors](radial_basis_functions.png)

| Kernel | RMS error | Max error |
| --- | --- | --- |
| Gaussian | 0.299 | 0.852 |
| Multiquadric | 0.634 | 2.145 |
| Inverse multiquadric | 0.444 | 1.185 |
| Wendland $C^2$ | 0.367 | 0.988 |
| Thin-plate spline + linear | 0.751 | 2.128 |
| Cubic + linear | 0.797 | 2.619 |

All six interpolants pass through the samples, where the error drops to zero, and they look alike at the scale of the left panel. The right panel shows that their errors differ by a factor of almost three, with the largest errors in the last interval, where the function rises from 0 to 15.8. The ranking depends on $\varepsilon$ and $\rho$; the [RBF Shape Parameter Trade-Off](../../plots/rbf_shape_parameter_tradeoff/) script shows how to choose $\varepsilon$.

## Related Notes

- [Radial Basis Functions](../../../notes/numerical/surrogates/radial_basis_functions.md)
- [Surrogate Models in CFD](../../../notes/numerical/surrogates/intro.md)
