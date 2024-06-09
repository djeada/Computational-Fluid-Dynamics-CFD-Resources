## The Singular Value Decomposition (SVD) and POD

### Equivalence of Direct POD and Snapshot POD
- **Overview**:
  - Both Direct POD and Snapshot POD are fundamentally related to the Singular Value Decomposition (SVD) of the snapshot matrix $\mathbf{U}$.
  - SVD provides a mathematical framework to decompose $\mathbf{U}$, revealing the intrinsic properties of the dataset.

- **SVD Decomposition**:
  - SVD factorizes a real $m \times n$ matrix $\mathbf{U}$ into three matrices:
    
$$
    \mathbf{U} = \mathbf{L} \mathbf{\Sigma} \mathbf{R}^T,
    $$

    where:
    - $\mathbf{L}$ is an $m \times m$ orthogonal matrix.
    - $\mathbf{\Sigma}$ is an $m \times n$ diagonal matrix containing the singular values.
    - $\mathbf{R}$ is an $n \times n$ orthogonal matrix.

### SVD and POD Connection
- **Covariance Matrices**:
  - From SVD, two important covariance matrices can be derived:
    
$$
    \mathbf{C} = \frac{1}{m-1} (\mathbf{U}^T \mathbf{U}) = \frac{1}{m-1} (\mathbf{R} (\mathbf{\Sigma}^T \mathbf{\Sigma}) \mathbf{R}^T),
    $$

    
$$
    \mathbf{C}_s = \frac{1}{m-1} (\mathbf{U} \mathbf{U}^T) = \frac{1}{m-1} (\mathbf{L} (\mathbf{\Sigma} \mathbf{\Sigma}^T) \mathbf{L}^T).
    $$

  - $\mathbf{C}$ is the $n \times n$ covariance matrix of the transposed snapshot matrix $\mathbf{U}^T$.
  - $\mathbf{C}_s$ is the $m \times m$ covariance matrix of the snapshot matrix $\mathbf{U}$.

### Key Observations
- **Diagonal Elements**:
  - $\mathbf{\Sigma}^T \mathbf{\Sigma}$ is an $n \times n$ diagonal matrix.
  - $\mathbf{\Sigma} \mathbf{\Sigma}^T$ is an $m \times m$ diagonal matrix.
  - The non-zero diagonal elements of $\mathbf{\Sigma}^T \mathbf{\Sigma}$ and $\mathbf{\Sigma} \mathbf{\Sigma}^T$ are the squares of the singular values of $\mathbf{U}$.

- **Relations**:
  - $\mathbf{\Lambda} = \mathbf{\Sigma}^T \mathbf{\Sigma}/(m-1)$: Eigenvalues of $\mathbf{C}$.
  - $\mathbf{\Phi} = \mathbf{R}$: Right singular vectors, spatial modes for Direct POD.
  - $\mathbf{A}_s = \mathbf{\Sigma} \mathbf{\Sigma}^T/(m-1)$: Eigenvalues of $\mathbf{C}_s$.
  - $\mathbf{\Phi}_s = \mathbf{L}$: Left singular vectors, temporal modes for Snapshot POD.
  - The eigenvalues $\lambda_i$ of $\mathbf{C}$ and $\mathbf{C}_s$ correspond to $\sigma_i^2/(m-1)$.

### POD Algorithms
- **Equivalence to SVD**:
  - Both Direct POD and Snapshot POD algorithms are equivalent to performing SVD on the scaled snapshot matrix $\mathbf{U}/\sqrt{m-1}$.
  - **Direct POD**:
    - Spatial modes (right singular vectors) are given by $\mathbf{R}$.
  - **Snapshot POD**:
    - Temporal modes (left singular vectors) are given by $\mathbf{L}$.
  - **Eigenvalues**:
    - The eigenvalues from POD are the squares of the singular values from the SVD of $\mathbf{U}$.

## Comparison

| **Method**       | **Procedure**                                                                                                                                                 | **Advantages**                                                                                                           | **Disadvantages**                                                                                                            |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| **POD**          | - Compute the covariance matrix $\mathbf{C} = \frac{1}{m-1} (\mathbf{U}^T \mathbf{U})$                                                                     | - Direct method                                                                                                          | - Computationally expensive for large datasets                                                                              |
|                  | - Perform eigenvalue decomposition on $\mathbf{C}$                                                                                                          | - Provides both spatial and temporal modes                                                                               | - Requires inverting large matrices                                                                                          |
|                  | - Eigenvalues are the variance in each direction                                                                                                              |                                                                                                                          |                                                                                                                              |
| **Snapshot POD** | - Compute the covariance matrix $\mathbf{C}_s = \frac{1}{m-1} (\mathbf{U} \mathbf{U}^T)$                                                                   | - Faster for $n > m$ (common in fluid dynamics)                                                                        | - Indirect method                                                                                                            |
|                  | - Perform eigenvalue decomposition on $\mathbf{C}_s$                                                                                                        | - Specifically developed for speeding up the process in large datasets                                                   |                                                                                                                              |
|                  | - Eigenvalues correspond to the temporal correlation of the snapshots                                                                                         | - More efficient in handling large matrices                                                                              |                                                                                                                              |
| **SVD**          | - Factorize $\mathbf{U}$ into $\mathbf{U} = \mathbf{L} \mathbf{\Sigma} \mathbf{R}^T$                                                                     | - Most economical in terms of lines of code                                                                              | - Requires normalization for consistency with POD                                                                            |
|                  | - Singular values $\sigma_i$ provide the same information as eigenvalues in POD                                                                             | - Provides both spatial and temporal modes                                                                               | - Computational cost still high for very large matrices                                                                      |
|                  | - Spatial modes are the right singular vectors ($\mathbf{R}$) and temporal modes are the left singular vectors ($\mathbf{L}$)                            | - Direct link to both POD methods                                                                                        | - May still require large matrix inversions depending on dataset size                                                        |
|                  | - Eigenvalues of $\mathbf{C}$ and $\mathbf{C}_s$ are given by $\sigma_i^2/(m-1)$                                                                        | - Singular values indicate energy content                                                                                |                                                                                                                              |
