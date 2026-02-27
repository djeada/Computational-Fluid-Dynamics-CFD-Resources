# Wind Loading on Buildings

Wind loading is one of the dominant design actions for tall buildings, towers, bridges, and lightweight structures. Accurate estimation of wind forces requires understanding of the atmospheric boundary layer, pressure distributions, and dynamic structural response. This chapter covers the key concepts and methods used in wind engineering practice.

## Wind Speed Profiles

### Power Law Profile

The variation of mean wind speed with height is commonly described by the power law:

$$V(z) = V_{ref}\left(\frac{z}{z_{ref}}\right)^{\alpha}$$

where:
- $V_{ref}$ = reference wind speed at height $z_{ref}$ (typically 10 m)
- $\alpha$ = terrain-dependent exponent (0.10 for open sea, 0.14 for open terrain, 0.22 for suburban, 0.33 for city centre)

### Logarithmic Law Profile

A more physically based description uses the log law:

$$V(z) = \frac{u_*}{\kappa} \ln\left(\frac{z}{z_0}\right)$$

where:
- $u_*$ = friction velocity (m/s)
- $\kappa \approx 0.41$ = von Kármán constant
- $z_0$ = aerodynamic roughness length (m)

Typical roughness lengths: open water $z_0 \approx 0.001$ m, grassland $z_0 \approx 0.03$ m, suburban $z_0 \approx 0.3$ m, urban $z_0 \approx 1$ m.

## Dynamic Pressure

The velocity pressure (dynamic pressure) at height $z$ is:

$$q(z) = \frac{1}{2}\rho V(z)^2$$

For standard air at sea level ($\rho = 1.225$ kg/m³) and $V$ in m/s, $q$ is in Pascals.

### Peak Gust Pressure

Design codes use a gust factor $G$ or a peak velocity pressure that accounts for turbulence:

$$q_p(z) = \frac{1}{2}\rho \left[V(z)(1 + g_v I_v(z))\right]^2$$

where $I_v(z)$ is turbulence intensity and $g_v \approx 3.5$ is the peak factor.

## Pressure Coefficients

The wind pressure on any surface of a building is expressed using a pressure coefficient:

$$p = C_p \, q_{ref}$$

where $C_p$ is determined experimentally (wind tunnel) or from code tables.

- $C_p > 0$: positive pressure (push)
- $C_p < 0$: suction (pull)

### Typical Values for a Rectangular Building

| Surface | $C_p$ range |
|---------|-------------|
| Windward wall | +0.7 to +0.8 |
| Leeward wall | −0.3 to −0.5 |
| Side walls | −0.6 to −0.7 |
| Flat roof (windward edge) | −1.0 to −2.0 |
| Flat roof (centre) | −0.4 to −0.7 |

### Internal Pressure

Buildings are not sealed; openings create internal pressure. The net design pressure on a cladding panel is:

$$p_{net} = (C_{p,ext} - C_{p,int}) \, q_{ref}$$

Internal pressure coefficients depend on the dominant opening configuration ($C_{p,int}$ typically $\pm 0.2$ to $\pm 0.6$).

## Along-Wind Response

### Static Component

The mean along-wind base shear is obtained by integrating the mean pressure over the building height:

$$F_{mean} = \int_0^H q(z) \, C_D \, B \, dz$$

where $B$ is the building width and $C_D$ is the drag coefficient for the overall cross-section.

### Dynamic Component — Gust Effect Factor

The total along-wind response includes a dynamic amplification represented by the gust effect factor $G$:

$$F_{design} = G \cdot F_{mean}$$

The gust effect factor accounts for:
1. **Background response** — quasi-static effect of turbulence gusts smaller than the building
2. **Resonant response** — dynamic amplification near the fundamental frequency $f_1$

$$G = 1 + 2 g_p \sqrt{B_s^2 + R^2}$$

where $g_p \approx 3.5$ is the peak factor, $B_s$ is the background factor, and $R$ is the resonance factor:

$$R^2 = \frac{\pi}{4 \zeta} S_L(f_1) R_h R_b$$

- $\zeta$ = damping ratio (structural + aerodynamic)
- $S_L(f_1)$ = normalised wind spectrum at the natural frequency
- $R_h, R_b$ = aerodynamic admittance functions

## Across-Wind Response

### Vortex Shedding

Wind flowing past a bluff body generates alternating vortices at the **Strouhal frequency**:

$$f_s = \frac{St \, V}{D}$$

where $St \approx 0.12$ for rectangular buildings and $D$ is the across-wind dimension.

### Lock-in

When $f_s \approx f_n$ the structure and vortex shedding synchronise (**lock-in**), leading to large across-wind oscillations. The critical wind speed is:

$$V_{cr} = \frac{f_n D}{St}$$

Across-wind accelerations often govern occupant comfort in tall buildings.

### Mitigation Strategies
- Vary the cross-section along the height (tapering, setbacks)
- Add aerodynamic modifications (corner cuts, slots, spoilers)
- Install supplemental damping (tuned mass dampers, viscous dampers)

