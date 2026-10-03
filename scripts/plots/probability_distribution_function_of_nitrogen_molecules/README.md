# Maxwell-Boltzmann Speed Distribution of N₂ Molecules

This script plots the Maxwell-Boltzmann speed distribution of nitrogen (N₂) molecules at 300 K, 600 K, 900 K and 1200 K, and marks the most probable, mean and root-mean-square speed on each curve. It shows how a higher temperature flattens and broadens the distribution and moves all three characteristic speeds to higher values, which is the kinetic-theory picture behind gas properties such as the speed of sound.

## Overview

- Evaluates the Maxwell-Boltzmann probability density $f(v)$ on 500 points from 0 to 3000 m/s.
- Plots one curve per temperature (300, 600, 900 and 1200 K) on a single axes.
- Marks the most probable speed $v_p$ (dotted), mean speed $\bar{v}$ (dashed) and RMS speed $v_{rms}$ (dash-dot) of each curve with a vertical line from the axis up to the curve, in the curve's colour.
- Prints the three characteristic speeds for each temperature.
- Uses the N₂ molecular mass $m = 4.65 \times 10^{-26}$ kg and $k_B = 1.380649 \times 10^{-23}$ J/K.

## Mathematical Background

### Maxwell-Boltzmann Distribution

The probability density of molecular speed $v$ in an ideal gas at temperature $T$ is

$$
f(v) = 4\pi\left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2
\exp\left(-\frac{m v^2}{2 k_B T}\right)
$$

It has units of s/m and integrates to one over $0 \le v < \infty$.

### Characteristic Speeds

Most probable speed (maximum of $f$):

$$
v_p = \sqrt{\frac{2 k_B T}{m}}
$$

Mean speed:

$$
\bar{v} = \sqrt{\frac{8 k_B T}{\pi m}}
$$

Root-mean-square speed:

$$
v_{rms} = \sqrt{\frac{3 k_B T}{m}}
$$

so $v_p < \bar{v} < v_{rms}$ at every temperature, and all three scale with $\sqrt{T}$. At 300 K the script gives $v_p = 422$ m/s, $\bar{v} = 476$ m/s and $v_{rms} = 517$ m/s.

## Implementation

- Constants: `K_B` (J/K), `M_N2` (kg), `TEMPERATURES` (K) and `MAX_SPEED` (m/s).
- `maxwell_boltzmann_distribution(v, T, m)` evaluates $f(v)$.
- `characteristic_speeds(T, m)` returns $(v_p, \bar{v}, v_{rms})$.
- `plot_distributions(temperatures, max_speed)` plots the curves and draws the speed markers with `plt.vlines`, then builds a legend with one entry per temperature and one per marker style.
- `main(argv=None)` prints the speeds, parses the flags, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                      # open the figure in a window
python main.py --no-show --output . # save probability_distribution_function.png without opening a window
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |

## Output

Four distribution curves, one per temperature, with vertical markers at the most probable, mean and RMS speeds. The 300 K curve is tall and narrow with a peak near 420 m/s; the 1200 K curve is flatter and extends past 2000 m/s.

![Maxwell-Boltzmann speed distribution of N2](probability_distribution_function.png)

## Related Notes

- [From Boltzmann to Lattice Boltzmann](../../../notes/numerical/lattice_boltzmann/from_boltzmann_to_lattice_boltzmann.md)
- [The Boltzmann Equation](../../../notes/numerical/lattice_boltzmann/boltzmann_equation.md)
- [Thermodynamics of Compressible Flow](../../../notes/fluid_mechanics/compressible_flow/thermodynamics.md)
- [Speed of Sound](../../../notes/fluid_mechanics/compressible_flow/speed_of_sound.md)
