# Surrogate Models in CFD

Surrogate models, also known as metamodels, play a pivotal role in modern computational fluid dynamics (CFD), enabling engineers and scientists to approximate the behavior of complex fluid systems at a fraction of the computational cost of full-scale numerical simulations. By replacing expensive CFD computations with fast-to-evaluate approximations, surrogate models facilitate rapid design optimization, uncertainty quantification, sensitivity analysis, inverse problems, and real-time decision-making in fluid engineering applications.

As high-fidelity CFD simulations—such as those solving the Navier-Stokes equations in three dimensions and complex geometries—can require thousands to millions of CPU-hours, reducing this computational burden becomes a priority. Surrogate models address this challenge by learning from a limited set of sampled CFD results and then predicting flow fields, integral quantities, or performance metrics without re-running the full CFD solver. They form the backbone of simulation-driven engineering, allowing iterative processes that would otherwise be intractable within given time or resource constraints.

## The Need for Surrogate Models in CFD

### Complexity of CFD Simulations

CFD involves discretizing and numerically approximating the governing partial differential equations (PDEs) of fluid flow, typically the Navier-Stokes equations (for Newtonian fluids) or more specialized sets of equations depending on the flow physics. For incompressible, Newtonian flows, the Navier-Stokes equations are:

$$\nabla \cdot \mathbf{u} = 0,$$

$$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{f},$$

where $\mathbf{u}$ is the velocity field, $p$ is pressure, $\rho$ is fluid density, $\nu$ is kinematic viscosity, and $\mathbf{f}$ are body forces. The complexity escalates for turbulent flows, reacting flows, multiphase flows, and flows through complex geometries. High-fidelity simulations (e.g., Direct Numerical Simulation, Large Eddy Simulation) involve fine spatial-temporal resolutions and advanced turbulence modeling, making single runs expensive.

### High-Dimensional Parameter Spaces

In engineering design and analysis, the fluid’s behavior may depend on numerous parameters, such as boundary conditions, geometric parameters (shape of an airfoil, configuration of a heat exchanger), operating conditions (Reynolds number, Mach number), and material properties. Exploring this high-dimensional design space with brute-force CFD is prohibitive. Instead, a limited set of carefully chosen CFD runs is used to build a surrogate model that approximates the relationship:

$$x \in \mathbb{R}^d \rightarrow y(x) \in \mathbb{R}^m,$$

where $x$ is the input parameter vector (e.g., geometric shape parameters, inflow velocity) and $y(x)$ represents the output of interest (e.g., lift and drag coefficients, pressure drop, flow rate, heat transfer coefficient, or even an entire field distribution).

### Accelerating Engineering Workflows

Once a surrogate is constructed, it can be evaluated in milliseconds rather than hours or days. This acceleration enables:
- Rapid optimization loops using gradient-based or evolutionary algorithms.
- Robust uncertainty quantification and probabilistic analysis.
- Real-time predictions for digital twins and operational monitoring systems.

## Types of Surrogate Models

A wide range of surrogate modeling techniques can be employed, each with its strengths and limitations. Common classes include:

I. **Polynomial Response Surfaces**:
- Approximate $y(x)$ with low-order polynomials (e.g., linear or quadratic forms).  
- Advantage: Simplicity and interpretability.
- Disadvantage: May struggle with complex, nonlinear responses and high-dimensionality.
II. **Kriging or Gaussian Process Regression (GPR)**:
- Model responses as realizations of a Gaussian process with mean and covariance functions.
- Provides not only predictions but also estimates of predictive uncertainty.
- Often used in global optimization frameworks (e.g., Efficient Global Optimization).
- Well-suited for moderate dimensions and smoothly varying functions.
III. **Radial Basis Functions (RBF)**:
- Use basis functions centered on training points. For a set $\{x^{(i)}, y^{(i)}\}_{i=1}^N$, the RBF surrogate is:

 $$\hat{y}(x) = \sum_{i=1}^N w_i R(\|x - x^{(i)}\|),$$
 where $R$ is a radially symmetric kernel (e.g., Gaussian, multiquadric).
