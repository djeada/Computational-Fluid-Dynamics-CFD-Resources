# Pressure–Velocity Coupling

In incompressible flow the pressure has no evolution equation of its own. It is whatever field makes the velocity divergence-free, and computing it is the central difficulty of every incompressible finite-volume solver. This note derives the discrete problem, shows why storing pressure and velocity at the same points with linear interpolation lets a checkerboard pressure pass unnoticed, and covers the two remedies (staggered grids and Rhie–Chow interpolation) and the segregated algorithms built on them: SIMPLE, SIMPLEC, PISO, PIMPLE-type outer and inner loops, and projection methods. It follows the discretization of convection and diffusion in [Finite Volume Discretization](./discretization.md) and [Convection Schemes](./convection_schemes.md); compressible flows, where pressure follows from an equation of state, are treated with the methods of [Riemann Solvers and Godunov Methods](./riemann_solvers.md).

## Problem Statement

The incompressible Navier–Stokes equations for velocity $\mathbf{u}$ and pressure $p$, with constant density $\rho$ and kinematic viscosity $\nu$, are

$$
\nabla \cdot \mathbf{u} = 0,
\qquad \frac{\partial \mathbf{u}}{\partial t} + \nabla \cdot
(\mathbf{u}\mathbf{u}) = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u}
$$

in a domain $\Omega$, with velocity prescribed on inlets and walls and a static or total pressure prescribed on outlets (see [Boundary Conditions](../cfd/boundary_conditions.md)). The unknowns are the three velocity components and $p$; there are four equations, but none of them contains $\partial p/\partial t$. Pressure acts as a Lagrange multiplier for the constraint $\nabla \cdot \mathbf{u} = 0$. Taking the divergence of the momentum equation and using the constraint gives the pressure Poisson equation

```math
\nabla^2 p = -\rho\, \nabla \cdot \nabla \cdot (\mathbf{u}\mathbf{u})
```

which shows that pressure is determined instantaneously by the velocity field everywhere: it is elliptic, and a change anywhere is felt everywhere at once. If velocity is prescribed on the whole boundary, $p$ is fixed only up to a constant.

After discretization in space the momentum equations become $\mathbf{A}\mathbf{u} + \mathbf{G}p = \mathbf{b}$, with $\mathbf{A}$ the convection–diffusion (and time-derivative) matrix and $\mathbf{G}$ the discrete gradient, and continuity becomes $\mathbf{D}\mathbf{u} = 0$ with the discrete divergence $\mathbf{D}$. Together they form the saddle-point system

```math
\begin{pmatrix} \mathbf{A} & \mathbf{G} \\ \mathbf{D} & \mathbf{0} \end{pmatrix}
\begin{pmatrix} \mathbf{u} \\ p \end{pmatrix}
=
\begin{pmatrix} \mathbf{b} \\ 0 \end{pmatrix}
```

The zero block means that $p$ has no diagonal entry, so the Gauss–Seidel-type relaxations used for scalar transport cannot be applied to the coupled system, and $\mathbf{A}$ depends on $\mathbf{u}$, so the system is nonlinear. A solution is acceptable when the momentum residuals and the mass imbalance of every cell have fallen by several orders of magnitude and the quantities of interest (pressure drop, forces, a reattachment length) no longer change with further iterations. Two things make this hard: finding an efficient way to iterate on the coupled system, and choosing $\mathbf{D}$ and $\mathbf{G}$ so that the discrete problem determines a unique, smooth pressure.

### The Pressure Equation as a Schur Complement

Eliminating $\mathbf{u} = \mathbf{A}^{-1}(\mathbf{b} - \mathbf{G}p)$ from the continuity equation gives the exact discrete pressure equation

```math
\left(\mathbf{D}\,\mathbf{A}^{-1}\mathbf{G}\right) p = \mathbf{D}\,\mathbf{A}^{-1}\mathbf{b}
```

The matrix $\mathbf{D}\mathbf{A}^{-1}\mathbf{G}$ is dense because $\mathbf{A}^{-1}$ is. Every segregated algorithm in this note replaces $\mathbf{A}^{-1}$ in it with something cheap, usually the inverse of the diagonal of $\mathbf{A}$, which gives a sparse Laplacian-like matrix for the pressure (or a pressure correction). The algorithms differ in how they make up for that approximation: under-relaxation and outer iterations in SIMPLE, a modified diagonal in SIMPLEC, extra correction steps in PISO, and a small time step in projection methods.

## Checkerboard Pressure on Collocated Grids

A collocated grid stores $\mathbf{u}$ and $p$ at the same cell centres, which is the natural choice for unstructured meshes. On a uniform 1D grid with linear interpolation of face pressures, $p_{i+1/2} = \frac{1}{2}(p_i + p_{i+1})$, the pressure force on cell $i$ per unit volume is

