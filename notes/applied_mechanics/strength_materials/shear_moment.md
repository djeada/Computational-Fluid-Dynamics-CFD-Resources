# Shear and Moment Diagrams

Shear and moment diagrams are graphical representations of the internal shear force $V(x)$ and bending moment $M(x)$ along the length of a beam. These diagrams are essential for identifying critical sections where maximum stresses occur, enabling safe and efficient beam design.

## Relationship Between Load, Shear, and Moment

### Fundamental Differential Relations

The relationships between the distributed load $w(x)$, shear force $V(x)$, and bending moment $M(x)$ are:

$$\frac{dV}{dx} = -w(x)$$

$$\frac{dM}{dx} = V(x)$$

Combining these:

$$\frac{d^2M}{dx^2} = -w(x)$$

### Integral Forms

These differential equations can be integrated to give:

$$V(x) = V(x_0) - \int_{x_0}^{x} w(\xi)\,d\xi$$

$$M(x) = M(x_0) + \int_{x_0}^{x} V(\xi)\,d\xi$$

**Key insight:** The change in shear between two points equals the negative of the area under the load diagram; the change in moment between two points equals the area under the shear diagram.

### Important Consequences

| Load Condition | Shear Diagram | Moment Diagram |
|---------------|---------------|----------------|
| No load ($w = 0$) | Constant | Linear |
| Uniform load ($w = $ const) | Linear | Parabolic (2nd degree) |
| Linearly varying load | Parabolic | Cubic (3rd degree) |
| Concentrated force $P$ | Jump discontinuity of $P$ | Slope change (kink) |
| Concentrated moment $M_0$ | No change | Jump discontinuity of $M_0$ |

## Constructing Shear Diagrams

### Step-by-Step Procedure

1. **Calculate support reactions** from equilibrium ($\sum F = 0$, $\sum M = 0$)
2. **Start at the left end** of the beam
3. **Move right**, tracking how the shear changes:
   - Upward forces cause a positive jump in $V$
   - Downward forces cause a negative jump in $V$
   - Distributed loads change $V$ linearly (for uniform $w$)
4. **Verify** that $V$ returns to zero (or matches the reaction) at the right end

### Sign Convention

- Positive shear: net upward force to the left of the section
- Positive moment: causes the beam to sag (concave up)

## Constructing Moment Diagrams

### Step-by-Step Procedure

1. **Start at the left end** — moment is typically zero at a pin/roller or has a known value at a fixed support
2. **Add the area under the shear diagram** to get the change in moment
3. **At concentrated moments**, add or subtract the applied moment value
4. **Identify maximum moment** — occurs where $V = 0$ (since $dM/dx = V$)
5. **Verify** that $M$ returns to zero at a free end or pin/roller

### Key Points

- **Where $V = 0$**: $M$ has a local maximum or minimum
- **Where $V$ changes sign**: $M$ is at an extremum
- **Under a concentrated moment**: $M$ has a jump discontinuity

## Maximum Shear and Moment Identification

Identifying the locations and magnitudes of maximum shear and moment is the primary purpose of these diagrams.

### Maximum Shear Force

- Usually occurs at the supports
- For uniform loads: $V_{max}$ is at the reaction points
- For concentrated loads: check immediately to the left and right of each load

### Maximum Bending Moment

- Occurs where $V(x) = 0$ or changes sign
- For a simply supported beam with uniform load: $M_{max}$ is at midspan
- For a cantilever beam: $M_{max}$ is at the fixed support
- For overhanging beams: compare moment at the support and at locations where $V = 0$

## Example Problems

### Example 1: Simply Supported Beam with Uniform Load

A simply supported beam of length $L = 6$ m carries a uniform distributed load $w = 10$ kN/m.

**Given:**
- $L = 6$ m, $w = 10$ kN/m

**Find:** Shear and moment diagrams; maximum $V$ and $M$.

**Solution:**

**Reactions** (by symmetry):
$$R_A = R_B = \frac{wL}{2} = \frac{10 \times 6}{2} = 30 \text{ kN}$$

**Shear force:**
$$V(x) = R_A - wx = 30 - 10x \text{ kN}$$

$V = 0$ when $x = 3$ m (midspan).

$$V_{max} = 30 \text{ kN (at supports)}$$

**Bending moment:**
$$M(x) = R_A x - \frac{wx^2}{2} = 30x - 5x^2 \text{ kN·m}$$

$$M_{max} = M(3) = 30(3) - 5(3)^2 = 90 - 45 = 45 \text{ kN·m}$$

**Diagram shapes:**
- Shear: linear, from +30 kN to −30 kN
- Moment: parabolic, maximum of 45 kN·m at midspan

### Example 2: Cantilever Beam with Point Load

A cantilever beam of length $L = 3$ m has a point load $P = 12$ kN at the free end.

**Given:**
- $L = 3$ m, $P = 12$ kN at the free end

**Find:** Shear and moment diagrams.

**Solution:**

