# Thermodynamics of Compressible Flow

## Overview

In low-speed flow the energy equation can often be solved after the velocity field, or ignored altogether, because the kinetic energy of the fluid is tiny compared with its thermal energy. In compressible flow the two are comparable. For air, the ratio of kinetic energy to enthalpy is

$$
\frac{V^2/2}{c_p T} = \frac{\gamma - 1}{2} M^2
$$

This ratio is 0.2 at $M = 1$ and 1.8 at $M = 3$. Every change in velocity is therefore a change in temperature, pressure and density, and the flow cannot be analysed without thermodynamics.

This page collects the thermodynamic tools used throughout gas dynamics:

- the perfect-gas model and its specific heats;
- internal energy and enthalpy;
- the first law for closed systems and for steady flow;
- the second law and the entropy change of a perfect gas;
- isentropic relations;
- stagnation (total) conditions.

The ideal gas law and real-gas corrections are covered in [equation_of_state.md](../governing_equations/equation_of_state.md). The differential form of the energy equation is derived in [energy.md](../governing_equations/energy.md). Unless stated otherwise, numbers are for air with $\gamma = 1.4$ and $R = 287\ \text{J/(kg K)}$.

## The Perfect Gas Model

### Thermally and Calorically Perfect Gases

Gas dynamics is built on two layers of idealisation (terminology as in Anderson, *Modern Compressible Flow*).

A **thermally perfect gas** obeys the equation of state

$$
p = \rho R T
$$

and its internal energy and enthalpy depend on temperature only, $e = e(T)$ and $h = h(T)$. This holds when intermolecular forces are negligible, which is true for air at ordinary pressures. The specific heats may still vary with temperature.

A **calorically perfect gas** is a thermally perfect gas whose specific heats $c_v$ and $c_p$ are also constant. This is the model behind every closed-form relation on these pages: isentropic flow, normal and oblique shocks, and Fanno and Rayleigh flow.

### Specific Heats

For a thermally perfect gas the specific heats are defined by

$$
de = c_v\, dT,
\qquad dh = c_p\, dT
$$

Since $h = e + p/\rho = e + RT$, differentiating gives $dh = de + R\, dT$, so

$$
c_p - c_v = R
$$

With the ratio of specific heats $\gamma = c_p/c_v$:

$$
c_v = \frac{R}{\gamma - 1},
\qquad c_p = \frac{\gamma R}{\gamma - 1}
$$

For air this gives $c_v = 717.5\ \text{J/(kg K)}$ and $c_p = 1004.5\ \text{J/(kg K)}$.

Kinetic theory explains the value of $\gamma$. Each fully excited molecular degree of freedom stores $\tfrac{1}{2}RT$ per unit mass, so a gas with $f$ active degrees of freedom has $c_v = \tfrac{f}{2}R$ and $\gamma = (f + 2)/f$.

| Gas type | Active degrees of freedom | $\gamma$ |
| --- | --- | --- |
| Monatomic (He, Ar) | 3 translational | $5/3 \approx 1.667$ |
| Diatomic (N$_2$, O$_2$, air near room temperature) | 3 translational + 2 rotational | $7/5 = 1.4$ |

### When the Model Fails

The calorically perfect model with $\gamma = 1.4$ is accurate for air from cryogenic wind-tunnel conditions up to several hundred kelvin. At higher temperatures:

- molecular **vibration** becomes excited (noticeably above roughly 800 K), so $c_p$ rises and $\gamma$ falls;
- at around atmospheric pressure, **oxygen dissociates** from roughly 2000 K and **nitrogen** from roughly 4000 K, so the gas becomes chemically reacting.

These conditions appear behind strong shocks in hypersonic flight and in combustion chambers, and they need temperature-dependent or reacting-gas models.

## Internal Energy and Enthalpy

With the reference energy set to zero at $T = 0$, a calorically perfect gas has

$$
e = c_v T,
\qquad h = c_p T
$$

**Internal energy** $e$ is the energy stored in the random motion of the molecules: translation plus rotation for air near room temperature. **Enthalpy** $h = e + p/\rho$ adds the flow work $p/\rho$, the energy needed to push a unit mass of fluid into or out of a control volume. This is why $h$, not $e$, appears in energy balances for open systems such as nozzles, ducts and turbomachines.

## The First Law

### Closed Systems

For a fixed mass of gas that receives heat $\delta q$ and does work $\delta w$ per unit mass,

$$
de = \delta q - \delta w
$$

For a reversible process the work is $\delta w = p\, dv$, where $v = 1/\rho$ is the specific volume.

### Steady-Flow Energy Equation

For a control volume in steady flow with one inlet (1) and one outlet (2),

$$
q - w_s = \left(h_2 + \frac{V_2^2}{2} + g z_2\right) -
\left(h_1 + \frac{V_1^2}{2} + g z_1\right)
$$

