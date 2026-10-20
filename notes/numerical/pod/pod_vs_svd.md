# POD and the Singular Value Decomposition

The POD of a snapshot matrix is its singular value decomposition: the left singular vectors are the spatial modes, the squared singular values are the energies, and the right singular vectors are the normalised time histories. This note derives that correspondence, shows that the direct method and the method of snapshots are the two eigenvalue problems hidden in one SVD, explains why computing the SVD of the data is more accurate than diagonalising either correlation matrix, and compares the cost of the options, including randomized SVD for very large data. The notation is that of [POD for N Points](derivation_in_n_dim.md).

## Problem Statement

Given the mean-subtracted snapshot matrix $\mathbf{U} \in \mathbb{R}^{N \times M}$, with one snapshot per column and usually $N \gg M$, compute the leading POD modes $\boldsymbol{\phi}_i$, the eigenvalues $\lambda_i$ and the coefficients $\mathbf{A} = \boldsymbol{\Phi}^T\mathbf{U}$ with an error close to machine precision relative to $\lVert \mathbf{U} \rVert$, without forming the $N \times N$ covariance matrix. The questions are how the SVD factors map onto these quantities, which algorithm to use for which $N$ and $M$, and how accurate each is. On a non-uniform mesh the same applies to the weighted matrix $\mathbf{W}^{1/2}\mathbf{U}$.

## The Thin SVD

Every real $N \times M$ matrix with $N \ge M$ can be factorised as

```math
\mathbf{U} = \mathbf{L}\boldsymbol{\Sigma}\mathbf{V}^T = \sum_{i=1}^{M}\sigma_i\,\boldsymbol{\ell}_i\mathbf{v}_i^T, \qquad \mathbf{L}^T\mathbf{L} = \mathbf{I}_M, \qquad \mathbf{V}^T\mathbf{V} = \mathbf{V}\mathbf{V}^T = \mathbf{I}_M
```

with $\mathbf{L} \in \mathbb{R}^{N \times M}$ (left singular vectors $\boldsymbol{\ell}_i$), $\mathbf{V} \in \mathbb{R}^{M \times M}$ (right singular vectors $\mathbf{v}_i$) and $`\boldsymbol{\Sigma} = \mathrm{diag}(\sigma_1, \dots, \sigma_M)`$, $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$. This is the thin (economy) SVD; the full SVD pads $\mathbf{L}$ with $N - M$ further orthonormal columns that multiply zeros. The number of nonzero singular values is the rank, at most $M - 1$ after mean subtraction. The factors are unique up to the signs of matching pairs $(\boldsymbol{\ell}_i, \mathbf{v}_i)$, and up to rotations within the span of repeated singular values.

## Relation to POD

Substituting the SVD into the two Gram matrices of the data gives their eigendecompositions directly:

```math
\mathbf{C} = \frac{1}{M-1}\mathbf{U}\mathbf{U}^T = \mathbf{L}\,\frac{\boldsymbol{\Sigma}^2}{M-1}\,\mathbf{L}^T, \qquad \mathbf{K} = \frac{1}{M-1}\mathbf{U}^T\mathbf{U} = \mathbf{V}\,\frac{\boldsymbol{\Sigma}^2}{M-1}\,\mathbf{V}^T
```

Both are symmetric with orthonormal eigenvectors, so by uniqueness of the eigendecomposition:

| POD quantity | SVD expression |
| --- | --- |
| spatial modes $\boldsymbol{\Phi}$ (eigenvectors of $\mathbf{C}$) | left singular vectors $\mathbf{L}$ |
| eigenvalues $\lambda_i$ (energy of mode $i$) | $\sigma_i^2/(M-1)$ |
| energy fraction of mode $i$ | $`\sigma_i^2/\sum_k\sigma_k^2`$ |
| temporal coefficients $\mathbf{A} = \boldsymbol{\Phi}^T\mathbf{U}$ | $\boldsymbol{\Sigma}\mathbf{V}^T$: row $i$ is $\sigma_i\mathbf{v}_i^T$ |
| eigenvectors of the snapshot correlation $\mathbf{K}$ | right singular vectors $\mathbf{V}$, the coefficients normalised to unit length |
| rank-$`r`$ reconstruction | $`\mathbf{L}_r\boldsymbol{\Sigma}_r\mathbf{V}_r^T`$ |

