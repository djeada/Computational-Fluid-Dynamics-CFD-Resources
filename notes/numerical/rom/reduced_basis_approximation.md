## Solution Manifold and Reduced Basis Approximation

In this section, we introduce reduced order methods aimed at tackling computationally expensive problems involving parameters. We will focus on the proper orthogonal decomposition (POD) method to study our high-order problem.

### Phases in Reduced Order Methods

- **Offline Phase**:
  - Explore the solution manifold.
  - Construct a reduced basis that approximates any member of the solution manifold.
  - Computationally expensive due to solving $N$ truth problems with $N_h$ degrees of freedom.
  - Result: $N$-dimensional reduced basis space.
- **Online Phase**:
  - Perform Galerkin projection using the bilinear form $a(\cdot;\cdot;\mu)$ with parameter $\mu \in \mathcal{P}$.
  - Explore the parameter space at a substantially reduced computational cost, ideally independent of $N_h$.

### Exact Solution of the Parameterized Problem

We aim to obtain the solution of the parameterized exact problem:


$$ a(u(\mu), v;\mu) = f(v;\mu) \quad \forall v \in V $$


where $u(\mu) \in V$ is the exact solution. The solution manifold $\mathcal{M}$ consists of the solution of the problem under changing the parameter $\mu$:


$$ \mathcal{M} = \{u(\mu); \mu \in \mathcal{P}\} \subset V $$


### Finite Subspace and Truth Problem

Due to difficulty in finding the analytical exact solution, we introduce the finite subspace $V_h$ and formulate the truth problem:


$$ a(u_h(\mu), v_h; \mu) = f(v_h;\mu) \quad \forall v_h \in V_h $$


- $u_h(\mu) \in V_h$ is the truth solution, approximating the exact solution with arbitrary accuracy.
- High computational cost, dependent on $N_h$.

### Discrete Solution Manifold

The discrete version of the solution manifold is:


$$ \mathcal{M}_{d_s} = \{u_h(\mu); \mu \in \mathcal{P}\} \subset V_h $$


- Assumption: The solution manifold has low dimensionality.
- Low number of appropriately chosen basis functions represent the solution manifold with a small error.

### Reduced Basis Space

Let $\{\xi_j\}_{j=1}^N$ be the reduced basis, forming the reduced basis space:


$$ V_{N_h} = \text{span}(\xi_1, ..., \xi_N) \subset V_h $$


### Reduced Basis Approximation Problem

For any $\mu \in \mathcal{P}$, find $u_{N_h}(\mu) \in V_{N_h}$ such that:


$$ a(u_{N_h}(\mu), v_{N_h};\mu) = f(v_{N_h};\mu) \quad \forall v_{N_h} \in V_{N_h} $$


Evaluate:


$$ s_{N_h}(\mu) = l(u_{N_h}(\mu);\mu) $$


### Representation of Reduced Basis Solution

- Basis functions of $V_{N_h}$: $\xi_1, ..., \xi_N$.
- Solution representation: $u_{N_h}(\mu) = \sum_{n=1}^N u_{N_h}(\xi_n)\xi_n$.

### Reduced Approximation Solver

- Let $\{\xi_j\}_{j=1}^N$ be the reduced basis.
- Define matrix $B \in \mathbb{R}^{N \times N_h}$:


$$ \xi_n = \sum_{m=1}^{N_h} B_{nm} \phi_m $$


- The $k$-th column of matrix $B$ represents the coefficients of the $k$-th basis $\xi_n$ in terms of $\{\phi_i\}_{i=1}^{N_h}$.

### Reduced Basis Solution Matrix

- Reduced basis solution matrix $A_{N_h}^r \in \mathbb{R}^{N \times N}$ and right-hand side $f_{N_h}^r \in \mathbb{R}^N$:


$$ (A_{N_h}^r)_{ij} = a(\xi_i, \xi_j;\mu) $$


$$ (f_{N_h}^r)_i = f(\xi_i;\mu) $$


- Computed by:


$$ A_{N_h}^r = B^T A_{N_h} B $$


$$ f_{N_h}^r = B^T f_{N_h} $$


### Solving the Reduced Basis Approximation

- Solve the linear system:


$$ A_{N_h}^r u_{N_h}^r = f_{N_h}^r $$


- Output of interest:


$$ s_{N_h}(\mu) = (u_{N_h}^r)^T f_{N_h}^r $$


### Approximation Error


$$ ||u(\mu) - u_{N_h}(\mu)||_V \leq ||u(\mu) - u_h(\mu)||_V + ||u_h(\mu) - u_{N_h}(\mu)||_V $$


- The first term on the right-hand side can be made arbitrarily small.
- The accuracy of the reduced basis approximation depends on the problem, parameter set, required accuracy, and number of reduced basis functions.
