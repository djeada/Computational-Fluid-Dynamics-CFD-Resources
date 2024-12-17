## Discretization Techniques

In the previous sections, we established a parameterized variational problem and introduced a suitable function space $V$ for the solution field. To solve this problem numerically, we must discretize the continuous setting. This involves replacing the infinite-dimensional space $V$ with a finite-dimensional approximation space $V_h$. By doing so, we obtain a system of algebraic equations that can be solved by standard numerical linear algebra methods.

### Construction of the Approximation Space $V_h$

**Key Idea**: To approximate $u(\mu) \in V$, we introduce a conforming finite-dimensional subspace:

$$V_h \subset V,$$
where $V_h$ has dimension $N_h$. The term "conforming" means that $V_h$ respects the boundary conditions and continuity requirements of $V$.

**Common Choices for $V_h$**:
- **Finite Element Method (FEM)**: Create a mesh (triangulation, tetrahedra, quadrilaterals, etc.) of the domain $\Omega$. On each element, choose polynomial basis functions (e.g., piecewise linear or higher-order polynomials) that form a local approximation. Assembling these local bases yields a global approximation space $V_h$.
- **Spectral Methods**: Use global polynomial expansions (e.g., Chebyshev or Legendre polynomials) to approximate the solution.
- **Other methods (e.g., higher-order finite volumes or isogeometric analysis)**: As long as the resulting space $V_h$ is a subspace of $V$, the variational framework remains valid.

The key requirement is that the discretization is derived from a variational principle. This ensures we inherit coercivity, continuity, and stability properties from the continuous problem.

### Discrete Problem Formulation

Once $V_h$ is constructed, we pick a basis $\{\phi_i\}_{i=1}^{N_h}$ for $V_h$. Any $u_h(\mu) \in V_h$ can be expressed as:

$$u_h(\mu) = \sum_{i=1}^{N_h} (u_{N_h}^\mu)_i \phi_i,$$
where $(u_{N_h}^\mu)_i \in \mathbb{R}$ are the coordinates of the discrete solution in the chosen basis.

Substitute $u_h(\mu)$ into the weak formulation:

$$a(u_h(\mu), v_h;\mu) = f(v_h;\mu) \quad \forall v_h \in V_h.$$

This results in a linear (or nonlinear) system of algebraic equations. For linear problems, the discrete problem can be represented as:

$$A_{N_h}^\mu u_{N_h}^\mu = f_{N_h}^\mu,$$
where $A_{N_h}^\mu \in \mathbb{R}^{N_h \times N_h}$ is the stiffness (or system) matrix, and $f_{N_h}^\mu \in \mathbb{R}^{N_h}$ is the load vector. Both depend on the parameter $\mu$.

### Truth Problem and High Fidelity Model

**Definition**: The resulting discrete problem is known as the **truth problem**, and $u_h(\mu)$ is called the **truth solution**. The truth solution is a high-fidelity approximation to the exact solution $u(\mu)$. As we refine the mesh or increase polynomial order, $u_h(\mu)$ converges to $u(\mu)$.

- **High Fidelity Model**: The truth model is often very expensive computationally, especially if $N_h$ is large (e.g., millions of degrees of freedom in a 3D problem). Each solve may require $\mathcal{O}(N_h^3)$ operations with standard direct solvers or $\mathcal{O}(N_h^{\alpha})$ for some $\alpha > 1$ with iterative solvers.
- **Need for Reduction**: If we must solve this problem repeatedly for many parameter values $\mu \in \mathcal{P}$, the cost becomes prohibitive. This motivates the development of Reduced Order Models (ROMs).

### Error Estimates and Galerkin Orthogonality

**Galerkin Orthogonality**: Due to the variational formulation and the choice $V_h \subset V$, the error $(u(\mu)-u_h(\mu))$ is orthogonal (with respect to $a(\cdot;\cdot;\mu)$ or $(\cdot,\cdot)_V$) to the approximation space:

$$a(u(\mu)-u_h(\mu), v_h;\mu) = 0 \quad \forall v_h \in V_h.$$

**Cea's Lemma**: This classic result gives:

$$||u(\mu)-u_h(\mu)||_V \leq \frac{\gamma(\mu)}{\alpha(\mu)} \inf_{v_h \in V_h} ||u(\mu)-v_h||_V,$$
where $\frac{\gamma(\mu)}{\alpha(\mu)}$ quantifies how well the approximation space can represent the exact solution.

This shows that the discrete solution $u_h(\mu)$ is quasi-optimal—up to a factor $\frac{\gamma(\mu)}{\alpha(\mu)}$—with respect to the best possible $V_h$-approximation of $u(\mu)$.

### Relation to Reduced Order Modeling (ROM) and POD

**Motivation for ROM**: While the high-fidelity solution $u_h(\mu)$ is accurate, it is too costly to compute for multiple parameter values. In practice, one wants a method to rapidly evaluate the solution for any $\mu \in \mathcal{P}$. 

**Idea of ROM**: Reduced order models drastically reduce the dimension of the problem:

I. **Offline Phase**: Solve the high-fidelity problem for several "training" parameter values $\{\mu_1,\ldots,\mu_{N_s}\}$. These solutions, called **snapshots**, form a snapshot set.
II. **POD or Other Basis Extraction Methods**: Use the snapshots to extract a low-dimensional subspace $V_{N_h} \subset V_h$ of dimension $N \ll N_h$ that captures most of the solution variance. The Proper Orthogonal Decomposition (POD) is a popular technique for this:
- Arrange snapshots into a matrix.
- Perform a singular value decomposition (SVD).
- Select the first $N$ modes associated with the largest singular values as the reduced basis.

III. **Reduced Basis (RB) Approximation**: Approximate:

$$u_h(\mu) \approx u_{N_h}(\mu) = \sum_{i=1}^N a_i(\mu)\xi_i,$$
where $\{\xi_i\}_{i=1}^N$ is the reduced basis extracted from POD. This replacement reduces the problem from $\mathcal{O}(N_h)$ unknowns to $\mathcal{O}(N)$ unknowns.

**Effect on Complexity**:
- The high-fidelity solve is $\mathcal{O}(N_h^3)$ typically.
- The reduced solve is $\mathcal{O}(N^3)$, where $N \ll N_h$. Thus, once the reduced basis is constructed, evaluating the solution for a new $\mu$ is much cheaper.
**Ensuring Accuracy and Stability**:
- The POD procedure ensures that the reduced basis approximates the solution manifold well. The smaller the singular values associated with omitted modes, the better the approximation from the retained modes.
- The same error estimates and Galerkin orthogonality arguments apply in the reduced space, ensuring that the reduced solution $u_{N_h}(\mu)$ is also quasi-optimal in $V_{N_h}$ with respect to the best approximation in that subspace.
