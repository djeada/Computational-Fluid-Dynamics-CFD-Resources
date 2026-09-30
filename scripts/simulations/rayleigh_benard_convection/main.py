"""Rayleigh-Benard convection in a 2D Boussinesq fluid, rendered with Pygame.

A layer heated from below (T = 1 at the bottom wall, T = 0 at the top wall,
periodic side boundaries) is solved in vorticity-streamfunction form in
free-fall units. Small seeded temperature noise grows into convection rolls,
and the temperature field is drawn as a colour map in real time.
"""

import os
import sys
from pathlib import Path

import numpy as np
from scipy import fft

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int  # noqa: E402

# Physical parameters (dimensionless)
RAYLEIGH = 1.0e5  # Ra = g beta dT H^3 / (nu kappa)
PRANDTL = 1.0  # Pr = nu / kappa
DIFFUSIVITY = 1.0 / np.sqrt(RAYLEIGH * PRANDTL)  # kappa in free-fall units
VISCOSITY = np.sqrt(PRANDTL / RAYLEIGH)  # nu in free-fall units
T_BOTTOM, T_TOP = 1.0, 0.0  # wall temperatures (hot bottom, cold top)
NOISE_AMPLITUDE = 1e-2  # initial temperature perturbation
SEED = 0

# Numerical parameters
GRID_SIZE = 128  # nodes in x (periodic) and in z (walls included)
MAX_TIME_STEP = 2e-3  # free-fall time units; diffusion limit is about 2.4e-3
CFL = 0.4  # advective Courant number used to shrink dt when the flow is fast
STEPS_PER_FRAME = 20  # time steps between drawn frames

# Display parameters
WINDOW_SIZE = 400
FPS = 60


def value_to_color(values):
    """Map values in [0, 1] to RGB: blue -> cyan -> green -> yellow -> red."""
    v = np.clip(values, 0.0, 1.0)
    r = np.clip(4 * v - 2, 0, 1)
    g = np.where(v < 0.75, np.clip(4 * v, 0, 1), np.clip(4 - 4 * v, 0, 1))
    b = np.clip(2 - 4 * v, 0, 1)
    return (255 * np.stack([r, g, b], axis=-1)).astype(np.uint8)


def initialize_fields(rng):
    """Conductive temperature profile plus noise; fluid at rest.

    Arrays are indexed [j, i] with j = 0 at the bottom wall and i along x.
    """
    z = np.linspace(0.0, 1.0, GRID_SIZE)
    temperature = np.tile(T_BOTTOM + (T_TOP - T_BOTTOM) * z[:, None], (1, GRID_SIZE))
    temperature[1:-1] += NOISE_AMPLITUDE * rng.standard_normal(
        (GRID_SIZE - 2, GRID_SIZE)
    )
    vorticity = np.zeros_like(temperature)
    return temperature, vorticity


def poisson_eigenvalues(dx, dz):
    """Eigenvalues of the 5-point Laplacian for periodic x and psi = 0 walls."""
    m = np.arange(GRID_SIZE)
    n = np.arange(1, GRID_SIZE - 1)
    lam_x = -((2 * np.sin(np.pi * m / GRID_SIZE) / dx) ** 2)
    lam_z = -((2 * np.sin(np.pi * n / (2 * (GRID_SIZE - 1))) / dz) ** 2)
    return lam_z[:, None] + lam_x[None, :]


def solve_streamfunction(vorticity, eigenvalues):
    """Solve lap(psi) = -omega exactly (FFT in x, DST-I in z)."""
    rhs = -vorticity[1:-1]
    rhs_hat = fft.fft(fft.dst(rhs, type=1, axis=0), axis=1)
    psi_interior = fft.idst(
        np.real(fft.ifft(rhs_hat / eigenvalues, axis=1)), type=1, axis=0
    )
    psi = np.zeros_like(vorticity)
    psi[1:-1] = psi_interior
    return psi


def velocities(psi, dx, dz):
    """u = d(psi)/dz, w = -d(psi)/dx with central differences."""
    u = np.zeros_like(psi)
    u[1:-1] = (psi[2:] - psi[:-2]) / (2 * dz)
    w = -(np.roll(psi, -1, axis=1) - np.roll(psi, 1, axis=1)) / (2 * dx)
    return u, w


