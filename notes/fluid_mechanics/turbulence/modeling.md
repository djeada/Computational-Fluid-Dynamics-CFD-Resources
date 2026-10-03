# Turbulence Modeling

The [RANS equations](./rans_equations.md) contain Reynolds stresses that cannot be computed from the mean flow alone. The [energy cascade](./energy_cascade.md) shows that resolving every eddy costs roughly $Re^3$. Turbulence modeling sits between these two facts. It decides which scales are computed, and supplies approximations for the effect of the rest.

This page covers the model hierarchy, the equations and standard constants of the most widely used models, the basics of large-eddy simulation, and how to choose among them. For solver-side practicalities (how these models appear in a CFD workflow, boundary inputs and outputs), see [Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md).

## The Modeling Hierarchy

```
 log E(k)
   ^
   |   ____
   |  /    \___
   | /         \____
   |/               \_____
   |                      \_____
   |                            \____
   |                                 \___
   +--------------------|---------------------\----> log k
   |<-- resolved in LES -->|<--- modeled in LES (SGS) --->|
   |<------------------- resolved in DNS ---------------->|
   |<------------ everything modeled in RANS ------------>|
```

| Approach | Resolved | Modeled | Grid scaling for a flat-plate boundary layer | Typical use |
| --- | --- | --- | --- | --- |
| DNS | All scales down to $\eta$ | Nothing | $Re_{L_x}^{37/14}$ | Physics research, model calibration |
| Wall-resolved LES | Energy-containing eddies, including near-wall streaks | Subgrid scales | $Re_{L_x}^{13/7}$ | Moderate-$Re$ research, aeroacoustics |
| Wall-modeled LES | Outer-layer eddies | Subgrid scales and the inner layer | $Re_{L_x}$ | High-$Re$ flows, increasingly industrial |
| Hybrid RANS–LES (DES family) | Eddies in separated regions | Attached boundary layers (RANS) and subgrid scales | Between RANS and WMLES | Massively separated flows |
| URANS | Large-scale unsteadiness well separated from turbulence | All turbulence | RANS grid | Periodic shedding, slowly varying flows |
| RANS | Mean flow only | All turbulence | Weak dependence on $Re$ | Industrial design and optimization |

The grid scalings are the estimates of Choi and Moin (*Physics of Fluids*, 2012) for a boundary layer of length $L_x$. For homogeneous turbulence, DNS scales as $Re^{9/4}$ (see [Energy Cascade](./energy_cascade.md)).

## Eddy-Viscosity Models: The Common Framework

Most engineering models use the Boussinesq hypothesis (derived in [RANS Equations](./rans_equations.md)):

$$
-\overline{u_i'u_j'} = 2\nu_t\,\overline{S}_{ij} - \frac{2}{3}k\,\delta_{ij}
$$

On dimensional grounds $\nu_t$ is a velocity times a length, $\nu_t \sim u^\ast \ell^\ast$. Models are classified by how many transport equations they solve to obtain these scales:

- **zero-equation** models prescribe both algebraically;
- **one-equation** models transport one quantity;
- **two-equation** models transport two, making them "complete": they need no flow-specific length-scale input.

## Zero-Equation Models: Mixing Length

Prandtl (1925) pictured fluid lumps travelling a distance $\ell_m$ before mixing with their surroundings. The resulting eddy viscosity is

$$
\nu_t = \ell_m^2\left\lvert \frac{\partial U}{\partial y}\right\rvert
\qquad \text{(thin shear layers)},
\qquad \nu_t = \ell_m^2\, S
\qquad \text{(general)}
$$

For wall boundary layers the mixing length is:

- **Log layer:** $\ell_m = \kappa y$, which reproduces the log law exactly.
- **Viscous sublayer:** van Driest damping, $\ell_m = \kappa y\left[1 - \exp(-y^+/A^+)\right]$ with $A^+ = 26$.
- **Outer layer:** capped at $\ell_m \approx 0.09\,\delta$.

Algebraic models of this kind, notably Cebeci–Smith and Baldwin–Lomax, were the workhorses of early aerodynamic CFD. They are cheap, but they have no memory of upstream history. They need a length scale that is hard to define in complex geometries, and they perform poorly in separated flows.

## One-Equation Models: Spalart–Allmaras

