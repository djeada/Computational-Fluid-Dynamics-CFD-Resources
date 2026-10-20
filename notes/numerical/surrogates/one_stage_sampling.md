# One-Stage Sampling Plans

A one-stage (or a priori) sampling plan fixes all $N$ sample points before any expensive evaluation is made. It is the first step of every surrogate study and often the only one when the runs are submitted to a cluster as one batch. Since nothing is known about the response yet, the points are chosen for their geometry: they should cover the design space evenly, have no near-duplicates, and project well onto each input. This note covers factorial and screening designs, Latin hypercubes, the criteria that measure space-filling quality, low-discrepancy sequences and orthogonal arrays, and works through a nine-point example.

The plan is followed by surrogate fitting ([Surrogate Models in CFD](intro.md)) and, when the budget allows, by sequential refinement ([Adaptive Sampling](adaptive_sampling.md)). The application to vehicle design studies, with sample-size guidelines and train/test splits, is in [Design of Experiments and Dataset Construction](../../machine_learning/automotive_aerodynamics/datasets.md).

## Problem Statement

The inputs are scaled to the unit cube, $\Omega = [0, 1]^d$, by $x_k = (q_k - a_k)/(b_k - a_k)$ for a physical variable $q_k \in [a_k, b_k]$. Choose a design

```math
X = \{x^{(1)}, \dots, x^{(N)}\} \subset [0, 1]^d
```

with $N$ fixed by the budget, such that a surrogate fitted to $`\{x^{(i)}, f(x^{(i)})\}`$ is accurate over all of $\Omega$ for any reasonable $f$. That goal cannot be evaluated before the runs, so it is replaced by computable proxies: distances between points (no two points should be close, no point of $\Omega$ should be far from the design), discrepancy (the fraction of points in any box should match the box volume), and the quality of the one- and two-dimensional projections (if only a few inputs matter, the design should still have $N$ distinct values of each). A design is good when it scores well on these criteria in the projections that matter, and the difficulty is that $N$ is small (often $10d$) while $d$ can be 10 or more, so every design is sparse.

## Factorial Designs

### Full Factorial

A full factorial design takes $n_k$ equally spaced levels in each input and all their combinations,

```math
x_k \in \left\{0, \frac{1}{n_k - 1}, \dots, 1\right\}, \qquad N = \prod_{k=1}^{d} n_k = n^d \text{ if } n_k = n
```

It is easy to construct and to interpret, and a two-level factorial ($n = 2$) estimates every main effect and interaction of a linear model with interactions independently. Its weaknesses for surrogate modelling are the exponential growth of $N$, the restriction of $N$ to products of level counts, and the poor projections: in each one-dimensional projection the $n^d$ points collapse onto only $n$ values, so most runs repeat information about each single input.

### Fractional Factorial

A two-level fractional factorial $2^{d-p}$ keeps $2^{d-p}$ of the $2^d$ corners. With levels coded $\pm 1$, the first $d - p$ columns form a full factorial and each remaining column is defined by a generator, a product of earlier columns. In the $2^{3-1}$ design with generator $C = AB$ the runs are

| Run | $A$ | $B$ | $C = AB$ |
| --- | --- | --- | --- |
| 1 | $-1$ | $-1$ | $+1$ |
| 2 | $+1$ | $-1$ | $-1$ |
| 3 | $-1$ | $+1$ | $-1$ |
| 4 | $+1$ | $+1$ | $+1$ |

The defining relation is $I = ABC$, so each main effect is aliased with a two-factor interaction ($A = BC$, $B = AC$, $C = AB$): the design cannot tell them apart. The resolution, the length of the shortest word in the defining relation (here III), measures how severe the aliasing is (Montgomery, 2017). Fractional factorials are screening designs: they find which of many inputs matter before a space-filling design is spent on those that do.

### Plackett–Burman Designs

Plackett and Burman (1946) constructed two-level orthogonal designs for $N$ a multiple of 4, which estimate up to $N - 1$ main effects from $N$ runs. The 12-run design takes the generating row

```math
(+\,+\,-\,+\,+\,+\,-\,-\,-\,+\,-)
```

