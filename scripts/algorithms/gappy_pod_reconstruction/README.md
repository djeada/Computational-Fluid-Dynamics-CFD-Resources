# Gappy POD Reconstruction

This script reconstructs complete flow fields from incomplete data with gappy POD: a POD basis built from complete snapshots of a synthetic cylinder wake is fitted by least squares to held-out snapshots of which only 50% of the points, or a few point sensors, are known. It compares random sensor locations with locations chosen by QR factorization with column pivoting of the basis, shows how the error depends on the number of sensors and modes, and runs the iterative Everson–Sirovich procedure that builds the basis itself from gappy snapshots.

## Overview

- Uses the wake model of [pod_energy_and_truncation](../../plots/pod_energy_and_truncation/README.md) (transverse velocity $v/U_\infty$ of a vortex street plus small-scale travelling structures and noise) on a uniform $120 \times 48$ grid, $1 \le x/D \le 11$, $-3 \le y/D \le 3$.
- Builds the POD basis from $M = 200$ complete snapshots over $0 \le tU_\infty/D < 40$ with `compute_pod` from [the shared POD code](../../_numerics.py), and keeps $r = 10$ modes (95.6% of the energy).
- Tests on 20 snapshots at random times in $40 \le tU_\infty/D \le 60$, after the training record, with independent noise.
- Reconstructs each test snapshot from a random 50% of its points, and from $p$ point sensors placed at random or by QR pivoting.
- Sweeps the number of sensors $p$ (50 random layouts per $p$) and the number of modes $r$.
- Removes 30% of the entries of the training snapshots at random and refills them with the Everson–Sirovich iteration.

## Mathematical Background

### Gappy Least Squares

A snapshot is approximated as $`\mathbf{u} \approx \bar{\mathbf{u}} + \boldsymbol{\Phi}_r\mathbf{a}`$. When only the entries in the set $\mathcal{S}$ are known, with selection matrix $\mathbf{P}$ ($`\mathbf{P}^T\mathbf{P} = \mathbf{D}`$, the diagonal 0/1 mask), the coefficients minimise the misfit at the known points,

```math
\hat{\mathbf{a}} = \arg\min_{\mathbf{a}} \lVert \mathbf{P}(\mathbf{u} - \bar{\mathbf{u}} - \boldsymbol{\Phi}_r\mathbf{a}) \rVert_2^2, \qquad (\boldsymbol{\Phi}_r^T\mathbf{D}\boldsymbol{\Phi}_r)\,\hat{\mathbf{a}} = \boldsymbol{\Phi}_r^T\mathbf{D}(\mathbf{u} - \bar{\mathbf{u}})
```

and the full field is estimated as $\bar{\mathbf{u}} + \boldsymbol{\Phi}_r\hat{\mathbf{a}}$. If $\mathbf{u} - \bar{\mathbf{u}}$ lies in the span of $\boldsymbol{\Phi}_r$ and $\mathbf{P}\boldsymbol{\Phi}_r$ has full column rank, the recovery is exact. Otherwise the part of the field outside the basis is aliased into $\hat{\mathbf{a}}$, amplified by up to $`\lVert(\mathbf{P}\boldsymbol{\Phi}_r)^{+}\rVert_2 = 1/\sigma_{\min}(\mathbf{P}\boldsymbol{\Phi}_r)`$.

### Sensor Placement

QR factorization with column pivoting of $\boldsymbol{\Phi}_r^T$, $`\boldsymbol{\Phi}_r^T\boldsymbol{\Pi} = \mathbf{Q}\mathbf{R}`$, picks at each step the point whose row of $\boldsymbol{\Phi}_r$ has the largest component orthogonal to the rows already chosen; the first $r$ pivots are a greedy approximation to the $r$ points that maximise $|\det(\mathbf{P}\boldsymbol{\Phi}_r)|$. For $p > r$ the script continues greedily: with $\boldsymbol{\Theta} = \mathbf{P}\boldsymbol{\Phi}_r$, adding the row $\boldsymbol{\phi}_i$ multiplies $\det(\boldsymbol{\Theta}^T\boldsymbol{\Theta})$ by $`1 + \boldsymbol{\phi}_i^T(\boldsymbol{\Theta}^T\boldsymbol{\Theta})^{-1}\boldsymbol{\phi}_i`$, so the point with the largest value of that quadratic form is added.

### Everson–Sirovich Iteration

