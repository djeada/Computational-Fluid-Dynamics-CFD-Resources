# Wind Loading on Structures

Wind is a design action for almost every structure above ground, and the governing one for tall buildings, towers, chimneys, long-span bridges, roofs and cladding. The load depends on how the mean wind speed grows with height over the upstream terrain, on the turbulence that makes the load fluctuate, on the shape of the structure through its pressure coefficients, and on the dynamics of the structure, which can amplify the fluctuations along the wind or respond to vortex shedding across it. This note follows that chain from the atmospheric boundary layer to the design pressure and the along-wind and across-wind response. Design codes package the same steps into tabulated factors; their specific values are not repeated here.

## Problem Statement

Given a structure of height $H$ and breadth $B$ with known shape, natural frequencies $f_j$, modal masses and damping ratios $\zeta_j$, and a site characterised by its terrain roughness and a reference mean wind speed, find:

1. the mean wind speed $U(z)$ and the turbulence intensity $I_u(z)$ over the height of the structure;
2. the mean and peak pressures on its surfaces, for the design of cladding and roof fixings;
3. the overall forces and moments (base shear, overturning moment), including dynamic amplification of the turbulent fluctuations along the wind;
4. the across-wind response to vortex shedding, and whether an aeroelastic instability (galloping, flutter) can occur below the design wind speed.

The structure is linear elastic with small deflections, and the flow is treated as quasi-steady unless stated: the pressure at any instant is $`p = C_p\,\tfrac12\rho U(t)^2`$ with the instantaneous speed. The structural response of each mode obeys

$$
m_j\ddot{q}_j + 2m_j\zeta_j\omega_j\dot{q}_j + m_j\omega_j^2 q_j = Q_j(t)
$$

with the generalised wind force $Q_j$ obtained by integrating the pressure field against the mode shape.

## The Atmospheric Boundary Layer

### Mean Wind Profiles

Friction with the ground slows the wind near the surface over a boundary layer several hundred metres deep. In strong winds the atmosphere is close to neutrally stratified, and the mean speed in the lower part follows the logarithmic law

$$
U(z) = \frac{u_*}{\kappa}\ln \frac{z}{z_0}
$$

where $u_*$ is the friction velocity (m/s), $\kappa \approx 0.41$ the von Kármán constant and $z_0$ the aerodynamic roughness length (m), which characterises the upstream terrain. Over dense, tall buildings the profile is shifted up by a zero-plane displacement $d$, $\ln((z - d)/z_0)$. The same law describes the inner region of any turbulent boundary layer ([Boundary Layers](../../fluid_mechanics/viscous_flow/boundary_layers.md)). The older empirical power law

$$
U(z) = U_{\mathrm{ref}}\left(\frac{z}{z_{\mathrm{ref}}}\right)^\alpha
$$

fits the log law over a limited height range. Equating the slopes $dU/dz$ of the two laws at a height $z_m$ gives $\alpha \approx 1/\ln(z_m/z_0)$, so the exponent rises with roughness.

| Terrain | $z_0$ (m) | Least-squares $\alpha$ over 10–200 m |
| --- | --- | --- |
| Open sea | 0.0002 | 0.081 |
| Open country, grassland | 0.03 | 0.138 |
| Suburbs, forest | 0.3 | 0.204 |
| City centre | 1.0 | 0.272 |

The figure assumes the same mean wind at 300 m over all four terrains, with 25 m/s at 10 m over open country, and shows the resulting log profiles, the power-law fits and the velocity pressure.

![Log-law and fitted power-law wind profiles, mean velocity pressure and peak velocity pressure against height for four terrains](../../../scripts/plots/fluid_loading_wind_profile/fluid_loading_wind_profile.png)

The rough terrain reduces the 10 m speed from 30.2 m/s over the sea to 16.0 m/s in the city centre, and the mean base shear on a 100 m × 30 m face from 2.73 to 1.61 MN. Panel (c) shows that the extra turbulence of rough terrain almost cancels that reduction in the peak pressure.

### Turbulence and Gusts

The wind speed at a point is $U + u'(t)$, with a longitudinal standard deviation $\sigma_u \approx 2.5u_*$ in neutral flow, so the turbulence intensity is