its 10 cyclic shifts, and a final row of all $-$ signs. The 11 columns are mutually orthogonal and balanced (six $+$ and six $-$ each). Plackett–Burman designs assume interactions are negligible, and their main effects are partially aliased with two-factor interactions, so they are used only for screening.

## Latin Hypercube Sampling

### Definition and Construction

A Latin hypercube design (LHD) of $N$ points in $d$ dimensions divides each axis into $N$ equal intervals $I_j = [(j - 1)/N, j/N)$ and places exactly one point in each interval of each axis (McKay, Beckman and Conover, 1979). It is built as follows:

1. Draw $d$ independent random permutations $\pi_1, \dots, \pi_d$ of $`\{1, \dots, N\}`$.
2. For point $i$ and coordinate $k$, choose the interval $I_{\pi_k(i)}$.
3. Place the coordinate inside that interval, either at a uniform random position or at its centre:

```math
x_k^{(i)} = \frac{\pi_k(i) - u_{ik}}{N}, \qquad u_{ik} \sim \mathcal{U}(0, 1) \text{ or } u_{ik} = \tfrac{1}{2}
```

Any $N$ is possible, and removing one input leaves an LHD in $d - 1$ dimensions.

### Properties

Every one-dimensional projection is perfectly stratified. For estimating the mean of $f$ by the sample average, a random LHD is never much worse than independent random sampling, and it removes the variance contributed by the additive part $\sum_k g_k(x_k)$ of $f$. For surrogate fitting this means that the main effects of all inputs are sampled at $N$ distinct levels each.

Stratification in one dimension says nothing about the joint layout. The identity permutation $\pi_1 = \pi_2 = \dots$ is a valid LHD with all points on the diagonal, and random permutations often leave clusters and empty regions. This is why an LHD is almost always optimized for a space-filling criterion.

### Maximin Latin Hypercubes

Morris and Mitchell (1995) proposed searching over LHDs for the one that is best by the $\phi_p$ criterion defined below, using simulated annealing in which each move swaps two entries of one column. A swap keeps the Latin property, so the search never leaves the set of LHDs. The cheapest variant, used in many codes, draws a few hundred random LHDs and keeps the best. The [Adaptive Sampling with Kriging](../../../scripts/algorithms/adaptive_sampling_kriging/) script uses that best-of-20 rule for its initial designs.

## Space-Filling Criteria

### Distance-Based Criteria

Let $d_{ij} = \lVert x^{(i)} - x^{(j)} \rVert_2$. Johnson, Moore and Ylvisaker (1990) defined two optimal designs:

```math
\text{maximin:} \quad \max_X \ \min_{i \neq j} d_{ij},
\qquad
\text{minimax:} \quad \min_X \ \max_{x \in \Omega} \min_i \lVert x - x^{(i)} \rVert
```

A maximin design has no two points close together, so no CFD run is wasted on a near-duplicate. A minimax design leaves no point of $\Omega$ far from a sample, which bounds the distance over which the surrogate must interpolate; it is harder to compute because it needs a maximum over the whole domain. Many designs share the same minimum distance, so Morris and Mitchell (1995) proposed the scalar criterion

```math
\phi_p(X) = \left(\sum_{i < j} d_{ij}^{-p}\right)^{1/p}
```

to be minimized. For large $p$ the smallest distances dominate, and $\phi_p \to 1/\min_{i \ne j} d_{ij}$ as $p \to \infty$, so minimizing $\phi_p$ breaks ties between designs with the same maximin distance in favour of those with fewer pairs at that distance. Values $p = 20$ to $50$ are usual.

### Discrepancy

The star discrepancy compares the fraction of points in every box anchored at the origin with the box volume:

```math
D_N^*(X) = \sup_{a \in [0, 1]^d}\left|\frac{\#\{i : x^{(i)} \in [0, a)\}}{N} - \prod_{k=1}^{d} a_k\right|
```

It appears in the Koksma–Hlawka inequality, which bounds the error of the sample mean of $f$ by $`V_{HK}(f)\,D_N^*(X)`$ with $V_{HK}$ the Hardy–Krause variation (Niederreiter, 1992). The supremum is expensive to compute, so $L_2$ versions are used in practice. The $L_2$-star discrepancy, which averages instead of taking the supremum, has the closed form

