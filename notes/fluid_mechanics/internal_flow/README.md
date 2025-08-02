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
```
ṁ = ρVA = constant
```

**Momentum equation (pipe flow):**
```
dp/dx = -τw(P/A) - ρg sin θ
```

**Energy equation:**
```
h₁ + V₁²/2 + gz₁ = h₂ + V₂²/2 + gz₂ + losses
```

### Dimensionless Parameters

**Reynolds number:**
```
Re = ρVD/μ = VD/ν
```

**Friction factor:**
```
f = (Δp/L) × (D/ρV²/2)
```

**Darcy-Weisbach equation:**
```
hf = f(L/D)(V²/2g)
```

## Laminar Pipe Flow

### Velocity Profile
For fully developed laminar flow in a circular pipe:
```
u(r) = umax[1 - (r/R)²]
```
where umax = 2Vavg

### Pressure Drop
**Hagen-Poiseuille equation:**
```
Δp = (32μLV)/(D²)
```

**Friction factor:**
```
f = 64/Re
```

### Heat Transfer
**Thermal entrance length:**
```
Lt,thermal = 0.05 Re Pr D
```

**Nusselt number (constant wall temperature):**
```
Nu = 3.66 (fully developed)
```

## Turbulent Pipe Flow

### Velocity Profiles
**Power law approximation:**
```
u/umax = (y/R)^(1/n)
```
where n ≈ 7 for smooth pipes

**Log law (near wall):**
```
u⁺ = (1/κ)ln(y⁺) + B
```

### Friction Factor Correlations
**Smooth pipes (Blasius):**
```
f = 0.316/Re^0.25 (Re < 10⁵)
```

**Colebrook equation (rough pipes):**
```
1/√f = -2log₁₀(ε/D/3.7 + 2.51/(Re√f))
```

**Moody diagram**: Graphical representation of friction factor

### Heat Transfer
**Dittus-Boelter equation:**
```
Nu = 0.023 Re^0.8 Pr^n
```
where n = 0.4 (heating) or 0.3 (cooling)

## Non-Circular Ducts

### Hydraulic Diameter
For non-circular cross-sections:
```
Dh = 4A/P
```
where A = cross-sectional area, P = wetted perimeter

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
```
hL = K(V²/2g)
```

### Common Components
1. **Sudden expansion:**
   ```
   K = (1 - A₁/A₂)²
   ```

2. **Sudden contraction:**
   ```
   K = 0.5(1 - A₂/A₁)
   ```

3. **Bends and elbows:**
   - 90° elbow: K ≈ 0.9
   - 45° elbow: K ≈ 0.4

4. **Valves and fittings:**
   - Gate valve (open): K ≈ 0.15
   - Globe valve (open): K ≈ 10
   - Check valve: K ≈ 2.5

### Entrance and Exit Losses
- **Sharp-edged entrance:** K = 0.5
- **Well-rounded entrance:** K = 0.04
- **Exit to reservoir:** K = 1.0

## System Analysis

### Network Methods
1. **Series systems:**
   ```
   Δptotal = Σ Δpi
   ```

2. **Parallel systems:**
   ```
   Qtotal = Σ Qi
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
