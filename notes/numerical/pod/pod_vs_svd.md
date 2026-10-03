## The Singular Value Decomposition (SVD) and POD

The Proper Orthogonal Decomposition (POD) is closely intertwined with the Singular Value Decomposition (SVD). In essence, POD can be viewed as extracting the principal directions of maximum variance (or energy) from a dataset, which are precisely what the SVD reveals. Both Direct POD and Snapshot POD can be reformulated in terms of SVD. This connection provides important insights and simplifies conceptual understanding, computational implementations, and algorithmic efficiency.

### Snapshot Matrix Setup

Consider a dataset represented as a matrix $\mathbf{U} \in \mathbb{R}^{m \times n}$:

- Each row of $\mathbf{U}$ (an $n$-vector) represents a single "snapshot" of the state of a system (e.g., a flow field at a given time).
- There are $m$ snapshots, and each snapshot is an $n$-dimensional vector. Typically, $n$ might be very large if it represents high-dimensional spatial data (e.g., velocity fields on a fine mesh), and $m$ is the number of snapshots in time or parameter variations.

POD aims to find an orthonormal basis (set of modes) that best represents the data in a least-squares sense. To do so, one may compute a covariance matrix from $\mathbf{U}$:

I. **Centered Data**: Usually, one first subtracts the mean from each snapshot to focus on fluctuations. For simplicity, assume $\mathbf{U}$ is already mean-subtracted.

II. **Covariance Matrices**:

- The covariance matrix in "state space": $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T \mathbf{U}$ is an $n \times n$ matrix.
- The covariance matrix in "snapshot space": $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ is an $m \times m$ matrix.

Eigen-decomposition of either $\mathbf{C}$ or $\mathbf{C}_s$ yields the POD modes and eigenvalues. However, computing eigen-decomposition directly on these large matrices can be expensive.

### Singular Value Decomposition (SVD)

SVD provides a factorization of the snapshot matrix $\mathbf{U}$ itself:

$$
\mathbf{U} = \mathbf{L} \mathbf{\Sigma} \mathbf{R}^T
$$

where:

- $\mathbf{L} \in \mathbb{R}^{m \times m}$ is an orthonormal matrix whose columns $\ell_i$ are called left singular vectors.
- $\mathbf{R} \in \mathbb{R}^{n \times n}$ is an orthonormal matrix whose columns $r_i$ are called right singular vectors.
- $\mathbf{\Sigma} \in \mathbb{R}^{m \times n}$ is a rectangular diagonal matrix with nonnegative real numbers $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$ on the diagonal. These $\sigma_i$ are the singular values of $\mathbf{U}$.

The rank of $\mathbf{U}$ and the number of nonzero singular values match. The singular values squared ($\sigma_i^2$) represent the energy associated with each mode in a similar way that eigenvalues do for the POD covariance matrices.

### Connection Between SVD and POD

**Key Insight**: The eigenvalue decompositions for the POD covariance matrices $\mathbf{C}$ and $\mathbf{C}_s$ are inherently related to the SVD of $\mathbf{U}$.

I. **From SVD to Covariance**:

Consider $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T \mathbf{U}$:

$$
\mathbf{C} = \frac{1}{m-1} (\mathbf{R}(\mathbf{\Sigma}^T\mathbf{\Sigma})\mathbf{R}^T)
$$

Since $\mathbf{R}$ is orthonormal and $\mathbf{\Sigma}^T\mathbf{\Sigma}$ is diagonal with $\sigma_i^2$ on the diagonal, the eigen-decomposition of $\mathbf{C}$ gives eigenvalues $\frac{\sigma_i^2}{m-1}$ and eigenvectors $\mathbf{R}$.

Similarly, $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$:

$$
\mathbf{C}_s = \frac{1}{m-1} (\mathbf{L}(\mathbf{\Sigma}\mathbf{\Sigma}^T)\mathbf{L}^T)
$$

Its eigenvalues are also $\frac{\sigma_i^2}{m-1}$, and eigenvectors are the columns of $\mathbf{L}$.

II. **Eigenvalues and Modes**:

- The singular values $\sigma_i$ of $\mathbf{U}$ determine the energy content of the modes.
- The columns of $\mathbf{R}$ (right singular vectors) correspond to eigenvectors of $\mathbf{C}$ and represent spatial modes in Direct POD.
- The columns of $\mathbf{L}$ (left singular vectors) correspond to eigenvectors of $\mathbf{C}_s$ and represent temporal modes in Snapshot POD.

### Equivalence of Direct POD and Snapshot POD

- **Direct POD**:

Direct POD involves forming $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$ (an $n \times n$ matrix), and then performing eigenvalue decomposition. This is suitable if $n$ is not too large.

- **Snapshot POD**:

Snapshot POD was introduced for the scenario where $n \gg m$. Instead of working with the huge $n \times n$ covariance matrix $\mathbf{C}$, one computes $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ (an $m \times m$ matrix) and performs eigenvalue decomposition there. The resulting eigenvectors correspond to temporal modes, and one can recover spatial modes by subsequent multiplications.

- **SVD Link**:

Both Direct POD and Snapshot POD computations reduce to performing SVD on $\frac{\mathbf{U}}{\sqrt{m-1}}$. The singular vectors and singular values from the SVD provide the same information as the eigenvectors and eigenvalues from the POD covariance matrices.

Thus, whether one uses Direct POD or Snapshot POD, the underlying mathematics is the same. The choice is motivated by computational efficiency: Snapshot POD is typically more efficient when there are fewer snapshots $m$ than the dimension $n$ of each snapshot.

### Summary of Relationships

- The eigenvalues from POD equal $\frac{\sigma_i^2}{m-1}$, where $\sigma_i$ are the singular values of $\mathbf{U}$.
- Spatial modes from Direct POD correspond to the right singular vectors $\mathbf{R}$.
- Temporal modes from Snapshot POD correspond to the left singular vectors $\mathbf{L}$.

## Comparison of Methods

Below is a structured comparison of POD, Snapshot POD, and SVD-based methods for extracting modes.

| **Method** | **Procedure** | **Advantages** | **Disadvantages** |
| --- | --- | --- | --- |
| **POD (Direct)** | - Form $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$ and compute eigen-decomposition.<br>- Suitable if $n$ is moderate. | - Direct method aligns well with theoretical definitions of POD. | - Infeasible for very large $n$ due to storing and factorizing $n \times n$ matrix |
|  | - Extract spatial modes as eigenvectors of $\mathbf{C}$. | - Provides direct access to spatial modes. |  |
| **Snapshot POD** | - Form $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ and compute eigen-decomposition.<br>- Favored when $m < n$. | - Much less computationally expensive for $n \gg m$. | - Indirect: Must map back to spatial modes after finding temporal modes. |
|  | - Extract temporal modes first, then spatial modes via $\mathbf{U}^T\mathbf{L}$. | - Ideal for large-dimensional problems with relatively few snapshots. |  |
| **SVD** | - Perform $\mathbf{U} = \mathbf{L}\mathbf{\Sigma}\mathbf{R}^T$.<br>- SVD provides both sets of modes directly. | - Unified approach, no separate covariance needed. | - Similar computational cost to snapshot method, still large SVD computations. |
|  | - Spatial modes: columns of $\mathbf{R}$.<br>Temporal modes: columns of $\mathbf{L}$. | - Gives a direct link between both POD approaches. | - Scaling by $\sqrt{m-1}$ needed to relate to POD eigenvalues. |

## Practical Considerations

- **Choosing a Method**:
- If $n$ is small-to-moderate and $m$ is large, Direct POD is manageable.
- If $n$ is very large (common in CFD or large-scale scientific computing) and $m$ is relatively small, Snapshot POD is the standard approach.
- SVD is conceptually the cleanest but may require careful implementation and scaling for very large matrices.
- **Interpreting Results**:

The singular values $\sigma_i$ inform the significance of each mode. Modes corresponding to larger $\sigma_i$ (or eigenvalues $\sigma_i^2/(m-1)$) represent directions in which the data vary most. Truncating small $\sigma_i$ yields a reduced model retaining the dominant dynamics.

## Purpose in CFD

This note clarifies the mathematical relationship between POD and SVD. It shows that the eigenvalues from POD equal $\sigma_i^2/(m-1)$, the right singular vectors of $\mathbf{U}$ are the spatial modes, and the left singular vectors are the temporal modes. Understanding this equivalence helps practitioners choose the most efficient computational path and interpret results from different software implementations.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Snapshot matrix $\mathbf{U} \in \mathbb{R}^{m \times n}$ (mean-subtracted) |
| **Outputs** | SVD factorization $\mathbf{U} = \mathbf{L}\mathbf{\Sigma}\mathbf{R}^T$, singular values $\sigma_i$, equivalence to POD eigenvalues $\lambda_i = \sigma_i^2/(m-1)$ |

## Related Scripts

- [Image Compression Using SVD](../../../scripts/algorithms/image_compression_using_svd/): compresses a grayscale image by keeping only its $r$ largest singular values and the matching singular vectors, then compares the rank-$r$ reconstructions with the original.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Modes of a Two-Point Velocity Signal](../../../scripts/plots/pod_modes_2d/): applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.

## Exercises

**Exercise 1.** A CFD data set has $n = 10^6$ spatial points and $m = 500$ snapshots. Compare the storage of $\mathbf{C}$ ($n \times n$) and $\mathbf{C}_s$ ($m \times m$) in double precision, and the order of the floating-point work for (a) a dense eigen-decomposition of $\mathbf{C}$, (b) forming and decomposing $\mathbf{C}_s$, and (c) a thin SVD of $\mathbf{U}$.

<details>
<summary>Answer</summary>

