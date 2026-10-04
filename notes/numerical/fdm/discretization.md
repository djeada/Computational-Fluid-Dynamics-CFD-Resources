# Discretization Using the Finite-Difference Method

To explain the core concepts of Computational Fluid Dynamics (CFD), we will apply these principles to a simple one-dimensional equation:

$$
\frac{du}{dx} + u^m = 0; \quad 0 \le x \le 1; \quad u(0) = 1
$$

We will start with the case where $m = 1$ (a linear equation), and then explore the case where $m = 2$ (a nonlinear equation).

## Discrete Representation for $m = 1$

Here, we will derive a discrete form of the equation for $m = 1$ using a grid-based approach:

```
x₁=0      x₂=1/3         x₃=2/3        x₄=1
|-----------|-------------|-------------|
    Δx=1/3       Δx=1/3       Δx=1/3
```

This grid has four equally spaced grid points with $\Delta x$ being the spacing between successive points. The governing equation is valid at any grid point:

$$
\left(\frac{du}{dx} \right)_i + u_i = 0
$$

where the subscript $i$ represents the value at grid point $x_i$.

### Taylor Series Expansion

To express $`\left( \frac{du}{dx} \right)_i`$ in terms of $`u`$ at the grid points, we expand $`u_{i-1}`$ in a Taylor series:

$$
u_{i-1} = u_i - \Delta x \left(\frac{du}{dx} \right)_i + O(\Delta x^2)
$$

Rearranging gives:

$$
\frac{du}{dx}\bigg|_i = \frac{u_i - u_{i-1}}{\Delta x} + O(\Delta x)
$$

The error in $\left( \frac{du}{dx} \right)_i$ due to the neglected terms in the Taylor series is called the truncation error. Since the truncation error is $O(\Delta x)$, this discrete representation is termed first-order accurate.

### Discrete Equation

Using the finite-difference approximation in the original differential equation and excluding higher-order terms, we get the following discrete equation:

$$
\frac{u_i - u_{i-1}}{\Delta x} + u_i = 0
$$

Thus, we have converted a differential equation into an algebraic equation.

## Steps for Discretization Using the Finite-Difference Method

1. **Define the Continuous Problem**: Start with the continuous differential equation to be solved.

2. **Select a Grid**: Divide the domain into a finite number of grid points. For the given problem, the domain $0 \le x \le 1$ is divided into 4 points with $\Delta x = \frac{1}{3}$.

3. **Discretize the Derivatives**: Use finite-difference approximations to express derivatives at the grid points. For example, the first derivative $\frac{du}{dx}$ at point $i$ is approximated as:

$$
\left(\frac{du}{dx} \right)_i \approx \frac{u_i - u_{i-1}}{\Delta x}
$$

4. **Substitute into the Original Equation**: Replace the derivatives in the original differential equation with their finite-difference approximations. This results in an algebraic equation for each grid point.

5. **Solve the Algebraic Equations**: The resulting system of algebraic equations can be solved using appropriate numerical methods to obtain the values of $u$ at the grid points.

## Example: Solving for $u$ on the Grid

Given the initial condition $u(0) = 1$, we can solve the discrete equation step-by-step for each grid point:

- For $x_2 = \frac{1}{3}$:

$$
\frac{u_2 - u_1}{\Delta x} + u_2 = 0
$$

Given $u_1 = 1$ and $\Delta x = \frac{1}{3}$, solve for $u_2$.

- For $x_3 = \frac{2}{3}$:

$$
\frac{u_3 - u_2}{\Delta x} + u_3 = 0
$$

Use the previously calculated $u_2$ to solve for $u_3$.

- For $x_4 = 1$:

$$
\frac{u_4 - u_3}{\Delta x} + u_4 = 0
$$

Use the previously calculated $u_3$ to solve for $u_4$.

By following these steps, we obtain a numerical solution for $u$ at each grid point, providing an approximate solution to the original differential equation.

## Purpose in CFD

This note demonstrates the core FDM discretization workflow on a minimal 1-D example: define the continuous ODE, lay out a grid, approximate derivatives via Taylor series, assemble the resulting algebraic equations, and solve step by step. It introduces the concept of truncation error and first-order accuracy, which are central to evaluating any numerical scheme in CFD.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | ODE $du/dx + u^m = 0$ with $u(0) = 1$, grid points $x_1, \dots, x_4$, spacing $\Delta x = 1/3$, exponent $m$ |
| **Outputs** | Discrete solution values $u_1, u_2, u_3, u_4$, truncation error order $O(\Delta x)$ |

