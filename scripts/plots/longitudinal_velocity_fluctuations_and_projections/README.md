# Longitudinal Velocity Fluctuations and Projections

This script plots synthetic two-point velocity fluctuations as time traces, as a scatter cloud, and projected onto a unit vector, which are the first steps of the two-point POD example. All three figures use one seeded, correlated data set: 1000 samples of $u'_a$ and $u'_b$ over $0.9 \le t \le 1.1$ s. The third figure projects every sample onto $\boldsymbol{\Phi} = (2, 1)/\sqrt{5} \approx (0.894, 0.447)$ and reports the variance along that direction.

## Overview

- Generates $u'_a \sim \mathcal{N}(0, 2^2)$ and $`u'_b = 0.5\,u'_a + \mathcal{N}(0, 2^2)`$ (m/s) and removes the sample means
- Figure 1: time traces of $u'_a(t)$ and $u'_b(t)$
- Figure 2: scatter plot of the $(u'_a, u'_b)$ pairs, whose elliptical shape shows the correlation
- Figure 3: the cloud, the line along $\boldsymbol{\Phi}$, and each sample's projection $a_i\boldsymbol{\Phi}$ drawn as a red point on that line
- Prints the covariance matrix, the correlation coefficient, and the variance along $\boldsymbol{\Phi}$

## Mathematical Background

### Reynolds Decomposition

An instantaneous velocity is split into a time mean and a fluctuation:

$$
U = \overline{U} + u',
\qquad \overline{u'} = 0
$$

Here the samples are generated directly as fluctuations, and their small sample mean is subtracted.

### Covariance and Correlation

With the $m \times 2$ fluctuation matrix $\mathbf{U}$:

```math
\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U},
\qquad \rho_{ab} = \frac{c_{12}}{\sqrt{c_{11}\,c_{22}}}
```

For the generator used here the exact values are $c_{11} = 4$, $c_{12} = 2$, $c_{22} = 5$, and $\rho_{ab} = 1/\sqrt{5} \approx 0.45$.

### Projection onto a Unit Vector

The scalar projection of sample $`\mathbf{u}'_i = (u'_{a,i}, u'_{b,i})`$ onto the unit vector $\boldsymbol{\Phi} = (\phi_1, \phi_2)$ and its position on the line are

```math
a_i = \mathbf{u}'_i \cdot \boldsymbol{\Phi} = u'_{a,i}\phi_1 + u'_{b,i}\phi_2,
\qquad \mathbf{p}_i = a_i\,\boldsymbol{\Phi}
```

The variance along $\boldsymbol{\Phi}$ is

```math
\mathrm{var}_{\boldsymbol{\Phi}} = \frac{1}{m-1}\sum_{i=1}^m
a_i^2 = \boldsymbol{\Phi}^T\mathbf{C}\,\boldsymbol{\Phi}
```

### Link to POD

POD looks for the direction that maximises $\boldsymbol{\Phi}^T\mathbf{C}\boldsymbol{\Phi}$ subject to $|\boldsymbol{\Phi}| = 1$. The solution is the leading eigenvector of $\mathbf{C}$, $\mathbf{C}\boldsymbol{\Phi} = \lambda_1\boldsymbol{\Phi}$. The fixed vector $(0.894, 0.447)$ used here is an arbitrary trial direction; its variance is larger than either $c_{11}$ or $c_{22}$ but smaller than $\lambda_1$. The companion script [eigenvector_projection](../eigenvector_projection/README.md) computes the optimal directions.

## Implementation

- `generate_fluctuations(n, sigma, coupling, seed)` returns the time array and the zero-mean `(n, 2)` data (`N_SAMPLES = 1000`, `SIGMA = 2`, `COUPLING = 0.5`, `SEED = 0`).
- `project(data, phi)` returns the scalar projections $a_i$ and the projected points $a_i\boldsymbol{\Phi}$.
- `plot_time_series(t, data)`, `plot_scatter(data)`, and `plot_projection(data, phi)` build the three figures; the two scatter figures use equal axis scaling.
- `main(argv=None)` prints the statistics and shows or saves the figures.

## Usage

```bash
python main.py                          # open the three figure windows
python main.py --no-show --output out   # save the three PNGs into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open plot windows |
| `--output DIR` | Create `DIR` and save `velocity_fluctuations_time_series.png`, `velocity_fluctuations_scatter.png`, and `velocity_fluctuations_projection.png` |

## Output

With the default seed the script prints

```math
\mathbf{C} = \begin{bmatrix} 3.82 & 2.15 \\ 2.15 & 5.38 \end{bmatrix}, \qquad \rho_{ab} = 0.47, \qquad \mathrm{var}_{\boldsymbol{\Phi}} = 5.85\ \text{m}^2/\text{s}^2
```

Figure 1 shows the two noisy fluctuation signals.

![Velocity fluctuation time series](velocity_fluctuations_time_series.png)

Figure 2 shows the tilted elliptical cloud of $(u'_a, u'_b)$ pairs.

![Scatter of velocity fluctuations](velocity_fluctuations_scatter.png)

Figure 3 shows the red projected points lying on the black line through the origin along $\boldsymbol{\Phi}$.

![Projection onto a unit vector](velocity_fluctuations_projection.png)

## Related Notes

- [POD Derivation in 2D](../../../notes/numerical/pod/derivation_in_2d.md)
- [POD Derivation in N Dimensions](../../../notes/numerical/pod/derivation_in_n_dim.md)
- [Reynolds Decomposition](../../../notes/fluid_mechanics/turbulence/reynolds_decomposition.md)
- [Turbulence Statistics](../../../notes/fluid_mechanics/turbulence/statistics.md)
