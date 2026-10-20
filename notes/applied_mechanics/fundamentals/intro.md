# Introduction to Applied Mechanics

Applied mechanics uses Newton's laws, together with laws that describe how materials and fluids respond to load, to predict the forces in and the motion of engineering systems: the reactions that hold a bridge up, the stresses in a shaft, the vibration of a turbine blade, the trajectory of a vehicle, the load the wind puts on a building. This note sets out what the subject covers, the idealized models it works with, the units and dimensional checks every calculation needs, Newton's laws in the form used throughout the section, and a procedure for solving problems. The later notes in [Fundamentals](./README.md) develop the vector tools, force systems, moments and free-body diagrams on which statics, dynamics and strength of materials are built.

## Problem Statement

A problem in applied mechanics gives a physical system and asks for its response. The data are:

- the geometry of the bodies and how they are connected (dimensions, joints, supports);
- the loads: applied forces and couples, distributed loads such as weight, pressure and wind, and prescribed motions;
- the material behaviour, when deformation matters (elastic modulus, yield strength, density);
- for motion, the initial position and velocity.

The unknowns are some of: support reactions, internal forces and moments, stresses and deformations, accelerations and trajectories, natural frequencies, or the control input that makes a system behave as required. The analyst chooses a model (particle, rigid body or deformable body; 2D or 3D; static or dynamic; linear or nonlinear) and writes the governing equations. For a body of mass $m$ with centre of mass $G$, these are the balance of linear and angular momentum,

$$
\sum \mathbf{F} = m\mathbf{a}_G,
\qquad \sum \mathbf{M}_G = \frac{d\mathbf{H}_G}{dt}
$$

where $\sum \mathbf{F}$ is the resultant external force (N), $\mathbf{a}_G$ the acceleration of $G$ (m/s²), $\sum \mathbf{M}_G$ the resultant external moment about $G$ (N·m) and $\mathbf{H}_G$ the angular momentum about $G$ (kg·m²/s). Statics is the special case $\mathbf{a}_G = \mathbf{0}$ and $d\mathbf{H}_G/dt = \mathbf{0}$. For a deformable body the momentum balance holds for every part of the body and must be supplemented by compatibility of deformation and a constitutive law such as Hooke's law $\sigma = E\epsilon$.

## Scope of the Subject

| Branch | Question it answers | Main equations | Notes |
| --- | --- | --- | --- |
| Statics | What forces hold a body at rest? | $\sum \mathbf{F} = \mathbf{0}$, $\sum \mathbf{M} = \mathbf{0}$ | [Statics](../statics/README.md) |
| Kinematics | How does a body move, regardless of cause? | $\mathbf{v} = d\mathbf{r}/dt$, $\mathbf{a} = d\mathbf{v}/dt$ | [Dynamics](../dynamics/README.md) |
| Kinetics | What motion do given forces produce? | Newton–Euler equations, work–energy, impulse–momentum | [Dynamics](../dynamics/README.md) |
| Strength of materials | What stresses and deformations do loads cause, and when does a member fail? | Equilibrium, compatibility, $\sigma = E\epsilon$ | [Strength of Materials](../strength_materials/README.md) |
| Fluid loading | What forces does a flowing or still fluid put on a structure, and how does the structure respond? | Pressure and shear integrals, Morison and wind-load models, coupled fluid–structure equations | [Fluid Loading](../fluid_loading/README.md) |
| Machines and control | How do mechanisms transmit motion and power, and how is a system made to follow a command? | Kinematic constraints, transfer functions, feedback laws | [Mechanical Systems](../mechanical_systems/README.md), [Control Systems](../control_systems/README.md) |

The fluid mechanics behind the loads is in [`notes/fluid_mechanics/`](../../fluid_mechanics/README.md); the numerical methods used when the geometry is too complex for hand analysis are in [`notes/numerical/`](../../numerical/README.md).

## Idealized Models

Every analysis replaces the real object by a model that keeps only what affects the answer. The choice is a modelling decision and has to be justified.

