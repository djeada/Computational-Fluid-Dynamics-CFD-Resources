## Introduction to Radial Basis Functions (RBF)

Radial Basis Functions (RBF) offer a flexible and powerful way to interpolate scattered data in multiple dimensions without requiring prior knowledge about the function’s underlying structure. Originally introduced for multivariate interpolation problems, RBF methods have since found broad applications in areas like image registration, surface reconstruction, and meshfree solutions of partial differential equations. By viewing the radial basis function approach as a single-layer artificial neural network (ANN), one gains insights into its adaptability and capability to approximate complex responses.

## The RBF Surrogate Model

The core idea behind RBF interpolation is to construct a surrogate model $\hat{y}(x)$ as a weighted sum of radially symmetric basis functions centered at the sample points $x^{(i)}$. Defining a suitable radial function $R: \mathbb{R}^d \to \mathbb{R}$ allows the model to capture nonlinear relationships, often outperforming simple polynomial regressions in complex settings.

A general RBF surrogate takes the form:

$$
\hat{y}(x): = \sum_{i=1}^{N} w_i R(\| x - x^{(i)} \|)
$$

where $\| \cdot \|$ is typically the Euclidean norm, and the centers $x^{(i)}$ correspond to the known sample locations. In principle, one could also choose different centers $c^{(i)}$ not coinciding with the sample points, but the standard approach sets centers equal to sample locations for simplicity.

## Interpolation Conditions and Solving for the Weights

To achieve an exact interpolation of the available data $(x^{(i)}, y(x^{(i)}))$, the surrogate must satisfy:

$$
\hat{y}(x^{(i)}) = y(x^{(i)}), \quad \text{for } i = 1,\ldots,N
$$

Substituting into the surrogate model yields a system of linear equations:

$$
\sum_{j=1}^{N} w_j R(\| x^{(i)} - x^{(j)} \|) = y_i, \quad i = 1,\ldots,N
$$

which can be written in matrix form as:

$$
R w = Y
$$

where:

$$
R: = [R(\| x^{(i)} - x^{(j)} \|)]_{i,j=1}^{N,N} \quad \text{and} \quad
w: = (w_1, \ldots, w_N)^T, \quad Y: = (y_1, \ldots, y_N)^T
$$

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

$$
\begin{array}{|c|c|}
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
\end{array}
$$

Using an RBF interpolation with, for instance, the polyharmonic spline $R(h) = h^3$, one can reconstruct a smooth curve passing exactly through these points. Even for more complex functions like $y(x) = (6x - 2)^2 \sin(12x - 4)$, an RBF interpolant using $R(h) = h^3$ can capture the nonlinear oscillations accurately, outperforming simple polynomial fits.

Visual Representation

![RBF Interpolation](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/fcd47b3f-f1f7-48d0-8406-559e46f120cc)

The figure shows an RBF interpolation using polyharmonic splines on a set of data. The resulting curve smoothly interpolates all sample points, highlighting how RBFs adapt to nonlinearity without requiring explicit knowledge of the underlying function form. In contrast to ordinary least squares approximations that might impose a fixed polynomial degree and fail to capture complex behaviors, RBF interpolation flexibly conforms to the data’s shape, providing accurate and smooth interpolations.

## Purpose in CFD

RBF interpolation provides a flexible, mesh-free surrogate that can handle scattered sample points in high-dimensional design spaces. This note defines the RBF model $\hat{y}(x) = \sum w_i R(\|x - x^{(i)}\|)$, catalogs common basis functions (Gaussian, multiquadric, inverse multiquadric, polyharmonic splines), discusses the scaling parameter and its effect, and explains how to solve for the weights. RBF surrogates are widely used for aerodynamic shape optimization and response-surface modeling in CFD.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Sample points $\{x^{(i)}\}_{i=1}^N$, observations $Y$, choice of radial function $R(\cdot)$, scaling parameter $c$ |
| **Outputs** | Weight vector $w = R^{-1}Y$, surrogate prediction $\hat{y}(x)$ at new points, interpolation system matrix $R$ |

## Related Scripts

- [Condition Number of the Correlation Matrix](../../../scripts/algorithms/condition_number_of_the_correlation_matrix/): plots how the condition number of a kriging correlation matrix changes with the correlation parameter $\theta$ for the linear, exponential, Gaussian and cubic spline correlation functions.
- [Kriging Interpolation](../../../scripts/algorithms/kriging_interpolation/): interpolates 11 samples of $y(x) = (3x-3)^2 \sin(2x-10)$ with a kriging-type predictor built on the cubic spline correlation function, for four values of the correlation parameter $\theta$.
- [Radial Basis Functions](../../../scripts/algorithms/radial_basis_functions/): fits a multiquadric radial basis function (RBF) interpolant through 11 data points on $[0, 1]$ using SciPy's `Rbf` class and plots it on a fine grid.

## Exercises

**Exercise 1.** Interpolate the data $(0, 1)$ and $(1, 2)$ with the Gaussian RBF $R(h) = \exp(-\kappa^2)$, $\kappa = \theta h$, $\theta = 1$. Compute the weights and $\hat{y}(0.5)$. What does the surrogate predict far from the data, and how can this be fixed?

