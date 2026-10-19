"""Mach 3 wind tunnel with a forward-facing step (Woodward & Colella, 1984).

The 2D compressible Euler equations are solved with a finite-volume scheme:
MUSCL reconstruction of the primitive variables with the monotonised-central
limiter, HLLC fluxes and second-order strong-stability-preserving Runge-Kutta
time stepping under a CFL condition. A uniform Mach 3 stream enters a 3 x 1
tunnel and meets a step of height 0.2. The bow shock, its reflections off the
walls, the Mach stem and the slip line behind it are shown as a numerical
schlieren image above the Mach number and the pressure.
"""

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from matplotlib import colormaps
from numba import njit, prange

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _animation import Animation, Simulation, View  # noqa: E402

# Problem (nondimensional, as in Woodward & Colella 1984)
GAMMA = 1.4  # ratio of specific heats
TUNNEL_LENGTH = 3.0  # x extent of the tunnel
TUNNEL_HEIGHT = 1.0  # y extent of the tunnel
STEP_X = 0.6  # the step face is at x = 0.6 ...
STEP_HEIGHT = 0.2  # ... and the step reaches up to y = 0.2
INFLOW = (1.4, 3.0, 0.0, 1.0)  # rho, u, v, p: sound speed 1, so Mach 3
END_TIME = 4.0  # time of the last frame

# Numerical parameters
CELLS_PER_UNIT = 160  # dx = dy = 1/160: 480 x 160 cells
CFL = 0.45  # bound on dt * max((|u| + c)/dx + (|v| + c)/dy)
STEPS_PER_FRAME = 25  # time steps per animation frame
N_FRAMES = 400  # default frames: 10 000 steps reach t = END_TIME
TIME_STEP = END_TIME / (N_FRAMES * STEPS_PER_FRAME)  # dt = 4e-4, CFL about 0.4
DENSITY_FLOOR = 1e-6  # positivity safeguards (see apply_floors), in units of
PRESSURE_FLOOR = 1e-6  # the inflow density and pressure

# Display
SCHLIEREN_SCALE = 40.0  # |grad rho| at which the schlieren value is exp(-1)
MACH_LIMITS = (0.0, 3.5)
PRESSURE_LIMITS = (0.0, 14.0)  # the Mach 3 stagnation pressure is about 12
STEP_COLOR = "0.45"

# Boundary codes of Domain.x_boundary and Domain.y_boundary
BOUNDARIES = ("tunnel", "outflow", "wall", "periodic")


def primitive(state):
    """Density, velocity components and pressure from (rho, rho u, rho v, E)."""
    rho = state[0]
    u = state[1] / rho
    v = state[2] / rho
    p = (GAMMA - 1.0) * (state[3] - 0.5 * rho * (u * u + v * v))
    return np.stack((rho, u, v, p))


def conservative(rho, u, v, p):
    """(rho, rho u, rho v, E) with E = p / (gamma - 1) + rho |u|^2 / 2."""
    rho, u, v, p = np.broadcast_arrays(
        *(np.asarray(q, dtype=float) for q in (rho, u, v, p))
    )
    energy = p / (GAMMA - 1.0) + 0.5 * rho * (u * u + v * v)
    return np.stack((rho, rho * u, rho * v, energy))


