# Flow Feature Extraction

Machine learning's key capabilities include pattern detection and data mining. The machine learning community has produced several methods that work well with spatiotemporal fluid data.

- Unlike image classification, where large datasets like ImageNet are available (15 million labeled images), fluid mechanics lacks vast, labeled datasets.
- Future prospects include curating large, labeled fluid databases to facilitate deep learning algorithms.

Overview:

- **Dimensionality Reduction**: Techniques to reduce data dimensions, both linear and nonlinear.
- **Clustering and Classification**: Methods to categorize and identify patterns in fluid data.
- **Data Processing**: Techniques for processing experimental flow field data and strategies for rapid measurement and calculation.

## Dimensionality Reduction: Linear and Nonlinear Embeddings

### Linear Embeddings

- **Orthogonal Linear Transformation**: Used to convert physical coordinates into a modal basis.
- **Proper Orthogonal Decomposition (POD)**:
  - Provides an orthogonal basis for intricate geometries using empirical measurements.
  - **Snapshot POD**: Introduced by Sirovich in 1987, simplifies computation using a data-driven approach through singular value decomposition.
  - POD was also applied by Sirovich to create a low-dimensional feature space for human face classification, a fundamental aspect of modern computer vision.

### Principal Component Analysis (PCA)

- PCA, closely related to POD, is a fundamental algorithm in applied statistics and machine learning.
- **Purpose**: Describes correlations in high-dimensional data.
- **Representation**: Can be viewed as a two-layer neural network (autoencoder) that compresses high-dimensional data into a compact representation.
  - The network transforms high-dimensional data into a lower-dimensional latent space and then decodes it back.
  - When network nodes are linear and the encoder and decoder are transposes of each other, the autoencoder resembles POD/PCA decomposition.
  - **Modularity**: Allows incorporation of nonlinear activation units, enabling the development of nonlinear embeddings for more concise coordinates.

### Nonlinear Embeddings

- **Deep Neural Networks (DNNs)**: Based on the universal approximation theorem, deep NNs can represent complex input-output functions.
  - Initial applications included reconstructing the near-wall velocity field in a turbulent channel flow using wall pressure and shear.
  - Modern ML provides more powerful autoencoders, warranting further exploration of this connection.
  - **Deep Learning**: Requires large volumes of training data, usually good for interpolation but may not be suitable for extrapolation if new data distributions differ from the training data.

## Sparse and Randomized Methods

Machine learning (ML) approaches and developments in sparse optimization and randomized linear algebra work synergistically, offering new opportunities and efficiencies, especially in situations where processing, storage, or data collection resources are limited.

### Overview

- **Sparse Optimization**: Focuses on solutions with few non-zero components, allowing compact data representation.
- **Randomized Linear Algebra**: Uses randomization techniques to approximate matrix operations efficiently.
- **Compressed Sensing**: Acquires and reconstructs signals from a reduced set of measurements, ideal for sparse data.

### Synergy Between Sparse Methods and ML

1. **Sparse Optimization**:
   - **Definition**: Deals with problems where the solution is sparse, i.e., having few non-zero components.
   - **Benefits**: 
     - Enhances ML models by reducing the number of features or parameters.
     - Improves model interpretability and computational efficiency.
     - Often enhances generalization to new data.
   
2. **Randomized Linear Algebra**:
   - **Definition**: Involves using randomization techniques to approximate matrix operations.
   - **Benefits**:
     - Faster and more memory-efficient than traditional methods.
     - Useful for dimensionality reduction, matrix factorization, and solving linear systems.
     - Leverages low-dimensional structure in data to enhance computational efficiency.
     - **Example**: Efficient computation of Singular Value Decomposition (SVD), crucial for Principal Component Analysis (PCA).

### Applications in Fluid Mechanics

1. **Compressed Sensing**:
   - **Definition**: Technique for acquiring and reconstructing sparse or compressible signals from a reduced set of measurements.
   - **Applications**:
     - **Wall-Bounded Turbulence**: Used to create concise representations, reducing data volume needed for accurate depiction.
     - **POD-Based Flow Reconstruction**: Employed with Proper Orthogonal Decomposition (POD) to reconstruct flows efficiently, facilitating rapid decision-making in control systems.

2. **Randomized Linear Algebra Techniques**:
   - **Enhancements**: Randomized methods significantly reduce computational costs for matrix decompositions while preserving essential data structures.
   - **Practical Application**: Efficient SVD computation, crucial for tasks like PCA, allowing for rapid processing of large datasets.

### Benefits of Sparse and Randomized Methods

- **Efficiency**: Reduce data volume and computational resources required.
- **Speed**: Enable rapid measurement and calculation, critical for real-time applications.
- **Accuracy**: Maintain accuracy in data representation and reconstruction with fewer resources.
- **Practicality**: Suitable for large-scale problems where traditional methods are impractical due to resource constraints.

## Clustering and Classification

Machine learning (ML) relies heavily on clustering and classification techniques. These methods are essential for organizing and categorizing data, with various well-established algorithms available to suit different data sizes and desired categories.

### Clustering

- **Purpose**: Groups data points into clusters based on similarity, making it easier to analyze and interpret large datasets.
- **k-Means Algorithm**:
  - **Application**: Kaiser et al. (2014) used k-means to discretize a high-dimensional phase space for fluid mixing, developing tractable Markov transition models to capture flow evolution.
  - **Interpretation**: Associating each cluster centroid with a physical flow field enhances result interpretation.
  - **Stability and Robustness**: Amsallem et al. (2012) employed k-means clustering to partition phase space, improving stability and robustness in the presence of parameter variations.
  
### Classification

- **Purpose**: Differentiates between different behaviors and dynamic regimes using labeled data to develop models that classify new data into specific categories.
- **Supervised Learning**:
  - **Neural Networks and Vorticity Measurements**: Colvert et al. (2018) investigated the classification of wake topology.
  - **k-Nearest Neighbors and Dynamical Systems Models**: Wang & Hemati (2017) and Hou et al. (2019) used these algorithms to detect flow disturbances and estimate their parameters.
  - **Graph and Network Approaches**: Nair & Taira (2015) and Meena et al. (2018) utilized these techniques for community detection in wake flows.
  
### Notable Studies

- **Sparse Representation Methods**: Early examples like Bright et al. (2013) applied sparse representation methods to fluid dynamics.
- **Community Detection**: Graph-based approaches have proven effective in identifying distinct flow structures and behaviors within fluid datasets.

### Applications in Fluid Dynamics

1. **Phase Space Discretization**:
   - **K-Means Clustering**: Helps in developing models to understand and predict fluid behavior over time.
   - **Markov Transition Models**: Capture the evolution of flow, providing insights into fluid dynamics.

2. **Classification of Wake Topology**:
   - **Neural Networks**: Effective for classifying complex fluid behaviors using measurements like vorticity.
   - **Parameter Estimation**: Algorithms like k-nearest neighbors combined with dynamical systems models help in estimating parameters of flow disturbances.

3. **Community Detection in Wake Flows**:
   - **Graph Approaches**: Useful for identifying and analyzing communities within wake flows, revealing underlying patterns and structures.



