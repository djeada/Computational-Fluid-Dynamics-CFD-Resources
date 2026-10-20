# Rotating Machinery

Turbines, compressors, pumps, fans, electric motors and spindles are rotors carried on bearings, and two questions decide whether they work. The structural one is rotor dynamics: at which speeds the rotor whirls violently, how large the vibration from residual unbalance is, and how to balance it. The fluid one is turbomachinery: how the blades exchange energy with the flow, what head and flow a pump delivers into a given pipe system, and when it cavitates. This note treats the Jeffcott rotor, critical speeds, gyroscopic effects and the Campbell diagram, single- and two-plane balancing and flywheels, then the Euler turbomachine equation, velocity triangles, specific speed, pump and system curves, the affinity laws and NPSH. Pipe losses are covered in [Pipe Flow](../../fluid_mechanics/internal_flow/pipes.md) and the bearings that support the rotor in [Bearings and Lubrication](bearings.md).

## Problem Statement

For the rotor: given the rotor mass, inertias and unbalance, the shaft stiffness and the support damping, find the critical speeds, the steady unbalance response (amplitude and phase) over the speed range, the dependence of the natural frequencies on speed, and the correction masses that balance the rotor. The model is linear, the supports isotropic and the disks rigid; the governing equations are the equations of lateral motion in complex form,

```math
\mathbf{M}\ddot{\mathbf{q}} +
\left(\mathbf{C} - i\Omega\mathbf{G}\right)\dot{\mathbf{q}} +
\mathbf{K}\mathbf{q} = \mathbf{f}\,\Omega^2 e^{i\Omega t}
```

with $\mathbf{q}$ the complex displacements and tilts, $\Omega$ the spin speed, $\mathbf{G}$ the gyroscopic matrix and $\mathbf{f}$ the unbalance.

For the turbomachine: given the impeller geometry and speed, find the ideal head from the Euler equation; given the pump characteristic, the system (static head and pipe losses) and the suction conditions, find the operating point, its change with speed, the shaft power and the margin against cavitation. The flow is steady and incompressible; the Euler equation is exact for the momentum exchange, and losses enter through measured efficiencies.

## Rotor Dynamics

### The Jeffcott Rotor

The simplest model is a disk of mass $m$ at the middle of a massless shaft of lateral stiffness $k$, with viscous damping $c$ acting on the disk centre. The mass centre of the disk is a distance $e$ (the eccentricity) from the shaft axis. With $z = x + iy$ the position of the shaft centre at the disk and the rotor spinning at constant $\Omega$, the mass centre is at $`z + e\,e^{i\Omega t}`$, and Newton's law gives

```math
m\ddot z + c\dot z + kz = me\,\Omega^2 e^{i\Omega t}
```

The unbalance acts as a force rotating with the shaft. With $\omega_n = \sqrt{k/m}$, $\zeta = c/(2\sqrt{km})$ and $s = \Omega/\omega_n$, the steady response is a circular synchronous whirl $z = |z|e^{i(\Omega t - \phi)}$ with

$$
\frac{|z|}{e} = \frac{s^2}{\sqrt{(1 - s^2)^2 + (2\zeta s)^2}},
\qquad \tan\phi = \frac{2\zeta s}{1 - s^2}
$$

where $\phi$ is the angle by which the shaft displacement (the high spot) lags the heavy spot. Three regimes follow:

1. Below the critical speed ($s \ll 1$) the shaft bows towards the heavy spot, $\phi \approx 0$ and $|z| \approx e s^2$.
2. At the critical speed $\Omega = \omega_n$ the phase lag is exactly 90° for any damping and $|z|/e = 1/(2\zeta)$. The peak is $1/(2\zeta\sqrt{1 - \zeta^2})$ at $s = 1/\sqrt{1 - 2\zeta^2}$, slightly above $\omega_n$.
3. Above the critical speed $\phi \to 180^\circ$ and $|z| \to e$: the heavy spot moves to the inside of the whirl orbit and the disk turns about its own mass centre. This self-centring is what lets flexible rotors run smoothly above their first critical speed.

