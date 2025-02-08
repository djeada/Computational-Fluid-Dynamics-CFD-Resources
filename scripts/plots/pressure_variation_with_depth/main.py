import numpy as np
import matplotlib.pyplot as plt

def plot_pressure_variation_with_depth(fluid_density=1000, g=9.81, max_depth=20):
    # Depth range from 0 to max_depth meters
    depth = np.linspace(0, max_depth, 100)

    # Pressure calculation using P = P0 + ρgh
    atmospheric_pressure = 101325  # Pa
    pressure = atmospheric_pressure + fluid_density * g * depth

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(pressure, depth, label='Pressure vs Depth', color='blue')

    # Inverting y-axis to represent increasing depth downwards
    plt.gca().invert_yaxis()

    plt.title('Pressure Variation with Depth')
    plt.xlabel('Pressure (Pa)')
    plt.ylabel('Depth (m)')
    plt.grid(True)
    plt.legend()

    plt.show()

# Example usage
plot_pressure_variation_with_depth()
