# Surrogate Models in CFD

A converged RANS solution of a car or a wing costs hours to days of CPU time, and a design study, an uncertainty analysis or a sensitivity analysis needs hundreds to millions of evaluations of the same output. A surrogate model (or metamodel, or response surface) replaces the solver by a cheap function fitted to a few dozen or a few hundred solver runs. This note states the approximation problem, compares the main families of surrogates, describes the workflow from sampling to validation, and explains why the number of design variables limits all of them.

The surrogate sits outside the CFD solver: it maps input parameters (geometry, operating conditions) to a scalar or vector output and knows nothing about the Navier–Stokes equations. Reduced-order models, which project the discretized equations themselves onto a low-dimensional basis, are covered in the [ROM notes](../rom/rom.md) and [POD notes](../pod/pod_intro.md).

## Problem Statement

Let $x \in \Omega \subset \mathbb{R}^d$ be a vector of $d$ input parameters, for example shape parameters of an airfoil, a Reynolds number and an angle of attack, each scaled to $[0, 1]$ so that $\Omega = [0, 1]^d$. A CFD run at $x$ returns an output of interest

$$
y = f(x)
$$

such as a drag coefficient $C_D$, a pressure drop $\Delta p$ or a heat-transfer coefficient. The function $f$ has no closed form; each evaluation means meshing, solving and post-processing, at a cost $c$ of minutes to days. Given a budget of $N$ runs, choose sample points $x^{(1)}, \dots, x^{(N)}$, evaluate $y^{(i)} = f(x^{(i)})$, and build a function $\hat{y}(x)$ that is cheap to evaluate and close to $f$ everywhere in $\Omega$, not just at the samples. Closeness is usually measured by the root-mean-square error over the domain,

```math
\varepsilon_{\mathrm{RMS}} = \left(\frac{1}{|\Omega|}\int_\Omega \left(\hat{y}(x) - f(x)\right)^2 dx\right)^{1/2}
```

estimated on test points that were not used for fitting. The surrogate is good enough when this error is small compared with the variation of $f$ over $\Omega$ and with the accuracy the application needs, for example one drag count ($\Delta C_D = 10^{-4}$) in a shape optimization.

Three things make the problem hard. The budget is small, typically $N \approx 10d$ to $50d$, so accuracy per sample is what matters. The output carries numerical noise from incomplete iterative convergence and from remeshing, so an exact interpolant may chase noise (see [Iterative Convergence](../cfd/iterative_convergence.md)). And $f$ may change character inside $\Omega$, for example where a flow separates or a shock forms, which no smooth global model captures with few samples.

## Families of Surrogate Models

| Family | Form of $\hat{y}(x)$ | Fitted by | Interpolates the data | Error estimate | Typical use |
| --- | --- | --- | --- | --- | --- |
| Polynomial response surface | $\sum_k \beta_k p_k(x)$, usually degree 1 or 2 | Least squares | No | Regression statistics | Small $d$, smooth trends, screening |
| Radial basis functions | $\sum_i w_i \varphi(\lVert x - x^{(i)} \rVert)$ plus a low-degree polynomial | One linear solve | Yes (or smoothed) | Cross-validation only | Scattered data in moderate $d$ |
| Kriging / Gaussian process | Trend plus a Gaussian process conditioned on the data | Linear solve plus likelihood maximization | Yes (no nugget) | Predictive variance $\hat{s}^2(x)$ | Expensive black boxes, adaptive sampling, optimization |
| Polynomial chaos, sparse grids | Orthogonal polynomials in the inputs, or hierarchical interpolation on a sparse grid | Projection, regression or interpolation on structured points | Depends on the method | Coefficient decay | Uncertainty propagation with known input distributions |
| Neural networks | Compositions of affine maps and nonlinearities | Gradient descent on a loss | No | Ensembles or Bayesian variants | Large data sets, field outputs on meshes |

The polynomial response surface of degree 2,

```math
\hat{y}(x) = \beta_0 + \sum_{k=1}^{d}\beta_k x_k + \sum_{k=1}^{d}\sum_{l=k}^{d}\beta_{kl}\,x_k x_l
```

has $(d + 1)(d + 2)/2$ coefficients and needs at least that many samples. It cannot represent more than one extremum along a line, and that is why it is used for screening and local models rather than global ones.

Radial basis functions ([Radial Basis Functions](radial_basis_functions.md)) and kriging ([Kriging](kriging.md)) are both weighted sums of functions centred at the samples, and both interpolate. Kriging derives the weights from a statistical model and therefore also returns the predictive variance that adaptive sampling and Bayesian optimization need. Polynomial chaos expansions (Xiu and Karniadakis, 2002) and sparse grids (Bungartz and Griebel, 2004) are built for uncertainty quantification, where the inputs have known probability distributions and the moments of the output are the goal. Neural-network surrogates and their training are covered in the machine-learning notes, for example [Neural Networks](../../machine_learning/fundamentals/neural_networks.md) and [Training and Validation](../../machine_learning/fundamentals/training_and_validation.md); they pay off when the data set is large or the output is a whole field.

