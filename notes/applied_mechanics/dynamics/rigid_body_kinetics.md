# Rigid Body Kinetics

Rigid body kinetics extends Newton's laws from particles to bodies with finite size and shape. Both translational and rotational equations of motion must be considered, introducing the mass moment of inertia as the rotational analog of mass.

## Mass Moment of Inertia

The **mass moment of inertia** quantifies a body's resistance to angular acceleration about a given axis:

$$I = \int_m r^2 \, dm$$

where $r$ is the perpendicular distance from the axis to the element $dm$.

### Common Shapes

| Shape | Axis | Moment of Inertia |
|-------|------|-------------------|
| Slender rod (length $L$) | Through center, perpendicular | $\frac{1}{12}mL^2$ |
| Slender rod (length $L$) | Through end, perpendicular | $\frac{1}{3}mL^2$ |
| Thin disk/cylinder (radius $R$) | Through center, perpendicular to face | $\frac{1}{2}mR^2$ |
| Solid sphere (radius $R$) | Through center | $\frac{2}{5}mR^2$ |
| Thin-walled hollow sphere (radius $R$) | Through center | $\frac{2}{3}mR^2$ |
| Rectangular plate ($a \times b$) | Through center, perpendicular to plate | $\frac{1}{12}m(a^2 + b^2)$ |

### Parallel-Axis Theorem

If $I_G$ is the moment of inertia about an axis through the mass center $G$, then the moment about a parallel axis at distance $d$ is:

$$I = I_G + md^2$$

### Radius of Gyration

The radius of gyration $k$ satisfies $I = mk^2$:

$$k = \sqrt{\frac{I}{m}}$$

## Equations of Motion for Rigid Bodies

For a rigid body in plane motion, three independent scalar equations govern the dynamics:

$$\sum F_x = m(a_G)_x$$

$$\sum F_y = m(a_G)_y$$

$$\sum M_G = I_G \alpha$$

where $G$ is the mass center, $a_G$ is the acceleration of the mass center, and $\alpha$ is the angular acceleration. Alternatively, moments can be summed about any point $P$:

$$\sum M_P = I_G \alpha + m \mathbf{r}_{G/P} \times \mathbf{a}_G$$

## Special Cases of Plane Motion

### Pure Translation ($\alpha = 0$, $\omega = 0$)

All points have the same acceleration. The moment equation simplifies to:

$$\sum M_G = 0 \quad \text{(if no angular acceleration)}$$

Forces may still produce a net moment about points other than $G$.

### Rotation About a Fixed Axis

For rotation about a fixed point $O$:

$$\sum M_O = I_O \alpha$$

where $I_O = I_G + md^2$ and $d$ is the distance from $O$ to $G$. The mass center has both tangential and normal acceleration:

$$(\mathbf{a}_G)_t = \alpha \, d, \quad (\mathbf{a}_G)_n = \omega^2 d$$

### General Plane Motion

All three equations are needed simultaneously. The mass center translates while the body rotates:

$$\sum F_x = m(a_G)_x, \quad \sum F_y = m(a_G)_y, \quad \sum M_G = I_G \alpha$$

Kinematic constraints (e.g., rolling without slipping: $a_G = \alpha R$) provide additional relationships.

## D'Alembert's Principle for Rigid Bodies

D'Alembert's principle introduces an **inertia force** $-m\mathbf{a}_G$ at the mass center and an **inertia couple** $-I_G\alpha$:

$$\sum \mathbf{F} + (-m\mathbf{a}_G) = \mathbf{0}$$

$$\sum M_G + (-I_G \alpha) = 0$$

This converts the dynamic problem into a pseudo-static equilibrium, allowing the use of static equilibrium techniques.

## Worked Examples

### Example 1: Rolling Cylinder on an Incline

A solid cylinder of mass 8 kg and radius 0.2 m rolls without slipping down a 25° incline.

**Given:**
- $m = 8$ kg, $R = 0.2$ m, $\theta = 25°$
- Rolling without slipping: $a_G = \alpha R$
- $I_G = \frac{1}{2}mR^2 = \frac{1}{2}(8)(0.04) = 0.16$ kg·m²

**Find:** Acceleration of the center and the friction force.

**Solution:**

**Force equation along the incline** (positive down the slope):
$$mg\sin\theta - f = ma_G$$
$$8(9.81)\sin 25° - f = 8a_G$$
$$33.15 - f = 8a_G \quad \text{...(1)}$$

**Moment equation about $G$:**
$$fR = I_G \alpha = I_G \frac{a_G}{R}$$
$$f(0.2) = 0.16 \frac{a_G}{0.2}$$
$$f = 4a_G \quad \text{...(2)}$$

Substituting (2) into (1):
$$33.15 - 4a_G = 8a_G$$
$$a_G = \frac{33.15}{12} = 2.76 \text{ m/s}^2$$

