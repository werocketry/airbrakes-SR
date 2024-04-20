# Introduction

The Western Engineering Rocketry Team competes annually in the
Intercollegiate Rocket Engineering Competition. For the 2023-2024
iteration, the team aims to improve apogee targeting by integrating an
airbrake system into their rocket designed to reach 10, 000 feet. The
main challenge is engineering an airbrake system that will induce a
controlled amount of drag during the rocket's ascent to closely achieve
the desired apogee. The project encompasses multiple domains, including
mechanical, electrical and software design.  

The project began with concept generation that involved brainstorming
sessions, research, and cross-disciplinary collaboration. Various
concepts, notably flap-style and pancake-style airbrakes, were explored.
After a comprehensive evaluation process, the flap-style airbrake
concept was selected as the most promising for the project. 

The detailed design phase focused on creating a CAD model, engineering
drawings, and material selection for the airbrake components. Iterative
design reviews and feedback ensured the final design met the project
requirements.

Prior to the manufacturing of the functional prototype, extensive
simulations were conducted to validate the design. Finite Element
Analysis and Computational Fluid Dynamics were employed to guide the
design and ensure safety margins would be met.

The mechanical design when manufactured and assembled functioned as
intended and inspired confidence that it will perform well during
flight. A few changes were made to the design during the prototyping
stage as various small problems arose during assembly. The first change
made was the addition of a motor mount to adequately secure the motor to
the top platform and the lead screw. The second change made was to add
platform support members, which served two purposes. First, these
supports guaranteed a fixed distance between the top and bottom
platforms, ensuring that there will be no binding of the lead screw.
Secondarily, it means that the airbrake system can be installed as a
single unit into a coupler tube, vastly simplifying the rocket
installation process.


## Description of Need

The Western Engineering Rocketry Team (WE Rocketry) competes annually at
the Spaceport America Cup, the largest intercollegiate rocketry
competition in the world. For the 2024 competition, the team will be
competing in the 10k feet COTS motor category.

At competition, 35% of a team's score is based on how close their apogee
is to their competition category's target apogee. The most competitive
teams at the competition hit within 100 ft of their apogee target \[1\].
Doing so reliably without the use of an active flight control system is
unfeasible, as minor variations in conditions that are outside of the
team's control (including atmospheric conditions, motor thrust
variability, and the launch rail angle set by Range Safety Officers on
launch day \[2\]) can lead to significant deviations from what can be
simulated, or even achieved in a previous test flight.

The most commonly used form of active control for precision apogee
targeting at competition are airbrakes systems \[3\]. WE Rocketry
intends to integrate an airbrakes system into their rocket for the 2024
Spaceport America Cup to target a 10,000-foot apogee with more precision
than would be possible without an active control system.

##  Report Scope

This report and the other files provided alongside it (part drawings,
the costed BOM, and the project Gantt chart) constitute the final
deliverables of the capstone course, and as such provide a summary of
all the work done on this project up until the due date of the report.
It should be noted at the outset that the airbrakes project does not end
with the conclusion of the capstone course. Further work needs to be
done before the competition in June, and forward-looking remarks for
this project are included in Section 14: Recommendations, Future Design
Directions.

# Problem Definition

The capstone project was undertaken with the objective of creating WE
Rocketry's first airbrakes system to make the team more competitive at
the Spaceport America Cup. An airbrakes system is an electromechanical
assembly that extends outwards from the body of a rocket or aircraft
during flight to induce drag to decelerate the rocket or aircraft. There
are different ways of implement aerobraking on a rocket -- the two most
common of which are flap-style and pancake-style systems, which will be
discussed in more detail in Section 9: State-of-the-Art and Emerging
Technologies and Section 10: Concept Generation and Evaluation -- but
the main principles stay the same regardless of the mechanism (by
extending a control surface into the freestream flow to induce drag).

There are many considerations that must be made when fitting a rocket
with an airbrakes system. Ensuring the rocket's structural integrity and
aerodynamic stability are of paramount importance. The requirements in
the following section are the result of the first phase of the design,
which defined the scope of the problem, as well as the requirements and
constraints for the airbrakes system.

## References
\[1\] "2023 SA Cup," ESRA. Accessed: Apr. 08, 2024. \[Online\].
Available: https://www.soundingrocket.org/2023-sa-cup.html

\[2\] "Spaceport America Cup Intercollegiate Rocket Engineering
Competition Design, Test, & Evaluation Guide." The Experimental Sounding
Rocket Association (ESRA), Oct. 24, 2023. Accessed: Apr. 08, 2024.
\[Online\]. Available:
https://www.soundingrocket.org/uploads/9/0/6/4/9064598/2023-sa_cup_dteg_v2.2.9_10-24-23.pdf

\[3\] "IREC Reports - Google Drive." Accessed: Apr. 08, 2024.
\[Online\]. Available:
https://drive.google.com/drive/folders/14pfiOCJ2Xkqqd72IAzEHdSXjxMHer6_0