## Workflow

1. Define the inputs, their ranges and the outputs. Scale every input to $[0, 1]$, so that distances, correlation lengths and kernel widths are comparable between variables, and drop inputs that a screening study shows to have little effect.
2. Choose the sampling plan. A space-filling design such as a maximin Latin hypercube or a scrambled Sobol sequence spreads $N_0$ points over $\Omega$ before any run is made ([One-Stage Sampling](one_stage_sampling.md)).
3. Run the CFD cases with the same mesh family, numerical settings and convergence criteria, so that differences between runs come from the inputs and not from the numerics. Record failed or unconverged runs instead of silently dropping them.
4. Fit the surrogate: least squares for polynomials, one linear solve for RBFs, maximum likelihood plus a linear solve for kriging, gradient descent for networks.
5. Validate it on data not used for fitting (next section). If the error is too large, add samples where the model is least reliable ([Adaptive Sampling](adaptive_sampling.md)), change the model, or remove an input.
6. Use the surrogate for its purpose, and confirm the final answer (an optimum, a failure probability) with a CFD run, because the surrogate is least accurate exactly where an optimizer pushes it.

When a cheaper model of the same flow exists (a coarser mesh, an Euler or panel code), step 3 can mix fidelities: many cheap runs fix the shape of the response and a few expensive ones correct it ([Hierarchical Kriging](hierarchical_kriging.md)).

## Validation

Training error says nothing for an interpolating surrogate, which is exact at every sample. Three estimates of the prediction error are in use:

- A hold-out test set, ideally its own space-filling design. It is unbiased but spends CFD runs that the model cannot learn from.
- $k$-fold cross-validation, which refits the model $k$ times, each time without one fold, and pools the errors on the left-out folds. The general procedure and the usual metrics (RMSE, MAE, $R^2$) are in [Training and Validation](../../machine_learning/fundamentals/training_and_validation.md).
- Leave-one-out cross-validation (LOO-CV), the case $k = N$, with residuals $`e_i = y^{(i)} - \hat{y}_{-i}(x^{(i)})`$, where $`\hat{y}_{-i}`$ is the model built without sample $i$.

For interpolants that are linear in the data, LOO-CV needs no refitting. For an RBF interpolant with system $A\mathbf{c} = \mathbf{y}$, Rippa (1999) showed that

```math
e_i = \frac{c_i}{(A^{-1})_{ii}}
```

and the same formula holds for the smoothed system $(A + \lambda I)\mathbf{c} = \mathbf{y}$. For kriging with fixed correlation parameters, or an RBF with a polynomial tail, the bordered matrix $M$ of the system (the correlation or kernel matrix bordered by the trend or polynomial matrix, as in [Kriging](kriging.md)) takes the place of $A$:

```math
e_i = \frac{\left[M^{-1}\begin{pmatrix}\mathbf{y} \\ \mathbf{0}\end{pmatrix}\right]_i}{(M^{-1})_{ii}},
\qquad i = 1, \dots, N
```

Both formulas give all $N$ residuals for the cost of one factorization and are checked against brute-force refitting in the tests of this repository. Two summaries are common: the LOO-CV RMS error $\left(\sum_i e_i^2/N\right)^{1/2}$, and for kriging the standardized residuals $e_i/\hat{s}_{-i}(x^{(i)})$, which should mostly lie in $[-3, 3]$ if the model's error estimate is to be trusted (Jones, Schonlau and Welch, 1998). LOO-CV is slightly pessimistic, because each model sees $N - 1$ samples, and it is inflated near the boundary of $\Omega$, where leaving out a point turns interpolation into extrapolation.

## Uses

- Optimization. A surrogate-based optimizer fits the model, finds the point that minimizes the prediction or maximizes an infill criterion such as expected improvement, runs CFD there and refits. With a Gaussian process this is efficient global optimization (EGO) or Bayesian optimization; see [Optimization with CFD and Machine Learning](../../machine_learning/flow/optimization.md) for the acquisition functions and a worked example.
- Uncertainty quantification. If the inputs are random (inflow angle, roughness, manufacturing tolerances), Monte Carlo sampling of the surrogate gives the mean, variance and quantiles of the output, or a failure probability $P(f(x) > y_{\mathrm{lim}})$, with $10^5$ or more samples at negligible cost.
- Sensitivity analysis. Variance-based Sobol indices, which need many thousands of evaluations, are computed on the surrogate and rank the inputs by their contribution to the output variance (Saltelli et al., 2008). The [Sobol Sensitivity Analysis](../../../scripts/algorithms/sobol_sensitivity_analysis/) script estimates them with the Saltelli scheme.
- Inverse problems and calibration. Fitting model constants or boundary conditions to measurements needs repeated forward evaluations, which the surrogate supplies.

