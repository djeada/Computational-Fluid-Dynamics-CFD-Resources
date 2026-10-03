## The Snapshot POD

The Proper Orthogonal Decomposition (POD) is a powerful technique used to identify the most energetic modes (patterns) in a dataset—often coming from fluid dynamics, structural vibrations, or other complex systems. Traditional POD can be performed in two main ways: the so-called **Direct POD** and the **Snapshot POD**. While Direct POD deals directly with large covariance matrices that can be huge if the spatial dimension is large, Snapshot POD provides a more computationally tractable route when the number of snapshots (time samples) is smaller than the spatial dimension.

### Symmetry in the POD Equation

A key concept behind POD is that it involves decomposing a field $\mathbf{u}'(\mathbf{x}, t)$ into modes that depend either on space or on time. Mathematically, POD often starts from an equation like:

$$
\mathbf{u}'(\mathbf{x}, t) = \sum_{k=1}^{\infty} a_k(t) \mathbf{\Phi}_k(\mathbf{x}),
\quad (1)
$$

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

$$
\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T
$$

Notice that in Direct POD, you'd consider $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$, an $n \times n$ matrix (if you have $n$ spatial points). However, now $\mathbf{C}_s$ is $m \times m$, which can be much smaller and thus computationally more feasible if $m < n$.

### The Correlation Matrix $\mathbf{C}_s$

The matrix $\mathbf{C}_s = \frac{1}{m-1}\mathbf{U}\mathbf{U}^T$ can be interpreted as follows:

- Instead of averaging along the temporal dimension to form a large $n \times n$ matrix, you are now considering a correlation matrix along the snapshot dimension, resulting in an $m \times m$ matrix.
- Since $m$ (the number of snapshots) is typically much smaller than $n$ (the number of spatial points), $\mathbf{C}_s$ is computationally more manageable.

You then compute the eigenvalue decomposition:

$$
[A_s, LAM_s] = \text{eig}(C_s)
$$

where $A_s \in \mathbb{R}^{m \times m}$ contains eigenvectors and $LAM_s$ is the diagonal matrix of eigenvalues. These eigenvectors represent temporal modes in this framework.

### From Temporal Modes to Spatial Coefficients

Once you have the temporal modes from $\mathbf{C}_s$, you still need the spatial patterns. Since your original data is in $\mathbf{U}$, you can recover the spatial coefficients:

$$
\mathbf{\Phi}_s = \mathbf{U}^T A_s
$$

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

An essential property of POD (including Snapshot POD) is that you can reconstruct the original data matrix $\mathbf{U}$ using the product of temporal modes and spatial modes. Specifically, from the Snapshot POD framework:

$$
\mathbf{U} = A_s \mathbf{\Phi}_s^T
$$

where:

- $A_s$ contains the temporal modes (time coefficients).
- $\mathbf{\Phi}_s$ contains the (unnormalized) spatial modes.

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

Both Snapshot and Direct POD methods yield the same set of significant modes (limited by $\min(m,n)$). If $m < n$, some modes from the direct method would correspond to zero eigenvalues and be physically irrelevant. Snapshot POD naturally avoids dealing with those irrelevant modes due to its truncated dimension. Additionally:

- The sign of the modes (or time coefficients) may differ between methods. This is inconsequential, as a negative sign can be absorbed either in the mode shape or the coefficient. The physics (energy, variance captured) remains the same.

## Purpose in CFD

In high-fidelity CFD the spatial dimension $n$ (millions of grid points) far exceeds the number of snapshots $m$ (hundreds or thousands). Snapshot POD avoids forming the huge $n \times n$ covariance matrix by instead working with the much smaller $m \times m$ correlation matrix, making the eigenvalue decomposition tractable. This note explains both Snapshot POD methods, the normalization step needed to recover spatial modes, and the computational savings.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Snapshot matrix $\mathbf{U} \in \mathbb{R}^{m \times n}$ with $m \ll n$ |
| **Outputs** | Correlation matrix $\mathbf{C}_s \in \mathbb{R}^{m \times m}$, eigenvalues (same as Direct POD), temporal modes $A_s$, spatial modes $\boldsymbol{\Phi}_s = \mathbf{U}^T A_s$ (after normalization) |

## Related Scripts

- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.

## Exercises

**Exercise 1.** For the separation-bubble data ($m = 3580$ snapshots, $n = 5805$ points), by what factor is the snapshot correlation matrix $\mathbf{C}_s$ smaller in storage than $\mathbf{C}$? Repeat for a simulation with $m = 1000$ snapshots and $n = 10^6$ cells.

<details>
<summary>Answer</summary>

The storage ratio is $(n/m)^2$. For the separation bubble, $(5805/3580)^2 \approx 2.63$, a modest saving. For the simulation, $(10^6/10^3)^2 = 10^6$: $\mathbf{C}$ would need 8 TB while $\mathbf{C}_s$ needs 8 MB.

