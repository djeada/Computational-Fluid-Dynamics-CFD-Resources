# Design Space Distribution via Sobol Sequences

This script generates 500 two-dimensional design-space samples using a scrambled Sobol quasi-random sequence and visualises their distribution as side-by-side scatter plots. By replacing pseudo-random sampling with a low-discrepancy sequence, the script demonstrates how CFD design-space exploration achieves more uniform coverage of the parameter domain $[0,1]^2$, represented here through two aerodynamic shape parameters: `Approach_Angle` and `Decklid_Height`.

## Overview

- Uses `scipy.stats.qmc.Sobol` with `scramble=True` to generate 500 samples in 2D
- Produces two scatter plots sharing the same sample set under different axis labels
- Illustrates the space-filling superiority of quasi-random over pseudo-random sampling
- Serves as a template for driving CFD geometry-variant sweeps or surrogate-model training sets

## Mathematical Background

### Low-Discrepancy Sequences

Sobol sequences are quasi-random sequences constructed to fill $[0,1]^d$ as uniformly as possible. Their uniformity is measured by the **star discrepancy**:

$$D^*_N = \sup_{J \subseteq [0,1]^d} \left| \frac{\#\{i : x_i \in J\}}{N} - \text{Vol}(J) \right|$$

### Discrepancy Comparison

For $N$ samples in $d$ dimensions, Sobol sequences achieve near-optimal discrepancy:

$$D^*_N \sim \frac{(\log N)^d}{N}$$

compared to pseudo-random sampling, which converges only as:

$$D^*_N \sim \mathcal{O}\!\left(N^{-1/2}\right)$$

### Design Space Coverage

Each sample $(x_1, x_2) \in [0,1]^2$ maps to a pair of geometry parameters. For a CFD or surrogate evaluation $f(x_1, x_2)$, Sobol sampling minimises the integration error of the quasi-Monte Carlo estimate:

$$\hat{\mu} = \frac{1}{N} \sum_{i=1}^{N} f(x_i^{(1)}, x_i^{(2)})$$

## Implementation

1. Instantiate `Sobol(d=2, scramble=True)` from `scipy.stats.qmc`
2. Draw `N = 500` samples, yielding an array of shape `(500, 2)` in $[0,1]^2$
3. Treat the sample array directly as mock geometry-variant data
4. Create a `1 × 2` subplot figure (`figsize=(12, 6)`)
5. Plot the samples on the left axes with x-label `Approach_Angle` and y-label `Variable_1`
6. Plot the same samples on the right axes with x-label `Decklid_Height` and y-label `Variable_2`
7. Add a figure-level super-title and display with `plt.show()`

## Output

The script displays a figure containing two scatter plots side by side, each showing 500 blue points distributed with high uniformity across the unit square. The left panel uses `Approach_Angle` as the horizontal axis, the right panel uses `Decklid_Height`, and both share `Variable_1` / `Variable_2` on the vertical axis. A super-title notes that 500 geometry variants were generated.

![design space distribution](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/bfe914f2-1543-458e-9f4f-06aa8cff871c)
