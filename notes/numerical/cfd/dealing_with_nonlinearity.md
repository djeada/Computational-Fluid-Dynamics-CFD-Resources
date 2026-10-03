# Dealing with Nonlinearity

The highly nonlinear nature of the governing equations for fluid flow makes obtaining accurate numerical solutions for complicated flows challenging. In Computational Fluid Dynamics (CFD), the nonlinearities often arise from convective terms, turbulence models, or nonlinear source terms. Understanding and handling nonlinearity is important because it directly affects the stability, accuracy, and convergence of numerical solvers. This section explains how nonlinearity can be managed via linearization and iterative solution techniques.

## Demonstrating the Effect of Nonlinearity

Consider a simple one-dimensional (1D) example with a nonlinear term. The governing differential equation is given by:

$$
\frac{du}{dx} + u^2 = 0; \quad 0 \le x \le 1; \quad u(0) = 1
$$

This equation is nonlinear due to the $u^2$ term. When discretizing the problem using a finite-difference method, we approximate the derivative at a grid point $x_i$ by

$$
\frac{u_i - u_{i-1}}{\Delta x}
$$

resulting in the discrete equation

$$
\frac{u_i - u_{i-1}}{\Delta x} + u_i^2 = 0
$$

The presence of $u_i^2$ makes this a nonlinear algebraic equation at each grid point, meaning that standard linear solution techniques cannot be applied directly. Instead, we must handle the nonlinearity—typically via linearization—before proceeding with an iterative solution.

## Linearization Strategy

A common approach for dealing with nonlinear equations in CFD is to linearize them about an initial guess and then solve the resulting linear equations iteratively until convergence. This strategy is central to methods like the Newton–Raphson algorithm and many of its variants.

### Steps for Linearization

I. Initial Guess:

- Assume an initial guess for the solution at the grid point, denoted as $u_{ig}$ (the subscript “g” stands for "guess"). The choice of $u_{ig}$ can be based on physical intuition, previous solutions, or even a simple constant value.

II. Define the Perturbation:

- Define the difference between the true solution $u_i$ and the guess $u_{ig}$ as:

  ```math
  \Delta u_i = u_i - u_{ig}
  ```

III. Expand and Approximate:

- Substitute $u_i = u_{ig} + \Delta u_i$ into the nonlinear term. Squaring the expression yields:

  ```math
  u_i^2 = (u_{ig} + \Delta u_i)^2 = u_{ig}^2 + 2u_{ig}\Delta u_i + (\Delta u_i)^2
  ```

- If the perturbation $\Delta u_i$ is small compared to $u_{ig}$, then $(\Delta u_i)^2$ is insignificant. This is a standard assumption in linearization procedures, which leads to:

  ```math
  u_i^2 \approx u_{ig}^2 + 2u_{ig}\Delta u_i
  ```

- Expressing $\Delta u_i$ in terms of $u_i$ and $u_{ig}$ gives:

  ```math
  u_i^2 \approx u_{ig}^2 + 2u_{ig}(u_i - u_{ig})
  ```

IV. Simplify the Expression:

- Simplify the expression further to obtain a linear form in $u_i$:

  ```math
  u_i^2 \approx 2u_{ig} u_i - u_{ig}^2
  ```

V. Linearized Finite-Difference Approximation:

- Substitute the linearized expression for $u_i^2$ back into the finite-difference approximation:

  ```math
  \frac{u_i - u_{i-1}}{\Delta x} + 2u_{ig} u_i - u_{ig}^2 = 0
  ```

This linearization transforms the originally nonlinear finite-difference equation into a linear equation in terms of $u_i$, which can then be solved using standard linear solvers.

### Error Analysis

- The error introduced by neglecting the $(\Delta u_i)^2$ term is of order $O((\Delta u_i)^2)$. As the iterative process proceeds and $u_{ig}$ converges to the true solution $u_i$, the perturbation $\Delta u_i$ decreases, rendering the linearization error insignificant. This error analysis justifies the iterative refinement process.

## Iterative Solution Process

