# Inertial Navigation Systems

An inertial navigation system (INS) computes position, velocity and attitude by integrating the outputs of accelerometers and gyroscopes from a known starting state. It needs no external signal, cannot be jammed, and runs at hundreds of hertz, which is why it is the core navigation sensor of airliners, submarines, missiles and launch vehicles, and why cars, drones and phones carry small MEMS versions of it. The price of autonomy is drift: every sensor error is integrated once or twice, so the errors grow with time unless an external reference such as GNSS corrects them. This note covers the sensors and their error models, strapdown and gimballed mechanizations, attitude representations, the navigation equations, the growth of navigation errors including the Schuler oscillation, and INS/GNSS fusion with a Kalman filter.

Inertial navigation is the mechanized form of dead reckoning, the old practice of advancing a known position by estimated speed, heading and elapsed time. It became practical with precision gyroscopes in the 1950s and 1960s; the Litton LN-3 of the F-104G Starfighter was among the first inertial navigators in a production fighter, and the Boeing 747 entered service with inertial navigation for oceanic flight.

## Problem Statement

Given the initial position $`\mathbf{p}_0`$, velocity $`\mathbf{v}_0`$ and attitude $`\mathbf{C}_{b,0}^n`$ of a vehicle, and the outputs of a triad of accelerometers (specific force $`\tilde{\mathbf{f}}^b`$) and a triad of gyroscopes (angular rate $`\tilde{\boldsymbol\omega}_{ib}^b`$) rigidly mounted in the body frame $b$, find the position $\mathbf{p}(t)$, velocity $\mathbf{v}^n(t)$ and attitude $\mathbf{C}_b^n(t)$ in a navigation frame $n$, together with an estimate of their errors. The sensors have biases, scale-factor errors and noise. When aiding measurements are available (GNSS position, barometric height), they are fused with the inertial solution to bound the errors and to estimate the sensor errors.

The governing equations are the rigid-body kinematics of the attitude and the navigation equations

```math
\dot{\mathbf{C}}_b^n = \mathbf{C}_b^n\,[\boldsymbol\omega_{nb}^b\times],
\qquad
\dot{\mathbf{v}}^n = \mathbf{C}_b^n\mathbf{f}^b + \mathbf{g}^n - (2\boldsymbol\Omega_{ie}^n + \boldsymbol\omega_{en}^n)\times\mathbf{v}^n,
\qquad
\dot{\mathbf{p}} = \mathbf{v}^n
```

where $[\boldsymbol\omega\times]$ is the skew-symmetric matrix of $\boldsymbol\omega$, $\mathbf{g}^n$ is gravity, $\boldsymbol\Omega_{ie}$ is the Earth rotation rate and $\boldsymbol\omega_{en}$ the transport rate of the navigation frame over the curved Earth. The position equation is written in Cartesian form here; on the real Earth it is expressed in latitude, longitude and height.

## Inertial Sensors

### Accelerometers and Specific Force

An accelerometer measures the force per unit mass that its case exerts on a proof mass, the **specific force**

$$
\mathbf{f} = \mathbf{a} - \mathbf{g}
$$

where $\mathbf{a}$ is the acceleration relative to inertial space and $\mathbf{g}$ the gravitational acceleration. An accelerometer at rest on a table reads $9.81$ m/s² upward; in free fall it reads zero. Gravitation and acceleration cannot be separated by any local measurement, so the INS must add a gravity model back in, and an error in that model enters the velocity directly.

Navigation accelerometers are pendulous force-rebalance devices, in which a servo holds a hinged proof mass at null and the restoring current measures the force, or vibrating-beam devices whose resonant frequency changes with axial load. MEMS accelerometers are etched silicon proof masses on flexures with capacitive pick-offs.

### Gyroscopes

A gyroscope measures angular rate relative to inertial space. Three principles dominate:

| Type | Principle | Typical use |
| --- | --- | --- |
| spinning-mass (mechanical) | the angular momentum of a rotor resists changes of direction; the precession torque or deflection measures rate | older gimballed platforms, some high-end strategic systems |
| ring-laser gyro (RLG) | two laser beams travel in opposite directions round a closed cavity; rotation shortens one path and lengthens the other (Sagnac effect), and the beat frequency $\Delta f = 4A\Omega/(\lambda L)$ is proportional to the rate $\Omega$ | navigation-grade strapdown systems in airliners and military aircraft |
| fibre-optic gyro (FOG) | the Sagnac phase shift $\Delta\phi = 8\pi N A\Omega/(\lambda c)$ between counter-propagating light in a coil of $N$ turns enclosing area $A$ | tactical and navigation grade, ships, spacecraft |
| MEMS vibratory gyro | a vibrating proof mass in a rotating frame feels a Coriolis force $-2m\boldsymbol\Omega\times\mathbf{v}$ that excites a second vibration mode | consumer, automotive and tactical grade |

Here $A$ is the enclosed area, $L$ the cavity perimeter, $\lambda$ the wavelength and $c$ the speed of light. A ring-laser gyro has no output at very low rates because backscatter locks the two beams to one frequency; it is mechanically dithered to stay out of this lock-in band.

### Error Models

The output of one sensor axis is modelled as

```math
\tilde{f} = (1 + s)\, f + b + \mathbf{m}\cdot\mathbf{f}_\perp + n
```

with scale-factor error $s$, bias $b$, cross-axis (misalignment) coefficients $\mathbf{m}$ acting on the orthogonal components $\mathbf{f}_\perp$, and noise $n$; the gyro model is the same with $\omega$ in place of $f$. The terms behave differently:

| Error | Description | Effect after integration |
| --- | --- | --- |
| bias | constant offset; differs from turn-on to turn-on (repeatability) and drifts slowly in a run (in-run stability) | accelerometer: position error $\propto t^2$; gyro: attitude error $\propto t$, position error $\propto t^3$ |
| scale factor | output proportional to the true input with gain error $s$, usually quoted in ppm | error proportional to the manoeuvre, zero when the input is zero |
| misalignment | sensitive axis not exactly along the body axis | couples motion about one axis into another |
| white noise | velocity random walk (VRW) $N$ in m/s/√h for accelerometers; angle random walk (ARW) in °/√h for gyros | random walk of velocity or angle, standard deviation $\propto \sqrt{t}$ |
| bias instability | low-frequency $1/f$ wander of the bias, the floor of the Allan deviation curve | limits how well the bias can be calibrated in flight |

The Allan deviation $\sigma(\tau)$ of a recording at rest separates these processes by averaging time $\tau$: white noise gives a slope of $-\tfrac{1}{2}$, bias instability the flat minimum, and rate random walk a slope of $+\tfrac{1}{2}$.

Sensor quality spans many orders of magnitude, which sets what an INS can do on its own. Approximate figures for in-run bias are:

| Grade | Gyro bias | Accelerometer bias | Unaided position error |
| --- | --- | --- | --- |
| navigation (RLG, FOG) | about $0.01^\circ$/h | 30–100 μg | of order 1 nautical mile per hour |
| tactical (FOG, high-end MEMS) | 1–10 °/h | 0.1–1 mg | kilometres within ten minutes |
| consumer and automotive MEMS | 10–1000 °/h | 1–10 mg | useful only for seconds without aiding |

Here 1 μg = $9.81 \times 10^{-6}$ m/s². The Earth rotates at $15.04^\circ$/h, so only navigation-grade gyros can sense it well enough to find north.

## Gimballed and Strapdown Systems

A **gimballed** (stable-platform) INS mounts the sensors on a platform held in a chosen orientation, usually local level and north-pointing, by a set of gimbals driven from the gyro outputs. The accelerometers then measure navigation-frame specific force directly, and the attitude is read from the gimbal angles. A **strapdown** INS fixes the sensors to the vehicle and replaces the platform with computation: the gyro outputs are integrated to keep the attitude matrix $\mathbf{C}_b^n$, which resolves the body-frame specific force into the navigation frame.

| Aspect | Gimballed | Strapdown |
| --- | --- | --- |
| sensors see | platform motion, small rates | full vehicle rates, up to hundreds of °/s |
| attitude from | gimbal angle pickoffs | numerical integration of the gyro outputs |
| hardware | gimbals, torque motors, slip rings; large and costly to maintain | no moving parts besides dither; small, reliable |
| computation | light | attitude update at hundreds of hertz, coning and sculling corrections |
| sensor requirements | moderate dynamic range | large dynamic range and good scale-factor stability |

Since the 1980s nearly all new systems are strapdown, made possible by ring-laser and fibre-optic gyros, which tolerate high rates, and by fast navigation computers.

