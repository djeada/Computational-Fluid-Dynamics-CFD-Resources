# Feedback Control

Feedback control uses measured output information to correct the control action and drive the system toward desired behavior. This note covers closed-loop performance analysis, steady-state error theory, sensitivity, disturbance rejection, and frequency-domain compensator design.

## Unity and Non-Unity Feedback Systems

### Unity Feedback

The sensor transfer function is $H(s) = 1$. The closed-loop transfer function is:

$$
T(s) = \frac{G(s)}{1 + G(s)}
$$

and the error transfer function is:

$$
E(s) = \frac{R(s)}{1 + G(s)}
$$

### Non-Unity Feedback

When $H(s) \neq 1$, the closed-loop transfer function becomes:

$$
T(s) = \frac{G(s)}{1 + G(s)H(s)}
$$

The error measured at the output differs from the error at the plant input. To analyze steady-state error, it is often convenient to convert to an equivalent unity-feedback form.

## Steady-State Error Analysis

The steady-state error for a unity-feedback system with open-loop transfer function $G(s)$ is:

$$
e_{ss} = \lim_{s \to 0} \frac{sR(s)}{1 + G(s)}
$$

### System Type

The **system type** is the number of free integrators in the open-loop transfer function:

$$
G(s) = \frac{K \prod(s + z_i)}{s^N \prod(s + p_j)}
$$

$N$ is the system type.

### Error Constants and Steady-State Errors

| Input | Error Constant | Formula | Type 0 | Type 1 | Type 2 |
| --- | --- | --- | --- | --- | --- |
| Step $R/s$ | Position $K_p$ | $\lim_{s\to 0} G(s)$ | $\frac{R}{1+K_p}$ | 0 | 0 |
| Ramp $R/s^2$ | Velocity $K_v$ | $\lim_{s\to 0} sG(s)$ | $\infty$ | $R/K_v$ | 0 |
| Parabola $R/s^3$ | Acceleration $K_a$ | $\lim_{s\to 0} s^2G(s)$ | $\infty$ | $\infty$ | $R/K_a$ |

**Key insight**: Increasing system type reduces steady-state error for polynomial inputs, but each added integrator reduces phase margin and makes stabilization harder.

## Sensitivity to Parameter Variations

A major advantage of feedback is reduced sensitivity to plant parameter changes. The **sensitivity function** of the closed-loop transfer function $T$ with respect to the plant $G$ is:

$$
S_G^T = \frac{\partial T / T}{\partial G / G} = \frac{1}{1 + G(s)H(s)}
$$

For large loop gain $|G(s)H(s)| \gg 1$:

$$
S_G^T \approx \frac{1}{G(s)H(s)} \approx 0
$$

This means that at frequencies where the loop gain is high, the closed-loop transfer function is **insensitive** to changes in the plant.

### Complementary Sensitivity

$$
T(s) + S(s) = 1
$$

where $T(s) = \frac{G(s)H(s)}{1 + G(s)H(s)}$ is the complementary sensitivity function. This constraint implies a fundamental trade-off: you cannot achieve both perfect tracking ($|T| = 1$) and perfect disturbance/noise rejection ($|S| = 0$) at the same frequency.

## Disturbance Rejection

For a system with disturbance $D(s)$ entering at the plant input:

$$
Y(s) = \frac{G(s)}{1 + G(s)C(s)} D(s) + \frac{G(s)C(s)}{1 + G(s)C(s)} R(s)
$$

The transfer function from disturbance to output is:

$$
\frac{Y(s)}{D(s)} = \frac{G(s)}{1 + G(s)C(s)} = G(s) S(s)
$$

High loop gain at the disturbance frequency makes $|S(j\omega)|$ small, thereby rejecting the disturbance. This is the fundamental mechanism of feedback control.

## Lead Compensator

A lead compensator adds phase lead near the gain crossover frequency to improve phase margin and transient response.

$$
C_{lead}(s) = K_c \frac{s + z}{s + p}, \quad p > z > 0
$$

or equivalently:

$$
C_{lead}(s) = K_c \frac{T s + 1}{\alpha T s + 1}, \quad 0 < \alpha < 1
$$

**Maximum phase lead**: $\phi_{max} = \sin^{-1}\frac{1 - \alpha}{1 + \alpha}$ at frequency $\omega_m = \frac{1}{T\sqrt{\alpha}}$

