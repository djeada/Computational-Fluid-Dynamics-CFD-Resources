## FINITE ELEMENT METHOD

The finite element method is a widely used numerical approach for solving partial differential equations, and it is particularly well-suited for complicated geometries and varied boundary conditions. Many engineering and physics problems, such as structural analysis, heat transfer, and fluid flow, can be tackled effectively by breaking down a domain into smaller pieces known as elements and using polynomial-based approximations for unknown variables. This strategy makes it possible to handle irregular boundaries and curved shapes more gracefully than certain other numerical methods.

A simple one-dimensional domain can be split into elements, each with two or more nodes:

```
 Domain: x in [0, L]

     Node 0      Node 1      Node 2      Node 3
       |-----------|-----------|-----------|
        Element 1     Element 2   Element 3

If the domain is [0, L], each element might have length h, so:
 x_0 = 0, x_1 = h, x_2 = 2h, ...
```

In this example, each element is a line segment, and shape functions are typically polynomials of degree 1 (linear), 2 (quadratic), or higher. Linear shape functions in element $e$ will be zero outside that element and will vary linearly between the nodes inside that element.

For a two-dimensional domain, elements might be triangles or quadrilaterals:

```
Example of a triangular mesh:

  *-------*-------* 
  |\      |\      |
  | \     | \     |
  |  \    |  \    |
  *---\---*---\---*
  |\  |   |\  |   
  | \ |   | \ |   
  *---*---*---*  
```

- Nodes are at intersections of lines (the asterisks).
- Each triangle is a finite element, and shape functions are defined locally.

### OVERVIEW AND PHILOSOPHY

Finite element analysis focuses on approximating a solution by combining local shape functions that live on small subdomains, or elements, of the overall problem domain. Each element is typically associated with a set of nodes at which the unknown quantities are explicitly stored. The method often starts by writing the problem in its variational or weak form, which allows one to consider integrals of products involving the unknown function and specified test functions. These integrals make it possible to capture the behavior of the solution without requiring explicit finite-difference-style approximations of derivatives. Instead, integration by parts and standard function space arguments are used to make sure that the solution respects the underlying physics.

Mathematically speaking, if the differential equation is written in the form

$$
\mathcal{L}(u) = 0
$$

then the finite element method tries to solve the integral condition

```math
\int_{\Omega} w(x)\,\mathcal{L}(u)\, dx = 0
```

for all test functions $w$ in a suitable function space, sometimes with additional boundary terms if integration by parts is applied. The unknown $u$ and the test functions $w$ are expanded in terms of local basis functions that have support only over a small portion of the domain.

### CONCEPTS IN THE FINITE ELEMENT METHOD

1) Elements and Nodes. The domain is divided into subdomains called elements (line segments in 1D, triangles or quadrilaterals in 2D, tetrahedra or hexahedra in 3D, and so on). Each element has a few corner points or additional internal points called nodes. The values of the unknown solution are generally stored at these nodes.

2) Shape (Basis) Functions. Within each element, the unknown variable can be approximated by a combination of polynomials (or other basis functions) that take a value of 1 at one node and 0 at every other node. These shape functions make sure that the local approximation on each element matches nicely with neighboring elements at shared boundaries.

3) Weak (Variational) Form. The original differential equation is converted to an equivalent integral statement. This typically involves integration by parts to reduce the order of the derivatives that must be approximated, which helps produce stable and accurate numerical formulations.

4) Global Assembly. After choosing a polynomial approximation in each element, one obtains local element equations. These local equations are assembled into a large system of algebraic equations for the entire domain. The unknowns in this system are the nodal values of the solution.

5) Boundary Conditions. Dirichlet (prescribed value) or Neumann (prescribed flux/derivative) conditions are incorporated into the finite element formulation through modifications to the system of equations or through integrals in the weak form. Accurately implementing boundary conditions is important for a well-posed problem.

6) Solving the System. Once the global system is assembled, standard linear or nonlinear solvers can be used. For large-scale problems, iterative methods such as Conjugate Gradient, GMRES, or multigrid approaches might be necessary.

### STEPS IN THE FINITE ELEMENT METHOD

1) Derive the Weak Form. Consider a boundary value problem like

$$
-\frac{d}{dx} \Big(p(x) \frac{du}{dx} \Big) = f(x), \quad x \in [0,L]
$$

with boundary conditions on $u$. The weak form is obtained by multiplying by a test function $w(x)$ and integrating over $[0,L]$:

```math
\int_0^L w(x) \Big(-\frac{d}{dx}\big(p(x)\, u'(x) \big) \Big) \, dx = \int_0^L w(x)\,
f(x)\, dx
```

By applying integration by parts, one obtains

