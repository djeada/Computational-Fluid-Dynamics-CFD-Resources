# Radial Basis Functions (RBF)

- Radial Basis Functions (RBF) are used for interpolating scattered data without prior information about the true response $y(x)$.
- Applications include multivariate interpolation, image registration, and meshfree solutions of PDEs.
- RBF can be interpreted as a single-layer artificial neural network (ANN).

## RBF Surrogate Model

### Definition
- The surrogate model is defined by:
  
$$
  \hat{y}(x) := \sum_{i=1}^{N} w_i R(||x - x^{(i)}||)
  $$

- $R : \mathbb{R}^d \rightarrow \mathbb{R}$ is a radially symmetric function.
- Centers of these functions coincide with samples $x^{(i)}$, but other centers $c^{(i)}$ are possible.
- Usually, the Euclidean distance $||.||_2$ is used.

### Interpolation Condition
- The interpolation condition is:
  
$$
  \hat{y}(x^{(i)}) = y_i \quad (i = 1, \ldots, N)
  $$

- This condition determines the unknowns $w_i$:
  
$$
  Rw = Y
  $$

- $R$ is an $N \times N$ matrix:
  
$$
  R := [R(||x^{(i)} - x^{(j)}||)]_{i,j=1}^{N,N}
  $$

- $R$ must be nonsingular, which excludes cases where $x^{(i)} = x^{(j)}$ for $i 
eq j$.

## Types of Radial Basis Functions

### Popular Choices
- **Gaussian:** $e^{-\kappa^2}$
- **Inverse Multiquadric:** $(1 + \kappa^2)^{-\frac{1}{2}}$
- **Multiquadric:** $(1 + \kappa^2)^{\frac{1}{2}}$
- **Polyharmonic Splines:** $\kappa^k$ or $\kappa^k \log h$

### Local vs. Global Basis Functions
- **Local Basis Functions:** Gaussian and inverse multiquadric ( $R(h) \rightarrow 0$ as $h \rightarrow \infty$ ).
- **Global Basis Functions:** Multiquadric and polyharmonic splines ( $R(h) \rightarrow \infty$ as $h \rightarrow \infty$ ).

## Enhancements to the Basic Method

### Scaling Factor
- $h$ can be replaced by $\theta h$ where $\theta > 0$.

### Regression Term
- An additional regression term $f(x)^T \beta$ (e.g., low-order polynomials) can be added to capture global trends.

### Approximation and Regularization
- Use fewer basis functions than samples and solve in a least squares sense.
- Regularize $R$ with $R + \epsilon I$ for noisy data, acting as a smoothing approximation.

## Considerations for Surrogate Modeling

- Radial basis functions interpolate observations without statistical assumptions.
- Radial assumption may be inappropriate for surrogate modeling due to varying sensitivity with respect to input parameters $x_k$.
- Alternative norms or methods like Kriging can handle different sensitivities.

## Example Data and Interpolation

### Example Data Points

$$
\begin{array}{|c|c|}
\hline
\text{x} & \text{y(x)} \\
\hline
0.0 & 0.0 \\
0.2 & 0.4 \\
0.4 & 0.8 \\
0.6 & 1.2 \\
0.8 & 1.6 \\
1.0 & 2.0 \\
\hline
\end{array}
$$


### RBF Interpolation

$$
\text{RBF interpolation } \hat{y}(x) \text{ using } R(h) = ||h||^3, y(x) = (6x - 2)^2 \sin(12x - 4)
$$


## Visual Representation
![RBF Interpolation](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/fcd47b3f-f1f7-48d0-8406-559e46f120cc)
- Figure 2.2 depicts an RBF interpolation of data using polyharmonic splines.
- RBF interpolation captures nonlinear behavior of the response accurately, unlike ordinary least squares approximation.
