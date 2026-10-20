# System Modeling

A controller can only be designed against a model of what it controls. This note derives lumped differential-equation models of mechanical, electrical, electromechanical, fluid and thermal systems, converts them into transfer functions with the Laplace transform, works out the step responses of first- and second-order systems, introduces the state-space form, linearizes nonlinear models about an operating point, and reduces interconnected models with block-diagram algebra. The models reappear in the other notes: the pump-fed tank in [Frequency Response](./frequency_response.md), the heated water stream in [PID Controllers](./pid_controllers.md) and the car in [Introduction to Control Systems](./intro.md).

## Problem Statement

Given a physical system with an identified input $u(t)$ (force, voltage, flow, heat input), output $y(t)$ (position, speed, level, temperature) and parameters (masses, stiffnesses, resistances, areas), find a model that predicts $y$ from $u$, in one of three equivalent linear forms:

1. an $n$-th order linear ordinary differential equation with constant coefficients,

$$
a_n y^{(n)} + \dots + a_1 \dot{y} + a_0 y = b_m u^{(m)} + \dots + b_1 \dot{u} + b_0 u
$$

2. a transfer function $G(s) = Y(s)/U(s)$, the ratio of the Laplace transforms with zero initial conditions;
3. a state-space model $\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}u$, $y = \mathbf{C}\mathbf{x} + Du$.

The assumptions are lumped parameters (no spatial variation inside an element), linear constitutive laws or a linearization about an operating point, and parameters constant in time.

## Modeling Procedure

1. Draw the system boundary and name the input, the output and the disturbances.
2. Choose one variable per energy store (mass velocity, spring deflection, capacitor voltage, inductor current, tank level, body temperature). These become the states.
3. Write the balance laws: Newton's second law, Kirchhoff's voltage and current laws, conservation of mass, conservation of energy.
4. Write the constitutive laws of the elements (spring $F = kx$, resistor $v = Ri$, orifice $q = k_v\sqrt{h}$, conductor $q = \Delta T/R$).
5. Eliminate internal variables, linearize if necessary, and check the units of every term.

## Lumped Models of Physical Systems

### Mechanical Systems

A mass $m$ (kg) on a spring of stiffness $k$ (N/m) with a viscous damper $c$ (N s/m), driven by a force $F(t)$ (N), obeys

$$
m\ddot{x} + c\dot{x} + kx = F(t),
\qquad G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2 + cs + k}
$$

with $\omega_n = \sqrt{k/m}$ and $\zeta = c/(2\sqrt{km})$. The rotational analogue, an inertia $J$ (kg m²) on a torsional spring $k_t$ (N m/rad) with damping $b$ (N m s/rad) driven by a torque $\tau$, is $J\ddot{\theta} + b\dot{\theta} + k_t\theta = \tau$ with $G(s) = 1/(Js^2 + bs + k_t)$.

### Electrical Systems

Kirchhoff's voltage law around a series resistor $R$, inductor $L$ and capacitor $C$ driven by $v_{in}$, with the output taken across the capacitor, gives $`LC\ddot{v}_C + RC\dot{v}_C + v_C = v_{in}`$:

$$
G(s) = \frac{V_C(s)}{V_{in}(s)} = \frac{1/(LC)}{s^2 + (R/L)s + 1/(LC)},
\qquad \omega_n = \frac{1}{\sqrt{LC}},
\qquad \zeta = \frac{R}{2} \sqrt{\frac{C}{L}}
$$

### DC Motor

The armature circuit (resistance $R_a$, inductance $L_a$, back-EMF constant $K_b$) and the rotor (inertia $J$, viscous friction $b$, torque constant $K_t$) are coupled through the back-EMF $K_b\dot{\theta}$ and the torque $K_t i_a$:

$$
L_a \frac{di_a}{dt} + R_a i_a + K_b \dot{\theta} = v_a,
\qquad J\ddot{\theta} + b\dot{\theta} = K_t i_a
$$

In SI units $K_b = K_t$ for an ideal motor. Eliminating $i_a$ gives the transfer function from armature voltage to shaft angle,

