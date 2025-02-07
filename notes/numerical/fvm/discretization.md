# Discretization of Conservation Equations Using the Finite-Volume Method

The finite-volume method (FVM) is a widely used technique for solving partial differential equations that express conservation laws. In FVM, the computational domain is divided into small control volumes (cells), and the integral form of the conservation laws is applied to each cell. This approach makes sure that the numerical scheme directly enforces conservation of mass, momentum, and energy.

## Overview of the Finite-Volume Method

### Control Volumes and Grid Structure

- Control Volumes: The computational domain is partitioned into a finite number of non-overlapping cells (e.g., quadrilaterals in 2D or hexahedrals in 3D). Each cell acts as a control volume.
- Nodes: A representative point (or node) is typically associated with each cell, where primary unknowns (such as velocity, pressure, temperature, etc.) are stored.
- Flux Evaluation: The integral forms of the conservation laws are applied over each control volume, with fluxes computed at the cell faces. These fluxes represent the flow of quantities (mass, momentum, energy) across the control volume boundaries.

## Integral Form of Conservation Equations

The starting point in FVM is the integral formulation of a conservation law over an arbitrary control volume $V$ with boundary surface $S$:

$$\frac{\partial}{\partial t}\int_V \phi, dV + \int_S \vec{F} \cdot \hat{n}, dS = \int_V S_\phi, dV$$

where:

- $\phi$ is a conserved variable (e.g., density, momentum component, energy),
- $\vec{F}$ is the corresponding flux vector,
- $\hat{n}$ is the outward-pointing unit normal vector on the surface $S$,
- $S_\phi$ is a source term.

### Example: Continuity Equation for Steady, Incompressible Flow

For steady, incompressible flow (i.e., time-independent with constant density), the continuity equation simplifies to:

$$\int_S \vec{V} \cdot \hat{n}, dS = 0$$

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

$$\vec{V}_1 = u_1, \hat{i} + v_1, \hat{j}$$

Face 2 (Top):

$$\vec{V}_2 = u_2, \hat{i} + v_2, \hat{j}$$

Face 3 (Right):

$$\vec{V}_3 = u_3, \hat{i} + v_3, \hat{j}$$

Face 4 (Bottom):

$$\vec{V}_4 = u_4, \hat{i} + v_4, \hat{j}$$

*Note:* In many practical applications, one assumes that the primary contributions come from the normal components of the velocity at each face. For instance, on the left and right faces, the $u$-component is dominant, and on the top and bottom faces, the $v$-component is dominant.

### Discrete Continuity Equation

By applying the integral continuity equation to the control volume, we approximate the surface integrals over each face. Let the contribution from each face be given by the product of the normal velocity and the face length. Assuming the outward normals are defined as:

Left face: 

$$\hat{n} = -\hat{i}$$

Top face: 

$$\hat{n} = +\hat{j}$$

Right face: 

$$\hat{n} = +\hat{i}$$

Bottom face: 

$$\hat{n} = -\hat{j}$$

the discrete form of the continuity equation becomes:

$$(-u_1) \Delta y + (v_2) \Delta x + (u_3) \Delta y + (-v_4) \Delta x = 0$$

Rearranging the terms:

$$- u_1, \Delta y - v_4, \Delta x + u_3, \Delta y + v_2, \Delta x = 0$$

This expression states that the net mass flux through the cell faces must sum to zero, thus preserving mass conservation within the control volume.

## Extension to Momentum and Energy Conservation

### Conservation of Momentum

For the momentum equations, the same approach is used. For example, the $x$-momentum conservation in its integral form is:

$$\int_S \rho u, \vec{V} \cdot \hat{n}, dS = \int_S (\text{Pressure and viscous forces}) \cdot \hat{i}, dS$$

After discretizing the surface integrals over the cell faces (and including any body forces or source terms), one obtains an algebraic equation for the $x$-momentum at the cell center. A similar procedure applies to the $y$-momentum.

### Conservation of Energy

Similarly, the energy conservation equation is integrated over the control volume:

$$\int_S \left( \rho E, \vec{V} + p, \vec{V} \right) \cdot \hat{n}, dS = \int_S \text{Heat flux}, dS$$

and then discretized by approximating the fluxes across each cell face.

## Interpolation and Assembly of the Discrete System

### Interpolating Face Values

In the finite-volume framework, the primary unknowns (e.g., velocities, pressures) are typically stored at the cell centers. However, the fluxes at the cell faces require values at these locations. To obtain face-centered values, interpolation is used. A common approach is linear interpolation. For example, the velocity at a face between cell $P$ (primary cell) and cell $N$ (neighboring cell) is approximated as:

$$u_f = \frac{1}{2}\left(u_P + u_N\right)$$

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
