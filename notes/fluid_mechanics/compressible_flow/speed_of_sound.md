# Speed of Sound and Mach Number

## Overview

The speed of sound is the speed at which small pressure disturbances travel through a fluid. It sets the "information speed" of a compressible flow. Comparing the flow speed with the speed of sound, through the **Mach number**, tells us:

- whether the fluid ahead of a body can adjust before the body arrives;
- whether shock waves can form;
- whether density changes are large enough to matter.

This page derives $a = \sqrt{(\partial p/\partial \rho)_s} = \sqrt{\gamma R T}$ from a weak pressure wave, connects it to molecular motion, defines the flow regimes, introduces the Mach cone, and justifies the familiar $M \approx 0.3$ compressibility criterion. Thermodynamic background is in [thermodynamics.md](thermodynamics.md). Numbers are for air with $\gamma = 1.4$ and $R = 287\ \text{J/(kg K)}$.

## Sound as a Weak Pressure Wave

### Setting Up the Problem

Consider a plane pressure wave of very small strength moving to the left at speed $a$ into still gas with pressure $p$, density $\rho$ and temperature $T$. Behind the wave the gas has been set moving with a small velocity $dV$ and has slightly different properties $p + dp$, $\rho + d\rho$, $T + dT$.

The wave is unsteady in the lab frame. In a frame moving with the wave it is steady: gas enters from the left at speed $a$ and leaves at speed $a - dV$.

```
                  frame moving with the wave

     undisturbed gas               |        gas behind the wave
     p, rho, T                     |        p + dp, rho + drho, T + dT
                                   |
     -------->   a                 |        -------->   a - dV
     -------->                     |        -------->
                                   |
                            wave front (at rest in this frame)
```

### Conservation Laws Across the Wave

Apply steady conservation laws to a thin control volume enclosing the wave, per unit area.

**Continuity:**

$$
\rho a = (\rho + d\rho)(a - dV)
$$

Expanding and dropping the product of small quantities gives

$$
dV = \frac{a\, d\rho}{\rho}
$$

**Momentum** (no viscous forces act across the thin control volume):

$$
p + \rho a^2 = (p + dp) + (\rho + d\rho)(a - dV)^2
$$

Continuity says $(\rho + d\rho)(a - dV) = \rho a$, so the last term is $\rho a (a - dV)$, and

$$
dp = \rho a\, dV
$$

**Combining** the two results:

$$
dp = \rho a \cdot \frac{a\, d\rho}{\rho} = a^2\, d\rho \quad \Rightarrow \quad
a^2 = \frac{dp}{d\rho}
$$

### Which Derivative?

The ratio $dp/d\rho$ depends on the process. Inside a weak sound wave the gradients of velocity and temperature are tiny, so viscous dissipation and heat conduction are negligible. The process is adiabatic and reversible, which means **isentropic**:

$$
a^2 = \left(\frac{\partial p}{\partial \rho}\right)_s
$$

Newton, in the seventeenth century, assumed an isothermal process, $(\partial p/\partial \rho)_T = RT$. At 293.15 K this gives 290.1 m/s, about 15% below the measured value. Laplace corrected the estimate in the early nineteenth century by treating the compressions as adiabatic.

For a calorically perfect gas the isentrope is $p = C \rho^\gamma$, so $(\partial p/\partial \rho)_s = \gamma p/\rho$, and with $p = \rho R T$:

$$
a = \sqrt{\frac{\gamma p}{\rho}} = \sqrt{\gamma R T}
$$

Three consequences:

- In a given perfect gas, $a$ depends **only on temperature**, not on pressure or density separately.
- $a$ grows as $\sqrt{T}$ and falls as the molecular weight rises, since $R = R_u/\mathcal{M}$.
- For liquids and general fluids, write $a = \sqrt{K_s/\rho}$ with the isentropic bulk modulus $K_s = \rho (\partial p/\partial \rho)_s$ (see [pressure_and_compressibility.md](../fluid_properties/pressure_and_compressibility.md)).

The momentum result $dp = \rho a\, dV$ is also useful on its own. It relates the pressure amplitude of a wave to the fluid velocity it induces. In sea-level air ($\rho = 1.225\ \text{kg/m}^3$, $a = 340.3\ \text{m/s}$), inducing just 1 m/s of fluid velocity takes a pressure jump of 417 Pa.

### Typical Values

| Medium | Condition | Speed of sound |
| --- | --- | --- |
| Air | 288.15 K (sea level, standard atmosphere) | 340.3 m/s |
| Air | 300 K | 347.2 m/s |
| Air | 216.65 K (11 km, standard atmosphere) | 295.0 m/s |
| Helium | 293.15 K | 1007 m/s |
| Water | about 20 $^\circ$C ($K_s \approx 2.2\ \text{GPa}$) | about 1480 m/s |

