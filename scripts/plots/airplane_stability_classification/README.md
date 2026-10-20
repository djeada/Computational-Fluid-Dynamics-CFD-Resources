# Static and Dynamic Stability Classification

This script draws the static picture of stability (a ball in a bowl, on a hill and on a flat surface) and the five free responses of a second-order system, from non-oscillatory convergence to monotonic divergence, together with their eigenvalues in the complex plane. It shows that static stability is a statement about the sign of the stiffness alone, while dynamic stability depends on the real parts of the eigenvalues, so a statically stable system can still oscillate with growing amplitude.

## Overview

- Plots the potential energy $V(x) = \tfrac{1}{2}kx^2$ for $k = 1$, $-1$ and $0$, with a ball at the equilibrium, a displaced ball and the force $-dV/dx$ acting on it.
- Integrates $\ddot x + c\dot x + kx = 0$ from $x(0) = 1$, $\dot x(0) = 0$ for five $(c, k)$ pairs with the matrix exponential, over 12 s.
- Draws the exponential envelope $e^{\sigma t}$ of each oscillatory response, with $\sigma$ the real part of the eigenvalues.
- Labels each response with its static and dynamic classification, computed from the signs of $k$ and of the eigenvalues' real parts.
- Places all ten eigenvalues in one complex plane with the stable left half-plane shaded.

## Mathematical Background

A system with potential energy $V(x)$ has an equilibrium where $dV/dx = 0$. It is statically stable there if a small displacement produces a force back towards the equilibrium, i.e. $d^2V/dx^2 = k > 0$, statically unstable if $k < 0$ and neutral if $k = 0$.

The unit-mass oscillator $\ddot x + c\dot x + kx = 0$ has eigenvalues

```math
\lambda_{1,2} = -\frac{c}{2} \pm \sqrt{\frac{c^2}{4} - k}
```

and the free response is a combination of $e^{\lambda_1 t}$ and $e^{\lambda_2 t}$. The motion decays if both real parts are negative (dynamically stable), persists at constant amplitude if they are zero, and grows if any real part is positive. Complex eigenvalues ($c^2 < 4k$) give oscillation at the damped frequency $`\mathrm{Im}\,\lambda`$ inside the envelope $`e^{\mathrm{Re}\,\lambda\,t}`$.

| Case | $c$ (1/s) | $k$ (1/s²) | Eigenvalues | Static | Dynamic |
| --- | --- | --- | --- | --- | --- |
| Non-oscillatory convergence | 3 | 2 | $-1$, $-2$ | stable | stable |
| Damped oscillation | 0.5 | 4 | $-0.25 \pm 1.984j$ | stable | stable |
| Neutral oscillation | 0 | 4 | $\pm 2j$ | stable | neutral |
| Divergent oscillation | $-0.3$ | 4 | $0.15 \pm 1.994j$ | stable | unstable |
| Monotonic divergence | 0.5 | $-1$ | $0.781$, $-1.281$ | unstable | unstable |

## Implementation

- `CASES` holds the title, $c$ and $k$ of each system; `COLOURS` gives each one the same colour in every panel.
- `eigenvalues(c, k)` returns the roots of $\lambda^2 + c\lambda + k$; `free_response(c, k, t)` evaluates $e^{At}\mathbf{x}_0$ with `scipy.linalg.expm`.
- `classify(c, k)` returns the static class, the dynamic class and whether the response oscillates.
- `plot_static()` draws the three potential wells with matplotlib patches; `plot_dynamic()` draws the five responses and the eigenvalue plane.

## Usage

```bash
python main.py                          # print the eigenvalues and show both figures
python main.py --no-show --output .     # save the PNGs in the current directory
```

## Output

The script prints the eigenvalues in the table above.

![Static stability: bowl, hill and flat surface](airplane_static_stability.png)

In the bowl the force on the displaced ball points back to the bottom, on the hill it points away from the top, and on the flat surface there is none.

![Five free responses and their eigenvalues](airplane_dynamic_stability.png)

The first four systems all have $k = 2$ or $4 > 0$ and are statically stable, yet only the first two return to rest. The divergent oscillation has a restoring force but negative damping, which feeds energy into the motion each cycle. The eigenvalue panel shows that the dynamic class is read from the horizontal position of the eigenvalues alone, and oscillation from whether they leave the real axis.

## Related Notes

- [Static and Dynamic Stability of Oscillating Systems](../../../notes/applied_mechanics/transportation/airplanes/pecking.md)
- [Airplane Stability](../../../notes/applied_mechanics/transportation/airplanes/airplane_stability.md)
