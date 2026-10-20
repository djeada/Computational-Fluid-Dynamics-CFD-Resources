# Finite Difference Method

The finite difference method (FDM) replaces the derivatives in a differential equation by difference quotients of the unknown at the points of a grid. Each grid point then contributes one algebraic equation, and the differential problem becomes a system of linear or nonlinear equations for the nodal values. The method is the most direct of the discretization techniques and the easiest to analyse, which is why the vocabulary used for every other method (truncation error, order of accuracy, consistency, stability) is introduced with it.

In CFD the FDM is used on structured grids: rectangular or mapped domains, spectral and compact schemes for direct numerical simulation, and the time-stepping parts of almost every solver. Unstructured industrial solvers use the [finite volume method](../fvm/intro.md) instead, but its face interpolations and gradients are finite differences in disguise. This note derives the basic formulas, assembles a boundary-value problem, and points to the stability theory. The systematic construction of arbitrary stencils, compact schemes and the modified-wavenumber analysis are in [Systematic Finite-Difference Discretization](./discretization.md).

## Problem Statement

Given a linear differential operator $\mathcal{L}$, a source $f$ and boundary conditions on a domain $\Omega$, find $\phi$ with

$$
\mathcal{L}\phi = f \quad \text{in } \Omega
$$

The model problem used below is the 1D Poisson equation

$$
-\frac{d^2\phi}{dx^2} = f(x), \quad 0 < x < 1,
\qquad \phi(0) = \phi_L, \quad \phi(1) = \phi_R
$$

and its 2D and time-dependent analogues. The finite difference solution is a grid function $\phi_i \approx \phi(x_i)$ that satisfies a discrete equation $\mathcal{L}_h\phi_h = f_h$ at every interior node. The problem is solved when the global error

```math
e_h = \max_i |\phi_i - \phi(x_i)|
```

falls below a tolerance and decreases as $O(h^p)$ under grid refinement, with $p$ the formal order of the scheme. The difficulties are:

- choosing difference formulas whose error vanishes fast enough as $h \to 0$ without losing stability;
- imposing boundary conditions, especially derivative conditions and curved boundaries, without degrading the order;
- solving the resulting large sparse systems, whose condition number grows like $h^{-2}$;
- for time-dependent problems, choosing $\Delta t$ so that errors do not grow from step to step.

## Grids and Grid Functions

A uniform 1D grid on $[0, L]$ has nodes $x_i = ih$, $i = 0, \dots, N$, with spacing $h = \Delta x = L/N$. A grid function assigns a value $\phi_i$ to every node. In 2D the nodes are $(x_i, y_j) = (i\Delta x, j\Delta y)$ with values $\phi_{i,j}$, and in time-dependent problems a superscript gives the time level, $\phi_i^n \approx \phi(x_i, t^n)$ with $t^n = n\Delta t$.

The values $\phi_0$ and $\phi_N$ on a Dirichlet boundary are known. The unknowns are the interior values $\phi_1, \dots, \phi_{N-1}$, and every interior node needs one equation.

## Difference Quotients From Taylor Series

Expanding the neighbours of $x_i$ in Taylor series about $x_i$ gives

```math
\phi_{i\pm1} = \phi_i \pm h\phi'_i + \frac{h^2}{2}\phi''_i \pm \frac{h^3}{6}\phi'''_i + \frac{h^4}{24}\phi''''_i \pm \dots
```

Solving the "+" expansion for $\phi'_i$ gives the forward difference, the "−" expansion the backward difference, and subtracting the two the central difference:

```math
\frac{\phi_{i+1} - \phi_i}{h} = \phi'_i + \frac{h}{2}\phi''_i + O(h^2),
\qquad
\frac{\phi_i - \phi_{i-1}}{h} = \phi'_i - \frac{h}{2}\phi''_i + O(h^2),
\qquad
\frac{\phi_{i+1} - \phi_{i-1}}{2h} = \phi'_i + \frac{h^2}{6}\phi'''_i + O(h^4)
```

Adding the two expansions cancels the odd derivatives and gives the three-point second derivative,

```math
\frac{\phi_{i+1} - 2\phi_i + \phi_{i-1}}{h^2} = \phi''_i + \frac{h^2}{12}\phi''''_i + O(h^4)
```

