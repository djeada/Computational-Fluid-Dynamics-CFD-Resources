# Stress and Strain

Stress and strain form the fundamental concepts in strength of materials, describing how materials respond to applied forces. Understanding these concepts is essential for designing safe and efficient structures, machines, and components that can withstand operational loads without failure.

## Definition of Stress

**Stress** is the internal force per unit area that develops within a material when external forces are applied. It represents the intensity of internal forces acting on a plane through the material.

### Mathematical Definition

$$
\sigma = \lim_{\Delta A \to 0} \frac{\Delta F}{\Delta A} = \frac{dF}{dA}
$$

For uniform stress distribution:

$$
\sigma = \frac{F}{A}
$$

where:

- $\sigma$ = stress (Pa, N/m², or psi)
- $F$ = internal force (N or lbs)
- $A$ = cross-sectional area (m² or in²)

### Types of Stress

#### 1. Normal Stress

Force perpendicular to the cross-sectional area:

**Tensile Stress** (pulling apart):

$$
\sigma_t = \frac{P}{A}
$$

where $P$ is the tensile force.

**Compressive Stress** (pushing together):

$$
\sigma_c = \frac{P}{A}
$$

where $P$ is the compressive force.

#### 2. Shear Stress

Force parallel to the cross-sectional area:

$$
\tau = \frac{V}{A}
$$

where $V$ is the shear force.

**Examples:**

- Bolt in shear
- Rivet connections
- Key and shaft interfaces

### Sign Convention

- **Tensile stress**: Positive (+)
- **Compressive stress**: Negative (-)
- **Shear stress**: Positive when causing clockwise rotation

## Definition of Strain

**Strain** is the deformation per unit length that occurs when a material is subjected to stress. It is a dimensionless quantity representing the relative change in geometry.

### Mathematical Definition

$$
\epsilon = \lim_{\Delta L \to 0} \frac{\Delta L}{L} = \frac{dL}{L}
$$

For uniform deformation:

$$
\epsilon = \frac{\Delta L}{L_0}
$$

where:

- $\epsilon$ = strain (dimensionless, often expressed as %)
- $\Delta L$ = change in length
- $L_0$ = original length

### Types of Strain

#### 1. Normal Strain

Change in length per unit length:

**Tensile Strain** (elongation):

$$
\epsilon_t = \frac{\Delta L}{L_0}
$$

**Compressive Strain** (shortening):

$$
\epsilon_c = -\frac{\Delta L}{L_0}
$$

#### 2. Shear Strain

Angular distortion of a material:

$$
\gamma = \tan\theta \approx \theta
$$

where $\theta$ is the shear angle (in radians for small angles).

#### 3. Volumetric Strain

Change in volume per unit volume:

$$
\epsilon_v = \frac{\Delta V}{V_0}
$$

For isotropic materials:

$$
\epsilon_v = \epsilon_x + \epsilon_y + \epsilon_z
$$

## Stress-Strain Relationships

### Linear Elastic Behavior (Hooke's Law)

For linearly elastic materials, stress is proportional to strain:

#### Normal Stress-Strain

$$
\sigma = E\epsilon
$$

