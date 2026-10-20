# Deformation Parameters and Shape Morphing

A surrogate model of vehicle aerodynamics learns a map from a small set of numbers to the flow, so those numbers have to describe the geometry changes of interest completely, smoothly and without producing invalid shapes. In industrial studies they are usually morphing parameters applied to a baseline CAD surface and mesh: a bonnet edge moved up, a rear window tilted, the whole body lowered. This note describes the morphing methods that turn parameters into shapes, lists the 13 parameters used in this case study with their expected aerodynamic effects, and shows how sensitivity analysis, parameter correlations and constraints determine which parameters are worth keeping and how the design space should be sampled.

## Problem Statement

Let $\mathbf{X}_0 \in \mathbb{R}^{n \times 3}$ be the vertex coordinates of the baseline surface mesh. A parameterisation is a map from the design space $`\mathcal{P} = \prod_{k=1}^{d}[a_k, b_k] \subset \mathbb{R}^{d}`$ to deformed surfaces,

$$
\mathbf{X}(\mathbf{p}) = \mathbf{X}_0 + \mathbf{D}(\mathbf{p}),
\qquad \mathbf{D}(\mathbf{0}) = \mathbf{0}
$$

which must be smooth in $\mathbf{p}$ and in space, produce valid surfaces (no self-intersections, consistent with packaging constraints $g_j(\mathbf{p}) \le 0$) and, ideally, carry over to the volume mesh so that every variant is meshed consistently. The parameters must also be expressive: the shape changes that move the outputs should be reachable with small $d$.

Given such a parameterisation and an output $Y = C_d(\mathbf{p})$, the second task is to quantify how much each parameter and each group of parameters contributes to the variation of $Y$ over $\mathcal{P}$, so that unimportant parameters can be fixed and the sampling budget spent on the rest.

The difficulties are practical. Parameters that move the same surface region interact and may be nearly redundant. Valid ranges depend on each other (a longer trunk leaves less room for a longer rear window). And each evaluation of $C_d$ is a full CFD run, so sensitivity analysis on the CFD itself is limited to a few hundred evaluations and is usually done on a surrogate.

## Morphing Parameterisations

### Free-Form Deformation

Free-form deformation (Sederberg and Parry, 1986) embeds the region to be changed in a lattice of control points $\mathbf{P}_{ijk}$ and maps a point with lattice coordinates $(s, t, u)$ to

```math
\mathbf{X}(s, t, u) = \sum_{i=0}^{l}\sum_{j=0}^{m}\sum_{k=0}^{n} B_i^{l}(s)\,
B_j^{m}(t)\, B_k^{n}(u)\, \mathbf{P}_{ijk}
```

with Bernstein polynomials $B_i^{l}(s) = \binom{l}{i}s^i(1-s)^{l-i}$. A deformation parameter is a prescribed motion of a group of control points, for instance all points along the bonnet leading edge moved in $z$ by $p_1$. The surface displacement is linear in the control-point motions, and it is smooth and zero on the lattice boundary when the outer layers of control points are kept fixed, which blends the change into the unchanged body. The map remains locally invertible as long as the Jacobian determinant of $\mathbf{X}(s, t, u)$ stays positive.

### Radial-Basis-Function Morphing

RBF morphing prescribes displacements $\mathbf{d}_j$ at a set of control points $\mathbf{c}_j$ (some moved by the parameters, others held fixed) and interpolates them to every surface or volume node,

```math
\mathbf{d}(\mathbf{x}) = \sum_{j=1}^{M} \mathbf{w}_j\,
\varphi\!\left(\frac{\|\mathbf{x} - \mathbf{c}_j\|}{r}\right) + \mathbf{q}(\mathbf{x})
```

