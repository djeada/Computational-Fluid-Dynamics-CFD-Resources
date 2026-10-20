# Axial Loading

A bar loaded along its axis is the simplest structural member: truss members, cables, tie rods, bolts, columns short enough not to buckle, and the struts and links of mechanisms all carry axial force only. This note derives the axial force, stress and deformation of bars with varying section, material and load; solves statically indeterminate bars, where equilibrium alone does not give the forces, by adding compatibility; treats thermal stress in constrained bars; explains Saint-Venant's principle and the stress concentration at a hole in a finite plate; and uses strain energy to find deflections and impact stresses. The same equations, discretized element by element, are the simplest case of the [finite element method](../../numerical/fem/intro.md).

## Problem Statement

A straight bar occupies $0 \le x \le L$. Its cross-section has area $A(x)$, its material Young's modulus $E(x)$ and thermal expansion coefficient $\alpha(x)$, and the cross-section may change abruptly between segments. It carries concentrated axial forces $P_i$ at points $x_i$, a distributed axial load $p(x)$ (N/m, for example self-weight), and a temperature change $\Delta T(x)$. One or both ends are fixed, or an end may close a gap $\Delta$ against a rigid support. Find the internal axial force $N(x)$, the stress $\sigma(x) = N/A$, the displacement $u(x)$, the change of length $\delta$ and the support reactions.

