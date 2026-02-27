# Snapshot Proper Orthogonal Decomposition (Snapshot POD)

This script implements the Snapshot POD method on synthetic spatio-temporal flow data. Unlike the direct SVD-based POD, the Snapshot POD computes modes by solving an eigenvalue problem in the smaller time domain, making it computationally efficient when the number of snapshots is much smaller than the number of spatial points.

## Overview

- Generates synthetic 3D spatio-temporal flow data using trigonometric functions.
- Constructs a snapshot matrix and applies mean-subtraction to center the data.
- Assembles and solves the temporal covariance eigenvalue problem to obtain time coefficients.
- Recovers spatial modes by projecting the data onto the temporal eigenvectors and normalizes them.
- Visualizes the leading modes and their time evolution side by side.

## Mathematical Background

Given a centered snapshot matrix $\tilde{U} \in \mathbb{R}^{N \times M}$ (where $N$ is the number of spatial points and $M$ is the number of snapshots), the Snapshot POD forms the temporal covariance matrix:

$$C_s = \frac{1}{M-1} \tilde{U}^T \tilde{U} \in \mathbb{R}^{M \times M}$$

The eigenvalue problem is then solved:

$$C_s \mathbf{a}_i = \lambda_i \mathbf{a}_i$$

where $\lambda_i$ are the eigenvalues (proportional to the energy of each mode) and $\mathbf{a}_i$ are the temporal eigenvectors, ordered by decreasing eigenvalue.

### Spatial Mode Recovery

The spatial modes are recovered by projecting the data onto the temporal eigenvectors:

$$\boldsymbol{\phi}_i = \tilde{U} \mathbf{a}_i$$

The modes are then normalized so that $\|\boldsymbol{\phi}_i\| = 1$.

### Advantages over Direct POD

When $M \ll N$ (many spatial points, few snapshots), forming $C_s \in \mathbb{R}^{M \times M}$ is far cheaper than the direct POD covariance matrix $C \in \mathbb{R}^{N \times N}$. Both approaches yield identical spatial modes.

## Implementation

1. **Synthetic Data Generation**: A 3D spatio-temporal field is generated using trigonometric functions over a grid in $x$, $y$, and $t$.
2. **Snapshot Matrix**: The 3D data array is reshaped into a 2D snapshot matrix of shape $(N_x \cdot N_y) \times N_t$.
3. **Snapshot POD**: The temporal covariance matrix $C_s$ is assembled and its eigenvalue problem solved. Spatial modes are computed by projection.
4. **Mode Normalization**: Spatial modes are normalized to unit norm.
5. **Visualization**: The first three spatial modes and temporal coefficients are plotted side by side.

## Output

The script produces a figure with two columns:
- **Left column**: Filled contour plots of the first three Snapshot POD spatial modes over the $(x, y)$ domain.
- **Right column**: Time series of the corresponding temporal eigenvectors $a_i(t)$.
