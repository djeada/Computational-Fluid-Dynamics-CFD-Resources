# Parametrized Variational Problems

Reduced-order models are built for families of problems: the same PDE solved for many values of a parameter such as a conductivity, a Péclet or Reynolds number, a boundary flux or a geometric dimension. This note sets up the abstract framework in which such families are analysed and in which the reduced basis method of the following notes is formulated: a Hilbert space, a parametrized bilinear and linear form, the conditions under which every member of the family is well posed, and the affine parameter dependence that makes fast online evaluation possible. The discretization of the problem is the subject of [Truth Discretization](discretization_techniques.md); the general weak formulation of PDEs is in [Weak Formulation of PDEs](../fem/weak_formulation_pde.md).

## Problem Statement

Let $\Omega \subset \mathbb{R}^d$, $`d \in \{1, 2, 3\}`$, be a bounded Lipschitz domain whose boundary is split into a Dirichlet part $\Gamma_D$ and a Neumann part $\Gamma_N$. Let $\mathcal{P} \subset \mathbb{R}^p$ be a closed and bounded parameter set. For each $\mu \in \mathcal{P}$:

```math
\text{find } u(\mu) \in V \text{ such that } a(u(\mu), v; \mu) = f(v; \mu) \quad \text{for all } v \in V,
\qquad \text{then evaluate } s(\mu) = \ell(u(\mu); \mu)
```

Here $V$ is a Hilbert space of functions on $\Omega$ with inner product $(\cdot, \cdot)_V$ and norm $`\lVert \cdot \rVert_V`$, $a(\cdot, \cdot; \mu) : V \times V \to \mathbb{R}$ is bilinear for each $\mu$, and $f(\cdot; \mu)$ and $\ell(\cdot; \mu)$ are linear functionals that represent sources and boundary data, and the quantity of interest. The output is called compliant when $\ell = f$ and $a$ is symmetric, which simplifies error estimation.

The problem is solved for a given $\mu$ when $u(\mu)$ is found; the question this note answers is under which conditions on $a$ and $f$ a unique solution exists and depends stably on the data, with constants whose dependence on $\mu$ is known. The difficulties are that these constants can degenerate at the edge of $\mathcal{P}$ (a conductivity tending to zero, a Péclet number tending to infinity), that non-symmetric problems have no energy norm, and that a form whose dependence on $\mu$ is not affine cannot be evaluated cheaply in a reduced model.

## Function Spaces

For a scalar field such as a temperature, the natural space with homogeneous Dirichlet data on $\Gamma_D$ is

```math
V = H^1_{\Gamma_D}(\Omega) = \{ v \in H^1(\Omega) : v = 0 \text{ on } \Gamma_D \},
\qquad \lVert v \rVert_V^2 = \int_\Omega \nabla v \cdot \nabla v \, d\mathbf{x}
```

where $H^1(\Omega)$ is the space of square-integrable functions with square-integrable first derivatives. If $\Gamma_D$ has positive measure, the Poincaré inequality $`\lVert v \rVert_{L^2} \le C_P\lVert \nabla v \rVert_{L^2}`$ makes the $H^1$ seminorm above a norm on $V$. For a vector field with $d_s$ components, such as a velocity or displacement, $V = (H^1_{\Gamma_D}(\Omega))^{d_s}$ with the sum of the component inner products. Inhomogeneous Dirichlet data $u = g$ on $\Gamma_D$ are handled by a lifting $R_g \in H^1(\Omega)$ with $R_g = g$ on $\Gamma_D$: write $u = R_g + u_0$ with $u_0 \in V$ and move $a(R_g, v; \mu)$ to the right-hand side.

## Well-Posedness

### Coercivity, Continuity and Lax–Milgram

The bilinear form is coercive and continuous if there are constants $\alpha(\mu) > 0$ and $\gamma(\mu) < \infty$ with

```math
\alpha(\mu) = \inf_{v \in V \setminus \{0\}} \frac{a(v, v; \mu)}{\lVert v \rVert_V^2},
\qquad
\gamma(\mu) = \sup_{u, v \in V \setminus \{0\}} \frac{a(u, v; \mu)}{\lVert u \rVert_V \lVert v \rVert_V}
```

and the load is bounded, $`\lVert f(\cdot; \mu) \rVert_{V'} = \sup_{v \ne 0} f(v; \mu)/\lVert v \rVert_V < \infty`$. The Lax–Milgram lemma then gives, for each $\mu$, a unique solution $u(\mu) \in V$ and the stability bound

