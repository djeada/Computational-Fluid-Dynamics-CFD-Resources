# Eigenvector Projection of Velocity Fluctuations

This script generates correlated 2D velocity fluctuation data $(u'_a, u'_b)$, computes the covariance matrix, extracts its eigenvectors (principal directions), and produces two figures: the raw fluctuation data with eigenvectors overlaid as arrows, and the data projected onto each principal direction. The analysis mirrors the Proper Orthogonal Decomposition (POD) procedure widely used in turbulence research.

## Overview

- Generates correlated 2D Gaussian velocity fluctuation samples $(u'_a, u'_b)$
- Computes the 2×2 sample covariance matrix from the data
- Solves the eigenvalue problem to obtain principal directions and their energies
- Produces two plots: raw data with eigenvector arrows, and projected scalar signals

## Mathematical Background

### Covariance Matrix

$$C = \frac{1}{N-1}\begin{bmatrix}\langle u_a'^2\rangle & \langle u_a'u_b'\rangle \\ \langle u_a'u_b'\rangle & \langle u_b'^2\rangle\end{bmatrix}$$

### Eigenvalue Problem

$$C\,\mathbf{e}_i = \lambda_i\,\mathbf{e}_i$$

Each eigenvalue $\lambda_i$ equals the variance (energy) of the data along the corresponding eigenvector $\mathbf{e}_i$.

### Projection onto Principal Direction

$$p_i = \mathbf{u}'_i \cdot \mathbf{e}_1$$

where $\mathbf{u}'_i = (u'_{a,i},\, u'_{b,i})$ is the $i$-th fluctuation sample vector.

### Physical Interpretation

Eigenvalues equal the POD mode energies; eigenvectors define the principal axes of the velocity-fluctuation cloud, identifying the directions of maximum and minimum variance in the measured flow.

## Implementation

1. Define a covariance structure and draw $N$ correlated 2D Gaussian samples representing velocity fluctuations.
2. Subtract the sample mean to ensure zero-mean fluctuations.
3. Compute the 2×2 sample covariance matrix $C$.
4. Solve the eigenvalue problem to obtain eigenvalues $\lambda_1 \geq \lambda_2$ and eigenvectors $\mathbf{e}_1, \mathbf{e}_2$.
5. Plot 1: scatter the raw $(u'_a, u'_b)$ data and overlay $\mathbf{e}_1$, $\mathbf{e}_2$ as scaled arrows from the origin.
6. Plot 2: project each sample onto $\mathbf{e}_1$ and $\mathbf{e}_2$ and display both projections as time-series lines.

## Output

The script produces two figures. The first shows the 2D velocity fluctuation cloud with eigenvector arrows indicating the principal axes. The second shows scalar projection signals onto each eigenvector, demonstrating how POD separates the energetically dominant direction from the subdominant one.

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/2880d4e4-45ae-4f5b-a713-69cdcb7d675a)

![Figure_2](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/c955eeb5-d045-47c4-94e6-1146171edee1)
