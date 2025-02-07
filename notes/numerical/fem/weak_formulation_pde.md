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

$$\frac{\partial u}{\partial t} = \nabla \cdot \big( D, \nabla u \big) - s, u$$

where:

- $u = u(\mathbf{x}, t)$ is the state variable (for example, a chemical concentration or temperature),
- $D$ is the diffusion coefficient (which may vary with position),
- $s$ is the reaction (or source/sink) term coefficient.

This **strong form** requires that $u$ is differentiable enough to satisfy the PDE at every point in $\Omega$.


## Function Spaces for the Weak Formulation

Before deriving the weak formulation, we need to define the function spaces for the trial (solution) and test functions. These spaces are typically Sobolev spaces that require square-integrable derivatives.

### Trial Function Space

We assume that the solution $u(\mathbf{x}, t)$ belongs to the space

$$\mathcal{S}_{t} := \Big\{ u(\mathbf{x}, t) ,\Big|, u \in \mathcal{H}^{1}(\Omega) \text{ for } t>0,  \frac{\partial u}{\partial n} = 0 \text{ on } \Gamma \Big\}$$

where:

- $\mathcal{H}^{1}(\Omega)$ is the Sobolev space of functions with square-integrable derivatives,
- $\Gamma = \partial \Omega$ is the boundary of the domain,
- $\frac{\partial u}{\partial n} = 0$ represents a Neumann (no-flux) boundary condition.

### Test Function Space

The test functions are chosen from the space

$$\mathcal{V} := \Big\{ v(\mathbf{x}) ,\Big|, v \in \mathcal{H}^{1}(\Omega),  v = 0 \text{ on } \Gamma \Big\}$$

*Note:* The homogeneous condition $v = 0$ on $\Gamma$ is often imposed to make sure that the boundary contributions vanish when integration by parts is applied.

## Derivation of the Weak Formulation

We now derive the weak formulation step by step.

### Multiplying by a Test Function

Multiply the strong form of the PDE by an arbitrary test function $v \in \mathcal{V}$:

$$\frac{\partial u}{\partial t} , v = \nabla \cdot \big( D, \nabla u \big) , v - s, u, v$$

### Integrating Over the Domain

Integrate the above equation over the spatial domain $\Omega$:

$$\int_{\Omega} \frac{\partial u}{\partial t}, v , d\omega = \int_{\Omega} \nabla \cdot \big( D, \nabla u \big) , v , d\omega - \int_{\Omega} s, u, v , d\omega$$

where $d\omega$ represents the volume element.

### Applying Integration by Parts

Focus on the diffusion term. Applying the divergence theorem (integration by parts), we have:

$$\int_{\Omega} \nabla \cdot \big( D, \nabla u \big) , v , d\omega = \underbrace{\int_{\Omega} \nabla \cdot \Big( v, (D, \nabla u) \Big) , d\omega}_{\text{Surface term}} - \int_{\Omega} \nabla v \cdot \big( D, \nabla u \big) , d\omega$$

The surface term becomes a boundary integral:

$$\int_{\Omega} \nabla \cdot \Big( v, (D, \nabla u) \Big) , d\omega = \int_{\Gamma} v, D, \frac{\partial u}{\partial n}, d\gamma$$

with $d\gamma$ being the measure on $\Gamma$ and $\frac{\partial u}{\partial n}$ the outward normal derivative. With the imposed Neumann condition $\frac{\partial u}{\partial n} = 0$ on $\Gamma$, the boundary term vanishes:

$$\int_{\Gamma} v, D, \frac{\partial u}{\partial n}, d\gamma = 0$$

Thus, the diffusion term simplifies to:

$$\int_{\Omega} \nabla \cdot \big( D, \nabla u \big) , v , d\omega = - \int_{\Omega} \nabla v \cdot \big( D, \nabla u \big) , d\omega$$

### Temporal Discretization

For a time-dependent problem, we discretize the time derivative. Using the **backward Euler scheme** at time level $n+1$ gives:

$$\frac{\partial u}{\partial t} \approx \frac{u^{n+1} - u^{n}}{\Delta t}$$

where:

- $u^{n+1}$ is the solution at the new time level,
- $u^{n}$ is the known solution at the previous time level,
- $\Delta t$ is the time step.

Substitute this approximation into the integrated equation:

$$\int_{\Omega} \frac{u^{n+1} - u^{n}}{\Delta t}, v , d\omega = - \int_{\Omega} \nabla v \cdot \big( D, \nabla u^{n+1} \big) , d\omega - \int_{\Omega} s, u^{n+1}, v , d\omega$$

### Rearranging into the Final Weak Form

Rearrange the terms to isolate those involving the unknown $u^{n+1}$:

$$\int_{\Omega} \frac{u^{n+1}}{\Delta t}, v, d\omega + \int_{\Omega} \nabla v \cdot \big( D, \nabla u^{n+1} \big) , d\omega + \int_{\Omega} s, u^{n+1}, v, d\omega = \int_{\Omega} \frac{u^{n}}{\Delta t}, v, d\omega$$

It is common practice to multiply the entire equation by $\Delta t$ to simplify the appearance of the time-stepping term:

$$\int_{\Omega} u^{n+1}, v, d\omega + \Delta t, \int_{\Omega} D, \nabla u^{n+1} \cdot \nabla v, d\omega + \Delta t, \int_{\Omega} s, u^{n+1}, v, d\omega = \int_{\Omega} u^{n}, v, d\omega$$

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
