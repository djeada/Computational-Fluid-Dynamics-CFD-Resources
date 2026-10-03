# Particle Equilibrium

Particle equilibrium is the foundation of statics, dealing with bodies where all forces pass through a single point. This simplification allows us to focus on force balance without considering rotational effects, making it an ideal starting point for understanding equilibrium principles.

## Definition of a Particle

In mechanics, a **particle** is an idealized body where:

- All forces act at a single point
- The size and shape are negligible compared to the system dimensions
- Rotational effects are ignored
- Only translational equilibrium is considered

Examples of systems that can be modeled as particles:

- A suspended weight
- A joint in a pin-connected truss
- A satellite in orbit (for trajectory analysis)
- A hanging traffic light

## Conditions for Particle Equilibrium

For a particle to be in static equilibrium, the vector sum of all forces acting on it must be zero:

$$
\sum \mathbf{F} = 0
$$

In component form, this becomes:

$$
\sum F_x = 0
$$

$$
\sum F_y = 0
$$

$$
\sum F_z = 0
$$

These equations represent the mathematical statement that there is no net force in any direction.

## Two-Dimensional Particle Equilibrium

### Basic Approach

For coplanar force systems (2D problems):

1. Draw a free body diagram
2. Establish a coordinate system
3. Resolve forces into components
4. Apply equilibrium equations: $\sum F_x = 0$ and $\sum F_y = 0$
5. Solve for unknown forces

### Example 1: Suspended Weight

A 100 kg mass is suspended by two cables making angles of 30° and 45° with the horizontal.

**Given:**

- Mass: $m = 100$ kg
- Weight: $W = mg = 100 \times 9.81 = 981$ N
- Cable angles: $\theta_1 = 30^\circ$, $\theta_2 = 45^\circ$

**Solution:**

**Free Body Diagram:** Shows the mass as a particle with three forces: weight $W$ downward, and tensions $T_1$ and $T_2$ in the cables.

**Force Components:**

- $T_1$: $T_{1x} = T_1\cos(30^\circ)$, $T_{1y} = T_1\sin(30^\circ)$
- $T_2$: $T_{2x} = -T_2\cos(45^\circ)$, $T_{2y} = T_2\sin(45^\circ)$
- $W$: $W_x = 0$, $W_y = -981$ N

**Equilibrium Equations:**

$$
\sum F_x = T_1\cos(30^\circ) - T_2\cos(45^\circ) = 0
$$

$$
\sum F_y = T_1\sin(30^\circ) + T_2\sin(45^\circ) - 981 = 0
$$

From the first equation:

$$
T_1 = T_2 \frac{\cos(45^\circ)}{\cos(30^\circ)} = T_2
\frac{\sqrt{2}/2}{\sqrt{3}/2} = T_2 \frac{\sqrt{2}}{\sqrt{3}}
$$

Substituting into the second equation:

$$
T_2 \frac{\sqrt{2}}{\sqrt{3}} \times \frac{1}{2} + T_2 \frac{\sqrt{2}}{2} = 981
$$

$$
T_2 \left(\frac{\sqrt{2}}{2\sqrt{3}} + \frac{\sqrt{2}}{2}\right) = 981
$$

Solving: $T_2 = 880$ N and $T_1 = 718$ N

## Three-Dimensional Particle Equilibrium

### Vector Analysis Method

For 3D problems, we use three equilibrium equations:

$$
\sum F_x = 0, \quad \sum F_y = 0, \quad \sum F_z = 0
$$

Forces are typically expressed using:

- **Cartesian components**: $\mathbf{F} = F_x\mathbf{i} + F_y\mathbf{j} + F_z\mathbf{k}$
- **Unit vectors**: $\mathbf{F} = F\mathbf{u}$ where $\mathbf{u}$ is the unit vector along the force direction

### Unit Vector Method

For a force $\mathbf{F}$ acting from point A to point B:

1. **Position vector**: $\mathbf{r}_{AB} = (x_B - x_A)\mathbf{i} + (y_B - y_A)\mathbf{j} + (z_B - z_A)\mathbf{k}$

2. **Magnitude**: $r_{AB} = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2 + (z_B - z_A)^2}$

3. **Unit vector**: $\mathbf{u}_{AB} = \frac{\mathbf{r}_{AB}}{r_{AB}}$

4. **Force vector**: $\mathbf{F} = F\mathbf{u}_{AB}$

### Example 2: 3D Cable System

A 500 N weight is supported by three cables attached to points:

- A(3, 0, 4) m
- B(-2, 2, 5) m
- C(1, -3, 6) m

The weight is at the origin O(0, 0, 0).

**Solution:**

**Position vectors from O to attachment points:**

- $\mathbf{r}_{OA} = 3\mathbf{i} + 0\mathbf{j} + 4\mathbf{k}$
- $\mathbf{r}_{OB} = -2\mathbf{i} + 2\mathbf{j} + 5\mathbf{k}$
- $\mathbf{r}_{OC} = 1\mathbf{i} - 3\mathbf{j} + 6\mathbf{k}$

