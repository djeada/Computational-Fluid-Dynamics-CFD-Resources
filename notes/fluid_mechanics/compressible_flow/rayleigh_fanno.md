# Fanno and Rayleigh Flow

## Overview

[Isentropic flow](isentropic_flow.md) changes a gas stream by changing the duct area. Two other mechanisms can drive a one-dimensional compressible flow just as strongly:

- **Fanno flow**: adiabatic flow in a constant-area duct **with wall friction**. Examples are long gas pipelines, bleed-air ducts and the tubes that feed pressure sensors.
- **Rayleigh flow**: frictionless flow in a constant-area duct **with heat addition or removal**. Examples are combustors, afterburners, ramjets and heat exchangers.

Both models reveal a surprising effect. Friction or heating drives a subsonic flow *faster* and a supersonic flow *slower*, always toward $M = 1$. A duct that is too long, or a stream that is heated too much, becomes **choked** and forces the upstream flow to change.

Each model is derived below, with its property ratios referenced to the sonic (starred) state and its $T$–$`s`$ diagram, followed by worked examples. Numbers are for air with $\gamma = 1.4$ and $R = 287\ \text{J/(kg K)}$.

## Fanno Flow: Adiabatic Flow with Friction

### Governing Equations

Consider steady flow in a duct of constant diameter $D$ with no heat transfer and no work. Apply the conservation laws to a slice of length $dx$.

**Continuity:**

$$
\rho V = \text{const} \quad \Rightarrow \quad \frac{d\rho}{\rho} + \frac{dV}{V} = 0
$$

**Momentum.** The wall shear stress $\tau_w$ acts on the perimeter $\pi D$:

```math
-A\, dp - \tau_w \pi D\, dx = \rho V A\, dV \quad \Rightarrow \quad dp + \rho V\, dV +
\frac{4\tau_w}{D} dx = 0
```

**Energy.** The flow is adiabatic with no work, so $h_0$ is constant:

$$
c_p T + \frac{V^2}{2} = c_p T_0 = \text{const}
$$

The wall shear is expressed with the **Fanning friction factor** $f$, defined by $\tau_w = f \cdot \tfrac{1}{2}\rho V^2$. It is one quarter of the Darcy friction factor used in [pipes.md](../internal_flow/pipes.md), $f_D = 4f$, so $`4f\, L/D = f_D\, L/D`$. The friction factor comes from the Moody chart as in incompressible pipe flow. It stays nearly constant along the duct because $\rho V D/\mu$ changes only through the viscosity $\mu(T)$.

### The Fanno Relation

Combining continuity, momentum, energy, $p = \rho R T$ and $M^2 = V^2/(\gamma R T)$ gives one ordinary differential equation in $M$:

```math
\frac{4f\, dx}{D} = \frac{1 - M^2}{\gamma M^4 \left(1 + \frac{\gamma - 1}{2} M^2\right)}\, dM^2
```

The sign of $1 - M^2$ tells the story. Friction always adds a positive $dx$, so $dM^2 > 0$ for subsonic flow and $dM^2 < 0$ for supersonic flow. **Friction drives the Mach number toward 1 from either side.**

Integrate from a station with Mach number $M$ to the (possibly imaginary) station downstream where $M = 1$. The length between them is the **choking length** $L^*$:

$$
\frac{4f L^*}{D} = \frac{1 - M^2}{\gamma M^2} + \frac{\gamma + 1}{2\gamma}
\ln\left[\frac{(\gamma + 1) M^2}{2 + (\gamma - 1) M^2}\right]
$$

For two stations 1 and 2 in the same duct, a distance $L$ apart,

```math
\frac{4f L}{D} = \left(\frac{4f L^*}{D}\right)_{M_1} -
\left(\frac{4f L^*}{D}\right)_{M_2}
```

### Property Ratios

Continuity ($\rho V = \rho^* V^*$), constant $T_0$, and the state equation give the ratios to the sonic state:

```math
\frac{T}{T^*} = \frac{\gamma + 1}{2 + (\gamma - 1) M^2},
\qquad \frac{p}{p^*} = \frac{1}{M} \sqrt{\frac{\gamma + 1}{2 + (\gamma - 1) M^2}}
```

```math
\frac{\rho}{\rho^*} = \frac{V^*}{V} = \frac{1}{M}
\sqrt{\frac{2 + (\gamma - 1) M^2}{\gamma + 1}},
\qquad
\frac{p_0}{p_0^*} = \frac{1}{M}\left[\frac{2 + (\gamma - 1) M^2}{\gamma + 1}\right]^{\frac{\gamma + 1}{2(\gamma - 1)}}
```

The last ratio has the same form as the isentropic area ratio $`A/A^*`$. Ratios between two stations follow by division, for example $`p_2/p_1 = (p/p^*)_{M_2}/(p/p^*)_{M_1}`$.

| $M$ | $4fL^*/D$ | $T/T^*$ | $p/p^*$ | $\rho/\rho^*$ | $p_0/p_0^*$ |
| --- | --- | --- | --- | --- | --- |
| 0.2 | 14.533 | 1.1905 | 5.4554 | 4.5826 | 2.9635 |
| 0.3 | 5.2993 | 1.1788 | 3.6191 | 3.0702 | 2.0351 |
| 0.5 | 1.0691 | 1.1429 | 2.1381 | 1.8708 | 1.3398 |
| 0.8 | 0.07229 | 1.0638 | 1.2893 | 1.2119 | 1.0382 |
| 1.0 | 0 | 1 | 1 | 1 | 1 |
| 1.5 | 0.13605 | 0.8276 | 0.6065 | 0.7328 | 1.1762 |
| 2.0 | 0.30500 | 0.6667 | 0.4082 | 0.6124 | 1.6875 |
| 3.0 | 0.52216 | 0.4286 | 0.2182 | 0.5092 | 4.2346 |

As $M \to \infty$, $4fL^*/D$ tends to only $0.8215$. Supersonic flow can survive just a short length of duct before it chokes.

### Physical Behaviour

In **subsonic** Fanno flow, friction lowers the pressure. The density drops with it, so by continuity the velocity must rise. Kinetic energy grows while $h_0$ stays fixed, so the static temperature *falls*: the gas cools even though friction dissipates energy. In **supersonic** Fanno flow every trend reverses except the entropy rise and the loss of stagnation pressure.

### Frictional Choking

What happens if the actual duct is longer than $L^*$ for the inlet conditions?

- **Subsonic inlet.** The flow cannot pass $M = 1$ inside the duct. Signals travel upstream and the inlet Mach number drops until the duct length equals the new $L^*$. For a given reservoir, the mass flow decreases.
- **Supersonic inlet.** A normal shock forms inside the duct, and the flow behind it follows the subsonic branch to $M = 1$ at the exit. As the duct is lengthened further, the shock moves upstream until it reaches the supplying nozzle, and the whole duct becomes subsonic.

## Rayleigh Flow: Heat Addition Without Friction

### Governing Equations

Now take a constant-area duct with no friction and heat $q$ per unit mass added between stations 1 and 2.

$$
\rho_1 V_1 = \rho_2 V_2
$$

$$
p_1 + \rho_1 V_1^2 = p_2 + \rho_2 V_2^2
$$

$$
q = c_p (T_{02} - T_{01})
$$

The momentum equation is the same as for a normal shock, because friction is absent and the area is constant. Heat addition shows up **only as a change in stagnation temperature**.

### Property Ratios

With $\rho V^2 = \gamma p M^2$, the momentum equation gives $p(1 + \gamma M^2) = \text{const}$. Combining with continuity and the state equation gives:

```math
\frac{p}{p^*} = \frac{1 + \gamma}{1 + \gamma M^2},
\qquad \frac{T}{T^*} = M^2 \left(\frac{1 + \gamma}{1 + \gamma M^2}\right)^2,
\qquad \frac{\rho}{\rho^*} = \frac{V^*}{V} = \frac{1 + \gamma M^2}{(1 + \gamma) M^2}
```

