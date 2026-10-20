"""Fundamentals of mechanics: resultants, moments about axes, frame rotation, reactions."""

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


resultant_mod = load_example("plots", "fundamentals_force_resultant")
supports_mod = load_example("plots", "fundamentals_support_reactions")
fbd_mod = load_example("plots", "fundamentals_free_body_diagram")
axis_mod = load_example("algorithms", "fundamentals_moment_about_axis")
rotation_mod = load_example("plots", "fundamentals_coordinate_rotation")


class ForceResultantTests(unittest.TestCase):
    def setUp(self):
        self.vectors, self.points = resultant_mod.force_vectors()
        self.total, self.moment = resultant_mod.resultant(self.vectors, self.points)

    def test_resultant_matches_hand_calculation(self):
        np.testing.assert_allclose(self.total, [-100.0, -659.8076], atol=1e-3)
        self.assertAlmostEqual(self.moment, -624.5191, places=3)

    def test_single_resultant_is_equivalent_about_any_point(self):
        foot, _ = resultant_mod.line_of_action(self.total, self.moment)
        for q in ([0.0, 0.0], [3.0, -1.0], [-2.0, 5.0], [4.0, 2.0]):
            q = np.array(q)
            system = resultant_mod.COUPLE + sum(
                resultant_mod.moment_2d(p, f, q)
                for p, f in zip(self.points, self.vectors)
            )
            single = resultant_mod.moment_2d(foot, self.total, q)
            self.assertAlmostEqual(system, single, places=9)

    def test_moment_arm_and_intercepts_lie_on_the_line(self):
        foot, direction = resultant_mod.line_of_action(self.total, self.moment)
        self.assertAlmostEqual(
            np.hypot(*foot), abs(self.moment) / np.hypot(*self.total), places=12
        )
        self.assertAlmostEqual(np.dot(foot, direction), 0.0, places=12)
        for y in (0.0, 2.0):
            x = resultant_mod.axis_intercept(self.total, self.moment, y=y)
            moment = resultant_mod.moment_2d((x, y), self.total)
            self.assertAlmostEqual(moment, self.moment, places=9)

    def test_pure_couple_has_no_line_of_action(self):
        with self.assertRaises(ValueError):
            resultant_mod.line_of_action(np.zeros(2), 50.0)


class SupportReactionTests(unittest.TestCase):
    def test_unknown_counts_match_planar_supports(self):
        expected = {
            "cable": 1,
            "link": 1,
            "roller": 1,
            "smooth": 1,
            "collar": 1,
            "pin": 2,
            "fixed_collar": 2,
            "fixed": 3,
        }
        for key, count in expected.items():
            self.assertEqual(supports_mod.unknown_count(key), count)

    def test_every_support_has_a_drawing(self):
        keys = {key for key, *_ in supports_mod.SUPPORTS}
        self.assertEqual(keys, set(supports_mod.DRAWERS))


class FreeBodyDiagramTests(unittest.TestCase):
    def test_reactions_satisfy_all_three_equilibrium_equations(self):
        reactions = fbd_mod.beam_reactions()
        np.testing.assert_allclose(
            fbd_mod.equilibrium_residual(reactions), 0.0, atol=1e-12
        )
        np.testing.assert_allclose(reactions, [-10.0, 13.6378, 18.6827], atol=1e-4)

    def test_triangular_load_resultant_and_centroid(self):
        r, xc = fbd_mod.distributed_resultant(0.0, 6.0, 0.0, 4.0)
        self.assertAlmostEqual(r, 12.0)
        self.assertAlmostEqual(xc, 4.0)

    def test_symmetric_load_splits_equally(self):
        a_x, a_y, b_y = fbd_mod.beam_reactions(
            length=10.0, point_loads=((5.0, 8.0, -90.0),), distributed=()
        )
        self.assertAlmostEqual(a_x, 0.0, places=12)
        self.assertAlmostEqual(a_y, 4.0)
        self.assertAlmostEqual(b_y, 4.0)


class MomentAboutAxisTests(unittest.TestCase):
    def test_worked_example(self):
        m_o = axis_mod.moment_about_point(
            axis_mod.AXIS_POINT, axis_mod.POINT, axis_mod.FORCE
        )
        np.testing.assert_allclose(m_o, [60.0, 5.0, -100.0], atol=1e-12)
        m_a = axis_mod.moment_about_axis(
            axis_mod.AXIS_POINT, axis_mod.AXIS_DIRECTION, axis_mod.POINT, axis_mod.FORCE
        )
        self.assertAlmostEqual(m_a, -25.0, places=10)

    def test_triple_product_equals_projection(self):
        rng = np.random.default_rng(0)
        for _ in range(20):
            a, d, p, f = rng.normal(size=(4, 3))
            u = d / np.linalg.norm(d)
            expected = np.dot(u, np.cross(p - a, f))
            self.assertAlmostEqual(
                axis_mod.moment_about_axis(a, d, p, f), expected, places=10
            )

    def test_axis_moment_is_invariant_and_bounds_point_moment(self):
        point_moment, axis_q, axis_p = axis_mod.invariance_study()
        np.testing.assert_allclose(axis_q, -25.0, atol=1e-10)
        np.testing.assert_allclose(axis_p, -25.0, atol=1e-10)
        self.assertTrue(np.all(point_moment >= 25.0 - 1e-9))

    def test_parallel_or_intersecting_force_has_no_axis_moment(self):
        u = np.array([0.0, 0.0, 1.0])
        self.assertAlmostEqual(
            axis_mod.moment_about_axis([0, 0, 0], u, [1.0, 2.0, 0.0], 5.0 * u), 0.0
        )
        self.assertAlmostEqual(
            axis_mod.moment_about_axis([0, 0, 0], u, [0.0, 0.0, 3.0], [1.0, 2.0, 0.0]),
            0.0,
        )

    def test_split_moment_is_orthogonal(self):
        m = np.array([60.0, 5.0, -100.0])
        par, perp = axis_mod.split_moment(m, axis_mod.AXIS_DIRECTION)
        np.testing.assert_allclose(par + perp, m)
        self.assertAlmostEqual(
            np.dot(perp, axis_mod.unit(axis_mod.AXIS_DIRECTION)), 0.0
        )


class CoordinateRotationTests(unittest.TestCase):
    def test_matrix_is_proper_orthogonal(self):
        for theta in (0.0, 17.0, 30.0, 135.0, 300.0):
            q = rotation_mod.rotation_matrix_z(theta)
            np.testing.assert_allclose(q @ q.T, np.eye(3), atol=1e-14)
            self.assertAlmostEqual(np.linalg.det(q), 1.0, places=14)

    def test_components_and_invariants(self):
        f_new = rotation_mod.transform(rotation_mod.FORCE, 30.0)
        np.testing.assert_allclose(f_new, [459.8076, 196.4102], atol=1e-4)
        self.assertAlmostEqual(np.linalg.norm(f_new), 500.0, places=10)
        g = np.array([-120.0, 50.0])
        self.assertAlmostEqual(
            np.dot(f_new, rotation_mod.transform(g, 30.0)),
            np.dot(rotation_mod.FORCE, g),
            places=9,
        )

    def test_successive_rotations_add(self):
        np.testing.assert_allclose(
            rotation_mod.rotation_matrix(25.0) @ rotation_mod.rotation_matrix(40.0),
            rotation_mod.rotation_matrix(65.0),
            atol=1e-14,
        )


if __name__ == "__main__":
    unittest.main()
