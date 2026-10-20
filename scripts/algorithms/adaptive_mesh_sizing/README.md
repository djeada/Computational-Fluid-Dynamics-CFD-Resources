# Adaptive Mesh Sizing

This script learns a mesh-size field for a one-dimensional convection-diffusion boundary layer from optimally adapted training cases and uses it to mesh Peclet numbers it has not seen. The optimal density is obtained by equidistributing an interpolation-error indicator built from the exact second derivative; a ridge regression on two physically scaled features learns its logarithm; and linear finite-element solutions on uniform, optimally adapted and ML-predicted meshes are compared through their $L^2$ error as the number of elements grows.

## Overview

- Solves $-\varepsilon u'' + u' = 0$ on $[0, 1]$ with $u(0) = 0$, $u(1) = 1$ and $\varepsilon = 1/\mathrm{Pe}$, whose solution has a layer of width $\varepsilon$ at $x = 1$.
- For the training cases $`\mathrm{Pe} \in \{10, 20, 50, 100, 200, 500, 1000\}`$ computes the optimal normalised mesh density $\hat\rho(x)$ and samples 300 points per case (2100 training samples).
- Fits $\log_{10}\hat\rho$ with ridge regression on all monomials up to degree 4 in $s = \log_{10}\mathrm{Pe}$ and $`\xi = \log_{10}(1 + (1 - x)\,\mathrm{Pe})`$.
- For the test cases $\mathrm{Pe} = 30$, 300 and 3000 (the last outside the training range) builds meshes with $N = 10$ to 320 elements by equidistribution and solves the Galerkin finite-element problem on each.
- Prints the training error and the $L^2$ errors for $N = 20$, 80 and 320, and draws a four-panel figure.

## Mathematical Background

### Model problem

The exact solution is

```math
u(x) = \frac{e^{\mathrm{Pe}(x-1)} - e^{-\mathrm{Pe}}}{1 - e^{-\mathrm{Pe}}},
\qquad u''(x) = \frac{\mathrm{Pe}^2\, e^{\mathrm{Pe}(x-1)}}{1 - e^{-\mathrm{Pe}}}
```

With piecewise-linear elements the Galerkin method is stable only when the mesh Peclet number $h/(2\varepsilon)$ is below one inside the layer. A uniform mesh coarser than that produces node-to-node oscillations that pollute the whole domain.

### Optimal density

The piecewise-linear interpolation error on an element of size $h$ is of order $h^2|u''|$, so with a local size $h(x) = 1/(N\rho(x))$ the squared $L^2$ error is approximately

```math
\| u - I_h u\|_{L^2}^2 \approx C\int_0^1 h^4 |u''|^2\, dx = \frac{C}{N^4}\int_0^1
\rho^{-4}|u''|^2\, dx
```

Minimising the right-hand side subject to $`\int_0^1 \rho\,dx = 1`$ (a Lagrange multiplier gives $\rho^{-5}|u''|^2 = \mathrm{const}$) yields $\rho \propto |u''|^{2/5}$. The script uses the regularised form

```math
\rho(x) = \left(1 + \frac{|u''(x)|}{\alpha}\right)^{2/5},
\qquad \alpha = \left(\int_0^1 |u''|^{2/5}\, dx\right)^{5/2}
```

which keeps a minimum resolution outside the layer. With this integral choice of $\alpha$ the share of nodes inside $5\varepsilon$ of the wall stays between 0.43 and 0.50 for $\mathrm{Pe}$ from 30 to 3000. The density is normalised to $`\int_0^1 \hat\rho\,dx = 1`$, so the local mesh size for $N$ elements is $h(x) = 1/(N\hat\rho(x))$.

### Equidistribution

Nodes $x_0 = 0 < x_1 < \dots < x_N = 1$ are placed so that every element carries the same density mass,

```math
\int_{x_{j-1}}^{x_j} \hat\rho(x)\, dx = \frac{1}{N},
\qquad j = 1, \dots, N
```

by inverting the cumulative integral of $\hat\rho$ with linear interpolation.

### Learned size field

The regression input uses the wall distance in layer units, $`(1 - x)\,\mathrm{Pe}`$, which collapses the layers of different thickness onto one coordinate. The model $g(s, \xi) = \boldsymbol\phi(s, \xi)^T\boldsymbol\beta$ has 15 polynomial features, and $\boldsymbol\beta = (\Phi^T\Phi + \lambda I)^{-1}\Phi^T\mathbf{y}$ with $\lambda = 10^{-8}$. At prediction time $10^{g}$ is renormalised to unit integral before equidistribution.

## Implementation

- `exact_solution`, `exact_second_derivative` and `reference_grid` give $u$, $u''$ and a fine grid with 3000 extra points clustered geometrically in the layer.
- `optimal_density(x, pe)` and `equidistribute(x, rho, n_elements)` build adapted meshes.
- `solve_fem(nodes, pe)` assembles the tridiagonal Galerkin system and solves it with `scipy.linalg.solve_banded`; `l2_error` integrates the error on the union of the fine grid and the mesh nodes.
- `features`, `training_set`, `fit_ridge` and `predicted_density` implement the regression.
- `error_curves(pe, coef)` returns the error of the three mesh types for every entry of `NODE_COUNTS`.
- `TRAIN_PECLET`, `TEST_PECLET`, `POLY_DEGREE`, `RIDGE` and `DENSITY_EXPONENT` set the experiment.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Learned mesh-size fields and error vs number of elements for uniform, adapted and ML-predicted meshes](adaptive_mesh_sizing.png)

The top-left panel compares the optimal size field (solid) with the prediction (dashed) for the three unseen Peclet numbers. The training RMSE is 0.062 decades. The largest deviation from the optimal density is 0.11 decades at $\mathrm{Pe} = 30$, 0.34 decades (a factor 2.2) at $\mathrm{Pe} = 300$ and 0.76 decades at $\mathrm{Pe} = 3000$, always in the transition between the layer value and the outer value; inside the layer the prediction is close in all three cases. The top-right panel shows why adaptation matters: with 20 uniform elements at $\mathrm{Pe} = 300$ the Galerkin solution oscillates between $-0.77$ and $0.58$ at the interior nodes, while 20 elements placed by the learned size field follow the layer.

The bottom panels give the $L^2$ error. At $\mathrm{Pe} = 300$, inside the training range, the learned meshes are within 30% of the optimal ones for $N \geq 14$ and better than them at $N = 10$ ($6.4 \times 10^{-4}$ against $4.9 \times 10^{-4}$ at $N = 20$), while uniform meshes need far more elements for the same error ($1.7 \times 10^{-1}$ at $N = 20$ and $2.4 \times 10^{-3}$ at $N = 320$). At $\mathrm{Pe} = 3000$, outside the training range, the learned meshes are still more than two orders of magnitude better than uniform meshes, but up to 8.6 times worse than the optimal ones at small $N$ ($5.4 \times 10^{-3}$ against $8.4 \times 10^{-4}$ at $N = 20$) and about 1.6 times worse for $N \geq 113$. Both adapted families converge at the optimal rate $N^{-2}$, independently of the Peclet number.

## Related Notes

- [Machine Learning for Mesh Generation and Adaptation](../../../notes/machine_learning/geometry/ml_with_meshes.md)
- [Mesh Quality](../../../practice/mesh_generation/mesh_quality.md)
- [Boundary Layers](../../../practice/mesh_generation/boundary_layers.md)
