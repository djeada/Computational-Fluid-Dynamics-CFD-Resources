## The Snapshot POD

### POD Equation Symmetry
- **Symmetry in Variables**:
  - The original Proper Orthogonal Decomposition (POD) equation exhibits symmetry between the temporal variable $t$ and the spatial variable $\mathbf{x}$:
    
$$
    \mathbf{u}'(\mathbf{x}, t) = \sum_{k=1}^{\infty} a_k(t) \mathbf{\Phi}_k(\mathbf{x}). \quad (1)
    $$

  - This symmetry implies that $t$ and $\mathbf{x}$ can be interchanged in the analysis.
  - The concept of Snapshot POD, introduced by Sirovich, leverages this symmetry.

### Snapshot POD Methods
- **First Method**:
  - Transpose the snapshot matrix $\mathbf{U}$ and apply the direct POD algorithm.
  
- **Second Method**:
  - Use the same $m \times n$ snapshot matrix $\mathbf{U}$.
  - Construct the correlation matrix:
    
$$
    \mathbf{C}_s = \frac{1}{m-1} \mathbf{U} \mathbf{U}^T
    $$

  - Note that $\mathbf{C}_s$ is now an $m \times m$ matrix, unlike the $n \times n$ matrix in direct POD.

### Correlation Matrix $\mathbf{C}_s$
- **Averaging**:
  - $\mathbf{C}_s$ is built by averaging in the spatial domain rather than the temporal domain.
- **Eigen Decomposition**:
  - Compute the eigenvalues and eigenvectors:
    
$$
    [A_s, LAM_s] = \text{eig}(C_s)
    $$

  - Order the eigenvalues from largest to smallest.
  - This decomposition in $m$-dimensional space yields $m$ eigenvalues and eigenvectors, representing the temporal modes.

### Obtaining Spatial Coefficients
- **Projection**:
  - Project the velocity data onto the temporal modes:
    
$$
    \mathbf{\Phi}_s = \mathbf{U}^T \mathbf{A}_s
    $$

  - The matrix $\mathbf{\Phi}_s$ contains the spatial coefficients, ordered from strongest to weakest.

### Equivalence of Methods
- **Eigenvalues**:
  - The eigenvalues obtained from both the snapshot and direct methods are identical.
- **Coefficients and Modes**:
  - While the spatial coefficients and temporal modes differ by a multiplicative factor between the two methods:
    - **Direct Method**: Spatial modes are orthonormal, and time coefficients are orthogonal.
    - **Snapshot Method**: Temporal modes are orthonormal, but spatial coefficients are not.

### Normalization and Scaling
- **Normalization**:
  - Normalize each spatial coefficient in the snapshot POD to ensure consistency.
- **Scaling**:
  - Scale the temporal modes to align the results of the snapshot POD with the direct POD.

- **Reconstruction from Snapshot POD**:
  - The original snapshot matrix $\mathbf{U}$ can be reconstructed using spatial coefficients and temporal modes without normalization:
    
$$
    \mathbf{\Phi}_s = \mathbf{U}^T \mathbf{A}_s \implies \mathbf{U}^T = \mathbf{\Phi}_s \mathbf{A}_s^{-1} = \mathbf{\Phi}_s \mathbf{A}_s^T \implies \mathbf{U} = \mathbf{A}_s \mathbf{\Phi}_s^T.
    $$

    Here’s what each term means:
    - $\mathbf{U}$: Original snapshot matrix containing the data.
    - $\mathbf{A}_s$: Spatial coefficients matrix.
    - $\mathbf{\Phi}_s$: Temporal modes matrix.

    The equation shows that we can reconstruct the original data matrix $\mathbf{U}$ by multiplying the spatial coefficients $\mathbf{A}_s$ by the transpose of the temporal modes $\mathbf{\Phi}_s^T$. This reconstruction is done without needing to normalize the data.

  - Summarized as:
    
$$
    \mathbf{U} = \sum_{k=1}^{m} \tilde{\mathbf{U}}^k_s,
    $$

    where each $\tilde{\mathbf{U}}^k_s$ is given by:
    
$$
    \tilde{\mathbf{U}}^k_s = 
    \begin{pmatrix}
    (a_s)_{1k} \\
    (a_s)_{2k} \\
    \vdots \\
    (a_s)_{mk}
    \end{pmatrix}
    \begin{pmatrix}
    (\phi_s)_{1k} & \cdots & (\phi_s)_{nk}
    \end{pmatrix}.
    $$

    This represents the matrix $\mathbf{U}$ as a sum of smaller matrices, each formed by the outer product of the $k$-th column of $\mathbf{A}_s$ and the $k$-th row of $\mathbf{\Phi}_s$. Essentially, each term $\tilde{\mathbf{U}}^k_s$ represents a mode contributing to the overall reconstruction.

- **Advantages of Snapshot POD**:
  - **Efficiency**: Snapshot POD is computationally faster compared to the direct method because it deals with a smaller matrix size. This leads to reduced computational load and faster processing times.
  - **Practicality**:
    - **In cases involving planar or volumetric velocity data**: Typically, the number of spatial points $n$ is much larger than the number of snapshots $m$.
    - **Correlation matrix $\mathbf{C}_s$ is smaller**: Since $\mathbf{C}_s$ is $m \times m$ instead of $n \times n$, it is much smaller and easier to store and manipulate.
    - **Eigenvalue problem is faster to solve**: Solving the eigenvalue problem for $\mathbf{C}_s$ (which is $m \times m$) is computationally cheaper than solving it for $\mathbf{C}$ (which is $n \times n$).
  - **Example**:
    - In a **turbulent separation bubble** scenario, if the full correlation matrix $\mathbf{C}$ has 33.7 million elements, the snapshot correlation matrix $\mathbf{C}_s$ only has 12.8 million elements.
    - For both longitudinal and vertical velocity components, the full correlation matrix $\mathbf{C}$ would have 135 million elements, while the snapshot correlation matrix $\mathbf{C}_s$ still has only 12.8 million elements. This significant reduction in size highlights the efficiency of the snapshot POD method.

- **Use Cases**:
  - **Snapshot POD**: This method is ideal for datasets obtained from Particle Image Velocimetry (PIV) or Computational Fluid Dynamics (CFD), where the number of spatial points $n$ is much greater than the number of snapshots $m$.
  - **Direct Method**: This method is preferred for scenarios where measurements are taken using a limited number of single-point probes that provide high temporal resolution data.

- **Results Comparison**:
  - When $m < n$, the last $n - m$ eigenvalues from the direct method are zero, and the corresponding modes are irrelevant because they do not contain any useful information.
  - Both the Snapshot POD and the Direct Method return $\min(m, n)$ modes, ensuring that all significant modes are captured regardless of the method used.
  - Modes calculated by both methods might have opposite signs, but this is not an issue because the corresponding time coefficients will also have opposite signs, effectively cancelling out any sign differences in practical applications.


