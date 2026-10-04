# Discretization of Conservation Equations Using the Finite-Volume Method

The finite-volume method (FVM) is a widely used technique for solving partial differential equations that express conservation laws. In FVM, the computational domain is divided into small control volumes (cells), and the integral form of the conservation laws is applied to each cell. This approach makes sure that the numerical scheme directly enforces conservation of mass, momentum, and energy.

## Overview of the Finite-Volume Method

### Control Volumes and Grid Structure

- Control Volumes: The computational domain is partitioned into a finite number of non-overlapping cells (e.g., quadrilaterals in 2D or hexahedrals in 3D). Each cell acts as a control volume.
- Nodes: A representative point (or node) is typically associated with each cell, where primary unknowns (such as velocity, pressure, temperature, etc.) are stored.
- Flux Evaluation: The integral forms of the conservation laws are applied over each control volume, with fluxes computed at the cell faces. These fluxes represent the flow of quantities (mass, momentum, energy) across the control volume boundaries.

## Integral Form of Conservation Equations

The starting point in FVM is the integral formulation of a conservation law over an arbitrary control volume $V$ with boundary surface $S$:

```math
\frac{\partial}{\partial t}\int_V \phi \, dV + \int_S \vec{F} \cdot \hat{n} \,
dS = \int_V S_\phi \, dV
```

where:

- $\phi$ is a conserved variable (e.g., density, momentum component, energy),
- $\vec{F}$ is the corresponding flux vector,
- $\hat{n}$ is the outward-pointing unit normal vector on the surface $S$,
- $S_\phi$ is a source term.

### Example: Continuity Equation for Steady, Incompressible Flow

For steady, incompressible flow (i.e., time-independent with constant density), the continuity equation simplifies to:

```math
\int_S \vec{V} \cdot \hat{n} \, dS = 0
```

where $\vec{V}$ is the velocity vector. This equation implies that the net volumetric flow into the control volume is zero.

## Discretization on a Rectangular Cell

To illustrate the discretization process, consider a two-dimensional rectangular cell with dimensions $\Delta x$ (width) and $\Delta y$ (height).

### Cell Geometry and Notation

A schematic of the rectangular cell is as follows:

```
          (Face 2: top)
         |             |
         |             |  Δx
         |             |
(Face 1) |             | (Face 3)
(left)   ---------------  (right)
         |             |
         |             |
         (Face 4: bottom)
                Δx
                Δy (vertical distance)
```

Face 1 (Left):

```math
\vec{V}_1 = u_1 \, \hat{i} + v_1 \, \hat{j}
```

Face 2 (Top):

```math
\vec{V}_2 = u_2 \, \hat{i} + v_2 \, \hat{j}
```

Face 3 (Right):

```math
\vec{V}_3 = u_3 \, \hat{i} + v_3 \, \hat{j}
```

Face 4 (Bottom):

```math
\vec{V}_4 = u_4 \, \hat{i} + v_4 \, \hat{j}
```

*Note:* In many practical applications, one assumes that the primary contributions come from the normal components of the velocity at each face. For instance, on the left and right faces, the $u$-component is dominant, and on the top and bottom faces, the $v$-component is dominant.

### Discrete Continuity Equation

By applying the integral continuity equation to the control volume, we approximate the surface integrals over each face. Let the contribution from each face be given by the product of the normal velocity and the face length. Assuming the outward normals are defined as:

Left face:

$$
\hat{n} = -\hat{i}
$$

Top face:

$$
\hat{n} = +\hat{j}
$$

Right face:

$$
\hat{n} = +\hat{i}
$$

Bottom face:

$$
\hat{n} = -\hat{j}
$$

the discrete form of the continuity equation becomes:

$$
(-u_1) \Delta y + (v_2) \Delta x + (u_3) \Delta y + (-v_4) \Delta x = 0
$$

Rearranging the terms:

```math
-u_1 \, \Delta y - v_4 \, \Delta x + u_3 \, \Delta y + v_2 \, \Delta x = 0
```

This expression states that the net mass flux through the cell faces must sum to zero, thus preserving mass conservation within the control volume.

## Extension to Momentum and Energy Conservation

### Conservation of Momentum

For the momentum equations, the same approach is used. For example, the $x$-momentum conservation in its integral form is:

```math
\int_S \rho u \, \vec{V} \cdot \hat{n} \, dS = \int_S
(\text{Pressure and viscous forces}) \cdot \hat{i} \, dS
```

After discretizing the surface integrals over the cell faces (and including any body forces or source terms), one obtains an algebraic equation for the $x$-momentum at the cell center. A similar procedure applies to the $y$-momentum.

### Conservation of Energy

Similarly, the energy conservation equation is integrated over the control volume:

```math
\int_S \left(\rho E \, \vec{V} + p \, \vec{V} \right) \cdot \hat{n} \, dS = \int_S
\text{Heat flux} \, dS
```

and then discretized by approximating the fluxes across each cell face.

## Interpolation and Assembly of the Discrete System

### Interpolating Face Values

In the finite-volume framework, the primary unknowns (e.g., velocities, pressures) are typically stored at the cell centers. However, the fluxes at the cell faces require values at these locations. To obtain face-centered values, interpolation is used. A common approach is linear interpolation. For example, the velocity at a face between cell $P$ (primary cell) and cell $N$ (neighboring cell) is approximated as:

$$
u_f = \frac{1}{2}\left(u_P + u_N\right)
$$

### Assembly and Solution

Once all control volumes are discretized, the result is a system of algebraic equations that can be written in matrix form. Depending on the problem size and complexity, this system is solved using:

- Direct Solvers: Suitable for smaller systems.
- Iterative Solvers: Such as Gauss-Seidel, Conjugate Gradient, or Multigrid methods for larger systems.

The accuracy and stability of the solution are enhanced by the conservation properties inherent in the finite-volume method.

## Comparison with the Finite-Difference Method

### Finite-Volume Method (FVM)

- Conservation: FVM applies the integral conservation laws over each control volume, making sure that conservation (e.g., mass, momentum, energy) is satisfied locally.
- Flexibility: It readily handles unstructured grids and complicated geometries.
- Flux Computation: The fluxes are computed explicitly at the cell faces, which is particularly advantageous in the presence of discontinuities (e.g., shocks).

### Finite-Difference Method (FDM)

- Differential Approach: FDM approximates the derivatives in the governing equations using Taylor series expansions, which results in pointwise approximations of the differential equations.
- Grid Restrictions: FDM is typically more straightforward on structured grids and may face challenges with irregular geometries.
- Conservation: While FDM can be conservative with careful formulation, conservation is not inherently built into the method as it is in FVM.

## Purpose in CFD

This note shows how to discretize the integral conservation equations (continuity, momentum, energy) on rectangular finite-volume cells. It derives the discrete continuity equation by summing normal velocity contributions at each cell face, extends the approach to momentum and energy, and discusses face-value interpolation and system assembly. These steps are the core of every FVM-based CFD code.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Rectangular cell dimensions $\Delta x$, $\Delta y$, face velocity components $(u_f, v_f)$, outward normals $\hat{n}$, cell-centered primary variables |
| **Outputs** | Discrete continuity equation $(-u_1)\Delta y + (v_2)\Delta x + (u_3)\Delta y + (-v_4)\Delta x = 0$, momentum and energy algebraic equations, global matrix system |

## Related Scripts

- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.

## Exercises

**Exercise 1.** A rectangular cell has $\Delta x = 0.1$ m and $\Delta y = 0.05$ m. The face velocities are $u_1 = 1.0$ m/s (left), $u_3 = 1.2$ m/s (right) and $v_4 = 0.3$ m/s (bottom). Use the discrete continuity equation to find the velocity $v_2$ on the top face.

