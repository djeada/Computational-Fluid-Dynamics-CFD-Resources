# Trusses and Frames

Trusses and frames are fundamental structural systems used extensively in engineering. Trusses carry loads through axial forces in their members, while frames include multi-force members that also resist shear and bending. Understanding both systems is essential for structural design and analysis.

## Definition and Classification of Trusses

A **truss** is an assembly of slender members connected at their endpoints by frictionless pins, with external loads applied only at the joints. Under these idealizations, every member is a **two-force member** carrying only axial force (tension or compression).

### Assumptions for Truss Analysis
- All members are straight and connected at their ends by frictionless pins
- Loads and reactions act only at the joints
- The weight of members is negligible compared to applied loads
- Members deform negligibly (rigid body assumption for statics)

### Determinacy Condition

For a plane truss with $m$ members, $j$ joints, and $r$ external reactions, the structure is statically determinate if:

$$m + r = 2j$$

- If $m + r > 2j$: statically indeterminate (degree = $m + r - 2j$)
- If $m + r < 2j$: unstable mechanism

## Simple vs Compound Trusses

### Simple Trusses
A **simple truss** is constructed by starting with a basic triangular element and adding two members and one joint at a time. Every simple truss satisfies $m = 2j - 3$.

### Compound Trusses
A **compound truss** is formed by connecting two or more simple trusses together. The connection can be:
- Three bars not all parallel and not concurrent
- A common joint plus one bar
- A pin and a roller

Compound trusses require careful analysis to ensure they are both stable and determinate.

## Method of Joints

### Procedure

The method of joints applies equilibrium equations at each joint, treating it as a particle:

$$\sum F_x = 0, \quad \sum F_y = 0$$

Since each joint provides two equations, the method works well for finding forces in **all** members of a truss.

### Steps
1. Determine external support reactions using whole-truss equilibrium
2. Start at a joint with at most two unknown member forces
3. Assume unknown forces are in tension (pulling away from the joint)
4. Apply $\sum F_x = 0$ and $\sum F_y = 0$
5. A positive result confirms tension; a negative result indicates compression
6. Proceed to adjacent joints, using previously found forces

### Worked Example 1: Method of Joints

Analyze the following simple truss. Joints A and C are at the base, 4 m apart. Joint B is at the top, 3 m directly above A. A horizontal force of 12 kN acts to the right at joint B. Support A is a pin; support C is a roller on a horizontal surface.

**Given:**
- Triangle ABC: $A = (0, 0)$, $B = (0, 3)$, $C = (4, 0)$
- Horizontal load at B: $P = 12$ kN (to the right)
- Support A: pin ($A_x$, $A_y$); Support C: roller ($C_y$)

**Find:** Forces in members AB, BC, and AC.

**Solution:**

Member lengths:
- $AB = 3$ m
- $AC = 4$ m
- $BC = \sqrt{4^2 + 3^2} = 5$ m

**Global equilibrium:**

$$\sum F_x = A_x + 12 = 0 \implies A_x = -12 \text{ kN}$$

$$\sum M_A = 12(3) - C_y(4) = 0 \implies C_y = 9 \text{ kN}$$

$$\sum F_y = A_y + C_y = 0 \implies A_y = -9 \text{ kN}$$

**Joint B** (two unknowns: $F_{AB}$, $F_{BC}$):

The direction from B to C is $(4, -3)/5$. Assume both members in tension.

$$\sum F_x = 12 + F_{BC}\frac{4}{5} = 0 \implies F_{BC} = -15 \text{ kN (compression)}$$

$$\sum F_y = F_{AB} + F_{BC}\frac{-3}{5} = 0 \implies F_{AB} = F_{BC}\frac{3}{5} = -9 \text{ kN}$$

Wait — re-examine directions. Tension in AB means force pulls B toward A, i.e., downward. Tension in BC pulls B toward C.

$$\sum F_x = 12 + F_{BC}\frac{4}{5} = 0 \implies F_{BC} = -15 \text{ kN (compression)}$$

$$\sum F_y = -F_{AB} + F_{BC}\left(\frac{-3}{5}\right) = 0 \implies F_{AB} = -15 \times \frac{-3}{5} = 9 \text{ kN (tension)}$$

**Joint A** (one unknown: $F_{AC}$):

$$\sum F_x = -12 + F_{AC} = 0 \implies F_{AC} = 12 \text{ kN (tension)}$$

**Results:**
- $F_{AB} = 9$ kN (tension)
- $F_{BC} = 15$ kN (compression)
- $F_{AC} = 12$ kN (tension)

