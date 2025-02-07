# Iterative Convergence

## Approach to True Solution

- As we get closer to the true solution $u$, the errors from both linearization and matrix inversion diminish.
- The iterative process continues until the residual—a measure of the difference between the current approximation $u_g$ and the true solution $u$—becomes sufficiently small.
- This makes sure that the final approximation is an accurate representation of the true solution.

## Residual Definition

The residual $R$ is defined as the root mean square (RMS) of the difference between the true solution $u$ and the current guess $u_g$ over all grid points:

$$R \equiv \sqrt{\frac{1}{N} \sum_{i=1}^{N} (u_i - u_{gi})^2}$$

- Here, $N$ is the total number of grid points.
- The residual quantifies the overall error in the current solution approximation.

## Scaling the Residual

- Scaling the residual with the average value of $u$ transforms it into a relative measure, which is often more meaningful than an absolute error.
- For example, an unscaled residual of 0.01 might be insignificant if the average $u$ is 5000 but important if the average $u$ is only 0.1.
- The scaled residual is defined as:
$$R = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (u_i - u_{gi})^2} \left(\frac{N}{\sum_{i=1}^{N} u_i}\right)$$

- This normalization makes sure that the convergence criterion adapts to the magnitude of the solution.

## Iterative Process

For a nonlinear 1D example, the iterative process follows these steps:

- Initial Guess:  
Begin by setting the initial guess at all grid points equal to the left boundary value, for example, $u_{gi}^{(1)} = 1$.

- Update Strategy:  
In each iteration, update the guess $u_g$ by sweeping through the grid (typically from right to left), sequentially updating points (e.g., updating $u_4$, then $u_3$, and finally $u_2$).

- Residual Calculation:  
After each sweep, compute the residual $R$ using the formula above to measure the error between the current solution and the guess.

- Convergence Criterion:  
Continue the iterations until the residual falls below a threshold (for example, $10^{-9}$). This indicates that further iterations yield insignificant changes.

## Python Implementation

Carrying out this iterative procedure in Python is an excellent way to understand the mechanics of convergence. A typical implementation would:

- Initialize the grid and guess values.
- Iterate through a loop where the solution is updated according to the chosen finite-difference scheme.
- Compute and record the residual at each iteration.
- Plot the residual versus iteration number to visualize convergence.
Below is a representative graph showing the residual versus iteration number. Notice the logarithmic scale on the ordinate (y-axis). In this example, the iterative process converges to a residual smaller than $10^{-9}$ in just 6 iterations.

![Graph of residual vs. iteration number](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/17a1f9b6-1bae-435f-98de-00130dc721dd)

## Solution Comparison

The following comparison demonstrates the convergence of the iterative process:

- Exact Solution:  
The exact solution is given by $u_{\text{exact}} = \frac{1}{x + 1}$.

- Iterative Solutions:  
Solutions obtained after 2, 4, and 6 iterations are plotted alongside the exact solution.

- Observation:  
The solutions after 4 and 6 iterations are indistinguishable on the graph, indicating that convergence has been achieved.

- Accuracy Note:  
Although the iterative convergence error is on the order of $10^{-9}$, the overall error is dominated by the truncation error (on the order of $10^{-1}$) due to the coarse grid resolution.

![Graph of iteration solutions vs. exact solution](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/007e2ce3-2cd8-4036-b799-4f55c8821eb3)

## Points to Note

Understanding Residuals:
- Residuals are a key diagnostic tool in iterative solvers, providing insight into how close the current solution is to the true solution.
- Monitoring the residual helps identify issues like slow convergence or oscillatory behavior, prompting adjustments in solver settings or numerical schemes.

Different Residual Definitions:
- Various CFD codes may use different definitions of the residual. It is important to consult the documentation for the specific code to understand the formulation used, making sure proper interpretation and comparison of results.

Choosing Convergence Criteria:
- The convergence criteria for each conservation equation should be chosen based on the specific problem and code. Starting with default values is often a good idea, but these may need fine-tuning for higher accuracy or efficiency.
- Adjusting the criteria based on initial simulation results can help balance computational cost and solution accuracy.

Scaling and Normalization:
- Proper scaling of the residual makes sure that it is a relative measure, making it meaningful across different problems and solution magnitudes.
- Normalizing the residual helps in setting appropriate convergence thresholds that are neither too strict nor too lenient.
