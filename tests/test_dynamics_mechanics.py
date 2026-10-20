"""Dynamics scripts: integrators, modal analysis and kinematics against closed forms."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_example(category, name):
    spec = importlib.util.spec_from_file_location(
        f"dynamics_{name}", ROOT / "scripts" / category / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sdof = load_example("algorithms", "dynamics_sdof_response")
two_dof = load_example("algorithms", "dynamics_two_dof_modes")
pendulum = load_example("algorithms", "dynamics_double_pendulum_lagrange")
projectile = load_example("algorithms", "dynamics_projectile_drag")
crank = load_example("algorithms", "dynamics_slider_crank_kinematics")
euler = load_example("algorithms", "dynamics_torque_free_rigid_body")
rocket = load_example("algorithms", "dynamics_variable_mass_rocket")
paths = load_example("plots", "dynamics_path_coordinates")


class SdofTests(unittest.TestCase):
    def test_newmark_matches_analytic_free_response(self):
        omega_n = np.sqrt(sdof.STIFFNESS / sdof.MASS)
        for zeta in (0.0, 0.1, 1.0, 2.0):
            with self.subTest(zeta=zeta):
                dt = 2 * np.pi / omega_n / 400
                t = np.arange(0.0, 3.0, dt)
                c = sdof.damping_coefficient(zeta)
                x, _, _ = sdof.newmark(
                    sdof.MASS, c, sdof.STIFFNESS, np.zeros_like(t), dt, 0.01, 0.0
                )
                exact = sdof.free_response(t, zeta, omega_n, 0.01, 0.0)
                self.assertLess(np.max(np.abs(x - exact)) / 0.01, 2e-3)

    def test_newmark_is_second_order(self):
        omega_n = np.sqrt(sdof.STIFFNESS / sdof.MASS)
        errors = []
        for steps in (50, 100, 200):
            dt = 2 * np.pi / omega_n / steps
            t = np.arange(0.0, 2.0 + 0.5 * dt, dt)
            c = sdof.damping_coefficient(0.1)
            x, _, _ = sdof.newmark(
                sdof.MASS, c, sdof.STIFFNESS, np.zeros_like(t), dt, 0.01, 0.0
            )
            errors.append(
                np.max(np.abs(x - sdof.free_response(t, 0.1, omega_n, 0.01, 0.0)))
            )
        orders = np.log2(np.array(errors[:-1]) / np.array(errors[1:]))
        np.testing.assert_allclose(orders, 2.0, atol=0.1)

    def test_undamped_newmark_conserves_energy(self):
        omega_n = np.sqrt(sdof.STIFFNESS / sdof.MASS)
        dt = 2 * np.pi / omega_n / 20
        t = np.arange(0.0, 50.0, dt)
        x, v, _ = sdof.newmark(
            sdof.MASS, 0.0, sdof.STIFFNESS, np.zeros_like(t), dt, 0.01, 0.0
        )
        energy = 0.5 * sdof.MASS * v**2 + 0.5 * sdof.STIFFNESS * x**2
        np.testing.assert_allclose(energy, energy[0], rtol=1e-10)

    def test_forced_steady_state_matches_magnification_and_phase(self):
        zeta, r = 0.2, 1.3
        omega_n = np.sqrt(sdof.STIFFNESS / sdof.MASS)
        omega = r * omega_n
        dt = 2 * np.pi / omega / 400
        t = np.arange(0.0, 40.0, dt)
        force = sdof.STIFFNESS * np.sin(omega * t)  # F0 / k = 1 m
        c = sdof.damping_coefficient(zeta)
        x, _, _ = sdof.newmark(sdof.MASS, c, sdof.STIFFNESS, force, dt, 0.0, 0.0)
        tail = t > 30.0
        # Fit x = A sin(w t) + B cos(w t) over the steady part.
        basis = np.column_stack([np.sin(omega * t[tail]), np.cos(omega * t[tail])])
        a, b = np.linalg.lstsq(basis, x[tail], rcond=None)[0]
        np.testing.assert_allclose(
            np.hypot(a, b), sdof.magnification(r, zeta), rtol=2e-4
        )
        self.assertAlmostEqual(np.arctan2(-b, a), sdof.phase_lag(r, zeta), places=3)

    def test_frf_peak_location(self):
        r = np.linspace(0.5, 1.2, 200001)
        for zeta in (0.05, 0.1, 0.2, 0.5):
            with self.subTest(zeta=zeta):
                peak = r[np.argmax(sdof.magnification(r, zeta))]
                self.assertAlmostEqual(peak, np.sqrt(1 - 2 * zeta**2), places=4)
                self.assertAlmostEqual(
                    sdof.magnification(1.0, zeta), 1 / (2 * zeta), places=12
                )

    def test_transmissibility_is_one_at_root_two(self):
        for zeta in (0.0, 0.1, 0.5, 1.0):
            self.assertAlmostEqual(sdof.transmissibility(np.sqrt(2.0), zeta), 1.0)


class TwoDofTests(unittest.TestCase):
    def test_eigenfrequencies_match_closed_form_and_modes_are_orthogonal(self):
        for k2 in (5000.0, 7895.0, 20000.0):
            with self.subTest(k2=k2):
                mass, stiffness, _ = two_dof.matrices(
                    two_dof.M1, two_dof.M2, two_dof.K1, k2
                )
                omega, modes = two_dof.normal_modes(mass, stiffness)
                exact = two_dof.closed_form_frequencies(
                    two_dof.M1, two_dof.M2, two_dof.K1, k2
                )
                np.testing.assert_allclose(omega, exact, rtol=1e-12)
                np.testing.assert_allclose(
                    modes.T @ mass @ modes, np.eye(2), atol=1e-12
                )
                np.testing.assert_allclose(
                    modes.T @ stiffness @ modes,
                    np.diag(omega**2),
                    rtol=1e-10,
                    atol=1e-8,
                )

    def test_tuned_absorber_frequencies_and_mode_ratios(self):
        # mu = 0.05 and equal tuning give w^2/w1^2 = 1 + mu/2 -/+ sqrt(mu + mu^2/4).
        mu = two_dof.MASS_RATIO
        k2 = two_dof.M2 * two_dof.K1 / two_dof.M1
        mass, stiffness, _ = two_dof.matrices(two_dof.M1, two_dof.M2, two_dof.K1, k2)
        omega, modes = two_dof.normal_modes(mass, stiffness)
        ratio_sq = 1 + mu / 2 + np.array([-1, 1]) * np.sqrt(mu + mu**2 / 4)
        np.testing.assert_allclose(omega**2 / (two_dof.K1 / two_dof.M1), ratio_sq)
        np.testing.assert_allclose(modes[1] / modes[0], [5.0, -4.0], rtol=1e-10)

    def test_undamped_absorber_gives_antiresonance(self):
        k2 = two_dof.M2 * two_dof.K1 / two_dof.M1
        m, k, c = two_dof.matrices(
            two_dof.M1, two_dof.M2, two_dof.K1, k2, two_dof.C1, 0.0
        )
        w_a = np.sqrt(k2 / two_dof.M2)
        x = two_dof.receptance(np.array([w_a]), m, k, c, np.array([1.0, 0.0]))
        self.assertLess(abs(x[0, 0]), 1e-15)
        # The absorber then carries the force: k2 X2 = -F0.
        self.assertAlmostEqual((k2 * x[0, 1]).real, -1.0, places=10)


class DoublePendulumTests(unittest.TestCase):
    def test_linearized_frequencies_closed_form(self):
        omegas, modes = pendulum.linear_modes()
        g = pendulum.GRAVITY
        np.testing.assert_allclose(
            omegas**2, g * np.array([2 - np.sqrt(2), 2 + np.sqrt(2)]), rtol=1e-12
        )
        np.testing.assert_allclose(modes[1] / modes[0], [np.sqrt(2), -np.sqrt(2)])

    def test_small_angle_frequencies_match_linearization(self):
        omegas, _, measured, _ = pendulum.small_amplitude_study()
        np.testing.assert_allclose(measured, omegas, rtol=1e-3)

    def test_energy_drift_is_small(self):
        _, y = pendulum.integrate(pendulum.LARGE_START, pendulum.LARGE_DURATION)
        self.assertLess(np.max(np.abs(pendulum.energy_drift(y))), 1e-7)

    def test_rest_state_and_mirror_symmetry(self):
        # The hanging state is an equilibrium, and mirroring the state mirrors
        # the accelerations.
        a1, a2 = pendulum.accelerations(0.0, 0.0, 0.0, 0.0)
        self.assertEqual((a1, a2), (0.0, 0.0))
        b1, b2 = pendulum.accelerations(0.1, -0.2, 0.3, 0.4)
        c1, c2 = pendulum.accelerations(-0.1, 0.2, -0.3, -0.4)
        self.assertAlmostEqual(b1, -c1)
        self.assertAlmostEqual(b2, -c2)


class ProjectileTests(unittest.TestCase):
    def test_no_drag_range_matches_formula(self):
        for angle in (20.0, 45.0, 70.0):
            self.assertAlmostEqual(
                projectile.flight_range(angle, k=0.0),
                projectile.vacuum_range(angle),
                places=6,
            )

    def test_drop_approaches_terminal_speed(self):
        from scipy.integrate import solve_ivp

        k = projectile.drag_constant()
        t = np.linspace(0.0, 15.0, 31)
        sol = solve_ivp(
            projectile.rhs,
            (0.0, 15.0),
            [0, 0, 0, 0, 0],
            args=(k,),
            t_eval=t,
            rtol=1e-10,
            atol=1e-12,
        )
        np.testing.assert_allclose(
            -sol.y[3], projectile.fall_speed(t), rtol=1e-7, atol=1e-9
        )

    def test_work_energy_balance(self):
        _, s, _ = projectile.fly(45.0)
        kinetic, potential, work = projectile.energy_budget(s)
        total = kinetic + potential + work
        np.testing.assert_allclose(total, total[0], rtol=1e-7)

    def test_optimum_angle_below_45_with_drag(self):
        angle, _ = projectile.optimum_angle()
        self.assertTrue(38.0 < angle < 45.0)


class SliderCrankTests(unittest.TestCase):
    def test_relative_motion_matches_finite_differences(self):
        theta, v_fd, a_fd = crank.finite_difference_check(n=2881)
        k = crank.kinematics(theta)
        np.testing.assert_allclose(k["v_B"], v_fd, atol=2e-6)
        np.testing.assert_allclose(k["a_B"], a_fd, atol=2e-5)

    def test_instantaneous_centre_reproduces_slider_speed(self):
        for deg in (30.0, 60.0, 120.0, 250.0):
            theta = np.radians(deg)
            k = crank.kinematics(theta)
            ic = crank.instantaneous_centre(theta)
            # v_B = w_AB k x (r_B - r_IC), x-component.
            v_from_ic = -k["w_AB"] * (k["B"][1] - ic[1])
            self.assertAlmostEqual(float(v_from_ic), float(k["v_B"]), places=12)

    def test_dead_centre_and_quarter_turn(self):
        k0 = crank.kinematics(0.0)
        self.assertAlmostEqual(float(k0["v_B"]), 0.0, places=14)
        r, l, w = crank.CRANK, crank.ROD, crank.CRANK_RATE
        self.assertAlmostEqual(float(k0["a_B"]), -r * w**2 * (1 + r / l), places=12)
        self.assertAlmostEqual(float(k0["w_AB"]), -r * w / l, places=12)
        k90 = crank.kinematics(np.pi / 2)
        self.assertAlmostEqual(float(k90["v_B"]), -r * w, places=12)
        self.assertAlmostEqual(float(k90["w_AB"]), 0.0, places=12)


class TorqueFreeTests(unittest.TestCase):
    def test_invariants_conserved(self):
        inertia = euler.principal_inertia()
        for axis in range(3):
            _, omega = euler.spin(axis)
            energy, h = euler.invariants(omega, inertia)
            self.assertLess(np.ptp(energy) / energy[0], 1e-9)
            self.assertLess(np.ptp(h) / h[0], 1e-9)

    def test_stability_of_principal_axes(self):
        for axis, stable in ((0, True), (1, False), (2, True)):
            _, omega = euler.spin(axis)
            flips = np.min(omega[axis]) < 0
            self.assertEqual(flips, not stable)

    def test_intermediate_axis_growth_rate(self):
        inertia = euler.principal_inertia()
        _, lam, _ = euler.linear_rates(inertia)
        t, omega = euler.spin(1, eps=1e-6, duration=1.0)
        mask = (t > 0.3) & (t < 1.0)
        perturbation = np.hypot(omega[0, mask], omega[2, mask])
        slope = np.polyfit(t[mask], np.log(perturbation), 1)[0]
        self.assertAlmostEqual(slope, lam, delta=0.01 * lam)


class RocketTests(unittest.TestCase):
    def test_gravity_only_matches_closed_form(self):
        t, s = rocket.burn(drag=False)
        v, h = rocket.gravity_only(t)
        np.testing.assert_allclose(s[1], v, rtol=1e-8, atol=1e-6)
        np.testing.assert_allclose(s[0], h, rtol=1e-8, atol=1e-5)

    def test_no_gravity_no_drag_is_tsiolkovsky(self):
        t, s = rocket.burn(g=0.0, drag=False)
        np.testing.assert_allclose(s[1], rocket.ideal_speed(t), rtol=1e-8, atol=1e-6)

    def test_speed_budget_closes(self):
        t, s = rocket.burn()
        ideal = rocket.ideal_speed(rocket.BURN_TIME)
        self.assertAlmostEqual(s[1, -1], ideal - s[2, -1] - s[3, -1], places=5)
        self.assertAlmostEqual(s[2, -1], rocket.GRAVITY * rocket.BURN_TIME, places=6)


class PathCoordinateTests(unittest.TestCase):
    def test_normal_acceleration_and_curvature(self):
        t_flight = 2 * paths.LAUNCH_SPEED * np.sin(paths.LAUNCH_ANGLE) / paths.GRAVITY
        _, v, a = paths.projectile_state(np.linspace(0.05, 0.95, 7) * t_flight)
        speed, a_t, a_n, _, _, rho = paths.normal_tangential(v, a)
        np.testing.assert_allclose(np.hypot(a_t, a_n), paths.GRAVITY)
        np.testing.assert_allclose(a_n, paths.GRAVITY * np.abs(v[0]) / speed)
        # Apex: rho = (v0 cos theta)^2 / g.
        _, v, a = paths.projectile_state([0.5 * t_flight])
        rho_apex = paths.normal_tangential(v, a)[-1][0]
        expected = (
            paths.LAUNCH_SPEED * np.cos(paths.LAUNCH_ANGLE)
        ) ** 2 / paths.GRAVITY
        self.assertAlmostEqual(rho_apex, expected, places=10)

    def test_bead_has_no_radial_acceleration(self):
        r, r_dot, r_ddot, _, w, alpha = paths.bead_state(np.linspace(0, 1, 11))
        a_r, a_theta = paths.polar_acceleration(r, r_dot, r_ddot, w, alpha)
        np.testing.assert_allclose(a_r, 0.0, atol=1e-12)
        np.testing.assert_allclose(a_theta, 2 * r_dot * w)

    def test_rotating_frame_acceleration(self):
        self.assertLess(paths.rotating_frame_check(), 1e-5)


if __name__ == "__main__":
    unittest.main()
