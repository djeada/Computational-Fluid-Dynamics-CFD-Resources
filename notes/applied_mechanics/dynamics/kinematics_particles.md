# Kinematics of Particles

Kinematics is the branch of mechanics that describes motion without considering the forces that cause it. For particles, we focus on position, velocity, and acceleration as functions of time, providing the foundation for understanding how objects move through space.

## Basic Definitions

### Position
The **position vector** $\mathbf{r}(t)$ describes the location of a particle relative to a fixed coordinate system:

$$\mathbf{r}(t) = x(t)\mathbf{i} + y(t)\mathbf{j} + z(t)\mathbf{k}$$

The **magnitude** of position (distance from origin):
$$r = |\mathbf{r}| = \sqrt{x^2 + y^2 + z^2}$$

### Displacement
**Displacement** is the change in position over a time interval:
$$\Delta \mathbf{r} = \mathbf{r}(t_2) - \mathbf{r}(t_1)$$

Note: Displacement is different from distance traveled—displacement is a vector representing the straight-line change in position.

### Velocity
**Average velocity** over a time interval:
$$\mathbf{v}_{avg} = \frac{\Delta \mathbf{r}}{\Delta t} = \frac{\mathbf{r}(t_2) - \mathbf{r}(t_1)}{t_2 - t_1}$$

**Instantaneous velocity** (first derivative of position):
$$\mathbf{v}(t) = \frac{d\mathbf{r}}{dt} = \dot{x}\mathbf{i} + \dot{y}\mathbf{j} + \dot{z}\mathbf{k}$$

**Speed** is the magnitude of velocity:
$$v = |\mathbf{v}| = \sqrt{\dot{x}^2 + \dot{y}^2 + \dot{z}^2}$$

### Acceleration
**Average acceleration** over a time interval:
$$\mathbf{a}_{avg} = \frac{\Delta \mathbf{v}}{\Delta t} = \frac{\mathbf{v}(t_2) - \mathbf{v}(t_1)}{t_2 - t_1}$$

**Instantaneous acceleration** (first derivative of velocity, second derivative of position):
$$\mathbf{a}(t) = \frac{d\mathbf{v}}{dt} = \frac{d^2\mathbf{r}}{dt^2} = \ddot{x}\mathbf{i} + \ddot{y}\mathbf{j} + \ddot{z}\mathbf{k}$$

## One-Dimensional Motion

For motion along a straight line (say, the x-axis):

### Position, Velocity, and Acceleration
- Position: $x(t)$
- Velocity: $v(t) = \frac{dx}{dt}$
- Acceleration: $a(t) = \frac{dv}{dt} = \frac{d^2x}{dt^2}$

### Kinematic Equations for Constant Acceleration

When acceleration is constant ($a = $ constant), we have:

1. **Velocity as function of time:**
   $$v(t) = v_0 + at$$

2. **Position as function of time:**
   $$x(t) = x_0 + v_0 t + \frac{1}{2}at^2$$

3. **Velocity-position relationship:**
   $$v^2 = v_0^2 + 2a(x - x_0)$$

4. **Average velocity:**
   $$v_{avg} = \frac{v_0 + v}{2}$$

### Example 1: Projectile Motion (Vertical)

A ball is thrown vertically upward with initial velocity $v_0 = 20$ m/s.

**Given:**
- Initial velocity: $v_0 = 20$ m/s (upward)
- Acceleration: $a = -g = -9.81$ m/s² (downward)
- Initial position: $y_0 = 0$

**Find:** Maximum height and time to return to ground.

**Solution:**

**Maximum height** occurs when $v = 0$:
$$0 = 20 - 9.81t_{max}$$
$$t_{max} = \frac{20}{9.81} = 2.04 \text{ s}$$

$$y_{max} = 0 + 20(2.04) + \frac{1}{2}(-9.81)(2.04)^2 = 20.4 \text{ m}$$

**Time to return to ground** ($y = 0$):
$$0 = 0 + 20t - \frac{1}{2}(9.81)t^2$$
$$t(20 - 4.905t) = 0$$
$$t = 0 \text{ or } t = \frac{20}{4.905} = 4.08 \text{ s}$$

## Two-Dimensional Motion

### Projectile Motion
For a projectile launched at angle $\theta_0$ with initial speed $v_0$:

**Initial conditions:**
- $x_0 = 0, y_0 = 0$
- $v_{0x} = v_0\cos\theta_0, v_{0y} = v_0\sin\theta_0$
- $a_x = 0, a_y = -g$

