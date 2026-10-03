# Rigid Body Kinematics

Rigid body kinematics describes the motion of bodies that do not deform, accounting for both translation and rotation. Unlike particle kinematics, every point in a rigid body can have a different velocity and acceleration, making the analysis richer and more complex.

## Types of Rigid Body Motion

### Translation

Every line segment in the body remains parallel to its original orientation. All points have the **same** velocity and acceleration:

$$
\mathbf{v}_B = \mathbf{v}_A, \quad \mathbf{a}_B = \mathbf{a}_A
$$

Translation can be rectilinear (straight-line) or curvilinear (curved path).

### Rotation About a Fixed Axis

The body revolves around a stationary line. All points move in circular arcs centered on the axis.

### General Plane Motion

A combination of translation and rotation in a single plane, such as a wheel rolling along a surface. This is the most general type of planar motion.

## Rotation About a Fixed Axis

### Angular Quantities

**Angular position:** $\theta(t)$ (rad)

**Angular velocity:**

$$
\omega = \frac{d\theta}{dt} = \dot{\theta}
$$

**Angular acceleration:**

$$
\alpha = \frac{d\omega}{dt} = \ddot{\theta}
$$

### Constant Angular Acceleration

Analogous to rectilinear kinematics with constant linear acceleration:

$$
\omega = \omega_0 + \alpha t
$$

$$
\theta = \theta_0 + \omega_0 t + \frac{1}{2}\alpha t^2
$$

$$
\omega^2 = \omega_0^2 + 2\alpha(\theta - \theta_0)
$$

### Velocity and Acceleration of a Point

For a point at distance $r$ from the axis of rotation:

**Velocity** (tangential only):

$$
v = \omega r
$$

In vector form: $\mathbf{v} = \boldsymbol{\omega} \times \mathbf{r}$

**Acceleration:**

$$
a_t = \alpha r \quad \text{(tangential)}, \quad a_n = \omega^2 r \quad
\text{(centripetal)}
$$

$$
\mathbf{a} = \boldsymbol{\alpha} \times \mathbf{r} + \boldsymbol{\omega} \times
(\boldsymbol{\omega} \times \mathbf{r})
$$

## Relative Velocity — General Plane Motion

For two points $A$ and $B$ on the same rigid body undergoing general plane motion:

$$
\mathbf{v}_B = \mathbf{v}_A + \boldsymbol{\omega} \times \mathbf{r}_{B/A}
$$

where:

- $\mathbf{v}_A$ is the velocity of the reference point $A$
- $\boldsymbol{\omega}$ is the angular velocity of the body
- $\mathbf{r}_{B/A}$ is the position vector from $A$ to $B$

In scalar form for planar motion:

$$
v_{Bx} = v_{Ax} - \omega \, r_{B/A,y}
$$

$$
v_{By} = v_{Ay} + \omega \, r_{B/A,x}
$$

## Instantaneous Center of Zero Velocity

The **instantaneous center (IC)** is a point (which may lie outside the body) that has zero velocity at a given instant. Every point's velocity can then be computed as pure rotation about the IC:

$$
v_P = \omega \, d_P
$$

where $d_P$ is the distance from $P$ to the IC.

### Locating the IC

1. **Two known velocity directions:** The IC lies at the intersection of lines drawn perpendicular to each velocity vector.
2. **Two parallel velocities (same direction, unequal speeds):** The IC lies on the line through the two points (perpendicular to the velocities), outside the segment between them, at distances proportional to the speeds. If the speeds are equal, the IC is at infinity and the body is instantaneously translating.
3. **Two parallel velocities (opposite directions):** The IC lies on the line connecting the two points, between them, at distances proportional to the speeds.

## Relative Acceleration

For two points on the same rigid body:

$$
\mathbf{a}_B = \mathbf{a}_A + \boldsymbol{\alpha} \times \mathbf{r}_{B/A} +
\boldsymbol{\omega} \times (\boldsymbol{\omega} \times \mathbf{r}_{B/A})
$$

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

$$
\omega = 0 + 4(3) = 12 \text{ rad/s}
$$

**Velocity of rim point:**

$$
v = \omega r = 12(0.5) = 6 \text{ m/s}
$$

**Tangential acceleration:**

$$
a_t = \alpha r = 4(0.5) = 2 \text{ m/s}^2
$$

**Normal (centripetal) acceleration:**