The difference between a difference quotient and the derivative it replaces, evaluated on the exact solution, is the **truncation error** $\tau$. A formula is of order $p$ when $\tau = O(h^p)$. The leading term also tells which derivative of the solution controls the error, which is why central differences are exact for quadratics and the three-point second derivative is exact for cubics.

| Approximation | Formula | Leading truncation error | Order |
| --- | --- | --- | --- |
| Forward, $\phi'$ | $(\phi_{i+1} - \phi_i)/h$ | $\tfrac{h}{2}\phi''$ | 1 |
| Backward, $\phi'$ | $(\phi_i - \phi_{i-1})/h$ | $-\tfrac{h}{2}\phi''$ | 1 |
| Central, $\phi'$ | $(\phi_{i+1} - \phi_{i-1})/(2h)$ | $\tfrac{h^2}{6}\phi'''$ | 2 |
| One-sided, $\phi'$ | $(3\phi_i - 4\phi_{i-1} + \phi_{i-2})/(2h)$ | $-\tfrac{h^2}{3}\phi'''$ | 2 |
| Central, $\phi'$ | $(-\phi_{i+2} + 8\phi_{i+1} - 8\phi_{i-1} + \phi_{i-2})/(12h)$ | $-\tfrac{h^4}{30}\phi^{(5)}$ | 4 |
| Central, $\phi''$ | $(\phi_{i+1} - 2\phi_i + \phi_{i-1})/h^2$ | $\tfrac{h^2}{12}\phi''''$ | 2 |

The one-sided second-order formula is the one used at a boundary, where there is no neighbour on one side. The general recipe behind the table, valid for any set of points and any derivative, is in [Systematic Finite-Difference Discretization](./discretization.md#the-method-of-undetermined-coefficients).

### Truncation Error Against Round-Off

The order of a formula is only visible over a range of $h$. As $h$ shrinks, the truncation error falls like $h^p$, but the samples $\phi_{i\pm1}$ become nearly equal and their difference loses digits: the rounding error of about $`\epsilon_{\mathrm{mach}}|\phi|`$ in each sample is divided by $h$. The total error of a first-derivative formula is roughly

```math
E(h) \approx C h^p + \frac{\epsilon_{\mathrm{mach}}|\phi|}{h},
\qquad
h_{\mathrm{opt}} \sim \epsilon_{\mathrm{mach}}^{1/(p+1)}
```

with $`\epsilon_{\mathrm{mach}} = 2.2 \times 10^{-16}`$ in double precision. A forward difference cannot be more accurate than about $10^{-8}$, whatever $h$ is used. In a PDE solve on realistic grids $h$ is far above $h_{\mathrm{opt}}$ and truncation error dominates, but the floor matters when derivatives are computed by finite differences for Jacobians or sensitivities.

![Error of finite-difference derivatives against h, and modified wavenumbers](../../../scripts/algorithms/finite_difference_stencils/finite_difference_stencils.png)

Panel (a) shows the error in $f'(1)$ for $f = e^{\sin x}$: each formula follows the slope of its order on the right and meets the rising round-off line on the left. The forward difference bottoms out at $9.5 \times 10^{-9}$ for $h = 10^{-8}$, the second-order central difference at $1.1 \times 10^{-11}$ for $h \approx 3 \times 10^{-6}$, and the fourth-order one at $3.2 \times 10^{-13}$ for $h \approx 3 \times 10^{-4}$. Panels (b) and (c) are discussed in [Systematic Finite-Difference Discretization](./discretization.md#modified-wavenumber-analysis).

## A 1D Boundary-Value Problem

Replacing $-\phi''$ by the three-point formula at every interior node of the model problem gives

```math
\frac{-\phi_{i-1} + 2\phi_i - \phi_{i+1}}{h^2} = f_i, \qquad i = 1, \dots, N-1
```

The boundary values $\phi_0 = \phi_L$ and $\phi_N = \phi_R$ are known, so they move to the right-hand side of the first and last equations. In matrix form,

```math
\frac{1}{h^2}
\begin{pmatrix}
2 & -1 & & & \\
-1 & 2 & -1 & & \\
 & \ddots & \ddots & \ddots & \\
 & & -1 & 2 & -1 \\
 & & & -1 & 2
\end{pmatrix}
\begin{pmatrix} \phi_1 \\ \phi_2 \\ \vdots \\ \phi_{N-2} \\ \phi_{N-1} \end{pmatrix}
=
\begin{pmatrix} f_1 + \phi_L/h^2 \\ f_2 \\ \vdots \\ f_{N-2} \\ f_{N-1} + \phi_R/h^2 \end{pmatrix}
```

The matrix $A$ is tridiagonal, symmetric and positive definite, and the system is solved in $O(N)$ operations by the Thomas algorithm (Gaussian elimination without fill-in). Its eigenvalues are $`\lambda_k = (4/h^2)\sin^2(k\pi h/2)`$, $k = 1, \dots, N-1$, so the condition number is

```math
\kappa(A) = \frac{\lambda_{N-1}}{\lambda_1} \approx \frac{4}{\pi^2 h^2}
```

This $h^{-2}$ growth is why iterative solvers slow down on fine grids; see [Direct and Iterative Solvers](../cfd/direct_and_iterative_solvers.md).

### Worked Example

Take $f = \pi^2\sin(\pi x)$ with $\phi_L = \phi_R = 0$, whose exact solution is $\phi = \sin(\pi x)$. With $N = 4$ ($h = 1/4$) there are three unknowns:

```math
16\begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}
\begin{pmatrix} \phi_1 \\ \phi_2 \\ \phi_3 \end{pmatrix}
= \pi^2\begin{pmatrix} 0.7071 \\ 1 \\ 0.7071 \end{pmatrix}
```

The solution is $(\phi_1, \phi_2, \phi_3) = (0.7446, 1.0530, 0.7446)$, against the exact $(0.7071, 1, 0.7071)$. Because $\sin(\pi x_i)$ is an eigenvector of the discrete operator, the discrete solution is the exact one multiplied by $`\pi^2 h^2/(4\sin^2(\pi h/2)) = 1.0530`$. The maximum error falls from $5.30 \times 10^{-2}$ ($N = 4$) to $1.30 \times 10^{-2}$ ($N = 8$), $3.22 \times 10^{-3}$ ($N = 16$) and $8.04 \times 10^{-4}$ ($N = 32$): a factor of 4 per halving of $h$, as expected for a second-order scheme.

### Derivative Boundary Conditions

A Neumann condition $\phi'(1) = g$ makes $\phi_N$ an unknown. Two treatments keep second order:

1. Add a ghost node $x_{N+1}$, impose $(\phi_{N+1} - \phi_{N-1})/(2h) = g$, and use the interior equation at $i = N$. Eliminating $\phi_{N+1}$ gives $(2\phi_N - 2\phi_{N-1})/h^2 = f_N + 2g/h$.
2. Use the one-sided formula $(3\phi_N - 4\phi_{N-1} + \phi_{N-2})/(2h) = g$ as the last equation. This breaks the symmetry and the tridiagonal structure of $A$ slightly.

The first-order alternative $(\phi_N - \phi_{N-1})/h = g$ is simpler, but its $O(h)$ error at the boundary pollutes the whole solution and reduces the global order to 1. Boundary conditions for flow problems are covered in [Boundary Conditions](../cfd/boundary_conditions.md).

## The Five-Point Laplacian in 2D

On a uniform grid with $\Delta x = \Delta y = h$, applying the three-point formula in each direction gives

```math
\nabla^2\phi\big|_{i,j} \approx \frac{\phi_{i+1,j} + \phi_{i-1,j} + \phi_{i,j+1} + \phi_{i,j-1} - 4\phi_{i,j}}{h^2},
\qquad
\tau = \frac{h^2}{12}\left(\frac{\partial^4\phi}{\partial x^4} + \frac{\partial^4\phi}{\partial y^4}\right) + O(h^4)
```

The stencil couples each node to its four neighbours, $(i\pm1, j)$ and $(i, j\pm1)$. For the Poisson equation on the unit square with $N$ intervals in each direction there are $(N-1)^2$ unknowns. Numbering them row by row ("lexicographic" order) gives a block tridiagonal matrix

```math
A = \frac{1}{h^2}\begin{pmatrix} T & -I & & \\ -I & T & -I & \\ & \ddots & \ddots & \ddots \\ & & -I & T \end{pmatrix},
\qquad
T = \mathrm{tridiag}(-1, 4, -1)
```

with $N - 1$ blocks of size $(N-1) \times (N-1)$. The matrix has at most five non-zeros per row but a bandwidth of $N - 1$, so a banded direct solve costs $O(N^4)$ and fills in the band. Iterative methods (conjugate gradients, multigrid) or fast Poisson solvers based on the FFT are used instead. The condition number is again about $4/(\pi^2 h^2)$, and in 3D the seven-point stencil gives $(N-1)^3$ unknowns and a bandwidth of $(N-1)^2$.

## Non-Uniform Grids

Boundary layers and shear layers need small spacing in one region only, so CFD grids are stretched. With $h_- = x_i - x_{i-1}$ and $h_+ = x_{i+1} - x_i$, Taylor expansion gives

```math
\phi'_i \approx \frac{h_-^2\,\phi_{i+1} + (h_+^2 - h_-^2)\,\phi_i - h_+^2\,\phi_{i-1}}{h_+ h_-(h_+ + h_-)},
\qquad
\phi''_i \approx \frac{2}{h_+ + h_-}\left(\frac{\phi_{i+1} - \phi_i}{h_+} - \frac{\phi_i - \phi_{i-1}}{h_-}\right)
```

The first-derivative formula is second order on any grid. The second-derivative formula has truncation error $\tfrac{1}{3}(h_+ - h_-)\phi''' + O(h^2)$, which is first order for an arbitrary grid but second order when the spacing varies smoothly, $h_+ - h_- = O(h^2)$, as for a geometric stretching with a ratio $r = h_+/h_- = 1 + O(h)$. This is the reason for the usual meshing advice to keep the growth ratio of adjacent cells below about 1.2; see [Boundary-Layer Meshing](../../../practice/mesh_generation/boundary_layers.md). An alternative is to map the stretched grid to a uniform computational coordinate $\xi$ with $x = x(\xi)$ and use $`d/dx = (1/x_\xi)\,d/d\xi`$ with uniform differences in $\xi$.

