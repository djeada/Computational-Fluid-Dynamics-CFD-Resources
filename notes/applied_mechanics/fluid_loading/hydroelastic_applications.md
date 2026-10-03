# Hydroelastic Applications

Hydroelasticity is the study of the mutual interaction between deformable structures and surrounding fluid, where neither the fluid loading nor the structural response can be determined independently. This chapter covers the fundamental concepts of added mass, fluid-structure coupling, and practical applications in marine, offshore, and subsea engineering.

## Hydroelasticity Fundamentals

### Definition

In a hydroelastic problem the structural deformation modifies the fluid flow, and the modified flow in turn changes the loading on the structure. This two-way coupling distinguishes hydroelasticity from simpler load-then-analyse approaches.

### Classification

| Type | Description | Examples |
| --- | --- | --- |
| **Hydrostatic** | Fluid loads depend on static displacement only | Buoyancy restoring forces, static heel |
| **Hydrokinetic** | Loads depend on structural velocity | Radiation damping, flutter |
| **Hydroinertial** | Loads depend on structural acceleration | Added mass, whipping |

### Governing Equation

The coupled equation of motion for a structure in fluid is:

$$
[M_s + M_a]\ddot{x} + [C_s + C_f]\dot{x} + [K_s + K_f]x = F_{ext}(t)
$$

where:

- $M_s$, $C_s$, $K_s$ = structural mass, damping, and stiffness matrices
- $M_a$ = **added mass** (hydrodynamic) matrix
- $C_f$ = **radiation damping** matrix (energy radiated as waves)
- $K_f$ = **hydrostatic restoring stiffness** matrix
- $F_{ext}$ = external excitation (waves, current, impact)

## Added Mass Concept

### Physical Interpretation

When a body accelerates through a fluid, it must also accelerate a volume of surrounding fluid. The force required for this additional acceleration appears as an **added mass** (or virtual mass):

$$
F_{added} = -m_a \ddot{x}
$$

The added mass is not a fixed quantity of fluid but a mathematical representation of the fluid's inertial reaction.

### Added Mass Coefficient

The added mass coefficient relates the added mass to the displaced fluid mass:

$$
C_a = \frac{m_a}{\rho \mathcal{V}_{ref}}
$$

where $\mathcal{V}_{ref}$ is a reference volume (typically the displaced volume).

### Analytical Values for Simple Shapes

| Shape | Motion | $C_a$ |
| --- | --- | --- |
| Circular cylinder (2-D) | Transverse | 1.0 |
| Sphere | Any direction | 0.5 |
| Thin flat plate (width $b$) | Normal to plate | 1.0, referred to $\rho \pi b^2/4$ per unit length |
| Ellipsoid (semi-axes $a,b$) | Along $a$-axis | Depends on $a/b$ ratio |

For a **circular cylinder** of diameter $D$ oscillating transversely in an unbounded fluid:

$$
m_a = C_a \rho \frac{\pi D^2}{4} \quad \text{per unit length}
$$

with $C_a = 1.0$ in potential flow.

### Effect on Natural Frequency

The added mass reduces the natural frequency of a submerged structure:

$$
f_{n,fluid} = \frac{1}{2\pi} \sqrt{\frac{k}{m_s + m_a}} = f_{n,vacuum}
\sqrt{\frac{m_s}{m_s + m_a}}
$$

For structures in water, the frequency reduction can be 30–60% compared to the in-air value.

## Fluid-Structure Coupling Methods

### Partitioned (Staggered) Approach

The fluid and structural solvers run separately and exchange information at the interface:

1. Solve the fluid equations for pressure on the current structural configuration
2. Transfer pressure loads to the structural solver
3. Solve the structural equations for the new displacement
4. Update the fluid domain mesh to match the new structural shape
5. Repeat until convergence within each time step

**Advantages:** Existing fluid and structural codes can be reused.
**Disadvantages:** May require sub-iterations for stability; added mass instability can arise when $m_a \gg m_s$.

### Monolithic Approach

The fluid and structural equations are assembled into a single system and solved simultaneously:

$$
\begin{bmatrix} A_{ff} & A_{fs} \\ A_{sf} & A_{ss} \end{bmatrix} \begin{bmatrix} u_f \\ u_s \end{bmatrix} = \begin{bmatrix} b_f \\ b_s \end{bmatrix}
$$

**Advantages:** Unconditionally stable; handles strong coupling.
**Disadvantages:** Requires a unified solver; larger system to solve.

### Modal Superposition

For linear problems the structural response is expanded in terms of dry (in-vacuo) modes $\phi_i$:

$$
x(\mathbf{r},t) = \sum_{i=1}^{N} q_i(t) \, \phi_i(\mathbf{r})
$$

Substituting into the coupled equation yields a set of ordinary differential equations in the generalised coordinates $q_i$, with frequency-dependent added mass and damping from the hydrodynamic analysis:

$$
(m_i + a_{ii}(\omega))\ddot{q}_i + (c_i + b_{ii}(\omega))\dot{q}_i + k_i q_i = f_i(t)
$$

where $a_{ii}$ and $b_{ii}$ are the diagonal terms of the generalised added mass and radiation damping matrices.

## Ship Hydroelasticity

### Why It Matters

Modern ships are larger, more flexible, and operate in severe seas. The traditional rigid-body seakeeping assumption breaks down when structural deformation is comparable to the rigid-body motions.

### Springing

**Springing** is the resonant excitation of the lowest flexural modes of a ship hull by higher-order (nonlinear) wave forces. The excitation frequency is:

$$
f_{exc} = n f_e \quad (n = 2, 3, \ldots)
$$

where $f_e$ is the encounter frequency. Springing causes continuous low-amplitude fatigue loading.

### Whipping

**Whipping** is the transient vibration of the hull girder caused by impulsive loads:

- **Bow slamming**: Impact of the bow on the water surface after emerging from a wave
- **Green water**: Solid water on deck creating sudden loads
- **Stern slamming**: Impact on flat stern sections

The whipping response adds to the wave-induced bending moment. For ultra-large container ships the whipping contribution can be **30–50%** of the rigid-body wave bending moment.

### Analysis Methods

1. **2-D strip theory + beam model**: The hull is modelled as a Timoshenko beam; each strip provides hydrodynamic coefficients
2. **3-D panel method + FE model**: Full 3-D diffraction/radiation analysis coupled with a finite element structural model
3. **CFD + FE**: Viscous flow solvers coupled with structural FE for slamming and green water events

## Underwater Vehicle Dynamics

### Equations of Motion

For a submerged vehicle the 6-DOF equations include added mass in all modes:

$$
[M_s + M_a]\dot{V} + \text{(Coriolis and centripetal terms)} = F_{hydro} + F_{control}
$$

The added mass matrix $M_a$ is a $6 \times 6$ symmetric matrix. For a body with three planes of symmetry, off-diagonal terms vanish and the matrix becomes diagonal.

### Manoeuvring Coefficients

The hydrodynamic forces on a manoeuvring submarine are expressed using stability derivatives:

$$
Y = Y_v v + Y_{\dot{v}} \dot{v} + Y_r r + Y_{\dot{r}} \dot{r} + \cdots
$$

where $Y_{\dot{v}}$ and $Y_{\dot{r}}$ are added mass derivatives (sway and yaw coupling).

### Depth Control and Stability

- **Static stability**: Requires the centre of buoyancy above the centre of gravity ($BG > 0$)
- **Dynamic stability**: Routh stability criteria applied to the linearised equations with hydrodynamic derivatives
- Added mass strongly affects the pitch and heave natural frequencies, which govern depth-keeping performance

## Pipe Flow Vibrations

### Internal Flow in Flexible Pipes

A flexible pipe conveying fluid of density $\rho_f$ at velocity $U$ is governed by:

$$
EI \frac{\partial^4 y}{\partial x^4} + (m_f U^2) \frac{\partial^2 y}{\partial x^2} +
2m_f U \frac{\partial^2 y}{\partial x \partial t} + (m_s + m_f)
\frac{\partial^2 y}{\partial t^2} = 0
$$

where:

- $EI$ = flexural rigidity
- $m_s$ = pipe mass per unit length
- $m_f = \rho_f A_i$ = fluid mass per unit length ($A_i$ = internal cross-section area)
- The $m_f U^2$ term acts as a compressive follower force
- The $2m_f U$ term is a Coriolis/gyroscopic term