```math
\frac{T_0}{T_0^*} = \frac{(\gamma + 1) M^2 \left[2 + (\gamma - 1) M^2\right]}{\left(1 + \gamma M^2\right)^2},
\qquad
\frac{p_0}{p_0^*} = \frac{1 + \gamma}{1 + \gamma M^2}\left[\frac{2 + (\gamma - 1) M^2}{\gamma + 1}\right]^{\gamma/(\gamma - 1)}
```

Here $T_0^*$ is the stagnation temperature the stream would have if enough heat were added to bring it exactly to $M = 1$.

| $M$ | $T_0/T_0^*$ | $T/T^*$ | $p/p^*$ | $p_0/p_0^*$ |
| --- | --- | --- | --- | --- |
| 0.2 | 0.17355 | 0.20661 | 2.2727 | 1.2346 |
| 0.3 | 0.34686 | 0.40887 | 2.1314 | 1.1985 |
| 0.5 | 0.69136 | 0.79012 | 1.7778 | 1.1141 |
| 0.845 | 0.97959 | 1.02857 | 1.2000 | 1.0116 |
| 1.0 | 1 | 1 | 1 | 1 |
| 2.0 | 0.79339 | 0.52893 | 0.3636 | 1.5031 |
| 3.0 | 0.65398 | 0.28028 | 0.1765 | 3.4245 |

### Physical Behaviour

- $T_0/T_0^*$ reaches its maximum of 1 at $M = 1$. **Heating drives the Mach number toward 1 from either side, and cooling drives it away from 1.**
- Heating always lowers the stagnation pressure. This is the "Rayleigh loss" that combustor designers minimise by burning at low Mach number. At $M \to 0$ the loss is still finite: $p_0/p_0^*$ falls from $1.268$ to 1 as a low-speed stream is heated all the way to choking.
- The static temperature peaks at $M = 1/\sqrt{\gamma} = 0.845$, where $T/T^* = (\gamma + 1)^2/(4\gamma) = 1.0286$. Between $M = 0.845$ and $M = 1$, adding heat *lowers* the static temperature. So much of the added energy goes into accelerating the flow that the kinetic energy increase exceeds the heat input. For example, heating from $M = 0.85$ to $M = 0.95$ raises $T_0$ by 1.75% but lowers $T$ by 1.35%.

### Thermal Choking

The largest amount of heat a stream at $M_1$ can absorb is

```math
q_{max} = c_p \left(T_0^* - T_{01}\right) = c_p
T_{01}\left[\frac{1}{(T_0/T_0^*)_{M_1}} - 1\right]
```

If more heat is added, the duct is **thermally choked**. A subsonic flow responds by reducing its inlet Mach number, and hence its mass flow, until the exit is just sonic. A supersonic flow responds with a shock that moves upstream. This is one of the main operating limits of ramjets and afterburners.

Note that $M = 1/\sqrt{\gamma}$ is *not* the choking point of Rayleigh flow, only the point of maximum static temperature. The same value is the limiting Mach number of isothermal flow with friction, which is a different model.

## T–s Diagrams

Plotting static temperature against entropy gives a map of each process. For Fanno flow $`(s - s^*)/R = \ln\left[(T/T^*)^{\gamma/(\gamma - 1)}/(p/p^*)\right]`$, and similarly for Rayleigh flow. A line on this map is the set of all states with the same mass flux $\rho V$ and the same $h_0$ (Fanno) or the same $p + \rho V^2$ (Rayleigh).

**Fanno line.** The line is a "nose" pointing toward higher entropy. The subsonic branch is the upper part, at high temperature and low kinetic energy. The supersonic branch is the lower part. Entropy is **maximum at $M = 1$**. Friction can only increase entropy, so both branches move toward the nose.

