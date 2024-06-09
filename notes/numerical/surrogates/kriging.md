# Kriging

  - Named after Daniel Krige, developed in the 1950s for ore concentration prediction.
  - Further developed by Matheron.
  - Widely used in spatial prediction and geostatistics.
  - Introduced to deterministic computer experiments in the 1980s by Sacks et al.
  - Popular in surrogate modeling for expensive simulations and engineering problems.

- **Model Assumptions:**
  - **Kriging Prediction Formula:**
    - $\hat{y}(x) = \sum_{i=1}^{N} \lambda_i(x) y_i$
    - Weights $\lambda(x) = (\lambda_1(x), \ldots, \lambda_N(x))^\top \in \mathbb{R}^N$ depend on $x$.
    - Influence of $y_i$ on $\hat{y}(x)$ increases if $x$ is close to $x^{(i)}$.

  - **Model Components:**
    - $y(x)$ is modeled as a sum of a linear regression part and a lack-of-fit term:
      - $y(x) = \sum_{j=1}^{K} \beta_j f_j(x) + z(x), \quad x \in \Omega \subset \mathbb{R}^d$
    - $f_j(x)$ are known functions with coefficients $\beta_j \in \mathbb{R}$.

  - **Error Term $z(x)$:**
    - Not a random error or white noise.
    - Captures the nonlinear behavior of $y(x)$.
    - Modeled as a realization of a Gaussian stochastic process.

- **Gaussian Process Assumptions:**
  - $Z = (z(x^{(1)}), \ldots, z(x^{N)}))^\top$ is multivariate normally distributed.
  - Second-order stationary process:
    - $\mathbb{E}[z(x)] = 0$
    - $\text{Cov}[z(x), z(\tilde{x})] = \sigma^2 R(||x - \tilde{x}||), \quad \forall x, \tilde{x} \in \Omega$
    - $\sigma^2 > 0$ is the process variance.
    - $R(||x - \tilde{x}||)$ is the spatial autocorrelation function.

  - **Autocorrelation Function:**
    - Must satisfy symmetry and nonnegative definiteness:
      - $R(\tilde{x} - x) = R(x - \tilde{x}) \quad \forall x, \tilde{x} \in \Omega$
      - $\sum_{i=1}^{N} \sum_{j=1}^{N} w_i w_j R(||x^{(i)} - x^{(j)}||) \geq 0 \quad \forall \{ w_i \}_{i=1}^{N} \subset \mathbb{R}$

- **Kriging Model Properties:**
  - For unbiased approximation, the covariation function depends only on the distance vector $\tilde{x} - x$.
  - $z(x)$ and $\tilde{x}$ are strongly correlated when $x$ and $\tilde{x}$ are close.
  - A suitable correlation function satisfies $R(0) = 1$ and $R(\tilde{x} - x) \rightarrow 0$ as $||\tilde{x} - x|| \rightarrow \infty$.

- **Gaussian Process for $y(x)$:**
  - $y(x)$ is a Gaussian process with:
    - $\mathbb{E}[y(x)] = f(x)^\top \beta$
    - $\text{Cov}[y(x), y(\tilde{x})] = \sigma^2 R(||\tilde{x} - x||)$

  - $Y$ and $Z$ distributions:
    - $Y \sim \mathcal{N}_N(F \beta, \sigma^2 R)$
    - $Z \sim \mathcal{N}_N(0, \sigma^2 R)$

  - **Matrices:**
    - $F := [f_j(x^{(i)})]_{i=1,j=1}^{N,K} \in \mathbb{R}^{N \times K}$ is the regression matrix.
    - $R := [R(||x^{(i)} - x^{(j)}||)]_{i,j=1}^{N,N} \in \mathbb{R}^{N \times N}$ is the symmetric and positive definite correlation matrix.

  - **Positive Definiteness Condition:**
    - For $R$ to be positive definite:
      - $\sum_{i=1}^{N} \sum_{j=1}^{N} w_i w_j R(||x^{(i)} - x^{(j)}||) > 0 \quad \forall x^{(i)} 
