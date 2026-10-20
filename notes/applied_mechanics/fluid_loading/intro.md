# Fluid Loading on Structures

Structures in wind, currents and waves, and structures that contain liquids, carry loads that come from the surrounding fluid: hydrostatic pressure on dams and hulls, drag and lift on buildings and bridges, wave forces on offshore platforms, the oscillating forces of vortex shedding, and the inertia of the water that moves with a vibrating body. This section of the notes treats these loads from the structural side: how to compute them, how a structure responds to them, and when the response changes the load so that fluid and structure must be solved together. It is where the applied mechanics notes meet fluid mechanics and CFD. This introduction sets out the components of a fluid load, the coefficients and dimensionless groups used to describe it, and the decision between one-way and two-way coupling, and points to the notes that develop each topic.

## Problem Statement

Given a structure (geometry, mass, stiffness and damping, or its natural frequencies, mode shapes and damping ratios), a fluid (density $\rho$, viscosity $\mu$) and the incident flow (a steady current, a wind profile with turbulence, a wave field, or the internal flow of a pipe or tank), find the distributed fluid load, its resultant forces and moments, the static and dynamic structural response, and whether any flow-induced instability can occur in the operating range. The fluid load is always the surface integral of pressure and wall shear stress over the wetted surface $S$, with outward normal $\mathbf{n}$:

```math
\mathbf{F} = \int_S\left(-p\,\mathbf{n} + \boldsymbol{\tau}_w\right)dA
```

For each structural mode with generalised coordinate $x$ the response obeys

$$
m\ddot{x} + c\dot{x} + kx = F(t, x, \dot{x}, \ddot{x})
$$

where the dependence of $F$ on the motion is what distinguishes the problems of this section. When it can be neglected the load is computed once on the undeformed structure; when it cannot, part of it moves to the left-hand side as added mass, fluid damping and fluid stiffness, and the rest is an excitation:

$$
(m + m_a)\ddot{x} + (c + c_f)\dot{x} + (k + k_f)x = F_{\mathrm{exc}}(t)
$$

The structure is usually linear elastic with small deflections; the fluid may be inviscid (potential flow, waves) or viscous and turbulent (drag, separation, vortex shedding).

## Components of a Fluid Load

| Component | Origin | Scales with | Treated in |
| --- | --- | --- | --- |
| Hydrostatic pressure | Weight of a fluid at rest | $\rho gh$ | [Pressure Forces on Structures](./pressure_forces.md) |
| Steady pressure (form) force | Pressure differences in a moving flow, separation | $\tfrac12\rho U^2$ | [Pressure Forces](./pressure_forces.md), [Wind Loading](./wind_loading.md) |
| Viscous (friction) force | Wall shear stress | $\tfrac12\rho U^2$, depends on $Re$ | [Understanding Drag](../../fluid_mechanics/viscous_flow/drag.md) |
| Inertia force | Acceleration of the fluid (Froude–Krylov) and of the disturbed flow (added mass) | $\rho V\dot{u}$ | [Wave Loading](./wave_loading.md), [Hydroelastic Applications](./hydroelastic_applications.md) |
| Turbulent buffeting | Gusts and turbulence in the oncoming flow | $\rho Uu'$ | [Wind Loading](./wind_loading.md) |
| Wake excitation | Vortex shedding from the body itself | $\tfrac12\rho U^2C_L$ at $`f_s = St\,U/D`$ | [Flow-Induced Vibrations](./flow_induced_vibrations.md) |
| Motion-dependent forces | The structure's own velocity and displacement change the flow | Fluid damping $c_f$ and stiffness $k_f$ | [Flow-Induced Vibrations](./flow_induced_vibrations.md) |

Pressure and viscous contributions differ in importance with the body shape. On a bluff body (a cylinder, a building, a bridge pier) the flow separates and most of the drag is the pressure difference between front and rear; on a streamlined body (a wing, a ship hull, a pipeline in axial flow) the flow stays attached and friction dominates the drag. Potential-flow theory predicts the inertia forces well but gives zero drag on any body in steady flow, d'Alembert's paradox ([Potential Flow Theory](../../fluid_mechanics/inviscid_flow/potential_flow.md)), so drag always needs viscous theory, experiment or CFD.

## Force and Moment Coefficients

Fluid loads are reported as coefficients, which remove the dependence on $\rho$, $U$ and size:

$$
C_D = \frac{F_D}{\tfrac12\rho U^2A},
\qquad C_L = \frac{F_L}{\tfrac12\rho U^2A},
\qquad C_M = \frac{M}{\tfrac12\rho U^2AL},
\qquad C_p = \frac{p - p_\infty}{\tfrac12\rho U^2}
$$

with drag along the free stream, lift across it, a reference area $A$ (frontal area, plan area, or diameter times length per unit span) and a reference length $L$. A coefficient is meaningless without its reference area and length. For slender members per unit length the area is the diameter, so $`f_D = \tfrac12\rho C_DD\,U^2`$. In unsteady flows the mean, the fluctuating (root-mean-square) and the peak coefficients are distinct quantities, and design uses all three.

## Dimensionless Groups

| Group | Definition | Governs |
| --- | --- | --- |
| Reynolds number | $Re = \rho UD/\mu$ | Boundary-layer state, separation, $C_D$ and $St$ (drag crisis of the cylinder near $Re \approx 2$–$`5 \times 10^5`$) |
| Strouhal number | $St = f_sD/U$ | Vortex-shedding frequency; about 0.2 for a circular cylinder at subcritical $Re$ |
| Keulegan–Carpenter number | $\mathrm{KC} = u_mT/D$ | Oscillatory flow: drag share and separation in wave loading |
| Froude number | $Fr = U/\sqrt{gL}$ | Free-surface waves, ship wave resistance, model scaling in wave basins |
| Reduced velocity | $U_r = U/(f_nD)$ | Ratio of the flow time scale to the structural period; lock-in near $U_r \approx 1/St$ |
| Mass ratio | $m^* = m/(\rho\pi D^2/4)$ | Structural mass per displaced fluid mass; added-mass effects and the width of lock-in |
| Scruton number | $Sc = 2m\delta/(\rho D^2)$ | Mass–damping parameter, with $\delta \approx 2\pi\zeta$; VIV amplitude |
| Frequency ratio | $r = f/f_n$ | Dynamic amplification of a forced response |

Model tests cannot match all of them at once. Wave basins scale by Froude number, so the model Reynolds number is too low by the scale factor to the power 1.5, and drag-dominated members and separation must be corrected. Wind tunnels for buildings rely on sharp-edged shapes, whose separation points do not depend on $Re$. CFD can run at full scale but must then model turbulence ([Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md)).

## Static or Dynamic Response

A load that varies slowly compared with the structure's natural period acts quasi-statically. For harmonic forcing at frequency ratio $r = f/f_n$ and damping ratio $\zeta$ the dynamic amplification factor is

$$
\mathrm{DAF} = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}
$$

which is 1.04 at $r = 0.2$ but 5.2 at $r = 0.9$ and 25 at resonance for $\zeta = 0.02$ ([Mechanical Vibrations](../dynamics/vibrations.md)). Fluid loads are rarely harmonic: wind and waves are random, with spectra, and the response is found spectrally or by time-domain simulation. The questions are where the load spectrum has energy relative to the natural frequencies, and how much damping is available.

## One-Way or Two-Way Coupling

The most important modelling decision is whether the structure's motion feeds back into the flow.

1. One-way coupling applies when deflections and structural velocities are too small to change the flow, as for a dam, most buildings under mean wind, and stiff jacket members. The load is computed on the undeformed geometry, by hand, from code coefficients or by CFD, and applied to a structural model, statically or as a time history.
2. Two-way coupling with a simple fluid model applies when the feedback can be represented by coefficients: added mass in water, hydrodynamic damping from the Morison drag on relative velocity, aerodynamic damping in the gust factor, quasi-steady galloping forces.
3. Fully coupled simulation is needed when the feedback changes the flow qualitatively: VIV lock-in, flutter, slamming of a flexible hull, sails, heart valves, a flexible plate in water.

The indicators are the deflection relative to the body size, the structural velocity relative to the flow velocity, the reduced velocity relative to the lock-in and instability speeds, the added-mass ratio $m_a/m_s$ and the closeness of load and natural frequencies. [Fluid–Structure Interaction: Coupling Methods](./fluid_structure_interaction.md) gives a decision table and develops the numerical coupling; the [FSI theory note](../../fluid_mechanics/specialized_topics/fluid_structure_interaction.md) gives the field equations.

### Worked Example: Screening a Cylinder in a Current

A cylinder of diameter $D = 0.1$ m with natural frequency $f_n = 5$ Hz in water and mass 16 kg/m stands in a current of $U = 2$ m/s ($\rho = 1000$ kg/m³, $\nu = 10^{-6}$ m²/s).

