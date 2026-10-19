## FINITE VOLUME METHOD IN CFD

The finite volume method is a powerful technique for solving partial differential equations, especially those arising in fluid dynamics. It stands out because it directly enforces the conservation of physical quantities such as mass, momentum, and energy over small regions of a computational domain. Each region is typically referred to as a control volume or cell. The approach naturally respects integral balances and is well-suited for complicated flow problems where conservation properties are important.

Below is a simple diagram showing a 1D domain subdivided into control volumes. Each cell is bounded by interfaces at $x_{i-1/2}$ and $x_{i+1/2}$. The unknown quantity $u$ is typically stored at the cell center $x_i$.

```
      x_{0}   x_{1}   x_{2}   x_{3}        x_{i-1}   x_{i}    x_{i+1}
        |-------|-------|-------|   ...       |-------|--------|
          CV1     CV2     CV3                  CV_{i}  CV_{i+1}

Cell centers at x_0, x_1, x_2, ...
Interfaces at x_{1/2}, x_{3/2}, ...
```

Each arrow at the interfaces represents a possible flux moving in or out of a cell. The finite volume method revolves around estimating these fluxes in a way that maintains the balance of quantities in every control volume.

### OVERVIEW OF COMMON NUMERICAL METHODS

It can be helpful to compare the finite volume method with several other widely used techniques for solving partial differential equations. Each method has its own strengths, and the choice often depends on the nature of the problem and the geometry of the domain.

1) Finite Difference Methods (FDM). This method usually approximates derivatives by taking differences of values at discrete grid points. Finite difference techniques excel in problems with relatively simple geometries and boundary conditions. Their implementation can be straightforward, but they may face difficulties on unstructured meshes or complicated domains.

2) Finite Volume Methods (FVM). This method divides the domain into control volumes and applies the integral form of the governing equations over each volume. By computing fluxes of conserved quantities across the boundaries of each volume, finite volume approaches preserve the integral conservation laws exactly in discrete form. This property makes them very popular in fluid dynamics codes where conservation of mass, momentum, and energy is important.

3) Spectral Methods. These methods represent the solution as a sum of global basis functions, often polynomials or trigonometric functions such as Fourier series. The accuracy can be very high for smooth problems, but spectral methods can be more challenging to apply if the problem or the domain is irregular.

4) Finite Element Methods (FEM). This approach represents the solution using piecewise polynomials defined on subdivided elements of the domain. Local polynomial bases and variational formulations make it a flexible technique for handling complicated geometries, although the method involves more algebraic machinery compared to finite differences or finite volumes.

### PRINCIPLES OF THE FINITE VOLUME METHOD

The finite volume method begins with the integral form of the partial differential equations describing the physics of interest. The domain is split into small, non-overlapping cells. Each cell is sometimes called a control volume, and each control volume is associated with a representative point where the unknown quantities are stored. The integral (or weak) form of the equations is then approximated over each cell, which turns the continuous PDE problem into a set of algebraic equations that can be solved on a computer.

When thinking about the finite volume method, it helps to picture the physical balances of mass, momentum, or energy over a small region. The key quantity is the flux across each cell boundary, since flux represents how much of a particular quantity flows in or out of the cell. By ensuring that the net flux into a cell equals the cell’s rate of change of the conserved quantity, the method enforces local conservation. This local conservation, in turn, guarantees that global conservation is also maintained.

The resulting algebraic equations involve the values of unknowns at the cell centers (or cell vertices, depending on the variant) and the fluxes through shared boundaries. The fluxes are often computed or approximated using interpolation methods that depend on the surrounding cell values, and special care is taken to capture flow phenomena such as shocks or large gradients accurately.

### STEPS IN THE FINITE VOLUME METHOD

1) Select the geometry and generate the grid. The domain is divided into a collection of non-overlapping control volumes. The shape of these volumes can vary (structured or unstructured meshes), but each volume must cover a distinct region without overlapping its neighbors.

2) Integrate the governing equations over each control volume. The starting point is usually a conservation law in differential form, such as

$$
\frac{\partial \phi}{\partial t} + \nabla \cdot \mathbf{F} = 0
$$

where $\phi$ might be mass density or another conserved quantity, and $\mathbf{F}$ is the flux vector. By integrating over a control volume $V_i$, one obtains

```math
\int_{V_i} \frac{\partial \phi}{\partial t}\, dV + \int_{\partial V_i} \mathbf{F} \cdot
\mathbf{n} \, dS = 0
```

where $\partial V_i$ denotes the boundary (surface) of the control volume and $\mathbf{n}$ is the outward-facing unit normal.

4) Apply the divergence theorem. Converting volume integrals of $\nabla \cdot \mathbf{F}$ into surface integrals of $\mathbf{F} \cdot \mathbf{n}$ helps emphasize that the necessary contributions come from the fluxes crossing each control volume boundary.

5) Approximate the fluxes at each cell boundary. Various interpolation and differencing schemes can be used to find the value of $\phi$ and its gradients at the interfaces. Choices such as central differencing, upwind schemes, or more advanced flux limiters can significantly affect accuracy and numerical stability.

