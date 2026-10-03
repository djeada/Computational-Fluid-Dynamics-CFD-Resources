## Model Training Methodology

Training a geometric deep learning model for aerodynamic prediction requires careful experimental design to assess both single-geometry accuracy and cross-geometry generalization. The fundamental question is whether a model trained on one family of shapes can make reliable predictions for an entirely different geometry, or whether a combined model trained on diverse shapes offers better generalization. Answering this requires structured experiments with separate and merged datasets, rigorous hyperparameter optimization, and standardized evaluation metrics.

A core objective in applying geometric deep learning (GDL) to external aerodynamics is to train neural networks—often based on graph or mesh-based architectures—that can handle different vehicle or body shapes. One way to test generalization capabilities is to design two distinct “Design of Experiments” (DoE) scenarios. In the first scenario, separate GDL models are trained on individual shapes (e.g., Design 1 and Design 2), each model specializing in a single geometry family. In the second scenario, the datasets for both shapes are merged, and a single “universal” model is trained to see if it can maintain adequate performance when encountering unfamiliar geometrical features.

I. **Scenario 1**: Each model is dedicated to one particular geometry. For instance, **Model 1** only uses data from Design 1, while **Model 2** only uses data from Design 2.

II. **Scenario 2**: A combined **Model 3** is trained on the merged data from both designs, examining whether a shared representation emerges that handles a broader variety of shapes.

This methodology aims to clarify if geometric deep learning can adapt not only to minor shape deviations within a single design but also to entirely new geometries with different styling cues or proportions.

### Models and Datasets

In a typical setup, two different design datasets are used. One corresponds to Design 1 (e.g., a baseline shape family with certain variants), and another corresponds to Design 2 (a different family of shapes with its own unique modifications). Both datasets might involve systematic geometry alterations—such as bumper changes or roof attachments—to enrich the training space with diverse configurations.

**Design 1 dataset (X):**

I. 50 to 70 simulations (X) for training

II. An additional 10 to 20 simulations (X) for testing

**Design 2 dataset (Y):**

I. 20 to 40 simulations (Y) for training

II. 5 to 15 simulations (Y) for testing

Hence:

- **Model 1** (trained on Design 1 data)
- **Model 2** (trained on Design 2 data)
- **Model 3** (trained on a combination of Design 1 and Design 2 data, i.e., 50–70X + 20–40Y, tested on 10–20X + 5–15Y)

#### Hyperparameter Optimization

Before the final training, an essential step is to optimize model hyperparameters: network depth, message-passing updates, and embedding dimensions. Deeper or wider networks can capture more complex aerodynamic phenomena, but they demand more GPU memory and longer training. Engineers typically conduct grid searches or Bayesian optimization over hyperparameter ranges. This tuning phase may consume substantial GPU hours, yet it often determines whether the final GDL model can learn subtle features in boundary layers, separation regions, or vortex structures.

Once a promising configuration is identified, the final training run for each model usually completes within a day of GPU time, depending on the size of the dataset and hardware (e.g., NVIDIA A10, RTX 6000, or similar).

```
 +----------------+        +-----------------+       +-----------------+
 |  CFD Datasets  |  -->   | Hyperparameter  |  -->  |  GDL Training & |
 | (Design 1/2)   |        |  Optimization   |       |    Validation   |
 +----------------+        +-----------------+       +-----------------+
     |                                                    |
     | (Mesh & Flow                                       |
     |  Decimation)                                       |
     |                                                    |
     v                                                    v
 +----------------+                                 +-----------------+
 |  Decimated     |                                 |  Trained Model  |
 |  Geometries    |                                 | (1, 2, or 3)    |
 +----------------+                                 +-----------------+
```

The above ASCII diagram summarizes the data flow: raw CFD results are first reduced in geometric and flow-field complexity to create a manageable training dataset. Subsequent hyperparameter tuning ensures that the chosen GDL architecture is well-suited to the mesh or point-cloud data structure.

