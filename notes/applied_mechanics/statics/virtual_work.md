# Virtual Work and Stability of Equilibrium

The principle of virtual work replaces the force and moment balances of every body in a system by one scalar equation per degree of freedom. For linkages, mechanisms and machines connected by pins, sliders and rigid links, it gives the relation between input and output forces without computing any internal pin forces. Written with the potential energy, it also decides whether an equilibrium is stable, which is the starting point of buckling theory. The same principle, applied to deformable bodies, gives the unit-load method of [Structural Analysis](./structural_analysis.md) and the weak form on which the [Finite Element Method](../../numerical/fem/intro.md) is built, and its dynamic extension leads to [Lagrangian Mechanics](../dynamics/lagrangian_mechanics.md).

## Problem Statement

A system of rigid bodies is connected to each other and to the ground by ideal constraints, and its configuration is described by $n$ independent generalized coordinates $q_1, \dots, q_n$ (angles in rad, lengths in m). Known applied forces and couples act on it: loads, weights, spring forces. The tasks are:

- to find the configuration $\mathbf{q}$ in which the system is in equilibrium under given loads, or the load needed to hold a given configuration;
- to decide whether that equilibrium is stable, neutral or unstable, and at which load it stops being stable.

The assumptions are that the bodies are rigid, that the constraints do no work in any displacement they allow (smooth contacts, frictionless pins, inextensible links, rolling without slip), and that friction, if present, is treated as an applied force. The governing statements are the principle of virtual work and, for conservative forces, the stationarity and convexity of the potential energy $V(\mathbf{q})$:

```math
\delta W = \sum_{i=1}^{n} Q_i\,\delta q_i = 0 \;\; \text{for all } \delta q_i
\qquad\Longleftrightarrow
\qquad \frac{\partial V}{\partial q_i} = 0,
\qquad \text{stable if } \left[\frac{\partial^2 V}{\partial q_i\,\partial q_j}\right]
\text{ is positive definite}
```

## Virtual Displacements and Virtual Work

A virtual displacement $\delta\mathbf{r}$ is an imagined, infinitesimal change of configuration that the constraints allow, made at a fixed instant with the forces held at their current values. It does not have to happen; it is a test of the force balance. The virtual work of a force $\mathbf{F}$ at a point that moves by $\delta\mathbf{r}$, and of a couple $\mathbf{C}$ on a body that rotates by $\delta\boldsymbol{\theta}$, is

$$
\delta W = \mathbf{F}\cdot\delta\mathbf{r} + \mathbf{C}\cdot\delta\boldsymbol{\theta}
$$

For a rigid body, any virtual displacement is a translation $\delta\mathbf{r}_O$ of a reference point plus a rotation $\delta\boldsymbol{\theta}$, so a point $P$ moves by $`\delta\mathbf{r}_P = \delta\mathbf{r}_O + \delta\boldsymbol{\theta}\times\mathbf{r}_{OP}`$. Summing over all forces and using $\mathbf{F}\cdot(\delta\boldsymbol{\theta}\times\mathbf{r}) = \delta\boldsymbol{\theta}\cdot(\mathbf{r}\times\mathbf{F})$:

$$
\delta W = \left(\sum\mathbf{F}\right)\cdot\delta\mathbf{r}_O +
\left(\sum\mathbf{M}_O\right)\cdot\delta\boldsymbol{\theta}
$$

$\delta W$ vanishes for every $\delta\mathbf{r}_O$ and $\delta\boldsymbol{\theta}$ if and only if $\sum\mathbf{F} = \mathbf{0}$ and $\sum\mathbf{M}_O = \mathbf{0}$. Virtual work is therefore an equivalent statement of equilibrium, not a new law.

## The Principle for Connected Bodies

For a system of bodies, apply the result to each body and add. The forces between bodies come in equal and opposite pairs, and an ideal constraint does no net work in any displacement it permits:

| Constraint | Why its virtual work is zero |
| --- | --- |
| Smooth surface or roller | The reaction is normal to the surface, the allowed displacement tangential |
| Frictionless pin between two bodies | Equal and opposite forces act at the same point, which moves by the same $\delta\mathbf{r}$ on both bodies |
| Rigid link or inextensible cable | Equal and opposite forces along the link; its length cannot change |
| Fixed pin to the ground | The point does not move |
| Rolling without slip | The contact point has zero velocity, so zero virtual displacement |

