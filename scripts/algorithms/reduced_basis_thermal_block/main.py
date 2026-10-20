"""Certified reduced basis method for a 2D thermal block, built by a weak greedy.

Steady heat conduction -div(k grad u) = 0 on the unit square, split into
2 x 2 blocks with conductivities k = (1, mu_1, mu_2, mu_3), mu_i in [0.1, 10].
A unit heat flux enters through the bottom edge, the top edge is held at
u = 0 and the sides are insulated. The truth model uses piecewise-linear
finite elements on a structured triangulation (4160 unknowns). The stiffness
matrix is affine in the parameters, A(mu) = sum_q theta_q(mu) A_q, so all
reduced quantities, including the dual norm of the residual, split into
parameter-independent pieces computed offline. The weak greedy algorithm adds
the truth solution at the training parameter where the error bound
||r(mu)||_X' / alpha_LB(mu) is largest. The figure shows the decay of the
bound and of the true error, the effectivity of the bound and the online cost
compared with a truth solve.
"""

import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

N_CELLS = 64  # mesh cells per side of the unit square (m)
BLOCKS = 2  # blocks per side; block 0 (bottom left) has conductivity 1 W/(m K)
MU_RANGE = (0.1, 10.0)  # conductivity range of the other blocks (W/(m K))
N_TRAIN = 1000  # training parameters, log-uniform in MU_RANGE
N_TEST = 50  # test parameters for the true error
N_MAX = 25  # largest reduced basis
TOLERANCE = 1e-7  # stop when max relative error bound < TOLERANCE
SEED = 0
EXAMPLE_MU = (5.0, 0.2, 1.0)  # parameters of the solution panel
TIMING_QUERIES = 200  # online queries used to time the reduced solve


@dataclass(frozen=True)
class ThermalBlock:
    """P1 finite element model of the thermal block with affine operators."""

    points: np.ndarray  # node coordinates (n_nodes, 2)
    triangles: np.ndarray  # node indices (n_tri, 3)
    block_of_triangle: np.ndarray  # block index of each triangle
    free: np.ndarray  # nodes not on the Dirichlet edge y = 1
    local_stiffness: np.ndarray  # (n_tri, 3, 3) element matrices for k = 1
    load: np.ndarray  # f_i = integral of phi_i over the bottom edge

    @property
    def n_blocks(self) -> int:
        return int(self.block_of_triangle.max()) + 1

    @property
    def n_dofs(self) -> int:
        return self.free.size


def build_model(n_cells=N_CELLS, blocks=BLOCKS) -> ThermalBlock:
    """Triangulate the unit square and compute element stiffness matrices."""
    if n_cells % blocks:
        raise ValueError("n_cells must be a multiple of blocks")
    h = 1.0 / n_cells
    xs = np.linspace(0.0, 1.0, n_cells + 1)
    gx, gy = np.meshgrid(xs, xs, indexing="xy")
    points = np.column_stack([gx.ravel(), gy.ravel()])
    i, j = np.meshgrid(np.arange(n_cells), np.arange(n_cells), indexing="xy")
    a = (j * (n_cells + 1) + i).ravel()
    b, c, d = a + 1, a + n_cells + 2, a + n_cells + 1
    triangles = np.vstack([np.column_stack([a, b, c]), np.column_stack([a, c, d])])

    centroid = points[triangles].mean(axis=1)
    column = np.minimum((centroid[:, 0] * blocks).astype(int), blocks - 1)
    row = np.minimum((centroid[:, 1] * blocks).astype(int), blocks - 1)

    # Gradients of the barycentric coordinates: rows 1-2 of inv([1, x, y]).
    vertices = points[triangles]
    vandermonde = np.concatenate([np.ones((len(triangles), 3, 1)), vertices], axis=2)
    gradients = np.linalg.inv(vandermonde)[:, 1:, :]
    area = 0.5 * np.abs(np.linalg.det(vandermonde))
    local = area[:, None, None] * np.einsum("eki,ekj->eij", gradients, gradients)

    free = np.flatnonzero(points[:, 1] < 1.0 - 0.5 * h)
    load = np.zeros(len(points))
    bottom = np.flatnonzero(points[:, 1] < 0.5 * h)
    load[bottom] = h
    load[bottom[[0, -1]]] = h / 2  # corner nodes see half an edge
    return ThermalBlock(
        points, triangles, column + blocks * row, free, local, load[free]
    )


