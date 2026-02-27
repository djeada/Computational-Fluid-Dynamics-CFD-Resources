# Gears and Transmissions

Gears are toothed machine elements that transmit rotary motion and power between shafts. They provide precise speed ratios, high efficiency, and reliable power transmission, making them indispensable in nearly every mechanical system from wristwatches to wind turbines.

## Gear Fundamentals

### Terminology and Geometry

**Pitch circle**: The theoretical circle on which gear calculations are based. Two meshing gears have pitch circles that are tangent to each other.

**Key parameters:**
- **Module** ($m$): Ratio of pitch diameter to number of teeth
$$m = \frac{d}{N}$$
- **Circular pitch** ($p_c$): Arc distance between adjacent teeth on the pitch circle
$$p_c = \pi m$$
- **Diametral pitch** ($P_d$): Number of teeth per unit pitch diameter (Imperial)
$$P_d = \frac{N}{d} = \frac{1}{m}$$
- **Pressure angle** ($\phi$): Angle between the line of action and the tangent to the pitch circle, typically 20° or 25°
- **Addendum** ($a$): Radial distance from pitch circle to tooth tip, $a = m$
- **Dedendum** ($b$): Radial distance from pitch circle to tooth root, $b = 1.25m$

### Fundamental Law of Gearing

For a constant angular velocity ratio, the common normal to the tooth profiles at the contact point must always pass through a fixed point on the line of centers:

$$\frac{\omega_1}{\omega_2} = \frac{N_2}{N_1} = \frac{d_2}{d_1}$$

The **involute tooth profile** satisfies this requirement for all contact positions, making it the standard profile for modern gears.

### Contact Ratio

The contact ratio ensures smooth power transmission by having more than one pair of teeth in contact:

$$CR = \frac{\sqrt{r_{a1}^2 - r_{b1}^2} + \sqrt{r_{a2}^2 - r_{b2}^2} - C\sin\phi}{\pi m \cos\phi}$$

where $r_a$ is the addendum radius, $r_b$ is the base circle radius, and $C$ is the center distance. A minimum contact ratio of 1.2 is recommended.

## Spur Gear Geometry and Kinematics

Spur gears have straight teeth parallel to the shaft axis and transmit power between parallel shafts.

### Gear Ratio

$$i = \frac{\omega_1}{\omega_2} = \frac{N_2}{N_1} = \frac{d_2}{d_1}$$

### Center Distance

$$C = \frac{d_1 + d_2}{2} = \frac{m(N_1 + N_2)}{2}$$

### Transmitted Power

$$P = T\omega = F_t \cdot v$$

where $v = \frac{\pi d N_{rpm}}{60}$ is the pitch line velocity.

## Gear Tooth Forces

### Spur Gear Forces

The resultant force acts along the line of action at the pressure angle $\phi$:

**Tangential force** (transmits power):
$$F_t = \frac{2T}{d} = \frac{P}{v}$$

**Radial force** (separating force):
$$F_r = F_t \tan\phi$$

**Resultant force**:
$$F = \frac{F_t}{\cos\phi}$$

### Helical Gear Forces

For helical gears with helix angle $\psi$:

$$F_t = \frac{2T}{d}$$

$$F_r = \frac{F_t \tan\phi_n}{\cos\psi}$$

$$F_a = F_t \tan\psi$$

where $\phi_n$ is the normal pressure angle and $F_a$ is the axial thrust force.

## Helical Gears

Helical gears have teeth cut at an angle to the shaft axis, providing smoother and quieter operation than spur gears.

### Key Relationships

**Normal module**: $m_n = m_t \cos\psi$

**Normal pressure angle**: $\tan\phi_n = \tan\phi_t \cos\psi$

**Virtual number of teeth** (for strength calculations):
$$N_v = \frac{N}{\cos^3\psi}$$

### Advantages Over Spur Gears
- Gradual tooth engagement reduces noise and vibration
- Higher contact ratio for smoother operation
- Greater load-carrying capacity

### Disadvantage
- Axial thrust forces require thrust bearings
- Double helical (herringbone) gears eliminate axial thrust

## Bevel Gears

Bevel gears transmit power between intersecting shafts, typically at 90°.

### Geometry

The pitch surfaces are cones rather than cylinders. For a shaft angle $\Sigma$:

$$\tan\gamma_1 = \frac{\sin\Sigma}{i + \cos\Sigma}, \quad \tan\gamma_2 = \frac{\sin\Sigma}{1/i + \cos\Sigma}$$

where $\gamma_1$ and $\gamma_2$ are the pitch cone angles.

### Forces on Bevel Gear Teeth

$$F_t = \frac{2T}{d_m}$$

$$F_r = F_t \tan\phi \cos\gamma$$

$$F_a = F_t \tan\phi \sin\gamma$$

where $d_m$ is the mean pitch diameter.

## Worm Gears

Worm gears provide high reduction ratios in a compact package. The worm resembles a screw thread that meshes with a helical gear (worm wheel).

### Gear Ratio

$$i = \frac{N_w}{N_g}$$

