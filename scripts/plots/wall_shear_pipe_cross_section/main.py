import matplotlib.pyplot as plt
import numpy as np


def plot_wall_shear(pipe_radius=1, max_velocity=2):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the pipe cross-section
    circle = plt.Circle((0, 0), pipe_radius, color="gray", alpha=0.2)
    ax.add_artist(circle)

    # Draw velocity vectors
    radii = np.linspace(0, pipe_radius, 5)
    for r in radii:
        velocity = max_velocity * (1 - (r / pipe_radius) ** 2)  # Parabolic profile
        ax.arrow(
            0,
            r,
            velocity / 2,
            0,
            head_width=0.05,
            head_length=0.1,
            fc="blue",
            ec="blue",
        )
        ax.arrow(
            0,
            -r,
            velocity / 2,
            0,
            head_width=0.05,
            head_length=0.1,
            fc="blue",
            ec="blue",
        )

    # Annotate maximum velocity
    ax.text(
        max_velocity / 2 + 0.2,
        0,
        "Maximum Velocity\n(r=0)",
        ha="left",
        va="center",
        fontsize=10,
    )

    # Annotate velocity gradient
    ax.text(
        0,
        pipe_radius / 2,
        "~~~~ Velocity Gradient ~~~~",
        ha="center",
        va="center",
        fontsize=10,
        color="black",
    )

    # Annotate no-slip condition
    ax.annotate(
        "No-slip Condition\n(v = 0)",
        xy=(0, pipe_radius),
        xytext=(-1.5, pipe_radius + 0.2),
        arrowprops=dict(arrowstyle="->"),
        ha="center",
        fontsize=10,
    )

    # Annotate high shear region
    ax.annotate(
        "High Shear Region",
        xy=(pipe_radius, 0),
        xytext=(1.2, -0.5),
        arrowprops=dict(arrowstyle="->"),
        ha="center",
        fontsize=10,
    )

    # Add descriptive text
    ax.text(
        0,
        -1.5,
        "Wall shear ~ friction force that fluid exerts on the pipe walls",
        ha="center",
        fontsize=11,
        wrap=True,
    )

    # Settings
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.title("Wall Shear in Pipe Cross-Section", fontsize=14)
    plt.show()


# Example usage
plot_wall_shear()
