# Free Body Diagrams

Free body diagrams (FBDs) are the single most important tool in engineering mechanics. They provide a systematic graphical representation of all forces and moments acting on a body, enabling the correct application of equilibrium equations and the determination of unknown reactions, internal forces, and loading effects.

## Purpose and Importance

A free body diagram isolates a body (or portion of a body) from its surroundings and replaces all contacts, supports, and connections with the forces and moments they exert. The FBD serves as:

- **A visual inventory** of every external influence on the body
- **The starting point** for writing equilibrium equations
- **A communication tool** that clearly conveys the analyst's assumptions
- **An error-checking device** for verifying completeness and consistency

Without a correct FBD, the equilibrium equations will be incomplete or wrong, leading to incorrect results regardless of the mathematical skill applied.

## Steps for Constructing a Free Body Diagram

### Step 1: Select the Body to Isolate
Choose the body or system of interest. This could be:
- A single rigid body
- A portion of a structure obtained by cutting through members
- A system of connected bodies analyzed together

### Step 2: Detach the Body from All Supports and Contacts
Mentally remove the body from its environment, including:
- Supports (pins, rollers, fixed walls)
- Connections to other bodies (cables, ropes, joints)
- Contact surfaces (ground, adjacent members)

### Step 3: Draw the Isolated Body
Sketch the outline of the body clearly, maintaining approximate proportions and geometry.

### Step 4: Apply All External Forces and Moments
Add every force and moment acting on the body:
- **Known forces**: Show with correct magnitude, direction, and point of application
- **Unknown reactions**: Show with assumed directions (to be determined by equilibrium)
- **Weight**: Applied at the center of gravity, directed downward

### Step 5: Label All Forces and Establish a Coordinate System
- Assign variable names to unknown forces and moments
- Indicate dimensions and angles
- Establish a clear sign convention and coordinate axes

## Types of External Loads

### Concentrated (Point) Forces
A force applied at a single point on the body:

$$\mathbf{F} = F_x\mathbf{i} + F_y\mathbf{j}$$

Examples include: a cable pulling on a bracket, a wheel load on a bridge, or a weight hanging from a hook.

### Distributed Loads
Forces spread over a length, area, or volume:

**Uniform load** (constant intensity $w$, force per unit length):

$$R = wL, \quad \text{acting at } \bar{x} = \frac{L}{2}$$

**Linearly varying load** (triangular distribution from $0$ to $w_{\max}$):

$$R = \frac{1}{2}w_{\max}L, \quad \text{acting at } \bar{x} = \frac{2L}{3} \text{ from the zero end}$$

**General distributed load** $w(x)$:

$$R = \int_0^L w(x)\,dx, \quad \bar{x} = \frac{\int_0^L x\,w(x)\,dx}{\int_0^L w(x)\,dx}$$

### Applied Moments (Couples)
External torques or couples applied directly to the body:

$$\mathbf{M} = M\,\hat{\mathbf{k}}$$

These appear as curved arrows on the FBD and represent pure rotational effects without a net force.

## Support Reactions

Each type of support provides specific reactions that must be included on the FBD.

### 2D Support Types

**Roller Support**:
- Allows translation along the surface and rotation
- Provides one reaction: normal force perpendicular to the surface
- Number of unknowns: 1

**Pin (Hinge) Support**:
- Allows rotation but prevents all translation
- Provides two reaction components: $R_x$ and $R_y$
- Number of unknowns: 2

**Fixed (Clamped) Support**:
- Prevents all translation and rotation
- Provides two force reactions and one moment reaction: $R_x$, $R_y$, $M$
- Number of unknowns: 3

**Cable or Rope**:
- Can only pull (tension only), always directed along the cable
- Provides one reaction: tension $T$
- Number of unknowns: 1

**Smooth Contact Surface**:
- Reaction is normal to the contact surface
- Number of unknowns: 1

### 3D Support Types

**Ball-and-Socket Joint**:
- Prevents translation in all three directions
- Reactions: $R_x$, $R_y$, $R_z$
- Number of unknowns: 3

**Journal Bearing**:
- Prevents translation in two directions perpendicular to the shaft
- Reactions: Two force components perpendicular to the shaft axis
- Number of unknowns: 2

**Fixed Support (3D)**:
- Prevents all translation and rotation
- Reactions: $R_x$, $R_y$, $R_z$, $M_x$, $M_y$, $M_z$
- Number of unknowns: 6

## Internal Forces and Method of Sections

When analyzing internal forces, a cut is made through the structure to expose the internal actions at that section.

### Internal Force Components
At any cut section of a beam, the internal forces consist of:

**Normal Force** $N$: Axial force perpendicular to the cut (along the member axis)

**Shear Force** $V$: Force parallel to the cut face

**Bending Moment** $M$: Couple acting in the plane of the cut

The sign conventions for internal forces in beams are:
- Positive $N$: tension (member being pulled apart)
- Positive $V$: causes clockwise rotation of the isolated segment
- Positive $M$: causes the beam to sag (concave upward)

### Procedure for Internal Force Analysis
1. Draw the FBD of the entire structure and solve for external reactions
2. Cut the structure at the section of interest
3. Draw the FBD of either segment, showing internal forces at the cut
4. Apply equilibrium to the isolated segment to find $N$, $V$, and $M$

## Example 1: Simply Supported Beam