## Attitude Representation

### Rotation Matrices

The direction cosine matrix $\mathbf{C}_b^n$ transforms a vector from body to navigation axes, $\mathbf{x}^n = \mathbf{C}_b^n\mathbf{x}^b$. It is orthogonal, $(\mathbf{C}_b^n)^{-1} = (\mathbf{C}_b^n)^T = \mathbf{C}_n^b$, and evolves as

```math
\dot{\mathbf{C}}_b^n = \mathbf{C}_b^n\,[\boldsymbol\omega_{nb}^b\times],
\qquad
[\boldsymbol\omega\times] = \begin{bmatrix} 0 & -\omega_z & \omega_y \\ \omega_z & 0 & -\omega_x \\ -\omega_y & \omega_x & 0 \end{bmatrix}
```

where $`\boldsymbol\omega_{nb}^b = \boldsymbol\omega_{ib}^b - \mathbf{C}_n^b\boldsymbol\omega_{in}^n`$ is the body rate relative to the navigation frame: the gyro output minus the rotation of the navigation frame itself ($\boldsymbol\omega_{in} = \boldsymbol\Omega_{ie} + \boldsymbol\omega_{en}$). Nine numbers describe three degrees of freedom, and numerical integration slowly destroys orthogonality, so the matrix is re-orthonormalized periodically.

### Euler Angles and Gimbal Lock

Roll $\phi$, pitch $\theta$ and yaw $\psi$ describe the attitude as three successive rotations, $\mathbf{C}_b^n = \mathbf{R}_z(\psi)\mathbf{R}_y(\theta)\mathbf{R}_x(\phi)$ for a north-east-down navigation frame. With body rates $(p, q, r)$ the angles obey

$$
\dot\phi = p + (q\sin\phi + r\cos\phi)\tan\theta,
\qquad \dot\theta = q\cos\phi - r\sin\phi,
\qquad \dot\psi = \frac{q\sin\phi + r\cos\phi}{\cos\theta}
$$

At $\theta = \pm 90^\circ$ the roll and yaw axes coincide, $\tan\theta$ and $1/\cos\theta$ are infinite and one degree of freedom is lost. This is **gimbal lock**, the same singularity that a three-gimbal platform suffers mechanically when two gimbal axes align. Euler angles are convenient for display and for small-angle analysis but are not used to propagate the attitude of a vehicle that can reach vertical attitudes.

### Quaternions

A rotation by angle $\alpha$ about the unit axis $\mathbf{e}$ is the unit quaternion

$$
\mathbf{q} = \left(\cos\tfrac{\alpha}{2},\ \mathbf{e}\sin\tfrac{\alpha}{2}\right) = (q_0, q_1, q_2, q_3),
\qquad \lVert\mathbf{q}\rVert = 1
$$

Four parameters with one constraint describe the attitude without singularities. The kinematic equation is

```math
\dot{\mathbf{q}}_b^n = \tfrac{1}{2}\,\mathbf{q}_b^n \otimes \begin{bmatrix} 0 \\ \boldsymbol\omega_{nb}^b \end{bmatrix}
```

where $\otimes$ is the quaternion product, $(a_0, \mathbf{a})\otimes(b_0, \mathbf{b}) = (a_0b_0 - \mathbf{a}\cdot\mathbf{b},\ a_0\mathbf{b} + b_0\mathbf{a} + \mathbf{a}\times\mathbf{b})$. If the rate is constant over a step $\Delta t$, the exact update is a multiplication by the quaternion of the rotation vector $\boldsymbol\sigma = \boldsymbol\omega\Delta t$:

```math
\mathbf{q}_{k+1} = \mathbf{q}_k \otimes \left(\cos\frac{\lVert\boldsymbol\sigma\rVert}{2},\ \frac{\boldsymbol\sigma}{\lVert\boldsymbol\sigma\rVert}\sin\frac{\lVert\boldsymbol\sigma\rVert}{2}\right)
```

followed by renormalization. In a real strapdown computer the rotation vector is built from several gyro samples per step with a coning correction, because rates that rotate in direction do not commute. The direction cosine matrix follows from the quaternion as

