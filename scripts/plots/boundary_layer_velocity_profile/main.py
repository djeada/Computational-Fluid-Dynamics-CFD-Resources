import numpy as np
import matplotlib.pyplot as plt

# Vertical coordinate (y-direction)
y = np.linspace(0, 1, 100)

# Velocity profile approximation within the boundary layer
u_profile = y ** (1 / 7)

# Plotting the velocity profile
plt.figure(figsize=(8, 6))

# Velocity profile plot
plt.plot(
    u_profile, y, linewidth=2, color="blue", label="Velocity Profile (Boundary Layer)"
)

# Indicating boundary layer thickness (approx. u ~ 0.99 U∞)
plt.axhline(y=1, linestyle="--", color="red", linewidth=1)
plt.text(0.5, 1.02, "Boundary Layer Thickness (δ)", fontsize=12, color="red")

# Wall
plt.axhline(y=0, color="black", linewidth=3, label="Wall (y=0, u=0)")

# Annotations and labels
plt.title("Boundary Layer Velocity Profile", fontsize=14)
plt.xlabel("Velocity u/U∞", fontsize=12)
plt.ylabel("Distance from Wall (y)", fontsize=12)
plt.legend()
plt.grid(True)

# Axis limits
plt.xlim(0, 1.05)
plt.ylim(0, 1)

plt.show()
