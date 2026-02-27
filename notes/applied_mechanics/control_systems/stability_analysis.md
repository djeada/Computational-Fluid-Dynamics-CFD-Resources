# Stability Analysis

Stability is the most fundamental requirement of any control system. An unstable system produces unbounded outputs and is unusable — or dangerous — regardless of how well other performance criteria are met. This note covers the major analytical tools for assessing closed-loop stability.

## BIBO Stability

A system is **Bounded-Input Bounded-Output (BIBO) stable** if every bounded input produces a bounded output:

$$|u(t)| \leq M_u < \infty \quad \forall\, t \geq 0 \implies |y(t)| \leq M_y < \infty \quad \forall\, t \geq 0$$

For an LTI system with impulse response $g(t)$, BIBO stability requires:

$$\int_0^{\infty} |g(t)|\, dt < \infty$$

### Internal (Lyapunov) Stability

A stronger condition: the system is **internally stable** if all state variables remain bounded for any bounded initial condition and input. Internal stability implies BIBO stability, but not vice versa (hidden unstable modes may exist due to pole-zero cancellation).

## Pole Locations and Stability

For an LTI system with transfer function $G(s)$, BIBO stability depends entirely on the poles (roots of the denominator):

- **Stable**: All poles in the open left-half plane ($\text{Re}(p_i) < 0$)
- **Marginally stable**: Poles on the imaginary axis (simple, non-repeated)
- **Unstable**: Any pole in the right-half plane or repeated poles on the imaginary axis

For a pole at $s = \sigma + j\omega$:
- $\sigma < 0$: Decaying response component $\propto e^{\sigma t}$
- $\sigma = 0$: Sustained oscillation or constant
- $\sigma > 0$: Growing response — **unstable**

## Routh-Hurwitz Criterion

The Routh-Hurwitz criterion determines stability from the characteristic polynomial coefficients **without computing the roots**. This is especially useful for polynomials with symbolic parameters.

### Characteristic Polynomial

$$P(s) = a_n s^n + a_{n-1} s^{n-1} + \cdots + a_1 s + a_0$$

**Necessary condition**: All coefficients $a_i$ must be positive (for $a_n > 0$). If any coefficient is zero or negative, the system is unstable.

### Routh Array Construction

$$\begin{array}{c|cccc}
s^n     & a_n     & a_{n-2} & a_{n-4} & \cdots \\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} & \cdots \\
s^{n-2} & b_1     & b_2     & b_3     & \cdots \\
s^{n-3} & c_1     & c_2     & c_3     & \cdots \\
\vdots  & \vdots  & \vdots  &         &
\end{array}$$

where:

$$b_1 = \frac{a_{n-1} a_{n-2} - a_n a_{n-3}}{a_{n-1}}, \quad b_2 = \frac{a_{n-1} a_{n-4} - a_n a_{n-5}}{a_{n-1}}$$

$$c_1 = \frac{b_1 a_{n-3} - a_{n-1} b_2}{b_1}, \quad c_2 = \frac{b_1 a_{n-5} - a_{n-1} b_3}{b_1}$$

**Stability rule**: The number of sign changes in the first column of the Routh array equals the number of roots in the right-half plane.

### Special Cases

1. **Zero in the first column**: Replace 0 with a small positive $\epsilon$, complete the array, and take the limit as $\epsilon \to 0^+$.
2. **Entire row of zeros**: Indicates symmetric root pairs (e.g., $\pm j\omega$ or $\pm\sigma$). Form the **auxiliary polynomial** from the row above, differentiate it, and use the coefficients to replace the zero row.

## Root Locus Method

The root locus is a graphical technique that shows how the closed-loop poles migrate in the $s$-plane as a gain parameter $K$ varies from 0 to $\infty$.

### Setup

For the closed-loop characteristic equation:

$$1 + K\frac{N(s)}{D(s)} = 0 \implies KG(s)H(s) = -1$$

The root locus is the set of points satisfying:

- **Magnitude condition**: $|KG(s)H(s)| = 1$
- **Angle condition**: $\angle G(s)H(s) = (2q+1) \times 180°, \quad q = 0, \pm 1, \pm 2, \ldots$

### Rules for Construction

1. **Number of branches**: Equals the number of open-loop poles $n$
2. **Start and end points**: Branches start at open-loop poles ($K=0$) and end at open-loop zeros or infinity ($K \to \infty$)
3. **Real-axis segments**: A point on the real axis is on the root locus if the number of real poles and zeros to its right is odd
4. **Asymptotes**: $n - m$ branches go to infinity along asymptotes with angles $\phi_a = \frac{(2q+1) \times 180°}{n - m}$ and centroid $\sigma_a = \frac{\sum p_i - \sum z_j}{n - m}$
5. **Breakaway/break-in points**: Found by solving $\frac{dK}{ds} = 0$ where $K = -\frac{D(s)}{N(s)}$
6. **Imaginary axis crossings**: Use Routh-Hurwitz or substitute $s = j\omega$
7. **Departure/arrival angles**: $\theta_{dep} = 180° - \sum \angle(\text{to other poles}) + \sum \angle(\text{to zeros})$

### Interpretation

- If all branches remain in the left-half plane for a range of $K$, the system is stable in that range
- Branches crossing the imaginary axis indicate the **critical gain** where stability is lost
- Desired pole locations guide the choice of $K$ and additional compensation

## Nyquist Stability Criterion

The Nyquist criterion uses the frequency response $G(j\omega)H(j\omega)$ plotted in the complex plane to determine closed-loop stability.

### Nyquist Contour and Mapping

The Nyquist contour $\Gamma$ encloses the entire right-half $s$-plane. The plot of $G(s)H(s)$ evaluated along $\Gamma$ produces the Nyquist diagram.

### Criterion Statement

$$Z = N + P$$

where:
- $Z$ = number of closed-loop RHP poles (unstable poles)
- $P$ = number of open-loop RHP poles (known)
- $N$ = number of **clockwise** encirclements of the critical point $-1 + j0$

**For stability**: $Z = 0$, so $N = -P$ (i.e., $P$ counterclockwise encirclements of $-1$).

**If the open-loop system is stable** ($P = 0$): The Nyquist plot must not encircle the $-1$ point at all.

## Gain Margin and Phase Margin

These are practical measures of **relative stability** — how close a stable system is to becoming unstable.

### Gain Margin (GM)

The factor by which the open-loop gain can be increased before instability:

$$GM = \frac{1}{|G(j\omega_{pc})H(j\omega_{pc})|}$$

where $\omega_{pc}$ is the **phase crossover frequency** at which $\angle G(j\omega)H(j\omega) = -180°$.

In decibels: $GM_{dB} = -20\log_{10}|G(j\omega_{pc})H(j\omega_{pc})|$

### Phase Margin (PM)

The additional phase lag needed to reach instability:

$$PM = 180° + \angle G(j\omega_{gc})H(j\omega_{gc})$$

where $\omega_{gc}$ is the **gain crossover frequency** at which $|G(j\omega)H(j\omega)| = 1$ (0 dB).

### Design Guidelines

| Specification | Minimum Recommended |
|---|---|
| Gain margin | $> 6$ dB (factor of 2) |
| Phase margin | $> 30°$ (typically $45°$–$60°$) |

A system with both adequate GM and PM is **robustly stable** against modeling errors and parameter variations.

## Relative Stability

Beyond simple stable/unstable classification, relative stability quantifies **how stable** a system is:

- **Damping ratio** $\zeta$: Larger $\zeta$ means less oscillatory response
- **Distance of dominant poles from imaginary axis**: Larger $|\sigma|$ gives faster decay
- **Gain and phase margins**: Larger margins mean more tolerance to uncertainty
- **Sensitivity peak** $M_s = \max_\omega |S(j\omega)|$: Smaller $M_s$ indicates better robustness (typically $M_s < 2$)

