# Impulse and Momentum

The principle of impulse and momentum is Newton's second law integrated over time. It relates the impulse of the forces over an interval to the change in linear and angular momentum, which makes it the natural tool when forces act for a known time, when they are too large and brief to measure (impacts), or when mass enters or leaves the system (jets, rockets). This note covers linear and angular impulse–momentum for particles, systems and rigid bodies, conservation of momentum, central and oblique impact with the coefficient of restitution, steady mass flow through a control volume, and variable-mass systems with the rocket equation. The position-based counterpart is [Work and Energy Methods](work_energy.md).

## Problem Statement

A particle, a system of particles or a rigid body is acted on by forces whose time history is known, or by impulsive contact forces whose history is unknown but whose duration is short; or a stream of mass enters and leaves a body. Given the velocities and angular velocities before an interval and the impulses of the external forces, find the velocities after it; or, given the change of motion, find the impulse, the average force or the thrust. For impacts the bodies are rigid except at the contact, the contact is smooth unless stated, and non-impulsive forces such as gravity are neglected during the impact. The governing equations are

```math
m\mathbf{v}_{G1} + \sum\int_{t_1}^{t_2}\mathbf{F}\, dt = m\mathbf{v}_{G2},
\qquad \mathbf{H}_{O1} + \sum\int_{t_1}^{t_2}\mathbf{M}_O\, dt = \mathbf{H}_{O2}
```

with $O$ a fixed point or the mass centre, supplemented for impacts by the coefficient of restitution and for variable-mass systems by the momentum flux of the ejected mass. Impulse is in N·s, linear momentum in kg·m/s and angular momentum in kg·m²/s.

## Linear Impulse and Momentum

The linear momentum of a particle is $\mathbf{L} = m\mathbf{v}$, and the second law is $\sum\mathbf{F} = d\mathbf{L}/dt$. Integrating over $t_1 \le t \le t_2$,

```math
m\mathbf{v}_1 + \sum\int_{t_1}^{t_2}\mathbf{F}\, dt = m\mathbf{v}_2
```

The integral is the linear impulse of the force. For a constant force it is $\mathbf{F}\Delta t$, and for any force the average force over the interval is $\bar{\mathbf{F}} = m(\mathbf{v}_2 - \mathbf{v}_1)/\Delta t$. For a system of particles, internal forces cancel in pairs, and the total momentum is $m\mathbf{v}_G$, so the same equation holds with the external forces and the velocity of the mass centre.

When the resultant external impulse in some direction is zero, the momentum of the system in that direction is conserved. This holds exactly for an isolated system, and very nearly during an impact or an explosion, where the internal forces are so much larger than gravity or friction that the external impulse over the short interval is negligible.

## Angular Impulse and Momentum

The angular momentum of a particle about a fixed point $O$ is $\mathbf{H}_O = \mathbf{r} \times m\mathbf{v}$, which in the plane is $mvd$ with $d$ the perpendicular distance from $O$ to the line of $m\mathbf{v}$. Its rate of change is the moment of the forces, $\sum\mathbf{M}_O = \dot{\mathbf{H}}_O$. For a rigid body in plane motion,

$$
H_G = I_G\omega,
\qquad H_O = I_G\omega +
\left(\mathbf{r}_{G/O} \times m\mathbf{v}_G\right)\cdot\mathbf{k}
$$

which for rotation about a fixed axis through $O$ is $H_O = I_O\omega$. Integrating over time,

```math
(H_O)_1 + \sum\int_{t_1}^{t_2}M_O\, dt = (H_O)_2
```

When the external forces have no moment about $O$, angular momentum about $O$ is conserved. A body that changes its own moment of inertia by internal forces, such as a skater pulling in her arms or a satellite deploying booms, changes its spin rate as $I_1\omega_1 = I_2\omega_2$, and its kinetic energy changes by the work of the internal forces (Exercise 4).

## Impact

An impact is a collision over a short time $\Delta t$ during which large contact forces act. The line of impact is the common normal to the surfaces at the contact. The impact is central when the mass centres lie on the line of impact, and oblique when the velocities have components across it.

### Coefficient of Restitution

