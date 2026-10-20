# Gears and Transmissions

Gears transmit rotation and torque between shafts at a fixed speed ratio by the meshing of teeth. They are the standard means of changing speed and torque in machine tools, vehicle transmissions, wind turbines, helicopter rotors and geared turbofans, and spur and helical stages run at 98 to 99% efficiency. This note derives the fundamental law of gearing and the involute profile, sets out the tooth geometry and the conditions for smooth meshing (contact ratio, interference), treats simple, compound and planetary gear trains, and ends with tooth forces, the Lewis bending stress and efficiency.

## Problem Statement

Given the power $P$ to be transmitted, the input speed, the required ratio, and the gear geometry (number of teeth $N$, module $m$, pressure angle $\phi$, face width $F$, helix angle for helical gears), find:

- the speeds and directions of every shaft of a gear train, including planetary trains with two inputs;
- the geometry of the mesh: pitch and base circles, centre distance, contact ratio, and whether the teeth interfere;
- the forces on the teeth and so on the shafts and bearings;
- the bending stress at the tooth root and the efficiency of the drive.

The teeth are rigid involutes with no backlash, the transmitted torque is steady, and the load is carried by one tooth pair at the worst point of the mesh. The governing relations are the fundamental law of gearing, $\omega_1/\omega_2 = N_2/N_1$ for each mesh, and the Willis equation for trains whose axes move.

## The Fundamental Law of Gearing

Let two tooth profiles on gears turning about $O_1$ and $O_2$ touch at a point $C$, and let the common normal to the profiles at $C$ cut the line of centres at $P$. The velocities of the two points that coincide at $C$ are $\omega_1 \times O_1C$ and $\omega_2 \times O_2C$. If the profiles neither separate nor penetrate, their components along the common normal are equal, which gives $\omega_1 r_{n1} = \omega_2 r_{n2}$, with $r_{n1}$ and $r_{n2}$ the distances from $O_1$ and $O_2$ to the normal. By similar triangles,

$$
\frac{\omega_1}{\omega_2} = \frac{O_2P}{O_1P}
$$

The angular velocity ratio is constant only if $P$ stays fixed: the common normal at every point of contact must pass through a fixed point on the line of centres, the **pitch point**. This is the fundamental law of gearing. Circles about $O_1$ and $O_2$ through $P$ are the pitch circles; they roll on each other without slipping, so $\omega_1 r_1 = \omega_2 r_2$. The tangential components of the two velocities at $C$ differ except at $P$, so teeth slide on each other everywhere except at the pitch point, and the sliding speed grows with distance from it.

Profiles that satisfy the law are called conjugate. Cycloidal profiles are conjugate and were used in clocks. Almost all power gears use the involute.

## The Involute Profile

An involute of a circle is the curve traced by the end of a taut string unwound from it. For a base circle of radius $r_b$ and roll angle $t$,

$$
x = r_b(\cos t + t\sin t),
\qquad y = r_b(\sin t - t\cos t)
$$

The string is tangent to the base circle and normal to the involute at every instant. For two involutes on base circles $r_{b1}$ and $r_{b2}$ in contact, the common normal is therefore the common internal tangent of the two base circles, a fixed line. It is the **line of action**, and it passes through the pitch point at the **pressure angle** $\phi$ to the common tangent of the pitch circles, with

$$
r_b = r\cos\phi
$$

The involute has three properties that make it the standard profile. The force between teeth acts along a fixed line, so its direction does not change through the mesh. A change in centre distance changes the pitch circles and the operating pressure angle but not the ratio $r_{b2}/r_{b1}$, so the ratio is insensitive to mounting errors and shaft deflection. The involute rack has straight-sided teeth, so a single straight-sided cutter (hob or rack cutter) generates gears of any number of teeth.

At radius $\rho \ge r_b$ the involute makes the pressure angle $\alpha$ with $\cos\alpha = r_b/\rho$, and its polar angle is the involute function

```math
\mathrm{inv}\,\alpha = \tan\alpha - \alpha
```

which gives the tooth thickness at any radius from the thickness at the pitch circle.

![Involute construction, a meshing pinion and gear with the line of action and path of contact, and the minimum pinion teeth without interference](../../../scripts/plots/gears_involute_profile/gears_involute_profile.png)

