# Grid Convergence Comparison

This script illustrates grid convergence by plotting the model numerical solutions $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4, 8, 16$ against the exact solution $u(x) = e^{-x}$ on $[0, 1]$. It also prints the maximum error for each $N$, which roughly halves each time $N$ doubles, as expected for a first-order method.

## Overview

- Plots the exact solution $u(x) = e^{-x}$ as a solid black curve.
- Overlays $u_N(x) = e^{-x(1 + x/N)}$ for $N = 4$ (red solid), $N = 8$ (blue dashed) and $N = 16$ (magenta dotted).
- Marks each $u_N$ at $x = 0, 0.25, 0.5, 0.75, 1$. These are the same five locations for every $N$.
- Prints $\max_x |u(x) - u_N(x)|$ on the 100-point plotting grid for each $N$, with the ratio to the previous $N$.

$u_N$ is a closed-form model of a first-order discretisation error, not the output of an actual finite-difference or finite-volume solver.

## Mathematical Background

### Exact Solution

$$
u(x) = e^{-x}
$$

### Model Numerical Solution

$$
u_N(x) = e^{-x\left(1 + x/N\right)} = e^{-x}\, e^{-x^2/N}
$$

The exponent differs from the exact one by $x^2/N$, so

$$
\lim_{N \to \infty} u_N(x) = u(x)
$$

### Error

$$
\varepsilon_N(x) = u(x) - u_N(x) = e^{-x}\left(1 - e^{-x^2/N}\right) \approx
\frac{x^2 e^{-x}}{N} \quad \text{for large } N
$$

so the error is $O(1/N)$ and doubling $N$ roughly halves it. On $[0, 1]$ the maximum error is at $x = 1$.

## Implementation

- `exact_solution(x)` and `numerical_solution(N, x)` evaluate $u$ and $u_N$.
- `max_errors(n_values, x)` returns the maximum absolute error for each $N$.
- `plot_comparison(x_fine, n_values)` draws the curves and markers.
- `N_VALUES`, `N_FINE`, `X_DISCRETE`, `LINE_STYLES` and `MARKER_COLORS` set the resolutions, the plotting grid, the marker locations and the styles.

## Usage

```bash
python main.py                          # print the errors and show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

The script prints:

```
N =  4: max |u - u_N| = 0.08137
N =  8: max |u - u_N| = 0.04323  (ratio to previous N: 1.88)
N = 16: max |u - u_N| = 0.02229  (ratio to previous N: 1.94)
```

![Graph comparing grid convergence](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/c86df1dd-ad03-4d61-908a-79c646821cab)

All curves start at $u = 1$ and lie below the exact solution. The gap is largest at $x = 1$ and shrinks as $N$ increases, and the error ratio approaches 2 as $N$ grows.

## Related Notes

- [CFD Process (Grid Convergence section)](../../../notes/numerical/cfd/cfd_process.md)
- [Finite Difference Discretization](../../../notes/numerical/fdm/discretization.md)