### Design Procedure (Bode Method)

1. Set the gain $K_c$ to meet the steady-state error requirement
2. Evaluate the uncompensated phase margin
3. Determine the required additional phase lead: $\phi_{max} = PM_{desired} - PM_{current} + \text{safety margin}$
4. Compute $\alpha = \frac{1 - \sin\phi_{max}}{1 + \sin\phi_{max}}$
5. Place $\omega_m$ at the new gain crossover frequency: $T = \frac{1}{\omega_m \sqrt{\alpha}}$
6. Verify gain and phase margins

## Lag Compensator

A lag compensator improves steady-state accuracy by boosting low-frequency gain without significantly affecting the phase margin.

$$
C_{lag}(s) = K_c \frac{s + z}{s + p}, \quad z > p > 0
$$

or equivalently:

$$
C_{lag}(s) = K_c \frac{T s + 1}{\beta T s + 1}, \quad \beta > 1
$$

### Design Procedure (Bode Method)

1. Set gain $K_c$ to meet transient response (phase margin) at the desired crossover frequency
2. Determine the low-frequency gain boost needed: $\beta = \frac{K_{required}}{K_c}$
3. Place the zero $z = 1/T$ at a frequency one decade below the gain crossover: $\omega_z = \omega_{gc}/10$
4. Place the pole at $p = z/\beta$
5. Verify that the phase margin is not degraded

## Lead-Lag Compensator

When both transient response improvement and steady-state accuracy are needed, a **lead-lag** compensator combines both:

$$
C(s) = K_c \frac{(s + z_1)(s + z_2)}{(s + p_1)(s + p_2)}
$$

where the lead section ($z_1, p_1$ with $p_1 > z_1$) improves phase margin and the lag section ($z_2, p_2$ with $z_2 > p_2$) boosts low-frequency gain.

## Root Locus Design

Compensators can also be designed using the root locus:

- **Adding a zero** (PD-like action) pulls the locus toward the left, improving stability
- **Adding a pole** (integral action) pushes the locus toward the right
- **Lead compensator**: Adds a pole-zero pair to reshape the locus so it passes through the desired closed-loop pole location
- **Lag compensator**: Adds a tightly spaced pole-zero pair near the origin to increase static gain without moving the dominant poles significantly

### Angle Condition for Compensator Design

The compensator zero and pole must contribute the correct angle at the desired pole location $s_d$:

$$
\angle C(s_d) = \angle(s_d + z) - \angle(s_d + p) = \theta_{required}
$$

where $\theta_{required} = 180^\circ - \angle G(s_d)H(s_d)$.

## Worked Examples

### Example 1: Steady-State Error Calculation

**Given**: Unity feedback system with $G(s) = \frac{50}{s(s+5)}$, input $r(t) = 3t$ (ramp).

**Find**: Steady-state error.

**Solution**:

System type = 1 (one free integrator).

Velocity error constant:

$$
K_v = \lim_{s \to 0} sG(s) = \lim_{s \to 0} \frac{50s}{s(s+5)} = \frac{50}{5} = 10
$$

Steady-state error for a ramp of magnitude 3:

$$
e_{ss} = \frac{3}{K_v} = \frac{3}{10} = 0.3
$$

### Example 2: Lead Compensator Design

**Given**: Plant $G(s) = \frac{4}{s(s+2)}$ in unity feedback. Desired phase margin $\geq 45^\circ$ with $K_v \geq 20\;\text{s}^{-1}$.

**Find**: Lead compensator parameters.

**Solution**:

**Step 1** — Set gain for steady-state requirement. Use the form $C(s) = K_c \frac{Ts+1}{\alpha Ts+1}$, whose DC gain is $K_c$:

$$
K_v = \lim_{s\to 0} s \cdot K_c \frac{Ts+1}{\alpha Ts+1} \cdot \frac{4}{s(s+2)} = 2K_c
$$