```
   T
   ^
   |  .  M -> 0
   |      '  .                  subsonic branch
   |            '  .            (friction: M increases, T decreases)
   |                 ' .
   |                     '.
   |                       :   <-- M = 1, maximum entropy
   |                     .'
   |                 . '
   |            .  '            supersonic branch
   |      .  '                  (friction: M decreases, T increases)
   |  .
   +--------------------------------------------> s
```

**Rayleigh line.** Entropy is also maximum at $M = 1$ on this line. The upper subsonic branch climbs to its highest temperature at $M = 1/\sqrt{\gamma}$ just before the nose. Heat addition ($ds > 0$) moves the state toward $M = 1$, and cooling moves it away.

```
   T
   ^
   |                   _.--._     <-- T max at M = 1/sqrt(gamma)
   |               _.-'      '.
   |           _.-'            \  <-- M = 1, maximum entropy
   |       _.-'  subsonic      /
   |     .'      branch      .'
   |   .'                  .'
   |  /                  .'   supersonic branch
   | /                 .'
   |/                .'
   +--------------------------------------------> s
```

**Link to normal shocks.** A normal shock conserves mass flux, $h_0$ and $p + \rho V^2$. The states before and after it therefore lie on *both* the Fanno line and the Rayleigh line through the upstream state. The two lines intersect in two points, one supersonic and one subsonic, and these are exactly the upstream and downstream states of the normal shock. The jump goes from the supersonic point to the subsonic point, the direction of increasing entropy. For example, at $M_1 = 2$ and $M_2 = 0.5774$, both the Fanno and the Rayleigh pressure ratios give $p_2/p_1 = 4.5$, matching [shock_waves.md](shock_waves.md).

### Summary of Trends

| Property | Fanno, subsonic | Fanno, supersonic | Rayleigh heating, subsonic | Rayleigh heating, supersonic |
| --- | --- | --- | --- | --- |
| $M$ | increases | decreases | increases | decreases |
| $V$ | increases | decreases | increases | decreases |
| $p$ | decreases | increases | decreases | increases |
| $\rho$ | decreases | increases | decreases | increases |
| $T$ | decreases | increases | increases (decreases for $M > 0.845$) | increases |
| $T_0$ | constant | constant | increases | increases |
| $p_0$ | decreases | decreases | decreases | decreases |
| $s$ | increases | increases | increases | increases |

For Rayleigh flow with cooling, every arrow in the last two columns reverses.

## Worked Example 1: Fanno Flow in a Pipe

Air enters a pipe with $D = 5\ \text{cm}$ and Darcy friction factor $f_D = 4f = 0.02$ at $M_1 = 0.3$, $T_1 = 300\ \text{K}$ and $p_1 = 200\ \text{kPa}$. The pipe is 8 m long.

**Is the pipe choked?**

```math
\left(\frac{4fL^*}{D}\right)_1 = 5.2993 \quad \Rightarrow \quad
L_1^* = \frac{5.2993 \times 0.05}{0.02} = 13.25\ \text{m}
```

Since $8\ \text{m} < 13.25\ \text{m}$, the pipe is not choked.

**Exit Mach number.**

$$
\left(\frac{4fL^*}{D}\right)_2 = 5.2993 - \frac{0.02 \times 8}{0.05} = 2.0993 \quad
\Rightarrow \quad M_2 = 0.4121 \quad \text{(subsonic root)}
$$

**Exit properties.**

- $T_2 = 300 \times 1.1606/1.1788 = 295.4\ \text{K}$ (the gas cooled);
- $p_2 = 200 \times (p/p^*)_{M_2}/3.6191 = 144.5\ \text{kPa}$;
- $V_1 = 104.2\ \text{m/s}$ and $V_2 = 142.0\ \text{m/s}$;
- $T_0 = 305.4\ \text{K}$ at both ends.

**Losses.** $p_{02}/p_{01} = 0.7627$, so $s_2 - s_1 = -287 \ln 0.7627 = 77.7\ \text{J/(kg K)}$.

