# Pressure Forces on Structures

Pressure forces arising from static and slowly varying fluid loads are fundamental to the design of hydraulic structures, retaining walls, dams, gates, and submerged bodies. This chapter covers hydrostatic force analysis, center of pressure calculations, curved surface loading, buoyancy, and floating body stability.

## Hydrostatic Pressure Distribution

The pressure at any point in a static, incompressible fluid increases linearly with depth:

$$
p = p_0 + \rho g h
$$

where:

- $p_0$ = surface pressure (atmospheric if open to air)
- $\rho$ = fluid density (kg/m³)
- $g$ = gravitational acceleration (9.81 m/s²)
- $h$ = depth below the free surface (m)

### Gauge vs. Absolute Pressure

In most structural applications the atmospheric pressure acts on both sides of a surface and cancels out. The **gauge pressure** used for force calculations is:

$$
p_g = \rho g h
$$

## Force on Plane Surfaces

### Resultant Force

The total hydrostatic force on a plane surface of area $A$ is:

$$
F = \bar{p} \, A = \rho g \bar{h} \, A
$$

where $\bar{h}$ is the depth of the centroid of the surface below the free surface.

### Center of Pressure

The point through which the resultant force acts is located below the centroid. For a surface inclined at angle $\theta$ to the horizontal, the distance from the free surface to the center of pressure measured along the incline is:

$$
y_{cp} = \bar{y} + \frac{I_{xc}}{\bar{y} \, A}
$$

where:

- $\bar{y}$ = distance from the surface to the centroid along the incline ($\bar{y} = \bar{h}/\sin\theta$)
- $I_{xc}$ = second moment of area about the centroidal axis parallel to the surface

### Common Second Moments of Area

| Shape | $I_{xc}$ |
| --- | --- |
| Rectangle ($b \times d$) | $\dfrac{bd^3}{12}$ |
| Circle (diameter $D$) | $\dfrac{\pi D^4}{64}$ |
| Triangle (base $b$, height $d$) | $\dfrac{bd^3}{36}$ |

## Force on Curved Surfaces

For a curved submerged surface the resultant force is resolved into horizontal and vertical components.

### Horizontal Component

The horizontal component equals the hydrostatic force on the **vertical projection** of the curved surface:

$$
F_H = \rho g \bar{h}_{vp} \, A_{vp}
$$

where $\bar{h}_{vp}$ and $A_{vp}$ are the centroid depth and area of the vertical projection.

### Vertical Component

The vertical component equals the **weight of the fluid** directly above (or that would be above) the curved surface up to the free surface:

$$
F_V = \rho g \, \mathcal{V}
$$

where $\mathcal{V}$ is the volume of fluid above the surface.

### Resultant Force

$$
F_R = \sqrt{F_H^2 + F_V^2}
$$

acting at angle $\alpha = \arctan(F_V / F_H)$ to the horizontal.

## Buoyancy and Archimedes' Principle

A body immersed in a fluid experiences an upward buoyant force equal to the weight of the displaced fluid:

$$
F_B = \rho_f g \, \mathcal{V}_{disp}
$$

### Equilibrium of Floating Bodies

For a floating body in static equilibrium:

$$
W = F_B \implies \rho_s \mathcal{V}_s = \rho_f \mathcal{V}_{disp}
$$

The **draft** of a vessel is set by the displaced volume needed to balance its weight.

## Stability of Floating Bodies

### Metacentric Height

The stability of a floating body depends on the position of the **metacentre** $M$ relative to the centre of gravity $G$. The metacentric height is:

$$
GM = BM - BG
$$

where:

$$
BM = \frac{I_{wp}}{\mathcal{V}_{disp}}
$$

- $I_{wp}$ = second moment of area of the waterplane about the longitudinal axis
- $BG$ = distance from the centre of buoyancy $B$ to the centre of gravity $G$

### Stability Criterion

| Condition | Result |
| --- | --- |
| $GM > 0$ | Stable — restoring moment returns body upright |
| $GM = 0$ | Neutral — body remains at displaced angle |
| $GM < 0$ | Unstable — overturning moment capsizes body |

The restoring moment for a small heel angle $\phi$ is:

$$
M_{rest} = W \cdot GM \cdot \sin\phi
$$

## Worked Example 1: Hydrostatic Force on a Dam

**Given:**

- Vertical rectangular dam wall, width $w = 30$ m, height $H = 12$ m
- Water on one side to full depth, $\rho = 1000$ kg/m³

**Find:** Resultant force and its line of action.

**Solution:**

Centroid depth: $\bar{h} = H/2 = 6$ m

Resultant force:

$$
F = \rho g \bar{h} \, A = 1000 \times 9.81 \times 6 \times
(12 \times 30) = 21{,}189{,}600 \text{ N} \approx 21.2 \text{ MN}
$$

Center of pressure below the surface:

$$
y_{cp} = \bar{y} + \frac{I_{xc}}{\bar{y} A} = 6 +
\frac{30 \times 12^3/12}{6 \times 360} = 6 + 2 = 8 \text{ m}
$$

The force acts **8 m below the surface** (4 m above the base).

## Worked Example 2: Submerged Circular Gate

**Given:**

- Circular gate, diameter $D = 2$ m, hinged at the top
- Centre of gate is 5 m below the water surface
- Gate is vertical

**Find:** Force on the gate and the moment about the hinge.

**Solution:**

Area: $A = \pi D^2/4 = \pi$ m²

Resultant force:

$$
F = \rho g \bar{h} A = 1000 \times 9.81 \times 5 \times \pi = 154{,}095 \text{ N}
\approx 154.1 \text{ kN}
$$

Second moment of area: $I_{xc} = \pi D^4/64 = \pi/4$ m⁴

Center of pressure below surface:

$$
y_{cp} = 5 + \frac{\pi/4}{5 \times \pi} = 5 + 0.05 = 5.05 \text{ m}
$$

Distance from hinge (top of gate at 4 m depth) to center of pressure:

$$
d = 5.05 - 4.0 = 1.05 \text{ m}
$$

Moment about the hinge:

$$
M = F \times d = 154.1 \times 1.05 \approx 161.8 \text{ kN·m}
$$

## Worked Example 3: Stability of a Floating Barge

**Given:**

- Rectangular barge: length $L = 20$ m, beam $B = 8$ m, depth $D = 3$ m
- Barge mass $m = 200{,}000$ kg (centre of gravity 1.8 m above keel)
- Seawater density $\rho = 1025$ kg/m³

**Find:** Draft and metacentric height.

**Solution:**

Draft $T$ from equilibrium:

$$
\rho g L B T = mg \implies
T = \frac{m}{\rho L B} = \frac{200{,}000}{1025 \times 20 \times 8} = 1.22 \text{ m}
$$

Centre of buoyancy above keel: $KB = T/2 = 0.61$ m

Second moment of waterplane area:

$$
I_{wp} = \frac{L B^3}{12} = \frac{20 \times 8^3}{12} = 853.3 \text{ m}^4
$$

Displaced volume: $\mathcal{V}_{disp} = L B T = 195.1$ m³

$$
BM = \frac{I_{wp}}{\mathcal{V}_{disp}} = \frac{853.3}{195.1} = 4.37 \text{ m}
$$

$$
KM = KB + BM = 0.61 + 4.37 = 4.98 \text{ m}
$$

$$
GM = KM - KG = 4.98 - 1.80 = 3.18 \text{ m}
$$

Since $GM > 0$, the barge is **stable** with a comfortable margin.

## Applications

### Dams and Retaining Walls

- Gravity dam design relies on the overturning moment from hydrostatic force
- Sliding and overturning safety factors are checked against resultant forces
- Uplift pressure beneath the dam is included in stability analysis

### Lock Gates and Sluice Gates

- Force on lock gates determines hinge reactions and gate thickness
- Sluice gates require knowledge of the center of pressure for actuator sizing

### Submerged Pipelines and Tunnels

- Net buoyancy or downward force depends on pipe weight versus displaced water
- Ballast or anchoring is sized using Archimedes' principle

### Ship and Offshore Platform Design

- Hull form is shaped to achieve the required displaced volume at design draft
- Metacentric height governs intact and damaged stability criteria
- Classification society rules specify minimum $GM$ values

## Design Considerations

### Load Combinations

- Hydrostatic load is combined with seismic, thermal, and operational loads
- Partial safety factors are applied to water level and density

### Factors of Safety

- Overturning: $\text{FOS}_{OT} = M_{restoring} / M_{overturning} \geq 1.5$ (typical)
- Sliding: $\text{FOS}_{SL} = \mu W / F_H \geq 1.5$

### Pressure Testing

- Tanks and pressure vessels are hydrostatically tested to 1.25–1.5 times design pressure
- Proof testing confirms structural adequacy before service

Understanding hydrostatic pressure forces is a prerequisite for more advanced fluid loading topics such as wave loading and dynamic flow forces on structures.

## Related Scripts

- [Pressure Variation with Depth](../../../scripts/plots/pressure_variation_with_depth/): plots how hydrostatic pressure increases linearly with depth below the free surface of a fluid at rest.

## Exercises

