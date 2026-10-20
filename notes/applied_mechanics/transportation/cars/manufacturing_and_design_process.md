# Car Design and Manufacturing

A new car takes three to five years from the first targets to the start of production, and the process is organized so that thousands of engineers can work on one vehicle while its mass, cost, energy consumption, safety and appearance stay within their targets. This note outlines the vehicle development process, the package that fixes the main dimensions, the aerodynamic development loop in which CFD and the wind tunnel work alongside the styling studio, the crash structure, and the production of the body in the press, body and paint shops and final assembly. The mechanics of the vehicle itself are in [How Cars Work](how_cars_work.md).

## Problem Statement

Given a product brief (vehicle segment and body style, number of occupants and luggage volume, target price and production volume, powertrain options) and the external requirements (crash regulations and consumer test ratings, emissions or energy-consumption limits, pedestrian protection), find a vehicle definition that meets vehicle-level targets for mass, drag area $C_dA$, range or fuel consumption, crash performance, noise and vibration, and cost, and a manufacturing process that can build it at volume with the required quality.

The problem is a constrained multidisciplinary design. The package fixes the hard dimensions, styling fixes much of the outer surface, and the engineering disciplines trade within what is left: aerodynamics and thermal management through the flow equations of external and under-hood flow, crash through the energy balance and load paths of the structure, and production through the limits of forming, joining and painting. Development relies on simulation (CFD, crash and structural finite element analysis, multibody dynamics) that is validated by physical tests before the design is released.

## Vehicle Development Process

| Stage | Work | Main decisions |
| --- | --- | --- |
| strategy and targets | market positioning, competitor benchmarking, choice of platform and powertrains | vehicle-level targets: mass, $C_dA$, consumption, crash ratings, cost |
| concept | competing styling themes, package studies, early CFD and crash simulations, target cascade from vehicle to systems | selected styling theme and package |
| engineering development | detailed design of every system with virtual prototypes; styling surfaces refined with aerodynamics and feasibility | frozen surfaces and released designs |
| prototype build and validation | prototypes and pre-series vehicles for crash, durability, climatic, noise and handling tests and for homologation | sign-off of each attribute |
| production preparation | press dies, body-shop fixtures and robots, paint and assembly processes; pre-series build on the production line | process capability and quality |
| launch | start of production and ramp-up |  |

Development passes through quality gates at which the design must show, by simulation or test, that it is on track for every target. Targets are cascaded down: a vehicle mass target becomes budgets for the body, chassis, interior and powertrain, and a $C_dA$ target becomes budgets for the front end, wheels, underbody, mirrors and cooling flow. Most cars are built on shared platforms or modular architectures, so many components are carried over and the development concentrates on the parts that differentiate the model.

## Packaging

The package defines the positions of the people and the large components before the shape is styled. Its hard points include the seating reference points (H-points) of the occupants, which fix the head room and the roof height; the driver's eye point and the vision angles through the windscreen and pillars; the wheelbase, track widths and tyre size; the overhangs, ground clearance and approach and departure angles; the volumes of the engine or motor, the battery or fuel tank, the luggage and the cooling package; and the crush space in front of and beside the occupants.

The package bounds the aerodynamics. Height and width set the frontal area $A$, and the roof and rear-end shape that the head room allows set much of $C_d$. A battery-electric car with the battery under the floor is taller for the same head room, often by around 100 mm, which raises $A$, but has a flat underbody without exhaust or fuel tank and needs much less cooling flow, both of which reduce $C_d$.

## Aerodynamic Development Loop

Aerodynamic development runs in parallel with styling, from the first sketches to the release of the surfaces:

1. The styling studio proposes themes as digital surfaces and clay models.
2. CFD screens the themes and their variants. Production work uses steady RANS or, increasingly, hybrid RANS–LES or lattice-Boltzmann simulations of the full car with rotating wheels, moving ground, the cooling flow through the radiator modelled as a porous medium, and an underbody with its real detail; meshes of tens to hundreds of millions of cells are common. Mesh morphing and adjoint sensitivities show which parts of the surface matter most.
3. Scale models, often at 1:4 or 2:5 scale, are tested in a wind tunnel early on, when many shape changes are still cheap.
4. Full-scale clay models and then prototypes are tested in a full-scale tunnel with a moving belt, wheel drives and boundary-layer suction, which reproduce the relative motion of the road. The tunnel and CFD results are compared, and the aerodynamicists and stylists iterate on details such as the front corners, A-pillars, mirrors, roof spoiler, rear taper and wheel design.
5. The final car is checked on the road by coastdown tests. The car is allowed to roll freely in neutral and the deceleration is fitted to $`-m_{eff}\,dU/dt = F_0 + F_1U + F_2U^2`$; the coefficients are the road-load inputs for consumption testing, and $F_2 = \tfrac{1}{2}\rho C_dA$.

Changes are measured in drag counts, $\Delta C_d = 0.001$. Typical measures are a tapered rear with sharp separation edges, a smooth and partly closed underbody with a diffuser, wheel deflectors and aerodynamically shaped wheels, air curtains that guide air around the front wheels, active grille shutters, and flush door handles and glazing. Each saves a few to a few tens of counts, and a programme reaches its target by accumulating many of them.

CFD has the advantage of giving the whole flow field and of running before any hardware exists; the tunnel gives a trusted integral force on the real geometry. Repeatability and the accuracy of drag prediction to a few counts are what make the combination work, and they depend on mesh convergence and validated turbulence modelling (see [Verification and Validation](../../../numerical/cfd/verification_and_validation.md)). Machine-learning surrogates trained on thousands of CFD simulations of morphed car shapes, which predict $C_d$ and surface fields in seconds, are the subject of the [automotive aerodynamics case study](../../../machine_learning/automotive_aerodynamics/ml_process.md); its notes on [shape morphing](../../../machine_learning/automotive_aerodynamics/deformation_parameters.md) and on [generating the CFD data](../../../machine_learning/automotive_aerodynamics/generating_cfd_datasets.md) describe how the design variants of step 2 are produced and simulated.

## Crash Structures

The structure must absorb the kinetic energy of a crash in controlled deformation while keeping the passenger compartment intact. The front of the car is a crumple zone: longitudinal rails, crash boxes and the bumper beam collapse progressively in folding modes and absorb most of the energy. The passenger cell, made largely of press-hardened boron steel and other ultra-high-strength steels in the pillars, sills, roof rails and floor cross-members, resists intrusion. Side impacts leave only the door and sill depth for crush, so the side structure relies on load paths through the B-pillar, sills, roof and seat cross-members rather than on crush distance.

The energy is $E = \tfrac{1}{2}mv^2$, and for a crush distance $s$ the average deceleration is $v^2/(2s)$. A 1500 kg car hitting a rigid barrier at 56 km/h (15.6 m/s) carries 182 kJ; with 0.6 m of effective crush the average deceleration is 202 m/s², about 21 $g$. The restraint system (seat belts with pretensioners and load limiters, airbags) then shapes the deceleration of the occupant so that the loads on the body stay within limits. Crash development uses explicit finite element simulation of the whole vehicle with occupant models; full-scale tests cover frontal full-width and offset impacts, side barrier and pole impacts, rear impacts, roof strength and pedestrian protection, both for regulatory approval and for consumer rating programmes such as Euro NCAP and IIHS.

## Manufacturing

### Press Shop

The body-in-white (the welded body structure before paint, trim and moving parts) is made mostly of sheet steel and, in some cars, aluminium. Steel coil is cut into blanks, sometimes laser-welded from sheets of different thickness or grade (tailor-welded blanks) so that material is placed where it is needed. Tandem press lines or transfer presses form the panels in a sequence of dies: deep drawing, trimming, piercing and flanging. Springback, splits and wrinkles are predicted with sheet-forming simulation and compensated in the die surfaces. Press-hardened parts are heated to about 900 °C, formed and quenched in a cooled die, which gives a tensile strength of about 1500 MPa. Large high-pressure aluminium die castings replace assemblies of many stamped parts in some recent designs.

### Body Shop

