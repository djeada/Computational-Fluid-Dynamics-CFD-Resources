# Training and Validation

A model that reproduces its training data proves nothing; the question is how well it predicts cases it has not seen, and how much each prediction can be trusted. This note covers the protocol that answers that question for CFD surrogates: how to split data without leaking information, how to scale it, the bias-variance trade-off and the regularisers that control it, error metrics, cross-validation, hyperparameter search, uncertainty quantification, out-of-distribution detection, and what a credible report contains. The models themselves are described in [Neural Networks](neural_networks.md) and the [surrogate notes](../../numerical/surrogates/intro.md).

## Problem Statement

Let input-output pairs $(\mathbf{x}, \mathbf{y})$ follow a distribution $P$ that describes the intended use: the design space and operating conditions on which the model will be queried. For a model $f_{\boldsymbol\theta}$ trained on a dataset $`\mathcal{D} = \{(\mathbf{x}_i, \mathbf{y}_i)\}_{i=1}^N`$, the quantity of interest is the expected risk (generalisation error)

$$
\mathcal{R}(f_{\boldsymbol\theta}) = \mathbb{E}_{(\mathbf{x}, \mathbf{y}) \sim P}
\Big[\ell\big(f_{\boldsymbol\theta}(\mathbf{x}), \mathbf{y}\big) \Big]
$$

whereas training minimises the empirical risk on $\mathcal{D}$:

$$
\hat{\mathcal{R}}_{\mathcal{D}}(f_{\boldsymbol\theta}) = \frac{1}{N} \sum_{i=1}^{N}
\ell\big(f_{\boldsymbol\theta}(\mathbf{x}_i), \mathbf{y}_i\big)
$$

Because $\boldsymbol\theta$ was chosen to make $\hat{\mathcal{R}}_{\mathcal{D}}$ small, the training error is a biased, optimistic estimate of $\mathcal{R}$. The tasks are to choose the model and its hyperparameters to make $\mathcal{R}$ small, to estimate $\mathcal{R}$ without bias from data the model has never influenced, and to estimate the error of each individual prediction.

CFD data make this harder than in textbook settings. $N$ is small because each sample is a simulation. Samples are not independent: snapshots of one run, operating points of one geometry and mesh variants of one shape are strongly correlated. The distribution $P$ is set by an engineer's choice of design space, and queries during optimisation tend to drift to the edge of it.

## Data Splits

The data are divided into three disjoint parts:

| Set | Used for | Typical share |
| --- | --- | --- |
| Training | Fitting $\boldsymbol\theta$ | 60-80 % |
| Validation | Choosing hyperparameters, early stopping, model selection | 10-20 % |
| Test | One final, unbiased estimate of $\mathcal{R}$ | 10-20 % |

The test set is used once, after every decision is made. A test error that has been looked at and then acted on (by changing the architecture, say) has become a validation error and is optimistically biased. With fewer than a few hundred cases, cross-validation (below) replaces the fixed validation set.

A random split is valid only if samples are independent and identically distributed. CFD data usually are not, and a random split then leaks information from training to test.

Consecutive snapshots of an unsteady simulation are correlated over an integral time scale $T_I$. A random split puts the neighbours of every test snapshot into training, so the model only has to interpolate between nearly identical fields. Forecasting is tested by a blocked split in time: train on $t < t_1$, validate on $t_1 + \Delta < t < t_2$, and test on $t > t_2 + \Delta$, with a gap $\Delta$ of several $T_I$.

When the dataset contains several cases per geometry (yaw angles, ride heights, speeds, or mesh refinements of one car), a random split almost always puts siblings of each test case into training. The test error then measures interpolation between operating points of known shapes, not prediction for a new shape. A group split assigns all cases of one geometry to the same set; group k-fold applies the same rule to cross-validation. The same applies to fields: splitting the nodes of one simulation into training and test points says nothing about other simulations.

If the model will be used near the edge of the design space, also hold out a region (for example all cases with rear slant angle above $30^\circ$) and report the error there separately as an extrapolation test.

## Feature and Target Scaling

