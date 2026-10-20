# Fourier Neural Operator Layer in 1D

This script learns the solution operator $G: f \mapsto u$ of the periodic problem $-\nu u'' + u = f$ from 200 random forcing–solution pairs with a single spectral convolution, the linear part of a Fourier neural operator (FNO) layer, fitted by least squares. The learned weights match the exact Fourier multiplier, and the layer trained on a 64-point grid predicts solutions on grids of up to 2048 points with the same error, which is the discretization invariance that distinguishes neural operators from grid-bound surrogates.

## Overview

- Draws 200 random real forcings with Fourier modes $k \le 31$ and spectrum $|f_k| \propto (1 + (k/8)^2)^{-1}$, samples them on a 64-point grid, and computes the exact solutions.
- Adds Gaussian noise with standard deviation $`10^{-3}\,\mathrm{std}(u)`$ to the training solutions.
- Fits one complex weight $R_k$ per retained mode $0 \le k \le K$ by linear least squares, for $`K \in \{4, 8, 16, 31\}`$.
- Draws one unseen forcing with modes up to $k = 48$, above the Nyquist mode of the training grid, and evaluates the learned layer on grids of 128 to 2048 points without retraining.
- Prints the maximum relative error of the learned weights and the zero-shot relative $L^2$ error on each grid, and draws a $2 \times 2$ figure.

## Mathematical Background

### Solution Operator

On the periodic unit interval, write $f(x) = \sum_k \hat f_k e^{2\pi i k x}$. Since the second derivative of $e^{2\pi i k x}$ is $-(2\pi k)^2 e^{2\pi i k x}$, the solution of $-\nu u'' + u = f$ is

```math
\hat u_k = m(k)\, \hat f_k,
\qquad m(k) = \frac{1}{1 + \nu (2\pi k)^2}
```

The operator is linear and translation invariant, so it is a convolution, diagonal in Fourier space, with symbol $m(k)$.

### Spectral Convolution Layer

An FNO layer maps a function $v$ to $\sigma\left(W v + \mathcal{F}^{-1}[R \cdot \mathcal{F} v]\right)$, where $\mathcal{F}$ is the discrete Fourier transform, $R_k$ are learned complex weights for the lowest $K$ modes and are zero above them, $W$ is a pointwise linear map and $\sigma$ is a nonlinearity. With one channel, no $W$ and no $\sigma$ the layer is

$$
(\mathcal{K}_R f)(x) = \sum_{|k| \le K} R_k \hat f_k e^{2\pi i k x}
$$

and the exact operator truncated to $K$ modes is the case $R_k = m(k)$.

### Least-Squares Fit

Given pairs $`\{(f_i, u_i)\}_{i=1}^{n}`$ with Fourier coefficients $`\hat f_{ik}`$ and $\hat u_{ik}$, the loss $\sum_i \sum_{k \le K} |\hat u_{ik} - R_k \hat f_{ik}|^2$ decouples over modes, and each weight has the closed form

```math
R_k = \frac{\sum_i \overline{\hat f_{ik}}\, \hat u_{ik}}{\sum_i |\hat f_{ik}|^2}
```

In a full FNO the layer is followed by a nonlinearity and stacked, so the weights are found by gradient descent instead; the linear case isolates the spectral part.

### Discretization Invariance

The weights $R_k$ are attached to wavenumbers, not to grid points. Evaluating the layer on a grid of $N > 2K$ points uses the same $R_k$, and for a forcing defined as a function (not as a vector on one grid) the prediction is the same function on every grid fine enough to represent the forcing.

## Implementation

- `exact_multiplier(k)` returns $m(k)$ with `NU = 0.01`.
- `random_coefficients(rng, n_samples, k_max)` draws the complex Fourier coefficients of real random forcings.
- `synthesize(coef, n)` samples the corresponding function on $n$ points with an inverse real FFT, and refuses grids that would alias mode `k_max`.
- `solve_exact(coef)` multiplies the coefficients by $m(k)$.
- `fit_spectral_weights(f, u, n_modes)` computes $R_k$ in closed form; `spectral_convolution(weights, f)` applies the layer on any grid.
- `make_training_set(rng)` builds the noisy training pairs; `zero_shot_errors(weights, test_coef)` returns the relative $L^2$ error on every grid in `EVAL_GRIDS`.
- [`tests/test_neural_operator_pinn_ml.py`](../../../tests/test_neural_operator_pinn_ml.py) checks that a noise-free fit recovers $m(k)$ to $10^{-10}$, that the noisy fit matches the first 17 modes to 1 %, and that the zero-shot error is below $10^{-2}$ and identical on every grid.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Learned Fourier multiplier, unseen forcing, prediction and zero-shot error versus grid size](fourier_neural_operator_1d.png)

The script prints:

| $K$ | max relative weight error | zero-shot relative $L^2$ error (all grids) |
| --- | --- | --- |
| 4 | $9.6 \times 10^{-5}$ | $8.5 \times 10^{-2}$ |
| 8 | $9.5 \times 10^{-4}$ | $1.8 \times 10^{-2}$ |
| 16 | $6.7 \times 10^{-3}$ | $1.5 \times 10^{-3}$ |
| 31 | $9.6 \times 10^{-2}$ | $3.4 \times 10^{-4}$ |

The top-left panel shows the learned weights on top of the exact symbol for $K = 16$; their imaginary parts, which should be zero, are below $10^{-4}$. The bottom-left panel shows the prediction for the unseen forcing (top right) on the 2048-point grid and, as circles, on the 128-point grid; both follow the exact solution with a relative error of $1.5 \times 10^{-3}$. The bottom-right panel is flat: the error depends on the number of retained modes, not on the evaluation grid. For small $K$ the error is the energy of the discarded modes; for $K = 31$ the high modes are fitted mainly to noise (their signal $m(k)|\hat f_k|$ is below $10^{-3}$ of the low modes), so the weight error grows to 10 % but those modes contribute little to $u$.

## Related Notes

- [Neural Operators](../../../notes/machine_learning/neural_networks/neural_operators.md)
