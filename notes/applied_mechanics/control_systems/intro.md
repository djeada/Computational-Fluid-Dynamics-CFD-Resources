# Introduction to Control Theory

Control theory is the mathematical framework for analyzing and designing systems that maintain desired behavior in the presence of disturbances and uncertainties. In applied mechanics, control systems are essential for stabilizing structures, guiding vehicles, regulating machines, and automating processes across all engineering disciplines.

## What is a Control System?

A **control system** is an interconnected set of components that manages, commands, directs, or regulates the behavior of other systems. Control systems are designed to:

- **Regulate**: Maintain system output at a desired value
- **Track**: Follow a time-varying reference signal
- **Stabilize**: Ensure system remains stable under disturbances
- **Optimize**: Achieve best performance within constraints

### Basic Control System Components

1. **Plant**: The system being controlled
2. **Sensor**: Measures system output
3. **Controller**: Processes error and generates control signal
4. **Actuator**: Applies control action to the plant
5. **Reference**: Desired system behavior

## Open-Loop vs. Closed-Loop Control

### Open-Loop Control

- **No feedback**: Controller doesn't use output information
- **Simple**: Easy to design and implement
- **Limitations**: No correction for disturbances or model errors

**Example**: Microwave oven timer (time-based, no temperature feedback)

### Closed-Loop Control (Feedback Control)

- **Uses feedback**: Controller uses output measurement
- **Self-correcting**: Automatically compensates for disturbances
- **Complex**: Requires stability analysis and tuning

**Example**: Thermostat (temperature feedback controls heating/cooling)

### Mathematical Representation

**Open-loop transfer function**:

$$
Y(s) = G(s)U(s)
$$

**Closed-loop transfer function**:

$$
\frac{Y(s)}{R(s)} = \frac{G(s)}{1 + G(s)H(s)}
$$

where:

- $G(s)$ = plant transfer function
- $H(s)$ = sensor transfer function
- $R(s)$ = reference input
- $Y(s)$ = system output
- $U(s)$ = control signal

## System Modeling

### Transfer Functions

For linear time-invariant (LTI) systems, the transfer function relates output to input in the Laplace domain:

$$
G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + b_{m-1} s^{m-1} + ... + b_1 s + b_0}{a_n s^n + a_{n-1} s^{n-1} + ... + a_1 s + a_0}
$$

### State-Space Representation

For systems with multiple inputs/outputs:

$$
\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}
$$

$$
\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}
$$

where:

- $\mathbf{x}$ = state vector
- $\mathbf{u}$ = input vector
- $\mathbf{y}$ = output vector
- $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ = system matrices

### Example 1: Mass-Spring-Damper System

A mass $m$ connected to a spring (stiffness $k$) and damper (coefficient $c$):

**Equation of motion**:

$$
m\ddot{x} + c\dot{x} + kx = F
$$

**Transfer function**:

$$
G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + cs + k}
$$

**State-space form**:
Let $x_1 = x$, $x_2 = \dot{x}$:

$$
\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -k/m & -c/m \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \begin{bmatrix} 0 \\ 1/m \end{bmatrix} F
$$

$$
y = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
$$

## System Response Analysis

### Time Domain Analysis

#### Step Response

Response to unit step input reveals:

- **Rise time**: Time to reach 90% of final value
- **Settling time**: Time to stay within 2% of final value
- **Overshoot**: Maximum percentage overshoot
- **Steady-state error**: Final tracking error

#### Impulse Response

Response to Dirac delta function:

$$
g(t) = \mathcal{L}^{-1}\{ G(s)\}
$$

For second-order systems:

$$
G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}
$$

**Step response**:

- **Underdamped** ($\zeta < 1$): Oscillatory response
- **Critically damped** ($\zeta = 1$): Fastest response without overshoot
- **Overdamped** ($\zeta > 1$): Slow, non-oscillatory response

### Frequency Domain Analysis

#### Bode Plots

Magnitude and phase plots vs. frequency:

- **Magnitude**: $|G(j\omega)|$ in dB
- **Phase**: $\angle G(j\omega)$ in degrees

**Benefits**:

- Easy to sketch by hand
- Clear indication of stability margins
- Straightforward controller design

#### Nyquist Plot

Complex plane plot of $G(j\omega)$ as $\omega$ varies from 0 to $\infty$.

**Nyquist Stability Criterion**: System is stable if Nyquist plot encircles -1 point $P$ times counterclockwise, where $P$ = number of open-loop RHP poles.

