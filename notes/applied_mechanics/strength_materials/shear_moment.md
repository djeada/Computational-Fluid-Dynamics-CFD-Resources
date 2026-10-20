# Shear Force and Bending Moment Diagrams

A beam carries transverse load by developing an internal shear force $V(x)$ and bending moment $M(x)$ at every cross-section. The diagrams of $V$ and $M$ along the span locate the sections where the bending stress (from $M$) and the transverse shear stress (from $V$) are largest, and they are the input to every later beam calculation: the flexure formula and the elastic curve in [Bending of Beams](./beam_bending.md), shaft design in [Combined Loading](./combined_loading.md), and the response of structures to wind and wave forces in [Fluid Loading](../fluid_loading/intro.md). This note fixes a sign convention, derives the differential relations between load, shear and moment, gives a procedure for drawing the diagrams by hand and with singularity functions, and works through point loads, couples and distributed loads.

## Problem Statement

A straight beam occupies $0 \le x \le L$. Given:

- the supports (pin, roller, fixed end) and their positions;
- the applied loads: point forces $P_i$ at $x = a_i$, couples $C_j$ at $x = c_j$, and distributed loads $w(x)$ in N/m;

find the support reactions, the shear force $V(x)$ and the bending moment $M(x)$ for all $x$, their maximum magnitudes and where they occur, and the points of contraflexure where $M$ changes sign.

The beam is treated as a rigid body for the reactions and is cut by the method of sections for the internal forces. Deformations are assumed small, so equilibrium is written in the undeformed geometry. If the reactions follow from the three equilibrium equations of the plane,

$$
\sum F_x = 0,
\qquad \sum F_y = 0,
\qquad \sum M = 0
$$

