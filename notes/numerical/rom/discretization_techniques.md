## Discretization Techniques

In the previous sections, we set up a parameterized variational problem and introduced a suitable function space $V$ for the solution field. To solve this problem numerically, we must discretize the continuous setting. This involves replacing the infinite-dimensional space $V$ with a finite-dimensional approximation space $V_h$. By doing so, we obtain a system of algebraic equations that can be solved by standard numerical linear algebra methods.

### Construction of the Approximation Space $V_h$

To approximate $u(\mu) \in V$, we introduce a conforming finite-dimensional subspace:

$$V_h \subset V$$

where $V_h$ has dimension $N_h$. The term **conforming** means that $V_h$ respects the same boundary conditions and continuity requirements as $V$. This ensures that functions in $V_h$ satisfy the same necessary constraints (e.g., Dirichlet boundary conditions, inter-element continuity) as the exact solution space $V$.

**Common Choices for $V_h$**:

I. **Finite Element Method (FEM)**:  

   - **Mesh Generation**: The domain $\Omega$ is partitioned into smaller elements (e.g., intervals, triangles, tetrahedra, quadrilaterals, or hexahedra).  
   - **Local Shape Functions**: On each element, we choose polynomial basis functions (e.g., piecewise linear, quadratic, or higher-order polynomials) that form a local approximation. These basis functions typically possess desirable properties such as local support (they are nonzero only on a few elements) and continuity across element interfaces if needed.  
   - **Global Assembly**: By assembling these local shape functions element by element, we create a global basis for $V_h$. The dimension of $V_h$, denoted $N_h$, is directly related to the total number of mesh nodes (or degrees of freedom).  

II. **Spectral Methods**:  

   - **Global Polynomials**: Instead of piecewise polynomials, we use high-degree global polynomials (e.g., Chebyshev or Legendre polynomials).  
   - **Spectral Accuracy**: These methods can achieve very fast convergence (spectral or exponential) for sufficiently smooth problems. However, they can be more difficult to apply in complicated geometries and often require transformations or specialized quadratures.  

III. **Other Methods**:  

   - **Isogeometric Analysis (IGA)** uses spline or NURBS-based functions that are inherited from CAD representations, offering smooth and accurate geometry representation.  
   - **Higher-Order Finite Volumes** or **Discontinuous Galerkin (DG)** methods can also be formulated in a variational (weak) setting, as long as the resulting discrete space is a subspace of (or at least compatible with) $V$.  
   - The main requirement is that the discretization must be derived from the same variational principle, preserving coercivity, continuity, and stability properties of the continuous problem.
**Importance of Conformity and Continuity**:  

- Conforming approximations make sure that boundary conditions are naturally embedded in the discrete space.  
- Non-conforming or discontinuous methods require additional penalty or stabilization terms to make sure consistency and convergence.

### Discrete Problem Formulation

Once $V_h$ is constructed, we pick a basis $\{\phi_i\}_{i=1}^{N_h}$ for $V_h$. Any $u_h(\mu) \in V_h$ can then be written as:

$$u_h(\mu) = \sum_{i=1}^{N_h} \bigl(u_{N_h}^\mu\bigr)_i \, \phi_i$$

where $\bigl(u_{N_h}^\mu\bigr)_i \in \mathbb{R}$ are the unknown coordinates (degrees of freedom) for the discrete solution in the chosen basis.

#### Substituting into the Weak Formulation

Substituting $u_h(\mu)$ into the weak formulation

$$a\bigl(u_h(\mu), v_h;\mu\bigr) = f\bigl(v_h;\mu\bigr) 
\quad 
\forall v_h \in V_h$$

yields a set of algebraic equations. Because $v_h \in V_h$ is also spanned by $\{\phi_i\}$, we can test the equation against each basis function $\phi_j$. This leads to

$$a\Bigl(\sum_{i=1}^{N_h} \bigl(u_{N_h}^\mu\bigr)_i \phi_i, \phi_j;\mu\Bigr) 
= f\bigl(\phi_j;\mu\bigr),
\quad 
j = 1, 2, \ldots, N_h$$

By linearity (assuming a linear PDE for simplicity), we can write

$$\sum_{i=1}^{N_h} \bigl(u_{N_h}^\mu\bigr)_i \, a(\phi_i, \phi_j;\mu) 
= f(\phi_j;\mu)$$

Hence we obtain the matrix-vector system

$$A_{N_h}^\mu \, u_{N_h}^\mu = f_{N_h}^\mu$$

where

- $\displaystyle \bigl(A_{N_h}^\mu\bigr)_{ji} = a(\phi_i, \phi_j;\mu)$,
- $\displaystyle \bigl(f_{N_h}^\mu\bigr)_j = f(\phi_j;\mu)$,
- $A_{N_h}^\mu \in \mathbb{R}^{N_h \times N_h}$ and $f_{N_h}^\mu \in \mathbb{R}^{N_h}$.
In practice, $A_{N_h}^\mu$ is often called the **stiffness matrix** (or system matrix), and $f_{N_h}^\mu$ is the **load vector**. Both may depend on the parameter $\mu$. For nonlinear problems, the situation is similar except that $A_{N_h}^\mu$ and $f_{N_h}^\mu$ will depend nonlinearly on the solution itself, requiring iterative solvers (e.g., Newton’s method).

