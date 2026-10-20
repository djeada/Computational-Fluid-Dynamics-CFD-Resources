# PIV Cross-Correlation

This script measures a known vortex displacement field from a synthetic pair of particle images with the standard particle image velocimetry (PIV) pipeline: FFT cross-correlation in interrogation windows, a three-point Gaussian sub-pixel peak fit, iterative window deformation, and the normalized median test for spurious vectors. Because the true displacement is known at every window, the figure can show how much each stage of the pipeline reduces the error, and which vectors the outlier test catches.

## Overview

- Seeds 3550 particles (0.03 particles per pixel, about 31 per $32 \times 32$ window) over a $320 \times 320$ px image and renders them as pixel-integrated Gaussian spots with an $e^{-2}$ diameter of 2.8 px, peak intensities in $[0.6, 1]$ and additive Gaussian camera noise of standard deviation 0.03.
- Moves the particles with a Lamb–Oseen vortex of core radius 48 px and peak displacement 5 px, centred in the image.
- Replaces the second-frame content of five interrogation windows with unrelated particles, so that these windows produce spurious vectors.
- Correlates $32 \times 32$ px windows on a 16 px grid (50 % overlap, $19 \times 19$ vectors), first without any offset and then in three window-deformation passes.
- After every pass, flags outliers with the normalized median test (threshold 2, $\varepsilon_0 = 0.1$ px) and replaces them by the median of their valid neighbours.
- Prints the median and RMS error of every pass and saves a six-panel figure.

## Mathematical Background

### Particle Images

A particle at $(x_p, y_p)$ with peak intensity $I_p$ and image diameter $d_\tau$ contributes the Gaussian $I_p \exp(-8 r^2 / d_\tau^2)$, which has standard deviation $\sigma = d_\tau/4$. The script integrates it over each pixel with error functions, so the image is the separable sum

```math
I(i, j) = 2\pi\sigma^2 \sum_p I_p\, G_y(i; y_p)\, G_x(j; x_p),
\qquad G_x(j; x_p) = \tfrac{1}{2}\left[\mathrm{erf}\!\left(\frac{j + \frac{1}{2} - x_p}{\sqrt{2}\,\sigma}\right) - \mathrm{erf}\!\left(\frac{j - \frac{1}{2} - x_p}{\sqrt{2}\,\sigma}\right)\right]
```

A particle seeded at $\mathbf{x}_m$ is drawn at $\mathbf{x}_m - \mathbf{d}(\mathbf{x}_m)/2$ in frame 1 and at $\mathbf{x}_m + \mathbf{d}(\mathbf{x}_m)/2$ in frame 2, so $\mathbf{d}(\mathbf{x})$ is the central-difference displacement $`\mathbf{u}\,\Delta t`$ at the midpoint of the particle path.

### Lamb–Oseen Vortex

The swirl displacement at radius $r$ from the centre is

```math
d_\theta(r) = A\, \frac{r_c}{r}\left(1 - e^{-r^2/r_c^2}\right)
```

with $r_c = 48$ px. The function $(1 - e^{-s^2})/s$ peaks at $s = 1.1209$ with value 0.63817, so $A = 5/0.63817$ gives a peak displacement of 5 px at $r = 53.8$ px. Near the centre the flow rotates almost as a solid body at $A/r_c = 0.16$ rad per frame, so the displacement changes by about 5 px across one window. A single correlation pass cannot represent such a gradient.

### FFT Cross-Correlation

For windows $a$ and $b$ of frames 1 and 2 with their means removed, the circular cross-correlation is computed with the FFT and normalized:

```math
R(\mathbf{s}) = \frac{\sum_{\mathbf{x}} a(\mathbf{x})\, b(\mathbf{x} + \mathbf{s})}{\sqrt{\sum_{\mathbf{x}} a^2 \sum_{\mathbf{x}} b^2}} = \frac{\mathcal{F}^{-1}\left[\overline{\mathcal{F}(a)}\,\mathcal{F}(b)\right]}{\sqrt{\sum a^2 \sum b^2}}
```

The integer location of the highest peak is the integer displacement.

### Gaussian Sub-Pixel Fit

With $R_{-}$, $R_0$, $R_{+}$ the correlation values at the peak and its two neighbours along one axis, fitting a Gaussian through the three points gives the sub-pixel offset

$$
\varepsilon = \frac{\ln R_{-} - \ln R_{+}}{2\left(\ln R_{-} - 2\ln R_0 + \ln R_{+}\right)}
$$

