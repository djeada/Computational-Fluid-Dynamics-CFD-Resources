# Discontinuous Galerkin Linear Advection

This script solves the 1D periodic linear advection equation $`u_t + a\,u_x = 0`$ with the discontinuous Galerkin (DG) method, using Legendre polynomials of degree $p = 0$ to 3 in every element, an upwind numerical flux and the three-stage SSP Runge–Kutta method, and confirms that the error falls as $h^{p+1}$. It also advects a Gaussian pulse and a square pulse through one period on a coarse mesh to show how the polynomial degree affects resolution and how a discontinuity produces over- and undershoots when no limiter is used.

## Overview

- Represents the solution in each of $K$ uniform elements by $p + 1$ Legendre coefficients; the mass matrix is diagonal in this basis.
- Computes the volume integrals exactly with Gauss quadrature and couples elements only through the upwind flux at their faces.
- Advances in time with SSP-RK3 and $`\Delta t = 0.5\,h/((2p + 1)|a|)`$; for $p \ge 2$ the convergence study reduces $\Delta t$ further so that the third-order time error does not hide the spatial order.
- Projects the initial data with an $L^2$ projection and measures the $L^2$ error with 12-point Gauss quadrature per element.
- Runs a smooth wave $\sin 2\pi x$ through one period on 4 to 256 elements for each $p$, and a Gaussian plus square pulse on 20 elements for $p = 1$ and $p = 3$.
- Offers a central flux (`flux="central"`) for comparison; the tests use it to check that it conserves the discrete energy.

## Mathematical Background

On element $I_k = [x_{k-1/2}, x_{k+1/2}]$ of size $h$, with $x = x_k + (h/2)\xi$, the solution is $`u_h = \sum_{m=0}^{p} c_{k,m}(t)\,P_m(\xi)`$. Multiplying by $P_m$, integrating over $I_k$ and integrating the flux term by parts gives

```math
\frac{h}{2m+1}\frac{dc_{k,m}}{dt} = a\sum_{n=0}^{p} S_{mn}\,c_{k,n} - \left[\hat f_{k+1/2}\,P_m(1) - \hat f_{k-1/2}\,P_m(-1)\right],
\qquad S_{mn} = \int_{-1}^{1} P_m'(\xi)\,P_n(\xi)\,d\xi
```

with $P_m(1) = 1$ and $P_m(-1) = (-1)^m$. The upwind flux for $a > 0$ takes the value from the element on the left of the face, $`\hat f_{k+1/2} = a\,u_h(x_{k+1/2}^-)`$. With $p = 0$ the scheme is the first-order upwind finite volume scheme. The time integrator is

```math
c^{(1)} = c^n + \Delta t\,L(c^n), \quad
c^{(2)} = \tfrac{3}{4}c^n + \tfrac{1}{4}\left(c^{(1)} + \Delta t\,L(c^{(1)})\right), \quad
c^{n+1} = \tfrac{1}{3}c^n + \tfrac{2}{3}\left(c^{(2)} + \Delta t\,L(c^{(2)})\right)
```

For smooth solutions the upwind DG error is $O(h^{p+1})$ in $L^2$. The upwind flux dissipates energy at the faces in proportion to the squared jumps of $u_h$; the central flux conserves the semi-discrete energy $`\|u_h\|^2`$.

## Implementation

- `legendre_values(xi, degree)` evaluates $P_0, \dots, P_p$; `volume_matrix(degree)` integrates $S_{mn}$.
- `DGAdvection(n_elements, degree, speed, flux)` holds the mesh and operators. Its methods are `project`, `face_flux`, `rhs`, `stable_dt`, `ssp_rk3_step`, `advance`, `evaluate`, `l2_error`, `mass` and `energy`.
- `convergence_study(degrees, n_values)` runs the smooth-wave refinement study; `observed_orders` computes the slopes.
- Constants `ADVECTION_SPEED`, `DOMAIN_LENGTH`, `CFL_BASE`, `DEGREES`, `N_ELEMENTS_STUDY`, `N_ELEMENTS_PLOT` and `N_QUAD` set the experiment.

## Usage

```bash
python main.py                          # print the error tables and show the figure
python main.py --no-show --output .     # save dg_linear_advection.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

On 256 elements the $L^2$ errors after one period are $5.3 \times 10^{-2}$ ($p = 0$), $2.6 \times 10^{-5}$ ($p = 1$), $5.1 \times 10^{-8}$ ($p = 2$) and $7.7 \times 10^{-11}$ ($p = 3$), with observed orders 0.95, 2.00, 3.00 and 4.00 on the last refinement. For the pulses on 20 elements the $L^2$ error is 0.177 for $p = 1$ and 0.086 for $p = 3$; the solution ranges over $[-0.087, 1.130]$ and $[-0.097, 1.098]$ instead of $[0, 1]$, the mass changes by less than $3 \times 10^{-15}$, and the upwind flux removes 20% ($p = 1$) and 3.5% ($p = 3$) of the energy $`\|u_h\|^2`$.

![DG solutions after one period and convergence](dg_linear_advection.png)

Panels (a) and (b) show the pulses after one period with each element's polynomial drawn separately, so the jumps between elements are visible. With $p = 1$ (40 unknowns) the Gaussian has lost a third of its height; with $p = 3$ (80 unknowns) it is nearly exact, but the square pulse carries oscillations of about 10% next to each discontinuity, which a slope limiter would remove. Panel (c) shows each error curve parallel to its dotted $h^{p+1}$ reference line.

## Related Notes

- [High-Order Methods](../../../notes/numerical/high_order/intro.md)
- [Finite Element Method](../../../notes/numerical/fem/intro.md)
