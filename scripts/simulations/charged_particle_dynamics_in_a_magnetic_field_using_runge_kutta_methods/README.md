# Charged Particle Dynamics in a Magnetic Field

This script simulates and animates the helical motion of a charged particle moving through a uniform magnetic field, using the 4th-order Runge-Kutta (RK4) method to integrate the equations of motion.

## Physics Background

A charged particle with charge $q$ and mass $m$ moving with velocity $\mathbf{v}$ in a magnetic field $\mathbf{B}$ experiences the **Lorentz force**:

$$\mathbf{F} = q\,(\mathbf{v} \times \mathbf{B})$$

This force is always perpendicular to the velocity, so it does no work and does not change the particle's speed — it only changes the direction of motion.

### Equations of Motion

The acceleration of the particle is:

$$\dot{\mathbf{v}} = \frac{q}{m}(\mathbf{v} \times \mathbf{B})$$

Combined with $\dot{\mathbf{r}} = \mathbf{v}$, this forms a system of 6 first-order ODEs:

$$\frac{d}{dt}\begin{pmatrix}\mathbf{r} \\ \mathbf{v}\end{pmatrix} = \begin{pmatrix}\mathbf{v} \\ \frac{q}{m}(\mathbf{v} \times \mathbf{B})\end{pmatrix}$$

### Helical Motion

For a uniform magnetic field $\mathbf{B} = B\hat{z}$, the particle undergoes **helical motion**:
- The velocity component perpendicular to $\mathbf{B}$ drives circular motion in the $xy$-plane with the **cyclotron (Larmor) radius**:
$$r_L = \frac{m v_\perp}{|q| B}$$
and **cyclotron frequency**:
$$\omega_c = \frac{|q| B}{m}$$
- The velocity component parallel to $\mathbf{B}$ ($v_z$) is unchanged, causing the particle to drift along the field direction.

## Numerical Method: Runge-Kutta 4th Order (RK4)

The RK4 method advances the state $\mathbf{y} = (\mathbf{r}, \mathbf{v})$ by a time step $\Delta t$:

$$\mathbf{y}^{n+1} = \mathbf{y}^n + \frac{\Delta t}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

where:
$$k_1 = f(t^n, \mathbf{y}^n), \quad k_2 = f\!\left(t^n + \frac{\Delta t}{2},\, \mathbf{y}^n + \frac{\Delta t}{2}k_1\right)$$
$$k_3 = f\!\left(t^n + \frac{\Delta t}{2},\, \mathbf{y}^n + \frac{\Delta t}{2}k_2\right), \quad k_4 = f(t^n + \Delta t,\, \mathbf{y}^n + \Delta t\,k_3)$$

RK4 provides fourth-order accuracy in $\Delta t$, giving excellent energy conservation for the cyclotron motion over long integration times.

## Simulation Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| $q$ | 1.0 | Particle charge |
| $m$ | 1.0 | Particle mass |
| $\mathbf{B}$ | $(0, 0, 1)$ | Uniform magnetic field along $z$ |
| $\mathbf{r}_0$ | $(0, 1, 0)$ | Initial position |
| $\mathbf{v}_0$ | $(1, 0, 1)$ | Initial velocity |
| $\Delta t$ | 0.01 | Time step |
| $t_f$ | 50.0 | Final time |

## Output

The script produces a 3D animation showing the particle's helical trajectory over time. The path is drawn progressively as the particle moves, illustrating the characteristic helical winding along the magnetic field direction.
