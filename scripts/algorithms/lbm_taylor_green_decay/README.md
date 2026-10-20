# LBM Taylor–Green Decay

This script measures the viscosity of the D2Q9 BGK lattice Boltzmann scheme from the decay of a Taylor–Green vortex and compares it with $\nu = c_s^2(\tau - 1/2)$. The vortex is an exact solution of the Navier–Stokes equations whose kinetic energy decays as $\exp(-4\nu k^2 t)$, so a fit of the simulated energy history gives the viscosity that the scheme actually produces. The figure shows that the measured values follow $c_s^2(\tau - 1/2)$, not the unshifted kinetic value $c_s^2\tau$, and that the remaining discrepancy falls as $1/N^2$.

## Overview

- Initialises a Taylor–Green vortex of wavenumber $k = 2\pi/N$ and amplitude $u_0 = 0.005$ (Mach number 0.0087) on a doubly periodic $N \times N$ lattice, with the matching pressure field carried by the density.
- Advances it with BGK collisions and periodic streaming (`np.roll`) until the predicted energy has fallen by $e^{-2}$.
- Fits $\ln E(t)$ by least squares over the last 80% of the run and converts the slope to a measured viscosity $\nu_m$.
- Repeats this for nine relaxation times between 0.51 and 2 on a $32 \times 32$ lattice.
- Repeats it for $N = 16, 32, 64, 128$ at $\tau = 1$ and $\tau = 1.5$ to measure the convergence of $\nu_m$.
- Records the total mass at every step; it is conserved to round-off.

## Mathematical Background

### Taylor–Green Vortex

On a periodic square of side $N$ the velocity and pressure

```math
u = -u_0 \cos(kx)\sin(ky)\,e^{-2\nu k^2 t}, \qquad v = u_0 \sin(kx)\cos(ky)\,e^{-2\nu k^2 t}, \qquad p = p_0 - \frac{\rho_0 u_0^2}{4}\left[\cos(2kx) + \cos(2ky)\right]e^{-4\nu k^2 t}
```

solve the incompressible Navier–Stokes equations exactly: the nonlinear term is balanced by the pressure gradient, and viscosity alone makes the vortex decay. The mean kinetic energy is $`E(t) = E_0\,e^{-4\nu k^2 t}`$, so

```math
\nu_m = -\frac{1}{4k^2}\frac{d \ln E}{dt}
```

The initial density is $\rho = 1 + (p - p_0)/c_s^2$ with $c_s^2 = 1/3$, and the populations start at equilibrium.

### Expected Viscosity

The Chapman–Enskog analysis of the lattice Boltzmann equation gives $\nu = c_s^2(\tau - 1/2)$ in lattice units. The $-1/2$ comes from the second-order term of the streaming step (or equivalently from the trapezoidal integration of the collision term) and is absent from the continuous BGK result $\nu = c_s^2\tau$. The measured viscosity also contains a discretisation error that depends on $k$, and a compressibility error of order $\mathrm{Ma}^2$, kept small here by the low amplitude.

## Implementation

- `equilibrium(rho, u)` and `moments(f)` evaluate the D2Q9 equilibrium and the density and velocity.
- `taylor_green_initial(n, u0)` returns the initial density and velocity fields.
- `collide_and_stream(f, tau)` performs one BGK step.
- `run_decay(n, tau)` runs one vortex and returns the time steps, the energy history and the total mass.
- `measured_viscosity(n, tau)` fits the energy decay from `FIT_START` onwards.
- `make_figure` draws the four panels. `GRID`, `TAUS`, `CURVE_TAUS`, `RESOLUTIONS`, `RESOLUTION_TAUS`, `U0` and `ENERGY_DROP` set the studies.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save lbm_taylor_green_decay.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script runs in about 5 s and prints:

```text
N = 32, u0 = 0.005:
  tau =  0.51: nu predicted 0.00333, measured 0.00333 (-0.00%), c_s^2 tau = 0.17000
  tau =  0.55: nu predicted 0.01667, measured 0.01667 (+0.00%), c_s^2 tau = 0.18333
  tau =  0.60: nu predicted 0.03333, measured 0.03334 (+0.01%), c_s^2 tau = 0.20000
  tau =  0.70: nu predicted 0.06667, measured 0.06670 (+0.05%), c_s^2 tau = 0.23333
  tau =  0.80: nu predicted 0.10000, measured 0.10012 (+0.12%), c_s^2 tau = 0.26667
  tau =  1.00: nu predicted 0.16667, measured 0.16720 (+0.32%), c_s^2 tau = 0.33333
  tau =  1.25: nu predicted 0.25000, measured 0.25182 (+0.73%), c_s^2 tau = 0.41667
  tau =  1.50: nu predicted 0.33333, measured 0.33768 (+1.31%), c_s^2 tau = 0.50000
  tau =  2.00: nu predicted 0.50000, measured 0.51447 (+2.89%), c_s^2 tau = 0.66667
tau = 1: relative viscosity error for N = (16, 32, 64, 128): 1.31e-02, 3.22e-03, 7.98e-04, 1.95e-04
tau = 1.5: relative viscosity error for N = (16, 32, 64, 128): 4.66e-02, 1.31e-02, 3.22e-03, 7.98e-04
```

![Taylor–Green vortex decay and the measured lattice viscosity](lbm_taylor_green_decay.png)

Panel (a) shows the initial vorticity, four counter-rotating cells, with the velocity vectors. Panel (b) shows the energy histories for three values of $\tau$ falling on the predicted exponentials. Panel (c) is the main result: the measured viscosities lie on $c_s^2(\tau - 1/2)$, while $c_s^2\tau$ would overestimate the viscosity by a factor of 51 at $\tau = 0.51$ and 1.3 at $\tau = 2$. Panel (d) shows that the relative viscosity error falls by a factor of 4 per doubling of $N$. The $\tau = 1.5$ errors equal the $\tau = 1$ errors at half the resolution, so the error depends only on $(\tau - 1/2)/N$, that is on the product $\nu k$ in lattice units.

## Related Notes

- [From Boltzmann to Lattice Boltzmann](../../../notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md)
- [The Boltzmann Equation](../../../notes/numerical/lattice_boltzmann/boltzmann_equation.md)
- [The Lattice Boltzmann Algorithm](../../../notes/numerical/lattice_boltzmann/lattice_boltzmann_algorithm.md)
- [The Lattice Boltzmann Method in Practice](../../../notes/numerical/lattice_boltzmann/practical_lbm.md)
