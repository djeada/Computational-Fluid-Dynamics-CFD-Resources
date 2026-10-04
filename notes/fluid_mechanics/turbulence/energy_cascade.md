# Energy Cascade

Turbulent kinetic energy is produced at the largest scales of motion: shear, buoyancy or stirring feed eddies comparable in size to the flow itself. It is dissipated into heat by viscosity at the smallest scales, where velocity gradients are steep. In between, energy is handed down through a hierarchy of ever-smaller eddies. This **energy cascade** explains why turbulent dissipation does not depend on viscosity, why turbulence contains such a vast range of scales, and why simulating all of them directly is so expensive.

## Richardson's Cascade

L. F. Richardson summarized the idea in 1922 with a parody of a nursery rhyme: *"Big whorls have little whorls that feed on their velocity, and little whorls have lesser whorls and so on to viscosity."*

```
  energy input from the mean flow (shear, buoyancy, stirring)
        |
        v
  +------------------+   size l0, velocity u0, Re = u0 l0 / nu  >> 1
  |   large eddies   |   anisotropic, shaped by the geometry
  +------------------+
        |   break-up by inertial instabilities and vortex stretching,
        |   transfer rate ~ u0^3 / l0 (independent of viscosity)
        v
   +---------+  +---------+
   |  eddies |  |  eddies |    size l, Re_l = u(l) l / nu, still >> 1
   +---------+  +---------+
        |
        v
    [o][o][o][o][o]           size ~ eta, Re_eta ~ 1
        |
        v
  viscous dissipation into heat at rate epsilon
```

Three features of the cascade matter most.

1. Large eddies at high Reynolds number are hardly affected by viscosity. They are unstable and break up, passing their energy to smaller eddies on a time scale of about one turnover time.
2. The process repeats. At each stage the eddy Reynolds number $`Re_\ell = u(\ell)\,\ell/\nu`$ decreases.
3. The cascade stops when $Re_\ell$ approaches unity. There viscous stresses are as strong as inertia, and the energy is dissipated.

The rate is set at the top of the cascade. Viscosity only decides *where* the cascade ends.

## The Dissipation Estimate

An eddy of size $\ell_0$ and velocity $u_0$ holds kinetic energy of order $u_0^2$ per unit mass. It loses that energy in about one turnover time $\tau_0 = \ell_0/u_0$. The rate of energy transfer is therefore

$$
\Pi \sim \frac{u_0^2}{\tau_0} = \frac{u_0^3}{\ell_0}
$$

In statistically steady turbulence, whatever enters the cascade must leave it by dissipation, so

$$
\varepsilon \sim \frac{u_0^3}{\ell_0}
$$

Viscosity does not appear. Experiments and DNS confirm that $`\varepsilon\,\ell_0/u_0^3`$ tends to a constant of order one as the Reynolds number increases. This is sometimes called the "zeroth law" of turbulence.

It can look paradoxical, since the exact definition $\varepsilon = 2\nu\langle s_{ij}s_{ij} \rangle$ is proportional to $\nu$. The resolution is that the smallest scales adjust: as $\nu$ decreases, velocity gradients at the smallest scales grow so that $\langle s_{ij}s_{ij} \rangle \sim \varepsilon/\nu$.

For contrast, if a large eddy lost its energy by viscous diffusion alone, the decay time would be $\ell_0^2/\nu$. The ratio of that time to $\tau_0$ is $u_0\ell_0/\nu = Re$. Without the cascade, turbulence would take $Re$ times longer to decay.

## Kolmogorov's 1941 Hypotheses

A. N. Kolmogorov (1941) turned the cascade picture into a quantitative theory, now known as K41. In the form given by Pope (2000):

I. **Local isotropy.** At sufficiently high Reynolds number, the small-scale motions ($\ell \ll \ell_0$) are statistically isotropic. The directional information imposed by the mean flow and the boundaries is lost as energy passes down the cascade.

II. **First similarity hypothesis.** In every turbulent flow at sufficiently high Reynolds number, the statistics of the small-scale motions have a universal form that is uniquely determined by $\nu$ and $\varepsilon$.

III. **Second similarity hypothesis.** For scales in the range $\ell_0 \gg \ell \gg \eta$, the statistics have a universal form uniquely determined by $\varepsilon$, independent of $\nu$.

These hypotheses divide the scales into ranges. Pope suggests the representative boundaries $\ell_{EI} \approx \ell_0/6$ and $\ell_{DI} \approx 60\eta$.

