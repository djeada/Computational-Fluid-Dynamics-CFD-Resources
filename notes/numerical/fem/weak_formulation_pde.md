# Deriving the Weak Formulation for a Reaction-Diffusion PDE

The finite element method (FEM) is a powerful numerical technique for solving partial differential equations (PDEs) that arise in various fields such as physics, engineering, and applied mathematics. One key concept in FEM is the transition from the **strong form** of a PDE (the classical pointwise formulation) to its **weak form**. This process is necessary because it relaxes the differentiability requirements of the solution, allows for the incorporation of boundary conditions in a natural way, and prepares the problem for discretization using finite-dimensional spaces.

In this explanation, we illustrate the derivation of the weak formulation using a reaction-diffusion equation as our model problem.

## Background and Motivation

### Why Weak Formulations?

In many practical problems, the solution to a PDE may not be sufficiently smooth to satisfy the differential equation pointwise. The weak formulation alleviates this issue by:

- **Integrating against test functions:** This “averages” the equation over the domain.
- **Shifting derivatives:** Integration by parts transfers derivatives from the unknown solution onto smoother test functions.
- **Incorporating boundary conditions:** Natural boundary conditions emerge naturally in the weak form.

### Overview of the Process

The process of deriving the weak formulation typically follows these steps:

I. **Start with the strong form of the PDE.**

II. **Multiply by an arbitrary test function** from an appropriate function space.

III. **Integrate over the domain.**

IV. **Apply integration by parts (Green’s theorem)** to move derivatives onto the test functions.

V. **Handle boundary terms** using prescribed boundary conditions.

VI. **Discretize any time derivatives** (if dealing with a time-dependent problem).

A diagram summarizing this workflow is provided below.

```plaintext
+-----------------------+

|   Strong Form PDE     |
|  (Pointwise Equation) |

+-----------+-----------+

        |

        | Multiply by test function v(x)
        v
+-----------------------+

|  Multiply by v(x)     |

+-----------+-----------+

        |

        | Integrate over domain Ω
        v
+-----------------------+

|   Integrated Form     |

+-----------+-----------+

        |

        | Integration by Parts (Transfer derivatives)
        v
+-----------------------+

| Weak Formulation with |
|   Boundary Terms      |

+-----------+-----------+

        |

        | Apply Boundary Conditions
        v
+-----------------------+

|  Final Weak Form PDE  |

+-----------------------+

```

## The Reaction-Diffusion Equation (Strong Form)

Consider the following reaction-diffusion equation defined on a spatial domain $\Omega$ and over time $t > 0$:

```math
\frac{\partial u}{\partial t} = \nabla \cdot \big(D\,\nabla u \big) - s\, u
```

where:

- $u = u(\mathbf{x}, t)$ is the state variable (for example, a chemical concentration or temperature),
- $D$ is the diffusion coefficient (which may vary with position),
- $s$ is the reaction (or source/sink) term coefficient.

This **strong form** requires that $u$ is differentiable enough to satisfy the PDE at every point in $\Omega$.

## Function Spaces for the Weak Formulation

Before deriving the weak formulation, we need to define the function spaces for the trial (solution) and test functions. These spaces are typically Sobolev spaces that require square-integrable derivatives.

### Trial Function Space

We assume that the solution $u(\mathbf{x}, t)$ belongs to the space

```math
\mathcal{S}_{t}: = \Big\{ u(\mathbf{x}, t) \;\Big|\; u(\cdot, t) \in
\mathcal{H}^{1}(\Omega) \text{ for } t > 0 \Big\}
```

where:

- $\mathcal{H}^{1}(\Omega)$ is the Sobolev space of functions with square-integrable derivatives,
- $\Gamma = \partial \Omega$ is the boundary of the domain,
- $\frac{\partial u}{\partial n} = 0$ on $\Gamma$ is the Neumann (no-flux) boundary condition. It is a *natural* condition: it is not built into the function space but is enforced weakly through the boundary term below.

### Test Function Space

The test functions are chosen from the space

