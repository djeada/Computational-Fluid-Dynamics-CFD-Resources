"""Sod's shock tube solved with first- and second-order Godunov-type schemes.

The 1D Euler equations for an ideal gas are advanced on 200 finite-volume
cells with HLLC fluxes: once with the first-order Godunov scheme and once with
the second-order MUSCL-Hancock scheme (van Leer limiter). Density, velocity,
pressure and specific internal energy of both runs are animated against the
exact Riemann solution, computed with Toro's pressure function and a Newton
iteration for the star pressure.
"""

import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

GAMMA = 1.4  # ratio of specific heats [-]
LEFT = (1.0, 0.0, 1.0)  # (rho, u, p) for x < X0, Sod (1978)
RIGHT = (0.125, 0.0, 0.1)  # (rho, u, p) for x > X0
X0 = 0.5  # position of the diaphragm on the tube [0, 1]
N_CELLS = 200  # finite-volume cells
END_TIME = 0.2  # time of the standard comparison
N_FRAMES = 200  # default frames
STEPS_PER_FRAME = 1  # time steps per frame
TIME_STEP = END_TIME / (N_FRAMES * STEPS_PER_FRAME)  # dt = 1e-3
MAX_CFL = 0.9  # a step whose CFL number would exceed this is split
N_EXACT = 1000  # points at which the exact solution is drawn
SCHEMES = ("godunov", "muscl")


# ---------------------------------------------------------------- gas state
def conservative(rho, u, p, gamma=GAMMA):
    """Conservative variables (rho, rho u, E) from primitive ones."""
    rho, u, p = np.broadcast_arrays(*map(np.asarray, (rho, u, p)))
    return np.array([rho, rho * u, p / (gamma - 1.0) + 0.5 * rho * u**2])


def primitive(U, gamma=GAMMA):
    """Density, velocity and pressure from conservative variables."""
    rho = U[0]
    u = U[1] / rho
    return rho, u, (gamma - 1.0) * (U[2] - 0.5 * rho * u**2)


def physical_flux(U, gamma=GAMMA):
    """Euler flux F(U) = (rho u, rho u^2 + p, (E + p) u)."""
    rho, u, p = primitive(U, gamma)
    return np.array([rho * u, rho * u**2 + p, (U[2] + p) * u])


def sound_speed(rho, p, gamma=GAMMA):
    return np.sqrt(gamma * p / rho)


# ------------------------------------------------------ exact Riemann solver
def pressure_function(p, rho_k, p_k, c_k, gamma=GAMMA):
    """Toro's f_K(p) and f_K'(p): velocity change across the left or right wave."""
    if p > p_k:  # shock
        a_k = 2.0 / ((gamma + 1.0) * rho_k)
        b_k = (gamma - 1.0) / (gamma + 1.0) * p_k
        root = np.sqrt(a_k / (p + b_k))
        return (p - p_k) * root, root * (1.0 - 0.5 * (p - p_k) / (p + b_k))
    ratio = p / p_k  # rarefaction
    value = 2.0 * c_k / (gamma - 1.0) * (ratio ** ((gamma - 1.0) / (2 * gamma)) - 1)
    return value, ratio ** (-(gamma + 1.0) / (2.0 * gamma)) / (rho_k * c_k)


def star_state(left, right, gamma=GAMMA, tol=1e-14, max_iter=100):
    """Solve f_L(p) + f_R(p) + u_R - u_L = 0 by Newton; return (p*, u*)."""
    (rl, ul, pl), (rr, ur, pr) = left, right
    cl, cr = sound_speed(rl, pl, gamma), sound_speed(rr, pr, gamma)
    if 2.0 * (cl + cr) / (gamma - 1.0) <= ur - ul:
        raise ValueError("the initial data generate a vacuum")
    p = max(0.5 * (pl + pr) - 0.125 * (ur - ul) * (rl + rr) * (cl + cr), 1e-8)
    for _ in range(max_iter):
        fl, dl = pressure_function(p, rl, pl, cl, gamma)
        fr, dr = pressure_function(p, rr, pr, cr, gamma)
        p_new = max(p - (fl + fr + ur - ul) / (dl + dr), 1e-3 * p)
        converged = 2.0 * abs(p_new - p) / (p_new + p) < tol
        p = p_new
        if converged:
            break
    fl = pressure_function(p, rl, pl, cl, gamma)[0]
    fr = pressure_function(p, rr, pr, cr, gamma)[0]
    return p, 0.5 * (ul + ur) + 0.5 * (fr - fl)


