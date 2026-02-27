# Rigid Body Kinematics

Rigid body kinematics describes the motion of bodies that do not deform, accounting for both translation and rotation. Unlike particle kinematics, every point in a rigid body can have a different velocity and acceleration, making the analysis richer and more complex.

## Types of Rigid Body Motion

### Translation
Every line segment in the body remains parallel to its original orientation. All points have the **same** velocity and acceleration:

$$\mathbf{v}_B = \mathbf{v}_A, \quad \mathbf{a}_B = \mathbf{a}_A$$

Translation can be rectilinear (straight-line) or curvilinear (curved path).

### Rotation About a Fixed Axis
The body revolves around a stationary line. All points move in circular arcs centered on the axis.

### General Plane Motion
A combination of translation and rotation in a single plane, such as a wheel rolling along a surface. This is the most general type of planar motion.

## Rotation About a Fixed Axis

### Angular Quantities

**Angular position:** $\theta(t)$ (rad)

**Angular velocity:**
$$\omega = \frac{d\theta}{dt} = \dot{\theta}$$

**Angular acceleration:**
$$\alpha = \frac{d\omega}{dt} = \ddot{\theta}$$

### Constant Angular Acceleration

Analogous to rectilinear kinematics with constant linear acceleration:

$$\omega = \omega_0 + \alpha t$$

$$\theta = \theta_0 + \omega_0 t + \frac{1}{2}\alpha t^2$$

$$\omega^2 = \omega_0^2 + 2\alpha(\theta - \theta_0)$$

### Velocity and Acceleration of a Point

For a point at distance $r$ from the axis of rotation:

**Velocity** (tangential only):
$$v = \omega r$$

In vector form: $\mathbf{v} = \boldsymbol{\omega} \times \mathbf{r}$

**Acceleration:**
$$a_t = \alpha r \quad \text{(tangential)}, \quad a_n = \omega^2 r \quad \text{(centripetal)}$$

$$\mathbf{a} = \boldsymbol{\alpha} \times \mathbf{r} + \boldsymbol{\omega} \times (\boldsymbol{\omega} \times \mathbf{r})$$

## Relative Velocity — General Plane Motion

For two points $A$ and $B$ on the same rigid body undergoing general plane motion:

$$\mathbf{v}_B = \mathbf{v}_A + \boldsymbol{\omega} \times \mathbf{r}_{B/A}$$

where:
- $\mathbf{v}_A$ is the velocity of the reference point $A$
- $\boldsymbol{\omega}$ is the angular velocity of the body
- $\mathbf{r}_{B/A}$ is the position vector from $A$ to $B$

In scalar form for planar motion:

$$v_{Bx} = v_{Ax} - \omega \, r_{B/A,y}$$

$$v_{By} = v_{Ay} + \omega \, r_{B/A,x}$$

## Instantaneous Center of Zero Velocity

The **instantaneous center (IC)** is a point (which may lie outside the body) that has zero velocity at a given instant. Every point's velocity can then be computed as pure rotation about the IC:

$$v_P = \omega \, d_P$$

where $d_P$ is the distance from $P$ to the IC.

### Locating the IC
1. **Two known velocity directions:** The IC lies at the intersection of lines drawn perpendicular to each velocity vector.
2. **Two parallel velocities (same direction):** The IC lies on the line connecting the two points, at a distance determined by the ratio of speeds.
3. **Two parallel velocities (opposite directions):** The IC lies on the extension of the line connecting the two points, between or outside them.

## Relative Acceleration

For two points on the same rigid body:

$$\mathbf{a}_B = \mathbf{a}_A + \boldsymbol{\alpha} \times \mathbf{r}_{B/A} + \boldsymbol{\omega} \times (\boldsymbol{\omega} \times \mathbf{r}_{B/A})$$

The last two terms can be decomposed into:
- **Tangential component**: $(\mathbf{a}_{B/A})_t = \boldsymbol{\alpha} \times \mathbf{r}_{B/A}$, magnitude $= \alpha \, r_{B/A}$
- **Normal component**: $(\mathbf{a}_{B/A})_n = \boldsymbol{\omega} \times (\boldsymbol{\omega} \times \mathbf{r}_{B/A})$, magnitude $= \omega^2 r_{B/A}$, directed from $B$ toward $A$

## Worked Examples

### Example 1: Rotating Disk

A disk of radius 0.5 m starts from rest and accelerates uniformly at $\alpha = 4$ rad/s².

**Given:**
- $r = 0.5$ m, $\omega_0 = 0$, $\alpha = 4$ rad/s²

**Find:** Velocity and acceleration of a point on the rim after 3 seconds.

**Solution:**

**Angular velocity at $t = 3$ s:**
$$\omega = 0 + 4(3) = 12 \text{ rad/s}$$

**Velocity of rim point:**
$$v = \omega r = 12(0.5) = 6 \text{ m/s}$$

