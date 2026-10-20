# Frequency Response

The frequency response describes how a linear system amplifies and delays sinusoids of each frequency. It is the basis of the most widely used design tools in classical control: Bode plots, which can be sketched by hand from straight-line asymptotes; the Nyquist criterion, which decides closed-loop stability from the open-loop response alone, even with a time delay or with nothing but measured data; and the gain and phase margins, which say how far a stable loop is from instability. This note develops these tools on a pump-fed tank level loop, with and without a transport delay in the supply pipe, and relates the margins to the damping of the closed-loop step response.

## Problem Statement

Given the loop transfer function of a feedback system, $L(s) = C(s)G(s)H(s)$, either as a rational function multiplied by a delay $e^{-sT}$ or as measured values of $L(j\omega)$ from a sine-sweep test, determine:

1. whether the closed loop $1 + L(s) = 0$ is stable, counting any closed-loop right-half-plane poles;
2. the gain margin, phase margin and delay margin, and the peak sensitivity;
3. the closed-loop bandwidth and the damping to expect in the step response;
4. how to modify $C(s)$ so that $L(j\omega)$ is large at low frequency, small at high frequency, and crosses unity with enough phase margin.

The loop is assumed linear and time-invariant; $L$ may contain poles on the imaginary axis (integrators) and a finite number of right-half-plane poles, whose number $P$ must be known.

## The Frequency Response

If a stable LTI system $G(s)$ is driven by $u(t) = \sin\omega t$, then once the transients have decayed its output is

$$
y_{ss}(t) = \lvert G(j\omega)\rvert\sin\left(\omega t + \angle G(j\omega)\right)
$$

The complex number $G(j\omega)$ is the frequency response: its magnitude is the amplitude ratio and its argument the phase shift. It follows from the partial-fraction expansion of $`Y(s) = G(s)\,\omega/(s^2 + \omega^2)`$: the terms from the poles of $G$ decay, and the two terms from $s = \pm j\omega$ combine into the sinusoid above. Because it can be measured by applying sinusoids to a running plant, the frequency response is available even when no model is.

## Bode Plots

A Bode plot draws $20\log_{10}\lvert G(j\omega)\rvert$ (in decibels) and $\angle G(j\omega)$ (in degrees) against $\log\omega$. Because $G$ is a product of factors, the logarithm of its magnitude and its phase are sums of the contributions of the factors, each of which has a simple straight-line approximation:

| Factor | Magnitude asymptotes | Phase |
| --- | --- | --- |
| Gain $K$ | Constant $20\log_{10}K$ | $0^\circ$ (for $K > 0$) |
| Integrator $1/s$ | $-20$ dB/decade, through 0 dB at $\omega = 1$ | $-90^\circ$ |
| Lag $1/(\tau s + 1)$ | 0 dB below the corner $1/\tau$, $-20$ dB/decade above it; actual curve 3 dB below the corner of the asymptotes | 0 to $-90^\circ$; $-45^\circ$ at $1/\tau$; straight line between $0.1/\tau$ and $10/\tau$, error at most $5.7^\circ$ |
| Lead $\tau s + 1$ | Mirror image of the lag: $+20$ dB/decade above $1/\tau$ | 0 to $+90^\circ$ |
| Second-order $\omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2)$ | 0 dB, then $-40$ dB/decade above $\omega_n$; resonant peak $M_r = 1/(2\zeta\sqrt{1 - \zeta^2})$ at $\omega_r = \omega_n\sqrt{1 - 2\zeta^2}$ for $\zeta < 0.707$ | 0 to $-180^\circ$, $-90^\circ$ at $\omega_n$, steeper for small $\zeta$ |
| Delay $e^{-sT}$ | 0 dB at all frequencies | $-\omega T$ (in radians), growing without bound |

