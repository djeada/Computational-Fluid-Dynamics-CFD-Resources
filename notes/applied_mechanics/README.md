# Applied Mechanics

Applied mechanics is the mechanics of rigid and deformable bodies put to engineering use: the forces that hold structures in equilibrium, the motion and vibration of bodies and machines, the stresses and deformations that decide whether a part survives, the mechanisms and control systems that make machines do useful work, and the loads that fluids exert on structures. The last of these is where this section meets CFD. A flow solver returns pressure and shear stress on every wall face; integrated over a surface they become the forces and moments that structural analysis, vibration analysis and vehicle dynamics start from, and when the structure deforms enough to change the flow, the two calculations must be coupled. These notes give the mechanics needed to use CFD results in that way, and the vehicle and aircraft notes show where the aerodynamic quantities that CFD predicts enter design.

## Prerequisites

The notes assume calculus of one and several variables, including ordinary differential equations and the solution of linear ODEs with constant coefficients, and linear algebra up to matrices, linear systems and eigenvalues. Vector algebra is developed in [Vector Analysis in Mechanics](./fundamentals/vector_analysis.md) and need not be known beforehand. The control-systems notes use the Laplace transform, which they introduce briefly. The fluid-loading and transportation notes assume the basic fluid mechanics of [`notes/fluid_mechanics/`](../fluid_mechanics/README.md): pressure, the Bernoulli equation, the Reynolds number, boundary layers and drag. Running and modifying the scripts linked from each note needs some Python.

## Suggested Reading Order

1. [Fundamentals](./fundamentals/README.md), in order: idealizations, units and Newton's laws; vectors; force systems; moments; free-body diagrams.
2. [Statics](./statics/README.md): equilibrium of particles and rigid bodies, trusses and frames, friction, centroids, and virtual work.
3. [Strength of Materials](./strength_materials/README.md), starting with stress and strain and material properties, then axial loading, torsion, beam bending and shear–moment diagrams, combined loading, buckling and fatigue.
4. [Dynamics](./dynamics/README.md): kinematics and kinetics of particles and rigid bodies, energy and momentum methods, vibrations and Lagrangian mechanics. It can be read in parallel with strength of materials once statics is done.
5. [Fluid Loading on Structures](./fluid_loading/README.md), after the fluid mechanics prerequisites and the vibrations note: pressure forces, wind and wave loads, flow-induced vibration and fluid–structure interaction.
6. [Control Systems](./control_systems/README.md) and [Mechanical Systems](./mechanical_systems/README.md), in either order, after dynamics.
7. [Transportation](./transportation/README.md): airplanes and cars, which draw on everything above.

## Contents

### Fundamentals: [`fundamentals/`](./fundamentals/README.md)

| Note | What it covers |
| --- | --- |
| [Introduction to Applied Mechanics](./fundamentals/intro.md) | Scope of the subject, particle, rigid-body, deformable-body and continuum models, SI units and dimensional homogeneity, Newton's laws and a problem-solving procedure |
| [Vector Analysis in Mechanics](./fundamentals/vector_analysis.md) | Components, unit vectors, direction cosines, dot and cross products, moments as cross products, triple products and rotation matrices |
| [Force Systems and Resultants](./fundamentals/force_systems.md) | Concurrent, coplanar, parallel and general force systems, force–couple systems, the single resultant, the wrench, distributed loads and integrated fluid pressure |
| [Moments and Couples](./fundamentals/moments_couples.md) | Moment about a point and an axis, Varignon's theorem, couples and moving a force by adding a couple |
| [Free-Body Diagrams](./fundamentals/free_body_diagrams.md) | Isolating a body, 2D and 3D support reactions, two- and three-force members, static determinacy and the method of sections |

### Statics: [`statics/`](./statics/README.md)

