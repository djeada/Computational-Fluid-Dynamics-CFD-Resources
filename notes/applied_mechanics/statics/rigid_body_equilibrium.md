# Rigid Body Equilibrium

A rigid body can translate and rotate, so its equilibrium requires both the resultant force and the resultant moment to vanish. These equations give the support reactions of beams, brackets, machine parts, vehicle axles and landing gear, and they are the first step of every structural calculation: internal forces, stresses and deflections all start from the reactions. This note states the equilibrium equations in 2D and 3D, models the common supports, and explains when the supports determine the reactions uniquely (statical determinacy) and when they fail to hold the body at all (improper constraint).

## Problem Statement

A body, assumed rigid, carries known loads: point forces $\mathbf{F}_k$ (N) at known points, couples $\mathbf{C}_k$ (N m) and distributed loads $w(x)$ (N/m) or pressures (Pa). It is held by supports whose types and positions are known. The task is to find the support reactions, and sometimes the load or position at which equilibrium is lost. The assumptions are:

- deformations are small enough that the equilibrium equations can be written on the undeformed geometry;
- supports are ideal: a roller is frictionless, a pin has no moment resistance, a fixed support allows no motion;
- the body is in static equilibrium (or moves with constant velocity, which is the same thing in an inertial frame).

The governing equations are

$$
\sum \mathbf{F} = \mathbf{0},
\qquad \sum \mathbf{M}_O = \sum \mathbf{r} \times \mathbf{F} + \sum
\mathbf{C} = \mathbf{0}
$$

where $O$ is any point and $\mathbf{r}$ is the position vector from $O$ to a point on the line of action of each force. They give 3 scalar equations in a plane and 6 in space.

## Equilibrium Equations

### Why One Moment Point Suffices

The moment about another point $P$ is $`\mathbf{M}_P = \mathbf{M}_O + \mathbf{r}_{PO} \times \sum\mathbf{F}`$. When $\sum \mathbf{F} = \mathbf{0}$, the moment is the same about every point, so if it vanishes about one point it vanishes about all. Writing moment equations about several points therefore adds no new information, but it can give equations that each contain only one unknown.

### Two Dimensions

For forces in the $xy$-plane and couples about $z$:

$$
\sum F_x = 0,
\qquad \sum F_y = 0,
\qquad \sum M_O = 0
$$

with $M_O = x F_y - y F_x$ for a force at $(x, y)$, counterclockwise positive. Two alternative sets are also independent:

| Equation set | Condition for independence |
| --- | --- |
| $\sum F_x = 0$, $\sum M_A = 0$, $\sum M_B = 0$ | The line $AB$ is not perpendicular to the $x$-axis |
| $\sum M_A = 0$, $\sum M_B = 0$, $\sum M_C = 0$ | $A$, $B$, $C$ are not collinear |

Choose moment points where two unknown reaction lines intersect; each equation then contains a single unknown.

### Three Dimensions

In space there are six equations:

$$
\sum F_x = \sum F_y = \sum F_z = 0,
\qquad \sum M_x = \sum M_y = \sum M_z = 0
$$

The moment about an axis through $O$ with unit vector $\mathbf{u}$ is $\mathbf{u}\cdot(\mathbf{r}\times\mathbf{F})$. Moments about an axis that passes through several unknown forces, or is parallel to them, remove those forces from the equation.

### Distributed Loads

A distributed load $w(x)$ (N/m) on a beam has the resultant $`R = \int w\,dx`$, the area under the load diagram, acting through the centroid of that area at $`\bar{x} = \int x\,w\,dx / R`$. A uniform load $w$ over a length $a$ is therefore equivalent to $wa$ at mid-length, and a triangular load rising to $w_0$ is equivalent to $w_0 a/2$ at two thirds of the length from the zero end. The replacement is valid for the reactions and the overall equilibrium only; internal forces must be computed with the actual distribution (see [Shear and Moment Diagrams](../strength_materials/shear_moment.md)). Centroids of common shapes are in [Center of Mass and Centroids](./center_of_mass.md).

## Supports and Their Reactions

A support provides a force in every direction in which it prevents translation and a couple about every axis about which it prevents rotation.