Here $q$ is the heat added and $w_s$ the shaft work done by the fluid, both per unit mass. In gas flows the gravity term is usually negligible: a height change of 1 m corresponds to $9.81\ \text{J/kg}$, while a temperature change of 1 K corresponds to $1004.5\ \text{J/kg}$.

An important consequence: **if the flow is adiabatic and does no shaft work, $h + V^2/2$ is the same at inlet and outlet.** This is true even with wall friction or shock waves inside the control volume. Friction and shocks convert kinetic energy into internal energy, but they do not remove energy from the flow, because a stationary wall does no work on it. This observation underlies Fanno flow and the normal-shock energy equation.

## The Second Law and Entropy

Entropy is defined through reversible heat transfer, $ds = \delta q_{rev}/T$. For any real process the second law requires

$$
ds \ge \frac{\delta q}{T}
$$

with equality only when the process is reversible. For an **adiabatic** process this becomes $ds \ge 0$: entropy can only increase or stay constant. In compressible flow the irreversibilities that raise entropy are viscous dissipation and heat conduction. They are concentrated in boundary layers and inside shock waves.

### Gibbs Relations

Combining the first law for a reversible process ($\delta q = T\, ds$, $\delta w = p\, dv$) with $h = e + pv$ gives the **Gibbs relations**:

$$
T\, ds = de + p\, dv,
\qquad T\, ds = dh - v\, dp
$$

They are derived along a reversible path, but they relate only state properties. They therefore hold between any two equilibrium states, whatever process connects them.

## Entropy Change for a Perfect Gas

Substitute $dh = c_p\, dT$ and $v = RT/p$ into the second Gibbs relation:

$$
ds = c_p \frac{dT}{T} - R \frac{dp}{p}
$$

Integrating with constant $c_p$:

$$
s_2 - s_1 = c_p \ln \frac{T_2}{T_1} - R \ln \frac{p_2}{p_1}
$$

The first Gibbs relation gives an equivalent form in terms of density:

$$
s_2 - s_1 = c_v \ln \frac{T_2}{T_1} - R \ln \frac{\rho_2}{\rho_1}
$$

Entropy is a state function, so the same formula applies between the stagnation states defined below. These have the same entropy as their static states:

$$
s_2 - s_1 = c_p \ln \frac{T_{02}}{T_{01}} - R \ln \frac{p_{02}}{p_{01}}
$$

In adiabatic flow $T_{02} = T_{01}$, which leaves

$$
\frac{p_{02}}{p_{01}} = \exp\left(-\frac{s_2 - s_1}{R}\right)
$$

**The loss of stagnation pressure directly measures the entropy generated.** This result is used repeatedly for shock waves ([shock_waves.md](shock_waves.md)) and duct flows ([rayleigh_fanno.md](rayleigh_fanno.md)).

## Isentropic Relations

An isentropic process is both adiabatic and reversible. Setting $ds = 0$ in the entropy equation gives $c_p\, dT/T = R\, dp/p$, and with $R/c_p = (\gamma - 1)/\gamma$:

$$
\frac{T_2}{T_1} = \left(\frac{p_2}{p_1}\right)^{(\gamma - 1)/\gamma}
$$

Using $p = \rho R T$ to eliminate temperature or pressure:

$$
\frac{p_2}{p_1} = \left(\frac{\rho_2}{\rho_1}\right)^{\gamma},
\qquad \frac{T_2}{T_1} = \left(\frac{\rho_2}{\rho_1}\right)^{\gamma - 1}
$$

Equivalently, $p/\rho^\gamma$ is constant along an isentrope, as stated in [equation_of_state.md](../governing_equations/equation_of_state.md).

Isentropic relations apply wherever dissipation is negligible: the core flow in nozzles and diffusers, expansion fans, and weak compressions. They do **not** apply across shock waves or inside boundary layers.

### Worked Example 1: Ideal and Real Compression

Air at $T_1 = 288.15\ \text{K}$ and $p_1 = 101.325\ \text{kPa}$ is compressed adiabatically to $p_2 = 10\, p_1$ in a steady-flow compressor. Kinetic-energy changes are negligible.

**Ideal (isentropic) compressor.**

$$
T_{2s} = 288.15 \times 10^{0.2857} = 556.3\  \text{K},
\qquad \frac{\rho_2}{\rho_1} = 10^{1/1.4} = 5.179
$$

The steady-flow energy equation with $q = 0$ gives the work input

$$
-w_s = c_p (T_{2s} - T_1) = 1004.5 \times 268.2 = 269.4\  \text{kJ/kg}
$$

**Real compressor.** Suppose the measured exit temperature is $T_2 = 600\ \text{K}$. The work input is $c_p(600 - 288.15) = 313.3\ \text{kJ/kg}$, and the isentropic efficiency is

