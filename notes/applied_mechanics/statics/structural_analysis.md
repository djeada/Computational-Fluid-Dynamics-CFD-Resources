# Structural Analysis

Structural analysis is the systematic determination of the effects of loads on physical structures. It provides the analytical framework for predicting how structures respond to applied forces, enabling engineers to design safe and efficient load-bearing systems across civil, mechanical, and aerospace engineering.

## Introduction to Structural Systems

A **structure** is an assembly of members connected together to support loads and transmit them safely to the ground or other supports. The primary goals of structural analysis are:
- Determine support reactions
- Find internal forces (axial, shear, bending moment) in each member
- Assess deformations and displacements
- Verify that stresses remain within allowable limits

## Types of Structures

### Beams

Beams are members subjected primarily to transverse loads and bending:
- **Simply supported beam**: Supported by a pin and a roller
- **Cantilever beam**: Fixed at one end, free at the other
- **Overhanging beam**: Extends beyond one or both supports
- **Continuous beam**: Spans over more than two supports (statically indeterminate)

### Trusses

Trusses consist of straight members connected at joints, loaded only at the joints:
- Members carry purely axial forces (tension or compression)
- Connections are idealized as frictionless pins
- Self-weight of members is typically neglected or applied at the joints

### Frames

Frames are structures with at least one multi-force member:
- Members can carry axial force, shear, and bending moment simultaneously
- Connections may be rigid or pinned
- Common in buildings, bridges, and machinery

### Arches

Arches are curved structures that transfer loads primarily through compression:
- **Three-hinged arch**: Statically determinate with pins at supports and crown
- **Two-hinged arch**: One degree of indeterminacy
- **Fixed arch**: Three degrees of indeterminacy

The horizontal thrust $H$ in a three-hinged parabolic arch under uniform load $w$ is:

$$H = \frac{wL^2}{8h}$$

where $L$ is the span and $h$ is the rise.

### Cables

Cables are flexible members that carry loads in pure tension:
- Under a uniform load along the horizontal, a cable takes a **parabolic** shape
- Under its own weight (catenary loading), the shape is a **catenary curve**

The equation of a parabolic cable with sag $h$ and span $L$ is:

$$y = \frac{4h}{L^2}x^2$$

The maximum tension occurs at the supports and the minimum tension at the lowest point.

## Method of Analysis Overview

### Equilibrium Method (Statics)

For statically determinate structures, equilibrium equations alone suffice:
$$\sum F_x = 0, \quad \sum F_y = 0, \quad \sum M = 0$$

This is the foundation for analyzing determinate beams, trusses, and frames.

### Compatibility and Force Methods

For statically indeterminate structures, additional equations based on geometric compatibility of deformations are required:

$$\delta_{total} = \delta_{load} + R \cdot \delta_{redundant} = 0$$

where $R$ is the redundant reaction and $\delta$ represents displacements.

### Stiffness Method

The stiffness (displacement) method relates forces to displacements through the stiffness matrix:

$$\mathbf{F} = \mathbf{K}\mathbf{d}$$

where $\mathbf{K}$ is the global stiffness matrix and $\mathbf{d}$ is the displacement vector. This method is the basis for modern finite element analysis.

## Idealization and Modeling

### Modeling Assumptions

Real structures are idealized through simplifying assumptions:
- **Supports**: Classified as pins, rollers, or fixed based on the degree of restraint
- **Connections**: Treated as perfectly rigid or perfectly pinned
- **Members**: Assumed to be straight, prismatic (uniform cross-section), and made of linearly elastic material
- **Loading**: Concentrated forces, distributed loads, or moments applied at specific locations

### Load Types

| Load Type | Description | Example |
|---|---|---|
| Dead load | Permanent, self-weight | Weight of beams, slabs |
| Live load | Variable, occupancy-related | People, furniture |
| Wind load | Lateral pressure from wind | Pressure on building facades |
| Seismic load | Inertia forces from ground motion | Earthquake-induced forces |
| Thermal load | Forces from temperature changes | Expansion of bridge decks |