```math
\int_0^L p(x)\, w'(x)\, u'(x)\, dx -
\Big[\underbrace{p(x)\,w(x)\,u'(x)}_{\text{boundary term}} \Big]_0^L = \int_0^L w(x)\,
f(x)\, dx
```

and boundary conditions help determine how to handle the boundary term.

2) Discretize the Domain. Partition $[0,L]$ into elements of size $h_i$. Suppose there are $N$ elements, each with (at least) two nodes.

3) Choose Shape Functions. Let each element have local shape functions $\phi_j^e(x)$, defined only within element $e$. Over the entire domain, the approximate solution $u_h$ is

```math
u_h(x) = \sum_{i=1}^{\text{TotalNodes}} U_i\,\Phi_i(x)
```

where each global basis function $\Phi_i$ is built from the local shape functions. The coefficient $U_i$ represents the unknown value at node $i$.

4) Form Local Stiffness Matrices and Load Vectors. For each element $e$, define

```math
K^e_{ij} = \int_{x_{e,\text{start}}}^{x_{e,\text{end}}}
p(x)\,\phi_i^e{}'(x)\,\phi_j^e{}'(x)\, dx, \quad
F^e_{i} = \int_{x_{e,\text{start}}}^{x_{e,\text{end}}} \phi_i^e(x)\, f(x)\, dx
```

These integrals capture how each pair of shape functions interacts under the problem’s differential operator and forcing term.

5) Assemble the Global System. The local element stiffness matrices $K^e$ and load vectors $F^e$ are added into global matrices $K$ and global vectors $F$. This leads to a large system of equations

```math
K\, U = F
```

where $U$ is the vector of unknown nodal values.

6) Apply Boundary Conditions. Prescribed displacements (Dirichlet) are incorporated by fixing nodal values in $U$. Prescribed fluxes (Neumann) appear as boundary integrals in the load vector. Other boundary conditions, like Robin or mixed types, can also be handled in the weak form with additional surface integrals.

7) Solve the System. Use direct solvers (e.g., LU decomposition) for small or moderate problems. Use iterative solvers (e.g., Conjugate Gradient, GMRES) with suitable preconditioners for larger systems.

### EXAMPLE: 1D POISSON EQUATION

A classic application in one dimension is solving

$$
-\frac{d^2 u}{dx^2} = f(x), \quad x \in [0,1]
$$

with boundary conditions $u(0) = 0$ and $u(1) = 0$ for simplicity. The weak form is found by multiplying by a test function $w(x)$ and integrating:

```math
\int_0^1 w(x) \Big(-\frac{d^2 u}{dx^2} \Big)\, dx = \int_0^1 w(x)\, f(x)\, dx
```

Integration by parts yields

```math
\int_0^1 w'(x)\, u'(x)\, dx = \int_0^1 w(x)\, f(x)\, dx
```

assuming homogeneous Dirichlet boundary conditions eliminate boundary terms. The domain is divided into elements $[x_{i-1}, x_i]$ for $i=1,\dots,N$. On each element, approximate $u$ by a linear combination of local shape functions. Compute the local stiffness matrices and load vectors, and assemble them into

```math
K\, U = F
```

where $K$ is an $(N+1)\times(N+1)$ matrix (one row per node, before boundary conditions are applied), $U$ is the vector of nodal unknowns, and $F$ is the load vector. After applying the boundary conditions $u(0)=0$ and $u(1)=0$, the resulting system can be solved for the interior nodes.

### IMPLEMENTATION AND APPLICATIONS

Many commercial and open-source software packages rely on finite element techniques. Packages such as ANSYS, COMSOL, and Abaqus are widely used in industry for structural and thermal analyses. Other open-source codes like deal.II and FEniCS give researchers and engineers the flexibility to write custom finite element solvers for specialized problems. The scope of applications is vast, including elasticity, fluid-structure interaction, electromagnetics, and more. The overarching idea always remains the same: local polynomial approximations over small elements, assembled into a global system that captures the physics of the problem.

### POTENTIAL PITFALLS

FEM can become computationally expensive when the mesh is refined or the polynomial order is increased, though adaptive mesh refinement strategies can selectively refine only the regions where the solution has large gradients or singularities. Numerical instabilities may arise if the problem is poorly posed or if the discretization scheme does not capture key features, especially in convection-dominated flows where specialized stabilization methods might be needed. Implementing boundary conditions requires careful consideration of the problem’s physical meaning. Also, ensuring that the chosen polynomial order and element shape align with the desired accuracy is necessary.

## Purpose in CFD

