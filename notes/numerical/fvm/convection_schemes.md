# Convection Schemes for Finite Volume Methods

The convective flux through a face is $F_f\phi_f$, the mass flux times the value of $\phi$ on the face. The mass flux is known from the flow solution, but $\phi_f$ has to be built from the cell values on either side, and this choice decides the accuracy, the boundedness and the robustness of a finite volume solution more than any other. This note covers the classical linear schemes (upwind, central, hybrid, power law, linear upwind, QUICK), the numerical diffusion of upwinding, Godunov's order barrier, and the nonlinear TVD and NVD schemes that get around it, together with deferred correction, the standard way to implement any of them in an implicit code. The 1D setting and the notation are those of [The Finite Volume Method](intro.md); the unstructured-mesh ingredients (gradients, skewness) are in [Finite Volume Discretization on General Meshes](discretization.md).

## Problem Statement

Given the cell values $\phi_i$ and the mass flux $F_f$ on every face, define a face value $\phi_f$ such that the discrete convection term $\sum_f F_f\phi_f$ is

- consistent and as accurate as possible (second order or better on smooth solutions);
- bounded: it creates no new maxima or minima, so that a concentration stays between 0 and 1, a turbulence energy stays positive, and a steep front does not generate oscillations;
- conservative: one value per face, used by both cells;
- solvable: the resulting implicit system can be solved efficiently by iterative methods.

Two model problems are used. The steady 1D convection–diffusion equation $`d(\rho u\phi)/dx = d(\Gamma\,d\phi/dx)/dx`$ with $\phi(0) = 1$, $\phi(L) = 0$ tests accuracy and boundedness as a function of the cell Péclet number $Pe_\Delta = \rho u\Delta x/\Gamma$. The unsteady linear advection equation $`\partial\phi/\partial t + u\,\partial\phi/\partial x = 0`$ on a periodic domain, with $u > 0$ and Courant number $C = u\Delta t/\Delta x$, tests how a scheme transports smooth and discontinuous profiles. The exact solutions are known in both cases.

The difficulty is that the requirements conflict: as shown below, no linear scheme is both bounded and more than first-order accurate.

## Notation

Relative to the flow direction at face $f$, $U$ is the upstream cell, $D$ the downstream cell and $UU$ the cell upstream of $U$. For face $e$ of cell $P$ with $F_e > 0$, $U = P$, $D = E$ and $UU = W$; for $F_e < 0$, $U = E$, $D = P$ and $UU = EE$. Writing every scheme in terms of $U$, $D$ and $UU$ makes it valid for both flow directions.

## Linear Schemes

A scheme is linear if its face value is a fixed linear combination of cell values, with coefficients that do not depend on the solution. On a uniform grid the common ones are:

| Scheme | Face value $\phi_f$ | Order of $\phi_f$ | Bounded |
| --- | --- | --- | --- |
| first-order upwind (UD) | $\phi_U$ | 1 | yes |
| central (CD) | $\tfrac{1}{2}(\phi_U + \phi_D)$ | 2 | only for $\lvert Pe_\Delta \rvert \le 2$ |
| linear upwind, second-order upwind (LUD, SOU) | $\tfrac{3}{2}\phi_U - \tfrac{1}{2}\phi_{UU}$ | 2 | no |
| QUICK (Leonard 1979) | $\tfrac{6}{8}\phi_U + \tfrac{3}{8}\phi_D - \tfrac{1}{8}\phi_{UU}$ | 3 | no |
| hybrid (Spalding) | CD for $\lvert Pe_\Delta \rvert < 2$, UD with diffusion switched off for $\lvert Pe_\Delta \rvert \ge 2$ | 2 or 1 | yes |
| power law (Patankar 1980) | a polynomial fit of the exponential scheme, below | 2 or 1 | yes |

QUICK is the parabola through $UU$, $U$ and $D$ evaluated at the face. The upwind, central, linear upwind and QUICK schemes are members of van Leer's $\kappa$ family,

```math
\phi_f = \phi_U + \frac{1 + \kappa}{4}(\phi_D - \phi_U) + \frac{1 - \kappa}{4}(\phi_U - \phi_{UU})
```