def exact_solution(x, t, left=LEFT, right=RIGHT, x0=X0, gamma=GAMMA):
    """Exact (rho, u, p) of the Riemann problem at positions x and time t > 0."""
    p_star, u_star = star_state(left, right, gamma)
    xi = (np.asarray(x, dtype=float) - x0) / t
    rho, u, p = (np.empty_like(xi) for _ in range(3))
    g1 = (gamma - 1.0) / (gamma + 1.0)
    for state, sign, side in ((left, -1.0, xi <= u_star), (right, 1.0, xi > u_star)):
        rk, uk, pk = state
        ck = sound_speed(rk, pk, gamma)
        s = xi[side]
        r_out, u_out, p_out = (
            np.full_like(s, rk),
            np.full_like(s, uk),
            np.full_like(s, pk),
        )
        if p_star > pk:  # shock: Rankine-Hugoniot density and shock speed
            speed = uk + sign * ck * np.sqrt(
                (gamma + 1) / (2 * gamma) * p_star / pk + (gamma - 1) / (2 * gamma)
            )
            behind = sign * (s - speed) <= 0
            rho_behind = rk * (p_star / pk + g1) / (g1 * p_star / pk + 1.0)
        else:  # rarefaction: isentropic star density and the centred fan
            c_star = ck * (p_star / pk) ** ((gamma - 1.0) / (2.0 * gamma))
            head, tail = uk + sign * ck, u_star + sign * c_star
            fan = (sign * (s - head) <= 0) & (sign * (s - tail) > 0)
            c_fan = (
                2.0 / (gamma + 1.0) * (ck - sign * 0.5 * (gamma - 1.0) * (uk - s[fan]))
            )
            r_out[fan] = rk * (c_fan / ck) ** (2.0 / (gamma - 1.0))
            u_out[fan] = (
                2.0 / (gamma + 1.0) * (-sign * ck + 0.5 * (gamma - 1.0) * uk + s[fan])
            )
            p_out[fan] = pk * (c_fan / ck) ** (2.0 * gamma / (gamma - 1.0))
            behind = sign * (s - tail) <= 0
            rho_behind = rk * (p_star / pk) ** (1.0 / gamma)
        r_out[behind], u_out[behind], p_out[behind] = rho_behind, u_star, p_star
        rho[side], u[side], p[side] = r_out, u_out, p_out
    return rho, u, p


# ----------------------------------------------------------------- schemes
def hllc_flux(UL, UR, gamma=GAMMA):
    """HLLC flux of Toro, Spruce and Speares (1994) with Davis wave speeds."""
    rl, ul, pl = primitive(UL, gamma)
    rr, ur, pr = primitive(UR, gamma)
    cl, cr = sound_speed(rl, pl, gamma), sound_speed(rr, pr, gamma)
    s_left = np.minimum(ul - cl, ur - cr)
    s_right = np.maximum(ul + cl, ur + cr)
    s_star = (pr - pl + rl * ul * (s_left - ul) - rr * ur * (s_right - ur)) / (
        rl * (s_left - ul) - rr * (s_right - ur)
    )

    def star_flux(U, F, rho, u, p, s):
        factor = rho * (s - u) / (s - s_star)
        energy = U[2] / rho + (s_star - u) * (s_star + p / (rho * (s - u)))
        return F + s * (factor * np.array([np.ones_like(rho), s_star, energy]) - U)

    FL, FR = physical_flux(UL, gamma), physical_flux(UR, gamma)
    return np.where(
        s_left >= 0,
        FL,
        np.where(
            s_star >= 0,
            star_flux(UL, FL, rl, ul, pl, s_left),
            np.where(s_right > 0, star_flux(UR, FR, rr, ur, pr, s_right), FR),
        ),
    )


