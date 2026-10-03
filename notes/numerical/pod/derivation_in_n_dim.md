# Derivation of POD for N Dimensions

## Introduction

- Proper Orthogonal Decomposition (POD) is a powerful tool for analyzing large-dimensional datasets.
- This guide explains the application of POD to a complete longitudinal velocity field measured by Particle Image Velocimetry (PIV).

## Snapshot Matrix Creation

1. **Subtraction of Time-Averaged Velocity Field**

   - Subtract the time-averaged velocity field from each individual vector field to obtain fluctuating velocity fields $u'(x_i, y_j, t_k)$.

2. **Reordering Dataset**

   - For each time instant $t_k$, concatenate the velocity fields into a single $1 \times n$ row.
   - Stack these rows to form an $m \times n$ snapshot matrix $\mathbf{U}$.

$$
\mathbf{U} =
\begin{pmatrix}
u'(x_1, y_1, t_1) & \cdots & u'(x_{N_x}, y_{N_y}, t_1) \\
u'(x_1, y_1, t_2) & \cdots & u'(x_{N_x}, y_{N_y}, t_2) \\
\vdots & \ddots & \vdots \\
u'(x_1, y_1, t_m) & \cdots & u'(x_{N_x}, y_{N_y}, t_m)
\end{pmatrix}
$$

- Here, $m = N_t = 3580$ and $n = N_x \times N_y = 5805$.

## Covariance Matrix and Eigen Decomposition

1. **Compute Covariance Matrix**

   - Calculate the covariance matrix $\mathbf{C} = \frac{1}{m-1} \mathbf{U}^T \mathbf{U}$.
   - $\mathbf{C}$ is an $n \times n$ matrix.

2. **Eigenvalues and Eigenvectors**

   - Compute the eigenvalues and eigenvectors using MATLAB command `[PHI LAM] = eig(C)`.
   - Order the eigenvalues from largest to smallest and arrange the corresponding eigenvectors in matrix $\mathbf{\Phi}$.

$$
\mathbf{\Phi} =
\begin{pmatrix}
\phi_{11} & \cdots & \phi_{1n} \\
\phi_{21} & \cdots & \phi_{2n} \\
\vdots & \ddots & \vdots \\
\phi_{n1} & \cdots & \phi_{nn}
\end{pmatrix}
$$

## Visualization of Modes

- The eigenvectors (columns of $\mathbf{\Phi}$) are the proper orthogonal modes.
- To visualize these modes, reverse the reordering process to create $N_x \times N_y$ fields for each column of $\mathbf{\Phi}$.

## Interpretation of POD Modes

1. **Mode Interpretation**

   - Each POD mode represents a pattern of velocity fluctuations.
   - For example, mode 1 might indicate a global fluctuation, while modes 2 and 3 show anti-correlated fluctuations.

2. **Contour Plots**

   - Plot the first few modes as contour plots to visualize the spatial distribution of fluctuations.
   - These plots help in understanding the correlation and anti-correlation in the velocity fields.

## Extending the Snapshot Matrix

1. **Including Vertical Velocity**
   - Extend the snapshot matrix to include both longitudinal ($u'$) and vertical ($v'$) velocity components.

$$
\mathbf{U} =
\begin{pmatrix}
u'(x_1, y_1, t_1) & \cdots & u'(x_{N_x}, y_{N_y}, t_1) & v'(x_1, y_1, t_1) & \cdots & v'(x_{N_x}, y_{N_y}, t_1) \\
u'(x_1, y_1, t_2) & \cdots & u'(x_{N_x}, y_{N_y}, t_2) & v'(x_1, y_1, t_2) & \cdots & v'(x_{N_x}, y_{N_y}, t_2) \\
\vdots & \ddots & \vdots & \vdots & \ddots & \vdots \\
u'(x_1, y_1, t_m) & \cdots & u'(x_{N_x}, y_{N_y}, t_m) & v'(x_1, y_1, t_m) & \cdots & v'(x_{N_x}, y_{N_y}, t_m)
\end{pmatrix}
$$

2. **Three-Dimensional Velocity Data**
   - For 3D velocity data, include all three components in the snapshot matrix.
   - Adjust the matrix dimensions accordingly and account for increased storage and computation requirements.

## Necessity of Interpreting All Modes

- **Low-Order Modes Focus**: Typically, only a few low-order modes are analyzed.
- **Variance Contribution**: POD ranks modes by their contribution to the total variance.
  - The first mode often contributes significantly to the total kinetic energy (TKE).
  - Example: First mode ≈ 20% TKE, second mode ≈ 8% TKE, subsequent modes contribute less.

