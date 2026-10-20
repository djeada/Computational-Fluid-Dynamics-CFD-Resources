# Bending of Beams

A beam resists transverse load by bending: one side of the cross-section stretches, the other shortens, and the internal moment $M(x)$ found in [Shear Force and Bending Moment Diagrams](./shear_moment.md) is carried by the resulting normal stresses. This note derives the Euler–Bernoulli theory of bending, from the kinematic assumptions to the flexure formula, the transverse shear stress, and the elastic curve that gives the deflection. It then covers superposition with a table of standard cases, statically indeterminate beams, the Timoshenko correction for shear deformation in deep beams, and sections made of two materials. The same theory underlies floor beams and bridge girders, machine shafts, aircraft wing spars and the beam elements of a structural finite-element model loaded by CFD surface forces.

## Problem Statement

A straight prismatic beam of length $L$ has a cross-section with a vertical axis of symmetry, Young's modulus $E$ and shear modulus $G$. Given the supports and the transverse loads acting in the plane of symmetry, find:

- the normal stress $\sigma_x(x, y)$ and the transverse shear stress $\tau_{xy}(x, y)$ at any point;
- the deflection $v(x)$ and slope $v'(x)$ of the beam axis;
- for statically indeterminate beams, the redundant reactions.

The assumptions of Euler–Bernoulli beam theory are:

1. Plane cross-sections remain plane and perpendicular to the deformed axis, so shear deformation is neglected.
2. The material is homogeneous and linear elastic, with the same $E$ in tension and compression.
3. Slopes are small, $|v'| \ll 1$, and deflections are small compared with the span.
4. Loads act in a plane of symmetry of the section, so the beam bends in that plane without twisting.
5. The beam is slender, with depth much smaller than span.

