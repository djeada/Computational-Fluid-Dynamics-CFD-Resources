# Turbulence Statistics

Turbulence is governed by deterministic equations, yet two runs of the same experiment never produce the same velocity signal. Tiny differences in initial and boundary conditions are amplified until the details are effectively unpredictable. What *is* reproducible is the statistics: mean velocity, variance, correlation between components, how far apart two points must be before their velocities become independent, and how energy is distributed among scales.

This page treats the velocity as a random field and introduces the statistical tools used throughout turbulence theory and modeling. The notation $\langle \cdot \rangle$ denotes the expectation, i.e. the ensemble average. It is the same operation written as an overbar in [Reynolds Decomposition](./reynolds_decomposition.md), and fluctuations are written $u' = u - \langle u \rangle$.

## Random Variables and Probability Density Functions

Consider the streamwise velocity $u$ at a fixed point and time. Distinguish the random variable $u$ from the **sample-space variable** $V$, which stands for a possible value of $u$.

The **cumulative distribution function** (CDF) is

$$
F(V) = \mathrm{Prob}(u < V)
$$

and the **probability density function** (PDF) is its derivative, $f(V) = dF/dV$. The PDF has the properties

$$
f(V) \ge 0,
\qquad \int_{-\infty}^{\infty} f(V)\, dV = 1,
\qquad \mathrm{Prob}(a \le u < b) = \int_a^b f(V)\, dV
$$

The PDF contains everything there is to know about $u$ at one point and one time. Expectations of any function $Q(u)$ follow from it:

$$
\langle Q(u) \rangle = \int_{-\infty}^{\infty} Q(V)\, f(V)\, dV
$$

In an experiment the PDF is estimated from a normalized histogram of samples.

For two variables, such as $u$ and $v$ at the same point, the **joint PDF** $f_{uv}(V_1, V_2)$ gives the probability density of the pair. Integrating over one variable recovers the marginal PDF of the other. Joint PDFs of velocity components are tilted ellipses in shear flows, which is the statistical signature of the Reynolds shear stress.

## Moments

The mean is the first moment, $\langle u \rangle = \int V f(V)\,dV$. Higher-order **central moments** describe the shape of the PDF:

$$
\mu_n = \langle (u - \langle u \rangle)^n \rangle = \int_{-\infty}^{\infty}
(V - \langle u \rangle)^n f(V)\, dV
$$

The standard normalized measures are:

| Moment | Definition | Measures |
| --- | --- | --- |
| Variance | $\sigma^2 = \langle u'^2 \rangle$ | Spread; $\sigma = u_{rms}$ |
| Skewness | $S = \langle u'^3 \rangle / \sigma^3$ | Asymmetry of the PDF |
| Flatness (kurtosis) | $F = \langle u'^4 \rangle / \sigma^4$ | Weight of the tails, i.e. how often extreme events occur |

Reference values help with interpretation:

| Distribution | $S$ | $F$ |
| --- | --- | --- |
| Gaussian | 0 | 3 |
| Uniform | 0 | 1.8 |
| Pure sine wave | 0 | 1.5 |

In turbulence:

- **Velocity** PDFs in homogeneous turbulence are close to Gaussian, with $S \approx 0$ and $F \approx 3$.
- **Wall-bounded and free shear flows** show strong departures near walls and at the edges of jets, wakes and boundary layers. There the flow alternates between turbulent and irrotational fluid (**intermittency**), producing large skewness and flatness.
- **Velocity derivatives** are distinctly non-Gaussian. The longitudinal derivative $\partial u/\partial x$ has a skewness of about $-0.5$. The negative sign is linked to vortex stretching and the net transfer of energy to small scales. Derivative flatness exceeds 3 and increases with Reynolds number, which reflects the spotty, intermittent nature of small-scale dissipation.

## Covariance and Correlation Coefficient

The **covariance** of two fluctuating quantities is $\langle u'v' \rangle$. Normalizing gives the **correlation coefficient**:

$$
\rho_{uv} = \frac{\langle u'v' \rangle}{u_{rms}\,v_{rms}},
\qquad - 1 \le \rho_{uv} \le 1
$$

In boundary layers and channel flows, $\rho_{uv}$ is typically of order $-0.4$ to $-0.5$ across much of the layer. The velocities are clearly correlated, but far from perfectly.

The covariance matrix of the three velocity components *is* the Reynolds stress tensor $\langle u_i'u_j' \rangle$. Its eigenvectors are the principal axes of the velocity fluctuations. The same idea, applied to whole fields rather than single points, underlies proper orthogonal decomposition (POD).

## Stationarity, Homogeneity and Isotropy

Symmetries of the statistics simplify analysis enormously.

- **Statistically stationary**: all statistics are invariant under a shift in time. A long time average then equals the ensemble average.
- **Statistically homogeneous**: all statistics are invariant under a shift in space. Mean gradients vanish, and single-point statistics are the same everywhere. A flow can be homogeneous in some directions only. Fully developed channel flow is homogeneous in $x$ and $z$ but not in $y$.
- **Statistically isotropic**: statistics are also invariant under rotations and reflections of the coordinate system. The Reynolds stress then reduces to $\langle u_i'u_j' \rangle = \frac{2}{3}k\,\delta_{ij}$: equal normal stresses and zero shear stresses. Isotropic turbulence cannot sustain a mean shear, so it decays unless forced.

The closest laboratory approximation is **grid turbulence**, the decaying turbulence behind a mesh in a uniform wind-tunnel flow. Most practical flows are anisotropic at large scales. However, Kolmogorov's hypothesis of **local isotropy** asserts that the *small* scales become isotropic at high Reynolds number (see [Energy Cascade](./energy_cascade.md)).

## Two-Point and Two-Time Correlations

Single-point statistics say nothing about the size of turbulent structures. For that we correlate velocities at two points:

$$
R_{ij}(\mathbf{r};\mathbf{x},t) = \langle u_i'(\mathbf{x},t)\,
u_j'(\mathbf{x} + \mathbf{r},t) \rangle
$$

In homogeneous turbulence $R_{ij}$ depends only on the separation $\mathbf{r}$. It satisfies $R_{ij}(\mathbf{0}) = \langle u_i'u_j' \rangle$ and $R_{ij}(\mathbf{r}) = R_{ji}(-\mathbf{r})$.

At a single point in a stationary flow, the analogous quantity is the **autocorrelation** in time:

$$
R(s) = \langle u'(t)\, u'(t + s) \rangle,
\qquad \rho(s) = \frac{R(s)}{\langle u'^2 \rangle}
$$

It is even in $s$, with $\rho(0) = 1$ and $\lvert \rho(s) \rvert \le 1$.

### Longitudinal and Transverse Correlations

In isotropic turbulence two scalar functions describe $R_{ij}$ completely. With the separation along $x_1$, they are the **longitudinal** correlation $f(r)$, in which the velocity component is parallel to the separation, and the **transverse** correlation $g(r)$, in which it is perpendicular.

```
 Longitudinal f(r):                     Transverse g(r):

   u1 -->           u1 -->                ^ u2              ^ u2
   o----------------o                     o-----------------o
   x             x + r e1                 x              x + r e1
```

$$
f(r) = \frac{\langle u_1'(\mathbf{x})\,u_1'(\mathbf{x} + r\mathbf{e}_1) \rangle}{\langle u_1'^2 \rangle},
\qquad
g(r) = \frac{\langle u_2'(\mathbf{x})\,u_2'(\mathbf{x} + r\mathbf{e}_1) \rangle}{\langle u_2'^2 \rangle}
$$

In terms of these,

$$
R_{ij}(\mathbf{r}) = u'^2\left[g(r)\,\delta_{ij} + \big(f(r) - g(r)\big)
\frac{r_i r_j}{r^2}\right]
$$

where $u'^2$ is the variance of any single component. Incompressibility links the two functions:

$$
g(r) = f(r) + \frac{r}{2} \frac{df}{dr}
$$

## Integral Scales

The **integral time scale** and the **integral length scale** measure how long, and over what distance, the velocity stays correlated:

$$
\mathcal{T} = \int_0^\infty \rho(s)\, ds,
\qquad L_{11} = \int_0^\infty f(r)\, dr,
\qquad L_{22} = \int_0^\infty g(r)\, dr
$$

For isotropic turbulence $L_{22} = L_{11}/2$ (Exercise 5). The integral length scale is a measure of the size of the energy-containing eddies. For an exponential correlation $\rho(s) = e^{-\lvert s \rvert/\tau}$ the integral scale is simply $\tau$.

Correlations with negative lobes, such as signals with a strong periodic component, can have small integral scales even though the correlation persists over long times. Always look at the whole function, not just its integral.

### How Long Must You Measure?

Integral scales determine how quickly statistics converge. The mean estimated from a record of length $T$ is itself a random variable, with variance

$$
\mathrm{var}\left(\frac{1}{T}\int_0^T u\, dt\right) = \frac{1}{T^2}\int_0^T\int_0^T
R(t - t')\, dt\, dt' \approx \frac{2\,\mathcal{T}\,\sigma^2}{T}
\qquad (T \gg \mathcal{T})
$$

The record therefore behaves as if it contained $N_{eff} \approx T/(2\mathcal{T})$ independent samples, however fast it was sampled. Sampling faster than about once per integral time scale adds almost no statistical information about the mean. It is still needed for resolving spectra.

## Taylor Microscales

Expanding the correlation functions near the origin defines the **Taylor microscales** $\lambda_f$ and $\lambda_g$ through the osculating parabolas:

$$
f(r) \approx 1 - \frac{r^2}{\lambda_f^2},
\qquad g(r) \approx 1 - \frac{r^2}{\lambda_g^2}
$$

In isotropic turbulence $\lambda_f = \sqrt{2}\,\lambda_g$, and the dissipation rate can be written as

$$
\varepsilon = 15\,\nu \left\langle \left(\frac{\partial u_1'}{\partial x_1}\right)^2
\right\rangle = 15\,\nu\, \frac{u'^2}{\lambda_g^2}
$$

This is how $\varepsilon$ is estimated from single hot-wire measurements, using Taylor's hypothesis (below) to convert time derivatives into space derivatives. The **Taylor-scale Reynolds number** $R_\lambda = u'\lambda_g/\nu$ is the standard way to quote the Reynolds number of homogeneous turbulence. It is related to the large-scale Reynolds number by $R_\lambda = (20\,R_L/3)^{1/2}$, where $R_L = k^2/(\varepsilon\nu)$. The Taylor microscale lies between the integral scale and the Kolmogorov scale. It is a convenient length, not the size of any identifiable eddy.

## Taylor's Frozen-Turbulence Hypothesis

A single probe gives a time series, but theory is usually phrased in terms of spatial structure. G. I. Taylor (1938) suggested that when turbulence is swept past a probe by a mean velocity $U$ much larger than the fluctuations, the eddies change little while they pass. The pattern behaves as if frozen and convected:

$$
u'(x, t + s) \approx u'(x - U s, t)
\qquad \Longrightarrow
\qquad \frac{\partial}{\partial t} \approx - U \frac{\partial}{\partial x}
$$

The consequences are:

- a time lag $s$ corresponds to a streamwise separation $r = U s$, so $L_{11} \approx U\,\mathcal{T}$;
- a frequency $f$ (Hz) corresponds to a streamwise wavenumber $\kappa_1 = 2\pi f / U$ (rad/m).

The hypothesis works well when $u_{rms}/U$ is small, roughly 10–20% or less. It degrades in highly turbulent jets, in separated and recirculating regions, and close to walls, where eddies may be convected at a speed different from the local mean velocity.

## Energy Spectra and the Wiener–Khinchin Relation

### Frequency Spectrum

For a stationary signal the **Wiener–Khinchin theorem** states that the autocovariance and the power spectral density form a Fourier transform pair. Using a one-sided spectrum over $\omega \ge 0$:

$$
E(\omega) = \frac{1}{\pi}\int_{-\infty}^{\infty} R(s)\, e^{-i\omega s}\,
ds = \frac{2}{\pi}\int_0^\infty R(s)\cos(\omega s)\, ds
$$

$$
R(s) = \int_0^\infty E(\omega)\cos(\omega s)\, d\omega
$$

Two consequences follow immediately:

$$
\langle u'^2 \rangle = R(0) = \int_0^\infty E(\omega)\, d\omega,
\qquad E(0) = \frac{2}{\pi}\langle u'^2 \rangle\,\mathcal{T}
$$

The first says the variance is distributed over frequencies, with $E(\omega)\,d\omega$ the contribution from the band $d\omega$. The second says the low-frequency plateau of the spectrum measures the integral time scale.

For example, the exponential autocorrelation $R(s) = \sigma^2 e^{-\lvert s \rvert/\tau}$ has the spectrum

$$
E(\omega) = \frac{2\sigma^2\tau/\pi}{1 + \omega^2\tau^2}
$$

This spectrum is flat for $\omega\tau \ll 1$ and rolls off as $\omega^{-2}$ for $\omega\tau \gg 1$. Real turbulence rolls off as $\omega^{-5/3}$ over the inertial range, then faster in the dissipation range. In practice spectra are computed with FFTs of windowed segments, averaged together (Welch's method).

### Wavenumber Spectra

In homogeneous turbulence the two-point correlation is transformed in space. The **velocity spectrum tensor** is

$$
\Phi_{ij}(\boldsymbol{\kappa}) = \frac{1}{(2\pi)^3}\int R_{ij}(\mathbf{r})\,
e^{-i\boldsymbol{\kappa}\cdot\mathbf{r}}\, d\mathbf{r}
$$

Integrating half its trace over spherical shells of radius $\kappa = \lvert \boldsymbol{\kappa} \rvert$ removes directional information and gives the **energy spectrum function** $E(\kappa)$, which satisfies

$$
k = \int_0^\infty E(\kappa)\, d\kappa,
\qquad \varepsilon = 2\nu\int_0^\infty \kappa^2 E(\kappa)\, d\kappa
$$

The factor $\kappa^2$ shows that energy sits at small wavenumbers (large eddies) while dissipation sits at large wavenumbers (small eddies).

Experiments usually measure a **one-dimensional spectrum** along a line:

$$
E_{11}(\kappa_1) = \frac{1}{\pi}\int_{-\infty}^{\infty} R_{11}(r\,\mathbf{e}_1)\,
e^{-i\kappa_1 r}\, dr,
\qquad L_{11} = \frac{\pi\,E_{11}(0)}{2\langle u_1'^2 \rangle}
$$

In isotropic turbulence it is related to $E(\kappa)$ by

$$
E_{11}(\kappa_1) = \int_{\kappa_1}^\infty
\frac{E(\kappa)}{\kappa}\left(1 - \frac{\kappa_1^2}{\kappa^2}\right)d\kappa
$$

A line measurement at wavenumber $\kappa_1$ picks up contributions from all three-dimensional wavenumbers with $\kappa \ge \kappa_1$, i.e. from eddies whose wavevector is oblique to the line. This **aliasing** is why $E_{11}$ stays finite and flat as $\kappa_1 \to 0$, while $E(\kappa)$ goes to zero.

## Worked Example: Interpreting a Hot-Wire Record

A hot-wire in a wind tunnel measures $U = 12$ m/s and $u_{rms} = 0.9$ m/s. The measured autocorrelation is well fitted by an exponential with integral time scale $\mathcal{T} = 8$ ms.

I. **Is Taylor's hypothesis reasonable?** $u_{rms}/U = 0.075$, so yes.

II. **Integral length scale.** $L_{11} \approx U\mathcal{T} = 12 \times 0.008 = 0.096$ m, about 10 cm.

III. **Spectrum.** The fitted exponential gives a spectrum that is flat up to $\omega\tau \approx 1$, i.e. $f = 1/(2\pi\mathcal{T}) = 19.9$ Hz. Frozen turbulence maps frequencies to wavelengths $\Lambda = U/f$:

| $f$ (Hz) | $\kappa_1 = 2\pi f/U$ (rad/m) | Wavelength $U/f$ (m) |
| --- | --- | --- |
| 10 | 5.24 | 1.2 |
| 100 | 52.4 | 0.12 |
| 1000 | 524 | 0.012 |

IV. **Record length.** Suppose the mean must be known to within $\pm 0.5\%$ of $U$ with 95% confidence (1.96 standard deviations). Then

$$
1.96\, u_{rms} \sqrt{\frac{2\mathcal{T}}{T}} \le 0.005\, U \quad \Longrightarrow \quad T
\ge 2\mathcal{T}\left(\frac{1.96\,u_{rms}}{0.005\,U}\right)^2 = 13.8\ \mathrm{s}
$$

This corresponds to $N_{eff} \approx 860$ independent samples. Sampling at 10 kHz for 13.8 s gives 138,000 samples, but only about 860 of them carry independent information about the mean. Higher moments, and statistics in regions with longer integral scales, need much longer records.

## Related Scripts

- [longitudinal_velocity_fluctuations_and_projections](../../../scripts/plots/longitudinal_velocity_fluctuations_and_projections/): scatter plots of two fluctuating velocity components, i.e. a sampled joint PDF, and their projection onto a direction. Relates the covariance matrix to POD.
- [correlation_functions](../../../scripts/algorithms/correlation_functions/): plots exponential, Gaussian, linear and cubic-spline correlation functions for several length-scale parameters. The script is written for kriging, but the exponential and Gaussian shapes are the standard model autocorrelations. Their integrals give the integral scale: $1/\theta$ for $e^{-\theta\lvert h \rvert}$.
- [turbulent_flow](../../../scripts/plots/turbulent_flow/): computes the mean and the squared fluctuation of a synthetic signal, whose average is the variance.
- [Mean Velocity Magnitude: Experiment vs CFD Comparison](../../../scripts/plots/mean_velocity_magnitude/): plots a mock experimental profile and a mock CFD scale-resolving simulation (SRS) profile of the normalised mean velocity magnitude $|U|/U_0$ along an under-body centreline.
- [Time-Averaged Velocity Field](../../../scripts/plots/time_averaged_velocity_field/): generates a synthetic noisy longitudinal velocity field on a 200 × 60 grid and compares it with its mean field, the first step of a Reynolds decomposition.

## Exercises

**Exercise 1.** A random variable is uniformly distributed on $[-a, a]$. Compute its variance, skewness and flatness, and compare the flatness with the Gaussian value.

<details>
<summary>Answer</summary>

The PDF is $f = 1/(2a)$ on $[-a, a]$, and the mean is zero.

- Variance: $\sigma^2 = \int_{-a}^{a} V^2/(2a)\,dV = a^2/3$.
- Skewness: $S = 0$ by symmetry.
- Fourth moment: $\langle u^4 \rangle = \int_{-a}^{a} V^4/(2a)\,dV = a^4/5$, so $F = (a^4/5)/(a^4/9) = 9/5 = 1.8$.

A flatness below 3 means lighter tails than a Gaussian: no extreme values at all beyond $\pm a$.

</details>

**Exercise 2.** A stationary signal has the autocorrelation $R(s) = \sigma^2 e^{-\lvert s \rvert/\tau}$. Show that its integral time scale is $\tau$. Use the Wiener–Khinchin relation to find $E(\omega)$, check that $\int_0^\infty E\,d\omega = \sigma^2$, and evaluate $E(0)$ for $\sigma = 0.9$ m/s and $\tau = 8$ ms.

<details>
<summary>Answer</summary>

**Integral scale.** $\mathcal{T} = \int_0^\infty e^{-s/\tau}\,ds = \tau$.

**Spectrum.** $E(\omega) = \frac{2}{\pi}\sigma^2\int_0^\infty e^{-s/\tau}\cos(\omega s)\,ds = \frac{2}{\pi}\sigma^2\frac{\tau}{1 + \omega^2\tau^2}$.

**Check.** $\int_0^\infty E\,d\omega = \frac{2\sigma^2\tau}{\pi}\cdot\frac{\pi}{2\tau} = \sigma^2$.

**Value at zero.** $E(0) = 2\sigma^2\tau/\pi = 2(0.81)(0.008)/\pi = 4.13 \times 10^{-3}\ \mathrm{m^2/s}$, i.e. $\mathrm{m^2/s^2}$ per rad/s. Inverting, $\mathcal{T} = \pi E(0)/(2\sigma^2) = 8$ ms, as it should be.

</details>

**Exercise 3.** A probe in a flow with $U = 10$ m/s shows a spectral peak at $f = 100$ Hz. What streamwise wavenumber and wavelength does this correspond to? Would you trust the conversion if $u_{rms} = 3$ m/s?

<details>
<summary>Answer</summary>

$\kappa_1 = 2\pi f/U = 2\pi(100)/10 = 62.8$ rad/m, and the wavelength is $U/f = 0.1$ m.

With $u_{rms}/U = 0.3$, eddies are advected at speeds varying by $\pm 30\%$ and evolve while passing the probe. The frozen-turbulence mapping then smears spectral features and becomes unreliable.

</details>

**Exercise 4.** You want the mean velocity in a flow with $U = 5$ m/s, $u_{rms} = 1$ m/s and $\mathcal{T} = 20$ ms to within $\pm 1\%$ of $U$ at 95% confidence. How long must you record?

<details>
<summary>Answer</summary>

$$
T = 2\mathcal{T}\left(\frac{1.96\,u_{rms}}{0.01\,U}\right)^2 = 0.04 \times
(39.2)^2 = 61.5\ \mathrm{s}
$$

Halving the tolerance quadruples the record length.

</details>

**Exercise 5.** Starting from the isotropic relation $g = f + \frac{r}{2}\frac{df}{dr}$, show that $L_{22} = L_{11}/2$. Assume $r f(r) \to 0$ as $r \to \infty$.

<details>
<summary>Answer</summary>

Integrate the relation from 0 to $\infty$:

$$
L_{22} = \int_0^\infty g\, dr = L_{11} + \frac{1}{2}\int_0^\infty r \frac{df}{dr}\, dr
$$

Integrate the last term by parts:

$$
\int_0^\infty r f'\, dr = \big[r f\big]_0^\infty - \int_0^\infty f\, dr = -L_{11}
$$

Hence $L_{22} = L_{11} - L_{11}/2 = L_{11}/2$. Transverse correlations decay faster than longitudinal ones and can go negative, a direct consequence of continuity.

</details>

## References

- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000. (Chapter 3: random variables and fields; Chapter 6: spectra and correlations in homogeneous turbulence.)
- Tennekes, H., and Lumley, J. L. *A First Course in Turbulence*. MIT Press, 1972. (Chapters 6–8.)
- Davidson, P. A. *Turbulence: An Introduction for Scientists and Engineers*. Oxford University Press, 2004.
- Bendat, J. S., and Piersol, A. G. *Random Data: Analysis and Measurement Procedures*, 4th ed. Wiley, 2010.
