import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Generate sample data
np.random.seed(0)
Cd = np.random.rand(50) * 0.2 + 0.15  # Random data for Cd in range 0.15 to 0.35
Cd_pred_red = Cd + (np.random.rand(50) * 0.05 - 0.025)  # Red markers
Cd_pred_blue = Cd + (np.random.rand(50) * 0.05 - 0.025)  # Blue markers

# Perform linear regression
slope_red, intercept_red, r_value_red, p_value_red, std_err_red = linregress(
    Cd, Cd_pred_red
)
slope_blue, intercept_blue, r_value_blue, p_value_blue, std_err_blue = linregress(
    Cd, Cd_pred_blue
)
regression_line_red = slope_red * Cd + intercept_red
regression_line_blue = slope_blue * Cd + intercept_blue

# Plot the data
plt.figure(figsize=(8, 6))
plt.scatter(Cd, Cd_pred_red, color="red", marker="+", label="Red markers", s=100)
plt.scatter(Cd, Cd_pred_blue, color="blue", marker="o", label="Blue markers", s=60)

# Plot regression lines
plt.plot(
    Cd,
    regression_line_red,
    color="red",
    linestyle="--",
    label=f"Red Fit: y={slope_red:.2f}x+{intercept_red:.2f}",
)
plt.plot(
    Cd,
    regression_line_blue,
    color="blue",
    linestyle="-.",
    label=f"Blue Fit: y={slope_blue:.2f}x+{intercept_blue:.2f}",
)

# Add titles and labels
plt.title("Model C", fontsize=14)
plt.xlabel("Cd", fontsize=12)
plt.ylabel("Cd_pred", fontsize=12)

# Add legend
plt.legend(loc="upper left", fontsize=10)

# Add grid
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Set axis limits for better visualization
plt.xlim(0.14, 0.36)
plt.ylim(0.14, 0.37)

# Show plot
plt.tight_layout()
plt.show()
