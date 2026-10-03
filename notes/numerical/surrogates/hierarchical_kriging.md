## Introduction to Hierarchical Kriging

Hierarchical Kriging is an advanced surrogate modeling technique designed to enhance the accuracy of predictions, especially near known sample points $x^{(i)}$. In many engineering and scientific applications, evaluating the response function $y(x)$ at sample points can be computationally expensive, so each data point is extremely valuable. The ultimate goal is to build a surrogate model that reproduces these data points exactly, eliminating approximation errors at known samples and ensuring a highly accurate interpolation scheme. By leveraging a low-fidelity model $\bar{y}(x)$ as part of the Kriging framework, Hierarchical Kriging refines predictions and achieves interpolation-level accuracy.

## Variable-Fidelity Modeling (VFM)

In the context of Variable-Fidelity Modeling, engineers often have access to two sets of data: a small number of high-fidelity evaluations $y(x)$, which are expensive but accurate, and a larger quantity of low-fidelity evaluations $\bar{y}(x)$, which are cheaper but less accurate approximations. For instance, high-fidelity data might come from a Navier-Stokes solver in computational fluid dynamics (CFD), while the low-fidelity data might come from a simpler Euler solver. VFM methods aim to combine both data types to produce a surrogate that is more accurate than any single-fidelity model could achieve alone.

The generic surrogate model $\bar{y}$ is interpreted as the low-fidelity model, capturing large-scale trends of the response at a reduced computational cost. Hierarchical Kriging takes this idea a step further by embedding the low-fidelity model directly into the Kriging framework, reducing the surrogate’s complexity while increasing its interpolation accuracy.

## Established VFM Frameworks

Several methods have been developed to harness variable-fidelity data:

I. **CoKriging**: Originating in geostatistics, CoKriging models high-fidelity and low-fidelity data jointly through cross-correlation structures. It can efficiently fuse both data sources but may become complex in terms of model building and parameter estimation.

II. **Bridge Functions**: These approaches define a correction function between the low- and high-fidelity data. Depending on the application, the correction can be additive, multiplicative, or a hybrid form. By applying this correction to the low-fidelity model, one can refine it into a more accurate surrogate.

III. **Hierarchical Kriging**: This newer approach integrates the low-fidelity model within the Kriging predictor, turning a simple least squares approximation into a full interpolation scheme. It provides robustness and maintains a relatively simple computational structure, making it appealing for complex modeling problems.

## Hierarchical Kriging Model Formulation

Hierarchical Kriging modifies the standard Kriging model by replacing the linear regression (trend) terms $f(x) \beta$ with the low-fidelity model $\bar{y}(\bar{\phi}(p), p, a)$. Here, $\bar{y}$ represents the low-fidelity approximation of the response, which may depend on parameters $p$ and auxiliary variables $\bar{\phi}(p)$ that help map input parameters to the low-fidelity model space. In the presence of these terms, the Hierarchical Kriging model is expressed as:

$$
y(x) = \bar{y}(\bar{\phi}(p), p, a) + z(x), \quad x \in \Omega \subset \mathbb{R}^d
$$

The term $z(x)$ represents a zero-mean Gaussian process used to model the deviation from $\bar{y}(x)$. In classical Kriging, the deterministic part is often a linear trend $f(x)^T \beta$. By using $\bar{y}(x)$ instead, one incorporates prior knowledge or a simpler model directly, improving efficiency and accuracy.

## Hierarchical Kriging Predictor

As in standard Kriging, the predictor $\hat{y}(x)$ at an arbitrary point $x$ is a weighted linear combination of the known responses $Y = \{ y(x^{(1)}), \dots, y(x^{(N)}) \}$:

$$
\hat{y}(x) = \lambda(x)^T Y
$$

where $\lambda(x) \in \mathbb{R}^N$ is a vector of weights determined by solving a linear system that ensures both unbiasedness and minimal mean squared error. To achieve unbiasedness, one imposes constraints involving $\bar{y}(x)$ at the sample points.

Define the correlation matrix $R \in \mathbb{R}^{N \times N}$ from the Gaussian process assumption, and a vector $r(x) \in \mathbb{R}^N$ of correlations between $x$ and the sample points $X = \{x^{(i)}\}$. With Hierarchical Kriging, the role of the regression matrix $F \in \mathbb{R}^{N}$ (which in standard Kriging corresponds to the regression functions evaluated at sample points) is taken by:

$$
F: = \bigl(\bar{y}(\bar{\phi}(p), p, a) \bigr)_{i=1}^N \in \mathbb{R}^N
$$

Similarly, for the point $x$, we define:

$$
f(x): = \bar{y}(\bar{\phi}(p), p, a)
$$

