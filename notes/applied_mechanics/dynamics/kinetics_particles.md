# Kinetics of Particles

Kinetics relates the forces acting on a particle to its resulting motion. Building on kinematics, we now apply Newton's laws to predict how particles accelerate under the influence of external forces, forming the core of classical mechanics.

## Newton's Laws of Motion

### First Law (Inertia)

A particle remains at rest or in uniform rectilinear motion unless acted upon by an unbalanced force.

### Second Law (Fundamental Equation)

The acceleration of a particle is proportional to the net force and inversely proportional to its mass:

$$
\sum \mathbf{F} = m\mathbf{a}
$$

In component form:

$$
\sum F_x = m a_x, \quad \sum F_y = m a_y, \quad \sum F_z = m a_z
$$

### Third Law (Action-Reaction)

For every action there is an equal and opposite reaction: $\mathbf{F}_{AB} = -\mathbf{F}_{BA}$.

## Equations of Motion in Different Coordinate Systems

### Cartesian Coordinates

Best suited for problems where forces align naturally with rectangular axes:

$$
\sum F_x = m\ddot{x}, \quad \sum F_y = m\ddot{y}, \quad \sum F_z = m\ddot{z}
$$

### Normal-Tangential Coordinates

Ideal for curved-path motion where the path geometry is known:

$$
\sum F_t = m a_t = m \frac{dv}{dt}
$$

$$
\sum F_n = m a_n = m \frac{v^2}{\rho}
$$

where $\rho$ is the radius of curvature. The tangential component changes the speed, while the normal component changes the direction.

### Polar (Cylindrical) Coordinates

Useful for problems with radial symmetry, such as orbital or rotating-arm motion:

$$
\sum F_r = m(\ddot{r} - r\dot{\theta}^2)
$$

$$
\sum F_\theta = m(r\ddot{\theta} + 2\dot{r}\dot{\theta})
$$

The term $-mr\dot{\theta}^2$ is the centripetal acceleration contribution, and $2m\dot{r}\dot{\theta}$ is the Coriolis acceleration contribution.

## Dynamic Equilibrium — D'Alembert's Principle

D'Alembert's principle rewrites Newton's second law in an equilibrium-like form by introducing an **inertia force** $\mathbf{F}^* = -m\mathbf{a}$:

$$
\sum \mathbf{F} + \mathbf{F}^* = \mathbf{0}
$$

This allows static-equilibrium techniques (free-body diagrams, moment equations) to be applied to dynamic problems. The inertia force acts through the mass center in the direction opposite to acceleration.

## Central Force Motion

A **central force** is always directed toward or away from a fixed point, with magnitude depending only on distance:

$$
\mathbf{F} = f(r)\mathbf{e}_r
$$

Key properties:

- Angular momentum is conserved: $h = r^2\dot{\theta} = \text{constant}$
- Motion is confined to a plane

### Gravitational Central Force

For a mass $m$ orbiting a body of mass $M$:

$$
F = -\frac{GMm}{r^2}
$$

The orbit equation is:

$$
\frac{1}{r} = \frac{GM}{h^2}(1 + e\cos\theta)
$$

where $e$ is the eccentricity ($e = 0$ circle, $0 < e < 1$ ellipse, $e = 1$ parabola, $e > 1$ hyperbola).

## Worked Examples

### Example 1: Block on an Incline

A 10 kg block slides down a 30° incline with coefficient of kinetic friction $\mu_k = 0.2$.

**Given:**

- Mass: $m = 10$ kg
- Incline angle: $\theta = 30^\circ$
- Coefficient of friction: $\mu_k = 0.2$

**Find:** Acceleration of the block.

**Solution:**

Apply Newton's second law along and perpendicular to the incline.

**Normal direction** (perpendicular to incline, no acceleration):

$$
N - mg\cos\theta = 0
$$

$$
N = 10(9.81)\cos 30^\circ = 84.96 \text{ N}
$$

**Along the incline** (positive down the slope):

$$
mg\sin\theta - \mu_k N = ma
$$

$$
10(9.81)\sin 30^\circ - 0.2(84.96) = 10a
$$

$$
49.05 - 16.99 = 10a
$$

$$
a = 3.21 \text{ m/s}^2
$$

### Example 2: Banked Curve

