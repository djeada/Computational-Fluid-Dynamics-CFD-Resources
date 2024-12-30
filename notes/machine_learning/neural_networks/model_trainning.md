## Model Training Methodology  

A core objective in applying geometric deep learning (GDL) to external aerodynamics is to train neural networks—often based on graph or mesh-based architectures—that can handle different vehicle or body shapes. One way to test generalization capabilities is to design two distinct “Design of Experiments” (DoE) scenarios. In the first scenario, separate GDL models are trained on individual shapes (e.g., Design 1 and Design 2), each model specializing in a single geometry family. In the second scenario, the datasets for both shapes are merged, and a single “universal” model is trained to see if it can maintain adequate performance when encountering unfamiliar geometrical features.

I. **Scenario 1**: Each model is dedicated to one particular geometry. For instance, **Model 1** only uses data from Design 1, while **Model 2** only uses data from Design 2.  

II. **Scenario 2**: A combined **Model 3** is trained on the merged data from both designs, examining whether a shared representation emerges that handles a broader variety of shapes.

This methodology aims to clarify if geometric deep learning can adapt not only to minor shape deviations within a single design but also to entirely new geometries with different styling cues or proportions.

### Models and Datasets  

In a typical setup, two different design datasets are used. One corresponds to Design 1 (e.g., a baseline shape family with certain variants), and another corresponds to Design 2 (a different family of shapes with its own unique modifications). Both datasets might involve systematic geometry alterations—such as bumper changes or roof attachments—to enrich the training space with diverse configurations.  


I. 50 to 70 simulations (X) for training  

II. An additional 10 to 20 simulations (X) for testing  


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

|                  | Model 1              | Model 2              | Model 3                      |
|------------------|----------------------|----------------------|------------------------------|
| **Training data**    | 50–70X              | 20–40Y              | 50–70X + 20–40Y              |
| **Test data (unseen)** | 10–20X              | 5–15Y               | 10–20X + 5–15Y               |

- **Model 1** trains exclusively on X data points (from Design 1).  
- **Model 2** trains exclusively on Y data points (from Design 2).  
- **Model 3** mixes X and Y data points in the training set, aiming for robust generalization.

Test samples come from configurations excluded from the training process, ensuring a fair assessment of each model’s ability to predict unobserved aerodynamic conditions.

### Results  

To evaluate the success of this approach, each trained model’s outputs (e.g., drag coefficient $C_d$, lift coefficient $C_l$, or flow field variables) are compared against reference CFD solutions. The key question is whether GDL methods can faithfully reconstruct aerodynamic forces and distributions given only a geometric mesh plus learned aerodynamic correlations.

### Evaluation Parameters  

Commonly used performance metrics include:

- Measures how well predicted results correlate with reference CFD data.
- Indicates the average deviation between predicted and actual values (e.g., $C_d$).
- Shows how the prediction errors are distributed around the mean.
- Puts the errors into percentage form relative to a typical baseline (e.g., the nominal drag coefficient of a baseline geometry).

Together, these metrics give engineers a comprehensive picture of how each model behaves on both training and test sets.

### Comparison of Models 1, 2, and 3  

| Model     | Training R² Score | Test R² Score | Training MAE | Test MAE | Training Std Dev | Test Std Dev | Training Relative MAE (%) | Test Relative MAE (%) |
|-----------|--------------------|---------------|--------------|----------|------------------|--------------|---------------------------|------------------------|
| Model 1   | 0.930             | 0.610         | 0.0053       | 0.0110   | 0.0058           | 0.0115       | 2.5                       | 4.8                    |
| Model 2   | 0.925             | 0.620         | 0.0051       | 0.0108   | 0.0056           | 0.0112       | 2.4                       | 4.7                    |
| Model 3   | 0.940             | 0.630         | 0.0050       | 0.0105   | 0.0055           | 0.0110       | 2.3                       | 4.5                    |

- **Model 1** and **Model 2** each exhibit strong performance on their respective geometry families in training but show moderate drops in $R^2$ and increased MAE on unseen test data. This is expected since test conditions may involve shape or flow variations not present in the training set.  
- **Model 3**, trained on both designs, achieves slightly higher test-set $R^2$ and lower MAE, suggesting that exposure to diverse geometric modifications helps the model learn more generalized aerodynamic relationships.

### Quality of Field Variable Predictions  

For more nuanced validation, predicted flow fields (e.g., surface pressure, velocity contours, turbulent kinetic energy) can be compared against CFD references. Visual inspections often confirm whether the GDL model reproduces key flow features like stagnation regions, vortical structures, and trailing wake patterns. While minor discrepancies may arise—especially in regions of high curvature or strong flow separation—the overall accuracy often proves sufficient for early-stage design exploration or parametric studies.