$$
I_u = \frac{\sigma_u}{U} \approx \frac{1}{\ln(z/z_0)}
$$

which is about 0.17 at 10 m over open country and more than 0.4 in a city centre. The peak gust over an averaging time of a few seconds is $\hat{U} = U(1 + g_uI_u)$, with a peak factor $g_u \approx 3$–3.5. Wind speeds must therefore always be quoted with their averaging time: a 3-second gust speed is about 1.4–1.5 times the 10-minute mean over open country, which is why codes that specify gust speeds (ASCE 7 in the United States) and codes that specify 10-minute means (EN 1991-1-4 in Europe) quote very different numbers for the same climate. The energy of $u'$ is distributed over frequency by a spectrum $S_u(f)$; a widely used form is von Kármán's

```math
\frac{fS_u(f)}{\sigma_u^2} = \frac{4\,fL_u/U}{\left[1 + 70.8\,(fL_u/U)^2\right]^{5/6}}
```

with an integral length scale $L_u$ of order 100 m.

## Design Wind Pressure

The velocity pressure

$$
q(z) = \tfrac12\rho U(z)^2
$$

with $\rho = 1.225$ kg/m³ is $q = 0.613U^2$ Pa for $U$ in m/s: 0.38 kPa at 25 m/s and 1.53 kPa at 50 m/s. For cladding the gust matters, and to first order in $I_u$ the peak velocity pressure is $\hat{q} = q(1 + 2g_uI_u)$. The pressure on a surface is $p = C_p q_{\mathrm{ref}}$, where the pressure coefficient $C_p$ comes from wind-tunnel tests, CFD or code tables and depends on the shape, the wind direction and the position on the surface.

| Surface of a rectangular building | Typical mean $C_p$ |
| --- | --- |
| Windward wall | $+0.7$ to $+0.8$ |
| Leeward wall | $-0.3$ to $-0.5$ |
| Side walls | $-0.6$ to $-0.7$ |
| Flat roof near the windward edge | $-1.0$ to $-2.0$ |
| Flat roof, central zone | $-0.4$ to $-0.7$ |

Suction dominates: only the windward wall is pushed, and the largest loads are uplift at roof edges and corners, where the flow separates and conical vortices form. Buildings are not sealed, so the net load on a panel is

$$
p_{\mathrm{net}} = \left(C_{p,\mathrm{ext}} - C_{p,\mathrm{int}}\right)q_{\mathrm{ref}}
$$

with an internal coefficient that depends on where the openings are, typically between $-0.3$ and $+0.2$ for evenly distributed openings and larger in magnitude when one wall has a dominant opening. Each panel is designed for the worst combination of the two signs.

## Along-Wind Response

The mean drag on a building of breadth $B$ is the integral of the mean pressure over the height:

```math
\bar{F} = \int_0^H C_D B\, q(z)\, dz
```

The fluctuating part has two components with different physics. The background response is the quasi-static response to gusts slower than the structure's natural frequency; it is smaller than the point gust suggests because gusts are not correlated over the whole face. The resonant response is the dynamic amplification of gust energy near $f_1$. For a linear quasi-steady load the force fluctuation is $F' \approx 2\bar{F}u'/U$, and Davenport's gust factor relates the peak response to the mean:

```math
G = \frac{\hat{x}}{\bar{x}} = 1 + 2gI_u \sqrt{B_g + R},
\qquad R = \frac{\pi}{4\zeta}\,\chi^2(f_1)\, \frac{f_1S_u(f_1)}{\sigma_u^2}
```

Here $g$ is a peak factor (3 to 4), $B_g \le 1$ the background factor, which falls as the structure grows relative to the gust size, and $R$ the resonant factor. In $R$, $\chi^2(f_1) \le 1$ is the aerodynamic admittance, the reduction of the force spectrum because small gusts are not correlated over the structure at frequency $f_1$, and $\zeta$ the total damping ratio, structural plus aerodynamic. The resonant term varies as $1/\zeta$, so light damping matters, and it matters most for flexible structures with $f_1$ below about 1 Hz. The design load is $G\bar{F}$ distributed like the mean load; codes write the same product with their own factors.

