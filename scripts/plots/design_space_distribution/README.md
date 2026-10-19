# Design Space Distribution via Sobol Sequences

This script draws a four-dimensional scrambled Sobol design of 512 geometry variants and plots two 2D projections of it, showing how evenly a low-discrepancy sequence covers a design space. Each dimension stands for one normalised shape parameter (`Approach_Angle`, `Variable_1`, `Decklid_Height`, `Variable_2`) in $[0, 1]$. In a real CFD workflow each sample would be turned into a deformed mesh and simulated to build a surrogate-model training set.

## Overview

- Generates $2^9 = 512$ points of a 4D scrambled Sobol sequence with `scipy.stats.qmc.Sobol` (seeded, so the design is reproducible)
- Uses a power-of-two sample count, which keeps the balance properties of the Sobol sequence
- Plots `Approach_Angle` against `Variable_1` in the left panel and `Decklid_Height` against `Variable_2` in the right panel
- Shows every sample on axes fixed to the unit square

## Mathematical Background

### Low-Discrepancy Sequences

Sobol sequences are deterministic sequences built to fill $[0,1]^d$ as evenly as possible. Uniformity is measured by the star discrepancy, where the supremum is taken over boxes $J = [0, a_1) \times \dots \times [0, a_d)$ anchored at the origin:

```math
D^*_N = \sup_{J} \left| \frac{\#\{i : \mathbf{x}_i \in J\}}{N} - \text{Vol}(J) \right|
```

### Discrepancy Rates

For $N$ points in $d$ dimensions a Sobol sequence achieves

```math
D^*_N = \mathcal{O}\!\left(\frac{(\log N)^d}{N}\right)
```

while independent pseudo-random points have a discrepancy that decreases only like $N^{-1/2}$, up to a logarithmic factor.

### Why It Matters for Sampling

For a response $f$ evaluated at the design points (for example a drag coefficient from CFD), the Koksma–Hlawka inequality bounds the error of the sample mean $\hat{\mu} = \frac{1}{N}\sum_{i=1}^{N} f(\mathbf{x}_i)$:

```math
\left|\hat{\mu} - \int_{[0,1]^d} f(\mathbf{x})\, d\mathbf{x}\right| \le V_{HK}(f)\,
D^*_N
```

where $V_{HK}(f)$ is the Hardy–Krause variation of $f$. A lower discrepancy therefore gives a tighter error bound and fewer gaps in the design space.

## Implementation

- `generate_design(log2_samples, dimension, seed)` creates `Sobol(d=4, scramble=True, rng=SEED)` and calls `random_base2(m=LOG2_SAMPLES)` with `LOG2_SAMPLES = 9`.
- `make_figure(samples, parameters)` makes a 1 × 2 figure (`figsize=(12, 6)`) and scatters dimensions (0, 1) and (2, 3) using the names in `PARAMETERS`.
- `main(argv=None)` parses the flags, then shows or saves the figure.

## Usage

```bash
python main.py                          # open the figure window
python main.py --no-show --output out   # save design_space_distribution.png into out/
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

Two square scatter plots, each showing all 512 blue points spread evenly over the unit square with no visible clusters or large gaps. The title gives the number of variants and the dimension of the design.

![Design space distribution](design_space_distribution.png)

## Related Notes

- [One-Stage Sampling](../../../notes/numerical/surrogates/one_stage_sampling.md)
- [Surrogate Models: Introduction](../../../notes/numerical/surrogates/intro.md)
- [Dataset of Meshes](../../../notes/machine_learning/automotive_aerodynamics/dataset_of_meshes.md)
- [Deformation Parameters](../../../notes/machine_learning/automotive_aerodynamics/deformation_parameters.md)