## Load Paths and Load Transfer

### Concept of Load Paths

A **load path** is the route through which an applied force travels from the point of application to the final support (foundation). Every load must have a continuous and complete path to the ground.

### Tributary Area Method

For distributed systems such as floor slabs, the load carried by each beam is estimated using the tributary area:

$$P_{beam} = w \times A_{tributary}$$

where $w$ is the load per unit area and $A_{tributary}$ is the area of floor supported by that beam.

### Hierarchical Load Transfer

In a typical building structure, loads transfer through the following hierarchy:
1. **Slab** → carries floor loads
2. **Beams** → receive loads from the slab
3. **Girders** → receive loads from beams
4. **Columns** → receive loads from girders
5. **Foundations** → transfer column loads to the soil

## Influence Lines

### Concept

An **influence line** is a graph showing how a particular response (reaction, shear, or moment) at a specific point varies as a unit load moves across the structure.

### Construction for a Simply Supported Beam

For a simply supported beam of length $L$, the influence line for the reaction at A is:

$$R_A(x) = 1 - \frac{x}{L}$$

where $x$ is the position of the unit load measured from A.

The influence line for the bending moment at a section located at distance $a$ from A is:

$$M(x) = \begin{cases} \frac{(L - a)}{L}x & \text{for } 0 \le x \le a \\ \frac{a}{L}(L - x) & \text{for } a \le x \le L \end{cases}$$

### Using Influence Lines

To find the effect of a distributed load $w(x)$ on a response quantity, integrate the product of the load and the influence line ordinate:

$$R = \int w(x) \cdot \eta(x) \, dx$$

where $\eta(x)$ is the influence line ordinate.

## Worked Example: Beam Internal Forces

Determine the shear force and bending moment at the midpoint of a 10 m simply supported beam carrying a 20 kN point load at 3 m from the left support A.

**Given:**
- Beam length: $L = 10$ m
- Point load: $P = 20$ kN at $x = 3$ m from A
- Section of interest: midpoint $x = 5$ m

**Find:** Shear force $V$ and bending moment $M$ at the midpoint.

**Solution:**

First, determine support reactions:
$$\sum M_A = 0: \quad B_y(10) - 20(3) = 0 \implies B_y = 6 \text{ kN}$$
$$\sum F_y = 0: \quad A_y + 6 - 20 = 0 \implies A_y = 14 \text{ kN}$$

Cut the beam at the midpoint ($x = 5$ m) and consider the left segment:

Shear force at midpoint:
$$V = A_y - P = 14 - 20 = -6 \text{ kN}$$

Bending moment at midpoint:
$$M = A_y(5) - P(5 - 3) = 14(5) - 20(2) = 70 - 40 = 30 \text{ kN·m}$$

**Results:** $V = -6$ kN and $M = 30$ kN·m at the midpoint.

## Applications

### Civil Engineering
- **Building design**: Analyzing frames and shear walls for gravity and lateral loads
- **Bridge engineering**: Designing girders, decks, and cable systems
- **Foundation design**: Transferring superstructure loads to the soil

### Mechanical Engineering
- **Machine frames**: Analyzing housings, brackets, and support structures
- **Pressure vessels**: Evaluating shell and nozzle stresses
- **Automotive chassis**: Predicting structural response under road loads

### Aerospace Engineering
- **Aircraft fuselage**: Analyzing semi-monocoque structures
- **Wing spars**: Evaluating bending and shear under aerodynamic loads
- **Launch vehicle structures**: Designing for thrust, pressure, and inertia loads

## Practical Tips

- Always start with a clear free body diagram showing all external loads and reactions
- Verify equilibrium by checking that the sum of forces and moments equals zero
- Use symmetry whenever possible to reduce the number of unknowns
- For complex structures, break the problem into simpler sub-structures
- Check results against physical intuition: reactions should oppose applied loads

Structural analysis provides the essential toolkit for understanding how forces flow through engineered systems. The principles covered here form the basis for more advanced topics including finite element analysis, dynamic structural response, and nonlinear structural behavior.
