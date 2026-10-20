# Mechanisms and Linkages

A mechanism is an assembly of rigid links connected by joints that turns a given input motion into a required output motion: the crank, connecting rod and piston of an engine, the four-bar linkages of windscreen wipers, suspensions and landing gear, the cam that opens a valve. This note covers the classification of joints, the mobility of planar mechanisms, the kinematic analysis of the four-bar linkage and the slider-crank by vector loop closure, the transmission angle, cam follower motions and a short introduction to synthesis. Gears, which are also mechanisms, have their own note, [Gears and Transmissions](gears.md).

Kinematic analysis comes before everything else in machine design. The accelerations it produces set the inertia forces that load the joints and bearings (see [Rigid Body Kinetics](../dynamics/rigid_body_kinetics.md)), and the same loop-closure equations are what multibody codes solve when a moving geometry is coupled to a CFD simulation.

## Problem Statement

Given a planar mechanism, that is the link lengths, the joint types and positions, and the motion of the input link, for example a crank angle $\theta_2(t)$ with $\omega_2 = \dot\theta_2$ and $\alpha_2 = \ddot\theta_2$, find:

- the number of independent inputs the mechanism needs (its mobility);
- the angular position, velocity and acceleration of every other link, and the path, velocity and acceleration of any point on them;
- the quality of force transmission, measured by the transmission angle, and the positions where the mechanism locks or changes branch.

The links are rigid, the joints ideal (no clearance, friction or elasticity) and the motion planar. The governing equations are the vector loop equations: for every independent closed loop of the mechanism, the sum of the link vectors around the loop is zero at every instant,

$$
\sum_k r_k e^{i\theta_k} = 0
$$

with $r_k$ the length of link $k$ and $\theta_k$ its angle from a fixed $x$ axis. Velocities and accelerations follow by differentiating this equation with respect to time. The reverse problem, choosing link lengths that produce a required motion, is synthesis.

## Links, Joints and Kinematic Pairs

A **kinematic pair** is a joint between two links, classified by the relative motion it allows. Lower pairs have surface contact and higher pairs line or point contact.

| Pair | Contact | Relative motion | Degrees of freedom | Constraints in the plane | Constraints in space |
| --- | --- | --- | --- | --- | --- |
| revolute (pin) | surface | rotation about one axis | 1 | 2 | 5 |
| prismatic (slider) | surface | translation along one axis | 1 | 2 | 5 |
| cylindrical | surface | rotation and translation along one axis | 2 |  | 4 |
| spherical (ball) | surface | rotation about any axis through a point | 3 |  | 3 |
| cam or gear contact | line or point | rolling and sliding | 2 in the plane | 1 |  |

A link with two joints is binary, one with three ternary. A kinematic chain becomes a mechanism when one link, the ground or frame, is fixed. Fixing a different link of the same chain gives an **inversion** of the mechanism, which changes the absolute motions but not the relative motions between links.

## Mobility

A free rigid body in the plane has three degrees of freedom. A mechanism of $n$ links, one of them ground, therefore starts with $3(n - 1)$; each one-degree-of-freedom joint (pin or slider) removes two and each two-degree-of-freedom joint (cam or gear contact with rolling and sliding) removes one. This is the Grübler–Kutzbach criterion:

$$
M = 3(n - 1) - 2j_1 - j_2
$$

In space the free body has six degrees of freedom and $M = 6(n - 1) - \sum_i c_i$, where $c_i$ is the number of constraints imposed by joint $i$.

| Mechanism | $n$ | $j_1$ | $j_2$ | $M$ |
| --- | --- | --- | --- | --- |
| four-bar linkage | 4 | 4 | 0 | 1 |
| slider-crank (3 pins, 1 slider) | 4 | 4 | 0 | 1 |
| five-bar linkage | 5 | 5 | 0 | 2 |
| Watt or Stephenson six-bar | 6 | 7 | 0 | 1 |
| cam with roller follower (cam, roller, follower, ground) | 4 | 3 | 1 | 2 |
| three links pinned in a triangle | 3 | 3 | 0 | 0 (a structure) |

The criterion counts constraints and ignores geometry, so it can be wrong in both directions. The roller follower has $M = 2$ because the free spin of the roller is an idle degree of freedom that does not affect the follower motion. A parallelogram linkage with a fifth link parallel to two others has $M = 0$ by the formula but moves, because the extra link imposes a constraint that is already satisfied: the mechanism is overconstrained, and it binds as soon as manufacturing errors break the parallelism.