### Critical Flow Velocity

For a simply supported pipe the critical velocity for divergence (buckling) is:

$$
U_{cr} = \frac{\pi}{L} \sqrt{\frac{EI}{m_f}}
$$

For a cantilevered pipe the instability is **flutter** (oscillatory), occurring at a higher velocity than divergence.

### Practical Implications

- Offshore flexible risers and flowlines carry high-velocity hydrocarbons
- Nuclear power plant piping must resist flow-induced vibration from coolant
- Hydraulic hose assemblies can vibrate at resonant frequencies set by flow velocity

## Worked Example 1: Added Mass Effect on Subsea Module

**Given:**

- Subsea module approximated as a rectangular box: $3 \times 3 \times 2$ m
- Module mass in air: $m_s = 15{,}000$ kg
- Added mass coefficient for heave: $C_a = 0.68$ (from panel method)
- Displaced volume: $\mathcal{V} = 18$ m³, seawater $\rho = 1025$ kg/m³

**Find:** Effective mass during lift through the splash zone and the period of heave oscillation if suspended on a crane wire of stiffness $k = 500$ kN/m.

**Solution:**

Added mass:

$$
m_a = C_a \rho \mathcal{V} = 0.68 \times 1025 \times 18 = 12{,}546 \text{ kg}
$$

Effective mass:

$$
m_{eff} = m_s + m_a = 15{,}000 + 12{,}546 = 27{,}546 \text{ kg}
$$

Natural period of heave oscillation:

$$
T_n = 2\pi \sqrt{\frac{m_{eff}}{k}} = 2\pi \sqrt{\frac{27{,}546}{500{,}000}} = 1.47
\text{ s}
$$

The added mass nearly **doubles** the effective inertia, significantly increasing the oscillation period compared to the in-air case ($T_{air} = 1.09$ s).

## Worked Example 2: Whipping Bending Moment

**Given:**

- Container ship: $L = 350$ m, first flexural natural frequency $f_1 = 0.45$ Hz (wet)
- Rigid-body wave bending moment: $M_{wave} = 8{,}000$ MN·m (sagging)
- Bow slam impulse excites the first mode with an initial velocity $\dot{q}_1(0)$
- Modal mass $m_1 = 50{,}000$ tonnes, damping ratio $\zeta = 0.015$

**Find:** Whipping bending moment if the slam impulse $I = 5{,}000$ kN·s.

**Solution:**

Initial modal velocity:

$$
\dot{q}_1(0) = \frac{I}{m_1} = \frac{5 \times 10^6}{5 \times 10^7} = 0.10 \text{ m/s}
$$

Peak modal displacement (free vibration decay envelope):

$$
q_{1,max} = \frac{\dot{q}_1(0)}{\omega_1} = \frac{0.10}{2\pi \times 0.45} = 0.0354
\text{ m}
$$

The product of modal stiffness and modal displacement is the peak modal restoring **force**, not a bending moment:

$$
k_1 q_{1,max} = \omega_1^2 m_1 q_{1,max} = (2.83)^2 \times 5 \times 10^7 \times 0.0354
\approx 1.41 \times 10^7 \text{ N}
$$

Converting this to a hull-girder bending moment requires the modal bending-moment distribution, $M_{whip}(x) = EI(x)\,\phi_1''(x)\,q_{1,max}$, which depends on the mode shape and its normalisation and is not given here. For large container ships the whipping contribution is typically 30–50% of the wave bending moment, i.e. about 2,400–4,000 MN·m for this ship. Real slam loads are also spread in time and space rather than being a single ideal impulse, which reduces the modal response. The example illustrates why **whipping cannot be ignored** in modern hull girder design.

## Worked Example 3: Critical Velocity for a Fluid-Conveying Pipe

**Given:**

- Simply supported pipe: $L = 6$ m, outer diameter $D_o = 0.15$ m, wall thickness $t = 0.01$ m
- Steel: $E = 210$ GPa, $\rho_s = 7850$ kg/m³
- Internal fluid: water, $\rho_f = 1000$ kg/m³

**Find:** Critical flow velocity for divergence.