| Planar support | Prevents | Reactions | Unknowns |
| --- | --- | --- | --- |
| Roller, rocker, smooth surface | Motion normal to the surface | One force normal to the surface | 1 |
| Short link or cable | Motion along the link | One force along the link (a cable only pulls) | 1 |
| Pin (hinge) | Translation in both directions | Two force components $R_x$, $R_y$ | 2 |
| Pin in a smooth slot | Motion normal to the slot | One force normal to the slot | 1 |
| Fixed (built-in) | Translation and rotation | $R_x$, $R_y$ and a couple $M$ | 3 |

| Spatial support | Reactions | Unknowns |
| --- | --- | --- |
| Ball on a smooth surface | One normal force | 1 |
| Ball and socket | Three force components | 3 |
| Single journal bearing | Two forces normal to the shaft and two couples about those axes | 4 |
| Journal bearings in an aligned pair, or a bearing with other supports | Two forces each; the couples are not developed | 2 per bearing |
| Hinge | Three forces and two couples (rotation about the hinge axis is free) | 5 |
| Fixed | Three forces and three couples | 6 |

The couples at a bearing or hinge exist only if the bearing alone must prevent the shaft from tilting. When a shaft runs in two aligned bearings, the tilt is prevented by the pair of forces and the couples are omitted.

## Two-Force and Three-Force Members

A member loaded only at two points, with no couples, is a two-force member. Force equilibrium makes the two forces equal and opposite, and moment equilibrium about either point makes them collinear: both act along the line joining the two points. Truss bars, links and struts are two-force members, and the direction of their force is known before any calculation.

A member loaded by exactly three forces, with no couples, is a three-force member. Moment equilibrium about the intersection of two of the lines of action shows that the third must pass through the same point: the three forces are concurrent, or else all parallel. This fixes the direction of an unknown pin reaction when the other two lines of action are known.

## Statical Determinacy and Constraint

A planar body has 3 equilibrium equations, a spatial one 6. With $r$ unknown reaction components, the count gives a necessary condition:

| Count (2D) | Classification |
| --- | --- |
| $r < 3$ | Partially constrained: the body can move under some loads |
| $r = 3$ | Determinate if the supports are proper |
| $r > 3$ | Indeterminate to degree $r - 3$ if the supports are proper |

The count is not sufficient. The reactions can be written as $\mathbf{A}\mathbf{R} = -\mathbf{F}$, where column $j$ of the $3 \times r$ matrix $\mathbf{A}$ holds the force components and the moment about the origin of a unit value of reaction $j$, and $\mathbf{F}$ holds the resultant force and moment of the loads. The supports are proper when $\mathbf{A}$ has rank 3. Two arrangements have enough reactions but rank 2:

- All reactions parallel. They cannot resist a load perpendicular to them, as with a beam on three rollers.
- All reaction lines concurrent at one point. They cannot resist a moment about that point, as with a pin and a roller whose reaction line passes through the pin.

These are improper constraints. The body starts to move, and in a real structure the supports or members are overloaded long before that, because the equations are nearly singular for supports that are close to an improper layout.

![Free-body diagram of a simply supported beam with its computed reactions, and six support layouts classified by the rank of the reaction matrix](../../../scripts/plots/statics_support_reactions/statics_support_reactions.png)

The lower six panels show the classification. Layouts (e) and (f) have three reactions, the right number, yet the rank test marks them improper; (d) has one reaction more than needed, so one reaction must come from the deformation of the beam (see [Structural Analysis](./structural_analysis.md)).

For an indeterminate body, equilibrium gives a family of reaction sets, and the actual one depends on stiffness. A beam on three supports carries a different share at the middle support if that support settles by a millimetre. Structures are often built indeterminate on purpose, because the redundancy offers an alternative load path when one member fails.

## Worked Example: Simply Supported Beam

A 6 m beam has a pin at A ($x = 0$) and a roller at B ($x = 6$ m). It carries a 10 kN point load at $x = 2$ m and a uniform load of 5 kN/m over $3 \leq x \leq 6$ m. The distributed load has the resultant $W = 5 \times 3 = 15$ kN at $x = 4.5$ m.

Horizontal equilibrium gives $A_x = 0$. Moments about A, counterclockwise positive, involve only $B_y$:

$$
\sum M_A = 6B_y - 10(2) - 15(4.5) = 0 \implies B_y = \frac{20 + 67.5}{6} = 14.58
\text{ kN}
$$

Vertical equilibrium gives $A_y = 10 + 15 - 14.58 = 10.42$ kN. As a check, moments about B: $-6A_y + 10(4) + 15(1.5) = -62.5 + 62.5 = 0$. Panel (a) of the figure shows the free-body diagram with these values, obtained by solving the $3 \times 3$ system.

