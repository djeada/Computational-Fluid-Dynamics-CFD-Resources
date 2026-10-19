# Internal Flow

## Overview

Internal flow deals with fluid motion confined within boundaries such as pipes, ducts, channels, and other enclosed passages. This is fundamental to many engineering applications including pipeline systems, HVAC design, turbomachinery, and process equipment.

## Topics Covered

### Pipe Flow Fundamentals

- **[Pipes](pipes.md)**: Comprehensive treatment of flow in circular pipes and ducts
- Laminar vs turbulent flow regimes
- Entrance effects and developing flows
- Pressure drop calculations and friction factors

### Flow Development

- Entrance length calculations
- Velocity profile development
- Boundary layer growth in ducts
- Fully developed flow characteristics

### Pressure Drop Analysis

- Major losses due to wall friction
- Minor losses at fittings and components
- Total system pressure drop calculations
- Pump and fan sizing considerations

## Mathematical Framework

### Governing Equations

**Continuity for steady flow:**

$$
\dot{m} = \rho V A = \text{constant}
$$

**Momentum equation (pipe flow):**

$$
\frac{dp}{dx} = -\tau_w \frac{P}{A} - \rho g \sin\theta
$$

**Energy equation:**

$$
h_1 + \frac{V_1^2}{2} + g z_1 = h_2 + \frac{V_2^2}{2} + g z_2 + \text{losses}
$$

### Dimensionless Parameters

**Reynolds number:**

$$
Re = \frac{\rho V D}{\mu} = \frac{V D}{\nu}
$$

**Friction factor:**

```math
f = \frac{\Delta p}{L}\, \frac{D}{\rho V^2/2}
```

**Darcy-Weisbach equation:**

$$
h_f = f \frac{L}{D} \frac{V^2}{2g}
$$

## Laminar Pipe Flow

### Velocity Profile

For fully developed laminar flow in a circular pipe:

$$
u(r) = u_{\text{max}}\left[1 - \left(\frac{r}{R}\right)^2\right]
$$

where $u_{\text{max}} = 2V_{\text{avg}}$

### Pressure Drop

**Hagen-Poiseuille equation:**

$$
\Delta p = \frac{32 \mu L V}{D^2}
$$

**Friction factor:**

$$
f = \frac{64}{Re}
$$

### Heat Transfer

**Thermal entrance length:**

```math
L_{t,\text{thermal}} = 0.05\, Re\, Pr\, D
```

**Nusselt number (constant wall temperature):**

$$
Nu = 3.66 \quad (\text{fully developed})
$$

## Turbulent Pipe Flow

### Velocity Profiles

**Power law approximation:**

$$
\frac{u}{u_{\text{max}}} = \left(\frac{y}{R}\right)^{1/n}
$$

where $n \approx 7$ for smooth pipes

**Log law (near wall):**

$$
u^+ = \frac{1}{\kappa}\ln(y^+) + B
$$

### Friction Factor Correlations

**Smooth pipes (Blasius):**

$$
f = \frac{0.316}{Re^{0.25}} \quad (Re < 10^5)
$$

**Colebrook equation (rough pipes):**

$$
\frac{1}{\sqrt{f}} = -2\log_{10}\left(\frac{\epsilon/D}{3.7} +
\frac{2.51}{Re\sqrt{f}}\right)
$$

**Moody diagram**: Graphical representation of friction factor

### Heat Transfer

**Dittus-Boelter equation:**

```math
Nu = 0.023\, Re^{0.8}\, Pr^n
```

where $n = 0.4$ (heating) or $0.3$ (cooling)

## Non-Circular Ducts

### Hydraulic Diameter

For non-circular cross-sections:

$$
D_h = \frac{4A}{P}
$$

where $A$ = cross-sectional area, $P$ = wetted perimeter

### Common Geometries

1. **Rectangular ducts**

   - Aspect ratio effects
   - Secondary flow considerations
   - Corner effects

2. **Annular passages**

   - Inner and outer diameter effects
   - Heat transfer applications
   - Concentric vs eccentric arrangements

3. **Triangular and other shapes**

   - Specialized applications
   - Manufacturing considerations
   - Flow distribution effects

## Minor Losses

### Loss Coefficients

$$
h_L = K \frac{V^2}{2g}
$$

### Common Components