$$
a_n = \omega^2 r = (12)^2(0.5) = 72 \text{ m/s}^2
$$

**Total acceleration:**

$$
a = \sqrt{a_t^2 + a_n^2} = \sqrt{4 + 5184} = 72.03 \text{ m/s}^2
$$

### Example 2: Slider-Crank Mechanism

A crank $OA$ of length 0.1 m rotates at constant $\omega_{OA} = 10$ rad/s. The connecting rod $AB$ has length 0.3 m. At the instant when crank angle $\theta = 90^\circ$, find the velocity of the piston $B$.

**Given:**

- $OA = 0.1$ m, $AB = 0.3$ m
- $\omega_{OA} = 10$ rad/s, $\theta = 90^\circ$

**Find:** Velocity of piston $B$ (constrained to slide horizontally).

**Solution:**

**Velocity of point $A$:**

$$
v_A = \omega_{OA} \times OA = 10(0.1) = 1 \text{ m/s}
$$

At $\theta = 90^\circ$, point $A$ is directly above $O$, so $\mathbf{v}_A$ is directed horizontally (to the left if $\omega$ is counterclockwise).

**Geometry at $\theta = 90^\circ$:**
Point $A$ is at $(0, 0.1)$ relative to $O$. The rod $AB$ connects to $B$ on the horizontal axis.

$$
AB\sin\phi = OA, \quad \sin\phi = \frac{0.1}{0.3} = \frac{1}{3}, \quad
\phi = 19.47^\circ
$$

Using the relative velocity equation $\mathbf{v}_B = \mathbf{v}_A + \boldsymbol{\omega}_{AB} \times \mathbf{r}_{B/A}$ with a counterclockwise crank, $\mathbf{v}_A = -1\,\mathbf{i}$ m/s, $\mathbf{v}_B = v_B\,\mathbf{i}$ and $\mathbf{r}_{B/A} = AB\cos\phi\,\mathbf{i} - OA\,\mathbf{j} = 0.283\,\mathbf{i} - 0.1\,\mathbf{j}$ m:

$$
v_B\,\mathbf{i} = -1\,\mathbf{i} + \omega_{AB}\mathbf{k} \times
(0.283\,\mathbf{i} - 0.1\,\mathbf{j}) = (-1 + 0.1\,\omega_{AB})\,\mathbf{i} +
0.283\,\omega_{AB}\,\mathbf{j}
$$

Vertical ($\mathbf{j}$) components: $0 = 0.283\,\omega_{AB} \implies \omega_{AB} = 0$.

Horizontal ($\mathbf{i}$) components: $v_B = -1$ m/s.

At this instant $\mathbf{v}_A$ and $\mathbf{v}_B$ are parallel, so the IC of rod $AB$ is at infinity and the rod translates: the piston moves at $1$ m/s in the same direction as $A$ (to the left for a counterclockwise crank).

### Example 3: Rolling Wheel (IC Method)

A wheel of radius 0.4 m rolls without slipping along a flat surface. The center has velocity $v_C = 2$ m/s to the right.

**Given:**

- $R = 0.4$ m, $v_C = 2$ m/s

**Find:** Angular velocity and velocity of the top of the wheel.

**Solution:**

For rolling without slipping, the contact point with the ground is the IC (zero velocity).

**Angular velocity:**

$$
\omega = \frac{v_C}{R} = \frac{2}{0.4} = 5 \text{ rad/s}
$$

**Velocity of the top point** (distance $2R$ from IC):

$$
v_{top} = \omega(2R) = 5(0.8) = 4 \text{ m/s (to the right)}
$$

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

## Exercises

**Exercise 1.** A flywheel turning at 1800 rpm decelerates uniformly to rest in 30 s. Find its angular acceleration and the number of revolutions it makes while stopping.

<details>
<summary>Answer</summary>

$\omega_0 = 1800 \times 2\pi/60 = 188.5$ rad/s, so $\alpha = -188.5/30 = -6.28$ rad/s².

$$
\theta = \frac{\omega_0 t}{2} = \frac{188.5 \times 30}{2} = 2827 \text{ rad} = 450
\text{ rev}
$$

</details>

**Exercise 2.** A wheel of radius 0.3 m rolls without slipping to the right with centre speed 3 m/s. Use the instantaneous centre to find the velocity of the point on the front of the rim level with the centre.

