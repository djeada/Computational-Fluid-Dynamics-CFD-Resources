# Energy Equation in Fluid Mechanics

## Overview

The energy equation represents conservation of energy in fluid flow and is essential for:

- **Compressible flow analysis** (temperature and density coupling)
- **Heat transfer problems** (thermal boundary layers)
- **Combustion and reacting flows** (chemical energy conversion)
- **Turbomachinery design** (work transfer and efficiency)

## Derivation from First Law of Thermodynamics

### General Energy Balance

For a fluid element, the first law of thermodynamics states:

$$
\frac{DE}{Dt} = \dot{Q} - \dot{W}
$$

where:

- $E$ = total energy per unit mass
- $\dot{Q}$ = heat addition rate per unit mass
- $\dot{W}$ = work done by the fluid per unit mass

### Total Energy Components

$$
E = e + \frac{1}{2}V^2 + gz
$$

where:

- $e$ = specific internal energy
- $\frac{1}{2}V^2$ = kinetic energy per unit mass
- $gz$ = gravitational potential energy per unit mass

### Heat Addition

Heat addition occurs through:

1. **Conduction**: $\nabla \cdot (k \nabla T)$
2. **Radiation**: $\dot{q}_{rad}$
3. **Chemical reactions**: $\dot{q}_{chem}$
4. **Viscous dissipation**: $\Phi$

### Work Terms

Work is done by:

1. **Pressure forces**: $\nabla \cdot (p \vec{V})$
2. **Viscous stresses**: $\nabla \cdot (\boldsymbol{\tau} \cdot \vec{V})$
3. **Gravitational forces**: $\rho \vec{g} \cdot \vec{V}$

## Conservative Form

### Total Energy Equation

$$
\frac{\partial (\rho E)}{\partial t} + \nabla \cdot (\rho E \vec{V}) = -\nabla \cdot
(p \vec{V}) + \nabla \cdot (\boldsymbol{\tau} \cdot \vec{V}) + \nabla \cdot
(k \nabla T) + \rho \dot{q} + \rho \vec{g} \cdot \vec{V}
$$

This can be rewritten as:

$$
\frac{\partial (\rho E)}{\partial t} + \nabla \cdot [(\rho E + p)\vec{V}] = \nabla \cdot
(\boldsymbol{\tau} \cdot \vec{V}) + \nabla \cdot (k \nabla T) + \rho \dot{q} + \rho
\vec{g} \cdot \vec{V}
$$

In these two equations gravity enters through the work term $\rho \vec{g} \cdot \vec{V}$, so here $E = e + \frac{1}{2}V^2$. If the potential energy $gz$ is included in $E$ (as in the definition above), the term $\rho \vec{g} \cdot \vec{V}$ must be dropped, otherwise gravity is counted twice.

### Enthalpy Form

Introducing specific enthalpy $h = e + p/\rho$:

$$
\rho \frac{DH}{Dt} = \frac{\partial p}{\partial t} + \nabla \cdot
(\boldsymbol{\tau} \cdot \vec{V}) + \nabla \cdot (k \nabla T) + \rho \dot{q}
$$

where $H = h + \frac{1}{2}V^2 + gz$ is total enthalpy (steady gravitational field).

## Internal Energy Equation

### Derivation

Subtracting the mechanical energy equation from the total energy equation:

$$
\rho \frac{De}{Dt} = -p \nabla \cdot \vec{V} + \nabla \cdot (k \nabla T) + \Phi + \rho
\dot{q}
$$

### Physical Interpretation

- **$-p \nabla \cdot \vec{V}$**: Compression work (positive for compression)
- **$\nabla \cdot (k \nabla T)$**: Heat conduction
- **$\Phi$**: Viscous dissipation (always positive)
- **$\rho \dot{q}$**: Heat sources/sinks

### Viscous Dissipation Function

For a Newtonian fluid:

$$
\Phi = \boldsymbol{\tau}: \nabla \vec{V} = \mu
\left[2\left(\frac{\partial u}{\partial x}\right)^2 +
2\left(\frac{\partial v}{\partial y}\right)^2 +
2\left(\frac{\partial w}{\partial z}\right)^2 + \left(\frac{\partial u}{\partial y} +
\frac{\partial v}{\partial x}\right)^2 + \left(\frac{\partial u}{\partial z} +
\frac{\partial w}{\partial x}\right)^2 + \left(\frac{\partial v}{\partial z} +
\frac{\partial w}{\partial y}\right)^2\right] -
\frac{2}{3}\mu\left(\nabla \cdot \vec{V}\right)^2
$$

## Temperature Equation

### For Ideal Gas

Using the relation $de = c_v dT$ for an ideal gas:

$$
\rho c_v \frac{DT}{Dt} = -p \nabla \cdot \vec{V} + \nabla \cdot (k \nabla T) + \Phi +
\rho \dot{q}
$$

### Simplified Forms

**For incompressible flow** ($\nabla \cdot \vec{V} = 0$):

$$
\rho c_p \frac{DT}{Dt} = \nabla \cdot (k \nabla T) + \Phi + \rho \dot{q}
$$

**For constant properties**:

$$
\frac{DT}{Dt} = \alpha \nabla^2 T + \frac{\Phi}{\rho c_p} + \frac{\dot{q}}{c_p}
$$

where $\alpha = k/(\rho c_p)$ is thermal diffusivity.

## Enthalpy Equation

### Substantial Derivative Form

$$
\rho \frac{Dh}{Dt} = \frac{Dp}{Dt} + \nabla \cdot (k \nabla T) + \Phi + \rho \dot{q}
$$

### For Ideal Gas

Using $h = c_p T$:

$$
\rho c_p \frac{DT}{Dt} = \frac{Dp}{Dt} + \nabla \cdot (k \nabla T) + \Phi + \rho \dot{q}
$$

### Stagnation Enthalpy

For flow without heat conduction, heat sources, or body forces:

$$
\rho \frac{D}{Dt}\left(h + \frac{1}{2}V^2\right) = \frac{\partial p}{\partial t} +
\nabla \cdot (\boldsymbol{\tau} \cdot \vec{V})
$$

For steady, inviscid flow: $h_0 = h + \frac{1}{2}V^2 = \text{constant}$

## Boundary Conditions

### Wall Boundary Conditions

**Isothermal wall**: $T = T_w$

**Adiabatic wall**: $\frac{\partial T}{\partial n} = 0$

**Heat flux specified**: $k \frac{\partial T}{\partial n} = q_w$

**Convective boundary**: $k \frac{\partial T}{\partial n} = h(T_\infty - T_w)$

### Inlet/Outlet Conditions

**Specified temperature**: $T = T_{inlet}$

**Specified enthalpy**: $h = h_{inlet}$

**Adiabatic**: Total temperature specified

## Dimensional Analysis

### Energy Equation Scaling

Characteristic scales:

- Length: $L$
- Velocity: $U$
- Temperature difference: $\Delta T$
- Density: $\rho$

### Dimensionless Groups

**Peclet number**: $Pe = \frac{UL}{\alpha} = Re \cdot Pr$

**Prandtl number**: $Pr = \frac{\nu}{\alpha} = \frac{\mu c_p}{k}$

**Eckert number**: $Ec = \frac{U^2}{c_p \Delta T}$

**Brinkman number**: $Br = \frac{\mu U^2}{k \Delta T} = Pr \cdot Ec$

### Dimensionless Energy Equation

```math
\frac{D\Theta}{Dt^*} = \frac{1}{Pe} \nabla^{*2} \Theta + \frac{Ec}{Re} \Phi^* +
\dot{Q}^*
```

where $\Theta = (T - T_\infty)/\Delta T$ is dimensionless temperature, $t^* = tU/L$, $\Phi^* = \Phi L^2/(\mu U^2)$, and the dissipation coefficient $Ec/Re$ equals $Br/Pe$.

