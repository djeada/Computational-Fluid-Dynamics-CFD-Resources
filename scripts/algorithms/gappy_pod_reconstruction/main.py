"""Gappy POD: reconstruct wake snapshots from gappy data and from point sensors.

A POD basis is built from complete snapshots of a synthetic cylinder-wake
transverse velocity field. Held-out snapshots taken later in time are then
reconstructed from (a) 50 % of their points, chosen at random, and (b) a few
point sensors placed at random or by QR factorization with column pivoting of
the POD basis. The figure compares true, gappy and reconstructed fields and
plots the reconstruction error against the number of sensors and modes. The
iterative Everson-Sirovich procedure, which builds the basis itself from gappy
snapshots, is also run and its error is plotted per iteration.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import qr

# Allow execution with `python main.py` from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import create_parser, finish_figures  # noqa: E402
from _numerics import compute_pod  # noqa: E402

# Wake model (lengths in cylinder diameters D, velocities in U_inf); the same
# model as scripts/plots/pod_energy_and_truncation, here on a uniform grid.
STROUHAL = 0.2  # shedding Strouhal number f D / U_inf [-]
CONVECTION_SPEED = 0.8  # convection speed of the vortices / U_inf [-]
ENVELOPE_PEAK = 4.0  # x/D at which the fluctuation amplitude peaks [-]
HARMONICS = ((1.0, 1), (0.35, 2), (0.15, 3))  # (amplitude [-], harmonic number)
N_BROADBAND = 30  # number of random small-scale travelling structures
BROADBAND_AMPLITUDE = 0.22  # amplitude of the first one; the j-th has A j^-1/2 [-]
NOISE_STD = 0.01  # measurement noise [-]
SEED = 1

X_RANGE = (1.0, 11.0)  # streamwise extent [D]
Y_RANGE = (-3.0, 3.0)  # cross-stream extent [D]
N_X, N_Y = 120, 48
N_TRAIN = 200  # complete snapshots used to build the basis
DT = 0.2  # time between training snapshots [D / U_inf]
N_TEST = 20  # held-out snapshots, at random times in TEST_WINDOW
TEST_WINDOW = (40.0, 60.0)  # [D / U_inf], after the training record

RANK = 10  # modes used for the reconstructions
GAP_FRACTION = 0.5  # fraction of points removed in the gappy test
N_SENSORS_SHOWN = 20  # sensors in the field panels
SENSOR_COUNTS = (10, 11, 12, 14, 17, 20, 25, 30, 40, 60, 80, 120)
N_RANDOM_DRAWS = 50  # random sensor layouts per sensor count
RANKS = tuple(range(1, 41))
SENSORS_FOR_RANK_SWEEP = 30
TRAIN_GAP_FRACTION = 0.3  # fraction of missing points in the iterative test
N_ITERATIONS = 10


def wake_components(seed=SEED):
    """Return the travelling structures as (amplitude, wavenumber, omega, phase, shape)."""
    rng = np.random.default_rng(seed)
    omega = 2.0 * np.pi * STROUHAL  # shedding angular frequency [U_inf / D]
    k = omega / CONVECTION_SPEED  # wavenumber of the vortex street [1 / D]
    profiles = (
        lambda eta: np.exp(-(eta**2)),
        lambda eta: 2.0 * eta * np.exp(-(eta**2)),
        lambda eta: (1.0 - 2.0 * eta**2) * np.exp(-(eta**2)),
    )
    components = [(amp, h * k, h * omega, 0.0, profiles[h - 1]) for amp, h in HARMONICS]
    for j in range(N_BROADBAND):
        k_j = k * rng.uniform(1.5, 6.0)
        centre, width = rng.uniform(-1.0, 1.0), rng.uniform(0.3, 0.8)
        components.append(
            (
                BROADBAND_AMPLITUDE / np.sqrt(j + 1),
                k_j,
                CONVECTION_SPEED * k_j,
                rng.uniform(0.0, 2.0 * np.pi),
                lambda eta, c=centre, s=width: np.exp(-(((eta - c) / s) ** 2)),
            )
        )
    return components


def wake_snapshots(x, y, t, seed=SEED, noise_std=NOISE_STD, noise_seed=None):
    """Return the N x M matrix of v / U_inf, points (x slowest) in rows."""
    X, Y = np.meshgrid(x, y, indexing="ij")
    envelope = (X / ENVELOPE_PEAK) * np.exp(1.0 - X / ENVELOPE_PEAK)
    eta = Y / (0.5 + 0.1 * X)
    data = np.zeros((X.size, t.size))
    for amp, k, omega, phase, shape in wake_components(seed):
        spatial = (amp * envelope * shape(eta)).ravel()
        data += np.outer(spatial * np.cos(k * X.ravel() + phase), np.cos(omega * t))
        data += np.outer(spatial * np.sin(k * X.ravel() + phase), np.sin(omega * t))
    rng = np.random.default_rng(seed + 1000 if noise_seed is None else noise_seed)
    return data + noise_std * rng.standard_normal(data.shape)


def gappy_coefficients(modes, mean, values, observed):
    """Least-squares POD coefficients from the observed entries of one snapshot.

    Solves min_a || D (u - mean - Phi a) ||, i.e. the normal equations
    (Phi^T D Phi) a = Phi^T D (u - mean) with the diagonal 0/1 mask D, using the
    rows of Phi at the observed points. ``observed`` is a boolean mask or an
    index array; ``values`` holds the snapshot at all points or only at the
    observed points. With fewer observations than modes the minimum-norm
    solution is returned.
    """
    rows = modes[observed]
    data = values if values.shape[0] == rows.shape[0] else values[observed]
    coeffs, *_ = np.linalg.lstsq(rows, data - mean[observed], rcond=None)
    return coeffs


def gappy_reconstruct(modes, mean, values, observed):
    """Full-field estimate mean + Phi a from the observed entries."""
    return mean + modes @ gappy_coefficients(modes, mean, values, observed)


def qr_sensors(modes, n_sensors):
    """Sensor indices from QR pivoting of Phi_r^T, then greedy oversampling.

    The first min(r, p) sensors are the leading column pivots of Phi_r^T. Each
    further sensor is the point that maximizes det(Theta^T Theta) when its row
    phi_i of Phi_r is appended to Theta, i.e. the point with the largest
    phi_i^T (Theta^T Theta)^{-1} phi_i.
    """
    n_points, rank = modes.shape
    if not 1 <= n_sensors <= n_points:
        raise ValueError("n_sensors must be between one and the number of points")
    _, _, pivots = qr(modes.T, mode="economic", pivoting=True)
    chosen = list(pivots[: min(rank, n_sensors)])
    available = np.ones(n_points, dtype=bool)
    available[chosen] = False
    while len(chosen) < n_sensors:
        theta = modes[chosen]
        inverse = np.linalg.inv(theta.T @ theta)
        scores = np.einsum("ij,jk,ik->i", modes, inverse, modes)
        scores[~available] = -np.inf
        best = int(np.argmax(scores))
        chosen.append(best)
        available[best] = False
    return np.array(chosen)


def random_sensors(n_points, n_sensors, rng):
    """Indices of n_sensors distinct points chosen uniformly at random."""
    return rng.choice(n_points, size=n_sensors, replace=False)


def relative_error(estimate, truth, mean):
    """|| estimate - truth ||_F / || truth - mean ||_F over all given snapshots."""
    return np.linalg.norm(estimate - truth) / np.linalg.norm(truth - mean)


def reconstruct_all(modes, mean, truth, observed):
    """Reconstruct every column of ``truth`` from its observed points.

    ``observed`` is either one index array shared by all snapshots (fixed
    sensors, solved as one least-squares problem with many right-hand sides)
    or a list with one boolean mask per snapshot.
    """
    if isinstance(observed, np.ndarray):
        return gappy_reconstruct(modes, mean, truth, observed)
    return np.column_stack(
        [
            gappy_reconstruct(modes, mean[:, 0], truth[:, j], obs)
            for j, obs in enumerate(observed)
        ]
    )


def iterative_gappy_pod(data, observed, rank, n_iter, truth=None):
    """Everson-Sirovich gap filling: build a POD basis from gappy snapshots.

    Missing entries (``observed`` False) are first filled with the mean of the
    observed values at that point. Each iteration computes the POD of the
    filled data, re-estimates every snapshot from its observed entries with
    ``rank`` modes, and replaces only the missing entries. Returns the filled
    matrix, the final POD and, if ``truth`` is given, the relative error of the
    filled entries after each iteration (index 0 is the initial mean fill).
    """
    counts = observed.sum(axis=1)
    if np.any(counts == 0):
        raise ValueError("every point must be observed in at least one snapshot")
    point_mean = np.where(observed, data, 0.0).sum(axis=1) / counts
    filled = np.where(observed, data, point_mean[:, None])
    missing = ~observed
    errors = []

    def record():
        if truth is not None:
            scale = np.linalg.norm((truth - truth.mean(axis=1, keepdims=True))[missing])
            errors.append(np.linalg.norm((filled - truth)[missing]) / scale)

    record()
    for _ in range(n_iter):
        pod = compute_pod(filled)
        modes, mean = pod.modes[:, :rank], pod.mean[:, 0]
        for j in range(data.shape[1]):
            estimate = gappy_reconstruct(modes, mean, filled[:, j], observed[:, j])
            filled[missing[:, j], j] = estimate[missing[:, j]]
        record()
    return filled, compute_pod(filled), errors


def run_experiments(seed=SEED):
    """Compute every quantity shown in the figure and return them in a dict."""
    rng = np.random.default_rng(seed + 7)
    x = np.linspace(*X_RANGE, N_X)
    y = np.linspace(*Y_RANGE, N_Y)
    train = wake_snapshots(x, y, DT * np.arange(N_TRAIN), seed)
    t_test = np.sort(rng.uniform(*TEST_WINDOW, N_TEST))
    test = wake_snapshots(x, y, t_test, seed, noise_seed=seed + 2000)
    pod = compute_pod(train)
    mean = pod.mean
    n_points = train.shape[0]
    modes = pod.modes[:, :RANK]

    full = mean + modes @ (modes.T @ (test - mean))
    gap_masks = [rng.random(n_points) >= GAP_FRACTION for _ in range(N_TEST)]
    gappy = reconstruct_all(modes, mean, test, gap_masks)

    shown_qr = qr_sensors(modes, N_SENSORS_SHOWN)
    shown_random = random_sensors(n_points, N_SENSORS_SHOWN, rng)
    qr_field = gappy_reconstruct(modes, mean[:, 0], test[:, 0], shown_qr)
    random_field = gappy_reconstruct(modes, mean[:, 0], test[:, 0], shown_random)

    qr_errors, random_errors = [], []
    for p in SENSOR_COUNTS:
        sensors = qr_sensors(modes, p)
        qr_errors.append(
            relative_error(reconstruct_all(modes, mean, test, sensors), test, mean)
        )
        draws = []
        for _ in range(N_RANDOM_DRAWS):
            sensors = random_sensors(n_points, p, rng)
            draws.append(
                relative_error(reconstruct_all(modes, mean, test, sensors), test, mean)
            )
        random_errors.append(draws)

    rank_full, rank_gappy, rank_qr = [], [], []
    for r in RANKS:
        basis = pod.modes[:, :r]
        rank_full.append(
            relative_error(mean + basis @ (basis.T @ (test - mean)), test, mean)
        )
        rank_gappy.append(
            relative_error(reconstruct_all(basis, mean, test, gap_masks), test, mean)
        )
        sensors = qr_sensors(basis, SENSORS_FOR_RANK_SWEEP)
        rank_qr.append(
            relative_error(reconstruct_all(basis, mean, test, sensors), test, mean)
        )

    train_observed = rng.random(train.shape) >= TRAIN_GAP_FRACTION
    _, gappy_pod, fill_errors = iterative_gappy_pod(
        np.where(train_observed, train, np.nan),
        train_observed,
        RANK,
        N_ITERATIONS,
        truth=train,
    )
    gappy_basis = gappy_pod.modes[:, :RANK]
    test_from_gappy_basis = relative_error(
        reconstruct_all(gappy_basis, gappy_pod.mean, test, gap_masks), test, mean
    )

    return dict(
        x=x,
        y=y,
        test=test,
        mean=mean,
        energy=np.cumsum(pod.energy_fractions),
        full=full,
        gappy=gappy,
        gap_mask=gap_masks[0],
        shown_qr=shown_qr,
        shown_random=shown_random,
        qr_field=qr_field,
        random_field=random_field,
        qr_errors=np.array(qr_errors),
        random_errors=np.array(random_errors),
        rank_full=np.array(rank_full),
        rank_gappy=np.array(rank_gappy),
        rank_qr=np.array(rank_qr),
        fill_errors=np.array(fill_errors),
        test_from_gappy_basis=test_from_gappy_basis,
        cond_qr=np.linalg.cond(modes[shown_qr]),
        cond_random=np.linalg.cond(modes[shown_random]),
    )


def plot_results(res):
    x, y = res["x"], res["y"]
    shape = (x.size, y.size)
    truth = res["test"][:, 0]
    limit = np.abs(truth).max()
    mean = res["mean"]

    def err(field):
        return 100 * relative_error(field, truth, mean[:, 0])

    gappy_field = np.where(res["gap_mask"], truth, np.nan)
    fig = plt.figure(figsize=(13, 9.5), layout="constrained")
    grid = fig.add_gridspec(3, 3, height_ratios=(1.0, 1.0, 1.5))
    fields = [
        ("(a) held-out snapshot", truth),
        (f"(b) {100 * GAP_FRACTION:.0f} % of points removed", gappy_field),
        (
            f"(c) gappy POD, r = {RANK}, error {err(res['gappy'][:, 0]):.0f} %",
            res["gappy"][:, 0],
        ),
        (f"(d) {N_SENSORS_SHOWN} sensors: QR (black), random (green)", truth),
        (f"(e) from QR sensors, error {err(res['qr_field']):.0f} %", res["qr_field"]),
        (
            f"(f) from random sensors, error {err(res['random_field']):.0f} %",
            res["random_field"],
        ),
    ]
    X, Y = np.meshgrid(x, y, indexing="ij")
    for n, (title, values) in enumerate(fields):
        ax = fig.add_subplot(grid[n // 3, n % 3])
        ax.set_facecolor("0.75")
        mesh = ax.pcolormesh(
            x,
            y,
            values.reshape(shape).T,
            cmap="RdBu_r",
            vmin=-limit,
            vmax=limit,
            shading="nearest",
        )
        if n == 3:
            for idx, marker, color in (
                (res["shown_qr"], "o", "black"),
                (res["shown_random"], "^", "tab:green"),
            ):
                ax.plot(
                    X.ravel()[idx],
                    Y.ravel()[idx],
                    marker,
                    color=color,
                    ms=6,
                    mfc="none",
                    mew=1.8,
                )
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("x / D")
        if n % 3 == 0:
            ax.set_ylabel("y / D")
        ax.set_aspect("equal")
    fig.colorbar(
        mesh, ax=fig.axes, shrink=0.5, location="right", label=r"$v / U_\infty$ [-]"
    )

    ax = fig.add_subplot(grid[2, 0])
    counts = np.array(SENSOR_COUNTS)
    lo, med, hi = np.percentile(res["random_errors"], (10, 50, 90), axis=1)
    ax.fill_between(
        counts, lo, hi, color="tab:green", alpha=0.25, label="random, 10-90 %"
    )
    ax.loglog(counts, med, "^-", color="tab:green", label="random, median")
    ax.loglog(counts, res["qr_errors"], "o-", color="black", label="QR pivoting")
    ax.axhline(
        res["rank_full"][RANK - 1],
        color="tab:blue",
        ls="--",
        label="full-data projection",
    )
    ax.set_xlabel("number of sensors p")
    ax.set_ylabel("relative error [-]")
    ax.set_title(f"(g) error vs sensors, r = {RANK}")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.3, which="both")

    ax = fig.add_subplot(grid[2, 1])
    ranks = np.array(RANKS)
    ax.semilogy(
        ranks, res["rank_full"], "-", color="tab:blue", label="full-data projection"
    )
    ax.semilogy(
        ranks,
        res["rank_gappy"],
        "--",
        color="tab:orange",
        label=f"{100 * GAP_FRACTION:.0f} % random gaps",
    )
    ax.semilogy(
        ranks,
        res["rank_qr"],
        "o-",
        ms=3,
        color="black",
        label=f"{SENSORS_FOR_RANK_SWEEP} QR sensors",
    )
    ax.set_xlabel("number of modes r")
    ax.set_ylabel("relative error [-]")
    ax.set_title("(h) error vs modes")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(alpha=0.3, which="both")

    ax = fig.add_subplot(grid[2, 2])
    iterations = np.arange(res["fill_errors"].size)
    ax.plot(iterations, res["fill_errors"], "o-", color="tab:purple")
    ax.set_xlabel("iteration")
    ax.set_ylabel("relative error of filled entries [-]")
    ax.set_title(f"(i) Everson-Sirovich, {100 * TRAIN_GAP_FRACTION:.0f} % gaps")
    ax.set_ylim(0, 1.05 * res["fill_errors"].max())
    ax.set_xticks(iterations[::2])
    ax.grid(alpha=0.3)
    return fig


def main(argv=None):
    parser = create_parser(__doc__)
    args = parser.parse_args(argv)

    res = run_experiments()
    print(
        f"Basis: {N_TRAIN} complete snapshots, {N_X * N_Y} points; r = {RANK} "
        f"modes hold {100 * res['energy'][RANK - 1]:.1f} % of the energy"
    )
    print(f"Test-set error, full-data projection: {res['rank_full'][RANK - 1]:.3f}")
    print(
        f"Test-set error, {100 * GAP_FRACTION:.0f} % random gaps: "
        f"{relative_error(res['gappy'], res['test'], res['mean']):.3f}"
    )
    print(
        f"Condition number of Phi at {N_SENSORS_SHOWN} sensors: "
        f"QR {res['cond_qr']:.1f}, random {res['cond_random']:.1f}"
    )
    for p, e_qr, draws in zip(SENSOR_COUNTS, res["qr_errors"], res["random_errors"]):
        print(f"p = {p:3d}: QR {e_qr:.3f}, random median {np.median(draws):.3f}")
    best = int(np.argmin(res["rank_qr"]))
    print(
        f"With {SENSORS_FOR_RANK_SWEEP} QR sensors the error is lowest at "
        f"r = {RANKS[best]} ({res['rank_qr'][best]:.3f})"
    )
    print(
        f"Everson-Sirovich filled-entry error: {res['fill_errors'][0]:.3f} (mean fill)"
        f" -> {res['fill_errors'][-1]:.3f} after {N_ITERATIONS} iterations"
    )
    print(
        f"Test-set error with the basis built from gappy data: "
        f"{res['test_from_gappy_basis']:.3f}"
    )

    fig = plot_results(res)
    finish_figures(
        {"gappy_pod_reconstruction.png": fig}, output=args.output, show=not args.no_show
    )


if __name__ == "__main__":
    main()
