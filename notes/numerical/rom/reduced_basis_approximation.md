## Solution Manifold and Reduced Basis Approximation

In computational engineering and sciences, it is common to face parameterized problems that must be solved repeatedly for varying parameter values (e.g., material properties, boundary conditions, geometrical features). Such tasks become computationally expensive if each parameter variation requires a full high-fidelity simulation. **Reduced order methods (ROMs)** provide a way to alleviate this cost by building a low-dimensional approximation space—often called a “reduced basis”—that accurately captures the necessary dynamics of the **solution manifold**. Once constructed, this reduced space allows **rapid evaluation** of the solution for new parameter values at a fraction of the original computational cost.

### Solution Manifold

**Definition**  
Consider a parameterized PDE problem that depends on a parameter $\mu$ drawn from a parameter set $\mathcal{P}$. For each $\mu \in \mathcal{P}$, let $u(\mu)$ be the exact solution to the PDE. The set of all such solutions, as $\mu$ varies, is called the **solution manifold**:

$$\mathcal{M} = \{\,u(\mu) : \mu \in \mathcal{P}\} \subset V$$

where $V$ is a suitable (often infinite-dimensional) function space—such as a Hilbert or Banach space of continuous or differentiable functions—depending on the PDE’s regularity requirements.

- **Intuition**: This manifold $\mathcal{M}$ captures all possible “shapes” of solutions in response to different parameter choices ($\mu$ could include boundary conditions, material properties, geometry, etc.).
- **High Dimensionality**: If we discretize the PDE with $N_h$ degrees of freedom, $u(\mu)$ becomes a vector in $\mathbb{R}^{N_h}$. Hence, $\mathcal{M}$ lives in a (potentially very large) subspace of $\mathbb{R}^{N_h}$.
- **Low-Dimensional Structure**: Many PDEs exhibit solutions that, despite appearing high-dimensional, **effectively** lie near a much lower-dimensional manifold. ROMs exploit this property to significantly reduce computational costs.

### Parameterized Problem and Exact Solution

We assume a parameter-dependent variational formulation:

$$
a\bigl(u(\mu), v; \mu\bigr) = f\bigl(v; \mu\bigr), \quad \forall v \in V
$$

where  

- $a(\cdot,\cdot;\mu)$ is a **bilinear (or nonlinear) form** that depends on the parameter $\mu$,  
- $f(\cdot;\mu)$ is a **linear functional** (or more generally, a nonlinear functional) encoding source terms or boundary data,  
- $u(\mu) \in V$ is the parameter-dependent **exact solution**.
In many practical applications, solving for $u(\mu)$ in an infinite-dimensional space $V$ directly is not feasible, prompting a finite-dimensional **discretization**.

### Finite Element/Volume Discretization: The Truth Problem

To handle the infinite-dimensional problem, we introduce a high-fidelity **discretization** of dimension $N_h$. For instance, we may use:

I. **Finite Element Method (FEM)**: Construct a mesh of the domain, choose polynomial shape functions, and assemble global matrices.  

II. **Finite Volume Method (FVM)**: Subdivide the domain into control volumes and enforce integral conservation laws at each cell.  

Let $V_h \subset V$ be this finite-dimensional approximation space of dimension $N_h$. The **truth problem** becomes:

$$
a\bigl(u_h(\mu), v_h; \mu\bigr) = f\bigl(v_h; \mu\bigr), \quad \forall v_h \in V_h
$$

where $u_h(\mu) \in V_h$ is the **high-fidelity (truth) solution**.  

- **High Dimensionality**: In realistic 3D problems, $N_h$ can be in the millions.  
- **Computational Cost**: Each new $\mu$ requires solving a large linear or nonlinear system. This can be extremely expensive if one needs many parameter evaluations (e.g., optimization, real-time control, uncertainty quantification).

### Discrete Solution Manifold

Correspondingly, the set of all truth solutions lives in $V_h$:

$$
\mathcal{M}_{d_s} = \{ u_h(\mu) : \mu \in \mathcal{P} \} \subset V_h
$$

- **Potentially Complicated Geometry**: $\mathcal{M}_{d_s}$ may be curved or nonlinear in the high-dimensional space $V_h$.  
- **Approximate Low Rank**: Often, $\mathcal{M}_{d_s}$ can be approximated well by a low-dimensional subspace, thanks to the physical nature of the PDE or correlations in parameter variations.

### Reduced Basis Method: Outline

If $\mathcal{M}_{d_s}$ is (approximately) of low dimension, we can **find or construct** a set of $N$ basis functions $\{\xi_1, \ldots, \xi_N\}$ with $N \ll N_h$ such that any truth solution $u_h(\mu)$ can be approximated by:

$$
u_{N_h}(\mu) = \sum_{i=1}^N a_i(\mu) \, \xi_i
$$

where:  

- $\{\xi_i\}$ is called the **reduced basis (RB)**, and  
- $\mathcal{V}_{N_h} = \text{span}\{\xi_1,\ldots,\xi_N\} \subset V_h$ is the corresponding **reduced space**.

Once we have $\mathcal{V}_{N_h}$, we **project** the PDE onto this small subspace, flexible an $N \times N$ system for the coefficients $\{a_i(\mu)\}$. The computational cost then **scales with** $N$, not the large $N_h$.

### The Offline-Online Decomposition

The reduced basis approach typically follows a **two-phase** methodology:

I. **Offline Phase**  

   - **High-Fidelity Sampling**: Select a set of “training” parameters $\{\mu_1, \ldots, \mu_{N_s}\}$.  
   - **Solve** the truth problem for each $\mu_j$ to obtain snapshots $u_h(\mu_j)$. This is computationally expensive but done only once.  
   - **Basis Construction**: Use techniques such as **POD** (Proper Orthogonal Decomposition) to extract the low-dimensional subspace from the snapshot set.  
   - **Precomputation**: Compute data structures (reduced matrices, vectors) necessary for fast evaluation in the online phase.  

