# Proper Orthogonal Decomposition in CFD

Proper Orthogonal Decomposition (POD), also known as Principal Component Analysis (PCA) in statistical contexts, is a mathematical tool widely used in computational fluid dynamics for model reduction, data compression, feature extraction, and flow analysis. By leveraging the intrinsic patterns in fluid flow fields, POD provides a systematic way to capture the most energetic structures within large datasets. The resulting low-dimensional representations are invaluable for simulation speedups, real-time control, optimization, and deeper physical insights.

## Introduction and Motivation

CFD simulations often generate high-dimensional data, such as velocity, pressure, temperature, and species concentration fields discretized across millions of spatial points and numerous time steps. Analyzing and using such massive datasets directly can be challenging, costly, and sometimes impractical. POD offers a framework to extract the essential "modes" or "patterns" that dominate the flow dynamics while filtering out less critical, higher-dimensional fluctuations.

By identifying a few dominant coherent structures, POD can reduce the complexity of the original PDE-based system from thousands or millions of degrees of freedom to just a handful of modes. This approach leads to Reduced-Order Models (ROMs) that retain the main physical phenomena but are much cheaper to evaluate. These ROMs are crucial in iterative tasks—such as optimization, parameter studies, sensitivity analysis, and uncertainty quantification—where running a full CFD simulation for each design or parameter set would be prohibitive.

## Theoretical Foundations of POD

### Link to Functional Analysis and Linear Algebra

At its core, POD is a technique from functional analysis and linear algebra that aims to find a set of orthonormal basis functions (modes) that optimally represent a given dataset in a least-squares sense. Given a set of snapshots (realizations of the system state), POD seeks a linear combination of orthonormal basis vectors that best approximates the data with minimal mean-squared error.

### Mathematical Formulation

**Step 1: Snapshot Acquisition**

Consider a fluid flow problem governed by the Navier-Stokes equations. Let $\mathbf{u}(x,t)$ be a vector field representing the flow state (e.g., velocity components) at spatial location $x \in \Omega$ and time $t$. We collect $N$ snapshots $`\{\mathbf{u}(x,t_i)\}_{i=1}^N`$ at discrete times $t_i$. These snapshots could be:

- Incompressible velocity fields $(u(x,t), v(x,t), w(x,t))$
- Pressure fields $p(x,t)$
- Temperature or scalar fields

For simplicity, assume each snapshot $\mathbf{u}(x,t_i)$ is reshaped into a column vector $\mathbf{u}_i \in \mathbb{R}^M$, where $M$ is the total number of spatial degrees of freedom (grid points times number of variables). Arrange these snapshots into a matrix $\mathbf{X} = [\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_N]$ of size $M \times N$.

**Step 2: Mean Subtraction (Optional)**

Often, we consider fluctuations around the mean flow. Let $\bar{\mathbf{u}}$ be the temporal mean:

$$
\bar{\mathbf{u}} = \frac{1}{N}\sum_{i=1}^N \mathbf{u}_i
$$

We may define $\mathbf{X}' = \mathbf{X} - \bar{\mathbf{u}}\mathbf{1}^T$, so each snapshot represents a fluctuation about the mean.

**Step 3: Correlation Matrix**

The correlation matrix $\mathbf{C}$ is defined as:

$$
\mathbf{C} = \frac{1}{N}\mathbf{X}'^T \mathbf{X}' \in \mathbb{R}^{N \times N}
$$

It encodes the covariance of the data. Alternatively, one could form $\mathbf{X}' \mathbf{X}'^T$ which is $M \times M$, but typically $N \ll M$, making the $N \times N$ formulation more computationally efficient (the so-called "snapshot POD").

**Step 4: Eigenvalue Decomposition**

Solve the eigenvalue problem:

$$
\mathbf{C}\mathbf{v}_i = \lambda_i \mathbf{v}_i
$$

where $\lambda_i$ are eigenvalues (sorted $\lambda_1 \geq \lambda_2 \geq \ldots \geq 0$) and $\mathbf{v}_i$ are eigenvectors. Each eigenvalue $\lambda_i$ represents the energy (variance) captured by the corresponding mode.

**Step 5: POD Modes**

