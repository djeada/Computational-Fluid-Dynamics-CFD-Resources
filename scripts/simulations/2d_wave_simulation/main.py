import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
L = 5
Nx = 100
Ny = 100
c = 1  # wave speed
x = np.linspace(-L, L, Nx)
y = np.linspace(-L, L, Ny)
dx = x[1] - x[0]
dy = y[1] - y[0]
dt = 0.5 * min(dx, dy) / (c * np.sqrt(2))  # CFL condition

# Initial condition: Scaled Gaussian type
scale_factor = 5  # Increase this value to make the wave height larger
X, Y = np.meshgrid(x, y)
u0 = scale_factor * np.exp(-0.5 * (X**2 + Y**2))
u1 = u0.copy()
u = u0.copy()

# Set up the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Initial plot
surf = ax.plot_surface(X, Y, u0, cmap='viridis')
ax.set_zlim(-scale_factor, scale_factor)
color_bar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, pad=0.1, location='left')
color_bar.set_label('Wave Amplitude', color='white')
color_bar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(color_bar.ax.axes, 'yticklabels'), color='white')

# Function to update the plot
def update(frame):
    global u, u1, surf
    u_new = np.zeros_like(u)
    u_new[1:-1, 1:-1] = (2 * u[1:-1, 1:-1] - u1[1:-1, 1:-1] +
                         (dt * c)**2 * ((u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2 +
                                        (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2))

    # Apply Dirichlet boundary conditions (u = 0 on the boundary)
    u_new[0, :] = 0
    u_new[-1, :] = 0
    u_new[:, 0] = 0
    u_new[:, -1] = 0

    # Update previous steps
    u1 = u.copy()
    u = u_new.copy()

    # Update the surface plot
    surf.remove()
    surf = ax.plot_surface(X, Y, u, cmap='viridis')
    ax.set_zlim(-scale_factor, scale_factor)
    ax.set_title('2D Wave Equation Simulation Using Finite Differences', color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('U', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    return surf,

# Create animation
anim = FuncAnimation(fig, update, frames=int(40 / dt), blit=False)
plt.show()
