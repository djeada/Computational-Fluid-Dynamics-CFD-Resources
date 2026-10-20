"""Physics-informed neural network for a 1D advection-diffusion boundary layer.

Trains a one-hidden-layer tanh network u_theta(x) so that the residual of
eps u'' - u' = 0 vanishes at collocation points in [0, 1] and the boundary
conditions u(0) = 0, u(1) = 1 hold, for three values of eps. The derivatives
of the network with respect to x are written out analytically, and so is the
Jacobian of the residuals with respect to the weights, which Levenberg-Marquardt
(scipy.optimize.least_squares) uses. The thinner the layer at x = 1, the harder
the training problem: at the smallest eps the network converges to a solution
that hides the jump between two collocation points.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

EPSILONS = (0.1, 0.02, 0.01)  # diffusivity / advection speed (layer width), [-]
N_HIDDEN = 10  # neurons in the single tanh hidden layer
N_COLLOCATION = 50  # uniformly spaced residual points in [0, 1]
N_EVAL = 4001  # dense grid used to measure the true error and residual
BC_WEIGHT = 1.0  # lambda multiplying the squared boundary-condition misfit
INIT_WEIGHT_STD = 5.0  # std of the initial input weights w_j, [1/length]
MAX_EVALUATIONS = 1000  # residual evaluations allowed per training run
SEED = 0


@dataclass
class PINNResult:
    eps: float
    theta: np.ndarray
    x_collocation: np.ndarray
    loss_history: np.ndarray


def exact_solution(x, eps):
    """u(x) = (exp(x/eps) - 1) / (exp(1/eps) - 1), written without overflow."""
    return (np.exp((x - 1.0) / eps) - np.exp(-1.0 / eps)) / (1.0 - np.exp(-1.0 / eps))


def unpack(theta, n_hidden=N_HIDDEN):
    """Split the flat parameter vector into (w, b, v, c)."""
    w = theta[:n_hidden]
    b = theta[n_hidden : 2 * n_hidden]
    v = theta[2 * n_hidden : 3 * n_hidden]
    c = theta[3 * n_hidden]
    return w, b, v, c


def hidden_layer(theta, x, n_hidden=N_HIDDEN):
    """Return tanh(z), its first three z-derivatives, and the weights.

    With t = tanh(z): dt/dz = s = 1 - t^2, d2t/dz2 = q = -2 t s and
    d3t/dz3 = q' = -2 s^2 + 4 t^2 s.
    """
    w, b, v, c = unpack(theta, n_hidden)
    z = np.outer(x, w) + b
    t = np.tanh(z)
    s = 1.0 - t * t
    q = -2.0 * t * s
    dq = -2.0 * s * s + 4.0 * t * t * s
    return t, s, q, dq, w, v, c


def network(theta, x, n_hidden=N_HIDDEN):
    """Evaluate u, du/dx and d2u/dx2 of u(x) = sum_j v_j tanh(w_j x + b_j) + c."""
    t, s, q, _, w, v, c = hidden_layer(theta, x, n_hidden)
    u = t @ v + c
    du = (s * w) @ v
    d2u = (q * w**2) @ v
    return u, du, d2u


def network_jacobians(theta, x, n_hidden=N_HIDDEN):
    """Derivatives of u, u' and u'' with respect to theta = (w, b, v, c).

    Each returned array has one row per point in x and one column per parameter.
    """
    t, s, q, dq, w, v, _ = hidden_layer(theta, x, n_hidden)
    xc = x[:, None]
    ones = np.ones((x.size, 1))
    zeros = np.zeros((x.size, 1))
    j_u = np.hstack([v * s * xc, v * s, t, ones])
    j_du = np.hstack([v * s + v * w * q * xc, v * w * q, w * s, zeros])
    j_d2u = np.hstack(
        [2 * v * w * q + v * w**2 * dq * xc, v * w**2 * dq, w**2 * q, zeros]
    )
    return j_u, j_du, j_d2u


def pde_residual(theta, x, eps, n_hidden=N_HIDDEN):
    """Pointwise residual r(x) = eps u'' - u' of the network."""
    _, du, d2u = network(theta, x, n_hidden)
    return eps * d2u - du


def residual_vector(theta, x, eps, n_hidden=N_HIDDEN, bc_weight=BC_WEIGHT):
    """Stacked residuals whose sum of squares is the PINN loss.

    L(theta) = (1/N) sum_k r(x_k)^2 + lambda [u(0)^2 + (u(1) - 1)^2].
    """
    r = pde_residual(theta, x, eps, n_hidden) / np.sqrt(x.size)
    u_bc = network(theta, np.array([0.0, 1.0]), n_hidden)[0]
    bc = np.sqrt(bc_weight) * (u_bc - np.array([0.0, 1.0]))
    return np.concatenate([r, bc])


