# Fluid Loading on Structures

These notes treat the loads that fluids exert on structures and the response they cause, from hydrostatic pressure on a gate to the coupled simulation of a flexible structure in water. They start with the components of a fluid load, the coefficients and dimensionless groups that describe it and the choice between one-way and two-way coupling, then cover pressure forces and the integration of CFD surface fields, wind and wave loading, flow-induced vibrations and hydroelasticity, and end with the numerical methods that couple a flow solver to a structural solver.

## Table of Contents

### 1. [Fluid Loading on Structures](./intro.md)

Pressure, viscous, inertia and motion-dependent load components, force and moment coefficients, the groups $Re$, $St$, KC, $Fr$, $U_r$, $m^*$ and $Sc$, dynamic amplification, and when the structure's motion feeds back into the flow.

### 2. [Pressure Forces on Structures](./pressure_forces.md)

Hydrostatic forces on plane and curved surfaces and their centres of pressure, buoyancy and floating stability, the pressure coefficient, and the integration of a surface pressure and shear field into forces and moments.

### 3. [Wind Loading on Structures](./wind_loading.md)

Log-law and power-law profiles of the atmospheric boundary layer, turbulence and gusts, pressure coefficients on buildings, Davenport's gust factor, vortex shedding across the wind and galloping.

### 4. [Wave Loading on Offshore Structures](./wave_loading.md)

Airy wave theory and the dispersion relation, the Morison equation and its KC regimes, MacCamy–Fuchs diffraction, Pierson–Moskowitz and JONSWAP spectra and extreme loads.

### 5. [Flow-Induced Vibrations](./flow_induced_vibrations.md)

Vortex-induced vibration and lock-in, mass–damping, galloping, wake galloping, buffeting, flutter, fluid-elastic instability of tube bundles, and mitigation with strakes and tuned mass dampers.

### 6. [Hydroelastic Applications](./hydroelastic_applications.md)

Added mass and wet natural frequencies, ship springing and whipping, propeller blades, risers and pipes conveying fluid, sloshing, and hydroelastic modelling approaches.

### 7. [Fluid–Structure Interaction: Coupling Methods](./fluid_structure_interaction.md)

One-way and two-way coupling, monolithic and partitioned Dirichlet–Neumann schemes, the added-mass instability of explicit coupling, Aitken relaxation, interface data transfer, ALE mesh motion and the geometric conservation law.
