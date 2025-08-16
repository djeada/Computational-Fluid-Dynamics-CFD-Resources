import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from numpy import ndarray

# Constants
N_POINTS: int = 128
N_ITERATIONS: int = 300  # Increase the number of iterations for more steps
N_PRESSURE_POISSON_ITERATIONS: int = 50
TIME_STEP: float = 0.000003  # Smaller time step length for stability
KINEMATIC_VISCOSITY: float = 0.1
HORIZONTAL_VELOCITY: float = 1.0
EPSILON: float = 1e-6  # Small value to avoid zero range for contour levels
DENSITY: float = 1.0


# Functions
def central_difference_x(f: ndarray, element_length: float) -> ndarray:
    diff = np.zeros_like(f)
    diff[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * element_length)
    return diff


def central_difference_y(f: ndarray, element_length: float) -> ndarray:
    diff = np.zeros_like(f)
    diff[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2 * element_length)
    return diff


def laplace(f: ndarray, element_length: float) -> ndarray:
    lap = np.zeros_like(f)
    lap[1:-1, 1:-1] = (
        f[1:-1, :-2] + f[:-2, 1:-1] + f[1:-1, 2:] + f[2:, 1:-1] - 4 * f[1:-1, 1:-1]
    ) / (element_length**2)
    return lap


def apply_boundary_conditions(
    u: ndarray, v: ndarray, horizontal_velocity_top: float
) -> tuple[ndarray, ndarray]:
    u[0, :], u[:, 0], u[:, -1], u[-1, :] = 0.0, 0.0, 0.0, horizontal_velocity_top
    v[0, :], v[:, 0], v[:, -1], v[-1, :] = 0.0, 0.0, 0.0, 0.0
    return u, v


def solve_pressure_poisson(p: ndarray, rhs: ndarray, element_length: float) -> ndarray:
    for _ in range(N_PRESSURE_POISSON_ITERATIONS):
        p_next = np.copy(p)
        p_next[1:-1, 1:-1] = 0.25 * (
            p[1:-1, :-2]
            + p[:-2, 1:-1]
            + p[1:-1, 2:]
            + p[2:, 1:-1]
            - element_length**2 * rhs[1:-1, 1:-1]
        )
        p_next[:, -1] = p_next[:, -2]
        p_next[0, :] = p_next[1, :]
        p_next[:, 0] = p_next[1, :]
        p_next[-1, :] = 0.0
        p = p_next
    return p


