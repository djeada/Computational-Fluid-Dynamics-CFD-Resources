# Gappy POD in Hilbert Spaces

Gappy Proper Orthogonal Decomposition (Gappy POD) is a variant of the standard Proper Orthogonal Decomposition (POD) technique, designed to reconstruct and approximate functions or fields from incomplete or partial data. While traditional POD relies on a complete set of snapshots, Gappy POD gracefully handles scenarios where data are missing, sparse, or corrupted. This makes Gappy POD particularly attractive in real-world situations such as experimental fluid dynamics measurements, sensor-limited data acquisition, or database-driven parametric studies where full-field information is not readily available.

## Background and Motivation

Classical POD identifies a set of orthonormal basis functions (modes) from a set of complete snapshots, typically collected from numerical simulations or experiments. The key step in POD involves projecting the system onto a reduced subspace that captures the most energetic or dominant structures. This approach enables the construction of reduced-order models (ROMs) that significantly reduce computational costs in simulations, while retaining essential dynamics.

However, in many practical scenarios—such as when sensors fail, data become partially inaccessible, or only a few measurements are available—traditional POD cannot be directly applied. Gappy POD extends the concept to handle "gappy" data: data sets where only subsets of the spatial domain or certain snapshots are known. By cleverly leveraging an existing basis derived from a "complete" reference dataset (or a suitable approximation), Gappy POD can fill in missing information and reconstruct the full field.

## Hilbert Space Setting

Both POD and Gappy POD are naturally formulated in Hilbert spaces. Consider a function space $L^2(\Omega)$, where $\Omega \subseteq \mathbb{R}^d$ is the spatial domain. A function $y(x)$, with $x \in \Omega$, belongs to $L^2(\Omega)$ if the integral of $|y(x)|^2$ over $\Omega$ is finite. This ensures an inner product and norm can be defined:

$$\langle f, g \rangle_{L^2(\Omega)} = \int_\Omega f(x) g(x) \, dx, \quad \|y\|_{L^2(\Omega)} = \sqrt{\langle y, y \rangle_{L^2(\Omega)}}.$$

POD typically seeks a low-dimensional subspace $\mathcal{Y}^L \subseteq L^2(\Omega)$ spanned by the first $L$ POD modes $\{\psi_j(x)\}_{j=1}^L$. These modes form an orthonormal basis in that subspace. Any function $y \in \mathcal{Y}^L$ can be approximated as:

$$y(x) \approx \hat{y}(x) = \sum_{j=1}^L a_j^{(y)} \psi_j(x),$$

where the coefficients $a_j^{(y)} = \langle y, \psi_j \rangle_{L^2(\Omega)}$ are determined by projecting $y$ onto each mode.

## Gappy POD: Plain Database Method

### Non-Gappy Function Approximation

If we have a complete description of $y \in L^2(\Omega)$, the best $L^2$-approximation in the subspace spanned by $\{\psi_j\}$ is obtained by minimizing:

$$\min_{\{a_j^{(y)}\}} \frac{1}{2}\|y(x) - \sum_{j=1}^L a_j^{(y)}\psi_j(x)\|_{L^2(\Omega)}^2.$$

The solution is straightforward:

$$a_j^{(y)} = \langle y, \psi_j \rangle_{L^2(\Omega)},$$

resulting in

$$\hat{y}(x) = \sum_{j=1}^L a_j^{(y)} \psi_j(x).$$

This assumes we have full knowledge of $y(x)$. In practice, especially in experimental settings or databases built from simulations at parameter sets, we often have only a set of discrete measurements $\{y(x^{(i)})\}_{i=1}^N$.

### Gappy Data Approximation

In Gappy POD, instead of minimizing over the entire domain $\Omega$, we only have partial information at sample points $x^{(i)}$, $i=1,\ldots,N$:

$$\min_{\{a_j^{(y)}\}} \frac{1}{2} \sum_{i=1}^N (y(x^{(i)}) - \sum_{j=1}^L a_j^{(y)} \psi_j(x^{(i)}))^2.$$

