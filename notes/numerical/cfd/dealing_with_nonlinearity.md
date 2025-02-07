# Dealing with Nonlinearity

The highly nonlinear nature of the governing equations for fluid flow makes obtaining accurate numerical solutions for complicated flows challenging. In Computational Fluid Dynamics (CFD), the nonlinearities often arise from convective terms, turbulence models, or nonlinear source terms. Understanding and handling nonlinearity is important because it directly affects the stability, accuracy, and convergence of numerical solvers. This section explains how nonlinearity can be managed via linearization and iterative solution techniques.

## Demonstrating the Effect of Nonlinearity

Consider a simple one-dimensional (1D) example with a nonlinear term. The governing differential equation is given by:

$$\frac{du}{dx} + u^2 = 0; \quad 0 \le x \le 1; \quad u(0) = 1$$

This equation is nonlinear due to the $u^2$ term. When discretizing the problem using a finite-difference method, we approximate the derivative at a grid point $x_i$ by

$$\frac{u_i - u_{i-1}}{\Delta x}$$

resulting in the discrete equation

$$\frac{u_i - u_{i-1}}{\Delta x} + u_i^2 = 0$$

The presence of $u_i^2$ makes this a nonlinear algebraic equation at each grid point, meaning that standard linear solution techniques cannot be applied directly. Instead, we must handle the nonlinearity—typically via linearization—before proceeding with an iterative solution.

## Linearization Strategy

A common approach for dealing with nonlinear equations in CFD is to linearize them about an initial guess and then solve the resulting linear equations iteratively until convergence. This strategy is central to methods like the Newton–Raphson algorithm and many of its variants.

### Steps for Linearization

I. Initial Guess:

- Assume an initial guess for the solution at the grid point, denoted as $u_{ig}$ (the subscript “g” stands for "guess"). The choice of $u_{ig}$ can be based on physical intuition, previous solutions, or even a simple constant value.

II. Define the Perturbation:

- Define the difference between the true solution $u_i$ and the guess $u_{ig}$ as:
 $$\Delta u_i = u_i - u_{ig}$$

III. Expand and Approximate:

- Substitute $u_i = u_{ig} + \Delta u_i$ into the nonlinear term. Squaring the expression yields:
 $$u_i^2 = (u_{ig} + \Delta u_i)^2 = u_{ig}^2 + 2u_{ig}\Delta u_i + (\Delta u_i)^2$$

- If the perturbation $\Delta u_i$ is small compared to $u_{ig}$, then $(\Delta u_i)^2$ is insignificant. This is a standard assumption in linearization procedures, which leads to:
 $$u_i^2 \approx u_{ig}^2 + 2u_{ig}\Delta u_i$$

- Expressing $\Delta u_i$ in terms of $u_i$ and $u_{ig}$ gives:
 $$u_i^2 \approx u_{ig}^2 + 2u_{ig}(u_i - u_{ig})$$

IV. Simplify the Expression:

- Simplify the expression further to obtain a linear form in $u_i$:
 $$u_i^2 \approx 2u_{ig} u_i - u_{ig}^2$$

V. Linearized Finite-Difference Approximation:

- Substitute the linearized expression for $u_i^2$ back into the finite-difference approximation:
 $$\frac{u_i - u_{i-1}}{\Delta x} + 2u_{ig} u_i - u_{ig}^2 = 0$$

This linearization transforms the originally nonlinear finite-difference equation into a linear equation in terms of $u_i$, which can then be solved using standard linear solvers.

### Error Analysis

- The error introduced by neglecting the $(\Delta u_i)^2$ term is of order $O((\Delta u_i)^2)$. As the iterative process proceeds and $u_{ig}$ converges to the true solution $u_i$, the perturbation $\Delta u_i$ decreases, rendering the linearization error insignificant. This error analysis justifies the iterative refinement process.

## Iterative Solution Process

Since the linearization is based on an initial guess, the solution must be refined iteratively. The overall approach is to repeatedly update the guess and solve the linearized equations until the solution converges to within a prescribed tolerance.

### Iterative Scheme

I. Iteration 1:  

- Start with an initial guess $u_i^{(1)}$ for each grid point.

II. Iteration 2:  

- Use the solution from the previous iteration as the new guess: $u_i^{(2)} = u_i^{(1)}$.

III. Iteration 3 and Beyond:  

- Continue updating using:
 $$u_i^{(n)} = u_i^{(n-1)}$$

 while re-linearizing the nonlinear term around the latest guess at each iteration.

IV. Convergence Check:  

- After each iteration, compare the new solution $u_i^{(n)}$ with the previous one $u_i^{(n-1)}$. If the difference (measured by an appropriate norm) is less than a specified tolerance, the solution is considered converged.
The iterative process makes sure that the approximation gradually improves, reducing the error introduced by the initial linearization and finally providing a solution that satisfies the nonlinear equation.

## Convergence

Convergence is a important aspect of the iterative solution process. It makes sure that the numerical solution becomes both stable and accurate as the iterations progress.

- Convergence Check:  
A common practice is to compute the residual (the difference between the left- and right-hand sides of the equation) or the difference between successive iterates. When these quantities fall below a predefined threshold, the solution is deemed converged.

- Criteria for Convergence:  
Convergence is typically assessed using norms (e.g., the $L_2$ norm) of the error:

$$\|u^{(n)} - u^{(n-1)}\| < \epsilon$$

where $\epsilon$ is the tolerance level.

- Importance of Convergence:  
- Accuracy: Convergence guarantees that the computed solution accurately represents the physical problem and satisfies the governing equations.
- Efficiency: Setting up a clear convergence criterion prevents unnecessary iterations, saving computational resources.
- Stability: A well-converged solution is generally more stable and reliable, reducing the risk of numerical instabilities in further calculations or coupled simulations.

### Steps in the Iterative Solution Process

I. Initial Guess:  

- Begin with an initial guess $u_i^{(1)}$ that is as close as possible to the expected solution. A good initial guess can greatly reduce the number of iterations needed.

II. Linearization:  

- Linearize the nonlinear term around the current guess $u_{ig}$ using the steps outlined above.

III. Update the Solution:  

- Solve the resulting linear equation to obtain an updated solution $u_i^{(n)}$.

IV. Check Convergence:  

- Compare the new solution with the previous iteration. If the difference is below the specified tolerance, the solution has converged.

V. Iterate:  

- If convergence is not achieved, use $u_i^{(n)}$ as the new guess and repeat the linearization and solution process.

### Importance of Convergence

- Accuracy:  
A converged solution means that the linearization error is minimized and the numerical solution accurately reflects the underlying physical phenomena.

- Efficiency:  
By setting up strong convergence criteria, the iterative process avoids unnecessary computations, thereby optimizing the use of computational resources.

- Stability:  
Convergence is often associated with numerical stability. A solution that has converged within a tight tolerance is less likely to exhibit erratic behavior, making sure that the results are both reliable and reproducible.
