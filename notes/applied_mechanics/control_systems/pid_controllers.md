# PID Controllers

The Proportional-Integral-Derivative (PID) controller is the most widely used control algorithm in industry, found in over 90% of industrial control loops. Its enduring popularity comes from a simple structure that handles a broad class of plants with intuitive tuning.

## PID Controller Form

The standard (parallel) PID controller is:

$$
u(t) = K_p e(t) + K_i \int_0^t e(\tau)\, d\tau + K_d \frac{de(t)}{dt}
$$

where $e(t) = r(t) - y(t)$ is the error signal.

In the Laplace domain:

$$
C(s) = K_p + \frac{K_i}{s} + K_d s
$$

### Alternative Forms

**Ideal (textbook) form**:

$$
C(s) = K_p \left(1 + \frac{1}{T_i s} + T_d s\right)
$$

where $T_i = K_p / K_i$ is the integral time and $T_d = K_d / K_p$ is the derivative time.

**Series (interacting) form** — common in industrial controllers:

$$
C(s) = K_c \frac{T_i s + 1}{T_i s} \cdot (T_d s + 1)
$$

## Effect of Each Term on Response

### Proportional Action ($K_p$)

- Provides a control signal proportional to the current error
- **Increasing $K_p$**: Reduces steady-state error, speeds up response, but increases overshoot
- Cannot eliminate steady-state error for step inputs to Type 0 systems
- Alone: $C(s) = K_p$

### Integral Action ($K_i$)

- Accumulates past error to drive steady-state error to zero
- **Increasing $K_i$**: Eliminates offset, but slows response and may cause oscillation
- Adds a pole at $s = 0$, increasing system type by one
- Can cause **integral windup** if the actuator saturates

### Derivative Action ($K_d$)

- Responds to the rate of change of error — provides anticipatory control
- **Increasing $K_d$**: Reduces overshoot and settling time, improves damping
- Amplifies high-frequency noise — never used without filtering in practice
- Adds a zero, improving phase margin near crossover

### Summary Table

| Parameter | Rise Time | Overshoot | Settling Time | Steady-State Error |
| --- | --- | --- | --- | --- |
| $K_p \uparrow$ | Decrease | Increase | Small change | Decrease |
| $K_i \uparrow$ | Decrease | Increase | Increase | Eliminate |
| $K_d \uparrow$ | Small change | Decrease | Decrease | No effect |

## Tuning Methods

### Ziegler-Nichols Ultimate Gain Method

**Procedure**:

1. Set $K_i = 0$, $K_d = 0$
2. Increase $K_p$ until the system oscillates with sustained constant-amplitude oscillations
3. Record the **ultimate gain** $K_u$ and the **ultimate period** $T_u$

**Tuning rules**:

| Controller | $K_p$ | $T_i$ | $T_d$ |
| --- | --- | --- | --- |
| P | $0.50\, K_u$ | — | — |
| PI | $0.45\, K_u$ | $T_u / 1.2$ | — |
| PID | $0.60\, K_u$ | $T_u / 2$ | $T_u / 8$ |

These rules give a quarter-decay ratio (overshoot decays by 75% each cycle), which is often too aggressive. A common modification is to use $K_p = 0.33\,K_u$ for less oscillatory response.

### Ziegler-Nichols Step Response Method

For a plant that can be approximated as a first-order-plus-dead-time (FOPDT) model:

$$
G(s) \approx \frac{K_p e^{-Ls}}{Ts + 1}
$$

where $L$ is the apparent dead time and $T$ is the time constant, both estimated from the open-loop step response.

| Controller | $K_p$ | $T_i$ | $T_d$ |
| --- | --- | --- | --- |
| P | $T/(K_p L)$ | — | — |
| PI | $0.9\,T/(K_p L)$ | $3.33\,L$ | — |
| PID | $1.2\,T/(K_p L)$ | $2\,L$ | $0.5\,L$ |

### Cohen-Coon Method

Also based on the FOPDT model but provides better tuning for processes with larger dead-time-to-time-constant ratios ($L/T > 0.25$). The PID gains are computed as $K_p = \frac{1}{K_p}\frac{T}{L}\left(\frac{4}{3} + \frac{L}{4T}\right)$, $T_i = L \cdot \frac{32 + 6L/T}{13 + 8L/T}$, and $T_d = L \cdot \frac{4}{11 + 2L/T}$.