**Mass flow.** $`\rho_1 V_1 = 2.3229 \times 104.16 = 241.9\ \text{kg/(m}^2\,\text{s)}`$, which gives $\dot m = 0.475\ \text{kg/s}$. The same value is recovered at the exit.

**A longer pipe.** Suppose the pipe is fed from the same reservoir ($p_{01} = 212.9\ \text{kPa}$, $T_{01} = 305.4\ \text{K}$) through a short isentropic entrance, but is 20 m long. Then $4fL/D = 8.0 > 5.2993$ and the pipe chokes. The inlet Mach number drops to the value with $4fL^*/D = 8.0$, which is $M_1 = 0.2559$. The mass flow falls to 86.6% of its previous value, and the exit is exactly sonic.

## Worked Example 2: Heat Addition in a Combustor

Air enters a constant-area combustor at $M_1 = 0.2$, $T_1 = 400\ \text{K}$ and $p_1 = 150\ \text{kPa}$, and receives $q = 800\ \text{kJ/kg}$. Treat the gas as air throughout.

**Stagnation temperatures.**

```math
T_{01} = 400 \times 1.008 = 403.2\ \text{K},
\qquad T_{02} = 403.2 + \frac{800\,000}{1004.5} = 1199.6\ \text{K}
```

**Reference state and exit Mach number.**

```math
T_0^* = \frac{403.2}{0.17355} = 2323.2\ \text{K},
\qquad \frac{T_{02}}{T_0^*} = 0.5164 \quad \Rightarrow \quad M_2 = 0.3928
```

**Exit properties.**

- $T_2 = 400 \times (T/T^*)_{M_2}/0.20661 = 1163.7\ \text{K}$;
- $p_2 = 150 \times (p/p^*)_{M_2}/2.2727 = 130.3\ \text{kPa}$;
- $V_1 = 80.2\ \text{m/s}$ and $V_2 = 268.6\ \text{m/s}$.
- Check: $p + \rho V^2 = 158.4\ \text{kPa}$ at both stations.

**Stagnation-pressure loss.** $p_{02}/p_{01} = 0.9393$, from 154.2 kPa to 144.9 kPa, even though there is no friction.

**Choking limit.** $q_{max} = 1004.5 \times (2323.2 - 403.2) = 1928.6\ \text{kJ/kg}$.

**Too much heat.** If $q = 2500\ \text{kJ/kg}$ is added instead, the combustor chokes. The exit stagnation temperature $T_{02} = 2892.0\ \text{K}$ becomes the new $`T_0^*`$, so the inlet must satisfy $`T_0/T_0^* = 403.2/2892.0 = 0.1394`$, giving $M_1 = 0.1774$. With the same upstream stagnation state, the mass flow drops to 89.1% of its original value.

## Related Scripts

- [compressible_vs_incompressible](../../../scripts/plots/compressible_vs_incompressible/): contrasts a fully developed incompressible pipe profile with a compressible one that accelerates along the pipe. This is a qualitative picture of subsonic Fanno flow, where the density falls and the velocity rises with distance.

## Exercises

**Exercise 1.** Air enters a duct of 2 cm diameter with $f_D = 0.016$ at $M_1 = 2.5$. What is the longest duct that can be used without a shock forming inside it?

<details>
<summary>Answer</summary>

$`(4fL^*/D)_{2.5} = 0.4320`$, so $`L^* = 0.4320 \times 0.02/0.016 = 0.540\ \text{m}`$.

A longer duct forces a normal shock into the duct. Even an infinitely high inlet Mach number would allow only $4fL^*/D = 0.8215$, or $L = 1.03\ \text{m}$.

</details>

**Exercise 2.** In the same duct ($D = 2\ \text{cm}$, $f_D = 0.016$), air enters at $M_1 = 3$ and flows through 0.5 m. Find $M_2$, $T_2/T_1$, $p_2/p_1$ and $p_{02}/p_{01}$.

