# Work and Energy Methods

The principle of work and energy is Newton's second law integrated along the path. It relates the work done by the forces between two positions to the change in kinetic energy, so speeds at given positions follow without computing accelerations or times, and forces that do no work drop out. This note defines the work of forces and couples, the kinetic energy of particles and rigid bodies, potential energy and the conservation of mechanical energy, power and efficiency, and the energy balance as a check on numerical integration. Energy expressions are also the starting point of [Lagrangian Mechanics](lagrangian_mechanics.md) and of the energy method for natural frequencies in [Mechanical Vibrations](vibrations.md).

## Problem Statement

A particle, a rigid body or a system of connected bodies moves between two configurations 1 and 2 under known forces: gravity, springs, friction, drag, applied forces and couples. Given the configuration and speed at position 1 and the forces as functions of position (or of velocity, for dissipative forces), find the speed or angular speed at position 2, the distance needed to reach a given speed, the force or couple needed to produce a motion, or the power required. Bodies are rigid, connections do not stretch unless they are modelled as springs, and rolling is without slipping unless stated. The governing equation is

$$
T_1 + \sum U_{1\to2} = T_2
$$

or, with the work of conservative forces written as a change of potential energy $V$,

$$
T_1 + V_1 + U_{1\to2}^{nc} = T_2 + V_2
$$

where $T$ is kinetic energy and $U^{nc}$ the work of the non-conservative forces. Energies and work are in J, power in W.

## Work of a Force

A force $\mathbf{F}$ whose point of application moves along a path from 1 to 2 does work

```math
U_{1\to2} = \int_1^2\mathbf{F}\cdot d\mathbf{r} = \int_{s_1}^{s_2}F\cos\theta\, ds
```

where $\theta$ is the angle between the force and the displacement of its point of application. Only the component of the force along the motion does work.

| Force | Work from 1 to 2 | Notes |
| --- | --- | --- |
| constant force, straight path | $`F\,d\cos\theta`$ | $d$ is the displacement |
| weight | $-mg(y_2 - y_1)$ | $y$ upward; independent of the path |
| linear spring | $-\tfrac{1}{2}k(\delta_2^2 - \delta_1^2)$ | $\delta$ is the extension from the free length |
| kinetic friction on a fixed surface | $`-\mu_kN\,s`$ | $s$ is the distance slid, not the displacement |
| normal force on a fixed surface, pin reaction at a fixed pin | 0 | no displacement along the force |
| friction at a rolling contact without slip | 0 | the contact point is at rest |
| couple $M$ on a rotating body | $`\int_{\theta_1}^{\theta_2}M\,d\theta`$ | $M(\theta_2 - \theta_1)$ for constant $M$ |

## Kinetic Energy

A particle has $T = \tfrac{1}{2}mv^2$. For a rigid body in plane motion, the velocity of an element is $\mathbf{v}_G + \boldsymbol{\omega} \times \boldsymbol{\rho}$ where $\boldsymbol{\rho}$ is measured from the mass centre. Squaring and integrating, the cross term vanishes because $`\int\boldsymbol{\rho}\,dm = \mathbf{0}`$, leaving

$$
T = \tfrac{1}{2}mv_G^2 + \tfrac{1}{2}I_G\omega^2
$$

the energy of the mass centre moving with the whole mass plus the energy of rotation about it. For rotation about a fixed axis through $O$ this equals $\tfrac{1}{2}I_O\omega^2$, and for pure translation $\tfrac{1}{2}mv_G^2$. In three dimensions the rotational part is $\tfrac{1}{2}\boldsymbol{\omega}\cdot\mathbf{I}_G\boldsymbol{\omega}$.

## Principle of Work and Energy

For a particle, the tangential component of the second law is $`F_t = mv\,dv/ds`$. Multiplying by $ds$ and integrating from 1 to 2,

$$
\int_1^2\mathbf{F}\cdot d\mathbf{r} = \tfrac{1}{2}mv_2^2 - \tfrac{1}{2}mv_1^2
$$

For a system of particles the same equation holds with the work of all forces, internal and external. Internal forces between particles of a rigid body do no net work, because the pair acts at points whose separation does not change; internal forces in springs, between bodies sliding on each other and in a deformable body do. For a system of connected rigid bodies with inextensible links and pins without friction, the work–energy equation is therefore written with the external forces, the springs and the friction alone, and the connection forces never appear.

Work–energy is one scalar equation. It gives a speed at a position directly, but it cannot by itself find a quantity that does no work (a normal force, a pin reaction) or the time taken; for those, Newton's laws or impulse–momentum are needed.

## Potential Energy and Conservation of Energy

A force is conservative when its work depends only on the end points, which is equivalent to saying that the work around every closed path is zero and that the force derives from a potential, $\mathbf{F} = -\nabla V$. Then $U_{1\to2} = V_1 - V_2$.

