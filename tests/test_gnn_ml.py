"""Graph and message-passing contracts for the GNN and surrogate-input figures."""

import importlib.util
import unittest
from pathlib import Path

import matplotlib
import numpy as np
from scipy.sparse.csgraph import shortest_path
from scipy.spatial import Delaunay

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]


def load_plot(name):
    spec = importlib.util.spec_from_file_location(
        f"plot_{name}", ROOT / "scripts" / "plots" / name / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gnn = load_plot("gnn_message_passing")
representations = load_plot("surrogate_input_representations")


def square_mesh(n=61, seed=0):
    """Jittered Delaunay mesh of [-1, 1]^2 with fixed boundary nodes."""
    rng = np.random.default_rng(seed)
    s = np.linspace(-1.0, 1.0, n)
    gx, gy = np.meshgrid(s, s)
    points = np.column_stack([gx.ravel(), gy.ravel()])
    interior = np.all(np.abs(points) < 1.0 - 1e-12, axis=1)
    h = s[1] - s[0]
    points[interior] += 0.3 * h * rng.uniform(-1.0, 1.0, (interior.sum(), 2))
    return points, Delaunay(points).simplices


class CylinderMeshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.points, cls.triangles = gnn.cylinder_mesh()
        cls.edges = gnn.unique_edges(cls.triangles)

    def test_no_triangle_inside_body_and_annulus_topology(self):
        centroids = self.points[self.triangles].mean(axis=1)
        self.assertTrue(np.all(np.hypot(*centroids.T) > gnn.RADIUS))
        # An annulus has Euler characteristic V - E + F = 0.
        euler = len(self.points) - len(self.edges) + len(self.triangles)
        self.assertEqual(euler, 0)

    def test_bfs_matches_scipy_unweighted_shortest_path(self):
        graph = gnn.adjacency(len(self.points), self.edges)
        for source in (0, 123, len(self.points) - 1):
            with self.subTest(source=source):
                hops = gnn.hop_distances(len(self.points), self.edges, source)
                reference = shortest_path(graph, indices=source, unweighted=True)
                np.testing.assert_array_equal(hops, reference.astype(int))

    def test_receptive_field_equals_support_of_k_linear_steps(self):
        edges, weights = gnn.cotangent_weights(self.points, self.triangles)
        areas = gnn.lumped_areas(self.points, self.triangles)
        dt = 0.5 * gnn.stable_time_step(edges, weights, areas)
        source = 200
        # Edges whose cotangent weight is zero carry no message.
        hops = gnn.hop_distances(len(self.points), edges[weights > 0.0], source)
        h = np.zeros(len(self.points))
        h[source] = 1.0
        for k in range(1, 7):
            h = gnn.message_passing_step(h, edges, weights, areas, dt)
            support = h > 0.0
            np.testing.assert_array_equal(support, (hops >= 0) & (hops <= k))

    def test_diffusion_conserves_integral_and_obeys_maximum_principle(self):
        edges, weights = gnn.cotangent_weights(self.points, self.triangles)
        areas = gnn.lumped_areas(self.points, self.triangles)
        self.assertTrue(np.all(weights >= 0.0))
        dt = gnn.stable_time_step(edges, weights, areas)
        h = gnn.gaussian(self.points, gnn.BLOB_CENTRE, gnn.BLOB_SIGMA)
        mass0, peak = np.sum(areas * h), h.max()
        for _ in range(200):
            h = gnn.message_passing_step(h, edges, weights, areas, dt)
            self.assertLessEqual(h.max(), peak + 1e-12)
            self.assertGreaterEqual(h.min(), -1e-14)
            peak = h.max()
        self.assertAlmostEqual(np.sum(areas * h) / mass0, 1.0, places=13)


class DiffusionAccuracyTests(unittest.TestCase):
    def test_lumped_areas_sum_to_domain_area(self):
        points, triangles = square_mesh()
        self.assertAlmostEqual(gnn.lumped_areas(points, triangles).sum(), 4.0)

    def test_gaussian_spreads_at_the_exact_rate(self):
        points, triangles = square_mesh()
        edges, weights = gnn.cotangent_weights(points, triangles)
        areas = gnn.lumped_areas(points, triangles)
        sigma0, kappa, t_end = 0.1, 1.0, 0.005
        dt = 0.9 * gnn.stable_time_step(edges, weights, areas, kappa)
        n_steps = int(np.ceil(t_end / dt))
        h = gnn.gaussian(points, (0.0, 0.0), sigma0)
        for _ in range(n_steps):
            h = gnn.message_passing_step(
                h, edges, weights, areas, t_end / n_steps, kappa
            )
        exact = gnn.gaussian(points, (0.0, 0.0), np.sqrt(sigma0**2 + 2 * kappa * t_end))
        error = np.sqrt(np.sum(areas * (h - exact) ** 2) / np.sum(areas * exact**2))
        self.assertLess(error, 0.01)
        self.assertAlmostEqual(
            gnn.spread_variance(points, h, areas),
            sigma0**2 + 2 * kappa * t_end,
            delta=0.005 * (sigma0**2 + 2 * kappa * t_end),
        )


class RepresentationTests(unittest.TestCase):
    def test_signed_distance_sign_and_magnitude(self):
        outline = representations.naca4("0012")
        probes = np.array([[0.3, 0.0], [0.5, 1.0], [-1.0, 0.0]])
        phi = representations.signed_distance(probes, outline)
        self.assertLess(phi[0], 0.0)
        # NACA 0012 half-thickness at x = 0.3 is about 0.06c.
        self.assertAlmostEqual(-phi[0], 0.06, delta=0.002)
        self.assertAlmostEqual(phi[2], 1.0, delta=1e-3)

    def test_point_cloud_lies_on_surface_with_unit_outward_normals(self):
        outline = representations.naca4()
        pts, normal = representations.point_cloud(outline)
        np.testing.assert_allclose(np.hypot(*normal.T), 1.0)
        on_surface = representations.signed_distance(pts, outline)
        self.assertLess(np.abs(on_surface).max(), 1e-3)
        outside = representations.signed_distance(pts + 0.01 * normal, outline)
        self.assertTrue(np.all(outside > 0.0))


if __name__ == "__main__":
    unittest.main()