where $E$ is the **elastic modulus** (Young's modulus):

- Steel: $E \approx 200$ GPa
- Aluminum: $E \approx 70$ GPa
- Concrete: $E \approx 30$ GPa

#### Shear Stress-Strain

$$
\tau = G\gamma
$$

where $G$ is the **shear modulus**:

$$
G = \frac{E}{2(1 + \nu)}
$$

### Poisson's Effect

When a material is stretched in one direction, it contracts in the perpendicular directions:

$$
\nu = -\frac{\epsilon_{lateral}}{\epsilon_{axial}}
$$

where $\nu$ is **Poisson's ratio**:

- Most metals: $\nu \approx 0.3$
- Rubber: $\nu \approx 0.5$
- Cork: $\nu \approx 0$

**Lateral strain:**

$$
\epsilon_{lateral} = -\nu \epsilon_{axial}
$$

### Three-Dimensional Stress-Strain Relations

For a general state of stress:

$$
\epsilon_x = \frac{1}{E}[\sigma_x - \nu(\sigma_y + \sigma_z)]
$$

$$
\epsilon_y = \frac{1}{E}[\sigma_y - \nu(\sigma_x + \sigma_z)]
$$

$$
\epsilon_z = \frac{1}{E}[\sigma_z - \nu(\sigma_x + \sigma_y)]
$$

$$
\gamma_{xy} = \frac{\tau_{xy}}{G}, \quad \gamma_{yz} = \frac{\tau_{yz}}{G}, \quad
\gamma_{xz} = \frac{\tau_{xz}}{G}
$$

## Typical Stress-Strain Diagram

### For Ductile Materials (e.g., mild steel)

Key points on the stress-strain curve:

1. **Proportional Limit**: Maximum stress where Hooke's law applies
2. **Elastic Limit**: Maximum stress where material returns to original shape
3. **Yield Point**: Stress where permanent deformation begins
4. **Ultimate Strength**: Maximum stress the material can withstand
5. **Fracture Point**: Stress at which material fails

**Yield Strength** (engineering definition):

- 0.2% offset method for materials without clear yield point
- $\sigma_{y0.2}$ = stress corresponding to 0.2% permanent strain

### For Brittle Materials (e.g., concrete, cast iron)

- Linear relationship until fracture
- No significant plastic deformation
- Ultimate strength ≈ fracture strength
- Different behavior in tension vs. compression

## Working Stress and Safety Factors

### Allowable Stress

To ensure safe operation, actual stress must not exceed allowable stress:

$$
\sigma_{allow} = \frac{\sigma_{ultimate}}{SF}
$$

or

$$
\sigma_{allow} = \frac{\sigma_{yield}}{SF}
$$

where $SF$ is the **safety factor** (typically 1.5 to 4).

### Factor of Safety Selection

- **Life-critical applications**: SF = 3-4
- **Standard structural**: SF = 2-3
- **Temporary structures**: SF = 1.5-2

## Example Problems

### Example 1: Tensile Loading

A steel rod of diameter 20 mm and length 2 m is subjected to a tensile force of 50 kN.

**Given:**

- $d = 20$ mm, $L = 2$ m, $P = 50$ kN
- Steel: $E = 200$ GPa, $\nu = 0.3$

**Find:** Stress, axial strain, lateral strain, and elongation.

**Solution:**

**Cross-sectional area:**

$$
A = \frac{\pi d^2}{4} = \frac{\pi (0.02)^2}{4} = 3.14 \times 10^{-4} \text{ m}^2
$$

**Tensile stress:**

$$
\sigma = \frac{P}{A} = \frac{50 \times 10^3}{3.14 \times 10^{-4}} = 159.2 \text{ MPa}
$$

**Axial strain:**

$$
\epsilon_{axial} = \frac{\sigma}{E} = \frac{159.2 \times 10^6}{200 \times 10^9} = 7.96
\times 10^{-4}
$$

**Lateral strain:**

$$
\epsilon_{lateral} = -\nu \epsilon_{axial} = -0.3 \times 7.96 \times 10^{-4} = -2.39
\times 10^{-4}
$$

**Elongation:**

$$
\Delta L = \epsilon_{axial} \times L = 7.96 \times 10^{-4} \times 2 = 1.59 \text{ mm}
$$

### Example 2: Shear Loading

A bolt of diameter 12 mm is subjected to a shear force of 15 kN.

**Given:**

- $d = 12$ mm, $V = 15$ kN

**Find:** Shear stress.

**Solution:**

**Shear area:**

$$
A_{shear} = \frac{\pi d^2}{4} = \frac{\pi (0.012)^2}{4} = 1.13 \times 10^{-4}
\text{ m}^2
$$

**Shear stress:**

$$
\tau = \frac{V}{A_{shear}} = \frac{15 \times 10^3}{1.13 \times 10^{-4}} = 132.7
\text{ MPa}
$$

## Thermal Stress and Strain

### Thermal Strain

When temperature changes, materials expand or contract:

$$
\epsilon_{thermal} = \alpha \Delta T
$$

where:

- $\alpha$ = coefficient of thermal expansion (1/°C)
- $\Delta T$ = temperature change

**Common values:**

- Steel: $\alpha = 12 \times 10^{-6}$ /°C
- Aluminum: $\alpha = 23 \times 10^{-6}$ /°C
- Concrete: $\alpha = 10 \times 10^{-6}$ /°C

### Thermal Stress

If thermal expansion is constrained:

$$
\sigma_{thermal} = E \alpha \Delta T
$$

### Example 3: Thermal Stress

A steel beam is heated from 20°C to 80°C but is constrained from expanding.

**Given:**

- $\Delta T = 60^\circ\text{C}$
- Steel: $E = 200$ GPa, $\alpha = 12 \times 10^{-6}$ /°C

**Find:** Thermal stress.

**Solution:**

$$
\sigma_{thermal} = E \alpha \Delta T = 200 \times 10^9 \times 12 \times 10^{-6} \times
60 = 144 \text{ MPa}
$$

This is a significant compressive stress that could cause buckling or failure.

## Stress Concentration

Real components have geometric discontinuities that cause stress concentrations:

### Stress Concentration Factor

$$
K_t = \frac{\sigma_{max}}{\sigma_{nominal}}
$$

**Common sources:**

- Holes: $K_t = 2-3$
- Notches: $K_t = 1.5-5$
- Sharp corners: $K_t = 2-4$

### Design Considerations

- Use generous fillets at corners
- Avoid abrupt section changes
- Consider fatigue effects

## Applications in Engineering

### Structural Engineering

- **Building columns**: Compressive stress analysis
- **Bridge tension members**: Tensile stress calculations
- **Connection design**: Shear stress in bolts and welds

### Mechanical Engineering

- **Shaft design**: Torsional shear stress
- **Pressure vessels**: Hoop and longitudinal stress
- **Machine components**: Combined stress analysis

### Aerospace Engineering

- **Aircraft structures**: Weight optimization with stress limits
- **Spacecraft**: Thermal stress considerations
- **Turbine blades**: High-temperature stress analysis

## Advanced Topics

### Elastic Energy

Energy stored in a deformed elastic material:

$$
U = \frac{1}{2}\sigma\epsilon V = \frac{\sigma^2 V}{2E}
$$

where $V$ is the volume.

### Stress Transformation

For stress at different orientations:

$$
\sigma_x' = \frac{\sigma_x + \sigma_y}{2} + \frac{\sigma_x - \sigma_y}{2}\cos(2\theta) +
\tau_{xy}\sin(2\theta)
$$

### Principal Stresses

Maximum and minimum normal stresses:

$$
\sigma_{1,2} = \frac{\sigma_x + \sigma_y}{2} \pm
\sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}
$$

