# Bayesian Optimization

This script minimizes a one-dimensional drag-like test function and the two-dimensional Branin function by Bayesian optimization: a Gaussian-process (GP) surrogate with a squared-exponential kernel, hyperparameters fitted by maximum marginal likelihood, and the expected-improvement (EI) acquisition function of the EGO algorithm. It draws the surrogate and EI after several iterations and compares the best value found against random search over ten seeds, the situation of a design study in which each evaluation is a CFD run.

## Overview

- Uses $`J(p) = 0.30 + 0.005\,(6p - 2)^2 \sin(12p - 4)`$ on $[0, 1]$, a scaled Forrester function with a global minimum $J^* = 0.26990$ at $p = 0.75725$ and a local minimum 0.29507 at $p = 0.14259$, as a stand-in for a drag coefficient against one shape parameter.
- Uses the Branin function on $[0, 1]^2$ (minimum 0.397887, reached at three points) as a two-parameter problem.
- Starts from a Latin hypercube design of 3 points in 1D and 5 points in 2D, then adds one point per iteration up to 15 and 30 evaluations.
- At every iteration fits the GP by maximizing the log marginal likelihood over the length scales and the amplitude (L-BFGS-B with an analytic gradient, three starts), then evaluates the objective where EI is largest on a grid of 1001 points in 1D or $101 \times 101$ points in 2D.
- Repeats both problems for ten seeds and records the best-so-far gap $J_{best} - J^*$ for Bayesian optimization and for uniform random search with the same budget.

## Mathematical Background

### Gaussian-Process Surrogate

The observations are standardized to $z_i = (J_i - \bar J)/s_J$ and modelled as a zero-mean GP with an automatic-relevance-determination squared-exponential kernel:

```math
k(\mathbf{p}, \mathbf{p}') = \sigma_f^2 \exp\left(-\frac{1}{2}\sum_{j=1}^{d} \frac{(p_j - p_j')^2}{\ell_j^2}\right),
\qquad K_{ij} = k(\mathbf{p}_i, \mathbf{p}_j) + \sigma_n^2 \delta_{ij}
```

with a fixed nugget $\sigma_n^2 = 10^{-6}$. At a new point, with $\mathbf{k}_*$ the vector of kernel values against the samples,

```math
\mu(\mathbf{p}) = \mathbf{k}_*^T K^{-1}\mathbf{z},
\qquad \sigma^2(\mathbf{p}) = \sigma_f^2 - \mathbf{k}_*^T K^{-1}\mathbf{k}_*
```

which are mapped back to the units of $J$ with $\bar J$ and $s_J$.

### Hyperparameters

With $\boldsymbol{\alpha} = K^{-1}\mathbf{z}$, the log marginal likelihood and its gradient with respect to $`\theta_j \in \{\log\ell_1, \dots, \log\ell_d, \log\sigma_f\}`$ are

```math
\log p(\mathbf{z}\mid\boldsymbol\theta) = -\tfrac{1}{2}\mathbf{z}^T\boldsymbol\alpha - \tfrac{1}{2}\log|K| - \tfrac{n}{2}\log 2\pi,
\qquad \frac{\partial \log p}{\partial \theta_j} = \tfrac{1}{2}\mathrm{tr}\left[\left(\boldsymbol\alpha\boldsymbol\alpha^T - K^{-1}\right)\frac{\partial K}{\partial \theta_j}\right]
```

The bounds are $0.02 \le \ell_j \le 2$ and $0.1 \le \sigma_f \le 10$.

### Expected Improvement

For minimization with the current best value $J_{best}$, the improvement is $I = \max(J_{best} - J, 0)$ with $J \sim \mathcal{N}(\mu, \sigma^2)$. Its expectation has the closed form (Jones, Schonlau & Welch, 1998)

```math
\mathrm{EI}(\mathbf{p}) = (J_{best} - \mu)\,\Phi(z) + \sigma\,\phi(z),
\qquad z = \frac{J_{best} - \mu}{\sigma}
```

where $\Phi$ and $\phi$ are the standard normal CDF and PDF. The first term rewards a low predicted mean (exploitation) and the second a large uncertainty (exploration).

## Implementation

- `drag_like_1d(x)` and `branin_2d(x)` are the objectives, and `DRAG_1D_MIN` and `BRANIN_MIN` their minima.
- `se_kernel(a, b, lengths, amplitude)` evaluates the kernel matrix. `GaussianProcess` has `fit`, `predict`, `log_marginal_likelihood` and `log_marginal_likelihood_gradient`, and uses a Cholesky factorization of $K$.
- `fit_gp(x, y, rng)` maximizes the likelihood with `scipy.optimize.minimize`.
- `expected_improvement(mean, std, f_best, xi=0.0)` implements the formula above.
- `latin_hypercube`, `candidate_grid` and `bayesian_optimization(objective, dim, n_initial, budget, rng, record)` implement the loop. With `record=True` it stores the surrogate and EI of every iteration.
- `random_search` and `convergence` run the seed study. `plot_results` draws the figure.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![GP surrogate and expected improvement at three iterations, and convergence against random search in 1D and 2D](bayesian_optimization.png)

The top rows show the 1D run at iterations 0, 2 and 5 (3, 5 and 8 evaluations). With three samples the fitted length scale sits at its lower bound of 0.02. The GP mean then reverts to the sample mean between samples and EI is spread over the whole interval: maximum likelihood with very few points overfits. By iteration 2 two samples lie in the global basin, and EI peaks at the unexplored right edge and at the two gaps between samples on the left. By iteration 5 the surrogate matches the function closely and EI is a narrow spike at the minimum. The run reaches $J = 0.26990$ at $p = 0.7570$ and then keeps resampling that grid point, where EI is largest but tiny. A real study would stop once the largest EI falls below a tolerance.

The bottom row shows the median and quartiles over ten seeds. In 1D the median gap after 15 evaluations is $1.6 \times 10^{-7}$ for Bayesian optimization, the resolution of the 1001-point candidate grid, against $5.6 \times 10^{-3}$ for random search. In 2D, after 30 evaluations, it is $5.9 \times 10^{-3}$, the best value on the $101 \times 101$ grid, against 2.1 for random search. Maximizing EI with a continuous optimizer would remove this floor.

## Related Notes

- [Optimization for Flow Modeling](../../../notes/machine_learning/flow/optimization.md)
- [Kriging](../../../notes/numerical/surrogates/kriging.md)
- [Adaptive Sampling](../../../notes/numerical/surrogates/adaptive_sampling.md)