![Jeffcott rotor unbalance response amplitude and phase for several damping ratios, and the Campbell diagram of an overhung disk](../../../scripts/algorithms/rotor_jeffcott_campbell/rotor_jeffcott_campbell.png)

Panels (a) and (b) show the response for $\zeta = 0.05$ to $0.5$; the circles come from integrating the equation of motion in time and agree with the formula to $10^{-6}$. Note that every phase curve passes through 90° at $\Omega = \omega_n$: in a run-up test the critical speed is located from the phase, which is sharper than the amplitude peak when the damping is large.

The whirl in the Jeffcott model is synchronous and the shaft does not flex cyclically: the bent shaft turns as a whole, so the bending stress is steady, not alternating. The loads are transmitted to the bearings as a rotating force $k|z|$, which is what the vibration sensors measure.

### Critical Speed of a Shaft with a Disk

For a disk at the middle of a simply supported shaft of span $L$ and flexural rigidity $EI$, $k = 48EI/L^3$ and

$$
\omega_c = \sqrt{\frac{48EI}{mL^3}} = \sqrt{\frac{g}{\delta_{st}}}
$$

with $\delta_{st}$ the static deflection under the disk weight. For a shaft with several disks, two classical estimates bracket the first critical speed. Rayleigh's method equates the maximum kinetic and strain energies with the static deflection curve as the mode shape and gives an upper bound,

$$
\omega_c^2 \approx \frac{g\sum m_i\delta_i}{\sum m_i\delta_i^2}
$$

with $\delta_i$ the static deflection at disk $i$ under all the disk weights. Dunkerley's formula combines the critical speeds $\omega_i$ of each disk alone and $\omega_s$ of the shaft alone and gives a lower bound,

$$
\frac{1}{\omega_c^2} \approx \frac{1}{\omega_s^2} + \sum_i \frac{1}{\omega_i^2}
$$

For real rotors the critical speeds come from finite-element rotor models that include the bearing stiffness and damping, which lower the critical speeds well below the rigid-support values when the bearings are soft. A rigid rotor is designed to run well below its first critical speed (commonly below about 70% of it), a flexible rotor between critical speeds with a separation margin of 15 to 20% from each, accelerating quickly through the criticals it must pass.

### Gyroscopic Effects and the Campbell Diagram

When a disk is not at a node of tilt, the mode involves tilting of the spinning disk and gyroscopic moments appear. Consider a rigid disk of mass $m$, polar moment $I_p$ and diametral moment $I_d$ at the free end of a cantilever shaft of length $L$. With complex translation $u$ and tilt $\psi$ of the disk, and $\mathbf{K}$ the inverse of the cantilever flexibility matrix $`\frac{1}{EI}\begin{bmatrix} L^3/3 & L^2/2 \\ L^2/2 & L\end{bmatrix}`$,

$$
m\ddot u + k_{11}u + k_{12}\psi = 0,
\qquad I_d\ddot\psi - iI_p\Omega\dot\psi + k_{21}u + k_{22}\psi = 0
$$

The term $-iI_p\Omega\dot\psi$ is the gyroscopic moment, perpendicular to the tilt velocity. Free whirl $u, \psi \propto e^{i\lambda t}$ gives the frequency equation

$$
\left(k_{11} - m\lambda^2\right)\left(k_{22} - I_d\lambda^2 + I_p\Omega\lambda\right) -
k_{12}^2 = 0
$$

Positive roots $\lambda$ are forward whirl (the orbit turns with the spin), negative roots backward whirl. At $\Omega = 0$ the two are equal; as the speed rises, the gyroscopic moment stiffens the forward modes and softens the backward ones. A plot of the whirl frequencies against speed is a **Campbell diagram**. A critical speed is an intersection with the line of the excitation, 1X for unbalance: setting $\lambda = \Omega$ gives

$$
m(I_d - I_p)\Omega^4 - \left[mk_{22} + (I_d - I_p)k_{11}\right]\Omega^2 +
\det\mathbf{K} = 0
$$