## Failure Theories

### Maximum Stress Theory

Failure occurs when maximum stress exceeds material strength:

$$
\sigma_{max} \leq \sigma_{allow}
$$

### Maximum Shear Stress Theory (Tresca)

$$
\tau_{max} = \frac{\sigma_1 - \sigma_3}{2} \leq \frac{\sigma_y}{2}
$$

### Distortion Energy Theory (von Mises)

$$
\sigma_{eq} = \sqrt{\frac{1}{2}[(\sigma_1-\sigma_2)^2 + (\sigma_2-\sigma_3)^2 + (\sigma_3-\sigma_1)^2]} \leq \sigma_y
$$

## Practical Design Guidelines

### Material Selection

- Consider service environment (temperature, corrosion)
- Match elastic modulus to stiffness requirements
- Balance strength vs. weight vs. cost

### Geometric Design

- Minimize stress concentrations
- Use appropriate safety factors
- Consider manufacturing tolerances

### Testing and Validation

- Perform material testing for critical applications
- Use finite element analysis for complex geometries
- Conduct prototype testing under realistic conditions

Understanding stress and strain is fundamental to:

- Safe structural design
- Efficient material utilization
- Failure prevention
- Performance optimization

These concepts form the foundation for more advanced topics in strength of materials, including beam bending, torsion, and combined loading scenarios.

