## FINITE DIFFERENCE METHOD

The finite difference method is one of the most straightforward ways to transform partial differential equations into algebraic equations. It replaces continuous derivatives with difference quotients calculated at discrete grid points. Although conceptually simpler than other methods, finite difference schemes require a structured mesh and often perform best on regular geometries such as rectangular or cubical domains. It remains popular for problems like wave equations, heat equations, and fluid flow in simple domains, partly due to its relatively direct implementation and lower overhead in algorithmic complexity.

Below is a sketch of a one-dimensional domain divided into equally spaced points, each separated by a distance $h$. The variable of interest is stored at each node $x_i$.

```
   x_0     x_1     x_2     x_3     x_4     x_5
    |-------|-------|-------|-------|-------|
    <---- h ---->
```

If $u_i$ denotes the approximation of $u(x_i)$, one might write a central difference approximation for a first derivative at $x_2$ as

$$
\left. \frac{du}{dx}\right|_{x_2} \approx \frac{u_3 - u_1}{2h}
$$

### OVERVIEW AND BASIC APPROACH

The essence of the finite difference method lies in approximating derivatives by looking at the values of a function at discrete points. If we assume that we have a function $u(x)$ and a grid defined by points $x_0, x_1, x_2, \dots, x_N$, each spaced by a mesh size $h$, then the derivative of $u$ at $x_i$ can be approximated by a difference quotient. For example, a first-order derivative can be approximated by

$$
\frac{du}{dx}\Big|_{x_i} \approx \frac{u_{i+1} - u_i}{h}
$$

if we use a forward difference, or

$$
\frac{du}{dx}\Big|_{x_i} \approx \frac{u_{i} - u_{i-1}}{h}
$$

for a backward difference. A more accurate central difference uses

$$
\frac{du}{dx}\Big|_{x_i} \approx \frac{u_{i+1} - u_{i-1}}{2h}
$$

These approximations have different orders of accuracy and stability properties. Higher derivatives, such as the second derivative, can also be approximated by finite differences. For instance,

$$
\frac{d^2 u}{dx^2}\Big|_{x_i} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{h^2}
$$

By applying these difference formulas to partial differential equations, a continuous problem is turned into a system of algebraic equations involving nodal values $u_i$.

### CONCEPTS

1) Discretized Grid. The domain is covered by a uniform or non-uniform grid. Each grid point is associated with a coordinate $(x_i)$ in one dimension, $(x_i, y_j)$ in two dimensions, or $(x_i, y_j, z_k)$ in three dimensions.

2) Approximation of Derivatives. Continuous derivatives are replaced by finite difference operators, which are derived from Taylor series expansions. The choice of forward, backward, or central difference can affect both the accuracy and stability of the solution.

3) Boundary Conditions. The values of the unknown function or its derivatives at boundary points are often prescribed. These boundary conditions are woven into the difference equations at the points adjacent to the boundary.

4) Assembly of Algebraic Equations. Each interior point in the domain generates an equation relating $u_i$ (the solution at that point) to neighboring points. Collecting all these equations leads to a system of linear or nonlinear equations.

5) Solving the System. Methods range from direct factorization techniques (LU decomposition) for smaller problems to iterative methods like Jacobi, Gauss-Seidel, Conjugate Gradient, or multigrid for larger systems.

### DERIVATION IN A SIMPLE EXAMPLE

Consider the 1D heat equation

$$
\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}
$$

where $u = u(x,t)$ is the temperature, $\alpha$ is the thermal diffusivity, and $x \in [0, L]$. To use the finite difference method, discretize the spatial domain into $N+1$ points $x_0, x_1, \ldots, x_N$ with $`x_i = i\,h`$ and $h = \frac{L}{N}$. For time discretization, choose a time step $\Delta t$ and denote time levels by $`t^n = n\,\Delta t`$.

Let $u_i^n \approx u(x_i, t^n)$. A standard explicit finite difference approximation replaces the second spatial derivative by

```math
\frac{\partial^2 u}{\partial x^2}\Big|_{x_i, t^n} \approx
\frac{u_{i+1}^n - 2\,u_i^n + u_{i-1}^n}{h^2}
```

The time derivative is approximated using a forward difference:

$$
\frac{\partial u}{\partial t}\Big|_{x_i, t^n} \approx \frac{u_i^{n+1} - u_i^n}{\Delta t}
$$

Putting these together gives the discrete heat equation

```math
\frac{u_i^{n+1} - u_i^n}{\Delta t} = \alpha \,
\frac{u_{i+1}^n - 2\,u_i^n + u_{i-1}^n}{h^2}
```

Rearrange to solve for the new time level:

```math
u_i^{n+1} = u_i^n +
\frac{\alpha\,\Delta t}{h^2}\,\Big(u_{i+1}^n - 2\, u_i^n + u_{i-1}^n\Big)
```

Boundary conditions, such as $u(0, t) = u_L$ and $u(L, t) = u_R$, are enforced by setting $u_0^n = u_L$ and $u_N^n = u_R$ for all time levels $n$. This yields a straightforward update formula to march the solution in time.

