# Introduction to Machine Learning for CFD

In fluid mechanics, handling vast amounts of data has been a longstanding practice. This data is sourced from experiments, field measurements, and extensive numerical simulations. With the advent of high-performance computing architectures and advancements in experimental measurement capabilities, big data has become an integral part of fluid mechanics research in recent decades.

## Evolution of Data Handling in Fluid Mechanics

- **Historical Context**: 
  - Over the past 50 years, numerous techniques have been developed to manage the growing volumes of data.
- **Techniques**: 
  - Sophisticated algorithms for data processing and compression.
  - Establishment of fluid mechanics databases.
- **Traditional Analysis**: 
  - Relied on domain expertise, statistical analysis, and heuristic algorithms.

## Cross-Disciplinary Data Proliferation

- The proliferation of data extends beyond fluid mechanics to various scientific disciplines.
- Extracting valuable insights and actionable information from data has become a new approach to scientific inquiry and a lucrative commercial prospect.

## Factors Driving the Advancement of Machine Learning (ML)

Our current generation is witnessing an unprecedented convergence of factors:

1. **Exponential Growth in Data Volume**:
   - Increasing availability of data from various sources.
   
2. **Advancements in Computational Hardware**:
   - Reduced costs for computation, data storage, and transfer.
   
3. **Availability of Sophisticated Algorithms**:
   - Enhanced algorithms for data analysis.
   
4. **Open-Source Software and Benchmark Problems**:
   - Facilitates widespread use and development of ML techniques.
   
5. **Industry Investments**:
   - Significant investments in data-driven problem-solving.

## Impact on Fluid Mechanics

- The advancements in ML have reignited interest and progress in extracting information from vast datasets in fluid mechanics.
- ML is rapidly gaining ground in the realm of fluid mechanics, offering new methodologies for data analysis and interpretation.

## Categories of Machine Learning

Learning algorithms can be classified into three categories: supervised, semi-supervised, and unsupervised learning, depending on the extent of information available to the learning machine (LM) about the data.

### Supervised Learning

Supervised learning involves training a model on a labeled dataset, where the desired output is known. This means that for each input, there is a corresponding output which the model aims to predict. It can be divided into three main types: classification, regression, and optimization and control.

- **Classification**: Predicts categorical labels.
  - **Support Vector Machines (SVM)**: Finds the hyperplane that best separates different classes.
  - **Decision Trees**: Splits the data into subsets based on the value of input features.
  - **Random Forests**: An ensemble of decision trees to improve prediction accuracy.
  - **Neural Networks**: Models inspired by the human brain, capable of capturing complex patterns.
  - **k-Nearest Neighbor (k-NN)**: Classifies based on the majority label of the nearest data points.

- **Regression**: Predicts continuous values.
  - **Linear Regression**: Models the relationship between two variables by fitting a linear equation.
  - **Generalized Linear Models**: Extends linear regression for various distributions of the output variable.
  - **Gaussian Process Regression**: Uses probability distributions over functions to make predictions.

- **Optimization and Control**: Optimizes performance measures and controls system behavior.
  - **Linear Control**: Uses linear equations to control system dynamics.
  - **Genetic Algorithms**: Mimics natural evolution to optimize solutions.
  - **Deep Model Predictive Control**: Uses deep learning for predicting future states and optimizing controls.
  - **Estimation of Distribution Algorithms**: Builds probabilistic models of good solutions to guide search.
  - **Evolutionary Strategies**: Optimizes by iterating and selecting the best candidates.

### Semi-Supervised Learning

Semi-supervised learning uses both labeled and unlabeled data for training. This approach is particularly useful when obtaining labeled data is expensive or time-consuming, combining the strengths of supervised and unsupervised learning.

- **Reinforcement Learning**: Involves an agent learning to make decisions by taking actions in an environment to maximize some notion of cumulative reward.
  - **Q-Learning**: Learns the value of actions in given states to find the optimal policy.
  - **Markov Decision Processes (MDP)**: A mathematical framework for modeling decision-making.
  - **Deep Reinforcement Learning**: Combines deep learning with reinforcement learning to handle high-dimensional state spaces.

### Unsupervised Learning

Unsupervised learning is used when the model is provided with data without explicit instructions on what to do with it. The model tries to learn the patterns and the structure from the data without labeled outputs.

- **Generative Models**: Aim to generate new data points with similar properties to the training data.
  - **Generative Adversarial Networks (GANs)**: Consist of two neural networks competing against each other to generate realistic data.

- **Clustering**: Groups data points into clusters based on similarity.
  - **k-Means**: Partitions data into k clusters by minimizing the variance within each cluster.
  - **Spectral Clustering**: Uses the eigenvalues of a similarity matrix to perform dimensionality reduction before clustering.

- **Dimensionality Reduction**: Reduces the number of random variables under consideration.
  - **Proper Orthogonal Decomposition (POD) / Principal Component Analysis (PCA)**: Identifies the directions (principal components) that maximize variance in the data.
  - **Autoencoders**: Neural networks used to learn efficient codings of input data.
  - **Self-Organizing Maps**: Reduces dimensions while preserving the topological properties of the data.
  - **Diffusion Maps**: Uses the connectivity of data points to reduce dimensions.

