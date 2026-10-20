# Kolmogorov n-Width of Diffusing and Translating Solutions

This script compares how fast linear subspaces can approximate three parametrized solution families, a diffusing pulse, a translating pulse and a translating step, by plotting the singular values of their snapshot matrices and the worst-case error of projecting the samples onto the best $N$-dimensional subspace. It illustrates why linear reduced-order models work well for diffusion-dominated problems and poorly for transport and shocks.

## Overview

- Samples each family $u(x;\mu)$ at 400 equally spaced $\mu \in [0, 1]$ on 2000 points in $x \in [0, 1]$ m.
- The diffusing pulse is $\exp(-(x - 0.5)^2/(2s(\mu)))$ with variance $s(\mu) = 0.002 + 0.05\mu$ m $`^2`$; its shape changes smoothly with $\mu$ but it does not move.
- The translating pulse is $\exp(-((x - x_0(\mu))/0.05)^2)$ and the translating step is $H(x_0(\mu) - x)$, with $x_0(\mu) = 0.2 + 0.6\mu$ m.
- Computes the SVD of each $2000 \times 400$ snapshot matrix (without subtracting a mean) and, for $N = 1, \dots, 100$, the largest relative projection error over the samples.
- Plots example members of each family, the normalized singular values and the projection error on log-log axes with an $N^{-1/2}$ reference line.

## Mathematical Background

The Kolmogorov $N$-width of a set $\mathcal{M}$ in a normed space $V$ is the worst-case error of the best $N$-dimensional linear subspace:

```math
d_N(\mathcal{M}) = \inf_{\dim V_N = N}\ \sup_{u \in \mathcal{M}}\ \inf_{v \in V_N} \lVert u - v \rVert
```

For a finite sample of $\mathcal{M}$ the POD subspace minimizes the mean squared projection error rather than the worst case, so

```math
e_N = \max_j \frac{\lVert \mathbf{u}_j - U_NU_N^T\mathbf{u}_j \rVert_2}{\lVert \mathbf{u}_j \rVert_2}
```

with the first $N$ left singular vectors $U_N$ is an upper estimate of the relative $N$-width of the sampled set. Each sample lies in the span of all singular vectors, so its squared error is the sum of its squared coefficients $(U^T\mathbf{u}_j)_k^2$ for $k > N$; the script sums this tail directly, which keeps the error accurate down to round-off.

A unit step translated over a distance $L$ has an $L^2$ $N$-width that decays like $N^{-1/2}$: an $N$-dimensional subspace can resolve the step position only to about $L/N$, and the $L^2$ error of misplacing a unit jump by $\delta$ is $\sqrt{\delta}$. A smooth pulse of width $w$ needs roughly one mode per width travelled, $N \approx L/w$, before the error drops, after which it decays faster than any power. Smooth dependence of the shape on $\mu$ without transport gives exponential decay from the start.

## Implementation

- `diffusing_pulse`, `translating_pulse` and `translating_step` define the families; `FAMILIES` maps their names to the functions.
- `snapshot_matrix(family, x, mus)` stacks the samples as columns.
- `projection_errors(snapshots, n_max)` returns the singular values and the worst relative projection error for $N = 1, \dots, n_{\max}$.
- `N_X`, `N_MU`, `N_MAX`, `SHIFT_START`, `SHIFT_TRAVEL`, `PULSE_WIDTH`, `VARIANCE_MIN` and `VARIANCE_RANGE` set the grids and the families.

## Usage

```bash
python main.py                          # print the errors and show the figure
python main.py --no-show --output .     # save rom_n_width_decay.png in the current directory
```

## Output

![Singular values and projection errors of three solution families](rom_n_width_decay.png)

For the diffusing pulse $\sigma_{10}/\sigma_1 = 8.4 \times 10^{-6}$ and five modes already give a worst-case error of 2%; the error reaches $10^{-12}$ at $N = 20$. The translating pulse travels 0.6 m, twelve widths, and the error stays near 79% at $N = 5$ and is still 0.7% at $N = 20$ before it falls to round-off. The translating step follows the $N^{-1/2}$ line throughout: 36% at $N = 5$, 17% at $N = 20$ and 5.7% at $N = 100$, where the snapshot matrix has only 400 columns. A linear ROM of a flow with a moving shock therefore needs hundreds of modes for a few per cent accuracy, which is the motivation for nonlinear-manifold, shifted-basis and local reduced-order models.

## Related Notes

- [Reduced-Order Modeling](../../../notes/numerical/rom/rom.md)
- [Reduced Basis Approximation](../../../notes/numerical/rom/reduced_basis_approximation.md)
- [Dynamic Mode Decomposition as a Reduced-Order Model](../../../notes/numerical/rom/dmd.md)
