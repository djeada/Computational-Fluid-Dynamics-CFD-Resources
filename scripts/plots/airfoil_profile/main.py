import numpy as np
import matplotlib.pyplot as plt

# Define the chord length (unit length for simplicity)
chord = 1.0
x = np.linspace(0, chord, 500)  # Chordwise positions

# Define camber line (for a cambered airfoil similar to a NACA 4-digit profile)
camber_max = 0.04  # Max camber (4% of chord)
camber_position = 0.4  # Max camber position (40% of chord)

# Define the camber line using a simple parabolic equation
camber_line = np.where(
    x < camber_position,
    camber_max / (camber_position**2) * (2 * camber_position * x - x**2),
    camber_max
    / ((1 - camber_position) ** 2)
    * ((1 - 2 * camber_position) + 2 * camber_position * x - x**2),
)

# Substantially increase the thickness
thickness_max = 0.6  # Increase max thickness to 60% of chord for a much thicker airfoil

# Recalculate thickness distribution with the increased thickness
thickness_distribution = thickness_max * (
    0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4
)

# Calculate upper and lower surfaces
upper_surface = camber_line + thickness_distribution
lower_surface = camber_line - thickness_distribution

# Create the plot
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the upper and lower surfaces
ax.plot(x, upper_surface, color="gray", label="Upper Surface")
ax.plot(x, lower_surface, color="gray", label="Lower Surface")

# Plot the chord line
ax.plot([0, 1], [0, 0], "yellow", lw=2, label="Chord Line")

# Plot the camber line
ax.plot(x, camber_line, "r--", lw=2, label="Mean Camber Line")

# Add annotations for key points
ax.text(
    0,
    0.04,
    "Leading edge",
    fontsize=12,
    bbox=dict(facecolor="lightgray", edgecolor="black"),
)
ax.text(
    0.9,
    0.04,
    "Trailing edge",
    fontsize=12,
    bbox=dict(facecolor="lightgray", edgecolor="black"),
)
ax.text(
    0.5,
    -0.03,
    "Chord line",
    fontsize=12,
    bbox=dict(facecolor="yellow", edgecolor="black"),
    ha="center",
)
ax.text(
    0.5,
    0.18,
    "Mean camber line",
    fontsize=12,
    bbox=dict(facecolor="orange", edgecolor="black"),
    ha="center",
)
ax.text(0.15, 0.28, "Camber of upper surface", fontsize=10, ha="center")
ax.text(0.15, -0.25, "Camber of lower surface", fontsize=10, ha="center")

# Set axis limits, title, and remove the grid
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.35, 0.35)
ax.set_aspect("equal")
ax.axis("off")

# Add title
plt.title("Airfoil Profile with Increased Thickness")

# Display the plot
plt.legend()
plt.tight_layout()
plt.show()