eq x^{(j)} (i 
eq j), w \in \mathbb{R}^N \setminus \{0\}$

## Kriging Predictor

- **Overview:**
  - Kriging, also known as Gaussian process prediction, uses the properties of Gaussian processes to interpolate data.
  - Unlike regression models that rely on a sophisticated linear model, Kriging uses Gaussian processes to provide a best linear unbiased predictor (BLUP) for the response $y(x)$.

- **Best Linear Unbiased Prediction (BLUP):**
  - A prediction $\hat{y}(x)$ is a BLUP if it is a linear combination of observed data:
    - $\hat{y}(x) = \sum_{i=1}^{N} \lambda_i(x) y_i$
  - The BLUP minimizes the mean squared error (MSE):
    - $\text{MSE}[\hat{y}(x)] := \mathbb{E} \left[ (\hat{y}(x) - y(x))^2 \right]$
  - Subject to the unbiasedness condition:
    - $\mathbb{E}[\hat{y}(x) - y(x)] = 0$

- **Theorem 2.4:**
  - For $x^{(i)} 
eq x^{(j)}$ (for $i 
eq j$) and $F$ having full column rank $K$, the Kriging predictor $\hat{y}(x)$ is a BLUP for $y(x)$.
  - The linear system to solve is:
    - 
$$
      \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)
      \left( \begin{array}{c} \lambda(x) \\ \mu(x) \end{array} \right) =
      \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right)
      $$

  - Here, $r(x)$ is the correlation vector, $\mu(x)$ is a Lagrange variable, and $R, F, f(x), \lambda(x)$ are as previously defined.

- **Proof Outline:**
  - The proof involves minimizing the MSE subject to the unbiasedness condition.
  - The unbiasedness condition leads to:
    - $\lambda(x)^T F = f(x)^T$
  - The error of the surrogate model is:
    - $\lambda(x)^T Z - z(x)$
  - The MSE is:
    - $\sigma^2 \left( \lambda(x)^T R \lambda(x) - 2 \lambda(x)^T r(x) + 1 \right)$
  - Solving the optimization problem:
    - 
$$
      \min_{\lambda(x) \in \mathbb{R}^N} \frac{1}{2} \lambda(x)^T R \lambda(x) - r(x)^T \lambda(x)
      $$

    - Subject to:
      - $F^T \lambda(x) - f(x) = 0$
  - Introducing Lagrange variable $\mu(x)$, the Karush-Kuhn-Tucker system is:
    - 
$$
      \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)
      \left( \begin{array}{c} \lambda(x) \\ \mu(x) \end{array} \right) =
      \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right)
      $$


- **Interpolation Property:**
  - Inserting any $x^{(i)}$ for $x$, the surrogate model evaluates correctly:
    - $\hat{y}(x^{(i)}) = y_i$

- **MSE Representation:**
  - The MSE can be expressed as:
    - 
$$
      \text{MSE}[\hat{y}(x)] = \sigma^2 \left\{ 1 - \left( \begin{array}{c} r(x)^T \\ f(x)^T \end{array} \right)^T \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)^{-1} \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right) \right\}
      $$


- **Noisy Data Consideration:**
  - Kriging can be extended to handle noisy or stochastic data by:
    - Regularizing the correlation matrix: $R + \epsilon I$
    - Scaling the correlation function: $\tilde{R}(h) := (1 - \epsilon) R(h)$
  - For deterministic and smooth responses, interpolation without regularization is preferred.

## Connection to Radial Basis Functions

- **Expansion of the Surrogate Model:**
  - The expression $\lambda(x)^T Y$ can be expanded as:
    - 
$$
      \left( \begin{array}{c} \lambda(x) \\ \mu(x) \end{array} \right)^T
      \left( \begin{array}{c} Y \\ 0 \end{array} \right) =
      \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right)^T
      \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)^{-1}
      \left( \begin{array}{c} Y \\ 0 \end{array} \right)
      $$

  - Instead of solving for $\lambda(x)$ each time, solve the linear equation once:
    - 
