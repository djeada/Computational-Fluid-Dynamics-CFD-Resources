# Mean Velocity Magnitude: Experiment vs CFD Comparison

This script plots a mock experimental profile and a mock CFD scale-resolving simulation (SRS) profile of the normalised mean velocity magnitude $|U|/U_0$ along an under-body centreline. It mimics the line plots used in industrial CFD validation, where simulation results are overlaid on wind-tunnel measurements. Both curves are synthetic, so the figure shows the layout of such a comparison, not real data.

## Overview

- Generates a mock "experimental" profile from an exponentially damped sine wave on 50 points over 0 to 6 m.
- Adds seeded Gaussian noise to that profile to produce a mock "CFD SRS" profile.
- Prints the RMS difference between the two profiles.
- Plots the experimental data as black markers joined by a line and the CFD result as a cyan line, with axis labels, a legend and a dashed grid.

## Mathematical Background

### Normalised velocity magnitude

The quantity on the vertical axis is the mean velocity magnitude divided by a reference free-stream speed $U_0$:

$$
\frac{|\overline{\mathbf{U}}|}{U_0} = \frac{\sqrt{\overline{u}^2 + \overline{v}^2 + \overline{w}^2}}{U_0}
$$

The script does not compute this from velocity components. It prescribes the profile directly.

### Mock experimental profile

$$
u_{\mathrm{exp}}(x) = e^{-0.2x}\sin(x) + 0.75,
\qquad 0 \le x \le 6
$$

### Mock CFD profile

$$
u_{\mathrm{CFD}}(x_i) = u_{\mathrm{exp}}(x_i) + \epsilon_i,
\qquad \epsilon_i \sim \mathcal{N}(0,\, 0.05^2)
$$

### Agreement metric

$$
\mathrm{RMS} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(u_{\mathrm{CFD}}(x_i) - u_{\mathrm{exp}}(x_i)\right)^2}
$$

## Implementation

- `generate_data(n_points, x_max, noise_std, seed)` builds the coordinate array and both profiles. The constants `N_POINTS = 50`, `X_MAX = 6.0` m, `DECAY_RATE = 0.2`, `OFFSET = 0.75`, `NOISE_STD = 0.05` and `SEED = 0` set the shape and noise.
- `plot_profiles(x, exp, cfd)` draws both curves on one set of axes and returns the figure.
- `main(argv)` parses the command-line flags, prints the RMS difference, and saves and/or shows the figure.

## Usage

```bash
python main.py                      # open the plot window
python main.py --no-show --output . # save mean_velocity_magnitude.png without opening a window
```

| Flag | Effect |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save `mean_velocity_magnitude.png` in it |

## Output

The figure shows $|U|/U_0$ against relative distance along the line. The black experimental curve rises to about 1.5, falls to about 0.35 and recovers. The noisy cyan CFD curve follows it closely, with an RMS difference of about 0.05.

![mean_velocity_magnitude_plot](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/786494a3-21c4-4141-bafd-0f40da8db897)

## Related Notes

- [Turbulence Modeling](../../../notes/numerical/cfd/turbulence_modeling.md): time averages, mean velocity, and the RANS/LES approaches behind SRS.
- [Turbulence Statistics](../../../notes/fluid_mechanics/turbulence/statistics.md): mean and fluctuating quantities.
- [The Strategy of CFD](../../../notes/numerical/cfd/cfd_process.md): post-processing and comparing numerical with reference solutions.
