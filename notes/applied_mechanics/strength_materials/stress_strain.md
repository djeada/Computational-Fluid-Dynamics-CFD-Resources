# Stress and Strain

Stress measures how internal force is distributed over the planes through a point of a loaded body, and strain measures how the material around that point is stretched and distorted. This note defines both as tensors, relates them through Hooke's law for an isotropic elastic material, reduces them to plane stress and plane strain, and develops stress transformation, principal stresses and Mohr's circle. It ends with thermal strain, stress concentrations around holes and the factor of safety. The other strength-of-materials notes (axial loading, torsion, bending) build on these definitions by assuming how the strain varies over a cross-section; finite element and CFD-coupled structural solvers compute the same tensors directly at every point.

## Problem Statement

A body occupies a region $V$ with boundary $S$. It is made of a homogeneous, isotropic, linear elastic material with Young's modulus $E$, Poisson's ratio $\nu$ and thermal expansion coefficient $\alpha$. It carries body forces $\mathbf{b}$ (N/m³), surface tractions $\bar{\mathbf{t}}$ (Pa) on part of $S$ and prescribed displacements on the rest, and it may undergo a temperature change $\Delta T$. The unknowns at every point are the displacement $\mathbf{u}$ (m), the strain tensor $\boldsymbol{\varepsilon}$ and the stress tensor $\boldsymbol{\sigma}$ (Pa). With small displacements and strains they satisfy

```math
\frac{\partial \sigma_{ij}}{\partial x_j} + b_i = 0,
\qquad
\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right),
\qquad
\varepsilon_{ij} = \frac{1 + \nu}{E}\sigma_{ij} - \frac{\nu}{E}\sigma_{kk}\delta_{ij} + \alpha\,\Delta T\,\delta_{ij}
```

(equilibrium, kinematics and the constitutive law, with summation over repeated indices). Solving this boundary value problem in general needs the theory of elasticity or a numerical method such as the [finite element method](../../numerical/fem/intro.md). This note treats the local questions that every such solution leads to: given the stress components at a point, find the stress on any plane through it, the principal stresses and directions, the maximum shear stress, the strains, and whether the material is safe.

## Traction and the Cauchy Stress Tensor

Cut the body by a plane through a point $P$ with unit normal $\mathbf{n}$. The material on the side towards which $\mathbf{n}$ points exerts a force $\Delta\mathbf{F}$ on a small area $\Delta A$ around $P$. The **traction vector** is

$$
\mathbf{t}^{(\mathbf{n})} = \lim_{\Delta A \to 0} \frac{\Delta \mathbf{F}}{\Delta A}
$$

It depends on the orientation of the plane as well as on the point. Cauchy showed, from the equilibrium of a small tetrahedron whose faces are the cutting plane and three coordinate planes, that the traction on every plane is a linear function of $\mathbf{n}$:

$$
t_i = \sigma_{ji} n_j,
\qquad \mathbf{t} = \boldsymbol{\sigma}^{\mathsf{T}}\mathbf{n}
$$

The nine components $\sigma_{ij}$ form the **Cauchy stress tensor**. $\sigma_{ij}$ is the component in direction $j$ of the traction on the face whose outward normal is $+x_i$. The diagonal components $\sigma_{xx}, \sigma_{yy}, \sigma_{zz}$ (written $\sigma_x, \sigma_y, \sigma_z$) are normal stresses; the off-diagonal ones $\tau_{xy}, \tau_{yz}, \tau_{zx}$ are shear stresses. Stress has units of pressure; in strength of materials the convenient unit is $1\ \mathrm{MPa} = 1\ \mathrm{N/mm^2}$.

Moment equilibrium of a small cube about its centre shows that the shear stresses on perpendicular faces are equal, $\tau_{xy} = \tau_{yx}$, $\tau_{yz} = \tau_{zy}$, $\tau_{zx} = \tau_{xz}$. The tensor is therefore symmetric, has six independent components, and $\mathbf{t} = \boldsymbol{\sigma}\mathbf{n}$. The normal and shear stress on the plane are