| Model | What is kept | What is neglected | Justified when | Example |
| --- | --- | --- | --- | --- |
| Particle | Mass, position | Size, shape, rotation | The body's size is small compared with the distances it moves, or its rotation does not affect the question | A satellite in orbit; a car on a long route |
| Rigid body | Mass, geometry, rotation | Deformation | Deformations are small and do not change the geometry over which forces act | Reactions of a steel beam; a linkage in a mechanism |
| Deformable body | Geometry, deformation, material law | Molecular structure | Stresses, deflections, stability or statically indeterminate reactions are wanted | Deflection of the same beam; buckling of a column |
| Continuum | Fields (density, velocity, stress) defined at every point | Discrete molecules | The smallest length of interest is much larger than the molecular spacing, or the mean free path for a gas (Knudsen number $\mathrm{Kn} \ll 1$) | Air flow over a wing; stress in a plate |

Loads are idealized in the same way. A **concentrated force** acts at a point; it stands for a load spread over an area small compared with the body, such as a wheel contact patch on a bridge deck. A **distributed load** has an intensity per unit length (N/m), area (Pa) or volume (N/m³). Supports are idealized as pins, rollers and fixed ends that prevent specific motions, as tabulated in [Free-Body Diagrams](./free_body_diagrams.md).

A rigid-body model is enough to find the reactions of a statically determinate structure, but not those of an indeterminate one, which depend on stiffness; the same beam must then be treated as deformable. A more refined model is still only as good as its assumptions.

## Units and Dimensional Consistency

The notes use SI units. Mechanics needs three base units, the metre (m), kilogram (kg) and second (s); the others are derived:

| Quantity | Unit | In base units |
| --- | --- | --- |
| Force | newton, N | kg·m/s² |
| Moment, torque | newton metre, N·m | kg·m²/s² |
| Pressure, stress | pascal, Pa = N/m² | kg/(m·s²) |
| Work, energy | joule, J = N·m | kg·m²/s² |
| Power | watt, W = J/s | kg·m²/s³ |
| Angle | radian, rad | dimensionless |

Prefixes in engineering use are k ($10^3$), M ($10^6$), G ($10^9$), m ($10^{-3}$) and µ ($10^{-6}$): stresses in MPa, elastic moduli in GPa, loads in kN, moments in kN·m. Mass and weight are different quantities: a 1000 kg mass weighs $W = mg = 9.81$ kN at the Earth's surface, with $g = 9.81$ m/s². Moment and energy share the unit N·m but are different quantities; energy is usually written in J.

Every term of a physical equation must have the same dimensions, a property called dimensional homogeneity. Checking it catches most algebraic slips. The deflection of a simply supported beam under a uniform load,

$$
\delta_{\max} = \frac{5wL^4}{384EI}
$$

with $w$ in N/m, $L$ in m, $E$ in Pa and $I$ in m⁴, has units $`(\mathrm{N/m})\,\mathrm{m}^4/((\mathrm{N/m^2})\,\mathrm{m}^4) = \mathrm{m}`$, as a deflection must. Arguments of functions such as $\sin$, $\exp$ and $\ln$ must be dimensionless, and angles in formulas derived by calculus (arc length $s = r\theta$, $\omega = d\theta/dt$) must be in radians. Convert all data to base units, or to a consistent set such as N, mm and MPa (where 1 MPa = 1 N/mm²), before substituting.

## Newton's Laws

Newton's three laws, stated for a particle in an inertial (non-accelerating, non-rotating) reference frame, are the starting point of the whole subject.

1. A particle on which the resultant force is zero remains at rest or moves in a straight line at constant speed.

2. The resultant force on a particle equals its mass times its acceleration:

   ```math
   \mathbf{F} = m\mathbf{a}
   ```

3. The forces of interaction between two bodies are equal in magnitude, opposite in direction and collinear:

   ```math
   \mathbf{F}_{AB} = -\mathbf{F}_{BA}
   ```

The law of gravitation gives the attraction between two masses $m_1$ and $m_2$ a distance $r$ apart as $F = Gm_1m_2/r^2$ with $G = 6.674 \times 10^{-11}$ m³/(kg·s²). At the Earth's surface ($M_E = 5.972 \times 10^{24}$ kg, $R_E = 6.371 \times 10^6$ m) this gives $W = mg$ with $g = GM_E/R_E^2 = 9.82$ m/s²; the measured value varies with latitude, from 9.78 m/s² at the equator to 9.83 m/s² at the poles, because of the Earth's rotation and flattening. Engineering calculations use the standard value $g = 9.81$ m/s².