## Worked Example: L-Shaped Bracket

An L-shaped bracket is built into a wall at A. Its vertical arm AB runs 0.4 m straight down from A, and its horizontal arm BC is 0.3 m long. A horizontal force of 500 N to the right acts at C. The fixed support provides $A_x$, $A_y$ and $M_A$.

$$
\sum F_x = A_x + 500 = 0 \implies A_x = -500 \text{ N},
\qquad \sum F_y = A_y = 0
$$

Point C is at $(0.3, -0.4)$ m relative to A, so the moment of the 500 N force about A is $x F_y - y F_x = 0 - (-0.4)(500) = 200$ N m, counterclockwise:

$$
\sum M_A = M_A + 200 = 0 \implies M_A = -200 \text{ N}\cdot \text{m}
$$

The wall pushes left with 500 N and resists with a clockwise couple of 200 N m. The 0.3 m arm does not enter the moment, because the force is parallel to it.

## Worked Example: Pole Held by Two Cables

A vertical pole OA of height 4 m stands on a ball-and-socket joint at $O(0, 0, 0)$. Two cables run from the top $A(0, 0, 4)$ m to ground anchors $B(-3, 2, 0)$ and $C(-3, -2, 0)$ m. A horizontal force of 2 kN in the $+x$ direction acts at A. The unknowns are $O_x$, $O_y$, $O_z$, $T_B$ and $T_C$.

The unit vectors from A to the anchors are $`\mathbf{u}_{AB} = (-3, 2, -4)/\sqrt{29}`$ and $`\mathbf{u}_{AC} = (-3, -2, -4)/\sqrt{29}`$. Take moments about O. All forces at A have the position vector $\mathbf{r} = 4\mathbf{k}$, and $4\mathbf{k}\times\mathbf{G} = (-4G_y, 4G_x, 0)$ for a resultant $\mathbf{G}$ at A, so the $x$- and $y$-moment equations require the horizontal components at A to cancel:

```math
x:\; -\frac{3(T_B + T_C)}{\sqrt{29}} + 2 = 0, \qquad
y:\; \frac{2(T_B - T_C)}{\sqrt{29}} = 0
```

Hence $T_B = T_C = \sqrt{29}/3 = 1.795$ kN. Force equilibrium of the pole gives $O_x = O_y = 0$ and $O_z = 4(T_B + T_C)/\sqrt{29} = 2.667$ kN upward, so the pole is in compression.

The $z$-moment equation reads $0 = 0$: every force passes through the axis of the pole, and the supports cannot resist a torque about that axis. The pole is free to spin about its own axis, which is harmless here but would be an improper constraint if a load had a moment about that axis.

## Common Mistakes

- Omitting a reaction component, most often the couple at a fixed support or the horizontal component at a pin.
- Placing the resultant of a distributed load at the middle of the beam rather than at the centroid of the loaded area.
- Counting reactions without checking for parallel or concurrent lines of action.
- Using the same moment sign convention inconsistently within one equation.
- Adding a reaction at a two-force member in a direction other than along the member.

## Key Takeaways

- Equilibrium of a rigid body needs $\sum \mathbf{F} = \mathbf{0}$ and $\sum \mathbf{M} = \mathbf{0}$: 3 scalar equations in 2D, 6 in 3D.
- Moments about well-chosen points or axes give equations with one unknown each.
- Each support contributes one reaction per prevented translation or rotation.
- Determinacy needs the right number of reactions and a reaction matrix of full rank; parallel or concurrent reactions are improper.
- An indeterminate body needs deformation compatibility as well as equilibrium.

## Related Scripts

- [Support Reactions and Constraint](../../../scripts/plots/statics_support_reactions/): solves the reactions of a simply supported beam from the $3 \times 3$ equilibrium system and classifies support layouts as determinate, indeterminate or improper from the rank of the reaction matrix.
- [Plane Truss Solver](../../../scripts/algorithms/statics_truss_solver/): solves a plane pin-jointed truss by the method of joints and by the direct stiffness method.
- [Composite Centroid](../../../scripts/plots/statics_composite_centroid/): computes the centroids of a T-section and of a plate with a hole and a notch from a table of parts, checks them against the polygon formula for the exact boundary, and gives the centroidal second moment of the T-section.

## Exercises

