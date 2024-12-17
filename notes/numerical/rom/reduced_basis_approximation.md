## Solution Manifold and Reduced Basis Approximation

In computational engineering and sciences, it is common to face parameterized problems that must be solved repeatedly for varying parameter values (e.g., material properties, boundary conditions, geometrical features). Such tasks become computationally expensive if each parameter variation requires a full high-fidelity simulation. Reduced order methods (ROMs) provide a way to alleviate this cost by building a low-dimensional approximation space—often called a "reduced basis"—that accurately captures the essential dynamics of the problem’s *solution manifold*. Once constructed, this reduced space allows rapid evaluation of the solution for new parameter values at a fraction of the original computational cost.

### Solution Manifold

**Definition**: Consider a parameterized PDE problem that depends on a parameter $\mu$ drawn from a parameter set $\mathcal{P}$. For each $\mu \in \mathcal{P}$, let $u(\mu)$ be the exact solution to the PDE. The set of all such solutions as $\mu$ varies is called the **solution manifold**:

$$\mathcal{M} = \{ u(\mu) : \mu \in \mathcal{P} \} \subset V,$$
where $V$ is a suitable (often infinite-dimensional) function space, such as a Hilbert space of continuous or differentiable functions.

The dimension of $\mathcal{M}$ can be quite large. Indeed, if the PDE is discretized by finite elements or finite volumes, resulting in $N_h$ degrees of freedom, $\mathcal{M}$ will live in a very high-dimensional subspace of $\mathbb{R}^{N_h}$. The goal of ROM is to identify a low-dimensional subspace of $V$ (or equivalently of $\mathbb{R}^{N_h}$) that well-approximates $\mathcal{M}$.

### Parameterized Problem and Exact Solution

Suppose we have a parameterized bilinear form $a(\cdot;\cdot;\mu)$ and a linear functional $f(\cdot;\mu)$. The exact problem can be stated as:

$$a(u(\mu), v;\mu) = f(v;\mu) \quad \forall v \in V,$$
with $u(\mu) \in V$ as the exact solution that depends smoothly on the parameter $\mu$. However, solving this problem exactly is often intractable, so we introduce a high-fidelity discretization step.

### Finite Element/Volume Discretization: The Truth Problem

Since we cannot solve infinite-dimensional problems exactly, we resort to a finite dimension $N_h$ discretization. For instance, a finite element or finite volume approximation $V_h \subset V$ is introduced. The "truth problem" then is:

$$a(u_h(\mu), v_h;\mu) = f(v_h;\mu) \quad \forall v_h \in V_h,$$
where $u_h(\mu) \in V_h$ is the high-fidelity (truth) solution. The dimension $N_h$ of $V_h$ is large, and each solution at a new parameter $\mu$ may be very expensive to compute.

### Discrete Solution Manifold

The discrete solution manifold is:

$$\mathcal{M}_{d_s} = \{u_h(\mu) : \mu \in \mathcal{P}\} \subset V_h.$$

This manifold can have a very complicated structure, but crucially, many PDE problems exhibit solutions that live near a low-dimensional manifold due to underlying physics and parameter dependencies. Reduced order methods exploit this property.

### Reduced Basis Method: Outline

**Key Idea**: If the manifold $\mathcal{M}_{d_s}$ is (approximately) low-dimensional, we can find a set of $N$ basis functions $\{\xi_1,\ldots,\xi_N\}$ (with $N \ll N_h$) such that any solution $u_h(\mu)$ can be approximated as:

$$u_{N_h}(\mu) = \sum_{i=1}^N a_i(\mu) \xi_i.$$

Here, $\{\xi_i\}_{i=1}^N$ is called a **reduced basis**, and $\mathcal{V}_{N_h} = \text{span}\{\xi_1,\ldots,\xi_N\}$ is the reduced subspace of $V_h$. The aim is to approximate $u_h(\mu)$ by $u_{N_h}(\mu) \in \mathcal{V}_{N_h}$ so that computations depend only on $N$, not on the large dimension $N_h$.

### The Offline-Online Decomposition