## The Curse of Dimensionality

If $N$ points are spread evenly over $[0, 1]^d$, each one represents a cube of side

```math
\ell = N^{-1/d}
```

With $N = 100$, $\ell = 0.1$ in two dimensions, $0.22$ in three and $0.63$ in ten: in ten dimensions every sample stands for nearly two thirds of the range of every variable. The required $N$ grows exponentially with $d$ at fixed resolution, a full factorial with $L$ levels needs $L^d$ points, and the quadratic response surface needs $(d + 1)(d + 2)/2$ coefficients. Kriging adds one correlation parameter per input, so the likelihood landscape becomes harder to optimize as $d$ grows.

Surrogates work in practice at $d \approx 10$–$`20`$ because most CFD responses are dominated by a few inputs and by low-order interactions. The usual remedies exploit this: screen the inputs first (fractional factorials, Morris elementary effects, Sobol indices), reduce the geometry parametrization (for example by principal components of a shape family), and choose models that degrade gracefully, such as kriging with separate length scales per input, which effectively switches off unimportant directions.

## Key Takeaways

- A surrogate approximates the map from a few scaled inputs to a CFD output from $N$ expensive samples; accuracy per sample is the figure of merit.
- Polynomials suit screening and smooth local trends, RBFs and kriging suit scattered data in moderate dimension, and only kriging provides a built-in error estimate.
- Interpolating surrogates must be validated on unseen data; LOO-CV residuals of RBF and kriging models follow from one matrix inverse.
- Numerical noise in the CFD outputs argues for a smoothing parameter or nugget rather than exact interpolation.
- The sample density $N^{-1/d}$ is what limits every method; reduce $d$ before adding samples.

## Related Scripts

- [Correlation Functions](../../../scripts/algorithms/correlation_functions/): plots six correlation functions used in kriging surrogate models (linear, exponential, Matérn 3/2, Matérn 5/2, cubic spline and Gaussian) for several values of the correlation parameter $\theta$.
- [Kriging Interpolation](../../../scripts/algorithms/kriging_interpolation/): builds an ordinary kriging model of the Forrester function from nine samples with a compactly supported cubic correlation, estimates $\theta$ by maximum likelihood and compares the predictor and its uncertainty band for three values of $\theta$.
- [Radial Basis Functions](../../../scripts/algorithms/radial_basis_functions/): interpolates eight samples of the Forrester function with six RBF kernels written in numpy and plots the interpolants and their pointwise errors.
- [RBF Shape Parameter Trade-Off](../../../scripts/plots/rbf_shape_parameter_tradeoff/): sweeps the shape parameter of Gaussian and multiquadric RBF interpolants of Franke's function and plots the true error, Rippa's LOOCV estimate and the condition number of the interpolation matrix.
- [Design Space Distribution via Sobol Sequences](../../../scripts/plots/design_space_distribution/): draws a four-dimensional scrambled Sobol design of 512 geometry variants and shows all of its 2D projections and 1D marginals in a scatter matrix, with the discrepancy of each projection compared against a random design of the same size.
- [Sobol Sensitivity Analysis](../../../scripts/algorithms/sobol_sensitivity_analysis/): estimates first-order and total Sobol sensitivity indices of a synthetic five-parameter drag model with the Saltelli sampling scheme and checks them against the exact values.

## Exercises

**Exercise 1.** An airfoil study has $d = 5$ shape parameters, and one RANS run costs 4 CPU-hours. How many runs, and CPU-hours, does a full factorial design with 3 levels per parameter need? With 5 levels? Compare with a Latin hypercube plan of $N = 50$ runs.

<details>
<summary>Answer</summary>

3 levels: $3^5 = 243$ runs, i.e. 972 CPU-hours. 5 levels: $5^5 = 3125$ runs, i.e. 12500 CPU-hours. The LHS plan needs 50 runs, i.e. 200 CPU-hours. Its cost does not grow exponentially with $d$.

</details>

**Exercise 2.** A full quadratic response surface in $d$ variables has $(d + 1)(d + 2)/2$ coefficients. How many are needed for $d = 5$, $10$ and $20$? Can a 50-sample data set support a quadratic fit for $d = 10$?

<details>
<summary>Answer</summary>

$d = 5$: 21 coefficients. $d = 10$: 66. $d = 20$: 231. With $N = 50 < 66$ samples, the least-squares problem for $d = 10$ is underdetermined, so a full quadratic cannot be fitted; a reduced polynomial, kriging or an RBF model is needed instead.

</details>