def van_leer_slope(backward, forward):
    """Van Leer's harmonic-mean limiter: zero at extrema, TVD."""
    product = backward * forward
    total = backward + forward
    safe = np.where(product > 0, total, 1.0)
    return np.where(product > 0, 2.0 * product / safe, 0.0)


def pad(U, ghosts):
    """Zero-gradient (transmissive) ghost cells at both ends of the tube."""
    return np.concatenate(
        [np.repeat(U[:, :1], ghosts, axis=1), U, np.repeat(U[:, -1:], ghosts, axis=1)],
        axis=1,
    )


def godunov_fluxes(U, dt, dx, gamma=GAMMA):
    """First-order face fluxes: the HLLC flux of the two adjacent cell averages."""
    W = pad(U, 1)
    return hllc_flux(W[:, :-1], W[:, 1:], gamma)


def muscl_hancock_fluxes(U, dt, dx, gamma=GAMMA):
    """MUSCL-Hancock face fluxes (Toro 2009, section 14.4).

    Limited linear reconstruction of the conservative variables, a half-step
    evolution of both boundary-extrapolated values with the physical flux,
    and the HLLC flux of the evolved values on either side of each face.
    """
    W = pad(U, 2)
    slope = van_leer_slope(W[:, 1:-1] - W[:, :-2], W[:, 2:] - W[:, 1:-1])
    centre = W[:, 1:-1]
    low, high = centre - 0.5 * slope, centre + 0.5 * slope
    change = 0.5 * dt / dx * (physical_flux(low, gamma) - physical_flux(high, gamma))
    low, high = low + change, high + change
    return hllc_flux(high[:, :-1], low[:, 1:], gamma)


FLUX_FUNCTIONS = {"godunov": godunov_fluxes, "muscl": muscl_hancock_fluxes}


def update(U, scheme, dt, dx, gamma=GAMMA):
    """Conservative update U_i - dt/dx (F_{i+1/2} - F_{i-1/2})."""
    F = FLUX_FUNCTIONS[scheme](U, dt, dx, gamma)
    return U - dt / dx * (F[:, 1:] - F[:, :-1])


def max_wave_speed(U, gamma=GAMMA):
    rho, u, p = primitive(U, gamma)
    return float(np.max(np.abs(u) + sound_speed(rho, p, gamma)))


class SodSimulation(Simulation):
    """Both schemes on the same grid; one step advances each by ``dt``.

    The time step is fixed so that frames are evenly spaced in time. Should
    its CFL number exceed ``max_cfl`` (on a finer grid, say), it is split into
    as many equal sub-steps as needed. ``states`` holds the conservative
    variables of each scheme, ``cfl`` the largest CFL number of the last step.
    """

    def __init__(self, n_cells=N_CELLS, dt=TIME_STEP, max_cfl=MAX_CFL):
        super().__init__()
        if n_cells < 4:
            raise ValueError("at least four cells are required")
        self.n_cells, self.dt, self.max_cfl = n_cells, dt, max_cfl
        self.dx = 1.0 / n_cells
        self.x = (np.arange(n_cells) + 0.5) * self.dx
        left = self.x < X0
        initial = conservative(*(np.where(left, a, b) for a, b in zip(LEFT, RIGHT)))
        self.states = {scheme: initial.copy() for scheme in SCHEMES}
        self.cfl = dt * max_wave_speed(initial) / self.dx

    def step(self):
        largest = 0.0
        for scheme, U in self.states.items():
            rate = max_wave_speed(U) / self.dx
            parts = max(1, int(np.ceil(self.dt * rate / self.max_cfl)))
            dt = self.dt / parts
            for _ in range(parts):
                U = update(U, scheme, dt, self.dx)
            self.states[scheme] = U
            largest = max(largest, dt * rate)
        self.cfl = largest

    def fields(self, scheme):
        """Density, velocity, pressure and specific internal energy of a scheme."""
        rho, u, p = primitive(self.states[scheme])
        return rho, u, p, p / ((GAMMA - 1.0) * rho)

    def exact(self, x):
        """The same four quantities from the exact solution at the current time."""
        if self.time <= 0.0:
            rho, u, p = (np.where(x < X0, a, b) for a, b in zip(LEFT, RIGHT))
        else:
            rho, u, p = exact_solution(x, self.time)
        return rho, u, p, p / ((GAMMA - 1.0) * rho)

    def l1_errors(self):
        """Mean |rho - rho_exact| over the cells for each scheme."""
        reference = self.exact(self.x)[0]
        return {
            s: float(np.mean(np.abs(self.fields(s)[0] - reference))) for s in SCHEMES
        }


