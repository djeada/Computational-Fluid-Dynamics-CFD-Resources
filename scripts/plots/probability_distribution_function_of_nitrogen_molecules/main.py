import matplotlib.pyplot as plt
import numpy as np

# Data for the plot
temperatures = [300, 600, 900, 1200]
velocities = np.linspace(0, 3000, 500)


# Relative number of N2 molecules for each temperature
def maxwell_boltzmann_distribution(v, T):
    k_B = 1.38e-23  # Boltzmann constant in J/K
    m = 4.65e-26  # mass of N2 molecule in kg
    return (
        4
        * np.pi
        * (m / (2 * np.pi * k_B * T)) ** (3 / 2)
        * v**2
        * np.exp(-m * v**2 / (2 * k_B * T))
    )


distributions = [maxwell_boltzmann_distribution(velocities, T) for T in temperatures]

# Plot
plt.figure(figsize=(12, 8))

for T, distribution in zip(temperatures, distributions):
    plt.plot(velocities, distribution, label=f"{T} K")

plt.xlabel("Velocity (m/s)", fontsize=14)
plt.ylabel("Relative number of N2 molecules", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.title("Probability Distribution Function of N2 Molecules", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlim(0, 3000)
plt.ylim(0, None)

# Save plot to a static image file
plt.savefig("/mnt/data/probability_distribution_function.png")

plt.show()