### STABILITY AND COURANT-FRIEDRICHS-LEWY (CFL) CONDITION

When using explicit time-stepping schemes like the one above, there is often a restriction on the size of $\Delta t$ relative to $h$. This restriction is necessary for stability. In the example of the 1D heat equation, a common condition for stability is

```math
\Delta t \le \frac{h^2}{2\,\alpha}
```

More generally, partial differential equations with significant advection or wave-like behavior have stricter CFL-type constraints linking time step size to spatial grid spacing and wave speeds. If these conditions are not satisfied, the numerical solution might oscillate wildly and diverge from the actual solution.

### 2D AND 3D EXTENSIONS

In higher dimensions, the idea remains the same: approximate the derivatives by differences, but organize them according to a grid in multiple directions. For a 2D domain $(x,y)$, one might define

$$
u_{i,j}^n \approx u(x_i, y_j, t^n)
$$

and approximate partial derivatives like

```math
\frac{\partial^2 u}{\partial x^2}\Big|_{(x_i, y_j, t^n)} \approx
\frac{u_{i+1,j}^n - 2\,u_{i,j}^n + u_{i-1,j}^n}{h_x^2}
```

```math
\frac{\partial^2 u}{\partial y^2}\Big|_{(x_i, y_j, t^n)} \approx
\frac{u_{i,j+1}^n - 2\,u_{i,j}^n + u_{i,j-1}^n}{h_y^2}
```

The updates for time stepping or solving stationary equations follow a similar pattern, just applied across a 2D or 3D mesh.

Below is a basic depiction of a uniform grid in two dimensions. Each node $(i,j)$ references a point in the $(x,y)$ plane, and finite differences involve values at neighbors in both horizontal and vertical directions.

```
  (i-1,j+1)    (i,j+1)    (i+1,j+1)
       *--------*--------*
       |        |        |
       |        |        |
 (i-1,j)*--------*--------* (i+1,j)
       |        |        |
       |        |        |
       *--------*--------*
  (i-1,j-1)    (i,j-1)    (i+1,j-1)
```

### IMPLEMENTATION AND APPLICATIONS

Finite difference methods are typically easy to code. One starts with arrays representing the values of the solution and boundary conditions, then applies the chosen difference formulas to fill in the equations for interior points. This method is well-known for problems on rectangular domains in areas such as heat conduction, simple fluid flow, electromagnetic wave propagation, or wave equations in acoustics. In practice, it is often combined with iterative solvers, especially when the problem becomes large in multiple dimensions.

### COMMON PITFALLS

Finite difference solutions can exhibit instability or inaccuracy if the grid spacing or time step is chosen poorly. Convection-dominated problems may require special “upwinding” or artificial diffusion to avoid nonphysical oscillations. Non-uniform grids can make the approach more flexible, but also more challenging, since difference formulas must be modified to account for varying spacing. Handling complicated or curved boundaries with a purely structured grid can introduce errors or require coordinate transformations that complicate the implementation.

## Purpose in CFD

The Finite Difference Method (FDM) is one of the earliest and most intuitive discretization techniques. By replacing continuous derivatives with difference quotients on a structured grid, FDM converts PDEs such as the heat equation or wave equation into systems of algebraic equations. This note covers forward, backward, and central difference approximations, Taylor-series error analysis, the CFL stability condition, and extensions to 2-D/3-D grids. FDM is well-suited for problems on regular geometries and serves as the conceptual foundation for understanding other discretization methods.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Structured grid ($x_0, \dots, x_N$), mesh spacing $h$, time step $\Delta t$, thermal diffusivity $\alpha$, boundary conditions ($u_L$, $u_R$), initial condition $u(x,0)$ |
| **Outputs** | Nodal solution values $u_i^n$ at each grid point and time level, error estimates (truncation error order), stability limit $\Delta t \le h^2/(2\alpha)$ |

## Related Scripts

- [1D Heat and Wave Equation Simulations](../../../scripts/simulations/1d_heat_and_wave_equations/): solves the 1D heat equation with the implicit Crank–Nicolson scheme and the 1D wave equation with the explicit leapfrog scheme, animating both from the same initial Gaussian pulse.
- [2D Wave Equation Simulation](../../../scripts/simulations/2d_wave_simulation/): solves the 2D scalar wave equation on a square domain with an explicit leapfrog finite difference scheme and animates the result as a 3D surface.
- [Numerical vs. Exact Solution Comparison](../../../scripts/plots/numerical_vs_exact_solution/): solves $du/dx + u = 0$ with $u(0) = 1$ by a first-order finite-difference scheme and compares the result with the exact solution $u(x) = e^{-x}$, plotting the pointwise error.
- [Variation of Residual with Iteration](../../../scripts/plots/variation_of_residual/): solves the 1D Laplace equation with Gauss-Seidel iteration on a 100-point grid and plots the normalised residual against iteration number on a logarithmic scale.

## Exercises

**Exercise 1.** Use Taylor expansions of $u_{i+1}$ and $u_{i-1}$ about $x_i$ to show that the central difference $(u_{i+1} - u_{i-1})/(2h)$ has truncation error $O(h^2)$ and the forward difference $(u_{i+1} - u_i)/h$ has $O(h)$. Find the leading error terms.