### Relay Feedback Method (Åström-Hägglund)

An automated alternative to the Ziegler-Nichols ultimate gain method:

1. Replace the controller with an on/off relay of amplitude $d$
2. The system oscillates in a limit cycle with amplitude $a$ and period $T_u$
3. Estimate the ultimate gain: $K_u \approx \frac{4d}{\pi a}$
4. Apply standard tuning rules with $K_u$ and $T_u$

**Advantage**: No risk of instability during the test — the relay naturally limits oscillation amplitude.

## Anti-Windup Strategies

When the actuator saturates, the integrator continues to accumulate error, causing **integral windup** — large overshoot and slow recovery once the setpoint is reached.

### Clamping (Conditional Integration)

Stop integrating when the actuator is saturated:

$$
\text{If } |u| \geq u_{max}: \quad \text{freeze } \int e\, d\tau
$$

### Back-Calculation

Feed back the difference between the controller output and the actual (saturated) actuator output:

$$
\frac{d}{dt}\int e\, d\tau = e(t) + \frac{1}{T_t}\big(u_{sat} - u\big)
$$

where $T_t$ is the tracking time constant, typically $T_t = \sqrt{T_i T_d}$.

### Integrator Reset

Immediately reset the integrator when the error changes sign, preventing accumulated overshoot.

## Digital PID Implementation

In a sampled-data system with sampling period $T_s$, the continuous PID is discretized.

### Position Form

$$
u[k] = K_p\, e[k] + K_i T_s \sum_{j=0}^{k} e[j] + K_d \frac{e[k] - e[k-1]}{T_s}
$$

### Velocity (Incremental) Form

$$
\Delta u[k] = u[k] - u[k - 1] = K_p(e[k] - e[k - 1]) + K_i T_s\, e[k] + K_d
\frac{e[k] - 2e[k-1] + e[k-2]}{T_s}
$$

**Advantages of velocity form**: bumpless transfer between manual/automatic modes, inherent anti-windup, and direct output limiting.

### Sampling Rate Selection

Rule of thumb: $T_s \leq T_u / 10$ or equivalently the sampling frequency should be at least 10 times the closed-loop bandwidth.

## Practical Considerations

### Derivative Filtering

Pure derivative amplifies noise. A practical derivative term includes a low-pass filter:

$$
D(s) = \frac{K_d s}{1 + (T_d / N) s}
$$

where $T_d = K_d / K_p$ and $N$ is the filter coefficient, typically $N = 8$ to $20$. This limits the derivative gain at high frequencies to $N \cdot K_p$.

### Setpoint Weighting

To reduce overshoot from setpoint changes while maintaining disturbance rejection:

$$
u(t) = K_p(b\, r - y) + K_i \int(r - y)\, d\tau + K_d \frac{d(c\, r - y)}{dt}
$$

where $b \in [0,1]$ and $c \in [0,1]$ are weighting factors. Setting $b < 1$ reduces proportional kick; setting $c = 0$ avoids derivative kick.

### Actuator Saturation

Always implement output limiting:

$$
u_{applied} = \text{clamp}(u, u_{min}, u_{max})
$$

and couple it with anti-windup to prevent integrator accumulation during saturation.

## Worked Examples

### Example 1: Temperature Control

**Given**: A thermal process modeled as FOPDT: $G(s) = \frac{2\, e^{-3s}}{10s + 1}$ (gain = 2 °C/%, dead time $L = 3$ s, time constant $T = 10$ s).

**Find**: PID parameters using Ziegler-Nichols step response method.

**Solution**:

Using $K_p = 2$, $L = 3$, $T = 10$:

$$
K_p = \frac{1.2\, T}{K_p L} = \frac{1.2 \times 10}{2 \times 3} = 2.0
$$

$$
T_i = 2L = 6\; \text{s}
$$

$$
T_d = 0.5L = 1.5\; \text{s}
$$

Converting to parallel form:

$$
K_i = \frac{K_p}{T_i} = \frac{2.0}{6} = 0.333\; \text{s}^{-1}
$$

$$
K_d = K_p \cdot T_d = 2.0 \times 1.5 = 3.0\; \text{s}
$$

The controller is: $C(s) = 2.0 + \frac{0.333}{s} + 3.0s$.

### Example 2: Position Control with Anti-Windup

**Given**: A motor position control with plant $G(s) = \frac{10}{s(s+5)}$, actuator limited to $\pm 12$ V. Using PID with $K_p = 5$, $K_i = 2$, $K_d = 1$.

**Find**: Describe the back-calculation anti-windup implementation.

**Solution**:

Tracking time constant: $T_t = \sqrt{T_i T_d} = \sqrt{(K_p/K_i)(K_d/K_p)} = \sqrt{2.5 \times 0.2} = 0.707$ s.

Digital implementation at $T_s = 0.01$ s:

$$
u_{raw}[k] = K_p\, e[k] + I[k] + K_d \frac{e[k] - e[k-1]}{T_s}
$$

$$
u_{sat}[k] = \text{clamp}(u_{raw}[k],\, - 12,\, 12)
$$

$$
I[k + 1] = I[k] + K_i T_s\, e[k] + \frac{T_s}{T_t}(u_{sat}[k] - u_{raw}[k])
$$

The back-calculation term $\frac{T_s}{T_t}(u_{sat} - u_{raw})$ prevents the integrator from growing when the output is clamped, ensuring fast recovery from saturation.

### Example 3: Relay Tuning

**Given**: A process is tested with a relay of amplitude $d = 1$. The resulting limit cycle has amplitude $a = 0.5$ and period $T_u = 4$ s.

**Find**: PID parameters using Ziegler-Nichols rules.

**Solution**:

Ultimate gain: $K_u = \frac{4d}{\pi a} = \frac{4 \times 1}{\pi \times 0.5} = \frac{4}{1.571} \approx 2.55$

Apply Ziegler-Nichols PID rules:

$$
K_p = 0.6\, K_u = 0.6 \times 2.55 = 1.53
$$

$$
T_i = T_u / 2 = 2.0\; \text{s} \implies K_i = K_p / T_i = 0.765\; \text{s}^{-1}
$$

$$
T_d = T_u / 8 = 0.5\; \text{s} \implies K_d = K_p \cdot T_d = 0.765\; \text{s}
$$

## Applications

- **Process industry**: Temperature, pressure, flow, and level control in refineries
- **Motion control**: Servo drives for robotics, CNC machines, and 3D printers
- **Automotive**: Cruise control, idle speed control, electronic throttle
- **Aerospace**: Inner-loop rate controllers in autopilot systems

## Practical Tips

- **Start with PI** — derivative action is often unnecessary and introduces noise sensitivity
- Always implement **derivative filtering** ($N = 10$ is a safe default)
- Use **setpoint weighting** ($b = 0.5$, $c = 0$) to reduce overshoot on setpoint changes
- Ziegler-Nichols rules give an **aggressive starting point** — expect to de-tune for less overshoot
- Anti-windup is **essential** in any system with actuator limits
- For oscillatory loops, check for **mechanical backlash or stiction** before increasing gains

## Exercises

**Exercise 1.** A parallel PID controller has $K_p = 4$, $K_i = 2\;\text{s}^{-1}$ and $K_d = 0.5$ s. Convert it to the ideal form $K_p(1 + \frac{1}{T_i s} + T_d s)$. If the closed-loop response overshoots too much, which gain changes does the summary table suggest?

<details>
<summary>Answer</summary>

$T_i = K_p/K_i = 4/2 = 2$ s and $T_d = K_d/K_p = 0.5/4 = 0.125$ s.

To reduce overshoot: increase $K_d$ (more damping), or reduce $K_i$ and/or $K_p$. Reducing $K_i$ slows the removal of steady-state error; reducing $K_p$ slows the response.

</details>

**Exercise 2.** An ultimate-gain test gives $K_u = 8$ and $T_u = 2.5$ s. Find the Ziegler-Nichols PI and PID settings in both ideal ($T_i$, $T_d$) and parallel ($K_i$, $K_d$) form.

