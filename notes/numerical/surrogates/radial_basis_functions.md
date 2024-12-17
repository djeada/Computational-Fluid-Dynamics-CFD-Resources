## Introduction to Radial Basis Functions (RBF)

Radial Basis Functions (RBF) offer a flexible and powerful way to interpolate scattered data in multiple dimensions without requiring prior knowledge about the function’s underlying structure. Originally introduced for multivariate interpolation problems, RBF methods have since found broad applications in areas like image registration, surface reconstruction, and meshfree solutions of partial differential equations. By viewing the radial basis function approach as a single-layer artificial neural network (ANN), one gains insights into its adaptability and capability to approximate complex responses.

## The RBF Surrogate Model

The core idea behind RBF interpolation is to construct a surrogate model $\hat{y}(x)$ as a weighted sum of radially symmetric basis functions centered at the sample points $x^{(i)}$. Defining a suitable radial function $R: \mathbb{R}^d \to \mathbb{R}$ allows the model to capture nonlinear relationships, often outperforming simple polynomial regressions in complex settings.

A general RBF surrogate takes the form:

$$\hat{y}(x) := \sum_{i=1}^{N} w_i R(\| x - x^{(i)} \|),$$
where $\| \cdot \|$ is typically the Euclidean norm, and the centers $x^{(i)}$ correspond to the known sample locations. In principle, one could also choose different centers $c^{(i)}$ not coinciding with the sample points, but the standard approach sets centers equal to sample locations for simplicity.

## Interpolation Conditions and Solving for the Weights

To achieve an exact interpolation of the available data $(x^{(i)}, y(x^{(i)}))$, the surrogate must satisfy:

$$\hat{y}(x^{(i)}) = y(x^{(i)}), \quad \text{for } i=1,\ldots,N.$$

Substituting into the surrogate model yields a system of linear equations:

$$\sum_{j=1}^{N} w_j R(\| x^{(i)} - x^{(j)} \|) = y_i, \quad i=1,\ldots,N,$$
which can be written in matrix form as:

$$R w = Y,$$
where:

$$R := [R(\| x^{(i)} - x^{(j)} \|)]_{i,j=1}^{N,N} \quad \text{and} \quad w := (w_1, \ldots, w_N)^T, \quad Y := (y_1, \ldots, y_N)^T.$$

Provided that $R$ is nonsingular, this system can be solved for the weights $w$. Nonsingularity typically requires distinct sample points $(x^{(i)} \neq x^{(j)} \text{ for } i \neq j)$.

## Types of Radial Basis Functions

RBF methods allow great flexibility through the choice of the radial function $R(h)$, where $h = \|x - x'\|$.

Some popular choices include:

I. Gaussian: $\displaystyle R(h) = \exp(-\kappa^2)$, where $\kappa = \theta h$. This function is infinitely differentiable and provides very smooth interpolants.

II. Inverse Multiquadric: $\displaystyle R(h) = (1 + \kappa^2)^{-1/2}$. This function tends to produce smooth interpolations while decaying more slowly than the Gaussian.

III. Multiquadric: $\displaystyle R(h) = (1 + \kappa^2)^{1/2}$. Known for its capability to handle scattered data but can lead to ill-conditioned systems if not scaled properly.

IV. Polyharmonic Splines: $\displaystyle R(h) = h^k \log(h)$ or $h^k$ for certain values of $k$. This class of functions is often used in surface reconstruction tasks and can produce stable, well-conditioned interpolations.

A key distinction is that some basis functions are local (e.g., Gaussian), tending to vanish as $h \to \infty$, while others are global (e.g., polyharmonic splines), growing unbounded with $h$. The choice between local and global RBFs often depends on problem size, data distribution, and desired interpolation properties.

## Enhancements and Extensions

RBF methods can be augmented in various ways to improve their performance and stability.

I. **Scaling Factor:**

Introducing a parameter $\theta > 0$ into the radial function as $R(h) = \tilde{R}(\theta h)$ tunes the spatial scaling of the RBF. Adjusting $\theta$ influences how quickly the function decays or grows and can greatly affect interpolation accuracy and stability.

II. **Regression Terms:**

To capture global trends that RBFs alone might miss, one can add a regression term $f(x)^T \beta$, where $f(x)$ might be a low-order polynomial. This creates a hybrid model that blends global polynomial trends with local RBF corrections, similar to Kriging’s trend plus correlation model.

III. **Approximation and Regularization:**

If computational resources are limited, using fewer basis functions than samples can lead to a least squares approximation approach. Additionally, adding a regularization term, such as $R + \epsilon I$, can handle noise and produce smoother approximations, mitigating overfitting.

## Suitability for Surrogate Modeling

While RBF interpolation does not require statistical assumptions, its strength comes from its flexibility and straightforward implementation. However, the assumption of radial symmetry might be overly simplistic for certain surrogate modeling tasks. If input parameters $x_k$ have varying sensitivities, a radial function that treats all directions uniformly might not capture anisotropic behavior well.

For such cases, more sophisticated methods like Kriging offer a built-in way to handle different length scales along each dimension. Alternatively, anisotropic scaling or using different norms could help adapt RBF methods to complex surrogate modeling scenarios.

## Example: One-Dimensional Illustration

Consider a set of data points:

$$\begin{array}{|c|c|}

\hline
x & y(x) \\

\hline

0.0 & 0.0 \\

0.2 & 0.4 \\

0.4 & 0.8 \\

0.6 & 1.2 \\

0.8 & 1.6 \\

1.0 & 2.0 \\

\hline

\end{array}$$

Using an RBF interpolation with, for instance, the polyharmonic spline $R(h) = h^3$, one can reconstruct a smooth curve passing exactly through these points. Even for more complex functions like $y(x) = (6x - 2)^2 \sin(12x - 4)$, an RBF interpolant using $R(h) = h^3$ can capture the nonlinear oscillations accurately, outperforming simple polynomial fits.

Visual Representation

![RBF Interpolation](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/fcd47b3f-f1f7-48d0-8406-559e46f120cc)

The figure shows an RBF interpolation using polyharmonic splines on a set of data. The resulting curve smoothly interpolates all sample points, highlighting how RBFs adapt to nonlinearity without requiring explicit knowledge of the underlying function form. In contrast to ordinary least squares approximations that might impose a fixed polynomial degree and fail to capture complex behaviors, RBF interpolation flexibly conforms to the data’s shape, providing accurate and smooth interpolations.
