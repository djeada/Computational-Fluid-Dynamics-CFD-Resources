# Reduced Order Modeling in CFD

Reduced Order Modeling (ROM) simplifies complex computational models while retaining essential features and accuracy, particularly in computational fluid dynamics (CFD). This approach reduces the computational cost of simulations.

## Key Points

- **Purpose**: Simplifies complex models for real-time simulation, optimization, and control in CFD.
- **Methodology**: Builds on techniques like Proper Orthogonal Decomposition (POD) to create simplified models that accurately represent complex systems.
- **Basis Functions**: The core idea is to find problem-dependent bases that represent parameterized solutions of PDEs (Partial Differential Equations).
- **Early Works**: Initial approaches lacked a posteriori error estimators, crucial for determining the reliability of the output.
- **Advancements**:
  - Development of effective sampling strategies, especially for problems with many parameters.
  - Greedy algorithms, directly applicable in multi-dimensional parameter domains, have advantages over POD but require a posteriori error bounds.
- **Applications**: ROM has been extended to non-coercive, nonlinear, and time-dependent problems.
- **Discretization Techniques**: Initially focused on finite element discretizations but has since extended to other methods like finite volume frameworks.

## Comparison of Methods

- **POD**: Applied mostly in one-dimensional space, simpler but less flexible.
- **Greedy Approach**: More flexible, applicable in multi-dimensional parameter domains, but depends on having a posteriori error bounds.


## Detailed Description of ROM

### Key Concepts in ROM

1. **High-Fidelity Model**: Start with a detailed, high-fidelity CFD model that accurately captures the physics of the problem.
2. **Data Collection**: Gather simulation data (snapshots) from the high-fidelity model under various conditions.
3. **Dimensionality Reduction**: Use techniques like POD to reduce the dimensionality of the data, identifying the most important modes.
4. **Model Reduction**: Develop a reduced-order model that approximates the behavior of the high-fidelity model using the identified modes.
5. **ROM Validation**: Validate the reduced-order model against the high-fidelity model to ensure accuracy.

### Steps in ROM

1. **Construct High-Fidelity Model**:
    - Develop a detailed CFD model that solves the full set of governing equations.
    - Perform simulations to capture the behavior of the system under different scenarios.

2. **Collect Snapshots**:
    - Collect a series of snapshots representing the state of the system at different time steps or parameter values.
    - Organize these snapshots into a matrix $ \mathbf{X} $, where each column represents a snapshot.

3. **Perform POD**:
    - Apply Proper Orthogonal Decomposition to the snapshot matrix to identify the dominant modes.
    - Compute the correlation matrix $ \mathbf{C} = \mathbf{X}^T \mathbf{X} $ and perform eigenvalue decomposition to obtain the eigenvalues and eigenvectors.

4. **Build Reduced-Order Model**:
    - Construct the ROM using the most energetic modes obtained from POD.
    - Approximate the original high-fidelity model using a linear combination of these modes.

5. **Solve the ROM**:
    - Solve the reduced-order model for new conditions or parameter values.
    - The ROM requires significantly less computational resources compared to the high-fidelity model.

6. **Validate and Refine**:
    - Compare the ROM results with those from the high-fidelity model to ensure accuracy.
    - Refine the ROM as necessary to improve its predictive capabilities.

### Example: Application in CFD

1. **High-Fidelity Simulation**:
    - Perform high-fidelity simulations of a turbulent flow around an airfoil using a detailed CFD model.
    - Collect velocity and pressure fields as snapshots over time.

2. **POD Analysis**:
    - Apply POD to the collected snapshots to identify the dominant flow structures (modes).
    - Retain the most significant modes to form the basis of the ROM.

3. **ROM Development**:
    - Develop a ROM that uses the retained modes to approximate the flow field.
    - Implement the ROM to perform rapid simulations of the flow under varying conditions.

4. **Validation**:
    - Validate the ROM by comparing its predictions with high-fidelity simulation results for different flow scenarios.
    - Ensure the ROM accurately captures the essential dynamics of the flow.

## Conclusion

Reduced Order Modeling is a crucial technique in CFD for simplifying complex simulations while maintaining accuracy. By leveraging methods like POD, ROM enables efficient analysis, real-time simulation, and optimization of fluid flows. ROM is particularly valuable in applications requiring multiple simulations, such as design optimization and control.

## Further Reading

1. **Books**
    - "Model Reduction and Approximation: Theory and Algorithms" by Peter Benner, Albert Cohen, Mario Ohlberger, and Karen Willcox.
    - "Reduced Order Methods for Modeling and Computational Reduction" by Alfio Quarteroni and Gianluigi Rozza.

2. **Research Papers**
    - "Model Reduction for Flow Analysis and Control" by Berkooz, Holmes, and Lumley.
    - "A Comparison of Reduced-Order Modeling Techniques for Fluid Flows" by Rowley et al.

3. **Online Resources**
    - Online courses on model reduction and ROM.
    - Tutorials and example codes available on GitHub and other repositories.
