# Python examples

Each example lives in `algorithms/`, `plots/`, or `simulations/`, with its own `main.py`, explanation, and output image. Run examples directly from their folders or by passing their full path from the repository root.

```bash
python scripts/algorithms/pod/main.py --no-show --output results/pod
python scripts/simulations/2d_wave_simulation/main.py --no-show --steps 45 --output results/wave
```

All examples accept `--no-show` and `--output DIR`. Iterative examples also accept a positive `--steps N`; check `--help` for whether one step means an iteration or an animation frame containing several iterations.

## Shared code

| Module | Responsibility |
| --- | --- |
| [_common.py](_common.py) | CLI options, PNG export, and static figure cleanup |
| [_numerics.py](_numerics.py) | POD by SVD or snapshot eigendecomposition, field generation, and reconstruction |
| [_plotting.py](_plotting.py) | Paired POD spatial contours and temporal coefficient plots |

POD uses one matrix convention: spatial points are rows and time snapshots are columns. The returned spatial modes have unit norm; temporal coefficients include singular-value amplitudes. `result.modes @ result.coefficients + result.mean` reconstructs the data. Numerical null modes are discarded; a constant field has no fluctuation modes.

Static examples return figures from their plotting functions and use `finish_figures` to save, display, and close them. The helper closes only the supplied figures, including when export fails.

## Simulation state

The heat/wave, 2D wave, Schrödinger, cavity, and lattice Boltzmann examples expose state classes with `advance(steps)`. Their numerical state can be initialized and advanced without creating figures. Constructors accept grid parameters for smaller experiments and tests. `advance` counts numerical iterations; the CLI retains each example's documented frame grouping.

Animation callbacks advance the state and redraw it. Initialization callbacks draw without advancing. Headless runs advance the requested iterations in a batch and render the final state once.

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

Tests check reconstruction and orthonormality, analytical heat and wave solutions, Schrödinger probability and phase, cavity wall conditions, LBM density and momentum, animation step counts, import safety, and figure ownership. Headless smoke runs exercise all examples but do not replace numerical correctness tests.