| Note | What it covers |
| --- | --- |
| [Particle Equilibrium](./statics/particle_equilibrium.md) | Concurrent forces in 2D and 3D as a linear system, cables under transverse load, force polygons and Lami's theorem, springs and ideal pulleys |
| [Rigid Body Equilibrium](./statics/rigid_body_equilibrium.md) | Force and moment balance in 2D and 3D, support reactions, two- and three-force members, determinacy and improper constraints |
| [Structural Analysis](./statics/structural_analysis.md) | Load paths, degree of indeterminacy, cables and arches, influence lines, the force method and the direct stiffness method for trusses |
| [Trusses, Frames and Machines](./statics/trusses_frames.md) | Plane and space trusses by the methods of joints and sections in hand and matrix form, zero-force members, and frames and machines |
| [Friction](./statics/friction.md) | Coulomb friction, sliding versus tipping, wedges, square-threaded screws, the capstan equation for belts and rolling resistance |
| [Center of Mass and Centroids](./statics/center_of_mass.md) | Centres of mass and gravity, centroids by integration and by composite parts, Pappus–Guldinus theorems and second moments of area |
| [Virtual Work and Stability of Equilibrium](./statics/virtual_work.md) | Virtual displacements, generalized forces, mechanical advantage of linkages, potential energy and the stability of equilibrium |

### Dynamics: [`dynamics/`](./dynamics/README.md)

| Note | What it covers |
| --- | --- |
| [Kinematics of Particles](./dynamics/kinematics_particles.md) | Rectilinear motion, projectiles, normal–tangential and polar coordinates with the Coriolis term, and relative motion between translating frames |
| [Kinetics of Particles](./dynamics/kinetics_particles.md) | Newton's second law in Cartesian, path and polar coordinates, force models, central-force motion, quadratic drag and systems of particles |
| [Rigid Body Kinematics](./dynamics/rigid_body_kinematics.md) | Fixed-axis rotation and general plane motion, the instantaneous centre, relative velocity and acceleration, the slider-crank and rotating frames |
| [Rigid Body Kinetics](./dynamics/rigid_body_kinetics.md) | Mass moments of inertia, the equations of plane motion, rolling with and without slip, Euler's equations, spin stability and gyroscopic moments |
| [Work and Energy Methods](./dynamics/work_energy.md) | Work of forces and couples, kinetic and potential energy, conservation of energy, power and efficiency, and energy as a check on numerical integration |
| [Impulse and Momentum](./dynamics/impulse_momentum.md) | Linear and angular impulse and momentum, central and oblique impact, steady mass flow and variable-mass systems with the rocket equation |
| [Mechanical Vibrations](./dynamics/vibrations.md) | Free, damped and harmonically forced vibration, the logarithmic decrement, base excitation and isolation, multi-degree-of-freedom modes and the tuned mass damper |
| [Lagrangian Mechanics](./dynamics/lagrangian_mechanics.md) | Generalized coordinates and forces, Lagrange's equations, Rayleigh's dissipation function, the cart–pendulum and double pendulum, and linearization |

### Strength of Materials: [`strength_materials/`](./strength_materials/README.md)

| Note | What it covers |
| --- | --- |
| [Stress and Strain](./strength_materials/stress_strain.md) | The Cauchy stress and small-strain tensors, generalized Hooke's law, stress transformation and Mohr's circle, yield criteria and stress concentration at a hole |
| [Mechanical Properties of Materials](./strength_materials/material_properties.md) | The tensile test, engineering and true stress–strain curves, strength, ductility, toughness and hardness, Ashby indices, temperature, rate and creep effects |
| [Axial Loading](./strength_materials/axial_loading.md) | Deformation of stepped and tapered bars, indeterminate bars, thermal stress, Saint-Venant's principle, stress concentration, strain energy and impact |
| [Torsion](./strength_materials/torsion.md) | Shear stress and twist of circular shafts, power transmission, indeterminate shafts, rectangular, thin-walled closed and open sections |
| [Bending of Beams](./strength_materials/beam_bending.md) | Flexural and shear stress in beams, the elastic curve and beam deflection |
| [Shear Force and Bending Moment Diagrams](./strength_materials/shear_moment.md) | Internal shear and moment in beams, the load–shear–moment relations and the construction of shear and moment diagrams |
| [Combined Loading](./strength_materials/combined_loading.md) | Superposition of axial, bending, shear and torsional stresses and failure criteria for combined stress states |
| [Buckling of Columns](./strength_materials/buckling.md) | Euler buckling of columns, effective length and the stability of compression members |
| [Fatigue](./strength_materials/fatigue.md) | Failure under cyclic loading: stress–life curves, endurance limit, mean-stress corrections and fatigue design |

### Fluid Loading on Structures: [`fluid_loading/`](./fluid_loading/README.md)

