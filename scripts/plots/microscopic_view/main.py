import matplotlib.pyplot as plt
import numpy as np

# Function to plot the microscopic view
def plot_microscopic_view():
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Microscopic view
    ax[0].set_title('Microscopic (Molecular) View')
    ax[0].set_xlim(0, 10)
    ax[0].set_ylim(0, 10)
    ax[0].set_aspect('equal')
    ax[0].axis('off')

    # Random molecules
    np.random.seed(0)
    x = np.random.rand(20) * 10
    y = np.random.rand(20) * 10
    ax[0].scatter(x, y, s=100, color='black')
    ax[0].text(5, -1, 'Molecules in constant random motion.', ha='center', fontsize=10)

    # Macroscopic view
    ax[1].set_title('Macroscopic (Continuum) View')
    ax[1].set_xlim(0, 10)
    ax[1].set_ylim(0, 10)
    ax[1].set_aspect('equal')
    ax[1].axis('off')

    # Smoothly varying field representation
    X, Y = np.meshgrid(np.linspace(0, 10, 20), np.linspace(0, 10, 20))
    U = np.sin(Y / 2)
    V = np.cos(X / 2)
    ax[1].quiver(X, Y, U, V, scale=20)
    ax[1].text(5, -1, 'Fluid as a continuous medium with properties like density, pressure, velocity.', 
               ha='center', fontsize=10)

    plt.suptitle('Microscopic vs. Macroscopic View', fontsize=14)
    plt.show()

# Example usage
plot_microscopic_view()