For the steel disk of radius 150 mm and thickness 30 mm on a 20 mm shaft overhung by 100 mm in panel (c) of the figure, the non-rotating frequencies are 53.1 Hz and 206.5 Hz. The first forward branch is stiffened so much that it meets the 1X line only at 8101 rpm (135 Hz), not at the 3186 rpm the non-rotating frequency suggests. For a thin disk $I_p > I_d$, the quartic in $\Omega$ has only one positive root and the second forward mode never becomes critical. Unbalance excites only forward synchronous whirl when the supports are isotropic; the backward crossings at 2097 and 10 916 rpm matter only when the bearing stiffness differs between directions. Campbell diagrams are also used for blades and disks, with excitation lines at multiples of speed set by the number of upstream vanes or struts.

Not all whirl is driven by unbalance. Cross-coupled forces from oil-film bearings, seals and internal friction in the rotor can make a forward mode self-excited above some speed; the classical example is oil whip, where a journal bearing drives subsynchronous whirl at about half running speed once the speed exceeds twice the first critical speed. Tilting-pad bearings and seals with swirl brakes are the usual cures.

## Balancing

### Single-Plane (Static) Balancing

A thin rotor, such as a fan disk or a grinding wheel, can be balanced in one plane. Masses $m_i$ at radii $r_i$ and angles $\theta_i$ produce the rotating force $\Omega^2\sum m_ir_ie^{i\theta_i}$. It is cancelled by a correction mass at the angle opposite the resultant, with

$$
m_br_b = \left|\sum_i m_ir_ie^{i\theta_i}\right|,
\qquad
\theta_b = \mathrm{atan2}\left(-\sum m_ir_i\sin\theta_i,\ - \sum
m_ir_i\cos\theta_i\right)
$$

A rotor in static balance stays at rest in any angular position on knife edges, which is how this kind of balance can be checked without rotation.

### Two-Plane (Dynamic) Balancing

A long rotor in static balance can still carry an unbalanced couple, with equal and opposite unbalances at its two ends. Force and moment must both vanish, and any distribution of unbalance can be cancelled by two correction masses in two chosen planes A and B a distance $l_{AB}$ apart. Taking moments about plane A,

$$
\sum_i m_ir_il_ie^{i\theta_i} + m_Br_Bl_{AB}e^{i\theta_B} = 0,
\qquad \sum_i m_ir_ie^{i\theta_i} + m_Ar_Ae^{i\theta_A} + m_Br_Be^{i\theta_B} = 0
$$

with $l_i$ the axial position of mass $i$ from plane A. The first equation gives the correction in plane B, the second then the correction in plane A.

### Influence Coefficients

In the field the unbalance is unknown and is found from vibration measurements. For one plane: measure the vibration $V_0$ (amplitude and phase relative to a once-per-revolution mark), add a known trial mass $U_t$, measure $V_1$, and compute the influence coefficient $\alpha = (V_1 - V_0)/U_t$. Because the system is linear, the correction that cancels $V_0$ is $U_c = -V_0/\alpha$. For example, with $V_0 = 80$ μm at 30° and $V_1 = 50$ μm at 120° after a 10 g trial mass at 0°, $\alpha = 9.43$ μm/g at 178.0° and the correction is 8.48 g at 32.0°. Two planes need two trial runs and a $2 \times 2$ complex matrix of influence coefficients. Flexible rotors running above several critical speeds are balanced at several speeds or by modal balancing, one mode at a time.

### Balance Quality

ISO 21940-11 (formerly ISO 1940-1) specifies the permissible residual unbalance through a balance quality grade $G = e_{\mathrm{per}}\Omega$ in mm/s, with $e_{\mathrm{per}}$ the permissible mass-centre eccentricity. Grade G 6.3 applies to general machinery such as pumps and fans, G 2.5 to gas and steam turbines and machine-tool drives. A 50 kg turbine rotor at 3000 rpm ($\Omega = 314.2$ rad/s) balanced to G 2.5 may have $e_{\mathrm{per}} = 2.5/314.2 = 7.96$ μm, a residual unbalance of $50 \times 7.96 \times 10^{-3} = 0.40$ kg·mm (398 g·mm), split between its two correction planes.

## Flywheels

A flywheel stores kinetic energy $E = \tfrac{1}{2}I\Omega^2$ to smooth the speed of a machine whose driving or load torque varies over a cycle, such as an engine or a punch press. If $\Delta E$ is the largest excess of energy delivered over energy absorbed during a cycle, the speed varies between $\Omega_{\max}$ and $\Omega_{\min}$ with

