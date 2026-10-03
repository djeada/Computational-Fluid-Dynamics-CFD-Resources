# Friction and Its Applications

Friction is the resistive force that opposes the relative motion or tendency of motion between two surfaces in contact. It plays a critical role in the design and analysis of mechanical systems, from simple inclined planes to complex braking systems and power transmission devices.

## Dry Friction (Coulomb Friction)

### Basic Model

Dry friction, also called **Coulomb friction**, arises between non-lubricated surfaces. The friction force $f$ is governed by:

$$
f \leq \mu_s N
$$

where $\mu_s$ is the coefficient of static friction and $N$ is the normal force between the surfaces. This inequality means the friction force adjusts to whatever value is needed to maintain equilibrium, up to a maximum of $\mu_s N$.

### Friction Force Regimes

The friction force transitions through distinct regimes:

- **No motion (static)**: $f < \mu_s N$ — the friction force equals the applied tangential force
- **Impending motion**: $f = \mu_s N$ — the maximum static friction is reached
- **Sliding (kinetic)**: $f = \mu_k N$ — the friction force drops to the kinetic value

Typically $\mu_k < \mu_s$, meaning less force is needed to maintain sliding than to initiate it.

## Static vs Kinetic Friction

| Property | Static Friction | Kinetic Friction |
| --- | --- | --- |
| Symbol | $\mu_s$ | $\mu_k$ |
| Condition | No relative motion | Surfaces sliding |
| Magnitude | $0 \leq f \leq \mu_s N$ | $f = \mu_k N$ |
| Typical values (steel on steel) | 0.6–0.8 | 0.4–0.6 |
| Typical values (rubber on concrete) | 0.8–1.0 | 0.6–0.8 |

### Angle of Friction

The **angle of static friction** $\phi_s$ is defined as:

$$
\phi_s = \tan^{-1}(\mu_s)
$$

This is the angle that the resultant of $N$ and $f_{max}$ makes with the normal. A body on an inclined surface will begin to slide when the inclination angle exceeds $\phi_s$.

## Friction on Inclined Planes

### Block on an Incline

For a block of weight $W$ on a plane inclined at angle $\theta$:

**Normal force:**

$$
N = W\cos\theta
$$

**Friction force required for equilibrium:**

$$
f = W\sin\theta
$$

**Condition for impending slip:**

$$
W\sin\theta = \mu_s W\cos\theta
$$

$$
\tan\theta = \mu_s
$$

$$
\theta_{critical} = \tan^{-1}(\mu_s) = \phi_s
$$

### Pushing or Pulling on an Incline

If an external force $P$ is applied at angle $\alpha$ above the horizontal to push a block up an incline at angle $\theta$:

$$
\sum F_{\parallel} = P\cos(\alpha - \theta) - W\sin\theta - \mu_s N = 0
$$

$$
\sum F_{\perp} = N - W\cos\theta + P\sin(\alpha - \theta) = 0
$$

The optimal pushing angle to minimize $P$ is $\alpha = \theta + \phi_s$.

## Wedges

A **wedge** is a simple machine that converts a small input force into a large output force through friction and geometry.

### Analysis of a Wedge

For a wedge with angle $\alpha$ used to lift a block of weight $W$, the applied force $P$ required at impending motion is found by analyzing each body separately:

For the block (free body 1):

$$
\sum F_y = N_2\cos\alpha - \mu_s N_2\sin\alpha - W = 0
$$

For the wedge (free body 2):

$$
\sum F_x = P - \mu_s N_1 - N_2\sin\alpha - \mu_s N_2\cos\alpha = 0
$$

$$
\sum F_y = N_1 - N_2\cos\alpha + \mu_s N_2\sin\alpha = 0
$$

### Self-Locking Condition

A wedge is **self-locking** (will not slip out on its own) when:

$$
\alpha \leq 2\phi_s
$$

where $\phi_s = \tan^{-1}(\mu_s)$. Physically, there are two friction surfaces acting on the wedge, each capable of resisting slip up to the friction angle $\phi_s$. When the wedge half-angle exceeds $\phi_s$ on both contact faces, the component of the applied load pushing the wedge out overcomes the combined friction resistance, and the wedge slips. The factor of two arises because both the top and bottom surfaces contribute one friction angle each. This is a critical design criterion for wedge-based clamping and lifting devices.

## Belt Friction (Capstan Equation)

### Derivation

When a belt or rope wraps around a cylindrical surface (drum, pulley, or capstan), friction between the belt and the surface creates a tension difference. At impending slip, the relationship between the tight side tension $T_2$ and the slack side tension $T_1$ is:

$$
\frac{T_2}{T_1} = e^{\mu\beta}
$$

where:

- $\mu$ = coefficient of friction between belt and surface
- $\beta$ = total angle of wrap (in radians)
- $T_2 > T_1$

This is the **capstan equation** (or Euler's friction equation).

### Worked Example 1: Capstan

A rope is wrapped 2.5 turns around a bollard. The coefficient of friction is $\mu = 0.3$. The slack side has a tension of 50 N.

**Given:**

- Angle of wrap: $\beta = 2.5 \times 2\pi = 5\pi$ rad
- $\mu = 0.3$
- $T_1 = 50$ N

**Find:** Maximum holding force $T_2$.

**Solution:**

$$
T_2 = T_1 e^{\mu\beta} = 50 \times e^{0.3 \times 5\pi}
$$

$$
T_2 = 50 \times e^{4.712}
$$

$$
T_2 = 50 \times 111.3 = 5565 \text{ N}
$$

A person applying only 50 N can hold a load of 5565 N — a mechanical advantage of over 111:1.

## Screws and Thread Friction

### Square-Threaded Screw

A screw converts rotational motion into linear motion. For a square-threaded screw with:

- Mean radius: $r$
- Lead (axial advance per turn): $l$
- Lead angle: $\theta = \tan^{-1}\left(\frac{l}{2\pi r}\right)$

**Moment to raise a load $W$:**

$$
M_{raise} = Wr\tan(\theta + \phi_s)
$$

**Moment to lower a load $W$:**

$$
M_{lower} = Wr\tan(\phi_s - \theta)
$$

### Self-Locking Screw

A screw is self-locking (will not unwind under load) when:

$$
\theta \leq \phi_s
$$

or equivalently:

$$
\mu_s \geq \frac{l}{2\pi r}
$$

### Efficiency of a Screw

The mechanical efficiency of a screw jack is:

$$
\eta = \frac{\tan\theta}{\tan(\theta + \phi_s)}
$$

Maximum efficiency occurs at $\theta = 45^\circ - \phi_s/2$.

## Worked Example 2: Block on an Incline

A 200 N block rests on a 25° inclined plane. The coefficient of static friction is $\mu_s = 0.4$. A horizontal force $P$ is applied to prevent the block from sliding down.

**Given:**

- Weight: $W = 200$ N
- Incline angle: $\theta = 25^\circ$
- $\mu_s = 0.4$

**Find:** Minimum horizontal force $P$ to prevent sliding.

**Solution:**

Resolve forces parallel and perpendicular to the incline:

$$
\sum F_{\perp} = N - W\cos\theta - P\sin\theta = 0
$$

$$
N = 200\cos25^\circ + P\sin25^\circ = 181.3 + 0.4226P
$$

At impending motion (block about to slide down), friction acts up the incline:

$$
\sum F_{\parallel} = P\cos\theta + \mu_s N - W\sin\theta = 0
$$

$$
P\cos25^\circ + 0.4(181.3 + 0.4226P) - 200\sin25^\circ = 0
$$

$$
0.9063P + 72.50 + 0.1690P - 84.52 = 0
$$

$$
1.0753P = 12.02
$$

$$
P = 11.18 \text{ N}
$$

A horizontal force of approximately 11.2 N prevents the block from sliding.

## Applications

### Brakes and Clutches

- **Disc brakes**: Friction between pads and rotor converts kinetic energy to heat
- **Band brakes**: Belt friction (the capstan equation) governs the contact between band and drum
- **Clutches**: Friction transmits torque between driving and driven shafts

### Fasteners

- **Bolted joints**: Thread friction provides clamping force and self-locking
- **Wedge anchors**: Friction and geometry combine for secure anchorage
- **Set screws**: Rely on friction at the tip to prevent relative motion

### Power Transmission

- **Belt drives**: Capstan equation governs the torque capacity of V-belts and flat belts
- **Rope brakes**: Used in hoisting and mooring applications
- **Conveyor belts**: Friction drives the belt and prevents slippage

### Everyday Applications

- **Walking**: Static friction between shoe and ground provides the propulsive force
- **Vehicle tires**: Friction determines braking distance and cornering ability
- **Door wedges**: Self-locking wedge principle keeps doors open

## Practical Tips

- Always determine whether the problem involves impending motion or actual sliding before selecting $\mu_s$ or $\mu_k$
- Draw free body diagrams carefully, showing friction in the correct direction (opposing the tendency of motion)
- For wedge problems, analyze each body separately and apply Newton's third law at contact surfaces
- In belt friction problems, ensure angles are converted to radians before using the capstan equation
- Check the self-locking condition for any wedge or screw design to ensure safety under load

Friction analysis is essential for designing safe and functional mechanical systems. From the simplest inclined plane to sophisticated braking mechanisms, the principles of Coulomb friction, belt friction, and screw mechanics provide the analytical framework for engineering design.

## Exercises

**Exercise 1.** A 50 kg crate rests on a 20° ramp with $\mu_s = 0.3$. (a) Does it stay put on its own? (b) What force parallel to the ramp is needed to just hold it? (c) What force parallel to the ramp is needed to start pushing it up?

<details>
<summary>Answer</summary>

(a) $\tan 20^\circ = 0.364 > 0.3$, so the incline is steeper than the friction angle ($16.7^\circ$) and the crate slides.

$W = 490.5$ N, so $N = W\cos 20^\circ = 460.9$ N and $W\sin 20^\circ = 167.8$ N.

(b) Friction acts up the slope: $P = 167.8 - 0.3(460.9) = 29.5$ N.

(c) Friction acts down the slope: $P = 167.8 + 0.3(460.9) = 306.0$ N.

</details>

**Exercise 2.** A sailor must hold a 10 kN load with a pull of 100 N by wrapping the rope around a bollard with $\mu = 0.25$. How many full turns are needed?

<details>
<summary>Answer</summary>

```math
\beta = \frac{\ln(T_2/T_1)}{\mu} = \frac{\ln 100}{0.25} = 18.42 \text{ rad} = 2.93
\text{ turns}
```

Use 3 full turns, which give $e^{0.25 \times 6\pi} = 111$, enough to hold 11.1 kN with 100 N.

</details>

**Exercise 3.** A square-threaded screw jack has a mean diameter of 30 mm, a lead of 6 mm and $\mu_s = 0.15$. It supports $W = 20$ kN. Find the lead angle, the moments needed to raise and lower the load, whether the screw is self-locking, and its efficiency when raising.

<details>
<summary>Answer</summary>

$\theta = \tan^{-1}[6/(2\pi \times 15)] = 3.64^\circ$ and $\phi_s = \tan^{-1}0.15 = 8.53^\circ$.

```math
M_{raise} = Wr\tan(\theta + \phi_s) = 20\,000 \times 0.015 \times \tan
12.17^\circ = 64.7 \text{ N}\cdot \text{m}
```

```math
M_{lower} = Wr\tan(\phi_s - \theta) = 300 \times \tan 4.89^\circ = 25.7 \text{ N}\cdot
\text{m}
```

The screw is self-locking because $\theta < \phi_s$. Efficiency: $\eta = \tan 3.64^\circ/\tan 12.17^\circ = 0.295$. The low efficiency is the price of self-locking.

</details>

**Exercise 4.** Show that the force $P$ needed to push a block of weight $W$ up an incline $\theta$, with $P$ applied at angle $\alpha$ above the horizontal, is least when $\alpha = \theta + \phi_s$, and that the minimum is $P_{min} = W\sin(\theta + \phi_s)$. Evaluate it for $W = 200$ N, $\theta = 25^\circ$, $\mu_s = 0.4$.

<details>
<summary>Answer</summary>

Eliminating $N$ from the two equilibrium equations gives

```math
P = \frac{W(\sin\theta + \mu_s\cos\theta)}{\cos(\alpha - \theta) + \mu_s\sin(\alpha - \theta)}
```

Substitute $\mu_s = \tan\phi_s$ and multiply top and bottom by $\cos\phi_s$:

```math
P = \frac{W\sin(\theta + \phi_s)}{\cos(\alpha - \theta - \phi_s)}
```

The denominator is largest (equal to 1) when $\alpha = \theta + \phi_s$, so $P_{min} = W\sin(\theta + \phi_s)$.

Numbers: $\phi_s = 21.80^\circ$, $\alpha = 46.8^\circ$, $P_{min} = 200\sin 46.8^\circ = 145.8$ N. A numerical sweep over $\alpha$ confirms this.

</details>

**Exercise 5.** A flat belt wraps $160^\circ$ around a 200 mm diameter pulley with $\mu = 0.3$. The tight-side tension may not exceed 1.2 kN. Find the slack-side tension, the maximum torque and the power transmitted at 1500 rpm.

<details>
<summary>Answer</summary>

$\beta = 160^\circ = 2.793$ rad, so $e^{\mu\beta} = e^{0.838} = 2.311$.

$T_1 = 1200/2.311 = 519$ N, and $T_2 - T_1 = 681$ N.

Torque: $(T_2 - T_1)r = 681 \times 0.1 = 68.1$ N·m. Power: $68.1 \times 157.1 = 10.7$ kW.

</details>

## References

- Hibbeler, R. C., *Engineering Mechanics: Statics*, 14th ed., Pearson, 2016.
- Meriam, J. L., and Kraige, L. G., *Engineering Mechanics: Statics*, Wiley.
- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*, 10th ed., McGraw-Hill Education, 2015.