The Spalart–Allmaras (SA) model (1992) solves a single transport equation for a working variable $\tilde{\nu}$, which equals $\nu_t$ away from walls. It was built for external aerodynamics and calibrated on mixing layers, wakes and flat-plate boundary layers. The standard form, without the rarely used trip term, is

$$
\frac{\partial \tilde{\nu}}{\partial t} + U_j
\frac{\partial \tilde{\nu}}{\partial x_j} = c_{b1}(1 - f_{t2})\tilde{S}\tilde{\nu} -
\left(c_{w1}f_w -
\frac{c_{b1}}{\kappa^2}f_{t2}\right)\left(\frac{\tilde{\nu}}{d}\right)^2 +
\frac{1}{\sigma}\left[\frac{\partial}{\partial x_j}\left((\nu + \tilde{\nu})
\frac{\partial \tilde{\nu}}{\partial x_j}\right) + c_{b2}
\frac{\partial \tilde{\nu}}{\partial x_i}
\frac{\partial \tilde{\nu}}{\partial x_i}\right]
$$

Here $d$ is the distance to the nearest wall and $\Omega$ is the vorticity magnitude. The eddy viscosity and auxiliary functions are

$$
\nu_t = \tilde{\nu}f_{v1},
\qquad f_{v1} = \frac{\chi^3}{\chi^3 + c_{v1}^3},
\qquad \chi = \frac{\tilde{\nu}}{\nu}
$$

$$
\tilde{S} = \Omega + \frac{\tilde{\nu}}{\kappa^2 d^2}f_{v2},
\qquad f_{v2} = 1 - \frac{\chi}{1 + \chi f_{v1}},
\qquad f_{t2} = c_{t3}\exp(-c_{t4}\chi^2)
$$

$$
f_w = g\left(\frac{1 + c_{w3}^6}{g^6 + c_{w3}^6}\right)^{1/6},
\qquad g = r + c_{w2}(r^6 - r),
\qquad r = \min\left(\frac{\tilde{\nu}}{\tilde{S}\kappa^2 d^2},\ 10\right)
$$

| $c_{b1}$ | $c_{b2}$ | $\sigma$ | $\kappa$ | $c_{w1}$ | $c_{w2}$ | $c_{w3}$ | $c_{v1}$ | $c_{t3}$ | $c_{t4}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1355 | 0.622 | 2/3 | 0.41 | $c_{b1}/\kappa^2 + (1 + c_{b2})/\sigma \approx 3.239$ | 0.3 | 2 | 7.1 | 1.2 | 0.5 |

The equation reads as production proportional to $\tilde{S}\tilde{\nu}$, destruction proportional to $(\tilde{\nu}/d)^2$ (walls damp turbulence through the distance $d$), and diffusion. Many codes set $f_{t2} = 0$ (the "SA-noft2" variant). Boundary conditions are $\tilde{\nu} = 0$ at walls and a small free-stream value, typically $\tilde{\nu}/\nu \approx 3$–5.

SA is robust, cheap, and accurate for attached and mildly separated aerodynamic boundary layers. It is less reliable for free shear flows and massive separation. It provides no $k$, so inlet turbulence intensity has no direct meaning in it.

## Two-Equation Models

### Standard $k$–$\varepsilon$

The standard model of Launder and Spalding (1974) transports $k$ and $\varepsilon$ and forms $\nu_t = C_\mu k^2/\varepsilon$:

$$
\frac{\partial k}{\partial t} + U_j
\frac{\partial k}{\partial x_j} = \frac{\partial}{\partial x_j}\left[\left(\nu +
\frac{\nu_t}{\sigma_k}\right) \frac{\partial k}{\partial x_j}\right] + \mathcal{P}_k -
\varepsilon
$$

$$
\frac{\partial \varepsilon}{\partial t} + U_j
\frac{\partial \varepsilon}{\partial x_j} = \frac{\partial}{\partial x_j}\left[\left(\nu + \frac{\nu_t}{\sigma_\varepsilon}\right) \frac{\partial \varepsilon}{\partial x_j}\right] + C_{\varepsilon 1} \frac{\varepsilon}{k}\mathcal{P}_k - C_{\varepsilon 2} \frac{\varepsilon^2}{k}
$$

Production is $\mathcal{P}_k = \nu_t S^2$. The $k$ equation is a modeled version of the exact TKE equation, with gradient-diffusion transport. The $\varepsilon$ equation is largely empirical.

