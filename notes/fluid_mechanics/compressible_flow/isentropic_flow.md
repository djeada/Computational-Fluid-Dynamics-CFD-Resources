# Isentropic Flow

## Overview

Isentropic flow is the reference model for gas moving through nozzles, diffusers, wind-tunnel contractions and engine inlets. The flow is assumed to be

- **steady** and **quasi-one-dimensional**: properties are uniform over each cross-section and vary only with the axial position $x$ through the area $A(x)$;
- **adiabatic** and **inviscid**, with no shaft work, so it is **isentropic** everywhere outside shock waves;
- a **calorically perfect gas** with constant $\gamma$ and $R$ (see [thermodynamics.md](thermodynamics.md)).

These assumptions ignore the wall boundary layers, but they predict pressure distributions, mass flow rates and exit velocities of well-designed nozzles within a few percent. This page derives the stagnation-to-static ratios, the area–velocity and area–Mach relations, the choked mass flow, and then uses them to explain how converging and converging–diverging nozzles behave as the back pressure changes. All numbers are for air with $\gamma = 1.4$ and $R = 287\ \text{J/(kg K)}$.

## Stagnation-to-Static Ratios

In adiabatic flow with no work, the stagnation enthalpy $h_0 = h + V^2/2$ is constant. For a calorically perfect gas this gives $c_p T_0 = c_p T + V^2/2$. Dividing by $c_p T$ and using $a^2 = \gamma R T$ (derived in [speed_of_sound.md](speed_of_sound.md)) and $c_p = \gamma R/(\gamma - 1)$:

$$
\frac{T_0}{T} = 1 + \frac{\gamma - 1}{2} M^2
$$

Because the flow is isentropic, the pressure and density follow from $p \propto T^{\gamma/(\gamma-1)}$ and $\rho \propto T^{1/(\gamma-1)}$:

$$
\frac{p_0}{p} = \left(1 + \frac{\gamma - 1}{2} M^2\right)^{\gamma/(\gamma - 1)},
\qquad \frac{\rho_0}{\rho} = \left(1 + \frac{\gamma - 1}{2} M^2\right)^{1/(\gamma - 1)}
$$

In isentropic flow $T_0$, $p_0$ and $\rho_0$ stay the same along the whole duct. So the Mach number fixes every static property, and the geometry decides only where each Mach number appears.

The **sonic** (starred) state at $M = 1$ is a second fixed reference:

$$
\frac{T^*}{T_0} = \frac{2}{\gamma + 1} = 0.8333,
\qquad
\frac{p^*}{p_0} = \left(\frac{2}{\gamma + 1}\right)^{\gamma/(\gamma - 1)} = 0.5283,
\qquad
\frac{\rho^*}{\rho_0} = \left(\frac{2}{\gamma + 1}\right)^{1/(\gamma - 1)} = 0.6339
$$

Selected values (the last column is derived below):

| $M$ | $T_0/T$ | $p_0/p$ | $\rho_0/\rho$ | $A/A^*$ |
| --- | --- | --- | --- | --- |
| 0.5 | 1.0500 | 1.1862 | 1.1297 | 1.3398 |
| 0.8 | 1.1280 | 1.5243 | 1.3514 | 1.0382 |
| 1.0 | 1.2000 | 1.8929 | 1.5774 | 1.0000 |
| 1.5 | 1.4500 | 3.6710 | 2.5317 | 1.1762 |
| 2.0 | 1.8000 | 7.8244 | 4.3469 | 1.6875 |
| 3.0 | 2.8000 | 36.733 | 13.119 | 4.2346 |

These agree with NACA Report 1135.

## The Area–Velocity Relation

Take logarithmic derivatives of the three governing equations for steady quasi-one-dimensional flow:

- continuity, $\rho V A = \text{const}$: $\dfrac{d\rho}{\rho} + \dfrac{dV}{V} + \dfrac{dA}{A} = 0$
- Euler's equation: $dp = -\rho V\, dV$
- isentropic process: $dp = a^2\, d\rho$

The last two combine to give $d\rho/\rho = -M^2\, dV/V$, the same relation used in [speed_of_sound.md](speed_of_sound.md) for the compressibility criterion. Putting this into continuity:

$$
\frac{dA}{A} = \left(M^2 - 1\right) \frac{dV}{V}
$$

This short equation explains the de Laval nozzle:

|  | Subsonic, $M < 1$ | Supersonic, $M > 1$ |
| --- | --- | --- |
| Converging duct, $dA < 0$ | $V$ increases, $p$ decreases (nozzle) | $V$ decreases, $p$ increases (diffuser) |
| Diverging duct, $dA > 0$ | $V$ decreases, $p$ increases (diffuser) | $V$ increases, $p$ decreases (nozzle) |

Physically, in subsonic flow density barely changes, so continuity forces the velocity up when the area shrinks. In supersonic flow the density falls faster than the velocity rises ($|d\rho/\rho| = M^2 |dV/V| > |dV/V|$). The product $\rho V$ therefore drops, and the area has to grow to carry the same mass flow. For example, a 1% area increase at $M = 0.5$ slows the flow by 1.33%, while at $M = 2$ it speeds the flow up by 0.33%.

At $M = 1$ the equation needs $dA = 0$. **Sonic flow can occur only at an area minimum, the throat.** The reverse does not hold: a throat with $M \neq 1$ simply has $dV = 0$ (a velocity maximum in a subsonic venturi).

## Mass Flow and the Area–Mach Relation

Write the mass flow in terms of stagnation conditions. With $\rho = p/(RT)$ and $V = M\sqrt{\gamma R T}$:

$$
\dot m = \rho V A = \frac{p}{RT} M \sqrt{\gamma R T} A = \frac{p_0 A}{\sqrt{T_0}}
\sqrt{\frac{\gamma}{R}}\, M
\left(1 + \frac{\gamma - 1}{2} M^2\right)^{-\frac{\gamma + 1}{2(\gamma - 1)}}
$$

For fixed $p_0$ and $T_0$, the mass flow per unit area $\dot m/A$ is largest at $M = 1$. Since $\dot m$ is the same at every section, compare a general section with a (possibly imaginary) section where the flow would be sonic, of area $A^*$. This gives the **area–Mach relation**:

$$
\frac{A}{A^*} = \frac{1}{M}\left[\frac{2}{\gamma + 1}\left(1 + \frac{\gamma - 1}{2}
M^2\right)\right]^{\frac{\gamma + 1}{2(\gamma - 1)}}
$$

Key properties:

- $A/A^* \ge 1$, with the minimum at $M = 1$.
- Every $A/A^* > 1$ has **two** solutions, one subsonic and one supersonic. For $A/A^* = 2$ they are $M = 0.3059$ and $M = 2.1972$. Which one occurs depends on the downstream (back) pressure.
- $A^*$ is a flow reference, not necessarily a physical area. It stays constant only while $p_0$ is constant. Across a shock $p_0$ falls, so $A^*$ grows: $p_{01} A_1^* = p_{02} A_2^*$.

The area–Mach relation cannot be inverted in closed form. In practice $M$ is found with a bracketed root finder on $(0, 1)$ or $(1, M_{max})$, or read from tables.

## Choking

At $M = 1$ in the throat the mass flow reaches its maximum:

$$
\dot m_{max} = \frac{p_0 A^*}{\sqrt{T_0}} \sqrt{\frac{\gamma}{R}}
\left(\frac{2}{\gamma + 1}\right)^{\frac{\gamma + 1}{2(\gamma - 1)}} = 0.04042\,
\frac{p_0 A^*}{\sqrt{T_0}} \quad \text{(air, SI units)}
$$

Once the throat is sonic, the nozzle is **choked**. Lowering the back pressure further cannot increase the mass flow. Pressure signals travel upstream at speed $a - V$ relative to the duct, and at a sonic throat that speed is zero, so the flow upstream of the throat never finds out that the back pressure has changed. A choked nozzle's flow rate depends only on $p_0$, $T_0$ and $A^*$. This makes a choked orifice or sonic venturi a simple and accurate flow meter and flow limiter.

## The Converging Nozzle

A converging nozzle fed from a reservoir at $p_0$, $T_0$ discharges into a back pressure $p_b$. Its minimum area is the exit, so the exit Mach number can never exceed 1.

- **$p_b/p_0 > 0.5283$**: the exit is subsonic and the jet exits at $p_e = p_b$. Get $M_e$ from $p_0/p_e$ and then $\dot m$ from the mass-flow formula.
- **$p_b/p_0 = 0.5283$**: the exit just reaches $M_e = 1$.
- **$p_b/p_0 < 0.5283$**: the nozzle is choked. The exit stays at $M_e = 1$ and $p_e = p^* > p_b$. The remaining pressure drop happens outside the nozzle through expansion waves in the jet, which is then **under-expanded**.

