# Weak Formulation of a Reaction–Diffusion Equation

Every finite element solver starts from a weak form: the equation multiplied by test functions, integrated over the domain, and integrated by parts until the trial and test functions carry the same number of derivatives. This note carries out the derivation for a time-dependent reaction–diffusion equation, the template for heat conduction, scalar transport and the energy equation in CFD. It states the function spaces precisely, shows where each kind of boundary condition goes, proves well-posedness of the steady problem with the Lax–Milgram lemma, and discretizes in space and time to reach the fully discrete matrix system. The Galerkin method, basis functions and error estimates are introduced in [Finite Element Method](./intro.md).

## Problem Statement

Let $\Omega \subset \mathbb{R}^d$ be a bounded domain with boundary $\Gamma = \partial\Omega$ split into a Dirichlet part $\Gamma_D$ and a Neumann part $\Gamma_N$. Find $u(\mathbf{x}, t)$ such that

```math
\frac{\partial u}{\partial t} = \nabla\cdot\left(D\,\nabla u\right) - s\,u + f \quad \text{in } \Omega \times (0, T]
```

```math
u = g \ \text{on } \Gamma_D, \qquad D\,\frac{\partial u}{\partial n} = q \ \text{on } \Gamma_N, \qquad u(\mathbf{x}, 0) = u_0(\mathbf{x}) \ \text{in } \Omega
```

Here $u$ is a concentration or temperature, $D(\mathbf{x})$ the diffusivity with $0 < D_0 \le D \le D_1$, $s(\mathbf{x}) \ge 0$ a first-order reaction (decay) rate, $f$ a source, $g$ a prescribed value, $q$ a prescribed flux and $\mathbf{n}$ the outward unit normal. The goal is a weak formulation that needs only one derivative of $u$, is well-posed (a unique solution that depends continuously on the data), and leads after discretization to a linear system for the nodal values at each time level. A solution of that system is acceptable when its error decreases at the rates predicted by the theory as $h$ and $\Delta t$ are reduced, and when it inherits the stability of the continuous problem: no growth of $`\|u\|`$ when $f = 0$, $q = 0$ and $g = 0$.

## Function Spaces

The weak form is posed in Sobolev spaces, which measure functions by integrals rather than pointwise values. $L^2(\Omega)$ is the space of square-integrable functions, with inner product $`(u, v) = \int_\Omega uv\,d\Omega`$ and norm $`\|u\| = (u, u)^{1/2}`$. $H^1(\Omega)$ contains the functions in $L^2(\Omega)$ whose first (weak) derivatives are also in $L^2(\Omega)$, with norm and seminorm

```math
\| u\|_{H^1}^2 = \int_\Omega \left(u^2 + |\nabla u|^2\right) d\Omega,
\qquad
| u|_{H^1} = \| \nabla u\|
```

Functions in $H^1$ can have kinks (a continuous piecewise linear function is in $H^1$) but not jumps. A function in $H^1(\Omega)$ has a well-defined boundary value (its trace) in $L^2(\Gamma)$, so a condition such as $u = g$ on $\Gamma_D$ makes sense, and the functions that vanish on $\Gamma_D$ form the subspace

```math
H^1_{\Gamma_D}(\Omega) = \left\{v \in H^1(\Omega) : v = 0 \text{ on } \Gamma_D\right\}
```

written $H^1_0(\Omega)$ when $\Gamma_D = \Gamma$.

The trial space consists of the functions in $H^1(\Omega)$ that equal $g$ on $\Gamma_D$, and the test space is $V = H^1_{\Gamma_D}(\Omega)$. The two differ by a fixed function: if $u_g \in H^1(\Omega)$ is any extension (lifting) of $g$, then $u = u_g + w$ with $w \in V$. Test functions vanish exactly where the solution is prescribed, because there the equation is replaced by the boundary condition and there is nothing to test.

When $\Gamma_D$ has positive measure, the **Poincaré inequality** holds on $V$:

```math
\| v\| \le C_P\,\| \nabla v\| \quad \text{for all } v \in V
```

with a constant $C_P$ that depends on the domain (for $\Omega = (0, L)$ with $v(0) = 0$, $C_P = 2L/\pi$). It makes the seminorm $`|v|_{H^1}`$ a norm on $V$ and is what makes the pure diffusion problem coercive.