### The Kinetic Theory View

Pressure disturbances are carried by molecular collisions, so they cannot travel faster than the molecules themselves. The root-mean-square molecular speed is

$$
v_{rms} = \sqrt{\frac{3 k_B T}{m}} = \sqrt{3 R T}
$$

so

$$
a = \sqrt{\frac{\gamma}{3}}\, v_{rms}
$$

For air, $a \approx 0.683\, v_{rms}$. For nitrogen at 300 K ($m = 4.65 \times 10^{-26}\ \text{kg}$), $v_{rms} = 517\ \text{m/s}$ and $a = 353\ \text{m/s}$. Sound is a coordinated drift superimposed on this random motion, and it propagates at a fixed fraction of the typical molecular speed.

## Mach Number

The **Mach number** is the local ratio of flow speed to sound speed:

$$
M = \frac{V}{a}
$$

It is a local property: $a$ changes with temperature, so the same velocity gives different Mach numbers in hot and cold parts of a flow. It has several physical interpretations:

- **Signal speed.** $M$ compares how fast the fluid moves with how fast pressure information travels through it.
- **Energy.** $\dfrac{V^2/2}{c_v T} = \dfrac{\gamma(\gamma - 1)}{2} M^2$, the ratio of directed kinetic energy to random molecular energy.
- **Forces.** With $K_s = \rho a^2$, $M^2 = \rho V^2/K_s$, the ratio of inertial pressure to the fluid's resistance to compression.

### Flow Regimes

| Regime | Mach range (approximate) | Characteristics |
| --- | --- | --- |
| Incompressible | $M < 0.3$ | density changes below about 5%, Bernoulli applies |
| Subsonic | $0.3 < M < 0.8$ | smooth flow, noticeable compressibility corrections |
| Transonic | $0.8 < M < 1.2$ | mixed subsonic and supersonic regions, local shocks on wings |
| Supersonic | $1.2 < M < 5$ | shocks and expansion fans, no upstream influence |
| Hypersonic | $M > 5$ | thin, hot shock layers, high-temperature gas effects |

The boundaries are not sharp. The transonic range, for example, begins when the flow over some part of a body first becomes locally sonic, and that depends on the body's shape.

## Propagation of Disturbances and the Mach Cone

Picture a small source emitting a sound pulse every second while it moves at speed $V$ through still air. Each pulse spreads as a sphere of radius $a t$ around the point where it was emitted, while the source travels a distance $V t$.

- **$M = 0$**: the wavefronts are concentric circles.
- **$M < 1$**: the wavefronts crowd together ahead of the source (the Doppler effect) but always stay ahead of it. The air ahead "hears" the source coming and can adjust.
- **$M = 1$**: all wavefronts touch at the source and form a plane front. No signal gets ahead.
- **$M > 1$**: the source outruns its own wavefronts. They are enclosed by a cone with the source at its apex, the **Mach cone**.

In the frame of the source, a supersonic stream flows past it:

```
                                             /
     M > 1                                 /    Mach wave
   ---------->                           /
   ---------->     zone of silence     /
   ---------->     (no signal from   /      zone of action
   ---------->      the source)    /        (inside the cone)
   ----------> - - - - - - - - - S ) mu - - - - - - - - - - -
   ---------->                     \
   ---------->                       \
                                       \
                                         \   Mach wave
```

The half-angle $\mu$ of the cone follows from the right triangle formed by the source path $V t$ and the pulse radius $a t$. The cone surface is tangent to the pulse sphere, so

$$
\sin \mu = \frac{a t}{V t} = \frac{1}{M},
\qquad \mu = \arcsin \frac{1}{M}
$$

| $M$ | 1.2 | 1.5 | 2 | 3 | 5 |
| --- | --- | --- | --- | --- | --- |
| $\mu$ | $56.4^\circ$ | $41.8^\circ$ | $30.0^\circ$ | $19.5^\circ$ | $11.5^\circ$ |

The surface of the cone is a **Mach wave**: the limit of an infinitely weak shock, across which properties change only infinitesimally. Mach waves are the characteristic lines of steady supersonic flow. They are the building blocks of the Prandtl–Meyer expansion fan and the method of characteristics ([shock_waves.md](shock_waves.md)). Only points inside the downstream cone can be influenced by the source, which is why supersonic flow has no upstream influence without a shock.

### Worked Example 1: Hearing a Sonic Boom

An aircraft flies level at $M = 1.5$ at an altitude of $h = 3000\ \text{m}$. Take a uniform speed of sound of 340 m/s. When does an observer on the ground hear the boom?

The observer hears the aircraft when the Mach cone reaches them. By then the aircraft has passed overhead and travelled a horizontal distance $x$ with $\tan \mu = h/x$:

$$
\mu = \arcsin \frac{1}{1.5} = 41.8^\circ,
\qquad x = \frac{h}{\tan \mu} = h \sqrt{M^2 - 1} = 3000 \times 1.118 = 3354\  \text{m}
$$

The aircraft speed is $V = 1.5 \times 340 = 510\ \text{m/s}$, so the boom arrives $t = 3354/510 = 6.58\ \text{s}$ after the aircraft was directly overhead. A real atmosphere is colder at altitude, which bends the cone and shifts this estimate.

## When Does Compressibility Matter?

### The Density–Velocity Relation

Euler's equation along a streamline gives $dp = -\rho V\, dV$. For an isentropic flow $dp = a^2\, d\rho$. Eliminating $dp$:

$$
\frac{d\rho}{\rho} = -M^2 \frac{dV}{V}
$$

**The relative density change is $M^2$ times the relative velocity change.** At $M = 0.3$, a 10% change in velocity produces only a 0.9% change in density. At $M = 2$, the density change is four times the velocity change.

### Density Change When the Flow Is Brought to Rest

For the largest density change in a flow, compare the free stream with the stagnation point. From [thermodynamics.md](thermodynamics.md):

$$
\frac{\rho_0}{\rho} = \left(1 + \frac{\gamma - 1}{2} M^2\right)^{1/(\gamma - 1)} = 1 +
\frac{M^2}{2} + \frac{2 - \gamma}{8} M^4 + \cdots
$$

So the fractional density change is $\Delta\rho/\rho \approx M^2/2$.

The pressure rise at the stagnation point, compared with the incompressible prediction $\tfrac{1}{2}\rho V^2$, is

$$
\frac{p_0 - p}{\tfrac{1}{2}\rho V^2} = 1 + \frac{M^2}{4} + \frac{2 - \gamma}{24} M^4 +
\cdots
$$

| $M$ | $\rho_0/\rho - 1$ (exact) | $M^2/2$ | $(p_0 - p)/(\tfrac{1}{2}\rho V^2)$ |
| --- | --- | --- | --- |
| 0.1 | 0.50% | 0.50% | 1.0025 |
| 0.2 | 2.01% | 2.00% | 1.0100 |
| 0.3 | 4.56% | 4.50% | 1.0227 |
| 0.5 | 12.97% | 12.50% | 1.0641 |

At $M = 0.3$ the density varies by less than 5%, and Bernoulli's equation underestimates the stagnation pressure rise by 2.3%. This is the origin of the rule of thumb that **flows below $M \approx 0.3$ may be treated as incompressible**. It agrees with the estimate $\Delta p/p \approx \tfrac{\gamma}{2}M^2$ in [pressure_and_compressibility.md](../fluid_properties/pressure_and_compressibility.md). The [bernoulli.md](../inviscid_flow/bernoulli.md) note gives the compressible form of Bernoulli's equation for larger Mach numbers.

### Limits of the Criterion

The $M < 0.3$ rule addresses density changes caused by **velocity**. Density can also change significantly at low Mach number because of:

- **large temperature differences**, as in combustion, heat exchangers and natural convection. These need variable-density or low-Mach-number models (the Boussinesq approximation only when the differences are small);
- **large height changes**, as in atmospheric flows where hydrostatic pressure varies;
- **unsteady acoustic effects**, such as water hammer or combustion instabilities, where waves travelling at speed $a$ matter even though the mean flow is slow.

### Worked Example 2: Speed Limits for Incompressible Analysis

Air with stagnation temperature 293.15 K flows over a model. What is the highest speed for which the density varies by less than (a) 1% and (b) 5%?

Solve $\rho_0/\rho = (1 + 0.2 M^2)^{2.5}$ for $M$:

$$
M = \sqrt{5\left[\left(\frac{\rho_0}{\rho}\right)^{0.4} - 1\right]}
$$

(a) $\rho_0/\rho = 1.01$ gives $M = 0.141$. Then $T = 293.15/(1 + 0.2 \times 0.141^2) = 292.0\ \text{K}$, $a = 342.5\ \text{m/s}$ and $V = 48.4\ \text{m/s}$.

(b) $\rho_0/\rho = 1.05$ gives $M = 0.314$ and $V = 106.7\ \text{m/s}$.

Most low-speed wind tunnels operate below about 100 m/s, and the incompressible approximation is adequate there.

## Summary

- A weak pressure wave travels at $a = \sqrt{(\partial p/\partial \rho)_s}$. For a perfect gas this is $\sqrt{\gamma R T}$, independent of pressure.
- The wave pressure and induced velocity are linked by $dp = \rho a\, dV$.
- The Mach number $M = V/a$ compares flow speed with signal speed, kinetic energy with thermal energy, and inertia with compressibility.
- Supersonic disturbances are confined to a Mach cone of half-angle $\mu = \arcsin(1/M)$.
- $d\rho/\rho = -M^2\, dV/V$, and $\Delta\rho/\rho \approx M^2/2$ when a flow is brought to rest. Below $M \approx 0.3$ density changes stay under 5%.

