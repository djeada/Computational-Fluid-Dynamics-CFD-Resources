import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize

# Define grid size and parameters
grid_size = 20
num_grains = 1000  # Total grains to add over time
critical_height = 8

# Initialize grid
grid = np.zeros((grid_size, grid_size), dtype=int)


# Toppling function with cascading effect
def topple(grid):
    unstable = True
    while unstable:
        unstable = False
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i, j] >= critical_height:
                    grid[i, j] -= critical_height
                    if i > 0:
                        grid[i - 1, j] += 1  # top neighbor
                    if i < grid_size - 1:
                        grid[i + 1, j] += 1  # bottom neighbor
                    if j > 0:
                        grid[i, j - 1] += 1  # left neighbor
                    if j < grid_size - 1:
                        grid[i, j + 1] += 1  # right neighbor
                    unstable = True



# Prepare the figure and axis for 3D plotting with dark background
fig = plt.figure(figsize=(12, 8), facecolor='black')

# Define the position of the 3D plot and color bar
# [left, bottom, width, height]
ax = fig.add_axes([0.3, 0.1, 0.65, 0.8], projection='3d', facecolor='black')

# Create a separate axes for the color bar on the left
cbar_ax = fig.add_axes([0.1, 0.1, 0.02, 0.8])  # [left, bottom, width, height]

# Create meshgrid for plotting
x, y = np.meshgrid(range(grid_size), range(grid_size))

# Normalize the color scale based on z-axis limits
norm = Normalize(vmin=0, vmax=10)

# Initial plot setup (set z-axis limits for better visualization)
ax.set_zlim(0, 10)
ax.set_xlabel('X-axis', fontsize=12, color='white')
ax.set_ylabel('Y-axis', fontsize=12, color='white')
ax.set_zlabel('Grains (Height)', fontsize=12, color='white')
ax.set_title('Bak-Tang-Wiesenfeld Sandpile Model: Evolution Over Time', fontsize=14, color='white')

# Customize the axes background and grid
ax.xaxis.pane.set_facecolor('black')
ax.yaxis.pane.set_facecolor('black')
ax.zaxis.pane.set_facecolor('black')

# Customize grid lines for better visibility on dark background
ax.grid(True, color='gray', linestyle='--', linewidth=0.5)

# Adjust tick parameters to have light-colored ticks and labels
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.tick_params(axis='z', colors='white')

# Initial plot_surface (empty grid)
surf = ax.plot_surface(x, y, grid, cmap='plasma', norm=norm, edgecolor='k', linewidth=0.5, antialiased=True)

# Create the color bar
cbar = fig.colorbar(surf, cax=cbar_ax, orientation='vertical')
cbar.set_label('Grains (Height)', color='white', fontsize=12)
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')


# Update function for the animation
def update(frame):
    global surf
    # Add a grain to a random position
    x_pos, y_pos = np.random.randint(0, grid_size, 2)
    grid[x_pos, y_pos] += 1

    # Topple the sandpile to stabilize after adding a grain
    topple(grid)

    # Remove existing surface collections
    # Iterate over a copy of the collections list to avoid modification issues
    for coll in ax.collections[:]:
        coll.remove()

    # Re-plot the surface with updated grid
    surf = ax.plot_surface(x, y, grid, cmap='plasma', norm=norm, edgecolor='k', linewidth=0.5, antialiased=True)

    return surf,

# Create the animation without using tight_layout
ani = animation.FuncAnimation(fig, update, frames=num_grains, interval=20, blit=False)

# Show the animation
plt.show()