## Special Cases and Approximations

### Low-Speed Flow (Ma → 0)

**Incompressible energy equation**:

$$
\rho c_p \frac{DT}{Dt} = \nabla \cdot (k \nabla T) + \Phi + \rho \dot{q}
$$

**Boussinesq approximation**: For natural convection

$$
\rho = \rho_0[1 - \beta(T - T_0)]
$$

### High-Speed Flow

**Compressible effects dominant**:

- Coupling with momentum equations
- Shock wave heating
- Viscous heating becomes important

### Boundary Layer Approximation

**Thermal boundary layer**:

$$
u \frac{\partial T}{\partial x} + v \frac{\partial T}{\partial y} = \alpha
\frac{\partial^2 T}{\partial y^2} +
\frac{\nu}{c_p}\left(\frac{\partial u}{\partial y}\right)^2
$$

## Numerical Methods

### Finite Difference Methods

**Explicit schemes**: Forward Euler, Runge-Kutta

$$
T_i^{n+1} = T_i^n + \Delta t
\left[\alpha \frac{T_{i+1}^n - 2T_i^n + T_{i-1}^n}{(\Delta x)^2} + S_i^n\right]
$$

**Implicit schemes**: Backward Euler, Crank-Nicolson

$$
T_i^{n+1} - \Delta t \alpha
\frac{T_{i+1}^{n+1} - 2T_i^{n+1} + T_{i-1}^{n+1}}{(\Delta x)^2} = T_i^n + \Delta t
S_i^{n+1}
$$

### Finite Volume Methods

**Control volume discretization**:

$$
\frac{\partial (\rho c_p T)}{\partial t} + \nabla \cdot (\rho c_p T \vec{V}) = \nabla
\cdot (k \nabla T) + S
$$

**Convection-diffusion equation**: Special attention to numerical diffusion

### Finite Element Methods

**Weak formulation**:

$$
\int_\Omega w \rho c_p \frac{\partial T}{\partial t} d\Omega + \int_\Omega \nabla w
\cdot (k \nabla T) d\Omega = \int_\Omega w S d\Omega + \int_{\partial \Omega} w q_n
d\Gamma
$$

## Applications

### Heat Transfer Problems

**Forced convection**: Flow over heated surfaces

$$
Nu = f(Re, Pr)
$$

**Natural convection**: Buoyancy-driven flows

$$
Nu = f(Ra, Pr)
$$

**Mixed convection**: Combined forced and natural

$$
Nu = f(Re, Gr, Pr)
$$

### Compressible Flow Applications

**Nozzle flows**: Temperature variation with expansion/compression

**Shock waves**: Temperature jump across normal shocks:

$$
\frac{T_2}{T_1} = \frac{[2\gamma Ma_1^2 - (\gamma-1)][(\gamma-1)Ma_1^2 + 2]}{(\gamma+1)^2 Ma_1^2}
$$

**Atmospheric entry**: Extreme heating due to compression

### Turbomachinery

**Gas turbines**: Work extraction and heat addition

$$
W = c_p(T_{03} - T_{04})
$$

**Compressors**: Temperature rise due to compression

$$
T_{02}/T_{01} = \left(p_{02}/p_{01}\right)^{(\gamma-1)/\gamma}
$$

### Combustion Systems

**Energy release**: Chemical energy to thermal energy

$$
\dot{q}_{chem} = -\sum_i h_{f,i} \dot{\omega}_i
$$

**Flame propagation**: Coupling of energy and species equations

## Advanced Topics

### Turbulent Energy Equation

**Reynolds-averaged**:

$$
\rho c_p \frac{D\bar{T}}{Dt} = \nabla \cdot (k \nabla \bar{T}) - \nabla \cdot
\overline{\rho c_p \vec{v}' T'} + \bar{\Phi} + \rho \dot{q}
$$

**Turbulent heat flux**: $\overline{\rho c_p \vec{v}' T'}$ requires modeling