the beam is statically determinate; otherwise compatibility of deflections is also needed, which is treated in [Bending of Beams](./beam_bending.md#statically-indeterminate-beams). Once the reactions are known, the internal forces follow from equilibrium alone in either case. Axial force is zero unless loads have a component along the beam.

## Internal Forces and Sign Convention

Cutting the beam at $x$ exposes an internal shear force and bending moment that act in opposite senses on the two faces of the cut. A sign convention is therefore attached to the deformation they produce, not to a direction in space. These notes use the convention of Gere and Goodno:

| Quantity | Positive when | Equivalent statement |
| --- | --- | --- |
| Distributed load $w(x)$ | It acts downward |  |
| Point load $P$ | It acts downward |  |
| Applied couple $C$ | It is clockwise |  |
| Shear force $V(x)$ | The net external force on the segment to the left of the cut is upward | It tends to rotate a beam element clockwise |
| Bending moment $M(x)$ | It bends the beam concave upward (sagging) | It compresses the top fibres |
| Deflection $v(x)$ | It is upward |  |

With these definitions, $V(x)$ is the sum of the upward forces to the left of the section, and $M(x)$ is the sum of the moments, about the section, of all forces and couples to the left of it, counted positive when they would sag the beam. Taking the segment to the right instead gives the same values with the signs of the sums reversed. Hibbeler takes $w$ positive upward and therefore writes $dV/dx = w$; the physics is the same.

## Relations Between Load, Shear and Moment

Consider an element between $x$ and $x + dx$ carrying a downward distributed load $w$. The left face carries $V$ and $M$, the right face $V + dV$ and $M + dM$, both in the positive senses defined above. Vertical equilibrium gives

```math
V - w\, dx - (V + dV) = 0
```

and moment equilibrium about the right face gives

```math
-M - V\, dx + w\, dx\, \frac{dx}{2} + (M + dM) = 0
```

Dropping the second-order term and dividing by $dx$:

$$
\frac{dV}{dx} = -w(x),
\qquad \frac{dM}{dx} = V(x),
\qquad \frac{d^2M}{dx^2} = -w(x)
$$

Integrating between two sections $x_1 < x_2$ between which no concentrated loads act:

```math
V_2 - V_1 = -\int_{x_1}^{x_2} w\,dx, \qquad M_2 - M_1 = \int_{x_1}^{x_2} V\,dx
```

The change in shear is minus the area under the load diagram, and the change in moment is the area under the shear diagram. Concentrated actions produce jumps that the differential relations do not contain. Writing $x^-$ and $x^+$ for the two sides of the point of application:

| Concentrated action at $x = a$ | Jump in $V$ | Jump in $M$ |
| --- | --- | --- |
| Downward force $P$ | $V(a^+) - V(a^-) = -P$ | None; the slope of $M$ changes |
| Upward reaction $R$ | $+R$ | None |
| Clockwise couple $C$ | None | $M(a^+) - M(a^-) = +C$ |

These relations fix the shape of each diagram between load points.

| Load between two points | Shear diagram | Moment diagram |
| --- | --- | --- |
| None, $w = 0$ | Constant | Linear |
| Uniform, $w = w_0$ | Linear, slope $-w_0$ | Parabolic, concave down for $w_0 > 0$ |
| Linearly varying | Parabolic | Cubic |

Since $dM/dx = V$, the moment has a stationary value wherever the shear passes through zero, and its largest magnitude is found either at such a point, at a point where $V$ jumps through zero, at a couple, or at a support or end.

## Drawing the Diagrams

1. Draw the free-body diagram and find the reactions from $\sum F_y = 0$ and $\sum M = 0$. Check them with a moment equation about a second point.
2. Divide the beam into segments at every support, point load, couple and start or end of a distributed load.
3. Start at the left end with $V = 0$ and $M = 0$ (a free end, pin or roller), or with the reaction values at a fixed end.
4. Move right. Apply each jump in $V$ from the table above, and change $V$ continuously by minus the area of the load diagram.
5. Build $M$ from the area of the shear diagram, adding $+C$ at each clockwise couple.
6. At the right end, $V$ and $M$ must return to the values required by the support (zero at a free end or simple support). A non-zero residual means an error in the reactions or the arithmetic.
7. Find the stationary points of $M$ where $V = 0$ and evaluate $M$ there, at the supports and at each couple.

## Worked Examples

### Simply Supported Beam with a Uniform Load

A simply supported beam of span $L = 6$ m carries $w = 10$ kN/m. By symmetry, $R_A = R_B = wL/2 = 30$ kN. For $0 \le x \le L$:

```math
V(x) = 30 - 10x \ \mathrm{kN},
\qquad M(x) = 30x - 5x^2 \ \mathrm{kN\,m}
```

The shear falls linearly from $+30$ kN to $-30$ kN and is zero at mid-span, where $M_{\max} = wL^2/8 = 45$ kN m. The largest shear magnitude, 30 kN, is at the supports.

### Cantilever with a Tip Load

A cantilever of length $L = 3$ m is fixed at $x = 0$ and carries $P = 12$ kN at its free end. The wall supplies an upward force of 12 kN and a counterclockwise couple of $PL = 36$ kN m. Then $V(x) = +12$ kN for $0 < x < L$ and

```math
M(x) = -P(L - x) = -12(3 - x) \ \mathrm{kN\,m}
```

The moment is hogging everywhere and largest in magnitude at the wall, $M(0) = -36$ kN m. Measuring $x$ from the free end instead changes the formula but not the diagram: the beam always bends concave downward.

### Simply Supported Beam with Two Point Loads

A simply supported beam with $L = 8$ m carries $P_1 = 10$ kN at $x = 2$ m and $P_2 = 20$ kN at $x = 5$ m. Moments about A give $8R_B = 10(2) + 20(5) = 120$, so $R_B = 15$ kN and $R_A = 30 - 15 = 15$ kN. The shear is piecewise constant:

| Segment | $V$ (kN) |
| --- | --- |
| $0 < x < 2$ m | $+15$ |
| $2 < x < 5$ m | $+5$ |
| $5 < x < 8$ m | $-15$ |

The moment is piecewise linear, with $M(2) = 30$ kN m and $M(5) = 15(5) - 10(3) = 45$ kN m. The shear changes sign at $x = 5$ m, so the maximum moment is 45 kN m under $P_2$.

### Overhanging Beam with a Couple

The beam in the left column of the figure has a pin at A ($x = 0$), a roller at B ($x = 6$ m) and an overhang to C ($x = 8$ m). It carries 10 kN/m over $0 \le x \le 3$ m, a clockwise couple of 9 kN m at $x = 4.5$ m and a downward load of 15 kN at C.

Moments about A, counterclockwise positive:

$$
6R_B - 30(1.5) - 9 - 15(8) = 0 \implies R_B = 29 \ \mathrm{kN}
$$

and vertical equilibrium gives $R_A = 30 + 15 - 29 = 16$ kN.

- On $0 \le x \le 3$ m, $V = 16 - 10x$, which vanishes at $x = 1.6$ m, where $M = 16(1.6) - 5(1.6)^2 = 12.8$ kN m. At $x = 3$ m, $V = -14$ kN and $M = 48 - 45 = 3$ kN m.
- On $3 < x < 6$ m, $V = -14$ kN. The moment falls to $M(4.5^-) = 3 - 14(1.5) = -18$ kN m, jumps by $+9$ to $-9$ kN m at the couple, and reaches $M_B = -9 - 14(1.5) = -30$ kN m.
- At B the shear jumps by $+29$ to $+15$ kN, and on the overhang $M$ rises linearly to $M_C = -30 + 15(2) = 0$, as it must at a free end.

The largest moment magnitude is the hogging moment of 30 kN m over support B; the largest sagging moment is 12.8 kN m. The moment changes sign at $x = 3.21$ m, a point of contraflexure.

![Load, shear, moment and deflection diagrams of an overhanging beam and a propped cantilever](../../../scripts/algorithms/beams_shear_moment_diagrams/beams_shear_moment_diagrams.png)

The figure is computed by a finite-element beam solver and the singularity functions of the next section. In the left column, the shear has slope $-10$ kN/m under the distributed load and jumps at both supports, and the moment diagram has a step of exactly 9 kN m at the couple. The right column is a statically indeterminate propped cantilever, whose reactions need the deflection condition at the roller; its diagrams are discussed in [Bending of Beams](./beam_bending.md#statically-indeterminate-beams). The bottom row shows that the elastic curve is concave down wherever $M < 0$.

## Singularity Functions

Writing a separate expression for each segment becomes tedious when there are many loads. Singularity functions, introduced for beams by Macaulay, give one expression valid over the whole span. The Macaulay bracket is defined as

```math
\langle x - a \rangle^n =
\begin{cases}
0, & x < a \\
(x - a)^n, & x \ge a
\end{cases}
\qquad n = 0, 1, 2, \dots
```

so $\langle x - a\rangle^0$ is a unit step at $x = a$. For $n \ge 0$ the brackets integrate like ordinary powers:

```math
\int_0^x \langle \xi - a \rangle^n \, d\xi = \frac{\langle x - a \rangle^{n+1}}{n + 1}
```

Building $V$ and $M$ directly from the loads to the left of the section, with the conventions of this note:

| Action at $x = a$ | Contribution to $V(x)$ | Contribution to $M(x)$ |
| --- | --- | --- |
| Upward force $R$ (a reaction) | $R\langle x - a\rangle^0$ | $R\langle x - a\rangle^1$ |
| Downward force $P$ | $-P\langle x - a\rangle^0$ | $-P\langle x - a\rangle^1$ |
| Clockwise couple $C$ | 0 | $C\langle x - a\rangle^0$ |
| Uniform load $w_0$ from $x = a$ onward | $-w_0\langle x - a\rangle^1$ | $-\tfrac{w_0}{2}\langle x - a\rangle^2$ |
| Load increasing at slope $s$ (N/m²) from $x = a$ onward | $-\tfrac{s}{2}\langle x - a\rangle^2$ | $-\tfrac{s}{6}\langle x - a\rangle^3$ |

A load that stops at $x = b$ is written as the same load starting at $a$ minus an identical load starting at $b$. For the overhanging beam above:

```math
M(x) = 16x - 5\langle x \rangle^2 + 5\langle x - 3 \rangle^2 + 9\langle x - 4.5 \rangle^0 + 29\langle x - 6 \rangle^1 \ \mathrm{kN\,m}
```

with $x$ in metres. At $x = 8$ m this gives $128 - 320 + 125 + 9 + 58 = 0$, which checks the reactions. The same expression, integrated twice with $`EI\,v'' = M`$, gives the deflection in a single pass with only two constants of integration (see [Bending of Beams](./beam_bending.md#elastic-curve)). For this beam, with $EI = 16$ MN m², the conditions $v(0) = v(6) = 0$ give a tip deflection of 5.85 mm downward, as in the figure.

## Common Mistakes

- Mixing sign conventions between textbooks, in particular $dV/dx = -w$ with $w$ positive downward and $dV/dx = +w$ with $w$ positive upward.
- Forgetting the reaction couple at a fixed end, or giving it the wrong sense. A wall at the left end of a cantilever with downward loads applies a counterclockwise couple, and the moment there is hogging.
- Looking for the maximum moment only where $V = 0$. At a couple the moment jumps, and the largest magnitude is often at an interior support of an overhanging beam.
- Treating a couple as if it changed the shear. It changes only $M$.
- Writing a distributed load that stops at $x = b$ as $w_0\langle x - a\rangle^0$ without cancelling it at $b$.

## Moving Loads

For bridges and crane runways the load position varies. The influence line for $V$ or $M$ at a fixed section is the value of that quantity as a function of the position of a unit load. For a simply supported beam, the influence line for the moment at $x = a$ is a triangle with peak $a(L - a)/L$ under the section, so a single moving load $P$ produces the largest moment at $a$ when it stands at $a$. Influence lines are a different object from the diagrams in this note, which fix the loads and vary the section.

## Key Takeaways

- With $w$ positive downward and $M$ positive when sagging, $dV/dx = -w$ and $dM/dx = V$.
- Point forces make $V$ jump and $M$ kink; clockwise couples make $M$ jump by $+C$ and leave $V$ unchanged.
- The moment is stationary where $V = 0$, but the largest magnitude may sit at a support, an end or a couple.
- The diagram must close: $V$ and $M$ return to the support values at the right end, which checks the reactions.
- Macaulay brackets write $V$, $M$ and the deflection of a beam with many loads as single expressions.

## Related Scripts

- [Shear and Moment Diagrams of Beams](../../../scripts/algorithms/beams_shear_moment_diagrams/): solves statically determinate and indeterminate beams with Euler–Bernoulli finite elements and draws the load, shear-force, bending-moment and deflection diagrams with their extreme values.

## Exercises

**Exercise 1.** A cantilever of length $L$ carries a uniform load $w$. Without detailed calculation, state the shapes of the shear and moment diagrams, their maximum values and where they occur.

<details>
<summary>Answer</summary>

Since $dV/dx = -w$ is constant, the shear is linear, from zero at the free end to magnitude $wL$ at the wall. Since $dM/dx = V$, the moment is parabolic, with zero slope at the free end (where $V = 0$) and magnitude $wL^2/2$ at the wall. The moment is hogging (negative) along the whole beam.

</details>

**Exercise 2.** A simply supported beam of span 6 m carries a triangular load rising from zero at A to $w_0 = 12$ kN/m at B. Find the reactions, the location of zero shear and the maximum moment.

<details>
<summary>Answer</summary>

The total load is $w_0L/2 = 36$ kN, acting at $2L/3 = 4$ m from A, so $R_B = 36(4)/6 = 24$ kN and $R_A = 12$ kN.

With $w(x) = 2x$ kN/m, $V(x) = 12 - x^2$, which is zero at $x = \sqrt{12} = 3.46$ m. Then

```math
M(x) = 12x - \frac{x^3}{3}, \qquad M_{\max} = 12(3.464) - \frac{3.464^3}{3} = 27.7 \ \mathrm{kN\,m}
```

which agrees with the closed form $w_0L^2/(9\sqrt{3})$.

</details>

**Exercise 3.** A simply supported beam of span 8 m carries a single clockwise couple $M_0 = 40$ kN m at $x = 3$ m and no other load. Find the reactions and sketch the shear and moment diagrams, giving the key values.

<details>
<summary>Answer</summary>

Moments about A, counterclockwise positive: $8R_B - 40 = 0$, so $R_B = 5$ kN upward and $R_A = -5$ kN, that is 5 kN downward.

The shear is $V = -5$ kN over the whole span; the couple does not change it.

The moment is $M = -5x$ up to the couple, so $M(3^-) = -15$ kN m. The clockwise couple makes it jump by $+40$ to $M(3^+) = +25$ kN m, and it then decreases linearly to $M(8) = 25 - 5(5) = 0$.

</details>

**Exercise 4.** A beam is supported at A ($x = 0$) and B ($x = 6$ m) with an overhang to C ($x = 8$ m), and carries 10 kN/m over its whole length. Find the reactions, the maximum positive and negative moments, and the point of contraflexure between A and B.

<details>
<summary>Answer</summary>

Moments about A: $6R_B = 80(4)$, so $R_B = 53.3$ kN and $R_A = 26.7$ kN.

In AB, $V = 26.7 - 10x$, which is zero at $x = 2.67$ m, where

```math
M_{\max}^+ = 26.67(2.667) - 5(2.667)^2 = 35.6 \ \mathrm{kN\,m}
```

At B the overhang gives $M_B = -10(2)^2/2 = -20$ kN m.

Contraflexure: $26.67x - 5x^2 = 0$ gives $x = 5.33$ m.

</details>

**Exercise 5.** Write $V(x)$ and $M(x)$ with singularity functions for a simply supported beam of span 10 m carrying 20 kN at $x = 3$ m and 6 kN/m over $5 \le x \le 10$ m. Find the reactions and the maximum moment.

<details>
<summary>Answer</summary>

The distributed load totals 30 kN acting at 7.5 m. Moments about A: $10R_B = 20(3) + 30(7.5) = 285$, so $R_B = 28.5$ kN and $R_A = 50 - 28.5 = 21.5$ kN.

```math
V(x) = 21.5 - 20\langle x - 3\rangle^0 - 6\langle x - 5\rangle^1
```

```math
M(x) = 21.5x - 20\langle x - 3\rangle^1 - 3\langle x - 5\rangle^2
```

The shear is $+21.5$ kN up to the load, then $+1.5$ kN, and it reaches zero where $1.5 - 6(x - 5) = 0$, at $x = 5.25$ m. There

```math
M_{\max} = 21.5(5.25) - 20(2.25) - 3(0.25)^2 = 67.69 \ \mathrm{kN\,m}
```

slightly above $M(3) = 64.5$ kN m under the point load. Check: $M(10) = 215 - 140 - 75 = 0$.

</details>

## References

- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Hibbeler, R. C., *Structural Analysis*, 10th ed., Pearson, 2018.
- Macaulay, W. H., "Note on the deflection of beams", *Messenger of Mathematics*, 48, 129–130, 1919.
- Timoshenko, S. P., and Young, D. H., *Elements of Strength of Materials*, 5th ed., Van Nostrand, 1968.
