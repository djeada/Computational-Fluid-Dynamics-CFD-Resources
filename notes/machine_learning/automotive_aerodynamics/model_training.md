# Training and Evaluating Surrogates Across Vehicle Designs

A surrogate that predicts drag well for morphs of the vehicle it was trained on may still fail on a different vehicle. This note sets out an experiment that measures both abilities: models trained on one design family, on another, and on both, each tested in distribution and across designs. It then covers hyperparameter optimisation, loss functions for surface fields, metrics for fields and integrated forces, parity plots and error maps, and how to read the resulting patterns. The architectures themselves (graph neural networks on meshes, neural operators) are in [Graph Neural Networks](../neural_networks/graph_neural_networks.md), and general training practice is in [Training and Validation](../fundamentals/training_and_validation.md).

## Problem Statement

Two design families are available: family X (Design 1, for example morphs of a saloon) with dataset $\mathcal{D}_X$, and family Y (Design 2, for example morphs of an SUV) with $\mathcal{D}_Y$. Each sample $i$ consists of an input $\mathbf{x}_i$ (the surface mesh with node coordinates and normals, or the design parameters $`\mathbf{p}_i`$, plus operating conditions) and CFD targets $`\mathbf{y}_i`$: surface fields such as the pressure coefficient $`C_{p}`$ and wall-shear coefficient $`\mathbf{c}_f`$ at each surface node, and integrated coefficients such as $`C_d`$. A surrogate $`f_{\boldsymbol\theta}`$ is trained on a training set $`\mathcal{D}_{\mathrm{train}} \subseteq \mathcal{D}_X \cup \mathcal{D}_Y`$ by minimising

```math
\boldsymbol\theta^\star = \arg\min_{\boldsymbol\theta}\ \frac{1}{|\mathcal{D}_{\mathrm{train}}|}\sum_{i \in \mathcal{D}_{\mathrm{train}}} w_i\, \mathcal{L}\left(f_{\boldsymbol\theta}(\mathbf{x}_i), \mathbf{y}_i\right) + \lambda\, \Omega(\boldsymbol\theta),
```

with per-sample weights $w_i$, a regulariser $\Omega$ and penalty $\lambda$. The quantities of interest are the expected errors on new designs from each family,

```math
R_X(f) = \mathbb{E}_{\mathbf{x} \sim P_X}\left[\ell(f(\mathbf{x}), \mathbf{y})\right],
\qquad
R_Y(f) = \mathbb{E}_{\mathbf{x} \sim P_Y}\left[\ell(f(\mathbf{x}), \mathbf{y})\right],
```

estimated on held-out test geometries, where $P_X$ and $P_Y$ are the distributions of the two families and $\ell$ is an evaluation metric. Testing on the family used for training measures in-distribution generalisation; testing on the other family measures cross-design generalisation, under a shift of the input distribution from $P_X$ to $P_Y$. The difficulty is that each family contributes only tens of geometries, every sample is a large field, and the two families may differ in ways that the inputs do not describe.

## Experimental Design

Three models are trained with the same architecture and the same hyperparameter search.

|  | Model 1 | Model 2 | Model 3 |
| --- | --- | --- | --- |
| Training data | 50 to 70 designs of X | 20 to 40 designs of Y | Both training sets |
| In-distribution test | 10 to 20 designs of X | 5 to 15 designs of Y | Both test sets, reported separately |
| Cross-design test | Test designs of Y | Test designs of X | None (both families seen) |

The six combinations of training set and test family form a $3 \times 2$ table. Its in-distribution entries show how well each model interpolates within a family, and its off-diagonal entries show how far it transfers. Comparing Model 3 with the specialists on each family shows whether combining the data helps (positive transfer) or hurts (negative transfer).

The experiment is meaningful only with the following controls.

