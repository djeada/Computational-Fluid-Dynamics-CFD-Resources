# Mechanical Properties of Materials

Understanding the mechanical properties of materials is essential for selecting appropriate materials in engineering design. These properties describe how a material responds to applied forces, temperature changes, and sustained loading over time.

## Tensile Testing and Stress-Strain Curves

### The Tensile Test

The uniaxial tensile test is the most common method for characterizing material behavior. A standardized specimen is pulled in tension at a controlled rate while measuring force and elongation.

**Engineering stress and strain:**
$$\sigma_{eng} = \frac{P}{A_0}, \quad \epsilon_{eng} = \frac{\Delta L}{L_0}$$

**True stress and strain:**
$$\sigma_{true} = \frac{P}{A_{inst}}, \quad \epsilon_{true} = \ln\left(\frac{L}{L_0}\right)$$

Relationship between engineering and true quantities (before necking):
$$\sigma_{true} = \sigma_{eng}(1 + \epsilon_{eng}), \quad \epsilon_{true} = \ln(1 + \epsilon_{eng})$$

### Key Points on the Stress-Strain Curve

1. **Proportional limit** — end of linear region
2. **Elastic limit** — maximum stress with full recovery
3. **Yield strength** ($\sigma_y$) — onset of permanent deformation
4. **Ultimate tensile strength** ($\sigma_u$) — peak engineering stress
5. **Fracture strength** ($\sigma_f$) — stress at rupture

## Elastic vs. Plastic Behavior

### Elastic Region

In the elastic region, deformation is fully recoverable upon unloading:
$$\sigma = E\epsilon$$