## Time-Dependent Problems

For the heat equation $\phi_t = \alpha\phi_{xx}$, a forward difference in time and the three-point formula in space give the explicit FTCS scheme

```math
\phi_i^{n+1} = \phi_i^n + r\left(\phi_{i+1}^n - 2\phi_i^n + \phi_{i-1}^n\right),
\qquad
r = \frac{\alpha\,\Delta t}{h^2}
```

It is first order in time and second order in space, and it is stable only for $r \le 1/2$, that is $`\Delta t \le h^2/(2\alpha)`$ (in 2D with $\Delta x = \Delta y = h$, $`\Delta t \le h^2/(4\alpha)`$). For the advection equation the corresponding restriction is the CFL condition $C = u\Delta t/\Delta x \le C_{\max}$. Implicit schemes such as backward Euler and Crank–Nicolson remove the restriction at the cost of a linear solve per step. Time integration is treated in [Time Integration](../cfd/time_integration.md).

## Consistency, Stability and Convergence

A scheme is **consistent** if its truncation error tends to zero as $h, \Delta t \to 0$, **stable** if errors (from round-off, initial data or the truncation error itself) are not amplified without bound as the grid is refined, and **convergent** if the discrete solution tends to the exact one. For a well-posed linear initial-value problem, the Lax equivalence theorem states that a consistent scheme converges if and only if it is stable. For a steady boundary-value problem the analogous statement is $`\|e_h\| \le \|A^{-1}\|\,\|\tau\|`$: if $`\|A^{-1}\|`$ is bounded independently of $h$ (stability), the global error has the order of the truncation error. For the 1D Poisson matrix above, $`\|A^{-1}\|_2 = 1/\lambda_1 \approx 1/\pi^2`$.

