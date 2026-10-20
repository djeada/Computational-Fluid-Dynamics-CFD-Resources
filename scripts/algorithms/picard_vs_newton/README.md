# Picard Iteration and Newton's Method for Steady Burgers

This script solves the discretized steady viscous Burgers equation, a 1D model of the convective nonlinearity in the Navier–Stokes equations, with Picard iteration and Newton's method and compares their convergence. Picard iteration lags the convecting velocity, as segregated CFD solvers do, and converges linearly at best; Newton's method uses the exact Jacobian and converges quadratically once it is close to the solution. The script also shows a starting guess from which plain Newton diverges, a backtracking line search fails, and pseudo-transient continuation converges.

## Overview

- Solves $`u\,u' = \nu\,u''`$ on $0 < x < 1$ with $u(0) = 1$, $u(1) = 0$ and $\nu = 0.02$ on $N = 64$ cells, with the conservative central discretization below. The cell Péclet number $u h/\nu$ is at most 0.78, so the discrete solution has no wiggles.
- Compares the converged solution with the exact solution $`u = A\tanh\left(A(1-x)/2\nu\right)`$ on 32 and 64 cells.
- From the linear guess $u^0 = 1 - x$, runs Picard iteration, Picard with under-relaxation $\alpha = 0.7$, and Newton's method until $`\Vert R\Vert_2 < 10^{-10}`$ or 200 iterations.
- Plots $e_{k+1}$ against $e_k$, where $e_k$ is the max-norm distance from the converged discrete solution, to show slopes 1 and 2.
- From the guess $u^0 = 1 - x - 2\sin(\pi x)$, which has reversed flow in the interior, runs Newton with full steps, Newton with a backtracking line search, pseudo-transient continuation and under-relaxed Picard.

## Mathematical Background

### Discrete System

At the interior nodes $i = 1, \dots, N-1$ with spacing $h = 1/N$,

```math
R_i(\mathbf{u}) = \frac{u_{i+1}^2 - u_{i-1}^2}{4h} - \nu\,\frac{u_{i+1} - 2u_i + u_{i-1}}{h^2} = 0
```

The exact solution of the differential equation is $`u = A\tanh\left(A(1-x)/2\nu\right)`$ with $`A\tanh(A/2\nu) = 1`$; for $\nu = 0.02$, $A = 1$ to machine precision.

### Picard Iteration

Writing $`u^2 = \bar{u}\,u`$ and freezing the convecting velocity $\bar{u}$ at the previous iterate gives a linear tridiagonal system for $u^\ast$:

```math
\frac{u^k_{i+1}\,u^\ast_{i+1} - u^k_{i-1}\,u^\ast_{i-1}}{4h} - \nu\,\frac{u^\ast_{i+1} - 2u^\ast_i + u^\ast_{i-1}}{h^2} = 0,
\qquad
\mathbf{u}^{k+1} = \mathbf{u}^k + \alpha\left(\mathbf{u}^\ast - \mathbf{u}^k\right)
```

Near the solution the error obeys $`e_{k+1} \approx G\,e_k`$ with a fixed matrix $G$, so convergence is linear with rate $\rho(G)$. Linearizing one Picard step about the converged solution (a separate check, not done by the script) gives dominant eigenvalues $-0.94 \pm 0.24\mathrm{i}$ for $\alpha = 1$: modulus 0.97, an oscillating and very slow iteration. With $\alpha = 0.7$ their modulus drops to 0.395, which is the error ratio per iteration the script measures.

### Newton's Method

```math
J(\mathbf{u}^k)\,\delta\mathbf{u} = -\mathbf{R}(\mathbf{u}^k), \qquad \mathbf{u}^{k+1} = \mathbf{u}^k + \lambda\,\delta\mathbf{u},
\qquad
\frac{\partial R_i}{\partial u_{i\pm1}} = \pm\frac{u_{i\pm1}}{2h} - \frac{\nu}{h^2}, \quad \frac{\partial R_i}{\partial u_i} = \frac{2\nu}{h^2}
```

