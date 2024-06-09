import matplotlib.pyplot as plt
import numpy as np

# Generate mock data for the plot
x = np.linspace(-1, 4, 50)
exp = -0.2 * np.sin(x) - 0.1 * np.cos(2 * x)
cfd = exp + 0.05 * np.random.normal(size=x.size)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the experimental data
ax.plot(x, exp, 'o-', label='Exp', color='black')

# Plot the CFD simulation data
ax.plot(x, cfd, 'o-', label='CFD SRS', color='cyan')

# Add labels and title
ax.set_xlabel('x [m]')
ax.set_ylabel('$C_P$ [-]')
ax.set_title('Mean pressure coefficient, upper-body centreline\nUpperbody Centerline (y = 0m)')
ax.legend()

# Highlight specific area
ax.annotate('Separation plateau less\npronounced in simulation',
            xy=(3, 0.3), xytext=(2.5, 0.6),
            arrowprops=dict(facecolor='blue', shrink=0.05),
            fontsize=10, color='blue')

# Show the plot
plt.tight_layout()
plt.show()
