## Deformation Parameters in Automotive Aerodynamics

Understanding how geometry changes affect aerodynamic performance requires a systematic way to define and vary shape modifications. Without parametric control, design exploration becomes ad-hoc, difficult to reproduce, and nearly impossible to scale across large design spaces. Deformation parameters address this by providing a structured numeric framework for shape variation that integrates directly with CAD tools, CFD solvers, and machine learning pipelines. This makes them indispensable for modern automotive aerodynamic development.

In the search for improved vehicle efficiency and performance, engineers commonly employ **deformation parameters**—numeric descriptors that systematically modify geometric features. This strategy allows controlled exploration of design changes to the bonnet (hood), intakes, windscreen, and rear geometry, among others. Each parameter directly influences how air flows around and under the car, making them a key tool in both simulation-based and experimental aerodynamic studies. By shifting, tilting, or extending elements in a precise manner, aerodynamicists can gauge the effect of individual modifications on drag, lift, and overall flow structures.

Parametric approaches often integrate with **computer-aided design (CAD)** software and **automatic meshing routines**, ensuring consistency from shape generation to CFD (computational fluid dynamics) analysis. Yet, implementing large deformations requires caution: overly aggressive parameter values risk geometry self-intersections or unphysical mesh distortions. Therefore, robust design-of-experiments (DoE) frameworks typically confine parameter ranges to maintain realistic configurations and reliable simulation quality.

```
                Original CAD Model
                  +-----------+
                  |           |
                  |  Baseline |
                  |  Geometry |
                  +-----+-----+
                        |
                        | Apply Deformation Parameters
                        v
  +------------------------------------------------+
  | Deformation Engine (Parameter-based Adjustments)|
  |                                                |
  |   - Bonnet LE Z-pos       - Ride Height (Pitch)|
  |   - Ramp Angle            - Windscreen Angle    |
  |   - Intakes Z-extension   - etc.               |
  +------------------------------------------------+
                        |
                        v
                Updated Geometry
                 (Ready for Meshing)
```

Each parameter triggers a local (e.g., bonnet LE only) or global (e.g., entire body pitch) transformation. Afterward, the updated shape goes through **mesh generation**, followed by **CFD** or wind tunnel evaluations.

### Modern Parametric Workflow

I. **Parametric Definitions**: Assign numerical bounds and increments (or continuous ranges) for each deformation parameter, e.g. $`\pm 20\%`$ around the baseline.

II. **Geometry Updates**: Apply transformations to the baseline CAD model, ensuring feature continuity, smooth surfaces, and minimal distortion.

III. **Mesh Generation**: Re-mesh or adapt the existing mesh to the new geometry. Some workflows use advanced morphing techniques to update an existing mesh incrementally, while others re-generate a fresh volume or surface mesh.

IV. **CFD Simulation**: Solve the Reynolds-averaged Navier–Stokes (RANS), large eddy simulation (LES), or other suitable flow model on each deformed geometry.

V. **Data Storage and Analysis**: Record integral quantities (e.g., $C_d$, $C_l$) and field data for each geometry. This dataset can populate machine learning models, shape optimizers, or design trade-off studies.

### Deformation Parameters

Automotive geometry is typically segmented into distinct zones (front fascia, cabin, underbody, rear deck, etc.). The parameters below represent common modifications, though the full list can vary with vehicle category and design goals.

#### 1. Bonnet LE Z-Position

- Vertical shift of the bonnet (hood) leading edge.
- Small variations can adjust air intake at the grille, flow attachment on the hood, and frontal area.
  - Raising might facilitate cooling airflow or engine packaging but can increase drag.
  - Lowering may improve flow attachment but reduce under-hood space.

#### 2. Upper Intake Z-Extension

- Vertical stretch or relocation of the upper grille or intake inlet.
- Controls airflow distribution to radiators, intercoolers, or electric powertrain components.
  - Larger intake area promotes cooling yet risks aerodynamic penalties if poorly integrated.
  - Excess vertical extension may raise stagnation pressure and drag near the front fascia.

#### 3. Lower Intake Z-Extension

- Vertical shift of the lower intake or grille region.
- Balances air entering below the bumper with underbody flow management (e.g., splitters).
  - Subtle changes here can alter drag, front lift, and cooling.
  - Interactions with ride height or undertray geometry can either be beneficial or detrimental to performance.