with $\kappa = -1$ for linear upwind, $\kappa = 0$ for Fromm's scheme, $\kappa = 1/2$ for QUICK and $\kappa = 1$ for central differencing; first-order upwind drops both correction terms. On unstructured meshes the linear-upwind face value is $\phi_f = \phi_U + (\nabla\phi)_U\cdot(\mathbf{x}_f - \mathbf{x}_U)$, which needs no $UU$ cell.

The order in the table is that of the face value as a point value. With midpoint integration over the face and cell values interpreted as averages, the finite volume scheme as a whole is second order in 2D and 3D even with QUICK; in the 1D test below QUICK also converges at second order.

### Coefficients of the 1D Equations

For upwind, central, hybrid and power law, Patankar (1980) writes the neighbour coefficients of $a_P\phi_P = a_W\phi_W + a_E\phi_E + b$ in one form,

```math
a_E = D_e\,A(|Pe_e|) + \max(-F_e, 0),
\qquad
a_W = D_w\,A(|Pe_w|) + \max(F_w, 0),
\qquad
a_P = a_W + a_E + (F_e - F_w)
```

with $D = \Gamma/\delta x$, $Pe = F/D$ and

| Scheme | $A(\lvert Pe \rvert)$ |
| --- | --- |
| central | $1 - 0.5\lvert Pe \rvert$ |
| upwind | $1$ |
| hybrid | $\max(0,\ 1 - 0.5\lvert Pe \rvert)$ |
| power law | $\max(0,\ (1 - 0.1\lvert Pe \rvert)^5)$ |
| exponential | $\lvert Pe \rvert/(e^{\lvert Pe \rvert} - 1)$ |

The exponential scheme reproduces the exact solution of the 1D steady problem at the nodes for any $Pe_\Delta$, but it is expensive and loses that property in multidimensional flows with sources; the power law approximates it within a few per cent at far lower cost. The coefficients are non-negative whenever $A \ge 0$, which is why hybrid and power law are bounded and central is not.

QUICK on a uniform grid with $F_w, F_e > 0$ gives

```math
a_W = D_w + \tfrac{6}{8}F_w + \tfrac{1}{8}F_e,
\qquad
a_E = D_e - \tfrac{3}{8}F_e,
\qquad
a_{WW} = -\tfrac{1}{8}F_w,
\qquad
a_P = a_W + a_E + a_{WW} + (F_e - F_w)
```

The coefficient $a_{WW}$ is always negative and $a_E$ becomes negative for $Pe_e > 8/3$, so QUICK is not bounded and its matrix is not diagonally dominant. It is therefore implemented by deferred correction (below).

### Results on the 1D Problem

The [convection–diffusion script](../../../scripts/algorithms/fvm_convection_diffusion_1d/) solves the test case of Versteeg and Malalasekera ($L = 1$ m, $\rho = 1$ kg/m³, $\Gamma = 0.1$ kg/(m s)) with all five schemes.

![Central, upwind, hybrid and QUICK on the 1D convection-diffusion problem](../../../scripts/algorithms/fvm_convection_diffusion_1d/fvm_convection_diffusion_1d.png)

At $Pe_\Delta = 5$ (panel a) central differencing and QUICK both overshoot to about 2.5, while upwind and hybrid are bounded but smear the outlet layer. Panel (c) gives the RMS error at $u = 2.5$ m/s ($Pe_L = 25$):

| Scheme | observed order, finest grids | RMS error, 1280 cells |
| --- | --- | --- |
| central | 2.00 | $9.3\times10^{-6}$ |
| upwind | 0.99 | $9.7\times10^{-4}$ |
| hybrid | 2.00 | $5.0\times10^{-6}$ |
| power law | 1.99 | $7.1\times10^{-6}$ |
| QUICK | 2.02 | $5.8\times10^{-6}$ |

Hybrid and power law behave like upwind while $Pe_\Delta > 2$ and like central once the grid resolves the layer. On a practical mesh much of the domain has $Pe_\Delta \gg 2$, so both are effectively first-order schemes there.

## Numerical Diffusion of Upwinding

The modified equation shows what the upwind scheme actually solves. For $u > 0$ on a uniform grid, Taylor expansion about node $P$ gives

```math
\frac{\phi_P - \phi_W}{\Delta x} = \frac{d\phi}{dx} - \frac{\Delta x}{2}\frac{d^2\phi}{dx^2} + \frac{\Delta x^2}{6}\frac{d^3\phi}{dx^3} - \dots
```