@dataclass(frozen=True)
class Domain:
    """Cell grid with an optional solid step in the lower right corner.

    Arrays are (component, row, column): rows are y, columns x. The cells
    with column >= ``step_i`` and row < ``step_j`` are solid. ``x_boundary``
    is "tunnel" (the primitive ``inflow`` state enters on the left, with a
    zero-gradient outflow on the right), "outflow" (zero gradient at both
    ends), "wall" or "periodic"; ``y_boundary`` is "wall" or "periodic".
    Walls reflect: their ghost cells mirror the fluid next to them.
    """

    nx: int
    ny: int
    dx: float
    dy: float
    step_i: int = 0
    step_j: int = 0
    x_boundary: str = "tunnel"
    y_boundary: str = "wall"
    inflow: tuple = INFLOW

    def __post_init__(self):
        if self.x_boundary not in BOUNDARIES:
            raise ValueError(f"unknown x boundary {self.x_boundary!r}")
        if self.y_boundary not in ("wall", "periodic"):
            raise ValueError(f"unknown y boundary {self.y_boundary!r}")
        if self.step_j > 0 and not (2 <= self.step_i and self.step_j <= self.ny - 2):
            raise ValueError("the step needs two fluid cells in front and above")

    @property
    def solid(self):
        mask = np.zeros((self.ny, self.nx), dtype=bool)
        mask[: self.step_j, self.step_i :] = True
        return mask


def make_tunnel(cells_per_unit=CELLS_PER_UNIT):
    """The Woodward-Colella tunnel with the step resolved by whole cells."""
    if cells_per_unit < 10:
        raise ValueError("need at least 10 cells per unit length")
    nx = round(TUNNEL_LENGTH * cells_per_unit)
    ny = round(TUNNEL_HEIGHT * cells_per_unit)
    step_i = round(STEP_X * cells_per_unit)
    step_j = round(STEP_HEIGHT * cells_per_unit)
    h = 1.0 / cells_per_unit
    return Domain(nx, ny, h, h, step_i, step_j)


@njit(cache=False, parallel=True)
def fill_primitives(state, wx, wy, gamma):
    """Write the primitives (rho, u, v, p) of every cell into the interiors of
    wx (two ghost columns each side) and wy (two ghost rows each side)."""
    ny, nx = state.shape[1], state.shape[2]
    for row in prange(ny):
        for col in range(nx):
            rho = state[0, row, col]
            u = state[1, row, col] / rho
            v = state[2, row, col] / rho
            p = (gamma - 1.0) * (state[3, row, col] - 0.5 * rho * (u * u + v * v))
            wx[0, row, col + 2] = wy[0, row + 2, col] = rho
            wx[1, row, col + 2] = wy[1, row + 2, col] = u
            wx[2, row, col + 2] = wy[2, row + 2, col] = v
            wx[3, row, col + 2] = wy[3, row + 2, col] = p


def mirror(target, source, normal):
    """Copy primitive cells into ghost cells, reversing the normal velocity."""
    target[:] = source
    target[normal] *= -1.0


def fill_ghosts_x(wx, domain):
    """Ghost columns of wx (4, ny, nx + 4) for the faces normal to x.

    The two solid columns behind the step face mirror the two fluid columns
    in front of it; interior column k is column k + 2 of wx.
    """
    kind = domain.x_boundary
    if kind == "periodic":
        wx[:, :, :2], wx[:, :, -2:] = wx[:, :, -4:-2], wx[:, :, 2:4]
    elif kind == "wall":
        mirror(wx[:, :, :2], wx[:, :, 3:1:-1], 1)
        mirror(wx[:, :, -2:], wx[:, :, -3:-5:-1], 1)
    else:
        wx[:, :, :2] = wx[:, :, 2:3]
        wx[:, :, -2:] = wx[:, :, -3:-2]
        if kind == "tunnel":
            wx[:, :, :2] = np.reshape(domain.inflow, (4, 1, 1))
    i, j = domain.step_i, domain.step_j
    if j > 0:
        mirror(wx[:, :j, i + 2 : i + 4], wx[:, :j, i + 1 : i - 1 : -1], 1)


def fill_ghosts_y(wy, domain):
    """Ghost rows of wy (4, ny + 4, nx) for the faces normal to y.

    The two solid rows under the top of the step mirror the two fluid rows
    above it; interior row k is row k + 2 of wy.
    """
    if domain.y_boundary == "periodic":
        wy[:, :2], wy[:, -2:] = wy[:, -4:-2], wy[:, 2:4]
    else:
        mirror(wy[:, :2], wy[:, 3:1:-1], 2)
        mirror(wy[:, -2:], wy[:, -3:-5:-1], 2)
    i, j = domain.step_i, domain.step_j
    if j > 0:
        mirror(wy[:, j : j + 2, i:], wy[:, j + 3 : j + 1 : -1, i:], 2)


