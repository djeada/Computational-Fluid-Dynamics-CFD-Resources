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

$$y(x) = \bar{y}(\bar{\phi}(p), p, a) + z(x), \quad x \in \Omega \subset \mathbb{R}^d.$$

The term $z(x)$ represents a zero-mean Gaussian process used to model the deviation from $\bar{y}(x)$. In classical Kriging, the deterministic part is often a linear trend $f(x)^T \beta$. By using $\bar{y}(x)$ instead, one incorporates prior knowledge or a simpler model directly, improving efficiency and accuracy.

## Hierarchical Kriging Predictor

As in standard Kriging, the predictor $\hat{y}(x)$ at an arbitrary point $x$ is a weighted linear combination of the known responses $Y = \{ y(x^{(1)}), \dots, y(x^{(N)}) \}$:

$$\hat{y}(x) = \lambda(x)^T Y,$$

where $\lambda(x) \in \mathbb{R}^N$ is a vector of weights determined by solving a linear system that ensures both unbiasedness and minimal mean squared error. To achieve unbiasedness, one imposes constraints involving $\bar{y}(x)$ at the sample points.

Define the correlation matrix $R \in \mathbb{R}^{N \times N}$ from the Gaussian process assumption, and a vector $r(x) \in \mathbb{R}^N$ of correlations between $x$ and the sample points $X = \{x^{(i)}\}$. With Hierarchical Kriging, the role of the regression matrix $F \in \mathbb{R}^{N}$ (which in standard Kriging corresponds to the regression functions evaluated at sample points) is taken by:

$$F := \bigl( \bar{y}(\bar{\phi}(p), p, a) \bigr)_{i=1}^N \in \mathbb{R}^N.$$

Similarly, for the point $x$, we define:

$$f(x) := \bar{y}(\bar{\phi}(p), p, a).$$

The Kriging system, ensuring optimal weights, is:

$$\begin{pmatrix}

R & F \\ F^T & 0

\end{pmatrix}

\begin{pmatrix}

\lambda(x) \\ \mu(x)

\end{pmatrix}

=

\begin{pmatrix}
r(x) \\ f(x)

\end{pmatrix}.$$

Solving this system yields $\lambda(x)$ and $\mu(x)$, which in turn gives the prediction $\hat{y}(x) = \lambda(x)^T Y$.

## Closed-Form Predictor and Interpretation

Using matrix operations, one can write the Hierarchical Kriging predictor in a compact form:

$$\hat{y}(x) = 

\begin{pmatrix}
r(x)^T & f(x)

\end{pmatrix}

\begin{pmatrix}

R & F \\ F^T & 0

\end{pmatrix}^{-1}

\begin{pmatrix}

Y \\ 0

\end{pmatrix}.$$

Alternatively, if we define:

$$\beta := (F^T R^{-1} F)^{-1} F^T R^{-1} Y,$$

we can express the predictor as:

$$\hat{y}(x) = f(x) \beta + r(x)^T R^{-1}(Y - F \beta).$$

This form mirrors the structure of standard Kriging but replaces the regression term with the low-fidelity model $\bar{y}$. The coefficient $\beta$ adjusts the scale of the low-fidelity model so that the combined model $f(x)\beta$ fits the global trend suggested by $Y$. The term $r(x)^T R^{-1}(Y - F \beta)$ ensures that the model interpolates the data exactly, applying local corrections based on the correlation structure.

## Practical Implementation

In practice, the preferred formulation for implementation is the block matrix inversion form. Rather than explicitly computing $\beta$, one solves:

$$\begin{pmatrix}

R & F \\ F^T & 0

\end{pmatrix}

\begin{pmatrix}
w^{(Y)} \\ w^{(f)}

\end{pmatrix}

=

\begin{pmatrix}

Y \\ 0

\end{pmatrix},$$

where $\begin{pmatrix} w^{(Y)} \\ w^{(f)} \end{pmatrix}$ is independent of $x$ and can be solved once and stored. The predictor evaluation at a new point $x$ then involves computing $(r(x), f(x))$ and taking their dot product with the stored solution. This method is computationally efficient and maintains the exact interpolation property.

## Interpreting the Correction Terms

When the low-fidelity model $\bar{y}(x)$ closely approximates the high-fidelity response $y(x^{(i)})$ at sample points, the coefficient $\beta$ will approach unity. This means that the low-fidelity model is already a good predictor of $Y$, and only minor corrections are needed from the correlation terms. On the other hand, if $\bar{y}$ is less accurate, the correlation-based correction will have a more substantial role, pulling the predictions towards the exact known data points and ensuring an interpolation that corrects any discrepancies.

## Example Scenarios

I. **Accurate Low-Fidelity Model**: Suppose $\bar{y}(x)$ is a near-perfect approximation. Then $\hat{y}(x)$ will differ from $\bar{y}(x)$ only by a small, smooth correction, ensuring exact interpolation without much alteration of the global trend.

II. **Coarse Low-Fidelity Model**: If $\bar{y}(x)$ is only a rough approximation, the correlation corrections $r(x)^T R^{-1}(Y - F \beta)$ will dominate, refining the surrogate especially near known samples and gradually bending $\bar{y}(x)$ towards the observed data $Y$.

In either scenario, Hierarchical Kriging ensures that the final model honors the data points exactly, overcoming the limitations of pure least squares approximations and benefiting from the global trend captured by the low-fidelity model.