#### 4. Ramp Angle

- An inclination (ramp) near the hood–windshield transition, sometimes behind the engine bay.
- Affects the flow’s ability to remain attached over the hood, impacting local turbulence and drag.
  - A gentle slope reduces risk of flow separation but can enlarge frontal area.
  - A steeper slope might produce local separation or higher turbulence levels, affecting the A-pillar region.

#### 5. Windscreen Angle

- The inclination of the windshield (windscreen) relative to a horizontal or vertical reference.
- A shallower windscreen angle often decreases drag by streamlining the roof transition.
  - Extreme angles might cause strong vortex formations along A-pillars, raising noise levels or localized drag.
  - Interior constraints (visibility, ergonomics) typically limit how steep or shallow this angle can be.

#### 6. Ride Height – Pitch Angle (Y-Rotation)

- Tilting the vehicle about the lateral (y-axis) axis, so the front or rear is higher relative to the other end.
- Adjusts underbody flow acceleration and overall aerodynamic balance (e.g., front vs. rear downforce).
  - Nose-up pitch can create suction under the rear, beneficial for some race-car configurations but risky for stability.
  - Nose-down pitch might reduce drag in some contexts but can increase front lift if not managed properly.

#### 7. Ride Height – Ground Clearance (Z-Translation)

- Shifting the entire vehicle up or down relative to the ground plane.
- Affects underbody volume and velocity distribution, crucial for generating or mitigating downforce.
  - Lowering can reduce drag or boost downforce, but real-world practicality (speed bumps, road irregularities) becomes a concern.
  - Higher ride height might soften ground effect but could also ease cooling airflow or reduce aerodynamic sensitivity.

#### 8. Battery Pack Z-Position (for EVs and Hybrids)

- Vertical placement of the underfloor battery pack.
- Balances aerodynamic efficiency with center-of-gravity concerns and underbody packaging.
  - Lower battery packs free up interior space but reduce underbody airflow, possibly increasing drag.
  - Higher packs help generate a smoother underbody airflow at the expense of less cabin space or higher CG.

#### 9. Rear Window Angle

- The slope of the rear windshield.
- Shapes the wake region, potentially reducing base drag if flow remains attached longer.
  - A gradual slope can limit the size of the recirculation zone.
  - A sudden angle can induce a well-defined separation bubble, sometimes helping reduce drag (e.g., “fastback” designs) but often adding complexity.

#### 10. Rear Window Length

- The horizontal extent of the rear windshield (how far it extends before meeting the trunk lid).
- Governs how quickly the flow transitions from roofline to trunk, influencing rear pressure recovery.
  - Longer can reduce abrupt flow separation but raises manufacturing costs or length constraints.
  - Shorter is compact but can accelerate wake formation and increase drag.

#### 11. Trunk Lid Angle

- The orientation of the trunk or rear deck relative to the horizontal plane.
- Adjusts trailing edge detachment, altering base pressure and lift distribution.
  - An upward tilt might provide a spoiler-like effect, raising downforce but also drag.
  - A downward tilt can enhance streamlining at the cost of decreased rear grip.

#### 12. Trunk Length

- The longitudinal extent of the trunk or rear overhang.
- Affects how smoothly the roof flow merges with the base of the car, influencing rear-end wake.
  - Longer trunk designs reduce sharp flow gradients, but add weight and length constraints.
  - Shorter trunks can be sportier or more compact, yet risk increasing flow separation.

#### 13. Diffuser Angle

- The slope of the rear diffuser located under the car.
- Helps expand and slow underbody flow for increased static pressure recovery, often improving downforce.
  - Overly steep angles prompt flow separation, undermining the diffuser’s benefits.
  - Too shallow yields limited pressure recovery, underutilizing underbody aerodynamics.

### Validation and Optimization

After each deformation:

I. **CFD Simulation**

- RANS or LES calculations estimate the aerodynamic response ($C_d$, $C_l$, wake patterns, etc.).
- Data is stored in a parametric database for correlation with deformation settings.

II. **Wind Tunnel or Road Tests**

- When available, physical prototyping or scaled models validate the parametric results.
- Discrepancies highlight potential modeling gaps (e.g., turbulence assumptions, neglected thermal effects).

III. **Optimization Loop**