def assemble(model: ThermalBlock, element_weights) -> sp.csr_matrix:
    """Assemble sum_e w_e K_e and restrict it to the free nodes."""
    rows = np.repeat(model.triangles, 3, axis=1).ravel()
    cols = np.tile(model.triangles, (1, 3)).ravel()
    values = (
        np.asarray(element_weights)[:, None, None] * model.local_stiffness
    ).ravel()
    n = len(model.points)
    matrix = sp.coo_matrix((values, (rows, cols)), shape=(n, n)).tocsr()
    return matrix[model.free][:, model.free].tocsr()


def affine_operators(model: ThermalBlock) -> list:
    """A_q: the stiffness matrix of block q with unit conductivity."""
    return [
        assemble(model, (model.block_of_triangle == q).astype(float))
        for q in range(model.n_blocks)
    ]


def theta(mu) -> np.ndarray:
    """Affine coefficients theta_q(mu) = (1, mu_1, ..., mu_{Q-1}) per row."""
    mu = np.atleast_2d(mu)
    return np.column_stack([np.ones(len(mu)), mu])


def assemble_direct(model: ThermalBlock, mu) -> sp.csr_matrix:
    """Assemble A(mu) element by element from the conductivity of each block."""
    return assemble(model, theta(mu)[0][model.block_of_triangle])


def assemble_affine(operators, mu) -> sp.csr_matrix:
    """A(mu) = sum_q theta_q(mu) A_q."""
    return sum(t * a for t, a in zip(theta(mu)[0], operators, strict=True))


def truth_solve(model, operators, mu) -> np.ndarray:
    """High-fidelity solution u_h(mu)."""
    return spla.spsolve(assemble_affine(operators, mu).tocsc(), model.load)


def coercivity_lower_bound(mu) -> np.ndarray:
    """Min-theta bound alpha_LB(mu) = min_q theta_q(mu) for the X = A(1) norm.

    a(v, v; mu) = sum_q theta_q a_q(v, v) >= min_q theta_q sum_q a_q(v, v)
    because every a_q is positive semi-definite.
    """
    return theta(mu).min(axis=1)


