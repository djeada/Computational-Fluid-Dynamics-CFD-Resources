# Residual Monitoring During an Iterative Solve

This script follows a Gauss–Seidel solve of the 2D Poisson equation sweep by sweep and records everything a CFD user might look at to decide whether the run has converged: the residual with two normalisations, the change between iterates, the true iterative error, and an integral quantity (the flux through a wall). Because the exact solution and the direct solution of the discrete system are both known, the figure shows how these measures relate to the error and to each other. It also reproduces two typical stalled residual histories and the solution profile at several stages of the iteration.

## Overview

- Solves $`-(\phi_{xx} + \phi_{yy}) = 2\pi^2\sin(\pi x)\sin(\pi y)`$ on the unit square with $\phi = \sin(\pi x)$ on the top wall and $\phi = 0$ on the other three, on $31 \times 31$ interior points with the five-point stencil. The exact solution is $`\phi = \sin(\pi x)\left[\sin(\pi y) + \sinh(\pi y)/\sinh\pi\right]`$.
- Starts from $\phi = 0$ in the interior and performs 2500 red-black Gauss–Seidel sweeps (`--steps`, at least 1000).
- After every sweep records $`\Vert r^k\Vert/\Vert r^0\Vert`$, $`\Vert r^k\Vert/\Vert f\Vert`$ (normalised by the source term only; with the zero initial guess $\Vert r^0\Vert$ equals the norm of the full right-hand side $b$, boundary values included), $`\Vert\phi^k - \phi^{k-1}\Vert/\Vert\phi^k\Vert`$, $`\Vert\phi^k - \phi_h\Vert/\Vert\phi_h\Vert`$ with $\phi_h$ from a sparse direct solve of the same system, and the flux $`Q = \int_0^1 \partial\phi/\partial y\,dx`$ through the bottom wall.
- Repeats the solve in single precision to show the round-off floor of the residual.
- Solves a cell-centred pure-Neumann problem whose source has a nonzero mean, which has no solution, and the same problem with a zero-mean source.
- Plots the profile $\phi(x, 0.5)$ after 10, 100 and 1000 sweeps against the converged discrete and the exact solution.

## Mathematical Background

### Residual and Error

For a linear system $A\boldsymbol{\phi} = \mathbf{b}$, the residual of an iterate is $\mathbf{r}^k = \mathbf{b} - A\boldsymbol{\phi}^k$ and the iterative error is $\mathbf{e}^k = \boldsymbol{\phi}_h - \boldsymbol{\phi}^k$, so $A\mathbf{e}^k = \mathbf{r}^k$. This gives the bound

```math
\frac{\Vert\mathbf{e}^k\Vert}{\Vert\boldsymbol{\phi}_h\Vert} \le \kappa(A)\,\frac{\Vert\mathbf{r}^k\Vert}{\Vert\mathbf{b}\Vert}, \qquad \kappa(A) = \Vert A\Vert\,\Vert A^{-1}\Vert
```

which for this grid has $\kappa = \cot^2(\pi h/2) \approx 414$. Once one error mode dominates, all the monitored quantities decay at the same rate $\rho$, here $\cos^2(\pi h) = 0.99039$ per sweep, and the change between iterates underestimates the error by a factor of about $1/(1 - \rho) \approx 104$ (the script's histories give 103).

### Compatibility of the Neumann Problem

Integrating $-\nabla^2\phi = f$ over a domain with $\partial\phi/\partial n = 0$ on the whole boundary gives $`\int f\,dA = 0`$. When the source violates this condition no solution exists. The residual of the iteration then stops decreasing at a level set by the incompatible part of $f$, and the mean of $\phi$ drifts by a constant amount per sweep. In an incompressible solver the same thing happens to the pressure equation when the boundary mass fluxes do not balance.

## Implementation

- `exact_solution(x, y)` and `exact_wall_flux()` give $\phi$ and $Q = 2 + 2/\sinh\pi$.
- `setup(n, dtype)` builds the grid, the source and the boundary values; `residual(phi, f, h)` and `gauss_seidel_sweep(phi, f, h)` (red-black, strided slices) do the iteration.
- `wall_flux(phi, h)` uses the second-order one-sided difference $(-3\phi_0 + 4\phi_1 - \phi_2)/(2h)$ and the trapezoid rule.
- `direct_solution(n)` assembles the five-point matrix with `scipy.sparse.kron` and solves it with `spsolve`.
- `monitored_solve(n, sweeps, dtype, keep)` runs the sweeps and returns the histories and the profiles at the sweeps in `keep`.
- `neumann_solve(n, sweeps, mean_source)` solves the cell-centred Neumann problem with mirrored ghost cells and returns the residual and the mean of $\phi$ per sweep.
- `first_sweep_below(values, threshold)` returns the sweep after which a history stays below a threshold.
- Constants: `N`, `MAX_SWEEPS`, `FLUX_BAND`, `PROFILE_SWEEPS`, `NEUMANN_N`, `NEUMANN_SWEEPS`, `NEUMANN_MEAN_SOURCE`.

## Usage

```bash
python main.py                                  # 2500 sweeps, print the summary and show the figure
python main.py --no-show --output .             # save residual_monitoring.png without opening a window
python main.py --no-show --output out --steps 10  # quick run (raised to 1000 sweeps for the profiles)
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |
| `--steps N` | Number of Gauss–Seidel sweeps (default 2500, at least 1000) |

## Output

The discretisation error of the converged solution is $7.55 \times 10^{-4}$, and the discrete flux is $Q_h = 2.17918$ against the exact $Q = 2.17318$. The measured error ratio per sweep is 0.99039, equal to $\cos^2(\pi h)$.

| Residual drop $`\Vert r^k\Vert/\Vert r^0\Vert`$ | Sweep | Iterative error | Flux deviation $\lvert Q^k - Q_h\rvert/Q_h$ |
| --- | --- | --- | --- |
| $10^{-3}$ | 515 | $6.5 \times 10^{-3}$ | $8.4 \times 10^{-3}$ |
| $10^{-4}$ | 753 | $6.5 \times 10^{-4}$ | $8.5 \times 10^{-4}$ |
| $10^{-5}$ | 992 | $6.5 \times 10^{-5}$ | $8.4 \times 10^{-5}$ |
| $10^{-6}$ | 1230 | $6.5 \times 10^{-6}$ | $8.5 \times 10^{-6}$ |

The iterative error falls below the discretisation error after 739 sweeps and the flux settles within 0.1% after 736. The single-precision residual stops at $1.4 \times 10^{-5}$. The incompatible Neumann problem stalls at a relative residual of 0.137 (the mean of $f$ alone is 0.0995 of $\Vert f\Vert$) while the mean of $\phi$ grows by $2.4 \times 10^{-5}$ per sweep; the compatible one reaches $1.6 \times 10^{-6}$ in 1500 sweeps and is still falling.

![Residual, error and flux histories, stalled residuals and solution profiles](residual_monitoring.png)

Panel (a) shows that after the first few sweeps every measure falls along the same line, but at different levels: a residual drop of three orders leaves an iterative error of 0.65%, 6.5 times the relative residual, and the change between iterates is two orders of magnitude below the error. Panel (b) shows the flux monitor settling at the same rate. Panel (c) shows the two stalls, and panel (d) shows that after 100 sweeps, when the residual has fallen to 5.5% of its initial value, the solution is still 36% away from the converged one.

## Related Notes

- [Iterative Convergence](../../../notes/numerical/cfd/iterative_convergence.md)
- [Direct and Iterative Solvers](../../../notes/numerical/cfd/direct_and_iterative_solvers.md)