<details>
<summary>Answer</summary>

PI: $K_p = 0.45 \times 8 = 3.6$, $T_i = T_u/1.2 = 2.08$ s, so $K_i = K_p/T_i = 1.73\;\text{s}^{-1}$.

PID: $K_p = 0.6 \times 8 = 4.8$, $T_i = T_u/2 = 1.25$ s, $T_d = T_u/8 = 0.3125$ s, so $K_i = 4.8/1.25 = 3.84\;\text{s}^{-1}$ and $K_d = 4.8 \times 0.3125 = 1.5$ s.

</details>

**Exercise 3.** Apply the Cohen-Coon PID rules to the thermal process of Example 1 (process gain $K = 2$, $L = 3$ s, $T = 10$ s) and compare with the Ziegler-Nichols result from that example.

<details>
<summary>Answer</summary>

With $L/T = 0.3$:

$$
K_c = \frac{1}{K} \frac{T}{L}\left(\frac{4}{3} + \frac{L}{4T}\right) = \frac{1}{2}
\times 3.333 \times (1.333 + 0.075) = 2.35
$$

$$
T_i = L \frac{32 + 6L/T}{13 + 8L/T} = 3 \times \frac{33.8}{15.4} = 6.58 \text{ s}, \quad
T_d = L \frac{4}{11 + 2L/T} = \frac{12}{11.6} = 1.03 \text{ s}
$$

Ziegler-Nichols gave $K_p = 2.0$, $T_i = 6$ s, $T_d = 1.5$ s. Because $L/T = 0.3 > 0.25$, Cohen-Coon is the more appropriate rule here. It gives about 17% more gain, similar integral time, and less derivative action. Both are starting points to be refined by simulation.

</details>

**Exercise 4.** A filtered derivative term $D(s) = \frac{K_d s}{1 + (T_d/N)s}$ is used with $K_p = 2$, $T_d = 0.5$ s and $N = 10$. Find $K_d$, the filter corner frequency, and $|D(j\omega)|$ at $\omega = 1$ rad/s and $\omega = 200$ rad/s. Compare with an ideal derivative $K_d s$.

<details>
<summary>Answer</summary>

$K_d = K_p T_d = 1$ s. The filter time constant is $T_d/N = 0.05$ s, so the corner frequency is 20 rad/s.

$$
|D(j1)| = \frac{1}{\sqrt{1 + 0.05^2}} = 0.999 \quad (\text{ideal: } 1.0)
$$

$$
|D(j200)| = \frac{200}{\sqrt{1 + 10^2}} = 19.9 \quad (\text{ideal: } 200)
$$

Well below the corner the filter acts as a true derivative. At high frequency its gain levels off at $K_d N/T_d = N K_p = 20$, instead of growing without bound and amplifying noise.

</details>

**Exercise 5.** A velocity-form PID with $K_p = 2$, $K_i = 0.5\;\text{s}^{-1}$, $K_d = 0.1$ s and $T_s = 0.1$ s has error samples $e[k-2] = 1.0$, $e[k-1] = 0.8$ and $e[k] = 0.5$. Compute $\Delta u[k]$. Explain why the velocity form has built-in protection against integral windup when the actuator saturates.

<details>
<summary>Answer</summary>

$$
\Delta u[k] = 2(0.5 - 0.8) + 0.5 \times 0.1 \times 0.5 + 0.1\,
\frac{0.5 - 1.6 + 1.0}{0.1} = -0.6 + 0.025 - 0.1 = -0.675
$$

The controller outputs an increment that is added to the previous applied value. If $u[k-1]$ is the saturated actuator value, no integral state keeps growing beyond the limit. As soon as the error changes sign, the increments move the output back off the limit, so there is no stored windup to unwind.

</details>

## References

- K. J. Åström, T. Hägglund, *Advanced PID Control*, ISA, 2006.
- J. G. Ziegler, N. B. Nichols, "Optimum settings for automatic controllers", *Transactions of the ASME* 64, 759–768, 1942.
- G. H. Cohen, G. A. Coon, "Theoretical consideration of retarded control", *Transactions of the ASME* 75, 1953.
- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
