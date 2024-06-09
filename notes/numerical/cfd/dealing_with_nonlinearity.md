# Dealing with Nonlinearity

The highly nonlinear nature of the governing equations for fluid flow makes obtaining accurate numerical solutions for complex flows challenging. Understanding and handling nonlinearity is crucial in Computational Fluid Dynamics (CFD).

## Demonstrating the Effect of Nonlinearity

Consider the equation with $m = 2$ in a simple 1D example:

$$
\frac{du}{dx} + u^2 = 0; \quad 0 \le x \le 1; \quad u(0) = 1
$$

A first-order finite-difference approximation to this equation is:

$$
\frac{u_i - u_{i-1}}{\Delta x} + u_i^2 = 0
$$

Here, the term $u_i^2$ introduces nonlinearity, resulting in a nonlinear algebraic equation.

## Linearization Strategy

To handle nonlinearity, we linearize the equations around an initial guess value of the solution and iterate until the guess aligns with the solution within a specified tolerance level.

### Steps for Linearization

1. **Initial Guess**:
   - Let $u_{ig}$ be the initial guess for $u_i$.

2. **Define the Perturbation**:
   - Define the perturbation as $\Delta u_i = u_i - u_{ig}$.

3. **Expand and Approximate**:
   - Squaring the perturbation expression:
   
$$
u_i^2 = u_{ig}^2 + 2u_{ig} \Delta u_i + (\Delta u_i)^2
$$
   
   - Assuming $\Delta u_i \ll u_{ig}$, the term $(\Delta u_i)^2$ is small and can be neglected, yielding:
   
$$
u_i^2 \simeq u_{ig}^2 + 2u_{ig} \Delta u_i = u_{ig}^2 + 2u_{ig} (u_i - u_{ig})
$$

4. **Simplify the Expression**:
   - Simplify to get:
   
$$
u_i^2 \simeq 2u_{ig} u_i - u_{ig}^2
$$

5. **Linearized Finite-Difference Approximation**:
   - Substitute back into the finite-difference approximation (11):
   
$$
\frac{u_i - u_{i-1}}{\Delta x} + 2u_{ig} u_i - u_{ig}^2 = 0
$$

### Error Analysis

- The error due to linearization is $O(\Delta u_i^2)$, which becomes negligible as $u_{ig}$ converges to $u$.

## Iterative Solution Process

To calculate the finite-difference approximation, we need guess values $u_{ig}$ at the grid points. The process is iterative:

1. **Iteration 1:** $u_i^{(1)} = \text{Initial guess}$
2. **Iteration 2:** $u_i^{(2)} = u_i^{(1)}$
3. **Iteration 3:** $u_i^{(3)} = u_i^{(2)}$
4. **...**
5. **Iteration $n$:** $u_i^{(n)} = u_i^{(n-1)}$

The superscript indicates the iteration level. We continue the iterations until they converge within a specified tolerance.

## Convergence

The iterations are repeated until the solution converges within a specified tolerance. This process of linearizing the nonlinear terms and iterating until convergence is commonly used in Computational Fluid Dynamics (CFD) codes. The key points are:

- **Linearization**: Performed about a guess value to handle nonlinearity.
- **Convergence Check**: Ensuring the solution has converged within the specified tolerance is crucial.

### Steps in the Iterative Solution Process

1. **Initial Guess**:
   - Start with an initial guess $u_i^{(1)}$.

2. **Linearization**:
   - Linearize the governing equations around the guess value.

3. **Update Solution**:
   - Compute the new values $u_i^{(m)}$ using the updated guess values from the previous iteration.

4. **Check Convergence**:
   - Compare the new solution with the previous iteration.
   - If the difference is within the specified tolerance, the solution has converged.

5. **Iterate**:
   - If the solution has not converged, use the new values as the guess for the next iteration and repeat the process.

### Importance of Convergence

- **Accuracy**: Ensures the solution accurately represents the physical problem.
- **Efficiency**: Reduces computational resources by avoiding unnecessary iterations.
- **Stability**: A well-converged solution is typically more stable and reliable.