A car travels at constant speed around a banked curve of radius $R = 150$ m with banking angle $\beta = 20^\circ$. Find the speed at which no friction is needed.

**Given:**

- $R = 150$ m, $\beta = 20^\circ$, friction not required

**Find:** Ideal speed $v$.

**Solution:**

Using normal-tangential coordinates with the normal direction toward the center of the curve:

**Vertical equilibrium:**

$$
N\cos\beta = mg
$$

**Radial equation (toward center):**

$$
N\sin\beta = \frac{mv^2}{R}
$$

Dividing the second equation by the first:

$$
\tan\beta = \frac{v^2}{Rg}
$$

$$
v = \sqrt{Rg\tan\beta} = \sqrt{150(9.81)\tan 20^\circ} = \sqrt{535.6} = 23.1 \text{ m/s}
\approx 83.3 \text{ km/h}
$$

### Example 3: Satellite Orbit

A satellite orbits Earth at an altitude of 400 km. Find its orbital speed and period.

**Given:**

- Earth radius: $R_E = 6371$ km
- Altitude: $h = 400$ km
- $GM_E = 3.986 \times 10^{14}$ m³/s²

**Find:** Orbital speed $v$ and period $T$.

**Solution:**

Orbital radius: $r = R_E + h = 6771$ km $= 6.771 \times 10^6$ m

For a circular orbit, gravitational force provides centripetal acceleration:

$$
\frac{GMm}{r^2} = \frac{mv^2}{r}
$$

$$
v = \sqrt{\frac{GM}{r}} = \sqrt{\frac{3.986 \times 10^{14}}{6.771 \times 10^6}} = 7672
\text{ m/s} \approx 7.67 \text{ km/s}
$$

**Period:**

$$
T = \frac{2\pi r}{v} = \frac{2\pi(6.771 \times 10^6)}{7672} = 5545 \text{ s} \approx
92.4 \text{ min}
$$

## Common Force Models

| Force | Expression | Notes |
| --- | --- | --- |
| Gravity (near surface) | $W = mg$ | $g \approx 9.81$ m/s² |
| Gravity (general) | $F = \frac{GMm}{r^2}$ | Inverse-square law |
| Spring | $F = -kx$ | Hooke's law, $x$ from natural length |
| Kinetic friction | $f_k = \mu_k N$ | Opposes relative sliding motion |
| Drag | $F_D = \frac{1}{2}C_D \rho A v^2$ | Quadratic in velocity |

## Applications in Engineering

### Aerospace Engineering

- Orbital mechanics and satellite deployment
- Launch vehicle trajectory analysis
- Re-entry dynamics and heat shield design

### Automotive Engineering

- Vehicle acceleration and braking performance
- Tire-road interaction on curves
- Suspension response to road inputs

### Biomechanics

- Human gait analysis and joint forces
- Prosthetic limb design
- Sports equipment optimization

### Marine Engineering

- Ship propulsion and resistance calculations
- Mooring line tension under wave loads
- Submarine depth control dynamics

## Practical Problem-Solving Tips

### 1. Draw a Complete Free-Body Diagram

- Isolate the particle and show all external forces
- Include weight, normal forces, friction, springs, and applied loads
- Indicate the assumed positive direction for acceleration

### 2. Choose the Right Coordinate System

- Cartesian for rectilinear or projectile motion
- Normal-tangential for known curved paths
- Polar for radial or orbital motion

### 3. Count Equations and Unknowns

- Two-dimensional problems yield two scalar equations
- Ensure you have enough equations before solving
- Use constraint equations for connected systems

### 4. Check Limiting Cases

- Verify results reduce to known solutions (e.g., zero friction, zero angle)
- Ensure forces balance when acceleration is zero
- Confirm direction of friction opposes motion

### 5. Validate with Energy or Momentum

- Cross-check answers using work-energy or impulse-momentum methods
- These scalar methods often catch sign or algebra errors

Kinetics of particles is the stepping stone to rigid body dynamics, where distributed mass and rotational effects become important. Mastering particle kinetics ensures a solid understanding of force-acceleration relationships used throughout engineering mechanics.

## Related Scripts