$$
      \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)
      \left( \begin{array}{c} w^{(Y)} \\ w^{(f)} \end{array} \right) =
      \left( \begin{array}{c} Y \\ 0 \end{array} \right)
      $$

    - Solution $\left( \begin{array}{c} w^{(Y)} \\ w^{(f)} \end{array} \right)$ is independent of $x$ and depends on $X, Y$.

- **Evaluation of the Surrogate Model:**
  - Evaluate $\hat{y}(x)$ as:
    - 
$$
      \hat{y}(x) = \left( \begin{array}{c} w^{(Y)} \\ w^{(f)} \end{array} \right)^T
      \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right)
      $$

    - This reveals the connection between Kriging and radial basis functions (RBF).

- **Weighted Sum of Functions:**
  - The surrogate is a weighted sum of:
    - Correlation functions $R(||x^{(i)} - x||)$
    - Regression functions $f_j(x)$
  - Weights satisfy interpolation and unbiasedness conditions.
  - Correlation functions act as local basis functions with centers $x^{(i)}$.

- **Comparison to Radial Basis Functions:**
  - Unlike RBF, $R(||x^{(i)} - x||)$ does not need to be radially symmetric around $x^{(i)}$.

## Connection to Model Assumptions

- **Optimal Weights $\lambda(x)$:**
  - Connection between $\hat{y}(x) = \lambda(x)^T Y$ and model assumption $y(x)$.
  - Use partitioned inversion formula:
    - 
$$
      \left( \begin{array}{cc} R & F \\ F^T & 0 \end{array} \right)^{-1} =
      \left( \begin{array}{cc} R^{-1} - R^{-1} F (F^T R^{-1} F)^{-1} F^T R^{-1} & R^{-1} F (F^T R^{-1} F)^{-1} \\
      (F^T R^{-1} F)^{-1} F^T R^{-1} & -(F^T R^{-1} F)^{-1} \end{array} \right)
      $$

  - Solution for $\lambda(x)$ and $\mu(x)$:
    - 
$$
      \mu(x) = (F^T R^{-1} F)^{-1} (F^T R^{-1} r(x) - f(x))
      $$

    - 
$$
      \lambda(x) = R^{-1} (r(x) - F \mu(x))
      $$


- **Rewriting the Kriging Predictor:**
  - 
$$
      \hat{y}(x) = \lambda(x)^T Y = (r(x) - F \mu(x))^T R^{-1} Y
      $$

    - 
$$
      = f(x)^T \beta + r(x)^T R^{-1} (Y - F \beta)
      $$

    - 
$$
      = f(x)^T \beta + r(x)^T R^{-1} Z
      $$

  - The surrogate is a sum of:
    - Regression model $f(x)^T \beta$
    - Weighted sum of correlation functions $r(x)^T R^{-1} Z$
  - Regression model approximates the global trend; the second term captures nonlinear behavior.

- **Types of Kriging:**
  - **Ordinary Kriging:**
    - Simplest case with $K = 1, f_1 = 1, y(x) = \beta_1 + z(x)$.
  - **Universal Kriging:**
    - Uses low-order polynomials.

- **Considerations for Interpolation:**
  - Ordinary Kriging suffices if no global trend is known.
  - Universal Kriging notation is maintained for general applicability.

## Correlation Functions

- **Importance of Correlation Functions:**
  - Before generating a Kriging predictor, specify a correlation function $R(\tilde{x} - x)$.
  - The surrogate model $\hat{y}(x) = \lambda(x)^T Y = \left( \begin{array}{c} w^{(Y)} \\ w^{(f)} \end{array} \right)^T \left( \begin{array}{c} r(x) \\ f(x) \end{array} \right)$ is a weighted sum of:
    - Correlation functions $r_i(x) = R(||x^{(i)} - x||)$ with centers $x^{(i)}$
    - Regression functions $f_j(x)$
  - The choice of an appropriate correlation function is crucial.