### Truth Problem and High Fidelity Model

**Definition**: The resulting discrete problem

$$\text{Find } u_h(\mu) \in V_h \text{ such that } a\bigl(u_h(\mu), v_h;\mu\bigr) = f\bigl(v_h;\mu\bigr), 
\quad \forall v_h \in V_h$$

is often referred to as the **truth problem**, and $u_h(\mu)$ is called the **truth solution**. This discrete solution is considered a **high-fidelity** approximation to the exact solution $u(\mu)$ because the space $V_h$ is typically chosen to be large and rich enough to capture most solution features with acceptable accuracy.

- **High Fidelity Model**:  
  - For 2D or 3D problems with fine meshes or higher-order elements, $N_h$ can be very large (ranging into the millions of degrees of freedom).  
  - Solving one instance of $A_{N_h}^\mu \, u_{N_h}^\mu = f_{N_h}^\mu$ can cost on the order of $\mathcal{O}(N_h^3)$ operations with direct solvers, or $\mathcal{O}(N_h^\alpha)$ with iterative solvers (where $\alpha$ is often between 1 and 2, depending on the method and preconditioning strategy).
- **Need for Reduction**:  
  - If we need to solve this problem repeatedly for many parameter values $\mu \in \mathcal{P}$ (e.g., for design optimization, real-time simulation, or uncertainty quantification), the cost becomes prohibitive.  
  - **Reduced Order Modeling (ROM)** or **Model Order Reduction (MOR)** techniques aim to approximate $u_h(\mu)$ in a much smaller (reduced) subspace while retaining acceptable accuracy, thus drastically reducing the computational cost for repeated solves.

### Error Estimates and Galerkin Orthogonality

The rigorous foundations of the Finite Element Method (and other Galerkin-type methods) provide valuable error estimates and guarantee stability under mild assumptions.

#### Galerkin Orthogonality

By construction, since $V_h \subset V$, the discrete solution $u_h(\mu)$ satisfies the same weak form but restricted to $V_h$. This leads to the **Galerkin orthogonality** property:

$$a\bigl(u(\mu) - u_h(\mu), v_h;\mu\bigr) = 0 
\quad \forall v_h \in V_h$$

In simple terms, the error $e_h(\mu) = u(\mu) - u_h(\mu)$ is orthogonal (with respect to the bilinear form $a(\cdot,\cdot;\mu)$ or an associated inner product $(\cdot,\cdot)_V$) to the entire discrete space $V_h$. This is the key property that underpins the stability and convergence of Galerkin methods.

#### Cea’s Lemma

A classical result in the analysis of Galerkin methods is **Cea’s lemma**, which states that, for a coercive problem,

$$\|u(\mu) - u_h(\mu)\|_V 
\leq 
\frac{\gamma(\mu)}{\alpha(\mu)} \, \inf_{v_h \in V_h} \|u(\mu) - v_h\|_V$$

where

- $\alpha(\mu)$ is the coercivity constant of the bilinear form $a(\cdot,\cdot;\mu)$,  
- $\gamma(\mu)$ is the continuity constant of the bilinear form,  
- $\| \cdot \|_V$ denotes the norm on $V$.
This shows that $u_h(\mu)$ is **quasi-optimal** in $V_h$: up to the constant factor $\frac{\gamma(\mu)}{\alpha(\mu)}$, it is as good an approximation to $u(\mu)$ as you can get within the finite-dimensional space $V_h$. 

**Interpretation**:  

- The term $\inf_{v_h \in V_h} \|u(\mu) - v_h\|_V$ reflects the best possible approximation error if we could pick the ideal function in $V_h$.  
- The factor $\frac{\gamma(\mu)}{\alpha(\mu)}$ comes from the properties of the bilinear form (continuity and coercivity). A well-conditioned problem has $\gamma(\mu)/\alpha(\mu)$ close to 1, making the Galerkin solution nearly the best approximation in $V_h$.
These results form the theoretical backbone of why Galerkin discretizations (like FEM) are reliable and converge systematically as $V_h$ is enriched (e.g., by refining the mesh or increasing the polynomial order).

### Relation to Reduced Order Modeling (ROM) and POD

In many practical problems, especially when dealing with large parameter spaces, the **high-fidelity** solution $u_h(\mu)$ is both accurate and extremely costly to compute repeatedly for different values of the parameter $\mu$. This motivates the development of **Reduced Order Models (ROMs)**, which aim to preserve the accuracy of the high-fidelity model while substantially cutting down the computational time for new parameter queries.

#### Motivation for ROM