The POD modes (spatial structures) $\boldsymbol{\Phi}_i \in \mathbb{R}^M$ are given by:

$$
\boldsymbol{\Phi}_i = \frac{1}{\sqrt{N\lambda_i}}\mathbf{X}'\mathbf{v}_i
$$

These modes form an orthonormal basis. They capture dominant flow patterns ranked by their importance (energy content).

**Step 6: Truncation**

Choose $r \ll N$ to keep only the top $r$ modes. The reduced basis:

$$
\boldsymbol{\Phi} = [\boldsymbol{\Phi}_1, \ldots, \boldsymbol{\Phi}_r]
$$

approximates snapshots as:

$$
\mathbf{u}_i \approx \bar{\mathbf{u}} + \sum_{j=1}^r a_{j}(t_i) \boldsymbol{\Phi}_j
$$

where $a_j(t_i)$ are the projection coefficients onto the $j$-th mode.

**Step 7: Reduced-Order Modeling**

If a PDE-based system (e.g., Navier-Stokes) governs the flow, one can project these equations onto the POD modes to derive a system of ordinary differential equations (ODEs) in the time-dependent coefficients $`\{a_j(t)\}`$. This yields a much lower-dimensional system, i.e., a Reduced-Order Model (ROM).

## Applications in CFD

I. **Flow Analysis and Data Compression**:

POD identifies coherent structures such as vortices, shear layers, or wakes. By focusing on a small number of modes, one can visualize and quantify the key patterns driving fluid dynamics. It also dramatically compresses storage needs.

II. **Reduced-Order Modeling for Rapid Simulations**:

Instead of solving full Navier-Stokes PDEs at every time step, use the ROM derived from POD modes. This can enable real-time simulations for control applications, rapid design iterations, and embedded systems (e.g., UAV flight control).

III. **Flow Control and Optimization**:

POD-based ROMs allow quick exploration of parameter spaces. For example, optimizing the shape of an airfoil for minimal drag under varying operating conditions can be done orders of magnitude faster using a POD-ROM instead of full CFD.

IV. **Uncertainty Quantification (UQ) and Sensitivity Studies**:

When exploring uncertainties in boundary conditions, material properties, or geometric parameters, POD-based ROMs allow thousands of runs for Monte Carlo or polynomial chaos expansions, which would be infeasible with full-scale CFD.

V. **Detection of Dominant Frequencies and Structures**:

Combining POD with temporal Fourier analysis or Dynamic Mode Decomposition (DMD) can distinguish between energetic structures and their characteristic frequencies. This is valuable in turbulence research and stability analysis.

## Comparison with Other Techniques

I. **POD vs. PCA in Statistics**:

POD and PCA are essentially the same technique, but in CFD, POD typically deals with vector fields and continuous domains. PCA often deals with tabular numerical data. Both find principal directions of maximum variance.

II. **POD vs. DMD (Dynamic Mode Decomposition)**:

While POD focuses on capturing the most energetic modes, DMD is interested in modes with distinct temporal frequencies and growth/decay rates. DMD can identify coherent structures associated with specific frequencies. POD does not directly yield temporal dynamics, only spatial modes and energy ranks.

III. **POD vs. Reduced Basis Methods (RBM)**:

Reduced Basis Methods (RBM) also reduce complexity by building a basis from selected "snapshots." POD is often used within RBM frameworks to identify the best basis from snapshot data. RBM might include additional constraints or optimizations for parametric PDE solutions.

IV. **POD vs. Proper Generalized Decomposition (PGD)**:

PGD constructs solution manifolds incrementally and can handle multidimensional parameter spaces effectively. POD is often applied a posteriori to data from simulations, while PGD aims at a more "intrinsic" decomposition approach.

## Best Practices and Practical Considerations

I. **Choice of Snapshots**:

- Ensure snapshots adequately represent the flow variability. Include multiple time instants, parameter variations, and operating conditions.
- Too few snapshots may lead to inaccurate mode representations. Too many snapshots increase computational cost.
  II. **Preprocessing**:
- Mean subtraction ensures focusing on fluctuations.
- Normalization or scaling may be necessary if variables have vastly different magnitudes.
  III. **Computational Efficiency**:
- For large-scale problems, directly handling $\mathbf{X}' \mathbf{X}'^T$ (size $M \times M$) is expensive. Use the snapshot formulation ($N \times N$) if $N < M$.
- Use efficient linear algebra libraries, parallel computing, and iterative solvers for eigenvalue problems.
  IV. **Mode Selection Criteria**:
- Retain modes corresponding to large eigenvalues until a certain energy threshold (e.g., 99% of energy) is captured.
- Overly aggressive truncation might lose crucial dynamics.
  V. **Stability and Robustness**:
- POD modes derived from a limited dataset might not generalize well outside that dataset’s parameter range.
- Regular updates or adaptive POD techniques can be used as the system evolves or if new conditions are introduced.

## Example: Vortex Shedding Around a Cylinder

**Scenario**: Simulate a 2D laminar flow past a circular cylinder at a Reynolds number of 100. The flow exhibits periodic vortex shedding, resulting in a well-known von Kármán vortex street.

I. **Snapshot Generation**:

Run a high-fidelity CFD simulation (e.g., finite volume method) and store velocity fields at $N=200$ time steps evenly spaced over a few shedding periods.

II. **POD Analysis**:

Form $\mathbf{X}$ from the stacked velocity fields. Subtract the mean flow. Compute the correlation matrix $\mathbf{C}$ and find its eigen-decomposition.

III. **Interpretation of Modes**:

The first few POD modes often represent symmetrical and anti-symmetrical vortex structures. The first mode might capture the largest-scale vortical pattern, the second mode the next significant spatial variation, and so forth.

IV. **Reduced-Order Model**:

Keep the top $r=10$ modes to represent 99% of the flow energy. Project Navier-Stokes equations onto these modes to obtain a ROM.

This ROM can simulate the dynamics of vortex shedding much faster than the original solver, enabling quick parametric studies or control law testing.

## Advanced Topics and Research Directions

I. **Time-Dependent Coefficients and Online Updating**:

Adaptive or online POD methods update modes as new data arrives, accommodating non-stationary flows.

II. **Nonlinear Model Reduction**:

POD is linear. For strongly nonlinear dynamics, techniques like Kernel PCA or manifold learning might better capture essential features. Neural network-based autoencoders also offer nonlinear dimension reduction.

III. **Parametric and Multi-Fidelity Extensions**:

Extend POD to handle variation in parameters (geometry, inflow conditions) by including multiple parameter slices in the snapshot set. Combine POD with Co-Kriging or Gaussian Processes to interpolate POD modes across parameter spaces.

IV. **Integration with Machine Learning (ML)**:

- Use ML-based regression to map parameters to POD coefficients, enabling parametric surrogate models.
- Employ deep learning to identify nonlinear embeddings that improve model accuracy over standard POD modes.

V. **POD for Turbulence Modeling**:

POD filters out noise and less energetic scales. Insights from POD modes can inform turbulence modeling, identify coherent structures in turbulent flows, and guide the development of reduced-order turbulence closures.

## Suggested Further Reading

I. **Books**:

- Holmes, P., Lumley, J.L., Berkooz, G., Rowley, C.W.: "Turbulence, Coherent Structures, Dynamical Systems, and Symmetry."
- Benner, P., Cohen, A., Ohlberger, M., Willcox, K. (eds.): "Model Reduction and Approximation: Theory and Algorithms."

II. **Seminal Research Papers**:

- Sirovich, L.: "Turbulence and the dynamics of coherent structures. Part I: Coherent structures." Quarterly of Applied Mathematics (1987).
- Berkooz, G., Holmes, P., Lumley, J.L.: "The proper orthogonal decomposition in the analysis of turbulent flows." Annual Review of Fluid Mechanics (1993).

III. **Contemporary Research**:

- Rowley, C.W., Dawson, S.T.M.: "Model reduction for flow analysis and control." Annual Review of Fluid Mechanics (2017) provides an overview of POD and related techniques.
- Taira, K. et al.: "Modal Analysis of Fluid Flows: An Overview." AIAA Journal (2017) discusses POD, DMD, and other modal decomposition methods.

## Purpose in CFD