The Finite Element Method (FEM) divides the domain into elements (triangles, quadrilaterals, tetrahedra, etc.) and approximates the solution with piecewise polynomial shape functions. By formulating the problem in its weak (variational) form, FEM naturally handles complex geometries, curved boundaries, and mixed boundary conditions. This note explains the core concepts—elements, nodes, shape functions, weak form, global assembly, and boundary condition application—and walks through a 1-D Poisson equation example.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Domain $\Omega$, element mesh, polynomial degree, forcing function $f(x)$, boundary conditions (Dirichlet, Neumann), material properties $p(x)$ |
| **Outputs** | Nodal solution vector $U$, global stiffness matrix $K$, load vector $F$, approximate solution $u_h(x)$ |

## Related Scripts

There are no dedicated FEM simulation scripts in this repository. For hands-on FEM implementations, consider open-source packages such as [FEniCS](https://fenicsproject.org/) or [deal.II](https://www.dealii.org/). The POD and ROM scripts listed under those notes use solution snapshots that could originate from an FEM solver.

## Exercises

**Exercise 1.** On an element $[x_a, x_b]$ of length $h$, the linear shape functions are $\phi_1 = (x_b - x)/h$ and $\phi_2 = (x - x_a)/h$. Compute the element stiffness matrix $K^e$ for $p(x) = 1$ and the load vector $F^e$ for a constant $f$.

<details>
<summary>Answer</summary>

$\phi_1' = -1/h$ and $\phi_2' = 1/h$, so $`K^e_{ij} = \int_{x_a}^{x_b}\phi_i'\phi_j'\,dx`$ gives:

- diagonal entries $K^e_{11} = K^e_{22} = 1/h$
- off-diagonal entries $K^e_{12} = K^e_{21} = -1/h$

Since $`\int\phi_i\,dx = h/2`$, the load vector is $F^e_1 = F^e_2 = fh/2$.

</details>

**Exercise 2.** Solve $-u'' = 1$ on $[0,1]$ with $u(0) = u(1) = 0$ using three equal linear elements ($h = 1/3$). Assemble the global $4 \times 4$ system, apply the boundary conditions, solve for the interior nodal values, and compare with the exact solution $u = x(1 - x)/2$.

<details>
<summary>Answer</summary>

Adding the element contributions (each $1/h = 3$) gives a tridiagonal global stiffness matrix:

- rows 0 and 3: $3, -3$
- rows 1 and 2: $-3, 6, -3$

The global load vector is $F = (1/6, 1/3, 1/3, 1/6)$.

Deleting the rows and columns of the Dirichlet nodes 0 and 3 leaves

```math
6U_1 - 3U_2 = \frac{1}{3},
\qquad - 3U_1 + 6U_2 = \frac{1}{3}
```

so $U_1 = U_2 = 1/9$.

The exact value is $u(1/3) = \frac{1}{3}\cdot\frac{2}{3}/2 = 1/9$. The nodal values are exact, a known property of linear elements for 1D problems of this form, while between the nodes the approximation is piecewise linear.

</details>

**Exercise 3.** For a variable coefficient $p(x) = 1 + x$, compute $K^e$ for the linear element $[0.5, 1]$.

<details>
<summary>Answer</summary>

The shape-function derivatives are $\pm 1/h$ with $h = 0.5$, so every entry equals $`\pm\frac{1}{h^2}\int_{0.5}^{1}(1 + x)\,dx`$. The integral is $0.5 + (1 - 0.25)/2 = 0.875$, and dividing by $h^2 = 0.25$ gives 3.5.

$K^e$ has diagonal entries $3.5$ and off-diagonal entries $-3.5$. For linear elements, $K^e$ is just the constant-coefficient matrix multiplied by the average of $p$ over the element ($1.75/0.5 = 3.5$).

</details>

**Exercise 4.** Solve $-u'' = 0$ on $[0,1]$ with $u(0) = 0$ and the Neumann condition $u'(1) = g$, using two linear elements. Show how the boundary term in the weak form enters the load vector, and compare the result with the exact solution.

<details>
<summary>Answer</summary>

The weak form is $`\int_0^1 w'u'\,dx - [w u']_0^1 = 0`$. Since $w(0) = 0$ at the Dirichlet node and $u'(1) = g$, the boundary term becomes $`g\,w(1)`$ and adds $g$ to the load entry of the last node.

With $h = 0.5$ (so $1/h = 2$), deleting node 0 leaves

```math
4U_1 - 2U_2 = 0,
\qquad - 2U_1 + 2U_2 = g
```

so $U_1 = g/2$ and $U_2 = g$. This matches the exact solution $u = gx$.

The Neumann condition was never imposed directly on $U$. It entered naturally through the load vector.

</details>

## References

- T. J. R. Hughes, *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*, Prentice-Hall, 1987.
- G. Strang, G. J. Fix, *An Analysis of the Finite Element Method*, Prentice-Hall, 1973.
- O. C. Zienkiewicz, R. L. Taylor, J. Z. Zhu, *The Finite Element Method: Its Basis and Fundamentals*, 7th ed., Butterworth-Heinemann, 2013.
