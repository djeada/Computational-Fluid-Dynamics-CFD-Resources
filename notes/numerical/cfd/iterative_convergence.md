# Iterative Convergence

## Approach to True Solution

- As we get closer to the true solution $u$, errors from linearization and matrix inversion decrease.
- Iterations continue until the residual, a measure of the difference between the current approximation $u_g$ and the true solution $u$, is sufficiently small.

## Residual Definition

The residual $R$ is defined as the root mean square (RMS) value of the difference between $u$ and $u_g$ over the grid:

$$
R \equiv \sqrt{\frac{1}{N} \sum_{i=1}^{N} (u_i - u_{gi})^2}
$$

## Scaling the Residual

- Scaling the residual with the average value of $u$ ensures it is a relative measure rather than an absolute one.
- Example: An unscaled residual of 0.01 might be small if the average value of $u$ is 5000 but large if the average value is 0.1.
- To scale the residual:

$$
R = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (u_i - u_{gi})^2} \left(\frac{N}{\sum_{i=1}^{N} u_i}\right)
$$

## Iterative Process

For a nonlinear 1D example:

- Start with an initial guess at all grid points equal to the left boundary value, i.e., $u_{gi}^{(1)} = 1$.
- During each iteration, update $u_g$ by sweeping from right to left on the grid, updating $u_4, u_3$, and $u_2$.
- Calculate the residual at each step.
- Terminate iterations when the residual falls below $10^{-9}$, the convergence criterion.

## Python Implementation

- Implementing this procedure in Python helps understand the mechanics.
- Graph of residual vs. iteration number:
  - Note the logarithmic scale on the ordinate.
  - The iterative process converges to a residual smaller than $10^{-9}$ in just 6 iterations.
  - More iterations are necessary for more complex problems to achieve convergence.

![Graph of residual vs. iteration number](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/17a1f9b6-1bae-435f-98de-00130dc721dd)

## Solution Comparison

Solutions after 2, 4, and 6 iterations, along with the exact solution:
- Exact solution: $u_{exact} = \frac{1}{x + 1}$
- Solutions for iterations 4 and 6 are indistinguishable on the graph, indicating convergence.
- The converged solution does not agree well with the exact solution due to a coarse grid, resulting in significant truncation error.
- Iterative convergence error is on the order of $10^{-9}$, overshadowed by the truncation error on the order of $10^{-1}$.

![Graph of iteration solutions vs. exact solution](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/007e2ce3-2cd8-4036-b799-4f55c8821eb3)

## Points to Note

- **Understanding Residuals:**
  - Residuals provide insight into the iterative process of solving equations. They help identify if the solution is improving and converging towards a stable state.
  - Monitoring residuals can highlight potential issues such as slow convergence or oscillations, which may require adjustments in solver settings or numerical schemes.

- **Different Residual Definitions:**
  - Various computational codes may use slightly different definitions for the residual. It is crucial to read the documentation of the specific code you are using to understand precisely how the residual is being calculated. This ensures accurate interpretation and comparison of results.

- **Choosing Convergence Criteria:**
  - The convergence criterion for each conservation equation depends on the specific problem and the code being used. It is generally advisable to start with the default values provided in the code. These defaults are usually set based on typical problem requirements and provide a good starting point.
  - After running initial simulations with default values, you may need to adjust these criteria based on the specific needs of your problem. Fine-tuning the convergence criteria can help achieve a balance between computational efficiency and solution accuracy.

- **Scaling and Normalization:**
  - Scaling residuals by relevant quantities (like the average value of the solution) ensures that the residuals are relative measures, making them more meaningful across different scales of problems.
  - Proper normalization of residuals helps in setting appropriate convergence criteria that are neither too stringent nor too lenient.
