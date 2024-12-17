## The Singular Value Decomposition (SVD) and POD

The Proper Orthogonal Decomposition (POD) is closely intertwined with the Singular Value Decomposition (SVD). In essence, POD can be viewed as extracting the principal directions of maximum variance (or energy) from a dataset, which are precisely what the SVD reveals. Both Direct POD and Snapshot POD can be reformulated in terms of SVD. This connection provides important insights and simplifies conceptual understanding, computational implementations, and algorithmic efficiency.

### Snapshot Matrix Setup

Consider a dataset represented as a matrix $\mathbf{U} \in \mathbb{R}^{m \times n}$:

- Each column of $\mathbf{U}$ (an $m$-vector) represents a single "snapshot" of the state of a system (e.g., a flow field at a given time).
- There are $n$ snapshots, and each snapshot is an $m$-dimensional vector. Typically, $m$ might be very large if it represents high-dimensional spatial data (e.g., velocity fields on a fine mesh), and $n$ is the number of snapshots in time or parameter variations.

POD aims to find an orthonormal basis (set of modes) that best represents the data in a least-squares sense. To do so, one may compute a covariance matrix from $\mathbf{U}$:

I. **Centered Data**: Usually, one first subtracts the mean from each snapshot to focus on fluctuations. For simplicity, assume $\mathbf{U}$ is already mean-subtracted.

II. **Covariance Matrices**:
- The covariance matrix in "snapshot space": $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T \mathbf{U}$ is an $n \times n$ matrix.
- The covariance matrix in "state space": $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ is an $m \times m$ matrix.

Eigen-decomposition of either $\mathbf{C}$ or $\mathbf{C}_s$ yields the POD modes and eigenvalues. However, computing eigen-decomposition directly on these large matrices can be expensive.

### Singular Value Decomposition (SVD)

SVD provides a factorization of the snapshot matrix $\mathbf{U}$ itself:

$$\mathbf{U} = \mathbf{L} \mathbf{\Sigma} \mathbf{R}^T,$$

where:

- $\mathbf{L} \in \mathbb{R}^{m \times m}$ is an orthonormal matrix whose columns $\ell_i$ are called left singular vectors.
- $\mathbf{R} \in \mathbb{R}^{n \times n}$ is an orthonormal matrix whose columns $r_i$ are called right singular vectors.
- $\mathbf{\Sigma} \in \mathbb{R}^{m \times n}$ is a rectangular diagonal matrix with nonnegative real numbers $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$ on the diagonal. These $\sigma_i$ are the singular values of $\mathbf{U}$.

The rank of $\mathbf{U}$ and the number of nonzero singular values match. The singular values squared ($\sigma_i^2$) represent the energy associated with each mode in a similar way that eigenvalues do for the POD covariance matrices.

### Connection Between SVD and POD

**Key Insight**: The eigenvalue decompositions for the POD covariance matrices $\mathbf{C}$ and $\mathbf{C}_s$ are inherently related to the SVD of $\mathbf{U}$.

I. **From SVD to Covariance**:

Consider $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T \mathbf{U}$:

$$\mathbf{C} = \frac{1}{m-1} (\mathbf{R}(\mathbf{\Sigma}^T\mathbf{\Sigma})\mathbf{R}^T).$$

Since $\mathbf{R}$ is orthonormal and $\mathbf{\Sigma}^T\mathbf{\Sigma}$ is diagonal with $\sigma_i^2$ on the diagonal, the eigen-decomposition of $\mathbf{C}$ gives eigenvalues $\frac{\sigma_i^2}{m-1}$ and eigenvectors $\mathbf{R}$.

Similarly, $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$:

$$\mathbf{C}_s = \frac{1}{m-1} (\mathbf{L}(\mathbf{\Sigma}\mathbf{\Sigma}^T)\mathbf{L}^T).$$

Its eigenvalues are also $\frac{\sigma_i^2}{m-1}$, and eigenvectors are the columns of $\mathbf{L}$.

