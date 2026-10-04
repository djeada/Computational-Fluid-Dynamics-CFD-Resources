# RANS Equations

The Reynolds-averaged Navier–Stokes (RANS) equations govern the *mean* flow of a turbulent fluid. They are what almost every industrial CFD simulation of turbulent flow actually solves. They look like the Navier–Stokes equations with one extra term, the Reynolds stress. That term turns a closed set of equations into an open one. This page derives the RANS equations, shows why they cannot be closed exactly, derives the transport equations for the Reynolds stresses and the turbulent kinetic energy, and introduces the two ideas that underpin most practical models: the Boussinesq eddy-viscosity hypothesis and the law of the wall.

The decomposition $u_i = U_i + u_i'$ and the averaging rules used below are set out in [Reynolds Decomposition](./reynolds_decomposition.md).

## Starting Point

For an incompressible Newtonian fluid with constant $\rho$ and $\nu$, and body forces absorbed into the pressure, the [continuity](../governing_equations/continuity.md) and [Navier–Stokes](../governing_equations/navier_stokes.md) equations in index notation are

$$
\frac{\partial u_i}{\partial x_i} = 0
$$

$$
\frac{\partial u_i}{\partial t} +
\frac{\partial (u_i u_j)}{\partial x_j} = -\frac{1}{\rho}
\frac{\partial p}{\partial x_i} + \nu \frac{\partial^2 u_i}{\partial x_j \partial x_j}
$$

The convective term has been written in conservative form using continuity. This makes the averaging of the nonlinear term transparent.

## Deriving the RANS Equations

Substitute $u_i = U_i + u_i'$ and $p = P + p'$, then average each term.

| Term | Instantaneous | Averaged |
| --- | --- | --- |
| Unsteady | $\partial u_i/\partial t$ | $\partial U_i/\partial t$ |
| Convective | $\partial (u_i u_j)/\partial x_j$ | $`\partial (U_i U_j)/\partial x_j + \partial\,\overline{u_i'u_j'}/\partial x_j`$ |
| Pressure | $`-(1/\rho)\,\partial p/\partial x_i`$ | $`-(1/\rho)\,\partial P/\partial x_i`$ |
| Viscous | $`\nu\,\partial^2 u_i/\partial x_j\partial x_j`$ | $`\nu\,\partial^2 U_i/\partial x_j\partial x_j`$ |

Every linear term keeps its form. Only the convective term produces something new, because $\overline{u_i u_j} = U_iU_j + \overline{u_i'u_j'}$. Averaging continuity gives $\partial U_i/\partial x_i = 0$, which lets us write $`\partial (U_iU_j)/\partial x_j = U_j\,\partial U_i/\partial x_j`$. The result is the **RANS momentum equation**:

$$
\frac{\partial U_i}{\partial t} + U_j
\frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho} \frac{\partial P}{\partial x_i} +
\frac{\partial}{\partial x_j}\left[\nu\left(\frac{\partial U_i}{\partial x_j} +
\frac{\partial U_j}{\partial x_i}\right) - \overline{u_i'u_j'}\right]
$$

The term $`\nu\,\partial U_j/\partial x_i`$ contributes nothing (its divergence vanishes by continuity). It is included so that the bracket is a proper symmetric stress. Multiplying by $\rho$:

```math
\rho
\frac{\overline{D} U_i}{\overline{D} t} = \frac{\partial}{\partial x_j}\left[-P\,\delta_{ij} + 2\mu\,\overline{S}_{ij} - \rho\,\overline{u_i'u_j'}\right],
\qquad
\overline{S}_{ij} = \frac{1}{2}\left(\frac{\partial U_i}{\partial x_j} +
\frac{\partial U_j}{\partial x_i}\right)
```

Here $`\overline{D}/\overline{D}t = \partial/\partial t + U_k\,\partial/\partial x_k`$ is the rate of change following the *mean* flow, not a fluid particle. The mean momentum is acted on by the mean pressure, the mean viscous stress and the **Reynolds stress** $`-\rho\,\overline{u_i'u_j'}`$. For compressible flow the same steps are carried out with Favre averaging (see [Reynolds Decomposition](./reynolds_decomposition.md)).

## The Closure Problem