<details>
<summary>Answer</summary>

$4fL/D = 0.016 \times 0.5/0.02 = 0.4$. Then $(4fL^*/D)_2 = 0.5222 - 0.4 = 0.1222$, and the supersonic root is $M_2 = 1.462$.

$`T_2/T_1 = (T/T^*)_{1.462}/(T/T^*)_{3} = 1.962`$.

$p_2/p_1 = 2.874$.

$p_{02}/p_{01} = (p_0/p_0^*)_{1.462}/4.2346 = 0.2719$.

Supersonic friction is extremely lossy: nearly three quarters of the stagnation pressure is lost in 25 diameters.

</details>

**Exercise 3.** A subsonic stream enters a frictionless heated duct at $M_1 = 0.3$ with $T_{01} = 400\ \text{K}$. How much heat per unit mass can be added before the duct chokes?

<details>
<summary>Answer</summary>

$`(T_0/T_0^*)_{0.3} = 0.34686`$, so $`T_0^* = 400/0.34686 = 1153.2\ \text{K}`$.

$q_{max} = 1004.5 \times (1153.2 - 400) = 756.6\ \text{kJ/kg}$.

</details>

**Exercise 4.** A supersonic stream at $M_1 = 3$ and $T_1 = 300\ \text{K}$ receives $q = 300\ \text{kJ/kg}$ in a constant-area frictionless duct. Find $M_2$, $T_2$, $p_2/p_1$ and $p_{02}/p_{01}$. What is the maximum heat addition for this inlet state?

<details>
<summary>Answer</summary>

$T_{01} = 300 \times 2.8 = 840\ \text{K}$ and $`T_{02} = 840 + 300\,000/1004.5 = 1138.7\ \text{K}`$.

$T_0^* = 840/0.65398 = 1284.4\ \text{K}$, so $T_{02}/T_0^* = 0.8865$ and the supersonic root is $M_2 = 1.591$.

$`T_2 = 300 \times (T/T^*)_{1.591}/0.28028 = 756.0\ \text{K}`$, $`p_2/p_1 = 2.994`$, and $`p_{02}/p_{01} = 0.3417`$.

$q_{max} = 1004.5 \times (1284.4 - 840) = 446.4\ \text{kJ/kg}$.

Heating supersonic flow slows it, compresses it and costs a large fraction of the total pressure. This is why supersonic combustion is so demanding.

</details>

**Exercise 5.** Show that the states on either side of a normal shock with $M_1 = 2$ ($M_2 = 0.5774$) lie on the same Fanno line and the same Rayleigh line, by computing $p_2/p_1$ and $T_2/T_1$ from the Fanno ratios and from the Rayleigh ratios.

<details>
<summary>Answer</summary>

**Fanno ratios.** $`p_2/p_1 = (p/p^*)_{0.5774}/(p/p^*)_{2} = 1.8371/0.40825 = 4.500`$, and $T_2/T_1 = 1.125/0.66667 = 1.6875$.

**Rayleigh ratios.** $p_2/p_1 = 1.63636/0.36364 = 4.500$, and $T_2/T_1 = 0.89256/0.52893 = 1.6875$.

Both agree with the normal-shock relations ($p_2/p_1 = 4.5$, $T_2/T_1 = 1.6875$). The Fanno line carries fixed $\rho V$ and $h_0$, and the Rayleigh line fixed $\rho V$ and $p + \rho V^2$. The shock conserves all three, so both endpoints lie on both lines.

</details>

## References

- Shapiro, A. H., *The Dynamics and Thermodynamics of Compressible Fluid Flow*, Vol. 1, Ronald Press, 1953. Includes the classic treatment of generalised one-dimensional flow with friction and heat transfer.
- Zucker, R. D., and Biblarz, O., *Fundamentals of Gas Dynamics*, 2nd ed., Wiley, 2002.
- Anderson, J. D., *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003. Chapter 3 covers flow with heat addition and with friction.