```math
\left(\frac{\partial p}{\partial x}\right)_i \approx \frac{p_{i+1/2} - p_{i-1/2}}{\Delta x} = \frac{p_{i+1} - p_{i-1}}{2\Delta x}
```

The value $p_i$ does not appear. For the checkerboard field $p_i = (-1)^i$, and in 2D $p_{ij} = (-1)^{i+j}$, this gradient is zero in every cell, so a checkerboard can be added to any solution without changing the momentum equations. The same happens to continuity: interpolating cell velocities linearly to the faces gives $(u_{i+1} - u_{i-1})/(2\Delta x)$, and the pressure equation built from these two operators is the wide Laplacian

```math
(\mathbf{D}\mathbf{G}\,p)_i = \frac{p_{i+2} - 2p_i + p_{i-2}}{4\Delta x^2}
```

which couples only every second cell. For a Fourier mode $p_j = e^{\mathrm{i}\theta j}$ its eigenvalue is $-\sin^2\theta/\Delta x^2$, which vanishes at $\theta = \pi$ as well as at $\theta = 0$. The compact Laplacian $(p_{i+1} - 2p_i + p_{i-1})/\Delta x^2$ has eigenvalue $-4\sin^2(\theta/2)/\Delta x^2$, zero only for a constant.

![Checkerboard field, operators applied to it, and Laplacian spectra](../../../scripts/plots/checkerboard_pressure/checkerboard_pressure.png)

The top right panel shows that the interpolated gradient and the wide Laplacian of a 1D checkerboard are exactly zero while the compact Laplacian is $-4p_i/\Delta x^2$. The bottom panels show the consequence for the spectra: the wide-stencil operator has two zero eigenvalues in 1D and four on a periodic 2D grid (the constant and the checkerboards in $x$, in $y$ and in both), and it damps every mode near $\theta = \pi$ only weakly. In practice the result is a pressure field with grid-scale oscillations superposed on the correct solution, or an iteration that does not converge. The remedy is to make $\mathbf{G}$ and $\mathbf{D}$ act across single faces, either by moving the velocity unknowns or by changing how face velocities are interpolated.

## Staggered Grids

The marker-and-cell (MAC) arrangement of Harlow and Welch (1965) stores pressure at cell centres and each velocity component at the centres of the faces normal to it: $u$ on the $x$-faces at $(i + 1/2, j)$, $v$ on the $y$-faces at $(i, j + 1/2)$. Each velocity has its own control volume, shifted half a cell from the pressure cell, so

1. the pressure force on $u_{i+1/2,j}$ is $`(p_{i,j} - p_{i+1,j})\,\Delta y`$, a difference across one face;
2. the continuity equation of pressure cell $(i, j)$ uses the face velocities directly, $`(u_{i+1/2,j} - u_{i-1/2,j})\Delta y + (v_{i,j+1/2} - v_{i,j-1/2})\Delta x = 0`$;
3. the pressure equation is the compact five-point Laplacian, whose only null vector is the constant.

A checkerboard pressure now produces a nonzero force on every face velocity, so it is suppressed. The costs are three sets of control volumes in 3D, interpolation of velocities to the faces of the shifted momentum cells for the convective fluxes, and awkward bookkeeping on curvilinear or unstructured meshes. Staggered grids remain common in structured research codes and in teaching; the [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/) simulation and the [SIMPLE in a 1D Converging Nozzle](../../../scripts/algorithms/simple_1d_nozzle/) example use them.

## Rhie–Chow Interpolation

Rhie and Chow (1983) kept all unknowns at cell centres and changed the face velocity used in the mass fluxes. The discrete momentum equation of cell $P$ with volume $V_P$ is

```math
a_P\,\mathbf{u}_P = \sum_{nb} a_{nb}\,\mathbf{u}_{nb} + \mathbf{b}_P - V_P\,(\nabla p)_P
\quad\Longrightarrow\quad
\mathbf{u}_P = \frac{\mathbf{H}_P}{a_P} - \frac{V_P}{a_P}(\nabla p)_P,
\qquad \mathbf{H}_P = \sum_{nb} a_{nb}\mathbf{u}_{nb} + \mathbf{b}_P
```

At a face $f$ between $P$ and its neighbour $N$, the idea is to interpolate the first term and the coefficient $V/a$, but to evaluate the pressure gradient directly across the face from the two adjacent values:

```math
\mathbf{u}_f \cdot \mathbf{n}_f = \overline{\left(\frac{\mathbf{H}}{a}\right)}_f \cdot \mathbf{n}_f - \overline{\left(\frac{V}{a}\right)}_f \frac{p_N - p_P}{|\mathbf{d}_{PN}|}
```