The contact force has a deformation phase, until the bodies move at the same normal speed, and a restitution phase, during which they separate. The ratio of the restitution impulse to the deformation impulse is the coefficient of restitution, which for particles reduces to the ratio of the normal separation speed to the normal approach speed:

$$
e = \frac{v_{B2} - v_{A2}}{v_{A1} - v_{B1}}
$$

$e = 1$ is a perfectly elastic impact with no loss of kinetic energy, $e = 0$ a perfectly plastic one in which the bodies move together afterwards. In practice $e$ depends on the materials, the shape and the impact speed, and decreases as the speed increases.

### Central Impact

Momentum conservation and the restitution equation give two equations for the two final velocities:

```math
m_Av_{A1} + m_Bv_{B1} = m_Av_{A2} + m_Bv_{B2},
\qquad v_{B2} - v_{A2} = e\,(v_{A1} - v_{B1})
```

Writing the kinetic energy as the energy of the mass centre plus the energy of relative motion shows that the loss is

```math
\Delta T = \frac{1}{2}\, \frac{m_Am_B}{m_A + m_B}\,(1 - e^2)\,(v_{A1} - v_{B1})^2
```

A 2 kg ball moving at 6 m/s hits a stationary 3 kg ball with $e = 0.7$. The equations give $12 = 2v_{A2} + 3v_{B2}$ and $v_{B2} - v_{A2} = 4.2$, so $v_{A2} = -0.12$ m/s (a small rebound) and $v_{B2} = 4.08$ m/s. The loss is $\tfrac{1}{2}(1.2)(0.51)(36) = 11.0$ J of the initial 36 J.

### Oblique Impact

For smooth bodies the contact force acts only along the line of impact $n$. Along $n$, momentum conservation and restitution apply as for central impact; along the tangent $t$, the momentum of each body separately is unchanged. A ball hitting a fixed smooth wall at 10 m/s and $40^\circ$ to the wall with $e = 0.8$ keeps $v_t = 10\cos 40^\circ = 7.66$ m/s and leaves with $v_n = 0.8 \times 10\sin 40^\circ = 5.14$ m/s, so it rebounds at 9.23 m/s and $33.9^\circ$ to the wall.

### Impact Followed by Motion

Impact problems usually combine two principles: momentum across the impact, where energy is lost, and energy before or after it, where momentum is not conserved because gravity acts over a finite time. In the ballistic pendulum, a 10 g bullet embeds in a 2 kg block hung as a pendulum, which then swings up 0.15 m. After the impact, energy conservation gives the common speed $v' = \sqrt{2gh} = 1.716$ m/s; across the impact, momentum gives

$$
m_bv_0 = (m_b + m_B)v' \quad\Rightarrow\quad v_0 = \frac{2.01 \times 1.716}{0.01} = 345
\text{ m/s}
$$

The bullet's 595 J of kinetic energy is reduced to 3.0 J by the impact; using energy conservation across it would be badly wrong.

## Steady Mass Flow

For a control volume through which mass flows steadily, such as a pipe bend, a nozzle or a turbine blade passage, the impulse–momentum principle applied to the mass inside and the mass crossing the boundary in $dt$ gives

```math
\sum\mathbf{F} = \dot{m}\,(\mathbf{v}_{\mathrm{out}} - \mathbf{v}_{\mathrm{in}})
```

where $\sum\mathbf{F}$ includes pressure forces on the inlet and outlet. A water jet of area 0.002 m² at 20 m/s ($\dot{m} = 40$ kg/s) turned through $120^\circ$ by a fixed vane at atmospheric pressure needs a force on the water of $\dot{m}V(\cos 120^\circ - 1) = -1200$ N along the jet and $\dot{m}V\sin 120^\circ = 693$ N across it; the vane feels the opposite, 1386 N in total. This is the integral form of the momentum equation solved cell by cell in CFD (see [Navier-Stokes Equations](../../fluid_mechanics/governing_equations/navier_stokes.md)), and the same balance gives the reaction forces that fluid loads put on structures.

## Variable-Mass Systems and the Rocket Equation

A rocket of mass $m$ moving at $v$ ejects $`\dot{m}\,dt`$ of propellant in $dt$ at speed $v_e$ relative to itself. Applying impulse–momentum to the rocket and the ejected mass together over $dt$, with external force $\sum F$ (gravity, drag),

