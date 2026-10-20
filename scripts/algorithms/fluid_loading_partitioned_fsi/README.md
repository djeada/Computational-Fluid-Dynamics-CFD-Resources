# Partitioned Fluid–Structure Coupling and the Added-Mass Instability

This script couples a structure solver and a fluid solver through their interface in the Dirichlet–Neumann way used by partitioned FSI codes, and shows that explicit coupling becomes unstable once the added mass of the fluid exceeds the structural mass, whatever the time step, while implicit coupling with Aitken relaxation converges to the monolithic solution. The model is a tensioned membrane resting on a layer of incompressible fluid, small enough that every result can be checked against an exact modal analysis.

## Overview

- The structure is a membrane of mass $m_s$ per unit area and tension $T$ on $0 < x < L$ with fixed ends, discretised by second-order finite differences on 31 interior nodes and advanced with the Newmark average-acceleration rule.
- The fluid is an inviscid, incompressible layer of depth $H$ under the membrane with a rigid bottom and open ends ($p = 0$). For a given membrane acceleration the fluid solver returns the interface pressure from the exact potential-flow solution of each sine mode.
- Explicit (loosely coupled) scheme: one structure solve per step with the pressure of the previous step, then one fluid solve.
- Implicit (strongly coupled) scheme: sub-iterations within each step on the interface pressure, either unrelaxed, with a constant relaxation factor $\omega = 0.2$, or with Aitken's dynamic relaxation, to a residual of $10^{-8}$ relative to the first fluid response of the step.
- A monolithic reference solves the same discrete equations with the fluid added mass moved to the left-hand side.
- The membrane starts undeflected with a triangular velocity field peaking at 0.1 m/s at $x = 0.3L$, a crude slam.
- Default case: a 10 mm steel plate ($m_s = 78.5$ kg/m²) with a dry first frequency of 20 Hz over 0.2 m of water, time step 1 ms.

## Mathematical Background

### Fluid Operator and Added Mass

With velocity potential $\phi$, $\nabla^2\phi = 0$ in $0 < y < H$, $\partial\phi/\partial y = 0$ on the bottom, $\phi = 0$ at the open ends and $\partial\phi/\partial y = \dot w$ on the membrane, a membrane mode $w_j\sin(k_jx)$ with $k_j = j\pi/L$ produces the linearised interface pressure

```math
p_j = -\rho_f\frac{\coth(k_jH)}{k_j}\,\ddot w_j = -m_{a,j}\,\ddot w_j
```

so the fluid acts as a mode-dependent added mass $m_{a,j}$ per unit area, largest for the first mode. In nodal form $\mathbf{p} = -\mathbf{M}_A\ddot{\mathbf{w}}$ with $`\mathbf{M}_A = \mathbf{S}\,\mathrm{diag}(m_{a,j})\,\mathbf{S}^T`$, where $\mathbf{S}$ is the orthonormal discrete sine transform, which also diagonalises the finite-difference stiffness $\mathbf{K}$. The coupled problem is $`(m_s\mathbf{I} + \mathbf{M}_A)\ddot{\mathbf{w}} + \mathbf{K}\mathbf{w} = \mathbf{0}`$, whose natural frequencies are lowered by the factor $`\sqrt{m_s/(m_s + m_{a,j})}`$.

### Explicit Coupling

Writing the structure step as $`(m_s + \beta\Delta t^2 k)\,a^{n+1} = p - k\,\tilde w^{n+1}`$ with predictor $\tilde w^{n+1} = w^n + \Delta t v^n + \Delta t^2(\tfrac12 - \beta)a^n$ and the explicit fluid load $p = -m_a a^n$, each mode is a linear map of $(w, v, a)$. For $\beta = \tfrac14$, $\gamma = \tfrac12$ a sign-alternating solution ($\lambda = -1$) requires $w = v = 0$ and then $m_s a = m_a a$, so the stability boundary is exactly

```math
\frac{m_{a,j}}{m_s} = 1
```

independent of $\Delta t$ and of the stiffness. For large ratios the error in the acceleration grows by a factor close to $m_a/m_s$ per step.

### Implicit Coupling and Aitken Relaxation