Each input feature $j$ is standardised with the training mean $\mu_j$ and standard deviation $s_j$,

$$
x'_j = \frac{x_j - \mu_j}{s_j}
$$

or mapped onto $[-1, 1]$ with the training minimum and maximum when bounds are known. Targets are scaled in the same way, and predictions are transformed back before computing errors in physical units. Quantities spanning decades ($Re$, $\nu_t$, wall shear stress near separation) are log-transformed first. Nondimensional groups are better features than dimensional ones because they combine variables that act together.

For fields, scale each variable ($u$, $v$, $p$, $k$) with one statistic over all nodes and training cases. Per-node scaling amplifies noise in the free stream, where the variance is almost zero. The statistics are computed on the training set only. Computing them on all data before splitting is a common, silent leak.

## Bias-Variance Decomposition

Suppose $y = f(\mathbf{x}) + \varepsilon$ with $\mathbb{E}[\varepsilon] = 0$ and $\mathrm{Var}(\varepsilon) = \sigma^2$, and let $\hat f_{\mathcal{D}}$ be the model trained on a random dataset $\mathcal{D}$. At a fixed input $\mathbf{x}$, the expected squared error over datasets and noise splits into three terms:

$$
\mathbb{E}_{\mathcal{D}, \varepsilon}\Big[\big(y - \hat
f_{\mathcal{D}}(\mathbf{x})\big)^2 \Big] = \underbrace{\sigma^2}_{\text{noise}} +
\underbrace{\Big(f(\mathbf{x}) - \mathbb{E}_{\mathcal{D}}\big[\hat f_{\mathcal{D}}(\mathbf{x})\big]\Big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}_{\mathcal{D}}\Big[\Big(\hat f_{\mathcal{D}}(\mathbf{x}) - \mathbb{E}_{\mathcal{D}}\big[\hat f_{\mathcal{D}}(\mathbf{x})\big]\Big)^2\Big]}_{\text{variance}}
$$

The proof adds and subtracts $`\mathbb{E}_{\mathcal{D}}[\hat f_{\mathcal{D}}]`$ and $f$; the cross terms vanish because $\varepsilon$ is independent of $\mathcal{D}$ and has zero mean. The noise term is the floor that no model can beat. For CFD data it includes the residual unsteadiness of averaged quantities and the scatter from incomplete convergence. Bias is the error of the average model and falls as the model becomes more flexible. Variance is the sensitivity to the particular sample and grows with flexibility.

For least squares with $p$ coefficients fitted to $N$ samples at fixed design points, the variance averaged over those points is exactly $\sigma^2 p / N$, the expected training MSE is $\sigma^2(1 - p/N) + \text{bias}^2$, and the expected error on new noise at the same points is $\sigma^2(1 + p/N) + \text{bias}^2$. The gap between training and test error therefore grows in proportion to $p/N$.

![Polynomial fits of degree 1, 7 and 15; training, validation and leave-one-out error against degree; and the Monte Carlo bias-variance split](../../../scripts/plots/bias_variance_tradeoff/bias_variance_tradeoff.png)

The figure fits Legendre polynomials of degree $d = 0, \dots, 15$ to 20 noisy samples ($\sigma = 0.2$). In the left panel, degree 1 misses the shape (high bias), degree 7 follows the true curve, and degree 15 passes close to every sample while oscillating between and beyond them. In the centre panel, the training error falls monotonically with $d$ (from 0.76 to 0.04), is below the noise level $\sigma = 0.2$ from $d = 5$ on, and is useless for model selection. The validation and leave-one-out curves are U-shaped, and leave-one-out cross-validation picks $d = 7$ using only the 20 training samples. In the right panel, averaging over 400 noise realisations shows bias² falling from 0.53 to 0.002 by $d = 7$ while the variance rises from 0.002 to 0.37, so their sum with $\sigma^2$ has its minimum at $d = 7$.

Very large networks can show a second descent of the test error beyond the point where they interpolate the training data (Belkin et al., 2019). The decomposition still holds there; the implicit regularisation of the optimiser keeps the variance in check. For the small datasets typical of CFD, the classical U-curve is the relevant picture.