## Worked Examples

### Example 1: Routh-Hurwitz Criterion

**Given**: Unity feedback system with open-loop transfer function $G(s) = \frac{K(s+1)}{s^3 + 3s^2 + 2s}$.

**Find**: Range of $K$ for closed-loop stability.

**Solution**:

Characteristic equation: $s^3 + 3s^2 + 2s + K(s+1) = 0$

$$s^3 + 3s^2 + (2+K)s + K = 0$$

Routh array:

$$\begin{array}{c|cc}
s^3 & 1 & 2+K \\
s^2 & 3 & K \\
s^1 & \frac{3(2+K) - K}{3} & 0 \\
s^0 & K &
\end{array}$$

The $s^1$ entry simplifies to $\frac{6 + 2K}{3}$.

For stability, all first-column entries must be positive:
- $s^1$ row: $6 + 2K > 0 \implies K > -3$
- $s^0$ row: $K > 0$

Therefore the system is stable for $K > 0$.

### Example 2: Root Locus Imaginary-Axis Crossing

**Given**: Open-loop transfer function $G(s)H(s) = \frac{K}{s(s+1)(s+4)}$.

**Find**: Value of $K$ at which the root locus crosses the imaginary axis.

**Solution**:

Characteristic equation: $s^3 + 5s^2 + 4s + K = 0$.

Substitute $s = j\omega$:

$$(j\omega)^3 + 5(j\omega)^2 + 4(j\omega) + K = 0$$

$$(-j\omega^3 - 5\omega^2 + 4j\omega + K) = 0$$

Real part: $-5\omega^2 + K = 0 \implies K = 5\omega^2$

Imaginary part: $-\omega^3 + 4\omega = 0 \implies \omega(\omega^2 - 4) = 0 \implies \omega = 2$ rad/s

Therefore $K = 5(4) = 20$. The root locus crosses the imaginary axis at $s = \pm 2j$ when $K = 20$.

### Example 3: Gain and Phase Margin from Bode Plot

**Given**: Open-loop transfer function $G(s) = \frac{10}{s(s+1)(0.1s+1)}$.

**Find**: Gain margin and phase margin.

**Solution**:

**Phase crossover frequency** ($\angle G = -180°$):

$$\angle G(j\omega) = -90° - \arctan(\omega) - \arctan(0.1\omega) = -180°$$

$$\arctan(\omega) + \arctan(0.1\omega) = 90°$$

Using the identity for $\arctan a + \arctan b = 90°$ when $ab = 1$: $0.1\omega^2 = 1 \implies \omega_{pc} = \sqrt{10} \approx 3.16$ rad/s.

$$|G(j\omega_{pc})| = \frac{10}{3.16 \cdot \sqrt{1+10} \cdot \sqrt{1+1}} = \frac{10}{3.16 \times 3.32 \times 1.41} \approx 0.676$$

$$GM = \frac{1}{0.676} \approx 1.48 \implies GM_{dB} \approx 3.4\;\text{dB}$$

This gain margin is **below the recommended 6 dB**, indicating the system has poor relative stability and would benefit from compensation.

## Applications

- **Aerospace**: Ensuring flight control stability across varying altitude and speed conditions
- **Power systems**: Generator rotor angle stability and voltage stability assessment
- **Chemical process control**: Stability of reactor temperature and concentration loops
- **Structural engineering**: Flutter analysis of bridges and aircraft wings
- **Robotics**: Joint-level stability under varying payload and configuration

## Practical Tips

- The Routh-Hurwitz criterion is best for finding **stability boundaries** in terms of symbolic parameters (e.g., gain $K$)
- Root locus is ideal for understanding **how** stability changes with a single parameter
- Nyquist and Bode methods work directly with **experimental frequency response data** — no analytical model needed
- Always check both gain margin **and** phase margin; either alone can be misleading
- For digital control systems, stability analysis must account for sampling effects — use the $z$-plane or bilinear (Tustin) transformation
