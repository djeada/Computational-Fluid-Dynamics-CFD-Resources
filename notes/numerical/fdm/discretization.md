# Systematic Finite-Difference Discretization

The [Finite Difference Method](./intro.md) note derives the standard two- and three-point formulas by hand. This note turns the derivation into a procedure that produces the weights for any derivative on any set of points, applies a derived stencil to a marching problem, introduces compact (Padé) schemes that reach high order on narrow stencils, and analyses all of them in Fourier space. The Fourier view (the modified wavenumber) is what decides how many grid points per wavelength a scheme needs, which is the practical question when choosing a scheme for wave propagation, aeroacoustics, or direct and large-eddy simulation of turbulence.

## Problem Statement

Given $n$ nodes $x_i + s_j h$, $j = 0, \dots, n-1$, around a point $x_i$ (the offsets $s_j$ need not be integers or symmetric) and a derivative order $m < n$, find weights $w_j$ such that

```math
\frac{d^m\phi}{dx^m}\bigg|_{x_i} = \frac{1}{h^m}\sum_{j=0}^{n-1} w_j\,\phi(x_i + s_j h) + O(h^p)
```

with the order $p$ as high as possible, and determine the leading error term. For a periodic problem, also determine how accurately the resulting operator differentiates a Fourier mode $e^{\mathrm{i}kx}$ for each $k\Delta x \in [0, \pi]$: the error in its phase (dispersion) and its amplitude (dissipation). A scheme is satisfactory when it reaches the required accuracy with the fewest points per wavelength at an acceptable cost per point. The difficulties are that wide stencils are ill-conditioned to compute and awkward near boundaries, that high formal order says nothing about poorly resolved waves, and that compact schemes need a linear solve for every derivative.

## The Method of Undetermined Coefficients

Write the Taylor expansion of each sample about $x_i$,

```math
\phi(x_i + s_j h) = \sum_{k=0}^{\infty} \frac{(s_j h)^k}{k!}\,\phi^{(k)}_i
```

and require that the weighted sum reproduces $h^m\phi^{(m)}_i$ term by term for $k = 0, \dots, n-1$:

```math
\sum_{j=0}^{n-1} w_j\,\frac{s_j^k}{k!} = \delta_{km}, \qquad k = 0, 1, \dots, n-1
```

These $n$ equations for $n$ weights form a (transposed) Vandermonde system, which has a unique solution whenever the offsets are distinct. The first index $q \ge n$ for which the moment $`\mu_q = \sum_j w_j s_j^q/q!`$ is not zero gives the truncation error,

```math
\tau = \mu_q\,h^{q-m}\,\phi^{(q)}_i + \dots, \qquad p = q - m \ge n - m
```

On a symmetric stencil the moments whose index has the opposite parity to $m$ vanish by symmetry, so the order is one higher than $n - m$ whenever $n - m$ is odd. That is why the three-point second derivative is second order and not first.

### A Taylor Table

For a one-sided first derivative at a left boundary with offsets $0, 1, 2$, arrange the Taylor coefficients in a table. Each row is one sample, each column one term of the expansion:

| Sample | $\phi_i$ | $h\phi'_i$ | $h^2\phi''_i$ | $h^3\phi'''_i$ |
| --- | --- | --- | --- | --- |
| $`w_0\,\phi_i`$ | $w_0$ | 0 | 0 | 0 |
| $`w_1\,\phi_{i+1}`$ | $w_1$ | $w_1$ | $w_1/2$ | $w_1/6$ |
| $`w_2\,\phi_{i+2}`$ | $w_2$ | $2w_2$ | $2w_2$ | $4w_2/3$ |
| required sum | 0 | 1 | 0 | (error) |

The first three columns give $w_0 + w_1 + w_2 = 0$, $w_1 + 2w_2 = 1$ and $w_1/2 + 2w_2 = 0$, so $w = (-3/2, 2, -1/2)$. The fourth column gives $\mu_3 = 2/6 - 4/6 = -1/3$:

```math
\phi'_i = \frac{-3\phi_i + 4\phi_{i+1} - \phi_{i+2}}{2h} + \frac{h^2}{3}\phi'''_i + O(h^3)
```

### Common Stencils

The [Finite-Difference Stencils](../../../scripts/algorithms/finite_difference_stencils/) script solves the Vandermonde system for any offsets and prints the weights below as fractions.