| Note | What it covers |
| --- | --- |
| [Fluid Loading on Structures](./fluid_loading/intro.md) | Pressure, viscous, inertia and motion-dependent loads, force coefficients, the governing dimensionless groups and dynamic amplification |
| [Pressure Forces on Structures](./fluid_loading/pressure_forces.md) | Hydrostatic forces on plane and curved surfaces, buoyancy and floating stability, the pressure coefficient, and integrating surface pressure and shear into forces and moments |
| [Wind Loading on Structures](./fluid_loading/wind_loading.md) | The atmospheric boundary layer, turbulence and gusts, pressure coefficients on buildings, Davenport's gust factor, across-wind vortex shedding and galloping |
| [Wave Loading on Offshore Structures](./fluid_loading/wave_loading.md) | Airy wave theory, the Morison equation and its KC regimes, MacCamy–Fuchs diffraction, wave spectra and extreme loads |
| [Flow-Induced Vibrations](./fluid_loading/flow_induced_vibrations.md) | Vortex-induced vibration and lock-in, galloping, buffeting, flutter, fluid-elastic instability of tube bundles and mitigation |
| [Hydroelastic Applications](./fluid_loading/hydroelastic_applications.md) | Added mass and wet natural frequencies, ship springing and whipping, propeller blades, risers and pipes conveying fluid, and sloshing |
| [Fluid–Structure Interaction: Coupling Methods](./fluid_loading/fluid_structure_interaction.md) | One- and two-way coupling, monolithic and partitioned schemes, the added-mass instability, Aitken relaxation, interface data transfer and ALE mesh motion |

### Control Systems: [`control_systems/`](./control_systems/README.md)

| Note | What it covers |
| --- | --- |
| [Introduction to Control Systems](./control_systems/intro.md) | Plant, actuator, sensor and controller, open- and closed-loop operation, time- and frequency-domain specifications and the LTI assumption |
| [System Modeling](./control_systems/system_modeling.md) | Lumped models of mechanical, electrical, fluid and thermal systems, transfer functions, step responses, state-space form and linearization |
| [Stability Analysis](./control_systems/stability_analysis.md) | BIBO and internal stability, pole locations, the Routh–Hurwitz criterion and the root locus |
| [Feedback Control](./control_systems/feedback_control.md) | Closed-loop transfer functions, sensitivity and complementary sensitivity, steady-state error and system type, lead and lag compensation |
| [PID Controllers](./control_systems/pid_controllers.md) | P, I and D action, controller forms, derivative filtering, anti-windup, Ziegler–Nichols, IMC and SIMC tuning and discrete implementation |
| [Frequency Response](./control_systems/frequency_response.md) | Bode and Nyquist plots, gain, phase and delay margins, bandwidth, phase margin and damping, time delay and loop shaping |

### Mechanical Systems: [`mechanical_systems/`](./mechanical_systems/README.md)

| Note | What it covers |
| --- | --- |
| [Mechanisms and Linkages](./mechanical_systems/mechanisms.md) | Mobility, the Grashof condition, four-bar position, velocity and acceleration analysis, transmission angle, slider-crank inertia terms, cams and function synthesis |
| [Gears and Transmissions](./mechanical_systems/gears.md) | The law of gearing and the involute, tooth proportions and contact ratio, helical, bevel and worm gears, planetary trains, tooth forces and Lewis bending stress |
| [Bearings and Lubrication](./mechanical_systems/bearings.md) | Rolling-bearing rating life, the Reynolds equation for thin films, journal-bearing solutions, the Sommerfeld number, the Stribeck curve and EHL films |
| [Rotating Machinery](./mechanical_systems/rotating_machinery.md) | The Jeffcott rotor and critical speeds, the Campbell diagram, balancing, flywheels, the Euler turbomachine equation, pump curves, affinity laws and NPSH |
| [Hydraulic and Pneumatic Systems](./mechanical_systems/hydraulic_pneumatic.md) | Pascal's law, cylinders, pumps and valves, the orifice equation, line losses, accumulators, power and heat, and the stiffness of oil and air columns |

### Transportation: [`transportation/`](./transportation/README.md)

#### Airplanes: [`transportation/airplanes/`](./transportation/airplanes/README.md)

