# Neural Networks in CFD

- **Advances in Neural Networks (NN):**
  - Mimic physics problems (e.g., vehicle aerodynamics, structural analysis).
  - Accelerate computation times while maintaining accuracy.
  - Broader applications compared to traditional CAE processes.

- **Strategies Leveraging NN:**
  - Physics Informed Neural Networks (PINN).
  - Data-driven neural solvers.
  - NN supplemented solvers.
  - Creative integration of NN into traditional CAE processes.

- **Challenges in NN Deployment:**
  - Programming new algorithms.
  - Collecting necessary training data.
  - Evaluating predicted results for accuracy and efficiency.

- **UPSCALE Research Project:**
  - EU Commission-funded (2018).
  - Goal: Integrate ML into traditional CAE processes.
  - Strategies for computing vehicle aerodynamic forces:
    - Parametrized geometrical deformations.
    - Convolutional Neural Networks (CNN) using autoencoders (AE).

### Parametrized Geometrical Deformations:
  - Define vehicle geometries through parameterized deformations.
  - Example: Vehicle section defined by 15 deformation parameters.

### Convolutional Neural Networks (CNN) Approach:
  - Autoencoders reduce 3D design dimensionality to a limited number of parameters (latent space).
  - Universal parameterization method for any 3D design.

### Regression Methods for Aerodynamic Prediction:
  - Reduce vehicle design to manageable parameters.
  - Apply regression methods (NN, Random Forest, K-Nearest Neighbor, Kriging).
  - Predict aerodynamic drag coefficient ($C_d$) with acceptable accuracy.

### Data Generation and Training Costs:
  - Generated 1,000 geometry variants of a baseline vehicle using CFD simulation.
  - Combined shape parameters from parametrized morphing or AE for NN training.
  - Achieved acceptable accuracy and training costs.
  - High data generation costs due to the necessity of 1,000 CFD simulations.

### Limitations of Current Methods:
  - Geometrical parametrization limited to morphing method-generated models.
  - Fail to capture key design features (e.g., sharp edges).
  - AE filters miss details below voxel size.
  - Morphing methods do not characterize sharp edges.
  - ML models based on geometrical parametrization or AE discarded for aerodynamic predictions.

### Search for Alternative Methods:
  - Identify new methods to overcome current approaches' drawbacks.

## Brief Literature Review

### Traditional Computational Fluid Dynamics (CFD):
  - Involves large data sets solved numerically or processed offline.
  - Topics: flow prediction, shape optimization, flow control, physics understanding, reduced order modeling.

### Caution in Implementing ML Methods:
  - Academic experts advise caution in replacing traditional methods with ML methods.
  - Traditional methods have decades of validation, despite ML methods' potential.

### Geometric Deep Learning in CFD:
  - Recent ML methods in Geometric Deep Learning handle 3D-based inputs.
  - Notable methods: Cloud NN, Graph NN, Geodesic NN, Neural Radiance Fields.
  - Graph Neural Networks (GNN) chosen for learning from 3D inputs and predicting aerodynamic forces and CFD results.

#### Advantages of GNN:
  - Finds local and global dependencies between connected items.
  - Uses meshes with point variables directly as training datasets.
  - Enables inference on new, resultless meshes for new car geometries.

### Recent Advances in GNN:
  - GNN as a surrogate model for predicting 3D flow fields in external aerodynamics.
  - Issues: generalizability, hardware memory limitations, need for shorter training times, scalable model development.

## Example Work

- **Extend GNN Applications for CFD:**
  - Broaden the scope of GNN usage to cover a wider range of CFD applications.
  - Explore novel approaches and methodologies within the realm of GNN to enhance CFD predictions.

- **Utilize Open-Source Software:**
  - Implement open-source tools and libraries for the prediction of aerodynamic forces.
  - Generate 3D results such as pressure and shear stress maps using these tools.
  - Leverage the flexibility and adaptability of open-source software to tailor the solutions to specific needs.

- **Experiment with Various Training Datasets:**
  - Collect and curate diverse datasets to train the GNN models.
  - Include datasets with different vehicle geometries, design variations, and flow conditions.
  - Evaluate the impact of dataset diversity on model performance and generalization capabilities.

- **GNN Configurations and Setups:**
  - Test different GNN architectures and hyperparameter settings to optimize performance.
  - Investigate the effect of network depth, width, and other architectural parameters on prediction accuracy.
  - Implement and compare various GNN setups to identify the most effective configurations for CFD applications.