**Kinematic equations:**
$$x(t) = v_0\cos\theta_0 \cdot t$$
$$y(t) = v_0\sin\theta_0 \cdot t - \frac{1}{2}gt^2$$

$$v_x(t) = v_0\cos\theta_0$$
$$v_y(t) = v_0\sin\theta_0 - gt$$

**Trajectory equation** (eliminating time):
$$y = x\tan\theta_0 - \frac{gx^2}{2v_0^2\cos^2\theta_0}$$

**Key results:**
- **Range**: $R = \frac{v_0^2\sin(2\theta_0)}{g}$
- **Maximum height**: $H = \frac{v_0^2\sin^2\theta_0}{2g}$
- **Time of flight**: $T = \frac{2v_0\sin\theta_0}{g}$

### Example 2: Projectile Motion

A cannon fires a projectile at 45° with initial speed 100 m/s.

**Given:**
- $v_0 = 100$ m/s, $\theta_0 = 45°$
- $g = 9.81$ m/s²

**Solution:**

**Range:**
$$R = \frac{(100)^2\sin(2 \times 45°)}{9.81} = \frac{10000 \times 1}{9.81} = 1019 \text{ m}$$

**Maximum height:**
$$H = \frac{(100)^2\sin^2(45°)}{2 \times 9.81} = \frac{10000 \times 0.5}{19.62} = 255 \text{ m}$$

**Time of flight:**
$$T = \frac{2 \times 100 \times \sin(45°)}{9.81} = \frac{200 \times 0.707}{9.81} = 14.4 \text{ s}$$

## Curvilinear Motion

### Path-Dependent Description

For motion along a curved path, we use:

#### Tangential-Normal Coordinate System
- **Tangent direction** ($\mathbf{e}_t$): Along the path, in direction of motion
- **Normal direction** ($\mathbf{e}_n$): Perpendicular to path, toward center of curvature

**Velocity:**
$$\mathbf{v} = v\mathbf{e}_t$$
where $v$ is the speed (scalar).

**Acceleration:**
$$\mathbf{a} = a_t\mathbf{e}_t + a_n\mathbf{e}_n$$

where:
- **Tangential acceleration**: $a_t = \frac{dv}{dt}$ (changes speed)
- **Normal acceleration**: $a_n = \frac{v^2}{\rho}$ (changes direction)
- $\rho$ is the **radius of curvature**

### Circular Motion

For motion in a circle of radius $R$:

#### Uniform Circular Motion
- **Angular velocity**: $\omega = \frac{v}{R}$ (constant)
- **Centripetal acceleration**: $a_c = \frac{v^2}{R} = \omega^2 R$
- **Period**: $T = \frac{2\pi R}{v} = \frac{2\pi}{\omega}$

#### Non-uniform Circular Motion
- **Angular acceleration**: $\alpha = \frac{d\omega}{dt}$
- **Tangential acceleration**: $a_t = \alpha R$
- **Normal acceleration**: $a_n = \omega^2 R$
- **Total acceleration**: $a = \sqrt{a_t^2 + a_n^2}$

### Example 3: Circular Motion

A car travels around a circular track of radius 200 m. Its speed increases from 20 m/s to 30 m/s in 10 seconds.

**Given:**
- $R = 200$ m
- $v_1 = 20$ m/s, $v_2 = 30$ m/s
- $\Delta t = 10$ s

**Solution:**

**Tangential acceleration:**
$$a_t = \frac{v_2 - v_1}{\Delta t} = \frac{30 - 20}{10} = 1 \text{ m/s}^2$$

**Normal acceleration at $t = 0$:**
$$a_{n1} = \frac{v_1^2}{R} = \frac{20^2}{200} = 2 \text{ m/s}^2$$

**Normal acceleration at $t = 10$ s:**
$$a_{n2} = \frac{v_2^2}{R} = \frac{30^2}{200} = 4.5 \text{ m/s}^2$$

**Total acceleration at $t = 10$ s:**
$$a = \sqrt{a_t^2 + a_{n2}^2} = \sqrt{1^2 + 4.5^2} = 4.61 \text{ m/s}^2$$

## Relative Motion

### Relative Velocity
If particle A moves with velocity $\mathbf{v}_A$ and particle B with velocity $\mathbf{v}_B$, then:

**Velocity of A relative to B:**
$$\mathbf{v}_{A/B} = \mathbf{v}_A - \mathbf{v}_B$$

**Velocity of B relative to A:**
$$\mathbf{v}_{B/A} = \mathbf{v}_B - \mathbf{v}_A = -\mathbf{v}_{A/B}$$