Panel (a) shows the involute as the end of the unwound string. Panel (b) is a 20-tooth pinion and a 40-tooth gear of module 4 mm: the teeth touch on the line of action, and the red segment between the two addendum circles is the path along which they are in contact. Panel (c) is discussed under interference below.

## Tooth Geometry

The size of the teeth is set by the **module** $m = d/N$, the pitch diameter in millimetres per tooth. In US practice the diametral pitch $P_d = N/d$ is used, in teeth per inch, so $P_d = 25.4/m$ with $m$ in mm. Two gears mesh only if they have the same module (or diametral pitch) and pressure angle. The standard pressure angle is 20°; 14.5° survives in old designs and 25° is used for high load capacity. Standard full-depth proportions are:

| Quantity | Formula |
| --- | --- |
| pitch diameter | $d = mN$ |
| circular pitch (tooth plus space on the pitch circle) | $p = \pi m$ |
| base pitch (along the line of action) | $p_b = \pi m\cos\phi$ |
| base circle radius | $r_b = \tfrac{1}{2}mN\cos\phi$ |
| addendum, tooth height above the pitch circle | $a = m$ |
| dedendum, depth below the pitch circle | $b = 1.25m$ |
| clearance | $b - a = 0.25m$ |
| tooth thickness on the pitch circle | $\pi m/2$ |
| centre distance | $C = \tfrac{1}{2}m(N_1 + N_2)$ |
| speed ratio | $\omega_1/\omega_2 = N_2/N_1 = d_2/d_1$ |

The pitch line velocity is $v = \omega r = \pi d n/60$ with $n$ in rpm, and the power is $P = T\omega = F_t v$.

## Contact Ratio

For continuous motion the next pair of teeth must come into contact before the present pair separates. Contact starts where the addendum circle of the driven gear crosses the line of action and ends where the addendum circle of the driver crosses it. The length of this path of contact is

$$
Z = \sqrt{r_{a1}^2 - r_{b1}^2} + \sqrt{r_{a2}^2 - r_{b2}^2} - C\sin\phi
$$

with $r_a = r + a$ the addendum radii. Successive teeth are a base pitch apart along the line of action, so the **contact ratio**, the average number of tooth pairs in contact, is

$$
m_c = \frac{Z}{p_b} = \frac{Z}{\pi m\cos\phi}
$$

It should be at least 1.2, and spur gears usually have 1.4 to 1.8. With $m_c = 1.6$, two pairs share the load for 60% of each base pitch and one pair carries it alone for 40%. The pinion and gear of the figure have $Z = 19.31$ mm, $p_b = 11.81$ mm and $m_c = 1.635$.

## Interference and the Minimum Number of Teeth

The pinion flank is an involute only outside its base circle. If the addendum circle of the gear cuts the line of action beyond the point where the line touches the pinion base circle, the gear tip meets the non-involute part of the pinion flank: this is involute interference. In cutting, the generating tool then removes material from the pinion root (undercut), which weakens the tooth and shortens the contact. For full-depth teeth (addendum $km$ with $k = 1$) and gear ratio $m_G = N_G/N_P$, the smallest pinion free of interference is

$$
N_P = \frac{2k}{(1 + 2m_G)\sin^2\phi}\left(m_G +
\sqrt{m_G^2 + (1 + 2m_G)\sin^2\phi}\right)
$$

rounded up, and against a rack $N_P = 2k/\sin^2\phi$.

| Pressure angle | Equal gears ($m_G = 1$) | Against a rack |
| --- | --- | --- |
| 14.5° | 23 | 32 |
| 20° | 13 | 18 |
| 25° | 9 | 12 |

Panel (c) of the figure plots the limit against gear ratio. Smaller pinions are made by profile shift: the cutter is withdrawn by a fraction of the module, which thickens the tooth root and moves the active profile outside the base circle, at the cost of changing the centre distance or the mating gear.

## Gear Types

| Type | Shafts | Typical ratio per stage | Efficiency | Notes |
| --- | --- | --- | --- | --- |
| spur | parallel | up to about 6 | 98–99% | simplest, no axial force, noisy at high speed |
| helical | parallel (or crossed) | up to about 10 | 97–99% | gradual engagement, quieter, axial thrust |
| double helical (herringbone) | parallel | up to about 10 | 97–99% | thrust cancels between the two halves |
| straight or spiral bevel | intersecting, usually 90° | up to about 6 | 97–99% | pitch surfaces are cones |
| worm and wheel | crossed, 90° | 5 to 100 | 40–90% | sliding contact, can be self-locking |

