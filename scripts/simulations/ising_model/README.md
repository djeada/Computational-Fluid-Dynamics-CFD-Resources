# Ising Model Simulation

This script simulates a two-dimensional Ising model using the Metropolis algorithm to study phase transitions between ferromagnetic and paramagnetic states on a 2D spin lattice. Watch it on YouTube: [![YouTube](https://img.youtube.com/vi/aIUKwLx_Kj8/maxresdefault.jpg)](https://youtube.com/shorts/aIUKwLx_Kj8?feature=share)

## Overview

- **2D spin lattice**: each site $s_i \in \{+1,-1\}$, initialized randomly.
- **Metropolis Monte Carlo**: samples spin configurations from the Boltzmann distribution.
- **Phase transition** at critical temperature $T_c$: spontaneous magnetization appears below $T_c$.
- **Numba-accelerated** (`@njit`) energy and magnetization calculations for fast Monte Carlo sweeps.
- **Live animation**: spin lattice coloring plus real-time plots of magnetization and energy.

## Mathematical Background

### Hamiltonian

The energy of a spin configuration is described by:

$$H = -J \sum_{\langle i,j \rangle} s_i s_j$$

where $J$ is the coupling constant ($J > 0$ ferromagnetic, $J < 0$ antiferromagnetic) and $\langle i,j\rangle$ denotes nearest-neighbor pairs.

### Magnetization

$$M = \sum_i s_i$$

$M > 0$ indicates a ferromagnetic phase; $M \approx 0$ a disordered (paramagnetic) phase.

### Boltzmann Factor

Thermal fluctuations enter via the acceptance probability:

$$P(\Delta E) = \exp\!\left(-\frac{\Delta E}{k_B T}\right)$$

where $\Delta E = 2s_i\sum_{\text{neighbors}} s_j$ is the energy change from flipping spin $s_i$.

### Metropolis Criterion

A proposed spin flip is accepted with probability:

$$A = \begin{cases} 1 & \Delta E \le 0 \\ e^{-\beta\Delta E} & \Delta E > 0 \end{cases}, \quad \beta = \frac{1}{k_B T}$$

At low $T$ the system orders (ferromagnetic phase); at high $T$ thermal noise destroys order (paramagnetic phase).

## Implementation

1. Initialize an $N\times N$ lattice with random $\pm1$ spins via `initialize_lattice(N_ROWS, N_COLS)`.
2. For each Monte Carlo step, loop over all lattice sites: compute $\Delta E = 2s_i\sum_{\text{neighbors}}s_j$ using `metropolis_step_numba` (Numba JIT-compiled).
3. Accept or reject each spin flip using the Metropolis criterion with $\beta = 1/(k_B T)$.
4. Periodically compute total energy via `calculate_energy_numba` and magnetization via `calculate_magnetization_numba`.
5. Feed the lattice state and thermodynamic observables into `animate_simulation` for live plotting.
6. Repeat for `TOTAL_STEPS` Monte Carlo sweeps.

## Output

The animation produces three synchronized panels:

- **Lattice**: spin-up ($+1$) sites colored orange, spin-down ($-1$) blue; domain walls are visible near $T_c$.
- **Magnetization plot**: tracks $M(t)$; shows spontaneous symmetry breaking below $T_c$.
- **Energy plot**: tracks $H(t)$; drops sharply as the system orders at low temperature.

## Running the Script

Adjust `N_ROWS`, `N_COLS`, `BETA`, and `TOTAL_STEPS` at the top of the script:

```python
N_ROWS, N_COLS = 100, 100   # lattice size
BETA           = 0.44       # ≈ 1/T_c for the 2D Ising model
TOTAL_STEPS    = 500        # Monte Carlo sweeps
```