| Force | Potential energy |
| --- | --- |
| weight near the surface | $V_g = mgy$, $y$ upward from any datum |
| gravitation | $V_g = -GMm/r$ |
| linear spring | $V_e = \tfrac{1}{2}k\delta^2$ |

With $U^{nc}$ the work of the remaining forces,

$$
T_1 + V_1 + U_{1\to2}^{nc} = T_2 + V_2
$$

and when only conservative forces do work, $E = T + V$ is constant. Friction, drag, damping and engine forces are not conservative: friction and drag always make $U^{nc}$ negative, converting mechanical energy to heat.

## Power and Efficiency

Power is the rate of doing work,

$$
P = \frac{dU}{dt} = \mathbf{F}\cdot\mathbf{v},
\qquad P = M\omega \text{ for a couple}
$$

with $1\text{ W} = 1\text{ J/s}$ and 1 hp = 745.7 W. The mechanical efficiency of a machine is $\eta = P_{\mathrm{out}}/P_{\mathrm{in}} < 1$, and the efficiencies of components in series multiply.

## Worked Examples

### Block Released by a Spring

A 5 kg block on a frictionless surface is pushed against a spring ($k = 800$ N/m), compressing it 0.15 m, and released. When the spring reaches its free length,

$$
\tfrac{1}{2}k\delta^2 = \tfrac{1}{2}mv^2 \quad\Rightarrow\quad v = \delta
\sqrt{k/m} = 0.15 \sqrt{160} = 1.90 \text{ m/s}
$$

### Cylinder Rolling Down a Ramp

A solid cylinder ($m = 10$ kg, $R = 0.3$ m) starts from rest and rolls without slipping 4 m down a $30^\circ$ incline, dropping $h = 2$ m. Friction at the contact does no work, and $\omega = v_G/R$, so

$$
mgh = \tfrac{1}{2}mv_G^2 + \tfrac{1}{2}\left(\tfrac{1}{2}mR^2\right)
\frac{v_G^2}{R^2} = \tfrac{3}{4}mv_G^2 \quad\Rightarrow\quad
v_G = \sqrt{\tfrac{4}{3}gh} = 5.11 \text{ m/s}
$$

The result is independent of mass and radius; a block sliding without friction would reach $\sqrt{2gh} = 6.26$ m/s.

### Power to Climb a Grade

A 1500 kg car climbs a 5% grade ($\sin\theta \approx 0.05$) at a steady 90 km/h (25 m/s) against 600 N of aerodynamic and rolling resistance. The tractive force is $mg\sin\theta + 600 = 736 + 600 = 1336$ N, and the power at the wheels is

$$
P = Fv = 1336 \times 25 = 33.4 \text{ kW} = 44.8 \text{ hp}
$$

### Pendulum with Pivot Friction

A uniform rod ($m = 2$ kg, $L = 0.8$ m, $I_O = \tfrac{1}{3}mL^2 = 0.427$ kg·m²) swings from horizontal to vertical against a constant friction couple of 0.5 N·m at the pivot. The mass centre falls $L/2$, and the friction couple does $-0.5 \times \pi/2$ J:

$$
mg \frac{L}{2} - M_f \frac{\pi}{2} = \tfrac{1}{2}I_O\omega^2 \quad\Rightarrow\quad
\omega = \sqrt{\frac{7.848 - 0.785}{0.2133}} = 5.75 \text{ rad/s}
$$

## Energy as a Check on Numerical Integration

When the equations of motion are integrated numerically, the energy balance is an independent check. Integrating the dissipated work as an extra state and monitoring $T + V + W_{\mathrm{dissipated}}$ shows whether the time step and tolerances are adequate.

![Projectile with quadratic drag: trajectories, range and the energy budget](../../../scripts/algorithms/dynamics_projectile_drag/dynamics_projectile_drag.png)

Panel (c) shows the energy budget of a baseball launched at 40 m/s and $45^\circ$: kinetic energy turns into potential energy on the way up and back again on the way down, while drag removes 68.5 J of the 116 J launch energy by impact; the dashed sum $T + V + W_{\mathrm{drag}}$ stays constant to $2\times10^{-7}$ J. For a conservative system the same check is the drift of $T + V$; the [double pendulum script](../../../scripts/algorithms/dynamics_double_pendulum_lagrange/) shows that an adaptive Runge–Kutta method lets it drift slowly and steadily, whereas the energy error of a symplectic integrator stays bounded over long runs.

## Common Mistakes

1. Using displacement instead of distance slid in the work of friction.
2. Counting the work of a force both as work and as a change of potential energy.
3. Omitting the rotational kinetic energy of wheels, pulleys and rolling bodies.
4. Assigning work to friction at a rolling contact without slip, or to the normal force of a fixed surface.
5. Using work–energy to find forces that do no work, or the time of a motion.

## Key Takeaways