- **High-Fidelity Cost**: Solving the large-scale problem with $N_h$ degrees of freedom can take $\mathcal{O}(N_h^3)$ operations for direct solvers, or at least $\mathcal{O}(N_h^\alpha)$ for iterative solvers (with $\alpha > 1$).  
- **Repeated Parameter Queries**: Many engineering and scientific applications (e.g., real-time control, design optimization, uncertainty quantification) require evaluating the solution for multiple parameter values $\mu$. Doing so with the full high-fidelity model becomes prohibitively expensive.
Hence, **Reduced Order Modeling** offers a pathway to drastically speed up parameterized simulations by constructing and utilizing a much smaller, yet representative, subspace of the original high-fidelity space $V_h$.

#### Idea of ROM

A typical ROM workflow is split into two main phases: an **offline** phase and an **online** phase.

I. **Offline Phase**  

   - **Snapshot Generation**: Solve the high-fidelity problem $u_h(\mu)$ for several "training" parameter values $\{\mu_1,\ldots,\mu_{N_s}\}$. This set of solutions is referred to as **snapshots**.  
   - **Snapshot Set**: Collect the snapshots in a data structure (e.g., a matrix whose columns are solutions in vectorized form).  
   - This phase involves the majority of the computational cost because each snapshot is a large-scale finite element (or other method) solve.

II. **Basis Extraction (e.g., via POD)**  

   - **Proper Orthogonal Decomposition (POD)**:  
     - Arrange the snapshot solutions into a matrix $S$ (each snapshot is one column).  
     - Perform a **Singular Value Decomposition (SVD)** of $S$, obtaining singular values $\sigma_1 \ge \sigma_2 \ge \cdots$ and corresponding orthonormal singular vectors.  
     - **Truncation**: Choose the first $N$ singular vectors associated with the largest singular values. These vectors $\{\xi_i\}_{i=1}^N$ form the **reduced basis**.  
   - **Rationale**: The SVD identifies directions in which the snapshots vary the most. By retaining only the leading singular vectors, we keep the subspace that captures the bulk of the solution’s energy or variance.

III. **Online Phase: Reduced Basis (RB) Approximation**  

   - **Approximate Solution**: For a new parameter $\mu$, approximate the solution in the low-dimensional subspace spanned by the POD modes:  
     $$u_{N_h}(\mu) = \sum_{i=1}^N a_i(\mu)\,\xi_i$$  
     where the vectors $\xi_i \in V_h$ are the reduced basis vectors, and $a_i(\mu)$ are the new unknowns (much fewer in number than $N_h$).  

   - **Reduced Problem**: By restricting the problem to this reduced subspace $V_{N_h} = \text{span}\{\xi_1,\dots,\xi_N\}$, one obtains a system of $\mathcal{O}(N)$ unknowns instead of $\mathcal{O}(N_h)$. Solving for $a_i(\mu)$ is thus much cheaper computationally.

#### Effect on Complexity

- **High-Fidelity Solve**: Typically $\mathcal{O}(N_h^3)$ per parameter instance (for direct methods).  
- **Reduced Solve**: Approximately $\mathcal{O}(N^3)$, where $N \ll N_h$.  
Since $N$ is chosen based on the rapid decay of the singular values (representing the solution’s main features), the dimension of the reduced subspace is significantly smaller than $N_h$, often by several orders of magnitude. Therefore, once the reduced basis is constructed in the offline phase, **online** evaluations of the solution for new parameters $\mu$ are dramatically accelerated.

#### Ensuring Accuracy and Stability

I. **Quality of the Reduced Basis**  

   - The POD procedure systematically identifies the directions of maximum variance in the snapshot set. If the singular values decay quickly, the solution manifold in $V_h$ is well-approximated by a subspace of small dimension $N$. This leads to accurate reduced solutions.  
   - In practice, the user chooses $N$ such that the ratio of retained singular values to the total energy meets a desired tolerance (e.g., $\sum_{i=1}^N \sigma_i^2 / \sum_{j=1}^{N_s} \sigma_j^2 \ge 1 - \epsilon$).

II. **Quasi-Optimality**  

   - The same Galerkin orthogonality arguments used in the full finite element analysis can be applied to the reduced problem, provided the reduced basis method maintains a variational structure.  
   - If the reduced basis space $V_{N_h} \subset V_h$ (and hence $V_{N_h} \subset V$), then an analogous version of Cea’s lemma ensures that the reduced solution $u_{N_h}(\mu)$ is quasi-optimal within $V_{N_h}$.  
   - The factor $\frac{\gamma(\mu)}{\alpha(\mu)}$ in the error estimate still governs the stability of the approximation, just as in the high-fidelity problem.

III. **Offline/Online Efficiency**  

   - While the offline phase can be expensive (because it involves generating snapshots via high-fidelity solves), the cost is paid only once.  
   - In the online phase, the **reduced** system is solved for each new $\mu$ with very low computational effort, making real-time or rapid parameter sweeps feasible.