```math
\sum F\, dt = \left[(m - \dot{m}\, dt)(v + dv) + \dot{m}\, dt\,(v - v_e)\right] - mv
\quad\Rightarrow\quad m \frac{dv}{dt} = \dot{m}\, v_e + \sum F
```

The term $\dot{m}v_e$ is the thrust (plus $(p_e - p_a)A_e$ if the nozzle exit pressure differs from ambient). With no external force, $`dv = -v_e\,dm/m`$ integrates to the Tsiolkovsky rocket equation

$$
\Delta v = v_e\ln \frac{m_0}{m_f}
$$

which depends only on the exhaust speed and the mass ratio. A 1000 kg rocket in space exhausting 50 kg/s at 3000 m/s has a thrust of 150 kN, and after 10 s, at 500 kg, it has gained $3000\ln 2 = 2079$ m/s.

With gravity and drag the speed at burnout is the ideal $\Delta v$ minus the gravity loss $`\int g\,dt`$ and the drag loss $`\int D/m\,dt`$.

![Speed and altitude of a vertically launched rocket and its burnout speed budget](../../../scripts/algorithms/dynamics_variable_mass_rocket/dynamics_variable_mass_rocket.png)

For a 1000 kg rocket burning 700 kg of propellant at 10 kg/s with $v_e = 2500$ m/s, panel (a) shows the ideal curve $v_e\ln(m_0/m)$, the closed-form solution with constant gravity (matched by the RK45 markers) and the solution with drag. Panel (c) shows the budget at burnout: 3010 m/s ideal, 687 m/s lost to gravity over the 70 s burn and 341 m/s to drag, leaving 1983 m/s at 50 km. A short burn reduces the gravity loss, which is why launchers need a lift-off thrust well above their weight.

## Common Mistakes

1. Applying conservation of energy across an impact or a plastic collision.
2. Applying restitution to the tangential velocity components in an oblique impact.
3. Forgetting the sign of velocities in the restitution equation; write all velocities positive in one direction along the line of impact.
4. Taking angular momentum about a moving point other than the mass centre with the fixed-point formula.
5. Writing $\mathbf{F} = d(m\mathbf{v})/dt$ for a rocket, which counts the ejected momentum wrongly; use $`m\,d\mathbf{v}/dt = \dot{m}\mathbf{v}_e + \sum\mathbf{F}`$.

## Key Takeaways

- Impulse equals the change in momentum, linear for the mass centre and angular about a fixed point or the mass centre.
- Momentum is conserved in any direction with zero external impulse, which during an impact means almost every direction.
- The coefficient of restitution closes the impact equations; the kinetic energy lost is $\tfrac{1}{2}\mu(1 - e^2)v_{\mathrm{rel}}^2$.
- Steady flow through a control volume needs a force $`\dot{m}(\mathbf{v}_{\mathrm{out}} - \mathbf{v}_{\mathrm{in}})`$.
- A rocket gains $v_e\ln(m_0/m_f)$ in free space; gravity and drag losses come off that.

## Related Scripts

- [Variable-Mass Rocket](../../../scripts/algorithms/dynamics_variable_mass_rocket/): integrates the momentum balance of a vertically launched rocket and splits its burnout speed into the ideal rocket-equation increment, the gravity loss and the drag loss.
- [Torque-Free Rigid Body Rotation](../../../scripts/algorithms/dynamics_torque_free_rigid_body/): integrates Euler's equations for a rigid box spinning with no applied moment and shows that rotation about the axis of intermediate moment of inertia is unstable.

## Exercises

**Exercise 1.** A 0.15 kg ball arrives at a bat at 30 m/s and leaves at 40 m/s in the opposite direction. The contact lasts 0.01 s. Find the impulse on the ball and the average contact force.

<details>
<summary>Answer</summary>

Taking the outgoing direction as positive, the impulse is $m(v_2 - v_1) = 0.15(40 - (-30)) = 10.5$ N·s, and the average force is $10.5/0.01 = 1050$ N in the outgoing direction.

</details>

