import numpy as np
import matplotlib.pyplot as plt

# Parameters
U_inf = 1.0  # Free-stream velocity
delta = 0.05  # Boundary layer thickness
num_points = 100  # Number of points

# Generate Y-coordinates
Y = np.linspace(0, 2 * delta, num_points)

# Calculate U-velocity components using a simplified parabolic profile
U0 = U_inf * (Y / delta)**0.5
U1 = np.zeros(num_points)  # Assuming no flow in the Y direction
U2 = np.zeros(num_points)  # Assuming no flow in the Z direction

# Add some noise for a more realistic simulation
U0 += np.random.normal(0, 0.02, num_points)

# Save the data to a CSV file
data = np.column_stack((U0, U1, U2, np.zeros(num_points), Y, np.zeros(num_points)))
np.savetxt("boundary_layer_data.csv", data, delimiter=',', header="U0,U1,U2,X,Y,Z", comments='')

# Plot U0 versus Y
plt.figure()
plt.plot(Y, U0, "*")
plt.xlabel('Y [m]')
plt.ylabel('U0')
plt.title('U0 versus Y')
plt.grid()
plt.savefig("U0_vs_Y.png")
plt.show()

# Plot U versus Y
plt.figure()
plt.plot(Y, U0, "*", label='U0')
plt.plot(Y, U1, "-", label='U1')
plt.plot(Y, U2, ".", label='U2')
plt.xlabel('Y [m]')
plt.ylabel('U')
plt.title('U versus Y')
plt.legend(loc='center left', bbox_to_anchor=(0.6, 0.815), numpoints=2)
plt.grid()
plt.savefig("U_vs_Y.png")
plt.show()
