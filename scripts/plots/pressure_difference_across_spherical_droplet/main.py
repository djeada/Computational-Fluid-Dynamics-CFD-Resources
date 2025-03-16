import numpy as np
import matplotlib.pyplot as plt

# Set parameters
R = 1  # radius of droplet
sigma = 0.0728  # surface tension of water at room temp (N/m)
p_out = 1  # atmospheric pressure (arbitrary units)
p_in = p_out + (2 * sigma / R)

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Create droplet interface
circle = plt.Circle((0, 0), R, color='skyblue', alpha=0.4, edgecolor='navy', linewidth=2)
ax.add_artist(circle)

# Mark radius
ax.annotate('Radius R', xy=(0,0.2), xytext=(0.5, 0.8), arrowprops=dict(arrowstyle='<->', color='black'), fontsize=12)

# Annotations for pressures
ax.text(0, 0, f'$p_{{in}} = p_{{out}} + \\frac{{2 \, \sigma}}{{R}}$', fontsize=14, ha='center')
ax.text(-1.5, 1.2, 'Inside droplet\n$\\Delta p$ higher', fontsize=12, color='navy')
ax.text(-1.5, -1.4, 'Outside droplet\n$p_{out}$ (atmosphere)', fontsize=12, color='navy')

# Axes adjustments
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Pressure Difference Across a Spherical Droplet', fontsize=14)

plt.show()
