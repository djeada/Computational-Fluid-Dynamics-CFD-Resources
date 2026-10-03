# Bending of Beams

Bending is one of the most common loading conditions in structural and mechanical engineering. When a beam is subjected to transverse loads, it develops internal bending moments that produce normal stresses and shear stresses throughout the cross-section.

## Flexure Formula

### Normal Stress Due to Bending

The flexure formula gives the normal stress at any point in the cross-section of a beam subjected to pure bending:

$$
\sigma = \frac{My}{I}
$$

where:

- $\sigma$ = normal stress at distance $y$ from the neutral axis
- $M$ = internal bending moment at the section
- $y$ = perpendicular distance from the neutral axis
- $I$ = second moment of area (moment of inertia) about the neutral axis

**Maximum bending stress** occurs at the extreme fibers ($y = c$):

$$
\sigma_{max} = \frac{Mc}{I} = \frac{M}{S}
$$

where $S = I/c$ is the **section modulus**.

### Assumptions

The flexure formula is based on:

1. Plane sections remain plane after bending (Bernoulli hypothesis)
2. Material is linearly elastic and homogeneous
3. The beam has a plane of symmetry, and loads act in that plane
4. Deformations are small compared to beam dimensions

## Neutral Axis and Section Properties

### Neutral Axis

The neutral axis passes through the centroid of the cross-section. At this axis:

- Normal stress is zero ($\sigma = 0$)
- Material transitions from tension to compression

For a symmetric cross-section, the neutral axis is the axis of symmetry. For unsymmetric sections, the centroid must be calculated:

$$
\bar{y} = \frac{\sum A_i \bar{y}_i}{\sum A_i}
$$

### Section Modulus

The section modulus simplifies bending stress calculations:

$$
S = \frac{I}{c}
$$

For unsymmetric sections, two section moduli exist — one for the top fiber and one for the bottom fiber.

## Moment of Inertia for Common Cross-Sections

| Cross-Section | Moment of Inertia $I$ | Section Modulus $S$ |
| --- | --- | --- |
| Rectangle ($b \times h$) | $\dfrac{bh^3}{12}$ | $\dfrac{bh^2}{6}$ |
| Circle (diameter $d$) | $\dfrac{\pi d^4}{64}$ | $\dfrac{\pi d^3}{32}$ |
| Hollow circle ($d_o$, $d_i$) | $\dfrac{\pi(d_o^4 - d_i^4)}{64}$ | $\dfrac{\pi(d_o^4 - d_i^4)}{32 d_o}$ |
| I-beam (flanges + web) | Use parallel axis theorem | $I/c$ |

### Parallel Axis Theorem

To find the moment of inertia about an axis parallel to the centroidal axis:

$$
I = I_c + Ad^2
$$

where:

- $I_c$ = moment of inertia about the centroidal axis
- $A$ = area of the shape
- $d$ = distance between the two parallel axes

This theorem is essential for computing the moment of inertia of composite cross-sections.

## Shear Stress in Beams

Transverse loads also produce shear stress in the beam cross-section:

$$
\tau = \frac{VQ}{It}
$$

where:

- $V$ = internal shear force at the section
- $Q$ = first moment of the area above (or below) the point about the neutral axis
- $I$ = moment of inertia of the entire cross-section
- $t$ = width of the cross-section at the point of interest

**For a rectangular cross-section:**

$$
\tau_{max} = \frac{3V}{2A}
$$

which occurs at the neutral axis.

## Beam Deflection — Double Integration Method

### Governing Equation

The elastic curve of a beam is governed by the Euler–Bernoulli equation:

$$
EI \frac{d^2y}{dx^2} = M(x)
$$

where $y(x)$ is the deflection of the beam at position $x$.

### Procedure

1. Determine the bending moment $M(x)$ as a function of $x$
2. Integrate once to get the slope: $EI\dfrac{dy}{dx} = \int M(x)\,dx + C_1$
3. Integrate again to get the deflection: $EI\,y = \iint M(x)\,dx\,dx + C_1 x + C_2$
4. Apply boundary conditions to find $C_1$ and $C_2$

### Common Boundary Conditions

| Support Type | Deflection | Slope |
| --- | --- | --- |
| Pin or roller | $y = 0$ | $dy/dx \neq 0$ |
| Fixed (clamped) | $y = 0$ | $dy/dx = 0$ |
| Free end | $y \neq 0$ | $dy/dx \neq 0$ |

## Superposition Method

