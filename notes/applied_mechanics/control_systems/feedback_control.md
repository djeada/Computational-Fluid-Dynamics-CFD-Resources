# Feedback Control

Feedback control uses measured output information to correct the control action and drive the system toward desired behavior. This note covers closed-loop performance analysis, steady-state error theory, sensitivity, disturbance rejection, and frequency-domain compensator design.

## Unity and Non-Unity Feedback Systems

### Unity Feedback

The sensor transfer function is $H(s) = 1$. The closed-loop transfer function is:

$$T(s) = \frac{G(s)}{1 + G(s)}$$

and the error transfer function is:

$$E(s) = \frac{R(s)}{1 + G(s)}$$

### Non-Unity Feedback

When $H(s) \neq 1$, the closed-loop transfer function becomes:

$$T(s) = \frac{G(s)}{1 + G(s)H(s)}$$

The error measured at the output differs from the error at the plant input. To analyze steady-state error, it is often convenient to convert to an equivalent unity-feedback form.

## Steady-State Error Analysis

The steady-state error for a unity-feedback system with open-loop transfer function $G(s)$ is:

$$e_{ss} = \lim_{s \to 0} \frac{sR(s)}{1 + G(s)}$$

### System Type

The **system type** is the number of free integrators in the open-loop transfer function:

$$G(s) = \frac{K \prod(s + z_i)}{s^N \prod(s + p_j)}$$

$N$ is the system type.

### Error Constants and Steady-State Errors

| Input | Error Constant | Formula | Type 0 | Type 1 | Type 2 |
|---|---|---|---|---|---|
| Step $R/s$ | Position $K_p$ | $\lim_{s\to 0} G(s)$ | $\frac{R}{1+K_p}$ | 0 | 0 |
| Ramp $R/s^2$ | Velocity $K_v$ | $\lim_{s\to 0} sG(s)$ | $\infty$ | $R/K_v$ | 0 |
| Parabola $R/s^3$ | Acceleration $K_a$ | $\lim_{s\to 0} s^2G(s)$ | $\infty$ | $\infty$ | $R/K_a$ |

**Key insight**: Increasing system type reduces steady-state error for polynomial inputs, but each added integrator reduces phase margin and makes stabilization harder.

## Sensitivity to Parameter Variations

A major advantage of feedback is reduced sensitivity to plant parameter changes. The **sensitivity function** of the closed-loop transfer function $T$ with respect to the plant $G$ is:

$$S_G^T = \frac{\partial T / T}{\partial G / G} = \frac{1}{1 + G(s)H(s)}$$

For large loop gain $|G(s)H(s)| \gg 1$:

$$S_G^T \approx \frac{1}{G(s)H(s)} \approx 0$$

This means that at frequencies where the loop gain is high, the closed-loop transfer function is **insensitive** to changes in the plant.

### Complementary Sensitivity

$$T(s) + S(s) = 1$$

where $T(s) = \frac{G(s)H(s)}{1 + G(s)H(s)}$ is the complementary sensitivity function. This constraint implies a fundamental trade-off: you cannot achieve both perfect tracking ($|T| = 1$) and perfect disturbance/noise rejection ($|S| = 0$) at the same frequency.

## Disturbance Rejection

For a system with disturbance $D(s)$ entering at the plant input:

$$Y(s) = \frac{G(s)}{1 + G(s)C(s)} D(s) + \frac{G(s)C(s)}{1 + G(s)C(s)} R(s)$$

The transfer function from disturbance to output is:

$$\frac{Y(s)}{D(s)} = \frac{G(s)}{1 + G(s)C(s)} = G(s) S(s)$$

High loop gain at the disturbance frequency makes $|S(j\omega)|$ small, thereby rejecting the disturbance. This is the fundamental mechanism of feedback control.

## Lead Compensator

A lead compensator adds phase lead near the gain crossover frequency to improve phase margin and transient response.

$$C_{lead}(s) = K_c \frac{s + z}{s + p}, \quad p > z > 0$$

or equivalently:

$$C_{lead}(s) = K_c \frac{T s + 1}{\alpha T s + 1}, \quad 0 < \alpha < 1$$

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

$$C_{lag}(s) = K_c \frac{s + z}{s + p}, \quad z > p > 0$$

or equivalently:

$$C_{lag}(s) = K_c \frac{T s + 1}{\beta T s + 1}, \quad \beta > 1$$

### Design Procedure (Bode Method)

1. Set gain $K_c$ to meet transient response (phase margin) at the desired crossover frequency
2. Determine the low-frequency gain boost needed: $\beta = \frac{K_{required}}{K_c}$
3. Place the zero $z = 1/T$ at a frequency one decade below the gain crossover: $\omega_z = \omega_{gc}/10$
4. Place the pole at $p = z/\beta$
5. Verify that the phase margin is not degraded

