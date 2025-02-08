def plot_archimedes_principle(object_density, fluid_density=1000, object_volume=1):
    # Constants
    g = 9.81  # gravitational acceleration (m/s^2)
    
    # Forces
    weight = object_density * object_volume * g  # Weight of the object
    buoyant_force = fluid_density * object_volume * g  # Buoyant force

    # Determine if the object floats or sinks
    floats = buoyant_force >= weight

    # Plot setup
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Draw water
    ax.add_patch(patches.Rectangle((0, 0), 4, 4, color='skyblue', alpha=0.5))

    # Draw object
    object_height = 1
    object_position = 3 if floats else 1  # Floating or sunken position
    ax.add_patch(patches.Rectangle((1.5, object_position), 1, object_height, color='brown'))

    # Draw forces
    ax.annotate('', xy=(2, object_position + object_height), xytext=(2, object_position + object_height + 1),
                arrowprops=dict(arrowstyle='->', lw=2),
                annotation_clip=False)
    ax.text(2.1, object_position + object_height + 0.5, 'Buoyant Force', va='center')

    ax.annotate('', xy=(2, object_position), xytext=(2, object_position - 1),
                arrowprops=dict(arrowstyle='->', lw=2),
                annotation_clip=False)
    ax.text(2.1, object_position - 0.5, 'Weight', va='center')

    # Title and labels
    ax.set_title("Archimedes' Principle Demonstration")
    ax.set_xlim(0, 4)
    ax.set_ylim(-1, 5)
    ax.axis('off')

    # Display object status
    if floats:
        ax.text(0.5, 1.5, "The object floats because the buoyant force >= weight.", fontsize=12, color='green')
    else:
        ax.text(0.5, 4.5, "The object sinks because the weight > buoyant force.", fontsize=12, color='red')

    plt.show()

# Example usage
plot_archimedes_principle(object_density=500)  # Adjust density to see different behaviors