where the overbar is linear interpolation between $P$ and $N$ and $\mathbf{d}_{PN}$ joins the two cell centres. Written in terms of the interpolated cell velocities, this is

```math
\mathbf{u}_f \cdot \mathbf{n}_f = \overline{\mathbf{u}}_f \cdot \mathbf{n}_f - \overline{\left(\frac{V}{a}\right)}_f \left[\frac{p_N - p_P}{|\mathbf{d}_{PN}|} - \overline{(\nabla p)}_f \cdot \mathbf{n}_f\right]
```

The bracket is the difference between a compact and a wide pressure gradient. On a uniform 1D grid, at the face between cells $P$ and $E$,

```math
\frac{p_E - p_P}{\Delta x} - \frac{1}{2}\left(\frac{p_E - p_W}{2\Delta x} + \frac{p_{EE} - p_P}{2\Delta x}\right)
= -\frac{p_{EE} - 3p_E + 3p_P - p_W}{4\Delta x}
\approx -\frac{\Delta x^2}{4}\frac{\partial^3 p}{\partial x^3}
```

so the correction is a third-derivative pressure dissipation that vanishes as $\Delta x^2$ for smooth fields and does not lower the formal second-order accuracy. For a checkerboard it is as large as the compact gradient itself, $2/\Delta x$ per unit amplitude, so the mass fluxes respond to it and the pressure equation built from these face velocities contains the compact Laplacian. Because the face fluxes, not the cell velocities, satisfy continuity, the solver should transport momentum and scalars with these face fluxes.

Two refinements are standard. The plain formula makes the converged solution depend slightly on the momentum under-relaxation factor and, in transient runs, on the time step, because $a_P$ contains both; practical implementations interpolate the relaxation and time-derivative contributions consistently so that the steady result is independent of them. On non-orthogonal meshes the face-normal gradient $(p_N - p_P)/|\mathbf{d}_{PN}|$ is supplemented by the usual non-orthogonal correction.

## The SIMPLE Algorithm

SIMPLE (Semi-Implicit Method for Pressure-Linked Equations, Patankar and Spalding 1972) solves the momentum equations with a guessed pressure and then corrects pressure and velocity so that continuity holds. On a staggered grid, or a collocated grid with Rhie–Chow fluxes, the discrete momentum equation for the velocity normal to face $e$ is

```math
a_e u_e = \sum_{nb} a_{nb} u_{nb} + b_e + (p_P - p_E) A_e
```

with $A_e$ the face area.

### Deriving the Pressure-Correction Equation

1. Solve the momentum equations with the current pressure $`p^*`$ to obtain $`u^*`$, which satisfies $`a_e u_e^* = \sum a_{nb} u_{nb}^* + b_e + (p_P^* - p_E^*)A_e`$ but not continuity.

2. Write the corrected fields as $p = p^* + p'$ and $u = u^* + u'$. Subtracting the two momentum equations gives the exact relation $a_e u_e' = \sum a_{nb} u_{nb}' + (p_P' - p_E')A_e$.

3. Drop the neighbour term $\sum a_{nb} u_{nb}'$. This is the approximation that gives SIMPLE its name and its need for under-relaxation. The velocity correction is then local:

   ```math
   u_e' = d_e\,(p_P' - p_E'),
   \qquad d_e = \frac{A_e}{a_e}
   ```

4. Require the corrected face velocities to satisfy continuity for pressure cell $P$, $`\sum_f \rho\, u_f A_f\, \mathrm{sign}_f = 0`$ (outflow positive). Substituting $u = u^* + u'$ gives

   ```math
   a_P\,p_P' = \sum_{nb} a_{nb}\,p_{nb}' + b,
   \qquad a_{nb} = \rho\,d_f\,A_f,
   \qquad a_P = \sum_{nb} a_{nb},
   \qquad b = \sum_{f,\,\mathrm{in}} \rho\,u_f^* A_f - \sum_{f,\,\mathrm{out}} \rho\,u_f^* A_f
   ```

   The source $b$ is the mass imbalance of the cell left by $u^*$. The matrix is a compact, symmetric, diagonally dominant discrete Laplacian, solved with conjugate gradients or multigrid (see [Direct and Iterative Solvers](../cfd/direct_and_iterative_solvers.md)).

### One SIMPLE Iteration