### Training Data Overview

|  | Model 1 | Model 2 | Model 3 |
| --- | --- | --- | --- |
| **Training data** | 50–70X | 20–40Y | 50–70X + 20–40Y |
| **Test data (unseen)** | 10–20X | 5–15Y | 10–20X + 5–15Y |

- **Model 1** trains exclusively on X data points (from Design 1).
- **Model 2** trains exclusively on Y data points (from Design 2).
- **Model 3** mixes X and Y data points in the training set, aiming for robust generalization.

Test samples come from configurations excluded from the training process, ensuring a fair assessment of each model’s ability to predict unobserved aerodynamic conditions.

### Results

To evaluate the success of this approach, each trained model’s outputs (e.g., drag coefficient $C_d$, lift coefficient $C_l$, or flow field variables) are compared against reference CFD solutions. The key question is whether GDL methods can faithfully reconstruct aerodynamic forces and distributions given only a geometric mesh plus learned aerodynamic correlations.

### Evaluation Parameters

Commonly used performance metrics include:

- **$R^2$ Score (Coefficient of Determination)**: Measures how well predicted results correlate with reference CFD data. An $R^2$ of 1.0 indicates perfect prediction, while values below 0.5 suggest the model explains less than half the variance in the data. Formally:

$$
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}
$$

where $y_i$ are the reference CFD values, $\hat{y}_i$ are the model predictions, and $\bar{y}$ is the mean of the reference values.

- **Mean Absolute Error (MAE)**: Indicates the average deviation between predicted and actual values (e.g., $C_d$). Defined as:

$$
\text{MAE} = \frac{1}{N}\sum_{i=1}^{N} |y_i - \hat{y}_i|
$$

- **Standard Deviation of Error**: Shows how the prediction errors are distributed around the mean. A low standard deviation indicates consistent predictions, while a high value suggests the model is unreliable for certain configurations.
- **Relative MAE (%)**: Puts the errors into percentage form relative to a typical baseline (e.g., the nominal drag coefficient of a baseline geometry), making it easier to judge engineering significance across different quantities.

Together, these metrics give engineers a comprehensive picture of how each model behaves on both training and test sets.

### Comparison of Models 1, 2, and 3

| Model | Training R² Score | Test R² Score | Training MAE | Test MAE | Training Std Dev | Test Std Dev | Training Relative MAE (%) | Test Relative MAE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model 1 | 0.930 | 0.610 | 0.0053 | 0.0110 | 0.0058 | 0.0115 | 2.5 | 4.8 |
| Model 2 | 0.925 | 0.620 | 0.0051 | 0.0108 | 0.0056 | 0.0112 | 2.4 | 4.7 |
| Model 3 | 0.940 | 0.630 | 0.0050 | 0.0105 | 0.0055 | 0.0110 | 2.3 | 4.5 |

- **Model 1** and **Model 2** each exhibit strong performance on their respective geometry families in training but show moderate drops in $R^2$ and increased MAE on unseen test data. This is expected since test conditions may involve shape or flow variations not present in the training set.
- **Model 3**, trained on both designs, achieves slightly higher test-set $R^2$ and lower MAE, suggesting that exposure to diverse geometric modifications helps the model learn more generalized aerodynamic relationships.

### Quality of Field Variable Predictions

For more nuanced validation, predicted flow fields (e.g., surface pressure, velocity contours, turbulent kinetic energy) can be compared against CFD references. Visual inspections often confirm whether the GDL model reproduces key flow features like stagnation regions, vortical structures, and trailing wake patterns. While minor discrepancies may arise—especially in regions of high curvature or strong flow separation—the overall accuracy often proves sufficient for early-stage design exploration or parametric studies.

Quantitative field-level validation typically involves computing pointwise error metrics across the surface or volume mesh. A common approach is to evaluate the normalized root-mean-square error (NRMSE) for a field variable $\phi$ (e.g., surface pressure coefficient $C_p$):