6) Assemble the discretized equations. The flux balances for each control volume yield an algebraic equation linking the unknown $\phi_i$ to its neighbors. Collecting the equations for all cells produces a large system of equations to be solved.

7) Impose boundary conditions. The flux calculation at domain boundaries often depends on known values or fluxes specified by the physics of the problem. These boundary conditions modify the equations in the outermost cells.

8) Solve the system of equations. Typical solution methods range from basic iterative techniques like Gauss-Seidel to more sophisticated approaches such as the Conjugate Gradient or multigrid methods, depending on the structure of the equations.

### EXAMPLE: 1D CONVECTION-DIFFUSION EQUATION

It can be insightful to see how the finite volume steps come together in a simple 1D setting. Consider the convection-diffusion equation,

$$
\frac{\partial u}{\partial t} + v \frac{\partial u}{\partial x} = D
\frac{\partial^2 u}{\partial x^2}
$$

where $u = u(x,t)$ might represent a scalar quantity such as temperature, $v$ is a constant flow velocity, and $D$ is the diffusion coefficient.

Suppose the domain $x \in [0, L]$ is subdivided into $N$ control volumes, each centered at $x_i$, with edges at $x_{i-1/2}$ and $x_{i+1/2}$. Integrating the equation over the control volume from $x_{i-1/2}$ to $x_{i+1/2}$ and applying the divergence theorem gives

```math
\int_{x_{i-1/2}}^{x_{i+1/2}} \frac{\partial u}{\partial t}\, dx +
\int_{x_{i-1/2}}^{x_{i+1/2}} v \frac{\partial u}{\partial x}\,
dx = \int_{x_{i-1/2}}^{x_{i+1/2}} D \frac{\partial^2 u}{\partial x^2}\, dx
```

The middle term involving convection can be expressed as the net flux of $u$ through the boundaries:

```math
\int_{x_{i-1/2}}^{x_{i+1/2}} v \frac{\partial u}{\partial x}\, dx = v\, u
\Big|_{x_{i+1/2}} - v\, u \Big|_{x_{i-1/2}}
```

and similarly for the diffusion term by considering its gradient at each boundary. After approximating $u$ and its derivatives or fluxes at $x_{i-1/2}$ and $x_{i+1/2}$ through suitable interpolation schemes, one obtains a discretized equation relating $u_i$ (the cell-average or center value in cell $i$) to its neighboring values. The complete set of discrete equations for $i = 1,\dots,N$ can then be solved at each time step, ensuring that each control volume properly accounts for convection and diffusion fluxes across its boundaries.

### ADDITIONAL DIAGRAM FOR CONTROL VOLUME FLUXES

A typical 1D control volume approach for a cell $i$ is illustrated below. The flux $F_{i+1/2}$ exits cell $i$ and enters cell $i+1$. Meanwhile, flux $F_{i-1/2}$ arrives from cell $i-1$. The net rate of change in cell $i$ equals the difference between these fluxes plus any source terms that may appear.

```
 Cell i-1     Cell i     Cell i+1
    |---|-------|-------|---|
       x_{i-1/2}   x_{i+1/2}
           --> F_{i-1/2}
                    <--
               Net Flow
                    -->
                 F_{i+1/2}
```

### IMPLEMENTATION AND APPLICATIONS

Many commercial and open-source CFD software packages, such as ANSYS Fluent and OpenFOAM, rely heavily on the finite volume method. These codes include sophisticated mesh generation tools for complicated geometries and provide a range of flux calculation schemes tailored to different types of flow. Implementation details can vary, but the overarching theme remains the focus on local conservation via surface (or face) fluxes.

The method works well in complicated flow scenarios, including compressible flows, reacting flows, and multiphase problems. It can handle irregular meshes and boundary-fitted coordinates. One of its major advantages is the direct interpretation of solution variables in terms of integral balances, which makes physical conservation more intuitive and strong.

### POTENTIAL PITFALLS

Numerical instabilities can arise if the chosen interpolation and time-stepping schemes are not appropriate for the type of flow or the grid spacing. High-speed flows often benefit from upwind and flux-limiter schemes that avoid spurious oscillations near shocks. Diffusion-dominated problems can be relatively forgiving, but convection-dominated scenarios may demand careful scheme selection to maintain stability and accuracy. Boundary conditions also play a key role in determining the quality of the final solution, so implementing them consistently is important.

## Purpose in CFD

The Finite Volume Method (FVM) is the dominant discretization technique in industrial CFD codes (OpenFOAM, ANSYS Fluent). It integrates conservation laws over small control volumes and computes fluxes at cell faces, guaranteeing local and global conservation of mass, momentum, and energy. This note explains control-volume concepts, the divergence theorem link, flux approximation, and the resulting algebraic system, using the 1-D convection-diffusion equation as an example.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Control-volume mesh (structured or unstructured), conservation law $\partial\phi/\partial t + \nabla\cdot\mathbf{F}=0$, flux interpolation scheme, boundary conditions, diffusion coefficient $D$, velocity $v$ |
| **Outputs** | Cell-averaged values $\phi_i$, face fluxes $F_{i\pm 1/2}$, assembled algebraic system, converged field solution |

## Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Raindrops on a Pond: Shallow-Water Ripples](../../../scripts/simulations/shallow_water_ripples/): simulates raindrops falling on a square basin of still water by solving the 2D shallow-water equations with a conservative finite-volume scheme, and animates the free surface as shaded relief.

## Exercises

**Exercise 1.** Explain why summing the finite-volume equations over all cells of a 1D domain gives a statement of global conservation that involves only the boundary fluxes.

<details>
<summary>Answer</summary>

Cell $i$ gains $F_{i-1/2}$ and loses $F_{i+1/2}$. The same numerical flux $F_{i+1/2}$ is the gain of cell $i+1$. When all cells are summed, every interior flux appears once with each sign and cancels, leaving

```math
\frac{d}{dt}\sum_i u_i\,\Delta x = F_{1/2} - F_{N+1/2}
```

This holds exactly for any flux formula, provided both neighbours use the same face flux.

</details>

**Exercise 2.** For steady convection-diffusion, $`v\,du/dx = D\,d^2u/dx^2`$, central differencing on a uniform grid gives $a_P u_P = a_W u_W + a_E u_E$ with $a_W = D/\Delta x + v/2$, $a_E = D/\Delta x - v/2$ and $a_P = a_W + a_E$. Find the cell Péclet number above which $a_E$ becomes negative, and evaluate it for $v = 2$ m/s, $D = 0.01$ m²/s and $\Delta x = 0.02$ m.

<details>
<summary>Answer</summary>

$a_E < 0$ when $v/2 > D/\Delta x$, that is when $Pe_\Delta = v\Delta x/D > 2$.

Here $Pe_\Delta = 2 \times 0.02/0.01 = 4$. The downstream neighbour gets a negative weight, so the solution can overshoot and wiggle.

Two fixes: refine to $\Delta x < 0.01$ m, or use an upwind (or bounded high-resolution) convection scheme, which keeps all coefficients positive.

</details>

**Exercise 3.** For pure advection, $u_t + v u_x = 0$ with $v = 1$ m/s, use the explicit upwind finite-volume update $u_i^{n+1} = u_i^n - \frac{v\Delta t}{\Delta x}(u_i^n - u_{i-1}^n)$ with $\Delta x = 0.1$ m and $\Delta t = 0.05$ s. The cell values are $(1, 1, 0, 0)$, and cell 0 is held at 1 by the inflow. (a) Advance one step. (b) Check that the change in total content equals the net boundary flux.

<details>
<summary>Answer</summary>

(a) The Courant number is $C = v\Delta t/\Delta x = 0.5 \le 1$, so the step is stable.

- $u_1 = 1 - 0.5(1 - 1) = 1$
- $u_2 = 0 - 0.5(0 - 1) = 0.5$
- $u_3 = 0 - 0.5(0 - 0) = 0$

(b) Over cells 1 to 3, the content changes by $\Delta x\sum\Delta u = 0.1 \times 0.5 = 0.05$. The net flux is $`\Delta t\,(v u_0 - v u_3) = 0.05 \times (1 - 0) = 0.05`$. The two agree.

</details>

**Exercise 4.** Solve $`v\,du/dx = D\,d^2u/dx^2`$ on $[0, 1]$ with $u(0) = 1$, $u(1) = 0$, $v = 0.1$ m/s and $D = 0.1$ m²/s, using 5 cells and central differencing. Boundary faces use the boundary value for convection and a half-cell distance for diffusion. Compare with the exact solution $u = 1 - (e^{vx/D} - 1)/(e^{vL/D} - 1)$.

<details>
<summary>Answer</summary>

$\Delta x = 0.2$, so $D/\Delta x = 0.5$ and $Pe_\Delta = 0.2$. The coefficients are:

- Interior cells: $a_W = 0.55$, $a_E = 0.45$, $a_P = 1.0$.
- Cell 1: $`1.55\,u_1 - 0.45\,u_2 = 1.1\,u(0)`$.
- Cell 5: $`1.45\,u_5 - 0.55\,u_4 = 0.9\,u(1) = 0`$.

| $x$ | FVM (central) | exact |
| --- | --- | --- |
| 0.1 | 0.9421 | 0.9388 |
| 0.3 | 0.8006 | 0.7964 |
| 0.5 | 0.6276 | 0.6225 |
| 0.7 | 0.4163 | 0.4100 |
| 0.9 | 0.1579 | 0.1505 |

The largest error is below 0.008. Because $Pe_\Delta < 2$, all coefficients are positive and central differencing is accurate and free of wiggles.

</details>

## References

- H. K. Versteeg, W. Malalasekera, *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Prentice Hall, 2007.
- R. J. LeVeque, *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002.
- J. H. Ferziger, M. Perić, R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
