# POD Energy and Truncation

This script computes the POD of a synthetic cylinder-wake velocity field on a stretched mesh and shows how the number of retained modes $r$ follows from the eigenvalue spectrum, with the 90% and 99% energy thresholds and reconstructions of one snapshot with $r = 1, 2, 5$ and $10$ modes. Because the mesh cells have different sizes, the decomposition uses the area-weighted inner product, so that the eigenvalues are energies of the continuous field rather than sums over grid points.

## Overview

- Builds the transverse velocity $v/U_\infty$ of a model vortex street behind a cylinder of diameter $D$: three harmonics of the shedding frequency ($St = 0.2$, vortices convected at $0.8U_\infty$) plus 30 weaker travelling structures with random wavenumbers, and noise of standard deviation 0.01.
- Samples it on $120 \times 48$ points over $1 \le x/D \le 11$, $-3 \le y/D \le 3$, with the $y$ points clustered toward the centreline by a $\sinh$ stretching, at $M = 200$ instants spaced $0.2D/U_\infty$ apart (8 shedding periods).
- Forms the trapezoidal-rule area weights $w_k$ and computes the weighted POD by the SVD of $\mathbf{W}^{1/2}\mathbf{U}$, using `compute_pod` from [the shared POD code](../../_numerics.py).
- Prints the energy fractions of the first six modes with and without the weights, the number of modes needed for 90% and 99% of the energy, and the reconstruction errors.
- Plots (a) the normalised eigenvalue spectrum, (b) the cumulative energy with the thresholds, (c) a snapshot, (d)–(g) its reconstructions with $r = 1, 2, 5, 10$, and (h) the residual for $r = 10$.

## Mathematical Background

### Wake Model

Every structure has the form

```math
v_c(x, y, t) = A_c\, g(x)\, f_c\!\left(\frac{y}{b(x)}\right) \cos(k_c x - \omega_c t + \varphi_c), \qquad g(x) = \frac{x}{x_p} e^{1 - x/x_p}, \qquad b(x) = 0.5 + 0.1x
```

with $x_p = 4D$. The fundamental has $`\omega = 2\pi St\,U_\infty/D`$ and $k = \omega/(0.8U_\infty)$, a wavelength of $4D$; the second and third harmonics have $2k, 2\omega$ and $3k, 3\omega$ and cross-stream profiles that are odd and even in $y$. A travelling wave is the sum of two standing patterns,

```math
\cos(kx - \omega t + \varphi) = \cos(kx + \varphi)\cos\omega t + \sin(kx + \varphi)\sin\omega t
```

so each structure contributes a pair of POD modes with nearly equal eigenvalues, a quarter wavelength apart in $x$.

### Weighted POD

With the diagonal weight matrix $\mathbf{W} = \mathrm{diag}(w_k)$ the inner product $`\langle \mathbf{f}, \mathbf{g} \rangle_W = \mathbf{f}^T\mathbf{W}\mathbf{g}`$ approximates $`\int f g\, dA`$. If $`\mathbf{W}^{1/2}\mathbf{U}' = \boldsymbol{\Psi}\boldsymbol{\Sigma}\mathbf{V}^T`$, the weighted modes and coefficients are

```math
\boldsymbol{\Phi} = \mathbf{W}^{-1/2}\boldsymbol{\Psi}, \qquad \boldsymbol{\Phi}^T\mathbf{W}\boldsymbol{\Phi} = \mathbf{I}, \qquad \mathbf{A} = \boldsymbol{\Phi}^T\mathbf{W}\,\mathbf{U}' = \boldsymbol{\Sigma}\mathbf{V}^T, \qquad \lambda_i = \frac{\sigma_i^2}{M - 1}
```

### Truncation

The fraction of energy in the first $r$ modes and the root-mean-square relative error over all snapshots are

```math
E(r) = \frac{\sum_{i \le r}\lambda_i}{\sum_i \lambda_i}, \qquad \frac{\lVert \mathbf{U}' - \boldsymbol{\Phi}_r\mathbf{A}_r \rVert_W}{\lVert \mathbf{U}' \rVert_W} = \sqrt{1 - E(r)}
```

The error of an individual snapshot scatters around this value.

## Implementation

- `stretched_mesh(n_x, n_y, beta)`, `trapezoid_weights(coordinates)` and `area_weights(x, y)` build the mesh and the weights; the flattened index has $x$ varying slowest.
- `wake_components(seed)` draws the travelling structures and `wake_snapshots(x, y, t, seed, noise_std)` returns the $N \times M$ snapshot matrix, points in rows.
- `weighted_pod(snapshots, weights)` scales the rows by $\sqrt{w_k}$, calls `compute_pod`, and returns a `PODResult` whose modes satisfy $\boldsymbol{\Phi}^T\mathbf{W}\boldsymbol{\Phi} = \mathbf{I}$.
- `modes_for_energy(energy_fractions, threshold)` returns the smallest $r$ with $E(r) \ge$ threshold.
- `relative_error(pod, snapshots, weights, rank, index)` is the weighted relative error of one reconstructed snapshot.
- `plot_figure(...)` draws the eight panels; `RANKS`, `THRESHOLDS` and `SNAPSHOT_INDEX` choose what is shown.

## Usage

```bash
python main.py                      # open the figure
python main.py --no-show --output . # save pod_energy_and_truncation.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints

| $r$ | $E(r)$ | rms error, all snapshots | error, snapshot 37 |
| --- | --- | --- | --- |
| 1 | 40.8% | 76.9% | 68.8% |
| 2 | 80.7% | 43.9% | 44.4% |
| 5 | 92.3% | 27.8% | 27.3% |
| 10 | 95.6% | 20.9% | 17.1% |

90% of the energy needs $r = 4$ modes and 99% needs $r = 26$. The first six weighted energy fractions are 40.82, 39.92, 5.32, 5.27, 0.94 and 0.92%; without the weights they are 41.97, 41.31, 4.46, 4.43, 0.98 and 0.97%, and 99% is reached at $r = 24$. The unweighted decomposition counts the many small cells near the centreline too heavily, where the fundamental is strongest.

![POD energy spectrum and truncated reconstructions](pod_energy_and_truncation.png)

Panel (a) shows the eigenvalues in pairs, one pair per travelling structure. In (d) a single mode gives a standing pattern that cannot move: it is only half of the travelling fundamental. Two modes (e) give the convected vortex street, five (f) add the second harmonic, and ten (g) begin to resolve the small-scale structures; the residual (h) contains only small scales.

## Related Notes

- [Proper Orthogonal Decomposition](../../../notes/numerical/pod/pod_intro.md)
- [POD for N Points](../../../notes/numerical/pod/derivation_in_n_dim.md)
- [POD and the Singular Value Decomposition](../../../notes/numerical/pod/pod_vs_svd.md)
