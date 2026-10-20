# Aircraft Design and Manufacturing

An aircraft is designed by narrowing a large space of possible configurations to one detailed definition that meets a set of requirements, can be certified, and can be built at an acceptable cost. This note follows that process from requirements through conceptual, preliminary and detailed design, with the sizing tools used in the early stages (weight-fraction sizing, the Breguet range equation and the constraint diagram), the role of CFD and wind-tunnel testing at each stage, certification and testing, and the materials and manufacturing methods of modern airframes. The aerodynamic background is in [How Airplanes Fly](how_airplanes_work.md) and [Airfoil Design](airfoil_design.md); stability is treated in [Airplane Stability and Control](airplane_stability.md).

## Problem Statement

Given a set of mission requirements (payload and number of passengers, design range, cruise Mach number and altitude, takeoff and landing field lengths, approach speed, climb gradient and ceiling) and the available technology (engine fuel consumption, achievable lift-to-drag ratio, structural materials), find

- the configuration: wing, tail and engine arrangement;
- the takeoff weight $W_0$ and its split into empty weight, fuel and payload;
- the wing area $S$ and the installed thrust $T$, usually expressed as the wing loading $W/S$ and the thrust-to-weight ratio $T/W$;
- the geometry, structure and systems in increasing detail, and a way of building and certifying them.

The early sizing assumes quasi-steady point-mass flight, a parabolic drag polar $C_D = C_{D0} + kC_L^2$ with $k = 1/(\pi e AR)$, and statistical correlations for the empty weight. Its governing relations are the weight balance, the Breguet range equation for the cruise fuel, and the force balances of each flight condition:

```math
W_0 = W_{crew} + W_{payload} + W_{fuel} + W_{empty},
\qquad R = \frac{V}{c\,g}\, \frac{L}{D}\ln \frac{W_i}{W_f},
\qquad \frac{T}{W} = \frac{q C_{D0}}{W/S} + k\, n^2\, \frac{W/S}{q} + \frac{1}{V}
\frac{dh}{dt}
```

## The Design Process

Design proceeds in phases of increasing detail and cost, and the freedom to change the design shrinks as the cost of a change grows:

| Phase | Questions answered | Typical tools | Output |
| --- | --- | --- | --- |
| requirements | what the market or customer needs: payload, range, speed, airports, operating cost, entry-into-service date | market studies, airline consultation, competitor analysis | requirements document |
| conceptual design | which configuration, how heavy, how big a wing and engine | weight-fraction sizing, constraint diagram, handbook drag estimates, trade studies | a sized baseline configuration and its expected performance |
| preliminary design | can it be built as drawn; refined aerodynamics, structure, weights and systems | CFD on the full configuration, wind-tunnel tests, finite element models of the primary structure, loads analysis | frozen external shape (lofts), major structural layout, firm performance guarantees |
| detailed design | every part, joint and system | CAD of all parts, detailed stress analysis, fatigue and damage-tolerance analysis, manufacturing planning | drawings and digital models released to manufacturing |
| test and certification | does the real aircraft meet the requirements and the airworthiness rules | ground tests, flight tests | type certificate |

Most of the life-cycle cost is committed in the conceptual and preliminary phases, although they consume only a small part of the engineering effort. This is why a lot of attention goes to getting the configuration and sizing right before the shape is frozen.

## Weight Estimation

The takeoff weight is the sum of the crew and payload, which the requirements fix, the fuel, and the empty weight. Writing the fuel and empty weights as fractions of $W_0$ gives

$$
W_0 = \frac{W_{crew} + W_{payload}}{1 - W_f/W_0 - W_e/W_0}
$$

The empty-weight fraction comes from statistics of existing aircraft. Raymer (2018) fits $`W_e/W_0 = A\,W_0^{C}`$, with $A = 1.02$ and $C = -0.06$ for jet transports when $W_0$ is in pounds. The fuel fraction is built from the weight ratios of the mission segments: warm-up and takeoff (about 0.970), climb (0.985), cruise from the Breguet equation, and landing (0.995), with about 6% added for reserves and trapped fuel. Because $W_e/W_0$ depends on $W_0$, the equation is solved by iteration.

