import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set up the domain
nx, ny = 40, 10  # Increase the grid resolution for a smoother plot
xmax, ymax = 10.0, 2.0
x = np.linspace(0, xmax, nx)
y = np.linspace(0, ymax, ny)
X, Y = np.meshgrid(x, y)

# -----------------------------------------------------------------------------
# Incompressible Flow:
#   - Parabolic profile in y, constant along x
#   - Typical laminar flow in a rectangular duct
# -----------------------------------------------------------------------------
# Center-line at y_mid = ymax/2. We'll define a simple parabola:
#     U_incomp(y) = U_max * [1 - ((y - y_mid)/(y_mid))^2]
# so the max velocity is at the center y = y_mid and zero at the walls.
y_mid = ymax / 2.0
U_max_incomp = 2.0  # you can tweak this for a more distinct difference
u_incomp = U_max_incomp * (1.0 - ((Y - y_mid) / y_mid) ** 2)
u_incomp = np.clip(
    u_incomp, 0, None
)  # Parabolic shape can go negative if outside the range
v_incomp = np.zeros_like(u_incomp)

# -----------------------------------------------------------------------------
# Compressible Flow (highly simplified):
#   - Velocity profile also parabolic in y,
#   - Increases from left (x=0) to right (x=xmax).
# -----------------------------------------------------------------------------
# We'll say the velocity at x=0 is half of the incompressible's maximum,
# and grows to something larger by x = xmax.
U_inlet = 1.0  # smaller than incompressible peak
U_outlet = 4.0  # distinctly larger to emphasize acceleration
U_slope = (U_outlet - U_inlet) / xmax

# Parabolic shape in y again:
u_parab = 1.0 - ((Y - y_mid) / y_mid) ** 2
u_parab = np.clip(u_parab, 0, None)

# Now make it depend on x:
#   U(x,y) = [U_inlet + U_slope * x] * [parabolic in y]
# This way, speed increases significantly in the downstream direction.
u_comp = (U_inlet + U_slope * X) * u_parab
v_comp = np.zeros_like(u_comp)

# Compute speed for color mapping
speed_incomp = np.sqrt(u_incomp**2 + v_incomp**2)
speed_comp = np.sqrt(u_comp**2 + v_comp**2)

# Create side-by-side subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# -----------------------------------------------------------------------------
# Left subplot: Incompressible flow
# -----------------------------------------------------------------------------
# Draw a rectangle to outline the pipe
axes[0].add_patch(Rectangle((0, 0), xmax, ymax, fill=False, linewidth=1))

# Use pcolormesh for a filled contour of velocity magnitude
c1 = axes[0].pcolormesh(X, Y, speed_incomp, shading="auto")
# Add a colorbar for velocity magnitude
cb1 = fig.colorbar(c1, ax=axes[0], label="Velocity Magnitude")

# Overlay velocity vectors
axes[0].quiver(X, Y, u_incomp, v_incomp, color="white", scale=15)

axes[0].set_xlim([0, xmax])
axes[0].set_ylim([0, ymax])
axes[0].set_aspect("equal", adjustable="box")
axes[0].set_title("Incompressible Flow (Laminar Parabolic)")

# -----------------------------------------------------------------------------
# Right subplot: Compressible flow
# -----------------------------------------------------------------------------
axes[1].add_patch(Rectangle((0, 0), xmax, ymax, fill=False, linewidth=1))

# Filled contour of velocity magnitude
c2 = axes[1].pcolormesh(X, Y, speed_comp, shading="auto")
fig.colorbar(c2, ax=axes[1], label="Velocity Magnitude")

# Velocity vectors
axes[1].quiver(X, Y, u_comp, v_comp, color="white", scale=15)

axes[1].set_xlim([0, xmax])
axes[1].set_ylim([0, ymax])
axes[1].set_aspect("equal", adjustable="box")
axes[1].set_title("Compressible Flow (Increasing Speed)")

plt.tight_layout()
plt.show()
