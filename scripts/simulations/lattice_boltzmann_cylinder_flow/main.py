"""
This script simulates 2D flow around a cylinder using the Lattice-Boltzmann method with optimized NumPy techniques.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation

# Simulation parameters
TOTAL_TIME_STEPS = 10000
REYNOLDS_NUMBER = 350.0
LATTICE_DIMENSIONS = (1040, 360)
NUM_POPULATIONS = 9
CYLINDER_COORDS = (LATTICE_DIMENSIONS[0] // 4, LATTICE_DIMENSIONS[1] // 2)
CYLINDER_RADIUS = LATTICE_DIMENSIONS[1] // 12
VELOCITY_LATTICE_UNITS = 0.06

# Compute relaxation parameter
NULB = VELOCITY_LATTICE_UNITS * CYLINDER_RADIUS / REYNOLDS_NUMBER
RELAXATION_PARAMETER = 1.0 / (3.0 * NULB + 0.5)

# Lattice Constants
LATTICE_VELOCITIES = np.array([(x, y) for x in [0, -1, 1] for y in [0, -1, 1]])
LATTICE_WEIGHTS = np.ones(NUM_POPULATIONS) / 36.0
LATTICE_WEIGHTS[np.linalg.norm(LATTICE_VELOCITIES, axis=1) < 1.1] = 1.0 / 9.0
LATTICE_WEIGHTS[0] = 4.0 / 9.0
NOSLIP = [LATTICE_VELOCITIES.tolist().index((-LATTICE_VELOCITIES[i]).tolist()) for i in range(NUM_POPULATIONS)]
INDICES_RIGHT_WALL = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] < 0]
INDICES_VERTICAL_MIDDLE = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] == 0]
INDICES_LEFT_WALL = np.arange(NUM_POPULATIONS)[LATTICE_VELOCITIES[:, 0] > 0]

# Helper function for density computation
def compute_density(fin):
    return np.sum(fin, axis=0)

# Equilibrium distribution function
def equilibrium(rho, u):
    cu = 3.0 * np.dot(LATTICE_VELOCITIES, u.transpose(1, 0, 2))
    usqr = 3.0 / 2.0 * (u[0] ** 2 + u[1] ** 2)
    feq = np.zeros((NUM_POPULATIONS, *LATTICE_DIMENSIONS))
    for i in range(NUM_POPULATIONS):
        feq[i] = rho * LATTICE_WEIGHTS[i] * (1.0 + cu[i] + 0.5 * cu[i] ** 2 - usqr)
    return feq

# Setup: cylindrical obstacle and velocity inlet with perturbation
obstacle = np.fromfunction(lambda x, y: (x - CYLINDER_COORDS[0]) ** 2 + (y - CYLINDER_COORDS[1]) ** 2 < CYLINDER_RADIUS ** 2, LATTICE_DIMENSIONS)
initial_velocity = np.fromfunction(lambda d, x, y: (1 - d) * VELOCITY_LATTICE_UNITS * (1.0 + 1e-4 * np.sin(y / (LATTICE_DIMENSIONS[1] - 1.0) * 2 * np.pi)), (2, *LATTICE_DIMENSIONS))
feq = equilibrium(1.0, initial_velocity)
fin = feq.copy()

# Setup the figure and axis
fig, ax = plt.subplots(facecolor='black')
ax.set_facecolor('black')
cax = ax.imshow(np.sqrt(initial_velocity[0] ** 2 + initial_velocity[1] ** 2).T, cmap=cm.viridis, origin='lower')
colorbar = fig.colorbar(cax, label='Velocity Magnitude (lattice units)', ax=ax)

# Set colorbar tick and label colors
colorbar.ax.yaxis.set_tick_params(color='white')
colorbar.ax.yaxis.label.set_color('white')
plt.setp(plt.getp(colorbar.ax.axes, 'yticklabels'), color='white')

ax.set_xlabel('X (lattice units)', color='white')
ax.set_ylabel('Y (lattice units)', color='white')
ax.set_title('2D Flow Around a Cylinder', color='white')

# Set tick parameters and spine colors to make them visible
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_edgecolor('white')

def update(frame):
    global fin
    for _ in range(10):  # Smaller steps for smoother animation
        fin[INDICES_RIGHT_WALL, -1, :] = fin[INDICES_RIGHT_WALL, -2, :]  # Right wall: outflow condition.
        rho = compute_density(fin)  # Calculate macroscopic density and velocity.
        u = np.zeros((2, *LATTICE_DIMENSIONS))
        for i in range(NUM_POPULATIONS):
            u += LATTICE_VELOCITIES[i].reshape(2, 1, 1) * fin[i]
        u /= rho

        u[:, 0, :] = initial_velocity[:, 0, :]  # Left wall: compute density from known populations.
        rho[0, :] = 1.0 / (1.0 - u[0, 0, :]) * (compute_density(fin[INDICES_VERTICAL_MIDDLE, 0, :]) + 2.0 * compute_density(fin[INDICES_RIGHT_WALL, 0, :]))

        feq = equilibrium(rho, u)  # Left wall: Zou/He boundary condition.
        fin[INDICES_LEFT_WALL, 0, :] = fin[INDICES_RIGHT_WALL, 0, :] + feq[INDICES_LEFT_WALL, 0, :] - fin[INDICES_RIGHT_WALL, 0, :]
        fout = fin - RELAXATION_PARAMETER * (fin - feq)  # Collision step.

        for i in range(NUM_POPULATIONS):
            fout[i, obstacle] = fin[NOSLIP[i], obstacle]

        for i in range(NUM_POPULATIONS):  # Streaming step.
            fin[i] = np.roll(np.roll(fout[i], LATTICE_VELOCITIES[i, 0], axis=0), LATTICE_VELOCITIES[i, 1], axis=1)

    # Update the plot
    u_mag = np.sqrt(u[0] ** 2 + u[1] ** 2).T
    cax.set_data(u_mag)
    return cax,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(TOTAL_TIME_STEPS // 10), blit=False)

# Show the animation
plt.show()