## The Four-Bar Linkage

The four-bar linkage has a ground link of length $d$ between the fixed pivots $O_2$ and $O_4$, an input crank $a$ pinned at $O_2$, a coupler $b$ and an output rocker $c$ pinned at $O_4$. The joint between crank and coupler is $A$, the joint between coupler and rocker $B$. Angles are measured counter-clockwise from the line $O_2 O_4$.

### Grashof Condition

Let $s$ and $l$ be the shortest and longest links and $p$, $q$ the other two. The Grashof condition

$$
s + l \le p + q
$$

is necessary and sufficient for at least one link to make full revolutions relative to the others. If it holds, the type of linkage depends on which link is grounded:

| Grashof ($s + l < p + q$), ground link is | Linkage | Motion |
| --- | --- | --- |
| adjacent to the shortest link | crank-rocker | the shortest link (crank) turns fully, the opposite link rocks |
| the shortest link | double-crank (drag link) | both links attached to ground turn fully |
| opposite the shortest link | double-rocker | both grounded links rock; the coupler turns fully |

If $s + l > p + q$ every inversion is a triple-rocker and no link turns fully. If $s + l = p + q$ the linkage is a change-point mechanism: at some position all four links are collinear and the output can switch branch, so it needs a guide or flywheel to pass through.

### Position Analysis by Loop Closure

The loop $O_2 \to A \to B \to O_4 \to O_2$ gives

$$
a e^{i\theta_2} + b e^{i\theta_3} - c e^{i\theta_4} - d = 0
$$

two real equations for the two unknowns $\theta_3$ and $\theta_4$. To eliminate $\theta_3$, isolate $b e^{i\theta_3} = d + c e^{i\theta_4} - a e^{i\theta_2}$ and take the squared modulus of both sides:

$$
b^2 = a^2 + c^2 + d^2 + 2cd\cos\theta_4 - 2ad\cos\theta_2 - 2ac\cos(\theta_2 - \theta_4)
$$

Dividing by $2ac$ gives the Freudenstein equation

$$
K_1\cos\theta_4 - K_2\cos\theta_2 + K_3 = \cos(\theta_2 - \theta_4),
\qquad K_1 = \frac{d}{a}, \quad K_2 = \frac{d}{c}, \quad
K_3 = \frac{a^2 - b^2 + c^2 + d^2}{2ac}
$$

With $t = \tan(\theta_4/2)$, $\cos\theta_4 = (1 - t^2)/(1 + t^2)$ and $\sin\theta_4 = 2t/(1 + t^2)$, it becomes the quadratic $At^2 + Bt + C = 0$ with

$$
A = \cos\theta_2 - K_1 - K_2\cos\theta_2 + K_3,
\qquad B = -2\sin\theta_2,
\qquad C = K_1 - (K_2 + 1)\cos\theta_2 + K_3
$$

so that

$$
\theta_4 = 2\arctan \frac{-B \pm \sqrt{B^2 - 4AC}}{2A}
$$

The two signs are the two assemblies of the linkage for the same crank angle, open (minus) and crossed (plus); a Grashof crank-rocker stays on one of them for its whole revolution. A negative discriminant means the links cannot be joined at that crank angle, which happens over part of the revolution of a non-Grashof linkage. Once $\theta_4$ is known, $\theta_3$ is the argument of $d + c e^{i\theta_4} - a e^{i\theta_2}$, and a point $P$ on the coupler at distance $p$ from $A$ and angle $\delta$ to the line $AB$ is at $a e^{i\theta_2} + p e^{i(\theta_3 + \delta)}$. Its path over a revolution is the coupler curve.

### Velocity Analysis

Differentiating the loop equation with respect to time at the current position gives

$$
i a\omega_2 e^{i\theta_2} + i b\omega_3 e^{i\theta_3} - i c\omega_4 e^{i\theta_4} = 0
$$

which is linear in the unknown $\omega_3$ and $\omega_4$. Multiplying by $e^{-i\theta_3}$ and taking the imaginary part eliminates $\omega_3$; multiplying by $e^{-i\theta_4}$ eliminates $\omega_4$:

$$
\omega_4 = \frac{a\omega_2}{c}
\frac{\sin(\theta_2 - \theta_3)}{\sin(\theta_4 - \theta_3)},
\qquad \omega_3 = \frac{a\omega_2}{b}
\frac{\sin(\theta_4 - \theta_2)}{\sin(\theta_3 - \theta_4)}
$$

The ratio $\omega_4/\omega_2$ is the instantaneous velocity ratio, the reciprocal of the mechanical advantage for an ideal linkage. It goes to zero when crank and coupler are collinear ($\theta_3 = \theta_2$ or $\theta_2 + \pi$), the toggle positions, and becomes infinite when coupler and rocker are collinear, where the input cannot drive the output at all.

### Acceleration Analysis

Differentiating once more,

$$
a(i\alpha_2 - \omega_2^2)e^{i\theta_2} + b(i\alpha_3 - \omega_3^2)e^{i\theta_3} -
c(i\alpha_4 - \omega_4^2)e^{i\theta_4} = 0
$$

Each term has a tangential part $i\alpha r e^{i\theta}$ and a centripetal part $-\omega^2 r e^{i\theta}$. With the velocities known, this is again a linear system for $\alpha_3$ and $\alpha_4$, with the same coefficient matrix as the velocity problem:

```math
\begin{bmatrix} -b\sin\theta_3 & c\sin\theta_4 \\ b\cos\theta_3 & -c\cos\theta_4 \end{bmatrix}
\begin{bmatrix} \alpha_3 \\ \alpha_4 \end{bmatrix} =
\begin{bmatrix}
a\alpha_2\sin\theta_2 + a\omega_2^2\cos\theta_2 + b\omega_3^2\cos\theta_3 - c\omega_4^2\cos\theta_4 \\
-a\alpha_2\cos\theta_2 + a\omega_2^2\sin\theta_2 + b\omega_3^2\sin\theta_3 - c\omega_4^2\sin\theta_4
\end{bmatrix}
```

The acceleration of any point follows from $\ddot{\mathbf{r}}$ of its position vector. Graphical velocity and acceleration polygons, and instant centres, solve the same equations by construction and remain useful as checks.

### Transmission Angle and Toggle Positions

The **transmission angle** $\mu$ is the angle between coupler and rocker at $B$. The coupler can only push the rocker along its own line, so the component that turns the rocker is proportional to $\sin\mu$; at $\mu = 90^\circ$ all the coupler force produces output torque, and near $0^\circ$ or $180^\circ$ almost none does, while joint friction and clearances still act. From the triangle $A B O_4$, with $|AO_4|^2 = a^2 + d^2 - 2ad\cos\theta_2$,

$$
\cos\mu = \frac{b^2 + c^2 - a^2 - d^2 + 2ad\cos\theta_2}{2bc}
$$

For a crank-rocker the extremes are at $\theta_2 = 0$ and $\theta_2 = 180^\circ$. A common design guideline keeps $40^\circ \le \mu \le 140^\circ$.

The rocker reaches its extreme positions when crank and coupler are collinear: extended, with $|O_2 B| = a + b$, and folded, with $|O_2 B| = b - a$. The crank does not turn through equal angles between them, so the forward and return strokes take different times at constant crank speed. The time ratio, the larger crank arc divided by the smaller, is the basis of quick-return mechanisms in shapers and packaging machines.

### Worked Example

A crank-rocker has $d = 120$ mm, $a = 40$ mm, $b = 110$ mm, $c = 90$ mm and the crank turns at a constant $\omega_2 = 10$ rad/s. Analyse it at $\theta_2 = 90^\circ$.

