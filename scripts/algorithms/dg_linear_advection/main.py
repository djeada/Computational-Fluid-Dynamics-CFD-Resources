"""Discontinuous Galerkin method for 1D periodic linear advection with an upwind flux and SSP-RK3.

Solves u_t + a u_x = 0 on the periodic unit interval with a modal Legendre
basis of degree p = 0..3 in every element, an upwind numerical flux at the
element faces and the three-stage strong-stability-preserving Runge-Kutta
method in time. The figure shows a Gaussian pulse and a square pulse after
one period for p = 1 and p = 3 on 20 elements, and the L2 error for a smooth
wave against the number of elements, which falls as h^(p+1).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import legendre

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

ADVECTION_SPEED = 1.0  # a [m/s]
DOMAIN_LENGTH = 1.0  # L [m], periodic
PERIOD = DOMAIN_LENGTH / ADVECTION_SPEED  # time for one transit [s]
CFL_BASE = 0.5  # dt = CFL_BASE / (2p + 1) * h / |a|
DEGREES = (0, 1, 2, 3)
N_ELEMENTS_STUDY = (4, 8, 16, 32, 64, 128, 256)
N_ELEMENTS_PLOT = 20
N_QUAD = 12  # Gauss points for projection and error integrals


def legendre_values(xi, degree):
    """P_0..P_degree evaluated at xi, shape (degree + 1, len(xi))."""
    xi = np.atleast_1d(xi)
    return np.array(
        [legendre.legval(xi, np.eye(degree + 1)[m]) for m in range(degree + 1)]
    )


def volume_matrix(degree):
    """S_mn = integral over [-1, 1] of P_m'(xi) P_n(xi) dxi."""
    xq, wq = legendre.leggauss(degree + 2)
    p = legendre_values(xq, degree)
    dp = np.array(
        [
            legendre.legval(xq, legendre.legder(np.eye(degree + 1)[m]))
            for m in range(degree + 1)
        ]
    )
    return (dp * wq) @ p.T


class DGAdvection:
    """Semi-discrete DG operator for u_t + a u_x = 0 on a periodic uniform mesh.

    The state is an array c of shape (K, p + 1) of Legendre coefficients:
    on element k, u_h = sum_m c[k, m] P_m(xi) with x = x_k + (h / 2) xi.
    """

    def __init__(self, n_elements, degree, speed=ADVECTION_SPEED, flux="upwind"):
        self.k = n_elements
        self.p = degree
        self.a = speed
        self.flux = flux
        self.h = DOMAIN_LENGTH / n_elements
        self.centers = (np.arange(n_elements) + 0.5) * self.h
        m = np.arange(degree + 1)
        self.inv_mass = (2 * m + 1) / self.h  # inverse of the diagonal mass matrix
        self.sign_left = (-1.0) ** m  # P_m(-1)
        self.s = volume_matrix(degree)

    def project(self, func):
        """L2 projection of func onto the element polynomials."""
        xq, wq = legendre.leggauss(N_QUAD)
        p = legendre_values(xq, self.p)
        x = self.centers[:, None] + 0.5 * self.h * xq[None, :]
        m = np.arange(self.p + 1)
        return (func(x) * wq) @ p.T * (2 * m + 1) / 2.0

    def face_flux(self, c):
        """Numerical flux a u_hat at the right face of every element."""
        u_left_of_face = c.sum(axis=1)  # u_k(xi = +1)
        u_right_of_face = np.roll(c @ self.sign_left, -1)  # u_{k+1}(xi = -1)
        if self.flux == "upwind":
            u_hat = u_left_of_face if self.a >= 0 else u_right_of_face
        elif self.flux == "central":
            u_hat = 0.5 * (u_left_of_face + u_right_of_face)
        else:
            raise ValueError("flux must be 'upwind' or 'central'")
        return self.a * u_hat

    def rhs(self, c):
        """dc/dt = M^-1 [a S c - (f_hat_right P_m(1) - f_hat_left P_m(-1))]."""
        f_right = self.face_flux(c)
        f_left = np.roll(f_right, 1)
        volume = self.a * c @ self.s.T
        surface = f_right[:, None] - f_left[:, None] * self.sign_left[None, :]
        return (volume - surface) * self.inv_mass

    def stable_dt(self, cfl_base=CFL_BASE):
        return cfl_base / (2 * self.p + 1) * self.h / abs(self.a)

    def ssp_rk3_step(self, c, dt):
        c1 = c + dt * self.rhs(c)
        c2 = 0.75 * c + 0.25 * (c1 + dt * self.rhs(c1))
        return c / 3.0 + 2.0 / 3.0 * (c2 + dt * self.rhs(c2))

    def advance(self, c, t_end, dt=None):
        dt = self.stable_dt() if dt is None else dt
        n_steps = int(np.ceil(t_end / dt - 1e-12))
        dt = t_end / n_steps
        for _ in range(n_steps):
            c = self.ssp_rk3_step(c, dt)
        return c

    def evaluate(self, c, points_per_element=30):
        xi = np.linspace(-1.0, 1.0, points_per_element)
        p = legendre_values(xi, self.p)
        x = self.centers[:, None] + 0.5 * self.h * xi[None, :]
        return x, c @ p

    def l2_error(self, c, exact):
        xq, wq = legendre.leggauss(N_QUAD)
        p = legendre_values(xq, self.p)
        x = self.centers[:, None] + 0.5 * self.h * xq[None, :]
        err = c @ p - exact(x)
        return np.sqrt(0.5 * self.h * np.sum(wq * err**2))

    def mass(self, c):
        """Integral of u_h over the domain (only P_0 contributes)."""
        return self.h * c[:, 0].sum()

    def energy(self, c):
        """Squared L2 norm of u_h."""
        m = np.arange(self.p + 1)
        return np.sum(c**2 * self.h / (2 * m + 1))


