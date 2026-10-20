# Combined Loading

Real members rarely carry one kind of load. A column carries its axial load off-centre, a drive shaft transmits torque while gear forces bend it, a pressurized pipe also hangs under its own weight, and an offshore riser feels internal pressure, tension and wave-induced bending at once. This note combines the stresses of the elementary cases (axial load, bending, torsion and internal pressure) by superposition, finds the critical point and its principal stresses, and judges that stress state against the yield and fracture criteria for ductile and brittle materials. The single-load stresses come from [Axial Loading](./axial_loading.md), [Torsion](./torsion.md) and [Bending of Beams](./beam_bending.md); the transformation to principal stresses and Mohr's circle are in [Stress and Strain](./stress_strain.md).

## Problem Statement

A member of known geometry and material carries several loads at once: an axial force $N$, bending moments $M_y$ and $M_z$, a torque $T$, shear forces, and possibly an internal pressure $p$. Given the internal forces at a cross-section (from free-body diagrams and the diagrams of [Shear Force and Bending Moment Diagrams](./shear_moment.md)) and the material's yield strength $\sigma_Y$, or its ultimate strengths $S_{ut}$ and $S_{uc}$ in tension and compression, find:

- the stress components $\sigma_x$, $\tau_{xy}$, $\tau_{xz}$ at the critical points of the section;
- the principal stresses $\sigma_1 \ge \sigma_2 \ge \sigma_3$ there;
- the safety factor $n$ against yielding or fracture, or the member size that gives a required $n$.

The material is linear elastic, deformations are small, and each load acting alone produces the stresses of elementary theory. Under these conditions stresses superpose:

```math
\sigma_x = \frac{N}{A} - \frac{M_z\,y}{I_z} + \frac{M_y\,z}{I_y},
\qquad \tau = \frac{T\rho}{J} + \frac{VQ}{It}
```

where $y$ and $z$ are measured from the centroid along the principal axes of the section, $M_y$ and $M_z$ are moment vectors along those axes by the right-hand rule ($M_z > 0$ is sagging for $y$ upward), and $\rho$ is the radius in a circular shaft. Failure is predicted by comparing an equivalent stress built from the principal stresses with a strength measured in a uniaxial test.

## Superposition and the Critical Point