For example, a 150-seat airliner with 15 500 kg of crew and payload, a 5000 km range at $V = 230$ m/s, $L/D = 17$ and $c = 1.6 \times 10^{-5}$ kg/(N s) has a cruise weight ratio $`\exp(-Rcg/(V\,L/D)) = 0.818`$, a mission weight ratio $0.970 \times 0.985 \times 0.818 \times 0.995 = 0.778$ and a fuel fraction $1.06 \times (1 - 0.778) = 0.236$. Iteration converges at $`W_0 \approx 59\,000`$ kg with $W_e/W_0 = 0.50$. Each kilogram of payload needs about 3.8 kg of takeoff weight, the growth factor $W_0/(W_{crew} + W_{payload})$, which is why a small increase in empty weight or fuel burn late in a programme has a large effect.

Preliminary design replaces the single empty-weight fraction with component weights (wing, fuselage, tail, landing gear, engines, systems, furnishings), each from semi-empirical equations and then from the structural models, and tracks the centre of gravity of every loading condition.

## The Breguet Range Equation

In cruise, the distance flown is $`dR = V\,dt`$ and the fuel weight flow equals $`c\,g\,T`$, where $c$ is the thrust-specific fuel consumption in kg of fuel per newton of thrust per second. With $T = D = W/(L/D)$,

```math
\frac{dW}{dt} = -\frac{c\,g\,W}{L/D} \quad\Longrightarrow\quad R = \frac{V}{c\,g}\,
\frac{L}{D}\,\ln \frac{W_i}{W_f}
```

for constant $V$, $L/D$ and $c$, which corresponds to a slow cruise-climb. The units are consistent: $V$ in m/s, $c$ in kg/(N s) and $g$ in m/s² make $V/(cg)$ a length in metres. Modern high-bypass turbofans in cruise have $c$ between $1.5 \times 10^{-5}$ and $1.7 \times 10^{-5}$ kg/(N s), quoted in imperial units as 0.53–0.60 lb/(lbf h). For a propeller aircraft, with power-specific fuel consumption $c_P$ in kg/J and propeller efficiency $\eta_p$, the equation becomes $R = (\eta_p/(c_P g))(L/D)\ln(W_i/W_f)$.

The three factors separate the contributions of the disciplines: propulsion ($V/c$, which for a jet is proportional to overall engine efficiency), aerodynamics ($L/D$) and structures ($W_i/W_f$, the fuel that can be carried for a given empty weight).

## The Constraint Diagram

Each performance requirement gives the thrust-to-weight ratio needed at each wing loading. Taking the drag polar above and dynamic pressure $q = \tfrac{1}{2}\rho V^2$, the standard constraint equations (Raymer 2018, ch. 5; Gudmundsson 2014, ch. 3) are:

| Requirement | Required $T/W$ |
| --- | --- |
| level cruise or manoeuvre at load factor $n$ | $`\dfrac{q C_{D0}}{W/S} + k n^2\dfrac{W/S}{q}`$ |
| sustained climb rate $V_V$ at speed $V$ | $`\dfrac{V_V}{V} + \dfrac{q C_{D0}}{W/S} + k\dfrac{W/S}{q}`$ |
| takeoff ground run $S_G$ | $`\dfrac{V_{LOF}^2}{2gS_G} + \dfrac{q C_{D,TO}}{W/S} + \mu\left(1 - \dfrac{q C_{L,TO}}{W/S}\right)`$ at $q$ for $V_{LOF}/\sqrt{2}$ |
| stall speed $V_s$ | none; it limits $`W/S \le \tfrac{1}{2}\rho V_s^2 C_{L\max}`$ |

The cruise and climb requirements are evaluated at the cruise weight and with the thrust available at altitude, then referred back to takeoff weight and sea-level static thrust: $T_{SL}/W_0 = (\beta/\alpha)(T/W)$ with weight fraction $\beta$ and thrust lapse $\alpha$. The lift-off speed in the takeoff constraint is a multiple of the stall speed, so the first term grows linearly with $W/S$.

![Constraint diagram and Breguet range](../../../../scripts/plots/aircraft_design_constraint_diagram/aircraft_design_constraint_diagram.png)

Panel (a) shows the constraints for a light business jet. The cruise curve falls with wing loading at first, because a lightly loaded wing cruises at a low $C_L$ where zero-lift drag dominates, while the takeoff line rises. Every point in the shaded region above all thrust curves and left of the stall line meets the requirements; the lowest thrust is at the crossing of the takeoff and cruise curves, $W/S = 2327$ N/m² and $T/W = 0.221$. A designer then adds margin and checks the choice against the empty weight and fuel volume it implies. Panel (b) shows the Breguet range growing in proportion to $L/D$: at $L/D = 18$ and $W_i/W_f = 1.35$ the range is 7900 km.

