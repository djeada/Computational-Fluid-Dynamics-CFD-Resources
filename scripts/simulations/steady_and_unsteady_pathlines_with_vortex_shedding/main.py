import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Apply dark background style
plt.style.use("dark_background")

R = 1.0  # Radius of the cylinder
U = 1.0  # Free stream velocity
Gamma = 4 * np.pi * R * U  # Circulation
x = np.linspace(-5, 10, 300)
y = np.linspace(-5, 5, 300)
X, Y = np.meshgrid(x, y)


class Vortex:
    def __init__(self, x, y, gamma):
        self.x = x
        self.y = y
        self.gamma = gamma

    def velocity(self, X, Y):
        dx = X - self.x
        dy = Y - self.y
        r2 = dx**2 + dy**2
        r2 = np.where(r2 == 0, 1e-10, r2)
        Ux = self.gamma / (2 * np.pi) * (-dy) / r2
        Uy = self.gamma / (2 * np.pi) * dx / r2
        return Ux, Uy


def steady_velocity(X, Y, vortices):
    mask = X**2 + Y**2 < R**2
    theta = np.arctan2(Y, X)
    V_r = U * (1 - (R**2) / (X**2 + Y**2))
    V_theta = -U * (R**2) / (X**2 + Y**2) + Gamma / (2 * np.pi * (X**2 + Y**2))
    Ux = V_r * np.cos(theta) - V_theta * np.sin(theta)
    Uy = V_r * np.sin(theta) + V_theta * np.cos(theta)
    Ux = np.where(mask, np.nan, Ux)
    Uy = np.where(mask, np.nan, Uy)
    for vortex in vortices:
        Vu, Vv = vortex.velocity(X, Y)
        Ux += Vu
        Uy += Vv
    return Ux, Uy


def velocity_at_point(x, y, vortices):
    r2 = x**2 + y**2
    if r2 < R**2:
        return np.nan, np.nan
    theta = np.arctan2(y, x)
    V_r = U * (1 - (R**2) / r2)
    V_theta = -U * (R**2) / r2 + Gamma / (2 * np.pi * r2)
    Ux = V_r * np.cos(theta) - V_theta * np.sin(theta)
    Uy = V_r * np.sin(theta) + V_theta * np.cos(theta)
    for vortex in vortices:
        dx = x - vortex.x
        dy = y - vortex.y
        r2_vortex = dx**2 + dy**2
        if r2_vortex == 0:
            continue
        Ux += vortex.gamma / (2 * np.pi) * (-dy) / r2_vortex
        Uy += vortex.gamma / (2 * np.pi) * dx / r2_vortex
    return Ux, Uy


def rk4_step(U_func, pos, vortices, t, dt):
    k1x, k1y = U_func(pos[0], pos[1], vortices)
    if np.isnan(k1x) or np.isnan(k1y):
        return np.array([np.nan, np.nan])
    k2x, k2y = U_func(pos[0] + 0.5 * dt * k1x, pos[1] + 0.5 * dt * k1y, vortices)
    if np.isnan(k2x) or np.isnan(k2y):
        return np.array([np.nan, np.nan])
    k3x, k3y = U_func(pos[0] + 0.5 * dt * k2x, pos[1] + 0.5 * dt * k2y, vortices)
    if np.isnan(k3x) or np.isnan(k3y):
        return np.array([np.nan, np.nan])
    k4x, k4y = U_func(pos[0] + dt * k3x, pos[1] + dt * k3y, vortices)
    if np.isnan(k4x) or np.isnan(k4y):
        return np.array([np.nan, np.nan])
    x_new = pos[0] + (dt / 6.0) * (k1x + 2 * k2x + 2 * k3x + k4x)
    y_new = pos[1] + (dt / 6.0) * (k1y + 2 * k2y + 2 * k3y + k4y)
    return np.array([x_new, y_new])


