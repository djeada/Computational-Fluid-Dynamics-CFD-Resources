# Turbulent Flow: Reynolds Decomposition

This script splits a synthetic velocity signal into its time mean and fluctuation, following the Reynolds decomposition used in turbulence modelling. It plots the signal, the fluctuation and the squared fluctuation, and reports the mean, RMS fluctuation, one-component turbulent kinetic energy and turbulence intensity.

## Overview

- Generates $u(t) = U + A\sin(t) + \epsilon(t)$ on 1000 samples over $0 \le t \le 100$, with $U = 5$, $A = 1$ and Gaussian noise $\epsilon$ of standard deviation 0.2 from a seeded random generator.
- Computes the time mean $\bar{u}$ and the fluctuation $u'(t) = u(t) - \bar{u}$.
- Plots, in a 2 × 2 grid: (a) $u(t)$ with $\bar{u}$ as a dashed line, (b) $u'(t)$, and (c) $(u')^2$ with its mean $\overline{u'^2}$ as a dashed line.
- Lists $\bar{u}$, $\overline{u'^2}$, $u_{rms}$, $k_u = \frac{1}{2}\overline{u'^2}$ and $Tu = u_{rms}/\bar{u}$ in the fourth panel.

## Mathematical Background

### Reynolds Decomposition

$$
u(t) = \bar{u} + u'(t)
$$

### Time Mean

```math
\bar{u} = \frac{1}{T}\int_0^T u\, dt
```

evaluated as the arithmetic mean of the samples. By definition $\overline{u'} = 0$.

### RMS Fluctuation and Turbulence Intensity

$$
u_{rms} = \sqrt{\overline{u'^2}},
\qquad Tu = \frac{u_{rms}}{\bar{u}}
$$

### Turbulent Kinetic Energy

The turbulent kinetic energy per unit mass is $k = \frac{1}{2}\left(\overline{u'^2} + \overline{v'^2} + \overline{w'^2}\right)$. With only one velocity component the script reports its contribution

$$
k_u = \frac{1}{2}\overline{u'^2}
$$

For the default signal the variance is close to $A^2/2 + 0.2^2 = 0.54$, so $u_{rms} \approx 0.73$ and $`Tu \approx 15\%`$.

## Implementation

- Constants: `MEAN_VELOCITY`, `OSCILLATION_AMPLITUDE`, `NOISE_STD`, `DURATION`, `N_SAMPLES` and `SEED`.
- `synthetic_signal(seed)` returns the time array and $u(t)$.
- `reynolds_decomposition(velocity)` returns $\bar{u}$ and $u'$.
- `turbulence_statistics(mean, fluctuation)` returns $\overline{u'^2}$, $u_{rms}$, $k_u$ and $Tu$.
- `plot_decomposition(time, velocity)` draws panels (a)-(c) and the statistics panel and returns the figure.
- `main(argv=None)` parses the flags, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                      # open the figure in a window
python main.py --no-show --output . # save turbulence_plots.png without opening a window
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |

## Output

Panel (a) shows the signal oscillating about its mean of about 5, panel (b) the same signal shifted to zero mean, and panel (c) the non-negative squared fluctuation, whose mean equals $2k_u$. The fourth panel lists the computed statistics. The synthetic signal is a noisy sine wave rather than real turbulence, so it has a single dominant frequency instead of a broad spectrum.

![Reynolds decomposition of a velocity signal](turbulence_plots.png)

## Related Notes

- [Reynolds Decomposition](../../../notes/fluid_mechanics/turbulence/reynolds_decomposition.md)
- [Turbulence Statistics](../../../notes/fluid_mechanics/turbulence/statistics.md)
- [RANS Equations](../../../notes/fluid_mechanics/turbulence/rans_equations.md)
- [Turbulence Modeling in CFD](../../../notes/numerical/cfd/turbulence_modeling.md)