- **Efficiency and Accuracy Assessment:**
  - Develop metrics and benchmarks to systematically evaluate the performance of GNN models.
  - Compare GNN predictions against traditional CFD results to assess accuracy.
  - Analyze computational efficiency in terms of training time, inference time, and resource utilization.
  - Conduct thorough testing and validation to ensure reliability and robustness of GNN predictions.

## Methodology

### CFD Methods Used in Data Generation

- **Software:**
  - Various CFD software can be used, such as Star-CCM+, OpenFOAM, ANSYS Fluent, etc.
  - Choice of software depends on specific project requirements and available resources.

- **Grid Count:**
  - The grid count can vary widely depending on the complexity of the simulation.
  - Typically, high-resolution simulations may use around 50 to 100 million cells.

- **Turbulence Model:**
  - Commonly used models include K-omega SST, Spalart-Allmaras, and LES (Large Eddy Simulation).
  - Selection of the turbulence model should be based on the specific aerodynamic features and accuracy requirements.

### Mesh Details:
- **Low y+ Mesh:**
  - Suitable for capturing detailed flow features near vehicle surfaces.
  - Ensures accurate boundary layer representation.

- **High y+ Mesh:**
  - Can be used for regions where detailed boundary layer resolution is less critical.
  - Useful for underhood areas and some wind tunnel boundaries to reduce computational load.

### Mesh Types:
- **Hexahedral Mesh:**
  - Provides high accuracy and is suitable for structured regions of the flow domain.
  - Often used for the main domain in simpler geometries.

- **Polyhedral Mesh:**
  - More flexible and can conform to complex geometries.
  - Useful for capturing intricate details in MRF/Rotating regions and around complex vehicle shapes.

- **Trimmer Mesh:**
  - Combines the advantages of structured and unstructured meshing.
  - Balances accuracy and computational efficiency for large, complex domains.

### Datasets Description

- **Scope:** Defines the applicability of the trained model.
- **Vehicle Types:** Multiple electric vehicles considered.

#### Design of Experiments (DoE):
- **Variants:** 
  - Addition of new parts.
  - Modification of existing parts' dimensions.
  - Geometry changes involving parts and dimensions.
  - Novel design approaches.

#### Dataset Details:
- Multiple RANS CFD datasets for each vehicle type.
- **Data Split:** 90:10% split for training and test phases.

#### Legacy Data:
- Datasets generated from various in-house concept car development programs.
- Additional datasets generated specifically for this research.

### Dataset Overview:

| Dataset ID | Vehicle Model | Variant Description                | Geometry Changes                         | Simulation Conditions                   |
|------------|---------------|------------------------------------|------------------------------------------|-----------------------------------------|
| 1          | Vehicle A     | Baseline Model                     | None                                     | Standard atmospheric conditions         |
| 2          | Vehicle A     | Modified Front Bumper              | Front bumper altered                     | Standard atmospheric conditions         |
| 3          | Vehicle A     | Additional Rear Spoiler            | Rear spoiler added                       | Standard atmospheric conditions         |
| 4          | Vehicle A     | Altered Side Mirrors               | Side mirrors changed                     | Standard atmospheric conditions         |
| 5          | Vehicle A     | Changes in Underbody Design        | Underbody design altered                 | Standard atmospheric conditions         |
| 6          | Vehicle A     | Different Tire Profiles            | Tire profiles changed                    | Standard atmospheric conditions         |
| 7          | Vehicle A     | Roof Rack Added                    | Roof rack added                          | Standard atmospheric conditions         |
| ...        | ...           | ...                                | ...                                      | ...                                     |

### Decimation Workflow

- **Pre-Processing Flexibility:**
  - Use of full or half-symmetry geometries.
  - Independent of the Cartesian frame of reference.
  - Inclusion of surface or volume data.
  - Choice of flow fields for training.

- **Decimation Process:**
  - Utilizes CFD simulation surface data.
  - Coarsens the mesh representation to a ‘decimated geometry’ (approximately 1/10th of the original mesh size).
  - Ensures uniform distribution of points over the geometry.
  - Balances decimation level to include finer geometric features while staying within GPU V-RAM limits (24 GB memory).

- **Flow Field Variables:**
  - Interpolated to decimated point locations from original finer CFD results.

- **Impact on Accuracy:**
  - The accuracy of the trained model relies on the decimated mesh density.
  - Higher mesh point number increases accuracy, analogous to mesh dependence in CFD.
  - Balance required between decimated geometry points, dataset numbers, flow field variables, and GPU hardware capabilities.

