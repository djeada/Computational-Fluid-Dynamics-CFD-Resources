# Structural Analysis

Structural analysis predicts the reactions, internal forces and displacements of a structure under its loads. It starts by idealizing the real structure as members, joints and supports, decides whether equilibrium alone can determine the forces, and, when it cannot, adds the compatibility of deformations through the force (flexibility) method or the stiffness (displacement) method. The direct stiffness method for trusses developed at the end of this note is the simplest finite element method, and leads directly to the [Finite Element Method](../../numerical/fem/intro.md) for continua.

## Problem Statement

A structure is defined by its geometry (member axes and joint coordinates, m), member properties (Young's modulus $E$ in Pa, area $A$ in m², second moment of area $I$ in m⁴), supports and loads (forces in N, distributed loads in N/m, imposed settlements or temperature changes). The unknowns are:

- the support reactions;
- the internal forces in every member: axial force $N$, shear force $V$ and bending moment $M$;
- the displacements and rotations of the joints.

The assumptions of linear static analysis are small displacements (equilibrium is written on the undeformed geometry), linear elastic material, and loads applied slowly enough that inertia is negligible. Under these assumptions the response is linear in the loads and superposition holds. The three sets of equations are

```math
\text{equilibrium: } \mathbf{A}\,\mathbf{s} = \mathbf{p},
\qquad \text{compatibility: } \mathbf{e} = \mathbf{B}\,\mathbf{d},
\qquad \text{constitutive law: } \mathbf{s} = \mathbf{k}\,\mathbf{e}
```

where $\mathbf{s}$ are member forces, $\mathbf{p}$ joint loads, $\mathbf{e}$ member deformations and $\mathbf{d}$ joint displacements. For a pin-jointed truss, with tension and elongation both positive, $\mathbf{B} = \mathbf{A}^{\mathsf{T}}$, $\mathbf{k}$ is diagonal with entries $EA/L$, and the three combine into $\mathbf{K}\mathbf{d} = \mathbf{p}$ with $\mathbf{K} = \mathbf{A}\mathbf{k}\mathbf{A}^{\mathsf{T}}$.

## Structural Idealization

### Members

| Member | Carries | Idealized as | Examples |
| --- | --- | --- | --- |
| Bar, tie, strut | Axial force only | Two-force member between pins | Truss members, bracing, hangers |
| Beam | Bending moment and shear, little axial force | Line with flexural stiffness $EI$ | Floor beams, girders, wing spars |
| Frame member | Axial force, shear and moment | Beam-column with rigid or pinned ends | Portal frames, vehicle chassis rails |
| Cable | Tension only, no bending stiffness | Flexible line taking the funicular shape of the load | Suspension bridges, guyed masts |
| Arch | Mainly compression | Curved member, ideally shaped to the load | Bridges, vaults |
| Plate, shell | In-plane and bending stresses | 2D surface | Slabs, fuselage skins, tanks |

### Joints, Supports and Loads

Joints are modelled as pinned (no moment transferred) or rigid (all members rotate together). Real connections are in between, and the choice affects the moments greatly; a bolted angle cleat is normally treated as pinned, a fully welded end plate as rigid. Supports are pins, rollers or fixed, as in [Rigid Body Equilibrium](./rigid_body_equilibrium.md).

Loads are classified by origin. Dead loads (self-weight, finishes) are permanent; live loads (occupants, traffic, stored goods) vary in position and magnitude; environmental loads include wind, snow, waves and earthquakes; temperature changes and support settlements load indeterminate structures by restraining their deformation. Design codes combine them with load factors. Wind and wave loads, which come from the surrounding flow, are covered in [Wind Loading](../fluid_loading/wind_loading.md) and [Wave Loading](../fluid_loading/wave_loading.md).

### Load Paths and Tributary Areas

Every load must have a continuous path to the foundations: slab to beams, beams to girders, girders to columns, columns to foundations. A first estimate of the load on a member uses its tributary area, the part of the floor closer to it than to any neighbour. Floor beams spanning 6 m at 3 m spacing under a 5 kPa floor load each carry $w = 5 \times 3 = 15$ kN/m, giving end reactions of $wL/2 = 45$ kN on the girders and a maximum moment of $wL^2/8 = 67.5$ kN m.

## Determinacy and Stability

A structure is statically determinate when equilibrium alone fixes all reactions and internal forces. Counting unknowns against independent equations gives the degree of indeterminacy $i$:

| Structure | Unknowns | Equations | Degree $i$ |
| --- | --- | --- | --- |
| Plane truss | $m + r$ | $2j$ | $m + r - 2j$ |
| Space truss | $m + r$ | $3j$ | $m + r - 3j$ |
| Plane beam | $r$ | $3 + c$ | $r - 3 - c$ |
| Plane rigid frame | $3m + r$ | $3j + c$ | $3m + r - 3j - c$ |

Here $m$ is the number of members, $r$ the reaction components, $j$ the joints and $c$ the number of equations of condition from internal releases: an internal hinge that joins two members adds one equation ($M = 0$ there). A negative $i$ means a mechanism. A non-negative $i$ is necessary for stability but not sufficient, because supports or members can still be arranged improperly (parallel or concurrent reactions, a non-triangulated panel). The rank of the equilibrium matrix decides.

Determinate structures are insensitive to support settlement, temperature change and fabrication errors, since they can accommodate them by rigid-body motion without stress. Indeterminate structures develop stresses from all three, but they are stiffer, have lower peak moments, and can redistribute load if one member yields or fails.

## Cables and Arches

A cable has no bending stiffness, so it takes the shape along which the load is carried by tension alone. For a uniform load $w$ (N/m) per horizontal length, horizontal equilibrium makes the horizontal tension component $H$ constant, and vertical equilibrium of an element gives $`H\,y'' = w`$. With the origin at the lowest point of a cable spanning $L$ between supports at equal height with sag $h$:

$$
y = \frac{4h}{L^2}x^2,
\qquad H = \frac{wL^2}{8h},
\qquad T_{\max} = \sqrt{H^2 + (wL/2)^2}
$$

The minimum tension $H$ is at the lowest point and the maximum at the supports. A cable hanging under its own weight per unit length of cable takes the shape of a catenary, $y = (H/w)[\cosh(wx/H) - 1]$, which is close to the parabola when the sag is small.

An arch inverts the cable: a parabolic arch under uniform horizontal load carries it in pure compression with no bending. A three-hinged arch (pins at both supports and at the crown) is determinate. Moments about the crown hinge for one half give $Hh = (wL/2)(L/2) - (wL/2)(L/4)$, so the horizontal thrust is the same as the cable tension, $H = wL^2/(8h)$. A two-hinged arch is indeterminate to degree 1 and a fixed arch to degree 3.

## Influence Lines

An influence line gives the value of one response quantity (a reaction, shear or moment at a fixed section) as a unit load moves across the structure. For a simply supported beam of span $L$ with the unit load at $x$, the reaction at A and the moment at a section a distance $a$ from A are

```math
R_A(x) = 1 - \frac{x}{L}, \qquad
M_a(x) = \begin{cases} \dfrac{(L - a)\,x}{L} & 0 \leq x \leq a \\[2mm] \dfrac{a\,(L - x)}{L} & a \leq x \leq L \end{cases}
```

A moving point load $P$ gives the largest response when it sits at the peak ordinate, and a distributed load $w(x)$ gives $`\int w(x)\,\eta(x)\,dx`$, where $\eta$ is the influence-line ordinate. By the Müller-Breslau principle, which follows from [virtual work](./virtual_work.md), the influence line of a force quantity has the shape of the structure's deflected form when the corresponding restraint is removed and a unit displacement is imposed in its place. For determinate structures the shapes are straight-line segments, as above.

## Force (Flexibility) Method

The force method makes an indeterminate structure determinate by removing $i$ redundant restraints, then restores them by requiring the deformations to be compatible.

1. Choose $i$ redundants $X_1, \dots, X_i$ (reactions or internal forces) whose removal leaves a stable determinate primary structure.
2. Compute the displacement $\Delta_{k0}$ of the primary structure under the loads at the location and in the direction of each redundant.
3. Compute the flexibility coefficients $f_{kl}$: the displacement at $k$ due to a unit value of redundant $l$.
4. Solve the compatibility equations $\Delta_{k0} + \sum_l f_{kl} X_l = \Delta_k$, where $\Delta_k$ is the prescribed displacement (zero for a rigid support, the settlement otherwise).
5. Superpose: any response equals its value on the primary structure plus $\sum_l X_l$ times its value under the unit redundant.

The displacements come from the unit-load method, which is the principle of virtual work with a virtual unit load:

```math
\Delta = \sum_{\mathrm{members}} \frac{N\,n\,L}{EA} \;\; \text{(trusses)},
\qquad \Delta = \int \frac{M\,m}{EI}\, dx \;\; \text{(beams and frames)}
```

where $N$, $M$ are the internal forces under the real loads and $n$, $m$ those under a unit load at the point and in the direction of the displacement sought. Maxwell's reciprocal theorem gives $f_{kl} = f_{lk}$.

### Worked Example: Propped Cantilever

A beam of length $L = 6$ m and constant $EI$ is fixed at A and rests on a roller at B, under a uniform load $w = 10$ kN/m. It is indeterminate to degree 1; take the roller reaction $R_B$ as the redundant. The primary structure is a cantilever, whose tip deflection under the load is $wL^4/(8EI)$ downward, and under an upward tip force $R_B$ is $R_B L^3/(3EI)$ upward. Compatibility at the roller requires zero net deflection:

$$
\frac{wL^4}{8EI} = \frac{R_B L^3}{3EI} \implies R_B = \frac{3wL}{8} = 22.5 \text{ kN}
$$

Equilibrium then gives $A_y = 60 - 22.5 = 37.5$ kN and $M_A = wL^2/2 - R_B L = 180 - 135 = 45$ kN m, which equals $wL^2/8$. Note that $EI$ cancels: in an indeterminate structure the forces depend on the relative stiffness of the members, not on their absolute stiffness.

## Stiffness (Displacement) Method

The stiffness method takes the joint displacements as unknowns. Compatibility is then automatic, and equilibrium at the joints gives as many equations as there are free degrees of freedom, whether the structure is determinate or not. Because the procedure is the same for every structure, it is the basis of all general-purpose structural and finite element programs.

### Bar Element

A bar from joint $i$ to joint $j$ with length $L$, axial rigidity $EA$ and unit vector $\mathbf{c} = (c_x, c_y)$ from $i$ to $j$ elongates by $e = \mathbf{c}\cdot(\mathbf{d}_j - \mathbf{d}_i)$ when its ends move by $\mathbf{d}_i$ and $\mathbf{d}_j$. Its axial force is $`N = (EA/L)\,e`$, and it pushes on its end joints with $-N\mathbf{c}$ at $i$ and $+N\mathbf{c}$ at $j$. In terms of the four end displacements,

```math
\begin{bmatrix} \mathbf{f}_i \\ \mathbf{f}_j \end{bmatrix}
= \frac{EA}{L}
\begin{bmatrix} \mathbf{c}\mathbf{c}^{\mathsf{T}} & -\mathbf{c}\mathbf{c}^{\mathsf{T}} \\ -\mathbf{c}\mathbf{c}^{\mathsf{T}} & \mathbf{c}\mathbf{c}^{\mathsf{T}} \end{bmatrix}
\begin{bmatrix} \mathbf{d}_i \\ \mathbf{d}_j \end{bmatrix},
\qquad
\mathbf{c}\mathbf{c}^{\mathsf{T}} = \begin{bmatrix} c_x^2 & c_x c_y \\ c_x c_y & c_y^2 \end{bmatrix}
```

The $4 \times 4$ matrix is the element stiffness matrix $\mathbf{k}_e$ in global coordinates. It is symmetric and singular: a rigid translation of the bar, or a rotation about either end, produces no force.

### Direct Stiffness Procedure

1. Number the degrees of freedom: $2j$ for a plane truss ($3j$ in space).
2. For each member, compute $L$, $\mathbf{c}$ and $\mathbf{k}_e$, and add its entries into the global matrix $\mathbf{K}$ at the rows and columns of its two joints.
3. Partition the degrees of freedom into free (f) and restrained (r). Before supports are applied, $\mathbf{K}$ is singular with three rigid-body modes in 2D (six in 3D).
4. Solve $`\mathbf{K}_{ff}\,\mathbf{d}_f = \mathbf{p}_f`$ for the free displacements, with the restrained ones zero (or equal to prescribed settlements).
5. Recover each member force from $`N = (EA/L)\,\mathbf{c}\cdot(\mathbf{d}_j - \mathbf{d}_i)`$ and the reactions from $`\mathbf{R} = \mathbf{K}_{rf}\,\mathbf{d}_f - \mathbf{p}_r`$.

$`\mathbf{K}_{ff}`$ is symmetric and positive definite when the supports prevent all rigid-body motion, and sparse, because each joint connects only to its neighbours. A singular $`\mathbf{K}_{ff}`$ signals a mechanism.

### Worked Example: Pratt Truss

The six-panel Pratt truss of [Trusses, Frames and Machines](./trusses_frames.md) (3 m panels, 3 m deep, 20 kN at each interior bottom joint) has 14 joints, 25 members and 3 reactions, so the global matrix is $28 \times 28$ and $\mathbf{K}_{ff}$ is $25 \times 25$. With $E = 200$ GPa and $A = 2000$ mm² for every member, the stiffness method reproduces the member forces of the method of joints to within $4 \times 10^{-10}$ N and gives a midspan deflection of 7.76 mm. The unit-load method with the member forces from statics, $\sum N n L/(EA)$, gives the same 7.759 mm, which checks both.

![Pratt truss member forces, its deflected shape from the stiffness method, and a cross-braced indeterminate version](../../../scripts/algorithms/statics_truss_solver/statics_truss_solver.png)

Panel (b) shows the deflected shape magnified 46 times: the chords curve like a beam, the bottom chord lengthens and the top chord shortens, and the roller at the right end moves outward. Panel (c) adds the second diagonal in every panel. The truss is then six times indeterminate, the method of joints no longer applies, and the stiffness method solves it unchanged: each panel's shear is shared between two diagonals, the largest diagonal force falls from 70.7 kN to 37.9 kN, and the midspan deflection falls from 7.76 mm to 5.90 mm.

### From Trusses to Finite Elements

The finite element method applies the same steps to continua. The body is divided into elements, the displacement inside each element is interpolated from its nodal values, the element stiffness matrix comes from the strain energy (or the weak form of the equilibrium equations), and the global matrix is assembled and solved exactly as above. For a 1D bar with linear shape functions, the finite element stiffness matrix is identical to the truss element, and for beams it reproduces the classical slope-deflection relations. See [The Finite Element Method](../../numerical/fem/intro.md) and [Weak Formulation of PDEs](../../numerical/fem/weak_formulation_pde.md).

## Comparison of Methods

|  | Force (flexibility) method | Stiffness (displacement) method |
| --- | --- | --- |
| Primary unknowns | Redundant forces | Joint displacements |
| Number of equations | Degree of indeterminacy $i$ | Number of free degrees of freedom |
| Equations enforce | Compatibility | Equilibrium |
| Choice required | Redundants and primary structure | None; the procedure is fixed |
| Suited to | Hand calculation with few redundants | Computers, any structure |
| Determinate structures | No equations (statics) | Still needs the solve |

## Common Mistakes

- Choosing redundants whose removal leaves a mechanism.
- Mixing units in $EA/L$ (mm² with m) so that displacements are off by $10^6$.
- Forgetting the support conditions before solving, which leaves $\mathbf{K}$ singular.
- Reading displacements from a linear analysis when they are large enough to change the geometry; a cable or a shallow arch then needs a geometrically nonlinear analysis.
- Treating a rigid joint as pinned (or the reverse) without checking how the actual connection behaves.

## Key Takeaways

- Idealization (members, joints, supports, loads) decides the answer as much as the method of solution.
- The degree of indeterminacy counts unknowns minus equilibrium equations; the rank of the equilibrium matrix decides stability.
- Indeterminate structures need compatibility: the force method writes it for the redundants, the stiffness method satisfies it automatically.
- The unit-load method, a form of virtual work, gives displacements and flexibility coefficients.
- The direct stiffness method assembles $`\mathbf{K} = \sum \mathbf{k}_e`$, solves $`\mathbf{K}_{ff}\mathbf{d}_f = \mathbf{p}_f`$ and recovers forces; it is the finite element method for bars.

## Related Scripts

- [Plane Truss Solver](../../../scripts/algorithms/statics_truss_solver/): solves a plane pin-jointed truss by the method of joints and by the direct stiffness method.
- [Support Reactions and Constraint](../../../scripts/plots/statics_support_reactions/): solves the reactions of a simply supported beam from the $3 \times 3$ equilibrium system and classifies support layouts as determinate, indeterminate or improper from the rank of the reaction matrix.

## Exercises

**Exercise 1.** A three-hinged parabolic arch spans 40 m with a rise of 8 m and carries 20 kN/m uniformly along the horizontal. Find the horizontal thrust, the vertical support reactions and the resultant force at each support.

<details>
<summary>Answer</summary>

```math
H = \frac{wL^2}{8h} = \frac{20 \times 40^2}{8 \times 8} = 500 \text{ kN}
```

$V = wL/2 = 400$ kN at each support, and the resultant is $\sqrt{500^2 + 400^2} = 640$ kN. For a parabolic arch under this load the bending moment is zero everywhere: the arch carries the load in pure compression.

</details>

**Exercise 2.** For a 10 m simply supported beam, use the influence line for the moment at $a = 4$ m to find (a) the largest moment there from a single 50 kN moving load and (b) the moment there from a 5 kN/m load over the whole span. Check (b) directly.

<details>
<summary>Answer</summary>

The peak ordinate, at $x = a$, is $a(L - a)/L = 4 \times 6/10 = 2.4$ m.

(a) $M = 50 \times 2.4 = 120$ kN m, with the load at the section.

(b) The area under the influence line is $\tfrac{1}{2} \times 10 \times 2.4 = 12$ m², so $M = 5 \times 12 = 60$ kN m. Directly, $M(4) = (wL/2)(4) - w(4)^2/2 = 100 - 40 = 60$ kN m.

</details>

**Exercise 3.** A cable spans 100 m between supports at equal height, with 10 m sag, and carries 2 kN/m along the horizontal. Find the tension at the lowest point and at the supports.

<details>
<summary>Answer</summary>

```math
H = \frac{wL^2}{8h} = \frac{2 \times 100^2}{8 \times 10} = 250 \text{ kN}
```

At a support the vertical component is $wL/2 = 100$ kN, so $T_{\max} = \sqrt{250^2 + 100^2} = 269$ kN, and $T_{\min} = H = 250$ kN at midspan.

</details>

**Exercise 4.** A continuous beam of constant $EI$ has two equal spans $L = 5$ m on three supports and carries $w = 12$ kN/m over its full length. Use the force method with the middle reaction as the redundant to find all three reactions.

<details>
<summary>Answer</summary>

The primary structure is a simply supported beam of span $2L$. Its midspan deflection under the load is $5w(2L)^4/(384EI)$, and under a point load $R$ at midspan $R(2L)^3/(48EI)$. Compatibility:

```math
\frac{5w(2L)^4}{384EI} = \frac{R(2L)^3}{48EI} \implies R = \frac{5}{8}w(2L) = 1.25\,wL = 75 \text{ kN}
```

The end reactions are $(2wL - R)/2 = (120 - 75)/2 = 22.5$ kN each, that is $3wL/8$, the same as the propped cantilever: by symmetry the slope over the middle support is zero, so each span behaves as if fixed there.

</details>

**Exercise 5.** Two bars meet at a free joint $C(4, 3)$ m. Bar AC comes from a pin at $A(0, 0)$ and bar BC from a pin at $B(4, 0)$. Both have $EA = 2 \times 10^8$ N. A 10 kN horizontal load acts at C in the $+x$ direction. Assemble the $2 \times 2$ stiffness matrix of joint C, find its displacement and the member forces, and check them by the method of joints.

<details>
<summary>Answer</summary>

Bar AC: $L = 5$ m, $\mathbf{c} = (0.8, 0.6)$, $EA/L = 4 \times 10^7$ N/m. Bar BC: $L = 3$ m, $\mathbf{c} = (0, 1)$, $EA/L = 6.67 \times 10^7$ N/m. Only the $\mathbf{d}_j\mathbf{d}_j$ block of each element contributes:

```math
\mathbf{K} = 4 \times 10^7 \begin{bmatrix} 0.64 & 0.48 \\ 0.48 & 0.36 \end{bmatrix}
+ 6.67 \times 10^7 \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}
= \begin{bmatrix} 2.56 & 1.92 \\ 1.92 & 8.107 \end{bmatrix} \times 10^7 \text{ N/m}
```

Solving $\mathbf{K}\mathbf{d} = (10^4, 0)$ gives $\mathbf{d} = (0.475, -0.1125)$ mm. Then $N_{AC} = 4 \times 10^7 (0.8 \times 0.475 - 0.6 \times 0.1125) \times 10^{-3} = 12.5$ kN and $N_{BC} = 6.67 \times 10^7 \times (-0.1125 \times 10^{-3}) = -7.5$ kN.

Method of joints at C: $\sum F_x = 10 - 0.8N_{AC} = 0$ gives $N_{AC} = 12.5$ kN tension, and $\sum F_y = -0.6N_{AC} - N_{BC} = 0$ gives $N_{BC} = -7.5$ kN compression. The two methods agree because the truss is determinate.

</details>

## References

- Hibbeler, R. C., *Structural Analysis*, 10th ed., Pearson, 2018.
- Kassimali, A., *Matrix Analysis of Structures*, 2nd ed., Cengage Learning, 2012.
- McGuire, W., Gallagher, R. H., and Ziemian, R. D., *Matrix Structural Analysis*, 2nd ed., Wiley, 2000.
- Timoshenko, S. P., and Young, D. H., *Theory of Structures*, 2nd ed., McGraw-Hill, 1965.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