Define the "design matrix" $\Psi \in \mathbb{R}^{N \times L}$ as:

$$\Psi_{ij} = \psi_j(x^{(i)}).$$

We also have the vector $Y = [y(x^{(1)}), y(x^{(2)}), \ldots, y(x^{(N)})]^T \in \mathbb{R}^N$. The optimization problem becomes:

$$\min_{\Gamma_{a}^{(y)}} \frac{1}{2}\|Y - \Psi \Gamma_{a}^{(y)}\|_2^2,$$

where $\Gamma_{a}^{(y)} = [a_1^{(y)}, \ldots, a_L^{(y)}]^T$. Provided $\text{rank}(\Psi)=L$, the least-squares solution is:

$$\Gamma_{a}^{(y)} = (\Psi^T \Psi)^{-1} \Psi^T Y.$$

Thus, even with incomplete data, we recover the coefficients that best fit the data to the chosen POD basis. The reconstructed approximation is then:

$$\hat{y}(x) = \sum_{j=1}^L a_j^{(y)} \psi_j(x).$$

### Avoiding Redundancy and Database Functions

In many practical cases, the POD modes $\psi_j(x)$ come from a pre-computed database of solutions $\{\phi_j(x)\}_{j=1}^M$ that span a larger manifold $\mathcal{M} \subset L^2(\Omega)$. Using a singular value decomposition (SVD), we extract the dominant $L \le M$ modes to form a reduced basis $\psi_j(x)$. Then:

$$\Psi = \Phi V_L W_L^{-1},$$

where $\Phi \in \mathbb{R}^{N \times M}$ contains evaluations of the original database functions $\phi_j(x)$. This decomposition ensures that the Gappy POD approximation can leverage a well-structured database.

## Gappy POD: Aligned Database Method

In more complex scenarios, we may have to deal with databases where the underlying parameterization or geometry is not consistent or "aligned." For example, consider a shape optimization problem: different snapshots correspond to different geometries. The "aligned database method" applies a transformation to the function or the domain to align datasets.

I. **Transforming Database Elements**:

If each database element $\bar{\phi}(x)$ must be transformed according to some parameter $p$, we redefine:

$$\bar{\phi}(p) := \bar{\phi}(x(p)),$$

where $x(p)$ encodes scaling, translation, or more general transformations (e.g., from a parametric mapping $x \mapsto x(1+p_1)+p_2$). This allows the database to be "aligned," ensuring that different snapshots represent comparable features at corresponding locations.

II. **Approximation with Transformation**:

After alignment, we write:

$$\bar{y}(\bar{\phi}(p), p, a^{(y)}) = \bar{\phi}(\bar{\phi}(p)) V_L W_L^{-1} a^{(y)} + p_5,$$

ensuring that the function reconstruction accounts for geometric changes or parameter shifts in the dataset.

III. **Regularization**:

In presence of transformations and incomplete data, a regularization term $\frac{\delta}{2} p^T p$ can be introduced to stabilize the solution. The optimization problem becomes:

$$\min_{\Gamma_{a}^{(y)}, p} \left\{ \frac{1}{2}\sum_{i=1}^N (y(x^{(i)}) - \bar{y}(\bar{\phi}(p), p, a^{(y)}))^2 + \frac{\delta}{2} \|p\|_2^2 \right\}.$$

This ensures robustness against ill-conditioned problems and overfitting.

## Differences from Traditional POD in ROM Applications

### Purpose and Focus

- **Traditional POD**:  

The classical POD approach aims at reducing computational complexity by extracting a low-dimensional subspace that captures the dominant flow features. It is commonly used for Reduced-Order Modeling (ROM) in CFD, structural dynamics, acoustics, and more. The primary goal is to replace expensive full-scale simulations with cheaper reduced models, enabling rapid simulations, optimization, and control.

- **Gappy POD**:  

