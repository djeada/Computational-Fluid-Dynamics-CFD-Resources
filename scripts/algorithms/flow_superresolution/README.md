# Flow Super-Resolution

This script reconstructs a $128 \times 128$ velocity field from its $4\times$ block average with cubic-spline (bicubic) interpolation and with a learned linear patch model, then denoises noisy vortex-street snapshots by truncating their proper orthogonal decomposition (POD). Both parts use synthetic fields with a known truth, so the relative $L_2$ errors and energy spectra show exactly what each method recovers and what is lost for good.

## Overview

- Generates random divergence-free velocity fields on a periodic $[0, 2\pi)^2$ grid of $128^2$ points with an energy spectrum that peaks at $k = 3$ and decays as $k^{-3}$, the slope of the two-dimensional enstrophy cascade.
- Applies the measurement operator $H$: averaging over $4 \times 4$ blocks, which gives a $32 \times 32$ field, as a PIV interrogation window or a coarse grid would.
- Reconstructs the $u$ component of a held-out field in two ways. The first is periodic cubic-spline interpolation (`scipy.ndimage.zoom`, order 3). The second is a ridge-regression model that maps each $5 \times 5$ patch of coarse values to the 16 fine values inside its centre cell, trained on 40 separate fields (40 960 patches).
- Compares the relative $L_2$ errors and radially summed energy spectra with the truth and with the truth low-pass filtered at the input Nyquist wavenumber $k = 16$.
- Builds 80 snapshots of a convected Kármán-like vortex street ($128 \times 64$ points), adds white noise of standard deviation $0.5\times$ the field RMS, and reconstructs the snapshots from $r = 0, \dots, 40$ POD modes.
- Marks the rank chosen by the Gavish–Donoho optimal hard threshold for known noise.

## Mathematical Background

### Synthetic Velocity Fields

White noise is filtered in Fourier space to give a stream function $\hat\psi(\mathbf{k})$. The velocity is $u = \partial\psi/\partial y$, $v = -\partial\psi/\partial x$, so $\nabla\cdot\mathbf{u} = 0$ exactly. The modulus is chosen so that the shell-summed spectrum is

$$
E(k) \propto \frac{(k/k_0)^4}{\left(1 + (k/k_0)^2\right)^{(4 + 3)/2}},
\qquad |\hat{\mathbf{u}}(\mathbf{k})|^2 = \frac{E(k)}{2\pi k},
\qquad |\hat\psi| = \frac{|\hat{\mathbf{u}}|}{k}
$$

with $k_0 = 3$. The fields are scaled to unit RMS per component, and the Nyquist modes are removed so that the spectral derivatives stay real.

### Measurement Model

The coarse data are $\mathbf{y} = H\mathbf{x}$, where $H$ averages $4 \times 4$ blocks. $H$ has a 16-dimensional null space in every coarse cell, so super-resolution is ill-posed and every method has to supply a prior.

### Ridge Patch Model

For coarse cell $c$, $\mathbf{a}_c \in \mathbb{R}^{26}$ holds its $5 \times 5$ periodic neighbourhood plus a constant 1, and $\mathbf{b}_c \in \mathbb{R}^{16}$ holds the fine values inside the cell. Stacking all cells of all training fields as rows of $A$ and $B$, the weights are

```math
W = \left(A^T A + \lambda I\right)^{-1} A^T B,
\qquad \lambda = 10^{-3}\,\frac{\mathrm{tr}(A^T A)}{26}
```

and the reconstruction of a new field is $\hat{\mathbf{b}}_c = W^T \mathbf{a}_c$ for every cell. The model is the best linear estimator of the fine values given the patch, learned from data. For a Gaussian random field, Fourier modes above the Nyquist wavenumber of the input are statistically independent of those below it. No estimator can then predict them, and the best it can do is undo the blurring of the block average below $k = 16$ and share out the aliased energy.

### Errors and Spectra