## Related Scripts

- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [2D Schrödinger Equation Simulation](../../../scripts/simulations/schroedinger_equation/): solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [Grid Convergence Comparison](../../../scripts/plots/comparing_grid_convergence/): illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$.
- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/): solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error.

## Exercises

**Exercise 1.** Carry out the step-by-step solution of the note for $m = 1$ with $\Delta x = 1/3$. Compute $u_2$, $u_3$ and $u_4$, and compare $u_4$ with the exact value $u(1) = e^{-1}$.

<details>
<summary>Answer</summary>

Rearranging $(u_i - u_{i-1})/\Delta x + u_i = 0$ gives $`u_i = u_{i-1}/(1 + \Delta x) = 0.75\,u_{i-1}`$. So:

- $u_2 = 0.75$
- $u_3 = 0.5625$
- $u_4 = 0.4219$

The exact value is $e^{-1} = 0.3679$, so the error at $x = 1$ is $0.054$.

</details>

**Exercise 2.** Repeat Exercise 1 with $\Delta x = 1/6$ (seven grid points). Compute the ratio of the errors at $x = 1$, and use it to confirm the order of accuracy.

<details>
<summary>Answer</summary>

After $N$ steps, $u(1) \approx (1 + \Delta x)^{-N}$. With $\Delta x = 1/6$, $u(1) \approx (6/7)^6 = 0.3966$, so the error is $0.0287$.

The error ratio is $0.0540/0.0287 = 1.88$, close to 2. Halving $\Delta x$ roughly halves the error, which confirms first-order accuracy.

</details>

**Exercise 3.** (a) Extend the Taylor series to find the leading term of the truncation error of the backward difference. (b) Use the forward difference $(u_{i+1} - u_i)/\Delta x + u_i = 0$ instead, compute $u(1)$ with $\Delta x = 1/3$, and explain what goes wrong if $\Delta x > 2$.

<details>
<summary>Answer</summary>

(a) $`u_{i-1} = u_i - \Delta x\,u'_i + \frac{\Delta x^2}{2}u''_i - \dots`$, so

```math
\frac{u_i - u_{i-1}}{\Delta x} = u'_i - \frac{\Delta x}{2}u''_i + O(\Delta x^2)
```

The leading error is $-\frac{\Delta x}{2}u''$.

(b) The forward (explicit) update is $u_{i+1} = (1 - \Delta x)u_i$, which gives $u(1) = (2/3)^3 = 0.2963$ (error $-0.072$). The backward scheme overestimates the exact $e^{-1}$ and the forward scheme underestimates it.

If $\Delta x > 2$, then $|1 - \Delta x| > 1$ and the forward solution oscillates in sign and grows, even though the exact solution decays. The backward (implicit) factor $1/(1 + \Delta x)$ stays below 1 for every $\Delta x > 0$.

</details>

**Exercise 4.** Solve the nonlinear case $m = 2$ on the same grid ($\Delta x = 1/3$) with the backward difference $(u_i - u_{i-1})/\Delta x + u_i^2 = 0$. Compare with the exact solution $u = 1/(1 + x)$.

<details>
<summary>Answer</summary>

Each step is a quadratic, $`\Delta x\,u_i^2 + u_i - u_{i-1} = 0`$. Its positive root is

```math
u_i = \frac{-1 + \sqrt{1 + 4\Delta x\,u_{i-1}}}{2\Delta x}
```

| $x$ | numerical | exact $1/(1+x)$ |
| --- | --- | --- |
| 1/3 | 0.7913 | 0.7500 |
| 2/3 | 0.6503 | 0.6000 |
| 1 | 0.5496 | 0.5000 |

The error at $x = 1$ is $0.050$. The nonlinearity means a small algebraic equation, here a quadratic, must be solved at each point. On larger problems this is done with Newton or Picard iteration.

</details>

## References

- R. J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems*, SIAM, 2007.
- J. D. Anderson, *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
- J. H. Ferziger, M. Perić, R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
