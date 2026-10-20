# Transportation

These notes apply the mechanics of the earlier sections to vehicles. Airplanes and cars are the two vehicle classes covered: how they produce and spend their forces, how they are controlled and navigated, and how they are designed and built. The material is at the level needed to set up and interpret a vehicle simulation: the forces, coefficients, operating conditions and design constraints that decide what a CFD or structural model must deliver and how accurately.

## Table of Contents

### 1. [Airplanes](./airplanes/README.md)

Flight mechanics, airfoils, stability, navigation and the aircraft design process.

- [How Airplanes Fly](./airplanes/how_airplanes_work.md): the four forces, where lift comes from, lift and drag coefficients and the drag polar, level-flight performance and control surfaces.
- [Airfoil Design](./airplanes/airfoil_design.md): airfoil geometry, the NACA four-digit family, pressure distributions, stall, Reynolds-number effects and high-lift devices.
- [Reading Airfoil Polars with Airfoil Tools](./airplanes/airfoil_tools_walkthrough.md): finding and comparing airfoils in an online database and reading their lift, drag and moment polars.
- [The Reynolds Number in Flight](./airplanes/reynolds_number.md): the Reynolds number of flyers from insects to airliners, and its effect on transition, separation, skin friction and maximum lift.
- [Airplane Stability and Control](./airplanes/airplane_stability.md): static longitudinal stability, the neutral point and static margin, trim, and the longitudinal and lateral–directional modes.
- [Static and Dynamic Stability of Oscillating Systems](./airplanes/pecking.md): the damped oscillator and its kinds of free response, applied to aircraft pitching motion and pilot-induced oscillations.
- [Inertial Navigation Systems](./airplanes/inertial_navigation_systems.md): accelerometers and gyroscopes and their error models, strapdown mechanization, attitude representation, error growth and the Schuler period, and INS/GNSS fusion with a Kalman filter.
- [Aircraft Design and Manufacturing](./airplanes/manufacturing_and_design_process.md): design phases, weight-fraction sizing, the Breguet range equation, the constraint diagram, the role of CFD and wind tunnels, certification, and airframe materials and manufacturing.

### 2. [Cars](./cars/README.md)

Vehicle mechanics and the development and production of a car.

- [How Cars Work](./cars/how_cars_work.md): road load and energy demand, combustion engines and electric drives, gear ratios, braking and tyre friction, the quarter-car ride model and vehicle aerodynamics.
- [Car Design and Manufacturing](./cars/manufacturing_and_design_process.md): the development process, packaging, the aerodynamic loop of CFD, wind tunnel and coastdown, crash structures, and body manufacturing.

## Connection to CFD

Both vehicle classes are external-flow problems, and most CFD in industry is done for them. The quantities that the notes derive from simple models (lift, drag and moment coefficients, surface pressures, cooling flow, loads on the structure) are what a full simulation must predict, and the operating conditions set the physics the simulation must capture:

| Aspect | Airliner wing in cruise | Passenger car at highway speed |
| --- | --- | --- |
| Reynolds number | a few times $10^7$ based on mean chord | about $10^7$ based on length |
| Mach number | 0.75–0.85, transonic, with shocks on the wing | below 0.2, incompressible |
| flow character | attached boundary layers, thin wake, drag dominated by skin friction and induced drag | bluff body, massive separation at the rear, drag dominated by the wake |
| main modelling issues | shock–boundary-layer interaction, transition, buffet onset and maximum lift | separation and wake, rotating wheels and moving ground, under-hood flow |
| accuracy needed | a drag count ($\Delta C_D = 0.0001$) | a few drag counts ($\Delta C_d = 0.001$) |

The physics of drag is in [Drag](../../fluid_mechanics/viscous_flow/drag.md) and the turbulence modelling behind these simulations in [Turbulence Modeling in CFD](../../numerical/cfd/turbulence_modeling.md). The [automotive aerodynamics case study](../../machine_learning/automotive_aerodynamics/ml_process.md) follows a complete workflow from morphed car shapes through thousands of CFD runs to machine-learning models that predict the drag coefficient, and it is the best place to see how the vehicle-level quantities of these notes become simulation targets.

## Not Yet Covered

Ships and marine vehicles, railways and spacecraft are planned but not written; they are tracked in the [roadmap](../../../ROADMAP.md).
