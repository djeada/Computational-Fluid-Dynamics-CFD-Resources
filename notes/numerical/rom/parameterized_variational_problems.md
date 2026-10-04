## Parameterized Variational Problems

In computational science and engineering, many physical and mechanical systems depend on parameters that can significantly change their behavior. Examples include varying material properties, geometrical dimensions, boundary conditions, or force terms. Our goal is to define and analyze a **parameterized variational problem**, where we solve a partial differential equation (PDE) (or system of PDEs) for different parameter values $\mu$ from a parameter set $\mathcal{P}$.

### The Setting

**Domain and Dimension**

- Let $\Omega \subset \mathbb{R}^d$ be a **bounded**, sufficiently regular domain, where $`d \in \{1,2,3\}`$ is the spatial dimension.

- The boundary $\partial \Omega$ is decomposed into (possibly) multiple subdomains, and $\partial \Omega_D \subset \partial \Omega$ denotes the portion where Dirichlet boundary conditions are imposed.\
  **Field Variables**

- We consider both scalar and vector fields. A field $u : \Omega \to \mathbb{R}^q$ can represent:

  - Temperature (if $q=1$),
  - Displacement (if $q = d_s$),
  - Velocity fields in fluid flow (again $q = d_s$),
  - Or other physical quantities of interest.

- Here $d_s$ indicates the dimension of the field variable; thus $q$ matches that dimension:

  - **Scalar field**: $q = 1$.
  - **Vector field**: $q = d_s$.

### Function Spaces

To formulate the PDE in a **variational** (weak) form, we need to work in an appropriate **Hilbert space** that accommodates the required boundary conditions and regularity.

I. **Scalar Field Space**

For a scalar problem, each component function (there is only one if $q=1$) belongs to

```math
V_i(\Omega) = \{\, v \in H^1(\Omega): \, v|_{\partial \Omega_D} = 0\,\}, \quad 1 \leq i
\leq d_s
```

This is the standard Sobolev space $H^1(\Omega)$, but restricted so that the function $v$ vanishes on the Dirichlet boundary $\partial \Omega_D$. The subscript $i$ allows for the possibility of multiple components if needed.

II. **Vector Field Space**

For a vector field $u(\mu) = (u_1(\mu),\ldots,u_{d_s}(\mu))$, we define the product space:

```math
V = V_1(\Omega)\,\times \cdots \times\, V_{d_s}(\Omega)
```

so that each component $u_i(\mu)$ belongs to $V_i(\Omega)$. Since each $V_i(\Omega)$ is a Hilbert space, their product $V$ is also a Hilbert space under a suitable inner product $(\cdot,\cdot)_V$. In turn, this induces a norm $`\|u\|_V = \sqrt{(u,u)_V}`$, ensuring $V$ is a normed, complete space.

### Parameter Domain

- Let $\mu \in \mathcal{P} \subset \mathbb{R}^p$ be a **parameter vector**, where $\mathcal{P}$ is a closed, bounded domain in parameter space.
- Each parameter $\mu$ could represent:
  - **Material properties** (e.g., Young’s modulus, conductivity),
  - **Geometric parameters** (e.g., shape dimensions),
  - **Boundary/loading conditions** (e.g., magnitude of applied forces).
    The solution will then be written as:

```math
u(\mu) = \bigl(u_1(\mu),\, u_2(\mu),\,\ldots,\, u_{d_s}(\mu)\bigr) \in V
```

indicating that for each $\mu$, we solve a PDE and obtain a solution in the Hilbert space $V$.

## Parametric Weak Formulation

We consider a **parametric variational problem** of the form:

```math
a\bigl(u(\mu);\, v;\,\mu\bigr) = f\bigl(v;\,\mu\bigr), \quad \forall \, v \in V
```

Here:

- $a(\cdot;\cdot;\mu) : V \times V \to \mathbb{R}$ is a **parameterized bilinear form**, linear and continuous in both arguments for each fixed $\mu$.
- $f(\cdot;\mu) : V \to \mathbb{R}$ is a **parameterized linear functional** that represents sources, loads, or other forcing terms.
  Thus, for each $\mu \in \mathcal{P}$, the **weak formulation** is:\
  **Find** $u(\mu) \in V$ **such that**

```math
a\bigl(u(\mu), v;\mu\bigr) = f\bigl(v;\mu\bigr), \quad \forall \, v \in V
```

After solving for $u(\mu)$, we might be interested in **outputs** such as

$$
s(\mu) = l\bigl(u(\mu);\mu\bigr)
$$

where $l(\cdot;\mu): V \to \mathbb{R}$ is another linear functional capturing specific physical quantities (e.g., total flux, average displacement, stress intensity).

