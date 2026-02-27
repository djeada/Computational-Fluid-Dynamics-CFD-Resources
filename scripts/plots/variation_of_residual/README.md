# Variation of Residual with Iteration

This script performs a 1D Gauss-Seidel iterative solve on a 100-point domain, tracks the normalised residual at each iteration, and plots its convergence history on a logarithmic scale. The resulting curve is characteristic of iterative solvers used in CFD and illustrates how residuals must decrease by several orders of magnitude to achieve a converged solution.

## Overview

- Applies the Gauss-Seidel update rule on a 1D array of 100 points with fixed boundary conditions
- Computes the normalised RMS residual after each iteration
- Terminates the iteration loop when the residual drops below $10^{-9}$
- Plots residual vs iteration number on a semi-logarithmic scale

## Mathematical Background

### Gauss-Seidel Update Rule

$$u_i^{n+1} = \frac{1}{2}\!\left(u_{i-1}^n + u_{i+1}^n\right)$$

This update corresponds to a finite-difference discretisation of the 1D Laplace equation.

### Normalised RMS Residual

$$R^n = \frac{\sqrt{\dfrac{1}{N}\displaystyle\sum_{i=1}^{N}\!\left(u_i^n - u_i^{n-1}\right)^2}}{\dfrac{1}{N}\displaystyle\sum_{i=1}^{N}\!\left|u_i^{n-1}\right|}$$

### Convergence Criterion

$$R^n < 10^{-9}$$

Iteration stops as soon as this threshold is reached, indicating that successive iterates have converged to a common solution.

## Implementation

1. Initialise the solution array $u$ with an interior guess and fixed Dirichlet boundary conditions.
2. At each iteration, sweep through interior points applying the Gauss-Seidel update in-place.
3. Compute the normalised RMS residual $R^n$ comparing the new and previous iterates.
4. Append $R^n$ to a history list and check against the convergence threshold.
5. Plot the residual history on a logarithmic y-axis against iteration count.

## Output

The script displays a semi-logarithmic plot of normalised residual versus iteration number. The curve shows an initial rapid drop followed by a linear decrease (on the log scale), characteristic of Gauss-Seidel convergence, terminating when $R < 10^{-9}$.

![Graph of residual vs. iteration number](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/17a1f9b6-1bae-435f-98de-00130dc721dd)
