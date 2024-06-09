# One-Stage Sampling

- One-stage sampling designs are used in deterministic computer experiments.
- They determine the design points $X = \{ x^{(1)}, \ldots, x^{(N)} \} \subset \Omega$ before computing any observations $y(x^{(i)})$.
- Also known as a-priori or input-based designs since $y(x)$ has no influence on $X$.
- Goal: Produce surrogate models that are globally accurate.
- Without information on $y(x)$, designs should be space-filling, meaning samples $x^{(i)}$ are evenly distributed in $\Omega$.

## Types of One-Stage Approaches
- **Deterministic vs. Random Designs**: Deterministic designs follow a specific pattern, while random designs rely on randomness.
- **Model-Based vs. Model-Independent**:
  - **Model-Independent**: Only require knowledge about $\Omega$ and the number of samples $N$.
  - **Model-Based**: Require additional information about the surrogate model $\hat{y}(x)$, such as the regression matrix $F$ and the correlation matrix $R$.
    - Correlation matrix depends on the design $X$ and the correlation function’s hyperparameters $\theta$, typically determined by maximum likelihood estimation.

## Comparison with Adaptive Sampling
- **Adaptive Sampling**: Learns about $y(x)$ and adjusts the design accordingly.
- **One-Stage Sampling**: Independent of $y(x)$, producing generic designs.
- **Advantages of Adaptive Sampling**:
  - More accurate surrogate models for the same sample size $N$.
  - Allows for parallel computation, increasing efficiency.

## Applications and Considerations
- **Screening**: Identifies redundant variables in high-dimensional input spaces to reduce problem complexity.
- **Parallel Computing**: Enables simultaneous computation of $y(x^{(1)}), \ldots, y(x^{(N)})$, reducing wall clock time.
- **Initial Designs for Adaptive Strategies**: Small initial designs help in higher-dimensional problems where careful selection is crucial.

## Literature Survey on One-Stage Designs
- **Historical Context**: Early studies on designs for regression models predate surrogate modeling for computer experiments.
- **Key Publications**:
  - **Early Works**: Discussed model-based approaches like the entropy criterion, IMSE, and MMSE criteria.
  - **Minimax and Latin Hypercube Designs**: Introduced various techniques to improve design performance.
  - **Gradient-Enhanced Kriging**: Discussed different design strategies including Latin hypercube and maximin designs.
- **Comprehensive Reviews**: Provided by authors like [73], who reviewed one-stage approaches and computational investigations into low-discrepancy designs.
- **Recent Surveys**: Covered advancements in Latin hypercube designs and new algorithms for optimizing these designs.

### Factorial Designs

- **Full Factorial Designs**:
  - Distribute samples evenly in a d-dimensional hypercube $\Omega$.
  - Consist of $N = \prod_{k=1}^{d} N_k$ points on a grid.
  - Coordinates: $x_k = \frac{i_k - 1}{N_k - 1}$ ($i_k = 1, \ldots, N_k, k = 1, \ldots, d$).
  - If no information on input parameters $x_k$, values for $N_k$ are usually uniform, resulting in $N = n^d$ points on a regular grid.
  - **Limitations**:
    - Each variable $x_k$ takes only $n$ distinct values.
    - Removing a variable $x_k$ collapses the design to $n^{d-1}$ points.
    - Curse of dimensionality: Total samples $N = n^d$ grow exponentially with $d$.
    - Limited to specific sample sizes $N = \prod_{k=1}^{d} N_k$, i.e., non-prime numbers.

- **Fractional Factorial Designs**:
  - Reduce the number of samples from a full factorial design to overcome dimensionality issues.
  - Useful for screening variables and reducing sample sizes in $2^d$-factorial designs.
  - Example: $2^{10}$-factorial design with 10 variables results in 1024 samples, which is computationally intensive.
  - Fractional designs delete specific samples to maintain performance with fewer evaluations.

- **Stratified Random Samplings**:
  - Subdivide domain $\Omega$ into $N = n^d$ equal bins or strata.
  - Randomly choose a sample from each bin.
  - Ensures each region of the input space is represented, with each variable $x_k$ generally taking more than $n$ values.
  - **Issues**:
    - Potential large holes in the design.
    - Possible clustering of samples, leading to closely adjacent points that cause ill-conditioned correlation matrices in Kriging models.

### Distance-Based Designs

- **Minimax Designs**:
  - Introduced as space-filling designs for computer experiments.
  - Objective: Minimize the maximum distance from any point $x \in \Omega$ to the nearest design point $x^{(i)}$.
  - Formulation:
    
$$
\max_{x \in \Omega} \text{dist}(x, X^*) = \min_{X \subset \Omega, |X| = N} \max_{x \in \Omega} \text{dist}(x, X)
$$

  - Ensures all points in $\Omega$ are within a small distance $\epsilon$ to the nearest design point.

- **Maximin Designs**:
  - Select samples such that the minimum distance between any pair $x^{(i)}, x^{(j)} \in X^*$ is maximized.
  - Formulation:
    
