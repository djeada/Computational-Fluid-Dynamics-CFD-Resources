## Iterative Methods in Solving Nonlinear Terms and Matrix Inversion

In practical CFD problems, nonlinear terms in the governing equations lead to systems of nonlinear algebraic equations upon discretization. Because of their inherent nonlinearity and the vast size of the resulting matrices (especially for large-scale problems), direct inversion methods are often impractical. Instead, iterative techniques are used both to handle the nonlinear terms and to invert the corresponding matrices efficiently.

### Iteration in Nonlinear Terms

Need for Iterations:

- Handling Nonlinearity:  
Many governing equations in CFD include nonlinear terms—such as convective fluxes or quadratic source terms—which preclude direct analytical solutions. Iterative methods allow us to approximate the solution by starting with an initial guess and refining it until the solution stabilizes.

- Practical Considerations:  
Realistic CFD problems typically involve multiple coupled nonlinear terms. Iteration is a natural choice in these cases because it allows one to update the solution gradually, thereby making sure stability and convergence.

The idea is to start with an initial guess for the solution, use it to linearize the nonlinear terms, and then solve the linearized equations. This process is repeated until the difference between successive iterates falls below a prescribed tolerance.

### Discrete Equation System

Consider a finite-difference approximation on a four-point grid. For example, the discretized system for a nonlinear term can be written in matrix form as follows:

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

In this system:

- The diagonal entries contain terms like $1 + 2 \Delta x, u_{gi}$, where $u_{gi}$ represents the guess value at grid point $i$.
- The right-hand side reflects the nonlinear contributions, here expressed as $\Delta x, u_{gi}^2$.
This representation is obtained after applying a linearization (such as a Newton–Raphson type approach) to the original nonlinear finite-difference equations.

### Challenges with Large Systems

- Scale of the Problem:  
In real CFD applications, the number of grid points can range from thousands to millions. The associated matrices are therefore extremely large.

- Memory and Computational Cost:  
Directly inverting these large matrices requires substantial memory and computational resources. As a result, iterative matrix inversion methods are preferred over direct methods.

- Sparsity:  
Fortunately, the matrices derived from finite-difference or finite-volume discretizations are often sparse. Iterative methods are particularly well-suited for such sparse systems, as they do not require the storage or manipulation of the full matrix.

### Iterative Matrix Inversion

Rather than using a direct inversion method, an iterative scheme can be used to update the solution at each grid point. One common strategy is to rearrange the finite-difference approximation into an explicit update formula.

For grid point $i$, the rearranged equation might be written as:

$$u_i = \frac{u_{i-1} + \Delta x, u_{gi}^2}{1 + 2 \Delta x, u_{gi}}$$

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

To update $u_3$, if the updated value $u_4^{(m)}$ is not yet available during the $m^{th}$ iteration, one can temporarily use the initial guess $u_{g3}^{(1)}$:

$$u_3^{(m)} = \frac{u_2^{(m)} + \Delta x \left(u_{g3}^{(1)}\right)^2}{1 + 2 \Delta x, u_{g3}^{(1)}}$$

III. Update $u_2$:  

Finally, update $u_2$ using the most recent values from the previous grid point.

This process is repeated across all grid points and over successive iterations until the solution converges.

### Advantages of Iteration

- Approximate Solution with Reduced Memory Requirements:  
By using iterative methods, one avoids the direct inversion of large matrices, thereby reducing the memory overhead significantly. The iterative approach provides an approximate solution that is refined progressively.

- Combined Handling of Nonlinear Terms and Matrix Inversion:  
Iteration naturally combines the resolution of nonlinear terms (via linearization and successive updates) with the process of matrix inversion. This integration streamlines the computational process.

- Convergence to the Exact Solution:  
As iterations proceed, the guess values $u_{gi}$ converge to the true solution $u$. The error introduced by using initial guesses diminishes, and the approximate solution approaches the exact solution.

### Purposes of Iteration

I. Efficient Matrix Inversion:  

Iterative methods greatly reduce the memory requirements and computational cost associated with inverting large matrices, making them practical for high-resolution CFD problems.

II. Solving Nonlinear Equations:  

Nonlinear terms in the governing equations are inherently challenging. Iteration allows these terms to be linearized and solved repeatedly, making sure that the solution converges accurately.

### Strategy in Steady Problems

For steady-state problems, a common strategy is to use time marching to reach a steady solution:

- Time Marching Approach:  
The linearized form of the governing equations is solved at each time step, gradually "marching" the solution toward a steady state. Each time step uses the solution from the previous step as the new guess.

- Iterative Convergence:  
As the time steps progress, the solution iterates converge toward a steady state. In this context, the iterative process not only handles nonlinear terms and matrix inversion but also makes sure that the temporary behavior decays, leaving behind a stable, steady solution.
