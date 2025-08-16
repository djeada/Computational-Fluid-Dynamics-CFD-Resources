def plot_flow_rate(pipe_radius=0.1, velocity=2, length=5):
    # Constants
    area = np.pi * pipe_radius**2  # Cross-sectional area
    flow_rate = area * velocity  # Flow rate Q = A * v

    # Plot setup
    fig, ax = plt.subplots(figsize=(10, 4))

    # Draw the pipe
    ax.add_patch(
        plt.Rectangle(
            (0, -pipe_radius), length, 2 * pipe_radius, color="gray", alpha=0.3
        )
    )

    # Draw flow arrows
    x_positions = np.linspace(0.5, length - 0.5, 8)
    y_positions = np.linspace(-pipe_radius * 0.8, pipe_radius * 0.8, 5)

    for x in x_positions:
        for y in y_positions:
            ax.annotate(
                "",
                xy=(x + 0.4, y),
                xytext=(x, y),
                arrowprops=dict(arrowstyle="->", lw=2, color="blue"),
            )

    # Annotate flow rate (moved above the pipe to avoid overlapping)
    ax.text(
        length / 2,
        pipe_radius * 2,
        f"Flow Rate: {flow_rate:.3f} m³/s",
        ha="center",
        fontsize=12,
        color="black",
    )

    # Settings
    ax.set_xlim(-0.5, length + 0.5)
    ax.set_ylim(-pipe_radius * 3, pipe_radius * 3)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.title("Flow Rate Through a Pipe")
    plt.show()


# Example usage
plot_flow_rate(pipe_radius=0.1, velocity=2, length=5)