so the upwind convection term equals the exact one minus $`(\rho u\Delta x/2)\,d^2\phi/dx^2`$. Moving that term to the right-hand side, the discrete equations are a second-order approximation of

$$
\frac{d(\rho u\phi)}{dx} = \frac{d}{dx}\left[(\Gamma + \Gamma_{\mathrm{num}})
\frac{d\phi}{dx}\right],
\qquad \Gamma_{\mathrm{num}} = \frac{\rho|u|\Delta x}{2}
$$

The ratio $\Gamma_{\mathrm{num}}/\Gamma = Pe_\Delta/2$ is exactly the quantity that makes central differencing unbounded: whenever upwinding is needed for boundedness, its numerical diffusion is larger than the physical diffusion. For explicit time stepping of linear advection the corresponding result is

$$
\frac{\partial\phi}{\partial t} + u
\frac{\partial\phi}{\partial x} = \frac{u\Delta x}{2}(1 - C)
\frac{\partial^2\phi}{\partial x^2} + O(\Delta x^2)
$$

so explicit upwind is exact at $C = 1$ and most diffusive at small Courant numbers. The central scheme has no even-derivative error term: its leading error, $`(\Delta x^2/6)\,d^3\phi/dx^3`$, is dispersive, which produces wave-like errors instead of smearing.

### False Diffusion in Multidimensional Flow

In 2D and 3D, upwinding is applied face by face along the grid lines. When the flow is aligned with the grid, it adds diffusion only in the streamwise direction, where it does little harm at high $Pe$. When the flow crosses the grid at an angle $\theta$, it also adds diffusion across the streamlines, called **false diffusion**. For a uniform flow of speed $U$ on a grid of spacing $\Delta x$, $\Delta y$, de Vahl Davis and Mallinson (1976) estimated

```math
\Gamma_{\mathrm{false}} = \frac{\rho U\,\Delta x\,\Delta y\,\sin 2\theta}{4\left(\Delta y\sin^3\theta + \Delta x\cos^3\theta\right)}
```

which vanishes for $\theta = 0^\circ$ and $90^\circ$ and is largest at $45^\circ$, where on a square grid it equals $\rho U\Delta x/(2\sqrt{2})$. The standard demonstration is a uniform flow at $45^\circ$ carrying a step in $\phi$ with $\Gamma = 0$: the exact solution keeps the step sharp along the diagonal, and upwinding spreads it into a band that widens downstream. Refining the grid, aligning it with the flow, or using a higher-order scheme reduces the error; using upwinding on a coarse grid in a recirculating flow can produce a smooth, converged and badly wrong solution.

## Godunov's Order Barrier

A scheme for linear advection is monotonicity preserving if monotone initial data stay monotone. Godunov (1959) proved:

> A linear scheme that is monotonicity preserving is at most first-order accurate.

The proof is short. A linear explicit scheme can be written $\phi_i^{n+1} = \sum_k c_k\phi_{i+k}^n$ with constant coefficients $c_k$, and it is monotonicity preserving for all data only if every $c_k \ge 0$. The exact solution shifts the profile by $C$ cells, so a scheme that is exact for polynomials up to degree two, the requirement for second order, must satisfy

```math
\sum_k c_k = 1, \qquad \sum_k k\,c_k = -C, \qquad \sum_k k^2 c_k = C^2
```

These give $\sum_k c_k(k + C)^2 = C^2 - 2C^2 + C^2 = 0$. With all $c_k \ge 0$, every non-zero $c_k$ must sit at $k = -C$, which is impossible unless $C$ is an integer. Lax–Wendroff, for example, has $c_{-1} = C(1 + C)/2$, $c_0 = 1 - C^2$ and $c_1 = -C(1 - C)/2 < 0$.

The way around the barrier is to give up linearity: let the scheme depend on the local solution, behaving like a second-order scheme where the solution is smooth and like upwind near extrema and steep gradients. TVD and NVD schemes do exactly this.

## TVD Schemes and Flux Limiters

### Total Variation

The total variation of a grid function is

$$
TV(\phi) = \sum_i |\phi_{i+1} - \phi_i|
$$

