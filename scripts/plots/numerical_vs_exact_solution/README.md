# Numerical vs. Exact Solution Comparison

This script compares the exact analytical solution $u(x) = e^{-x}$ with a discrete numerical approximation evaluated at five sample points. Plotting both curves on the same axes gives an intuitive visual measure of the discretisation error introduced by the numerical scheme. The comparison is a classic pedagogical tool for demonstrating the gap between continuous mathematics and its finite approximation.

## Overview

- Evaluates the exact solution on a dense x grid for a smooth reference curve
- Computes the numerical approximation at five prescribed sample points
- Plots both on the same axes and marks the numerical points explicitly
- Computes and displays the pointwise error at each sample location
- Uses a clear legend and grid to aid comparison

## Mathematical Background

### Exact Solution

$$u(x) = e^{-x}$$

This is the continuous analytical solution, valid for all $x \ge 0$.

### Numerical Approximation

At the five sample points $x_i \in \{0,\, 0.25,\, 0.5,\, 0.75,\, 1.0\}$, the numerical values are:

$$u_N = \left[1,\; \frac{3}{4},\; \frac{9}{16},\; \frac{27}{64},\; \frac{27}{64}\right]$$

### Pointwise Error

$$e_i = u(x_i) - u_N(x_i)$$

The error highlights where the numerical scheme over- or under-estimates the true solution, particularly at $x_4 = x_5 = 0.75$ where $u_N$ is repeated.

## Implementation

1. Define a dense array `x = np.linspace(0, 1, 300)` and compute `u_exact = np.exp(-x)`.
2. Define sample points `x_pts = [0, 0.25, 0.5, 0.75, 1.0]` and numerical values `u_N`.
3. Compute exact values at sample points and calculate pointwise errors `e_i`.
4. Plot the exact solution as a continuous curve and the numerical values as markers.
5. Optionally draw vertical error bars between the exact and numerical values.
6. Set axis labels, title, legend, and grid; display the figure.

## Output

The script produces a figure showing the smooth exponential decay of the exact solution alongside the five discrete numerical approximation points. Discrepancies are visible at x = 0.75 and x = 1.0, where the numerical scheme repeats a value instead of tracking the true exponential. The plot clearly illustrates the concept of discretisation error.