Count equations and unknowns:

- **Equations:** 4 (three mean momentum components plus mean continuity).
- **Unknowns:** 10 (three $U_i$, one $P$, and six independent Reynolds stresses).

The system is not closed. The natural response is to derive transport equations for $\overline{u_i'u_j'}$ themselves. Those equations contain new unknowns: triple correlations $\overline{u_i'u_j'u_k'}$, pressure–velocity correlations, and velocity-gradient correlations. Equations for the triple correlations bring in fourth-order moments, and so on without end.

This **closure problem** is a direct consequence of the quadratic nonlinearity of the Navier–Stokes equations. Every moment equation couples to the next higher moment. At some level the hierarchy must be truncated with a **model**: a physically motivated approximation relating the unknown correlations to known quantities. The models themselves are the subject of [Turbulence Modeling](./modeling.md).

## Equation for the Fluctuations

Subtracting the RANS equation from the instantaneous Navier–Stokes equation gives an exact equation for the velocity fluctuation. The steps use $`\partial (U_i u_k')/\partial x_k = u_k'\,\partial U_i/\partial x_k`$ and $`\partial (u_i'U_k)/\partial x_k = U_k\,\partial u_i'/\partial x_k`$, both of which follow from continuity. The result is

$$
\frac{\partial u_i'}{\partial t} + U_k \frac{\partial u_i'}{\partial x_k} = -u_k'
\frac{\partial U_i}{\partial x_k} -
\frac{\partial}{\partial x_k}\left(u_i'u_k' - \overline{u_i'u_k'}\right) -
\frac{1}{\rho} \frac{\partial p'}{\partial x_i} + \nu
\frac{\partial^2 u_i'}{\partial x_k\partial x_k}
$$

The first term on the right, $`-u_k'\,\partial U_i/\partial x_k`$, is the interaction of fluctuations with mean gradients. It is how the mean flow feeds the turbulence.

## Reynolds Stress Transport Equation

Multiply the fluctuation equation for $u_i'$ by $u_j'$, add the same with $i$ and $j$ exchanged, and average. After rearranging:

$$
\frac{\partial \overline{u_i'u_j'}}{\partial t} + U_k
\frac{\partial \overline{u_i'u_j'}}{\partial x_k} = P_{ij} + R_{ij} - \varepsilon_{ij} -
\frac{\partial T_{kij}}{\partial x_k}
$$

The terms on the right are:

$$
P_{ij} = -\overline{u_i'u_k'} \frac{\partial U_j}{\partial x_k} - \overline{u_j'u_k'}
\frac{\partial U_i}{\partial x_k}
$$

```math
R_{ij} = \overline{\frac{p'}{\rho}\left(\frac{\partial u_i'}{\partial x_j} + \frac{\partial u_j'}{\partial x_i}\right)},
\qquad
\varepsilon_{ij} = 2\nu\,\overline{\frac{\partial u_i'}{\partial x_k}\frac{\partial u_j'}{\partial x_k}}
```

```math
T_{kij} = \overline{u_i'u_j'u_k'} +
\frac{1}{\rho}\left(\overline{p'u_i'}\,\delta_{jk} +
\overline{p'u_j'}\,\delta_{ik}\right) - \nu
\frac{\partial \overline{u_i'u_j'}}{\partial x_k}
```

| Term | Name | Physical role | Closed? |
| --- | --- | --- | --- |
| $P_{ij}$ | Production | Energy extracted from the mean flow by the mean velocity gradients | Yes, if the stresses are known |
| $R_{ij}$ | Pressure–strain | Redistributes energy among components; trace-free | No |
| $\varepsilon_{ij}$ | Dissipation tensor | Viscous destruction at small scales | No |
| $\overline{u_i'u_j'u_k'}$ | Turbulent transport | Spatial transport by the fluctuations themselves | No |
| $\overline{p'u_i'}/\rho$ | Pressure transport | Spatial transport by pressure fluctuations | No (often neglected or lumped with turbulent transport) |
| $`\nu\,\partial \overline{u_i'u_j'}/\partial x_k`$ | Viscous diffusion | Molecular transport; important only near walls | Yes |

The pressure–strain term deserves special attention. Its trace is $`R_{ii} = 2\,\overline{(p'/\rho)\,\partial u_i'/\partial x_i} = 0`$ by continuity. It therefore changes no energy in total; it only moves energy between components.

In a simple shear flow $U(y)$ the production tensor has only two nonzero components: $`P_{11} = -2\,\overline{u'v'}\,dU/dy`$ and $`P_{12} = -\overline{v'^2}\,dU/dy`$. The mean shear feeds only $\overline{u'^2}$. That $\overline{v'^2}$ and $\overline{w'^2}$ are nonzero is entirely due to pressure–strain redistribution, which tends to restore isotropy.

**Reynolds stress models** (RSM) close the terms marked "No" in the table and solve all six equations (see [Turbulence Modeling](./modeling.md)).

## Turbulent Kinetic Energy Equation

Taking half the trace of the Reynolds stress equation gives the transport equation for $k = \frac{1}{2}\overline{u_i'u_i'}$:

$$
\frac{\partial k}{\partial t} + U_j \frac{\partial k}{\partial x_j} = \mathcal{P} -
\varepsilon -
\frac{\partial}{\partial x_j}\left(\frac{1}{2}\overline{u_i'u_i'u_j'} +
\frac{1}{\rho}\overline{p'u_j'} - \nu \frac{\partial k}{\partial x_j}\right)
$$

with

```math
\mathcal{P} = -\overline{u_i'u_j'} \frac{\partial U_i}{\partial x_j},
\qquad
\varepsilon = \nu\,\overline{\frac{\partial u_i'}{\partial x_j}\frac{\partial u_i'}{\partial x_j}}
```

The terms have clear physical meanings.

- **Production** $\mathcal{P}$ is the rate at which the mean flow does work against the Reynolds stresses. The same term appears with the opposite sign in the equation for the mean kinetic energy $\frac{1}{2}U_iU_i$, so it is a *transfer*, not a creation. It is usually positive: energy flows from the mean flow into turbulence.
- **Dissipation** $\varepsilon$ is the rate at which viscosity converts turbulent kinetic energy into internal energy at the smallest scales (see [Energy Cascade](./energy_cascade.md)). Strictly, the expression above is the "pseudo-dissipation". It differs from the true dissipation $`2\nu\,\overline{s_{ij}'s_{ij}'}`$ by a term that is usually small.
- **Transport**, the divergence on the right, contains turbulent transport, pressure transport and viscous diffusion. It moves $k$ from place to place. Integrated over a closed volume with no flux through the boundary, it contributes nothing.

Two limiting cases are instructive:

- In **decaying homogeneous turbulence** there is no mean gradient and no transport, so $dk/dt = -\varepsilon$.
- In the **logarithmic region** of a wall-bounded flow, transport is small and production balances dissipation locally: $\mathcal{P} \approx \varepsilon$. This local equilibrium is used to calibrate many model constants.

## The Boussinesq Eddy-Viscosity Hypothesis

Boussinesq (1877) proposed that turbulent momentum transfer behaves like molecular momentum transfer. The Reynolds stress is taken proportional to the mean strain rate, with a scalar **eddy viscosity** $\nu_t$:

```math
-\overline{u_i'u_j'} = \nu_t\left(\frac{\partial U_i}{\partial x_j} +
\frac{\partial U_j}{\partial x_i}\right) - \frac{2}{3}k\,\delta_{ij}
```

The isotropic term is needed for consistency. Taking the trace of the left side gives $-2k$. On the right, the strain term has trace $`2\nu_t\,\partial U_i/\partial x_i = 0`$, so the $`-\frac{2}{3}k\,\delta_{ij}`$ term is what supplies $-2k$.

Substituting into RANS gives equations of Navier–Stokes form with an effective viscosity $\nu + \nu_t$ and a modified pressure $P + \frac{2}{3}\rho k$:

$$
\frac{\partial U_i}{\partial t} + U_j
\frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho}
\frac{\partial}{\partial x_i}\left(P + \frac{2}{3}\rho k\right) +
\frac{\partial}{\partial x_j}\left[(\nu +
\nu_t)\left(\frac{\partial U_i}{\partial x_j} +
\frac{\partial U_j}{\partial x_i}\right)\right]
$$

The production of $k$ becomes

```math
\mathcal{P} = 2\nu_t\,\overline{S}_{ij}\overline{S}_{ij} = \nu_t S^2 \ge 0,
\qquad S = \sqrt{2\,\overline{S}_{ij}\overline{S}_{ij}}
```

Unlike molecular viscosity, $\nu_t$ is a property of the *flow*, not the fluid. It varies in space and time, and it must be supplied by a turbulence model. All eddy-viscosity models (mixing length, Spalart–Allmaras, $k$–$`\varepsilon`$, $k$–$`\omega`$, SST) differ only in how they compute $\nu_t$.

### Limitations

The hypothesis is convenient but physically restrictive.

- **Alignment.** It assumes the anisotropy tensor is aligned with the mean strain rate, and that the stresses respond instantly to local strain. Real turbulence has memory, on a time scale of about $k/\varepsilon$.
- **Normal stresses.** In simple shear it predicts equal normal stresses, $\overline{u'^2} = \overline{v'^2} = \overline{w'^2} = \frac{2}{3}k$. Measurements show $\overline{u'^2}$ is clearly the largest. As a result, linear eddy-viscosity models cannot predict the secondary flows in straight non-circular ducts, which are driven by normal-stress differences.
- **Curvature and rotation.** It is blind to streamline curvature, system rotation and swirl, which strongly modify real turbulence.
- **Strong normal strain.** Because $\mathcal{P} = \nu_t S^2$ grows without bound, it overpredicts $k$ at stagnation points and in other regions of strong normal strain.
- **Counter-gradient transport.** Some flows, such as wall jets and asymmetric channels, have locations where the shear stress and the mean velocity gradient do not vanish together. A scalar eddy viscosity cannot represent this.

## Wall-Bounded Flows and the Law of the Wall

### Total Stress in a Channel

Consider fully developed flow in a channel of half-height $\delta$. The mean velocity is $U(y)$, and the statistics depend only on $y$. The RANS $x$-momentum equation reduces to

$$
0 = -\frac{1}{\rho} \frac{dP}{dx} +
\frac{d}{dy}\left(\nu \frac{dU}{dy} - \overline{u'v'}\right)
$$

The total shear stress $`\tau(y) = \rho\nu\,dU/dy - \rho\,\overline{u'v'}`$ therefore varies linearly. By symmetry it vanishes on the centreline, so

$$
\tau(y) = \tau_w\left(1 - \frac{y}{\delta}\right)
$$

At the wall the no-slip condition forces $u' = v' = 0$, so all the stress is viscous. A short distance away, almost all of it is carried by the Reynolds stress.

```
  y/delta
   1.0 |\
       | \      total shear stress  tau = tau_w (1 - y/delta)
       |  \
       |   \    <- carried almost entirely by  -rho <u'v'>
       |    \
       |     \
   0.0 |______\   viscous stress mu dU/dy dominates only in a thin layer
       0     tau_w
```

### Wall Units

Near the wall the only relevant parameters are $\tau_w$, $\rho$ and $\nu$. They define the **friction velocity** and the **viscous length scale**:

```math
u_\tau = \sqrt{\frac{\tau_w}{\rho}}, \qquad \delta_\nu = \frac{\nu}{u_\tau}, \qquad y^+ = \frac{y}{\delta_\nu} = \frac{y\,u_\tau}{\nu}, \qquad u^+ = \frac{U}{u_\tau}
```

The friction Reynolds number $Re_\tau = u_\tau\delta/\nu = \delta/\delta_\nu$ is the ratio of the outer and inner length scales. Prandtl's **law of the wall** states that, in the inner layer ($y/\delta$ below about 0.1), $u^+$ depends on $y^+$ alone: $u^+ = f_w(y^+)$.

### Viscous Sublayer

Very close to the wall, continuity and no-slip give $u' \propto y$ and $v' \propto y^2$, so $\overline{u'v'} \propto y^3$. The Reynolds stress is negligible, and $`\tau \approx \mu\,dU/dy \approx \tau_w`$. Hence

$$
u^+ = y^+ \qquad (y^+ \lesssim 5)
$$

### Log Law

Far enough from the wall that viscosity is unimportant ($y^+ \gg 1$), but close enough that the outer scale $\delta$ does not matter ($y/\delta \ll 1$), the only length available is $y$ itself. Dimensional reasoning then requires $dU/dy = u_\tau/(\kappa y)$. Prandtl's mixing length $\ell_m = \kappa y$ gives the same result: with $-\overline{u'v'} = \ell_m^2(dU/dy)^2 = u_\tau^2$, one gets $dU/dy = u_\tau/(\kappa y)$. Integrating:

$$
u^+ = \frac{1}{\kappa}\ln y^+ + B, \qquad \kappa \approx 0.41, \quad B \approx 5.0 \text{ to } 5.2
$$

The constants are:

- **von Kármán constant.** $\kappa = 0.41$ is the value built into most turbulence models. Some recent high-Reynolds-number studies argue for values closer to 0.38–0.39.
- **Additive constant.** $B$ is usually taken as 5.0–5.2 for smooth walls; Pope uses $\kappa = 0.41$ and $B = 5.2$. Roughness lowers $B$.

The log law holds approximately for $y^+ > 30$ and $y/\delta < 0.3$. Between the sublayer and the log layer lies the **buffer layer** ($5 < y^+ < 30$), where viscous and Reynolds stresses are comparable. TKE production peaks there, at about $y^+ \approx 12$. With $\kappa = 0.41$ and $B = 5.2$, the linear and log profiles intersect at $y^+ = 11.1$, a common switching point in wall functions.

In the log layer, production balances dissipation:

$$
\mathcal{P} = -\overline{u'v'} \frac{dU}{dy} \approx u_\tau^2\cdot
\frac{u_\tau}{\kappa y} = \frac{u_\tau^3}{\kappa y} \approx \varepsilon
$$

A single smooth formula covering all three inner regions is **Spalding's law**:

$$
y^+ = u^+ + e^{-\kappa B}\left[e^{\kappa u^+} - 1 - \kappa u^+ - \frac{(\kappa u^+)^2}{2} - \frac{(\kappa u^+)^3}{6}\right]
$$

| $y^+$ | Linear law $u^+ = y^+$ | Log law ($\kappa = 0.41$, $B = 5.2$) | Spalding |
| --- | --- | --- | --- |
| 1 | 1.00 | (not valid) | 1.00 |
| 5 | 5.00 | (not valid) | 4.88 |
| 10 | 10.0 | (not valid) | 8.36 |
| 30 | (not valid) | 13.50 | 12.79 |
| 100 | (not valid) | 16.43 | 16.26 |

```
  u+
  25 |                                                .....  log law
  20 |                                       ........
  15 |                             ........
  10 |                    ....''''
   5 |           ..'''
   0 |.....''''
     +--------+----------+---------------+---------------+----> y+ (log)
     1        5         30              300            3000
     | viscous| buffer   |      log layer (up to y/delta ~ 0.3)
     |sublayer|  layer   |
```

### What $y^+$ Means for a CFD Mesh

The first near-wall grid point must be placed consistently with the chosen wall treatment.

- **Wall-resolved (low-Reynolds-number) treatment**, used with Spalart–Allmaras, $k$–$`\omega`$, SST and low-Re $k$–$`\varepsilon`$: the first cell centroid should sit at $y^+ \approx 1$, with several cells inside the buffer layer.
- **Wall functions**: the first cell centroid should sit in the log layer, typically $30 < y^+ < 300$, and still well inside $y/\delta < 0.3$. The log law is then used to bridge the unresolved inner layer.
- **Buffer layer**: placing the first cell at $5 < y^+ < 30$ is the worst choice for standard wall functions.

Solver-specific wall treatments and meshing practice are covered in [Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md).

## Worked Example: First-Cell Height on a Flat Plate

Air ($\rho = 1.2\ \mathrm{kg/m^3}$, $\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$) flows at $U_\infty = 20$ m/s over a flat plate. We want the near-wall mesh at $x = 1$ m, assuming the boundary layer is turbulent from the leading edge.

I. **Reynolds number.** $Re_x = U_\infty x/\nu = 1.33 \times 10^6$.

II. **Skin friction.** From the turbulent flat-plate correlation, $`C_f = 0.0592\,Re_x^{-1/5} = 0.00353`$.

III. **Wall shear stress.** $\tau_w = \frac{1}{2}\rho U_\infty^2 C_f = 0.846$ Pa.

IV. **Friction velocity and viscous length.** $u_\tau = \sqrt{\tau_w/\rho} = 0.840$ m/s and $\delta_\nu = \nu/u_\tau = 17.9\ \mu\mathrm{m}$.

V. **Wall distances.**

| Target $y^+$ | Wall distance $y = y^+\delta_\nu$ | First cell height (cell-centred, $2y$) |
| --- | --- | --- |
| 1 | 0.018 mm | 0.036 mm |
| 30 | 0.54 mm | 1.07 mm |
| 100 | 1.79 mm | 3.57 mm |

VI. **Boundary-layer thickness.** The one-seventh power-law estimate is $`\delta \approx 0.37\,x\,Re_x^{-1/5} = 22`$ mm, so $\delta^+ \approx 1{,}230$. The log layer extends only to about $`y^+ \approx 0.3\,\delta^+ \approx 370`$. A wall-function mesh with $y^+ = 300$ would already sit at $y/\delta = 0.24$, near the limit.

The estimate of $C_f$ is only a starting point. After a first solution, check the actual $y^+$ distribution and refine where needed. At $y^+ = 100$ in this flow, the log-layer balance gives $\mathcal{P} \approx u_\tau^3/(\kappa y) \approx 810\ \mathrm{m^2/s^3}$, orders of magnitude above typical free-stream levels. This is why near-wall resolution matters.

## Related Scripts

- [boundary_layer_velocity_profile](../../../scripts/plots/boundary_layer_velocity_profile/): the one-seventh power-law profile of a turbulent boundary layer, an empirical alternative to the log law for the mean profile.
- [laminar_vs_turbulent_boundary_layer](../../../scripts/plots/laminar_vs_turbulent_boundary_layer/): compares laminar and turbulent profiles. The fuller turbulent profile and its steeper wall gradient are the visible effect of Reynolds-stress momentum transport.
- [laminar_vs_turbulent_pipe](../../../scripts/plots/laminar_vs_turbulent_pipe/): the same comparison for pipe flow.
- [Turbulent Flow: Reynolds Decomposition](../../../scripts/plots/turbulent_flow/): splits a synthetic velocity signal into its time mean and fluctuation, following the Reynolds decomposition used in turbulence modelling.

## Exercises

**Exercise 1.** Count the equations and unknowns in the three-dimensional incompressible RANS equations. Then show from continuity that the pressure–strain tensor $R_{ij}$ is trace-free, and explain what this means physically.

<details>
<summary>Answer</summary>

**Counting.** There are 4 equations (three momentum plus continuity) and 10 unknowns ($U_1$, $U_2$, $U_3$, $P$ and six Reynolds stresses), so 6 relations are missing.

**Trace of pressure–strain.** $`R_{ii} = \overline{(p'/\rho)(\partial u_i'/\partial x_i + \partial u_i'/\partial x_i)} = 2\,\overline{(p'/\rho)\,\partial u_i'/\partial x_i} = 0`$, because $\partial u_i'/\partial x_i = 0$.

**Meaning.** Pressure–strain does not appear in the $k$ equation. It cannot create or destroy turbulent kinetic energy, only shuffle it between the normal stresses, generally toward isotropy.

</details>

**Exercise 2.** For a simple shear flow $U = U(y)$, $V = W = 0$, evaluate all components of the production tensor $P_{ij}$ and the TKE production $\mathcal{P}$.

<details>
<summary>Answer</summary>

The only nonzero mean gradient is $\partial U_1/\partial x_2 = dU/dy$. From $`P_{ij} = -\overline{u_i'u_k'}\,\partial U_j/\partial x_k - \overline{u_j'u_k'}\,\partial U_i/\partial x_k`$:

- $`P_{11} = -2\,\overline{u'v'}\,dU/dy`$
- $`P_{12} = -\overline{v'^2}\,dU/dy`$
- $P_{22} = P_{33} = P_{13} = P_{23} = 0$

The TKE production is $`\mathcal{P} = \frac{1}{2}P_{ii} = -\overline{u'v'}\,dU/dy`$. This is positive, since $\overline{u'v'} < 0$ when $dU/dy > 0$.

Energy enters only the streamwise component. Pressure–strain redistributes it to $\overline{v'^2}$ and $\overline{w'^2}$.

</details>

**Exercise 3.** A Pitot probe measures $U = 15$ m/s at $y = 5$ mm above a smooth wall in air ($\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$, $\rho = 1.2\ \mathrm{kg/m^3}$). Assuming the point lies in the log layer, with $\kappa = 0.41$ and $B = 5.2$, find $u_\tau$, $y^+$ and $\tau_w$. Is the assumption consistent?

<details>
<summary>Answer</summary>

**Equation to solve.** $`U/u_\tau = \frac{1}{0.41}\ln(y\,u_\tau/\nu) + 5.2`$, with $U = 15$ m/s and $y = 0.005$ m.

**Solution.** Iterating, or using a root finder, gives $u_\tau = 0.797$ m/s.

**Wall quantities.** $y^+ = 0.005 \times 0.797/(1.5 \times 10^{-5}) = 266$ and $\tau_w = \rho u_\tau^2 = 0.763$ Pa.

**Consistency.** $y^+ = 266$ is above 30, so the log-law assumption is consistent, provided $y/\delta < 0.3$. This is the basis of the Clauser chart method for estimating wall shear stress from a mean profile.

</details>

**Exercise 4.** Water flows in a smooth pipe with $D = 0.1$ m, $U_b = 2$ m/s, $\nu = 10^{-6}\ \mathrm{m^2/s}$ and Darcy friction factor $f = 0.0156$. Using $\tau_w = \rho f U_b^2/8$, find $u_\tau$, the wall distance corresponding to $y^+ = 1$, the first cell height for a cell-centred mesh, and the wall distance for $y^+ = 30$.

<details>
<summary>Answer</summary>

**Wall shear and friction velocity.** $\tau_w = 1000 \times 0.0156 \times 4/8 = 7.8$ Pa, and $u_\tau = \sqrt{7.8/1000} = 0.088$ m/s.

**$y^+ = 1$.** $y = \nu/u_\tau = 11.3\ \mu\mathrm{m}$, so the first cell height is about $23\ \mu\mathrm{m}$.

**$y^+ = 30$.** $y = 0.34$ mm.

**Context.** $Re_\tau = u_\tau (D/2)/\nu \approx 4{,}400$. The pipe radius spans more than four thousand viscous lengths, which is why wall-resolved meshes need strong grid stretching.

</details>

**Exercise 5.** In the log layer, the Reynolds shear stress is approximately constant, $-\overline{u'v'} \approx u_\tau^2$. Using the Boussinesq hypothesis, derive the eddy viscosity and express $\nu_t/\nu$ in wall units. Evaluate it at $y^+ = 100$ and $y^+ = 1{,}000$.

<details>
<summary>Answer</summary>

**Derivation.** Boussinesq gives $`-\overline{u'v'} = \nu_t\,dU/dy`$. With $dU/dy = u_\tau/(\kappa y)$, this becomes $`u_\tau^2 = \nu_t\,u_\tau/(\kappa y)`$, so

```math
\nu_t = \kappa\, u_\tau\, y
\qquad \Longrightarrow
\qquad \frac{\nu_t}{\nu} = \kappa\, y^+
```

**Values.** $\nu_t/\nu = 41$ at $y^+ = 100$ and $410$ at $y^+ = 1{,}000$.

The eddy viscosity grows linearly with wall distance and quickly exceeds the molecular viscosity by orders of magnitude. Turbulence models are commonly checked to reproduce this behaviour.

</details>

## References

- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000. (Chapter 4: mean-flow equations; Chapter 5 and Section 7.3: TKE and Reynolds-stress budgets; Chapter 7: wall flows.)
- Wilcox, D. C. *Turbulence Modeling for CFD*, 3rd ed. DCW Industries, 2006.
- Tennekes, H., and Lumley, J. L. *A First Course in Turbulence*. MIT Press, 1972.
- Schlichting, H., and Gersten, K. *Boundary-Layer Theory*, 9th ed. Springer, 2017.
- Spalding, D. B. "A single formula for the law of the wall." *Journal of Applied Mechanics*, 28(3), 455–458, 1961.
