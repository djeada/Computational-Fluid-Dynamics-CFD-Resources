## Iterative Methods in Solving Nonlinear Terms and Matrix Inversion

In practical CFD problems, nonlinear terms in the governing equations lead to systems of nonlinear algebraic equations upon discretization. Because of their inherent nonlinearity and the vast size of the resulting matrices (especially for large-scale problems), direct inversion methods are often impractical. Instead, iterative techniques are used both to handle the nonlinear terms and to invert the corresponding matrices efficiently.

### Iteration in Nonlinear Terms

Need for Iterations:

- Handling Nonlinearity:\
  Many governing equations in CFD include nonlinear terms—such as convective fluxes or quadratic source terms—which preclude direct analytical solutions. Iterative methods allow us to approximate the solution by starting with an initial guess and refining it until the solution stabilizes.

- Practical Considerations:\
  Realistic CFD problems typically involve multiple coupled nonlinear terms. Iteration is a natural choice in these cases because it allows one to update the solution gradually, thereby making sure stability and convergence.

The idea is to start with an initial guess for the solution, use it to linearize the nonlinear terms, and then solve the linearized equations. This process is repeated until the difference between successive iterates falls below a prescribed tolerance.

### Discrete Equation System

Consider a finite-difference approximation on a four-point grid. For example, the discretized system for a nonlinear term can be written in matrix form as follows:

$$
\begin{bmatrix}
1 & 0 & 0 & 0 \\
-1 & 1 + 2 \Delta x\, u_{g2} & 0 & 0 \\
0 & -1 & 1 + 2 \Delta x\, u_{g3} & 0 \\
0 & 0 & -1 & 1 + 2 \Delta x\, u_{g4}
\end{bmatrix}
\begin{bmatrix}
u_1 \\
u_2 \\
u_3 \\
u_4
\end{bmatrix} =
\begin{bmatrix}
1 \\
\Delta x\, u_{g2}^2 \\
\Delta x\, u_{g3}^2 \\
\Delta x\, u_{g4}^2
\end{bmatrix}
$$

In this system:

- The diagonal entries contain terms like $1 + 2 \Delta x\, u_{gi}$, where $u_{gi}$ represents the guess value at grid point $i$.
- The right-hand side reflects the nonlinear contributions, here expressed as $\Delta x\, u_{gi}^2$.
  This representation is obtained after applying a linearization (such as a Newton–Raphson type approach) to the original nonlinear finite-difference equations.

### Challenges with Large Systems

- Scale of the Problem:\
  In real CFD applications, the number of grid points can range from thousands to millions. The associated matrices are therefore extremely large.

- Memory and Computational Cost:\
  Directly inverting these large matrices requires substantial memory and computational resources. As a result, iterative matrix inversion methods are preferred over direct methods.

- Sparsity:\
  Fortunately, the matrices derived from finite-difference or finite-volume discretizations are often sparse. Iterative methods are particularly well-suited for such sparse systems, as they do not require the storage or manipulation of the full matrix.

### Iterative Matrix Inversion

Rather than using a direct inversion method, an iterative scheme can be used to update the solution at each grid point. One common strategy is to rearrange the finite-difference approximation into an explicit update formula.

For grid point $i$, the rearranged equation might be written as:

$$
u_i = \frac{u_{i-1} + \Delta x\, u_{gi}^2}{1 + 2 \Delta x\, u_{gi}}
$$

In this expression:

- $u_i$ is the updated solution at the current grid point.
- $u_{gi}$ is the guess value used to linearize the nonlinear term $u_i^2$.
- $\Delta x$ is the grid spacing.
  If the current iteration values for neighboring points are not yet available, the method uses available guess values to carry on the update.

### Example Iteration Process

A common practical approach is to perform a sweep through the grid points in a specific order. For example, one might update the solution from right to left:

I. Update $u_4$:

Start at the right-most grid point and compute $u_4$ using the rearranged formula.

II. Update $u_3$:

To update $u_3$, the neighbouring value $u_2^{(m)}$ has not yet been computed in the $m^{th}$ sweep (the sweep runs right to left), so its guess value $u_{g2}$ from the previous sweep is used in its place, together with the guess $u_{g3}$ for the linearization:

$$
u_3^{(m)} = \frac{u_{g2} + \Delta x\, u_{g3}^2}{1 + 2 \Delta x\, u_{g3}}
$$

III. Update $u_2$:

Finally, update $u_2$ using the most recent values from the previous grid point.

This process is repeated across all grid points and over successive iterations until the solution converges.

### Advantages of Iteration

- Approximate Solution with Reduced Memory Requirements:\
  By using iterative methods, one avoids the direct inversion of large matrices, thereby reducing the memory overhead significantly. The iterative approach provides an approximate solution that is refined progressively.

- Combined Handling of Nonlinear Terms and Matrix Inversion:\
  Iteration naturally combines the resolution of nonlinear terms (via linearization and successive updates) with the process of matrix inversion. This integration streamlines the computational process.

- Convergence to the Exact Solution:\
  As iterations proceed, the guess values $u_{gi}$ converge to the true solution $u$. The error introduced by using initial guesses diminishes, and the approximate solution approaches the exact solution.

### Purposes of Iteration

I. Efficient Matrix Inversion:

Iterative methods greatly reduce the memory requirements and computational cost associated with inverting large matrices, making them practical for high-resolution CFD problems.

II. Solving Nonlinear Equations:

Nonlinear terms in the governing equations are inherently challenging. Iteration allows these terms to be linearized and solved repeatedly, making sure that the solution converges accurately.

### Strategy in Steady Problems

For steady-state problems, a common strategy is to use time marching to reach a steady solution:

- Time Marching Approach:\
  The linearized form of the governing equations is solved at each time step, gradually "marching" the solution toward a steady state. Each time step uses the solution from the previous step as the new guess.

- Iterative Convergence:\
  As the time steps progress, the solution iterates converge toward a steady state. In this context, the iterative process not only handles nonlinear terms and matrix inversion but also makes sure that the temporary behavior decays, leaving behind a stable, steady solution.

## Purpose in CFD

After discretization the governing equations reduce to a large algebraic system $Ax = b$. This note explains **direct solvers** (Gaussian elimination, LU decomposition) suitable for small systems, and **iterative solvers** (Conjugate Gradient, GMRES) preferred for the large, sparse matrices typical of CFD. It also covers parallelization strategies and the role of grid convergence in verifying the discrete solution.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Coefficient matrix $A$ (sparse), right-hand-side vector $b$, initial guess $u_g$, convergence tolerance, grid spacing $\Delta x$ |
| **Outputs** | Solution vector $x$ (nodal values of velocity, pressure, etc.), residual history, comparison with exact solutions |

## Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Grid Convergence Comparison](../../../scripts/plots/comparing_grid_convergence/): illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$.
- [Laplace Equation Maze Solver](../../../scripts/simulations/laplace_equation_maze_solver/): solves a randomly generated maze by computing a potential that satisfies Laplace's equation in the maze passages and then following the potential uphill from the entrance to the exit.
- [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/): solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error.
- [Simplified Real-Time Fluid Dynamics Simulator](../../../scripts/simulations/simplified_real_time_fluid_dynamics_simulator/): is an interactive 2D smoke simulation that uses Jos Stam's Stable Fluids algorithm (1999) to approximate the incompressible Navier-Stokes equations fast enough to run in real time in a Pygame window.
- [Variation of Residual with Iteration](../../../scripts/plots/variation_of_residual/): solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale.

## Exercises

**Exercise 1.** With all guesses $u_{gi} = 1$ and $\Delta x = 1/3$, solve the $4 \times 4$ linearized system of this note directly. It is lower triangular, so use forward substitution. Compare the result with one right-to-left sweep of the iterative update, which uses the guess $u_{g,i-1}$ for the neighbour.

<details>
<summary>Answer</summary>

Forward substitution: $u_1 = 1$ and $u_i = (u_{i-1} + \Delta x)/(1 + 2\Delta x)$ with $1 + 2\Delta x = 5/3$.