$$
\mathcal{V}: = \mathcal{H}^{1}(\Omega)
$$

*Note:* Test functions are required to vanish only on parts of the boundary where a Dirichlet (essential) condition is prescribed. Here the whole boundary carries the Neumann condition, so $v$ is unrestricted on $\Gamma$; the boundary term vanishes because $\partial u/\partial n = 0$, not because $v = 0$.

## Derivation of the Weak Formulation

We now derive the weak formulation step by step.

### Multiplying by a Test Function

Multiply the strong form of the PDE by an arbitrary test function $v \in \mathcal{V}$:

```math
\frac{\partial u}{\partial t} \, v = \nabla \cdot \big(D\,\nabla u \big) \, v - s\, u\,
v
```

### Integrating Over the Domain

Integrate the above equation over the spatial domain $\Omega$:

```math
\int_{\Omega} \frac{\partial u}{\partial t}\, v \, d\omega = \int_{\Omega} \nabla \cdot
\big(D\,\nabla u \big) \, v \, d\omega - \int_{\Omega} s\, u\, v \, d\omega
```

where $d\omega$ represents the volume element.

### Applying Integration by Parts

Focus on the diffusion term. Applying the divergence theorem (integration by parts), we have:

```math
\int_{\Omega} \nabla \cdot \big(D\,\nabla u \big) \, v \,
d\omega = \underbrace{\int_{\Omega} \nabla \cdot \Big( v\,(D\,\nabla u) \Big) \, d\omega}_{\text{Surface term}} - \int_{\Omega} \nabla v \cdot \big(D\,\nabla u \big) \, d\omega
```

The surface term becomes a boundary integral:

```math
\int_{\Omega} \nabla \cdot \Big(v\,(D\,\nabla u) \Big) \, d\omega = \int_{\Gamma} v\,
D\, \frac{\partial u}{\partial n}\, d\gamma
```

with $d\gamma$ being the measure on $\Gamma$ and $\frac{\partial u}{\partial n}$ the outward normal derivative. With the imposed Neumann condition $\frac{\partial u}{\partial n} = 0$ on $\Gamma$, the boundary term vanishes:

```math
\int_{\Gamma} v\, D\, \frac{\partial u}{\partial n}\, d\gamma = 0
```

Thus, the diffusion term simplifies to:

```math
\int_{\Omega} \nabla \cdot \big(D\,\nabla u \big) \, v \, d\omega = -\int_{\Omega}
\nabla v \cdot \big(D\,\nabla u \big) \, d\omega
```

### Temporal Discretization

For a time-dependent problem, we discretize the time derivative. Using the **backward Euler scheme** at time level $n+1$ gives:

$$
\frac{\partial u}{\partial t} \approx \frac{u^{n+1} - u^{n}}{\Delta t}
$$

where:

- $u^{n+1}$ is the solution at the new time level,
- $u^{n}$ is the known solution at the previous time level,
- $\Delta t$ is the time step.

Substitute this approximation into the integrated equation:

```math
\int_{\Omega} \frac{u^{n+1} - u^{n}}{\Delta t}\, v \, d\omega = -\int_{\Omega} \nabla v
\cdot \big(D\,\nabla u^{n+1} \big) \, d\omega - \int_{\Omega} s\, u^{n+1}\, v \, d\omega
```

### Rearranging into the Final Weak Form

Rearrange the terms to isolate those involving the unknown $u^{n+1}$:

```math
\int_{\Omega} \frac{u^{n+1}}{\Delta t}\, v\, d\omega + \int_{\Omega} \nabla v \cdot
\big(D\,\nabla u^{n+1} \big) \, d\omega + \int_{\Omega} s\, u^{n+1}\, v\,
d\omega = \int_{\Omega} \frac{u^{n}}{\Delta t}\, v\, d\omega
```

It is common practice to multiply the entire equation by $\Delta t$ to simplify the appearance of the time-stepping term:

```math
\int_{\Omega} u^{n+1}\, v\, d\omega + \Delta t \int_{\Omega} D\,\nabla u^{n+1} \cdot
\nabla v\, d\omega + \Delta t \int_{\Omega} s\, u^{n+1}\, v\, d\omega = \int_{\Omega}
u^{n}\, v\, d\omega
```

This is the **final weak formulation** of the reaction-diffusion equation, ready for spatial discretization using finite element spaces.

## Visual Summary of the Derivation Process

Below is a diagram summarizing the key steps in the derivation:

```plaintext
[Strong Form PDE]
     │
     │  Multiply by v(x)
     ▼
[Weighted Equation]
     │
     │  Integrate over Ω
     ▼
[Integrated Equation]
     │
     │  Apply Integration by Parts:
     │  ──> Transfer derivative from u to v
     ▼
[Equation with Boundary Term]
     │
     │  Apply Boundary Condition:
     │  (No-flux: ∂u/∂n = 0 ⇒ Surface term = 0)
     ▼
[Simplified Integrated Equation]
     │
     │  Discretize Time (Backward Euler)
     ▼
[Time-Discretized Equation]
     │
     │  Rearrange to isolate u^(n+1)
     ▼
[Final Weak Formulation]
```

The weak formulation derived above:

- **Accommodates lower regularity:** The solution $u$ is only required to be in $\mathcal{H}^1(\Omega)$ instead of being twice differentiable.
- **Incorporates boundary conditions naturally:** The no-flux boundary condition appears as a vanishing surface term.
- **Prepares the PDE for FEM discretization:** The integral form can be approximated using finite-dimensional basis functions, leading to a system of algebraic equations that can be solved using standard numerical techniques.

## Purpose in CFD

Deriving the weak form is the first step in any FEM-based CFD solver. This note walks through the complete derivation for a reaction-diffusion PDE: multiply by a test function, integrate over the domain, apply integration by parts, handle boundary terms, and discretize in time with backward Euler. The result is a bilinear form ready for spatial discretization with finite elements. These techniques apply directly to the energy equation and scalar transport in CFD.

## Input / Output

| Aspect | Details |
| --- | --- |
| **Inputs** | Strong-form PDE ($\partial u/\partial t = \nabla\cdot(D\nabla u) - su$), diffusion coefficient $D$, reaction coefficient $s$, domain $\Omega$, Neumann boundary condition, time step $\Delta t$, previous solution $u^n$ |
| **Outputs** | Weak-form bilinear problem: find $u^{n+1} \in \mathcal{S}_t$ such that the integral equation holds for all $v \in \mathcal{V}$; after FEM discretization this becomes $K U^{n+1} = F$ |

## Related Scripts