1. Assemble the momentum equations from the current velocity (for the convective coefficients) and pressure, and under-relax them.
2. Solve them for $`u^*`$, $`v^*`$, $w^*$, usually only approximately (a few sweeps or a loose tolerance).
3. Compute the coefficients $d_f$ and the face mass fluxes of $u^*$ (with Rhie–Chow interpolation on a collocated grid), and assemble the pressure-correction equation.
4. Solve for $p'$ more accurately than the momentum equations, since it carries the continuity constraint.
5. Correct the face fluxes and velocities with the full $p'$, $`u = u^* + d\,\Delta p'`$, so that the fluxes satisfy continuity.
6. Correct the pressure with under-relaxation, $p = p^* + \alpha_p p'$.
7. Solve the other transport equations (energy, turbulence quantities) with the corrected fluxes, check convergence, and return to step 1.

### Under-Relaxation

Dropping $\sum a_{nb} u_{nb}'$ attributes the whole mass imbalance of a cell to its own pressure, so $p'$ is too large and the uncorrected iteration overshoots and usually diverges. SIMPLE therefore relaxes both fields. Momentum is relaxed implicitly, which keeps the steady solution unchanged:

```math
\frac{a_e}{\alpha_u}\,u_e = \sum_{nb} a_{nb} u_{nb} + b_e + (p_P - p_E) A_e + \frac{1 - \alpha_u}{\alpha_u}\,a_e\,u_e^{\mathrm{old}}
```

and $d_e = A_e\alpha_u/a_e$ follows from the relaxed coefficient. Pressure is relaxed explicitly, $p = p^* + \alpha_p p'$. Typical values are $\alpha_u \approx 0.7$ and $\alpha_p \approx 0.3$, and a common heuristic is to keep $\alpha_u + \alpha_p \approx 1$. The heuristic has a reason, derived in the SIMPLEC section below, but it is a guideline, not a stability bound.

![SIMPLE nozzle solution, grid convergence and relaxation study](../../../scripts/algorithms/simple_1d_nozzle/simple_1d_nozzle.png)

The figure comes from the converging-nozzle problem of Versteeg and Malalasekera (2007, Example 6.2), solved with SIMPLE on a staggered grid. The top row shows that the converged mass flow approaches Bernoulli's value 0.44721 kg/s at first order: first-order upwinding gives 37 % too much on 5 pressure nodes and 0.5 % on 257. The bottom row shows that the converged solution does not depend on the relaxation factors but the path to it does. On 33 nodes, $\alpha_u = \alpha_p = 0.8$ diverges, $0.7/0.3$ converges in 68 iterations and $0.8/0.2$ in 101. The iteration map shows the fastest settings (45 to 57 iterations) at $\alpha_u + \alpha_p$ between about 1.05 and 1.3, next to the boundary beyond which the iteration fails; $\alpha_u + \alpha_p = 1$ stays on the safe side of it.

### SIMPLER

Patankar's SIMPLER (1980) first solves a pressure equation for the pressure itself, built from the pseudo-velocities $\mathbf{H}/a$, and uses $p'$ only to correct velocities. It needs no pressure under-relaxation and often fewer iterations, at the cost of one more linear solve per iteration; SIMPLEC achieves similar gains more cheaply and is more common today.

## SIMPLEC

SIMPLE-Consistent (Van Doormaal and Raithby 1984) makes a more consistent approximation in step 3. Subtracting $\sum a_{nb} u_e'$ from both sides of the exact correction equation gives

```math
\left(a_e - \sum_{nb} a_{nb}\right) u_e' = \sum_{nb} a_{nb}\left(u_{nb}' - u_e'\right) + (p_P' - p_E') A_e
```

The neighbour term now involves only differences of corrections, which are smaller than the corrections themselves, and dropping it gives

```math
u_e' = d_e^{C}\,(p_P' - p_E'),
\qquad d_e^{C} = \frac{A_e}{a_e/\alpha_u - \sum_{nb} a_{nb}}
```

with the under-relaxed diagonal in the denominator, which keeps it positive. The pressure-correction equation is the same as in SIMPLE with $d^C$ in place of $d$, and the pressure is usually not under-relaxed ($\alpha_p = 1$).

The two algorithms are closely related. Without a transient term or a linearized source, $\sum a_{nb} = a_e$ at convergence, so

```math
d^{C} = \frac{A_e}{a_e(1/\alpha_u - 1)} = \frac{d^{S}}{1 - \alpha_u},
\qquad d^{S} = \frac{\alpha_u A_e}{a_e}
```

The pressure-correction matrix scales with $d$, so $`p'^{C} = (1 - \alpha_u)\,p'^{S}`$, while the velocity corrections $`d\,\Delta p'`$ are identical. SIMPLEC with $\alpha_p = 1$ therefore updates the pressure exactly as SIMPLE with $\alpha_p = 1 - \alpha_u$, which is where the rule $\alpha_u + \alpha_p = 1$ comes from. The last panel of the nozzle figure confirms it: the two curves of iteration count against $\alpha_u$ almost coincide. Where the equivalence breaks down (transient terms, strong sources, skewed meshes), SIMPLEC is usually the more robust of the two.