$u_2 = (4/3)/(5/3) = 0.8$, $u_3 = (0.8 + 1/3)/(5/3) = 0.68$, $u_4 = (0.68 + 1/3)/(5/3) = 0.608$.

The right-to-left sweep uses $u_{g,i-1} = 1$ for every point, so $u_2 = u_3 = u_4 = 0.8$.

Solving the linear system exactly (left to right, using updated neighbours) moves information across the whole grid in one pass. The sweep in the note needs several passes to carry the boundary value to $u_4$. Both still have to be repeated to resolve the nonlinearity.

</details>

**Exercise 2.** Apply two iterations of Jacobi and of Gauss–Seidel, both starting from $\mathbf{x} = 0$, to $A\mathbf{x} = \mathbf{b}$ with $A = \begin{bmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{bmatrix}$ and $\mathbf{b} = (2, 4, 10)$. The exact solution is $(1, 2, 3)$.

<details>
<summary>Answer</summary>

Jacobi (all updates use the previous iterate):

- $\mathbf{x}^{(1)} = (0.5, 1, 2.5)$
- $\mathbf{x}^{(2)} = (0.75, 1.75, 2.75)$

Gauss–Seidel (each update uses the newest values):

- $\mathbf{x}^{(1)} = (0.5, 1.125, 2.78125)$
- $\mathbf{x}^{(2)} = (0.78125, 1.890625, 2.97265625)$

After two iterations Gauss–Seidel is noticeably closer to $(1, 2, 3)$.

</details>

**Exercise 3.** For the matrix of Exercise 2 the Jacobi iteration matrix has spectral radius $\rho_J = \tfrac{1}{2}\cos(\pi/4)$, and for Gauss–Seidel $\rho_{GS} = \rho_J^2$. How many iterations does each need to reduce the error by $10^6$? For a 1D Poisson problem with grid spacing $h = 0.01$, $\rho_J = \cos(\pi h)$. How many Jacobi iterations are needed there?

<details>
<summary>Answer</summary>

$\rho_J \approx 0.354$ and $\rho_{GS} = 0.125$. The iteration count is $k = \ln(10^{-6})/\ln\rho$.

- Jacobi: $k \approx 13.3$, so 14 iterations.
- Gauss–Seidel: $k \approx 6.6$, so 7 iterations.

For Poisson with $h = 0.01$: $\rho_J = \cos(0.0314) \approx 0.99951$, so $k \approx 28{,}000$.

Strongly diagonally dominant matrices converge fast. Discretized elliptic operators have $\rho \to 1$ as the grid is refined, which is why CFD codes use Krylov methods with preconditioning, or multigrid.

</details>

**Exercise 4.** Estimate the time and memory to solve a dense system with $n = 10^5$ unknowns by LU decomposition (about $\tfrac{2}{3}n^3$ floating-point operations) on hardware doing $10^{10}$ operations per second. Compare with 1000 iterations of an iterative method on a sparse matrix with 5 nonzeros per row, counting only the matrix–vector products.

<details>
<summary>Answer</summary>

LU: $\tfrac{2}{3}(10^5)^3 \approx 6.7 \times 10^{14}$ operations, about $6.7 \times 10^4$ s or 18.5 h. The matrix alone needs $10^{10} \times 8$ bytes $= 80$ GB.

Sparse iterative: $5 \times 10^5$ operations per product, times 1000 iterations, is $5 \times 10^8$ operations, about 0.05 s of arithmetic (real timings are dominated by memory access, but the gap is still several orders of magnitude). Memory is a few megabytes.

</details>

## References

- Saad, Y., *Iterative Methods for Sparse Linear Systems*, 2nd ed., SIAM, 2003.
- Golub, G. H., & Van Loan, C. F., *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
- Trefethen, L. N., & Bau, D., *Numerical Linear Algebra*, SIAM, 1997.
- Kelley, C. T., *Iterative Methods for Linear and Nonlinear Equations*, SIAM, 1995.
- Versteeg, H. K., & Malalasekera, W., *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Education, 2007.
