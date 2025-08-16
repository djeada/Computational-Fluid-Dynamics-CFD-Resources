import numpy as np
import matplotlib.pyplot as plt

# Coordinates for the wall
wall_x = np.linspace(-1, 2, 100)
wall_y = np.zeros_like(wall_x)

# Coordinates for attached boundary layer
attached_x = np.linspace(-1, 0, 100)
attached_y = 0.3 * np.sqrt(np.abs(attached_x))

# Coordinates for separated flow
separated_x = np.linspace(0, 1.5, 100)
separated_y = -0.5 * np.sqrt(separated_x)

# Plotting
plt.figure(figsize=(10, 6))

# Wall
plt.plot(wall_x, wall_y, "k-", linewidth=3, label="Wall")

# Attached boundary layer
plt.plot(attached_x, attached_y, "b-", linewidth=2, label="Attached Boundary Layer")

# Separated flow region
plt.plot(
    separated_x,
    separated_y,
    "r-",
    linewidth=2,
    label="Separated Region (Recirculation)",
)

# Free stream arrows (adverse pressure gradient)
for x_pos in np.linspace(-0.9, 1.2, 5):
    plt.arrow(
        x_pos, 0.8, 0.3, 0, head_width=0.05, head_length=0.1, fc="green", ec="green"
    )

# Annotations
plt.text(0.1, 0.2, "Flow Separation Point", fontsize=12, color="purple")
plt.annotate(
    "High-momentum fluid brought by turbulence",
    xy=(0.5, 0.1),
    xytext=(0.8, 0.3),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
)

# Plot settings
plt.title("Flow Separation in Boundary Layers", fontsize=14)
plt.xlabel("Flow Direction (x)", fontsize=12)
plt.ylabel("Vertical Direction (y)", fontsize=12)
plt.grid(True)
plt.legend()

plt.xlim(-1, 2)
plt.ylim(-1, 1)

plt.show()
