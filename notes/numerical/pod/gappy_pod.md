# Gappy POD in Hilbert Spaces

- **Gappy POD**: Method for reconstructing functions from incomplete data.
- **Plain Database**: Approximating functions using available data pairs.
- **Aligned Database**: Transformation applied to the approximating function.
- **Difference from Traditional POD**: Focuses on identifying important structures rather than reducing numerical effort in simulations.

## Plain Database Method
- **Non-Gappy Function Approximation**: 
  - Approximating an arbitrary function $y \in L^2 (\Omega)$ using the POD basis:
    
$$
    a_j^{(y)} \min_{a_1^{(y)}, \ldots, a_L^{(y)} \in \mathbb{R}} \frac{1}{2} \left\| y(x) - \sum_{j=1}^L a_j^{(y)} \psi_j (x) \right\|_{L^2 (\Omega)}^2
    $$

  - Solution:
    
$$
    a_j^{(y)} = \langle y, \psi_j \rangle_{L^2 (\Omega)} \quad (j = 1, \ldots, L)
    $$

  - Approximating function:
    
$$
    \hat{y}(x) = \sum_{j=1}^L a_j^{(y)} \psi_j (x)
    $$

  - Projection of $y(x)$ onto subspace $\mathcal{Y}^L \subset \mathcal{M} \subset L^2 (\Omega)$.

- **Gappy Data Approximation**: 
  - Data pairs of evaluations:
    
$$
    \left\{ \left( x^{(i)}, y(x^{(i)}) \right) \right\}_{i=1}^N, \quad x^{(i)} \in \Omega \subset \mathbb{R}^d, \quad y(x^{(i)}) \in \mathbb{R}
    $$

  - Optimization problem:
    
$$
    a_j^{(y)} \min_{a_1^{(y)}, \ldots, a_L^{(y)} \in \mathbb{R}} \frac{1}{2} \sum_{i=1}^N \left( y(x^{(i)}) - \sum_{j=1}^L a_j^{(y)} \psi_j (x^{(i)}) \right)^2
    $$


- **Design Matrix $\Psi$**:
  
$$
  \Psi := \left[ \psi_j (x^{(i)}) \right]_{j=1, \ldots, L}^{i=1, \ldots, N} \in \mathbb{R}^{N \times L}, \quad N \geq L, \quad \text{rank} \Psi = L.
  $$

  - Solution:
    
$$
    \Psi \Gamma_{a}^{(y)} = \Psi^T Y
    $$


- **Avoiding Redundant Evaluations**:
  
$$
  \Phi := \left[ \phi_j (x^{(i)}) \right]_{i=1, \ldots, N}^{j=1, \ldots, M} \in \mathbb{R}^{N \times M}
  $$

  - Relation:
    
$$
    \Psi = \Phi V_L W_L^{-1}
    $$


- **Approximating Function**:
  
$$
  \hat{y}(x) = \sum_{j=1}^L a_j^{(y)} \psi_j (x)
  $$

  
$$
  = \psi (x) \Gamma_{a}^{(y)}
  $$

  
$$
  = \phi (x) V_L W_L^{-1} a^{(y)}
  $$

  
$$
  = \phi (x) \Gamma_{a}^{(\phi)}
  $$


## Aligned Database Method
- **Transforming Database Elements**:
  - Database elements transformed by solving the correspondence problem.
  - Transformation applied to approximating function $\hat{y}(x)$.

- **Cross-Validation Error**:
  
$$
  \bar{\phi}(p) := \begin{pmatrix} \bar{\phi}_1 (q^i)(1 + p_1) + p_2 \\ \bar{\phi}_2 (q^i)(1 + p_3) + p_4 \end{pmatrix}
  $$

  
$$
  = \begin{pmatrix} x_1 (1 + q_1^i) (1 + p_1) + p_2 \\ x_2 (1 + q_3^i) (1 + p_3) + p_4 \end{pmatrix}
  $$


- **Approximating Function with Transformation**:
  
$$
  \bar{y} (\bar{\phi}(p), p, a^{(y)}) := \bar{y} (\bar{\phi}(p), a^{(y)}) + p_5
  $$

  
