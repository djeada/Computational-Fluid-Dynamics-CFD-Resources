# Gears and Transmissions

Gears are toothed machine elements that transmit rotary motion and power between shafts. They provide precise speed ratios, high efficiency, and reliable power transmission, making them indispensable in nearly every mechanical system from wristwatches to wind turbines.

## Gear Fundamentals

### Terminology and Geometry

**Pitch circle**: The theoretical circle on which gear calculations are based. Two meshing gears have pitch circles that are tangent to each other.

**Key parameters:**

- **Module** ($m$): Ratio of pitch diameter to number of teeth

$$
m = \frac{d}{N}
$$

- **Circular pitch** ($p_c$): Arc distance between adjacent teeth on the pitch circle

$$
p_c = \pi m
$$

- **Diametral pitch** ($P_d$): Number of teeth per unit pitch diameter (Imperial)

$$
P_d = \frac{N}{d} = \frac{1}{m}
$$

- **Pressure angle** ($\phi$): Angle between the line of action and the tangent to the pitch circle, typically 20° or 25°
- **Addendum** ($a$): Radial distance from pitch circle to tooth tip, $a = m$
- **Dedendum** ($b$): Radial distance from pitch circle to tooth root, $b = 1.25m$

### Fundamental Law of Gearing

For a constant angular velocity ratio, the common normal to the tooth profiles at the contact point must always pass through a fixed point on the line of centers:

$$
\frac{\omega_1}{\omega_2} = \frac{N_2}{N_1} = \frac{d_2}{d_1}
$$

The **involute tooth profile** satisfies this requirement for all contact positions, making it the standard profile for modern gears.

### Contact Ratio

The contact ratio ensures smooth power transmission by having more than one pair of teeth in contact:

$$
CR = \frac{\sqrt{r_{a1}^2 - r_{b1}^2} + \sqrt{r_{a2}^2 - r_{b2}^2} - C\sin\phi}{\pi m \cos\phi}
$$

where $r_a$ is the addendum radius, $r_b$ is the base circle radius, and $C$ is the center distance. A minimum contact ratio of 1.2 is recommended.

## Spur Gear Geometry and Kinematics

Spur gears have straight teeth parallel to the shaft axis and transmit power between parallel shafts.

### Gear Ratio

$$
i = \frac{\omega_1}{\omega_2} = \frac{N_2}{N_1} = \frac{d_2}{d_1}
$$

### Center Distance

$$
C = \frac{d_1 + d_2}{2} = \frac{m(N_1 + N_2)}{2}
$$

### Transmitted Power

$$
P = T\omega = F_t \cdot v
$$

where $v = \frac{\pi d N_{rpm}}{60}$ is the pitch line velocity.

## Gear Tooth Forces

### Spur Gear Forces

The resultant force acts along the line of action at the pressure angle $\phi$:

**Tangential force** (transmits power):

$$
F_t = \frac{2T}{d} = \frac{P}{v}
$$

**Radial force** (separating force):

$$
F_r = F_t \tan\phi
$$

**Resultant force**:

$$
F = \frac{F_t}{\cos\phi}
$$

### Helical Gear Forces

For helical gears with helix angle $\psi$:

$$
F_t = \frac{2T}{d}
$$

$$
F_r = \frac{F_t \tan\phi_n}{\cos\psi}
$$

$$
F_a = F_t \tan\psi
$$

where $\phi_n$ is the normal pressure angle and $F_a$ is the axial thrust force.

## Helical Gears

Helical gears have teeth cut at an angle to the shaft axis, providing smoother and quieter operation than spur gears.

### Key Relationships

**Normal module**: $m_n = m_t \cos\psi$

**Normal pressure angle**: $\tan\phi_n = \tan\phi_t \cos\psi$

**Virtual number of teeth** (for strength calculations):

$$
N_v = \frac{N}{\cos^3\psi}
$$

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

$$
\tan\gamma_1 = \frac{\sin\Sigma}{i + \cos\Sigma}, \quad
\tan\gamma_2 = \frac{\sin\Sigma}{1/i + \cos\Sigma}
$$

where $\gamma_1$ and $\gamma_2$ are the pitch cone angles.

### Forces on Bevel Gear Teeth

$$
F_t = \frac{2T}{d_m}
$$

$$
F_r = F_t \tan\phi \cos\gamma
$$

$$
F_a = F_t \tan\phi \sin\gamma
$$

where $d_m$ is the mean pitch diameter.

## Worm Gears

Worm gears provide high reduction ratios in a compact package. The worm resembles a screw thread that meshes with a helical gear (worm wheel).