## Underfitting and Overfitting

| Symptom | Diagnosis | Action |
| --- | --- | --- |
| Training and validation errors both high and close to each other | Underfitting (bias dominates) | Larger model, better features, longer training, check the scaling |
| Training error far below validation error | Overfitting (variance dominates) | More data, regularisation, smaller model, early stopping |
| Training error below the noise level $\sigma$ | The model fits noise | Same as overfitting |
| Both errors near $\sigma$ | Near the attainable limit | Stop; only better data help |
| Validation error below training error | Leaky or unrepresentative split, or regularisation active only during training (dropout) | Check the split and the evaluation mode |

A learning curve plots both errors against $N$. If the validation error is still falling at the full dataset size, more CFD runs will help. If both curves have flattened at a level above the target accuracy, the model class or the features are the limitation.

## Regularisation

Regularisation reduces variance at the price of some bias.

An L2 penalty adds $\lambda \lVert \boldsymbol\theta \rVert_2^2$ to the loss. For a linear model with design matrix $X$, the minimiser is ridge regression,

$$
\hat{\boldsymbol\theta} = \big(X^T X + \lambda I\big)^{-1} X^T \mathbf{y}
$$

which also fixes the ill-conditioning of $X^T X$. For networks the same penalty, with weight $\lambda/2$, is called weight decay because a gradient step becomes $\boldsymbol\theta \leftarrow (1 - \eta\lambda)\boldsymbol\theta - \eta \nabla \mathcal{L}_{\mathrm{data}}$. An L1 penalty $\lambda \lVert \boldsymbol\theta \rVert_1$ drives coefficients exactly to zero and is used for sparse models such as SINDy ([Flow Dynamics](../flow/flow_dynamics.md)).

Dropout (Srivastava et al., 2014) multiplies each hidden activation during training by an independent mask $m_i \sim \mathrm{Bernoulli}(1 - p)$ and rescales,

```math
\tilde a_i = \frac{m_i\, a_i}{1 - p}
```

so the expected activation is unchanged. At test time the mask is removed. Dropout stops units from relying on each other and acts like averaging many thinned networks.

Early stopping monitors the validation loss and keeps the parameters from the epoch at which it was lowest, stopping after a patience of several epochs without improvement. For linear least squares trained by gradient descent from zero, stopping after $k$ steps of size $\eta$ acts approximately like an L2 penalty with $\lambda \sim 1/(\eta k)$.

Data augmentation adds transformed copies of the training cases that are known to be valid solutions. For a car that is symmetric about its centre plane, the case at yaw angle $\beta$ mirrored in that plane is the case at $-\beta$, with the lateral velocity and side force reversed in sign. Mirroring the geometry of a symmetric channel, or rotating an isotropic turbulence field, are other examples. Where the symmetry is exact it is better built into the inputs or the architecture (for example invariant inputs in turbulence closures), but augmentation works with any model.

Physics-based penalties on the PDE residual ([PINNs](../neural_networks/pinns.md)), smaller architectures and ensembles are further ways to reduce variance.

## Error Metrics

For $N$ test cases with predictions $\hat y_i$, targets $y_i$ and mean target $\bar y$:

| Metric | Definition | Remarks |
| --- | --- | --- |
| Mean absolute error | $\mathrm{MAE} = \frac{1}{N}\sum_i \lvert \hat y_i - y_i \rvert$ | Same units as $y$; less sensitive to outliers |
| Root-mean-square error | $\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_i (\hat y_i - y_i)^2}$ | Penalises large errors; compare with $\sigma$ and with the CFD discretisation error |
| Maximum error | $\max_i \lvert \hat y_i - y_i \rvert$ | The error a design decision can actually suffer; report with a high percentile (95th) |
| Coefficient of determination | $R^2 = 1 - \sum_i (\hat y_i - y_i)^2 / \sum_i (y_i - \bar y)^2$ | Dimensionless, but grows with the spread of the test set; not comparable between datasets |
| Relative $L^2$ field error | $\varepsilon_{L^2} = \lVert \hat{\mathbf{u}} - \mathbf{u} \rVert_V / \lVert \mathbf{u} \rVert_V$ | Per case, with $\lVert \mathbf{u} \rVert_V^2 = \sum_j V_j \lVert \mathbf{u}_j \rVert^2$ and cell volumes or face areas $V_j$; report the mean and worst case over test cases |