$$
G(s) = \frac{\Theta(s)}{V_a(s)} = \frac{K_t}{s\left[(L_a s + R_a)(Js + b) + K_t K_b\right]}
$$

The factor $s$ is the integration from speed to angle. For $R_a = 2$ Ω, $L_a = 0.5$ H, $K_t = K_b = 0.1$ N m/A, $J = 0.01$ kg m² and $b = 0.1$ N m s/rad, the bracket is $(0.5s + 2)(0.01s + 0.1) + 0.01 = 0.005s^2 + 0.07s + 0.21$, so

$$
G(s) = \frac{0.1}{s(0.005s^2 + 0.07s + 0.21)} = \frac{20}{s(s^2 + 14s + 42)}
$$

with poles at $0$, $-4.35$ and $-9.65$ s⁻¹. When the electrical time constant $L_a/R_a$ is much shorter than the mechanical one $J/b$, $L_a$ can be neglected and the model drops to second order (Exercise 4 shows that this motor does not qualify).

### Fluid Systems: a Tank

A tank of cross-section $A$ (m²) with level $h$ (m), filled by a flow $q_{in}$ and drained through a valve whose outflow follows Torricelli's law $q_{out} = k_v\sqrt{h}$ (see [Bernoulli's Equation](../../fluid_mechanics/inviscid_flow/bernoulli.md)), obeys the mass balance

$$
A \frac{dh}{dt} = q_{in} - k_v \sqrt{h}
$$

This is nonlinear; its linearization is worked out below. If instead the outflow is drawn by a positive-displacement pump at a rate that does not depend on $h$, the level is the integral of the flow imbalance, $H(s)/Q_{in}(s) = 1/(As)$. That integrating tank is the plant of the level loop in [Frequency Response](./frequency_response.md). Pipe networks add inertance (the momentum of the liquid column, $\rho l/A_p$) and the pipe flow resistances of [Pipe Flow](../../fluid_mechanics/internal_flow/pipes.md).

### Thermal Systems

A body of heat capacity $C_{th}$ (J/K) at temperature $T$, heated at a rate $P$ (W) and losing heat to surroundings at $T_\infty$ through a thermal resistance $R_{th}$ (K/W), obeys $C_{th}\dot{T} = P - (T - T_\infty)/R_{th}$, a first-order system with time constant $R_{th}C_{th}$ and gain $R_{th}$.

The heated water stream of the PID note is the same balance with the loss replaced by the enthalpy carried away by the flow $\dot{m}$: $C_{th}\dot{T} = P - \dot{m}c_p(T - T_{in})$. With $\dot{m} = 0.12$ kg/s, $c_p = 4180$ J/(kg K) and $C_{th} = 5$ kJ/K (about 1.2 kg of water in the heater), the gain is $1/(\dot{m}c_p) = 2$ K/kW and the time constant $C_{th}/(\dot{m}c_p) = 10$ s. The temperature sensor sits downstream, so the measured temperature is also delayed by the transport time.

### Analogies

All these systems store and dissipate energy in the same patterns. With effort (force, voltage, pressure, temperature difference) and flow (velocity, current, volume flow, heat flow) as the paired variables:

| Element | Mechanical | Electrical | Fluid | Thermal |
| --- | --- | --- | --- | --- |
| Effort | Force $F$ | Voltage $v$ | Pressure $p$ | Temperature difference $\Delta T$ |
| Flow | Velocity $\dot{x}$ | Current $i$ | Volume flow $q$ | Heat flow $\dot{Q}$ |
| Resistance | Damper $c$ | Resistor $R$ | Valve or pipe $R_f = \Delta p/q$ | $R_{th} = \Delta T/\dot{Q}$ |
| Capacitance (stores effort) | Spring compliance $1/k$ | Capacitor $C$ | Tank $A/(\rho g)$ | Heat capacity $C_{th}$ |
| Inertance (stores flow) | Mass $m$ | Inductor $L$ | Liquid column $\rho l/A_p$ | (none) |

Thermal systems have no inertance, so a network of thermal resistances and capacitances cannot oscillate.

## Laplace Transform and Transfer Functions

The Laplace transform $`F(s) = \int_0^\infty f(t)e^{-st}\,dt`$ turns differentiation into multiplication by $s$:

```math
\mathcal{L}\{\dot{f}\} = sF(s) - f(0),
\qquad \mathcal{L}\{\ddot{f}\} = s^2F(s) - sf(0) - \dot{f}(0)
```

With zero initial conditions the ODE of the problem statement becomes algebraic, and

$$
G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_1 s + b_0}{a_n s^n + \dots + a_1 s + a_0} = K \frac{(s - z_1)\cdots(s - z_m)}{(s - p_1)\cdots(s - p_n)}
$$

The roots $p_i$ of the denominator are the poles; each contributes a mode $e^{p_i t}$ to the response, so their real parts set the decay rate and their imaginary parts the oscillation frequency. The roots $z_j$ of the numerator are the zeros; they do not create modes but change how much of each mode appears. A single real zero in the right half-plane makes the step response start in the wrong direction. The system is proper when $m \leq n$, which holds for every physical system.

The transfer function is the Laplace transform of the impulse response $g(t)$, and for any input $`y(t) = \int_0^t g(t - \tau)u(\tau)\,d\tau`$. Two limit theorems give the ends of a response without inverting the transform:

$$
y(0^+) = \lim_{s\to\infty} sY(s),
\qquad y(\infty) = \lim_{s\to 0} sY(s)
$$

The final value theorem holds only if $sY(s)$ has all its poles in the open left half-plane. For a unit step, $y(\infty) = G(0)$, the DC gain.

## First-Order Response

A first-order system $G(s) = K/(\tau s + 1)$ with a step of size $U$ responds as

$$
y(t) = KU\left(1 - e^{-t/\tau}\right)
$$

It reaches 63.2% of the final value at $t = \tau$, 95.0% at $3\tau$ and 98.2% at $4\tau$, so the 2% settling time is $t_s \approx 4\tau$, and the 10–90% rise time is $\tau\ln 9 = 2.2\tau$. The initial slope $KU/\tau$ is used to read $\tau$ from a measured step response.

## Second-Order Response

The standard second-order system

$$
G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}
$$

has poles $s = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2}$ when $0 < \zeta < 1$. In the $s$-plane they lie at distance $\omega_n$ from the origin, at angle $\arccos\zeta$ from the negative real axis, with real part $-\sigma = -\zeta\omega_n$ and imaginary part $\omega_d = \omega_n\sqrt{1 - \zeta^2}$, the damped natural frequency. Inverting $G(s)/s$ gives the unit step response

$$
y(t) = 1 -
\frac{e^{-\zeta\omega_n t}}{\sqrt{1 - \zeta^2}}\sin\left(\omega_d t +
\arccos\zeta\right)
$$

Setting $\dot{y} = 0$ gives the peak at $\omega_d t = \pi$, from which the peak time and overshoot follow; the envelope $e^{-\zeta\omega_n t}/\sqrt{1-\zeta^2}$ falling to 0.02 gives the settling time:

$$
t_p = \frac{\pi}{\omega_d},
\qquad M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}},
\qquad t_s = \frac{-\ln\left(0.02\sqrt{1 - \zeta^2}\right)}{\zeta\omega_n} \approx
\frac{4}{\zeta\omega_n}
$$

Inverting the overshoot formula gives the damping ratio needed for a specified overshoot, $\zeta = -\ln M_p/\sqrt{\pi^2 + \ln^2 M_p}$: 0.59 for 10% and 0.46 for 20%. For $\zeta \geq 1$ the poles are real, there is no overshoot, and for $\zeta > 1$ the slower pole $-\omega_n(\zeta - \sqrt{\zeta^2 - 1})$ dominates, so increasing the damping beyond 1 slows the response.

![Step responses for six damping ratios, overshoot and timing against the formulas, and pole locations](../../../scripts/algorithms/control_second_order_response/control_second_order_response.png)

The values measured from the simulated responses in the figure ($\omega_n = 2$ rad/s) are:

| $\zeta$ | $t_r$ (s) | $t_p$ (s) | $M_p$ (%) | $t_s$ measured (s) | $`4/\lvert\mathrm{Re}\,p\rvert`$ of the slowest pole (s) |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 0.55 | 1.58 | 72.9 | 19.2 | 20.0 |
| 0.3 | 0.66 | 1.65 | 37.2 | 5.62 | 6.67 |
| 0.5 | 0.82 | 1.81 | 16.3 | 4.04 | 4.00 |
| 0.7 | 1.06 | 2.20 | 4.6 | 2.99 | 2.86 |
| 1.0 | 1.68 |  | 0 | 2.92 | 2.00 |
| 2.0 | 4.12 |  | 0 | 7.44 | 7.46 |

Peak time and overshoot match the formulas exactly. The settling time is a staircase function of $\zeta$, because it jumps whenever a peak of the oscillation stops leaving the 2% band, so $4/(\zeta\omega_n)$ is an estimate within roughly 20% for $0.3 < \zeta < 0.8$. Overshoot depends on $\zeta$ alone, while all the times scale with $1/\omega_n$.

An additional real pole slows the response and reduces overshoot; an additional left-half-plane zero near the dominant poles increases overshoot. Both effects are small when the extra pole or zero is more than about five times farther from the imaginary axis than the dominant pair, which is the basis of the dominant-pole approximation.

## State-Space Form

Choosing the energy-storage variables as states gives $n$ first-order equations,

$$
\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u},
\qquad \mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}
$$

For the mass-spring-damper with $\mathbf{x} = [x,\ \dot{x}]^T$:

```math
\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -k/m & -c/m \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1/m \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = 0
```

The state-space form handles several inputs and outputs, nonzero initial conditions and time-varying or nonlinear models, and it is the form ODE integrators use.

From state space to transfer function, transforming with zero initial state gives

$$
G(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} + \mathbf{D}
$$

whose denominator is $\det(s\mathbf{I} - \mathbf{A})$, so the poles are the eigenvalues of $\mathbf{A}$ (unless a pole is cancelled by a zero).

From transfer function to state space the realization is not unique: any change of variables $\mathbf{x} = \mathbf{T}\mathbf{z}$ gives another. The controllable canonical form of $G(s) = (b_1 s + b_0)/(s^2 + a_1 s + a_0)$ is

```math
\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -a_0 & -a_1 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} b_0 & b_1 \end{bmatrix}, \quad D = 0
```

and extends to order $n$ with ones on the superdiagonal and $-a_0, \dots, -a_{n-1}$ in the last row (for a monic denominator).

## Linearization About an Operating Point

A nonlinear model $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u})$ has an operating point $(\bar{\mathbf{x}}, \bar{\mathbf{u}})$ where $\mathbf{f}(\bar{\mathbf{x}}, \bar{\mathbf{u}}) = 0$. For small deviations $\delta\mathbf{x} = \mathbf{x} - \bar{\mathbf{x}}$ and $\delta\mathbf{u} = \mathbf{u} - \bar{\mathbf{u}}$, a first-order Taylor expansion gives the linear model

```math
\delta\dot{\mathbf{x}} = \mathbf{A}\,\delta\mathbf{x} + \mathbf{B}\,\delta\mathbf{u},
\qquad \mathbf{A} = \left.
\frac{\partial\mathbf{f}}{\partial\mathbf{x}}\right|_{(\bar{\mathbf{x}}, \bar{\mathbf{u}})},
\qquad \mathbf{B} = \left.
\frac{\partial\mathbf{f}}{\partial\mathbf{u}}\right|_{(\bar{\mathbf{x}}, \bar{\mathbf{u}})}
```

The matrices depend on the operating point, so a single linear model holds only near it.

### Example: Gravity-Drained Tank

For the tank $A\dot{h} = q_{in} - k_v\sqrt{h}$ with $A = 1$ m², operating at $\bar{h} = 1$ m with $\bar{q} = 0.01$ m³/s (so $k_v = \bar{q}/\sqrt{\bar{h}} = 0.01$ $\mathrm{m}^{5/2}$/s), the derivative of the outflow is $k_v/(2\sqrt{\bar{h}}) = \bar{q}/(2\bar{h})$. Its inverse is the linearized outflow resistance

