# Sod Shock Tube

This script animates Sod's shock tube, the standard test of compressible-flow solvers, computed with a first-order Godunov scheme and a second-order MUSCL–Hancock scheme and compared with the exact Riemann solution at every frame. Both schemes are cell-centred finite-volume methods with the HLLC approximate Riemann solver at the faces. The four panels show density, velocity, pressure and specific internal energy, so the rarefaction, the contact discontinuity and the shock can be followed as they leave the diaphragm, and the status line reports the L1 density error of both schemes.

## Overview

- Solves the 1D Euler equations for an ideal gas with $\gamma = 1.4$ on $0 \le x \le 1$ with 200 cells (`N_CELLS`). The diaphragm is at $x_0 = 0.5$, with $(\rho, u, p) = (1, 0, 1)$ on the left and $(0.125, 0, 0.1)$ on the right (Sod 1978).
- Runs two schemes side by side on the same grid: first-order Godunov (piecewise-constant cells) and MUSCL–Hancock (limited piecewise-linear cells with a half-step predictor), both with HLLC fluxes.
- Uses a fixed time step $\Delta t = 10^{-3}$, so that frames are evenly spaced in time; 200 steps reach the comparison time $t = 0.2$. The CFL number is about 0.44. A step whose CFL number would exceed 0.9 (`MAX_CFL`, on a finer grid for example) is split into equal sub-steps.
- Uses zero-gradient ghost cells at both ends. Until the waves reach the ends, these keep mass and energy exactly constant and change the momentum only by the pressure force $(p_L - p_R)t$.
- Computes the exact solution with Toro's pressure function and Newton iteration for the star pressure, and draws it on 1000 points at the current time.
- Shows a 2 × 2 grid of panels in the window, the `--output` PNG and the reel; the status line gives the time, the step count and the L1 density errors of the first- and second-order schemes.
- `--reel FILE` renders the run as a 1080 × 1920 MP4 for YouTube Shorts or Instagram Reels.

## Mathematical Background

### Euler Equations

In conservation form,

```math
\frac{\partial \mathbf{U}}{\partial t} + \frac{\partial \mathbf{F}(\mathbf{U})}{\partial x} = 0,
\qquad
\mathbf{U} = \begin{pmatrix} \rho \\ \rho u \\ E \end{pmatrix},
\qquad
\mathbf{F} = \begin{pmatrix} \rho u \\ \rho u^2 + p \\ (E + p)u \end{pmatrix},
\qquad
p = (\gamma - 1)\left(E - \tfrac{1}{2}\rho u^2\right)
```

The specific internal energy is $e = p/((\gamma - 1)\rho)$ and the sound speed $c = \sqrt{\gamma p/\rho}$.

### Exact Riemann Solution

The initial jump breaks into a left rarefaction, a contact and a right shock. The pressure $`p^*`$ and velocity $`u^*`$ between the left and right waves solve

```math
f_L(p^*) + f_R(p^*) + u_R - u_L = 0,
\qquad
f_K(p) =
\begin{cases}
(p - p_K)\sqrt{\dfrac{A_K}{p + B_K}}, & p > p_K \ \text{(shock)}, \\[2ex]
\dfrac{2c_K}{\gamma - 1}\left[\left(\dfrac{p}{p_K}\right)^{(\gamma - 1)/2\gamma} - 1\right], & p \le p_K \ \text{(rarefaction)},
\end{cases}
```

with $A_K = 2/((\gamma + 1)\rho_K)$ and $B_K = (\gamma - 1)p_K/(\gamma + 1)$. `star_state` solves it by Newton iteration from the primitive-variable estimate, and $u^* = \tfrac12(u_L + u_R) + \tfrac12(f_R - f_L)$. For Sod's problem $p^* = 0.30313$ and $u^* = 0.92745$. `exact_solution` then samples the self-similar solution at $\xi = (x - x_0)/t$: Rankine–Hugoniot densities behind a shock, isentropic densities behind a rarefaction, and the centred fan inside it.

### Finite-Volume Update and HLLC Flux

Both schemes update the cell averages with

```math
\mathbf{U}_i^{n+1} = \mathbf{U}_i^n - \frac{\Delta t}{\Delta x}\left(\mathbf{F}_{i+1/2} - \mathbf{F}_{i-1/2}\right)
```

The face flux is the HLLC flux of Toro, Spruce and Speares (1994) with the wave-speed estimates $S_L = \min(u_L - c_L, u_R - c_R)$ and $S_R = \max(u_L + c_L, u_R + c_R)$ and the contact speed

```math
S_* = \frac{p_R - p_L + \rho_L u_L(S_L - u_L) - \rho_R u_R(S_R - u_R)}{\rho_L(S_L - u_L) - \rho_R(S_R - u_R)}
```

The first-order Godunov scheme takes the two cell averages next to the face as the left and right states.

### MUSCL–Hancock

The second-order scheme (Toro 2009, section 14.4) reconstructs each conservative variable linearly with van Leer's limited slope

