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
$$Y(s) = G(s)U(s)$$

**Closed-loop transfer function**:
$$\frac{Y(s)}{R(s)} = \frac{G(s)}{1 + G(s)H(s)}$$

where:
- $G(s)$ = plant transfer function
- $H(s)$ = sensor transfer function  
- $R(s)$ = reference input
- $Y(s)$ = system output
- $U(s)$ = control signal

## System Modeling

### Transfer Functions
For linear time-invariant (LTI) systems, the transfer function relates output to input in the Laplace domain:

$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + b_{m-1} s^{m-1} + ... + b_1 s + b_0}{a_n s^n + a_{n-1} s^{n-1} + ... + a_1 s + a_0}$$

### State-Space Representation
For systems with multiple inputs/outputs:

$$\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$$
$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$$

where:
- $\mathbf{x}$ = state vector
- $\mathbf{u}$ = input vector
- $\mathbf{y}$ = output vector
- $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$ = system matrices

### Example 1: Mass-Spring-Damper System

A mass $m$ connected to a spring (stiffness $k$) and damper (coefficient $c$):

**Equation of motion**:
$$m\ddot{x} + c\dot{x} + kx = F$$

**Transfer function**:
$$G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + cs + k}$$

**State-space form**:
Let $x_1 = x$, $x_2 = \dot{x}$:

$$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -k/m & -c/m \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \begin{bmatrix} 0 \\ 1/m \end{bmatrix} F$$

$$y = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$$

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
$$g(t) = \mathcal{L}^{-1}\{G(s)\}$$

For second-order systems:
$$G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

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
$$\begin{array}{c|cc}
s^n & a_n & a_{n-2} & a_{n-4} & ... \\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} & ... \\
s^{n-2} & b_1 & b_2 & b_3 & ... \\
s^{n-3} & c_1 & c_2 & c_3 & ... \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{array}$$

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
$$GM = \frac{1}{|G(j\omega_{pc})|} \text{ where } \angle G(j\omega_{pc}) = -180°$$

**Phase margin**: Additional phase lag before instability  
$$PM = 180° + \angle G(j\omega_{gc}) \text{ where } |G(j\omega_{gc})| = 1$$

**Design guidelines**:
- GM > 6 dB (factor of 2)
- PM > 45°

### Example 2: Stability Analysis

For unity feedback system with $G(s) = \frac{K}{s(s+2)(s+5)}$:

**Characteristic equation**: $s^3 + 7s^2 + 10s + K = 0$

**Routh array**:
$$\begin{array}{c|cc}
s^3 & 1 & 10 \\
s^2 & 7 & K \\
s^1 & \frac{70-K}{7} & 0 \\
s^0 & K & 
\end{array}$$

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
$$u(t) = K_p e(t)$$
$$C(s) = K_p$$

**Effects**:
- Reduces steady-state error
- May cause instability for high gains
- No improvement in transient response

#### Proportional-Integral (PI) Control
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau$$
$$C(s) = K_p + \frac{K_i}{s}$$

**Effects**:
- Eliminates steady-state error for step inputs
- Slower response due to integral action
- Reduces stability margins

#### Proportional-Integral-Derivative (PID) Control
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
$$C(s) = K_p + \frac{K_i}{s} + K_d s$$

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
For 2nd-order dominant behavior: $\zeta = 0.45$, $\omega_n = 2$ rad/s

**Step 2**: Design controller
Using pole placement or optimization techniques:
$K_p = 12$, $K_i = 8$, $K_d = 3$

**Step 3**: Verify performance
Simulate closed-loop response and check specifications.

## Advanced Control Topics

### State Feedback Control
$$\mathbf{u} = -\mathbf{K}\mathbf{x} + \mathbf{N}r$$

**Pole placement**: Choose $\mathbf{K}$ to place poles at desired locations
**LQR**: Minimize cost function $J = \int_0^∞ (\mathbf{x}^T\mathbf{Q}\mathbf{x} + \mathbf{u}^T\mathbf{R}\mathbf{u}) dt$

### Observer Design
Estimate unmeasured states:
$$\dot{\hat{\mathbf{x}}} = \mathbf{A}\hat{\mathbf{x}} + \mathbf{B}\mathbf{u} + \mathbf{L}(\mathbf{y} - \mathbf{C}\hat{\mathbf{x}})$$

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
