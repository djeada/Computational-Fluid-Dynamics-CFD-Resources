"""Exact dynamic mode decomposition (DMD) of a synthetic three-mode wave field.

A real 1D field u(x, t) is built from three travelling wave packets with known
angular frequencies and growth rates, and Gaussian noise is added. Exact DMD
(Tu et al. 2014) is fitted to the first half of the record, and the figure
shows the singular value spectrum, the DMD eigenvalues against the unit circle
and the true ones, the recovered spatial modes, and the error of the DMD
reconstruction and forecast beyond the training window.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402

SEED = 0
N_X = 200  # grid points on x in [-10, 10]
X_MIN, X_MAX = -10.0, 10.0  # domain (m)
DT = 0.05  # snapshot spacing (s)
N_TRAIN = 200  # snapshots used to fit DMD (t = 0 ... 9.95 s)
N_TOTAL = 400  # snapshots generated (forecast to t = 19.95 s)
NOISE_STD = 0.02  # standard deviation of additive noise (field units)
RANK = 6  # DMD truncation rank: three conjugate pairs

# Each packet: (amplitude, growth rate (1/s), angular frequency (rad/s),
# envelope centre (m), envelope width (m), carrier wavenumber (rad/m)).
MODES = [
    (1.0, 0.00, 2.0, -4.0, 1.5, 1.5),
    (0.8, -0.15, 5.0, 0.0, 1.0, 0.6),
    (0.4, 0.05, 8.0, 4.0, 1.2, -2.5),
]


def true_spatial_modes(x):
    """Complex spatial shapes phi_k(x) = A_k exp(-(x - c_k)^2 / w_k^2) exp(i k_k x)."""
    return np.column_stack(
        [
            amp * np.exp(-(((x - centre) / width) ** 2)) * np.exp(1j * wavenumber * x)
            for amp, _, _, centre, width, wavenumber in MODES
        ]
    )


def true_continuous_eigenvalues():
    """Continuous-time eigenvalues omega_k = g_k + i w_k (one per conjugate pair)."""
    return np.array([growth + 1j * freq for _, growth, freq, *_ in MODES])


def make_field(x, t, noise_std=NOISE_STD, seed=SEED):
    """Return the clean real field and a noisy copy, shape (n_x, n_t)."""
    phi = true_spatial_modes(x)
    temporal = np.exp(np.outer(true_continuous_eigenvalues(), t))
    clean = np.real(phi @ temporal)
    rng = np.random.default_rng(seed)
    noisy = clean + noise_std * rng.standard_normal(clean.shape)
    return clean, noisy


def dmd(X, r):
    """Exact DMD of the snapshot sequence X (space in rows, time in columns).

    Returns the eigenvalues lambda (r,), the exact DMD modes Phi (n, r) and the
    mode amplitudes b (r,) fitted to the first snapshot, so that
    x_k ~ Phi diag(lambda)^k b.
    """
    X = np.asarray(X)
    X1, X2 = X[:, :-1], X[:, 1:]
    U, s, Vh = np.linalg.svd(X1, full_matrices=False)
    r = min(r, int(np.sum(s > s[0] * 1e-13)))
    U_r, s_r, V_r = U[:, :r], s[:r], Vh[:r].conj().T
    A_tilde = U_r.conj().T @ X2 @ V_r / s_r
    eigenvalues, W = np.linalg.eig(A_tilde)
    modes = X2 @ V_r / s_r @ W
    amplitudes = np.linalg.lstsq(modes, X[:, 0], rcond=None)[0]
    return eigenvalues, modes, amplitudes


def dmd_predict(eigenvalues, modes, amplitudes, n_steps):
    """Evaluate x_k = Phi diag(lambda)^k b for k = 0 ... n_steps - 1."""
    powers = eigenvalues[:, None] ** np.arange(n_steps)[None, :]
    return modes @ (amplitudes[:, None] * powers)


def match_eigenvalues(estimated, true):
    """For each true eigenvalue, return the index of the closest estimate."""
    return np.array([np.argmin(np.abs(estimated - value)) for value in true])


def relative_error(prediction, reference):
    """Relative L2 error per snapshot (column)."""
    return np.linalg.norm(prediction - reference, axis=0) / np.linalg.norm(
        reference, axis=0
    )


def make_figure(x, t, clean, noisy, singular_values, eigs, modes, amps):
    lam_true = np.exp(true_continuous_eigenvalues() * DT)
    t_train_end = t[N_TRAIN - 1]
    prediction = np.real(dmd_predict(eigs, modes, amps, t.size))
    error = relative_error(prediction, clean)

    fig = plt.figure(figsize=(13, 9))
    grid = fig.add_gridspec(2, 3)
    colours = plt.get_cmap("tab10").colors

    ax = fig.add_subplot(grid[0, 0])
    limit = np.abs(noisy).max()
    shown = np.hstack([noisy[:, :N_TRAIN], prediction[:, N_TRAIN:]])
    mesh = ax.pcolormesh(
        t, x, shown, cmap="RdBu_r", vmin=-limit, vmax=limit, shading="auto"
    )
    ax.axvline(t_train_end, color="k", linewidth=1.5)
    ax.text(t_train_end * 0.5, X_MAX * 0.9, "noisy data", ha="center", fontsize=10)
    ax.text(t_train_end * 1.5, X_MAX * 0.9, "DMD forecast", ha="center", fontsize=10)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("$x$ (m)")
    ax.set_title("(a) Field $u(x,t)$: data, then forecast")
    fig.colorbar(mesh, ax=ax, label="$u$")

    ax = fig.add_subplot(grid[0, 1])
    index = np.arange(1, singular_values.size + 1)
    ax.semilogy(index, singular_values / singular_values[0], "o", color=colours[0])
    ax.axvline(RANK + 0.5, color="k", linestyle="--", linewidth=1)
    ax.text(RANK + 1, 0.5, f"$r = {RANK}$", fontsize=11)
    ax.set_xlim(0, 30)
    ax.set_xlabel("index $j$")
    ax.set_ylabel(r"$\sigma_j / \sigma_1$")
    ax.set_ylim(5e-3, 2)
    ax.set_title("(b) Singular values of $X = [x_0 \\dots x_{m-2}]$")
    ax.grid(True, which="both", alpha=0.3)

    ax = fig.add_subplot(grid[0, 2])
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="0.6", linewidth=1, label="unit circle")
    lam_all = np.concatenate([lam_true, lam_true.conj()])
    ax.plot(lam_all.real, lam_all.imag, "x", color="k", ms=10, mew=2, label="true")
    ax.plot(
        eigs.real,
        eigs.imag,
        "o",
        mfc="none",
        color=colours[1],
        ms=12,
        mew=2,
        label="DMD",
    )
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\,\lambda$")
    ax.set_ylabel(r"$\mathrm{Im}\,\lambda$")
    ax.set_title("(c) DMD eigenvalues $\\lambda_j$")
    ax.legend(loc="center", fontsize=10)
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(grid[1, 0])
    matched = match_eigenvalues(eigs, lam_true)
    omega_true = true_continuous_eigenvalues()
    for k, j in enumerate(matched):
        omega = np.log(eigs[j]) / DT
        ax.plot(omega_true[k].imag, omega_true[k].real, "x", color="k", ms=10, mew=2)
        ax.plot(omega.imag, omega.real, "o", mfc="none", color=colours[k], ms=12, mew=2)
        ax.annotate(
            f"DMD {omega.real:+.3f}\ntrue {omega_true[k].real:+.3f}",
            (omega.imag, omega.real),
            textcoords="offset points",
            xytext=(0, -38 if omega.real < omega_true[k].real else 12),
            ha="center",
            fontsize=10,
        )
    ax.axhline(0, color="0.6", linewidth=1)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.35, 0.15)
    ax.set_xlabel(r"angular frequency $\mathrm{Im}\,\omega$ (rad/s)")
    ax.set_ylabel(r"growth rate $\mathrm{Re}\,\omega$ (1/s)")
    ax.set_title(r"(d) $\omega = \ln(\lambda)/\Delta t$")
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(grid[1, 1])
    phi_true = true_spatial_modes(x)
    for k, j in enumerate(matched):
        shape_true = np.abs(phi_true[:, k]) / np.abs(phi_true[:, k]).max()
        shape_dmd = np.abs(modes[:, j]) / np.abs(modes[:, j]).max()
        ax.plot(
            x, shape_dmd, "-", color=colours[k], linewidth=2.5, label=f"mode {k + 1}"
        )
        ax.plot(x, shape_true, "--", color="k", linewidth=1.2)
    ax.plot([], [], "k--", linewidth=1.2, label="true")
    ax.set_xlabel("$x$ (m)")
    ax.set_ylabel(r"$|\phi_k(x)|$ / max")
    ax.set_title("(e) DMD mode magnitudes")
    ax.set_ylim(0, 1.35)
    ax.legend(fontsize=10, loc="upper center", ncol=4, columnspacing=0.8)
    ax.grid(True, alpha=0.3)

    ax = fig.add_subplot(grid[1, 2])
    noise_level = relative_error(noisy, clean)
    ax.semilogy(t, error, color=colours[0], label="DMD vs clean field")
    ax.semilogy(t, noise_level, color="0.5", linewidth=0.8, label="noise in data")
    ax.axvspan(0, t_train_end, color="0.9", zorder=0)
    ax.text(t_train_end * 0.5, 1.2, "training", ha="center", fontsize=10)
    ax.text(t_train_end * 1.5, 1.2, "forecast", ha="center", fontsize=10)
    ax.set_xlabel("$t$ (s)")
    ax.set_ylabel("relative $L_2$ error")
    ax.set_title("(f) Reconstruction and forecast error")
    ax.set_ylim(1e-3, 3)
    ax.legend(fontsize=10, loc="lower right")
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    return fig, error


def parse_args(argv=None):
    parser = create_parser(__doc__)
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    x = np.linspace(X_MIN, X_MAX, N_X)
    t = DT * np.arange(N_TOTAL)
    clean, noisy = make_field(x, t)
    train = noisy[:, :N_TRAIN]
    singular_values = np.linalg.svd(train[:, :-1], compute_uv=False)
    eigs, modes, amps = dmd(train, RANK)

    fig, error = make_figure(x, t, clean, noisy, singular_values, eigs, modes, amps)
    omega = np.log(eigs) / DT
    order = np.argsort(-omega.imag)
    print("continuous-time DMD eigenvalues omega = ln(lambda)/dt:")
    for value in omega[order]:
        print(f"  {value.real:+.4f} {value.imag:+.4f}i")
    print(f"mean relative error, training window: {error[:N_TRAIN].mean():.4f}")
    print(f"relative error at t = {DT * (N_TOTAL - 1):.2f} s: {error[-1]:.4f}")

    finish_figures(
        {"dynamic_mode_decomposition.png": fig},
        output=args.output,
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()
