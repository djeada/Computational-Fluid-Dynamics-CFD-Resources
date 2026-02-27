# POD Analysis for Flow Fields

This script performs Proper Orthogonal Decomposition (POD) on a synthetic 100×50 snapshot matrix using Singular Value Decomposition (SVD). It then visualises the eigenvalue spectrum and the percentage of turbulent kinetic energy (%TKE) captured by each of the first ten modes on a dual y-axis plot. POD is widely used in CFD to identify the dominant coherent structures in a flow field and to build reduced-order models.

## Overview

- Generates a synthetic 100×50 snapshot matrix representing spatial-temporal flow data
- Applies SVD to extract POD modes, singular values, and temporal coefficients
- Computes eigenvalues and percentage TKE for each mode
- Plots eigenvalue magnitude and cumulative energy content on dual y-axes
- Provides a clear view of how many modes are needed to capture most of the flow energy

## Mathematical Background

### Snapshot Matrix and SVD

Given snapshot matrix $U \in \mathbb{R}^{100 \times 50}$, SVD decomposes it as:

$$U = \Phi \Sigma \Psi^T$$

where $\Phi$ contains spatial modes, $\Sigma = \text{diag}(\sigma_1, \sigma_2, \ldots)$, and $\Psi$ contains temporal coefficients.

### Eigenvalues

$$\lambda_i = \frac{\sigma_i^2}{M - 1}$$

where $M = 50$ is the number of snapshots and $\sigma_i$ are the singular values.

### Percentage Turbulent Kinetic Energy

$$\text{TKE}_i = \frac{\lambda_i}{\sum_j \lambda_j} \times 100\%$$

This quantifies the fraction of total energy captured by mode $i$.

## Implementation

1. Generate synthetic snapshot matrix `U = np.random.randn(100, 50)`.
2. Subtract the temporal mean to centre the data.
3. Compute SVD: `Phi, sigma, PsiT = np.linalg.svd(U, full_matrices=False)`.
4. Calculate eigenvalues `lam = sigma**2 / (M - 1)` and `%TKE` for modes 1–10.
5. Create a figure with dual y-axes: bar chart of eigenvalues (left) and line plot of %TKE (right).
6. Label axes, add legend, and display the figure.

## Output

The script displays a dual y-axis bar/line chart for the first ten POD modes. The left axis shows eigenvalue magnitude, decaying rapidly for higher modes. The right axis shows the percentage of TKE, illustrating how the first few modes dominate the energy content of the synthetic flow field.