**Solution:**

Internal area: $A_i = \pi(D_o - 2t)^2/4 = \pi(0.13)^2/4 = 0.01327$ m²

Moment of inertia: $I = \pi(D_o^4 - D_i^4)/64 = \pi(0.15^4 - 0.13^4)/64 = 1.083 \times 10^{-5}$ m⁴

Flexural rigidity: $EI = 210 \times 10^9 \times 1.083 \times 10^{-5} = 2.274 \times 10^6$ N·m²

Fluid mass per unit length: $m_f = \rho_f A_i = 1000 \times 0.01327 = 13.27$ kg/m

Critical velocity:

$$
U_{cr} = \frac{\pi}{L} \sqrt{\frac{EI}{m_f}} = \frac{\pi}{6}
\sqrt{\frac{2.274 \times 10^6}{13.27}} = 0.524 \times 414.0 = 217 \text{ m/s}
$$

This is well above typical pipeline flow velocities ($< 10$ m/s), so divergence instability is not a concern for this configuration. However, for longer, more flexible pipes (e.g., elastomeric hoses) the critical velocity can be much lower.

## Applications in Marine and Offshore Engineering

### Ship Design

- Hull girder strength must account for hydroelastic (springing and whipping) loads
- Classification rules (IACS, DNV, Lloyd's) now include hydroelastic load components
- Fatigue damage from springing can contribute 30% or more of the total midships fatigue

### Offshore Platform Installation

- Heavy lifts through the splash zone require added mass in dynamic analysis
- Lowering operations use heave compensators tuned to the wet natural frequency
- Hydrodynamic slam loads on flat-bottomed modules can govern lifting sling design

### Flexible Risers and Umbilicals

- Internal flow effects are included in global riser analysis
- VIV interaction with hydroelastic response determines fatigue life
- Cross-section deformation (ovalisation) under pressure is a hydroelastic problem

### Underwater Vehicles and Submarines

- Added mass dominates the inertial properties, especially in pitch and yaw
- Manoeuvring simulation requires frequency-dependent hydrodynamic coefficients
- Torpedo launch transients involve impulsive hydroelastic loading

### Tidal and Wave Energy Devices

- Flexible turbine blades interact with unsteady tidal flow
- Wave energy converters rely on radiation damping for power extraction
- Optimising the power capture requires tuning of hydroelastic parameters:

$$
P_{max} = \frac{|F_{exc}|^2}{8 b_{rad}}
$$

where $b_{rad}$ is the radiation damping coefficient at resonance.

## Design Considerations

### Modelling Fidelity

- Simple beam + strip theory models are fast and suitable for preliminary design
- Full 3-D panel method + FE coupling is needed for detailed design
- CFD coupling is required for impact and highly nonlinear events

### Frequency Dependence

- Added mass and radiation damping are functions of oscillation frequency
- Low-frequency modes see higher added mass than high-frequency modes
- Frequency-domain analysis handles this naturally; time-domain requires convolution integrals or state-space approximations

### Validation

- Model basin tests with flexible models (segmented or continuous backbone) validate hydroelastic predictions
- Full-scale monitoring (strain gauges, accelerometers) on ships and platforms provides validation data
- Benchmark cases (e.g., ISSC comparative studies) are used to verify numerical tools

Hydroelasticity extends classical structural analysis into the fluid domain, revealing phenomena that rigid-body assumptions cannot capture. For modern marine and offshore structures, hydroelastic analysis is increasingly a design requirement rather than an academic exercise.

## Exercises

**Exercise 1.** A steel pipe of outer diameter 0.5 m has structural mass 150 kg/m (empty, ends sealed) and oscillates transversely in seawater ($\rho = 1025$ kg/m³). Using $C_a = 1.0$, find the added mass per unit length and the percentage reduction of the natural frequency compared with the in-air value.

<details>
<summary>Answer</summary>

```math
m_a = C_a\rho \frac{\pi D^2}{4} = 1025 \times \frac{\pi \times 0.25}{4} = 201
\text{ kg/m}
```

```math
\frac{f_{n,fluid}}{f_{n,vacuum}} = \sqrt{\frac{150}{150 + 201}} = 0.653
```

The natural frequency drops by about 35%.

</details>

**Exercise 2.** Classify each effect as hydrostatic, hydrokinetic or hydroinertial: (a) the change in buoyancy as a floating module heaves; (b) the energy radiated away as waves by a heaving buoy; (c) the added mass that resists a hull during a slam. Then explain why a partitioned FSI scheme can become unstable when $m_a > m_s$.

<details>
<summary>Answer</summary>

(a) Hydrostatic (depends on displacement). (b) Hydrokinetic (radiation damping depends on velocity). (c) Hydroinertial (depends on acceleration).

In a staggered scheme the fluid force is computed from the previous structural acceleration: $m_s\ddot{x}^{(i+1)} = F - m_a\ddot{x}^{(i)}$. An error in the acceleration therefore evolves as $e^{(i+1)} = -(m_a/m_s)\,e^{(i)}$. It grows, with alternating sign, whenever $m_a/m_s > 1$, which is typical of light structures in water and of blood-vessel models. Relaxation, strong coupling or monolithic schemes are needed in that case.

</details>

**Exercise 3.** For the pipe of Example 3, how long would a simply supported span have to be for the divergence velocity to drop to 10 m/s? Comment on the result.

<details>
<summary>Answer</summary>

```math
L = \frac{\pi}{U_{cr}} \sqrt{\frac{EI}{m_f}} = \frac{\pi}{10} \times 414.0 = 130
\text{ m}
```

A 130 m unsupported steel span is unrealistic, so divergence is not a practical concern for stiff steel piping at normal flow speeds. It becomes relevant for soft hoses, where $EI$ is orders of magnitude smaller.

</details>

**Exercise 4.** A heaving wave energy converter at resonance is driven by an excitation force of amplitude $|F_{exc}|$ and has radiation damping $b_{rad}$. A power take-off adds linear damping $b_{pto}$. Show that the absorbed power is maximized when $b_{pto} = b_{rad}$ and that $P_{max} = |F_{exc}|^2/(8b_{rad})$. Evaluate it for $|F_{exc}| = 500$ kN and $b_{rad} = 200$ kN·s/m.

<details>
<summary>Answer</summary>

At resonance the inertia and stiffness terms cancel, so the velocity amplitude is $V = |F_{exc}|/(b_{rad} + b_{pto})$. The mean absorbed power is

```math
P = \frac{1}{2}b_{pto}V^2 = \frac{1}{2} \frac{b_{pto}|F_{exc}|^2}{(b_{rad} + b_{pto})^2}
```

Setting $dP/db_{pto} = 0$ gives $b_{pto} = b_{rad}$, and then $P_{max} = \frac{|F_{exc}|^2}{8b_{rad}}$.

```math
P_{max} = \frac{(5 \times 10^5)^2}{8 \times 2 \times 10^5} = 156 \text{ kW}
```

</details>

**Exercise 5.** For the subsea module of Example 1 ($m_{eff} = 27\,546$ kg in water), what crane-wire stiffness would keep the heave natural period below 1.0 s? Why is it important to use the wet effective mass rather than the dry mass in this check?

<details>
<summary>Answer</summary>

```math
k \geq \frac{4\pi^2 m_{eff}}{T_n^2} = 39.48 \times 27\,546 = 1.09 \text{ MN/m}
```

Using only the dry mass (15 000 kg) would suggest that 0.59 MN/m is enough. With that stiffness the real submerged system would have a period of about 1.36 s, closer to the range excited by vessel motion and waves. Added mass nearly doubles the inertia, so resonance checks, heave-compensator tuning and snap-load assessments must use wet properties.

</details>

## References

- R. E. D. Bishop, W. G. Price, *Hydroelasticity of Ships*, Cambridge University Press, 1979.
- J. N. Newman, *Marine Hydrodynamics*, MIT Press, 1977.
- O. M. Faltinsen, *Sea Loads on Ships and Offshore Structures*, Cambridge University Press, 1990.
- M. P. Païdoussis, *Fluid-Structure Interactions: Slender Structures and Axial Flow*, Vol. 1, Academic Press, 1998.
- T. I. Fossen, *Handbook of Marine Craft Hydrodynamics and Motion Control*, Wiley, 2011.
