# Truth Discretization

A reduced-order model never approximates the exact solution of a PDE directly. It approximates a high-fidelity discrete solution, the truth, computed with a conventional finite element, finite volume or spectral discretization fine enough to be trusted. This note describes that truth problem for the parametrized variational problems of [Parametrized Variational Problems](parameterized_variational_problems.md): the Galerkin discretization, its algebraic form and the matrices a reduced model needs, the error analysis through Galerkin orthogonality and Céa's lemma, and the assumption, implicit in every reduced basis error bound, that the truth error is negligible. The reduced model built on top of it is the subject of [Reduced Basis Approximation](reduced_basis_approximation.md).

## Problem Statement

Given the variational problem "find $u(\mu) \in V$ with $a(u(\mu), v; \mu) = f(v; \mu)$ for all $v \in V$", choose a finite-dimensional subspace $V_h \subset V$ of dimension $N_h$ and solve

```math
\text{find } u_h(\mu) \in V_h \text{ such that } a(u_h(\mu), v_h; \mu) = f(v_h; \mu) \quad \text{for all } v_h \in V_h
```

The unknowns are the $N_h$ coefficients of $u_h$ in a basis of $V_h$; the data are the forms $a$, $f$, the domain and its mesh, and the parameter $\mu$. The truth is adequate when its discretization error $`\lVert u(\mu) - u_h(\mu) \rVert_V`$ is below the accuracy required of the final reduced model, uniformly over the parameter set $\mathcal{P}$. The difficulties are that this uniform accuracy can require a very fine mesh (for example to resolve boundary layers whose thickness changes with $\mu$), that each truth solve then costs seconds to hours, and that some parameter values make the discrete problem badly conditioned or unstable, as in convection-dominated flow.

## Galerkin Discretization

### Algebraic Form

Let $`\{\varphi_j\}_{j=1}^{N_h}`$ be a basis of $V_h$, for example the piecewise-linear hat functions of a finite element mesh ([Finite Element Method](../fem/intro.md)). Writing $`u_h(\mu) = \sum_j (\mathbf{u}_h(\mu))_j\varphi_j`$ and testing with each $\varphi_i$ gives the linear system

```math
A_h(\mu)\,\mathbf{u}_h(\mu) = \mathbf{f}_h(\mu),
\qquad
(A_h(\mu))_{ij} = a(\varphi_j, \varphi_i; \mu),
\qquad
(\mathbf{f}_h(\mu))_i = f(\varphi_i; \mu)
```

with the stiffness matrix $A_h \in \mathbb{R}^{N_h \times N_h}$ and load vector $\mathbf{f}_h \in \mathbb{R}^{N_h}$. Local support of the basis functions makes $A_h$ sparse. For a nonlinear problem the same construction gives a nonlinear residual $\mathbf{R}_h(\mathbf{u}_h; \mu) = \mathbf{0}$, solved by Newton or Picard iteration.

### Matrices a Reduced Model Needs

Three objects of the truth model are used by the reduced model.

- The affine components. If $`a = \sum_q\theta_q(\mu)a_q`$, then $`A_h(\mu) = \sum_q\theta_q(\mu)A_q`$ with $(A_q)_{ij} = a_q(\varphi_j, \varphi_i)$, assembled once by the same code with the parameter-dependent coefficient replaced by an indicator.
- The inner-product matrix $X_h$ with $(X_h)_{ij} = (\varphi_j, \varphi_i)_V$, so that $`\lVert v_h \rVert_V^2 = \mathbf{v}^TX_h\mathbf{v}`$. It is not the identity: the Euclidean norm of the coefficient vector depends on the mesh and is not a discretization of any function norm.
- The dual norm of a residual vector $\mathbf{r} \in \mathbb{R}^{N_h}$, the discrete counterpart of $`\lVert r \rVert_{V'}`$, which is $`\lVert \mathbf{r} \rVert_{X_h^{-1}} = \sqrt{\mathbf{r}^TX_h^{-1}\mathbf{r}}`$. Reduced basis error bounds are expressed in it.

## Error Analysis

### Galerkin Orthogonality

Because $V_h \subset V$, the exact solution also satisfies the discrete equations, $a(u, v_h; \mu) = f(v_h; \mu)$ for all $v_h \in V_h$. Subtracting the discrete problem gives Galerkin orthogonality,

$$
a(u(\mu) - u_h(\mu), v_h; \mu) = 0 \quad \text{for all } v_h \in V_h
$$

The error is orthogonal to the discrete space with respect to the form $a$. When $a$ is symmetric and coercive this is orthogonality in the energy inner product, and $u_h$ is the energy-orthogonal projection of $u$ onto $V_h$.

