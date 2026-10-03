# Reynolds Decomposition

In a turbulent flow the velocity at a fixed point never settles to a steady value. It wanders irregularly around some typical level, and repeating the experiment gives a different trace every time. The instantaneous fields still obey the [Navier–Stokes equations](../governing_equations/navier_stokes.md) exactly, but predicting every wiggle is neither possible (the flow is extremely sensitive to initial and boundary conditions) nor usually needed. An engineer wants the *mean* drag, the *mean* heat flux, the *mean* pressure drop.

Osborne Reynolds (1895) proposed splitting every flow variable into a mean part and a fluctuating part, and averaging the governing equations. This page sets out that decomposition, the averaging operators behind it, the algebraic rules they obey, and the new unknown it produces: the **Reynolds stress tensor**.

```
 u
 ^      /\        /\  /\            /\
 |  /\ /  \  /\  /  \/  \    /\    /  \  /\
 |-/--V----\/--\/--------\--/--\--/----\/--\---- U   (mean)
 |/                       \/    \/          \
 |          u' > 0 above the line, u' < 0 below it
 +----------------------------------------------> t
```

## The Decomposition

Every instantaneous quantity is written as the sum of its mean and a fluctuation:

$$
u_i(\mathbf{x},t) = U_i(\mathbf{x},t) + u_i'(\mathbf{x},t),
\qquad p = P + p',
\qquad T = \overline{T} + T'
$$

where $U_i = \overline{u_i}$ is the mean velocity and $u_i'$ is the fluctuation. In these notes an overbar $\overline{(\cdot)}$ denotes the Reynolds average, and capital letters are used for mean velocity and pressure. The page on [turbulence statistics](./statistics.md) uses the equivalent probabilistic notation $\langle \cdot \rangle$.

By construction, averaging the decomposition gives $\overline{u_i} = \overline{U_i} + \overline{u_i'}$. For this to reduce to $\overline{u_i'} = 0$ we need $\overline{U_i} = U_i$, i.e. averaging must leave the mean unchanged. Whether that holds depends on the averaging operator, so the choice of average is not a detail.

## Averaging Operators

### Ensemble Average

Imagine $N$ nominally identical realizations of the flow (same geometry, same boundary conditions, microscopically different initial conditions). The ensemble average is

$$
\langle u_i \rangle(\mathbf{x},t) = \lim_{N \to \infty} \frac{1}{N}\sum_{n=1}^{N}
u_i^{(n)}(\mathbf{x},t)
$$

This is the most general definition. It allows the mean to depend on both position and time, so it handles flows whose statistics change in time: a starting jet, an engine cycle, a gust. Mathematically it is the expected value of a random field.

### Time Average

If the flow is **statistically stationary**, meaning its statistics do not change in time, the mean can be taken from a single long record:

$$
\overline{u_i}(\mathbf{x}) = \lim_{T \to \infty} \frac{1}{T}\int_{t_0}^{t_0+T}
u_i(\mathbf{x},t)\, dt
$$

The result is independent of $t_0$. In practice $T$ is finite, and it must be much longer than the integral time scale of the turbulence. The [statistics page](./statistics.md) shows how to estimate the required record length.

### Spatial Average

If the flow is **statistically homogeneous** in some direction, the mean can be taken along that direction. In a fully developed channel flow, statistics are homogeneous in the streamwise ($x$) and spanwise ($z$) directions:

$$
\overline{u_i}(y,t) = \lim_{L_x, L_z \to \infty}
\frac{1}{L_x L_z}\int_0^{L_z}\int_0^{L_x} u_i(x,y,z,t)\, dx\, dz
$$

DNS databases for channel flow are usually averaged over $x$, $z$ *and* $t$ to speed up convergence.

### Phase Average

Some turbulent flows contain a strong periodic component, such as vortex shedding behind a cylinder or blade passing in a turbomachine. Averaging at a fixed phase of the cycle separates the flow into a mean, a coherent periodic part, and a random part: $u = U + \hat{u} + u'$. This **triple decomposition** was introduced by Hussain and Reynolds (1970).

