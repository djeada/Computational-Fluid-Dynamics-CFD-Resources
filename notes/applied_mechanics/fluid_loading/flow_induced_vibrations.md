# Flow-Induced Vibrations

A flow can make a structure vibrate in two different ways. It can force it, through turbulence in the oncoming flow (buffeting) or through the periodic wake of the body itself (vortex shedding); or the motion of the structure can change the fluid force so that the flow feeds energy into the motion, which is a self-excited instability (galloping, flutter, fluid-elastic instability). Vortex-induced vibration lies in between: shedding starts as a forced excitation but locks onto the structural motion. These mechanisms cause fatigue of chimneys, cables, risers and heat-exchanger tubes and, in the case of the Tacoma Narrows bridge in 1940, collapse. This note gives the physics and the design checks for each, and connects them to the cylinder-flow simulations in the repository and to coupled flow–structure computation.

## Problem Statement

Given a slender elastic structure of cross-section dimension $D$, mass per unit length $m$, natural frequencies $f_n$ and damping ratios $\zeta$, in a steady flow of speed $U$ and density $\rho$ (wind, current or internal flow), find which flow-induced vibration mechanisms can occur within the operating range of $U$, the flow speeds at which they start, the response amplitude, and the measures that keep the response acceptable. Each mode is modelled as a single-degree-of-freedom oscillator per unit length,

$$
m\ddot{y} + 2m\zeta\omega_n\dot{y} + m\omega_n^2y = F_y(t, y, \dot{y}, \ddot{y})
$$

with $\omega_n = 2\pi f_n$. The mechanisms differ in how the fluid force $F_y$ depends on time and on the motion. The governing dimensionless groups are the reduced velocity $U_r = U/(f_nD)$, the mass ratio $m^* = m/(\rho\pi D^2/4)$, the damping ratio, their product (the mass–damping parameter, or the Scruton number), and the Reynolds number.

| Mechanism | Force | Typical structures |
| --- | --- | --- |
| Buffeting | Forced by incident turbulence, $F_y(t)$ | Buildings, bridges, towers in gusty wind |
| Vortex-induced vibration | Periodic wake force that synchronises with the motion | Chimneys, cables, risers, pipelines, heat-exchanger tubes |
| Galloping | Self-excited, single degree of freedom, $F_y(\dot{y})$ | Iced conductors, square and rectangular towers, bridge decks |
| Wake galloping | Self-excited, a cylinder in the wake of another | Bundled conductors, tandem cylinders |
| Flutter | Self-excited, coupled bending and torsion | Wings, long-span bridge decks, turbine blades |
| Fluid-elastic instability | Self-excited, coupled motion of tubes in an array | Heat-exchanger and steam-generator tube bundles |

## Vortex-Induced Vibration

### Vortex Shedding and the Strouhal Number

Behind a bluff body the separated shear layers roll up alternately into a von Kármán vortex street, which can be seen in the [lattice Boltzmann cylinder flow](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/) simulation. Each shed vortex changes the circulation around the body, so the lift force alternates at the shedding frequency

```math
f_s = \frac{St\,U}{D}
```

and the drag fluctuates at $2f_s$. For a circular cylinder $St \approx 0.2$ over the subcritical range $300 < Re < 2 \times 10^5$; it becomes scattered, and shedding less coherent, in the critical and supercritical ranges where the boundary layer turns turbulent before separation, and recovers to about 0.25–0.3 at transcritical Reynolds numbers. Square sections give about 0.13 and a flat plate normal to the flow about 0.15. Because the Strouhal number depends on where the boundary layer separates, a CFD prediction of shedding on rounded bodies at high Reynolds number depends on the turbulence model and the near-wall resolution ([Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md)).

### Lock-In

On a fixed cylinder the shedding frequency rises linearly with $U$. On an elastically mounted cylinder, as $f_s$ approaches $f_n$ the motion organises the shedding: over a band of flow speeds the shedding frequency follows the structure instead of the Strouhal law, the lift becomes coherent along the span and the amplitude grows to a fraction of a diameter or more. In terms of reduced velocity, lock-in begins near $U_r \approx 1/St = 5$ and extends over roughly $4 \lesssim U_r \lesssim 8$ for a circular cylinder of moderate mass ratio. Unlike classical resonance, the force adapts to the motion, so the response is self-limiting.

