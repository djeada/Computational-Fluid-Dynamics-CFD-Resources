# Fatigue: S–N Curve, Haigh Diagram and Miner's Rule

This script builds the S–N curve of a machined steel shaft from Marin factors, draws the Goodman, Gerber and Soderberg lines with an operating point, and sums the Miner damage of a rainflow-counted random stress history. It follows the stress-life procedure of Budynas and Nisbett for a 30 mm shaft with $S_{ut} = 600$ MPa: endurance limit, finite-life line, mean-stress correction and safety factor, then rainflow counting (ASTM E1049) and the Palmgren–Miner damage sum for a variable-amplitude block.

## Overview

- Computes the Marin factors (machined surface, 30 mm diameter in rotating bending, 90% reliability) and the specimen and component endurance limits $`S'_e = 0.5S_{ut}`$ and $S_e$.
- Estimates the fraction $f$ of $S_{ut}$ reached at $10^3$ cycles and draws the S–N lines through $(10^3, fS_{ut})$ and $(10^6, S_e)$, with the endurance limit beyond, for the specimen and the shaft; marks the life at a fully reversed amplitude of 250 MPa.
- Draws the Goodman, Gerber, Soderberg and Langer yield lines in the $\sigma_m$–$`\sigma_a`$ plane, with the operating point $(\sigma_m, \sigma_a) = (150, 100)$ MPa, its radial load line and its safety factor under each criterion.
- Generates a seeded block of 400 alternating peaks and valleys with a mean of 60 MPa, rainflow-counts it as a repeating block, converts every cycle to a Goodman-equivalent fully reversed amplitude, and sums the Miner damage.
- Shows the first 60 reversals and a histogram of counted cycles with the share of damage from each amplitude bin.

## Mathematical Background

### Endurance Limit and S–N Line

With $S_{ut}$ in MPa,

```math
S_e = k_a k_b k_c k_d k_e\,S'_e, \qquad k_a = 4.51\,S_{ut}^{-0.265}, \qquad k_b = 1.24\,d^{-0.107}, \qquad k_e = 0.897
```

and $k_c = k_d = 1$. The fraction $f$ uses the estimate $`\sigma'_F = S_{ut} + 345`$ MPa: $`b_F = -\log_{10}(\sigma'_F/S'_e)/\log_{10}(2 \times 10^6)`$ and $`f = (\sigma'_F/S_{ut})(2 \times 10^3)^{b_F}`$. The finite-life line $`S_f = aN^b`$ through $`(10^3, fS_{ut})`$ and $(10^6, S_e)$ has

```math
a = \frac{(fS_{ut})^2}{S_e}, \qquad b = -\frac{1}{3}\log_{10}\frac{fS_{ut}}{S_e}, \qquad N = \left(\frac{\sigma_{ar}}{a}\right)^{1/b}
```

and the life is taken as infinite for $\sigma_{ar} \le S_e$.

### Mean-Stress Criteria

Along a radial load line the safety factors are $n = (\sigma_a/S_e + \sigma_m/S_{ut})^{-1}$ (Goodman), $n = (\sigma_a/S_e + \sigma_m/S_y)^{-1}$ (Soderberg), $n = S_y/(\sigma_a + \sigma_m)$ (Langer), and for Gerber

```math
n = \frac{1}{2}\left(\frac{S_{ut}}{\sigma_m}\right)^2\frac{\sigma_a}{S_e}\left[-1 + \sqrt{1 + \left(\frac{2\sigma_m S_e}{S_{ut}\sigma_a}\right)^2}\right]
```

The Goodman-equivalent fully reversed amplitude of a cycle is $\sigma_{ar} = \sigma_a/(1 - \sigma_m/S_{ut})$, with compressive means set to zero.

### Rainflow Counting and Miner's Rule

The three-point algorithm of ASTM E1049 keeps a stack of reversals. With $X$ the range of the last two points and $Y$ the range of the two before, a range $Y \le X$ is counted as a half cycle if it contains the first point of the stack and as a full cycle otherwise, and its points are removed; the ranges left at the end are half cycles. A repeating block is first rotated to start and end at its largest peak, so all cycles close. The damage is

```math
D = \sum_i \frac{n_i}{N_i(\sigma_{ar,i})}
```

and the life is $1/D$ blocks.

## Implementation

- `marin_factors`, `endurance_limits`, `fatigue_strength_fraction`, `basquin_constants`, `fatigue_strength` and `cycles_to_failure` implement the stress-life model.
- `safety_goodman`, `safety_gerber`, `safety_soderberg`, `safety_yield` and `goodman_equivalent_amplitude` implement the mean-stress criteria.
- `turning_points(series)` keeps the reversals; `rainflow(series, repeating=False)` returns `(range, mean, count)` tuples; `miner_damage(cycles, s_e)` returns the damage sum and the per-cycle amplitudes, counts and damage; `random_history(n, seed)` generates the block.
- `plot_sn`, `plot_haigh`, `plot_history` and `plot_damage` draw the four panels.
- Constants: `S_UT` = 600 MPa, `S_Y` = 450 MPa, `DIAMETER` = 30 mm, `SURFACE_A` and `SURFACE_B`, `K_RELIABILITY`, `EXAMPLE_AMPLITUDE`, `OPERATING_MEAN`, `OPERATING_AMPLITUDE`, and `HISTORY_REVERSALS`, `HISTORY_MEAN`, `HISTORY_SCALE`, `SEED` for the random block.

## Usage

```bash
python main.py                          # print the results and show the figure
python main.py --no-show --output .     # save fatigue_sn_and_goodman.png in the current directory
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $k_a = 0.828$, $k_b = 0.862$, $k_e = 0.897$, $S'_e = 300.0$ MPa and $S_e = 192.0$ MPa; $f = 0.8634$, $a = 1398.0$ MPa and $b = -0.14371$. For the operating point it prints safety factors of 1.297 (Goodman), 1.609 (Gerber), 1.171 (Soderberg) and 1.800 (yield). The random block contains 200.0 rainflow cycles, its Miner damage is $2.628 \times 10^{-4}$, and the predicted life is 3806 blocks.

![S-N curves, Haigh diagram with Goodman, Gerber and Soderberg lines, a random stress history and its rainflow-counted damage](fatigue_sn_and_goodman.png)

Panel (a) shows that the Marin factors lower the endurance limit but not the $10^3$-cycle strength, so the shaft's line is steeper and a 250 MPa amplitude gives $1.59 \times 10^5$ cycles. In panel (b), the radial load line through the operating point meets the Goodman line at the cross, 1.30 times farther from the origin. Panel (d) shows that most counted cycles lie below $S_e$ and do no damage, while the one largest cycle of each block, counted as two half cycles, causes about two thirds of the damage.

## Related Notes

- [Fatigue](../../../notes/applied_mechanics/strength_materials/fatigue.md)
- [Combined Loading](../../../notes/applied_mechanics/strength_materials/combined_loading.md)
- [Flow-Induced Vibrations](../../../notes/applied_mechanics/fluid_loading/flow_induced_vibrations.md)