```math
\Delta_i = \begin{cases} \dfrac{2\,ab}{a + b}, & ab > 0, \\[1ex] 0, & ab \le 0, \end{cases}
\qquad a = \mathbf{U}_i - \mathbf{U}_{i-1}, \quad b = \mathbf{U}_{i+1} - \mathbf{U}_i,
```

evolves the two boundary values of each cell by half a time step,

```math
\bar{\mathbf{U}}_i^{L,R} = \mathbf{U}_i \mp \tfrac12\Delta_i + \frac{\Delta t}{2\Delta x}\left[\mathbf{F}\left(\mathbf{U}_i - \tfrac12\Delta_i\right) - \mathbf{F}\left(\mathbf{U}_i + \tfrac12\Delta_i\right)\right],
```

and takes the HLLC flux of $`\bar{\mathbf{U}}_i^R`$ and $`\bar{\mathbf{U}}_{i+1}^L`$ at face $i + 1/2$. The limiter sets the slope to zero at extrema, which keeps the scheme free of the large oscillations a linear second-order scheme would produce at the shock; a small overshoot remains in the internal energy at the contact.

### Accuracy

For a solution with discontinuities, the L1 error of a first-order scheme falls roughly like $\Delta x^{1/2}$ to $\Delta x$: the contact smears over a width that grows like $`\sqrt{t\,\Delta x}`$, while a shock stays a few cells wide. Second order improves the smooth rarefaction most and sharpens the contact.

## Implementation

- `conservative`, `primitive`, `physical_flux` and `sound_speed` convert between variables and evaluate the Euler flux.
- `pressure_function`, `star_state` and `exact_solution` implement the exact Riemann solver.
- `hllc_flux` is the vectorised HLLC flux; `godunov_fluxes` and `muscl_hancock_fluxes` compute all face fluxes of one scheme (`van_leer_slope` is the limiter and `pad` adds two zero-gradient ghost cells), and `update` applies the conservative update.
- `SodSimulation(n_cells, dt, max_cfl)` derives from the shared `Simulation` class in [`scripts/_animation.py`](../../_animation.py). It holds the conservative `states` of both schemes; `step()` advances each by `dt`, split into sub-steps if needed, and stores the CFL number in `cfl`. `fields(scheme)` returns density, velocity, pressure and internal energy, `exact(x)` the exact solution at the current time and `l1_errors()` the mean absolute density error of each scheme.
- `SodView` draws the exact solution as a solid line, the first-order scheme dashed and MUSCL–Hancock as dots, on fixed axes. The legend sits under the velocity plateau in the window and below the pressure plateau in the reel, where the curves never pass.
- `ANIMATION` sets the title, the PNG name `sod_shock_tube.png`, 200 frames and one time step per frame.

The tests in `tests/test_sod_shock_tube.py` check the star states of Toro's five test problems, the wave positions and isentropy of the exact solution, conservation of mass and energy and the momentum balance, positivity, the accuracy and convergence of both schemes, and the CFL sub-stepping.

## Usage

```bash
python main.py                                    # animate in a window (space pauses)
python main.py --no-show --output . --steps 200   # save the state at t = 0.2 as a PNG
python main.py --reel reel.mp4                    # vertical video for Shorts/Reels
python main.py --reel reel.mp4 --reel-seconds 8   # shorter reel
```

`--steps N` sets the number of frames; each frame is one time step of $\Delta t = 10^{-3}$, and the default 200 frames reach $t = 0.2$. A reel shows one time step per video frame, so the default run gives a reel of about 9 s at 30 fps, including the 2 s hold on the final frame. The script prints the final time, the CFL number, the exact $`p^*`$ and $`u^*`$ and the two L1 errors.

## Output

![Density, velocity, pressure and internal energy of Sod's shock tube at t = 0.2](sod_shock_tube.png)

The image shows the state at $t = 0.2$. From left to right, the rarefaction fan spans $0.26 < x < 0.49$, the contact is at $x = 0.685$ and the shock at $x = 0.850$. Counting the cells between 10 % and 90 % of each density jump, the first-order scheme (dashed) spreads the contact over 15 cells and the shock over 5, and it rounds the corners of the fan; this is clearest in the density and internal-energy panels. MUSCL–Hancock follows the fan closely and needs 5 cells for the contact and 2 for the shock, with a small overshoot of the internal energy just behind the contact. The shock stays narrow in both schemes because the characteristics on either side run into it, whereas the contact keeps spreading as the run goes on. The pressure and velocity are continuous across the contact, and neither scheme produces a disturbance there. At $t = 0.2$ the L1 density error is 0.0115 for the first-order scheme and 0.0031 for MUSCL–Hancock.

## Related Notes

- [Riemann Solvers and Godunov Methods](../../../notes/numerical/fvm/riemann_solvers.md)
- [Convection Schemes and Limiters](../../../notes/numerical/fvm/convection_schemes.md)
- [Shock Waves](../../../notes/fluid_mechanics/compressible_flow/shock_waves.md)
- [Finite Volume Discretization](../../../notes/numerical/fvm/discretization.md)