II. **Eigenvalues and Modes**:
- The singular values $\sigma_i$ of $\mathbf{U}$ determine the energy content of the modes.
- The columns of $\mathbf{R}$ (right singular vectors) correspond to eigenvectors of $\mathbf{C}$ and represent spatial modes in Direct POD.
- The columns of $\mathbf{L}$ (left singular vectors) correspond to eigenvectors of $\mathbf{C}_s$ and represent temporal modes in Snapshot POD.

### Equivalence of Direct POD and Snapshot POD

- **Direct POD**:

Direct POD involves forming $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ (an $m \times m$ matrix), and then performing eigenvalue decomposition. This is suitable if $m$ is not too large.

- **Snapshot POD**:

Snapshot POD was introduced for the scenario where $m \gg n$. Instead of working with the huge $m \times m$ covariance matrix $\mathbf{C}_s$, one computes $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$ (an $n \times n$ matrix) and performs eigenvalue decomposition there. The resulting eigenvectors correspond to temporal modes, and one can recover spatial modes by subsequent multiplications.

- **SVD Link**:

Both Direct POD and Snapshot POD computations reduce to performing SVD on $\frac{\mathbf{U}}{\sqrt{m-1}}$. The singular vectors and singular values from the SVD provide the same information as the eigenvectors and eigenvalues from the POD covariance matrices.

Thus, whether one uses Direct POD or Snapshot POD, the underlying mathematics is the same. The choice is motivated by computational efficiency: Snapshot POD is typically more efficient when there are fewer snapshots $n$ than the dimension $m$ of each snapshot.

### Summary of Relationships

- The eigenvalues from POD equal $\frac{\sigma_i^2}{m-1}$, where $\sigma_i$ are the singular values of $\mathbf{U}$.
- Spatial modes from Direct POD correspond to the right singular vectors $\mathbf{R}$.
- Temporal modes from Snapshot POD correspond to the left singular vectors $\mathbf{L}$.

## Comparison of Methods

Below is a structured comparison of POD, Snapshot POD, and SVD-based methods for extracting modes.

| **Method**       | **Procedure**                                                                                                                                         | **Advantages**                                                                | **Disadvantages**                                                                    |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **POD (Direct)** | - Form $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ and compute eigen-decomposition.<br>- Suitable if $m$ is moderate.                  | - Direct method aligns well with theoretical definitions of POD.               | - Infeasible for very large $m$ due to storing and factorizing $m \times m$ matrix |
|                  | - Extract spatial modes as eigenvectors of $\mathbf{C}_s$.                                                   | - Provides direct access to spatial modes.                                    |                                                                                      |
| **Snapshot POD** | - Form $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$ and compute eigen-decomposition.<br>- Favored when $n < m$.                        | - Much less computationally expensive for $m \gg n$.                        | - Indirect: Must map back to spatial modes after finding temporal modes.              |
|                  | - Extract temporal modes first, then spatial modes via $\mathbf{U}\mathbf{R}$.                                | - Ideal for large-dimensional problems with relatively few snapshots.          |                                                                                      |
| **SVD**          | - Perform $\mathbf{U} = \mathbf{L}\mathbf{\Sigma}\mathbf{R}^T$.<br>- SVD provides both sets of modes directly. | - Unified approach, no separate covariance needed.                            | - Similar computational cost to snapshot method, still large SVD computations.        |
|                  | - Spatial modes: columns of $\mathbf{R}$.<br>Temporal modes: columns of $\mathbf{L}$.                        | - Gives a direct link between both POD approaches.                            | - Scaling by $\sqrt{m-1}$ needed to relate to POD eigenvalues.                     |

## Practical Considerations

- **Choosing a Method**:
- If $m$ is small-to-moderate and $n$ is large, Direct POD is manageable.
- If $m$ is very large (common in CFD or large-scale scientific computing) and $n$ is relatively small, Snapshot POD is the standard approach.
- SVD is conceptually the cleanest but may require careful implementation and scaling for very large matrices.
- **Interpreting Results**:

The singular values $\sigma_i$ inform the significance of each mode. Modes corresponding to larger $\sigma_i$ (or eigenvalues $\sigma_i^2/(m-1)$) represent directions in which the data vary most. Truncating small $\sigma_i$ yields a reduced model retaining the dominant dynamics.