class SodView(View):
    """Four panels (density, velocity, pressure, internal energy) in a 2 x 2 grid.

    The exact solution is a solid line, the first-order Godunov scheme a
    dashed line and MUSCL-Hancock dots, so the smearing of the contact and
    the shock is visible. The reel uses the same grid with larger text.
    """

    figsize = (12.0, 7.5)
    LIMITS = ((0.0, 1.1), (-0.1, 1.05), (0.0, 1.1), (1.6, 3.0))
    NAMES = (
        r"Density $\rho$",
        r"Velocity $u$",
        r"Pressure $p$",
        r"Internal energy $e$",
    )

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        axes = figure.subplots(2, 2, sharex=True).ravel()
        self.x_exact = np.linspace(0.0, 1.0, N_EXACT)
        exact = simulation.exact(self.x_exact)
        size = 5 if portrait else 2.5
        self.lines = []
        for k, ax in enumerate(axes):
            (exact_line,) = ax.plot(
                self.x_exact, exact[k], lw=1.5, label="exact", zorder=3
            )
            (first,) = ax.plot(
                simulation.x, simulation.fields("godunov")[k], "--", lw=1.6,
                label="Godunov (1st order)",
            )  # fmt: skip
            (second,) = ax.plot(
                simulation.x, simulation.fields("muscl")[k], "o", ms=size,
                label="MUSCL-Hancock (2nd)",
            )  # fmt: skip
            self.lines.append((exact_line, first, second))
            ax.set(xlim=(0.0, 1.0), ylim=self.LIMITS[k], title=self.NAMES[k])
            ax.grid(color="0.3")
        for ax in axes[2:]:
            ax.set_xlabel("x")
        if portrait:  # below the pressure plateau, left of the contact: always empty
            axes[2].legend(
                list(self.lines[2]), ["exact", "1st order", "2nd order"],
                loc="lower left", fontsize="small",
            )  # fmt: skip
        else:  # under the velocity plateau: empty except for the shock
            axes[1].legend(loc="center", bbox_to_anchor=(0.64, 0.42))

    def draw(self):
        simulation = self.simulation
        exact = simulation.exact(self.x_exact)
        first, second = simulation.fields("godunov"), simulation.fields("muscl")
        for k, (exact_line, first_line, second_line) in enumerate(self.lines):
            exact_line.set_ydata(exact[k])
            first_line.set_ydata(first[k])
            second_line.set_ydata(second[k])

    def status(self):
        simulation = self.simulation
        errors = simulation.l1_errors()
        return (
            f"t = {simulation.time:.3f}   step {simulation.steps}   "
            f"L1 {errors['godunov']:.4f}, {errors['muscl']:.4f}"
        )


ANIMATION = Animation(
    title="Sod Shock Tube",
    subtitle="Godunov and MUSCL-Hancock with HLLC against the exact Riemann solution",
    filename="sod_shock_tube.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, SodSimulation(), SodView)
    p_star, u_star = star_state(LEFT, RIGHT)
    errors = simulation.l1_errors()
    print(
        f"t = {simulation.time:.3f} after {simulation.steps} steps "
        f"(CFL {simulation.cfl:.2f}): exact p* = {p_star:.5f}, u* = {u_star:.5f}; "
        f"L1 density error Godunov {errors['godunov']:.4f}, "
        f"MUSCL-Hancock {errors['muscl']:.4f}"
    )


if __name__ == "__main__":
    main()
