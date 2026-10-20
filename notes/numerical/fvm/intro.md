# The Finite Volume Method

The finite volume method (FVM) discretizes a conservation law in its integral form: the domain is split into control volumes, the unknowns are the averages of the conserved quantity over each volume, and the change of each average is balanced by the fluxes through the faces of its volume. Because the flux leaving one cell through a face is the flux entering its neighbour, the discrete equations conserve mass, momentum and energy exactly, cell by cell and over the whole domain, on any mesh. This property, together with its natural handling of unstructured meshes, is why most general-purpose CFD codes (OpenFOAM, ANSYS Fluent, STAR-CCM+, SU2) are finite-volume codes.

This note derives the method from the integral conservation law, proves the conservation property, and works through the 1D steady convection–diffusion problem in full, which already shows the central difficulty of the method: choosing the face values of a convected quantity. The general multidimensional discretization on unstructured meshes is in [Finite Volume Discretization on General Meshes](discretization.md), and the face-value schemes for convection are in [Convection Schemes](convection_schemes.md). The equations being discretized are introduced in [Governing Equations for CFD](../cfd/governing_equations.md).

## Problem Statement

Most transport equations of fluid dynamics are special cases of the generic transport equation for a scalar $\phi$ per unit mass,

$$
\frac{\partial (\rho\phi)}{\partial t} +
\nabla\cdot(\rho\mathbf{u}\phi) = \nabla\cdot(\Gamma\nabla\phi) + S_\phi
$$

with density $\rho$, velocity $\mathbf{u}$, diffusion coefficient $\Gamma$ and volumetric source $S_\phi$. With $\phi = 1$, $\Gamma = 0$, $S = 0$ it is the continuity equation; with $\phi = u_i$ it is a momentum equation, with the pressure gradient in the source; with $\phi$ = temperature or species concentration it is an energy or species equation.

In this note the velocity field is given and satisfies continuity. The domain $\Omega$ is divided into $N$ non-overlapping cells $V_P$ that cover it, and the boundary $\partial\Omega$ carries a prescribed value of $\phi$ (Dirichlet), a prescribed flux (Neumann) or a mix. The unknowns are the cell averages $\bar\phi_P$. The discrete problem is solved when the $N$ algebraic balance equations are satisfied to a residual tolerance far below the discretization error, and the computed field is useful when it is bounded (no values outside the range set by the boundary data and sources) and close to the grid-converged solution.

The hard part is that the balance needs $\phi$ and $\nabla\phi$ on the faces, where no unknowns are stored. For diffusion this is easy and central interpolation works. For convection it is not: when convection dominates diffusion over one cell, central interpolation produces oscillations and upwind interpolation smears the solution, and the choice of face values decides both accuracy and boundedness.

## Integral Form and Cell Averages

Integrate the transport equation over a fixed control volume $V_P$ with closed surface $\partial V_P$ and outward unit normal $\mathbf{n}$. The divergence (Gauss) theorem, $`\int_V \nabla\cdot\mathbf{a}\,dV = \oint_{\partial V}\mathbf{a}\cdot\mathbf{n}\,dS`$, turns the convection and diffusion terms into surface integrals:

```math
\frac{d}{dt}\int_{V_P}\rho\phi\,dV + \oint_{\partial V_P}\left(\rho\mathbf{u}\phi - \Gamma\nabla\phi\right)\cdot\mathbf{n}\,dS = \int_{V_P} S_\phi\,dV
```

This is exact. The rate of change of the content of the cell equals the net inflow through its surface plus what the source produces inside. For a polyhedral cell the surface is a set of plane faces $f$ with area vectors $`\mathbf{S}_f = \int_f\mathbf{n}\,dS`$, so

```math
\frac{d}{dt}\left(\overline{\rho\phi}_P V_P\right) + \sum_{f} \int_f \mathbf{J}\cdot\mathbf{n}\,dS = \bar S_P V_P,
\qquad
\mathbf{J} = \rho\mathbf{u}\phi - \Gamma\nabla\phi
```

where the overbar denotes the average over the cell. Two approximations turn this into a finite-dimensional system.

The first replaces the cell average by the value at the cell centroid $\mathbf{x}_P$. Expanding $\phi$ in a Taylor series about $\mathbf{x}_P$,

