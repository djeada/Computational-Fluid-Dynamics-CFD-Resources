# Learned Mixing-Length Closure

This script learns a near-wall correction to Prandtl's mixing length from reference velocity data, then inserts the learned closure into a 1D RANS solver to check whether a good fit to the closure data also gives a good velocity profile. Spalding's law of the wall stands in for DNS data; the figure compares the a priori fits of the damping function with the a posteriori RANS solutions $u^+(y^+)$ on a logarithmic axis.

## Overview

- Uses Spalding's law ($\kappa = 0.41$, $B = 5.2$) as the reference profile $u^+_{\mathrm{ref}}(y^+)$ in the constant-stress inner layer.
- Computes the eddy viscosity, mixing length and van Driest damping function implied by the reference profile.
- Fits two closures to the implied damping at 60 log-spaced points in $1 \leq y^+ \leq 100$: a van Driest damping with one learned constant $A^+$ (`scipy.optimize.least_squares`) and an unconstrained cubic polynomial in $\ln y^+$ (`numpy.polyfit`).
- Integrates the RANS momentum equation from the wall to $y^+ = 1000$ with `scipy.integrate.solve_ivp` for plain Prandtl mixing length, the learned van Driest closure and the polynomial closure.
- Prints and tabulates the a priori error (in the damping function, on the training range) and the a posteriori error (in $u^+$, inside and beyond the training range), and the error of van Driest's original $A^+ = 26$ for comparison.

## Mathematical Background

### RANS Momentum Equation in the Inner Layer

For fully developed flow near a wall the mean momentum equation in wall units is

```math
\frac{d}{dy^+}\left[(1 + \nu_t^+)\frac{du^+}{dy^+}\right] = 0, \qquad u^+(0) = 0, \qquad \left.\frac{du^+}{dy^+}\right|_{0} = 1
```

so the total stress is constant: $`(1 + \nu_t^+)\,du^+/dy^+ = 1`$. Here $u^+ = U/u_\tau$, $y^+ = y u_\tau/\nu$ and $\nu_t^+ = \nu_t/\nu$.

### Mixing-Length Closure

Prandtl's model sets $`\nu_t^+ = (\ell^+)^2\,du^+/dy^+`$ with $\ell^+ = \kappa y^+ D(y^+)$, where $D$ is a damping function ($D = 1$ in the plain model). Substituting into the constant-stress equation gives a quadratic for the velocity gradient $g = du^+/dy^+$:

```math
(\ell^+)^2 g^2 + g - 1 = 0 \quad\Rightarrow\quad g = \frac{2}{1 + \sqrt{1 + 4(\ell^+)^2}}
```

The van Driest form is $`D = 1 - e^{-y^+/A^+}`$.

### Closure Data Implied by the Reference

Spalding's law gives $y^+$ explicitly as a function of $u^+$:

```math
y^+ = u^+ + e^{-\kappa B}\left[e^{\kappa u^+} - 1 - \kappa u^+ - \frac{(\kappa u^+)^2}{2} - \frac{(\kappa u^+)^3}{6}\right]
```

Inverting the constant-stress relation, the data imply $`\nu_t^+ = dy^+/du^+ - 1`$, then $`\ell^+ = \sqrt{\nu_t^+(1 + \nu_t^+)}`$ and $D = \ell^+/(\kappa y^+)$. These are the training targets.

### A Priori and A Posteriori Errors

The a priori error compares the closure with its training target, here $\max |D_{\mathrm{model}} - D_{\mathrm{data}}|$ on $1 \leq y^+ \leq 100$. The a posteriori error compares the solution of the RANS equation that uses the closure with the reference, here $\max |u^+ - u^+_{\mathrm{ref}}|$. Because $u^+$ is the integral of $g$, local closure errors accumulate, and a closure evaluated outside its training range enters the solution without any warning.

## Implementation

- `spalding_y_plus` evaluates Spalding's law, `reference_u_plus` inverts it by Newton iteration and `reference_eddy_viscosity_u` gives $\nu_t^+$ as a function of $u^+$.
- `implied_closure(y_plus)` returns the data-implied $\nu_t^+$, $\ell^+$ and $D$.
- `velocity_gradient(mixing_length)` solves the quadratic for $g$, and `solve_rans(damping, y_plus)` integrates $du^+/dy^+ = g$ from the wall for any damping function.
- `fit_van_driest` and `fit_polynomial` build the two learned closures, and `build_closures` returns them with the plain model.
- `TRAIN_RANGE`, `N_TRAIN`, `Y_PLUS_MAX` and `POLY_DEGREE` set the training data, the solution range and the polynomial degree.

## Usage

```bash
python main.py                          # show the figure
python main.py --no-show --output .     # save the figure as a PNG in the current directory
```

## Output

![Learned mixing-length closures: damping fits and RANS solutions](learned_mixing_length_closure.png)

The learned van Driest constant is $A^+ = 24.83$, close to van Driest's 26. The table in panel (d) gives the errors:

| Closure | A priori $\max \lvert \Delta D \rvert$, $1 \leq y^+ \leq 100$ | $\max \lvert \Delta u^+ \rvert$, $y^+ \leq 100$ | $\max \lvert \Delta u^+ \rvert$, $y^+ \leq 1000$ |
| --- | --- | --- | --- |
| Prandtl, $D = 1$ | 0.939 | 6.23 | 6.43 |
| van Driest, $A^+ = 24.83$ | 0.076 | 0.21 | 0.21 |
| Cubic in $\ln y^+$ | 0.048 | 0.19 | 3.08 |

Without damping, the eddy viscosity is far too large in the buffer layer, and $u^+$ ends up about 6.4 too low throughout the log layer. The cubic polynomial fits the training data better than the van Driest form and gives a slightly better profile up to $y^+ = 100$, but beyond the training range its damping first exceeds 0.9 and then falls towards 0.2 at $y^+ = 1000$, so the predicted profile rises above the log law, with an error of 3.1. The one-parameter van Driest form has the right limit $D \to 1$ built in and keeps its 0.21 error out to $y^+ = 1000$. With $A^+ = 26$ the maximum error is 0.41.

## Related Notes

- [Machine-Learned Turbulence Closures](../../../notes/machine_learning/flow/ml_turbulence_closures.md)
- [Turbulence Modeling](../../../notes/fluid_mechanics/turbulence/modeling.md)
- [RANS Equations](../../../notes/fluid_mechanics/turbulence/rans_equations.md)
