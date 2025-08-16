import numpy as np
import matplotlib.pyplot as plt

# Define the parameters for visualization
layers = ["Slow layer (bottom)", "Medium layer (middle)", "Fast layer (top)"]
velocities = [0, 5, 10]  # Example velocities (arbitrary units)

# Create a figure for visualization
fig, ax = plt.subplots(figsize=(8, 6))

# Define layer boundaries and fill colors
layer_boundaries = [0, 1, 2, 3]
colors = ["lightblue", "skyblue", "dodgerblue"]

# Plot layers
for i in range(len(layers)):
    ax.fill_betweenx(
        [layer_boundaries[i], layer_boundaries[i + 1]],
        0,
        velocities[i],
        color=colors[i],
        alpha=0.7,
        label=f"{layers[i]} (V = {velocities[i]})",
    )

# Add annotations
for i, velocity in enumerate(velocities):
    ax.annotate(
        f"V = {velocity}",
        xy=(velocity, (layer_boundaries[i] + layer_boundaries[i + 1]) / 2),
        xytext=(velocity + 1, (layer_boundaries[i] + layer_boundaries[i + 1]) / 2),
        va="center",
        arrowprops=dict(arrowstyle="->"),
    )

# Label velocity gradient
ax.annotate(
    "Velocity gradient\n(viscous forces)",
    xy=(7, 2.5),
    xytext=(8, 2),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=10,
    color="red",
)

# Set plot labels and title
ax.set_xlabel("Velocity")
ax.set_ylabel("Layer Position")
ax.set_title("Velocity Gradient and Viscous Forces in Fluid Layers")
ax.set_yticks([])
ax.legend(loc="upper left")

plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
