import matplotlib.pyplot as plt
import numpy as np

# Generate sample data to mimic the turbulent flow data in the provided image
time = np.linspace(0, 100, 1000)
velocity = np.sin(time) + np.random.normal(scale=0.2, size=time.shape)
fluctuating_velocity = velocity - np.mean(velocity)
squared_fluctuating_velocity = fluctuating_velocity**2

# Create subplots similar to the provided image
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Remove the empty subplot (2,1)
fig.delaxes(axs[1, 1])

# Plot the data
axs[0, 0].plot(time, velocity, color='black')
axs[0, 0].set_title('(a)')
axs[0, 0].set_xlabel('time')
axs[0, 0].set_ylabel('u')
axs[0, 0].axhline(np.mean(velocity), color='gray', linestyle='--')

axs[0, 1].plot(time, fluctuating_velocity, color='black')
axs[0, 1].set_title('(b)')
axs[0, 1].set_xlabel('time')
axs[0, 1].set_ylabel('u\'')

axs[1, 0].plot(time, squared_fluctuating_velocity, color='black')
axs[1, 0].set_title('(c)')
axs[1, 0].set_xlabel('time')
axs[1, 0].set_ylabel('(u\')^2')
axs[1, 0].axhline(np.mean(squared_fluctuating_velocity), color='gray', linestyle='--')

# Adjust layout
plt.tight_layout()

# Save the generated plot
plt.savefig("/mnt/data/turbulence_plots.png")

plt.show()