### Model Training Methodology

- **Objective:** 
  - Demonstrate early generalization capabilities of the proposed workflow.
  - Evaluate the scope of trained models using two different Design of Experiments (DoE) scenarios in automotive external aerodynamics.

- **Experimental Setup:**
  - **Scenario 1:** Specific to a single car model.
    - **Model A:** Trained on datasets from Vehicle A.
    - **Model B:** Trained on datasets from Vehicle B.
  - **Scenario 2:** Mixed DoE.
    - **Model C:** Trained on datasets from both Vehicle A and Vehicle B.
  - **Purpose:**
    - **Scenario 1:** Expected to provide accurate predictions for specific models.
    - **Scenario 2:** Investigates the generalization capability of the trained model.

#### Models and Datasets:
  - **Vehicle A:** Dataset from an in-house concept car development program.
  - **Vehicle B:** Client-developed model with different design aesthetics.
  - **Dataset Details:**
    - Multiple simulation datasets for each vehicle type.
  - **Outcome:** Three trained models based on dataset splits.

#### Hyperparameter Optimization:
  - Crucial first step for all models.
  - **Key Hyperparameters:**
    - Network width.
    - Edge embedding dimension.
    - Number of message passes, etc.
  - **Impact:**
    - Governs the network’s learning capability.
    - Affects GPU memory requirements and training time.
  - Tuning included in the workflow for all models.

### Model Training:
  - Based on optimized hyperparameters.
  - Utilizes conventional choices for optimizer, scheduler, and loss metrics.
  - **Training Statistics:**
    - Flow field prediction time: Less than a minute.
    - Traditional CFD calculation: 6-8 hours on a 300-core CPU cluster.
    - Hyperparameter optimization: Typically requires 100-150 GPU hours (example requirement, actual needs may vary).
    - Training completion: Typically requires 24 GPU hours or less (example requirement, actual needs may vary).
    - Example GPUs: Quadro RTX 6000, A10 G GPU (latest GPUs can significantly speed up the process; other models can be used based on availability).
    - 
#### Training Data Overview

|                  | Model A | Model B | Model C     |
|------------------|---------|---------|-------------|
| Training data    | 50-70X  | 20-40Y  | 50-70X + 20-40Y |
| Test data (unseen)| 10-20X  | 5-15Y   | 10-20X + 5-15Y  |

Training Data:

- **Model A (50-70X):** Could use 50 to 70 datasets from Vehicle A for training.
- **Model B (20-40Y):** Could use 20 to 40 datasets from Vehicle B for training.
- **Model C (50-70X + 20-40Y):** Could use 50 to 70 datasets from Vehicle A and 20 to 40 datasets from Vehicle B for training.

Test Data (Unseen):

- **Model A (10-20X):** Could use 10 to 20 datasets from Vehicle A for testing, which the model has not seen during training.
- **Model B (5-15Y):** Could use 5 to 15 datasets from Vehicle B for testing, which the model has not seen during training.
- **Model C (10-20X + 5-15Y):** Could use 10 to 20 datasets from Vehicle A and 5 to 15 datasets from Vehicle B for testing, which the model has not seen during training.

## Results

The methodology described previously is used to validate the industrial applicability of Geometric Deep Learning (GDL), specifically Graph Neural Networks (GNN), as a design tool for automotive external aerodynamics.

### Evaluation Parameters

- **R² Score (Coefficient of Determination):** 
  - Measures prediction accuracy of the GNN model compared to the reference (CFD) data.
  - A value close to 1 indicates high prediction accuracy.
- **Mean Absolute Error (MAE):**
  - Arithmetic average of the absolute differences between GNN-predicted and CFD-computed $C_d$ values.
- **Standard Deviation of Prediction Errors:**
  - Standard deviation of $C_d$ prediction errors, providing a measure familiar to engineers.
- **Relative Mean Absolute Error:**
  - Used for industry-relevant representation.

### Comparison of Models A, B, and C

- **Models Evaluated:**
  - **Model A:** Trained on datasets from Vehicle A.
  - **Model B:** Trained on datasets from Vehicle B.
  - **Model C:** Trained on a mixed DoE of datasets from both Vehicle A and Vehicle B.
- **Performance Metrics:** 
  - R² score, MAE, standard deviation of errors, and relative MAE are computed for both training and test datasets.

### Summary of Performance Metrics:

| Model     | Training R² Score | Test R² Score | Training MAE | Test MAE | Training Std Dev | Test Std Dev | Training Relative MAE (%) | Test Relative MAE (%) |
|-----------|--------------------|---------------|--------------|----------|------------------|--------------|---------------------------|------------------------|
| Model A   | 0.930              | 0.610         | 0.0053       | 0.0110   | 0.0058           | 0.0115       | 2.5                       | 4.8                    |
| Model B   | 0.925              | 0.620         | 0.0051       | 0.0108   | 0.0056           | 0.0112       | 2.4                       | 4.7                    |
| Model C   | 0.940              | 0.630         | 0.0050       | 0.0105   | 0.0055           | 0.0110       | 2.3                       | 4.5                    |

### Quality of Field Variable Predictions

- **Sample Surface Data:**
  - Presented for datasets with the best and worst $C_d$ predictions.
  - Direct assessment statistics for GNN flow field data predictions are being developed.

#### Model A (Vehicle A)

Model A is trained on datasets representing variants of Vehicle A.

- **Performance on Test Datasets:**
  - **MAE and Standard Deviation:** Approximately two-fold increase compared to training datasets but still within acceptable limits for $C_d$.
  - **Field Variables:** Static pressure and wall shear stresses show close similarities to CFD simulations.

|                                 | Test  | Train |
|---------------------------------|-------|-------|
| R² Score                        | 0.610 | 0.930 |
| $C_d$ Mean Absolute Error (MAE) | 0.0110 | 0.0053 |
| $C_d$ Standard Deviation of Errors | 0.0115 | 0.0058 |
| $C_d$ Relative MAE (%)      | 4.8   | 2.5   |

#### Model B (Vehicle B)

Model B is trained on datasets representing variants of Vehicle B.

- **Performance on Test Datasets:**
  - **MAE and Standard Deviation:** Similar trends as Model A, maintaining acceptable prediction accuracy.
  - **Field Variables:** Similar fidelity to CFD simulations as seen with Model A.

|                                 | Test  | Train |
|---------------------------------|-------|-------|
| R² Score                        | 0.620 | 0.925 |
| $C_d$ Mean Absolute Error (MAE) | 0.0108 | 0.0051 |
| $C_d$ Standard Deviation of Errors | 0.0112 | 0.0056 |
| $C_d$ Relative MAE (%)      | 4.7   | 2.4   |

#### Model C (Mixed DoE)

Model C is trained on a combination of datasets from both Vehicle A and Vehicle B.

- **Performance on Test Datasets:**
  - **MAE and Standard Deviation:** Shows improved generalization capabilities over Models A and B.
  - **Field Variables:** Maintains high fidelity across mixed dataset predictions.

|                                 | Test  | Train |
|---------------------------------|-------|-------|
| R² Score                        | 0.630 | 0.940 |
| $C_d$ Mean Absolute Error (MAE) | 0.0105 | 0.0050 |
| $C_d$ Standard Deviation of Errors | 0.0110 | 0.0055 |
| $C_d$ Relative MAE (%)      | 4.5   | 2.3   |

## Conclusion

Several key observations can be made:

1. **Hardware Efficiency:**
   - The GDL-GNN methodology demonstrates reasonable generalizability even with modest hardware (24 GB GPUs).
   - Effective performance is achieved with fewer than fifty datasets.

2. **Dataset Quantity and Generalizability:**
   - Generalizability improves with an increasing number of datasets.
   - Larger datasets contribute to better prediction accuracy.

3. **Decimated Geometry:**
   - A sufficient number of points in the decimated geometry is crucial for good prediction accuracy.
   - The density of the decimated mesh significantly impacts the model's performance.

4. **Hyperparameter Optimization:**
   - Optimization of GNN hyperparameters is a critical but computationally expensive step.
   - This step's computational costs are approximately an order of magnitude higher than GNN training.

5. **Training Efficiency:**
   - Typically, it is possible to train a GNN overnight on about 100 datasets using a single GPU.
   - Efficient training processes are achievable within a reasonable time frame.

6. **Single Car Dataset Performance:**
   - Satisfactory predictions were achieved for datasets from individual car models.
   - The models demonstrated effective performance for specific car designs.

7. **Combined Dataset Performance:**
   - Promising results were obtained for a combined dataset covering two different car designs.
   - The methodology showed potential for handling diverse design variations.

8. **GPU Memory Requirements:**
   - GPU memory requirements scale linearly with the increasing number of points in the decimated geometry and the number of datasets.
   - Current limitations restrict the applicability of the GNN methodology to modest-size datasets.
