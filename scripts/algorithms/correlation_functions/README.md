# Correlation Functions

This script plots six correlation functions used in kriging surrogate models (linear, exponential, Matérn 3/2, Matérn 5/2, cubic spline and Gaussian) for several values of the correlation parameter $\theta$. Laying the curves side by side shows how the choice of function sets the smoothness of the correlation at zero lag and whether it has compact support, and how $\theta$ sets its range.

## Overview

- Evaluates the six correlation functions on 400 lag values $h \in [-2, 2]$.
- Overlays one curve per $`\theta \in \{0.5, 1, 2\}`$ in each panel.
- Draws a $2 \times 3$ figure, one panel per function with its formula in the title, ordered from the roughest to the smoothest function.

## Mathematical Background

A stationary correlation function $`R(h;\,\theta)`$ depends only on the lag $h = x - x'$ and a parameter $\theta > 0$. The six functions below have $`R(0;\,\theta) = 1`$ and decay as $|h|$ grows. In this convention a larger $\theta$ means a shorter correlation range.

### Linear

```math
R(h;\,\theta) = \max\bigl(0,\; 1 - \theta|h|\bigr)
```

This is a tent function that is zero for $|h| \geq 1/\theta$. It has a kink at $h = 0$ and at the edge of its support.

### Exponential

```math
R(h;\,\theta) = e^{-\theta|h|}
```

It has global support and correlation length $1/\theta$, and it is continuous but not differentiable at $h = 0$. It is the correlation function of the Ornstein–Uhlenbeck process.

### Matérn 3/2 and 5/2

```math
R_{3/2}(h;\,\theta) = \left(1 + \sqrt{3}\,\theta|h|\right)e^{-\sqrt{3}\,\theta|h|},
\qquad
R_{5/2}(h;\,\theta) = \left(1 + a + \tfrac{a^2}{3}\right)e^{-a},\quad a = \sqrt{5}\,\theta|h|
```

The Matérn family $R_\nu$ sits between the exponential ($\nu = 1/2$) and the Gaussian ($\nu \to \infty$). A process with Matérn correlation is $\lceil\nu\rceil - 1$ times mean-square differentiable, so $\nu = 3/2$ gives once and $\nu = 5/2$ twice differentiable sample paths. They are common defaults in Gaussian-process software because they are smooth enough for physical responses without the ill-conditioning of the Gaussian.

### Gaussian

```math
R(h;\,\theta) = e^{-\theta h^2}
```

It has global support and is infinitely differentiable. Its effective range scales as $1/\sqrt{\theta}$.

### Cubic Spline

In the scaled lag $\xi = \theta|h|$:

```math
R(h;\,\theta) = \begin{cases} 1 - \tfrac{3}{2}\xi^2 + \tfrac{3}{4}\xi^3, & \xi \leq 1, \\ \tfrac{1}{4}(2 - \xi)^3, & 1 < \xi \leq 2, \\ 0, & \xi > 2. \end{cases}
```

This is the cubic B-spline scaled so that $R(0) = 1$. It is twice continuously differentiable and zero for $|h| \geq 2/\theta$. The [Kriging](../../../notes/numerical/surrogates/kriging.md) note and the [Kriging Interpolation](../kriging_interpolation/) script write the same function with support $1/\theta$, so their $\theta$ is half the value used here.

## Implementation

- `linear`, `exponential`, `matern32`, `matern52`, `gaussian` and `cubic_spline` evaluate $R(h;\theta)$ element-wise. `cubic_spline` handles its three branches with nested `numpy.where` calls.
- `CORRELATION_FUNCTIONS` maps each panel title to its function.
- `plot_correlation_functions(h, thetas)` draws one panel per function and one curve per $\theta$.
- `H_MAX`, `N_LAGS` and `THETAS` set the lag range, the number of lag samples and the parameter values.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Linear, exponential, Matérn 3/2, Matérn 5/2, cubic spline and Gaussian correlation functions](correlation_functions.png)

The linear tents reach zero at $|h| = 1/\theta$ (at $\pm 2$, $\pm 1$ and $\pm 0.5$), and the exponential has the same sharp peak at $h = 0$ with tails that are still non-zero at $|h| = 2$. The two Matérn functions have rounded peaks and exponential tails; at $\theta = 0.5$ and $|h| = 2$ they are still 0.48 and 0.52. The cubic spline reaches zero at $|h| = 2/\theta$; for $\theta = 0.5$ the support extends to $|h| = 4$, beyond the plotted range, so the curve is still 0.25 at $h = \pm 2$. The Gaussian bells narrow as $\theta$ grows, but more slowly than the others, because their range scales as $1/\sqrt{\theta}$ rather than $1/\theta$.

## Related Notes

- [Kriging](../../../notes/numerical/surrogates/kriging.md)
- [Hierarchical Kriging](../../../notes/numerical/surrogates/hierarchical_kriging.md)
- [Surrogate Modelling Introduction](../../../notes/numerical/surrogates/intro.md)