| $C_\mu$ | $C_{\varepsilon 1}$ | $C_{\varepsilon 2}$ | $\sigma_k$ | $\sigma_\varepsilon$ |
| --- | --- | --- | --- | --- |
| 0.09 | 1.44 | 1.92 | 1.0 | 1.3 |

The constants are not arbitrary.

- **$C_{\varepsilon 2}$ from decaying turbulence.** With no mean gradients, $dk/dt = -\varepsilon$ and $d\varepsilon/dt = -C_{\varepsilon 2}\varepsilon^2/k$. These give power-law decay $k \propto t^{-n}$ with $n = 1/(C_{\varepsilon 2} - 1) = 1.09$. Grid-turbulence experiments give values of roughly 1.1 to 1.4.
- **$C_\mu$ from equilibrium shear layers.** If $\mathcal{P}_k = \varepsilon$, the Boussinesq relation gives $(\overline{u'v'})^2 = \nu_t^2(dU/dy)^2 = \nu_t\,\varepsilon = C_\mu k^2$, i.e. $-\overline{u'v'}/k = C_\mu^{1/2}$. The measured ratio is about 0.3, hence $C_\mu = 0.09$.
- **$\sigma_\varepsilon$ from the log law.** Substituting the log-layer solution into the $\varepsilon$ equation requires $\kappa^2 = \sigma_\varepsilon C_\mu^{1/2}(C_{\varepsilon 2} - C_{\varepsilon 1})$. The standard constants imply $\kappa = 0.433$, close to 0.41 (Exercise 1).
- **$C_{\varepsilon 1}$ and $\sigma_k$** were set by fitting homogeneous shear-flow data and by analogy, respectively.

In use, $\varepsilon$ is ill-behaved at walls. The model is therefore used with **wall functions**, or with low-Reynolds-number damping functions or two-layer formulations. It performs well in free shear flows and flows without strong pressure gradients. It overpredicts turbulence at stagnation points, responds too weakly to adverse pressure gradients (separation is predicted too late or not at all), and ignores curvature and swirl. The RNG and realizable variants modify the $\varepsilon$ equation and $C_\mu$ to address some of these problems.

### $k$–$\omega$

Wilcox's model replaces $\varepsilon$ with the specific dissipation rate $\omega \sim \varepsilon/k$, a turbulence frequency. In its 1988 form:

$$
\frac{\partial k}{\partial t} + U_j \frac{\partial k}{\partial x_j} = \mathcal{P}_k -
\beta^\ast k\omega +
\frac{\partial}{\partial x_j}\left[(\nu + \sigma^\ast\nu_t)
\frac{\partial k}{\partial x_j}\right]
$$

$$
\frac{\partial \omega}{\partial t} + U_j \frac{\partial \omega}{\partial x_j} = \alpha
\frac{\omega}{k}\mathcal{P}_k - \beta\omega^2 +
\frac{\partial}{\partial x_j}\left[(\nu + \sigma\nu_t)
\frac{\partial \omega}{\partial x_j}\right]
$$

with $\nu_t = k/\omega$ and $\varepsilon = \beta^\ast k\omega$.

| $\alpha$ | $\beta$ | $\beta^\ast$ | $\sigma$ | $\sigma^\ast$ |
| --- | --- | --- | --- | --- |
| 5/9 | 3/40 | 9/100 | 1/2 | 1/2 |

The log-layer consistency condition is $\alpha = \beta/\beta^\ast - \sigma\kappa^2/\sqrt{\beta^\ast}$, which with these values gives $\kappa = 0.408$. Decaying turbulence follows $k \propto t^{-\beta^\ast/\beta} = t^{-1.2}$.

Near a smooth wall the exact solution is $\omega \to 6\nu/(\beta y^2)$. The equations can therefore be integrated to the wall without damping functions, which gives better behaviour than $k$–$\varepsilon$ in adverse pressure gradients. Menter's practical boundary condition is $\omega_{wall} = 10 \times 6\nu/(\beta_1 \Delta y_1^2)$, where $\Delta y_1$ is the first-cell distance.

The main weakness of the 1988 model is a strong sensitivity to the free-stream value of $\omega$. Wilcox's 2006 revision reduces this with a cross-diffusion term and a stress limiter. Its constants are $\alpha = 13/25$, $\beta_0 = 0.0708$, $\beta^\ast = 0.09$, $\sigma = 1/2$, $\sigma^\ast = 3/5$ and $\sigma_{do} = 1/8$.