## Derivation

Multiply the equation by a test function $v \in V$ and integrate over $\Omega$:

```math
\int_\Omega \frac{\partial u}{\partial t}\,v\,d\Omega = \int_\Omega \nabla\cdot\left(D\nabla u\right) v\,d\Omega - \int_\Omega s\,u\,v\,d\Omega + \int_\Omega f\,v\,d\Omega
```

The product rule $`\nabla\cdot(vD\nabla u) = v\,\nabla\cdot(D\nabla u) + D\nabla u\cdot\nabla v`$ and the divergence theorem give Green's first identity,

```math
\int_\Omega \nabla\cdot\left(D\nabla u\right) v\,d\Omega = \int_\Gamma v\,D\,\frac{\partial u}{\partial n}\,d\Gamma - \int_\Omega D\,\nabla u\cdot\nabla v\,d\Omega
```

The boundary integral splits into two parts. On $\Gamma_D$ it vanishes because $v = 0$ there. On $\Gamma_N$ the flux $`D\,\partial u/\partial n`$ is the prescribed $q$. Therefore

```math
\int_\Gamma v\,D\,\frac{\partial u}{\partial n}\,d\Gamma = \int_{\Gamma_N} q\,v\,d\Gamma
```

and the weak formulation is: find $u(t)$ with $u(t) - u_g \in V$ for each $t$ and $u(0) = u_0$, such that

```math
\left(\frac{\partial u}{\partial t}, v\right) + a(u, v) = \ell(v) \quad \text{for all } v \in V
```

with the bilinear and linear forms

```math
a(u, v) = \int_\Omega \left(D\,\nabla u\cdot\nabla v + s\,u\,v\right) d\Omega,
\qquad
\ell(v) = \int_\Omega f\,v\,d\Omega + \int_{\Gamma_N} q\,v\,d\Gamma
```

The Dirichlet condition is built into the trial space (essential), and the Neumann condition appears only in $\ell$ (natural). With $q = 0$ on $\Gamma_N$ (no flux) the boundary term drops out entirely, not because $v$ vanishes but because the flux does. If the solution of the weak problem is smooth enough, integrating by parts backwards and choosing $v$ freely in the interior and on $\Gamma_N$ recovers both the differential equation and the Neumann condition.

## Well-Posedness: The Lax–Milgram Lemma

Consider first the steady problem: find $w \in V$ with $a(w, v) = \ell(v) - a(u_g, v)$ for all $v \in V$. The **Lax–Milgram lemma** states that if $V$ is a Hilbert space and

1. $a$ is continuous: $`|a(u, v)| \le M\| u\|_{H^1}\| v\|_{H^1}`$,
2. $a$ is coercive: $`a(v, v) \ge \alpha\| v\|_{H^1}^2`$ with $\alpha > 0$,
3. $\ell$ is continuous: $`|\ell(v)| \le \Lambda\| v\|_{H^1}`$,

then the problem has exactly one solution, and $`\|w\|_{H^1} \le \Lambda/\alpha`$. For the reaction–diffusion form:

- Continuity follows from the Cauchy–Schwarz inequality with $M = \max(D_1, \max s)$. Continuity of $\ell$ needs $f \in L^2(\Omega)$ and $q \in L^2(\Gamma_N)$, together with the trace inequality.
- Coercivity: $`a(v, v) \ge D_0\|\nabla v\|^2 + \int s v^2\,d\Omega`$. If $s \ge s_0 > 0$, then $\alpha = \min(D_0, s_0)$. If $s = 0$ but $\Gamma_D$ has positive measure, the Poincaré inequality gives $`\|v\|_{H^1}^2 \le (1 + C_P^2)\|\nabla v\|^2`$, so $\alpha = D_0/(1 + C_P^2)$.
- If $s = 0$ and $\Gamma_D$ is empty (pure Neumann), constants satisfy $a(1, 1) = 0$ and coercivity fails. The solution is unique only up to a constant, and it exists only if $`\ell(1) = \int_\Omega f\,d\Omega + \int_\Gamma q\,d\Gamma = 0`$ (the sources balance the boundary fluxes).