$$
\text{NRMSE}(\phi) = \frac{\sqrt{\frac{1}{N}\sum_{i=1}^{N}(\phi_i^{\text{pred}} - \phi_i^{\text{ref}})^2}}{\phi_{\max}^{\text{ref}} - \phi_{\min}^{\text{ref}}}
$$

Spatial error maps—computed as $\Delta\phi(\mathbf{x}) = \phi^{\text{pred}}(\mathbf{x}) - \phi^{\text{ref}}(\mathbf{x})$—are especially useful for identifying systematic prediction weaknesses. For example, consistently high errors near the A-pillar or in the rear wake indicate that the network struggles with separated flow regions and may benefit from additional training data or architectural changes in those areas.

### Setting Up the Problem

1. **Define geometry families and simulation budgets.** Identify distinct shape families (e.g., Design 1 and Design 2) and allocate a fixed number of CFD simulations to each, balancing cost against data diversity.
2. **Choose a training strategy.** Decide whether to train separate single-geometry models (one per family) or a combined model on merged data. Running both approaches enables a direct comparison of specialist vs. generalist performance.
3. **Configure hyperparameter search.** Use grid search for small parameter spaces or Bayesian optimization (e.g., Optuna) for larger ones. Key hyperparameters include network depth, message-passing iterations, learning rate, and embedding dimension.
4. **Select evaluation metrics.** Report $R^2$ for overall correlation, MAE for absolute accuracy, standard deviation for error spread, and relative MAE (%) for engineering interpretability. Consistent metrics across all models ensure fair comparison.
5. **Reserve unseen test geometries.** Hold out complete configurations—not just random samples—from training so that test performance reflects true generalization to new shapes rather than interpolation within known ones.
6. **Compare field-level vs. global predictions.** Evaluate both integrated quantities (e.g., $C_d$, $C_l$) and spatially resolved fields (e.g., surface $C_p$). A model may predict accurate global forces yet miss local flow features, so both levels of fidelity matter.

### Key Takeaways

- Structured DoE with separate and merged datasets is essential for quantifying single-geometry accuracy versus cross-geometry generalization.
- Hyperparameter optimization (grid search or Bayesian) has an outsized impact on final model quality and should not be skipped.
- A combined model trained on diverse geometries typically achieves better generalization than single-geometry specialists, as reflected by higher test-set $R^2$ and lower MAE.
- Reserving entire unseen geometries—not random splits—for testing provides the most realistic estimate of deployment performance.
- Both global aerodynamic coefficients and local field variables should be evaluated, since aggregate metrics can mask localized prediction errors.
- Early-stage design exploration benefits most from GDL surrogates, where modest accuracy trade-offs are acceptable in exchange for orders-of-magnitude speedup over full CFD.

### Related Scripts

- [Drag Coefficient Prediction](../../../scripts/plots/drag_coefficient_prediction/): compares two synthetic drag-coefficient predictors with reference values in a predicted-vs-reference plot, adding a regression line and $R^2$ for each.

### Exercises

**Exercise 1.** For Model 1 the comparison table gives a test MAE of 0.0110 and a test relative MAE of 4.8%. What baseline $C_d$ does this imply? What relative error does the same absolute MAE represent for a design with $C_d = 0.30$?

<details>
<summary>Answer</summary>

Baseline $C_d \approx 0.0110/0.048 \approx 0.229$.

For $C_d = 0.30$: $0.0110/0.30 \approx 3.7\%$.

Relative MAE depends on the chosen baseline, so the reference value must be reported with it.

</details>

**Exercise 2.** Model 1 has test $R^2 = 0.61$ and a test error standard deviation of 0.0115. Assuming the errors have zero mean, estimate the standard deviation of the reference $C_d$ values in the test set. Explain how a model with under 5% relative MAE can still have a modest $R^2$.

