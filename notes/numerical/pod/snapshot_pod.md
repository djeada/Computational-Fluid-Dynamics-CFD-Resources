# The Method of Snapshots

The method of snapshots, introduced by Sirovich (1987), computes POD from the $M \times M$ matrix of inner products between snapshots instead of the $N \times N$ spatial covariance matrix. Since CFD and PIV data usually have far more spatial degrees of freedom $N$ than snapshots $M$, this turns an impossible eigenvalue problem into a small one. This note gives the derivation, the algorithm including the normalisation of the recovered modes, and when the method is the right choice. The relation to the SVD and the accuracy cost of forming the correlation matrix are in [POD and the SVD](pod_vs_svd.md); the notation is that of [POD for N Points](derivation_in_n_dim.md).

## Problem Statement

Given the mean-subtracted snapshot matrix $\mathbf{U} \in \mathbb{R}^{N \times M}$ with $M \ll N$ (for example $N = 10^7$ cells and $M = 500$ instants), and optionally a diagonal weight matrix $\mathbf{W}$, compute the POD eigenvalues $\lambda_i$, the unit-norm spatial modes $\boldsymbol{\phi}_i$ and the coefficients $a_i(t_j)$ using $O(M^2)$ memory beyond the data and $O(NM^2)$ operations. The method is correct when its modes and eigenvalues equal those of the direct method for every $\lambda_i > 0$.

## Derivation

Every POD mode with $\lambda > 0$ lies in the span of the snapshots: from $\mathbf{C}\boldsymbol{\phi} = \lambda\boldsymbol{\phi}$,

```math
\boldsymbol{\phi} = \frac{1}{\lambda}\mathbf{C}\boldsymbol{\phi} = \frac{1}{(M-1)\lambda}\mathbf{U}(\mathbf{U}^T\boldsymbol{\phi}) = \mathbf{U}\mathbf{c}
```

for some coefficient vector $\mathbf{c} \in \mathbb{R}^M$. Substituting $\boldsymbol{\phi} = \mathbf{U}\mathbf{c}$ into the eigenvalue problem, $`\mathbf{U}\mathbf{U}^T\mathbf{U}\mathbf{c} = (M-1)\lambda\,\mathbf{U}\mathbf{c}`$, which holds if $\mathbf{c}$ solves the $M \times M$ problem

```math
\mathbf{K}\mathbf{v} = \lambda\mathbf{v}, \qquad \mathbf{K} = \frac{1}{M-1}\mathbf{U}^T\mathbf{U}, \qquad K_{jl} = \frac{(\mathbf{u}'_j, \mathbf{u}'_l)}{M-1}
```

with $\mathbf{c}$ proportional to $\mathbf{v}$. The entry $K_{jl}$ is the inner product of snapshots $j$ and $l$: the roles of space and time are exchanged, which is the symmetry Sirovich exploited. Conversely, if $\mathbf{K}\mathbf{v} = \lambda\mathbf{v}$ with $\lambda > 0$, then

```math
\mathbf{C}(\mathbf{U}\mathbf{v}) = \frac{1}{M-1}\mathbf{U}(\mathbf{U}^T\mathbf{U}\mathbf{v}) = \mathbf{U}\mathbf{K}\mathbf{v} = \lambda\,(\mathbf{U}\mathbf{v})
```

so $\mathbf{U}\mathbf{v}$ is an eigenvector of $\mathbf{C}$ with the same eigenvalue. The two problems share their nonzero spectrum, and at most $M - 1$ eigenvalues are nonzero after mean subtraction.

The vector $\mathbf{U}\mathbf{v}$ is not normalised. With $\lVert \mathbf{v} \rVert = 1$,

```math
\lVert \mathbf{U}\mathbf{v} \rVert^2 = \mathbf{v}^T\mathbf{U}^T\mathbf{U}\mathbf{v} = (M-1)\lambda \quad \Longrightarrow \quad \boldsymbol{\phi}_i = \frac{\mathbf{U}\mathbf{v}_i}{\sqrt{(M-1)\lambda_i}}
```

The modes obtained this way are orthonormal, $`\boldsymbol{\phi}_i^T\boldsymbol{\phi}_k = \mathbf{v}_i^T\mathbf{U}^T\mathbf{U}\mathbf{v}_k/((M-1)\sqrt{\lambda_i\lambda_k}) = \delta_{ik}`$. The coefficients follow without another pass over the data:

```math
\mathbf{a}_i^T = \boldsymbol{\phi}_i^T\mathbf{U} = \frac{\mathbf{v}_i^T\mathbf{U}^T\mathbf{U}}{\sqrt{(M-1)\lambda_i}} = \sqrt{(M-1)\lambda_i}\;\mathbf{v}_i^T
```

