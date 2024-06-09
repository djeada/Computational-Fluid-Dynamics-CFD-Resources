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
\left( \frac{du}{dx} \right)_i + u_i = 0
$$

where the subscript $i$ represents the value at grid point $x_i$.

### Taylor Series Expansion

To express $\left( \frac{du}{dx} \right)_i$ in terms of $u$ at the grid points, we expand $u_{i-1}$ in a Taylor series:

$$
u_{i-1} = u_i - \Delta x \left( \frac{du}{dx} \right)_i + O(\Delta x^2)
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
\left( \frac{du}{dx} \right)_i \approx \frac{u_i - u_{i-1}}{\Delta x}
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
