# Feedback Control

Feedback compares the measured output with the reference and acts on the difference. This note derives the closed-loop transfer functions of a single loop with disturbances and sensor noise, defines the sensitivity and complementary sensitivity functions that express what feedback can and cannot do, computes steady-state errors from the system type and error constants, shows how feedback reduces sensitivity to plant variations, and designs lead and lag compensators that reshape the loop when a pure gain is not enough. The tools for checking stability are in [Stability Analysis](./stability_analysis.md) and [Frequency Response](./frequency_response.md).

## Problem Statement

Given a plant $G(s)$, a sensor $H(s)$, and the signals that act on the loop (a reference $r$, a disturbance $d$ at the plant input and sensor noise $n$, each with a known character such as a step, a ramp or a frequency band), choose a controller $C(s)$ such that:

1. the closed loop is internally stable;
2. the steady-state error to the specified reference and disturbance inputs is zero or below a bound;
3. disturbances in the low-frequency band are attenuated and noise in the high-frequency band is not amplified;
4. the transient response meets the specifications on damping and speed, which in the frequency domain are a phase margin and a crossover frequency;
5. these properties survive the expected variation of the plant parameters.

The plant is assumed LTI near its operating point; unless stated otherwise the sensor is ideal, $H = 1$, and the measurement is $y_m = y + n$.

## Closed-Loop Transfer Functions

With the controller acting on the error, $u = C(r - y_m)$, and the plant output $y = G(u + d)$, eliminating $u$ gives the output, the error $e = r - y$ and the control signal:

```math
Y = T\, R + GS\, D - T\, N
```

```math
E = S\, R - GS\, D + T\, N
```

```math
U = CS\,(R - N) - T\, D
```

where the loop transfer function, the sensitivity function and the complementary sensitivity function are

$$
L = CG,
\qquad S = \frac{1}{1 + L},
\qquad T = \frac{L}{1 + L}
$$

With a sensor $H \neq 1$ in the feedback path, $L = CGH$, the reference response is $Y/R = CG/(1 + CGH)$, and the output tracks $R/H$ at frequencies where the loop gain is high; the sensor calibration therefore sets the accuracy of the loop. All closed-loop transfer functions share the denominator $1 + L$, whose roots are the closed-loop poles.

## Sensitivity and Complementary Sensitivity

The two functions always add to one,

$$
S(s) + T(s) = 1
$$

and each describes a different job. $S$ is the transfer function from reference to error and, multiplied by $G$, from disturbance to output: it should be small where references and disturbances have their energy. $T$ is the transfer function from noise to output (with a minus sign) and from reference to output: it should be close to 1 where references must be tracked and small where noise lies. Because they add to one, both cannot be small at the same frequency. A loop is therefore designed with $\lvert L\rvert \gg 1$ (so $S \approx 1/L$ small) at low frequency and $\lvert L\rvert \ll 1$ (so $T \approx L$ small) at high frequency, with the crossover in between; the [frequency-response note](./frequency_response.md) plots both functions for a tank level loop.

### Sensitivity to Plant Variations

The name of $S$ comes from its second meaning. If the plant changes by $dG$, the relative change of the closed-loop transfer function $T = CG/(1 + CG)$ is

$$
\frac{dT/T}{dG/G} = \frac{G}{T} \frac{dT}{dG} = \frac{1}{1 + CG} = S
$$

A 10% change in the plant changes the closed-loop response by $`10\% \times \lvert S\rvert`$, so at frequencies where the loop gain is high the closed loop depends almost only on the controller and the sensor. For $G = 10/(s + 1)$ in unity feedback with $C = 1$, the DC sensitivity is $1/11$: a 10% rise of the plant gain changes the closed-loop DC gain by about 0.9% (exactly 0.83%, from $10/11$ to $11/12$). The sensitivity to the sensor is $-T$, close to $-1$: feedback cannot correct errors of its own measurement.