1. Grashof: $s + l = 40 + 120 = 160$ mm, $p + q = 110 + 90 = 200$ mm. The condition holds and the shortest link is the crank, adjacent to ground, so the linkage is a crank-rocker.
2. Constants: $K_1 = 120/40 = 3$, $K_2 = 120/90 = 4/3$, $`K_3 = (1600 - 12\,100 + 8100 + 14\,400)/(2 \times 40 \times 90) = 5/3`$.
3. At $\theta_2 = 90^\circ$: $A = -3 + 5/3 = -4/3$, $B = -2$, $C = 3 + 5/3 = 14/3$, so $B^2 - 4AC = 28.89$. The open branch gives $\tan(\theta_4/2) = (2 - 5.375)/(-8/3) = 1.266$ and $\theta_4 = 103.37^\circ$.
4. The coupler vector is $d + c e^{i\theta_4} - a e^{i\theta_2} = (99.17, 47.56)$ mm, of length 110 mm as it must be, so $\theta_3 = 25.62^\circ$.
5. Velocities: $\omega_4 = (40 \times 10/90)\sin 64.38^\circ/\sin 77.75^\circ = 4.10$ rad/s and $\omega_3 = (40 \times 10/110)\sin 13.37^\circ/\sin(-77.75^\circ) = -0.861$ rad/s.
6. Accelerations from the linear system: $\alpha_3 = 22.3$ rad/s² and $\alpha_4 = 16.9$ rad/s².
7. Transmission angle: $`\cos\mu = (12\,100 + 8100 - 1600 - 14\,400)/(2 \times 110 \times 90) = 0.212`$, so $\mu = 77.7^\circ$.

![Four-bar linkage positions, link angles, angular velocities and accelerations, and transmission angle over one crank revolution](../../../scripts/algorithms/mechanisms_four_bar_linkage/mechanisms_four_bar_linkage.png)

The figure repeats the analysis over a full revolution. The rocker swings 54.6° between 90.0° and 144.6°, the toggle positions are at crank angles of 36.9° and 228.2°, and the time ratio is $191.3^\circ/168.7^\circ = 1.134$. The transmission angle stays between 45.8° and 105.8°. Note that the rocker velocity curve is far from sinusoidal, and that the largest angular acceleration of the rocker, 85 rad/s², occurs shortly before the extended toggle.

## The Slider-Crank Mechanism

The in-line slider-crank has a crank of radius $r$ turning about $O$, a connecting rod of length $l$ and a slider (piston) moving along a line through $O$. With the crank angle $\theta$ measured from top dead centre and $\phi$ the rod angle, the loop gives $r\sin\theta = l\sin\phi$ and the piston position from $O$

$$
x = r\cos\theta + l\cos\phi = r\cos\theta + \sqrt{l^2 - r^2\sin^2\theta}
$$

At constant $\omega = \dot\theta$ the exact velocity and acceleration are

```math
v = -r\omega\sin\theta - \frac{r^2\omega\sin\theta\cos\theta}{l\cos\phi},
\qquad
a = -r\omega^2\cos\theta - \frac{r^2\omega^2\cos 2\theta}{l\cos\phi} - \frac{r^4\omega^2\sin^2\theta\cos^2\theta}{l^3\cos^3\phi}
```

With $\lambda = r/l$, expanding $\sqrt{1 - \lambda^2\sin^2\theta} \approx 1 - \tfrac{1}{2}\lambda^2\sin^2\theta$ gives

$$
x \approx l + r\cos\theta - \frac{r\lambda}{4}(1 - \cos 2\theta),
\qquad a \approx - r\omega^2\left(\cos\theta + \lambda\cos 2\theta\right)
$$

The piston acceleration, and so the reciprocating inertia force $-m_{\mathrm{rec}}a$, has a primary component at crank frequency and a secondary component $\lambda$ times smaller at twice crank frequency. Counterweights on the crank can cancel only the primary part; the secondary forces of an inline four-cylinder engine add up and need balance shafts turning at twice crank speed. At top dead centre the exact acceleration is $-r\omega^2(1 + \lambda)$.

![Exact and two-term approximation of piston velocity and acceleration of a slider-crank](../../../scripts/algorithms/mechanisms_four_bar_linkage/mechanisms_slider_crank.png)

For $r = 50$ mm, $l = 200$ mm and 3000 rpm the two-term approximation is within 41 m/s² of the exact acceleration, whose peak is 6169 m/s² at top dead centre. The primary term alone misses the flat part of the curve around bottom dead centre.

## Cams

A cam drives a follower through a prescribed displacement $s(\theta)$ as it turns through angle $\theta$. The design starts from the follower motion; the cam profile is then the envelope of the follower positions. Each rise or fall of height $h$ over a cam angle $\beta$ is described by a motion law, and the velocity and acceleration follow from $`v = \omega\,ds/d\theta`$ and $`a = \omega^2\,d^2s/d\theta^2`$ at constant cam speed $\omega$.