A rational factor with all its poles and zeros in the left half-plane is minimum phase: for such a system the phase is fixed by the slope of the magnitude curve (Bode's gain–phase relation), roughly $-90^\circ$ per $-20$ dB/decade of slope sustained over a decade or more. A delay or a right-half-plane zero adds phase lag without changing the magnitude, and so cannot be seen in the magnitude plot.

### Example: Tank Level Loop

A tank of area $A = 1$ m² is filled by a pump whose flow responds to its voltage command $u$ with gain $k_q = 0.05$ m³/(s V) and time constant $\tau_p = 2$ s, and emptied by a positive-displacement pump at a fixed rate, so the level integrates the flow imbalance ([System Modeling](./system_modeling.md)). The level sensor has a lag $\tau_m = 0.5$ s, and a proportional controller sets $u = K_c(r - h_m)$ with $K_c = 10$ V/m. In a second configuration the water spends $T = 1$ s in the supply pipe between pump and tank. The loop transfer function is

$$
L(s) = \frac{K}{s(\tau_p s + 1)(\tau_m s + 1)}e^{-sT},
\qquad K = \frac{K_c k_q}{A} = 0.5 \text{ s}^{-1}
$$

The magnitude asymptote falls at $-20$ dB/decade from 34 dB at 0.01 rad/s to 0 dB at the first corner $1/\tau_p = 0.5$ rad/s, at $-40$ dB/decade to $-24$ dB at $1/\tau_m = 2$ rad/s, and at $-60$ dB/decade above. The phase starts at $-90^\circ$ and tends to $-270^\circ$ without delay; with delay it falls without bound.

![Bode magnitude and phase with asymptotes and margins, and Nyquist plot with the -1 point, for the tank level loop with and without a 1 s delay](../../../scripts/algorithms/control_bode_nyquist/control_bode_nyquist.png)

In panel (a) the magnitude curves of the two loops coincide, and the dotted asymptotes follow them to within 3 dB except near the corners. In panel (b) the delay pulls the phase down by $\omega T$, which at the gain crossover costs $22^\circ$ of phase margin and moves the phase crossover from 1.0 to 0.52 rad/s, where the magnitude is much larger, so the gain margin falls from 14.0 to 3.7 dB.

## The Nyquist Criterion

The Nyquist criterion follows from the argument principle: if a closed contour in the $s$-plane encircles $Z$ zeros and $P$ poles of a function $F(s)$ clockwise, then the image of the contour under $F$ encircles the origin $Z - P$ times clockwise. Taking $F(s) = 1 + L(s)$, whose zeros are the closed-loop poles and whose poles are the open-loop poles, and a contour that encloses the whole right half-plane, gives the criterion.

The Nyquist contour runs up the imaginary axis from $-j\infty$ to $+j\infty$ and closes along a semicircle of infinite radius through the right half-plane; poles of $L$ on the imaginary axis, such as an integrator, are bypassed on small semicircles into the right half-plane. Encircling the origin with $1 + L$ is the same as encircling $-1$ with $L$, so with $N$ the number of clockwise encirclements of $-1 + 0j$ by the image of the contour under $L$:

$$
Z = N + P
$$

where $Z$ is the number of closed-loop poles in the right half-plane and $P$ the number of open-loop poles there. The loop is stable if and only if $Z = 0$, that is $N = -P$: the plot must encircle $-1$ counterclockwise once for each unstable open-loop pole, and not at all if the open loop is stable.

In practice only the positive-frequency half $L(j\omega)$, $\omega$ from $0^+$ to $\infty$, is drawn; the negative-frequency half is its mirror image in the real axis, the infinite semicircle maps to the origin for a strictly proper $L$, and the small semicircle around an integrator maps to a large arc that swings clockwise through the right half-plane from the $\omega = 0^-$ end to the $\omega = 0^+$ end.

For the level loop, $P = 0$ (the integrator is on the axis and bypassed). In panel (c) both plots start far down near the negative imaginary axis; at low frequency their real part tends to $-K(\tau_p + \tau_m + T)$, which is $-1.25$ without delay and $-1.75$ with it. Both cross the negative real axis to the right of $-1$, at $-0.200$ and $-0.652$, so $N = 0$ and the loop is stable. The script counts the encirclements along the full contour numerically: $N = 0$ at the nominal gain, and $N = 2$, so two unstable closed-loop poles, when the gain is raised 10% beyond the gain margin.

A delay has no rational transfer function, so the Routh array and the root locus cannot treat it exactly; the Nyquist plot can, because it needs only $L(j\omega)$. The delay multiplies $L(j\omega)$ by $e^{-j\omega T}$, a pure rotation, which winds the high-frequency end of the plot into a spiral around the origin.

## Gain, Phase and Delay Margins

The point $-1$ corresponds to $\lvert L\rvert = 1$ and $\angle L = -180^\circ$ simultaneously. The margins measure how far the plot stays from it, along the two directions in which the plant is most often wrong: gain and phase.

The gain margin is the factor by which the loop gain can be multiplied before the plot reaches $-1$. It is read at the phase crossover frequency $\omega_{pc}$, where $\angle L(j\omega_{pc}) = -180^\circ$:

$$
GM = \frac{1}{\lvert L(j\omega_{pc})\rvert},
\qquad GM_{\mathrm{dB}} = -20\log_{10}\lvert L(j\omega_{pc})\rvert
$$

On the Nyquist plot, the crossing of the negative real axis is at $-1/GM$.

The phase margin is the additional phase lag that would bring the plot to $-1$. It is read at the gain crossover frequency $\omega_{gc}$, where $\lvert L(j\omega_{gc})\rvert = 1$:

$$
PM = 180^\circ + \angle L(j\omega_{gc})
$$

On the Nyquist plot, it is the angle between the negative real axis and the point where the plot crosses the unit circle. Because a delay $T$ adds a phase lag $\omega T$ without changing $\omega_{gc}$, the delay margin, the largest extra delay the loop tolerates, is

$$
T_{dm} = \frac{PM\ (\text{rad})}{\omega_{gc}}
$$

The distance from $-1$ to the nearest point of the plot is $1/M_s$, where $M_s = \max_\omega\lvert 1/(1 + L(j\omega))\rvert$ is the peak sensitivity. It is a single robustness measure that bounds both classical margins:

$$
GM \geq \frac{M_s}{M_s - 1},
\qquad PM \geq 2\arcsin \frac{1}{2M_s}
$$

Common targets are $GM \geq 2$ (6 dB), $PM$ between $45^\circ$ and $60^\circ$, and $M_s$ between 1.4 and 2. For the level loop the script finds:

| Quantity | No delay | Delay $T = 1$ s |
| --- | --- | --- |
| Gain crossover $\omega_{gc}$ (rad/s) | 0.388 | 0.388 |
| Phase margin | $41.2^\circ$ | $19.0^\circ$ |
| Phase crossover $\omega_{pc}$ (rad/s) | 1.000 | 0.517 |
| Gain margin | 5.00 (14.0 dB) | 1.53 (3.7 dB) |
| Nyquist crossing $`\mathrm{Re}\,L`$ at $\omega_{pc}$ | $-0.200$ | $-0.652$ |
| Delay margin $T_{dm}$ (s) | 1.86 | 0.86 |
| Peak sensitivity $M_s$ | 1.85 | 4.13 |

Without delay the phase crossover can be found by hand: $\arctan(2\omega) + \arctan(0.5\omega) = 90^\circ$ requires $2\omega \cdot 0.5\omega = 1$, so $\omega_{pc} = 1$ rad/s, and $\lvert L(j1)\rvert = 0.5/(1 \cdot \sqrt{5} \cdot \sqrt{1.25}) = 0.2$. The margins computed from the Bode functions and the crossings read off the Nyquist curve agree to the precision of the frequency grid, as the unit tests check. The delay margin of 1.86 s without delay equals the 1 s pipe delay plus the 0.86 s that remain with it.

Both margins are needed. A loop can have a large gain margin and a small phase margin, or the reverse, and in either case come close to $-1$; $M_s$ measures the closest approach directly.

## Bandwidth and Closed-Loop Damping

The closed-loop bandwidth $\omega_{BW}$ is the frequency at which $\lvert T(j\omega)\rvert = \lvert L/(1 + L)\rvert$ falls 3 dB below its low-frequency value. For a loop with a single crossover, $\omega_{gc} \leq \omega_{BW} \leq 2\omega_{gc}$ for phase margins between about $30^\circ$ and $90^\circ$, so the crossover frequency sets the speed of response: for the standard second-order loop with $0.3 \leq \zeta \leq 0.7$ the 10–90% rise time lies between $1.2/\omega_{gc}$ and $1.4/\omega_{gc}$.

The phase margin sets the damping. For the loop $L(s) = \omega_n^2/[s(s + 2\zeta\omega_n)]$, whose closed loop is the standard second-order system, solving $\lvert L(j\omega_{gc})\rvert = 1$ gives

$$
PM = \arctan \frac{2\zeta}{\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}}
$$

