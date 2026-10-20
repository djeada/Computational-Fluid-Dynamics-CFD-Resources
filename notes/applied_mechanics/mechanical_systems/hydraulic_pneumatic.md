# Hydraulic and Pneumatic Systems

Fluid power systems transmit energy through a pressurized fluid: a pump or compressor converts shaft power into flow at pressure, valves direct and meter the flow, and cylinders or motors convert it back into force and motion. Hydraulic systems use oil at 10 to 40 MPa and give large forces, high stiffness and precise control in excavators, presses, aircraft flight controls and injection-moulding machines. Pneumatic systems use air at 0.5 to 1 MPa and give cheap, clean and fast motion between end stops in factory automation. This note covers Pascal's law and force multiplication, actuators, positive-displacement pumps and motors, valves and the orifice equation, line losses, accumulators, power and efficiency, and the effect of compressibility that separates pneumatics from hydraulics.

## Problem Statement

Given the loads and speeds an actuator must deliver, and the components of the circuit (pump displacement and speed, valve areas and discharge coefficients, line lengths and diameters, cylinder bore and rod diameters, fluid density, viscosity and bulk modulus), find the pressures and flows in the circuit, the forces and speeds of the actuators, the power drawn and lost, and the stiffness and natural frequency of the actuator with its load.

The fluid is a liquid of constant density (hydraulics) or an ideal gas (pneumatics); flows are quasi-steady except where the compressibility of the fluid is the point. The governing relations are hydrostatic pressure transmission ($p$ uniform in a static fluid, so $F = pA$), conservation of volume flow $Q = vA$ in each actuator chamber, the orifice equation $Q = C_dA\sqrt{2\Delta p/\rho}$ for valves, the Darcy–Weisbach equation for lines, and for transients the compressibility relation $dp/dt = (\beta/V)(Q_{\mathrm{in}} - Q_{\mathrm{out}} - dV/dt)$ for each fluid volume $V$ with bulk modulus $\beta$.

## Pascal's Law and Force Multiplication

In a fluid at rest, pressure is transmitted undiminished to every part of the fluid and acts normal to every surface; gravity adds only $\rho gh$, which is negligible at hydraulic pressures (see [Hydrostatics](../../fluid_mechanics/fluid_statics/hydrostatics.md)). Two pistons of areas $A_1$ and $A_2$ connected by a closed volume of liquid therefore carry forces in the ratio

$$
\frac{F_2}{F_1} = \frac{A_2}{A_1}
$$

Volume is conserved, $A_1x_1 = A_2x_2$, so the work done on the small piston equals the work done by the large one, $F_1x_1 = F_2x_2$: the force gain is paid for in displacement.

A hand press has a pump piston of 20 mm and a ram of 200 mm diameter, and the operator pushes the pump piston with 500 N. The pressure is $p = 500/(\pi \times 0.020^2/4) = 1.59$ MPa and the ram force $F_2 = pA_2 = 1.59 \times 10^6 \times 0.0314 = 50$ kN, a hundredfold gain equal to the area ratio $(200/20)^2$.

## Actuators

A double-acting cylinder with bore $D$ and rod diameter $d$ has the cap-side area $A_c = \pi D^2/4$ and the annulus area $A_a = \pi(D^2 - d^2)/4$. With supply pressure $p_s$ on one side and return pressure $p_r$ on the other, and ignoring seal friction,

$$
F_{\mathrm{ext}} = p_sA_c - p_rA_a,
\qquad F_{\mathrm{ret}} = p_sA_a - p_rA_c
$$

and for a supply flow $Q$ the piston speeds are $v_{\mathrm{ext}} = Q/A_c$ and $v_{\mathrm{ret}} = Q/A_a$. Retraction is faster and weaker than extension. The return flow differs from the supply flow by the area ratio, which matters when sizing return lines and filters. In a regenerative circuit the rod-side outflow is fed back to the cap side, so the extension speed rises to $Q/(A_c - A_a) = Q/(\pi d^2/4)$ while the force falls to $p_s\pi d^2/4$.

A cylinder of 100 mm bore and 50 mm rod at 15 MPa and 30 L/min ($5.0 \times 10^{-4}$ m³/s) has $A_c = 7.854 \times 10^{-3}$ m² and $A_a = 5.890 \times 10^{-3}$ m². It extends with 117.8 kN at 0.064 m/s and retracts with 88.4 kN at 0.085 m/s.

A rotary hydraulic motor of displacement $D_m$ per revolution, working across a pressure difference $\Delta p$, gives torque and speed

