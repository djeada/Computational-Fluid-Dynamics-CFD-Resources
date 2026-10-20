# Direct and Iterative Solvers

Every implicit time step, every outer iteration of a steady solver and every Newton step ends in a linear system $A\boldsymbol{\phi} = \mathbf{b}$ with one unknown per cell and variable. Solving these systems usually takes most of the run time of a CFD code. This note describes the structure of the matrices that discretization produces, direct elimination including the Thomas algorithm, the classical stationary iterations, Krylov methods and preconditioning, and multigrid, and ends with a guide to choosing a solver.

How the nonlinear equations are reduced to linear ones is covered in [Dealing with Nonlinearity](dealing_with_nonlinearity.md), and how to judge when an iteration has converged in [Iterative Convergence](iterative_convergence.md).

## Problem Statement

Given a sparse matrix $A \in \mathbb{R}^{N \times N}$ and a right-hand side $\mathbf{b}$ from a finite-difference, finite-volume or finite-element discretization, find $\boldsymbol{\phi}$ such that

$$
A\boldsymbol{\phi} = \mathbf{b}
$$

to a prescribed accuracy, usually a relative residual $`\|\mathbf{b} - A\boldsymbol{\phi}\|/\|\mathbf{b}\| \le \varepsilon`$. Inside a nonlinear iteration $\varepsilon$ is moderate ($10^{-1}$ to $10^{-3}$), because the matrix changes at the next outer iteration anyway; for a pressure equation in a time-accurate projection method it is tight ($10^{-6}$ or below), because the error goes directly into the divergence of the velocity.

What makes the problem hard:

- $N$ ranges from $10^5$ to $10^9$, so dense methods are out of the question and even sparse direct methods run out of memory in 3D.
- The condition number of discretized elliptic operators grows like $h^{-2}$, which slows most iterative methods as the mesh is refined.
- Convection makes $A$ nonsymmetric; pure Neumann conditions on a pressure equation make it singular.
- The solver must run in parallel on distributed memory, which rules out inherently sequential algorithms.

## Sparse Matrices from Discretization

For the 1D Poisson equation $-\phi'' = f$ with Dirichlet ends, central differences give a tridiagonal matrix:

```math
\frac{1}{h^2}\begin{bmatrix}
2 & -1 & & & \\
-1 & 2 & -1 & & \\
 & \ddots & \ddots & \ddots & \\
 & & -1 & 2 & -1 \\
 & & & -1 & 2
\end{bmatrix}
\begin{bmatrix} \phi_1 \\ \phi_2 \\ \vdots \\ \phi_{n-1} \\ \phi_n \end{bmatrix}
=
\begin{bmatrix} f_1 + \phi_0/h^2 \\ f_2 \\ \vdots \\ f_{n-1} \\ f_n + \phi_{n+1}/h^2 \end{bmatrix}
```

In 2D the five-point stencil on an $n \times n$ grid, numbered row by row, gives a block-tridiagonal matrix $A = (T \otimes I + I \otimes T)/h^2$ with $T = \mathrm{tridiag}(-1, 2, -1)$. Each row has five nonzeros, but the outer diagonals are $n$ positions away from the main diagonal: the **bandwidth** is $n = \sqrt{N}$. In 3D the seven-point stencil has bandwidth $n^2 = N^{2/3}$. On unstructured finite-volume meshes, row $P$ has one entry for the cell and one per face neighbour, and the bandwidth depends on the cell numbering (reverse Cuthill–McKee reordering reduces it).

The properties that decide which solver works:

| Source of the matrix | Symmetric | Definite | Typical structure |
| --- | --- | --- | --- |
| Diffusion, pressure Poisson or pressure correction | yes | positive (semi-definite with pure Neumann conditions) | M-matrix, diagonally dominant |
| Convection–diffusion with upwind convection | no | eigenvalues with positive real part | diagonally dominant M-matrix |
| Convection–diffusion with central convection at high cell Péclet number | no | indefinite symmetric part possible | not diagonally dominant |
| Newton Jacobian of the coupled Navier–Stokes equations | no | indefinite (saddle point for incompressible flow) | block structure, ill-conditioned |