1. $Re = UD/\nu = 2 \times 10^5$: subcritical, near the drag crisis, so $C_D$ is uncertain between about 0.5 and 1.2.
2. The shedding frequency is $f_s = 0.2 \times 2/0.1 = 4$ Hz, close to $f_n$.
3. $U_r = 2/(5 \times 0.1) = 4$, at the lower edge of the lock-in band $4 \lesssim U_r \lesssim 8$.
4. $m^* = 16/(1000\pi \times 0.01/4) = 2.0$: the added mass is half the structural mass, and lock-in at low mass ratio is wide.

The cylinder can lock in at a slightly higher current, and the large added-mass ratio means its motion will change the wake. A one-way load calculation with a static $C_D$ would miss the dominant oscillating cross-flow load. The design must either move $f_n$ well away, suppress shedding, or be assessed with a VIV model.

## Notes in This Section

| Note | Content |
| --- | --- |
| [Pressure Forces on Structures](./pressure_forces.md) | Hydrostatic forces and centres of pressure, curved surfaces, buoyancy and stability, $C_p$, integrating CFD surface fields into forces |
| [Wind Loading on Structures](./wind_loading.md) | Atmospheric boundary layer, turbulence and gusts, pressure coefficients, along-wind gust factor, across-wind shedding, galloping |
| [Wave Loading on Offshore Structures](./wave_loading.md) | Airy wave theory, Morison equation and KC regimes, MacCamy–Fuchs diffraction, wave spectra and extremes |
| [Flow-Induced Vibrations](./flow_induced_vibrations.md) | VIV and lock-in, galloping, wake galloping, buffeting, flutter, tube-bundle instability, mitigation |
| [Hydroelastic Applications](./hydroelastic_applications.md) | Added mass and wet frequencies, ship springing and whipping, blades, risers and pipes conveying fluid, sloshing |
| [Fluid–Structure Interaction: Coupling Methods](./fluid_structure_interaction.md) | One-way and two-way coupling, monolithic and partitioned schemes, added-mass instability, Aitken relaxation, data transfer, ALE and the geometric conservation law |

## Key Takeaways

- Every fluid load is the integral of $`-p\,\mathbf{n} + \boldsymbol{\tau}_w`$ over the wetted surface; pressure dominates on bluff bodies and friction on streamlined ones.
- Coefficients need a stated reference area and length, and unsteady loads need mean, fluctuating and peak values.
- $Re$, $St$, KC, $Fr$, $U_r$, $m^*$ and $Sc$ decide which physics matters and how model tests scale.
- The response is dynamic when the load has energy near a natural frequency; damping then controls it.
- Decide early between one-way loading, coefficient-based feedback and fully coupled simulation.

## Related Scripts

- [Surface Force Integration over Boundary Faces](../../../scripts/algorithms/fluid_loading_surface_force_integration/): integrates a surface pressure and wall-shear field over the flat faces of a body into a force and a moment, the same face sum a CFD code uses to report drag, lift and moment coefficients.
- [Morison Wave Force on a Vertical Pile](../../../scripts/algorithms/fluid_loading_morison_wave_force/): computes the wave force on a vertical pile by integrating the Morison equation over the depth with linear (Airy) wave kinematics.
- [Vortex-Induced Vibration with a Wake Oscillator](../../../scripts/algorithms/fluid_loading_viv_wake_oscillator/): models vortex-induced vibration of an elastically mounted cylinder with the coupled structure and van der Pol wake oscillators of Facchinetti, de Langre and Biolley (2004).
- [Partitioned Fluid–Structure Coupling and the Added-Mass Instability](../../../scripts/algorithms/fluid_loading_partitioned_fsi/): couples a structure solver and a fluid solver through their interface in the Dirichlet–Neumann way used by partitioned FSI codes, and shows that explicit coupling becomes unstable once the added mass of the fluid exceeds the structural mass, whatever the time step, while implicit coupling with Aitken relaxation converges to the monolithic solution.
- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.
- [Ship Hull in Water](../../../scripts/plots/ship_hull_in_water/): draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$.

## Exercises

**Exercise 1.** A vertical dam wall retains water to a depth of 15 m. Per metre of width, find the resultant hydrostatic force, its height above the base and the overturning moment about the base.

<details>
<summary>Answer</summary>

