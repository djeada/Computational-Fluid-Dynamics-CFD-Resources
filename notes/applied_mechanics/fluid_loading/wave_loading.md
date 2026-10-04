# Wave Loading on Offshore Structures

Wave loading is the primary environmental action on offshore structures such as fixed platforms, floating production systems, subsea pipelines, and wind turbine foundations. This chapter covers the fundamental wave theories, force calculation methods, and design approaches used in offshore engineering practice.

## Linear Wave Theory (Airy Theory)

### Surface Elevation

The simplest description of ocean surface waves uses **Airy (linear) theory**. For a regular wave travelling in the positive $x$-direction:

$$
\eta(x,t) = \frac{H}{2}\cos(kx - \omega t)
$$

where:

- $H$ = wave height (crest-to-trough)
- $k = 2\pi/\lambda$ = wave number
- $\omega = 2\pi/T$ = angular frequency
- $\lambda$ = wavelength, $T$ = wave period

### Dispersion Relation

The relationship between wave frequency and wave number in water of depth $d$ is:

$$
\omega^2 = gk\tanh(kd)
$$

Limiting cases:

- **Deep water** ($d/\lambda > 0.5$): $\omega^2 \approx gk$, $\lambda_0 = gT^2/(2\pi)$
- **Shallow water** ($d/\lambda < 0.05$): $\omega^2 \approx gk^2 d$, $c = \sqrt{gd}$

## Wave Kinematics

### Horizontal Velocity

$$
u = \frac{\pi H}{T} \frac{\cosh k(z+d)}{\sinh kd} \cos(kx - \omega t)
$$

### Vertical Velocity

$$
w = \frac{\pi H}{T} \frac{\sinh k(z+d)}{\sinh kd} \sin(kx - \omega t)
$$

### Horizontal Acceleration

$$
\dot{u} = \frac{2\pi^2 H}{T^2} \frac{\cosh k(z+d)}{\sinh kd} \sin(kx - \omega t)
$$

### Dynamic Pressure

$$
p_d = \rho g \frac{H}{2} \frac{\cosh k(z+d)}{\cosh kd} \cos(kx - \omega t)
$$

The kinematics decay with depth; in deep water the decay factor is $e^{kz}$ (with $z$ measured upward from the still water level, negative downward).

## Morison Equation

For **slender cylindrical members** where the member diameter $D$ is small compared with the wavelength ($D/\lambda < 0.2$), wave forces are calculated using the Morison equation:

```math
dF = \underbrace{\rho \frac{\pi D^2}{4} C_M \dot{u}}_{\text{inertia}} \; dz +
\underbrace{\frac{1}{2}\rho D C_D |u| u}_{\text{drag}} \; dz
```

where:

- $C_M$ = inertia coefficient (typically 1.6–2.0 for smooth cylinders)
- $C_D$ = drag coefficient (typically 0.6–1.2 depending on roughness and Reynolds number)
- $\dot{u}$ = horizontal fluid acceleration
- $u$ = horizontal fluid velocity

### Total Force and Overturning Moment

The total horizontal force on a vertical pile from the seabed ($z = -d$) to the surface ($z = 0$) is:

$$
F = \int_{-d}^{0} dF
$$

The overturning moment about the seabed is:

```math
M = \int_{-d}^{0} (z + d) \, dF
```

### Inertia- vs. Drag-Dominated Regimes

The Keulegan–Carpenter number classifies the relative importance:

$$
KC = \frac{u_{max} T}{D}
$$

- $KC < 10$: inertia-dominated (large-diameter members, small waves)
- $KC > 25$: drag-dominated (slender members, large waves)

## Diffraction Theory for Large Structures

When $D/\lambda > 0.2$, the structure significantly modifies the incident wave field and **diffraction effects** must be included. The total force is found by integrating the pressure from the combined incident and scattered wave fields over the structure surface:

```math
F = \iint_S p \, \hat{n} \, dS
```

### MacCamy–Fuchs Solution

For a vertical circular cylinder of radius $a$ in linear waves, the analytical solution gives the inertia coefficient correction:

$$
C_M = \frac{4}{\pi (ka)^2} \left| \frac{1}{H_1'^{(1)}(ka)}\right|
$$

where $H_1'^{(1)}$ is the derivative of the Hankel function of the first kind. As $ka \to 0$ the result recovers the Morison inertia limit.

### Numerical Diffraction Analysis

For arbitrary geometries, boundary element methods (panel methods) solve the potential flow problem:

- Structure surface is discretised into panels
- Green's function satisfies the free surface, seabed, and radiation conditions
- Output includes wave forces, added mass, radiation damping, and wave run-up

Common software: WAMIT, ANSYS AQWA, OrcaFlex, NEMOH (open-source).

## Design Wave Approach

### Deterministic Method

A single **design wave** with specified height $H_d$ and period $T_d$ is used to calculate the maximum force. The design wave height is typically the 100-year return period individual wave:

```math
H_{100} \approx 1.86 \, H_{s,100}
```

where $H_{s,100}$ is the 100-year significant wave height (Rayleigh distribution assumption).

### Load Cases

For jacket-type platforms, critical load cases include:

1. Maximum base shear — wave crest at the structure
2. Maximum overturning moment — wave crest at the structure
3. Maximum member force — wave position varied to find worst case per member

### Higher-Order Wave Theories

For steep waves in shallow water, linear theory is insufficient. Design practice uses:

- **Stokes 5th-order theory** for deep and intermediate water
- **Stream function theory** for general applicability
- **Cnoidal theory** for very shallow water

## Spectral Methods

### Wave Energy Spectrum

Real sea states are irregular and described statistically using a wave spectrum $S(\omega)$. Common spectral models:

**JONSWAP spectrum** (fetch-limited seas):

$$
S(\omega) = \alpha g^2 \omega^{-5}
\exp\left[-\frac{5}{4}\left(\frac{\omega_p}{\omega}\right)^4\right]
\gamma^{\exp\left[-\frac{(\omega - \omega_p)^2}{2\sigma^2\omega_p^2}\right]}
$$

where $\omega_p = 2\pi/T_p$ is the peak frequency and $\gamma \approx 3.3$ is the peak enhancement factor.

**Pierson–Moskowitz spectrum** (fully developed seas): same form with $\gamma = 1$.

### Spectral Force Calculation

The response spectrum of force (or moment) is obtained by transferring the wave spectrum through the force transfer function $|H_F(\omega)|^2$:

```math
S_F(\omega) = |H_F(\omega)|^2 \, S(\omega)
```

The standard deviation of the force is:

```math
\sigma_F = \sqrt{\int_0^\infty S_F(\omega) \, d\omega}
```

The most probable maximum force in a sea state of duration $D_{st}$ is:

$$
F_{max} \approx \sigma_F \sqrt{2\ln(f_0 D_{st})}
$$

where $f_0$ is the mean zero-crossing frequency of the force process.

## Worked Example 1: Morison Force on a Monopile

**Given:**

- Vertical steel monopile: $D = 2$ m, water depth $d = 20$ m
- Design wave: $H = 6$ m, $T = 10$ s (Airy theory)
- $C_M = 2.0$, $C_D = 1.0$, seawater $\rho = 1025$ kg/m³

**Find:** Maximum total horizontal force.

**Solution:**

Wave number from dispersion relation (iterative): $k \approx 0.0518$ m⁻¹, $\lambda \approx 121$ m ($kd \approx 1.04$, intermediate depth).

Check slenderness: $D/\lambda = 2/121 = 0.017 < 0.2$ — Morison equation applies.

Maximum velocity at $z = 0$:

$$
u_{max} = \frac{\pi H}{T} \frac{1}{\tanh kd} = \frac{\pi \times 6}{10} \times
\frac{1}{\tanh(1.04)} = 1.885 \times 1.288 = 2.43 \text{ m/s}
$$

Maximum acceleration at $z = 0$:

$$
\dot{u}_{max} = \frac{2\pi^2 H}{T^2} \frac{1}{\tanh kd} = \frac{2\pi^2 \times 6}{100}
\times 1.288 = 1.53 \text{ m/s}^2
$$

Inertia force (integrated over depth; the $\cosh k(z+d)$ profile integrates to a factor $`\tanh(kd)/(kd)`$):

$$
F_I = \rho \frac{\pi D^2}{4} C_M \dot{u}_{max} \frac{\tanh kd}{kd} d \approx 1025 \times
3.14 \times 2.0 \times 1.53 \times 0.749 \times 20 \approx 147 \text{ kN}
$$

Drag force (integrated, simplified):

$$
F_D \approx \frac{1}{2}\rho D C_D u_{max}^2 \frac{d}{2} \approx 0.5 \times 1025 \times 2
\times 1.0 \times 5.89 \times 10 \approx 60 \text{ kN}
$$

(Integrating the $\cosh^2 k(z+d)$ profile exactly gives $F_D \approx 69$ kN.)

Maximum inertia and maximum drag do not occur simultaneously (90° phase difference). Writing $F(\phi) = F_I \sin\phi + F_D |\cos\phi| \cos\phi$, the peak equals $F_I$ whenever $F_D \leq F_I/2$, which holds here (inertia-dominated, $KC \approx 12.1$):

$$
F_{max} \approx 147 \text{ kN}
$$

## Worked Example 2: Diffraction Check

**Given:**

- Concrete gravity base structure: $D = 30$ m, $\lambda = 150$ m

**Find:** Whether diffraction analysis is required.

**Solution:**

$$
\frac{D}{\lambda} = \frac{30}{150} = 0.20
$$

At the threshold $D/\lambda = 0.2$, diffraction effects become significant. A **diffraction analysis** (e.g., panel method) should be used instead of the Morison equation for the base structure.

## Worked Example 3: Spectral Force Estimate

**Given:**

- Sea state: $H_s = 4$ m, $T_p = 9$ s (JONSWAP, $\gamma = 3.3$)
- Monopile $D = 2$ m, $d = 20$ m (inertia-dominated)
- Storm duration: 3 hours

**Find:** Most probable maximum horizontal force.

**Solution:**

The force transfer function for an inertia-dominated monopile is approximately:

$$
|H_F(\omega)|^2 \propto \left(\rho \frac{\pi D^2}{4} C_M \omega \frac{\tanh kd}{kd} d\right)^2
$$

Numerical integration of $S_F(\omega) = |H_F(\omega)|^2 S(\omega)$ over frequency gives $\sigma_F \approx 55$ kN.

Mean zero-crossing frequency: $f_0 \approx 0.11$ Hz (close to the spectral peak).

$$
F_{max} \approx 55 \sqrt{2\ln(0.11 \times 10800)} = 55 \times 3.76 \approx 207
\text{ kN}
$$

## Applications in Offshore Engineering

### Fixed Platforms (Jackets)

- Morison equation applied member-by-member
- Combined wave, current, and wind loading
- Fatigue design uses long-term wave scatter diagrams

### Floating Production Systems (FPSO, Semi-submersible)

- Diffraction/radiation analysis for hull motions
- Mooring line tensions derived from motion response
- Riser design depends on vessel offsets and motions

### Offshore Wind Turbines

- Monopile foundations: Morison equation with higher-order wave theories
- Jacket foundations: member-level Morison loading
- Combined wind and wave loading requires aero-hydro-elastic simulation

### Subsea Pipelines

- On-bottom stability against wave- and current-induced forces
- Hydrodynamic lift, drag, and inertia on near-seabed pipes
- Burial or rock-dumping for protection in shallow water

## Design Considerations

### Load Combinations

- 100-year wave combined with 10-year current and 10-year wind (or other code-specified combinations)
- Collinear and non-collinear cases examined

### Marine Growth

- Biofouling increases effective diameter and roughness
- Drag coefficient increases from $C_D \approx 0.65$ (smooth) to $C_D \approx 1.05$ (rough)
- Marine growth thickness of 50–150 mm is typical in design

### Current Superposition

- Steady current velocity is added vectorially to wave particle velocity in the Morison equation
- Current stretching methods (e.g., Hedges, Wheeler) extend kinematics to the instantaneous surface

Wave loading analysis is the cornerstone of offshore structural design, connecting oceanographic data to engineering forces that drive member sizing, foundation design, and fatigue life prediction.

## Related Scripts

- [Froude Number vs. Flow Velocity](../../../scripts/plots/froude_number/): plots the length-based Froude number $Fr = U/\sqrt{gL}$ against speed for hulls of 5, 10, 15, and 20 m, with reference lines at hull speed and at the approximate start of planing.
- [Ship Hull in Water](../../../scripts/plots/ship_hull_in_water/): draws a side-view sketch of a ship hull sitting in a sinusoidal free-surface wave and annotates it with the Froude number $Fr = U/\sqrt{gL}$.

## Exercises

**Exercise 1.** For a wave of period $T = 8$ s, find the deep-water wavelength and phase speed, and check whether a water depth of 60 m counts as deep water.

<details>
<summary>Answer</summary>

```math
\lambda_0 = \frac{gT^2}{2\pi} = \frac{9.81 \times 64}{2\pi} = 99.9 \text{ m}, \quad
c = \frac{\lambda_0}{T} = 12.5 \text{ m/s}
```

$d/\lambda_0 = 60/99.9 = 0.60 > 0.5$, so the deep-water approximation is valid.

</details>

**Exercise 2.** The same 8 s wave travels into water 15 m deep. Solve the dispersion relation for $k$ and $\lambda$, classify the depth, and compare with the deep-water and shallow-water estimates.

<details>
<summary>Answer</summary>

Solving $\omega^2 = gk\tanh(kd)$ with $\omega = 0.785$ rad/s and $d = 15$ m numerically (Newton or fixed-point iteration) gives $k = 0.0768$ m⁻¹ and $\lambda = 81.8$ m.

$d/\lambda = 0.18$ lies between 0.05 and 0.5, so this is intermediate depth. The deep-water value (99.9 m) and the shallow-water value $T\sqrt{gd} = 97.0$ m both overestimate the wavelength by about 20%, so the full relation is needed.

</details>

**Exercise 3.** A deep-water wave has $H = 4$ m and $T = 8$ s. Find the surface particle velocity amplitude and the Keulegan-Carpenter number for a 1 m diameter leg and a 0.3 m diameter brace. Which force component dominates on each?

<details>
<summary>Answer</summary>

In deep water the factor $\cosh k(z+d)/\sinh kd \to 1$ at the surface, so $u_{max} = \pi H/T = 1.57$ m/s.

- Leg: $KC = u_{max}T/D = 1.57 \times 8/1 = 12.6$. This lies between the regimes, so both inertia and drag matter.
- Brace: $KC = 12.57/0.3 = 41.9 > 25$, so the brace is drag-dominated.

</details>

**Exercise 4.** For the 1 m leg of Exercise 3 at the still-water level ($C_M = 2$, $C_D = 1$, $\rho = 1025$ kg/m³), find the inertia and drag force amplitudes per unit length. Show that when $F_D \geq F_I/2$ the peak of $F_I\sin\phi + F_D|\cos\phi|\cos\phi$ is $F_D + F_I^2/(4F_D)$, and evaluate it.

<details>
<summary>Answer</summary>

$\dot{u}_{max} = 2\pi^2H/T^2 = 1.234$ m/s², so

```math
F_I = 1025 \times \frac{\pi}{4} \times 2 \times 1.234 = 1986 \text{ N/m}, \quad
F_D = 0.5 \times 1025 \times 1 \times 1.571^2 = 1265 \text{ N/m}
```

For $\cos\phi > 0$, $`dF/d\phi = \cos\phi\,(F_I - 2F_D\sin\phi) = 0`$ gives $\sin\phi = F_I/(2F_D)$, which is only possible if $F_D \geq F_I/2$. Substituting back:

```math
F_{max} = \frac{F_I^2}{2F_D} + F_D\left(1 - \frac{F_I^2}{4F_D^2}\right) = F_D +
\frac{F_I^2}{4F_D} = 1265 + 780 = 2045 \text{ N/m}
```

This occurs at $\phi = 51.8^\circ$. If $F_D < F_I/2$, the peak is simply $F_I$.

</details>

**Exercise 5.** A spectral analysis gives a force standard deviation $\sigma_F = 40$ kN with mean zero-crossing frequency $f_0 = 0.15$ Hz. Estimate the most probable maximum force in a 3-hour storm. For comparison, what individual design wave height corresponds to $H_s = 6$ m?

<details>
<summary>Answer</summary>

```math
F_{max} \approx 40 \sqrt{2\ln(0.15 \times 10\,800)} = 40 \sqrt{2 \times 7.39} = 40
\times 3.84 = 154 \text{ kN}
```

The deterministic design wave is $H_{max} \approx 1.86H_s = 11.2$ m.

</details>

## References

- T. Sarpkaya, M. Isaacson, *Mechanics of Wave Forces on Offshore Structures*, Van Nostrand Reinhold, 1981.
- R. G. Dean, R. A. Dalrymple, *Water Wave Mechanics for Engineers and Scientists*, World Scientific, 1991.
- O. M. Faltinsen, *Sea Loads on Ships and Offshore Structures*, Cambridge University Press, 1990.
- S. K. Chakrabarti, *Hydrodynamics of Offshore Structures*, Computational Mechanics Publications, 1987.
- J. R. Morison, M. P. O'Brien, J. W. Johnson, S. A. Schaaf, "The force exerted by surface waves on piles", *Petroleum Transactions, AIME* 189, 1950.