The coefficients follow from $`\boldsymbol{\Phi}^T\mathbf{U} = \mathbf{L}^T\mathbf{L}\boldsymbol{\Sigma}\mathbf{V}^T = \boldsymbol{\Sigma}\mathbf{V}^T`$. Their covariance is $`\boldsymbol{\Sigma}\mathbf{V}^T\mathbf{V}\boldsymbol{\Sigma}/(M-1) = \boldsymbol{\Lambda}`$, the uncorrelatedness proved in [POD for N Points](derivation_in_n_dim.md#properties-and-proofs). `compute_pod` in [scripts/_numerics.py](../../../scripts/_numerics.py) returns exactly these quantities: `modes` is $\mathbf{L}$, `singular_values` is $`\mathrm{diag}\,\boldsymbol{\Sigma}`$, `coefficients` is $\boldsymbol{\Sigma}\mathbf{V}^T$, and `eigenvalues` is $\sigma_i^2/(M-1)$. Some codes use $1/M$ instead of $1/(M-1)$ or omit the factor altogether; this rescales every eigenvalue by the same constant and leaves modes and energy fractions unchanged.

## Equivalence of the Direct and Snapshot Methods

The direct method solves $\mathbf{C}\boldsymbol{\phi} = \lambda\boldsymbol{\phi}$ ($N \times N$); the method of snapshots solves $\mathbf{K}\mathbf{v} = \lambda\mathbf{v}$ ($M \times M$). The relations above show that both compute pieces of the same SVD and share their nonzero eigenvalues. The pieces are linked by

```math
\boldsymbol{\ell}_i = \frac{1}{\sigma_i}\mathbf{U}\mathbf{v}_i, \qquad \mathbf{v}_i = \frac{1}{\sigma_i}\mathbf{U}^T\boldsymbol{\ell}_i, \qquad \sigma_i > 0
```

which follow from $\mathbf{U}\mathbf{V} = \mathbf{L}\boldsymbol{\Sigma}$ and $\mathbf{U}^T\mathbf{L} = \mathbf{V}\boldsymbol{\Sigma}$. The method of snapshots therefore obtains the spatial modes from $\mathbf{K}$ with one product $\mathbf{U}\mathbf{V}\boldsymbol{\Sigma}^{-1}$; [The Method of Snapshots](snapshot_pod.md) gives the algorithm. Eigenvectors of $\mathbf{C}$ with zero eigenvalue have no counterpart and carry no energy. Both methods give the same modes up to sign, which is why results from different codes agree after a possible sign flip of each mode and its coefficient.

## Best Low-Rank Approximation

The Eckart–Young (Eckart–Young–Mirsky) theorem states that the truncated SVD $`\mathbf{U}_r = \sum_{i \le r}\sigma_i\boldsymbol{\ell}_i\mathbf{v}_i^T`$ is the best rank-$`r`$ approximation of $\mathbf{U}$ in both the Frobenius and the spectral norm:

```math
\min_{\mathrm{rank}\,\mathbf{X} \le r}\lVert \mathbf{U} - \mathbf{X} \rVert_F^2 = \lVert \mathbf{U} - \mathbf{U}_r \rVert_F^2 = \sum_{i > r}\sigma_i^2, \qquad \min_{\mathrm{rank}\,\mathbf{X} \le r}\lVert \mathbf{U} - \mathbf{X} \rVert_2 = \sigma_{r+1}
```

The Frobenius statement, divided by $M - 1$, is the POD optimality result: no $r$-dimensional basis captures more energy than the first $r$ modes. The spectral-norm statement bounds the worst direction rather than the average. The same theorem underlies image compression with the SVD, shown in the [Image Compression Using SVD](../../../scripts/algorithms/image_compression_using_svd/) script, where the "snapshots" are the columns of an image.

## Numerical Accuracy

Forming $\mathbf{U}^T\mathbf{U}$ or $\mathbf{U}\mathbf{U}^T$ squares the condition number: the eigenvalues of $\mathbf{K}$ are $\sigma_i^2/(M-1)$, so $\kappa(\mathbf{K}) = \kappa(\mathbf{U})^2$. A backward-stable symmetric eigensolver computes each eigenvalue with an absolute error of about $\epsilon\lambda_1$, where $\epsilon = 2.2 \times 10^{-16}$ in double precision. A singular value recovered as $\sqrt{(M-1)\lambda_i}$ is then accurate only if

```math
\sigma_i \gg \sqrt{\epsilon}\,\sigma_1 \approx 1.5 \times 10^{-8}\,\sigma_1
```

whereas an SVD computed directly from $\mathbf{U}$ by Householder bidiagonalisation (the Golub–Kahan approach used by LAPACK) has absolute errors of about $\epsilon\sigma_1$, so it resolves singular values down to about $10^{-16}\sigma_1$. Modes belonging to small singular values also lose orthogonality in the snapshot method, because $\boldsymbol{\ell}_i = \mathbf{U}\mathbf{v}_i/\sigma_i$ divides by an inaccurate $\sigma_i$. For energy-dominated flow analysis, where modes below $10^{-8}$ of the leading amplitude are noise anyway, this rarely matters; it matters when POD modes are used as a basis for Galerkin projection with many modes, for data with a wide dynamic range, or in single precision, where $\sqrt{\epsilon} \approx 3 \times 10^{-4}$. For this reason `compute_pod` discards modes whose singular value (SVD route) or eigenvalue (snapshot route) falls below $\epsilon\max(N, M)$ times the largest one, instead of normalising round-off noise into spurious modes.

## Cost

For $N \gg M$ and $r$ retained modes:

| Method | Main work | Memory | Remarks |
| --- | --- | --- | --- |
| direct: eigendecomposition of $\mathbf{C}$ | $O(N^2M)$ to form, $O(N^3)$ to decompose | $N^2$ | only for small $N$, e.g. sparse sensor data |
| method of snapshots: eigendecomposition of $\mathbf{K}$ | $O(NM^2)$ to form, $O(M^3)$ to decompose, $O(NMr)$ for the modes | $NM + M^2$ | $\mathbf{K}$ can be accumulated from blocks of rows or snapshots; squares the condition number |
| thin SVD of $\mathbf{U}$ | $O(NM^2)$, a few times more than forming $\mathbf{K}$ | $NM$ | most accurate; needs $\mathbf{U}$ in memory |
| truncated iterative SVD (Lanczos, e.g. `scipy.sparse.linalg.svds`) | $O(NMr)$ per iteration | $N(r + \text{few})$ | for $r \ll M$; needs only products with $\mathbf{U}$ and $\mathbf{U}^T$ |
| randomized SVD | $O(NM(r + p))$ per pass over the data, plus $O(N(r + p)^2)$ | $N(r + p)$ | oversampling $p$ of 5 to 10; 2–4 passes over the data |

With $N = 10^6$ and $M = 500$, forming $\mathbf{K}$ and computing the thin SVD both cost about $10^{11}$ to $10^{12}$ operations, minutes on a workstation, while the direct method would need $10^{18}$ operations and 8 TB of memory (Exercise 1).

## Randomized SVD

When $\mathbf{U}$ is too large for a dense SVD but only $r \ll M$ modes are wanted, a randomized range finder (Halko, Martinsson and Tropp, 2011) captures the dominant column space with a few passes over the data:

1. Draw a Gaussian test matrix $\boldsymbol{\Omega} \in \mathbb{R}^{M \times (r + p)}$.
2. Form $\mathbf{Y} = \mathbf{U}\boldsymbol{\Omega}$; optionally apply $q$ power iterations $\mathbf{Y} \leftarrow \mathbf{U}(\mathbf{U}^T\mathbf{Y})$, re-orthonormalising between them, to sharpen a slowly decaying spectrum.
3. Orthonormalise, $\mathbf{Y} = \mathbf{Q}\mathbf{R}$.
4. Compute the small SVD $`\mathbf{Q}^T\mathbf{U} = \tilde{\mathbf{L}}\boldsymbol{\Sigma}\mathbf{V}^T`$ and set $`\mathbf{L} = \mathbf{Q}\tilde{\mathbf{L}}`$.

The expected error is close to $\sigma_{r+1}$ when the spectrum decays quickly, and the power iterations reduce it when it does not. [Flow Feature Extraction](../../machine_learning/flow/feature_extraction.md#randomized-svd) discusses it in the context of large flow data sets.

## Key Takeaways

- POD modes are the left singular vectors of the snapshot matrix, $\lambda_i = \sigma_i^2/(M-1)$, and the temporal coefficients are $\boldsymbol{\Sigma}\mathbf{V}^T$.
- The direct method and the method of snapshots diagonalise $\mathbf{U}\mathbf{U}^T$ and $\mathbf{U}^T\mathbf{U}$, the two halves of the same SVD, and give identical nonzero eigenvalues and modes up to sign.
- The truncated SVD is the best rank-$`r`$ approximation (Eckart–Young); the squared Frobenius error is $\sum_{i > r}\sigma_i^2$.
- Forming either correlation matrix squares the condition number, limiting resolvable singular values to about $10^{-8}\sigma_1$ in double precision; the SVD of $\mathbf{U}$ does not.
- For very large data use a truncated iterative or randomized SVD, which need only products with $\mathbf{U}$.

## Related Scripts

- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.
- [Image Compression Using SVD](../../../scripts/algorithms/image_compression_using_svd/): compresses a grayscale image by keeping only its $r$ largest singular values and the matching singular vectors, then compares the rank-$`r`$ reconstructions with the original.
- [POD Energy and Truncation](../../../scripts/plots/pod_energy_and_truncation/): computes the POD of a synthetic cylinder-wake velocity field on a stretched mesh and shows how the number of retained modes $r$ follows from the eigenvalue spectrum, with the 90% and 99% energy thresholds and reconstructions of one snapshot with $r = 1, 2, 5$ and $10$ modes.
- [POD Modes of a Two-Point Velocity Signal](../../../scripts/plots/pod_modes_2d/): applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal.
- [Airfoil Shape PCA](../../../scripts/algorithms/airfoil_shape_pca/): builds a linear shape space for NACA 4-digit airfoils by principal component analysis (PCA) of their surface coordinates and shows how few modes are needed to describe the family.
- [Dynamic Mode Decomposition (DMD)](../../../scripts/algorithms/dynamic_mode_decomposition/): applies exact dynamic mode decomposition to a noisy synthetic 1D wave field built from three wave packets whose frequencies and growth rates are known, and checks how well DMD recovers them.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.

## Exercises

**Exercise 1.** A data set has $N = 10^6$ points and $M = 500$ snapshots. Compare the storage of $\mathbf{C}$ and $\mathbf{K}$ in double precision and the order of the work for (a) the direct method, (b) the method of snapshots and (c) the thin SVD.

<details>
<summary>Answer</summary>

$\mathbf{C}$ needs $10^{12} \times 8$ bytes $= 8$ TB; $\mathbf{K}$ needs $500^2 \times 8$ bytes $= 2$ MB.

- (a) $O(N^3) = 10^{18}$ operations.
- (b) Forming $\mathbf{K}$ costs $O(NM^2) = 2.5 \times 10^{11}$, its eigendecomposition $O(M^3) = 1.25 \times 10^8$, and the modes $O(NMr)$.
- (c) $O(NM^2) = 2.5 \times 10^{11}$, with a larger constant than (b).

(b) and (c) are of the same order; (c) is more accurate for small singular values.

</details>

**Exercise 2.** Two points and three mean-subtracted snapshots give

```math
\mathbf{U} = \begin{pmatrix} 1 & 1 & -2 \\ 1 & -1 & 0 \end{pmatrix}
```

Compute the singular values from $\mathbf{U}\mathbf{U}^T$, the POD eigenvalues, the modes $\mathbf{L}$, the right singular vectors $\mathbf{v}_i = \mathbf{U}^T\boldsymbol{\ell}_i/\sigma_i$ and the coefficients $\boldsymbol{\Sigma}\mathbf{V}^T$.

<details>
<summary>Answer</summary>

$`\mathbf{U}\mathbf{U}^T = \begin{pmatrix} 6 & 0 \\ 0 & 2 \end{pmatrix}`$, so $\sigma_1 = \sqrt{6} = 2.449$, $\sigma_2 = \sqrt{2} = 1.414$, and $\lambda_1 = 6/2 = 3$, $\lambda_2 = 1$. The modes are $\boldsymbol{\ell}_1 = (1, 0)$ and $\boldsymbol{\ell}_2 = (0, 1)$: the two rows are already uncorrelated. Then $\mathbf{v}_1 = (1, 1, -2)/\sqrt{6}$ and $\mathbf{v}_2 = (1, -1, 0)/\sqrt{2}$, and the coefficients $\sigma_i\mathbf{v}_i^T$ are $(1, 1, -2)$ and $(1, -1, 0)$, the rows of $\mathbf{U}$ themselves, as they must be when $\mathbf{L} = \mathbf{I}$.

</details>

**Exercise 3.** For the matrix of Exercise 2, form $\mathbf{K} = \mathbf{U}^T\mathbf{U}/(M-1)$, verify that its eigenvalues are $3, 1, 0$ with eigenvectors $\mathbf{v}_1$, $\mathbf{v}_2$ and $(1, 1, 1)/\sqrt{3}$, and recover the modes as $\boldsymbol{\ell}_i = \mathbf{U}\mathbf{v}_i/\sigma_i$. Why is one eigenvalue exactly zero?

<details>
<summary>Answer</summary>

```math
\mathbf{K} = \frac{1}{2}\begin{pmatrix} 2 & 0 & -2 \\ 0 & 2 & -2 \\ -2 & -2 & 4 \end{pmatrix} = \begin{pmatrix} 1 & 0 & -1 \\ 0 & 1 & -1 \\ -1 & -1 & 2 \end{pmatrix}
```

$\mathbf{K}(1, 1, -2)^T = (3, 3, -6)^T$, $\mathbf{K}(1, -1, 0)^T = (1, -1, 0)^T$ and $\mathbf{K}(1, 1, 1)^T = \mathbf{0}$. The modes are $\mathbf{U}\mathbf{v}_1/\sigma_1 = (6, 0)/6 = (1, 0)$ and $\mathbf{U}\mathbf{v}_2/\sigma_2 = (0, 2)/2 = (0, 1)$. The zero eigenvalue comes from mean subtraction: each row of $\mathbf{U}$ sums to zero, so $\mathbf{U}(1, 1, 1)^T = \mathbf{0}$ and $`\mathrm{rank}\,\mathbf{U} \le M - 1`$.

</details>

**Exercise 4.** For the matrix of Exercise 2, write the rank-1 truncation, verify the Eckart–Young error in both norms, and give the captured energy fraction.

<details>
<summary>Answer</summary>

$`\mathbf{U}_1 = \sigma_1\boldsymbol{\ell}_1\mathbf{v}_1^T`$ has rows $(1, 1, -2)$ and $(0, 0, 0)$. The error has rows $(0, 0, 0)$ and $(1, -1, 0)$, with squared Frobenius norm $2 = \sigma_2^2$ and spectral norm $\sqrt{2} = \sigma_2$. The captured fraction is $`6/8 = 75\%`$, equal to $\lambda_1/(\lambda_1 + \lambda_2) = 3/4$.

</details>

**Exercise 5.** A matrix $\mathbf{U} \in \mathbb{R}^{1000 \times 50}$ is built with exact singular values $1$, $10^{-4}$ and $\sigma_3$ (and zero otherwise). In double precision, which values of $\sigma_3$ can be recovered as $\sqrt{\mu_3}$ from the eigenvalues $\mu_i$ of $\mathbf{U}^T\mathbf{U}$, and which from the SVD? Check $\sigma_3 = 10^{-6}$ and $10^{-9}$.

<details>
<summary>Answer</summary>

The eigenvalues of $\mathbf{U}^T\mathbf{U}$ are $1$, $10^{-8}$ and $\sigma_3^2$, computed with absolute errors near $\epsilon \approx 2 \times 10^{-16}$. For $\sigma_3 = 10^{-6}$, $\mu_3 = 10^{-12}$ has a relative error of about $10^{-4}$ or less, and $\sqrt{\mu_3}$ is accurate to several digits: a numerical test with random orthonormal factors gives $1.0000008 \times 10^{-6}$. For $\sigma_3 = 10^{-9}$, $\mu_3 = 10^{-18}$ is below the rounding level, and the same test returns $\sqrt{\mu_3} = 1.6 \times 10^{-8}$, a pure rounding artefact. The SVD of $\mathbf{U}$ returns $10^{-9}$ correctly in both cases. The threshold is $`\sigma_3 \approx \sqrt{\epsilon}\,\sigma_1 = 1.5 \times 10^{-8}`$.

</details>

## References

- C. Eckart and G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1(3), 1936, pp. 211–218.
- G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
- L. N. Trefethen and D. Bau, *Numerical Linear Algebra*, SIAM, 1997.
- N. Halko, P. G. Martinsson and J. A. Tropp, "Finding structure with randomness: Probabilistic algorithms for constructing approximate matrix decompositions", *SIAM Review* 53(2), 2011, pp. 217–288.
- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987, pp. 561–571.
- S. L. Brunton and J. N. Kutz, *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*, 2nd ed., Cambridge University Press, 2022.
- K. Taira, S. L. Brunton, S. T. M. Dawson, C. W. Rowley, T. Colonius, B. J. McKeon, O. T. Schmidt, S. Gordeyev, V. Theofilis and L. S. Ukeiley, "Modal analysis of fluid flows: An overview", *AIAA Journal* 55(12), 2017, pp. 4013–4041.