### Gear Ratio

$$
i = \frac{\omega_{worm}}{\omega_{wheel}} = \frac{N_g}{N_w}
$$

where $N_w$ is the number of starts on the worm (typically 1–4) and $N_g$ is the number of teeth on the worm wheel.

### Efficiency

$$
\eta = \frac{\tan\lambda}{\tan(\lambda + \phi_f)}
$$

where $\lambda$ is the lead angle and $\phi_f$ is the friction angle. Worm gears are often **self-locking** when $\lambda < \phi_f$, preventing back-driving.

## Gear Trains

### Simple Gear Train

Each shaft carries one gear. The overall ratio is:

$$
i = \frac{\omega_{in}}{\omega_{out}} = (-1)^n \frac{N_{last}}{N_{first}}
$$

where $n$ is the number of external mesh pairs. Intermediate (idler) gears change direction but not ratio.

### Compound Gear Train

Multiple gears share a shaft, enabling large ratios in compact space:

$$
i = \frac{N_2}{N_1} \cdot \frac{N_4}{N_3} \cdot \frac{N_6}{N_5} \cdots
$$

### Planetary (Epicyclic) Gear Trains

**Components**: Sun gear ($s$), planet gears ($p$), ring gear ($r$), carrier ($c$).

**Willis equation** (using tabular method):

$$
\frac{\omega_r - \omega_c}{\omega_s - \omega_c} = -\frac{N_s}{N_r}
$$

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

$$
i_{stage} \approx i_{total}^{1/n}
$$

## Worked Examples

### Example 1: Spur Gear Forces

**Given:** A spur gear pair transmits 15 kW at 1500 rpm. The pinion has 20 teeth, the gear has 60 teeth, and the module is 4 mm. Pressure angle is 20°.

**Find:** Tangential, radial, and resultant tooth forces.

**Solution:**

Pitch diameter of pinion: $d_1 = mN_1 = 4 \times 20 = 80$ mm

Pitch line velocity:

$$
v = \frac{\pi d_1 n}{60} = \frac{\pi \times 0.080 \times 1500}{60} = 6.28 \text{ m/s}
$$

Tangential force:

$$
F_t = \frac{P}{v} = \frac{15000}{6.28} = 2389 \text{ N}
$$

Radial force:

$$
F_r = F_t \tan\phi = 2389 \times \tan 20^\circ = 870 \text{ N}
$$

Resultant force:

$$
F = \frac{F_t}{\cos\phi} = \frac{2389}{\cos 20^\circ} = 2542 \text{ N}
$$

### Example 2: Planetary Gear Ratio

**Given:** A planetary gearbox has a sun gear with 24 teeth, planet gears with 18 teeth, and a ring gear with 60 teeth. The ring is fixed. The sun gear rotates at 3000 rpm.

**Find:** Carrier speed and gear ratio.

**Solution:**

Verify tooth constraint: $N_r = N_s + 2N_p \Rightarrow 60 = 24 + 2(18) = 60$ ✓

Using the Willis equation with $\omega_r = 0$:

$$
\frac{0 - \omega_c}{\omega_s - \omega_c} = -\frac{N_s}{N_r} = -\frac{24}{60}
$$

$$
-\omega_c = -\frac{24}{60}(\omega_s - \omega_c)
$$

$$
-\omega_c = -0.4\omega_s + 0.4\omega_c
$$

$$
\omega_c = \frac{0.4}{1.4}\omega_s = \frac{2}{7}\omega_s
$$

$$
\omega_c = \frac{2}{7} \times 3000 = 857.1 \text{ rpm}
$$

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

## Exercises

**Exercise 1.** A spur gear pair with standard full-depth teeth has module $m = 3$ mm, pinion $N_1 = 18$ and gear $N_2 = 54$. Find the pitch diameters, centre distance, gear ratio, circular pitch, and the pinion's outside and root diameters.

<details>
<summary>Answer</summary>

- Pitch diameters: $d_1 = mN_1 = 54$ mm, $d_2 = mN_2 = 162$ mm
- Centre distance: $C = (d_1 + d_2)/2 = 108$ mm
- Ratio: $i = N_2/N_1 = 3$
- Circular pitch: $p_c = \pi m = 9.42$ mm
- Pinion outside diameter: $d_1 + 2a = 54 + 2(3) = 60$ mm
- Pinion root diameter: $d_1 - 2b = 54 - 2(1.25 \times 3) = 46.5$ mm

</details>

