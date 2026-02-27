# POD Spatial Modes and Temporal Coefficients

This script generates a three-dimensional synthetic spatio-temporal flow field $u(x, y, t) = \sin(0.02x)\cos(0.05y)\sin(0.5t)$ on a 50×30×100 grid, reshapes it into a snapshot matrix, and performs SVD to extract POD modes. The first three spatial modes are visualised as contour plots and their corresponding temporal coefficients are shown as time series, providing a complete picture of the dominant flow structures and their evolution in time.

## Overview

- Generates a 3D synthetic field on a 50×30×100 spatio-temporal grid
- Reshapes the field into a snapshot matrix of size (N_x N_y) × N_t
- Applies SVD to extract spatial POD modes and temporal coefficients
- Plots first three spatial modes as filled contour plots (one per subplot)
- Plots corresponding temporal coefficients as time series in a separate panel

## Mathematical Background

### Snapshot Matrix

The 3D field $u(x, y, t)$ is reshaped into:

$$U \in \mathbb{R}^{N_x N_y \times N_t}, \qquad N_x = 50,\; N_y = 30,\; N_t = 100$$

### SVD Decomposition

$$U = \Phi \Sigma \Psi^T$$

where columns of $\Phi$ are the spatial POD modes and columns of $\Psi$ are the temporal coefficients.

### Spatial Modes and Temporal Coefficients

$$\phi_i \in \mathbb{R}^{N_x N_y} \quad \text{reshaped to } (N_x, N_y) \text{ for visualisation}$$

$$a_i(t) = \psi_i(t), \quad i = 1, 2, 3$$

The singular values $\sigma_i$ encode the energy of each mode.

## Implementation

1. Build coordinate grids `x = np.linspace(0, 49, 50)`, `y = np.linspace(0, 29, 30)`, `t = np.linspace(0, 99, 100)`.
2. Compute field `u[i, j, k] = sin(0.02*x[i]) * cos(0.05*y[j]) * sin(0.5*t[k])`.
3. Reshape to snapshot matrix `U = u.reshape(Nx*Ny, Nt)`.
4. Compute SVD: `Phi, sigma, PsiT = np.linalg.svd(U, full_matrices=False)`.
5. Reshape first three columns of `Phi` to `(Nx, Ny)` and plot as contour maps.
6. Plot first three rows of `PsiT` as temporal coefficient time series.

## Output

The script produces two sets of panels: three contour plots showing the spatial structure of the first three POD modes over the (x, y) domain, and three time-series plots showing the corresponding temporal coefficients $a_i(t)$. The dominant mode captures the primary oscillation pattern encoded in the synthetic field.