### Céa's Lemma

For any $v_h \in V_h$, coercivity, Galerkin orthogonality (with $v_h - u_h \in V_h$) and continuity give

```math
\alpha(\mu)\lVert u - u_h \rVert_V^2 \le a(u - u_h, u - u_h; \mu) = a(u - u_h, u - v_h; \mu) \le \gamma(\mu)\lVert u - u_h \rVert_V\,\lVert u - v_h \rVert_V
```

Dividing by $`\alpha\lVert u - u_h \rVert_V`$ and minimizing over $v_h$ gives Céa's lemma,

```math
\lVert u(\mu) - u_h(\mu) \rVert_V \le
\frac{\gamma(\mu)}{\alpha(\mu)}\,\inf_{v_h \in V_h} \lVert u(\mu) - v_h \rVert_V
```

The Galerkin solution is quasi-optimal: up to the factor $\gamma/\alpha$ it is as good as the best approximation from $V_h$. For symmetric $a$ the factor improves to $\sqrt{\gamma/\alpha}$, and in the energy norm the Galerkin solution is the best approximation. Combined with an interpolation estimate, for example $`\inf_{v_h}\lVert u - v_h \rVert_{H^1} \le Ch^k\lvert u \rvert_{H^{k+1}}`$ for polynomials of degree $k$ on a mesh of size $h$, Céa's lemma gives the convergence rate of the method.

The lemma applies verbatim to any subspace of $V$, including a reduced space $V_N \subset V_h$. This is why the reduced basis solution is quasi-optimal in the reduced space with the same constant $\gamma/\alpha$, and why a large ratio, as in convection-dominated problems, hurts the truth and the reduced model alike.

### Discrete Stability

Coercivity is inherited by every conforming subspace: $a(v_h, v_h; \mu) \ge \alpha(\mu)\lVert v_h \rVert_V^2$ for $v_h \in V_h$ because $v_h \in V$. The discrete coercivity constant $\alpha_h(\mu)$, the smallest eigenvalue of the generalized problem $A_h^{\mathrm{sym}}\mathbf{v} = \lambda X_h\mathbf{v}$ with the symmetric part $A_h^{\mathrm{sym}} = (A_h + A_h^T)/2$, therefore satisfies $\alpha_h(\mu) \ge \alpha(\mu)$. The inf-sup condition of saddle-point and indefinite problems is not inherited; it has to be proven for each pair of discrete spaces, which is the origin of the stable velocity–pressure element pairs of incompressible flow.

## Choices of the Truth Space

| Discretization | Space $V_h$ | Conforming Galerkin? | Notes for ROM |
| --- | --- | --- | --- |
| Continuous finite elements | piecewise polynomials, continuous across elements | yes | the setting of reduced basis theory; affine components by assembly with indicator coefficients |
| Spectral and spectral-element methods | global or high-degree local polynomials | yes | exponential convergence for smooth solutions, small $N_h$ for a given accuracy ([High-Order Methods](../high_order/intro.md)) |
| Discontinuous Galerkin | piecewise polynomials, discontinuous | no; consistent penalty terms replace conformity | Galerkin orthogonality holds for the DG form; coercivity in a mesh-dependent norm |
| Finite volumes | piecewise constants with reconstructed face values | no; a Petrov–Galerkin method with cell indicator test functions | no variational error analysis; ROMs are built by projecting the discrete equations with a volume-weighted inner product ([Finite Volume Method](../fvm/intro.md)) |
| Stabilized finite elements (SUPG) | continuous finite elements with residual-based test functions | consistent Petrov–Galerkin | needed at high Péclet or Reynolds number; affine if the stabilization parameter is |

Most industrial CFD codes are finite volume codes. For them the abstract framework above is replaced by the algebraic one: the truth is the discrete system as the code solves it, inner products are discrete sums weighted by cell volumes, and the reduced model is obtained by projecting the discrete operators (discretize, then project), as described in [POD-Galerkin Projection](pod_galerkin_projection.md).

## The Truth Assumption

The error of the reduced solution $u_N(\mu)$ splits into a discretization and a reduction part,

$$
\lVert u(\mu) - u_N(\mu) \rVert_V \le \lVert u(\mu) - u_h(\mu) \rVert_V + \lVert
u_h(\mu) - u_N(\mu) \rVert_V
$$

Reduced basis error bounds control only the second term; they certify the reduced model with respect to the truth, not with respect to the exact solution. The method therefore assumes that the truth error is negligible compared with the reduction error, uniformly in $\mu$, and the truth mesh must be chosen to make this true. In practice this is checked with a mesh-refinement study at a few parameters chosen at the edges of $\mathcal{P}$ where the solution is hardest to resolve, for example with the grid convergence index described in [Generating CFD Training Data](../../machine_learning/automotive_aerodynamics/generating_cfd_datasets.md) and [Verification and Validation](../cfd/verification_and_validation.md).

