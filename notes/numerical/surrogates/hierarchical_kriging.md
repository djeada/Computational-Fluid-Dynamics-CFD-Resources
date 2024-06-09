# Hierarchical Kriging

- Hierarchical Kriging extends a generic surrogate model from a least squares approximation to an interpolation method.
- Data points are extremely valuable due to the high computational cost of evaluations $y(x^{(i)})$.
- Aim: Surrogate model should be highly accurate, especially near $x^{(i)}$.
- Interpolation method, such as Kriging, is preferred over approximation.

## Variable-Fidelity Modeling (VFM)
- VFM improves approximation quality using limited high-fidelity data and more abundant low-fidelity data.
- High-fidelity data: Expensive, accurate computations (e.g., Navier-Stokes in CFD).
- Low-fidelity data: Cheaper, less accurate computations (e.g., Euler code).
- The generic surrogate model $\bar{y}$ is used as the low-fidelity model.

## VFM Frameworks
1. **CoKriging**:
   - Developed in geostatistics.
   - Relates primary and auxiliary variables through cross-correlation.

2. **Bridge Functions**:
   - Correct the discrepancy between low-fidelity and high-fidelity models.
   - Types: Additive, multiplicative, hybrid.

3. **Hierarchical Kriging**:
   - Recently introduced, robust method.
   - Extends Kriging method with minimal increase in computational complexity.

## Hierarchical Kriging Model
- In Kriging, replace regression term with the low-fidelity model $\bar{y}$:
  
$$
  y(x) = \bar{y} (\bar{\phi}(p), p, a) + z(x), \quad x \in \Omega \subset \mathbb{R}^d
  $$

- Hierarchical Kriging predictor:
  
$$
  \hat{y}(x) = \lambda(x)^T Y
  $$

  - Weighted sum of $Y = \{ y(x^{(1)}), \ldots, y(x^{(N)}) \}$.
- Weights $\lambda(x)$ determined by solving a linear equation:
  
$$
  \begin{pmatrix} R & F \\ F^T & 0 \end{pmatrix} \begin{pmatrix} \lambda(x) \\ \mu(x) \end{pmatrix} = \begin{pmatrix} r(x) \\ f(x) \end{pmatrix}
  $$

  - Minimizes mean squared error subject to unbiasedness constraint.
- Components:
  - $R$: Correlation matrix.
  - $r(x)$: Correlation vector.
  - $F$:
    
$$
    F := \left( \bar{y} (\bar{\phi}(p), p, a) \right)_{i=1}^N \in \mathbb{R}^N
    $$

  - $f(x)$:
    
$$
    f(x) := \bar{y} (\bar{\phi}(p), p, a) \in \mathbb{R}
    $$


## Predictor Formulation
- Closed form of hierarchical Kriging predictor:
  
$$
  \hat{y}(x) = \lambda(x)^T Y = \left( \begin{pmatrix} r(x)^T \\ f(x) \end{pmatrix}^T \begin{pmatrix} R & F \\ F^T & 0 \end{pmatrix}^{-1} \begin{pmatrix} Y \\ 0 \end{pmatrix} \right)
  $$

- Alternatively, with $\beta$:
  
$$
  \hat{y}(x) = \beta \bar{f}(x) + r(x)^T R^{-1} ( Y - \beta F)
  $$

  - $\beta = \left( F^T R^{-1} F \right)^{-1} F^T R^{-1} Y$

## Implementation
- Formulation (5.57) preferred for implementation:
  - $\beta$ does not need to be computed explicitly.
  - Linear system solution $\begin{pmatrix} R & F \\ F^T & 0 \end{pmatrix}^{-1} \begin{pmatrix} Y \\ 0 \end{pmatrix}$ computed once.
  - Ensures interpolation at $x^{(i)}$.

## Interpretation of Predictor
- When $\bar{y}$ approximates $y(x^{(i)})$ well, $\beta \approx 1$.
- Second summand: Weighted sum of correlation functions adjusts response towards exact evaluations $y(x^{(i)})$.
- Example:
  - Generic surrogate model $\bar{y}$ approximates data $Y$ well.
  - Hierarchical Kriging corrects discrepancies, ensuring accurate interpolation.
