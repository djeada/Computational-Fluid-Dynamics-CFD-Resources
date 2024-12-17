## Introduction to Kriging

Kriging is a powerful method for predicting values of a function at untried points based on values observed at known sample points. It originated in the field of geostatistics, thanks to the pioneering work of Daniel Krige in the 1950s for estimating ore concentrations in mining. Later, Georges Matheron provided a rigorous mathematical foundation for Kriging, turning it into a cornerstone of spatial interpolation methods. In the 1980s, Sacks and colleagues introduced these ideas to deterministic computer experiments, making Kriging a valuable tool in surrogate modeling for complex and expensive simulations in engineering and the sciences.

The idea behind Kriging is to model your data as a realization of a Gaussian process. This perspective allows for a broad and mathematically rigorous framework for interpolation and prediction, ensuring that the resulting interpolant is not only as accurate as possible given the data, but also accompanied by a measure of uncertainty. By carefully selecting correlation functions and tuning hyperparameters, Kriging models can adapt to various kinds of underlying behaviors, capturing both smooth global trends and highly nonlinear local features.

## Model Formulation and Assumptions

Kriging treats the unknown function of interest, typically denoted by $y(x)$ for $x \in \Omega \subset \mathbb{R}^d$, as the sum of a known global trend and a stochastic fluctuation term. This approach encodes the idea that we know something about the large-scale behavior of the function while acknowledging the complexity of the smaller-scale variations. In this formulation, each observation $y_i = y(x^{(i)})$ at a sample location $x^{(i)}$ is seen as a realization from a Gaussian process.

Consider a function modeled as  

$$y(x) = \sum_{j=1}^{K} \beta_j f_j(x) + z(x),$$  
where the functions $f_j(x)$ are known and capture the global or trend-like behavior, and the coefficients $\beta_j \in \mathbb{R}$ are unknown parameters. The term $z(x)$ represents the more complex, nonlinear part of the function, and is assumed to be a realization of a Gaussian process with zero mean, variance $\sigma^2$, and a correlation structure defined by a chosen correlation function $R(\|x-\tilde{x}\|)$.

A key assumption is second-order stationarity, meaning that the covariance depends only on the distance between points, not on their absolute position. Formally,  

$$\mathbb{E}[z(x)] = 0, \quad \text{Cov}[z(x), z(\tilde{x})] = \sigma^2 R(\|x - \tilde{x}\|).$$  

Here, $\sigma^2$ is the process variance and $R(\|\cdot\|)$ is a spatial autocorrelation function. This correlation function must be symmetric and positive definite, ensuring a well-posed problem that leads to a unique and stable solution.

In practice, this implies that points closer together are more strongly correlated, and as the distance between points grows large, their correlation approaches zero. The Kriging model often includes a linear regression part $f(x)^T \beta$ to represent large-scale trends, while $z(x)$ models complex departures from these trends through the Gaussian process framework.

## The Kriging Predictor as a Best Linear Unbiased Predictor (BLUP)

The Kriging predictor $\hat{y}(x)$ at any new point $x$ is defined as a linear combination of the observed data $Y = (y_1, \dots, y_N)^T$:

$$\hat{y}(x) = \sum_{i=1}^N \lambda_i(x) y_i.$$  

The weights $\lambda_i(x)$ depend on $x$ and are chosen to achieve the best linear unbiased prediction (BLUP). Best means that the mean squared error of the prediction is minimized, and unbiased means the expected difference between $\hat{y}(x)$ and $y(x)$ is zero.

This leads to a constrained optimization problem. The predictor must be unbiased, so that for any $f(x)$ representing the known trend,  

$$\mathbb{E}[\hat{y}(x)] = f(x)^T \beta.$$  

From the Gaussian process assumptions, it follows that there exist weights $\lambda(x) = (\lambda_1(x), \ldots, \lambda_N(x))^T \in \mathbb{R}^N$ and a vector $\mu(x) \in \mathbb{R}^K$ such that the Kriging weights and the Lagrange multipliers $\mu(x)$ solve the system:

$$\begin{pmatrix}
R & F \\
F^T & 0
\end{pmatrix}

\begin{pmatrix}
\lambda(x) \\ \mu(x)
\end{pmatrix}

=

\begin{pmatrix}
r(x) \\ f(x)
\end{pmatrix}
$$

Here, $R$ is the correlation matrix constructed from all sample points, and $r(x)$ is the vector of correlations between the new point $x$ and each sample point $x^{(i)}$. The matrix $F$ contains the regression basis functions evaluated at each sample point. Solving this system provides the Kriging weights $\lambda(x)$ and ensures unbiasedness and optimality of the prediction.

