# Bearings and Lubrication

Bearings are machine elements that support relative motion between components while minimizing friction and wear. Combined with proper lubrication, bearings enable the reliable, efficient operation of virtually all rotating and sliding machinery.

## Types of Bearings

### Rolling Element Bearings

Rolling element bearings use balls or rollers to maintain separation between moving parts, converting sliding friction into much lower rolling friction.

#### Ball Bearings

- **Deep groove ball bearings**: Most common type, handles radial and moderate axial loads
- **Angular contact ball bearings**: Designed for combined radial and axial loads, contact angle typically 15°–40°
- **Self-aligning ball bearings**: Accommodate shaft misalignment up to 2.5°
- **Thrust ball bearings**: Handle purely axial loads

#### Roller Bearings

- **Cylindrical roller bearings**: High radial load capacity, permit axial sliding
- **Needle roller bearings**: Compact design for high radial loads in limited space
- **Spherical roller bearings**: High load capacity with self-aligning capability

#### Tapered Roller Bearings

- Handle combined radial and axial loads
- Contact angle determines axial-to-radial load ratio
- Typically used in pairs (face-to-face or back-to-back)
- **Applications**: Wheel bearings, gearbox shafts, heavy machinery

### Journal Bearings (Sliding Bearings)

Journal bearings support a rotating shaft within a cylindrical sleeve. The shaft and bearing are separated by a thin film of lubricant.

**Advantages over rolling bearings:**

- Higher load capacity for a given size
- Quieter operation at high speeds
- Simpler construction, longer life under ideal conditions
- Better suited for very high speeds and shock loads

## Bearing Loads and Life

### L10 Life Equation

The basic rating life is the number of revolutions at which 90% of a group of identical bearings will still be operational:

$$
L_{10} = \left(\frac{C}{P}\right)^p
$$

where:

- $L_{10}$ = basic rating life in millions of revolutions
- $C$ = basic dynamic load rating (from manufacturer catalog)
- $P$ = equivalent dynamic bearing load
- $p$ = life exponent: 3 for ball bearings, 10/3 for roller bearings

### Life in Hours

$$
L_{10h} = \frac{L_{10} \times 10^6}{60 \cdot n}
$$

where $n$ is the rotational speed in rpm.

### Adjusted Rating Life

The modified life equation accounts for reliability, material, and lubrication:

$$
L_{na} = a_1 \cdot a_{SKF} \cdot L_{10}
$$

where:

- $a_1$ = life adjustment factor for reliability (1.0 for 90%, 0.62 for 95%, 0.53 for 96%)
- $a_{SKF}$ = combined factor for lubrication, contamination, and fatigue load limit

## Static and Dynamic Load Ratings

### Dynamic Load Rating ($C$)

The constant radial load under which a bearing achieves a basic rating life of one million revolutions. Represents the bearing's capacity under rotating conditions.

### Static Load Rating ($C_0$)

The static load that produces a total permanent deformation of the rolling element and raceway of $0.0001d$ at the most heavily loaded contact:

$$
C_0 = f_0 \cdot i \cdot Z \cdot D_w^2 \quad \text{(ball bearings)}
$$

where $f_0$ is a geometry factor, $i$ is the number of rows, $Z$ is the number of balls, and $D_w$ is the ball diameter.

### Equivalent Dynamic Load

For combined radial ($F_r$) and axial ($F_a$) loads:

$$
P = X F_r + Y F_a
$$

where $X$ and $Y$ are radial and axial load factors from bearing catalogs, dependent on the ratio $F_a / F_r$ and the bearing geometry.

## Bearing Selection Process

1. **Determine loads**: Radial and axial forces on the bearing from shaft analysis
2. **Calculate equivalent load** $P$ from combined loading
3. **Specify required life** $L_{10h}$ based on application (e.g., 20,000 h for industrial machines)
4. **Calculate required dynamic load rating**:

$$
C = P \left(\frac{60 \cdot n \cdot L_{10h}}{10^6}\right)^{1/p}
$$