## PISO

PISO (Pressure-Implicit with Splitting of Operators, Issa 1986) was designed for transient calculations, where a time step is small enough that the nonlinearity and the coupling can be resolved without outer iterations. Each time step:

1. Predictor: assemble and solve the momentum equations with the old pressure $p^n$, without under-relaxation, giving $\mathbf{u}^*$.

2. First corrector: solve the SIMPLE pressure-correction equation for $p'$ and correct the velocity and fluxes to $`\mathbf{u}^{**}`$, which satisfies continuity.

3. Second corrector: the neighbour corrections $\sum a_{nb} u_{nb}'$ dropped in step 2 are now known, so the velocity is written as

   ```math
   u_e^{***} = u_e^{**} + \frac{\sum_{nb} a_{nb}\,(u_{nb}^{**} - u_{nb}^{*})}{a_e} + d_e\,(p_P'' - p_E'')
   ```

   and continuity for $`u^{***}`$ gives a second pressure-correction equation for $p''$ with the same matrix and a new source.

4. Repeat the corrector as often as needed; two correctors are usual. The momentum matrix is not re-assembled within the step, so the nonlinearity is lagged by one time step.

Issa showed that with two correctors the splitting error is of the order of the time-discretization error for small time steps. PISO is efficient when the Courant number $C = |\mathbf{u}|\Delta t/\Delta x$ is around 1 or smaller; at larger time steps the lagged convection coefficients make it inaccurate or unstable.

## Outer and Inner Loops (PIMPLE)

Many solvers combine the two ideas into a transient algorithm with two nested loops, known in OpenFOAM as PIMPLE:

1. An outer loop, repeated within each time step, re-assembles the momentum equations with the latest velocity, can under-relax them, and solves them as in SIMPLE.
2. An inner loop of PISO correctors, typically one to three, solves the pressure equation and corrects the fluxes.
3. The outer loop ends when the residuals at the start of an outer iteration fall below a tolerance or after a fixed number of iterations.

With one outer iteration this is PISO. With several outer iterations and under-relaxation it converges the nonlinear problem within every time step, which allows Courant numbers well above 1 at the cost of more work per step; a steady problem marched in pseudo-time with large steps behaves like SIMPLE.

## Projection Methods

Fractional-step or projection methods (Chorin 1968) split each time step into a momentum step that ignores the constraint and a projection onto divergence-free fields. With explicit convection and diffusion:

1. Predictor: $`\mathbf{u}^* = \mathbf{u}^n + \Delta t\left[-\nabla\cdot(\mathbf{u}\mathbf{u}) + \nu\nabla^2\mathbf{u}\right]^n`$, with the velocity boundary conditions applied to $\mathbf{u}^*$.
2. Pressure: solve $\nabla^2 p^{n+1} = \frac{\rho}{\Delta t}\nabla\cdot\mathbf{u}^*$ with $\partial p/\partial n = 0$ on walls.
3. Corrector: $\mathbf{u}^{n+1} = \mathbf{u}^* - \frac{\Delta t}{\rho}\nabla p^{n+1}$.

The corrected field is divergence-free in the discrete sense only if the discrete Laplacian of step 2 equals the product $\mathbf{D}\mathbf{G}$ of the divergence and gradient used in steps 2 and 3. On a staggered grid it does, and the method is an exact projection. On a collocated grid, using the compact Laplacian with central-difference $\mathbf{D}$ and $\mathbf{G}$ gives an approximate projection: the mismatch leaves a divergence of order $\Delta x^2$, and it is exactly the Rhie–Chow-type term that keeps the checkerboard out of the pressure.

The pressure obtained this way is first-order accurate in time, and the artificial condition $\partial p/\partial n = 0$ creates a numerical boundary layer in the pressure. Incremental schemes, which keep $\nabla p^n$ in the predictor and solve for the increment $p^{n+1} - p^n$, improve the pressure to second order. Projection methods are the standard choice for time-accurate DNS and LES with small time steps, where one pressure solve per step is cheaper than outer iterations; for steady problems SIMPLE-family methods converge faster.

The [Lid-Driven Cavity](../../../scripts/simulations/lid_driven_cavity/) simulation uses this explicit projection on a collocated $129 \times 129$ grid: central differences for $\mathbf{D}$, $\mathbf{G}$ and the convective terms, the compact five-point Laplacian for the pressure, and 50 Jacobi sweeps per time step started from the previous pressure, with the mean pressure removed because every wall carries a Neumann condition. Its velocity is therefore divergence-free only approximately: the Poisson equation is not solved to convergence in each step, and the wide and compact operators differ.