- Flexible and can handle scattered data in any dimension.
- Hyperparameter tuning (e.g., scaling factors) is essential.
IV. **Neural Networks (NNs)**:
- Universal function approximators. Deep neural networks can capture highly nonlinear and complex relationships.
- Convolutional neural networks (CNNs) or graph-based NNs may be used if dealing with field data on a mesh.
- Require more training data and careful architecture selection and regularization.
V. **Support Vector Regression (SVR)**:
- Forms a sparse kernel-based model. Good for moderate-sized datasets.
- May be outperformed by GPR or NNs in certain complex scenarios.
VI. **Surrogate Models from Reduced-Order Modeling (ROM)**:
- Use techniques like Proper Orthogonal Decomposition (POD), Dynamic Mode Decomposition (DMD), or Autoencoders to build reduced-order representations of the flow fields.
- Then fit a simpler mapping from parameters to the reduced coefficients, enabling fast reconstructions of flow fields.

## Building a Surrogate Model: Detailed Steps

### 1. Problem Definition and Input Parameterization

- Define the input domain $\Omega \subset \mathbb{R}^d$. This might represent geometric variation (e.g., shape variables of an airfoil), operating conditions (inflow velocity, angle of attack), or environmental parameters.
- Determine output quantities of interest (QoI) such as lift coefficient $C_L$, drag coefficient $C_D$, or temperature distribution at a set of probe points.

### 2. Sampling Strategy

- Choose a one-stage or adaptive sampling plan to select training points $\{x^{(i)}\}_{i=1}^N$.
- Space-filling designs (e.g., Latin Hypercube Sampling) or low-discrepancy sequences are commonly used initially.
- Ensure sufficiently many samples to represent the complexity of $y(x)$. If $N$ is too small, the surrogate may underfit.

### 3. High-Fidelity Data Generation (Running CFD)

- Run the CFD simulations at each chosen input $x^{(i)}$.
- Solving the Navier-Stokes equations numerically (via finite volume, finite element, or finite difference methods) yields flow fields and integrated quantities.
- Store $y^{(i)} = y(x^{(i)})$ as training data. This step is usually the computational bottleneck.

### 4. Model Selection

- Consider complexity, available data, dimensionality, and desired properties (e.g., smoothness, uncertainty estimates) to select the model type.
- For well-studied aerodynamic shape optimization, Kriging might be popular due to uncertainty quantification. For big data from parametric studies, neural networks might be better.

### 5. Model Fitting or Training

- Fit the chosen surrogate model by determining its parameters:
- Polynomial regression: Solve a least-squares problem.
- Kriging: Estimate hyperparameters $\theta$ by maximizing the likelihood:

$$\hat{\theta} = \arg\max_{\theta} L(\theta | Y).$$
- Neural networks: Use stochastic gradient descent to minimize a loss function (e.g., mean squared error):

$$\min_{w,b} \sum_{i=1}^N \|y^{(i)} - \hat{y}(x^{(i)}; w,b)\|^2,$$
where $w,b$ are weights and biases.

- Regularization and cross-validation are crucial to prevent overfitting. For Kriging, a nugget term may be added for noisy data. For NNs, use dropout or weight decay.

### 6. Validation and Error Assessment

- Hold out a portion of data or use k-fold cross-validation.
- Compute error metrics: Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), or $R^2$-score.
- In CFD contexts, also consider checking how well the surrogate captures known flow physics. For instance, does the predicted $C_L$ vs. angle-of-attack curve match the expected stall behavior?
- If the model is unsatisfactory, adjust the model type, add more training data, or improve sampling coverage.

### 7. Deployment and Use

- Once validated, apply the surrogate model in optimization loops:
- Use gradient-based methods if the surrogate is differentiable.
- Use global optimization (e.g., genetic algorithms) to find optimal parameters for flow performance.
- For uncertainty propagation, sample the surrogate repeatedly to estimate probability distributions of QoI under uncertain inputs.
- Integrate the surrogate in real-time systems where quick responses are needed.

## Example Application in Aerodynamic Design

Consider an airfoil shape characterized by a set of parameters $x \in \mathbb{R}^d$ that control the thickness, camber, or leading-edge radius. We want to predict the lift and drag coefficients $(C_L, C_D)$.