5. **Select bearing** from catalog with $C \geq C_{required}$
6. **Verify static safety**: Check $C_0 / P_0 \geq s_0$ (safety factor)
7. **Check speed rating**: Ensure operating speed is within bearing limits

## Lubrication Fundamentals

### Viscosity

**Dynamic viscosity** ($\mu$): Resistance to shear flow

$$
\tau = \mu \frac{du}{dy}
$$

**Kinematic viscosity** ($\nu$): Dynamic viscosity divided by density

$$
\nu = \frac{\mu}{\rho}
$$

Viscosity decreases with temperature. The **viscosity index** (VI) characterizes this dependence — higher VI means less variation with temperature.

### Reynolds Equation

The Reynolds equation governs pressure distribution in thin lubricant films:

$$
\frac{\partial}{\partial x}\left(h^3 \frac{\partial p}{\partial x}\right) +
\frac{\partial}{\partial z}\left(h^3 \frac{\partial p}{\partial z}\right) = 6\mu U
\frac{\partial h}{\partial x}
$$

where:

- $h$ = film thickness
- $p$ = pressure
- $\mu$ = dynamic viscosity
- $U$ = surface velocity

This is the foundation of hydrodynamic lubrication theory.

## Hydrodynamic Lubrication (Journal Bearings)

### Sommerfeld Number

The Sommerfeld number is the key dimensionless parameter for journal bearing design:

$$
S = \frac{\mu N_s}{P}\left(\frac{R}{c}\right)^2
$$

where:

- $\mu$ = dynamic viscosity
- $N_s$ = rotational speed (rev/s)
- $P = W / (L \cdot d)$ = bearing pressure
- $R$ = journal radius
- $c$ = radial clearance

### Minimum Film Thickness

The eccentricity ratio $\varepsilon = e/c$ determines the minimum film thickness:

$$
h_{min} = c(1 - \varepsilon)
$$

where $e$ is the eccentricity (offset of journal center from bearing center). A safe design typically requires $h_{min} \geq 3R_a$ where $R_a$ is the combined surface roughness.

### Petroff's Equation

For a lightly loaded journal bearing (concentric operation), the friction coefficient is:

$$
f = 2\pi^2 \frac{\mu N_s}{P} \frac{R}{c}
$$

### Power Loss

$$
P_{loss} = f \cdot W \cdot v = f \cdot W \cdot \pi d N_s
$$

## Elastohydrodynamic Lubrication (EHL)

EHL occurs in non-conformal contacts such as rolling element bearings and gears, where very high local pressures cause elastic deformation of the surfaces.

### Characteristics

- Contact pressures of 0.5–3 GPa
- Film thickness of 0.1–1.0 μm
- Lubricant viscosity increases dramatically under pressure (piezo-viscous effect)

### Minimum Film Thickness (Hamrock-Dowson)

For elliptical contacts:

$$
h_{min} = 3.63 R_x U^{0.68} G^{0.49} W_e^{-0.073}(1 - e^{-0.68k})
$$

where:

- $U = \mu_0 u / (E' R_x)$ = speed parameter
- $G = \alpha E'$ = materials parameter
- $W_e = W / (E' R_x^2)$ = load parameter
- $k$ = ellipticity ratio

### Lubrication Regimes

The **lambda ratio** determines the lubrication regime:

$$
\Lambda = \frac{h_{min}}{\sqrt{R_{q1}^2 + R_{q2}^2}}
$$

- $\Lambda > 3$: Full film lubrication (no asperity contact)
- $1 < \Lambda < 3$: Mixed lubrication (partial contact)
- $\Lambda < 1$: Boundary lubrication (significant contact)

## Worked Examples

### Example 1: Bearing Life Calculation

**Given:** A deep groove ball bearing (6208) with $C = 29.1$ kN and $C_0 = 17.8$ kN supports a radial load of 5 kN and an axial load of 2 kN at 1800 rpm.

**Find:** The L10 life in hours.

**Solution:**

Load ratio: $F_a / F_r = 2/5 = 0.4$

From bearing tables for this ratio, $X = 0.56$ and $Y = 1.45$:

$$
P = X F_r + Y F_a = 0.56 \times 5 + 1.45 \times 2 = 5.7 \text{ kN}
$$

Basic rating life:

$$
L_{10} = \left(\frac{C}{P}\right)^3 = \left(\frac{29.1}{5.7}\right)^3 = 133.2
\text{ million revolutions}
$$

Life in hours:

$$
L_{10h} = \frac{133.2 \times 10^6}{60 \times 1800} = 1233 \text{ hours}
$$

### Example 2: Journal Bearing Design

**Given:** A journal bearing supports a shaft of diameter $d = 80$ mm rotating at 1200 rpm. Bearing length $L = 80$ mm, radial clearance $c = 0.06$ mm, load $W = 10$ kN, lubricant viscosity $\mu = 0.025$ Pa·s.

**Find:** Sommerfeld number and minimum film thickness.

**Solution:**

Bearing pressure:

$$
P = \frac{W}{L \cdot d} = \frac{10000}{0.080 \times 0.080} = 1.5625 \text{ MPa}
$$

Rotational speed: $N_s = 1200/60 = 20$ rev/s

Sommerfeld number:

$$
S = \frac{0.025 \times 20}{1.5625 \times 10^6}\left(\frac{40}{0.06}\right)^2 = 0.1422
$$

From Raimondi-Boyd charts for $L/d = 1$ and $S = 0.1422$, the eccentricity ratio $\varepsilon \approx 0.62$.

Minimum film thickness:

$$
h_{min} = c(1 - \varepsilon) = 0.06(1 - 0.62) = 0.0228 \text{ mm} = 22.8\ \mu \text{m}
$$

## Applications

### Automotive

- **Wheel bearings**: Tapered roller or angular contact ball bearings
- **Engine bearings**: Crankshaft and camshaft journal bearings
- **Transmission bearings**: Tapered roller bearings for gear shaft support

### Industrial Machinery

- **Electric motors**: Deep groove ball bearings
- **Pumps and compressors**: Cylindrical and spherical roller bearings
- **Paper mills**: Self-aligning spherical roller bearings for large rolls

### Aerospace

- **Gas turbine engines**: Angular contact ball bearings and cylindrical roller bearings operating at extreme speeds
- **Control surface actuators**: Needle roller and spherical plain bearings
- **Landing gear**: High-load spherical plain bearings

A thorough understanding of bearing types, life prediction, and lubrication theory is essential for designing reliable mechanical systems that meet performance and durability requirements.

## Exercises

**Exercise 1.** The life exponent in $L_{10} = (C/P)^p$ is $p = 3$ for ball bearings and $p = 10/3$ for roller bearings. By what factor does the $L_{10}$ life change when the equivalent load $P$ is doubled, for each type? What does this imply for load estimates during bearing selection?

<details>
<summary>Answer</summary>

Since $L_{10} \propto P^{-p}$:

- Ball bearing: $2^{-3} = 1/8$, so the life drops to 12.5%.
- Roller bearing: $2^{-10/3} = 1/10.08$, so the life drops to about 9.9%.

Life is very sensitive to load. Underestimating the load (ignoring shock, misalignment or preload) costs a large fraction of the life, which is why application load factors are applied before selection. The converse also holds: a slightly larger bearing buys a lot of extra life.

</details>

**Exercise 2.** A deep groove ball bearing carries an equivalent load $P = 3.5$ kN at $n = 1450$ rpm and must reach $L_{10h} = 20\,000$ h. (a) Find the required basic dynamic load rating $C$. (b) The reliability requirement is raised to 96% ($a_1 = 0.53$, take $a_{SKF} = 1$). What rating is needed now?

<details>
<summary>Answer</summary>

(a) Required life in revolutions:

$$
L_{10} = \frac{60 \cdot n \cdot L_{10h}}{10^6} = \frac{60 \times 1450 \times 20\,000}{10^6} = 1740 \text{ million rev}
$$

$$
C = P\, L_{10}^{1/3} = 3.5 \times 1740^{1/3} = 3.5 \times 12.03 = 42.1 \text{ kN}
$$

(b) Now $a_1 L_{10} \geq 1740$, so $L_{10} \geq 1740/0.53 = 3283$ million rev:

$$
C = 3.5 \times 3283^{1/3} = 52.0 \text{ kN}
$$

Raising reliability from 90% to 96% needs a 24% higher load rating.

</details>

**Exercise 3.** The 6208 bearing of Example 1 ($C = 29.1$ kN) runs at 1800 rpm. What is the largest equivalent dynamic load it can carry if it must reach $L_{10h} = 20\,000$ h?

<details>
<summary>Answer</summary>

$$
L_{10} = \frac{60 \times 1800 \times 20\,000}{10^6} = 2160 \text{ million rev}
$$

$$
P_{max} = \frac{C}{L_{10}^{1/3}} = \frac{29.1}{2160^{1/3}} = \frac{29.1}{12.93} = 2.25
\text{ kN}
$$

The load of 5.7 kN in Example 1 is about 2.5 times this, which is why that bearing reaches only about 1230 h.

</details>

**Exercise 4.** Use Petroff's equation to estimate the friction coefficient, friction torque and power loss of the journal bearing in Example 2 ($d = 80$ mm, $L = 80$ mm, $c = 0.06$ mm, $W = 10$ kN, $\mu = 0.025$ Pa·s, 1200 rpm). Why is the result only a first estimate for this bearing?

<details>
<summary>Answer</summary>

With $P = 1.5625$ MPa, $N_s = 20$ rev/s and $R/c = 40/0.06 = 666.7$:

$$
f = 2\pi^2 \frac{\mu N_s}{P} \frac{R}{c} = 2\pi^2 \times
\frac{0.025 \times 20}{1.5625 \times 10^6} \times 666.7 = 4.21 \times 10^{-3}
$$

Friction torque: $T_f = f W R = 4.21 \times 10^{-3} \times 10\,000 \times 0.040 = 1.68$ N·m.

Power loss:

$$
P_{loss} = f W \pi d N_s = 4.21 \times 10^{-3} \times 10\,000 \times \pi \times 0.080
\times 20 = 212 \text{ W}
$$

Petroff's equation assumes a concentric (lightly loaded) journal. With $S \approx 0.14$ this journal runs well off-centre, so design values of friction and temperature rise should come from the Raimondi–Boyd charts.

</details>

**Exercise 5.** For a rolling contact the Hamrock–Dowson formula gives $h_{min} = 0.35$ μm. The RMS roughnesses are $R_{q1} = 0.10$ μm and $R_{q2} = 0.15$ μm. (a) Which lubrication regime applies? (b) What composite roughness gives full-film lubrication, and what RMS roughness per surface if both surfaces are finished equally?

<details>
<summary>Answer</summary>

(a)

$$
\Lambda = \frac{0.35}{\sqrt{0.10^2 + 0.15^2}} = \frac{0.35}{0.180} = 1.94
$$

Since $1 < \Lambda < 3$, the contact runs in mixed lubrication.

(b) For $\Lambda = 3$ the composite roughness must be at most $0.35/3 = 0.117$ μm. With equal surfaces, $\sqrt{2}\,R_q = 0.117$ μm, so $R_q = 0.083$ μm. The other route is to raise $h_{min}$, for example with a more viscous oil, since $h_{min} \propto U^{0.68}$.

</details>

## References

- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 10th ed., McGraw-Hill Education, 2015.
- Hamrock, B. J., Schmid, S. R., and Jacobson, B. O., *Fundamentals of Fluid Film Lubrication*, 2nd ed., Marcel Dekker, 2004.
- Raimondi, A. A., and Boyd, J., "A solution for the finite journal bearing and its application to analysis and design", Parts I–III, *ASLE Transactions* 1(1), 1958.
- ISO 281:2007, *Rolling bearings — Dynamic load ratings and rating life*, International Organization for Standardization, 2007.
