# Vibrations and Oscillations

Vibrations are repetitive motions about an equilibrium position and are central to mechanical and structural engineering. Understanding vibratory behavior is essential for designing systems that avoid resonance, minimize unwanted oscillations, and exploit beneficial vibration characteristics.

## Free Vibration of Undamped Systems

### Equation of Motion

For a mass $m$ attached to a spring of stiffness $k$ with no damping or external forcing:

$$m\ddot{x} + kx = 0$$

Dividing by $m$:

$$\ddot{x} + \omega_n^2 x = 0$$

where the **natural frequency** is:

$$\omega_n = \sqrt{\frac{k}{m}} \quad \text{(rad/s)}$$

### General Solution

$$x(t) = A\sin(\omega_n t + \phi)$$

or equivalently:

$$x(t) = C_1\sin(\omega_n t) + C_2\cos(\omega_n t)$$

where $A$ is the amplitude and $\phi$ is the phase angle, determined by initial conditions.

With $x(0) = x_0$ and $\dot{x}(0) = v_0$:

$$x(t) = \frac{v_0}{\omega_n}\sin(\omega_n t) + x_0\cos(\omega_n t)$$

$$A = \sqrt{x_0^2 + \left(\frac{v_0}{\omega_n}\right)^2}$$

### Key Parameters

- **Natural frequency:** $f_n = \frac{\omega_n}{2\pi}$ (Hz)
- **Natural period:** $\tau_n = \frac{1}{f_n} = \frac{2\pi}{\omega_n}$ (s)
- **Simple pendulum natural frequency:** $\omega_n = \sqrt{\frac{g}{L}}$
- **Compound pendulum natural frequency:** $\omega_n = \sqrt{\frac{mgd}{I_O}}$, where $d$ is the distance from pivot to mass center

## Free Vibration of Damped Systems

### Equation of Motion

Adding viscous damping with coefficient $c$:

$$m\ddot{x} + c\dot{x} + kx = 0$$

### Critical Damping and Damping Ratio

**Critical damping coefficient:**
$$c_c = 2m\omega_n = 2\sqrt{km}$$

**Damping ratio:**
$$\zeta = \frac{c}{c_c} = \frac{c}{2m\omega_n}$$

The character roots of the characteristic equation are:

$$s_{1,2} = (-\zeta \pm \sqrt{\zeta^2 - 1})\omega_n$$

### Underdamped System ($\zeta < 1$)

The most common case in engineering. The system oscillates with decaying amplitude:

$$x(t) = Ae^{-\zeta\omega_n t}\sin(\omega_d t + \phi)$$

where the **damped natural frequency** is:

$$\omega_d = \omega_n\sqrt{1 - \zeta^2}$$

The amplitude decays exponentially with time constant $\tau = \frac{1}{\zeta\omega_n}$.

**Logarithmic decrement** (ratio of successive peaks):
$$\delta = \ln\frac{x_n}{x_{n+1}} = \frac{2\pi\zeta}{\sqrt{1 - \zeta^2}}$$

For small damping ($\zeta \ll 1$): $\delta \approx 2\pi\zeta$

### Critically Damped System ($\zeta = 1$)

The system returns to equilibrium as quickly as possible without oscillating:

$$x(t) = (C_1 + C_2 t)e^{-\omega_n t}$$

### Overdamped System ($\zeta > 1$)

The system returns to equilibrium without oscillating, but more slowly than critical damping:

$$x(t) = C_1 e^{s_1 t} + C_2 e^{s_2 t}$$

where $s_1$ and $s_2$ are both real and negative.

## Forced Vibration and Resonance

### Harmonically Excited System

For a damped system subjected to a harmonic force $F_0\sin(\omega t)$:

$$m\ddot{x} + c\dot{x} + kx = F_0\sin(\omega t)$$

The **steady-state response** is:

$$x_p(t) = X\sin(\omega t - \phi)$$

