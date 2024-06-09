### Adaptive Designs

Adaptive sampling strategies have emerged as a viable alternative to one-stage approaches and have gained significant attention over the past decade. Unlike a-priori designs, in a-posteriori sampling (also called sequential, adaptive, or output-based designs), the design $X$ and the surrogate model $\hat{y}(x)$ are built incrementally. 

#### Initial Design and Model Construction

- **Initial Design**: Start with a small initial design $X(N_0)$ of size $N_0$, often determined by a one-stage approach.
- **Initial Surrogate Model**: Evaluate the response $y(x)$ at all samples $x \in X(N_0)$ and build the initial surrogate model $\hat{y}^{(N_0)}(x)$ based on $X(N_0)$ and $Y(N_0) \in \mathbb{R}^{N_0}$.
  - For Kriging and gradient-enhanced Kriging, this involves hyperparameter estimation and solving the linear Kriging system.

#### Adaptive Sampling Process

- **Stage-wise Update**:
  - At each stage $N_i$, select one or more new samples $x \in \Omega$ using a selection criterion based on the current surrogate model $\hat{y}^{(N_i)}(x)$.
  - Add the new samples to the current design, evaluate the response, and build a new surrogate model $\hat{y}^{(N_{i+1})}(x)$ based on the augmented data $X(N_{i+1})$ and $Y(N_{i+1}) \in \mathbb{R}^{N_{i+1}}$, including a new hyperparameter estimation.

#### Iteration and Termination

- **Iteration**: Continue this process until a predefined maximum number of samples $N_{\text{max}}$ is reached or until an error estimator falls below a certain threshold.
- **Flexibility**: Adaptive strategies are more flexible than one-stage approaches as the total number of samples does not need to be known in advance.

#### Optimal Design and Intelligent Sampling

- **Adaptation to True Response**: Information about the true response $y(x)$ is directly included in the process of finding an optimal design $X$.
- **Problem-Adapted Design**: The design adapts to the specific test case and the research goal, resulting in a more intelligent distribution of samples in the input parameter domain $\Omega \subset \mathbb{R}^d$.
  - Higher concentration of samples in critical regions of $\Omega$ is pursued, reducing the total number of samples $N_{\text{max}}$ compared to space-filling designs.

#### Exploitation and Exploration

- **Exploitation**: Focuses on areas where the current surrogate model predicts the response is optimal.
  - Risk: May converge to a local optimum if the surrogates are not suitable global approximations.
- **Exploration**: Focuses on areas where the approximation error is assumed highest or where a space-filling criterion can be improved.
  - Risk: May require a large number of samples to ensure the global optimum is reached.

#### Balanced Strategy

- **Mixed Strategy**: Combines exploitation and exploration to ensure efficient convergence to the global optimum.
  - Ensures accuracy of the surrogate model and efficient use of expensive response evaluations.
  - Samples are distributed densely in critical regions while maintaining a global coverage.

### Algorithm for Efficient Global Optimization (EGO)

- **Expected Improvement Criterion**: An algorithm based on this criterion was presented receiving significant attention and subsequent enhancements.
- **Surveys and Applications**: Detailed surveys on adaptive sampling strategies for optimization and recent applications in various fields are available.

### Notable Approaches and Studies

- **IMSE Criterion**: Used for adaptive refinement in global approximation methods.
- **Model-Based Criteria**: Used for updating Kriging surrogates adaptively.
- **Cross-Validation Approaches**: Introduced to measure local errors and compared to model-based and distance-based adaptive designs.
- **Adaptive Maximum Entropy Designs**: Adjust entries of the correlation matrix based on observed irregularities.
- **Adaptive Gridding and Voronoi Tessellation**: Used for regular partitioning of the input parameter domain.
- **Active Learning**: Discussed for designs based on nonstationary Gaussian processes.
- **Optimal Design Extraction**: Investigated for designs based on dense validation sets and their distribution relative to local complexity and error estimators.

#### MSE-based Strategies

The Mean Squared Error (MSE) $\hat{y}(x)$ is a measure of the uncertainty in prediction, making it an intuitive selection criterion for adaptive sampling. The MSE is zero at each $x^{(i)} \in X$ and increases with distance from the existing samples. The expanded expression for MSE is:


$$ \text{MSE} [\hat{y}(x)] = \sigma^2 \left\{ 1 - \begin{pmatrix} r(x)^T & f(x)^T \end{pmatrix} \begin{pmatrix} R & F \\ F^T & 0 \end{pmatrix}^{-1} \begin{pmatrix} r(x) \\ f(x) \end{pmatrix} \right\} $$



$$ = \sigma^2 \left\{ 1 - \begin{pmatrix} r(x)^T & f(x)^T \end{pmatrix} \begin{pmatrix} \Lambda(x) \\ \mu(x) \end{pmatrix} \right\} $$



$$ = \sigma^2 \left\{ 1 - r(x)^T \Lambda(x) - f(x)^T (F^T R^{-1} F)^{-1} (F^T R^{-1} r(x) - f(x)) \right\}, $$