def compute_pathlines_steady(particles, dt, nt):
    paths = [[pos.copy()] for pos in particles]
    positions = particles.copy()
    vortices = []
    for _ in range(nt):
        for i in range(len(positions)):
            if not np.isnan(positions[i, 0]) and not np.isnan(positions[i, 1]):
                pos = positions[i]
                new_pos = rk4_step(velocity_at_point, pos, vortices, 0, dt)
                if not np.isnan(new_pos[0]) and not np.isnan(new_pos[1]):
                    if new_pos[0] ** 2 + new_pos[1] ** 2 < R**2:
                        positions[i] = np.array([np.nan, np.nan])
                    else:
                        positions[i] = new_pos
                else:
                    positions[i] = np.array([np.nan, np.nan])
                paths[i].append(positions[i].copy())
    return paths


def unsteady_velocity(X, Y, t, vortices):
    """Compute unsteady velocity field including contributions from vortices."""
    mask = X**2 + Y**2 < R**2
    theta = np.arctan2(Y, X)
    V_r = U * (1 - (R**2) / (X**2 + Y**2))
    V_theta = -U * (R**2) / (X**2 + Y**2) + Gamma / (2 * np.pi * (X**2 + Y**2))
    Ux = V_r * np.cos(theta) - V_theta * np.sin(theta)
    Uy = V_r * np.sin(theta) + V_theta * np.cos(theta)
    Ux = np.where(mask, np.nan, Ux)
    Uy = np.where(mask, np.nan, Uy)

    for vortex in vortices:
        Vu, Vv = vortex.velocity(X, Y)
        Ux += Vu
        Uy += Vv

    return Ux, Uy