## Disturbance Rejection and Noise

### Example: Proportional Control and a Step Disturbance

For a plant $G(s) = 1/(s + 1)$ under proportional control $C = K$, a unit step disturbance $D(s) = 1/s$ at the plant input produces the output

$$
Y_d(s) = \frac{G}{1 + KG}D(s) = \frac{1}{s(s + 1 + K)},
\qquad y_d(\infty) = \lim_{s\to 0} sY_d(s) = \frac{1}{1 + K}
$$

The steady-state effect falls as $1/(1 + K)$ but never vanishes: $K = 99$ leaves 1% of it. Exercise 4 shows that integral action in the controller removes it entirely.

### Where the Integrator Must Be

For a step disturbance at the plant input, what matters is an integrator in the controller, not in the plant. For the pump-fed tank, whose level $h$ integrates the flow imbalance, a proportional controller $u = K_c(r - h)$ driving a pump of gain $k_q$ gives the disturbance-to-level transfer function

$$
\frac{H(s)}{Q_d(s)} = \frac{1/(As)}{1 + K_c k_q/(As)} = \frac{1}{As + K_c k_q}
$$

for an increase $q_d$ in the draw-off flow (entering with a minus sign). A step increase of $0.005$ m³/s with $K_c k_q = 0.5$ m²/s leaves a steady level error of $0.005/0.5 = 0.01$ m, although the plant contains an integrator: at steady state the pump must deliver the extra flow, which a proportional controller only does if an error persists. The integrator in the plant removes the steady-state error to reference steps, not to input disturbances.

### Noise and Control Effort

Noise reaches the output through $T$ and the actuator through $CS$. At high frequency $\lvert CS\rvert \approx \lvert C\rvert$, so a controller with large high-frequency gain (an unfiltered derivative, a lead network with small $\alpha$) passes the full sensor noise, multiplied by that gain, to the actuator. This wears valves and motors and can saturate them even when the output looks clean.

## Steady-State Error and System Type

For a unity-feedback loop, the final value theorem applied to $E = SR$ gives

$$
e_{ss} = \lim_{s\to 0} \frac{sR(s)}{1 + L(s)}
$$

provided the closed loop is stable. Writing $L(s) = K\prod(\tau_i s + 1)/[s^N\prod(\tau_j s + 1)]$, the number $N$ of free integrators in the loop is the system type. The error constants and the resulting errors are:

| Input | Error constant | Type 0 | Type 1 | Type 2 |
| --- | --- | --- | --- | --- |
| Step $R/s$ | Position $K_p = \lim_{s\to 0}L(s)$ | $R/(1 + K_p)$ | 0 | 0 |
| Ramp $R/s^2$ | Velocity $K_v = \lim_{s\to 0}sL(s)$ | $\infty$ | $R/K_v$ | 0 |
| Parabola $R/s^3$ | Acceleration $K_a = \lim_{s\to 0}s^2L(s)$ | $\infty$ | $\infty$ | $R/K_a$ |

Each integrator adds $-90^\circ$ of phase at all frequencies, so a higher type makes the loop harder to stabilize: a type-2 loop needs phase lead near crossover, and a type-3 loop is rarely used.

### Example: Ramp Error of a Type-1 Servo

For $L(s) = \frac{50}{s(s + 5)}$ tracking $r(t) = 3t$ (a ramp of 3 units per second), $K_v = \lim_{s\to 0} sL(s) = 50/5 = 10$ s⁻¹, so the output follows the ramp with a constant lag $e_{ss} = 3/K_v = 0.3$ units.

## Lead and Lag Compensation

When adjusting a gain cannot satisfy both the steady-state and the transient specifications, a compensator adds poles and zeros that reshape the loop.

### Lead Compensator

$$
C_{lead}(s) = K_c \frac{Ts + 1}{\alpha Ts + 1},
\qquad 0 < \alpha < 1
$$

