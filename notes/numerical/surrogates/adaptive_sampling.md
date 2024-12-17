## Introduction to Adaptive Designs

Adaptive sampling strategies have been developed as an effective alternative to one-stage design methods, and they have gained considerable attention over the past decade. Unlike a-priori methods, which fix all sample locations before constructing the surrogate model, adaptive or a-posteriori sampling dynamically updates both the sample set $X$ and the surrogate model $\hat{y}(x)$. These updates occur in stages and incorporate information from the currently available data and model predictions to guide the selection of new sample points. By incrementally refining the design, adaptive approaches aim to place samples more intelligently, resulting in models that achieve a desired accuracy with fewer evaluations of the expensive response function $y(x)$.

## Initial Design and Incremental Model Construction

Adaptive approaches typically start with a small initial design $X(N_0)$ of size $N_0$. This initial set of sample points often results from a one-stage method, which may be something as simple as a space-filling design over $\Omega \subset \mathbb{R}^d$. After evaluating the response $y(x)$ at these initial samples, one constructs the initial surrogate model $\hat{y}^{(N_0)}(x)$ based on the data $X(N_0)$ and $Y(N_0) \in \mathbb{R}^{N_0}$.

When using Kriging or gradient-enhanced Kriging, this initial step involves estimating hyperparameters and solving the linear Kriging system. Once the initial model is built, one can proceed to the adaptive sampling stages. At each subsequent stage, new samples are added based on criteria derived from the current surrogate model, and the model is then updated to incorporate the newly acquired data. This iterative process continues until a stopping condition is reached, such as a maximum budget of evaluations $N_{\text{max}}$ or a convergence criterion on the surrogate model error.

## Adaptive Sampling Process and Termination Criteria

Adaptive sampling follows a stage-wise update process. Suppose one currently has $N_i$ samples and a surrogate $\hat{y}^{(N_i)}(x)$. The approach selects a new point $x^{(N+1)}$ according to a selection criterion that reflects the current knowledge encoded in $\hat{y}^{(N_i)}(x)$. After evaluating $y(x^{(N+1)})$, the design and data sets become $X(N_{i+1}) = X(N_i) \cup \{x^{(N+1)}\}$ and $Y(N_{i+1}) = Y(N_i) \cup \{y(x^{(N+1)})\}$. A new surrogate $\hat{y}^{(N_{i+1})}(x)$ is constructed, often with updated hyperparameters. This process of adding new samples, evaluating responses, and rebuilding surrogates continues until either the maximum number of samples $N_{\text{max}}$ is used or until an error estimator indicates that the model meets accuracy targets.

Adaptive strategies do not require knowing $N_{\text{max}}$ in advance. Instead, the process adapts to the complexity of the underlying response. This flexibility leads to more efficient exploration of $\Omega$.

## Exploitation, Exploration, and Balanced Strategies

Adaptive designs often balance two opposing tendencies: exploitation and exploration. Exploitation focuses on regions where the surrogate currently predicts good performance (for example, areas near a predicted optimum), aiming to refine local accuracy. Exploration targets regions where the surrogate is uncertain or where insufficient sampling density exists, ensuring the model does not miss important behaviors elsewhere.

Relying solely on exploitation can lead to local optima, since the model might fail to discover distant but potentially better parts of the domain. Pure exploration can be expensive, as it may require too many samples to fully guarantee global discovery of important features. A mixed strategy that balances exploration and exploitation tends to be more robust. Such an approach places more samples in critical regions, while still maintaining sufficient global coverage to uncover all essential features of the response.

## Adaptive Designs for Global Optimization

A seminal algorithm in this field is the Efficient Global Optimization (EGO) method, which uses the expected improvement criterion to select new samples. This approach has inspired many enhancements and variants that improve performance or adapt to different problem contexts.

Other criteria for adaptively selecting new samples include integrated mean squared error (IMSE) or related measures. These adapt the design to the shape of the true response $y(x)$, ensuring that regions of high complexity or importance are sampled more densely. By doing this, adaptive strategies often yield a more intelligent distribution of samples in $\Omega$ and can outperform traditional space-filling designs that spread samples uniformly without considering the response itself.

## MSE-based Strategies and their Limitations

A common approach to adaptive sampling is based on the mean squared error (MSE) of the current surrogate model $\hat{y}(x)$. Because Kriging provides not only a prediction $\hat{y}(x)$ but also an uncertainty measure in terms of MSE, one can select new samples where the predicted MSE is largest. This naturally leads to a strategy that fills gaps in the design, reducing global uncertainty in the surrogate.

For a Kriging surrogate,

