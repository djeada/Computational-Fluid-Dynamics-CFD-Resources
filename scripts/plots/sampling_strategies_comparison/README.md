# Sampling Strategies Comparison

This script compares random, Latin hypercube and scrambled Sobol designs of the same size in a 2D design space, showing their point layouts, their 1D marginal histograms and how their centred $L_2$ discrepancy falls with the number of samples. It is the kind of check used to choose a design of experiments before spending CFD time on each sample.

## Overview

- Draws $N = 32$ points in $[0, 1)^2$ with `numpy.random.default_rng` (random), `scipy.stats.qmc.LatinHypercube` and `scipy.stats.qmc.Sobol(scramble=True)`, all seeded.
- Plots each design over a light $32 \times 32$ grid, with marginal histograms of 8 bins (4 points per bin for a perfectly even design).
- Prints and annotates the number of empty columns of the $32 \times 32$ grid and the minimum pairwise distance (the maximin criterion) of each design.
- Computes the centred $L_2$ discrepancy for $N = 16, 32, \dots, 1024$, averaged over 20 seeds, and plots it against $N$ on log-log axes with fitted slopes and $N^{-1/2}$ and $N^{-1}$ reference lines.

## Mathematical Background

### Latin Hypercube

A Latin hypercube design of $N$ points in $d$ dimensions places exactly one point in each of the $N$ equal intervals of every coordinate:

```math
x_{ik} = \frac{\pi_k(i) - u_{ik}}{N}, \qquad u_{ik} \sim \mathcal{U}(0, 1),
```

where each $\pi_k$ is an independent random permutation of $1, \dots, N$. The 1D projections are therefore perfectly stratified; the 2D layout is still random.

### Scrambled Sobol Sequence

The first $N = 2^m$ points of a Sobol sequence form a $(t, m, d)$-net in base 2: every elementary dyadic box of volume $2^{t-m}$ contains exactly $2^t$ points. In two dimensions $t = 0$, so each box of volume $1/N$ (including each of the $N$ columns and rows) holds exactly one point. Scrambling randomises the digits while keeping this balance, which gives an unbiased estimator and allows error estimates from repeated scrambles.

### Centred $L_2$ Discrepancy

Hickernell's centred $L_2$ discrepancy has the closed form

```math
CD_2^2 = \left(\frac{13}{12}\right)^d
- \frac{2}{N}\sum_{i=1}^{N}\prod_{k=1}^{d}\left(1 + \tfrac{1}{2}|z_{ik}| - \tfrac{1}{2}z_{ik}^2\right)
+ \frac{1}{N^2}\sum_{i,j=1}^{N}\prod_{k=1}^{d}\left(1 + \tfrac{1}{2}|z_{ik}| + \tfrac{1}{2}|z_{jk}| - \tfrac{1}{2}|x_{ik} - x_{jk}|\right)
```

with $z_{ik} = x_{ik} - 1/2$. `scipy.stats.qmc.discrepancy(..., method="CD")` returns $CD_2^2$, so the script takes the square root. For independent uniform points $E[CD_2^2] \propto 1/N$, so $CD_2$ decays like $N^{-1/2}$. Low-discrepancy sequences reach nearly $N^{-1}$ (up to logarithmic factors).

## Implementation

- `sample(method, n, dimension, seed)` returns a design from one of the three samplers; Sobol requires a power-of-two `n`.
- `stratum_counts(samples, n_strata)` counts points per interval in each dimension (all ones for a Latin hypercube with `n_strata = n`).
- `min_pairwise_distance(samples)` computes the maximin criterion.
- `centred_l2_discrepancy(samples)` wraps `qmc.discrepancy`.
- `discrepancy_study(log2_n_range, n_seeds)` averages the discrepancy over seeds; `fitted_slope(ns, values)` fits the log-log slope.
- `make_figure(designs, ns, disc)` draws the three scatter panels with marginal histograms and the discrepancy panel.

## Usage

```bash
python main.py                          # print the table and show the figure
python main.py --no-show --output .     # save sampling_strategies_comparison.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

With the default seed and $N = 32$, the random design leaves 8 of the 32 columns empty and has a minimum point spacing of 0.015, against 0 empty columns for both the Latin hypercube (minimum spacing 0.040) and the Sobol design (0.085). Averaged over 20 seeds, the fitted discrepancy slopes are $-0.51$ (random), $-0.57$ (Latin hypercube) and $-0.95$ (scrambled Sobol). At $N = 1024$ the mean discrepancies are 0.0183, 0.0049 and 0.00088: the Latin hypercube lowers the constant but not the rate, while Sobol improves the rate.

![Random, Latin hypercube and Sobol designs and their discrepancy](sampling_strategies_comparison.png)

## Related Notes

- [Design of Experiments and Dataset Construction](../../../notes/machine_learning/automotive_aerodynamics/datasets.md)
- [Building and Validating a Mesh Dataset](../../../notes/machine_learning/automotive_aerodynamics/dataset_of_meshes.md)
- [One-Stage Sampling](../../../notes/numerical/surrogates/one_stage_sampling.md)
- [Adaptive Sampling](../../../notes/numerical/surrogates/adaptive_sampling.md)
