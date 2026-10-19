"""Check the acoustic wave solver of the moving-source (Mach cone) example.

A stationary impulsive source must give a circular front that grows at the
speed of sound, the undamped scheme must conserve its discrete energy, the
sponge must absorb outgoing waves, and a supersonic source must produce a
Mach cone of half-angle arcsin(1/M): exactly, with the exact amplitude, for a
steady source, and within a degree for the oscillating source of the demo.
"""

import importlib.util
import math
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / "simulations" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cone = load_example("mach_cone_moving_source")
PULSE_TIME, PULSE_WIDTH = (
    0.5,
    0.15,
)  # centre and width of the impulsive source [periods]


class PulseSimulation(cone.MachConeSimulation):
    """The same solver with a short Gaussian pulse instead of the tone."""

    def source_signal(self, t):
        return self.amplitude * math.exp(-(((t - PULSE_TIME) / PULSE_WIDTH) ** 2))


class SteadySimulation(cone.MachConeSimulation):
    """The same solver with a source of constant strength after the ramp."""

    def source_signal(self, t):
        return self.amplitude * (1.0 - math.exp(-((t / cone.RAMP_TIME) ** 2)))


def front_radii(simulation, directions=24):
    """Outermost radius where |p| reaches half its maximum, along rays from the source."""
    xs, ys = simulation.source_position()
    radii = np.arange(0.0, 6.0, 0.002)
    result = []
    for angle in np.arange(directions) * 2 * np.pi / directions:
        x, y = xs + radii * np.cos(angle), ys + radii * np.sin(angle)
        col = (x - simulation.x[0]) / simulation.h
        row = (y - simulation.y[0]) / simulation.h
        c0, r0 = np.floor(col).astype(int), np.floor(row).astype(int)
        fc, fr = col - c0, row - r0
        p = simulation.p
        profile = np.abs(
            (1 - fr) * ((1 - fc) * p[r0, c0] + fc * p[r0, c0 + 1])
            + fr * ((1 - fc) * p[r0 + 1, c0] + fc * p[r0 + 1, c0 + 1])
        )  # bilinear interpolation along the ray
        result.append(radii[np.nonzero(profile >= 0.5 * profile.max())[0].max()])
    return np.array(result)


def wedge_half_angle(simulation, level, distances):
    """Half-angle of the region where p exceeds level / 2, behind the source."""
    xs, ys = simulation.source_position()
    behind, half_width = [], []
    for d in distances:
        row = np.argmin(np.abs(simulation.y - (ys - d)))
        right = simulation.p[row, simulation.x >= xs]
        k = np.nonzero(right >= 0.5 * level)[0].max()
        crossing = k + (right[k] - 0.5 * level) / (right[k] - right[k + 1])
        behind.append(ys - simulation.y[row])
        half_width.append(crossing * simulation.h)
    return math.degrees(math.atan(np.polyfit(behind, half_width, 1)[0]))


class KinematicsTests(unittest.TestCase):
    def test_distance_is_the_integral_of_the_speed(self):
        t = np.linspace(0.0, cone.END_TIME, 20001)
        speed = [cone.mach_number(s) * cone.SOUND_SPEED for s in t]
        expected = np.concatenate(
            ([0], np.cumsum(0.5 * (speed[1:] + np.array(speed[:-1])) * np.diff(t)))
        )
        for k in (0, 5000, 13913, 20000):
            self.assertAlmostEqual(cone.travelled(t[k]), expected[k], places=8)
        self.assertEqual(cone.mach_number(cone.END_TIME), cone.MACH_MAX)