The panels are joined in fixtures, mostly by robots. Steel bodies are held together by several thousand resistance spot welds, supplemented by laser welding, structural adhesives that add stiffness and fatigue strength, and, for aluminium and mixed-material joints that cannot be fusion-welded, self-piercing rivets, clinching and flow-drill screws. The geometry of the body is measured in-line with optical systems, because the gap and flush of the closures depend on it.

### Paint Shop

The painted body has several layers, applied in sequence:

1. cleaning and a conversion coating (zinc phosphate or a thin-film zirconium treatment) for adhesion and corrosion protection;
2. cathodic electrocoat, in which the whole body is dipped and the paint is deposited electrically into every cavity, then baked;
3. seam sealing and underbody protection;
4. primer, colour basecoat and clearcoat, sprayed by robots with electrostatic bells and baked in ovens.

The paint shop is the largest energy consumer of the plant, because of its ovens and the conditioned air of the spray booths.

### General Assembly

The painted body moves along the assembly line, where the doors are removed for access, and the wiring harness, interior, glazing, instrument panel and seats are installed. In the "marriage" the powertrain or battery and the chassis are raised into the body from below. Fluids are filled, the doors refitted and the car passes end-of-line tests: wheel alignment and headlamp aim, a rolling-road test of powertrain and brakes, a water-leak test, and electrical and software checks. Sample vehicles are audited for dimensional and paint quality.

## Key Takeaways

- Development cascades vehicle-level targets (mass, $C_dA$, consumption, crash, cost) to systems and checks them at quality gates over three to five years.
- The package fixes the occupants and large components and bounds the frontal area and shape available to aerodynamics.
- Aerodynamic development iterates styling, CFD and wind tunnel; the road load measured in coastdown tests is the final check, with $F_2 = \tfrac{1}{2}\rho C_dA$.
- Crash structures absorb $\tfrac{1}{2}mv^2$ in a controlled crush zone and protect a stiff passenger cell.
- The body is stamped, joined mainly by spot welding and adhesives, protected by electrocoat and painted before final assembly.

## Related Scripts

