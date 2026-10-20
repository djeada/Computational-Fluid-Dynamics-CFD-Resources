# Proper Orthogonal Decomposition

Proper orthogonal decomposition (POD) extracts from a set of flow fields the orthonormal spatial modes that capture the most fluctuation energy, together with their time coefficients. These notes start from the problem statement and its continuous form, work through a two-point example and the general discrete derivation, cover the SVD and the method of snapshots as the algorithms used in practice, and end with gappy POD for incomplete data and sensor-based estimation. POD bases are the starting point of the [reduced-order models](../rom/rom.md) in the next folder.

## Table of Contents

### 1. [Proper Orthogonal Decomposition](./pod_intro.md)

The least-squares problem, the Fredholm eigenproblem of the two-point correlation tensor, optimality, history, energy fractions and truncation, uses in CFD, limitations, and comparison with DMD, spectral POD and Fourier modes.

### 2. [Two-Point POD: A Worked Example](./derivation_in_2d.md)

Velocity at two probes: covariance matrix, variance along a direction, principal axes as eigenvectors, energy split and rank-one mode contributions.

### 3. [POD for N Points](./derivation_in_n_dim.md)

Snapshot matrix with points in rows, covariance eigenproblem, coefficients and reconstruction, proofs of orthogonality and truncation error, turbulent kinetic energy per mode, and weighted inner products on non-uniform meshes.

### 4. [POD and the Singular Value Decomposition](./pod_vs_svd.md)

Modes as left singular vectors, $\lambda_i = \sigma_i^2/(M-1)$, equivalence of the direct and snapshot methods, Eckart–Young, accuracy, cost, and randomized SVD.

### 5. [The Method of Snapshots](./snapshot_pod.md)

Sirovich's $M \times M$ correlation matrix, recovery and normalisation of the spatial modes, and when the method is the right choice.

### 6. [Gappy POD](./gappy_pod.md)

Least-squares reconstruction from incomplete data, the masked Gram matrix, error bounds, the Everson–Sirovich iteration, and sensor placement.