Von Neumann analysis, which checks stability by inserting a Fourier mode $\phi_i^n = G^n e^{\mathrm{i}kx_i}$ and requiring the amplification factor to satisfy $|G| \le 1$, and the CFL condition are derived in [Numerical Stability](../cfd/numerical_stability.md).

## Pitfalls

- An $O(h)$ boundary formula reduces the global order of an otherwise second-order scheme. Check the order of every boundary closure.
- Central differences for a convection term $`u\,\phi_x`$ produce node-to-node oscillations when the cell Péclet number $u h/\nu$ exceeds 2. Upwind and bounded schemes are discussed in [Convection Schemes](../fvm/convection_schemes.md).
- Second-derivative formulas on abruptly stretched grids are only first order. Keep the stretching smooth.
- The explicit time-step limit for diffusion falls by a factor of 4 each time $h$ is halved, so doubling the resolution of the explicit heat equation costs 8 times the work in 1D.
- The observed order on coarse grids can differ from the formal order. Measure it on at least three grids before quoting it; see [Verification and Validation](../cfd/verification_and_validation.md).
- Curved boundaries do not fit a Cartesian grid. Boundary-fitted coordinate maps or immersed-boundary corrections are needed, and both complicate the formulas.

## Key Takeaways

- Every finite difference formula follows from Taylor series; the first neglected term is the truncation error and its power of $h$ is the order.
- Central differences are second order with three points; one-sided formulas need an extra point for the same order.
- The 1D Poisson problem gives a tridiagonal system and the 2D problem a five-point, block-tridiagonal one, with condition numbers growing like $h^{-2}$.
- Round-off sets a floor below which reducing $h$ makes a difference quotient worse.
- Convergence needs consistency and stability; the order of the global error is set by the worst truncation error, often at a boundary.