## Exercises

**Exercise 1.** An aluminium rod ($E = 70$ GPa, $\nu = 0.33$) of diameter 25 mm carries a 40 kN compressive load. Find the axial stress, axial strain and change in diameter.

<details>
<summary>Answer</summary>

$A = 490.9$ mm², so $`\sigma = -40\,000/490.9 = -81.5`$ MPa and $\epsilon = \sigma/E = -1.164 \times 10^{-3}$.

The lateral strain is $+0.33 \times 1.164 \times 10^{-3} = 3.84 \times 10^{-4}$, so $\Delta d = 25 \times 3.84 \times 10^{-4} = +0.0096$ mm. The rod gets slightly fatter.

</details>

**Exercise 2.** Find the shear modulus of steel ($E = 200$ GPa, $\nu = 0.3$) and the shear strain produced by a shear stress of 100 MPa.

<details>
<summary>Answer</summary>

```math
G = \frac{E}{2(1 + \nu)} = \frac{200}{2.6} = 76.9 \text{ GPa}, \quad
\gamma = \frac{\tau}{G} = \frac{100}{76\,900} = 1.30 \times 10^{-3} \text{ rad}
```

</details>

**Exercise 3.** (a) The 12 mm bolt of Example 2 is placed in double shear (a clevis joint) with the same 15 kN load. What is the shear stress? (b) What bolt diameter is needed in single shear if the allowable shear stress is 100 MPa?

<details>
<summary>Answer</summary>

(a) Two shear planes share the load: $`\tau = 15\,000/(2 \times 113.1) = 66.3`$ MPa, half the single-shear value.

(b) $`d = \sqrt{4V/(\pi\tau_{allow})} = \sqrt{4 \times 15\,000/(\pi \times 100)} = 13.8`$ mm, so use a 14 mm bolt.

</details>

**Exercise 4.** A steel element ($E = 200$ GPa, $\nu = 0.3$) is loaded with $\sigma_x = 100$ MPa, $\sigma_y = -50$ MPa and $\sigma_z = 0$. Find the three normal strains and the volumetric strain.

<details>
<summary>Answer</summary>

```math
\epsilon_x = \frac{100 - 0.3(-50)}{200\,000} = 5.75 \times 10^{-4}, \quad
\epsilon_y = \frac{-50 - 0.3(100)}{200\,000} = -4.00 \times 10^{-4}
```

```math
\epsilon_z = \frac{0 - 0.3(100 - 50)}{200\,000} = -7.5 \times 10^{-5}
```

```math
\epsilon_v = \epsilon_x + \epsilon_y + \epsilon_z = 1.0 \times 10^{-4}
```

There is a strain in $z$ even though $\sigma_z = 0$, because of the Poisson effect.

</details>

**Exercise 5.** At a point, $\sigma_x = 60$ MPa, $\sigma_y = 20$ MPa and $\tau_{xy} = 25$ MPa (plane stress). Find the normal stress on the plane at $\theta = 45^\circ$, the principal stresses, and the safety factors against yield ($\sigma_y = 250$ MPa) by Tresca and von Mises.

<details>
<summary>Answer</summary>

$\sigma_{x'}(45^\circ) = 40 + 20\cos 90^\circ + 25\sin 90^\circ = 65$ MPa.

```math
\sigma_{1,2} = 40 \pm \sqrt{20^2 + 25^2} = 72.0,\ 8.0 \text{ MPa}, \quad \sigma_3 = 0
```

Tresca: $\tau_{max} = (\sigma_1 - \sigma_3)/2 = 36.0$ MPa, so $n = 125/36.0 = 3.47$.

von Mises:

```math
\sigma_{eq} = \sqrt{\tfrac{1}{2}\left[(72.0 - 8.0)^2 + 8.0^2 + 72.0^2\right]} = 68.4
\text{ MPa} \implies n = 3.66
```

</details>

## References

- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 8th ed., Cengage Learning, 2013.
