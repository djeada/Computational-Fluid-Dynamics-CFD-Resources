import numpy as np
import matplotlib.pyplot as plt

def froude_number(velocity, g, length):
    """
    Compute the Froude number.
    Fr = U / sqrt(g * L)

    Parameters
    ----------
    velocity : float or np.ndarray
        Characteristic flow velocity (m/s).
    g : float
        Gravitational acceleration (m/s^2).
    length : float
        Characteristic length scale (m).

    Returns
    -------
    Fr : float or np.ndarray
        Froude number.
    """
    return velocity / np.sqrt(g * length)


def plot_froude_number_vs_velocity():
    """
    Plots the Froude number vs. velocity for a list of characteristic hull lengths.
    """

    # Define parameters
    g = 9.81  # m/s^2
    lengths = [5, 10, 15, 20]  # example hull lengths in meters
    velocities = np.linspace(0, 10, 200)  # range of velocities: 0 to 10 m/s

    # Create a new figure
    plt.figure(figsize=(7, 5))

    # Plot Froude curves for each length
    for L in lengths:
        fr_values = froude_number(velocities, g, L)
        plt.plot(velocities, fr_values, label=f"L = {L} m")

    plt.title("Froude Number vs. Velocity for Various Hull Lengths")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Froude Number (Fr)")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plot_froude_number_vs_velocity()
