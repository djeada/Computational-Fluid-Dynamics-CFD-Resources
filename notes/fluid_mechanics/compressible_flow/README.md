# Compressible Flow Theory

## Overview

Compressible flow is flow in which density changes are large enough to affect the velocity, pressure and temperature fields. This occurs with:

- **High velocities**: Mach number $Ma > 0.3$, where density changes exceed about 5%
- **Large pressure or temperature differences**: for example gas pipelines, combustors and blow-down tanks
- **High-speed phenomena**: shock waves and expansion fans
- **Gas dynamics**: supersonic and hypersonic flows

## Contents

| Page | What it covers |
| --- | --- |
| [Thermodynamics of Compressible Flow](thermodynamics.md) | Calorically perfect gas, internal energy and enthalpy, first and second laws, entropy change, isentropic relations, stagnation conditions |
| [Speed of Sound and Mach Number](speed_of_sound.md) | Derivation of $a = \sqrt{\gamma R T}$ from a weak pressure wave, Mach number and flow regimes, Mach cone, the $Ma \approx 0.3$ compressibility criterion |
| [Isentropic Flow](isentropic_flow.md) | Stagnation-to-static ratios, area–Mach relation, converging and converging–diverging nozzles, choking, over- and under-expanded operation |
| [Shock Waves and Expansion Fans](shock_waves.md) | Normal shocks (Rankine–Hugoniot), entropy rise and total-pressure loss, oblique shocks ($\theta$–$`\beta`$–$`M`$), Prandtl–Meyer expansion fans |
| [Fanno and Rayleigh Flow](rayleigh_fanno.md) | Adiabatic duct flow with friction, frictionless flow with heat addition, frictional and thermal choking, $T$–$`s`$ diagrams |

A suggested reading order is the order of the table.

## Fundamental Concepts

### Compressibility Effects

**Density variation**: Unlike incompressible flow, where $\rho = \text{constant}$, compressible flow has

$$
\frac{D\rho}{Dt} \neq 0
$$

**Speed of sound**: the speed at which small pressure disturbances propagate. For an ideal gas it is

$$
a = \sqrt{\left(\frac{\partial p}{\partial \rho}\right)_s} = \sqrt{\gamma R T}
$$

**Mach number**: the ratio of flow speed to sound speed,

$$
Ma = \frac{V}{a}
$$

Along a streamline in isentropic flow, $`d\rho/\rho = -Ma^2\, dV/V`$. The derivation, the flow regimes and the Mach cone are in [speed_of_sound.md](speed_of_sound.md).

### Thermodynamic Relations

Compressible-flow theory normally uses a calorically perfect gas: $p = \rho R T$, $c_p - c_v = R$, $\gamma = c_p/c_v$. For air $\gamma \approx 1.4$ and $R \approx 287$ J/(kg K). Along an isentrope

$$
\frac{T_2}{T_1} = \left(\frac{p_2}{p_1}\right)^{(\gamma-1)/\gamma},
\qquad \frac{\rho_2}{\rho_1} = \left(\frac{p_2}{p_1}\right)^{1/\gamma}
$$

Entropy change, stagnation conditions and the limits of the perfect-gas model are covered in [thermodynamics.md](thermodynamics.md).

## Governing Equations

### Conservation Laws

#### Continuity Equation

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{V}) = 0
$$

#### Momentum Equation

$$
\frac{\partial (\rho \vec{V})}{\partial t} + \nabla \cdot
(\rho \vec{V} \vec{V}) = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \vec{g}
$$

#### Energy Equation

$$
\frac{\partial E}{\partial t} + \nabla \cdot ((E + p)\vec{V}) = \nabla \cdot
(\boldsymbol{\tau} \cdot \vec{V}) + \nabla \cdot (k \nabla T) + \rho \vec{g} \cdot
\vec{V}
$$

where $E = \rho(e + \frac{1}{2}V^2)$ is total energy per unit volume. See [continuity.md](../governing_equations/continuity.md), [energy.md](../governing_equations/energy.md) and [equation_of_state.md](../governing_equations/equation_of_state.md) for derivations.

### One-Dimensional Flow

For steady, quasi-one-dimensional flow with area variation:

**Continuity**: $\rho V A = \text{constant}$

**Momentum**: $\rho V \frac{dV}{dx} = -\frac{dp}{dx}$ (inviscid)

**Energy**: $h + \frac{1}{2}V^2 = h_0 = \text{constant}$ (adiabatic, no shaft work)

where $h = c_p T$ is specific enthalpy.

## Key Results at a Glance

### Isentropic Flow

$$
\frac{T_0}{T} = 1 + \frac{\gamma-1}{2}Ma^2,
\qquad \frac{p_0}{p} = \left(1 + \frac{\gamma-1}{2}Ma^2\right)^{\gamma/(\gamma-1)}
$$

$$
\frac{dA}{A} = \left(Ma^2 - 1\right) \frac{dV}{V}
$$

- Subsonic flow accelerates in a converging duct, and supersonic flow accelerates in a diverging duct.
- $Ma = 1$ can occur only at a throat.
- Every area ratio $A/A^* > 1$ has one subsonic and one supersonic solution.
- For air at the sonic state, $`T^*/T_0 = 0.8333`$, $`p^*/p_0 = 0.5283`$ and $\rho^*/\rho_0 = 0.6339$.

Full treatment, including choked mass flow and nozzle operating regimes: [isentropic_flow.md](isentropic_flow.md).

