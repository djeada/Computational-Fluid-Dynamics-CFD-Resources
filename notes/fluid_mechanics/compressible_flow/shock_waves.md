# Shock Waves and Expansion Fans

## Overview

A shock wave is an extremely thin region, only a few molecular mean free paths thick (of order $10^{-7}\ \text{m}$ in sea-level air), across which pressure, density, temperature and velocity change almost discontinuously. Shocks form because compression waves steepen as they travel. The high-pressure part of a compression is hotter, so its sound speed is higher, and it also moves with the fluid velocity the wave has induced. It therefore catches up with the weaker parts ahead until the wave becomes a near-discontinuity. Expansion waves do the opposite and spread out into fans.

For design and CFD, the internal structure of a shock is irrelevant. What matters is the jump in properties, which follows from applying conservation laws to a control volume around the shock. This page covers:

- **normal shocks**: the Rankine–Hugoniot jump conditions, entropy rise and total-pressure loss;
- **oblique shocks**: the $\theta$–$\beta$–$M$ relation, weak and strong solutions, and detachment;
- **Prandtl–Meyer expansion fans**: the isentropic turning of supersonic flow around convex corners.

Background on stagnation properties and entropy is in [thermodynamics.md](thermodynamics.md), and on Mach waves in [speed_of_sound.md](speed_of_sound.md). Numbers are for air with $\gamma = 1.4$ and $R = 287\ \text{J/(kg K)}$.

## Normal Shocks

### Jump Conditions

Place a control volume around a stationary shock normal to the flow. State 1 is upstream and state 2 downstream. The flow is steady, there is no heat transfer or work, and viscous stresses act only inside the shock, so they do not appear at the control-volume faces:

$$
\rho_1 u_1 = \rho_2 u_2
$$

$$
p_1 + \rho_1 u_1^2 = p_2 + \rho_2 u_2^2
$$

$$
h_1 + \frac{u_1^2}{2} = h_2 + \frac{u_2^2}{2}
$$

Together with $p = \rho R T$ and $h = c_p T$ these are the **Rankine–Hugoniot conditions**. The same equations also allow the trivial solution: no shock at all.

### The Prandtl Relation

Divide the momentum equation by the continuity equation and use $a^2 = \gamma p/\rho$:

$$
\frac{a_1^2}{\gamma u_1} - \frac{a_2^2}{\gamma u_2} = u_2 - u_1
$$

The energy equation holds on both sides with the same $T_0$, and hence the same sonic speed $a^*$:

$$
a^2 = \frac{\gamma + 1}{2} a^{*2} - \frac{\gamma - 1}{2} u^2
$$

Substituting for $a_1^2$ and $a_2^2$ and dividing by $u_2 - u_1 \neq 0$ leaves the **Prandtl relation**:

$$
u_1 u_2 = a^{*2}
$$

With the characteristic Mach number $M^* = u/a^*$, this reads $M_1^* M_2^* = 1$. If the upstream flow is supersonic ($M_1^* > 1$), the downstream flow must be subsonic.

### Property Ratios

Using $M^{*2} = (\gamma + 1)M^2/[2 + (\gamma - 1)M^2]$ and the three conservation laws, all ratios can be written in terms of $M_1$ alone:

$$
\frac{\rho_2}{\rho_1} = \frac{u_1}{u_2} = \frac{(\gamma + 1) M_1^2}{(\gamma - 1) M_1^2 + 2}
$$

$$
\frac{p_2}{p_1} = 1 + \frac{2\gamma}{\gamma + 1}\left(M_1^2 - 1\right)
$$

$$
\frac{T_2}{T_1} = \frac{p_2}{p_1} \frac{\rho_1}{\rho_2}
$$

$$
M_2^2 = \frac{1 + \frac{\gamma - 1}{2} M_1^2}{\gamma M_1^2 - \frac{\gamma - 1}{2}}
$$

The stagnation temperature is unchanged, $T_{02} = T_{01}$. The stagnation-pressure ratio is