```math
\bar\phi_P = \frac{1}{V_P}\int_{V_P}\phi\,dV = \phi(\mathbf{x}_P) + \nabla\phi(\mathbf{x}_P)\cdot\frac{1}{V_P}\int_{V_P}(\mathbf{x} - \mathbf{x}_P)\,dV + O(h^2) = \phi(\mathbf{x}_P) + O(h^2)
```

because the first moment about the centroid vanishes ($h$ is the cell size). The second evaluates each face integral by the midpoint rule, $`\int_f\mathbf{J}\cdot\mathbf{n}\,dS \approx \mathbf{J}(\mathbf{x}_f)\cdot\mathbf{S}_f`$, which is also second-order accurate when $\mathbf{x}_f$ is the face centroid. A finite volume scheme built on these two rules is therefore at most second order, whatever the accuracy of the face interpolation; higher order needs higher-order quadrature on each face and a reconstruction of the cell averages, as in the high-order methods of [High-Order Methods](../high_order/intro.md).

## Cell-Centred and Vertex-Centred Arrangements

The control volumes can be built in two ways.

|  | Cell-centred | Vertex-centred (median dual) |
| --- | --- | --- |
| Unknowns stored at | centroids of the mesh cells | vertices of the mesh |
| Control volume | the mesh cell itself | a dual cell around each vertex, bounded by segments joining edge midpoints and cell centroids |
| Unknowns per mesh | one per cell (roughly five to six times the vertex count on a tetrahedral mesh) | one per vertex |
| Boundary | values on boundary faces come from boundary conditions | unknowns sit on the boundary; boundary control volumes are half or partial cells |
| Typical use | general-purpose pressure-based codes (OpenFOAM, Fluent, STAR-CCM+) | unstructured compressible aerodynamics codes (SU2, FUN3D, TAU) |

Both give a flux balance per control volume, and the derivations below apply to either. The rest of these notes use the cell-centred arrangement. In 1D the cell faces lie midway between nodes on a uniform grid, and the two arrangements differ only at the boundaries.

![Control-volume notation in 1D and on unstructured 2D cells](../../../scripts/plots/control_volume_stencil/control_volume_stencil.png)

Panel (a) fixes the 1D notation used below: node $P$ with neighbours $W$ (west) and $E$ (east), faces $w$ and $e$, cell width $\Delta x = \delta x_{we}$ and node spacings $\delta x_{WP}$, $\delta x_{PE}$. Panel (b) shows the same objects on an unstructured mesh, discussed in [Finite Volume Discretization on General Meshes](discretization.md).

## Conservation Property

Write the semi-discrete balance of cell $P$ as

```math
\frac{d}{dt}\left(\overline{\rho\phi}_P V_P\right) + \sum_{f\in\partial V_P} \hat J_{f,P} = \bar S_P V_P
```

where $\hat J_{f,P}$ is the numerical flux leaving cell $P$ through face $f$. A scheme is **conservative** if every interior face $f$ shared by cells $P$ and $N$ has a single numerical flux:

$$
\hat J_{f,N} = -\hat J_{f,P}
$$

Then summing the balances of all cells cancels every interior face, because each one appears twice with opposite signs, and leaves

```math
\frac{d}{dt}\sum_{P}\overline{\rho\phi}_P V_P + \sum_{f\in\partial\Omega}\hat J_f = \sum_P \bar S_P V_P
```

which is the discrete form of the global balance for $\Omega$: the total content changes only through the boundary fluxes and the sources. In 1D the cancellation is a telescoping sum, $\sum_{i=1}^{N}(\hat J_{i+1/2} - \hat J_{i-1/2}) = \hat J_{N+1/2} - \hat J_{1/2}$. Nothing in the argument depends on how $\hat J$ is computed, only on the fact that both cells use the same value. Codes guarantee it by looping over faces, computing each flux once, and adding it to one cell and subtracting it from the other.

Conservation matters most for flows with discontinuities. The Lax–Wendroff theorem (Lax and Wendroff 1960) states that if a conservative, consistent scheme converges as the grid is refined, its limit is a weak solution of the conservation law, so shocks move at the correct speed. A non-conservative discretization of, for example, $`u\,\partial u/\partial x`$ instead of $\partial(u^2/2)/\partial x$ can converge to a shock with the wrong speed. This is developed in [Riemann Solvers and Godunov Methods](riemann_solvers.md).

