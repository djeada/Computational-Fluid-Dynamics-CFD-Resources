"""Shared layouts for examples that visualize the same numerical quantities."""

import matplotlib.pyplot as plt


def plot_pod_mode_pairs(x, y, t, modes, coefficients, energy_fractions=None):
    """Plot spatial contours beside their amplitude-scaled temporal coefficients.

    Spatial modes have shape (len(x), len(y), n_modes); coefficients have
    shape (n_modes, len(t)). Optional energy fractions are shown in titles.
    """
    n_modes = modes.shape[-1]
    if modes.shape != (len(x), len(y), n_modes) or coefficients.shape != (
        n_modes,
        len(t),
    ):
        raise ValueError("mode and coefficient shapes must match the spatial/time axes")
    if n_modes < 1:
        raise ValueError("at least one mode is needed for plotting")
    fig, axes = plt.subplots(n_modes, 2, figsize=(12, 10), squeeze=False)
    for i, (spatial_ax, temporal_ax) in enumerate(axes):
        title = f"Mode {i + 1}"
        if energy_fractions is not None:
            title += f" ({100 * energy_fractions[i]:.1f}% TKE)"
        # Modes are signed: use a diverging map centred on zero.
        limit = abs(modes[:, :, i]).max()
        contours = spatial_ax.contourf(
            x, y, modes[:, :, i].T, cmap="RdBu_r", levels=41, vmin=-limit, vmax=limit
        )
        fig.colorbar(contours, ax=spatial_ax, label=rf"$\phi_{i + 1}$ [-]")
        spatial_ax.set(xlabel="x [mm]", ylabel="y [mm]", title=title)
        temporal_ax.plot(t, coefficients[i], color="tab:blue")
        temporal_ax.axhline(0.0, color="0.6", lw=0.8)
        temporal_ax.grid(alpha=0.3)
        temporal_ax.set(xlabel="t [s]", ylabel=f"$a_{i + 1}(t)$", title=title)
    fig.tight_layout()
    return fig