and a scheme is total variation diminishing (TVD) if $TV(\phi^{n+1}) \le TV(\phi^{n})$ for all data (Harten 1983). The exact solution of the advection equation preserves the total variation, a new local extremum would increase it, and a TVD scheme is therefore monotonicity preserving. Harten's lemma gives a practical test: a scheme that can be written as

```math
\phi_i^{n+1} = \phi_i^n - A_{i-1/2}\,(\phi_i^n - \phi_{i-1}^n) + B_{i+1/2}\,(\phi_{i+1}^n - \phi_i^n)
```

is TVD if $A_{i-1/2} \ge 0$, $B_{i+1/2} \ge 0$ and $A_{i+1/2} + B_{i+1/2} \le 1$ for every $i$. The coefficients may depend on the solution, which is what allows second order.

### Flux-Limited Schemes

Sweby (1984) wrote a family of schemes as the upwind flux plus a limited anti-diffusive correction towards Lax–Wendroff. For $u > 0$,

```math
F_{i+1/2} = u\,\phi_i + \frac{u}{2}(1 - C)\,\psi(r_i)\,(\phi_{i+1} - \phi_i),
\qquad
r_i = \frac{\phi_i - \phi_{i-1}}{\phi_{i+1} - \phi_i}
```

where $r_i$ is the ratio of consecutive gradients, close to 1 for smooth data and negative at an extremum. The limiter $\psi = 0$ gives upwind, $\psi = 1$ gives Lax–Wendroff and $\psi = r$ gives Beam–Warming. With $\psi(r_i)(\phi_{i+1} - \phi_i) = (\psi(r_i)/r_i)(\phi_i - \phi_{i-1})$, the update takes Harten's form with $B = 0$ and

```math
A_{i-1/2} = C\left[1 + \frac{1 - C}{2}\left(\frac{\psi(r_i)}{r_i} - \psi(r_{i-1})\right)\right]
```

If $0 \le \psi(r)/r \le 2$ and $0 \le \psi(r) \le 2$, the bracket lies between $1 - (1 - C)$ and $1 + (1 - C)$, so $C^2 \le A \le C(2 - C) \le 1$ for $0 \le C \le 1$. The scheme is therefore TVD if

```math
\psi(r) = 0 \ \text{ for } r \le 0,
\qquad
0 \le \psi(r) \le \min(2r,\ 2) \ \text{ for } r > 0
```

The first condition means that every TVD scheme switches to first-order upwind at a local extremum. Second-order accuracy on smooth data requires $\psi(1) = 1$, and Sweby showed that the second-order TVD limiters are those lying between minmod and superbee: between $r$ and $\min(2r, 1)$ for $0 < r \le 1$ and between $1$ and $\min(r, 2)$ for $r \ge 1$.

### Limiter Functions

| Limiter | $\psi(r)$ | Character |
| --- | --- | --- |
| minmod | $\max\left[0,\ \min(1, r)\right]$ | lower boundary of the second-order region; most diffusive |
| superbee | $\max\left[0,\ \min(2r, 1),\ \min(r, 2)\right]$ | upper boundary; sharpest, steepens smooth profiles |
| van Leer | $(r + \lvert r \rvert)/(1 + \lvert r \rvert)$ | smooth (differentiable for $r > 0$), intermediate |
| monotonized central (MC) | $\max\left[0,\ \min(2r,\ (1 + r)/2,\ 2)\right]$ | follows the central slope $(1 + r)/2$ where the TVD bounds allow |
| van Albada | $(r^2 + r)/(r^2 + 1)$ for $r > 0$, else 0 | smooth, close to central near $r = 1$ |

All five are symmetric, $\psi(r)/r = \psi(1/r)$, so a profile and its mirror image are treated the same way.

![Sweby diagram and convergence of limiters on a smooth wave](../../../scripts/algorithms/tvd_limiters_advection/sweby_diagram.png)

Panel (a) is the Sweby diagram: the light region is where the TVD conditions hold, the dark region is its second-order part, and every limiter passes through $(1, 1)$. Lax–Wendroff ($\psi = 1$) leaves the TVD region for $r < 1/2$, and Beam–Warming ($\psi = r$) for $r > 2$. Panel (b) shows that all limiters converge at close to second order in the L1 norm on a smooth sine wave, against first order for upwind.

The [TVD advection script](../../../scripts/algorithms/tvd_limiters_advection/) transports a Gaussian, a square wave and a triangle once around a periodic domain of 200 cells at $C = 0.5$:

![Upwind, Lax-Wendroff and TVD limiters after one period](../../../scripts/algorithms/tvd_limiters_advection/tvd_advection_profiles.png)

| Scheme | L1 error | max $\phi$ | min $\phi$ | $TV/TV_0$ after one period |
| --- | --- | --- | --- | --- |
| upwind | 0.165 | 0.954 | 0.024 | 0.644 |
| Lax–Wendroff | 0.069 | 1.232 | −0.231 | 1.259 |
| minmod | 0.049 | 1.000 | 0.000 | 0.904 |
| van Leer | 0.028 | 1.000 | 0.000 | 0.945 |
| superbee | 0.016 | 1.000 | 0.000 | 0.972 |
| MC | 0.022 | 1.000 | 0.000 | 0.959 |
| van Albada | 0.035 | 1.000 | 0.000 | 0.929 |

Upwind keeps the solution within $[0, 1]$ but removes 42% of the Gaussian peak. Lax–Wendroff is far more accurate on the smooth parts but overshoots by 23% at the square wave and raises the total variation. All TVD schemes keep the solution within the initial range, and the script confirms that their total variation never increases in any of the 400 steps. They clip smooth peaks, minmod most and superbee least, while superbee turns the Gaussian into a flattened plateau. Van Leer and MC are common compromises.

### Steady Implicit Form and Unstructured Meshes

In steady and implicit finite volume codes the limiter acts on the face value directly,

```math
\phi_f = \phi_U + \frac{1}{2}\psi(r_f)\,(\phi_D - \phi_U),
\qquad
r_f = \frac{\phi_U - \phi_{UU}}{\phi_D - \phi_U}
```

without the Courant-number factor. On unstructured meshes there is no $UU$ cell, and $r_f$ is built from the upwind cell gradient as if $`\phi_{UU} = \phi_D - 2\,\mathbf{d}\cdot(\nabla\phi)_U`$, with $\mathbf{d}$ the vector from $U$ to $D$:

```math
r_f = \frac{2\,\mathbf{d}\cdot(\nabla\phi)_U}{\phi_D - \phi_U} - 1
```

The TVD property is proved for scalar 1D schemes. On multidimensional unstructured meshes the same limiters keep the solution bounded in practice, but without a general proof.

## Normalized Variables and the Convection Boundedness Criterion

Leonard also introduced the normalized variable

$$
\tilde\phi = \frac{\phi - \phi_{UU}}{\phi_D - \phi_{UU}}
$$

which maps $\phi_{UU}$ to 0 and $\phi_D$ to 1, so every scheme that uses $UU$, $U$ and $D$ becomes a single curve $\tilde\phi_f(\tilde\phi_U)$ in the normalized variable diagram (NVD). In this variable upwind is $\tilde\phi_f = \tilde\phi_U$, central is $(1 + \tilde\phi_U)/2$, linear upwind is $3\tilde\phi_U/2$ and QUICK is $3/8 + 3\tilde\phi_U/4$. Second-order schemes pass through the point $(1/2, 3/4)$.

Gaskell and Lau (1988) stated the convection boundedness criterion (CBC): an implicit steady scheme is bounded if its normalized face value satisfies

```math
\tilde\phi_U \le \tilde\phi_f \le 1 \ \text{ for } 0 < \tilde\phi_U < 1,
\qquad
\tilde\phi_f = \tilde\phi_U \ \text{ otherwise}
```

with a continuous curve through $(0, 0)$ and $(1, 1)$. A limiter is the same object in the other variable: $\tilde\phi_f = \tilde\phi_U + \tfrac{1}{2}\psi(r)(1 - \tilde\phi_U)$ with $r = \tilde\phi_U/(1 - \tilde\phi_U)$. Substituting the TVD bounds gives $\tilde\phi_U \le \tilde\phi_f \le \min(2\tilde\phi_U, 1)$, a subregion of the CBC region. Schemes designed in the NVD, such as SMART (Gaskell and Lau 1988), a bounded QUICK with

```math
\tilde\phi_f = \begin{cases}
3\tilde\phi_U, & 0 < \tilde\phi_U < 1/6 \\
3/8 + 3\tilde\phi_U/4, & 1/6 \le \tilde\phi_U \le 5/6 \\
1, & 5/6 < \tilde\phi_U < 1 \\
\tilde\phi_U, & \text{otherwise}
\end{cases}
```

