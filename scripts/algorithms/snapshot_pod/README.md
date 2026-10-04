# Snapshot Proper Orthogonal Decomposition (Snapshot POD)

This script computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one. It plots the three leading spatial modes next to their temporal coefficients and prints the share of fluctuation energy in each.

## Overview

- Generates the same synthetic field as the [POD script](../pod/README.md): three separable structures on a $50 \times 30$ grid with 100 time samples.
- Builds the $1500 \times 100$ snapshot matrix and subtracts the temporal mean at every point.
- Forms the $100 \times 100$ temporal correlation matrix $C_s$ and solves its symmetric eigenvalue problem with `numpy.linalg.eigh`.
- Recovers the spatial modes by projecting the data onto the eigenvectors and normalises them to unit length.
- Prints the energy fraction $\lambda_i / \sum_j \lambda_j$ of the first three modes.
- Plots the first three spatial modes next to their amplitude-scaled temporal coefficients.

## Mathematical Background

### Temporal Correlation Matrix

For the mean-subtracted snapshot matrix $\tilde{U} \in \mathbb{R}^{N \times M}$, with $N$ spatial points and $M$ snapshots:

$$
C_s = \frac{1}{M-1} \tilde{U}^T \tilde{U} \in \mathbb{R}^{M \times M}
$$

### Eigenvalue Problem

$$
C_s \mathbf{a}_i = \lambda_i \mathbf{a}_i,
\qquad \lambda_1 \geq \lambda_2 \geq \cdots \geq 0
$$

where the $\mathbf{a}_i$ are unit-norm temporal eigenvectors and $\lambda_i$ is proportional to the energy of mode $i$.

### Spatial Modes

```math
\boldsymbol{\phi}_i = \frac{\tilde{U} \mathbf{a}_i}{\|\tilde{U} \mathbf{a}_i\|}
```

### Link to the SVD

If $\tilde{U} = \Phi \Sigma \Psi^T$, then $\lambda_i = \sigma_i^2/(M-1)$, $\mathbf{a}_i = \boldsymbol{\psi}_i$ and $\boldsymbol{\phi}_i$ is the $i$-th column of $\Phi$, each up to sign. The snapshot method and the direct SVD therefore give the same modes and energy fractions. The snapshot method is cheaper when $M \ll N$.

The amplitude-scaled time coefficient of spatial mode $i$ is $a_i(t) = \sigma_i\psi_i(t)$. Both examples plot this quantity, rather than the unit-norm temporal eigenvector alone.

## Implementation

- `generate_synthetic_data` and `create_snapshot_matrix` come from [the shared numerical helpers](../../_numerics.py), so both POD examples use the same field and matrix orientation.
- `compute_pod(snapshots, method="snapshot")` forms $C_s$, calls `numpy.linalg.eigh`, sorts the eigenpairs, and discards numerical null modes before normalizing.
- The returned `PODResult` contains unit-norm spatial `modes` and amplitude-scaled `coefficients` $A = \Sigma\Psi^T$. Its `eigenvalues` are $\sigma_i^2/(M-1)$ and its `energy_fractions` give each retained mode's energy share.
- `result.reconstruct(n_modes)` reconstructs the original data, including its temporal mean. Constant fields retain no fluctuation modes and reconstruct from their mean.
- `plot_snapshot_modes_and_time_coeffs` uses the same paired contour/time-series layout as the SVD example.
- `N_SAMPLES`, `N_X`, `N_Y` and `NUM_MODES` set the data size and the number of modes plotted.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![First three snapshot POD modes and temporal coefficients](snapshot_pod_modes.png)

The printed energy fractions are 49.14 %, 39.16 % and 11.70 %, identical to the SVD-based POD script. The modes and temporal coefficients match that script's figure up to the sign of each mode, which is arbitrary in both methods. Mode 1 is the $\cos(2t)$ structure, mode 2 the slowly varying $\sin(0.5t)$ structure, and mode 3 the $\sin(4t)$ structure.

## Related Notes

- [Snapshot POD](../../../notes/numerical/pod/snapshot_pod.md)
- [SVD and POD](../../../notes/numerical/pod/pod_vs_svd.md)
- [POD Introduction](../../../notes/numerical/pod/pod_intro.md)