For the model Poisson problem the eigenvalues are known exactly, and the condition number is

$$
\kappa(A) = \frac{\lambda_{\max}}{\lambda_{\min}} = \cot^2 \frac{\pi h}{2} \approx
\frac{4}{\pi^2h^2}
$$

in both 1D and 2D: halving the mesh spacing multiplies $\kappa$ by four.

Matrices are stored in compressed sparse row (CSR) format or, in finite-volume codes, as one coefficient per face plus a diagonal (the $a_P$, $a_{nb}$ form of Patankar). Memory and work are then proportional to the number of nonzeros, $O(N)$.

## Direct Methods

### Gaussian Elimination and LU Factorization

Gaussian elimination factorizes $A = LU$ with $L$ unit lower triangular and $U$ upper triangular, after which $L\mathbf{y} = \mathbf{b}$ and $U\boldsymbol{\phi} = \mathbf{y}$ are solved by forward and back substitution. For a dense matrix the factorization costs about $\tfrac{2}{3}N^3$ floating-point operations and the substitutions $2N^2$. Partial pivoting is needed for general matrices; for symmetric positive-definite or diagonally dominant matrices the factorization is stable without it (Cholesky, $A = LL^T$, at half the cost).

For a banded matrix with half-bandwidth $b$, elimination does not create nonzeros outside the band, so the cost is $O(Nb^2)$ and the storage $O(Nb)$. Inside the band, however, the zeros between the diagonals fill in: the factors of the 2D five-point matrix are dense within the band. This **fill-in** is what limits direct methods:

| Grid | $N$ | Bandwidth $b$ | Banded LU work $O(Nb^2)$ | Storage $O(Nb)$ |
| --- | --- | --- | --- | --- |
| 1D, $n$ points | $n$ | 1 | $O(N)$ | $O(N)$ |
| 2D, $n \times n$ | $n^2$ | $n$ | $O(N^2)$ | $O(N^{3/2})$ |
| 3D, $n \times n \times n$ | $n^3$ | $n^2$ | $O(N^{7/3})$ | $O(N^{5/3})$ |

Reordering with nested dissection reduces the 2D cost to $O(N^{3/2})$ work and $O(N\log N)$ storage, and the 3D cost to $O(N^2)$ work and $O(N^{4/3})$ storage (George, 1973). Modern sparse direct solvers (multifrontal and supernodal) are robust and fast for 2D problems and moderate 3D problems, and they are the method of choice when many right-hand sides share one matrix. For large 3D CFD problems the memory requirement rules them out, except on small subproblems such as coarse multigrid levels.

### Thomas Algorithm

A tridiagonal system $a_i\phi_{i-1} + d_i\phi_i + c_i\phi_{i+1} = b_i$, $i = 1, \dots, n$ (with $a_1 = c_n = 0$) has no fill-in, and Gaussian elimination reduces to the Thomas algorithm, also called TDMA:

1. Forward sweep: set $c'_1 = c_1/d_1$ and $b'_1 = b_1/d_1$, then for $i = 2, \dots, n$

   ```math
   m_i = d_i - a_i c'_{i-1}, \qquad c'_i = \frac{c_i}{m_i}, \qquad b'_i = \frac{b_i - a_i b'_{i-1}}{m_i}
   ```

2. Back substitution: $\phi_n = b'_n$, then for $i = n-1, \dots, 1$

   ```math
   \phi_i = b'_i - c'_i\,\phi_{i+1}
   ```

The cost is about $8n$ operations, and the algorithm is stable without pivoting when the matrix is diagonally dominant ($|d_i| \ge |a_i| + |c_i|$), as discretized diffusion and upwind convection matrices are.

As a worked example, take $A = \mathrm{tridiag}(-1, 4, -1)$ with $n = 3$ and $\mathbf{b} = (2, 4, 10)$. The forward sweep gives $c'_1 = -0.25$, $b'_1 = 0.5$; $m_2 = 4 - 0.25 = 3.75$, $c'_2 = -0.2667$, $b'_2 = 4.5/3.75 = 1.2$; $m_3 = 4 - 0.2667 = 3.7333$, $b'_3 = 11.2/3.7333 = 3$. Back substitution gives $\phi_3 = 3$, $\phi_2 = 1.2 + 0.2667 \times 3 = 2$ and $\phi_1 = 0.5 + 0.25 \times 2 = 1$.

