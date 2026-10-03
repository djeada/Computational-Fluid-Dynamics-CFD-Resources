# Equation of State

## Overview

The equation of state provides the **thermodynamic closure** for the fluid mechanics equations by relating pressure, density, and temperature. It's essential for:

- **Compressible flow analysis** (density variations)
- **Thermodynamic property calculations** (speed of sound, specific heats)
- **Phase change phenomena** (vapor-liquid equilibrium)
- **Real gas effects** (high pressure, temperature conditions)

## General Concept

### Mathematical Form

A general equation of state relates thermodynamic state variables:

$$
f(p, \rho, T) = 0
$$

or in explicit forms:

$$
p = p(\rho, T)
$$

$$
\rho = \rho(p, T)
$$

$$
T = T(p, \rho)
$$

### Closure of Conservation Equations

The conservation equations provide:

- **Continuity**: Relates $\rho$ and $\vec{V}$
- **Momentum**: Relates $\vec{V}$ and $p$
- **Energy**: Relates $e$ (or $T$) and other variables

The equation of state **closes the system** by providing the $p$-$\rho$-$T$ relationship.

## Ideal Gas Law

### Basic Form

$$
p = \rho R T
$$

where:

- $p$ = pressure \[Pa\]
- $\rho$ = density \[kg/m³\]
- $R$ = specific gas constant \[J/(kg⋅K)\]
- $T$ = absolute temperature \[K\]

### Gas Constants

**Universal gas constant**: $R_u = 8314.5$ J/(kmol⋅K)

**Specific gas constant**: $R = R_u/M$ where $M$ is molar mass

**Common values**:

- Air: $R = 287.0$ J/(kg⋅K), $M = 28.97$ kg/kmol
- Helium: $R = 2077$ J/(kg⋅K), $M = 4.00$ kg/kmol
- Water vapor: $R = 461.5$ J/(kg⋅K), $M = 18.02$ kg/kmol

### Caloric Relations

For an ideal gas, internal energy depends only on temperature:

$$
e = e(T) = c_v T + \text{constant}
$$

$$
h = h(T) = c_p T + \text{constant}
$$

**Specific heat relation**:

$$
c_p - c_v = R
$$

**Specific heat ratio**:

$$
\gamma = \frac{c_p}{c_v}
$$

### Speed of Sound

For an ideal gas:

$$
a^2 = \frac{\partial p}{\partial \rho}\bigg|_s = \gamma \frac{p}{\rho} = \gamma R T
$$

Therefore:

$$
a = \sqrt{\gamma R T}
$$

## Isentropic Relations

### Basic Relations

For reversible, adiabatic (isentropic) processes:

$$
p \rho^{-\gamma} = \text{constant}
$$

$$
T \rho^{-(\gamma-1)} = \text{constant}
$$

$$
p^{(\gamma-1)/\gamma} T^{-1} = \text{constant}
$$

### Differential Forms

$$
\frac{dp}{p} = \gamma \frac{d\rho}{\rho}
$$

$$
\frac{dT}{T} = (\gamma - 1) \frac{d\rho}{\rho}
$$

$$
\frac{dp}{p} = \frac{\gamma}{\gamma-1} \frac{dT}{T}
$$

### Applications

**Compressible flow analysis**:

- Isentropic nozzle flows
- Shock wave relations (combined with Rankine-Hugoniot)
- Expansion fan analysis

## Real Gas Effects

### Limitations of Ideal Gas Law

The ideal gas law fails when:

1. **High pressure**: Molecular volume becomes significant
2. **Low temperature**: Intermolecular forces become important
3. **Near critical point**: Phase change effects
4. **Very light molecules**: Quantum effects (e.g., hydrogen at low T)

### Van der Waals Equation

$$
\left(p + \frac{a}{\bar{v}^2}\right)(\bar{v} - b) = RT
$$

where:

- $\bar{v} = 1/\rho$ is specific volume
- $a$ = intermolecular attraction parameter
- $b$ = molecular volume parameter

**Physical meaning**:

- $a/\bar{v}^2$ term: Accounts for intermolecular attractions
- $b$ term: Accounts for finite molecular size