- **Hyperparameters:**
  - Correlation functions are parametrized by hyperparameters $\theta = (\theta_1, \ldots, \theta_d)^T \in \mathbb{R}^d$.
  - Often, the multivariate $R : \mathbb{R}^d \rightarrow \mathbb{R}$ is modeled as a product of univariate correlation functions:
    - $\tilde{R}(\tilde{x} - x, \theta) = \prod_{k=1}^{d} R_k (||\tilde{x}_k - x_k||, \theta_k)$
  - $\theta_k > 0$ controls the influence of $y_i$ along the $x_k$-axis.

- **Modeling Anisotropy:**
  - Allows scaling and rotation in the input space $\mathbb{R}^d$ by additional parameters $\tilde{\theta}$.
  - For $d = 2$, the rotation matrix:
    - $Q_{\tilde{\theta}_1} = \left( \begin{array}{cc} \cos \tilde{\theta}_1 & -\sin \tilde{\theta}_1 \\ \sin \tilde{\theta}_1 & \cos \tilde{\theta}_1 \end{array} \right)$
  - For $d = 3$, the rotation matrix:
    - 
$$
      Q_{\tilde{\theta}_1, \tilde{\theta}_2, \tilde{\theta}_3} = \left( \begin{array}{ccc} \cos \tilde{\theta}_2 \cos \tilde{\theta}_3 & -\sin \tilde{\theta}_3 \cos \tilde{\theta}_1 + \cos \tilde{\theta}_3 \sin \tilde{\theta}_2 \sin \tilde{\theta}_1 & \sin \tilde{\theta}_3 \sin \tilde{\theta}_1 + \cos \tilde{\theta}_3 \sin \tilde{\theta}_2 \cos \tilde{\theta}_1 \\ \cos \tilde{\theta}_2 \sin \tilde{\theta}_3 & \cos \tilde{\theta}_3 \cos \tilde{\theta}_1 + \sin \tilde{\theta}_3 \sin \tilde{\theta}_2 \sin \tilde{\theta}_1 & -\cos \tilde{\theta}_3 \sin \tilde{\theta}_1 + \sin \tilde{\theta}_3 \sin \tilde{\theta}_2 \cos \tilde{\theta}_1 \\ -\sin \tilde{\theta}_2 & \cos \tilde{\theta}_2 \sin \tilde{\theta}_1 & \cos \tilde{\theta}_2 \cos \tilde{\theta}_1 \end{array} \right)
      $$


![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/4ff1c3e1-fe3c-4f14-87c5-55f41a40fef4)

- **Examples of Correlation Functions:**
  - **Linear Correlation Functions:**
    - $\tilde{R}(\tilde{x} - x, \theta) = \max \{ 1 - \theta ||\tilde{x} - x||, 0 \}$
    - $C^0(\mathbb{R})$-functions, not differentiable at the origin.
    - Zero correlation for $||h|| \geq \frac{1}{\theta}$.
  - **Exponential Correlation Functions:**
    - $\tilde{R}(\tilde{x} - x, \theta) = \exp \{ -\theta ||\tilde{x} - x|| \}$
    - $C^0(\mathbb{R})$, not differentiable at the origin.
    - $R(h) > 0$ for all $h \in \mathbb{R}$.
  - **Gaussian Correlation Functions:**
    - $\tilde{R}(\tilde{x} - x, \theta) = \exp \left\{ -\theta (\tilde{x} - x)^2 \right\}$
    - $C^\infty (\mathbb{R})$, very smooth interpolations.
    - Can produce inappropriate interpolations for highly nonlinear responses.
    - Correlation matrices can be ill-conditioned.
  - **Cubic Splines:**
    - 