The experiments reviewed by Williamson and Govardhan (2004) show that the response depends mainly on the combined mass–damping $(m^* + C_a)\zeta$. At low mass–damping, typical of structures in water, there is an initial branch, an upper branch reaching $A/D \approx 1$ and a lower branch at about $A/D \approx 0.6$, the band of synchronisation widens as $m^*$ falls, and the frequency in the lower branch exceeds $f_n$. At high mass–damping, typical of structures in air, there is a single narrow peak of smaller amplitude. Plotting the peak amplitude against mass–damping collapses data from many experiments onto one curve, the Griffin plot.

### A Wake-Oscillator Model

A minimal model that reproduces lock-in couples the structure equation to a van der Pol oscillator for the wake variable $q = 2C_L/C_{L0}$ (Facchinetti, de Langre and Biolley 2004). In time scaled with the Strouhal frequency and displacement scaled with $D$,

$$
\ddot{y} + \left(2\zeta\delta + \frac{\gamma}{\mu}\right)\dot{y} + \delta^2y = Mq,
\qquad \ddot{q} + \varepsilon\left(q^2 - 1\right)\dot{q} + q = A\ddot{y}
$$

where $`\delta = 1/(St\,U_r)`$ is the natural frequency relative to the Strouhal frequency, $\mu = (m^* + C_a)\pi/4$ the mass ratio including added mass, $\gamma$ a fluid damping parameter, and $M$, $\varepsilon$ and $A$ constants fitted to experiments. On its own the wake oscillates at the Strouhal frequency with $q = 2$; through the coupling term $A\ddot{y}$ the cylinder's acceleration can entrain it.

![Amplitude response, lock-in of the response frequency, and peak amplitude against mass-damping from the wake-oscillator model](../../../scripts/algorithms/fluid_loading_viv_wake_oscillator/fluid_loading_viv_wake_oscillator.png)

For $m^* = 20$ the response frequency in panel (b) leaves the Strouhal line and stays within 5% of $f_n$ for $4.4 \le U_r \le 6.0$, where the amplitude in panel (a) peaks at $A/D = 0.22$. For $m^* = 2$ the response band is wider and the frequency rises steadily through $f_n$ instead of locking onto it, as observed at low mass ratio. Panel (c) is the model's Griffin plot: the peak amplitude depends on $(m^* + C_a)\zeta$, and the two mass ratios fall on one curve. With the published constants the model's peak amplitudes are well below the measured upper branch, so it is a tool for understanding lock-in and for fast parametric studies of long risers, not for predicting amplitudes.

### Mass–Damping and the Scruton Number

The design parameter for VIV is the Scruton number

$$
Sc = \frac{2m\delta}{\rho D^2}
$$

with $\delta \approx 2\pi\zeta$ the logarithmic decrement; other definitions differ by constant factors ($\pi^2m^*\zeta$ is also common), so the definition must be checked before comparing with a threshold. In air, structures with $Sc$ above about 10–20 generally show only small VIV amplitudes, while in water $Sc$ is often below 1 and amplitudes of the order of a diameter are possible. The same structure has a Scruton number about 840 times smaller in water than in air, which is why VIV is a fatigue problem for most marine risers and only for light, lightly damped structures in air.

### Screening Procedure

1. Compute $f_n$ of the relevant modes, in the fluid (with added mass for water).
2. Compute the critical speed $U_{cr} = f_nD/St$ for each mode and compare with the range of flow speeds, including the variation of speed along the span (wind profile, sheared current).
3. If $U_{cr}$ lies inside the range, compute $Sc$ or $(m^* + C_a)\zeta$ and estimate the amplitude from experimental data or design rules.
4. Check the fatigue damage of the resulting stress cycles at the lock-in frequency, accumulated over the time the flow spends in the lock-in band.
5. If the response is unacceptable, change $f_n$, add damping or suppress the shedding.

## Galloping

Galloping is a single-degree-of-freedom instability of sections whose lift changes steeply with the angle of attack. A body moving across a steady flow with velocity $\dot{y}$ sees a relative wind at angle $\alpha = -\dot{y}/U$. With lift and drag coefficients $C_L(\alpha)$ and $C_D(\alpha)$, the quasi-steady force coefficient across the flow for small $\alpha$ is