The Kriging system, ensuring optimal weights, is:

$$
\begin{pmatrix}
R & F \\ F^T & 0
\end{pmatrix}
\begin{pmatrix}
\lambda(x) \\ \mu(x)
\end{pmatrix} =
\begin{pmatrix}
r(x) \\ f(x)
\end{pmatrix}
$$

Solving this system yields $\lambda(x)$ and $\mu(x)$, which in turn gives the prediction $\hat{y}(x) = \lambda(x)^T Y$.

## Closed-Form Predictor and Interpretation

Using matrix operations, one can write the Hierarchical Kriging predictor in a compact form:

$$
\hat{y}(x) =
\begin{pmatrix}
r(x)^T & f(x)
\end{pmatrix}
\begin{pmatrix}
R & F \\ F^T & 0
\end{pmatrix}^{-1}
\begin{pmatrix}
Y \\ 0
\end{pmatrix}
$$

Alternatively, if we define:

$$
\beta: = (F^T R^{-1} F)^{-1} F^T R^{-1} Y
$$

we can express the predictor as:

$$
\hat{y}(x) = f(x) \beta + r(x)^T R^{-1}(Y - F \beta)
$$

This form mirrors the structure of standard Kriging but replaces the regression term with the low-fidelity model $\bar{y}$. The coefficient $\beta$ adjusts the scale of the low-fidelity model so that the combined model $f(x)\beta$ fits the global trend suggested by $Y$. The term $r(x)^T R^{-1}(Y - F \beta)$ ensures that the model interpolates the data exactly, applying local corrections based on the correlation structure.

## Practical Implementation

In practice, the preferred formulation for implementation is the block matrix inversion form. Rather than explicitly computing $\beta$, one solves:

$$
\begin{pmatrix}
R & F \\ F^T & 0
\end{pmatrix}
\begin{pmatrix}
w^{(Y)} \\ w^{(f)}
\end{pmatrix} =
\begin{pmatrix}
Y \\ 0
\end{pmatrix}
$$

where $\begin{pmatrix} w^{(Y)} \\ w^{(f)} \end{pmatrix}$ is independent of $x$ and can be solved once and stored. The predictor evaluation at a new point $x$ then involves computing $(r(x), f(x))$ and taking their dot product with the stored solution. This method is computationally efficient and maintains the exact interpolation property.

## Interpreting the Correction Terms

When the low-fidelity model $\bar{y}(x)$ closely approximates the high-fidelity response $y(x^{(i)})$ at sample points, the coefficient $\beta$ will approach unity. This means that the low-fidelity model is already a good predictor of $Y$, and only minor corrections are needed from the correlation terms. On the other hand, if $\bar{y}$ is less accurate, the correlation-based correction will have a more substantial role, pulling the predictions towards the exact known data points and ensuring an interpolation that corrects any discrepancies.

## Example Scenarios

I. **Accurate Low-Fidelity Model**: Suppose $\bar{y}(x)$ is a near-perfect approximation. Then $\hat{y}(x)$ will differ from $\bar{y}(x)$ only by a small, smooth correction, ensuring exact interpolation without much alteration of the global trend.

II. **Coarse Low-Fidelity Model**: If $\bar{y}(x)$ is only a rough approximation, the correlation corrections $r(x)^T R^{-1}(Y - F \beta)$ will dominate, refining the surrogate especially near known samples and gradually bending $\bar{y}(x)$ towards the observed data $Y$.

In either scenario, Hierarchical Kriging ensures that the final model honors the data points exactly, overcoming the limitations of pure least squares approximations and benefiting from the global trend captured by the low-fidelity model.

## Purpose in CFD

High-fidelity CFD is expensive, but cheaper low-fidelity models (coarser meshes, simpler physics) are often available. Hierarchical Kriging fuses low-fidelity and high-fidelity data into a single surrogate, improving prediction accuracy without requiring many expensive runs. This note formulates the hierarchical Kriging predictor, shows how the low-fidelity trend replaces the polynomial regression term, and discusses practical implementation.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Low-fidelity model $\hat{y}_c(x)$, high-fidelity samples $\{(x^{(i)}, y^{(i)})\}$, correlation function $R(\cdot)$, hyperparameters |
| **Outputs** | Hierarchical Kriging predictor $\hat{y}(x)$ combining low- and high-fidelity information, mean squared error, optimized hyperparameters |

## Related Scripts

- [Correlation Functions](../../../scripts/algorithms/correlation_functions/): plots four correlation functions used in kriging surrogate models (linear, exponential, Gaussian and cubic spline) for several values of the correlation parameter $\theta$.
- [Kriging Interpolation](../../../scripts/algorithms/kriging_interpolation/): interpolates 11 samples of $y(x) = (3x-3)^2 \sin(2x-10)$ with a kriging-type predictor built on the cubic spline correlation function, for four values of the correlation parameter $\theta$.