## Boundary Conditions for the Pressure Correction

The boundary conditions of the physical problem translate into conditions on the correction:

| Boundary | Velocity | Pressure | Pressure correction |
| --- | --- | --- | --- |
| Wall, velocity inlet | prescribed | extrapolated from the interior | no correction of the boundary flux, $d_f = 0$: zero normal gradient of $p'$ |
| Static-pressure outlet | zero normal gradient | prescribed | $p' = 0$ on the boundary face |
| Total-pressure inlet | direction prescribed, magnitude from $p_0 = p + \frac{1}{2}\rho\lvert\mathbf{u}\rvert^2$ | follows from $p_0$ and $\mathbf{u}$ | $p' = 0$ or a linearized relation between $p'$ and $u'$ |
| Symmetry plane | zero normal component | zero normal gradient | zero normal gradient |

When velocity is prescribed on every boundary, as in a closed cavity, the pressure-correction matrix is singular with the constant vector as its null vector. The equation has a solution only if the cell sources $b$ sum to zero, which holds when the prescribed boundary fluxes balance, and the level must be fixed by setting $p'$ in one reference cell or removing the mean. The converging-nozzle example uses a total-pressure inlet and a static-pressure outlet; the derivations behind each condition are in [Boundary Conditions](../cfd/boundary_conditions.md).

## Convergence Monitors

The algorithms above iterate until several monitors agree that the solution has stopped changing (see [Iterative Convergence](../cfd/iterative_convergence.md)):

- the continuity residual $\sum_P |b_P|$ of the pressure-correction equation, scaled by the inflow mass flux or by its value in the first iterations;
- the scaled residuals of the momentum equations, $`\sum_P |a_P u_P - \sum a_{nb} u_{nb} - b_P| \,/\, \sum_P |a_P u_P|`$;
- the global mass balance between inlets and outlets, which a converged SIMPLE solution satisfies to round-off;
- integral and point quantities: forces, pressure drop, a velocity at a probe or a separation length, which should be flat to the required number of digits.

Residuals typically have to fall three to five orders of magnitude. A continuity residual that stalls while the momentum residuals keep falling usually points to a boundary-condition inconsistency or an outlet cutting through a recirculation zone. The [Backward-Facing Step](../../../scripts/simulations/backward_facing_step_simple/) simulation stops when all three residuals have fallen to $10^{-3}$ of their maximum over the first 10 iterations and the global mass imbalance is below 0.5 %; its imbalance oscillates for hundreds of iterations, because pressure corrections travel slowly along a long channel.

## Comparison

| Method | Typical use | Relaxation | Work per iteration or step | Remarks |
| --- | --- | --- | --- | --- |
| SIMPLE | steady flows | $\alpha_u \approx 0.7$, $\alpha_p \approx 0.3$ | one momentum and one pressure solve per outer iteration | many outer iterations; robust |
| SIMPLEC | steady flows | $\alpha_u \approx 0.7$–0.9, $\alpha_p = 1$ | as SIMPLE | fewer iterations than SIMPLE in most flows |
| PISO | transient, $C \lesssim 1$ | none | one momentum and two pressure solves per time step | no outer iterations; nonlinearity lagged |
| PIMPLE (outer + inner loops) | transient, large $C$ | optional | several of the above per time step | converges each step; PISO with one outer iteration |
| Projection | time-accurate DNS, LES | none | one pressure solve per step (per stage) | exact projection only if the Laplacian equals $\mathbf{D}\mathbf{G}$ |
| Coupled solvers | steady, stiff coupling | small or none | one large block system per iteration | solve the saddle-point system directly with block preconditioners; memory-intensive |

## Key Takeaways

- Incompressible pressure is a Lagrange multiplier for $\nabla \cdot \mathbf{u} = 0$; the discrete problem is a saddle-point system whose pressure equation is the Schur complement $\mathbf{D}\mathbf{A}^{-1}\mathbf{G}$.
- On collocated grids, linear interpolation of pressure and velocity decouples odd and even cells; the checkerboard lies in the null space of the resulting wide Laplacian.
- Staggered grids and Rhie–Chow interpolation both give a compact pressure Laplacian; Rhie–Chow adds a third-derivative pressure term of order $\Delta x^2$ to the face fluxes.
- SIMPLE approximates $\mathbf{A}^{-1}$ by its diagonal and needs under-relaxation; SIMPLEC with $\alpha_p = 1$ is equivalent to SIMPLE with $\alpha_p = 1 - \alpha_u$ when $\sum a_{nb} = a_P$.
- PISO and projection methods are for time-accurate runs with small Courant numbers; outer iterations (PIMPLE) are needed for large time steps.
- The converged solution must not depend on the relaxation factors, and convergence is judged by the mass imbalance, the momentum residuals and the quantities of interest together.