Force coefficients are best reported in drag counts ($\Delta C_d = 10^{-4}$ is one count), which engineers can compare directly with the design changes they care about. Field errors should also be looked at locally. A small $\varepsilon_{L^2}$ can hide a wrong separation line, which matters more than the free-stream error. For pressure, a relative error in the denominator $\lVert p \rVert$ depends on the reference pressure, so use $C_p$ or subtract the free-stream value first.

## Cross-Validation

In k-fold cross-validation the data are split into $k$ folds. Each fold is predicted by the model trained on the other $k - 1$ folds, and the held-out errors are pooled:

$$
\mathrm{CV}_k = \frac{1}{N} \sum_{i=1}^{N}
\ell\Big(\hat f^{(-\kappa(i))}(\mathbf{x}_i), y_i \Big)
$$

where $\kappa(i)$ is the fold containing sample $i$ and $\hat f^{(-\kappa)}$ the model trained without that fold. Every sample serves once for validation, so the estimate uses all the data, at the price of $k$ trainings; $k = 5$ or 10 is usual. With $k = N$ (leave-one-out, LOO) and a linear smoother $\hat{\mathbf{y}} = H\mathbf{y}$, such as least squares, ridge regression or a GP with fixed hyperparameters, no refitting is needed:

$$
y_i - \hat f^{(-i)}(\mathbf{x}_i) = \frac{y_i - \hat y_i}{1 - H_{ii}}
$$

The figure above uses LOO. At high degree its error grows much faster than the validation error, because removing an end sample forces the polynomial to extrapolate to it. Cross-validation estimates the error of a model trained on $(k-1)N/k$ samples, so it is slightly pessimistic for the final model trained on all $N$.

With groups (geometries) the folds must be groups, as with the splits above. If cross-validation is used both to tune hyperparameters and to report the error, the reported number is biased low. Nested cross-validation runs an inner loop for tuning inside each outer training fold and reports only the outer error.

## Hyperparameter Search

Hyperparameters (width, depth, learning rate, $\lambda$, dropout rate, kernel length scales) are chosen to minimise the validation or CV error, never the test error.

Grid search evaluates every combination of $m$ values for each of $h$ hyperparameters, $m^h$ trainings in all, and wastes most of them when only a few hyperparameters matter. Random search draws $n$ configurations from a distribution over the ranges. Each important hyperparameter is then tried at $n$ distinct values, and for the same budget it beats grid search in practice (Bergstra and Bengio, 2012). Scale parameters such as the learning rate and $\lambda$ are drawn log-uniformly.

Bayesian optimisation fits a GP to the validation errors observed so far and chooses the next configuration by maximising an acquisition function, typically the expected improvement over the best value $\mathcal{L}^\ast$ found so far. With GP mean $\mu(\mathbf{h})$, standard deviation $s(\mathbf{h})$ and $z = (\mathcal{L}^\ast - \mu)/s$,

```math
\mathrm{EI}(\mathbf{h}) = (\mathcal{L}^\ast - \mu)\, \Phi(z) + s\, \phi(z)
```

This is the same machinery as surrogate-based shape optimisation ([Adaptive Sampling](../../numerical/surrogates/adaptive_sampling.md)) and needs far fewer trainings when each is expensive (Snoek et al., 2012). Whatever the search, tune the learning rate first: it usually matters more than the architecture.

## Uncertainty Quantification

Prediction uncertainty has two sources. Aleatoric uncertainty is noise in the data, such as the scatter of time-averaged coefficients from a finite averaging window or experimental error, and does not shrink with more samples. Epistemic uncertainty comes from limited data and grows away from the training samples. It is the part that warns of extrapolation.

