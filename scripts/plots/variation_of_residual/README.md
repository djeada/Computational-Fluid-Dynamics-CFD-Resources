# Variation of Residual with Iteration

This script solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale. The curve is the kind of convergence history CFD solvers report: a fast initial drop, then a slow, steady decrease until the residual falls below the convergence criterion of $10^{-9}$.

## Overview

- Solves $d^2u/dx^2 = 0$ on $N = 100$ points with Dirichlet boundary values $u_0 = 0$ and $u_{N-1} = 1$; the exact discrete solution is a straight line.
- Starts from a random interior guess (seeded, so the run is reproducible).
- Applies in-place Gauss-Seidel sweeps and computes the normalised RMS change between successive iterates after each sweep.
- Stops when the residual drops below $10^{-9}$ (after 9709 iterations with the default seed) or after a maximum number of iterations (50000, or `--steps N`).
- Plots the residual history on a logarithmic y-axis with the convergence criterion as a dashed line, and prints the iteration count, final residual and maximum error against the exact solution.

## Mathematical Background

### Discretised Laplace Equation

The second-order central difference of $d^2u/dx^2 = 0$ gives, at each interior point,

$$
u_{i-1} - 2u_i + u_{i+1} = 0
$$

### Gauss-Seidel Update

Sweeping from left to right and using the value already updated at $i-1$:

$$
u_i^{n+1} = \frac{1}{2}\left(u_{i-1}^{n+1} + u_{i+1}^{n}\right)
$$

### Normalised RMS Residual

$$
R^n = \frac{\sqrt{\dfrac{1}{N}\displaystyle\sum_{i=1}^{N}\left(u_i^n - u_i^{n-1}\right)^2}}{\dfrac{1}{N}\displaystyle\sum_{i=1}^{N}\left|u_i^{n-1}\right|}
$$

### Convergence Criterion

$$
R^n < 10^{-9}
$$

### Convergence Rate

High-wavenumber error components are damped within a few sweeps, which gives the fast initial drop. The smoothest error mode decays by a factor of about $\cos^2\left(\pi/(N-1)\right) \approx 0.999$ per sweep, so the tail of the curve is a straight line on the log axis and thousands of sweeps are needed. Because $R^n$ measures the change between iterates, not the error, the error at convergence (about $7 \times 10^{-7}$ here) is much larger than $10^{-9}$.

## Implementation

- Constants: `N`, `U_LEFT`, `U_RIGHT`, `MAX_ITERATIONS`, `CONVERGENCE_CRITERION` and `SEED`.
- `compute_residual(u, u_old)` returns $R^n$.
- `gauss_seidel_sweep(u)` updates the interior points in place.
- `solve(n, max_iterations, tol, seed)` sets the initial guess and boundary values, sweeps until $R^n$ < `tol` or `max_iterations` is reached, and returns the solution and the residual list.
- `plot_residuals(residuals, tol)` draws the residual history (markers on about 25 points) and returns the figure.
- `main(argv=None)` parses the flags, runs the solver, prints a summary, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                                 # iterate to convergence and open the figure
python main.py --no-show --output .            # save variation_of_residual.png without opening a window
python main.py --no-show --output out --steps 10  # stop after at most 10 iterations
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |
| `--steps N` | Maximum number of iterations (default 50000) |

## Output

A semi-logarithmic plot of the residual against iteration number. The residual falls from about 0.5 to $10^{-2}$ within 10 iterations and to $10^{-3}$ within about 100, then decreases steadily until it crosses the $10^{-9}$ line after 9709 iterations.

![Residual against iteration number](variation_of_residual.png)

## Related Notes

- [Iterative Convergence](../../../notes/numerical/cfd/iterative_convergence.md)
- [Direct and Iterative Solvers](../../../notes/numerical/cfd/direct_and_iterative_solvers.md)
- [Finite Difference Method](../../../notes/numerical/fdm/intro.md)