**Magnitudes:**

- $r_{OA} = \sqrt{3^2 + 0^2 + 4^2} = 5$ m
- $r_{OB} = \sqrt{(-2)^2 + 2^2 + 5^2} = \sqrt{33}$ m
- $r_{OC} = \sqrt{1^2 + (-3)^2 + 6^2} = \sqrt{46}$ m

**Unit vectors:**

- $\mathbf{u}_{OA} = \frac{3\mathbf{i} + 4\mathbf{k}}{5} = 0.6\mathbf{i} + 0.8\mathbf{k}$
- $\mathbf{u}_{OB} = \frac{-2\mathbf{i} + 2\mathbf{j} + 5\mathbf{k}}{\sqrt{33}}$
- $\mathbf{u}_{OC} = \frac{\mathbf{i} - 3\mathbf{j} + 6\mathbf{k}}{\sqrt{46}}$

**Force vectors:**

- $\mathbf{T}_A = T_A(0.6\mathbf{i} + 0.8\mathbf{k})$
- $\mathbf{T}_B = T_B\mathbf{u}_{OB}$
- $\mathbf{T}_C = T_C\mathbf{u}_{OC}$
- $\mathbf{W} = -500\mathbf{k}$ N

**Equilibrium equations:**

$$
\sum F_x = 0.6T_A - \frac{2T_B}{\sqrt{33}} + \frac{T_C}{\sqrt{46}} = 0
$$

$$
\sum F_y = \frac{2T_B}{\sqrt{33}} - \frac{3T_C}{\sqrt{46}} = 0
$$

$$
\sum F_z = 0.8T_A + \frac{5T_B}{\sqrt{33}} + \frac{6T_C}{\sqrt{46}} - 500 = 0
$$

Solving this system yields the cable tensions.

## Spring Systems

Springs introduce force-displacement relationships in equilibrium problems.

### Hooke's Law

For a linear spring:

$$
F = kx
$$

where:

- $F$ = spring force
- $k$ = spring constant (stiffness)
- $x$ = deformation from natural length

### Spring in Series

Springs connected end-to-end:

$$
\frac{1}{k_{eq}} = \frac{1}{k_1} + \frac{1}{k_2} + ... + \frac{1}{k_n}
$$

### Springs in Parallel

Springs connected to common points:

$$
k_{eq} = k_1 + k_2 + ... + k_n
$$

### Example 3: Spring-Mass System

A 50 kg mass is suspended by two springs in parallel with stiffnesses $k_1 = 1000$ N/m and $k_2 = 1500$ N/m.

**Solution:**

**Equivalent stiffness:**

$$
k_{eq} = k_1 + k_2 = 1000 + 1500 = 2500 \text{ N/m}
$$

**Equilibrium position:**
At equilibrium, spring force balances weight:

$$
k_{eq}x = mg
$$

$$
x = \frac{mg}{k_{eq}} = \frac{50 \times 9.81}{2500} = 0.196 \text{ m}
$$

## Friction and Particle Equilibrium

When friction is present, additional force components must be considered.

### Static Friction

Maximum static friction force:

$$
f_{s,max} = \mu_s N
$$

For equilibrium on an inclined plane:

- **Normal force**: $N = W\cos\theta$
- **Friction force**: $f = W\sin\theta$ (for equilibrium)
- **Condition for no sliding**: $W\sin\theta \leq \mu_s W\cos\theta$

This gives the critical angle: $\theta_{critical} = \tan^{-1}(\mu_s)$

## Practical Problem-Solving Strategy

### Step 1: Problem Identification

- Identify the particle (point where forces meet)
- List all known and unknown forces
- Determine what needs to be found

### Step 2: Free Body Diagram

- Draw the particle as a point
- Show all forces with proper directions
- Label known and unknown quantities

### Step 3: Coordinate System

- Choose convenient axes (often align with some forces)
- Be consistent with sign conventions

### Step 4: Force Resolution

- Break forces into components
- Use trigonometry for angled forces
- Express in terms of unit vectors for 3D

### Step 5: Apply Equilibrium

- Write equilibrium equations
- Substitute known values
- Solve system of equations

### Step 6: Verification

- Check signs and magnitudes
- Verify units are consistent
- Confirm physical reasonableness

## Common Applications

### Engineering Structures

- **Truss joints**: Pin connections modeled as particles
- **Cable networks**: Intersection points in cable systems
- **Suspension systems**: Connection points in bridges

### Mechanical Systems

- **Pulley systems**: Loads at pulley intersections
- **Linkage mechanisms**: Pin joints in mechanical linkages
- **Lifting devices**: Crane hook points

### Aerospace Applications

- **Satellite positioning**: Thruster force balance
- **Aircraft loading**: Point loads on wings
- **Spacecraft docking**: Force analysis at connection points