### Compressibility Factor

$$
z = \frac{p\bar{v}}{RT} = \frac{p}{\rho RT}
$$

**For ideal gas**: $z = 1$

**For real gases**: $z \neq 1$

- $z < 1$: Attractive forces dominate (moderate pressures, temperatures below the Boyle temperature)
- $z > 1$: Repulsive forces dominate (very high pressures, or temperatures above the Boyle temperature)

### Virial Equation

$$
z = 1 + B(T)\rho + C(T)\rho^2 + \cdots
$$

where $B(T)$, $C(T)$ are virial coefficients depending only on temperature.

### Redlich-Kwong Equation

$$
p = \frac{RT}{\bar{v} - b} - \frac{a}{\sqrt{T}\bar{v}(\bar{v} + b)}
$$

Better accuracy than van der Waals for many applications.

### Peng-Robinson Equation

$$
p = \frac{RT}{\bar{v} - b} - \frac{a\alpha(T)}{\bar{v}(\bar{v} + b) + b(\bar{v} - b)}
$$

Widely used in process engineering for hydrocarbon systems.

## Phase Equilibrium

### Clausius-Clapeyron Equation

For phase transitions:

$$
\frac{dp_{sat}}{dT} = \frac{L}{T(\bar{v}_g - \bar{v}_l)}
$$

where:

- $L$ = latent heat of vaporization
- $\bar{v}_g$, $\bar{v}_l$ = specific volumes of gas and liquid phases

### Critical Point

**Critical constants**: $T_c$, $p_c$, $\rho_c$

**Reduced properties**:

$$
T_r = \frac{T}{T_c}, \quad p_r = \frac{p}{p_c}, \quad \rho_r = \frac{\rho}{\rho_c}
$$

**Principle of corresponding states**: Fluids with same reduced properties have same compressibility factor.

### Two-Phase Flow

In the saturation region:

$$
\frac{1}{\rho} = \frac{x}{\rho_g} + \frac{1-x}{\rho_l}
$$

$$
h = xh_g + (1 - x)h_l
$$

where $x$ is the dryness fraction (quality).

## Specific Applications

### High-Speed Aerodynamics

**Real gas effects** become important for:

- **Hypersonic flight**: $Ma > 5$, high temperature behind shock waves
- **Reentry vehicles**: Extreme heating, dissociation, ionization
- **Rocket nozzles**: High pressure and temperature conditions

**Modified relations**:

$$
a^2 = \frac{\partial p}{\partial \rho}\bigg|_s = \gamma
\frac{\partial p}{\partial \rho}\bigg|_T, \quad \gamma = \frac{c_p}{c_v}
$$

### Gas Turbine Engines

**Combustion products**: Mixture of gases with varying composition

$$
R_{mix} = \sum_i y_i R_i
$$

$$
\gamma_{mix} = f(T, \text{composition})
$$

**Variable specific heats**: $c_p = c_p(T)$, $c_v = c_v(T)$

### Cryogenic Systems

**Liquid nitrogen, oxygen, hydrogen**:

- Significant deviations from ideal gas behavior
- Phase change considerations
- Quantum effects for hydrogen

### Supercritical Fluids

**Above critical point**: No distinct liquid-gas phases

$$
z = z(p_r, T_r)
$$

Applications in supercritical extraction, power cycles.

## Computational Implementation

### Tabulated Data

**NIST databases**: Real fluid properties

- REFPROP: Reference fluid properties
- CoolProp: Open-source property database

**Implementation**: Interpolation routines for $p(\rho,T)$, $h(\rho,T)$, etc.

### Analytic Approximations

**Polynomial fits**:

$$
c_p(T) = a_0 + a_1 T + a_2 T^2 + a_3 T^3 + \cdots
$$

**NASA polynomials**: Standard format for combustion gases

### Iterative Procedures

For implicit equations of state:

$$
F(p, \rho, T) = 0
$$

Use Newton-Raphson or other root-finding methods.

## Numerical Methods

### Density-Based Solvers

**Conservative variables**: $(\rho, \rho \vec{V}, \rho E)$

**Equation of state**: $p = p(\rho, e)$ where $e = E - \frac{1}{2}V^2$