$$f = 4(2.76) = 11.05 \text{ N}$$

Note: The acceleration is $\frac{2}{3}g\sin\theta$, less than that of a sliding block ($g\sin\theta$), because energy goes into rotation.

### Example 2: Simple Pendulum (Compound)

A uniform rod of mass 3 kg and length 1.2 m is pivoted at one end and released from a horizontal position.

**Given:**
- $m = 3$ kg, $L = 1.2$ m
- $I_O = \frac{1}{3}mL^2 = \frac{1}{3}(3)(1.44) = 1.44$ kg·m²
- Released from horizontal ($\theta = 0$)

**Find:** Angular acceleration immediately after release and angular velocity at the vertical position.

**Solution:**

**At $\theta = 0$ (horizontal):**

Taking moments about pivot $O$:
$$mg\frac{L}{2} = I_O \alpha$$
$$3(9.81)(0.6) = 1.44\alpha$$
$$\alpha = \frac{17.66}{1.44} = 12.26 \text{ rad/s}^2$$

**Angular velocity at vertical ($\theta = 90°$):**

Using energy methods (gravity does work as the center of mass drops $L/2$):
$$mg\frac{L}{2} = \frac{1}{2}I_O \omega^2$$
$$3(9.81)(0.6) = \frac{1}{2}(1.44)\omega^2$$
$$\omega = \sqrt{\frac{2(17.66)}{1.44}} = 4.95 \text{ rad/s}$$

### Example 3: Pulley with Hanging Masses

A solid disk pulley of mass 4 kg and radius 0.15 m supports two masses: $m_1 = 6$ kg and $m_2 = 4$ kg connected by a cord.

**Given:**
- Pulley: $m_p = 4$ kg, $R = 0.15$ m, $I_p = \frac{1}{2}m_p R^2 = 0.045$ kg·m²
- $m_1 = 6$ kg, $m_2 = 4$ kg

**Find:** Acceleration of the masses and tension in each cord segment.

**Solution:**

Let $a$ be the downward acceleration of $m_1$ (upward for $m_2$), and $\alpha = a/R$.

**Mass 1** (moving down): $m_1 g - T_1 = m_1 a$
$$6(9.81) - T_1 = 6a \quad \text{...(1)}$$

**Mass 2** (moving up): $T_2 - m_2 g = m_2 a$
$$T_2 - 4(9.81) = 4a \quad \text{...(2)}$$

**Pulley** (rotation): $T_1 R - T_2 R = I_p \alpha = I_p \frac{a}{R}$
$$T_1 - T_2 = \frac{I_p a}{R^2} = \frac{0.045a}{0.0225} = 2a \quad \text{...(3)}$$

Adding equations (1), (2), (3):
$$(6)(9.81) - (4)(9.81) = (6 + 4 + 2)a$$
$$19.62 = 12a$$
$$a = 1.635 \text{ m/s}^2$$

From (1): $T_1 = 58.86 - 6(1.635) = 49.05$ N
From (2): $T_2 = 39.24 + 4(1.635) = 45.78$ N

## Applications

### Automotive Engineering
- Wheel dynamics during braking and acceleration
- Drivetrain torque analysis
- Vehicle rollover stability

### Industrial Machinery
- Flywheel energy storage and speed regulation
- Gear train torque and speed calculations
- Conveyor system motor sizing

### Structural Engineering
- Wind load response of tall structures
- Seismic analysis of buildings
- Crane boom dynamics during lifting operations

### Aerospace
- Satellite attitude control and spin stabilization
- Helicopter rotor dynamics
- Control surface effectiveness

## Practical Problem-Solving Tips

### 1. Always Draw a Free-Body Diagram and Kinetic Diagram
- The FBD shows all external forces and couples
- The kinetic diagram shows $m\mathbf{a}_G$ and $I_G\alpha$
- These two diagrams together embody the equations of motion

### 2. Choose the Moment Center Wisely
- Summing moments about a fixed pivot eliminates unknown reactions
- Summing about the mass center separates translation from rotation
- Summing about the contact point of a rolling body can simplify algebra

### 3. Apply Kinematic Constraints
- Rolling without slipping: $a_G = \alpha R$
- Cord wrapped around pulley: $a = \alpha R$
- Connected bodies share acceleration at their connection points

### 4. Check the Friction Assumption
- For rolling without slipping, verify $f \leq \mu_s N$
- If violated, the body slips and $f = \mu_k N$ with $a_G \neq \alpha R$

### 5. Use Energy or Momentum for Efficiency
- If only final velocities are needed, work-energy methods avoid solving for accelerations
- For impacts, impulse-momentum methods are more direct

Rigid body kinetics provides the tools for analyzing real-world mechanical systems, from simple pendulums to complex machinery, and forms the basis for multibody dynamics and finite element analysis.
