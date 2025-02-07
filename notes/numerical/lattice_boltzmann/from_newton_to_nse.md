# From Newton to Navier-Stokes

Fluid dynamics spans multiple scales. At the microscopic level, Newton's laws (or molecular dynamics, MD) govern the behavior of individual particles. At the macroscopic level, fluids are described by the Navier-Stokes equations (NSE). Bridging these scales is essential for both physical insight and computational efficiency. The **Lattice-Boltzmann Method (LBM)** provides this bridge by adopting a mesoscopic approach that leverages a simplified kinetic model. LBM recovers the NSE while retaining key microscopic insights, making it an appealing alternative to traditional computational fluid dynamics (CFD).


## 1. Introduction: Why a Mesoscopic Approach?

Traditional CFD methods solve the continuum Navier-Stokes equations directly, but they may obscure the underlying physics present at the molecular level. A mesoscopic approach, such as LBM, operates between these extremes by:
- **Averaging Microscopic Behavior:** Instead of tracking each molecule, we average over small volumes where molecular fluctuations are smoothed out.
- **Retaining Key Kinetic Details:** Essential kinetic information is preserved, enabling the recovery of macroscopic behavior.
- **Enhancing Computational Efficiency:** LBM is inherently parallel and can handle complex boundaries with relative ease.

This approach not only offers computational advantages but also deepens our understanding of how macroscopic fluid phenomena emerge from microscopic interactions.

---

## 2. The Lattice-Boltzmann Approach

The Lattice-Boltzmann method is based on a discrete version of the Boltzmann kinetic equation. It does not solve the full Boltzmann equation directly; instead, it employs a simplified, discretized version that is designed to recover the Navier-Stokes equations in the macroscopic limit.

### 2.1. Transition Diagram: From Microscopic to Macroscopic

The following diagram outlines the cascade of models from fundamental molecular dynamics to continuum fluid dynamics:

```
+------------+        +-------------+          +---------------+               +-------+
| Newton/MD  +------->+  Boltzmann  +--------->+ Navier-Stokes | <-----------> +  CFD  +
+------------+        +-------------+          +---------------+               +-------+
      |                      |                         ^
      v                      v                         |
+------------+        +----------------+               |
| Lattice    +------->+ Lattice        +---------------+
| Gas        |        | Boltzmann      |
+------------+        +----------------+
```

- **Newton/MD:** The microscopic laws governing individual particles.
- **Boltzmann Equation:** A statistical description of particle distributions.
- **Lattice Boltzmann:** A mesoscopic model that discretizes the Boltzmann equation on a lattice.
- **Navier-Stokes & CFD:** The macroscopic continuum equations and their numerical solution.

This flow illustrates how the Lattice-Boltzmann method serves as the crucial intermediary, combining microscopic fidelity with macroscopic efficiency.

---

## 3. The Probability Distribution Function (PDF)

At the heart of the LBM lies the **probability distribution function** \( f(\xi, x, t) \). This function encapsulates the statistical information about particles at a mesoscopic scale.

### 3.1. Simplifying Microscopic Details

The objective is to remove unnecessary microscopic details while retaining the essential physics needed to describe macroscopic fluid behavior. This is achieved by averaging over a volume \( \ell_{\text{av}} \) that satisfies

\[
\ell_{\text{mfp}} \ll \ell_{\text{av}} \ll \ell,
\]

where:
- \( \ell_{\text{mfp}} \) is the mean free path (the typical distance a molecule travels between collisions),
- \( \ell \) is the macroscopic length scale.

The **distribution function** \( f(\xi, x, t) \):
- **Definition:** Describes the density of molecules with velocity \( \xi \) at position \( x \) and time \( t \).
- **Kinetic Link:** The molecular velocity is defined as \( \xi = \frac{dx}{dt} \).

In essence, \( f(\xi, x, t) \, d\xi \, dx \) represents the number of molecules in a small velocity range \( d\xi \) and spatial element \( dx \).

### 3.2. Visualizing Molecular Averaging

Consider the following schematic representation of molecules (dots) distributed within a small control volume. The averaging process smooths out microscopic fluctuations while capturing overall behavior:

```
+------------------------------------------------+
|   *    .         *     .      *               |
|   .  *    .          .   *         .          |
|  *     .       *         .     *              |
|        .         . *         .    *           |
|   *          .         *         .            |
|         *        .           *         .       |
+------------------------------------------------+
```

*This diagram shows the random positions of molecules. Averaging over such a control volume yields a continuum description that feeds into the LBM framework.*

---

## 4. Advantages of the Lattice-Boltzmann Method

The LBM offers several compelling benefits compared to conventional CFD approaches:

1. **Inherent Parallelism:**  
   LBM’s algorithm naturally partitions over a lattice, making it highly efficient on parallel computing architectures.

2. **Simplicity in Implementation:**  
   The underlying algorithm is straightforward, reducing coding complexity and facilitating rapid development.

3. **Flexibility with Complex Boundaries:**  
   Complex geometries and boundary conditions are easier to handle compared to traditional CFD methods.

4. **Physical Transparency:**  
   By working at the mesoscopic level, LBM retains a clear connection to the underlying kinetic theory, providing physical insights that can be obscured in fully macroscopic formulations.

---

## 5. Macroscopic Properties via Moments of \( f(\xi, x, t) \)

The power of the LBM lies in its ability to recover macroscopic fluid properties by taking moments of the probability distribution function \( f(\xi, x, t) \).

### 5.1. Important Properties

1. **Normalization (Total Mass):**
   \[
   \int d^3\xi \int d^3x \, f(\xi, x, t) = M(t),
   \]
   where \( M(t) \) is the total mass.

2. **Fluid Density:**
   \[
   \int d^3\xi \, f(\xi, x, t) = \rho(x, t),
   \]
   which defines the density at point \( x \) and time \( t \).

3. **Momentum Density:**
   \[
   \int d^3\xi \, \xi\, f(\xi, x, t) = \rho(x, t)\, u(x, t),
   \]
   where \( u(x, t) \) is the macroscopic fluid velocity.

4. **Pressure and Stress Tensor:**
   Higher moments (involving \( \xi \otimes \xi \)) provide information about the pressure and viscous stresses in the fluid. Although the exact expressions are more involved, they underpin the recovery of the Navier-Stokes equations from the kinetic model.

### 5.2. Comprehensive Role of \( f(\xi, x, t) \)

The function \( f(\xi, x, t) \) holds all local information about the fluid:
- **Zeroth Moment:** Yields the density.
- **First Moment:** Gives the momentum.
- **Second Moment:** Relates to the pressure and stress tensor.

Thus, macroscopic properties are obtained as **moments** of the mesoscopic distribution, effectively bridging the scales.

![Probability Distribution Function](https://github.com/djeada/Computational-Fluid-Dynamics-CFD-Resources/assets/37275728/9821d7ff-d499-45a9-8fdd-3e4d73e6efb9)
*Figure: The probability distribution function \( f(\xi, x, t) \) encapsulates the complete mesoscopic description of the fluid, from which macroscopic properties emerge.*






