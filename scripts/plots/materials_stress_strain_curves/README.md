# Stress-Strain Curves

This script draws model engineering and true stress–strain curves of a ductile and a brittle material. The ductile metal follows the Ramberg–Osgood law between true stress and true strain, from which the engineering curve, the ultimate tensile strength and the onset of necking follow; the drop of the engineering curve after necking is drawn as a schematic curve to fracture. The figure shades the toughness under the full curve and, in a zoomed panel, shows the 0.2% offset construction, the modulus of resilience and a brittle material that is linear to fracture. The parameters are representative of a structural steel but do not describe a particular grade.

## Overview

- Models the ductile metal with $E = 200$ GPa, $\sigma_{0.2} = 350$ MPa and Ramberg–Osgood exponent $n = 8$ (constants `E_DUCTILE`, `SIGMA_02`, `N_RO`).
- Converts true to engineering values assuming uniform, constant-volume deformation, and takes the maximum of the engineering stress as the ultimate tensile strength.
- Continues the engineering curve after necking with a parabola that falls to 80% of the UTS at a fracture strain of 0.30 (`FRACTURE_RATIO`, `STRAIN_FRACTURE`); this part is schematic.
- Draws the true curve up to necking and, dotted, the model extrapolated beyond it.
- Integrates the engineering curve for the toughness and computes the modulus of resilience $\sigma_{0.2}^2/(2E)$.
- Finds the 0.2% offset yield strength numerically by intersecting the offset line with the model curve.
- Adds a brittle material with $E = 120$ GPa that fractures at 300 MPa (`E_BRITTLE`, `SIGMA_FRACTURE_BRITTLE`).

## Mathematical Background

The Ramberg–Osgood law in true stress $\sigma_t$ and true strain $\varepsilon_t$ is

$$
\varepsilon_t = \frac{\sigma_t}{E} + 0.002\left(\frac{\sigma_t}{\sigma_{0.2}}\right)^{n}
$$

The plastic part equals 0.002 at $\sigma_t = \sigma_{0.2}$, so the 0.2% offset line $\sigma = E(\varepsilon - 0.002)$ meets the curve exactly at $\sigma_{0.2}$. While the gauge section deforms uniformly, constant volume gives

$$
\varepsilon_e = e^{\varepsilon_t} - 1,
\qquad \sigma_e = \frac{\sigma_t}{1 + \varepsilon_e}
$$

The force $P = \sigma_t A$ is maximum when $dP = 0$; with $dA/A = -d\varepsilon_t$ this is the Considère condition $d\sigma_t/d\varepsilon_t = \sigma_t$, which marks the ultimate tensile strength and the onset of necking. The toughness is $`u_T = \int_0^{\varepsilon_f}\sigma_e\,d\varepsilon_e`$ and the modulus of resilience $u_r = \sigma_{0.2}^2/(2E)$, both in MJ/m³ when stress is in MPa.

## Implementation

- `ramberg_osgood_strain(sigma, modulus, sigma_02, n)` evaluates the law.
- `offset_yield(...)` solves for the intersection with the offset line using `scipy.optimize.brentq`.
- `true_curve(sigma_max, points)` samples the model on a stress grid; `engineering_from_true(eps_true, sigma_true)` converts it.
- `ultimate_point()` returns the engineering strain, UTS, true strain and true stress at the maximum of the engineering curve.
- `engineering_curve(points)` joins the model part up to the UTS with the schematic post-necking part.
- `toughness(eps, sigma)` integrates with the trapezoidal rule.
- `make_figure()` draws the full curves (left) and the small-strain detail (right).

## Usage

```bash
python main.py                          # open the figure window
python main.py --no-show --output .     # save materials_stress_strain_curves.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints

```text
0.2 % offset yield = 350.0 MPa (model parameter 350 MPa)
UTS = 516.4 MPa at engineering strain 0.1359 (true strain 0.1274, true stress 586.6 MPa)
toughness = 144.9 MJ/m^3, resilience = 0.306 MJ/m^3
brittle: fracture strain 0.0025, toughness 0.375 MJ/m^3
```

![Model stress-strain curves](materials_stress_strain_curves.png)

In the left panel the true curve (orange) rises above the engineering curve (blue) as the area shrinks, and the engineering curve peaks at 516 MPa where the Considère condition is met. The shaded toughness of the ductile metal is almost 400 times that of the brittle material, although the two have similar strengths. The right panel shows the gradual yielding typical of the Ramberg–Osgood law with $n = 8$: the curve leaves the line $\sigma = E\varepsilon$ well before $\sigma_{0.2}$, which is why yield is defined by the offset construction.

## Related Notes

- [Mechanical Properties of Materials](../../../notes/applied_mechanics/strength_materials/material_properties.md)
- [Stress and Strain](../../../notes/applied_mechanics/strength_materials/stress_strain.md)