$$
C_y \approx -
\left(\frac{dC_L}{d\alpha} + C_D\right)\alpha = \left(\frac{dC_L}{d\alpha} + C_D\right)
\frac{\dot{y}}{U}
$$

so that $F_y = \tfrac12\rho U^2DC_y$ is proportional to $\dot{y}$, a damping force. Moving it to the left-hand side of the equation of motion gives a total damping coefficient

$$
c_{\mathrm{tot}} = 2m\zeta\omega_n + \tfrac12\rho
UD\left(\frac{dC_L}{d\alpha} + C_D\right)
$$

which can become negative only if $dC_L/d\alpha + C_D < 0$ (Den Hartog's criterion). Galloping then starts when $c_{\mathrm{tot}} = 0$:

$$
U_g = \frac{4m\zeta\omega_n}{\rho D\left|dC_L/d\alpha + C_D\right|}
$$

A circular cylinder cannot gallop, because $dC_L/d\alpha = 0$. A square section has $dC_L/d\alpha + C_D \approx -2.7$ (measured in smooth flow), and ice or wet snow on a conductor can make an otherwise round section gallop. Quasi-steady theory requires the vortex-shedding frequency to be well above $f_n$, that is $U_r \gg 1/St$; when $U_g$ is close to the lock-in speed the two mechanisms interact. Above $U_g$ the amplitude grows with the flow speed, limited only by the nonlinearity of $C_y(\alpha)$, and galloping of iced transmission lines can reach several metres.

### Worked Example: Iced Conductor

A conductor with $D = 0.05$ m, $m = 2.5$ kg/m, $f_n = 1.0$ Hz and $\zeta = 0.005$ has, with its ice accretion, $dC_L/d\alpha = -3.0$ and $C_D = 1.2$. The Den Hartog parameter is $-1.8$, so galloping is possible, and

$$
U_g = \frac{4 \times 2.5 \times 0.005 \times 2\pi}{1.225 \times 0.05 \times 1.8} = 2.85
\text{ m/s}
$$

Galloping can start in a light breeze. Remedies are anti-galloping devices that detune or damp the motion, interphase spacers, and ice prevention.

## Wake Galloping and Buffeting

A cylinder in the wake of another, such as the leeward conductor of a bundle or the second of two chimneys, sees a velocity and angle of the flow that vary across the wake. Its lift and drag then depend on its position within the wake, and an orbiting, self-excited motion can develop at spacings of a few to about 20 diameters. The analysis is the galloping analysis with position-dependent coefficients measured in the wake.

Buffeting is the forced response to turbulence, in the oncoming flow or shed by upstream structures. With a quasi-steady force $F' = \tfrac12\rho U^2D(2C_Du'/U + C_L'w'/U)$, where $u'$ and $w'$ are the longitudinal and vertical turbulent velocities and $C_L' = dC_L/d\alpha$, the response spectrum is the force spectrum times the squared mechanical admittance, $S_y = |H(f)|^2S_F$. This is the basis of the gust factor in [Wind Loading on Structures](./wind_loading.md). Buffeting is not an instability, but it controls the fatigue of bridges and towers in everyday winds.

## Flutter

Flutter is the self-excited oscillation of a structure with two or more coupled degrees of freedom, classically the heave (bending) $h$ and pitch (torsion) $\alpha$ of a wing or bridge-deck section. The aerodynamic lift and moment depend on $h$, $\alpha$ and their rates, so the equations of the typical section,

$$
m\ddot{h} + S_\alpha\ddot{\alpha} + k_hh = -L(h, \alpha, \dot{h}, \dot{\alpha}),
\qquad S_\alpha\ddot{h} + I_\alpha\ddot{\alpha} +
k_\alpha\alpha = M_{ea}(h, \alpha, \dot{h}, \dot{\alpha})
$$

with static imbalance $S_\alpha$, form an eigenvalue problem whose frequencies and damping change with the flow speed. As $U$ rises, the two natural frequencies approach each other; at the flutter speed one coupled mode has zero total damping, and above it the oscillation grows. The aerodynamic forces are unsteady: Theodorsen's function $C(k)$ of the reduced frequency $k = \omega b/U$ ($b$ the semichord) gives them for a thin aerofoil in potential flow, and bridge-deck sections are characterised by flutter derivatives measured on section models in a wind tunnel. Separating the torsional and bending frequencies, placing the centre of mass ahead of the elastic axis (mass balancing of control surfaces) and choosing streamlined or slotted deck sections all raise the flutter speed.