```math
\left(D_2^*\right)^2 = 3^{-d} - \frac{2^{1-d}}{N}\sum_{i=1}^{N}\prod_{k=1}^{d}\left(1 - x_{ik}^2\right) + \frac{1}{N^2}\sum_{i=1}^{N}\sum_{j=1}^{N}\prod_{k=1}^{d}\left(1 - \max(x_{ik}, x_{jk})\right)
```

where $x_{ik}$ is coordinate $k$ of point $i$. It favours points near the corner $(1, \dots, 1)$, because all boxes contain the origin. The centred $L_2$ discrepancy of Hickernell (1998) uses boxes anchored at the nearest corner, which makes it invariant under reflections $x_k \to 1 - x_k$:

```math
\mathrm{CD}^2 = \left(\frac{13}{12}\right)^d - \frac{2}{N}\sum_{i=1}^{N}\prod_{k=1}^{d}\left(1 + \frac{1}{2}a_{ik} - \frac{1}{2}a_{ik}^2\right) + \frac{1}{N^2}\sum_{i,j=1}^{N}\prod_{k=1}^{d}\left(1 + \frac{1}{2}a_{ik} + \frac{1}{2}a_{jk} - \frac{1}{2}\left|x_{ik} - x_{jk}\right|\right)
```

with $a_{ik} = |x_{ik} - 1/2|$. It is the measure used in the figure below and is available as `scipy.stats.qmc.discrepancy(X, method="CD")`, which returns $\mathrm{CD}^2$.

Distance and discrepancy measure different things and both should be checked. A design can have small discrepancy and still contain two almost coincident points, and a maximin design in high dimension tends to push points to the boundary of the cube, which raises its discrepancy.

## Low-Discrepancy Sequences

### Van der Corput and Halton

Write the integer $i$ in base $b$ as $i = \sum_j a_j b^j$. The radical inverse mirrors the digits about the radix point:

```math
\phi_b(i) = \sum_{j \ge 0} a_j\, b^{-j-1}
```

The van der Corput sequence $\phi_2(1), \phi_2(2), \dots = 1/2, 1/4, 3/4, 1/8, 5/8, \dots$ fills $[0, 1]$ by repeatedly halving the gaps. The Halton sequence uses a different prime base per coordinate, $x^{(i)} = (\phi_2(i), \phi_3(i), \phi_5(i), \dots)$, and the Hammersley set replaces the first coordinate by $i/N$ for a fixed $N$. In high dimensions the large prime bases produce long linear runs and strong correlations between neighbouring coordinates unless the digits are scrambled.

### Sobol Sequences and Nets

The Sobol sequence uses base 2 in every coordinate, with digit permutations generated by direction numbers chosen per dimension. Its first $2^m$ points form a $(t, m, d)$-net in base 2: every elementary box $\prod_k [c_k 2^{-l_k}, (c_k + 1) 2^{-l_k})$ of volume $2^{t-m}$ contains exactly $2^t$ points, with a quality parameter $t$ that is small for good direction numbers. The balance holds only for $N$ a power of two, which is why Sobol designs should have $N = 2^m$ points.

Low-discrepancy sequences achieve

```math
D_N^* = \mathcal{O}\left(\frac{(\log N)^d}{N}\right)
```

against $\mathcal{O}(N^{-1/2})$ for random points. The logarithmic factor is large when $d$ is large and $N$ moderate, so the bound alone guarantees little for $d = 10$ (Exercise 2), yet Sobol points still perform well in practice, because CFD responses are dominated by low-dimensional projections, where the sequences are very uniform. Both sequences are extensible: continuing the sequence fills the gaps of the earlier points, which a Latin hypercube cannot do without losing its stratification.

### Scrambling

Owen (1995) applied random nested permutations to the digits of a net. The scrambled points keep the net property, but each point is uniformly distributed on $[0, 1]^d$, so the sample mean is unbiased and independent replicates give an error estimate. For smooth integrands the root-mean-square error of a scrambled net falls like $N^{-3/2}(\log N)^{(d-1)/2}$ (Owen, 1997). For surrogate design, scrambling mainly removes the artefacts of the unscrambled sequences: the point at the origin, the aligned initial points and the correlated coordinates of Halton in high dimension. `scipy.stats.qmc.Sobol` and `scipy.stats.qmc.Halton` scramble by default.