<details>
<summary>Answer</summary>

With zero-mean errors, MSE $\approx 0.0115^2 = 1.32 \times 10^{-4}$. Since $R^2 = 1 - \text{MSE}/\text{Var}(y)$:

$$
\text{Var}(y) = \frac{1.32 \times 10^{-4}}{1 - 0.61} \approx 3.39 \times 10^{-4},
\qquad \text{std}(y) \approx 0.0184
$$

The test designs differ in $C_d$ by only about 0.018, so an error spread of 0.0115 (62% of that) leaves much of the variance unexplained, even though it is small relative to $C_d$ itself. $R^2$ measures the ability to rank and separate designs; relative MAE measures absolute accuracy. Design studies usually care about the former.

</details>

**Exercise 3.** At four surface nodes the predicted pressure coefficients are $(0.95, 0.40, -0.30, -0.60)$ and the references are $(1.00, 0.35, -0.20, -0.65)$. Compute the NRMSE defined in the note.

<details>
<summary>Answer</summary>

The errors are $(-0.05, 0.05, -0.10, 0.05)$, so RMSE $= \sqrt{(0.0025 + 0.0025 + 0.01 + 0.0025)/4} \approx 0.0661$.

The reference range is $1.00 - (-0.65) = 1.65$, so NRMSE $\approx 0.0661/1.65 \approx 0.040$ (4.0%).

</details>

**Exercise 4.** Model 3 is trained on 60 Design 1 cases and 30 Design 2 cases. What per-sample loss weights make both designs contribute equally to the training loss while keeping the average weight equal to 1? Why might this matter?

<details>
<summary>Answer</summary>

With $N = 90$ samples and 2 groups, use $w_g = N/(2N_g)$: $w_X = 90/120 = 0.75$ and $w_Y = 90/60 = 1.5$.

Each group then contributes $60 \times 0.75 = 30 \times 1.5 = 45$ effective samples, and the total weight stays at 90.

Without weighting, the combined model is optimized mostly for Design 1, and its better average test score could hide poorer performance on Design 2. Report the metrics per design as well as combined.

</details>

**Exercise 5.** A grid search covers depth $\in \{4, 8, 12, 16\}$, hidden size $\in \{64, 128, 256\}$, learning rate $\in \{10^{-3}, 3 \times 10^{-4}, 10^{-4}\}$ and message-passing steps $\in \{5, 10, 15\}$, at 6 GPU-hours per trial. Compute the total cost and compare with 20 random-search trials. What is the probability that at least one of the 20 random trials lands in the best 5% of the search space?

<details>
<summary>Answer</summary>

Grid search: $4 \times 3 \times 3 \times 3 = 108$ trials, or $108 \times 6 = 648$ GPU-hours.

Random search: $20 \times 6 = 120$ GPU-hours.

The probability that at least one random trial lands in the top 5% is $1 - 0.95^{20} \approx 0.64$.

Random search is much cheaper and, when only a few hyperparameters really matter, tries more distinct values of each one than a grid does. Bayesian optimization (for example, Optuna) improves on this by concentrating later trials in promising regions.

</details>

### References

- Bronstein, M. M., Bruna, J., Cohen, T., & Veličković, P., "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges", arXiv:2104.13478, 2021.
- Bergstra, J., & Bengio, Y., "Random Search for Hyper-Parameter Optimization", *Journal of Machine Learning Research* 13, 2012.
- Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M., "Optuna: A Next-generation Hyperparameter Optimization Framework", ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2019.
- Hastie, T., Tibshirani, R., & Friedman, J., *The Elements of Statistical Learning*, 2nd ed., Springer, 2009.
- Pfaff, T., Fortunato, M., Sanchez-Gonzalez, A., & Battaglia, P. W., "Learning Mesh-Based Simulation with Graph Networks", International Conference on Learning Representations (ICLR), 2021.