$$
\Delta
E = \tfrac{1}{2}I\left(\Omega_{\max}^2 - \Omega_{\min}^2\right) = IC_f\bar\Omega^2,
\qquad C_f = \frac{\Omega_{\max} - \Omega_{\min}}{\bar\Omega}
$$

$C_f$ is the coefficient of speed fluctuation, about 0.002 for generators, 0.02 for machine tools and 0.1 to 0.2 for punch presses. A punch press that takes 5 kJ per stroke at a mean speed of 300 rpm with $C_f = 0.15$ needs $I = 5000/(0.15 \times 31.42^2) = 33.8$ kg m². The speed of a flywheel is limited by the stress from rotation, which for a solid disk of radius $r$ peaks at the centre at $\sigma_{\max} = \tfrac{3 + \nu}{8}\rho\Omega^2r^2$; since $E \propto \Omega^2$, a flywheel geared to run faster needs much less inertia.

## Turbomachinery

### The Euler Turbomachine Equation

A rotor with blades exchanges energy with a fluid by changing its angular momentum. Apply the angular-momentum balance to a control volume enclosing the rotor in steady flow, with the fluid entering at radius $r_1$ and leaving at $r_2$, and let $c_u$ be the tangential (whirl) component of the absolute velocity. The torque on the fluid is

$$
T = \rho Q\left(r_2c_{u2} - r_1c_{u1}\right)
$$

and the power $T\Omega$, divided by the weight flow $\rho gQ$, gives the head added to the fluid,

$$
H_E = \frac{u_2c_{u2} - u_1c_{u1}}{g}
$$

with $u = \Omega r$ the blade speed. This is the Euler turbomachine equation. It holds for pumps, fans and compressors (positive head) and turbines (negative), for radial and axial machines alike, and it is exact for the ideal flow that follows the blades; losses, recirculation and the slip of the flow relative to the blades make the real head smaller.

### Velocity Triangles

At inlet and outlet the absolute velocity $\mathbf{c}$ is the sum of the velocity $\mathbf{w}$ relative to the blade and the blade velocity $\mathbf{u}$:

$$
\mathbf{c} = \mathbf{w} + \mathbf{u}
$$

The relative velocity leaves the blade approximately along the blade, at the blade angle $\beta_2$ measured from the tangential direction. For a centrifugal pump with impeller outlet diameter $D_2$ and width $b_2$, the radial (meridional) velocity is $c_{r2} = Q/(\pi D_2b_2)$, so the outlet triangle gives $c_{u2} = u_2 - c_{r2}\cot\beta_2$. With no inlet whirl ($c_{u1} = 0$), the ideal head is

$$
H_E = \frac{u_2^2}{g} - \frac{u_2\cot\beta_2}{g\pi D_2b_2}Q
$$

a straight line in $Q$. Backward-curved blades ($\beta_2 < 90^\circ$, usually 20° to 30°) give a head that falls with flow, which makes the operating point stable in any system and keeps the power curve from rising without limit. Forward-curved blades give a rising head and are used only in small fans. Slip (the flow leaves at a smaller angle than the blade) lowers the head by a slip factor, roughly 0.8 to 0.9; friction and shock losses at off-design flow bend the line into the measured head curve.

### Dimensional Analysis and Specific Speed

For geometrically similar machines of diameter $D$ running at $\Omega$, dimensional analysis reduces the performance to relations between the flow coefficient $\phi = Q/(\Omega D^3)$, the head coefficient $\psi = gH/(\Omega^2D^2)$, the power coefficient $P/(\rho\Omega^3D^5)$ and the efficiency, with the Reynolds number a weak secondary influence. Eliminating $D$ between $\phi$ and $\psi$ gives the specific speed, here in its dimensionless form evaluated at the best-efficiency point,

$$
\Omega_s = \frac{\Omega\sqrt{Q}}{(gH)^{3/4}}
$$