One of the neatest features of Kriging is its interpolation property. If we evaluate the Kriging predictor at any sample point $x^{(i)}$, we recover exactly $y(x^{(i)})$.

## Mean Squared Error and Confidence Intervals

The mean squared error (MSE) of the Kriging predictor measures the expected squared difference between the predicted value and the true function value:

$$\text{MSE}[\hat{y}(x)] = \mathbb{E}[(\hat{y}(x)-y(x))^2].$$  

This can be written explicitly as:

$$\text{MSE}[\hat{y}(x)] = \sigma^2 \left\{1 - 

\begin{pmatrix}
r(x) \\ f(x)
\end{pmatrix}^T

\begin{pmatrix}
R & F \\ F^T & 0
\end{pmatrix}^{-1}

\begin{pmatrix}
r(x) \\ f(x)
\end{pmatrix}

\right\}
$$  

From this formula, we see that if $x$ coincides with a sample point $x^{(i)}$, the MSE goes to zero, confirming exact interpolation.

When working with noisy data, additional regularization terms can be introduced, such as using $R + \epsilon I$ instead of $R$ to handle measurement noise. This balances fitting the data exactly with dealing robustly with noise.

## Relationship to Radial Basis Functions (RBF)

Kriging can be viewed as a weighted sum of correlation functions and low-order regression functions. After solving the initial system once, the evaluation of the Kriging surrogate at any new point $x$ is straightforward:

$$\hat{y}(x) = (w^{(Y)})^T r(x) + (w^{(f)})^T f(x),$$  
where the weight vectors $w^{(Y)}$ and $w^{(f)}$ depend only on the sample set and not on $x$.

This structure resembles radial basis function interpolation, where each sample point acts as a center for a basis function, here given by the correlation function. The difference is that Kriging ensures these basis functions emerge from a probabilistic and theoretically well-grounded model, while RBF methods usually adopt a more direct interpolation standpoint without a stochastic model.

## Choosing the Trend and Different Types of Kriging

If the trend $f(x)$ is chosen to be a constant function, the resulting method is called ordinary Kriging. If a polynomial trend is used, universal Kriging results. Generally, universal Kriging is more versatile since it can represent varying global behavior, but it introduces more unknown parameters and requires careful estimation.

## Correlation Functions and Anisotropy

The correlation function $R(\| x - \tilde{x} \|)$ lies at the heart of Kriging. Popular choices include exponential, Gaussian, and cubic spline-based correlations. Each correlation function has its own smoothness properties, affecting how the interpolant behaves, especially in regions with fewer sample points.

For instance, the Gaussian correlation function

$$R(h) = \exp\{ -\theta h^2 \}$$
produces very smooth interpolants but can be ill-conditioned if the data are highly correlated.

The choice of correlation function and its parameters $\theta = (\theta_1, \ldots, \theta_d)^T$ plays a crucial role in shaping the approximation quality. The parameter $\theta_k$ can be interpreted as a length scale along the $x_k$-direction. A small $\theta_k$ means rapid decay of correlation, focusing the prediction on nearby points. A large $\theta_k$ spreads the influence of observations over a larger region. For multi-dimensional problems, one can even model anisotropy and rotation of axes through transformations of the input space, though this becomes complex for higher dimensions.

Below is a plot reference (do not remove):

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/4ff1c3e1-fe3c-4f14-87c5-55f41a40fef4)

When selecting a correlation function, consider both the smoothness of the underlying function and the computational conditioning of the correlation matrix. For example, cubic correlation functions are known to produce well-conditioned matrices and can be beneficial for stability.

Another figure reference (do not remove):

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/3042ba17-f674-4851-b3e2-be35ee359c4c)

## Hyperparameter Estimation

Determining the correlation parameters $\theta$ is crucial. One typically uses maximum likelihood estimation (MLE) to find $\beta \in \mathbb{R}^K$, $\sigma^2 \in \mathbb{R}_+$, and $\theta \in \mathbb{R}^d_+$. The likelihood function measures how probable it is to observe the given data $Y$ under the chosen model. Maximizing the likelihood leads to optimal parameter estimates in a statistical sense.

The log-likelihood function involves the determinant and inverse of the correlation matrix $R(\theta)$, making the optimization a challenging nonlinear problem. With well-chosen optimization algorithms and correlation functions, one can successfully determine $\theta$ and achieve a high-quality surrogate.