def padded_primitives(state, domain):
    """Primitives with ghost cells: (wx, wy) for the x and y faces."""
    wx = np.empty((4, domain.ny, domain.nx + 4))
    wy = np.empty((4, domain.ny + 4, domain.nx))
    fill_primitives(state, wx, wy, GAMMA)
    fill_ghosts_x(wx, domain)
    fill_ghosts_y(wy, domain)
    return wx, wy


@njit(cache=False)
def limited_slope(backward, forward):
    """Monotonised-central limiter: zero at an extremum, otherwise the
    smallest of the central difference and twice each one-sided one."""
    if backward * forward <= 0.0:
        return 0.0
    central = 0.5 * (backward + forward)
    if central > 0.0:
        return min(central, 2.0 * backward, 2.0 * forward)
    return max(central, 2.0 * backward, 2.0 * forward)


@njit(cache=False)
def hllc_flux(rl, ul, vl, pl, rr, ur, vr, pr, gamma):
    """HLLC flux (Toro, Spruce & Speares 1994) through a face.

    u is the velocity normal to the face and v the tangential one. Returns
    the fluxes of mass, normal momentum, tangential momentum and energy. The
    outer wave speeds are the Davis estimates min(u - c) and max(u + c).
    """
    cl = math.sqrt(gamma * pl / rl)
    cr = math.sqrt(gamma * pr / rr)
    el = pl / (gamma - 1.0) + 0.5 * rl * (ul * ul + vl * vl)
    er = pr / (gamma - 1.0) + 0.5 * rr * (ur * ur + vr * vr)
    sl = min(ul - cl, ur - cr)
    sr = max(ul + cl, ur + cr)
    if sl >= 0.0:
        return rl * ul, rl * ul * ul + pl, rl * ul * vl, (el + pl) * ul
    if sr <= 0.0:
        return rr * ur, rr * ur * ur + pr, rr * ur * vr, (er + pr) * ur
    ml = rl * (sl - ul)
    mr = rr * (sr - ur)
    star = (pr - pl + ml * ul - mr * ur) / (ml - mr)  # contact speed S*
    if star >= 0.0:
        r, u, v, p, e, s, m = rl, ul, vl, pl, el, sl, ml
    else:
        r, u, v, p, e, s, m = rr, ur, vr, pr, er, sr, mr
    rho_star = m / (s - star)
    e_star = rho_star * (e / r + (star - u) * (star + p / m))
    return (
        r * u + s * (rho_star - r),
        r * u * u + p + s * (rho_star * star - r * u),
        r * u * v + s * (rho_star - r) * v,
        (e + p) * u + s * (e_star - e),
    )


@njit(cache=False)
def face_value(w, q, row, col, d_row, d_col, side):
    """Variable q of cell (row, col) reconstructed at one of its faces.

    The neighbours are (row -/+ d_row, col -/+ d_col); side is +1 for the
    face towards the next cell and -1 for the face towards the previous one.
    """
    centre = w[q, row, col]
    backward = centre - w[q, row - d_row, col - d_col]
    forward = w[q, row + d_row, col + d_col] - centre
    return centre + 0.5 * side * limited_slope(backward, forward)


