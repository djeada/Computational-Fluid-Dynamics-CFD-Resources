# Control Systems

Control systems make a speed, a level, a temperature or an attitude follow a desired value despite disturbances and an imperfectly known plant. These notes cover classical single-loop control of linear time-invariant systems: building models from the physics, checking closed-loop stability from the characteristic polynomial and from the frequency response, using feedback to reject disturbances and reduce sensitivity to the plant, and designing and tuning compensators and PID controllers. The running examples are a car cruise control, a pump-fed tank level loop with a transport delay, a DC-motor position servo and a heated water stream.

## Table of Contents

### 1. [Introduction to Control Systems](./intro.md)

Plant, actuator, sensor, controller, reference and disturbance; open-loop and closed-loop operation; time- and frequency-domain specifications; the linear time-invariant assumption and its limits.

### 2. [System Modeling](./system_modeling.md)

Lumped models of mechanical, electrical, electromechanical, fluid and thermal systems, the Laplace transform and transfer functions, poles and zeros, first- and second-order step responses, state-space form, linearization and block-diagram algebra.

### 3. [Stability Analysis](./stability_analysis.md)

BIBO and internal stability, pole locations, the Routh–Hurwitz criterion with its special cases and relative stability, and the root locus.

### 4. [Frequency Response](./frequency_response.md)

Bode plots and their asymptotes, the Nyquist criterion, gain, phase and delay margins, peak sensitivity, bandwidth, the relation between phase margin and damping, time delay and loop shaping.

### 5. [Feedback Control](./feedback_control.md)

Closed-loop transfer functions with disturbance and noise, sensitivity and complementary sensitivity, parameter sensitivity, steady-state error and system type, and lead and lag compensation.

### 6. [PID Controllers](./pid_controllers.md)

The P, I and D actions, ideal, parallel and series forms, derivative filtering, set-point weighting, integrator windup and anti-windup, Ziegler–Nichols, Cohen–Coon, IMC and SIMC tuning, and discrete implementation.