## Eigenvalues and TKE Contribution

- **Plot of Eigenvalues**: The first 10 eigenvalues illustrate their contributions to TKE.
  - Largest eigenvalue is dominant.
  - Contribution diminishes with higher modes.

## Projection of Original Dataset onto Modes

1. **Projection Equation**:

$$
\mathbf{A} = \mathbf{U} \mathbf{\Phi}
$$

- $\mathbf{A}$ represents the projections of the original dataset onto each mode.
- Each $a_{ij}$ is the projection of data measured at time $i$ on mode $j$.

2. **Time Coefficients of Modes**:
   - Each column of $\mathbf{A}$ is the time coefficient of the corresponding mode.
   - Time coefficients illustrate how each mode varies over time.

## Reconstruction of Original Snapshot Matrix

1. **Reconstruction Equation**:

$$
\mathbf{U} = \mathbf{A} \mathbf{\Phi}^T
$$

- The original snapshot matrix $\mathbf{U}$ can be expressed as the sum of contributions from all $n$ modes.

2. **Contribution from Each Mode**:

$$
\mathbf{U} = \tilde{\mathbf{U}}^1 + \tilde{\mathbf{U}}^2 + \cdots + \tilde{\mathbf{U}}^n
$$

- Each $\tilde{\mathbf{U}}^k$ is the contribution of mode $k$ to the snapshot matrix.
- Each contribution can be calculated as:

$$
\tilde{\mathbf{U}}^k = \mathbf{A}_k \mathbf{\Phi}_k^T
$$

```
 - $\mathbf{A}_k$ is the time coefficient for mode $k$.
 - $\mathbf{\Phi}_k$ is the corresponding eigenvector.
```

## Derivations and Equations

1. **Snapshot Matrix**:

$$
\mathbf{U} =
\begin{pmatrix}
u_{11} & \cdots & u_{1n} \\
u_{21} & \cdots & u_{2n} \\
\vdots & \ddots & \vdots \\
u_{m1} & \cdots & u_{mn}
\end{pmatrix}
$$

- Each element $u_{ij}$ is the velocity fluctuation at point $j$ measured at time $i$.

2. **Covariance Matrix**:

$$
\mathbf{C} = \frac{1}{m-1} \mathbf{U}^T \mathbf{U}
$$

- $\mathbf{C}$ is an $n \times n$ matrix.

3. **Eigen Decomposition**:

$$
\mathbf{\Phi} = [\phi_1, \phi_2, \ldots, \phi_n]
$$

- $\mathbf{\Phi}$ contains the eigenvectors.
- Eigenvalues and eigenvectors are obtained using MATLAB command `[PHI, LAM] = eig(C)`.

4. **Projection Matrix**:

$$
\mathbf{A} =
\begin{pmatrix}
a_{11} & \cdots & a_{1n} \\
a_{21} & \cdots & a_{2n} \\
\vdots & \ddots & \vdots \\
a_{m1} & \cdots & a_{mn}
\end{pmatrix}
$$

## Visualization and Analysis

- **Contour Plots**: Visualize the first few modes as contour plots to understand spatial distribution.
- **Identification of Coherent Structures**: The first few modes usually capture dominant coherent motions.

## Summary

- **Focus on Dominant Modes**: Analyze the first few modes for significant insights into flow dynamics.
- **Projection and Reconstruction**: Use projection and reconstruction equations to interpret and visualize modes.
- **Efficiency**: Concentrating on a few modes is efficient and often sufficient for understanding the key features of the dataset.

## Illustrations

- **Eigenvalues Plot**:
  ![Eigenvalues Plot](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/e5b18034-bb88-458a-8cee-613bb4bf0c3d)

  - Shows the first 10 eigenvalues and their contribution to TKE.

- **Mode Contour Plots**:
  ![Mode Contour Plots](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/405dd246-3f0c-429d-9a3d-9a6b484b3895)

  - Visualizes the first three POD modes of the turbulent separation bubble as contour plots.

- **Projection and Reconstruction Illustration**:

$$
\begin{pmatrix}
u_{11} & \cdots & u_{1n} \\
u_{21} & \cdots & u_{2n} \\
\vdots & \ddots & \vdots \\
u_{m1} & \cdots & u_{mn}
\end{pmatrix} =
\begin{pmatrix}
a_{11} & \cdots & a_{1n} \\
a_{21} & \cdots & a_{2n} \\
\vdots & \ddots & \vdots \\
a_{m1} & \cdots & a_{mn}
\end{pmatrix}
\begin{pmatrix}
\phi_{11} & \cdots & \phi_{1n} \\
\phi_{21} & \cdots & \phi_{2n} \\
\vdots & \ddots & \vdots \\
\phi_{n1} & \cdots & \phi_{nn}
\end{pmatrix}
$$

$$
= \begin{pmatrix}
\tilde{u}_{11}^1 & \cdots & \tilde{u}_{1n}^1 \\
\tilde{u}_{21}^1 & \cdots & \tilde{u}_{2n}^1 \\
\vdots & \ddots & \vdots \\
\tilde{u}_{m1}^1 & \cdots & \tilde{u}_{mn}^1
\end{pmatrix} +
\cdots +
\begin{pmatrix}
\tilde{u}_{11}^n & \cdots & \tilde{u}_{1n}^n \\
\tilde{u}_{21}^n & \cdots & \tilde{u}_{2n}^n \\
\vdots & \ddots & \vdots \\
\tilde{u}_{m1}^n & \cdots & \tilde{u}_{mn}^n
\end{pmatrix}
$$

$$
\begin{pmatrix}
\tilde{u}_{11}^k & \cdots & \tilde{u}_{1n}^k \\
\tilde{u}_{21}^k & \cdots & \tilde{u}_{2n}^k \\
\vdots & \ddots & \vdots \\
\tilde{u}_{m1}^k & \cdots & \tilde{u}_{mn}^k
\end{pmatrix} =
\begin{pmatrix}
a_{1k} \\
a_{2k} \\
\vdots \\
a_{mk}
\end{pmatrix}
\begin{pmatrix}
\phi_{1k} & \cdots & \phi_{nk}
\end{pmatrix}
= \tilde{\mathbf{U}}^k
$$

## Decomposition of Velocity Fluctuations

- Each matrix $\tilde{\mathbf{U}}^k$ has the same dimensions as $\mathbf{U}$.
- The original velocity fluctuations can be decomposed into $n$ contributions from $n$ proper orthogonal modes:

$$
\mathbf{U} = \sum_{k=1}^{n} \tilde{\mathbf{U}}^k
$$

- This decomposition is the finite-dimensional equivalent of the original infinite-dimensional POD theorem:

$$
\mathbf{u}'(\mathbf{x}, t) = \sum_{k=1}^{\infty} a_k(t) \mathbf{\Phi}_k(\mathbf{x})
$$

- Here, $a_k(t)$ are the time coefficients and $\mathbf{\Phi}_k(\mathbf{x})$ are the deterministic spatial functions.

## Time Coefficients and Spatial Points

- In the finite-dimensional case:
  - $a_k(t)$ is the column vector $(a_{1k}, a_{2k}, \ldots, a_{mk})^T$.
  - $\mathbf{\Phi}_k(\mathbf{x})$ is the row vector $(\phi_{1k}, \phi_{2k}, \ldots, \phi_{nk})$.
  - Example: $m = 3580$ time coefficients (one per snapshot), $n = 5805$ spatial points.

## Orthogonality of POD Modes

- The orthonormality of the POD modes ensures that matrix $\mathbf{\Phi}$ is orthogonal:

$$
\mathbf{\Phi}^{-1} = \mathbf{\Phi}^T
$$

## Dimensionality Reduction

- Dimensionality reduction allows focusing on the dominant modes:
  - Example: First POD mode accounts for about 20% of the TKE in the flow.
  - Visualizing $\tilde{\mathbf{U}}^1$ shows the motion contributing to these fluctuations.

## Low-Order Model (LOM)

- Create a low-order model using the first POD mode:

  - Reorder $\tilde{\mathbf{U}}^1$ into $m = 3580$ snapshots.
  - Add the time-averaged flow field to the reordered snapshots.
  - The first mode represents the main motion of the TSB.

- Approximate the complete fluctuating velocity field using a limited number of POD modes:

$$
\mathbf{u}'(\mathbf{x}, t) \simeq
\tilde{\mathbf{u}}'(\mathbf{x}, t) = \sum_{k=k_1}^{k_2} a_k(t)
\mathbf{\Phi}_k(\mathbf{x})
$$

- In matrix terms:

$$
\mathbf{U} \approx \tilde{\mathbf{U}} = \sum_{k=k_1}^{k_2} \tilde{\mathbf{U}}^k
$$