<details>
<summary>Answer</summary>

$\omega = v_C/R = 10$ rad/s (clockwise), with the IC at the contact point. The point is at $(R, R)$ relative to the IC, a distance $\sqrt{2}R = 0.424$ m away.

$$
v = \omega \sqrt{2}R = 10 \times 0.424 = 4.24 \text{ m/s}
$$

It is directed perpendicular to the line from the IC: $45^\circ$ below the horizontal, forward and down. Its components are $(3, -3)$ m/s.

</details>

**Exercise 3.** For the slider-crank of Example 2 ($OA = 0.1$ m, $AB = 0.3$ m, $\omega_{OA} = 10$ rad/s), find $v_B$ and $\omega_{AB}$ at $\theta = 0$, when $A$ lies on the line $OB$.

<details>
<summary>Answer</summary>

$\mathbf{v}_A$ is perpendicular to $OA$ (vertical, 1 m/s), and $\mathbf{v}_B$ is horizontal. The line through $A$ perpendicular to $\mathbf{v}_A$ is $OB$ itself, and the line through $B$ perpendicular to $\mathbf{v}_B$ is vertical. They intersect at $B$, so $B$ is the IC of rod $AB$.

Hence $v_B = 0$ (dead-centre position) and $\omega_{AB} = v_A/AB = 1/0.3 = 3.33$ rad/s.

</details>

**Exercise 4.** A wheel of radius $R = 0.4$ m rolls without slipping. At an instant its centre has $v_C = 2$ m/s and $a_C = 1.2$ m/s², both to the right. Find the accelerations of the top point and of the contact point.

<details>
<summary>Answer</summary>

$\omega = v_C/R = 5$ rad/s and $\alpha = a_C/R = 3$ rad/s² (both clockwise). Using $\mathbf{a}_P = \mathbf{a}_C + \boldsymbol{\alpha} \times \mathbf{r}_{P/C} - \omega^2\mathbf{r}_{P/C}$:

- Top point ($\mathbf{r} = R\mathbf{j}$): $\mathbf{a} = (1.2 + \alpha R)\mathbf{i} - \omega^2 R\,\mathbf{j} = 2.4\mathbf{i} - 10\mathbf{j}$ m/s², magnitude 10.3 m/s².
- Contact point ($\mathbf{r} = -R\mathbf{j}$): $\mathbf{a} = (1.2 - \alpha R)\mathbf{i} + \omega^2 R\,\mathbf{j} = 10\mathbf{j}$ m/s², directed toward the centre.

The contact point has zero velocity but not zero acceleration, which is why the IC cannot be used for acceleration analysis.

</details>

**Exercise 5.** For the slider-crank of Example 2, derive $v_B$ as a function of the crank angle $\theta$ from the position $x_B = OA\cos\theta + \sqrt{AB^2 - OA^2\sin^2\theta}$. Evaluate $v_B$ and $\omega_{AB}$ at $\theta = 60^\circ$, and check the formula against the $\theta = 90^\circ$ result.

<details>
<summary>Answer</summary>

Differentiating with $\dot{\theta} = \omega$ and $r = OA$, $l = AB$:

$$
v_B = -r\omega\sin\theta -
\frac{r^2\omega\sin\theta\cos\theta}{\sqrt{l^2 - r^2\sin^2\theta}}
$$

At $\theta = 60^\circ$: $\sqrt{0.09 - 0.0075} = 0.2872$ m, so $v_B = -0.866 - 0.151 = -1.017$ m/s, i.e. 1.02 m/s toward $O$.

The rod angle $\phi$ below the horizontal satisfies $l\sin\phi = r\sin\theta$, so $\omega_{AB} = \dot{\phi} = \frac{r\omega\cos\theta}{l\cos\phi} = \frac{0.1 \times 10 \times 0.5}{0.2872} = 1.74$ rad/s (clockwise).

At $\theta = 90^\circ$ the second term vanishes and $v_B = -r\omega = -1$ m/s with $\omega_{AB} = 0$, which agrees with Example 2.

</details>

## References

- R. C. Hibbeler, *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- J. L. Meriam, L. G. Kraige, *Engineering Mechanics: Dynamics*, Wiley.
- F. P. Beer, E. R. Johnston, P. J. Cornwell, *Vector Mechanics for Engineers: Dynamics*, McGraw-Hill.