| $\zeta$ | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $PM$ | $11.4^\circ$ | $22.6^\circ$ | $33.3^\circ$ | $43.1^\circ$ | $51.8^\circ$ | $59.2^\circ$ | $65.2^\circ$ |
| $M_r$ | 5.03 | 2.55 | 1.75 | 1.36 | 1.15 | 1.04 | 1.00 |
| $\omega_{BW}/\omega_n$ | 1.54 | 1.51 | 1.45 | 1.37 | 1.27 | 1.15 | 1.01 |

Up to about $65^\circ$ the table is close to the rule of thumb $\zeta \approx PM/100$ with $PM$ in degrees. Applied to other loops it is an estimate: for the level loop, $PM = 41.2^\circ$ corresponds to $\zeta = 0.38$ and a predicted overshoot of 27.5%, against 28.8% in the simulated response; with the delay, $PM = 19.0^\circ$ gives $\zeta = 0.17$ and a predicted 58.7%, against 64.8%.

![Sensitivity and complementary sensitivity magnitudes, and closed-loop level responses to a 1 m set-point step, with and without delay](../../../scripts/algorithms/control_bode_nyquist/control_sensitivity.png)

Panel (a) shows the cost of the delay as a sensitivity peak of $M_s = 4.13$ (12.3 dB) near 0.45 rad/s: disturbances near that frequency are amplified four times instead of being attenuated. Panel (b) shows the matching set-point responses.

