# Compressible Flow Theory

## Overview

Compressible flow involves significant density variations due to pressure changes. This occurs when:
- **High velocities**: Mach number $Ma > 0.3$
- **Large pressure differences**: $\Delta p/p > 5\%$
- **High-speed phenomena**: Shock waves, expansion fans
- **Gas dynamics**: Supersonic and hypersonic flows

## Fundamental Concepts

### Compressibility Effects

**Density variation**: Unlike incompressible flow where $\rho = \text{constant}$, compressible flow has:
$$\frac{D\rho}{Dt} \neq 0$$

**Speed of sound**: Characteristic velocity for pressure wave propagation:
$$a = \sqrt{\frac{\partial p}{\partial \rho}\bigg|_s} = \sqrt{\gamma R T}$$

for an ideal gas with isentropic processes.

**Mach number**: Fundamental parameter:
$$Ma = \frac{V}{a}$$

### Thermodynamic Relations

#### Ideal Gas Law
$$p = \rho R T$$

where $R$ is the specific gas constant.

#### Specific Heats
$$c_p - c_v = R$$
$$\gamma = \frac{c_p}{c_v}$$

For air: $\gamma \approx 1.4$, $R \approx 287$ J/(kg⋅K)

#### Isentropic Relations
$$\frac{T_2}{T_1} = \left(\frac{p_2}{p_1}\right)^{(\gamma-1)/\gamma}$$
$$\frac{\rho_2}{\rho_1} = \left(\frac{p_2}{p_1}\right)^{1/\gamma}$$

## Governing Equations

### Conservation Laws

#### Continuity Equation
$$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{V}) = 0$$

#### Momentum Equation
$$\frac{\partial (\rho \vec{V})}{\partial t} + \nabla \cdot (\rho \vec{V} \vec{V}) = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \vec{g}$$

#### Energy Equation
$$\frac{\partial E}{\partial t} + \nabla \cdot ((E + p)\vec{V}) = \nabla \cdot (\boldsymbol{\tau} \cdot \vec{V}) + \nabla \cdot (k \nabla T) + \rho \vec{g} \cdot \vec{V}$$

where $E = \rho(e + \frac{1}{2}V^2)$ is total energy per unit volume.

### One-Dimensional Flow

For steady, 1D flow with area variation:

**Continuity**: $\rho V A = \text{constant}$

**Momentum**: $\rho V \frac{dV}{dx} = -\frac{dp}{dx}$ (inviscid)

**Energy**: $h + \frac{1}{2}V^2 = h_0 = \text{constant}$ (adiabatic)

where $h = c_p T$ is specific enthalpy.

## Isentropic Flow Relations

### Stagnation Properties

**Stagnation temperature**:
$$T_0 = T + \frac{V^2}{2c_p} = T\left(1 + \frac{\gamma-1}{2}Ma^2\right)$$

**Stagnation pressure**:
$$p_0 = p\left(1 + \frac{\gamma-1}{2}Ma^2\right)^{\gamma/(\gamma-1)}$$

**Stagnation density**:
$$\rho_0 = \rho\left(1 + \frac{\gamma-1}{2}Ma^2\right)^{1/(\gamma-1)}$$

### Critical Conditions

At the **sonic condition** ($Ma = 1$):

**Critical temperature**:
$$T^* = \frac{2}{\gamma+1}T_0$$

**Critical pressure**:
$$p^* = \left(\frac{2}{\gamma+1}\right)^{\gamma/(\gamma-1)}p_0$$

**Critical density**:
$$\rho^* = \left(\frac{2}{\gamma+1}\right)^{1/(\gamma-1)}\rho_0$$

For air: $T^*/T_0 = 0.833$, $p^*/p_0 = 0.528$, $\rho^*/\rho_0 = 0.634$

## Area-Velocity Relations

### Differential Form

From continuity and momentum for isentropic flow:
$$\frac{dV}{V} = -\frac{d\rho}{\rho}$$
$$\frac{dV}{V} = \frac{dA/A}{Ma^2 - 1}$$

**Key insights**:
- **Subsonic** ($Ma < 1$): Converging nozzle accelerates flow
- **Supersonic** ($Ma > 1$): Diverging nozzle accelerates flow
- **Sonic** ($Ma = 1$): Minimum area (throat) required

### Area Ratio

$$\frac{A}{A^*} = \frac{1}{Ma}\left[\frac{2}{\gamma+1}\left(1 + \frac{\gamma-1}{2}Ma^2\right)\right]^{(\gamma+1)/[2(\gamma-1)]}$$