Lax–Milgram also applies to the discrete problem on any subspace $V_h \subset V$ with the same constants. This is the starting point of Céa's lemma and of the error estimates in [Finite Element Method](./intro.md#a-priori-error-estimates).

For the time-dependent problem with $f = 0$, $q = 0$, $g = 0$, choosing $v = u$ gives the energy identity

```math
\frac{1}{2}\frac{d}{dt}\| u\|^2 + a(u, u) = 0
\quad\Longrightarrow\quad
\| u(t)\| \le \| u_0\|
```

The $L^2$ norm of the solution never grows. A good discretization should reproduce this property.

## Spatial Discretization

Choose a finite element space $V_h \subset V$ with basis $\phi_1, \dots, \phi_n$ and expand $`u_h(\mathbf{x}, t) = \sum_j U_j(t)\,\phi_j(\mathbf{x})`$ (for $g = 0$; otherwise the Dirichlet nodes are fixed and moved to the right-hand side). Taking $v = \phi_i$ gives a system of ordinary differential equations for the nodal values:

```math
M\frac{dU}{dt} + (K + R)\,U = F(t),
\qquad
M_{ij} = \int_\Omega \phi_i\phi_j\,d\Omega,
\quad
K_{ij} = \int_\Omega D\,\nabla\phi_j\cdot\nabla\phi_i\,d\Omega,
\quad
R_{ij} = \int_\Omega s\,\phi_j\phi_i\,d\Omega
```

with $F_i = \ell(\phi_i)$. $M$ is the mass matrix, $K$ the stiffness (diffusion) matrix and $R$ the reaction matrix; for constant $s$, $R = sM$. All three are symmetric, $M$ is positive definite and $K$ positive semi-definite, with $K\mathbf{1} = \mathbf{0}$ when there are no Dirichlet nodes. In 1D with linear elements of length $h$ and constant $D$,

```math
M^e = \frac{h}{6}\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix},
\qquad
K^e = \frac{D}{h}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}
```

Replacing $M$ by a diagonal matrix with the row sums of $M$ on the diagonal (mass lumping) turns the P1 system into the standard finite difference scheme, and makes explicit time stepping cheap.

## Time Discretization: The θ-Scheme

Let $U^n \approx U(t^n)$ with $t^n = n\Delta t$ and $A = K + R$. The θ-scheme evaluates the spatial terms as a weighted average of the old and new time levels:

```math
\left(M + \theta\Delta t\,A\right)U^{n+1} = \left(M - (1 - \theta)\Delta t\,A\right)U^n + \Delta t\left(\theta F^{n+1} + (1 - \theta)F^n\right)
```

| $\theta$ | Scheme | Order in $\Delta t$ | Stability |
| --- | --- | --- | --- |
| 0 | forward Euler | 1 | $\Delta t \le 2/\lambda_{\max}$ |
| 1/2 | Crank–Nicolson | 2 | unconditional; large-$`\Delta t`$ modes oscillate |
| 1 | backward Euler | 1 | unconditional; damps all modes (L-stable) |

Here $\lambda_{\max}$ is the largest eigenvalue of the generalized problem $A\mathbf{x} = \lambda M\mathbf{x}$. A mode with eigenvalue $\lambda \ge 0$ is multiplied in each step by

```math
G(\lambda\Delta t) = \frac{1 - (1 - \theta)\lambda\Delta t}{1 + \theta\lambda\Delta t}
```

and $|G| \le 1$ for every $\lambda\Delta t \ge 0$ exactly when $\theta \ge 1/2$. For Crank–Nicolson $G \to -1$ as $\lambda\Delta t \to \infty$, so stiff, poorly resolved modes (sharp initial data, for example) decay slowly while changing sign every step; backward Euler sends them to zero. For 1D P1 elements, $\lambda_{\max} \approx 12D/h^2$ with the consistent mass matrix, so forward Euler requires $\Delta t \le h^2/(6D)$; with the lumped mass matrix $\lambda_{\max} \approx 4D/h^2$ and the limit is the finite difference value $h^2/(2D)$. Even explicit schemes require a solve with $M$ at every step unless the mass is lumped.

