# Grid Convergence Comparison

This script demonstrates grid convergence by comparing a family of numerical solutions $u_N(x)$ against the exact analytical solution $u(x) = e^{-x}$ for increasing grid resolution parameters $N = 4, 8, 16$. As $N$ grows the numerical approximation approaches the exact solution, illustrating the convergence behaviour expected from a consistent finite-difference or finite-volume discretisation. The plot provides a clear visual argument for why grid refinement studies are essential in computational fluid dynamics.

## Overview

- Plots the exact solution $u(x) = e^{-x}$ as a reference curve
- Overlays numerical approximations $u_N(x) = e^{-x(1+x/N)}$ for $N = 4, 8, 16$
- Demonstrates monotonic convergence of $u_N$ to $u$ as $N \to \infty$
- Quantifies the pointwise error and its $O(1/N)$ decay
- Uses distinct line styles and colours for each refinement level

## Mathematical Background

### Exact Solution

The analytical reference solution is:

$$u(x) = e^{-x}$$

### Numerical Approximation

The discretisation introduces a truncation error proportional to $x/N$, yielding the approximate solution:

$$u_N(x) = e^{-x\left(1 + x/N\right)}$$

### Convergence Behaviour

As the grid is refined ($N \to \infty$) the exponent approaches $-x$ and the numerical solution recovers the exact result:

$$\lim_{N \to \infty} u_N(x) = e^{-x} = u(x)$$

### Pointwise Error

The local truncation error scales as:

$$\varepsilon_N(x) = |u(x) - u_N(x)| \sim O\!\left(\frac{1}{N}\right)$$

so doubling $N$ halves the error, consistent with first-order convergence.

## Implementation

1. Define the domain $x \in [0, x_{\max}]$ with a fine uniform grid for smooth curves.
2. Evaluate the exact solution $u(x) = e^{-x}$.
3. For each $N \in \{4, 8, 16\}$, evaluate $u_N(x) = e^{-x(1+x/N)}$.
4. Plot all curves on the same axes with distinct styles and labels.
5. Optionally compute and display the maximum error for each $N$.
6. Add a legend identifying the exact solution and each numerical approximation.

## Output

The script produces a single figure with the exact solution drawn as a solid reference line and three numerical approximations drawn as dashed or dotted curves. The curves converge visually as $N$ increases, and a legend identifies each line. An optional error panel or annotation may show the $O(1/N)$ convergence rate numerically.

![Graph comparing grid convergence](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/c86df1dd-ad03-4d61-908a-79c646821cab)