**Exercise 1.** Find the degree of static indeterminacy $r - 3$ of these planar beams: (a) cantilever (fixed at one end), (b) propped cantilever (fixed at one end, roller at the other), (c) beam on a pin and two rollers, (d) beam fixed at both ends.

<details>
<summary>Answer</summary>

- (a) $r = 3$, degree 0 (determinate)
- (b) $r = 4$, degree 1
- (c) $r = 4$, degree 1
- (d) $r = 6$, degree 3

All four layouts are proper. Each indeterminate case needs as many compatibility equations as its degree.

</details>

**Exercise 2.** A 3 m cantilever, fixed at its left end A, carries a uniform load of 4 kN/m over its full length and a 6 kN downward point load at the free end. Find the reactions at A.

<details>
<summary>Answer</summary>

$A_x = 0$ and $A_y = 4(3) + 6 = 18$ kN upward. Moments about A, counterclockwise positive:

```math
M_A - 12(1.5) - 6(3) = 0 \implies M_A = 36 \text{ kN}\cdot\text{m}
```

The reaction moment is counterclockwise.

</details>

**Exercise 3.** A uniform 5 m ladder of mass 20 kg leans against a smooth vertical wall at $60^\circ$ to the floor. Find the wall reaction, the floor normal force and friction, and the minimum floor friction coefficient for the ladder to stay put.

<details>
<summary>Answer</summary>

$W = 196.2$ N acts at mid-length. The smooth wall exerts only a horizontal force $N_w$. Moments about the foot:

```math
N_w(5\sin 60^\circ) = W(2.5\cos 60^\circ) \implies
N_w = \frac{196.2 \times 1.25}{4.330} = 56.6 \text{ N}
```

Force balance gives a floor friction of $F = N_w = 56.6$ N and $N_f = W = 196.2$ N, so $\mu_{\min} = 56.6/196.2 = 0.289$. The ladder is a three-force member: the floor resultant must pass through the point where the weight line meets the wall reaction line.

</details>

**Exercise 4.** A beam has a pin at A ($x = 0$) and a roller at B ($x = 6$ m), and overhangs to $x = 8$ m. It carries 3 kN/m between A and B and a 10 kN point load at its tip. Find $A_y$ and $B_y$, and the tip load at which the beam would lift off at A if A were a simple support.

<details>
<summary>Answer</summary>

The distributed load resultant is 18 kN at $x = 3$ m.

```math
\sum M_A = 6B_y - 18(3) - 10(8) = 0 \implies B_y = 22.3 \text{ kN}, \qquad
A_y = 18 + 10 - 22.3 = 5.67 \text{ kN}
```

With a tip load $P$, $B_y = 9 + 4P/3$ and $A_y = 18 + P - B_y = 9 - P/3$, which becomes zero at $P = 27$ kN. A larger tip load would need the pin at A to hold the beam down.

</details>

**Exercise 5.** A horizontal plate with a 400 N weight acting at $(1, 0.5)$ m is held by three vertical cables attached at $A(0, 0)$, $B(2, 0)$ and $D(1, 1)$ m. Find the three tensions. Why are only three of the six equilibrium equations useful?

<details>
<summary>Answer</summary>

All forces are parallel to $z$, so $\sum F_x$, $\sum F_y$ and $\sum M_z$ are identically zero. The remaining three equations are:

- moments about the $x$-axis (lever arm $y$): $T_D(1) = 400(0.5)$, so $T_D = 200$ N;
- moments about the $y$-axis (lever arm $x$): $T_B(2) + T_D(1) = 400(1)$, so $T_B = 100$ N;
- vertical forces: $T_A = 400 - 200 - 100 = 100$ N.

The plate is only partially constrained: a horizontal push would move it. The three cables do not lie on one line, so the plate is properly held for vertical loads.

</details>

## References

- Hibbeler, R. C., *Engineering Mechanics: Statics*, 14th ed., Pearson, 2016.
- Beer, F. P., Johnston, E. R., and Mazurek, D. F., *Vector Mechanics for Engineers: Statics*, 12th ed., McGraw-Hill Education, 2019.
- Meriam, J. L., Kraige, L. G., and Bolton, J. N., *Engineering Mechanics: Statics*, 9th ed., Wiley, 2018.
- Pytel, A., and Kiusalaas, J., *Engineering Mechanics: Statics*, 4th ed., Cengage Learning, 2016.
- Hibbeler, R. C., *Structural Analysis*, 10th ed., Pearson, 2018.