It depends only on the duty, not on the size, and selects the type of machine: radial (centrifugal) impellers for $\Omega_s$ below about 1, mixed-flow impellers between about 1 and 3, axial propellers above about 3. A pump delivering 25 L/s at 30 m and 1450 rpm has $\Omega_s = 151.8 \times 0.158/294.3^{0.75} = 0.34$, a typical centrifugal pump.

### Pump and System Curves

The system a pump feeds needs a head that rises with flow: the static head $H_s$ (elevation plus pressure difference between the two reservoirs) plus the friction and fitting losses from the [Darcy–Weisbach equation](../../fluid_mechanics/internal_flow/pipes.md),

$$
H_{\mathrm{sys}} = H_s + \left(f \frac{L}{D} + \sum K\right) \frac{8Q^2}{g\pi^2D^4}
$$

The pump operates where its head curve crosses the system curve. Its shaft power there is $P = \rho gQH/\eta$, and a good selection puts that point close to the best-efficiency point. Two pumps in series add their heads at the same flow; two in parallel add their flows at the same head, and with a steep system curve the second pump adds little flow.

![Pump head curves at four speeds with constant-efficiency lines, the system curve and operating points, the shaft power for throttling and speed control, and NPSH available against required](../../../scripts/plots/hydraulics_pump_system_curve/hydraulics_pump_system_curve.png)

In panel (a) the pump ($`H = 40 - 16\,000Q^2`$ at 1450 rpm, BEP 78% at 25 L/s) feeds a system with 15 m static head and a 120 m, 100 mm pipe ($`H_{\mathrm{sys}} = 15 + 23\,962Q^2`$). It runs at 25.0 L/s and 30.0 m with 9.42 kW of shaft power. At 1000 rpm it delivers 10.0 L/s at 64% efficiency: the operating points move along the system curve, not along a similarity parabola, so the efficiency drops when the static head is a large part of the total.

### Affinity Laws and Flow Control

For similar operating points of one pump at speeds $n_1$ and $n_2$ the dimensionless coefficients are equal, so

$$
\frac{Q_2}{Q_1} = \frac{n_2}{n_1},
\qquad \frac{H_2}{H_1} = \left(\frac{n_2}{n_1}\right)^2,
\qquad \frac{P_2}{P_1} = \left(\frac{n_2}{n_1}\right)^3
$$

and the same laws with $D$ in place of $n$ (and exponents 3, 2 and 5) apply approximately to trimming the impeller. The flow can be reduced by throttling a valve, which adds a loss and moves the pump up its curve at constant speed, or by lowering the speed with a variable-frequency drive. In panel (b), 70% of the design flow costs 8.48 kW by throttling and 5.03 kW at 1197 rpm. The cube law makes speed control the dominant energy saving in pump and fan systems with variable demand.

### Cavitation and NPSH

Where the static pressure in the impeller eye falls to the vapour pressure $p_v$ the liquid boils locally; the vapour bubbles collapse when they reach higher pressure, which erodes the blades, makes noise and lowers the head. The margin is expressed as the net positive suction head, the total head at the pump inlet above the vapour-pressure head. For a pump a height $z$ above an open sump at atmospheric pressure, with suction-line loss $h_{f,s}$,

$$
\mathrm{NPSH}_a = \frac{p_{\mathrm{atm}} - p_v}{\rho g} - z - h_{f,s}
$$

The manufacturer gives the required value $\mathrm{NPSH}_r$, measured as the inlet head at which the pump head drops by 3%; it rises with flow and scales with $n^2$. The installation must have $\mathrm{NPSH}_a$ above $\mathrm{NPSH}_r$ with a margin, typically 0.5 to 1 m or a factor of 1.1 to 1.5. In panel (c), with a 3 m suction lift, the pump has 6.11 m available against 3.00 m required at the design flow with water at 20 °C. At 80 °C the vapour pressure is 47.4 kPa and only 1.66 m is available, so the same installation cavitates; hot liquids, high altitude, long suction lines and high speed all reduce the margin, and the usual remedy is to lower the pump below the liquid level.

## Key Takeaways

