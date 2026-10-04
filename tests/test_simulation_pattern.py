"""Every simulation follows the shared Simulation / View / Animation pattern."""

import importlib.util
import sys
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from _animation import REEL_BANDS, REEL_SIZE, Animation, Simulation, View  # noqa: E402

FOLDERS = sorted(
    path.parent for path in (ROOT / "scripts/simulations").glob("*/main.py")
)

# Small, fast instances: constructor keyword arguments, or a factory taking the
# loaded module when the constructor needs more than keywords.
SMALL = {
    "1d_heat_and_wave_equations": {"nx": 21, "total_time": 1},
    "2d_wave_simulation": {"nx": 13, "ny": 11},
    "backward_facing_step_simple": lambda m: m.BackwardStepSimulation(
        m.Params(nx=24, ny=8)
    ),
    "bak_tang_wiesenfeld_sandpile_model_3d": {"size": 6},
    "decaying_2d_turbulence": {"n": 16},
    "double_gyre_chaotic_mixing": {
        "tracers": (40, 20),
        "image_shape": (20, 40),
        "ftle_shape": (8, 16),
    },
    "eulerian_cylinder_flow": {"resolution": 20},
    "gray_scott_reaction_diffusion": {"n": 16},
    "ising_model": {"n_rows": 16, "n_cols": 16},
    "kelvin_helmholtz_instability": {"n": 32},
    "laplace_equation_maze_solver": {"size": 11},
    "lattice_boltzmann_cylinder_flow": {"dimensions": (36, 24)},
    "lid_driven_cavity": {"n_points": 17},
    "lorenz_attractor": {"n_trajectories": 4, "trail_steps": 5, "ghost_time": 1.0},
    "mach_cone_moving_source": {
        "width": 3,
        "height": 4,
        "cells_per_wavelength": 8,
        "sponge_width": 1,
    },
    "point_vortex_leapfrogging": {"smoke_per_vortex": 50},
    "rayleigh_benard_convection": {"n": 16},
    "rayleigh_taylor_instability": {"nx": 16, "nz": 32},
    "schroedinger_equation": {"n": 16},
    "shallow_water_ripples": {"n": 24},
    "simplified_real_time_fluid_dynamics_simulator": {"width": 20, "height": 15},
    "sph_dam_break": {"particles_across": 4},
    "steady_and_unsteady_pathlines_with_vortex_shedding": {"num_particles": 4},
    "supersonic_forward_facing_step": {"cells_per_unit": 10},
}


def small_simulation(folder, module, simulation_class):
    small = SMALL.get(folder.name, {})
    return small(module) if callable(small) else simulation_class(**small)


def load(folder):
    name = f"pattern_{folder.name}"
    spec = importlib.util.spec_from_file_location(name, folder / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def defined_subclasses(module, base):
    return [
        value
        for value in vars(module).values()
        if isinstance(value, type)
        and issubclass(value, base)
        and value.__module__ == module.__name__
    ]


class SimulationPatternTests(unittest.TestCase):
    def test_folders_define_state_view_and_animation(self):
        self.assertEqual(len(FOLDERS), 25)
        for folder in FOLDERS:
            with self.subTest(folder.name):
                module = load(folder)
                source = (folder / "main.py").read_text(encoding="utf-8")
                self.assertEqual(len(defined_subclasses(module, Simulation)), 1)
                self.assertEqual(len(defined_subclasses(module, View)), 1)
                self.assertIsInstance(module.ANIMATION, Animation)
                self.assertTrue((folder / module.ANIMATION.filename).is_file())
                self.assertIn("ANIMATION.parser(__doc__)", source)
                self.assertIn("ANIMATION.run(", source)
                for forbidden in ("pygame", "matplotlib.pyplot", "FuncAnimation"):
                    self.assertNotIn(forbidden, source)
                readme = (folder / "README.md").read_text(encoding="utf-8")
                self.assertIn("--reel", readme)

    def test_views_draw_without_advancing_in_both_layouts(self):
        for folder in FOLDERS:
            with self.subTest(folder.name):
                module = load(folder)
                (simulation_class,) = defined_subclasses(module, Simulation)
                (view_class,) = defined_subclasses(module, View)
                simulation = small_simulation(folder, module, simulation_class)
                width, height = REEL_SIZE[0], REEL_BANDS[1]
                for portrait, size in (
                    (False, (8, 6)),
                    (True, (width / 100, height / 100)),
                ):
                    figure = Animation.offscreen_figure(size)
                    view = view_class(simulation, figure, portrait=portrait)
                    view.draw()
                    view.draw()
                    figure.canvas.draw()
                    self.assertEqual(simulation.steps, 0)
                    status = view.status()
                    self.assertTrue(status and "\n" not in status, status)
                simulation.advance(1)
                self.assertEqual(simulation.steps, 1)
                view.draw()
                figure.canvas.draw()


if __name__ == "__main__":
    unittest.main()