### Examples and Simplifications

I. **Linear Elasticity (Compliance Problems)**

- The bilinear form $a(u,v;\mu)$ represents the internal strain energy or stiffness effect, and $f(v;\mu)$ accounts for external forces.
- If the PDE is self-adjoint (common in linear elasticity), then $a(u,v;\mu)$ is symmetric for all $\mu$.

II. **Convection-Diffusion Problems**

- The bilinear form $a(u,v;\mu)$ typically combines diffusive terms (e.g., $\nabla u \cdot \nabla v$) with advective (convection) terms (e.g., $\mathbf{b}\cdot \nabla u$), each possibly dependent on parameters.
- $\mu$ can represent a **Peclet number**, **diffusivity**, or **convective velocity** scaling.

## Well-Posedness and Requirements

To make sure that the parameterized problem admits a **unique solution** for each $\mu$, we typically rely on conditions analogous to those in the **Lax–Milgram** theorem. Specifically, for each $\mu \in \mathcal{P}$:

I. **Coercivity**

```math
a(v,v;\mu) \geq \alpha(\mu)\,\| v\|_V^2, \quad \forall \, v \in V
```

where $\alpha(\mu)$ is **bounded away from zero**. If there is a uniform constant $\alpha$ such that $\alpha(\mu) \geq \alpha > 0$ for all $\mu$, we say the bilinear form is **uniformly coercive**. This property guarantees the problem is not degenerate and rules out trivial solutions.

II. **Continuity**

```math
\bigl|a(u,v;\mu)\bigr| \leq \gamma(\mu)\,\| u\|_V\,\| v\|_V, \quad \forall \, u,v \in V
```

where $\gamma(\mu)$ is **finite**. A uniform bound $\gamma(\mu) \le \gamma < \infty$ across all $\mu$ indicates the bilinear form does not grow uncontrollably.

III. **Boundedness of the Load Functional**

```math
\bigl|f(v;\mu)\bigr| \leq \delta(\mu)\,\| v\|_V
```

where $\delta(\mu)$ is finite and, preferably, uniformly bounded over $\mu \in \mathcal{P}$. This ensures the right-hand side is well-defined and does not introduce unbounded forcing.

Under these assumptions, the **Lax-Milgram lemma** implies that for each $\mu\in\mathcal{P}$, there is a unique solution $u(\mu)\in V$. Moreover, this solution depends continuously on $\mu$ under certain regularity assumptions.

### Inner Products, Norms, and Parameter-Dependency

In many PDE problems, the **bilinear form** $a(\cdot;\cdot;\mu)$ can be used to define an **inner product** and **norm** on $V$. For a fixed $\mu$, we might write:

```math
(u,v)_a = a(u,v;\mu), \quad \| v\|_a = \sqrt{a(v,v;\mu)}
```

- If $\alpha(\mu)$ and $\gamma(\mu)$ are **bounded away from zero and infinity** respectively, $`\|\cdot\|_a`$ is **equivalent** to the original $`\|\cdot\|_V`$ norm.
- This equivalence is necessary for **stability analyses** and for deriving **error estimates** in both classical finite element methods and **reduced order models**.

## Purpose in CFD

Many CFD problems depend on parameters such as Reynolds number, geometry, or boundary conditions. This note formulates these problems as parameterized variational equations, defines the function spaces, and establishes well-posedness via the Lax–Milgram theorem (coercivity, continuity, boundedness). This mathematical framework is the starting point for any rigorous ROM construction.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Parameter domain $\mathcal{P}$, bilinear form $a(\cdot,\cdot;\mu)$, linear form $f(\cdot;\mu)$, trial space $X$, test space $X$ |
| **Outputs** | Well-posed variational problem: find $u(\mu) \in X$ such that $a(u,v;\mu) = f(v;\mu)$ for all $v \in X$; coercivity and continuity constants |

## Related Scripts

- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.

## Exercises

**Exercise 1.** Let $`a(u, v; \mu) = \mu\int_\Omega \nabla u \cdot \nabla v \, dx`$ on $V = H_0^1(\Omega)$ with $`\|v\|_V = \|\nabla v\|_{L^2}`$ and $\mu \in \mathcal{P} = [0.1, 10]$. Find $\alpha(\mu)$ and $\gamma(\mu)$, and the uniform constants over $\mathcal{P}$.

<details>
<summary>Answer</summary>

$`a(v, v; \mu) = \mu\|v\|_V^2`$, so $\alpha(\mu) = \mu$. By Cauchy–Schwarz, $`|a(u, v; \mu)| \le \mu\|u\|_V\|v\|_V`$, so $\gamma(\mu) = \mu$. Uniformly, $\alpha(\mu) \ge \alpha = 0.1$ and $\gamma(\mu) \le \gamma = 10$.

