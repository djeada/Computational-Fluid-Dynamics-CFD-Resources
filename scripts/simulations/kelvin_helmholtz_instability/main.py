"""Kelvin-Helmholtz instability in a periodic 2D incompressible shear flow.

Two shear layers (a central band moving right, the surrounding fluid moving
left) are seeded with a sinusoidal cross-stream perturbation. The velocity is
advanced with semi-Lagrangian advection, a spectral pressure projection and
explicit viscous diffusion, and a passive temperature field marks the two
layers so the roll-up is visible in the Pygame window.
"""

import os
import sys
from pathlib import Path

import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, positive_int  # noqa: E402

# Simulation parameters (grid units: dx = dy = 1)
GRID_SIZE = 256  # cells per side of the periodic square domain
WINDOW_SIZE = 512  # pixels per side
SHEAR_VELOCITY = 1.0  # U0: the band moves at +U0, the rest at -U0 [cells / time]
LAYER_THICKNESS = 4.0  # delta in the tanh velocity profile [cells]
PERTURBATION_AMPLITUDE = 0.05  # cross-stream velocity perturbation, fraction of U0
PERTURBATION_WAVES = 4  # wavelengths along x (lambda = 64 cells, k delta = 0.39)
NOISE_AMPLITUDE = 1e-3  # seeded random velocity noise, fraction of U0
SEED = 0
TIME_STEP = 0.5  # dt; Courant number U0 dt / dx = 0.5
VISCOSITY = 0.01  # nu [cells^2 / time]; nu dt / dx^2 = 0.005 < 0.25
DIFFUSION_RATE = 0.01  # thermal diffusivity D [cells^2 / time]
STEPS_PER_FRAME = 2  # solver steps between drawn frames
T_HOT, T_COLD = 1.0, 0.0  # temperature of the central band and of the outer fluid


def initialize_fields(n=GRID_SIZE, rng=None):
    """Double shear layer with a sinusoidal perturbation localised at both layers."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    j, i = np.meshgrid(np.arange(n), np.arange(n))  # j: x index, i: y index
    y1, y2 = n / 4, 3 * n / 4
    band = 0.5 * (
        np.tanh((i - y1) / LAYER_THICKNESS) - np.tanh((i - y2) / LAYER_THICKNESS)
    )

    u = SHEAR_VELOCITY * (2 * band - 1)
    envelope = np.exp(-(((i - y1) / (2 * LAYER_THICKNESS)) ** 2)) + np.exp(
        -(((i - y2) / (2 * LAYER_THICKNESS)) ** 2)
    )
    v = (
        PERTURBATION_AMPLITUDE
        * SHEAR_VELOCITY
        * np.sin(2 * np.pi * PERTURBATION_WAVES * j / n)
        * envelope
    )
    u += NOISE_AMPLITUDE * SHEAR_VELOCITY * rng.standard_normal((n, n))
    v += NOISE_AMPLITUDE * SHEAR_VELOCITY * rng.standard_normal((n, n))
    temperature = T_COLD + (T_HOT - T_COLD) * band
    return project(u, v) + (temperature,)


def advect(field, u, v, dt=TIME_STEP):
    """Semi-Lagrangian step: trace each cell back along (u, v), interpolate bilinearly."""
    n_y, n_x = field.shape
    j, i = np.meshgrid(np.arange(n_x), np.arange(n_y))
    x = (j - u * dt) % n_x
    y = (i - v * dt) % n_y
    j0 = np.floor(x).astype(int)
    i0 = np.floor(y).astype(int)
    s1, t1 = x - j0, y - i0
    j0 %= n_x
    i0 %= n_y
    j1, i1 = (j0 + 1) % n_x, (i0 + 1) % n_y
    return (1 - s1) * ((1 - t1) * field[i0, j0] + t1 * field[i1, j0]) + s1 * (
        (1 - t1) * field[i0, j1] + t1 * field[i1, j1]
    )


def diffuse(field, rate, dt=TIME_STEP):
    """Explicit Euler step of the periodic 5-point Laplacian."""
    laplacian = (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4 * field
    )
    return field + rate * dt * laplacian


def project(u, v):
    """Remove the gradient part of (u, v): solve lap(p) = div(u) with FFTs."""
    n_y, n_x = u.shape
    kx = 2 * np.pi * np.fft.fftfreq(n_x)[None, :]
    ky = 2 * np.pi * np.fft.fftfreq(n_y)[:, None]
    k2 = kx**2 + ky**2
    k2[0, 0] = 1.0  # the mean flow has no pressure part
    u_hat, v_hat = np.fft.fft2(u), np.fft.fft2(v)
    k_dot_u = (kx * u_hat + ky * v_hat) / k2
    u_hat -= kx * k_dot_u
    v_hat -= ky * k_dot_u
    return np.real(np.fft.ifft2(u_hat)), np.real(np.fft.ifft2(v_hat))


def update_fields(u, v, temperature):
    """One time step: advect, project, diffuse velocity; advect-diffuse temperature."""
    u_new = advect(u, u, v)
    v_new = advect(v, u, v)
    u_new, v_new = project(u_new, v_new)
    u_new = diffuse(u_new, VISCOSITY)
    v_new = diffuse(v_new, VISCOSITY)
    temperature = diffuse(advect(temperature, u_new, v_new), DIFFUSION_RATE)
    return u_new, v_new, temperature


def temperature_to_rgb(temperature):
    """Map temperature to hue 240 (blue, coldest) ... 0 (red, hottest) at full saturation."""
    t_min, t_max = temperature.min(), temperature.max()
    norm = (temperature - t_min) / (t_max - t_min) if t_max > t_min else 0 * temperature
    h = 240 * (1 - norm) / 60.0
    x = 1 - np.abs(h % 2 - 1)
    sector = np.minimum(np.floor(h).astype(int), 5)
    one, zero = np.ones_like(h), np.zeros_like(h)
    r = np.choose(sector, [one, x, zero, zero, x, one])
    g = np.choose(sector, [x, one, one, x, zero, zero])
    b = np.choose(sector, [zero, zero, x, one, one, x])
    return (255 * np.stack([r, g, b], axis=-1)).astype(np.uint8)


def draw(screen, pygame, temperature):
    rgb = temperature_to_rgb(temperature[::-1])  # row 0 of the image is the top (max y)
    surface = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))
    screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))


def main(argv=None):
    parser = create_parser(__doc__)
    parser.add_argument(
        "--steps",
        type=positive_int,
        default=None,
        help=f"frames to run, each {STEPS_PER_FRAME} solver steps "
        "(default: until the window is closed)",
    )
    args = parser.parse_args(argv)

    if args.no_show:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    import pygame

    u, v, temperature = initialize_fields()

    pygame.init()
    try:
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Kelvin-Helmholtz Instability Simulation")
        frame = 0
        while args.steps is None or frame < args.steps:
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break
            for _ in range(STEPS_PER_FRAME):
                u, v, temperature = update_fields(u, v, temperature)
            draw(screen, pygame, temperature)
            pygame.display.flip()
            if not args.no_show:
                pygame.time.wait(10)  # slow the animation down slightly
            frame += 1

        print(f"t = {frame * STEPS_PER_FRAME * TIME_STEP:g} after {frame} frames")
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            pygame.image.save(
                screen, str(args.output / "kelvin_helmholtz_instability.png")
            )
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