### Pressure-Based Solvers

**Primitive variables**: $(p, \vec{V}, T)$

**Density from EOS**: $\rho = \rho(p, T)$

### Preconditioning for Low Mach Number

**Artificial compressibility**: Modify time derivatives to improve conditioning

$$
\frac{1}{\beta^2} \frac{\partial p}{\partial t} + \nabla \cdot \vec{V} = 0
$$

where $\beta$ is artificial compressibility parameter.

## Measurement and Calibration

### Direct Measurements

**Pressure**: Piezoelectric, strain gauge transducers
**Temperature**: Thermocouples, resistance temperature detectors
**Density**: Vibrating tube densimeters, buoyancy methods

### Derived Properties

**Speed of sound**: Acoustic measurements

$$
a = \sqrt{\frac{\partial p}{\partial \rho}\bigg|_s}
$$

**Specific heats**: Calorimetric methods

### Uncertainty Analysis

Propagation of measurement uncertainties through equation of state:

$$
\delta p = \frac{\partial p}{\partial \rho}\delta \rho +
\frac{\partial p}{\partial T}\delta T
$$

## Historical Development

- **1662**: Boyle's law ($p \propto 1/V$ at constant temperature)
- **1802**: Gay-Lussac's law ($V \propto T$ at constant pressure)
- **1834**: Clapeyron combined these into ideal gas law
- **1873**: van der Waals developed first real gas equation
- **1940s**: Development of corresponding states principle

## Engineering Applications

### Aircraft and Spacecraft

**Standard atmosphere**: $p$, $\rho$, $T$ vs. altitude

$$
p = p_0 \left(1 - \frac{\Lambda z}{T_0}\right)^{g/(R \Lambda)}
$$

for the troposphere, where the temperature falls linearly as $T = T_0 - \Lambda z$ with lapse rate $\Lambda \approx 0.0065$ K/m and $R$ is the specific gas constant.

**Flight performance**: Thrust, lift calculations depend on air density

### Process Engineering

**Distillation columns**: Vapor-liquid equilibrium
**Chemical reactors**: Real gas effects on reaction rates
**Pipeline flow**: Compressibility effects in gas transmission

### Power Generation

**Steam cycles**: Water/steam properties from NIST steam tables
**Gas turbines**: Air and combustion product properties
**Supercritical CO₂**: Advanced power cycle working fluid

### Environmental Engineering

**Atmospheric modeling**: Real gas effects in weather prediction
**Pollution dispersion**: Density stratification effects
**Climate modeling**: Radiative properties of gases

## Learning Strategy

### Prerequisites

- Thermodynamics fundamentals
- Kinetic theory of gases
- Basic fluid mechanics principles

### Key Concepts

1. Ideal gas law and its limitations
2. Real gas effects and when they become important
3. Phase equilibrium and critical phenomena
4. Isentropic relations for compressible flow
5. Computational implementation considerations
6. Connection to conservation equations

### Problem-Solving Approach

1. Identify flow conditions (pressure, temperature range)
2. Assess validity of ideal gas assumption
3. Select appropriate equation of state
4. Implement consistently with conservation equations
5. Validate against experimental data or correlations

### Common Mistakes

1. Using ideal gas law outside its range of validity
2. Inconsistent use of specific vs. molar quantities
3. Neglecting temperature dependence of specific heats
4. Incorrect application of isentropic relations
5. Units confusion (absolute vs. gauge pressure)

Understanding equations of state is crucial for accurate fluid mechanics analysis, especially in compressible flows, high-temperature applications, and systems involving phase changes. The choice of equation of state can significantly impact the accuracy of numerical simulations and engineering calculations.

## Exercises

**Exercise 1.** Use the ideal gas law to compute the density of air ($R = 287$ J/(kg K)) and of helium ($R = 2077$ J/(kg K)) at $p = 101325$ Pa and $T = 288.15$ K.

<details>
<summary>Answer</summary>

$\rho = p/(RT)$:

- Air: $101325/(287 \times 288.15) = 1.225$ kg/m³.
- Helium: $101325/(2077 \times 288.15) = 0.169$ kg/m³.