With $x$ along the axis, $y$ upward from the neutral axis, $v$ positive upward, and $V$ and $M$ in the sign convention of [Shear Force and Bending Moment Diagrams](./shear_moment.md#internal-forces-and-sign-convention) ($M > 0$ sagging), the governing equations are

```math
\sigma_x = -\frac{M y}{I},
\qquad \tau_{xy} = \frac{V Q}{I t},
\qquad EI\, \frac{d^2 v}{dx^2} = M(x)
```

with $I$ the second moment of area about the neutral axis, $Q$ the first moment of the area beyond the point, and $t$ the width of the section at the point.

## Flexure Formula

### Strain and Stress

Under a moment the beam axis bends into an arc of radius $\rho$, and its curvature is $\kappa = 1/\rho$. A fibre at height $y$ above the neutral surface (the surface of zero strain) changes length in proportion to its distance from the centre of curvature, so the longitudinal strain is

$$
\varepsilon_x = -\kappa y
$$

For a sagging beam ($\kappa > 0$, concave up) the top fibres are shortened. Hooke's law gives $\sigma_x = -E\kappa y$, a stress that varies linearly over the depth.

### Neutral Axis

With no axial force, the stresses must have zero resultant:

```math
\int_A \sigma_x\,dA = -E\kappa \int_A y\,dA = 0
```

so the first moment of the section about the neutral axis vanishes: the neutral axis passes through the centroid of the section.

### Moment–Curvature Relation

The stresses must also produce the internal moment. A positive (sagging) moment is the resultant of compression above and tension below the axis:

```math
M = -\int_A y\,\sigma_x\,dA = E\kappa \int_A y^2\,dA = EI\kappa
```

Eliminating $\kappa$ between $\kappa = M/(EI)$ and $\sigma_x = -E\kappa y$ gives the flexure formula

$$
\sigma_x = -\frac{M y}{I}
$$

The largest stress magnitude is at the fibre farthest from the neutral axis, at distance $c$:

$$
|\sigma|_{\max} = \frac{|M| c}{I} = \frac{|M|}{S}, \qquad S = \frac{I}{c}
$$

where $S$ is the elastic section modulus. A section that is not symmetric about the neutral axis has two values, $S_{\mathrm{top}}$ and $S_{\mathrm{bottom}}$, and for a material with different strengths in tension and compression (cast iron, concrete) both fibres must be checked.

The formula is exact for pure bending and, by Saint-Venant's principle, accurate a few depths away from load points and supports in beams with shear, since the warping due to shear barely changes the normal stresses in a slender beam.

## Section Properties

### Second Moments of Area

| Section | $I$ about the centroidal axis | $S = I/c$ |
| --- | --- | --- |
| Rectangle, width $b$, depth $h$ | $bh^3/12$ | $bh^2/6$ |
| Solid circle, diameter $d$ | $\pi d^4/64$ | $\pi d^3/32$ |
| Tube, diameters $d_o$ and $d_i$ | $\pi(d_o^4 - d_i^4)/64$ | $\pi(d_o^4 - d_i^4)/(32 d_o)$ |
| Thin-walled tube, radius $r$, wall $t$ | $\pi r^3 t$ | $\pi r^2 t$ |
| Symmetric I-section, flanges $b \times t_f$, depth $h$, web $t_w$ | $\approx b t_f (h - t_f)^2/2 + t_w (h - 2t_f)^3/12$ | $2I/h$ |

The I-section entry neglects the flanges' own second moment about their centroids, which is small. Placing material far from the neutral axis raises $I$ for a given area, which is why I-sections and box sections carry bending far more efficiently than solid rectangles.

### Parallel-Axis Theorem

For a composite section, each part's second moment about the section's centroidal axis is

$$
I = I_c + A d^2
$$

where $I_c$ is the part's second moment about its own centroidal axis, $A$ its area and $d$ the distance between the two parallel axes. The centroid of the whole section is found first:

```math
\bar{y} = \frac{\sum_i A_i \bar{y}_i}{\sum_i A_i}
```

### Example: T-Section

A T-section has a flange of $200 \times 30$ mm on top of a web of $30 \times 170$ mm. Measured from the bottom, the flange has $A_f = 6000$ mm² at $\bar{y}_f = 185$ mm and the web $A_w = 5100$ mm² at $\bar{y}_w = 85$ mm:

```math
\bar{y} = \frac{6000(185) + 5100(85)}{11\,100} = 139.1 \ \mathrm{mm}
```

```math
I = \frac{200(30)^3}{12} + 6000(45.9)^2 + \frac{30(170)^3}{12} + 5100(54.1)^2 = 40.30 \times 10^6 \ \mathrm{mm}^4
```

The top fibre is $c_t = 60.9$ mm and the bottom fibre $c_b = 139.1$ mm from the neutral axis, so $S_{\mathrm{top}} = 6.61 \times 10^5$ mm³ and $S_{\mathrm{bottom}} = 2.90 \times 10^5$ mm³. Under a sagging moment of 10 kN m the top flange is at $-15.1$ MPa and the bottom of the web at $+34.5$ MPa.

## Shear Stress in Beams

When $M$ varies along the beam, the normal stresses on the two faces of a slice $dx$ differ, and the part of the slice beyond a level $y_1$ can only be in equilibrium if a longitudinal shear stress acts on the cut at $y_1$. Balancing the forces on that part gives

```math
\tau = \frac{V Q}{I t},
\qquad Q = \int_{A'} y\, dA
```

where $A'$ is the area between $y_1$ and the outer fibre, $Q$ its first moment about the neutral axis, and $t$ the width of the section at $y_1$. By the symmetry of the stress tensor, the same $\tau$ acts vertically on the cross-section.

For a rectangle, $Q = \tfrac{b}{2}(h^2/4 - y^2)$, so the shear stress is parabolic over the depth, zero at the top and bottom, and largest at the neutral axis:

$$
\tau_{\max} = \frac{3V}{2A}
$$

For a solid circle, $\tau_{\max} = 4V/(3A)$. In an I-section the web carries almost all the shear, nearly uniformly, and $`\tau_{\max} \approx V/(h\,t_w)`$. In thin-walled open sections the product $q = \tau t = VQ/I$ is the shear flow, which runs along the walls.

For the T-section above under $V = 50$ kN, the area below the neutral axis is web only, with $Q = 30(139.1)^2/2 = 2.90 \times 10^5$ mm³:

```math
\tau_{\max} = \frac{50\,000 \times 2.90 \times 10^5}{40.30 \times 10^6 \times 30} = 12.0 \ \mathrm{MPa}
```

In a solid beam the transverse shear stress is small compared with the bending stress unless the beam is short: for a rectangular cantilever with a tip load, $\tau_{\max}/\sigma_{\max} = h/(4L)$. Shear governs short deep beams, thin webs, timber (weak in shear along the grain) and bolted or welded connections between flanges and webs, which must carry the shear flow.

## Elastic Curve

For a curve $v(x)$, the exact curvature is $\kappa = v''/(1 + v'^2)^{3/2}$, which reduces to $\kappa \approx v''$ when the slope is small. With $\kappa = M/(EI)$ this gives the equation of the elastic curve and, through $dM/dx = V$ and $dV/dx = -w$, its higher-order forms:

```math
EI\, v'' = M(x),
\qquad (EI\, v'')' = V(x),
\qquad (EI\, v'')'' = -w(x)
```

The second-order form is integrated twice when $M(x)$ is known, which is the case for a statically determinate beam; the fourth-order form is integrated four times from the load and needs four boundary conditions, which also handles indeterminate beams.

| Support | Conditions |
| --- | --- |
| Pin or roller | $v = 0$ and $`M = EI\,v'' = 0`$ (at an end) |
| Fixed end | $v = 0$ and $v' = 0$ |
| Free end | $M = 0$ and $V = 0$ |
| Interior hinge | $M = 0$; $v$ continuous, $v'$ may jump |

Between segments, $v$ and $v'$ are continuous. Singularity functions (see [Shear Force and Bending Moment Diagrams](./shear_moment.md#singularity-functions)) build these continuity conditions in automatically and leave only two constants of integration for the whole beam.

### Example: Simply Supported Beam with a Uniform Load

With $M(x) = \tfrac{w}{2}(Lx - x^2)$, integrating twice:

```math
EI\,v' = \frac{w}{2}\left(\frac{Lx^2}{2} - \frac{x^3}{3}\right) + C_1, \qquad
EI\,v = \frac{w}{2}\left(\frac{Lx^3}{6} - \frac{x^4}{12}\right) + C_1 x + C_2
```

The condition $v(0) = 0$ gives $C_2 = 0$, and $v(L) = 0$ gives $C_1 = -wL^3/24$. So

```math
v(x) = -\frac{w x}{24 EI}\left(L^3 - 2Lx^2 + x^3\right), \qquad
v\left(\tfrac{L}{2}\right) = -\frac{5 w L^4}{384 EI}, \qquad
v'(0) = -\frac{w L^3}{24 EI}
```

## Superposition

The elastic curve equation is linear in $v$ and in the loads, so the deflection under several loads is the sum of the deflections under each load acting alone. The table collects the standard cases, with $\delta$ the deflection magnitude (downward for downward loads) and $\theta$ the slope magnitude.

| Beam and load | Maximum deflection | Location | End slope |
| --- | --- | --- | --- |
| Cantilever, tip load $P$ | $PL^3/(3EI)$ | Free end | $PL^2/(2EI)$ at free end |
| Cantilever, uniform load $w$ | $wL^4/(8EI)$ | Free end | $wL^3/(6EI)$ at free end |
| Cantilever, tip couple $M_0$ | $M_0 L^2/(2EI)$ | Free end | $M_0 L/EI$ at free end |
| Simply supported, central load $P$ | $PL^3/(48EI)$ | Mid-span | $PL^2/(16EI)$ at each end |
| Simply supported, load $P$ at $a$ from A and $b$ from B, $a \ge b$ | $`Pb(L^2 - b^2)^{3/2}/(9\sqrt{3}\,EIL)`$ | $\sqrt{(L^2 - b^2)/3}$ from A | $Pab(L + b)/(6EIL)$ at A |
| Simply supported, uniform load $w$ | $5wL^4/(384EI)$ | Mid-span | $wL^3/(24EI)$ at each end |
| Simply supported, couple $M_0$ at one end | $`M_0 L^2/(9\sqrt{3}\,EI)`$ | $L(1 - 1/\sqrt{3})$ from the loaded end | $M_0 L/(3EI)$ loaded end, $M_0 L/(6EI)$ other |
| Propped cantilever, uniform load $w$ | $wL^4/(185 EI)$ | $0.579L$ from the fixed end | $wL^3/(48EI)$ at the prop |
| Fixed–fixed, uniform load $w$ | $wL^4/(384EI)$ | Mid-span | 0 |
| Fixed–fixed, central load $P$ | $PL^3/(192EI)$ | Mid-span | 0 |

For the off-centre point load, the deflection under the load is $Pa^2b^2/(3EIL)$, and the slope at B is $Pab(L + a)/(6EIL)$. The maximum deflection lies between the load and mid-span, so the central-load formula is a good estimate when the load is near the middle.

### Example: Cantilever with Two Loads

A steel cantilever with $E = 200$ GPa, $I = 5 \times 10^6$ mm⁴ and $L = 2$ m carries 8 kN/m over its length and 2 kN at its tip. Working in N and mm:

```math
\delta_w = \frac{wL^4}{8EI} = \frac{8 \times 2000^4}{8 \times 200\,000 \times 5 \times 10^6} = 16.0 \ \mathrm{mm}, \qquad
\delta_P = \frac{PL^3}{3EI} = \frac{2000 \times 2000^3}{3 \times 200\,000 \times 5 \times 10^6} = 5.33 \ \mathrm{mm}
```

The tip deflection is $16.0 + 5.33 = 21.3$ mm downward.

### Serviceability Limits

A beam that is strong enough may still deflect too much. Building codes typically limit live-load deflection of floor beams to $L/360$, total-load deflection of roof members to $L/240$, and deflection of members supporting brittle finishes to tighter values; machine elements have limits set by gear mesh, bearing alignment or seal clearance.

## Statically Indeterminate Beams

A beam with more support reactions than equilibrium equations is statically indeterminate; the degree of indeterminacy is the number of extra reactions. The method of superposition (the force or compatibility method) solves it in three steps:

1. Remove the redundant supports, choosing the remaining structure so it is stable and determinate.
2. Compute the deflection of this released structure at each removed support, once under the applied load and once under a unit value of each redundant.
3. Choose the redundants so that the total deflection (or slope) at each removed support matches the real support condition, then find the other reactions from equilibrium.

### Example: Propped Cantilever

A beam fixed at A ($x = 0$) and resting on a roller at B ($x = L$) carries a uniform load $w$. Removing the roller leaves a cantilever whose tip moves down by $wL^4/(8EI)$ under the load, and up by $R_B L^3/(3EI)$ under the roller reaction. Compatibility at B requires zero net deflection:

```math
\frac{R_B L^3}{3EI} = \frac{wL^4}{8EI} \implies R_B = \frac{3wL}{8}
```

Equilibrium then gives $R_A = 5wL/8$ and a fixed-end moment $M_A = R_B L - wL^2/2 = -wL^2/8$ (hogging). The shear vanishes at $x = 5L/8$, where the sagging moment is $9wL^2/128$. For $L = 6$ m and $w = 10$ kN/m: $R_B = 22.5$ kN, $R_A = 37.5$ kN, $M_A = -45$ kN m and $M_{\max}^+ = 25.3$ kN m at 3.75 m. With $EI = 16$ MN m², the largest deflection is $wL^4/(185EI) = 4.39$ mm at 3.47 m from the wall. These are the values in the right-hand column of the figure in [Shear Force and Bending Moment Diagrams](./shear_moment.md#overhanging-beam-with-a-couple), which was computed by a finite-element beam solver.

Fixing both ends of a uniformly loaded span gives end moments $-wL^2/12$ and a mid-span moment $wL^2/24$, so the peak moment is $2/3$ of the simply supported $wL^2/8$ and the deflection is one fifth. Continuity and fixity reduce moments and deflections, but they also attract moment to the supports and make the beam sensitive to support settlement and temperature change, which a determinate beam accommodates without stress.

For more than one or two redundants, the stiffness (displacement) method is used instead: the unknowns are the nodal deflections and rotations, and each beam segment contributes the $4 \times 4$ stiffness matrix of a Hermite cubic element. That is the beam element of structural finite-element codes, introduced in [The Finite Element Method](../../numerical/fem/intro.md); for an Euler–Bernoulli beam with consistent nodal loads it reproduces the exact nodal deflections.

## Timoshenko Beam Correction

Euler–Bernoulli theory neglects the shear strain $\gamma = \tau/G$, which tilts each cross-section relative to the normal of the deformed axis. Timoshenko beam theory lets the section rotate by an independent angle $\psi$, with $`M = EI\,\psi'`$ and the shear force proportional to $\gamma = v' - \psi$ through the effective shear stiffness $\kappa G A$. The shear coefficient $\kappa$ accounts for the non-uniform shear stress over the section: $\kappa = 5/6$ for a rectangle, about $0.89$ for a solid circle with $\nu = 0.3$, and roughly $A_{\mathrm{web}}/A$ for an I-section.

For static loads the result is an additional shear deflection that satisfies $`\kappa G A\,v_s' = -V`$, superposed on the bending deflection. For a cantilever with a tip load, $v_s(L) = -PL/(\kappa G A)$, and the ratio to the bending deflection is

```math
\frac{\delta_s}{\delta_b} = \frac{3EI}{\kappa G A L^2} = \frac{E}{4\kappa G}\left(\frac{h}{L}\right)^2 \quad \text{(rectangle)}
```

For steel ($E/G = 2(1 + \nu) = 2.6$) this is $`0.78\,(h/L)^2`$: 0.8% for $L/h = 10$ but 8.7% for $L/h = 3$. Shear deformation matters for short deep beams, sandwich panels with soft cores (where $G$ of the core is tiny), composite laminates and the higher vibration modes of any beam, whose wavelength is comparable with the depth.

## Composite Sections

A beam made of two bonded materials, such as a timber joist with a steel flitch plate or a reinforced concrete beam, still has plane sections that remain plane, so the strain is linear over the depth, but the stress jumps where the modulus changes. The transformed-section method replaces material 2 by an equivalent width of material 1:

1. Choose a reference material 1 and form the modular ratio $n = E_2/E_1$.
2. Multiply the width of every part made of material 2 by $n$, keeping its depth and position.
3. Find the centroid and the second moment $I_t$ of the transformed section; the neutral axis passes through this centroid.
4. Compute the stress as $\sigma_1 = -My/I_t$ in material 1 and $\sigma_2 = -nMy/I_t$ in material 2.

### Example: Timber Beam with a Steel Plate

A timber beam of $100 \times 200$ mm ($E_1 = 10$ GPa) has a $100 \times 10$ mm steel plate ($E_2 = 200$ GPa) bonded to its underside and carries a sagging moment of 10 kN m. With $n = 20$, the plate becomes 2000 mm wide. Measured from the bottom of the plate:

```math
\bar{y} = \frac{20\,000(110) + 20\,000(5)}{40\,000} = 57.5 \ \mathrm{mm}
```

```math
I_t = \frac{100(200)^3}{12} + 20\,000(52.5)^2 + \frac{2000(10)^3}{12} + 20\,000(52.5)^2 = 177.1 \times 10^6 \ \mathrm{mm}^4
```

The stresses are $-8.61$ MPa at the top of the timber ($y = 152.5$ mm), $+2.68$ MPa at the bottom of the timber ($y = -47.5$ mm), and $20(10 \times 10^6)(57.5)/(177.1 \times 10^6) = 64.9$ MPa at the bottom of the steel. Without the plate, the timber alone would see $\pm 15.0$ MPa. The same method with cracked concrete ignored below the neutral axis is the basis of elastic reinforced-concrete design.

## Common Mistakes

- Using the flexure formula about an axis that is not through the centroid, or forgetting that an unsymmetric section has different stresses at the two extreme fibres.
- Using the full width of the section for $t$ in $VQ/(It)$ instead of the width at the level considered, for example the web thickness of an I-section.
- Using bending deflection formulas outside the small-slope, linear-elastic range, or for a deep beam where shear deflection is comparable.
- Superposing deflections of cases with different support conditions, or adding slopes and deflections at different points.
- Choosing a released structure for an indeterminate beam that is itself unstable.

## Key Takeaways

- The neutral axis passes through the centroid, and the bending stress $\sigma_x = -My/I$ varies linearly over the depth.
- The section modulus $S = I/c$ measures bending strength; material far from the neutral axis is what makes it large.
- The shear stress $VQ/(It)$ is largest at the neutral axis and usually small in slender solid beams, but governs short beams, thin webs and connections.
- The deflection follows from $`EI\,v'' = M`$ with support conditions; superposition of tabulated cases avoids most integrations.
- Indeterminate beams add compatibility conditions; finite-element beam elements generalize the procedure.
- Timoshenko's shear deflection adds about $0.8(h/L)^2$ of the bending deflection of a steel rectangular cantilever.

## Related Scripts

- [Shear and Moment Diagrams of Beams](../../../scripts/algorithms/beams_shear_moment_diagrams/): solves statically determinate and indeterminate beams with Euler–Bernoulli finite elements and draws the load, shear-force, bending-moment and deflection diagrams with their extreme values.
- [Column Buckling Curves](../../../scripts/plots/beams_buckling_curves/): plots the Euler, Johnson, AISC and secant-formula column curves for a structural steel, computes the buckled modes and effective-length factors of four end conditions with a finite-element eigenvalue analysis, and fits a Southwell plot to synthetic test readings.

## Exercises

**Exercise 1.** A $100 \times 200$ mm rectangular beam carries a mid-span moment of 20 kN m. Find the maximum bending stress with the 200 mm side vertical, then with the beam laid flat. Why do they differ?

<details>
<summary>Answer</summary>

Upright: $S = bh^2/6 = 100(200)^2/6 = 6.67 \times 10^5$ mm³ and $\sigma_{\max} = 20 \times 10^6/6.67 \times 10^5 = 30.0$ MPa.

Flat: $S = 200(100)^2/6 = 3.33 \times 10^5$ mm³ and $\sigma_{\max} = 60.0$ MPa.

$S$ grows with the square of the depth but only linearly with the width, so the same area placed farther from the neutral axis is twice as effective here.

</details>

**Exercise 2.** A simply supported steel beam ($E = 200$ GPa) of span 5 m carries a uniform load of 12 kN/m. Its section has $I = 8.0 \times 10^7$ mm⁴ and $c = 150$ mm. Find the maximum bending stress and the mid-span deflection, and check the deflection against $L/360$.

<details>
<summary>Answer</summary>

```math
M_{\max} = \frac{wL^2}{8} = \frac{12(5)^2}{8} = 37.5 \ \mathrm{kN\,m}, \qquad
\sigma_{\max} = \frac{37.5 \times 10^6 \times 150}{8.0 \times 10^7} = 70.3 \ \mathrm{MPa}
```

```math
\delta_{\max} = \frac{5wL^4}{384EI} = \frac{5 \times 12 \times 5000^4}{384 \times 200\,000 \times 8.0 \times 10^7} = 6.10 \ \mathrm{mm}
```

$L/360 = 13.9$ mm, so the beam satisfies the limit.

</details>

**Exercise 3.** A simply supported beam of span 4 m with a $100 \times 200$ mm rectangular section carries a central load of 20 kN. Find the maximum transverse shear stress and where it occurs, and compare it with the maximum bending stress.

<details>
<summary>Answer</summary>

$V = P/2 = 10$ kN in each half, so

```math
\tau_{\max} = \frac{3V}{2A} = \frac{3 \times 10\,000}{2 \times 20\,000} = 0.75 \ \mathrm{MPa}
```

at the neutral axis, where the bending stress is zero. With $M_{\max} = PL/4 = 20$ kN m, $\sigma_{\max} = 30$ MPa at mid-span, so the shear stress is only 2.5% of the bending stress, consistent with $\tau_{\max}/\sigma_{\max} = h/(2L)$ for this loading.

</details>

**Exercise 4.** Integrate $`EI\,v'' = M`$ to derive the tip deflection and slope of a cantilever of length $L$ with a point load $P$ at its free end.

<details>
<summary>Answer</summary>

With the fixed end at $x = 0$, $M(x) = -P(L - x)$.

Integrate once: $`EI\,v' = -P(Lx - x^2/2) + C_1`$, and $v'(0) = 0$ gives $C_1 = 0$.

Integrate again: $`EI\,v = -P(Lx^2/2 - x^3/6) + C_2`$, and $v(0) = 0$ gives $C_2 = 0$.

At $x = L$:

```math
v(L) = -\frac{PL^3}{3EI}, \qquad v'(L) = -\frac{PL^2}{2EI}
```

The negative signs mean downward deflection and clockwise rotation.

</details>

**Exercise 5.** A beam of span $L$ is fixed at both ends and carries a uniform load $w$. Use superposition on a simply supported beam with equal end couples $M_e$ to find the end moments and the mid-span deflection.

<details>
<summary>Answer</summary>

On the simply supported beam the uniform load rotates each end by $wL^3/(24EI)$. Equal end couples $M_e$ (hogging) rotate each end back by $M_e L/(3EI) + M_e L/(6EI) = M_e L/(2EI)$, using the table entry for an end couple at the near and far ends. Zero slope requires $M_e L/(2EI) = wL^3/(24EI)$, so $M_e = wL^2/12$, and the end moments are $-wL^2/12$.

A uniform hogging moment $M_e$ on a simply supported span lifts the mid-span by $M_e L^2/(8EI) = wL^4/(96EI)$. The net mid-span deflection is

```math
\delta = \frac{5wL^4}{384EI} - \frac{wL^4}{96EI} = \frac{wL^4}{384EI}
```

one fifth of the simply supported value.

</details>

## References

- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Timoshenko, S. P., and Goodier, J. N., *Theory of Elasticity*, 3rd ed., McGraw-Hill, 1970.
- Young, W. C., Budynas, R. G., and Sadegh, A. M., *Roark's Formulas for Stress and Strain*, 8th ed., McGraw-Hill, 2012.
- Cowper, G. R., "The shear coefficient in Timoshenko's beam theory", *Journal of Applied Mechanics*, 33(2), 335–340, 1966.
- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 11th ed., McGraw-Hill Education, 2020.
