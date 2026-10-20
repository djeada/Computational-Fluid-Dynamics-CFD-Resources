"""Fluid loading: dispersion relation, Morison force, wave spectra, VIV, FSI coupling."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


morison = load_example("algorithms", "fluid_loading_morison_wave_force")
spectra = load_example("plots", "fluid_loading_wave_spectra")
viv = load_example("algorithms", "fluid_loading_viv_wake_oscillator")
wind = load_example("plots", "fluid_loading_wind_profile")
fsi = load_example("algorithms", "fluid_loading_partitioned_fsi")
surface = load_example("algorithms", "fluid_loading_surface_force_integration")


class DispersionRelationTests(unittest.TestCase):
    def test_root_satisfies_relation(self):
        for period, depth in ((4.0, 5.0), (10.0, 20.0), (15.0, 100.0)):
            omega = 2 * np.pi / period
            k = morison.wave_number(omega, depth)
            self.assertAlmostEqual(
                morison.G * k * np.tanh(k * depth) / omega**2, 1.0, places=12
            )

    def test_deep_water_limit(self):
        omega = 2 * np.pi / 8.0
        k = morison.wave_number(omega, 1000.0)
        self.assertAlmostEqual(k, omega**2 / morison.G, places=12)

    def test_shallow_water_limit(self):
        omega = 2 * np.pi / 60.0
        depth = 1.0
        k = morison.wave_number(omega, depth)
        # omega = k sqrt(g h) (1 - (kh)^2 / 6 + ...), here kh = 0.033
        np.testing.assert_allclose(k, omega / np.sqrt(morison.G * depth), rtol=1e-3)


class MorisonTests(unittest.TestCase):
    def test_pure_inertia_peak_matches_closed_form(self):
        phase = np.linspace(-np.pi, np.pi, 2001)
        drag, inertia, total, _ = morison.pile_force(phase, cd=0.0)
        self.assertTrue(np.all(drag == 0.0))
        omega = 2 * np.pi / morison.WAVE_PERIOD
        k = morison.wave_number(omega, morison.WATER_DEPTH)
        expected = (
            morison.RHO_SEA
            * morison.INERTIA_COEFF
            * np.pi
            * morison.PILE_DIAMETER**2
            / 4
            * 0.5
            * morison.WAVE_HEIGHT
            * omega**2
            / k
        )
        np.testing.assert_allclose(total.max(), expected, rtol=1e-10)
        # Peak inertia occurs a quarter period before the crest.
        self.assertAlmostEqual(phase[np.argmax(total)], -np.pi / 2, places=2)

    def test_quadrature_matches_drag_amplitude(self):
        drag, _, _, _ = morison.pile_force(np.array([0.0]))
        f_d, _ = morison.force_amplitudes()
        np.testing.assert_allclose(drag[0], f_d, rtol=1e-10)

    def test_peak_formula_against_brute_force(self):
        phi = np.linspace(-np.pi, np.pi, 200001)
        for f_d, f_i in ((1.0, 3.0), (1.0, 2.0), (1.0, 1.0), (2.0, 0.5)):
            brute = np.max(f_d * np.abs(np.cos(phi)) * np.cos(phi) - f_i * np.sin(phi))
            np.testing.assert_allclose(morison.peak_force(f_d, f_i), brute, rtol=1e-8)

    def test_drag_equals_half_inertia_at_kc_pi2_cm_over_2cd(self):
        kc = np.pi**2 * morison.INERTIA_COEFF / (2 * morison.DRAG_COEFF)
        self.assertAlmostEqual(morison.drag_to_inertia_ratio(kc), 0.5, places=12)


class WaveSpectrumTests(unittest.TestCase):
    def test_zeroth_moment_gives_significant_height(self):
        omega = np.linspace(1e-3, spectra.OMEGA_MAX, spectra.N_OMEGA)
        for gamma in (1.0, 3.3, 7.0):
            s, _ = spectra.jonswap(omega, gamma)
            m0 = spectra.spectral_moment(omega, s, 0)
            np.testing.assert_allclose(4 * np.sqrt(m0), spectra.HS, rtol=1e-4)

    def test_pierson_moskowitz_moments(self):
        omega = np.linspace(1e-3, spectra.OMEGA_MAX, spectra.N_OMEGA)
        s = spectra.pierson_moskowitz(omega)
        m0 = spectra.spectral_moment(omega, s, 0)
        m2 = spectra.spectral_moment(omega, s, 2)
        np.testing.assert_allclose(m0, spectra.HS**2 / 16, rtol=1e-4)
        # T_z = T_p (1.25 pi)^(-1/4) for the PM spectrum.
        tz = 2 * np.pi * np.sqrt(m0 / m2)
        np.testing.assert_allclose(tz, spectra.TP * (1.25 * np.pi) ** -0.25, rtol=2e-3)


class WindProfileTests(unittest.TestCase):
    def test_log_law_reproduces_reference_speed(self):
        u_star = wind.friction_velocity(25.0, 10.0, 0.03)
        self.assertAlmostEqual(float(wind.log_law(10.0, u_star, 0.03)), 25.0, places=12)

    def test_power_exponent_grows_with_roughness(self):
        alphas = [wind.fit_power_law(1.0, z0)[0] for z0 in wind.TERRAINS.values()]
        self.assertTrue(np.all(np.diff(alphas) > 0))


class WakeOscillatorTests(unittest.TestCase):
    def test_uncoupled_wake_reaches_van_der_pol_limit_cycle(self):
        _, _, q = viv.simulate(np.array([5.0]), 20.0, 0.01, coupling=0.0)
        self.assertAlmostEqual(np.abs(q).max(), 2.0, delta=0.02)

    def test_lock_in_and_strouhal_branches(self):
        ur = np.array([5.5, 12.0])
        _, f_ratio, _ = viv.response(ur, 20.0, 0.002)
        # Inside lock-in the response follows f_n, not St U_r = 1.1.
        self.assertLess(abs(f_ratio[0] - 1.0), 0.02)
        # Far above lock-in it returns close to the Strouhal frequency.
        np.testing.assert_allclose(f_ratio[1], viv.STROUHAL * ur[1], rtol=0.05)

    def test_amplitude_decreases_with_mass_damping(self):
        amp, _, _ = viv.response(np.full(3, 5.5), 20.0, np.array([0.001, 0.01, 0.1]))
        self.assertTrue(np.all(np.diff(amp) < 0))


class PartitionedCouplingTests(unittest.TestCase):
    def test_explicit_threshold_is_added_mass_equal_to_structural_mass(self):
        for omega_dt in (1e-3, 0.1, 1.0, 3.0):
            lo, hi = 0.5, 2.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if fsi.explicit_amplification(mid, omega_dt) > 1.0 + 1e-12:
                    hi = mid
                else:
                    lo = mid
            self.assertAlmostEqual(0.5 * (lo + hi), 1.0, places=6)

    def test_membrane_explicit_coupling_bounded_below_and_grows_above(self):
        per_rho = fsi.modal_added_mass(1, 1.0)[0]
        below, _, _ = fsi.run("explicit", rho_f=0.9 * fsi.STRUCT_MASS / per_rho)
        above, _, _ = fsi.run("explicit", rho_f=1.1 * fsi.STRUCT_MASS / per_rho)
        self.assertLess(below.max(), 2 * below[:100].max())
        self.assertGreater(above.max(), 100 * above[:100].max())

    def test_aitken_coupling_matches_monolithic_solution(self):
        _, w, iterations = fsi.run("aitken", n_steps=100)
        reference = fsi.monolithic(n_steps=100)
        error = np.abs(w - reference).max() / np.abs(reference).max()
        self.assertLess(error, 1e-6)
        self.assertLess(iterations.max(), fsi.MAX_ITER)

    def test_unrelaxed_iteration_factor_is_largest_modal_ratio(self):
        membrane = fsi.Membrane()
        fluid = fsi.FluidLayer()
        iteration = -np.linalg.solve(
            fsi.NewmarkStructure(membrane).effective, fluid.added_mass
        )
        radius = np.max(np.abs(np.linalg.eigvals(iteration)))
        np.testing.assert_allclose(
            radius, fsi.iteration_factor(membrane, fluid), rtol=1e-8
        )

    def test_wet_frequencies_follow_modal_added_mass(self):
        numeric, analytic = fsi.wet_dry_ratio(fsi.RHO_WATER)
        np.testing.assert_allclose(numeric, analytic, rtol=1e-8)

    def test_modal_added_mass_deep_layer_limit(self):
        # Long-wave check: m_a = rho coth(kH) / k tends to rho / k for kH >> 1.
        k = np.pi / fsi.LENGTH
        np.testing.assert_allclose(
            fsi.modal_added_mass(1, 1000.0, depth=50.0)[0], 1000.0 / k, rtol=1e-12
        )


class SurfaceIntegrationTests(unittest.TestCase):
    def test_buoyancy_exact_for_polygon_area(self):
        for n in (8, 64):
            force, _ = surface.loads_for(n, "hydrostatic")
            area = 0.5 * n * surface.RADIUS**2 * np.sin(2 * np.pi / n)
            np.testing.assert_allclose(
                force[1], surface.RHO * surface.G * area, rtol=1e-12
            )
            self.assertAlmostEqual(force[0], 0.0, places=8)

    def test_potential_flow_has_no_drag_and_kutta_joukowski_lift(self):
        gamma = (
            -surface.CIRCULATION_FRACTION * 2 * np.pi * surface.RADIUS * surface.U_INF
        )
        errors = []
        for n in (64, 128):
            force, moment = surface.loads_for(n, "circulation")
            self.assertAlmostEqual(force[0], 0.0, places=8)
            self.assertAlmostEqual(moment, 0.0, places=8)
            errors.append(abs(force[1] + surface.RHO * surface.U_INF * gamma))
        self.assertAlmostEqual(np.log2(errors[0] / errors[1]), 2.0, delta=0.05)

    def test_uniform_shear_gives_pure_moment(self):
        n, tau = 64, 3.0
        _, c, normals, lengths = surface.cylinder_faces(n)
        tangent = np.column_stack((-normals[:, 1], normals[:, 0]))
        force, moment = surface.integrate_loads(
            c, normals, lengths, np.zeros(n), shear=tau * tangent
        )
        np.testing.assert_allclose(force, 0.0, atol=1e-10)
        apothem = surface.RADIUS * np.cos(np.pi / n)
        np.testing.assert_allclose(moment, tau * lengths.sum() * apothem, rtol=1e-12)


if __name__ == "__main__":
    unittest.main()