@dataclass
class ReducedBasis:
    """X-orthonormal basis Z and the offline data for online solves and bounds.

    The Riesz representers of the residual pieces, X^{-1} f and X^{-1} A_q z_n,
    are orthonormalized in the X inner product, W = O R. Online, the residual
    representer is O R c(mu), so ||r||_X' = ||R c(mu)||_2 with no cancellation.
    """

    operators: list
    inner: sp.csc_matrix  # X = sum_q A_q, the energy matrix at mu = 1
    load: np.ndarray
    basis: np.ndarray = None
    reduced_ops: np.ndarray = None  # (Q, N, N) Z^T A_q Z
    reduced_load: np.ndarray = None  # (N,) Z^T f
    residual_r: np.ndarray = None  # R factor of the representers
    gram: np.ndarray = None  # W^T X W, used by the naive bound
    representers: list = field(default_factory=list)
    _lu: object = None

    def __post_init__(self):
        self._lu = spla.splu(self.inner)
        self.basis = np.zeros((self.load.size, 0))
        self._orth = np.zeros((self.load.size, 0))
        self._r = np.zeros((0, 0))
        self._append_representer(self._lu.solve(self.load))

    @property
    def size(self) -> int:
        return self.basis.shape[1]

    def x_inner(self, u, v):
        return u.T @ (self.inner @ v)

    def _append_representer(self, w):
        """Add one column to W = O R by two passes of Gram-Schmidt in X."""
        self.representers.append(w)
        coefficients = np.zeros(self._orth.shape[1])
        v = w.copy()
        for _ in range(2):
            step = self._orth.T @ (self.inner @ v)
            v -= self._orth @ step
            coefficients += step
        norm = np.sqrt(self.x_inner(v, v))
        k = self._r.shape[0]
        r = np.zeros((k + 1, k + 1))
        r[:k, :k] = self._r
        r[:k, k] = coefficients
        r[k, k] = norm
        self._r = r
        self._orth = np.column_stack([self._orth, v / norm])

    def add(self, snapshot):
        """Orthonormalize a truth solution against Z and update offline data."""
        z = snapshot.copy()
        for _ in range(2):
            z -= self.basis @ self.x_inner(self.basis, z)
        z /= np.sqrt(self.x_inner(z, z))
        self.basis = np.column_stack([self.basis, z])
        for a_q in self.operators:
            self._append_representer(self._lu.solve(a_q @ z))
        self.reduced_ops = np.array(
            [self.basis.T @ (a @ self.basis) for a in self.operators]
        )
        self.reduced_load = self.basis.T @ self.load
        # Column order of W: f, then (z_1: A_1..A_Q), (z_2: A_1..A_Q), ...
        self.residual_r = self._r
        w = np.column_stack(self.representers)
        self.gram = w.T @ (self.inner @ w)

    def solve(self, mus):
        """Reduced coefficients a(mu) for each row of mus, shape (n_mu, N)."""
        matrices = np.einsum("sq,qnm->snm", theta(mus), self.reduced_ops)
        rhs = np.broadcast_to(self.reduced_load, (len(matrices), self.size))
        return np.linalg.solve(matrices, rhs[..., None])[..., 0]

    def residual_coefficients(self, mus, coefficients):
        """c(mu) with r(mu) representer = W c: (1, -theta_q a_n ...)."""
        th = theta(mus)
        products = -np.einsum("sn,sq->snq", coefficients, th).reshape(len(th), -1)
        return np.column_stack([np.ones(len(th)), products])

    def residual_norm(self, mus, coefficients, stable=True):
        """Dual norm ||f - A(mu) Z a||_X' for each parameter."""
        c = self.residual_coefficients(mus, coefficients)
        if stable:
            return np.linalg.norm(c @ self.residual_r.T, axis=1)
        squared = np.einsum("si,ij,sj->s", c, self.gram, c)
        return np.sqrt(np.maximum(squared, 0.0))

    def error_bound(self, mus, coefficients, stable=True):
        """Delta_N(mu) = ||r(mu)||_X' / alpha_LB(mu), an upper bound on ||e||_X."""
        return self.residual_norm(mus, coefficients, stable) / coercivity_lower_bound(
            mus
        )


def sample_parameters(rng, n, n_params):
    """Log-uniform samples in MU_RANGE."""
    low, high = np.log10(MU_RANGE)
    return 10.0 ** rng.uniform(low, high, (n, n_params))