For beams with multiple loads, the total deflection can be found by superimposing the deflections from individual load cases (valid in the linear elastic range).

### Common Deflection Formulas

**Simply supported beam, central point load $P$:**

$$
\delta_{max} = \frac{PL^3}{48EI}
$$

**Simply supported beam, uniform load $w$:**

$$
\delta_{max} = \frac{5wL^4}{384EI}
$$

**Cantilever beam, point load $P$ at free end:**

$$
\delta_{max} = \frac{PL^3}{3EI}
$$

**Cantilever beam, uniform load $w$:**

$$
\delta_{max} = \frac{wL^4}{8EI}
$$

## Example Problems

### Example 1: Bending Stress in a Rectangular Beam

A simply supported beam ($L = 4$ m) with a rectangular cross-section ($b = 100$ mm, $h = 200$ mm) carries a central point load of 20 kN.

**Given:**

- $L = 4$ m, $P = 20$ kN
- $b = 100$ mm, $h = 200$ mm

**Find:** Maximum bending stress.

**Solution:**

**Maximum bending moment (at midspan):**

$$
M_{max} = \frac{PL}{4} = \frac{20 \times 4}{4} = 20 \text{ kN}\cdot \text{m}
$$

**Moment of inertia:**

$$
I = \frac{bh^3}{12} = \frac{100 \times 200^3}{12} = 6.667 \times 10^7 \text{ mm}^4
$$

**Maximum bending stress:**

$$
\sigma_{max} = \frac{Mc}{I} = \frac{20 \times 10^6 \times 100}{6.667 \times 10^7} = 30.0
\text{ MPa}
$$

### Example 2: Cantilever Beam Deflection

A steel cantilever beam ($E = 200$ GPa, $I = 5 \times 10^6$ mm$^4$, $L = 2$ m) carries a uniform distributed load of 8 kN/m.

**Given:**

- $E = 200$ GPa, $I = 5 \times 10^6$ mm$^4$
- $L = 2$ m, $w = 8$ kN/m

**Find:** Maximum deflection at the free end.

**Solution:**

$$
\delta_{max} = \frac{wL^4}{8EI} = \frac{8 \times 2000^4}{8 \times 200\,000 \times 5 \times 10^6}
$$

$$
\delta_{max} = \frac{8 \times 1.6 \times 10^{13}}{8 \times 10^{12}} = 16.0 \text{ mm}
$$

### Example 3: Composite Cross-Section

A T-beam is composed of a flange (200 mm × 30 mm) on top of a web (30 mm × 170 mm). Find the moment of inertia about the neutral axis.

**Given:**

- Flange: $b_f = 200$ mm, $h_f = 30$ mm
- Web: $b_w = 30$ mm, $h_w = 170$ mm

**Find:** Neutral axis location and $I_{NA}$.

**Solution:**

**Centroid location** (measured from bottom):

$$
A_f = 200 \times 30 = 6000 \text{ mm}^2, \quad \bar{y}_f = 170 + 15 = 185 \text{ mm}
$$

$$
A_w = 30 \times 170 = 5100 \text{ mm}^2, \quad \bar{y}_w = 85 \text{ mm}
$$

$$
\bar{y} = \frac{6000 \times 185 + 5100 \times 85}{6000 + 5100} = \frac{1\,110\,000 + 433\,500}{11\,100} = 139.1 \text{ mm}
$$

**Moment of inertia** (parallel axis theorem):

$$
I_{NA} = \left[\frac{200 \times 30^3}{12} + 6000(185 - 139.1)^2\right] +
\left[\frac{30 \times 170^3}{12} + 5100(139.1 - 85)^2\right]
$$

$$
I_{NA} = [450\,000 + 12\,640\,860] + [12\,282\,500 + 14\,926\,731]
$$

$$
I_{NA} = 13\,090\,860 + 27\,209\,231 = 40.30 \times 10^6 \text{ mm}^4
$$

## Beam Design Considerations

### Deflection Limits

Building codes typically limit beam deflection to:

- $L/360$ for floors under live load
- $L/240$ for roofs under total load
- $L/180$ for members supporting brittle finishes

### Efficient Cross-Sections

I-beams and wide-flange sections are efficient because they concentrate material far from the neutral axis, maximizing $I$ for a given area. The optimal beam has most of its material in the flanges.

## Applications

### Structural Engineering

- **Floor beams and joists**: carry distributed and point loads
- **Bridge girders**: long-span bending under traffic loads
- **Lintels**: beams above door and window openings