- [Car Road Load and Quarter-Car Ride](../../../../scripts/algorithms/car_road_load_and_quarter_car/): computes the road-load power and energy demand of a mid-size car and the ride response of a quarter-car suspension model.
- [Grid Convergence Index](../../../../scripts/algorithms/grid_convergence_index/): estimates discretization error from three meshes with Richardson extrapolation and the grid convergence index (GCI), following the procedure of Celik et al. (2008).
- [Drag Coefficient Prediction](../../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient surrogates with held-out CFD values in a parity plot and an error plot, and shows that a high $R^2$ can hide errors of ten drag counts.

## Exercises

**Exercise 1.** A coastdown test gives $F_0 = 150$ N, $F_1 = 0$ and $F_2 = 0.40$ N/(m/s)² for a car with effective mass 1550 kg. (a) Find its drag area $C_dA$ ($\rho = 1.225$ kg/m³). (b) How long does it take to coast from 100 to 90 km/h?

<details>
<summary>Answer</summary>

(a) $C_dA = 2F_2/\rho = 2 \times 0.40/1.225 = 0.653$ m².

(b) $`m\,dU/dt = -(F_0 + F_2U^2)`$ integrates to

```math
t = \frac{m}{\sqrt{F_0F_2}}\left[\arctan\left(U\sqrt{F_2/F_0}\right)\right]_{U_2}^{U_1} = \frac{1550}{7.75}\left[\arctan(1.434) - \arctan(1.291)\right] = 10.1\ \mathrm{s}
```

with $U_1 = 27.8$ m/s and $U_2 = 25.0$ m/s. The deceleration at 100 km/h is only 0.30 m/s², which is why coastdowns need a long, level track and correction for wind.

</details>

**Exercise 2.** An electric car with $A = 2.2$ m² is restyled to reduce $C_d$ from 0.30 to 0.25. Estimate the aerodynamic energy per 100 km at a steady 120 km/h before and after, in kWh. Why does aerodynamics matter more for electric cars than it did for combustion cars?

<details>
<summary>Answer</summary>

At $U = 33.3$ m/s, $D = \tfrac{1}{2}\rho U^2 C_dA$ is 449 N for $C_d = 0.30$ and 374 N for $C_d = 0.25$. Energy equals force times distance, $10^5$ m per 100 km:

- $C_d = 0.30$: $449 \times 10^5$ J $= 12.5$ kWh
- $C_d = 0.25$: $374 \times 10^5$ J $= 10.4$ kWh

The restyle saves about 2.1 kWh per 100 km at the wheels. An electric drivetrain loses little energy, so aerodynamic drag is a larger share of its highway consumption, and every kilowatt-hour saved extends the range of an expensive, heavy battery.

</details>

**Exercise 3.** A 1:4 scale model of a 4.5 m car is to be tested at the Reynolds number of the full-size car at 100 km/h. What tunnel speed is needed, and what problems does this create? Why do manufacturers use full-scale tunnels with moving belts?

<details>
<summary>Answer</summary>

Matching $Re = \rho UL/\mu$ with a quarter of the length needs four times the speed, $4 \times 27.8 = 111$ m/s, a Mach number of about 0.33, where compressibility begins to change the pressure distribution; the full-size car is at $M = 0.08$. Model loads and fan power also rise steeply. Scale tests are therefore run at lower Reynolds number and used for comparisons between variants.

Full-scale tunnels match $Re$ at the real speed and include the real cooling flow, wheel rotation and underbody detail. The moving belt reproduces the relative motion between car and road, which strongly affects the underbody flow, the wheel wakes and the lift.

</details>

**Exercise 4.** A rear wing on a sports car produces a lift coefficient of $-0.30$ (downforce) and adds $\Delta C_d = 0.03$, both based on a reference area of 2.0 m². At 200 km/h find the downforce, the added drag and the added power. Discuss the trade-off.

<details>
<summary>Answer</summary>

$q = \tfrac{1}{2} \times 1.225 \times 55.6^2 = 1890$ Pa.

- downforce: $1890 \times 0.30 \times 2.0 = 1134$ N;
- added drag: $1890 \times 0.03 \times 2.0 = 113$ N;
- added power: $113 \times 55.6 = 6.3$ kW.

The downforce adds grip without adding mass, the equivalent of 116 kg of load on the tyres, which improves cornering and braking stability. It costs top speed and energy, which is why active spoilers deploy only when needed.

</details>

**Exercise 5.** A 1500 kg car hits a rigid barrier at 56 km/h. (a) How much energy must the structure absorb? (b) What average deceleration results from 0.6 m of crush, and from 0.4 m? (c) Why can the side structure not use the same strategy?

<details>
<summary>Answer</summary>

(a) $E = \tfrac{1}{2} \times 1500 \times 15.56^2 = 182$ kJ.

(b) $a = v^2/(2s) = 15.56^2/1.2 = 202$ m/s² $\approx 21g$ for 0.6 m, and $15.56^2/0.8 = 302$ m/s² $\approx 31g$ for 0.4 m. Less crush space means a proportionally higher deceleration, and the real pulse has peaks well above the average.

(c) Between the side of the car and the occupant there are only the door and sill, about 0.2–0.3 m. The side structure must instead resist intrusion and spread the load through the B-pillar, sills, roof and floor cross-members, while side airbags cushion the occupant.

</details>

## References

- Hucho, W.-H. (ed.), *Aerodynamics of Road Vehicles*, 4th ed., SAE International, 1998.
- Barnard, R. H., *Road Vehicle Aerodynamic Design*, 3rd ed., MechAero Publishing, 2009.
- Katz, J., *Race Car Aerodynamics: Designing for Speed*, Bentley Publishers, 1995.
- Happian-Smith, J. (ed.), *An Introduction to Modern Vehicle Design*, Butterworth-Heinemann, 2002.
- Omar, M. A., *The Automotive Body Manufacturing Systems and Processes*, Wiley, 2011.
- Huang, M., *Vehicle Crash Mechanics*, CRC Press, 2002.
- Ferziger, J. H., Perić, M., and Street, R. L., *Computational Methods for Fluid Dynamics*, 4th ed., Springer, 2020.
