# Design Requirements and Constraints

## Preamble

The following is an outline of the most important design requirements
for the airbrakes system, as needed to understand the contents of the
final report. Other requirements that did not have a major effect on the
contents of this report may be found in Rev 1 of the Project
Requirements document.

The design requirements were generated primarily from two sources:
consultation with the rocketry team to determine the specifications of
an airbrakes system that could be integrated into this year's rocket,
and competition requirements, principally those found in the DTEG \[2\],
the competition Rules and Requirements Document \[4\], and the Range
Standard Operating Procedures \[5\].

The requirements laid out in the following sections fall into two
categories:

1.  "Shall" requirements are requirements that must be met for the
    system to conform to this specification.

2.  "Should" requirements are recommendations which would be nice to
    have and which the team should endeavour to achieve if it is
    feasible and does not come at the expense of failing to meet any
    "shall" requirement(s).

## Functional Requirements

The functional requirements define the features and/or functions of the
airbrake system that must be implemented to achieve the desired
outcomes. Table 1 provides a summary of the most important functional
requirements, along with the rationale for each.
| **Requirement ID** | **Requirement**                                                                   | **Rationale**                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|--------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-002             | The system shall induce the correct amount of drag such that the rocket achieves its 10,000 ft target apogee to within +/- 200 ft. | The purpose of the airbrakes system is to enable the rocket to have a final apogee of as close as possible to 10,000 ft to maximize the team's flight score as laid out in section 2.7.1.4 of the SAC Rules & Requirements Document [4]. This score given for precise apogee targeting is 35% of the total points that a team can earn during the competition. +/- 200 ft is an achievable goal for most teams using airbrakes at SAC. Being 200 ft off-target would result in the rocketry team achieving 327 out of 350 possible points for final apogee, as per section 2.7.1.4 of the SAC Rules & Requirements Document [4]. |
| FR-003             | The system shall survive exposure to 13.58gs of force when in its stowed configuration. | As determined by flight simulations (OpenRocket, RocketPy, custom flight simulator). See Section 11.4.5 for the determination of the value. |
| FR-004             | The system shall survive exposure to the aerodynamic loading expected during max q: 48.7 kPa. | As determined by flight simulations (OpenRocket, RocketPy, custom flight simulator). See Section 11.4.5 for the determination of the value. Note that the flaps will never be deployed at max-q, because as per section 7.4 in SAC Design, Test, & Evaluation Guide, that is when they may begin to deploy [2]. |
| FR-006             | The system shall default to a neutral state if any of the following occur: - The controller sends an abort signal. - Primary system power is lost. - The rocket's attitude exceeds 30° from its launch elevation. | A neutral state is defined as one which does not apply any moments to the rocket.|
| FR-007             | The system shall remain in a neutral state until at least one of the following have occurred: - The rocket's boost phase has ended (i.e., all propulsive stages have ceased producing thrust), - The launch vehicle has crossed the point of maximum aerodynamic pressure (max Q) in its trajectory, - Or the launch vehicle has reached an altitude of 6,500 ft (2,000 m) AGL. | A neutral state is defined as one which does not apply any moments to the rocket. Competition requirement as per section 7.4 in SAC Design, Test, & Evaluation Guide [2]. The rocket has virtually no chance of clearing 20,000 ft before either of the first two conditions are met. In addition, with a single stage rocket of the order of magnitude of the WE Rocketry Team's previous rocket in the 10,000 ft category, the first two conditions will be met within a second of each other (as determined by the flight simulations detailed in Section 11.4). Therefore, the airbrakes can easily target a second or two after engine cut-off for a release of its mechanical locking system. |


## Physical Requirements