- Test designs are complete geometries never seen in training, with all their operating conditions held out together, and they are drawn independently of the training designs (see [Design of Experiments and Dataset Construction](datasets.md#splitting-by-geometry-family)).
- Both families come from the same CFD pipeline. Otherwise a difference in labels caused by the setup is indistinguishable from a failure to transfer.
- Simple baselines are reported alongside: the training-set mean, and a scalar surrogate on the design parameters such as kriging or ridge regression. A deep model that does not beat them on $C_d$ adds nothing for that quantity.
- In Model 3 the smaller family can be weighted so that both families contribute equally, with $`w_i = N/(G\,N_{g(i)})`$ for $G$ families of sizes $N_g$ and total size $N$; the average weight stays 1.
- Every model is trained with several random seeds, and the spread over seeds is reported, since with 10 to 20 test designs the difference between two models is often smaller than that spread.

![Synthetic illustration of in-distribution and cross-design errors](../../../scripts/plots/cross_design_generalization/cross_design_generalization.png)

The figure is a synthetic illustration with an analytic $C_d$ in a 2D parameter space, not CFD data. Family X occupies the lower-left part of the space and family Y the upper-right, with a small overlap, and each model is a ridge regression on radial basis functions tuned by 5-fold cross validation. Each specialist is within a factor of two of the 2-count label-noise floor on its own family (1.7 counts for Model 1 on X, 3.4 for Model 2 on Y) and is 4 to 16 times worse across designs (26.8 counts for Model 1 on Y, 13.5 for Model 2 on X). Model 3 matches each specialist on its own family (1.8 and 3.4 counts) because the two families share one underlying function here. The parity plots show where the cross-design predictions fail: on the test designs farthest from the other family's training region.

## Hyperparameter Optimisation

The search space for a mesh-based network typically includes the number of message-passing steps or layers, the hidden width, the learning rate and its schedule, weight decay, batch size and the loss weights. The procedure is the same whatever the model.

1. Split the training geometries into a training and a validation part, or into grouped folds, by geometry. The test set is not touched.
2. Search with random search or Bayesian optimisation. Random search samples each hyperparameter at many distinct values and, when only a few hyperparameters matter, finds good settings with far fewer trials than a grid (Bergstra and Bengio, 2012). Bayesian optimisation, for example the tree-structured Parzen estimator used by Optuna, concentrates later trials in promising regions.
3. Stop poor trials early on the validation loss to save GPU time.
4. Retrain the selected configuration on all training geometries with several seeds, and evaluate once on the test sets.

For the cross-design experiment the hyperparameters of Models 1 and 2 must be selected on their own family's validation data. Tuning Model 1 on validation designs from Y would leak the cross-design test into training.

## Losses for Surface Fields

Surface nodes of a decimated mesh are not evenly spaced: small features such as mirrors and wheel spokes carry many nodes per unit area. An unweighted mean over nodes therefore emphasises those regions in proportion to their node density, not to their area or their effect on the forces. The area-weighted, masked loss for one sample is

```math
\mathcal{L}_{\mathrm{surf}} = \frac{\sum_{j=1}^{n} m_j A_j \left(\hat{C}_{p,j} - C_{p,j}\right)^2}{\sum_{j=1}^{n} m_j A_j},
```

where $n$ is the number of surface nodes, $A_j$ the surface area associated with node $j$ (for example a third of the area of the adjacent triangles), $`\hat{C}_{p,j}`$ and $`C_{p,j}`$ the predicted and CFD pressure coefficients, and $`m_j \in \{0, 1\}`$ a mask. The mask excludes nodes that should not be fitted: padding added to batch meshes of different size, surfaces outside the vehicle such as the ground, and nodes whose labels are unreliable. Volume fields are weighted by cell volume in the same way. With several output fields, each is normalised by its standard deviation over the training set before the losses are added with weights $\lambda_k$.

A force-consistency term can be added. The coefficients predicted by integrating the fields are differentiable functions of the predictions, so the loss can include $\lambda_F (\hat{C}_d - C_d)^2$, with $\hat{C}_d$ obtained by the surface integral below.

## Evaluation Metrics

### Point-Wise Field Errors

For a field $\phi$ on test sample $i$, with area-weighted norms $`\|\phi\|_A^2 = \sum_j A_j \phi_j^2`$, the relative error is

```math
\varepsilon_i = \frac{\|\hat{\phi}_i - \phi_i\|_A}{\|\phi_i\|_A}
```

The normalised RMSE divides the RMSE by the range of the reference values,

```math
\mathrm{NRMSE}(\phi) = \frac{1}{\phi^{\mathrm{ref}}_{\max} - \phi^{\mathrm{ref}}_{\min}}\sqrt{\frac{1}{n}\sum_{j=1}^{n}\left(\hat{\phi}_j - \phi_j^{\mathrm{ref}}\right)^2}
```

Both should be reported per sample, as a mean and a maximum over the test set, because the worst designs are often the ones that matter.

### Integrated Forces

Field errors only matter through the quantities engineers use. Integrate the predicted surface fields to obtain the force coefficients and compare them with the CFD values. With outward unit normals $`\mathbf{n}_j`$ (pointing from the vehicle into the fluid), the unit vector $`\mathbf{e}_x`$ in the free-stream direction and the friction coefficient vector $`\mathbf{c}_{f,j} = \boldsymbol\tau_{w,j}/(\tfrac{1}{2}\rho U_\infty^2)`$,

```math
C_d = \frac{1}{A_{\mathrm{ref}}}\sum_{j=1}^{n} A_j \left(-C_{p,j}\,\mathbf{n}_j + \mathbf{c}_{f,j}\right)\cdot \mathbf{e}_x
```

The free-stream pressure drops out because $`\oint \mathbf{n}\,dA = \mathbf{0}`$ on a closed surface. The integral weights each pressure error by $n_x A_j$: an error on the base or the front face changes the drag one-for-one, while the same error on a side panel changes it hardly at all. Report the $C_d$ error in drag counts ($1$ count $= 0.001$), compare the integrated $\hat{C}_d$ with any directly predicted $C_d$ (a large difference shows that the field and scalar outputs are inconsistent), and also apply the integration to the CFD fields to confirm that it reproduces the solver's force monitor.

### Scalar Metrics

For the integrated coefficients over $N_{\mathrm{test}}$ designs, with reference values $y_i$, predictions $\hat{y}_i$ and reference mean $\bar{y}$:

```math
\mathrm{MAE} = \frac{1}{N_{\mathrm{test}}}\sum_i |y_i - \hat{y}_i|,
\qquad
\mathrm{RMSE} = \sqrt{\frac{1}{N_{\mathrm{test}}}\sum_i (y_i - \hat{y}_i)^2},
\qquad
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}
```

$R^2$ compares the error with the spread of the test designs, so it depends on how different the test designs are, not only on the model. Pooling two families with different mean drag inflates $R^2$, because the between-family variance enters the denominator; report it per family. For design selection the rank correlation (Spearman's $\rho$) between predicted and reference $C_d$ is often the most relevant number, since the surrogate is used to decide which designs to simulate next.

## Parity Plots and Error Maps

A parity plot shows predicted against reference values for each test design, with the line $\hat{y} = y$. Points along a line of slope below 1 indicate that the model damps design effects towards the mean, typical of over-regularisation or too little data; a parallel offset indicates a bias; scatter that grows at the edge of the range indicates extrapolation. Plot each test family separately, as in the figure above.

Error maps show $\Delta\phi_j = \hat{\phi}_j - \phi_j$ on the surface. Two summaries over the test set are useful: the mean error map, which shows systematic bias such as a consistent under-prediction of suction at the A-pillar, and the map of the standard deviation of the error, which shows where predictions are unreliable, typically separation lines, the base and the wake. Weighting the map by $|n_x|$ shows which errors actually change the drag.

## Interpreting the Results

| Observation | Likely meaning | What to do |
| --- | --- | --- |
| Training error far below in-distribution test error | Overfitting to too few geometries | More designs, stronger regularisation, a smaller model, data augmentation such as mirror symmetry |
| Good in-distribution, poor cross-design error | The model learned features specific to one family; the second family is outside its training distribution | Train on both families, use inputs that describe geometry locally (normals, curvature, distance fields) rather than global parameters |
| Model 3 matches each specialist | Both families share a representation | Use the combined model; check whether fewer designs per family suffice |
| Model 3 worse than the specialist on one family | Negative transfer: the families conflict, their labels are inconsistent, or the larger family dominates the loss | Check that both used the same CFD pipeline, add a family indicator, reweight the families, increase capacity |
| Low field error but large $C_d$ error | Errors concentrated where $n_x$ is large (front, base), or a small bias that integrates over a large area | Inspect $\lvert n_x \rvert$-weighted error maps; add the force-consistency loss |
| High pooled $R^2$, low per-family $R^2$ | The model separates the families but not the designs within each family | Report per-family metrics and rank correlation |

## Key Takeaways

- Measure in-distribution and cross-design errors separately with a train-family by test-family table; a single pooled score hides the difference.
- Hold out whole geometries, tune hyperparameters only on validation geometries from the training families, and report the spread over seeds.
- Use an area-weighted, masked loss for surface fields so that node density does not decide what the model fits.
- Integrate predicted $C_p$ and wall shear to obtain $C_d$ and report its error in drag counts; field metrics alone do not show the force error.
- Compare against simple baselines, and use per-family $R^2$ and rank correlation rather than pooled $R^2$.
- A combined model can help or hurt; worse performance on one family usually points to inconsistent labels or unbalanced weighting.

## Related Scripts

- [Cross-Design Generalization](../../../scripts/plots/cross_design_generalization/): a synthetic illustration of why a surrogate trained on one design family can fail on another: three ridge-regression models trained on family X, family Y and both are tested on held-out designs of each family.
- [Drag Coefficient Prediction](../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient surrogates with held-out CFD values in a parity plot and an error plot, and shows that a high $R^2$ can hide errors of ten drag counts.

## Exercises

**Exercise 1.** The test designs of family X have $C_d$ values with standard deviation 0.005 around 0.30, and those of family Y the same spread around 0.33. A model has zero-mean errors with standard deviation 0.004 on both. Compute $R^2$ for each family separately and for the pooled test set (assume equal numbers of designs). What does the difference show?

<details>
<summary>Answer</summary>

Per family: $R^2 = 1 - 0.004^2/0.005^2 = 1 - 0.64 = 0.36$.

Pooled: the variance of the pooled references is the within-family variance plus the between-family variance, $0.005^2 + 0.015^2 = 2.5 \times 10^{-4}$ (the two means are $\pm 0.015$ from the pooled mean). Then $R^2 = 1 - 1.6 \times 10^{-5}/2.5 \times 10^{-4} = 0.936$.

The pooled score looks good only because the model can tell a saloon from an SUV. Within each family it explains only a third of the variance between designs, which is what a design study needs.

</details>

**Exercise 2.** Four surface nodes have $C_p$ errors $(0.10, 0.10, 0.02, 0.02)$ and associated areas $(1, 1, 8, 8)$ cm². The first two lie on a mirror, where the mesh is dense. Compute the unweighted and the area-weighted mean squared errors and explain the difference.

<details>
<summary>Answer</summary>

Unweighted: $(0.01 + 0.01 + 0.0004 + 0.0004)/4 = 0.0052$.

Area-weighted: $(1 \times 0.01 + 1 \times 0.01 + 8 \times 0.0004 + 8 \times 0.0004)/18 = 0.0264/18 \approx 0.00147$.

The unweighted loss is 3.5 times larger and dominated by the two mirror nodes, which cover 11% of the area. A model trained on it would spend its capacity on the densely meshed mirror; the area-weighted loss weights each region by its share of the surface.

</details>

**Exercise 3.** A simplified vehicle is a box with a front face and a base, each of 2 m², and four side faces parallel to the flow; $A_{\mathrm{ref}} = 2$ m². The mean $C_p$ is 0.6 on the front face and $-0.25$ on the base. Ignoring friction, compute the pressure drag coefficient. A surrogate predicts the base $C_p$ as $-0.27$ and makes errors of 0.05 on all side faces. What is the error in $C_d$?

<details>
<summary>Answer</summary>

The front face has $n_x = -1$, the base $n_x = +1$, and the sides $n_x = 0$. With the formula of the note:

```math
C_d = \frac{1}{2}\left[-0.6 \times (-1) \times 2 - (-0.25) \times 1 \times 2\right] = \frac{1.2 + 0.5}{2} = 0.85
```

With base $C_p = -0.27$ the base term becomes $0.54$ and $C_d = 0.87$, an error of 20 counts. The side-face errors contribute nothing because $n_x = 0$ there. A base-pressure error of 0.02 is small by field metrics, yet it produces a drag error larger than most design effects.

</details>

**Exercise 4.** Model 3 is trained on 60 designs of X and 30 of Y. Find per-sample weights that make both families contribute equally while keeping the average weight 1. Why might this matter?

<details>
<summary>Answer</summary>

With $N = 90$ and $G = 2$, $w_g = N/(G N_g)$ gives $w_X = 90/120 = 0.75$ and $w_Y = 90/60 = 1.5$.

Each family then contributes $60 \times 0.75 = 30 \times 1.5 = 45$ effective samples, and the total weight is 90.

Without weighting the combined model is optimised mostly for X, and a good average test score could hide poor performance on Y. Weighting is a choice to make deliberately, with results reported per family either way.

</details>

**Exercise 5.** A grid search covers depth in $`\{4, 8, 12, 16\}`$, hidden size in $`\{64, 128, 256\}`$, learning rate in $`\{10^{-3}, 3 \times 10^{-4}, 10^{-4}\}`$ and message-passing steps in $`\{5, 10, 15\}`$, at 6 GPU-hours per trial. Compute the total cost and compare it with 20 random-search trials. What is the probability that at least one of the 20 random trials lands in the best 5% of the search space?

<details>
<summary>Answer</summary>

Grid search: $4 \times 3 \times 3 \times 3 = 108$ trials, or $108 \times 6 = 648$ GPU-hours.

Random search: $20 \times 6 = 120$ GPU-hours.

The probability that at least one random trial lands in the top 5% is $1 - 0.95^{20} \approx 0.64$.

Random search costs less than a fifth as much. When only one or two hyperparameters matter, it also tries 20 distinct values of each, against 3 or 4 for the grid. Bayesian optimisation improves on it further by concentrating later trials in promising regions.

</details>

## References

- Pfaff, T., Fortunato, M., Sanchez-Gonzalez, A., & Battaglia, P. W., "Learning mesh-based simulation with graph networks", International Conference on Learning Representations (ICLR), 2021.
- Bronstein, M. M., Bruna, J., Cohen, T., & Veličković, P., "Geometric deep learning: Grids, groups, graphs, geodesics, and gauges", arXiv:2104.13478, 2021.
- Bergstra, J., & Bengio, Y., "Random search for hyper-parameter optimization", *Journal of Machine Learning Research*, 13, 281–305, 2012.
- Bergstra, J., Bardenet, R., Bengio, Y., & Kégl, B., "Algorithms for hyper-parameter optimization", *Advances in Neural Information Processing Systems 24*, 2011.
- Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M., "Optuna: A next-generation hyperparameter optimization framework", *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 2623–2631, 2019.
- Hastie, T., Tibshirani, R., & Friedman, J., *The Elements of Statistical Learning*, 2nd ed., Springer, 2009.
- Pan, S. J., & Yang, Q., "A survey on transfer learning", *IEEE Transactions on Knowledge and Data Engineering*, 22(10), 1345–1359, 2010.
- Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A., & Lawrence, N. D. (Eds.), *Dataset Shift in Machine Learning*, MIT Press, 2009.