Finite-volume codes use TDMA along grid lines inside line-by-line iterations (Patankar, 1980): each sweep solves the tridiagonal systems of all lines in one direction with the off-line neighbours taken from the latest iterate, alternating directions. In multidimensional ADI time stepping each half-step is a set of tridiagonal solves.

## Stationary Iterative Methods

### Splitting and Convergence

Write $A = M - N$ with $M$ easy to invert. The iteration

$$
M\boldsymbol{\phi}^{k+1} = N\boldsymbol{\phi}^k + \mathbf{b}
\qquad \Longleftrightarrow
\qquad \boldsymbol{\phi}^{k+1} = \boldsymbol{\phi}^k + M^{-1}\mathbf{r}^k, \quad
\mathbf{r}^k = \mathbf{b} - A\boldsymbol{\phi}^k
$$

has the exact solution as a fixed point, and its error $\mathbf{e}^k = \boldsymbol{\phi} - \boldsymbol{\phi}^k$ obeys

```math
\mathbf{e}^{k+1} = G\,\mathbf{e}^k,
\qquad G = M^{-1}N = I - M^{-1}A
```

The iteration converges for every initial guess if and only if the spectral radius $\rho(G) = \max_j|\lambda_j(G)| < 1$. Asymptotically the error is multiplied by $\rho$ per iteration, so reducing it by a factor $10^{-m}$ takes

$$
k \approx \frac{m\ln 10}{-\ln\rho(G)}
$$

iterations. With $A = D - L - U$ (diagonal, strictly lower and strictly upper parts with the signs reversed), the classical methods are:

| Method | $M$ | Component form |
| --- | --- | --- |
| Jacobi | $D$ | $`\phi_i^{k+1} = \left(b_i - \sum_{j \ne i} a_{ij}\phi_j^k\right)/a_{ii}`$ |
| Gauss–Seidel | $D - L$ | $`\phi_i^{k+1} = \left(b_i - \sum_{j < i} a_{ij}\phi_j^{k+1} - \sum_{j > i} a_{ij}\phi_j^k\right)/a_{ii}`$ |
| SOR | $D/\omega - L$ | $`\phi_i^{k+1} = (1 - \omega)\phi_i^k + \omega\,\phi_i^{\mathrm{GS}}`$, with $\phi_i^{\mathrm{GS}}$ the Gauss–Seidel value |

Jacobi and Gauss–Seidel converge for strictly diagonally dominant matrices and Gauss–Seidel for all symmetric positive-definite ones. SOR converges for symmetric positive-definite matrices when $0 < \omega < 2$.

### The Model Poisson Problem

For the five-point Poisson matrix with $h = 1/(n+1)$ the spectral radii are known (Young, 1954):

```math
\rho_J = \cos\pi h \approx 1 - \frac{\pi^2h^2}{2}, \qquad
\rho_{GS} = \rho_J^2 = \cos^2\pi h, \qquad
\omega_{\mathrm{opt}} = \frac{2}{1 + \sin\pi h}, \qquad
\rho_{\mathrm{SOR}} = \omega_{\mathrm{opt}} - 1 \approx 1 - 2\pi h
```

To reduce the error by $10^{-8}$, Jacobi needs about $3.7/h^2$ iterations, Gauss–Seidel half as many, and optimal SOR about $2.9/h$. Each refinement of the grid by a factor two multiplies the Jacobi and Gauss–Seidel count by four and the SOR count by two.

The reason is visible in the error modes. The eigenvector $\sin(p\pi x)\sin(q\pi y)$ of the Jacobi iteration has the eigenvalue $\tfrac{1}{2}(\cos p\pi h + \cos q\pi h)$, which is close to 1 for smooth modes ($p, q$ small) and small for oscillatory ones. Jacobi and Gauss–Seidel remove local, oscillatory error in a few sweeps and then crawl, because each sweep only moves information one cell. That observation is the starting point of multigrid.