POD is the foundational technique for Reduced-Order Modeling in CFD. By extracting the most energetic spatial modes from high-dimensional simulation data, POD compresses flow fields from millions of degrees of freedom to a handful of modes. The resulting Reduced-Order Model (ROM) can replace full Navier–Stokes solves in optimization, control, uncertainty quantification, and real-time applications.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Snapshot matrix $\mathbf{X} \in \mathbb{R}^{M \times N}$ (each column is a flow field at one time/parameter), number of retained modes $r$, energy threshold (e.g., 99%) |
| **Outputs** | POD modes $\boldsymbol{\Phi}_1, \dots, \boldsymbol{\Phi}_r$, eigenvalues $\lambda_i$ (energy per mode), temporal coefficients $a_j(t)$, reconstructed fields $\mathbf{u} \approx \bar{\mathbf{u}} + \sum a_j \boldsymbol{\Phi}_j$ |

## Related Scripts

- [Eigenvector Projection of Velocity Fluctuations](../../../scripts/plots/eigenvector_projection/): finds the principal directions of correlated 2D velocity fluctuations from the eigenvectors of their covariance matrix and projects the data onto them.
- [Image Compression Using SVD](../../../scripts/algorithms/image_compression_using_svd/): compresses a grayscale image by keeping only its $r$ largest singular values and the matching singular vectors, then compares the rank-$`r`$ reconstructions with the original.
- [POD Analysis for Flow Fields](../../../scripts/plots/pod_analysis_for_flow_fields/): performs Proper Orthogonal Decomposition (POD) on a synthetic 100 × 50 snapshot matrix with the singular value decomposition (SVD) and plots the eigenvalue spectrum with the share of turbulent kinetic energy (TKE) in each mode.
- [POD Modes of a Two-Point Velocity Signal](../../../scripts/plots/pod_modes_2d/): applies Proper Orthogonal Decomposition to velocity signals measured at two points, a and b, and plots how much each of the two POD modes contributes to each signal.
- [POD Spatial Modes and Temporal Coefficients](../../../scripts/plots/pod_modes_and_temporal_coefficients/): extracts the first three POD spatial modes and their temporal coefficients from a synthetic two-dimensional, time-dependent field and plots them.
- [Proper Orthogonal Decomposition (POD)](../../../scripts/algorithms/pod/): performs Proper Orthogonal Decomposition on a synthetic spatio-temporal field by taking the singular value decomposition of the mean-subtracted snapshot matrix.
- [Snapshot Proper Orthogonal Decomposition (Snapshot POD)](../../../scripts/algorithms/snapshot_pod/): computes POD modes of a synthetic spatio-temporal field with the snapshot method, which solves an eigenvalue problem for the $M \times M$ temporal correlation matrix instead of the much larger $N \times N$ spatial one.

## Exercises

**Exercise 1.** A snapshot set has POD eigenvalues $\lambda = (12, 6, 1.5, 0.3, 0.15, 0.05)$. How many modes $r$ are needed to capture at least 90% and at least 99% of the energy?

<details>
<summary>Answer</summary>

The total is $\sum_i \lambda_i = 20$. Cumulative fractions: $0.60, 0.90, 0.975, 0.99, 0.9975, 1.0$. So $r = 2$ reaches 90% and $r = 4$ reaches 99%.

</details>

**Exercise 2.** A 3D CFD case has $M = 10^6$ spatial degrees of freedom and $N = 200$ snapshots. Compare the double-precision storage of the $M \times M$ matrix $\mathbf{X}'\mathbf{X}'^T$ with that of the $N \times N$ correlation matrix $\mathbf{C}$.

<details>
<summary>Answer</summary>

$M \times M$: $10^{12} \times 8 = 8 \times 10^{12}$ bytes, i.e. 8 TB. $N \times N$: $200^2 \times 8 = 3.2 \times 10^5$ bytes, i.e. 320 kB. Only the snapshot formulation is feasible.

</details>

**Exercise 3.** Three snapshots of a field at $M = 3$ points are $\mathbf{u}_1 = (1, 2, 3)$, $\mathbf{u}_2 = (2, 2, 2)$ and $\mathbf{u}_3 = (3, 2, 1)$. Following Steps 2–6, compute $\bar{\mathbf{u}}$, $\mathbf{X}'$, $\mathbf{C}$, its nonzero eigenpair, the mode $\boldsymbol{\Phi}_1$ and the coefficients $a_1(t_i)$. Then reconstruct $\mathbf{u}_1$ from one mode.

