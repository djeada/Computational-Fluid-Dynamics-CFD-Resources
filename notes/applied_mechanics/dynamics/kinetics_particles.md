# Kinetics of Particles

Kinetics relates the forces on a body to the motion they produce. For a particle, or for a body whose rotation does not matter, the relation is Newton's second law, written in the coordinate system chosen in [Kinematics of Particles](kinematics_particles.md). This note sets up the equations of motion in Cartesian, normal–tangential and polar coordinates, treats drag, central forces and the motion of the mass centre of a system of particles, and works through the standard problems: inclines, banked curves, orbits and projectiles with air resistance. The integrated forms of the same law, work–energy and impulse–momentum, are in [Work and Energy Methods](work_energy.md) and [Impulse and Momentum](impulse_momentum.md).

## Problem Statement

A particle of mass $m$ (kg), or a system of particles, moves in an inertial reference frame under known forces: gravity, contact and normal forces, friction, spring forces, aerodynamic drag, thrust. Given the forces as functions of position, velocity and time, and the initial position and velocity, find the acceleration and, by integration, the motion; or, given the motion, find the forces needed to produce it, such as a normal reaction, a cable tension or the friction required on a curve. The bodies are rigid enough that their size and rotation can be ignored, speeds are small compared with the speed of light, and the reference frame is inertial (fixed to the ground for most engineering problems, to the stars for orbits). The governing equation is

$$
\sum\mathbf{F} = m\mathbf{a}
$$