```math
\mathbf{C}_b^n = \begin{bmatrix}
q_0^2 + q_1^2 - q_2^2 - q_3^2 & 2(q_1q_2 - q_0q_3) & 2(q_1q_3 + q_0q_2) \\
2(q_1q_2 + q_0q_3) & q_0^2 - q_1^2 + q_2^2 - q_3^2 & 2(q_2q_3 - q_0q_1) \\
2(q_1q_3 - q_0q_2) & 2(q_2q_3 + q_0q_1) & q_0^2 - q_1^2 - q_2^2 + q_3^2
\end{bmatrix}
```

## Navigation Equations

### Local-Level Frame

In the north-east-down frame at latitude $\varphi$, longitude $\lambda$ and height $h$, the velocity and position equations are

```math
\dot{\mathbf{v}}^n = \mathbf{C}_b^n\mathbf{f}^b + \mathbf{g}^n - (2\boldsymbol\Omega_{ie}^n + \boldsymbol\omega_{en}^n)\times\mathbf{v}^n,
\qquad
\dot\varphi = \frac{v_N}{R_N + h},
\quad
\dot\lambda = \frac{v_E}{(R_E + h)\cos\varphi},
\quad
\dot h = -v_D
```

with Earth rate $\boldsymbol\Omega_{ie}^n = \Omega(\cos\varphi, 0, -\sin\varphi)$, $\Omega = 7.292 \times 10^{-5}$ rad/s, transport rate $\boldsymbol\omega_{en}^n = (\dot\lambda\cos\varphi, -\dot\varphi, -\dot\lambda\sin\varphi)$, and meridian and transverse radii of curvature $R_N$ and $R_E$. The term $2\boldsymbol\Omega_{ie}\times\mathbf{v}$ is the Coriolis acceleration, and $\mathbf{g}^n$ is the local gravity: gravitation plus the centrifugal acceleration of the rotating Earth. A simple model is

```math
g \approx 9.780\left(1 + 5.3 \times 10^{-3}\sin^2\varphi\right) - 3.09 \times 10^{-6}\,h \quad \mathrm{m/s^2}
```

with $h$ in metres; the second term is the free-air gradient $2g/R$.

### Simplified Flat-Earth Form

Over short times, for low-grade sensors, or in a simulation that isolates sensor errors, the navigation frame is taken as fixed and flat:

```math
\dot{\mathbf{C}}_b^n = \mathbf{C}_b^n\,[\boldsymbol\omega_{ib}^b\times],
\qquad
\dot{\mathbf{v}}^n = \mathbf{C}_b^n\mathbf{f}^b + \mathbf{g},
\qquad
\dot{\mathbf{p}}^n = \mathbf{v}^n
```

with constant $\mathbf{g}$. This form omits

- Earth rotation: the gyros sense the Earth's $15.04^\circ$/h, which must be removed from the attitude update, and the Coriolis term $2\boldsymbol\Omega_{ie}\times\mathbf{v}$ (0.026 m/s² at 250 m/s and $45^\circ$ latitude, see Exercise 4);
- transport rate: the rotation of the local vertical as the vehicle moves over the curved Earth, $\lvert\boldsymbol\omega_{en}\rvert \approx V/R$, which is also what produces the Schuler loop below;
- the gravity model: the variation of $g$ with latitude and height and the deflection of the vertical;
- curvature of position: latitude and longitude rather than Cartesian distance.

The flat-Earth form is adequate when these terms are smaller than the sensor errors, for example for a MEMS IMU whose gyro bias exceeds Earth rate. It is not adequate for a navigation-grade system or for flights longer than a few minutes.

### Initial Alignment

Before navigating, the INS must know its attitude. At rest the accelerometers measure $\mathbf{f}^b = -\mathbf{C}_n^b\mathbf{g}^n$, which fixes roll and pitch (levelling). In the levelled frame the gyros measure the horizontal component of Earth rate, $\Omega\cos\varphi$, which points north, so the heading follows from the ratio of the two horizontal gyro outputs (gyrocompassing). A gyro bias $\varepsilon$ gives a heading error of about $\varepsilon/(\Omega\cos\varphi)$, so gyrocompassing needs gyros far better than Earth rate. Lower-grade systems take heading from a magnetometer, from GNSS velocity during motion, or from a transfer alignment to a better INS.

## Error Growth

### Single-Channel Error Equations

