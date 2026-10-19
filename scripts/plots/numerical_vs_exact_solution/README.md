# Numerical vs. Exact Solution Comparison

This script solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error. With the default four grid points ($\Delta x = 1/3$) it reproduces the discrete values $1, 3/4, 9/16, 27/64$ derived in the FDM notes, where the error at $x = 1$ is 14.7%. The `--points` option lets you refine the grid to see the error shrink.

## Overview

- Marches the backward-difference equation $(u_i - u_{i-1})/\Delta x + u_i = 0$ from $x = 0$ to $x = 1$ on `--points` equally spaced grid points (default 4).
- Evaluates the exact solution at the grid points and on a fine grid of 100 points for a smooth reference curve.
- Computes the pointwise error $e_i = u(x_i) - u_i$ and prints a table of $x_i$, $u_i$, $u(x_i)$, $e_i$ and the relative error.
- Plots the exact curve and the numerical points in the top panel and the pointwise error in the bottom panel.

## Mathematical Background

### Problem and exact solution

$$
\frac{du}{dx} + u = 0,
\qquad 0 \le x \le 1,
\qquad u(0) = 1 \quad\Longrightarrow\quad u(x) = e^{-x}
$$

### Discretisation

A backward Taylor expansion gives the first-order approximation $`\left(du/dx\right)_i \approx (u_i - u_{i-1})/\Delta x`$, with truncation error $O(\Delta x)$. Substituting it into the ODE gives

$$
\frac{u_i - u_{i-1}}{\Delta x} + u_i = 0 \quad\Longrightarrow\quad
u_i = \frac{u_{i-1}}{1 + \Delta x} = \left(\frac{1}{1 + \Delta x}\right)^{i}
$$

This is the implicit (backward) Euler method applied to $u' = -u$. For $\Delta x = 1/3$ the ratio is $3/4$, so

$$
u_N = \left[1,\ \frac{3}{4},\ \frac{9}{16},\ \frac{27}{64}\right] \quad \text{at}\quad
x_i = \left[0,\ \frac{1}{3},\ \frac{2}{3},\ 1\right]
$$

### Pointwise error

$$
e_i = u(x_i) - u_i
$$

Since $1/(1 + \Delta x) > e^{-\Delta x}$, the scheme decays too slowly. Every $e_i$ for $i \ge 1$ is negative, and $|e_i|$ grows with $x$. With four points the values are:

| $x_i$ | $u_i$ | $e^{-x_i}$ | $e_i$ | relative error |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0% |
| 1/3 | 0.7500 | 0.7165 | −0.0335 | 4.7% |
| 2/3 | 0.5625 | 0.5134 | −0.0491 | 9.6% |
| 1 | 0.4219 | 0.3679 | −0.0540 | 14.7% |

Halving $\Delta x$ roughly halves the error at $x = 1$, as expected for a first-order scheme.

## Implementation

- Constants: `X_END = 1.0`, `U0 = 1.0`, `N_POINTS = 4`.
- `exact_solution(x)` returns $u_0 e^{-x}$.
- `solve_backward_difference(n_points, x_end, u0)` builds the grid and applies $u_i = u_{i-1}/(1 + \Delta x)$.
- `plot_comparison(x, u_num, error)` draws the two stacked panels.
- `main(argv)` parses `--points`, `--no-show` and `--output`, and prints the error table.

## Usage

```bash
python main.py                      # 4 points (dx = 1/3), open the plot window
python main.py --points 16          # finer grid
python main.py --no-show --output . # save numerical_vs_exact_solution.png without opening a window
```

| Flag | Effect |
| --- | --- |
| `--points N` | Number of grid points including both ends (default 4) |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save `numerical_vs_exact_solution.png` in it |

## Output

In the top panel, the red numerical points lie above the black exact curve and move further away as $x$ increases. The bottom panel shows the error growing in magnitude to about $-0.054$ at $x = 1$.

![numerical_vs_exact_solution](numerical_vs_exact_solution.png)

## Related Notes

- [Discretization Using the Finite-Difference Method](../../../notes/numerical/fdm/discretization.md): derives the backward-difference equation solved here.
- [The Strategy of CFD](../../../notes/numerical/cfd/cfd_process.md): gives the $\Delta x = 1/3$ solution, the comparison with $e^{-x}$ and grid convergence.
- [Finite Difference Method](../../../notes/numerical/fdm/intro.md): introduction to FDM and truncation error.