$$
\sigma_n = \mathbf{n}\cdot\boldsymbol{\sigma}\mathbf{n},
\qquad \tau_n = \sqrt{|\mathbf{t}|^2 - \sigma_n^2}
$$

The sign convention follows from the definition: a normal stress is positive in tension and negative in compression. A shear stress is positive when it acts in the positive coordinate direction on a face with an outward normal in a positive coordinate direction (or negative on negative), so a positive $\tau_{xy}$ points in $+y$ on the $+x$ face and in $+x$ on the $+y$ face.

### Average Stress in Simple Members

When a member is loaded so that the stress over a section is nearly uniform, the stress is the force divided by the area. An axial force $N$ on a cross-section of area $A$ gives the normal stress $\sigma = N/A$; a shear force $V$ carried by an area $A$ gives the average shear stress $\tau_{\mathrm{avg}} = V/A$. The second is only an average: in a beam the shear stress varies over the depth (see [Shear and Moment Diagrams](shear_moment.md) and [Bending of Beams](beam_bending.md)), and over a solid circular section it peaks at $4/3$ of the average.

A steel rod of diameter 20 mm and length 2 m carries a tensile force of 50 kN. The area is $A = \pi(20)^2/4 = 314.2$ mm², so $`\sigma = 50\,000/314.2 = 159.2`$ MPa. With $E = 200$ GPa and $\nu = 0.3$ the axial strain is $\varepsilon = \sigma/E = 7.96 \times 10^{-4}$, the elongation $\varepsilon L = 1.59$ mm and the lateral strain $-\nu\varepsilon = -2.39 \times 10^{-4}$, which reduces the diameter by 4.8 μm. A 12 mm bolt carrying 15 kN across one shear plane has $A = 113.1$ mm² and $\tau_{\mathrm{avg}} = 132.6$ MPa.

## Strain

Let $\mathbf{u}(\mathbf{x}) = (u, v, w)$ be the displacement of the material point at $\mathbf{x}$. The **normal strain** in direction $x$ is the change of length per unit length of a short fibre along $x$, and the **shear strain** $\gamma_{xy}$ is the decrease of the right angle between fibres along $x$ and $y$, in radians. For displacement gradients much smaller than one,

$$
\varepsilon_x = \frac{\partial u}{\partial x}, \quad
\varepsilon_y = \frac{\partial v}{\partial y}, \quad
\varepsilon_z = \frac{\partial w}{\partial z}, \quad
\gamma_{xy} = \frac{\partial u}{\partial y} + \frac{\partial v}{\partial x}, \quad
\gamma_{yz} = \frac{\partial v}{\partial z} + \frac{\partial w}{\partial y}, \quad
\gamma_{zx} = \frac{\partial w}{\partial x} + \frac{\partial u}{\partial z}
$$

The tensor components are $\varepsilon_{xx} = \varepsilon_x$ and $\varepsilon_{xy} = \gamma_{xy}/2$; the factor of two between the engineering shear strain $\gamma$ and the tensor component is a common source of errors. The strain tensor transforms exactly like the stress tensor (with $\gamma/2$ in place of $\tau$), so the transformation formulas and Mohr's circle below apply to strain as well, which is how strain-gauge rosettes are evaluated.

The relative change of volume is the **volumetric strain** $\varepsilon_v = \Delta V/V = \varepsilon_x + \varepsilon_y + \varepsilon_z$, to first order and for any material. A uniform strain over a length $L_0$ gives the familiar $\varepsilon = \Delta L/L_0$. Strains in metal structures in service are of order $10^{-3}$, so the small-strain theory is accurate; for large plastic strains see the true strain in [Mechanical Properties of Materials](material_properties.md).

## Generalized Hooke's Law

For an isotropic linear elastic material, a uniaxial stress $\sigma_x$ produces $\varepsilon_x = \sigma_x/E$ and lateral strains $\varepsilon_y = \varepsilon_z = -\nu\sigma_x/E$, where **Poisson's ratio** $\nu = -\varepsilon_{\mathrm{lateral}}/\varepsilon_{\mathrm{axial}}$. Superposing the three normal stresses, adding the shear response and a free thermal strain gives