Because the online cost of a well-built reduced model does not depend on $N_h$, a rich truth space is affordable: its cost is paid only in the offline stage, once per snapshot.

## Cost of a Truth Solve

| Solver for $A_h\mathbf{u}_h = \mathbf{f}_h$ | Typical cost (3D, $N_h$ unknowns) |
| --- | --- |
| Dense direct solver | $O(N_h^3)$, never used for PDEs |
| Sparse direct solver (nested dissection) | about $O(N_h^2)$ operations and $O(N_h^{4/3})$ memory |
| Krylov solver with a good preconditioner | $O(N_h)$ per iteration, iteration count growing slowly with $N_h$ |
| Multigrid | $O(N_h)$ |

Even with optimal $O(N_h)$ solvers, a truth solve at $N_h = 10^7$ takes minutes to hours on a workstation, and a many-query study multiplies that by thousands. The reduced model replaces it by an $N \times N$ system with $N$ typically between 10 and 100. Solver choice is discussed in [Direct and Iterative Solvers](../cfd/direct_and_iterative_solvers.md).

## Key Takeaways

- The truth is a conforming Galerkin discretization $V_h \subset V$ of dimension $N_h$, giving $A_h(\mu)\mathbf{u}_h = \mathbf{f}_h(\mu)$; affine forms give affine matrices $`A_h = \sum_q\theta_qA_q`$.
- A reduced model also needs the inner-product matrix $X_h$: function norms are $\mathbf{v}^TX_h\mathbf{v}$, and residual dual norms are $\mathbf{r}^TX_h^{-1}\mathbf{r}$.
- Galerkin orthogonality gives Céa's lemma, $`\lVert u - u_h \rVert_V \le (\gamma/\alpha)\inf_{v_h}\lVert u - v_h \rVert_V`$, for the truth and, unchanged, for any reduced subspace.
- Coercivity is inherited by subspaces; the inf-sup condition is not.
- Reduced basis bounds certify the distance to the truth only, so the truth mesh must make the discretization error negligible over the whole parameter set.

## Related Scripts

- [Certified Reduced Basis Method for a Thermal Block](../../../scripts/algorithms/reduced_basis_thermal_block/): builds a certified reduced basis model of steady heat conduction in a 2D thermal block with three parametrized conductivities, using a weak greedy algorithm driven by the residual-based error bound $`\lVert r(\mu) \rVert_{X'}/\alpha_{\mathrm{LB}}(\mu)`$.
- [Grid Convergence Index](../../../scripts/algorithms/grid_convergence_index/): estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008).
- [2D Schrödinger Equation Simulation](../../../scripts/simulations/schroedinger_equation/): solves the time-dependent Schrödinger equation for a free particle in two dimensions with the split-step Fourier method and animates the probability density of the spreading wavepacket as a 3D surface.

## Exercises

**Exercise 1.** A truth problem has $N_h = 10^6$ unknowns and a reduced model has $N = 20$. Using the dense direct-solver estimates $O(N_h^3)$ and $O(N^3)$, what is the cost ratio? At $10^9$ floating-point operations per second, how long would each solve take? How does the picture change with an $O(N_h)$ multigrid solver needing about 100 operations per unknown?

<details>
<summary>Answer</summary>

$N_h^3 = 10^{18}$ and $N^3 = 8000$, a ratio of $1.25 \times 10^{14}$. At $10^9$ operations per second the dense truth solve would take $10^9$ s (about 32 years), the reduced solve 8 µs. With multigrid the truth solve costs about $10^8$ operations, 0.1 s, still more than $10^4$ times the reduced solve. The dense estimate exaggerates the gain enormously; the realistic speed-up of a linear reduced model is the ratio of an optimal sparse solve to an $N^3$ dense solve.

</details>

**Exercise 2.** Solve $-u'' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$ using piecewise-linear finite elements on a uniform mesh, for $h = 1/2$ and $h = 1/4$. Assemble $A_h$ and $\mathbf{f}_h$ from $`a(u, v) = \int_0^1 u'v' \, dx`$ and $`f(v) = \int_0^1 v \, dx`$, solve, and compare with the exact solution $u(x) = x(1 - x)/2$.

<details>
<summary>Answer</summary>

For hat functions, $a(\varphi_i, \varphi_i) = 2/h$, $a(\varphi_i, \varphi_{i \pm 1}) = -1/h$ and $f(\varphi_i) = h$.