**Reactions at the fixed end:**
$$R_A = 12 \text{ kN (upward)}, \quad M_A = -12 \times 3 = -36 \text{ kN·m (counterclockwise)}$$

**Shear force** (measuring $x$ from the free end):
$$V(x) = -P = -12 \text{ kN (constant along the beam)}$$

**Bending moment** (measuring $x$ from the free end):
$$M(x) = -Px = -12x \text{ kN·m}$$

$$M_{max} = 36 \text{ kN·m (at fixed support)}$$

**Diagram shapes:**
- Shear: constant at −12 kN
- Moment: linear, from 0 at free end to −36 kN·m at the fixed support

### Example 3: Overhanging Beam

A beam is supported at A ($x = 0$) and B ($x = 4$ m) with an overhang to C ($x = 6$ m). A point load $P = 18$ kN acts at C.

**Given:**
- $L_{AB} = 4$ m, $L_{BC} = 2$ m
- $P = 18$ kN at C

**Find:** Reactions, shear and moment diagrams.

**Solution:**

**Reactions:**

$\sum M_A = 0$:
$$R_B \times 4 - 18 \times 6 = 0 \implies R_B = 27 \text{ kN}$$

$\sum F_y = 0$:
$$R_A + 27 - 18 = 0 \implies R_A = -9 \text{ kN (downward)}$$

**Shear diagram:**
- At A: $V = -9$ kN
- A to B: $V = -9$ kN (constant, no load between)
- At B: $V = -9 + 27 = +18$ kN
- B to C: $V = +18$ kN (constant)
- At C: $V = 18 - 18 = 0$ ✓

**Moment diagram:**
- At A: $M = 0$
- At B: $M = -9 \times 4 = -36$ kN·m
- At C: $M = -36 + 18 \times 2 = 0$ ✓

The maximum moment is $|M_{max}| = 36$ kN·m at support B. Note the negative moment indicates hogging (concave down).

### Example 4: Beam with Multiple Loads

A simply supported beam ($L = 8$ m) carries a point load $P_1 = 10$ kN at $x = 2$ m and a point load $P_2 = 20$ kN at $x = 5$ m.

**Given:**
- $L = 8$ m
- $P_1 = 10$ kN at $x = 2$ m, $P_2 = 20$ kN at $x = 5$ m

**Find:** Reactions and maximum bending moment.

**Solution:**

**Reactions:**

$\sum M_A = 0$:
$$R_B \times 8 = 10 \times 2 + 20 \times 5 = 120 \implies R_B = 15 \text{ kN}$$

$\sum F_y = 0$:
$$R_A = 10 + 20 - 15 = 15 \text{ kN}$$

**Shear diagram:**
- $0 \leq x < 2$: $V = +15$ kN
- $2 < x < 5$: $V = 15 - 10 = +5$ kN
- $5 < x \leq 8$: $V = 5 - 20 = -15$ kN

**Moment at key points:**
- $M(2) = 15 \times 2 = 30$ kN·m
- $M(5) = 15 \times 5 - 10 \times 3 = 75 - 30 = 45$ kN·m
- $M(8) = 0$ ✓

$$M_{max} = 45 \text{ kN·m at } x = 5 \text{ m}$$

## Graphical Construction Tips

### Quick Sketching Rules

1. Between point loads, the shear is constant and the moment is linear
2. Under uniform loads, the shear is linear and the moment is parabolic
3. The moment diagram is always one degree higher than the shear diagram
4. The moment curve is concave down where $w$ acts downward
5. Areas under the shear diagram give changes in moment

### Common Patterns

- **Simply supported, uniform load**: triangular shear, parabolic moment (max at center)
- **Cantilever, tip load**: constant shear, linear moment (max at wall)
- **Cantilever, uniform load**: linear shear, parabolic moment (max at wall)

## Applications

### Structural Engineering
- **Building beams**: sizing floor joists and girders for code-required load combinations
- **Bridge design**: determining critical moment and shear sections for traffic loading
- **Retaining walls**: moment diagrams for lateral earth pressure

### Mechanical Engineering
- **Machine shafts**: identifying critical cross-sections for combined shear and bending
- **Crane booms**: shear and moment analysis under moving loads
- **Vehicle frames**: load path analysis for suspension and body loads

### Influence Lines
For moving loads (bridges, cranes), influence lines show how $V$ and $M$ at a specific section vary as a unit load moves across the beam. These are closely related to shear and moment diagrams but serve a complementary purpose.

## Practical Tips

- Always verify equilibrium before drawing diagrams: $\sum F_y = 0$ and $\sum M = 0$
- Check that the moment diagram closes to zero at free ends and simple supports
- The point of maximum moment is the most critical section for bending stress design
- The points of maximum shear are critical for web shear and bearing design
- Use the area method (integrating the shear diagram) for rapid construction of moment diagrams
- For complex loadings, break the beam into segments and analyze each separately

Shear and moment diagrams are indispensable tools for structural analysis and form the basis for beam design in every branch of engineering.