```math
T = \frac{\Delta p\,D_m}{2\pi}\eta_m,
\qquad n = \frac{Q}{D_m}\eta_v
```

with mechanical efficiency $\eta_m$ (friction) and volumetric efficiency $\eta_v$ (internal leakage); the overall efficiency is $\eta_m\eta_v$.

## Pumps

Hydraulic pumps are positive-displacement machines: each revolution moves a fixed volume $D$ from inlet to outlet, whatever the outlet pressure, so the flow is set by the speed and the pressure by the load. The delivered flow is

```math
Q = D\, n\,\eta_v
```

where $\eta_v$ accounts for leakage back across the clearances, which grows with pressure and falls with viscosity. A positive-displacement pump must never be dead-headed: with the outlet blocked the pressure rises until something breaks, so every circuit has a relief valve. This is the opposite of a centrifugal pump, whose head is limited and whose flow depends on the system (see [Rotating Machinery](rotating_machinery.md)).

| Pump type | Displacement | Typical maximum pressure | Notes |
| --- | --- | --- | --- |
| external gear | fixed | about 25 MPa | cheap, tolerant of contamination, noisy |
| vane | fixed or variable (eccentric ring) | about 20 MPa | quiet, moderate pressure |
| axial piston, swashplate | variable: $D = zA_pD_{pc}\tan\alpha$ | 35 to 45 MPa | $z$ pistons of area $A_p$ on pitch-circle diameter $D_{pc}$, swashplate angle $\alpha$; high efficiency |
| radial piston | fixed or variable | up to 70 MPa | very high pressure, low speed |

Variable-displacement pumps with pressure compensation reduce the displacement when the system pressure reaches a set value, so they deliver only the flow the actuators take instead of dumping the excess over a relief valve.

## Valves and the Orifice Equation

Valves control the direction, pressure and flow rate. Almost all of them meter flow through a short restriction, where the flow accelerates through a vena contracta and the pressure drop is set by inertia rather than viscosity. Bernoulli's equation between the upstream chamber and the vena contracta, with a discharge coefficient $C_d$ (about 0.6 to 0.7 for sharp-edged orifices and spool valves) for the contraction and losses, gives the orifice equation

$$
Q = C_dA \sqrt{\frac{2\Delta p}{\rho}}
$$

Flow varies with the square root of the pressure drop, so a plain throttle passes a load-dependent flow: an actuator controlled by a fixed orifice slows down as its load rises. A pressure-compensated flow control valve keeps the drop across its metering orifice constant with a spring-loaded compensator spool, so the flow stays constant.

| Valve | Function |
| --- | --- |
| directional control (for example 4/3: four ports, three positions) | connects pump, tank and the two actuator ports; the centre position (closed, open or tandem) decides what the actuator and pump do at rest |
| check valve | free flow in one direction, none in the other |
| relief valve | opens to tank when the pressure reaches its setting $p = F_{\mathrm{spring}}/A$; protects the circuit |
| pressure-reducing valve | holds a lower pressure in a branch circuit |
| sequence valve | opens a second branch only when the first has reached a set pressure |
| counterbalance valve | holds back an overrunning load, such as a lowering boom |
| flow control (throttle, pressure-compensated) | sets actuator speed |
| proportional and servo valves | spool position proportional to an electrical signal, for closed-loop position, speed or force control |

Speed control by a throttle in the supply line is called meter-in and suits loads that resist motion; a throttle in the return line (meter-out) holds back loads that try to run away, because it keeps a back-pressure on the actuator.

## Line Losses

Flow through lines, hoses and fittings loses pressure according to the [Darcy–Weisbach equation](../../fluid_mechanics/internal_flow/pipes.md),

$$
\Delta p = \left(f \frac{L}{D} + \sum K\right) \frac{\rho v^2}{2}
$$

with $f = 64/Re$ for laminar flow ($Re < 2000$, common in hydraulic lines because of the high oil viscosity) and from the Colebrook equation or the Moody chart for turbulent flow. Oil of $\nu = 32$ cSt and $\rho = 870$ kg/m³ at 30 L/min in a hose of 12 mm bore flows at 4.42 m/s with $Re = 1660$, so $f = 0.0386$ and a 5 m hose loses 0.14 MPa. Recommended line velocities are about 1 m/s in suction lines (to avoid cavitation at the pump inlet), 3 to 5 m/s in pressure lines and 2 to 3 m/s in return lines. The viscosity of oil falls steeply with temperature, so the losses of a cold circuit at start-up can be several times the running values.