@njit(cache=False)
def muscl_hllc(w, row, col, d_row, d_col, normal, gamma):
    """HLLC flux through the face between cell (row, col) and the next cell.

    ``w`` holds padded primitives (rho, u, v, p), the next cell is
    (row + d_row, col + d_col), and ``normal`` is the index (1 or 2) of the
    velocity normal to the face. Each face state is reconstructed linearly
    with limited slopes; a state with nonpositive density or pressure falls
    back to the cell average (first order) on that side of the face.
    """
    t = 3 - normal
    r2, c2 = row + d_row, col + d_col
    rl = face_value(w, 0, row, col, d_row, d_col, 1.0)
    ul = face_value(w, normal, row, col, d_row, d_col, 1.0)
    vl = face_value(w, t, row, col, d_row, d_col, 1.0)
    pl = face_value(w, 3, row, col, d_row, d_col, 1.0)
    rr = face_value(w, 0, r2, c2, d_row, d_col, -1.0)
    ur = face_value(w, normal, r2, c2, d_row, d_col, -1.0)
    vr = face_value(w, t, r2, c2, d_row, d_col, -1.0)
    pr = face_value(w, 3, r2, c2, d_row, d_col, -1.0)
    if rl <= 0.0 or pl <= 0.0:
        rl, ul, vl, pl = (
            w[0, row, col],
            w[normal, row, col],
            w[t, row, col],
            w[3, row, col],
        )
    if rr <= 0.0 or pr <= 0.0:
        rr, ur, vr, pr = w[0, r2, c2], w[normal, r2, c2], w[t, r2, c2], w[3, r2, c2]
    return hllc_flux(rl, ul, vl, pl, rr, ur, vr, pr, gamma)


@njit(cache=False, parallel=True)
def flux_divergence(wx, wy, dx, dy, gamma, rate):
    """rate = -div(F) from the padded primitives wx and wy.

    Every face flux is computed once and enters the two cells it separates
    with opposite signs, so the scheme is conservative. Face f of a row lies
    between interior cells f - 1 and f (padded cells f + 1 and f + 2).
    """
    ny, nx = rate.shape[1], rate.shape[2]
    flux_y = np.empty((4, ny + 1, nx))
    for f in prange(ny + 1):
        for col in range(nx):
            fm, fn, ft, fe = muscl_hllc(wy, f + 1, col, 1, 0, 2, gamma)
            flux_y[0, f, col] = fm
            flux_y[1, f, col] = ft
            flux_y[2, f, col] = fn
            flux_y[3, f, col] = fe
    for row in prange(ny):
        flux_x = np.empty((4, nx + 1))
        for f in range(nx + 1):
            fm, fn, ft, fe = muscl_hllc(wx, row, f + 1, 0, 1, 1, gamma)
            flux_x[0, f] = fm
            flux_x[1, f] = fn
            flux_x[2, f] = ft
            flux_x[3, f] = fe
        for col in range(nx):
            for k in range(4):
                rate[k, row, col] = (flux_x[k, col] - flux_x[k, col + 1]) / dx + (
                    flux_y[k, row, col] - flux_y[k, row + 1, col]
                ) / dy


def euler_rhs(state, domain):
    """dU/dt = -div(F) for every cell of state (4, ny, nx); zero in the step."""
    rate = np.empty_like(state)
    wx, wy = padded_primitives(state, domain)
    flux_divergence(wx, wy, domain.dx, domain.dy, GAMMA, rate)
    rate[:, : domain.step_j, domain.step_i :] = 0.0
    return rate


@njit(cache=False, parallel=True)
def signal_rates(state, gamma, dx, dy, step_i, step_j):
    """Largest (|u| + c)/dx + (|v| + c)/dy of each row, skipping the step."""
    ny, nx = state.shape[1], state.shape[2]
    rates = np.zeros(ny)
    for row in prange(ny):
        for col in range(nx):
            if row < step_j and col >= step_i:
                continue
            rho = state[0, row, col]
            u = state[1, row, col] / rho
            v = state[2, row, col] / rho
            p = (gamma - 1.0) * (state[3, row, col] - 0.5 * rho * (u * u + v * v))
            c = math.sqrt(gamma * max(p, 0.0) / rho)
            rates[row] = max(rates[row], (abs(u) + c) / dx + (abs(v) + c) / dy)
    return rates