![Random, Latin hypercube and scrambled Sobol designs of 32 points and their centred L2 discrepancy against N](../../../scripts/plots/sampling_strategies_comparison/sampling_strategies_comparison.png)

The top row compares 32-point random, Latin hypercube and scrambled Sobol designs with their marginal histograms: the random design leaves columns empty, while the other two fill every column. The bottom panel shows the centred $L_2$ discrepancy averaged over seeds: random and Latin hypercube designs decay at about $N^{-1/2}$, with a smaller constant for the Latin hypercube, while scrambled Sobol decays at about $N^{-1}$.

## Orthogonal Arrays

An orthogonal array $\mathrm{OA}(N, d, s, t)$ is an $N \times d$ array with entries in $`\{1, \dots, s\}`$ in which every set of $t$ columns contains each of the $s^t$ possible rows equally often. Strength $t = 1$ is the stratification of one Latin hypercube column; a two-level fractional factorial of resolution III is an orthogonal array of strength 2. Tang (1993) used orthogonal arrays to build Latin hypercubes that are also stratified on the $s \times s$ grid of every two-dimensional projection: the 9-run array $\mathrm{OA}(9, 4, 3, 2)$ gives a 9-point, 4-variable Latin hypercube in which every 2D projection has one point in each of the nine cells of a $3 \times 3$ grid. Such designs are worth considering when interactions between pairs of inputs are expected.

## Worked Example

Take $d = 2$, $N = 9$ and a midpoint Latin hypercube from the permutations

```math
\pi_1 = (2, 9, 4, 1, 8, 3, 7, 5, 6), \qquad \pi_2 = (5, 2, 1, 8, 4, 9, 6, 7, 3)
```

The interval midpoints are $(2j - 1)/18$, so the points in units of $1/18$ are $(3, 9)$, $(17, 3)$, $(7, 1)$, $(1, 15)$, $(15, 7)$, $(5, 17)$, $(13, 11)$, $(9, 13)$ and $(11, 5)$. Each odd number from 1 to 17 appears once per coordinate, which confirms the Latin property. The 36 pairwise distances give the scores in the first row below. The other rows are the best midpoint LHD found by exhaustive search over all $9!$ second permutations (Exercise 5), the first nine points of the unscrambled Halton sequence in bases 2 and 3, and the mean over 2000 sets of nine independent uniform points.

| Design | $\min_{i \ne j} d_{ij}$ | Pairs at the minimum | $\phi_{50}$ | $\mathrm{CD}^2$ |
| --- | --- | --- | --- | --- |
| Random LHD above | 0.2485 | 5 | 4.157 | $6.28 \times 10^{-3}$ |
| Best midpoint LHD, $\pi_2(i) = 3i \bmod 10$ | 0.3514 | 12 | 2.991 | $3.79 \times 10^{-3}$ |
| Halton, $i = 1, \dots, 9$ | 0.1672 | 1 | 5.979 | $1.04 \times 10^{-2}$ |
| Independent uniform (mean) | — | — | — | $4.36 \times 10^{-2}$ |

The optimized Latin hypercube is better by both measures: its minimum distance is $\sqrt{2}$ times larger and its discrepancy is 40% lower. For only nine points the Halton sequence does not beat a random LHD, which is consistent with the asymptotic nature of its bound; its advantage appears as $N$ grows and when points must be added later. All structured designs are about an order of magnitude better than independent random points.

## Choosing a Design

| Design | 1D projections | Allowed $N$ | Extensible | Use |
| --- | --- | --- | --- | --- |
| Full factorial | $n$ values | $n^d$ | Only by a full new level | $d \le 3$, or interaction studies with 2 levels |
| Fractional factorial, Plackett–Burman | 2 values | $2^{d-p}$, multiple of 4 | No | Screening many inputs |
| Random Latin hypercube | Stratified | Any | No | Baseline; avoid without optimization |
| Maximin or $\phi_p$-optimal LHD | Stratified | Any | No | Default for $N$ fixed in advance |
| OA-based LHD | Stratified in 1D and on a grid in 2D | $s^2$ and similar | No | Expected pairwise interactions |
| Scrambled Sobol | Balanced for $N = 2^m$ | Powers of 2 preferred | Yes | Large $N$, staged budgets, quasi-Monte Carlo |