**Exercise 2.** A 4 kg block at rest on a frictionless horizontal surface is pushed by a force $F(t) = 200t$ N for $0 \le t \le 0.5$ s. Find its speed at $t = 0.5$ s.

<details>
<summary>Answer</summary>

```math
\int_0^{0.5}200t\,dt = 100(0.5)^2 = 25 \text{ N·s},
\qquad
v_2 = \frac{25}{4} = 6.25 \text{ m/s}
```

</details>

**Exercise 3.** Derive the energy loss of a direct central impact, $\Delta T = \tfrac{1}{2}\mu(1 - e^2)(v_{A1} - v_{B1})^2$ with $\mu = m_Am_B/(m_A + m_B)$, and check it against the 2 kg and 3 kg example.

<details>
<summary>Answer</summary>

The kinetic energy of two particles is the energy of the mass centre plus that of the relative motion:

```math
T = \tfrac{1}{2}(m_A + m_B)v_G^2 + \tfrac{1}{2}\mu v_{\mathrm{rel}}^2,
\qquad
v_{\mathrm{rel}} = v_A - v_B
```

Momentum conservation keeps $v_G$ unchanged, and restitution gives $`v_{\mathrm{rel},2} = -e\,v_{\mathrm{rel},1}`$. Hence $\Delta T = T_1 - T_2 = \tfrac{1}{2}\mu(1 - e^2)v_{\mathrm{rel},1}^2$.

For the example $\mu = 6/5 = 1.2$ kg, so $\Delta T = 0.5 \times 1.2 \times 0.51 \times 36 = 11.0$ J, which matches.

</details>

**Exercise 4.** A skater spins at 2 rev/s with a moment of inertia of 3.5 kg·m², then pulls in her arms to reduce it to 1.2 kg·m². Find the new spin rate and the kinetic energy before and after. Where does the extra energy come from?

<details>
<summary>Answer</summary>

```math
\omega_2 = \frac{I_1}{I_2}\omega_1 = \frac{3.5}{1.2} \times 2 = 5.83 \text{ rev/s}
```

$T_1 = \tfrac{1}{2}(3.5)(4\pi)^2 = 276$ J and $T_2 = \tfrac{1}{2}(1.2)(2\pi \times 5.83)^2 = 806$ J.

The internal forces have no net moment about the spin axis, so angular momentum is conserved, but they do work: the extra 530 J is supplied by the skater's muscles pulling the arms inward against the centripetal requirement.

</details>

**Exercise 5.** A smooth ball $A$ moving at 4 m/s strikes an identical stationary ball $B$. At impact the line of centres makes $30^\circ$ with the velocity of $A$, and $e = 0.9$. Find the velocities of both balls after impact.

<details>
<summary>Answer</summary>

Along the line of impact $n$: $v_{An} = 4\cos 30^\circ = 3.464$ m/s. Across it, $v_{At} = 4\sin 30^\circ = 2.0$ m/s, which is unchanged.

For equal masses the momentum and restitution equations along $n$ give

```math
v'_{An} = \frac{1 - e}{2}v_{An} = 0.173 \text{ m/s},
\qquad
v'_{Bn} = \frac{1 + e}{2}v_{An} = 3.291 \text{ m/s}
```

Ball $A$ leaves at $\sqrt{2.0^2 + 0.173^2} = 2.01$ m/s, $4.9^\circ$ from the tangent direction; ball $B$ leaves at 3.29 m/s along the line of centres. Check: $0.173 + 3.291 = 3.464$ m/s, so momentum along $n$ is conserved.

</details>

## References

- R. C. Hibbeler, *Engineering Mechanics: Dynamics*, 14th ed., Pearson, 2016.
- J. L. Meriam, L. G. Kraige and J. N. Bolton, *Engineering Mechanics: Dynamics*, 9th ed., Wiley, 2018.
- F. P. Beer, E. R. Johnston, P. J. Cornwell and B. P. Self, *Vector Mechanics for Engineers: Dynamics*, 12th ed., McGraw-Hill, 2019.
- W. Goldsmith, *Impact: The Theory and Physical Behaviour of Colliding Solids*, Edward Arnold, 1960.
- G. P. Sutton and O. Biblarz, *Rocket Propulsion Elements*, 9th ed., Wiley, 2017.
