"""Transportation notes: INS error growth and fusion, aircraft sizing, car road load and ride."""

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


ins = load_example("algorithms", "ins_dead_reckoning_errors")
design = load_example("plots", "aircraft_design_constraint_diagram")
car = load_example("algorithms", "car_road_load_and_quarter_car")


class InertialNavigationTests(unittest.TestCase):
    def test_accelerometer_bias_error_is_half_b_t_squared(self):
        bias = 1.0e-3
        t, err = ins.stationary_error(accel_bias=bias, dt=0.5, duration=1800.0)
        np.testing.assert_allclose(err, 0.5 * bias * t**2, rtol=1e-9, atol=1e-9)

    def test_gyro_bias_error_grows_as_t_cubed(self):
        eps = 1.0 * ins.DEG_PER_HOUR
        t, err = ins.stationary_error(gyro_bias=eps, dt=0.5, duration=1800.0)
        late = t >= 60.0  # past the start-up transient of the discrete time steps
        expected = ins.GRAVITY * eps * t[late] ** 3 / 6.0
        np.testing.assert_allclose(np.abs(err[late]), expected, rtol=0.01)

    def test_schuler_loop_bounds_accelerometer_bias_error(self):
        bias = 5.0e-4
        t, err = ins.stationary_error(
            accel_bias=bias, schuler=True, dt=1.0, duration=7200.0
        )
        lin, _ = ins.schuler_error(t, accel_bias=bias)
        np.testing.assert_allclose(err, lin, atol=0.01 * lin.max())
        self.assertAlmostEqual(ins.SCHULER_PERIOD / 60.0, 84.4, places=1)

    def test_perfect_sensors_reproduce_truth(self):
        t = np.arange(0.0, 300.0 + 1e-9, 0.1)
        speed, pitch = ins.flight_profile(t)
        truth, gyro, force_b = ins.truth_and_imu(t, speed, pitch)
        pos, vel, att = ins.mechanize(
            0.1, gyro, force_b, truth["pos"][0], truth["vel"][0], truth["pitch"][0]
        )
        np.testing.assert_allclose(pos, truth["pos"], atol=1e-6)
        np.testing.assert_allclose(att, truth["pitch"], atol=1e-12)

    def test_kalman_filter_covariance_positive_and_error_bounded(self):
        aided = ins.run_flight(aided=True)
        free = ins.run_flight(aided=False)
        self.assertGreater(aided["min_eig"], 0.0)
        err_aided = np.linalg.norm(aided["pos"] - aided["truth"]["pos"], axis=1)
        err_free = np.linalg.norm(free["pos"] - free["truth"]["pos"], axis=1)
        self.assertLess(err_aided[-1000:].max(), 15.0)
        self.assertGreater(err_free[-1], 1000.0)
        # The actual error stays inside the filter's 3-sigma bound almost always.
        inside = err_aided <= 3.0 * np.linalg.norm(aided["sigma"], axis=1)
        self.assertGreater(inside.mean(), 0.97)


class AircraftDesignTests(unittest.TestCase):
    def test_breguet_range_units_and_value(self):
        # V/(c g) (L/D) ln(Wi/Wf) with V = 230 m/s, c = 1.6e-5 kg/(N s).
        expected = 230.0 / (1.6e-5 * 9.81) * 18.0 * np.log(1.35)
        self.assertAlmostEqual(design.breguet_range(18.0, 1.35), expected)
        self.assertAlmostEqual(design.breguet_range(18.0, 1.35) / 1e3, 7916, delta=1)

    def test_cruise_constraint_minimum(self):
        # q C_D0/(W/S) + k (W/S)/q is smallest at W/S = q sqrt(C_D0/k), where T/W = 2 sqrt(k C_D0).
        q = design.dynamic_pressure(1.0, 100.0)
        ws = np.linspace(100.0, 20000.0, 20001)
        tw = design.level_flight_tw(ws, q)
        k = np.argmin(tw)
        self.assertAlmostEqual(
            ws[k], q * np.sqrt(design.CD0 / design.K_INDUCED), delta=2.0
        )
        self.assertAlmostEqual(
            tw[k], 2.0 * np.sqrt(design.K_INDUCED * design.CD0), places=6
        )

    def test_design_point_is_feasible(self):
        ws, tw, _ = design.design_point()
        self.assertLessEqual(ws, design.stall_wing_loading())
        for func in (
            design.takeoff_constraint,
            design.climb_constraint,
            design.cruise_constraint,
        ):
            self.assertLessEqual(float(func(np.array(ws))), tw + 1e-12)


class CarTests(unittest.TestCase):
    def test_crossover_speed_balances_rolling_and_aero(self):
        u_c = car.crossover_speed()
        self.assertAlmostEqual(car.aero_force(u_c), car.rolling_force(), places=9)
        expected = np.sqrt(2 * 1500 * 9.81 * 0.010 / (1.225 * 0.30 * 2.2))
        self.assertAlmostEqual(u_c, expected, places=12)

    def test_road_load_grade_and_inertia(self):
        f = car.road_load(0.0, accel=1.0, grade=np.arctan(0.05))
        expected = 1500 * 9.81 * 0.010 + 1500 * 9.81 * np.sin(np.arctan(0.05)) + 1500
        self.assertAlmostEqual(f, expected)

    def test_cycle_energy_balance(self):
        # Traction minus braking energy equals the dissipated rolling and aero work
        # because the cycle starts and ends at rest.
        t, u = car.drive_cycle()
        distance, traction, braking, _ = car.cycle_energy(t, u)
        dt = t[1] - t[0]
        u_mid = 0.5 * (u[1:] + u[:-1])
        moving = u_mid > 0
        dissipated = (
            np.sum(
                (car.rolling_force() + car.aero_force(u_mid[moving])) * u_mid[moving]
            )
            * dt
        )
        self.assertAlmostEqual((traction - braking) / dissipated, 1.0, places=9)
        self.assertGreater(distance, 0.0)

    def test_quarter_car_frequencies_match_closed_form(self):
        ms, mu, ks, kt = (
            car.SPRUNG_MASS,
            car.UNSPRUNG_MASS,
            car.SPRING_RATE,
            car.TYRE_RATE,
        )
        # m_s m_u w^4 - (m_s (k_s + k_t) + m_u k_s) w^2 + k_s k_t = 0
        a, b, c = ms * mu, -(ms * (ks + kt) + mu * ks), ks * kt
        w2 = np.sort(np.roots([a, b, c]).real)
        np.testing.assert_allclose(
            car.natural_frequencies(), np.sqrt(w2) / (2 * np.pi), rtol=1e-10
        )
        f_body, f_wheel = car.natural_frequencies()
        approx_body = np.sqrt(ks * kt / ((ks + kt) * ms)) / (2 * np.pi)
        approx_wheel = np.sqrt((ks + kt) / mu) / (2 * np.pi)
        self.assertAlmostEqual(f_body / approx_body, 1.0, delta=0.02)
        self.assertAlmostEqual(f_wheel / approx_wheel, 1.0, delta=0.02)

    def test_quarter_car_static_limit(self):
        accel, tyre = car.quarter_car_response(np.array([1e-4]), 0.3)
        self.assertLess(accel[0], 1e-6)
        self.assertLess(tyre[0], 1e-6)


if __name__ == "__main__":
    unittest.main()
