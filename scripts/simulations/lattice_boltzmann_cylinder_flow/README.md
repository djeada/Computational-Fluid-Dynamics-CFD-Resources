# Notes on Lattice Boltzmann Method

## Overview
- Lattice Boltzmann method: A computational fluid dynamics approach.
- Used to numerically solve incompressible, time-dependent Navier-Stokes equations.
- Easily represents complex physical phenomena (e.g., multiphase flows, chemical interactions).
- Originates from molecular description of a fluid, can incorporate physical terms from molecular interaction knowledge.
- Valuable in fundamental research and industrial problems due to efficiency and convenience.

## Origin of the Method
- Lattice Boltzmann seen as numerical solver of Boltzmann equation.
- Boltzmann equation describes space-time dynamics of probability distribution function, defined in 6-dimensional phase space.
- Covers more physical phenomena than Navier-Stokes equation, not subject to time scales separation, describes fluids in non-hydrodynamic regimes.
- Captures transport phenomena like friction, diffusion, and temperature transport, deriving corresponding transport coefficients.
- Lattice Boltzmann evolved from Cellular Automata models, describing the evolution of discrete states.
- Cellular Automata represents position and velocity of "mesoscopic" particles.
- Lattice Boltzmann models simulate dynamics of corresponding discrete Boltzmann equation.

## Why Lattice Boltzmann?
- Different from classical CFD in theory, code implementation, and application.
- Advantage: efficiency. Designed to run on high performance hardware and accommodate complex physics or sophisticated algorithms.
- Lattice Boltzmann allows solving previously unapproachable problems or problems with insufficient accuracy.
- Typical achievements: data pre-processing and mesh generation, parallel data analysis, post-processing and evaluation, fully resolved multi-phase flow, flow through complex geometries and porous media, complex coupled flow with heat transfer and chemical reactions.
- Hybrid modeling approach: mesh based but also inherits aspects of a particle based method. Can be coupled with embedded particle methods.

## Lattice Boltzmann and High Performance Computing
- Lattice Boltzmann seems resource consuming compared to classical CFD as it requires more memory for the discrete probability distribution functions.
- This is compensated by outstanding computational efficiency, thanks to explicit formulation and exact advection operator.
- Well suited for computations on a parallel architecture, even with slow interconnection network.
- Works well with other types of high performance hardware like General Purpose Graphics Processing Units (GPGPUs).