class AcousticSolverTests(unittest.TestCase):
    def test_impulsive_source_gives_circle_of_radius_ct(self):
        simulation = PulseSimulation(
            width=13, height=13, cells_per_wavelength=20, sponge_width=2,
            mach_max=0.0, source_start=6.5,
        )  # fmt: skip
        simulation.advance(round(2.5 / simulation.dt))
        first, t1 = front_radii(simulation), simulation.time
        simulation.advance(round(2.0 / simulation.dt))
        second, t2 = front_radii(simulation), simulation.time
        for radii in (first, second):
            self.assertLess(np.ptp(radii), 0.03)  # round to within a cell
        speed = (second.mean() - first.mean()) / (t2 - t1)
        self.assertAlmostEqual(speed, cone.SOUND_SPEED, delta=0.005)
        # The half-maximum front leads c (t - t_pulse) by about a pulse width.
        offset = second.mean() - cone.SOUND_SPEED * (t2 - PULSE_TIME)
        self.assertLess(abs(offset), PULSE_WIDTH)

    def test_energy_is_conserved_without_source_and_sponge(self):
        simulation = cone.MachConeSimulation(
            width=6, height=6, cells_per_wavelength=10, sponge_width=0, amplitude=0.0
        )
        x, y = np.meshgrid(simulation.x, simulation.y)
        bump = np.exp(-((x - 2.5) ** 2 + (y - 3.5) ** 2) / 0.3)
        simulation.p = bump.copy()
        simulation.p_previous = bump.copy()  # starts (nearly) at rest
        initial = simulation.energy()
        self.assertGreater(initial, 0.0)
        for _ in range(10):
            simulation.advance(60)  # 600 steps: many reflections off the walls
            self.assertAlmostEqual(simulation.energy() / initial, 1.0, delta=1e-12)
        self.assertGreater(np.abs(simulation.p - bump).max(), 0.1)

    def test_sponge_absorbs_outgoing_waves(self):
        simulation = cone.MachConeSimulation(
            width=6, height=6, cells_per_wavelength=10, amplitude=0.0
        )
        x, y = np.meshgrid(simulation.x, simulation.y)
        bump = np.exp(-((x - 3) ** 2 + (y - 3) ** 2) / 0.3)
        simulation.p, simulation.p_previous = bump.copy(), bump.copy()
        initial = simulation.energy()
        simulation.advance(round(20.0 / simulation.dt))
        self.assertLess(simulation.energy(), 1e-3 * initial)
        rows, cols = simulation.visible
        self.assertLess(np.abs(simulation.p[rows, cols]).max(), 1e-2)


class MachConeTests(unittest.TestCase):
    def test_steady_supersonic_source_gives_exact_mach_wedge(self):
        # In 2D a steady source of strength q moving at Mach M > 1 gives
        # p = q / (2 c^2 sqrt(M^2 - 1)) inside the wedge |x| < d tan(mu)
        # behind it, with sin(mu) = 1/M, and p = 0 outside.
        q = cone.SOURCE_AMPLITUDE * 2.0 * math.pi * cone.SOURCE_RADIUS**2
        for mach in (1.5, 2.0, 3.0):
            with self.subTest(mach=mach):
                simulation = SteadySimulation(
                    width=16, height=14, cells_per_wavelength=10, sponge_width=2,
                    mach_max=mach, acceleration_time=0.0, source_start=1.0,
                )  # fmt: skip
                simulation.advance(round(12.0 / mach / simulation.dt))
                level = q / (2.0 * cone.SOUND_SPEED**2 * math.sqrt(mach**2 - 1.0))
                # Close behind the source the start-up transient has not
                # arrived yet (at M = 1.5 it reaches 3 wavelengths back).
                distances = np.linspace(1.0, 2.5, 13)
                angle = wedge_half_angle(simulation, level, distances)
                self.assertAlmostEqual(
                    angle, math.degrees(math.asin(1 / mach)), delta=0.4
                )
                xs, ys = simulation.source_position()
                axis = np.argmin(np.abs(simulation.x - xs))
                inside = (simulation.y < ys - 1.5) & (simulation.y > ys - 2.5)
                np.testing.assert_allclose(
                    simulation.p[inside, axis], level, rtol=0.005
                )
                ahead = simulation.y > ys + 0.6
                self.assertLess(np.abs(simulation.p[ahead]).max(), 1e-4 * level)

    def test_oscillating_source_cone_half_angle(self):
        # Arrival times at receivers on a line across the path: the cone
        # reaches lateral distance r when the source is r / tan(mu) further
        # on, so dt/dr = 1 / (V tan(mu)).
        mach = 2.0
        simulation = cone.MachConeSimulation(
            width=16, height=16, cells_per_wavelength=10, sponge_width=2,
            mach_max=mach, acceleration_time=0.0, source_start=1.0,
        )  # fmt: skip
        row = np.argmin(np.abs(simulation.y - 7.0))
        xs = 0.5 * simulation.width
        cols = np.nonzero((simulation.x > xs + 0.5) & (simulation.x < xs + 5.0))[0]
        n_steps = round(7.0 / simulation.dt)
        history = np.empty((n_steps, len(cols)))
        for k in range(n_steps):
            simulation.advance(1)
            history[k] = simulation.p[row, cols]
        loudest = np.abs(history).max(axis=0)
        arrival = (
            np.argmax(np.abs(history) >= 0.1 * loudest, axis=0) + 1
        ) * simulation.dt
        slope = np.polyfit(simulation.x[cols] - xs, arrival, 1)[0]
        angle = math.degrees(math.atan(1.0 / (mach * cone.SOUND_SPEED * slope)))
        self.assertAlmostEqual(angle, 30.0, delta=1.0)


if __name__ == "__main__":
    unittest.main()