## Krylov Subspace Methods

Krylov methods build the iterate from the space

```math
\mathcal{K}_k(A, \mathbf{r}^0) = \mathrm{span}\left\{\mathbf{r}^0, A\mathbf{r}^0,
A^2\mathbf{r}^0, \dots, A^{k-1}\mathbf{r}^0\right\}
```

and pick, at each step, the best approximation in $\boldsymbol{\phi}^0 + \mathcal{K}_k$ in some norm. They need only matrix–vector products and inner products, so they work with any sparse format and parallelize well.

### Conjugate Gradients

For symmetric positive-definite $A$, the conjugate gradient method (Hestenes and Stiefel, 1952) minimises the energy norm $`\|\mathbf{e}\|_A = \sqrt{\mathbf{e}^TA\mathbf{e}}`$ over $\boldsymbol{\phi}^0 + \mathcal{K}_k$ with short recurrences:

1. $\mathbf{r}^0 = \mathbf{b} - A\boldsymbol{\phi}^0$, $\mathbf{p}^0 = \mathbf{r}^0$.

2. For $k = 0, 1, \dots$ until $`\|\mathbf{r}^{k+1}\| \le \varepsilon\|\mathbf{b}\|`$:

   ```math
   \alpha_k = \frac{\mathbf{r}^{k\,T}\mathbf{r}^k}{\mathbf{p}^{k\,T}A\mathbf{p}^k},\quad
   \boldsymbol{\phi}^{k+1} = \boldsymbol{\phi}^k + \alpha_k\mathbf{p}^k,\quad
   \mathbf{r}^{k+1} = \mathbf{r}^k - \alpha_k A\mathbf{p}^k,\quad
   \beta_k = \frac{\mathbf{r}^{k+1\,T}\mathbf{r}^{k+1}}{\mathbf{r}^{k\,T}\mathbf{r}^k},\quad
   \mathbf{p}^{k+1} = \mathbf{r}^{k+1} + \beta_k\mathbf{p}^k
   ```

Each iteration costs one matrix–vector product, two inner products and three vector updates. The error satisfies

```math
\|\mathbf{e}^k\|_A \le
2\left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^k\|\mathbf{e}^0\|_A
```

so about $`\tfrac{1}{2}\sqrt{\kappa}\,\ln(2/\varepsilon)`$ iterations reduce the error by $\varepsilon$. For the Poisson problem $\sqrt{\kappa} \propto 1/h$, the same growth as optimal SOR, but without a parameter to tune; with a good preconditioner the count drops much further.

### Nonsymmetric Systems: GMRES and BiCGStab

GMRES (Saad and Schultz, 1986) minimises $`\|\mathbf{r}^k\|_2`$ over $\boldsymbol{\phi}^0 + \mathcal{K}_k$. The residual decreases monotonically, and in exact arithmetic it terminates in at most $N$ steps, but it has to store an orthonormal basis of the Krylov space, so memory and work grow with $k$. In practice it is restarted every $m$ iterations, GMRES($m$), with $m$ between 20 and 100, at the price of possible stagnation. It is the usual inner solver of Newton–Krylov methods.

BiCGStab (van der Vorst, 1992) uses short recurrences with two matrix–vector products per iteration and fixed memory. Its residual history is irregular and it can break down, but it is often faster than restarted GMRES on convection–diffusion matrices and is widely used in segregated finite-volume codes for the momentum and transport equations.

## Preconditioning

A preconditioner $P \approx A$ that is cheap to apply transforms the system into one with a smaller condition number or more clustered eigenvalues, for example $P^{-1}A\boldsymbol{\phi} = P^{-1}\mathbf{b}$. The Krylov method then needs only products with $A$ and solves with $P$. Common choices:

| Preconditioner | Construction | Effect |
| --- | --- | --- |
| Jacobi (diagonal) | $P = D$ | removes badly scaled rows from variable coefficients or cell sizes; no gain for the constant-coefficient Poisson matrix |
| Incomplete LU, ILU(0) | LU factorization that keeps only the nonzero pattern of $A$ | several times fewer iterations; $\kappa(P^{-1}A)$ still grows like $h^{-2}$ |
| Incomplete Cholesky, IC(0) | the symmetric analogue for SPD matrices | used with CG for pressure equations |
| Multigrid (geometric or algebraic) | one V-cycle as $P^{-1}$ | iteration count nearly independent of $h$ |
| Block Jacobi or additive Schwarz | ILU or direct solve on each processor's subdomain | the standard parallel preconditioner; weakens as the number of subdomains grows |

ILU and Gauss–Seidel are inherently sequential, so parallel codes apply them per subdomain. A good preconditioner for the coupled Navier–Stokes Jacobian has to respect its block structure, for example by approximating the pressure Schur complement.

## Multigrid

### Smoothing and Coarse-Grid Correction

Multigrid (Brandt, 1977; Briggs, Henson and McCormick, 2000) uses the two observations from the stationary methods. A few sweeps of a relaxation method, the **smoother**, remove the oscillatory part of the error and leave a smooth error. A smooth error can be represented on a coarser grid, where it looks more oscillatory and is again reduced efficiently, and where the work is smaller.

For weighted Jacobi on the 1D Poisson matrix with $n$ intervals, the mode $\sin(k\pi x)$ is multiplied per sweep by

$$
\lambda_k(\omega) = 1 - 2\omega\sin^2 \frac{k\pi}{2n}
$$

With $\omega = 2/3$, every mode with $n/2 \le k < n$, which the grid of spacing $2h$ cannot represent, is reduced at least by a factor 3 per sweep, while the smoothest mode is reduced by only $1 - O(h^2)$. Plain Jacobi ($\omega = 1$) does not damp the highest modes at all. Red-black Gauss–Seidel is an even better smoother for the Poisson equation.

### Two-Grid Cycle and V-Cycle

A two-grid cycle for $A_h\boldsymbol{\phi}_h = \mathbf{b}_h$ is:

1. Pre-smooth: apply $\nu_1$ sweeps of the smoother to $\boldsymbol{\phi}_h$.
2. Compute the residual $`\mathbf{r}_h = \mathbf{b}_h - A_h\boldsymbol{\phi}_h`$ and restrict it, $`\mathbf{r}_{2h} = I_h^{2h}\mathbf{r}_h`$ (full weighting averages each coarse point with its fine neighbours, with weights $\tfrac{1}{4}, \tfrac{1}{8}, \tfrac{1}{16}$ in 2D).
3. Solve the coarse error equation $`A_{2h}\mathbf{e}_{2h} = \mathbf{r}_{2h}`$.
4. Interpolate and correct: $`\boldsymbol{\phi}_h \leftarrow \boldsymbol{\phi}_h + I_{2h}^h\mathbf{e}_{2h}`$ (bilinear interpolation).
5. Post-smooth with $\nu_2$ sweeps.

The **V-cycle** solves step 3 by applying the same cycle recursively on the coarse grid, down to a grid small enough for a direct solve. In 2D the coarse grids have $\tfrac{1}{4}, \tfrac{1}{16}, \dots$ of the fine-grid points, so a V-cycle costs at most $1/(1 - 1/4) = 4/3$ times the work of the fine-grid smoothing and residual computation ($8/7$ in 3D). Because the convergence factor per cycle is bounded independently of $h$ (about 0.1 for the Poisson equation with red-black Gauss–Seidel), the total work to reach a fixed tolerance is $O(N)$. Full multigrid, which starts on the coarsest grid and interpolates each converged solution to the next finer grid as an initial guess, reaches the discretization error in $O(N)$ work.

Geometric multigrid needs a hierarchy of grids. Algebraic multigrid (AMG) builds the coarse levels from the matrix entries alone, which makes it applicable to unstructured meshes. It is the default pressure solver or preconditioner in many CFD codes (GAMG in OpenFOAM, for example). For strongly anisotropic problems, such as high-aspect-ratio boundary-layer cells, point smoothers fail and line smoothers or semi-coarsening are needed. Multigrid is also used directly on the nonlinear equations (the full approximation scheme), which is how many compressible steady-state solvers accelerate pseudo-time marching.