A deep ensemble trains $M$ networks (typically 5 to 10) from different random initialisations, and optionally different bootstrap samples (Lakshminarayanan et al., 2017). If member $m$ predicts a mean $\mu_m$ and, through a Gaussian likelihood, a variance $\sigma_m^2$, the ensemble prediction is

$$
\mu = \frac{1}{M}\sum_{m=1}^{M} \mu_m,
\qquad \sigma^2 = \frac{1}{M}\sum_{m=1}^{M} \big(\sigma_m^2 + \mu_m^2\big) - \mu^2
$$

where the spread of the $\mu_m$ estimates the epistemic part and the mean of the $\sigma_m^2$ the aleatoric part.

Monte Carlo dropout keeps dropout active at prediction time and takes the mean and variance over $T$ stochastic forward passes. It approximates Bayesian inference over the weights (Gal and Ghahramani, 2016) at the cost of $T$ evaluations and no extra training.

Gaussian processes give the predictive variance $\sigma^{\ast 2}$ in closed form (see the [introduction](../intro.md) and [Kriging](../../numerical/surrogates/kriging.md)). It depends only on the input locations and the kernel, which makes it a reliable extrapolation warning for low-dimensional inputs.

An uncertainty estimate is useful only if it is calibrated. On the test set, the fraction of targets inside the nominal 95 % interval $\mu \pm 1.96\sigma$ should be close to 95 %. If it is lower, the intervals are overconfident and can be rescaled by a factor fitted on the validation set. The Gaussian negative log-likelihood rewards accuracy and calibration together.

## Out-of-Distribution Detection

A query far from the training data should be flagged before its prediction is used. Common checks, from cheapest to most general, are:

- Range checks flag any feature outside its training interval. They are necessary but weak, because a point can lie inside every interval and still be far from the data.
- The Mahalanobis distance $d^2 = (\mathbf{x} - \boldsymbol\mu)^T \Sigma^{-1} (\mathbf{x} - \boldsymbol\mu)$ uses the training mean $\boldsymbol\mu$ and covariance $\Sigma$ and accounts for correlated parameters. For roughly Gaussian inputs, $d^2$ beyond the 95 % quantile of $\chi^2$ with $d$ degrees of freedom (5.99 for $d = 2$) marks a point as unusual.
- The distance from the query to its nearest training sample, in scaled inputs, can be compared with the distribution of the same distance within the training set.
- Disagreement between ensemble members, or a large GP variance, flags the query directly.
- Fields and geometries have no natural coordinates. For them, a large reconstruction error of an autoencoder trained on the training inputs, or a large distance in its latent space, marks a shape unlike any seen before.

Interpolation in the strict sense, meaning a query inside the convex hull of the training inputs, becomes rare as the dimension grows. For 200 samples drawn uniformly in a unit hypercube, a Monte Carlo test with linear programming finds about 96 % of new uniform points inside the hull in 2 dimensions, 62 % in 4, 19 % in 6 and 2 % in 10. A ten-parameter surrogate therefore extrapolates on almost every query, and OOD checks must measure how far, not just whether.

## Reporting Checklist for CFD Surrogates

1. Data provenance: solver, turbulence model, mesh strategy and resolution, convergence criteria, averaging windows, and an estimate of the CFD's own discretisation error.
2. The design space: parameter ranges, the sampling plan, number of cases, and any cases removed (unconverged, failed meshes) with the reason.
3. The split: the grouping variable (geometry, run, time block), the sizes of the training, validation and test sets, and confirmation that scaling statistics come from the training set.
4. The model: inputs and outputs with their preprocessing, architecture and parameter count, loss function, optimiser, learning-rate schedule, epochs, regularisation, and how hyperparameters were chosen.
5. Results on the untouched test set, in physical units (drag counts, $C_p$), with mean, high-percentile and maximum errors, and error plots against each input parameter.
6. Baselines: the mean predictor, linear regression and a GP or RBF model on the same split.
7. The comparison of the surrogate error with the CFD error and with the accuracy the application needs.
8. Uncertainty estimates and their calibration on the test set, and the OOD criterion used in deployment.
9. Cost: CFD hours for the data, training time and hardware, inference time per query, and the break-even number of queries.
10. Variability across random seeds (mean and spread over at least 3 trainings), and code and data availability.