Superposition requires that each load case is linear in its load and that the loads do not change the geometry on which the others act. It fails for slender columns, where an axial load multiplies the bending deflection (see [Buckling of Columns](./buckling.md#eccentric-loading-and-the-secant-formula)), and after yielding. The procedure for a member under combined loads is:

1. Find the internal forces $N$, $V_y$, $V_z$, $T$, $M_y$, $M_z$ at the section of interest.
2. Write the stress from each internal force separately and locate where each is largest: bending at the extreme fibres, torsion on the outer surface, transverse shear at the neutral axis.
3. Choose candidate critical points where the large contributions coincide, and add the stress components at each.
4. Find the principal stresses at each candidate point, with Mohr's circle or the transformation formulas.
5. Apply the failure criterion appropriate to the material and compute the safety factor.

## Eccentric Axial Load

A compressive load $P$ applied at the point $(e_y, e_z)$ of the section is statically equivalent to a centric load $P$ plus bending moments $P e_y$ and $P e_z$. With compressive stress negative, the normal stress is

```math
\sigma_x = -\frac{P}{A}\left(1 + \frac{e_y\,y}{r_z^2} + \frac{e_z\,z}{r_y^2}\right), \qquad r_z^2 = \frac{I_z}{A}, \quad r_y^2 = \frac{I_y}{A}
```

where $r_y$ and $r_z$ are the radii of gyration. The neutral axis is the line on which the bracket vanishes. It does not pass through the centroid, and it moves toward the centroid as the eccentricity grows.

### Kern of a Section

The kern (core) is the region of load positions for which the whole section stays in compression. This matters for materials with little tensile strength, such as masonry, unreinforced concrete and soil under a footing. For a rectangle $b \times h$ (with $h$ along $y$), the tensile corner $(y, z) = (-h/2, -b/2)$ stays in compression if

```math
\frac{|e_y|}{h/6} + \frac{|e_z|}{b/6} \le 1
```

so the kern is a rhombus with vertices at $e_y = \pm h/6$ on one axis and $e_z = \pm b/6$ on the other. On each axis alone this is the middle-third rule; a load with both eccentricities below one sixth of the side can still lie outside the rhombus. For a solid circle of diameter $d$ the kern is a concentric circle of diameter $d/4$.

### Example: Eccentrically Loaded Column

A short $300 \times 300$ mm concrete column carries 500 kN at $e_y = 40$ mm. With $`A = 90\,000`$ mm² and $I = 6.75 \times 10^8$ mm⁴:

```math
\sigma = -\frac{500\,000}{90\,000} \pm \frac{500\,000 \times 40 \times 150}{6.75 \times 10^8} = -5.56 \pm 4.44 \ \mathrm{MPa}
```

The extreme stresses are $-1.11$ MPa and $-10.0$ MPa, both compressive, since $e_y = 40$ mm is inside the kern ($h/6 = 50$ mm). If the same load is placed at $e_y = 30$ mm and $e_z = 25$ mm, each eccentricity is inside its middle third but $30/50 + 25/50 = 1.1 > 1$: the corner stress is $-5.56 + 3.33 + 2.78 = +0.56$ MPa, in tension.

## Bending and Torsion of Shafts

A solid circular shaft of diameter $d$ carrying a bending moment $M$ and a torque $T$ is critical at the outer fibre on the tension side of the bending, where

$$
\sigma_x = \frac{32 M}{\pi d^3},
\qquad \tau_{xy} = \frac{16 T}{\pi d^3}
$$

The other normal stresses are zero, so the principal stresses are

```math
\sigma_{1,2} = \frac{\sigma_x}{2} \pm \sqrt{\left(\frac{\sigma_x}{2}\right)^2 + \tau_{xy}^2}, \qquad \sigma_3 = 0
```

Because $\sigma_1$ and $\sigma_2$ have opposite signs, the maximum shear stress is the in-plane value, and the two common yield criteria of the next section reduce to

```math
\tau_{\max} = \frac{16}{\pi d^3}\sqrt{M^2 + T^2}, \qquad
\sigma_{\mathrm{vM}} = \sqrt{\sigma_x^2 + 3\tau_{xy}^2} = \frac{16}{\pi d^3}\sqrt{4M^2 + 3T^2}
```

An axial force adds $4N/(\pi d^2)$ to $\sigma_x$ before the combination. A rotating shaft under a steady bending moment sees a fully reversed bending stress at every surface point once per revolution, so shafts are designed against [Fatigue](./fatigue.md), and the static check here is the first-cycle yield check.

### Example: Shaft Under Bending and Torsion

A solid steel shaft with $d = 50$ mm carries $M = 1.2$ kN m and $T = 0.8$ kN m:

```math
\sigma_x = \frac{32 \times 1.2 \times 10^6}{\pi \times 50^3} = 97.8 \ \mathrm{MPa}, \qquad
\tau_{xy} = \frac{16 \times 0.8 \times 10^6}{\pi \times 50^3} = 32.6 \ \mathrm{MPa}
```

```math
\tau_{\max} = \sqrt{48.9^2 + 32.6^2} = 58.8 \ \mathrm{MPa}, \qquad
\sigma_{\mathrm{vM}} = \sqrt{97.8^2 + 3(32.6)^2} = 112.9 \ \mathrm{MPa}
```

The principal stresses are $\sigma_1 = 107.7$ MPa and $\sigma_2 = -9.9$ MPa (point A in the failure-envelope figure below).

## Thin-Walled Pressure Vessels

A vessel is thin-walled when its wall thickness $t$ is small compared with its radius $r$, conventionally $r/t \ge 10$. The membrane stresses are then nearly uniform through the wall and follow from free-body diagrams.

For a closed cylinder under internal gauge pressure $p$, cutting a length $\ell$ along a diameter balances the pressure force $2pr\ell$ on the projected area against the hoop force $2\sigma_h t \ell$ in the two cut walls. Cutting across the axis balances $p\pi r^2$ on the end against $`\sigma_l\,2\pi r t`$ in the wall:

$$
\sigma_h = \frac{p r}{t},
\qquad \sigma_l = \frac{p r}{2t}
$$

For a sphere, every diametral cut is the same and $\sigma_1 = \sigma_2 = pr/(2t)$, so a spherical vessel needs half the wall thickness of a cylinder of the same radius. In the cylinder, the hoop stress governs and longitudinal seams are the critical welds.

The radial stress varies from $-p$ at the inner surface to zero at the outer surface, so it is a fraction $t/r$ of the hoop stress and is neglected in membrane theory. At the outer surface the principal stresses of a cylinder are $\sigma_h$, $\sigma_l$ and $0$, so the absolute maximum shear stress is $\sigma_h/2 = pr/(2t)$, not the in-plane value $(\sigma_h - \sigma_l)/2 = pr/(4t)$. Thick-walled vessels, with $r/t$ below about 10, need the Lamé solution, in which the hoop stress is largest at the bore.

### Example: Cylinder with Pressure and Axial Load

A cylindrical tank with $r = 400$ mm and $t = 8$ mm holds $p = 2$ MPa and is also pulled by an axial force $F = 300$ kN:

```math
\sigma_h = \frac{2 \times 400}{8} = 100 \ \mathrm{MPa}, \qquad
\sigma_l = \frac{2 \times 400}{2 \times 8} + \frac{300\,000}{2\pi \times 400 \times 8} = 50 + 14.9 = 64.9 \ \mathrm{MPa}
```

Neither load produces shear on these planes, so $\sigma_h$ and $\sigma_l$ are principal stresses (point B in the figure). A torque $T$ on the same tank adds a shear $\tau = T/(2\pi r^2 t)$; for $T = 200$ kN m this is 24.9 MPa, and the principal stresses become 110.3 MPa and 39.7 MPa.

## Failure Criteria

A uniaxial tensile test gives one number, the yield strength $\sigma_Y$ or the ultimate strength $S_{ut}$. A failure criterion predicts failure under a multiaxial stress state from that number. Which criterion applies depends on how the material fails: ductile metals yield by shear slip, brittle materials fracture from the largest tensile stress acting on a flaw. All criteria are written in principal stresses so that they do not depend on the choice of axes. In plane stress one principal stress is zero, and it must be included: below, $\sigma_1$ and $\sigma_2$ are the two in-plane principal stresses in any order and $\sigma_3 = 0$.

### Maximum Shear Stress (Tresca)

Yield starts when the largest shear stress reaches its value in the tensile test at yield, $\sigma_Y/2$:

```math
\tau_{\max} = \frac{1}{2}\max\left(|\sigma_1 - \sigma_2|,\ |\sigma_1|,\ |\sigma_2|\right) = \frac{\sigma_Y}{2n}
```

In the $\sigma_1$–$`\sigma_2`$ plane the yield surface is a hexagon. Tresca predicts a shear yield strength $`\tau_Y = 0.5\,\sigma_Y`$.

### Distortion Energy (von Mises)

Yield starts when the strain energy of distortion (the part of the strain energy not associated with volume change) reaches its value at tensile yield. The equivalent stress is

```math
\sigma_{\mathrm{vM}} = \sqrt{\frac{(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2}{2}} = \frac{\sigma_Y}{n}
```

which in plane stress is $\sqrt{\sigma_1^2 - \sigma_1\sigma_2 + \sigma_2^2}$, an ellipse in the $\sigma_1$–$`\sigma_2`$ plane that circumscribes the Tresca hexagon, and in terms of components $\sqrt{\sigma_x^2 - \sigma_x\sigma_y + \sigma_y^2 + 3\tau_{xy}^2}$. It is equivalent to a critical octahedral shear stress, predicts $`\tau_Y = \sigma_Y/\sqrt{3} = 0.577\,\sigma_Y`$, and fits tests on ductile metals better than Tresca. It is the equivalent stress reported by finite-element codes. Tresca is never less conservative, and the two differ by at most 15%, in pure shear.

### Maximum Normal Stress (Rankine) for Brittle Materials

Fracture occurs when a principal stress reaches the ultimate tensile strength $S_{ut}$ or the ultimate compressive strength $-S_{uc}$:

$$
-S_{uc} \le \sigma_1, \sigma_2 \le S_{ut}
$$

The envelope is a rectangle. It is accurate when both principal stresses are tensile, but in the quadrant of mixed signs it overestimates the strength of brittle materials. The Coulomb–Mohr criterion replaces the rectangle there by the straight line

```math
\frac{\sigma_1}{S_{ut}} - \frac{\sigma_2}{S_{uc}} = \frac{1}{n}, \qquad \sigma_1 \ge 0 \ge \sigma_2
```

which agrees better with tests on cast iron. Budynas and Nisbett recommend Coulomb–Mohr or its modified form for brittle design.

### Comparing the Criteria

![Tresca and von Mises yield envelopes for a steel, and maximum-normal-stress and Coulomb-Mohr fracture envelopes for a grey cast iron, with load points and radial load lines](../../../scripts/plots/beams_failure_envelopes/beams_failure_envelopes.png)

Each load point is joined to the origin by a radial load line, along which all stresses grow in proportion; the safety factor of a criterion is the ratio of the distance to that criterion's envelope (the crosses) to the distance to the point. The three ductile points are the shaft and the tank of the examples above and a pure shear of 120 MPa:

| Point | $\sigma_1$, $\sigma_2$ (MPa) | $n$ Tresca | $n$ von Mises |
| --- | --- | --- | --- |
| A, shaft | 107.7, $-9.9$ | 2.13 | 2.21 |
| B, tank | 100.0, 64.9 | 2.50 | 2.84 |
| C, pure shear | 120, $-120$ | 1.04 | 1.20 |

with $\sigma_Y = 250$ MPa. For point B, using only the in-plane shear $(\sigma_h - \sigma_l)/2 = 17.5$ MPa would give a Tresca safety factor of 7.1 instead of 2.5. For a grey cast iron with $S_{ut} = 214$ MPa and $S_{uc} = 752$ MPa, pure shear of 120 MPa has $n = 1.78$ by maximum normal stress but $n = 1.39$ by Coulomb–Mohr, and a state of 50 MPa tension with 400 MPa compression has 1.88 and 1.31. The maximum normal stress criterion is unsafe for brittle parts in torsion or in combined tension and compression.

| Criterion | Material | Envelope | Shear strength predicted |
| --- | --- | --- | --- |
| Tresca | Ductile | Hexagon | $`0.5\,\sigma_Y`$ |
| von Mises | Ductile | Ellipse | $`0.577\,\sigma_Y`$ |
| Maximum normal stress | Brittle | Rectangle | $S_{ut}$ |
| Coulomb–Mohr | Brittle | Irregular hexagon | $S_{ut}S_{uc}/(S_{ut} + S_{uc})$ |

## Common Mistakes

- Adding stresses from different points of the section, for example the bending stress at the extreme fibre and the transverse shear stress at the neutral axis.
- Omitting the zero principal stress in Tresca for plane stress when both in-plane principal stresses have the same sign.
- Treating the kern of a rectangle as a rectangle; it is a rhombus.
- Applying a ductile yield criterion to a brittle material, or the maximum normal stress criterion where the principal stresses have opposite signs.
- Using thin-wall formulas when $r/t$ is below about 10.
- Checking only static strength for a rotating shaft, which fails in [Fatigue](./fatigue.md).

## Key Takeaways

- In the linear elastic range, stresses from axial load, bending, torsion and pressure add; principal stresses do not.
- A load outside the kern puts part of the section in tension; the kern of a rectangle is a rhombus with semi-diagonals $h/6$ and $b/6$.
- For a solid shaft, $\tau_{\max} = 16\sqrt{M^2 + T^2}/(\pi d^3)$ and $\sigma_{\mathrm{vM}} = 16\sqrt{4M^2 + 3T^2}/(\pi d^3)$.
- In a thin cylinder, $\sigma_h = pr/t$ is twice $\sigma_l = pr/(2t)$, and the absolute maximum shear stress is $pr/(2t)$.
- Use von Mises or Tresca for ductile materials and Coulomb–Mohr for brittle ones; the safety factor is measured along the radial load line.

## Related Scripts

- [Failure Envelopes in the Principal-Stress Plane](../../../scripts/plots/beams_failure_envelopes/): draws the Tresca, von Mises, maximum-normal-stress and Coulomb–Mohr envelopes in the plane-stress principal-stress plane and computes the safety factor of example load points under each criterion.
- [Fatigue: S–N Curve, Haigh Diagram and Miner's Rule](../../../scripts/plots/fatigue_sn_and_goodman/): builds the S–N curve of a machined steel shaft from Marin factors, draws the Goodman, Gerber and Soderberg lines with an operating point, and sums the Miner damage of a rainflow-counted random stress history.
- [Mohr's Circle for Plane Stress](../../../scripts/algorithms/materials_mohr_circle/): transforms a 2D plane-stress state and draws Mohr's circle with the given, rotated, principal and maximum-shear stress elements.
- [Torsional Shear Stress Distribution](../../../scripts/plots/materials_torsion_shear_distribution/): plots torsional shear stress in solid, hollow, rectangular and thin-walled closed sections.

## Exercises

**Exercise 1.** The eccentricity of the 500 kN load on the $300 \times 300$ mm column of the example is increased to 60 mm along one axis. Find the extreme normal stresses. Is any part of the section in tension?

<details>
<summary>Answer</summary>

```math
\sigma = -\frac{500\,000}{90\,000} \pm \frac{500\,000 \times 60 \times 150}{6.75 \times 10^8} = -5.56 \pm 6.67 \ \mathrm{MPa}
```

The extremes are $+1.11$ MPa (tension) and $-12.2$ MPa. The load is outside the kern ($e > h/6 = 50$ mm), so one face is in tension, which matters for unreinforced concrete or masonry.

</details>

**Exercise 2.** At a point, $\sigma_x = 80$ MPa, $\sigma_y = -40$ MPa and $\tau_{xy} = 30$ MPa. Find the principal stresses, the maximum shear stress and the principal angle, and the von Mises stress.

<details>
<summary>Answer</summary>

The centre and radius of Mohr's circle are

```math
C = \frac{80 - 40}{2} = 20 \ \mathrm{MPa}, \qquad R = \sqrt{60^2 + 30^2} = 67.1 \ \mathrm{MPa}
```

so $\sigma_1 = 87.1$ MPa and $\sigma_2 = -47.1$ MPa, with $\tan 2\theta_p = 60/120$ and $\theta_p = 13.3^\circ$. The principal stresses have opposite signs, so the absolute maximum shear stress is the in-plane value $R = 67.1$ MPa. The von Mises stress is $\sqrt{87.1^2 + 87.1(47.1) + 47.1^2} = 117.9$ MPa.

</details>

**Exercise 3.** Size a solid shaft for $M = 1.2$ kN m and $T = 0.8$ kN m in a steel with $\sigma_Y = 350$ MPa and a safety factor of 2, using (a) von Mises and (b) Tresca.

<details>
<summary>Answer</summary>

(a) With an allowable equivalent stress of 175 MPa:

```math
d = \left(\frac{16\sqrt{4(1200)^2 + 3(800)^2}}{\pi \times 175 \times 10^6}\right)^{1/3} = 43.2 \ \mathrm{mm}
```

(b) With an allowable shear stress of 87.5 MPa, $d = (16\sqrt{1200^2 + 800^2}/(\pi \times 87.5 \times 10^6))^{1/3} = 43.8$ mm.

Tresca is slightly more conservative; a standard 45 mm shaft satisfies both. A real shaft must then be checked for fatigue, which usually governs.

</details>

**Exercise 4.** A cylindrical tank of radius 1 m holds gas at 1.5 MPa, and the wall's allowable stress is 150 MPa. Find the wall thickness for the cylinder and for hemispherical end caps of the same radius, and check the thin-wall assumption.

<details>
<summary>Answer</summary>

For the cylinder the hoop stress governs: $t = pr/\sigma_{\mathrm{allow}} = 1.5(1000)/150 = 10$ mm. For the caps, $t = pr/(2\sigma_{\mathrm{allow}}) = 5$ mm.

$r/t = 100$ and 200, both well above 10, so membrane theory applies. In practice the heads are made thicker than this near the junction, where the cylinder and hemisphere expand by different amounts and local bending stresses arise.

</details>

**Exercise 5.** A grey cast iron shaft ($S_{ut} = 214$ MPa, $S_{uc} = 752$ MPa) of diameter 40 mm carries a torque only. Find the torque at fracture predicted by the maximum normal stress and Coulomb–Mohr criteria, and say on which plane the fracture surface forms.

<details>
<summary>Answer</summary>

Pure shear $\tau$ gives $\sigma_1 = \tau$, $\sigma_2 = -\tau$.

Maximum normal stress: $\tau = S_{ut} = 214$ MPa. Coulomb–Mohr: $\tau/214 + \tau/752 = 1$, so $\tau = 166.6$ MPa.

With $T = \pi d^3 \tau/16$ and $`\pi(40)^3/16 = 12\,566`$ mm³, the torques are 2.69 kN m and 2.09 kN m. Coulomb–Mohr is 22% lower and is the one to design with.

The fracture runs perpendicular to $\sigma_1$, on a helix at $45^\circ$ to the shaft axis, which is the familiar spiral fracture of a brittle bar twisted to failure (a ductile shaft fails instead on a plane perpendicular to the axis, the plane of maximum shear).

</details>

## References

- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 11th ed., McGraw-Hill Education, 2020.
- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Young, W. C., Budynas, R. G., and Sadegh, A. M., *Roark's Formulas for Stress and Strain*, 8th ed., McGraw-Hill, 2012.
- Dowling, N. E., *Mechanical Behavior of Materials*, 4th ed., Pearson, 2013.