## Accumulators

An accumulator stores liquid under pressure against a gas charge (usually nitrogen behind a bladder, diaphragm or piston). It supplies peak flows larger than the pump can deliver, maintains pressure during pump failure, and absorbs pressure pulsations and shocks. With precharge pressure $p_0$ and gas volume $V_0$, and minimum and maximum working pressures $p_1$ and $p_2$ (absolute), the gas volumes follow $pV^n = $ constant, with $n = 1$ for slow (isothermal) and $n \approx 1.4$ for fast (adiabatic) processes. The usable liquid volume between $p_2$ and $p_1$ is

$$
\Delta V = V_2\left[\left(\frac{p_2}{p_1}\right)^{1/n} - 1\right],
\qquad V_2 = V_0\left(\frac{p_0}{p_2}\right)^{1/n_c}
$$

where $n_c$ is the exponent of the charging process. A 10 L accumulator precharged to 9 MPa and charged slowly to 20 MPa has $V_2 = 10 \times 9/20 = 4.5$ L of gas. Discharged slowly to 10 MPa it delivers $4.5(20/10 - 1) = 4.5$ L; discharged quickly it delivers $4.5(2^{1/1.4} - 1) = 2.9$ L, because the gas cools as it expands. The precharge is usually set at about 90% of $p_1$, so the bladder does not slam against the poppet at the lowest working pressure.

## Hydraulic Power and Efficiency

The power carried by a flow $Q$ at pressure $p$ is

$$
P = pQ
$$

so a pump delivering 30 L/min at 15 MPa supplies 7.5 kW. Every pressure drop $\Delta p$ across a valve or line at flow $Q$ turns $`\Delta p\,Q`$ into heat. A fixed-displacement pump whose excess flow goes over the relief valve at full pressure converts all of that excess power into heat, which is why such circuits need oil coolers and why load-sensing and variable-displacement pumps, which set the pump pressure just above the highest load pressure and deliver only the flow needed, are used on mobile machines. The input shaft power of a pump is $P_{\mathrm{in}} = pQ/(\eta_v\eta_m)$.

## Pneumatics

### Compression

Air is compressed from atmospheric pressure, and the work depends on the process. For $V_1$ of free air at $p_1$ compressed to $p_2$,

$$
W_{\mathrm{iso}} = p_1V_1\ln \frac{p_2}{p_1},
\qquad
W_{\mathrm{ad}} = \frac{\gamma}{\gamma - 1}p_1V_1\left[\left(\frac{p_2}{p_1}\right)^{(\gamma - 1)/\gamma} - 1\right]
$$

with $\gamma = 1.4$ for air (see [Thermodynamics](../../fluid_mechanics/compressible_flow/thermodynamics.md)). Real compressors are close to adiabatic, and the delivery temperature $T_2 = T_1(p_2/p_1)^{(\gamma - 1)/\gamma}$ is high, so multistage compressors cool the air between stages, which brings the process nearer the isothermal one. The compressed air is dried, filtered and regulated before use; the water condensing from it is the main source of corrosion and malfunction in pneumatic systems. Compressed air is an expensive form of energy: only 10 to 20% of the electrical input to the compressor ends up as useful work at the actuators.

### Compressibility and Positioning

The fundamental difference between hydraulics and pneumatics is the stiffness of the working fluid. A column of fluid of volume $V$ under a piston of area $A$ acts as a spring of stiffness

$$
k = \frac{\beta A^2}{V}
$$

where $\beta$ is the bulk modulus: about 1.5 GPa for mineral oil (lower with entrained air), and $\gamma p$ for air in fast, adiabatic compression, 0.84 MPa at 0.6 MPa absolute. For a 50 mm bore with 200 mm of trapped fluid ($V = 3.9 \times 10^{-4}$ m³), the oil spring is $k = 1.47 \times 10^7$ N/m and the air spring $k = 8.2 \times 10^3$ N/m, 1800 times softer. With a moving mass of 20 kg the hydraulic actuator has a natural frequency of 137 Hz and the pneumatic one 3.2 Hz.

This is why pneumatic positioning between end stops is easy and in between is hard:

1. The low natural frequency limits the bandwidth of any position loop to a few hertz, and external force changes produce large position errors.
2. The stiffness depends on the pressure and on the piston position (through $V$), so the plant is strongly nonlinear.
3. Seal friction is large compared with the driving force differences near rest, which gives stick-slip and limit cycles.
4. Valve flow is nonlinear and chokes at pressure ratios below about 0.53 (see [Isentropic Flow](../../fluid_mechanics/compressible_flow/isentropic_flow.md)), and the air temperature changes during each stroke.

Servo-pneumatic systems overcome part of this with proportional valves, chamber pressure feedback and model-based control, reaching accuracies of a fraction of a millimetre; most pneumatic actuators still run between mechanical stops with cushioning at the ends. Hydraulic servo systems are analysed with the same compressibility relation, in which the oil spring and the load mass give the hydraulic resonance that limits their bandwidth; see [Feedback Control](../control_systems/feedback_control.md).

## Circuit Symbols

Fluid power circuits are drawn with the graphic symbols of ISO 1219-1. The main ones are:

| Component | Symbol |
| --- | --- |
| hydraulic pump, fixed displacement | circle with one solid triangle pointing outward on the outlet side |
| hydraulic motor | circle with a solid triangle pointing inward |
| compressor or air motor | the same circles with hollow triangles |
| variable displacement | a diagonal arrow drawn through the pump or motor circle |
| double-acting cylinder | rectangle with a piston line and a rod leaving one end, a port at each end |
| directional control valve | one square per position, side by side; arrows inside show flow paths, a T shows a blocked port; the actuating method (lever, spring, solenoid, pilot) is drawn at the ends |
| check valve | ball sitting in a V-shaped seat |
| relief valve | square with an arrow offset from the flow line, a spring on one side and a dashed pilot line from the inlet on the other |
| flow control valve | two arcs forming a restriction, with a diagonal arrow if adjustable |
| accumulator | vertical oval (capsule) on a line |
| filter | diamond with a dashed line across it |
| reservoir (tank) | open-topped rectangle |
| working, pilot and drain lines | solid, long-dashed and short-dashed lines |

## Key Takeaways

- Pressure is uniform in a static fluid, so force scales with area; volume conservation makes the displacement scale inversely, and work is conserved.
- Cylinders extend with $p_sA_c$ at $Q/A_c$ and retract faster and weaker with the annulus area.
- Positive-displacement pumps deliver $Q = Dn\eta_v$ regardless of pressure; the load sets the pressure and a relief valve limits it.
- Valves follow $Q = C_dA\sqrt{2\Delta p/\rho}$, so plain throttles give load-dependent speed; every pressure drop $`\Delta p\,Q`$ becomes heat.
- Accumulators deliver less volume in fast (adiabatic) discharge than in slow (isothermal) discharge.
- The air spring $\gamma pA^2/V$ is three orders of magnitude softer than the oil spring $\beta A^2/V$, which is why pneumatic positioning is hard.

## Related Scripts

- [Pump and System Curves](../../../scripts/plots/hydraulics_pump_system_curve/): plots the head–flow curves of a centrifugal pump at four speeds from the affinity laws, the curve of the pipe system it feeds, and the operating points where they meet.

## Exercises

**Exercise 1.** In the hand press of the text (pump piston 20 mm, ram 200 mm, pump force 500 N), each pump stroke moves the pump piston 50 mm. How far does the ram rise per stroke, how many strokes raise it by 20 mm, and does the work balance?

<details>
<summary>Answer</summary>

Volume conservation $A_1x_1 = A_2x_2$ with $A_2/A_1 = 100$ gives $x_2 = 50/100 = 0.5$ mm per stroke, so a 20 mm rise takes $20/0.5 = 40$ strokes.

Work per stroke: input $500 \times 0.050 = 25$ J, output $`50\,000 \times 0.0005 = 25`$ J. The hundredfold force gain is paid for with a hundredfold loss of displacement.

</details>

**Exercise 2.** A double-acting cylinder must push 40 kN on extension from a 12 MPa supply. (a) Find the minimum bore, ignoring friction and back-pressure. (b) A 70 mm bore is chosen. What extension force does it give, and what flow rate gives an extension speed of 0.1 m/s?

<details>
<summary>Answer</summary>

(a)

```math
D_{\min} = \sqrt{\frac{4F}{\pi p}} = \sqrt{\frac{4 \times 40\,000}{\pi \times 12 \times 10^6}} = 0.0651 \text{ m} = 65.1 \text{ mm}
```

(b) $A = \pi(0.070)^2/4 = 3.848 \times 10^{-3}$ m², so $F = pA = 46.2$ kN, a margin of about 15% for seal friction and back-pressure.