- [Charged Particle Dynamics in a Magnetic Field](../../../scripts/simulations/charged_particle_dynamics_in_a_magnetic_field_using_runge_kutta_methods/): integrates the motion of a charged particle in a uniform magnetic field with the classical fourth-order Runge–Kutta (RK4) method and animates the resulting helical trajectory in 3D.

## Exercises

**Exercise 1.** A 70 kg person stands on a scale in an elevator that accelerates upward at 1.5 m/s². What does the scale read?

<details>
<summary>Answer</summary>

$N - mg = ma$, so $N = m(g + a) = 70(9.81 + 1.5) = 792$ N (equivalent to an 80.7 kg reading on a scale calibrated in kg).

</details>

**Exercise 2.** A 20 kg crate is pulled up a $25^\circ$ incline by a force $P = 200$ N parallel to the slope. The kinetic friction coefficient is $\mu_k = 0.3$. Find the acceleration.

<details>
<summary>Answer</summary>

$N = mg\cos 25^\circ = 177.8$ N, so friction is $0.3 \times 177.8 = 53.3$ N down the slope. The weight component along the slope is $mg\sin 25^\circ = 82.9$ N.

$$
a = \frac{200 - 82.9 - 53.3}{20} = 3.19 \text{ m/s}^2 \text{ (up the slope)}
$$

</details>

**Exercise 3.** For the banked curve of Example 2 ($R = 150$ m, $\beta = 20^\circ$), derive the maximum speed before the car slides outward if $\mu_s = 0.3$, and evaluate it.

<details>
<summary>Answer</summary>

At the maximum speed, friction $\mu_s N$ acts down the bank. Vertical: $N\cos\beta - \mu_s N\sin\beta = mg$. Radial: $N\sin\beta + \mu_s N\cos\beta = mv^2/R$. Dividing:

$$
v_{max} = \sqrt{Rg\,\frac{\sin\beta + \mu_s\cos\beta}{\cos\beta - \mu_s\sin\beta}} = \sqrt{150 \times 9.81 \times \frac{0.342 + 0.282}{0.940 - 0.103}} = 33.1 \text{ m/s}
$$

This is about 119 km/h, compared with 83 km/h for the friction-free design speed.

</details>

**Exercise 4.** Find the radius, altitude and orbital speed of a geostationary orbit, whose period equals one sidereal day (86 164 s). Use $GM_E = 3.986 \times 10^{14}$ m³/s² and $R_E = 6371$ km.

<details>
<summary>Answer</summary>

For a circular orbit $v = 2\pi r/T$ and $v^2 = GM/r$, so

$$
r = \left(\frac{GM\,T^2}{4\pi^2}\right)^{1/3} = 4.216 \times 10^7 \text{ m} = 42\,164
\text{ km}
$$

The altitude is $42\,164 - 6371 = 35\,793$ km and the speed is $v = 2\pi r/T = 3.07$ km/s.

</details>

**Exercise 5.** A 0.2 kg bead slides without friction along a straight rod that rotates in a horizontal plane at a constant $\dot{\theta} = \omega = 3$ rad/s. The bead starts at $r_0 = 0.1$ m with no radial velocity. Using polar coordinates, find $r(t)$, and the radial speed and the transverse force from the rod at $t = 0.5$ s.

<details>
<summary>Answer</summary>

The frictionless rod exerts no radial force, so $\sum F_r = m(\ddot{r} - r\omega^2) = 0$. With $r(0) = r_0$ and $\dot{r}(0) = 0$:

$$
r(t) = r_0\cosh(\omega t), \quad \dot{r}(t) = r_0\omega\sinh(\omega t)
$$

At $t = 0.5$ s: $r = 0.1\cosh(1.5) = 0.235$ m and $\dot{r} = 0.3\sinh(1.5) = 0.639$ m/s.

Since $\ddot{\theta} = 0$, the transverse equation gives $F_\theta = m(2\dot{r}\dot{\theta}) = 2(0.2)(0.639)(3) = 0.767$ N. This is the Coriolis force the rod must supply.

</details>

## References

- R. C. Hibbeler, *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- J. L. Meriam, L. G. Kraige, *Engineering Mechanics: Dynamics*, Wiley.
- F. P. Beer, E. R. Johnston, P. J. Cornwell, *Vector Mechanics for Engineers: Dynamics*, McGraw-Hill.