## Related Scripts

- [Finite-Difference Stencils](../../../scripts/algorithms/finite_difference_stencils/): computes finite-difference weights for any set of stencil offsets by solving the Taylor-series (Vandermonde) system, then measures how the error of each stencil depends on the grid spacing and how well it represents each Fourier wavenumber.
- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [Variation of Residual with Iteration](../../../scripts/plots/variation_of_residual/): solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale.
- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Gray-Scott Reaction-Diffusion Simulation](../../../scripts/simulations/gray_scott_reaction_diffusion/): simulates the Gray-Scott reaction-diffusion system, in which two chemicals that react and diffuse on a periodic square turn a small seeded square into self-replicating spots or branching coral, and animates the concentration of one of them with Matplotlib.
- [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/): solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error.

## Exercises

**Exercise 1.** Use Taylor expansions of $\phi_{i+1}$ and $\phi_{i-1}$ about $x_i$ to show that the central difference $(\phi_{i+1} - \phi_{i-1})/(2h)$ has truncation error $O(h^2)$ and the forward difference $(\phi_{i+1} - \phi_i)/h$ has $O(h)$. Find the leading error terms.

<details>
<summary>Answer</summary>

$`\phi_{i\pm1} = \phi_i \pm h\phi' + \frac{h^2}{2}\phi'' \pm \frac{h^3}{6}\phi''' + O(h^4)`$. Therefore:

- Forward: $`(\phi_{i+1} - \phi_i)/h = \phi' + \frac{h}{2}\phi'' + O(h^2)`$, which is first order.
- Central: subtracting the two expansions, $`(\phi_{i+1} - \phi_{i-1})/(2h) = \phi' + \frac{h^2}{6}\phi''' + O(h^4)`$, which is second order.

</details>

**Exercise 2.** For $\phi = \sin x$ at $x = 1$, compute the errors of the forward and central differences with $h = 0.1$ and $h = 0.05$, and check the observed orders of accuracy.

<details>
<summary>Answer</summary>

The exact derivative is $\cos 1 = 0.5403$.

| $h$ | forward error | central error |
| --- | --- | --- |
| 0.1 | $-4.29 \times 10^{-2}$ | $-9.00 \times 10^{-4}$ |
| 0.05 | $-2.13 \times 10^{-2}$ | $-2.25 \times 10^{-4}$ |

Halving $h$ divides the forward error by 2.02 and the central error by 4.00, confirming orders 1 and 2. The signs match the leading terms from Exercise 1: $`\frac{h}{2}\phi'' = -\frac{h}{2}\sin 1`$ and $`\frac{h^2}{6}\phi''' = -\frac{h^2}{6}\cos 1`$.

