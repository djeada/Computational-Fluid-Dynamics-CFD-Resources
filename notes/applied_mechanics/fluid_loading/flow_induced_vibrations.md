# Flow-Induced Vibrations

Flow-induced vibrations (FIV) arise when fluid flow interacts with a structure to produce sustained or growing oscillatory motion. These phenomena are responsible for some of the most dramatic structural failures in engineering history and are a critical design consideration for chimneys, cables, bridges, heat exchangers, and offshore risers.

## Vortex-Induced Vibrations (VIV)

### Mechanism

When a fluid flows past a bluff body, the boundary layer separates and forms an alternating pattern of vortices known as the **von Kármán vortex street**. Each vortex shed from one side induces a transverse (lift) force, creating a periodic excitation.

### Strouhal Number

The non-dimensional shedding frequency is characterised by the Strouhal number:

$$
St = \frac{f_s D}{U}
$$

where:

- $f_s$ = vortex shedding frequency (Hz)
- $D$ = characteristic cross-section dimension (m)
- $U$ = free-stream velocity (m/s)

Typical values:

- Circular cylinder: $St \approx 0.20$ for $300 < Re < 3 \times 10^5$
- Square section: $St \approx 0.13$
- Flat plate normal to flow: $St \approx 0.15$

### Lock-in Phenomenon

When the shedding frequency $f_s$ approaches a structural natural frequency $f_n$, the vortex shedding **synchronises** with the structural motion over a range of velocities. During lock-in:

- The shedding frequency deviates from the Strouhal prediction and locks onto $f_n$
- Vibration amplitude increases significantly (up to $1D$ peak-to-peak for low mass-damping)
- The phenomenon persists over a reduced velocity range $4 \lesssim U_r \lesssim 8$

The reduced velocity is defined as:

$$
U_r = \frac{U}{f_n D}
$$

### VIV Amplitude Estimation

The response amplitude depends on the **mass-damping parameter** (Scruton number):

$$
Sc = \frac{2 m \delta}{\rho D^2}
$$

where $m$ is mass per unit length, $\delta$ is logarithmic decrement of damping, and $\rho$ is fluid density.

For high Scruton numbers ($Sc > 10$ in air), VIV amplitudes are small. For low Scruton numbers (typical in water, $Sc < 5$), amplitudes can reach $A/D \approx 1.0$.

An empirical fit for the maximum cross-flow amplitude is:

$$
\frac{A}{D} \approx \frac{1}{1 + 0.43 \, (2\pi St^2 Sc)}
$$

## Galloping Instability

### Mechanism

**Galloping** is a large-amplitude, low-frequency, single-degree-of-freedom oscillation caused by aerodynamic forces that vary with the angle of attack. Unlike VIV, galloping is a self-excited instability that grows monotonically once a critical velocity is exceeded.

### Den Hartog Criterion

The onset of galloping occurs when the aerodynamic damping becomes negative. For a body oscillating transversely in a steady flow, the instability criterion is:

$$
\frac{dC_L}{d\alpha}\bigg|_{\alpha=0} + C_D < 0
$$

where $C_L$ is the lift coefficient, $C_D$ is the drag coefficient, and $\alpha$ is the angle of attack. This is the **Den Hartog criterion**.

### Critical Velocity

The critical wind speed for galloping onset is:

$$
U_{cr} = \frac{4 m \omega_n \zeta}{\rho D \left| \frac{dC_L}{d\alpha} + C_D \right|}
$$

- Circular cylinders are **immune** to galloping ($dC_L/d\alpha + C_D > 0$)
- Square, D-shaped, and ice-coated sections are highly susceptible
- Galloping amplitudes grow without bound in a linear model; nonlinear aerodynamics limits the response in practice

## Flutter

### Mechanism

**Flutter** is a dynamic aeroelastic instability involving the coupling of two or more structural modes (typically bending and torsion). Energy is extracted from the flow into the structure when the phase relationship between the coupled modes allows net positive work per cycle.

### Binary Flutter of a Bridge Deck

For a bridge deck with vertical (heave) frequency $f_h$ and torsional frequency $f_\alpha$, the critical flutter speed is estimated using the Selberg formula (for a flat plate):

$$
U_f = 0.44 \, f_\alpha B \sqrt{\frac{r_\alpha}{\mu}}
\sqrt{1 - \left(\frac{f_h}{f_\alpha}\right)^2}
$$

where:

- $B$ = deck width
- $r_\alpha$ = radius of gyration / half-chord
- $\mu = m / (\rho B^2)$ = mass ratio

### Flutter Derivatives

