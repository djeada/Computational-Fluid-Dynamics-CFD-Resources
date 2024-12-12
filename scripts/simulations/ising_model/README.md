# Ising Model Simulation

This script simulates a two-dimensional Ising model using the Metropolis algorithm. The Ising model is a fundamental statistical physics model for understanding phase transitions, such as the transition between ferromagnetic and paramagnetic states.

## **Overview**

The script visualizes the evolution of spins in a 2D lattice over time, showing how the system approaches equilibrium under a given temperature. Key quantities like **magnetization** and **energy** are tracked and plotted alongside the lattice configuration.

## **Mathematical Foundation**

The Ising model describes a system of interacting spins on a lattice, where each spin $s_i$ can take one of two values: $+1$ (spin-up) or $-1$ (spin-down).

### **Hamiltonian (Energy of the System)**

The energy of a spin configuration is described by the Hamiltonian:

$$H = -J \sum_{\langle i, j \rangle} s_i s_j$$

- $J$: Coupling constant, representing the strength of the interaction between neighboring spins.
- $J > 0$: Favors aligned spins (ferromagnetic interaction).
- $J < 0$: Favors anti-aligned spins (antiferromagnetic interaction).
- $\langle i, j \rangle$: Sum over all nearest-neighbor pairs.
- $s_i$: Spin value at site $i$ ($+1$ or $-1$).

This Hamiltonian captures the competition between thermal fluctuations and spin alignment.

### **Magnetization**

The **magnetization** is the net spin of the system, a measure of how "aligned" the spins are:

$$M = \sum_i s_i$$

- $M > 0$: Spins are predominantly aligned (ferromagnetic phase).
- $M \approx 0$: Spins are disordered (paramagnetic phase).

### **Temperature and the Boltzmann Factor**

Thermal fluctuations are introduced via the Boltzmann factor:

$$P(\Delta E) = \exp\left(-\frac{\Delta E}{k_B T}\right)$$

- $T$: Temperature.
- $\Delta E$: Change in energy due to flipping a spin.
- $k_B$: Boltzmann constant (typically set to 1 in dimensionless simulations).

At high $T$, thermal fluctuations dominate, leading to disordered spins. At low $T$, spin alignment minimizes the energy.

## **Physics of the Simulation**

The simulation models a 2D lattice of spins evolving under the influence of:

I. **Thermal fluctuations**: Controlled by temperature ($\beta = \frac{1}{k_B T}$).

II. **Energy minimization**: The system naturally evolves toward configurations that minimize the Hamiltonian.

A **phase transition** occurs at a critical temperature $T_c$, below which the system exhibits spontaneous magnetization (ferromagnetic phase).

## **Numerical Method: Metropolis Algorithm**

The simulation uses the **Metropolis algorithm**, a Monte Carlo method to sample spin configurations based on the Boltzmann probability distribution.

### Steps:

I. Randomly select a spin $s_i$ and calculate the energy change $\Delta E$ if the spin were flipped.

$$\Delta E = 2 s_i \sum_{\text{neighbors}} s_j$$

II. Flip the spin with probability:

- $1$, if $\Delta E \leq 0$ (energy decreases).
- $\exp(-\beta \Delta E)$, if $\Delta E > 0$ (energy increases).

III. Repeat for all spins in the lattice.

This process evolves the system toward equilibrium.

## **Code Structure**

### 1. **Lattice Initialization**

The lattice is initialized randomly with $+1$ or $-1$ spins.

```python
def initialize_lattice(n_rows: int, n_cols: int) -> np.ndarray:
return np.random.choice([-1, 1], size=(n_rows, n_cols)).astype(np.int8)
```
### 2. **Metropolis Step**
The energy change for a potential spin flip is calculated, and the spin is flipped based on the Metropolis criterion.

```python
@njit
def metropolis_step_numba(lattice, beta):
...
```

### 3. **Energy and Magnetization Calculation**

The total energy and magnetization of the lattice are calculated periodically.

```python

@njit
def calculate_energy_numba(lattice):

...

@njit
def calculate_magnetization_numba(lattice):

...
```
### 4. **Animation**
An animated visualization of the lattice is created, with live plots of magnetization and energy.

```python
def animate_simulation(lattice, beta, steps, ...):
...
```

## **Inputs**

- **Lattice Size**: $N \times N$, controlled by `N_ROWS` and `N_COLS`.
- **Temperature**: Controlled via `BETA = 1 / (k_B T)`.
- **Steps**: Number of Monte Carlo steps (`TOTAL_STEPS`).
- **Animation Options**: Interval and update frequency.

## **Outputs**

I. **Lattice Evolution**
- Spin-up ($+1$) is visualized as orange, and spin-down ($-1$) as blue.
II. **Magnetization Plot**
- Tracks the total magnetization of the system over time.
III. **Energy Plot**
- Tracks the total energy of the system over time.

## **Key Parameters**

- **Temperature ($T$)**: Higher $T$ introduces more randomness in spin configurations.
- **Coupling Constant ($J$)**: Determines the interaction strength between spins.
- **Beta ($\beta$)**: Inverse temperature ($\beta = 1 / k_B T$).