### Ergodicity

For a stationary flow, the time average equals the ensemble average. For a homogeneous flow, the spatial average equals the ensemble average. This **ergodic hypothesis** justifies what experimentalists and simulators actually do: take one long time series from one probe, or one large simulation, and treat its averages as ensemble statistics. Unsteady RANS (URANS) should be read in the ensemble sense. Interpreting its mean as a time average only makes sense when the mean-flow unsteadiness is much slower than the turbulence.

## Reynolds Averaging Rules

Let $f = F + f'$ and $g = G + g'$, let $a$ be a constant, and let $s$ be any of $x_1, x_2, x_3, t$. An ensemble average satisfies the following rules exactly.

I. **Linearity**: $\overline{f + g} = F + G$ and $\overline{a f} = a F$.

II. **Averaging a mean changes nothing**: $\overline{F} = F$, hence $\overline{f'} = 0$.

III. **Mean times fluctuation averages to zero**: $\overline{F g'} = F\,\overline{g'} = 0$.

IV. **Commutation with derivatives**: $\overline{\partial f/\partial s} = \partial F/\partial s$.

V. **Commutation with integrals**: $\overline{\int f\,ds} = \int F\,ds$.

The most important consequence is the rule for products:

$$
\overline{fg} = \overline{(F + f')(G + g')} = \overline{FG} + \overline{F g'} +
\overline{f' G} + \overline{f'g'} = FG + \overline{f'g'}
$$

The **correlation** $\overline{f'g'}$ is generally *not* zero, even though $\overline{f'}$ and $\overline{g'}$ are. The same expansion for a triple product gives

$$
\overline{fgh} = FGH + F\,\overline{g'h'} + G\,\overline{f'h'} + H\,\overline{f'g'} +
\overline{f'g'h'}
$$

Not every practical average obeys these rules.

- An infinite time average obeys them for stationary flow, where the time derivative of the mean is zero.
- A **finite-window** average does not satisfy rule II exactly. Averaging twice with a moving window of length $T$ is not the same as averaging once. For example, the window average of $u = U_0 + a\sin(\omega t)$ over $[0, T]$ equals $U_0 + a(1 - \cos\omega T)/(\omega T)$, which can differ from $U_0$ by up to $2a/(\omega T)$.
- The spatial **filters** used in large-eddy simulation violate rule II ($\overline{\overline{u}} \neq \overline{u}$). This is why the filtered equations contain extra terms that do not appear in RANS (see [Turbulence Modeling](./modeling.md)).

## Mean Continuity

For incompressible flow, $\partial u_i/\partial x_i = 0$. Averaging with rule IV gives

$$
\frac{\partial U_i}{\partial x_i} = 0
$$

Subtracting this from the instantaneous equation gives $\partial u_i'/\partial x_i = 0$. Both the mean and the fluctuating velocity fields are solenoidal.

## Mean Momentum and the Reynolds Stress Tensor

Using continuity, the incompressible momentum equation can be written in conservative form:

$$
\frac{\partial u_i}{\partial t} +
\frac{\partial (u_i u_j)}{\partial x_j} = -\frac{1}{\rho}
\frac{\partial p}{\partial x_i} + \nu \frac{\partial^2 u_i}{\partial x_j \partial x_j}
$$

Every linear term averages to the same term written in mean quantities. The convective term is the exception: by the product rule, $\overline{u_i u_j} = U_i U_j + \overline{u_i' u_j'}$. The averaged equation is therefore

$$
\frac{\partial U_i}{\partial t} + U_j
\frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho} \frac{\partial P}{\partial x_i} +
\frac{\partial}{\partial x_j}\left(\nu \frac{\partial U_i}{\partial x_j} -
\overline{u_i' u_j'}\right)
$$

The step-by-step derivation, the resulting closure problem, and the transport equations for $\overline{u_i'u_j'}$ and $k$ are covered in [RANS Equations](./rans_equations.md).

### Physical Meaning

Multiplied by $\rho$, the new term $-\rho\,\overline{u_i'u_j'}$ sits next to the viscous stress and has units of stress. It is called the **Reynolds stress**, but it is really a *momentum flux*. A fluctuating velocity $u_j'$ carries fluctuating momentum $\rho u_i'$ across a surface whose normal points in direction $j$. If $u_i'$ and $u_j'$ are correlated, that flux does not average to zero.

The tensor is

$$
\overline{u_i'u_j'} =
\begin{pmatrix}
\overline{u'^2} & \overline{u'v'} & \overline{u'w'} \\
\overline{u'v'} & \overline{v'^2} & \overline{v'w'} \\
\overline{u'w'} & \overline{v'w'} & \overline{w'^2}
\end{pmatrix}
$$

It has the following properties:

- It is **symmetric**, so it has six independent components.
- The diagonal entries are the **normal stresses** (variances), and they are never negative.
- The off-diagonal entries are the **shear stresses** (covariances). By the Cauchy–Schwarz inequality, $\lvert \overline{u'v'} \rvert \le u_{rms} v_{rms}$.
- The tensor is **positive semi-definite**. Its trace is twice the turbulent kinetic energy.

### Why the Shear Stress Has a Definite Sign

Consider a shear flow with $dU/dy > 0$, such as the lower half of a channel or a boundary layer.

```
                      v'
                      ^
     Q2  "ejection"   |   Q1
     u' < 0, v' > 0   |   u' > 0, v' > 0
  --------------------+--------------------> u'
     Q3               |   Q4  "sweep"
     u' < 0, v' < 0   |   u' > 0, v' < 0
```

A parcel moving upward ($v' > 0$) comes from a region of lower mean velocity. It therefore arrives with a velocity deficit ($u' < 0$), which is quadrant Q2, an ejection. A parcel moving downward brings high-speed fluid ($u' > 0$), which is Q4, a sweep. Q2 and Q4 events dominate, so $\overline{u'v'} < 0$ and $-\rho\,\overline{u'v'} > 0$. This has the same sign as the viscous stress $\mu\,dU/dy$. Turbulent mixing transports momentum down the mean gradient, like a greatly enhanced viscosity. That observation is the basis of the Boussinesq eddy-viscosity hypothesis.

### Anisotropy

The isotropic part of the Reynolds stress acts like a pressure. Only the deviatoric part transports momentum between layers. It is measured by

$$
a_{ij} = \overline{u_i'u_j'} - \frac{2}{3}k\,\delta_{ij},
\qquad b_{ij} = \frac{\overline{u_i'u_j'}}{2k} - \frac{1}{3}\delta_{ij}
$$

Both tensors have zero trace. The normalized anisotropy $b_{ij}$ vanishes for isotropic turbulence, and its eigenvalues lie between $-1/3$ and $2/3$.

## Turbulence Intensity and Turbulent Kinetic Energy

The root-mean-square fluctuation of a component is $u_{rms} = \sqrt{\overline{u'^2}}$. Referred to a velocity scale $U_{ref}$, this gives the **component turbulence intensity** $I_u = u_{rms}/U_{ref}$.

The **turbulent kinetic energy** (TKE) per unit mass is half the trace of the Reynolds stress tensor:

$$
k = \frac{1}{2}\overline{u_i'u_i'} = \frac{1}{2}\left(\overline{u'^2} +
\overline{v'^2} + \overline{w'^2}\right)
$$

It has units of $\mathrm{m^2/s^2}$. The mean of the total kinetic energy splits cleanly into a mean-flow part and a turbulent part:

$$
\overline{\tfrac{1}{2}u_i u_i} = \tfrac{1}{2}U_i U_i + k
$$

The **overall turbulence intensity** is defined from $k$ so that it equals $I_u$ when the turbulence is isotropic:

$$
I = \frac{\sqrt{2k/3}}{U_{ref}}
\qquad \Longleftrightarrow
\qquad k = \frac{3}{2}\left(I\, U_{ref}\right)^2
$$

This inversion is how CFD inlet conditions for $k$ are usually set (see [Turbulence Modeling](./modeling.md)).

## Worked Example: Statistics from a Velocity Record

A two-component probe in a boundary layer records eight simultaneous samples of $u$ and $v$ (m/s).

| Sample | $u$ | $v$ | $u'$ | $v'$ | $u'^2$ | $v'^2$ | $u'v'$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 10.8 | -0.2 | 0.8 | -0.2 | 0.64 | 0.04 | -0.16 |
| 2 | 9.1 | 0.5 | -0.9 | 0.5 | 0.81 | 0.25 | -0.45 |
| 3 | 11.6 | -0.6 | 1.6 | -0.6 | 2.56 | 0.36 | -0.96 |
| 4 | 8.7 | 0.1 | -1.3 | 0.1 | 1.69 | 0.01 | -0.13 |
| 5 | 10.3 | 0.4 | 0.3 | 0.4 | 0.09 | 0.16 | 0.12 |
| 6 | 9.5 | -0.3 | -0.5 | -0.3 | 0.25 | 0.09 | 0.15 |
| 7 | 11.2 | 0.2 | 1.2 | 0.2 | 1.44 | 0.04 | 0.24 |
| 8 | 8.8 | -0.1 | -1.2 | -0.1 | 1.44 | 0.01 | 0.12 |
| **Sum** | 80.0 | 0.0 | 0 | 0 | 8.92 | 0.96 | -1.07 |

**Means.** $U = 80.0/8 = 10.0$ m/s and $V = 0$.

**Second moments.** $\overline{u'^2} = 8.92/8 = 1.115\ \mathrm{m^2/s^2}$, $\overline{v'^2} = 0.96/8 = 0.12\ \mathrm{m^2/s^2}$, and $\overline{u'v'} = -1.07/8 = -0.134\ \mathrm{m^2/s^2}$.

**Correlation coefficient.** $\rho_{uv} = \overline{u'v'}/(u_{rms}v_{rms}) = -0.134/\sqrt{1.115 \times 0.12} = -0.37$. The value is negative, as the quadrant argument predicts.

**TKE.** $w$ was not measured. Assuming $\overline{w'^2} \approx \overline{v'^2}$ (a common assumption in boundary layers):

$$
k \approx \tfrac{1}{2}(1.115 + 0.12 + 0.12) = 0.678\ \mathrm{m^2/s^2}
$$

**Intensities.** $I_u = \sqrt{1.115}/10 = 10.6\%$, while $I = \sqrt{2(0.678)/3}/10 = 6.7\%$. The two differ because the turbulence is strongly anisotropic, with $b_{11} = 1.115/(2 \times 0.678) - 1/3 = 0.49$.

**Reynolds shear stress.** In air ($\rho = 1.2\ \mathrm{kg/m^3}$), $-\rho\,\overline{u'v'} = 0.16$ Pa.

Eight samples are far too few for converged statistics. The numbers only illustrate the arithmetic. How many *independent* samples are needed is discussed in [Turbulence Statistics](./statistics.md).

## Favre (Density-Weighted) Decomposition

When density varies (compressible flows, combustion, strongly heated flows), Reynolds averaging produces density–velocity correlations even in the continuity equation:

$$
\frac{\partial \overline{\rho}}{\partial t} +
\frac{\partial}{\partial x_j}\left(\overline{\rho}\,\overline{u_j} +
\overline{\rho' u_j'}\right) = 0
$$

The momentum equation acquires triple correlations such as $\overline{\rho' u_i' u_j'}$. Favre (1965) avoided this by using a **mass-weighted average**:

$$
\tilde{u}_i = \frac{\overline{\rho u_i}}{\overline{\rho}},
\qquad u_i = \tilde{u}_i + u_i''
$$

The rules change:

- $\overline{\rho\,u_i''} = 0$ holds, but the plain average $\overline{u_i''}$ is *not* zero.
- Instead, $\overline{u_i''} = \overline{u_i} - \tilde{u}_i = -\overline{\rho' u_i'}/\overline{\rho}$.
- Density and pressure are still Reynolds-averaged.

With these definitions the mean continuity equation keeps its laminar form:

$$
\frac{\partial \overline{\rho}}{\partial t} +
\frac{\partial (\overline{\rho}\,\tilde{u}_j)}{\partial x_j} = 0
$$

The mean momentum equation contains a single unclosed term, the Favre Reynolds stress $\overline{\rho}\,\widetilde{u_i''u_j''} = \overline{\rho\,u_i''u_j''}$:

$$
\frac{\partial (\overline{\rho}\,\tilde{u}_i)}{\partial t} +
\frac{\partial (\overline{\rho}\,\tilde{u}_i\tilde{u}_j)}{\partial x_j} = -\frac{\partial \overline{p}}{\partial x_i} + \frac{\partial \overline{\tau}_{ij}}{\partial x_j} - \frac{\partial \left(\overline{\rho}\,\widetilde{u_i''u_j''}\right)}{\partial x_j}
$$

The corresponding TKE is $\tilde{k} = \frac{1}{2}\widetilde{u_i''u_i''}$. Compressible RANS solvers therefore solve Favre-averaged equations. Boundary layers at moderate supersonic Mach numbers still behave much like incompressible ones once mean density variations are accounted for (Morkovin's hypothesis), so incompressible closures are often carried over.

## Related Scripts

- [turbulent_flow](../../../scripts/plots/turbulent_flow/): builds a synthetic velocity signal and plots $u$, $u' = u - \overline{u}$ and $u'^2$ with their means. This is the decomposition of this page applied to a time series.
- [time_averaged_velocity_field](../../../scripts/plots/time_averaged_velocity_field/): averages a 2D field along a homogeneous direction to obtain $\overline{u}(y)$ and the fluctuation field $u'(x,y)$.
- [longitudinal_velocity_fluctuations_and_projections](../../../scripts/plots/longitudinal_velocity_fluctuations_and_projections/): scatter plots of two correlated fluctuating components. The tilt of the data cloud is a visual picture of a nonzero correlation like $\overline{u'v'}$.

## Exercises

**Exercise 1.** Using only $u = U + u'$ and the averaging rules, show that $\overline{u'^2} = \overline{u^2} - U^2$. A probe reports $\overline{u^2} = 101.2\ \mathrm{m^2/s^2}$ and $U = 10$ m/s. Find $u_{rms}$ and $I_u$.

<details>
<summary>Answer</summary>

$\overline{u^2} = \overline{(U + u')^2} = U^2 + 2U\overline{u'} + \overline{u'^2} = U^2 + \overline{u'^2}$, using $\overline{u'} = 0$. Hence $\overline{u'^2} = 101.2 - 100 = 1.2\ \mathrm{m^2/s^2}$, $u_{rms} = \sqrt{1.2} = 1.095$ m/s and $I_u = 11.0\%$.

The example shows why variances must be computed from fluctuations in practice: a 1.2% error in $\overline{u^2}$ would completely change the answer.

</details>

**Exercise 2.** A CFD inlet is specified with turbulence intensity $I = 5\%$ at $U_{ref} = 20$ m/s. Find $k$, assuming isotropic turbulence. What value would you get by mistakenly using $k = \frac{1}{2}\overline{u'^2}$, i.e. only the streamwise component?

<details>
<summary>Answer</summary>

For isotropic turbulence, $\overline{u'^2} = \overline{v'^2} = \overline{w'^2} = (I U_{ref})^2 = (0.05 \times 20)^2 = 1\ \mathrm{m^2/s^2}$. Therefore $k = \frac{3}{2}(1) = 1.5\ \mathrm{m^2/s^2}$.

Using only one component gives $k = 0.5\ \mathrm{m^2/s^2}$, an underestimate by a factor of three. That error feeds directly into $\varepsilon$, $\omega$ and the eddy viscosity at the inlet.

</details>

**Exercise 3.** The mean flow in a plane channel is two-dimensional, and the statistics are invariant under the reflection $z \to -z$. Show that $\overline{u'w'} = \overline{v'w'} = 0$, so only four Reynolds stress components survive.

<details>
<summary>Answer</summary>

Under the reflection $z \to -z$, the components $u'$ and $v'$ are unchanged while $w' \to -w'$. Reflection invariance requires every statistic to take the same value in the reflected frame, so $\overline{u'w'} = \overline{u'(-w')} = -\overline{u'w'}$, which forces $\overline{u'w'} = 0$. The same argument gives $\overline{v'w'} = 0$.

The remaining components are $\overline{u'^2}$, $\overline{v'^2}$, $\overline{w'^2}$ and $\overline{u'v'}$.

</details>

**Exercise 4.** A velocity signal is $u(t) = U_0 + a\sin(2\pi f t)$ with $a = 0.5U_0$ and $f = 5$ Hz. Averaging runs over a window $[0, T]$. Using the worst case of the window error $a(1 - \cos\omega T)/(\omega T)$, find the smallest $T$ that guarantees the mean is within $0.1\%$ of $U_0$.

<details>
<summary>Answer</summary>

The error is bounded by $2a/(\omega T) = a/(\pi f T)$. Requiring $a/(\pi f T) \le 0.001\,U_0$ gives

$$
T \ge \frac{0.5}{\pi \times 5 \times 0.001} = 31.8\ \mathrm{s}
$$

That is about 160 periods. Random turbulent signals converge in a different way, governed by the integral time scale (see [Turbulence Statistics](./statistics.md)), but the lesson is the same: finite averages are only approximately Reynolds averages.

</details>

**Exercise 5.** A flow alternates between two states with equal probability: cold dense fluid ($\rho = 1.2\ \mathrm{kg/m^3}$, $u = 10$ m/s) and hot light fluid ($\rho = 0.4\ \mathrm{kg/m^3}$, $u = 20$ m/s). Compute $\overline{\rho}$, the Reynolds mean $\overline{u}$, the Favre mean $\tilde{u}$, $\overline{\rho' u'}$ and $\overline{u''}$. Check the relation $\overline{u''} = -\overline{\rho'u'}/\overline{\rho}$.

<details>
<summary>Answer</summary>

**Density and Reynolds mean.** $\overline{\rho} = \frac{1}{2}(1.2 + 0.4) = 0.8\ \mathrm{kg/m^3}$ and $\overline{u} = 15$ m/s.

**Favre mean.** $\overline{\rho u} = \frac{1}{2}(12 + 8) = 10\ \mathrm{kg/(m^2 s)}$, so $\tilde{u} = 10/0.8 = 12.5$ m/s.

**Correlation.** The fluctuations are $\rho' = \pm 0.4$ and $u' = \mp 5$, so $\overline{\rho'u'} = -2.0\ \mathrm{kg/(m^2 s)}$.

**Check.** $\overline{u''} = \overline{u} - \tilde{u} = 2.5$ m/s, and $-\overline{\rho'u'}/\overline{\rho} = 2.0/0.8 = 2.5$ m/s, as required.

The Favre mean is pulled toward the dense, slow state because it measures the mean *mass flux* per unit mean density.

</details>

## References

- Reynolds, O. "On the dynamical theory of incompressible viscous fluids and the determination of the criterion." *Philosophical Transactions of the Royal Society of London A*, 186, 123–164, 1895.
- Pope, S. B. *Turbulent Flows*. Cambridge University Press, 2000. (Chapters 3–4: statistical description and mean-flow equations.)
- Tennekes, H., and Lumley, J. L. *A First Course in Turbulence*. MIT Press, 1972.
- Wilcox, D. C. *Turbulence Modeling for CFD*, 3rd ed. DCW Industries, 2006. (Chapter 2 covers Reynolds and Favre averaging.)