## Stability Analysis

### Routh-Hurwitz Criterion

For characteristic equation $a_n s^n + a_{n-1} s^{n-1} + ... + a_1 s + a_0 = 0$:

System is stable if all coefficients are positive and all elements in first column of Routh array are positive.

**Routh array construction**:

$$
\begin{array}{c|cccc}
s^n & a_n & a_{n-2} & a_{n-4} & ... \\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} & ... \\
s^{n-2} & b_1 & b_2 & b_3 & ... \\
s^{n-3} & c_1 & c_2 & c_3 & ... \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{array}
$$

where $b_1 = \frac{a_{n-1}a_{n-2} - a_n a_{n-3}}{a_{n-1}}$

### Root Locus Method

Graphical method showing how closed-loop poles move as controller gain varies.

**Rules for sketching**:

1. Number of branches = number of open-loop poles
2. Branches start at open-loop poles, end at zeros or infinity
3. Real axis segments between odd number of poles/zeros
4. Asymptotes for large gains

### Gain and Phase Margins

**Gain margin**: Additional gain before instability

$$
GM = \frac{1}{|G(j\omega_{pc})|} \text{ where } \angle G(j\omega_{pc}) = -180^\circ
$$

**Phase margin**: Additional phase lag before instability

$$
PM = 180^\circ + \angle G(j\omega_{gc}) \text{ where } |G(j\omega_{gc})| = 1
$$

**Design guidelines**:

- GM > 6 dB (factor of 2)
- PM > 45°

### Example 2: Stability Analysis

For unity feedback system with $G(s) = \frac{K}{s(s+2)(s+5)}$:

**Characteristic equation**: $s^3 + 7s^2 + 10s + K = 0$

**Routh array**:

$$
\begin{array}{c|cc}
s^3 & 1 & 10 \\
s^2 & 7 & K \\
s^1 & \frac{70-K}{7} & 0 \\
s^0 & K &
\end{array}
$$

**Stability condition**: $0 < K < 70$

## Control System Design

### Performance Specifications

#### Time Domain Specs

- **Settling time**: $t_s \leq t_{s,spec}$
- **Overshoot**: $M_p \leq M_{p,spec}$
- **Steady-state error**: $e_{ss} \leq e_{ss,spec}$

#### Frequency Domain Specs

- **Bandwidth**: Frequency range of good tracking
- **Disturbance rejection**: Attenuation of low-frequency disturbances
- **Noise rejection**: Attenuation of high-frequency noise

### Controller Types

#### Proportional (P) Control

$$
u(t) = K_p e(t)
$$

$$
C(s) = K_p
$$

**Effects**:

- Reduces steady-state error
- May cause instability for high gains
- No improvement in transient response

#### Proportional-Integral (PI) Control

$$
u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau
$$

$$
C(s) = K_p + \frac{K_i}{s}
$$

**Effects**:

- Eliminates steady-state error for step inputs
- Slower response due to integral action
- Reduces stability margins

#### Proportional-Integral-Derivative (PID) Control

$$
u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}
$$

$$
C(s) = K_p + \frac{K_i}{s} + K_d s
$$

**Effects**:

- Derivative action improves transient response
- Amplifies high-frequency noise
- Most common industrial controller

### Controller Tuning Methods

#### Ziegler-Nichols Method

**Step 1**: Find ultimate gain $K_u$ and period $T_u$ at stability limit

**Step 2**: Apply tuning rules:

- P control: $K_p = 0.5 K_u$
- PI control: $K_p = 0.45 K_u$, $K_i = 0.54 K_u / T_u$
- PID control: $K_p = 0.6 K_u$, $K_i = 1.2 K_u / T_u$, $K_d = 0.075 K_u T_u$

#### Cohen-Coon Method

Based on process reaction curve from step test.

#### Model-Based Methods

- **Pole placement**: Place closed-loop poles at desired locations
- **LQR (Linear Quadratic Regulator)**: Optimize quadratic cost function
- **H∞ control**: Robust control design

### Example 3: PID Controller Design

Design PID controller for plant $G(s) = \frac{1}{s(s+1)(s+2)}$ with specifications:

- Settling time < 4 seconds
- Overshoot < 20%
- Zero steady-state error for step input

**Solution**:

**Step 1**: Determine desired closed-loop pole locations
For 2nd-order dominant behavior: overshoot below 20% requires $\zeta > 0.46$, and $t_s \approx 4/(\zeta\omega_n) < 4$ s requires $\zeta\omega_n > 1$ rad/s (for example $\zeta = 0.5$, $\omega_n \geq 2.5$ rad/s).