$$
\frac{p_{02}}{p_{01}} = \left[\frac{(\gamma + 1) M_1^2}{(\gamma - 1) M_1^2 + 2}\right]^{\gamma/(\gamma - 1)} \left[\frac{\gamma + 1}{2\gamma M_1^2 - (\gamma - 1)}\right]^{1/(\gamma - 1)}
$$

Eliminating the Mach number gives the **Hugoniot curve**, which relates the density and pressure ratios directly:

$$
\frac{\rho_2}{\rho_1} = \frac{1 + \frac{\gamma + 1}{\gamma - 1}\frac{p_2}{p_1}}{\frac{\gamma + 1}{\gamma - 1} + \frac{p_2}{p_1}}
$$

For the same pressure ratio, a shock compresses the gas *less* than an isentropic process. At $p_2/p_1 = 4.5$ the shock gives $\rho_2/\rho_1 = 2.667$, while an isentropic compression gives $4.5^{1/1.4} = 2.928$. The difference appears as extra temperature rise and entropy. As $M_1 \to \infty$ the density ratio tends to $(\gamma + 1)/(\gamma - 1) = 6$ and $M_2 \to \sqrt{(\gamma - 1)/(2\gamma)} = 0.378$, while pressure and temperature grow without bound.

| $M_1$ | $M_2$ | $p_2/p_1$ | $\rho_2/\rho_1$ | $T_2/T_1$ | $p_{02}/p_{01}$ | $(s_2 - s_1)/R$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1.2 | 0.8422 | 1.5133 | 1.3416 | 1.1280 | 0.9928 | 0.0072 |
| 1.5 | 0.7011 | 2.4583 | 1.8621 | 1.3202 | 0.9298 | 0.0728 |
| 2.0 | 0.5774 | 4.5000 | 2.6667 | 1.6875 | 0.7209 | 0.3273 |
| 3.0 | 0.4752 | 10.333 | 3.8571 | 2.6790 | 0.3283 | 1.1137 |
| 5.0 | 0.4152 | 29.000 | 5.0000 | 5.8000 | 0.0617 | 2.7852 |

### Entropy Rise and Why Expansion Shocks Cannot Exist

The shock is adiabatic, so the entropy change follows from the stagnation-pressure ratio (see [thermodynamics.md](thermodynamics.md)):

$$
s_2 - s_1 = c_p \ln \frac{T_2}{T_1} - R \ln \frac{p_2}{p_1} = -R \ln
\frac{p_{02}}{p_{01}}
$$

The jump conditions are purely algebraic and have solutions for $M_1 < 1$ as well. At $M_1 = 0.8$ they predict a rarefaction "shock" with $p_2/p_1 = 0.58$. They also give $p_{02}/p_{01} = 1.0165$, which means $s_2 - s_1 = -0.0164\, R < 0$. **Entropy would decrease in an adiabatic process, which violates the second law.** Only the $M_1 > 1$ branch is physical, so every normal shock:

- takes supersonic flow to subsonic flow;
- increases $p$, $\rho$ and $T$ and decreases $u$;
- conserves $T_0$ and destroys stagnation pressure.

For weak shocks the entropy rise is very small. To leading order,

$$
\frac{s_2 - s_1}{R} \approx \frac{2\gamma}{3(\gamma + 1)^2}\left(M_1^2 - 1\right)^3
$$

It is third order in shock strength, while the pressure jump is first order. A weak shock is therefore almost isentropic, which is why weak compressions can be treated with isentropic relations and Mach-wave theory.

### Total-Pressure Loss and the Pitot Tube

The loss of stagnation pressure is lost capacity to do work. A supersonic inlet that decelerates $M = 3$ air through a single normal shock keeps only 33% of the free-stream total pressure. That is why practical inlets use a series of weaker oblique shocks.

A pitot tube in supersonic flow has a detached normal shock in front of its mouth. It measures $p_{02}$, not $p_{01}$. Combining the normal-shock ratio with the isentropic deceleration behind the shock gives the **Rayleigh pitot-tube formula**:

$$
\frac{p_{02}}{p_1} = \left[\frac{(\gamma + 1)^2 M_1^2}{4\gamma M_1^2 - 2(\gamma - 1)}\right]^{\gamma/(\gamma - 1)} \frac{1 - \gamma + 2\gamma M_1^2}{\gamma + 1}
$$