Within a step, the unrelaxed iteration on the interface pressure has the iteration matrix $`-(m_s\mathbf{I} + \beta\Delta t^2\mathbf{K})^{-1}\mathbf{M}_A`$, with spectral radius $`\max_j m_{a,j}/(m_s + \beta\Delta t^2\lambda_j)`$. It diverges when this exceeds 1, and a smaller time step makes it worse. Relaxation $\mathbf{p}^{(i+1)} = \mathbf{p}^{(i)} + \omega_i\mathbf{r}^{(i)}$ with the residual $\mathbf{r}^{(i)} = \mathbf{p}_{\mathrm{fluid}}(\mathbf{p}^{(i)}) - \mathbf{p}^{(i)}$ converges for small enough constant $\omega$. Aitken's method updates the factor from the last two residuals (Küttler and Wall 2008):

```math
\omega_i = -\omega_{i-1}\,\frac{\mathbf{r}^{(i-1)}\cdot\left(\mathbf{r}^{(i)} - \mathbf{r}^{(i-1)}\right)}{\left|\mathbf{r}^{(i)} - \mathbf{r}^{(i-1)}\right|^2}
```

## Implementation

- `Membrane` builds the stiffness matrix and its eigenvalues; the tension is set from `DRY_FREQUENCY`.
- `sine_basis(n)` and `modal_added_mass(n, rho_f)` build $\mathbf{S}$ and $m_{a,j}$; `FluidLayer.pressure(a)` is the fluid solver.
- `NewmarkStructure.solve(state, pressure)` returns the new acceleration for an imposed pressure, and `update` applies the Newmark formulas.
- `coupled_step(structure, fluid, state, p_guess, method)` performs one step with `method` in `"explicit"`, `"fixed"`, `"constant"` or `"aitken"` and returns the residual history.
- `run(method, rho_f, ...)` advances `N_STEPS` steps; `monolithic(...)` is the reference.
- `explicit_amplification(mass_ratio, omega_dt)` is the spectral radius of the single-mode explicit scheme, used for the stability map.
- `iteration_factor(membrane, fluid)` is the spectral radius of the unrelaxed sub-iteration, and `wet_dry_ratio(rho_f)` solves the coupled eigenproblem.

## Usage

```bash
python main.py                         # print the results and show the figure
python main.py --no-show --output .    # save fluid_loading_partitioned_fsi.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The tension is 125.6 kN/m. The first-mode added mass is 571.6 kg/m² in water, 7.28 times the plate mass, and 0.69 kg/m² in air (ratio 0.0087). In water the unrelaxed sub-iteration factor is 7.25, so plain fixed-point iteration diverges (residual $5 \times 10^{50}$ after 60 iterations). Constant relaxation with $\omega = 0.2$ needs 60 iterations in the first step, Aitken 29. Over 400 steps Aitken needs 25 sub-iterations per step on average and reproduces the monolithic solution to $4 \times 10^{-9}$. Explicit coupling with $m_{a,1}/m_s = 0.5$ and 0.95 stays bounded for 400 steps; at 1.05 it grows slowly to 13.5 mm, at 1.5 it passes 10 m after 55 steps, and in water after 11 steps. In air explicit coupling is stable and differs from the monolithic solution by 2.6% of the peak deflection. In water the wet/dry frequency ratios of modes 1 to 4 are 0.347, 0.544, 0.643 and 0.702.

![Sub-iteration residuals, growth of explicit coupling, stability map and wet-to-dry frequency ratios for a membrane on a fluid layer](fluid_loading_partitioned_fsi.png)

Panel (a) compares the sub-iteration residuals within the first step in water. Panel (b) shows the running maximum deflection of explicit coupling for five added-mass ratios. Panel (c) is the spectral radius of the explicit scheme for one mode: the boundary at $m_a/m_s = 1$ is a horizontal line, so refining the time step never restores stability. Panel (d) compares the wet-to-dry frequency ratios of the coupled eigenproblem with $\sqrt{m_s/(m_s + m_{a,j})}$.

## Related Notes

- [Fluid–Structure Interaction: Coupling Methods](../../../notes/applied_mechanics/fluid_loading/fluid_structure_interaction.md)
- [Hydroelastic Applications](../../../notes/applied_mechanics/fluid_loading/hydroelastic_applications.md)
- [Fluid Loading on Structures](../../../notes/applied_mechanics/fluid_loading/intro.md)
