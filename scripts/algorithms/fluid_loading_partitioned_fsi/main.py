"""Partitioned FSI of a membrane on a fluid layer: added-mass instability and Aitken.

A tensioned membrane (a string of mass m_s per unit area and tension T) lies
on a layer of incompressible, inviscid fluid of depth H in a channel whose
ends are open (p = 0). The structure solver is a finite-difference membrane
advanced with the Newmark average-acceleration rule; the fluid solver returns
the interface pressure for a given membrane acceleration from the exact
potential-flow solution of each sine mode, p = -M_A w''. The two solvers are
coupled Dirichlet-Neumann: the fluid receives the motion, the structure the
pressure. Explicit (loose) coupling uses the pressure of the previous step;
implicit (strong) coupling iterates within each step, without relaxation,
with a constant relaxation factor, or with Aitken's dynamic relaxation
(Kuttler and Wall 2008). The figure shows the sub-iteration residuals, the
growth of explicit coupling above the added-mass ratio m_a / m_s = 1, the
stability map against time step, and the wet-to-dry frequency ratios.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

LENGTH = 1.0  # membrane span L (m)
FLUID_DEPTH = 0.2  # fluid layer depth H (m)
N_NODES = 31  # interior membrane nodes
STRUCT_MASS = 78.5  # m_s = rho_s h_s, a 10 mm steel plate (kg/m^2)
DRY_FREQUENCY = 20.0  # first dry natural frequency (Hz), sets the tension
RHO_WATER = 1000.0  # (kg/m^3)
RHO_AIR = 1.2  # (kg/m^3)
DT = 1.0e-3  # time step (s)
N_STEPS = 400  # steps of the coupled run (0.4 s)
IMPACT_VELOCITY = 0.1  # peak of the initial triangular velocity field (m/s)
IMPACT_POSITION = 0.3  # position of the peak as a fraction of L
NEWMARK_BETA, NEWMARK_GAMMA = 0.25, 0.5  # average-acceleration (trapezoidal) rule
TOLERANCE = 1.0e-8  # interface pressure residual relative to the first fluid response
MAX_ITER = 60  # sub-iterations per step
OMEGA_CONSTANT = 0.2  # constant relaxation factor
ENVELOPE_STEPS = 40  # window of the deflection envelope in panel (b)
OMEGA_START = 0.1  # first relaxation factor of Aitken's method in each step


class Membrane:
    """Finite-difference membrane with N interior nodes and fixed ends."""

    def __init__(self, n=N_NODES, length=LENGTH, mass=STRUCT_MASS, f_dry=DRY_FREQUENCY):
        self.n = n
        self.h = length / (n + 1)
        self.x = self.h * np.arange(1, n + 1)
        self.mass = mass
        # Tension giving the continuous first dry frequency f_dry.
        self.tension = mass * (2.0 * length * f_dry) ** 2
        main = 2.0 * np.ones(n)
        off = -np.ones(n - 1)
        self.stiffness = (
            self.tension
            / self.h**2
            * (np.diag(main) + np.diag(off, 1) + np.diag(off, -1))
        )

    def eigenvalues(self):
        """Eigenvalues of the stiffness matrix, (4T/h^2) sin^2(j pi / (2(N+1)))."""
        j = np.arange(1, self.n + 1)
        return (
            4.0 * self.tension / self.h**2 * np.sin(j * np.pi / (2 * (self.n + 1))) ** 2
        )


def sine_basis(n):
    """Orthonormal DST-I matrix S with S_ij = sqrt(2/(n+1)) sin(i j pi / (n+1))."""
    i = np.arange(1, n + 1)
    return np.sqrt(2.0 / (n + 1)) * np.sin(np.outer(i, i) * np.pi / (n + 1))


def modal_added_mass(n, rho_f, length=LENGTH, depth=FLUID_DEPTH):
    """Added mass per unit area of sine mode j: rho_f coth(k_j H) / k_j, k_j = j pi / L."""
    k = np.arange(1, n + 1) * np.pi / length
    return rho_f / (k * np.tanh(k * depth))


class FluidLayer:
    """Potential-flow fluid solver: interface pressure from membrane acceleration."""

    def __init__(self, n=N_NODES, rho_f=RHO_WATER):
        basis = sine_basis(n)
        self.modal_mass = modal_added_mass(n, rho_f)
        self.added_mass = basis @ np.diag(self.modal_mass) @ basis.T

    def pressure(self, acceleration):
        """p = -M_A a at the membrane nodes (Pa)."""
        return -self.added_mass @ acceleration


class NewmarkStructure:
    """Membrane state advanced by the Newmark rule for a given pressure load."""

    def __init__(self, membrane, dt=DT, beta=NEWMARK_BETA, gamma=NEWMARK_GAMMA):
        self.m = membrane
        self.dt, self.beta, self.gamma = dt, beta, gamma
        self.effective = (
            membrane.mass * np.eye(membrane.n) + beta * dt**2 * membrane.stiffness
        )
        self.effective_inv = np.linalg.inv(self.effective)

    def initial_state(self, v0):
        """Undeflected membrane with velocity v0; then K w = 0 and p = 0, so a = 0."""
        zero = np.zeros_like(v0)
        return zero, v0.copy(), zero.copy()

    def predictor(self, state):
        w, v, a = state
        return w + self.dt * v + self.dt**2 * (0.5 - self.beta) * a

    def solve(self, state, pressure):
        """Acceleration at the new step for an imposed interface pressure."""
        rhs = pressure - self.m.stiffness @ self.predictor(state)
        return self.effective_inv @ rhs

    def update(self, state, a_new):
        w, v, a = state
        w_new = self.predictor(state) + self.beta * self.dt**2 * a_new
        v_new = v + self.dt * ((1.0 - self.gamma) * a + self.gamma * a_new)
        return w_new, v_new, a_new


def impact_velocity(membrane, amplitude=IMPACT_VELOCITY, position=IMPACT_POSITION):
    """Triangular initial velocity field peaking at x = position L (a slam)."""
    xp = position * LENGTH
    x = membrane.x
    return amplitude * np.where(x <= xp, x / xp, (LENGTH - x) / (LENGTH - xp))


def coupled_step(structure, fluid, state, p_guess, method, omega0=OMEGA_START):
    """One time step of Dirichlet-Neumann coupling.

    method is "explicit" (one structure solve with p_guess, then a fluid
    update), "fixed" (unrelaxed sub-iterations), "constant" (relaxation
    factor OMEGA_CONSTANT) or "aitken". Returns (state, pressure, residuals).
    """
    p = p_guess.copy()
    residuals = []
    omega = OMEGA_CONSTANT if method == "constant" else omega0
    r_old = None
    scale = None
    for _ in range(1 if method == "explicit" else MAX_ITER):
        a = structure.solve(state, p)
        p_fluid = fluid.pressure(a)
        r = p_fluid - p
        if scale is None:  # fixed per step: the first fluid response
            scale = max(np.linalg.norm(p_fluid), 1e-300)
        residuals.append(np.linalg.norm(r) / scale)
        if method == "explicit":
            return structure.update(state, a), p_fluid, residuals
        if residuals[-1] < TOLERANCE:
            break
        if method == "fixed":
            omega = 1.0
        elif method == "aitken" and r_old is not None:
            dr = r - r_old
            omega = -omega * (r_old @ dr) / (dr @ dr)
        p = p + omega * r
        r_old = r
    a = structure.solve(state, p)
    return structure.update(state, a), p, residuals


def run(method, rho_f=RHO_WATER, n_steps=N_STEPS, dt=DT, mass=STRUCT_MASS, blow_up=1.0):
    """Max |w| per step, displacement history and sub-iterations per step.

    The run stops early once max |w| exceeds ``blow_up`` metres.
    """
    membrane = Membrane(mass=mass)
    structure = NewmarkStructure(membrane, dt)
    fluid = FluidLayer(rho_f=rho_f)
    state = structure.initial_state(impact_velocity(membrane))
    p = np.zeros(membrane.n)
    w_max, w_hist, iterations = [], [], []
    for _ in range(n_steps):
        state, p, res = coupled_step(structure, fluid, state, p, method)
        w_max.append(np.abs(state[0]).max())
        w_hist.append(state[0].copy())
        iterations.append(len(res))
        if w_max[-1] > blow_up:
            break
    return np.array(w_max), np.array(w_hist), np.array(iterations)


def monolithic(rho_f=RHO_WATER, n_steps=N_STEPS, dt=DT, mass=STRUCT_MASS):
    """Reference: (m_s I + M_A) w'' + K w = 0 advanced by the same Newmark rule."""
    membrane = Membrane(mass=mass)
    fluid = FluidLayer(rho_f=rho_f)
    total = mass * np.eye(membrane.n) + fluid.added_mass
    eff_inv = np.linalg.inv(total + NEWMARK_BETA * dt**2 * membrane.stiffness)
    v = impact_velocity(membrane)
    w = np.zeros_like(v)
    a = np.zeros_like(v)
    hist = []
    for _ in range(n_steps):
        pred = w + dt * v + dt**2 * (0.5 - NEWMARK_BETA) * a
        a_new = eff_inv @ (-membrane.stiffness @ pred)
        w = pred + NEWMARK_BETA * dt**2 * a_new
        v = v + dt * ((1 - NEWMARK_GAMMA) * a + NEWMARK_GAMMA * a_new)
        a = a_new
        hist.append(w.copy())
    return np.array(hist)


def explicit_amplification(
    mass_ratio, omega_dt, beta=NEWMARK_BETA, gamma=NEWMARK_GAMMA
):
    """Spectral radius of explicit coupling for one mode.

    Scalar model m_s a + k w = -m_a a_old with Newmark updates, written for
    m_s = 1, k = omega^2 = 1 and time step omega_dt. State (w, v, a).
    """
    dt = omega_dt
    k, ms, ma = 1.0, 1.0, mass_ratio
    m_eff = ms + beta * dt**2 * k
    ra = np.array([-k, -k * dt, -k * dt**2 * (0.5 - beta) - ma]) / m_eff
    rw = np.array([1.0, dt, dt**2 * (0.5 - beta)]) + beta * dt**2 * ra
    rv = np.array([0.0, 1.0, dt * (1.0 - gamma)]) + gamma * dt * ra
    return np.max(np.abs(np.linalg.eigvals(np.array([rw, rv, ra]))))


def iteration_factor(membrane, fluid, dt=DT):
    """Spectral radius of unrelaxed sub-iterations, max m_a,j / (m_s + beta dt^2 lambda_j)."""
    lam = membrane.eigenvalues()
    return np.max(fluid.modal_mass / (membrane.mass + NEWMARK_BETA * dt**2 * lam))


def wet_dry_ratio(rho_f, mass=STRUCT_MASS):
    """Wet/dry natural frequency ratios from the coupled eigenproblem, by mode."""
    membrane = Membrane(mass=mass)
    fluid = FluidLayer(rho_f=rho_f)
    basis = sine_basis(membrane.n)
    lam = membrane.eigenvalues()
    total = mass * np.eye(membrane.n) + fluid.added_mass
    wet = np.sort(
        np.real(np.linalg.eigvals(np.linalg.solve(total, membrane.stiffness)))
    )
    dry = np.sort(lam / mass)
    # The modes stay sine modes, so sort order matches; check the basis is modal.
    modal = basis.T @ total @ basis
    assert np.allclose(modal, np.diag(np.diag(modal)), atol=1e-8 * modal.max())
    return np.sqrt(wet / dry), np.sqrt(mass / (mass + fluid.modal_mass))


def running_max(values, window):
    """Maximum of each value and the window - 1 values before it."""
    return np.array(
        [values[max(0, i - window + 1) : i + 1].max() for i in range(len(values))]
    )


def make_figure(residuals, growth, stability, wet):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    ax = axes[0, 0]
    labels = {
        "fixed": "unrelaxed fixed point",
        "constant": f"constant relaxation $\\omega$ = {OMEGA_CONSTANT:g}",
        "aitken": "Aitken dynamic relaxation",
    }
    colors = {"fixed": "tab:red", "constant": "tab:orange", "aitken": "tab:blue"}
    for method, res in residuals.items():
        ax.semilogy(
            np.arange(1, len(res) + 1),
            res,
            "o-",
            ms=4,
            color=colors[method],
            label=labels[method],
        )
    ax.axhline(TOLERANCE, color="0.4", ls="--", lw=1, label="tolerance")
    ax.set_ylim(1e-12, 1e8)
    ax.set_xlabel("Sub-iteration within the first time step", fontsize=11)
    ax.set_ylabel("Relative interface pressure residual", fontsize=11)
    ax.set_title("(a) Implicit coupling, water on a 10 mm steel membrane", fontsize=12)
    ax.legend(fontsize=10, loc="upper right")

    ax = axes[0, 1]
    colors_b = ("tab:blue", "tab:green", "tab:orange", "tab:red", "tab:purple")
    for (ratio, w_max), color in zip(growth.items(), colors_b):
        t = DT * np.arange(1, len(w_max) + 1) * 1e3
        envelope = running_max(w_max, ENVELOPE_STEPS)
        ax.semilogy(
            t, envelope * 1e3, color=color, lw=2, label=f"$m_{{a,1}}/m_s$ = {ratio:g}"
        )
    ax.set_xlabel("Time (ms)", fontsize=11)
    ax.set_ylabel(f"Max $|w|$ over the last {ENVELOPE_STEPS} steps (mm)", fontsize=11)
    ax.set_title("(b) Explicit coupling against added-mass ratio", fontsize=12)
    ax.legend(fontsize=10, loc="upper left")
    ax.set_ylim(1e-2, 1e4)

    ax = axes[1, 0]
    ratios, omega_dts, rho = stability
    mesh = ax.pcolormesh(
        omega_dts,
        ratios,
        np.log10(rho),
        cmap="RdBu_r",
        vmin=-0.5,
        vmax=0.5,
        shading="auto",
    )
    ax.contour(omega_dts, ratios, rho, levels=[1.0 + 1e-9], colors="k", linewidths=1.5)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.text(omega_dts[1], 1.25, "unstable", fontsize=11, color="k")
    ax.text(omega_dts[1], 0.6, "stable", fontsize=11, color="k")
    fig.colorbar(mesh, ax=ax, label="$\\log_{10}$ spectral radius")
    ax.set_xlabel(
        "Dimensionless time step $\\omega_j\\,\\Delta t$ (dry mode)", fontsize=11
    )
    ax.set_ylabel("Added-mass ratio $m_{a,j}/m_s$", fontsize=11)
    ax.set_title("(c) Explicit coupling stability map (one mode)", fontsize=12)

    ax = axes[1, 1]
    for name, (numeric, analytic), color in zip(
        wet.keys(), wet.values(), ("tab:blue", "tab:orange")
    ):
        j = np.arange(1, len(numeric) + 1)
        ax.plot(
            j, numeric, "o", ms=7, color=color, label=f"{name}: coupled eigenproblem"
        )
        ax.plot(
            j,
            analytic,
            "-",
            color=color,
            lw=1.2,
            label=f"{name}: $\\sqrt{{m_s/(m_s + m_{{a,j}})}}$",
        )
    ax.set_xlim(0.5, 10.5)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Mode number $j$", fontsize=11)
    ax.set_ylabel("Wet / dry natural frequency", fontsize=11)
    ax.set_title("(d) Added mass lowers the natural frequencies", fontsize=12)
    ax.legend(fontsize=9.5, loc="lower right")
    for a in (axes[0, 0], axes[0, 1], axes[1, 1]):
        a.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    membrane = Membrane()
    water = FluidLayer(rho_f=RHO_WATER)
    air = FluidLayer(rho_f=RHO_AIR)
    print(
        f"tension = {membrane.tension / 1e3:.1f} kN/m, m_s = {STRUCT_MASS} kg/m^2, "
        f"m_a,1 (water) = {water.modal_mass[0]:.1f} kg/m^2 (ratio {water.modal_mass[0] / STRUCT_MASS:.2f}), "
        f"m_a,1 (air) = {air.modal_mass[0]:.3f} kg/m^2 (ratio {air.modal_mass[0] / STRUCT_MASS:.4f})"
    )
    print(
        f"unrelaxed sub-iteration factor (water, dt = {DT:g} s) = {iteration_factor(membrane, water):.3f}"
    )

    # (a) residuals within the first step for water.
    structure = NewmarkStructure(membrane)
    state0 = structure.initial_state(impact_velocity(membrane))
    residuals = {}
    for method in ("fixed", "constant", "aitken"):
        _, _, res = coupled_step(structure, water, state0, np.zeros(membrane.n), method)
        residuals[method] = np.array(res)[np.array(res) < 1e8]
        print(f"  {method:8s}: {len(res)} sub-iterations, final residual {res[-1]:.2e}")

    # Implicit Aitken run against the monolithic reference.
    reference = monolithic()
    _, w_aitken, iters = run("aitken")
    err = np.abs(w_aitken - reference).max() / np.abs(reference).max()
    print(
        f"Aitken over {N_STEPS} steps: mean {iters.mean():.1f}, max {iters.max()} sub-iterations; "
        f"max deviation from monolithic = {err:.1e} (relative)"
    )
    w_air, _, _ = run("explicit", rho_f=RHO_AIR)
    ref_air = monolithic(rho_f=RHO_AIR)
    err_air = np.abs(w_air - np.abs(ref_air).max(axis=1)).max() / np.abs(ref_air).max()
    print(
        f"explicit coupling in air: max |w| = {1e3 * w_air.max():.3f} mm, deviation from monolithic = {err_air:.1e}"
    )

    # (b) explicit growth for several added-mass ratios (fluid density varied).
    growth = {}
    m_a1_per_rho = modal_added_mass(1, 1.0)[0]
    water_ratio = round(float(water.modal_mass[0] / STRUCT_MASS), 2)
    for ratio in (0.5, 0.95, 1.05, 1.5, water_ratio):
        rho_f = ratio * STRUCT_MASS / m_a1_per_rho
        w_max, _, _ = run("explicit", rho_f=rho_f, n_steps=N_STEPS, blow_up=10.0)
        growth[ratio] = w_max
        print(
            f"  explicit, m_a1/m_s = {ratio:5.2f} (rho_f = {rho_f:7.1f}): {len(w_max)} steps, final max|w| = {1e3 * w_max[-1]:.3g} mm"
        )

    # (c) stability map.
    ratios = np.geomspace(0.1, 10.0, 81)
    omega_dts = np.geomspace(1e-3, 10.0, 81)
    rho = np.array([[explicit_amplification(r, w) for w in omega_dts] for r in ratios])

    # (d) wet/dry frequency ratios.
    wet = {"water": wet_dry_ratio(RHO_WATER), "air": wet_dry_ratio(RHO_AIR)}
    print(
        "wet/dry frequency ratio, modes 1-4 (water): "
        + ", ".join(f"{v:.3f}" for v in wet["water"][0][:4])
    )

    fig = make_figure(residuals, growth, (ratios, omega_dts, rho), wet)
    finish_figures(
        {"fluid_loading_partitioned_fsi.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