This function has:
- Minimum at $Ma = 1$ where $A = A^*$
- Same area ratio for subsonic and supersonic Mach numbers
- Choked flow occurs when $A_{throat} = A^*$

## Shock Waves

### Normal Shock Relations

For a stationary normal shock, the **Rankine-Hugoniot relations** give:

**Mach number**:
$$Ma_2^2 = \frac{Ma_1^2 + \frac{2}{\gamma-1}}{{\frac{2\gamma}{\gamma-1}Ma_1^2 - 1}}$$

**Pressure ratio**:
$$\frac{p_2}{p_1} = \frac{2\gamma Ma_1^2 - (\gamma-1)}{\gamma+1}$$

**Density ratio**:
$$\frac{\rho_2}{\rho_1} = \frac{(\gamma+1)Ma_1^2}{(\gamma-1)Ma_1^2 + 2}$$

**Temperature ratio**:
$$\frac{T_2}{T_1} = \frac{[2\gamma Ma_1^2 - (\gamma-1)][(\gamma-1)Ma_1^2 + 2]}{(\gamma+1)^2 Ma_1^2}$$

**Stagnation pressure ratio**:
$$\frac{p_{02}}{p_{01}} = \left[\frac{(\gamma+1)Ma_1^2}{(\gamma-1)Ma_1^2 + 2}\right]^{\gamma/(\gamma-1)} \left[\frac{\gamma+1}{2\gamma Ma_1^2 - (\gamma-1)}\right]^{1/(\gamma-1)}$$

### Shock Properties

- **Entropy increase**: $s_2 > s_1$ (irreversible process)
- **Stagnation pressure loss**: $p_{02} < p_{01}$
- **Stagnation temperature conserved**: $T_{02} = T_{01}$
- **Compression only**: $p_2 > p_1$, $\rho_2 > \rho_1$, $T_2 > T_1$
- **Deceleration**: $V_2 < V_1$

### Oblique Shocks

For oblique shocks with deflection angle $\theta$ and shock angle $\beta$:

**Shock-deflection relation**:
$$\tan \theta = 2 \cot \beta \frac{Ma_1^2 \sin^2 \beta - 1}{Ma_1^2(\gamma + \cos 2\beta) + 2}$$

**Normal Mach number**:
$$Ma_{1n} = Ma_1 \sin \beta$$

Properties across oblique shock use normal shock relations with $Ma_{1n}$.

## Expansion Waves

### Prandtl-Meyer Expansion

For supersonic flow around a convex corner, expansion occurs through a **Prandtl-Meyer fan**.

**Prandtl-Meyer function**:
$$\nu(Ma) = \sqrt{\frac{\gamma+1}{\gamma-1}} \arctan\sqrt{\frac{\gamma-1}{\gamma+1}(Ma^2-1)} - \arctan\sqrt{Ma^2-1}$$

**Property relations**:
$$\nu_2 - \nu_1 = \theta$$
$$\frac{p_2}{p_1} = \left(\frac{1 + \frac{\gamma-1}{2}Ma_1^2}{1 + \frac{\gamma-1}{2}Ma_2^2}\right)^{\gamma/(\gamma-1)}$$

### Characteristics

- **Isentropic process**: No entropy change
- **Expansion**: $p_2 < p_1$, $\rho_2 < \rho_1$, $T_2 < T_1$
- **Acceleration**: $V_2 > V_1$, $Ma_2 > Ma_1$
- **Stagnation properties conserved**

## Flow Through Nozzles

### Converging Nozzle

**Subsonic throughout**: Exit Mach number depends on pressure ratio:
$$\frac{p_e}{p_0} = \left(1 + \frac{\gamma-1}{2}Ma_e^2\right)^{-\gamma/(\gamma-1)}$$

**Choked condition**: When $p_e/p_0 = (p^*/p_0) = 0.528$, flow becomes sonic at exit.

### Converging-Diverging Nozzle

**Design condition**: Smooth acceleration to supersonic speeds
- Subsonic in converging section
- Sonic at throat ($Ma = 1$)
- Supersonic in diverging section

**Off-design conditions**:
1. **Over-expanded**: Exit pressure below design, shock outside nozzle
2. **Under-expanded**: Exit pressure above design, compression outside nozzle
3. **Shock in nozzle**: Strong shock wave inside diverging section

## Fanno Flow (Adiabatic Duct Flow)

For steady, adiabatic flow in a constant-area duct with friction:

**Governing parameter**: $4fL^*/D$ where $f$ is friction factor, $L^*$ is length to choke point.