Helium is about 7 times less dense than air, which is what gives a balloon its lift.

</details>

**Exercise 2.** Air ($\gamma = 1.4$, $R = 287$ J/(kg K)) is compressed isentropically from $p_1 = 100$ kPa, $T_1 = 300$ K to $p_2 = 800$ kPa. Find $T_2$, $\rho_1$, $\rho_2$ and check the result with $p\\rho^{-\\gamma} = $ constant.

<details>
<summary>Answer</summary>

$T_2 = T_1 (p_2/p_1)^{(\gamma-1)/\gamma} = 300 \times 8^{0.2857} = 543.4$ K.

$\rho_1 = 100000/(287 \times 300) = 1.161$ kg/m³ and $\rho_2 = 800000/(287 \times 543.4) = 5.129$ kg/m³.

Check: $\rho_2/\rho_1 = 4.416$ and $8^{1/1.4} = 4.416$. The two agree.

</details>

**Exercise 3.** Carbon dioxide at $T = 300$ K occupies a molar volume $v_m = 5.0 \times 10^{-4}$ m³/mol, a density of about 88 kg/m³. Using the molar van der Waals form $(p + a/v_m^2)(v_m - b) = R_u T$ with $a = 0.364$ Pa m⁶/mol², $b = 4.267 \times 10^{-5}$ m³/mol and $R_u = 8.314$ J/(mol K), compute $p$. Compare it with the ideal-gas value and find the compressibility factor $z$.

<details>
<summary>Answer</summary>

Ideal gas: $p = R_u T/v_m = 8.314 \times 300/(5 \times 10^{-4}) = 4.99$ MPa.

Van der Waals:

$$
p = \frac{R_u T}{v_m - b} - \frac{a}{v_m^2} = \frac{2494.2}{4.573 \times 10^{-4}} -
\frac{0.364}{2.5 \times 10^{-7}} = 5.454 \times 10^6 - 1.456 \times 10^6 = 4.00
\text{ MPa}
$$

$z = p v_m/(R_u T) = 0.80$. With $z < 1$, attraction dominates, and the ideal gas law overpredicts the pressure by about 25%.

</details>

**Exercise 4.** Compare the speed of sound in air ($\gamma = 1.4$, $R = 287$ J/(kg K)) and in helium ($\gamma = 5/3$, $R = 2077$ J/(kg K)) at 300 K.

<details>
<summary>Answer</summary>

- Air: $a = \sqrt{1.4 \times 287 \times 300} = 347$ m/s.
- Helium: $a = \sqrt{(5/3) \times 2077 \times 300} = 1019$ m/s.

Helium's small molar mass (large $R$) and larger $\gamma$ give it almost three times the sound speed of air. This is why helium raises the pitch of the voice.

</details>

**Exercise 5.** A saturated water-steam mixture at 100 °C has quality $x = 0.1$. Take $v_l = 0.001043$ m³/kg and $v_g = 1.672$ m³/kg. Compute the mixture density, and show that mass-weighting the phase densities, $x\rho_g + (1-x)\rho_l$, gives a badly wrong answer.

<details>
<summary>Answer</summary>

Quality is a mass fraction, so specific volumes add:

$$
v = x v_g + (1 - x) v_l = 0.1 \times 1.672 + 0.9 \times 0.001043 = 0.1681 \text{ m}^3/
\text{kg}
$$

giving $\rho = 1/v = 5.95$ kg/m³.

Mass-weighting the densities instead gives $0.1 \times 0.598 + 0.9 \times 958.8 = 863$ kg/m³, about 145 times too large. Although only 10% of the mass is steam, the steam fills more than 99% of the volume.

</details>

## References

- H. B. Callen, *Thermodynamics and an Introduction to Thermostatistics*, 2nd ed., Wiley, 1985.
- B. E. Poling, J. M. Prausnitz, J. P. O'Connell, *The Properties of Gases and Liquids*, 5th ed., McGraw-Hill, 2001.
- D.-Y. Peng, D. B. Robinson, "A new two-constant equation of state", *Industrial & Engineering Chemistry Fundamentals* 15(1), 59–64, 1976.
- J. D. Anderson, *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003.