The assumptions are linear elasticity, small displacements, loads applied along the centroidal axis, cross-sections that remain plane so that $\sigma$ is uniform over each section (valid away from load points, by Saint-Venant's principle), and, in compression, a bar short enough not to buckle (see [Buckling and Stability](buckling.md)). The governing equations are

```math
\frac{dN}{dx} + p = 0,
\qquad \varepsilon = \frac{du}{dx},
\qquad N = EA\left(\frac{du}{dx} - \alpha\,\Delta T\right)
```

which combine into $`\dfrac{d}{dx}\left[EA\left(\dfrac{du}{dx} - \alpha\,\Delta T\right)\right] + p = 0`$, a second-order equation that needs one boundary condition at each end: a prescribed displacement or a prescribed force.

## Axial Force and Stress

The internal force at a section is found by the method of sections: cut the bar at $x$, draw the free body of either part, and sum forces along the axis. $N$ is taken positive in tension, pointing away from the cut face. Between concentrated loads $N$ is constant if $p = 0$; it jumps by $-P_i$ at a load $P_i$ acting in the $+x$ direction, and it varies linearly under a uniform $p$. The plot of $N(x)$ is the axial force diagram, and the stress $\sigma = N/A$ follows section by section. The largest stress need not occur where $N$ is largest, because the area can change.

## Deformation

Integrating $`du/dx = N/(EA) + \alpha\,\Delta T`$ over the length gives the elongation

```math
\delta = u(L) - u(0) = \int_0^L \frac{N(x)}{E(x)A(x)}\, dx + \int_0^L \alpha\,\Delta T\,
dx
```

For a bar made of $n$ prismatic segments with constant force in each, the mechanical part reduces to

$$
\delta = \sum_{i=1}^{n} \frac{N_i L_i}{E_i A_i}
$$

The quantity $f = L/(EA)$ is the **flexibility** of a segment (m/N) and its inverse $k = EA/L$ the **axial stiffness** (N/m).

A bar hanging under its own weight is the standard case with distributed load. With density $\rho$ and constant area, the force at height $x$ above the free end is the weight below, $N = \rho g A x$, so the stress is largest at the support, $\sigma_{\max} = \rho g L$, and

```math
\delta = \int_0^L \frac{\rho g A x}{EA}\, dx = \frac{\rho g L^2}{2E}
```

half of what a concentrated load equal to the total weight would produce. A steel cable ($\rho = 7850$ kg/m³, $E = 200$ GPa) hanging 1000 m down a mine shaft stretches 0.19 m under its own weight and carries 77 MPa at the top before any payload is attached.

For a tapered flat bar of thickness $t$ whose width varies linearly from $w_0$ at the fixed end to $w_1$ at the loaded end, $A(x) = t[w_0 + (w_1 - w_0)x/L]$ and an end load $P$ gives

$$
\delta = \frac{P}{E}\int_0^L \frac{dx}{A(x)} = \frac{PL}{E t (w_0 - w_1)}\ln
\frac{w_0}{w_1}
$$

With $L = 1$ m, $w_0 = 60$ mm, $w_1 = 20$ mm, $t = 10$ mm, $E = 200$ GPa and $P = 20$ kN, $\delta = 0.2747$ mm. A prismatic bar with the mean width of 40 mm would give 0.2500 mm, 9% less: the narrow end dominates the flexibility. The [axial bar finite element script](../../../scripts/algorithms/materials_axial_bar_fem/) approximates this bar by prismatic elements with the area at each element midpoint; the error falls as the square of the element length (lower-right panel of the figure below).

## Statically Indeterminate Bars

A bar is statically indeterminate when it has more unknown reactions or internal forces than independent equilibrium equations. A bar fixed at both ends has two unknown reactions but only one equation along the axis; a column of two materials side by side has two unknown internal forces. The missing equations come from the geometry of the deformation, and the solution procedure is:

1. Write the equilibrium equations for the free bodies, with the unknown forces in them.
2. Write the compatibility conditions: the deformations that the supports and connections impose (zero total elongation between rigid walls, equal elongation of parts bonded together, elongation equal to a gap).
3. Express each deformation through the force–deformation law, $`\delta_i = N_i L_i/(E_i A_i) + \alpha_i\,\Delta T\,L_i`$.
4. Solve the combined equations for the forces, then compute stresses and displacements.

Indeterminate structures share load in proportion to stiffness: the stiffer path attracts more force.

### Bar Between Two Walls

A bar is fixed at A and C, and a force $P$ acts towards C at the joint B between segment AB (flexibility $`f_1 = L_1/(E_1A_1)`$) and segment BC ($`f_2 = L_2/(E_2A_2)`$). Equilibrium of the joint gives $N_{BC} = N_{AB} - P$. Compatibility requires the total elongation to vanish:

```math
N_{AB} f_1 + (N_{AB} - P) f_2 + \Delta T\,(\alpha_1 L_1 + \alpha_2 L_2) = 0
```

so

```math
N_{AB} = \frac{P f_2 - \Delta T\,(\alpha_1 L_1 + \alpha_2 L_2)}{f_1 + f_2},
\qquad u_B = N_{AB} f_1 + \alpha_1\,\Delta T\, L_1
```

For a single material and section with $\Delta T = 0$ this reduces to $R_A = N_{AB} = P L_2/L$ and $R_C = -N_{BC} = P L_1/L$: the load splits in inverse proportion to the segment lengths.

As a worked case, take segment AB of steel ($L_1 = 0.4$ m, $A_1 = 600$ mm², $E_1 = 200$ GPa, $\alpha_1 = 12 \times 10^{-6}$ K⁻¹), segment BC of aluminium ($L_2 = 0.3$ m, $A_2 = 900$ mm², $E_2 = 70$ GPa, $\alpha_2 = 23 \times 10^{-6}$ K⁻¹), $P = 60$ kN and a temperature rise of 30 K. Then $f_1 = 3.333 \times 10^{-9}$ m/N, $f_2 = 4.762 \times 10^{-9}$ m/N, $Pf_2 = 0.2857$ mm and the free thermal elongation is $30(12 \times 0.4 + 23 \times 0.3) \times 10^{-6}$ m $= 0.351$ mm, so

```math
N_{AB} = \frac{0.2857 - 0.351}{8.095 \times 10^{-9}} \times 10^{-3} = -8.07 \text{ kN},
\qquad
N_{BC} = -68.07 \text{ kN}
```

The stresses are $-13.4$ MPa in the steel and $-75.6$ MPa in the aluminium, and B moves 0.117 mm towards C. The force alone would put the steel in tension (58.8 MPa); the heating adds 43.4 kN of compression to both segments.

![Two-material bar between walls: finite element displacement and stress for the force alone, the temperature rise alone and both, and convergence for the tapered bar](../../../scripts/algorithms/materials_axial_bar_fem/materials_axial_bar_fem.png)

The figure, from the [axial bar finite element script](../../../scripts/algorithms/materials_axial_bar_fem/), solves the same bar with eight two-node elements per segment. Each element contributes the stiffness matrix $`(EA/L_e)\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}`$ and the thermal load $`EA\,\alpha\,\Delta T\,[-1,\ 1]^{\mathsf{T}}`$; the nodal displacements agree with the hand solution to machine precision, because linear elements are exact for a prismatic bar with nodal loads. The displacement panel shows that the temperature rise alone barely moves B: the steel's free expansion (0.144 mm) and the aluminium's (0.207 mm) are each almost cancelled by the walls. The stress panel shows superposition: the green line (both loads) is the sum of the blue (force) and orange (temperature) lines.

### Bars in Parallel

When two materials are bonded side by side and loaded through rigid end plates, they share the same elongation. A steel tube of outer diameter 60 mm and inner diameter 50 mm ($A_s = 863.9$ mm², $E_s = 200$ GPa) is filled with concrete ($A_c = 1963.5$ mm², $E_c = 25$ GPa) and compressed by 200 kN over a length of 1.5 m. Equal strain means $N_s/(E_sA_s) = N_c/(E_cA_c)$, so each material carries a share proportional to its axial stiffness $EA$:

```math
N_s = \frac{E_sA_s}{E_sA_s + E_cA_c}\,P = \frac{172.8}{172.8 + 49.1} \times 200 = 155.8 \text{ kN},
\qquad
N_c = 44.2 \text{ kN}
```

The stresses are $\sigma_s = 180.3$ MPa and $\sigma_c = 22.5$ MPa, in the ratio $E_s/E_c = 8$, and the shortening is $\delta = N_sL/(E_sA_s) = 1.35$ mm. Reinforced concrete columns are designed the same way, using the modular ratio $E_s/E_c$ to convert the steel into an equivalent area of concrete.

## Thermal Stress in Constrained Bars

A free bar heated by $\Delta T$ lengthens by $`\alpha\,\Delta T\,L`$ with no stress. Between rigid walls the total elongation must be zero, so $`N L/(EA) + \alpha\,\Delta T\,L = 0`$ and

```math
\sigma = -E\alpha\,\Delta T
```

independent of the length and the area. An aluminium bar ($E = 70$ GPa, $\alpha = 23 \times 10^{-6}$ K⁻¹) heated from 20 °C to 80 °C between rigid walls develops $`\sigma = -70\,000 \times 23 \times 10^{-6} \times 60 = -96.6`$ MPa. If a gap $\Delta$ is left, the bar first expands freely; stress develops only after the gap closes, and compatibility becomes $\delta = \Delta$. Rail expansion joints, pipe loops and bridge bearings use this principle. A long slender bar that is heated between walls may buckle before it reaches the compressive stress above, at the Euler load treated in [Buckling and Stability](buckling.md).

## Saint-Venant's Principle

The formula $\sigma = N/A$ assumes the stress is uniform across the section. Near a concentrated load, a support or a change of section this is false: a bolt head or a clamp introduces the force over a small area. Saint-Venant's principle states that statically equivalent load distributions (same resultant force and moment) produce stress fields that differ only within a region whose size is about the largest cross-sectional dimension. Beyond that distance the elementary formula holds whatever the details of the load introduction.

The Kirsch solution for a hole in a plate, plotted in [Stress and Strain](stress_strain.md#stress-concentration), shows the decay quantitatively. Along the ligament the stress falls from $3\sigma_\infty$ at the edge to $1.22\sigma_\infty$ at one radius from the edge, $1.07\sigma_\infty$ at two radii and $1.02\sigma_\infty$ at four. Strain gauges should therefore be placed a few section widths from grips and holes, and a finite element model can represent a bolted connection crudely if only the stress far from it is needed.

## Stress Concentration in a Finite Plate

A plate of width $w$ and thickness $t$ with a central hole of diameter $d$ carries an axial load $P$. The nominal stress on the net section is $\sigma_{\mathrm{nom}} = P/[(w - d)t]$, and the peak stress at the hole edge is $\sigma_{\max} = K_t\sigma_{\mathrm{nom}}$. For a small hole $K_t \to 3$ (Kirsch, based on the gross stress, which equals the net stress in that limit). Based on the net section, $K_t$ falls towards 2 as the hole fills the plate; Heywood's approximation, reproduced in Peterson's,

$$
K_t = 2 + \left(1 - \frac{d}{w}\right)^3
$$

is a convenient fit to the chart. Other common values: a shoulder fillet in a stepped bar has $K_t$ between about 1.5 and 2.5 depending on the radius ratio $r/d$ and the step $D/d$; a semicircular edge notch about 3.

For $w = 50$ mm, $t = 10$ mm, $d = 10$ mm and $P = 20$ kN, the net area is 400 mm², $\sigma_{\mathrm{nom}} = 50$ MPa, $d/w = 0.2$ gives $K_t = 2.51$, and $\sigma_{\max} = 126$ MPa.

## Strain Energy

A bar stretched elastically stores the work done on it as strain energy. Integrating $u = \sigma^2/(2E)$ over the volume gives

```math
U = \int_0^L \frac{N^2}{2EA}\, dx = \sum_i \frac{N_i^2 L_i}{2E_iA_i}
```

For a single load $P$ that rises slowly from zero, $U = \frac{1}{2}P\delta$ (Clapeyron's theorem); for the steel–aluminium bar under the force alone, the script finds $U = 3.529$ J, equal to $`\frac{1}{2} \times 60\,000 \times 0.1176 \times 10^{-3}`$ J. **Castigliano's theorem** gives the displacement at any load $P_j$ as $\delta_j = \partial U/\partial P_j$, which is the basis of energy methods for trusses and frames; a dummy load can be added where a displacement is wanted and set to zero after differentiation.

Energy also gives a first estimate of impact stress. A mass $m$ falls through a height $h$ onto a collar at the end of a vertical rod. If the rod is massless and elastic and no energy is lost, $`mg(h + \delta_{\max}) = \frac{1}{2}k\,\delta_{\max}^2`$ with $k = EA/L$, so

```math
\delta_{\max} = \delta_{\mathrm{st}}\left(1 + \sqrt{1 + \frac{2h}{\delta_{\mathrm{st}}}}\right),
\qquad
\delta_{\mathrm{st}} = \frac{mgL}{EA}
```

A 10 kg mass dropped 50 mm onto a steel rod 2 m long and 20 mm in diameter gives $\delta_{\mathrm{st}} = 3.12$ μm and an impact factor of 180: the peak stress is 56 MPa instead of the static 0.31 MPa. Even a load applied suddenly with $h = 0$ doubles the static deflection and stress. The estimate is conservative, because the rod's inertia and local plasticity absorb part of the energy.

## Key Takeaways

- Draw the axial force diagram first; the critical section is where $N/A$, not $N$, is largest.
- $`\delta = \int N/(EA)\,dx`$, or $\sum N_iL_i/(E_iA_i)$ for prismatic segments; flexibilities $L/(EA)$ add in series, stiffnesses $EA/L$ add in parallel.
- Indeterminate bars need compatibility; the stiffer load path carries more force.
- A fully constrained bar develops $`\sigma = -E\alpha\,\Delta T`$, independent of its length; a gap relieves part of it.
- The uniform-stress formula holds a section width or so away from loads and discontinuities (Saint-Venant); at the discontinuity multiply by $K_t$.
- Strain energy gives deflections by Castigliano's theorem and shows that impact loads can multiply the static stress many times.

## Related Scripts

- [Axial Bar Finite Elements](../../../scripts/algorithms/materials_axial_bar_fem/): solves statically indeterminate axial bars with two-node finite elements and checks them against the hand solution from equilibrium and compatibility.
- [Kirsch Stress Field Around a Hole](../../../scripts/plots/materials_kirsch_hole/): plots the closed-form Kirsch stress field around a circular hole in a plate under uniaxial tension and shows the stress concentration factor of 3 at the hole edge.

## Exercises

**Exercise 1.** A steel bar ($E = 200$ GPa) is fixed at A. Segment AB is 1 m long with $A = 400$ mm²; segment BC is 0.5 m long with $A = 200$ mm². A 50 kN force pulls to the right (away from A) at B, and a 20 kN force pushes to the left at C. Find the internal force in each segment and the displacement of C.

<details>
<summary>Answer</summary>

Cutting each segment and keeping the part towards the free end:

- BC carries only the load at C: $N_{BC} = -20$ kN (compression).
- AB carries both loads: $N_{AB} = 50 - 20 = 30$ kN (tension).

```math
\delta_C = \frac{30\,000 \times 1000}{400 \times 200\,000} + \frac{-20\,000 \times 500}{200 \times 200\,000} = 0.375 - 0.250 = 0.125 \text{ mm}
```

C moves 0.125 mm to the right.

</details>

**Exercise 2.** A bar of cross-section 300 mm² is fixed between two walls. A 60 kN axial load is applied 0.4 m from wall A and 0.6 m from wall B. Find both reactions and the stress in each segment.

<details>
<summary>Answer</summary>

```math
R_A = P\frac{L_2}{L_1 + L_2} = 60 \times 0.6 = 36 \text{ kN}, \qquad R_B = 60 \times 0.4 = 24 \text{ kN}
```

The shorter, stiffer segment takes more load. The segment next to A is in tension, $`36\,000/300 = 120`$ MPa, and the segment next to B in compression, $`24\,000/300 = 80`$ MPa.

</details>

**Exercise 3.** Repeat the constrained aluminium bar ($L = 0.5$ m, $E = 70$ GPa, $\alpha = 23 \times 10^{-6}$ K⁻¹, temperature rise 60 K), but with a gap of 0.2 mm between the bar and one wall at the start. Find the stress after heating.

<details>
<summary>Answer</summary>

Free expansion is $`\alpha\,\Delta T\,L = 23 \times 10^{-6} \times 60 \times 500 = 0.69`$ mm. The gap absorbs 0.2 mm, so the walls suppress the remaining 0.49 mm:

```math
\sigma = -E\,\frac{0.49}{500} = -70\,000 \times 9.8 \times 10^{-4} = -68.6 \text{ MPa}
```

The small gap removes 29% of the thermal stress.

</details>

**Exercise 4.** For the concrete-filled steel tube above, what axial load makes the steel reach its yield stress of 250 MPa? What is the concrete stress at that load, and is it likely to be acceptable?

<details>
<summary>Answer</summary>

Both materials share the strain $\varepsilon = \sigma_s/E_s = 1.25 \times 10^{-3}$, so

```math
P = \varepsilon\,(A_sE_s + A_cE_c) = 1.25 \times 10^{-3} \times (863.9 \times 200\,000 + 1963.5 \times 25\,000) = 277 \text{ kN}
```

The concrete stress is $\sigma_c = E_c\varepsilon = 31.3$ MPa, close to or above the compressive strength of ordinary concrete (see [Mechanical Properties of Materials](material_properties.md)), so the concrete may govern before the steel yields. Confinement by the tube raises the concrete's effective strength, which is one reason such columns perform well.

</details>

**Exercise 5.** The plate with a hole above ($w = 50$ mm, $t = 10$ mm, $d = 10$ mm) is made of a steel whose allowable peak stress is 180 MPa. What is the largest axial load? Why do designers often ignore $K_t$ for a single static load on a ductile plate, but never for fatigue?

<details>
<summary>Answer</summary>

With $K_t = 2.51$,

```math
P_{\max} = \frac{\sigma_{\mathrm{allow}}A_{\mathrm{net}}}{K_t} = \frac{180 \times 400}{2.51} = 28.7 \text{ kN}
```

Under a single static load a ductile material yields locally at the hole edge and redistributes the stress across the net section, so the net-section stress $P/A_{\mathrm{net}}$ governs failure. Under cyclic loading, fatigue cracks start at the stress peak, so the concentration (through the fatigue factor $K_f$) directly shortens the life; see [Fatigue](fatigue.md).

</details>

## References

- Gere, J. M., and Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Hibbeler, R. C., *Mechanics of Materials*, 10th ed., Pearson, 2017.
- Beer, F. P., Johnston, E. R., DeWolf, J. T., and Mazurek, D. F., *Mechanics of Materials*, 7th ed., McGraw-Hill Education, 2015.
- Timoshenko, S. P., and Goodier, J. N., *Theory of Elasticity*, 3rd ed., McGraw-Hill, 1970.
- Pilkey, W. D., and Pilkey, D. F., *Peterson's Stress Concentration Factors*, 3rd ed., Wiley, 2008.
- Heywood, R. B., *Designing by Photoelasticity*, Chapman and Hall, 1952.