<details>
<summary>Answer</summary>

$u_{i\pm1} = u_i \pm h u' + \frac{h^2}{2}u'' \pm \frac{h^3}{6}u''' + O(h^4)$. Therefore:

- Forward: $\dfrac{u_{i+1} - u_i}{h} = u' + \dfrac{h}{2}u'' + O(h^2)$, which is first order.
- Central: subtracting the two expansions, $\dfrac{u_{i+1} - u_{i-1}}{2h} = u' + \dfrac{h^2}{6}u''' + O(h^4)$, which is second order.

</details>

**Exercise 2.** For $u = \sin x$ at $x = 1$, compute the errors of the forward and central differences with $h = 0.1$ and $h = 0.05$, and check the observed orders of accuracy.

<details>
<summary>Answer</summary>

The exact derivative is $\cos 1 = 0.5403$.

| $h$ | forward error | central error |
| --- | --- | --- |
| 0.1 | $-4.29 \times 10^{-2}$ | $-9.00 \times 10^{-4}$ |
| 0.05 | $-2.13 \times 10^{-2}$ | $-2.25 \times 10^{-4}$ |

Halving $h$ divides the forward error by 2.02 and the central error by 4.00, confirming orders 1 and 2.

The signs match the leading terms from Exercise 1: $\frac{h}{2}u'' = -\frac{h}{2}\sin 1$ and $\frac{h^2}{6}u''' = -\frac{h^2}{6}\cos 1$.

</details>

**Exercise 3.** Apply the three-point second-derivative formula to $u = x^4$ at $x = 1$ with $h = 0.1$. Compare with the exact value, and show that the error equals $\frac{h^2}{12}u''''$ exactly for this function.

<details>
<summary>Answer</summary>

$(1.1^4 - 2 + 0.9^4)/0.01 = 12.02$, while the exact value is $u'' = 12x^2 = 12$.

The Taylor error series is $\frac{h^2}{12}u'''' + \frac{h^4}{360}u^{(6)} + \dots$. Here $u'''' = 24$ and all higher derivatives vanish, so the error is exactly $0.01 \times 24/12 = 0.02$.

</details>

**Exercise 4.** A steel rod ($\alpha = 1.2 \times 10^{-5}$ m²/s) of length $L = 0.1$ m is modelled with the explicit scheme using $N = 50$ intervals. (a) What is the largest stable time step, and how many steps does 60 s of simulated time take? (b) Repeat for $N = 100$. (c) What is the limit on a uniform 2D grid with $h_x = h_y = h$?

<details>
<summary>Answer</summary>

(a) $h = 0.002$ m and $\Delta t \le h^2/(2\alpha) = 4 \times 10^{-6}/(2.4 \times 10^{-5}) = 0.167$ s, so 60 s takes 360 steps.

(b) $h = 0.001$ m and $\Delta t \le 0.0417$ s, so 60 s takes 1440 steps. Doubling the resolution costs 8 times the work: twice the points and four times the steps.

(c) In 2D, $\Delta t \le \dfrac{1}{2\alpha(1/h_x^2 + 1/h_y^2)} = h^2/(4\alpha)$. For $h = 0.002$ m that is 0.083 s.

</details>

**Exercise 5.** Take $L = 1$, $N = 4$ ($h = 0.25$), $\alpha = 1$, boundary values $u_0 = u_4 = 0$ and interior initial values $(0.5, 1, 0.5)$. (a) Advance one step with $\Delta t = 0.025$. (b) For the mode $u_i^n = G^n e^{\mathrm{i} k x_i}$, von Neumann analysis gives the amplification factor $G = 1 - 4r\sin^2(kh/2)$ with $r = \alpha\Delta t/h^2$. Evaluate $|G|$ for the sawtooth mode $kh = \pi$ with $r = 0.4$ and $r = 0.6$, and explain the limit $r \le 1/2$.

<details>
<summary>Answer</summary>

(a) $r = 0.025/0.0625 = 0.4$. Then:

- $u_1^{1} = 0.5 + 0.4(1 - 1 + 0) = 0.5$
- $u_2^{1} = 1 + 0.4(0.5 - 2 + 0.5) = 0.6$
- $u_3^{1} = 0.5$ by symmetry.

(b) For $kh = \pi$, $G = 1 - 4r$:

- $r = 0.4$: $G = -0.6$ and $|G| < 1$, so the mode decays.
- $r = 0.6$: $G = -1.4$ and $|G| > 1$, so the sawtooth grows by 40% per step, flipping sign each time.

Requiring $|G| \le 1$ for every $k$ gives $4r \le 2$, that is $r \le 1/2$, which is the condition $\Delta t \le h^2/(2\alpha)$ quoted in the note.

</details>

## References

- R. J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems*, SIAM, 2007.
- J. C. Strikwerda, *Finite Difference Schemes and Partial Differential Equations*, 2nd ed., SIAM, 2004.
- K. W. Morton, D. F. Mayers, *Numerical Solution of Partial Differential Equations: An Introduction*, 2nd ed., Cambridge University Press, 2005.