### Menter SST

The shear-stress transport (SST) model (Menter, 1994) blends the two approaches. It uses $k$–$\omega$ near walls, where it performs well, and switches to a $k$–$\varepsilon$ model rewritten in $\omega$ form away from walls, which removes the free-stream sensitivity. It also limits the eddy viscosity in adverse pressure gradients.

$$
\frac{\partial k}{\partial t} + U_j
\frac{\partial k}{\partial x_j} = \tilde{\mathcal{P}}_k - \beta^\ast k\omega +
\frac{\partial}{\partial x_j}\left[(\nu + \sigma_k\nu_t)
\frac{\partial k}{\partial x_j}\right]
$$

$$
\frac{\partial \omega}{\partial t} + U_j
\frac{\partial \omega}{\partial x_j} = \frac{\gamma}{\nu_t}\mathcal{P}_k -
\beta\omega^2 +
\frac{\partial}{\partial x_j}\left[(\nu + \sigma_\omega\nu_t)
\frac{\partial \omega}{\partial x_j}\right] + 2(1 - F_1)
\frac{\sigma_{\omega 2}}{\omega} \frac{\partial k}{\partial x_j}
\frac{\partial \omega}{\partial x_j}
$$

$$
\nu_t = \frac{a_1 k}{\max(a_1\omega,\ \Omega F_2)}
$$

The blending functions use the wall distance $y$:

$$
F_1 = \tanh\left(\mathrm{arg}_1^4\right),
\qquad
\mathrm{arg}_1 = \min\left[\max\left(\frac{\sqrt{k}}{\beta^\ast\omega y},\
\frac{500\nu}{y^2\omega}\right),\  \frac{4\sigma_{\omega 2}k}{CD_{k\omega}\,y^2}\right]
$$

$$
CD_{k\omega} = \max\left(\frac{2\sigma_{\omega 2}}{\omega}
\frac{\partial k}{\partial x_j} \frac{\partial \omega}{\partial x_j},\ 10^{-20}\right),
\qquad F_2 = \tanh\left(\mathrm{arg}_2^2\right),
\qquad
\mathrm{arg}_2 = \max\left(\frac{2\sqrt{k}}{\beta^\ast\omega y},\
\frac{500\nu}{y^2\omega}\right)
$$

Each coefficient $\phi$ is blended as $\phi = F_1\phi_1 + (1 - F_1)\phi_2$, where set 1 applies near the wall ($F_1 \to 1$) and set 2 in the free stream ($F_1 \to 0$). Common constants are $\beta^\ast = 0.09$, $\kappa = 0.41$ and $a_1 = 0.31$, with $\gamma_i = \beta_i/\beta^\ast - \sigma_{\omega i}\kappa^2/\sqrt{\beta^\ast}$.

| Set | $\sigma_k$ | $\sigma_\omega$ | $\beta$ | $\gamma$ |
| --- | --- | --- | --- | --- |
| 1 (inner, $k$–$\omega$) | 0.85 | 0.5 | 0.075 | 0.553 |
| 2 (outer, $k$–$\varepsilon$) | 1.0 | 0.856 | 0.0828 | 0.440 |

The eddy-viscosity limiter encodes Bradshaw's observation that $-\overline{u'v'} \approx a_1 k$ in boundary layers. In adverse pressure gradients, where production exceeds dissipation, the standard formula overpredicts the shear stress and delays separation; the limiter caps it.

The 2003 revision (Menter, Kuntz and Langtry) uses the strain-rate magnitude $S$ in place of $\Omega$ in the limiter, limits production to $\tilde{\mathcal{P}}_k = \min(\mathcal{P}_k,\ 10\beta^\ast k\omega)$, and uses $10^{-10}$ as the lower bound in $CD_{k\omega}$. SST is among the most widely used general-purpose RANS models.

## Reynolds Stress Models

Reynolds stress models (RSM) drop the Boussinesq hypothesis. They solve the six transport equations for $\overline{u_i'u_j'}$ derived in [RANS Equations](./rans_equations.md), plus an equation for $\varepsilon$ or $\omega$. Production is then exact, and the modeling effort goes into the pressure–strain term. A classic closure combines two parts:

- **Rotta's return-to-isotropy term:** $-2C_1\varepsilon\,b_{ij}$.
- **The isotropization-of-production term:** $-C_2\left(P_{ij} - \frac{2}{3}\mathcal{P}\,\delta_{ij}\right)$.

The LRR-IP model uses $C_1 = 1.8$ and $C_2 = 0.6$. RSMs naturally capture normal-stress anisotropy, streamline curvature, rotation and swirl, and secondary flows in ducts. The cost is seven equations, stiffer numerics, and less robust convergence.

## Large-Eddy Simulation

### Filtering

LES computes the large, geometry-dependent eddies directly and models only the small, more universal ones. The velocity is **filtered** with a kernel $G$ of width $\Delta$:

$$
\overline{u}_i(\mathbf{x},t) = \int G(\mathbf{r};\Delta)\,
u_i(\mathbf{x} - \mathbf{r},t)\, d\mathbf{r},
\qquad \int G(\mathbf{r};\Delta)\, d\mathbf{r} = 1
$$

Common kernels are the box (top-hat), the Gaussian, and the sharp spectral cutoff at $\kappa_c = \pi/\Delta$. Many codes filter implicitly, through the grid and discretization. Here the overbar denotes filtering, which is not a Reynolds average. In general $\overline{\overline{u}} \ne \overline{u}$, and the residual $u' = u - \overline{u}$ does not filter to zero, except for the sharp spectral filter.

Filtering the incompressible Navier–Stokes equations, and assuming the filter commutes with derivatives, gives

$$
\frac{\partial \overline{u}_i}{\partial t} +
\frac{\partial (\overline{u}_i\overline{u}_j)}{\partial x_j} = -\frac{1}{\rho}
\frac{\partial \overline{p}}{\partial x_i} + \nu
\frac{\partial^2 \overline{u}_i}{\partial x_j\partial x_j} -
\frac{\partial \tau_{ij}^r}{\partial x_j},
\qquad \tau_{ij}^r = \overline{u_iu_j} - \overline{u}_i\overline{u}_j
$$

The **subgrid-scale (SGS) stress** $\tau_{ij}^r$ plays the role of the Reynolds stress. It drains energy from the resolved field at the rate $\Pi = -\tau_{ij}^r\overline{S}_{ij}$. If the filter lies in the inertial range, the mean of $\Pi$ equals $\varepsilon$.

Pope suggests that a well-resolved LES should resolve at least about 80% of the turbulent kinetic energy. Near walls, the energetic structures scale with the viscous length: low-speed streaks are spaced about 100 wall units apart. Wall-resolved LES therefore becomes expensive at high Reynolds number, which is what motivates wall-modeled LES and hybrid methods.

### The Smagorinsky Model

Smagorinsky (1963) proposed an eddy viscosity built from the filter width and the resolved strain rate:

$$
\tau_{ij}^r - \frac{1}{3}\tau_{kk}^r\,\delta_{ij} = -2\nu_r\overline{S}_{ij},
\qquad \nu_r = (C_s\Delta)^2\,\lvert \overline{S} \rvert,
\qquad \lvert \overline{S} \rvert = \sqrt{2\,\overline{S}_{ij}\overline{S}_{ij}}
$$

The SGS dissipation is then $\Pi = \nu_r\lvert \overline{S} \rvert^2 \ge 0$. The model always removes energy from the resolved scales and cannot represent backscatter.

**Lilly's estimate** of $C_s$ assumes a sharp cutoff inside a Kolmogorov inertial range $E = C_K\varepsilon^{2/3}\kappa^{-5/3}$ and requires $\langle \Pi \rangle = \varepsilon$. This gives

$$
C_s = \frac{1}{\pi}\left(\frac{2}{3C_K}\right)^{3/4} \approx 0.17
\qquad (C_K = 1.5)
$$

In practice $C_s \approx 0.1$ works better in shear flows such as channels. The model is too dissipative near walls, where $\lvert \overline{S} \rvert$ is large but turbulence is damped. Standard remedies are:

- van Driest damping of $C_s\Delta$;
- the **dynamic procedure** (Germano et al., 1991; Lilly, 1992), which computes $C_s$ locally from the resolved field using a test filter;
- the **WALE** model, whose eddy viscosity vanishes naturally at walls.