$$
\eta_c = \frac{T_{2s} - T_1}{T_2 - T_1} = \frac{268.2}{311.9} = 0.860
$$

The entropy change is

$$
s_2 - s_1 = 1004.5 \ln \frac{600}{288.15} - 287 \ln 10 = 736.7 - 660.8 = 75.9\
\text{J/(kg K)}
$$

It is positive, as the second law requires for an adiabatic process. The extra 43.9 kJ/kg of work was dissipated into heat by friction and turbulence inside the machine.

## Stagnation (Total) Conditions

### Definition

The **stagnation state** at a point is the state the fluid would reach if it were brought to rest:

- **adiabatically and with no work**, which defines the stagnation enthalpy $h_0$ and temperature $T_0$;
- **isentropically**, which additionally defines the stagnation pressure $p_0$ and density $\rho_0$.

The fluid does not actually have to stop. Stagnation properties are local properties defined at every point, like the static values $p$, $T$ and $\rho$ measured by an observer moving with the flow.

From the steady-flow energy equation with $q = w_s = 0$:

$$
h_0 = h + \frac{V^2}{2},
\qquad T_0 = T + \frac{V^2}{2 c_p}
$$

### In Terms of Mach Number

Divide by $T$ and use $c_p = \gamma R/(\gamma - 1)$ and $a^2 = \gamma R T$ (see [speed_of_sound.md](speed_of_sound.md)):

$$
\frac{T_0}{T} = 1 + \frac{\gamma - 1}{2} M^2
$$

The deceleration to $p_0$ is isentropic by definition, so the isentropic relations give

$$
\frac{p_0}{p} = \left(1 + \frac{\gamma - 1}{2} M^2\right)^{\gamma/(\gamma - 1)},
\qquad \frac{\rho_0}{\rho} = \left(1 + \frac{\gamma - 1}{2} M^2\right)^{1/(\gamma - 1)}
$$

The state where the flow is exactly sonic is a second reference, marked with an asterisk: $T^*/T_0 = 2/(\gamma + 1) = 0.8333$ and $p^*/p_0 = 0.5283$ for air. These ratios and their role in nozzle design are developed in [isentropic_flow.md](isentropic_flow.md).

### What Changes Stagnation Properties

| Process | $T_0$ | $p_0$ |
| --- | --- | --- |
| Isentropic flow (nozzle, expansion fan) | constant | constant |
| Adiabatic with friction or shocks | constant | **decreases** |
| Heat addition | increases, $q = c_p (T_{02} - T_{01})$ | decreases |
| Shaft work (compressor, turbine) | changes, $w_s = -c_p(T_{02} - T_{01})$ | changes |

Two further consequences:

- **Maximum speed.** If all the enthalpy were converted into kinetic energy ($T \to 0$), the flow would reach $V_{max} = \sqrt{2 c_p T_0}$. For $T_0 = 300\ \text{K}$ that is $776.3\ \text{m/s}$.
- **Low-speed limit.** For small $M$, expanding $p_0/p$ gives $p_0 - p = \tfrac{1}{2}\rho V^2 (1 + M^2/4 + \cdots)$. This reduces to Bernoulli's equation as $M \to 0$ (see [bernoulli.md](../inviscid_flow/bernoulli.md)).

### Worked Example 2: Stagnation Conditions of a Moving Stream

Air flows at $V = 250\ \text{m/s}$ with $T = 250\ \text{K}$ and $p = 50\ \text{kPa}$.

$$
T_0 = 250 + \frac{250^2}{2 \times 1004.5} = 281.1\  \text{K}
$$

$$
a = \sqrt{1.4 \times 287 \times 250} = 316.9\  \text{m/s},
\qquad M = 0.789
$$

$$
p_0 = 50 \left(\frac{281.1}{250}\right)^{3.5} = 75.38\  \text{kPa}
$$

The static density is $\rho = p/(RT) = 0.6969\ \text{kg/m}^3$, and the stagnation density is $\rho_0 = 0.9343\ \text{kg/m}^3$.

The incompressible Bernoulli equation would predict $p_0 = p + \tfrac{1}{2}\rho V^2 = 71.78\ \text{kPa}$, which is 4.8% too low. At this Mach number, compressibility cannot be neglected.

## Summary

- Calorically perfect gas: $p = \rho R T$, $e = c_v T$, $h = c_p T$, $c_p - c_v = R$, $\gamma = c_p/c_v$.
- Steady adiabatic flow without work conserves $h_0 = h + V^2/2$, whether or not the flow is reversible.
- $s_2 - s_1 = c_p \ln(T_2/T_1) - R \ln(p_2/p_1)$. In adiabatic flow the entropy rise equals $-R \ln(p_{02}/p_{01})$.
- Isentropic: $p/\rho^\gamma = \text{const}$ and $T \propto p^{(\gamma - 1)/\gamma}$.
- $T_0/T = 1 + \tfrac{\gamma - 1}{2}M^2$, and $p_0/p$ and $\rho_0/\rho$ follow from the isentropic exponents.

