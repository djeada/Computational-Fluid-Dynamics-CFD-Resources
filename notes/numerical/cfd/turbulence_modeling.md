# Turbulence Modeling in CFD

Most engineering flows are turbulent, and no practical grid resolves all of their eddies. A CFD calculation therefore decides which scales it computes and models the effect of the rest on them, and that choice sets the mesh, the time step, the boundary data, the run time and the accuracy that can be expected. This note covers the averaging that defines the modeled equations, the RANS closure problem, the main eddy-viscosity models with their standard constants, how the model equations are solved, near-wall treatment, large-eddy simulation, hybrid methods and DNS, and what each approach costs. The derivations and the full form of each model are in the fluid-mechanics notes on [Reynolds Decomposition](../../fluid_mechanics/turbulence/reynolds_decomposition.md), [RANS Equations](../../fluid_mechanics/turbulence/rans_equations.md) and [Turbulence Modeling](../../fluid_mechanics/turbulence/modeling.md); OpenFOAM settings are in [Turbulence Modeling in OpenFOAM](../../../practice/openfoam/turbulence_modeling.md).

## Problem Statement

The incompressible Navier–Stokes equations describe turbulent flow exactly. The difficulty is the range of scales: the ratio of the largest eddies, of size $L$, to the Kolmogorov scale $\eta = (\nu^3/\varepsilon)^{1/4}$ grows as $Re^{3/4}$, so resolving everything in 3D needs of order $Re^{9/4}$ grid points and $Re^{3/4}$ time steps, a cost of roughly $Re^3$ (see [Energy Cascade](../../fluid_mechanics/turbulence/energy_cascade.md)). At the Reynolds numbers of a car or an aircraft ($10^6$ to $10^8$) this is far out of reach.

The modeling problem is therefore: given the geometry, the Reynolds number, the inflow (including its turbulence intensity and length scale) and the wall conditions, compute the statistics that matter (mean velocity and pressure, wall shear stress and heat flux, forces, separation and reattachment points, and in some cases spectra or fluctuating loads) from equations for averaged or filtered fields, with a model for the unresolved stresses. The unknowns are the mean or filtered velocity and pressure plus the model variables ($\tilde\nu$, $k$, $\varepsilon$ or $\omega$, or a subgrid viscosity), each with its own boundary conditions. A turbulent calculation counts as solved when the discretization error is small compared with the modeling error (grid-independent quantities of interest, see [Verification and Validation](./verification_and_validation.md)), the wall resolution matches the wall treatment of the model, and, for scale-resolving methods, the statistics are averaged over long enough samples. What makes it hard is that every closure is partly empirical and fails in identifiable flows, that the near-wall layer is thin but controls the friction, that the model equations are stiff and must stay positive, and that scale-resolving simulations need fine grids, small time steps and long averaging.

## Averaging

The Reynolds decomposition splits every variable into a mean and a fluctuation, $u = \overline{u} + u'$, with $\overline{u'} = 0$. For a statistically stationary flow the mean is the time average

```math
\overline{u}(\mathbf{x}) = \lim_{T \to \infty} \frac{1}{T}\int_{t_0}^{t_0 + T} u(\mathbf{x}, t)\, dt
```

For flows whose statistics change in time, such as a periodically forced flow or a transient, the mean is an ensemble average over repeated realizations, or a phase average for periodic forcing. Ergodicity lets time averages stand in for ensemble averages in stationary flows. Averaging is linear, commutes with derivatives, and leaves products of fluctuations, $\overline{u_i'u_j'} \ne 0$, which is where the closure problem comes from.

![Time history of a velocity signal, its fluctuation and the squared fluctuation](../../../scripts/plots/turbulent_flow/turbulence_plots.png)