where $\mathbf{q}$ is a linear polynomial and the weights follow from the interpolation conditions $\mathbf{d}(\mathbf{c}_j) = \mathbf{d}_j$ together with the orthogonality conditions $\sum_j \mathbf{w}_j = \mathbf{0}$ and $\sum_j \mathbf{w}_j \mathbf{c}_j^T = 0$. A compactly supported basis such as the Wendland function $\varphi(\xi) = (1 - \xi)^4(4\xi + 1)$ for $\xi < 1$ and zero otherwise limits the influence to radius $r$ and makes the system sparse. Because the same interpolant can be evaluated at the nodes of the volume mesh, RBF morphing is also the standard way to deform a CFD mesh without remeshing (de Boer et al., 2007), which keeps the mesh topology identical across variants and gives node-to-node correspondence of the outputs. The interpolation itself is the same as in [Radial Basis Functions](../../numerical/surrogates/radial_basis_functions.md).

### Cage-Based Deformation

Cage-based methods enclose the part in a coarse closed polyhedron, the cage, and express every point as a weighted combination of the cage vertices $\mathbf{v}_k$ with generalised barycentric coordinates $\lambda_k(\mathbf{x})$, such as mean value coordinates (Ju et al., 2005):

```math
\mathbf{x} = \sum_{k} \lambda_k(\mathbf{x})\,\mathbf{v}_k \quad \Longrightarrow \quad
\mathbf{x}' = \sum_{k} \lambda_k(\mathbf{x})\,\mathbf{v}'_k
```

The coordinates are computed once for the undeformed shape, and moving the cage vertices deforms everything inside. Cages follow the shape more closely than a box lattice and are convenient when the deformation handles should follow the body contours.

### Comparison

| Method | Design variables | Smoothness | Volume mesh | Typical use |
| --- | --- | --- | --- | --- |
| CAD feature parameters | Dimensions and angles in the CAD model | Exact CAD | Remesh every variant | Few, well-defined changes; manufacturable output |
| FFD | Control-point motions in a lattice | Smooth polynomial | Remesh or morph | Local smooth changes, optimisation |
| RBF morphing | Displacements of control points | Smooth, local with compact support | Morph the existing mesh | Industrial design studies, mesh-consistent datasets |
| Cage-based | Motions of cage vertices | Smooth inside the cage | Remesh or morph | Shape-following handles |

Morphing the volume mesh avoids remeshing noise, the small variations in output caused only by a different mesh, which can be comparable to the effect of small parameter changes. Its limit is mesh quality: large deformations shear the prism layers, so the minimum cell quality must be checked for every variant and the parameter ranges chosen so that it stays acceptable.

## The 13 Parameters of the Case Study

The parameters below cover the front end, the cabin, the ride height and underbody, and the rear end. The ranges are illustrative of morphing studies about a baseline and must in practice be set by packaging, styling and regulations. The expected sensitivity is a prior judgement based on where drag is generated on a passenger car; it is what the sensitivity analysis below has to confirm or correct.

| No. | Parameter | Physical effect | Illustrative range | Expected sensitivity of $C_d$ |
| --- | --- | --- | --- | --- |
| 1 | Bonnet leading-edge $z$-position | Moves the stagnation region and changes the acceleration of the flow over the bonnet | $\pm 30$ mm | Medium |
| 2 | Upper intake $z$-extension | Changes the cooling-air inlet area and the internal flow through the radiator | $\pm 20$ mm | Low to medium (higher with cooling flow modelled) |
| 3 | Lower intake $z$-extension | Changes the split between cooling flow and underbody flow at the front bumper | $\pm 20$ mm | Medium |
| 4 | Ramp angle | Inclination of the bonnet-windscreen transition; affects flow attachment over the bonnet and the A-pillar region | $\pm 3^\circ$ | Low to medium |
| 5 | Windscreen angle | Changes the pressure on the windscreen and roof and the strength of the A-pillar vortices | $\pm 3^\circ$ | Medium |
| 6 | Pitch angle (rotation about $y$) | Changes the underbody flow and the balance between front and rear lift | $\pm 1^\circ$ | Medium for lift, low to medium for drag |
| 7 | Ground clearance ($z$-translation) | Changes the underbody flow rate and the flow around the wheels | $\pm 30$ mm | Medium to high |
| 8 | Battery pack $z$-position | Changes the local underfloor clearance | $\pm 20$ mm | Low to medium |
| 9 | Rear window angle | Controls separation on the rear slope and the strength of the C-pillar vortices | $\pm 5^\circ$ | High |
| 10 | Rear window length | Moves the position of the separation line at the rear | $\pm 50$ mm | Medium to high |
| 11 | Trunk lid angle | Changes the base pressure and the rear lift, acting like an integrated spoiler | $\pm 5^\circ$ | High |
| 12 | Trunk length | Changes the size of the wake and the pressure recovery at the rear | $\pm 50$ mm | Medium to high |
| 13 | Diffuser angle | Controls pressure recovery under the rear of the car; separates if too steep | $\pm 4^\circ$ | Medium to high |

