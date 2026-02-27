# Vector Analysis in Mechanics

Vector analysis provides the mathematical language for describing and manipulating the physical quantities encountered in mechanics. Forces, velocities, accelerations, and moments are all vector quantities, and their proper treatment requires a solid foundation in vector algebra and calculus.

## Vector Fundamentals

A vector is a quantity that possesses both magnitude and direction. In contrast, a scalar has magnitude only.

### Representation
A vector $\mathbf{A}$ in three-dimensional space is expressed in terms of its rectangular components:

$$\mathbf{A} = A_x\mathbf{i} + A_y\mathbf{j} + A_z\mathbf{k}$$

where $\mathbf{i}$, $\mathbf{j}$, $\mathbf{k}$ are unit vectors along the $x$, $y$, $z$ axes respectively.

### Magnitude
The magnitude (or norm) of a vector is:

$$|\mathbf{A}| = A = \sqrt{A_x^2 + A_y^2 + A_z^2}$$

### Direction
The direction of a vector is described by its direction cosines:

$$\cos\alpha = \frac{A_x}{A}, \quad \cos\beta = \frac{A_y}{A}, \quad \cos\gamma = \frac{A_z}{A}$$

where $\alpha$, $\beta$, $\gamma$ are the angles the vector makes with the $x$, $y$, $z$ axes. These satisfy:

$$\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$$

## Unit Vectors

A unit vector has a magnitude of one and indicates direction only:

$$\hat{\mathbf{u}}_A = \frac{\mathbf{A}}{|\mathbf{A}|} = \frac{A_x\mathbf{i} + A_y\mathbf{j} + A_z\mathbf{k}}{A}$$

Unit vectors are essential for expressing forces along specified directions. If a force of magnitude $F$ acts along the direction from point $P_1$ to point $P_2$:

$$\mathbf{F} = F\hat{\mathbf{u}} = F\frac{\mathbf{r}_{P_2} - \mathbf{r}_{P_1}}{|\mathbf{r}_{P_2} - \mathbf{r}_{P_1}|}$$

## Position Vectors

A position vector defines the location of a point relative to the origin or another point:

$$\mathbf{r} = x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$$

The relative position vector from point $A$ to point $B$ is:

$$\mathbf{r}_{AB} = \mathbf{r}_B - \mathbf{r}_A = (x_B - x_A)\mathbf{i} + (y_B - y_A)\mathbf{j} + (z_B - z_A)\mathbf{k}$$

Position vectors are fundamental for moment calculations, where $\mathbf{M} = \mathbf{r} \times \mathbf{F}$.

## Vector Operations

### Vector Addition and Subtraction

**Addition** (parallelogram law or head-to-tail rule):

$$\mathbf{A} + \mathbf{B} = (A_x + B_x)\mathbf{i} + (A_y + B_y)\mathbf{j} + (A_z + B_z)\mathbf{k}$$

**Subtraction**:

$$\mathbf{A} - \mathbf{B} = (A_x - B_x)\mathbf{i} + (A_y - B_y)\mathbf{j} + (A_z - B_z)\mathbf{k}$$

Properties:
- Commutative: $\mathbf{A} + \mathbf{B} = \mathbf{B} + \mathbf{A}$
- Associative: $(\mathbf{A} + \mathbf{B}) + \mathbf{C} = \mathbf{A} + (\mathbf{B} + \mathbf{C})$

### Scalar Multiplication

Multiplying a vector by a scalar $c$ scales the magnitude and may reverse the direction:

$$c\mathbf{A} = cA_x\mathbf{i} + cA_y\mathbf{j} + cA_z\mathbf{k}$$

- If $c > 0$: same direction as $\mathbf{A}$
- If $c < 0$: opposite direction to $\mathbf{A}$
- If $c = 0$: the zero vector $\mathbf{0}$

## Dot Product (Scalar Product)

The dot product of two vectors produces a scalar:

$$\mathbf{A} \cdot \mathbf{B} = |\mathbf{A}||\mathbf{B}|\cos\theta = A_xB_x + A_yB_y + A_zB_z$$

where $\theta$ is the angle between the two vectors.

### Properties
- Commutative: $\mathbf{A} \cdot \mathbf{B} = \mathbf{B} \cdot \mathbf{A}$
- Distributive: $\mathbf{A} \cdot (\mathbf{B} + \mathbf{C}) = \mathbf{A} \cdot \mathbf{B} + \mathbf{A} \cdot \mathbf{C}$
- $\mathbf{A} \cdot \mathbf{A} = |\mathbf{A}|^2$

### Applications in Mechanics

**Angle between two vectors**:

$$\theta = \cos^{-1}\left(\frac{\mathbf{A} \cdot \mathbf{B}}{|\mathbf{A}||\mathbf{B}|}\right)$$

**Projection of a vector onto a direction**:

$$A_b = \mathbf{A} \cdot \hat{\mathbf{u}}_b = |\mathbf{A}|\cos\theta$$

**Work done by a force** along a displacement:

$$W = \mathbf{F} \cdot \mathbf{d} = Fd\cos\theta$$

## Cross Product (Vector Product)

The cross product of two vectors produces a vector perpendicular to both:

$$\mathbf{A} \times \mathbf{B} = |\mathbf{A}||\mathbf{B}|\sin\theta\,\hat{\mathbf{n}}$$

where $\hat{\mathbf{n}}$ is determined by the right-hand rule. In component form:

$$\mathbf{A} \times \mathbf{B} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ A_x & A_y & A_z \\ B_x & B_y & B_z \end{vmatrix}$$

$$= (A_yB_z - A_zB_y)\mathbf{i} - (A_xB_z - A_zB_x)\mathbf{j} + (A_xB_y - A_yB_x)\mathbf{k}$$

### Properties
- Anti-commutative: $\mathbf{A} \times \mathbf{B} = -(\mathbf{B} \times \mathbf{A})$
- Distributive: $\mathbf{A} \times (\mathbf{B} + \mathbf{C}) = \mathbf{A} \times \mathbf{B} + \mathbf{A} \times \mathbf{C}$
- $\mathbf{A} \times \mathbf{A} = \mathbf{0}$
- If $\mathbf{A} \times \mathbf{B} = \mathbf{0}$ and neither is zero, then $\mathbf{A}$ and $\mathbf{B}$ are parallel

### Applications in Mechanics

**Moment of a force about a point**:

$$\mathbf{M}_O = \mathbf{r} \times \mathbf{F}$$

**Area of a parallelogram** defined by two vectors:

$$\text{Area} = |\mathbf{A} \times \mathbf{B}|$$

## Triple Products

### Scalar Triple Product

$$\mathbf{A} \cdot (\mathbf{B} \times \mathbf{C}) = \begin{vmatrix} A_x & A_y & A_z \\ B_x & B_y & B_z \\ C_x & C_y & C_z \end{vmatrix}$$

The absolute value of the scalar triple product gives the volume of the parallelepiped formed by the three vectors. It is also used to compute the moment of a force about an axis:

$$M_a = \hat{\mathbf{u}}_a \cdot (\mathbf{r} \times \mathbf{F})$$

Properties:
- Cyclic permutation preserves the value: $\mathbf{A} \cdot (\mathbf{B} \times \mathbf{C}) = \mathbf{B} \cdot (\mathbf{C} \times \mathbf{A}) = \mathbf{C} \cdot (\mathbf{A} \times \mathbf{B})$
- If the scalar triple product is zero, the three vectors are coplanar

### Vector Triple Product

$$\mathbf{A} \times (\mathbf{B} \times \mathbf{C}) = \mathbf{B}(\mathbf{A} \cdot \mathbf{C}) - \mathbf{C}(\mathbf{A} \cdot \mathbf{B})$$

This identity (the BAC-CAB rule) is useful in advanced dynamics and electromagnetic theory.