With $\lambda = 1$ and an invertible Jacobian near the root, $e_{k+1} \le C e_k^2$. The line search halves $\lambda$ until $`\Vert\mathbf{R}(\mathbf{u}^k + \lambda\delta\mathbf{u})\Vert \le (1 - 10^{-4}\lambda)\Vert\mathbf{R}(\mathbf{u}^k)\Vert`$ and declares failure below $\lambda = 1/1024$. Pseudo-transient continuation solves $`(I/\Delta\tau_k + J)\,\delta\mathbf{u} = -\mathbf{R}`$ with $`\Delta\tau_k = \Delta\tau_0\,\Vert\mathbf{R}^0\Vert/\Vert\mathbf{R}^k\Vert`$ (switched evolution relaxation), so it behaves like implicit time stepping far from the solution and like Newton's method near it.

## Implementation

- `residual(u, h, nu)`, `jacobian_bands(u, h, nu)` and `picard_bands(u, h, nu)` build $\mathbf{R}$, $J$ and the Picard matrix in the banded layout of `scipy.linalg.solve_banded`.
- `picard(u0, h, alpha, ...)` and `newton(u0, h, line_search, pseudo_dt, ...)` return the final iterate, all iterates and the residual history.
- `exact_solution(x, nu)` finds $A$ with `scipy.optimize.brentq`.
- `error_sequence(iterates, converged)` and `convergence_order(errors)` measure the convergence rate.
- `run()` performs the two sets of solves; `make_figure` draws the four panels.
- Constants: `VISCOSITY`, `N_CELLS`, `TOLERANCE`, `MAX_ITERATIONS`, `UNDER_RELAXATION`, `HARD_GUESS_AMPLITUDE`, `PSEUDO_TIME_STEP`, `ARMIJO`, `MIN_STEP`.

## Usage

```bash
python main.py                          # print the convergence summary and show the figure
python main.py --no-show --output .     # save picard_vs_newton.png without opening a window
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The discrete solution on 64 cells differs from the exact one by at most $7.2 \times 10^{-3}$. From the linear guess:

| Method | Iterations to $`\Vert R\Vert < 10^{-10}`$ | Behaviour |
| --- | --- | --- |
| Picard, $\alpha = 1$ | not converged in 200 ($`\Vert R\Vert = 4.3 \times 10^{-2}`$) | oscillating, slow |
| Picard, $\alpha = 0.7$ | 28 | linear, error ratio about 0.40 per iteration |
| Newton | 7 | errors $9.6 \times 10^{-2}$, $4.0 \times 10^{-3}$, $7.5 \times 10^{-6}$, $2.4 \times 10^{-11}$ in the last steps |

From the hard guess, Newton with full steps reaches $`\Vert R\Vert = 4 \times 10^{13}`$ after two steps, the line search finds no acceptable step at the third iteration, pseudo-transient continuation converges in 20 iterations and under-relaxed Picard in 34.

![Steady Burgers solutions and Picard and Newton convergence histories](picard_vs_newton.png)

Panel (a) shows the converged solutions on 32 and 64 cells against the exact layer at $x = 1$. Panel (b) shows the residual histories from the linear guess, and panel (c) the same runs as $e_{k+1}$ against $e_k$: the Picard points follow a line of slope 1 below the diagonal, the Newton points a line of slope 2. Panel (d) shows the runs from the hard guess. The first full Newton step overshoots to $\max|u| = 21$, where the Jacobian has a condition number of about $10^9$, and the next step is enormous. Shortening the step does not fix a nearly singular Jacobian, while the $I/\Delta\tau$ term of pseudo-transient continuation regularizes the system until the iterate is close enough for Newton's method to take over.

## Related Notes

- [Dealing with Nonlinearity](../../../notes/numerical/cfd/dealing_with_nonlinearity.md)
- [Direct and Iterative Solvers](../../../notes/numerical/cfd/direct_and_iterative_solvers.md)
- [Numerical Stability](../../../notes/numerical/cfd/numerical_stability.md)