- $T_1 + \sum U_{1\to2} = T_2$ is the second law integrated along the path; it relates speeds at two positions.
- A rigid body in plane motion has $T = \tfrac{1}{2}mv_G^2 + \tfrac{1}{2}I_G\omega^2$.
- Forces that do no work, such as fixed-surface normal forces, pin reactions and rolling friction, drop out.
- Conservative forces enter through $V$; friction, drag and damping always remove mechanical energy.
- Power is $\mathbf{F}\cdot\mathbf{v}$ or $M\omega$, and the energy balance is a useful check on any numerical integration.

## Related Scripts

- [Projectile with Quadratic Drag](../../../scripts/algorithms/dynamics_projectile_drag/): integrates Newton's second law for a projectile with quadratic air drag and compares it with the drag-free parabola.
- [Double Pendulum from Lagrange's Equations](../../../scripts/algorithms/dynamics_double_pendulum_lagrange/): integrates the Lagrange equations of a planar double pendulum and compares its small-amplitude motion with the normal modes of the linearized equations.

## Exercises

**Exercise 1.** A 0.2 kg ball sits on a vertical spring ($k = 500$ N/m) compressed by 0.1 m. When released, how high does the ball rise above its release point? Neglect the spring mass and air resistance.

<details>
<summary>Answer</summary>

All of the spring energy becomes gravitational potential energy at the top:

```math
\tfrac{1}{2}k\delta^2 = mgh
\quad\Rightarrow\quad
h = \frac{0.5 \times 500 \times 0.01}{0.2 \times 9.81} = \frac{2.5}{1.962} = 1.27 \text{ m}
```

</details>

**Exercise 2.** A 3 kg block slides across a floor at 6 m/s. The kinetic friction coefficient is $\mu_k = 0.25$. How far does it slide before stopping?

<details>
<summary>Answer</summary>

$`T_1 - \mu_kmg\,s = 0`$, and the mass cancels:

```math
s = \frac{v^2}{2\mu_kg} = \frac{36}{2 \times 0.25 \times 9.81} = 7.34 \text{ m}
```

</details>

**Exercise 3.** A small object is released from rest at height $h$ on a track that leads into a vertical loop of radius $R = 0.5$ m. Find the minimum $h$, measured from the bottom of the loop, for the object to stay on the track at the top when it is (a) a block sliding without friction and (b) a small solid sphere rolling without slipping.

<details>
<summary>Answer</summary>

At the top the normal force must be non-negative, so $mv^2/R \ge mg$, or $v^2 \ge gR$.

(a) $mgh = mg(2R) + \tfrac{1}{2}mv^2$ gives $h = 2R + R/2 = 2.5R = 1.25$ m.

(b) The sphere also carries rotational energy, $T = \tfrac{1}{2}mv^2(1 + \tfrac{2}{5}) = 0.7mv^2$. Then $mgh = 2mgR + 0.7mgR$, so $h = 2.7R = 1.35$ m.

</details>

**Exercise 4.** A pump lifts 50 L/s of water through a height of 30 m with an overall efficiency of 70%. Find the power delivered to the water and the input power in kW and hp.

<details>
<summary>Answer</summary>

```math
P_{\mathrm{out}} = \rho gQh = 1000 \times 9.81 \times 0.05 \times 30 = 14.7 \text{ kW}
```

```math
P_{\mathrm{in}} = \frac{P_{\mathrm{out}}}{\eta} = \frac{14\,715}{0.7} = 21.0 \text{ kW} = 28.2 \text{ hp}
```

</details>

**Exercise 5.** A solid disk flywheel ($m = 50$ kg, $R = 0.4$ m) spins at 3000 rpm. A brake applies a constant friction couple of 20 N·m. Using the work of a couple, find the number of revolutions before it stops, and use angular impulse to find the stopping time.

<details>
<summary>Answer</summary>

$I = \tfrac{1}{2}mR^2 = 4$ kg·m², $\omega = 314.2$ rad/s and $T_1 = \tfrac{1}{2}I\omega^2 = 197.4$ kJ.

```math
M\,\Delta\theta = T_1
\quad\Rightarrow\quad
\Delta\theta = \frac{197\,392}{20} = 9870 \text{ rad} = 1571 \text{ rev}
```

The stopping time follows from angular impulse and momentum, $M t = I\omega$: $t = 4 \times 314.2/20 = 62.8$ s.

</details>

## References

- R. C. Hibbeler, *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- J. L. Meriam, L. G. Kraige and J. N. Bolton, *Engineering Mechanics: Dynamics*, 9th ed., Wiley, 2018.
- F. P. Beer, E. R. Johnston, P. J. Cornwell and B. P. Self, *Vector Mechanics for Engineers: Dynamics*, 12th ed., McGraw-Hill, 2019.
- E. Hairer, C. Lubich and G. Wanner, *Geometric Numerical Integration*, 2nd ed., Springer, 2006.
