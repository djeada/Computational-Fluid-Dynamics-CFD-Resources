# Image Compression Using SVD

This script demonstrates how Singular Value Decomposition (SVD) can be used to compress grayscale images by retaining only the $r$ largest singular values and their associated singular vectors. Truncating the full decomposition produces a rank-$r$ approximation that captures the dominant structure of the image while discarding fine detail, offering a controlled trade-off between file size and visual fidelity.

## Overview

- Loads a grayscale image and decomposes it with NumPy's `linalg.svd`.
- Reconstructs the image at ranks $r \in \{5, 25, 100\}$ and displays them alongside the original.
- Plots the singular value spectrum on a logarithmic scale to reveal the rapid decay typical of natural images.
- Plots the cumulative energy ratio $\mathcal{E}(r)$ versus rank to show how many singular values are needed to capture a given fraction of total image energy.
- Annotates each reconstructed panel with its rank and relative storage cost.

## Mathematical Background

### Singular Value Decomposition

Any real $m \times n$ matrix $A$ (the pixel intensity matrix of a grayscale image) can be factored as

$$A = U \Sigma V^T,$$

where $U \in \mathbb{R}^{m \times m}$ and $V \in \mathbb{R}^{n \times n}$ are orthogonal matrices and $\Sigma = \mathrm{diag}(\sigma_1, \sigma_2, \dots, \sigma_p)$ with $p = \min(m,n)$ and $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_p \geq 0$.

### Rank-$r$ Approximation

The best rank-$r$ approximation of $A$ in the Frobenius (and 2-norm) sense is given by the Eckart–Young theorem:

$$A_r = U_r \Sigma_r V_r^T = \sum_{i=1}^{r} \sigma_i \mathbf{u}_i \mathbf{v}_i^T,$$

where $U_r$ and $V_r$ contain the first $r$ columns of $U$ and $V$ respectively, and $\Sigma_r = \mathrm{diag}(\sigma_1, \dots, \sigma_r)$.

### Approximation Error

The Frobenius-norm error of the truncation is

$$\|A - A_r\|_F = \sqrt{\sum_{i=r+1}^{p} \sigma_i^2}.$$

### Cumulative Energy Ratio

The fraction of total signal energy captured by the first $r$ singular values is

$$\mathcal{E}(r) = \frac{\displaystyle\sum_{i=1}^{r} \sigma_i^2}{\displaystyle\sum_{i=1}^{p} \sigma_i^2}.$$

A value $\mathcal{E}(r) \approx 1$ means the rank-$r$ approximation is nearly lossless.

### Storage Comparison

The full image requires $m \times n$ values. The rank-$r$ approximation requires only $r(m + n + 1)$ values (the columns of $U_r$, the rows of $V_r^T$, and the $r$ singular values), yielding a compression ratio of

$$\rho = \frac{mn}{r(m+n+1)}.$$

## Implementation

1. **Load image** — read a grayscale image into an $m \times n$ NumPy array of floating-point pixel intensities.
2. **Full SVD** — compute $U$, $\boldsymbol{\sigma}$ (as a 1-D array), $V^T$ via `numpy.linalg.svd` with `full_matrices=True`.
3. **Rank-$r$ reconstruction** — for each target rank $r \in \{5, 25, 100\}$, slice $U_r$, $\Sigma_r$, $V_r^T$ and compute $A_r = U_r \Sigma_r V_r^T$; clip pixel values to $[0, 255]$.
4. **Image panels** — display the original and three reconstructions side by side using Matplotlib with a grey colormap; label each panel with its rank.
5. **Singular value plot** — plot $\sigma_i$ versus $i$ on a semi-logarithmic scale to visualise spectral decay.
6. **Energy plot** — compute the cumulative sum of $\sigma_i^2 / \|\boldsymbol{\sigma}\|^2$ and plot against rank $r$.

## Output

The script produces three figures:

- **Reconstruction comparison** — a row of four images: original, rank-5, rank-25, and rank-100 approximations, illustrating the progressive recovery of detail.
- **Singular value spectrum** — a log-scale plot of $\sigma_i$ versus index $i$, demonstrating the rapid decay that makes low-rank compression effective for natural images.
- **Cumulative energy** — a plot of $\mathcal{E}(r)$ versus $r$, showing the rank required to capture 90 %, 95 %, and 99 % of total image energy.