1. Fill every missing entry with the mean of the known values at that point.
2. Compute the POD of the filled snapshot matrix.
3. Re-estimate each snapshot from its known entries with $r$ modes by gappy least squares, and overwrite only the missing entries.
4. Repeat from step 2.

### Error Measure

All errors are relative errors of the fluctuation over the test snapshots, $`\lVert \hat{\mathbf{U}} - \mathbf{U} \rVert_F / \lVert \mathbf{U} - \bar{\mathbf{u}}\mathbf{1}^T \rVert_F`$. The full-data projection $`\boldsymbol{\Phi}_r\boldsymbol{\Phi}_r^T(\mathbf{u} - \bar{\mathbf{u}})`$ is the best any method using $r$ modes can do.

## Implementation

- `wake_components(seed)` and `wake_snapshots(x, y, t, seed, noise_std, noise_seed)` build the data, points in rows and snapshots in columns.
- `gappy_coefficients(modes, mean, values, observed)` solves the masked least-squares problem with `numpy.linalg.lstsq` (minimum-norm solution when $p < r$); `gappy_reconstruct` returns the full-field estimate.
- `qr_sensors(modes, n_sensors)` takes the pivots of `scipy.linalg.qr(modes.T, pivoting=True)` and adds further sensors by the determinant rule; `random_sensors(n_points, n_sensors, rng)` draws distinct points uniformly.
- `reconstruct_all(modes, mean, truth, observed)` handles either one shared sensor set (many right-hand sides at once) or one mask per snapshot.
- `iterative_gappy_pod(data, observed, rank, n_iter, truth)` implements the Everson–Sirovich iteration and records the error of the filled entries.
- `run_experiments(seed)` performs all computations; `plot_results(res)` draws the nine panels. Constants such as `RANK`, `GAP_FRACTION`, `SENSOR_COUNTS`, `N_RANDOM_DRAWS` and `N_ITERATIONS` set the experiment.

## Usage

```bash
python main.py                      # open the figure
python main.py --no-show --output . # save gappy_pod_reconstruction.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints a test-set error of 0.240 for the full-data projection with $r = 10$, and the same 0.240 from 50% random gaps: with 2880 known points for 10 unknowns, the gaps cost nothing measurable. With 20 sensors the condition number of $\mathbf{P}\boldsymbol{\Phi}_{10}$ is 2.0 for the QR layout and 29.9 for the random layout shown. Selected rows of the sensor sweep:

| $p$ | QR pivoting | random, median of 50 |
| --- | --- | --- |
| 10 | 0.325 | 4.380 |
| 14 | 0.304 | 1.015 |
| 20 | 0.292 | 0.566 |
| 40 | 0.284 | 0.343 |
| 80 | 0.282 | 0.281 |
| 120 | 0.281 | 0.266 |

With 30 QR sensors the error is lowest at $r = 30$ (0.177). The Everson–Sirovich iteration reduces the error of the filled entries from 1.006 for the mean fill to 0.225 after 10 iterations, and the basis it produces reconstructs the gappy test snapshots with error 0.242, against 0.240 for the basis from complete data.

![Gappy POD reconstruction](gappy_pod_reconstruction.png)

Panels (a)–(c) show that a random half of the points is plenty. Panel (d) marks the 20 QR sensors (black circles), which lie in two short rows, one on the centreline and one at $0.6 \le y/D \le 1$, all within $2 \le x/D \le 6$ where the fluctuations peak, and 20 random sensors (green triangles), many of which fall where the field is nearly zero. The QR layout (e) gives a smooth estimate with error 33%; the random layout (f) overshoots, error 46%. Panel (g) shows that QR placement is close to its asymptote already at $p = r$, while random placement needs several times more sensors and has a wide spread between layouts. For $p \ge 80$ random layouts catch up and are slightly better, because the error is then dominated by the energy outside the 10-mode basis, which spread-out random sensors sample more evenly than the clustered QR sensors. Panel (h) shows the gappy error following the full-data projection exactly for 50% gaps, while with 30 fixed sensors the error falls until $r = p$ and rises sharply when $r > p$ and the problem becomes underdetermined. Panel (i) shows the iterative filling converging in about three iterations.

## Related Notes

- [Gappy POD](../../../notes/numerical/pod/gappy_pod.md)
- [Flow Feature Extraction](../../../notes/machine_learning/flow/feature_extraction.md): sparse sensor placement by QR pivoting
- [Proper Orthogonal Decomposition](../../../notes/numerical/pod/pod_intro.md)