**Exercise 3.** A hold-out set of five CFD results has $y = (0.80, 0.95, 1.10, 1.22, 1.30)$, and the surrogate predicts $\hat{y} = (0.82, 0.93, 1.12, 1.18, 1.31)$. Compute RMSE, MAE and $R^2 = 1 - \sum(y - \hat{y})^2 / \sum(y - \bar{y})^2$.

<details>
<summary>Answer</summary>

The errors are $(0.02, -0.02, 0.02, -0.04, 0.01)$, and their squares sum to $0.0029$.

- RMSE $= \sqrt{0.0029/5} = 0.0241$.
- MAE $= 0.11/5 = 0.022$.
- $\bar{y} = 1.074$ and $\sum(y - \bar{y})^2 = 0.16352$, so $R^2 = 1 - 0.0029/0.16352 = 0.982$.

</details>

**Exercise 4.** Fit (a) a linear and (b) a quadratic polynomial response surface by least squares to the data $x = (0, 1, 2, 3)$, $y = (1, 3, 7, 13)$. Report the coefficients and residuals, and explain why a low training error alone does not validate a surrogate.

<details>
<summary>Answer</summary>

(a) $\bar{x} = 1.5$ and $\bar{y} = 6$; $S_{xy} = 20$ and $S_{xx} = 5$. The slope is 4 and the intercept is $6 - 4 \times 1.5 = 0$, so $\hat{y} = 4x$. The residuals are $(1, -1, -1, 1)$ and the sum of squared errors is 4.

(b) The quadratic fit reproduces the data exactly: $\hat{y} = 1 + x + x^2$, with zero residuals.

Training error measures only the fit at the samples. A model with as many coefficients as data points always fits exactly, even if it behaves badly between or beyond them. Hold-out or cross-validation errors (Exercise 3) are needed to judge predictive accuracy.

</details>

**Exercise 5.** A Gaussian RBF $\varphi(r) = e^{-r^2}$ interpolates $(0, 1)$ and $(1, 2)$. The weights are $\mathbf{c} = (0.3056, 1.8876)$. Compute both LOO-CV residuals with Rippa's formula and check them by refitting.

<details>
<summary>Answer</summary>

$`A = \begin{pmatrix} 1 & e^{-1} \\ e^{-1} & 1 \end{pmatrix}`$, so $`(A^{-1})_{11} = (A^{-1})_{22} = 1/(1 - e^{-2}) = 1.1565`$. Rippa's formula gives $e_1 = 0.3056/1.1565 = 0.2642$ and $e_2 = 1.8876/1.1565 = 1.6321$.

Refitting without the first point gives $s(x) = 2e^{-(x - 1)^2}$, so $s(0) = 2e^{-1} = 0.7358$ and $e_1 = 1 - 0.7358 = 0.2642$. Without the second point, $s(x) = e^{-x^2}$, $s(1) = 0.3679$ and $e_2 = 2 - 0.3679 = 1.6321$. The second residual is larger because the decaying Gaussian, left with one point, falls toward zero instead of following the trend: an RBF without a polynomial tail extrapolates poorly.

</details>

## References

- J. Sacks, W. J. Welch, T. J. Mitchell and H. P. Wynn, "Design and analysis of computer experiments", *Statistical Science* 4(4), 409–423, 1989.
- A. I. J. Forrester, A. Sóbester and A. J. Keane, *Engineering Design via Surrogate Modelling: A Practical Guide*, Wiley, 2008.
- N. V. Queipo, R. T. Haftka, W. Shyy, T. Goel, R. Vaidyanathan and P. K. Tucker, "Surrogate-based analysis and optimization", *Progress in Aerospace Sciences* 41(1), 1–28, 2005.
- T. W. Simpson, J. D. Peplinski, P. N. Koch and J. K. Allen, "Metamodels for computer-based engineering design: survey and recommendations", *Engineering with Computers* 17(2), 129–150, 2001.
- A. I. J. Forrester and A. J. Keane, "Recent advances in surrogate-based optimization", *Progress in Aerospace Sciences* 45(1–3), 50–79, 2009.
- D. R. Jones, M. Schonlau and W. J. Welch, "Efficient global optimization of expensive black-box functions", *Journal of Global Optimization* 13(4), 455–492, 1998.
- S. Rippa, "An algorithm for selecting a good value for the parameter c in radial basis function interpolation", *Advances in Computational Mathematics* 11(2–3), 193–210, 1999.
- D. Xiu and G. E. Karniadakis, "The Wiener–Askey polynomial chaos for stochastic differential equations", *SIAM Journal on Scientific Computing* 24(2), 619–644, 2002.
- H.-J. Bungartz and M. Griebel, "Sparse grids", *Acta Numerica* 13, 147–269, 2004.
- A. Saltelli, M. Ratto, T. Andres, F. Campolongo, J. Cariboni, D. Gatelli, M. Saisana and S. Tarantola, *Global Sensitivity Analysis: The Primer*, Wiley, 2008.
