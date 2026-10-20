# RBF Shape Parameter Trade-Off

This script sweeps the shape parameter $\varepsilon$ of Gaussian and multiquadric radial basis function interpolants of Franke's 2D test function and plots the true error, Rippa's leave-one-out cross-validation (LOOCV) estimate of it, and the condition number of the interpolation matrix. It shows why $\varepsilon$ cannot simply be made small for accuracy, and how the LOOCV curve picks a usable value from the data alone, which is what one has when the function is a CFD response.

## Overview

- Places 50 scrambled Halton points in $[0, 1]^2$ (seed 3) and samples Franke's function there.
- For 80 log-spaced values $\varepsilon \in [0.3, 30]$ and the Gaussian and multiquadric kernels, solves the interpolation system $A\mathbf{c} = \mathbf{y}$ with `numpy.linalg.solve`.
- Records the RMS error on a $60 \times 60$ test grid, the RMS of the LOOCV residuals from Rippa's formula, and $\mathrm{cond}_2(A)$.
- Draws the function with the points, the two error curves per kernel with the LOOCV minimum marked, and the condition numbers against $1/\epsilon_{\mathrm{mach}} \approx 4.5 \times 10^{15}$.

## Mathematical Background

### Interpolant

```math
s(x) = \sum_{j=1}^{N} c_j\,\varphi(\|x - x_j\|),
\qquad A_{ij} = \varphi(\|x_i - x_j\|),
\qquad A\mathbf{c} = \mathbf{y}
```

with $\varphi(r) = e^{-(\varepsilon r)^2}$ (Gaussian, positive definite) or $\varphi(r) = \sqrt{1 + (\varepsilon r)^2}$ (multiquadric, nonsingular for distinct points by Micchelli's theorem). Small $\varepsilon$ makes the kernels flat, the columns of $A$ nearly parallel and $A$ ill-conditioned. Large $\varepsilon$ makes them narrow peaks; $A$ tends to the identity for the Gaussian, and the interpolant falls back toward zero between points.

### Rippa's LOOCV Formula

Let $s^{(-i)}$ be the interpolant built without point $i$. Rippa (1999) showed that the leave-one-out residual needs no refitting:

```math
e_i = y_i - s^{(-i)}(x_i) = \frac{c_i}{(A^{-1})_{ii}}
```

so all $N$ residuals cost one inverse instead of $N$ solves. The cost function is $`\|\mathbf{e}\|_2/\sqrt{N}`$. The script also contains a brute-force version, `brute_force_loocv`, which the tests use to check the formula.

## Implementation

- `franke(x, y)` is the test function, `make_data(seed)` builds the points and the test grid.
- `KERNELS` maps each kernel name to $\varphi(r, \varepsilon)$, and `distance_matrix(a, b)` returns pairwise distances.
- `rippa_loocv(a, y)` and `brute_force_loocv(a, y)` compute the LOOCV residuals.
- `sweep(...)` returns the true error, the LOOCV error and the condition number for every $\varepsilon$.
- `make_figure(...)` draws the three panels. `N_CENTRES`, `N_GRID`, `EPS_MIN`, `EPS_MAX`, `N_EPS` and `SEED` set the experiment.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Franke function with 50 Halton points, RBF error and LOOCV estimate against the shape parameter, and the condition number of the RBF matrix](rbf_shape_parameter_tradeoff.png)

For the Gaussian kernel the smallest true RMS error is $1.79 \times 10^{-2}$ at $\varepsilon = 4.6$, where $\mathrm{cond}(A) = 8.3 \times 10^{3}$. At $\varepsilon = 30$ the matrix is almost the identity (condition number 1.1) and the error is 0.43, while below $\varepsilon \approx 1$ the condition number passes $1/\epsilon_{\mathrm{mach}}$ and the error curves become erratic because round-off dominates the solve. The multiquadric behaves the same way, with its best error $1.27 \times 10^{-2}$ at $\varepsilon = 7.4$.

The dashed LOOCV curves run parallel to the true errors. Their minima are at $\varepsilon = 3.9$ (Gaussian) and 3.5 (multiquadric), where the true errors are $2.6 \times 10^{-2}$ and $1.96 \times 10^{-2}$, within a factor 1.6 of the best possible, found without evaluating the function anywhere else.

## Related Notes

- [Radial Basis Functions](../../../notes/numerical/surrogates/radial_basis_functions.md)
- [Surrogate Models in CFD](../../../notes/numerical/surrogates/intro.md)