$$
  = \bar{\phi} (\bar{\phi}(p), q) V_L W_L^{-1} a^{(y)} + p_5
  $$


- **Regularization Term**:
  
$$
  a^{(y)} \min_{\mathbb{R}^{K+5}} \left\{ \frac{1}{2} \sum_{i=1}^N \left( y(x^{(i)}) - \bar{y} (\bar{\phi}(p), p, a^{(y)}) \right)^2 + \frac{\delta}{2} p^T p \right\}.
  $$


## Application and Differences from Traditional POD

### Reduced-Order Modeling (ROM)
- **Purpose**: 
  - ROM is primarily used to reduce the computational complexity of solving large-scale problems in fluid dynamics and other fields.
  - It involves reducing the number of degrees of freedom in the system while maintaining the essential features of the original problem.

- **Traditional POD in ROM**:
  - **Snapshot Collection**:
    - Collect a set of snapshots representing the system's state at different time steps or parameter values.
    - For example, in CFD, these snapshots could be the velocity fields at various time instances.
  - **POD Basis Construction**:
    - Apply POD to these snapshots to construct an orthogonal basis.
    - The basis vectors (modes) capture the most energetic structures in the dataset.
  - **Dimensionality Reduction**:
    - Project the original high-dimensional data onto a lower-dimensional subspace spanned by the most significant POD modes.
    - This reduces the system's dimensionality, leading to a simplified model.
  - **Solving Reduced System**:
    - Solve the reduced-order model instead of the full system.
    - This significantly decreases computational time and resources while retaining accuracy.

- **Advantages**:
  - **Efficiency**: Greatly reduces computational costs.
  - **Accuracy**: Maintains the accuracy of the original high-dimensional model if the most important modes are captured.

### Gappy POD
- **Purpose**:
  - Gappy POD is designed to handle and reconstruct incomplete datasets.
  - It is particularly useful when only partial data is available, such as in situations with missing or corrupted measurements.

- **Application**:
  - **Identifying Important Data Structures**:
    - Gappy POD focuses on identifying and reconstructing the underlying structures of the data despite gaps.
    - This is crucial in applications where complete datasets are difficult to obtain.
  - **Database Functions**:
    - Unlike traditional POD, which uses snapshots collected over time or different parameter values, gappy POD utilizes database functions.
    - These functions are responses based on specific computational models, such as Reynolds-Averaged Navier-Stokes (RANS) computations for different airfoil geometries.

- **Example in CFD**:
  - In traditional POD, one might use velocity fields from different time steps of a simulation to create the basis.
  - In gappy POD, one might have velocity measurements only at certain points or times, and the method reconstructs the missing data by leveraging known structures from a database of similar solutions.

- **Advantages**:
  - **Handling Incomplete Data**: Capable of reconstructing missing parts of the data accurately.
  - **Flexibility**: Can be applied to various fields where incomplete data is common, not just CFD.

| Aspect                 | Traditional POD                                      | Gappy POD                                         |
|------------------------|------------------------------------------------------|--------------------------------------------------|
| **Purpose**            | Reduce computational complexity in solving large-scale problems | Handle and reconstruct incomplete datasets       |
| **Data Source**        | Complete datasets from time-dependent simulations or experiments | Incomplete datasets, using pre-computed database functions |
| **Basis Construction** | Uses snapshots representing the system's state at different time steps or parameter values | Uses responses from computational models, such as RANS for different geometries |
| **Focus**              | Reducing the number of degrees of freedom while maintaining essential features | Identifying and reconstructing important data structures despite gaps |
| **Application Scope**  | Scenarios with full data availability where computational efficiency is a concern | Scenarios with incomplete data where accurate reconstruction and data recovery are essential |
| **Typical Use Case**   | Fluid dynamics, structural analysis, and other large-scale system simulations | Situations with missing or corrupted measurements, such as partial experimental data |
| **Advantages**         | Significant reduction in computational time and resources; maintains accuracy with most important modes | Accurate reconstruction of missing data; flexible application in various fields with incomplete data |