If SGS dissipation balances $\varepsilon$, the Smagorinsky viscosity can be estimated as $\nu_r = (C_s\Delta)^{4/3}\varepsilon^{1/3}$.

## Hybrid RANS–LES: Detached-Eddy Simulation

Detached-eddy simulation (DES) was introduced by Spalart and co-workers in 1997. It uses one model that acts as RANS in attached boundary layers and as an LES subgrid model in separated regions. In the SA-based version, the wall distance $d$ in the destruction term is replaced by

$$
\tilde{d} = \min(d,\  C_{DES}\Delta),
\qquad \Delta = \max(\Delta x, \Delta y, \Delta z),
\qquad C_{DES} = 0.65
$$

Close to walls, $d < C_{DES}\Delta$ and the model is plain SA. Far from walls, the length scale becomes proportional to $\Delta$ and the model behaves like a Smagorinsky-type SGS model.

The weakness is the switch location. It depends on the grid, not the flow. If the wall-parallel spacing becomes smaller than the boundary-layer thickness, LES mode activates inside an attached boundary layer whose grid cannot support resolved eddies. The modeled stress is then depleted, which can cause grid-induced separation. **Delayed DES** (DDES, 2006) adds a shielding function that keeps boundary layers in RANS mode. **Improved DDES** (IDDES) adds wall-modeled LES capability. SST-based variants compare $k^{1/2}/(\beta^\ast\omega)$ with $C_{DES}\Delta$.

## Worked Examples

### Inlet Turbulence Quantities

Air ($\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$) enters a duct with hydraulic diameter $D_h = 0.2$ m at $U = 10$ m/s. The inlet turbulence intensity is $I = 5\%$, and the common rule of thumb for duct flow gives a turbulence length scale $\ell = 0.07D_h = 0.014$ m.

$$
k = \frac{3}{2}(IU)^2 = 0.375\ \mathrm{m^2/s^2}
$$

$$
\varepsilon = C_\mu^{3/4} \frac{k^{3/2}}{\ell} = 2.70\ \mathrm{m^2/s^3},
\qquad \omega = \frac{k^{1/2}}{C_\mu^{1/4}\ell} = 79.9\ \mathrm{s^{-1}}
$$

$$
\nu_t = C_\mu \frac{k^2}{\varepsilon} = \frac{k}{\omega} = 4.70 \times
10^{-3}\ \mathrm{m^2/s},
\qquad \frac{\nu_t}{\nu} = 313
$$

The two routes to $\nu_t$ agree, and $\varepsilon = \beta^\ast k\omega$ holds, which confirms consistency. Viscosity ratios of hundreds at the inlet are normal for internal flows. For external aerodynamics much lower values (order 1–10) are typical. Uncertain inlet values should be tested for their influence on the result.

### Smagorinsky Viscosity in a Pipe LES

For the water pipe of the [Energy Cascade](./energy_cascade.md) worked example, $\varepsilon \approx 0.63\ \mathrm{W/kg}$ and $\eta \approx 36\ \mu\mathrm{m}$. Take a filter width $\Delta = 2$ mm, about $56\eta$, which lies in the inertial range.

| $C_s$ | $\Delta$ (mm) | $\nu_r = (C_s\Delta)^{4/3}\varepsilon^{1/3}$ ($\mathrm{m^2/s}$) | $\nu_r/\nu$ |
| --- | --- | --- | --- |
| 0.17 | 2 | $2.1 \times 10^{-5}$ | 21 |
| 0.17 | 1 | $8.3 \times 10^{-6}$ | 8.3 |
| 0.10 | 2 | $1.0 \times 10^{-5}$ | 10 |

The SGS viscosity exceeds the molecular viscosity by an order of magnitude and scales as $\Delta^{4/3}$. Away from walls, the resolved LES dynamics are controlled by the model rather than by $\nu$. This is why grid refinement studies are essential in LES.

## Choosing a Model

