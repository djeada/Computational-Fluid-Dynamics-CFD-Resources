# Impulse-Momentum Methods

Impulse-momentum methods relate forces acting over time intervals to changes in momentum. These methods are particularly effective for analyzing collisions, impacts, explosions, and any situation where forces act over short or variable time periods.

## Linear Impulse and Momentum

### Linear Momentum

The **linear momentum** of a particle is:

$$\mathbf{L} = m\mathbf{v}$$

For a system of particles or a rigid body:

$$\mathbf{L} = m\mathbf{v}_G$$

where $\mathbf{v}_G$ is the velocity of the mass center.

### Linear Impulse

The **linear impulse** of a force over a time interval is:

$$\mathbf{Imp} = \int_{t_1}^{t_2} \mathbf{F} \, dt$$

For a constant force: $\mathbf{Imp} = \mathbf{F}(t_2 - t_1) = \mathbf{F}\Delta t$

## Impulse-Momentum Theorem

Newton's second law in integral form gives the **impulse-momentum theorem**:

$$m\mathbf{v}_1 + \sum \int_{t_1}^{t_2} \mathbf{F} \, dt = m\mathbf{v}_2$$

In words: initial momentum plus the total impulse equals final momentum.

In component form:

$$mv_{1x} + \sum \int_{t_1}^{t_2} F_x \, dt = mv_{2x}$$

$$mv_{1y} + \sum \int_{t_1}^{t_2} F_y \, dt = mv_{2y}$$

## Conservation of Linear Momentum

When the **net external impulse** on a system is zero in a given direction, linear momentum is conserved in that direction:

$$\sum m_i \mathbf{v}_{i,1} = \sum m_i \mathbf{v}_{i,2}$$

This applies to:
- Collisions (internal forces are large; external forces are comparatively negligible during impact)
- Explosions and separations
- Systems with no external force in a particular direction

## Angular Impulse and Angular Momentum

### Angular Momentum of a Particle

About a fixed point $O$:

$$\mathbf{H}_O = \mathbf{r} \times m\mathbf{v}$$

In planar problems: $H_O = mvd$, where $d$ is the perpendicular distance from $O$ to the line of action of $m\mathbf{v}$.

### Angular Momentum of a Rigid Body

About the mass center $G$:
$$H_G = I_G \omega$$

About a fixed point $O$:
$$H_O = I_O \omega = (I_G + md^2)\omega$$

where $d$ is the distance from $O$ to $G$.

### Angular Impulse-Momentum Theorem

$$(H_O)_1 + \sum \int_{t_1}^{t_2} M_O \, dt = (H_O)_2$$

If no net external moment acts about $O$, angular momentum is conserved:

$$I_1\omega_1 = I_2\omega_2$$

This explains phenomena like a figure skater spinning faster when pulling in their arms.

## Impact

**Impact** is a collision between two bodies over a very short time interval, during which large internal forces act while external forces (like gravity) are negligible by comparison.

### Classification

- **Direct impact:** Velocities are along the line connecting the mass centers (line of impact)
- **Oblique impact:** Velocities have components both along and perpendicular to the line of impact

### Coefficient of Restitution

The **coefficient of restitution** $e$ characterizes the elasticity of the collision along the line of impact:

$$e = \frac{v_{B2} - v_{A2}}{v_{A1} - v_{B1}}$$

where $v_{A1}, v_{B1}$ are approach velocities and $v_{A2}, v_{B2}$ are separation velocities along the line of impact.

- $e = 1$: Perfectly elastic (kinetic energy conserved)
- $0 < e < 1$: Partially elastic (some energy lost)
- $e = 0$: Perfectly plastic (bodies stick together)

### Direct Central Impact

Two particles collide head-on. Conservation of momentum and the restitution equation give:

$$m_A v_{A1} + m_B v_{B1} = m_A v_{A2} + m_B v_{B2}$$

$$e(v_{A1} - v_{B1}) = v_{B2} - v_{A2}$$

Solving simultaneously:

$$v_{A2} = \frac{m_A v_{A1} + m_B v_{B1} + m_B e(v_{B1} - v_{A1})}{m_A + m_B}$$

$$v_{B2} = \frac{m_A v_{A1} + m_B v_{B1} + m_A e(v_{A1} - v_{B1})}{m_A + m_B}$$

### Oblique Impact

For oblique impact between smooth particles:
1. **Along the line of impact:** Apply conservation of momentum and the restitution equation
2. **Perpendicular to the line of impact:** Each particle's momentum component is individually conserved (no force in that direction)

## Worked Examples

### Example 1: Direct Central Impact

A 2 kg ball moving at 6 m/s strikes a stationary 3 kg ball. The coefficient of restitution is $e = 0.7$.

**Given:**
- $m_A = 2$ kg, $v_{A1} = 6$ m/s
- $m_B = 3$ kg, $v_{B1} = 0$
- $e = 0.7$

**Find:** Final velocities and energy lost.

**Solution:**

**Conservation of momentum:**
$$2(6) + 3(0) = 2v_{A2} + 3v_{B2}$$
$$12 = 2v_{A2} + 3v_{B2} \quad \text{...(1)}$$

**Restitution:**
$$v_{B2} - v_{A2} = e(v_{A1} - v_{B1}) = 0.7(6 - 0) = 4.2 \quad \text{...(2)}$$

From (2): $v_{B2} = v_{A2} + 4.2$