## Lead-Lag Compensator

When both transient response improvement and steady-state accuracy are needed, a **lead-lag** compensator combines both:

$$C(s) = K_c \frac{(s + z_1)(s + z_2)}{(s + p_1)(s + p_2)}$$

where the lead section ($z_1, p_1$ with $p_1 > z_1$) improves phase margin and the lag section ($z_2, p_2$ with $z_2 > p_2$) boosts low-frequency gain.

## Root Locus Design

Compensators can also be designed using the root locus:

- **Adding a zero** (PD-like action) pulls the locus toward the left, improving stability
- **Adding a pole** (integral action) pushes the locus toward the right
- **Lead compensator**: Adds a pole-zero pair to reshape the locus so it passes through the desired closed-loop pole location
- **Lag compensator**: Adds a tightly spaced pole-zero pair near the origin to increase static gain without moving the dominant poles significantly

### Angle Condition for Compensator Design

The compensator zero and pole must contribute the correct angle at the desired pole location $s_d$:

$$\angle C(s_d) = \angle(s_d + z) - \angle(s_d + p) = \theta_{required}$$

where $\theta_{required} = 180° - \angle G(s_d)H(s_d)$.

## Worked Examples

### Example 1: Steady-State Error Calculation

**Given**: Unity feedback system with $G(s) = \frac{50}{s(s+5)}$, input $r(t) = 3t$ (ramp).

**Find**: Steady-state error.

**Solution**:

System type = 1 (one free integrator).

Velocity error constant:

$$K_v = \lim_{s \to 0} sG(s) = \lim_{s \to 0} \frac{50s}{s(s+5)} = \frac{50}{5} = 10$$

Steady-state error for a ramp of magnitude 3:

$$e_{ss} = \frac{3}{K_v} = \frac{3}{10} = 0.3$$

### Example 2: Lead Compensator Design

**Given**: Plant $G(s) = \frac{4}{s(s+2)}$ in unity feedback. Desired phase margin $\geq 45°$ with $K_v \geq 20\;\text{s}^{-1}$.

**Find**: Lead compensator parameters.

**Solution**:

**Step 1** — Set gain for steady-state requirement:

$$K_v = \lim_{s\to 0} s \cdot K_c \cdot \frac{s+z}{s+p} \cdot \frac{4}{s(s+2)} = K_c \cdot \frac{z}{p} \cdot \frac{4}{2} = 2K_c\frac{z}{p}$$

Since lead has $z/p < 1$, we need $K_c$ large enough. Setting $K_c = 10$ initially gives $K_v = 20(z/p)$.

**Step 2** — Evaluate uncompensated system $10 \cdot \frac{4}{s(s+2)} = \frac{40}{s(s+2)}$.

At the gain crossover $|G(j\omega)| = 1$: solving numerically gives $\omega_{gc} \approx 5.8$ rad/s, with $PM \approx 18°$.

**Step 3** — Required phase lead: $\phi_{max} = 45° - 18° + 12° = 39°$ (12° safety margin).

**Step 4** — Compute $\alpha$:

$$\alpha = \frac{1 - \sin 39°}{1 + \sin 39°} = \frac{1 - 0.629}{1 + 0.629} = \frac{0.371}{1.629} \approx 0.228$$

**Step 5** — Place maximum phase at the new crossover. The lead compensator magnitude at $\omega_m$ is $1/\sqrt{\alpha}$, so the new crossover satisfies $|\frac{40}{\omega_m^2}| \cdot \frac{1}{\sqrt{0.228}} = 1$, giving $\omega_m \approx 8.6$ rad/s. Then $T = \frac{1}{8.6\sqrt{0.228}} \approx 0.244$ s.

Zero: $z = 1/T \approx 4.1$, Pole: $p = 1/(\alpha T) \approx 18.0$.

$$C(s) = 10 \cdot \frac{s + 4.1}{s + 18.0}$$

### Example 3: Disturbance Rejection

**Given**: Plant $G(s) = \frac{1}{s+1}$, controller $C(s) = K$, unity feedback. A step disturbance $D(s) = 1/s$ enters at the plant input.

**Find**: Steady-state output due to the disturbance.

**Solution**:

$$Y_d(s) = \frac{G(s)}{1 + C(s)G(s)} D(s) = \frac{1/(s+1)}{1 + K/(s+1)} \cdot \frac{1}{s} = \frac{1}{s(s + 1 + K)}$$

By the final value theorem:

$$y_{d,ss} = \lim_{s\to 0} s \cdot \frac{1}{s(s+1+K)} = \frac{1}{1+K}$$

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