At $M_1 = 2$, $p_{02}/p_1 = 5.640$, whereas the isentropic value would be $p_{01}/p_1 = 7.824$.

### Worked Example 1: Normal Shock at Mach 2

Air at $M_1 = 2$, $T_1 = 288.15\ \text{K}$ and $p_1 = 101.325\ \text{kPa}$ passes through a normal shock.

**Upstream.**

- $a_1 = 340.3\ \text{m/s}$, so $u_1 = 680.5\ \text{m/s}$;
- $\rho_1 = 1.2252\ \text{kg/m}^3$;
- $T_0 = 288.15 \times 1.8 = 518.7\ \text{K}$;
- $p_{01} = 101.325 \times 7.8244 = 792.8\ \text{kPa}$.

**Downstream.**

- $M_2 = 0.5774$;
- $p_2 = 4.5 \times 101.325 = 456.0\ \text{kPa}$;
- $T_2 = 1.6875 \times 288.15 = 486.3\ \text{K}$;
- $\rho_2 = 2.6667 \times 1.2252 = 3.267\ \text{kg/m}^3$;
- $u_2 = 680.5/2.6667 = 255.2\ \text{m/s}$;
- $p_{02} = 0.7209 \times 792.8 = 571.5\ \text{kPa}$.

**Checks.**

- Momentum: $p + \rho u^2 = 668.7\ \text{kPa}$ on both sides.
- Energy: $c_p T + u^2/2 = 521.0\ \text{kJ/kg}$ on both sides.
- Prandtl relation: $u_1 u_2 = 173\,668\ \text{m}^2/\text{s}^2 = a^{*2} = 2\gamma R T_0/(\gamma + 1)$.
- Entropy: $s_2 - s_1 = -287 \ln 0.7209 = 93.9\ \text{J/(kg K)}$.

## Oblique Shocks

### Geometry and Decomposition

When supersonic flow meets a concave corner or a wedge of half-angle $\theta$, it is turned by a straight **oblique shock** inclined at the wave angle $\beta$ to the upstream flow.

```
                                          /
                                        /   oblique shock
       M1                             /
   ---------->                      /
   ---------->                    /        M2
   ---------->                  /     _____----->
   ---------->                /____---
   ---------->              / --   theta
   ======================= O ------------------------------
                           ^ beta measured between the upstream flow and the shock
```

Split the velocity into components normal and tangential to the shock. There is no pressure gradient along the shock, so the tangential momentum equation gives **equal tangential velocity on both sides**. The normal components obey exactly the normal-shock relations, with the normal Mach numbers

$$
M_{n1} = M_1 \sin\beta,
\qquad M_{n2} = M_2 \sin(\beta - \theta)
$$

Every ratio in the normal-shock table (pressure, density, temperature, total pressure) applies with $M_1$ replaced by $M_{n1}$. The downstream Mach number is $M_2 = M_{n2}/\sin(\beta - \theta)$.

### The θ–β–M Relation

Geometry gives $\tan\beta = u_{n1}/u_t$ and $\tan(\beta - \theta) = u_{n2}/u_t$. Continuity gives $u_{n2}/u_{n1} = \rho_1/\rho_2$. Hence

$$
\frac{\tan(\beta - \theta)}{\tan\beta} = \frac{(\gamma - 1) M_1^2 \sin^2\beta + 2}{(\gamma + 1) M_1^2 \sin^2\beta}
$$

After some trigonometry this becomes the **$\theta$–$\beta$–$M$ relation**:

$$
\tan\theta = 2\cot\beta\, \frac{M_1^2 \sin^2\beta - 1}{M_1^2 (\gamma + \cos 2\beta) + 2}
$$

### Weak, Strong and Detached Shocks

For a given $M_1$, $\theta$ is zero at two wave angles: at the Mach angle $\beta = \mu = \arcsin(1/M_1)$, an infinitely weak Mach wave, and at $\beta = 90^\circ$, a normal shock. In between it rises to a maximum $\theta_{max}$. So:

- **$\theta < \theta_{max}$**: there are two solutions. The **weak** solution has the smaller $\beta$ and a downstream flow that is usually still supersonic. The **strong** solution has $\beta$ near $90^\circ$ and a subsonic downstream flow. On wedges and ramps in open flows the weak shock is what is normally observed. The strong solution appears only when a high downstream pressure forces it, for example in some inlet and duct flows.
- **$\theta > \theta_{max}$**: no straight attached shock can turn the flow. The shock **detaches** and stands ahead of the body as a curved **bow shock**. It is locally normal on the axis, with subsonic flow behind that part, and it weakens toward a Mach wave far from the body.

| $M_1$ | 1.5 | 2 | 3 | 5 | 10 | $\to \infty$ |
| --- | --- | --- | --- | --- | --- | --- |
| $\theta_{max}$ | $12.11^\circ$ | $22.97^\circ$ | $34.07^\circ$ | $41.12^\circ$ | $44.43^\circ$ | $45.58^\circ$ |
| $\beta$ at $\theta_{max}$ | $66.6^\circ$ | $64.7^\circ$ | $65.2^\circ$ | $66.6^\circ$ | $67.5^\circ$ |  |

The $\theta$–$\beta$–$M$ relation is explicit only for $\theta$. To find $\beta$ from $\theta$, bracket the weak root on $(\mu, \beta_{\theta_{max}})$ and the strong root on $(\beta_{\theta_{max}}, 90^\circ)$, and solve each with a scalar root finder. This is how the numbers below were computed.

### Worked Example 2: Wedge in a Mach 2 Stream

A $10^\circ$ half-angle wedge is placed in air at $M_1 = 2$.

**Weak solution.**

- $\beta = 39.31^\circ$ and $M_{n1} = 2 \sin 39.31^\circ = 1.267$;
- normal-shock relations at 1.267: $M_{n2} = 0.8032$, $p_2/p_1 = 1.707$, $\rho_2/\rho_1 = 1.458$, $T_2/T_1 = 1.170$, $p_{02}/p_{01} = 0.9846$;
- $M_2 = 0.8032/\sin(29.31^\circ) = 1.641$, still supersonic.
- Check: $\tan 39.31^\circ/\tan 29.31^\circ = 1.458 = \rho_2/\rho_1$.

**Strong solution.** $\beta = 83.70^\circ$, $M_2 = 0.604$, $p_2/p_1 = 4.444$, $p_{02}/p_{01} = 0.7265$.

Compare with a normal shock at the same Mach number, which has $p_{02}/p_{01} = 0.7209$. Turning the flow through the weak oblique shock costs only 1.5% of the total pressure. If the wedge angle were $25^\circ > \theta_{max} = 22.97^\circ$, the shock would detach.

## Prandtl–Meyer Expansion Fans

### Turning Through Mach Waves

When supersonic flow turns *away* from itself around a convex corner, the area available to the flow increases, and supersonic flow accelerates. The turning happens through a centred fan of infinitely many Mach waves radiating from the corner. Each wave is infinitely weak, so the whole expansion is **isentropic**: $p_0$ and $T_0$ stay constant.

```
   M1 ------------>        /  forward Mach line, at mu1 to the upstream flow
   M1 ------------>      /    .
   M1 ------------>    /   .    ,  rear Mach line, at mu2 to the downstream flow
   M1 ------------>  /  .   ,
   ================ O .  ,         M2 > M1
                      \   ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~>
                        \  theta
                          \  wall turns away by theta
```

Across one Mach wave that turns the flow by $d\theta$, the geometry of the wave gives $dV/V = d\theta/\sqrt{M^2 - 1}$. Using $V = M a$ and $a/a_0 = (1 + \tfrac{\gamma - 1}{2}M^2)^{-1/2}$,

$$
d\theta = \frac{\sqrt{M^2 - 1}}{1 + \frac{\gamma - 1}{2} M^2} \frac{dM}{M}
$$

Integrating from $M = 1$ defines the **Prandtl–Meyer function**:

$$
\nu(M) = \sqrt{\frac{\gamma + 1}{\gamma - 1}} \arctan
\sqrt{\frac{\gamma - 1}{\gamma + 1}\left(M^2 - 1\right)} - \arctan \sqrt{M^2 - 1}
$$

A turn through $\theta$ changes the Mach number according to

$$
\nu(M_2) = \nu(M_1) + \theta
$$

The static properties then follow from the isentropic ratios with constant $p_0$ and $T_0$, for example $p_2/p_1 = (p_0/p)_{M_1}/(p_0/p)_{M_2}$.

| $M$ | 1.5 | 2.0 | 2.5 | 3.0 |
| --- | --- | --- | --- | --- |
| $\nu$ | $11.91^\circ$ | $26.38^\circ$ | $39.12^\circ$ | $49.76^\circ$ |

The function has a maximum $\nu_{max} = \tfrac{\pi}{2}\left(\sqrt{(\gamma + 1)/(\gamma - 1)} - 1\right) = 130.45^\circ$. This is the largest turn a sonic stream can make, expanding all the way to zero pressure.

The same function describes **isentropic compression** on a gradually curved concave wall. There the Mach waves converge and eventually merge into an oblique shock away from the wall.

### Worked Example 3: Expansion Corner

Air at $M_1 = 2$ flows around a convex corner that turns it by $10^\circ$.

$$
\nu(M_2) = 26.38^\circ + 10^\circ = 36.38^\circ \quad \Rightarrow \quad M_2 = 2.385
$$

$$
\frac{p_2}{p_1} = \frac{7.8244}{(1 + 0.2 \times 2.385^2)^{3.5}} = 0.5480,
\qquad \frac{T_2}{T_1} = \frac{1.8}{1 + 0.2 \times 2.385^2} = 0.8421
$$

The fan starts at $\mu_1 = 30.0^\circ$ to the upstream flow. It ends at $\mu_2 = 24.79^\circ$ to the turned flow, which is $14.79^\circ$ to the original flow direction.

## Summary

- Normal shocks conserve mass, momentum and $h_0$. They take $M_1 > 1$ to $M_2 < 1$ and raise $p$, $\rho$, $T$ and $s$.
- Expansion shocks would decrease entropy and cannot exist. The entropy rise across weak shocks scales as $(M_1^2 - 1)^3$.
- $s_2 - s_1 = -R \ln(p_{02}/p_{01})$, so shocks are measured by total-pressure loss.
- Oblique shocks are normal shocks in the normal component $M_1 \sin\beta$. The $\theta$–$\beta$–$M$ relation gives weak and strong solutions below $\theta_{max}$ and a detached bow shock above it.
- Convex corners produce isentropic Prandtl–Meyer fans with $\nu(M_2) = \nu(M_1) + \theta$.

## Exercises

**Exercise 1.** A normal shock stands in air at $M_1 = 3$. Find $M_2$, $p_2/p_1$, $\rho_2/\rho_1$, $T_2/T_1$, $p_{02}/p_{01}$ and the entropy rise.

<details>
<summary>Answer</summary>

$p_2/p_1 = 1 + (2.8/2.4)(9 - 1) = 10.333$.

$\rho_2/\rho_1 = 2.4 \times 9/(0.4 \times 9 + 2) = 21.6/5.6 = 3.857$.

$T_2/T_1 = 10.333/3.857 = 2.679$.

$M_2^2 = (1 + 0.2 \times 9)/(1.4 \times 9 - 0.2) = 2.8/12.4 = 0.2258$, so $M_2 = 0.4752$.

$p_{02}/p_{01} = 0.3283$, so $s_2 - s_1 = -287 \ln 0.3283 = 319.6\ \text{J/(kg K)}$.

</details>

**Exercise 2.** A pitot tube in a supersonic wind tunnel reads a pressure 8.0 times the static pressure measured at a wall tap. Find the free-stream Mach number. What Mach number would you get, incorrectly, from the isentropic relation?

<details>
<summary>Answer</summary>

The probe reads $p_{02}$ behind its bow shock. Solve the Rayleigh pitot formula $p_{02}/p_1 = 8.0$ numerically: $M_1 = 2.417$.

