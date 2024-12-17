## Parameterized Variational Problems

In computational science and engineering, many physical and mechanical systems depend on parameters that can significantly change their behavior. Examples include varying material properties, geometrical dimensions, boundary conditions, or force terms. Our interest lies in defining and analyzing a **parameterized variational problem**, where we solve a partial differential equation (PDE) or system of PDEs for different parameter values $\mu$ from a parameter set $\mathcal{P}$.

### The Setting

**Domain and Dimension**:  

Let $\Omega \subset \mathbb{R}^d$ be a bounded, sufficiently regular domain, where $d \in \{1,2,3\}$ is the spatial dimension. The boundary $\partial \Omega$ is decomposed into subdomains, and in particular, $\partial \Omega_D \subset \partial \Omega$ denotes the portion of the boundary where Dirichlet boundary conditions are imposed.

**Field Variables**:  
We consider both scalar and vector fields. A field $u : \Omega \to \mathbb{R}^q$ may represent temperature (if $q=1$), displacement (if $q=d_s$), velocity fields in fluid flow (again $q=d_s$ for dimension $d_s$), or other physical quantities. Here $d_s$ indicates the dimension of the field variable, and $q$ matches that dimension. Thus:
- If we deal with a scalar field, $q=1$.
- If we deal with a vector field, $q=d_s$.

### Function Spaces

To pose our PDE in a variational form, we work in appropriate Hilbert spaces. For scalar problems, we consider:

$$V_i(\Omega) = \{ v \in H^1(\Omega) : v|_{\partial \Omega_D} = 0 \}, \quad 1 \leq i \leq d_s.$$

This is the space of $H^1$-functions (once differentiable and square-integrable) that vanish on the Dirichlet boundary. For a vector field $u=(u_1,\ldots,u_{d_s})$, we define:

$$V = V_1(\Omega) \times \cdots \times V_{d_s}(\Omega),$$
so that each component $u_i$ belongs to $V_i$. Since each $V_i$ is a Hilbert space, their product $V$ is also a Hilbert space under a suitable inner product $(\cdot,\cdot)_V$. The induced norm is defined by $\|u\|_V = \sqrt{(u,u)_V}$, ensuring $V$ is a normed, complete space (a Hilbert space).

### Parameter Domain

We consider a parameter vector $\mu \in \mathcal{P} \subset \mathbb{R}^p$, where $\mathcal{P}$ is a closed, bounded parameter domain. Each parameter $\mu$ could represent material parameters (e.g., Young’s modulus, conductivity), geometric parameters (e.g., shape dimensions), or boundary conditions. The solution of our problem depends on $\mu$.

We represent the parameter-dependent solution as:

$$u(\mu) = (u_1(\mu), u_2(\mu), \ldots, u_{d_s}(\mu)) \in V.$$

Thus, for every $\mu$, we solve a PDE and obtain a solution in $V$.

## Parametric Weak Formulation

We assume a parametric variational problem of the form:

$$a(u(\mu); v;\mu) = f(v;\mu) \quad \forall v \in V.$$

Here,
- $a(\cdot;\cdot;\mu) : V \times V \to \mathbb{R}$ is a parameterized bilinear form, linear and continuous in both arguments $u$ and $v$ for each fixed $\mu$.
- $f(\cdot;\mu) : V \to \mathbb{R}$ is a parameterized linear functional representing sources, loads, or forcing terms.

For each $\mu \in \mathcal{P}$, the weak formulation states: **Find $u(\mu) \in V$ such that**:

$$a(u(\mu), v;\mu) = f(v;\mu) \quad \forall v \in V.$$

Once the solution $u(\mu)$ is found, we might also be interested in outputs of interest:

$$s(\mu) = l(u(\mu);\mu),$$
where $l(\cdot;\mu): V \to \mathbb{R}$ is another linear functional capturing a physical quantity like stress intensity, flux through a boundary, or average displacement.

### Examples and Simplifications

I. **Compliance Problems**: Consider a linear elasticity problem, where the bilinear form $a(u,v;\mu)$ might represent the internal elastic energy, and $f(v;\mu)$ represents external forces. If the PDE is self-adjoint and we use symmetric bilinear forms, then $a(\cdot;\cdot;\mu)$ is symmetric for all $\mu$.

II. **Convection-Diffusion Problems**: Here, $a(u,v;\mu)$ might include both diffusive and convective terms, and $\mu$ could represent a Peclet number or conductivity parameter.

## Well-Posedness and Requirements

For the parameterized problem to admit a unique solution for each $\mu$, we rely on conditions analogous to the Lax-Milgram theorem. To ensure well-posedness, the following must hold for each $\mu \in \mathcal{P}$:

I. **Coercivity**: There exists a uniform constant $\alpha(\mu)$ (bounded away from zero) such that:

$$a(v,v;\mu) \geq \alpha(\mu) \|v\|_V^2 \quad \forall v \in V.$$

If $\alpha(\mu)\geq \alpha > 0$ for all $\mu$, we have uniform coercivity. Coercivity ensures that the bilinear form provides a sufficient "stiffness" to rule out trivial (zero) solutions only.

II. **Continuity**: There exists $\gamma(\mu) \leq \gamma < \infty$ such that:

$$|a(u,v;\mu)| \leq \gamma(\mu) \|u\|_V \|v\|_V \quad \forall u,v \in V.$$

Continuity ensures no pathological growth in the bilinear form.

III. **Boundedness of Load Functional**: There exists $\delta(\mu)\leq \delta < \infty$ such that:

$$|f(v;\mu)| \leq \delta(\mu) \|v\|_V.$$

Under these assumptions, the Lax-Milgram lemma guarantees that for each $\mu$, there is a unique solution $u(\mu)\in V$.

### Inner Products, Norms, and Parameter-Dependency

In many PDE problems, the bilinear form $a(\cdot;\cdot;\mu)$ can be used to define an inner product and norm on $V$. For a fixed $\mu$:

$$(u,v)_a = a(u,v;\mu), \quad \|v\|_a = \sqrt{a(v,v;\mu)}.$$

If $\alpha(\mu)$ and $\gamma(\mu)$ are bounded and away from zero, $(\cdot,\cdot)_a$ defines an equivalent inner product and $\|\cdot\|_a$ an equivalent norm to $\|\cdot\|_V$. These equivalences are crucial when analyzing stability and error estimates, especially in reduced order methods.

## Summary

I. **Variational Setting**: We started from a parameterized PDE problem and recast it into a weak form using appropriate function spaces $V$.

II. **Parameterization**: The solution depends on a parameter vector $\mu$. The family of solutions $\{u(\mu):\mu\in\mathcal{P}\}$ forms the solution manifold.

III. **Well-Posedness**: Under coercivity and continuity assumptions on the bilinear form $a(\cdot;\cdot;\mu)$ and boundedness of the load functional $f(\cdot;\mu)$, each problem for a given $\mu$ is well-posed, ensuring a unique solution.

IV. **Inner Products and Norms**: These assumptions allow us to define parameter-dependent inner products and norms that can simplify the analysis of stability and error.

These foundational concepts lay the groundwork for subsequent techniques like reduced basis approximations (e.g., POD or greedy algorithms) to efficiently solve for $u(\mu)$ for many parameter values. By ensuring well-posedness and understanding the structure of the parametric weak formulation, we prepare the path toward reduced order modeling and its offline-online decomposition strategy.
