"""Airplane notes: thin-airfoil theory, panel method, polar, longitudinal modes."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_script(category, name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


airfoil = load_script("algorithms", "airplane_thin_airfoil_and_polar")
modes = load_script("algorithms", "airplane_longitudinal_modes")
classes = load_script("plots", "airplane_stability_classification")
reynolds = load_script("plots", "airplane_reynolds_number_scale")
profile = load_script("plots", "airfoil_profile")
forces = load_script("plots", "airplane_four_forces")


class ThinAirfoilTests(unittest.TestCase):
    def test_zero_lift_angle_of_naca_2412(self):
        self.assertAlmostEqual(np.degrees(airfoil.zero_lift_angle("2412")), -2.077, 2)
        self.assertEqual(airfoil.zero_lift_angle("0012"), 0.0)

    def test_zero_lift_angle_matches_closed_form(self):
        # Independent check of the adaptive quadrature with a fine
        # trapezoidal rule over theta.
        m, p, _ = airfoil.parse_naca4("4412")
        th = np.linspace(0, np.pi, 400001)
        f = airfoil.camber_slope(0.5 * (1 - np.cos(th)), m, p) * (np.cos(th) - 1)
        expected = -np.trapezoid(f, th) / np.pi
        self.assertAlmostEqual(airfoil.zero_lift_angle("4412"), expected, 7)

    def test_lift_slope_is_two_pi(self):
        a1, a2 = np.radians(2.0), np.radians(6.0)
        cl1, _ = airfoil.thin_airfoil_coefficients("2412", a1)
        cl2, _ = airfoil.thin_airfoil_coefficients("2412", a2)
        self.assertAlmostEqual((cl2 - cl1) / (a2 - a1), 2 * np.pi, 10)

    def test_quarter_chord_moment_is_independent_of_alpha(self):
        cms = [
            airfoil.thin_airfoil_coefficients("2412", np.radians(a))[1]
            for a in (0, 5, 10)
        ]
        np.testing.assert_allclose(cms, cms[0], atol=1e-12)
        self.assertAlmostEqual(cms[0], -0.0531, 3)

    def test_loading_integrates_to_lift(self):
        alpha = np.radians(4.0)
        th = np.linspace(1e-6, np.pi - 1e-6, 200001)
        x = 0.5 * (1 - np.cos(th))
        dcp = airfoil.thin_airfoil_loading("2412", alpha, x)
        cl_load = np.trapezoid(dcp * 0.5 * np.sin(th), th)
        cl, _ = airfoil.thin_airfoil_coefficients("2412", alpha)
        self.assertAlmostEqual(cl_load, cl, 3)


class PanelMethodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xs, cls.ys = airfoil.naca4_panels("2412", 160)

    def test_symmetric_airfoil_has_no_lift_at_zero_incidence(self):
        xs, ys = airfoil.naca4_panels("0012", 160)
        res = airfoil.solve_panels(xs, ys, 0.0)
        self.assertAlmostEqual(res["cl"], 0.0, 8)
        self.assertAlmostEqual(res["circulation"], 0.0, 8)

    def test_closed_body_has_zero_net_source(self):
        res = airfoil.solve_panels(self.xs, self.ys, np.radians(4.0))
        self.assertLess(abs(res["source_sum"]), 1e-3)

    def test_pressure_lift_matches_kutta_joukowski(self):
        res = airfoil.solve_panels(self.xs, self.ys, np.radians(4.0))
        self.assertAlmostEqual(res["cl"] / res["cl_kj"], 1.0, delta=0.02)

    def test_panel_method_close_to_thin_airfoil_theory(self):
        alphas = np.radians([-2.0, 0.0, 2.0, 4.0, 6.0])
        cl = [airfoil.solve_panels(self.xs, self.ys, a)["cl"] for a in alphas]
        slope, intercept = np.polyfit(alphas, cl, 1)
        # Thickness raises the slope above 2 pi by roughly 0.77 t/c.
        self.assertGreater(slope, 2 * np.pi)
        self.assertLess(slope, 2 * np.pi * (1 + 0.77 * 0.12) * 1.03)
        alpha_l0 = -intercept / slope
        self.assertAlmostEqual(np.degrees(alpha_l0), -2.08, delta=0.15)
        cm = airfoil.solve_panels(self.xs, self.ys, np.radians(4.0))["cm_quarter"]
        self.assertAlmostEqual(cm, -0.053, delta=0.01)


class FiniteWingAndPolarTests(unittest.TestCase):
    def test_finite_wing_slope_limits(self):
        a = 2 * np.pi
        self.assertAlmostEqual(airfoil.finite_wing_slope(a, 1e9, 1.0), a, 6)
        # Elliptic wing with AR = 2 pi: slope halves.
        self.assertAlmostEqual(airfoil.finite_wing_slope(a, 2.0, 1.0), a / 2, 12)

    def test_induced_drag(self):
        k = airfoil.induced_drag_factor(8.0, 0.8)
        self.assertAlmostEqual(k * 0.5**2, 0.25 / (np.pi * 0.8 * 8), 15)
        self.assertAlmostEqual(k * 0.5**2, 0.0124, 4)

    def test_max_lift_to_drag(self):
        k = airfoil.induced_drag_factor(airfoil.aspect_ratio())
        cl_star, ld = airfoil.max_lift_to_drag(k=k)
        cl = np.linspace(0.05, 2.0, 200001)
        ratio = cl / airfoil.drag_polar(cl, k=k)
        self.assertAlmostEqual(ratio.max(), ld, 6)
        self.assertAlmostEqual(cl[np.argmax(ratio)], cl_star, 3)
        # Induced drag equals parasite drag at C_L*.
        self.assertAlmostEqual(k * cl_star**2, airfoil.CD0, 12)

    def test_minimum_power_speed(self):
        k = airfoil.induced_drag_factor(airfoil.aspect_ratio())
        v = np.linspace(25.0, 60.0, 70001)
        p = airfoil.power_required(v, k=k)
        v_mp = airfoil.level_flight_speed(np.sqrt(3 * airfoil.CD0 / k))
        self.assertAlmostEqual(v[np.argmin(p)], v_mp, 2)
        # Minimum-power speed is 3^(-1/4) times the minimum-drag speed.
        v_md = airfoil.level_flight_speed(np.sqrt(airfoil.CD0 / k))
        self.assertAlmostEqual(v_mp / v_md, 3 ** (-0.25), 12)


class LongitudinalModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = modes.trim_and_derivatives()
        cls.a, cls.b = modes.state_space(cls.d)
        cls.eig = np.linalg.eigvals(cls.a)

    def test_trim_lift_equals_weight(self):
        ac = modes.AIRCRAFT
        lift = self.d["cl"] * self.d["q_dyn"] * ac["wing_area"]
        self.assertAlmostEqual(lift, ac["mass"] * modes.G, 8)
        self.assertAlmostEqual(self.d["Zu"], -2 * modes.G / self.d["u0"], 12)

    def test_all_modes_stable(self):
        self.assertTrue(np.all(self.eig.real < 0))

    def test_short_period_approximation(self):
        sp, _ = modes.split_modes(self.eig)
        wn, zeta, _ = modes.mode_properties(sp)
        wn_a, zeta_a = modes.short_period_approximation(self.d)
        self.assertAlmostEqual(wn / wn_a, 1.0, delta=0.02)
        self.assertAlmostEqual(zeta, zeta_a, delta=0.02)

    def test_phugoid_close_to_lanchester(self):
        _, ph = modes.split_modes(self.eig)
        wn, zeta, _ = modes.mode_properties(ph)
        _, _, lanchester = modes.phugoid_approximation(self.d)
        self.assertAlmostEqual(
            lanchester, np.sqrt(2) * modes.G / modes.AIRCRAFT["speed"]
        )
        self.assertAlmostEqual(wn / lanchester, 1.0, delta=0.2)
        self.assertLess(zeta, 0.2)

    def test_lanchester_exact_without_pitch_damping(self):
        d = dict(self.d, Mq=0.0, Mwdot=0.0)
        a, _ = modes.state_space(d)
        _, ph = modes.split_modes(np.linalg.eigvals(a))
        _, _, lanchester = modes.phugoid_approximation(d)
        self.assertAlmostEqual(abs(ph) / lanchester, 1.0, delta=0.01)

    def test_step_response_reaches_static_trim(self):
        t = np.linspace(0, 600, 12001)
        x = modes.step_response(self.a, self.b, modes.ELEVATOR_STEP, t)
        steady = -np.linalg.solve(self.a, self.b * modes.ELEVATOR_STEP)
        np.testing.assert_allclose(x[-1], steady, atol=1e-3 * np.abs(steady).max())

    def test_critical_pilot_gain_separates_stable_and_unstable_loops(self):
        k_crit, w180 = modes.critical_pilot_gain(self.a, self.b)
        g = modes.pitch_frequency_response(self.a, self.b, w180)[0]
        loop = -k_crit * g * np.exp(-1j * w180 * modes.PILOT_DELAY)
        self.assertAlmostEqual(loop.real, -1.0, 6)
        self.assertAlmostEqual(loop.imag, 0.0, 6)
        t = np.linspace(0, 30, 6001)

        def late_amplitude(factor):
            x, _ = modes.simulate_pilot_loop(self.a, self.b, factor * k_crit, t)
            theta = x[:, 3]
            return np.ptp(theta[-1000:]), np.ptp(theta[1000:2000])

        late, early = late_amplitude(0.8)
        self.assertLess(late, early)
        late, early = late_amplitude(1.2)
        self.assertGreater(late, early)


class StabilityClassificationTests(unittest.TestCase):
    def test_classification(self):
        expected = [
            ("stable", "stable", False),
            ("stable", "stable", True),
            ("stable", "neutral", True),
            ("stable", "unstable", True),
            ("unstable", "unstable", False),
        ]
        got = [classes.classify(c, k) for _, c, k in classes.CASES]
        self.assertEqual(got, expected)

    def test_free_response_matches_closed_form(self):
        t = np.linspace(0, 10, 101)
        c, k = 0.5, 4.0
        wn, zeta = 2.0, 0.125
        wd = wn * np.sqrt(1 - zeta**2)
        exact = np.exp(-zeta * wn * t) * (
            np.cos(wd * t) + zeta * wn / wd * np.sin(wd * t)
        )
        np.testing.assert_allclose(classes.free_response(c, k, t), exact, atol=1e-10)


class ReynoldsAndProfileTests(unittest.TestCase):
    def test_reynolds_number(self):
        # Exercise of the note: airliner at 11 km, 230 m/s, 5 m chord.
        re = reynolds.reynolds(230.0, 5.0, reynolds.NU_CRUISE)
        self.assertAlmostEqual(re / 2.94e7, 1.0, delta=0.01)

    def test_transitional_skin_friction_is_continuous(self):
        rc = reynolds.RE_CRIT_PLATE
        self.assertAlmostEqual(
            float(reynolds.cf_transitional(rc * (1 + 1e-9))),
            float(reynolds.cf_laminar(rc)),
            9,
        )
        self.assertAlmostEqual(
            float(reynolds.cf_transitional(1e5)), float(reynolds.cf_laminar(1e5))
        )

    def test_naca_thickness(self):
        x, tmax = profile.max_thickness_location(0.12)
        self.assertAlmostEqual(tmax, 0.12, 3)
        self.assertAlmostEqual(x, 0.30, 2)
        self.assertAlmostEqual(profile.leading_edge_radius(0.12), 0.01587, 5)


class ClimbForceTests(unittest.TestCase):
    def test_equilibrium_along_and_normal_to_the_path(self):
        f = forces.climb_forces(40.0, 6.0)
        g = f["gamma"]
        self.assertAlmostEqual(f["T"] - f["D"] - f["W"] * np.sin(g), 0.0, 8)
        self.assertAlmostEqual(f["L"] - f["W"] * np.cos(g), 0.0, 8)
        self.assertLess(f["L"], f["W"])
        self.assertAlmostEqual(f["rate_of_climb"], f["excess_power"] / f["W"], 10)


if __name__ == "__main__":
    unittest.main()
