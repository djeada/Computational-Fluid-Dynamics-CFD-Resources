# Boundary Conditions

Boundary conditions select, from all the solutions of a partial differential equation, the one that belongs to a particular flow. They are also where many CFD calculations go wrong: too few conditions leave the solution undetermined, too many make the problem contradictory, an inaccurate implementation lowers the order of accuracy of the whole solution, and an artificial outflow boundary placed too close can reflect waves back into the domain. This note covers the mathematical types of boundary condition, how many conditions each kind of equation needs and where, their implementation in finite-difference and finite-volume codes, the physical conditions used for incompressible flow, artificial outflow and far-field boundaries, and initial conditions. The equations themselves and their classification are in [Governing Equations for CFD](./governing_equations.md).

## Problem Statement

A PDE holds in a domain $\Omega$ with boundary $\partial\Omega$, which is divided into parts (inlet, outlet, walls, symmetry planes, far field). On each part, data must be supplied so that the problem is well posed in the sense of Hadamard: a solution exists, it is unique, and it depends continuously on the data. For unsteady problems an initial condition is also needed. The questions for the numerical method are:

1. What kind of condition belongs on each part of the boundary, and how many conditions for a system of equations?
2. How is it imposed in the discrete equations, with an accuracy that does not degrade the interior scheme?
3. How are physical boundaries (a wall, a fan, an open outflow) and artificial ones (the edge of a truncated domain) represented?

An implementation is acceptable when the discrete problem has a unique solution, the observed order of accuracy of the whole solution equals that of the interior scheme, and changing the position of artificial boundaries does not change the quantities of interest.

## Mathematical Types

For a scalar $\phi$ with outward unit normal $\mathbf{n}$ on the boundary, the three standard linear conditions are:

| Type | Form | Physical examples |
| --- | --- | --- |
| Dirichlet (first kind) | $\phi = g$ | Prescribed wall temperature; inlet velocity; no-slip wall $\mathbf{u} = \mathbf{u}_{\mathrm{wall}}$ |
| Neumann (second kind) | $\partial\phi/\partial n = g$ | Prescribed heat flux $`-k\,\partial T/\partial n = q`$; insulated wall or symmetry plane ($g = 0$); fully developed outflow |
| Robin (third kind, mixed) | $`a\phi + b\,\partial\phi/\partial n = g`$ | Convective heat transfer $`-k\,\partial T/\partial n = h_c(T - T_\infty)`$; partially reflecting outflow |

Different parts of the boundary can carry different types. If only Neumann conditions are imposed on an elliptic equation, the solution is determined only up to an additive constant and exists only if the data are compatible. For $-\nabla^2\phi = f$ with $\partial\phi/\partial n = g$ on the whole boundary, integrating over $\Omega$ and applying the divergence theorem gives the compatibility condition

```math
\int_\Omega f \, dV + \oint_{\partial\Omega} g \, dA = 0
```

The pressure equation of incompressible flow with velocity prescribed on every boundary is exactly this case: the discrete matrix is singular with the constant vector in its null space, global mass conservation must hold to round-off, and the pressure level is fixed by a reference value or a zero-mean constraint.

## How Many Conditions, and Where

The number and location of the conditions follow from the type of the equation.

| Type | Conditions |
| --- | --- |
| Elliptic | One condition (Dirichlet, Neumann or Robin) at every point of a closed boundary |
| Parabolic | An initial condition, plus one condition at every point of the spatial boundary at all times |
| Hyperbolic | An initial condition, plus one condition for each characteristic that enters the domain through the boundary, and none for characteristics that leave it |

The hyperbolic rule is the subtle one. For the advection equation $`\partial\phi/\partial t + a\,\partial\phi/\partial x = 0`$ on $0 < x < L$ with $a > 0$, information travels to the right along the characteristics $dx/dt = a$. A value must be prescribed at the inflow $x = 0$; at the outflow $x = L$ the solution is determined by the interior, and prescribing a value there over-determines the problem. The discrete scheme still needs something at the outflow, but that is a numerical boundary condition, typically extrapolation from the interior, not a physical one.

### Characteristic Count for the Euler Equations

For the Euler equations, the characteristic speeds normal to a boundary are $u_n - c$, $u_n$ (for entropy and, in 2D and 3D, the tangential velocity components) and $u_n + c$, where $u_n$ is the velocity component along the inward normal and $c$ the speed of sound. The number of conditions equals the number of positive speeds, that is the number of waves entering the domain.

