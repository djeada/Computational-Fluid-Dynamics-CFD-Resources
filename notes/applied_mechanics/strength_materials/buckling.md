# Buckling and Stability

Buckling is a sudden lateral deflection of a structural member subjected to compressive loading. Unlike material failure (yielding or fracture), buckling is a stability failure that can occur at stresses well below the material's yield strength. It is one of the most critical considerations in the design of columns, struts, and thin-walled structures.

## Euler's Buckling Formula

### Critical Load

Leonhard Euler derived the critical buckling load for an ideal, slender, perfectly straight column with pinned ends:

$$
P_{cr} = \frac{\pi^2 EI}{L^2}
$$

where:

- $P_{cr}$ = critical (Euler) buckling load
- $E$ = elastic modulus of the material
- $I$ = minimum moment of inertia of the cross-section
- $L$ = length of the column (for pin-pin end conditions)

### Critical Stress

The critical buckling stress is obtained by dividing by the cross-sectional area:

$$
\sigma_{cr} = \frac{P_{cr}}{A} = \frac{\pi^2 E}{(L/r)^2}
$$

where $r = \sqrt{I/A}$ is the **radius of gyration** and $L/r$ is the **slenderness ratio**.

### Assumptions

Euler's formula is valid when:

1. The column is perfectly straight (no initial imperfection)
2. The load is applied exactly at the centroid
3. The material is linearly elastic ($\sigma_{cr} < \sigma_y$)
4. The column is long and slender

## Effective Length for Different End Conditions

### Effective Length Concept

The **effective length** $L_e$ accounts for different end support conditions by relating them to the equivalent pin-pin column:

$$
P_{cr} = \frac{\pi^2 EI}{L_e^2}
$$

where $L_e = KL$ and $K$ is the **effective length factor**.

### Effective Length Factors

| End Conditions | $K$ (theoretical) | $K$ (recommended) | Description |
| --- | --- | --- | --- |
| Pin–Pin | 1.0 | 1.0 | Both ends free to rotate |
| Fixed–Free (cantilever) | 2.0 | 2.1 | One end fixed, other free |
| Fixed–Fixed | 0.5 | 0.65 | Both ends fully restrained |
| Fixed–Pin | 0.7 | 0.80 | One end fixed, other pinned |

The recommended values are higher than theoretical because perfectly rigid connections are impossible to achieve in practice.

### Critical Stress with Effective Length

$$
\sigma_{cr} = \frac{\pi^2 E}{(L_e/r)^2} = \frac{\pi^2 E}{(KL/r)^2}
$$

## Slenderness Ratio

### Definition

The slenderness ratio is the key parameter governing column behavior:

$$
\lambda = \frac{L_e}{r} = \frac{KL}{r}
$$

where $r = \sqrt{I_{min}/A}$ is the minimum radius of gyration.

### Column Classification

- **Short columns** ($\lambda < 30$–50): Failure by crushing (material yielding), not buckling
- **Intermediate columns** ($30 < \\lambda < $ critical): Inelastic buckling
- **Long (slender) columns** ($\\lambda > $ critical): Elastic (Euler) buckling

The **critical slenderness ratio** separating elastic and inelastic buckling is:

$$
\lambda_c = \sqrt{\frac{\pi^2 E}{\sigma_y}}
$$

For structural steel ($E = 200$ GPa, $\sigma_y = 250$ MPa): $\lambda_c \approx 89$.

### Buckling Direction

A column buckles about the axis with the **minimum moment of inertia** (minimum $r$). For non-symmetric sections, always check both principal axes.

## Inelastic Buckling

### Tangent Modulus Theory

When the critical stress exceeds the proportional limit, the material is no longer linearly elastic, and Euler's formula overestimates the buckling load. The **tangent modulus theory** replaces $E$ with the tangent modulus $E_t$:

$$
\sigma_{cr} = \frac{\pi^2 E_t}{(L_e/r)^2}
$$

where $E_t = d\sigma/d\epsilon$ is the slope of the stress-strain curve at the stress level $\sigma_{cr}$.

### Reduced Modulus (Engesser–von Kármán)

The reduced modulus theory accounts for the fact that fibers on the unloading side of the cross-section behave elastically:

$$
E_r = \frac{4EE_t}{(\sqrt{E} + \sqrt{E_t})^2}
$$

In practice, the actual buckling load lies between the tangent modulus and reduced modulus predictions.

### Empirical Formulas

Several empirical and semi-empirical formulas bridge the gap between short-column yielding and long-column Euler buckling:

**Johnson's parabolic formula** (for intermediate columns):

$$
\sigma_{cr} = \sigma_y - \frac{\sigma_y^2}{4\pi^2 E}\left(\frac{L_e}{r}\right)^2
$$

Valid for $L_e/r \leq \lambda_c$, where $\lambda_c = \sqrt{2\pi^2 E / \sigma_y}$.

## Column Design

### Allowable Stress Approach

The allowable compressive stress for column design incorporates a factor of safety:

$$
\sigma_{allow} = \frac{\sigma_{cr}}{FS}
$$

The required cross-section must satisfy:

$$
\frac{P}{A} \leq \sigma_{allow}
$$

### Design Procedure

1. **Estimate** the effective length $L_e = KL$
2. **Assume** a trial cross-section and compute $r_{min}$, $\lambda = L_e/r_{min}$
3. **Determine** $\sigma_{cr}$ from the appropriate formula (Euler or Johnson)
4. **Apply** the factor of safety to get $\sigma_{allow}$
5. **Check** that $P/A \leq \sigma_{allow}$
6. **Iterate** if necessary to optimize the section

### AISC Design Approach (Steel Columns)

The AISC specification uses a unified approach:

For $\lambda_c = (KL/r)\sqrt{\sigma_y/(\pi^2 E)} \leq 1.5$ (inelastic buckling):

$$
\sigma_{cr} = (0.658^{\lambda_c^2})\sigma_y
$$

For $\lambda_c > 1.5$ (elastic buckling):

$$
\sigma_{cr} = \frac{0.877}{\lambda_c^2}\sigma_y
$$

## Example Problems

### Example 1: Euler Buckling of a Pin-Pin Column

A steel column ($E = 200$ GPa) has a W200×46 wide-flange section ($I_{min} = 15.4 \times 10^6$ mm$^4$, $A = 5890$ mm$^2$) and a length of 5 m with pin-pin end conditions.

**Given:**

- $E = 200$ GPa, $L = 5$ m, $K = 1.0$
- $I_{min} = 15.4 \times 10^6$ mm$^4$, $A = 5890$ mm$^2$

**Find:** Critical buckling load and stress.

**Solution:**

**Effective length:**

$$
L_e = KL = 1.0 \times 5000 = 5000 \text{ mm}
$$

**Critical load:**

$$
P_{cr} = \frac{\pi^2 EI_{min}}{L_e^2} = \frac{\pi^2 \times 200\,000 \times 15.4 \times 10^6}{5000^2}
$$

$$
P_{cr} = \frac{3.041 \times 10^{13}}{25 \times 10^6} = 1216 \text{ kN}
$$

**Critical stress:**

$$
\sigma_{cr} = \frac{P_{cr}}{A} = \frac{1\,216\,000}{5890} = 206.4 \text{ MPa}
$$

**Check:** $r_{min} = \sqrt{I/A} = \sqrt{15.4 \times 10^6 / 5890} = 51.1$ mm

$\lambda = L_e/r = 5000/51.1 = 97.8$

For steel with $\sigma_y = 250$ MPa: $\lambda_c = \sqrt{\pi^2 \times 200\,000/250} = 88.9$

Since $\lambda = 97.8 > \lambda_c = 88.9$, Euler's formula is valid (elastic buckling).

### Example 2: Effect of End Conditions

For the same column as Example 1, compare the critical loads for different end conditions.

**Solution:**

| End Condition | $K$ | $L_e$ (mm) | $P_{cr}$ (kN) | Ratio |
| --- | --- | --- | --- | --- |
| Pin–Pin | 1.0 | 5000 | 1216 | 1.0 |
| Fixed–Pin | 0.7 | 3500 | 2482 | 2.04 |
| Fixed–Fixed | 0.5 | 2500 | 4864 | 4.0 |
| Fixed–Free | 2.0 | 10000 | 304 | 0.25 |

End conditions have a dramatic effect. A fixed-fixed column carries 4× the load of a pin-pin column.