## Design Codes Overview

### ASCE 7 (United States)

- **Directional Procedure** (Chapter 27): Detailed for any building
- **Envelope Procedure** (Chapter 28): Simplified for low-rise buildings
- Uses a 3-second gust basic wind speed at 10 m in Exposure C
- Risk categories I–IV with corresponding load factors

### Eurocode 1 (EN 1991-1-4)

- 10-minute mean reference wind speed at 10 m in Terrain Category II
- Peak velocity pressure includes turbulence through $c_e(z)$ exposure factor
- Structural factor $c_s c_d$ replaces the gust effect factor

### Key Differences

| Parameter | ASCE 7 | Eurocode 1 |
|-----------|--------|------------|
| Reference speed averaging | 3-second gust | 10-minute mean |
| Height profile | $K_z$ factor | $c_e(z)$ exposure |
| Dynamic factor | Gust effect factor $G$ | Structural factor $c_s c_d$ |

## Worked Example 1: Wind Force on a Low-Rise Building

**Given:**
- Rectangular building: $B = 20$ m, $L = 40$ m, $H = 10$ m
- Basic wind speed $V = 45$ m/s (3-s gust at 10 m, open terrain)
- Drag coefficient $C_D = 1.3$

**Find:** Along-wind base shear.

**Solution:**

Dynamic pressure at roof height:

$$q_H = \frac{1}{2} \times 1.225 \times 45^2 = 1240 \text{ Pa} = 1.24 \text{ kPa}$$

Using a simplified uniform pressure over the height:

$$F = q_H \, C_D \, B \, H = 1240 \times 1.3 \times 20 \times 10 = 322{,}400 \text{ N} \approx 322 \text{ kN}$$

## Worked Example 2: Across-Wind Vibration Check

**Given:**
- Tall building: $H = 180$ m, $D = 30$ m (square plan)
- Fundamental frequency $f_1 = 0.20$ Hz, $St = 0.12$
- Design wind speed at top $V_H = 55$ m/s

**Find:** Whether vortex-shedding lock-in is a concern.

**Solution:**

Shedding frequency at design wind speed:

$$f_s = \frac{St \, V_H}{D} = \frac{0.12 \times 55}{30} = 0.22 \text{ Hz}$$

Critical wind speed for lock-in:

$$V_{cr} = \frac{f_1 D}{St} = \frac{0.20 \times 30}{0.12} = 50 \text{ m/s}$$

Since $V_{cr} = 50$ m/s is within the design range, **lock-in is a concern**. A detailed across-wind analysis including aerodynamic damping and potential mitigation measures is required.

## Worked Example 3: Cladding Design Pressure

**Given:**
- Building with $q_{ref} = 1.5$ kPa at the parapet level
- Windward wall $C_{p,ext} = +0.8$, roof corner zone $C_{p,ext} = -2.0$
- Internal pressure coefficient $C_{p,int} = +0.3$

**Find:** Net cladding pressures for the windward wall and the roof corner zone.

**Solution:**

Windward wall (net positive pressure):

$$p_{net} = (0.8 - 0.3) \times 1.5 = 0.75 \text{ kPa (outward push)}$$

Roof corner zone (net suction):

$$p_{net} = (-2.0 - 0.3) \times 1.5 = -3.45 \text{ kPa (uplift suction)}$$

The roof corner zone experiences the most severe cladding load — this governs fastener and panel design.

## Applications

### Tall Buildings
- Along-wind and across-wind accelerations determine occupant comfort
- Tuned mass dampers are installed in many supertall buildings (e.g., Taipei 101)
- Wind tunnel testing is standard for buildings over approximately 120 m

### Bridges
- Flutter and vortex shedding govern long-span suspension bridge deck design
- Aerodynamic deck sections reduce wind forces
- Cable-stayed bridges require analysis of cable vibration under wind and rain

### Towers and Chimneys
- Circular cross-sections are prone to vortex-induced vibrations
- Helical strakes suppress coherent vortex shedding
- Guy-wire tension must account for wind-induced oscillations

### Solar and Communication Structures
- Open lattice frames use solidity ratio to determine effective drag
- Parabolic dish antennas experience high drag at stow position
- Solar panel arrays are sensitive to tilt angle and ground clearance

## Design Considerations

### Directionality
- Wind climate is rarely uniform in all directions
- Directional analysis can reduce design loads by 10–20%

### Terrain and Topography
- Speed-up over hills and escarpments must be included ($K_{zt}$ in ASCE 7)
- Shielding from upstream buildings can be accounted for, with caution

### Fatigue
- Cladding connections and secondary steelwork may be fatigue-sensitive under repeated gust cycles
- S-N curves and Palmgren–Miner rule are used for fatigue life estimation

### Serviceability
- Peak acceleration limits for occupant comfort: 10–15 milli-g for residential, 20–25 milli-g for office (10-year return period)
- Lateral drift limits: $H/400$ to $H/500$ under design wind

Wind loading analysis links the atmospheric boundary layer physics to structural engineering design, forming a core competency for engineers working on exposed structures.