def smooth_wave(x):
    return np.sin(2 * np.pi * x / DOMAIN_LENGTH)


def pulses(x):
    """Gaussian pulse centred at 0.25 and a square pulse on [0.6, 0.8]."""
    x = np.mod(x, DOMAIN_LENGTH)
    gauss = np.exp(-(((x - 0.25) / 0.05) ** 2))
    square = ((x > 0.6) & (x < 0.8)).astype(float)
    return gauss + square


def convergence_study(degrees=DEGREES, n_values=N_ELEMENTS_STUDY):
    """L2 error after one period for each degree and element count.

    The time step is reduced as h^((p+1)/3) relative to the base CFL so that
    the third-order time error stays below the spatial error of order p + 1.
    """
    results = {}
    for p in degrees:
        errs = []
        for k in n_values:
            solver = DGAdvection(k, p)
            dt = solver.stable_dt()
            if p >= 2:
                dt *= (solver.h / DOMAIN_LENGTH) ** ((p + 1) / 3.0 - 1.0)
                dt = min(dt, solver.stable_dt())
            c = solver.advance(solver.project(smooth_wave), PERIOD, dt)
            errs.append(solver.l2_error(c, smooth_wave))
        results[p] = np.array(errs)
    return np.array(n_values), results


def observed_orders(n_values, err):
    return np.log(err[:-1] / err[1:]) / np.log(n_values[1:] / n_values[:-1])


def make_figure(pulse_solutions, n_values, study):
    colors = plt.cm.tab10.colors
    fig = plt.figure(figsize=(13, 9.5))
    grid_spec = fig.add_gridspec(2, 2)
    x_fine = np.linspace(0.0, DOMAIN_LENGTH, 1000)

    for col, (p, (solver, c)) in enumerate(pulse_solutions.items()):
        ax = fig.add_subplot(grid_spec[0, col])
        ax.plot(x_fine, pulses(x_fine), "k-", linewidth=2, label="exact")
        x, u = solver.evaluate(c)
        for k in range(solver.k):
            ax.plot(
                x[k],
                u[k],
                "-",
                color=colors[col],
                linewidth=1.8,
                label=f"DG, p = {p}" if k == 0 else None,
            )
        faces = np.arange(solver.k + 1) * solver.h
        ax.plot(
            faces,
            np.full(faces.size, -0.25),
            "|",
            color="0.4",
            markersize=10,
            label="element faces",
        )
        ax.set_ylim(-0.35, 1.35)
        ax.set_xlim(0.0, DOMAIN_LENGTH)
        ax.set_xlabel("$x$ [m]", fontsize=11)
        ax.set_ylabel("$u$ [-]", fontsize=11)
        ax.set_title(
            f"({'ab'[col]}) p = {p}, {solver.k} elements, after one period", fontsize=12
        )
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        ax.legend(fontsize=9.5, loc="upper left")

    ax = fig.add_subplot(grid_spec[1, :])
    h = DOMAIN_LENGTH / n_values
    for p, err in study.items():
        rate = observed_orders(n_values, err)[-1]
        ax.loglog(
            h, err, "o-", color=colors[p], label=f"p = {p} (observed order {rate:.2f})"
        )
        ax.loglog(
            h, err[-1] * (h / h[-1]) ** (p + 1), ":", color=colors[p], linewidth=1
        )
    ax.set_xlabel("Element size $h$ [m]", fontsize=11)
    ax.set_ylabel(r"$L^2$ error after one period [-]", fontsize=11)
    ax.set_title(
        r"(c) Smooth wave $\sin 2\pi x$: error $\propto h^{p+1}$ (dotted: reference slopes)",
        fontsize=12,
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    ax.legend(fontsize=10, loc="lower right")
    fig.tight_layout()
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    pulse_solutions = {}
    for p in (1, 3):
        solver = DGAdvection(N_ELEMENTS_PLOT, p)
        c0 = solver.project(pulses)
        c = solver.advance(c0, PERIOD)
        pulse_solutions[p] = (solver, c)
        x, u = solver.evaluate(c)
        print(
            f"Pulses, p = {p}, K = {N_ELEMENTS_PLOT}: L2 error {solver.l2_error(c, pulses):.3e}, "
            f"max u {u.max():.3f}, min u {u.min():.3f}, "
            f"mass change {solver.mass(c) - solver.mass(c0):.1e}, "
            f"energy ratio {solver.energy(c) / solver.energy(c0):.4f}"
        )

    n_values, study = convergence_study()
    print("Smooth wave, L2 error after one period:")
    for p, err in study.items():
        text = ", ".join(f"K={k}: {e:.2e}" for k, e in zip(n_values, err))
        orders = " ".join(f"{q:.2f}" for q in observed_orders(n_values, err))
        print(f"  p = {p}: {text}\n         orders {orders}")

    fig = make_figure(pulse_solutions, n_values, study)
    finish_figures(
        {"dg_linear_advection.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