### Example 3: Column Design with Johnson's Formula

Design a steel column ($E = 200$ GPa, $\sigma_y = 350$ MPa) to carry $P = 400$ kN with a length of 3 m and pin-pin ends. Use a factor of safety of 2.0 and a solid circular cross-section.

**Given:**

- $P = 400$ kN, $L = 3$ m, $K = 1.0$, $FS = 2.0$
- $E = 200$ GPa, $\sigma_y = 350$ MPa

**Find:** Required diameter.

**Solution:**

**Required load capacity:**

$$
P_{design} = FS \times P = 2.0 \times 400 = 800 \text{ kN}
$$

**Trial:** Assume $d = 80$ mm.

$$
A = \frac{\pi (80)^2}{4} = 5027 \text{ mm}^2, \quad I = \frac{\pi (80)^4}{64} = 2.011
\times 10^6 \text{ mm}^4
$$

$$
r = \sqrt{I/A} = \sqrt{2.011 \times 10^6 / 5027} = 20.0 \text{ mm}
$$

$$
\lambda = \frac{L_e}{r} = \frac{3000}{20} = 150
$$

$$
\lambda_c = \sqrt{\frac{2\pi^2 \times 200\,000}{350}} = 106.2
$$

Since $\lambda = 150 > \lambda_c = 106.2$, use Euler's formula:

$$
\sigma_{cr} = \frac{\pi^2 \times 200\,000}{150^2} = 87.7 \text{ MPa}
$$

$$
P_{cr} = 87.7 \times 5027 = 441 \text{ kN} < 800 \text{ kN}
$$

Not adequate. Try $d = 100$ mm:

$$
A = 7854 \text{ mm}^2, \quad r = 25.0 \text{ mm}, \quad \lambda = 3000/25 = 120
$$

$$
\sigma_{cr} = \frac{\pi^2 \times 200\,000}{120^2} = 137.1 \text{ MPa}
$$

$$
P_{cr} = 137.1 \times 7854 = 1077 \text{ kN} > 800 \text{ kN}
$$

Select $d = 100$ mm with an actual factor of safety of $1077/400 = 2.69$.

## Imperfection Effects

Real columns always have initial imperfections (crookedness, load eccentricity). The **secant formula** accounts for eccentric loading:

$$
\sigma_{max} = \frac{P}{A}\left[1 + \frac{ec}{r^2}\sec\left(\frac{L_e}{2r}
\sqrt{\frac{P}{AE}}\right)\right]
$$

where $e$ is the load eccentricity and $c$ is the distance from the neutral axis to the extreme fiber.

## Applications

### Structural Engineering

- **Building columns**: steel and concrete column design under gravity and lateral loads
- **Bracing members**: compression diagonals in braced frames
- **Truss members**: compression chords and web members

### Mechanical Engineering

- **Piston rods**: slender members under cyclic compression
- **Connecting rods**: buckling under peak compressive loads
- **Jack screws**: long slender screws under compressive force

### Aerospace Engineering

- **Fuselage stringers**: thin compression members in aircraft skin-stringer panels
- **Rocket structures**: thin-walled cylinders under axial compression
- **Landing gear struts**: column buckling during touchdown loads

## Practical Tips

- Always use the **minimum** moment of inertia to find the critical buckling axis
- Use recommended (not theoretical) effective length factors for design safety
- Check that $\sigma_{cr} < \sigma_y$ for Euler's formula to be valid; otherwise use inelastic buckling formulas
- Bracing a column at intermediate points reduces $L_e$ and dramatically increases capacity
- For thin-walled sections, also consider **local buckling** (flange or web buckling) in addition to global buckling
- Initial imperfections significantly reduce actual buckling capacity — design codes account for this

Buckling analysis is essential for the safe design of any structural member subjected to compressive loading and must always be considered alongside material strength checks.

## Exercises

**Exercise 1.** A column has a solid rectangular section of 50 mm by 100 mm and is pinned at both ends in both planes. About which axis does it buckle, and what is the ratio of the two Euler loads?

<details>
<summary>Answer</summary>

$I_{min} = 100 \times 50^3/12 = 1.04 \times 10^6$ mm⁴ (bending across the 50 mm dimension) and $I_{max} = 50 \times 100^3/12 = 4.17 \times 10^6$ mm⁴.