I. **Sampling**:
- Let $d=5$ parameters define the airfoil shape.
- Generate $N=50$ samples using Latin Hypercube Sampling in $[0,1]^5$.
II. **CFD Data Generation**:
- For each $x^{(i)}$, run a steady-state RANS solver with a chosen turbulence model (e.g., $k-\omega$ SST).
- Extract $C_L^{(i)}$ and $C_D^{(i)}$.
III. **Model Selection**:
- Pick Kriging as it can handle moderate datasets well and provides uncertainty estimates.
IV. **Model Fitting**:
- Estimate Kriging hyperparameters $\theta$ by maximizing the log-likelihood. Solve:

 $$\hat{\theta} = \arg\max_{\theta} \left(-\frac{N}{2}\log(2\pi\sigma^2(\theta)) - \frac{1}{2}\log(\det(R(\theta))) - \frac{1}{2\sigma^2(\theta)}(Y - F\beta)^TR(\theta)^{-1}(Y - F\beta)\right),$$
 where $R(\theta)$ is the correlation matrix, $F$ is the regression matrix, and $Y$ contains $[C_L, C_D]$ values.

V. **Validation**:
- Reserve 10% of data for validation.
- Compute error metrics: Suppose RMSE in $C_L$ is 0.005, and in $C_D$ is 0.001—both acceptable for preliminary design purposes.
VI. **Use**:
- Use the surrogate in an optimization loop (e.g., genetic algorithm) to find the shape $x$ that maximizes $C_L/C_D$ ratio.
- Since evaluations are now instantaneous, thousands of trial configurations can be tested within minutes rather than days.

## Comparisons with Other Numerical Methods

I. **Direct CFD vs. Surrogate**:
- Direct CFD: Highly accurate but computationally expensive per evaluation.
- Surrogates: Fast but approximate. Accuracy depends on training data quality and chosen model.
II. **Reduced-Order Models (ROMs)**:
- ROMs focus on reducing the PDE system dimension itself, whereas surrogates directly approximate input-output mappings.
- Often combined: ROM can supply low-dimensional features that a surrogate can quickly map to parameters.
III. **Adjoint-Based Methods**:
- For design optimization, adjoint methods compute gradients efficiently.
- Surrogates facilitate global exploration, not just local gradients. They can complement adjoint methods by guiding initial search directions or supporting robust optimization under uncertainty.

## Advanced Topics and Current Research Directions

I. **Multi-Fidelity Surrogate Modeling**:
- Combine data from high-fidelity (expensive) and low-fidelity (cheaper but less accurate) simulations.
- Co-Kriging or hierarchical surrogate models leverage correlations between fidelity levels to improve accuracy at reduced cost.
II. **Active Learning and Adaptive Sampling**:
- Instead of fixed one-stage sampling, adaptively choose new sample points where the surrogate is uncertain or potentially inaccurate.
- Iterative improvement leads to better surrogates with fewer samples.
III. **Physics-Informed Surrogates**:
- Embed known physical constraints or PDE residual information into the surrogate.
- Physics-informed neural networks or constrained Kriging ensure predictions respect fundamental fluid equations, improving reliability.
IV. **High-Dimensional Parameter Spaces and Dimensionality Reduction**:
- Use manifold learning or POD to reduce parameter dimensionality.
- Simplify the surrogate construction by approximating $y(x)$ on a low-dimensional subspace of the design space.

## Further Reading and Resources

I. **Books**:

- Koziel, S., Leifsson, L. (eds.): "Surrogate-Based Modeling and Optimization"
- Forrester, A., Sobester, A., Keane, A.: "Engineering Design via Surrogate Modelling"

II. **Review Articles and Papers**:

- Simpson, T.W., Peplinski, J.D., Koch, P.N., Allen, J.K.: "Metamodels for Computer-Based Engineering Design"
- Forrester, A.I.J., Keane, A.J.: "Recent Advances in Surrogate-Based Optimization"
- Yarlanki, S., Chen, W., and Balaras, E.: "Surrogate-based uncertainty quantification and robust design"

III. **Software and Implementations**:

- Python libraries: `scikit-learn` for GPR, SVR, and NNs; `GPy` for Gaussian Processes; specialized ROM libraries.
- R packages: `DiceKriging` for Kriging, `mlegp` for Gaussian processes.
- Custom scripts integrating CFD solvers (like OpenFOAM) with surrogate model toolboxes.
