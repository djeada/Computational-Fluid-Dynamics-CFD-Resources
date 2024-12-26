## Model Training Methodology  
A core objective of this methodology is to show how a geometric deep learning (GDL) workflow can generalize to different automotive exterior designs, using two distinct Design of Experiments (DoE) scenarios in external aerodynamics. The first scenario trains separate models for a single car design each (Vehicle A or Vehicle B). The second mixes data from both vehicles to assess if a shared model can produce accurate results on unseen designs. This setup offers insight into whether a GNN approach can remain robust when faced with entirely new geometry.

The experimental setup revolves around two major scenarios. In Scenario 1, Model A relies solely on Vehicle A data and Model B on Vehicle B data. These models are tailored for their respective designs and are expected to excel at predicting aerodynamic forces for variants that do not deviate too far from their training samples. In Scenario 2, Model C draws on a combined dataset from both Vehicle A and Vehicle B, with the aim of testing broader generalization across different styling cues, geometrical proportions, or flow conditions.

### Models and Datasets  
Vehicle A relies on data generated from an in-house concept car program, while Vehicle B references a client-developed design with its own unique features. Each vehicle’s dataset comprises multiple CFD runs representing geometry changes, such as bumper modifications or spoiler additions. Model A trains on 50 to 70 simulations (X) from Vehicle A, reserving an additional 10 to 20 simulations (X) for testing. Model B follows a similar pattern with 20 to 40 simulations (Y) for training and 5 to 15 (Y) for testing. Model C mixes both vehicle datasets, combining 50 to 70 (X) with 20 to 40 (Y) for training, and 10 to 20 (X) plus 5 to 15 (Y) for testing.

Hyperparameter optimization is a pivotal step for each model. Network width, edge embedding dimension, and message-passing settings determine how the GNN interprets geometry and flow. Broader networks might capture more nuanced aerodynamic features but will demand additional GPU memory and training time. Tuning these parameters includes trial runs that can require substantial GPU hours. Once the best set of hyperparameters is pinned down, the actual model training typically finishes within a day of GPU time, depending on hardware availability.

An ASCII-style diagram can summarize the data flow and training process:

```
 +----------------+        +-----------------+       +-----------------+
 |  CFD Datasets  |  -->   | Hyperparameter  |  -->  |  GNN Training   |
 | (Vehicle A/B)  |        |  Optimization   |       |  & Validation   |
 +----------------+        +-----------------+       +-----------------+
     |                                                    |
     |  (Mesh & Flow                                      |
     |   Decimation)                                      |
     |                                                    |
     v                                                    v
 +----------------+                                 +-----------------+
 |  Decimated     |                                 |  Trained Model  |
 |  Geometries    |                                 | (A, B, or C)    |
 +----------------+                                 +-----------------+
```

This workflow clarifies how each model emerges from a combination of CFD outputs, decimated to manageable sizes, then fed into a GNN whose hyperparameters have been refined to yield the best predictive performance on drag coefficient or flow field variables.

Training time compares favorably to traditional CFD. Once trained, the GNN can produce flow field predictions in less than a minute, whereas a standard CFD run might occupy 6 to 8 hours on a 300-core CPU cluster. The up-front cost of hyperparameter tuning can total around 100 to 150 GPU hours, but final training often finishes in less than 24 hours on GPUs like the Quadro RTX 6000 or the A10 G.

### Training Data Overview  

|                  | Model A            | Model B            | Model C                  |
|------------------|--------------------|--------------------|--------------------------|
| Training data    | 50-70X            | 20-40Y            | 50-70X + 20-40Y          |
| Test data (unseen) | 10-20X            | 5-15Y              | 10-20X + 5-15Y           |

Model A uses X data points from Vehicle A, Model B uses Y data points from Vehicle B, and Model C fuses both into a combined training set. Test subsets always exclude any data seen during training, so each model’s ability to predict aerodynamic forces and flow fields is tested on genuinely unfamiliar configurations.

### Results  
The GNN methodology described above is validated by computing various performance metrics. Each model’s predictions are compared to reference CFD data, focusing on how well the GNN can reproduce the drag coefficient \(C_d\) and other field variables like pressure or shear stress.

### Evaluation Parameters  
Engineers rely on the R² (coefficient of determination) to measure correlation with the ground truth, while the mean absolute error (MAE) indicates the average discrepancy in predicted drag. A standard deviation of errors tracks how spread out these differences are, and a relative MAE in percentage form makes it easier to discuss the results in typical engineering terms.

### Comparison of Models A, B, and C  

| Model     | Training R² Score | Test R² Score | Training MAE | Test MAE | Training Std Dev | Test Std Dev | Training Relative MAE (%) | Test Relative MAE (%) |
|-----------|--------------------|---------------|--------------|----------|------------------|--------------|---------------------------|------------------------|
| Model A   | 0.930             | 0.610         | 0.0053       | 0.0110   | 0.0058           | 0.0115       | 2.5                       | 4.8                    |
| Model B   | 0.925             | 0.620         | 0.0051       | 0.0108   | 0.0056           | 0.0112       | 2.4                       | 4.7                    |
| Model C   | 0.940             | 0.630         | 0.0050       | 0.0105   | 0.0055           | 0.0110       | 2.3                       | 4.5                    |

Models A and B, each trained on a single vehicle’s data, attain high accuracy on their training sets but show some drop in performance on test sets. This gap is not unexpected, since the test conditions can include geometry or flow variations that the network has not encountered. Model C, drawing on both vehicles, has a slightly higher R² on test data, suggesting that mixing designs broadens the network’s generalization.

### Quality of Field Variable Predictions  
Surface data, including static pressure or wall shear stress, also compare well to CFD for the best and worst cases. While exact field-based statistics are still being refined, visual comparisons indicate that the GNN captures key flow patterns with minimal anomalies. Models A and B display twofold increases in error metrics when transitioning from training to unseen testing data, which still remains acceptable in many industrial contexts. Model C maintains a similar rate of error escalation but has a slight edge in absolute performance, highlighting its promise for general-purpose shape evaluations.