| Boundary | Normal Mach number | Incoming characteristics in 1D | Conditions in 3D | Usual choice of imposed quantities | Extrapolated from the interior |
| --- | --- | --- | --- | --- | --- |
| Supersonic inflow | $u_n/c > 1$ | 3 ($u_n - c$, $u_n$, $u_n + c$ all positive) | 5 | All variables, e.g. $\rho$, $\mathbf{u}$, $p$ | Nothing |
| Subsonic inflow | $0 < u_n/c < 1$ | 2 ($u_n$, $u_n + c$) | 4 | Total pressure, total temperature and flow direction, or $\rho$ and $\mathbf{u}$ | One quantity, e.g. the outgoing Riemann invariant or static pressure |
| Subsonic outflow | $-1 < u_n/c < 0$ | 1 ($u_n + c$) | 1 | Static pressure | Density and velocity |
| Supersonic outflow | $u_n/c < -1$ | 0 | 0 | Nothing | All variables |
| Inviscid wall | $u_n = 0$ | 1 | 1 | $\mathbf{u}\cdot\mathbf{n} = 0$ | The other variables |

At a subsonic far-field boundary of an external flow, a common implementation uses the 1D Riemann invariants $J^\pm = u_n \pm 2c/(\gamma - 1)$ normal to the boundary: the invariant that enters is computed from the free stream and the one that leaves from the interior, and the two are combined to give $u_n$ and $c$ at the boundary. The viscous terms of the Navier–Stokes equations add conditions: at a no-slip wall all velocity components are prescribed, together with a thermal condition (wall temperature or heat flux), and at an outflow the viscous stresses and heat flux normal to the boundary are usually set to zero.

### Incompressible Flow

In incompressible flow, pressure waves travel infinitely fast, so pressure behaves elliptically and every boundary needs a condition. The standard well-posed combination prescribes either the velocity (all components) or the normal traction, approximately the pressure, on each part of the boundary. Prescribing velocity everywhere leaves the pressure level undetermined and requires the inflow and outflow to balance; prescribing pressure at an outlet fixes the level.

## Implementation in Finite Differences

On a vertex-centred grid with nodes $x_0, \dots, x_N$ and spacing $h$, a Dirichlet condition is imposed exactly: the boundary value is known, and it is moved to the right-hand side of the equations at the neighbouring nodes. Neumann and Robin conditions involve a derivative at the boundary node $x_N$, which can be discretized in three ways. For $\partial\phi/\partial x = g$ at $x_N$:

1. The first-order one-sided difference $(\phi_N - \phi_{N-1})/h = g$. Its truncation error is $-\tfrac{h}{2}\phi''(x_N) + O(h^2)$.
2. The second-order one-sided difference $(3\phi_N - 4\phi_{N-1} + \phi_{N-2})/(2h) = g$. Its truncation error is $-\tfrac{h^2}{3}\phi'''(x_N) + O(h^3)$, but it widens the stencil and breaks the tridiagonal structure of the matrix.
3. A ghost point $x_{N+1} = x_N + h$ outside the domain. The central difference $(\phi_{N+1} - \phi_{N-1})/(2h) = g$, with truncation error $\tfrac{h^2}{6}\phi'''$, defines the ghost value $\phi_{N+1} = \phi_{N-1} + 2hg$, which is substituted into the interior equation written at the boundary node. The PDE is then enforced on the boundary as well, and the matrix keeps its structure.

A Robin condition $\partial\phi/\partial x + \beta\phi = \gamma$ is handled the same way, with $g$ replaced by $\gamma - \beta\phi_N$, which adds $2h\beta$ to the diagonal coefficient of node $N$.

The order of the boundary closure matters for the whole solution, not only near the boundary. For elliptic and parabolic problems an $O(h)$ boundary error spreads through the entire domain: the solution is coupled everywhere, so the global error becomes $O(h)$ even if the interior is second order. For hyperbolic problems, Gustafsson (1975) showed that a boundary closure one order lower than the interior scheme does not reduce the global order. The safe rule in practice is to use boundary treatments of the same order as the interior scheme and to check the observed order with a manufactured solution.