## Role of CFD and Wind Tunnels

Aerodynamic tools are matched to the phase, trading fidelity against the number of cases that can be run.

| Phase | Computation | Experiment |
| --- | --- | --- |
| conceptual | handbook and component drag build-up, vortex-lattice and panel methods for lift distribution and stability derivatives, 2D airfoil codes | none, or reuse of data from earlier aircraft |
| preliminary | RANS on the wing–body–nacelle–tail configuration for cruise drag, transonic wing design by inverse or adjoint optimization, high-lift studies | low-speed and high-speed tunnel tests of scaled models; pressure-plotting and force balances |
| detailed | RANS for loads databases (thousands of Mach, angle-of-attack and control-deflection cases), hybrid RANS–LES for buffet and high-lift maximum lift, coupled aeroelastic analysis for flutter and static deformation | high-Reynolds-number tests in pressurized or cryogenic tunnels, flutter models, engine-inlet and icing tests |
| flight test | correlation of the CFD and tunnel database with flight data | flight test with pressure belts, strain gauges and flow visualisation |

Wind tunnels cannot match the flight Reynolds number on a small model: a 1:20 model at the same Mach number has a Reynolds number 20 times too low unless the gas is pressurized or cooled, and transition and separation behaviour change with it (see [The Reynolds Number in Flight](reynolds_number.md)). CFD can run at flight Reynolds number and gives the full field, but turbulence models are least reliable for the separated flows that set maximum lift and buffet onset. The two are therefore used together, and the CFD is validated against tunnel data before its results are trusted (see [Verification and Validation](../../../numerical/cfd/verification_and_validation.md) and [Turbulence Modeling in CFD](../../../numerical/cfd/turbulence_modeling.md)).

## Structures and Loads

The structure is sized by a loads envelope: manoeuvre loads within the V–n diagram, gust loads, landing and ground loads, cabin pressurization, and loads from engine failure and control inputs. Transport aircraft are typically designed for limit manoeuvre load factors of +2.5 and −1.0. The structure must carry limit load without permanent deformation and ultimate load, 1.5 times limit, without failure for at least a few seconds. Fatigue and damage tolerance are as important as static strength for a pressurized fuselage flown for tens of thousands of cycles: the structure must keep its residual strength with a crack that inspections can find, which drives material choice, stress levels at fastener holes, and inspection intervals (see [Fatigue](../../strength_materials/fatigue.md)).

## Certification and Testing

An aircraft type needs a type certificate from the authority of the state of design (the FAA in the United States, EASA in the European Union), followed by a production approval for the factory and an airworthiness certificate for each aircraft built. For each requirement of the airworthiness code, the applicant agrees a means of compliance with the authority: analysis, simulation, ground test or flight test, documented with safety assessments such as failure modes and effects analysis and fault-tree analysis of the systems.

Ground testing includes

1. the static test of a complete airframe, loaded to limit and then to ultimate load, often finishing with the wing bent to failure;
2. the full-scale fatigue test of a second airframe, cycled through a multiple of the design life to demonstrate damage tolerance and to set inspection intervals;
3. systems integration rigs (the "iron bird" for flight controls and hydraulics), ground vibration tests that measure the structural modes for the flutter model, and component tests such as bird strike, lightning and fire.

Flight testing expands the envelope step by step: handling qualities and stall characteristics, flutter clearance with excitation at increasing speeds, performance (takeoff and landing distances, climb with one engine inoperative, fuel consumption), systems failures, and environmental tests in heat, cold and icing. Several test aircraft share the programme, which for a new airliner takes one to two years.

## Materials and Manufacturing

### Airframe Materials

| Material | Typical properties | Where used |
| --- | --- | --- |
| aluminium alloy 2024-T3 | $\rho$ = 2780 kg/m³, $E$ = 73 GPa, good fatigue and fracture toughness | fuselage skins, lower wing skins (tension-dominated) |
| aluminium alloys 7075, 7050, 7150 | $\rho \approx$ 2800 kg/m³, higher static strength | upper wing skins and stringers (compression), spars, frames, machined parts |
| aluminium–lithium alloys | 5–10% lower density and higher stiffness than conventional alloys | fuselage and wing parts of recent aircraft |
| titanium Ti-6Al-4V | $\rho$ = 4430 kg/m³, $E$ = 114 GPa, keeps strength at high temperature, galvanically compatible with carbon fibre | engine pylons, highly loaded fittings, parts in contact with CFRP |
| carbon-fibre reinforced polymer (CFRP) | $\rho \approx$ 1550–1600 kg/m³, quasi-isotropic laminates $E \approx$ 50–70 GPa, very good fatigue, no corrosion, low impact damage tolerance | wings, tails and fuselage of current wide-bodies (about half the structural weight of the Boeing 787 and Airbus A350) |
| high-strength steel | $\rho$ = 7800 kg/m³, very high strength | landing gear, flap tracks |