## Method of Sections

### Procedure

The method of sections is used when forces in only a few specific members are needed. It involves cutting the truss through a section and applying the three equilibrium equations to one part:

$$\sum F_x = 0, \quad \sum F_y = 0, \quad \sum M_O = 0$$

Since three equations are available, the cut should pass through at most **three members** with unknown forces.

### Steps
1. Determine external support reactions
2. Pass a section through the truss cutting the members of interest (no more than three unknowns)
3. Select one part of the cut truss as a free body
4. Apply the three equilibrium equations
5. Choose moment points wisely to isolate single unknowns

### Worked Example 2: Method of Sections

A Pratt truss has a span of 16 m with four equal panels of 4 m each. The height is 3 m. A vertical load of 24 kN acts at the second joint from the left on the bottom chord. Determine the force in the top chord member in the second panel.

**Given:**
- Span: $L = 16$ m, panel width: 4 m, height: $h = 3$ m
- Vertical load: $P = 24$ kN at 8 m from left support
- Simply supported (pin at left A, roller at right E)

**Find:** Force $F_{top}$ in the top chord member of the second panel.

**Solution:**

**Support reactions:**
$$\sum M_A = 0: \quad E_y(16) - 24(8) = 0 \implies E_y = 12 \text{ kN}$$
$$A_y = 24 - 12 = 12 \text{ kN}$$

**Section cut:** Cut through the second panel, slicing the top chord, a diagonal, and the bottom chord. Consider the left portion.

Taking moments about the bottom chord joint directly below the top chord member (at $x = 8$ m from A) eliminates the bottom chord and diagonal forces:

$$\sum M_{bottom} = A_y(8) - F_{top}(3) = 0$$
$$F_{top} = \frac{12 \times 8}{3} = 32 \text{ kN (compression)}$$

The top chord member carries 32 kN in compression.

## Zero-Force Members

**Zero-force members** carry no load under the given loading but are essential for truss stability. They can be identified by inspection:

### Rule 1
If only two non-collinear members meet at an unloaded joint, **both** members are zero-force members.

### Rule 2
If three members meet at an unloaded joint and two are collinear, the **third** member is a zero-force member.

Identifying zero-force members simplifies the analysis by reducing the number of unknowns.

## Frames and Machines

### Frames

A **frame** is a structure containing at least one **multi-force member** — a member with forces acting at more than two points. Unlike truss members, frame members can carry:
- Axial force
- Shear force
- Bending moment

### Machines

A **machine** is a structure designed to transmit and modify forces. Like frames, machines contain multi-force members but are not necessarily rigid — they may have movable parts (e.g., pliers, scissors, toggle clamps).

### Analysis Procedure for Frames

1. Draw the free body diagram of the entire frame to find external reactions
2. Disassemble the frame into individual members
3. Draw free body diagrams of each member, applying Newton's third law at connections
4. Apply equilibrium equations to each member:
   - Three equations per member in 2D ($\sum F_x = 0$, $\sum F_y = 0$, $\sum M = 0$)
5. Solve the system of equations for internal forces and pin reactions

### Pin Connection Convention

At a pin connecting two members, the forces on each member are equal and opposite:
- If member 1 exerts force $(P_x, P_y)$ on member 2 through a pin
- Then member 2 exerts force $(-P_x, -P_y)$ on member 1

## Applications

### Bridges
- **Pratt truss**: Diagonals in tension under gravity loads — efficient use of slender members
- **Warren truss**: Alternating diagonal directions — used for uniform loading
- **Howe truss**: Diagonals in compression — historically used with timber

### Roof Structures
- **Fink truss**: Common for residential pitched roofs
- **Scissor truss**: Provides a vaulted ceiling profile
- **Bowstring truss**: Curved top chord for long-span roofs

### Towers and Masts
- **Transmission towers**: Lattice trusses resisting wind and conductor loads
- **Crane booms**: Truss structures for lightweight, high-strength lifting arms
- **Space frames**: Three-dimensional truss systems for large-span roofs

## Practical Tips

- Always verify truss determinacy ($m + r = 2j$) before starting the analysis
- Identify zero-force members first to simplify calculations
- Use the method of joints for complete analysis and the method of sections for targeted member forces
- When analyzing frames, be meticulous with free body diagrams at each pin connection
- Check your work by verifying equilibrium of the portion not directly analyzed

Trusses and frames are among the most widely used structural systems in engineering. The analytical methods presented here — method of joints, method of sections, and frame disassembly — provide the tools for understanding and designing these essential structures.