| Flow | Reasonable starting point | Watch out for |
| --- | --- | --- |
| Attached external aerodynamics (wings, bodies) | SA or SST | Transition location if not fully turbulent |
| Adverse pressure gradients, smooth-surface separation | SST | Every RANS model is uncertain for separation and reattachment |
| Internal flows, ducts, industrial equipment without strong swirl | Realizable $k$–$\varepsilon$ or SST, with matching wall treatment | $y^+$ consistent with the wall treatment |
| Strong swirl, curvature, rotation, duct secondary flows | RSM, or eddy-viscosity models with curvature corrections | Linear Boussinesq models miss these effects |
| Impinging jets and stagnation-point heat transfer | SST or RSM | Standard $k$–$\varepsilon$ overpredicts stagnation turbulence |
| Free shear flows (jets, wakes, mixing layers) | $k$–$\varepsilon$ family | Spreading-rate errors differ between plane and round jets |
| Bluff bodies, massive separation, unsteady loads, aeroacoustics | DDES or LES | Grid and time-step resolution; statistical sampling time |
| Transitional flows (low-Re aerofoils, turbomachinery) | RANS with a transition model, or LES | Fully turbulent models ignore laminar regions |
| Fundamental physics and model development | DNS | Cost scales as $Re^3$ |

General guidance:

1. **Start from the quantity you need.** Mean pressure drop, peak heat flux, separation location and unsteady loads place very different demands on a model.
2. **Estimate the scales first.** Reynolds number, $\eta$ and the boundary-layer thickness tell you whether LES or DNS is affordable at all (see [Energy Cascade](./energy_cascade.md)).
3. **Match the mesh to the wall treatment.** Compute the expected $y^+$ before meshing (see [RANS Equations](./rans_equations.md)).
4. **Establish grid independence before comparing models.** Otherwise model and discretization errors cannot be separated (see [Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md)).
5. **Use more than one model.** The spread between reasonable models is a useful, if crude, measure of modeling uncertainty.
6. **Validate against data for a similar flow.** Do not expect a steady RANS model to predict phenomena it was never calibrated for, such as transition, unsteady massive separation or relaminarization.

## Related Scripts

- [turbulent_flow](../../../scripts/plots/turbulent_flow/): the mean-plus-fluctuation split of a velocity signal. RANS computes only the mean line in that figure, while LES and DNS resolve the fluctuations.
- [kelvin_helmholtz_instability](../../../scripts/simulations/kelvin_helmholtz_instability/): an unsteady shear-layer roll-up of the kind that scale-resolving methods (LES, DES) capture explicitly and steady RANS averages away.
- [boundary_layer_velocity_profile](../../../scripts/plots/boundary_layer_velocity_profile/): a turbulent mean velocity profile, the kind of target a RANS model with correct wall behaviour must reproduce.
- [Mean Pressure Coefficient Along Vehicle Centreline](../../../scripts/plots/mean_pressure_coefficient/): plots a mock validation figure of mean pressure coefficient $C_P$ against streamwise position, comparing "experimental" data with a "CFD SRS" (scale-resolving simulation) curve that under-predicts a separation plateau.

## Exercises

**Exercise 1.** In the log layer of an equilibrium boundary layer, show that the standard $k$–$\varepsilon$ model gives $-\overline{u'v'}/k = C_\mu^{1/2}$. Then compute the von Kármán constant implied by $\kappa^2 = \sigma_\varepsilon C_\mu^{1/2}(C_{\varepsilon 2} - C_{\varepsilon 1})$ with the standard constants. What value of $\sigma_\varepsilon$ would give $\kappa = 0.41$?

<details>
<summary>Answer</summary>

**Stress-to-energy ratio.** With $\mathcal{P}_k = \varepsilon$ and $-\overline{u'v'} = \nu_t\,dU/dy$:

```math
(\overline{u'v'})^2 = \nu_t\cdot\nu_t\left(\frac{dU}{dy}\right)^2 = \nu_t\,\varepsilon = C_\mu k^2
```

so $-\overline{u'v'}/k = C_\mu^{1/2} = 0.3$.

**Implied von Kármán constant.** $\kappa = \sqrt{1.3 \times 0.3 \times 0.48} = 0.433$.

**Required $\sigma_\varepsilon$.** For $\kappa = 0.41$, $\sigma_\varepsilon = 0.41^2/(0.3 \times 0.48) = 1.17$.

</details>

**Exercise 2.** In decaying homogeneous turbulence, with no mean gradients and no transport, find the power-law decay exponent $n$ in $k \propto t^{-n}$ predicted by the standard $k$–$\varepsilon$ model and by the 1988 $k$–$\omega$ model.

<details>
<summary>Answer</summary>