</details>

**Exercise 2.** On $\Omega = (0, 1)$ take $`f(v; \mu) = \int_0^1 v \, dx`$. Use the Poincaré inequality $`\|v\|_{L^2} \le \|v'\|_{L^2}/\pi`$ to show that $\delta = 1/\pi$. Derive the Lax–Milgram stability bound $`\|u(\mu)\|_V \le \delta/\alpha(\mu)`$, and compare it with the exact solution of $-\mu u'' = 1$, $u = x(1-x)/(2\mu)$, for $\mu = 0.1$.

<details>
<summary>Answer</summary>

$`|f(v)| \le \|1\|_{L^2}\|v\|_{L^2} \le \|v'\|_{L^2}/\pi`$, so $\delta = 1/\pi \approx 0.318$.

Stability: $`\alpha\|u\|_V^2 \le a(u, u; \mu) = f(u) \le \delta\|u\|_V`$, hence $`\|u\|_V \le \delta/\alpha`$. For $\mu = 0.1$ the bound is $3.18$.

Exact: $u' = (1 - 2x)/(2\mu)$ and $\int_0^1 (1 - 2x)^2 dx = 1/3$, so $`\|u'\| = 1/(2\sqrt{3}\,\mu) \approx 2.89`$. This is below the bound and fairly close to it.

</details>

**Exercise 3.** For the convection–diffusion form $`a(u, v; \mu) = \mu\int_0^1 u'v' \, dx + b\int_0^1 u'v \, dx`$ on $H_0^1(0, 1)$ with $b = 1$ and $\mu \in [0.01, 1]$, show that $\alpha(\mu) = \mu$ and $\gamma(\mu) \le \mu + |b|/\pi$. Is the problem uniformly coercive and continuous? Can $a$ define an inner product $(u, v)_a$?

<details>
<summary>Answer</summary>

$`\int_0^1 v'v \, dx = [v^2/2]_0^1 = 0`$, so $`a(v, v; \mu) = \mu\|v'\|^2`$ and $\alpha(\mu) = \mu \ge 0.01 > 0$. Continuity follows from $`|b\int u'v| \le |b|\,\|u'\|\,\|v'\|/\pi`$, giving $\gamma(\mu) \le \mu + 1/\pi \le 1.318$. The problem is uniformly coercive and continuous, so it is well posed for every $\mu$. The ratio $\gamma/\alpha$ nevertheless reaches $1 + 1/(0.01\pi) \approx 32.8$ at small $\mu$. Because $a$ is not symmetric ($\int u'v \ne \int v'u$ in general), it does not define an inner product; the energy norm of the last section requires a symmetric form.

</details>

**Exercise 4.** For the symmetric reaction–diffusion form $`a(u, v) = \int_0^1 u'v' \, dx + \sigma\int_0^1 uv \, dx`$ with $\sigma = 10$ on $H_0^1(0, 1)$, show that $`\|v\|_V \le \|v\|_a \le \sqrt{1 + \sigma/\pi^2}\,\|v\|_V`$ and evaluate the constant. Show that $v = \sin(\pi x)$ attains the upper bound.

<details>
<summary>Answer</summary>

$`\|v\|_a^2 = \|v'\|^2 + \sigma\|v\|^2`$. Since $`\sigma\|v\|^2 \ge 0`$, $`\|v\|_a \ge \|v'\| = \|v\|_V`$. By Poincaré, $`\sigma\|v\|^2 \le (\sigma/\pi^2)\|v'\|^2`$, so $`\|v\|_a^2 \le (1 + \sigma/\pi^2)\|v\|_V^2`$. The constant is $\sqrt{1 + 10/\pi^2} = \sqrt{2.0132} \approx 1.419$.

For $v = \sin(\pi x)$: $`\|v'\|^2 = \pi^2/2`$ and $`\|v\|^2 = 1/2`$, so $`\|v\|_a^2/\|v\|_V^2 = (\pi^2/2 + 5)/(\pi^2/2) = 1 + 10/\pi^2`$. The bound is attained because $\sin(\pi x)$ is the extremal function of the Poincaré inequality.

</details>

## References

- L. C. Evans, *Partial Differential Equations*, 2nd ed., American Mathematical Society, 2010.
- S. C. Brenner and L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Springer, 2008.
- A. Quarteroni, A. Manzoni and F. Negri, *Reduced Basis Methods for Partial Differential Equations: An Introduction*, Springer, 2016.
- J. S. Hesthaven, G. Rozza and B. Stamm, *Certified Reduced Basis Methods for Parametrized Partial Differential Equations*, Springer, 2016.
