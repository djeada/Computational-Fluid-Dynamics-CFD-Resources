# Turbulence Modeling in OpenFOAM

This guide covers the theory, setup, and practical usage of turbulence models available in OpenFOAM. Choosing the right turbulence model and configuring it correctly is one of the most important decisions in any CFD simulation.

## Table of Contents

- [Overview of Turbulence Approaches](#overview-of-turbulence-approaches)
- [RANS Models](#rans-models)
- [LES Models](#les-models)
- [Setting Up Turbulence in OpenFOAM](#setting-up-turbulence-in-openfoam)
- [Inlet Boundary Conditions for Turbulence](#inlet-boundary-conditions-for-turbulence)
- [Wall Treatment and y+ Requirements](#wall-treatment-and-y-requirements)
- [Choosing a Turbulence Model](#choosing-a-turbulence-model)
- [Worked Example: Turbulent Pipe Flow](#worked-example-turbulent-pipe-flow)
- [Monitoring and Validating Turbulence Results](#monitoring-and-validating-turbulence-results)

## Overview of Turbulence Approaches

| Approach | Description | Cost | Accuracy |
|----------|-------------|------|----------|
| **DNS** | Resolves all scales; no model needed | Very high | Exact (within numerical error) |
| **LES** | Resolves large eddies; models small scales | High | High for unsteady flows |
| **RANS** | Models all turbulent fluctuations | Low | Good for mean flow quantities |
| **Hybrid (DES/DDES)** | RANS near walls, LES away from walls | Medium–High | Good balance of cost and accuracy |

For most engineering applications, **RANS** models are the standard starting point. Switch to **LES** when you need to capture time-dependent flow features like vortex shedding, mixing, or acoustics.

## RANS Models

### k-epsilon Family

The k-ε model solves transport equations for turbulent kinetic energy (k) and its dissipation rate (ε).

#### Standard k-ε

```
Model name in OpenFOAM: kEpsilon
Strengths: Robust, well-validated for free-shear flows
Weaknesses: Poor for separated flows, adverse pressure gradients
Best for: Pipe flows, jets, mixing layers, far-field flows
```

#### Realizable k-ε

```
Model name in OpenFOAM: realizableKE
Strengths: Better separation prediction than standard k-ε
Weaknesses: Still limited in strong adverse pressure gradients
Best for: Recirculating flows, rotating flows, jets with strong curvature
```

#### RNG k-ε

```
Model name in OpenFOAM: RNGkEpsilon
Strengths: Improved for swirling and strained flows
Weaknesses: More complex, marginal improvement for simple flows
Best for: Swirl-dominated flows, transitional flows
```

### k-omega Family

The k-ω model solves for turbulent kinetic energy (k) and specific dissipation rate (ω).

#### Standard k-ω (Wilcox)

```
Model name in OpenFOAM: kOmega
Strengths: Better near-wall behavior than k-ε, no wall functions needed
Weaknesses: Sensitive to free-stream ω values
Best for: Boundary layer flows, low-Re applications
```

#### k-ω SST (Shear Stress Transport)

```
Model name in OpenFOAM: kOmegaSST
Strengths: Best general-purpose RANS model; k-ω near walls, k-ε in free stream
Weaknesses: Slightly more expensive than k-ε
Best for: Almost everything — external aero, turbomachinery, heat transfer, industrial flows
```

The **k-ω SST** model by Menter (1994) is the most widely recommended RANS model for general-purpose CFD. If in doubt, start here.

### Spalart-Allmaras

```
Model name in OpenFOAM: SpalartAllmaras
Strengths: One-equation model, cheap, good for attached boundary layers
Weaknesses: Poor for complex separated flows
Best for: External aerodynamics (especially aerospace), simple geometries
```

### Reynolds Stress Models (RSM)

```
Model name in OpenFOAM: LRR or SSG
Strengths: Accounts for anisotropy of turbulence; 7 transport equations
Weaknesses: Expensive, harder to converge, needs careful initialization
Best for: Strongly anisotropic flows (swirl, secondary flows, impinging jets)
```

## LES Models

### Smagorinsky

```
Model name in OpenFOAM: Smagorinsky
Strengths: Simple, well-understood, low computational overhead
Weaknesses: Too dissipative near walls, constant Cs must be tuned
Best for: Free-shear flows, rough estimates of unsteady behavior
```

### Dynamic Smagorinsky (Germano)

```
Model name in OpenFOAM: dynamicKEqn
Strengths: Automatically adjusts model constant based on local flow
Weaknesses: More expensive, can be unstable
Best for: Flows with varying turbulence intensity, wall-bounded LES
```

### WALE (Wall-Adapting Local Eddy-viscosity)

```
Model name in OpenFOAM: WALE
Strengths: Correct near-wall behavior without dynamic procedure
Weaknesses: Slightly more complex than Smagorinsky
Best for: Wall-bounded flows, when you need good near-wall LES behavior
```

### One-Equation Eddy Viscosity (kEqn)

```
Model name in OpenFOAM: kEqn
Strengths: More physically based than Smagorinsky
Weaknesses: Additional transport equation to solve
Best for: Recirculating flows, moderate-Re LES
```

## Setting Up Turbulence in OpenFOAM

### Step 1: Select a Turbulence Model

In `constant/momentumTransport` (OpenFOAM v11+) or `constant/turbulenceProperties` (earlier versions):

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      momentumTransport;
}

simulationType  RAS;

RAS
{
    model           kOmegaSST;
    turbulence      on;
    printCoeffs     on;
}
```

For LES:

```cpp
simulationType  LES;

LES
{
    model           WALE;
    turbulence      on;
    printCoeffs     on;
    delta           cubeRootVol;

    cubeRootVolCoeffs
    {
        deltaCoeff      1;
    }
}
```

### Step 2: Set Initial/Boundary Conditions

For a k-ω SST simulation, you need fields for `k`, `omega`, and `nut` in the `0/` directory.

#### 0/k

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      k;
}

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0.06;

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform 0.06;
    }
    outlet
    {
        type            zeroGradient;
    }
    walls
    {
        type            kqRWallFunction;
        value           uniform 0.06;
    }
}
```

#### 0/omega

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      omega;
}

dimensions      [0 0 -1 0 0 0 0];

internalField   uniform 400;

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform 400;
    }
    outlet
    {
        type            zeroGradient;
    }
    walls
    {
        type            omegaWallFunction;
        value           uniform 400;
    }
}
```

#### 0/nut

```cpp
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      nut;
}

dimensions      [0 2 -1 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            calculated;
        value           uniform 0;
    }
    outlet
    {
        type            calculated;
        value           uniform 0;
    }
    walls
    {
        type            nutkWallFunction;
        value           uniform 0;
    }
}
```

### Step 3: Configure the Solver

Use a RANS-capable solver such as `simpleFoam` (steady) or `pimpleFoam` (transient):

```cpp
// system/fvSchemes - divSchemes section
divSchemes
{
    default         none;
    div(phi,U)      bounded Gauss linearUpwind grad(U);
    div(phi,k)      bounded Gauss upwind;
    div(phi,omega)  bounded Gauss upwind;
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}
```

```cpp
// system/fvSolution - add solvers for k and omega
solvers
{
    k
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-06;
        relTol          0.1;
    }
    omega
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-06;
        relTol          0.1;
    }
}
```

## Inlet Boundary Conditions for Turbulence

Estimating turbulence quantities at the inlet is critical. Common approaches:

### From Turbulence Intensity and Length Scale

```
k = 1.5 * (U * I)^2
epsilon = C_mu^0.75 * k^1.5 / l
omega = k^0.5 / (C_mu^0.25 * l)
```

Where:
- `I` = turbulence intensity (typically 0.01–0.10 for external flows, 0.05–0.20 for internal)
- `l` = turbulent length scale (typically 0.07 × hydraulic diameter for pipes)
- `C_mu` = 0.09

### Example Calculation

```python
import numpy as np

U = 10.0          # m/s inlet velocity
I = 0.05          # 5% turbulence intensity
D_h = 0.1         # m hydraulic diameter
C_mu = 0.09

l = 0.07 * D_h                           # turbulent length scale
k = 1.5 * (U * I)**2                     # turbulent kinetic energy
epsilon = C_mu**0.75 * k**1.5 / l         # dissipation rate
omega = k**0.5 / (C_mu**0.25 * l)         # specific dissipation rate
nut = k / omega                            # turbulent viscosity

print(f"k       = {k:.4f} m²/s²")
print(f"epsilon = {epsilon:.4f} m²/s³")
print(f"omega   = {omega:.2f} 1/s")
print(f"nut     = {nut:.6f} m²/s")
```

### OpenFOAM Convenience Boundary Conditions

Instead of computing values manually, OpenFOAM offers derived inlet conditions:

```cpp
// 0/k
inlet
{
    type            turbulentIntensityKineticEnergyInlet;
    intensity       0.05;       // 5% turbulence intensity
    value           uniform 1;  // placeholder
}

// 0/omega
inlet
{
    type            turbulentMixingLengthFrequencyInlet;
    mixingLength    0.007;      // turbulent length scale in meters
    value           uniform 1;  // placeholder
}
```

## Wall Treatment and y+ Requirements

### Wall Functions (y+ ≈ 30–300)

Use wall functions when your mesh cannot resolve the viscous sublayer:

| Field | Wall Function |
|-------|--------------|
| `nut` | `nutkWallFunction` |
| `k` | `kqRWallFunction` |
| `omega` | `omegaWallFunction` |
| `epsilon` | `epsilonWallFunction` |

### Resolved Walls (y+ ≈ 1)

When using low-Re models or when wall resolution is critical:

| Field | Boundary Type |
|-------|--------------|
| `nut` | `nutLowReWallFunction` or `fixedValue uniform 0` |
| `k` | `fixedValue uniform 0` |
| `omega` | `omegaWallFunction` (automatic switching) |

### Checking y+ After Simulation

```bash
# Calculate and write y+ field
simpleFoam -postProcess -func yPlus

# Or for transient solvers
pimpleFoam -postProcess -func yPlus
```

Then visualize the `yPlus` field in ParaView to check that your mesh meets the model requirements.

## Choosing a Turbulence Model

### Decision Flowchart

```
Is the flow steady-state with no separation?
├── Yes → Spalart-Allmaras or k-ε (standard)
└── No
    ├── Is separation important?
    │   ├── Mild separation → k-ω SST
    │   └── Massive separation → LES or DES
    ├── Is near-wall accuracy critical?
    │   ├── Yes → k-ω SST (with y+ ≈ 1)
    │   └── No → k-ε with wall functions
    ├── Is the flow swirling or highly anisotropic?
    │   └── Yes → Reynolds Stress Model (LRR/SSG)
    └── Do you need time-accurate unsteady results?
        ├── Yes, all scales → LES (WALE or dynamic kEqn)
        └── Yes, large scales only → DES/DDES
```

### Quick Reference Table

| Scenario | Recommended Model | y+ Target |
|----------|------------------|-----------|
| Simple pipe/duct flow | k-ε or k-ω SST | 30–300 (wall functions) |
| External aerodynamics | k-ω SST or SA | ~1 (resolved) |
| Turbomachinery | k-ω SST | ~1 |
| Heat transfer (wall-dominated) | k-ω SST | ~1 |
| Mixing/combustion | realizable k-ε or LES | Depends on model |
| Free-shear flows (jets, wakes) | k-ε or LES | Not wall-limited |
| Vortex shedding | LES or DES | ~1 near walls |
| Swirling flows | RSM or LES | ~1 |

## Worked Example: Turbulent Pipe Flow

A fully developed turbulent pipe flow at Re = 44,000 (based on bulk velocity and diameter).

### Setup Parameters

```
D = 0.1 m          (pipe diameter)
L = 2.0 m          (pipe length, 20D)
U_bulk = 6.6 m/s   (bulk velocity)
nu = 1.5e-5 m²/s   (air at 20°C)
Re = U_bulk * D / nu = 44,000
```

### Turbulence Inlet Values

```python
U = 6.6
I = 0.04            # 4% for fully developed pipe flow
D_h = 0.1
l = 0.07 * D_h      # = 0.007 m

k = 1.5 * (U * I)**2          # = 0.10454 m²/s²
omega = k**0.5 / (0.09**0.25 * l)  # ≈ 84.4 1/s
```

### constant/momentumTransport

```cpp
simulationType  RAS;

RAS
{
    model           kOmegaSST;
    turbulence      on;
    printCoeffs     on;
}
```

### Running and Validating

```bash
# Generate mesh (ensure y+ ≈ 30–50 at walls for wall functions)
blockMesh
checkMesh

# Run steady-state solver
simpleFoam > log.simpleFoam 2>&1

# Check y+
simpleFoam -postProcess -func yPlus

# Extract velocity profile along diameter
sample
```

Compare the velocity profile against the DNS data of El Khoury et al. (2013) or the classical log-law:

```
u+ = (1/κ) * ln(y+) + B
```

where κ ≈ 0.41 and B ≈ 5.2.

## Monitoring and Validating Turbulence Results

### Key Checks

1. **Residuals**: Turbulence residuals (`k`, `omega`/`epsilon`) should drop at least 3–4 orders of magnitude.
2. **y+ distribution**: Verify that wall-adjacent cells match your model requirements.
3. **Turbulent viscosity ratio**: `nut/nu` should typically be 1–1000 in the bulk flow; values > 10,000 suggest problems.
4. **Physical plausibility**: Check that k > 0 everywhere and that turbulence levels match expectations.

### Extracting Turbulent Viscosity Ratio

```bash
# Post-process to compute and write turbulent viscosity ratio
simpleFoam -postProcess -func 'turbulenceFields(R, devReff, L, I, nut, nuEff, k, epsilon, omega)'
```

### Common Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `k` goes negative | Poor initialization or mesh | Initialize with larger k; refine mesh near walls |
| `omega` unbounded | Missing or wrong wall function | Check `0/omega` wall BC; use `omegaWallFunction` |
| High `nut/nu` (>10,000) | Poor mesh or wrong BCs | Check y+; refine mesh; check inlet values |
| Residuals plateau | Mesh quality or numerics | Improve mesh; try GAMG for pressure; adjust relaxation |
| Non-physical separation | Wrong model for the flow | Switch to k-ω SST; ensure mesh resolves gradients |

## Resources

- [OpenFOAM Turbulence Models Guide](https://www.openfoam.com/documentation/guides/latest/doc/guide-turbulence.html)
- Menter, F.R. (1994). "Two-equation eddy-viscosity turbulence models for engineering applications." AIAA Journal, 32(8), 1598-1605.
- Wilcox, D.C. (2006). *Turbulence Modeling for CFD*. DCW Industries.
- Pope, S.B. (2000). *Turbulent Flows*. Cambridge University Press.
