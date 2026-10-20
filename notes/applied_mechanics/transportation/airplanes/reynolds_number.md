# The Reynolds Number in Flight

The Reynolds number compares inertial and viscous forces in a flow. For a wing it decides how thick the boundary layer is relative to the chord, whether that boundary layer is laminar or turbulent, where it separates and therefore how much skin-friction drag the wing pays and how much lift it can reach before stalling. Flyers span six orders of magnitude in Reynolds number, from about $10^2$ for a fruit fly to $3 \times 10^7$ for an airliner wing, which is why their wings look so different. This note defines the Reynolds number, computes it for typical flyers, describes its effect on transition, drag and maximum lift, and explains why matching it is the central difficulty of wind-tunnel testing and a central requirement of CFD meshes. The general theory of dimensionless groups is in [Dimensional Analysis and Dimensionless Numbers](../../../fluid_mechanics/dimensions.md).

## Problem Statement

Given a lifting surface of characteristic length $c$ (the mean chord, m) moving at speed $V$ (m/s) through air at altitude $h$, find

- the air properties $\rho$, $\mu$ and $\nu = \mu/\rho$ at that altitude, and the Reynolds number $Re = Vc/\nu$;
- the boundary-layer regime: the approximate transition location and whether laminar separation is likely;
- the effect on skin-friction drag and maximum lift coefficient;
- for a scale model, the test conditions that reproduce the Reynolds number of the full-size aircraft, and what can be done when they cannot be reached.

The flow is assumed steady, incompressible unless the Mach number exceeds about 0.3, with smooth surfaces unless stated. The governing equations are the incompressible Navier–Stokes equations, which in dimensionless form with $\mathbf{u}^\star = \mathbf{u}/V$, $\mathbf{x}^\star = \mathbf{x}/c$, $p^\star = p/(\rho V^2)$ contain the Reynolds number as their only parameter:

```math
\frac{\partial \mathbf{u}^\star}{\partial t^\star} + (\mathbf{u}^\star\cdot\nabla^\star)\mathbf{u}^\star = -\nabla^\star p^\star + \frac{1}{Re}\nabla^{\star 2}\mathbf{u}^\star,
\qquad
\nabla^\star\cdot\mathbf{u}^\star = 0
```

Two geometrically similar bodies at the same $Re$ (and $M$, if compressibility matters) therefore have the same force coefficients.

## Definition and Physical Meaning

$$
Re = \frac{\rho V c}{\mu} = \frac{Vc}{\nu}
$$

with $\rho$ the density (kg/m³), $\mu$ the dynamic viscosity (Pa s) and $\nu$ the kinematic viscosity (m²/s). The ratio of a typical inertial force per unit volume, $\rho V^2/c$, to a typical viscous one, $\mu V/c^2$, is $Re$. A large Reynolds number does not mean that viscosity is unimportant everywhere: it means that viscous effects are confined to thin layers next to the surface and in the wake. For a laminar flat plate the boundary-layer thickness is

$$
\frac{\delta}{x} \approx \frac{5}{\sqrt{Re_x}},
\qquad Re_x = \frac{Vx}{\nu}
$$

so at $Re_x = 5 \times 10^5$ the boundary layer is only 0.7% of the distance from the leading edge. The wing chord is the usual reference length for airfoils and wings; the fuselage length is used for bodies, and the local distance $x$ from the leading edge for boundary-layer development.

### Air Properties