### Measured Iteration Counts

![Residual histories, iterations against grid size and weighted-Jacobi smoothing for the 2D Poisson equation](../../../scripts/algorithms/iterative_linear_solvers/iterative_linear_solvers.png)

The figure solves the 2D Poisson equation with a random source to a relative residual of $10^{-8}$. The iteration counts are:

| $N$ per direction | $\kappa$ | Jacobi | Gauss–Seidel | SOR ($\omega_{\mathrm{opt}}$) | CG | Multigrid V(2,1) |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 103 | 813 | 389 | 51 | 49 | 7 |
| 31 | 414 | 3040 | 1556 | 106 | 99 | 7 |
| 63 | 1659 | 12121 | 6156 | 217 | 194 | 7 |
| 127 | 6640 | 46436 | 23564 | 435 | 388 | 7 |

Jacobi and Gauss–Seidel scale like $N^2 \propto \kappa$, SOR and CG like $N \propto \sqrt{\kappa}$, and multigrid needs the same seven cycles on every grid. Panels (c) and (d) show the smoothing property behind that result.

## Which Solver

| Problem | Recommended solver | Remarks |
| --- | --- | --- |
| Tridiagonal systems: 1D problems, line relaxation, ADI | Thomas algorithm | $O(N)$, exact |
| Small or 2D problems, many right-hand sides, very ill-conditioned matrices | sparse direct LU or Cholesky | robust; memory grows quickly in 3D |
| Pressure or pressure-correction equation (SPD), large | CG preconditioned with AMG or IC, or AMG/GAMG as the solver | the most expensive linear solve of incompressible codes; needs tight tolerance in time-accurate projection methods |
| Momentum, energy and turbulence equations in segregated solvers (nonsymmetric, diagonally dominant) | a few Gauss–Seidel or ILU-preconditioned BiCGStab iterations | solved loosely, relative tolerance about 0.1, since the coefficients change every outer iteration |
| Newton or coupled-solver Jacobians (nonsymmetric, indefinite, ill-conditioned) | restarted GMRES with ILU, block or AMG preconditioning | see Newton–Krylov in [Dealing with Nonlinearity](dealing_with_nonlinearity.md) |
| Massively parallel runs | Krylov methods with AMG or domain-decomposition preconditioners | avoid global sequential sweeps |

The stationary methods (Jacobi, Gauss–Seidel, SOR) are rarely used as solvers on their own; they survive as smoothers inside multigrid and as cheap approximate solvers for well-conditioned transport equations. How linear solves fit into SIMPLE-type outer iterations is described in [Pressure–Velocity Coupling](../fvm/pressure_velocity_coupling.md).

## Key Takeaways

- Discretization produces sparse matrices with a few nonzeros per row; their bandwidth and fill-in make direct elimination $O(N^2)$ or worse in 2D and 3D, except for tridiagonal systems, where the Thomas algorithm costs $O(N)$.
- A stationary iteration converges if and only if the spectral radius of its iteration matrix is below 1; for Poisson problems $\rho \to 1$ as $h \to 0$, giving $O(h^{-2})$ iterations for Jacobi and Gauss–Seidel and $O(h^{-1})$ for optimal SOR.
- CG needs $O(\sqrt{\kappa})$ iterations for SPD matrices; GMRES and BiCGStab handle nonsymmetric ones; preconditioning is what makes Krylov methods practical.
- Relaxation smooths the error and the coarse grid removes the smooth remainder, so multigrid converges in a number of cycles independent of $h$, at $O(N)$ cost.
- Inside nonlinear iterations, solve the linear systems only as accurately as the outer iteration needs.

## Related Scripts