**Tangential acceleration:**
$$a_t = \alpha r = 4(0.5) = 2 \text{ m/s}^2$$

**Normal (centripetal) acceleration:**
$$a_n = \omega^2 r = (12)^2(0.5) = 72 \text{ m/s}^2$$

**Total acceleration:**
$$a = \sqrt{a_t^2 + a_n^2} = \sqrt{4 + 5184} = 72.03 \text{ m/s}^2$$

### Example 2: Slider-Crank Mechanism

A crank $OA$ of length 0.1 m rotates at constant $\omega_{OA} = 10$ rad/s. The connecting rod $AB$ has length 0.3 m. At the instant when crank angle $\theta = 90°$, find the velocity of the piston $B$.

**Given:**
- $OA = 0.1$ m, $AB = 0.3$ m
- $\omega_{OA} = 10$ rad/s, $\theta = 90°$

**Find:** Velocity of piston $B$ (constrained to slide horizontally).

**Solution:**

**Velocity of point $A$:**
$$v_A = \omega_{OA} \times OA = 10(0.1) = 1 \text{ m/s}$$

At $\theta = 90°$, point $A$ is directly above $O$, so $\mathbf{v}_A$ is directed horizontally (to the left if $\omega$ is counterclockwise).

**Geometry at $\theta = 90°$:**
Point $A$ is at $(0, 0.1)$ relative to $O$. The rod $AB$ connects to $B$ on the horizontal axis.

$$AB\sin\phi = OA, \quad \sin\phi = \frac{0.1}{0.3} = \frac{1}{3}, \quad \phi = 19.47°$$

Using the relative velocity equation $\mathbf{v}_B = \mathbf{v}_A + \boldsymbol{\omega}_{AB} \times \mathbf{r}_{B/A}$:

Since $B$ moves only horizontally and $\mathbf{v}_A$ is horizontal, equating the vertical components gives $\omega_{AB}$, then the horizontal components give $v_B$:

$$v_B = v_A - \omega_{AB} \cdot AB\cos\phi$$

Vertical: $0 = 0 + \omega_{AB} \cdot AB\sin\phi \implies$ this confirms the geometric constraint.

Solving the vector equation yields:
$$v_B = v_A \cdot \frac{\cos\phi}{\cos\phi} - \omega_{AB} \cdot AB\cos\phi$$

After resolving components: $v_B \approx 0.943$ m/s (toward the right).

### Example 3: Rolling Wheel (IC Method)

A wheel of radius 0.4 m rolls without slipping along a flat surface. The center has velocity $v_C = 2$ m/s to the right.

**Given:**
- $R = 0.4$ m, $v_C = 2$ m/s

**Find:** Angular velocity and velocity of the top of the wheel.

**Solution:**

For rolling without slipping, the contact point with the ground is the IC (zero velocity).

**Angular velocity:**
$$\omega = \frac{v_C}{R} = \frac{2}{0.4} = 5 \text{ rad/s}$$

**Velocity of the top point** (distance $2R$ from IC):
$$v_{top} = \omega(2R) = 5(0.8) = 4 \text{ m/s (to the right)}$$

The top of a rolling wheel always moves at twice the speed of the center.

## Applications in Mechanism Analysis

### Linkage Mechanisms
- Four-bar linkages in industrial machinery
- Quick-return mechanisms in shapers and planers
- Pantograph mechanisms for scaling motion

### Gear Systems
- Speed and torque relationships between meshing gears
- Planetary gear trains with compound motion
- Differential mechanisms in vehicles

### Cam-Follower Systems
- Valve timing in internal combustion engines
- Motion programming for automated machines
- Profile design for desired follower motion

### Robotics
- Forward and inverse kinematics of robotic arms
- End-effector velocity and workspace analysis
- Motion planning for multi-joint manipulators

## Practical Problem-Solving Tips

### 1. Identify the Type of Motion
- Pure translation: all points share the same velocity
- Fixed-axis rotation: velocities scale with distance from axis
- General plane motion: use relative velocity methods or IC

### 2. Use the IC for Velocity Problems
- Faster than vector equations for finding velocities
- Remember the IC changes position from instant to instant
- Cannot be used directly for acceleration analysis

### 3. Apply Relative Equations Systematically
- Choose a reference point whose motion is known or simple
- Write the vector equation, then resolve into components
- Use geometry to relate angles and distances

### 4. Relate Constraints to Kinematics
- Rolling without slipping: $v_C = \omega R$ and $a_C = \alpha R$
- Pin connections: points on both bodies share the same velocity
- Sliding contacts: relative velocity is along the contact surface

### 5. Verify with Independent Methods
- Check velocity results from relative equations against the IC method
- Ensure angular velocity is consistent across all point pairs on the same body
- Confirm that constraint conditions are satisfied

Rigid body kinematics provides the motion description needed for kinetics, where forces and moments are related to the translational and rotational accelerations of the body.