## Loop Shaping

Design in the frequency domain is a matter of shaping $\lvert L(j\omega)\rvert$, with $S = 1/(1 + L)$ and $T = L/(1 + L)$ as the closed-loop functions ([Feedback Control](./feedback_control.md)):

1. At low frequency, where references and disturbances live, make $\lvert L\rvert \gg 1$, so that $\lvert S\rvert \approx 1/\lvert L\rvert$ is small. An integrator in $L$ makes $\lvert L\rvert$ infinite at $\omega = 0$ and removes steady-state error to steps.
2. At high frequency, where sensor noise and unmodelled dynamics (structural modes, actuator lags) live, make $\lvert L\rvert \ll 1$, so that $\lvert T\rvert \approx \lvert L\rvert$ is small.
3. Cross over between the two at the frequency that gives the required speed, with a slope of about $-20$ dB/decade over roughly a decade around $\omega_{gc}$. By the gain–phase relation this gives a phase near $-90^\circ$ to $-120^\circ$ there, so a phase margin of $60^\circ$ to $90^\circ$; a slope of $-40$ dB/decade at crossover leaves almost no margin.

Lead compensation adds phase near the crossover, lag compensation adds low-frequency gain without moving the crossover, and PI and PID controllers do both in a fixed form. The crossover frequency cannot be pushed arbitrarily high: a delay $T$ costs $\omega T$ radians of phase at crossover, which limits $\omega_{gc}$ to roughly $1/T$, and Bode's sensitivity integral states that, for a stable open loop with at least two more poles than zeros, $`\int_0^\infty \ln\lvert S(j\omega)\rvert\,d\omega = 0`$: attenuation at some frequencies must be paid for with amplification at others.