A related static instability is torsional divergence: the aerodynamic moment about the elastic axis, $`qcC_{L\alpha}e\,\alpha`$ per unit span (chord $c$, distance $e$ of the elastic axis behind the aerodynamic centre), overcomes the torsional stiffness $k_\alpha$ at $q_D = k_\alpha/(ecC_{L\alpha})$. The Tacoma Narrows collapse was a torsional flutter of the deck, a single-degree-of-freedom instability in which the aerodynamic damping of the torsional mode became negative, not a resonance with vortex shedding (Billah and Scanlan 1991).

## Fluid-Elastic Instability of Tube Bundles

In heat exchangers and steam generators, tubes in cross-flow couple through the flow between them: the displacement of one tube changes the forces on its neighbours. Above a critical gap velocity the array becomes unstable. Connors' relation is the standard design form,

$$
\frac{U_c}{f_nD} = K \sqrt{\frac{m\delta}{\rho D^2}}
$$

with a constant $K$ of about 3 that depends on the array pattern. The instability causes rapid wear at the tube supports, and designs keep the gap velocity below $U_c$ with a margin.

## Suppression and Mitigation

| Measure | How it works | Notes |
| --- | --- | --- |
| Raise $f_n$ (stiffen, shorten spans) | Moves $U_{cr} = f_nD/St$ above the operating range | The cheapest fix when it is possible |
| Add damping (dampers, viscoelastic layers) | Raises $Sc$ and lowers the lock-in amplitude | Effective in air, much less so in water where $Sc$ is small |
| Tuned mass damper | Absorbs energy near $f_n$ | Mass ratio $\mu$ of 1–5% of the modal mass |
| Helical strakes | Three helical fins disrupt the spanwise coherence of shedding | Height about $0.1D$, pitch about $5D$; strongly reduce VIV but raise drag |
| Fairings | Streamlined, free-to-rotate shrouds remove the bluff wake | Used on drilling risers; little drag penalty |
| Splitter plates | Prevent the interaction of the two shear layers | Direction-dependent |
| Shape changes | Rounded or chamfered corners remove galloping and weaken shedding | Used on tall buildings and bridge decks |

For a tuned mass damper of mass $m_d = \mu m$ on a primary system with frequency $f_n$, Den Hartog's tuning for harmonic forcing is

$$
f_d = \frac{f_n}{1 + \mu},
\qquad \zeta_{d,\mathrm{opt}} = \sqrt{\frac{3\mu}{8(1 + \mu)^3}}
$$

### Worked Example: Steel Chimney

A steel chimney with $D = 3$ m, $f_n = 0.5$ Hz, $m = 600$ kg/m and $\zeta = 0.01$ stands in air ($\rho = 1.225$ kg/m³, $St = 0.2$).

1. The critical speed is $U_{cr} = 0.5 \times 3/0.2 = 7.5$ m/s, a wind speed that occurs often at the top of a chimney.
2. With $\delta = 2\pi\zeta = 0.0628$, $Sc = 2 \times 600 \times 0.0628/(1.225 \times 3^2) = 6.8$, in the range where significant VIV is expected.
3. The mass ratio is $m^* = 69$ and $(m^* + C_a)\zeta = 0.70$.

At $U = 15$ m/s the shedding frequency is 1.0 Hz, twice $f_n$, so there is no lock-in at that speed; the concern is the frequent winds near 7.5 m/s and the fatigue they cause. Helical strakes over the top third, or a damper that raises $\zeta$ to 0.03 ($Sc = 20$), are the usual remedies.

## Simulating Flow-Induced Vibration

A CFD simulation of VIV or galloping is a two-way coupled problem: the flow solver computes the force on the body, the structure equation advances the motion, and the mesh moves with the body or the body moves through the mesh. For a rigid body on springs the structural part is one ordinary differential equation per degree of freedom, and the coupling methods of [Fluid–Structure Interaction: Coupling Methods](./fluid_structure_interaction.md) apply. In water the added mass is of the order of the structural mass, so loosely coupled schemes can become unstable. Reproducing the upper branch requires resolving the shear-layer dynamics at the right Reynolds number, which in practice means DNS at low $Re$ or LES at moderate $Re$; two-dimensional and steady RANS computations underpredict the spanwise loss of correlation and the response.

