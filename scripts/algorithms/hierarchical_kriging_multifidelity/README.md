# Hierarchical Kriging for Multi-Fidelity Data

This script fits a hierarchical kriging model to the one-dimensional Forrester test case, using a kriging model of 11 cheap low-fidelity samples as the trend of a kriging model of a few expensive high-fidelity samples, and compares it with ordinary kriging of the high-fidelity samples alone. In CFD the two fidelities could be a coarse and a fine mesh, or an Euler and a RANS solver; the question is how many expensive runs the cheap ones can replace.

## Overview

- Defines the high-fidelity function $f_h(x) = (6x - 2)^2 \sin(12x - 4)$ and the low-fidelity function $f_l(x) = A f_h(x) + B(x - 0.5) - C$ with $A = 0.5$, $B = 10$, $C = -5$ on $[0, 1]$.
- Fits ordinary kriging with a Gaussian correlation to 11 equally spaced low-fidelity samples.
- Fits hierarchical kriging (HK) to the high-fidelity samples with the low-fidelity predictor as the trend, and ordinary kriging to the same high-fidelity samples for comparison. The correlation parameter $\theta$ of every model is found by maximizing the concentrated log-likelihood.
- Plots both predictions with $\pm 2\hat{s}$ bands for the four-point design $x = 0, 0.4, 0.6, 1$ of Forrester, Sóbester and Keane (2007).
- Repeats the comparison for 3 to 12 high-fidelity samples drawn by random 1D Latin hypercube sampling, 20 designs per size, and plots the median and quartiles of the test RMSE on 501 points.

## Mathematical Background

### Model

Hierarchical kriging (Han and Görtz, 2012) models the high-fidelity response as

```math
y_h(x) = \beta_0\,\hat{y}_l(x) + Z(x)
```

where $\hat{y}_l$ is the kriging predictor of the low-fidelity data, $\beta_0$ is an unknown scaling factor and $Z$ is a zero-mean Gaussian process with variance $\sigma^2$ and correlation $R(x, x') = \exp(-\theta (x - x')^2)$. Ordinary kriging is the special case in which the trend is the constant 1 instead of $\hat{y}_l$.

### Predictor and Mean Squared Error

With $n$ high-fidelity samples $\mathbf{y}$, correlation matrix $R$, trend vector $\mathbf{F} = (\hat{y}_l(x_1), \dots, \hat{y}_l(x_n))^T$ and correlation vector $\mathbf{r}(x)$,

```math
\beta_0 = \frac{\mathbf{F}^T R^{-1}\mathbf{y}}{\mathbf{F}^T R^{-1}\mathbf{F}},
\qquad
\hat{y}_h(x) = \beta_0\,\hat{y}_l(x) + \mathbf{r}(x)^T R^{-1}(\mathbf{y} - \beta_0\mathbf{F})
```

```math
\hat{s}^2(x) = \sigma^2\left[1 - \mathbf{r}^T R^{-1}\mathbf{r} + \frac{\left(\mathbf{F}^T R^{-1}\mathbf{r} - \hat{y}_l(x)\right)^2}{\mathbf{F}^T R^{-1}\mathbf{F}}\right],
\qquad
\sigma^2 = \frac{(\mathbf{y} - \beta_0\mathbf{F})^T R^{-1}(\mathbf{y} - \beta_0\mathbf{F})}{n}
```

### Hyperparameter

The concentrated log-likelihood $\ln L(\theta) = -\frac{n}{2}\ln\sigma^2(\theta) - \frac{1}{2}\ln\det R(\theta)$ is maximized over $\log_{10}\theta \in [-2, 3]$.

For this test case $f_h - 2 f_l = -20x$, so with a perfect low-fidelity model the correction $Z$ would be linear with $\beta_0 = 1/A = 2$. Linear functions have an infinite length scale, so the likelihood drives $\theta$ to the lower bound.

## Implementation

- `f_high(x)` and `f_low(x)` define the two fidelities with the constants `A`, `B` and `C`.
- `Kriging(x, y, trend=None, theta=None, nugget=NUGGET)` is the model: `trend=None` gives ordinary kriging and a callable gives hierarchical kriging. `fit_theta` runs a 41-point grid search in $\log_{10}\theta$ followed by `scipy.optimize.minimize_scalar`, `concentrated_log_likelihood` evaluates $\ln L$, and `predict(x_new, return_mse=True)` returns $\hat{y}$ and $\hat{s}^2$. Linear systems are solved with a Cholesky factor of $R + 10^{-10} I$.
- `fit_models(x_lf, x_hf)` returns the high-fidelity-only, low-fidelity and hierarchical models.
- `rmse_study(x_lf, x_test)` loops over `N_HF_RANGE` and `N_SEEDS` designs from `latin_hypercube_1d` and returns the quartiles of the test RMSE.
- `make_figure` draws the three panels.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Ordinary kriging and hierarchical kriging of the Forrester function, and test RMSE against the number of high-fidelity samples](hierarchical_kriging_multifidelity.png)

With four high-fidelity samples, ordinary kriging cannot know about the minimum near $x = 0.76$: its RMSE is 5.62, and the true function leaves the $\pm 2\hat{s}$ band there, because the band only reflects the estimated $\theta = 11.6$, not the unseen dip. Hierarchical kriging with the same four samples follows the truth with RMSE 0.059 and $\beta_0 = 1.993$. The low-fidelity kriging model has RMSE 0.028 against $f_l$, and this error scaled by $\beta_0$ is the floor that the hierarchical model cannot go below.

The right panel shows the median RMSE over 20 random designs:

| HF samples | 3 | 4 | 6 | 8 | 10 | 12 |
| --- | --- | --- | --- | --- | --- | --- |
| Kriging, HF only | 4.96 | 4.68 | 2.66 | 1.13 | 0.198 | 0.088 |
| Hierarchical kriging | 4.98 | 0.064 | 0.055 | 0.054 | 0.047 | 0.042 |

With three samples neither model can estimate $\theta$ and $\beta_0$ reliably. From four samples on, hierarchical kriging is one to two orders of magnitude more accurate, and ordinary kriging needs about twelve expensive samples to approach the same error.

## Related Notes

- [Hierarchical Kriging](../../../notes/numerical/surrogates/hierarchical_kriging.md)
- [Kriging](../../../notes/numerical/surrogates/kriging.md)
- [Optimization with CFD and Machine Learning](../../../notes/machine_learning/flow/optimization.md)