## Related Scripts

- [probability_distribution_function_of_nitrogen_molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell–Boltzmann speed distribution of N$_2$ and marks $v_{rms}$. Multiply $v_{rms}$ by $\sqrt{\gamma/3} = 0.683$ to get the speed of sound at each temperature.
- [compressible_vs_incompressible](../../../scripts/plots/compressible_vs_incompressible/): compares a fully developed incompressible pipe profile with an accelerating compressible one, illustrating why density changes must be tracked once the Mach number is no longer small.
- [Converging-Diverging Nozzle Flow](../../../scripts/plots/nozzle_flow/): plots quasi-one-dimensional isentropic flow through a converging-diverging (de Laval) nozzle, with streamlines coloured by Mach number.

## Exercises

**Exercise 1.** Compute the speed of sound in air at $-50\ ^\circ\text{C}$. What value would Newton's isothermal assumption give?

<details>
<summary>Answer</summary>

$T = 223.15\ \text{K}$, so $a = \sqrt{1.4 \times 287 \times 223.15} = 299.4\ \text{m/s}$.

The isothermal value is $\sqrt{RT} = \sqrt{287 \times 223.15} = 253.1\ \text{m/s}$, which is $1/\sqrt{1.4}$ times the correct value, or 15.5% too low.

</details>

**Exercise 2.** An airliner cruises at a true airspeed of 250 m/s at 11 km, where $T = 216.65\ \text{K}$. Find its Mach number and flow regime. Would the same airspeed at sea level ($T = 288.15\ \text{K}$) give a higher or lower Mach number?

<details>
<summary>Answer</summary>

$a = \sqrt{1.4 \times 287 \times 216.65} = 295.0\ \text{m/s}$, so $M = 250/295.0 = 0.847$.

This is high subsonic, at the lower edge of the transonic range. The flow over the upper surface of the wing can become locally supersonic and end in a weak shock.

At sea level $a = 340.3\ \text{m/s}$, so $M = 0.735$, which is lower. The same airspeed gives a lower Mach number in warmer air.

</details>

**Exercise 3.** A schlieren photograph of a projectile in air at 288.15 K shows weak Mach waves inclined at $40^\circ$ to the flight direction. Estimate the projectile's Mach number and speed.

<details>
<summary>Answer</summary>

$M = 1/\sin 40^\circ = 1/0.6428 = 1.556$.

$V = M a = 1.556 \times 340.3 = 529.4\ \text{m/s}$.

The waves near the nose are shocks, not Mach waves, and are steeper. The estimate should be made from weak waves far from the body.

</details>

**Exercise 4.** An aircraft flies at $M = 2$ at an altitude of 10 km. Using an average speed of sound of 320 m/s along the path, how far past the observer is the aircraft, and how much time has passed since it was overhead, when the boom is heard?

<details>
<summary>Answer</summary>

$\mu = \arcsin(1/2) = 30^\circ$.

$x = h\sqrt{M^2 - 1} = 10\,000 \times \sqrt{3} = 17\,320\ \text{m} = 17.3\ \text{km}$.

$V = 2 \times 320 = 640\ \text{m/s}$, so $t = 17\,320/640 = 27.1\ \text{s}$.

</details>

**Exercise 5.** A pitot-static probe measures $p_0 - p$ in a subsonic air stream, and the velocity is computed with the incompressible formula $V_{inc} = \sqrt{2(p_0 - p)/\rho}$. By what percentage does this overestimate the true velocity at $M = 0.3$ and at $M = 0.5$?

<details>
<summary>Answer</summary>

$V_{inc}^2/V^2 = (p_0 - p)/(\tfrac{1}{2}\rho V^2)$, which equals 1.0227 at $M = 0.3$ and 1.0641 at $M = 0.5$ (from the table above).

Taking square roots: $V_{inc}/V = 1.0113$ at $M = 0.3$, a 1.1% overestimate, and $V_{inc}/V = 1.0315$ at $M = 0.5$, a 3.2% overestimate.

Above $M \approx 0.3$ the compressible (isentropic) relation for $p_0/p$ should be used.

</details>

## References

- Anderson, J. D., *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003. Chapter 3 covers the speed of sound and Mach number.
- Anderson, J. D., *Fundamentals of Aerodynamics*, McGraw-Hill.
- Liepmann, H. W., and Roshko, A., *Elements of Gasdynamics*, Wiley, 1957 (reprinted by Dover).