Since the linearization is based on an initial guess, the solution must be refined iteratively. The overall approach is to repeatedly update the guess and solve the linearized equations until the solution converges to within a prescribed tolerance.

### Iterative Scheme

I. Iteration 1:

- Start with an initial guess $u_i^{(1)}$ for each grid point.

II. Iteration 2:

- Use the solution from the previous iteration as the new guess: $u_{ig}^{(2)} = u_i^{(1)}$.

III. Iteration 3 and Beyond:

- Continue updating the guess using:

  ```math
  u_{ig}^{(n)} = u_i^{(n-1)}
  ```

while re-linearizing the nonlinear term around the latest guess at each iteration.

IV. Convergence Check:

- After each iteration, compare the new solution $u_i^{(n)}$ with the previous one $u_i^{(n-1)}$. If the difference (measured by an appropriate norm) is less than a specified tolerance, the solution is considered converged.
  The iterative process makes sure that the approximation gradually improves, reducing the error introduced by the initial linearization and finally providing a solution that satisfies the nonlinear equation.

## Convergence

Convergence is an important aspect of the iterative solution process. It makes sure that the numerical solution becomes both stable and accurate as the iterations progress.

- Convergence Check:\
  A common practice is to compute the residual (the difference between the left- and right-hand sides of the equation) or the difference between successive iterates. When these quantities fall below a predefined threshold, the solution is deemed converged.

- Criteria for Convergence:\
  Convergence is typically assessed using norms (e.g., the $L_2$ norm) of the error:

$$
\| u^{(n)} - u^{(n-1)}\| < \epsilon
$$

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

- Accuracy:\
  A converged solution means that the linearization error is minimized and the numerical solution accurately reflects the underlying physical phenomena.

- Efficiency:\
  By setting up strong convergence criteria, the iterative process avoids unnecessary computations, thereby optimizing the use of computational resources.

- Stability:\
  Convergence is often associated with numerical stability. A solution that has converged within a tight tolerance is less likely to exhibit erratic behavior, making sure that the results are both reliable and reproducible.

## Purpose in CFD

The convective term $(\mathbf{v} \cdot \nabla)\mathbf{v}$ in the Navier–Stokes equations makes them nonlinear, so the discretized system is also nonlinear. This note explains how to linearize these terms (e.g., Newton–Raphson), iteratively update the solution, and combine nonlinear-term handling with matrix inversion. The time-marching strategy for reaching a steady state is also covered.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Nonlinear discrete system $A(u_g)u = b(u_g)$, initial guess $u_g$, grid spacing $\Delta x$, convergence tolerance |
| **Outputs** | Converged solution vector $u$, iteration count, residual history |

## Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.

## Exercises

**Exercise 1.** The true value at a grid point is $u_i = 0.75$ and the guess is $u_{ig} = 0.8$. Evaluate $u_i^2$ exactly and with the linearization $u_i^2 \approx 2u_{ig}u_i - u_{ig}^2$, and check that the error equals $(\Delta u_i)^2$.

<details>
<summary>Answer</summary>

Exact: $0.75^2 = 0.5625$.

Linearized: $2 \times 0.8 \times 0.75 - 0.64 = 0.56$.

The error is $0.0025$, and $\Delta u_i = 0.75 - 0.8 = -0.05$ gives $(\Delta u_i)^2 = 0.0025$. The two agree.

</details>

**Exercise 2.** At grid point 2 of the example ($\Delta x = 1/3$, $u_1 = 1$), solve the linearized equation $\frac{u_2 - u_1}{\Delta x} + 2u_{g}u_2 - u_{g}^2 = 0$ repeatedly, starting from $u_g = 1$ and using each result as the next guess. Give the first three iterates and their errors relative to the exact root of $\Delta x\, u_2^2 + u_2 - 1 = 0$.

<details>
<summary>Answer</summary>

Solving for $u_2$ gives $u_2 = \dfrac{u_1/\Delta x + u_g^2}{1/\Delta x + 2u_g}$.