**$k$–$\varepsilon$.** The model equations are $dk/dt = -\varepsilon$ and $d\varepsilon/dt = -C_{\varepsilon 2}\varepsilon^2/k$. Substituting $k \propto t^{-n}$ gives $\varepsilon = nk/t$. Then $d\varepsilon/dt = -n(n+1)k/t^2$ must equal $-C_{\varepsilon 2}n^2k/t^2$, so $n = 1/(C_{\varepsilon 2} - 1) = 1/0.92 = 1.09$.

**$k$–$\omega$.** The equation $d\omega/dt = -\beta\omega^2$ gives $\omega = 1/(\beta t)$. Then $dk/dt = -\beta^\ast k\omega = -(\beta^\ast/\beta)k/t$, so $n = \beta^\ast/\beta = 0.09/0.075 = 1.2$.

</details>

**Exercise 3.** A wind-tunnel inlet has $U = 50$ m/s, $I = 2\%$ and turbulence length scale $\ell = 0.01$ m, in air with $\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$. Compute $k$, $\varepsilon$, $\omega$ and $\nu_t/\nu$ using $C_\mu = 0.09$.

<details>
<summary>Answer</summary>

- $k = 1.5(0.02 \times 50)^2 = 1.5\ \mathrm{m^2/s^2}$
- $\varepsilon = 0.09^{3/4} \times 1.5^{3/2}/0.01 = 30.2\ \mathrm{m^2/s^3}$
- $\omega = 1.5^{1/2}/(0.09^{1/4} \times 0.01) = 224\ \mathrm{s^{-1}}$
- $\nu_t = k/\omega = 6.7 \times 10^{-3}\ \mathrm{m^2/s}$, so $\nu_t/\nu = 447$

</details>

**Exercise 4.** Evaluate Lilly's Smagorinsky constant for $C_K = 1.5$. An atmospheric-boundary-layer LES uses $\Delta = 1$ m where $\varepsilon = 10^{-2}\ \mathrm{m^2/s^3}$. Estimate $\nu_r$ and compare it with the molecular viscosity of air ($1.5 \times 10^{-5}\ \mathrm{m^2/s}$).

<details>
<summary>Answer</summary>

**Lilly's constant.** $C_s = \frac{1}{\pi}(2/4.5)^{3/4} = 0.173$.

**SGS viscosity.** $\nu_r = (C_s\Delta)^{4/3}\varepsilon^{1/3} = (0.173)^{4/3}(0.01)^{1/3} = 0.021\ \mathrm{m^2/s}$.

**Comparison.** $\nu_r/\nu \approx 1{,}400$. Molecular viscosity is irrelevant to the resolved dynamics of such an LES. This is why atmospheric LES often omits it entirely.

</details>

**Exercise 5.** An SA-based DES grid near a wing has $\Delta = \max(\Delta x, \Delta y, \Delta z) = 50$ mm, driven by the wall-parallel spacing, and the local boundary layer is $\delta = 100$ mm thick. Where does the model switch to LES mode? What problem does this cause, and how does DDES address it?

<details>
<summary>Answer</summary>

**Switch location.** LES mode applies where $d > C_{DES}\Delta = 0.65 \times 50 = 32.5$ mm, i.e. in the outer 67% of the attached boundary layer.

**Problem.** A wall-parallel spacing of $\delta/2$ is far too coarse to resolve boundary-layer eddies. The modeled Reynolds stress is reduced without resolved stress replacing it (modeled-stress depletion). Skin friction drops, and the boundary layer may separate for purely numerical reasons.

**DDES remedy.** DDES multiplies the switch by a shielding function, based on the ratio of the eddy viscosity to wall distance and velocity gradients, that keeps the whole attached boundary layer in RANS mode regardless of $\Delta$.

</details>

## References

- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000. (Chapters 10–13: RANS models, LES, and the Smagorinsky model with Lilly's analysis.)
- Wilcox, D. C. *Turbulence Modeling for CFD*, 3rd ed. DCW Industries, 2006.
- Launder, B. E., and Spalding, D. B. "The numerical computation of turbulent flows." *Computer Methods in Applied Mechanics and Engineering*, 3(2), 269–289, 1974.
- Spalart, P. R., and Allmaras, S. R. "A one-equation turbulence model for aerodynamic flows." AIAA Paper 92-0439, 1992.
- Menter, F. R. "Two-equation eddy-viscosity turbulence models for engineering applications." *AIAA Journal*, 32(8), 1598–1605, 1994.