Consider one horizontal channel of a level INS at rest or in straight flight. Let $\delta v$ be the velocity error, $\delta\theta$ the tilt error of the computed frame, $b$ the accelerometer bias and $\varepsilon$ the gyro bias about the horizontal axis normal to the channel. A tilt $\delta\theta$ resolves a component $`g\,\delta\theta`$ of the gravity reaction into the horizontal channel, so

```math
\delta\dot v = b - g\,\delta\theta, \qquad \delta\dot\theta = \varepsilon + \frac{\delta v}{R}
```

The last term is the transport-rate feedback: a velocity error makes the INS rotate its local-level frame at the wrong rate $\delta v/R$.

### Flat-Earth Growth

Without the feedback term ($R \to \infty$) the errors are pure integrals:

| Error source | Position error |
| --- | --- |
| accelerometer bias $b$ | $\delta x = \tfrac{1}{2}bt^2$ |
| gyro bias $\varepsilon$ | $\delta x = \tfrac{1}{6}g\varepsilon t^3$ |
| velocity random walk $N$ | standard deviation $N\sqrt{t^3/3}$ |
| angle random walk $N_\theta$ | standard deviation $gN_\theta\sqrt{t^5/20}$ |
| initial tilt $\delta\theta_0$ | $`\delta x = \tfrac{1}{2}g\,\delta\theta_0\,t^2`$ |

The gyro term overtakes the accelerometer term after $t = 3b/(g\varepsilon)$, about 53 minutes for a navigation-grade IMU with $b = 50$ μg and $\varepsilon = 0.01^\circ$/h, and about 2 minutes for a tactical IMU with 1 mg and $10^\circ$/h. In the long run gyros decide the quality of an INS.

### Schuler Oscillation

With the feedback term, eliminating $\delta\theta$ gives

```math
\delta\ddot x + \omega_s^2\,\delta x = b - g\varepsilon t + \ldots,
\qquad \omega_s = \sqrt{\frac{g}{R}}
```

an undamped oscillator with the **Schuler period**

$$
T_s = 2\pi \sqrt{\frac{R}{g}} = 84.4\ \mathrm{min}
$$

This is the period of a pendulum as long as the Earth's radius, and of a satellite in an orbit skimming the surface. Schuler (1923) showed that a device with this period stays vertical however the vehicle accelerates; an INS has it automatically because its frame follows the computed position. For constant biases

```math
\delta x_b = \frac{b}{\omega_s^2}\left(1 - \cos\omega_s t\right), \qquad
\delta x_\varepsilon = -R\varepsilon\left(t - \frac{\sin\omega_s t}{\omega_s}\right)
```

The accelerometer-bias error is bounded by $2bR/g$ (650 m for 50 μg) and returns to zero every 84.4 min; in steady state the tilt settles at $\delta\theta = b/g$, which exactly cancels the bias, so a stationary INS cannot tell a tilt from an accelerometer bias. The gyro-bias error grows linearly at $R\varepsilon$, which for $0.01^\circ$/h is 0.31 m/s, about 1.1 km/h. This is the origin of the "nautical mile per hour" rating of navigation-grade systems. Over many hours, Earth rate couples the north and east channels and adds a 24-hour oscillation and a Foucault modulation of the Schuler oscillation.

![Error growth of a stationary strapdown INS](../../../../scripts/algorithms/ins_dead_reckoning_errors/ins_error_growth.png)

Panel (a) shows a simulated stationary INS following the $\tfrac{1}{2}bt^2$ and $\tfrac{1}{6}g\varepsilon t^3$ laws exactly; panel (b) shows the same biases with the Schuler loop closed, where the accelerometer error oscillates and the gyro error grows only linearly; panel (c) shows the random-walk error of 400 noisy runs following $N\sqrt{t^3/3}$.

### Vertical Channel

The vertical channel has no Schuler loop. Gravity decreases with height at $2g/R$, so a height error $\delta h$ makes the computed gravity too small and the computed upward acceleration too large: $`\delta\ddot h = (2g/R)\,\delta h`$, which diverges with time constant $\sqrt{R/(2g)} \approx 570$ s. Every INS therefore aids its vertical channel with barometric altitude or GNSS height.

## INS/GNSS Integration

GNSS gives position errors of a few metres that do not grow with time, but at 1 to 10 Hz, with outages, and with no attitude. An INS gives smooth, high-rate position, velocity and attitude whose errors grow. Combining them with a Kalman filter gives the best of both: GNSS bounds the drift, and the INS bridges outages and fills in between fixes. In a **loosely coupled** system the filter uses the position and velocity solution of the GNSS receiver; in a **tightly coupled** system it uses the pseudoranges and range rates directly, which still helps when fewer than four satellites are visible.