<details>
<summary>Answer</summary>

$R = \begin{pmatrix} 1 & e^{-1} \\ e^{-1} & 1 \end{pmatrix}$ with $\det R = 1 - e^{-2} = 0.8647$. Then

$$
w = R^{-1}Y = \frac{1}{1 - e^{-2}}\begin{pmatrix} 1 - 2e^{-1} \\ 2 - e^{-1} \end{pmatrix} = \begin{pmatrix} 0.3056 \\ 1.8876 \end{pmatrix}
$$

and $\hat{y}(0.5) = e^{-0.25}(w_1 + w_2) = 0.7788 \times 2.1932 = 1.7080$. Far from the data every Gaussian decays, so $\hat{y} \to 0$. Adding a regression term $f(x)^T\beta$ (e.g. a constant or linear trend) gives sensible behaviour away from the samples.

</details>

**Exercise 2.** For six equally spaced points on $[0, 1]$ (spacing 0.2), compute the 2-norm condition number of the Gaussian RBF matrix for $\theta = 1$, $10$ and $100$. Discuss the trade-off in choosing $\theta$.

<details>
<summary>Answer</summary>

$\text{cond}(R) \approx 3.4 \times 10^6$ for $\theta = 1$, $1.07$ for $\theta = 10$, and $1.00$ for $\theta = 100$.

Small $\theta$ gives wide, nearly identical basis functions: the matrix is almost singular, but the interpolant is smooth. Large $\theta$ gives narrow bumps that barely overlap ($e^{-(10 \times 0.2)^2} = e^{-4} \approx 0.018$ between neighbours): the matrix is well conditioned, but the interpolant drops toward zero between samples. Good choices balance accuracy and conditioning, often by cross-validation.

</details>

**Exercise 3.** Interpolate the linear table of the example ($y = 2x$ at $x = 0, 0.2, \ldots, 1$) with the cubic RBF $R(h) = h^3$, first without and then with an appended linear polynomial, $\hat{y}(x) = \sum_i w_i|x - x^{(i)}|^3 + c_0 + c_1 x$ with side conditions $\sum_i w_i = 0$ and $\sum_i w_i x^{(i)} = 0$. Evaluate $\hat{y}(0.1)$ in both cases.

<details>
<summary>Answer</summary>

Without the polynomial, the weights are $w \approx (9.010, -15.179, 3.447, 1.392, -9.015, 4.216)$ and $\hat{y}(0.1) = 0.2421$ against the exact $0.2$, a 21% error, even though the data are linear.

With the polynomial, the augmented system

$$
\begin{pmatrix} R & P \\ P^T & 0 \end{pmatrix}\begin{pmatrix} w \\ c \end{pmatrix} = \begin{pmatrix} Y \\ 0 \end{pmatrix}, \qquad P = [\mathbf{1}, X]
$$

gives $w = 0$ and $(c_0, c_1) = (0, 2)$, so $\hat{y}(x) = 2x$ exactly and $\hat{y}(0.1) = 0.2$. The cubic RBF is only conditionally positive definite, so a low-degree polynomial tail is the standard way to guarantee solvability and to reproduce polynomial trends.

</details>

**Exercise 4.** Show that the Gaussian RBF matrix $R_{ij} = \exp(-\theta^2(x_i - x_j)^2)$ is positive definite for distinct points $x_1, \ldots, x_N \in \mathbb{R}$, so the interpolation system always has a unique solution. Use the Fourier representation $e^{-\theta^2 h^2} = \frac{1}{2\theta\sqrt{\pi}}\int_{-\infty}^{\infty} e^{-\omega^2/(4\theta^2)}\,e^{i\omega h}\,d\omega$.

<details>
<summary>Answer</summary>

For any real $w \ne 0$,

$$
w^T R w = \sum_{j,k} w_j w_k
e^{-\theta^2(x_j - x_k)^2} = \frac{1}{2\theta\sqrt{\pi}}\int_{-\infty}^{\infty}
e^{-\omega^2/(4\theta^2)}\left|\sum_j w_j e^{i\omega x_j}\right|^2 d\omega \ge 0
$$

The weight $e^{-\omega^2/(4\theta^2)}$ is strictly positive, so the integral vanishes only if $\sum_j w_j e^{i\omega x_j} = 0$ for all $\omega$. For distinct $x_j$ the exponentials are linearly independent, which forces $w = 0$. Hence $w^T R w > 0$ for all $w \ne 0$, and $R$ is nonsingular. The same argument (Bochner's theorem) holds in $\mathbb{R}^d$.

</details>

## References

- M. D. Buhmann, *Radial Basis Functions: Theory and Implementations*, Cambridge University Press, 2003.
- R. L. Hardy, "Multiquadric equations of topography and other irregular surfaces", *Journal of Geophysical Research* 76(8), 1971.
- C. A. Micchelli, "Interpolation of scattered data: distance matrices and conditionally positive definite functions", *Constructive Approximation* 2, 1986.
- G. E. Fasshauer, *Meshfree Approximation Methods with MATLAB*, World Scientific, 2007.
- A. I. J. Forrester, A. Sóbester and A. J. Keane, *Engineering Design via Surrogate Modelling: A Practical Guide*, Wiley, 2008.