<details>
<summary>Answer</summary>

$(-u_1)\Delta y + v_2\Delta x + u_3\Delta y - v_4\Delta x = 0$, so

```math
v_2 = v_4 - (u_3 - u_1) \frac{\Delta y}{\Delta x} = 0.3 - 0.2 \times 0.5 = 0.2
\text{ m/s}
```

The net volume flow out through the right face ($0.2 \times 0.05 = 0.01$ m²/s) is balanced by a reduced outflow through the top.

</details>

**Exercise 2.** Divide the discrete continuity equation by the cell area $`\Delta x\,\Delta y`$ and show that it is a consistent approximation of $\partial u/\partial x + \partial v/\partial y = 0$ at the cell centre. What is its order of accuracy on a uniform grid?

<details>
<summary>Answer</summary>

```math
\frac{u_3 - u_1}{\Delta x} + \frac{v_2 - v_4}{\Delta y} = 0
```

The face values sit a half cell on either side of the centre, so each quotient is a central difference with spacing $\Delta x$ (or $\Delta y$) about the centre. Its truncation error is $O(\Delta x^2) + O(\Delta y^2)$. The finite-volume balance is therefore consistent and second-order accurate, while also conserving mass exactly.

</details>

**Exercise 3.** On a non-uniform grid, cell centres lie at $x_P = 0$ and $x_N = 0.3$, the face is at $x_f = 0.1$, and $u_P = 2$, $u_N = 5$. Compute the linearly interpolated face value. What does first-order upwinding give if the flow goes from $P$ to $N$?

<details>
<summary>Answer</summary>

Linear interpolation with weight $f = (x_f - x_P)/(x_N - x_P) = 1/3$ gives

```math
u_f = (1 - f)u_P + f u_N = \frac{2}{3}(2) + \frac{1}{3}(5) = 3.0
```

The simple average $(u_P + u_N)/2 = 3.5$ would be wrong here, because the face is not midway.

Upwinding takes the upstream value, $u_f = u_P = 2$.

</details>

**Exercise 4.** Steady 1D heat conduction, $\frac{d}{dx}\left(k\frac{dT}{dx}\right) = 0$, in a rod of length $L = 0.5$ m, with $k = 1000$ W/(m K), cross-section $A = 10^{-2}$ m², $T_A = 100$ °C at $x = 0$ and $T_B = 500$ °C at $x = L$. Use 5 equal cells with the boundary temperatures applied on the end faces. Assemble the finite-volume equations, solve them, and check the heat flow through the rod.

<details>
<summary>Answer</summary>

$\delta x = 0.1$ m and the neighbour coefficient is $a = kA/\delta x = 100$ W/K. A boundary face lies half a cell from the cell centre, so its coefficient is $2a = 200$ W/K.

- Interior cells 2 to 4: $`200\,T_P = 100\,T_W + 100\,T_E`$.
- Cell 1: $`300\,T_1 = 100\,T_2 + 200\,T_A`$.
- Cell 5: $`300\,T_5 = 100\,T_4 + 200\,T_B`$.

Solving gives $T = (140, 220, 300, 380, 460)$ °C, which matches the exact linear profile $T = 100 + 800x$ at the cell centres.

Heat flow through the left face: $200 \times (140 - 100) = 8000$ W. Through the right face: $200 \times (500 - 460) = 8000$ W. Both equal $kA(T_B - T_A)/L = 8000$ W. Summing all cell equations cancels the interior face fluxes pairwise, which is the discrete form of global conservation.

</details>

## References

- H. K. Versteeg, W. Malalasekera, *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Prentice Hall, 2007.
- S. V. Patankar, *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
- F. Moukalled, L. Mangani, M. Darwish, *The Finite Volume Method in Computational Fluid Dynamics: An Advanced Introduction with OpenFOAM and Matlab*, Springer, 2016.