$$
R = \frac{2\bar{h}}{\bar{q}} = 200 \text{ s/m}^2,
\qquad \frac{\delta H(s)}{\delta Q_{in}(s)} = \frac{R}{ARs + 1} = \frac{200}{200s + 1}
$$

The time constant is $AR = 200$ s and the gain 200 m per m³/s: an extra 1 L/s of inflow raises the level by 0.2 m. At $\bar{h} = 0.25$ m the same valve passes 0.005 m³/s, and both the gain and the time constant halve to $R = 100$ s/m², which is why a level controller tuned at one level can be sluggish or oscillatory at another.

### Example: Inverted Pendulum on a Cart

A cart of mass $M$ carries a point mass $m$ on a massless rod of length $l$, with $\theta$ measured from the upright position and a horizontal force $F$ on the cart. Lagrange's equations, linearized for small $\theta$ ($\sin\theta \approx \theta$, $\cos\theta \approx 1$, $\dot{\theta}^2 \approx 0$), are $(M + m)\ddot{x} + ml\ddot{\theta} = F$ and $\ddot{x} + l\ddot{\theta} = g\theta$. With $\mathbf{x} = [x,\ \dot{x},\ \theta,\ \dot{\theta}]^T$ and both $x$ and $\theta$ measured:

```math
\mathbf{A} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & -mg/M & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & (M+m)g/(Ml) & 0 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1/M \\ 0 \\ -1/(Ml) \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{bmatrix}
```

The eigenvalues are $0, 0, \pm\sqrt{(M + m)g/(Ml)}$; the positive one makes the upright position unstable without feedback.

## Block-Diagram Algebra

Interconnected models are reduced with three rules: blocks in series multiply, $G_1 G_2$; blocks in parallel add, $G_1 + G_2$; and a block $G$ with $H$ in a negative feedback path reduces to

$$
T(s) = \frac{G(s)}{1 + G(s)H(s)}
$$

(with $1 - GH$ for positive feedback). To rearrange a diagram, a summing junction moved from after a block $G$ to before it requires the other input to be divided by $G$, and a pickoff point moved from before a block to after it requires the branch to be divided by $G$.

For diagrams with several interlocking loops, Mason's gain formula gives the transfer function directly from the signal-flow graph:

$$
T = \frac{1}{\Delta}\sum_k P_k\Delta_k,
\qquad \Delta = 1 - \sum_i L_i + \sum_{i,j} L_i L_j - \sum_{i,j,k} L_i L_j L_k + \dots
$$

Here $P_k$ is the gain of the $k$-th forward path, $L_i$ the gain of each loop, the sums of products run over loops that do not touch each other, and $\Delta_k$ is $\Delta$ computed with the loops that touch path $k$ removed.

## Key Takeaways

- Each energy store contributes one state and one order to the model; analogous elements in different domains give identical equations.
- The poles of $G(s)$ are the eigenvalues of $\mathbf{A}$ and set the modes; the zeros set how much of each mode appears.
- A second-order pair is described by $\omega_n$ and $\zeta$: overshoot depends only on $\zeta$, and every time scales with $1/\omega_n$.
- Linear models of nonlinear plants hold near an operating point, and their gains and time constants change with it.

## Related Scripts

- [Second-Order Step Response](../../../scripts/algorithms/control_second_order_response/): simulates the step response of the standard second-order system for six damping ratios, measures rise time, peak time, overshoot and settling time, and compares them with the closed-form formulas and the pole locations.

## Exercises

**Exercise 1.** A rotational system has $J = 0.02$ kg m², $b = 0.1$ N m s/rad and $k_t = 2$ N m/rad. Find its transfer function $\Theta(s)/T(s)$, natural frequency, damping ratio and DC gain.

<details>
<summary>Answer</summary>

```math
G(s) = \frac{1}{0.02s^2 + 0.1s + 2} = \frac{50}{s^2 + 5s + 100}
```

$\omega_n = \sqrt{k_t/J} = 10$ rad/s, $\zeta = \frac{b}{2\sqrt{Jk_t}} = \frac{0.1}{2 \times 0.2} = 0.25$, and the DC gain is $1/k_t = 0.5$ rad/(N m).

</details>

