# Time-Averaged Velocity Field

This script generates a synthetic noisy longitudinal velocity field on a 200 × 60 grid and compares it with its mean field, the first step of a Reynolds decomposition. Because the synthetic data has no time axis, the mean is taken along the streamwise direction $x$, which stands in for a time average when the flow is statistically homogeneous in $x$.

## Overview

- Builds a grid of 200 points in $x$ (1750 to 1900 mm) and 60 points in $y$ (0 to 60 mm).
- Evaluates $u(x,y) = 10\sin(0.02x)\cos(0.1y) + \epsilon$, where $\epsilon$ is Gaussian noise with standard deviation 5 m/s from a seeded random generator.
- Averages the field over $x$ at each $y$ to get the mean profile $\bar{u}(y)$.
- Plots the instantaneous field as a colour image (top) and the mean field $\bar{u}(y)$, repeated along $x$, as a filled contour plot (bottom), both with the `jet` colour map.

## Mathematical Background

### Reynolds Decomposition

$$
u(x,y) = \bar{u}(y) + u'(x,y)
$$

The mean $\bar{u}$ holds the large-scale structure and the fluctuation $u'$ the random part. The script computes and plots $\bar{u}$; $u'$ is the difference between the two panels.

### Mean Along the Streamwise Direction

$$
\bar{u}(y) = \langle u(x,y) \rangle_x = \frac{1}{N_x}\sum_{i=1}^{N_x} u(x_i, y)
$$

In an experiment or unsteady simulation $\bar{u}$ would be a time average at each point, $`\bar{u} = \frac{1}{T}\int_0^T u\,dt`$. Replacing it by an average over $x$ assumes the flow statistics do not change along $x$.

### Fluctuation

$$
u'(x,y) = u(x,y) - \bar{u}(y),
\qquad \langle u' \rangle_x = 0
$$

## Implementation

- Constants: `X_RANGE` and `Y_RANGE` (mm), `NX`, `NY`, `NOISE_STD` (m/s) and `SEED`.
- `synthetic_velocity_field(X, Y, rng, noise_std)` evaluates the sine-cosine field plus noise.
- `streamwise_average(field)` averages a `(NY, NX)` array over its $x$ axis.
- `plot_fields(seed)` builds the grid, computes the field and its mean, draws the top panel with `imshow(origin="lower")` so that $y = 0$ is at the bottom, and draws the bottom panel with `contourf`. Returns the figure.
- `main(argv=None)` parses the flags, saves the figure if requested, and shows it.

## Usage

```bash
python main.py                      # open the figure in a window
python main.py --no-show --output . # save time_averaged_velocity_field.png without opening a window
```

| Flag | Description |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure there as a PNG |

## Output

Top: the noisy instantaneous field, with a band of high velocity around $y \approx 30$ mm. Bottom: the mean field, a set of horizontal bands that keep the large-scale $y$ structure and remove the noise.

![Time-averaged velocity field](time_averaged_velocity_field.png)

## Related Notes

- [Reynolds Decomposition](../../../notes/fluid_mechanics/turbulence/reynolds_decomposition.md)
- [Turbulence Statistics](../../../notes/fluid_mechanics/turbulence/statistics.md)
- [Turbulence Modeling in CFD](../../../notes/numerical/cfd/turbulence_modeling.md)
