# Axial Loading

Axial loading refers to forces applied along the longitudinal axis of a structural member, resulting in either tension or compression. Understanding axial deformation is fundamental for analyzing bars, rods, cables, columns, and truss members.

## Deformation Under Axial Load

### Basic Deformation Formula

For a prismatic bar of constant cross-section under a constant axial force:

$$
\delta = \frac{PL}{AE}
$$

where:

- $\delta$ = axial deformation (elongation or shortening)
- $P$ = applied axial force
- $L$ = original length of the member
- $A$ = cross-sectional area
- $E$ = elastic modulus (Young's modulus)

### Variable Cross-Section or Loading

When the cross-section, internal force, or material varies along the length:

$$
\delta = \int_0^L \frac{N(x)}{A(x) E(x)} \, dx
$$

where $N(x)$ is the internal axial force at position $x$.

### Segmented Members

For a bar composed of $n$ segments, each with constant properties:

$$
\delta = \sum_{i=1}^{n} \frac{N_i L_i}{A_i E_i}
$$

This approach is used for stepped shafts, composite bars, and members with multiple applied loads.

## Statically Indeterminate Axially Loaded Members

### Identifying Indeterminate Problems

A problem is statically indeterminate when the number of unknown reactions exceeds the number of available equilibrium equations. An additional **compatibility equation** (geometric constraint) is required.

### Solution Procedure

1. **Equilibrium**: Write the available equilibrium equation(s)
2. **Compatibility**: Identify the geometric constraint on deformation
3. **Force–deformation**: Express deformations in terms of internal forces using $\delta = PL/(AE)$
4. **Solve**: Combine equations to find unknown forces and deformations

### Example: Bar Fixed at Both Ends

For a bar fixed at both ends with an applied load $P$ at an intermediate point:

**Equilibrium:**

$$
R_A + R_B = P
$$

**Compatibility (total deformation is zero):**

$$
\delta_{AB} = 0 \implies \frac{R_A L_1}{A E} - \frac{R_B L_2}{A E} = 0
$$

**Solving:**

$$
R_A = P \frac{L_2}{L_1 + L_2}, \quad R_B = P \frac{L_1}{L_1 + L_2}
$$

## Thermal Deformation and Stress

### Free Thermal Expansion

When a member is free to expand or contract due to a temperature change:

$$
\delta_T = \alpha \Delta T L
$$

where:

- $\alpha$ = coefficient of thermal expansion
- $\Delta T$ = change in temperature
- $L$ = original length

No stress develops in a freely expanding member.

### Constrained Thermal Expansion

When thermal expansion is partially or fully restrained, thermal stresses develop:

$$
\sigma_T = E \alpha \Delta T
$$

For a bar fixed at both ends with a temperature increase, the bar is in compression because it cannot expand.

### Combined Mechanical and Thermal Loading

The total deformation is the sum of mechanical and thermal contributions:

$$
\delta_{total} = \frac{PL}{AE} + \alpha \Delta T L
$$

For a statically indeterminate system, set the total deformation equal to the geometric constraint and solve for the unknown force.

## Stress Concentration in Axial Loading

### Stress Concentration Factor

Geometric discontinuities such as holes, notches, and fillets cause localized stress amplification:

$$
\sigma_{max} = K_t \sigma_{nom}
$$

where $K_t$ is the stress concentration factor and $\sigma_{nom}$ is the nominal stress based on the net cross-section.

### Common Configurations

| Feature | Typical $K_t$ |
| --- | --- |
| Circular hole in a wide plate | 3.0 |
| Semicircular notch | 3.0 |
| U-shaped notch | 1.5–3.0 |
| Shoulder fillet | 1.5–2.5 |

### Design Recommendations

- Use generous fillet radii at section changes ($K_t$ decreases as $r/d$ increases)
- Avoid sharp corners and abrupt geometry transitions
- For fatigue loading, use the fatigue stress concentration factor $K_f \leq K_t$

## Example Problems

### Example 1: Composite Bar Under Axial Load

A steel pipe (outer diameter 60 mm, inner diameter 50 mm) is filled with concrete, forming a composite column. An axial compressive load of 200 kN is applied.

**Given:**

- Steel: $E_s = 200$ GPa, $d_o = 60$ mm, $d_i = 50$ mm
- Concrete: $E_c = 25$ GPa, $d = 50$ mm
- $P = 200$ kN

**Find:** Stress in each material and the deformation of the column ($L = 1.5$ m).

**Solution:**

**Areas:**

$$
A_s = \frac{\pi}{4}(60^2 - 50^2) = 863.9 \text{ mm}^2
$$

$$
A_c = \frac{\pi}{4}(50^2) = 1963.5 \text{ mm}^2
$$

**Compatibility** — both materials deform equally:

$$
\delta_s = \delta_c \implies \frac{P_s L}{A_s E_s} = \frac{P_c L}{A_c E_c}
$$

$$
\frac{P_s}{A_s E_s} = \frac{P_c}{A_c E_c}
$$

**Equilibrium:**

$$
P_s + P_c = 200 \text{ kN}
$$

From compatibility:

$$
P_s = P_c \frac{A_s E_s}{A_c E_c} = P_c
\frac{863.9 \times 200}{1963.5 \times 25} = 3.52\, P_c
$$

Substituting into equilibrium:

$$
3.52\, P_c + P_c = 200 \implies P_c = 44.2 \text{ kN}, \quad P_s = 155.8 \text{ kN}
$$

**Stresses:**

$$
\sigma_s = \frac{155\,800}{863.9} = 180.3 \text{ MPa}
$$

$$
\sigma_c = \frac{44\,200}{1963.5} = 22.5 \text{ MPa}
$$

**Deformation:**

$$
\delta = \frac{P_s L}{A_s E_s} = \frac{155\,800 \times 1500}{863.9 \times 200\,000} = 1.35 \text{ mm}
$$

### Example 2: Thermal Stress in a Constrained Bar

An aluminum bar ($L = 0.5$ m) is placed between two rigid walls at 20°C. The temperature is raised to 80°C.

**Given:**

- $E_{Al} = 70$ GPa, $\alpha_{Al} = 23 \times 10^{-6}$ /°C
- $\Delta T = 60^\circ\text{C}$, $L = 0.5$ m

**Find:** Stress in the bar.

**Solution:**

The bar is fully constrained, so the total deformation must be zero:

$$
\delta_{total} = \delta_T + \delta_P = 0
$$

$$
\alpha \Delta T L + \frac{PL}{AE} = 0
$$

$$
\sigma = -E\alpha\Delta T = -70 \times 10^3 \times 23 \times 10^{-6} \times 60 = -96.6
\text{ MPa}
$$

The negative sign indicates compressive stress, as the constrained bar cannot expand.

### Example 3: Bar with a Hole Under Tension

A flat bar (width $w = 50$ mm, thickness $t = 10$ mm) has a central hole of diameter $d = 10$ mm and is subjected to an axial tensile load $P = 20$ kN.

**Given:**

- $w = 50$ mm, $t = 10$ mm, $d = 10$ mm
- $P = 20$ kN, $K_t \approx 2.5$ (net-section chart value for $d/w = 0.2$; the value 3.0 applies to a hole in a very wide plate)

**Find:** Maximum stress at the hole.

**Solution:**

**Net area:**

$$
A_{net} = (w - d) \times t = (50 - 10) \times 10 = 400 \text{ mm}^2
$$

**Nominal stress:**

$$
\sigma_{nom} = \frac{P}{A_{net}} = \frac{20\,000}{400} = 50 \text{ MPa}
$$

**Maximum stress:**

$$
\sigma_{max} = K_t \times \sigma_{nom} = 2.5 \times 50 = 125 \text{ MPa}
$$

## Principle of Saint-Venant

Saint-Venant's principle states that localized effects of loading become negligible at a distance roughly equal to the largest cross-sectional dimension away from the point of load application. This justifies using the uniform stress formula $\sigma = P/A$ away from supports and load points.

## Applications

### Structural Engineering

- **Truss members**: all members carry purely axial loads
- **Tie rods and anchor bolts**: tension members in foundations
- **Columns**: short columns under compression

### Mechanical Engineering

- **Connecting rods**: cyclic axial loading in engines
- **Bolted joints**: preload analysis requires axial deformation calculations
- **Press-fit assemblies**: interference fits generate thermal and mechanical axial stress

### Aerospace Engineering

- **Fuselage stringers**: axial load paths in aircraft structures
- **Launch vehicle structures**: thermal stresses during ascent heating

## Practical Tips

- Always check whether a problem is statically determinate or indeterminate before solving
- Sign convention matters: define tension as positive, compression as negative
- In composite members, stiffer materials (higher $EA$) carry a larger share of the load
- Thermal stresses can be very large — always consider temperature effects in constrained systems
- Stress concentrations are critical for fatigue but less so for static ductile failure

Mastery of axial loading analysis is the foundation for tackling more complex loading scenarios such as torsion, bending, and combined loading.

## Exercises

**Exercise 1.** A steel bar ($E = 200$ GPa) is fixed at A. Segment AB is 1 m long with $A = 400$ mm²; segment BC is 0.5 m long with $A = 200$ mm². A 50 kN force pulls to the right at B, and a 20 kN force pushes to the left at C. Find the internal force in each segment and the displacement of C.

<details>
<summary>Answer</summary>

Cutting each segment and looking at the free end:

- BC carries the load at C: $N_{BC} = -20$ kN (compression)
- AB carries both loads: $N_{AB} = 50 - 20 = 30$ kN (tension)

$$
\delta_C = \frac{30\,000 \times 1000}{400 \times 200\,000} +
\frac{-20\,000 \times 500}{200 \times 200\,000} = 0.375 - 0.250 = 0.125 \text{ mm}
$$

C moves 0.125 mm to the right.

</details>

**Exercise 2.** A bar of cross-section 300 mm² is fixed between two walls. A 60 kN axial load is applied 0.4 m from wall A and 0.6 m from wall B. Find both reactions and the stress in each segment.

<details>
<summary>Answer</summary>

From the formula in the notes:

$$
R_A = P \frac{L_2}{L_1 + L_2} = 60 \times 0.6 = 36 \text{ kN}, \quad R_B = 60 \times
0.4 = 24 \text{ kN}
$$

The shorter, stiffer segment takes more load. Segment A is in tension, $36\,000/300 = 120$ MPa; segment B is in compression, $24\,000/300 = 80$ MPa.

</details>

**Exercise 3.** Repeat Example 2 (aluminium bar, $L = 0.5$ m, $\Delta T = 60^\circ$C), but with a 0.2 mm gap between the bar and one wall at the start. Find the stress after heating.

<details>
<summary>Answer</summary>

Free expansion: $\alpha\Delta T L = 23 \times 10^{-6} \times 60 \times 500 = 0.69$ mm. The gap absorbs 0.2 mm, so the walls suppress the remaining 0.49 mm:

$$
\sigma = -E \frac{0.49}{500} = -70\,000 \times 9.8 \times 10^{-4} = -68.6 \text{ MPa}
$$

The stress is compressive. A small gap removes 29% of the thermal stress, which is the idea behind expansion joints.

</details>

**Exercise 4.** For the concrete-filled steel pipe of Example 1, what axial load makes the steel reach its yield stress of 250 MPa? What is the concrete stress at that load, and is it likely to be acceptable?

<details>
<summary>Answer</summary>

Both materials share the same strain $\epsilon = \sigma_s/E_s = 1.25 \times 10^{-3}$, so

$$
P = \epsilon\,(A_s E_s + A_c E_c) = 1.25 \times
10^{-3}\,(863.9 \times 200\,000 + 1963.5 \times 25\,000) = 277 \text{ kN}
$$

The concrete stress is $\sigma_c = E_c\epsilon = 31.3$ MPa. That is close to or above the compressive strength of ordinary concrete, so the concrete may govern before the steel yields. The confinement provided by the pipe raises the concrete's effective strength.

</details>

**Exercise 5.** The plate of Example 3 ($w = 50$ mm, $t = 10$ mm, hole $d = 10$ mm, $K_t \approx 2.5$) is made of a steel whose allowable peak stress is 180 MPa. What is the largest axial load? Why do designers often ignore $K_t$ for a single static load on a ductile plate, but never for fatigue?

<details>
<summary>Answer</summary>

$$
P_{max} = \frac{\sigma_{allow}A_{net}}{K_t} = \frac{180 \times 400}{2.5} = 28.8
\text{ kN}
$$

Under a single static load a ductile material yields locally at the hole edge and redistributes the stress, so the net-section stress $P/A_{net}$ governs failure. Under cyclic loading, fatigue cracks start at the stress peak, so the concentration (through $K_f$) directly shortens life.

</details>

## References

- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 8th ed., Cengage Learning, 2013.
- Pilkey, W. D., and Pilkey, D. F., *Peterson's Stress Concentration Factors*, 3rd ed., Wiley, 2008.