## Worked Example: 1D Steady Convection–Diffusion

Consider steady convection and diffusion of $\phi$ in a 1D flow with constant velocity $u$,

$$
\frac{d}{dx}(\rho u\phi) = \frac{d}{dx}\left(\Gamma \frac{d\phi}{dx}\right),
\qquad 0 < x < L,
\qquad \phi(0) = \phi_0, \quad \phi(L) = \phi_L
$$

where continuity gives $d(\rho u)/dx = 0$. The exact solution is

```math
\phi(x) = \phi_0 + (\phi_L - \phi_0)\,\frac{\exp(\rho u x/\Gamma) - 1}{\exp(\rho u L/\Gamma) - 1}
```

For a large global Péclet number $Pe_L = \rho u L/\Gamma$ it is almost equal to $\phi_0$ everywhere except in a layer of thickness about $\Gamma/(\rho u)$ at the outlet.

### Integration over a Control Volume

Integrating over the cell of node $P$, between faces $w$ and $e$, gives the exact balance

$$
(\rho u\phi)_e - (\rho u\phi)_w = \left(\Gamma \frac{d\phi}{dx}\right)_e -
\left(\Gamma \frac{d\phi}{dx}\right)_w
$$

Define the convective mass flux and the diffusion conductance of each face,

$$
F_w = (\rho u)_w, \quad F_e = (\rho u)_e,
\qquad D_w = \frac{\Gamma_w}{\delta x_{WP}}, \quad D_e = \frac{\Gamma_e}{\delta x_{PE}}
$$

and approximate the face gradients by central differences, $`(d\phi/dx)_e = (\phi_E - \phi_P)/\delta x_{PE}`$, which is second order on a uniform grid. The balance becomes

$$
F_e\phi_e - F_w\phi_w = D_e(\phi_E - \phi_P) - D_w(\phi_P - \phi_W)
$$

and continuity says $F_e = F_w$. The only remaining question is the convected face values $\phi_e$ and $\phi_w$.

### Central Differencing

Linear interpolation on a uniform grid gives $\phi_e = (\phi_P + \phi_E)/2$ and $\phi_w = (\phi_W + \phi_P)/2$. Collecting terms,

$$
a_P\phi_P = a_W\phi_W + a_E\phi_E
$$

with

$$
a_W = D_w + \frac{F_w}{2},
\qquad a_E = D_e - \frac{F_e}{2},
\qquad a_P = a_W + a_E + (F_e - F_w)
$$

### Upwind Differencing

The first-order upwind scheme takes the face value from the node on the upstream side: $\phi_e = \phi_P$ if $F_e > 0$ and $\phi_e = \phi_E$ if $F_e < 0$. For either flow direction,

$$
a_W = D_w + \max(F_w, 0),
\qquad a_E = D_e + \max(0, - F_e),
\qquad a_P = a_W + a_E + (F_e - F_w)
$$

The face value is only first-order accurate, so the scheme is first order.

### Boundary Cells

At $x = 0$ the face $w$ of cell 1 is the boundary $A$, where $\phi_A = \phi_0$ is known. The face lies half a cell from the node, so the diffusive flux is $2\Gamma(\phi_1 - \phi_A)/\Delta x$, a conductance $D_A = 2\Gamma/\Delta x$, and the convective flux through an inflow face is $F_A\phi_A$. For central differencing this gives

```math
a_W = 0,
\qquad a_E = D - \frac{F}{2},
\qquad a_P = a_E + F + D_A,
\qquad b = (D_A + F)\,\phi_A
```

and at the outflow boundary $B$ with $\phi_B = \phi_L$,

```math
a_W = D + \frac{F}{2},
\qquad a_E = 0,
\qquad a_P = a_W - F + D_B,
\qquad b = (D_B - F)\,\phi_B
```

with $D_B = 2\Gamma/\Delta x$, so that $a_P\phi_P = a_W\phi_W + a_E\phi_E + b$. Versteeg and Malalasekera write the same terms as a linearized source $S_u + S_P\phi_P$. For upwind the outflow face takes the upstream value $\phi_N$ instead of $\phi_B$. The resulting tridiagonal system is solved with the Thomas algorithm.