def max_signal_rate(state, domain):
    """max of (|u| + c)/dx + (|v| + c)/dy over the fluid; dt times it is the
    CFL number of the unsplit scheme."""
    return signal_rates(
        state, GAMMA, domain.dx, domain.dy, domain.step_i, domain.step_j
    ).max()


def apply_floors(state):
    """Keep density and pressure positive; return the number of cells changed.

    A cell whose density drops below DENSITY_FLOOR gets that density and loses
    its momentum; a cell whose pressure drops below PRESSURE_FLOOR gets that
    pressure by raising its energy. Neither happens in the default run (the
    reconstruction falls back to first order where it would create negative
    states), so there the scheme stays exactly conservative.
    """
    low_density = state[0] < DENSITY_FLOOR
    if low_density.any():
        state[0, low_density] = DENSITY_FLOOR
        state[1:3, low_density] = 0.0
    kinetic = 0.5 * (state[1] ** 2 + state[2] ** 2) / state[0]
    low_pressure = (GAMMA - 1.0) * (state[3] - kinetic) < PRESSURE_FLOOR
    if low_pressure.any():
        state[3, low_pressure] = PRESSURE_FLOOR / (GAMMA - 1.0) + kinetic[low_pressure]
    return int(np.count_nonzero(low_density | low_pressure))


def ssp_rk2_step(state, dt, domain):
    """Heun's method, the two-stage strong-stability-preserving Runge-Kutta
    scheme. Returns the new state and the number of floored cells."""
    stage = state + dt * euler_rhs(state, domain)
    floored = apply_floors(stage)
    stage += dt * euler_rhs(stage, domain)
    stage += state
    stage *= 0.5
    return stage, floored + apply_floors(stage)


def advance_cfl(state, dt, domain, cfl=CFL):
    """Advance state by dt in as few equal Runge-Kutta steps as the CFL limit allows.

    Returns the new state, the number of steps, their CFL number (measured
    at the start) and the number of floored cells.
    """
    rate = max_signal_rate(state, domain)
    n_steps = max(1, math.ceil(dt * rate / cfl))
    floored = 0
    for _ in range(n_steps):
        state, count = ssp_rk2_step(state, dt / n_steps, domain)
        floored += count
    return state, n_steps, dt / n_steps * rate, floored


class ForwardStepSimulation(Simulation):
    """Conservative state of the Mach 3 tunnel; one step advances it by ``dt``.

    The time step is fixed so that frames are evenly spaced in time. Should
    its CFL number exceed ``CFL`` (on a finer grid, say), the step is split
    into as many equal Runge-Kutta steps as needed.
    """

    def __init__(self, cells_per_unit=CELLS_PER_UNIT, dt=TIME_STEP):
        super().__init__()
        self.domain = make_tunnel(cells_per_unit)
        self.dt = dt
        shape = (self.domain.ny, self.domain.nx)
        self.state = conservative(*(np.full(shape, q) for q in INFLOW))
        self.cfl = dt * max_signal_rate(self.state, self.domain)
        self.runge_kutta_steps = 0
        self.floored_cells = 0

    def step(self):
        self.state, n_steps, self.cfl, floored = advance_cfl(
            self.state, self.dt, self.domain
        )
        self.runge_kutta_steps += n_steps
        self.floored_cells += floored

    def field(self, name):
        """Density, pressure or Mach number (ny, nx), NaN inside the step."""
        rho, u, v, p = primitive(self.state)
        value = {
            "density": rho,
            "pressure": p,
            "mach": np.sqrt((u * u + v * v) * rho / (GAMMA * p)),
        }[name].copy()
        value[self.domain.solid] = np.nan
        return value

    def standoff(self):
        """Distance from the step face to the bow shock along the bottom wall.

        The shock is the first cell in front of the step where the pressure
        exceeds twice the inflow pressure; zero before the shock forms.
        """
        i = self.domain.step_i
        p = primitive(self.state[:, :1, :i])[3, 0]
        shocked = np.nonzero(p > 2.0 * INFLOW[3])[0]
        if shocked.size == 0:
            return 0.0
        return (i - shocked[0]) * self.domain.dx

    def schlieren(self, scale=SCHLIEREN_SCALE):
        """Numerical schlieren exp(-|grad rho| / scale), NaN inside the step.

        Central differences use the mirrored ghost cells of the solver, so
        the walls and the step faces do not appear as density jumps.
        """
        domain = self.domain
        wx, wy = padded_primitives(self.state, domain)
        drho_dx = (wx[0, :, 3:-1] - wx[0, :, 1:-3]) / (2.0 * domain.dx)
        drho_dy = (wy[0, 3:-1] - wy[0, 1:-3]) / (2.0 * domain.dy)
        image = np.exp(-np.hypot(drho_dx, drho_dy) / scale)
        image[domain.solid] = np.nan
        return image