</details>

**Exercise 2.** Take $m = 2$ snapshots at $n = 3$ points,

$$
\mathbf{U} = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 2 & 1 \end{pmatrix}
$$

used without mean subtraction, so that $\frac{1}{m-1} = 1$. Compute $\mathbf{C}_s$, its eigenvalues and eigenvectors $A_s$, the unnormalized spatial modes $\mathbf{\Phi}_s = \mathbf{U}^T A_s$ and their norms, and the normalized modes. Compare with the eigen-decomposition of $\mathbf{C} = \mathbf{U}^T\mathbf{U}$.

<details>
<summary>Answer</summary>

$\mathbf{C}_s = \mathbf{U}\mathbf{U}^T = \begin{pmatrix} 5 & 4 \\ 4 & 6 \end{pmatrix}$. Its eigenvalues are $(11 \pm \sqrt{65})/2$, i.e. $\lambda_1 = 9.5311$ and $\lambda_2 = 1.4689$, with eigenvectors $a_1 = (0.6618, 0.7497)$ and $a_2 = (-0.7497, 0.6618)$.

$\mathbf{U}^T a_1 = (2.0733, 2.1612, 0.7497)$ has norm $3.0873 = \sqrt{\lambda_1}$. $\mathbf{U}^T a_2 = (-0.8376, 0.5739, 0.6618)$ has norm $1.2120 = \sqrt{\lambda_2}$. Dividing by these norms gives $\phi_1 = (0.6716, 0.7000, 0.2428)$ and $\phi_2 = (-0.6911, 0.4735, 0.5461)$.

Direct POD: $\mathbf{C} = \begin{pmatrix} 5 & 4 & 1 \\ 4 & 5 & 2 \\ 1 & 2 & 1 \end{pmatrix}$ has eigenvalues $9.5311, 1.4689, 0$, and its first two eigenvectors equal $\phi_1$ and $\phi_2$ up to sign. The third mode has zero energy and is not needed.

</details>

**Exercise 3.** Prove the eigenvalue equivalence. If $\mathbf{C}_s a = \lambda a$ with $\|a\| = 1$ and $\lambda > 0$, show that $\mathbf{U}^T a$ is an eigenvector of $\mathbf{C} = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}$ with the same eigenvalue, and that $\|\mathbf{U}^T a\|^2 = (m-1)\lambda$. Deduce the normalization $\phi = \mathbf{U}^T a/\sqrt{(m-1)\lambda}$.

<details>
<summary>Answer</summary>

$$
\mathbf{C}\,(\mathbf{U}^T a) = \frac{1}{m-1}\mathbf{U}^T\mathbf{U}\mathbf{U}^T
a = \mathbf{U}^T\mathbf{C}_s a = \lambda\,\mathbf{U}^T a
$$

$\mathbf{U}^T a \neq 0$ because $\|\mathbf{U}^T a\|^2 = a^T\mathbf{U}\mathbf{U}^T a = (m-1)\,a^T\mathbf{C}_s a = (m-1)\lambda > 0$. Dividing by the square root of this norm gives a unit spatial mode, $\phi = \mathbf{U}^T a/\sqrt{(m-1)\lambda}$. In Exercise 2, $m - 1 = 1$ and the norms were $\sqrt{\lambda}$.

</details>

**Exercise 4.** Show that $\mathbf{U} = A_s\mathbf{\Phi}_s^T$, where $\mathbf{\Phi}_s = \mathbf{U}^T A_s$ is unnormalized. Then show that the direct-POD time coefficients $\mathbf{U}\phi_k$ (with normalized $\phi_k$) equal $\sqrt{(m-1)\lambda_k}\,a_k$, and evaluate the first column for Exercise 2.

<details>
<summary>Answer</summary>

$A_s$ is an orthogonal $m \times m$ matrix, so $A_s\mathbf{\Phi}_s^T = A_s A_s^T\mathbf{U} = \mathbf{U}$.

With $\phi_k = \mathbf{U}^T a_k/\sqrt{(m-1)\lambda_k}$:

$$
\mathbf{U}\phi_k = \frac{\mathbf{U}\mathbf{U}^T a_k}{\sqrt{(m-1)\lambda_k}} = \frac{(m-1)\lambda_k\,a_k}{\sqrt{(m-1)\lambda_k}} = \sqrt{(m-1)\lambda_k}\; a_k
$$

So the snapshot eigenvectors are the time coefficients rescaled to unit norm; this is the scaling step mentioned in the note. For Exercise 2, $\mathbf{U}\phi_1 = 3.0873 \times (0.6618, 0.7497) = (2.0432, 2.3144)$.

</details>

## References

- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987.
- J. Weiss, "A Tutorial on the Proper Orthogonal Decomposition", *AIAA Aviation 2019 Forum*, Dallas, Texas, 2019.
- P. Holmes, J. L. Lumley, G. Berkooz and C. W. Rowley, *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
