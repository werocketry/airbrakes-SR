# Conceptual Design
Consists of the generation and evaluation of proposed designs.

## Mechanical Concept Generation

After conducting the study on prior art and emerging technologies, the
concept generation process began. Through structured brainstorming and
extensive research, four distinct concepts for the airbrake system's
mechanical design were developed.

### Pancake 

Pancake-style airbrakes are characterized by radially deploying flaps
that can be controlled by a servo or stepper motor. This design offers a
compact solution that incorporates flaps that are initially flush with
the rocket's airframe and then extend outwards, perpendicular to the
airflow. These extended flaps generate drag, thus reducing the airspeed
of the rocket. The pancake airbrakes can be driven by a slider crank
mechanism or geared together. The flaps are typically made of aluminum,
ensuring robustness while minimizing weight. Figure 9 depicts an example
of the pancake style airbrakes used in École Polytechnique Fédérale de
Lausanne's rocket design that competed in the Spaceport America Cup in
2018. 

![No photo description
available.](./media/image10.jpeg)

### Flaps 

Flaps-style airbrakes are a commonly used design in model rocketry that
offer precise apogee control. This design consists of hinged panels or
flaps that are initially flush with the rocket's airframe and then
deploy to induce drag. The flaps can be controlled remotely or be
programmed to actuate at specific speeds or altitudes. For deployment, a
servo or stepper motor can move a single platform along a lead screw to
actuate rods up and down. As the lead screw is actuated, the hinges move
out of the airframe to deploy the flaps. The flaps can be made of either
aluminum or carbon fiber. Figure 10 provides an example of a flap-style
airbrake system.

![A metal cylinder with metal rods Description automatically generated
with medium
confidence](./media/image11.png)

### Doppler Hole

The Doppler hole style of airbrakes is a novel, never tested concept
where holes are strategically cut into the rocket structure to generate
drag. These openings allow air to flow into the rocket body and increase
the rocket's drag. As the number of holes increases, the more drag is
produced. Unlike the other generated concepts, this style of airbrake
operates passively, and cannot be adjusted, negating the need for a
control system. Critical factors involved in this design are the size,
shape, and placement of the holes. Figure 11 depicts a conceptual model
of the doppler hole airbrake system.

![A close up of a black and white object Description automatically
generated](./media/image12.png)

### Origami Flashers

The origami flasher airbrakes are an adaptation of the pancake style
airbrakes. As the name suggests, this design is inspired by the Japanese
art of paper folding. In this concept, the intricate folding pattern is
deployed and creates a geometric surface that generates drag. The
controlled unfolding of the pattern is a critical aspect of the design
and can be achieved using mechanical actuators, spring, or pyrotechnics.
The geometric pattern must be carefully optimized to achieve the desired
aerodynamic performance that meets the project requirements. An example
of the origami flasher concept is provided in Figure 12.

![Jcs 05 00147 g014
550](./media/image13.jpeg)

## Mechanical Concept Evaluation 

After the concept generation phase, the next step in the design process
was to evaluate each concept to determine which approach will best meet
the project objectives and requirements. Comprehensive criteria were
then developed to assess each concept. The specific criteria included:

1.  Precision Apogee Targeting

2.  Safety

3.  Technology Readiness Level (TRL)

4.  Electrical Simplicity

5.  Mechanical Simplicity

6.  Ease to Simulate

7.  Simulation Accuracy

8.  Cost

9.  Ease of Manufacture

10. Mass

11. Durability

12. Redundancy

13. Length

14. Repairability

15. Reliable Deployment

16. Auto-Closing

Using the above criteria, a House of Quality (HOQ) and Pugh Matrix were
constructed to compare each concept. The HOQ and Pugh Matrix can be
found in Appendix I. In both methods, the concept that scored the
highest was the flap style airbrakes. The flap style airbrakes system
triumphed compared to other designs for its high durability, redundancy,
ease of manufacturability, and easy repairability. The flap style design
also has flight heritage and a high TRL, unlike the Doppler hole and
origami flashers concepts, which have both never been flown before.

At the concept selection phase, the airbrakes design consisted of four
flaps. Four flaps in the design meant that a critical safety feature
could be implemented such that the flaps retract in a neutral state if
one of them fails. This feature was considered incredibly important and
was a primary factor for choosing the flaps style airbrakes. However, in
January, the rocketry team shifted the rocket design to have three fins
instead of four. The number of flaps must match the number of fins to
ensure adequate stability of the rocket. Consequently, the design change
to three flaps meant the auto-retracting feature could no longer be
implemented. Instead, the software must include a feature to detect the
failure of a single flap and cause the airbrakes to retract.

The areas in which the flaps style design scored lower than the other
concepts were length and mass. However, the system requirements defined
a large range for these criteria that the airbrakes design can easily
meet. Careful consideration for material and design choices would also
make the flap style airbrakes successfully meet these requirements.