The exact root is $u_2 = \dfrac{-1 + \sqrt{1 + 4\Delta x}}{2\Delta x} \approx 0.7912878$.

- From $u_g = 1$: $u_2 = 4/5 = 0.8$, error $8.7 \times 10^{-3}$.
- From $u_g = 0.8$: $u_2 = 3.64/4.6 \approx 0.7913043$, error $1.65 \times 10^{-5}$.
- Next: $u_2 \approx 0.79128785$, error $5.9 \times 10^{-11}$.

The number of correct digits roughly doubles each iteration: quadratic convergence.

</details>

**Exercise 3.** Show that the linearized update of Exercise 2 is exactly the Newton–Raphson method applied to $F(u) = \frac{u - u_{i-1}}{\Delta x} + u^2 = 0$.

<details>
<summary>Answer</summary>

Newton's method gives $u^{\text{new}} = u_g - F(u_g)/F'(u_g)$, with $F'(u) = 1/\Delta x + 2u$. Then

```math
u^{\text{new}} = \frac{u_g\left(\frac{1}{\Delta x} + 2u_g\right) - \frac{u_g - u_{i-1}}{\Delta x} - u_g^2}{\frac{1}{\Delta x} + 2u_g} = \frac{\frac{u_{i-1}}{\Delta x} + u_g^2}{\frac{1}{\Delta x} + 2u_g}
```

which is the same expression as solving the linearized equation for $u_i$. Dropping $(\Delta u_i)^2$ is the same as keeping the first-order Taylor term that Newton's method uses, which is why the error is $O((\Delta u_i)^2)$.

</details>

**Exercise 4.** An alternative "Picard" linearization lags one factor: $u_i^2 \approx u_{ig} u_i$. Derive the update, iterate six times from $u_g = 1$ for the same point as Exercise 2, and compare the convergence with Newton's method.

<details>
<summary>Answer</summary>

The update is $u_2 = \dfrac{u_1/\Delta x}{1/\Delta x + u_g} = \dfrac{3}{3 + u_g}$.

The iterates are $0.75$, $0.8$, $0.78947$, $0.79167$, $0.79121$ and $0.79130$, with errors $-4.1 \times 10^{-2}$, $8.7 \times 10^{-3}$, $-1.8 \times 10^{-3}$, $3.8 \times 10^{-4}$, $-7.9 \times 10^{-5}$ and $1.65 \times 10^{-5}$.

The error changes sign and shrinks by a constant factor of about $u^*/(1/\Delta x + u^*) \approx 0.21$ per iteration: linear convergence. Picard needs six iterations to reach the accuracy Newton reaches in two. Picard is simpler and often more robust far from the solution, which is why codes sometimes start with Picard and switch to Newton.

</details>

**Exercise 5.** An iteration converges linearly with $e^{(n)} \approx \rho\, e^{(n-1)}$. The change between successive iterates is $\|u^{(n)} - u^{(n-1)}\| = 10^{-6}$. Estimate the remaining error for $\rho = 0.9$ and $\rho = 0.99$, and explain what this means for the convergence criterion $\|u^{(n)} - u^{(n-1)}\| < \epsilon$.

<details>
<summary>Answer</summary>

The change is $e^{(n-1)} - e^{(n)} \approx (1 - \rho)e^{(n-1)}$, so

```math
e^{(n)} \approx \frac{\rho}{1 - \rho}\,\| u^{(n)} - u^{(n-1)}\|
```

For $\rho = 0.9$: $9 \times 10^{-6}$. For $\rho = 0.99$: $9.9 \times 10^{-5}$.

For slowly converging iterations the true error can be about 100 times larger than the step size. The tolerance $\epsilon$ must be chosen tighter than the accuracy actually required, or the convergence rate estimated from the residual history and used to correct it.

</details>

## References

- Kelley, C. T., *Iterative Methods for Linear and Nonlinear Equations*, SIAM, 1995.
- Patankar, S. V., *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
- Ferziger, J. H., Perić, M., & Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- Anderson, J. D., *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