## Key Takeaways

- Training error is optimistic; estimate generalisation on data the model never influenced, and use the test set once.
- Random splits leak information for time series, for several cases per geometry and for points of the same field. Split by time block or by group instead.
- Expected error is noise + bias² + variance. More flexible models trade bias for variance, and the validation or CV error, not the training error, locates the optimum.
- L2 penalties, dropout, early stopping and symmetry-based augmentation reduce variance. Choose their strengths by validation or (nested) cross-validation.
- Report errors in physical units, including the worst case, against simple baselines and against the CFD's own error.
- Ensembles, MC dropout and GP variances give per-prediction uncertainty; check their calibration, and flag out-of-distribution queries before trusting a prediction.

## Related Scripts

- [Bias-Variance Trade-off](../../../scripts/plots/bias_variance_tradeoff/): Polynomial fits of increasing degree to 20 noisy samples show underfitting, overfitting, a U-shaped validation curve and the Monte Carlo split of the error into bias², variance and noise.
- [MLP Regression](../../../scripts/algorithms/mlp_regression/): A two-hidden-layer tanh network written in numpy, with hand-coded backpropagation and Adam, learns a lift curve with stall from 60 noisy samples.
- [Cross-Design Generalization](../../../scripts/plots/cross_design_generalization/): is a synthetic illustration of why a surrogate trained on one design family can fail on another: three ridge-regression models trained on family X, family Y and both are tested on held-out designs of each family.
- [Drag Coefficient Prediction](../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient surrogates with held-out CFD values in a parity plot and an error plot, and shows that a high $R^2$ can hide errors of ten drag counts.

## Exercises

**Exercise 1.** Five test cars have CFD drag coefficients $0.285, 0.312, 0.298, 0.341, 0.276$, and a surrogate predicts $0.290, 0.305, 0.301, 0.322, 0.281$. Compute the MAE, RMSE, maximum error (in drag counts) and $R^2$.

<details>
<summary>Answer</summary>

The errors $\hat y_i - y_i$ are $0.005, -0.007, 0.003, -0.019, 0.005$.

$\mathrm{MAE} = 0.039/5 = 0.0078$ (78 counts). $\mathrm{RMSE} = \sqrt{0.000469/5} = 0.0097$ (97 counts). The maximum error is 0.019 (190 counts), on the car with the highest drag.

With $\bar y = 0.3024$, $\sum_i (y_i - \bar y)^2 = 0.002601$, so $R^2 = 1 - 0.000469/0.002601 = 0.820$.

An $R^2$ of 0.82 sounds good, but the worst-case error of 190 counts is larger than most design changes a team would try to resolve. The maximum error should be reported alongside it.

</details>

**Exercise 2.** A degree-7 polynomial ($p = 8$ coefficients) is fitted by least squares to $N = 20$ samples with noise $\sigma = 0.2$ at fixed locations, and its bias is negligible. Compute the average prediction variance at the sample locations, the expected training MSE and RMSE, and the expected MSE for new noisy observations at the same locations.

<details>
<summary>Answer</summary>

The average variance is $\sigma^2 p/N = 0.04 \times 8/20 = 0.016$. The expected training MSE is $\sigma^2 (1 - p/N) = 0.024$, an RMSE of 0.155, below the noise level 0.2. The expected MSE on new observations is $\sigma^2 (1 + p/N) = 0.056$.

The training error underestimates the test error by a factor of $(1 + p/N)/(1 - p/N) = 2.3$. The variance in panel 3 of the figure at $d = 7$ is 0.014, close to 0.016; it is evaluated on a fine grid between the samples rather than at the samples themselves.

</details>

**Exercise 3.** A dataset has 40 car geometries, each simulated at 5 yaw angles (200 cases), split randomly into 160 training and 40 test cases. What is the probability that a given test case has none of its 4 siblings in the training set? How should the split be made instead?

<details>
<summary>Answer</summary>

Given the test case, its 4 siblings must all fall among the other 39 test slots out of the remaining 199 cases:

```math
P = \frac{\binom{39}{4}}{\binom{199}{4}} = \frac{82\,251}{63\,391\,251} = 0.0013 .
```

On average only $40 \times 0.0013 = 0.05$ test cases belong to an unseen geometry, so the random split measures interpolation in yaw angle for known cars. A group split puts all 5 cases of 8 geometries (40 cases) into the test set; group 5-fold cross-validation rotates which 8 geometries are held out.

</details>

**Exercise 4.** An ensemble of 5 networks predicts $C_d = 0.301, 0.296, 0.305, 0.299, 0.304$ for a new design, and the members predict no aleatoric variance. (a) Give the ensemble mean, standard deviation and 95 % interval. (b) On 200 test cases, 162 targets lie inside their nominal 95 % intervals. What does this say, and what can be done?

<details>
<summary>Answer</summary>

(a) $\mu = 0.301$. With $\sigma^2 = \frac{1}{M}\sum_m \mu_m^2 - \mu^2$ the standard deviation is $\sigma = 0.0033$ (0.0037 with the $M - 1$ normalisation). The interval is $0.301 \pm 1.96 \times 0.0033 = [0.2946, 0.3074]$.

(b) The coverage is $`162/200 = 81\,\%`$, below the nominal 95 %, so the intervals are too narrow and the ensemble is overconfident. This is typical of ensembles whose members differ only by initialisation. Remedies: add an aleatoric variance output, use bootstrap resampling for the members, or rescale $\sigma$ by a factor fitted on the validation set so that the coverage reaches 95 %.

</details>

**Exercise 5.** Two standardised design parameters have training mean $(0, 0)$, unit variances and correlation 0.8. Is the query $(1.5, -1.0)$ out of distribution by the Mahalanobis criterion at the 95 % level? Compare with $(1.5, 1.0)$.

<details>
<summary>Answer</summary>

The inverse covariance is

```math
\Sigma^{-1} = \frac{1}{1 - 0.64}\begin{pmatrix} 1 & -0.8 \\ -0.8 & 1 \end{pmatrix},
```

so for $(1.5, -1.0)$

```math
d^2 = \frac{1.5^2 - 2(0.8)(1.5)(-1.0) + 1.0^2}{0.36} = \frac{5.65}{0.36} = 15.7 > 5.99 .
```

The query is out of distribution, although each coordinate lies within $\pm 1.5$ standard deviations. The training designs never move the two parameters in opposite directions. For $(1.5, 1.0)$, $d^2 = (2.25 - 2.4 + 1)/0.36 = 2.36 < 5.99$, so the query is in distribution, at the same Euclidean distance from the mean.

</details>

## References

- Hastie, T., Tibshirani, R., and Friedman, J., *The Elements of Statistical Learning*, 2nd ed., Springer, 2009.
- Goodfellow, I., Bengio, Y., and Courville, A., *Deep Learning*, MIT Press, 2016.
- Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., and Salakhutdinov, R., "Dropout: A Simple Way to Prevent Neural Networks from Overfitting", *Journal of Machine Learning Research* 15, 1929-1958, 2014.
- Bergstra, J., and Bengio, Y., "Random Search for Hyper-Parameter Optimization", *Journal of Machine Learning Research* 13, 281-305, 2012.
- Snoek, J., Larochelle, H., and Adams, R. P., "Practical Bayesian Optimization of Machine Learning Algorithms", *Advances in Neural Information Processing Systems* 25, 2012.
- Lakshminarayanan, B., Pritzel, A., and Blundell, C., "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles", *Advances in Neural Information Processing Systems* 30, 2017.
- Gal, Y., and Ghahramani, Z., "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning", *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48, 1050-1059, 2016.
- Belkin, M., Hsu, D., Ma, S., and Mandal, S., "Reconciling Modern Machine-Learning Practice and the Classical Bias-Variance Trade-off", *Proceedings of the National Academy of Sciences* 116(32), 15849-15854, 2019.
- Rasmussen, C. E., and Williams, C. K. I., *Gaussian Processes for Machine Learning*, MIT Press, 2006.