### Helical Gears

The teeth of a helical gear lie on a helix of angle $\psi$ to the axis. Measured normal to the teeth, the tooth form is a standard one, so the normal module $m_n$ and normal pressure angle $\phi_n$ are the standard values; in the transverse plane

$$
m_t = \frac{m_n}{\cos\psi},
\qquad \tan\phi_t = \frac{\tan\phi_n}{\cos\psi},
\qquad d = m_t N
$$

For bending strength a helical gear behaves like a spur gear of $N_v = N/\cos^3\psi$ teeth, the virtual number of teeth. Contact moves across the face gradually, which raises the total contact ratio by the face contact ratio $F\tan\psi/p$ and makes helical gears quieter than spur gears.

### Bevel and Worm Gears

Bevel gears have conical pitch surfaces; for shafts at 90° the pitch cone angles satisfy $\tan\gamma_1 = N_1/N_2$ and $\tan\gamma_2 = N_2/N_1$. A worm is a screw with $N_w$ starts (threads) meshing with a wheel of $N_g$ teeth, so the ratio is $N_g/N_w$. The contact is mostly sliding, and for a worm of lead angle $\lambda$ and coefficient of friction $f = \tan\phi_f$, treated as a square-thread screw,

$$
\eta = \frac{\tan\lambda}{\tan(\lambda + \phi_f)}
$$

With the normal pressure angle $\phi_n$ of the thread included, $\eta = (\cos\phi_n - f\tan\lambda)/(\cos\phi_n + f\cot\lambda)$. When $\lambda$ is below about the friction angle the wheel cannot drive the worm: the drive is self-locking, which is useful in hoists but always goes with an efficiency below 50%.

## Gear Trains

### Simple and Compound Trains

In a simple train each shaft carries one gear. Each external mesh reverses the direction of rotation, and the overall ratio is

$$
\frac{\omega_{\mathrm{in}}}{\omega_{\mathrm{out}}} = (-1)^{k}
\frac{N_{\mathrm{last}}}{N_{\mathrm{first}}}
$$

with $k$ the number of external meshes. Intermediate (idler) gears change the direction but not the ratio. In a compound train two gears share a shaft, and the ratio is the product of the stage ratios,

$$
\frac{\omega_{\mathrm{in}}}{\omega_{\mathrm{out}}} = \pm
\frac{\text{product of driven teeth}}{\text{product of driving teeth}}
$$

A large ratio is made in several stages because one stage with a very small pinion would interfere or have a large gear. For a total ratio $i$ in $k$ stages, equal stage ratios $i^{1/k}$ give roughly the smallest train; a reverted train, with input and output on the same axis, also needs equal centre distances in its two stages.

### Planetary Trains and the Willis Equation

A planetary (epicyclic) train has a sun gear $s$, planets $p$ carried by an arm or carrier $c$, and an internal ring gear $r$. The planets turn about their own axes and orbit with the carrier. Relative to the carrier the train is an ordinary train with the planet as an idler, so the speeds relative to the carrier obey the Willis equation

$$
\frac{\omega_r - \omega_c}{\omega_s - \omega_c} = -\frac{N_s}{N_r}
$$

The minus sign is because sun and ring turn in opposite directions when the carrier is held. With $\alpha = N_r/N_s$ the equation is $\omega_s + \alpha\omega_r = (1 + \alpha)\omega_c$: the train has two degrees of freedom, and fixing one member or driving two of them sets the third. Concentric meshing requires $N_r = N_s + 2N_p$, and $n$ equally spaced planets can be assembled only if $(N_s + N_r)/n$ is an integer.

| Fixed member | Input | Output | Ratio $\omega_{\mathrm{in}}/\omega_{\mathrm{out}}$ |
| --- | --- | --- | --- |
| ring | sun | carrier | $1 + N_r/N_s$ |
| carrier | sun | ring | $-N_r/N_s$ |
| sun | ring | carrier | $1 + N_s/N_r$ |

Several planets share the load, the input and output are coaxial, and two-input operation allows differentials and power-split hybrid transmissions. In an automatic transmission, clutches and brakes select which member is held.

A planetary set has $N_s = 24$, $N_p = 18$ and $N_r = 60$ with the ring fixed and the sun at 3000 rpm. The tooth condition $24 + 2 \times 18 = 60$ holds, and three planets fit since $(24 + 60)/3 = 28$. With $\omega_r = 0$ the Willis equation gives $-\omega_c = -0.4(\omega_s - \omega_c)$, so $\omega_c = (0.4/1.4)\omega_s = 857.1$ rpm and the ratio is $1 + 60/24 = 3.5$.