It is exact for a Gaussian peak. If any of the three values is not positive, the code uses the parabolic fit $\varepsilon = (R_{-} - R_{+}) / (2(R_{-} - 2R_0 + R_{+}))$ instead.

### Window Deformation

Given a predictor field $\mathbf{d}_k$ on the vector grid, the code interpolates it to every pixel with cubic splines and warps both frames symmetrically:

```math
I_1^{(k)}(\mathbf{x}) = I_1\!\left(\mathbf{x} - \tfrac{1}{2}\mathbf{d}_k(\mathbf{x})\right),
\qquad I_2^{(k)}(\mathbf{x}) = I_2\!\left(\mathbf{x} + \tfrac{1}{2}\mathbf{d}_k(\mathbf{x})\right),
\qquad \mathbf{d}_{k+1} = \mathbf{d}_k + \Delta\mathbf{s}\left(I_1^{(k)}, I_2^{(k)}\right)
```

Particles that follow the predicted field line up in the warped pair, so the correlation peak is tall and narrow and only measures the residual $\Delta\mathbf{s}$. Before it is used as a predictor, the validated field is smoothed with a Gaussian of width 0.6 grid spacings. Without this filter, errors that alternate from one vector to the next are not corrected by the window average and the iteration stalls: for this case the RMS error of the unflagged vectors levels off at 0.16 px instead of 0.061 px (Schrijer & Scarano, 2008).

### Normalized Median Test

For each component $U$ of the vector at a node, with $U_m$ the median of its eight neighbours $U_i$ and $r_m$ the median of the neighbour residuals $|U_i - U_m|$, the normalized residual is (Westerweel & Scarano, 2005)

$$
r_0 = \frac{|U_0 - U_m|}{r_m + \varepsilon_0}
$$

A vector is flagged when $r_0 > 2$ for either component. The term $\varepsilon_0 = 0.1$ px represents the random correlation error and prevents division by zero in uniform regions. Edge and corner nodes have only five or three neighbours, all on one side, so the test is less reliable there.

## Implementation

- `render_particles(x, y, intensity, size, diameter)` builds the matrices $G_x$ and $G_y$ and returns $`G_y^T \mathrm{diag}(I_p)\, G_x`$.
- `lamb_oseen_displacement(...)`, `make_image_pair(displacement, rng)` and `decorrelate_windows(frame2, starts, rng)` generate the synthetic case. `make_case(seed)` assembles it and returns the true displacement at the window centres.
- `cross_correlation(window1, window2)`, `gaussian_subpixel(minus, centre, plus)` and `correlation_peak(corr)` implement one window.
- `correlate_grid(frame1, frame2)` runs every window. `warp_pair` and `deformation_pass` implement one deformation pass, using `dense_predictor` to interpolate the predictor with `scipy.ndimage.map_coordinates`.
- `normalized_median_test(dx, dy)` and `replace_outliers(dx, dy, flagged)` validate the field.
- `run_piv(frame1, frame2)` chains one plain pass and `N_DEFORMATION_PASSES = 3` deformation passes.
- `make_figure(...)` draws the panels. `IMAGE_SIZE`, `PARTICLE_DENSITY`, `WINDOW`, `STEP`, `CORE_RADIUS`, `MAX_DISPLACEMENT`, `MEDIAN_EPS` and `MEDIAN_THRESHOLD` are module constants.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![FFT cross-correlation PIV of a synthetic vortex: image pair, correlation maps, vectors, pass convergence and error histogram](piv_cross_correlation.png)

Panel (a) overlays a crop of frame 1 (magenta) and frame 2 (green) around the window used in (b) and (c), which lies just right of the vortex centre. In the plain first pass (b) the particle pattern inside the window rotates and shears between frames, so the peak is broad and low ($R = 0.46$). After deformation (c) the warped windows match ($R = 0.94$) and the residual peak sits at the origin. Panel (d) shows the last-pass vectors over the true field. The median test flags all five decorrelated windows (orange squares) and three edge vectors that are in fact accurate (errors below 0.15 px): false positives of the one-sided neighbourhood. Panel (e) shows that the median error falls from 0.108 px after the plain pass to 0.026 px after the third deformation pass, and the RMS error of the unflagged vectors from 0.21 px to 0.061 px. Panel (f) shows the five spurious vectors, with errors of 10–18 px, which disappear after replacement. The RMS error over all 361 vectors then drops from 1.60 px to 0.071 px.

## Related Notes

- [Machine Learning in Particle Image Velocimetry](../../../notes/machine_learning/flow/particle_image_velocimetry.md)
- [Super-Resolution and Flow Cleansing](../../../notes/machine_learning/flow/superresolution_and_flow_cleansing.md)