The rear-end parameters are expected to dominate because most of the drag of a passenger car is pressure drag from the separated wake. Their effect can be strongly nonlinear. On the Ahmed body, the generic bluff body used to study rear-end flows, drag rises with the rear slant angle up to a critical angle of about $30^\circ$ and then drops abruptly when the flow over the slant separates completely and the C-pillar vortices weaken (Ahmed et al., 1984). A parameter range that crosses such a regime change makes the output discontinuous, which no smooth surrogate can fit; either the range is restricted to one regime or the regime is treated as a separate output.

## Sensitivity Analysis

### One-at-a-Time and Elementary Effects

The simplest local measure is a finite difference about the baseline,

```math
\frac{\partial Y}{\partial p_k} \approx
\frac{Y(\mathbf{p} + \delta\,\mathbf{e}_k) - Y(\mathbf{p})}{\delta}
```

with $\mathbf{e}_k$ the unit vector of parameter $k$ and a step $\delta$ large enough to rise above the iterative noise of the CFD. It costs $d + 1$ runs, or a single adjoint solve for all $d$ derivatives (Jameson, 1988). Being local, it says nothing about the behaviour elsewhere in $\mathcal{P}$ or about interactions. The Morris method (Morris, 1991) repeats such one-at-a-time steps from $r$ random base points and summarises the elementary effects $`\mathrm{EE}_k = [Y(\mathbf{p} + \Delta\mathbf{e}_k) - Y(\mathbf{p})]/\Delta`$ by the mean of their absolute values $\mu_k^*$ (overall importance) and their standard deviation $\sigma_k$ (nonlinearity or interaction). With $r(d+1)$ runs, about 140 for $r = 10$ and $d = 13$, it is a practical screening method directly on CFD.

### Sobol Indices

