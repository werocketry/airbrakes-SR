# Literature Review

## Background

### Search Strategies & Terms

Key words terms (KWT)

1. "airbrakes" AND "sounding rocket"
2. "air brakes"
3. "rocket" AND "apogee targeting"
4. "airbrakes" OR "air brakes"
5. "rocket airbrakes"
6. "drag" AND "rocket"
7. "airbrakes" AND "SRAD"
8. "airbrakes" AND "github"
9. "airbrakes" AND "gitlab"

Strategies

1. Searched KWT 1-7 on duckduckgo

### What are Airbrakes?
TODO

### Theoretical Framework
TODO

### Significance and Importance
TODO

### Current State of the Art

#### Swiss Association: ARIS
- **Team:** 100
- **Year:** 2018 Spaceport America Cup 10K
- **Score:** 525.0, ranked 57th
- **Predicted Apogee:** not specified
- **Apogee Reached:** not specified
- **Airbrake Type:** Pancake, 3 x 3200mm²
- **Control Method:** A look-up table made with Monte Carlo simulations considering various factors.
- **More on Control Method:** "The control values are chosen to minimize the risk of missing the target due to deviations from the simulation, choosing the 'path' closest to 10000ft. Once the risk is minimized, the algorithm also tries to minimize brake movement during each trajectory. The rocket's vertical position and velocity are calculated by integrating IMU measurements and barometer values, with a preference for IMU measurements during ascent due to biases in barometer values. The control table adjusts airbrakes based on the current position and altitude; if the rocket deviates from stored values, airbrakes are either fully extended or retracted."
- [Project Report](https://www.soundingrocket.org/uploads/9/0/6/4/9064598/100_project_report.pdf)

#### University of Ottawa
- **Team:** 55
- **Year:** 2018 Spaceport America Cup 10K
- **Score:** 510.0, ranked 59th
- **Predicted Apogee:** not specified
- **Apogee Reached:** not specified
- **Airbrake Type:** Pancake, 3 x 110.4cm²
- **Control Method:** Model Predictive Control (MPC), simulating the rocket in real-time to predict the final apogee and adjust airbrakes accordingly.
- [Project Report](https://www.soundingrocket.org/uploads/9/0/6/4/9064598/55_project_report.pdf)

#### Worcester Polytechnic Institute High Power Rocketry Club
- **Team:** 81
- **Year:** 2022 Spaceport America Cup 10K
- **Score:** 59th of 94 (Barrowman rank)
- **Predicted Apogee:** 10000ft
- **Apogee Reached:** 3854ft (due to flight failure)
- **Airbrake Type:** Pancake, 4 x 110.4cm²
- **Control Method:** Adjusts airbrakes to match real-time drag coefficients to calculated values using CFD analysis and OpenRocket simulations.
- [Technical Report](https://aiaa.wpi.edu/static/hprc/aquila/81_technical_report.pdf)

#### University of Maryland
- **Team:** 127
- **Year:** 2023 Spaceport America Cup 10K
- **Score:** 29th of 119 (Barrowman rank)
- **Predicted Apogee:** 10000ft
- **Apogee Reached:** 10473ft
- **Airbrake Type:** Flaps (deploy almost 90 degrees to body at max deployment), 29.9in²
- **Control Method:** Drag-modulating closed-feedback system.
- [Technical Report](https://drive.google.com/file/d/18ZheeMO8H3UuRlllgGhdWLznT8SM7l4D/view)

#### Duke University
- **Team:** 21
- **Year:** 2023 Spaceport America Cup 10K
- **Score:** 64th of 119 (Barrowman rank)
- **Predicted Apogee:** 10000ft
- **Apogee Reached:** 8279ft
- **Airbrake Type:** Pancake
- **Control Method:** Look-up table with pre-rendered flight simulations.
- [Project Poster](https://www.dukerocketry.com/static/sac_poster_2023-2be0677cc1351e5e15706fc27638b094.pdf)

#### University of Akron
- **Team:** 120
- **Year:** 2023 Spaceport America Cup 10K
- **Score:** 392, 86th of 101
- **Predicted Apogee:** 10000ft
- **Apogee Reached:** not specified
- **Airbrake Type:** Pancake, 3x 2.25 in²
- **Control Method:** Look-up table with pre-rendered flight simulations from OpenRocket and Ras Aero.
- [Flight Readiness Review Report](https://akronauts.files.wordpress.com/2018/03/university-of-akron-2018-frr-report.pdf)


## Literature
### SOURCE TITLE NAME
APA-FORMAT-CITATION-OF-SOURCE
- Key points

TODO


## Analysis of Literature
The field of amateur rocketry has seen significant advancements in
apogee control systems, particularly through the integration of
airbrakes. One such study by ARIS Space formulated the problem of apogee
targeting as a chance-constrained optimal control problem, addressing
challenges such as nonlinear dynamics and external disturbances like
wind. The study employed a three-step approach involving a reduced-order
model, offline problem-solving to generate a control table, and
real-time control during flight. This methodology allowed for the
offline computation of control policy, reducing the computational load
during the flight \[6\].

![A close-up of a mechanical device Description automatically
generated](./media/image2.png)
Another team aiming for precise apogee targeting in the Spaceport
America Cup used a SRAD rocket simulator along with a discrete PI
controller. Their airbrake design was positioned above the motor and
extended perpendicularly to the flight direction. The team conducted 3D
CFD analysis in ANSYS Fluent and used Monte Carlo simulations to produce
a normal distribution for optimal air brake deployment time \[7\].

The Queen\'s Rocket Engineering Team (QRET) developed an Active Rocket
Apogee Control (ARAC) system that also aimed for a 10,000 ft apogee.
Their design constraints included fitting within the tube of their
existing rocket and ensuring autonomous actuation. The system used
aerodynamic drag flaps actuated by a servomotor and controlled by an
on-board microcontroller. They also conducted Computational Fluid
Dynamics (CFD) and Finite Element (FE) analysis for flow physics and
structural integrity \[8\].

![A diagram of a robot Description automatically
generated](./media/image3.png)
![A diagram of a robot Description automatically
generated](./media/image4.png)
Project EULER by ARIS Space in 2020 targeted a higher apogee of 30,000
feet. The project faced challenges with radial forces affecting
actuation and had to iterate their airbrake design. Despite a parachute
failure that led to rocket destruction, telemetry and accelerometer data
confirmed successful airbrake deployment \[9\]. 

![A close up of a pen Description automatically
generated](./media/image5.png)
![A heat map of a pipe Description automatically generated with medium
confidence](./media/image6.png)
ThrustMIT focused on designing a low-cost airbrake system. They employed
a 4th-order Runge-Kutta method for real-time apogee prediction and used
a Teensy 4.1 microcontroller for high computational power. The airbrakes
were made of aluminum and designed to withstand high forces. Safety
measures included a virtual floor of 5000ft to prevent unwanted
deployment \[10\]. 

![A collage of images of a mechanical device Description automatically
generated](./media/image7.png)

Another paper by ThrustMIT presents an optimization method for the
Runge-Kutta 4th Order Method used as part of the control scheme. This
Neural Network-based optimization technique aimed to improve
computational efficiency and allow a higher number of predictions during
the control period. The Neural Network was trained on data generated
from traditional RK4 simulations and could predict the airbrake state in
real-time \[11\].

The 10,000ft airbrakes system adopted by ARIS in 2018 uses three control
surfaces oriented perpendicularly to the roll axis to modulate drag,
activated by a servo motor based on sensor feedback, to fine-tune ascent
dynamics. The control strategy is supported by a software framework
comprising a trajectory simulator for validation and planning, dynamic
programming for optimal trajectory planning, an online control algorithm
that adjusts air brakes in real-time based on IMU and barometer data,
and a verification module that tests the system\'s reliability against
various failure scenarios. The IMU readings were prioritized during
ascent phase as it was found that test flights yielded a bias in the
barometer readings for high velocities \[12\]. This bias could be
attributed to the requirement for properly sized and tested pressure
ports \[13\], \[14\].

![A close-up of a circular object Description automatically
generated](./media/image8.png)
In 2018 the University of Ottawa Student Team of Aeronautics and
Rocketry employed flaps perpendicular to the roll axis to compensate for
the intentional overshooting. The system employs Model Predictive
Control (MPC) to predict the rocket\'s path to final apogee by
simulating real-time dynamics based on sensor data for position, speed,
and orientation. This predicted apogee is compared to the target apogee
of 10,000 ft, and the resulting error informs the optimal deployment
angle of the air brakes, calculated using a drag model derived from CFD
simulations. Commands are then relayed to actuate the servo motor
controlling the air brakes.

![A diagram of an orange scheme Description automatically generated with
medium
confidence](./media/image9.png)
An MPC-based approach is desirable as it allows for dynamic correction
of trajectory errors using an adaptive and nonlinear control schema
based on the system model \[15\], making it highly effective in
responding to real-time changes in rocket dynamics and environmental
conditions \[6\].

These studies collectively contribute to the understanding of airbrake
systems for rockets, each offering unique methodologies, designs, and
algorithms and a view into possible constraints, challenges, and
opportunities.


## References
\[6\] T. Lew, F. Lyck, and G. Müller, "Chance-Constrained Optimal
Altitude Control of a Rocket," 2019, \[Online\]. Available:
https://aris-space.ch/wp-content/uploads/2021/12/EUCASS2019_388.pdf

\[7\] H. Dragesun *et al.*, "Apogee Precision With Airbrake Control and
SRAD Rocket Simulator," *Spaceport America Cup Conference Podium
Session*, pp. 36--37, 2019.

\[8\] B. Taylor, "MECH 460: Final Report. Active Rocket Apogee Control
(ARAC)," Dec. 2018, \[Online\]. Available:
https://offroad.engineering.queensu.ca/wp-content/uploads/2020/05/MECH-460-Final-Report-Team-03.pdf

\[9\] S. Borne, "Project EULER: supersonic sounding rocket \| The
Eclectic Coder." Accessed: Sep. 29, 2023. \[Online\]. Available:
https://seanbone.ch/project-euler/

\[10\] ThrustMIT, "Peak of Flight Newsletter: How to Design Airbrakes in
a Sounding Rocket." Accessed: Sep. 29, 2023. \[Online\]. Available:
https://www.apogeerockets.com/education/downloads/Newsletter599.pdf

\[11\] T. Agrawal and U. Anand, "Optimization of a Runge-Kutta 4th Order
Method-based Airbrake Control System for High-Speed Vehicles Using
Neural Networks." arXiv, Jul. 22, 2023. doi: 10.48550/arXiv.2307.12038.

\[12\] ARIS, "Team 100 Project Technical Report to the 2018 Spaceport
America Cup," Zurich, Switzerland, 2018. Accessed: Apr. 07, 2024.
\[Online\]. Available:
https://www.soundingrocket.org/uploads/9/0/6/4/9064598/100_project_report.pdf

\[13\] "Most Accurate Way to Measure Velocity: Accelerometer vs
Barometer vs ?," Rocketry Forum - Model Rocketry Forums. Accessed: Apr.
07, 2024. \[Online\]. Available:
https://www.rocketryforum.com/threads/most-accurate-way-to-measure-velocity-accelerometer-vs-barometer-vs.157866/

\[14\] D. Walker, "Sizing static ports for altimeter sampling --
Cambridge University Spaceflight." Accessed: Apr. 07, 2024. \[Online\].
Available:
https://www.cusf.co.uk/2016/09/sizing-static-ports-of-altimeter-sampling/

\[15\] M. Schwenzer, M. Ay, T. Bergs, and D. Abel, "Review on model
predictive control: an engineering perspective," *Int J Adv Manuf
Technol*, vol. 117, no. 5--6, pp. 1327--1349, Nov. 2021, doi:
10.1007/s00170-021-07682-3.