| Note | What it covers |
| --- | --- |
| [How Airplanes Fly](./transportation/airplanes/how_airplanes_work.md) | The four forces, where lift comes from, lift and drag coefficients and the drag polar, level-flight performance and control surfaces |
| [Airfoil Design](./transportation/airplanes/airfoil_design.md) | Airfoil geometry, the NACA four-digit family, pressure distributions, stall, Reynolds-number effects and high-lift devices |
| [Reading Airfoil Polars with Airfoil Tools](./transportation/airplanes/airfoil_tools_walkthrough.md) | Finding and comparing airfoils in an online database and reading their lift, drag and moment polars |
| [The Reynolds Number in Flight](./transportation/airplanes/reynolds_number.md) | The Reynolds number of flyers from insects to airliners and its effect on transition, separation, skin friction and maximum lift |
| [Airplane Stability and Control](./transportation/airplanes/airplane_stability.md) | Static longitudinal stability, the neutral point and static margin, trim, and the longitudinal and lateral–directional modes |
| [Static and Dynamic Stability of Oscillating Systems](./transportation/airplanes/pecking.md) | The damped oscillator and its kinds of free response, applied to aircraft pitching motion and pilot-induced oscillations |
| [Inertial Navigation Systems](./transportation/airplanes/inertial_navigation_systems.md) | Accelerometer and gyroscope error models, strapdown mechanization, attitude representation, error growth, the Schuler period and INS/GNSS fusion |
| [Aircraft Design and Manufacturing](./transportation/airplanes/manufacturing_and_design_process.md) | Design phases, weight-fraction sizing, the Breguet range equation, the constraint diagram, CFD and wind tunnels, certification and airframe manufacturing |

#### Cars: [`transportation/cars/`](./transportation/cars/README.md)

| Note | What it covers |
| --- | --- |
| [How Cars Work](./transportation/cars/how_cars_work.md) | Road load and energy demand, engines and electric drives, gear ratios, braking and tyre slip, the quarter-car ride model and vehicle aerodynamics |
| [Car Design and Manufacturing](./transportation/cars/manufacturing_and_design_process.md) | The development process, packaging, the aerodynamic loop of CFD, wind tunnel and coastdown, crash structures and body manufacturing |

## Connecting to CFD

The notes that link most directly to the CFD and fluid-mechanics material in this repository are these.

- Surface pressure and wall shear from a CFD solution become structural loads by integration over the wetted surface. [Force Systems and Resultants](./fundamentals/force_systems.md#surface-loads-and-fluid-pressure) gives the face-sum form, and [Pressure Forces on Structures](./fluid_loading/pressure_forces.md) maps the loads onto a structure. The resulting forces and moments feed the [shear and moment diagrams](./strength_materials/shear_moment.md), [combined-loading](./strength_materials/combined_loading.md) checks and, for cyclic loads, [fatigue](./strength_materials/fatigue.md) assessment.
- Unsteady flows load structures dynamically: vortex shedding behind a cylinder, wind gusts on a tall building, waves on an offshore platform. [Flow-Induced Vibrations](./fluid_loading/flow_induced_vibrations.md), [Wind Loading on Structures](./fluid_loading/wind_loading.md) and [Wave Loading on Offshore Structures](./fluid_loading/wave_loading.md) combine the [vibration](./dynamics/vibrations.md) response with the flow physics of [drag](../fluid_mechanics/viscous_flow/drag.md) and [boundary layers](../fluid_mechanics/viscous_flow/boundary_layers.md).
- When the structure's motion changes the flow, the fluid and structural solvers must exchange data every step. [Fluid–Structure Interaction: Coupling Methods](./fluid_loading/fluid_structure_interaction.md) covers the coupling algorithms, and [the fluid-mechanics note on FSI](../fluid_mechanics/specialized_topics/fluid_structure_interaction.md) the physics. The structural side is usually a finite element model ([Finite Element Method](../numerical/fem/intro.md)).
- Vehicle and aircraft aerodynamics are the main industrial uses of external-flow CFD. [How Cars Work](./transportation/cars/how_cars_work.md) shows how drag and lift coefficients enter road load and handling, and the [automotive aerodynamics notes](../machine_learning/automotive_aerodynamics/README.md) build CFD datasets of car shapes. [How Airplanes Fly](./transportation/airplanes/how_airplanes_work.md) and [Airplane Stability and Control](./transportation/airplanes/airplane_stability.md) turn lift, drag and pitching-moment coefficients into performance and stability.

## Roadmap

Topics that are planned but not written yet (ships, railways and spacecraft; buildings, bridges, towers and earthquake engineering; wind turbines and other energy systems; robotics; biomechanics; and nonlinear, continuum, computational and multibody mechanics) are listed in the [roadmap](../../ROADMAP.md#applied-mechanics-notesapplied_mechanics).