class ForwardStepView(View):
    """Schlieren, Mach number and pressure maps stacked above each other.

    The schlieren colour map is reversed: smooth flow is black, and steep
    density gradients (shocks, the slip line) glow white. The step is grey.
    """

    figsize = (10.0, 9.4)

    def __init__(self, simulation, figure, portrait=False):
        super().__init__(simulation, figure, portrait)
        axes = figure.subplots(3, 1, sharex=True)
        extent = (0.0, TUNNEL_LENGTH, 0.0, TUNNEL_HEIGHT)
        panels = (
            ("schlieren", "bone_r", (0.0, 1.0), "Numerical schlieren"),
            ("mach", "turbo", MACH_LIMITS, "Mach number"),
            ("pressure", "magma", PRESSURE_LIMITS, r"Pressure $p\,/\,p_\infty$"),
        )
        self.images = {}
        for ax, (name, cmap, limits, title) in zip(axes, panels):
            image = ax.imshow(
                self.field(name), extent=extent, vmin=limits[0], vmax=limits[1],
                cmap=colormaps[cmap].with_extremes(bad=STEP_COLOR),
                interpolation="bilinear",
            )  # fmt: skip
            self.images[name] = image
            if name != "schlieren":
                figure.colorbar(image, ax=ax, pad=0.015, fraction=0.04)
            ax.set_title(title)
            ax.set_ylabel("y")
        # An invisible colour bar keeps the schlieren panel as wide as the others.
        figure.colorbar(
            self.images["schlieren"], ax=axes[0], pad=0.015, fraction=0.04
        ).ax.set_visible(False)
        axes[-1].set_xlabel("x")

    def field(self, name):
        if name == "schlieren":
            return self.simulation.schlieren()
        return self.simulation.field(name)

    def draw(self):
        for name, image in self.images.items():
            image.set_data(self.field(name))

    def status(self):
        simulation = self.simulation
        return (
            f"t = {simulation.time:.2f}   shock stand-off {simulation.standoff():.2f}"
        )


ANIMATION = Animation(
    title="Mach 3 Forward-Facing Step",
    subtitle="Shock reflections in a supersonic tunnel",
    filename="supersonic_forward_facing_step.png",
    frames=N_FRAMES,
    steps_per_frame=STEPS_PER_FRAME,
    step_label=f"time steps of dt = {TIME_STEP:g}",
)


def main(argv=None):
    args = ANIMATION.parser(__doc__).parse_args(argv)
    simulation = ANIMATION.run(args, ForwardStepSimulation(), ForwardStepView)
    rho, _, _, p = primitive(simulation.state)
    fluid = ~simulation.domain.solid
    print(
        f"t = {simulation.time:.3f} after {simulation.runge_kutta_steps} Runge-Kutta "
        f"steps (CFL {simulation.cfl:.2f}): density {rho[fluid].min():.3f} to "
        f"{rho[fluid].max():.3f}, pressure {p[fluid].min():.3f} to "
        f"{p[fluid].max():.3f}, floored cells {simulation.floored_cells}"
    )


if __name__ == "__main__":
    main()
