# Stability Regions of Time Integrators

This script draws the absolute-stability regions of explicit Euler, RK2, RK3, RK4, AB2 and BDF2 and overlays the eigenvalues of semi-discrete advection and diffusion operators, so the stable pairings of a spatial scheme and a time integrator can be read off directly. It also measures the order of accuracy of eight integrators on a smooth test equation, integrates a stiff equation on which explicit methods fail, and compares how the implicit methods damp very stiff modes.

## Overview

- Plots the boundary $|R(z)| = 1$, $z = \lambda\Delta t$, of the four explicit Runge–Kutta methods (filled inside) and the boundary loci of AB2 and BDF2.
- Overlays $\lambda\Delta t$ for the periodic semi-discrete operators on 64 Fourier modes: central advection at $C = 1$, first-order upwind advection at $C = 0.8$ and central diffusion at $r = 0.5$.
- Integrates $y' = y\cos t$, $y(0) = 1$ (exact $e^{\sin t}$) to $t = 2$ s with 10 to 320 steps using explicit Euler, implicit Euler, RK2 (Heun), AB2, BDF2, Crank–Nicolson, SSP-RK3 and RK4, and reports the observed order from the two finest runs.
- Integrates the Prothero–Robinson problem $y' = \lambda(y - \cos t) - \sin t$ with $\lambda = -1000$ s$`^{-1}`$ and $y(0) = 2$ with implicit Euler, BDF2 and Crank–Nicolson at $\Delta t = 0.05$ s ($\lambda\Delta t = -50$) and with RK4 at $\Delta t = 0.05$ s and $0.002$ s.
- Plots the growth factor per step on the negative real axis for implicit Euler, Crank–Nicolson, BDF2 and RK4.
- Prints the real- and imaginary-axis stability limits of the RK methods, the observed orders, the errors on the stiff problem and $|R(-50)|$ for each method.

## Mathematical Background

### Stability Function

Applied to the test equation $y' = \lambda y$, a one-step method gives $`y_{n+1} = R(z)\,y_n`$ with $z = \lambda\Delta t$. For an $s$-stage explicit RK method of order $s \le 4$,

```math
R(z) = \sum_{k=0}^{s} \frac{z^k}{k!}
```

and for implicit Euler and Crank–Nicolson $R(z) = 1/(1 - z)$ and $R(z) = (1 + z/2)/(1 - z/2)$. The method is absolutely stable where $|R(z)| \le 1$.

### Linear Multistep Methods

A two-step method $\sum_j \alpha_j y_{n+j} = \Delta t\sum_j \beta_j f_{n+j}$ applied to $y' = \lambda y$ has solutions $y_n = \xi^n$ with $`\rho(\xi) - z\,\sigma(\xi) = 0`$. The boundary of the stability region is the image of the unit circle under $z(\phi) = \rho(e^{\mathrm{i}\phi})/\sigma(e^{\mathrm{i}\phi})$. For AB2, $\rho = \xi^2 - \xi$ and $\sigma = (3\xi - 1)/2$; for BDF2, $\rho = \tfrac{3}{2}\xi^2 - 2\xi + \tfrac{1}{2}$ and $\sigma = \xi^2$, and the stable region lies outside the curve.

### Semi-Discrete Operators

On a periodic grid the Fourier mode $`e^{\mathrm{i}\,i\theta}`$ is an eigenvector of the difference operators, with

```math
\lambda\Delta t = -\mathrm{i}\,C\sin\theta \ \text{(central advection)}, \qquad
\lambda\Delta t = -C\left(1 - e^{-\mathrm{i}\theta}\right) \ \text{(upwind)}, \qquad
\lambda\Delta t = -4r\sin^2\frac{\theta}{2} \ \text{(central diffusion)}
```

The fully discrete scheme is stable when every scaled eigenvalue lies inside the region of the time integrator. Central advection gives a segment of the imaginary axis, which no part of the explicit Euler or RK2 region contains, but which RK3 contains up to $\sqrt{3}$ and RK4 up to $2\sqrt{2}$.

### Stiffness and L-Stability