def residual_jacobian(theta, x, eps, n_hidden=N_HIDDEN, bc_weight=BC_WEIGHT):
    """Analytic Jacobian of residual_vector with respect to theta."""
    _, j_du, j_d2u = network_jacobians(theta, x, n_hidden)
    j_r = (eps * j_d2u - j_du) / np.sqrt(x.size)
    j_bc = network_jacobians(theta, np.array([0.0, 1.0]), n_hidden)[0]
    return np.vstack([j_r, np.sqrt(bc_weight) * j_bc])


def initial_parameters(rng, n_hidden=N_HIDDEN, weight_std=INIT_WEIGHT_STD):
    """Random input weights with tanh centres -b_j/w_j spread over [0, 1]."""
    w = rng.normal(0.0, weight_std, n_hidden)
    b = -w * rng.uniform(0.0, 1.0, n_hidden)
    v = rng.normal(0.0, 0.1, n_hidden)
    return np.concatenate([w, b, v, [0.0]])


def train_pinn(
    eps,
    n_collocation=N_COLLOCATION,
    n_hidden=N_HIDDEN,
    max_evaluations=MAX_EVALUATIONS,
    seed=SEED,
):
    """Minimise the PINN loss with Levenberg-Marquardt and record its history."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 1.0, n_collocation)
    history = []

    def fun(theta):
        r = residual_vector(theta, x, eps, n_hidden)
        history.append(r @ r)
        return r

    solution = least_squares(
        fun,
        initial_parameters(rng, n_hidden),
        jac=lambda theta: residual_jacobian(theta, x, eps, n_hidden),
        method="lm",
        max_nfev=max_evaluations,
        xtol=1e-15,
        ftol=1e-15,
        gtol=1e-15,
    )
    return PINNResult(eps, solution.x, x, np.minimum.accumulate(history))


def plot_results(results):
    colors = plt.get_cmap("tab10").colors
    x_eval = np.linspace(0.0, 1.0, N_EVAL)
    fig, axs = plt.subplots(2, 3, figsize=(13, 8))

    for ax, result, color in zip(axs[0], results, colors):
        u_pinn = network(result.theta, x_eval)[0]
        u_exact = exact_solution(x_eval, result.eps)
        ax.plot(x_eval, u_exact, "k--", lw=2, label="exact")
        ax.plot(x_eval, u_pinn, color=color, lw=1.5, label="PINN")
        ax.plot(
            result.x_collocation,
            np.full(result.x_collocation.size, -0.05),
            "|",
            color="0.4",
            ms=8,
            label="collocation points",
        )
        max_error = np.max(np.abs(u_pinn - u_exact))
        ax.set_title(rf"$\varepsilon = {result.eps}$, max error {max_error:.1e}")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$u$")
        ax.set_ylim(-0.1, 1.1)
        ax.legend(loc="center left", bbox_to_anchor=(0.12, 0.6), fontsize=10)

    for result, color in zip(results, colors):
        label = rf"$\varepsilon = {result.eps}$"
        u_pinn = network(result.theta, x_eval)[0]
        residual = np.abs(pde_residual(result.theta, x_eval, result.eps))
        error = np.abs(u_pinn - exact_solution(x_eval, result.eps))
        axs[1, 0].semilogy(x_eval, residual + 1e-16, color=color, label=label)
        axs[1, 1].semilogy(x_eval, error + 1e-16, color=color, label=label)
        axs[1, 2].semilogy(result.loss_history, color=color, label=label)

    axs[1, 0].set_title(r"PDE residual $|\varepsilon u'' - u'|$ on a dense grid")
    axs[1, 0].set_xlabel("$x$")
    axs[1, 0].set_ylabel("residual")
    axs[1, 0].set_ylim(1e-8, 1e4)
    axs[1, 1].set_title(r"Pointwise error $|u_\theta - u|$")
    axs[1, 1].set_xlabel("$x$")
    axs[1, 1].set_ylabel("error")
    axs[1, 1].set_ylim(1e-10, 10)
    axs[1, 2].set_title(r"Training loss $\mathcal{L}(\theta)$")
    axs[1, 2].set_xlabel("residual evaluations (Levenberg-Marquardt)")
    axs[1, 2].set_ylabel("loss")
    for ax in axs[1]:
        ax.legend(fontsize=10)
        ax.grid(True, which="major", alpha=0.3)
    fig.tight_layout()
    return fig


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    x_eval = np.linspace(0.0, 1.0, N_EVAL)
    results = []
    for eps in EPSILONS:
        result = train_pinn(eps)
        u_pinn = network(result.theta, x_eval)[0]
        max_error = np.max(np.abs(u_pinn - exact_solution(x_eval, eps)))
        max_residual = np.max(np.abs(pde_residual(result.theta, x_eval, eps)))
        print(
            f"eps = {eps:5.3f}: final loss {result.loss_history[-1]:.2e}, "
            f"max error {max_error:.2e}, max dense-grid residual {max_residual:.2e}"
        )
        results.append(result)
    fig = plot_results(results)
    finish_figures(
        {"pinn_boundary_layer.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