## Electrical Concept Generation

After conducting the study on prior art and emerging technologies, the
concept generation process began. Through structured brainstorming and
extensive research, four distinct concepts for the airbrake system's
mechanical design were developed.

### Commercial-off-the-Shelf (COTS) Flight Computer

This idea centers on employing a commercial flight computer to integrate
into the airbrakes system. This flight computer would process crucial
flight data such as altitude and velocity to make decisions on the fly
regarding the deployment of airbrakes. Communication between the flight
computer and the actuation mechanism of the airbrakes could be achieved
through I2C or serial connections linked to a microcontroller unit (MCU)
that would directly manage the actuator. There would also be the
possibility of programming the flight computer's outputs to take control
of the actuation mechanism on its own. The advantage of this approach
lies in its potential to slash development time by leveraging
pre-constructed components, coupled with the high reliability that
commercial flight computers are known for. However, this method might
fall short in terms of customization capabilities, and would likely be
more costly than bespoke solutions, and introduces a dependency on
external suppliers for technical support.

### Microcontroller Unit (MCU)

Opting for an MCU as the backbone of the electrical scheme affords the
liberty to create a tailored flight program to monitor and control the
airbrakes mechanism. This approach requires programming the MCU to
interpret inputs from various sensors and execute airbrake deployment
based on established criteria. Selection criteria for the MCU would
hinge on its processing prowess, I/O capabilities, and sensor and
actuator compatibility. This path provides a high level of
customization, allowing for potentially better alignment with specific
project requirements and direct oversight over system integration.
Furthermore, MCUs are more economically feasible compared to
off-the-shelf alternatives. Nevertheless, it comes with its share of
challenges, including a lengthy development and testing phase of the
complete program, and a heightened risk of encountering bugs and
reliability issues without comprehensive testing.

### Field-Programmable Gate Array (FGPA)

Integrating an FPGA into the design allows for an advanced,
customizable, and performance-tuned control system. FPGAs are renowned
for their programmability to execute specific control logic and
processing tasks at remarkable speeds, which is ideal for real-time
applications such as high-speed active control. This option involves
crafting the logic and control algorithms for FPGA implementation. The
strengths of employing an FPGA include unparalleled real-time processing
and control performance, immense design flexibility and
reconfigurability, and the efficient handling of complex algorithms and
control logic. However, FPGAs come with a steeper learning curve and
greater complexity in programming compared to MCUs, generally higher
initial costs for development tools and components, and necessitate
specialized expertise for effective deployment.

## Electrical Concept Evaluation

After an extensive evaluation of the various electrical concepts for the
airbrakes system, the team decided to proceed with a Microcontroller
Unit (MCU)-based architecture. This decision aligns with our project's
specific needs, constraints, and goals, emphasizing the balance between
customization, cost-effectiveness, and manageable development timelines.

The choice of an MCU was driven by its superior flexibility in
customization. This allows our team to develop a flight computer and
actuator control programs tailored to our system, a level of specificity
that commercial-off-the-shelf (COTS) solutions cannot match. The ability
to finely tune and optimize the system is paramount, especially in
achieving the precision necessary for airbrake deployment to hit the
target apogee with minimal deviation. This customization capability is
crucial, even more so because the Western Engineering Rocketry Team is
moving towards developing their own Student Research and Developed
(SRAD) flight computers for future avionics applications. Adopting an
MCU for this project represents a strategic step towards building
in-house expertise in custom flight computer development, setting a
foundational knowledge base for future projects.

From a financial perspective, an MCU-based solution presents a more
economical option compared to both COTS flight computers and the more
advanced FPGA alternatives. The lower cost of MCUs, coupled with their
widespread availability and the extensive support materials available,
renders this path particularly attractive for a student project with
budgetary constraints.

The development timeframe was another critical factor in the decision to
choose an MCU. Despite the high performance and real-time processing
capabilities of FPGAs, they require specialized programming skills and
come with a steeper learning curve. Given the team\'s relative
proficiency with MCU programming and the abundant resources and
community support available for various MCU platforms, there is an
anticipation of a smoother and quicker development and testing phase
with an MCU, ensuring project timelines are met efficiently. Moreover,
the broad support for MCUs from both manufacturers and a global
community of developers offers an invaluable resource. 

However, selecting an MCU over a COTS flight computer comes with its own
set of implications that the team is cognizant of. While there is a gain
in customization and cost, the increased responsibility on the
development team must be acknowledged to ensure the reliability and
robustness of our custom solution. Developing the flight software
demands a comprehensive understanding of the system's requirements and a
thorough approach to testing and validation. Furthermore, this choice
necessitates a proactive approach to both the overall system design as
well as the subsequent documentation and knowledge transfer to ensure
that future teams can build upon the capstone team's work.