```math
F = \frac12\rho gH^2 = 0.5 \times 1000 \times 9.81 \times 15^2 = 1.10 \text{ MN per metre}
```

The resultant acts at $2H/3 = 10$ m below the surface, $H/3 = 5$ m above the base, so the overturning moment is $1.104 \times 5 = 5.52$ MN·m per metre.

</details>

**Exercise 2.** A flat road sign of 3 m × 2 m faces a 40 m/s wind ($\rho = 1.225$ kg/m³). With $C_D = 1.2$, find the dynamic pressure and the wind force.

<details>
<summary>Answer</summary>

```math
q = \frac12\rho U^2 = 0.5 \times 1.225 \times 40^2 = 980 \text{ Pa}, \qquad F = qC_DA = 980 \times 1.2 \times 6 = 7.06 \text{ kN}
```

</details>

**Exercise 3.** A platform member has natural frequency 1.8 Hz and damping ratio 0.02, and is loaded by a wave force at 0.2 Hz and by a vortex-shedding force at 1.6 Hz. Find the dynamic amplification of each. Which can be treated quasi-statically?

<details>
<summary>Answer</summary>

For the wave load $r = 0.111$ and $\mathrm{DAF} = 1/\sqrt{(1 - 0.0123)^2 + (0.0044)^2} = 1.01$, so it is quasi-static. For the shedding load $r = 0.889$ and

```math
\mathrm{DAF} = \frac{1}{\sqrt{(1 - 0.790)^2 + (2 \times 0.02 \times 0.889)^2}} = \frac{1}{\sqrt{0.0441 + 0.0013}} = 4.7
```

The shedding load is amplified almost five times, and as $f_s$ approaches $f_n$ lock-in can make it larger still.

</details>

**Exercise 4.** An offshore structure is tested in a wave basin at 1:50 scale with Froude scaling. What model wave period represents a 12 s prototype wave? What is the force scale factor if the model is tested in fresh water and the prototype is in seawater? By what factor is the model Reynolds number smaller, and why does it matter?

<details>
<summary>Answer</summary>

Time scales with $\sqrt{\lambda}$, so $T_m = 12/\sqrt{50} = 1.70$ s. Forces scale with $`(\rho_p/\rho_m)\lambda^3 = 1.025 \times 125\,000 = 128\,000`$. Velocity scales with $\sqrt{\lambda}$ and length with $\lambda$, so with the same viscosity $Re_p/Re_m = \lambda^{1.5} = 354$. Drag coefficients and separation depend on $Re$, so drag-dominated members are poorly represented in the model; roughened models or corrections are used.

</details>

**Exercise 5.** A steel riser of diameter 0.3 m and mass 150 kg/m (with contents) has a first natural frequency of 0.4 Hz in water and is exposed to a current of 0.6 m/s in seawater. Decide whether a one-way load calculation with a steady drag coefficient is adequate.

<details>
<summary>Answer</summary>

$U_r = 0.6/(0.4 \times 0.3) = 5.0$, right at $1/St$, the centre of the lock-in band. The mass ratio is $m^* = 150/(1025 \times \pi \times 0.09/4) = 2.07$, so the added mass is about half the structural mass and lock-in is wide. The riser will respond across the flow at an amplitude of the order of its diameter, and its motion will organise the wake. A one-way steady drag calculation misses the dominant load; a VIV assessment (empirical response model, wake-oscillator model or coupled CFD) is needed, and the in-line drag also increases because the vibrating riser has a larger effective $C_D$.

</details>

## References

- Blevins, R. D., *Flow-Induced Vibration*, 2nd ed., Van Nostrand Reinhold, 1990.
- Sumer, B. M., & Fredsøe, J., *Hydrodynamics Around Cylindrical Structures*, revised ed., World Scientific, 2006.
- Simiu, E., & Yeo, D., *Wind Effects on Structures: Modern Structural Design for Wind*, 4th ed., Wiley-Blackwell, 2019.
- Sarpkaya, T., & Isaacson, M., *Mechanics of Wave Forces on Offshore Structures*, Van Nostrand Reinhold, 1981.
- Faltinsen, O. M., *Sea Loads on Ships and Offshore Structures*, Cambridge University Press, 1990.
- Païdoussis, M. P., Price, S. J., & de Langre, E., *Fluid-Structure Interactions: Cross-Flow-Induced Instabilities*, Cambridge University Press, 2011.
- Rao, S. S., *Mechanical Vibrations*, 6th ed., Pearson, 2017.
