# Learning Paradigms on Flow Data

Three panels contrast supervised regression, supervised classification and unsupervised clustering on synthetic flow data, each computed in numpy. A Gaussian process fits noisy drag coefficients with a predictive band, logistic regression learns a laminar/turbulent boundary, and k-means groups unlabelled wake features into regimes.

## Overview

- Draws 25 rear slant angles uniformly in $[0^\circ, 40^\circ]$ and evaluates a smooth synthetic $C_d(\varphi)$ with a drag rise near $30^\circ$, adding Gaussian noise of standard deviation 0.008.
- Fits a Gaussian process with a squared-exponential kernel (length scale $6^\circ$, prior standard deviation 0.03, noise standard deviation 0.008) and plots its mean and 95 % predictive band.
- Draws 200 points in the plane of $\log_{10} Re_x \in [5, 6.5]$ and free-stream turbulence $`Tu \in [0, 3]\,\%`$, and labels them turbulent with probability $1/(1 + e^{-8m})$, where $`m = \log_{10} Re_x - (6.2 - 0.35\,Tu)`$ is the distance past a synthetic transition rule.
- Fits logistic regression by Newton's method and draws the probability field, the learned $p = 0.5$ boundary and the labelling rule.
- Draws 60 unlabelled samples from each of three Gaussian regimes in the plane of mean drag $\overline{C_d}$ and RMS lift $C_L'$ and clusters them with k-means ($k = 3$).

## Mathematical Background

### Gaussian-Process Regression

With kernel $k(\varphi, \varphi') = s^2 \exp\big(-(\varphi - \varphi')^2 / (2 l^2)\big)$, kernel matrix $K$, noise variance $\sigma_n^2$ and the sample mean $\bar y$ as constant prior mean, the prediction at $\varphi^\ast$ is

```math
\mu^\ast = \bar y + \mathbf{k}_\ast^T (K + \sigma_n^2 I)^{-1} (\mathbf{y} - \bar y),
\qquad
\sigma^{\ast 2} = s^2 - \mathbf{k}_\ast^T (K + \sigma_n^2 I)^{-1} \mathbf{k}_\ast + \sigma_n^2 ,
```

and the band is $`\mu^\ast \pm 1.96\, \sigma^\ast`$. Including $\sigma_n^2$ makes it a band for new observations, not only for the mean.

### Logistic Regression

The probability of the turbulent class is $\hat y = 1/(1 + e^{-(\mathbf{w}^T\mathbf{x} + b)})$. The weights minimise the cross-entropy

```math
\mathcal{L} = -\sum_i \big[ y_i \log \hat y_i + (1 - y_i) \log (1 - \hat y_i) \big],
```

whose gradient is $X^T(\hat{\mathbf{y}} - \mathbf{y})$ and whose Hessian is $X^T S X$ with $S = \mathrm{diag}(\hat y_i (1 - \hat y_i))$. Newton's method (iteratively reweighted least squares) updates $\boldsymbol\theta \leftarrow \boldsymbol\theta - (X^T S X)^{-1} X^T (\hat{\mathbf{y}} - \mathbf{y})$. The decision boundary is the line $\mathbf{w}^T \mathbf{x} + b = 0$.

### k-Means

Lloyd's algorithm minimises the within-cluster sum of squares $`J = \sum_i \lVert \mathbf{z}_i - \boldsymbol\mu_{c_i} \rVert^2`$ by alternating two steps: assign each point to its nearest centroid, then move each centroid to the mean of its points. Neither step can increase $J$, so the iteration converges, to a local minimum. The features are standardised first so that $\overline{C_d}$ and $C_L'$ count equally, and k-means++ seeding picks each new initial centroid with probability proportional to the squared distance from the nearest existing one.

## Implementation

- `drag_coefficient(slant_deg)` is the synthetic trend $`C_d = 0.25 + 0.06\, e^{-((\varphi - 30)/7)^2} + 0.0008\,\varphi`$.
- `rbf_kernel(a, b, length, signal_std)` and `gp_regression(x, y, x_new, noise_std)` compute the GP mean and 95 % half-width with a Cholesky factorisation.
- `make_classification_data(rng)` samples and labels the boundary-layer points; `fit_logistic_regression(features, labels, iterations)` runs 25 Newton steps on standardised features with a $10^{-6}$ ridge term and returns $(\mathbf{w}, b)$ in the original units.
- `make_clustering_data(rng)` draws the three regimes from `REGIME_CENTRES` and `REGIME_SPREADS`; `kmeans(points, k, rng, iterations)` returns labels, centroids and the within-cluster sum of squares.
- `plot_regression`, `plot_classification` and `plot_clustering` each draw one panel, and `make_figure(seed)` assembles them with a single seeded generator.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Gaussian-process regression of drag, logistic-regression classification of laminar and turbulent samples, and k-means clustering of wake features](ml_learning_paradigms.png)

In the left panel the GP mean follows the drag rise near $30^\circ$, and the predictive band is widest near the ends of the range, where each sample has neighbours on one side only. In the centre panel the learned boundary is $`\log_{10} Re_x = 6.14 - 0.31\,Tu`$, close to the rule $`6.2 - 0.35\,Tu`$ that generated the labels. The training accuracy is 88 %; the misclassified points lie in the band around the boundary where the labels are random by construction. In the right panel k-means finds the three regimes without labels, placing 176 of the 180 samples with the majority of their own regime. Of the four exceptions, two high-$`C_L'`$ samples fall in the middle cluster and two middle-regime samples fall in the low-drag cluster, all in the tails between neighbouring regimes.

## Related Notes

- [Introduction to ML for CFD](../../../notes/machine_learning/intro.md)
- [Flow Feature Extraction](../../../notes/machine_learning/flow/feature_extraction.md)
- [Kriging](../../../notes/numerical/surrogates/kriging.md)