def main() -> None:
    element_length = 1.0 / (N_POINTS - 1)
    x = np.linspace(0.0, 1.0, N_POINTS)
    y = np.linspace(0.0, 1.0, N_POINTS)
    X, Y = np.meshgrid(x, y)

    u = np.zeros((N_POINTS, N_POINTS))
    v = np.zeros((N_POINTS, N_POINTS))
    p = np.zeros((N_POINTS, N_POINTS))

    # Initialize with a small perturbation to help with the flow
    u[:, :] = 0.1

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), facecolor="black")
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    ax_u = axs[0]
    ax_v = axs[1]

    # Set titles and labels to white
    ax_u.set_title("Velocity (u)", color="white")
    ax_v.set_title("Velocity (v)", color="white")

    ax_u.set_xlim(0, 1.0)
    ax_u.set_ylim(0, 1.0)
    ax_u.set_aspect("equal")

    ax_v.set_xlim(0, 1.0)
    ax_v.set_ylim(0, 1.0)
    ax_v.set_aspect("equal")

    # Set axis labels and ticks to white
    for ax in axs:
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.spines["top"].set_color("white")
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["right"].set_color("white")

    # Initial contour plots
    contour_u = ax_u.contourf(
        X, Y, u, cmap="coolwarm", levels=np.linspace(np.min(u), np.max(u) + EPSILON, 20)
    )
    colorbar_u = fig.colorbar(contour_u, ax=ax_u)
    colorbar_u.ax.yaxis.set_tick_params(color="white")
    colorbar_u.ax.yaxis.set_tick_params(color="white")
    colorbar_u.outline.set_edgecolor("white")
    plt.setp(plt.getp(colorbar_u.ax.axes, "yticklabels"), color="white")

    contour_v = ax_v.contourf(
        X, Y, v, cmap="coolwarm", levels=np.linspace(np.min(v), np.max(v) + EPSILON, 20)
    )
    colorbar_v = fig.colorbar(contour_v, ax=ax_v)
    colorbar_v.ax.yaxis.set_tick_params(color="white")
    colorbar_v.outline.set_edgecolor("white")
    plt.setp(plt.getp(colorbar_v.ax.axes, "yticklabels"), color="white")

    # Text annotation for current iteration
    iteration_text = fig.suptitle("Iteration: 0", color="white")

    def update(frame: int) -> None:
        nonlocal u, v, p, contour_u, contour_v, colorbar_u, colorbar_v
        for _ in range(50):  # Inner loop for more steps per frame
            d_u_dx = central_difference_x(u, element_length)
            d_u_dy = central_difference_y(u, element_length)
            d_v_dx = central_difference_x(v, element_length)
            d_v_dy = central_difference_y(v, element_length)
            laplace_u = laplace(u, element_length)
            laplace_v = laplace(v, element_length)

            # Calculate tentative velocities
            u_tent = u + TIME_STEP * (
                -(u * d_u_dx + v * d_u_dy) + KINEMATIC_VISCOSITY * laplace_u
            )
            v_tent = v + TIME_STEP * (
                -(u * d_v_dx + v * d_v_dy) + KINEMATIC_VISCOSITY * laplace_v
            )

            u, v = apply_boundary_conditions(u_tent, v_tent, HORIZONTAL_VELOCITY)

            # Calculate the divergence of the velocity field
            rhs = (d_u_dx + d_v_dy) / TIME_STEP
            p = solve_pressure_poisson(p, rhs, element_length)

            d_p_dx = central_difference_x(p, element_length)
            d_p_dy = central_difference_y(p, element_length)

            u = u - TIME_STEP / DENSITY * d_p_dx
            v = v - TIME_STEP / DENSITY * d_p_dy

            u, v = apply_boundary_conditions(u, v, HORIZONTAL_VELOCITY)

        # Debug prints to verify intermediate values
        print(f"Frame: {frame + 1}")
        print(f"Max u: {np.max(u)}, Max v: {np.max(v)}, Max p: {np.max(p)}")

        # Remove previous contour plots and color bars
        for c in contour_u.collections:
            c.remove()
        for c in contour_v.collections:
            c.remove()
        colorbar_u.remove()
        colorbar_v.remove()

        # Update contour plots
        contour_u = ax_u.contourf(
            X,
            Y,
            u,
            cmap="coolwarm",
            levels=np.linspace(np.min(u), np.max(u) + EPSILON, 20),
        )
        colorbar_u = fig.colorbar(contour_u, ax=ax_u)
        colorbar_u.ax.yaxis.set_tick_params(color="white")
        colorbar_u.outline.set_edgecolor("white")
        plt.setp(plt.getp(colorbar_u.ax.axes, "yticklabels"), color="white")

        contour_v = ax_v.contourf(
            X,
            Y,
            v,
            cmap="coolwarm",
            levels=np.linspace(np.min(v), np.max(v) + EPSILON, 20),
        )
        colorbar_v = fig.colorbar(contour_v, ax=ax_v)
        colorbar_v.ax.yaxis.set_tick_params(color="white")
        colorbar_v.outline.set_edgecolor("white")
        plt.setp(plt.getp(colorbar_v.ax.axes, "yticklabels"), color="white")

        # Update the iteration text
        iteration_text.set_text(f"Iteration: {frame + 1}/{N_ITERATIONS}")

    ani = FuncAnimation(fig, update, frames=range(N_ITERATIONS), repeat=False)
    plt.show()


if __name__ == "__main__":
    main()
