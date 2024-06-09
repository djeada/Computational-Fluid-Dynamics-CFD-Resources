# Derivation of POD in 2D

### Origins and Purpose
- POD originated in turbulence studies, introduced by Lumley in 1967.
- Objective: Decompose turbulent fluid motion into deterministic functions (POD modes) to understand flow organization.
- Goal: Identify coherent structures within turbulent flows.

### Basic Concept
- Fluctuating velocity in flow: $\mathbf{u}'(\mathbf{x}, t)$ (velocity vector $\mathbf{U}$ minus its temporal mean).
- Position vector: $\mathbf{x} = (x, y, z)$.
- Velocity vector: $\mathbf{U} = (U, V, W)$.
- Time: $t$.

### Decomposition
- POD decomposes $\mathbf{u}'(\mathbf{x}, t)$ into spatial functions $\mathbf{\Phi}_k(\mathbf{x})$ and time coefficients $a_k(t)$:


$$ \mathbf{u}'(\mathbf{x}, t) = \sum_{k=1}^{\infty} a_k(t) \mathbf{\Phi}_k(\mathbf{x}). $$


### Key Properties
- **Optimality**: The sequence $\sum_{k=1}^n a_k(t) \mathbf{\Phi}_k(\mathbf{x})$ captures maximum kinetic energy.
- **Orthonormality**: Modes $\mathbf{\Phi}_k(\mathbf{x})$ are orthonormal:


$$ \int_{\mathbf{x}} \mathbf{\Phi}_{k_1}(\mathbf{x}) \mathbf{\Phi}_{k_2}(\mathbf{x}) d\mathbf{x} = \begin{cases} 
1 & \text{if } k_1 = k_2 \\
0 & \text{if } k_1 
e k_2 
\end{cases}. $$


- **Time Coefficients**: Each $a_k(t)$ depends on $\mathbf{\Phi}_k(\mathbf{x})$:


$$ a_k(t) = \int_{\mathbf{x}} \mathbf{u}'(\mathbf{x}, t) \mathbf{\Phi}_k(\mathbf{x}) d\mathbf{x}. $$


### Relevance in Engineering
- Often introduced to students through Principal Component Analysis (PCA), suited to finite-dimensional data.
- POD is used in fluid mechanics and aerodynamics, targeting experimental and numerical finite-dimensional data.

## II. Example Flow: Turbulent Separation-Bubble (TSB)

### Flow Geometry
- Investigated using Particle Image Velocimetry (PIV).
- TSB forms due to adverse and favorable pressure gradients in a wind tunnel.
- PIV data: 200 mm $\times$ 80 mm rectangle, centered at $x =$ 1825 mm, $z =$ 0 mm.
- Data consists of 3580 vector fields, 129 $N_x$ $\times$ 45 $N_y$ velocity vectors ($U, V$).

### Data Analysis
- Focus on longitudinal velocity $U$.
- Example: Instantaneous contour plot of $U$ shows unsteady shear layer.
- Time-averaged velocity field: Average of PIV sequences.

## III. The 2-Dimensional Example

### Snapshot Matrix
- Analyze data at two positions within the separation bubble.
- Velocity data: Two arrays of $m = 3580$ longitudinal velocity values ($U_a(t_i)$ and $U_b(t_i)$).
- Concatenate into $m \times 2$ matrix $\mathbf{S}$ (matrix of snapshots).

### Steps to Implement POD
1. **Data Collection**: Gather velocity data from PIV measurements.
2. **Matrix Formation**: Form snapshot matrix $\mathbf{S}$.
3. **Covariance Matrix**: Compute the covariance matrix of $\mathbf{S}$.
4. **Eigenvalue Decomposition**: Perform eigenvalue decomposition on the covariance matrix.
5. **POD Modes**: Extract eigenvectors as POD modes.
6. **Time Coefficients**: Calculate time coefficients using the POD modes.

### Practical Considerations
- **Finite-dimensional Implementation**: Suitable for experimental and numerical data.
- **Visualization**: Contour plots to visualize velocity fields and modes.
- **Interpretation**: Analyze modes to understand flow structures.

![output(8)](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/de29d473-ec6c-4376-91a8-5653bb1b80ff)


$$ 
\mathbf{S} = 
\begin{pmatrix}
    U_a(t_1) & U_b(t_1) \\
    U_a(t_2) & U_b(t_2) \\
    \vdots & \vdots \\
    U_a(t_m) & U_b(t_m)