As the distance to existing samples increases ($\text{dist}(x, X) \rightarrow \infty$), $r(x)$ approaches zero and the MSE approaches $\sigma^2 (1 + f(x)^T (F^T R^{-1} F)^{-1} f(x))$. Notably, its computation does not directly involve $y$.

Model-based criteria such as MMSE and IMSE can be applied in adaptive sampling:

- **MMSE-based Sampling**: The new sample is chosen to minimize the maximum MSE of the new surrogate:

  
$$ x^{(N+1)} = \arg \min_{x \in \Omega} \left\{ \max_{x' \in \Omega} \text{MSE} [\hat{y}^{(N+1)} (x')] \right\}.  $$


- **IMSE-based Sampling**: The new sample is chosen to minimize the integrated MSE of the new surrogate:

  
$$ x^{(N+1)} = \arg \min_{x \in \Omega} \left\{ \int_{\Omega} \text{MSE} [\hat{y}^{(N+1)} (x')] dx' \right\}. \tag{3.15} $$


A simpler approach for selecting a new sample is to choose the point with the maximum predicted MSE of the current surrogate:


$$ x^{(N+1)} = \arg \max_{x \in \Omega} \left\{ \text{MSE} [\hat{y}^{(N)} (x)] \right\}.  $$


Given that MSE($y^{(N+1)} | y(x^{(N+1)}) = 0$), choosing $x^{(N+1)}$ where MSE($\hat{y}^{(N)} (x)$) is largest will likely decrease both MMSE and IMSE scores of $\hat{y}^{(N+1)}$. This approach is related to maximum entropy designs, where the objective is to maximize the entropy of the dataset $X^{(N+1)} = X^{(N)} \cup \{ x^{(N+1)} \}$.

### Limitations of MSE-based Sampling

- **Poor Local Error Indicator**: The MSE does not include the response $y$ directly, making it a poor local error indicator. It provides a global measure of uncertainty via hyperparameters $\theta$.
- **Example Illustration**: Kriging interpolation $\hat{y}(x)$ of the Branin function shows that RMSE[$\hat{y}(x)$] fails to identify regions of high real error. The RMSE is primarily a distance-based measure weighted by the correlation function $R(||x - x^{(i)}||, \theta)$.

Selecting a new sample based on the highest predicted RMSE aims at a space-filling design. However, in each stage of the sequential process, the distance measure is based on the current surrogate model and hyperparameters $\theta$, making it a pure exploration method.

#### Cross-Validation-Based Strategies

Cross-validation is introduced as an exploitation criterion for adaptive sampling, allowing for a mixed strategy between exploration and exploitation. Kriging and gradient-enhanced Kriging are used as interpolators of the data $Y \in \mathbb{R}^N$. However, the assessment of approximation error in $\Omega \setminus X$ based on RMSE performs poorly, as discussed in Section 3.2.1. Cross-validation provides a method of estimating error by comparing predictions based on a reduced dataset to the existing data $Y$.

### Leave-One-Out Cross-Validation Error

- **Kriging Predictor**: Let $\hat{y}_{-i}(x)$ denote the Kriging predictor based on $X \setminus \{ x^{(i)} \}$.
- **Fixed Hyperparameters**: Keeping the hyperparameters $\theta$ of $g$ fixed, $\hat{y}_{-i}(x)$ can be computed by deleting the i-th column and row of the system matrix and the i-th entries of the vectors in the Kriging equation.
- **Gradient-Enhanced Kriging**: All $(kd + i)$-columns and rows of the system matrix and all $(kd + i)$-th vector entries are deleted.
- **Error Definition**: The leave-one-out cross-validation error for sample $x^{(i)}$ is defined by:

  
$$ e_i = \left| \hat{y}_{-i} (x^{(i)}) - y_i \right| \tag{3.17} $$


- **Error Estimator**: An error estimator can be evaluated by:

  
$$ \hat{e} = \frac{1}{N} \sum_{i=1}^N e_i \quad \text{or} \quad \hat{e} = \frac{1}{N} \sum_{i=1}^N e_i^2 $$


### Local Error Estimator for Adaptive Sampling

For adaptive sampling, a local error estimator is needed, which can be evaluated at arbitrary candidates $x \in \Omega$. The cross-validation error $e_i$ measures the influence of the data pair $(x^{(i)}, y_i)$ on the prediction $\hat{y}(x)$.

- **Low $e_i$**: $(x^{(i)}, y_i)$ is redundant; no additional samples are needed near $x^{(i)}$.
- **High $e_i$**: $(x^{(i)}, y_i)$ is crucial for $\hat{y}(x)$; indicates critical regions with large gradients or high curvature in $y(x)$.

### Extension to the Entire Domain

The concept of cross-validation is extended to $\Omega$:


$$ e(x) := \frac{1}{N} \sum_{i=1}^N \left| \hat{y}_{-i} (x) - \hat{y}(x) \right|.  $$


### Practical Selection Criterion

Choosing $x^{(N+1)}$ where the predicted error $e(x)$ is highest can be impractical because it tends to be highest near existing samples $x^{(i)}$. To address this, $e(x)$ can be multiplied by a minimum distance function $\text{dist}(x, X)$, ensuring the product is zero at every $x^{(i)} \in X$:


$$ x^{(N+1)} = \arg \max_{x \in \Omega} \left\{ e(x) \text{dist}(x, X) \right\}  $$


Another approach multiplies $e(x)$ with the root mean square error RMSE[$\hat{y}(x)$] and is called a mixed sample sensitivity error strategy:


$$ x^{(N+1)} = \arg \max_{x \in \Omega} \left\{ e(x) \text{RMSE} [\hat{y}(x)] \right\} $$


### Illustration and Application

- **Example**: Using the Kriging interpolation of the Branin function, the cross-validation error $e(x)$ indicates regions of high error but is maximal at existing samples.
- **Mixed Strategy**: Multiplying $e(x)$ with RMSE sets the error indicator to zero at existing samples, correctly identifying regions with the highest real error.

#### Adaptive Gridding

The methods from previous sections have limitations regarding efficiency, especially when dealing with a high number of input parameters $d$. Even though the evaluation of the computer experiment $y(x)$ dominates the cost of surrogate model generation, finding a new sample $x^{(N+1)} \in \Omega \subset \mathbb{R}^d$ can be a bottleneck if $d$ is large. Both MSE-based and cross-validation-based methods require global optimization of a target function over $\Omega$.

### Computational Complexity

- **MSE Evaluation**: After inverting the system matrices once, the numerical effort for computing MSE[$\hat{y}(x)$] is $O(N^2 d)$.
- **Cross-Validation Error**: For $e(x)$, the complexity is $O(N^2)$.
- **Gradient-Enhanced Kriging**: The complexity increases to $O(N^2 d^2)$ for MSE and $O(N^2 d)$ for cross-validation error.

### Challenges with High Dimensionality

For example, in an application with $d = 6$ variables, and candidates for $x^{(N+1)}$ located on a $50^6$-tensor grid, there would be $1.5625 \times 10^{10}$ evaluations required, making the process computationally infeasible.

### Parallelization for Efficiency

Practitioners might want to add more than one new sample per stage. Adding $m$ new samples $x^{(N+1)}, \ldots, x^{(N+m)}$ can be parallelized, reducing total wall-clock time. This is beneficial if the parallelization of $y(x)$ scales poorly with the number of available processors.

### Adaptive Gridding Method

a new method combining domain decomposition with local optimal design was introduced to overcome these limitations. The method involves:

1. **Domain Decomposition**: Decompose $\Omega$ into equal-sized cells $\zeta$.
   - Assume $\Omega$ is a hypercuboid, e.g., $\Omega = [0, 1]^d$.
   - Decompose into cells via equidistant partitioning of intervals $I_j = [0, 1]$ along the $x_j$-axis.
   - Define cells:

     
$$ \zeta_{i_1, \ldots, i_d} := I_{i_1}^1 \times \cdots \times I_{i_d}^d $$


     
$$ \Omega = \bigcup_{i_1 = 1}^{n_1} \cdots \bigcup_{i_d = 1}^{n_d} \zeta_{i_1, \ldots, i_d}$$


   - Lengths of intervals are $|I_j^i| = \frac{1}{n_j}$ for each $j$.

2. **Adaptive Gridding**: Make the gridding adaptive by choosing cell edge lengths proportional to the correlation length $\frac{1}{\theta_j}$ along the $x_j$-axis:

   
$$ |I_j^i| \approx \frac{1}{\theta_j} $$


   
$$ n_j \approx \theta_j |I_j| $$


   
$$ n_j = \left\lceil c \theta_j |I_j| \right\rceil  $$


3. **Assign Cell Prediction Error**: Assign a prediction error $\eta_\zeta$ to each cell using cross-validation:

   
$$ \eta_\zeta = \max_{x \in \Omega_\zeta} \left| \hat{y}_{-i} (x^{(i)}) - y_i \right|  $$


   - If $X_\zeta = \emptyset$, set $\eta_\zeta = \eta_{max}$.

### Adding New Samples

- Define a target accuracy $\eta^* < \eta_{max}$.
- Add one new sample in each cell $\zeta$ with $\eta_\zeta > \eta^*$.
- Alternatively, sort cells by $\eta_\zeta$ and add new samples in the $m$ worst cells.
- Use a local optimal design criterion to select new samples, e.g., maximum entropy criterion:

  
$$ x^{(N+1)} = \arg \max_{x \in \zeta_i} \left[ \text{MSE} [\hat{y}(x)] \right] \quad (i = 1, \ldots, m)  $$


### Mixed Strategy

The adaptive gridding method combines exploration and exploitation:

- **Exploration**: Domain decomposition adds an exploration component.
- **Exploitation**: Cross-validation-based error estimators add an exploitation component.