## Exercises

**Exercise 1.** Three high-fidelity samples have values $Y = (1.2, 2.1, 3.3)$, and the low-fidelity model gives $F = (1.0, 2.0, 3.0)$ at the same points. Assuming uncorrelated residuals ($R = I$), compute the scaling factor $\beta = (F^T R^{-1} F)^{-1} F^T R^{-1} Y$ and the residuals $Y - F\beta$ that the correlation term must interpolate.

<details>
<summary>Answer</summary>

$F^T F = 1 + 4 + 9 = 14$ and $F^T Y = 1.2 + 4.2 + 9.9 = 15.3$, so $\beta = 15.3/14 \approx 1.0929$. The residuals are $Y - F\beta = (0.1071, -0.0857, 0.0214)$. The low-fidelity model underpredicts by about 9% overall, and the Gaussian-process part corrects the small remaining local differences.

</details>

**Exercise 2.** Using the form $\hat{y}(x) = f(x)\beta + r(x)^T R^{-1}(Y - F\beta)$, prove that hierarchical Kriging interpolates the high-fidelity data: $\hat{y}(x^{(i)}) = y_i$.

<details>
<summary>Answer</summary>

At a sample point, the correlation vector is the $i$-th column of $R$, so $r(x^{(i)}) = R e_i$, and $f(x^{(i)}) = F_i$. Therefore

```math
\hat{y}(x^{(i)}) = F_i\beta + e_i^T R R^{-1}(Y - F\beta) = F_i\beta +
(y_i - F_i\beta) = y_i
```

This holds for any $\beta$ and any low-fidelity model, provided $R$ is nonsingular (no nugget term).

</details>

**Exercise 3.** The high-fidelity response is $y(x) = 2x + 0.5x(1 - x)$ and the low-fidelity model is $\bar{y}(x) = 2x$. High-fidelity samples are taken at $x = 0, 0.5, 1$, with correlation $R(h) = \exp(-10h^2)$. Compute $\beta$ and the hierarchical Kriging prediction at $x = 0.25$, and compare with $\bar{y}(0.25)$, $\beta\bar{y}(0.25)$ and the true value.

<details>
<summary>Answer</summary>

$Y = (0, 1.125, 2)$ and $F = (0, 1, 2)$. The off-diagonal correlations are $e^{-2.5} = 0.0821$ (neighbours) and $e^{-10} \approx 4.5 \times 10^{-5}$.

Solving gives $\beta = 1.0225$ and residuals $Y - F\beta = (0, 0.1025, -0.0450)$. With $r(0.25) = (e^{-0.625}, e^{-0.625}, e^{-5.625})$, the prediction is $\hat{y}(0.25) = 0.5639$.

For comparison, $\bar{y}(0.25) = 0.5$, $\beta\bar{y}(0.25) = 0.5112$ and $y(0.25) = 0.59375$. The correlation correction closes about 68% of the gap between the low-fidelity model and the truth using only three expensive samples. The rest comes from the limited sample density and the choice of $\theta$.

</details>

**Exercise 4.** Suppose the high-fidelity data are an exact multiple of the low-fidelity values at the samples, $Y = cF$. Show that $\beta = c$ and that the predictor reduces to $\hat{y}(x) = c\,\bar{y}(x)$ everywhere. Why is this a desirable property for variable-fidelity modelling?

<details>
<summary>Answer</summary>

$\beta = (F^T R^{-1} F)^{-1} F^T R^{-1}(cF) = c$, so $Y - F\beta = 0$ and the correlation term vanishes. Then $\hat{y}(x) = f(x)\beta = c\,\bar{y}(x)$ for every $x$. When the low-fidelity model has the correct shape and is only mis-scaled, hierarchical Kriging recovers the scaled model exactly and introduces no spurious bumps between samples. This is the source of its robustness compared with fitting the high-fidelity data alone.

</details>

## References

- Z.-H. Han and S. Görtz, "Hierarchical Kriging model for variable-fidelity surrogate modeling", *AIAA Journal* 50(9), 2012.
- M. C. Kennedy and A. O'Hagan, "Predicting the output from a complex computer code when fast approximations are available", *Biometrika* 87(1), 2000.
- A. I. J. Forrester, A. Sóbester and A. J. Keane, "Multi-fidelity optimization via surrogate modelling", *Proceedings of the Royal Society A* 463(2088), 2007.
- A. I. J. Forrester, A. Sóbester and A. J. Keane, *Engineering Design via Surrogate Modelling: A Practical Guide*, Wiley, 2008.