- An unbalanced rotor whirls synchronously with amplitude $`e\,s^2/\sqrt{(1 - s^2)^2 + (2\zeta s)^2}`$; the phase lag is 90° at the critical speed and approaches 180° above it, where the rotor self-centres.
- Gyroscopic moments split each tilting mode into a forward branch that stiffens and a backward branch that softens with speed; critical speeds are the crossings of the Campbell diagram with the 1X line.
- One correction plane removes a static unbalance; two planes are needed for a couple. Influence coefficients find the corrections from measured vibration.
- The Euler equation $H = (u_2c_{u2} - u_1c_{u1})/g$ gives the ideal head from the velocity triangles; backward-curved blades give a falling, stable head curve.
- A pump runs where its curve meets the system curve; the affinity laws $Q \propto n$, $H \propto n^2$, $P \propto n^3$ make speed control far cheaper than throttling.
- Check $\mathrm{NPSH}_a > \mathrm{NPSH}_r$ at the highest flow and the hottest liquid.

## Related Scripts

- [Jeffcott Rotor and Campbell Diagram](../../../scripts/algorithms/rotor_jeffcott_campbell/): computes the unbalance response of a Jeffcott rotor, amplitude and phase against speed for several damping ratios, and the Campbell diagram of an overhung disk whose gyroscopic moment splits each whirl mode into a forward and a backward branch.
- [Pump and System Curves](../../../scripts/plots/hydraulics_pump_system_curve/): plots the head–flow curves of a centrifugal pump at four speeds from the affinity laws, the curve of the pipe system it feeds, and the operating points where they meet.

## Exercises

**Exercise 1.** A steel shaft ($E = 200$ GPa) of diameter 25 mm is simply supported over a span of 0.6 m and carries a 15 kg disk at mid-span. Neglecting the shaft mass, find the critical speed and the static deflection under the disk. The disk has a mass eccentricity of 20 μm and the damping ratio is 0.02. Find the whirl amplitude at the critical speed and at 3000 rpm, and the phase lag at 3000 rpm.

<details>
<summary>Answer</summary>

```math
I = \frac{\pi d^4}{64} = 1.917 \times 10^{-8} \text{ m}^4, \quad k = \frac{48EI}{L^3} = 8.52 \times 10^5 \text{ N/m}
```

$\omega_c = \sqrt{k/m} = 238.4$ rad/s, or 2276 rpm. The static deflection is $\delta_{st} = mg/k = 0.173$ mm, and $\sqrt{9.81/1.727 \times 10^{-4}} = 238.4$ rad/s agrees.

At the critical speed $|z| = e/(2\zeta) = 20/0.04 = 500$ μm.

At 3000 rpm, $s = 314.16/238.4 = 1.318$:

```math
\frac{|z|}{e} = \frac{1.737}{\sqrt{(1 - 1.737)^2 + (2 \times 0.02 \times 1.318)^2}} = 2.35, \qquad |z| = 47 \text{ μm}
```

and $\phi = \mathrm{atan2}(0.0527, -0.737) = 175.9^\circ$: above the critical speed the heavy spot is almost opposite the high spot. The rotor must pass through 500 μm of whirl during run-up, which is why flexible rotors accelerate quickly through their critical speeds.

</details>

**Exercise 2.** The shaft of Exercise 1, on its own, has a first critical speed of 600 rad/s from its distributed mass. Use Dunkerley's formula to estimate the critical speed of the shaft with the disk.

<details>
<summary>Answer</summary>

```math
\frac{1}{\omega_c^2} = \frac{1}{238.4^2} + \frac{1}{600^2} \implies \omega_c = 221.5 \text{ rad/s} = 2115 \text{ rpm}
```

Dunkerley's formula is a lower bound, so the true critical speed lies slightly above 2115 rpm.

</details>

**Exercise 3.** Three masses rotate in one plane with mass-radius products of 0.20 kg·m at 0°, 0.24 kg·m at 90° and 0.18 kg·m at 210°. Find the balancing mass-radius product and its angle, and the balancing mass if it sits at a radius of 100 mm.

<details>
<summary>Answer</summary>

```math
\sum m_ir_i\cos\theta_i = 0.20 + 0 + 0.18\cos 210^\circ = 0.0441 \text{ kg m}, \qquad \sum m_ir_i\sin\theta_i = 0.24 + 0.18\sin 210^\circ = 0.150 \text{ kg m}
```