```
  mdot / mdot_max
   1.0 +===============.
       |                 '.
       |                    '.
       |                      '.
       |                        '.
       |                          '.
   0.0 +-----------------+----------'--> pb / p0
       0               0.528         1
       <-- choked -->   <-- unchoked -->
       pe = p*          pe = pb
```

The curve is very flat near the choke point. At $p_b/p_0 = 0.6$ the flow is already 98.9% of the maximum.

## The Converging–Diverging Nozzle

A converging–diverging (de Laval) nozzle with exit-to-throat ratio $A_e/A_t$ has **three critical back pressures**. Once the throat is sonic, $A^* = A_t$ and the exit Mach number must be one of the two roots of $A_e/A^* = A_e/A_t$:

1. $p_{b1}$: the subsonic root. The throat is just sonic and the flow is subsonic everywhere else (a choked venturi).
2. $p_{b2}$: the supersonic root followed by a normal shock standing exactly in the exit plane.
3. $p_{b3}$: the supersonic root with no shock. This is the **design** pressure, where the jet is perfectly expanded.

The regimes, from high to low back pressure:

| Back pressure | Flow in the nozzle | Exit and jet |
| --- | --- | --- |
| $p_{b1} < p_b < p_0$ | subsonic everywhere, not choked | $p_e = p_b$ |
| $p_b = p_{b1}$ | sonic throat, subsonic elsewhere | $p_e = p_b$, choked |
| $p_{b2} < p_b < p_{b1}$ | supersonic after throat, **normal shock in diverging part**, subsonic after it | $p_e = p_b$ |
| $p_b = p_{b2}$ | normal shock in the exit plane | $p_e = p_b$ |
| $p_{b3} < p_b < p_{b2}$ | fully supersonic, isentropic | **over-expanded**: $p_e < p_b$, oblique shocks at the exit lip |
| $p_b = p_{b3}$ | fully supersonic, isentropic | **perfectly expanded**: $p_e = p_b$ |
| $p_b < p_{b3}$ | fully supersonic, isentropic | **under-expanded**: $p_e > p_b$, expansion fans at the exit lip |

The mass flow stays constant for every $p_b \le p_{b1}$. Below $p_{b2}$ the flow inside the nozzle no longer changes at all, and only the external jet structure adjusts. Over- and under-expanded jets both form repeating shock-cell ("diamond") patterns as the waves reflect from the jet boundary. In real over-expanded nozzles the adverse pressure gradient can also separate the boundary layer from the wall before the ideal shock position is reached, which the inviscid theory does not predict. The shock and expansion relations used at the exit are in [shock_waves.md](shock_waves.md).

The static-pressure distribution along a nozzle with $A_e/A_t = 2$:

```
  p/p0
  1.00 +==.
       |     '-.                                   ___..--- (A) pb1/p0 = 0.937
       |        '-.                     ___..---'''          subsonic, sonic throat
       |           '-.         __..--'''
       |              '-. _.-''
  0.53 + - - - - - - - - -*                         .------ (B) shock inside
       |                   '-.                     |         nozzle, then
       |                      '-.                  |         subsonic recovery
       |                         '-.  . . . . . . .'
       |                            '-.                 |-- (C) pb2/p0 = 0.513
       |                               '-.              |    shock at exit
       |                                  '-.           |
       |                                     '-.        |
  0.09 +                                        '-.___._|__ (D) pb3/p0 = 0.094
       |                                                     design exit
       +------------------------+-----------------------+---> x
     inlet                   throat                    exit
```

Upstream of the throat all choked cases share the same curve. Downstream of the throat, cases (B), (C) and (D) follow the same supersonic branch until they reach their shock (if any). That branch depends only on the geometry, and the back pressure decides where it ends.

### Worked Example: A Converging–Diverging Nozzle

A nozzle has throat area $A_t = 10\ \text{cm}^2$ and exit area $A_e = 20\ \text{cm}^2$, and is fed with air at $p_0 = 1\ \text{MPa}$ and $T_0 = 500\ \text{K}$.

**Mass flow when choked.**

