## How Airplanes Work

Airplanes are remarkable machines that harness the principles of physics to soar through the sky. The complexity of flight, though impressive, can be broken down into a few fundamental concepts. To understand how airplanes fly, it’s important to explore the forces and components involved.

### Basic Principles of Flight

At the heart of every flight are four fundamental forces: lift, weight, thrust, and drag. These forces interact in a delicate balance that determines whether an airplane will rise, stay aloft, or descend.

#### The Four Forces

Flight is governed by four primary forces: lift, weight, thrust, and drag. Each of these forces can be described mathematically, and understanding their relationships is key to predicting an airplane’s behavior in flight.

![output(4)](https://github.com/user-attachments/assets/768de086-0099-43ff-9b6a-8556f67e49f0)

I. **Lift** is the force that counteracts the airplane’s weight, allowing it to stay in the air. Lift depends on the airspeed, the shape of the wings, and the density of the air. The equation for lift is:

$$
L = \frac{1}{2} \rho v^2 C_L A
$$

- $L$ is the lift force in newtons (N),
- $\rho$ is the air density (kg/m³),
- $v$ is the velocity of the airplane relative to the air (m/s),
- $C_L$ is the lift coefficient (a dimensionless number that depends on the wing shape and angle of attack),
- $A$ is the wing area (m²).

This equation reveals that lift increases with the square of the velocity and the size of the wings. Hence, larger airplanes or those flying faster generate more lift.

II. **Weight** is the gravitational force acting on the airplane, which is simply the mass of the airplane multiplied by the acceleration due to gravity:

$$
W = mg
$$

- $W$ is the weight (N),
- $m$ is the mass of the airplane (kg),
- $g$ is the acceleration due to gravity ($9.81 \, \text{m/s}^2$).

III. **Thrust** is the forward force provided by the airplane’s engines, and it is responsible for overcoming drag and propelling the aircraft. Thrust depends on the power of the engines and the design of the propellers or jet nozzles.

The power delivered by the engines can be expressed as:

$$
P = T \cdot v
$$

- $P$ is the power (W),
- $T$ is the thrust (N),
- $v$ is the airspeed (m/s).

IV. **Drag** is the aerodynamic resistance that opposes thrust. The drag force can be expressed by the drag equation:

$$
D = \frac{1}{2} \rho v^2 C_D A
$$

- $D$ is the drag force (N),
- $C_D$ is the drag coefficient, which depends on the shape of the airplane and its orientation relative to the airflow.

#### Bernoulli's Principle and the Continuity Equation

The generation of lift on an airplane wing can also be described using Bernoulli’s principle, which relates the pressure and velocity of a fluid. For a wing, air moves faster over the curved top surface than underneath, causing a pressure difference that generates lift.

According to Bernoulli’s equation:

$$
P_1 + \frac{1}{2} \rho v_1^2 = P_2 + \frac{1}{2} \rho v_2^2
$$

- $P_1$ and $P_2$ are the pressures on the top and bottom of the wing,
- $v_1$ and $v_2$ are the velocities of the airflow over the top and bottom surfaces,
- $\rho$ is the air density.

Because the air moves faster over the top of the wing ($v_1 > v_2$), the pressure on the top ($P_1$) is lower than the pressure on the bottom ($P_2$), leading to an upward lift force.

The continuity equation also governs the conservation of mass in a fluid flow. For incompressible flow over an airfoil, the continuity equation ensures that the product of the cross-sectional area and velocity remains constant:

$$
A_1 v_1 = A_2 v_2
$$

This explains how narrowing airflow over the top of the wing increases its velocity, contributing to Bernoulli’s effect.

### Aircraft Performance and Power

#### Power and Energy Considerations

Aircraft performance can also be explored through energy and power equations. The total mechanical power required to overcome drag and maintain steady flight is:

$$
P_{\text{required}} = D \cdot v = \frac{1}{2} \rho v^3 C_D A
$$

This equation highlights that the power required to maintain flight increases dramatically with velocity, as it is proportional to the cube of the airspeed for a constant $C_D$ (a fair approximation at high speed, where parasite drag dominates; at low speed induced drag raises $C_D$ and the power required climbs again). Therefore, small increases in speed require significantly more engine power to overcome drag.

In level flight, the engine must produce enough power to generate sufficient thrust to overcome both drag and maintain altitude. The efficiency of the engines can be expressed by the ratio of useful power (thrust times velocity) to the total energy expended:

$$
\eta = \frac{T \cdot v}{P_{\text{input}}}
$$

where $\eta$ is the efficiency of the engine.

#### Climbing and Descent Performance

A steady climb does not require more lift than weight (in fact $L = W\cos\gamma$, slightly less than $W$, where $\gamma$ is the climb angle); it requires excess thrust, i.e. excess power. The rate of climb is related to the excess power available from the engines after overcoming drag. The vertical component of velocity during a climb, called the rate of climb ($R_c$), can be approximated as:

$$
R_c = \frac{P_{\text{excess}}}{W}
$$

where $P_{\text{excess}}$ is the difference between the engine power and the power required to overcome drag at the current speed.

Conversely, during descent, the airplane can use gravity to its advantage, reducing the power needed from the engines. The descent rate depends on the lift-to-drag ratio ($L/D$), which is a measure of how efficiently an airplane converts lift into forward motion relative to the drag it encounters. A higher lift-to-drag ratio means the airplane can glide longer distances with minimal engine power.

### Stability and Control

#### Equilibrium and Stability

In steady, level flight, an airplane is in equilibrium, meaning that the sum of forces and the sum of moments (torques) acting on it are zero. Mathematically, this is expressed as:

$$
\sum F = 0 \quad \text{and} \quad \sum M = 0
$$

where $F$ represents the forces (lift, weight, thrust, drag) and $M$ represents the moments (generated by control surfaces like elevators, rudders, and ailerons).

For stability, the airplane must be able to return to this equilibrium state after a disturbance. Pitch stability, for instance, depends on the location of the center of gravity relative to the aerodynamic center of the wings. The stability condition can be quantified by the stability derivative:

$$
M_{\alpha} = \frac{\partial M}{\partial \alpha}
$$

where $\alpha$ is the angle of attack. If $M_{\alpha}$ is negative, the airplane tends to return to its original pitch angle after being disturbed, indicating positive static stability.

### Angle of Attack, Stall, and Lift Curves

The **angle of attack** ($\alpha$) is the angle between the oncoming airflow and the chord line of the wing. Lift increases with angle of attack up to a certain point, beyond which a stall occurs. The relationship between lift and angle of attack is captured in lift curves, where:

$$
L = C_L(\alpha) \cdot \frac{1}{2} \rho v^2 A
$$

For small angles of attack, the lift coefficient $C_L$ increases linearly with $\alpha$. However, once the critical angle is exceeded, airflow separation causes a dramatic loss of lift, leading to a stall. Stalls are a critical aspect of flight, and pilots must be aware of the airplane's stall speed:

$$
v_{\text{stall}} = \sqrt{\frac{2 W}{\rho C_{L_{\text{max}}} A}}
$$

where $C_{L_{\text{max}}}$ is the maximum lift coefficient before stall.

### Airplane Components

To appreciate how an airplane flies, it’s helpful to look at its various parts, each contributing to different aspects of flight.

The fuselage forms the main body of the airplane. This is where passengers, crew, and cargo are housed, and it connects the other major components like the wings and tail. The fuselage’s streamlined shape is crucial in reducing drag.

Wings are arguably the most critical part of the airplane when it comes to generating lift. Their shape and orientation, especially the angle of attack (the angle between the wing and the oncoming air), directly affect how much lift is created. On the wings, there are control surfaces like ailerons and flaps. Ailerons, located on the outer rear edges, allow the plane to roll, helping it turn. Flaps, located closer to the fuselage, can extend to increase both lift and drag, making it easier to take off and land at slower speeds.

At the back of the airplane is the empennage, or tail section, which provides stability and control. The horizontal stabilizer helps control pitch, allowing the airplane to point its nose up or down, while the vertical stabilizer manages yaw, which turns the airplane left or right. Attached to these stabilizers are elevators and the rudder. Elevators are small surfaces that move to control pitch, and the rudder swivels to control yaw.

Engines play a pivotal role in providing the thrust necessary to move the airplane forward. There are two main types of engines used in airplanes: jet engines and propeller engines. Jet engines generate thrust by expelling high-speed exhaust gases, while propeller engines use rotating blades to push air backward, moving the airplane forward.

### Control Surfaces

Airplanes are equipped with various control surfaces that pilots use to manipulate the aircraft’s orientation and path through the air. These surfaces can be divided into primary and secondary controls.

Primary control surfaces include ailerons, elevators, and the rudder. Ailerons control the airplane’s roll by moving one wing up while lowering the other, causing the airplane to tilt. Elevators control the pitch, which moves the airplane's nose up or down. The rudder is used to control yaw, allowing the airplane to point its nose left or right, which is essential for coordinated turns.

In addition to these, secondary control surfaces, such as flaps, slats, and spoilers, assist in specific flight conditions. Flaps extend downward from the wing to increase both lift and drag, enabling smoother takeoffs and landings at lower speeds. Slats, which are similar to flaps but located at the leading edge of the wing, increase lift at slow speeds by improving airflow over the wing. Spoilers, on the other hand, are deployed to disrupt the airflow over the wing, reducing lift and increasing drag, which helps the airplane descend and slow down more efficiently.

### Flight Dynamics

The motion of an airplane in the air can be described in terms of three basic types of movement: pitch, roll, and yaw. Each movement is controlled by different parts of the airplane, and understanding them is key to grasping how a plane maneuvers.

Pitch refers to the up and down movement of the airplane’s nose, which is controlled by the elevators on the tail. This movement is crucial for climbing and descending. By raising the elevators, the nose of the airplane points upward, and the aircraft begins to climb. Lowering the elevators causes the nose to drop, initiating a descent.

Roll, on the other hand, is the tilting of the airplane to the left or right. This motion is controlled by the ailerons, which adjust the wings' positions relative to one another. Rolling is a vital part of turning the airplane, as it allows the aircraft to bank into a turn smoothly.

Yaw describes the left or right movement of the airplane's nose, controlled by the rudder on the vertical stabilizer. This motion allows the airplane to align properly during turns and to correct for crosswinds when landing.

### Aerodynamics

Flight is governed by the principles of aerodynamics, with two key concepts being the angle of attack and the lift coefficient. The angle of attack is the angle between the wing's chord line (an imaginary straight line from the leading to the trailing edge) and the direction of the oncoming air. This angle is important because, up to a certain point, increasing the angle of attack increases the lift generated by the wings. However, if the angle becomes too steep, the airflow will separate from the wing’s surface, causing a loss of lift, a condition known as stall.

The lift coefficient is a dimensionless number that quantifies how effectively a wing generates lift. It depends on factors like the shape of the wing, the airspeed, and the angle of attack. The formula for the lift coefficient is given as:

$$
C_L = \frac{L}{0.5 \times \rho \times V^2 \times A}
$$

where $L$ is the lift force, $\rho$ is the air density, $V$ is the velocity, and $A$ is the wing area. This formula highlights that lift is proportional to both the square of the velocity and the wing area, meaning faster speeds or larger wings result in more lift.

Similarly, drag is quantified using the drag coefficient, which follows a similar formula:

$$
C_D = \frac{D}{0.5 \times \rho \times V^2 \times A}
$$

where $D$ is the drag force. Reducing the drag coefficient is essential for efficient flight, as minimizing drag allows the airplane to fly faster and use less fuel.

### Related Scripts

- [Airfoil Angle of Attack](../../../../scripts/plots/airfoil_angle_attack/): draws a NACA 2412 airfoil pitched nose-up about its leading edge to several angles of attack, $10^\circ$ and $60^\circ$ by default, relative to a free stream flowing left to right.

### Exercises

**Exercise 1.** A light aircraft has mass 1100 kg and wing area 16.2 m². Find its sea-level stall speed ($\rho = 1.225$ kg/m³) with $C_{L_{max}} = 1.6$ (flaps up) and $C_{L_{max}} = 2.1$ (flaps down). Give the answers in m/s and knots.

<details>
<summary>Answer</summary>

$W = 1100 \times 9.81 = 10\,791$ N.

- Flaps up: $v_{stall} = \sqrt{\dfrac{2 \times 10\,791}{1.225 \times 1.6 \times 16.2}} = 26.1$ m/s = 50.7 kt
- Flaps down: $v_{stall} = 22.8$ m/s = 44.2 kt

Flaps cut the stall speed by 13%, which shortens takeoff and landing distances roughly in proportion to $v^2$.

</details>

**Exercise 2.** The same aircraft cruises in level flight at 55 m/s at sea level. What lift coefficient is required? Compare it with $C_{L_{max}}$.

<details>
<summary>Answer</summary>

In level flight $L = W$:

$$
C_L = \frac{2W}{\rho v^2 A} = \frac{2 \times 10\,791}{1.225 \times 55^2 \times 16.2} = 0.36
$$

This is less than a quarter of $C_{L_{max}} = 1.6$, leaving a wide margin above the stall. It corresponds to a small angle of attack.

</details>

**Exercise 3.** Taking $C_D = 0.032$ as constant, find the drag and power required at 55 m/s and at 110 m/s for this aircraft. Why is the constant-$C_D$ assumption poor at low speed?

<details>
<summary>Answer</summary>

- At 55 m/s: $D = \tfrac{1}{2}(1.225)(55^2)(0.032)(16.2) = 960$ N and $P = Dv = 52.8$ kW
- At 110 m/s: $D = 3842$ N (4 times) and $P = 423$ kW (8 times)

At low speed the wing needs a higher $C_L$, and induced drag grows as $C_L^2$. $C_D$ therefore rises sharply as speed falls, and the real power-required curve has a minimum at an intermediate speed instead of falling steadily toward zero.

</details>

**Exercise 4.** At a climb speed of 40 m/s, the engine and propeller deliver 80 kW of useful power and the power required for level flight at that speed is 35 kW. Find the rate of climb and the climb angle, and show that the lift during the climb is slightly less than the weight.

<details>
<summary>Answer</summary>

$P_{excess} = 45$ kW, so

$$
R_c = \frac{P_{excess}}{W} = \frac{45\,000}{10\,791} = 4.17 \text{ m/s} \approx 820
\text{ ft/min}
$$

$\sin\gamma = R_c/V = 4.17/40$, so $\gamma = 6.0^\circ$.

Perpendicular to the flight path, $L = W\cos\gamma = 0.995\,W$. The climb comes from excess thrust, not excess lift.

</details>

**Exercise 5.** With the engine off, the aircraft's best lift-to-drag ratio is 10. How far can it glide from 1500 m in still air? What speed should the pilot fly, and how does a headwind change the answer?

<details>
<summary>Answer</summary>

Glide distance: $(L/D) \times h = 10 \times 1500 = 15$ km.

The pilot should fly at the speed that gives maximum $L/D$ (the best-glide speed in the handbook). A headwind reduces the distance over the ground, and the best range is then obtained by flying somewhat faster than the still-air best-glide speed.

</details>

### References

- Anderson, J. D., Jr., *Introduction to Flight*, 8th ed., McGraw-Hill Education, 2016.
- Anderson, J. D., Jr., *Fundamentals of Aerodynamics*, 6th ed., McGraw-Hill Education, 2017.
- Federal Aviation Administration, *Pilot's Handbook of Aeronautical Knowledge*, FAA-H-8083-25B, 2016.
