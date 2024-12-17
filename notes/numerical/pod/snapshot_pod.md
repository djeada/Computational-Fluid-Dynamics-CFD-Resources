## The Snapshot POD

The Proper Orthogonal Decomposition (POD) is a powerful technique used to identify the most energetic modes (patterns) in a dataset—often coming from fluid dynamics, structural vibrations, or other complex systems. Traditional POD can be performed in two main ways: the so-called **Direct POD** and the **Snapshot POD**. While Direct POD deals directly with large covariance matrices that can be huge if the spatial dimension is large, Snapshot POD provides a more computationally tractable route when the number of snapshots (time samples) is smaller than the spatial dimension.

### Symmetry in the POD Equation

A key concept behind POD is that it involves decomposing a field $\mathbf{u}'(\mathbf{x}, t)$ into modes that depend either on space or on time. Mathematically, POD often starts from an equation like:

$$\mathbf{u}'(\mathbf{x}, t) = \sum_{k=1}^{\infty} a_k(t) \mathbf{\Phi}_k(\mathbf{x}), \quad (1)$$

Here:

- $\mathbf{x}$ is the spatial coordinate.
- $t$ is the temporal variable.
- $\mathbf{\Phi}_k(\mathbf{x})$ are spatial modes.
- $a_k(t)$ are temporal coefficients.

This expression exhibits a certain symmetry: if you imagine interchanging the role of space and time, the same formalism applies. This conceptual symmetry underlies the idea behind Snapshot POD, as introduced by Sirovich. Instead of focusing on the spatial dimension first, Snapshot POD leverages the time dimension (or more generally, the dimension that has fewer samples) to simplify computations.

### Snapshot POD Methods

Recall that POD involves constructing a covariance matrix from your data and performing an eigenvalue decomposition to extract the principal modes. There are two common approaches:

I. **First Method (Transpose the Snapshot Matrix)**:

Take your snapshot matrix $\mathbf{U}$, which is usually sized $m \times n$ (with $m$ representing the number of snapshots and $n$ the number of spatial points). If performing Direct POD is challenging, you can instead transpose $\mathbf{U}$ (forming $\mathbf{U}^T$) and apply direct POD to this transposed data. Since transposition swaps the roles of $m$ and $n$, you effectively switch what you consider as the "parameter" dimension and the "measurement" dimension.

II. **Second Method (Use the Original Snapshot Matrix)**:

The hallmark of Snapshot POD as originally proposed by Sirovich is that you keep the original $m \times n$ snapshot matrix $\mathbf{U}$ intact, but you form a correlation matrix differently:

$$\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T.$$

Notice that in Direct POD, you'd consider $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$, an $n \times n$ matrix (if you have $n$ spatial points). However, now $\mathbf{C}_s$ is $m \times m$, which can be much smaller and thus computationally more feasible if $m < n$.

### The Correlation Matrix $\mathbf{C}_s$

The matrix $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ can be interpreted as follows:

- Instead of averaging along the temporal dimension to form a large $n \times n$ matrix, you are now considering a correlation matrix along the snapshot dimension, resulting in an $m \times m$ matrix.
- Since $m$ (the number of snapshots) is typically much smaller than $n$ (the number of spatial points), $\mathbf{C}_s$ is computationally more manageable.

You then compute the eigenvalue decomposition:

$$[A_s, LAM_s] = \text{eig}(C_s),$$

where $A_s \in \mathbb{R}^{m \times m}$ contains eigenvectors and $LAM_s$ is the diagonal matrix of eigenvalues. These eigenvectors represent temporal modes in this framework.

### From Temporal Modes to Spatial Coefficients

Once you have the temporal modes from $\mathbf{C}_s$, you still need the spatial patterns. Since your original data is in $\mathbf{U}$, you can recover the spatial coefficients:

$$\mathbf{\Phi}_s = \mathbf{U}^T A_s,$$

where $\mathbf{\Phi}_s$ will provide the spatial structures of the modes. This step effectively translates the temporal mode representation into spatial patterns.

### Equivalence and Differences from Direct POD

**Eigenvalues**: The eigenvalues you get from Snapshot POD match those you would get from Direct POD. Both methods identify the same energy distribution among modes. This ensures that no matter which approach you use, the fundamental modal decomposition remains consistent.

**Modes and Coefficients**: The main difference lies in what is orthonormal and where scaling factors appear:

- In Direct POD:
- Spatial modes are orthonormal in space.
- Time coefficients can be determined directly and typically require no additional scaling.
- In Snapshot POD:
- Temporal modes end up being orthonormal.
- The spatial modes you recover from $\mathbf{U}^T A_s$ are not initially normalized and often must be scaled appropriately.

### Normalization and Scaling

To align the results of Snapshot POD with those of Direct POD, a normalization step is often required. This ensures that you end up with a consistent set of modes and coefficients across different approaches. Although Snapshot POD initially yields temporal modes that are orthonormal and spatial modes that are not, simple post-processing (normalization and scaling) rectifies these differences.

### Reconstructing the Original Data

An essential property of POD (including Snapshot POD) is that you can reconstruct the original data matrix $\mathbf{U}$ using the product of spatial coefficients and temporal modes. Specifically, from the Snapshot POD framework:

$$\mathbf{U} = A_s \mathbf{\Phi}_s^T,$$

where:
- $\mathbf{A}_s$ contains the spatial coefficients.
- $\mathbf{\Phi}_s$ contains the temporal modes.

This decomposition shows that every snapshot can be rebuilt from a sum of modal contributions, affirming the completeness of the POD approximation.

### Computational Advantages of Snapshot POD

The main advantage of Snapshot POD is computational efficiency, especially when the spatial dimension $n$ is huge while the number of snapshots $m$ is relatively small:

- **Reduced Matrix Size**: Instead of dealing with an $n \times n$ covariance matrix (which could be huge), Snapshot POD deals with an $m \times m$ matrix. Since $m < n$ typically, this is a significant reduction in computational cost.
- **Faster Eigen-decompositions**: Computing the eigenvalue decomposition for a smaller $m \times m$ matrix is more tractable, saving both memory and CPU time.
- **Practical Example**: For complex fluid flow fields (e.g., a turbulent separation bubble):
- Direct POD would require forming and decomposing an enormous $n \times n$ matrix, with $n$ possibly in the millions.
- Snapshot POD only deals with an $m \times m$ matrix, with $m$ being the number of snapshots (often in the order of hundreds or thousands, which is far more manageable than millions).

### Use Cases

- **Snapshot POD**: Ideal when your dataset comes from, say, PIV (Particle Image Velocimetry) experiments or from large-scale CFD simulations, where you have a few hundred or thousand snapshots of a very high-dimensional field.
- **Direct POD**: More practical when you have a small set of spatial points but a very large number of time samples (or other parameters). It's less common in high-dimensional CFD but may arise in experimental setups with very limited spatial sensors but continuous time measurements.

### Practical Equivalence

Both Snapshot and Direct POD methods yield the same set of significant modes (limited by $\min(m,n)$). If $m<n$, some modes from the direct method would correspond to zero eigenvalues and be physically irrelevant. Snapshot POD naturally avoids dealing with those irrelevant modes due to its truncated dimension. Additionally:

- The sign of the modes (or time coefficients) may differ between methods. This is inconsequential, as a negative sign can be absorbed either in the mode shape or the coefficient. The physics (energy, variance captured) remains the same.
