# Continuous vs Discrete Domain

This script illustrates the central step of CFD, replacing a field defined at every point of a continuous domain by values stored at a finite set of grid points, and measures the error this introduces for the model problem $du/dx + u = 0$, $u(0) = 1$. The derivative is replaced by a backward difference on $N$ equally spaced points, the resulting bidiagonal system is solved, and the outlet value is compared with the exact $e^{-1}$ on grids of 4 to 256 points.

## Overview

- Draws the exact field $u(x) = e^{-x}$ as a continuous curve and the four-point discrete solution as values attached to grid points.
- Assembles and solves the discrete system for $N = 4$ and prints it, reproducing the hand calculation $u = (1, 3/4, 9/16, 27/64)$.
- Plots the discrete solutions for $N = 4$, 8 and 16 against the exact solution.
- Computes the error at $x = 1$ for $N = 4, 8, \dots, 256$ and the observed order between consecutive grids.

## Mathematical Background

On the grid $x_i = (i - 1)\Delta x$, $i = 1, \dots, N$, $\Delta x = 1/(N - 1)$, the backward difference gives

$$
\frac{u_i - u_{i-1}}{\Delta x} + u_i = 0 \quad\Longrightarrow\quad
u_i = \frac{u_{i-1}}{1 + \Delta x},
\qquad u_1 = 1
$$

so $u_N = (1 + \Delta x)^{-(N-1)}$. A Taylor expansion shows that the local truncation error is $-\tfrac{\Delta x}{2}u'' + O(\Delta x^2)$, so the scheme is first order and the error at $x = 1$ should halve when $\Delta x$ halves. Because the refinement ratio $\Delta x_k/\Delta x_{k+1}$ is not exactly 2 here, the observed order is computed as $p = \ln(e_k/e_{k+1})/\ln(\Delta x_k/\Delta x_{k+1})$.

## Implementation

- `solve_backward_difference(n_points)` returns the grid and the discrete solution in closed form.
- `assemble_system(n_points)` builds the matrix with the Dirichlet row first, the form a general solver would use.
- `outlet_errors()` and `observed_orders(dx, err)` produce the convergence data for `N_STUDY`; `N_COMPARE` sets the grids of panel (b).
- `make_figure()` draws the three panels.

## Usage

```bash
python main.py                          # print the system and the errors and show the figure
python main.py --no-show --output .     # save continuous_vs_discrete_domain.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The error at $x = 1$ is 0.05400 (14.68%) with 4 points, 0.02482 (6.75%) with 8, 0.01193 (3.24%) with 16 and 0.00072 (0.20%) with 256. The observed order rises from 0.92 to 1.00.

![Continuous and discrete domain, solutions and convergence](continuous_vs_discrete_domain.png)

Panel (a) contrasts the continuous field with the four stored values $u_1, \dots, u_4$. Panel (b) shows the discrete solutions approaching $e^{-x}$ from above, and panel (c) the outlet error parallel to the slope-1 line.

## Related Notes

- [The Strategy of CFD](../../../notes/numerical/cfd/cfd_process.md)
- [Verification and Validation](../../../notes/numerical/cfd/verification_and_validation.md)