For kriging surrogates an initial design of about $N = 10d$ points is a common starting rule (Loeppky, Sacks and Welch, 2009); it is adequate for smooth responses dominated by a few inputs and not for responses with sharp local features. If the budget may grow, or a second batch of runs is likely, an extensible sequence or a sequential design is better than a Latin hypercube whose size had to be fixed in advance.

## Key Takeaways

- A one-stage design is chosen by geometry alone: even coverage, no near-duplicates, and good low-dimensional projections.
- Factorial and Plackett–Burman designs are for screening; they project onto only two levels per input and grow badly with $d$.
- Latin hypercubes stratify every input but must be optimized (maximin, $\phi_p$) to avoid clusters.
- Discrepancy and distance criteria measure different defects; check both, in the projections that matter.
- Scrambled Sobol sequences are extensible, balanced for $N = 2^m$, and the usual choice when the budget is staged.

## Related Scripts

- [Sampling Strategies Comparison](../../../scripts/plots/sampling_strategies_comparison/): compares random, Latin hypercube and scrambled Sobol designs of the same size in a 2D design space, showing their point layouts, their 1D marginal histograms and how their centred $L_2$ discrepancy falls with the number of samples.
- [Design Space Distribution via Sobol Sequences](../../../scripts/plots/design_space_distribution/): draws a four-dimensional scrambled Sobol design of 512 geometry variants and shows all of its 2D projections and 1D marginals in a scatter matrix, with the discrepancy of each projection compared against a random design of the same size.
- [Adaptive Sampling with Kriging](../../../scripts/algorithms/adaptive_sampling_kriging/): grows a kriging surrogate of a 2D test function from an 8-point maximin Latin hypercube to 40 samples with max-MSE and LOO-CV infill criteria and compares both with one-shot maximin Latin hypercubes of the same size.
- [Sobol Sensitivity Analysis](../../../scripts/algorithms/sobol_sensitivity_analysis/): estimates first-order and total Sobol sensitivity indices of a synthetic five-parameter drag model with the Saltelli sampling scheme and checks them against the exact values.

## Exercises

**Exercise 1.** How many points does a full factorial design with 4 levels per variable need for $d = 6$? How many distinct midpoint Latin hypercube designs exist for $N$ points in $d$ dimensions (counting designs as point sets), and how many for $N = 9$, $d = 2$?

<details>
<summary>Answer</summary>

Full factorial: $4^6 = 4096$ points.

LHDs: order the points by their first coordinate. Each of the remaining $d - 1$ coordinates can be any permutation of $`\{1, \ldots, N\}`$, giving $(N!)^{d-1}$ distinct designs. For $N = 9$, $d = 2$: $9! = 362880$ designs.

</details>

**Exercise 2.** Low-discrepancy sequences achieve $D_N^* = \mathcal{O}((\log N)^d/N)$ against $\mathcal{O}(N^{-1/2})$ for random sampling. Evaluate both rates for $N = 10^4$ with $d = 2$ and $d = 10$ (ignoring constants). What does the comparison suggest?

<details>
<summary>Answer</summary>

$N^{-1/2} = 0.01$.

- $d = 2$: $(\ln 10^4)^2/10^4 = 9.21^2/10^4 = 0.0085$, already slightly better than random.
- $d = 10$: $9.21^{10}/10^4 \approx 4.4 \times 10^5$, meaningless as a bound.

The asymptotic advantage appears only for very large $N$ when $d$ is high. In practice Sobol sequences still perform well in moderate dimensions, because the responses depend mostly on low-dimensional projections, but the bound alone does not guarantee it.

</details>

**Exercise 3.** For the worked example, verify the minimum distance $\delta_{\min}$ and find the pairs that attain it.

<details>
<summary>Answer</summary>