```math
\varepsilon = \frac{\|\hat{\mathbf{x}} - \mathbf{x}\|_2}{\|\mathbf{x}\|_2},
\qquad E(k) = \sum_{\mathbf{k}:\ \mathrm{round}(|\mathbf{k}|) = k} \tfrac{1}{2}\left|\hat u(\mathbf{k})\right|^2
```

where $\hat u$ is the discrete Fourier transform divided by $128^2$.

### POD Truncation and the Gavish–Donoho Threshold

With the noisy snapshot matrix $Y = X + \sigma Z$ ($m = 8192$ points by $n = 80$ snapshots) and its POD from `scripts/_numerics.py`, the rank-$`r`$ reconstruction keeps the mean and the $`r`$ leading modes. For known $\sigma$, Gavish & Donoho (2014) show that the asymptotically optimal hard threshold on the singular values is

```math
\tau = \lambda(\beta)\sqrt{m}\,\sigma,
\qquad \lambda(\beta) = \sqrt{2(\beta + 1) + \frac{8\beta}{\beta + 1 + \sqrt{\beta^2 + 14\beta + 1}}},
\qquad \beta = n/m
```

which here gives $\tau = 20.3$.

## Implementation

- `random_velocity_field(rng, n, k0, slope)` generates $(u, v)$. `block_average`, `bicubic_upsample` and `lowpass` implement $H$, the interpolation baseline and the ideal low-pass reference.
- `patch_features`, `block_targets`, `assemble_blocks`, `fit_patch_model` and `patch_upsample` implement the ridge model with `numpy.linalg.solve`.
- `relative_l2` and `energy_spectrum` compute the metrics. `super_resolution_case(seed)` trains on `N_TRAIN = 40` fields and tests on one more.
- `vortex_street()` builds two staggered rows of Gaussian vortices of radius 0.35 in a $4 \times 2$ box. Their strengths oscillate by $`\pm 20\,\%`$, so the street is not a pure translation. `cleansing_case(seed)` adds noise, calls `compute_pod`, and evaluates every rank and the threshold from `gavish_donoho_threshold(shape, sigma)`.
- `plot_super_resolution` and `plot_cleansing` draw the two figures.

## Usage

```bash
python main.py                          # show the figures
python main.py --no-show --output .     # save both figures as PNGs in the current directory
```

## Output

![Truth, block-averaged input, bicubic and ridge reconstructions, their errors and energy spectra](flow_superresolution.png)

The held-out field has 6.9 % of its energy above $k = 16$. Bicubic interpolation gives a relative error of 0.284 and the ridge patch model 0.263. Keeping the truth exactly up to $|k_x|, |k_y| < 16$ would give 0.257. The spectra show where the gain comes from. Bicubic interpolation of block averages keeps only 65 % of the energy in the band $8 \le k \le 16$, while the ridge model, which has learned to undo the block filter, keeps 95 %. Above $k = 16$ the ridge output holds 1.4 % of the energy against 6.9 % in the truth. A model trained on a mean-square loss returns a conditional mean, which is smooth by construction.

![Clean, noisy and POD-denoised vortex-street snapshots, error against rank, and singular values](flow_cleansing.png)

The noise gives a relative error of 0.50. The street is described by two pairs of travelling modes, which hold 99.2 % of the fluctuation energy. Truncating at $r = 4$ reduces the error to 0.146. Adding more modes adds noise faster than signal, and at $r = 40$ the error has risen back to 0.37. The singular values of the noisy data level off at about 15–19, the noise floor. The Gavish–Donoho threshold selects $r = 4$, the same rank as the best truncation found with the clean data, which a real measurement would not have.

## Related Notes

- [Super-Resolution and Flow Cleansing](../../../notes/machine_learning/flow/superresolution_and_flow_cleansing.md)
- [Gappy POD](../../../notes/numerical/pod/gappy_pod.md)
- [Machine Learning in Particle Image Velocimetry](../../../notes/machine_learning/flow/particle_image_velocimetry.md)