Storage: $\mathbf{C}$ needs $10^{12} \times 8$ bytes (8 TB), while $\mathbf{C}_s$ needs $500^2 \times 8$ bytes (2 MB).

Work:

- (a) $O(n^3) = 10^{18}$ operations.
- (b) Forming $\mathbf{U}\mathbf{U}^T$ costs $O(nm^2) = 2.5 \times 10^{11}$, and its eigen-decomposition $O(m^3) \approx 1.25 \times 10^8$.
- (c) A thin SVD costs $O(nm^2) = 2.5 \times 10^{11}$.

Snapshot POD and the thin SVD are of the same order. The SVD avoids squaring the condition number, so it resolves small singular values more accurately.

</details>

**Exercise 2.** Let $m = 3$ mean-subtracted snapshots (rows) of $n = 2$ variables be

$$
\mathbf{U} = \begin{pmatrix} 1 & 1 \\ 1 & -1 \\ -2 & 0 \end{pmatrix}
$$

Compute the singular values from $\mathbf{U}^T\mathbf{U}$, the POD eigenvalues $\lambda_i = \sigma_i^2/(m-1)$, the right singular vectors $\mathbf{R}$ and the left singular vectors $\ell_i = \mathbf{U} r_i/\sigma_i$.

<details>
<summary>Answer</summary>

$\mathbf{U}^T\mathbf{U} = \begin{pmatrix} 6 & 0 \\ 0 & 2 \end{pmatrix}$, so $\sigma_1 = \sqrt{6} \approx 2.449$, $\sigma_2 = \sqrt{2} \approx 1.414$, and $\lambda_1 = 3$, $\lambda_2 = 1$.

$\mathbf{R} = \mathbf{I}$, so the spatial modes are $(1, 0)$ and $(0, 1)$. The left singular vectors are $\ell_1 = (1, 1, -2)/\sqrt{6}$ and $\ell_2 = (1, -1, 0)/\sqrt{2}$. The full $\mathbf{L}$ adds $\ell_3 = (1, 1, 1)/\sqrt{3}$, which has zero singular value.

</details>

**Exercise 3.** For the matrix of Exercise 2, form $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$, verify that its eigenvalues are $3, 1, 0$ with eigenvectors $\ell_1, \ell_2, \ell_3$, and recover the spatial modes as $r_i = \mathbf{U}^T\ell_i/\sigma_i$. Why is one eigenvalue exactly zero?

<details>
<summary>Answer</summary>

```math
\mathbf{C}_s = \frac{1}{2}\begin{pmatrix} 2 & 0 & -2 \\ 0 & 2 & -2 \\ -2 & -2 & 4 \end{pmatrix} = \begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & -1 \\ -1 & -1 & 2 \end{pmatrix}
```

- $\mathbf{C}_s(1, 1, -2) = (3, 3, -6)$, eigenvalue 3.
- $\mathbf{C}_s(1, -1, 0) = (1, -1, 0)$, eigenvalue 1.
- $\mathbf{C}_s(1, 1, 1) = 0$, eigenvalue 0.

Spatial modes: $\mathbf{U}^T\ell_1/\sigma_1 = (6, 0)/(\sqrt{6}\sqrt{6}) = (1, 0)$ and $\mathbf{U}^T\ell_2/\sigma_2 = (0, 2)/(\sqrt{2}\sqrt{2}) = (0, 1)$, matching $\mathbf{R}$.

The zero eigenvalue appears because mean subtraction makes the rows sum to zero, so $(1,1,1)$ is in the null space of $\mathbf{U}^T$ and $\text{rank}(\mathbf{U}) \le m - 1$.

</details>

**Exercise 4.** By the Eckart–Young theorem, the best rank-$r$ approximation of $\mathbf{U}$ in the Frobenius norm is the truncated SVD, with squared error $\sum_{i > r}\sigma_i^2$. For the matrix of Exercise 2, write the rank-1 approximation, verify the error and give the fraction of energy captured.

<details>
<summary>Answer</summary>

$\mathbf{U}_1 = \sigma_1\ell_1 r_1^T = \sqrt{6} \cdot \frac{(1, 1, -2)^T}{\sqrt{6}}(1, 0)$, which has rows $(1, 0), (1, 0), (-2, 0)$. The error $\mathbf{U} - \mathbf{U}_1$ has rows $(0, 1), (0, -1), (0, 0)$, so the squared error is $2 = \sigma_2^2$. The rank-1 model captures $\sigma_1^2/(\sigma_1^2 + \sigma_2^2) = 6/8 = 75\%$ of the energy, the same as $\lambda_1/(\lambda_1 + \lambda_2) = 3/4$.

</details>

## References

- G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
- L. N. Trefethen and D. Bau, *Numerical Linear Algebra*, SIAM, 1997.
- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987.
- S. L. Brunton and J. N. Kutz, *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*, Cambridge University Press, 2019.