use the extra room of the CBC and are bounded for steady implicit problems, though not TVD in the explicit sense.

## Deferred Correction

High-order and limited schemes give matrices with negative or solution-dependent coefficients. Deferred correction (Khosla and Rubin 1974) keeps the upwind scheme in the matrix and adds the difference to the high-order flux as an explicit source evaluated at the previous iteration $k$:

```math
F_f\phi_f^{k+1} \approx F_f\phi_{f,\mathrm{UD}}^{k+1} + \beta\,F_f\left(\phi_{f,\mathrm{HO}}^{k} - \phi_{f,\mathrm{UD}}^{k}\right)
```

with a blending factor $0 \le \beta \le 1$, usually 1. The matrix is the upwind M-matrix at every iteration, so it is diagonally dominant and easy to solve, and at convergence $\phi^{k+1} = \phi^{k}$ and the solution satisfies the high-order equations exactly. The cost is extra outer iterations: in the 1D script QUICK converges to a change below $10^{-12}$ in 10 to 27 iterations. The correction flux is computed once per face and added to one cell and subtracted from the other, so conservation is not affected. In a flow solver the deferred correction is updated together with the nonlinear coefficients in the outer iterations, so it costs little extra.

## Schemes in Practical Codes

Codes name their schemes differently, but most offer the same families:

| Family | Typical names |
| --- | --- |
| first-order upwind | upwind, first-order upwind |
| linear upwind | linearUpwind, second-order upwind |
| central | linear, central differencing |
| bounded central | limitedLinear, bounded central differencing |
| QUICK | QUICK |
| TVD limiters | Minmod, vanLeer, SuperBee, MUSCL, vanAlbada |
| NVD schemes | Gamma, SFCD |

A common practice for steady RANS is to start with first-order upwind and switch to a second-order or limited scheme once the flow has settled, to use a bounded scheme for turbulence and volume-fraction equations, and to use central or lightly limited schemes for the momentum equations in LES, where numerical diffusion competes with the subgrid model. For compressible flow with shocks the limiters are applied to the reconstructed states that enter a Riemann solver; see [Riemann Solvers and Godunov Methods](riemann_solvers.md).

## Pitfalls

- Using first-order upwind for final results. Its numerical diffusion, $\rho|u|\Delta x/2$, typically exceeds the physical or turbulent diffusion and produces converged, smooth, wrong answers, especially in flows at an angle to the grid.
- Using an unbounded scheme (central, linear upwind, QUICK) for a quantity that must stay within physical bounds, such as $k$, $\varepsilon$, $\omega$ or a volume fraction.
- Expecting a steady solution with a non-smooth limiter (minmod, superbee) to converge to machine precision. The switches in $\psi(r)$ can make the residual stall at a plateau; the smooth van Leer and van Albada limiters converge better.
- Overly compressive limiters on smooth flows: superbee steepens gradients and turns smooth peaks into plateaus.
- Taking the order of a face interpolant as the order of the scheme. With midpoint face integration, QUICK and the third-order MUSCL variants are second order overall in 2D and 3D.
- Applying 1D coefficient formulas on non-uniform or unstructured meshes without the geometric weights and the gradient-based construction of $\phi_{UU}$.

## Key Takeaways

- The convective face value is the central choice of a finite volume scheme; central differencing is bounded only for $|Pe_\Delta| \le 2$, upwinding is bounded but adds $\Gamma_{\mathrm{num}} = \rho|u|\Delta x/2$.
- Godunov's theorem: linear schemes that never create new extrema are at most first order, so accurate bounded schemes must be nonlinear.
- TVD schemes add a limited correction to upwind; the limiter $\psi(r)$ must satisfy $0 \le \psi \le \min(2r, 2)$, vanish for $r \le 0$, and pass through $(1, 1)$ for second order.
- Minmod and superbee bound the second-order TVD region; van Leer, MC and van Albada lie between them.
- The NVD and the CBC describe bounded schemes for steady implicit problems; the TVD region is a subset of the CBC region.
- Deferred correction puts any high-order scheme on top of the upwind matrix and converges to the high-order solution.

## Related Scripts