### Results

The test case of Versteeg and Malalasekera (Examples 5.1 and 5.2) uses $L = 1$ m, $\rho = 1$ kg/m³, $\Gamma = 0.1$ kg/(m s), $\phi_0 = 1$, $\phi_L = 0$ and five cells. The [convection–diffusion script](../../../scripts/algorithms/fvm_convection_diffusion_1d/) reproduces the published values:

| $x$ \[m\] | 0.1 | 0.3 | 0.5 | 0.7 | 0.9 |
| --- | --- | --- | --- | --- | --- |
| exact, $u = 0.1$ m/s | 0.9388 | 0.7964 | 0.6225 | 0.4100 | 0.1505 |
| central, $u = 0.1$ m/s ($Pe_\Delta = 0.2$) | 0.9421 | 0.8006 | 0.6276 | 0.4163 | 0.1579 |
| exact, $u = 2.5$ m/s | 1.0000 | 1.0000 | 1.0000 | 0.9994 | 0.9179 |
| central, $u = 2.5$ m/s ($Pe_\Delta = 5$) | 1.0356 | 0.8694 | 1.2573 | 0.3521 | 2.4644 |
| upwind, $u = 2.5$ m/s ($Pe_\Delta = 5$) | 0.9998 | 0.9987 | 0.9921 | 0.9524 | 0.7143 |

At $u = 0.1$ m/s central differencing is accurate to within 0.008. At $u = 2.5$ m/s on the same grid it oscillates and overshoots to 2.46, outside the range $[0, 1]$ of the boundary data. Upwinding stays bounded but places the outlet layer far too early.

![Central, upwind, hybrid and QUICK against the exact solution](../../../scripts/algorithms/fvm_convection_diffusion_1d/fvm_convection_diffusion_1d.png)

Panel (a) is the coarse grid at $Pe_\Delta = 5$; panel (b) the refined grid with 20 cells at $Pe_\Delta = 1.25$, where every scheme is bounded; panel (c) the RMS error against the number of cells, with observed orders 2.00 for central and 0.99 for upwind on the finest grids.

## The Péclet Number and Boundedness

The ratio of convection to diffusion over one cell is the **cell Péclet number**

```math
Pe_\Delta = \frac{F}{D} = \frac{\rho u\,\Delta x}{\Gamma}
```

For central differencing $a_E = D(1 - Pe_\Delta/2)$, which is negative when $Pe_\Delta > 2$. A negative neighbour coefficient means that raising $\phi_E$ lowers $\phi_P$, which is unphysical for convection and diffusion and allows overshoots.

The interior equations can be solved exactly. With constant coefficients, $a_P = a_W + a_E$, the difference equation $a_E\phi_{i+1} - a_P\phi_i + a_W\phi_{i-1} = 0$ has solutions $\phi_i = \lambda^i$ with $a_E\lambda^2 - (a_W + a_E)\lambda + a_W = 0$, whose roots are $\lambda = 1$ and $\lambda = a_W/a_E$. Every interior solution is therefore $\phi_i = A + B\lambda^i$. The exact solution sampled at the nodes has the same form with $\lambda = e^{Pe_\Delta}$. The two schemes give

| Scheme | $\lambda = a_W/a_E$ | $Pe_\Delta = 0.2$ | $Pe_\Delta = 5$ |
| --- | --- | --- | --- |
| exact | $e^{Pe_\Delta}$ | 1.2214 | 148.4 |
| central | $(2 + Pe_\Delta)/(2 - Pe_\Delta)$ | 1.2222 | −2.333 |
| upwind | $1 + Pe_\Delta$ | 1.2000 | 6.000 |

Central differencing gives the (1,1) Padé approximation of $e^{Pe_\Delta}$, which is accurate to $O(Pe_\Delta^3)$ for small $Pe_\Delta$ but becomes negative for $Pe_\Delta > 2$, so $\lambda^i$ changes sign from node to node: the wiggles are part of the exact discrete solution, not an instability of the solver. Upwinding gives $1 + Pe_\Delta$, the first two terms of the series, which is always positive but grows far too slowly, so the layer is spread over several cells.