The figure compares the treatments for the cooling-fin equation $-\theta'' + m^2\theta = 0$ on $(0, 1)$ with $m = 1$, a prescribed heat flux $-\theta'(0) = 1$ at the base (Neumann) and convective loss $`-\theta'(1) = \mathrm{Bi}\,\theta(1)`$ with $\mathrm{Bi} = 2$ at the tip (Robin).

![Ghost-node and ghost-cell stencils, solutions on four intervals, and error against grid spacing for four boundary treatments](../../../scripts/algorithms/ghost_cell_boundary_conditions/ghost_cell_boundary_conditions.png)

With one-sided differences at both ends the finite-difference solution converges at first order and is 18 times less accurate than the ghost-node solution on just four intervals; on 512 intervals the gap is a factor of about 2000 ($8.7 \times 10^{-4}$ against $4.1 \times 10^{-7}$). Panel (b) shows the boundary error shifting the whole solution, not only the end values.

## Implementation in Finite Volumes

In a cell-centred finite-volume method the unknowns are cell averages and the boundary coincides with cell faces, so a boundary condition enters as the flux through the boundary face. Two equivalent views are used.

### Boundary-Face Fluxes

For the diffusive flux $`-\Gamma\,\partial\phi/\partial n`$ through a boundary face $b$ of area $A_b$ adjacent to cell $P$, whose centre is at distance $\delta = h/2$ from the face:

| Condition | Diffusive flux out of cell $P$ | Remarks |
| --- | --- | --- |
| Dirichlet $\phi_b = g$ | $-\Gamma A_b (g - \phi_P)/\delta$ | Half-cell distance $\delta$, not $h$ |
| Neumann $`-\Gamma\,\partial\phi/\partial n = q`$ | $q A_b$ | Exact; the flux is the data |
| Robin $`-\Gamma\,\partial\phi/\partial n = h_c(\phi_b - \phi_\infty)`$ | $A_b(\phi_P - \phi_\infty)/(1/h_c + \delta/\Gamma)$ | Wall and film resistances in series |

The convective flux $\dot{m}_b\phi_b$ needs the face value $\phi_b$. At an inflow it is the prescribed value; at an outflow it is taken from the interior, $\phi_b = \phi_P$ (upwind), which is equivalent to a zero-gradient condition.

A frequent mistake is to use the cell value as the face value in the Robin flux, $h_c(\phi_P - \phi_\infty)$. It ignores the resistance of the half cell between the centre and the face and is first order. The fin example shows the consequence: on 512 cells the error of this shortcut is $3.3 \times 10^{-4}$, against $7.9 \times 10^{-8}$ with the correct series resistance, and the observed orders are 1.00 and 2.00.

### Ghost Cells

The alternative is to surround the mesh with one or more layers of ghost (halo) cells and set their values before each iteration so that the interior flux formula, applied unchanged at the boundary face, produces the required condition. With the boundary face midway between $P$ and the ghost cell $G$, and a linear profile between them:

| Condition | Ghost value |
| --- | --- |
| Dirichlet $\phi_b = g$ | $\phi_G = 2g - \phi_P$ |
| Neumann $\partial\phi/\partial n = g$ | $\phi_G = \phi_P + hg$ |
| No-slip wall moving at $\mathbf{u}_w$ | $\mathbf{u}_G = 2\mathbf{u}_w - \mathbf{u}_P$ |
| Slip wall or symmetry plane | Normal velocity reversed, $u_{n,G} = -u_{n,P}$; tangential velocity and scalars copied |
| Periodic | Values copied from the cells adjacent to the opposite periodic boundary |
| Supersonic outflow | All values copied from $P$ (zeroth-order extrapolation) |

For the Dirichlet case the interior diffusive flux $\Gamma(\phi_P - \phi_G)/h$ becomes $2\Gamma(\phi_P - g)/h$, identical to the face-flux formula with $\delta = h/2$; the two views give the same discrete equations. Ghost cells are convenient for wide stencils: a second-order MUSCL reconstruction needs two ghost layers and a fifth-order WENO scheme three. In compressible solvers the ghost state is combined with the interior state by the same Riemann solver as at interior faces, so a slip wall is a mirror state and the Riemann solver returns a zero mass flux. The [Supersonic Forward-Facing Step](../../../scripts/simulations/supersonic_forward_facing_step/) simulation uses two ghost layers in exactly this way for its inflow, outflow and walls.

## Physical Boundary Conditions for Incompressible Flow

| Boundary | Velocity | Pressure | Transported scalars and turbulence quantities |
| --- | --- | --- | --- |
| Velocity inlet | Prescribed (Dirichlet), uniform or a measured or fully developed profile | Zero normal gradient, or extrapolated from the interior | Prescribed $T$; $k$ and $\varepsilon$ or $\omega$ from a turbulence intensity and a length scale |
| Pressure outlet | Zero normal gradient $\partial\mathbf{u}/\partial n = 0$ | Prescribed static pressure (Dirichlet) | Zero normal gradient; values to use if flow re-enters (backflow) |
| Total-pressure inlet | Direction prescribed, magnitude from $p_0 = p + \tfrac{1}{2}\rho\lVert\mathbf{u}\rVert^2$ | Static pressure follows from the interior | As for a velocity inlet |
| No-slip wall | $\mathbf{u} = \mathbf{u}_{\mathrm{wall}}$ (zero for a stationary wall) | Zero normal gradient (approximation of the wall-normal momentum balance) | Wall temperature or heat flux; $k = 0$; $\omega$ from its near-wall asymptote or a wall function |
| Slip wall or symmetry plane | $\mathbf{u}\cdot\mathbf{n} = 0$, zero normal gradient of tangential components | Zero normal gradient | Zero normal gradient |
| Periodic pair | $\phi(\mathbf{x}) = \phi(\mathbf{x} + \mathbf{L})$ for every variable | Periodic, or periodic plus a prescribed mean pressure drop to drive the flow | Periodic |

Placement matters as much as type. A velocity inlet should be far enough upstream that the flow there is not influenced by the body; a pressure outlet should be where the flow leaves the domain everywhere and is close to fully developed. An outlet that cuts through a recirculation zone produces backflow, which the zero-gradient condition cannot handle and which often stalls convergence. The [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/) simulation, for example, places its zero-gradient outlet 48 step heights downstream of a parabolic inlet, about eight times the length of the recirculation zone.

### Wall Functions

Resolving the viscous sublayer of a turbulent boundary layer needs the first cell centre at $y^+ = u_\tau y/\nu \approx 1$. Wall functions avoid this by placing the first cell centre in the logarithmic layer, $30 \lesssim y^+ \lesssim 300$, and computing the wall shear stress from the log law $u^+ = \kappa^{-1}\ln(Ey^+)$ instead of from a velocity gradient; the turbulence quantities in the wall cell are set from equilibrium relations. They are a boundary condition for the momentum and turbulence equations, valid only when the first cell lies in the log layer and the boundary layer is close to equilibrium. The theory is in [RANS Equations](../../fluid_mechanics/turbulence/rans_equations.md), the choice of wall treatment in [Turbulence Modeling in CFD](./turbulence_modeling.md), and mesh design in [Boundary Layer Meshing Guide](../../../practice/mesh_generation/boundary_layers.md).

## Artificial Boundaries: Outflow and Far Field

Most computational domains are truncations of a larger or unbounded region, and their outer boundaries are not physical. Ideally they are transparent: waves and vortices should leave without reflection, and the solution inside should be the same as on a larger domain.

For steady incompressible flow, the zero-gradient outflow condition is adequate if the outlet is far enough downstream. For unsteady flows with vortices crossing the outlet (wakes, jets), a convective outflow condition

$$
\frac{\partial\phi}{\partial t} + U_c \frac{\partial\phi}{\partial n} = 0
$$

with a convection velocity $U_c$, usually the mean outflow velocity, carries structures out of the domain with less reflection (Orlanski 1976 introduced a version in which $U_c$ is computed locally from the solution).

In compressible flow, acoustic waves reflect from a boundary that fixes the pressure. Characteristic non-reflecting conditions (Thompson 1987; Poinsot and Lele 1992) decompose the flux normal to the boundary into wave amplitudes and set the amplitude of the incoming wave to zero, or relax it slowly towards a target pressure so that the mean pressure does not drift. Where reflections must be suppressed further, sponge or absorbing layers damp the solution towards a reference state over a region near the boundary, and far-field boundaries of external flows are placed tens of body lengths away, where the Riemann-invariant condition described above performs well.

## Initial Conditions

For an unsteady calculation the initial condition is part of the problem. It must satisfy the constraints of the equations: an initial velocity field for incompressible flow must be divergence-free, or the first pressure solve projects it onto a divergence-free field and produces an unphysical pressure transient. It should also be consistent with the boundary conditions, since a jump between the initial field and a boundary value creates a discontinuity that a compressible solver propagates as waves. For statistically steady turbulent flows the initial transient, typically several flow-through times, is discarded before averages are collected.

For a steady calculation the initial field is only the starting guess of an iteration. It affects whether and how fast the iteration converges, but not the converged solution, provided the solution is unique. Uniform free-stream values, a potential-flow solution or the solution on a coarser mesh are common choices; turbulence quantities must start positive and of plausible size.

## Key Takeaways

- Dirichlet, Neumann and Robin conditions prescribe the value, the normal derivative or a combination; pure Neumann problems need a compatibility condition and a reference value.
- Elliptic problems need one condition everywhere on the boundary; hyperbolic problems need one condition per incoming characteristic, which for the Euler equations gives 5, 4, 1 and 0 conditions at supersonic inflow, subsonic inflow, subsonic outflow and supersonic outflow in 3D.
- A first-order boundary closure makes the whole solution of an elliptic or parabolic problem first order; ghost points, ghost cells and second-order one-sided differences avoid this.
- In finite volumes a boundary condition is a boundary-face flux; ghost cells give the same equations and suit wide stencils and Riemann solvers.
- Incompressible solvers prescribe velocity or pressure on each boundary; outlets belong where the flow leaves everywhere.
- Artificial boundaries should be transparent: zero-gradient for steady flow far downstream, convective or characteristic non-reflecting conditions for unsteady flow.

## Related Scripts

- [Ghost-Cell Boundary Conditions](../../../scripts/algorithms/ghost_cell_boundary_conditions/): compares first-order and second-order ways of imposing Neumann and Robin boundary conditions in finite-difference and finite-volume discretizations of a 1D diffusion problem.
- [Method of Manufactured Solutions](../../../scripts/algorithms/method_of_manufactured_solutions/): verifies a second-order finite-difference Poisson solver with the method of manufactured solutions (MMS) and shows how the same test exposes a first-order boundary treatment.
- [Supersonic Forward-Facing Step](../../../scripts/simulations/supersonic_forward_facing_step/): solves the 2D compressible Euler equations for a Mach 3 stream that meets a forward-facing step in a wind tunnel, the benchmark of Woodward and Colella (1984), and animates the shock pattern that forms.
- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.

## Exercises

**Exercise 1.** How many boundary conditions does the 3D Euler system need at (a) a subsonic inlet with $Ma = 0.5$, (b) a subsonic outlet with $Ma = 0.5$, (c) a supersonic inlet with $Ma = 2$ and (d) a supersonic outlet with $Ma = 2$? What would go wrong if all five variables were prescribed at the subsonic outlet?

<details>
<summary>Answer</summary>

The normal characteristic speeds are $u_n - c$, $u_n$ (three times) and $u_n + c$; count those entering the domain.

(a) $u_n = 0.5c$ into the domain: $u_n > 0$ and $u_n + c > 0$ enter, $u_n - c = -0.5c$ leaves, so 4 conditions.

(b) Leaving at $0.5c$: only the acoustic wave travelling upstream at speed $c - 0.5c$ enters, so 1 condition (usually static pressure).

(c) All five speeds are positive: 5 conditions.

(d) None enter: 0 conditions; everything is extrapolated.

Prescribing five values at a subsonic outlet over-determines the problem: the four outgoing waves arriving from the interior are incompatible with the imposed values, and the scheme either reflects them back into the domain as spurious waves or fails to converge.

</details>

**Exercise 2.** Show by Taylor expansion that the one-sided difference $(\phi_N - \phi_{N-1})/h$ approximates $\phi'(x_N)$ with a leading error term of magnitude $\tfrac{h}{2}|\phi''(x_N)|$, and that the central difference across the boundary used to define the ghost value has error $O(h^2)$.

<details>
<summary>Answer</summary>

Expanding about $x_N$: $\phi_{N-1} = \phi_N - h\phi' + \tfrac{h^2}{2}\phi'' - \tfrac{h^3}{6}\phi''' + \dots$, so

```math
\frac{\phi_N - \phi_{N-1}}{h} = \phi' - \frac{h}{2}\phi'' + \frac{h^2}{6}\phi''' - \dots
```

so the error (approximation minus exact value) is $-\tfrac{h}{2}\phi'' + O(h^2)$: first order.

With $\phi_{N+1} = \phi_N + h\phi' + \tfrac{h^2}{2}\phi'' + \tfrac{h^3}{6}\phi''' + \dots$, the even terms cancel in the central difference:

```math
\frac{\phi_{N+1} - \phi_{N-1}}{2h} = \phi' + \frac{h^2}{6}\phi''' + O(h^4)
```

which is second order, provided $\phi$ is smooth enough to be extended past the boundary, which is what the ghost value assumes.

</details>

**Exercise 3.** Solve $-\phi'' = 2$ on $(0, 1)$ with $\phi(0) = 0$ and $\phi'(1) = 0$ by finite differences with $h = 1/2$ (nodes at 0, 0.5 and 1), once with the first-order one-sided Neumann condition and once with a ghost point. The exact solution is $\phi = 2x - x^2$.

<details>
<summary>Answer</summary>

The interior equation at $x = 0.5$ is $(-\phi_0 + 2\phi_1 - \phi_2)/h^2 = 2$, that is $2\phi_1 - \phi_2 = 0.5$.

One-sided: $\phi_2 - \phi_1 = 0$, so $\phi_1 = \phi_2 = 0.5$. The exact values are $\phi(0.5) = 0.75$ and $\phi(1) = 1$; the error at $x = 1$ is 50%.

Ghost point: $\phi_3 = \phi_1$, and the interior equation at node 2 becomes $(-2\phi_1 + 2\phi_2)/h^2 = 2$, that is $\phi_2 - \phi_1 = 0.25$. With the interior equation, $\phi_1 = 0.75$ and $\phi_2 = 1$, exact, because the solution is quadratic and every difference used is exact for quadratics.

</details>

**Exercise 4.** The pressure-correction equation in a closed lid-driven cavity is a Poisson equation with zero normal gradient on all walls. Explain why the discrete matrix is singular, what condition the right-hand side must satisfy, and two ways to obtain a unique solution.

<details>
<summary>Answer</summary>

With $\partial p/\partial n = 0$ everywhere, adding a constant to $p$ changes neither the equation nor the boundary conditions. The discrete matrix has the constant vector in its null space, so it is singular.

A solution exists only if the right-hand side is orthogonal to the null space of the transposed matrix, which for the usual symmetric discretization means its sum over all cells must vanish: the discrete form of $`\int_\Omega f\,dV + \oint g\,dA = 0`$. In the pressure-correction equation the right-hand side is the mass imbalance of each cell, whose sum is the net mass flux through the boundary, zero for a closed cavity up to round-off.

Uniqueness is obtained by fixing the value in one cell (replacing its equation by $p_{\mathrm{ref}} = 0$) or by imposing a zero mean, for example by subtracting the mean after each solve. Krylov solvers such as CG also converge on the singular system if the right-hand side is compatible, and the mean can be removed afterwards.

</details>

**Exercise 5.** A wall cell of a conduction solver has width $\Delta x = 0.01$ m, conductivity $k = 1$ W/(m K) and centre temperature $T_P = 60$ °C. The wall loses heat by convection with $h_c = 100$ W/(m² K) to air at $T_\infty = 20$ °C. Compute the wall heat flux and wall temperature with the series-resistance (ghost-cell) treatment and with the shortcut $T_b = T_P$. What dimensionless number decides whether the difference matters?

<details>
<summary>Answer</summary>

Series resistances: $q = (T_P - T_\infty)/(1/h_c + \Delta x/(2k)) = 40/(0.01 + 0.005) = 2667$ W/m². The wall temperature is $`T_b = T_P - q\,\Delta x/(2k) = 60 - 13.3 = 46.7`$ °C.

Shortcut: $q = h_c(T_P - T_\infty) = 4000$ W/m², 50% too high, with $T_b = 60$ °C.

The ratio of the two resistances is the cell Biot number $h_c\Delta x/k = 1$. When it is much smaller than 1 the half-cell resistance is negligible and the shortcut is harmless; when it is of order 1 or larger the shortcut is badly wrong, and it is always first order as $\Delta x \to 0$.

</details>

## References

- Ferziger, J. H., Perić, M., & Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
- Versteeg, H. K., & Malalasekera, W., *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed., Pearson Education, 2007.
- Hirsch, C., *Numerical Computation of Internal and External Flows, Volume 1: Fundamentals of Computational Fluid Dynamics*, 2nd ed., Butterworth-Heinemann, 2007.
- LeVeque, R. J., *Finite Volume Methods for Hyperbolic Problems*, Cambridge University Press, 2002.
- Gustafsson, B., "The convergence rate for difference approximations to mixed initial boundary value problems," *Mathematics of Computation*, 29(130), 396–406, 1975.
- Thompson, K. W., "Time dependent boundary conditions for hyperbolic systems," *Journal of Computational Physics*, 68(1), 1–24, 1987.
- Poinsot, T. J., & Lele, S. K., "Boundary conditions for direct simulations of compressible viscous flows," *Journal of Computational Physics*, 101(1), 104–129, 1992.
- Orlanski, I., "A simple boundary condition for unbounded hyperbolic flows," *Journal of Computational Physics*, 21(3), 251–269, 1976.
