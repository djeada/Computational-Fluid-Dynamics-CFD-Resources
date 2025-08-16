import numpy as np
import matplotlib.pyplot as plt


def draw_ship_hull_and_waves():
    """
    Draws a simple representation of a ship hull and waves at the free surface.
    """

    # Create a figure for the hull visualization
    plt.figure(figsize=(7, 5))

    # ---------------------------
    # Wave pattern at the surface
    # ---------------------------
    x_wave = np.linspace(-2, 12, 300)  # Extend beyond the hull region for clarity
    # A small sine wave representing free-surface undulation
    y_wave = 0.1 * np.sin(2.0 * np.pi * x_wave / 4.0)

    # Plot the free surface wave
    plt.plot(x_wave, y_wave, label="Free Surface Wave")

    # ---------------
    # Hull geometry
    # ---------------
    # A simple, stylized hull (2D cross-section) from x=0 (bow) to x=10 (stern).
    # This shape is purely illustrative and does not represent a specific vessel.
    x_hull = np.array([0.0, 1.5, 4.0, 6.0, 8.5, 10.0])
    y_hull = np.array([0.0, -0.5, -0.7, -0.7, -0.5, 0.0])

    # Fill the hull
    plt.fill(x_hull, y_hull, alpha=0.5, label="Ship Hull")

    # -----------------------------
    # Velocity vector (arrow) & text
    # -----------------------------
    # Place an arrow above the hull, indicating direction of flow (to the right).
    plt.arrow(1, 0.5, 2.0, 0.0, width=0.02, head_width=0.1, length_includes_head=True)
    plt.text(1, 0.65, "Velocity U", fontsize=10)

    # -----------------------------
    # Annotations
    # -----------------------------
    # Show the waterline level (y=0) as a reference
    plt.axhline(0, linestyle="--", label="Still Water Level")

    # Add the Froude number formula as a reminder
    plt.text(5, 0.7, r"$Fr = \frac{U}{\sqrt{g \, L}}$", fontsize=12, ha="center")

    # -----------------------------
    # Plot settings
    # -----------------------------
    plt.title("Ship Hull and Wave Pattern – Froude Number Concept")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.axis("equal")  # Same scale for x and y
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    draw_ship_hull_and_waves()