### Error-State Kalman Filter

The filter estimates the errors of the INS, not the navigation state itself. The error state contains position, velocity and attitude errors and the sensor biases, for example

$$
\delta\mathbf{x} = \left[\delta\mathbf{p},\ \delta\mathbf{v},\ \delta\boldsymbol\psi,\ \mathbf{b}_a,\ \mathbf{b}_g\right]
$$

and obeys the linearized error dynamics $`\delta\dot{\mathbf{x}} = \mathbf{F}\,\delta\mathbf{x} + \mathbf{G}\mathbf{w}`$. In the flat-Earth form

```math
\delta\dot{\mathbf{p}} = \delta\mathbf{v},
\qquad
\delta\dot{\mathbf{v}} = -[\mathbf{f}^n\times]\,\delta\boldsymbol\psi + \mathbf{C}_b^n\mathbf{b}_a + \mathbf{w}_a,
\qquad
\delta\dot{\boldsymbol\psi} = \mathbf{C}_b^n\mathbf{b}_g + \mathbf{w}_g,
\qquad
\dot{\mathbf{b}}_a = \mathbf{w}_{ba},
\quad
\dot{\mathbf{b}}_g = \mathbf{w}_{bg}
```

with $\delta\boldsymbol\psi$ the small attitude error angles, defined by $\hat{\mathbf{C}}_b^n = (\mathbf{I} + [\delta\boldsymbol\psi\times])\mathbf{C}_b^n$, and $\mathbf{w}$ white noises; Earth-rate and transport-rate terms are omitted. The term $`-[\mathbf{f}^n\times]\,\delta\boldsymbol\psi`$ is how an attitude error becomes a velocity error: during straight and level flight $\mathbf{f}^n$ is the gravity reaction and only the tilts are observable, while manoeuvres make heading observable too.

Over a step $\Delta t$ the filter propagates with the transition matrix $\boldsymbol\Phi_k \approx \mathbf{I} + \mathbf{F}\Delta t$ and process noise $\mathbf{Q}_k$:

```math
\delta\hat{\mathbf{x}}_k^- = \boldsymbol\Phi_{k-1}\,\delta\hat{\mathbf{x}}_{k-1}^+,
\qquad
\mathbf{P}_k^- = \boldsymbol\Phi_{k-1}\mathbf{P}_{k-1}^+\boldsymbol\Phi_{k-1}^T + \mathbf{Q}_{k-1}
```

At a GNSS fix the measurement is the difference between the INS and GNSS positions, $`\mathbf{z}_k = \mathbf{p}_{INS} - \mathbf{p}_{GNSS} = \mathbf{H}\,\delta\mathbf{x}_k + \mathbf{v}_k`$ with $\mathbf{H} = [\mathbf{I}\ \ \mathbf{0}]$ and measurement covariance $\mathbf{R}_k$, and the update is

```math
\mathbf{K}_k = \mathbf{P}_k^-\mathbf{H}^T\left(\mathbf{H}\mathbf{P}_k^-\mathbf{H}^T + \mathbf{R}_k\right)^{-1},
\qquad
\delta\hat{\mathbf{x}}_k^+ = \delta\hat{\mathbf{x}}_k^- + \mathbf{K}_k\left(\mathbf{z}_k - \mathbf{H}\,\delta\hat{\mathbf{x}}_k^-\right),
\qquad
\mathbf{P}_k^+ = (\mathbf{I} - \mathbf{K}_k\mathbf{H})\,\mathbf{P}_k^-
```

The Joseph form $\mathbf{P}^+ = (\mathbf{I} - \mathbf{K}\mathbf{H})\mathbf{P}^-(\mathbf{I} - \mathbf{K}\mathbf{H})^T + \mathbf{K}\mathbf{R}\mathbf{K}^T$ keeps $\mathbf{P}$ symmetric and positive definite in finite precision. In the usual closed-loop arrangement the estimated errors are subtracted from the INS solution and the bias estimates are applied to later sensor outputs, after which the error state is reset to zero. The filter therefore also calibrates the IMU in flight, which is what makes the INS useful during a GNSS outage.

### Worked Example