Using the isentropic relation $p_0/p = (1 + 0.2 M^2)^{3.5} = 8.0$ would give $M = 2.014$. This is 17% too low, because it ignores the total-pressure loss across the shock.

</details>

**Exercise 3.** A wedge of half-angle $15^\circ$ is placed in a Mach 3 air stream. Find the weak-shock wave angle, the downstream Mach number, and the pressure, temperature and stagnation-pressure ratios. What happens if the half-angle is increased to $40^\circ$?

<details>
<summary>Answer</summary>

Solving the $\theta$–$\beta$–$M$ relation on the weak branch: $\beta = 32.24^\circ$ and $M_{n1} = 3 \sin 32.24^\circ = 1.600$.

Normal-shock relations at 1.600: $M_{n2} = 0.6683$, $p_2/p_1 = 2.822$, $T_2/T_1 = 1.388$, $p_{02}/p_{01} = 0.8950$.

$M_2 = 0.6683/\sin(17.24^\circ) = 2.255$.

For $M_1 = 3$, $\theta_{max} = 34.07^\circ$. A $40^\circ$ wedge exceeds this, so no attached oblique shock exists and a detached bow shock forms ahead of the wedge.

</details>

**Exercise 4.** Air at $M_1 = 1.5$ expands around a $20^\circ$ convex corner. Find $M_2$, $p_2/p_1$ and the angles of the fan boundaries.

<details>
<summary>Answer</summary>

$\nu(1.5) = 11.91^\circ$, so $\nu(M_2) = 31.91^\circ$ and solving gives $M_2 = 2.207$.

$p_2/p_1 = (1 + 0.2 \times 1.5^2)^{3.5}/(1 + 0.2 \times 2.207^2)^{3.5} = 3.671/10.80 = 0.3398$.

The forward Mach line is at $\mu_1 = \arcsin(1/1.5) = 41.81^\circ$ to the upstream flow. The rear Mach line is at $\mu_2 = \arcsin(1/2.207) = 26.95^\circ$ to the downstream flow.

</details>

**Exercise 5.** A flat plate is at $5^\circ$ angle of attack in air at $M_\infty = 2.5$. Use shock-expansion theory (an oblique shock on the lower surface and a Prandtl–Meyer expansion on the upper surface) to find the lift and wave-drag coefficients. Compare with linearised supersonic theory, $c_l = 4\alpha/\sqrt{M_\infty^2 - 1}$ and $c_d = 4\alpha^2/\sqrt{M_\infty^2 - 1}$.

<details>
<summary>Answer</summary>

**Lower surface.** An oblique shock with $\theta = 5^\circ$ has $\beta = 27.42^\circ$ and $p_l/p_\infty = 1.380$.

**Upper surface.** An expansion by $5^\circ$: $\nu = 39.12^\circ + 5^\circ = 44.12^\circ$, so $M_u = 2.723$ and $p_u/p_\infty = 0.7080$.

**Coefficients.** With $q_\infty/p_\infty = \gamma M_\infty^2/2 = 4.375$, the normal-force coefficient is $c_n = (1.380 - 0.7080)/4.375 = 0.1536$. Then $c_l = c_n \cos 5^\circ = 0.1530$ and $c_d = c_n \sin 5^\circ = 0.01339$.

**Linear theory.** With $\alpha = 0.08727\ \text{rad}$: $c_l = 4 \times 0.08727/2.291 = 0.1523$ and $c_d = 0.01329$.

At this small angle the two methods agree to within 0.5% for lift and 0.7% for drag.

</details>

## References

- Anderson, J. D., *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003. Chapters 3 and 4 cover normal and oblique shocks and expansion waves.
- Liepmann, H. W., and Roshko, A., *Elements of Gasdynamics*, Wiley, 1957 (reprinted by Dover).
- Ames Research Staff, *Equations, Tables, and Charts for Compressible Flow*, NACA Report 1135, 1953. Includes normal-shock tables and oblique-shock charts.
- Anderson, J. D., *Fundamentals of Aerodynamics*, McGraw-Hill.