| Derivative | Offsets | Weights | Leading error |
| --- | --- | --- | --- |
| $\phi'$ | $-1, 0, 1$ | $-\tfrac12, 0, \tfrac12$ | $\tfrac16 h^2\phi'''$ |
| $\phi'$ | $-2, \dots, 2$ | $\tfrac{1}{12}, -\tfrac23, 0, \tfrac23, -\tfrac{1}{12}$ | $-\tfrac{1}{30}h^4\phi^{(5)}$ |
| $\phi'$ | $-3, \dots, 3$ | $-\tfrac{1}{60}, \tfrac{3}{20}, -\tfrac34, 0, \tfrac34, -\tfrac{3}{20}, \tfrac{1}{60}$ | $\tfrac{1}{140}h^6\phi^{(7)}$ |
| $\phi'$ | $-2, -1, 0$ | $\tfrac12, -2, \tfrac32$ | $-\tfrac13 h^2\phi'''$ |
| $\phi'$ | $-2, -1, 0, 1$ | $\tfrac16, -1, \tfrac12, \tfrac13$ | $\tfrac{1}{12}h^3\phi''''$ |
| $\phi''$ | $-1, 0, 1$ | $1, -2, 1$ | $\tfrac{1}{12}h^2\phi''''$ |
| $\phi''$ | $-2, \dots, 2$ | $-\tfrac{1}{12}, \tfrac43, -\tfrac52, \tfrac43, -\tfrac{1}{12}$ | $-\tfrac{1}{90}h^4\phi^{(6)}$ |
| $\phi''$ | $0, 1, 2, 3$ | $2, -5, 4, -1$ | $-\tfrac{11}{12}h^2\phi''''$ |

The stencil with offsets $-2, -1, 0, 1$ is the third-order upwind-biased formula for a convection term with positive velocity.

### Fornberg's Algorithm

The Vandermonde matrix becomes badly conditioned as the stencil widens, and solving it separately for every derivative and every boundary point is wasteful. Fornberg (1988) gave a recursion that builds the weights for all derivatives $0, \dots, m$ on the nested stencils $`\{x_0\}, \{x_0, x_1\}, \dots, \{x_0, \dots, x_{n-1}\}`$ in $O(n^2 m)$ operations, for arbitrarily spaced nodes. It differentiates the Lagrange interpolating polynomial through the nodes, adding one node at a time, and it is the standard way to generate stencils on non-uniform grids and for the boundary closures of high-order schemes. The script implements it (`fornberg_weights`) and checks it against the Vandermonde solution.

## Applying a Stencil to a Marching Problem

Consider the initial-value problem

$$
\frac{d\phi}{dx} + \phi = 0, \quad 0 \le x \le 1,
\qquad \phi(0) = 1
$$

with exact solution $\phi = e^{-x}$, on the grid $x_i = i\Delta x$. Using the backward difference at node $i$ gives

```math
\frac{\phi_i - \phi_{i-1}}{\Delta x} + \phi_i = 0
\quad\Longrightarrow\quad
\phi_i = \frac{\phi_{i-1}}{1 + \Delta x}
```

so each value follows from the previous one. With $\Delta x = 1/3$ the values at $x = 1/3, 2/3, 1$ are $3/4$, $9/16$ and $27/64 = 0.4219$, against $e^{-1} = 0.3679$, an error of 14.7%. The [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/) script plots this case.

Replacing the derivative by the second-order one-sided formula from the table, $(3\phi_i - 4\phi_{i-1} + \phi_{i-2})/(2\Delta x)$, gives

```math
\phi_i = \frac{4\phi_{i-1} - \phi_{i-2}}{3 + 2\Delta x}
```

which needs two previous values, so the first step $\phi_1$ comes from the exact solution or from one step of the first-order scheme. Starting from $\phi_1 = e^{-\Delta x}$:

| $\Delta x$ | error at $x = 1$, first order | error at $x = 1$, second order |
| --- | --- | --- |
| 1/3 | $5.40 \times 10^{-2}$ | $-8.09 \times 10^{-3}$ |
| 1/6 | $2.87 \times 10^{-2}$ | $-2.85 \times 10^{-3}$ |
| 1/12 | $1.48 \times 10^{-2}$ | $-7.92 \times 10^{-4}$ |
| 1/24 | $7.53 \times 10^{-3}$ | $-2.06 \times 10^{-4}$ |
| 1/48 | $3.80 \times 10^{-3}$ | $-5.24 \times 10^{-5}$ |

The first-order error halves with each refinement and the second-order error falls by a factor approaching 4. Starting the second-order scheme with one first-order step instead leaves the order unchanged, because a single step contributes a local error of $O(\Delta x^2)$. This is the BDF2 time integrator in disguise; for time-dependent problems see [Time Integration](../cfd/time_integration.md).

## Compact Schemes

Explicit stencils gain two orders of accuracy for every two extra points, which makes high-order schemes wide. Compact (Padé) schemes instead couple the unknown derivatives at neighbouring nodes. The tridiagonal family for the first derivative is

```math
\alpha\,\phi'_{i-1} + \phi'_i + \alpha\,\phi'_{i+1} = a\,\frac{\phi_{i+1} - \phi_{i-1}}{2h} + b\,\frac{\phi_{i+2} - \phi_{i-2}}{4h}
```

Matching Taylor series gives the conditions (Lele 1992)

```math
a + b = 1 + 2\alpha \;\; (\text{order } 2), \qquad
a + 4b = 6\alpha \;\; (\text{order } 4), \qquad
a + 16b = 10\alpha \;\; (\text{order } 6)
```

With $b = 0$ the first two give the classical fourth-order Padé scheme $\alpha = 1/4$, $a = 3/2$, which uses only the three points $i - 1, i, i + 1$. All three conditions together give the sixth-order scheme $\alpha = 1/3$, $a = 14/9$, $b = 1/9$ on a five-point stencil, whose truncation error constant is much smaller than that of the explicit sixth-order formula with seven points (for $e^{\sin x}$ on 64 or 128 points the compact error is about 15 times smaller). For the second derivative the fourth-order Padé scheme is

```math
\frac{1}{10}\phi''_{i-1} + \phi''_i + \frac{1}{10}\phi''_{i+1} = \frac{6}{5}\,\frac{\phi_{i+1} - 2\phi_i + \phi_{i-1}}{h^2}
```

Evaluating a compact derivative along a grid line means solving a tridiagonal system, which the Thomas algorithm does in $O(N)$ operations; on a periodic line the system is cyclic. Near a non-periodic boundary the scheme needs a one-sided closure, for example the third-order relation $\phi'_1 + 2\phi'_2 = (-5\phi_1 + 4\phi_2 + \phi_3)/(2h)$ used by Lele. Compact schemes are the standard spatial discretization of many DNS, LES and computational aeroacoustics codes on structured grids.

## Modified Wavenumber Analysis

Truncation error describes the limit $h \to 0$. Modified wavenumber analysis describes a fixed grid, by asking how each Fourier mode is differentiated. Apply a first-derivative stencil to $\phi = e^{\mathrm{i}kx}$:

```math
\frac{1}{h}\sum_j w_j\,e^{\mathrm{i}k(x_i + s_j h)} = \mathrm{i}\,k_{\mathrm{eff}}\,e^{\mathrm{i}kx_i},
\qquad
k_{\mathrm{eff}}\Delta x = -\mathrm{i}\sum_j w_j\,e^{\mathrm{i}s_j\theta}, \quad \theta = k\Delta x
```

The exact derivative has $k_{\mathrm{eff}} = k$. Only $0 \le \theta \le \pi$ matters, because $\theta = \pi$ (two points per wavelength) is the shortest wave the grid can carry. For the schemes above,

```math
k_{\mathrm{eff}}\Delta x =
\begin{cases}
\sin\theta & \text{central, 2nd order} \\
\left(8\sin\theta - \sin 2\theta\right)/6 & \text{central, 4th order} \\
\dfrac{a\sin\theta + (b/2)\sin 2\theta}{1 + 2\alpha\cos\theta} & \text{compact} \\
\sin\theta - \mathrm{i}\,(1 - \cos\theta) & \text{backward, 1st order}
\end{cases}
```

For the second derivative the three-point formula gives $`k^2_{\mathrm{eff}}\Delta x^2 = 2 - 2\cos\theta = 4\sin^2(\theta/2)`$ instead of $\theta^2$.

The meaning follows from the semi-discrete advection equation $`\phi_t + c\,\phi_x = 0`$. With the spatial derivative replaced by a stencil, the mode $e^{\mathrm{i}kx}$ evolves as $`\exp\left(\mathrm{i}k(x - c\,t\,\mathrm{Re}\,k_{\mathrm{eff}}/k)\right)\exp\left(c\,t\,\mathrm{Im}\,k_{\mathrm{eff}}\right)`$:

- The real part sets the numerical phase speed $`c^* = c\,\mathrm{Re}\,k_{\mathrm{eff}}/k`$. Central schemes have a purely real $k_{\mathrm{eff}}$ that falls below $k$ as $\theta$ grows, so short waves travel too slowly (dispersion error). At $\theta = \pi$, $k_{\mathrm{eff}} = 0$ and the sawtooth mode does not move at all.
- The group velocity $`c_g^* = c\,d(\mathrm{Re}\,k_{\mathrm{eff}}\Delta x)/d\theta`$ becomes negative where the curve turns down, for $\theta > \pi/2$ with the second-order scheme, so poorly resolved wave packets travel upstream.
- The imaginary part changes the amplitude. Upwind (one-sided against the flow) stencils have $`\mathrm{Im}\,k_{\mathrm{eff}} < 0`$ for $c > 0$ and damp the mode (numerical dissipation), most strongly at $\theta = \pi$. Downwind stencils have the opposite sign and amplify it, which is why they are unstable for advection.

![Modified wavenumbers of explicit, compact and one-sided stencils](../../../scripts/algorithms/finite_difference_stencils/finite_difference_stencils.png)

Panel (b) shows that every central scheme follows the exact line $k_{\mathrm{eff}} = k$ for long waves and falls to zero at $k\Delta x = \pi$. Higher order pushes the departure to shorter waves, and the sixth-order compact scheme stays accurate furthest. Panel (c) shows the real and imaginary parts of the first- and second-order backward and third-order upwind-biased stencils. The first-order scheme is very dissipative even at moderate $k\Delta x$, the third-order scheme much less so, and the second-order backward scheme overshoots in phase before damping strongly. Panel (a) is discussed in [Finite Difference Method](./intro.md#truncation-error-against-round-off).

## Resolution Per Wavelength

The modified wavenumber turns an accuracy requirement into a grid requirement. A wave of length $\lambda$ is sampled by $\mathrm{PPW} = \lambda/\Delta x = 2\pi/\theta$ points. Requiring the relative phase-speed error $`|\mathrm{Re}\,k_{\mathrm{eff}}/k - 1|`$ to stay below a tolerance gives the minimum PPW:

| Scheme | Stencil width | PPW for 1% phase error | PPW for 0.1% phase error |
| --- | --- | --- | --- |
| Central, 2nd order | 3 | 25.6 | 81.1 |
| Central, 4th order | 5 | 8.3 | 15.0 |
| Central, 6th order | 7 | 5.7 | 8.6 |
| Compact, 6th order | 5 (tridiagonal) | 4.0 | 5.7 |

The phase error accumulates: a wave that travels $L/\lambda$ wavelengths with a relative phase-speed error $\varepsilon$ ends up $2\pi\varepsilon L/\lambda$ radians out of phase. Propagating a wave 100 wavelengths with less than about 0.6 rad of error needs $\varepsilon \le 10^{-3}$, which is 81 points per wavelength with the second-order scheme and 15 with the fourth-order one. In 3D that is a factor $(81/15)^3 \approx 160$ in the number of grid points, far more than the extra cost per point of the wider stencil. This is the basic argument for high-order methods on smooth problems, continued in [High-Order Methods](../high_order/intro.md).

## Pitfalls

- High formal order pays off only on well-resolved, smooth solutions. Across shocks and other discontinuities, high-order central and compact stencils produce Gibbs-type oscillations, and the order of every scheme drops to 1 or below.
- Boundary closures of high-order schemes must be stable as well as accurate; a closure that is fine for a steady problem can make a time-dependent one blow up. Stability is usually checked by computing the eigenvalues of the semi-discrete operator.
- Central and compact schemes have no dissipation, so nonlinear terms on under-resolved grids feed energy into the grid-scale modes. Compact-scheme codes apply a low-pass filter every step or use a skew-symmetric (split) form of the convection term.
- Weights for the $m$-th derivative scale as $h^{-m}$, so round-off grows like $\epsilon_{\mathrm{mach}}/h^m$; very fine grids and high derivatives combine badly.
- Wide stencils need more ghost layers at processor boundaries in a parallel code, and compact schemes need parallel tridiagonal solvers.

## Key Takeaways

- The weights of any finite-difference formula solve a small Vandermonde system; the first moment that is not matched gives the truncation error.
- Fornberg's recursion computes the same weights stably for any node positions and all derivatives at once.
- Compact schemes reach fourth or sixth order on three or five points at the cost of a tridiagonal solve per grid line.
- The modified wavenumber separates dispersion (real part, phase speed) from dissipation (imaginary part, amplitude).
- Points per wavelength, not formal order, decides the cost: for 0.1% phase error a fourth-order scheme needs about 15 points per wavelength and a second-order scheme about 81.

## Related Scripts

- [Finite-Difference Stencils](../../../scripts/algorithms/finite_difference_stencils/): computes finite-difference weights for any set of stencil offsets by solving the Taylor-series (Vandermonde) system, then measures how the error of each stencil depends on the grid spacing and how well it represents each Fourier wavenumber.
- [Spectral vs Finite-Difference Differentiation](../../../scripts/algorithms/spectral_vs_finite_difference/): differentiates a smooth periodic function with the Fourier spectral method and with second- and fourth-order central finite differences, and shows that the spectral error falls exponentially with the number of points while the finite-difference errors fall algebraically.
- [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/): solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error.
- [Grid Convergence Comparison](../../../scripts/plots/comparing_grid_convergence/): illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [2D Schrödinger Equation Simulation](../../../scripts/simulations/schroedinger_equation/): solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface.
- [Gray-Scott Reaction-Diffusion Simulation](../../../scripts/simulations/gray_scott_reaction_diffusion/): simulates the Gray-Scott reaction-diffusion system, in which two chemicals that react and diffuse on a periodic square turn a small seeded square into self-replicating spots or branching coral, and animates the concentration of one of them with Matplotlib.
- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Mach Cone of a Moving Sound Source](../../../scripts/simulations/mach_cone_moving_source/): simulates the sound of a small source that accelerates from rest to twice the speed of sound and animates its pressure field, from the Doppler-compressed wavefronts of a subsonic source through the pile-up at Mach 1 to the Mach cone of a supersonic one.

## Exercises

**Exercise 1.** Use a Taylor table to derive the second-order backward formula for $\phi'_i$ from the offsets $-2, -1, 0$, and find its leading error term.

<details>
<summary>Answer</summary>

The rows give $w_{-2} + w_{-1} + w_0 = 0$ (column $\phi_i$), $-2w_{-2} - w_{-1} = 1$ (column $`h\phi'_i`$) and $`2w_{-2} + w_{-1}/2 = 0`$ (column $h^2\phi''_i$). The solution is $w = (1/2, -2, 3/2)$:

```math
\phi'_i \approx \frac{\phi_{i-2} - 4\phi_{i-1} + 3\phi_i}{2h}
```

The $h^3\phi'''_i$ column gives $\mu_3 = (-8 \cdot \tfrac12 + 2)/6 = -1/3$, so the error is $-\tfrac13 h^2\phi'''_i$. It is the mirror image of the forward formula derived in the note: reflecting the offsets negates the weights of a first derivative, and the moment $\mu_3$, and with it the leading error, is unchanged.

</details>

**Exercise 2.** Solve $d\phi/dx + \phi = 0$, $\phi(0) = 1$, with the first-order backward scheme for $\Delta x = 1/3$ and $\Delta x = 1/6$, and use the two errors at $x = 1$ to estimate the order. Then use the forward difference $(\phi_{i+1} - \phi_i)/\Delta x + \phi_i = 0$ instead with $\Delta x = 1/3$, and explain what goes wrong if $\Delta x > 2$.

<details>
<summary>Answer</summary>

The backward scheme gives $\phi_i = \phi_{i-1}/(1 + \Delta x)$, so $\phi(1) \approx (1 + \Delta x)^{-N}$. With $\Delta x = 1/3$: $(3/4)^3 = 0.4219$, error $0.0540$. With $\Delta x = 1/6$: $(6/7)^6 = 0.3966$, error $0.0287$. The ratio is $1.88$, close to 2, so the scheme is first order.

The forward (explicit) update is $\phi_{i+1} = (1 - \Delta x)\phi_i$, which gives $\phi(1) = (2/3)^3 = 0.2963$, an error of $-0.072$. The backward scheme overestimates $e^{-1}$ and the forward scheme underestimates it.

If $\Delta x > 2$ then $|1 - \Delta x| > 1$, and the forward solution changes sign every step and grows, although the exact solution decays. The backward factor $1/(1 + \Delta x)$ is below 1 for every $\Delta x > 0$.

</details>

**Exercise 3.** Solve the nonlinear problem $d\phi/dx + \phi^2 = 0$, $\phi(0) = 1$, on the grid $\Delta x = 1/3$ with the backward difference, and compare with the exact solution $\phi = 1/(1 + x)$.

<details>
<summary>Answer</summary>

Each step is the quadratic $`\Delta x\,\phi_i^2 + \phi_i - \phi_{i-1} = 0`$, whose positive root is

```math
\phi_i = \frac{-1 + \sqrt{1 + 4\Delta x\,\phi_{i-1}}}{2\Delta x}
```

| $x$ | numerical | exact $1/(1+x)$ |
| --- | --- | --- |
| 1/3 | 0.7913 | 0.7500 |
| 2/3 | 0.6503 | 0.6000 |
| 1 | 0.5496 | 0.5000 |

The error at $x = 1$ is $0.050$. The nonlinearity means a small algebraic equation must be solved at each point; on larger problems this is done with Newton or Picard iteration, see [Dealing with Nonlinearity](../cfd/dealing_with_nonlinearity.md).

</details>

**Exercise 4.** Show that the fourth-order central first derivative has $`k_{\mathrm{eff}}\Delta x = (8\sin\theta - \sin 2\theta)/6`$. Compute the relative phase-speed error of the second- and fourth-order central schemes for a wave resolved by 10 points per wavelength.

<details>
<summary>Answer</summary>

With weights $(1/12, -2/3, 0, 2/3, -1/12)$ on offsets $-2, \dots, 2$:

```math
k_{\mathrm{eff}}\Delta x = -\mathrm{i}\left[\tfrac{2}{3}\left(e^{\mathrm{i}\theta} - e^{-\mathrm{i}\theta}\right) - \tfrac{1}{12}\left(e^{2\mathrm{i}\theta} - e^{-2\mathrm{i}\theta}\right)\right] = \tfrac{4}{3}\sin\theta - \tfrac{1}{6}\sin 2\theta
```

which equals $(8\sin\theta - \sin 2\theta)/6$.

At 10 points per wavelength $\theta = 2\pi/10 = 0.6283$. The second-order scheme gives $\sin\theta/\theta = 0.9355$, a phase-speed error of $`-6.45\%`$. The fourth-order scheme gives $(8 \times 0.5878 - 0.9511)/6 = 0.6252$ and $0.6252/0.6283 = 0.9950$, an error of $`-0.50\%`$, thirteen times smaller.

</details>

**Exercise 5.** Show that the compact scheme with $b = 0$ is fourth order only for $\alpha = 1/4$, $a = 3/2$. Then compare the phase-speed errors at four points per wavelength ($\theta = \pi/2$) of this scheme, the explicit fourth-order scheme and the sixth-order compact scheme.

<details>
<summary>Answer</summary>

With $b = 0$ the conditions $a = 1 + 2\alpha$ and $a = 6\alpha$ give $4\alpha = 1$, so $\alpha = 1/4$ and $a = 3/2$.

At $\theta = \pi/2$, $\sin\theta = 1$, $\sin 2\theta = 0$ and $\cos\theta = 0$:

- fourth-order Padé: $k_{\mathrm{eff}}\Delta x = 3/2 = 1.500$ against $\pi/2 = 1.571$, an error of $`-4.5\%`$;
- explicit fourth order: $8/6 = 1.333$, an error of $`-15.1\%`$;
- sixth-order compact: $a = 14/9 = 1.556$, an error of $`-0.97\%`$.

The three-point Padé scheme is three times more accurate than the five-point explicit scheme of the same formal order.

</details>

## References

- B. Fornberg, "Generation of finite difference formulas on arbitrarily spaced grids", *Mathematics of Computation*, 51(184), 699–706, 1988.
- S. K. Lele, "Compact finite difference schemes with spectral-like resolution", *Journal of Computational Physics*, 103(1), 16–42, 1992.
- R. J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems*, SIAM, 2007.
- C. K. W. Tam and J. C. Webb, "Dispersion-relation-preserving finite difference schemes for computational acoustics", *Journal of Computational Physics*, 107(2), 262–281, 1993.
- L. N. Trefethen, "Group velocity in finite difference schemes", *SIAM Review*, 24(2), 113–136, 1982.
- J. H. Ferziger, M. Perić and R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- J. D. Anderson, *Computational Fluid Dynamics: The Basics with Applications*, McGraw-Hill, 1995.