```math
\varepsilon_x = \frac{1}{E}\left[\sigma_x - \nu(\sigma_y + \sigma_z)\right] + \alpha\,\Delta T,
\qquad
\varepsilon_y = \frac{1}{E}\left[\sigma_y - \nu(\sigma_z + \sigma_x)\right] + \alpha\,\Delta T,
\qquad
\varepsilon_z = \frac{1}{E}\left[\sigma_z - \nu(\sigma_x + \sigma_y)\right] + \alpha\,\Delta T
```

$$
\gamma_{xy} = \frac{\tau_{xy}}{G},
\qquad \gamma_{yz} = \frac{\tau_{yz}}{G},
\qquad \gamma_{zx} = \frac{\tau_{zx}}{G}
$$

Normal stresses cause no shear strain and shear stresses cause no normal strain in an isotropic material. Only two of the elastic constants are independent. Applying the transformation to a state of pure shear (which is a tension–compression pair at $45^\circ$) gives the **shear modulus**

$$
G = \frac{E}{2(1 + \nu)}
$$

and summing the three normal strains under a hydrostatic stress $\sigma_x = \sigma_y = \sigma_z = -p$ gives the **bulk modulus** $K = -p/\varepsilon_v = E/[3(1 - 2\nu)]$. A positive $K$ requires $\nu < 0.5$; $\nu \to 0.5$ is the incompressible limit approached by rubber. Typical values are $\nu \approx 0.3$ for steels, 0.33 for aluminium alloys, 0.2 for concrete and close to 0 for cork; the full property table is in [Mechanical Properties of Materials](material_properties.md).

Inverting the relations gives the stresses from the strains, which is the form a finite element code uses:

```math
\sigma_{ij} = \lambda\,\varepsilon_{kk}\,\delta_{ij} + 2G\,\varepsilon_{ij} - (3\lambda + 2G)\,\alpha\,\Delta T\,\delta_{ij},
\qquad
\lambda = \frac{E\nu}{(1 + \nu)(1 - 2\nu)}
```

The elastic strain energy stored per unit volume is $u = \frac{1}{2}\sigma_{ij}\varepsilon_{ij}$; for uniaxial stress $u = \sigma^2/(2E)$ and for pure shear $u = \tau^2/(2G)$.

## Plane Stress and Plane Strain

Two-dimensional idealizations cover most practical cases.

|  | Plane stress | Plane strain |
| --- | --- | --- |
| Geometry | thin plate loaded in its own plane, free surfaces $z = \pm t/2$ | long prismatic body loaded uniformly along $z$ (dam, tunnel lining, retaining wall) |
| Assumption | $\sigma_z = \tau_{xz} = \tau_{yz} = 0$ | $\varepsilon_z = \gamma_{xz} = \gamma_{yz} = 0$ |
| Out-of-plane result | $\varepsilon_z = -\nu(\sigma_x + \sigma_y)/E$ | $\sigma_z = \nu(\sigma_x + \sigma_y)$ |
| In-plane law | $\sigma_x = \dfrac{E}{1 - \nu^2}(\varepsilon_x + \nu\varepsilon_y)$ | $\sigma_x = \dfrac{E(1 - \nu)}{(1 + \nu)(1 - 2\nu)}\left(\varepsilon_x + \dfrac{\nu}{1 - \nu}\varepsilon_y\right)$ |

In both cases $\tau_{xy} = G\gamma_{xy}$ and the $y$ equation follows by exchanging $x$ and $y$. A plane-stress solution becomes a plane-strain solution if $E$ is replaced by $E/(1 - \nu^2)$ and $\nu$ by $\nu/(1 - \nu)$. Plane strain is stiffer and, because $\sigma_z \neq 0$, it changes the yield check: a thick cracked plate yields less readily at the crack tip than a thin one, which is why fracture toughness is measured in plane strain.

## Stress Transformation in Two Dimensions

In plane stress the state at a point is fully described by $\sigma_x$, $\sigma_y$ and $\tau_{xy}$. Rotate the axes counterclockwise by an angle $\theta$ to $x'$, $y'$. Equilibrium of a triangular wedge cut by the plane whose normal is $x'$ gives the stresses on that plane:

```math
\sigma_{x'} = \frac{\sigma_x + \sigma_y}{2} + \frac{\sigma_x - \sigma_y}{2}\cos 2\theta + \tau_{xy}\sin 2\theta,
\qquad
\tau_{x'y'} = -\frac{\sigma_x - \sigma_y}{2}\sin 2\theta + \tau_{xy}\cos 2\theta
```

and $\sigma_{y'}$ is $\sigma_{x'}$ evaluated at $\theta + 90^\circ$. The same result is $\boldsymbol{\sigma}' = \mathbf{R}\boldsymbol{\sigma}\mathbf{R}^{\mathsf{T}}$ with the rotation matrix $\mathbf{R}$, which shows that

$$
\sigma_{x'} + \sigma_{y'} = \sigma_x + \sigma_y,
\qquad \sigma_{x'}\sigma_{y'} - \tau_{x'y'}^2 = \sigma_x\sigma_y - \tau_{xy}^2
$$

are invariant: the trace and the determinant of a tensor do not depend on the axes.

### Principal Stresses and Maximum Shear

Setting $d\sigma_{x'}/d\theta = 0$ gives the same condition as $\tau_{x'y'} = 0$:

$$
\tan 2\theta_p = \frac{2\tau_{xy}}{\sigma_x - \sigma_y}
$$

The two solutions, $90^\circ$ apart, are the **principal directions**. The planes normal to them carry no shear, and their normal stresses are the **principal stresses**

```math
\sigma_{1,2} = C \pm R,
\qquad
C = \frac{\sigma_x + \sigma_y}{2},
\qquad
R = \sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}
```

with $\sigma_1 \ge \sigma_2$. They are the eigenvalues of the $2 \times 2$ stress matrix and the principal directions are its eigenvectors. To decide which root of the tangent belongs to $\sigma_1$, either substitute it into $\sigma_{x'}$ or use $\theta_{p1} = \frac{1}{2}\mathrm{atan2}(2\tau_{xy}, \sigma_x - \sigma_y)$.

The shear stress $\tau_{x'y'}$ is extreme on planes at $45^\circ$ to the principal planes, where it equals $\pm R$ and the normal stress on both faces equals $C$. $R$ is the **maximum in-plane shear stress**. In three dimensions the stress tensor has three principal stresses, the roots of $\det(\boldsymbol{\sigma} - \sigma\mathbf{I}) = 0$; in plane stress the third is $\sigma_z = 0$. The absolute maximum shear stress is half the difference between the largest and smallest of the three:

$$
\tau_{\mathrm{abs}} = \frac{\sigma_{\max} - \sigma_{\min}}{2}
$$

If $\sigma_1$ and $\sigma_2$ have opposite signs, $\tau_{\mathrm{abs}} = R$. If they have the same sign, the largest shear acts on a plane inclined to the $z$ axis and equals $|\sigma_1|/2$ or $|\sigma_2|/2$, larger than $R$. Thin-walled pressure vessels are the standard example: hoop and axial stresses are both tensile, and the out-of-plane shear governs.

## Mohr's Circle

Eliminating $\theta$ from the two transformation equations gives

$$
(\sigma_{x'} - C)^2 + \tau_{x'y'}^2 = R^2
$$

so the stress on every plane through the point lies on a circle in the $(\sigma, \tau)$ plane with centre $(C, 0)$ and radius $R$. A plane rotated by $\theta$ on the element corresponds to a point rotated by $2\theta$ on the circle. In this note $\sigma$ is plotted to the right and $\tau$ downward, so that both rotations have the same sense (the convention used by Hibbeler; texts that plot $\tau$ upward reverse the sense on the circle). The construction is:

1. Plot the point $X = (\sigma_x, \tau_{xy})$, which represents the $x$ face, and the point $Y = (\sigma_y, -\tau_{xy})$, which represents the $y$ face.
2. Join them. The line crosses the $\sigma$ axis at the centre $C$, and the distance $CX$ is the radius $R$.
3. Draw the circle. Its intersections with the $\sigma$ axis are $\sigma_1$ and $\sigma_2$; its top and bottom points are the maximum-shear planes, with normal stress $C$.
4. The angle from $CX$ to the $\sigma_1$ point is $2\theta_p$. Rotate the element by $\theta_p$ in the same sense to align it with the principal directions.
5. For a plane at angle $\theta$, rotate the diameter $XY$ by $2\theta$ in the same sense; the end points $X'$ and $Y'$ give the stresses on the rotated element.

![Mohr's circle for sigma_x = 80 MPa, sigma_y = -40 MPa, tau_xy = 50 MPa with the given, rotated, principal and maximum-shear elements](../../../scripts/algorithms/materials_mohr_circle/materials_mohr_circle.png)

The figure was produced by the [Mohr's circle script](../../../scripts/algorithms/materials_mohr_circle/) for $\sigma_x = 80$ MPa, $\sigma_y = -40$ MPa and $\tau_{xy} = 50$ MPa. The centre is $C = 20$ MPa and the radius $R = \sqrt{60^2 + 50^2} = 78.1$ MPa, so $\sigma_1 = 98.1$ MPa and $\sigma_2 = -58.1$ MPa. $X$ lies below the axis, and turning $CX$ counterclockwise by $2\theta_p = \arctan(100/120) = 39.8^\circ$ reaches $\sigma_1$: the principal element is rotated $19.9^\circ$ counterclockwise. The maximum-shear element is rotated $45^\circ$ clockwise from it, to $-25.1^\circ$, and carries $\tau = 78.1$ MPa with $\sigma = 20$ MPa on all four faces. For $\theta = 30^\circ$ the formulas give $\sigma_{x'} = 20 + 60\cos 60^\circ + 50\sin 60^\circ = 93.3$ MPa, $\sigma_{y'} = -53.3$ MPa and $\tau_{x'y'} = -60\sin 60^\circ + 50\cos 60^\circ = -27.0$ MPa, the point $X'$ on the circle. Because $\sigma_1$ and $\sigma_2$ have opposite signs, the absolute maximum shear stress equals $R$.

## Yield Criteria and the Factor of Safety

A tensile test gives one strength value for one stress state. To compare a general state with it, a yield criterion reduces the principal stresses to one equivalent stress. For ductile metals two criteria are standard:

```math
\text{Tresca:}\quad \sigma_{\max} - \sigma_{\min} \le \sigma_Y,
\qquad
\text{von Mises:}\quad \sigma_{\mathrm{vM}} = \sqrt{\tfrac{1}{2}\left[(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2\right]} \le \sigma_Y
```

where $\sigma_Y$ is the tensile yield strength. Tresca limits the absolute maximum shear stress to $\sigma_Y/2$; von Mises limits the distortional strain energy and is slightly less conservative (by at most about 15%, in pure shear). In plane stress $\sigma_{\mathrm{vM}} = \sqrt{\sigma_x^2 - \sigma_x\sigma_y + \sigma_y^2 + 3\tau_{xy}^2}$. The application of these criteria to shafts and beams under combined loads is in [Combined Loading](combined_loading.md).

The **factor of safety** is the ratio of the capacity to the demand, $n = \sigma_Y/\sigma_{\mathrm{eq}}$ for yielding, or more generally failure load divided by working load. A design is accepted if $n$ exceeds a required value, or equivalently if the working stress stays below the allowable stress $\sigma_{\mathrm{allow}} = \sigma_Y/n$ (or $\sigma_u/n$ for brittle materials). The required $n$ reflects the uncertainty in loads, material properties, analysis and the consequence of failure; machine design texts quote values from about 1.25–1.5 for well-characterized materials and loads up to 3–4 for brittle materials or poorly known loads. Structural codes instead apply separate partial factors to loads and to resistances (limit state design). Fatigue, buckling and stress concentrations each require their own check: a factor of safety against yield says nothing about a column that buckles elastically (see [Buckling and Stability](buckling.md)) or a shaft that fails by fatigue (see [Fatigue](fatigue.md)).

## Thermal Strain and Stress

A temperature change $\Delta T$ produces the free strain $`\varepsilon_T = \alpha\,\Delta T`$ in every direction and no shear strain. Typical coefficients are $12 \times 10^{-6}$ K⁻¹ for steel, $23 \times 10^{-6}$ K⁻¹ for aluminium and $10 \times 10^{-6}$ K⁻¹ for concrete; it is because steel and concrete expand almost equally that reinforced concrete works. A body that is free to expand develops no stress. If the expansion is prevented, Hooke's law with zero total strain gives a compressive stress whose size depends on how many directions are restrained:

| Restraint | Stress |
| --- | --- |
| one direction (bar between rigid walls) | $`\sigma = -E\alpha\,\Delta T`$ |
| two directions (plate held at its edges) | $`\sigma_x = \sigma_y = -E\alpha\,\Delta T/(1 - \nu)`$ |
| three directions (inclusion in a rigid cavity) | $`\sigma = -E\alpha\,\Delta T/(1 - 2\nu)`$ |

For steel ($E = 200$ GPa, $\alpha = 12 \times 10^{-6}$ K⁻¹) heated by 60 K, the bar case gives 144 MPa and the plate case 206 MPa of compression, more than half the yield strength of a structural steel for a moderate temperature change. Thermal stresses in bars, with gaps and with two materials, are worked in [Axial Loading](axial_loading.md). Nonuniform temperature fields cause stress even without external restraint, because hot fibres are restrained by cold ones.

## Stress Concentration

Holes, notches, fillets and keyways disturb the stress flow and raise the local stress above the nominal value calculated from $N/A$ or $Mc/I$. The **stress concentration factor** is

$$
K_t = \frac{\sigma_{\max}}{\sigma_{\mathrm{nom}}}
$$

with the nominal stress defined on either the gross or the net section; charts state which, and mixing them up is a common error.

The reference case is a small circular hole of radius $a$ in a large plate under remote uniaxial stress $\sigma_\infty$ along $x$, solved by Kirsch (1898). In polar coordinates centred on the hole, with $\theta$ measured from the load axis,

```math
\sigma_{rr} = \frac{\sigma_\infty}{2}\left(1 - \frac{a^2}{r^2}\right) + \frac{\sigma_\infty}{2}\left(1 - \frac{4a^2}{r^2} + \frac{3a^4}{r^4}\right)\cos 2\theta,
\qquad
\sigma_{\theta\theta} = \frac{\sigma_\infty}{2}\left(1 + \frac{a^2}{r^2}\right) - \frac{\sigma_\infty}{2}\left(1 + \frac{3a^4}{r^4}\right)\cos 2\theta
```

```math
\tau_{r\theta} = -\frac{\sigma_\infty}{2}\left(1 + \frac{2a^2}{r^2} - \frac{3a^4}{r^4}\right)\sin 2\theta
```

On the hole edge, $\sigma_{rr} = \tau_{r\theta} = 0$ and $\sigma_{\theta\theta} = \sigma_\infty(1 - 2\cos 2\theta)$: the hoop stress is $3\sigma_\infty$ at the two points on the transverse axis ($\theta = 90^\circ$), so $K_t = 3$ independently of the hole size, and $-\sigma_\infty$ (compression) on the load axis.

![Kirsch solution: hoop stress field around the hole, decay of sigma_xx along the ligament and hoop stress on the hole edge](../../../scripts/plots/materials_kirsch_hole/materials_kirsch_hole.png)

The [Kirsch script](../../../scripts/plots/materials_kirsch_hole/) draws the hoop stress field (left), the stress $\sigma_{xx}$ along the ligament $x = 0$ (centre) and the hoop stress around the edge (right). Along the ligament $\sigma_{xx}/\sigma_\infty = 1 + a^2/(2r^2) + 3a^4/(2r^4)$, which falls from 3 at the edge to 1.22 at $r = 2a$ and 1.07 at $r = 3a$: the disturbance is confined to a few hole radii.

Because the solution is linear, other remote loads follow by superposition. Equal biaxial tension gives $\sigma_{\theta\theta} = 2\sigma_\infty$ all round the hole ($K_t = 2$); pure shear, $\sigma_x = -\sigma_y = \tau$, gives $\sigma_{\theta\theta} = -4\tau\cos 2\theta$ and $K_t = 4$. An elliptical hole with semi-axis $b$ across the load and $c$ along it has $K_t = 1 + 2b/c = 1 + 2\sqrt{b/\rho}$, where $\rho$ is the radius of curvature at the end of the transverse axis (Inglis 1913); as $\rho \to 0$ the ellipse becomes a crack and $K_t$ grows without bound, which leads to fracture mechanics. Finite-width plates, shoulders and grooves are covered by the charts of Peterson's; the finite-width hole is worked in [Axial Loading](axial_loading.md#stress-concentration-in-a-finite-plate).

A ductile material under a single static load yields locally at the peak and redistributes the stress, so $K_t$ is often ignored for static strength of ductile parts. It is never ignored for brittle materials, or for cyclic loading, where cracks start at the peak; there the fatigue factor $K_f = 1 + q(K_t - 1)$ with notch sensitivity $0 \le q \le 1$ is used (see [Fatigue](fatigue.md)).

## Key Takeaways

- The stress at a point is a symmetric second-order tensor; the traction on any plane is $\mathbf{t} = \boldsymbol{\sigma}\mathbf{n}$.
- Small strains are the symmetric part of the displacement gradient; the engineering shear strain is twice the tensor component.
- An isotropic elastic material has two independent constants; $G = E/[2(1 + \nu)]$ and $K = E/[3(1 - 2\nu)]$.
- Principal stresses are the eigenvalues of the stress tensor; the maximum in-plane shear is the radius of Mohr's circle, but the absolute maximum shear must include the third principal stress.
- Mohr's circle turns through $2\theta$ for a rotation $\theta$ of the element; fix a sign convention for $\tau$ and keep it.
- Restrained thermal expansion and geometric discontinuities create stresses that the nominal formulas miss: $K_t = 3$ for a small hole under uniaxial tension.

## Related Scripts

- [Mohr's Circle for Plane Stress](../../../scripts/algorithms/materials_mohr_circle/): transforms a 2D plane-stress state and draws Mohr's circle with the given, rotated, principal and maximum-shear stress elements.
- [Kirsch Stress Field Around a Hole](../../../scripts/plots/materials_kirsch_hole/): plots the closed-form Kirsch stress field around a circular hole in a plate under uniaxial tension and shows the stress concentration factor of 3 at the hole edge.
- [Failure Envelopes in the Principal-Stress Plane](../../../scripts/plots/beams_failure_envelopes/): draws the Tresca, von Mises, maximum-normal-stress and Coulomb–Mohr envelopes in the plane-stress principal-stress plane and computes the safety factor of example load points under each criterion.
- [Stress-Strain Curves](../../../scripts/plots/materials_stress_strain_curves/): draws model engineering and true stress–strain curves of a ductile and a brittle material.

## Exercises

**Exercise 1.** An aluminium rod ($E = 70$ GPa, $\nu = 0.33$) of diameter 25 mm carries a compressive load of 40 kN. Find the axial stress, the axial strain and the change in diameter. What is the shear modulus of the alloy?

<details>
<summary>Answer</summary>

$A = \pi(25)^2/4 = 490.9$ mm², so $`\sigma = -40\,000/490.9 = -81.5`$ MPa and $\varepsilon = \sigma/E = -1.164 \times 10^{-3}$.

The lateral strain is $-\nu\varepsilon = +3.84 \times 10^{-4}$, so $\Delta d = 25 \times 3.84 \times 10^{-4} = +0.0096$ mm: the rod gets slightly thicker.

$G = 70/(2 \times 1.33) = 26.3$ GPa.

</details>

**Exercise 2.** (a) The 12 mm bolt above (15 kN) is placed in double shear in a clevis. What is the average shear stress? (b) What diameter does a bolt in single shear need if the allowable shear stress is 100 MPa?

<details>
<summary>Answer</summary>

(a) Two shear planes share the load: $`\tau = 15\,000/(2 \times 113.1) = 66.3`$ MPa, half the single-shear value.

(b) $`d = \sqrt{4V/(\pi\tau_{\mathrm{allow}})} = \sqrt{4 \times 15\,000/(\pi \times 100)} = 13.8`$ mm, so a 14 mm bolt.

</details>

**Exercise 3.** A steel element ($E = 200$ GPa, $\nu = 0.3$) carries $\sigma_x = 100$ MPa, $\sigma_y = -50$ MPa and $\sigma_z = 0$. Find the three normal strains and the volumetric strain.

<details>
<summary>Answer</summary>

```math
\varepsilon_x = \frac{100 - 0.3(-50)}{200\,000} = 5.75 \times 10^{-4}, \quad
\varepsilon_y = \frac{-50 - 0.3(100)}{200\,000} = -4.00 \times 10^{-4}, \quad
\varepsilon_z = \frac{0 - 0.3(100 - 50)}{200\,000} = -7.5 \times 10^{-5}
```

$\varepsilon_v = 1.0 \times 10^{-4}$. The strain in $z$ is not zero although $\sigma_z = 0$, because of the Poisson effect. As a check, $`\varepsilon_v = (1 - 2\nu)(\sigma_x + \sigma_y + \sigma_z)/E = 0.4 \times 50/200\,000`$.

</details>

**Exercise 4.** At a point in plane stress, $\sigma_x = 60$ MPa, $\sigma_y = 20$ MPa and $\tau_{xy} = 25$ MPa. Find the normal stress on the plane at $\theta = 45^\circ$, the principal stresses and the principal angle, the maximum in-plane and absolute maximum shear stresses, and the factors of safety against yield ($\sigma_Y = 250$ MPa) by Tresca and by von Mises.

<details>
<summary>Answer</summary>

$\sigma_{x'}(45^\circ) = 40 + 20\cos 90^\circ + 25\sin 90^\circ = 65$ MPa.

$C = 40$ MPa and $R = \sqrt{20^2 + 25^2} = 32.0$ MPa, so $\sigma_1 = 72.0$ MPa and $\sigma_2 = 8.0$ MPa, with $\theta_p = \frac{1}{2}\arctan(50/40) = 25.7^\circ$.

The maximum in-plane shear is $R = 32.0$ MPa. Both principal stresses are tensile and $\sigma_3 = 0$, so $\tau_{\mathrm{abs}} = (72.0 - 0)/2 = 36.0$ MPa.

Tresca: $n = 250/(72.0 - 0) = 3.47$. von Mises:

```math
\sigma_{\mathrm{vM}} = \sqrt{72.0^2 - 72.0 \times 8.0 + 8.0^2} = 68.4 \text{ MPa} \implies n = 3.66
```

Using the in-plane shear $R$ instead of $\tau_{\mathrm{abs}}$ in Tresca would overestimate the safety factor by 12%.

</details>

**Exercise 5.** A large plate with a small circular hole carries remote stresses $\sigma_x = 100$ MPa and $\sigma_y = 50$ MPa. Using the Kirsch solution and superposition, find the largest and smallest hoop stress on the hole edge and where they occur. What would they be if the plate were in equal biaxial tension of 100 MPa?

<details>
<summary>Answer</summary>

The load along $x$ contributes $100(1 - 2\cos 2\theta)$. The load along $y$ is the same solution rotated by $90^\circ$, $50(1 + 2\cos 2\theta)$. The sum is

```math
\sigma_{\theta\theta} = 150 - 100\cos 2\theta \ \text{MPa}
```

The maximum, 250 MPa, is at $\theta = 90^\circ$ (on the $y$ axis, across the larger load); the minimum, 50 MPa, is at $\theta = 0$. For equal biaxial tension of 100 MPa the hoop stress is 200 MPa all round the hole ($K_t = 2$).

</details>

## References

- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Timoshenko, S. P., and Goodier, J. N., *Theory of Elasticity*, 3rd ed., McGraw-Hill, 1970.
- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 11th ed., McGraw-Hill Education, 2020.
- Pilkey, W. D., and Pilkey, D. F., *Peterson's Stress Concentration Factors*, 3rd ed., Wiley, 2008.
- Kirsch, G., "Die Theorie der Elastizität und die Bedürfnisse der Festigkeitslehre", *Zeitschrift des Vereines deutscher Ingenieure*, 42, 1898.
- Inglis, C. E., "Stresses in a plate due to the presence of cracks and sharp corners", *Transactions of the Institution of Naval Architects*, 55, 219–241, 1913.
