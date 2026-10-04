"""Animate the helical path of a charged particle in a uniform magnetic field.

The Lorentz-force equations of motion dr/dt = v, dv/dt = (q/m) v x B are
integrated with the classical fourth-order Runge-Kutta method (RK4). A 3D view
shows the trajectory traced so far and the particle's current position.
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.ticker import MaxNLocator

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

Q = 1.0  # particle charge, C
M = 1.0  # particle mass, kg
B = np.array([0.0, 0.0, 1.0])  # magnetic field, T
R0 = np.array([0.0, 1.0, 0.0])  # initial position, m
V0 = np.array([1.0, 0.0, 1.0])  # initial velocity, m/s
DT = 0.01  # RK4 time step, s
STEPS_PER_FRAME = 25  # RK4 steps per animation frame
N_FRAMES = 200  # default frames; 200 * 25 * 0.01 s = 50 s
XY_LIMIT = 2.0  # half-width of the x and y axes, m (grows if the orbit is wider)
Z_LIMITS = (-2.0, 55.0)  # initial z range, m; fits the default run (z = 50 m)
COLOR = "dodgerblue"  # trail and particle; brighter than pure blue on black


def lorentz_force(t, y):
    """Return d/dt of the state y = (x, y, z, vx, vy, vz)."""
    v = y[3:]
    a = (Q / M) * np.cross(v, B)
    return np.hstack((v, a))


def rk4_step(func, t, y, dt):
    """Advance y by one classical fourth-order Runge-Kutta step."""
    k1 = func(t, y)
    k2 = func(t + dt / 2, y + dt / 2 * k1)
    k3 = func(t + dt / 2, y + dt / 2 * k2)
    k4 = func(t + dt, y + dt * k3)
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(num_steps, dt=DT):
    """Integrate from t = 0 for num_steps RK4 steps; return t, r, v arrays."""
    t_vals = np.arange(num_steps + 1) * dt
    r_vals = np.zeros((num_steps + 1, 3))
    v_vals = np.zeros((num_steps + 1, 3))
    y = np.hstack((R0, V0))
    r_vals[0], v_vals[0] = R0, V0
    for i in range(1, num_steps + 1):
        y = rk4_step(lorentz_force, t_vals[i - 1], y, dt)
        r_vals[i] = y[:3]
        v_vals[i] = y[3:]
    return t_vals, r_vals, v_vals


def report(t_vals, r_vals, v_vals):
    """Print the speed drift and the numerical vs analytical Larmor radius."""
    speed = np.linalg.norm(v_vals, axis=1)
    v_perp0 = np.linalg.norm(np.cross(V0, B / np.linalg.norm(B)))
    omega_c = abs(Q) * np.linalg.norm(B) / M
    r_larmor = v_perp0 / omega_c
    radius = np.linalg.norm(r_vals[:, :2], axis=1)  # guiding centre at origin
    print(
        f"t_final = {t_vals[-1]:.2f} s, cyclotron period = {2 * np.pi / omega_c:.3f} s"
    )
    print(
        f"Larmor radius: analytical {r_larmor:.6f} m, numerical {radius.mean():.6f} m"
    )
    print(f"max relative speed drift: {np.max(np.abs(speed / speed[0] - 1)):.2e}")


class ChargedParticleSimulation(Simulation):
    """RK4 state with every position and velocity recorded.

    ``positions[k]`` and ``velocities[k]`` belong to ``times()[k] = k dt``,
    so the recorded arrays match those returned by ``integrate``.
    """

    def __init__(self, r0=R0, v0=V0, dt=DT):
        super().__init__()
        self.dt = dt
        self.state = np.hstack((r0, v0)).astype(float)
        self.positions = [self.state[:3]]
        self.velocities = [self.state[3:]]

    def step(self):
        self.state = rk4_step(lorentz_force, self.time, self.state, self.dt)
        self.positions.append(self.state[:3])
        self.velocities.append(self.state[3:])

    def times(self):
        return np.arange(len(self.positions)) * self.dt

    def trajectory(self):
        """Return the recorded times, positions and velocities as arrays."""
        return self.times(), np.array(self.positions), np.array(self.velocities)


class ChargedParticleView(View):
    """Trail of the particle and its current position in 3D.

    The axes start at fixed limits that fit the default run and widen
    smoothly once the particle leaves them, so longer runs stay in view.
    """

    figsize = (6.5, 6.0)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        self.ax = ax = figure.add_subplot(projection="3d")
        (self.trail,) = ax.plot([], [], [], "-", color=COLOR)
        (self.particle,) = ax.plot(
            [], [], [], "o", color=COLOR, markersize=12 if portrait else 8
        )
        ax.set(xlabel="x (m)", ylabel="y (m)", zlabel="z (m)")
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(MaxNLocator(5, steps=[1, 2, 5, 10], prune="both"))
        if portrait:  # a taller box fills the reel panel and shows the pitch
            ax.set_box_aspect((1, 1, 1.4), zoom=0.95)
            for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
                axis.labelpad = 14

    def draw(self):
        r = np.array(self.simulation.positions)
        self.trail.set_data_3d(r[:, 0], r[:, 1], r[:, 2])
        self.particle.set_data_3d(r[-1:, 0], r[-1:, 1], r[-1:, 2])
        xy = max(XY_LIMIT, 1.1 * np.abs(r[:, :2]).max())
        self.ax.set_xlim(-xy, xy)
        self.ax.set_ylim(-xy, xy)
        z_low, z_high = Z_LIMITS
        self.ax.set_zlim(
            min(z_low, 1.1 * r[:, 2].min()), max(z_high, 1.1 * r[:, 2].max())
        )

    def status(self):
        return f"t = {self.simulation.time:.2f} s"


ANIMATION = Animation(
    title="Charged Particle Helix",
    subtitle="Lorentz force in a uniform B, RK4 integration",
    filename="charged_particle_helix.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"RK4 steps of dt = {DT:g} s",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, ChargedParticleSimulation(), ChargedParticleView)
    report(*simulation.trajectory())


if __name__ == "__main__":
    main()
