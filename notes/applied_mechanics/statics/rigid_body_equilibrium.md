# Rigid Body Equilibrium

Rigid body equilibrium extends particle equilibrium by accounting for the size and shape of objects. Unlike particles, rigid bodies can experience rotational effects due to moments, requiring both force and moment balance for complete equilibrium analysis.

## Conditions for Rigid Body Equilibrium

A rigid body is in static equilibrium when the resultant force and the resultant moment about any point are both zero:

$$\sum \mathbf{F} = 0$$
$$\sum \mathbf{M}_O = 0$$

These two vector equations ensure that the body has no tendency to translate or rotate.

## Two-Dimensional Equilibrium

### Equilibrium Equations in 2D

For coplanar force systems, the general equilibrium conditions reduce to three scalar equations:

$$\sum F_x = 0$$
$$\sum F_y = 0$$
$$\sum M_O = 0$$

These three equations can solve for at most **three unknowns**. Alternative equation sets include:
- Two moment equations and one force equation: $\sum M_A = 0$, $\sum M_B = 0$, $\sum F_x = 0$
- Three moment equations about non-collinear points: $\sum M_A = 0$, $\sum M_B = 0$, $\sum M_C = 0$

### Moment of a Force

The moment of a force $\mathbf{F}$ about point O is defined as:

$$\mathbf{M}_O = \mathbf{r} \times \mathbf{F}$$

where $\mathbf{r}$ is the position vector from O to any point on the line of action of $\mathbf{F}$. In 2D, the scalar moment is:

$$M_O = Fd$$

where $d$ is the perpendicular distance from O to the line of action.

## Three-Dimensional Equilibrium

### Equilibrium Equations in 3D

In three dimensions, the equilibrium conditions yield six scalar equations:

$$\sum F_x = 0, \quad \sum F_y = 0, \quad \sum F_z = 0$$
$$\sum M_x = 0, \quad \sum M_y = 0, \quad \sum M_z = 0$$

These six equations can solve for at most **six unknowns**.

## Support Reactions

### Common 2D Supports

| Support Type | Reactions Provided | Unknowns |
|---|---|---|
| Roller | One force (normal to surface) | 1 |
| Pin (hinge) | Two force components ($R_x$, $R_y$) | 2 |
| Fixed (cantilever) | Two force components and a moment ($R_x$, $R_y$, $M$) | 3 |
| Link | One force along the link axis | 1 |

### Common 3D Supports

| Support Type | Reactions Provided | Unknowns |
|---|---|---|
| Ball and socket | Three force components | 3 |
| Roller on surface | One normal force | 1 |
| Fixed support | Three forces and three moments | 6 |
| Journal bearing | Two forces and two moments | 4 |

## Statical Determinacy and Indeterminacy

A structure is **statically determinate** when the number of unknown reactions equals the number of independent equilibrium equations:
- 2D: 3 unknowns → determinate
- 3D: 6 unknowns → determinate

If the number of unknowns exceeds the number of equilibrium equations, the structure is **statically indeterminate**. The degree of indeterminacy is:

$$n = r - e$$

where $r$ is the number of unknown reactions and $e$ is the number of equilibrium equations. A structure with fewer unknowns than equations is a **mechanism** (unstable).

## Two-Force and Three-Force Members

### Two-Force Members

A **two-force member** has forces applied at exactly two points. For equilibrium:
- The two forces must be equal in magnitude
- Opposite in direction
- Collinear (acting along the line connecting the two points)

$$\mathbf{F}_A = -\mathbf{F}_B$$

Two-force members are always in pure tension or compression.

### Three-Force Members

A **three-force member** has forces applied at exactly three points. For equilibrium:
- The three forces must be concurrent (all lines of action meet at one point) or parallel
- This condition is useful for determining force directions without solving equations

## Worked Example 1: Simply Supported Beam

A 6 m simply supported beam carries a 10 kN point load at 2 m from the left support A and a 5 kN/m uniformly distributed load over the rightmost 3 m. Support A is a pin and support B is a roller at the right end.

**Given:**
- Beam length: $L = 6$ m
- Point load: $P = 10$ kN at $x = 2$ m from A
- Distributed load: $w = 5$ kN/m over the last 3 m (from $x = 3$ m to $x = 6$ m)
- Support A: pin, Support B: roller

**Find:** Support reactions $A_x$, $A_y$, and $B_y$.

**Solution:**

The resultant of the distributed load is:
$$W = w \times 3 = 5 \times 3 = 15 \text{ kN}$$

acting at the centroid of the loaded region, i.e., at $x = 4.5$ m from A.

**Equilibrium equations:**

Horizontal equilibrium:
$$\sum F_x = A_x = 0$$

Moment about A (counterclockwise positive):
$$\sum M_A = -P(2) - W(4.5) + B_y(6) = 0$$
$$-10(2) - 15(4.5) + 6B_y = 0$$
$$B_y = \frac{20 + 67.5}{6} = 14.58 \text{ kN}$$

Vertical equilibrium:
$$\sum F_y = A_y + B_y - P - W = 0$$
$$A_y = 10 + 15 - 14.58 = 10.42 \text{ kN}$$

**Results:** $A_x = 0$, $A_y = 10.42$ kN, $B_y = 14.58$ kN.

## Worked Example 2: L-Shaped Bracket

An L-shaped bracket is fixed at wall point A and carries a 500 N horizontal force at the free end C. The vertical segment AB is 0.4 m and the horizontal segment BC is 0.3 m.

**Given:**
- Vertical arm: $AB = 0.4$ m
- Horizontal arm: $BC = 0.3$ m
- Applied force at C: $F = 500$ N (horizontal, to the right)

**Find:** Reactions at the fixed support A.

**Solution:**

At the fixed support A there are three unknowns: $A_x$, $A_y$, and $M_A$.

Horizontal equilibrium:
$$\sum F_x = A_x + 500 = 0 \implies A_x = -500 \text{ N}$$

Vertical equilibrium:
$$\sum F_y = A_y = 0$$

Moment about A (counterclockwise positive):
$$\sum M_A = M_A + 500(0.4) = 0$$
$$M_A = -200 \text{ N·m}$$

**Results:** $A_x = -500$ N (leftward), $A_y = 0$, $M_A = -200$ N·m (clockwise).

## Practical Tips

### Choosing the Moment Point
- Select a point through which the maximum number of unknown forces pass
- This eliminates those unknowns from the moment equation, simplifying the algebra

### Free Body Diagram Checklist
1. Isolate the body from all supports and connections
2. Show all external forces including gravity
3. Replace each support with its corresponding reactions
4. Label all known and unknown quantities with assumed directions

### Sign Convention
- Establish consistent positive directions at the outset
- A negative result simply means the assumed direction was opposite to the actual direction

## Applications

### Civil Engineering
- **Bridge design**: Determining support reactions under traffic and self-weight loads
- **Building frames**: Analyzing load paths from roof to foundation
- **Retaining walls**: Evaluating overturning and sliding stability

### Mechanical Engineering
- **Machine frames**: Ensuring stability under operational loads
- **Robotic arms**: Calculating joint reactions for actuator sizing
- **Vehicle chassis**: Analyzing static load distribution among wheels

### Aerospace Engineering
- **Aircraft on ground**: Landing gear reaction analysis
- **Satellite structures**: Ensuring equilibrium during launch loads
- **Wing structures**: Evaluating root reactions from aerodynamic loads

Rigid body equilibrium is the essential bridge between particle equilibrium and full structural analysis. Mastery of free body diagrams and the systematic application of force and moment balance equations forms the basis for analyzing trusses, frames, beams, and all other structural systems.
