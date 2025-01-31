## Airplane Stability

Aircraft stability is a fundamental aspect of aerodynamics that ensures an airplane can maintain or return to a desired flight condition after a disturbance. Stability is categorized along three principal axes:

- Rotation about the lateral axis.
- Rotation about the longitudinal axis.
- Rotation about the vertical axis.

This document focuses on **longitudinal stability**, which involves controlling and stabilizing the aircraft's pitch attitude.

### Adding Pitch Control

Pitch control is essential for maintaining the desired angle of attack ($\alpha$) and for maneuvering the aircraft in the pitch axis. The primary control surfaces for pitch are the elevators located on the horizontal stabilizer of the empennage.

#### Control Surfaces

- A hinged surface on the trailing edge of the horizontal stabilizer used to control pitch.
- A one-piece horizontal tail surface that pivots to provide pitch control.

#### Mechanism of Pitch Control

The pitch control mechanism operates as follows:

- Pilot pulls back on the control column.
- Elevators deflect upward ($\delta_e > 0$).
- Downward aerodynamic force on the tail increases.
- Aircraft pitches up due to a nose-up moment.
- Pilot pushes forward on the control column.
- Elevators deflect downward ($\delta_e < 0$).
- Upward aerodynamic force on the tail increases.
- Aircraft pitches down due to a nose-down moment.

### Empennage in Aft

The empennage, or tail assembly, is located at the rear (aft) of the aircraft and provides stability and control in both pitch and yaw axes.

#### Components of the Empennage

- Provides longitudinal stability and supports the elevators.
- Provides directional stability and supports the rudder.
- Control pitch by altering the tail's lift.
- Controls yaw by altering the tail's lateral force.

#### Role in Stability

Placing the empennage aft leverages the moment arm between the center of gravity ($CG$) and the tail surfaces, enhancing stability and control effectiveness.

### Pitch Moment

The **pitching moment ($M$)** is a torque that causes rotation about the aircraft's lateral axis.

#### Definitions

- The point where the aircraft's mass is considered to act.
- The point along the chord where the aerodynamic pitching moment is constant with angle of attack.

#### Pitch Moment Equation

The total pitching moment about the $CG$ is:

$$M = M_{\text{wing}} + M_{\text{tail}} + M_{\text{fuselage}}$$

Where:

- Pitching moment due to the wing.
- Pitching moment due to the tail.
- Pitching moment due to the fuselage.

#### Pitching Moment Coefficient

The non-dimensional pitching moment coefficient is:

$$C_m = \frac{M}{\frac{1}{2} \rho V^2 S c}$$

Where:

- Air density.
- Flight speed.
- Wing reference area.
- Mean aerodynamic chord.

### Longitudinal Static Stability

An aircraft is **statically stable** in pitch if it tends to return to its original angle of attack after a disturbance.

#### Stability Criterion

The stability criterion is:

$$\frac{\partial C_m}{\partial \alpha} < 0$$

#### Contribution of Aircraft Components

Generates lift acting at its aerodynamic center.

$$M_{\text{wing}} = L_{\text{wing}} (x_{\text{AC,wing}} - x_{\text{CG}})$$

Tail provides a restoring moment.

$$L_{\text{tail}} = q S_{\text{tail}} C_{L_{\text{tail}}}$$

$$M_{\text{tail}} = -L_{\text{tail}} l_{\text{tail}}$$

Where $l_{\text{tail}} = x_{\text{CG}} - x_{\text{AC,tail}}$.

#### Total Pitching Moment Coefficient

$$C_m = C_{m_{\text{ac}}} + (C_{L_{\text{wing}}} + C_{L_{\text{tail}}}) \left( \frac{x_{\text{CG}} - x_{\text{ac}}}{c} \right)$$

### Neutral Point and Static Margin

#### Neutral Point ($NP$)

The neutral point is the $CG$ location where the aircraft is neutrally stable ($\frac{\partial C_m}{\partial \alpha} = 0$).

#### Static Margin ($SM$)

The static margin is:

$$SM = \frac{x_{\text{NP}} - x_{\text{CG}}}{c}$$

- Aircraft is stable.
- Aircraft is unstable.

### Tail Volume Coefficient

The tail volume coefficient ($V_H$) is a non-dimensional parameter representing the tail's effectiveness:

$$V_H = \frac{S_{\text{tail}} l_{\text{tail}}}{S c}$$

### Trim Condition

For steady-level flight, the aircraft must be in **trim**, meaning the sum of moments is zero.

#### Trim Equation

$$M_{\text{total}} = 0$$

#### Elevator Deflection for Trim

The required elevator deflection ($\delta_e$) for trim is found by solving:

$$C_m = C_{m_0} + C_{m_\alpha} \alpha + C_{m_{\delta_e}} \delta_e = 0$$

### Dynamic Stability

Dynamic stability involves the aircraft's response over time.

#### Longitudinal Modes

- Rapid oscillations involving angle of attack and pitch rate.
- Long-period oscillations involving exchange of kinetic and potential energy.

#### Stability Derivatives

- Derivative of pitching moment with respect to pitch rate ($q$).

$$C_{m_q} = \frac{\partial C_m}{\partial (q c / 2V)}$$

$$C_{m_{\dot{\alpha}}} = \frac{\partial C_m}{\partial (\dot{\alpha} c / 2V)}$$

### Control Surface Sizing

#### Elevator Effectiveness

The change in pitching moment due to elevator deflection is:

$$C_{m_{\delta_e}} = -\eta_{\text{e}} V_H C_{L_{\alpha_{\text{tail}}}}$$

Where:

- Elevator effectiveness factor.
- Tail lift curve slope.

#### Required Elevator Deflection

$$\delta_e = -\frac{C_{m_0} + C_{m_\alpha} \alpha}{C_{m_{\delta_e}}}$$

### Practical Design Considerations

- Aircraft must remain stable throughout its operational $CG$ range.
- Must balance stability requirements with weight and drag penalties.
- Ensuring sufficient control surface effectiveness for maneuvering.

**References**

- Anderson, J. D. *Aircraft Performance and Design*. McGraw-Hill.
- Stability and Control*. Wiley.