Substituting into (1):
$$12 = 2v_{A2} + 3(v_{A2} + 4.2) = 5v_{A2} + 12.6$$

$$v_{A2} = -0.12 \text{ m/s}, \quad v_{B2} = 4.08 \text{ m/s}$$

Ball $A$ bounces back slightly; ball $B$ moves forward.

**Energy lost:**
$$\Delta T = \frac{1}{2}(2)(6)^2 - \left[\frac{1}{2}(2)(0.12)^2 + \frac{1}{2}(3)(4.08)^2\right]$$
$$\Delta T = 36 - [0.0144 + 24.97] = 11.02 \text{ J}$$

### Example 2: Ballistic Pendulum

A 10 g bullet embeds itself in a 2 kg wooden block suspended as a pendulum. The block swings upward 0.15 m.

**Given:**
- $m_b = 0.01$ kg (bullet), $m_B = 2$ kg (block)
- $h = 0.15$ m (height of swing)
- Perfectly plastic impact ($e = 0$)

**Find:** Initial speed of the bullet.

**Solution:**

**Step 1 — Impact (conservation of momentum):**
$$m_b v_0 = (m_b + m_B)v'$$
$$0.01 v_0 = (0.01 + 2)v' = 2.01v' \quad \text{...(1)}$$

**Step 2 — Swing (conservation of energy):**
$$\frac{1}{2}(m_b + m_B)v'^2 = (m_b + m_B)gh$$
$$v' = \sqrt{2gh} = \sqrt{2(9.81)(0.15)} = 1.716 \text{ m/s}$$

**Substituting back into (1):**
$$v_0 = \frac{2.01(1.716)}{0.01} = 345 \text{ m/s}$$

### Example 3: Rocket Propulsion

A 1000 kg rocket in space exhausts propellant at 50 kg/s with an exhaust velocity of 3000 m/s relative to the rocket.

**Given:**
- $m_0 = 1000$ kg (initial mass)
- $\dot{m}_e = 50$ kg/s (mass flow rate)
- $v_e = 3000$ m/s (exhaust velocity)
- No external forces (space)

**Find:** Thrust and velocity after 10 seconds.

**Solution:**

**Thrust (force from exhaust):**
$$F_{thrust} = \dot{m}_e v_e = 50(3000) = 150\,000 \text{ N} = 150 \text{ kN}$$

**Tsiolkovsky rocket equation:**
$$v = v_0 + v_e \ln\frac{m_0}{m_0 - \dot{m}_e t}$$

Starting from rest ($v_0 = 0$) after $t = 10$ s:

$$m_{final} = 1000 - 50(10) = 500 \text{ kg}$$

$$v = 0 + 3000\ln\frac{1000}{500} = 3000\ln 2 = 3000(0.693) = 2079 \text{ m/s}$$

### Example 4: Oblique Impact

A ball strikes a smooth wall at 10 m/s at an angle of 40° to the wall. The coefficient of restitution with the wall is $e = 0.8$.

**Given:**
- $v_1 = 10$ m/s at 40° to the wall
- $e = 0.8$

**Find:** Speed and angle after rebound.

**Solution:**

Define axes: $n$ normal to wall, $t$ tangent to wall.

**Initial components:**
$$v_{1n} = 10\sin 40° = 6.43 \text{ m/s}, \quad v_{1t} = 10\cos 40° = 7.66 \text{ m/s}$$

**Tangential component (conserved, smooth wall):**
$$v_{2t} = v_{1t} = 7.66 \text{ m/s}$$

**Normal component (restitution):**
$$v_{2n} = e \cdot v_{1n} = 0.8(6.43) = 5.14 \text{ m/s}$$

**Rebound speed:**
$$v_2 = \sqrt{5.14^2 + 7.66^2} = 9.23 \text{ m/s}$$

**Rebound angle to wall:** $\alpha = \arctan(5.14/7.66) = 33.8°$ — shallower angle and lower speed than approach.

## Applications

### Crash Safety Engineering
- Vehicle collision analysis and crumple zone design
- Occupant kinematics during impact and airbag deployment timing

### Space and Ballistics Engineering
- Orbital maneuver calculations (delta-v budgets) and rocket staging
- Projectile penetration analysis and armor design

### Manufacturing and Sports
- Forging, stamping, and pile driving force estimation
- Ball-bat interactions and helmet impact protection design

## Practical Problem-Solving Tips

### 1. Identify the System and Time Interval
- Draw the system boundary to determine internal vs. external forces
- For impacts, the interval is the very short collision duration
- Internal forces cancel; only external impulses matter

### 2. Use Impulse-Momentum for Time-Dependent Problems
- When forces vary with time, integrate the force to find impulse
- For constant forces, impulse is simply $F \Delta t$
- Average impulsive force: $\bar{F} = \frac{\Delta(mv)}{\Delta t}$

### 3. Combine Methods for Multi-Phase Problems
- Impact phase: use impulse-momentum (momentum conserved)
- Post-impact phase: use work-energy (find heights, distances)
- This is the standard approach for ballistic pendulums and crash analysis

### 4. Handle Oblique Impact and Energy Loss
- Decompose velocities along and perpendicular to the line of impact
- Apply restitution only along the line of impact; tangential components are conserved for smooth surfaces
- Always compute kinetic energy before and after to quantify energy lost ($e < 1$ means energy loss)

Impulse-momentum methods are indispensable tools that complement Newton's second law and work-energy methods, completing the trio of fundamental approaches in classical dynamics.