There are no dedicated FEM weak-formulation scripts in this repository. For a practical implementation, the [FEniCS tutorial](https://fenicsproject.org/tutorial/) shows how to translate weak forms like the one derived here directly into Python code.

## Exercises

**Exercise 1.** Suppose the boundary is split as $\Gamma = \Gamma_D \cup \Gamma_N$, with $u = g$ prescribed on $\Gamma_D$ and $\partial u/\partial n = 0$ on $\Gamma_N$. How do the trial space and the test space change, and why does the boundary integral still vanish?

<details>
<summary>Answer</summary>

- Trial functions must satisfy the essential condition $u = g$ on $\Gamma_D$.
- Test functions must vanish on $\Gamma_D$: $`\mathcal{V} = \{v \in \mathcal{H}^1(\Omega) : v = 0 \text{ on } \Gamma_D\}`$.

The boundary integral $`\int_\Gamma v D\,\partial u/\partial n\,d\gamma`$ then vanishes for two different reasons. On $\Gamma_D$ it vanishes because $v = 0$, and on $\Gamma_N$ because $\partial u/\partial n = 0$.

</details>

**Exercise 2.** Replace the no-flux condition with a prescribed flux, $`D\,\partial u/\partial n = q`$ on $\Gamma$. Rederive the final backward-Euler weak form.

<details>
<summary>Answer</summary>

The boundary term no longer vanishes. It becomes $`\int_\Gamma v\,q\,d\gamma`$, so the diffusion term is $`\int_\Gamma q v\,d\gamma - \int_\Omega D\nabla u\cdot\nabla v\,d\omega`$. Following the same steps:

```math
\int_\Omega u^{n+1}v\, d\omega + \Delta t\int_\Omega D\nabla u^{n+1}\cdot\nabla v\,
d\omega + \Delta t\int_\Omega s\, u^{n+1}v\, d\omega = \int_\Omega u^n v\, d\omega +
\Delta t\int_\Gamma q^{n+1}v\, d\gamma
```

The prescribed flux appears only on the right-hand side, as a load term.

</details>

**Exercise 3.** In 1D with linear elements of length $h$ and constant $D$ and $s$, write the element mass matrix $`M^e_{ij} = \int\phi_i\phi_j\,dx`$ and the stiffness matrix $`K^e_{ij} = \int D\phi_i'\phi_j'\,dx`$. Then write the fully discrete system for $U^{n+1}$.

<details>
<summary>Answer</summary>

- $M^e$ has diagonal entries $h/3$ and off-diagonal entries $h/6$.
- $K^e$ has diagonal entries $D/h$ and off-diagonal entries $-D/h$.

After assembly, the weak form becomes

```math
\left[(1 + \Delta t\, s)M + \Delta t\, K\right]U^{n+1} = M U^n
```

The system matrix is symmetric positive definite, so a linear solve is needed at every step.

</details>

**Exercise 4.** Take $\Omega = [0,1]$ as a single linear element with $D = 1$, $s = 0$ and $\Delta t = 0.1$, starting from nodal values $U^0 = (1, 0)$. Compute $U^1$, and verify that $`\int_\Omega u_h\,dx`$ is conserved, as expected with no-flux boundaries and no reaction.

<details>
<summary>Answer</summary>

With $h = 1$, $M$ has diagonal $1/3$ and off-diagonal $1/6$, and $K$ has diagonal $1$ and off-diagonal $-1$. The system $(M + 0.1K)U^1 = MU^0$ reads

```math
\frac{13}{30}U_1 + \frac{1}{15}U_2 = \frac{1}{3},
\qquad \frac{1}{15}U_1 + \frac{13}{30}U_2 = \frac{1}{6}
```

Adding the equations gives $U_1 + U_2 = 1$. Subtracting gives $U_1 - U_2 = 5/11$. So $U^1 = (8/11, 3/11) = (0.727, 0.273)$.

For one linear element, $`\int u_h\,dx = (U_1 + U_2)/2`$, which is $0.5$ both before and after the step. Mass is conserved because every row of $K$ sums to zero.

</details>

**Exercise 5.** Show that the backward-Euler weak form is unconditionally stable in the $L^2$ norm when $D \ge 0$ and $s \ge 0$. Hint: choose $v = u^{n+1}$.

<details>
<summary>Answer</summary>

With $v = u^{n+1}$,

```math
\| u^{n+1}\|^2 + \Delta t\int_\Omega D|\nabla u^{n+1}|^2 d\omega + \Delta t\int_\Omega
s\,(u^{n+1})^2 d\omega = (u^n, u^{n+1}) \le \| u^n\|\,\| u^{n+1}\|
```

The last step uses the Cauchy–Schwarz inequality. The two integrals on the left are non-negative, so $`\|u^{n+1}\|^2 \le \|u^n\|\,\|u^{n+1}\|`$, which gives $`\|u^{n+1}\| \le \|u^n\|`$ for any $\Delta t > 0$. The discrete solution can never grow, unlike the explicit scheme with its $\Delta t \le h^2/(2D)$ limit.

</details>

## References

- S. C. Brenner, L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Springer, 2008.
- M. G. Larson, F. Bengzon, *The Finite Element Method: Theory, Implementation, and Applications*, Springer, 2013.
- V. Thomée, *Galerkin Finite Element Methods for Parabolic Problems*, 2nd ed., Springer, 2006.