def compute_pathlines_unsteady(particles, dt, nt, shed_interval=2.0):
    paths = [[pos.copy()] for pos in particles]
    positions = particles.copy()
    vortices = []
    t = 0.0
    for step in range(nt):
        # Shed a vortex periodically
        if step % int(shed_interval / dt) == 0:
            y_shed = R if (step // int(shed_interval / dt)) % 2 == 0 else -R
            vortices.append(Vortex(R, y_shed, vortex_strength))

        for i in range(len(positions)):
            if not np.isnan(positions[i, 0]) and not np.isnan(positions[i, 1]):
                pos = positions[i]
                new_pos = rk4_step(
                    lambda x, y, vs: unsteady_velocity(x, y, t, vs),
                    pos,
                    vortices,
                    t,
                    dt,
                )
                if not np.isnan(new_pos[0]) and not np.isnan(new_pos[1]):
                    if new_pos[0] ** 2 + new_pos[1] ** 2 < R**2:
                        positions[i] = np.array([np.nan, np.nan])
                    else:
                        positions[i] = new_pos
                else:
                    positions[i] = np.array([np.nan, np.nan])
                paths[i].append(positions[i].copy())
        t += dt
    return paths


# Initialize vortices list
vortices = []
dt = 0.05
nt = 300
t0 = 0.0
shed_side = 1
vortex_strength = Gamma / 2

# Modify particle initialization for uniform distribution around the cylinder
num_particles = 30  # Increased number for better distribution
angles = np.linspace(0, 2 * np.pi, num_particles, endpoint=False)
r_init = 2.0  # Radius for initial particle positions
particles = np.empty((num_particles, 2))
particles[:, 0] = r_init * np.cos(angles)
particles[:, 1] = r_init * np.sin(angles)

paths_steady = compute_pathlines_steady(particles, dt, nt)
paths_unsteady = compute_pathlines_unsteady(particles, dt, nt)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Steady Flow Plot
ax_steady = axes[0]
ax_steady.set_title("Steady Flow\nStreamlines and Pathlines coincide", color="white")
ax_steady.set_xlim(-5, 10)
ax_steady.set_ylim(-5, 5)
ax_steady.set_aspect("equal")
cylinder_steady = Circle((0, 0), R, color="white", zorder=5)
ax_steady.add_patch(cylinder_steady)
Ux_s, Uy_s = steady_velocity(X, Y, [])
stream_steady = ax_steady.streamplot(
    X,
    Y,
    Ux_s,
    Uy_s,
    color="cyan",
    linewidth=1.5,
    density=1.5,
    arrowstyle="->",
    arrowsize=1.5,
)
lines_steady = [
    ax_steady.plot([], [], linewidth=1.5, color="lime")[0] for _ in range(num_particles)
]
points_steady = [
    ax_steady.plot([], [], marker="o", markersize=6, color="yellow")[0]
    for _ in range(num_particles)
]

# Unsteady Flow Plot
ax_unsteady = axes[1]
ax_unsteady.set_title(
    "Unsteady Flow with Vortex Shedding\nStreamlines and Pathlines differ",
    color="white",
)
ax_unsteady.set_xlim(-5, 10)
ax_unsteady.set_ylim(-5, 5)
ax_unsteady.set_aspect("equal")
cylinder_unsteady = Circle((0, 0), R, color="white", zorder=5)
ax_unsteady.add_patch(cylinder_unsteady)
Ux_u, Uy_u = steady_velocity(X, Y, vortices)
stream_unsteady = ax_unsteady.streamplot(
    X,
    Y,
    Ux_u,
    Uy_u,
    color="magenta",
    linewidth=1.5,
    density=1.5,
    arrowstyle="->",
    arrowsize=1.5,
)
lines_unsteady = [
    ax_unsteady.plot([], [], linewidth=1.5, color="orange")[0]
    for _ in range(num_particles)
]
points_unsteady = [
    ax_unsteady.plot([], [], marker="o", markersize=6, color="red")[0]
    for _ in range(num_particles)
]


def animate(frame):
    global shed_side, vortices
    t = t0 + frame * dt
    y_shed = shed_side * R
    vortices.append(Vortex(R, y_shed, vortex_strength))
    shed_side *= -1
    Ux_un, Uy_un = unsteady_velocity(X, Y, t, vortices)

    # Clear and redraw unsteady plot
    ax_unsteady.clear()
    ax_unsteady.set_title(
        "Unsteady Flow with Vortex Shedding\nStreamlines and Pathlines differ",
        color="white",
    )
    ax_unsteady.set_xlim(-5, 10)
    ax_unsteady.set_ylim(-5, 5)
    ax_unsteady.set_aspect("equal")
    cylinder_unsteady = Circle((0, 0), R, color="white", zorder=5)
    ax_unsteady.add_patch(cylinder_unsteady)
    stream_unsteady = ax_unsteady.streamplot(
        X,
        Y,
        Ux_un,
        Uy_un,
        color="magenta",
        linewidth=1.5,
        density=1.5,
        arrowstyle="->",
        arrowsize=1.5,
    )

    # Update steady pathlines
    for i, line in enumerate(lines_steady):
        if frame < len(paths_steady[i]):
            path = np.array(paths_steady[i][: frame + 1])
            line.set_data(path[:, 0], path[:, 1])
    for i, point in enumerate(points_steady):
        if frame < len(paths_steady[i]):
            pos = paths_steady[i][frame]
            if not np.isnan(pos[0]) and not np.isnan(pos[1]):
                point.set_data([pos[0]], [pos[1]])
            else:
                point.set_data([], [])

    # Update unsteady pathlines
    for i, line in enumerate(lines_unsteady):
        if frame < len(paths_unsteady[i]):
            path = np.array(paths_unsteady[i][: frame + 1])
            line.set_data(path[:, 0], path[:, 1])
    for i, point in enumerate(points_unsteady):
        if frame < len(paths_unsteady[i]):
            pos = paths_unsteady[i][frame]
            if not np.isnan(pos[0]) and not np.isnan(pos[1]):
                point.set_data([pos[0]], [pos[1]])
            else:
                point.set_data([], [])

    # Redraw lines and points on unsteady plot
    for ln in lines_unsteady:
        ax_unsteady.add_line(ln)
    for pt in points_unsteady:
        ax_unsteady.add_line(pt)

    return lines_steady + points_steady + lines_unsteady + points_unsteady


# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=nt, interval=50, blit=False)
plt.tight_layout()
plt.show()