<details>
<summary>Answer</summary>

$\bar{\mathbf{u}} = (2, 2, 2)$. The columns of $\mathbf{X}'$ are $(-1, 0, 1)$, $(0, 0, 0)$ and $(1, 0, -1)$, and

```math
\mathbf{C} = \frac{1}{3}\mathbf{X}'^T\mathbf{X}' = \frac{1}{3}\begin{pmatrix} 2 & 0 & -2 \\ 0 & 0 & 0 \\ -2 & 0 & 2 \end{pmatrix}
```

The only nonzero eigenvalue is $\lambda_1 = 4/3$, with $\mathbf{v}_1 = (1, 0, -1)/\sqrt{2}$. Then

```math
\boldsymbol{\Phi}_1 = \frac{\mathbf{X}'\mathbf{v}_1}{\sqrt{N\lambda_1}} = \frac{(-2, 0, 2)/\sqrt{2}}{2} = \frac{(-1, 0, 1)}{\sqrt{2}}
```

which has unit norm. The coefficients are $a_1(t_i) = \boldsymbol{\Phi}_1^T(\mathbf{u}_i - \bar{\mathbf{u}}) = (\sqrt{2}, 0, -\sqrt{2})$. The reconstruction $`\bar{\mathbf{u}} + \sqrt{2}\,\boldsymbol{\Phi}_1 = (2,2,2) + (-1,0,1) = (1,2,3) = \mathbf{u}_1`$ is exact, because one mode holds 100% of the fluctuation energy.

</details>

**Exercise 4.** Let $\mathbf{C}\mathbf{v}_i = \lambda_i\mathbf{v}_i$ with orthonormal $\mathbf{v}_i$ and $\lambda_i > 0$. Prove that the modes $\boldsymbol{\Phi}_i = \mathbf{X}'\mathbf{v}_i/\sqrt{N\lambda_i}$ are orthonormal, and that each $\boldsymbol{\Phi}_i$ is an eigenvector of the $M \times M$ matrix $\frac{1}{N}\mathbf{X}'\mathbf{X}'^T$ with the same eigenvalue.

<details>
<summary>Answer</summary>

```math
\boldsymbol{\Phi}_i^T\boldsymbol{\Phi}_j = \frac{\mathbf{v}_i^T\mathbf{X}'^T\mathbf{X}'\mathbf{v}_j}{N\sqrt{\lambda_i\lambda_j}} = \frac{\mathbf{v}_i^T\mathbf{C}\mathbf{v}_j}{\sqrt{\lambda_i\lambda_j}} = \frac{\lambda_j\,\mathbf{v}_i^T\mathbf{v}_j}{\sqrt{\lambda_i\lambda_j}} = \delta_{ij}
```

For the eigenvector property:

```math
\frac{1}{N}\mathbf{X}'\mathbf{X}'^T\boldsymbol{\Phi}_i = \frac{\mathbf{X}'(\mathbf{X}'^T\mathbf{X}'/N)\mathbf{v}_i}{\sqrt{N\lambda_i}} = \lambda_i \frac{\mathbf{X}'\mathbf{v}_i}{\sqrt{N\lambda_i}} = \lambda_i\boldsymbol{\Phi}_i
```

The $N \times N$ and $M \times M$ problems share their nonzero eigenvalues, which is why the snapshot method gives the same modes as the direct method.

</details>

## References

- P. Holmes, J. L. Lumley, G. Berkooz and C. W. Rowley, *Turbulence, Coherent Structures, Dynamical Systems and Symmetry*, 2nd ed., Cambridge University Press, 2012.
- L. Sirovich, "Turbulence and the dynamics of coherent structures. Part I: Coherent structures", *Quarterly of Applied Mathematics* 45(3), 1987.
- A. Chatterjee, "An introduction to the proper orthogonal decomposition", *Current Science* 78(7), 2000.
- S. L. Brunton and J. N. Kutz, *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*, Cambridge University Press, 2019.