\end{pmatrix}. \quad (4) 
$$


### Removing Average Velocities
- To focus on flow dynamics, remove the average velocities $\overline{U}_a$ and $\overline{U}_b$ from their respective columns.
- This gives a new snapshot matrix $\mathbf{U}$ consisting of velocity fluctuations $u'_a(t) = U_a(t) - \overline{U}_a$ and $u'_b(t) = U_b(t) - \overline{U}_b$:


$$ 
\mathbf{U} = 
\begin{pmatrix}
    u_{11} & u_{12} \\
    u_{21} & u_{22} \\
    \vdots & \vdots \\
    u_{m1} & u_{m2}
\end{pmatrix} = 
\begin{pmatrix}
    u'_a(t_1) & u'_b(t_1) \\
    u'_a(t_2) & u'_b(t_2) \\
    \vdots & \vdots \\
    u'_a(t_m) & u'_b(t_m)
\end{pmatrix}. \quad (5) 
$$


### Visualizing Data
- The time traces of $u'_a$ and $u'_b$ show random turbulent signals, indicating some correlation due to proximity.
- On a 2D plot with $u'_a$ on the x-axis and $u'_b$ on the y-axis, the data points form an ellipse, showing correlation.

![Figure_1](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/8714451d-6864-40f3-9abd-c2e11ba4c9b8)

![Figure_2](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/75d6ea38-85f5-4fb8-896f-c4e684b5f890)

![Figure_3](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/b0e26fc6-7aaa-4b10-9d28-2d405197af2c)

### Covariance Matrix
- To quantify the correlation, compute the covariance matrix $\mathbf{C}$:


$$
\mathbf{C} = \frac{1}{m-1} \mathbf{U}^T \mathbf{U} = \frac{1}{m-1} 
\begin{pmatrix}
    \sum_{i=1}^{m} u'_a(t_i)^2 & \sum_{i=1}^{m} u'_a(t_i)u'_b(t_i) \\
    \sum_{i=1}^{m} u'_b(t_i)u'_a(t_i) & \sum_{i=1}^{m} u'_b(t_i)^2
\end{pmatrix}. \quad (6)
$$


- Diagonal elements: variances of $u'_a$ and $u'_b$.
- Off-diagonal elements: covariances between $u'_a$ and $u'_b$.
- Symmetric covariance matrix indicates correlation if off-diagonal terms are non-zero.

### Example Covariance Matrix
- For the given data:


$$
\mathbf{C} = 
\begin{pmatrix}
    c_{11} & c_{12} \\
    c_{21} & c_{22}
\end{pmatrix} = 
\begin{pmatrix}
    4.92 & 2.82 \\
    2.82 & 5.01
\end{pmatrix}. \quad (7)
$$


### Implications of Covariance Matrix
- Non-zero off-diagonal terms confirm statistical correlation between $u'_a$ and $u'_b$.
- Correlated velocity fluctuations suggest coherent structures in the flow.


### Correlation and Kinetic Energy

- **Correlation Coefficient**: Measures the degree of correlation between $u'_a$ and $u'_b$.
  
$$
  \rho_{ab} = \frac{c_{12}}{\sqrt{c_{11}c_{22}}} = 0.57
  $$

  - Indicates that $u'_a$ and $u'_b$ are fairly well correlated.

- **Total Fluctuating Kinetic Energy (TKE)**: Represents the kinetic energy of the velocity fluctuations.
  
$$
  \text{TKE} = \frac{1}{2} \frac{1}{m-1} \left( \sum_{i=1}^{m} u'_a(t_i)^2 + \sum_{i=1}^{m} u'_b(t_i)^2 \right) = \frac{1}{2} (c_{11} + c_{22}) = 4.96 \, \text{m}^2/\text{s}^2
  $$


### Variance and Modes of Variation

- **Natural Basis Variance**:
  - Variance of $u'_a$: $4.92 \, \text{m}^2/\text{s}^2$
  - Variance of $u'_b$: $5.01 \, \text{m}^2/\text{s}^2$
  - Statistical connection expressed as off-diagonal terms of $\mathbf{C}$.

- **Projection onto a Unit Vector**:
  - Any axis in the plane can define a mode of variation.
  - Project data onto a unit vector $\mathbf{\phi} = (\phi_1, \phi_2)$.
  - Compute dot product of each data point with $\mathbf{\phi}$:

  