## Advanced Considerations

### Multiple Equilibrium Positions

Some systems may have multiple stable equilibrium positions. Analysis involves:

- Identifying all possible configurations
- Checking stability of each position
- Determining which is most likely to occur

### Limiting Cases

Understanding behavior at limiting conditions:

- Maximum load before failure
- Critical angles for stability
- Minimum forces required for equilibrium

### Sensitivity Analysis

How small changes in parameters affect the equilibrium:

- Effect of small angle changes
- Influence of material property variations
- Impact of manufacturing tolerances

Particle equilibrium provides the foundation for more complex structural analysis. Mastering these concepts ensures success in:

- Truss analysis
- Frame structures
- Cable systems
- Machine component design

The principles learned here extend directly to rigid body equilibrium, where moment effects are added to force balance requirements.

## Exercises

**Exercise 1.** A 20 kg traffic light hangs at the midpoint of a cable whose two halves each make $15^\circ$ with the horizontal. Find the cable tension and comment on what happens as the sag angle shrinks.

<details>
<summary>Answer</summary>

By symmetry, vertical equilibrium gives $2T\sin 15^\circ = mg = 196.2$ N, so

$$
T = \frac{196.2}{2\sin 15^\circ} = 379 \text{ N}
$$

This is almost twice the weight. As the angle tends to zero, $T \to \infty$, so a cable can never be pulled perfectly straight under a transverse load.

</details>

**Exercise 2.** Solve Example 1 in closed form. Show that for two cables at angles $\theta_1$ and $\theta_2$ above the horizontal supporting weight $W$, $T_1 = W\cos\theta_2/\sin(\theta_1 + \theta_2)$ and $T_2 = W\cos\theta_1/\sin(\theta_1 + \theta_2)$. Evaluate them.

<details>
<summary>Answer</summary>

From $\sum F_x = 0$: $T_1 = T_2\cos\theta_2/\cos\theta_1$. Substituting into $\sum F_y = 0$:

$$
T_2\left(\frac{\cos\theta_2\sin\theta_1}{\cos\theta_1} + \sin\theta_2\right) = W
\implies T_2\, \frac{\sin(\theta_1 + \theta_2)}{\cos\theta_1} = W
$$

This gives the stated results. With $W = 981$ N, $\theta_1 = 30^\circ$ and $\theta_2 = 45^\circ$:

$$
T_1 = \frac{981\cos 45^\circ}{\sin 75^\circ} = 718 \text{ N}, \quad
T_2 = \frac{981\cos 30^\circ}{\sin 75^\circ} = 880 \text{ N}
$$

The steeper cable carries more load.

</details>

**Exercise 3.** Repeat Example 3 with the two springs ($k_1 = 1000$ N/m, $k_2 = 1500$ N/m) connected in series instead of in parallel. Find the equivalent stiffness and the static deflection under the 50 kg mass.

<details>
<summary>Answer</summary>

$$
k_{eq} = \left(\frac{1}{1000} + \frac{1}{1500}\right)^{-1} = 600 \text{ N/m}, \quad
x = \frac{50 \times 9.81}{600} = 0.818 \text{ m}
$$

This is more than four times the parallel deflection of 0.196 m. In series each spring carries the full weight; in parallel the springs share it.

</details>

**Exercise 4.** Complete Example 2: solve the three equilibrium equations for the cable tensions $T_A$, $T_B$ and $T_C$, and check that the cable model is valid.

<details>
<summary>Answer</summary>

Solving the linear system, for instance with a matrix solve:

$$
T_A = 103.1 \text{ N}, \quad T_B = 266.5 \text{ N}, \quad T_C = 209.8 \text{ N}
$$

Check for $x$: $0.6(103.1) - 2(266.5)/\sqrt{33} + 209.8/\sqrt{46} = 61.9 - 92.8 + 30.9 \approx 0$.

All three tensions are positive. The cables can only pull, so a negative value would have meant that one "cable" had to push, and that support arrangement could not hold the weight.

</details>

**Exercise 5.** A small block rests on a plank whose inclination is slowly increased. With $\mu_s = 0.35$, at what angle does the block start to slide? Does the answer depend on the block's mass?

<details>
<summary>Answer</summary>

Sliding starts when $W\sin\theta = \mu_s W\cos\theta$, i.e. $\theta_{critical} = \tan^{-1}0.35 = 19.3^\circ$. The weight cancels, so the angle does not depend on mass. That is why tilting-plane tests are a simple way to measure $\mu_s$.

</details>

## References

- Hibbeler, R. C., *Engineering Mechanics: Statics*, 14th ed., Pearson, 2016.
- Beer, F. P., Johnston, E. R., Mazurek, D. F., and Eisenberg, E. R., *Vector Mechanics for Engineers: Statics*, McGraw-Hill.
- Meriam, J. L., and Kraige, L. G., *Engineering Mechanics: Statics*, Wiley.