where $N_w$ is the number of starts on the worm (typically 1–4) and $N_g$ is the number of teeth on the worm wheel.

### Efficiency

$$\eta = \frac{\tan\lambda}{\tan(\lambda + \phi_f)}$$

where $\lambda$ is the lead angle and $\phi_f$ is the friction angle. Worm gears are often **self-locking** when $\lambda < \phi_f$, preventing back-driving.

## Gear Trains

### Simple Gear Train

Each shaft carries one gear. The overall ratio is:

$$i = \frac{\omega_{in}}{\omega_{out}} = (-1)^n \frac{N_{last}}{N_{first}}$$

where $n$ is the number of external mesh pairs. Intermediate (idler) gears change direction but not ratio.

### Compound Gear Train

Multiple gears share a shaft, enabling large ratios in compact space:

$$i = \frac{N_2}{N_1} \cdot \frac{N_4}{N_3} \cdot \frac{N_6}{N_5} \cdots$$

### Planetary (Epicyclic) Gear Trains

**Components**: Sun gear ($s$), planet gears ($p$), ring gear ($r$), carrier ($c$).

**Willis equation** (using tabular method):

$$\frac{\omega_r - \omega_c}{\omega_s - \omega_c} = -\frac{N_s}{N_r}$$

**Tooth constraint**: $N_r = N_s + 2N_p$

Common configurations:
- **Fixed ring**: $i = 1 + N_r/N_s$ (input: sun, output: carrier)
- **Fixed carrier**: $i = -N_r/N_s$ (input: sun, output: ring)
- **Fixed sun**: $i = 1 + N_s/N_r$ (input: ring, output: carrier)

## Transmission Design and Gear Ratio Selection

### Design Considerations
- **Required speed range and torque**: Determines overall ratio
- **Efficiency targets**: Each gear stage has 96–99% efficiency
- **Noise and vibration limits**: Influence gear type and quality
- **Size and weight constraints**: Favor planetary designs for compactness
- **Manufacturing cost**: Spur gears are cheapest to produce

### Multi-Stage Ratio Splitting

For a total ratio $i_{total}$ split across $n$ stages, an approximately equal split per stage minimizes total gear size:

$$i_{stage} \approx i_{total}^{1/n}$$

## Worked Examples

### Example 1: Spur Gear Forces

**Given:** A spur gear pair transmits 15 kW at 1500 rpm. The pinion has 20 teeth, the gear has 60 teeth, and the module is 4 mm. Pressure angle is 20°.

**Find:** Tangential, radial, and resultant tooth forces.

**Solution:**

Pitch diameter of pinion: $d_1 = mN_1 = 4 \times 20 = 80$ mm

Pitch line velocity:
$$v = \frac{\pi d_1 n}{60} = \frac{\pi \times 0.080 \times 1500}{60} = 6.28 \text{ m/s}$$

Tangential force:
$$F_t = \frac{P}{v} = \frac{15000}{6.28} = 2389 \text{ N}$$

Radial force:
$$F_r = F_t \tan\phi = 2389 \times \tan 20° = 870 \text{ N}$$

Resultant force:
$$F = \frac{F_t}{\cos\phi} = \frac{2389}{\cos 20°} = 2542 \text{ N}$$

### Example 2: Planetary Gear Ratio

**Given:** A planetary gearbox has a sun gear with 24 teeth, planet gears with 18 teeth, and a ring gear with 60 teeth. The ring is fixed. The sun gear rotates at 3000 rpm.

**Find:** Carrier speed and gear ratio.

**Solution:**

Verify tooth constraint: $N_r = N_s + 2N_p \Rightarrow 60 = 24 + 2(18) = 60$ ✓

Using the Willis equation with $\omega_r = 0$:
$$\frac{0 - \omega_c}{\omega_s - \omega_c} = -\frac{N_s}{N_r} = -\frac{24}{60}$$

$$-\omega_c = -\frac{24}{60}(\omega_s - \omega_c)$$

$$-\omega_c = -0.4\omega_s + 0.4\omega_c$$

$$\omega_c = \frac{0.4}{1.4}\omega_s = \frac{2}{7}\omega_s$$

$$\omega_c = \frac{2}{7} \times 3000 = 857.1 \text{ rpm}$$

Gear ratio: $i = \omega_s / \omega_c = 3.5$

## Applications

### Automotive
- **Manual transmissions**: Helical gear pairs for each speed
- **Automatic transmissions**: Planetary gear sets with clutches and brakes
- **Differentials**: Bevel gear systems for torque splitting

### Industrial Machinery
- **Speed reducers**: Worm and helical gear units
- **Machine tools**: Precision gear trains for feed drives
- **Conveyor systems**: Helical gear motors

### Aerospace
- **Turbofan engines**: Planetary gearboxes for fan speed reduction
- **Helicopter rotors**: Multi-stage epicyclic transmissions
- **Actuators**: Worm gear drives for flap and slat mechanisms

Gears remain the most efficient and reliable means of mechanical power transmission, and a thorough understanding of gear theory is essential for any mechanical engineer working with rotating machinery.
