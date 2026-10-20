# Flow Feature Extraction

A single unsteady CFD run or time-resolved PIV campaign produces thousands of snapshots, each with $10^5$ to $10^9$ values. Feature extraction compresses such data into a few coordinates, coherent structures or discrete flow states that can be inspected, used as inputs for a reduced-order model, or used to decide where to put sensors. This note covers linear and nonlinear dimensionality reduction, randomized and sparse methods that make the computations affordable, and clustering and classification of flow regimes.

Most methods here are unsupervised: they need snapshots but no labels. That suits fluid mechanics, where large curated, labeled datasets are rare compared with fields such as computer vision.

## Problem Statement

Collect $m$ snapshots $\mathbf{x}_1, \dots, \mathbf{x}_m \in \mathbb{R}^n$ (for example all velocity components at all cells at $m$ instants or $m$ parameter values) as the columns of the snapshot matrix

$$
\mathbf{X} = [\mathbf{x}_1 \ \cdots \ \mathbf{x}_m] \in \mathbb{R}^{n \times m},
\qquad n \gg m
$$

Usually the temporal mean $\bar{\mathbf{x}}$ is subtracted first. Feature extraction then seeks one of:

1. Low-dimensional coordinates, given by an encoder $E: \mathbb{R}^n \to \mathbb{R}^r$ and a decoder $D: \mathbb{R}^r \to \mathbb{R}^n$ with $r \ll n$.
2. Coherent structures, meaning spatial fields (modes) that represent the data with few coefficients.
3. Discrete states, found by partitioning the snapshots into $K$ clusters of similar flow, or, given labels $y_i$, by learning a classifier $\mathbf{x} \mapsto y$.
4. A small set of $p \ll n$ sensor locations from which the full field can be estimated.

For the first two tasks the encoder and decoder minimize the reconstruction loss

$$
\mathcal{L} = \frac{1}{m}\sum_{i=1}^{m} \lVert \mathbf{x}_i - D(E(\mathbf{x}_i))
\rVert_{\mathbf{M}}^2
$$

where $\lVert \mathbf{v} \rVert_{\mathbf{M}}^2 = \mathbf{v}^T\mathbf{M}\mathbf{v}$ and $\mathbf{M}$ is a diagonal matrix of cell volumes, so that $\mathcal{L}$ measures kinetic energy rather than a sum over grid points. Clustering minimizes a within-cluster spread instead, and classification a cross-entropy, both defined below.

The difficulties are size and structure. With $n = 10^7$ the $n \times n$ spatial covariance cannot be formed. Variables with different units (velocity, pressure, temperature) must be scaled before they share one norm. Advection makes linear subspaces inefficient: a structure that translates across the domain needs many modes, even though only one parameter (its position) changes. Snapshots taken close in time are strongly correlated, so the effective number of samples is much smaller than $m$.

## Linear Embeddings: POD and PCA

### SVD of the Snapshot Matrix

Proper orthogonal decomposition (POD) is the thin singular value decomposition of the mean-subtracted, weighted snapshot matrix $\mathbf{X}$:

$$
\mathbf{X} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T,
\qquad \sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_m \geq 0
$$

The columns $\mathbf{u}_j$ of $\mathbf{U} \in \mathbb{R}^{n \times m}$ are the POD modes, and row $j$ of $\boldsymbol{\Sigma}\mathbf{V}^T$ holds the temporal coefficients $a_j(t_i)$. When the weighting $\mathbf{M}$ is not the identity, the SVD is taken of $\mathbf{M}^{1/2}\mathbf{X}$ and the modes are mapped back with $\mathbf{M}^{-1/2}$. The encoder and decoder of the problem statement are then linear: $E(\mathbf{x}) = \mathbf{U}_r^T\mathbf{x}$ and $D(\mathbf{a}) = \mathbf{U}_r\mathbf{a}$.

By the Eckart–Young theorem, truncating to $r$ modes gives the best rank-$`r`$ approximation in the Frobenius norm, with error and captured energy fraction