$$
      \tilde{R}(\tilde{x} - x, \theta) = \begin{cases}
      1 - 6 (|\theta|h)^2 + 6 (|\theta|h)^3, & 0 \leq |\theta|h < 0.5 \\
      2 (1 - |\theta|h)^3, & 0.5 \leq |\theta|h < 1 \\
      0, & 1 \leq |\theta|h
      \end{cases}
      $$

    - Twice continuously differentiable in $\mathbb{R}$, finite support.
    - Correlation matrices are well-conditioned.
  - **Generalized Exponential Correlation Functions:**
    - $\tilde{R}(\tilde{x} - x, \theta, p) = \exp \left\{ -\theta ||\tilde{x} - x||^p \right\}$
    - Second hyperparameter $p \in (0, 2]$, varies for different dimensions.
    - Contains both exponential ($p = 1$) and Gaussian ($p = 2$) correlation functions.

- **Considerations for Geostatistics and Computer Experiments:**
  - In geostatistics, rotation of the correlation axis can improve approximation quality.
  - In computer experiments, the input parameters generally correspond to different physical inputs, so rotation is not typically applied.
  - Modeling anisotropy becomes challenging for $d > 3$ due to the growing number of rotation parameters.

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/3042ba17-f674-4851-b3e2-be35ee359c4c)'

## Hyperparameter Estimation

- **Correlation Function and Hyperparameters:**
  - After selecting a correlation function $R(h, \theta)$, the hyperparameters $\theta = (\theta_1, \ldots, \theta_d)^T$ need to be defined.
  - For most correlation functions, the scaling in $h_k$ is proportional to $\frac{1}{\theta_k}$, except for the Gaussian correlation function ($\frac{1}{\sqrt{\theta_k}}$) and the generalized exponential function ($\frac{1}{\theta_k}$).

- **Influence on Approximation Quality:**
  - The Kriging predictor is a weighted sum of correlation functions $R(||x^{(i)} - x||, \theta)$ and regression functions $f_j(x)$.
  - Both the choice of the correlation model and the hyperparameters $\theta$ greatly influence approximation quality.

- **Model Fitting:**
  - Optimal hyperparameters $\theta$ are determined to best suit the given data set $X, Y$.
  - This process, known as model fitting, adapts the hyperparameters to the data.
  - For every $\theta \in \mathbb{R}^d_+$, the Kriging predictor is an interpolator, affecting $\hat{y}(x)$ only in $\Omega \setminus X$.

- **Maximum Likelihood Estimation (MLE):**
  - Used to find unknowns $\beta \in \mathbb{R}^K$, $\sigma^2 \in \mathbb{R}_+$, and $\theta \in \mathbb{R}^d_+$.
  - The likelihood function is:
    - 
$$
      L(\beta, \sigma^2, \theta | Y) = (2 \pi \sigma^2)^{-\frac{N}{2}} (\det R(\theta))^{-\frac{1}{2}} \exp \left( -\frac{1}{2\sigma^2} (Y - F \beta)^T R(\theta)^{-1} (Y - F \beta) \right)
      $$

  - Maximizing $L(\beta, \sigma^2, \theta | Y)$ is equivalent to minimizing the negative log-likelihood:
    - 
$$
      -\log L(\beta, \sigma^2, \theta | Y) = \frac{N}{2} \log (2 \pi \sigma^2) + \frac{1}{2} \log (\det R(\theta)) + \frac{1}{2 \sigma^2} (Y - F \beta)^T R(\theta)^{-1} (Y - F \beta)
      $$


- **First Order Optimality Conditions:**
  - Partial derivatives with respect to $\beta_j$, $\sigma^2$, and $\theta_k$ are used to find optimal values:
    - 
$$
      \frac{\partial}{\partial \beta_j} (-\log L) = -\frac{1}{\sigma^2} (F^T R(\theta)^{-1} (Y - F \beta))_j
      $$

    - 
$$
      \frac{\partial}{\partial \sigma^2} (-\log L) = \frac{N}{2 \sigma^2} - \frac{1}{2 \sigma^4} (Y - F \beta)^T R(\theta)^{-1} (Y - F \beta)
      $$

    - 