**Turbulent Prandtl number**: $Pr_t = \nu_t/\alpha_t$

### Non-Newtonian Fluids

**Modified viscous dissipation**: Different constitutive relations

**Viscoelastic effects**: Additional energy storage mechanisms

### Multiphase Flows

**Phase change**: Latent heat effects

$$
\rho \frac{DH}{Dt} = \rho L \frac{D\alpha}{Dt}
$$

**Interface tracking**: Energy conservation across interfaces

## Experimental Techniques

### Temperature Measurement

**Thermocouples**: Point measurements with correction for recovery factor

**Infrared thermography**: Surface temperature distributions

**Laser-induced fluorescence**: Non-intrusive volumetric measurements

### Heat Transfer Measurement

**Heat flux sensors**: Direct measurement of surface heat transfer

**Transient techniques**: Liquid crystals, heat thin films

**Calorimetric methods**: Energy balance approach

## Historical Development

- **1822**: Fourier derived heat conduction equation
- **1845**: Stokes formulated viscous stress tensor
- **1895**: Reynolds developed turbulent energy equation
- **1904**: Prandtl introduced boundary layer energy equation
- **1930s**: Development of high-speed flow energy analysis

## Learning Strategy

### Prerequisites

- Thermodynamics and heat transfer fundamentals
- Vector calculus and differential equations
- Basic fluid mechanics and conservation laws

### Key Concepts

1. Energy conservation and first law of thermodynamics
2. Internal energy vs. enthalpy formulations
3. Viscous dissipation and its significance
4. Boundary conditions for thermal problems
5. Coupling with momentum equations in compressible flow
6. Dimensionless parameters for energy transport

### Problem-Solving Approach

1. Identify the appropriate form of energy equation
2. Determine relevant assumptions and simplifications
3. Apply proper boundary and initial conditions
4. Consider coupling with other conservation equations
5. Validate results against physical expectations

The energy equation is fundamental to understanding thermal effects in fluid flow and is essential for advanced applications in aerospace, energy systems, and process engineering.

## Related Scripts

- [Rayleigh-Bénard Convection Simulation](../../../scripts/simulations/rayleigh_benard_convection/): simulates Rayleigh-Bénard convection, the buoyancy-driven flow in a fluid layer heated from below and cooled from above, and draws the temperature field in real time with Pygame.

## Exercises

**Exercise 1.** In the internal energy equation $`\rho\, De/Dt = -p\nabla\cdot\vec{V} + \nabla\cdot(k\nabla T) + \Phi + \rho\dot{q}`$, which terms are reversible and which are irreversible? Why is $\Phi$ never negative?

<details>
<summary>Answer</summary>

$-p\nabla\cdot\vec{V}$ is reversible compression or expansion work: it changes sign between compression and expansion. $\Phi$ is irreversible, because it converts mechanical energy into heat in every case. Heat conduction $\nabla\cdot(k\nabla T)$ is irreversible when temperature gradients are present, and $\rho\dot{q}$ is an external source.

For a Newtonian fluid, $\Phi$ is a sum of squares of strain-rate combinations multiplied by $\mu$. Under Stokes' hypothesis it equals $2\mu$ times the squared deviatoric strain rate, so $\Phi \ge 0$, with equality only in rigid-body motion.

</details>

**Exercise 2.** In Couette flow, $u = Uy/h$, of oil ($\mu = 0.29$ Pa s, $k = 0.145$ W/(m K)) with $U = 2$ m/s and $h = 0.5$ mm, both walls are held at $T_w$. (a) Compute $\Phi$. (b) Solve the steady energy equation $`0 = k\, d^2T/dy^2 + \Phi`$ for the maximum temperature rise. (c) Check that the dissipation per unit wall area equals the power $\tau U$ supplied by the moving plate.

<details>
<summary>Answer</summary>

(a) $\Phi = \mu (du/dy)^2 = 0.29 \times (2/0.0005)^2 = 4.64 \times 10^6$ W/m³.

