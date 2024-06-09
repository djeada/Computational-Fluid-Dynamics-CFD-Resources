## Parameterized Variational Problems

In this section, we will provide an overview of parameterized variational differential equations. We assume that $\Omega \subset \mathbb{R}^d$ is a suitably regular domain with boundary $\partial \Omega$, where $d = 1, 2,$ or 3 represents the spatial dimension. We will address both scalar and vector fields, so field variables $u : \Omega \rightarrow \mathbb{R}^q$ are considered. Here, $d_s$ is the dimension of the field variable, with $q = 1$ for scalar fields and $q = d_s$ for vector fields. We also define the parts of the boundary where Dirichlet boundary conditions are imposed as $\partial \Omega_D$.

### Scalar Field Spaces

We introduce the scalar field spaces $V_i, 1 \leq i \leq d_s$:


$$ V_i = V_i(\Omega) = \{v \in H^1(\Omega), v|_{\partial \Omega_D} = 0\}, 1 \leq i \leq d_s $$


- In general, $H_0^1 (\Omega) \subset V_i (\Omega)$.
- The space where our vector-valued field variable will lie is the Cartesian vector product $V = V_1 \times \cdots \times V_{d_v}$.
- An element of $V$ is denoted as $u = (u_1, u_2, \ldots, u_{d_v})$.

### Inner Product and Norm in $V$

- $V$ is equipped with an inner product $(\cdot, \cdot)_V$.
- The induced norm is $\|u\|_V = (u,u)_V$ for $u \in V$.
- $V$ is a Hilbert space since the inner product induces the norm defined on the $H_0^1 (\Omega)$ norm.

### Parameter Domain

- The closed parameter domain is $\mathcal{P} \subset \mathbb{R}^p$.
- A typical parameter point or vector is denoted as $\mu = (\mu_1, \mu_2, \ldots, \mu_p)$.
- We define our parameterized family as $u(\mu) = \{u_1(\mu), u_2(\mu), \ldots, u_{d_v}(\mu)\} : \mathcal{P} \rightarrow V$, which denotes the field for parameter value $\mu$.

## Parametric Weak Formulation

### General Stationary Problem

- Parameterized linear forms: $f : V \times \mathcal{P} \rightarrow \mathbb{R}$ and $a : V \times \mathcal{P} \rightarrow \mathbb{R}$.
- Linearity with respect to the first variable.
- Parameterized bilinear form: $a : V \times V \times \mathcal{P} \rightarrow \mathbb{R}$, bilinear with respect to the first two variables.

The abstract formulation:
Given $\mu \in \mathcal{P}$, seek $u(\mu) \in V$ such that


$$ a(u(\mu);v;\mu) = f(v;\mu) \quad \forall v \in V $$


Evaluate $s(u) = l(\mu)$


$$ s(u) = l(u(\mu);\mu) = l(u;\mu) $$


- $s : \mathcal{P} \rightarrow \mathbb{R}$ represents the input-output relationship.
- $l$ is a linear "output" functional linking the input to the output through the field variable $u(\mu)$.

### Assumptions for Compliance Problems

1. $f(v;\mu) = f(v;\mu)$, $\forall v \in V$: The output functional and load/source functional are identical.
2. The bilinear form $a(\cdot ; \cdot;\mu)$ is symmetric for any parameter value $\mu \in \mathcal{P}$.

These conditions are satisfied in many mechanics and physics problems, e.g., material properties, geometrical parameterization.

## Inner Products, Norms, and Well-Posedness of the Parametric Weak Formulation

### Hilbert Space Norm

- The Hilbert space $V$ is equipped with an intrinsic norm $||v||_V$.
- Often, this norm is equivalent to the norm induced by the bilinear form $a$ for a fixed parameter $\mu \in \mathcal{P}$:


$$ (u, v)_V = a(u, v;\mu) \quad \forall u, v \in V $$



$$ ||v||_V = \sqrt{a(v,v;\mu)} \quad \forall v \in V $$


### Well-Posedness

- The well-posedness of the problem can be established by the Lax-Milgram theorem.
- For all parameter values $\mu \in \mathcal{P}$, assume:

#### Coercivity and Continuity of $a(\cdot;\cdot;\mu)$

- Coercive: For every $\mu \in \mathcal{P}$, there exists a positive constant $\alpha(\mu) \geq \alpha > 0$ such that


$$ a(v,v;\mu) \geq \alpha(\mu) ||v||_V^2 \quad \forall v \in V $$


- Continuous: For every $\mu \in \mathcal{P}$, there exists a finite constant $\gamma(\mu) < \infty$ such that


$$ |a(v,w;\mu)| \leq \gamma(\mu) ||v||_V ||w||_V \quad \forall v, w \in V $$


#### Continuity of $f(\cdot;\mu)$

- For every $\mu \in \mathcal{P}$, there exists a constant $\delta(\mu) \leq \delta < \infty$ such that


$$ f(v;\mu) \leq \delta(\mu) ||v||_V \quad \forall v \in V $$


### Coercivity and Continuity Constants

- Coercivity constant:


$$ \alpha(\mu) = \inf_{v \in V} \frac{a(v,v;\mu)}{||v||_V^2} $$


- Continuity constant:


$$ \gamma(\mu) = \sup_{v,w \in V} \frac{|a(v,w;\mu)|}{||v||_V ||w||_V} $$


### Energy Inner Product and Norm

- Energy inner product:


$$ (u, v)_a = a(u, v;\mu) \quad \forall v \in V $$


- Energy norm:


$$ ||v||_a = \sqrt{a(v,v;\mu)} \quad \forall v \in V $$


- These quantities are parameter-dependent and rely on the assumptions of coercivity and continuity.
