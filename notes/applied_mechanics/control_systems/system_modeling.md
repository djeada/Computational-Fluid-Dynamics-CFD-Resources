# System Modeling

System modeling is the process of developing mathematical descriptions of physical systems so that their behavior can be analyzed and controlled. Accurate models are the foundation of every control design — without a reliable model, no controller can guarantee performance or stability.

## Mathematical Modeling of Physical Systems

A mathematical model captures the essential dynamics of a system using differential equations, transfer functions, or state-space representations. The modeling procedure follows a consistent workflow:

1. **Identify** the system and its boundary
2. **Define** inputs, outputs, and states
3. **Apply** fundamental physical laws (Newton's laws, Kirchhoff's laws, energy conservation)
4. **Linearize** about an operating point if necessary
5. **Transform** into a convenient mathematical form

### Assumptions and Linearization

Most physical systems are nonlinear. For small deviations about an equilibrium point $\bar{x}$, a nonlinear function $f(x)$ can be linearized using a Taylor expansion:

$$f(x) \approx f(\bar{x}) + \left.\frac{\partial f}{\partial x}\right|_{\bar{x}} (x - \bar{x})$$

This yields a linear time-invariant (LTI) model valid in a neighborhood of the operating point.

## Mechanical Systems

### Mass-Spring-Damper System

Applying Newton's second law to a mass $m$ with spring stiffness $k$, damping coefficient $c$, and external force $F(t)$:

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

Taking the Laplace transform with zero initial conditions:

$$G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + cs + k}$$

### Rotational System

For a rotating inertia $J$ with torsional spring $k_t$ and damping $b$:

$$J\ddot{\theta} + b\dot{\theta} + k_t\theta = \tau(t)$$

$$G(s) = \frac{\Theta(s)}{T(s)} = \frac{1}{Js^2 + bs + k_t}$$

## Electrical Systems

### RLC Circuit

Applying Kirchhoff's voltage law around a series RLC loop driven by voltage $v_{in}(t)$, with output taken across the capacitor:

$$L\frac{di}{dt} + Ri + \frac{1}{C}\int i\,dt = v_{in}(t)$$

The transfer function from input voltage to capacitor voltage is:

$$G(s) = \frac{V_C(s)}{V_{in}(s)} = \frac{1/(LC)}{s^2 + (R/L)s + 1/(LC)}$$

This is a second-order system with natural frequency $\omega_n = 1/\sqrt{LC}$ and damping ratio $\zeta = \frac{R}{2}\sqrt{\frac{C}{L}}$.

### Analogy Between Mechanical and Electrical Systems

| Mechanical (Translational) | Electrical |
|---|---|
| Force $F$ | Voltage $v$ |
| Velocity $\dot{x}$ | Current $i$ |
| Mass $m$ | Inductance $L$ |
| Damping $c$ | Resistance $R$ |
| Spring $1/k$ | Capacitance $C$ |

## Electromechanical Systems

### DC Motor Model

A DC motor converts electrical energy to mechanical rotation. The armature circuit and mechanical load are coupled through the back-EMF and torque constants.

**Electrical equation** (armature circuit):

$$L_a \frac{di_a}{dt} + R_a i_a + K_b \dot{\theta} = v_a(t)$$

**Mechanical equation** (rotor):

$$J\ddot{\theta} + b\dot{\theta} = K_t i_a$$

where $K_b$ is the back-EMF constant, $K_t$ is the torque constant, and for an ideal motor $K_b = K_t$.

**Transfer function** from input voltage to shaft angle:

$$G(s) = \frac{\Theta(s)}{V_a(s)} = \frac{K_t}{s[(L_a s + R_a)(Js + b) + K_t K_b]}$$

If armature inductance is small ($L_a \approx 0$):

$$G(s) \approx \frac{K_t}{s[R_a(Js + b) + K_t K_b]} = \frac{K_t / R_a}{s(Js + b + K_t K_b / R_a)}$$

## Transfer Functions from Differential Equations

For any linear constant-coefficient ODE, the transfer function is obtained by taking the Laplace transform with zero initial conditions.

**General $n$-th order system**:

$$a_n \frac{d^n y}{dt^n} + \cdots + a_1 \frac{dy}{dt} + a_0 y = b_m \frac{d^m u}{dt^m} + \cdots + b_1 \frac{du}{dt} + b_0 u$$

$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \cdots + b_1 s + b_0}{a_n s^n + \cdots + a_1 s + a_0}$$

The **poles** (roots of the denominator) determine stability and transient behavior. The **zeros** (roots of the numerator) shape the response.

## State-Space Representation

State-space models use first-order matrix differential equations:

$$\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$$
$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$$

### Converting Transfer Function to State-Space

For a transfer function $G(s) = \frac{b_1 s + b_0}{s^2 + a_1 s + a_0}$, the **controllable canonical form** is:

$$\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -a_0 & -a_1 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} b_0 & b_1 \end{bmatrix}, \quad D = 0$$

### Converting State-Space to Transfer Function

$$G(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} + \mathbf{D}$$

## Block Diagram Algebra

Complex systems are built from interconnected subsystems. Standard block diagram reduction rules include:

- **Series**: $G_{total}(s) = G_1(s) \cdot G_2(s)$
- **Parallel**: $G_{total}(s) = G_1(s) + G_2(s)$
- **Negative feedback**: $T(s) = \frac{G(s)}{1 + G(s)H(s)}$
- **Positive feedback**: $T(s) = \frac{G(s)}{1 - G(s)H(s)}$

### Moving Blocks

- Moving a summing junction ahead of a block $G$: multiply the other input by $1/G$
- Moving a pickoff point ahead of a block $G$: multiply the branch by $1/G$

## Signal Flow Graphs and Mason's Gain Formula

A signal flow graph represents the system as nodes (signals) and directed branches (gains). **Mason's gain formula** computes the overall transfer function directly:

$$T(s) = \frac{1}{\Delta} \sum_{k} G_k \Delta_k$$

where:
- $G_k$ = gain of the $k$-th forward path
- $\Delta = 1 - \sum L_i + \sum L_i L_j - \sum L_i L_j L_k + \cdots$
- $L_i$ = gain of each individual loop
- $L_i L_j$ = product of non-touching loop pairs
- $\Delta_k$ = cofactor of $\Delta$ for the $k$-th forward path (remove all loops touching path $k$)

## Worked Examples

### Example 1: DC Motor Transfer Function

**Given**: A DC motor with $R_a = 2\;\Omega$, $L_a = 0.5\;\text{H}$, $K_t = K_b = 0.1\;\text{N·m/A}$, $J = 0.01\;\text{kg·m}^2$, $b = 0.1\;\text{N·m·s/rad}$.

**Find**: Transfer function $\Theta(s)/V_a(s)$.

**Solution**:

$$G(s) = \frac{K_t}{s[(L_a s + R_a)(Js + b) + K_t K_b]}$$

Substituting values:

$$G(s) = \frac{0.1}{s[(0.5s + 2)(0.01s + 0.1) + 0.01]}$$

Expanding the denominator:

$$(0.5s + 2)(0.01s + 0.1) = 0.005s^2 + 0.05s + 0.02s + 0.2 = 0.005s^2 + 0.07s + 0.2$$

Adding $K_t K_b = 0.01$:

$$G(s) = \frac{0.1}{s(0.005s^2 + 0.07s + 0.21)} = \frac{20}{s(s^2 + 14s + 42)}$$

### Example 2: Inverted Pendulum State-Space Model

**Given**: A cart of mass $M$ carrying an inverted pendulum of mass $m$ and length $l$. Small-angle approximation applies ($\sin\theta \approx \theta$, $\cos\theta \approx 1$).

**Find**: Linearized state-space model.

**Solution**:

Define states $\mathbf{x} = [x,\;\dot{x},\;\theta,\;\dot{\theta}]^T$ where $x$ is cart position and $\theta$ is pendulum angle from vertical. The linearized equations of motion yield:

$$\mathbf{A} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & -mg/M & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & (M+m)g/(Ml) & 0 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1/M \\ 0 \\ -1/(Ml) \end{bmatrix}$$

$$\mathbf{C} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{bmatrix}, \quad \mathbf{D} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

The eigenvalues of $\mathbf{A}$ include a positive real value, confirming that the inverted pendulum is **open-loop unstable** and requires active feedback control.

## Applications

- **Aerospace**: Modeling aircraft longitudinal/lateral dynamics for autopilot design
- **Robotics**: Multi-link manipulator dynamics using Lagrangian mechanics
- **Automotive**: Suspension quarter-car and full-car models for ride analysis
- **Process control**: Thermal systems, chemical reactors, and fluid networks
- **Power systems**: Generator and grid dynamics for voltage/frequency regulation

## Practical Tips

- Always **verify units** when deriving transfer functions — dimensional errors are the most common modeling mistake
- Start with the **simplest model** that captures the dominant dynamics, then add complexity as needed
- Use **experimental identification** (step tests, frequency sweeps) to validate or supplement analytical models
- For MIMO systems, state-space is generally more convenient than transfer function matrices
- Mason's gain formula is powerful for complex signal flow graphs but error-prone by hand — double-check loop identification