(b) With $T(0) = T(h) = T_w$, the solution is $T - T_w = \frac{\Phi}{2k}y(h - y)$. The maximum is at mid-gap:

```math
\Delta
T_{max} = \frac{\Phi h^2}{8k} = \frac{4.64 \times 10^6 \times (5 \times 10^{-4})^2}{8 \times 0.145} = 1.0 \text{ K}
```

(c) $\Phi h = 2320$ W/m², and $\tau U = \mu (U/h) U = 0.29 \times 4000 \times 2 = 2320$ W/m². All the work done by the moving plate is dissipated as heat.

</details>

**Exercise 3.** Air ($c_p = 1005$ J/(kg K)) at $T = 250$ K flows at $V = 250$ m/s. Using $h_0 = c_p T + V^2/2 = $ constant for steady adiabatic flow, find the stagnation temperature.

<details>
<summary>Answer</summary>

$T_0 = T + V^2/(2c_p) = 250 + 250^2/(2 \times 1005) = 250 + 31.1 = 281.1$ K.

This is roughly the temperature an adiabatic probe facing the flow would read, apart from a recovery-factor correction.

</details>

**Exercise 4.** Water ($\nu = 1.0 \times 10^{-6}$ m²/s, $\alpha = 1.43 \times 10^{-7}$ m²/s, $c_p = 4182$ J/(kg K)) flows at $U = 1$ m/s past a body of size $L = 0.1$ m with $\Delta T = 10$ K. Compute $Re$, $Pr$, $Pe$, $Ec$ and $Br$, and decide whether viscous heating matters.

<details>
<summary>Answer</summary>

- $Re = UL/\nu = 1.0 \times 10^5$
- $Pr = \nu/\alpha = 7.0$
- $Pe = Re \cdot Pr = 7.0 \times 10^5$
- $Ec = U^2/(c_p\Delta T) = 1/(4182 \times 10) = 2.39 \times 10^{-5}$
- $Br = Pr \cdot Ec = 1.67 \times 10^{-4}$

$Ec$ and $Br$ are tiny, so viscous dissipation is negligible compared with conduction and convection. It becomes important in high-speed gas flows, where $Ec \sim 1$, and in thin films of very viscous fluid.

</details>

**Exercise 5.** Apply the explicit finite-difference scheme from the note (with $S = 0$) to water ($\alpha = 1.43 \times 10^{-7}$ m²/s) on a grid with $\Delta x = 1$ mm. (a) What is the largest stable time step? (b) With $\Delta t = 2$ s and neighbouring temperatures $T_{i-1}^n = 20$ °C, $T_i^n = 30$ °C and $T_{i+1}^n = 20$ °C, compute $T_i^{n+1}$.

<details>
<summary>Answer</summary>

(a) Stability requires $r = \alpha\Delta t/\Delta x^2 \le 1/2$, so $\Delta t \le \Delta x^2/(2\alpha) = 10^{-6}/(2.86 \times 10^{-7}) = 3.50$ s.

(b) $r = 1.43 \times 10^{-7} \times 2/10^{-6} = 0.286$, and

```math
T_i^{n+1} = T_i^n + r\,(T_{i+1}^n - 2T_i^n + T_{i-1}^n) = 30 + 0.286 \times
(20 - 60 + 20) = 24.28\ ^\circ \text{C}
```

The hot spot cools toward its neighbours, as diffusion should.

</details>

## References

- F. M. White, *Viscous Fluid Flow*, 3rd ed., McGraw-Hill, 2006.
- R. B. Bird, W. E. Stewart, E. N. Lightfoot, *Transport Phenomena*, 2nd ed., Wiley, 2002.
- T. L. Bergman, A. S. Lavine, F. P. Incropera, D. P. DeWitt, *Fundamentals of Heat and Mass Transfer*, 7th ed., Wiley, 2011.
- J. D. Anderson, *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003.