## Key Takeaways

- $G(j\omega)$ is the steady-state amplitude ratio and phase shift for a sinusoid of frequency $\omega$, and can be measured without a model.
- On a Bode plot the factors add; straight-line asymptotes are accurate to 3 dB and $6^\circ$ away from the corners.
- The Nyquist criterion $Z = N + P$ decides closed-loop stability from the open-loop plot, including loops with time delay.
- Gain margin, phase margin and delay margin measure the distance from instability; $M_s$ bounds the first two and is the most compact robustness measure.
- The phase margin sets the closed-loop damping ($\zeta \approx PM/100$), and the crossover frequency sets its speed.
- A delay leaves the magnitude unchanged but costs $\omega T$ of phase, and limits the achievable crossover to roughly $1/T$.

## Related Scripts

- [Bode and Nyquist Margins](../../../scripts/algorithms/control_bode_nyquist/): computes the Bode magnitude and phase with straight-line asymptotes, the gain, phase and delay margins, the Nyquist plot and its encirclements of $-1$, the sensitivity functions and the closed-loop step response of a tank level loop with and without a transport delay.
- [Second-Order Step Response](../../../scripts/algorithms/control_second_order_response/): simulates the step response of the standard second-order system for six damping ratios, measures rise time, peak time, overshoot and settling time, and compares them with the closed-form formulas and the pole locations.

## Exercises

**Exercise 1.** Find the gain crossover frequency, phase margin and gain margin of $L(s) = \frac{10}{s(s+1)}$. Sketch the magnitude asymptotes and compare the asymptotic crossover with the exact one.

<details>
<summary>Answer</summary>

$\lvert L(j\omega)\rvert = \frac{10}{\omega\sqrt{\omega^2+1}} = 1$ gives $\omega^4 + \omega^2 - 100 = 0$, so $\omega^2 = 9.51$ and $\omega_{gc} = 3.08$ rad/s.

```math
PM = 180^\circ - 90^\circ - \arctan(3.08) = 18.0^\circ
```

The phase only approaches $-180^\circ$ as $\omega \to \infty$, so there is no phase crossover and the gain margin is infinite. The phase margin is far below $45^\circ$, so the step response is oscillatory ($\zeta \approx 0.16$).

The asymptotes are $20$ dB at $\omega = 1$ falling at $-20$ dB/decade, then $-40$ dB/decade above the corner at 1 rad/s; they reach 0 dB at $\omega = \sqrt{10} = 3.16$ rad/s, close to the exact 3.08 rad/s.

</details>

**Exercise 2.** For $L(s) = \frac{10}{s(s+1)(0.1s+1)}$, find the phase crossover frequency and the gain margin by hand, the phase margin numerically, and the smallest time delay that destabilizes the loop.

<details>
<summary>Answer</summary>

The phase is $-90^\circ - \arctan\omega - \arctan(0.1\omega)$. It reaches $-180^\circ$ when $\arctan\omega + \arctan(0.1\omega) = 90^\circ$, that is when $\omega \cdot 0.1\omega = 1$: $\omega_{pc} = \sqrt{10} = 3.16$ rad/s.

```math
\lvert L(j\omega_{pc})\rvert = \frac{10}{3.162\sqrt{11}\sqrt{1.1}} = 0.909, \qquad GM = 1.10 \ (0.83 \text{ dB})
```