The principle follows: a system with ideal constraints is in equilibrium if and only if the virtual work of the applied forces alone vanishes for every virtual displacement compatible with the constraints. The reactions and internal pin forces never enter. Friction does work in sliding and must be included as an applied force, with its magnitude from the Coulomb law of [Friction](./friction.md).

### Generalized Coordinates and Generalized Forces

If the position of every point of application can be written as $\mathbf{r}_k(q_1, \dots, q_n)$, then $`\delta\mathbf{r}_k = \sum_i (\partial\mathbf{r}_k/\partial q_i)\,\delta q_i`$ and

```math
\delta W = \sum_i Q_i\,\delta q_i,
\qquad Q_i = \sum_k \mathbf{F}_k\cdot \frac{\partial\mathbf{r}_k}{\partial q_i}
```

The generalized force $Q_i$ has units of force for a length coordinate and of moment for an angle. Because the $\delta q_i$ are independent, equilibrium requires $Q_i = 0$ for each $i$: one equation per degree of freedom, however many bodies the system has.

### Procedure

1. Count the degrees of freedom and choose generalized coordinates; a single-degree-of-freedom linkage needs one angle.
2. Draw the system displaced, and mark only the applied (active) forces: loads, weights, spring forces, friction.
3. Write the position coordinate of each force's point of application, measured from a fixed origin along the force's line of action, as a function of $q$.
4. Differentiate to get the virtual displacements, $`\delta y = (dy/dq)\,\delta q`$.
5. Add the virtual works with signs (positive when the force and the displacement point the same way), set the coefficient of $\delta q$ to zero and solve.

## Worked Example: Toggle Mechanism

Two links AB and BC, each of length $L$, are pinned at A to the ground and at C to a slider on a horizontal guide through A. Both links make the angle $\theta$ with the guide. A vertical force $P$ pushes the knee B down, and the slider presses on a workpiece that resists with a horizontal force $F$. Find $F$ in terms of $P$.

With A at the origin, B is at height $y_B = L\sin\theta$ and C at $x_C = 2L\cos\theta$, so

```math
\delta y_B = L\cos\theta\,\delta\theta,
\qquad \delta x_C = -2L\sin\theta\,\delta\theta
```

$P$ acts in $-y$ and $F$ on the slider in $-x$:

```math
\delta W = -P\,\delta y_B - F\,\delta
x_C = \left(-PL\cos\theta + 2FL\sin\theta\right)\delta\theta = 0 \implies
F = \frac{P}{2\tan\theta}
```

The mechanical advantage $F/P = 1/(2\tan\theta)$ grows without bound as the links straighten. With $P = 200$ N at $\theta = 5^\circ$, $F = 1.14$ kN. Toggle clamps, stone crushers and the locking linkages of landing gear use this; near $\theta = 0$, small elastic deflections and clearances limit the force that is actually achieved. Equilibrium of each link separately would have needed the pin forces at A, B and C, six unknowns more.

## Potential Energy

A force is conservative if its work depends only on the start and end positions, so it can be written as $\delta W = -\delta V$ with a potential energy $V(\mathbf{q})$ (J). The two that occur in statics are:

| Force | Potential energy | Notes |
| --- | --- | --- |
| Weight $W$ at height $y$ of its point of application | $V_g = W y$ | $y$ measured upward from any datum |
| Linear spring of stiffness $k$ (N/m), stretch $s$ from unstretched length | $V_e = \tfrac{1}{2}k s^2$ | Same for compression ($s < 0$) |
| Torsional spring of stiffness $k_t$ (N m/rad), twist $\phi$ | $V_e = \tfrac{1}{2}k_t\phi^2$ |  |
| Constant force $P$ in a fixed direction, point moving by $\mathbf{r}$ | $V = -\mathbf{P}\cdot\mathbf{r}$ | Covers dead loads that keep their direction |

If all applied forces are conservative, $`\delta W = -\sum_i (\partial V/\partial q_i)\,\delta q_i`$, and equilibrium becomes stationarity of the total potential energy:

$$
\frac{\partial V}{\partial q_i} = 0,
\qquad i = 1, \dots, n
$$

## Stability of Equilibrium

Disturb a system slightly from an equilibrium configuration $q_e$. If $V$ has a minimum at $q_e$, every disturbance raises the potential energy, the forces push the system back, and it is stable. At a maximum the forces push it further away, and it is unstable. For one degree of freedom:

| $d^2V/dq^2$ at $q_e$ | Equilibrium |
| --- | --- |
| $> 0$ | Stable (local minimum) |
| $< 0$ | Unstable (local maximum) |
| $= 0$ | Decided by the first non-zero higher derivative: stable if it is of even order and positive, otherwise unstable; neutral if all vanish (a ball on a flat table) |

For several degrees of freedom the equilibrium is stable when the Hessian matrix $`\partial^2 V/\partial q_i\,\partial q_j`$ is positive definite (all its eigenvalues positive). The load at which the smallest eigenvalue reaches zero is a critical load: the system either branches into a new equilibrium path (bifurcation) or reaches the largest load it can carry (a limit point).

### Worked Example: Rigid Bar on a Torsional Spring

A rigid vertical bar of length $L$ is pinned at its base, held by a torsional spring $k_t$, and carries a vertical load $P$ at its top. With $\theta$ the tilt from vertical, $V = \tfrac{1}{2}k_t\theta^2 + PL\cos\theta$, so

$$
\frac{dV}{d\theta} = k_t\theta - PL\sin\theta,
\qquad \frac{d^2V}{d\theta^2} = k_t - PL\cos\theta
$$

The upright position $\theta = 0$ is always an equilibrium, stable while $P < k_t/L$ and unstable beyond. At $P_{\mathrm{cr}} = k_t/L$ two tilted equilibria with $k_t\theta = PL\sin\theta$ branch off. This is the simplest model of [Buckling](../strength_materials/buckling.md): the Euler load of an elastic column is the same kind of critical load, with the spring replaced by the bending stiffness of the column.

## Worked Example: Spring-Loaded Linkage and Snap-Through

Two rigid bars AB and BC of length $L = 0.5$ m form a shallow inverted V. A is pinned, C rolls on a horizontal guide and is held by a horizontal spring of stiffness $k = 4$ kN/m attached to a fixed wall, unstretched when the bars make $\theta_0 = 30^\circ$ with the guide. A downward load $P$ acts at B. Bar weights are neglected.

The coordinates are $y_B = L\sin\theta$ and $x_C = 2L\cos\theta$, and the spring is compressed by $s = 2L(\cos\theta - \cos\theta_0)$ as the linkage flattens. The total potential energy is

$$
V(\theta) = 2kL^2(\cos\theta - \cos\theta_0)^2 + PL\sin\theta
$$

Setting $dV/d\theta = 0$ gives the load that holds the linkage at angle $\theta$:

$$
\frac{dV}{d\theta} = -4kL^2(\cos\theta - \cos\theta_0)\sin\theta + PL\cos\theta = 0
\implies P = 4kL(\cos\theta - \cos\theta_0)\tan\theta
$$

At $\theta = 20^\circ$ this gives $P = 4 \times 4000 \times 0.5 \times (0.9397 - 0.8660) \times 0.3640 = 214.5$ N. The same equation comes out of virtual work directly: the load does $`-PL\cos\theta\,\delta\theta`$, and the spring force $2kL(\cos\theta - \cos\theta_0)$ on C does $`2kL(\cos\theta - \cos\theta_0) \cdot 2L\sin\theta\,\delta\theta`$.

The second derivative,

$$
\frac{d^2V}{d\theta^2} = 4kL^2\left(\sin^2\theta - \cos^2\theta +
\cos\theta\cos\theta_0\right) - PL\sin\theta
$$

is $+154.5$ J/rad² at $\theta = 20^\circ$ with $P = 214.5$ N, so that equilibrium is stable. The load-angle curve $P(\theta)$ rises from zero at $\theta_0$, reaches a maximum and falls back to zero at $\theta = 0$. Its maximum, the limit point, is where $dP/d\theta = 0$, which reduces to $\cos^3\theta^* = \cos\theta_0$:

```math
\theta^* = \cos^{-1}\left(\cos^{1/3}\theta_0\right) = 17.6^\circ,
\qquad P^* = 4kL\sin^3\theta^* = 221 \text{ N}
```

![Spring-loaded two-bar linkage, its potential energy for four loads with stable and unstable equilibria marked, and the equilibrium path with the limit point](../../../scripts/plots/statics_virtual_work_stability/statics_virtual_work_stability.png)