def greedy(model, n_max=N_MAX, tolerance=TOLERANCE, seed=SEED):
    """Weak greedy construction with true errors on a test set at every N."""
    rng = np.random.default_rng(seed)
    n_params = model.n_blocks - 1
    train = sample_parameters(rng, N_TRAIN, n_params)
    test = sample_parameters(rng, N_TEST, n_params)
    operators = affine_operators(model)
    rb = ReducedBasis(operators, sum(operators).tocsc(), model.load)
    truth = np.column_stack([truth_solve(model, operators, mu) for mu in test])
    truth_norm = np.sqrt(np.einsum("hs,hs->s", truth, rb.inner @ truth))

    history = {
        key: []
        for key in (
            "bound",
            "naive",
            "error",
            "eta_min",
            "eta_med",
            "eta_max",
            "output_eta_min",
            "selected",
        )
    }
    mu = np.ones(n_params)  # first snapshot at the reference parameter
    for _ in range(n_max):
        history["selected"].append(mu)
        rb.add(truth_solve(model, operators, mu))
        a_train = rb.solve(train)
        rel = np.linalg.norm(a_train, axis=1)  # ||u_N||_X, Z is X-orthonormal
        bound = rb.error_bound(train, a_train) / rel
        naive = rb.error_bound(train, a_train, stable=False) / rel
        a_test = rb.solve(test)
        error_vec = truth - rb.basis @ a_test.T
        error = np.sqrt(np.einsum("hs,hs->s", error_vec, rb.inner @ error_vec))
        eta = rb.error_bound(test, a_test) / error
        # Compliant output s = f^T u: s - s_N = e^T A(mu) e, bound ||r||^2 / alpha_LB.
        output_bound = rb.residual_norm(test, a_test) ** 2 / coercivity_lower_bound(
            test
        )
        # s_h - s_N = f^T e = a(e, e; mu) by Galerkin orthogonality; the quadratic
        # form avoids the cancellation in subtracting two nearly equal outputs.
        output_error = np.array(
            [e @ (assemble_affine(operators, m) @ e) for m, e in zip(test, error_vec.T)]
        )
        history["bound"].append(bound.max())
        history["naive"].append(naive.max())
        history["error"].append((error / truth_norm).max())
        history["eta_min"].append(eta.min())
        history["eta_med"].append(np.median(eta))
        history["eta_max"].append(eta.max())
        history["output_eta_min"].append((output_bound / output_error).min())
        if bound.max() < tolerance:
            break
        mu = train[int(np.argmax(bound))]
    return rb, operators, {k: np.array(v) for k, v in history.items()}, train, test


def time_queries(model, operators, rb, mus):
    """Mean wall-clock time per query of the truth and the reduced model."""
    start = time.perf_counter()
    for mu in mus[:20]:
        truth_solve(model, operators, mu)
    truth_time = (time.perf_counter() - start) / 20

    sizes = np.arange(1, rb.size + 1)
    online = []
    for n in sizes:
        reduced_ops = rb.reduced_ops[:, :n, :n]
        reduced_load = rb.reduced_load[:n]
        start = time.perf_counter()
        for mu in mus:
            matrix = np.tensordot(theta(mu)[0], reduced_ops, axes=1)
            np.linalg.solve(matrix, reduced_load)
        online.append((time.perf_counter() - start) / len(mus))
    start = time.perf_counter()
    for mu in mus:
        a = rb.solve(mu[None])
        rb.error_bound(mu[None], a)
    certified = (time.perf_counter() - start) / len(mus)
    return truth_time, sizes, np.array(online), certified