For $\theta \ge 1/2$ the system matrix $`M + \theta\Delta t\,A`$ is symmetric positive definite, so it is solved by a Cholesky factorization computed once (for a fixed $\Delta t$) or by preconditioned conjugate gradients. Time integration methods are compared in more depth in [Time Integration](../cfd/time_integration.md), and stability analysis in [Numerical Stability](../cfd/numerical_stability.md).

## Key Takeaways

- The weak form needs only $u \in H^1$, so piecewise polynomials with kinks are admissible solutions.
- Test functions vanish on the Dirichlet boundary; Neumann data enter the right-hand side through the boundary integral of Green's identity.
- Lax–Milgram gives existence and uniqueness from continuity and coercivity; coercivity comes from the reaction term or, through the Poincaré inequality, from a Dirichlet boundary.
- Semi-discretization gives $M\dot U + (K + R)U = F$; the θ-scheme is unconditionally stable for $\theta \ge 1/2$, second order only for $\theta = 1/2$.
- With a consistent mass matrix the explicit time-step limit is three times smaller than with a lumped one.

## Related Scripts

- [1D Poisson Equation With Finite Elements](../../../scripts/algorithms/fem_1d_poisson/): solves the 1D Poisson equation $-u'' = f$ on $(0, 1)$ with homogeneous Dirichlet conditions by the Galerkin finite element method with linear (P1) and quadratic (P2) Lagrange elements, and confirms the a priori error estimates: the $L^2$ error falls as $h^{p+1}$ and the $H^1$ error as $h^p$.
- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [Gray-Scott Reaction-Diffusion Simulation](../../../scripts/simulations/gray_scott_reaction_diffusion/): simulates the Gray-Scott reaction-diffusion system, in which two chemicals that react and diffuse on a periodic square turn a small seeded square into self-replicating spots or branching coral, and animates the concentration of one of them with Matplotlib.

## Exercises

**Exercise 1.** Suppose $\Gamma = \Gamma_D \cup \Gamma_N$ with $u = g$ on $\Gamma_D$ and $\partial u/\partial n = 0$ on $\Gamma_N$. Which conditions do the trial and test functions satisfy, and why does the boundary integral of Green's identity vanish?

<details>
<summary>Answer</summary>

- Trial functions satisfy the essential condition $u = g$ on $\Gamma_D$.
- Test functions vanish on $\Gamma_D$: $`V = \{v \in H^1(\Omega) : v = 0 \text{ on } \Gamma_D\}`$.

The boundary integral $`\int_\Gamma v D\,\partial u/\partial n\,d\Gamma`$ vanishes for two different reasons: on $\Gamma_D$ because $v = 0$, and on $\Gamma_N$ because $\partial u/\partial n = 0$.

</details>

**Exercise 2.** Show that the steady problem $`-u'' + s\,u = f`$ on $(0, 1)$ with $u'(0) = u'(1) = 0$ is coercive on $H^1(0, 1)$ when $s > 0$, and give $\alpha$. What fails when $s = 0$, and what condition must $f$ then satisfy?

<details>
<summary>Answer</summary>

Here $`a(v, v) = \|v'\|^2 + s\|v\|^2 \ge \min(1, s)\left(\|v'\|^2 + \|v\|^2\right) = \min(1, s)\|v\|_{H^1}^2`$, so $\alpha = \min(1, s)$.

For $s = 0$ the constant function $v = 1$ gives $a(1, 1) = 0$ with $`\|1\|_{H^1} = 1`$, so no $\alpha > 0$ exists. Choosing $v = 1$ in the weak form gives $`0 = \int_0^1 f\,dx`$, so a solution exists only if $f$ has zero mean, and then it is unique only up to an added constant.

</details>

**Exercise 3.** In 1D with linear elements of length $h$ and constant $D$ and $s$, write the fully discrete θ-scheme for $f = 0$, $q = 0$ and no Dirichlet nodes. For backward Euler, show that the system matrix is symmetric positive definite.

<details>
<summary>Answer</summary>

With $R = sM$:

```math
\left[(1 + \theta\Delta t\,s)M + \theta\Delta t\,K\right]U^{n+1} = \left[(1 - (1 - \theta)\Delta t\,s)M - (1 - \theta)\Delta t\,K\right]U^n
```

