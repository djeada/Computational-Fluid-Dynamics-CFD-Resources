## Airplane Stability

Aircraft stability is a fundamental aspect of aerodynamics that ensures an airplane can maintain or return to a desired flight condition after a disturbance. Stability is categorized along three principal axes:

- Rotation about the lateral axis.
- Rotation about the longitudinal axis.
- Rotation about the vertical axis.

This document focuses on **longitudinal stability**, which involves controlling and stabilizing the aircraft's pitch attitude.

### Adding Pitch Control

Pitch control is essential for maintaining the desired angle of attack ($\alpha$) and for maneuvering the aircraft in the pitch axis. The primary control surfaces for pitch are the elevators located on the horizontal stabilizer of the empennage.

#### Control Surfaces

- **Elevator**: A hinged surface on the trailing edge of the horizontal stabilizer used to control pitch.
- **Stabilator** (all-moving tail): A one-piece horizontal tail surface that pivots to provide pitch control.

#### Mechanism of Pitch Control

The pitch control mechanism operates as follows:

- Pilot pulls back on the control column.
- Elevators deflect upward ($\delta_e < 0$, with the usual convention that trailing-edge-down deflection is positive).
- Downward aerodynamic force on the tail increases.
- Aircraft pitches up due to a nose-up moment.
- Pilot pushes forward on the control column.
- Elevators deflect downward ($\delta_e > 0$).
- Upward aerodynamic force on the tail increases.
- Aircraft pitches down due to a nose-down moment.

### Empennage in Aft

The empennage, or tail assembly, is located at the rear (aft) of the aircraft and provides stability and control in both pitch and yaw axes.

#### Components of the Empennage

- **Horizontal stabilizer**: Provides longitudinal stability and supports the elevators.
- **Vertical stabilizer**: Provides directional stability and supports the rudder.
- **Elevators**: Control pitch by altering the tail's lift.
- **Rudder**: Controls yaw by altering the tail's lateral force.

#### Role in Stability

Placing the empennage aft leverages the moment arm between the center of gravity ($CG$) and the tail surfaces, enhancing stability and control effectiveness.

### Pitch Moment

The **pitching moment ($M$)** is a torque that causes rotation about the aircraft's lateral axis.

#### Definitions

- **Center of gravity** ($CG$): The point where the aircraft's mass is considered to act.
- **Aerodynamic center** ($AC$): The point along the chord where the aerodynamic pitching moment is constant with angle of attack.

#### Pitch Moment Equation

The total pitching moment about the $CG$ is:

$$
M = M_{\text{wing}} + M_{\text{tail}} + M_{\text{fuselage}}
$$

Where:

- $M_{\text{wing}}$: Pitching moment due to the wing.
- $M_{\text{tail}}$: Pitching moment due to the tail.
- $M_{\text{fuselage}}$: Pitching moment due to the fuselage.

#### Pitching Moment Coefficient

The non-dimensional pitching moment coefficient is:

$$
C_m = \frac{M}{\frac{1}{2} \rho V^2 S c}
$$

Where:

- $\rho$: Air density.
- $V$: Flight speed.
- $S$: Wing reference area.
- $c$: Mean aerodynamic chord.

### Longitudinal Static Stability

An aircraft is **statically stable** in pitch if it tends to return to its original angle of attack after a disturbance.

#### Stability Criterion

The stability criterion is:

$$
\frac{\partial C_m}{\partial \alpha} < 0
$$

#### Contribution of Aircraft Components

**Wing**: Generates lift acting at its aerodynamic center. With $x$ measured aft (towards the tail) and nose-up moments positive:

$$
M_{\text{wing}} = L_{\text{wing}} (x_{\text{CG}} - x_{\text{AC,wing}})
$$

**Tail**: Provides a restoring moment.

$$
L_{\text{tail}} = q S_{\text{tail}} C_{L_{\text{tail}}}
$$

$$
M_{\text{tail}} = -L_{\text{tail}} l_{\text{tail}}
$$

Where $l_{\text{tail}} = x_{\text{AC,tail}} - x_{\text{CG}}$ is the (positive) tail moment arm.

#### Total Pitching Moment Coefficient

$$
C_m = C_{m_{\text{ac}}} + C_{L_{\text{wing}}}
\left(\frac{x_{\text{CG}} - x_{\text{ac}}}{c} \right) - \eta V_H C_{L_{\text{tail}}}
$$

where $\eta = q_{\text{tail}}/q$ is the tail efficiency and $V_H$ is the tail volume coefficient defined below (fuselage contribution neglected).

### Neutral Point and Static Margin

#### Neutral Point ($NP$)

The neutral point is the $CG$ location where the aircraft is neutrally stable ($\frac{\partial C_m}{\partial \alpha} = 0$).

#### Static Margin ($SM$)

The static margin is:

$$
SM = \frac{x_{\text{NP}} - x_{\text{CG}}}{c}
$$

- $SM > 0$: Aircraft is stable.
- $SM < 0$: Aircraft is unstable.

### Tail Volume Coefficient

The tail volume coefficient ($V_H$) is a non-dimensional parameter representing the tail's effectiveness:

$$
V_H = \frac{S_{\text{tail}} l_{\text{tail}}}{S c}
$$

### Trim Condition

For steady-level flight, the aircraft must be in **trim**, meaning the sum of moments is zero.

#### Trim Equation

$$
M_{\text{total}} = 0
$$

#### Elevator Deflection for Trim

The required elevator deflection ($\delta_e$) for trim is found by solving:

$$
C_m = C_{m_0} + C_{m_\alpha} \alpha + C_{m_{\delta_e}} \delta_e = 0
$$

### Dynamic Stability

Dynamic stability involves the aircraft's response over time.

#### Longitudinal Modes

