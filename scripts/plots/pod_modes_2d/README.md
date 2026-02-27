# POD Modes of 2D Velocity Field

This script applies Proper Orthogonal Decomposition to a synthetic time series of two-component (U, V) velocity data stored in a 1000×2 matrix. SVD extracts the dominant spatial modes and their temporal coefficients. The script then reconstructs the contributions of the first two POD modes separately and plots their individual and combined contributions to each velocity component, giving a direct view of how each mode shapes the flow.

## Overview

- Generates a 1000×2 synthetic velocity matrix with U and V components
- Performs SVD to extract POD modes and temporal coefficients
- Computes the contribution of each of the first two modes to U and V
- Plots mode 1, mode 2, and their sum for both velocity components
- Uses subplots for clear side-by-side comparison

## Mathematical Background

### Velocity Matrix and SVD

The velocity snapshot matrix $\mathbf{q} \in \mathbb{R}^{N_t \times 2}$ is decomposed as:

$$\mathbf{q} = \Phi \Sigma \Psi^T$$

where $\Phi \in \mathbb{R}^{N_t \times r}$ contains temporal modes and $\Psi \in \mathbb{R}^{2 \times r}$ contains spatial modes.

### Mode Contribution

The contribution of mode $k$ to the velocity field is:

$$q^{(k)} = \phi_k \, a_k(t), \qquad a_k = \sigma_k \psi_k^T$$

where $\phi_k$ is the $k$-th column of $\Phi$ and $\psi_k$ is the $k$-th column of $\Psi$.

### Reconstruction

$$\mathbf{q} \approx \overline{U}_1 + \overline{U}_2 + \cdots = \sum_{k=1}^{r} \phi_k \sigma_k \psi_k^T$$

## Implementation

1. Generate synthetic velocity data: sinusoidal U and V time series of length 1000.
2. Stack into matrix `q = np.column_stack([U, V])` and subtract mean.
3. Compute SVD: `Phi, sigma, PsiT = np.linalg.svd(q, full_matrices=False)`.
4. Compute mode contributions `q1 = sigma[0] * Phi[:, 0:1] @ PsiT[0:1, :]` and similarly for mode 2.
5. Plot mode 1, mode 2, and sum for U component and V component in separate subplots.
6. Label axes, add legend, and display the figure.

## Output

The script produces a multi-panel figure showing time series of the first and second POD mode contributions and their sum for both the U and V velocity components. The plot reveals how each mode captures a distinct oscillatory pattern and how their superposition reconstructs the original velocity signal.
