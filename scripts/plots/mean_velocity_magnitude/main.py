import matplotlib.pyplot as plt
import numpy as np

# Generate mock data for the plot
x = np.linspace(0, 6, 50)
exp = np.exp(-0.2 * x) * np.sin(x) + 0.75
cfd = exp + 0.05 * np.random.normal(size=x.size)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the experimental data
ax.plot(x, exp, "o-", label="Exp", color="black")

# Plot the CFD simulation data
ax.plot(x, cfd, "-", label="CFD SRS", color="cyan")

# Add labels and title
ax.set_xlabel("rel. distance [m]")
ax.set_ylabel("$|U|/U0$ [-]")
ax.set_title(
    "Mean velocity magnitude, under-body centreline\nL1 / Underbody Centerline @ z = -0.2376m"
)
ax.legend()

# Save the plot to a file
file_path = "/mnt/data/mean_velocity_magnitude_plot_no_annotation.png"
plt.tight_layout()
plt.savefig(file_path)

file_path