## Coordinate Systems

### Cartesian Coordinates $(x, y, z)$
The standard rectangular system with constant unit vectors $\mathbf{i}$, $\mathbf{j}$, $\mathbf{k}$:

$$\mathbf{r} = x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$$

Best suited for problems with rectangular geometry and linear motion.

### Cylindrical Coordinates $(r, \theta, z)$
Useful for problems with axial symmetry:

$$x = r\cos\theta, \quad y = r\sin\theta, \quad z = z$$

Unit vectors $\hat{\mathbf{e}}_r$, $\hat{\mathbf{e}}_\theta$, $\hat{\mathbf{e}}_z$ where $\hat{\mathbf{e}}_r$ and $\hat{\mathbf{e}}_\theta$ vary with position:

$$\hat{\mathbf{e}}_r = \cos\theta\,\mathbf{i} + \sin\theta\,\mathbf{j}$$
$$\hat{\mathbf{e}}_\theta = -\sin\theta\,\mathbf{i} + \cos\theta\,\mathbf{j}$$

Applications: rotating shafts, pipe flow analysis, turbomachinery.

### Spherical Coordinates $(R, \theta, \phi)$
For problems with point symmetry:

$$x = R\sin\theta\cos\phi, \quad y = R\sin\theta\sin\phi, \quad z = R\cos\theta$$

Applications: pressure vessels, gravitational field analysis, antenna radiation patterns.

## Example 1: Force Along a Line

**Given**:
- A cable connects point $A(1, 0, 3)$ m to point $B(5, 6, 0)$ m
- The cable tension is $T = 500$ N

**Find**: Express the tension force as a Cartesian vector

**Solution**:

Position vector from $A$ to $B$:

$$\mathbf{r}_{AB} = (5-1)\mathbf{i} + (6-0)\mathbf{j} + (0-3)\mathbf{k} = 4\mathbf{i} + 6\mathbf{j} - 3\mathbf{k} \text{ m}$$

Magnitude:

$$|\mathbf{r}_{AB}| = \sqrt{4^2 + 6^2 + 3^2} = \sqrt{16 + 36 + 9} = \sqrt{61} = 7.81 \text{ m}$$

Unit vector:

$$\hat{\mathbf{u}}_{AB} = \frac{\mathbf{r}_{AB}}{|\mathbf{r}_{AB}|} = \frac{4\mathbf{i} + 6\mathbf{j} - 3\mathbf{k}}{7.81} = 0.512\mathbf{i} + 0.768\mathbf{j} - 0.384\mathbf{k}$$

Tension vector:

$$\mathbf{T} = T\hat{\mathbf{u}}_{AB} = 500(0.512\mathbf{i} + 0.768\mathbf{j} - 0.384\mathbf{k})$$

$$\mathbf{T} = (256\mathbf{i} + 384\mathbf{j} - 192\mathbf{k}) \text{ N}$$

## Example 2: Work Done by a Force

**Given**:
- Force: $\mathbf{F} = (30\mathbf{i} - 40\mathbf{j} + 20\mathbf{k})$ N
- Displacement: $\mathbf{d} = (5\mathbf{i} + 2\mathbf{j} - 3\mathbf{k})$ m

**Find**: Work done by the force and angle between $\mathbf{F}$ and $\mathbf{d}$

**Solution**:

Work (dot product):

$$W = \mathbf{F} \cdot \mathbf{d} = (30)(5) + (-40)(2) + (20)(-3) = 150 - 80 - 60 = 10 \text{ J}$$

Magnitudes:

$$|\mathbf{F}| = \sqrt{30^2 + 40^2 + 20^2} = \sqrt{2900} = 53.85 \text{ N}$$

$$|\mathbf{d}| = \sqrt{5^2 + 2^2 + 3^2} = \sqrt{38} = 6.16 \text{ m}$$

Angle between the vectors:

$$\theta = \cos^{-1}\left(\frac{W}{|\mathbf{F}||\mathbf{d}|}\right) = \cos^{-1}\left(\frac{10}{53.85 \times 6.16}\right) = \cos^{-1}(0.0302) = 88.3°$$

The force is nearly perpendicular to the displacement, resulting in minimal work.

## Example 3: Moment Using the Cross Product

**Given**:
- A force $\mathbf{F} = (4\mathbf{i} - 3\mathbf{j} + 5\mathbf{k})$ kN acts at point $P(2, 1, -1)$ m
- Find the moment about the origin $O$

**Find**: Moment vector and its magnitude

**Solution**:

Position vector:

$$\mathbf{r} = 2\mathbf{i} + 1\mathbf{j} - 1\mathbf{k} \text{ m}$$

Moment (cross product):

$$\mathbf{M}_O = \mathbf{r} \times \mathbf{F} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 2 & 1 & -1 \\ 4 & -3 & 5 \end{vmatrix}$$

$$\mathbf{M}_O = [(1)(5) - (-1)(-3)]\mathbf{i} - [(2)(5) - (-1)(4)]\mathbf{j} + [(2)(-3) - (1)(4)]\mathbf{k}$$

$$\mathbf{M}_O = (5 - 3)\mathbf{i} - (10 + 4)\mathbf{j} + (-6 - 4)\mathbf{k}$$

$$\mathbf{M}_O = (2\mathbf{i} - 14\mathbf{j} - 10\mathbf{k}) \text{ kN·m}$$

Magnitude:

$$|\mathbf{M}_O| = \sqrt{2^2 + 14^2 + 10^2} = \sqrt{4 + 196 + 100} = \sqrt{300} = 17.32 \text{ kN·m}$$

## Applications in Force Analysis

### Resultant of Concurrent Forces
The resultant of $n$ concurrent forces is found by vector addition:

$$\mathbf{R} = \sum_{i=1}^{n}\mathbf{F}_i = \left(\sum F_{ix}\right)\mathbf{i} + \left(\sum F_{iy}\right)\mathbf{j} + \left(\sum F_{iz}\right)\mathbf{k}$$

### Equilibrium in Three Dimensions
A rigid body in 3D equilibrium satisfies:

$$\sum \mathbf{F} = \mathbf{0} \quad \Rightarrow \quad \sum F_x = 0, \quad \sum F_y = 0, \quad \sum F_z = 0$$

$$\sum \mathbf{M}_O = \mathbf{0} \quad \Rightarrow \quad \sum M_x = 0, \quad \sum M_y = 0, \quad \sum M_z = 0$$

These six scalar equations are the foundation for solving 3D statics problems.

## Common Mistakes and Tips

### Frequent Errors
1. **Confusing dot and cross products**: The dot product yields a scalar; the cross product yields a vector
2. **Wrong order in cross products**: $\mathbf{A} \times \mathbf{B} \neq \mathbf{B} \times \mathbf{A}$; the order matters
3. **Incorrect unit vectors**: Failing to normalize when computing direction from two points
4. **Sign errors in determinant expansion**: Carefully track the alternating signs in cross product computation

### Best Practices
1. **Always check magnitudes**: A unit vector must have magnitude 1; verify after computation
2. **Use component form** for systematic calculations to avoid geometric errors
3. **Verify with dot product**: Confirm perpendicularity ($\mathbf{A} \cdot \mathbf{B} = 0$) or parallelism ($|\mathbf{A} \times \mathbf{B}| = 0$) as expected
4. **Choose coordinate systems** to simplify the problem; align axes with symmetry or primary directions of motion
5. **Apply dimensional analysis**: Ensure that the units of each vector operation are consistent with the expected result

Vector analysis is the essential mathematical toolkit for all of mechanics. Proficiency with vector operations enables clear, systematic solutions to force analysis, moment computation, and equilibrium problems in both two and three dimensions. These skills form the prerequisite for advanced topics including dynamics, deformable body mechanics, and computational methods.