so $K_c = 10$ gives $K_v = 20\;\text{s}^{-1}$. (In the pole-zero form $K_c' \frac{s+z}{s+p}$ the DC gain is $K_c' z/p$, so the gain must be raised to $K_c' = K_c/\alpha$.)

**Step 2** — Evaluate uncompensated system $10 \cdot \frac{4}{s(s+2)} = \frac{40}{s(s+2)}$.

At the gain crossover $|G(j\omega)| = 1$: solving $\omega\sqrt{\omega^2 + 4} = 40$ gives $\omega_{gc} \approx 6.2$ rad/s, with $PM = 90^\circ - \arctan(6.17/2) \approx 18^\circ$.

**Step 3** — Required phase lead: $\phi_{max} = 45^\circ - 18^\circ + 12^\circ = 39^\circ$ (12° safety margin).

**Step 4** — Compute $\alpha$:

$$
\alpha = \frac{1 - \sin 39^\circ}{1 + \sin 39^\circ} = \frac{1 - 0.629}{1 + 0.629} = \frac{0.371}{1.629} \approx 0.228
$$

**Step 5** — Place maximum phase at the new crossover. The lead compensator adds a gain of $1/\sqrt{\alpha}$ at $\omega_m$, so the new crossover is where the uncompensated magnitude equals $\sqrt{\alpha}$: $\frac{40}{\omega_m\sqrt{\omega_m^2 + 4}} = \sqrt{0.228} = 0.477$, giving $\omega_m \approx 9.05$ rad/s. Then $T = \frac{1}{9.05\sqrt{0.228}} \approx 0.232$ s.

Zero: $z = 1/T \approx 4.3$, Pole: $p = 1/(\alpha T) \approx 19.0$.

$$
C(s) = 10 \cdot \frac{0.232s + 1}{0.0527s + 1} = 44.0 \cdot \frac{s + 4.3}{s + 19.0}
$$

Check: the compensated loop crosses over at about 9.05 rad/s with $PM \approx 51^\circ$, meeting the specification.

### Example 3: Disturbance Rejection

**Given**: Plant $G(s) = \frac{1}{s+1}$, controller $C(s) = K$, unity feedback. A step disturbance $D(s) = 1/s$ enters at the plant input.

**Find**: Steady-state output due to the disturbance.

**Solution**:

$$
Y_d(s) = \frac{G(s)}{1 + C(s)G(s)} D(s) = \frac{1/(s+1)}{1 + K/(s+1)} \cdot
\frac{1}{s} = \frac{1}{s(s + 1 + K)}
$$

By the final value theorem:

$$
y_{d,ss} = \lim_{s\to 0} s \cdot \frac{1}{s(s+1+K)} = \frac{1}{1+K}
$$

Increasing $K$ reduces the disturbance effect. For $K = 99$, $y_{d,ss} = 0.01$.

## Applications

- **Flight control**: Lead-lag compensators for pitch and roll autopilots
- **Disk drive servo**: Track-following with disturbance rejection from vibration
- **Temperature control**: Lag compensation for zero steady-state error in HVAC systems
- **Motion control**: Lead compensation for fast, well-damped positioning in CNC machines
- **Power electronics**: Feedback regulation of voltage converters under varying loads

## Practical Tips

- Increasing system type eliminates steady-state error but always **costs phase margin** — compensate accordingly
- Lead compensation improves speed and stability but amplifies high-frequency noise
- Lag compensation is low-risk but cannot improve transient response — it only improves steady-state accuracy
- Always verify the final design with a **time-domain simulation** (step response, ramp response) to confirm that the Bode-domain specifications translate correctly
- In practice, sensor dynamics and actuator saturation often limit achievable bandwidth more than the compensator design

## Exercises

**Exercise 1.** A unity-feedback system has $G(s) = \frac{20}{(s+2)(s+5)}$. Determine the system type, the position error constant $K_p$, and the steady-state errors for a unit step and a unit ramp input.

<details>
<summary>Answer</summary>

There is no free integrator, so the system is Type 0. The position error constant is $K_p = \lim_{s \to 0} G(s) = 20/10 = 2$.

- Unit step: $e_{ss} = \frac{1}{1 + K_p} = \frac{1}{3} \approx 0.333$.
- Unit ramp: $K_v = \lim_{s \to 0} sG(s) = 0$, so $e_{ss} = \infty$ (the output falls further and further behind the ramp).

</details>

**Exercise 2.** A plant $G(s) = \frac{10}{s+1}$ is placed in a unity-feedback loop. Use the sensitivity function to estimate the percentage change in the closed-loop DC gain when the plant gain rises by 10%, and compare the estimate with the exact change.

<details>
<summary>Answer</summary>

At DC the sensitivity is $S_G^T = \frac{1}{1 + G(0)} = \frac{1}{11} = 0.0909$, so a 10% change in $G$ gives roughly $0.0909 \times 10\% \approx 0.91\%$ change in $T$.

Exact: $T(0) = 10/11 = 0.9091$ before and $11/12 = 0.9167$ after, a change of $0.83\%$. The small difference arises because the sensitivity is a first-order (small-change) result. Without feedback the DC gain would change by the full 10%.

</details>

**Exercise 3.** A lead compensator $C(s) = \frac{Ts + 1}{\alpha T s + 1}$ has $\alpha = 0.1$ and $T = 0.5$ s. Find the maximum phase lead, the frequency at which it occurs, and the compensator gain in dB at that frequency. What is the high-frequency gain, and why does it matter?

<details>
<summary>Answer</summary>

```math
\phi_{max} = \sin^{-1} \frac{1 - 0.1}{1 + 0.1} = \sin^{-1}(0.818) = 54.9^\circ
```

```math
\omega_m = \frac{1}{T\sqrt{\alpha}} = \frac{1}{0.5\sqrt{0.1}} = 6.32 \text{ rad/s}
```

At $\omega_m$ the gain is $1/\sqrt{\alpha} = 3.16$, i.e. 10 dB. At high frequency the gain tends to $1/\alpha = 10$ (20 dB), so sensor noise above the crossover is amplified tenfold. This is why lead compensation is usually limited to $\alpha \gtrsim 0.05$–$0.1$.

</details>

**Exercise 4.** In Example 3 (plant $G(s) = \frac{1}{s+1}$ with a step disturbance at the plant input), replace the proportional controller by a PI controller $C(s) = K + K_i/s$. Show that the steady-state output caused by the disturbance is zero, and state the conditions on $K$ and $K_i$ required for this result.

<details>
<summary>Answer</summary>

```math
\frac{Y_d(s)}{D(s)} = \frac{G}{1 + CG} = \frac{\frac{1}{s+1}}{1 + \frac{Ks + K_i}{s(s+1)}} = \frac{s}{s^2 + (1+K)s + K_i}
```

With $D(s) = 1/s$, the final value theorem gives

```math
y_{d,ss} = \lim_{s \to 0} s \cdot \frac{s}{s^2 + (1+K)s + K_i} \cdot \frac{1}{s} = 0
```

The integrator in the controller makes the loop gain infinite at DC, so a constant disturbance is fully rejected. The final value theorem only applies if the closed loop is stable, which for this second-order polynomial requires $1 + K > 0$ and $K_i > 0$.

</details>

**Exercise 5.** A lag network $C_{lag}(s) = \frac{Ts + 1}{\beta T s + 1}$ uses $\beta = 10$, with its zero placed one decade below the gain crossover frequency $\omega_{gc} = 0.5$ rad/s. Find $T$, the pole location, and the phase and magnitude that the network contributes at $\omega_{gc}$. Use the result to explain the safety margin in the lag design procedure.

<details>
<summary>Answer</summary>

The zero is at $z = \omega_{gc}/10 = 0.05$ rad/s, so $T = 1/z = 20$ s. The pole is at $p = 1/(\beta T) = 0.005$ rad/s.

At $\omega = 0.5$ rad/s:

```math
\angle C_{lag} = \arctan(0.5 \times 20) - \arctan(0.5 \times 200) = 84.29^\circ -
89.43^\circ = -5.1^\circ
```

```math
|C_{lag}| = \frac{\sqrt{1 + 10^2}}{\sqrt{1 + 100^2}} = 0.1005 \approx 1/\beta
```

At crossover the network gain has already dropped to about $1/\beta$ of its DC value, so the low-frequency loop gain is $\beta = 10$ times (20 dB) larger relative to crossover, which improves the error constants. The network still costs about $5^\circ$ of phase at crossover, so the phase margin target in the design is increased by a few degrees to compensate.

</details>

## References

- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
- G. F. Franklin, J. D. Powell, A. Emami-Naeini, *Feedback Control of Dynamic Systems*, Pearson.
- N. S. Nise, *Control Systems Engineering*, 7th ed., Wiley, 2015.
- K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, Princeton University Press, 2008.
- S. Skogestad, I. Postlethwaite, *Multivariable Feedback Control: Analysis and Design*, 2nd ed., Wiley, 2005.
