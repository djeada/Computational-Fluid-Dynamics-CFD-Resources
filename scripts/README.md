# Python examples

Each example lives in `algorithms/`, `plots/`, or `simulations/`, with its own `main.py`, explanation, and output image. Run examples directly from their folders or by passing their full path from the repository root.

```bash
python scripts/algorithms/pod/main.py --no-show --output results/pod
python scripts/simulations/2d_wave_simulation/main.py --no-show --steps 45 --output results/wave
```

All examples accept `--no-show` and `--output DIR`. Iterative plot and algorithm examples also accept a positive `--steps N`. Every simulation shares one command line: `--steps N` counts animation frames (`--help` says how many solver iterations make one frame), and `--reel FILE` renders a vertical video for YouTube Shorts or Instagram Reels.

## Shared code

| Module | Responsibility |
| --- | --- |
| [_common.py](_common.py) | CLI options, PNG export, and static figure cleanup |
| [_animation.py](_animation.py) | Simulation state and view base classes, the live window, headless runs, and reel export |
| [_numerics.py](_numerics.py) | POD by SVD or snapshot eigendecomposition, field generation, and reconstruction |
| [_plotting.py](_plotting.py) | Paired POD spatial contours and temporal coefficient plots |

POD uses one matrix convention: spatial points are rows and time snapshots are columns. The returned spatial modes have unit norm; temporal coefficients include singular-value amplitudes. `result.modes @ result.coefficients + result.mean` reconstructs the data. Numerical null modes are discarded; a constant field has no fluctuation modes.

Static examples return figures from their plotting functions and use `finish_figures` to save, display, and close them. The helper closes only the supplied figures, including when export fails.

## Simulations

Every script in `simulations/` has the same three parts, built on [_animation.py](_animation.py):

| Part | Role |
| --- | --- |
| `<Name>Simulation(Simulation)` | Numerical state. `step()` performs one solver iteration; `advance(n)` repeats it, counts `steps`, and stops early once `done` (for solvers that converge or finish). Constructors accept grid sizes and seeds for small experiments and tests. Anything plotted over time, such as energy histories, trajectories, or residuals, is part of the state. |
| `<Name>View(View)` | Builds its axes on the figure it is given and updates them from the state in `draw()`, which never advances the solver. `status()` returns the one-line progress shown next to the title. With `portrait=True` it arranges its panels for the tall reel frame. |
| `ANIMATION = Animation(...)` | Title, reel subtitle, PNG name, default number of frames, and solver iterations per frame. `ANIMATION.parser(__doc__)` builds the shared command line and `ANIMATION.run(args, simulation, View)` runs it. |

Because a view only reads the state, the window, the `--output` PNG, and the reel show the same picture for the same state. All simulations use one dark Matplotlib style. In the window, space pauses or resumes and the right arrow advances one frame while paused. Real-time demos (`endless=True`) keep running until the window is closed; headless runs and reels always stop after `--steps` frames.

### Shorts and Reels

```bash
python scripts/simulations/kelvin_helmholtz_instability/main.py --reel reels/kh.mp4
python scripts/simulations/lid_driven_cavity/main.py --reel reels/cavity.mp4 --compare-ghia --reel-seconds 20
python tools/make_reels.py                          # every simulation into reels/
python tools/make_reels.py cavity kelvin --seconds 20 --jobs 2
```

A reel is a 1080 × 1920 H.264 MP4 (yuv420p, `+faststart`) at `--reel-fps` frames per second (30 by default). The title and subtitle sit in the top band and the status line and a progress bar sit below the panel, clear of the app overlays at the top and bottom of the screen. The run set by `--steps` is spread over about `--reel-seconds` (30 by default) with the same whole number of solver iterations in every video frame, so motion plays at a steady speed; rounding that number sets the exact length. The last frame is held for 2 s. A run with fewer solver iterations than video frames gives a shorter video rather than repeated frames. Rendering needs `ffmpeg`, either on the `PATH` or from the `imageio-ffmpeg` package in `requirements.txt`. `tools/make_reels.py` renders several simulations in parallel and passes arguments after `--` to every script.

## Run and inspect examples

From the repository root:

```bash
python tools/run_scripts.py --list
python tools/run_scripts.py pod --jobs 2
python tools/run_scripts.py --jobs 4 --output results --json-report results/report.json
python -m unittest discover -s tests -v
ruff check scripts tools tests
ruff format --check scripts tools tests
```

The runner checks `--help`, runs examples with headless backends, validates PNG contents, and reports results as they finish. Its timeout covers discovery and execution together. The default worker count is capped at four, and each subprocess uses one BLAS thread.

Without `--output`, generated files are temporary. With `--output`, each invocation gets a new `run-*` folder so existing results remain intact. The JSON report includes each example's status, duration, and complete captured log, plus the retained output directory.

Tests check reconstruction and orthonormality, analytical heat and wave solutions, Schrödinger probability and phase, cavity wall conditions, LBM density and momentum, import safety, and figure ownership. They also check that every simulation follows the shared pattern, that its view draws in both layouts without advancing the solver, and that the runner splits reels into frames correctly and writes a valid MP4. Headless smoke runs exercise all examples, and CI renders a two-second reel of every simulation, but neither replaces numerical correctness tests.
