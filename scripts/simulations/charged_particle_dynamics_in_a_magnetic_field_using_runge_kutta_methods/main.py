import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
q = 1.0  # Charge of the particle
m = 1.0  # Mass of the particle
B = np.array([0, 0, 1.0])  # Magnetic field vector


# Lorentz force differential equations
def lorentz_force(t, y):
    r, v = y[:3], y[3:]
    a = (q / m) * np.cross(v, B)
    return np.hstack((v, a))


# Runge-Kutta 4th order method (RK4)
def rk4_step(func, t, y, dt):
    k1 = func(t, y)
    k2 = func(t + dt / 2, y + dt / 2 * k1)
    k3 = func(t + dt / 2, y + dt / 2 * k2)
    k4 = func(t + dt, y + dt * k3)
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# Initial conditions
r0 = np.array([0.0, 1.0, 0.0])
v0 = np.array([1.0, 0.0, 1.0])  # Initial velocity adjusted for better visualization
y0 = np.hstack((r0, v0))

# Time parameters
t0 = 0.0
tf = 50.0  # Extended time to visualize the helical path
dt = 0.01  # Adjusted time step for finer granularity
num_steps = int((tf - t0) / dt)

# Initialize arrays to store the solution
t_vals = np.linspace(t0, tf, num_steps)
r_vals = np.zeros((num_steps, 3))
v_vals = np.zeros((num_steps, 3))

# Initial values
r_vals[0] = r0
v_vals[0] = v0

# Time integration using RK4
y = y0
for i in range(1, num_steps):
    y = rk4_step(lorentz_force, t_vals[i - 1], y, dt)
    r_vals[i] = y[:3]
    v_vals[i] = y[3:]

# Initialize the plot
fig = plt.figure(facecolor="black")
ax = fig.add_subplot(111, projection="3d", facecolor="black")

# Set plot limits
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 60)
ax.set_xlabel("X (meters)", color="white")
ax.set_ylabel("Y (meters)", color="white")
ax.set_zlabel("Z (meters)", color="white")
ax.tick_params(colors="white")

# Add title
ax.set_title("Helical Motion of a Charged Particle in a Magnetic Field", color="white")

# Initialize the line and point objects
(line,) = ax.plot([], [], [], "b-")
(point,) = ax.plot([], [], [], "bo")  # The moving particle


# Initialize the plot
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point


# Update function for animation
def update(frame):
    idx = frame * int(num_steps / 200)  # Use a subset of points for the animation
    line.set_data(r_vals[:idx, 0], r_vals[:idx, 1])
    line.set_3d_properties(r_vals[:idx, 2])
    point.set_data(
        [r_vals[idx, 0]], [r_vals[idx, 1]]
    )  # Pass sequences with one element
    point.set_3d_properties([r_vals[idx, 2]])  # Pass sequences with one element
    return line, point


# Create the animation
ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=50)

plt.show()