Gappy POD is not primarily about reducing computational costs in a fully known scenario. Instead, it focuses on reconstructing and identifying important underlying structures from incomplete or sparse data. While it can still facilitate model reduction (if a partial dataset is used to build or enhance a ROM), its defining characteristic is its ability to handle partial, gappy information.

### Data Requirements and Approaches

- **Traditional POD**:
- Data Source: Typically full-field snapshots obtained from simulations or experiments at different time steps or parameters.
- Complete Datasets: POD assumes data are complete, making computation of modes straightforward.
- **Gappy POD**:
- Data Source: Often partial or incomplete measurements—e.g., velocity data at a few sensor points, partial pressure distributions.
- Handling Gaps: Gappy POD reconstructs the missing data by leveraging a known basis (from a database of related solutions or previously computed modes).

### Applications

- **Traditional POD**:
- Used extensively in CFD to produce ROMs for fluid systems.
- Ideal for parametric studies, iterative design processes, and control applications when full datasets are available.
- **Gappy POD**:
- Suitable for situations where sensors provide only partial flow information.
- Can be used in data assimilation, where incomplete measurements (e.g., from sparse experimental probes) are combined with a known basis to recover full flow fields.
- Helps integrate measurement data into simulation-based frameworks to enhance accuracy and to fill in missing pieces of the puzzle.

## Example in CFD Context

**Scenario**: Suppose you are studying the aerodynamic performance of an airfoil. Using a Reynolds-Averaged Navier-Stokes (RANS) solver, you build a database of pressure and velocity fields at various angles of attack and Mach numbers. Traditional POD on this database yields a set of modes capturing the dominant flow features (e.g., shock waves, boundary-layer thickness variations, vortex structures).

Now, in an experimental wind tunnel test, you only have a handful of pressure sensors on the airfoil surface, missing the full field information. With Gappy POD, you use the modes derived from your complete CFD database and solve for the coefficients $a_j^{(y)}$ that best match the partial sensor readings. This approach reconstructs an estimate of the entire pressure field over the airfoil surface, enabling you to compare experiment with simulation and gain comprehensive insight.

## Advantages and Limitations

### Advantages of Gappy POD

- **Data Recovery**: Enables reconstruction of full fields from sparse data.
- **Flexibility**: Works with partial, incomplete, or noisy measurements, making it ideal in experimental or real-time sensing contexts.
- **Leverages Existing Knowledge**: Builds upon a known POD basis (e.g., from a precomputed database), thus integrating prior knowledge with new, limited observations.

### Limitations and Considerations

- **Quality of Basis**: The accuracy of Gappy POD reconstruction depends heavily on the richness and representativeness of the underlying POD basis. If the basis does not capture the needed structures, reconstruction quality suffers.
- **Conditioning and Stability**: The least-squares problem $\min \|Y - \Psi \Gamma_{a}^{(y)}\|$ can be ill-conditioned if the sampling points or available data are not chosen wisely. Regularization or sensor placement optimization may be needed.
- **Nonlinearity and Complexity**: For highly nonlinear problems or complex transformations (aligned database method), additional steps, such as nonlinear manifold learning or kernel methods, might be required.

## Future Directions and Research

Gappy POD continues to evolve as more sophisticated data assimilation, machine learning, and reduced-order modeling techniques emerge. Some promising avenues include:

I. **Integration with Machine Learning**:

Using neural networks or Gaussian processes to map partial measurements to POD coefficients can improve robustness and handle nonlinearity better.

II. **Adaptive Sampling and Sensor Placement**:

Determining optimal sensor locations or measurement strategies to maximize the accuracy of Gappy POD reconstructions.

III. **Nonlinear Extensions**:

Extending Gappy POD to nonlinear manifolds or using kernel POD or autoencoder-based approaches for enhanced reconstruction fidelity.

IV. **Data Assimilation in Complex Multiphysics Problems**:

Combining Gappy POD with advanced data assimilation frameworks (e.g., Ensemble Kalman Filters) to merge incomplete experimental or field data with high-fidelity simulations, improving model predictions and uncertainty quantification.