where the **amplitude** is:

$$X = \frac{F_0/k}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}$$

and the **phase lag** is:

$$\phi = \arctan\frac{2\zeta r}{1 - r^2}$$

Here $r = \omega/\omega_n$ is the **frequency ratio**.

### Magnification Factor

The **dynamic magnification factor** relates the dynamic amplitude to the static deflection $\delta_{st} = F_0/k$:

$$M = \frac{X}{\delta_{st}} = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}$$

Key observations:
- At $r = 0$: $M = 1$ (static case)
- At $r = 1$ (resonance): $M = \frac{1}{2\zeta}$ — amplitude is controlled only by damping
- At $r \gg 1$: $M \to 0$ — high-frequency excitation is attenuated
- Peak response occurs at $r = \sqrt{1 - 2\zeta^2}$ for $\zeta < 1/\sqrt{2}$

### Resonance

**Resonance** occurs when $\omega \approx \omega_n$ ($r \approx 1$). At resonance:
- Amplitudes become very large if damping is small
- Phase lag is approximately 90°
- Energy input from the excitation perfectly matches the system's natural oscillation

Resonance must be avoided in structural and mechanical design to prevent fatigue failure or catastrophic collapse.

## Vibration Isolation and Transmissibility

When a vibrating machine is mounted on springs and dampers, the **force transmissibility** is:

$$T_f = \frac{F_{transmitted}}{F_0} = \frac{\sqrt{1 + (2\zeta r)^2}}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}$$

- For $r < \sqrt{2}$: $T_f > 1$ — the mount amplifies the force
- For $r > \sqrt{2}$: $T_f < 1$ — isolation is achieved
- Effective isolation requires $\omega \gg \omega_n$ (soft mount, heavy base)

For **base excitation** $y(t) = Y\sin(\omega t)$, the absolute displacement transmissibility has the same expression as $T_f$.

## Two-Degree-of-Freedom Systems

For systems with two masses and multiple springs, the equations of motion form a coupled system:

$$[M]\ddot{\mathbf{x}} + [K]\mathbf{x} = \mathbf{0}$$

where $[M]$ and $[K]$ are the mass and stiffness matrices. The system has **two natural frequencies** $\omega_1$ and $\omega_2$, each with an associated **mode shape**. A **vibration absorber** uses a tuned secondary mass-spring system ($\omega_2 = \omega_{excitation}$) to suppress vibration at a specific frequency.

## Worked Examples

### Example 1: Undamped Free Vibration (Spring-Mass)

A 4 kg block is attached to a spring ($k = 900$ N/m) and displaced 50 mm from equilibrium before being released from rest.

**Given:**
- $m = 4$ kg, $k = 900$ N/m
- $x_0 = 0.05$ m, $v_0 = 0$

**Find:** Natural frequency, period, and maximum velocity.

**Solution:**

$$\omega_n = \sqrt{\frac{k}{m}} = \sqrt{\frac{900}{4}} = 15 \text{ rad/s}$$

$$f_n = \frac{15}{2\pi} = 2.39 \text{ Hz}, \quad \tau_n = \frac{1}{2.39} = 0.419 \text{ s}$$

$$x(t) = 0.05\cos(15t) \text{ m}$$

$$\dot{x}(t) = -0.05(15)\sin(15t) = -0.75\sin(15t) \text{ m/s}$$

$$v_{max} = A\omega_n = 0.05(15) = 0.75 \text{ m/s}$$

### Example 2: Damped Free Vibration

A 5 kg mass on a spring ($k = 500$ N/m) has a damping coefficient $c = 30$ N·s/m.

**Given:** $m = 5$ kg, $k = 500$ N/m, $c = 30$ N·s/m, $x_0 = 0.04$ m

**Find:** Damping ratio, damped frequency, and amplitude after 5 cycles.

**Solution:**