The choice weighs specific strength and stiffness against fatigue, damage tolerance, corrosion, repairability, cost and the manufacturing process.

### Manufacturing

Metal parts are made by machining from plate, forgings or extrusions (large monolithic spars and ribs replace assemblies of many smaller parts, at the cost of a high ratio of material bought to material that flies), by stretch-forming and roll-forming sheet into skins and stringers, and by chemical milling of skin pockets. Composite parts are laid up from pre-impregnated tape or tow by automated tape laying or automated fibre placement on a mould, vacuum-bagged and cured in an autoclave under heat and pressure (around 180 °C and 6–7 bar for common aerospace epoxies), then trimmed, drilled and inspected ultrasonically for porosity and delaminations.

Assembly proceeds from sub-assemblies (panels, ribs, spars) to major components (wing boxes, fuselage barrels or sections, tail surfaces) to final assembly, where the components are joined, systems are installed and tested, and the aircraft is painted. Joints are mostly mechanically fastened, with up to millions of rivets and bolts in a large airliner, because fasteners can be inspected and replaced; composite joints also use bonding. Jigs and laser tracking hold the positions of the parts, and gaps between composite parts are filled with shims to avoid preloading the structure. Each aircraft is ground-tested and flown before delivery.

## Key Takeaways

- Design moves from requirements through conceptual, preliminary and detailed design; most cost is committed before the shape is frozen.
- Takeoff weight follows from the payload and the fuel and empty-weight fractions, solved by iteration; each kilogram of payload brings several kilograms of takeoff weight.
- The Breguet equation $R = (V/(cg))(L/D)\ln(W_i/W_f)$ ties range to engine efficiency, aerodynamic efficiency and structural efficiency.
- The constraint diagram turns every performance requirement into a minimum $T/W$ or maximum $W/S$ and locates the design point.
- CFD and wind tunnels are complementary: tunnels give trusted data at the wrong Reynolds number, CFD gives flight conditions and full fields with modelling uncertainty.
- Certification demands analysis backed by static, fatigue and flight tests; material and process choices follow from fatigue, damage tolerance and manufacturing cost as much as from strength.

## Related Scripts

- [Aircraft Design Constraint Diagram](../../../../scripts/plots/aircraft_design_constraint_diagram/): draws the constraint diagram of conceptual aircraft design, the thrust-to-weight ratio each performance requirement demands as a function of wing loading, and picks the design point with the lowest thrust inside the feasible region.

## Exercises

**Exercise 1.** In preliminary design, a 75 000 kg airliner is to cruise at 230 m/s at an altitude where $\rho = 0.38$ kg/m³, with a cruise lift coefficient of 0.5. Size the wing area from the lift equation. What else pushes the wing area up or down?

<details>
<summary>Answer</summary>

```math
S = \frac{2mg}{\rho V^2 C_L} = \frac{2 \times 75\,000 \times 9.81}{0.38 \times 230^2 \times 0.5} = 146\ \mathrm{m^2}
```

Low-speed requirements usually decide the final size: the approach speed for the available $C_{L\max}$ with flaps, and the takeoff field length. Initial cruise altitude capability and fuel volume in the wing also play a part. A larger wing lowers these speeds but adds weight and friction drag in cruise.

</details>

**Exercise 2.** At $C_L = 0.5$ with $e = 0.8$, compare the induced drag coefficient for aspect ratios 9 and 11. Why do designers not simply choose a very high aspect ratio?

<details>
<summary>Answer</summary>

```math
C_{D_i}(AR = 9) = \frac{0.25}{\pi \times 0.8 \times 9} = 0.0111, \qquad
C_{D_i}(AR = 11) = 0.0090
```

That is an 18% reduction. A longer, slenderer wing has a larger root bending moment and a thinner structural box, so it needs more structural weight, is more flexible (aeroelastic and flutter concerns) and holds less fuel. Airport gate span limits also apply, which is one reason for folding wingtips on some recent designs.

