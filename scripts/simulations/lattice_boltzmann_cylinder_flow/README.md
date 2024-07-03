# Lattice Boltzmann Cylinder Flow Simulation

This project simulates the flow around a cylinder using the Lattice Boltzmann method, a powerful approach in computational fluid dynamics.

## Demonstration

Watch the Lattice Boltzmann Cylinder Flow Simulation in action:

[![Lattice Boltzmann Cylinder Flow Simulation](https://i9.ytimg.com/vi/Jzsxy2BsQRM/mqdefault.jpg?sqp=CMSXlrQG-oaymwEoCMACELQB8quKqQMcGADwAQH4AbYIgAL6DYoCDAgAEAEYYCATKH8wDw==&rs=AOn4CLDbqZndaVyMLoKIe0VMTCGB6TlvrQ)](https://youtube.com/shorts/mOMWcGnXtFQ)

## Overview

- **Lattice Boltzmann Method**: A computational fluid dynamics approach used to numerically solve incompressible, time-dependent Navier-Stokes equations.
- **Complex Phenomena**: Represents complex physical phenomena such as multiphase flows and chemical interactions.
- **Molecular Origin**: Originates from the molecular description of fluids and incorporates physical terms from molecular interactions.
- **Efficiency and Convenience**: Highly valuable in both fundamental research and industrial applications due to its efficiency and ease of use.

## Origin of the Method

- **Boltzmann Equation**: Lattice Boltzmann method is seen as a numerical solver of the Boltzmann equation, which describes the space-time dynamics of probability distribution functions in a 6-dimensional phase space.
- **Physical Phenomena**: Captures more physical phenomena than the Navier-Stokes equation, including non-hydrodynamic regimes and various transport phenomena like friction, diffusion, and temperature transport.
- **Cellular Automata**: Evolved from Cellular Automata models that describe the evolution of discrete states representing the position and velocity of "mesoscopic" particles.
- **Discrete Boltzmann Equation**: Lattice Boltzmann models simulate the dynamics of the corresponding discrete Boltzmann equation.

## Why Lattice Boltzmann?

- **Theoretical and Practical Differences**: Differs from classical CFD in theory, code implementation, and application.
- **Efficiency**: Designed for high-performance hardware, accommodating complex physics and sophisticated algorithms.
- **Complex Problem Solving**: Allows solving previously unapproachable problems or those with insufficient accuracy.
- **Achievements**: Includes data pre-processing, mesh generation, parallel data analysis, post-processing, fully resolved multi-phase flow, flow through complex geometries, and coupled flow with heat transfer and chemical reactions.
- **Hybrid Approach**: Combines mesh-based and particle-based methods, allowing coupling with embedded particle methods.

## Lattice Boltzmann and High Performance Computing

- **Resource Consumption**: Requires more memory for the discrete probability distribution functions compared to classical CFD.
- **Computational Efficiency**: Compensated by explicit formulation and exact advection operator, making it well-suited for parallel architectures and high-performance hardware like General Purpose Graphics Processing Units (GPGPUs).