For real bridge deck sections, the aerodynamic forces are expressed using experimentally determined **flutter derivatives** $H_i^*$ and $A_i^*$ ($i = 1 \ldots 4$):

$$
L_h = \frac{1}{2}\rho U^2 B
\left[K H_1^* \frac{\dot{h}}{U} + K H_2^* \frac{B\dot{\alpha}}{U} + K^2 H_3^* \alpha +
K^2 H_4^* \frac{h}{B} \right]
$$

These derivatives are obtained from wind tunnel section model tests.

### Design Approach

- Flutter speed must exceed the design wind speed by a suitable margin (typically $U_f / U_{design} > 1.2$)
- Frequency separation between bending and torsion modes improves flutter resistance
- Aerodynamic shaping (open girders, fairings, slots) increases $U_f$

## Buffeting

### Mechanism

**Buffeting** is forced vibration driven by fluctuating velocities in the turbulent wind or wake. Unlike VIV and flutter, buffeting does not involve aerodynamic feedback — it is purely a forced response.

### Buffeting Response

The buffeting force per unit length on a structure is:

$$
F_b(t) = \frac{1}{2}\rho U^2 D
\left[2 C_D \frac{u'(t)}{U} + C_L' \frac{w'(t)}{U} \right]
$$

where $u'$ and $w'$ are the longitudinal and vertical turbulence components, and $C_L'$ is the lift coefficient derivative.

The response is computed spectrally:

$$
S_x(\omega) = |H(\omega)|^2 \, S_F(\omega)
$$

where $|H(\omega)|^2$ is the mechanical admittance of the structure.

### Wake Buffeting

Downstream structures in the wake of an upstream body experience amplified turbulence. This is significant for:

- Tandem chimney stacks
- Transmission line bundles
- Closely spaced bridge towers

## Suppression Methods

### Helical Strakes

Helical strakes (typically three fins at 120° spacing, height $\approx 0.1D$, pitch $\approx 5D$) disrupt the spanwise coherence of vortex shedding. They are the most widely used VIV suppression device for chimneys and marine risers.

**Effect:** Reduce VIV amplitude by 80–90%, but increase drag by 20–30%.

### Fairings (Shrouds)

Streamlined fairings rotate freely to align with the flow, reducing the effective bluffness and eliminating coherent shedding.

**Effect:** Near-complete VIV suppression with minimal drag penalty.

### Tuned Mass Dampers (TMD)

A secondary mass-spring-dashpot system is tuned to the target frequency:

$$
f_{TMD} = \frac{f_n}{1 + \mu_m}, \quad
\zeta_{TMD,opt} = \sqrt{\frac{3\mu_m}{8(1+\mu_m)^3}}
$$

where $\mu_m = m_{TMD}/m_s$ is the mass ratio (typically 1–5%).

### Splitter Plates

A flat plate attached to the downstream side of the cylinder prevents vortex interaction and suppresses shedding.

### Active Control

Feedback-controlled actuators (e.g., blowing/suction, oscillating surfaces) can suppress vibrations in real time but are complex and expensive.

## Worked Example 1: VIV of a Steel Chimney

**Given:**

- Chimney: $D = 3$ m, height $H = 60$ m, $f_n = 0.50$ Hz
- Mass per unit length $m = 600$ kg/m, damping ratio $\zeta = 0.01$
- Wind $U = 15$ m/s, air $\rho = 1.225$ kg/m³, $St = 0.20$

**Find:** Whether lock-in occurs and estimate the response amplitude.

**Solution:**

Shedding frequency:

$$
f_s = \frac{St \, U}{D} = \frac{0.20 \times 15}{3} = 1.0 \text{ Hz}
$$

Since $f_s = 1.0$ Hz $\neq f_n = 0.5$ Hz, lock-in does **not** occur at $U = 15$ m/s.

Critical velocity for lock-in:

$$
U_{cr} = \frac{f_n D}{St} = \frac{0.5 \times 3}{0.20} = 7.5 \text{ m/s}
$$

At $U = 7.5$ m/s, check amplitude. Scruton number:

$$
Sc = \frac{2 m (2\pi\zeta)}{\rho D^2} = \frac{2 \times 600 \times 0.0628}{1.225 \times 9} = 6.85
$$

Estimated amplitude:

$$
\frac{A}{D} \approx
\frac{1}{1 + 0.43 \times 2\pi \times 0.04 \times 6.85} = \frac{1}{1 + 0.74} \approx 0.57
$$

$$
A \approx 0.57 \times 3 = 1.7 \text{ m}
$$

This is a significant amplitude — **helical strakes are recommended**.

## Worked Example 2: Galloping of an Ice-Coated Cable

**Given:**

- Power line cable: $D = 0.05$ m, $f_n = 1.0$ Hz, $\zeta = 0.005$
- Mass per unit length $m = 2.5$ kg/m
- Ice accretion creates $dC_L/d\alpha \approx -3.0$, $C_D = 1.2$
- Air $\rho = 1.225$ kg/m³

**Find:** Critical wind speed for galloping onset.

**Solution:**

Den Hartog parameter:

$$
\left| \frac{dC_L}{d\alpha} + C_D\right| = | - 3.0 + 1.2| = 1.8
$$

Since the quantity is negative, the Den Hartog criterion is satisfied — galloping is possible.

$$
U_{cr} = \frac{4 m \omega_n \zeta}{\rho D \times 1.8} = \frac{4 \times 2.5 \times 2\pi \times 0.005}{1.225 \times 0.05 \times 1.8}
$$

$$
U_{cr} = \frac{0.314}{0.110} = 2.85 \text{ m/s}
$$

Galloping can begin at very low wind speeds — **ice removal or aerodynamic treatment** is essential.

## Applications

### Chimneys and Stacks

- VIV is the dominant concern; helical strakes are standard for steel chimneys
- Scruton number criterion ($Sc > 10$) is used as a design target
- Grouped stacks require interference assessment

### Cables and Conductors

- Galloping of ice-coated power lines causes flashover and conductor fatigue
- Rain-wind-induced vibration of bridge stay cables requires dampers or surface treatment
- Aeolian vibration (high-frequency, low-amplitude VIV) causes strand fatigue at clamps

### Bridges

- Flutter governs the design wind speed of long-span suspension bridges
- Vortex shedding from the deck affects serviceability
- Buffeting determines fatigue loads under normal wind conditions

### Heat Exchangers

- Tube bundles in cross-flow are susceptible to fluid-elastic instability
- Critical velocity depends on tube pitch, mass, and damping
- Baffle spacing and tube support are designed to avoid instability

### Offshore Risers and Pipelines

- Deep-water risers experience VIV from ocean currents over long spans
- Strakes and fairings are standard suppression measures
- Fatigue from VIV is often the life-limiting design criterion

## Design Considerations

### Damping

- Increasing structural damping is the most effective general mitigation
- Damping ratios: welded steel $\zeta \approx 0.002$, bolted connections $\zeta \approx 0.005$, concrete $\zeta \approx 0.01$

### Frequency Avoidance

- Design natural frequencies to avoid shedding frequencies in the operating wind/current speed range
- Use a ±20% avoidance band around critical reduced velocities

### Fatigue Assessment

- VIV-induced cyclic stress must be checked against fatigue life
- Use Palmgren–Miner cumulative damage rule with wind/current speed probability distributions
- A fatigue damage fraction $D < 1.0$ is required; typical safety factor gives $D < 0.33$

Flow-induced vibrations represent a rich intersection of fluid mechanics, structural dynamics, and aeroelasticity. Proper identification and mitigation of FIV mechanisms is essential for the safe and reliable performance of slender structures in wind, water, and process flows.

## Exercises

**Exercise 1.** A taut cable of diameter $D = 0.03$ m has natural frequency $f_n = 12$ Hz. Taking $St = 0.2$, find the wind speed at which the Strouhal shedding frequency matches $f_n$, and the wind-speed range corresponding to the lock-in band $4 \lesssim U_r \lesssim 8$.

<details>
<summary>Answer</summary>

$f_s = f_n$ when $U = f_n D/St = 12 \times 0.03/0.2 = 1.8$ m/s, which corresponds to $U_r = 1/St = 5$.

From $U = U_r f_n D$ with $f_n D = 0.36$ m/s, the lock-in band is $1.44 \lesssim U \lesssim 2.88$ m/s. These low wind speeds occur very often, which is why aeolian vibration of cables is a common fatigue problem.

</details>

**Exercise 2.** A steel riser has $D = 0.3$ m, mass per unit length $m = 150$ kg/m (including contents) and damping ratio $\zeta = 0.01$. Compute the Scruton number in seawater ($\rho = 1025$ kg/m³) and in air ($\rho = 1.225$ kg/m³). What do the values imply for VIV?

<details>
<summary>Answer</summary>

$\delta \approx 2\pi\zeta = 0.0628$, so $2m\delta = 18.85$ kg/m.

```math
Sc_{water} = \frac{18.85}{1025 \times 0.09} = 0.20, \quad
Sc_{air} = \frac{18.85}{1.225 \times 0.09} = 171
```

Because water is about 840 times denser than air, the same structure has a very low mass-damping parameter in water. Large VIV amplitudes ($A/D$ of order 1) are therefore possible underwater, while in air the amplitudes would be negligible. Adding structural damping is ineffective in water; strakes or fairings are used instead.

</details>

**Exercise 3.** (a) In quasi-steady theory, a body moving transversely with small velocity $\dot{y}$ in a steady flow $U$ has transverse force coefficient $C_y \approx -\left(\frac{dC_L}{d\alpha} + C_D\right)\frac{\dot{y}}{U}$. Derive the Den Hartog criterion and the critical galloping speed. (b) Wind-tunnel data for a square bar give $\frac{dC_L}{d\alpha} + C_D = -2.7$. With $D = 0.5$ m, $m = 100$ kg/m, $f_n = 2$ Hz and $\zeta = 0.005$ in air, find $U_{cr}$.

<details>
<summary>Answer</summary>

(a) The transverse force per unit length is $F_y = \frac{1}{2}\rho U^2 D\,C_y = -\frac{1}{2}\rho U D\left(\frac{dC_L}{d\alpha} + C_D\right)\dot{y}$. Moving it to the left-hand side of $m\ddot{y} + 2m\omega_n\zeta\dot{y} + ky = F_y$ gives a total damping coefficient

```math
c_{tot} = 2m\omega_n\zeta + \frac{1}{2}\rho U D\left(\frac{dC_L}{d\alpha} + C_D\right)
```

The aerodynamic term can only make $c_{tot}$ negative if $\frac{dC_L}{d\alpha} + C_D < 0$ (the Den Hartog criterion). Instability then starts when $c_{tot} = 0$:

```math
U_{cr} = \frac{4m\omega_n\zeta}{\rho D\left|\frac{dC_L}{d\alpha} + C_D\right|}
```

(b) $\omega_n = 12.57$ rad/s:

```math
U_{cr} = \frac{4 \times 100 \times 12.57 \times 0.005}{1.225 \times 0.5 \times 2.7} = \frac{25.1}{1.654} = 15.2 \text{ m/s}
```

</details>

**Exercise 4.** A steel chimney has modal mass 20 000 kg and $f_n = 0.5$ Hz. Design a tuned mass damper with mass ratio $\mu_m = 0.02$ using the tuning formulas in this note: give the TMD mass, frequency, spring stiffness, optimum damping ratio and damping coefficient.

<details>
<summary>Answer</summary>

$m_{TMD} = 0.02 \times 20\,000 = 400$ kg and $f_{TMD} = 0.5/1.02 = 0.490$ Hz, so $\omega_{TMD} = 3.08$ rad/s.

```math
k_{TMD} = m_{TMD}\omega_{TMD}^2 = 400 \times 3.08^2 = 3.79 \text{ kN/m}
```

```math
\zeta_{opt} = \sqrt{\frac{3 \times 0.02}{8(1.02)^3}} = 0.084, \quad
c_{TMD} = 2m_{TMD}\omega_{TMD}\zeta_{opt} = 207 \text{ N·s/m}
```

</details>

**Exercise 5.** VIV of a riser produces a stress range of 60 MPa at 0.5 Hz for 50 hours per year. The S-N curve is $N = 10^{12}/\Delta\sigma^3$ ($\Delta\sigma$ in MPa). Estimate the annual Palmgren-Miner damage and the fatigue life for allowable damage fractions of 0.33 and 1.0.

<details>
<summary>Answer</summary>

Cycles per year: $n = 0.5 \times 3600 \times 50 = 90\,000$. Cycles to failure: $N = 10^{12}/60^3 = 4.63 \times 10^6$.

Annual damage: $D = n/N = 0.0194$. The life is $0.33/0.0194 = 17$ years with the safety factor, or $1/0.0194 = 51$ years to $D = 1$. The cubic S-N slope means a 20% reduction in stress range (for example from strakes) would extend the life by a factor of about $1/0.8^3 \approx 2$.

</details>

## References

- R. D. Blevins, *Flow-Induced Vibration*, 2nd ed., Van Nostrand Reinhold, 1990.
- E. Simiu, R. H. Scanlan, *Wind Effects on Structures: Fundamentals and Applications to Design*, 3rd ed., Wiley, 1996.
- M. P. Païdoussis, S. J. Price, E. de Langre, *Fluid-Structure Interactions: Cross-Flow-Induced Instabilities*, Cambridge University Press, 2011.
- C. H. K. Williamson, R. Govardhan, "Vortex-induced vibrations", *Annual Review of Fluid Mechanics* 36, 413–455, 2004.
- J. P. Den Hartog, *Mechanical Vibrations*, 4th ed., McGraw-Hill, 1956.