## Related Scripts

- [Checkerboard Pressure on a Collocated Grid](../../../scripts/plots/checkerboard_pressure/): shows why a collocated finite-volume grid with linearly interpolated face pressures cannot see a checkerboard pressure field: the cell pressure gradient and the pressure equation built from it both vanish for $p_i = (-1)^i$.
- [SIMPLE in a 1D Converging Nozzle](../../../scripts/algorithms/simple_1d_nozzle/): solves steady, incompressible, frictionless flow through a converging nozzle with the SIMPLE and SIMPLEC pressure–velocity coupling algorithms on a staggered grid, and compares the converged mass flow and pressure with Bernoulli's equation.
- [Backward-Facing Step Flow (SIMPLE Algorithm)](../../../scripts/simulations/backward_facing_step_simple/): solves steady 2D laminar incompressible flow over a backward-facing step with the finite volume method and the SIMPLE pressure–velocity coupling algorithm.
- [Lid-Driven Cavity Flow Simulation](../../../scripts/simulations/lid_driven_cavity/): solves the 2D incompressible Navier-Stokes equations for flow in a square cavity driven by a moving lid at a Reynolds number of 100 and animates the velocity field.

## Exercises

**Exercise 1.** On a periodic 1D grid of $N = 8$ cells, list the eigenvalues (times $\Delta x^2$) of the wide Laplacian $(p_{i+2} - 2p_i + p_{i-2})/(4\Delta x^2)$ and of the compact Laplacian for the wavenumbers $\theta = 0, \pi/4, \pi/2, 3\pi/4, \pi$. Which modes does each operator fail to see?

<details>
<summary>Answer</summary>

The eigenvalues are $-\sin^2\theta$ (wide) and $-4\sin^2(\theta/2)$ (compact), in units of $1/\Delta x^2$:

| $\theta$ | 0 | $\pi/4$ | $\pi/2$ | $3\pi/4$ | $\pi$ |
| --- | --- | --- | --- | --- | --- |
| wide | 0 | $-0.5$ | $-1$ | $-0.5$ | 0 |
| compact | 0 | $-0.586$ | $-2$ | $-3.414$ | $-4$ |

Both annihilate the constant ($\theta = 0$), which only reflects the undetermined pressure level. The wide operator also annihilates the checkerboard ($\theta = \pi$) and treats $3\pi/4$ like $\pi/4$: it cannot tell a grid-scale oscillation from a smooth mode. For small $\theta$ both behave as $-\theta^2$.

</details>

**Exercise 2.** Evaluate the Rhie–Chow bracket $`(p_E - p_P)/\Delta x - \overline{(\partial p/\partial x)}_e`$ on a uniform grid for (a) $p = x^3$ and (b) the checkerboard $p_i = (-1)^i$ at a face with $p_P = 1$. Compare the sizes.

<details>
<summary>Answer</summary>

The bracket equals $-(p_{EE} - 3p_E + 3p_P - p_W)/(4\Delta x)$.

(a) For a cubic the third difference is exact: $p_{EE} - 3p_E + 3p_P - p_W = 6\Delta x^3$, so the bracket is $`-1.5\,\Delta x^2`$. It vanishes under refinement, so the face flux of a smooth field is changed only at second order.

(b) With $p_W = -1$, $p_P = 1$, $p_E = -1$, $p_{EE} = 1$ the third difference is $1 + 3 + 3 + 1 = 8$, and the bracket is $-2/\Delta x$, the full compact gradient: the averaged cell gradients vanish and only the compact part remains. The correction is negligible for smooth pressure and of full strength for the checkerboard.

</details>

**Exercise 3.** Show that SIMPLEC with $\alpha_p = 1$ and SIMPLE with $\alpha_p = 1 - \alpha_u$ produce the same velocity and pressure updates when $\sum a_{nb} = a_e$. With $\alpha_u = 0.7$, what pressure relaxation should SIMPLE use, and by what factor are the SIMPLEC $d$ coefficients larger?

<details>
<summary>Answer</summary>

With the relaxed diagonal $a_e/\alpha_u$, SIMPLE has $d^S = \alpha_u A_e/a_e$ and SIMPLEC $d^C = A_e/(a_e/\alpha_u - a_e) = d^S/(1 - \alpha_u)$. The pressure-correction coefficients are $\rho d A$, so the SIMPLEC matrix is the SIMPLE matrix times $1/(1 - \alpha_u)$, while the source (the mass imbalance of $u^*$) is the same. Hence $p'^C = (1 - \alpha_u) p'^S$. The velocity corrections $`d\,\Delta p'`$ are identical, and the pressure updates agree if $`1 \cdot p'^C = \alpha_p^S\, p'^S`$, i.e. $\alpha_p^S = 1 - \alpha_u$.