The script [INS Dead-Reckoning Errors](../../../../scripts/algorithms/ins_dead_reckoning_errors/) flies a 10-minute climb, cruise and descent in a vertical plane with a MEMS-grade IMU (accelerometer biases 0.02 and −0.015 m/s², gyro bias $10^\circ$/h, plus noise). Unaided, the position error is 26 m after 1 min and 16.5 km after 10 min, dominated by the $t^3$ gyro term. An 8-state error-state Kalman filter with 1 Hz GNSS fixes ($\sigma$ = 3 m along-track, 5 m vertical) keeps the RMS error at 1.9 m; during a 60 s GNSS outage the error rises only to 3.4 m because the filter has already estimated the biases.

![INS-only and INS/GNSS trajectories and errors](../../../../scripts/algorithms/ins_dead_reckoning_errors/ins_gnss_fusion.png)

Panel (a) compares the trajectories, panel (b) the position errors with the filter's $3\sigma$ bound, which widens during the shaded outage and collapses at the first fix, and panel (c) the gyro bias estimate.

## Key Takeaways

- Accelerometers measure specific force $\mathbf{f} = \mathbf{a} - \mathbf{g}$; the INS must add gravity back from a model.
- Strapdown systems replace the stable platform by integrating the gyro outputs into a rotation matrix or quaternion; quaternions avoid the gimbal lock of Euler angles.
- Without aiding, an accelerometer bias gives $\tfrac{1}{2}bt^2$ and a gyro bias $\tfrac{1}{6}g\varepsilon t^3$; gyros dominate long-term performance.
- The transport-rate feedback of a real INS turns the horizontal errors into an 84.4-minute Schuler oscillation; the vertical channel is unstable and needs aiding.
- An error-state Kalman filter fusing GNSS bounds the errors and estimates the sensor biases, so the INS can bridge GNSS outages.

## Related Scripts

- [INS Dead-Reckoning Errors](../../../../scripts/algorithms/ins_dead_reckoning_errors/): simulates a two-dimensional strapdown inertial navigation system and shows how accelerometer bias, gyro bias and sensor noise turn into position error, and how a Kalman filter that fuses GNSS fixes keeps that error bounded.

## Exercises

**Exercise 1.** Compute the Schuler period from $T_s = 2\pi\sqrt{R/g}$ with $R = 6371$ km and $g = 9.81$ m/s². What physical systems have this period?

<details>
<summary>Answer</summary>

```math
T_s = 2\pi\sqrt{\frac{6.371 \times 10^6}{9.81}} = 5063\ \mathrm{s} = 84.4\ \mathrm{min}
```

It is the period of a pendulum whose length equals the Earth's radius, and the orbital period of a satellite skimming the surface. A platform or computed frame with this period stays level as the vehicle moves over the curved Earth.

</details>

**Exercise 2.** A horizontal accelerometer has an uncompensated bias of $b = 1 \times 10^{-3}$ m/s² (about 100 μg). (a) Treating the error as a simple double integration, find the position error after 1 min, 10 min and 1 h. (b) With the Schuler loop the error follows $\delta x = (b/\omega_s^2)(1 - \cos\omega_s t)$. What is its maximum, and when is it reached?

<details>
<summary>Answer</summary>

(a) $\delta x = \tfrac{1}{2}bt^2$ gives 1.8 m after 1 min, 180 m after 10 min and 6.48 km after 1 h.

(b) $\omega_s = \sqrt{g/R} = 1.24 \times 10^{-3}$ rad/s and

```math
\delta x_{max} = \frac{2b}{\omega_s^2} = \frac{2bR}{g} = \frac{2 \times 10^{-3} \times 6.371 \times 10^6}{9.81} = 1.30\ \mathrm{km}
```

reached after half a Schuler period, 42 min. The Schuler loop bounds the error caused by an accelerometer bias.

</details>

**Exercise 3.** Use $\mathbf{f} = \mathbf{a} - \mathbf{g}$, with a north-east-down navigation frame in which $\mathbf{g} = (0, 0, +9.81)$ m/s², to find the specific force measured by an ideal accelerometer triad (a) at rest on a runway, ignoring Earth rotation, and (b) in free fall. What does the result imply for the INS?

<details>
<summary>Answer</summary>

(a) $\mathbf{a} = 0$, so $\mathbf{f} = (0, 0, -9.81)$ m/s²: the accelerometers read 9.81 m/s² upward, the reaction of the runway.