Panel (b) shows the potential energy for four loads. Without load there are two wells at $\pm 30^\circ$ separated by an unstable maximum at $\theta = 0$, where the bars are flat. As $P$ grows, the right-hand well becomes shallower and moves towards the maximum, and beyond $P/(kL) = 0.1106$ it disappears. In panel (c), the stable branch (solid) and the unstable branch (dashed) meet at the limit point, where $d^2V/d\theta^2 = 0$. Loaded past $P^*$, the linkage has no nearby equilibrium and snaps through to the inverted configuration near $-34^\circ$. Shallow arches, domes, curved panels and bistable switches snap through the same way.

## Virtual Work for Deformable Bodies

For deformable bodies the internal forces do work in the virtual displacement as well, and the principle becomes: the external virtual work equals the internal virtual work, $`\delta W_{\mathrm{ext}} = \int \boldsymbol{\sigma} : \delta\boldsymbol{\varepsilon}\,dV`$, for every kinematically admissible $\delta\mathbf{u}$. Two uses follow:

- With real displacements and a virtual system of forces (complementary virtual work), it gives the unit-load method for deflections, $\Delta = \sum N n L/(EA)$ for trusses. The [Plane Truss Solver](../../../scripts/algorithms/statics_truss_solver/) uses it to check the midspan deflection from the stiffness method.
- With real stresses and virtual displacements, it is the weak form of the equilibrium equations. Interpolating the displacements and their variations with shape functions turns it into $\mathbf{K}\mathbf{d} = \mathbf{f}$, the finite element method; see [Weak Formulation of PDEs](../../numerical/fem/weak_formulation_pde.md).

## Common Mistakes

- Including reactions or internal pin forces, which do no virtual work under ideal constraints.
- Measuring coordinates from a moving point instead of a fixed origin, which gives wrong virtual displacements.
- Getting the sign of a weight's virtual work wrong; it is $`-W\,\delta y`$ with $y$ upward.
- Using a spring's force at the wrong configuration or forgetting that compression and extension store the same energy.
- Concluding stability from $dV/dq = 0$ alone; the second derivative (or Hessian) decides.

## Key Takeaways

- A system with ideal constraints is in equilibrium if and only if the virtual work of the applied forces vanishes for every admissible virtual displacement.
- Each generalized coordinate gives one equation $Q_i = 0$, without internal or reaction forces.
- For conservative forces, equilibrium is $\partial V/\partial q_i = 0$, and stability requires a positive definite Hessian of $V$.
- Critical loads appear where stability is lost, either at a bifurcation (buckling) or at a limit point (snap-through).
- The same principle underlies the unit-load method and the finite element method.

## Related Scripts

- [Virtual Work and Stability](../../../scripts/plots/statics_virtual_work_stability/): plots the potential energy of a spring-loaded two-bar linkage for several loads with its stable and unstable equilibria, and its equilibrium path from the virtual-work equation with the snap-through limit point.
- [Plane Truss Solver](../../../scripts/algorithms/statics_truss_solver/): solves a plane pin-jointed truss by the method of joints and by the direct stiffness method.

## Exercises

**Exercise 1.** A toggle clamp has two equal links at $\theta = 10^\circ$ to the line of the slider. A force of 500 N pushes the knee perpendicular to that line. Find the clamping force, and the angle at which the clamping force would be 5 kN.

<details>
<summary>Answer</summary>

$F = P/(2\tan\theta) = 500/(2\tan 10^\circ) = 1418$ N. For $F = 5000$ N, $\tan\theta = 500/(2 \times 5000) = 0.05$, so $\theta = 2.86^\circ$.

</details>

**Exercise 2.** A uniform ladder of weight $W = 196.2$ N rests with its foot A on a smooth floor and its top on a smooth vertical wall, at $\theta = 60^\circ$ to the floor. Use virtual work to find the horizontal force $P$ at A, directed towards the wall, that holds it. Compare with the ladder exercise of [Rigid Body Equilibrium](./rigid_body_equilibrium.md).

<details>
<summary>Answer</summary>

With the corner as origin, $x_A = L\cos\theta$ and the centre of gravity is at $y_G = (L/2)\sin\theta$. $P$ acts in $-x$ and $W$ in $-y$:

```math
\delta W = -P\,\delta x_A - W\,\delta y_G = \left(PL\sin\theta - \frac{WL}{2}\cos\theta\right)\delta\theta = 0
\implies P = \frac{W}{2\tan\theta} = 56.6 \text{ N}
```

This equals the floor friction found there: $P$ does the job of the friction force, and the wall and floor normal reactions never appear.

</details>

**Exercise 3.** A rigid bar of length $L = 1$ m on a torsional spring $k_t = 2$ kN m/rad carries a vertical load $P$ at its top. Find the critical load. For $P = 2.5$ kN, find the tilted equilibrium angle and show that it is stable.