### Nozzles

- A **converging nozzle** chokes when $p_b/p_0 \le 0.5283$ (air). The exit then stays sonic and the mass flow no longer depends on back pressure.
- A **converging–diverging nozzle** is **over-expanded** when the design exit pressure is below the back pressure ($p_e < p_b$). Oblique shocks form at the exit, and at higher back pressures a normal shock moves inside the nozzle.
- It is **under-expanded** when the exit pressure is above the back pressure ($p_e > p_b$). The flow keeps expanding outside the nozzle through expansion fans.

See [isentropic_flow.md](isentropic_flow.md).

### Shock Waves and Expansion Fans

- Normal shocks take supersonic flow to subsonic flow. They raise $p$, $\rho$, $T$ and entropy, conserve $T_0$, and reduce $p_0$. At $Ma_1 = 2$: $Ma_2 = 0.5774$, $p_2/p_1 = 4.5$, $p_{02}/p_{01} = 0.7209$.
- Expansion shocks would decrease entropy and cannot exist.
- Oblique shocks follow the $\theta$–$`\beta`$–$`M`$ relation and have weak and strong solutions. Above the maximum deflection angle the shock detaches.
- Convex corners produce isentropic Prandtl–Meyer fans with $\nu(Ma_2) = \nu(Ma_1) + \theta$.

See [shock_waves.md](shock_waves.md).

### Fanno and Rayleigh Flow

- **Fanno flow** (adiabatic, friction): friction drives $Ma$ toward 1. Subsonic flow accelerates while its static temperature *falls*, and supersonic flow decelerates while its temperature rises. The duct chokes when its length reaches $`L^*`$, given by $`4fL^*/D`$ with $f$ the Fanning friction factor.
- **Rayleigh flow** (frictionless, heat addition): heating drives $Ma$ toward 1 and always lowers $p_0$. **Thermal choking occurs at $Ma = 1$**, where $T_0$ reaches its maximum $T_0^*$. The point $Ma = 1/\sqrt{\gamma}$ is where the static temperature peaks.

See [rayleigh_fanno.md](rayleigh_fanno.md).

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
- Gas metering devices (choked nozzles and sonic venturis)

## Computational Methods

### Method of Characteristics

For one-dimensional unsteady flow, information travels along **characteristic lines**

$$
\frac{dx}{dt} = u \pm a
$$

In steady two-dimensional supersonic flow the characteristics are Mach lines inclined at $\pm\mu$ to the local flow direction. The method tracks disturbances and is used to design supersonic nozzle contours.

### Shock-Capturing Methods

**Finite volume schemes**:

- Total variation diminishing (TVD)
- Essentially non-oscillatory (ENO)
- Weighted ENO (WENO)

**Techniques for handling shocks**:

- Artificial viscosity
- Flux limiters
- Adaptive mesh refinement near discontinuities

### Modern CFD

**Commercial and open-source codes**:

- ANSYS Fluent
- STAR-CCM+
- OpenFOAM

**Specialized codes**:

- US3D (hypersonics)
- OVERFLOW (aerospace)

## Measurement Techniques

### Pressure Measurements

**Pitot tubes**: In **subsonic** flow the probe measures the isentropic stagnation pressure:

$$
\frac{p_0}{p} = \left(1 + \frac{\gamma-1}{2}Ma^2\right)^{\gamma/(\gamma-1)}
$$

In **supersonic** flow a bow shock stands in front of the probe, and the Rayleigh pitot-tube formula must be used instead (see [shock_waves.md](shock_waves.md)).

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

- **1870s–1880s**: Rankine (1870) and Hugoniot (1887–1889) derive the jump conditions across a shock
- **1887**: Ernst Mach and Peter Salcher photograph shock waves around supersonic projectiles
- **1908**: Theodor Meyer's dissertation under Prandtl gives the theory of supersonic expansion (Prandtl–Meyer flow)
- **1947**: First piloted supersonic flight (Bell X-1)
- **1950s–1960s**: Supersonic aircraft and the space program drive transonic, supersonic and hypersonic research

## Learning Strategy

### Prerequisites

- Thermodynamics and ideal gas relations
- Differential equations and mathematical methods
- Basic fluid mechanics and inviscid flow theory

### Key Concepts

1. Mach number and its physical significance ([speed_of_sound.md](speed_of_sound.md))
2. Isentropic flow relations and stagnation properties ([thermodynamics.md](thermodynamics.md), [isentropic_flow.md](isentropic_flow.md))
3. Area-velocity relationships and choked flow ([isentropic_flow.md](isentropic_flow.md))
4. Normal and oblique shock wave analysis ([shock_waves.md](shock_waves.md))
5. Prandtl-Meyer expansion theory ([shock_waves.md](shock_waves.md))
6. One-dimensional flow with friction or heat addition ([rayleigh_fanno.md](rayleigh_fanno.md))

### Problem-Solving Approach

1. Identify flow regime (subsonic, transonic, supersonic)
2. Determine relevant assumptions (isentropic, adiabatic, etc.)
3. Apply appropriate relations (isentropic, shock, expansion)
4. Use conservation laws consistently
5. Check results for physical reasonableness (for example, entropy must not decrease in adiabatic flow)

Understanding compressible flow theory is essential for aerospace engineering, gas turbine design, and any application involving high-speed gas flows. The theory provides powerful tools for analyzing complex phenomena such as shock waves, expansion fans, and choked flow conditions.