- [1D Finite-Volume Convection–Diffusion](../../../scripts/algorithms/fvm_convection_diffusion_1d/): solves steady 1D convection–diffusion with the finite volume method using central, upwind, hybrid, power-law and QUICK face values, and compares each with the exponential exact solution.
- [TVD Limiters for Linear Advection](../../../scripts/algorithms/tvd_limiters_advection/): advects a Gaussian, a square wave and a triangle once around a periodic domain with first-order upwind, Lax–Wendroff and flux-limited TVD schemes, and shows the trade-off that Godunov's theorem forces on linear schemes.
- [Supersonic Forward-Facing Step](../../../scripts/simulations/supersonic_forward_facing_step/): solves the 2D compressible Euler equations for a Mach 3 stream that meets a forward-facing step in a wind tunnel, the benchmark of Woodward and Colella (1984), and animates the shock pattern that forms.
- [Riemann Solver Comparison](../../../scripts/algorithms/riemann_solver_comparison/): compares five Riemann solvers inside the same first-order Godunov finite-volume scheme for the 1D Euler equations: the exact solver, Rusanov (local Lax–Friedrichs), HLL, HLLC and Roe with Harten's entropy fix.
- [Sod Shock Tube](../../../scripts/simulations/sod_shock_tube/): animates Sod's shock tube, the standard test of compressible-flow solvers, computed with a first-order Godunov scheme and a second-order MUSCL–Hancock scheme and compared with the exact Riemann solution at every frame.

## Exercises

**Exercise 1.** At face $e$ with $F_e > 0$ the cell values are $\phi_W = 0.2$, $\phi_P = 0.6$ and $\phi_E = 0.8$. Compute $\phi_e$ with upwind, central, linear upwind and QUICK, and with the steady limited form $\phi_e = \phi_P + \tfrac{1}{2}\psi(r)(\phi_E - \phi_P)$ for minmod, van Leer and superbee.

<details>
<summary>Answer</summary>

Upwind: $0.6$. Central: $(0.6 + 0.8)/2 = 0.7$. Linear upwind: $1.5 \times 0.6 - 0.5 \times 0.2 = 0.8$. QUICK: $0.75 \times 0.6 + 0.375 \times 0.8 - 0.125 \times 0.2 = 0.725$.

The gradient ratio is $r = (0.6 - 0.2)/(0.8 - 0.6) = 2$. Minmod: $\psi = 1$, $\phi_e = 0.7$. Van Leer: $\psi = 4/3$, $\phi_e = 0.733$. Superbee: $\psi = 2$, $\phi_e = 0.8$.

Superbee at $r = 2$ reaches the TVD upper bound and coincides with linear upwind; minmod falls back to central.

</details>

**Exercise 2.** A heat-transfer calculation convects temperature in air ($\Gamma/\rho = 2\times10^{-5}$ m²/s) at $u = 1$ m/s on a mesh with $\Delta x = 1$ cm. Compute the cell Péclet number, the numerical diffusivity of first-order upwind and its ratio to the physical diffusivity, and the cell size needed for central differencing to be bounded.

<details>
<summary>Answer</summary>

$Pe_\Delta = u\Delta x\rho/\Gamma = 1 \times 0.01/(2\times10^{-5}) = 500$.

$\Gamma_{\mathrm{num}}/\rho = u\Delta x/2 = 5\times10^{-3}$ m²/s, 250 times the physical value.

Central differencing needs $Pe_\Delta \le 2$, that is $\Delta x \le 2 \times 2\times10^{-5}/1 = 4\times10^{-5}$ m, 250 times finer. Neither is acceptable, which is why a bounded second-order scheme is used.

</details>

**Exercise 3.** For QUICK on a uniform grid with $D = 1$ and $F = 2$ on both faces, compute $a_W$, $a_E$, $a_{WW}$ and $a_P$. Above which cell Péclet number does $a_E$ become negative, and what does the sign of $a_{WW}$ imply?

<details>
<summary>Answer</summary>

$a_W = 1 + 0.75 \times 2 + 0.125 \times 2 = 2.75$, $a_E = 1 - 0.375 \times 2 = 0.25$, $a_{WW} = -0.125 \times 2 = -0.25$, and $a_P = a_W + a_E + a_{WW} = 2.75$.

$a_E < 0$ when $D < 3F/8$, that is $Pe_\Delta > 8/3$.