1. **Sudden expansion:**

   ```math
   K = \left(1 - \frac{A_1}{A_2}\right)^2
   ```

2. **Sudden contraction:**

   ```math
   K = 0.5\left(1 - \frac{A_2}{A_1}\right)
   ```

3. **Bends and elbows:**

   - $90^\circ$ elbow: $K \approx 0.9$
   - $45^\circ$ elbow: $K \approx 0.4$

4. **Valves and fittings:**

   - Gate valve (open): $K \approx 0.15$
   - Globe valve (open): $K \approx 10$
   - Check valve: $K \approx 2.5$

### Entrance and Exit Losses

- **Sharp-edged entrance:** $K = 0.5$
- **Well-rounded entrance:** $K = 0.04$
- **Exit to reservoir:** $K = 1.0$

## System Analysis

### Network Methods

1. **Series systems:**

   ```math
   \Delta p_{\text{total}} = \sum_i \Delta p_i
   ```

2. **Parallel systems:**

   ```math
   Q_{\text{total}} = \sum_i Q_i
   ```

3. **Complex networks:**

   - Hardy Cross method
   - Node analysis techniques
   - Matrix methods

### Pump/Fan Curves

- System characteristic curves
- Operating point determination
- Pump selection and sizing
- Efficiency considerations

## Special Considerations

### Compressible Flow in Ducts

- Fanno flow (adiabatic with friction)
- Rayleigh flow (frictionless with heat addition)
- Choked flow conditions
- Pressure drop limitations

### Non-Newtonian Fluids

- Power law fluids in pipes
- Yield stress fluid considerations
- Entrance effects
- Heat transfer modifications

### Unsteady Flow

- Water hammer phenomena
- Transient pressure analysis
- Surge tank design
- Safety considerations

## Engineering Applications

### Building Services

- HVAC duct design
- Plumbing systems
- Fire protection systems
- Ventilation requirements

### Process Industries

- Pipeline networks
- Heat exchanger design
- Reactor coolant systems
- Chemical processing equipment

### Power Generation

- Steam and gas turbine systems
- Nuclear reactor cooling
- Geothermal systems
- Solar thermal applications

### Transportation

- Aircraft fuel systems
- Automotive cooling systems
- Marine piping systems
- Railroad fluid systems

## Design Procedures

### System Design Steps

1. **Flow rate determination**
2. **Pipe sizing calculations**
3. **Pressure drop analysis**
4. **Pump/fan selection**
5. **Economic optimization**
6. **Safety factor application**

### Design Standards

- ASME pipe codes
- ASHRAE duct design
- API pipeline standards
- International plumbing codes

### Optimization Considerations

- Economic pipe diameter
- Energy cost vs capital cost
- Maintenance requirements
- Environmental factors

## Computational Methods

### CFD Applications

- Complex geometry analysis
- Heat transfer calculations
- Multi-phase flow simulation
- Optimization studies

### Network Analysis Software

- PIPE-FLO and similar packages
- HVAC design software
- Process simulation tools
- Custom analysis programs

### Numerical Techniques

- Finite difference methods
- Finite volume approaches
- Pressure correction algorithms
- Turbulence modeling

## Experimental Methods

### Flow Measurement

- Velocity measurement techniques
- Flow rate measurement devices
- Pressure drop measurement
- Temperature profiling

### Visualization Techniques

- Flow pattern observation
- Heat transfer visualization
- Mixing studies
- Particle tracking

### Model Testing

- Scale model considerations
- Similarity requirements
- Data extrapolation methods
- Uncertainty analysis

## Learning Path

### Prerequisites

- Basic fluid mechanics principles
- Heat transfer fundamentals
- Mathematical analysis techniques
- Engineering economics concepts

### Core Concepts

1. Reynolds number and flow regimes
2. Friction factor and pressure drop
3. Entrance effects and flow development
4. Minor loss calculations
5. System analysis techniques

### Design Skills

1. Pipe sizing and selection
2. Pump and fan applications
3. Economic optimization
4. Safety and code compliance

### Advanced Topics

1. Complex network analysis
2. Compressible flow effects
3. Non-Newtonian fluid systems
4. Computational fluid dynamics

Understanding internal flow is essential for designing efficient fluid transport systems, from simple piping to complex industrial networks and building services.