$$
\lVert u(\mu) \rVert_V \le \frac{\lVert f(\cdot; \mu) \rVert_{V'}}{\alpha(\mu)}
$$

The bound follows from coercivity by testing with $v = u$: $`\alpha\lVert u \rVert_V^2 \le a(u, u; \mu) = f(u; \mu) \le \lVert f \rVert_{V'}\lVert u \rVert_V`$. The family is uniformly well posed if $\alpha(\mu) \ge \alpha_0 > 0$ and $\gamma(\mu) \le \gamma_0$ for all $\mu \in \mathcal{P}$. The ratio $\gamma(\mu)/\alpha(\mu)$ is the condition number of the problem: it bounds the Galerkin error relative to the best approximation ([Truth Discretization](discretization_techniques.md)) and the effectivity of reduced basis error bounds ([Reduced Basis Approximation](reduced_basis_approximation.md)).

### Noncoercive Problems

Saddle-point problems such as Stokes flow, and indefinite problems such as the Helmholtz equation, are not coercive. Their well-posedness rests on the inf-sup condition of Babuška,

```math
\beta(\mu) = \inf_{u \in V \setminus \{0\}}\ \sup_{v \in W \setminus \{0\}} \frac{a(u, v; \mu)}{\lVert u \rVert_V \lVert v \rVert_W} > 0
```

together with continuity, where the test space $W$ may differ from $V$. Everything below carries over with $\alpha(\mu)$ replaced by $\beta(\mu)$, but $\beta$ is harder to bound from below, and a Galerkin reduced space does not inherit the inf-sup condition, which is why reduced Navier–Stokes models need pressure stabilization ([POD-Galerkin Projection](pod_galerkin_projection.md)).

### Energy Norm

If $a$ is symmetric and coercive, $(u, v)_\mu = a(u, v; \mu)$ is an inner product on $V$, and its norm $`\lVert v \rVert_\mu = \sqrt{a(v, v; \mu)}`$ satisfies

```math
\sqrt{\alpha(\mu)}\,\lVert v \rVert_V \le \lVert v \rVert_\mu \le \sqrt{\gamma(\mu)}\,\lVert v \rVert_V
```

Reduced basis methods usually take $`\lVert \cdot \rVert_V`$ to be the energy norm at a reference parameter $\bar{\mu}$, so that $\alpha(\bar{\mu}) = \gamma(\bar{\mu}) = 1$ and the constants at other parameters measure how far the problem is from the reference.

## Affine Parameter Dependence

The forms depend affinely on the parameter if they can be written as finite sums of parameter-independent forms with scalar parameter-dependent coefficients:

```math
a(u, v; \mu) = \sum_{q=1}^{Q_a} \theta_q^a(\mu)\, a_q(u, v),
\qquad
f(v; \mu) = \sum_{q=1}^{Q_f} \theta_q^f(\mu)\, f_q(v),
\qquad
\ell(v; \mu) = \sum_{q=1}^{Q_\ell} \theta_q^\ell(\mu)\, \ell_q(v)
```

This is the property that lets a reduced model run without touching the full-order dimension. After discretization, $`A(\mu) = \sum_q\theta_q^a(\mu)A_q`$, and for any reduced basis $V_N$ the reduced matrices $V_N^TA_qV_N$ can be precomputed once. Online, assembling $A_N(\mu)$ costs $O(Q_aN^2)$ operations for each new $\mu$, independent of the number $N_h$ of truth unknowns. Without affine dependence, every new $\mu$ requires a full assembly of $A(\mu)$ followed by projection, which costs at least $O(N_hN)$ and destroys most of the speed-up.

Affine dependence arises naturally for piecewise-constant coefficients (each subdomain contributes one term) and for geometric parameters that enter through an affine map to a reference domain, such as a stretched rectangle (Exercise 5). A coefficient such as $k(\mathbf{x}; \mu) = e^{-\mu\lvert\mathbf{x}\rvert^2}$ or a general shape deformation is not affine; the empirical interpolation method replaces it by an affine approximation $\sum_{q=1}^{Q}\theta_q(\mu)k_q(\mathbf{x})$ with interpolation error controlled by $Q$ ([Reduced-Order Modeling](rom.md)).

## Example: The Thermal Block

The thermal block is the standard test problem of reduced basis methods. The unit square is divided into $B_1 \times B_2$ rectangular blocks $\Omega_q$ with conductivity $k = \mu_q$ in block $q$. A unit heat flux enters through the bottom edge $\Gamma_{\mathrm{in}}$, the top edge is held at $u = 0$ and the sides are insulated:

```math
V = \{ v \in H^1(\Omega) : v = 0 \text{ on the top edge} \},
\qquad
a(u, v; \mu) = \sum_{q=1}^{B_1B_2} \mu_q \int_{\Omega_q} \nabla u \cdot \nabla v \, d\mathbf{x},
\qquad
f(v) = \int_{\Gamma_{\mathrm{in}}} v \, ds
```

The form is affine with $\theta_q(\mu) = \mu_q$ and $`a_q(u, v) = \int_{\Omega_q}\nabla u \cdot \nabla v \, d\mathbf{x}`$, symmetric, and with $\ell = f$ the output $`s(\mu) = \int_{\Gamma_{\mathrm{in}}} u \, ds`$ (the mean temperature of the heated edge) is compliant. With $`\lVert v \rVert_V^2 = \sum_q a_q(v, v)`$, the energy norm at $\mu = (1, \dots, 1)$,

```math
\min_q \mu_q\,\lVert v \rVert_V^2 \le a(v, v; \mu) \le \max_q \mu_q\,\lVert v \rVert_V^2
```

so $\alpha(\mu) \ge \min_q \mu_q$ and $\gamma(\mu) \le \max_q \mu_q$. These bounds are free to evaluate and are used as the coercivity lower bound in the [thermal block script](../../../scripts/algorithms/reduced_basis_thermal_block/), which fixes $\mu_1 = 1$ and varies three conductivities in $[0.1, 10]$.

## Example: Advection–Diffusion with a Parametrized Péclet Number

Steady transport of a scalar by a given divergence-free velocity $\mathbf{b}$, with diffusivity $\varepsilon$, length $L$ and speed $U$, reads in nondimensional form $-\mathrm{Pe}^{-1}\Delta u + \mathbf{b} \cdot \nabla u = g$ with the Péclet number $\mathrm{Pe} = UL/\varepsilon$. Taking $\mu = \mathrm{Pe}$ and $u = 0$ on $\partial\Omega$,

```math
a(u, v; \mu) = \frac{1}{\mu}\int_\Omega \nabla u \cdot \nabla v \, d\mathbf{x} + \int_\Omega (\mathbf{b} \cdot \nabla u)\, v \, d\mathbf{x},
\qquad
f(v) = \int_\Omega g\, v \, d\mathbf{x}
```

The form is affine with $Q_a = 2$, $\theta_1 = 1/\mu$ and $\theta_2 = 1$, but not symmetric. Because $\nabla \cdot \mathbf{b} = 0$ and $v = 0$ on the boundary, $`\int_\Omega (\mathbf{b} \cdot \nabla v)v \, d\mathbf{x} = \frac{1}{2}\int_\Omega \mathbf{b} \cdot \nabla(v^2) \, d\mathbf{x} = 0`$, so in the norm $`\lVert v \rVert_V = \lVert \nabla v \rVert_{L^2}`$

$$
\alpha(\mu) = \frac{1}{\mu},
\qquad \gamma(\mu) \le \frac{1}{\mu} + C_P\lVert \mathbf{b} \rVert_{L^\infty}
$$

and $\gamma/\alpha \le 1 + \mu C_P\lVert \mathbf{b} \rVert_{L^\infty}$ grows linearly with the Péclet number. Large Péclet numbers bring thin boundary and interior layers whose position and thickness change with $\mu$, so the solution set becomes harder to approximate by a fixed low-dimensional space as well as worse conditioned. Both truth and reduced models then need stabilization, for example streamline-upwind Petrov–Galerkin (SUPG) terms, which keep the affine structure if the stabilization parameter is affine in $\mu$.

## Other Parametrized Problems

| Problem | Forms | Well-posedness | Typical parameters |
| --- | --- | --- | --- |
| Linear elasticity | $`a = \int 2G\,\boldsymbol{\varepsilon}(\mathbf{u}) : \boldsymbol{\varepsilon}(\mathbf{v}) + \lambda (\nabla \cdot \mathbf{u})(\nabla \cdot \mathbf{v})`$ | coercive (Korn), symmetric | Young's modulus per subdomain, thickness |
| Stokes flow | velocity–pressure saddle point | inf-sup | viscosity, inflow profile, geometry |
| Unsteady heat conduction | $m(\partial_t u, v) + a(u, v; \mu) = f(v; \mu)$ | coercive $a$, $m$ the $L^2$ product | conductivity, heat transfer coefficient |
| Helmholtz equation | $\int \nabla u \cdot \nabla v - \kappa^2 uv$ | inf-sup, fails at resonances | wavenumber $\kappa$ |

## Key Takeaways

- A parametrized variational problem seeks, for each $\mu$, the $u(\mu) \in V$ with $a(u, v; \mu) = f(v; \mu)$ for all test functions $v$, and an output $s(\mu) = \ell(u(\mu); \mu)$.
- Coercivity $\alpha(\mu)$, continuity $\gamma(\mu)$ and a bounded load give a unique solution with $`\lVert u \rVert_V \le \lVert f \rVert_{V'}/\alpha(\mu)`$ (Lax–Milgram); noncoercive problems need an inf-sup constant $\beta(\mu)$.
- The ratio $\gamma/\alpha$ measures how well conditioned a member of the family is; it grows with the Péclet number in advection–diffusion.
- Affine dependence $a = \sum_q\theta_q(\mu)a_q$ is what makes the online cost of a reduced model independent of the truth dimension; non-affine terms are made affine by empirical interpolation.
- In the thermal block, $\min_q\mu_q$ and $\max_q\mu_q$ are rigorous coercivity and continuity bounds in the reference energy norm.

## Related Scripts

- [Certified Reduced Basis Method for a Thermal Block](../../../scripts/algorithms/reduced_basis_thermal_block/): builds a certified reduced basis model of steady heat conduction in a 2D thermal block with three parametrized conductivities, using a weak greedy algorithm driven by the residual-based error bound $`\lVert r(\mu) \rVert_{X'}/\alpha_{\mathrm{LB}}(\mu)`$.

## Exercises

**Exercise 1.** Let $`a(u, v; \mu) = \mu\int_\Omega \nabla u \cdot \nabla v \, d\mathbf{x}`$ on $V = H_0^1(\Omega)$ with $`\lVert v \rVert_V = \lVert \nabla v \rVert_{L^2}`$ and $\mu \in \mathcal{P} = [0.1, 10]$. Find $\alpha(\mu)$ and $\gamma(\mu)$, and the uniform constants over $\mathcal{P}$.

<details>
<summary>Answer</summary>

$`a(v, v; \mu) = \mu\lVert v \rVert_V^2`$, so $\alpha(\mu) = \mu$. By Cauchy–Schwarz, $`\lvert a(u, v; \mu) \rvert \le \mu\lVert u \rVert_V\lVert v \rVert_V`$, with equality for $u = v$, so $\gamma(\mu) = \mu$. Uniformly, $\alpha(\mu) \ge 0.1$ and $\gamma(\mu) \le 10$.

</details>

**Exercise 2.** On $\Omega = (0, 1)$ take $`f(v) = \int_0^1 v \, dx`$. Use the Poincaré inequality $`\lVert v \rVert_{L^2} \le \lVert v' \rVert_{L^2}/\pi`$ on $H^1_0(0, 1)$ to show that $`\lVert f \rVert_{V'} \le 1/\pi`$. Evaluate the Lax–Milgram stability bound for the form of Exercise 1 at $\mu = 0.1$, and compare it with the exact solution of $-\mu u'' = 1$, $u = x(1-x)/(2\mu)$.

<details>
<summary>Answer</summary>

$`\lvert f(v) \rvert \le \lVert 1 \rVert_{L^2}\lVert v \rVert_{L^2} \le \lVert v' \rVert_{L^2}/\pi`$, so $`\lVert f \rVert_{V'} \le 1/\pi \approx 0.318`$.

The bound is $`\lVert u \rVert_V \le (1/\pi)/0.1 = 3.18`$. Exactly, $u' = (1 - 2x)/(2\mu)$ and $\int_0^1 (1 - 2x)^2 dx = 1/3$, so $`\lVert u' \rVert_{L^2} = 1/(2\sqrt{3}\,\mu) \approx 2.89`$, below the bound and fairly close to it.

</details>

**Exercise 3.** For the advection–diffusion form $`a(u, v; \mu) = \mu\int_0^1 u'v' \, dx + b\int_0^1 u'v \, dx`$ on $H_0^1(0, 1)$ with $b = 1$ and $\mu \in [0.01, 1]$, show that $\alpha(\mu) = \mu$ and $\gamma(\mu) \le \mu + \lvert b \rvert/\pi$. Is the problem uniformly well posed? Can $a$ define an inner product?

<details>
<summary>Answer</summary>

$`\int_0^1 v'v \, dx = [v^2/2]_0^1 = 0`$, so $`a(v, v; \mu) = \mu\lVert v' \rVert^2`$ and $\alpha(\mu) = \mu \ge 0.01 > 0$. Continuity follows from $`\lvert b\int u'v \rvert \le \lvert b \rvert\,\lVert u' \rVert\,\lVert v' \rVert/\pi`$, giving $\gamma(\mu) \le \mu + 1/\pi \le 1.318$. The problem is uniformly coercive and continuous, so it is well posed for every $\mu$, but $\gamma/\alpha$ reaches $1 + 1/(0.01\pi) \approx 32.8$ at the smallest $\mu$. Because $a$ is not symmetric ($\int u'v \ne \int v'u$ in general), it does not define an inner product.

</details>

**Exercise 4.** For the symmetric reaction–diffusion form $`a(u, v) = \int_0^1 u'v' \, dx + \sigma\int_0^1 uv \, dx`$ with $\sigma = 10$ on $H_0^1(0, 1)$, show that $`\lVert v \rVert_V \le \lVert v \rVert_a \le \sqrt{1 + \sigma/\pi^2}\,\lVert v \rVert_V`$ and evaluate the constant. Show that $v = \sin(\pi x)$ attains the upper bound.

<details>
<summary>Answer</summary>

$`\lVert v \rVert_a^2 = \lVert v' \rVert^2 + \sigma\lVert v \rVert^2 \ge \lVert v' \rVert^2 = \lVert v \rVert_V^2`$. By Poincaré, $`\sigma\lVert v \rVert^2 \le (\sigma/\pi^2)\lVert v' \rVert^2`$, so $`\lVert v \rVert_a^2 \le (1 + \sigma/\pi^2)\lVert v \rVert_V^2`$. The constant is $\sqrt{1 + 10/\pi^2} = \sqrt{2.0132} \approx 1.419$.

For $v = \sin(\pi x)$: $`\lVert v' \rVert^2 = \pi^2/2`$ and $`\lVert v \rVert^2 = 1/2`$, so $`\lVert v \rVert_a^2/\lVert v \rVert_V^2 = (\pi^2/2 + 5)/(\pi^2/2) = 1 + 10/\pi^2`$. The bound is attained because $\sin(\pi x)$ is the extremal function of the Poincaré inequality.

</details>

**Exercise 5.** The problem $-u'' = 1$ on $(0, \mu)$, $u(0) = u(\mu) = 0$, has a parameter-dependent domain. Map it to the reference interval $(0, 1)$ with $x = \mu\hat{x}$, write the weak form for $\hat{u}(\hat{x}) = u(\mu\hat{x})$, and identify its affine decomposition. Check the result against the exact solution.

<details>
<summary>Answer</summary>

With $`dx = \mu\,d\hat{x}`$ and $d/dx = \mu^{-1}d/d\hat{x}$,

```math
\int_0^\mu u'v' \, dx = \frac{1}{\mu}\int_0^1 \hat{u}'\hat{v}' \, d\hat{x},
\qquad
\int_0^\mu v \, dx = \mu\int_0^1 \hat{v} \, d\hat{x}
```

so $`a(\hat{u}, \hat{v}; \mu) = \theta^a(\mu)\,a_1(\hat{u}, \hat{v})`$ with $\theta^a = 1/\mu$, and $`f(\hat{v}; \mu) = \theta^f(\mu)\,f_1(\hat{v})`$ with $\theta^f = \mu$, on the fixed space $H^1_0(0, 1)$. The reference problem $-\hat{u}''/\mu = \mu$ gives $\hat{u} = \mu^2\hat{x}(1 - \hat{x})/2$, and the exact solution $u = x(\mu - x)/2$ at $x = \mu\hat{x}$ is the same function. All solutions are multiples of one function, so a reduced basis with one vector is exact for every $\mu$.

</details>

## References

- L. C. Evans, *Partial Differential Equations*, 2nd ed., American Mathematical Society, 2010.
- S. C. Brenner and L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Springer, 2008.
- A. Ern and J.-L. Guermond, *Theory and Practice of Finite Elements*, Applied Mathematical Sciences 159, Springer, 2004.
- I. Babuška, "Error-bounds for finite element method", *Numerische Mathematik* 16, 322–333, 1971.
- A. Quarteroni, A. Manzoni and F. Negri, *Reduced Basis Methods for Partial Differential Equations: An Introduction*, Springer, 2016.
- J. S. Hesthaven, G. Rozza and B. Stamm, *Certified Reduced Basis Methods for Parametrized Partial Differential Equations*, SpringerBriefs in Mathematics, Springer, 2016.
- G. Rozza, D. B. P. Huynh and A. T. Patera, "Reduced basis approximation and a posteriori error estimation for affinely parametrized elliptic coercive partial differential equations", *Archives of Computational Methods in Engineering* 15(3), 229–275, 2008.
