# Bernoulli's Equation

## Derivation and Physical Meaning

### Starting from Euler's Equation

For inviscid, incompressible flow, Euler's momentum equation is:
$$\frac{\partial \vec{V}}{\partial t} + (\vec{V} \cdot \nabla)\vec{V} = -\frac{1}{\rho}\nabla p + \vec{g}$$

### Steady Flow Along a Streamline

For steady flow ($\frac{\partial \vec{V}}{\partial t} = 0$), taking the dot product with $d\vec{s}$ along a streamline:

$$(\vec{V} \cdot \nabla)\vec{V} \cdot d\vec{s} = -\frac{1}{\rho}\nabla p \cdot d\vec{s} + \vec{g} \cdot d\vec{s}$$

Since $\vec{V} \cdot \nabla = V \frac{\partial}{\partial s}$ along a streamline:
$$V \frac{\partial V}{\partial s} ds = -\frac{1}{\rho} \frac{\partial p}{\partial s} ds + g \frac{\partial z}{\partial s} ds$$

This simplifies to:
$$V dV = -\frac{dp}{\rho} + g dz$$

Integrating along the streamline:
$$\int V dV = -\int \frac{dp}{\rho} + g \int dz$$

For constant density:
$$\frac{1}{2}V^2 = -\frac{p}{\rho} + gz + C$$

Rearranging:
$$\frac{p}{\rho} + \frac{1}{2}V^2 + gz = \text{constant along streamline}$$

## Forms of Bernoulli's Equation

### Pressure Form
$$p_1 + \frac{1}{2}\rho V_1^2 + \rho g z_1 = p_2 + \frac{1}{2}\rho V_2^2 + \rho g z_2$$