So the eigenvectors $\mathbf{v}_i$ of $\mathbf{K}$ are the time coefficients scaled to unit length, and $\sqrt{(M-1)\lambda_i} = \sigma_i$ is the singular value of $\mathbf{U}$. In the SVD $\mathbf{U} = \mathbf{L}\boldsymbol{\Sigma}\mathbf{V}^T$, the method of snapshots computes $\mathbf{V}$ and $\boldsymbol{\Sigma}$ first and then $\mathbf{L} = \mathbf{U}\mathbf{V}\boldsymbol{\Sigma}^{-1}$.

## Algorithm

1. Assemble $\mathbf{U}$ from the snapshots and subtract the temporal mean from every row.
2. Form $\mathbf{K} = \mathbf{U}^T\mathbf{W}\mathbf{U}/(M-1)$, with $\mathbf{W} = \mathbf{I}$ on a uniform grid or the cell volumes on a mesh ([weighted inner products](derivation_in_n_dim.md#non-uniform-meshes-and-weighted-inner-products)).
3. Solve the symmetric eigenproblem $\mathbf{K}\mathbf{V} = \mathbf{V}\boldsymbol{\Lambda}$ and sort the eigenvalues in descending order.
4. Discard eigenpairs with $\lambda_i$ below a round-off tolerance, about $\epsilon\max(N, M)\lambda_1$. Mean subtraction always produces at least one such null pair.
5. Recover the modes $\boldsymbol{\phi}_i = \mathbf{U}\mathbf{v}_i/\sqrt{(M-1)\lambda_i}$ for the $r$ modes needed. They satisfy $\boldsymbol{\Phi}^T\mathbf{W}\boldsymbol{\Phi} = \mathbf{I}$.
6. Set the coefficients $`a_i(t_j) = \sqrt{(M-1)\lambda_i}\,v_{ji}`$.

This is `compute_pod(snapshots, method="snapshot")` in [scripts/_numerics.py](../../../scripts/_numerics.py) for $\mathbf{W} = \mathbf{I}$. Step 2 costs $O(NM^2)$, step 3 $O(M^3)$, step 5 $O(NMr)$. The sign of each $\mathbf{v}_i$ is arbitrary, so the modes and coefficients may differ in sign from those of another code; the products $\boldsymbol{\phi}_i\mathbf{a}_i^T$ do not.

## When to Use It

The method of snapshots is the natural choice when:

- $M \ll N$, the usual situation for 3D simulations and planar or volumetric PIV;
- the data do not fit in memory at once. $\mathbf{K}$ is a sum of contributions from blocks of points, $`\mathbf{K} = \sum_{\text{blocks } b}\mathbf{U}_b^T\mathbf{W}_b\mathbf{U}_b/(M-1)`$, so it can be accumulated while reading snapshots or row blocks from disk, or in parallel, with each process holding its own subdomain and a single reduction of an $M \times M$ matrix;
- snapshots arrive one by one: a new snapshot adds one row and column of inner products.

The snapshots need not be time-resolved or equally spaced; only the set matters. Unequal sampling (for example, snapshots clustered in one phase of a cycle) is handled by weighting the snapshots, which replaces $1/(M-1)$ by quadrature weights in time.

The direct method is preferable when $N < M$, for example a few hot-wire or pressure probes sampled for millions of time steps. The thin SVD of $\mathbf{U}$ costs the same order as forming $\mathbf{K}$ and is more accurate, because forming $\mathbf{K}$ squares the condition number and limits resolvable singular values to about $10^{-8}\sigma_1$ in double precision ([POD and the SVD](pod_vs_svd.md#numerical-accuracy)). When the whole matrix fits in memory, the SVD is therefore the default and the method of snapshots the tool for out-of-core and distributed data.

## Related Scripts

- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.

## Exercises

**Exercise 1.** By what factor is $\mathbf{K}$ smaller than $\mathbf{C}$ in storage for a PIV data set with $N = 5805$ points and $M = 3580$ snapshots, and for a simulation with $N = 10^6$ cells and $M = 1000$ snapshots?

<details>
<summary>Answer</summary>

The ratio is $(N/M)^2$. For the PIV data, $(5805/3580)^2 = 2.63$, a modest saving; here the direct method is also feasible. For the simulation, $(10^6/10^3)^2 = 10^6$: $\mathbf{C}$ would need 8 TB, $\mathbf{K}$ needs 8 MB.

</details>

**Exercise 2.** Three points and two snapshots, used without mean subtraction and with $M - 1 = 1$, give

```math
\mathbf{U} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \\ 0 & 1 \end{pmatrix}
```

Compute $\mathbf{K}$, its eigenpairs, the unnormalised modes $\mathbf{U}\mathbf{v}_i$ and their norms, and the normalised modes. Compare with the eigendecomposition of $\mathbf{C} = \mathbf{U}\mathbf{U}^T$.

<details>
<summary>Answer</summary>

$`\mathbf{K} = \mathbf{U}^T\mathbf{U} = \begin{pmatrix} 5 & 4 \\ 4 & 6 \end{pmatrix}`$, with eigenvalues $(11 \pm \sqrt{65})/2$, i.e. $\lambda_1 = 9.5311$ and $\lambda_2 = 1.4689$, and eigenvectors $\mathbf{v}_1 = (0.6618, 0.7497)$ and $\mathbf{v}_2 = (-0.7497, 0.6618)$.

$\mathbf{U}\mathbf{v}_1 = (2.0733, 2.1612, 0.7497)$ has norm $3.0873 = \sqrt{\lambda_1}$, and $\mathbf{U}\mathbf{v}_2 = (-0.8376, 0.5739, 0.6618)$ has norm $1.2120 = \sqrt{\lambda_2}$. Dividing gives $\boldsymbol{\phi}_1 = (0.6716, 0.7000, 0.2428)$ and $\boldsymbol{\phi}_2 = (-0.6911, 0.4735, 0.5461)$.

$`\mathbf{C} = \begin{pmatrix} 5 & 4 & 1 \\ 4 & 5 & 2 \\ 1 & 2 & 1 \end{pmatrix}`$ has eigenvalues $9.5311$, $1.4689$ and $0$, and its first two eigenvectors equal $\boldsymbol{\phi}_1$ and $\boldsymbol{\phi}_2$ up to sign. The third has zero energy and no counterpart in $\mathbf{K}$.

</details>

**Exercise 3.** Show that if $\mathbf{K}\mathbf{v} = \lambda\mathbf{v}$ with $\lambda > 0$ and $\lVert \mathbf{v} \rVert = 1$, then $\mathbf{U}\mathbf{v} \ne \mathbf{0}$, and that two such modes with different eigenvalues are orthogonal.

<details>
<summary>Answer</summary>

$`\lVert \mathbf{U}\mathbf{v} \rVert^2 = \mathbf{v}^T\mathbf{U}^T\mathbf{U}\mathbf{v} = (M-1)\mathbf{v}^T\mathbf{K}\mathbf{v} = (M-1)\lambda > 0`$. For two eigenpairs,

```math
(\mathbf{U}\mathbf{v}_i)^T(\mathbf{U}\mathbf{v}_k) = (M-1)\mathbf{v}_i^T\mathbf{K}\mathbf{v}_k = (M-1)\lambda_k\,\mathbf{v}_i^T\mathbf{v}_k = 0
```

because eigenvectors of the symmetric $\mathbf{K}$ for different eigenvalues are orthogonal. The recovered modes inherit orthogonality from $\mathbf{V}$, and the normalisation only rescales them.

</details>

**Exercise 4.** For Exercise 2, compute the coefficients $\mathbf{a}_1^T = \boldsymbol{\phi}_1^T\mathbf{U}$ directly and from $`\sqrt{(M-1)\lambda_1}\,\mathbf{v}_1^T`$, and check that $\mathbf{U} = \boldsymbol{\phi}_1\mathbf{a}_1^T + \boldsymbol{\phi}_2\mathbf{a}_2^T$ at one entry.

<details>
<summary>Answer</summary>

$\boldsymbol{\phi}_1^T\mathbf{U} = (2.0432, 2.3144)$ and $3.0873 \times (0.6618, 0.7497) = (2.0432, 2.3145)$, equal up to rounding. Similarly $`\mathbf{a}_2^T = 1.2120 \times (-0.7497, 0.6618) = (-0.9086, 0.8021)`$. At entry $`(1, 1)`$: $`0.6716 \times 2.0432 + (-0.6911)(-0.9086) = 1.3722 + 0.6279 = 2.000`$, the value of $`U_{11}`$.

</details>

## References

- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987, pp. 561–571.
- P. Holmes, J. L. Lumley, G. Berkooz and C. W. Rowley, *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
- J. Weiss, "A tutorial on the proper orthogonal decomposition", AIAA Paper 2019-3333, *AIAA Aviation 2019 Forum*, Dallas, 2019.
- K. Taira, S. L. Brunton, S. T. M. Dawson, C. W. Rowley, T. Colonius, B. J. McKeon, O. T. Schmidt, S. Gordeyev, V. Theofilis and L. S. Ukeiley, "Modal analysis of fluid flows: An overview", *AIAA Journal* 55(12), 2017, pp. 4013–4041.
