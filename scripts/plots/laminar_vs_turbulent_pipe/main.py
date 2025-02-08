import matplotlib.pyplot as plt
import numpy as np

# Function to plot laminar and turbulent flow velocity profiles
def plot_laminar_vs_turbulent(pipe_radius=1, max_velocity=2):
    r = np.linspace(0, pipe_radius, 100)

    # Laminar flow (parabolic profile)
    laminar_velocity = max_velocity * (1 - (r / pipe_radius)**2)

    # Turbulent flow (flatter profile with sharp drop near the wall)
    turbulent_velocity = max_velocity * (1 - (r / pipe_radius)**(1/7))

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Laminar flow plot
    ax[0].plot(laminar_velocity, r, label='Laminar Flow', color='blue')
    ax[0].invert_yaxis()
    ax[0].set_title('Laminar Flow (Parabolic)')
    ax[0].set_xlabel('Velocity')
    ax[0].set_ylabel('Radius (r)')
    ax[0].grid(True)
    ax[0].annotate('v(r) max here', xy=(max_velocity, 0), xytext=(max_velocity - 0.8, 0.3),
                   arrowprops=dict(arrowstyle='->'), fontsize=10)
    ax[0].annotate('Velocity = 0 at wall', xy=(0, pipe_radius), xytext=(0.5, pipe_radius - 0.2),
                   arrowprops=dict(arrowstyle='->'), fontsize=10)

    # Turbulent flow plot
    ax[1].plot(turbulent_velocity, r, label='Turbulent Flow', color='red')
    ax[1].invert_yaxis()
    ax[1].set_title('Turbulent Flow (Flatter)')
    ax[1].set_xlabel('Velocity')
    ax[1].grid(True)
    ax[1].annotate('High mixing region', xy=(max_velocity * 0.8, pipe_radius / 2), xytext=(max_velocity * 0.4, pipe_radius / 1.5),
                   arrowprops=dict(arrowstyle='->'), fontsize=10)
    ax[1].annotate('Velocity ~ 0 at wall', xy=(0, pipe_radius), xytext=(0.5, pipe_radius - 0.2),
                   arrowprops=dict(arrowstyle='->'), fontsize=10)

    plt.suptitle('Laminar vs. Turbulent Flow Velocity Profiles', fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# Example usage
plot_laminar_vs_turbulent()
