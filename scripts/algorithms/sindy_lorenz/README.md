# SINDy on the Lorenz System

This script identifies the Lorenz equations from a noisy simulated trajectory with sparse identification of nonlinear dynamics (SINDy), using sequential thresholded least squares over a library of cubic polynomials. It compares the identified coefficient matrix with the true one and integrates the identified model from the same initial condition as the true system.

## Overview

- Integrates the Lorenz system ($\sigma = 10$, $\rho = 28$, $\beta = 8/3$) from $(-8, 8, 27)$ with `scipy.integrate.solve_ivp` (LSODA, tolerances $10^{-10}$), sampled every $\Delta t = 0.002$ for $0 \leq t < 10$.
- Adds Gaussian noise of standard deviation 0.01 to $x$, $y$ and $z$, and estimates the time derivatives with fourth-order central differences.
- Builds the library $\boldsymbol{\Theta}(\mathbf{X})$ of all 20 monomials of degree up to three in $(x, y, z)$.
- Solves $\boldsymbol{\Theta}\boldsymbol{\Xi} \approx \dot{\mathbf{X}}$ with sequential thresholded least squares (threshold $\lambda = 0.1$).
- Prints the identified equations, the number of active terms and the largest relative coefficient error, then integrates the identified model for 15 time units.
- Draws the true and identified coefficient matrices as annotated heat maps, the two attractors in 3D, and $x(t)$ and $z(t)$ for both models.

## Mathematical Background

### The Lorenz System

```math
\dot{x} = \sigma (y - x), \qquad \dot{y} = x(\rho - z) - y, \qquad \dot{z} = xy - \beta z
```

In the monomial library, each equation has two or three non-zero coefficients, seven in total out of $20 \times 3 = 60$.

### Sparse Regression

With $m$ samples stacked as rows, $\mathbf{X} \in \mathbb{R}^{m \times 3}$ holds the states and $\dot{\mathbf{X}}$ their derivatives. SINDy assumes $\dot{\mathbf{X}} = \boldsymbol{\Theta}(\mathbf{X})\boldsymbol{\Xi}$ with a sparse $\boldsymbol{\Xi} \in \mathbb{R}^{20 \times 3}$, whose column $k$ holds the coefficients of equation $k$.

Sequential thresholded least squares (Brunton, Proctor and Kutz 2016) alternates two steps, starting from the least-squares solution:

1. Set every coefficient with $|\Xi_{jk}| < \lambda$ to zero.
2. For each equation $k$, refit the remaining coefficients by least squares on the retained library columns.

The loop stops when the set of active terms no longer changes.

### Derivatives

Away from the ends of the record the derivative is estimated with

```math
\dot{x}_i \approx \frac{-x_{i+2} + 8x_{i+1} - 8x_{i-1} + x_{i-2}}{12\,\Delta t}
```

which has truncation error $O(\Delta t^4)$ but amplifies noise of standard deviation $\eta$ to $`\sqrt{130}\,\eta/(12\,\Delta t) \approx 0.95\,\eta/\Delta t`$, about 4.8 here. Least squares over 5000 samples averages most of this out.

## Implementation

- `lorenz` is the right-hand side and `simulate(rhs, x0, t)` integrates any right-hand side with `solve_ivp`.
- `library_exponents`, `library_names` and `build_library` define and evaluate $\boldsymbol{\Theta}$.
- `central_difference(X, dt)` computes the derivatives and `stlsq(Theta, dX, threshold)` performs the sparse regression.
- `fit_lorenz(noise_std, threshold, seed)` runs the whole identification and returns $\boldsymbol{\Xi}$ and the library exponents.
- `true_coefficients` builds the exact $\boldsymbol{\Xi}$, and `identified_rhs(Xi, exponents)` wraps the identified model for `solve_ivp`.
- `NOISE_STD`, `THRESHOLD`, `POLY_ORDER`, `DT` and `T_TRAIN` control the data and the regression.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![True and SINDy-identified Lorenz coefficients and trajectories](sindy_lorenz.png)

STLSQ keeps exactly the seven true terms and identifies

```math
\dot{x} = -9.998x + 9.999y, \qquad \dot{y} = 28.005x - 1.002y - 1.000xz, \qquad \dot{z} = -2.667z + 1.000xy
```

The largest relative coefficient error is $2.1 \times 10^{-3}$. The identified trajectory follows the true one for about seven time units; the two separate by more than 1 at $t = 5.57$ and diverge completely after $t \approx 7$. This is the sensitivity to small perturbations of a chaotic system, not a model error: the identified attractor in panel (c) has the same shape as the true one.

## Related Notes

- [Modeling Flow Dynamics](../../../notes/machine_learning/flow/flow_dynamics.md)