- **Gradient-based or heuristic** (e.g., genetic algorithms) methods search for parameter combinations yielding minimal drag, suitable downforce, or balanced performance. For gradient-based approaches, the sensitivity of an aerodynamic objective $J$ (e.g., $C_d$) with respect to a deformation parameter $p_k$ is approximated as:

$$
\frac{\partial J}{\partial p_k} \approx
\frac{J(\mathbf{p} + \delta \mathbf{e}_k) - J(\mathbf{p})}{\delta}
$$

where $\mathbf{e}_k$ is the unit vector in the $k$-th parameter direction and $\delta$ is a small perturbation. Adjoint methods compute all such sensitivities simultaneously at a cost independent of the number of parameters, making them highly efficient for high-dimensional design spaces.

- **ML Surrogates**: Regression or graph-based neural networks learn from the parametric dataset, predicting aerodynamics without re-running full CFD. Once trained, these surrogates evaluate thousands of candidate designs per second, enabling exhaustive searches that would be infeasible with direct CFD.

### Setting Up the Problem

To define and use deformation parameters in your own project, follow these high-level steps:

1. **Identify geometric regions of interest.** Focus on areas with the greatest aerodynamic influence—front fascia, underbody, rear deck, and diffuser are common starting points.
2. **Define parameters and ranges.** For each region, select measurable quantities (angles, positions, lengths) and bound them using engineering constraints such as packaging limits, manufacturing tolerances, and regulatory requirements.
3. **Automate geometry updates.** Connect your parametric definitions to a CAD kernel or mesh morphing tool so that each parameter combination produces a valid, watertight geometry without manual intervention.
4. **Design a sampling plan.** Use a design-of-experiments (DoE) strategy—Latin hypercube sampling, Sobol sequences, or full factorial designs—to efficiently cover the parameter space while keeping the total number of CFD runs manageable.
5. **Run CFD evaluations.** Execute simulations for every sample point, recording both integral quantities ($C_d$, $C_l$) and field data (pressure, velocity) in a structured database.
6. **Train ML surrogate models.** Feed the resulting dataset into regression models, neural networks, or Gaussian processes to build a fast surrogate that maps parameter vectors to aerodynamic responses.
7. **Iterate and refine.** Use the surrogate to identify promising regions, add targeted CFD samples there, retrain, and repeat until the model accuracy meets your optimization needs.

Keeping each step scripted and version-controlled ensures reproducibility and makes it straightforward to extend the study with additional parameters or higher-fidelity simulations later.

### Key Takeaways

- Deformation parameters convert subjective shape changes into a **structured, repeatable numeric framework** suitable for automated workflows.
- Each parameter targets a specific geometric region, enabling engineers to **isolate and quantify** the aerodynamic effect of individual design modifications.
- Robust **DoE strategies** and bounded parameter ranges are essential to avoid unphysical geometries and ensure simulation reliability.
- Automated CAD-to-CFD pipelines eliminate manual rework, making it practical to evaluate **hundreds or thousands** of design variants.
- The parametric dataset produced by CFD evaluations serves as training data for **ML surrogate models**, dramatically accelerating design exploration.
- Combining surrogate predictions with optimization algorithms enables **rapid convergence** toward designs that balance drag, downforce, and other performance targets.

### Related Scripts

- [Design Space Distribution via Sobol Sequences](../../../scripts/plots/design_space_distribution/): draws a four-dimensional scrambled Sobol design of 512 geometry variants and plots two 2D projections of it, showing how evenly a low-discrepancy sequence covers a design space.

### Exercises

**Exercise 1.** At the baseline windscreen angle a CFD run gives $J = C_d = 0.310$. Increasing the windscreen angle parameter by $\delta = 1^\circ$ gives $C_d = 0.3065$. Estimate $\partial J / \partial p_k$ with the forward-difference formula from the note and predict $C_d$ for a $3^\circ$ increase. Why should this prediction be checked with CFD?

<details>
<summary>Answer</summary>

```math
\frac{\partial J}{\partial p_k} \approx \frac{0.3065 - 0.310}{1} = -0.0035
\text{ per degree}
```

The linear prediction for $+3^\circ$ is $0.310 + 3(-0.0035) = 0.2995$.