| Motion law | Rise $s(\theta)$, $0 \le \theta \le \beta$ | Peak $v$ | Peak $a$ | Acceleration at the ends |
| --- | --- | --- | --- | --- |
| simple harmonic | $\frac{h}{2}\left(1 - \cos\frac{\pi\theta}{\beta}\right)$ | $\frac{\pi h\omega}{2\beta}$ | $\frac{\pi^2 h\omega^2}{2\beta^2}$ | $\pm$ peak, a jump next to a dwell |
| cycloidal | $h\left(\frac{\theta}{\beta} - \frac{1}{2\pi}\sin\frac{2\pi\theta}{\beta}\right)$ | $\frac{2h\omega}{\beta}$ | $\frac{2\pi h\omega^2}{\beta^2}$ | zero |
| 3-4-5 polynomial | $h\left(10x^3 - 15x^4 + 6x^5\right)$, $x = \theta/\beta$ | $\frac{15h\omega}{8\beta}$ | $\frac{10\sqrt{3}h\omega^2}{3\beta^2}$ | zero |

A jump in acceleration means infinite jerk and an impulsive change of force, which excites vibration of the follower train. Between dwells the acceleration must start and end at zero; this is the fundamental law of cam design, which the simple harmonic law violates and the cycloidal and polynomial laws satisfy. The price is a higher peak acceleration.

The **pressure angle** $\phi$ is the angle between the follower's direction of motion and the normal to the cam at the contact point. For a translating roller follower with offset $e$ and prime circle radius $R_p$ (base circle radius plus roller radius),

$$
\tan\phi = \frac{ds/d\theta - e}{s + \sqrt{R_p^2 - e^2}}
$$

A large pressure angle pushes the follower sideways in its guide and can jam it; $|\phi| \le 30^\circ$ is the usual limit for translating followers. The pressure angle falls as the base circle grows, so the base circle is chosen as the smallest that keeps $\phi$ and the radius of curvature acceptable.

For the valve cam of the exercises, a 10 mm simple harmonic rise over 90° with a 25 mm base circle and a 5 mm roller on the cam axis ($e = 0$, $R_p = 30$ mm), $ds/d\theta = 10\sin 2\theta$ mm/rad and the pressure angle reaches 16.1° at $\theta = 40.9^\circ$. A cycloidal rise over the same angle reaches 20.1°.

## Synthesis

Synthesis chooses the type and dimensions of a mechanism for a task. Type synthesis picks the kind of mechanism (linkage, cam, gears) from the motion required. Dimensional synthesis then fixes the link lengths for one of three tasks:

1. Function generation: the output angle must be a given function of the input angle, $\theta_4 = f(\theta_2)$, as in a mechanical computing linkage or a steering linkage.
2. Path generation: a coupler point must follow a given curve, as in straight-line linkages and walking mechanisms.
3. Motion generation: the coupler must pass through given positions and orientations, as in a door or bucket linkage.

The Freudenstein equation is linear in $K_1$, $K_2$ and $K_3$, so a four-bar that matches a function exactly at three precision points $(\theta_{2,j}, \theta_{4,j})$ follows from three linear equations:

$$
K_1\cos\theta_{4,j} - K_2\cos\theta_{2,j} + K_3 = \cos(\theta_{2,j} - \theta_{4,j}),
\qquad j = 1, 2, 3
$$

Choosing $d$ then gives $a = d/K_1$, $c = d/K_2$ and $b^2 = a^2 + c^2 + d^2 - 2acK_3$. Between the precision points the error is not zero; Chebyshev spacing of the points over the input range keeps it near its minimum. With more conditions than unknowns the link lengths are found by least squares or optimization, which is how most practical linkages are designed today.

## Key Takeaways

- Mobility from the Grübler–Kutzbach criterion $M = 3(n - 1) - 2j_1 - j_2$ is a constraint count; check it against the geometry for overconstrained and idle degrees of freedom.
- The Grashof condition $s + l \le p + q$ and the position of the shortest link decide whether a four-bar is a crank-rocker, double-crank or double-rocker.
- Position analysis is nonlinear and has two branches; velocity and acceleration analysis are linear systems with the same matrix, singular only where coupler and rocker are collinear.
- Keep the transmission angle between about 40° and 140°; the output velocity is zero at the toggle positions.
- The slider-crank acceleration is $-r\omega^2(\cos\theta + \lambda\cos 2\theta)$ to first order in $\lambda = r/l$, which separates primary and secondary inertia forces.
- Cam motion laws must have zero acceleration at the ends of each rise next to a dwell, and the pressure angle limits the smallest usable base circle.

