# Morison Wave Force on a Vertical Pile

This script computes the wave force on a vertical pile by integrating the Morison equation over the depth with linear (Airy) wave kinematics. It solves the dispersion relation for the wave number, evaluates the drag and inertia force per unit length from the seabed to the still-water level, sums them into the base shear and overturning moment over one wave period, and shows how the share of drag in the peak force grows with the Keulegan–Carpenter number.

## Overview

- Solves $\omega^2 = gk\tanh(kh)$ for $k$ by Newton iteration from an explicit starting value.
- Evaluates the Airy horizontal velocity and acceleration at the pile ($x = 0$) for $-h \le z \le 0$.
- Computes the drag term $\tfrac12\rho C_d D|u|u$ and the inertia term $\rho C_m (\pi D^2/4)\dot u$ per unit length, and integrates both over the depth with 64-point Gauss–Legendre quadrature.
- Compares the integrated amplitudes with closed-form depth integrals and the peak force with the closed-form maximum of the combined signal.
- Plots, for the example pile, the force amplitudes per unit length against depth, the drag, inertia and total base shear over one period, and the drag and inertia amplitudes relative to the peak force as functions of KC.

## Mathematical Background

### Airy Kinematics

For a wave of height $H$ (amplitude $a = H/2$), period $T$ ($\omega = 2\pi/T$) and wave number $k$ in water of depth $h$, with the surface elevation $\eta = a\cos(kx - \omega t)$ and $z$ measured upward from the still-water level,

```math
u = a\omega\,\frac{\cosh k(z + h)}{\sinh kh}\cos(kx - \omega t),
\qquad
\dot u = a\omega^2\,\frac{\cosh k(z + h)}{\sinh kh}\sin(kx - \omega t)
```

At $x = 0$ the crest passes at $\omega t = 0$ and the acceleration is largest a quarter period earlier, at $\omega t = -\pi/2$.

### Morison Equation and Depth Integrals

The force per unit length on a fixed slender cylinder of diameter $D$ is

```math
f = \tfrac12\rho C_d D\,|u|\,u + \rho C_m \frac{\pi D^2}{4}\,\dot u
```

Integrating from $z = -h$ to $0$ gives amplitudes

```math
F_I = \rho C_m \frac{\pi D^2}{4}\,\frac{a\omega^2}{k},
\qquad
F_D = \tfrac12\rho C_d D\,(a\omega)^2\,\frac{\sinh(2kh)/(4k) + h/2}{\sinh^2 kh}
```

and the base shear $F(\phi) = F_D|\cos\phi|\cos\phi - F_I\sin\phi$ with $\phi = \omega t$. Its maximum is $F_I$ when $F_D \le F_I/2$ and $F_D + F_I^2/(4F_D)$ otherwise.

### Keulegan–Carpenter Number

Per unit length, with $u_m = a\omega\cosh k(z+h)/\sinh kh$ and $\mathrm{KC} = u_m T/D$, the ratio of the drag to the inertia amplitude is

```math
\frac{f_D}{f_I} = \frac{C_d\,\mathrm{KC}}{\pi^2 C_m}
```

so drag first contributes to the peak at $\mathrm{KC} = \pi^2 C_m/(2C_d)$ (9.9 for $C_d = 1$, $C_m = 2$) and the two amplitudes are equal at $\mathrm{KC} = \pi^2 C_m/C_d$ (19.7).

## Implementation

- `wave_number(omega, depth)` solves the dispersion relation by Newton iteration.
- `airy_kinematics(z, phase, height, period, depth)` returns $u$ and $\dot u$ broadcast over depth and phase.
- `morison_per_length(u, dudt, diameter, cd, cm)` returns the drag and inertia force per unit length.
- `pile_force(phase, ...)` integrates over the depth with Gauss–Legendre points (`N_DEPTH`) and returns drag, inertia, total base shear and moment about the seabed.
- `force_amplitudes(...)`, `peak_force(f_d, f_i)` and `drag_to_inertia_ratio(kc)` are the closed forms above.
- The example is set by `PILE_DIAMETER = 2` m, `WATER_DEPTH = 20` m, `WAVE_HEIGHT = 6` m, `WAVE_PERIOD = 10` s, `DRAG_COEFF = 1`, `INERTIA_COEFF = 2` and `RHO_SEA = 1025` kg/m³. Linear theory is applied only up to the still-water level, without stretching.

## Usage

```bash
python main.py                         # print the results and show the figure
python main.py --no-show --output .    # save fluid_loading_morison_wave_force.png
```

| Flag | Meaning |
| --- | --- |
| `--no-show` | Do not open a plot window |
| `--output DIR` | Create `DIR` and save the figure as a PNG |

## Output

The script prints $k = 0.05183$ rad/m, a wavelength of 121.2 m ($kh = 1.04$, intermediate depth, $D/L = 0.017$), a surface velocity amplitude of 2.43 m/s, an acceleration amplitude of 1.53 m/s² and a surface KC of 12.1. The integrated amplitudes are $F_D = 69.2$ kN and $F_I = 147.2$ kN from both quadrature and the closed forms. Because $F_D < F_I/2$, the peak base shear equals $F_I = 147.2$ kN and occurs at $\omega t = -90^\circ$; the peak overturning moment about the seabed is 1.59 MN·m.

![Morison force amplitudes over the depth, base shear over one period, and drag and inertia shares against KC](fluid_loading_morison_wave_force.png)

Panel (a) shows that drag decays faster with depth than inertia, because it follows $\cosh^2$ rather than $\cosh$. Panel (b) shows the total force peaking before the crest, where the inertia force is largest. Panel (c) is per unit length: at the surface the example has KC = 12.1, above the value 9.9 where drag starts to raise the peak, but over the whole depth the pile is still inertia-dominated.

## Related Notes

- [Wave Loading on Offshore Structures](../../../notes/applied_mechanics/fluid_loading/wave_loading.md)
- [Fluid Loading on Structures](../../../notes/applied_mechanics/fluid_loading/intro.md)