<details>
<summary>Answer</summary>

$P_{\mathrm{cr}} = k_t/L = 2$ kN. For $P = 2.5$ kN, the upright position is unstable since $k_t - PL = -500 < 0$. The tilted equilibrium solves $`2000\,\theta = 2500\sin\theta`$, i.e. $\sin\theta/\theta = 0.8$, which gives $\theta = 1.131$ rad $= 64.8^\circ$ (by Newton iteration). There

```math
\frac{d^2V}{d\theta^2} = k_t - PL\cos\theta = 2000 - 2500\cos 64.8^\circ = 936 \text{ N}\cdot\text{m/rad} > 0
```

so the tilted equilibrium is stable. The angle is large because the spring is linear in $\theta$ while the load's moment saturates as $\sin\theta$.

</details>

**Exercise 4.** For the spring-loaded linkage of the worked example ($L = 0.5$ m, $k = 4$ kN/m, $\theta_0 = 30^\circ$), find all equilibrium angles in $-55^\circ < \theta < 55^\circ$ under $P = 150$ N, and classify them.

<details>
<summary>Answer</summary>

The equilibria are the roots of $4kL(\cos\theta - \cos\theta_0)\tan\theta = P$, that is $8000(\cos\theta - 0.8660)\tan\theta = 150$. Solving numerically:

- $\theta = 25.0^\circ$: $d^2V/d\theta^2 = +538$ J/rad², stable (on the rising branch);
- $\theta = 8.7^\circ$: $d^2V/d\theta^2 = -404$ J/rad², unstable;
- $\theta = -33.1^\circ$: $d^2V/d\theta^2 = +1333$ J/rad², stable (snapped through).

$P = 150$ N is below the limit load of 221 N, so the original stable state still exists; the unstable state between them is the top of the energy barrier.

</details>

**Exercise 5.** For the same linkage, show that the limit point satisfies $\cos^3\theta^* = \cos\theta_0$ and $P^* = 4kL\sin^3\theta^*$, and that $d^2V/d\theta^2 = 0$ there.

<details>
<summary>Answer</summary>

With $c = \cos\theta$, $s = \sin\theta$ and $c_0 = \cos\theta_0$, the equilibrium path is $P = 4kL(c - c_0)\tan\theta$. Its maximum is where

```math
\frac{d}{d\theta}\left[(c - c_0)\tan\theta\right] = -s\tan\theta + \frac{c - c_0}{c^2} = 0
```

Multiplying by $c^2$ gives $-s^2 c + c - c_0 = 0$, that is $c(1 - s^2) = c^3 = c_0$. Then $(c - c_0)\tan\theta = (c - c^3)s/c = s^3$, so $`P^* = 4kL\sin^3\theta^*`$. Substituting $`P^*`$ and $c_0 = c^3$ into $d^2V/d\theta^2$:

```math
4kL^2\left(s^2 - c^2 + c^4\right) - 4kL^2 s^4 = 4kL^2\left(s^2 - s^4 - c^2(1 - c^2)\right) = 4kL^2\left(s^2 c^2 - c^2 s^2\right) = 0
```

For $\theta_0 = 30^\circ$: $\theta^* = 17.6^\circ$ and $P^* = 4 \times 4000 \times 0.5 \times \sin^3 17.6^\circ = 221$ N.

</details>

## References

- Hibbeler, R. C., *Engineering Mechanics: Statics*, 14th ed., Pearson, 2016.
- Meriam, J. L., Kraige, L. G., and Bolton, J. N., *Engineering Mechanics: Statics*, 9th ed., Wiley, 2018.
- Beer, F. P., Johnston, E. R., and Mazurek, D. F., *Vector Mechanics for Engineers: Statics*, 12th ed., McGraw-Hill Education, 2019.
- Lanczos, C., *The Variational Principles of Mechanics*, 4th ed., University of Toronto Press, 1970 (Dover reprint, 1986).
- Timoshenko, S. P., and Gere, J. M., *Theory of Elastic Stability*, 2nd ed., McGraw-Hill, 1961.
- Thompson, J. M. T., and Hunt, G. W., *A General Theory of Elastic Stability*, Wiley, 1973.
- Bažant, Z. P., and Cedolin, L., *Stability of Structures: Elastic, Inelastic, Fracture and Damage Theories*, Oxford University Press, 1991.