- [Iterative Linear Solvers on the Poisson Equation](../../../scripts/algorithms/iterative_linear_solvers/): solves the 2D Poisson equation on an $N \times N$ grid with Jacobi, Gauss–Seidel, SOR with the optimal relaxation factor, conjugate gradients and a geometric multigrid V-cycle, and compares how many iterations each needs as the grid is refined.
- [Residual Monitoring During an Iterative Solve](../../../scripts/algorithms/residual_monitoring/): follows a Gauss–Seidel solve of the 2D Poisson equation sweep by sweep and records everything a CFD user might look at to decide whether the run has converged: the residual with two normalisations, the change between iterates, the true iterative error, and an integral quantity (the flux through a wall).
- [Variation of Residual with Iteration](../../../scripts/plots/variation_of_residual/): solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale.
- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Picard Iteration and Newton's Method for Steady Burgers](../../../scripts/algorithms/picard_vs_newton/): solves the discretized steady viscous Burgers equation, a 1D model of the convective nonlinearity in the Navier–Stokes equations, with Picard iteration and Newton's method and compares their convergence.
- [Simplified Real-Time Fluid Dynamics Simulator](../../../scripts/simulations/simplified_real_time_fluid_dynamics_simulator/): is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Matplotlib window.

## Exercises

**Exercise 1.** Apply two iterations of Jacobi and of Gauss–Seidel, both starting from $\boldsymbol{\phi} = \mathbf{0}$, to $A\boldsymbol{\phi} = \mathbf{b}$ with $`A = \begin{bmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{bmatrix}`$ and $\mathbf{b} = (2, 4, 10)$. The exact solution is $(1, 2, 3)$.

<details>
<summary>Answer</summary>

Jacobi (all updates use the previous iterate):

- $\boldsymbol{\phi}^{(1)} = (0.5, 1, 2.5)$
- $\boldsymbol{\phi}^{(2)} = (0.75, 1.75, 2.75)$

Gauss–Seidel (each update uses the newest values):

- $\boldsymbol{\phi}^{(1)} = (0.5, 1.125, 2.78125)$
- $\boldsymbol{\phi}^{(2)} = (0.78125, 1.890625, 2.97265625)$

After two iterations Gauss–Seidel is noticeably closer to $(1, 2, 3)$. The Thomas algorithm in the note solves the same system exactly in one pass.

</details>

**Exercise 2.** For the matrix of Exercise 1 the Jacobi iteration matrix has spectral radius $\rho_J = \tfrac{1}{2}\cos(\pi/4)$, and $\rho_{GS} = \rho_J^2$. How many iterations does each need to reduce the error by $10^6$? For a 1D Poisson problem with $h = 0.01$, $\rho_J = \cos(\pi h)$. How many Jacobi iterations are needed there?

<details>
<summary>Answer</summary>

$\rho_J \approx 0.354$ and $\rho_{GS} = 0.125$. The iteration count is $k = \ln(10^{-6})/\ln\rho$:

- Jacobi: $k \approx 13.3$, so 14 iterations.
- Gauss–Seidel: $k \approx 6.6$, so 7 iterations.

For Poisson with $h = 0.01$: $\rho_J = \cos(0.0314) \approx 0.99951$, so $k \approx 28{,}000$.

Strongly diagonally dominant matrices, such as those of implicit time steps with small $\Delta t$, converge fast. Discretized elliptic operators have $\rho \to 1$ as the grid is refined, which is why CFD codes use preconditioned Krylov methods or multigrid for them.

</details>

**Exercise 3.** Estimate the time and memory to solve a dense system with $N = 10^5$ unknowns by LU decomposition on hardware doing $10^{10}$ floating-point operations per second. Compare with 1000 iterations of an iterative method on a sparse matrix with 5 nonzeros per row, counting only the matrix–vector products. Then estimate the banded-LU work for a $316 \times 316$ five-point grid ($N \approx 10^5$).

<details>
<summary>Answer</summary>

Dense LU: $\tfrac{2}{3}(10^5)^3 \approx 6.7 \times 10^{14}$ operations, about $6.7 \times 10^4$ s or 18.5 h. The matrix alone needs $10^{10} \times 8$ bytes $= 80$ GB.

Sparse iterative: $2 \times 5 \times 10^5 = 10^6$ operations per product (a multiply and an add per nonzero), times 1000, is $10^9$ operations, about 0.1 s of arithmetic. Real timings are dominated by memory access, but the gap is still several orders of magnitude, and the memory is a few megabytes.

