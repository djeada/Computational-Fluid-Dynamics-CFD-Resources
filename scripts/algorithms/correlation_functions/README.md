# Correlation Functions

This script visualises four classical spatial correlation functions used in kriging and Gaussian-process surrogate models. By plotting each function over a range of lag values $h \in [-2, 2]$ for multiple values of the length-scale parameter $\theta$, the script provides an intuitive picture of how different kernel choices and parameter settings control the spatial range and smoothness of the modelled correlations.

## Overview

- Evaluates four correlation functions — linear, exponential, Gaussian, and cubic spline — on a dense grid of lag values.
- Overlays curves for several values of $\theta$ in each panel to illustrate the sensitivity to the length-scale parameter.
- Renders a $2 \times 2$ subplot figure with one panel per correlation function.
- Labels each curve with its $\theta$ value and annotates axes for easy comparison.
- Highlights the compact-support property of the linear and cubic spline kernels versus the global support of the exponential and Gaussian kernels.

## Mathematical Background

### Spatial Correlation Functions

A stationary correlation function $R(h;\,\theta)$ depends only on the lag $h = x - x'$ between two locations and a positive length-scale parameter $\theta$. All functions satisfy $R(0;\,\theta) = 1$ and decay toward zero as $|h|$ grows.

### Linear Correlation

$$R(h;\,\theta) = \max\!\bigl(0,\; 1 - \theta|h|\bigr)$$

Piecewise linear and compactly supported on $|h| \leq 1/\theta$. Large $\theta$ yields a narrow tent function; small $\theta$ yields broad, slow decay.

### Exponential Correlation

$$R(h;\,\theta) = e^{-\theta|h|}$$

Globally supported with exponential decay. Corresponds to an Ornstein–Uhlenbeck process; the correlation length is $1/\theta$. The function is continuous but not differentiable at $h = 0$.

### Gaussian Correlation

$$R(h;\,\theta) = e^{-\theta h^2}$$

Globally supported with super-exponential (Gaussian) decay. Infinitely differentiable everywhere; produces very smooth sample paths. The effective range is proportional to $1/\sqrt{\theta}$.

### Cubic Spline Correlation

$$R(h;\,\theta) = \begin{cases} 1 - \tfrac{3}{2}|h|^2 + \tfrac{3}{4}|h|^3, & |h| \leq 1, \\ \tfrac{1}{4}(2 - |h|)^3, & 1 < |h| \leq 2, \\ 0, & |h| > 2. \end{cases}$$

Twice continuously differentiable ($C^2$) with compact support on $|h| \leq 2$. Balances smoothness and locality, making it a popular default in design-of-experiment surrogate models.

## Implementation

1. **Lag grid** — create a dense array of $h$ values in $[-2, 2]$ using `numpy.linspace`.
2. **Parameter set** — define a list of $\theta$ values spanning a range from small (broad correlation) to large (narrow correlation).
3. **Function evaluation** — for each correlation function, evaluate $R(h;\,\theta)$ vectorised over the lag grid using NumPy operations; `numpy.where` handles the piecewise cubic spline branches.
4. **Plotting** — arrange four `Axes` objects in a $2 \times 2$ grid; for each panel, plot one curve per $\theta$ value with a distinct colour and label.
5. **Formatting** — add axis labels ($h$ and $R$), a legend, and a title per panel; display the figure.

## Output

The script displays a single figure with four panels:

- **Top-left**: Linear correlation — tent-shaped curves collapsing toward the origin as $\theta$ increases.
- **Top-right**: Exponential correlation — smooth exponential decay with rate controlled by $\theta$.
- **Bottom-left**: Gaussian correlation — bell-shaped curves whose width narrows with increasing $\theta$.
- **Bottom-right**: Cubic spline correlation — smooth compactly supported curves with zero value beyond $|h| = 2$.