## Model Reduction via POD

- Model reduction can generate a set of ordinary differential equations (finite-dimensional dynamical system) simplifying partial differential equations in fluid mechanics (Galerkin projection).

## Purpose in CFD

This note extends the 2-D POD derivation to N dimensions, which is the form used in practical CFD applications. It explains how to build the snapshot matrix $\mathbf{U}$ from PIV or simulation data, compute the $n \times n$ covariance matrix (or the $m \times m$ snapshot correlation matrix, which is cheaper when $m \ll n$), extract eigenvalues and modes, and reconstruct the original field. The procedure applies directly to velocity, pressure, or any scalar field.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Snapshot matrix $\mathbf{U} \in \mathbb{R}^{m \times n}$ (rows = time instants, columns = spatial points), number of modes to retain |
| **Outputs** | Eigenvalues $\lambda_k$, spatial modes, temporal coefficients, energy distribution, truncated reconstruction |

## Related Scripts

- [Eigenvector Projection of Velocity Fluctuations](../../../scripts/plots/eigenvector_projection/): finds the principal directions of correlated 2D velocity fluctuations from the eigenvectors of their covariance matrix and projects the data onto them.
- [Longitudinal Velocity Fluctuations and Projections](../../../scripts/plots/longitudinal_velocity_fluctuations_and_projections/): plots synthetic two-point velocity fluctuations as time traces, as a scatter cloud, and projected onto a unit vector, which are the first steps of the two-point POD example.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Modes of a Two-Point Velocity Signal](../../../scripts/plots/pod_modes_2d/): applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.

## Exercises

**Exercise 1.** For the separation-bubble data ($n = 5805$ points, $m = 3580$ snapshots), estimate the memory needed to store the covariance matrix $\mathbf{C}$ ($n \times n$) and the snapshot correlation matrix ($m \times m$) in double precision. How do these change when both $u'$ and $v'$ are included in the snapshot matrix?

<details>
<summary>Answer</summary>

- $\mathbf{C}$: $5805^2 \times 8 \approx 2.70 \times 10^8$ bytes, about 270 MB.
- $m \times m$ matrix: $3580^2 \times 8 \approx 1.03 \times 10^8$ bytes, about 103 MB.
- With $u'$ and $v'$: $n = 11610$, so $\mathbf{C}$ needs $11610^2 \times 8 \approx 1.08 \times 10^9$ bytes (about 1.08 GB, four times larger). The $m \times m$ matrix is unchanged.

</details>

**Exercise 2.** The note reports that the first POD mode holds about 20% of the TKE and the second about 8%. What fraction of the TKE is contained in the two-mode low-order model $\tilde{\mathbf{U}} = \tilde{\mathbf{U}}^1 + \tilde{\mathbf{U}}^2$, and what fraction remains in $\mathbf{U} - \tilde{\mathbf{U}}$? Why may the percentages simply be added?

<details>
<summary>Answer</summary>

The two-mode model holds $20\% + 8\% = 28\%$ and the residual holds $72\%$. The percentages add because the modes are orthonormal and the time coefficients are uncorrelated, so the energy (squared Frobenius norm) of a sum of mode contributions is the sum of their energies: $\|\tilde{\mathbf{U}}^1 + \tilde{\mathbf{U}}^2\|_F^2 = \|\tilde{\mathbf{U}}^1\|_F^2 + \|\tilde{\mathbf{U}}^2\|_F^2$ (proved in Exercise 4). A low 28% is typical of turbulent flows, where energy is spread over many modes.

</details>

**Exercise 3.** Consider $m = 3$ mean-subtracted snapshots at $n = 4$ points:

$$
\mathbf{U} = \begin{pmatrix} 1 & 0 & -1 & 2 \\ 0 & 1 & 1 & -1 \\ -1 & -1 & 0 & -1 \end{pmatrix}
$$

Compute $\mathbf{C}$, its eigenvalues and energy fractions, the first two modes, and the matrix of time coefficients $\mathbf{A} = \mathbf{U}\mathbf{\Phi}$ (first two columns). Explain why only two eigenvalues are nonzero.

<details>
<summary>Answer</summary>

```math
\mathbf{C} = \frac{1}{2}\mathbf{U}^T\mathbf{U} = \begin{pmatrix} 1 & 0.5 & -0.5 & 1.5 \\ 0.5 & 1 & 0.5 & 0 \\ -0.5 & 0.5 & 1 & -1.5 \\ 1.5 & 0 & -1.5 & 3 \end{pmatrix}
```

