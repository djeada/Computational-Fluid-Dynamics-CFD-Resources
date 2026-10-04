# Eigenvector Projection of Velocity Fluctuations

This script finds the principal directions of correlated 2D velocity fluctuations from the eigenvectors of their covariance matrix and projects the data onto them. It generates synthetic fluctuations $(u'_a, u'_b)$, removes the mean, and solves the $2 \times 2$ eigenvalue problem. It then produces two figures: the data cloud with the eigenvectors drawn as arrows, and the data projected onto each eigenvector. This is the two-point Proper Orthogonal Decomposition (POD) used in turbulence analysis.

## Overview

- Generates 1000 seeded samples with $u'_a \sim \mathcal{N}(0, 2^2)$ and $`u'_b = 0.7\,u'_a + \mathcal{N}(0, 2^2)`$ (m/s), then subtracts the sample mean
- Computes the sample covariance matrix with the $1/(m-1)$ normalisation
- Solves the symmetric eigenvalue problem with `numpy.linalg.eigh` and sorts the modes by decreasing eigenvalue
- Prints the covariance matrix, eigenvalues, and eigenvectors
- Figure 1: the data cloud with each eigenvector drawn as an arrow of length $\sqrt{\lambda_k}$
- Figure 2: each sample projected onto $\mathbf{e}_1$ (red) and $\mathbf{e}_2$ (blue), drawn as points in the same plane

## Mathematical Background

### Covariance Matrix

With the $m \times 2$ matrix of zero-mean samples $\mathbf{U}$ (rows $`\mathbf{u}'_i = (u'_{a,i}, u'_{b,i})`$):

```math
\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U} = \frac{1}{m-1}\begin{bmatrix}\sum_i u'^2_{a,i} & \sum_i u'_{a,i}u'_{b,i} \\ \sum_i u'_{a,i}u'_{b,i} & \sum_i u'^2_{b,i}\end{bmatrix}
```

### Eigenvalue Problem

```math
\mathbf{C}\,\mathbf{e}_k = \lambda_k\,\mathbf{e}_k,
\qquad \lambda_1 \ge \lambda_2
```

Because $\mathbf{C}$ is symmetric, the unit eigenvectors are orthogonal and form the principal axes of the data ellipse.

### Projection onto the Principal Directions

The scalar projection (POD coefficient) of sample $i$ on mode $k$ and its position in the plane are

```math
a_{k,i} = \mathbf{u}'_i \cdot \mathbf{e}_k,
\qquad \mathbf{p}_{k,i} = a_{k,i}\,\mathbf{e}_k
```

The variance of the coefficients equals the eigenvalue, $`\frac{1}{m-1}\sum_i a_{k,i}^2 = \mathbf{e}_k^T\mathbf{C}\,\mathbf{e}_k = \lambda_k`$. The first mode therefore carries the most fluctuation energy, and $\lambda_1 + \lambda_2 = \mathrm{tr}\mathbf{C}$.

## Implementation

- `generate_fluctuations(n, sigma, coupling, seed)` returns the zero-mean `(n, 2)` data array (`N_SAMPLES = 1000`, `SIGMA = 2`, `COUPLING = 0.7`, `SEED = 0`).
- `principal_directions(data)` returns the covariance matrix, the eigenvalues in descending order, and the eigenvectors as columns.
- `draw_eigenvectors(ax, eigenvalues, eigenvectors)` draws the arrows with `quiver`, scaled by $\sqrt{\lambda_k}$.
- `plot_raw_data_with_eigenvectors(...)` and `plot_projections_on_eigenvectors(...)` build the two figures on equal-aspect axes, so orthogonal directions look orthogonal.
- `main(argv=None)` prints the decomposition and shows or saves both figures.

## Usage

```bash
python main.py                          # open both figure windows
python main.py --no-show --output out   # save both PNGs into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open plot windows |
| `--output DIR` | Create `DIR` and save `eigenvector_projection_raw.png` and `eigenvector_projection_projections.png` |

## Output

With the default seed the script prints

```math
\mathbf{C} = \begin{bmatrix} 3.82 & 2.91 \\ 2.91 & 6.39 \end{bmatrix}, \qquad \lambda_1 = 8.28,\ \mathbf{e}_1 = (0.546, 0.838), \qquad \lambda_2 = 1.92,\ \mathbf{e}_2 = (-0.838, 0.546)
```

The first figure shows the tilted elliptical cloud, with the black arrow along its major axis and the shorter grey arrow along its minor axis.

![Raw data with eigenvectors](eigenvector_projection_raw.png)

The second figure shows the projections lying on two perpendicular lines through the origin. The red points along $\mathbf{e}_1$ spread much further (variance 8.28) than the blue points along $\mathbf{e}_2$ (variance 1.92).

![Projections on eigenvectors](eigenvector_projection_projections.png)

## Related Notes

- [POD Derivation in 2D](../../../notes/numerical/pod/derivation_in_2d.md)
- [Introduction to POD](../../../notes/numerical/pod/pod_intro.md)
- [POD Derivation in N Dimensions](../../../notes/numerical/pod/derivation_in_n_dim.md)