## Related Scripts

- [Four-Bar Linkage Kinematics](../../../scripts/algorithms/mechanisms_four_bar_linkage/): solves the position, velocity and acceleration of a four-bar linkage over a full crank revolution by vector loop closure, using the Freudenstein equation for position and two linear 2 × 2 systems for the velocities and accelerations.
- [Involute Gear Geometry](../../../scripts/plots/gears_involute_profile/): draws the involute construction, a standard 20° spur pinion and gear in mesh with their line of action and path of contact, and the smallest pinion that can mesh without interference as a function of gear ratio.

## Exercises

**Exercise 1.** Use the Grübler–Kutzbach criterion to find the mobility of (a) a slider-crank (4 links including ground, 3 pin joints and 1 slider), (b) a Watt six-bar chain (6 links, 7 pin joints), (c) a planar five-bar linkage (5 links, 5 pin joints) and (d) a disk cam with a pivoted flat-faced follower (3 links: ground, cam, follower; 2 pins and 1 cam contact).

<details>
<summary>Answer</summary>

- (a) $M = 3(4 - 1) - 2(4) = 1$
- (b) $M = 3(6 - 1) - 2(7) = 1$
- (c) $M = 3(5 - 1) - 2(5) = 2$
- (d) $M = 3(3 - 1) - 2(2) - 1 = 1$

The five-bar needs two independent inputs, which is why it is used in two-motor planar robots and plotters. The flat-faced follower has no roller, so there is no idle degree of freedom and the criterion gives the true mobility.

</details>

**Exercise 2.** A four-bar linkage has link lengths 40, 90, 110 and 120 mm. Is it a Grashof linkage? What kinds of motion are possible depending on which link is fixed?

<details>
<summary>Answer</summary>

$s + l = 40 + 120 = 160$ mm and $p + q = 90 + 110 = 200$ mm. Since $160 < 200$ it is a Grashof linkage, so at least one link can rotate fully relative to the others.

- Fixing a link adjacent to the 40 mm link gives a crank-rocker, with the 40 mm link as the crank.
- Fixing the 40 mm link gives a double-crank (drag link).
- Fixing the link opposite the 40 mm link (the 110 mm link if the order around the loop is 40, 90, 110, 120) gives a double-rocker, in which the short coupler can still rotate fully.

</details>

**Exercise 3.** For the linkage of the worked example ($d = 120$, $a = 40$, $b = 110$, $c = 90$ mm), find the smallest and largest transmission angles, and the crank angles of the two toggle positions. Is the linkage acceptable by the 40° to 140° guideline?

<details>
<summary>Answer</summary>

At $\theta_2 = 0$, $|AO_4| = d - a = 80$ mm:

```math
\cos\mu_{\min} = \frac{110^2 + 90^2 - 80^2}{2 \times 110 \times 90} = 0.697, \qquad \mu_{\min} = 45.8^\circ
```

At $\theta_2 = 180^\circ$, $|AO_4| = d + a = 160$ mm, $`\cos\mu_{\max} = (20\,200 - 25\,600)/19\,800 = -0.273`$ and $\mu_{\max} = 105.8^\circ$. Both lie inside the guideline.

Extended toggle, $|O_2B| = a + b = 150$ mm: $\cos\beta_1 = (150^2 + 120^2 - 90^2)/(2 \times 150 \times 120) = 0.8$, so $\theta_2 = 36.87^\circ$. Folded toggle, $|O_2B| = b - a = 70$ mm: $\cos\beta_2 = (70^2 + 120^2 - 90^2)/(2 \times 70 \times 120) = 0.667$, $\beta_2 = 48.19^\circ$, and the crank points the other way, $\theta_2 = 228.19^\circ$. The crank turns through 191.3° on one stroke and 168.7° on the other, a time ratio of 1.134.

</details>