</details>

**Exercise 3.** An airliner starts cruise at 70 000 kg with 15 000 kg of usable cruise fuel, flies at 230 m/s with $L/D = 18$, and its engines have $c = 1.6 \times 10^{-5}$ kg/(N s). (a) Find the Breguet range. (b) What fraction of the initial cruise weight must be fuel to fly 6000 km?

<details>
<summary>Answer</summary>

(a) $V/(cg) = 230/(1.6 \times 10^{-5} \times 9.81) = 1.465 \times 10^6$ m, so

```math
R = 1.465 \times 10^6 \times 18 \times \ln\frac{70\,000}{55\,000} = 6.36 \times 10^6\ \mathrm{m} = 6360\ \mathrm{km}
```

(b) $`W_i/W_f = \exp(Rcg/(V\,L/D)) = \exp(6 \times 10^6/(1.465 \times 10^6 \times 18)) = 1.255`$, so the fuel fraction is $1 - 1/1.255 = 0.203$ of the initial cruise weight.

</details>

**Exercise 4.** For the cruise constraint $T/W = qC_{D0}/(W/S) + k(W/S)/q$, show that the required thrust is smallest at $W/S = q\sqrt{C_{D0}/k}$ and that $T/W$ is then $2\sqrt{kC_{D0}}$. Evaluate both for $\rho = 0.38$ kg/m³, $V = 230$ m/s, $C_{D0} = 0.020$, $AR = 9$ and $e = 0.8$, and interpret the result.

<details>
<summary>Answer</summary>

Setting $d(T/W)/d(W/S) = -qC_{D0}/(W/S)^2 + k/q = 0$ gives $(W/S)^2 = q^2C_{D0}/k$. Substituting back, both terms equal $\sqrt{kC_{D0}}$.

With $`q = \tfrac{1}{2} \times 0.38 \times 230^2 = 10\,051`$ Pa and $k = 1/(\pi \times 0.8 \times 9) = 0.0442$:

```math
\frac{W}{S} = 10\,051\sqrt{\frac{0.020}{0.0442}} = 6760\ \mathrm{N/m^2}, \qquad \frac{T}{W} = 2\sqrt{0.0442 \times 0.020} = 0.0595
```

At this wing loading the cruise lift coefficient is $W/(qS) = \sqrt{C_{D0}/k} = 0.67$, where induced and zero-lift drag are equal and $L/D$ is at its maximum, $1/(2\sqrt{kC_{D0}}) = 16.8$. The low-speed constraints normally prevent such a high wing loading, so real airliners cruise slightly below $(L/D)_{max}$ or cruise higher to raise $C_L$.

</details>

**Exercise 5.** A structural aluminium alloy follows Basquin's relation $S = \sigma_f'(2N_f)^b$ with $\sigma_f' = 1000$ MPa and $b = -0.1$. Find the cycles to failure at a stress amplitude of 250 MPa, and the factor by which life increases if a design change lowers the amplitude by 10%.

<details>
<summary>Answer</summary>

```math
2N_f = \left(\frac{250}{1000}\right)^{1/b} = 0.25^{-10} = 1.05 \times 10^6 \quad\Longrightarrow\quad N_f = 5.2 \times 10^5\ \mathrm{cycles}
```

At 225 MPa, $2N_f = 0.225^{-10} = 3.0 \times 10^6$, so $N_f = 1.5 \times 10^6$ cycles. The life grows by $(250/225)^{10} = 2.87$. Because $\lvert b \rvert$ is small, small stress reductions give large life gains, which is why fatigue-critical details such as fastener holes receive so much attention.

</details>

## References

- Raymer, D. P., *Aircraft Design: A Conceptual Approach*, 6th ed., American Institute of Aeronautics and Astronautics, 2018.
- Gudmundsson, S., *General Aviation Aircraft Design: Applied Methods and Procedures*, Butterworth-Heinemann, 2014.
- Anderson, J. D., Jr., *Aircraft Performance and Design*, McGraw-Hill, 1999.
- Torenbeek, E., *Synthesis of Subsonic Airplane Design*, Delft University Press, 1982.
- Megson, T. H. G., *Aircraft Structures for Engineering Students*, 6th ed., Butterworth-Heinemann, 2017.
- Niu, M. C. Y., *Airframe Structural Design*, 2nd ed., Conmilit Press, 1999.
- Dowling, N. E., *Mechanical Behavior of Materials*, 4th ed., Pearson, 2013.