The forward difference is only first-order accurate, and the linear extrapolation assumes the response stays smooth. The note points out that extreme windscreen angles can trigger strong A-pillar vortices, so the drag response may bend or reverse over a few degrees. The prediction is a hint about direction, not a result.

</details>

**Exercise 2.** The note lists 13 deformation parameters. Each CFD run takes 6 hours, and a gradient-based optimization needs 20 design iterations. Compare the cost of computing gradients with forward differences, central differences, and an adjoint method (assume the adjoint solve costs about one primal solve).

<details>
<summary>Answer</summary>

- Forward differences: 1 baseline plus 13 perturbed runs, so 14 runs per iteration and $14 \times 20 \times 6 = 1680$ h.
- Central differences: 2 runs per parameter plus the baseline for the objective value, so 27 runs per iteration and $27 \times 20 \times 6 = 3240$ h.
- Adjoint: 1 primal plus 1 adjoint solve per iteration, so $2 \times 20 \times 6 = 240$ h.

The adjoint cost does not depend on the number of parameters, which is why it dominates when there are many parameters and only a few objectives.

</details>

**Exercise 3.** An engineer proposes a full-factorial DoE with 3 levels for each of the 13 parameters. How many CFD runs is that, and how long would it take at 1 hour per run in serial? Suggest a practical alternative for building a surrogate.

<details>
<summary>Answer</summary>

$3^{13} = 1{,}594{,}323$ runs. At 1 h each that is about 1.59 million hours, or roughly 182 years in serial. It is infeasible even on a large cluster.

A space-filling design such as Latin hypercube or Sobol sampling is the practical choice. A common rule of thumb is about 10 samples per parameter, around 130 runs here, followed by adaptive infill samples where the surrogate is uncertain or where optimal designs are predicted.

</details>

**Exercise 4.** The trunk length has a baseline of 800 mm and is allowed to vary by $`\pm 20\%`$. For surrogate training all parameters are scaled to $[0, 1]$. What physical trunk length corresponds to a normalized value of 0.25, and why is this normalization useful when the parameters mix angles and lengths?

<details>
<summary>Answer</summary>

The range is $[640, 960]$ mm. A normalized value of 0.25 maps to $640 + 0.25 \times 320 = 720$ mm.

Normalization puts angles (degrees) and lengths (millimetres) on comparable scales. Without it, distance-based methods such as Gaussian processes and k-nearest neighbours are dominated by whichever parameter has the largest numerical range, and neural-network training becomes poorly conditioned. The same scaling must be stored and applied to new designs at prediction time.

</details>

**Exercise 5.** The CFD objective has iterative-convergence noise of amplitude $\eta = 10^{-4}$, and $|J''| \approx 2 \times 10^{-4}$ per degree squared. The forward-difference error is roughly $E(\delta) = |J''|\delta/2 + 2\eta/\delta$. Find the step $\delta$ that minimizes this error and the minimum error, and compare with $\delta = 0.1^\circ$ and $\delta = 5^\circ$.

<details>
<summary>Answer</summary>

Setting $dE/d\delta = |J''|/2 - 2\eta/\delta^2 = 0$ gives

```math
\delta^* = 2 \sqrt{\frac{\eta}{|J''|}} = 2 \sqrt{\frac{10^{-4}}{2 \times 10^{-4}}}
\approx 1.41^\circ
```

with minimum error $E^* = 2\sqrt{\eta |J''|} \approx 2.83 \times 10^{-4}$ per degree.

For comparison, $E(0.1^\circ) = 2.01 \times 10^{-3}$ (noise dominates) and $E(5^\circ) = 5.4 \times 10^{-4}$ (truncation dominates).

Even at the best step the error is about 8% of the sensitivity found in Exercise 1. Converging the solver more tightly (smaller $\eta$) is the only way to do much better.

</details>

### References

- Hucho, W.-H. (Ed.), *Aerodynamics of Road Vehicles*, 4th ed., SAE International, 1998.
- Katz, J., *Automotive Aerodynamics*, Wiley, 2016.
- Jameson, A., "Aerodynamic design via control theory", *Journal of Scientific Computing* 3(3), 1988.
- Nocedal, J., & Wright, S. J., *Numerical Optimization*, 2nd ed., Springer, 2006.
- Forrester, A. I. J., Sóbester, A., & Keane, A. J., *Engineering Design via Surrogate Modelling: A Practical Guide*, Wiley, 2008.