The general condition, the Scarborough criterion in the form used by Patankar (1980), is that the discrete equations $a_P\phi_P = \sum a_{nb}\phi_{nb} + b$ have a bounded solution, and are convergent with Gauss–Seidel-type iteration, if

```math
a_{nb} \ge 0 \ \text{ for all neighbours},
\qquad
\frac{\sum |a_{nb}|}{|a_P|} \le 1 \ \text{ at every node, and } < 1 \ \text{ at one node at least}
```

The second condition is diagonal dominance. With $a_P = \sum a_{nb}$ for a divergence-free flow it is satisfied with equality, and the strict inequality comes from the boundary nodes. A solution of such a system satisfies a discrete maximum principle: without sources, every $\phi_P$ is a weighted average of its neighbours with non-negative weights, so no interior value can exceed the boundary values. Central differencing meets the first condition only for $|Pe_\Delta| \le 2$; upwind meets it for every $Pe_\Delta$.

The bound $|Pe_\Delta| < 2$ is a resolution requirement. For $u = 2.5$ m/s and $\Gamma/\rho = 0.1$ m²/s it needs $\Delta x < 0.08$ m, which is affordable in 1D. For a boundary-layer flow at a Reynolds number of $10^6$, the equivalent requirement in the flow direction is beyond any practical mesh, which is why production codes use upwind-biased and bounded high-resolution schemes for convection.

## Properties a Discretization Scheme Needs

Versteeg and Malalasekera list three properties that a convection–diffusion scheme must have to give physically realistic results.

| Property | Meaning | Central | Upwind |
| --- | --- | --- | --- |
| Conservativeness | the flux through a shared face is the same for both cells | yes | yes |
| Boundedness | all coefficients positive and the matrix diagonally dominant, so no new extrema | only for $\lvert Pe_\Delta \rvert \le 2$ | yes |
| Transportiveness | the face value is weighted towards the upstream side as $\lvert Pe_\Delta \rvert$ grows, because information travels with the flow | no: equal weights for any $Pe_\Delta$ | yes |
| Order of accuracy | leading power of $\Delta x$ in the truncation error | 2 | 1 |

No linear scheme has all four in the most desirable form: by Godunov's theorem a linear scheme that never creates new extrema is at most first-order accurate. The hybrid, power-law, QUICK and TVD schemes that try to combine accuracy and boundedness are the subject of [Convection Schemes](convection_schemes.md).

## Steps of a Finite Volume Computation

1. Generate a mesh of non-overlapping cells covering the domain and compute the geometry: cell volumes and centroids, face area vectors and centroids, and the owner and neighbour of every face ([Mesh Quality](../../../practice/mesh_generation/mesh_quality.md)).
2. Integrate each conservation equation over every cell and replace volume integrals of divergences by face sums.
3. Approximate the face fluxes: interpolate face values for convection, use a gradient for diffusion, and linearize the source.
4. Apply the boundary conditions on the boundary faces ([Boundary Conditions](../cfd/boundary_conditions.md)).
5. Assemble the algebraic system $\mathbf{A}\boldsymbol\phi = \mathbf{b}$, one row per cell.
6. Solve it with a direct or iterative solver ([Direct and Iterative Solvers](../cfd/direct_and_iterative_solvers.md)). For nonlinear or coupled equations, update the coefficients and repeat until the residuals have fallen far enough ([Iterative Convergence](../cfd/iterative_convergence.md)); for the momentum and pressure equations of incompressible flow see [Pressure–Velocity Coupling](pressure_velocity_coupling.md).
7. Refine the mesh and check that the quantities of interest converge ([Verification and Validation](../cfd/verification_and_validation.md)).

## Relation to Other Methods

| Method | Unknowns | Equation satisfied | Conservation |
| --- | --- | --- | --- |
| Finite difference ([intro](../fdm/intro.md)) | point values on a structured grid | the differential equation at each grid point | only if written in flux form |
| Finite volume | cell averages | the integral balance on each cell | local and global, by construction |
| Finite element ([intro](../fem/intro.md)) | coefficients of piecewise polynomials | the weak form, weighted by test functions | global; local only for special formulations |
| Spectral and DG ([intro](../high_order/intro.md)) | coefficients of global or element-wise polynomials | the weak form | DG is locally conservative |