```math
Q = vA = 0.1 \times 3.848 \times 10^{-3} = 3.85 \times 10^{-4} \text{ m}^3\text{/s} = 23.1 \text{ L/min}
```

</details>

**Exercise 3.** A hydraulic motor has displacement $D_m = 40$ cm³/rev and works across $\Delta p = 18$ MPa with a supply of 50 L/min. Its volumetric efficiency is 0.94 and its mechanical efficiency 0.90. Find the output torque, speed, output power and overall efficiency.

<details>
<summary>Answer</summary>

```math
T = \frac{\Delta p\, D_m}{2\pi}\eta_m = \frac{18 \times 10^6 \times 40 \times 10^{-6}}{2\pi} \times 0.90 = 103.1 \text{ N m}
```

```math
n = \frac{Q}{D_m}\eta_v = \frac{50\,000 \text{ cm}^3\text{/min}}{40 \text{ cm}^3} \times 0.94 = 1175 \text{ rpm}
```

Output power: $T\omega = 103.1 \times (1175 \times 2\pi/60) = 12.69$ kW. Hydraulic input: $`\Delta p\,Q = 18 \times 10^6 \times 8.333 \times 10^{-4} = 15.0`$ kW. Overall efficiency: $12.69/15.0 = 0.846$, which equals $\eta_v\eta_m$.

</details>

**Exercise 4.** A flow control orifice has $C_d = 0.62$ and diameter 2.5 mm, and the oil density is 870 kg/m³. (a) Find the flow at $\Delta p = 4$ MPa. (b) What pressure drop halves the flow? (c) Why does this matter for actuator speed control, and how much power does the orifice dissipate in (a)?

<details>
<summary>Answer</summary>

(a) $A = \pi(0.0025)^2/4 = 4.909 \times 10^{-6}$ m²:

```math
Q = C_d A \sqrt{\frac{2\Delta p}{\rho}} = 0.62 \times 4.909 \times 10^{-6} \times \sqrt{\frac{2 \times 4 \times 10^6}{870}} = 2.92 \times 10^{-4} \text{ m}^3\text{/s} = 17.5 \text{ L/min}
```

(b) $Q \propto \sqrt{\Delta p}$, so halving the flow needs a quarter of the pressure drop: 1 MPa.

(c) A change in load changes the pressure drop across a plain orifice, so the actuator speed drifts with load; a pressure-compensated valve holds the drop constant. The orifice dissipates $`\Delta p\,Q = 4 \times 10^6 \times 2.92 \times 10^{-4} = 1.17`$ kW as heat.

</details>

**Exercise 5.** A compressor takes 1 m³ of free air at 101.3 kPa and 20 °C and delivers it at 700 kPa absolute. Compare the isothermal and adiabatic compression work, and find the adiabatic delivery temperature. Why do industrial compressors use intercooling?

<details>
<summary>Answer</summary>

Pressure ratio: $700/101.3 = 6.910$.

```math
W_{\mathrm{iso}} = p_1 V_1 \ln \frac{p_2}{p_1} = 101\,300 \times 1 \times \ln 6.910 = 195.8 \text{ kJ}
```

```math
W_{\mathrm{ad}} = \frac{1.4}{0.4} \times 101\,300 \times \left(6.910^{0.2857} - 1\right) = 261.4 \text{ kJ}
```

```math
T_2 = T_1\left(\frac{p_2}{p_1}\right)^{(\gamma - 1)/\gamma} = 293.15 \times 6.910^{0.2857} = 509 \text{ K} \approx 236^\circ\text{C}
```

Adiabatic compression needs about 33% more work. Staged compression with intercooling brings the process closer to isothermal, which saves work and keeps the delivery temperature within what oil and seals can tolerate.

</details>

## References

- Esposito, A., *Fluid Power with Applications*, 7th ed., Pearson Prentice Hall, 2009.
- Merritt, H. E., *Hydraulic Control Systems*, Wiley, 1967.
- Manring, N. D., *Hydraulic Control Systems*, Wiley, 2005.
- Beater, P., *Pneumatic Drives: System Design, Modelling and Control*, Springer, 2007.
- Parr, A., *Hydraulics and Pneumatics: A Technician's and Engineer's Guide*, 3rd ed., Butterworth-Heinemann, 2011.
- ISO 1219-1:2012, *Fluid power systems and components — Graphical symbols and circuit diagrams — Part 1: Graphical symbols for conventional use and data-processing applications*, International Organization for Standardization, 2012.
