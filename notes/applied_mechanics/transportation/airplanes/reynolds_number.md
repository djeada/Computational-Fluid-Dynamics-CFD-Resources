## The Reynolds Number

The Reynolds number (Re) is a fundamental concept in aerodynamics, as it tells us whether the airflow around an object is smooth (laminar) or turbulent. In simpler terms, it’s a way to measure how different forces (like speed, size, and air viscosity) affect how air flows around something, whether that’s an insect, bird, or airplane.

The formula for calculating the Reynolds number is:

$$
Re = \frac{\rho \cdot V \cdot L}{\mu}
$$

Where:

- $\rho$ is the air density (kg/m³),
- $V$ is the velocity or airspeed (m/s),
- $L$ is the characteristic length, often the chord length of the wing (m),
- $\mu$ is the dynamic viscosity of air (kg/m·s).

As you increase either the speed or the size of an object, the Reynolds number also increases, which typically means the airflow becomes more turbulent. For example, an airliner flying at 250 m/s will have a much larger Reynolds number compared to a bird flying at 10 m/s, because the airplane is both faster and larger.

![output(5)](https://github.com/user-attachments/assets/4df93a21-7788-4c0f-a595-3cf7d41fcf8f)

### Flight Airspeed and Mach Number

On the chart’s left side, you’ll see airspeed in meters per second (m/s) and knots. Airspeed is simply how fast the object is moving through the air. As you move up the Y-axis, the speed increases from very slow speeds for things like insects and birds, all the way to extremely fast speeds for supersonic jets and military aircraft.

The right side shows the **Mach number (M)**, which represents the speed of an object relative to the speed of sound in the air. When an object is flying at Mach 1, it is traveling at the speed of sound (about 343 m/s at sea level). If an object’s Mach number is less than 1, it’s flying below the speed of sound (subsonic); if greater than 1, it’s faster than sound (supersonic).

The Mach number is calculated as:

$$
M = \frac{V}{a}
$$

Where:

- $V$ is the velocity of the object (m/s),
- $a$ is the speed of sound in the medium (air), which depends on temperature.

For instance, an airliner typically cruises at Mach 0.8, just below the speed of sound. The Concorde, a famous supersonic passenger jet, cruised at Mach 2, meaning it traveled twice as fast as sound.

### Flight Regimes

Different types of aircraft or objects fit into certain regions on the chart, depending on their speed and size. These regions help us understand the unique challenges and characteristics of their flight. Here are some examples:

I. **Insects and Dust Particles**

Found at the lower left part of the chart, insects and dust particles have low Reynolds numbers because they are small and fly slowly. Their motion is dominated by laminar, smooth airflow. They experience minimal turbulence, and air behaves more like a thick fluid to them.

II. **Birds and Hang Gliders**

Moving toward the middle of the chart, birds and hang gliders operate at slightly higher speeds (5–20 m/s) and higher Reynolds numbers, roughly from $10^4$ (small birds) to $10^6$ (hang gliders). While their flight still involves laminar flow, they might experience some transition to turbulence, especially at higher speeds.

III. **General Aviation and Airliners**

Aircraft like small planes and airliners occupy the region where speeds are much higher (around 100–300 m/s) and Reynolds numbers exceed $10^6$. This is where airflow becomes much more turbulent, and aerodynamic forces like lift and drag become critical to maintaining stable flight.

IV. **Supersonic and Hypersonic Flight**

Military jets and the Concorde are shown at the top right, with Mach numbers greater than 1. In this region, the air becomes compressible, meaning the plane is moving so fast that it pushes air into shock waves. This is where advanced aerodynamics is necessary to overcome the effects of drag and heat from air compression.

### Understanding the Boundaries

The chart also includes horizontal lines that mark the boundaries between key flight regimes:

I. **Incompressible Flow**

At low speeds (below Mach 0.3), air behaves as if its density remains constant. This regime is where most general aviation and birds fly.

II. **Transonic Flow**

As speeds approach Mach 1 (around 343 m/s), the flow becomes compressible, and shock waves can form. This can cause instability, and it’s the regime where most airliners fly.

III. **Supersonic and Hypersonic Flow**

Beyond Mach 1, the air compresses significantly, leading to shock waves. Hypersonic flow occurs when speeds exceed Mach 5, and this is relevant for certain military and space vehicles.

### Putting it All Together

So, how do you use this chart? If you want to understand how a particular object, such as a plane or even a bird, interacts with the air around it, you can look at its **airspeed** and estimate its **Reynolds number** based on its size (the chord length). For example, if you know an airliner typically flies at around Mach 0.8 and has a wing chord of several meters, you can find where it falls on the chart—close to the region for general aviation and airliners.

Similarly, if you’re studying insects, you’d see that they exist in a low-speed, low-Reynolds-number world where laminar flow dominates. Meanwhile, military jets or the Concorde, which fly much faster, deal with much more complex and turbulent airflow, as their Reynolds numbers are extremely high and their Mach numbers surpass 1.

### Related Scripts

- [Laminar vs Turbulent Pipe Flow](../../../../scripts/plots/laminar_vs_turbulent_pipe/): plots laminar and turbulent radial velocity profiles of pipe flow in side-by-side panels to show how much flatter the turbulent profile is.

### Exercises

**Exercise 1.** An airliner cruises at 230 m/s at 11 km altitude, where $\rho = 0.364$ kg/m³, $T = 216.65$ K and $\mu = 1.42 \times 10^{-5}$ Pa·s. Its mean wing chord is 5 m. Find the Reynolds number and the Mach number ($\gamma = 1.4$, $R = 287$ J/(kg·K)).

<details>
<summary>Answer</summary>

```math
Re = \frac{0.364 \times 230 \times 5}{1.42 \times 10^{-5}} = 2.9 \times 10^7
```

```math
a = \sqrt{\gamma RT} = \sqrt{1.4 \times 287 \times 216.65} = 295 \text{ m/s}, \quad
M = \frac{230}{295} = 0.78
```

The flow is fully turbulent over most of the wing and is in the lower transonic regime.

</details>

**Exercise 2.** A bird with a 0.10 m wing chord flies at 10 m/s at sea level ($\rho = 1.225$ kg/m³, $\mu = 1.79 \times 10^{-5}$ Pa·s). Find its Reynolds number, and compare it with the airliner of Exercise 1.

<details>
<summary>Answer</summary>

```math
Re = \frac{1.225 \times 10 \times 0.10}{1.79 \times 10^{-5}} = 6.8 \times 10^4
```

This is about 430 times smaller than the airliner's. At this Reynolds number the boundary layer is largely laminar and prone to laminar separation, so bird and small-drone airfoils are thin and highly cambered rather than scaled-down airliner sections.

</details>

**Exercise 3.** Below what airspeed can sea-level air ($T = 288.15$ K) be treated as incompressible? Is a light aircraft cruising at 60 m/s in that regime?

<details>
<summary>Answer</summary>

$a = \sqrt{1.4 \times 287 \times 288.15} = 340$ m/s, so $M = 0.3$ corresponds to $0.3 \times 340 = 102$ m/s.

At 60 m/s, $M = 0.18$, well inside the incompressible regime. The density changes by only about 1.6% ($\approx M^2/2$).

</details>

**Exercise 4.** A 1:10 scale model of a wing with a 2 m chord is tested in a sea-level wind tunnel. The full-size aircraft flies at 70 m/s at sea level. What tunnel speed matches the Reynolds number, and why is this impractical? How do real facilities get around the problem?

<details>
<summary>Answer</summary>

Matching $Re = \rho VL/\mu$ with $L$ ten times smaller requires $V$ ten times larger: 700 m/s, or $M \approx 2.1$. The model would then see supersonic compressible flow that the aircraft never experiences, so Reynolds and Mach numbers cannot both be matched this way.

Real facilities raise $\rho/\mu$ instead: pressurized tunnels increase the density, and cryogenic tunnels such as NASA's National Transonic Facility cool the gas, which raises its density and lowers its viscosity. Alternatively, engineers test at lower $Re$ and correct the results with CFD and boundary-layer trips.

</details>

**Exercise 5.** On a smooth flat plate, laminar-to-turbulent transition occurs at a local Reynolds number $Re_x \approx 5 \times 10^5$. Estimate how far from the leading edge transition occurs on a light aircraft wing at 60 m/s at sea level, and explain why the answer is only indicative.

<details>
<summary>Answer</summary>

```math
x_{tr} = \frac{Re_x\,\mu}{\rho V} = \frac{5 \times 10^5 \times 1.79 \times 10^{-5}}{1.225 \times 60} = 0.12 \text{ m}
```

That is only about 8% of a 1.5 m chord. On a real wing the transition location depends strongly on the pressure gradient (a favourable gradient delays it, which is how laminar-flow airfoils work), on surface roughness, insect debris and free-stream turbulence. The flat-plate value is only a rough guide.

</details>

### References

- Anderson, J. D., Jr., *Fundamentals of Aerodynamics*, 6th ed., McGraw-Hill Education, 2017.
- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill Education, 2016.
- Schlichting, H., and Gersten, K., *Boundary-Layer Theory*, 9th ed., Springer, 2017.
- NOAA, NASA, and USAF, *U.S. Standard Atmosphere, 1976*, U.S. Government Printing Office, 1976.