The zero at $1/T$ comes before the pole at $1/(\alpha T)$, so the network adds positive phase between them, with a maximum

$$
\phi_{\max} = \arcsin \frac{1 - \alpha}{1 + \alpha}
\qquad \text{at}
\qquad \omega_m = \frac{1}{T\sqrt{\alpha}}
$$

where its gain is $K_c/\sqrt{\alpha}$. Its high-frequency gain is $K_c/\alpha$, so a small $\alpha$ amplifies noise; $\alpha \geq 0.05$ to 0.1 (a lead of at most $55^\circ$–$`65^\circ`$ per stage) is usual. The Bode design procedure is:

1. Choose $K_c$ to meet the steady-state error constant.
2. Find the phase margin of $K_c G$.
3. Set $\phi_{\max}$ to the missing phase plus 5–12° for the crossover shift.
4. Compute $\alpha = (1 - \sin\phi_{\max})/(1 + \sin\phi_{\max})$.
5. Place $\omega_m$ at the new crossover, the frequency where $\lvert K_c G\rvert = \sqrt{\alpha}$, and compute $T = 1/(\omega_m\sqrt{\alpha})$.
6. Check the margins and simulate the step response.

#### Example: Lead Design for a Servo

The plant is $G(s) = \frac{4}{s(s + 2)}$; the specification asks for $K_v \geq 20$ s⁻¹ and a phase margin of at least $45^\circ$.

1. $K_v = \lim_{s\to 0} s K_c G(s) = 2K_c$, so $K_c = 10$.
2. For $K_cG = 40/[s(s + 2)]$, $\omega\sqrt{\omega^2 + 4} = 40$ gives $\omega_{gc} = 6.17$ rad/s and $PM = 90^\circ - \arctan(6.17/2) = 18.0^\circ$.
3. $\phi_{\max} = 45^\circ - 18^\circ + 12^\circ = 39^\circ$.
4. $\alpha = (1 - \sin 39^\circ)/(1 + \sin 39^\circ) = 0.371/1.629 = 0.228$.
5. $40/(\omega\sqrt{\omega^2 + 4}) = \sqrt{0.228} = 0.477$ gives $\omega_m = 9.05$ rad/s, and $T = 1/(9.05 \times 0.477) = 0.232$ s.

The compensator is

```math
C(s) = 10\, \frac{0.232s + 1}{0.0527s + 1} = 44.0\, \frac{s + 4.31}{s + 19.0}
```

The compensated loop crosses over at 9.05 rad/s with a phase margin of $51.5^\circ$, meeting the specification while keeping $K_v = 20$ s⁻¹. The crossover has moved up from 6.2 to 9.1 rad/s, so the loop is also faster.

### Lag Compensator

$$
C_{lag}(s) = \frac{Ts + 1}{\beta Ts + 1},
\qquad \beta > 1
$$

has unit DC gain and a high-frequency gain $1/\beta$. Used together with a loop gain set for the steady-state requirement, it lowers the gain near crossover by the factor $\beta$ without adding much phase lag there, which is equivalent to raising the low-frequency gain by $\beta$ relative to the crossover. The procedure:

1. Set the loop gain $K$ to meet the error constant.
2. Find the frequency $\omega_{gc}'$ where the phase of $KG$ equals $-180^\circ + PM_{\mathrm{desired}} + 5^\circ$ (the $5^\circ$ allows for the lag that the network still adds there).
3. Choose $\beta = \lvert KG(j\omega_{gc}')\rvert$, so that the compensated loop crosses over at $\omega_{gc}'$.
4. Place the zero a decade below the new crossover, $1/T = \omega_{gc}'/10$, and the pole at $1/(\beta T)$.

Lag compensation improves steady-state accuracy and phase margin at the cost of a lower crossover frequency (a slower response) and a slow closed-loop pole near the lag zero, which leaves a long, small-amplitude tail in the step response.

### Lead-Lag and the Root Locus View

A lead-lag compensator $K_c(s + z_1)(s + z_2)/[(s + p_1)(s + p_2)]$ combines a lead section ($p_1 > z_1$) for speed and margin with a lag section ($z_2 > p_2$, both close to the origin) for accuracy. A PID controller is a lead-lag compensator with the lag pole at the origin and the lead pole at the derivative filter.

On the root locus a lead network is designed by the angle condition: to make the locus pass through a desired closed-loop pole $s_d$, the compensator must supply the angle missing from $\angle G(s_d) + \angle C(s_d) = -180^\circ$, and its zero and pole are placed so that $\angle(s_d + z) - \angle(s_d + p)$ equals that deficit. Adding a zero pulls the locus to the left (more stable); adding a pole pushes it to the right. A lag pair close to the origin changes the locus near the dominant poles very little while multiplying the error constant by $z/p$.

## Key Takeaways

- All closed-loop transfer functions follow from $L = CG$: $S = 1/(1+L)$ governs tracking errors, disturbances and sensitivity to the plant; $T = L/(1+L)$ governs tracking and noise; and $S + T = 1$.
- Feedback reduces the effect of plant variations by the factor $\lvert S\rvert$ but cannot correct sensor errors.
- The system type (integrators in $L$) sets the steady-state error to reference polynomials; a step disturbance at the plant input requires an integrator in the controller.
- Lead compensation adds phase at crossover (more margin, more speed, more noise); lag compensation adds low-frequency gain (more accuracy, lower crossover).

## Related Scripts

- [Bode and Nyquist Margins](../../../scripts/algorithms/control_bode_nyquist/): computes the Bode magnitude and phase with straight-line asymptotes, the gain, phase and delay margins, the Nyquist plot and its encirclements of $-1$, the sensitivity functions and the closed-loop step response of a tank level loop with and without a transport delay.
- [Root Locus and Routh–Hurwitz](../../../scripts/algorithms/control_root_locus/): computes the root locus of a third-order position servo by sweeping the gain, marks the asymptotes, breakaway point and damping-ratio design point, and checks that the gain where the locus crosses the imaginary axis equals the Routh–Hurwitz critical gain.
- [PID Tuning and Windup](../../../scripts/algorithms/control_pid_tuning/): tunes a PID controller for a first-order-plus-dead-time process with the Ziegler–Nichols and SIMC rules, compares the set-point and load responses and the stability margins, and shows integrator windup under actuator saturation with and without back-calculation.

## Exercises

**Exercise 1.** A unity-feedback system has $L(s) = \frac{20}{(s+2)(s+5)}$. Determine the system type, the position error constant and the steady-state errors for a unit step and a unit ramp.

<details>
<summary>Answer</summary>

There is no free integrator, so the system is type 0, with $K_p = \lim_{s \to 0} L(s) = 20/10 = 2$.

For a unit step, $e_{ss} = \frac{1}{1 + K_p} = \frac{1}{3} = 0.333$. For a unit ramp, $K_v = \lim_{s \to 0} sL(s) = 0$, so $e_{ss} = \infty$: the output falls further and further behind the ramp.

</details>

**Exercise 2.** A plant $G(s) = \frac{10}{s+1}$ is placed in a unity-feedback loop with $C = 1$. Use the sensitivity function to estimate the percentage change in the closed-loop DC gain when the plant gain rises by 10%, and compare the estimate with the exact change.

<details>
<summary>Answer</summary>

At DC, $S = \frac{1}{1 + G(0)} = \frac{1}{11} = 0.0909$, so a 10% change in $G$ gives about $`0.0909 \times 10\% = 0.91\%`$ change in $T$.

Exactly, $T(0) = 10/11 = 0.9091$ before and $11/12 = 0.9167$ after, a change of 0.83%. The difference arises because the sensitivity is a first-order (small-change) result. Without feedback the DC gain would change by the full 10%.

</details>

**Exercise 3.** A lead compensator $C(s) = \frac{Ts + 1}{\alpha T s + 1}$ has $\alpha = 0.1$ and $T = 0.5$ s. Find the maximum phase lead, the frequency at which it occurs and the compensator gain in dB at that frequency. What is the high-frequency gain, and why does it matter?

<details>
<summary>Answer</summary>

```math
\phi_{\max} = \arcsin \frac{1 - 0.1}{1 + 0.1} = \arcsin(0.818) = 54.9^\circ, \qquad \omega_m = \frac{1}{T\sqrt{\alpha}} = \frac{1}{0.5\sqrt{0.1}} = 6.32 \text{ rad/s}
```

At $\omega_m$ the gain is $1/\sqrt{\alpha} = 3.16$, i.e. 10 dB. At high frequency the gain tends to $1/\alpha = 10$ (20 dB), so sensor noise above the crossover reaches the actuator amplified tenfold, which is why $\alpha$ is seldom chosen below about 0.05–0.1.

</details>

**Exercise 4.** For the plant $G(s) = \frac{1}{s+1}$ with a unit step disturbance at the plant input, replace the proportional controller by a PI controller $C(s) = K + K_i/s$. Show that the steady-state output caused by the disturbance is zero, and state the conditions on $K$ and $K_i$ required for this result.

<details>
<summary>Answer</summary>

```math
\frac{Y_d(s)}{D(s)} = \frac{G}{1 + CG} = \frac{\frac{1}{s+1}}{1 + \frac{Ks + K_i}{s(s+1)}} = \frac{s}{s^2 + (1+K)s + K_i}
```

With $D(s) = 1/s$, the final value theorem gives

```math
y_{d,ss} = \lim_{s \to 0} s \cdot \frac{s}{s^2 + (1+K)s + K_i} \cdot \frac{1}{s} = 0
```

The integrator in the controller makes the loop gain infinite at DC, so a constant disturbance is fully rejected. The final value theorem applies only if the closed loop is stable, which for this second-order polynomial requires $1 + K > 0$ and $K_i > 0$.

</details>

**Exercise 5.** A lag network $C_{lag}(s) = \frac{Ts + 1}{\beta T s + 1}$ uses $\beta = 10$, with its zero placed one decade below the gain crossover frequency $\omega_{gc} = 0.5$ rad/s. Find $T$, the pole location, and the phase and magnitude that the network contributes at $\omega_{gc}$. Use the result to explain the extra $5^\circ$ in the lag design procedure.

<details>
<summary>Answer</summary>

The zero is at $\omega_{gc}/10 = 0.05$ rad/s, so $T = 20$ s, and the pole is at $1/(\beta T) = 0.005$ rad/s. At $\omega = 0.5$ rad/s:

```math
\angle C_{lag} = \arctan(0.5 \times 20) - \arctan(0.5 \times 200) = 84.29^\circ - 89.43^\circ = -5.1^\circ, \qquad \lvert C_{lag}\rvert = \frac{\sqrt{1 + 10^2}}{\sqrt{1 + 100^2}} = 0.1005
```

At crossover the network has already reduced the gain to almost exactly $1/\beta$, so the low-frequency loop gain is 10 times (20 dB) higher relative to the crossover, which multiplies the error constant by 10. It still costs about $5^\circ$ of phase at crossover, which is why the procedure targets a phase margin $5^\circ$ larger than required.

</details>

## References

- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
- G. F. Franklin, J. D. Powell, A. Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., Pearson, 2019.
- N. S. Nise, *Control Systems Engineering*, 8th ed., Wiley, 2019.
- K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, Princeton University Press, 2008.
- S. Skogestad, I. Postlethwaite, *Multivariable Feedback Control: Analysis and Design*, 2nd ed., Wiley, 2005.