**Exercise 2.** Compute the contact ratio of the gear pair in Example 1 ($m = 4$ mm, $N_1 = 20$, $N_2 = 60$, $\phi = 20^\circ$, addendum $a = m$). Is it acceptable?

<details>
<summary>Answer</summary>

Pitch radii 40 and 120 mm; addendum radii $r_{a1} = 44$ mm and $r_{a2} = 124$ mm; base radii $r_{b1} = 40\cos 20^\circ = 37.59$ mm and $r_{b2} = 112.76$ mm; $C = 160$ mm.

$$
\sqrt{44^2 - 37.59^2} = 22.87, \quad \sqrt{124^2 - 112.76^2} = 51.58, \quad
C\sin\phi = 54.72
$$

$$
CR = \frac{22.87 + 51.58 - 54.72}{\pi \times 4 \times \cos 20^\circ} = \frac{19.73}{11.81} = 1.67
$$

This is above the recommended minimum of 1.2: on average 1.67 tooth pairs share the load.

</details>

**Exercise 3.** A helical pinion has normal module $m_n = 3$ mm, 30 teeth, helix angle $\psi = 25^\circ$ and normal pressure angle $\phi_n = 20^\circ$. It transmits 10 kW at 1000 rpm. Find the transverse module, pitch diameter, transverse pressure angle and the tangential, radial and axial tooth forces.

<details>
<summary>Answer</summary>

- $m_t = m_n/\cos\psi = 3/\cos 25^\circ = 3.310$ mm, so $d = 30 m_t = 99.30$ mm
- $\tan\phi_t = \tan\phi_n/\cos\psi$ gives $\phi_t = 21.88^\circ$
- $T = P/\omega = 10\,000/(1000 \times 2\pi/60) = 95.49$ N·m

$$
F_t = \frac{2T}{d} = \frac{2 \times 95.49}{0.09930} = 1923 \text{ N}
$$

$$
F_r = \frac{F_t \tan\phi_n}{\cos\psi} = \frac{1923 \tan 20^\circ}{\cos 25^\circ} = 772
\text{ N}, \quad F_a = F_t\tan\psi = 897 \text{ N}
$$

The axial force of almost 900 N must be carried by a thrust-capable bearing.

</details>

**Exercise 4.** For the planetary set of Example 2 ($N_s = 24$, $N_p = 18$, $N_r = 60$): (a) the sun is held and the ring is driven at 1000 rpm; find the carrier speed. (b) The carrier is held and the sun turns at 3000 rpm; find the ring speed.

<details>
<summary>Answer</summary>

(a) Willis with $\omega_s = 0$:

$$
\frac{\omega_r - \omega_c}{0 - \omega_c} = -\frac{24}{60} \implies
\omega_r = 1.4\,\omega_c \implies \omega_c = \frac{1000}{1.4} = 714.3 \text{ rpm}
$$

in the same direction as the ring, matching $i = 1 + N_s/N_r = 1.4$.

(b) With $\omega_c = 0$: $\omega_r/\omega_s = -24/60$, so $\omega_r = -1200$ rpm. The ring turns opposite to the sun and $i = -2.5$.

</details>

**Exercise 5.** A single-start worm drives a 40-tooth worm wheel. The lead angle is $\lambda = 4.5^\circ$ and the coefficient of friction is 0.08. The worm receives 1.5 kW at 1450 rpm. Find the reduction ratio, efficiency, output speed and output torque. Is the drive self-locking?

<details>
<summary>Answer</summary>

- Ratio: $i = N_g/N_w = 40$, so the output speed is $1450/40 = 36.25$ rpm
- Friction angle: $\phi_f = \tan^{-1}0.08 = 4.57^\circ$
- Efficiency: $\eta = \tan 4.5^\circ/\tan(4.5^\circ + 4.57^\circ) = 0.0787/0.1597 = 0.493$
- Input torque: $T_{in} = 1500/(1450 \times 2\pi/60) = 9.88$ N·m
- Output torque: $T_{out} = T_{in}\, i\, \eta = 9.88 \times 40 \times 0.493 = 195$ N·m, which is 739 W of output power

Since $\lambda = 4.5^\circ < \phi_f = 4.57^\circ$ the drive is nominally self-locking, but only just. Vibration lowers the effective friction, so a separate brake is needed where back-driving would be dangerous. Low efficiency and self-locking go together.

</details>

## References

- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 10th ed., McGraw-Hill Education, 2015.
- Norton, R. L., *Machine Design: An Integrated Approach*, 5th ed., Pearson, 2014.
- Litvin, F. L., and Fuentes, A., *Gear Geometry and Applied Theory*, 2nd ed., Cambridge University Press, 2004.