II. **Online Phase**  

   - For a **new** parameter $\mu\not\in\{\mu_j\}$, **solve** the much smaller reduced system in dimension $N$.  
   - Quickly obtain $u_{N_h}(\mu)$ as $\sum_{i=1}^N a_i(\mu)\,\xi_i$.  
   - Achieve speedups of orders of magnitude if $N$ is small and if the parameter dependency is **affine** or can be efficiently handled.
**Remark**: The offline phase can be expensive, but its cost is amortized over many online queries.

### POD for Reduced Basis Construction

A common method to build the reduced basis from snapshots is **Proper Orthogonal Decomposition (POD)**:

I. **Snapshot Matrix**  

   - Suppose we have $N_s$ snapshots $\{u_h(\mu_j)\}_{j=1}^{N_s}$. Each $u_h(\mu_j)$ is a vector in $\mathbb{R}^{N_h}$.  
   - Form a snapshot matrix $\mathbf{U} \in \mathbb{R}^{N_h \times N_s}$, where columns are these snapshots (possibly after removing mean if desired).

II. **Correlation Matrix / SVD**  

   - Compute the correlation matrix $\mathbf{C} = \frac{1}{N_s}\,\mathbf{U}^\top \mathbf{U}$, or directly apply an **SVD** to $\mathbf{U}$.  
   - The singular values $\sigma_1 \geq \sigma_2 \geq \cdots$ indicate the **energy** captured by each mode.

III. **POD Modes**  

   - The POD modes (or left singular vectors) corresponding to the largest singular values form an **orthonormal basis** $\{\xi_1,\ldots,\xi_N\}$.  
   - Truncating at $N$ modes captures the bulk of the energy (variance) in the snapshot set.

IV. **Choosing $N$**  

   - Typically, choose $N$ so that $\sum_{i=1}^N \sigma_i^2$ is a high percentage (e.g., $> 99\%$) of $\sum_{i=1}^{N_s} \sigma_i^2$.  
   - The reduced space dimension $N$ is often **orders of magnitude** smaller than $N_h$.

### Reduced Basis Approximation

With the reduced basis $\{\xi_1, \ldots, \xi_N\}$ in hand, we seek:

$$
u_{N_h}(\mu) = \sum_{n=1}^N a_n(\mu) \, \xi_n
$$

as an approximation of the truth solution $u_h(\mu)$. We enforce a **Galerkin** (or Petrov–Galerkin) condition in the subspace $\mathcal{V}_{N_h}$:

$$
a\bigl(u_{N_h}(\mu), v_{N_h}; \mu\bigr) = f\bigl(v_{N_h}; \mu\bigr), \quad \forall v_{N_h} \in \mathcal{V}_{N_h}
$$

This gives a **small** system of $N$ equations in the unknown coefficients $\{a_n(\mu)\}$. For linear PDEs, this is an $N \times N$ linear system; for nonlinear PDEs, it might require iterative solvers but still in dimension $N$.

### Offline-Precomputation of Operators

**Efficiency** in the online phase hinges on **precomputing** key operators once and reusing them. For example, if the high-fidelity discretization yields matrices $\mathbf{A}(\mu)$, $\mathbf{F}(\mu)$, then in the reduced space we only need:

$$
\mathbf{A}_r(\mu) = \mathbf{Z}^\top \mathbf{A}(\mu) \mathbf{Z}, \quad \mathbf{F}_r(\mu) = \mathbf{Z}^\top \mathbf{F}(\mu)
$$

where $\mathbf{Z}$ is the matrix whose columns are the **discrete** reduced basis vectors. In an **affine** parameter dependence scenario,

$$\mathbf{A}(\mu) 
=
\sum_{q=1}^{Q} \Theta_q(\mu)\,\mathbf{A}_q$$

these can be stored and combined quickly for each new $\mu$ to yield $\mathbf{A}_r(\mu)$. This strategy is key to achieving fast online solves.

### Evaluating Quantities of Interest

Often, we do not just need the entire field $u(\mu)$ but specific “outputs”:

$$s(\mu) 
=
l\bigl(u(\mu);\mu\bigr)$$

which might represent integrated stresses, fluxes, or design functionals. In the reduced setting,

$$s_{N_h}(\mu)
=
l\bigl(u_{N_h}(\mu);\mu\bigr)$$

and evaluating $s_{N_h}(\mu)$ is typically very cheap once $u_{N_h}(\mu)$ is known. Moreover, one can precompute certain vector or matrix forms of $l$ for fast online evaluation, similar to how $\mathbf{A}_r$ and $\mathbf{F}_r$ are precomputed.

### Approximation Error

The final reduced order solution $u_{N_h}(\mu)$ differs from the exact infinite-dimensional solution $u(\mu)$. We can decompose this error as:

$$
\|u(\mu) - u_{N_h}(\mu)\|_V
\leq
\underbrace{\|u(\mu) - u_h(\mu)\|_V}_{\text{Discretization Error}}
+
\underbrace{\|u_h(\mu) - u_{N_h}(\mu)\|_V}_{\text{ROM Truncation Error}}
$$

I. **Discretization Error**: The difference $\|u(\mu) - u_h(\mu)\|_V$ can be controlled by mesh refinement or higher-order elements in the truth model.  

II. **ROM Truncation Error**: The difference $\|u_h(\mu) - u_{N_h}(\mu)\|_V$ depends on how well $\{\xi_i\}$ captures the solution manifold. Increasing $N$ typically decreases this error.

**Goal**: Choose $N$ large enough to meet accuracy requirements but small enough to yield significant computational gains.