## Related Scripts

- [probability_distribution_function_of_nitrogen_molecules](../../../scripts/plots/probability_distribution_function_of_nitrogen_molecules/): plots the Maxwell–Boltzmann speed distribution of N$_2$ at several temperatures. It shows temperature as a measure of random molecular kinetic energy, which is the physical content of $e = c_v T$.

## Exercises

**Exercise 1.** Helium has $R = 2077\ \text{J/(kg K)}$ and $\gamma = 5/3$. Compute $c_v$ and $c_p$, and explain why $\gamma$ is larger than for air.

<details>
<summary>Answer</summary>

$c_v = R/(\gamma - 1) = 2077/(2/3) = 3115.5\ \text{J/(kg K)}$ and $c_p = \gamma R/(\gamma - 1) = 5192.5\ \text{J/(kg K)}$. As a check, $c_p - c_v = 2077 = R$.

Helium is monatomic, so it can store energy only in its 3 translational degrees of freedom. Then $\gamma = (3 + 2)/3 = 5/3$. Diatomic air also has 2 rotational degrees of freedom, giving $\gamma = 7/5$.

</details>

**Exercise 2.** A temperature probe on an aircraft brings the oncoming air to rest adiabatically. The ambient temperature is 220 K and the airspeed is 250 m/s. What temperature does an ideal probe read, and what is the flight Mach number?

<details>
<summary>Answer</summary>

$T_0 = 220 + 250^2/(2 \times 1004.5) = 220 + 31.1 = 251.1\ \text{K}$.

$a = \sqrt{1.4 \times 287 \times 220} = 297.3\ \text{m/s}$, so $M = 0.841$.

The probe reads 31 K above ambient. Air-data computers must correct for this to recover the true outside air temperature.

</details>

**Exercise 3.** Air is heated from 300 K to 900 K (a) at constant pressure and (b) at constant volume. Compute the entropy change in each case and explain the difference.

<details>
<summary>Answer</summary>

(a) $s_2 - s_1 = c_p \ln 3 - R \ln 1 = 1004.5 \times 1.0986 = 1103.6\ \text{J/(kg K)}$.

(b) $s_2 - s_1 = c_v \ln 3 - R \ln 1 = 717.5 \times 1.0986 = 788.3\ \text{J/(kg K)}$.

The difference is $315.3\ \text{J/(kg K)} = R \ln 3$. At constant pressure the density falls by a factor of 3 as the gas expands, and the $-R \ln(\rho_2/\rho_1)$ term adds that amount of entropy.

</details>

**Exercise 4.** In an insulated duct the stagnation pressure falls by 10% between two stations. What happens to the stagnation temperature, and how much entropy is generated?

<details>
<summary>Answer</summary>

The duct is adiabatic and does no work, so $T_0$ is unchanged.

$s_2 - s_1 = -R \ln(p_{02}/p_{01}) = -287 \ln 0.9 = 30.24\ \text{J/(kg K)}$.

The generated entropy is positive, which shows the loss comes from an irreversible process such as wall friction or a shock.

</details>

**Exercise 5.** Combustion gas (treat as air) enters a turbine at $T_{01} = 1400\ \text{K}$ and expands to $p_{02}/p_{01} = 1/8$. (a) Find the isentropic exit stagnation temperature and specific work. (b) The actual exit stagnation temperature is 850 K. Find the actual work, the isentropic efficiency and the entropy generated.

<details>
<summary>Answer</summary>

(a) $T_{02s} = 1400 \times (1/8)^{0.2857} = 772.9\ \text{K}$, and $w_s = c_p (T_{01} - T_{02s}) = 1004.5 \times 627.1 = 630.0\ \text{kJ/kg}$.

(b) $w_s = 1004.5 \times 550 = 552.5\ \text{kJ/kg}$, and $\eta_t = (1400 - 850)/(1400 - 772.9) = 0.877$.

$s_2 - s_1 = c_p \ln(850/1400) - R \ln(1/8) = -501.2 + 596.8 = 95.6\ \text{J/(kg K)}$.

</details>

## References

- Anderson, J. D., *Modern Compressible Flow: With Historical Perspective*, 3rd ed., McGraw-Hill, 2003. Chapter 1 reviews thermodynamics for gas dynamics.
- Liepmann, H. W., and Roshko, A., *Elements of Gasdynamics*, Wiley, 1957 (reprinted by Dover).
- Zucker, R. D., and Biblarz, O., *Fundamentals of Gas Dynamics*, 2nd ed., Wiley, 2002.
