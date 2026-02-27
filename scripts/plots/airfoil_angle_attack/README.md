# Airfoil Angle of Attack

This script plots a NACA 4-digit airfoil (m = 0.02, p = 0.4, t = 0.12, chord c = 2.0) at two angles of attack — 10° and 60° — to contrast attached and fully separated flow regimes. The airfoil geometry is constructed from the standard NACA thickness distribution, then rotated using a 2D rotation matrix. Dashed chord-line arrows indicate the direction of each angle of attack, and a free-stream arrow marks the oncoming flow direction.

![angle_of_attack](https://github.com/user-attachments/assets/ec38fb22-8c04-4947-a911-e17eaec8e178)

## Overview

- NACA 4-digit airfoil geometry (m=0.02, p=0.4, t=0.12, c=2.0)
- Two overlaid airfoil outlines at α = 10° (attached) and α = 60° (stalled)
- 2D rotation matrix applied to transform airfoil coordinates
- Chord-line arrows and free-stream direction annotation

## Mathematical Background

### NACA 4-Digit Thickness Distribution

The half-thickness at chordwise position $x$ is given by:

$$y_t = \frac{t}{0.2}\,c\!\left(0.2969\sqrt{\frac{x}{c}} - 0.1260\frac{x}{c} - 0.3516\!\left(\frac{x}{c}\right)^{\!2} + 0.2843\!\left(\frac{x}{c}\right)^{\!3} - 0.1015\!\left(\frac{x}{c}\right)^{\!4}\right)$$

where $t$ is the maximum thickness-to-chord ratio.

### Rotation by Angle of Attack

The airfoil is rotated about the origin by angle $\alpha$ using the standard 2D rotation matrix:

$$\begin{pmatrix}x'\\y'\end{pmatrix} = \begin{pmatrix}\cos\alpha & -\sin\alpha\\\sin\alpha & \cos\alpha\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}$$

### Thin-Airfoil Lift and Stall

Thin-airfoil theory predicts the lift coefficient as a linear function of angle of attack:

$$C_L = 2\pi\sin\alpha$$

This relationship breaks down near the critical stall angle (~15° for typical airfoils), beyond which flow separates and lift drops sharply.

## Implementation

1. Generate chordwise stations $x \in [0, c]$ and evaluate the NACA thickness formula.
2. Construct upper and lower surface coordinates from camber line and thickness.
3. Apply the rotation matrix to both surfaces for each angle of attack.
4. Plot the rotated airfoils, chord lines, and a free-stream direction arrow.
5. Annotate each airfoil with its angle of attack and label the stall regime.

## Output

The script displays and saves `airfoil_angle_attack.png`: two NACA airfoil outlines rotated to 10° and 60° angles of attack, with chord-line dashed arrows and a free-stream indicator, illustrating attached versus post-stall configurations.