### Worked Example: Gust Factor of a Tall Building

A 180 m building has $f_1 = 0.2$ Hz and $\zeta = 0.015$. At its top the mean speed is $U = 35$ m/s, with $I_u = 0.15$ and $L_u = 150$ m; take $B_g = 0.6$, $\chi^2(f_1) = 0.1$ and $g = 3.4$. The reduced frequency is $f_1L_u/U = 0.857$, so the von Kármán spectrum gives $f_1S_u/\sigma_u^2 = 0.125$ and

$$
R = \frac{\pi}{4 \times 0.015} \times 0.1 \times 0.125 = 0.66,
\qquad G = 1 + 2 \times 3.4 \times 0.15 \sqrt{0.6 + 0.66} = 2.14
$$

The peak along-wind response is 2.1 times the mean, and the resonant part contributes about half the variance. Halving the damping to 0.0075 would double $R$ and raise $G$ to 2.4.

## Across-Wind Response

### Vortex Shedding

Wind past a bluff section sheds vortices alternately from each side at the frequency

```math
f_s = \frac{St\,U}{D}
```

where $D$ is the across-wind dimension and $St$ the Strouhal number: about 0.2 for a circular cylinder at subcritical Reynolds numbers and about 0.12 for a square section. The alternating vortices produce an across-wind force at $f_s$ and a smaller along-wind force at $2f_s$. When $f_s$ approaches a natural frequency the shedding locks onto the structural motion and large across-wind oscillations can build up, starting at the critical speed

$$
U_{cr} = \frac{f_nD}{St}
$$

The amplitude reached during lock-in falls with the Scruton number $Sc = 2m\delta/(\rho D^2)$, where $m$ is the mass per unit length and $\delta \approx 2\pi\zeta$ the logarithmic decrement. Structures in air with $Sc$ below about 10 can reach amplitudes of several per cent of $D$ or more. [Flow-Induced Vibrations](./flow_induced_vibrations.md) treats lock-in, the amplitude response and the wake-oscillator model, and the simulations listed at the end of this note show the vortex street behind a cylinder.

For tall buildings, across-wind accelerations from shedding and wake turbulence often govern occupant comfort rather than strength, and typical criteria limit peak accelerations to a few tens of milli-g. Remedies are aerodynamic (tapering, setbacks, chamfered or recessed corners, openings through the top floors), which reduce the coherence of shedding along the height, and supplementary damping such as tuned mass dampers.

### Galloping

Sections whose lift force changes sign steeply with the angle of attack, such as square, rectangular, D-shaped and iced sections, can gallop: a transverse velocity $\dot{y}$ changes the relative angle of attack by $-\dot{y}/U$, and if the resulting force acts in the direction of motion it feeds energy into the oscillation. Quasi-steady theory gives Den Hartog's necessary condition and the onset speed

$$
\left. \frac{dC_L}{d\alpha}\right|_0 + C_D < 0,
\qquad U_g = \frac{4m\zeta\omega_n}{\rho D\left|dC_L/d\alpha + C_D\right|}
$$

A circular cylinder cannot gallop, because by symmetry $dC_L/d\alpha = 0$ and $C_D > 0$. Unlike vortex-induced vibration, galloping is not confined to a band of speeds: above $U_g$ the amplitude keeps growing with wind speed until nonlinear aerodynamics limit it.

## Worked Examples

### Base Shear of a Low-Rise Building

A building 20 m wide and 10 m high has $C_D = 1.3$ and a design mean speed at roof height of 45 m/s. Taking the roof-height velocity pressure over the whole height,

$$
q_H = \tfrac12 \times 1.225 \times 45^2 = 1.24 \text{ kPa},
\qquad F = q_HC_DBH = 1240 \times 1.3 \times 20 \times 10 = 322 \text{ kN}
$$

Using the roof-height pressure over the whole height is conservative, since the speed is lower near the ground.

### Lock-In Check of a Tall Building