Variance-based sensitivity analysis treats the parameters as independent random variables, usually uniform on their ranges, and decomposes the variance of $Y$ into contributions of single parameters and groups (Sobol', 2001). The first-order and total indices of parameter $k$ are

$$
S_k = \frac{\mathrm{Var}_{p_k}\big(\mathbb{E}[Y \mid p_k]\big)}{\mathrm{Var}(Y)},
\qquad
S_{Tk} = \frac{\mathbb{E}_{\mathbf{p}_{\sim k}}\big[\mathrm{Var}_{p_k}(Y \mid \mathbf{p}_{\sim k})\big]}{\mathrm{Var}(Y)} = 1 - \frac{\mathrm{Var}_{\mathbf{p}_{\sim k}}\big(\mathbb{E}[Y \mid \mathbf{p}_{\sim k}]\big)}{\mathrm{Var}(Y)}
$$

where $`\mathbf{p}_{\sim k}`$ denotes all parameters except $`p_k`$. $`S_k`$ is the fraction of the variance that $`p_k`$ explains on its own, $`S_{Tk}`$ the fraction it is involved in including all interactions, and $S_{Tk} - S_k$ measures its interactions. The first-order indices satisfy $\sum_k S_k \le 1$, with equality for an additive model. A parameter with $S_{Tk} \approx 0$ can be fixed at any value in its range without changing the output distribution.

The indices are estimated with the Saltelli scheme. Two independent $N \times d$ sample matrices $A$ and $B$ are drawn, and $A_B^{(k)}$ denotes $A$ with its $k$-th column replaced by that of $B$. Then

$$
S_k \approx \frac{1}{\mathrm{Var}(Y)} \frac{1}{N}\sum_{j=1}^{N}
f(B)_j\left[f(A_B^{(k)})_j - f(A)_j\right],
\qquad S_{Tk} \approx \frac{1}{\mathrm{Var}(Y)}
\frac{1}{2N}\sum_{j=1}^{N}\left[f(A)_j - f(A_B^{(k)})_j\right]^2
$$

the first-order estimator of Saltelli et al. (2010) and the total-effect estimator of Jansen (1999). All indices together cost $N(d + 2)$ evaluations, so with $N$ in the thousands they are computed on a surrogate, not on CFD. The outputs should be centred by their sample mean before applying the formula for $S_k$; otherwise a large mean value (such as $C_d \approx 0.3$ against a spread of 0.01) adds a large noise term.

![Estimated and exact Sobol indices of a synthetic drag model and convergence with sample size](../../../scripts/algorithms/sobol_sensitivity_analysis/sobol_sensitivity_analysis.png)

The figure applies the estimators to a synthetic five-parameter drag model with exactly known indices. With 57,344 evaluations every estimate is within 0.001 of the exact value. The total index of $p_1$ (0.585) exceeds its first-order index (0.475) because of the $p_1 p_3$ interaction, and the inert parameter $p_5$ gets exactly zero. The right panel shows why quasi-random samples are preferred: the Monte Carlo error decreases as $N^{-1/2}$, while scrambled Sobol points reach the same accuracy with more than ten times fewer evaluations.

## Parameter Correlation and Constraints

Two kinds of correlation matter. The first is geometric redundancy. If two parameters move the same surface region in similar ways, their displacement fields $\mathbf{d}_k = \partial\mathbf{X}/\partial p_k$ are nearly parallel, which can be measured by

```math
\cos\theta_{kl} = \frac{\langle \mathbf{d}_k, \mathbf{d}_l \rangle}{\sqrt{\langle \mathbf{d}_k, \mathbf{d}_k \rangle\langle \mathbf{d}_l, \mathbf{d}_l \rangle}},
\qquad \langle \mathbf{d}_k, \mathbf{d}_l \rangle = \int_{\Gamma} \mathbf{d}_k \cdot
\mathbf{d}_l \, dS
```

Values close to $\pm 1$ mean the two parameters produce almost the same shape change. The CFD cannot distinguish them, the surrogate sees nearly collinear inputs, and the sensitivity of each is ill-defined; one of them should be removed or the pair replaced by their sum and difference. More generally, a singular value decomposition of the matrix of displacement fields shows how many independent shape changes the parameters span, the same idea as PCA of shapes in [Machine Learning on CAD Geometry](../geometry/ml_on_cad.md).

The second is statistical correlation in the sample. Space-filling designs such as Latin hypercube or Sobol sequences ([One-Stage Sampling](../../numerical/surrogates/one_stage_sampling.md)) give nearly uncorrelated parameters, which is what the Sobol decomposition assumes. Constraints break this. A packaging limit such as a fixed total rear overhang, $p_{10} + p_{12} \le L_{\max}$, or a minimum ground clearance after pitch, couples the parameters. Simple constraints can be handled by sampling the box and rejecting infeasible points (the acceptance rate tells how much of the box is lost), or by reparameterising, for example sampling the overhang share instead of the two lengths. With dependent inputs the classical Sobol indices no longer partition the variance uniquely, so sensitivity results obtained on the feasible set must be interpreted with care. Validity constraints come on top: no self-intersections, positive Jacobian of the FFD map or minimum mesh quality after morphing, checked for every sample before it is sent to the solver.

## Key Takeaways

- Morphing a baseline with FFD, RBF or cage-based methods gives smooth, low-dimensional parameterisations; RBF morphing of the volume mesh keeps the mesh topology and output correspondence identical across variants.
- The 13 parameters span front end, cabin, ride height and rear end; rear-end parameters are expected to dominate drag because the wake dominates pressure drag.
- One-at-a-time derivatives and Morris screening are affordable on CFD; Sobol indices need thousands of evaluations and are computed on a surrogate with quasi-random samples.
- $S_{Tk} - S_k$ measures interactions, and $S_{Tk} \approx 0$ identifies parameters that can be frozen.
- Check geometric redundancy between parameters with the correlation of their displacement fields, and handle packaging constraints explicitly in the sampling.
- Ranges that cross a flow-regime change make the output discontinuous and should be avoided or split.

## Related Scripts

- [Sobol Sensitivity Analysis](../../../scripts/algorithms/sobol_sensitivity_analysis/): estimates first-order and total Sobol sensitivity indices of a synthetic five-parameter drag model with the Saltelli sampling scheme and checks them against the exact values.
- [Design Space Distribution via Sobol Sequences](../../../scripts/plots/design_space_distribution/): draws a four-dimensional scrambled Sobol design of 512 geometry variants and shows all of its 2D projections and 1D marginals in a scatter matrix, with the discrepancy of each projection compared against a random design of the same size.
- [Airfoil Shape PCA](../../../scripts/algorithms/airfoil_shape_pca/): builds a linear shape space for NACA 4-digit airfoils by principal component analysis (PCA) of their surface coordinates and shows how few modes are needed to describe the family.
- [ML-CFD Surrogate Workflow](../../../scripts/plots/ml_cfd_workflow/): draws a schematic of the workflow for building a machine-learning surrogate of CFD results, from the design of experiments to deployment in an optimisation loop.

## Exercises

**Exercise 1.** At the baseline windscreen angle a CFD run gives $C_d = 0.310$. Increasing the windscreen angle by $\delta = 1^\circ$ gives $C_d = 0.3065$. Estimate $\partial C_d/\partial p_5$ with a forward difference and predict $C_d$ for a $3^\circ$ increase. Why should the prediction be checked with CFD?

<details>
<summary>Answer</summary>

```math
\frac{\partial C_d}{\partial p_5} \approx \frac{0.3065 - 0.310}{1} = -0.0035 \text{ per degree}
```

The linear prediction for $+3^\circ$ is $0.310 + 3 \times (-0.0035) = 0.2995$.

The forward difference is first-order accurate and the extrapolation assumes a linear response over three degrees. Changes of the A-pillar vortices or of the separation on the rear can bend or even reverse the trend, so the result indicates a direction, not a value.

</details>

**Exercise 2.** A gradient-based optimisation over the 13 parameters needs 20 design iterations, and each CFD run takes 6 hours. Compare the cost of the gradients with forward differences, central differences and an adjoint method (one adjoint solve costs about one primal solve).

<details>
<summary>Answer</summary>

- Forward differences: 1 baseline and 13 perturbed runs, 14 runs per iteration, $14 \times 20 \times 6 = 1680$ h.
- Central differences: 2 runs per parameter plus the baseline for the objective, 27 runs per iteration, $27 \times 20 \times 6 = 3240$ h.
- Adjoint: 1 primal and 1 adjoint solve per iteration, $2 \times 20 \times 6 = 240$ h.

The adjoint cost does not depend on the number of parameters, which is why it wins when there are many parameters and few objectives.

</details>

**Exercise 3.** An engineer proposes a full-factorial design with 3 levels for each of the 13 parameters. How many CFD runs is that, and how long would it take in serial at 1 hour per run? What is a practical alternative?

<details>
<summary>Answer</summary>

$3^{13} = 1{,}594{,}323$ runs, about 1.59 million hours or 182 years in serial.

A space-filling design (Latin hypercube or Sobol) with about 10 samples per parameter, around 130 runs, is a common starting point, optionally preceded by Morris screening to remove unimportant parameters, and followed by adaptive infill runs where the surrogate is uncertain or near the optimum.

</details>

**Exercise 4.** A surrogate gives $`C_d = 0.30 + 0.010\,x_1 + 0.005\,x_2 + 0.008\,x_1 x_2`$ with independent $x_1, x_2 \sim U(-1, 1)$. Compute $\mathrm{Var}(C_d)$, the first-order indices $S_1$, $S_2$ and the total indices $S_{T1}$, $S_{T2}$. What would one-at-a-time derivatives at $x_1 = x_2 = 0$ miss?

<details>
<summary>Answer</summary>

With $\mathrm{Var}(x) = 1/3$ and $\mathrm{Var}(x_1 x_2) = 1/9$, and all three terms uncorrelated:

- $V_1 = 0.010^2/3 = 3.33 \times 10^{-5}$, $V_2 = 0.005^2/3 = 8.33 \times 10^{-6}$, $V_{12} = 0.008^2/9 = 7.11 \times 10^{-6}$.
- $\mathrm{Var}(C_d) = 4.88 \times 10^{-5}$.
- $S_1 = 0.683$, $S_2 = 0.171$, interaction share $S_{12} = 0.146$.
- $S_{T1} = 0.683 + 0.146 = 0.829$ and $S_{T2} = 0.171 + 0.146 = 0.317$.

At the origin the derivatives are 0.010 and 0.005 and the interaction term has zero slope, so a local analysis misses the 15% of the variance due to the interaction. Weighting the squared derivatives by $\mathrm{Var}(x) = 1/3$ attributes $`0.005^2/(0.010^2 + 0.005^2) = 20\%`$ of the variance to $x_2$, whereas its total index is 0.317.

</details>

**Exercise 5.** The CFD drag has iterative-convergence noise of amplitude $\eta = 10^{-4}$, and $|C_d''| \approx 2 \times 10^{-4}$ per degree squared. The forward-difference error is roughly $`E(\delta) = |C_d''|\,\delta/2 + 2\eta/\delta`$. Find the step that minimises it and the minimum error, and compare with $\delta = 0.1^\circ$ and $\delta = 5^\circ$.

<details>
<summary>Answer</summary>

Setting $dE/d\delta = |C_d''|/2 - 2\eta/\delta^2 = 0$ gives

```math
\delta^* = 2\sqrt{\frac{\eta}{|C_d''|}} = 2\sqrt{\frac{10^{-4}}{2 \times 10^{-4}}} \approx 1.41^\circ
```

with minimum error $`E^* = 2\sqrt{\eta\,|C_d''|} \approx 2.83 \times 10^{-4}`$ per degree.

For comparison, $E(0.1^\circ) = 2.01 \times 10^{-3}$, dominated by noise, and $E(5^\circ) = 5.4 \times 10^{-4}$, dominated by truncation. Even the best step leaves an error of about 8% of the sensitivity in Exercise 1; only tighter solver convergence (smaller $\eta$) improves on that.

</details>

## References

- Sederberg, T. W., & Parry, S. R., "Free-Form Deformation of Solid Geometric Models", *Computer Graphics (Proceedings of SIGGRAPH '86)* 20(4), 151–160, 1986.
- de Boer, A., van der Schoot, M. S., & Bijl, H., "Mesh deformation based on radial basis function interpolation", *Computers & Structures* 85(11–14), 784–795, 2007.
- Ju, T., Schaefer, S., & Warren, J., "Mean value coordinates for closed triangular meshes", *ACM Transactions on Graphics* 24(3), 561–566, 2005.
- Ahmed, S. R., Ramm, G., & Faltin, G., "Some Salient Features of the Time-Averaged Ground Vehicle Wake", SAE Technical Paper 840300, 1984.
- Jameson, A., "Aerodynamic design via control theory", *Journal of Scientific Computing* 3(3), 233–260, 1988.
- Morris, M. D., "Factorial Sampling Plans for Preliminary Computational Experiments", *Technometrics* 33(2), 161–174, 1991.
- Sobol', I. M., "Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates", *Mathematics and Computers in Simulation* 55(1–3), 271–280, 2001.
- Jansen, M. J. W., "Analysis of variance designs for model output", *Computer Physics Communications* 117(1–2), 35–43, 1999.
- Saltelli, A., Annoni, P., Azzini, I., Campolongo, F., Ratto, M., & Tarantola, S., "Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index", *Computer Physics Communications* 181(2), 259–270, 2010.
- Hucho, W.-H. (Ed.), *Aerodynamics of Road Vehicles*, 4th ed., SAE International, 1998.