where $E$ is the elastic modulus (Young's modulus). The elastic modulus represents the stiffness of the material and is a measure of atomic bond strength.

**Elastic strain energy density (resilience per unit volume):**
$$u = \frac{1}{2}\sigma\epsilon = \frac{\sigma^2}{2E}$$

### Plastic Region

Beyond the yield point, permanent (plastic) deformation occurs. Key characteristics include:

- **Strain hardening**: stress increases with further plastic deformation
- **Necking**: localized reduction in cross-sectional area before fracture
- **Permanent set**: residual strain after unloading

**Strain hardening exponent** (power-law model):
$$\sigma_{true} = K \epsilon_{true}^n$$

where $K$ is the strength coefficient and $n$ is the strain hardening exponent. Typical values of $n$ range from 0.1 to 0.5.

### Yield Strength Determination

For materials without a clear yield point, the **0.2% offset method** is used:
1. Draw a line parallel to the elastic region, offset by $\epsilon = 0.002$
2. The intersection with the stress-strain curve defines $\sigma_{y(0.2\%)}$

## Ductile vs. Brittle Materials

### Ductile Materials

Ductile materials undergo significant plastic deformation before fracture. Examples include mild steel, aluminum alloys, and copper.

**Percent elongation:**
$$\% EL = \frac{L_f - L_0}{L_0} \times 100$$

**Percent reduction in area:**
$$\% RA = \frac{A_0 - A_f}{A_0} \times 100$$

A material with $\% EL > 5\%$ is generally considered ductile.

### Brittle Materials

Brittle materials fracture with little or no plastic deformation. Examples include cast iron, concrete, glass, and ceramics.

- Fracture occurs at or near the ultimate strength
- Much stronger in compression than in tension
- Sensitive to flaws and stress concentrations

## Hardness, Toughness, and Resilience

### Hardness

Hardness measures resistance to localized plastic deformation (indentation):

| Scale | Method | Typical Application |
|-------|--------|-------------------|
| Brinell (HB) | 10 mm steel ball | Castings, forgings |
| Rockwell (HRC) | Diamond cone | Hardened steels |
| Vickers (HV) | Diamond pyramid | Thin sections, coatings |

**Approximate relationship with tensile strength (for steels):**
$$\sigma_u \approx 3.45 \times HB \text{ (MPa)}$$

### Toughness

Toughness is the total energy absorbed per unit volume up to fracture, represented by the area under the entire stress-strain curve:

$$u_T = \int_0^{\epsilon_f} \sigma \, d\epsilon$$

**Approximate toughness for a ductile material:**
$$u_T \approx \frac{\sigma_y + \sigma_u}{2} \times \epsilon_f$$

**Impact toughness** is measured using the Charpy or Izod test and quantifies resistance to sudden loading.

### Resilience

Resilience is the energy absorbed per unit volume within the elastic region:
$$u_r = \frac{\sigma_y^2}{2E}$$

Materials with high resilience can absorb significant elastic energy — useful for springs and shock absorbers.

## Fatigue and Endurance Limit

### Fatigue Failure

Fatigue failure occurs under cyclic loading at stresses well below the ultimate strength. It accounts for approximately 90% of all mechanical failures in service.

**Stress amplitude and mean stress:**
$$\sigma_a = \frac{\sigma_{max} - \sigma_{min}}{2}, \quad \sigma_m = \frac{\sigma_{max} + \sigma_{min}}{2}$$

### S-N Curve

The S-N (stress–number of cycles) curve characterizes fatigue behavior. For ferrous metals, an **endurance limit** $\sigma_e$ exists below which the material can sustain an infinite number of cycles.

**Approximate endurance limit (steels):**
$$\sigma_e \approx 0.5\,\sigma_u \quad \text{for } \sigma_u \leq 1400 \text{ MPa}$$

### Modified Goodman Criterion

For combined alternating and mean stress:
$$\frac{\sigma_a}{\sigma_e} + \frac{\sigma_m}{\sigma_u} = 1$$

## Creep and Stress Relaxation

### Creep

Creep is the time-dependent deformation under sustained constant stress, significant at elevated temperatures (typically $T > 0.4\,T_m$ where $T_m$ is the melting point in Kelvin).

**Three stages of creep:**
1. **Primary creep** — decreasing strain rate
2. **Secondary (steady-state) creep** — constant strain rate $\dot{\epsilon}_s$
3. **Tertiary creep** — accelerating strain rate leading to rupture

**Steady-state creep rate (Arrhenius model):**
$$\dot{\epsilon}_s = A \sigma^n e^{-Q/(RT)}$$

where $A$ is a material constant, $n$ is the stress exponent, $Q$ is the activation energy, $R$ is the gas constant, and $T$ is absolute temperature.

### Stress Relaxation

Stress relaxation is the decrease in stress over time under constant strain, important for bolted joints and seals:
$$\sigma(t) = \sigma_0 \, e^{-t/\tau}$$

where $\tau$ is the relaxation time constant.

## Material Selection Criteria

### Performance Indices

Material selection often involves optimizing a **performance index** that combines multiple properties:

| Design Goal | Performance Index |
|-------------|------------------|
| Light, stiff tie rod | $E / \rho$ |
| Light, stiff beam | $E^{1/2} / \rho$ |
| Light, strong tie rod | $\sigma_y / \rho$ |
| Light, strong beam | $\sigma_y^{2/3} / \rho$ |

where $\rho$ is the material density.

### Typical Material Properties

| Material | $E$ (GPa) | $\sigma_y$ (MPa) | $\sigma_u$ (MPa) | $\rho$ (kg/m³) |
|----------|-----------|-----------------|-----------------|----------------|
| Mild steel | 200 | 250 | 400 | 7850 |
| Aluminum 6061-T6 | 69 | 276 | 310 | 2700 |
| Titanium Ti-6Al-4V | 114 | 880 | 950 | 4430 |
| CFRP (unidirectional) | 140 | — | 1500 | 1600 |

## Example Problems

### Example 1: Tensile Test Analysis

A tensile test on a steel specimen ($d_0 = 12.5$ mm, $L_0 = 50$ mm) yields the following data: yield load $P_y = 38$ kN, maximum load $P_u = 58$ kN, fracture length $L_f = 63$ mm, fracture diameter $d_f = 8.5$ mm.

**Given:**
- $d_0 = 12.5$ mm, $L_0 = 50$ mm
- $P_y = 38$ kN, $P_u = 58$ kN
- $L_f = 63$ mm, $d_f = 8.5$ mm

**Find:** Yield strength, ultimate tensile strength, percent elongation, percent reduction in area.

**Solution:**

$$A_0 = \frac{\pi (12.5)^2}{4} = 122.7 \text{ mm}^2$$

$$\sigma_y = \frac{P_y}{A_0} = \frac{38\,000}{122.7} = 309.7 \text{ MPa}$$

$$\sigma_u = \frac{P_u}{A_0} = \frac{58\,000}{122.7} = 472.7 \text{ MPa}$$

$$\% EL = \frac{63 - 50}{50} \times 100 = 26\%$$

$$\% RA = \frac{122.7 - 56.7}{122.7} \times 100 = 53.8\%$$

The material is ductile ($\% EL > 5\%$) with good strength and formability.

### Example 2: Fatigue Life Assessment

A steel shaft ($\sigma_u = 600$ MPa) is subjected to reversed bending with $\sigma_a = 250$ MPa and $\sigma_m = 100$ MPa.

**Given:**
- $\sigma_u = 600$ MPa, $\sigma_e \approx 0.5 \times 600 = 300$ MPa
- $\sigma_a = 250$ MPa, $\sigma_m = 100$ MPa

**Find:** Whether the shaft will have infinite fatigue life using the Goodman criterion.

**Solution:**

$$\frac{\sigma_a}{\sigma_e} + \frac{\sigma_m}{\sigma_u} = \frac{250}{300} + \frac{100}{600} = 0.833 + 0.167 = 1.0$$

The sum equals 1.0, indicating the shaft is exactly at the fatigue limit — it is on the boundary of safe design and should be redesigned with a larger cross-section or better surface finish.

## Practical Tips

- Always verify material properties from certified test reports for critical applications
- Account for temperature effects on material strength, especially above $0.3\,T_m$
- Surface finish significantly affects fatigue life — polished surfaces resist fatigue better
- Ductile materials are generally preferred for structures subject to impact or vibration
- Use appropriate safety factors to account for material variability and loading uncertainty

Understanding mechanical properties enables engineers to select materials that meet performance requirements while optimizing weight, cost, and manufacturability.