**Given**:
- A beam of length $L = 8$ m with a pin at $A$ (left) and roller at $B$ (right)
- A concentrated load $P = 20$ kN at $x = 3$ m from $A$
- A uniform distributed load $w = 5$ kN/m from $x = 5$ m to $x = 8$ m

**Find**: Support reactions at $A$ and $B$

**Solution**:

First, replace the distributed load with its resultant:

$$R_w = w \times 3 = 5 \times 3 = 15 \text{ kN, acting at } x = 5 + 1.5 = 6.5 \text{ m from } A$$

The FBD shows: pin reactions $A_x$, $A_y$ at the left, roller reaction $B_y$ at the right, load $P$ downward at $x = 3$ m, and resultant $R_w$ downward at $x = 6.5$ m.

Moment equilibrium about $A$:

$$\sum M_A = 0: \quad -P(3) - R_w(6.5) + B_y(8) = 0$$

$$B_y = \frac{20(3) + 15(6.5)}{8} = \frac{60 + 97.5}{8} = 19.69 \text{ kN}$$

Vertical force equilibrium:

$$\sum F_y = 0: \quad A_y + B_y - P - R_w = 0$$

$$A_y = 20 + 15 - 19.69 = 15.31 \text{ kN}$$

Horizontal force equilibrium:

$$\sum F_x = 0: \quad A_x = 0$$

## Example 2: Frame Structure

**Given**:
- An L-shaped frame with a fixed support at $A$ at the base
- Horizontal member $AB$ of length $4$ m, vertical member $BC$ of length $3$ m
- A horizontal force $F = 10$ kN applied at $C$

**Find**: Reactions at the fixed support $A$

**Solution**:

The FBD of the entire frame at the fixed support $A$ has reactions $A_x$, $A_y$, and moment $M_A$.

Force equilibrium:

$$\sum F_x = 0: \quad A_x + F = 0 \implies A_x = -10 \text{ kN}$$

$$\sum F_y = 0: \quad A_y = 0$$

Moment equilibrium about $A$:

$$\sum M_A = 0: \quad M_A + F \times 3 = 0$$

$$M_A = -10 \times 3 = -30 \text{ kN·m (clockwise)}$$

## Example 3: Truss Joint Analysis

**Given**:
- A truss joint $C$ where three members meet
- External load at joint $C$: $P = 50$ kN downward
- Member $CA$ is inclined at $45°$ to the horizontal
- Member $CB$ is horizontal
- Member $CD$ is vertical

**Find**: Forces in members $CA$, $CB$, and $CD$

**Solution**:

Isolate joint $C$ and draw its FBD showing all member forces as tensions (pulling away from the joint). Apply equilibrium:

Vertical equilibrium:

$$\sum F_y = 0: \quad F_{CA}\sin 45° + F_{CD} - P = 0$$

Horizontal equilibrium:

$$\sum F_x = 0: \quad F_{CA}\cos 45° + F_{CB} = 0$$

From the geometry and loading, solving simultaneously:

$$F_{CA}\sin 45° + F_{CD} = 50$$

If $F_{CD} = 0$ (two-force member condition not applicable here, additional information needed), with an assumed $F_{CD} = 20$ kN (tension):

$$F_{CA} = \frac{50 - 20}{\sin 45°} = \frac{30}{0.707} = 42.43 \text{ kN (tension)}$$

$$F_{CB} = -42.43\cos 45° = -30 \text{ kN (compression)}$$

The negative sign indicates that member $CB$ is in compression, opposite to the assumed tension direction.

## Common Mistakes

### Critical Errors to Avoid
1. **Missing forces**: Forgetting to include weight, internal reactions, or applied loads
2. **Incorrect support reactions**: Showing too many or too few reaction components for a given support type
3. **Drawing forces on the wrong body**: Including forces that act on adjacent bodies rather than the isolated body
4. **Double-counting forces**: Including both the applied load and its reaction on the same FBD
5. **Wrong direction of internal forces**: At a cut section, the internal forces on opposite faces must be equal and opposite

### Sign Convention Pitfalls
- Inconsistent positive directions between different FBDs of the same system
- Forgetting that a negative result simply means the assumed direction was wrong
- Mixing up moment signs when summing about different points

## Best Practices

1. **Always draw the FBD before writing equations**: Never skip this step, regardless of how simple the problem appears
2. **Include all dimensions and angles** on the diagram for reference
3. **Use consistent notation**: Label all forces clearly with unique variable names
4. **Verify static determinacy**: Confirm that the number of unknowns equals the number of independent equilibrium equations
5. **Check your results**: Sum moments about an alternative point to verify the solution
6. **Show the coordinate system** with clear positive directions
7. **Indicate assumed directions** for unknown forces; let the algebra determine the correct sign
8. **Replace distributed loads** with their equivalent resultant forces for reaction calculations

## Applications Across Engineering

### Structural Analysis
- Determining support reactions for buildings and bridges
- Analyzing internal forces in beams, columns, and trusses
- Evaluating load paths through complex frame structures

### Machine Design
- Gear and bearing force analysis
- Shaft loading diagrams for deflection and stress calculations
- Linkage mechanism force transmission

### Biomechanics
- Analyzing forces in human joints and muscles
- Prosthetic device load analysis
- Ergonomic assessment of tool usage

Free body diagrams are indispensable at every level of mechanics, from introductory statics through advanced structural dynamics and finite element analysis. Developing the discipline to draw complete, accurate FBDs is the single most effective way to avoid errors in engineering analysis.