## Tooth Forces

The force between spur teeth acts along the line of action. It is split into a tangential component that transmits torque and a radial component that pushes the gears apart:

$$
F_t = \frac{2T}{d} = \frac{P}{v},
\qquad F_r = F_t\tan\phi,
\qquad F = \frac{F_t}{\cos\phi}
$$

For helical gears with normal pressure angle $\phi_n$ an axial component appears,

$$
F_r = \frac{F_t\tan\phi_n}{\cos\psi},
\qquad F_a = F_t\tan\psi
$$

and for a straight bevel gear with mean pitch diameter $d_m$ and pitch cone angle $\gamma$, $F_t = 2T/d_m$, $F_r = F_t\tan\phi\cos\gamma$ and $F_a = F_t\tan\phi\sin\gamma$. These forces load the shafts in bending and the bearings radially and axially; see [Bearings and Lubrication](bearings.md).

## Bending Stress: the Lewis Equation

Lewis (1892) treated a tooth as a cantilever loaded at its tip by $F_t$, with the critical section where a parabola of uniform strength inscribed in the tooth touches the root fillet. If $l$ is the height of the load above that section and $t$ the tooth thickness there, the root stress is $\sigma = 6F_tl/(Ft^2)$. Writing $t$ and $l$ in units of the module collects the tooth shape into a dimensionless form factor $Y$:

```math
\sigma = \frac{F_t}{F\,m\,Y}
```

with $F$ the face width. $Y$ depends on the number of teeth and the tooth system. For 20° full-depth teeth:

| $N$ | 12 | 15 | 17 | 20 | 24 | 30 | 38 | 50 | 60 | 100 | rack |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $Y$ | 0.245 | 0.290 | 0.303 | 0.322 | 0.337 | 0.359 | 0.384 | 0.409 | 0.422 | 0.447 | 0.485 |

Dynamic loads from tooth errors and deflections are allowed for with a velocity factor, $\sigma = K_vF_t/(FmY)$. Barth's form for cut or milled teeth is $K_v = (6.1 + v)/6.1$ with $v$ in m/s; more accurate hobbed or ground teeth have smaller factors. The face width is usually 3 to 5 circular pitches.

The Lewis equation ignores the stress concentration at the root fillet, load sharing between tooth pairs and the radial compressive component, and it says nothing about surface fatigue (pitting). Gear rating standards, AGMA 2001 in the US and ISO 6336 internationally, keep the same structure but replace $Y$ by a geometry factor that includes the fillet and the load position, add factors for overload, dynamic load, size, load distribution and rim thickness, and add a separate contact-stress check based on the Hertz stress between the two flanks. Root bending is a fatigue problem, so the allowable stress is a fatigue strength corrected for life and reliability; see [Fatigue](../strength_materials/fatigue.md).

## Efficiency

Losses in a gear mesh come from sliding friction between the flanks, which grows with the distance of contact from the pitch point, and from oil churning and windage, which grow with speed. A spur or helical stage loses 1 to 2% of the power, so a three-stage gearbox is about 95% efficient. Worm gears lose far more because their contact is almost pure sliding. In a planetary train the mesh losses depend on the power that flows through the meshes relative to the carrier, which can be much larger or smaller than the transmitted power; trains with large ratios built from differential arrangements can have low efficiency for this reason.

## Worked Example

A spur pinion of $N_1 = 20$ teeth drives a gear of $N_2 = 60$ teeth. The module is 4 mm, the pressure angle 20° and the face width 40 mm, and the pinion transmits 15 kW at 1500 rpm. Find the tooth forces and the pinion bending stress.

1. Geometry: $d_1 = 4 \times 20 = 80$ mm, $d_2 = 240$ mm, $C = 160$ mm, ratio 3.
2. Pitch line velocity: $v = \pi \times 0.080 \times 1500/60 = 6.283$ m/s.
3. Tangential force: $`F_t = 15\,000/6.283 = 2387`$ N. Check with torque: $`T_1 = 15\,000/157.08 = 95.5`$ N·m and $2T_1/d_1 = 2387$ N.
4. Radial force: $F_r = 2387\tan 20^\circ = 869$ N; resultant $F = 2387/\cos 20^\circ = 2541$ N.
5. Lewis stress with $Y = 0.322$:

```math
\sigma = \frac{F_t}{FmY} = \frac{2387}{0.040 \times 0.004 \times 0.322} = 46.3 \text{ MPa}
```

6. With Barth's factor for cut teeth, $K_v = (6.1 + 6.283)/6.1 = 2.03$, the design stress is 94.1 MPa, to be compared with the corrected bending fatigue strength of the pinion material.

## Key Takeaways

- A constant speed ratio needs the common normal at every contact point to pass through the fixed pitch point; involute teeth satisfy this with a fixed line of action at the pressure angle.
- The base circle radius $r_b = r\cos\phi$ fixes the involute; centre-distance errors change the pressure angle but not the ratio.
- Gears mesh only with equal module (or diametral pitch) and pressure angle; the contact ratio should be at least 1.2.
- A 20° full-depth pinion needs at least 18 teeth against a rack and 13 against an equal gear to avoid interference.
- The Willis equation $(\omega_r - \omega_c)/(\omega_s - \omega_c) = -N_s/N_r$ handles every planetary configuration, including two inputs.
- The Lewis equation $\sigma = F_t/(FmY)$ gives the root bending stress; rating standards add fatigue, dynamic and contact-stress checks.

## Related Scripts

- [Involute Gear Geometry](../../../scripts/plots/gears_involute_profile/): draws the involute construction, a standard 20° spur pinion and gear in mesh with their line of action and path of contact, and the smallest pinion that can mesh without interference as a function of gear ratio.

## Exercises

**Exercise 1.** A spur gear pair with standard full-depth teeth has module $m = 3$ mm, pinion $N_1 = 18$ and gear $N_2 = 54$. Find the pitch diameters, centre distance, gear ratio, circular pitch, and the pinion's outside and root diameters.

<details>
<summary>Answer</summary>

- Pitch diameters: $d_1 = mN_1 = 54$ mm, $d_2 = mN_2 = 162$ mm
- Centre distance: $C = (d_1 + d_2)/2 = 108$ mm
- Ratio: $i = N_2/N_1 = 3$
- Circular pitch: $p = \pi m = 9.42$ mm
- Pinion outside diameter: $d_1 + 2a = 54 + 2(3) = 60$ mm
- Pinion root diameter: $d_1 - 2b = 54 - 2(1.25 \times 3) = 46.5$ mm

An 18-tooth 20° pinion is exactly at the rack limit for interference, and above the limit of 15 for a 1:3 gear ratio, so it is not undercut.

</details>

**Exercise 2.** Compute the contact ratio of the gear pair in the worked example ($m = 4$ mm, $N_1 = 20$, $N_2 = 60$, $\phi = 20^\circ$, addendum $a = m$). Is it acceptable?

<details>
<summary>Answer</summary>

Pitch radii 40 and 120 mm; addendum radii $r_{a1} = 44$ mm and $r_{a2} = 124$ mm; base radii $r_{b1} = 40\cos 20^\circ = 37.59$ mm and $r_{b2} = 112.76$ mm; $C = 160$ mm.

```math
\sqrt{44^2 - 37.59^2} = 22.87, \quad \sqrt{124^2 - 112.76^2} = 51.58, \quad C\sin\phi = 54.72
```

```math
m_c = \frac{22.87 + 51.58 - 54.72}{\pi \times 4 \times \cos 20^\circ} = \frac{19.73}{11.81} = 1.67
```

This is above the minimum of 1.2: on average 1.67 tooth pairs share the load, and a single pair carries it for 33% of each base pitch.

</details>

**Exercise 3.** A helical pinion has normal module $m_n = 3$ mm, 30 teeth, helix angle $\psi = 25^\circ$ and normal pressure angle $\phi_n = 20^\circ$. It transmits 10 kW at 1000 rpm. Find the transverse module, pitch diameter, transverse pressure angle and the tangential, radial and axial tooth forces.

<details>
<summary>Answer</summary>

- $m_t = m_n/\cos\psi = 3/\cos 25^\circ = 3.310$ mm, so $d = 30 m_t = 99.30$ mm
- $\tan\phi_t = \tan\phi_n/\cos\psi$ gives $\phi_t = 21.88^\circ$
- $`T = P/\omega = 10\,000/(1000 \times 2\pi/60) = 95.49`$ N·m

