# Torsion

A member twisted by moments about its own axis is in torsion. Drive shafts, axles, turbine and pump shafts, torsion bars, drill strings, screw threads and closed box sections such as aircraft wings and car bodies are all designed against torsional shear stress and twist. This note derives the shear stress and angle of twist of solid and hollow circular shafts, applies them to power transmission and to statically indeterminate shafts, and then treats non-circular sections, where cross-sections warp: solid rectangles with tabulated coefficients, thin-walled closed sections by the Bredt–Batho formula, and thin open sections. Torsion combined with bending and axial load is in [Combined Loading](combined_loading.md).

## Problem Statement

A straight shaft lies along $x$, $0 \le x \le L$. Its cross-section is given (solid or hollow circle, rectangle, thin-walled closed or open profile) and may change between segments; its material is linear elastic with shear modulus $G$. It carries concentrated torques $T_i$ at points $x_i$ and possibly a distributed torque $t(x)$ (N m/m), and it is supported by bearings that allow rotation, or fixed against rotation at one or both ends. Find the internal torque $T(x)$, the distribution and maximum of the shear stress over each section, the angle of twist $\phi(x)$, the reactions at fixed ends, and, for design, the section size that keeps the stress and twist below allowable values for a given power and speed.

The assumptions are small twist angles, linear elasticity, no axial force or bending, and torque applied so that end effects are local (Saint-Venant's principle). The governing equations are equilibrium of a slice and the torque–twist relation,

$$
\frac{dT}{dx} + t = 0,
\qquad T = G J_t \frac{d\phi}{dx}
$$

where $J_t$ is the torsion constant of the section. For a circular section $J_t$ is the polar second moment of area $J$; for every other section $J_t < J$.

## Circular Shafts

### Kinematics and Shear Stress

By symmetry, a cross-section of a circular shaft rotates as a rigid disc and stays plane, and radial lines stay straight. Consider a slice of length $dx$ whose faces rotate by $\phi$ and $\phi + d\phi$. A longitudinal fibre at radius $\rho$ is tilted by the angle

```math
\gamma = \rho\, \frac{d\phi}{dx}
```

which is the shear strain in the $x$–tangential plane. Hooke's law gives $`\tau = G\gamma = G\rho\,\phi'`$, linear in $\rho$. The resultant moment of these stresses about the axis must equal the internal torque:

```math
T = \int_A \rho\,\tau\, dA = G\phi'\int_A \rho^2\, dA = G J\phi'
```

Eliminating $G\phi'$ gives the torsion formula and the twist rate:

$$
\tau = \frac{T\rho}{J},
\qquad \tau_{\max} = \frac{Tc}{J},
\qquad \frac{d\phi}{dx} = \frac{T}{GJ}
$$

where $c$ is the outer radius. The polar second moments of area are

$$
J = \frac{\pi d^4}{32} \ \ \text{(solid)},
\qquad J = \frac{\pi}{32}\left(d_o^4 - d_i^4\right) \ \ \text{(hollow)}
$$

and for a solid shaft $\tau_{\max} = 16T/(\pi d^3)$.

By the symmetry of the stress tensor, the same shear stress acts on longitudinal planes. The principal stresses at the surface are $\pm\tau_{\max}$ on planes at $45^\circ$ to the axis. A ductile shaft therefore fails by shear on a transverse plane, giving a flat fracture, while a brittle shaft (cast iron, chalk) fails in tension along a $45^\circ$ helix. Wood and fibre composites, weak in longitudinal shear, split along the grain.

### Angle of Twist

Integrating the twist rate gives

```math
\phi = \int_0^L \frac{T(x)}{G J(x)}\, dx = \sum_i \frac{T_i L_i}{G_i J_i}
```

the sum applying to prismatic segments with constant torque. A steel shaft ($G = 80$ GPa) consists of segment AB, 600 mm long and 40 mm in diameter, carrying 500 N m, and segment BC, 400 mm long and 30 mm in diameter, carrying 200 N m. In N and mm, $J_1 = \pi(40)^4/32 = 2.513 \times 10^5$ mm⁴ and $J_2 = 7.952 \times 10^4$ mm⁴, so

```math
\phi_{C/A} = \frac{500 \times 10^3 \times 600}{80\,000 \times 2.513 \times 10^5} + \frac{200 \times 10^3 \times 400}{80\,000 \times 7.952 \times 10^4} = 0.01492 + 0.01258 = 0.0275 \text{ rad} = 1.58^\circ
```

Torques must be in N mm when lengths are in mm and $G$ in N/mm²; mixing N m with mm is the usual source of errors of $10^3$.

### Solid and Hollow Shafts

Material near the axis carries little stress and contributes little to $J$, because $J$ weights area by $\rho^2$. For a hollow shaft with $d_i/d_o = k$ and the same outer diameter as a solid one, $J_h/J_s = 1 - k^4$ and $A_h/A_s = 1 - k^2$.

![Shear stress in solid and hollow circular shafts, rectangle torsion coefficients, and shear stress in a thin-walled tube with walls of different thickness](../../../scripts/plots/materials_torsion_shear_distribution/materials_torsion_shear_distribution.png)

The figure, from the [torsion script](../../../scripts/plots/materials_torsion_shear_distribution/), compares a solid shaft of 60 mm diameter with a hollow shaft of 70 mm outer and 50 mm inner diameter under the same torque of 3 kN m (top row). $J = 1.272 \times 10^6$ mm⁴ for the solid shaft and $1.744 \times 10^6$ mm⁴ for the hollow one, so the peak stresses are 70.7 MPa and 60.2 MPa. The hollow shaft is 15% less stressed and uses 1885 mm² of material instead of 2827 mm², 33% less. The stress grows linearly with radius in both, and the dotted extension shows that the material removed from the hollow shaft would have been stressed below 43 MPa.

## Power Transmission

A shaft turning at angular speed $\omega$ (rad/s) and transmitting torque $T$ transmits power

$$
P = T\omega = \frac{2\pi n T}{60}
$$

with $n$ in revolutions per minute. A solid shaft must then satisfy both a strength and a stiffness criterion:

```math
d \ge \left(\frac{16T}{\pi\tau_{\mathrm{allow}}}\right)^{1/3},
\qquad
\frac{T}{GJ} \le \left(\frac{d\phi}{dx}\right)_{\mathrm{allow}}
```

A motor delivers 50 kW at 1500 rpm. The torque is $`T = 60 \times 50\,000/(2\pi \times 1500) = 318.3`$ N m, and with $\tau_{\mathrm{allow}} = 80$ MPa

```math
d \ge \left(\frac{16 \times 318.3}{\pi \times 80 \times 10^6}\right)^{1/3} = 0.0273 \text{ m}
```

so a 30 mm shaft. For the same power the torque scales as $1/n$, so high-speed shafts are slender and speed reducers are placed as close to the driven machine as possible. Keyways, splines and shoulders raise the local stress (stress concentration factors of 1.5–3 in torsion), and real shafts also carry bending from gear and belt forces, so shaft design codes combine the two through a yield criterion and a fatigue check (see [Combined Loading](combined_loading.md) and [Fatigue](fatigue.md)).

## Statically Indeterminate Shafts

A shaft fixed against rotation at both ends, or two shafts coupled side by side, has more unknown torques than equilibrium equations. The procedure is the same as for axial bars (see [Axial Loading](axial_loading.md#statically-indeterminate-bars)):

1. Equilibrium: the reactions balance the applied torques.
2. Compatibility: the total twist between the fixed ends is zero, or coupled members share the same twist.
3. Torque–twist relation: $\phi_i = T_iL_i/(G_iJ_i)$ for each segment.
4. Solve for the torques, then compute stresses and rotations.

For a uniform shaft fixed at A and B with a torque $T_0$ applied at C, a distance $L_1$ from A and $L_2$ from B, equilibrium gives $T_A + T_B = T_0$ and compatibility $T_AL_1/(GJ) - T_BL_2/(GJ) = 0$, so

$$
T_A = T_0 \frac{L_2}{L_1 + L_2},
\qquad T_B = T_0 \frac{L_1}{L_1 + L_2}
$$

The shorter segment is stiffer and takes the larger share. For a composite shaft made of a tube shrunk onto a core, both twist by the same angle, so each part carries torque in proportion to its torsional stiffness $G_iJ_i$.

## Non-Circular Sections

When the section is not circular, the plane-section assumption fails: the cross-sections **warp** out of their plane, and the circular-shaft formulas no longer apply. Saint-Venant's theory of torsion, which allows free warping, gives the exact solution through a stress function that satisfies a Poisson equation over the section; the results for common shapes are summarized here. The shear stress is always tangent to the boundary, it is zero at outside corners, and its maximum occurs at the point of the boundary closest to the centroid.

### Solid Rectangle

For a rectangle with long side $a$ and short side $b$,

$$
\tau_{\max} = \frac{T}{\alpha a b^2},
\qquad \frac{d\phi}{dx} = \frac{T}{G\beta a b^3}
$$

so $J_t = \beta a b^3$. The maximum stress acts at the middle of the long sides. The coefficients follow from Saint-Venant's series solution (Timoshenko and Goodier); the torsion script evaluates the series and gives:

| $a/b$ | 1.0 | 1.5 | 2.0 | 3.0 | 4.0 | 6.0 | 10.0 | $\infty$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\alpha$ | 0.208 | 0.231 | 0.246 | 0.267 | 0.282 | 0.298 | 0.312 | 0.333 |
| $\beta$ | 0.141 | 0.196 | 0.229 | 0.263 | 0.281 | 0.298 | 0.312 | 0.333 |

Both tend to $1/3$ for a thin strip, which gives the thin open section formulas below. A steel bar of 50 mm by 25 mm ($a/b = 2$) under 500 N m has $\tau_{\max} = 500/(0.246 \times 0.05 \times 0.025^2) = 65.1$ MPa and twists $2.0^\circ$ per metre. A circular bar of the same area (39.9 mm diameter) would be stressed to 40.1 MPa: the circle is the most efficient solid section in torsion.

### Thin-Walled Closed Sections

A closed tube of arbitrary shape with wall thickness $t(s)$, where $s$ runs round the median line of the wall, is analysed through the **shear flow** $q = \tau t$ (N/m). Equilibrium of a small piece of wall cut by two longitudinal planes shows that $q$ is the same everywhere round the section. The torque of the shear flow about any point is $`T = \oint q\,r\,ds`$, where $r$ is the perpendicular distance from the point to the tangent of the median line, and $`\oint r\,ds = 2A_m`$ with $A_m$ the area enclosed by the median line. Therefore

$$
q = \frac{T}{2A_m},
\qquad \tau = \frac{T}{2A_m t}
$$

the **Bredt–Batho** formula. The stress is largest where the wall is thinnest. Equating the strain energy per unit length to the work of the torque gives the twist rate and the torsion constant

$$
\frac{d\phi}{dx} = \frac{T}{4A_m^2 G}\oint \frac{ds}{t},
\qquad J_t = \frac{4A_m^2}{\oint ds/t}
$$

The lower-right panel of the figure shows a rectangular tube with a median line of 100 mm by 50 mm ($A_m = 5000$ mm²) under 1 kN m. The shear flow is $q = 100$ N/mm, so the stress is 33.3 MPa in the 3 mm flanges, 20.0 MPa in the 5 mm web and 50.0 MPa in the 2 mm web. With $\oint ds/t = 2(100/3) + 50/5 + 50/2 = 101.7$ the twist rate is $0.728^\circ$ per metre for steel. Real tubes have stress concentrations at sharp inside corners, which generous corner radii reduce.

### Thin-Walled Open Sections

An open section (an angle, channel, I-beam or slit tube) made of thin walls of length $b_i$ and thickness $t_i$ behaves like a set of thin rectangles:

```math
J_t = \frac{1}{3}\sum_i b_i t_i^3,
\qquad \tau_{\max} = \frac{T\,t_{\max}}{J_t}
```

The shear stress now varies linearly across the wall thickness and changes sign at its middle, so the lever arm of the internal stresses is of the order of $t$ instead of the section size. Compare a circular tube of median radius 50 mm and wall 2 mm, closed and with a longitudinal slit, under 1 kN m. Closed: $\tau = T/(2\pi r^2 t) = 31.8$ MPa and $J_t = 2\pi r^3 t = 1.571 \times 10^{-6}$ m⁴. Slit: $J_t = \frac{1}{3}(2\pi r)t^3 = 8.38 \times 10^{-10}$ m⁴ and $\tau = 2387$ MPa. The slit makes the tube $3(r/t)^2 = 1875$ times more flexible and $3r/t = 75$ times more highly stressed. This is why torsion members are closed sections, and why open sections such as I-beams under torsion are designed with warping restraint (non-uniform torsion), which is beyond this note.

## Key Takeaways

- In a circular shaft $\tau = T\rho/J$ grows linearly from the axis; $`\phi = \int T/(GJ)\,dx`$.
- Hollow shafts carry more torque per unit mass; the inner material of a solid shaft is lightly stressed.
- Power, torque and speed are related by $P = T\omega$; check both stress and twist, as stiffness often governs.
- Indeterminate shafts share torque in proportion to $GJ/L$ of each path.
- Non-circular sections warp. Use $\alpha$ and $\beta$ for rectangles, $\tau = T/(2A_mt)$ for thin closed sections and $J_t = \frac{1}{3}\sum bt^3$ for thin open ones.
- Closing a thin section increases its torsional stiffness by orders of magnitude.

## Related Scripts

- [Torsional Shear Stress Distribution](../../../scripts/plots/materials_torsion_shear_distribution/): plots torsional shear stress in solid, hollow, rectangular and thin-walled closed sections.

## Exercises

**Exercise 1.** Check that a hollow shaft with $d_i/d_o = 0.8$ has 59% of the polar moment of a solid shaft with the same outer diameter but 36% of its mass. For the same torque, how do the maximum stresses compare, and what is the gain in torque capacity per unit mass?

<details>
<summary>Answer</summary>

$J_h/J_s = 1 - 0.8^4 = 0.590$ and $A_h/A_s = 1 - 0.8^2 = 0.360$.

For the same torque and outer radius $\tau \propto 1/J$, so the hollow shaft is stressed $1/0.590 = 1.69$ times more. For the same allowable stress its torque capacity per unit mass is $0.590/0.360 = 1.64$ times that of the solid shaft.

</details>

**Exercise 2.** The 30 mm shaft of the motor example ($T = 318.3$ N m, $G = 80$ GPa) is 1.2 m long. Find its angle of twist. If the twist must not exceed $1^\circ$ per metre, what diameter is needed?

<details>
<summary>Answer</summary>

$J = \pi(0.030)^4/32 = 7.95 \times 10^{-8}$ m⁴:

```math
\phi = \frac{TL}{GJ} = \frac{318.3 \times 1.2}{80 \times 10^9 \times 7.95 \times 10^{-8}} = 0.0600 \text{ rad} = 3.44^\circ
```

That is $2.87^\circ$ per metre, too much. For $1^\circ$ per metre $= 0.01745$ rad/m:

```math
J \ge \frac{318.3}{80 \times 10^9 \times 0.01745} = 2.28 \times 10^{-7} \text{ m}^4
\implies d \ge \left(\frac{32J}{\pi}\right)^{1/4} = 39.0 \text{ mm}
```

Stiffness, not strength, governs: use a 40 mm shaft.

</details>

**Exercise 3.** A solid 50 mm steel shaft ($G = 80$ GPa) is fixed at both ends. A torque $T_0 = 1.5$ kN m is applied 0.3 m from end A; the total length is 1.0 m. Find the end torques, the maximum shear stress in each segment and the rotation of the loaded section.

<details>
<summary>Answer</summary>

$T_A = T_0L_2/L = 1500 \times 0.7 = 1050$ N m and $T_B = 450$ N m.

With $16T/(\pi d^3)$ the stresses are 42.8 MPa in AC and 18.3 MPa in CB. With $J = 6.14 \times 10^{-7}$ m⁴,

```math
\phi_C = \frac{T_AL_1}{GJ} = \frac{1050 \times 0.3}{80 \times 10^9 \times 6.14 \times 10^{-7}} = 6.42 \times 10^{-3} \text{ rad} = 0.37^\circ
```

</details>

**Exercise 4.** A thin-walled square tube has a median-line side of 100 mm and a uniform wall of 4 mm. Find the shear stress under 3 kN m with the Bredt–Batho formula, and the twist rate for $G = 80$ GPa. By how much would the stress rise if one wall were only 2 mm thick?

<details>
<summary>Answer</summary>

$A_m = 0.1^2 = 0.01$ m² and $q = T/(2A_m) = 150$ kN/m:

```math
\tau = \frac{q}{t} = \frac{150\,000}{0.004} = 37.5 \text{ MPa},
\qquad
\frac{d\phi}{dx} = \frac{3000}{4 \times 0.01^2 \times 80 \times 10^9} \times \frac{0.4}{0.004} = 0.0094 \text{ rad/m} = 0.54^\circ/\text{m}
```

The shear flow is unchanged by the thin wall, so the stress there doubles to 75 MPa while the other three walls stay at 37.5 MPa.

</details>

**Exercise 5.** A shaft transmits 20 kW with an allowable shear stress of 60 MPa. Find the required solid diameter at 300 rpm and at 3000 rpm, and the required outer diameter at 300 rpm for a hollow shaft with $d_i/d_o = 0.75$. Compare the masses of the two 300 rpm shafts.

<details>
<summary>Answer</summary>

At 300 rpm, $`T = 20\,000/31.42 = 636.6`$ N m and $d = (16T/(\pi\tau))^{1/3} = 37.8$ mm. At 3000 rpm, $T = 63.7$ N m and $d = 17.5$ mm: ten times the speed, $10^{-1/3}$ times the diameter.

Hollow: $\tau_{\max} = 16T/[\pi d_o^3(1 - k^4)]$ with $k = 0.75$, $1 - k^4 = 0.684$, so $d_o = 37.8/0.684^{1/3} = 42.9$ mm and $d_i = 32.2$ mm. The area ratio is $42.9^2(1 - 0.5625)/37.8^2 = 0.56$: the hollow shaft weighs 44% less.

</details>

## References

- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Timoshenko, S. P., and Goodier, J. N., *Theory of Elasticity*, 3rd ed., McGraw-Hill, 1970.
- Young, W. C., and Budynas, R. G., *Roark's Formulas for Stress and Strain*, 7th ed., McGraw-Hill, 2002.
- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 11th ed., McGraw-Hill Education, 2020.
- Megson, T. H. G., *Aircraft Structures for Engineering Students*, 6th ed., Butterworth-Heinemann, 2017.