Solving $\lvert L(j\omega)\rvert = 1$ numerically gives $\omega_{gc} = 3.01$ rad/s and $PM = 180^\circ - 90^\circ - \arctan 3.01 - \arctan 0.301 = 1.6^\circ$. The delay margin is $T_{dm} = (1.6^\circ \times \pi/180)/3.01 = 0.009$ s: a delay of 9 ms destabilizes the loop. The Routh array of $0.1s^3 + 1.1s^2 + s + K$ confirms that the loop becomes unstable at $K = 11$, only 10% above the actual gain.

</details>

**Exercise 3.** An open-loop transfer function has one right-half-plane pole ($P = 1$). Using $Z = N + P$, state whether the closed loop is stable when the Nyquist plot (a) encircles $-1$ once counterclockwise, (b) does not encircle $-1$, (c) encircles $-1$ once clockwise.

<details>
<summary>Answer</summary>

(a) $N = -1$, so $Z = 0$: stable. (b) $N = 0$, so $Z = 1$: one closed-loop right-half-plane pole, unstable. (c) $N = +1$, so $Z = 2$: unstable.

An open-loop unstable plant can only be stabilized by a loop whose Nyquist plot encircles $-1$ counterclockwise once for every unstable open-loop pole; for such a plant, "no encirclement" does not mean stable.

</details>

**Exercise 4.** A unity-feedback loop has $L(s) = \frac{K}{s(s+2)}$. Find $K$ for a phase margin of $50^\circ$ and predict the overshoot of the closed-loop step response.

<details>
<summary>Answer</summary>

The closed loop is $K/(s^2 + 2s + K)$, so $\omega_n = \sqrt{K}$ and $2\zeta\omega_n = 2$. Solving the phase-margin formula for $PM = 50^\circ$ gives $\zeta = 0.478$, then $\omega_n = 1/\zeta = 2.09$ rad/s and $K = \omega_n^2 = 4.38$. A direct check: $\lvert L(j\omega)\rvert = 1$ at $\omega_{gc} = 1.68$ rad/s, where $PM = 90^\circ - \arctan(1.68/2) = 50.0^\circ$.

The overshoot is $`M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} = 18.1\%`$. The rule $\zeta \approx PM/100 = 0.5$ would predict 16.3%.

</details>

**Exercise 5.** In the tank level loop with the 1 s pipe delay, the phase margin is only $19^\circ$. Find the loop gain $K$ and the controller gain $K_c$ that restore a phase margin of $45^\circ$, and the resulting gain margin. What is lost?

<details>
<summary>Answer</summary>

The phase does not depend on $K$, so first find the frequency where the phase is $-135^\circ$:

```math
90^\circ + \arctan(2\omega) + \arctan(0.5\omega) + \frac{180^\circ}{\pi}\,\omega \cdot 1 = 135^\circ \quad\Rightarrow\quad \omega = 0.233 \text{ rad/s}
```

This must become the gain crossover, so $K = \omega\sqrt{1 + 4\omega^2}\sqrt{1 + 0.25\omega^2} = 0.259$ s⁻¹ and $K_c = KA/k_q = 5.2$ V/m, about half the original gain. The phase crossover stays at 0.517 rad/s, where the gain margin is now 2.96 (9.4 dB).

The crossover frequency falls from 0.388 to 0.233 rad/s, so the loop responds and rejects disturbances about 1.7 times more slowly: the delay, not the controller, limits the achievable speed.

</details>

## References

- G. F. Franklin, J. D. Powell, A. Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th ed., Pearson, 2019.
- K. Ogata, *Modern Control Engineering*, 5th ed., Prentice Hall, 2010.
- N. S. Nise, *Control Systems Engineering*, 8th ed., Wiley, 2019.
- K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, Princeton University Press, 2008.
- S. Skogestad, I. Postlethwaite, *Multivariable Feedback Control: Analysis and Design*, 2nd ed., Wiley, 2005.
- H. W. Bode, *Network Analysis and Feedback Amplifier Design*, Van Nostrand, 1945.
- H. Nyquist, "Regeneration theory", *Bell System Technical Journal*, 11(1), 126–147, 1932.