</details>

**Exercise 3.** Apply the three-point second-derivative formula to $\phi = x^4$ at $x = 1$ with $h = 0.1$. Compare with the exact value, and show that the error equals $\frac{h^2}{12}\phi''''$ exactly for this function.

<details>
<summary>Answer</summary>

$(1.1^4 - 2 + 0.9^4)/0.01 = 12.02$, while the exact value is $\phi'' = 12x^2 = 12$.

The Taylor error series is $`\frac{h^2}{12}\phi'''' + \frac{h^4}{360}\phi^{(6)} + \dots`$. Here $\phi'''' = 24$ and all higher derivatives vanish, so the error is exactly $0.01 \times 24/12 = 0.02$.

</details>

**Exercise 4.** A steel rod ($`\alpha = 1.2 \times 10^{-5}\ \mathrm{m^2/s}`$) of length $L = 0.1$ m is modelled with the explicit FTCS scheme using $N = 50$ intervals. (a) What is the largest stable time step, and how many steps does 60 s of simulated time take? (b) Repeat for $N = 100$. (c) What is the limit on a uniform 2D grid with $\Delta x = \Delta y = h$?

<details>
<summary>Answer</summary>

(a) $h = 0.002$ m and $`\Delta t \le h^2/(2\alpha) = 4 \times 10^{-6}/(2.4 \times 10^{-5}) = 0.167`$ s, so 60 s takes 360 steps.

(b) $h = 0.001$ m and $\Delta t \le 0.0417$ s, so 60 s takes 1440 steps. Doubling the resolution costs 8 times the work: twice the points and four times the steps.

(c) In 2D, $`\Delta t \le 1/(2\alpha(1/\Delta x^2 + 1/\Delta y^2)) = h^2/(4\alpha)`$. For $h = 0.002$ m that is 0.083 s.

</details>

**Exercise 5.** Take $L = 1$, $N = 4$ ($h = 0.25$), $\alpha = 1$, boundary values $\phi_0 = \phi_4 = 0$ and interior initial values $(0.5, 1, 0.5)$. (a) Advance one FTCS step with $\Delta t = 0.025$. (b) For the mode $\phi_i^n = G^n e^{\mathrm{i}kx_i}$, von Neumann analysis gives the amplification factor $G = 1 - 4r\sin^2(kh/2)$. Evaluate $|G|$ for the sawtooth mode $kh = \pi$ with $r = 0.4$ and $r = 0.6$, and explain the limit $r \le 1/2$.

<details>
<summary>Answer</summary>

(a) $r = 0.025/0.0625 = 0.4$. Then:

- $\phi_1^{1} = 0.5 + 0.4(1 - 1 + 0) = 0.5$
- $\phi_2^{1} = 1 + 0.4(0.5 - 2 + 0.5) = 0.6$
- $\phi_3^{1} = 0.5$ by symmetry.

(b) For $kh = \pi$, $G = 1 - 4r$:

- $r = 0.4$: $G = -0.6$ and $|G| < 1$, so the mode decays.
- $r = 0.6$: $G = -1.4$ and $|G| > 1$, so the sawtooth grows by 40% per step, flipping sign each time.

Requiring $|G| \le 1$ for every $k$ gives $4r \le 2$, that is $r \le 1/2$, which is the condition $`\Delta t \le h^2/(2\alpha)`$.

</details>

## References

- R. J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems*, SIAM, 2007.
- J. C. Strikwerda, *Finite Difference Schemes and Partial Differential Equations*, 2nd ed., SIAM, 2004.
- K. W. Morton and D. F. Mayers, *Numerical Solution of Partial Differential Equations: An Introduction*, 2nd ed., Cambridge University Press, 2005.
- J. H. Ferziger, M. Perić and R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- C. Hirsch, *Numerical Computation of Internal and External Flows, Vol. 1: Fundamentals of Computational Fluid Dynamics*, 2nd ed., Butterworth-Heinemann, 2007.
- P. D. Lax and R. D. Richtmyer, "Survey of the stability of linear finite difference equations", *Communications on Pure and Applied Mathematics*, 9(2), 267–293, 1956.