**Relations**:
$$\frac{4fL^*}{D} = \frac{1-Ma^2}{\gamma Ma^2} + \frac{\gamma+1}{2\gamma}\ln\left[\frac{(\gamma+1)Ma^2}{2(1+\frac{\gamma-1}{2}Ma^2)}\right]$$

**Properties**:
- **Subsonic flow**: Acceleration with heating
- **Supersonic flow**: Deceleration with cooling
- **Choking**: Maximum entropy at $Ma = 1$

## Rayleigh Flow (Frictionless Heat Addition)

For steady flow in a constant-area duct with heat addition but no friction:

**Governing parameter**: $q/c_p T_0$ (heat added per unit mass)

**Relations**:
$$\frac{T_0}{T_{0^*}} = \frac{Ma^2(1+\gamma Ma^2)^2}{(\gamma+1)^2 Ma^2(1+\frac{\gamma-1}{2}Ma^2)}$$

**Properties**:
- **Subsonic flow**: Heat addition accelerates flow
- **Supersonic flow**: Heat addition decelerates flow
- **Thermal choking**: Occurs at $Ma = 1/\sqrt{\gamma}$

## Applications

### Aerospace Engineering

**Aircraft engines**:
- Inlet design for supersonic aircraft
- Turbine nozzle flows
- Afterburner analysis

**Rocket nozzles**:
- De Laval nozzle design
- Thrust optimization
- Altitude compensation

### Gas Turbines

**Compressor design**:
- Blade passage flows
- Shock formation and control
- Efficiency optimization

**Turbine analysis**:
- Expansion through blade rows
- Cooling air ejection
- Performance prediction

### Industrial Applications

**Steam turbines**:
- Nozzle and blade design
- Condensation effects
- Two-phase flow considerations

**Process equipment**:
- Pressure relief valves
- Pipeline rupture disks
- Gas metering devices

## Computational Methods

### Method of Characteristics

For supersonic flow, solve along **characteristic lines**:
$$\frac{dx}{dt} = u \pm a$$

Enables tracking of disturbances and shock formation.

### Shock-Capturing Methods

**Finite volume schemes**:
- Total variation diminishing (TVD)
- Essentially non-oscillatory (ENO)
- Weighted ENO (WENO)

**Shock detection**:
- Artificial viscosity
- Flux limiters
- Adaptive mesh refinement

### Modern CFD

**Commercial codes**:
- ANSYS Fluent
- STAR-CCM+
- OpenFOAM

**Specialized codes**:
- US3D (hypersonics)
- OVERFLOW (aerospace)
- CartesianGrid methods

## Measurement Techniques

### Pressure Measurements

**Pitot tubes**: Modified for compressible flow
$$\frac{p_0}{p} = \left(1 + \frac{\gamma-1}{2}Ma^2\right)^{\gamma/(\gamma-1)}$$

**Static pressure taps**: Minimize flow disturbance

### Optical Methods

**Schlieren photography**: Visualizes density gradients
**Shadowgraphy**: Shows shock waves and expansion fans
**Interferometry**: Quantitative density measurements

### Temperature Measurements

**Thermocouples**: Account for recovery factors
**Infrared thermography**: Non-intrusive surface measurements
**Laser diagnostics**: Advanced research techniques

## Historical Development

- **1887**: Ernst Mach first measured supersonic velocities
- **1906**: Prandtl developed boundary layer theory
- **1908**: Rayleigh analyzed flow with heat addition
- **1950s**: Development of transonic and supersonic aircraft
- **1960s**: Space program drove hypersonic research

## Learning Strategy

### Prerequisites
- Thermodynamics and ideal gas relations
- Differential equations and mathematical methods
- Basic fluid mechanics and inviscid flow theory

### Key Concepts
1. Mach number and its physical significance
2. Isentropic flow relations and stagnation properties
3. Area-velocity relationships and choked flow
4. Normal and oblique shock wave analysis
5. Prandtl-Meyer expansion theory
6. One-dimensional flow with area change, friction, or heat addition

### Problem-Solving Approach
1. Identify flow regime (subsonic, transonic, supersonic)
2. Determine relevant assumptions (isentropic, adiabatic, etc.)
3. Apply appropriate relations (isentropic, shock, expansion)
4. Use conservation laws consistently
5. Check results for physical reasonableness

Understanding compressible flow theory is essential for aerospace engineering, gas turbine design, and any application involving high-speed gas flows. The theory provides powerful tools for analyzing complex phenomena such as shock waves, expansion fans, and choked flow conditions.