Work in units of $1/18$. The smallest squared distance between two of the nine points is $4^2 + 2^2 = 20$, so $\delta_{\min} = \sqrt{20}/18 \approx 0.2485$. Checking all 36 pairs shows that exactly five attain it: $(17, 3)$–$`(15, 7)`$, $`(1, 15)`$–$`(5, 17)`$, $`(15, 7)`$–$`(13, 11)`$, $`(15, 7)`$–$`(11, 5)`$ and $`(13, 11)`$–$`(9, 13)`$. Three of the five involve the point $`(15, 7)`$, which is the natural candidate to move in an optimization of the design.

</details>

**Exercise 4.** For the design of the worked example, evaluate $\phi_p = \left(\sum_{i < j} d_{ij}^{-p}\right)^{1/p}$ for $p = 2$ and $p = 50$, and compare with $1/\delta_{\min}$. Explain the limit $p \to \infty$.

<details>
<summary>Answer</summary>

Over all 36 pairwise distances, $\phi_2 = 14.08$ and $\phi_{50} = 4.157$, while $1/\delta_{\min} = 4.025$.

For large $p$ the sum is dominated by the $k$ pairs at the minimum distance, so $\phi_p \approx k^{1/p}/\delta_{\min}$. Here $k = 5$, and $5^{1/50} \times 4.025 = 4.157$. As $p \to \infty$ the factor $k^{1/p}$ tends to 1, so minimizing $\phi_p$ becomes maximizing $\delta_{\min}$, and for finite $p$ designs with fewer pairs at the minimum distance are preferred.

</details>

**Exercise 5.** Write a short script that enumerates all $9!$ midpoint LHDs with $\pi_1$ equal to the identity and finds the design with the largest $\delta_{\min}$. Report the best $\delta_{\min}$, a permutation that attains it, and the improvement over the worked example.

<details>
<summary>Answer</summary>

The exhaustive search gives $\delta_{\min} = \sqrt{40}/18 \approx 0.3514$, attained by $\pi_2 = (3, 6, 9, 2, 5, 8, 1, 4, 7)$ (that is, $\pi_2(i) = 3i \bmod 10$) and by its mirror image $(7, 4, 1, 8, 5, 2, 9, 6, 3)$. The points form a rotated lattice in which each nearest-neighbour pair is offset by $(1, 3)$ or $(3, -1)$ interval units. The improvement over the random design is a factor $\sqrt{40}/\sqrt{20} = \sqrt{2} \approx 1.41$. Exhaustive search is only possible for tiny $N$, which is why larger designs rely on heuristics such as simulated annealing.

</details>

## References

- M. D. McKay, R. J. Beckman and W. J. Conover, "A comparison of three methods for selecting values of input variables in the analysis of output from a computer code", *Technometrics* 21(2), 239–245, 1979.
- M. E. Johnson, L. M. Moore and D. Ylvisaker, "Minimax and maximin distance designs", *Journal of Statistical Planning and Inference* 26(2), 131–148, 1990.
- M. D. Morris and T. J. Mitchell, "Exploratory designs for computational experiments", *Journal of Statistical Planning and Inference* 43(3), 381–402, 1995.
- R. L. Plackett and J. P. Burman, "The design of optimum multifactorial experiments", *Biometrika* 33(4), 305–325, 1946.
- B. Tang, "Orthogonal array-based Latin hypercubes", *Journal of the American Statistical Association* 88(424), 1392–1397, 1993.
- F. J. Hickernell, "A generalized discrepancy and quadrature error bound", *Mathematics of Computation* 67(221), 299–322, 1998.
- A. B. Owen, "Randomly permuted (t, m, s)-nets and (t, s)-sequences", in *Monte Carlo and Quasi-Monte Carlo Methods in Scientific Computing*, Lecture Notes in Statistics 106, Springer, 299–317, 1995.
- A. B. Owen, "Scrambled net variance for integrals of smooth functions", *The Annals of Statistics* 25(4), 1541–1562, 1997.
- H. Niederreiter, *Random Number Generation and Quasi-Monte Carlo Methods*, SIAM, 1992.
- D. C. Montgomery, *Design and Analysis of Experiments*, 9th ed., Wiley, 2017.
- J. L. Loeppky, J. Sacks and W. J. Welch, "Choosing the sample size of a computer experiment: a practical guide", *Technometrics* 51(4), 366–376, 2009.