(b) In free fall $\mathbf{a} = \mathbf{g}$, so $\mathbf{f} = 0$.

Accelerometers cannot distinguish gravitation from acceleration. The INS must add a gravity model back in, and errors in that model feed straight into the velocity. A tilt of the computed frame by $\delta\theta$ misresolves the 9.81 m/s² reaction and produces a horizontal error of $`g\,\delta\theta`$, which is $8.6 \times 10^{-3}$ m/s² for a tilt of only $0.05^\circ$.

</details>

**Exercise 4.** An aircraft flies north at 250 m/s at latitude $45^\circ$. Using $\Omega = 7.292 \times 10^{-5}$ rad/s, find the magnitude of the Coriolis term $2\boldsymbol\Omega_{ie} \times \mathbf{v}$. What position error would ignoring it produce after 10 minutes, treating it as a constant acceleration?

<details>
<summary>Answer</summary>

In NED, $\boldsymbol\Omega_{ie} = \Omega(\cos\varphi, 0, -\sin\varphi)$ and $\mathbf{v} = (250, 0, 0)$ m/s. The north component of Earth rate is parallel to the velocity, so only the vertical component contributes, giving an east-west acceleration of

```math
\lvert 2\boldsymbol\Omega_{ie} \times \mathbf{v} \rvert = 2 \times 7.292 \times 10^{-5} \times 250 \times \sin 45^\circ = 0.0258\ \mathrm{m/s^2}
```

```math
\delta x = \tfrac{1}{2}(0.0258)(600)^2 = 4.6\ \mathrm{km}
```

The term is small compared with $g$ but 25 to 85 times the bias of a navigation-grade accelerometer, so it must be included in the velocity update.

</details>

**Exercise 5.** A navigation-grade INS has a residual gyro bias of $\varepsilon = 0.01^\circ$/h about a horizontal axis. (a) Find the position error after 1 h predicted by the flat-Earth law and by the Schuler-loop solution. (b) What long-term error rate does the Schuler solution give? (c) Estimate the heading error of a gyrocompass alignment with this gyro at latitude $45^\circ$.

<details>
<summary>Answer</summary>

$\varepsilon = 0.01 \times \pi/180/3600 = 4.85 \times 10^{-8}$ rad/s and $\omega_s = 1.241 \times 10^{-3}$ rad/s.

(a) Flat Earth: $\tfrac{1}{6}g\varepsilon t^3 = \tfrac{1}{6} \times 9.81 \times 4.85 \times 10^{-8} \times 3600^3 = 3.70$ km. Schuler loop:

```math
R\varepsilon\left(t - \frac{\sin\omega_s t}{\omega_s}\right) = 0.309 \times \left(3600 - \frac{\sin 4.47}{1.241 \times 10^{-3}}\right) = 1.35\ \mathrm{km}
```

(b) $R\varepsilon = 6.371 \times 10^6 \times 4.85 \times 10^{-8} = 0.31$ m/s, about 1.1 km/h or 0.6 nautical miles per hour.

(c) The horizontal Earth rate is $\Omega\cos 45^\circ = 5.16 \times 10^{-5}$ rad/s, so the heading error is $\varepsilon/(\Omega\cos\varphi) = 9.4 \times 10^{-4}$ rad $= 0.054^\circ$. A MEMS gyro with a bias of $10^\circ$/h exceeds the $10.6^\circ$/h horizontal Earth rate and cannot gyrocompass at all.

</details>

## References

- Titterton, D. H., and Weston, J. L., *Strapdown Inertial Navigation Technology*, 2nd ed., Institution of Electrical Engineers, 2004.
- Groves, P. D., *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2nd ed., Artech House, 2013.
- Britting, K. R., *Inertial Navigation Systems Analysis*, Wiley-Interscience, 1971.
- Farrell, J. A., *Aided Navigation: GPS with High Rate Sensors*, McGraw-Hill, 2008.
- Savage, P. G., "Strapdown Inertial Navigation Integration Algorithm Design, Part 1: Attitude Algorithms," *Journal of Guidance, Control, and Dynamics*, 21(1), 19–28, 1998.
- Brown, R. G., and Hwang, P. Y. C., *Introduction to Random Signals and Applied Kalman Filtering*, 4th ed., Wiley, 2012.