- **Short-period mode**: Rapid oscillations involving angle of attack and pitch rate.
- **Phugoid mode**: Long-period oscillations involving exchange of kinetic and potential energy.

#### Stability Derivatives

- **Pitch damping** ($C_{m_q}$): Derivative of pitching moment with respect to non-dimensional pitch rate ($q$).

$$
C_{m_q} = \frac{\partial C_m}{\partial (q c / 2V)}
$$

The corresponding derivative with respect to the rate of change of angle of attack is:

$$
C_{m_{\dot{\alpha}}} = \frac{\partial C_m}{\partial (\dot{\alpha} c / 2V)}
$$

### Control Surface Sizing

#### Elevator Effectiveness

The change in pitching moment due to elevator deflection is:

$$
C_{m_{\delta_e}} = -\eta_{\text{e}} V_H C_{L_{\alpha_{\text{tail}}}}
$$

Where:

- $\eta_{\text{e}}$: Elevator effectiveness factor.
- $C_{L_{\alpha_{\text{tail}}}}$: Tail lift curve slope.

#### Required Elevator Deflection

$$
\delta_e = -\frac{C_{m_0} + C_{m_\alpha} \alpha}{C_{m_{\delta_e}}}
$$

### Practical Design Considerations

- Aircraft must remain stable throughout its operational $CG$ range.
- Must balance stability requirements with weight and drag penalties.
- Ensuring sufficient control surface effectiveness for maneuvering.

### Exercises

**Exercise 1.** Using the sign conventions in these notes (positive $\delta_e$ is trailing edge down, and nose-up pitching moments are positive), what are the signs of $C_{m_{\delta_e}}$ and $C_{m_\alpha}$ for a conventional, statically stable aircraft with an aft tail? What elevator deflection sign is needed to trim at a higher angle of attack?

<details>
<summary>Answer</summary>

Trailing-edge-down elevator increases the tail's lift, which acts behind the CG and pitches the nose down, so $C_{m_{\delta_e}} < 0$. Static stability requires $C_{m_\alpha} < 0$.

From $\delta_e = -(C_{m_0} + C_{m_\alpha}\alpha)/C_{m_{\delta_e}}$: raising $\alpha$ makes $C_{m_0} + C_{m_\alpha}\alpha$ more negative, so $\delta_e$ becomes more negative. The elevator moves trailing edge up, which matches pulling back on the control column to fly slower.

</details>

**Exercise 2.** An aircraft has wing area $S = 16$ m² and mean aerodynamic chord $c = 1.5$ m. Its horizontal tail has $S_{tail} = 3.6$ m² and moment arm $l_{tail} = 4.5$ m. With $\eta_e = 0.45$ and $C_{L_{\alpha_{tail}}} = 4.3$ per radian, find the tail volume coefficient and the elevator control power $C_{m_{\delta_e}}$.

<details>
<summary>Answer</summary>

```math
V_H = \frac{S_{tail}\,l_{tail}}{Sc} = \frac{3.6 \times 4.5}{16 \times 1.5} = 0.675
```

```math
C_{m_{\delta_e}} = -\eta_e V_H C_{L_{\alpha_{tail}}} = -0.45 \times 0.675 \times
4.3 = -1.31 \text{ per rad}
```

</details>

**Exercise 3.** For the aircraft of Exercise 2, $C_{m_0} = 0.06$ and $C_{m_\alpha} = -1.0$ per radian. Find the elevator deflection needed to trim at $\alpha = 5^\circ$.

<details>
<summary>Answer</summary>

$\alpha = 0.0873$ rad, so $C_{m_0} + C_{m_\alpha}\alpha = 0.06 - 0.0873 = -0.0273$.

```math
\delta_e = -\frac{-0.0273}{-1.31} = -0.0209 \text{ rad} = -1.20^\circ
```

That is 1.2° trailing edge up, consistent with Exercise 1.

</details>

**Exercise 4.** The neutral point is 0.62 m and the CG 0.45 m behind the leading edge of the mean aerodynamic chord ($c = 1.5$ m). The aircraft lift-curve slope is 5.2 per radian. Find the static margin and $`C_{m_\alpha} = -C_{L_\alpha}\,SM`$. How far aft can the CG move if the static margin must stay at least 5%?

<details>
<summary>Answer</summary>

```math
SM = \frac{0.62 - 0.45}{1.5} = 0.113 \ (11.3\%), \quad C_{m_\alpha} = -5.2 \times 0.113 = -0.59 \text{ per rad}
```

For $SM \geq 0.05$: $x_{CG} \leq 0.62 - 0.05 \times 1.5 = 0.545$ m. The aft CG limit is therefore 0.545 m, and loading must keep the CG ahead of it.

</details>

**Exercise 5.** Lanchester's approximation gives the phugoid period as $`T \approx \pi\sqrt{2}\,V/g`$. Estimate it at 60 m/s and explain why pilots can easily control the phugoid but not a poorly damped short-period mode.

<details>
<summary>Answer</summary>

```math
T \approx \pi \sqrt{2} \times \frac{60}{9.81} = 27 \text{ s}
```

The phugoid is a slow exchange of height and speed at nearly constant angle of attack, so a pilot has plenty of time to correct it even when it is lightly damped. The short-period mode involves angle of attack and pitch rate over about a second, faster than a pilot can respond without risking pilot-induced oscillation. It therefore needs good natural damping ($C_{m_q}$) or a stability augmentation system.

</details>

### References

- Anderson, J. D., Jr., *Aircraft Performance and Design*, McGraw-Hill, 1999.
- Etkin, B., and Reid, L. D., *Dynamics of Flight: Stability and Control*, 3rd ed., Wiley, 1996.
- Nelson, R. C., *Flight Stability and Automatic Control*, 2nd ed., McGraw-Hill, 1998.
