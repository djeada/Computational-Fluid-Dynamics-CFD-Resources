"""Steady versus unsteady pathlines around a cylinder with circulation.

The steady flow is the potential flow past a circular cylinder (uniform stream,
doublet and point vortex). The unsteady flow adds a kinematic vortex-street
model: point vortices of alternating sign are released behind the cylinder at
the Strouhal frequency and convected downstream, with image vortices keeping
the cylinder impermeable. Particle pathlines are integrated with RK4 and drawn,
in two stacked panels, over the instantaneous streamlines (contours of the
stream function): they coincide in the steady case and differ in the unsteady
one.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Flow parameters (dimensionless: lengths in R, velocities in U, times in R / U)
R = 1.0  # cylinder radius
U = 1.0  # free-stream velocity
GAMMA = 4 * np.pi * R * U  # cylinder circulation (counter-clockwise positive)
STROUHAL = 0.2  # St = f D / U
SHEDDING_PERIOD = 2 * R / (STROUHAL * U)  # one full cycle (two vortices)
VORTEX_STRENGTH = GAMMA / 2  # magnitude of each shed vortex
SHED_POSITION = (1.5 * R, 0.6 * R)  # release point (x, |y|) behind the cylinder
CONVECTION_SPEED = 0.8 * U  # downstream speed of the shed vortices
VORTEX_CORE = 0.3 * R  # core radius regularising the shed vortices
GROWTH_TIME = SHEDDING_PERIOD / 2  # shed vortices ramp up to full strength

# Numerical parameters
TIME_STEP = 0.01  # RK4 step for the particles
STEPS_PER_FRAME = 5  # RK4 steps per animation frame (0.05 time units)
N_FRAMES = 300  # default number of frames -> t = 15
NUM_PARTICLES = 20
SEED_X = -4.0  # particles start on a vertical line upstream of the cylinder
SEED_Y_RANGE = (-3.0, 3.0)
X_RANGE, Y_RANGE = (-5.0, 10.0), (-4.0, 5.0)  # plotted region; pathlines reach y = 4.9
GRID_POINTS = (300, 200)  # (nx, ny) samples of the stream function
PSI_RANGE = (-12.0, 8.0)  # stream-function values covered by the drawn streamlines


def base_velocity(x, y):
    """Potential flow past a cylinder with circulation; NaN inside the cylinder.

    Complex velocity u - i v = U (1 - R^2 / z^2) - i GAMMA / (2 pi z).
    """
    z = np.asarray(x) + 1j * np.asarray(y)
    with np.errstate(divide="ignore", invalid="ignore"):
        w = U * (1 - R**2 / z**2) - 1j * GAMMA / (2 * np.pi * z)
    inside = np.abs(z) < R
    return np.where(inside, np.nan, w.real), np.where(inside, np.nan, -w.imag)


def shed_vortices(t):
    """Positions and strengths of the vortices released up to time t."""
    half_period = SHEDDING_PERIOD / 2
    vortices = []
    for k in range(int(np.floor(t / half_period)) + 1):
        age = t - k * half_period
        x_v = SHED_POSITION[0] + CONVECTION_SPEED * age
        if x_v > X_RANGE[1] + 5:
            continue  # far downstream: negligible influence
        upper = k % 2 == 0
        y_v = SHED_POSITION[1] if upper else -SHED_POSITION[1]
        sign = (
            -1.0 if upper else 1.0
        )  # upper row clockwise, lower row counter-clockwise
        strength = sign * VORTEX_STRENGTH * min(1.0, age / GROWTH_TIME)
        vortices.append((complex(x_v, y_v), strength))
    return vortices


def vortex_velocity(x, y, vortices):
    """Velocity induced by shed vortices plus their images in the cylinder.

    For a vortex of strength g at z_v the circle theorem adds -g at R^2 / conj(z_v)
    and +g at the centre. Only the shed vortex itself has a regularised core.
    """
    z = np.asarray(x) + 1j * np.asarray(y)
    w = np.zeros_like(z)
    for z_v, g in vortices:
        for z_k, g_k, core in (
            (z_v, g, VORTEX_CORE),
            (R**2 / np.conj(z_v), -g, 0.0),
            (0.0, g, 0.0),
        ):
            dz = z - z_k
            with np.errstate(divide="ignore", invalid="ignore"):
                w += -1j * g_k / (2 * np.pi) * np.conj(dz) / (np.abs(dz) ** 2 + core**2)
    return w.real, -w.imag


def steady_velocity(x, y, t=0.0):
    return base_velocity(x, y)


def unsteady_velocity(x, y, t):
    u0, v0 = base_velocity(x, y)
    u1, v1 = vortex_velocity(x, y, shed_vortices(t))
    return u0 + u1, v0 + v1


def base_stream_function(x, y):
    """Stream function of the steady flow (u = dpsi/dy, v = -dpsi/dx).

    psi = Im F with F = U (z + R^2 / z) - i GAMMA ln(z) / (2 pi); NaN inside the
    cylinder. Its contours are the streamlines.
    """
    r2 = np.asarray(x) ** 2 + np.asarray(y) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        psi = U * np.asarray(y) * (1 - R**2 / r2) - GAMMA / (4 * np.pi) * np.log(r2)
    return np.where(r2 < R**2, np.nan, psi)


def vortex_stream_function(x, y, vortices):
    """Stream function of the shed vortices and their images.

    A vortex of strength g with core radius delta contributes
    -g ln(|z - z_k|^2 + delta^2) / (4 pi), which gives vortex_velocity.
    """
    z = np.asarray(x) + 1j * np.asarray(y)
    psi = np.zeros(z.shape)
    for z_v, g in vortices:
        for z_k, g_k, core in (
            (z_v, g, VORTEX_CORE),
            (R**2 / np.conj(z_v), -g, 0.0),
            (0.0, g, 0.0),
        ):
            with np.errstate(divide="ignore"):
                psi -= g_k / (4 * np.pi) * np.log(np.abs(z - z_k) ** 2 + core**2)
    return psi


def steady_stream_function(x, y, t=0.0):
    return base_stream_function(x, y)


def unsteady_stream_function(x, y, t):
    return base_stream_function(x, y) + vortex_stream_function(x, y, shed_vortices(t))


def rk4_step(velocity, pos, t, dt):
    """Classical RK4 for all particles at once; pos has shape (n, 2)."""

    def f(p, time):
        return np.stack(velocity(p[:, 0], p[:, 1], time), axis=1)

    k1 = f(pos, t)
    k2 = f(pos + 0.5 * dt * k1, t + 0.5 * dt)
    k3 = f(pos + 0.5 * dt * k2, t + 0.5 * dt)
    k4 = f(pos + dt * k3, t + dt)
    return pos + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def pathline_step(velocity, pos, t, dt):
    """One RK4 step; particles that end inside the cylinder become NaN."""
    new = rk4_step(velocity, pos, t, dt)
    new[np.hypot(new[:, 0], new[:, 1]) < R] = np.nan
    return new


def compute_pathlines(velocity, particles, dt, nt):
    """Return positions with shape (nt + 1, n, 2); particles hitting the cylinder become NaN."""
    paths = np.empty((nt + 1, *particles.shape))
    paths[0] = particles
    for step in range(nt):
        paths[step + 1] = pathline_step(velocity, paths[step], step * dt, dt)
    return paths


def seed_particles(num_particles=NUM_PARTICLES):
    """Particles on the vertical line x = SEED_X, shape (num_particles, 2)."""
    return np.column_stack(
        [np.full(num_particles, SEED_X), np.linspace(*SEED_Y_RANGE, num_particles)]
    )


def streamline_levels(seeds):
    """Stream-function values of the streamlines through the seed points.

    The steady pathlines then lie exactly on drawn streamlines. The levels are
    continued with the mean spacing to cover PSI_RANGE.
    """
    psi = np.sort(base_stream_function(seeds[:, 0], seeds[:, 1]))
    spacing = np.diff(psi).mean() if psi.size > 1 else 0.3  # 0.3 R for one seed
    below = np.arange(psi[0] - spacing, PSI_RANGE[0], -spacing)[::-1]
    above = np.arange(psi[-1] + spacing, PSI_RANGE[1], spacing)
    return np.concatenate([below, psi, above])


FLOWS = {
    "steady": (steady_velocity, steady_stream_function),
    "unsteady": (unsteady_velocity, unsteady_stream_function),
}


class PathlineSimulation(Simulation):
    """The same particles released into the steady and the unsteady flow.

    One step is one RK4 step of every particle in both flows; the positions
    after every step are kept, so ``paths(flow)`` is the pathline history.
    """

    dt = TIME_STEP

    def __init__(self, num_particles=NUM_PARTICLES):
        super().__init__()
        self.history = {flow: [seed_particles(num_particles)] for flow in FLOWS}

    def step(self):
        for flow, (velocity, _) in FLOWS.items():
            positions = self.history[flow]
            positions.append(pathline_step(velocity, positions[-1], self.time, self.dt))

    def paths(self, flow):
        """Positions with shape (steps + 1, num_particles, 2)."""
        return np.array(self.history[flow])


def polyline(paths):
    """Join the pathlines of all particles into one NaN-separated line."""
    gap = np.full((paths.shape[1], 1, 2), np.nan)
    joined = np.concatenate([paths.transpose(1, 0, 2), gap], axis=1)
    return joined.reshape(-1, 2).T


STREAMLINE_COLOR = "#4cc9f0"
PATHLINE_STYLE = {"color": "#ff9f1c", "linewidth": 2, "zorder": 3}
PARTICLE_STYLE = {
    "color": "#ffe066",
    "marker": "o",
    "markersize": 7,
    "ls": "",
    "zorder": 6,
}
VORTEX_STYLE = {
    "color": "#f72585",
    "marker": "o",
    "markersize": 14,
    "markerfacecolor": "none",
    "markeredgewidth": 2,
    "ls": "",
    "zorder": 6,
}


class PathlineView(View):
    """Streamlines, pathlines and particles of the steady and unsteady flow.

    Streamlines are contours of the stream function at the current time, which
    is far cheaper than a streamplot each frame and moves smoothly. The
    steady streamlines are drawn once; the unsteady ones are redrawn with the
    shed vortices. Panels sit side by side in the window and stacked in a reel.
    """

    figsize = (12.0, 4.8)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        if portrait:
            axes = figure.subplots(2, 1, sharex=True)
        else:
            axes = figure.subplots(1, 2, sharey=True)
        x = np.linspace(*X_RANGE, GRID_POINTS[0])
        y = np.linspace(*Y_RANGE, GRID_POINTS[1])
        self.grid = np.meshgrid(x, y)
        self.levels = streamline_levels(simulation.history["steady"][0])
        titles = {
            "steady": "Steady: pathlines follow streamlines",
            "unsteady": "Unsteady: pathlines cross streamlines",
        }
        self.axes, self.pathlines, self.particles = {}, {}, {}
        for ax, flow in zip(axes, FLOWS):
            self.axes[flow] = ax
            ax.set(xlim=X_RANGE, ylim=Y_RANGE, aspect="equal", title=titles[flow])
            ax.add_patch(Circle((0, 0), R, color="0.7", zorder=5))
            (self.pathlines[flow],) = ax.plot([], [], **PATHLINE_STYLE)
            (self.particles[flow],) = ax.plot([], [], **PARTICLE_STYLE)
        # Shared axes are labelled once: x below the stack, y left of the row.
        for ax in axes[1:] if portrait else axes:
            ax.set_xlabel("x / R")
        for ax in axes if portrait else axes[:1]:
            ax.set_ylabel("y / R")
        self.contour("steady")  # drawn once: the steady streamlines never change
        self.unsteady_streamlines = None
        (self.vortices,) = self.axes["unsteady"].plot([], [], **VORTEX_STYLE)
        handles = [
            Line2D([], [], color=STREAMLINE_COLOR, label="streamlines"),
            Line2D([], [], label="pathlines", **PATHLINE_STYLE),
            Line2D([], [], label="particles", **PARTICLE_STYLE),
            Line2D([], [], label="shed vortices", **VORTEX_STYLE),
        ]
        figure.legend(handles=handles, loc="outside lower center", ncols=4)

    def contour(self, flow):
        _, stream_function = FLOWS[flow]
        psi = stream_function(*self.grid, self.simulation.time)
        return self.axes[flow].contour(
            *self.grid, psi, levels=self.levels, colors=STREAMLINE_COLOR,
            linewidths=1.0, linestyles="solid", alpha=0.7, zorder=2,
        )  # fmt: skip

    def draw(self):
        if self.unsteady_streamlines is not None:
            self.unsteady_streamlines.remove()
        self.unsteady_streamlines = self.contour("unsteady")
        for flow in FLOWS:
            paths = self.simulation.paths(flow)
            self.pathlines[flow].set_data(*polyline(paths))
            self.particles[flow].set_data(paths[-1, :, 0], paths[-1, :, 1])
        vortices = np.array([z for z, _ in shed_vortices(self.simulation.time)])
        self.vortices.set_data(vortices.real, vortices.imag)

    def status(self):
        return f"t = {self.simulation.time:.2f} R/U"


ANIMATION = Animation(
    title="Steady and Unsteady Pathlines",
    subtitle="Streamlines vs pathlines past a cylinder",
    filename="steady_and_unsteady_pathlines.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"RK4 steps of {TIME_STEP:g} R/U",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, PathlineSimulation(), PathlineView)
    lost = {
        flow: int(np.isnan(simulation.paths(flow)[-1, :, 0]).sum()) for flow in FLOWS
    }
    print(
        f"t = {simulation.time:.2f} after {simulation.steps} RK4 steps; "
        f"particles lost in the cylinder: {lost['steady']} steady, "
        f"{lost['unsteady']} unsteady"
    )


if __name__ == "__main__":
    main()