**Step 2**: Design controller
The closed-loop characteristic polynomial is $s^4 + 3s^3 + (2 + K_d)s^2 + K_p s + K_i$. Its $s^3$ coefficient is fixed at 3, so the gains cannot place all four poles freely. A numerical search over the gains (checking stability and simulating the step response) gives, for example:
$K_p = 4$, $K_i = 0.25$, $K_d = 10$

The dominant poles are $s \approx -1.32 \pm 3.05j$; the two slow real poles ($s \approx -0.27$ and $s \approx -0.08$) lie close to the controller zeros, so they add only a small, slow tail.

**Step 3**: Verify performance
The simulated step response has about 16% overshoot and a 2% settling time of about 2.8 s, meeting both specifications.

## Advanced Control Topics

### State Feedback Control

$$
\mathbf{u} = -\mathbf{K}\mathbf{x} + \mathbf{N}r
$$

**Pole placement**: Choose $\mathbf{K}$ to place poles at desired locations
**LQR**: Minimize cost function $J = \int_0^\infty (\mathbf{x}^T\mathbf{Q}\mathbf{x} + \mathbf{u}^T\mathbf{R}\mathbf{u}) dt$

### Observer Design

Estimate unmeasured states:

$$
\dot{\hat{\mathbf{x}}} = \mathbf{A}\hat{\mathbf{x}} + \mathbf{B}\mathbf{u} +
\mathbf{L}(\mathbf{y} - \mathbf{C}\hat{\mathbf{x}})
$$

**Separation principle**: Controller and observer can be designed independently

### Robust Control

Design controllers that maintain performance despite:

- Model uncertainties
- Parameter variations
- External disturbances

**Methods**: H∞ control, μ-synthesis, sliding mode control

### Adaptive Control

Controllers that adjust parameters online:

- **Model Reference Adaptive Control (MRAC)**
- **Self-Tuning Regulators**
- **Neural network controllers**

## Applications in Applied Mechanics

### Structural Control

- **Active vibration control**: Buildings, bridges
- **Seismic isolation**: Earthquake protection
- **Wind turbine control**: Power regulation, load alleviation

### Vehicle Control

- **Cruise control**: Speed regulation
- **Electronic stability control**: Vehicle handling
- **Active suspension**: Ride comfort and handling

### Manufacturing Control

- **Robot control**: Position and force control
- **Machine tool control**: Precision machining
- **Process control**: Temperature, pressure, flow

### Aerospace Control

- **Flight control**: Aircraft stability and handling
- **Spacecraft attitude control**: Orientation control
- **Engine control**: Thrust and efficiency optimization

## Modern Control System Tools

### Software Packages

- **MATLAB/Simulink**: Industry standard for control design
- **Python**: Control library, growing popularity
- **LabVIEW**: Real-time control applications

### Hardware Platforms

- **Microcontrollers**: Arduino, Raspberry Pi
- **Real-time systems**: CompactRIO, dSPACE
- **Industrial PLCs**: Allen-Bradley, Siemens

### Implementation Considerations

- **Sampling rate**: Digital control system timing
- **Quantization effects**: A/D and D/A conversion
- **Computational delays**: Processing time limitations
- **Actuator saturation**: Physical limits on control action

Understanding control theory is essential for:

- System stability and performance
- Automated operation and safety
- Optimization of dynamic systems
- Integration of mechanical and electrical systems

Control systems form the "nervous system" of modern mechanical devices, enabling autonomous operation, precise regulation, and optimal performance across all engineering applications.

## Exercises

**Exercise 1.** A plant $G(s) = \frac{10}{s+1}$ is operated (a) open loop and (b) inside a unity-feedback loop. Find the DC gain from input to output in each case, and the percentage change in that gain when the plant gain drops by 20% (from 10 to 8). What does the comparison show?

<details>
<summary>Answer</summary>

(a) Open loop: the DC gain is $G(0) = 10$, which falls to 8, a change of $-20\%$.

(b) Closed loop: $T(0) = \frac{10}{1 + 10} = 0.909$, which falls to $\frac{8}{1+8} = 0.889$, a change of $-2.2\%$.

Feedback makes the output about $1 + G(0) \approx 11$ times less sensitive to plant variation. The price is that the closed-loop DC gain is not exactly 1 (a 9% steady-state error for a step), which integral action would remove.