For $\alpha_u = 0.7$: $\alpha_p = 0.3$, and $`d^C = d^S/0.3 \approx 3.33\,d^S`$.

</details>

**Exercise 4.** For the converging nozzle of Versteeg and Malalasekera (length 2 m, area falling linearly from 0.5 to 0.1 m², $\rho = 1$ kg/m³, $p_0 = 10$ Pa, exit pressure 0), compute the exact mass flow and the exact static pressure at $x = 1$ m. SIMPLE on 5 pressure nodes converges to $\dot m = 0.6125$ kg/s and $p = 8.38$ Pa at $x = 1$ m. Explain the size of the error, and how you would show that it is a discretization error and not an iteration error.

<details>
<summary>Answer</summary>

Bernoulli between the stagnation state and the exit gives $u_e = \sqrt{2 \times 10/1} = 4.472$ m/s and $\dot m = \rho A_e u_e = 0.1 \times 4.472 = 0.44721$ kg/s. At $x = 1$ m the area is 0.3 m², so $u = 0.44721/0.3 = 1.4907$ m/s and $p = 10 - 0.5 \times 1.4907^2 = 8.889$ Pa.

The coarse result is 37 % too high. Upwinding takes the momentum leaving the last control volume from the last velocity node, half a cell upstream of the exit, where the area is 0.15 m² instead of 0.1 m², and the five-node grid is far too coarse to resolve the steep rise of $u$ near the exit. To separate the error sources, converge the residual several orders further and check that $\dot m$ does not change (iteration error), then refine the grid: the error halves with each halving of $\Delta x$ (37 %, 17.7 %, 8.6 %, ...), the signature of a first-order discretization error.

</details>

**Exercise 5.** The lid-driven cavity script uses an explicit projection method with $\Delta t = 10^{-3}$ s on a grid of spacing $h = 1/128$ m, lid speed $U = 1$ m/s and $\nu = 0.01$ m²/s. Compute the convective Courant number $U\Delta t/h$ and the diffusion number $\nu\Delta t/h^2$, and compare the latter with the 2D stability limit $1/4$ of forward Euler with central diffusion. How many time steps reach $t = 15$ s, and how many Jacobi sweeps does that imply?

<details>
<summary>Answer</summary>

$U\Delta t/h = 10^{-3} \times 128 = 0.128$ and $\nu\Delta t/h^2 = 0.01 \times 10^{-3} \times 128^2 = 0.164$, below $0.25$. The time step is set by diffusion more than by convection: halving $h$ would quadruple the diffusion number and violate the limit unless $\Delta t$ fell by four.

Reaching $t = 15$ s takes $`15/10^{-3} = 15\,000`$ steps, and with 50 Jacobi sweeps per step $7.5 \times 10^5$ sweeps of the pressure equation. This is why production codes use implicit diffusion and multigrid or conjugate-gradient pressure solvers.

</details>

## References

- Harlow, F. H., and Welch, J. E. "Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface." *Physics of Fluids*, 8(12), 2182–2189, 1965.
- Chorin, A. J. "Numerical solution of the Navier–Stokes equations." *Mathematics of Computation*, 22(104), 745–762, 1968.
- Patankar, S. V., and Spalding, D. B. "A calculation procedure for heat, mass and momentum transfer in three-dimensional parabolic flows." *International Journal of Heat and Mass Transfer*, 15(10), 1787–1806, 1972.
- Patankar, S. V. *Numerical Heat Transfer and Fluid Flow*. Hemisphere, 1980.
- Rhie, C. M., and Chow, W. L. "Numerical study of the turbulent flow past an airfoil with trailing edge separation." *AIAA Journal*, 21(11), 1525–1532, 1983.
- Van Doormaal, J. P., and Raithby, G. D. "Enhancements of the SIMPLE method for predicting incompressible fluid flows." *Numerical Heat Transfer*, 7(2), 147–163, 1984.
- Issa, R. I. "Solution of the implicitly discretised fluid flow equations by operator-splitting." *Journal of Computational Physics*, 62(1), 40–65, 1986.
- Versteeg, H. K., and Malalasekera, W. *An Introduction to Computational Fluid Dynamics: The Finite Volume Method*, 2nd ed. Pearson, 2007. (Chapter 6.)
- Ferziger, J. H., Perić, M., and Street, R. L. *Computational Methods for Fluid Dynamics*, 4th ed. Springer, 2020. (Chapter 8.)
- Moukalled, F., Mangani, L., and Darwish, M. *The Finite Volume Method in Computational Fluid Dynamics*. Springer, 2016.