$$
\dot m = 0.04042 \times
\frac{(1.0 \times 10^6)(1.0 \times 10^{-3})}{\sqrt{500}} = 1.808\  \text{kg/s}
$$

At the throat, $T^* = 0.8333 \times 500 = 416.7\ \text{K}$, $p^* = 528.3\ \text{kPa}$, $V^* = a^* = \sqrt{1.4 \times 287 \times 416.7} = 409.2\ \text{m/s}$, and $\rho^* = 4.418\ \text{kg/m}^3$. As a check, $\rho^* V^* A_t = 1.808\ \text{kg/s}$.

**Critical back pressures.** For $A_e/A^* = 2$:

- subsonic root $M_e = 0.3059$, so $p_{b1} = p_0/1.0670 = 937.2\ \text{kPa}$;
- supersonic root $M_e = 2.1972$, so $p_{b3} = p_0/10.646 = 93.93\ \text{kPa}$;
- a normal shock at $M_1 = 2.1972$ has $p_2/p_1 = 5.466$, so $p_{b2} = 5.466 \times 93.93 = 513.4\ \text{kPa}$.

**Design exit state.** $T_e = 500/1.9655 = 254.4\ \text{K}$, and $V_e = 2.1972 \sqrt{1.4 \times 287 \times 254.4} = 702.5\ \text{m/s}$. The kinetic energy $V_e^2/2 = 246.7\ \text{kJ/kg}$ equals $c_p(T_0 - T_e)$, as the energy equation requires.

**Discharge to sea level.** At $p_b = 101.325\ \text{kPa}$ we have $p_{b3} < p_b < p_{b2}$, so the nozzle runs slightly **over-expanded** with $p_b/p_e = 1.079$. The internal flow is unchanged. A weak oblique shock at the exit lip ($M_{n1} = 1.033$, wave angle $\beta = 28.0^\circ$) turns the jet boundary inward by about $1.3^\circ$ and raises the pressure to $p_b$.

**Shock position at $p_b = 800\ \text{kPa}$.** Now $p_{b2} < p_b < p_{b1}$, so a normal shock stands inside the diverging section and the exit is subsonic with $p_e = p_b$. Since $p_{01} A_t = p_{02} A_2^*$ and $A_e/A_t = 2$,

$$
\frac{p_e}{p_{02}} \frac{A_e}{A_2^*} = \frac{p_b}{p_{01}} \frac{A_e}{A_t} = 0.8 \times
2 = 1.6
$$

The left side depends only on $M_e$. Solving on the subsonic branch gives $M_e = 0.3572$, so $p_{02} = p_e (p_0/p)_{M_e} = 873.7\ \text{kPa}$ and $p_{02}/p_{01} = 0.8737$. From the normal-shock relations, this total-pressure ratio corresponds to $M_1 = 1.656$. The isentropic relation then puts the shock at $A/A_t = (A/A^*)_{M_1} = 1.297$, and just behind it $M_2 = 0.652$.

## Summary

- Stagnation-to-static ratios depend only on $M$. In isentropic flow the stagnation values are the same throughout the duct.
- $dA/A = (M^2 - 1)\, dV/V$: subsonic flow accelerates in converging ducts and supersonic flow in diverging ducts, and $M = 1$ can occur only at a throat.
- $A/A^*$ has a subsonic and a supersonic root. The back pressure selects the root and decides whether and where shocks appear.
- A sonic throat chokes the flow at $\dot m = 0.04042\, p_0 A^*/\sqrt{T_0}$ for air.
- Over-expanded nozzles end in oblique shocks and under-expanded nozzles in expansion fans. Only at the design back pressure does the jet leave parallel and at ambient pressure.

## Related Scripts

- [nozzle_flow](../../../scripts/plots/nozzle_flow/): plots a converging–diverging nozzle at its design condition with streamlines coloured by Mach number. The Mach number comes from inverting the area–Mach relation above on the subsonic branch upstream of the throat and the supersonic branch downstream, so the flow is sonic at the throat and keeps accelerating in the diverging section. Off-design operation with shocks is not modelled.

## Exercises

**Exercise 1.** An aircraft flies at $M = 0.8$ at 11 km altitude, where $T = 216.65\ \text{K}$ and $p = 22.632\ \text{kPa}$. Find the stagnation temperature and pressure at the nose.

<details>
<summary>Answer</summary>