$a_{WW}$ is negative for every flow rate, so QUICK never satisfies the positive-coefficient condition. It can overshoot near steep gradients, and the matrix is not an M-matrix, which is why it is implemented by deferred correction around the upwind matrix.

</details>

**Exercise 4.** A uniform flow of $U = 1$ m/s crosses a square grid with $\Delta x = \Delta y = 1$ cm at $\theta = 45^\circ$, with $\rho = 1$ kg/m³. Estimate the false diffusion coefficient of first-order upwind. How does it compare with the streamwise numerical diffusion of the same scheme for flow aligned with the grid?

<details>
<summary>Answer</summary>

With $\sin 2\theta = 1$ and $\sin^3\theta = \cos^3\theta = 2^{-3/2}$,

```math
\Gamma_{\mathrm{false}} = \frac{\rho U \Delta x^2}{4 \times 2 \times 2^{-3/2}\,\Delta x} = \frac{\rho U\Delta x}{2\sqrt{2}} = 3.5\times10^{-3}\ \text{kg/(m s)}
```

For grid-aligned flow, $\rho U\Delta x/2 = 5\times10^{-3}$ kg/(m s), but it acts along the streamlines where gradients are usually weak. The false diffusion at 45° is about 70% of that and acts across the streamlines, where it smears shear layers and fronts.

</details>

**Exercise 5.** Write the explicit Lax–Wendroff scheme for $\phi_t + u\phi_x = 0$ as $\phi_i^{n+1} = \sum_k c_k\phi_{i+k}^n$. Check the three moment conditions for second order, and use the coefficients to show that it violates Godunov's monotonicity condition for $0 < C < 1$. Where does $\psi = 1$ leave the TVD region of the Sweby diagram?

<details>
<summary>Answer</summary>

$\phi_i^{n+1} = \phi_i - \tfrac{C}{2}(\phi_{i+1} - \phi_{i-1}) + \tfrac{C^2}{2}(\phi_{i+1} - 2\phi_i + \phi_{i-1})$, so

```math
c_{-1} = \frac{C(1 + C)}{2}, \qquad c_0 = 1 - C^2, \qquad c_1 = -\frac{C(1 - C)}{2}
```

$\sum c_k = 1$; $`\sum k\,c_k = -C(1 + C)/2 - C(1 - C)/2 = -C`$; $\sum k^2c_k = C(1 + C)/2 - C(1 - C)/2 = C^2$. All three hold, so the scheme is second order.

$c_1 < 0$ for $0 < C < 1$, so the scheme is not monotonicity preserving: a step produces an undershoot or overshoot, 23% in the TVD script.

In the Sweby diagram the TVD condition $\psi \le 2r$ fails for $\psi = 1$ when $r < 1/2$, and $\psi$ must be 0 for $r \le 0$, where Lax–Wendroff still has $\psi = 1$. Both happen next to discontinuities and extrema.

</details>

## References

- H. K. Versteeg, W. Malalasekera, *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Prentice Hall, 2007. Chapter 5.
- R. J. LeVeque, *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002. Chapter 6.
- B. P. Leonard, "A stable and accurate convective modelling procedure based on quadratic upstream interpolation", *Computer Methods in Applied Mechanics and Engineering*, 19(1), 59–98, 1979.
- S. K. Godunov, "A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics", *Matematicheskii Sbornik*, 47(89), 271–306, 1959.
- A. Harten, "High resolution schemes for hyperbolic conservation laws", *Journal of Computational Physics*, 49(3), 357–393, 1983.
- P. K. Sweby, "High resolution schemes using flux limiters for hyperbolic conservation laws", *SIAM Journal on Numerical Analysis*, 21(5), 995–1011, 1984.
- S. V. Patankar, *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
- P. H. Gaskell, A. K. C. Lau, "Curvature-compensated convective transport: SMART, a new boundedness-preserving transport algorithm", *International Journal for Numerical Methods in Fluids*, 8(6), 617–641, 1988.
- P. K. Khosla, S. G. Rubin, "A diagonally dominant second-order accurate implicit scheme", *Computers & Fluids*, 2(2), 207–209, 1974.
- G. de Vahl Davis, G. D. Mallinson, "An evaluation of upwind and central difference approximations by a study of recirculating flow", *Computers & Fluids*, 4(1), 29–43, 1976.
