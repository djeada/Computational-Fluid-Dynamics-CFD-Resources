# Condition Number of the Correlation Matrix

This script investigates how the condition number of a spatial correlation matrix depends on the choice of correlation function and its length-scale parameter $\theta$. Large condition numbers signal near-singular matrices that cause numerical instability when solving the kriging or Gaussian-process linear systems, so understanding this relationship is essential for robust surrogate modelling in CFD workflows.

## Overview

- Constructs a $10 \times 10$ correlation matrix on a uniform grid in $[0, 1]$ for four classical correlation functions.
- Sweeps $\theta$ over three orders of magnitude using a logarithmic grid of 100 values.
- Computes the 2-norm condition number $\kappa(R)$ via NumPy's `linalg.cond` for each $(\text{function},\, \theta)$ pair.
- Renders a $2 \times 2$ subplot figure — one panel per correlation function — showing $\kappa$ versus $\theta$ on a log–log scale.
- Identifies the $\theta$ regime where each function transitions from well-conditioned to ill-conditioned.

## Mathematical Background

### Correlation Matrix

Given $n$ observation locations $x_1, \dots, x_n \in \mathbb{R}$, the symmetric positive-definite correlation matrix is

$$R_{ij} = R(|x_i - x_j|;\, \theta), \quad i,j = 1,\dots,n.$$

The parameter $\theta > 0$ controls the effective range of correlation: small $\theta$ produces long-range, nearly constant correlations; large $\theta$ produces short-range correlations.

### Condition Number

The 2-norm condition number of $R$ is

$$\kappa(R) = \frac{\sigma_{\max}(R)}{\sigma_{\min}(R)},$$

where $\sigma_{\max}$ and $\sigma_{\min}$ are the largest and smallest singular values (equivalently, eigenvalues, since $R$ is symmetric positive semi-definite). A matrix with $\kappa \gg 1$ is ill-conditioned: small perturbations in data can cause large errors in the solved weights.

### Linear Correlation Function

$$R(h;\,\theta) = \max\!\bigl(0,\; 1 - \theta|h|\bigr)$$

Compact support; becomes identically zero beyond $|h| = 1/\theta$.

### Exponential Correlation Function

$$R(h;\,\theta) = e^{-\theta|h|}$$

Infinitely supported; the correlation length is $1/\theta$.

### Gaussian Correlation Function

$$R(h;\,\theta) = e^{-\theta h^2}$$

Super-exponential decay; tends to produce the most ill-conditioned matrices for large $\theta$ due to rapid collapse to a near-rank-one structure.

### Cubic Spline Correlation Function

$$R(h;\,\theta) = \begin{cases} 1 - \tfrac{3}{2}|h|^2 + \tfrac{3}{4}|h|^3, & |h| \leq 1, \\ \tfrac{1}{4}(2-|h|)^3, & 1 < |h| \leq 2, \\ 0, & |h| > 2. \end{cases}$$

Twice continuously differentiable; compact support limits long-range fill-in and often yields better conditioning than smooth global kernels.

## Implementation

1. **Grid setup** — create 10 equally spaced points in $[0,1]$ and form the $10\times 10$ lag matrix $H_{ij} = x_i - x_j$.
2. **Parameter sweep** — generate 100 values of $\theta$ log-uniformly in $[10^{-2}, 10^{1}]$ using `numpy.logspace`.
3. **Matrix assembly** — for each correlation function and each $\theta$, evaluate $R_{ij} = R(H_{ij};\,\theta)$ using vectorised NumPy operations.
4. **Condition number** — call `numpy.linalg.cond(R)` to obtain $\kappa(R)$ for each matrix.
5. **Plotting** — arrange results in a $2 \times 2$ subplot grid; each panel plots $\theta$ on the $x$-axis and $\kappa$ on the $y$-axis, both on logarithmic scales, with labelled axes and a title identifying the correlation function.

## Output

The script displays a single figure with four panels:

- **Top-left**: $\kappa$ vs $\theta$ for the linear correlation function.
- **Top-right**: $\kappa$ vs $\theta$ for the exponential correlation function.
- **Bottom-left**: $\kappa$ vs $\theta$ for the Gaussian correlation function.
- **Bottom-right**: $\kappa$ vs $\theta$ for the cubic spline correlation function.

Each panel uses a log–log scale, allowing clear identification of the critical $\theta$ range beyond which the matrix becomes numerically singular.
