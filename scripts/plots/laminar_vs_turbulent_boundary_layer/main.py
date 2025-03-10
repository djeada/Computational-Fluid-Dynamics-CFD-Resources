import numpy as np
import matplotlib.pyplot as plt

# Define dimensionless vertical coordinate (y/delta)
y = np.linspace(0, 1, 100)

# Laminar velocity profile (quadratic approximation)
u_laminar = 2 * (y) - (y)**2

# Turbulent velocity profile (1/7th power law approximation)
u_turbulent = y**(1/7)

# Plotting
plt.figure(figsize=(10, 6))

# Laminar BL plot
plt.plot(nu_laminar, y, label='Laminar BL (thin)', linewidth=2)

# Turbulent BL plot
plt.plot(nu_turbulent, y, label='Turbulent BL (thicker, fuller)', linewidth=2)

# Annotation and labels
plt.title('Laminar vs. Turbulent Boundary Layer Velocity Profiles', fontsize=14)
plt.xlabel('Velocity (u / U∞)', fontsize=12)
plt.ylabel('Boundary Layer Thickness (y / δ)', fontsize=12)
plt.legend()
plt.grid(True)

# Indicate BL thickness difference
plt.annotate('Thin, smooth profile', xy=(0.7, 0.3), xytext=(0.5, 0.2),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.annotate('Thicker, fuller, more mixing', xy=(0.9, 0.7), xytext=(0.6, 0.8),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.xlim(0, 1.05)
plt.ylim(0, 1)

plt.show()