A method is A-stable when its region contains the whole left half-plane and L-stable when, in addition, $|R(z)| \to 0$ as $z \to -\infty$. Crank–Nicolson is A-stable with $|R| \to 1$; implicit Euler and BDF2 are L-stable. The Prothero–Robinson solution is $y = \cos t + (y_0 - 1)e^{\lambda t}$: the transient lasts about $10^{-3}$ s and is then irrelevant, but an explicit method must still keep $|\lambda|\Delta t$ inside its region for the whole run.

## Implementation

- `rk_stability_function(name, z)`, `implicit_stability_function(name, z)` and `multistep_growth(name, z)` (largest root of $\rho - z\sigma$) evaluate the growth factors.
- `boundary_locus(name)` returns the AB2 or BDF2 boundary; `rk_boundary(name)` finds points with $|R(z)| = 1$ by bisection along rays from $z = -1$.
- `real_axis_limit(name)` and `imaginary_axis_limit(name)` scan the axes for the stability limits.
- `operator_eigenvalues(n, c, c_up, r)` returns the scaled eigenvalues of the three semi-discrete operators.
- `integrate(method, a, b, y0, t_end, n_steps)` integrates the linear equation $y' = a(t)y + b(t)$ with any of the eight methods, solving the implicit stages exactly. AB2 starts with one RK2 step and BDF2 with one implicit Euler step.
- `order_test_problem()`, `stiff_problem()`, `order_study()` and `observed_order(errors)` set up and evaluate the two test problems.
- Constants: `ADVECTION_COURANT`, `UPWIND_COURANT`, `DIFFUSION_NUMBER`, `N_MODES`, `ORDER_STEPS`, `STIFF_LAMBDA`, `STIFF_DT`, `STIFF_DT_EXPLICIT_STABLE`, `STIFF_PERTURBATION`.

## Usage

```bash
python main.py                          # print the limits and orders and show the figure
python main.py --no-show --output .     # save time_integrator_stability.png without opening a window
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

| Method | Real-axis limit | Imaginary-axis limit | Observed order | Error at $\Delta t = 0.00625$ s |
| --- | --- | --- | --- | --- |
| Explicit Euler | $-2$ | 0 | 0.999 | $4.7 \times 10^{-3}$ |
| RK2 | $-2$ | 0 | 2.004 | $1.8 \times 10^{-5}$ |
| SSP-RK3 | $-2.5128$ | 1.7321 | 2.997 | $6.5 \times 10^{-8}$ |
| RK4 | $-2.7853$ | 2.8284 | 4.003 | $1.6 \times 10^{-11}$ |
| Implicit Euler |  |  | 1.001 | $4.7 \times 10^{-3}$ |
| AB2 |  |  | 1.997 | $6.0 \times 10^{-5}$ |
| BDF2 |  |  | 1.980 | $2.4 \times 10^{-5}$ |
| Crank–Nicolson |  |  | 2.000 | $1.2 \times 10^{-5}$ |

On the stiff problem with $\lambda\Delta t = -50$: $|R| = 0.0196$ for implicit Euler, 0.0985 for BDF2, 0.923 for Crank–Nicolson and $2.4 \times 10^5$ for RK4. The largest error of implicit Euler and BDF2 is 0.0196, the remnant of the transient after the first step (BDF2 takes that step with implicit Euler), and the error is below $10^{-3}$ from the third step on; Crank–Nicolson carries an oscillation of amplitude up to 0.92 that decays by only 8% per step, and RK4 overflows. RK4 with $\Delta t = 0.002$ s ($|\lambda|\Delta t = 2$, inside its limit of 2.785) is accurate but needs 1000 steps.

![Stability regions, order of accuracy, stiff test and damping of stiff modes](time_integrator_stability.png)

Panel (a) shows the stability regions with the operator eigenvalues: the upwind circle fits inside the explicit Euler disc, the diffusion segment reaches its edge at $-2$, and the central-advection segment on the imaginary axis is only covered by RK3 and RK4. Panel (b) shows the errors with their observed orders. Panel (c) shows the stiff problem, and panel (d) explains it: on the negative real axis the growth factor of RK4 exceeds 1 beyond $-2.785$, Crank–Nicolson tends to 1, and implicit Euler and BDF2 tend to 0.

## Related Notes

- [Time Integration](../../../notes/numerical/cfd/time_integration.md)
- [Numerical Stability](../../../notes/numerical/cfd/numerical_stability.md)
