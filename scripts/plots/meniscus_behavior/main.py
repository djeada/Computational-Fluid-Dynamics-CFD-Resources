import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Water in glass: upward meniscus
axes[0].plot([-1, 1], [0, 0], "navy", linewidth=2)  # flat water surface outside
water_meniscus = np.linspace(-1, 1, 100)
axes[0].plot(water_meniscus, 0.5 * water_meniscus**2, "skyblue", linewidth=3)
axes[0].fill_between(
    water_meniscus, 0.5 * water_meniscus**2, 1, color="skyblue", alpha=0.4
)
axes[0].text(0, 0.6, "Water climbs", ha="center", fontsize=12, color="navy")
axes[0].text(0, -0.2, "flat water surface outside", ha="center", fontsize=10)
axes[0].set_title("(a) Water in Glass: Upward Meniscus", fontsize=14)
axes[0].axis("off")
axes[0].set_ylim(-0.5, 1)

# Mercury in glass: downward meniscus
axes[1].plot([-1, 1], [0, 0], "grey", linewidth=2)  # flat mercury surface outside
mercury_meniscus = np.linspace(-1, 1, 100)
axes[1].plot(mercury_meniscus, -0.5 * mercury_meniscus**2, "silver", linewidth=3)
axes[1].fill_between(
    mercury_meniscus, -0.5 * mercury_meniscus**2, -1, color="silver", alpha=0.6
)
axes[1].text(0, -0.8, "Mercury dips", ha="center", fontsize=12, color="black")
axes[1].text(0, 0.2, "flat mercury surface outside", ha="center", fontsize=10)
axes[1].set_title("(b) Mercury in Glass: Downward Meniscus", fontsize=14)
axes[1].axis("off")
axes[1].set_ylim(-1, 0.5)

fig.suptitle("Visualization of Meniscus Behavior", fontsize=16)
plt.show()