### Head Form (Hydraulics)
$$\frac{p_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{p_2}{\rho g} + \frac{V_2^2}{2g} + z_2$$

where:
- $\frac{p}{\rho g}$ = **pressure head**
- $\frac{V^2}{2g}$ = **velocity head** 
- $z$ = **elevation head**

### Energy Form
$$\frac{p}{\rho} + \frac{1}{2}V^2 + gz = \text{constant}$$

This represents mechanical energy per unit mass.

## Physical Interpretation

### Energy Conservation
Bernoulli's equation is essentially conservation of mechanical energy for a fluid particle:

- **Pressure energy**: $\frac{p}{\rho}$ (energy due to pressure forces)
- **Kinetic energy**: $\frac{1}{2}V^2$ (energy due to motion)
- **Potential energy**: $gz$ (energy due to gravity)

### Trade-offs
- **High velocity** → **low pressure** (venturi effect)
- **Low velocity** → **high pressure** (stagnation)
- **High elevation** → **low pressure** (hydrostatic effect)

## Applications

### 1. Pitot Tube

Measures flow velocity by comparing static and stagnation pressures.

**Configuration**:
- Point 1: Free stream ($V_1 = V$, $p_1 = p$)
- Point 2: Stagnation point ($V_2 = 0$, $p_2 = p_0$)

**Analysis**:
$$p + \frac{1}{2}\rho V^2 = p_0$$
$$V = \sqrt{\frac{2(p_0 - p)}{\rho}}$$

where $p_0$ is the stagnation pressure.

### 2. Venturi Meter

Measures flow rate using pressure difference across a constriction.

**Setup**:
- Section 1: Large diameter $D_1$, area $A_1$
- Section 2: Small diameter $D_2$, area $A_2$ (throat)

**Analysis**:
From continuity: $V_1 A_1 = V_2 A_2$
$$V_2 = V_1 \frac{A_1}{A_2}$$

From Bernoulli (assuming horizontal):
$$p_1 + \frac{1}{2}\rho V_1^2 = p_2 + \frac{1}{2}\rho V_2^2$$

Solving for $V_1$:
$$V_1 = \sqrt{\frac{2(p_1 - p_2)}{\rho\left[\left(\frac{A_1}{A_2}\right)^2 - 1\right]}}$$

Volume flow rate:
$$Q = A_1 V_1 = A_1 \sqrt{\frac{2(p_1 - p_2)}{\rho\left[\left(\frac{A_1}{A_2}\right)^2 - 1\right]}}$$

### 3. Orifice Flow

Flow through a small opening in a tank.

**Analysis**:
- Point 1: Free surface ($V_1 \approx 0$, $p_1 = p_{atm}$, $z_1 = h$)
- Point 2: Orifice exit ($p_2 = p_{atm}$, $z_2 = 0$)

$$p_{atm} + 0 + \rho g h = p_{atm} + \frac{1}{2}\rho V_2^2 + 0$$

**Torricelli's law**:
$$V_2 = \sqrt{2gh}$$

Actual flow includes discharge coefficient $C_d$:
$$V_{actual} = C_d\sqrt{2gh}$$

### 4. Siphon

Flow over an obstacle using atmospheric pressure.

**Critical point**: Top of siphon where pressure is lowest.
**Constraint**: Pressure cannot drop below vapor pressure.

**Maximum height**:
$$h_{max} = \frac{p_{atm} - p_{vapor}}{\rho g}$$

For water at room temperature: $h_{max} \approx 10.3$ m.

### 5. Airfoil Pressure Distribution

For flow over an airfoil (inviscid theory):
$$p = p_\infty + \frac{1}{2}\rho(V_\infty^2 - V^2)$$

**Coefficient of pressure**:
$$C_p = \frac{p - p_\infty}{\frac{1}{2}\rho V_\infty^2} = 1 - \left(\frac{V}{V_\infty}\right)^2$$

- $C_p = 1$ at stagnation points
- $C_p < 0$ where $V > V_\infty$ (upper surface)
- $C_p > 0$ where $V < V_\infty$ (lower surface)

## Limitations and Corrections

### 1. Viscous Effects

Real fluids have viscosity, leading to:
- **Energy losses** due to friction
- **Boundary layer effects**
- **Flow separation**

**Modified Bernoulli equation**:
$$\frac{p_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{p_2}{\rho g} + \frac{V_2^2}{2g} + z_2 + h_L$$

where $h_L$ is the head loss.

### 2. Compressibility Effects

For compressible flow, density varies. Modified form:
$$\int \frac{dp}{\rho} + \frac{1}{2}V^2 + gz = \text{constant}$$

For **isentropic flow** of an ideal gas:
$$\frac{\gamma}{\gamma-1} \frac{p}{\rho} + \frac{1}{2}V^2 = \text{constant}$$

### 3. Unsteady Effects

For unsteady flow, add acceleration term:
$$\frac{\partial \phi}{\partial t} + \frac{p}{\rho} + \frac{1}{2}V^2 + gz = f(t)$$

where $\phi$ is the velocity potential.

### 4. Rotating Reference Frame

In rotating systems, add centrifugal and Coriolis effects:
$$\frac{p}{\rho} + \frac{1}{2}V_{rel}^2 + gz - \frac{1}{2}\Omega^2 r^2 = \text{constant}$$

## Engineering Applications

### Hydraulic Systems

**Pipeline design**:
- Pump sizing using energy balance
- Pressure drop calculations
- Cavitation prediction

**Open channel flow**:
- Specific energy concept
- Critical flow conditions
- Hydraulic jumps

### Aerodynamics

**Wind tunnel testing**:
- Pressure measurements
- Velocity calibration
- Force calculations

**Aircraft performance**:
- Stall speed calculations
- Pressure altitude effects
- Pitot-static systems

### Process Engineering

**Flow measurement**:
- Venturi meters
- Orifice plates
- Flow nozzles

**Pump and turbine analysis**:
- Head calculations
- Efficiency definitions
- Performance curves

## Experimental Verification

### Pressure Measurements

**Static pressure taps**:
- Flush with surface
- Minimal flow disturbance
- Connected to manometers or transducers

**Pitot probes**:
- Measure stagnation pressure
- Combine with static pressure for velocity
- Corrections for viscous effects

### Velocity Measurements

**Pitot-static tubes**:
$$V = \sqrt{\frac{2(p_0 - p)}{\rho}}$$

**Hot-wire anemometry**:
- Measures velocity directly
- High frequency response
- Calibration using Bernoulli principle

### Flow Visualization

**Smoke/dye injection**:
- Visualize streamlines
- Confirm inviscid assumptions
- Identify separation regions

## Problem-Solving Strategy

### 1. Identify the Flow Type
- Steady vs. unsteady
- Compressible vs. incompressible
- Viscous vs. inviscid
- Internal vs. external

### 2. Choose Reference Points
- Select two points along a streamline
- Ensure Bernoulli assumptions are valid
- Include all relevant energy terms

### 3. Apply Conservation Laws
- **Continuity equation**: $\rho_1 A_1 V_1 = \rho_2 A_2 V_2$
- **Bernoulli equation**: Energy balance
- **Force balance**: If needed for pressure forces

### 4. Account for Losses
- Friction losses in pipes
- Form losses at fittings
- Separation losses at expansions

### 5. Check Results
- Physical reasonableness
- Units consistency
- Limiting cases

## Common Mistakes

1. **Applying between different streamlines** without justification
2. **Ignoring viscous effects** in high Reynolds number flows
3. **Using incompressible form** for high Mach number flows
4. **Neglecting elevation changes** in vertical flows
5. **Assuming steady flow** for rapidly changing conditions

## Advanced Topics

### Generalized Bernoulli Equation

For irrotational flow (not necessarily steady):
$$\frac{\partial \phi}{\partial t} + \frac{p}{\rho} + \frac{1}{2}|\nabla \phi|^2 + gz = F(t)$$

### Crocco's Theorem

For steady flow with entropy gradients:
$$T \nabla S = \vec{\omega} \times \vec{V}$$

Relates vorticity to entropy gradients in compressible flow.

### Kelvin's Circulation Theorem

For inviscid, barotropic flow:
$$\frac{D\Gamma}{Dt} = 0$$

Circulation is conserved following fluid particles.

Bernoulli's equation remains one of the most useful tools in fluid mechanics, providing insight into the fundamental trade-offs between kinetic, potential, and pressure energy in flowing fluids. Understanding its derivation, applications, and limitations is essential for any engineer working with fluid systems.