def plot_results(model, operators, rb, history, timing):
    """Four panels: example solution, greedy decay, effectivity, online cost."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 9.4), constrained_layout=True)
    ax = axes[0, 0]
    mu = np.array(EXAMPLE_MU)
    u = np.zeros(len(model.points))
    u[model.free] = truth_solve(model, operators, mu)
    contour = ax.tricontourf(
        model.points[:, 0],
        model.points[:, 1],
        model.triangles,
        u,
        levels=20,
        cmap="viridis",
    )
    fig.colorbar(contour, ax=ax, label="temperature u [K]")
    for k in range(1, BLOCKS):
        ax.axvline(k / BLOCKS, color="white", lw=1.2)
        ax.axhline(k / BLOCKS, color="white", lw=1.2)
    conductivity = theta(mu)[0]
    for q, value in enumerate(conductivity):
        cx = (q % BLOCKS + 0.5) / BLOCKS
        cy = (q // BLOCKS + 0.5) / BLOCKS
        ax.text(
            cx,
            cy,
            f"k = {value:g}",
            color="white",
            ha="center",
            va="center",
            fontsize=11,
            bbox={"facecolor": "black", "alpha": 0.35, "lw": 0},
        )
    ax.set(
        aspect="equal",
        xlabel="x [m]",
        ylabel="y [m]",
        title="(a) Truth solution; flux in at y = 0, u = 0 at y = 1",
    )

    ax = axes[0, 1]
    n = np.arange(1, len(history["bound"]) + 1)
    ax.semilogy(
        n, history["bound"], "o-", ms=4, label=r"max$_{train}$ $\Delta_N / \|u_N\|_X$"
    )
    ax.semilogy(
        n,
        history["error"],
        "s-",
        ms=4,
        label=r"max$_{test}$ $\|u_h - u_N\|_X / \|u_h\|_X$",
    )
    ax.semilogy(
        n,
        history["naive"],
        "--",
        color="0.5",
        label="bound from the Gram matrix (round-off floor)",
    )
    ax.set(
        xlabel="reduced basis size N [-]",
        ylabel="relative error [-]",
        title="(b) Weak greedy: error bound and true error",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=10)

    ax = axes[1, 0]
    ax.fill_between(
        n,
        history["eta_min"],
        history["eta_max"],
        color="tab:blue",
        alpha=0.25,
        label="range over test set",
    )
    ax.semilogy(n, history["eta_med"], "o-", ms=4, color="tab:blue", label="median")
    ax.axhline(1.0, color="k", lw=1.2, label=r"$\eta = 1$ (rigour limit)")
    ax.axhline(
        MU_RANGE[1] / MU_RANGE[0],
        color="tab:red",
        ls="--",
        label=r"$\gamma_{UB} / \alpha_{LB}$ worst case",
    )
    ax.set(
        ylim=(0.5, 300),
        xlabel="reduced basis size N [-]",
        ylabel=r"effectivity $\eta = \Delta_N / \|e\|_X$ [-]",
        title="(c) Effectivity of the error bound",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=10, loc="upper left")

    ax = axes[1, 1]
    truth_time, sizes, online, certified = timing
    ax.semilogy(sizes, 1e3 * online, "o-", ms=4, label="online reduced solve")
    ax.axhline(
        1e3 * truth_time,
        color="k",
        ls="--",
        label=f"truth assembly + sparse solve ({model.n_dofs} DOF)",
    )
    ax.axhline(
        1e3 * certified,
        color="tab:orange",
        ls=":",
        label=f"reduced solve + error bound, N = {rb.size}",
    )
    ax.set(
        ylim=(1e-3, 30),
        xlabel="reduced basis size N [-]",
        ylabel="time per query [ms]",
        title="(d) Online cost against a truth solve",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=10, loc="center right")
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)
    model = build_model()
    rb, operators, history, train, test = greedy(model)
    timing = time_queries(
        model, operators, rb, test[np.arange(TIMING_QUERIES) % len(test)]
    )
    print(
        f"truth model: {model.n_dofs} unknowns, {model.n_blocks - 1} parameters, "
        f"{N_TRAIN} training points"
    )
    print(
        "   N   max bound   max error   effectivity min / median / max   output eta min"
    )
    for k in range(len(history["bound"])):
        print(
            f"{k + 1:4d}   {history['bound'][k]:.2e}    {history['error'][k]:.2e}"
            f"    {history['eta_min'][k]:6.2f} / {history['eta_med'][k]:6.2f} / "
            f"{history['eta_max'][k]:6.2f}       {history['output_eta_min'][k]:.2f}"
        )
    truth_time, _, online, certified = timing
    print(
        f"truth solve {1e3 * truth_time:.2f} ms; reduced solve N = {rb.size} "
        f"{1e3 * online[-1]:.4f} ms; with bound {1e3 * certified:.4f} ms; "
        f"speed-up {truth_time / certified:.0f}x"
    )
    figure = plot_results(model, operators, rb, history, timing)
    finish_figures(
        {"reduced_basis_thermal_block.png": figure},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