### Relative Acceleration
$$\mathbf{a}_{A/B} = \mathbf{a}_A - \mathbf{a}_B$$

### Example 4: River Crossing

A boat can travel at 5 m/s in still water. It needs to cross a river that is 100 m wide with a current of 3 m/s.

**Case 1: Boat aims directly across**
- Boat velocity relative to water: $\mathbf{v}_{boat/water} = 5\mathbf{j}$ m/s
- Water velocity: $\mathbf{v}_{water} = 3\mathbf{i}$ m/s
- Boat velocity relative to ground: $\mathbf{v}_{boat} = 3\mathbf{i} + 5\mathbf{j}$ m/s

**Time to cross:**
$$t = \frac{100 \text{ m}}{5 \text{ m/s}} = 20 \text{ s}$$

**Downstream drift:**
$$x = 3 \times 20 = 60 \text{ m}$$

**Case 2: Boat aims to go straight across**
The boat must aim upstream at angle $\theta$:
$$\sin\theta = \frac{3}{5}$$
$$\theta = 36.87°$$

Effective velocity across river: $v_{across} = 5\cos\theta = 4$ m/s
Time to cross: $t = \frac{100}{4} = 25$ s

## Variable Acceleration

When acceleration is not constant, integration is required:

### Given $a(t)$:
$$v(t) = v_0 + \int_0^t a(\tau) d\tau$$
$$x(t) = x_0 + \int_0^t v(\tau) d\tau$$

### Given $a(v)$:
Using $a = v\frac{dv}{dx}$:
$$v dv = a dx$$
$$\int_{v_0}^v v' dv' = \int_{x_0}^x a dx'$$

### Given $a(x)$:
$$v^2 = v_0^2 + 2\int_{x_0}^x a dx'$$

### Example 5: Variable Acceleration

A particle starts from rest and has acceleration $a(t) = 2 + 3t$ m/s².

**Find:** Velocity and position after 4 seconds.

**Solution:**

**Velocity:**
$$v(t) = 0 + \int_0^t (2 + 3\tau) d\tau = [2\tau + \frac{3\tau^2}{2}]_0^t = 2t + 1.5t^2$$

At $t = 4$ s: $v(4) = 2(4) + 1.5(4)^2 = 8 + 24 = 32$ m/s

**Position:**
$$x(t) = 0 + \int_0^t (2\tau + 1.5\tau^2) d\tau = [\tau^2 + 0.5\tau^3]_0^t = t^2 + 0.5t^3$$

At $t = 4$ s: $x(4) = (4)^2 + 0.5(4)^3 = 16 + 32 = 48$ m

## Parametric Equations

Sometimes motion is described parametrically:
$$x = x(t), \quad y = y(t), \quad z = z(t)$$

**Velocity components:**
$$v_x = \frac{dx}{dt}, \quad v_y = \frac{dy}{dt}, \quad v_z = \frac{dz}{dt}$$

**Speed:**
$$v = \sqrt{v_x^2 + v_y^2 + v_z^2}$$

**Acceleration components:**
$$a_x = \frac{dv_x}{dt}, \quad a_y = \frac{dv_y}{dt}, \quad a_z = \frac{dv_z}{dt}$$

## Applications in Engineering

### Vehicle Dynamics
- Braking distance calculations
- Cornering analysis
- Acceleration performance

### Robotics
- Path planning for robotic manipulators
- Trajectory optimization
- Motion control systems

### Aerospace
- Satellite orbit calculations
- Aircraft flight path analysis
- Rocket trajectory design

### Manufacturing
- Machining tool path generation
- Conveyor system design
- Automated assembly line motion

## Practical Problem-Solving Tips

### 1. Choose Appropriate Coordinate System
- Align axes with motion when possible
- Use tangential-normal for curved paths
- Consider symmetry in the problem

### 2. Identify Motion Type
- Constant acceleration: Use kinematic equations
- Circular motion: Use angular quantities
- General motion: Use calculus methods

### 3. Set Up Initial Conditions
- Clearly define $t = 0$ reference
- Establish position and velocity at $t = 0$
- Be consistent with sign conventions

### 4. Work with Components
- Break vectors into components
- Solve each direction independently
- Combine results for final answer

### 5. Check Units and Reasonableness
- Verify dimensional consistency
- Check if results make physical sense
- Compare with known benchmarks

Understanding particle kinematics is essential for:
- Dynamics analysis (adding force considerations)
- Mechanism design and analysis
- Control system development
- Safety and performance optimization

This foundation in describing motion prepares for the next step: understanding why objects move as they do through the study of kinetics, where forces and motion are related.