### Mechanical Engineering

- **Machine frames**: bending under operational loads
- **Axles**: bending from wheel loads
- **Leaf springs**: designed for controlled bending deflection

### Aerospace Engineering

- **Wing spars**: primary bending members in aircraft wings
- **Fuselage frames**: resist bending from aerodynamic and inertial loads

## Practical Tips

- Always check both bending stress and deflection — a beam may be strong enough but too flexible
- For composite sections, calculate the centroid and use the parallel axis theorem
- Superposition is valid only in the linear elastic range
- I-beams are far more efficient than solid rectangular sections for bending
- Consider lateral-torsional buckling for long, narrow beams under bending

Understanding beam bending is essential for the design of virtually all structural and mechanical systems.

## Exercises

**Exercise 1.** The $100 \times 200$ mm rectangular beam of Example 1 is laid flat, with the 200 mm side horizontal. How do its section modulus and maximum bending stress change? Why?

<details>
<summary>Answer</summary>

- Upright: $S = bh^2/6 = 100 \times 200^2/6 = 6.67 \times 10^5$ mm³
- Flat: $S = 200 \times 100^2/6 = 3.33 \times 10^5$ mm³

The flat beam has half the section modulus, so at $M = 20$ kN·m the stress doubles from 30 MPa to 60 MPa. $S$ grows with the square of depth but only linearly with width, so material placed far from the neutral axis is more effective.

</details>

**Exercise 2.** A simply supported steel beam ($E = 200$ GPa) of span 5 m carries a uniform load of 12 kN/m. Its section has $I = 8.0 \times 10^7$ mm⁴ and $c = 150$ mm. Find the maximum bending stress and mid-span deflection, and check the deflection against $L/360$.

<details>
<summary>Answer</summary>

```math
M_{max} = \frac{wL^2}{8} = \frac{12 \times 5^2}{8} = 37.5 \text{ kN}\cdot \text{m},
\quad \sigma_{max} = \frac{37.5 \times 10^6 \times 150}{8.0 \times 10^7} = 70.3
\text{ MPa}
```

```math
\delta_{max} = \frac{5wL^4}{384EI} = \frac{5 \times 12 \times 5000^4}{384 \times 200\,000 \times 8.0 \times 10^7} = 6.10 \text{ mm}
```

$L/360 = 13.9$ mm, so the beam satisfies the limit.

</details>

**Exercise 3.** For the beam of Example 1 (central load 20 kN, section $100 \times 200$ mm), find the maximum transverse shear stress and where it occurs. Compare it with the maximum bending stress.

<details>
<summary>Answer</summary>

$V = P/2 = 10$ kN in each half.

```math
\tau_{max} = \frac{3V}{2A} = \frac{3 \times 10\,000}{2 \times 20\,000} = 0.75
\text{ MPa}
```

It occurs at the neutral axis, where the bending stress is zero. It is only 2.5% of the 30 MPa bending stress, so shear rarely governs long solid beams. It can govern short, deep beams, thin webs and timber.

</details>

**Exercise 4.** Use the double integration method to derive the tip deflection $PL^3/(3EI)$ of a cantilever of length $L$ with a point load $P$ at its free end.

<details>
<summary>Answer</summary>

Put the fixed end at $x = 0$. Then $M(x) = -P(L - x)$ and $EI\,y'' = -P(L - x)$.

Integrate once: $EI\,y' = -P(Lx - x^2/2) + C_1$, and $y'(0) = 0$ gives $C_1 = 0$.

Integrate again: $EI\,y = -P(Lx^2/2 - x^3/6) + C_2$, and $y(0) = 0$ gives $C_2 = 0$.

At $x = L$:

```math
EI\, y(L) = -P\left(\frac{L^3}{2} - \frac{L^3}{6}\right) = -\frac{PL^3}{3}
```

The negative sign means downward, and the magnitude is $PL^3/(3EI)$.

</details>

**Exercise 5.** The cantilever of Example 2 also carries a 2 kN point load at its free end. Use superposition to find the total tip deflection.

<details>
<summary>Answer</summary>

```math
\delta_P = \frac{PL^3}{3EI} = \frac{2000 \times 2000^3}{3 \times 200\,000 \times 5 \times 10^6} = 5.33 \text{ mm}
```

Adding the 16.0 mm from the distributed load gives a total of $21.3$ mm. Superposition is valid because both deflections are small and the material is linear elastic.

</details>

## References

- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 8th ed., Cengage Learning, 2013.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