$$\omega_n = \sqrt{500/5} = 10 \text{ rad/s}, \quad c_c = 2(5)(10) = 100 \text{ N·s/m}, \quad \zeta = 30/100 = 0.3$$

Underdamped ($\zeta < 1$): $\omega_d = 10\sqrt{1 - 0.09} = 9.54$ rad/s

**Logarithmic decrement:** $\delta = \frac{2\pi(0.3)}{\sqrt{1 - 0.09}} = 1.976$

**After 5 cycles:** $x_5 = x_0 / e^{5\delta} = 0.04 / e^{9.88} \approx 0.002$ mm — nearly fully damped.

### Example 3: Simple Pendulum Period

A pendulum of length $L = 1.5$ m.

**Solution:**

$$\omega_n = \sqrt{g/L} = \sqrt{9.81/1.5} = 2.557 \text{ rad/s}$$

$$\tau_n = \frac{2\pi}{\omega_n} = \frac{2\pi}{2.557} = 2.457 \text{ s}$$

### Example 4: Vibration Isolation

A 200 kg machine operates at 1200 RPM and produces a force amplitude of 500 N. Design a spring mount for 85% force isolation ($T_f = 0.15$). Neglect damping.

**Given:**
- $m = 200$ kg, operating speed $= 1200$ RPM $= 125.7$ rad/s
- $F_0 = 500$ N, $T_f = 0.15$, $\zeta \approx 0$

**Find:** Required spring stiffness.

**Solution:**

For $\zeta = 0$ and $r > \sqrt{2}$:
$$T_f = \frac{1}{r^2 - 1}$$

$$0.15 = \frac{1}{r^2 - 1} \implies r^2 - 1 = \frac{1}{0.15} = 6.667 \implies r^2 = 7.667$$

$$r = \frac{\omega}{\omega_n} = 2.769 \implies \omega_n = \frac{125.7}{2.769} = 45.4 \text{ rad/s}$$

$$k = m\omega_n^2 = 200(45.4)^2 = 412\,232 \text{ N/m} \approx 412 \text{ kN/m}$$

**Transmitted force:**
$$F_{trans} = T_f \cdot F_0 = 0.15(500) = 75 \text{ N}$$

## Applications

### Structural and Civil Engineering
- Earthquake-resistant building design using base isolation
- Wind-induced vibration of bridges and tuned mass dampers (e.g., Taipei 101)

### Mechanical and Automotive Engineering
- Engine mount design and rotating machinery balancing
- Suspension system tuning for ride comfort
- Machine tool chatter avoidance

### Aerospace Engineering
- Flutter analysis of aircraft wings and control surfaces
- Launch vehicle vibration during ascent and satellite component testing

## Practical Problem-Solving Tips

### 1. Determine the Natural Frequency First
- This is the most important parameter in any vibration problem
- For simple systems, use $\omega_n = \sqrt{k/m}$ or the energy method
- For complex systems, compute the stiffness and mass matrices

### 2. Identify the Damping Level
- Most engineering systems are underdamped ($\zeta < 1$)
- Measure damping via logarithmic decrement from free vibration tests
- Typical values: structural steel $\zeta \approx 0.01$–$0.05$, rubber mounts $\zeta \approx 0.05$–$0.15$

### 3. Avoid Resonance in Design
- Ensure operating frequencies are well separated from natural frequencies
- Rule of thumb: keep $r < 0.5$ or $r > 1.5$ to avoid resonance zone
- Add damping if operating near resonance is unavoidable

### 4. Design Isolation Systems Properly
- Isolation begins at $r = \sqrt{2}$; aim for $r > 2.5$ for effective isolation
- Soft mounts lower $\omega_n$ and increase $r$, but allow larger static deflection
- For complex systems, use Rayleigh's energy method to estimate natural frequency

Vibration analysis is a cornerstone of dynamic system design, ensuring that structures and machines operate safely, efficiently, and comfortably throughout their service life.