$T_0/T = 1 + 0.2(0.8)^2 = 1.128$, so $T_0 = 244.4\ \text{K}$.

$p_0/p = 1.128^{3.5} = 1.5243$, so $p_0 = 34.50\ \text{kPa}$.

</details>

**Exercise 2.** Find both Mach numbers at which $A/A^* = 3$.

<details>
<summary>Answer</summary>

Solving the area–Mach relation on each branch gives $M = 0.1974$ (subsonic) and $M = 2.637$ (supersonic). Substituting either value back into the formula returns $A/A^* = 3.000$.

</details>

**Exercise 3.** Air in a large tank at $p_0 = 500\ \text{kPa}$ and $T_0 = 300\ \text{K}$ discharges through a converging–diverging nozzle with a throat diameter of 2 cm. What is the maximum mass flow rate, and what condition must the back pressure satisfy to reach it?

<details>
<summary>Answer</summary>

$A^* = \pi (0.01)^2 = 3.1416 \times 10^{-4}\ \text{m}^2$.

$\dot m_{max} = 0.04042 \times 500\,000 \times 3.1416 \times 10^{-4}/\sqrt{300} = 0.3666\ \text{kg/s}$.

The throat must be sonic, which needs the back pressure to be at or below the first critical pressure $p_{b1}$ of the nozzle. $p_{b1}$ depends on the exit-to-throat area ratio and is always higher than $p^* = 264.1\ \text{kPa}$.

</details>

**Exercise 4.** The same tank ($p_0 = 500\ \text{kPa}$, $T_0 = 300\ \text{K}$) discharges through a *converging* nozzle with a 2 cm exit diameter. Find the exit Mach number and mass flow for (a) $p_b = 300\ \text{kPa}$ and (b) $p_b = 200\ \text{kPa}$.

<details>
<summary>Answer</summary>

(a) $p_b/p_0 = 0.6 > 0.5283$, so the nozzle is not choked and $p_e = p_b$. From $p_0/p_e = 1.6667$: $M_e = \sqrt{5[(1.6667)^{0.2857} - 1]} = 0.886$. Then $T_e = 300/(1 + 0.2 \times 0.886^2) = 259.3\ \text{K}$, $V_e = 286.1\ \text{m/s}$, $\rho_e = 300\,000/(287 \times 259.3) = 4.032\ \text{kg/m}^3$, and $\dot m = \rho_e V_e A_e = 0.3624\ \text{kg/s}$.

(b) $p_b/p_0 = 0.4 < 0.5283$, so the nozzle is choked: $M_e = 1$, $p_e = 264.1\ \text{kPa} > p_b$, and $\dot m = 0.3666\ \text{kg/s}$. This is only 1.2% more than in case (a), even though the back pressure is 100 kPa lower.

</details>

**Exercise 5.** A rocket nozzle has $A_e/A_t = 4$. (a) Find the design exit Mach number and $p_e/p_0$. (b) What chamber pressure makes it perfectly expanded at sea level ($101.325\ \text{kPa}$)? (c) Over what range of $p_b/p_0$ does a normal shock stand inside the diverging section?

<details>
<summary>Answer</summary>

(a) The supersonic root of $A/A^* = 4$ is $M_e = 2.940$, with $p_e/p_0 = 1/(1 + 0.2 \times 2.940^2)^{3.5} = 0.02979$.

(b) $p_0 = 101.325/0.02979 = 3402\ \text{kPa} \approx 3.40\ \text{MPa}$.

(c) The subsonic root is $M = 0.1465$, so $p_{b1}/p_0 = 0.9851$. A normal shock at $M_1 = 2.940$ has $p_2/p_1 = 9.918$, so $p_{b2}/p_0 = 9.918 \times 0.02979 = 0.2954$. A shock stands inside the nozzle for $0.2954 < p_b/p_0 < 0.9851$.

</details>

## References

- Anderson, J. D., *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003. Chapter 5 covers quasi-one-dimensional flow and nozzles.
- Ames Research Staff, *Equations, Tables, and Charts for Compressible Flow*, NACA Report 1135, 1953.
- Zucker, R. D., and Biblarz, O., *Fundamentals of Gas Dynamics*, 2nd ed., Wiley, 2002.
- Shapiro, A. H., *The Dynamics and Thermodynamics of Compressible Fluid Flow*, Vol. 1, Ronald Press, 1953.