```math
F_t = \frac{2T}{d} = \frac{2 \times 95.49}{0.09930} = 1923 \text{ N}
```

```math
F_r = \frac{F_t \tan\phi_n}{\cos\psi} = \frac{1923 \tan 20^\circ}{\cos 25^\circ} = 772 \text{ N}, \quad F_a = F_t\tan\psi = 897 \text{ N}
```

The axial force of almost 900 N must be carried by a thrust-capable bearing.

</details>

**Exercise 4.** For the planetary set with $N_s = 24$, $N_p = 18$, $N_r = 60$: (a) the sun is held and the ring is driven at 1000 rpm; find the carrier speed. (b) The carrier is held and the sun turns at 3000 rpm; find the ring speed. (c) In a second set with $N_r/N_s = 4$, the sun turns at 1000 rpm and the ring is driven at 200 rpm in the opposite direction. Find the carrier speed, and the ring speed that holds the carrier still.

<details>
<summary>Answer</summary>

(a) Willis with $\omega_s = 0$:

```math
\frac{\omega_r - \omega_c}{0 - \omega_c} = -\frac{24}{60} \implies \omega_r = 1.4\,\omega_c \implies \omega_c = \frac{1000}{1.4} = 714.3 \text{ rpm}
```

in the same direction as the ring, matching the ratio $1 + N_s/N_r = 1.4$.

(b) With $\omega_c = 0$: $\omega_r/\omega_s = -24/60$, so $\omega_r = -1200$ rpm. The ring turns opposite to the sun and the ratio is $-2.5$.

(c) With $\alpha = 4$:

```math
\omega_c = \frac{\omega_s + \alpha\omega_r}{1 + \alpha} = \frac{1000 + 4(-200)}{5} = 40 \text{ rpm}
```

The carrier is stationary when $\omega_s + \alpha\omega_r = 0$, that is $\omega_r = -250$ rpm. This two-input behaviour is the basis of differentials and power-split drives.

</details>

**Exercise 5.** A single-start worm drives a 40-tooth worm wheel. The lead angle is $\lambda = 4.5^\circ$ and the coefficient of friction is 0.08. The worm receives 1.5 kW at 1450 rpm. Find the reduction ratio, the efficiency by the square-thread formula, the output speed and torque, and decide whether the drive is self-locking. How much does a 20° normal pressure angle change the efficiency?

<details>
<summary>Answer</summary>

- Ratio: $i = N_g/N_w = 40$, so the output speed is $1450/40 = 36.25$ rpm
- Friction angle: $\phi_f = \tan^{-1}0.08 = 4.57^\circ$
- Efficiency: $\eta = \tan 4.5^\circ/\tan(4.5^\circ + 4.57^\circ) = 0.0787/0.1597 = 0.493$
- Input torque: $T_{\mathrm{in}} = 1500/(1450 \times 2\pi/60) = 9.88$ N·m
- Output torque: $`T_{\mathrm{out}} = T_{\mathrm{in}}\, i\, \eta = 9.88 \times 40 \times 0.493 = 195`$ N·m, which is 739 W of output power

Since $\lambda = 4.5^\circ < \phi_f = 4.57^\circ$ the drive is nominally self-locking, but only just. Vibration lowers the effective friction, so a separate brake is needed where back-driving would be dangerous.

With $\phi_n = 20^\circ$:

```math
\eta = \frac{\cos 20^\circ - 0.08\tan 4.5^\circ}{\cos 20^\circ + 0.08\cot 4.5^\circ} = \frac{0.9334}{1.9562} = 0.477
```

so the pressure angle lowers the efficiency by about 1.6 percentage points.

</details>

## References

- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 11th ed., McGraw-Hill Education, 2020.
- Norton, R. L., *Machine Design: An Integrated Approach*, 5th ed., Pearson, 2014.
- Litvin, F. L., and Fuentes, A., *Gear Geometry and Applied Theory*, 2nd ed., Cambridge University Press, 2004.
- Uicker, J. J., Pennock, G. R., and Shigley, J. E., *Theory of Machines and Mechanisms*, 5th ed., Oxford University Press, 2017.
- Dudley, D. W., *Handbook of Practical Gear Design*, CRC Press, 1994.
- ANSI/AGMA 2001-D04, *Fundamental Rating Factors and Calculation Methods for Involute Spur and Helical Gear Teeth*, American Gear Manufacturers Association, 2004.