$$\text{MSE}[\hat{y}(x)] = \sigma^2 \left\{ 1 - 

\begin{pmatrix} r(x)^T & f(x)^T \end{pmatrix} 

\begin{pmatrix} R & F \\ F^T & 0 \end{pmatrix}^{-1}

\begin{pmatrix} r(x) \\ f(x) \end{pmatrix}

\right\},$$
where $r(x)$ is the correlation vector between $x$ and the sample points, and $F$ is the regression matrix for the trend. The MSE vanishes at existing samples and grows with increasing distance from known data points. As $\|x - X\|$ becomes large, $r(x)$ approaches zero, and the MSE approaches a finite limit related to $\sigma^2$ and the chosen trend.

Selecting new points $x^{(N+1)}$ based on maximum MSE leads to what is essentially a space-filling approach informed by the current surrogate. Such MSE-based selection aims to reduce global uncertainty, benefiting exploration. However, the MSE does not incorporate the actual response values $y_i$, focusing solely on distance-based measures and hyperparameters. This can make MSE a poor local error indicator if the function is highly nonlinear or if certain regions require finer sampling due to complexity rather than just distance from known samples.

## Minimizing Global Error Measures

To refine MSE-based methods, some adaptive strategies minimize integrated or maximum MSE over $\Omega$. For example, the next sample point can be chosen as:

$$x^{(N+1)} = \arg \min_{x \in \Omega} \left\{ \int_\Omega \text{MSE}[\hat{y}^{(N+1)}(x')] dx' \right\}.$$

This integrated MSE (IMSE) approach considers the entire domain and seeks a point that will globally reduce uncertainty most effectively.

Alternatively, a simpler approach is to just pick the point where the MSE is currently highest:

$$x^{(N+1)} = \arg \max_{x \in \Omega} \left\{ \text{MSE}[\hat{y}^{(N)}(x)] \right\}.$$

While easy to implement, this maximum MSE criterion focuses purely on exploration. It places new samples in locations where the model is most uncertain, gradually filling the domain. Although this generally improves global coverage, it can still miss regions where the true response is complex or yields a high approximation error unrelated to sample spacing.

## Cross-Validation for Improved Adaptive Selection

To incorporate information about actual response values, cross-validation (CV) can be employed as an exploitation-based criterion. CV involves temporarily removing a data point $(x^{(i)}, y_i)$ and reconstructing the surrogate $\hat{y}_{-i}(x)$ without it. The difference $|\hat{y}_{-i}(x^{(i)}) - y_i|$ measures how crucial this sample is for modeling the local response. When $|\hat{y}_{-i}(x^{(i)}) - y_i|$ is small, the sample $(x^{(i)}, y_i)$ is somewhat redundant. When it is large, the sample exerts a strong influence on the surrogate in that region.

A local CV-based error estimator can be extended to any point $x \in \Omega$:

$$e(x) = \frac{1}{N} \sum_{i=1}^{N} |\hat{y}_{-i}(x) - \hat{y}(x)|.$$

This measures how sensitive the prediction at $x$ is to the removal of individual samples. Regions where $e(x)$ is large signal that the current surrogate is fragile and overly dependent on certain points, potentially missing critical information about $y(x)$.

However, $e(x)$ often peaks near existing samples. To avoid selecting samples too close to existing ones, the criterion can be modified by multiplying $e(x)$ by the distance to the nearest existing sample:

$$x^{(N+1)} = \arg \max_{x \in \Omega} \{e(x) \cdot \text{dist}(x, X)\}.$$

Alternatively, one can multiply $e(x)$ by the MSE, merging exploration (through MSE) and exploitation (through CV):

$$x^{(N+1)} = \arg \max_{x \in \Omega} \{e(x) \cdot \text{RMSE}[\hat{y}(x)]\}.$$

This combined metric zeroes out at existing sample points and shifts the focus to regions that are both uncertain and underrepresented.

## Practical Challenges and Adaptive Gridding Methods

While the adaptive approach is conceptually appealing, it can be computationally challenging, especially in higher dimensions. Evaluating the MSE or CV-based error indicators at many candidate points $x \in \Omega$ can be costly. The complexity grows with the number of samples $N$ and the dimension $d$. For large $d$, searching through a dense grid of candidate points quickly becomes infeasible.

One practical solution is to apply domain decomposition and adaptive gridding. By splitting $\Omega$ into smaller cells (e.g., forming a regular grid or using adaptive partitioning aligned with the correlation length scales $\frac{1}{\theta_j}$), one can assign a representative error measure $\eta_\zeta$ to each cell $\zeta$. The next samples are then chosen in the cells with the largest error. This reduces the complexity of the search by focusing on a smaller number of cells rather than searching the entire domain continuously.

This adaptive gridding method can be combined with local optimal design criteria, like maximum entropy or local MSE minimization, within each selected cell. The idea is that one first identifies problematic regions on a coarse scale and then refines the sample placement within those regions using a local design criterion.

## Parallelization and Multi-Sample Additions

Adaptive sampling can be parallelized by evaluating multiple new points simultaneously, especially if the expensive response evaluation $y(x)$ can be performed on multiple processors. If parallelization of the expensive computations is limited, adding several new points at once and evaluating them in parallel still reduces overall wall-clock time.