A square tower 180 m tall with $D = 30$ m has $f_1 = 0.20$ Hz and $St = 0.12$. Lock-in starts at $U_{cr} = 0.20 \times 30/0.12 = 50$ m/s. If the design speed at the top is 55 m/s, the shedding frequency $f_s = 0.12 \times 55/30 = 0.22$ Hz sweeps through $f_1$ within the design range, and an across-wind analysis or wind-tunnel test is required.

### Cladding Pressures

With $q_{\mathrm{ref}} = 1.5$ kPa, a windward wall with $C_{p,\mathrm{ext}} = +0.8$ and a roof corner with $C_{p,\mathrm{ext}} = -2.0$, and an internal coefficient of $+0.3$:

$$
p_{\mathrm{wall}} = (0.8 - 0.3) \times 1.5 = 0.75 \text{ kPa},
\qquad p_{\mathrm{corner}} = (-2.0 - 0.3) \times 1.5 = -3.45 \text{ kPa}
$$

The corner uplift is more than four times the wall pressure and governs the fixings.

## Wind Loads from CFD

CFD is used for wind loads on complex buildings and for pedestrian wind comfort, as a complement to boundary-layer wind tunnels. Three points decide whether the result is usable:

1. The inflow must reproduce the target mean profile and turbulence of the atmospheric boundary layer, and the profile must survive the empty upstream part of the domain without decaying.
2. Mean pressures on windward faces are predicted fairly well by steady RANS, but suctions in separated regions and all peak pressures depend on unsteady, separated flow, which needs large-eddy simulation or hybrid RANS–LES ([Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md)).
3. Forces follow from integrating the surface pressure ([Pressure Forces on Structures](./pressure_forces.md)), and peak values need records long enough for extreme-value statistics, typically the equivalent of several 10-minute full-scale periods.

## Key Takeaways

- The mean wind follows the log law with a roughness length $z_0$; the power-law exponent is a fit that rises with roughness.
- Turbulence intensity is about $1/\ln(z/z_0)$, so rough terrain lowers the mean pressure but raises the gust content.
- Pressures are $C_pq$ with $q = \tfrac12\rho U^2$; suction dominates, and roof edges and corners carry the largest cladding loads.
- The along-wind peak is the mean times a gust factor with background and resonant parts; the resonant part scales as $1/\zeta$.
- Across-wind, check lock-in at $U_{cr} = f_nD/St$ and the Scruton number, and check sharp-edged sections for galloping.

## Related Scripts

- [Wind Profiles and Velocity Pressure over Four Terrains](../../../scripts/plots/fluid_loading_wind_profile/): plots log-law mean wind profiles over open sea, open country, suburbs and a city centre, the power-law exponent that best fits each profile, and the resulting mean and peak velocity pressure with height.
- [Vortex-Induced Vibration with a Wake Oscillator](../../../scripts/algorithms/fluid_loading_viv_wake_oscillator/): models vortex-induced vibration of an elastically mounted cylinder with the coupled structure and van der Pol wake oscillators of Facchinetti, de Langre and Biolley (2004).
- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.
- [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](../../../scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/): compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model.

## Exercises

**Exercise 1.** The mean wind speed at 10 m is 30 m/s over suburban terrain ($\alpha = 0.22$). Use the power law to find the speed at 100 m and the ratio of velocity pressures at the two heights.

<details>
<summary>Answer</summary>

```math
U(100) = 30 \times 10^{0.22} = 49.8 \text{ m/s}, \qquad \frac{q(100)}{q(10)} = \left(10^{0.22}\right)^2 = 2.75
```

</details>

**Exercise 2.** Repeat Exercise 1 with the logarithmic law and $z_0 = 0.3$ m: find the friction velocity and $U(100)$. What turbulence intensity does the log law imply at 10 m?

<details>
<summary>Answer</summary>

```math
u_* = \frac{\kappa U(10)}{\ln(10/0.3)} = \frac{0.41 \times 30}{3.51} = 3.51 \text{ m/s}
```

```math
U(100) = \frac{3.51}{0.41}\ln\frac{100}{0.3} = 8.55 \times 5.81 = 49.7 \text{ m/s}
```

This is almost the power-law value, as expected when the exponent matches the terrain. At 10 m, $I_u \approx 1/\ln(10/0.3) = 0.285$.