**Exercise 2.** Write the controllable canonical form of $G(s) = \frac{3s + 2}{s^2 + 4s + 5}$ and verify it using $G(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B}$.

<details>
<summary>Answer</summary>

With $a_1 = 4$, $a_0 = 5$, $b_1 = 3$, $b_0 = 2$:

```math
\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -5 & -4 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 2 & 3 \end{bmatrix}
```

```math
(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} = \frac{1}{s^2 + 4s + 5}\begin{bmatrix} s + 4 & 1 \\ -5 & s \end{bmatrix}\begin{bmatrix} 0 \\ 1 \end{bmatrix} = \frac{1}{s^2 + 4s + 5}\begin{bmatrix} 1 \\ s \end{bmatrix}
```

so $\mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} = \frac{2 + 3s}{s^2 + 4s + 5}$, as required.

</details>

**Exercise 3.** A pendulum of mass $m$ on a massless rod of length $l = 0.5$ m obeys $ml^2\ddot{\theta} + mgl\sin\theta = \tau$. Linearize about $\theta = 0$ (hanging) and $\theta = \pi$ (inverted), and find the eigenvalues of each linear model.

<details>
<summary>Answer</summary>

About $\theta = 0$: $\sin\theta \approx \theta$, so $\ddot{\theta} = -\frac{g}{l}\theta + \frac{\tau}{ml^2}$. The eigenvalues are $\pm j\sqrt{g/l} = \pm 4.43j$ rad/s: an undamped oscillation (marginally stable).

About $\theta = \pi$: with $\theta = \pi + \delta$, $\sin(\pi + \delta) \approx -\delta$, so $\ddot{\delta} = +\frac{g}{l}\delta + \frac{\tau}{ml^2}$. The eigenvalues are $\pm\sqrt{g/l} = \pm 4.43$ s⁻¹; the positive one makes the inverted position unstable.

</details>

**Exercise 4.** Using the motor data above, derive the simplified transfer function with $L_a \approx 0$ and compare its non-zero pole with the poles of the full model. Is the approximation justified for this motor?

<details>
<summary>Answer</summary>

```math
G(s) \approx \frac{K_t/R_a}{s(Js + b + K_tK_b/R_a)} = \frac{0.05}{s(0.01s + 0.105)} = \frac{5}{s(s + 10.5)}
```

The simplified model has a pole at $s = -10.5$. The full model $\frac{20}{s(s^2 + 14s + 42)}$ has poles at $s = -4.35$ and $s = -9.65$.

The approximation is poor because the electrical time constant $L_a/R_a = 0.25$ s is longer than the mechanical time constant $J/b = 0.1$ s. Neglecting $L_a$ is justified only when $L_a/R_a$ is much shorter than the mechanical time constant.

</details>

**Exercise 5.** A position servo has forward blocks $G_1 = K$ and $G_2 = \frac{1}{s(s+1)}$, a tachometer feedback $H_2 = s$ around $G_2$, and an outer unity feedback loop. Use Mason's gain formula to find $Y(s)/R(s)$, then choose $K$ for $\zeta = 0.5$.

<details>
<summary>Answer</summary>

There is one forward path, $P_1 = G_1G_2$, and two loops, $L_1 = -G_2H_2$ and $L_2 = -G_1G_2$. The loops touch each other and the forward path, so $\Delta = 1 + G_2H_2 + G_1G_2$ and $\Delta_1 = 1$:

```math
T(s) = \frac{G_1G_2}{1 + G_2H_2 + G_1G_2} = \frac{K}{s(s+1) + s + K} = \frac{K}{s^2 + 2s + K}
```

Comparing with $s^2 + 2\zeta\omega_n s + \omega_n^2$: $\zeta\omega_n = 1$, so $\zeta = 0.5$ requires $\omega_n = 2$ rad/s and $K = \omega_n^2 = 4$.

</details>

## References

- K. Ogata, *System Dynamics*, 4th ed., Pearson Prentice Hall, 2004.
- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
- N. S. Nise, *Control Systems Engineering*, 8th ed., Wiley, 2019.
- G. F. Franklin, J. D. Powell, A. Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., Pearson, 2019.
- K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, Princeton University Press, 2008.