```
  l0            l_EI ~ l0/6                 l_DI ~ 60 eta          eta
  |------------------|-----------------------------|------------------|
    energy-containing        inertial subrange         dissipation
          range                                           range
                     <-------- universal equilibrium range --------->
   (anisotropic,         (depends on epsilon only)   (depends on
    flow-dependent)                                   epsilon and nu)
```

The small eddies are called *universal* because their turnover times are much shorter than those of the large eddies. They adjust almost instantly to the energy flux handed to them, and they forget how it was generated.

## Kolmogorov Microscales

If the smallest scales depend only on $\nu$ ($\mathrm{m^2/s}$) and $\varepsilon$ ($\mathrm{m^2/s^3}$), there is exactly one length, one velocity and one time that can be formed from them:

$$
\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4},
\qquad u_\eta = (\nu\varepsilon)^{1/4},
\qquad \tau_\eta = \left(\frac{\nu}{\varepsilon}\right)^{1/2}
$$

Two identities confirm that these are the dissipative scales:

```math
\frac{u_\eta\,\eta}{\nu} = 1,
\qquad \varepsilon = \nu\left(\frac{u_\eta}{\eta}\right)^2 = \frac{\nu}{\tau_\eta^2}
```

The Reynolds number at the Kolmogorov scale is one, and the dissipation equals viscosity times the square of the Kolmogorov velocity gradient $1/\tau_\eta$.

### Ratios to the Large Scales

Substituting $\varepsilon \sim u_0^3/\ell_0$ and $Re = u_0\ell_0/\nu$:

$$
\frac{\eta}{\ell_0} = \left(\frac{\nu^3\ell_0}{u_0^3}\right)^{1/4}
\frac{1}{\ell_0} = Re^{-3/4},
\qquad \frac{u_\eta}{u_0} = Re^{-1/4},
\qquad \frac{\tau_\eta}{\tau_0} = Re^{-1/2}
$$

| $Re$ | $\ell_0/\eta$ | $u_0/u_\eta$ | $\tau_0/\tau_\eta$ |
| --- | --- | --- | --- |
| $10^3$ | 178 | 5.6 | 32 |
| $10^4$ | 1,000 | 10 | 100 |
| $10^5$ | 5,620 | 17.8 | 316 |
| $10^6$ | 31,600 | 31.6 | 1,000 |

The smallest eddies are slow compared with the large ones, but they are so small that their velocity *gradients*, $`u_\eta/\eta = (u_0/\ell_0)\,Re^{1/2}`$, are much larger. Energy lives in the large scales, while strain, vorticity and dissipation live in the small ones.

In the inertial range the second similarity hypothesis gives the velocity and time scale of an eddy of size $\ell$:

$$
u(\ell) \sim (\varepsilon\ell)^{1/3} = u_0\left(\frac{\ell}{\ell_0}\right)^{1/3},
\qquad \tau(\ell) \sim \left(\frac{\ell^2}{\varepsilon}\right)^{1/3}
$$

Both decrease with decreasing $\ell$. Smaller eddies are faster to adjust, which is the physical basis of their universality.

## The $-5/3$ Spectrum

In spectral terms, the second similarity hypothesis says that in the inertial range the energy spectrum $E(\kappa)$ can depend only on $\varepsilon$ and $\kappa$. Write $E = C\varepsilon^a\kappa^b$ and match dimensions, using $[E] = \mathrm{m^3/s^2}$, $[\varepsilon] = \mathrm{m^2/s^3}$ and $[\kappa] = \mathrm{m^{-1}}$. The seconds require $-2 = -3a$, so $a = 2/3$. The metres require $3 = 2a - b$, so $b = -5/3$. The result is the **Kolmogorov spectrum**:

```math
E(\kappa) = C\,\varepsilon^{2/3}\kappa^{-5/3},
\qquad C \approx 1.5
```

Experiments usually measure the one-dimensional spectrum. In the inertial range it follows $E_{11}(\kappa_1) = C_1\varepsilon^{2/3}\kappa_1^{-5/3}$, with $C_1 = \frac{18}{55}C \approx 0.49$ (see [Turbulence Statistics](./statistics.md)).

In physical space, the equivalent statement concerns the second-order structure function of velocity differences $\Delta u_L = u_1(\mathbf{x} + r\mathbf{e}_1) - u_1(\mathbf{x})$:

```math
\langle (\Delta u_L)^2 \rangle = C_2\,(\varepsilon r)^{2/3},
\qquad C_2 \approx 2.0
```

The third-order structure function obeys **Kolmogorov's four-fifths law**, which is exact for homogeneous isotropic turbulence at high Reynolds number:

```math
\langle (\Delta u_L)^3 \rangle = -\frac{4}{5}\,\varepsilon\, r
```

It follows from the Kármán–Howarth equation without any similarity assumption. Its negative sign encodes the net transfer of energy from large to small scales, which also explains the negative skewness of velocity derivatives.

```
 log E(k)
   ^
   |      ___
   |     /   \__
   |    /       \___           slope -5/3
   |   /            \___
   |  /                 \___
   | /                      \___
   |/  energy-      inertial    \__   dissipation
   |   containing   subrange       \    range
   +------|------------------------|--\------------> log k
        ~1/l0                    ~1/eta
```

Beyond the inertial range the spectrum falls off faster than any power of $\kappa$. The dissipation spectrum $2\nu\kappa^2 E(\kappa)$ peaks at $\kappa\eta \approx 0.26$ (Pope's model spectrum). Most dissipation therefore occurs at wavelengths of tens of Kolmogorov lengths, not at $\eta$ itself: with the same model, about 90% of $\varepsilon$ comes from $\kappa\eta > 0.1$.

### Refinements and Limits

- **Intermittency.** Dissipation is not uniform in space but concentrated in intense, thin structures. Kolmogorov's 1962 refined similarity theory, and later multifractal models, account for this. The correction to the $-5/3$ exponent is very small, but high-order structure functions deviate clearly from the K41 prediction $\langle (\Delta u_L)^p \rangle \propto r^{p/3}$.
- **Finite Reynolds number.** Laboratory and engineering flows often have too little scale separation for a clean inertial range. A $-5/3$ slope over one decade typically requires $R_\lambda$ of a few hundred.
- **Two-dimensional turbulence** behaves differently. Without vortex stretching, energy cascades to *larger* scales (an inverse cascade), while enstrophy cascades to smaller scales with $E(\kappa) \propto \kappa^{-3}$ (Kraichnan, 1967). Two-dimensional simulations such as a Kelvin–Helmholtz roll-up show vortices merging into ever-larger ones instead of breaking down.

## Worked Example: Kolmogorov Scales in a Water Pipe

Water ($\nu = 1.0 \times 10^{-6}\ \mathrm{m^2/s}$) flows through a smooth pipe with $D = 0.1$ m at a bulk velocity $U_b = 2$ m/s.

**Reynolds number.** $Re = U_b D/\nu = 2 \times 10^5$.

**Friction factor.** Prandtl's smooth-pipe law $1/\sqrt{f} = 2.0\log_{10}(Re\sqrt{f}) - 0.8$ gives $f = 0.0156$ (see [pipe flow](../internal_flow/pipes.md)).

**Mean dissipation.** In fully developed flow, all the pumping power ends up as heat. The pressure gradient is $\Delta p/L = f\rho U_b^2/(2D)$, and dividing the power per unit volume by $\rho$ gives the power per unit mass:

```math
\varepsilon \approx
\frac{(\Delta p/L)\,U_b}{\rho} = \frac{f\,U_b^3}{2D} = \frac{0.0156 \times 8}{0.2} = 0.63\ \mathrm{W/kg}
```

This is a volume average. The local dissipation is much larger near the wall and smaller on the centreline, and a small part of it is direct viscous dissipation of the mean flow.

**Kolmogorov scales.**

$$
\eta = \left(\frac{(10^{-6})^3}{0.63}\right)^{1/4} = 3.6 \times
10^{-5}\ \mathrm{m} = 36\ \mu\mathrm{m},
\qquad u_\eta = 0.028\ \mathrm{m/s},
\qquad \tau_\eta = 1.26\ \mathrm{ms}
$$

**Scale separation.** $D/\eta \approx 2{,}800$, whereas $Re^{3/4} \approx 9{,}500$. The difference arises because the energy-containing eddies are smaller and slower than $D$ and $U_b$. Taking $`u_0 \approx 0.1\,U_b = 0.2`$ m/s gives $\ell_0 \sim u_0^3/\varepsilon \approx 13$ mm. The eddy Reynolds number is then $Re_{\ell_0} \approx 2{,}600$, and $\ell_0/\eta \approx 360 = Re_{\ell_0}^{3/4}$. That equality is an identity once $\varepsilon = u_0^3/\ell_0$ is adopted. The point is that scale separation is governed by the Reynolds number of the energy-containing eddies, not the bulk Reynolds number.

**Inertial-range eddies.** $u(\ell) = (\varepsilon\ell)^{1/3}$ gives 0.18 m/s for a 10 mm eddy and 0.086 m/s for a 1 mm eddy.

**Wall units.** With $u_\tau = U_b\sqrt{f/8} = 0.088$ m/s, the viscous length is $\nu/u_\tau = 11\ \mu\mathrm{m}$ and $Re_\tau = 4{,}400$. Near the wall the required resolution is set by this length rather than by the average $\eta$ (see [RANS Equations](./rans_equations.md)).

## Implications for Direct Numerical Simulation

DNS resolves every scale, so its grid must span a domain of several integral scales and still resolve the dissipative scales:

- **Grid spacing.** Pseudo-spectral DNS commonly requires $\kappa_{max}\eta \ge 1.5$, i.e. $\Delta x \approx 2\eta$.
- **Points per direction.** $N \sim \ell_0/\eta \sim Re^{3/4}$.
- **Total grid points.** $N^3 \sim Re^{9/4}$.
- **Time steps.** Small eddies are swept past the grid at the large-eddy velocity, so a CFL limit gives $\Delta t \sim \eta/u_0$. A run must cover several $\tau_0 = \ell_0/u_0$, so the number of steps scales as $\ell_0/\eta \sim Re^{3/4}$.
- **Total cost.** $Re^{9/4} \times Re^{3/4} = Re^3$.

| $Re$ | Grid points $\sim Re^{9/4}$ | Relative cost $\sim Re^3$ |
| --- | --- | --- |
| $10^3$ | $5.6 \times 10^6$ | $10^9$ |
| $10^4$ | $10^9$ | $10^{12}$ |
| $10^5$ | $1.8 \times 10^{11}$ | $10^{15}$ |
| $10^6$ | $3.2 \times 10^{13}$ | $10^{18}$ |

Doubling the Reynolds number multiplies the grid by $2^{9/4} = 4.8$ and the cost by 8.

For the pipe above, a crude bounding box $D \times D \times 5D$ at $\Delta x = 2\eta = 71\ \mu\mathrm{m}$ would need about $1.4 \times 10^{10}$ points, for a flow that is modest by engineering standards. Wall-bounded DNS is in practice designed in wall units. Channel-flow DNS typically uses streamwise and spanwise spacings of order 10 and 5 viscous lengths, with the first point below $y^+ = 1$. The Reynolds-number scaling is similarly punishing.

This cost is the reason for large-eddy simulation and RANS modeling, discussed in [Turbulence Modeling](./modeling.md).

## Related Scripts

- [kelvin_helmholtz_instability](../../../scripts/simulations/kelvin_helmholtz_instability/): a shear-layer instability rolling up into large vortices, i.e. the mechanism that creates energy-containing eddies from mean shear. The simulation is two-dimensional, so it shows vortex merging (the 2D inverse cascade) rather than the 3D forward cascade described here.
- [laminar_vs_turbulent_pipe](../../../scripts/plots/laminar_vs_turbulent_pipe/): laminar and turbulent mean velocity profiles in a pipe, the setting of the worked example.

## Exercises

**Exercise 1.** In the atmospheric surface layer, typical dissipation rates range from $10^{-3}$ to $10^{-2}\ \mathrm{m^2/s^3}$. For air with $\nu = 1.5 \times 10^{-5}\ \mathrm{m^2/s}$, compute $\eta$ and $\tau_\eta$ at both ends of the range.

<details>
<summary>Answer</summary>

For $\varepsilon = 10^{-3}$:

- $\eta = (3.375 \times 10^{-15}/10^{-3})^{1/4} = 1.36$ mm
- $\tau_\eta = (1.5 \times 10^{-2})^{1/2} = 0.12$ s

For $\varepsilon = 10^{-2}$:

- $\eta = 0.76$ mm
- $\tau_\eta = 0.039$ s

A tenfold increase in $\varepsilon$ reduces $\eta$ only by $10^{1/4} = 1.78$. Sub-millimetre sensors and kHz sampling are needed to resolve atmospheric dissipation.

</details>

**Exercise 2.** You stir a cup of coffee, treated as water with $\nu = 10^{-6}\ \mathrm{m^2/s}$, with eddies of size $\ell_0 = 3$ cm and velocity $u_0 = 0.1$ m/s. Estimate $\varepsilon$, $\eta$, $\tau_\eta$ and the scale ratio $\ell_0/\eta$.

<details>
<summary>Answer</summary>

**Dissipation.** $\varepsilon \sim u_0^3/\ell_0 = 10^{-3}/0.03 = 0.033\ \mathrm{W/kg}$.

**Kolmogorov scales.** $\eta = (10^{-18}/0.033)^{1/4} = 74\ \mu\mathrm{m}$ and $\tau_\eta = (10^{-6}/0.033)^{1/2} = 5.5$ ms.

**Scale ratio.** $Re = u_0\ell_0/\nu = 3{,}000$, so $\ell_0/\eta = Re^{3/4} = 405$.

</details>

**Exercise 3.** A hot-wire in a flow at $U = 10$ m/s measures a one-dimensional spectrum value of $E_{11} = 2.0 \times 10^{-4}\ \mathrm{m^3/s^2}$ at $\kappa_1 = 100$ rad/m, inside the inertial range. Estimate $\varepsilon$, taking $C_1 = 0.49$. What frequency does this wavenumber correspond to?

<details>
<summary>Answer</summary>

**Dissipation.** Invert $E_{11} = C_1\varepsilon^{2/3}\kappa_1^{-5/3}$:

```math
\varepsilon = \left(\frac{E_{11}\,\kappa_1^{5/3}}{C_1}\right)^{3/2} = \left(\frac{2.0 \times 10^{-4} \times 100^{5/3}}{0.49}\right)^{3/2} = 0.82\ \mathrm{m^2/s^3}
```

**Frequency.** By Taylor's hypothesis, $f = \kappa_1 U/(2\pi) = 159$ Hz.

In practice one fits the compensated spectrum $\kappa_1^{5/3}E_{11}$ over the whole plateau rather than using a single point.

</details>

**Exercise 4.** A DNS of homogeneous turbulence at $Re = 10^4$ uses $10^9$ grid points and one week of computer time. Estimate the grid and run time for $Re = 2 \times 10^4$ and for $Re = 10^5$, assuming the same hardware.

<details>
<summary>Answer</summary>

**Doubling the Reynolds number.** Points grow by $2^{9/4} = 4.76$, to $4.8 \times 10^9$. Cost grows by $2^3 = 8$, to 8 weeks.

**Tenfold increase.** Points grow by $10^{9/4} = 178$, to $1.8 \times 10^{11}$. Cost grows by $10^3$, to about 1,000 weeks, roughly 19 years.

This is why DNS Reynolds numbers grow only slowly with hardware.

</details>

**Exercise 5.** Show that the $-5/3$ spectrum is consistent with the inertial-range eddy velocity $u(\ell) \sim (\varepsilon\ell)^{1/3}$. Compute the energy contained in all wavenumbers above $\kappa$ and compare it with $u(\ell)^2$ at $\ell = 1/\kappa$.

<details>
<summary>Answer</summary>

Integrate the inertial-range spectrum from $\kappa$ upward:

```math
\int_\kappa^\infty C\varepsilon^{2/3}\kappa'^{-5/3}\,
d\kappa' = \frac{3}{2}C\,\varepsilon^{2/3}\kappa^{-2/3}
```

With $\ell = 1/\kappa$ this becomes $`\frac{3}{2}C\,(\varepsilon\ell)^{2/3} \sim u(\ell)^2`$. The coefficient is $\frac{3}{2}(1.5) = 2.25$, of order one. The kinetic energy of eddies of size $\ell$ and smaller scales as $(\varepsilon\ell)^{2/3}$, exactly as the dimensional argument in physical space predicts.

</details>

## References

- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000. (Chapter 6: the scales of turbulent motion.)
- Frisch, U. *Turbulence: The Legacy of A. N. Kolmogorov*. Cambridge University Press, 1995.
- Tennekes, H., and Lumley, J. L. *A First Course in Turbulence*. MIT Press, 1972.
- Kolmogorov, A. N. "The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers." *Doklady Akademii Nauk SSSR*, 30, 1941. English translation reprinted in *Proceedings of the Royal Society of London A*, 434, 1991.
- Richardson, L. F. *Weather Prediction by Numerical Process*. Cambridge University Press, 1922.