assembled from $M^e$ with entries $h/3$ (diagonal) and $h/6$ (off-diagonal) and $K^e$ with entries $\pm D/h$. For $\theta = 1$ this is $`[(1 + \Delta t\,s)M + \Delta t\,K]U^{n+1} = MU^n`$. $M$ is symmetric positive definite and $K$ symmetric positive semi-definite, so for $\Delta t > 0$ and $s \ge 0$ their positive combination is symmetric positive definite and a linear solve is needed at each step.

</details>

**Exercise 4.** Take $\Omega = [0, 1]$ as a single linear element with $D = 1$, $s = 0$ and $\Delta t = 0.1$, starting from nodal values $U^0 = (1, 0)$. Compute $U^1$ with backward Euler, and verify that $`\int_\Omega u_h\,dx`$ is conserved, as expected with no-flux boundaries and no reaction.

<details>
<summary>Answer</summary>

With $h = 1$, $M$ has diagonal $1/3$ and off-diagonal $1/6$, and $K$ has diagonal $1$ and off-diagonal $-1$. The system $(M + 0.1K)U^1 = MU^0$ reads

```math
\frac{13}{30}U_1 + \frac{1}{15}U_2 = \frac{1}{3},
\qquad \frac{1}{15}U_1 + \frac{13}{30}U_2 = \frac{1}{6}
```

Adding the equations gives $U_1 + U_2 = 1$; subtracting gives $U_1 - U_2 = 5/11$. So $U^1 = (8/11, 3/11) = (0.727, 0.273)$.

For one linear element $`\int u_h\,dx = (U_1 + U_2)/2`$, which is $0.5$ both before and after the step. Mass is conserved because every row and column of $K$ sums to zero: multiplying the scheme by $\mathbf{1}^T$ gives $`\mathbf{1}^T M U^{n+1} = \mathbf{1}^T M U^n`$, and $`\mathbf{1}^T M U = \int u_h\,dx`$.

</details>

**Exercise 5.** Show that the backward-Euler weak form is unconditionally stable in the $L^2$ norm when $D \ge 0$ and $s \ge 0$ (with $f = 0$, $q = 0$, $g = 0$). Then find the largest stable forward Euler time step for 1D P1 elements with consistent mass, using the sawtooth mode.

<details>
<summary>Answer</summary>

With $v = u^{n+1}$ in $`(u^{n+1} - u^n, v) + \Delta t\,a(u^{n+1}, v) = 0`$:

```math
\| u^{n+1}\|^2 + \Delta t\, a(u^{n+1}, u^{n+1}) = (u^n, u^{n+1}) \le \| u^n\|\,\| u^{n+1}\|
```

by Cauchy–Schwarz. Since $a(u^{n+1}, u^{n+1}) \ge 0$, this gives $`\|u^{n+1}\| \le \|u^n\|`$ for any $\Delta t > 0$.

For forward Euler the sawtooth $U_j = (-1)^j$ is the worst case. The assembled interior rows of $K$ are $(D/h)(-1, 2, -1)$ and those of $M$ are $(h/6)(1, 4, 1)$, so $`(KU)_j = (D/h)(1 + 2 + 1)(-1)^j = (4D/h)(-1)^j`$ and $`(MU)_j = (h/6)(-1 + 4 - 1)(-1)^j = (h/3)(-1)^j`$. So $`\lambda_{\max} = (4D/h)/(h/3) = 12D/h^2`$, and $`|G| = |1 - \lambda\Delta t| \le 1`$ requires $`\Delta t \le 2/\lambda_{\max} = h^2/(6D)`$, three times smaller than the lumped-mass (finite difference) limit $h^2/(2D)$.

</details>

## References

- S. C. Brenner and L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Springer, 2008.
- L. C. Evans, *Partial Differential Equations*, 2nd ed., American Mathematical Society, 2010.
- M. G. Larson and F. Bengzon, *The Finite Element Method: Theory, Implementation, and Applications*, Springer, 2013.
- V. Thomée, *Galerkin Finite Element Methods for Parabolic Problems*, 2nd ed., Springer, 2006.
- A. Quarteroni and A. Valli, *Numerical Approximation of Partial Differential Equations*, Springer, 1994.
- T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Dover, 2000.