**Exercise 1.** A vertical rectangular gate 2 m wide and 3 m tall has its top edge 1.5 m below the free surface of fresh water. Find the resultant force and the depth of the center of pressure.

<details>
<summary>Answer</summary>

The centroid depth is $\bar{h} = 1.5 + 1.5 = 3$ m and $A = 6$ m².

```math
F = \rho g\bar{h}A = 1000 \times 9.81 \times 3 \times 6 = 176.6 \text{ kN}
```

```math
y_{cp} = \bar{y} + \frac{I_{xc}}{\bar{y}A} = 3 +
\frac{2 \times 3^3/12}{3 \times 6} = 3 + 0.25 = 3.25 \text{ m}
```

</details>

**Exercise 2.** A rectangular plate 1.5 m wide and 2 m long (measured along its slope) lies in a plane inclined at $30^\circ$ to the horizontal, with its top edge 1 m below the surface of fresh water. Find the resultant force and the position of the center of pressure along the incline.

<details>
<summary>Answer</summary>

Along the incline the top edge is $1/\sin 30^\circ = 2$ m from the surface, so $\bar{y} = 3$ m and $\bar{h} = 3\sin 30^\circ = 1.5$ m. The area is $A = 3$ m².

```math
F = 1000 \times 9.81 \times 1.5 \times 3 = 44.1 \text{ kN}
```

```math
I_{xc} = \frac{1.5 \times 2^3}{12} = 1.0 \text{ m}^4, \quad y_{cp} = 3 +
\frac{1.0}{3 \times 3} = 3.11 \text{ m}
```

The center of pressure is 3.11 m from the surface along the incline, i.e. 1.11 m below the top edge.

</details>

**Exercise 3.** A gate has the shape of a quarter circle of radius $R = 2$ m and is 4 m wide. Water lies above the gate, filling the quarter-circle region between the curved surface and the free surface, which is level with the top of the gate. Find the horizontal and vertical force components and the resultant.

<details>
<summary>Answer</summary>

The vertical projection is 2 m high × 4 m wide, with centroid at 1 m depth:

```math
F_H = 1000 \times 9.81 \times 1 \times 8 = 78.5 \text{ kN}
```

The water above the gate occupies a quarter disc of area $\pi R^2/4 = \pi$ m², so

```math
F_V = \rho g\mathcal{V} = 9810 \times 4\pi = 123.3 \text{ kN}
```

```math
F_R = \sqrt{78.5^2 + 123.3^2} = 146.1 \text{ kN}, \quad \alpha = \arctan
\frac{123.3}{78.5} = 57.5^\circ
```

For a circular surface the resultant passes through the centre of the circle.

</details>

**Exercise 4.** A solid wooden cube (side 0.5 m, density 600 kg/m³) floats in fresh water with one face horizontal. Find its draft and metacentric height. Is this orientation stable?

<details>
<summary>Answer</summary>

Draft: $T = 0.5 \times 600/1000 = 0.3$ m, so $KB = 0.15$ m and $KG = 0.25$ m.

```math
BM = \frac{I_{wp}}{\mathcal{V}_{disp}} = \frac{0.5^4/12}{0.5 \times 0.5 \times 0.3} = \frac{0.005208}{0.075} = 0.069 \text{ m}
```

```math
GM = KB + BM - KG = 0.15 + 0.069 - 0.25 = -0.031 \text{ m}
```

$GM < 0$, so this upright orientation is unstable and the cube will heel over to a tilted equilibrium.

</details>

**Exercise 5.** An empty steel pipeline (outer diameter 0.6 m, wall thickness 20 mm, $\rho_s = 7850$ kg/m³) is laid in seawater ($\rho = 1025$ kg/m³). Find the net vertical force per metre and state whether it needs additional weight.

<details>
<summary>Answer</summary>

Steel area: $\frac{\pi}{4}(0.6^2 - 0.56^2) = 0.03644$ m², giving a mass of 286.1 kg/m.

Displaced water: $\frac{\pi}{4}(0.6^2) \times 1025 = 289.8$ kg/m.

The net force is $(289.8 - 286.1) \times 9.81 = 36.7$ N/m upward, so the empty pipe floats. A concrete weight coating or anchoring is required for on-bottom stability.

</details>

## References

- F. M. White, *Fluid Mechanics*, 7th ed., McGraw-Hill, 2011.
- B. R. Munson, D. F. Young, T. H. Okiishi, W. W. Huebsch, *Fundamentals of Fluid Mechanics*, Wiley.
- K. J. Rawson, E. C. Tupper, *Basic Ship Theory*, 5th ed., Butterworth-Heinemann, 2001.
