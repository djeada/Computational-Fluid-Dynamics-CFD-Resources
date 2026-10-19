# Contributing

Thanks for helping improve this repository. Corrections, new notes, new scripts, and fixes to existing material are all welcome. This guide describes the layout, the conventions each kind of file follows, and the checks that run on every pull request.

## Repository layout

| Path | Contents |
| --- | --- |
| `notes/` | Theory notes in Markdown, grouped by subject (`fluid_mechanics`, `numerical`, `machine_learning`, `applied_mechanics`) |
| `practice/` | Tool guides and worked projects (Gmsh, ParaView, OpenFOAM, meshing) |
| `scripts/algorithms/`, `scripts/plots/`, `scripts/simulations/` | One folder per Python script, each with `main.py` and `README.md` |
| `tests/` | Numerical correctness, import safety, figure ownership, and runner tests |
| `scripts/_numerics.py`, `scripts/_plotting.py`, `scripts/_common.py` | Shared computation, plotting layouts, and CLI/output helpers |
| `scripts/_animation.py` | Base classes and runner shared by every simulation: window, headless run, PNG, and reel |
| `tools/` | Maintenance scripts used locally and in CI, plus `make_reels.py` for Shorts/Reels videos |
| `ROADMAP.md` | Topics that are planned but not written yet |

## Setting up

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Checks

Run these before opening a pull request. CI runs the same commands.

```bash
python tools/check_links.py          # every relative link and image resolves
python tools/generate_index.py       # refresh the counts and script index in README.md
python tools/sync_related_scripts.py # add "Related Scripts" links to notes from script READMEs
ruff check scripts tools tests             # correctness, imports, and modern Python syntax
ruff format --check scripts tools tests    # consistent formatting
python -m unittest discover -s tests -v # numerical and runtime regression tests
python tools/run_scripts.py          # run every script headless (or pass a name filter)
```

## Script conventions

Each script lives in its own folder: `scripts/<category>/<name>/main.py` with a `README.md` next to it.

### Code

- Start the file with a module docstring that says what the script demonstrates.

- Put computation in functions or explicit solver state classes. Do not run anything at import time; end the file with:

  ```python
  if __name__ == "__main__":
      main()
  ```

- Use `create_parser(__doc__)` from `scripts/_common.py` for shared CLI options and `finish_figures({"name.png": fig}, output=args.output, show=not args.no_show)` for static examples. Reuse the POD implementation in `scripts/_numerics.py` with spatial points in rows and snapshots in columns. The examples add the `scripts/` directory to the import path so direct execution works from any working directory without installing a package.

- `main(argv=None)` parses arguments with `argparse` and supports these flags:

  | Flag | Required | Behaviour |
  | --- | --- | --- |
  | `--no-show` | always | Do not open a window |
  | `--output DIR` | always | Create `DIR` and save every figure as a PNG in it (`dpi=100`, `bbox_inches="tight"`). Simulations save their final frame |
  | `--steps N` | time-stepping, animated, or interactive scripts | Use `type=positive_int` for a positive iteration/frame count. In simulations it always counts animation frames |
  | `--reel FILE`, `--reel-seconds S`, `--reel-fps FPS` | simulations (added by `Animation.parser`) | Render a 1080 × 1920 MP4 for YouTube Shorts or Instagram Reels instead of opening a window |

  Running with no flags keeps the original interactive behaviour.

- With `--no-show --output DIR --steps 10`, a script must finish in well under a minute on a laptop.

- Never use absolute paths. Resolve input files relative to the script with `Path(__file__).parent`.

- Simulations follow the pattern in [`scripts/README.md`](scripts/README.md#simulations), with [`lid_driven_cavity`](scripts/simulations/lid_driven_cavity/main.py) as the reference:
  - a `Simulation` subclass whose `step()` performs one solver iteration and works without a figure;
  - a `View` subclass whose `draw()` updates its artists from the state without advancing it, and which also arranges its panels for the tall reel frame (`portrait=True`);
  - a module-level `ANIMATION = Animation(...)` used by `main` through `ANIMATION.parser(__doc__)` and `ANIMATION.run(...)`.

  Views use the figure they are given rather than `pyplot`, leave colours to the shared dark style, and keep the figure title free for the runner's title and status line. Check a new simulation's reel with `python main.py --reel reel.mp4 --reel-seconds 10` as well as its PNG.

- Test numerical changes against reconstruction identities, analytical solutions, or conservation laws. A successful PNG export alone does not establish numerical correctness.

- Seed random number generators so the output is reproducible.

- Keep physical parameters as named constants or function arguments with units in a comment.

### README

Script READMEs use these sections, in this order:

1. `# Title` and a one-paragraph description. The first sentence is used in the main README index, so make it stand alone.
2. `## Overview`: what the script does, as bullets. Every bullet must be true of the code.
3. `## Mathematical Background`: the equations the code implements.
4. `## Implementation`: how the code is structured, naming the real functions and parameters.
5. `## Usage`: the commands to run it, including the flags above.
6. `## Output`: what the figure shows, with the image embedded.
7. `## Related Notes`: relative links to the notes in `notes/` that explain the theory.

If the output image is not already hosted, generate it with `python main.py --no-show --output .` (plus a suitable `--steps`) and commit the PNG next to the script.

## Note conventions

- Math must render on GitHub, which reads the TeX inside `$` and `$$` as Markdown before rendering it:
  - put `$$` display math on its own lines with a blank line before and after;
  - write display math as a ` ```math ` fence instead when it sits in a list item or a `<details>` block, or holds an escape such as `\,`, `\{` or `\%`, or two `*`: GitHub would drop the backslashes and turn `T^*` and `p^*` into `T^_` and `p^_`;
  - write inline math as `` $`...`$ `` when GitHub would not render `$...$` as written: it holds an escape such as `\,`, a `*` or `_` pairs with another in the same paragraph (`$\mathbf{u}_i$ ... $u_{j}$`), the `$` does not follow a space or `(` (`moderate-$Re$`), or it sits inside `*italics*` or link text;
  - write degrees as `^\circ` inside math, not `°`;
  - put spaces around `<` and `>` in inline math (`$a < b$`);
  - use LaTeX commands rather than Unicode symbols inside math, and `\mathrm{...}` rather than `\operatorname{...}`, which GitHub does not allow.
- [marklign](https://github.com/djeada/marklign) applies the `$$`, fence and `` $`...`$ `` rules for you: run `marklign notes practice` before opening a pull request.
- End each note with these sections, at the same heading level as the note's other top-level sections:
  - **Related Scripts**: links to scripts in `scripts/` that demonstrate the topic (omit if none).
  - **Exercises**: three to five problems of increasing difficulty, each with a worked answer inside a `<details><summary>Answer</summary> ... </details>` block. Check numerical answers by computing them.
  - **References**: textbooks, papers, or stable online resources. Cite only works you can verify, with authors, title, edition or year, and publisher or venue.
- Link only to files that exist. Put planned topics in `ROADMAP.md` instead of linking to pages that have not been written.

## Pull requests

1. Fork the repository and create a branch (`git checkout -b fix/short-description`).
2. Make focused commits with clear messages.
3. Run the checks above.
4. Open a pull request describing what changed and how you verified it (for example, "compared with the analytical solution" or "ran the script and checked the plot").

Technical corrections should cite a source or show the derivation. By contributing you agree that your work is released under the repository's [MIT License](LICENSE).