which in each coordinate system gives up to three scalar equations, supplemented by constraint relations (a block stays on an incline, a car on a road, a cord stays taut) and force laws (Coulomb friction, Hooke's law, quadratic drag).

## Newton's Laws and Inertial Frames

Newton's first law states that a particle on which no net force acts moves at constant velocity; the frames in which this holds are the inertial frames. The second law states that in an inertial frame the net force equals mass times acceleration. The third law states that the forces two particles exert on each other are equal, opposite and collinear, $`\mathbf{F}_{AB} = -\mathbf{F}_{BA}`$; it is what makes internal forces cancel when particles are grouped into a system.

A frame fixed to the Earth's surface rotates at $7.29\times10^{-5}$ rad/s. For most machines and vehicles the resulting Coriolis and centripetal accelerations are negligible, so the ground counts as inertial; for long-range ballistics, ocean currents and the atmosphere they are not (see [Rigid Body Kinematics](rigid_body_kinematics.md#rotating-reference-frames)).

## Equations of Motion

### Procedure

1. Choose the coordinate system from the description of the motion: Cartesian for fixed directions, normal–tangential for a known path, polar for a distance and angle from a fixed point.
2. Draw the free-body diagram of the particle with every external force, and next to it the kinetic diagram with $m\mathbf{a}$ in components along the chosen axes.
3. Write one scalar equation per direction, with the acceleration expressed through the kinematic formulas.
4. Add the force laws and constraint conditions, and check that the number of equations equals the number of unknowns.
5. Solve, then check limiting cases and the sign of any friction or contact force (a normal force that comes out negative means contact is lost).

### Cartesian Coordinates

$$
\sum F_x = m\ddot{x},
\qquad \sum F_y = m\ddot{y},
\qquad \sum F_z = m\ddot{z}
$$

### Normal and Tangential Coordinates

$$
\sum F_t = m\dot{v},
\qquad \sum F_n = m \frac{v^2}{\rho},
\qquad \sum F_b = 0
$$

The tangential force changes the speed, the normal force toward the centre of curvature changes the direction, and the force along the binormal $\mathbf{e}_b = \mathbf{e}_t \times \mathbf{e}_n$ must vanish because there is no acceleration out of the osculating plane.

### Polar Coordinates

$$
\sum F_r = m(\ddot{r} - r\dot{\theta}^2),
\qquad \sum F_\theta = m(r\ddot{\theta} + 2\dot{r}\dot{\theta})
$$

### D'Alembert's Principle

Moving $m\mathbf{a}$ to the left-hand side, $\sum\mathbf{F} + (-m\mathbf{a}) = \mathbf{0}$, turns the second law into an equilibrium statement with an inertia force $-m\mathbf{a}$. It changes nothing physically, but it lets the methods of statics, including moment equations about convenient points, be used on dynamic problems, and it is the starting point of [Lagrangian Mechanics](lagrangian_mechanics.md).

## Force Models

| Force | Expression | Notes |
| --- | --- | --- |
| Weight near the surface | $W = mg$, $g = 9.81$ m/s² | constant direction |
| Gravitation | $F = GMm/r^2$ | $GM_E = 3.986\times10^{14}$ m³/s² for the Earth |
| Linear spring | $F = -k(\ell - \ell_0)$ | $\ell_0$ is the free length |
| Coulomb friction | $F \le \mu_s N$ at rest, $F = \mu_k N$ while sliding | opposes relative sliding |
| Quadratic drag | $\\mathbf{D} = -\\tfrac{1}{2}\\rho C_dA, | \\mathbf{v} |
| Linear drag | $`\mathbf{D} = -c\,\mathbf{v}`$ | creeping flow, $c = 3\pi\mu d$ for a sphere (Stokes) |

## Worked Examples

### Block on an Incline

A 10 kg block slides down a $30^\circ$ incline with $\mu_k = 0.2$. Perpendicular to the incline there is no acceleration, so $N = mg\cos 30^\circ = 84.96$ N. Along the incline, positive downward,

$$
mg\sin 30^\circ - \mu_kN = ma \quad\Rightarrow\quad a = \frac{49.05 - 16.99}{10} = 3.21
\text{ m/s}^2
$$

### Banked Curve

A car rounds a curve of radius $R = 150$ m banked at $\beta = 20^\circ$. At the design speed no friction is needed, and the normal force alone supplies the centripetal force. Vertically $N\cos\beta = mg$, and toward the centre $N\sin\beta = mv^2/R$. Dividing,

$$
v = \sqrt{Rg\tan\beta} = \sqrt{150 \times 9.81 \times \tan 20^\circ} = 23.1
\text{ m/s} = 83.3 \text{ km/h}
$$

Exercise 3 finds how much faster the car can go before it slides outward.

### Circular Orbit

For a satellite at altitude 400 km, $r = 6371 + 400 = 6771$ km. Gravitation is the only force and points to the centre, so $GMm/r^2 = mv^2/r$:

$$
v = \sqrt{\frac{GM_E}{r}} = \sqrt{\frac{3.986\times10^{14}}{6.771\times10^6}} = 7673
\text{ m/s},
\qquad T = \frac{2\pi r}{v} = 5545 \text{ s} = 92.4 \text{ min}
$$

## Central-Force Motion

A force that always points along the line to a fixed point $O$ exerts no moment about $O$, so the angular momentum per unit mass $h = r^2\dot{\theta}$ is constant and the motion stays in a plane. With $F_\theta = 0$ the transverse equation is $d(r^2\dot{\theta})/dt = 0$, and with the substitution $u = 1/r$ the radial equation for gravitation becomes

$$
\frac{d^2u}{d\theta^2} + u = \frac{GM}{h^2} \quad\Rightarrow\quad
\frac{1}{r} = \frac{GM}{h^2}\left(1 + e\cos\theta\right)
$$

a conic with eccentricity $e$: a circle for $e = 0$, an ellipse for $0 < e < 1$, a parabola for $e = 1$ and a hyperbola for $e > 1$, with $\theta$ measured from the point of closest approach. For an ellipse of semi-major axis $a$ the period is $T = 2\pi\sqrt{a^3/GM}$ (Kepler's third law).

## Projectile with Air Drag

With quadratic drag the equations of motion of a projectile couple through the speed,

```math
\ddot{x} = -k\, v\,\dot{x},
\qquad \ddot{y} = -g - k\, v\,\dot{y},
\qquad v = \sqrt{\dot{x}^2 + \dot{y}^2},
\qquad k = \frac{\rho C_dA}{2m}
```

and have no closed-form solution, so they are integrated numerically. In vertical fall drag balances weight at the terminal speed $v_t = \sqrt{g/k}$, approached as $v = v_t\tanh(gt/v_t)$. For a baseball ($m = 0.145$ kg, $d = 73$ mm, $C_d = 0.35$, $\rho = 1.2$ kg/m³) $k = 0.00606$ m⁻¹ and $v_t = 40.2$ m/s.

![Projectile trajectories with and without drag, range against launch angle, and energy budget](../../../scripts/algorithms/dynamics_projectile_drag/dynamics_projectile_drag.png)

At a launch speed of 40 m/s, panel (a) shows that drag cuts the range at $45^\circ$ from 163 m to 96.5 m and makes the descent steeper than the ascent. Panel (b) shows the optimum angle moving to $41.0^\circ$. Panel (c) shows that 68.5 J of the 116 J launch energy is dissipated by drag before impact, which the script checks against the work–energy balance. The drag coefficient itself depends on the Reynolds number and, for a ball, on spin and surface roughness, which is where wind-tunnel data or CFD enter (see [Drag](../../fluid_mechanics/viscous_flow/drag.md)).

## Systems of Particles

For $n$ particles with masses $m_i$, write the force on particle $i$ as an external part $`\mathbf{F}_i`$ and the internal forces $`\mathbf{f}_{ij}`$ exerted by the other particles. Summing the second law over all particles, the internal forces cancel in pairs by the third law, leaving

```math
\sum_i\mathbf{F}_i = \sum_i m_i\mathbf{a}_i = m\,\mathbf{a}_G,
\qquad m = \sum_i m_i,
\qquad \mathbf{r}_G = \frac{1}{m}\sum_i m_i\mathbf{r}_i
```

The mass centre $G$ moves as if the whole mass were concentrated there and every external force acted on it, whatever the internal forces do. Taking moments of the same equations about a fixed point $O$, the internal forces cancel again because each pair is collinear, so $\sum\mathbf{M}_O = \dot{\mathbf{H}}_O$ with $`\mathbf{H}_O = \sum_i\mathbf{r}_i \times m_i\mathbf{v}_i`$. The same equation about the mass centre, $\sum\mathbf{M}_G = \dot{\mathbf{H}}_G$, is the basis of rigid-body kinetics.

A shell fired at 100 m/s and $45^\circ$ bursts at the top of its path, 255 m up and 510 m downrange, into two equal fragments, one of which falls vertically from rest. Both fragments have zero vertical velocity after the burst, so both land at the same time; the mass centre lands where the unburst shell would have, at 1019 m, so the second fragment lands at $2 \times 1019 - 510 = 1529$ m.

## Common Mistakes

1. Writing $m\mathbf{a}$ as a force on the free-body diagram as well as on the kinetic diagram, which counts it twice.
2. Taking the normal force as $mg$ on an incline, in an accelerating lift or over a crest.
3. Assuming the friction force equals $\mu_sN$ when the body is not on the point of slipping.
4. Pointing $a_n$ away from the centre of curvature, or omitting it at constant speed.
5. Applying $\sum\mathbf{F} = m\mathbf{a}$ in an accelerating or rotating frame without the corresponding inertial terms.

## Key Takeaways

- $\sum\mathbf{F} = m\mathbf{a}$ holds in inertial frames and is written in the coordinates that make the acceleration simplest.
- The free-body diagram and the kinetic diagram together give the equations; constraints and force laws close the system.
- Central forces conserve $h = r^2\dot{\theta}$, which with the radial equation gives conic orbits.
- With quadratic drag the motion must be integrated numerically; the terminal speed $\sqrt{g/k}$ sets whether drag matters.
- The mass centre of any system moves under the external forces alone.

## Related Scripts

- [Projectile with Quadratic Drag](../../../scripts/algorithms/dynamics_projectile_drag/): integrates Newton's second law for a projectile with quadratic air drag and compares it with the drag-free parabola.
- [Path, Polar and Rotating-Frame Coordinates](../../../scripts/plots/dynamics_path_coordinates/): draws the acceleration of three moving particles resolved in the coordinate system that suits each of them: normal–tangential components along a projectile path, radial–transverse components for a bead on a rotating rod, and Coriolis and centrifugal terms for a puck seen from a rotating turntable.
- [Variable-Mass Rocket](../../../scripts/algorithms/dynamics_variable_mass_rocket/): integrates the momentum balance of a vertically launched rocket and splits its burnout speed into the ideal rocket-equation increment, the gravity loss and the drag loss.
- [Charged Particle Dynamics in a Magnetic Field](../../../scripts/simulations/charged_particle_dynamics_in_a_magnetic_field_using_runge_kutta_methods/): integrates the motion of a charged particle in a uniform magnetic field with the classical fourth-order Runge–Kutta (RK4) method and animates the resulting helical trajectory in 3D.

## Exercises

**Exercise 1.** A 70 kg person stands on a scale in a lift that accelerates upward at 1.5 m/s². What does the scale read?

<details>
<summary>Answer</summary>

$N - mg = ma$, so $N = m(g + a) = 70(9.81 + 1.5) = 792$ N, which a scale calibrated in kilograms shows as 80.7 kg.

</details>

**Exercise 2.** A 20 kg crate is pulled up a $25^\circ$ incline by a force $P = 200$ N parallel to the slope. The kinetic friction coefficient is $\mu_k = 0.3$. Find the acceleration.

<details>
<summary>Answer</summary>

$N = mg\cos 25^\circ = 177.8$ N, so friction is $0.3 \times 177.8 = 53.3$ N down the slope. The weight component along the slope is $mg\sin 25^\circ = 82.9$ N.

```math
a = \frac{200 - 82.9 - 53.3}{20} = 3.19 \text{ m/s}^2 \text{ up the slope}
```

</details>

**Exercise 3.** For the banked curve of the worked example ($R = 150$ m, $\beta = 20^\circ$), derive the maximum speed before the car slides outward if $\mu_s = 0.3$, and evaluate it.

<details>
<summary>Answer</summary>

At the maximum speed friction $\mu_sN$ acts down the bank. Vertically $N\cos\beta - \mu_sN\sin\beta = mg$, and toward the centre $N\sin\beta + \mu_sN\cos\beta = mv^2/R$. Dividing:

```math
v_{\max} = \sqrt{Rg\,\frac{\sin\beta + \mu_s\cos\beta}{\cos\beta - \mu_s\sin\beta}} = \sqrt{150 \times 9.81 \times \frac{0.342 + 0.282}{0.940 - 0.103}} = 33.1 \text{ m/s}
```

This is 119 km/h, against 83 km/h for the friction-free design speed.

</details>

**Exercise 4.** Find the radius, altitude and orbital speed of a geostationary orbit, whose period equals one sidereal day (86 164 s). Use $GM_E = 3.986\times10^{14}$ m³/s² and $R_E = 6371$ km.

<details>
<summary>Answer</summary>

For a circular orbit $v = 2\pi r/T$ and $v^2 = GM/r$, so

```math
r = \left(\frac{GM\,T^2}{4\pi^2}\right)^{1/3} = 4.216\times10^7 \text{ m} = 42\,164 \text{ km}
```

The altitude is $`42\,164 - 6371 = 35\,793`$ km and the speed is $v = 2\pi r/T = 3.07$ km/s.

</details>

**Exercise 5.** A 0.2 kg bead slides without friction along a straight rod that rotates in a horizontal plane at a constant $\dot{\theta} = \omega = 3$ rad/s. The bead starts at $r_0 = 0.1$ m with no radial velocity. Find $r(t)$, and the radial speed and the transverse force from the rod at $t = 0.5$ s.

<details>
<summary>Answer</summary>

The frictionless rod exerts no radial force, so $\sum F_r = m(\ddot{r} - r\omega^2) = 0$. With $r(0) = r_0$ and $\dot{r}(0) = 0$:

```math
r(t) = r_0\cosh\omega t, \qquad \dot{r}(t) = r_0\omega\sinh\omega t
```

At $t = 0.5$ s: $r = 0.1\cosh 1.5 = 0.235$ m and $\dot{r} = 0.3\sinh 1.5 = 0.639$ m/s.

Since $\ddot{\theta} = 0$, the transverse equation gives $F_\theta = m(2\dot{r}\dot{\theta}) = 2 \times 0.2 \times 0.639 \times 3 = 0.767$ N, the force the rod must supply to produce the Coriolis acceleration. This motion is panel (b) of the figure in [Kinematics of Particles](kinematics_particles.md#polar-and-cylindrical-coordinates).

</details>

## References

- R. C. Hibbeler, *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- J. L. Meriam, L. G. Kraige and J. N. Bolton, *Engineering Mechanics: Dynamics*, 9th ed., Wiley, 2018.
- F. P. Beer, E. R. Johnston, P. J. Cornwell and B. P. Self, *Vector Mechanics for Engineers: Dynamics*, 12th ed., McGraw-Hill, 2019.
- H. D. Curtis, *Orbital Mechanics for Engineering Students*, 3rd ed., Butterworth-Heinemann, 2014.
- J. D. Anderson, *Fundamentals of Aerodynamics*, 6th ed., McGraw-Hill, 2017.