The figure shows a synthetic velocity signal at a point with its time mean (dashed), the fluctuation $u'$, which averages to zero, and $u'^2$, whose mean $\overline{u'^2}$ measures the intensity of the fluctuations. RANS computes only the dashed line; LES and DNS compute the signal itself.

In compressible flow, Reynolds averaging of products with density produces many extra correlations such as $\overline{\rho' u_i'}$. Favre (density-weighted) averaging, $\tilde u = \overline{\rho u}/\overline{\rho}$ with $u = \tilde u + u''$, absorbs them, so the averaged compressible equations keep the form of the instantaneous ones with $\overline{\rho}$ and $\tilde u$ as variables. Compressible RANS and LES codes use Favre averages for velocity and temperature and Reynolds averages for density and pressure.

## The RANS Equations and the Closure Problem

Averaging the incompressible equations gives, for the mean velocity $U_i = \overline{u_i}$ and mean pressure $P$,

```math
\frac{\partial U_i}{\partial x_i} = 0,
\qquad
\frac{\partial U_i}{\partial t} + U_j\frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho}\frac{\partial P}{\partial x_i} + \frac{\partial}{\partial x_j}\left(\nu\frac{\partial U_i}{\partial x_j} - \overline{u_i'u_j'}\right)
```

The Reynolds stresses $\overline{u_i'u_j'}$ add six unknowns and no equations. Their exact transport equations contain further unknown correlations, so every level of averaging leaves more unknowns than equations: this is the closure problem. Most engineering models close it with the Boussinesq hypothesis,

```math
-\overline{u_i'u_j'} = 2\nu_t S_{ij} - \frac{2}{3}k\,\delta_{ij},
\qquad
S_{ij} = \frac{1}{2}\left(\frac{\partial U_i}{\partial x_j} + \frac{\partial U_j}{\partial x_i}\right),
\qquad
k = \frac{1}{2}\overline{u_i'u_i'}
```

which makes the stress proportional to the mean strain through a scalar eddy viscosity $\nu_t$. The isotropic part $\frac{2}{3}k$ is absorbed into a modified pressure. In the solver the momentum equations look laminar with $\nu$ replaced by $\nu + \nu_t$, so the discretization and pressure–velocity coupling of [Pressure–Velocity Coupling](../fvm/pressure_velocity_coupling.md) carry over unchanged. The hypothesis fails where the stresses are not aligned with the strain: strong curvature or swirl, secondary flows in non-circular ducts, and rapidly changing flows.

In fully developed channel flow of half-height $H$ the averaged equation reduces to

```math
\frac{d}{dy}\left(\nu\frac{dU}{dy} - \overline{u'v'}\right) = \frac{1}{\rho}\frac{dP}{dx}
```

so the total shear stress varies linearly from zero on the centreline to $`\tau_w = -H\,dP/dx`$ at the wall (Exercise 2). Near the wall it is carried by viscosity, further out by the Reynolds stress; an eddy-viscosity model must reproduce that transition to give the right friction.

Unsteady RANS (URANS) keeps the time derivative and resolves large-scale unsteadiness, such as vortex shedding, that is well separated in time scale from the turbulence; it still models all turbulent fluctuations.

## Eddy-Viscosity Models

On dimensional grounds $\nu_t$ is a velocity scale times a length scale. The models differ in how many transport equations they solve to obtain these scales.

### Mixing Length

Prandtl's mixing-length model prescribes both scales algebraically, $`\nu_t = \ell_m^2\,|dU/dy|`$ in a thin shear layer (or $\ell_m^2 S$ with $S = \sqrt{2S_{ij}S_{ij}}$ in general). Near a wall $\ell_m = \kappa y$ with $\kappa = 0.41$, which reproduces the log law, and van Driest damping $\ell_m = \kappa y[1 - \exp(-y^+/26)]$ extends it through the viscous sublayer. It needs no extra equations and is still used in boundary-layer codes and as a building block of learned closures, but it needs a length-scale prescription that is hard to define in complex geometries, and it has no memory of upstream conditions.

### Spalart–Allmaras

The Spalart–Allmaras model (1992) solves one transport equation for a working variable $\tilde\nu$ that equals $\nu_t$ away from walls:

```math
\frac{D\tilde\nu}{Dt} = c_{b1}\tilde S\tilde\nu - c_{w1}f_w\left(\frac{\tilde\nu}{d}\right)^2 + \frac{1}{\sigma}\left[\nabla\cdot\left((\nu + \tilde\nu)\nabla\tilde\nu\right) + c_{b2}\,|\nabla\tilde\nu|^2\right],
\qquad \nu_t = \tilde\nu f_{v1}
```

with production, destruction by the wall through the wall distance $d$, and diffusion. The constants are $c_{b1} = 0.1355$, $c_{b2} = 0.622$, $\sigma = 2/3$, $\kappa = 0.41$, $c_{w1} = c_{b1}/\kappa^2 + (1 + c_{b2})/\sigma$, $c_{w2} = 0.3$, $c_{w3} = 2$ and $c_{v1} = 7.1$; the functions $f_{v1}$, $f_w$ and $\tilde S$ are given in [Turbulence Modeling](../../fluid_mechanics/turbulence/modeling.md). The wall condition is $\tilde\nu = 0$ and the free-stream value is typically $\tilde\nu/\nu = 3$ to 5. SA was calibrated for aerodynamic boundary layers, wakes and mixing layers. It is robust, cheap and resolved to the wall ($y^+ \approx 1$), and it is a standard choice for external aerodynamics with attached or mildly separated flow; it needs the wall distance field and provides no $k$.

### Standard $k$–$`\varepsilon`$

The model of Launder and Spalding (1974) transports the turbulent kinetic energy $k$ and its dissipation rate $\varepsilon$, and sets $\nu_t = C_\mu k^2/\varepsilon$:

```math
\frac{Dk}{Dt} = \nabla\cdot\left[\left(\nu + \frac{\nu_t}{\sigma_k}\right)\nabla k\right] + \mathcal{P}_k - \varepsilon,
\qquad
\frac{D\varepsilon}{Dt} = \nabla\cdot\left[\left(\nu + \frac{\nu_t}{\sigma_\varepsilon}\right)\nabla\varepsilon\right] + C_{\varepsilon 1}\frac{\varepsilon}{k}\mathcal{P}_k - C_{\varepsilon 2}\frac{\varepsilon^2}{k}
```

with production $`\mathcal{P}_k = \nu_t S^2`$ and constants $`C_\mu = 0.09`$, $C_{\varepsilon 1} = 1.44$, $C_{\varepsilon 2} = 1.92$, $\sigma_k = 1.0$ and $\sigma_\varepsilon = 1.3$. The $\varepsilon$ equation is singular at walls, so the model is used with wall functions or with low-Reynolds-number damping functions. It works well in free shear flows and attached flows with mild pressure gradients; it overpredicts turbulence at stagnation points and predicts separation in adverse pressure gradients too late. The realizable and RNG variants modify $C_\mu$ and the $\varepsilon$ equation to reduce these errors and are common defaults in industrial codes.

### $k$–$`\omega`$

Wilcox's models replace $\varepsilon$ by the specific dissipation rate $\omega$, with $\varepsilon = \beta^* k\omega$. In the 2006 version (Wilcox 2006):

```math
\frac{Dk}{Dt} = \mathcal{P}_k - \beta^* k\omega + \nabla\cdot\left[\left(\nu + \sigma^*\frac{k}{\omega}\right)\nabla k\right],
\qquad
\frac{D\omega}{Dt} = \alpha\frac{\omega}{k}\mathcal{P}_k - \beta\omega^2 + \frac{\sigma_d}{\omega}\nabla k\cdot\nabla\omega + \nabla\cdot\left[\left(\nu + \sigma\frac{k}{\omega}\right)\nabla\omega\right]
```

with $\alpha = 13/25$, $\beta = \beta_0 f_\beta$, $\beta_0 = 0.0708$, $\beta^* = 0.09$, $\sigma = 1/2$, $\sigma^* = 3/5$, and $\sigma_d = 1/8$ where $\nabla k \cdot \nabla\omega > 0$ and zero otherwise. The eddy viscosity $\nu_t = k/\tilde\omega$ uses a limited $\tilde\omega = \max\left(\omega,\ C_{\mathrm{lim}}\sqrt{2S_{ij}S_{ij}/\beta^*}\right)$ with $C_{\mathrm{lim}} = 7/8$, and $f_\beta$ corrects the spreading rate of round jets. The $\omega$ equation can be integrated through the viscous sublayer without damping functions, since $\omega \to 6\nu/(\beta y^2)$ at a smooth wall, which gives better behaviour than $k$–$`\varepsilon`$ in adverse pressure gradients. The 1988 version was sensitive to the free-stream value of $\omega$; the cross-diffusion term $\sigma_d$ of the 2006 version reduces that sensitivity.

### Menter SST

Menter's shear-stress transport model (1994) blends $k$–$`\omega`$ near walls with a $k$–$`\varepsilon`$ model rewritten in terms of $\omega$ away from them, using a blending function $F_1$ of the wall distance, and limits the eddy viscosity:

```math
\nu_t = \frac{a_1 k}{\max\left(a_1\omega,\ S F_2\right)},
\qquad a_1 = 0.31
```

The limiter enforces Bradshaw's observation that the shear stress in a boundary layer is about $a_1 k$; without it, two-equation models overpredict the shear stress in adverse pressure gradients and delay separation. The coefficients are blended between the inner set ($\sigma_k = 0.85$, $\sigma_\omega = 0.5$, $\beta = 0.075$) and the outer set ($\sigma_k = 1.0$, $\sigma_\omega = 0.856$, $\beta = 0.0828$), with $\beta^* = 0.09$ and $\kappa = 0.41$; $F_1$, $F_2$ and the cross-diffusion term are given in [Turbulence Modeling](../../fluid_mechanics/turbulence/modeling.md). SST resolved to $y^+ \approx 1$ is one of the most widely used general-purpose RANS models, especially for separating boundary layers.

### Beyond Eddy Viscosity

Reynolds-stress models solve transport equations for all six stresses plus a scale equation. They capture curvature, rotation and duct secondary flows that linear eddy-viscosity models miss, at the price of seven equations and less robust convergence. Data-driven corrections of eddy-viscosity models are discussed in [Machine-Learned Turbulence Closures](../../machine_learning/flow/ml_turbulence_closures.md).

## Solving the Model Equations

The model equations are convection–diffusion equations with large source terms, solved after the momentum and pressure equations in each outer iteration of a segregated solver. They need some care:

1. Positivity. $k$, $\varepsilon$, $\omega$ and $\tilde\nu$ must stay positive. Destruction terms are linearized into the diagonal, for example $-\varepsilon$ in the $k$ equation as $`-(\varepsilon/k)^{\mathrm{old}}\,k`$, so that a source $S = S_u + S_P\phi$ always has $S_P \le 0$ and the matrix remains diagonally dominant. Production stays explicit in $S_u \ge 0$.

2. Bounded convection. Upwind or bounded TVD schemes are used for the turbulence variables even when the momentum equations use a higher-order scheme, since oscillations can drive them negative (see [Convection Schemes](../fvm/convection_schemes.md)).

3. Under-relaxation. Factors of 0.5 to 0.8 for $k$, $\varepsilon$, $\omega$ and $\nu_t$ are typical in steady runs; limiters on $\nu_t/\nu$ or on production (the 2003 form of SST limits $\mathcal{P}_k$ to $10\beta^* k\omega$) prevent run-away values at stagnation points.

4. Inlet values. Without measurements, $k$ and the dissipation variable are set from a turbulence intensity $I$ and a length scale $\ell$:

   ```math
   k = \frac{3}{2}(IU)^2,
   \qquad
   \varepsilon = C_\mu^{3/4}\frac{k^{3/2}}{\ell},
   \qquad
   \omega = \frac{k^{1/2}}{C_\mu^{1/4}\ell}
   ```

   The resulting $\nu_t/\nu$ (hundreds in internal flows, 1 to 10 in external aerodynamics) should be checked, and the sensitivity of the result to these guesses tested. The modeled free-stream turbulence decays between the inlet and the body, so the inlet values must be chosen to give the intended level where it matters.

## Near-Wall Treatment

In wall units, $y^+ = y u_\tau/\nu$ with friction velocity $u_\tau = \sqrt{\tau_w/\rho}$, a turbulent boundary layer has a viscous sublayer ($y^+ < 5$, $u^+ = y^+$), a buffer layer ($5 < y^+ < 30$) and a log layer ($y^+ > 30$, $y/\delta < 0.3$) where

```math
u^+ = \frac{1}{\kappa}\ln y^+ + B,
\qquad \kappa = 0.41, \quad B \approx 5.0\ \text{to}\ 5.2
```

(see [RANS Equations](../../fluid_mechanics/turbulence/rans_equations.md)). Since $u_\tau$ is not known before the run, the first cell height is estimated from a skin-friction correlation and checked afterwards. There are two strategies:

|  | Wall-resolved (low-Re) | Wall functions |
| --- | --- | --- |
| First cell centre | $y^+ \approx 1$ | $30 < y^+ < 200$–300, inside the log layer |
| Cells across the boundary layer | 15 to 30, growth ratio about 1.2 or less | a few |
| Models | SA, $k$–$`\omega`$, SST, low-Re $k$–$`\varepsilon`$ | standard, realizable $k$–$`\varepsilon`$; SST with wall functions |
| Wall shear stress | from the velocity gradient at the wall | from the log law at the first cell |
| Valid for | attached, separating and reattaching flows, heat transfer | equilibrium boundary layers |

A wall function (Launder and Spalding 1974) takes the velocity scale from the turbulent kinetic energy of the first cell, $u^* = C_\mu^{1/4}k_P^{1/2}$, which stays nonzero at separation where $u_\tau \to 0$, computes the wall shear stress from the log law at $`y_P^* = y_P u^*/\nu`$, and sets $\varepsilon_P = C_\mu^{3/4}k_P^{3/2}/(\kappa y_P)$ in the first cell instead of solving for it there. It saves most of the near-wall cells but assumes local equilibrium and a log layer, which fail near separation, reattachment, strong pressure gradients and low Reynolds numbers. A first cell in the buffer layer ($5 < y^+ < 30$) is wrong for both strategies; many codes now blend the two ("all-$`y^+`$" treatments), which reduces but does not remove this sensitivity. Meshing guidance for prism layers is in [Boundary-Layer Meshing](../../../practice/mesh_generation/boundary_layers.md).

## Large-Eddy Simulation

LES computes the large, energy-containing eddies, which depend on the geometry, and models the smaller, more universal ones. The equations are filtered with a kernel of width $\Delta$, usually the grid itself, $`\Delta = (\Delta x\,\Delta y\,\Delta z)^{1/3}`$, and the subgrid-scale stress $`\tau_{ij} = \overline{u_iu_j} - \overline{u}_i\,\overline{u}_j`$ replaces the Reynolds stress (here the overbar denotes filtering). The Smagorinsky model (1963) gives it an eddy viscosity built from the resolved strain rate:

```math
\tau_{ij} - \frac{1}{3}\tau_{kk}\delta_{ij} = -2\nu_{\mathrm{sgs}}\overline{S}_{ij},
\qquad
\nu_{\mathrm{sgs}} = (C_s\Delta)^2\,|\overline{S}|,
\qquad
|\overline{S}| = \sqrt{2\,\overline{S}_{ij}\overline{S}_{ij}}
```

Lilly's analysis for an inertial-range spectrum gives $C_s \approx 0.17$; shear flows such as channels need about 0.1. The model is too dissipative near walls and in laminar regions, where $|\overline{S}|$ is large without small-scale turbulence. The dynamic procedure of Germano et al. (1991) computes the coefficient from the resolved field. Filtering the resolved velocity again with a test filter $\widehat{\ \cdot\ }$ of width $\widehat\Delta = 2\Delta$ gives the Germano identity

```math
L_{ij} = \widehat{\overline{u}_i\,\overline{u}_j} - \widehat{\overline{u}}_i\,\widehat{\overline{u}}_j = T_{ij} - \widehat{\tau}_{ij}
```

in which $L_{ij}$ is computable. Inserting the Smagorinsky form for both $T_{ij}$ (at width $\widehat\Delta$) and $\tau_{ij}$ and minimizing the error in the least-squares sense (Lilly 1992) gives

```math
C_s^2 = \frac{\langle L_{ij}M_{ij}\rangle}{\langle M_{ij}M_{ij}\rangle},
\qquad
M_{ij} = 2\Delta^2\left(\widehat{|\overline{S}|\,\overline{S}_{ij}} - \frac{\widehat\Delta^2}{\Delta^2}\,|\widehat{\overline{S}}|\,\widehat{\overline{S}}_{ij}\right)
```

where $\langle\cdot\rangle$ averages over homogeneous directions or nearby cells and negative values are clipped. The coefficient then falls to zero at walls and in laminar regions by itself. The WALE model reaches the same near-wall behaviour algebraically.

The numerics matter as much as the model. Upwind-biased schemes add numerical dissipation that can exceed the subgrid dissipation, so LES uses low-dissipation central or kinetic-energy-preserving schemes, often with a little upwinding for robustness; implicit LES relies on the numerical dissipation alone. The time step is set by the resolved eddies, with a convective Courant number around 1 or less. A well-resolved LES should resolve about 80 % of the turbulent kinetic energy. Near walls the energetic streaks scale with viscous units, so wall-resolved LES needs spacings of the order of $\Delta x^+ \approx 50$–100, $\Delta z^+ \approx 15$–40 and a first cell at $y^+ \lesssim 1$, and its cost grows almost as fast as DNS with Reynolds number. Wall-modeled LES resolves only the outer layer and supplies the wall shear stress from a wall model, which makes LES affordable at high Reynolds number. Results are statistics: the initial transient (several flow-through times) is discarded, averages are collected over many more, and turbulent inflow has to be generated with synthetic fluctuations or a precursor simulation.

## Hybrid RANS–LES

Detached-eddy simulation (DES, Spalart and co-workers, 1997) runs one model as RANS in attached boundary layers and as a subgrid model in separated regions. In SA-based DES the wall distance in the destruction term is replaced by

```math
\tilde d = \min\left(d,\ C_{\mathrm{DES}}\Delta\right),
\qquad \Delta = \max(\Delta x, \Delta y, \Delta z),
\qquad C_{\mathrm{DES}} = 0.65
```

so the switch is set by the grid, not the flow. If the wall-parallel spacing is refined below the boundary-layer thickness, LES mode starts inside an attached boundary layer whose grid cannot support resolved eddies, the modeled stress is depleted, and the solution can separate for numerical reasons. Delayed DES (DDES, Spalart et al. 2006) adds a shielding function that keeps attached boundary layers in RANS mode, and improved DDES adds wall-modeled LES behaviour. Hybrid methods suit massively separated flows (bluff bodies, landing gear, the wake of a car) where the separation is fixed by the geometry, and need care in the "grey area" where the solution switches from modeled to resolved turbulence.

## Direct Numerical Simulation

DNS solves the Navier–Stokes equations with no model. The grid must resolve the dissipative scales, typically $k_{\max}\eta \ge 1.5$ for spectral methods, or spacings of a few $\eta$; in wall units a channel DNS uses about $\Delta x^+ \approx 10$, $\Delta z^+ \approx 5$ and $\Delta y^+ < 1$ at the wall, with high-order or spectral discretizations. The time step is limited by the smallest resolved scales. Moser, Kim and Mansour (1999) computed channel flow up to $Re_\tau = 590$ this way, and such databases are the reference data for calibrating and testing RANS and LES models. DNS is a research tool for moderate Reynolds numbers and simple geometries.

## Cost and Choice

Choi and Moin (2012) estimated how the number of grid points for a flat-plate boundary layer of length $L_x$ scales with $Re_{L_x}$: $Re_{L_x}^{37/14}$ for DNS, $Re_{L_x}^{13/7}$ for wall-resolved LES, and $Re_{L_x}$ for wall-modeled LES. RANS grids depend only weakly on $Re$ apart from the first-cell height.

| Approach | Resolved | Grid points (flat plate) | Time stepping | Typical outputs | Use when |
| --- | --- | --- | --- | --- | --- |
| RANS | mean flow only | weak $Re$ dependence | steady; $10^3$ to $10^4$ outer iterations | mean forces, pressure drop, mean heat transfer | design studies, attached flows, many configurations |
| URANS | mean flow and large-scale periodic unsteadiness | as RANS | time step resolving the period of the unsteadiness | shedding frequency, mean and periodic loads | unsteadiness well separated from turbulence |
| DDES and other hybrids | eddies in separated regions; RANS boundary layers | between RANS and wall-modeled LES | $C \lesssim 1$ in the LES region, long averaging | unsteady loads, wake spectra, separated mean flow | massive separation at high $Re$ |
| Wall-modeled LES | outer-layer eddies | $\propto Re_{L_x}$ | $C \lesssim 1$, many flow-through times | as LES, at high $Re$ | high-$`Re`$ flows where RANS fails |
| Wall-resolved LES | all energetic eddies | $\propto Re_{L_x}^{13/7}$ | $C \lesssim 1$, many flow-through times | turbulence statistics, acoustic sources | moderate $Re$, transition, aeroacoustics |
| DNS | all scales | $\propto Re_{L_x}^{37/14}$; $Re^{9/4}$ in homogeneous turbulence | number of steps $\propto Re^{3/4}$ | complete statistics and budgets | physics, model calibration, low $Re$ |

The choice follows from the quantity needed and the budget. Steady RANS with SA or SST, resolved to the wall, is the default for design studies; uncertain or separated cases should be run with more than one model, since the spread between reasonable models is a crude measure of the modeling error. Unsteady loads, noise and massively separated wakes need DDES or LES. A flow-by-flow table of reasonable starting models is in [Turbulence Modeling](../../fluid_mechanics/turbulence/modeling.md#choosing-a-model). In every case grid convergence comes first: comparing models on a grid that is not converged mixes discretization and modeling errors.

## Key Takeaways

- Averaging leaves the unclosed Reynolds stresses; eddy-viscosity models close them with $\nu_t$, so the solver sees a laminar-like momentum equation with $\nu + \nu_t$.
- SA (one equation) and SST (two equations), integrated to the wall, are the standard RANS choices for aerodynamics; $k$–$`\varepsilon`$ with wall functions remains common for internal and industrial flows.
- The first-cell $y^+$ must match the wall treatment: about 1 for wall-resolved models, 30 to 300 for wall functions, never in the buffer layer.
- Turbulence equations need implicit destruction terms, bounded convection schemes and sensible inlet values to stay positive and converge.
- LES needs low-dissipation numerics, fine near-wall grids unless the wall is modeled, and long averaging; the dynamic procedure removes the need to tune $C_s$.
- Cost rises from RANS to DES, LES and DNS by orders of magnitude, and DNS scales roughly as $Re^3$.

## Related Scripts

- [Turbulent Flow: Reynolds Decomposition](../../../scripts/plots/turbulent_flow/): splits a synthetic velocity signal into its time mean and fluctuation, following the Reynolds decomposition used in turbulence modelling.
- [Learned Mixing-Length Closure](../../../scripts/algorithms/learned_mixing_length_closure/): learns a near-wall correction to Prandtl's mixing length from reference velocity data, then inserts the learned closure into a 1D RANS solver to check whether a good fit to the closure data also gives a good velocity profile.
- [Laminar vs Turbulent Pipe Flow](../../../scripts/plots/laminar_vs_turbulent_pipe/): plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is.
- [Laminar vs. Turbulent Boundary Layer Profiles](../../../scripts/plots/laminar_vs_turbulent_boundary_layer/): plots normalised laminar and turbulent boundary-layer velocity profiles on the same axes to show how much fuller the turbulent profile is.
- [Time-Averaged Velocity Field](../../../scripts/plots/time_averaged_velocity_field/): generates a synthetic noisy longitudinal velocity field on a $200 \times 60$ grid and compares it with its mean field, the first step of a Reynolds decomposition.
- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.
- [Mean Velocity Magnitude: Experiment vs CFD Comparison](../../../scripts/plots/mean_velocity_magnitude/): plots a mock experimental profile and a mock CFD scale-resolving simulation (SRS) profile of the normalised mean velocity magnitude $|U|/U_0$ along an under-body centreline.

## Exercises

**Exercise 1.** A hot-wire probe records $u = 10.2, 9.6, 10.5, 9.9, 9.8, 10.0$ m/s. Compute $\overline{u}$, the fluctuations $u'$, $\overline{u'^2}$, the rms fluctuation and the turbulence intensity $u_{\mathrm{rms}}/\overline{u}$. If the other two components have the same rms value, what inlet $k$ would you specify?

<details>
<summary>Answer</summary>

$\overline{u} = 10.0$ m/s and $u' = (0.2, -0.4, 0.5, -0.1, -0.2, 0)$ m/s, which average to zero.

$\overline{u'^2} = (0.04 + 0.16 + 0.25 + 0.01 + 0.04 + 0)/6 = 0.0833\ \mathrm{m^2/s^2}$, so $u_{\mathrm{rms}} = 0.289$ m/s and the intensity is 2.9 %.

With three equal components, $k = \tfrac{3}{2}\overline{u'^2} = 0.125\ \mathrm{m^2/s^2}$, the same as $\tfrac32(IU)^2$ with $I = 0.0289$ and $U = 10$ m/s. Six samples are far too few for a reliable estimate; a real record needs many integral time scales.

</details>

**Exercise 2.** Integrate the averaged channel momentum equation from the centreline $y = 0$ to $y$ (with $y$ measured from the centreline and the wall at $y = H$) and show that the total shear stress varies linearly. Evaluate it at the wall to show that $`\tau_w = -H\,dP/dx`$.

<details>
<summary>Answer</summary>

Integrating $\frac{d}{dy}\left(\nu\frac{dU}{dy} - \overline{u'v'}\right) = \frac{1}{\rho}\frac{dP}{dx}$ from 0 to $y$, with $dU/dy = 0$ and $\overline{u'v'} = 0$ on the centreline by symmetry:

```math
\nu\frac{dU}{dy} - \overline{u'v'} = \frac{y}{\rho}\frac{dP}{dx}
```

At the wall the fluctuations vanish, so $`\mu\,dU/dy|_H = H\,dP/dx`$. With $dP/dx < 0$ the velocity gradient there is negative (velocity falls towards the wall), and the magnitude of the wall shear stress is $`\tau_w = -H\,dP/dx`$.

</details>

**Exercise 3.** Water ($\rho = 1000\ \mathrm{kg/m^3}$, $\nu = 10^{-6}\ \mathrm{m^2/s}$) flows in a channel of half-height $H = 0.05$ m under $dP/dx = -2$ Pa/m. Compute $\tau_w$, $u_\tau$ and $Re_\tau = u_\tau H/\nu$, and the first-cell-centre heights for $y^+ = 1$ (wall-resolved SST) and $y^+ = 30$ (wall functions). How many cells of growth ratio 1.2 does the wall-resolved mesh need to reach the height of the wall-function cell?

<details>
<summary>Answer</summary>

$\tau_w = 0.05 \times 2 = 0.1$ Pa, $u_\tau = \sqrt{0.1/1000} = 0.01$ m/s and $Re_\tau = 0.01 \times 0.05/10^{-6} = 500$.

$y^+ = 1$ means $y = \nu/u_\tau = 10^{-4}$ m (0.1 mm), and $y^+ = 30$ means $y = 3$ mm.

Taking the first cell height as $2 \times 10^{-4}$ m (centre at $10^{-4}$ m) and the wall-function cell height as $6 \times 10^{-3}$ m, a geometric stack of $n$ cells covers $2\times10^{-4}(1.2^n - 1)/0.2$, which reaches $6\times10^{-3}$ m for $1.2^n = 7$, i.e. $n = 10.7$, so 11 cells replace each wall-function cell.

</details>

**Exercise 4.** A $k$–$`\varepsilon`$ solution gives $k = 0.375\ \mathrm{m^2/s^2}$ and $\varepsilon = 0.5\ \mathrm{m^2/s^3}$ in air ($\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$). Compute $\nu_t = C_\mu k^2/\varepsilon$ and $\nu_t/\nu$, then the Kolmogorov scale $\eta = (\nu^3/\varepsilon)^{1/4}$. Estimate the number of grid points a DNS of a 1 m cube at this dissipation rate would need with a spacing of $\eta$.

<details>
<summary>Answer</summary>

$\nu_t = 0.09 \times 0.375^2/0.5 = 0.0253\ \mathrm{m^2/s}$, about 1690 times $\nu$: turbulent mixing dominates momentum transport.

$\eta = \left((1.5\times10^{-5})^3/0.5\right)^{1/4} = 2.9 \times 10^{-4}$ m.

A 1 m cube with spacing $\eta$ needs $(1/2.9\times10^{-4})^3 \approx 4 \times 10^{10}$ points, before counting the time steps, which is why engineering calculations model the turbulence.

</details>

**Exercise 5.** An SA-based DES of a wing uses wall-parallel spacings $\Delta x = \Delta z = 5$ mm over a boundary layer of thickness $\delta = 20$ mm. Where does the model switch to LES mode, and what is the risk? What wall-parallel spacing keeps the whole boundary layer in RANS mode?

<details>
<summary>Answer</summary>

The largest spacing is $\Delta = 5$ mm (the wall-normal spacing is much smaller), so $C_{\mathrm{DES}}\Delta = 0.65 \times 5 = 3.25$ mm. LES mode starts at $d = 3.25$ mm, inside the boundary layer, which spans 0 to 20 mm.

On a 5 mm grid the boundary layer cannot sustain resolved eddies, so in the outer 84 % of it the modeled stress is reduced without resolved stress to replace it. The skin friction drops and the boundary layer can separate too early (grid-induced separation).

Plain DES needs $C_{\mathrm{DES}}\Delta > \delta$, i.e. $\Delta > 20/0.65 = 31$ mm. DDES removes this constraint by shielding the boundary layer.

</details>

## References

- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000.
- Wilcox, D. C. *Turbulence Modeling for CFD*, 3rd ed. DCW Industries, 2006.
- Launder, B. E., and Spalding, D. B. "The numerical computation of turbulent flows." *Computer Methods in Applied Mechanics and Engineering*, 3(2), 269–289, 1974.
- Spalart, P. R., and Allmaras, S. R. "A one-equation turbulence model for aerodynamic flows." AIAA Paper 92-0439, 1992.
- Menter, F. R. "Two-equation eddy-viscosity turbulence models for engineering applications." *AIAA Journal*, 32(8), 1598–1605, 1994.
- Smagorinsky, J. "General circulation experiments with the primitive equations. I. The basic experiment." *Monthly Weather Review*, 91(3), 99–164, 1963.
- Germano, M., Piomelli, U., Moin, P., and Cabot, W. H. "A dynamic subgrid-scale eddy viscosity model." *Physics of Fluids A*, 3(7), 1760–1765, 1991.
- Spalart, P. R., Deck, S., Shur, M. L., Squires, K. D., Strelets, M. Kh., and Travin, A. "A new version of detached-eddy simulation, resistant to ambiguous grid densities." *Theoretical and Computational Fluid Dynamics*, 20(3), 181–195, 2006.
- Moser, R. D., Kim, J., and Mansour, N. N. "Direct numerical simulation of turbulent channel flow up to $Re_\tau = 590$." *Physics of Fluids*, 11(4), 943–945, 1999.
- Choi, H., and Moin, P. "Grid-point requirements for large eddy simulation: Chapman's estimates revisited." *Physics of Fluids*, 24(1), 011702, 2012.