**Exercise 4.** A slider-crank has $r = 50$ mm and $l = 200$ mm, and the crank turns at a constant 3000 rpm. At $\theta = 60^\circ$ find $\phi$, the slider position, velocity and acceleration, and compare the acceleration with the two-term approximation. Also find the acceleration at top dead centre.

<details>
<summary>Answer</summary>

$\omega = 314.16$ rad/s, $\sin\phi = r\sin\theta/l = 0.2165$, so $\phi = 12.50^\circ$ and $l\cos\phi = 0.1953$ m.

Position: $x = 0.05\cos 60^\circ + 0.1953 = 0.2203$ m.

Velocity:

```math
v = -r\omega\sin\theta - \frac{r^2\omega\cos\theta\sin\theta}{l\cos\phi} = -13.60 - 1.74 = -15.35 \text{ m/s}
```

Acceleration, term by term:

```math
a = -2467.4 + 631.8 - 15.5 = -1851 \text{ m/s}^2
```

The approximation gives $-4934.8(\cos 60^\circ + 0.25\cos 120^\circ) = -1850.6$ m/s², within 0.03% of the exact value.

At top dead centre, $\phi = 0$ and $a = -r\omega^2(1 + r/l) = -4934.8 \times 1.25 = -6169$ m/s², about 630 g. This is the source of the large inertia forces in high-speed engines.

</details>

**Exercise 5.** A valve cam lifts its follower 10 mm over 90° of cam rotation and turns at 1500 rpm. Find the maximum follower velocity and acceleration for a simple harmonic rise and for a cycloidal rise, and say which you would use next to a dwell.

<details>
<summary>Answer</summary>

$\omega = 157.08$ rad/s, $\beta = \pi/2$ rad, $h = 10$ mm.

Simple harmonic: $v_{\max} = \pi h\omega/(2\beta) = 1.571$ m/s and $a_{\max} = \pi^2 h\omega^2/(2\beta^2) = 493.5$ m/s², at $\theta = 0$ and $\theta = \beta$, where the acceleration jumps from zero (dwell) to its peak.

Cycloidal: $v_{\max} = 2h\omega/\beta = 2.0$ m/s and $a_{\max} = 2\pi h\omega^2/\beta^2 = 628.3$ m/s², at $\theta = \beta/4$. The acceleration is zero at both ends, so there is no jump.

The cycloidal law has the higher peak acceleration but finite jerk, which is why it is preferred next to dwells and in high-speed cams.

</details>

**Exercise 6.** A function-generating four-bar with ground link $d = 120$ mm must give rocker angles $\theta_4 = 90.32^\circ$, $103.37^\circ$ and $129.00^\circ$ at crank angles $\theta_2 = 30^\circ$, $90^\circ$ and $150^\circ$. Find $K_1$, $K_2$, $K_3$ and the link lengths.

<details>
<summary>Answer</summary>

The three Freudenstein equations $K_1\cos\theta_4 - K_2\cos\theta_2 + K_3 = \cos(\theta_2 - \theta_4)$ are

```math
\begin{aligned}
-0.00559K_1 - 0.86603K_2 + K_3 &= 0.49516 \\
-0.23124K_1 + K_3 &= 0.97290 \\
-0.62932K_1 + 0.86603K_2 + K_3 &= 0.93358
\end{aligned}
```

Their solution is $K_1 = 2.999$, $K_2 = 1.333$, $K_3 = 1.666$. Then $a = d/K_1 = 40.0$ mm, $c = d/K_2 = 90.0$ mm and $b = \sqrt{a^2 + c^2 + d^2 - 2acK_3} = 110.0$ mm. The precision points were taken, rounded to 0.01°, from the linkage of the worked example, and the synthesis recovers it.

</details>

## References

- Norton, R. L., *Design of Machinery: An Introduction to the Synthesis and Analysis of Mechanisms and Machines*, 5th ed., McGraw-Hill, 2012.
- Uicker, J. J., Pennock, G. R., and Shigley, J. E., *Theory of Machines and Mechanisms*, 5th ed., Oxford University Press, 2017.
- Erdman, A. G., Sandor, G. N., and Kota, S., *Mechanism Design: Analysis and Synthesis*, Vol. 1, 4th ed., Prentice Hall, 2001.
- Freudenstein, F., "Approximate synthesis of four-bar linkages", *Transactions of the ASME*, 77, 853–861, 1955.
- Hibbeler, R. C., *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