Banded LU with $b = 316$: about $2Nb^2 \approx 2 \times 10^5 \times 10^5 = 2 \times 10^{10}$ operations, 2 s, and $Nb \approx 3.2 \times 10^7$ stored entries (250 MB). Exploiting the band makes the direct solve practical in 2D; in 3D the same $N$ ($46^3$ cells) would have $b \approx 2150$ and need about 46 times more work.

</details>

**Exercise 4.** The $63 \times 63$ Poisson matrix has $\kappa = 1659$. Use the CG error bound to estimate the number of iterations for a reduction of $10^{-8}$, and compare with the 194 iterations measured by the script. Do the same for optimal SOR, whose measured count is 217.

<details>
<summary>Answer</summary>

CG: $`\tfrac{1}{2}\sqrt{1659}\,\ln(2 \times 10^8) = 20.4 \times 19.1 \approx 389`$ iterations. The measured 194 is half the bound: the bound assumes the worst distribution of eigenvalues, while CG adapts to the actual spectrum and the measured quantity is the residual, not the $A$-norm of the error.

SOR: $\omega_{\mathrm{opt}} = 2/(1 + \sin(\pi/64)) = 1.9065$, $\rho = 0.9065$, so $k = \ln 10^{-8}/\ln 0.9065 \approx 188$. The measured 217 is somewhat higher because the SOR iteration matrix at $\omega_{\mathrm{opt}}$ is not diagonalizable and its error first grows before decaying at the rate $\rho$.

</details>

**Exercise 5.** A 3D multigrid solver uses coarsening by two in each direction. Show that a V-cycle costs at most $8/7$ of the work done on the finest grid. If one V-cycle reduces the error by a factor 0.1, how many cycles and how much work, in units of fine-grid sweeps, are needed to reduce the error by $10^{-8}$ on a grid of $256^3$ cells, with 3 smoothing sweeps per level? Compare with Gauss–Seidel, $\rho_{GS} = \cos^2(\pi h)$ with $h = 1/257$.

<details>
<summary>Answer</summary>

Each coarse grid has $1/8$ of the points of the next finer one, so the work is at most $1 + 1/8 + 1/64 + \dots = 1/(1 - 1/8) = 8/7$ times the fine-grid work.

Eight cycles give $10^{-8}$. With 3 sweeps per level (plus a residual and transfer of about one sweep), each cycle costs about $4 \times 8/7 \approx 4.6$ fine-grid sweeps, so the total is about 37 sweep-equivalents.

Gauss–Seidel: $-\ln\rho_{GS} \approx \pi^2h^2 = 1.49 \times 10^{-4}$, so $k \approx 18.4/1.49 \times 10^{-4} \approx 1.2 \times 10^5$ sweeps, more than 3000 times the multigrid work.

</details>

## References

- Saad, Y., *Iterative Methods for Sparse Linear Systems*, 2nd ed., SIAM, 2003.
- Briggs, W. L., Henson, V. E., and McCormick, S. F., *A Multigrid Tutorial*, 2nd ed., SIAM, 2000.
- Golub, G. H., and Van Loan, C. F., *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
- Hestenes, M. R., and Stiefel, E., "Methods of conjugate gradients for solving linear systems", *Journal of Research of the National Bureau of Standards* 49(6), 409–436, 1952.
- Saad, Y., and Schultz, M. H., "GMRES: a generalized minimal residual algorithm for solving nonsymmetric linear systems", *SIAM Journal on Scientific and Statistical Computing* 7(3), 856–869, 1986.
- van der Vorst, H. A., "Bi-CGSTAB: a fast and smoothly converging variant of Bi-CG for the solution of nonsymmetric linear systems", *SIAM Journal on Scientific and Statistical Computing* 13(2), 631–644, 1992.
- Brandt, A., "Multi-level adaptive solutions to boundary-value problems", *Mathematics of Computation* 31(138), 333–390, 1977.
- George, A., "Nested dissection of a regular finite element mesh", *SIAM Journal on Numerical Analysis* 10(2), 345–363, 1973.
- Young, D. M., "Iterative methods for solving partial difference equations of elliptic type", *Transactions of the American Mathematical Society* 76(1), 92–111, 1954.
- Patankar, S. V., *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