ROM typically involves two distinct computational phases:

I. **Offline Phase**:
- Solve the high-fidelity problem (the "truth" problem) for several parameter values $\{\mu_1,\ldots,\mu_{N_s}\}$. This might require $N_s$ high-fidelity solves, each with complexity proportional to $N_h$.
- From these collected "snapshots" $\{u_h(\mu_j)\}$, use the POD (Proper Orthogonal Decomposition) or another technique to extract a low-dimensional basis that best approximates all solutions in some training set.
- The offline phase is computationally expensive because it involves many full-order solves. However, it is done only once.
II. **Online Phase**:
- For a new parameter $\mu$, approximate the solution $u(\mu) \approx u_{N_h}(\mu)$ by solving a much smaller $N \times N$ system derived from the reduced basis approximation.
- The cost of the online solution no longer depends on $N_h$, only on $N$ and the complexity of the parameter dependence. Thus, evaluations become extremely fast.

### POD for Reduced Basis Construction

POD is a method to extract the most energetic modes from a set of snapshots:

I. Suppose we have snapshot solutions $\{u_h(\mu_j)\}_{j=1}^{N_s}$.

II. Form a snapshot matrix whose columns are these solutions.

III. Compute the singular value decomposition (SVD) or eigenvalue decomposition of a correlation matrix derived from the snapshots.

IV. Select the first $N$ modes associated with the largest eigenvalues (singular values). These modes form the reduced basis.

The POD basis $\{\xi_j\}$ is chosen to minimize the average approximation error of the snapshots. With a good choice of $N$ (often small), the reduced space can achieve good accuracy.

### Reduced Basis Approximation

Once the reduced basis $\{\xi_j\}_{j=1}^N$ is constructed, we solve the reduced problem:

$$a(u_{N_h}(\mu), v_{N_h};\mu) = f(v_{N_h};\mu) \quad \forall v_{N_h} \in \mathcal{V}_{N_h}.$$

Since $\mathcal{V}_{N_h}$ is spanned by $\{\xi_1,\ldots,\xi_N\}$, we expand:

$$u_{N_h}(\mu) = \sum_{n=1}^N a_n(\mu)\xi_n.$$

Inserting this into the PDE yields a small $N \times N$ linear (or nonlinear) system for the coefficients $a_n(\mu)$.

### Offline-Precomputation of Operators

To accelerate the online phase, one typically precomputes operators that appear in the reduced problem:

- Represent the large stiffness or mass matrices (like $A_{N_h}$ or $f_{N_h}$) in the reduced basis by precomputing projections:

$$A_{N_h}^r = B^T A_{N_h} B, \quad f_{N_h}^r = B^T f_{N_h},$$
where $B$ is the matrix whose columns are the reduced basis vectors expressed in the high-dimensional basis $\{\phi_m\}$ of $V_h$.

This step is done offline and stored. Online, you only need to form parameter-dependent combinations efficiently.

### Evaluating Quantities of Interest

If you’re interested in a certain output functional $s(\mu) = l(u(\mu);\mu)$, you can approximate it via:

$$s_{N_h}(\mu) = l(u_{N_h}(\mu);\mu).$$

Since $u_{N_h}(\mu)$ is low-dimensional, computing $s_{N_h}(\mu)$ is also cheap.

### Approximation Error

The final reduced order approximation $u_{N_h}(\mu)$ has two error components:

$$||u(\mu) - u_{N_h}(\mu)||_V \leq ||u(\mu) - u_h(\mu)||_V + ||u_h(\mu) - u_{N_h}(\mu)||_V.$$

- The first term $||u(\mu)-u_h(\mu)||_V$ is the high-fidelity discretization error, which can be made arbitrarily small by refining the mesh or increasing polynomial order in the truth approximation.
- The second term $||u_h(\mu)-u_{N_h}(\mu)||_V$ is the ROM truncation error, controlled by how well the reduced basis can represent the solution manifold.

By increasing $N$, we can reduce this truncation error until a desired accuracy is attained (to a point, depending on the complexity of $\mathcal{M}$).
