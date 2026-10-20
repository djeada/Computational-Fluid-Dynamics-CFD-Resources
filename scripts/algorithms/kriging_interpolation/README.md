# Kriging Interpolation

This script builds an ordinary kriging model of the Forrester function $y(x) = (6x-2)^2 \sin(12x-4)$ from nine equally spaced samples with a compactly supported cubic correlation function, estimates the correlation parameter $\theta$ by maximum likelihood, and compares the predictor and its $\pm 2\hat{s}$ band for $\theta$ below, at and above the estimate. It reproduces the worked example of the kriging note, so the numbers quoted there can be checked by running it.

## Overview

- Samples the test function at $x = 0, 0.125, \dots, 1$.
- Scans the concentrated log-likelihood of ordinary kriging (constant trend) over 1901 values $\theta \in [0.5, 10]$ and takes the maximizer $\theta^*$.
- Fits the model for $\theta = 1.75$, $\theta^*$ and $\theta = 5$, and evaluates the predictor and its mean squared error at 501 points.
- Prints $\ln L$, $\hat\beta$, $\hat\sigma^2$, the RMS error and the maximum error for each $\theta$.
- Draws the likelihood curve and the three predictions with their uncertainty bands.

## Mathematical Background

### Model and Predictor

Ordinary kriging writes $y(x) = \beta + z(x)$, with $z$ a zero-mean Gaussian process of variance $\sigma^2$ and correlation $R(h;\theta)$. With $R_{ij} = R(x_i - x_j)$, $r_i(x) = R(x - x_i)$ and $\mathbf{1}$ the vector of ones,

```math
\hat\beta = \frac{\mathbf{1}^T R^{-1}\mathbf{y}}{\mathbf{1}^T R^{-1}\mathbf{1}},
\qquad
\hat{y}(x) = \hat\beta + \mathbf{r}(x)^T R^{-1}(\mathbf{y} - \hat\beta\mathbf{1})
```

```math
\hat{s}^2(x) = \hat\sigma^2\left[1 - \mathbf{r}^T R^{-1}\mathbf{r} + \frac{(1 - \mathbf{1}^T R^{-1}\mathbf{r})^2}{\mathbf{1}^T R^{-1}\mathbf{1}}\right],
\qquad
\hat\sigma^2 = \frac{(\mathbf{y} - \hat\beta\mathbf{1})^T R^{-1}(\mathbf{y} - \hat\beta\mathbf{1})}{n}
```

### Concentrated Likelihood

Substituting $\hat\beta$ and $\hat\sigma^2$ into the Gaussian log-likelihood leaves a function of $\theta$ alone, up to a constant:

```math
\ln L(\theta) = -\frac{n}{2}\ln\hat\sigma^2(\theta) - \frac{1}{2}\ln\det R(\theta)
```

### Cubic Correlation

With $\xi = \theta|h|$,

```math
R(h;\theta) = \begin{cases} 1 - 6\xi^2 + 6\xi^3, & 0 \le \xi < 0.5, \\ 2(1 - \xi)^3, & 0.5 \le \xi < 1, \\ 0, & \xi \ge 1. \end{cases}
```

It is the cubic B-spline scaled to $R(0) = 1$, twice continuously differentiable, and zero beyond $|h| = 1/\theta$. The [Correlation Functions](../correlation_functions/) script plots the same function with support $2/\theta$, so its $\theta$ is twice the $\theta$ used here. Because the support grows as $\theta$ falls, the likelihood has kinks wherever $1/\theta$ crosses a multiple of the sample spacing 0.125.

## Implementation

- `test_function(x)` evaluates the Forrester function and `cubic_correlation(h, theta)` the correlation.
- `fit(x_data, y_data, theta)` returns a dictionary with $R$, $\hat\beta$, $\hat\sigma^2$, the weights $R^{-1}(\mathbf{y} - \hat\beta\mathbf{1})$ and $\ln L$.
- `maximum_likelihood_theta(x_data, y_data)` scans `THETA_GRID` and returns the maximizer.
- `predict(x_new, x_data, model)` returns $\hat{y}$ and $\hat{s}^2$.
- `plot_results(...)` draws the four panels. `N_SAMPLES`, `N_PREDICT`, `THETA_GRID` and `THETA_COMPARE` set the experiment.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Concentrated log-likelihood of the correlation parameter and kriging predictions of the Forrester function for theta = 1.75, 2.03 and 5](kriging_interpolation.png)

The script prints

| $\theta$ | $\ln L$ | $\hat\beta$ | $\hat\sigma^2$ | RMSE | max error |
| --- | --- | --- | --- | --- | --- |
| 1.75 | -13.61 | 4.85 | 88.50 | 0.657 | 1.842 |
| 2.025 | -12.50 | 3.87 | 53.74 | 0.282 | 0.943 |
| 5.00 | -15.38 | 1.72 | 30.82 | 0.470 | 1.393 |

The likelihood peaks at $\theta^* = 2.03$, where the correlation reaches three sample spacings (the support radius is 0.49). With $\theta = 1.75$ the correlation reaches further, the predictor overshoots between $x = 0.2$ and $0.5$, and the error doubles. With $\theta = 5$ each sample influences less than two spacings, the predictor sags toward $\hat\beta$ between samples, and the uncertainty band widens to about $\pm 7$ midway between samples. For $\theta \ge 8$ the support is shorter than the sample spacing, $R$ is the identity, and the likelihood is flat. Every predictor passes through the samples, where $\hat{s} = 0$.

## Related Notes

- [Kriging](../../../notes/numerical/surrogates/kriging.md)
- [Surrogate Models in CFD](../../../notes/numerical/surrogates/intro.md)
- [Radial Basis Functions](../../../notes/numerical/surrogates/radial_basis_functions.md)