On a uniform Cartesian grid the second-order finite volume and finite difference schemes for convection–diffusion often give the same algebraic equations. The methods differ on non-uniform and unstructured meshes, at boundaries and for discontinuous solutions.

## Pitfalls

- Running central differencing at $|Pe_\Delta| > 2$. The oscillations are a property of the discrete equations, and an iterative solver may also fail to converge because the matrix is no longer diagonally dominant.
- Taking the smoothness of an upwind solution as evidence of accuracy. Its numerical diffusion is $\rho u\Delta x/2$, which at $Pe_\Delta = 5$ is 2.5 times the physical diffusion.
- Computing the flux of a shared face twice, once from each side, with different formulas. The scheme is then no longer conservative, even if each formula is consistent.
- Treating the boundary face as if it were a full cell from the node. The node-to-boundary distance is $\Delta x/2$, so the boundary conductance is $2\Gamma/\Delta x$.
- Positive source slopes. A source linearized as $S_c + S_P\phi_P$ must have $S_P \le 0$ to keep the matrix diagonally dominant ([Source Linearization](discretization.md#source-linearization)).

## Key Takeaways

- The FVM integrates the conservation law over each cell and balances the rate of change against face fluxes; the divergence theorem is the only step that turns the PDE into a face sum.
- Cell averages and midpoint face integrals are second-order approximations, so a standard finite volume scheme is at most second order.
- A single flux per shared face makes the scheme conservative locally and globally, independently of how the flux is approximated.
- For 1D convection–diffusion the discrete equations are $a_P\phi_P = a_W\phi_W + a_E\phi_E + b$; central and upwind face values differ only in the coefficients.
- Central differencing is bounded only for $|Pe_\Delta| \le 2$; upwinding is always bounded but first order and diffusive.

## Related Scripts

- [1D Finite-Volume Convection–Diffusion](../../../scripts/algorithms/fvm_convection_diffusion_1d/): solves steady 1D convection–diffusion with the finite volume method using central, upwind, hybrid, power-law and QUICK face values, and compares each with the exponential exact solution.
- [Control-Volume Stencil](../../../scripts/plots/control_volume_stencil/): draws the notation of the finite volume method: a 1D cell-centred grid with nodes W, P, E and faces w, e, and two unstructured 2D cells with the face area vector, the vector between the cell centroids and the split of the face area vector used to correct the diffusion flux on non-orthogonal meshes.
- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.
- [Raindrops on a Pond: Shallow-Water Ripples](../../../scripts/simulations/shallow_water_ripples/): simulates raindrops falling on a square basin of still water by solving the 2D shallow-water equations with a conservative finite-volume scheme, and animates the free surface as shaded relief.

## Exercises

**Exercise 1.** Explain why summing the finite volume equations over all cells of a 1D domain gives a statement of global conservation that involves only the boundary fluxes.

<details>
<summary>Answer</summary>

Cell $i$ gains $F_{i-1/2}$ and loses $F_{i+1/2}$. The same numerical flux $F_{i+1/2}$ is the gain of cell $i+1$. When all cells are summed, every interior flux appears once with each sign and cancels, leaving

```math
\frac{d}{dt}\sum_i \phi_i\,\Delta x = F_{1/2} - F_{N+1/2}
```

This holds exactly for any flux formula, provided both neighbours use the same face flux.

</details>

**Exercise 2.** For steady convection–diffusion with central differencing on a uniform grid, $a_W = D + F/2$ and $a_E = D - F/2$. Find the cell Péclet number above which $a_E$ becomes negative, and evaluate it for $u = 2$ m/s, $\Gamma/\rho = 0.01$ m²/s and $\Delta x = 0.02$ m.

<details>
<summary>Answer</summary>

$a_E < 0$ when $F/2 > D$, that is when $Pe_\Delta = \rho u\Delta x/\Gamma > 2$.

Here $Pe_\Delta = 2 \times 0.02/0.01 = 4$. The downstream neighbour gets a negative weight, so the solution can overshoot and wiggle.

Two fixes: refine to $\Delta x < 0.01$ m, or use an upwind or bounded high-resolution convection scheme, which keeps all coefficients non-negative.

</details>

**Exercise 3.** For pure advection, $\phi_t + u\phi_x = 0$ with $u = 1$ m/s, use the explicit upwind finite volume update $\phi_i^{n+1} = \phi_i^n - C(\phi_i^n - \phi_{i-1}^n)$ with $\Delta x = 0.1$ m and $\Delta t = 0.05$ s. The cell values are $(1, 1, 0, 0)$, and cell 0 is held at 1 by the inflow. (a) Advance one step. (b) Check that the change in total content of cells 1 to 3 equals the net boundary flux.

<details>
<summary>Answer</summary>

(a) The Courant number is $C = u\Delta t/\Delta x = 0.5 \le 1$, so the step is stable.

- $\phi_1 = 1 - 0.5(1 - 1) = 1$
- $\phi_2 = 0 - 0.5(0 - 1) = 0.5$
- $\phi_3 = 0 - 0.5(0 - 0) = 0$

(b) Over cells 1 to 3, the content changes by $\Delta x\sum\Delta\phi = 0.1 \times 0.5 = 0.05$. The net flux is $`\Delta t\,(u\phi_0 - u\phi_3) = 0.05 \times (1 - 0) = 0.05`$. The two agree.

</details>

**Exercise 4.** Solve $`\rho u\,d\phi/dx = \Gamma\,d^2\phi/dx^2`$ on $[0, 1]$ m with $\phi(0) = 1$, $\phi(1) = 0$, $\rho = 1$ kg/m³, $u = 0.1$ m/s and $\Gamma = 0.1$ kg/(m s), using 5 cells and central differencing with the boundary treatment of this note. Compare with the exact solution.

<details>
<summary>Answer</summary>

$\Delta x = 0.2$ m, so $D = \Gamma/\Delta x = 0.5$, $D_A = D_B = 1.0$, $F = 0.1$ and $Pe_\Delta = 0.2$. The coefficients are:

- Interior cells: $a_W = 0.55$, $a_E = 0.45$, $a_P = 1.0$.
- Cell 1: $a_P = a_E + F + D_A = 1.55$, so $`1.55\,\phi_1 - 0.45\,\phi_2 = 1.1\,\phi_A = 1.1`$.
- Cell 5: $a_P = a_W - F + D_B = 1.45$, so $`1.45\,\phi_5 - 0.55\,\phi_4 = 0.9\,\phi_B = 0`$.

| $x$ \[m\] | FVM (central) | exact |
| --- | --- | --- |
| 0.1 | 0.9421 | 0.9388 |
| 0.3 | 0.8006 | 0.7964 |
| 0.5 | 0.6276 | 0.6225 |
| 0.7 | 0.4163 | 0.4100 |
| 0.9 | 0.1579 | 0.1505 |

The largest error is 0.0074. Because $Pe_\Delta < 2$, all coefficients are positive and central differencing is accurate and free of wiggles.

</details>

**Exercise 5.** On a uniform grid with $Pe_\Delta = 4$, find the non-constant homogeneous solution $\lambda^i$ of the interior equations for central and upwind differencing and compare with the exact nodal ratio. Explain what the central result means for the computed profile.

<details>
<summary>Answer</summary>

Central: $\lambda = (2 + 4)/(2 - 4) = -3$. Upwind: $\lambda = 1 + 4 = 5$. Exact: $e^4 = 54.6$.

With central differencing the discrete solution is $\phi_i = A + B(-3)^i$. The second term changes sign from one node to the next and grows by a factor of 3 per cell towards the outlet, so the profile is a sawtooth whose amplitude is largest next to the outflow boundary, as in panel (a) of the figure. Upwinding gives a monotone profile, but its growth factor of 5 per cell instead of 54.6 spreads the outlet layer over several cells.

</details>

## References

- H. K. Versteeg, W. Malalasekera, *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Prentice Hall, 2007. Chapters 4 and 5.
- S. V. Patankar, *Numerical Heat Transfer and Fluid Flow*, Hemisphere, 1980.
- J. H. Ferziger, M. Perić, R. L. Street, *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- F. Moukalled, L. Mangani, M. Darwish, *The Finite Volume Method in Computational Fluid Dynamics: An Advanced Introduction with OpenFOAM and Matlab*, Springer, 2016.
- R. J. LeVeque, *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002.
- P. D. Lax, B. Wendroff, "Systems of conservation laws", *Communications on Pure and Applied Mathematics*, 13(2), 217–237, 1960.