$$
      \frac{\partial}{\partial \theta_k} (-\log L) = \frac{1}{2} \text{trace} \left( R(\theta)^{-1} \frac{\partial R(\theta)}{\partial \theta_k} \right) - \frac{1}{2 \sigma^2} (Y - F \beta)^T R(\theta)^{-1} \frac{\partial R(\theta)}{\partial \theta_k} R(\theta)^{-1} (Y - F \beta)
      $$


- **Solving the Optimization Problem:**
  - Numerical optimization is used to solve:
    - 
$$
      \min_{\beta \in \mathbb{R}^K, \sigma^2 \in \mathbb{R}_+, \theta \in \mathbb{R}^d_+} \left\{ - \log L(\beta, \sigma^2, \theta | Y) \right\}
      $$

  - The problem can be reduced by substituting $\beta$ and $\sigma^2$ with $\beta^*$ and $\sigma^{2*}$, leaving:
    - 
$$
      \min_{\theta \in \mathbb{R}^d_+} \left\{ N \log (\sigma^2 (\theta, \beta(\theta))) + \log (\det R(\theta)) \right\}
      $$


- **Numerical Challenges:**
  - Highly nonlinear implicit dependencies in $\theta$ can complicate optimization.
  - Gradient-based optimization algorithms can face difficulties due to nonlinearity.
  - The objective function's partial derivatives with respect to $\theta_k$ involve complex computations.
  - Choose differentiable correlation functions to ensure a smooth objective function.

- **Variogram Function Approach (Geostatistics):**
  - Instead of a correlation function, a variogram function $\gamma(h)$ is used:
    - 
$$
      2\gamma(h) := \text{Var} [y(x + h) - y(x)]
      $$

  - A variogram function can be defined by $\gamma(h) = \sigma^2 (1 - R(h))$.

### Examples

- **One-Dimensional Test Function:**
  - Test function: $y(x) = (6x - 2)^2 \sin (12x - 4)$
  - Interpolated in $\Omega = [0, 1]$
  - Influence of hyperparameter $\theta$ on approximation quality of $\hat{y}(x)$

- **Interpolation with Cubic Correlation Function:**
  - $N = 9$ samples $x^{(i)}$ are denser in the upper half of the interval to resolve erratic behavior.
  - $\theta$ acts as a scaling factor in $h$ for the correlation function.
  - Larger $\theta$ leads to faster decrease of $R(h, \theta)$ in $h$.
  - For cubic correlation function, $R(h, \theta) = 0$ for all $h \geq \frac{1}{\theta}$.
  - The surrogate model $\hat{y}(x)$ is influenced by $y(x^{(i)})$ only within $\left( x^{(i)} - \frac{1}{\theta}, x^{(i)} + \frac{1}{\theta} \right)$.

- **Optimal $\theta$:**
  - Approximate solution of maximum likelihood problem: $\theta^* = 2.5$
  - The surrogate model with $\theta^* = 2.5$ provides a good approximation except for $x \in (0, 0.25)$ where data is insufficient.

- **Effects of $\theta$ Values:**
  - **Too Small $\theta$ (e.g., $\theta = 1.75$):**
    - Overestimates correlation between $y(x^{(i)})$.
    - Large influence of $y(x^{(i)})$ on $\hat{y}(x)$ even if $x^{(i)}$ is far.
    - Unwanted variations in $\hat{y}(x)$ in regions with few samples ($x \in [0, 0.5]$).
    - Poor approximation quality.
  - **Too Large $\theta$ (e.g., $\theta = 5.0$):**
    - $R(h, \theta)$ decays too quickly towards zero.
    - Poor approximation quality in regions with few samples.
    - Even larger $\theta = 10.0$ results in poor approximation in the denser sampled upper half interval.
  - **General Behavior for Large $\theta$:**
    - For any correlation function with $\theta$ as a scaling parameter in $h$, $R(x - x, \theta) \rightarrow 1_{[0)}(x)$ as $\theta \rightarrow \infty$.
    - Correlation matrix becomes the identity matrix ($R \rightarrow I$).
    - Surrogate converges to the regression term: $\hat{y}(x) = f(x)^T \beta$.