$h = 1/2$ (one interior node): $A_h = [4]$ and $\mathbf{f}_h = [1/2]$, so $u_h(1/2) = 0.125$, equal to the exact value.

$h = 1/4$ (three interior nodes):

```math
A_h = \begin{pmatrix} 8 & -4 & 0 \\ -4 & 8 & -4 \\ 0 & -4 & 8 \end{pmatrix}, \qquad \mathbf{f}_h = \begin{pmatrix} 0.25 \\ 0.25 \\ 0.25 \end{pmatrix}, \qquad \mathbf{u}_h = \begin{pmatrix} 0.09375 \\ 0.125 \\ 0.09375 \end{pmatrix}
```

These equal the exact values at $x = 0.25, 0.5, 0.75$. In 1D the Galerkin solution of $-u'' = f$ is exact at the nodes; between the nodes the piecewise-linear function still differs from the parabola.

</details>

**Exercise 3.** Make the problem of Exercise 2 parametric: $-\mu u'' = 1$ with $\mu \in [0.1, 10]$. Show that $A_h(\mu) = \mu A_1$ and $\mathbf{u}_h(\mu) = \mathbf{u}_h(1)/\mu$. What does this imply for the discrete solution manifold and the smallest exact reduced basis?

<details>
<summary>Answer</summary>

$`a(\varphi_j, \varphi_i; \mu) = \mu\int\varphi_j'\varphi_i' \, dx`$, so $A_h(\mu) = \mu A_1$, while $\mathbf{f}_h$ does not depend on $\mu$. Then $\mathbf{u}_h(\mu) = (\mu A_1)^{-1}\mathbf{f}_h = \mathbf{u}_h(1)/\mu$. Every truth solution is a multiple of one vector, so the solution manifold lies in a one-dimensional subspace and a reduced basis with $N = 1$ is exact for every $\mu$. Most problems are not this simple, but fast singular value decay of the snapshots reflects the same idea.

</details>

**Exercise 4.** Solve $-\mu u'' + u' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$ and $\mu = 0.01$ by piecewise-linear finite elements with $h = 0.1$. The Céa factor for this problem is $\gamma/\alpha \le 1 + 1/(\pi\mu) \approx 32.8$ (Exercise 3 of [Parametrized Variational Problems](parameterized_variational_problems.md)). Compare the $H^1$-seminorm errors of the Galerkin solution and of the nodal interpolant of the exact solution $u = x - (e^{(x-1)/\mu} - e^{-1/\mu})/(1 - e^{-1/\mu})$, and look at the nodal values.

<details>
<summary>Answer</summary>

The Galerkin equations are $`(\mu/h)(-u_{i-1} + 2u_i - u_{i+1}) + (u_{i+1} - u_{i-1})/2 = h`$. Solving them gives the nodal values $(0.144, 0.178, 0.377, 0.328, 0.652, 0.417, 1.019, 0.365, 1.596)$ at $x = 0.1, \dots, 0.9$, against the exact values $0.1, \dots, 0.9$ (the boundary layer at $x = 1$ has thickness $\mu = 0.01$, far below $h$). The solution oscillates from node to node, with an error of 0.70 at $x = 0.9$, because the cell Péclet number $h/(2\mu) = 5$ exceeds 1.

In the $H^1$ seminorm the Galerkin error is 8.24 and the interpolation error 6.32, a ratio of 1.30. In 1D the interpolant is the best $H^1_0$-seminorm approximation from $V_h$, so Céa's bound of 32.8 is satisfied with a wide margin; both errors are dominated by the unresolved layer. The practical failure, the oscillation, is visible in the nodal values, not in the norm that Céa's lemma controls. It is cured by refining to $h < 2\mu$ or by SUPG stabilization.

</details>

## References

- S. C. Brenner and L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Springer, 2008.
- A. Ern and J.-L. Guermond, *Theory and Practice of Finite Elements*, Applied Mathematical Sciences 159, Springer, 2004.
- A. Quarteroni and A. Valli, *Numerical Approximation of Partial Differential Equations*, Springer, 1994.
- H. C. Elman, D. J. Silvester and A. J. Wathen, *Finite Elements and Fast Iterative Solvers: with Applications in Incompressible Fluid Dynamics*, 2nd ed., Oxford University Press, 2014.
- A. Quarteroni, A. Manzoni and F. Negri, *Reduced Basis Methods for Partial Differential Equations: An Introduction*, Springer, 2016.
- J. S. Hesthaven, G. Rozza and B. Stamm, *Certified Reduced Basis Methods for Parametrized Partial Differential Equations*, SpringerBriefs in Mathematics, Springer, 2016.