$m_br_b = \sqrt{0.0441^2 + 0.150^2} = 0.156$ kg·m. The resultant points at 73.6°, so the balancing mass goes opposite it, at 253.6°. At $r_b = 0.1$ m, $m_b = 1.56$ kg.

</details>

**Exercise 4.** A centrifugal pump impeller has an outlet diameter of 250 mm, an outlet width of 20 mm and backward-curved blades with outlet angle $\beta_2 = 25^\circ$ from the tangent. It turns at 1450 rpm and delivers 30 L/s of water with no inlet whirl. Find the blade speed, the outlet velocity components, the Euler head and the ideal hydraulic power.

<details>
<summary>Answer</summary>

- $u_2 = \pi D_2n/60 = \pi \times 0.25 \times 1450/60 = 18.98$ m/s
- $c_{r2} = Q/(\pi D_2b_2) = 0.030/(\pi \times 0.25 \times 0.020) = 1.91$ m/s
- $c_{u2} = u_2 - c_{r2}\cot\beta_2 = 18.98 - 1.91/\tan 25^\circ = 14.88$ m/s

```math
H_E = \frac{u_2c_{u2}}{g} = \frac{18.98 \times 14.88}{9.81} = 28.8 \text{ m}, \qquad \rho gQH_E = 998 \times 9.81 \times 0.030 \times 28.8 = 8.46 \text{ kW}
```

With a slip factor of about 0.85 and a hydraulic efficiency of about 0.85 the real head would be near 21 m.

</details>

**Exercise 5.** The pump of the figure delivers 25 L/s at 30 m with 9.42 kW of shaft power and needs 3.0 m NPSH at 1450 rpm. (a) Use the affinity laws to find the similar point at 1750 rpm. (b) In the system of the figure the static head is 15 m. Why does the pump not run at that similar point after the speed change? (c) Does the 20 °C installation, with 6.1 m NPSH available at 25 L/s, still have a margin at the higher speed?

<details>
<summary>Answer</summary>

(a) $r = 1750/1450 = 1.207$: $Q = 30.2$ L/s, $H = 30 \times 1.457 = 43.7$ m, $P = 9.42 \times 1.758 = 16.6$ kW at the same 78% efficiency.

(b) Similar points lie on the parabola $H \propto Q^2$ through the origin. The system curve $`H = 15 + 23\,962Q^2`$ does not pass through the origin, so the new operating point is where the 1750 rpm pump curve $`H = 58.3 - 16\,000Q^2`$ meets it: $`Q = \sqrt{43.3/39\,962} = 32.9`$ L/s at $H = 41.0$ m, at a flow above the BEP of the faster pump.

(c) $\mathrm{NPSH}_r$ scales with $n^2$ at similar points, so it becomes $3.0 \times 1.457 = 4.4$ m at 30.2 L/s and, with the curve of the figure scaled to 1750 rpm, 4.8 m at 32.9 L/s. $\mathrm{NPSH}_a$ falls with flow to 5.4 m at 32.9 L/s, so the margin shrinks from 3.1 m to 0.6 m, too small for continuous duty.

</details>

## References

- Childs, D., *Turbomachinery Rotordynamics: Phenomena, Modeling, and Analysis*, Wiley, 1993.
- Friswell, M. I., Penny, J. E. T., Garvey, S. D., and Lees, A. W., *Dynamics of Rotating Machines*, Cambridge University Press, 2010.
- Vance, J. M., *Rotordynamics of Turbomachinery*, Wiley, 1988.
- Den Hartog, J. P., *Mechanical Vibrations*, 4th ed., McGraw-Hill, 1956.
- Rao, S. S., *Mechanical Vibrations*, 6th ed., Pearson, 2017.
- Dixon, S. L., and Hall, C. A., *Fluid Mechanics and Thermodynamics of Turbomachinery*, 7th ed., Butterworth-Heinemann, 2014.
- Gülich, J. F., *Centrifugal Pumps*, 3rd ed., Springer, 2014.
- ISO 21940-11:2016, *Mechanical vibration — Rotor balancing — Part 11: Procedures and tolerances for rotors with rigid behaviour*, International Organization for Standardization, 2016.