The column buckles about the weak axis, bending in the direction of the 50 mm dimension, at one quarter of the load for the strong axis. Bracing the weak direction at mid-height halves $L_e$ for that axis and equalises the two loads.

</details>

**Exercise 2.** An aluminium tube ($E = 70$ GPa, $\sigma_y = 240$ MPa), outer diameter 50 mm and inner diameter 44 mm, is a 2 m flagpole-type strut fixed at the base and free at the top. Find the Euler buckling load and check that Euler's formula applies.

<details>
<summary>Answer</summary>

$I = \pi(50^4 - 44^4)/64 = 1.228 \times 10^5$ mm⁴, $A = 443$ mm², $r = 16.65$ mm, and $L_e = 2L = 4000$ mm (theoretical $K = 2$).

$$
P_{cr} = \frac{\pi^2 \times 70\,000 \times 1.228 \times 10^5}{4000^2} = 5.30 \text{ kN},
\quad \sigma_{cr} = 12.0 \text{ MPa}
$$

$\lambda = 4000/16.65 = 240$, far above $\sqrt{\pi^2 E/\sigma_y} = 53.7$, so buckling is elastic and Euler applies. The stress at buckling is only 5% of the yield strength.

</details>

**Exercise 3.** A solid round steel strut ($E = 200$ GPa, $\sigma_y = 350$ MPa), 60 mm in diameter and 1.2 m long, is pinned at both ends. Find its critical load with the appropriate formula, and compare it with the Euler prediction.

<details>
<summary>Answer</summary>

$r = d/4 = 15$ mm, so $\lambda = 1200/15 = 80$. The Johnson limit is $\sqrt{2\pi^2 E/\sigma_y} = 106.2$; since $80 < 106.2$, use Johnson:

$$
\sigma_{cr} = 350 - \frac{350^2}{4\pi^2 \times 200\,000}(80)^2 = 350 - 99.3 = 250.7
\text{ MPa}
$$

$A = 2827$ mm², so $P_{cr} = 709$ kN.

Euler would give $\pi^2 E/\lambda^2 = 308$ MPa, or 872 kN, an unsafe overestimate of 23%.

</details>

**Exercise 4.** At the buckling stress, a material has $E = 200$ GPa and tangent modulus $E_t = 50$ GPa. For a rectangular-section column with $L_e/r = 80$, compare the tangent-modulus and reduced-modulus buckling stresses.

<details>
<summary>Answer</summary>

$$
E_r = \frac{4EE_t}{(\sqrt{E} + \sqrt{E_t})^2} = \frac{4 \times 200 \times 50}{(14.14 + 7.07)^2} = 88.9 \text{ GPa}
$$

- Tangent modulus: $\sigma_{cr} = \pi^2 (50\,000)/80^2 = 77.1$ MPa
- Reduced modulus: $\sigma_{cr} = \pi^2 (88\,900)/80^2 = 137.1$ MPa

Shanley's analysis shows buckling begins near the tangent-modulus load, so the lower value is the one used in design.

</details>

**Exercise 5.** The W200×46 column of Example 1 ($A = 5890$ mm², $r = 51.1$ mm, $L_e = 5$ m, $E = 200$ GPa) carries 400 kN at an eccentricity of 10 mm about its weak axis. Taking $c = 100$ mm, use the secant formula to find the maximum compressive stress.

<details>
<summary>Answer</summary>

$P/A = 67.9$ MPa and $ec/r^2 = 10 \times 100/51.1^2 = 0.383$.

$$
\frac{L_e}{2r} \sqrt{\frac{P}{AE}} = \frac{5000}{102.3}
\sqrt{\frac{400\,000}{5890 \times 200\,000}} = 0.901 \text{ rad}, \quad
\sec(0.901) = 1.611
$$

$$
\sigma_{max} = 67.9\,(1 + 0.383 \times 1.611) = 109.7 \text{ MPa}
$$

A 10 mm eccentricity raises the peak stress by 62% over $P/A$.

</details>

## References

- Timoshenko, S. P., and Gere, J. M., *Theory of Elastic Stability*, 2nd ed., McGraw-Hill, 1961.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 8th ed., Cengage Learning, 2013.
