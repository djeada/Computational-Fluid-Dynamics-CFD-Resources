import numpy as np
import matplotlib.pyplot as plt

# --- Grid setup ---
nx, ny = 100, 50
xmin, xmax = 0.0, 2.0
ymin, ymax = 0.0, 1.0
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
X, Y = np.meshgrid(x, y)


def nozzle_top(x_array):
    """
    Converging-Diverging nozzle shape:
      - from x=0 to x=1: linearly goes 0.8 -> 0.4
      - from x=1 to x=2: linearly goes 0.4 -> 0.7
    Works for arrays (vectorized).
    """
    top = np.zeros_like(x_array)

    # Mask for x <= 1.0
    left_mask = x_array <= 1.0
    # Mask for x > 1.0
    right_mask = ~left_mask  # the complement

    # Left part (converging): 0.8 -> 0.4
    top[left_mask] = 0.8 - 0.4 * (x_array[left_mask] / 1.0)

    # Right part (diverging): 0.4 -> 0.7
    top[right_mask] = 0.4 + 0.3 * ((x_array[right_mask] - 1.0) / 1.0)

    return top


# Get nozzle boundary (2D) without ambiguity
Ytop = nozzle_top(X)

# --- Mask inside the nozzle ---
mask = Y <= Ytop

# Example: define a flow velocity that depends on cross-sectional area
Q = 0.2
A = np.clip(Ytop, 1e-5, None)  # cross-section from 0 to top
u = np.where(mask, Q / A, np.nan)
v = np.zeros_like(u)

# Mach number for demonstration
speed_of_sound = 0.5
M = u / speed_of_sound

# --- Plotting ---
fig, ax = plt.subplots(figsize=(9, 3))

ax.plot(x, nozzle_top(x), "k", lw=2, label="Nozzle top boundary")
ax.plot(x, np.zeros_like(x), "k", lw=2, label="Nozzle bottom boundary")

strm = ax.streamplot(X, Y, u, v, color=M, cmap="jet", density=1.4, linewidth=1.2)

cb = plt.colorbar(strm.lines, ax=ax, label="Mach Number")

ax.set_aspect("equal", "box")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel("x (arbitrary units)")
ax.set_ylabel("y (arbitrary units)")
ax.set_title("Flow Through a Converging-Diverging Nozzle")

plt.tight_layout()
plt.show()