$$
\lVert \mathbf{X} - \mathbf{U}_r\boldsymbol{\Sigma}_r\mathbf{V}_r^T
\rVert_F^2 = \sum_{j > r} \sigma_j^2,
\qquad \frac{E_r}{E} = \frac{\sum_{j=1}^{r} \sigma_j^2}{\sum_{j=1}^{m} \sigma_j^2}
$$

Principal component analysis (PCA) is the same computation applied to mean-subtracted data: the PCA directions are the eigenvectors of the sample covariance $\mathbf{X}\mathbf{X}^T/(m - 1)$, which are the left singular vectors of $\mathbf{X}$, with variances $\sigma_j^2/(m - 1)$.

The derivations, the method of snapshots (which solves the $m \times m$ eigenproblem of $\mathbf{X}^T\mathbf{X}$ instead of the $n \times n$ one) and worked examples are in the POD notes: [POD in CFD](../../numerical/pod/pod_intro.md), [POD and SVD](../../numerical/pod/pod_vs_svd.md), [snapshot POD](../../numerical/pod/snapshot_pod.md) and the [N-dimensional derivation](../../numerical/pod/derivation_in_n_dim.md).

### Choosing the Rank

Three rules are common:

- An energy threshold takes the smallest $r$ with $E_r/E \geq 0.9$ to $0.99$. It is simple but says nothing about noise.
- A gap in the singular value spectrum separates structure from noise: clean low-rank data plotted as $\log\sigma_j$ against $j$ show a drop followed by a noise floor (panel (b) of the [DMD figure](../../../scripts/algorithms/dynamic_mode_decomposition/dynamic_mode_decomposition.png) is an example).
- The optimal hard threshold of Gavish and Donoho (2014) keeps, for a square matrix with white noise of known standard deviation $\eta$, the singular values above $`(4/\sqrt{3})\sqrt{n}\,\eta \approx 2.31\sqrt{n}\,\eta`$. For unknown noise and an $n \times m$ matrix the threshold is $`\omega(\beta)\,\sigma_{\mathrm{med}}`$, where $\sigma_{\mathrm{med}}$ is the median singular value and $\omega(\beta) \approx 0.56\beta^3 - 0.95\beta^2 + 1.82\beta + 1.43$ with aspect ratio $\beta = m/n \leq 1$.

### Where Linear Subspaces Fail

POD is optimal among linear subspaces, but the best linear subspace can still be poor. A Gaussian pulse that translates across the domain produces snapshots that are nearly orthogonal once the pulse has moved more than its width, so the singular values decay slowly, while the data lie on a one-dimensional curve parameterized by the pulse position. Flows dominated by convection (shocks, fronts, vortices travelling through the domain) behave the same way. This is the motivation for nonlinear embeddings.

## Nonlinear Embeddings

### Kernel PCA

