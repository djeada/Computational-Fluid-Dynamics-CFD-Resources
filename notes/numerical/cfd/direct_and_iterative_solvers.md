## Iterative Methods in Solving Nonlinear Terms and Matrix Inversion

### Iteration in Nonlinear Terms
- **Need for Iterations**:
  - Nonlinear terms in governing equations require iterative methods to solve.
  - Practical CFD problems often involve iterations to handle these nonlinearities.

### Discrete Equation System
- **Finite-Difference Approximation**:
  - Discrete system from finite-difference approximation on a four-point grid is represented by:

$$
\begin{bmatrix}
1 & 0 & 0 & 0 \\
-1 & 1 + 2 \Delta x u_{g2} & 0 & 0 \\
0 & -1 & 1 + 2 \Delta x u_{g3} & 0 \\
0 & 0 & -1 & 1 + 2 \Delta x u_{g4}
\end{bmatrix}
\begin{bmatrix}
u_1 \\
u_2 \\
u_3 \\
u_4
\end{bmatrix}
$$

$$
\=
\begin{bmatrix}
1 \\
\Delta x u_{g2}^2 \\
\Delta x u_{g3}^2 \\
\Delta x u_{g4}^2
\end{bmatrix}
$$

### Challenges with Large Systems
- **Large Number of Grid Points**:
  - Practical problems involve thousands to millions of grid points.
  - Direct inversion of large matrices is memory-intensive and impractical.

### Iterative Matrix Inversion
- **Iterative Scheme**:
  - Instead of direct inversion, matrices are inverted using iterative schemes.
  - **Rearranged Finite-Difference Approximation** at grid point $i$:

$$
u_i = \frac{u_{i-1} + \Delta x u_{gi}^2}{1 + 2 \Delta x u_{gi}}
$$

  - Use guess values for neighboring points if current iteration values are unavailable.

### Example Iteration Process
- **Sweeping from Right to Left**:
  - Update $u_4$, then $u_3$, and finally $u_2$ in each iteration.
  - For the $m^{th}$ iteration, if $u_4^{(m)}$ is unavailable for updating $u_3^{(m)}$, use guess value $u_{g3}^{(1)}$:

$$
u_3^{(m)} = \frac{u_2^{(m)} + \Delta x (u_{g3}^{(1)})^2}{1 + 2 \Delta x u_{g3}^{(1)}}
$$

### Advantages of Iteration
- **Approximate Solution**:
  - Iteration provides an approximate solution, reducing memory requirements.
  - Combines handling of nonlinear terms with matrix inversion in a single process.

- **Convergence**:
  - As iterations converge ($u_g \to u$), the approximate solution tends towards the exact solution.
  - Error introduced by using guess values decreases as the solution refines.

### Purposes of Iteration
1. **Efficient Matrix Inversion**:
   - Greatly reduces memory requirements for large systems.

2. **Solving Nonlinear Equations**:
   - Necessary for handling nonlinear terms in governing equations.

### Strategy in Steady Problems
- **Time Marching to Steady Solution**:
  - Solve the linearized form of the governing equations.
  - "March" the solution in time until it converges to a steady value.
  - Each iteration level corresponds to a time step, with guess values from previous time steps.