$$
  \mathbf{a} = \mathbf{U} \mathbf{\phi} = 
  \begin{pmatrix}
      u_{11} & u_{12} \\
      u_{21} & u_{22} \\
      \vdots & \vdots \\
      u_{m1} & u_{m2}
  \end{pmatrix}
  \begin{pmatrix}
      \phi_1 \\
      \phi_2
  \end{pmatrix} = 
  \begin{pmatrix}
      a_1 = u_{11}\phi_1 + u_{12}\phi_2 \\
      a_2 = u_{21}\phi_1 + u_{22}\phi_2 \\
      \vdots \\
      a_m = u_{m1}\phi_1 + u_{m2}\phi_2
  \end{pmatrix}. \quad (9)
  $$


  - Result is an $m$-dimensional array $\mathbf{a}$ with coordinates $a_i$ projected on $\mathbf{\phi}$.

- **Variance in Any Direction**:
  - Compute variance along the direction $\mathbf{\phi}$:

  
$$
  \text{var}_{\mathbf{\phi}}(\mathbf{a}) = \frac{1}{m-1} \sum_{i=1}^{m} a_i^2 = \frac{1}{m-1} \mathbf{a}^T \mathbf{a}. \quad (10)
  $$


  - Example for unit vector $\mathbf{\phi} = \left( \frac{2}{\sqrt{5}}, \frac{1}{\sqrt{5}} \right)$:
    - Variance: $7.19 \, \text{m}^2/\text{s}^2$
    - Larger than variances on horizontal ($4.92 \, \text{m}^2/\text{s}^2$) or vertical ($5.01 \, \text{m}^2/\text{s}^2$) axes.

### Principal Axes and Modes
- **Infinite Variations**: Any direction $\mathbf{\phi}$ leads to new variance value.
- **Principal Axes**: Major and minor axes of the ellipse in the 2D plot.
  - **Major Axis**: Direction of maximum variance.
  - **Minor Axis**: Orthogonal to the major axis, represents remaining variance.
  - These axes form an orthonormal basis, called the principal axes or proper orthogonal modes of the dataset.


### Computing Principal Axes

- **Eigenvectors of Covariance Matrix**:
  - Directions of major and minor axes are eigenvectors of the covariance matrix $\mathbf{C}$.
  - Intuitively: In the proper orthogonal basis, variance is maximized on each axis, making covariance between axes zero (diagonal covariance matrix).

![Data with Eigenvectors](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/2880d4e4-45ae-4f5b-a713-69cdcb7d675a)

- **Symmetric Covariance Matrix**:
  - $\mathbf{C}$ is symmetric, so its eigenvectors form an orthonormal basis.
  - Covariance matrix $\mathbf{C}$ can be diagonalized using its eigenvectors:
  
  
$$
  \mathbf{C} = \mathbf{\Phi} \mathbf{\Lambda} \mathbf{\Phi}^{-1} = \mathbf{\Phi} \mathbf{\Lambda} \mathbf{\Phi}^T 
  = \begin{pmatrix}
      \phi_{11} & \phi_{12} \\
      \phi_{21} & \phi_{22}
  \end{pmatrix}
  \begin{pmatrix}
      \lambda_1 & 0 \\
      0 & \lambda_2
  \end{pmatrix}
  \begin{pmatrix}
      \phi_{11} & \phi_{12} \\
      \phi_{21} & \phi_{22}
  \end{pmatrix}^T, \quad (11)
  $$


- **Eigenvector Computation**:
  - In MATLAB: `[PHI LAM] = eig(C)`
  - Order eigenvalues from largest to smallest.
  - First eigenvector corresponds to the largest eigenvalue, representing the major axis.
  - Second eigenvector corresponds to the smallest eigenvalue, representing the minor axis.
  - Eigenvalues relate to the variance along their respective eigenvectors (principal axes).

![Principal Axes Directions](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/c955eeb5-d045-47c4-94e6-1146171edee1)

- **Projection onto Principal Axes**:
  - Project data onto each eigenvector to compute variance along principal axes:

  
$$
  \mathbf{A} = \mathbf{U} \mathbf{\Phi} = 
  \begin{pmatrix}
      u_{11} & u_{12} \\
      u_{21} & u_{22} \\
      \vdots & \vdots \\
      u_{m1} & u_{m2}
  \end{pmatrix}
  \begin{pmatrix}
      \phi_{11} & \phi_{12} \\
      \phi_{21} & \phi_{22}
  \end{pmatrix}. \quad (12)
  $$