The eigenvalues are $4.5, 1.5, 0, 0$, giving energy fractions of 75% and 25%. The modes (up to sign) are $\mathbf{\phi}_1 = (1, 0, -1, 2)/\sqrt{6}$ and $\mathbf{\phi}_2 = (1, 2, 1, 0)/\sqrt{6}$. You can check directly that $\mathbf{C}\mathbf{\phi}_1 = 4.5\,\mathbf{\phi}_1$ and $\mathbf{C}\mathbf{\phi}_2 = 1.5\,\mathbf{\phi}_2$.

Time coefficients: $\mathbf{a}_1 = \mathbf{U}\mathbf{\phi}_1 = (6, -3, -3)/\sqrt{6} = (2.449, -1.225, -1.225)$ and $\mathbf{a}_2 = \mathbf{U}\mathbf{\phi}_2 = (0, 3, -3)/\sqrt{6} = (0, 1.225, -1.225)$. Check: $\mathbf{a}_1^T\mathbf{a}_1/2 = 4.5$, $\mathbf{a}_2^T\mathbf{a}_2/2 = 1.5$ and $\mathbf{a}_1^T\mathbf{a}_2 = 0$.

Only two eigenvalues are nonzero because $\text{rank}(\mathbf{C}) = \text{rank}(\mathbf{U}) \le m - 1 = 2$: after mean subtraction the three rows sum to zero. In the separation-bubble case at most $3579$ of the $5805$ eigenvalues can be nonzero.

</details>

**Exercise 4.** Using $\mathbf{C}\mathbf{\Phi} = \mathbf{\Phi}\mathbf{\Lambda}$ with orthonormal $\mathbf{\Phi}$, prove that the time coefficients are uncorrelated, $\frac{1}{m-1}\mathbf{A}^T\mathbf{A} = \mathbf{\Lambda}$. Then show that the truncation error satisfies $\|\mathbf{U} - \sum_{k=1}^{r}\tilde{\mathbf{U}}^k\|_F^2 = (m-1)\sum_{k > r}\lambda_k$, and check this for $r = 1$ with the matrix of Exercise 3.

<details>
<summary>Answer</summary>

$\frac{1}{m-1}\mathbf{A}^T\mathbf{A} = \mathbf{\Phi}^T\left(\frac{1}{m-1}\mathbf{U}^T\mathbf{U}\right)\mathbf{\Phi} = \mathbf{\Phi}^T\mathbf{C}\mathbf{\Phi} = \mathbf{\Phi}^T\mathbf{\Phi}\mathbf{\Lambda} = \mathbf{\Lambda}$. So $\mathbf{a}_k^T\mathbf{a}_l = (m-1)\lambda_k\delta_{kl}$.

From $\mathbf{U} = \mathbf{A}\mathbf{\Phi}^T = \sum_k \mathbf{a}_k\mathbf{\phi}_k^T$, the error is $\mathbf{E} = \sum_{k > r}\mathbf{a}_k\mathbf{\phi}_k^T$. Therefore

```math
\|\mathbf{E}\|_F^2 = \text{tr}(\mathbf{E}^T\mathbf{E}) = \sum_{k,l > r}
(\mathbf{a}_k^T\mathbf{a}_l)(\mathbf{\phi}_l^T\mathbf{\phi}_k) = \sum_{k > r}\mathbf{a}_k^T\mathbf{a}_k = (m - 1)\sum_{k > r}\lambda_k
```

Check with Exercise 3: $\|\mathbf{U}\|_F^2 = 12 = 2(4.5 + 1.5)$. The rank-1 residual has squared norm $\|\mathbf{a}_2\|^2 = 3 = 2 \times 1.5$.

</details>

## References

- J. Weiss, "A Tutorial on the Proper Orthogonal Decomposition", *AIAA Aviation 2019 Forum*, Dallas, Texas, 2019. These notes follow the notation and turbulent separation bubble example of this tutorial.
- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987.
- P. Holmes, J. L. Lumley, G. Berkooz and C. W. Rowley, *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
- K. Taira, S. L. Brunton, S. T. M. Dawson, C. W. Rowley, T. Colonius, B. J. McKeon, O. T. Schmidt, S. Gordeyev, V. Theofilis and L. S. Ukeiley, "Modal analysis of fluid flows: An overview", *AIAA Journal* 55(12), 2017.
