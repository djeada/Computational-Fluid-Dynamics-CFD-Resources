# Proper Orthogonal Decomposition (POD)

This script implements Proper Orthogonal Decomposition (POD) on synthetic spatio-temporal flow data using Singular Value Decomposition (SVD). It extracts dominant spatial modes and their corresponding temporal coefficients to reveal the most energetically significant structures in a flow field.

## Mathematical Foundation

POD seeks an optimal low-dimensional basis for representing a dataset. Given a snapshot matrix $U \in \mathbb{R}^{N \times M}$ (where $N$ is the number of spatial points and $M$ is the number of time snapshots), POD is computed via the SVD:

$$U = \Phi \Sigma \Psi^T$$

where:
- $\Phi \in \mathbb{R}^{N \times M}$ — columns are the spatial modes (POD modes),
- $\Sigma \in \mathbb{R}^{M \times M}$ — diagonal matrix of singular values (related to the energy of each mode),
- $\Psi^T \in \mathbb{R}^{M \times M}$ — rows are the temporal coefficients.

The singular values $\sigma_i$ are ordered so that $\sigma_1 \geq \sigma_2 \geq \ldots \geq 0$. The first few modes capture the dominant structures and contain most of the energy.

### Data Preprocessing

Before computing the SVD, the data is mean-subtracted (centered):

$$\tilde{U} = U - \bar{U}$$

where $\bar{U}$ is the temporal mean. This ensures the decomposition captures fluctuations around the mean state.

## Implementation

1. **Synthetic Data Generation**: A 3D spatio-temporal field is generated using a combination of trigonometric functions over a grid in $x$, $y$, and $t$.
2. **Snapshot Matrix**: The 3D data array is reshaped into a 2D snapshot matrix of shape $(N_x \cdot N_y) \times N_t$.
3. **POD via SVD**: NumPy's `linalg.svd` decomposes the centered snapshot matrix to produce spatial modes and time coefficients.
4. **Visualization**: The first three spatial modes (reshaped to 2D) and their temporal coefficients are plotted side by side.

## Output

The script produces a figure with two columns:
- **Left column**: Filled contour plots of the first three POD spatial modes over the $(x, y)$ domain.
- **Right column**: Time series of the corresponding temporal coefficients $a_i(t)$.