The physical requirements define the physical attributes, including
dimensions and material requirements, of the airbrake system. Table 2
provides a summary of the most important physical requirements for the
system, along with the rationale for each.
| **Requirement ID** | **Requirement**                                                      | **Rationale**                                                                                                                                                                                                         |
|--------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PR-001             | The system shall have a 5.5'' diameter when in its neutral/stowed state. | The rocket will have a 5.5'' diameter. The flaps cannot stick out of the airframe when stowed, and the transfer of force along the longitudinal axis of the rocket would be less safe if the outer diameter of the structure was smaller over the airbrakes section. |
| PR-002             | The system shall have a mass of less than 4 kg.                      | 4 kg is the maximum mass that WE Rocketry is willing to allocate to the airbrakes system. |
| PR-003             | The system shall be less than 30 cm long.                            | The system must both reasonably fit within a body tube section along with other components, and not elongate the rocket so much as to undermine its stability. 30 cm is the length allotted by WE Rocketry to the airbrakes system, and is consistent with the length of other airbrakes systems observed at competition. |

## Electrical Requirements

The electrical requirements refer to the electrical specifications that
the airbrake system must comply with to achieve the desired outcomes.
Table 3 provides a summary of the most important electrical requirements
for the system, along with the rationale for each.
| **Requirement ID** | **Requirement Description**                          | **Rationale**                                                                                                                                                                                                                              |
|--------------------|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ER-002             | The system shall have safety-critical wiring with proper cable management for airbrake deployment. | Wiring associated with airbrake deployment is considered safety-critical since it can affect the rocket trajectory or stability as per Sections 6.11 & 6.12 of the SAC Design, Test, & Evaluation Guide [2].                                   |
| ER-003             | The system shall have a dedicated power supply separate from the rocket's main avionics. | To ensure that the airbrake system remains operational even if the main avionics fail.  |
| ER-004             | The battery shall provide a minimum of 20 hours of continuous operation and support the electrical demands of the actuator. | A 12 V battery is chosen to directly power the motor for the airbrakes, which generally require higher voltages for optimal performance.  |
| ER-005             | The system shall have real-time data acquisition from accelerometers and pressure sensors. | Real-time data is essential for adaptive control of airbrakes during flight.|
| ER-006             | The electrical subsystem shall incorporate fail-safe logic that mechanically locks the airbrakes in a neutral state upon loss of electrical power. | To meet FR-006 and ensure safety in case of system failure. |
| ER-007             | The electrical subsystem and its components shall be capable of operating in a temperature range of 5°C to 70°C. | To comply with ENR-003 and ensure functionality under harsh and varying environmental conditions.  |

## Programmatic Requirements

The programmatic requirements refer to the specific needs that are
required to meet technological, programmatic, or regulatory demands.
Table 4 provides a summary of the most important programmatic
requirements for the system, along with the rationale for each.


## References
\[2\] "Spaceport America Cup Intercollegiate Rocket Engineering
Competition Design, Test, & Evaluation Guide." The Experimental Sounding
Rocket Association (ESRA), Oct. 24, 2023. Accessed: Apr. 08, 2024.
\[Online\]. Available:
https://www.soundingrocket.org/uploads/9/0/6/4/9064598/2023-sa_cup_dteg_v2.2.9_10-24-23.pdf
\[4\] "Spaceport America Cup Intercollegiate Rocket Engineering
Competition Rules & Requirements Document." The Experimental Sounding
Rocket Association (ESRA), Mar. 04, 2024. Accessed: Apr. 08, 2024.
\[Online\]. Available:
https://www.soundingrocket.org/uploads/9/0/6/4/9064598/sa_cup_irec_rules_and_requirements_document\_-2024_v1.4_20240304.pdf

\[5\] "Spaceport America Cup Range Standard Operating Procedures." The
Experimental Sounding Rocket Association (ESRA), Jun. 15, 2023.
Accessed: Apr. 08, 2024. \[Online\]. Available:
https://www.soundingrocket.org/uploads/9/0/6/4/9064598/sa_cup_irec_range_standard_operating_procedures_2023-a.pdf

