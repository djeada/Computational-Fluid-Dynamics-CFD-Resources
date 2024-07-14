import numpy as np
from matplotlib import animation, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define parameters for the 3D Schrödinger equation
L = 10.0
N = 100
dx = L / N
x = np.linspace(-L/2, L/2, N)
y = np.linspace(-L/2, L/2, N)
dt = 0.01
T = 1.0
t_steps = int(T / dt)
speed_factor = 5  # Speed factor for the animation

X, Y = np.meshgrid(x, y)

# Initial wavefunction: 2D Gaussian
def psi_0(X, Y):
    return np.exp(-(X**2 + Y**2) / 2)

# Potential (free particle, so V=0 everywhere)
V = np.zeros_like(X)

# Initialize wavefunction
psi = psi_0(X, Y)

# Precompute the Fourier transform components
kx = np.fft.fftfreq(N, d=dx) * 2 * np.pi
ky = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY = np.meshgrid(kx, ky)
K2 = KX**2 + KY**2

# Time evolution function using the split-step Fourier method
def evolve(psi, dt, dx, V):
    psi_ft = np.fft.fft2(psi)
    psi_ft = psi_ft * np.exp(-1j * dt * 0.5 * K2)
    psi = np.fft.ifft2(psi_ft)
    psi = psi * np.exp(-1j * dt * V)
    return psi

# Set up the figure and axis
fig = plt.figure(facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

# Plotting the initial frame
wave = np.abs(psi)**2
surf = ax.plot_surface(X, Y, wave, cmap='viridis')

cax = fig.add_axes([0.05, 0.15, 0.02, 0.7])  # [left, bottom, width, height]
mappable = plt.cm.ScalarMappable(cmap='viridis')
mappable.set_array(wave)
cbar = plt.colorbar(mappable, cax=cax)
cbar.ax.tick_params(color='white', labelcolor='white')
cbar.outline.set_edgecolor('white')

ax.set_xlim(-L/2, L/2)
ax.set_ylim(-L/2, L/2)
ax.set_zlim(0, np.max(wave))
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')
ax.set_zlabel('|ψ|^2', color='white')
ax.set_title('Time Evolution of Schrödinger Equation in 2D', color='white')

# Set white color for all tick labels
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.tick_params(axis='z', colors='white')

def update(frame):
    global psi
    for _ in range(speed_factor):  # Evolve multiple steps per frame to speed up the animation
        psi = evolve(psi, dt, dx, V)
    wave = np.abs(psi)**2
    ax.clear()
    surf = ax.plot_surface(X, Y, wave, cmap='viridis')
    ax.set_xlim(-L/2, L/2)
    ax.set_ylim(-L/2, L/2)
    ax.set_zlim(0, 1)  # Fixed z-axis limit
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('|ψ|^2', color='white')
    ax.set_title('Time Evolution of Schrödinger Equation in 2D', color='white')
    # Keep the color bar static
    mappable.set_array(wave)
    cbar.update_normal(mappable)
    return ax

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=t_steps // speed_factor, blit=False)

# To prevent the animation from being garbage collected
anim = ani

plt.show()
