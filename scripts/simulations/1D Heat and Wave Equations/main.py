import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numba
from scipy.sparse import diags
from scipy.sparse.linalg import splu
# Define the spatial and temporal parameters
L = 10.0    # Length of the spatial domain
T = 500.0     # Total time for the simulation
Nx = 500    # Number of spatial steps for higher resolution
dx = L / (Nx - 1)  # Corrected spatial step size

# Stability conditions
c = 1.0  # Wave speed
alpha_heat_max = 0.5  # Maximum allowed value for alpha_heat
alpha_wave_max = 1.0  # Maximum allowed value for alpha_wave

# Introduce a safety factor to ensure stability
safety_factor = 0.9

# Determine the maximum allowed dt for stability
dt_heat =  safety_factor * alpha_heat_max * dx**2
dt_wave = safety_factor * dx / c

# Use the smaller dt for both equations to ensure stability
dt = min(dt_heat, dt_wave)
Nt = int(T / dt)
dt =T / Nt  # Recalculate dt to fit exactly into T

# Recalculate alphas
alpha_heat = dt / dx**2
alpha_wave = (c * dt / dx)**2

# Check stability conditions
print(f"alpha_heat = {alpha_heat:.5f} (should be <= 0.5)")
print(f"alpha_wave = {alpha_wave:.5f} (should be <= 1.0)")

if alpha_heat >= alpha_heat_max:
    print(f"Warning: The heat equation solver may be unstable (alpha_heat = {alpha_heat:.2f} >= 0.5).")
if alpha_wave >= alpha_wave_max:
    print(f"Warning: The wave equation solver may be unstable (Courant number = {np.sqrt(alpha_wave):.2f} >= 1).")

# Initialize the spatial grid and initial conditions with float32
x = np.linspace(0, L, Nx, dtype=np.float32)

# Adjusted initial condition for the heat equation (broader Gaussian pulse)
f_initial_heat = np.exp(-5 * (x - L/2)**2).astype(np.float32)

# Adjusted initial condition for the wave equation (broader Gaussian pulse)
f_initial_wave = np.exp(-5 * (x - L/2)**2).astype(np.float32)
f_prev_wave = f_initial_wave.copy()

# Arrays to hold the solutions
f_heat = f_initial_heat.copy()
f_wave = f_initial_wave.copy()
f_new_heat = np.zeros_like(f_heat)
f_new_wave = np.zeros_like(f_wave)

# Set up the figure and axes with dark background
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), facecolor='black')

# Set the axes backgrounds to black
ax1.set_facecolor('black')
ax2.set_facecolor('black')

# Initialize line plots with light colors
line_heat, = ax1.plot(x, f_heat, color='cyan', lw=2)
line_wave, = ax2.plot(x, f_wave, color='magenta', lw=2)

# Set axis labels and titles with light colors
ax1.set_title("Heat Equation", fontsize=16, color='white')
ax2.set_title("Wave Equation", fontsize=16, color='white')
ax1.set_ylabel('Amplitude', fontsize=14, color='white')
ax2.set_ylabel('Amplitude', fontsize=14, color='white')
ax2.set_xlabel('Spatial Coordinate $x$', fontsize=14, color='white')

# Set axis limits
ax1.set_xlim(0, L)
ax2.set_xlim(0, L)
ax1.set_ylim(-0.1, 1.1)
ax2.set_ylim(-1.1, 1.1)

# Customize grid lines for better visibility on dark background
ax1.grid(False)
ax2.grid(False)

# Adjust tick parameters to have light-colored ticks and labels
for ax in [ax1, ax2]:
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

# Time annotations on axes with light text
time_template = 'Time = %.4f s'
time_text1 = ax1.text(0.75, 0.85, '', transform=ax1.transAxes, fontsize=14,
                      color='white', bbox=dict(facecolor='black', alpha=0.5))
time_text2 = ax2.text(0.75, 0.85, '', transform=ax2.transAxes, fontsize=14,
                      color='white', bbox=dict(facecolor='black', alpha=0.5))

# Construct the Crank-Nicolson matrix for the heat equation
main_diag = (1 + alpha_heat) * np.ones(Nx)
off_diag = (-alpha_heat / 2) * np.ones(Nx - 1)
A = diags([off_diag, main_diag, off_diag], offsets=[-1, 0, 1]).tocsc()
lu = splu(A)  # Precompute LU decomposition for efficiency

@numba.njit
def update_wave(f_prev_wave, f_wave, f_new_wave, alpha_wave):
    f_new_wave[1:-1] = (
        2 * f_wave[1:-1]
        - f_prev_wave[1:-1]
        + alpha_wave * (f_wave[2:] - 2 * f_wave[1:-1] + f_wave[:-2])
    )
    # Apply Dirichlet boundary conditions
    f_new_wave[0] = 0
    f_new_wave[-1] = 0
    # Update f_prev_wave and f_wave for next iteration
    f_prev_wave[:], f_wave[:] = f_wave[:], f_new_wave[:]

def implicit_update_heat(f_heat, f_new_heat, lu):
    # Solve A * f_new = f_heat
    f_new = lu.solve(f_heat)
    f_new_heat[:] = f_new
    f_heat[:] = f_new_heat[:]

# Update function for the animation
def animate(i):
    global f_heat, f_wave, f_prev_wave
    implicit_update_heat(f_heat, f_new_heat, lu)
    update_wave(f_prev_wave, f_wave, f_new_wave, alpha_wave)
    line_heat.set_ydata(f_heat)
    line_wave.set_ydata(f_wave)
    current_time = (i + 1) * dt
    time_text1.set_text(time_template % current_time)
    time_text2.set_text(time_template % current_time)
    return [line_heat, line_wave, time_text1, time_text2]


# Create the animation with blitting
ani = animation.FuncAnimation(fig, animate, frames=Nt, interval=20, blit=True, repeat=False)

plt.tight_layout()
plt.show()