def upwind_advection(f, u, w, dx, dz):
    """First-order upwind approximation of u df/dx + w df/dz (interior rows)."""
    fx_minus = (f - np.roll(f, 1, axis=1)) / dx
    fx_plus = (np.roll(f, -1, axis=1) - f) / dx
    adv = np.zeros_like(f)
    fz_minus = (f[1:-1] - f[:-2]) / dz
    fz_plus = (f[2:] - f[1:-1]) / dz
    ui, wi = u[1:-1], w[1:-1]
    adv[1:-1] = (
        np.maximum(ui, 0) * fx_minus[1:-1]
        + np.minimum(ui, 0) * fx_plus[1:-1]
        + np.maximum(wi, 0) * fz_minus
        + np.minimum(wi, 0) * fz_plus
    )
    return adv


def laplacian(f, dx, dz):
    """5-point Laplacian on interior rows, periodic in x."""
    lap = np.zeros_like(f)
    lap[1:-1] = (np.roll(f, -1, axis=1) - 2 * f + np.roll(f, 1, axis=1))[
        1:-1
    ] / dx**2 + (f[2:] - 2 * f[1:-1] + f[:-2]) / dz**2
    return lap


def time_step(temperature, vorticity, eigenvalues, dx, dz):
    """Advance T and omega by one forward-Euler step; return the dt used."""
    psi = solve_streamfunction(vorticity, eigenvalues)
    u, w = velocities(psi, dx, dz)
    speed = np.abs(u).max() / dx + np.abs(w).max() / dz
    dt = MAX_TIME_STEP if speed == 0 else min(MAX_TIME_STEP, CFL / speed)

    # Thom's formula: no-slip walls with psi = 0 give omega_wall = -2 psi_1 / dz^2.
    vorticity[0] = -2 * psi[1] / dz**2
    vorticity[-1] = -2 * psi[-2] / dz**2

    dT_dx = (np.roll(temperature, -1, axis=1) - np.roll(temperature, 1, axis=1)) / (
        2 * dx
    )
    temperature += dt * (
        -upwind_advection(temperature, u, w, dx, dz)
        + DIFFUSIVITY * laplacian(temperature, dx, dz)
    )
    vorticity += dt * (
        -upwind_advection(vorticity, u, w, dx, dz)
        + VISCOSITY * laplacian(vorticity, dx, dz)
        + dT_dx
    )
    temperature[0], temperature[-1] = T_BOTTOM, T_TOP
    return dt


def nusselt_number(temperature, dz):
    """Mean conductive heat flux through the bottom wall, relative to conduction."""
    dT_dz = (-3 * temperature[0] + 4 * temperature[1] - temperature[2]) / (2 * dz)
    return float(np.mean(-dT_dz) / (T_BOTTOM - T_TOP))


def draw_grid(screen, pygame, temperature):
    """Draw the temperature field with the hot bottom wall at the bottom."""
    rgb = value_to_color(temperature[::-1])  # row 0 of the image is the top wall
    surface = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))
    screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help=f"frames to run, each {STEPS_PER_FRAME} time steps "
        "(default: until the window is closed)",
    )
    args = parser.parse_args(argv)

    if args.no_show:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    import pygame

    dx = 1.0 / GRID_SIZE  # periodic: GRID_SIZE nodes span one unit
    dz = 1.0 / (GRID_SIZE - 1)  # walls at z = 0 and z = 1
    eigenvalues = poisson_eigenvalues(dx, dz)
    temperature, vorticity = initialize_fields(np.random.default_rng(SEED))

    pygame.init()
    try:
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Rayleigh Bénard Convection")
        clock = pygame.time.Clock()
        time = 0.0

        for frame in range(args.steps):
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break
            for _ in range(STEPS_PER_FRAME):
                time += time_step(temperature, vorticity, eigenvalues, dx, dz)
            draw_grid(screen, pygame, temperature)
            pygame.display.flip()
            if not args.no_show:
                clock.tick(FPS)

        print(
            f"Ra = {RAYLEIGH:g}, Pr = {PRANDTL:g}: t = {time:.1f} free-fall times, "
            f"Nusselt number = {nusselt_number(temperature, dz):.2f}"
        )
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            pygame.image.save(
                screen, str(args.output / "rayleigh_benard_convection.png")
            )
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
