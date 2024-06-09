## Discretization Techniques

In this section, we introduce discrete approximations of the parametric weak formulation. We consider conforming approximations, where there exists a space $V_h$ such that $V_h \subset V$. The approximating solution is sought in $V_h$. This conforming nature of $V_h$ is crucial for our reduction treatment.

### Construction of Approximation Space

- The approximation space $V_h$ can be constructed using various methods, such as:
  - Standard finite element method (FEM) based on a triangulation and piece-wise linear basis functions.
  - Spectral methods.
  - Higher-order finite elements.
- The key requirement is that the formulation must be based on a variational approach.

### Discrete Problem Formulation

- Let the dimension of $V_h$ be $N_h$.
- Equip $V_h$ with a basis $\{\phi_i\}_{i=1}^{N_h}$.
- For each $\mu \in \mathcal{P}$ and $u_h(\mu) \in V_h$, the discrete problem is formulated as:


$$ a(u_h(\mu), v_h; \mu) = f(v_h;\mu) \quad \forall v_h \in V_h $$


- Evaluate the output:


$$ s(u_h) = l(u_h(\mu); \mu) $$


### Truth Problem and High Fidelity Model

- The discrete problem is known as the truth problem, and its solution is called the truth solution.
- The truth solution is computed with high accuracy but can be computationally expensive due to the large degrees of freedom in $V_h$.
- The high fidelity model ensures the error $|u(\mu) - u_h(\mu)|_V$ is minimized.

### Galerkin Orthogonality and Cea's Lemma

- Thanks to the coercivity and continuity of the bilinear form, and the conformity of the approximation space, we have Galerkin orthogonality:


$$ a(u - u_h, v_h; \mu) = 0 \quad \forall v_h \in V_h $$


- Applying Cea's Lemma:


$$ ||u(\mu) - u_h(\mu)||_V \leq \frac{\gamma}{\alpha} \inf_{v_h \in V_h} ||u(\mu) - v_h||_V $$


- Using the triangle inequality:


$$ ||u_h(\mu) - u_{n_h}(\mu)||_V \leq a(v_h, u_h; \mu - u_h(\mu); \mu) = a(u(\mu) - u_h(\mu); \mu) \leq \gamma||u(\mu) - u_h(\mu)||_V $$


- Proven result:


$$ ||u(\mu) - u_h(\mu)||_V \leq (1 + \frac{\gamma}{\alpha}) \inf_{v_h \in V_h} ||u(\mu) - v_h||_V $$


- The approximation error $|u(\mu) - u_{N_h}(\mu)|_V$ is closely related to the best approximation of $u(\mu)$ in $V_h$ through the constants $\frac{\gamma}{\alpha}(\mu)$.

### Truth Solver

- Denote the stiffness matrix and right-hand side of the truth problem 4.8 by $A_{N_h}^\mu \in \mathbb{R}^{N_h \times N_h}$ and $f_{N_h}^\mu \in \mathbb{R}^{N_h}$, respectively.
- Matrix associated with the inner product $(\cdot , \cdot )_V$ of $V_h$ is $M_{d_s} \in \mathbb{R}^{N_h \times N_h}$:


$$ (M_{d_s})_{ij} = (\phi_i , \phi_j)_V $$



$$ (A_{N_h}^\mu)_{ij} = a(\phi_i, \phi_j;\mu) $$



$$ (f_{N_h}^\mu)_i = f(\phi_i;\mu) $$


- For each $\mu \in \mathcal{P}$, find $u_{N_h}^\mu \in \mathbb{R}^{N_h}$ such that:


$$ A_{N_h}^\mu u_{N_h}^\mu = f_{N_h}^\mu $$


- The size of the unknown vector is $N_h$ and the size of the stiffness matrix is $N_h \times N_h$.
- The computational cost depends on the properties of the stiffness matrix and the method used to invert the linear system, typically $\mathcal{O}(N_h^3)$.