</details>

**Exercise 2.** A mass-spring-damper has $m = 2$ kg, $c = 8$ N·s/m and $k = 50$ N/m. Find $\omega_n$, $\zeta$, the poles, the percentage overshoot of the step response, and the 2% settling time. Write the state matrices $\mathbf{A}$ and $\mathbf{B}$ for the state $[x, \dot{x}]^T$.

<details>
<summary>Answer</summary>

$\omega_n = \sqrt{k/m} = 5$ rad/s and $\zeta = \frac{c}{2\sqrt{km}} = \frac{8}{20} = 0.4$ (underdamped). The poles are the roots of $2s^2 + 8s + 50 = 0$: $s = -2 \pm 4.58j$.

Overshoot: $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} = e^{-1.371} = 0.254$, i.e. 25.4%. Settling time: $t_s \approx \frac{4}{\zeta\omega_n} = 2.0$ s.

$$
\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -25 & -4 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 0.5 \end{bmatrix}
$$

</details>

**Exercise 3.** For unity feedback with $G(s) = \frac{K}{s(s+1)(s+3)}$, use the Routh array to find the range of $K$ for stability, the ultimate gain $K_u$ and the ultimate period $T_u$. Then apply the Ziegler-Nichols PID rules.

<details>
<summary>Answer</summary>

Characteristic equation: $s^3 + 4s^2 + 3s + K = 0$.

$$
\begin{array}{c|cc}
s^3 & 1 & 3 \\
s^2 & 4 & K \\
s^1 & \frac{12 - K}{4} & 0 \\
s^0 & K &
\end{array}
$$

Stability requires $0 < K < 12$, so $K_u = 12$. At $K = 12$ the auxiliary equation $4s^2 + 12 = 0$ gives $s = \pm j\sqrt{3}$, so $\omega_u = 1.732$ rad/s and $T_u = 2\pi/\omega_u = 3.63$ s.

Ziegler-Nichols PID: $K_p = 0.6K_u = 7.2$, $K_i = 1.2K_u/T_u = 3.97\;\text{s}^{-1}$, $K_d = 0.075K_uT_u = 3.26$ s.

</details>

**Exercise 4.** Find the gain crossover frequency, phase margin and gain margin of $G(s) = \frac{10}{s(s+1)}$. Does it meet the design guidelines?

<details>
<summary>Answer</summary>

$|G(j\omega)| = \frac{10}{\omega\sqrt{\omega^2+1}} = 1$ gives $\omega^4 + \omega^2 - 100 = 0$, so $\omega^2 = 9.51$ and $\omega_{gc} = 3.08$ rad/s.

$$
PM = 180^\circ - 90^\circ - \arctan(3.08) = 18.0^\circ
$$

The phase only approaches $-180^\circ$ as $\omega \to \infty$, so there is no phase crossover and the gain margin is infinite. The phase margin is well below the $45^\circ$ guideline, so the step response will be very oscillatory.

</details>

**Exercise 5.** For the plant of Example 3, $G(s) = \frac{1}{s(s+1)(s+2)}$, use the Routh array to show that the gains $K_p = 12$, $K_i = 8$, $K_d = 3$ give an unstable closed loop. Explain why the $s^3$ coefficient of the closed-loop polynomial limits what any PID controller can achieve here.

<details>
<summary>Answer</summary>

The closed-loop polynomial is $s^4 + 3s^3 + (2 + K_d)s^2 + K_p s + K_i = s^4 + 3s^3 + 5s^2 + 12s + 8$.

$$
\begin{array}{c|ccc}
s^4 & 1 & 5 & 8 \\
s^3 & 3 & 12 & \\
s^2 & 1 & 8 & \\
s^1 & -12 & & \\
s^0 & 8 & &
\end{array}
$$

The first column changes sign twice ($1 \to -12 \to 8$), so there are two right-half-plane poles (they are $s \approx 0.14 \pm 1.95j$).

The $s^3$ coefficient equals minus the sum of the closed-loop poles and does not depend on the gains, so the four poles always sum to $-3$. Pushing the dominant pair far to the left forces the remaining poles toward the right, which is why a numerical search with a stability check is needed.

</details>

## References

- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
- N. S. Nise, *Control Systems Engineering*, 7th ed., Wiley, 2015.
- G. F. Franklin, J. D. Powell, A. Emami-Naeini, *Feedback Control of Dynamic Systems*, Pearson.
- K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, Princeton University Press, 2008.