- **Variance on Principal Axes**:
  - Major axis variance: $\lambda_1$
  - Minor axis variance: $\lambda_2$
  - Diagonal matrix $\mathbf{\Lambda}$ represents variances in the principal orthogonal basis:

  
$$
  \mathbf{C'} = \frac{1}{m-1} \mathbf{A}^T \mathbf{A} = \frac{1}{m-1} (\mathbf{U} \mathbf{\Phi})^T (\mathbf{U} \mathbf{\Phi}) = \mathbf{\Lambda}. \quad (13)
  $$


### Significance of Eigenvectors

- **Correlation and Eigenvectors**:
  - Eigenvectors indicate how $u'_a$ and $u'_b$ are correlated.
  - In the proper orthogonal basis, $u'_a$ and $u'_b$ are uncorrelated, and their correlation is implicit in the directions of the eigenvectors.
  - Projected variables ($a_{i1}$ and $a_{i2}$) are uncorrelated and represent independent modes of fluctuation.

- **Proper Orthogonal Modes**:
  - Modes correspond to independent coherent structures in the flow.
  - **Example Directions**:
    - $(\sqrt{2}/2, \sqrt{2}/2)$: $u'_a$ and $u'_b$ move in phase with the same amplitude (first mode).
    - $(1,0)$: $u'_a$ fluctuates independently of $u'_b$ (natural basis).
    - $(\sqrt{2}/2, -\sqrt{2}/2)$: $u'_a$ and $u'_b$ fluctuate in opposition (second mode).

### Eigenvalues and Kinetic Energy

- **Eigenvalues and Correlation**:
  - Eigenvalues rank the correlation with respect to the variance (or kinetic energy) of the velocity fluctuations.
  - For the given data:
    - $\lambda_1 = 7.78 \, \text{m}^2/\text{s}^2$
    - $\lambda_2 = 2.15 \, \text{m}^2/\text{s}^2$
  - Total Kinetic Energy (TKE) is:
    
$$
    \text{TKE} = \frac{1}{2} (\lambda_1 + \lambda_2) = 4.96 \, \text{m}^2/\text{s}^2
    $$


- **Proportion of TKE by Each Mode**:
  - Mode 1: $\lambda_1/(\lambda_1 + \lambda_2) \approx 0.78$ (78% of TKE)
  - Mode 2: $\lambda_2/(\lambda_1 + \lambda_2) \approx 0.22$ (22% of TKE)

### Interpretation of Modes

- **First Mode**:
  - Oriented at roughly 45°, indicating a strong correlation between $u'_a$ and $u'_b$.
  - Accounts for 78% of the TKE, indicating significant in-phase fluctuations.

- **Second Mode**:
  - Represents a smaller portion (22%) of TKE.
  - Indicates out-of-phase fluctuations between $u'_a$ and $u'_b$.

### Summary of Steps

1. **Matrix of Snapshots**:
   - Start with the original matrix $\mathbf{S}$ and remove its mean to obtain $\mathbf{U}$.
   - $\mathbf{U}$ represents the velocity fluctuations.

2. **Covariance Matrix**:
   - Compute the covariance matrix $\mathbf{C} = \frac{1}{m-1} \mathbf{U}^T \mathbf{U}$.

3. **Eigenvectors and Eigenvalues**:
   - Obtain the matrix of eigenvectors $\mathbf{\Phi}$ and eigenvalues $\mathbf{\Lambda}$.

4. **Projection onto Eigenvectors**:
   - Project $\mathbf{U}$ onto each eigenvector to obtain $\mathbf{A} = \mathbf{U} \mathbf{\Phi}$.

5. **Reconstruction**:
   - Use the orthogonal property of $\mathbf{\Phi}$ to write $\mathbf{U}$ in terms of $\mathbf{A}$:

   
$$
   \mathbf{A} = \mathbf{U} \mathbf{\Phi} \Rightarrow \mathbf{U} = \mathbf{A} \mathbf{\Phi}^{-1} = \mathbf{A} \mathbf{\Phi}^T
   $$


### Detailed Reconstruction

- **Reconstruction of $\mathbf{U}$**:


$$
\mathbf{U} = \begin{pmatrix}
    u_{11} & u_{12} \\
    u_{21} & u_{22} \\
    \vdots & \vdots \\
    u_{m1} & u_{m2}
\end{pmatrix} = 
\begin{pmatrix}
    a_{11} & a_{12} \\
    a_{21} & a_{22} \\
    \vdots & \vdots \\
    a_{m1} & a_{m2}
\end{pmatrix}
\begin{pmatrix}
    \phi_{11} & \phi_{21} \\
    \phi_{12} & \phi_{22}
\end{pmatrix}
$$



$$
= 
\begin{pmatrix}
    a_{11} \phi_{11} + a_{12} \phi_{12} & a_{11} \phi_{21} + a_{12} \phi_{22} \\
    a_{21} \phi_{11} + a_{22} \phi_{12} & a_{21} \phi_{21} + a_{22} \phi_{22} \\
    \vdots & \vdots \\
    a_{m1} \phi_{11} + a_{m2} \phi_{12} & a_{m1} \phi_{21} + a_{m2} \phi_{22}
\end{pmatrix}
$$



$$
= 
\begin{pmatrix}
    a_{11} \phi_{11} & a_{11} \phi_{21} \\
    a_{21} \phi_{11} & a_{21} \phi_{21} \\
    \vdots & \vdots \\
    a_{m1} \phi_{11} & a_{m1} \phi_{21}
\end{pmatrix}
+
\begin{pmatrix}
    a_{12} \phi_{12} & a_{12} \phi_{22} \\
    a_{22} \phi_{12} & a_{22} \phi_{22} \\
    \vdots & \vdots \\
    a_{m2} \phi_{12} & a_{m2} \phi_{22}
\end{pmatrix}
$$



$$
= 
\begin{pmatrix}
    a_{11} \\
    a_{21} \\
    \vdots \\
    a_{m1}
\end{pmatrix}
\begin{pmatrix}
    \phi_{11} & \phi_{21}
\end{pmatrix}
+
\begin{pmatrix}
    a_{12} \\
    a_{22} \\
    \vdots \\
    a_{m2}
\end{pmatrix}
\begin{pmatrix}
    \phi_{12} & \phi_{22}
\end{pmatrix}
$$



$$
= \mathbf{\tilde{U}}^1 + \mathbf{\tilde{U}}^2
$$


### Decomposition into Proper Orthogonal Modes

- **Definition of Components**:
  - For $k = 1, 2$:
  
$$
  \mathbf{\tilde{U}}^k = 
  \begin{pmatrix}
      \tilde{u}^k_{11} & \tilde{u}^k_{12} \\
      \tilde{u}^k_{21} & \tilde{u}^k_{22} \\
      \vdots & \vdots \\
      \tilde{u}^k_{m1} & \tilde{u}^k_{m2}
  \end{pmatrix}
  = 
  \begin{pmatrix}
      a_{1k} \\
      a_{2k} \\
      \vdots \\
      a_{mk}
  \end{pmatrix}
  \begin{pmatrix}
      \phi_{1k} & \phi_{2k}
  \end{pmatrix}. \quad (16)
  $$


- **Interpretation of Decomposition**:
  - Original matrix $\mathbf{U}$ can be expressed as the sum of:
    - $\mathbf{\tilde{U}}^1$: Data projected onto the major axis, expressed in the natural basis.
    - $\mathbf{\tilde{U}}^2$: Data projected onto the minor axis, expressed in the natural basis.
  - This means the original velocity fluctuations are decomposed into contributions from the first mode ($\mathbf{\tilde{U}}^1$) and the second mode ($\mathbf{\tilde{U}}^2$).

### Geometric Interpretation

- **Projection Illustration**:
  - Projections involved in the decomposition are illustrated in the geometric interpretation (refer to Fig. 9).

### Simplification through Dominant Mode

- **Dominance of First Mode**:
  - The first mode ($\mathbf{\tilde{U}}^1$) is largely dominant compared to the second mode ($\mathbf{\tilde{U}}^2$).
  - Simplify data analysis by focusing only on the first mode, neglecting the second mode.

- **Approximation**:
  - The first mode provides a good approximation of the total fluctuations.
  - $\mathbf{U}$ can be approximated by $\mathbf{\tilde{U}}^1$.
  - Approximately 78% of the TKE is explained by the first mode.

### Dimensionality Reduction

- **Concept**:
  - Dimensionality reduction is a key feature of POD.
  - In higher dimensions ($n$), this feature becomes extremely useful.
  - Simplifies analysis by reducing the number of modes considered while retaining most of the important information.

## Refrences

These notes are inspired by Julien Weiss's "A Tutorial on the Proper Orthogonal Decomposition," presented at the 2019 AIAA Aviation Forum in Dallas, Texas.