Kernel PCA performs PCA in a feature space $\boldsymbol{\varphi}(\mathbf{x})$ defined only through a kernel $k(\mathbf{x}, \mathbf{x}') = \boldsymbol{\varphi}(\mathbf{x})^T\boldsymbol{\varphi}(\mathbf{x}')$, for example the Gaussian kernel $\exp(-\lVert \mathbf{x} - \mathbf{x}' \rVert^2/\epsilon)$. The steps are:

1. Form the Gram matrix $K_{ij} = k(\mathbf{x}_i, \mathbf{x}_j)$, of size $m \times m$.
2. Center it in feature space: $\tilde{\mathbf{K}} = \mathbf{H}\mathbf{K}\mathbf{H}$ with $\mathbf{H} = \mathbf{I} - \mathbf{1}\mathbf{1}^T/m$.
3. Solve $\tilde{\mathbf{K}}\mathbf{v}_j = \mu_j\mathbf{v}_j$; the $j$-th coordinate of snapshot $i$ is $`\sqrt{\mu_j}\,(\mathbf{v}_j)_i`$.

The cost is that of the method of snapshots, but there is no linear decoder: mapping a point in the embedding back to a flow field requires solving a separate pre-image problem. With the linear kernel $k = \mathbf{x}^T\mathbf{x}'$ kernel PCA reduces to the method of snapshots.

### Autoencoders

An autoencoder is a neural network trained to reproduce its input through a bottleneck of width $r$:

$$
\mathbf{z} = E_{\boldsymbol\theta}(\mathbf{x}) \in \mathbb{R}^r,
\qquad \hat{\mathbf{x}} = D_{\boldsymbol\theta}(\mathbf{z}),
\qquad \mathcal{L}(\boldsymbol\theta) = \frac{1}{m}\sum_{i=1}^m \lVert \mathbf{x}_i -
D_{\boldsymbol\theta}(E_{\boldsymbol\theta}(\mathbf{x}_i)) \rVert^2
$$

A one-hidden-layer encoder is $E(\mathbf{x}) = \sigma(\mathbf{W}_e\mathbf{x} + \mathbf{b}_e)$ and the decoder $D(\mathbf{z}) = \mathbf{W}_d\mathbf{z} + \mathbf{b}_d$, with an activation function $\sigma$; deep versions stack several layers, and convolutional layers are used for fields on structured grids. Training uses the backpropagation and optimizers described in [Neural Networks](../fundamentals/neural_networks.md).

When the activation is the identity, $`\hat{\mathbf{x}} = \mathbf{W}_d\mathbf{W}_e\mathbf{x}`$ is a rank-$`r`$ linear map, and the Eckart–Young theorem says its error cannot fall below $`\sum_{j > r}\sigma_j^2`$. Baldi and Hornik (1989) showed that every minimum of this loss is a global one, and at the minimum $`\mathbf{W}_d`$ spans the subspace of the first $`r`$ POD modes, although its columns need not be orthogonal or equal to the modes. A linear autoencoder is therefore POD found by gradient descent. Milano and Koumoutsakos (2002) demonstrated this for near-wall turbulence and then showed that a nonlinear autoencoder with the same latent size reconstructs the flow better.

The practical test follows directly. Train an autoencoder with latent size $r$ and compare its validation error with the POD error at rank $r$. If the autoencoder is clearly better, the data lie near a curved manifold; if not, POD is the cheaper, interpretable and orthogonal choice. Autoencoders need more data, careful validation ([Training and Validation](../fundamentals/training_and_validation.md)), and their latent coordinates have no unique ordering or physical meaning.

### Manifold Learning

Manifold learning builds coordinates from a graph of nearest neighbors instead of a global projection.

- Isomap (Tenenbaum, de Silva and Langford, *Science*, 2000) connects each snapshot to its $k$ nearest neighbors, approximates distances along the manifold by shortest paths through this graph, and embeds the snapshots with classical multidimensional scaling of those distances.
- Diffusion maps (Coifman and Lafon, *Applied and Computational Harmonic Analysis*, 2006) form the kernel $`W_{ij} = \exp(-\lVert \mathbf{x}_i - \mathbf{x}_j \rVert^2/\epsilon)`$, normalize its rows to the Markov matrix $`\mathbf{P} = \mathbf{D}^{-1}\mathbf{W}`$ with $`D_{ii} = \sum_j W_{ij}`$, and use the leading non-trivial eigenvectors $\boldsymbol{\psi}_k$ of $\mathbf{P}$, scaled by $\lambda_k^t$, as coordinates. Distances in this embedding approximate diffusion distances after $t$ steps of a random walk on the data.

For the translating pulse, both recover the pulse position as a single coordinate. Neither gives a decoder or a map for new snapshots without extra steps (Nyström extension or a regression from coordinates to fields), and both are sensitive to the neighborhood size $k$ or the kernel width $\epsilon$.

## Sparse and Randomized Methods

### Randomized SVD

For very large $\mathbf{X}$, the randomized range finder of Halko, Martinsson and Tropp (2011) computes an approximate rank-$`r`$ SVD with a few passes over the data:

1. Draw a Gaussian test matrix $\boldsymbol{\Omega} \in \mathbb{R}^{m \times (r + p)}$, with oversampling $p \approx 5$ to $10$.
2. Sample the range: $\mathbf{Y} = \mathbf{X}\boldsymbol{\Omega}$. For slowly decaying spectra, apply $q$ power iterations, $\mathbf{Y} = (\mathbf{X}\mathbf{X}^T)^q\mathbf{X}\boldsymbol{\Omega}$, with re-orthonormalization between them.
3. Orthonormalize: $\mathbf{Y} = \mathbf{Q}\mathbf{R}$, $\mathbf{Q} \in \mathbb{R}^{n \times (r + p)}$.
4. Project: $\mathbf{B} = \mathbf{Q}^T\mathbf{X}$, a small $(r + p) \times m$ matrix.
5. Take the SVD $\mathbf{B} = \hat{\mathbf{U}}\boldsymbol{\Sigma}\mathbf{V}^T$ and set $\mathbf{U} = \mathbf{Q}\hat{\mathbf{U}}$.

The cost is $O(nm(r + p))$ instead of $O(nm^2)$ for a full thin SVD. The expected error is close to the optimal $\sigma_{r+1}$ and improves rapidly with $p$ and $q$. Because $\mathbf{X}$ is only touched through products, the snapshots can stay on disk or be distributed across processors.

### Compressed Sensing

Compressed sensing reconstructs a signal from far fewer measurements than its dimension when the signal is sparse in a known basis $\boldsymbol{\Psi}$: $\mathbf{x} = \boldsymbol{\Psi}\mathbf{s}$ with only $K$ non-zero entries in $\mathbf{s}$. Given $p$ measurements $\mathbf{y} = \mathbf{C}\mathbf{x}$, where each row of $\mathbf{C}$ selects or combines grid values, the sparse coefficients are found from the convex problem

$$
\min_{\mathbf{s}} \lVert \mathbf{s} \rVert_1 \quad \text{subject to} \quad
\mathbf{y} = \mathbf{C}\boldsymbol{\Psi}\mathbf{s}
$$

Exact recovery requires $\mathbf{C}$ to be incoherent with $\boldsymbol{\Psi}$ (random point samples in a Fourier basis are the standard example) and about $p = O(K\log(n/K))$ measurements. In flows the generic Fourier or wavelet bases are often far from sparse, so data-driven bases are used instead.

### Sparse Sensor Placement

If the flow is well represented by $r$ POD modes, $\mathbf{x} \approx \boldsymbol{\Psi}_r\mathbf{a}$ with $\boldsymbol{\Psi}_r = \mathbf{U}_r$, then $p \geq r$ point sensors suffice, provided they are well placed. With $\mathbf{C} \in \mathbb{R}^{p \times n}$ selecting the sensor locations, the coefficients and the field estimate are

$$
\hat{\mathbf{a}} = (\mathbf{C}\boldsymbol{\Psi}_r)^{+}\mathbf{y},
\qquad \hat{\mathbf{x}} = \boldsymbol{\Psi}_r\hat{\mathbf{a}}
$$

Noise in $\mathbf{y}$ is amplified by the conditioning of $\mathbf{C}\boldsymbol{\Psi}_r$, so the sensors should make this matrix as well conditioned as possible, for example by maximising $\lvert\det(\mathbf{C}\boldsymbol{\Psi}_r)\rvert$ for $p = r$. The combinatorial search is replaced by a greedy one: QR factorization with column pivoting of $\boldsymbol{\Psi}_r^T$,

$$
\boldsymbol{\Psi}_r^T\mathbf{P} = \mathbf{Q}\mathbf{R}
$$

picks at each step the grid point whose row of $\boldsymbol{\Psi}_r$ has the largest component orthogonal to the rows already chosen. The first $r$ pivots in $\mathbf{P}$ are the sensor locations (Manohar et al. 2018). The same idea underlies the discrete empirical interpolation method used for hyper-reduction, and the reconstruction formula is the [gappy POD](../../numerical/pod/gappy_pod.md) estimate with point masks.

## Clustering and Classification

### k-means

k-means partitions $m$ points $\mathbf{a}_i$ (here usually POD coefficients, since distances between full snapshots are expensive and noisy) into $K$ clusters $C_1, \dots, C_K$ with centroids $\mathbf{c}_j$ by minimizing the within-cluster sum of squares

$$
J = \sum_{j=1}^{K}\sum_{i \in C_j} \lVert \mathbf{a}_i - \mathbf{c}_j \rVert^2
$$

Lloyd's algorithm alternates two steps:

1. Assign each point to the cluster of its nearest centroid.
2. Move each centroid to the mean of its members, $`\mathbf{c}_j = |C_j|^{-1}\sum_{i \in C_j}\mathbf{a}_i`$.

Each step minimizes $J$ over one set of unknowns with the other held fixed, so $J$ never increases, and since there are finitely many partitions the iteration terminates. It finds a local minimum only, so practical codes restart from several k-means++ seeds (Arthur and Vassilvitskii, ACM-SIAM Symposium on Discrete Algorithms, 2007), which pick each new initial centroid with probability proportional to its squared distance from the centroids already chosen. $K$ is chosen from the elbow in $J(K)$, from a silhouette score, or from the physics. Gaussian mixture models are the probabilistic generalization, with soft assignments and per-cluster covariances.

Because the POD coordinates are orthonormal projections, Euclidean distances between coefficient vectors equal the (weighted) distances between the rank-$`r`$ reconstructions of the fields, so clusters in POD space are clusters of flow fields. A centroid maps back to a field, $\bar{\mathbf{x}} + \mathbf{U}_r\mathbf{c}_j$, which can be checked against physical intuition.

![POD coefficients of a regime-switching wake clustered by k-means, cluster sequence and centroid fields](../../../scripts/plots/flow_regime_clustering/flow_regime_clustering.png)

In the figure, a synthetic wake switches between an antisymmetric vortex street, a symmetric street and a nearly steady wake. In the $(a_1, a_2)$ plane each regime forms a compact group, with trails of transitional snapshots between groups, and k-means with $K = 3$ recovers the true regime of every non-transitional snapshot. The centroids (bottom row) are regime averages, so the travelling vortices seen in the individual snapshots (middle row) are averaged out.

### Cluster-Based Reduced-Order Models

Kaiser et al. (2014) turned clustering into a dynamical model. With snapshots sampled at a fixed interval $\Delta t$ and clustered into $K$ states, the transition probabilities

$$
P_{jk} = \frac{n_{jk}}{\sum_{l} n_{jl}}
$$

are estimated from the counts $n_{jk}$ of consecutive snapshot pairs that move from cluster $j$ to cluster $k$. The probability row vector $\mathbf{q}_\ell$ of being in each cluster at step $\ell$ then evolves as a Markov chain,

```math
\mathbf{q}_{\ell+1} = \mathbf{q}_\ell\,\mathbf{P}
```

The stationary distribution (the left eigenvector of $\mathbf{P}$ with eigenvalue 1) gives the fraction of time spent in each state, and the other eigenvalues give the time scales of switching. Applied to a mixing layer, the model identified a few representative states and the transitions between them, and could be inspected cluster by cluster. With $K$ much larger than the number of regimes, a periodic regime is divided into phases of its cycle, and the transition matrix approximates the cycle as a chain of clusters. The model loses phase information within each cluster and smears out deterministic dynamics into probabilities, so it represents statistics better than individual trajectories.

### Classification of Flow Regimes

When labels are available, for example "attached" and "separated", or a range of Reynolds numbers, supervised classifiers map features to labels. With POD coefficients or a few sensor readings as features $\mathbf{a}$ and classes $c = 1, \dots, C$, a softmax (multinomial logistic) classifier predicts

$$
\hat{p}_c(\mathbf{a}) = \frac{\exp(\mathbf{w}_c^T\mathbf{a} + b_c)}{\sum_{c'}\exp(\mathbf{w}_{c'}^T\mathbf{a} + b_{c'})}
$$

and is trained by minimizing the cross-entropy $`\mathcal{L} = -\sum_i \log \hat{p}_{y_i}(\mathbf{a}_i)`$. Nearest-neighbor classifiers, support vector machines and convolutional networks on vorticity images are common alternatives. Bright, Lin and Kutz (*Physics of Fluids*, 2013) classified the Reynolds-number regime of a cylinder wake from a few surface pressure sensors by combining a library of POD modes per regime with sparse representation; Colvert, Alsalman and Kanso (*Bioinspiration & Biomimetics*, 2018) trained neural networks to classify the wake topology (2S, 2P) behind an oscillating airfoil from local vorticity time series.

Two pitfalls are specific to flow data. Neighbouring snapshots of one run are nearly identical, so a random train/test split leaks information and overstates accuracy; split by run or by blocks of time instead. Classes are often unbalanced (transitions are rare), so report per-class accuracy or a confusion matrix, not only the overall accuracy.

### Comparison

| Method | Map | Decoder | Cost for $m$ snapshots of size $n$ | Data needed | Interpretability |
| --- | --- | --- | --- | --- | --- |
| POD / PCA | linear | linear, exact | $O(nm^2)$ SVD, or $O(nmr)$ randomized | small | orthogonal modes ranked by energy |
| Kernel PCA | nonlinear | pre-image problem | $O(nm^2 + m^3)$ | moderate | low; depends on kernel |
| Autoencoder | nonlinear | learned | training cost, many epochs | large | low; latent axes not unique |
| Isomap, diffusion maps | nonlinear | none (needs regression) | $O(nm^2 + m^3)$ | dense sampling of the manifold | coordinates often physical (phase, position) |
| k-means, CROM | discrete | centroids | $O(nmK)$ per iteration | moderate | centroids are flow fields |
| QR sensor placement | linear | POD reconstruction | $O(nr^2)$ | as for POD | sensor locations |

## Practical Workflow

1. Define what is sought: compression, coherent structures, flow states or sensor locations. This fixes the method and the error measure.
2. Assemble the snapshots with sufficient temporal and spatial resolution, subtract the mean, scale each variable (for example by a reference velocity and dynamic pressure) and include cell volumes in the inner product.
3. Compute POD (randomized SVD if $\mathbf{X}$ does not fit in memory), inspect the singular value spectrum and the leading modes, and pick $r$.
4. If the spectrum decays slowly because of convection or large deformations, try an autoencoder or a manifold-learning embedding of the same dimension and compare validation errors with POD.
5. Cluster in the reduced coordinates to find regimes, check that centroids look like physically recognizable fields, and build a transition matrix if switching dynamics matter.
6. Validate on held-out runs or time windows and compare modes, clusters and sensor locations with known physics or independent measurements.

## Key Takeaways

- POD (the SVD of the mean-subtracted snapshot matrix) is the optimal linear embedding; its singular values give the reconstruction error of every truncation directly.
- A linear autoencoder can only rediscover the POD subspace, so a nonlinear autoencoder is worth its cost only when it clearly beats POD at the same latent dimension.
- Convection-dominated flows have slowly decaying POD spectra even when the underlying manifold is low-dimensional; kernel PCA, autoencoders and manifold learning target this case.
- Randomized SVD makes POD affordable for very large data, and QR pivoting on the POD basis places a few sensors from which the whole field can be estimated.
- k-means on POD coefficients turns flow data into discrete states with interpretable centroids, and transition counts between clusters give a Markov model of regime switching.
- Snapshots from the same run are strongly correlated; split training and test data by run or by time block.

## Related Scripts

- [Flow Regime Clustering with POD and k-means](../../../scripts/plots/flow_regime_clustering/): groups the snapshots of a synthetic wake that switches between three flow regimes into clusters, by projecting them onto their leading POD modes and running k-means on the POD coefficients.
- [Dynamic Mode Decomposition (DMD)](../../../scripts/algorithms/dynamic_mode_decomposition/): applies exact dynamic mode decomposition to a noisy synthetic 1D wave field built from three wave packets whose frequencies and growth rates are known, and checks how well DMD recovers them.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [Learning Paradigms on Flow Data](../../../scripts/plots/ml_learning_paradigms/): Three panels contrast supervised regression, supervised classification and unsupervised clustering on synthetic flow data, each computed in numpy.
- [Gappy POD Reconstruction](../../../scripts/algorithms/gappy_pod_reconstruction/): reconstructs complete flow fields from incomplete data with gappy POD: a POD basis built from complete snapshots of a synthetic cylinder wake is fitted by least squares to held-out snapshots of which only 50% of the points, or a few point sensors, are known.

## Exercises

**Exercise 1.** A snapshot matrix has singular values $\sigma = (10, 5, 2, 1, 0.5)$. Compute the cumulative energy fraction $E_r/E$ for $r = 1, \dots, 5$ and find the smallest $r$ that captures at least 99% of the energy.

<details>
<summary>Answer</summary>

The energies are $\sigma_j^2 = (100, 25, 4, 1, 0.25)$, which sum to 130.25.

The cumulative fractions are 0.768, 0.960, 0.990, 0.998 and 1.000.

$r = 3$ is the smallest rank that captures at least 99% (99.04%).

</details>

**Exercise 2.** For the same data, what is the smallest possible squared reconstruction error $\lVert \mathbf{X} - \tilde{\mathbf{X}} \rVert_F^2$ of any rank-2 approximation? A linear autoencoder with a two-dimensional latent space is trained on the (mean-subtracted) data. Can it beat this error? What would it mean if a nonlinear autoencoder with a two-dimensional latent space reached 1% relative error?

<details>
<summary>Answer</summary>

By the Eckart–Young theorem the best rank-2 approximation is the truncated SVD, with error $\sum_{j > 2}\sigma_j^2 = 4 + 1 + 0.25 = 5.25$, or $`5.25/130.25 = 4.0\%`$ of the total.

A linear autoencoder computes $\mathbf{W}_d\mathbf{W}_e\mathbf{x}$, a rank-2 map, so it cannot go below 4.0%. At best it learns the span of the first two POD modes.

A nonlinear autoencoder reaching 1% would show that the data lie close to a curved two-dimensional manifold that no two-dimensional linear subspace can represent. The comparison must be made on validation data; on training data a large network can reach a low error by memorising.

</details>

**Exercise 3.** A flow dataset has $n = 10^6$ values per snapshot and $m = 500$ snapshots, stored as 8-byte floats. Compute the storage of $\mathbf{X}$ and of a rank-20 POD representation ($\mathbf{U}_r$, $\boldsymbol{\Sigma}_r$, $\mathbf{V}_r$). Why is forming $\mathbf{X}\mathbf{X}^T$ out of the question? Estimate the ratio of floating-point work between a full thin SVD and a randomized SVD with $r = 20$ and oversampling $p = 10$.

<details>
<summary>Answer</summary>

$\mathbf{X}$ takes $10^6 \times 500 \times 8 = 4.0 \times 10^9$ bytes, or 4 GB.

At rank 20, $\mathbf{U}_r$ takes $10^6 \times 20 \times 8 = 160$ MB, $\mathbf{V}_r$ takes $500 \times 20 \times 8 = 80$ kB, and $\boldsymbol{\Sigma}_r$ is 20 numbers. The compression ratio is about 25.

$\mathbf{X}\mathbf{X}^T$ would be a $10^6 \times 10^6$ matrix of $8 \times 10^{12}$ bytes (8 TB). The method of snapshots ($500 \times 500$) or a randomized SVD avoids forming it.

The thin SVD costs $O(nm^2)$ and the randomized SVD $O(nm(r + p))$, so the ratio is about $m/(r + p) = 500/30 \approx 17$, before counting power iterations, each of which adds two more products with $\mathbf{X}$.

</details>

**Exercise 4.** A field on five equally spaced points is represented by two orthonormal modes, $\boldsymbol{\psi}_1 = (1, 1, 1, 1, 1)/\sqrt{5}$ and $\boldsymbol{\psi}_2 = (-2, -1, 0, 1, 2)/\sqrt{10}$. Apply QR pivoting to $\boldsymbol{\Psi}_2^T$ to choose two sensor locations, compare $\lvert\det(\mathbf{C}\boldsymbol{\Psi}_2)\rvert$ with that of sensors at points 1 and 2, and reconstruct the field from the readings $y_1 = 0.262$ and $y_5 = 1.527$.

<details>
<summary>Answer</summary>

The columns of $\boldsymbol{\Psi}_2^T$ are the rows of $\boldsymbol{\Psi}_2$, with norms $\sqrt{1/5 + 4/10} = 0.775$ at points 1 and 5, $\sqrt{1/5 + 1/10} = 0.548$ at points 2 and 4, and $0.447$ at point 3. The first pivot is point 1 (tied with point 5).

After removing the component along row 1, the largest remainder is at point 5, so the sensors are at points 1 and 5, the two ends.

```math
\mathbf{C}\boldsymbol{\Psi}_2 = \begin{bmatrix} 1/\sqrt{5} & -2/\sqrt{10} \\ 1/\sqrt{5} & 2/\sqrt{10} \end{bmatrix}, \qquad \lvert\det\rvert = \frac{4}{\sqrt{50}} = 0.566
```

Sensors at points 1 and 2 give $1/\sqrt{50} = 0.141$, four times smaller, so noise in the readings would be amplified much more.

Solving $\mathbf{C}\boldsymbol{\Psi}_2\hat{\mathbf{a}} = (0.262, 1.527)$: the sum of the two equations gives $2\hat{a}_1/\sqrt{5} = 1.789$, so $\hat{a}_1 = 2.00$; the difference gives $4\hat{a}_2/\sqrt{10} = 1.265$, so $\hat{a}_2 = 1.00$. The reconstructed field is $2\boldsymbol{\psi}_1 + \boldsymbol{\psi}_2 = (0.262, 0.578, 0.894, 1.211, 1.527)$.

</details>

**Exercise 5.** k-means on reduced coordinates assigns successive snapshots to clusters as A, A, B, B, C, A, A, B, C, C, A, B. Estimate the transition matrix of the cluster-based Markov model and describe the dominant cycle.

<details>
<summary>Answer</summary>

The 11 transitions are AA: 2, AB: 3, BB: 1, BC: 2, CA: 2, CC: 1. Normalizing each row gives

```math
\mathbf{P} = \begin{bmatrix} 0.4 & 0.6 & 0 \\ 0 & 1/3 & 2/3 \\ 2/3 & 0 & 1/3 \end{bmatrix}
```

with rows and columns ordered A, B, C.

The dominant cycle is A to B to C and back to A, with each state often repeating once before moving on. This is how a cluster-based model represents a quasi-periodic flow. Twelve snapshots are far too few for reliable probabilities; a real model needs many periods of data.

</details>

## References

- Holmes, P., Lumley, J. L., Berkooz, G., and Rowley, C. W., *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
- Taira, K., Brunton, S. L., Dawson, S. T. M., Rowley, C. W., Colonius, T., McKeon, B. J., Schmidt, O. T., Gordeyev, S., Theofilis, V., and Ukeiley, L. S., "Modal analysis of fluid flows: An overview", *AIAA Journal* 55(12), 4013–4041, 2017.
- Brunton, S. L., and Kutz, J. N., *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*, Cambridge University Press, 2019.
- Brunton, S. L., Noack, B. R., and Koumoutsakos, P., "Machine learning for fluid mechanics", *Annual Review of Fluid Mechanics* 52, 477–508, 2020.
- Baldi, P., and Hornik, K., "Neural networks and principal component analysis: Learning from examples without local minima", *Neural Networks* 2(1), 53–58, 1989.
- Milano, M., and Koumoutsakos, P., "Neural network modeling for near wall turbulent flow", *Journal of Computational Physics* 182(1), 1–26, 2002.
- Halko, N., Martinsson, P.-G., and Tropp, J. A., "Finding structure with randomness: Probabilistic algorithms for constructing approximate matrix decompositions", *SIAM Review* 53(2), 217–288, 2011.
- Gavish, M., and Donoho, D. L., "The optimal hard threshold for singular values is $4/\sqrt{3}$", *IEEE Transactions on Information Theory* 60(8), 5040–5053, 2014.
- Manohar, K., Brunton, B. W., Kutz, J. N., and Brunton, S. L., "Data-driven sparse sensor placement for reconstruction: Demonstrating the benefits of exploiting known patterns", *IEEE Control Systems Magazine* 38(3), 63–86, 2018.
- Kaiser, E., Noack, B. R., Cordier, L., Spohn, A., Segond, M., Abel, M., Daviller, G., Östh, J., Krajnović, S., and Niven, R. K., "Cluster-based reduced-order modelling of a mixing layer", *Journal of Fluid Mechanics* 754, 365–414, 2014.