## Key Takeaways

- Distinguish forced mechanisms (buffeting) from lock-in (VIV) and self-excited instabilities (galloping, flutter, fluid-elastic instability).
- VIV starts near $U_r = 1/St \approx 5$ and is governed by mass–damping; it is far more severe in water than in air.
- Den Hartog's criterion $dC_L/d\alpha + C_D < 0$ identifies sections that can gallop; circular cylinders cannot.
- Flutter couples modes and is controlled by frequency separation, mass balancing and section shape.
- Mitigation either moves the critical speed out of range, adds damping, or destroys the coherence of the wake.

## Related Scripts

- [Vortex-Induced Vibration with a Wake Oscillator](../../../scripts/algorithms/fluid_loading_viv_wake_oscillator/): models vortex-induced vibration of an elastically mounted cylinder with the coupled structure and van der Pol wake oscillators of Facchinetti, de Langre and Biolley (2004).
- [Lattice Boltzmann Cylinder Flow Simulation](../../../scripts/simulations/lattice_boltzmann_cylinder_flow/): simulates 2D flow past a circular cylinder with the lattice Boltzmann method (D2Q9 lattice, BGK collision operator) and animates the velocity magnitude and the vorticity with Matplotlib.
- [Steady and Unsteady Pathlines Around a Cylinder with Vortex Shedding](../../../scripts/simulations/steady_and_unsteady_pathlines_with_vortex_shedding/): compares streamlines and particle pathlines for steady potential flow past a cylinder with circulation and for an unsteady version of the same flow with a kinematic vortex-shedding model.
- [Eulerian Cylinder Flow](../../../scripts/simulations/eulerian_cylinder_flow/): simulates 2D incompressible, inviscid flow past a circular cylinder on a fixed Eulerian grid and animates a dye tracer with Matplotlib.
- [Fatigue: S–N Curve, Haigh Diagram and Miner's Rule](../../../scripts/plots/fatigue_sn_and_goodman/): builds the S–N curve of a machined steel shaft from Marin factors, draws the Goodman, Gerber and Soderberg lines with an operating point, and sums the Miner damage of a rainflow-counted random stress history.

## Exercises

**Exercise 1.** A taut cable of diameter $D = 0.03$ m has natural frequency $f_n = 12$ Hz. With $St = 0.2$, find the wind speed at which the Strouhal shedding frequency equals $f_n$, and the wind-speed range of the lock-in band $4 \lesssim U_r \lesssim 8$.

<details>
<summary>Answer</summary>

$f_s = f_n$ when $U = f_nD/St = 12 \times 0.03/0.2 = 1.8$ m/s, that is at $U_r = 1/St = 5$. With $f_nD = 0.36$ m/s the lock-in band is $1.44 \lesssim U \lesssim 2.88$ m/s. Such low speeds occur most of the time, which is why aeolian vibration of cables is a common fatigue problem at clamps.

</details>

**Exercise 2.** A steel riser has $D = 0.3$ m, mass per unit length $m = 150$ kg/m including contents, and damping ratio $\zeta = 0.01$. Compute its Scruton number in seawater ($\rho = 1025$ kg/m³) and in air. What do the values imply?

<details>
<summary>Answer</summary>

$\delta = 2\pi\zeta = 0.0628$, so $2m\delta = 18.85$ kg/m and

```math
Sc_{\mathrm{water}} = \frac{18.85}{1025 \times 0.09} = 0.20, \qquad Sc_{\mathrm{air}} = \frac{18.85}{1.225 \times 0.09} = 171
```

In water large VIV amplitudes, of the order of a diameter, are possible, and doubling the structural damping would barely change that; strakes or fairings are used instead. In air the same riser would hardly respond.

</details>

**Exercise 3.** Wind-tunnel data for a square bar give $dC_L/d\alpha + C_D = -2.7$. With $D = 0.5$ m, $m = 100$ kg/m, $f_n = 2$ Hz and $\zeta = 0.005$ in air, find the galloping onset speed and compare it with the vortex-shedding critical speed for $St = 0.13$. Is the quasi-steady assumption reasonable?

<details>
<summary>Answer</summary>

$\omega_n = 12.57$ rad/s, so

```math
U_g = \frac{4 \times 100 \times 0.005 \times 12.57}{1.225 \times 0.5 \times 2.7} = \frac{25.1}{1.654} = 15.2 \text{ m/s}
```

The shedding critical speed is $U_{cr} = 2 \times 0.5/0.13 = 7.7$ m/s. At $U_g$, $U_r = 15.2$, about twice $1/St = 7.7$, so the shedding frequency is about twice $f_n$; the quasi-steady assumption is marginal, and the interaction of VIV and galloping should be checked in a wind tunnel.

</details>

**Exercise 4.** A steel chimney has modal mass 20 000 kg and $f_n = 0.5$ Hz. Design a tuned mass damper with mass ratio $\mu = 0.02$: give its mass, frequency, spring stiffness, optimum damping ratio and damping coefficient.

<details>
<summary>Answer</summary>

$`m_d = 0.02 \times 20\,000 = 400`$ kg and $f_d = 0.5/1.02 = 0.490$ Hz, so $\omega_d = 3.08$ rad/s.

```math
k_d = m_d\omega_d^2 = 400 \times 3.08^2 = 3.79 \text{ kN/m}
```

```math
\zeta_{d,\mathrm{opt}} = \sqrt{\frac{3 \times 0.02}{8 \times 1.02^3}} = 0.084, \qquad c_d = 2m_d\omega_d\zeta_{d,\mathrm{opt}} = 207 \text{ N s/m}
```

</details>

**Exercise 5.** VIV of a riser produces a stress range of 60 MPa at 0.5 Hz for 50 hours per year. The S–N curve is $N = 10^{12}/\Delta\sigma^3$ with $\Delta\sigma$ in MPa. Estimate the annual Palmgren–Miner damage and the fatigue life for allowable damage sums of 0.33 and 1.0. By how much would a 20% reduction in stress range from strakes extend the life?

<details>
<summary>Answer</summary>

The riser sees $`n = 0.5 \times 3600 \times 50 = 90\,000`$ cycles per year, and $N = 10^{12}/60^3 = 4.63 \times 10^6$ cycles to failure. The annual damage is $n/N = 0.0194$, so the life is $0.33/0.0194 = 17$ years with the safety factor and 51 years to a damage sum of 1. With the cubic S–N slope a 20% lower stress range multiplies the life by $1/0.8^3 = 1.95$. The [fatigue note](../strength_materials/fatigue.md) treats S–N curves and Miner's rule.

</details>

## References

- Blevins, R. D., *Flow-Induced Vibration*, 2nd ed., Van Nostrand Reinhold, 1990.
- Williamson, C. H. K., & Govardhan, R., "Vortex-induced vibrations," *Annual Review of Fluid Mechanics*, 36, 413–455, 2004.
- Khalak, A., & Williamson, C. H. K., "Motions, forces and mode transitions in vortex-induced vibrations at low mass-damping," *Journal of Fluids and Structures*, 13(7–8), 813–851, 1999.
- Facchinetti, M. L., de Langre, E., & Biolley, F., "Coupling of structure and wake oscillators in vortex-induced vibrations," *Journal of Fluids and Structures*, 19(2), 123–140, 2004.
- Païdoussis, M. P., Price, S. J., & de Langre, E., *Fluid-Structure Interactions: Cross-Flow-Induced Instabilities*, Cambridge University Press, 2011.
- Den Hartog, J. P., *Mechanical Vibrations*, 4th ed., McGraw-Hill, 1956.
- Bisplinghoff, R. L., Ashley, H., & Halfman, R. L., *Aeroelasticity*, Addison-Wesley, 1955.
- Simiu, E., & Yeo, D., *Wind Effects on Structures: Modern Structural Design for Wind*, 4th ed., Wiley-Blackwell, 2019.
- Billah, K. Y., & Scanlan, R. H., "Resonance, Tacoma Narrows bridge failure, and undergraduate physics textbooks," *American Journal of Physics*, 59(2), 118–124, 1991.
- Connors, H. J., "Fluidelastic vibration of tube arrays excited by cross flow," in *Flow-Induced Vibration in Heat Exchangers*, ASME, 42–56, 1970.