</details>

**Exercise 3.** For the cladding example ($q_{\mathrm{ref}} = 1.5$ kPa), the internal coefficient may be $+0.3$ or $-0.3$ depending on where the openings are. Find the governing net pressures on the windward wall ($C_{p,\mathrm{ext}} = +0.8$) and at the roof corner ($C_{p,\mathrm{ext}} = -2.0$).

<details>
<summary>Answer</summary>

Windward wall: $(0.8 - 0.3) \times 1.5 = 0.75$ kPa or $(0.8 + 0.3) \times 1.5 = 1.65$ kPa. Internal suction governs, giving 1.65 kPa inward.

Roof corner: $(-2.0 - 0.3) \times 1.5 = -3.45$ kPa or $(-2.0 + 0.3) \times 1.5 = -2.55$ kPa. Internal pressure governs, giving 3.45 kPa of uplift.

</details>

**Exercise 4.** A circular steel chimney 4 m in diameter has natural frequencies of 0.8 Hz and 5 Hz in its first two modes. With $St = 0.2$, find the critical vortex-shedding speed of each mode. The design wind speed at the top is 35 m/s; which mode is a concern, and what would you do about it?

<details>
<summary>Answer</summary>

$U_{cr,1} = 0.8 \times 4/0.2 = 16$ m/s and $U_{cr,2} = 5 \times 4/0.2 = 100$ m/s.

Mode 1 locks in at 16 m/s, a speed that occurs often, so both fatigue and serviceability are concerns. Mode 2 would need 100 m/s. For mode 1: helical strakes on the upper third of the height, a tuned mass damper, or added damping to raise the Scruton number.

</details>

**Exercise 5.** A building 100 m tall and 30 m wide has $C_D = 1.3$, and the mean wind follows $U(z) = 30(z/10)^{0.22}$ m/s with $\rho = 1.225$ kg/m³. Derive the mean base shear and base moment by integrating over the height, evaluate them, and find the height of the resultant. If the gust factor is 2.1, what is the design base moment?

<details>
<summary>Answer</summary>

With $q(z) = \tfrac12\rho U_{\mathrm{ref}}^2(z/z_{\mathrm{ref}})^{2\alpha}$,

```math
F = \int_0^H q\,C_DB\,dz = \frac{\tfrac12\rho U_{\mathrm{ref}}^2C_DB\,H^{2\alpha+1}}{(2\alpha+1)z_{\mathrm{ref}}^{2\alpha}} = 4.11 \text{ MN}
```

```math
M = \int_0^H z\,q\,C_DB\,dz = \frac{\tfrac12\rho U_{\mathrm{ref}}^2C_DB\,H^{2\alpha+2}}{(2\alpha+2)z_{\mathrm{ref}}^{2\alpha}} = 243 \text{ MN m}
```

The resultant acts at $M/F = (2\alpha+1)H/(2\alpha+2) = 59.0$ m, above mid-height because the pressure grows with height. The design base moment is $2.1 \times 243 = 510$ MN·m.

</details>

## References

- Simiu, E., & Yeo, D., *Wind Effects on Structures: Modern Structural Design for Wind*, 4th ed., Wiley-Blackwell, 2019.
- Holmes, J. D., *Wind Loading of Structures*, 3rd ed., CRC Press, 2015.
- Dyrbye, C., & Hansen, S. O., *Wind Loads on Structures*, Wiley, 1997.
- Davenport, A. G., "The application of statistical concepts to the wind loading of structures," *Proceedings of the Institution of Civil Engineers*, 19(4), 449–472, 1961.
- Blevins, R. D., *Flow-Induced Vibration*, 2nd ed., Van Nostrand Reinhold, 1990.
- Den Hartog, J. P., *Mechanical Vibrations*, 4th ed., McGraw-Hill, 1956.
- CEN, *EN 1991-1-4: Eurocode 1: Actions on Structures, Part 1-4: General Actions, Wind Actions*, European Committee for Standardization, 2005.
- American Society of Civil Engineers, *Minimum Design Loads and Associated Criteria for Buildings and Other Structures*, ASCE/SEI 7-22, ASCE, 2022.