$$
\min_{x^{(i)}, x^{(j)} \in X^*, i 
eq j} \text{dist}(x^{(i)}, x^{(j)}) = \max_{X \subset \Omega, |X| = N} \min_{x^{(i)}, x^{(j)} \in X, i 
eq j} \text{dist}(x^{(i)}, x^{(j)})
$$

  - Ensures samples are spread out with a minimum distance $\epsilon$ between any two points.

- **$\phi_p$-Designs**:
  - Generalization of maximin distance designs.
  - Consider all pairs of points, using an averaged distance function:
    
$$
\phi_p (X) := \left( \frac{1}{\binom{N}{2}} \sum_{i=1}^{N-1} \sum_{j>i} \text{dist}(x^{(i)}, x^{(j)})^{-p} \right)^{\frac{1}{p}}
$$

  - Choose a design $X$ such that $\phi_p (X)$ is minimized.
  - For $p \rightarrow \infty$, the design becomes a maximin design.

- **Challenges**:
  - Finding optimal distance-based designs is challenging, especially in low-dimensional spaces.
  - Minimax designs relate to covering problems, and maximin designs relate to packing problems in combinatorics.
  - Often only best-known results for a given $N$ are available, with optimal minimax and maximin scores being sought after.

- **Use in Practice**:
  - Minimax score (3.2), maximin score (3.3), and $\phi_p$ (3.4) can measure and compare the space-filling quality of any design $X$.

### Latin Hypercube Designs

- **Concept**:
  - Generate a stratified design $X$ of size $N$ where each variable $x_k$ takes exactly $N$ different, evenly distributed values ($k = 1, \ldots, d$).
  - Introduced in [95].
  - Interval $[0, 1]$ partitioned into $N$ subintervals $I_j := \left[ \frac{j-1}{N}, \frac{j}{N} \right]$ ($j = 1, \ldots, N$).
  - Use d random permutations $\pi_k : \{ 1, \ldots, N \} \rightarrow \{ 1, \ldots, N \}$ ($k = 1, \ldots, d$).
  - Design consists of $N$ samples $x^{(i)} \in I_{\pi_1 (i)} \times \cdots \times I_{\pi_d (i)}$.

- **Sampling Methods**:
  - **Centers of Hypercubes**: Samples chosen as the centers of the hypercubes $I_{\pi_1 (i)} \times \cdots \times I_{\pi_d (i)}$.
  - **Random Sampling**: Coordinates $x_k^{(i)}$ randomly sampled from uniform distributions $\mathcal{U}(I_{\pi_k (i)})$.

- **Advantages**:
  - Ensures each subinterval $I_j \subset [0, 1]$ is represented in the design.
  - Requires only $N$ samples, unlike full factorial designs which need $N^d$ samples.

- **Non-Collapsing Property**:
  - Removing a variable $x_k$ from the model results in a new Latin hypercube design $\tilde{X} \subset \mathbb{R}^{d-1}$ of the same size $N$.
  - E.g., removing $x_d$ results in samples satisfying $x^{(i)} \in I_{\pi_1 (i)} \times \cdots \times I_{\pi_{d-1} (i)}$.

- **Potential Issues**:
  - Random permutations can produce bad designs, leaving large regions uncovered.
  - Worst-case scenario: Permutations are identity functions ($\pi_k (i) = i$), leading to degenerate designs and inaccurate surrogate models.

- **Improvements and Optimization**:
  - Efforts to improve space-filling quality over the past 20 years.
  - **Orthogonal Arrays**: Used to generate Latin hypercube designs evenly representing input space $[0, 1]^d$ ([108, 136]).
  - **Maximin Score ($3.3$) and $\phi_p$ Score ($3.4$)**: Used to enhance space-filling quality ([98]).
  - Recent survey on improvement techniques and new algorithms in [144].
  - Fig. 3.3 depicts an optimized Latin hypercube design generated by Matlab function `lhsdesign`.

### Low-Discrepancy Designs

- **Concept**:
  - Measure space-filling quality of a design $X$ with discrepancy.
  - Interval $I := \{ I \subset \mathbb{R}^d : I = [a_1, b_1] \times \cdots \times [a_d, b_d], a_k < b_k \}$ and its d-dimensional Lebesgue measure Vol(I).
  - Discrepancy $D_N(X)$:
    
$$
D_N (X) := \sup_{I \in \mathcal{I}} \left| \frac{\#(X \cap I)}{N} - \frac{\text{Vol}(I)}{\text{Vol}([0, 1]^d)} \right|
$$

  - Quantifies how much $X$ deviates from the uniform distribution $\mathcal{U}([0, 1]^d)$.

- **Monte Carlo Sampling**:
  - Discrepancy of $D_N(X) = O\left( \frac{1}{\sqrt{N}} \right)$.

- **Low-Discrepancy Sequences**:
  - Developed to improve convergence rate.
  - **Examples**:
    - Hammersley set
    - Van der Corput sequence
    - Sobol sequence
    - Halton sequence
  - Hammersley set depends on $N$, while Sobol and Halton sequences are independent of $N$.
  - Suitable for sequential sampling, refining existing low-discrepancy designs.

- **Applications**:
  - Good space-filling properties make low-discrepancy designs preferred for various applications.