In geostatistics, one may opt for variograms instead of correlation functions. A variogram $\gamma(h)$ relates directly to the difference $(y(x+h) - y(x))$, providing another avenue for fitting the correlation structure to data.

## Detailed Example in One Dimension

Consider a one-dimensional test function:

$$y(x) = (6x - 2)^2 \sin(12x - 4)$$
on the interval $\Omega = [0, 1]$. Suppose we choose nine sample points distributed more densely near the upper half of the domain where the function exhibits more erratic behavior.

Let us demonstrate how to build a Kriging surrogate step-by-step, including the estimation of $\theta$ and the evaluation of $\hat{y}(x)$.

I. Choose sample points $x^{(i)}$, for $i = 1, \ldots, 9$. For example, let:

$$X = \{0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0 \}.$$

Compute $y_i = y(x^{(i)})$ at these points. Since the function is known, we can directly evaluate:

$$y(x^{(i)}) = (6x^{(i)} - 2)^2 \sin(12x^{(i)} - 4).$$

For instance, if $x^{(1)} = 0.0$:

$$y(0.0) = (6 \cdot 0 - 2)^2 \sin(-4) = 4 \sin(-4).$$

If we approximate $\sin(-4)$ numerically (with $\sin(-4) \approx -0.7568$), this gives:

$$y(0.0) \approx 4 \cdot (-0.7568) = -3.0272.$$

Similarly, we compute $y(x^{(i)})$ for all sample points.

II. Choose a correlation function, for example a cubic correlation function. Its general form for a one-dimensional case might be:

$$R(h,\theta) = \begin{cases}

1 - 6(|\theta|h)^2 + 6(|\theta|h)^3 & \text{if } 0 \leq |\theta|h < 0.5, \\

2(1-|\theta|h)^3 & \text{if } 0.5 \leq |\theta|h < 1, \\

0 & \text{if } 1 \leq |\theta|h.

\end{cases}$$

Here, $h = |x - x^{(i)}|$ is the distance, and $\theta > 0$ is the hyperparameter that we need to estimate.

III. Construct the correlation matrix $R(\theta)$ of size $9 \times 9$ by evaluating $R(|x^{(i)} - x^{(j)}|,\theta)$ for every pair $(i,j)$. Since $R(0,\theta)=1$, the diagonal entries are all ones.

IV. Perform maximum likelihood estimation. We need to find $\beta, \sigma^2, \theta$ that maximize:

$$L(\beta,\sigma^2,\theta | Y) = (2 \pi \sigma^2)^{-\frac{N}{2}} (\det R(\theta))^{-\frac{1}{2}} \exp \left(-\frac{1}{2\sigma^2}(Y-F\beta)^T R(\theta)^{-1}(Y-F\beta)\right).$$

Here, if we assume a simple constant trend $f(x) = 1$, then $F$ is just a column of ones and $\beta$ is a scalar. We can derive conditions to solve for $\beta$ and $\sigma^2$ in terms of $\theta$. Then we use numerical optimization (e.g., gradient-based methods) to find the $\theta$ that maximizes the likelihood.

Suppose after optimization we find an approximately optimal $\theta^* = 2.5$.

V. Once $\theta^*$ is determined, we form the Kriging predictor:

$$\hat{y}(x) = f(x)^T\hat{\beta} + r(x)^T R(\theta^*)^{-1} (Y - F\hat{\beta}),$$
where $\hat{\beta}$ and $\sigma^{2*}$ are the estimated parameters. For each $x$, we compute $r(x)$, the correlation vector between $x$ and all sample points. Solving the linear systems provides the Kriging weights.

With the chosen $\theta^*=2.5$, the surrogate matches the data well in the denser upper half of the interval and gives a reasonably good approximation elsewhere, though it may struggle a bit in regions like $(0,0.25)$ where samples are sparse.

If we picked too small a $\theta$, say $\theta=1.75$, the correlation decays too slowly and each sample influences a large portion of the domain, potentially causing unwanted oscillations. Conversely, a very large $\theta$, say $\theta=5.0$, makes the correlation vanish too quickly, leaving each sample point influence very localized and possibly failing to capture the global structure in data-poor regions.

As $\theta \to \infty$, the correlation matrix $R(\theta)$ becomes closer to an identity matrix. This reduces the Kriging predictor to the simple regression model $f(x)^T\beta$ without meaningful interpolation of the sample variations. Thus, the parameter $\theta$ fundamentally controls how “local” or “global” the influence of each sample point is.