Summing the second law over all particles of a body, the internal forces cancel in pairs by the third law, which leaves the two balance equations of the [Problem Statement](#problem-statement): the external forces determine the motion of the centre of mass, and the external moments the rate of change of angular momentum. Statics, rigid-body dynamics and, applied to every small element, the equations of deformable solids and of fluids (the Cauchy momentum equation and the [Navier–Stokes equations](../../fluid_mechanics/governing_equations/navier_stokes.md)) all follow from these.

## Problem-Solving Procedure

1. State what is given and what is to be found, with units, and sketch the system.
2. Choose the model (particle, rigid or deformable body; 2D or 3D) and list the assumptions: neglected weights, frictionless pins, small deflections, linear elasticity.
3. Isolate the body or bodies and draw [free-body diagrams](./free_body_diagrams.md) showing every external force and couple, with a coordinate system.
4. Write the governing equations: equilibrium or equations of motion, plus compatibility and material laws if the body deforms. Count unknowns and independent equations before solving.
5. Solve symbolically as far as practical, then substitute numbers in consistent units.
6. Check the result: dimensions, signs and directions, limiting cases, an independent equation (for example moments about a second point), and orders of magnitude.

### Worked Example

A simply supported beam of span $L = 6$ m carries a uniform load $w = 10$ kN/m. It is a solid steel section 100 mm × 100 mm, so $I = bh^3/12 = 8.33 \times 10^{-6}$ m⁴, and $E = 200$ GPa. Find the reactions, the maximum bending moment and the maximum deflection.

1. Model: rigid body for the reactions, elastic Euler–Bernoulli beam for the deflection; self-weight neglected.

2. The total load $wL = 60$ kN acts at midspan, so by symmetry the reactions are $R_A = R_B = wL/2 = 30$ kN.

3. The bending moment is greatest at midspan: $M_{\max} = wL^2/8 = 10 \times 6^2/8 = 45$ kN·m.

4. The maximum deflection is

   ```math
   \delta_{\max} = \frac{5wL^4}{384EI} = \frac{5 \times (10 \times 10^3) \times 6^4}{384 \times (200 \times 10^9) \times (8.33 \times 10^{-6})} = 0.101 \text{ m}
   ```

5. Check: 101 mm is $L/59$, against a usual serviceability limit of $L/360 = 16.7$ mm, so the section is far too flexible for this span. The answer is plausible because a 100 mm square bar is a slender member for a 6 m span.

The [free-body diagram figure](./free_body_diagrams.md#worked-example-a-pin-roller-beam) carries a similar beam through steps 3 and 4 with an inclined load.

## From Hand Analysis to Computation

Hand analysis covers simple geometries and is how results are checked. Complex structures are analysed with the finite element method, which discretizes a deformable body into elements and solves the resulting equilibrium equations ([Finite Element Method](../../numerical/fem/intro.md)). Fluid forces on complex shapes come from CFD, which solves the flow equations and returns pressure and shear stress on every wall face; integrating these gives the forces and moments that a structural model then carries, as described in [Pressure Forces on Structures](../fluid_loading/pressure_forces.md). When the structure moves enough to change the flow, the two solvers must be coupled ([Fluid–Structure Interaction: Coupling Methods](../fluid_loading/fluid_structure_interaction.md)). In every case the numerical result is only as good as the idealizations, units and free-body diagrams behind it.

## Key Takeaways

- Every analysis starts with an idealized model; state its assumptions and check they hold.
- The particle, rigid-body, deformable-body and continuum models differ in what they keep; reactions of determinate structures need only rigid bodies, stresses and deflections need deformable ones.
- Work in consistent SI units and check dimensional homogeneity of every equation.
- Newton's laws, summed over a body, give $\sum \mathbf{F} = m\mathbf{a}_G$ and $\sum \mathbf{M}_G = d\mathbf{H}_G/dt$; statics is the case where both right-hand sides vanish.
- Solve problems in a fixed order: data, model, free-body diagram, equations, solution, checks.

## Related Scripts

- [Free-Body Diagram of a Beam](../../../scripts/plots/fundamentals_free_body_diagram/): turns a loaded, supported beam into its free-body diagram and solves the three planar equilibrium equations for the support reactions.

## Exercises

**Exercise 1.** For each question, name the branch of applied mechanics and the simplest adequate model (particle, rigid body or deformable body): (a) the tensions in the two cables holding a stationary sign; (b) the stopping distance of a car with a known constant deceleration; (c) the braking force needed to stop a 1500 kg car from 25 m/s in 40 m; (d) the elongation of a steel cable under load; (e) the reactions of a beam fixed at both ends.

<details>
<summary>Answer</summary>

(a) Statics; a rigid body, or a particle at the point where the cables meet. (b) Kinematics of a particle. (c) Kinetics of a particle; from $v^2 = 2as$ the deceleration is $25^2/(2 \times 40) = 7.81$ m/s², so $F = ma = 11.7$ kN. (d) Strength of materials; a deformable body. (e) Statics alone gives three equations for six unknowns, so the beam is statically indeterminate and must be modelled as a deformable body.

</details>

**Exercise 2.** A steel rod of diameter 20 mm and length 2 m carries an axial tensile load of 50 kN, with $E = 200$ GPa. Find the stress, strain and elongation.

<details>
<summary>Answer</summary>

```math
A = \frac{\pi(0.020)^2}{4} = 3.14 \times 10^{-4} \text{ m}^2, \qquad \sigma = \frac{50 \times 10^3}{3.14 \times 10^{-4}} = 159 \text{ MPa}
```

```math
\epsilon = \frac{\sigma}{E} = \frac{159 \times 10^6}{200 \times 10^9} = 7.96 \times 10^{-4}, \qquad \Delta L = \epsilon L = 1.59 \text{ mm}
```

</details>

**Exercise 3.** Check that $\delta_{\max} = 5wL^4/(384EI)$ is dimensionally consistent, and use it to explain why doubling the span of a beam is far more damaging than doubling its load. Then show that the frequency $\omega = \sqrt{k/m}$ of a mass on a spring has units of 1/s.

<details>
<summary>Answer</summary>

Units: $(\mathrm{N/m})(\mathrm{m^4})/((\mathrm{N/m^2})(\mathrm{m^4})) = \mathrm{m}$, a length. Deflection is linear in $w$ but proportional to $L^4$: doubling the load doubles the deflection, doubling the span multiplies it by 16.

For the spring, $k$ is in N/m $= \mathrm{kg/s^2}$, so $k/m$ is in $1/\mathrm{s^2}$ and $\omega$ in 1/s (rad/s, since the radian is dimensionless).

</details>

**Exercise 4.** For the beam of the worked example ($L = 6$ m, $w = 10$ kN/m, $E = 200$ GPa), find the second moment of area needed to limit the maximum deflection to $L/360$.

<details>
<summary>Answer</summary>

$\delta_{\mathrm{allow}} = 6000/360 = 16.7$ mm. Rearranging the deflection formula:

```math
I_{\mathrm{req}} = \frac{5wL^4}{384E\delta_{\mathrm{allow}}} = \frac{5 \times 10^4 \times 6^4}{384 \times 200 \times 10^9 \times 0.01667} = 5.06 \times 10^{-5} \text{ m}^4
```

This is 6.1 times the $I$ of the 100 mm square bar, consistent with its deflection of $L/59$.

</details>

**Exercise 5.** A 60 kg person jumps horizontally off a 40 kg boat that is initially at rest, reaching 2 m/s relative to the ground. Neglecting water resistance, find the boat's recoil velocity and the kinetic energy produced. Which conservation law applies to each quantity?

<details>
<summary>Answer</summary>

There is no external horizontal force on the person and boat together, so horizontal momentum is conserved: $0 = 60(2) + 40v_b$, giving $v_b = -3$ m/s, opposite to the person.

Kinetic energy: $\tfrac{1}{2}(60)(2^2) + \tfrac{1}{2}(40)(3^2) = 120 + 180 = 300$ J. Mechanical energy is not conserved; the 300 J comes from chemical energy in the person's muscles, and total energy is conserved.

</details>

## References

- Hibbeler, R. C., *Engineering Mechanics: Statics*, 14th ed., Pearson, 2016.
- Hibbeler, R. C., *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- Beer, F. P., Johnston, E. R., Mazurek, D. F., & Eisenberg, E. R., *Vector Mechanics for Engineers: Statics and Dynamics*, 12th ed., McGraw-Hill, 2019.
- Meriam, J. L., Kraige, L. G., & Bolton, J. N., *Engineering Mechanics: Statics*, 9th ed., Wiley, 2018.
- Gere, J. M., & Goodno, B. J., *Mechanics of Materials*, 9th ed., Cengage Learning, 2018.
- Bureau International des Poids et Mesures, *The International System of Units (SI)*, 9th ed., BIPM, 2019.