Viscosity of air depends on temperature only (Sutherland's law, $`\mu = 1.716 \times 10^{-5}\,(T/273.15)^{3/2}\,(273.15 + 110.4)/(T + 110.4)`$ Pa s), while density falls with altitude. Kinematic viscosity therefore rises with altitude:

| Altitude (ISA) | $T$ (K) | $\rho$ (kg/m³) | $\mu$ (Pa s) | $\nu$ (m²/s) | $a$ (m/s) |
| --- | --- | --- | --- | --- | --- |
| 0 m | 288.15 | 1.225 | $1.789 \times 10^{-5}$ | $1.461 \times 10^{-5}$ | 340.3 |
| 3000 m | 268.65 | 0.909 | $1.694 \times 10^{-5}$ | $1.863 \times 10^{-5}$ | 328.6 |
| 5000 m | 255.65 | 0.736 | $1.628 \times 10^{-5}$ | $2.212 \times 10^{-5}$ | 320.5 |
| 11 000 m | 216.65 | 0.364 | $1.422 \times 10^{-5}$ | $3.906 \times 10^{-5}$ | 295.1 |

At 11 km the kinematic viscosity is 2.7 times its sea-level value, so an airliner's Reynolds number barely changes between take-off and cruise even though its speed triples.

## Typical Values

![Reynolds numbers of flyers and flat-plate skin friction](../../../../scripts/plots/airplane_reynolds_number_scale/airplane_reynolds_number_scale.png)

| Flyer | Chord (m) | Speed (m/s) | $Re_c$ |
| --- | --- | --- | --- |
| Fruit fly (wing speed) | 0.0008 | 1.5–3 | 80–160 |
| Honeybee (wing speed) | 0.003 | 5–7 | 1000–1400 |
| Hummingbird | 0.012 | 5–10 | 4000–8000 |
| Sparrow | 0.05 | 8–12 | $3$–$`4 \times 10^4`$ |
| Pigeon | 0.10 | 10–20 | $0.7$–$`1.4 \times 10^5`$ |
| Model glider | 0.20 | 8–15 | $1$–$`2 \times 10^5`$ |
| Albatross | 0.20 | 10–25 | $1.4$–$`3.4 \times 10^5`$ |
| Sailplane | 0.65 | 25–60 | $1.1$–$`2.7 \times 10^6`$ |
| Light aircraft | 1.5 | 26–60 | $2.7$–$`6.2 \times 10^6`$ |
| Airliner, cruise at 11 km | 5.0 | 220–250 | $2.8$–$`3.2 \times 10^7`$ |

The values use typical chords and speeds rather than data for particular species or types. Panel (a) of the figure places all fourteen flyers of the script on one axis; birds, model aircraft and small UAVs fall in the shaded band where laminar separation and transition dominate airfoil behaviour.

## Effect on the Boundary Layer and Transition

On a smooth flat plate in a quiet free stream the boundary layer becomes turbulent at about $Re_{x,cr} = 5 \times 10^5$; in very quiet facilities it can stay laminar to $3 \times 10^6$ and with strong free-stream turbulence it may go turbulent below $10^5$. On an airfoil the pressure gradient matters as much as $Re$: a favourable gradient (accelerating flow over the front) delays transition, which is how laminar-flow sections work, and the adverse gradient behind the suction peak promotes it. Roughness, insect debris, rain and engine noise all move transition forward.

The Reynolds number decides which of three regimes a wing works in:

| $Re_c$ | Boundary layer | Consequences |
| --- | --- | --- |
| below about $5 \times 10^4$ | laminar; separates behind the suction peak and often does not reattach | low $c_l/c_d$; thin, sharp-nosed, highly cambered sections (insect wings, small birds) work best |
| about $5 \times 10^4$ to $10^6$ | laminar separation followed by turbulent reattachment, forming a separation bubble | drag and lift curve sensitive to $Re$, turbulence and surface finish; special low-$`Re`$ sections and turbulators |
| above about $10^6$ | transition ahead of separation; turbulent over much of the chord | lower drag coefficients, higher $c_{l,max}$, results change slowly with $Re$ |

## Effect on Drag and Maximum Lift

Skin friction, the dominant part of the profile drag of a streamlined section, depends on $Re$ and on the state of the boundary layer. For a flat plate of length $L$ the mean skin-friction coefficients are

```math
C_{f,lam} = \frac{1.328}{\sqrt{Re_L}},
\qquad
C_{f,turb} = \frac{0.074}{Re_L^{1/5}},
\qquad
C_{f,trans} = \frac{0.074}{Re_L^{1/5}} - \frac{1742}{Re_L}
```

the last for transition at $Re_x = 5 \times 10^5$. Panel (b) of the figure plots them. At $Re = 6 \times 10^6$, a light-aircraft wing, a fully laminar plate would have $C_f = 0.00054$, a fully turbulent one 0.0033 and a plate with natural transition 0.0030: transition alone multiplies the friction by 5.5, which is the prize sought by laminar-flow sections. At $Re = 3 \times 10^7$ the turbulent value falls to 0.0024. A thin airfoil has a profile drag coefficient of roughly twice the plate value (two surfaces) plus 10–30% form drag for its thickness, so low-$`Re`$ wings pay much higher drag coefficients.

The maximum lift coefficient rises with Reynolds number, because a thinner and more energetic turbulent boundary layer survives a stronger adverse pressure gradient before separating. The rise is large in the transitional range and slows above a few million. Wind-tunnel data at low $Re$ are therefore conservative for $c_{l,max}$ and pessimistic for drag.

For CFD the Reynolds number fixes the near-wall mesh: the first cell height for a wall-resolved RANS mesh ($y^+ \approx 1$) scales roughly as $`c\,Re^{-0.9}`$, so a $Re = 3 \times 10^7$ wing needs first cells of the order of microns on a 5 m chord.

## Reynolds and Mach Numbers in Wind-Tunnel Tests

Force coefficients measured on a model transfer to the aircraft only if the Reynolds number and, above $M \approx 0.3$, the Mach number $M = V/a$ match. With a model scaled by $1/n$ in the same gas at the same temperature, matching $Re$ needs the speed multiplied by $n$, which soon makes the flow supersonic (Exercise 4). Since $Re = \rho Vc/\mu$ and $M = V/a$ cannot both be held with a smaller $c$ in the same gas, facilities change the gas instead:

- pressurized tunnels raise $\rho$ at constant $\mu$ and $a$;
- cryogenic tunnels, such as NASA's National Transonic Facility and the European Transonic Windtunnel, cool nitrogen to well below 150 K, which raises $\rho$, lowers $\mu$ and lowers $a$, so the same Mach number comes with a much higher Reynolds number;
- otherwise, tests run at the reachable Reynolds number with the boundary layer tripped to turbulence at the expected full-scale transition location, and the results are extrapolated to flight Reynolds numbers with CFD and empirical corrections.

## Key Takeaways

- $Re = Vc/\nu$ is the only parameter of the incompressible flow equations; same $Re$ and geometry give the same coefficients.
- Kinematic viscosity rises with altitude, by a factor of 2.7 at 11 km.
- Flyers range from $Re \approx 10^2$ (insects) through $10^5$ (birds, models) to $3 \times 10^7$ (airliners); the band $5 \times 10^4$–$`10^6`$ is dominated by laminar separation bubbles.
- Turbulent skin friction is several times laminar friction at the same $Re$; both fall with $Re$.
- $c_{l,max}$ rises with $Re$; low-$`Re`$ test data are pessimistic for drag and conservative for maximum lift.
- Matching $Re$ and $M$ in a wind tunnel requires changing the gas properties (pressure, cryogenic temperature) or extrapolating with CFD.

## Related Scripts

- [Reynolds Numbers of Flyers](../../../../scripts/plots/airplane_reynolds_number_scale/): computes the chord Reynolds number $Re_c = Vc/\nu$ of fourteen flyers, from a fruit fly to an airliner at cruise, and draws them on one logarithmic axis next to the flat-plate skin-friction laws for laminar, turbulent and transitional boundary layers.
- [Laminar vs Turbulent Pipe Flow](../../../../scripts/plots/laminar_vs_turbulent_pipe/): plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is.

## Exercises

**Exercise 1.** An airliner cruises at 230 m/s at 11 km altitude, where $\rho = 0.364$ kg/m³, $T = 216.65$ K and $\mu = 1.42 \times 10^{-5}$ Pa s. Its mean wing chord is 5 m. Find the Reynolds number and the Mach number ($\gamma = 1.4$, $R = 287$ J/(kg K)).

<details>
<summary>Answer</summary>

```math
Re = \frac{0.364 \times 230 \times 5}{1.42 \times 10^{-5}} = 2.9 \times 10^7
```

```math
a = \sqrt{\gamma RT} = \sqrt{1.4 \times 287 \times 216.65} = 295 \text{ m/s},
\qquad
M = \frac{230}{295} = 0.78
```

The boundary layer is turbulent over most of the wing, and the flow is in the lower transonic regime, where the wing sections must be designed to keep shocks weak.

</details>

**Exercise 2.** A bird with a 0.10 m wing chord flies at 10 m/s at sea level ($\rho = 1.225$ kg/m³, $\mu = 1.79 \times 10^{-5}$ Pa s). Find its Reynolds number and compare it with the airliner of Exercise 1.

<details>
<summary>Answer</summary>

```math
Re = \frac{1.225 \times 10 \times 0.10}{1.79 \times 10^{-5}} = 6.8 \times 10^4
```

This is about 430 times smaller than the airliner's. At this Reynolds number the boundary layer is largely laminar and prone to laminar separation, so bird and small-drone wings use thin, highly cambered sections rather than scaled-down airliner sections.

</details>

**Exercise 3.** Below what airspeed can sea-level air ($T = 288.15$ K) be treated as incompressible, taking $M = 0.3$ as the limit? Is a light aircraft cruising at 60 m/s in that regime?

<details>
<summary>Answer</summary>

$a = \sqrt{1.4 \times 287 \times 288.15} = 340$ m/s, so $M = 0.3$ corresponds to 102 m/s.

At 60 m/s, $M = 0.18$, well inside the incompressible regime: the largest density change, at a stagnation point, is about $`M^2/2 = 1.6\%`$.

</details>

**Exercise 4.** A 1:10 scale model of a wing with a 2 m chord is tested in a sea-level wind tunnel. The full-size aircraft flies at 70 m/s at sea level. What tunnel speed matches the Reynolds number, and why is this impractical? By what factor would the density have to rise in a pressurized tunnel running at the full-scale speed?

<details>
<summary>Answer</summary>

Matching $Re = \rho Vc/\mu$ with $c$ ten times smaller requires $V$ ten times larger: 700 m/s, or $M \approx 2.1$. The model would see supersonic flow with shocks that the aircraft never experiences.

At 70 m/s the density must instead rise tenfold, i.e. a tunnel pressurized to about 10 atm at the same temperature, which keeps both $Re$ and $M$ equal to full scale. Pressurized and cryogenic tunnels exist for exactly this reason.

</details>

**Exercise 5.** On a smooth flat plate, transition occurs at about $Re_x = 5 \times 10^5$. Estimate how far from the leading edge transition occurs on a light-aircraft wing at 60 m/s at sea level ($\nu = 1.46 \times 10^{-5}$ m²/s), and the boundary-layer thickness there. Why is the answer only indicative?

<details>
<summary>Answer</summary>

```math
x_{tr} = \frac{Re_{x}\,\nu}{V} = \frac{5 \times 10^5 \times 1.46 \times 10^{-5}}{60} = 0.12 \text{ m},
\qquad
\delta \approx \frac{5x_{tr}}{\sqrt{Re_x}} = 0.85 \text{ mm}
```

That is only 8% of a 1.5 m chord. On a real wing the transition location depends strongly on the pressure gradient (a favourable gradient delays it, which is how laminar-flow airfoils reach 40–60% chord), on surface roughness, insect debris and free-stream turbulence.

</details>

## References

- Anderson, J. D., Jr., *Fundamentals of Aerodynamics*, 6th ed., McGraw-Hill Education, 2017.
- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill Education, 2016.
- Schlichting, H., and Gersten, K., *Boundary-Layer Theory*, 9th ed., Springer, 2017.
- Lissaman, P. B. S., "Low-Reynolds-number airfoils", *Annual Review of Fluid Mechanics*, vol. 15, pp. 223–239, 1983.
- Mueller, T. J., and DeLaurier, J. D., "Aerodynamics of small vehicles", *Annual Review of Fluid Mechanics*, vol. 35, pp. 89–111, 2003.
- Barlow, J. B., Rae, W. H., Jr., and Pope, A., *Low-Speed Wind Tunnel Testing*, 3rd ed., Wiley, 1999.
- NOAA, NASA, and USAF, *U.S. Standard Atmosphere, 1976*, U.S. Government Printing Office, 1976.
