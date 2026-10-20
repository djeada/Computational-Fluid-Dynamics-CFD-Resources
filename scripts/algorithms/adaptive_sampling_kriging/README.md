# Adaptive Sampling with Kriging

This script grows a kriging surrogate of a two-dimensional test function from an 8-point Latin hypercube to 40 samples by adding one point at a time, once by maximizing the kriging mean squared error and once by maximizing a leave-one-out cross-validation error indicator times the kriging standard deviation, and compares both with one-shot maximin Latin hypercubes of the same size. The test function has a narrow peak in one corner, the kind of local feature (a separation onset, a shock moving onto a surface) that makes some regions of a CFD design space harder to model than others.

## Overview

- The test function on $[0, 1]^2$ is $`y(x) = \exp\left(-\|x - (0.8, 0.75)\|^2/0.01\right) + 0.2\sin(2\pi x_1)\cos(\pi x_2)`$.
- Every surrogate is ordinary kriging with an anisotropic Gaussian correlation, refitted by maximum likelihood after each new sample.
- Each sequential run starts from an 8-point maximin Latin hypercube (best of 20 random ones by minimum distance) and stops at 40 points. New points are chosen on a $31 \times 31$ candidate grid.
- The max-MSE criterion picks $\arg\max \hat{s}^2(x)$. The cross-validation criterion picks $`\arg\max e(x)\,\hat{s}(x)`$, where $e(x)$ is the mean change of the prediction at $x$ when one sample is left out.
- The reference is an independent maximin Latin hypercube for each size from 8 to 40.
- The error is the RMS error on a $50 \times 50$ test grid divided by the standard deviation of $y$ on that grid, averaged over 5 initial designs.

## Mathematical Background

### Kriging Model

Ordinary kriging models $y(x) = \beta + Z(x)$ with a Gaussian process $Z$ of variance $\sigma^2$ and correlation $R(x, x') = \exp\left(-\sum_k \theta_k (x_k - x'_k)^2\right)$. With $n$ samples, correlation matrix $R$ and correlation vector $\mathbf{r}(x)$,

```math
\hat{y}(x) = \hat\beta + \mathbf{r}^T R^{-1}(\mathbf{y} - \hat\beta\mathbf{1}),
\qquad
\hat{s}^2(x) = \sigma^2\left[1 - \mathbf{r}^T R^{-1}\mathbf{r} + \frac{(1 - \mathbf{1}^T R^{-1}\mathbf{r})^2}{\mathbf{1}^T R^{-1}\mathbf{1}}\right]
```

and the $\theta_k$ maximize the concentrated log-likelihood $-\frac{n}{2}\ln\hat\sigma^2 - \frac{1}{2}\ln\det R$.

### Infill Criteria

The max-MSE criterion depends only on the sample locations and $\theta$, not on the sampled values, so it is a space-filling rule shaped by the fitted length scales. The cross-validation indicator

```math
e(x) = \frac{1}{n}\sum_{i=1}^{n}\left|\hat{y}_{-i}(x) - \hat{y}(x)\right|
```

uses the data: $\hat{y}_{-i}$ is the model refitted without sample $i$ (here with $\theta$ held fixed), so $e$ is large where the prediction depends strongly on individual samples. Because $e$ does not vanish at the samples, it is multiplied by $\hat{s}(x)$, which does.

## Implementation

- `test_function(x)` evaluates the test function for points in rows of `x`.
- `latin_hypercube(n, d, rng)` and `maximin_lhs(n, d, rng)` build the designs; `min_distance` is the maximin score.
- `OrdinaryKriging(x, y, theta=None, theta_start=None)` fits the model. `fit_theta` runs L-BFGS-B in $\log_{10}\theta$ from several starts (from the previous $\theta$ and one fixed start during a sequential run), and `predict(x_new, return_mse=True)` returns $\hat{y}$ and $\hat{s}^2$.
- `loo_error_indicator` and `infill_score` implement the two criteria.
- `adaptive_run` and `one_shot_run` produce the error histories, and `run_study` loops over `N_SEEDS` initial designs.
- `N_INITIAL`, `N_FINAL`, `N_SEEDS`, `N_CANDIDATES_1D` and `N_TEST_1D` set the study size.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Final 40-point designs of max-MSE, LOO-CV and one-shot maximin LHS sampling, and the surrogate error against the number of samples](adaptive_sampling_kriging.png)

The max-MSE design (top left) puts 25 of its 32 added points on the edges of the square, where the kriging variance is largest because each boundary point has neighbours on one side only, and has only two points within 0.15 of the peak centre. The cross-validation design (top middle) puts 6 points within that radius and most of the others in the ring around the peak and in the right half of the square, where leaving out a sample changes the prediction most. The designs shown are those of the first initial design. The bottom panel gives the mean normalized error:

| $N$ | 8 | 16 | 24 | 32 | 40 |
| --- | --- | --- | --- | --- | --- |
| max MSE | 0.859 | 0.845 | 0.791 | 0.646 | 0.672 |
| LOO-CV $\times \hat{s}$ | 0.859 | 0.654 | 0.596 | 0.446 | 0.343 |
| one-shot maximin LHS | 1.091 | 0.685 | 0.538 | 0.477 | 0.437 |

The two sequential runs share their initial designs, so they start from the same error. For this function, exploration alone is no better than a one-shot design of the same size, and the data-driven criterion ends with about 20% less error than the one-shot design. The errors are still large in absolute terms because a stationary Gaussian process with one length scale per direction has to describe both the narrow peak and the smooth background.

## Related Notes

- [Adaptive Sampling](../../../notes/numerical/surrogates/adaptive_sampling.md)
- [One-Stage Sampling](../../../notes/numerical/surrogates/one_stage_sampling.md)
- [Kriging](../../../notes/numerical/surrogates/kriging.md)
